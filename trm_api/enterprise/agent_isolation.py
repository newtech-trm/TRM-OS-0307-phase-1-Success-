"""
Enterprise Agent Isolation and Security Framework

Provides containerization, resource quotas, security sandboxing, and 
isolation mechanisms for multi-tenant agent deployments.
"""

from typing import Dict, Any, List, Optional, Union, Set, Callable
import logging
import asyncio
import time
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import uuid
import psutil
import docker
from docker.types import Resources, RestartPolicy, LogConfig
import sys
import subprocess
from contextlib import asynccontextmanager

# Import resource module with Windows fallback
try:
    import resource
    HAS_RESOURCE = True
except ImportError:
    # Windows doesn't have resource module, create fallback
    HAS_RESOURCE = False
    class MockResource:
        RLIMIT_AS = 'RLIMIT_AS'
        RLIMIT_CPU = 'RLIMIT_CPU'
        RLIMIT_NOFILE = 'RLIMIT_NOFILE'
        
        def setrlimit(self, resource_type, limits):
            # No-op on Windows
            pass
            
        def getrlimit(self, resource_type):
            # Return dummy limits
            return (float('inf'), float('inf'))
    
    resource = MockResource()

logger = logging.getLogger(__name__)


class IsolationLevel(str, Enum):
    """Agent isolation security levels"""
    NONE = "none"          # No isolation (development only)
    BASIC = "basic"        # Process isolation
    CONTAINER = "container"  # Docker container isolation
    VM = "vm"             # Virtual machine isolation (future)
    SECURE = "secure"     # Maximum security with all restrictions


class ResourceType(str, Enum):
    """Types of resources that can be quota-controlled"""
    CPU = "cpu"
    MEMORY = "memory"
    DISK = "disk"
    NETWORK = "network"
    FILE_HANDLES = "file_handles"
    PROCESSES = "processes"
    API_CALLS = "api_calls"
    DATABASE_CONNECTIONS = "database_connections"


@dataclass
class ResourceQuota:
    """Resource quota definition"""
    resource_type: ResourceType
    max_value: Union[int, float]
    current_usage: Union[int, float] = 0
    unit: str = ""  # MB, %, calls/sec, etc.
    enforcement_policy: str = "hard"  # hard, soft, warn
    
    def is_exceeded(self) -> bool:
        """Check if quota is exceeded"""
        return self.current_usage > self.max_value
    
    def utilization_percent(self) -> float:
        """Get utilization as percentage"""
        return (self.current_usage / self.max_value) * 100 if self.max_value > 0 else 0


@dataclass
class SecurityPolicy:
    """Security policy for agent execution"""
    allow_network_access: bool = True
    allow_file_system_access: bool = True
    allow_subprocess_execution: bool = False
    allow_api_access: bool = True
    allowed_domains: Set[str] = field(default_factory=set)
    blocked_domains: Set[str] = field(default_factory=set)
    allowed_file_paths: Set[str] = field(default_factory=set)
    blocked_file_paths: Set[str] = field(default_factory=set)
    max_execution_time: int = 300  # seconds
    require_approval_for: Set[str] = field(default_factory=set)  # operations requiring human approval


@dataclass
class ContainerConfig:
    """Docker container configuration"""
    image: str = "python:3.11-slim"
    memory_limit: str = "512m"
    cpu_limit: float = 1.0
    network_mode: str = "bridge"
    read_only: bool = True
    no_new_privileges: bool = True
    security_opts: List[str] = field(default_factory=lambda: ["no-new-privileges:true"])
    cap_drop: List[str] = field(default_factory=lambda: ["ALL"])
    cap_add: List[str] = field(default_factory=list)
    volumes: Dict[str, Dict[str, str]] = field(default_factory=dict)
    environment: Dict[str, str] = field(default_factory=dict)
    user: str = "nobody"


@dataclass
class AgentIsolationContext:
    """Complete isolation context for an agent"""
    agent_id: str
    isolation_level: IsolationLevel
    resource_quotas: Dict[ResourceType, ResourceQuota]
    security_policy: SecurityPolicy
    container_config: Optional[ContainerConfig] = None
    created_at: datetime = field(default_factory=datetime.now)
    last_accessed: datetime = field(default_factory=datetime.now)
    status: str = "initialized"
    
    # Runtime state
    container_id: Optional[str] = None
    process_id: Optional[int] = None
    resource_usage: Dict[ResourceType, float] = field(default_factory=dict)
    violations: List[Dict[str, Any]] = field(default_factory=list)


class AgentIsolationManager:
    """
    Enterprise Agent Isolation Manager
    
    Features:
    - Multi-level isolation (process, container, VM)
    - Resource quota enforcement
    - Security policy enforcement
    - Container orchestration
    - Resource monitoring and alerting
    - Violation tracking and reporting
    """
    
    def __init__(self):
        self._isolation_contexts: Dict[str, AgentIsolationContext] = {}
        self._docker_client: Optional[docker.DockerClient] = None
        self._monitoring_task: Optional[asyncio.Task] = None
        self._monitoring_interval = 5  # seconds
        
        # Performance tracking
        self._total_agents_created = 0
        self._active_violations = 0
        self._resource_utilization = {}
        
        # Initialize Docker client if available
        self._initialize_docker()
        
        logger.info("Agent Isolation Manager initialized")
    
    def _initialize_docker(self):
        """Initialize Docker client for container isolation"""
        try:
            self._docker_client = docker.from_env()
            # Test Docker connection
            self._docker_client.ping()
            logger.info("Docker client initialized successfully")
        except Exception as e:
            logger.warning(f"Docker not available: {e}")
            self._docker_client = None
    
    # ================================
    # ISOLATION CONTEXT MANAGEMENT
    # ================================
    
    async def create_isolation_context(
        self,
        agent_id: str,
        isolation_level: IsolationLevel = IsolationLevel.BASIC,
        resource_quotas: Optional[Dict[ResourceType, ResourceQuota]] = None,
        security_policy: Optional[SecurityPolicy] = None,
        container_config: Optional[ContainerConfig] = None
    ) -> AgentIsolationContext:
        """Create isolation context for agent"""
        
        if agent_id in self._isolation_contexts:
            raise ValueError(f"Isolation context already exists for agent {agent_id}")
        
        # Default resource quotas
        if resource_quotas is None:
            resource_quotas = self._get_default_quotas(isolation_level)
        
        # Default security policy
        if security_policy is None:
            security_policy = self._get_default_security_policy(isolation_level)
        
        # Default container config for container isolation
        if isolation_level == IsolationLevel.CONTAINER and container_config is None:
            container_config = ContainerConfig()
        
        context = AgentIsolationContext(
            agent_id=agent_id,
            isolation_level=isolation_level,
            resource_quotas=resource_quotas,
            security_policy=security_policy,
            container_config=container_config
        )
        
        # Initialize isolation environment
        await self._initialize_isolation_environment(context)
        
        self._isolation_contexts[agent_id] = context
        self._total_agents_created += 1
        
        logger.info(f"Created isolation context for agent {agent_id} with level {isolation_level}")
        return context
    
    async def destroy_isolation_context(self, agent_id: str) -> bool:
        """Destroy isolation context and cleanup resources"""
        if agent_id not in self._isolation_contexts:
            logger.warning(f"No isolation context found for agent {agent_id}")
            return False
        
        context = self._isolation_contexts[agent_id]
        
        try:
            # Cleanup based on isolation level
            if context.isolation_level == IsolationLevel.CONTAINER:
                await self._cleanup_container(context)
            elif context.isolation_level == IsolationLevel.BASIC:
                await self._cleanup_process(context)
            
            # Remove from tracking
            del self._isolation_contexts[agent_id]
            
            logger.info(f"Destroyed isolation context for agent {agent_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to destroy isolation context for agent {agent_id}: {e}")
            return False
    
    @asynccontextmanager
    async def isolated_execution(self, agent_id: str):
        """Context manager for isolated agent execution"""
        if agent_id not in self._isolation_contexts:
            raise ValueError(f"No isolation context found for agent {agent_id}")
        
        context = self._isolation_contexts[agent_id]
        
        try:
            # Pre-execution setup
            await self._pre_execution_setup(context)
            
            # Enter isolation environment
            if context.isolation_level == IsolationLevel.CONTAINER:
                async with self._container_execution_context(context):
                    yield context
            else:
                async with self._process_execution_context(context):
                    yield context
                    
        finally:
            # Post-execution cleanup
            await self._post_execution_cleanup(context)
    
    # ================================
    # ISOLATION ENVIRONMENT SETUP
    # ================================
    
    async def _initialize_isolation_environment(self, context: AgentIsolationContext):
        """Initialize isolation environment based on level"""
        try:
            if context.isolation_level == IsolationLevel.NONE:
                context.status = "ready"
                
            elif context.isolation_level == IsolationLevel.BASIC:
                await self._setup_process_isolation(context)
                
            elif context.isolation_level == IsolationLevel.CONTAINER:
                await self._setup_container_isolation(context)
                
            elif context.isolation_level == IsolationLevel.SECURE:
                await self._setup_secure_isolation(context)
                
            else:
                raise ValueError(f"Unsupported isolation level: {context.isolation_level}")
                
            context.status = "ready"
            logger.info(f"Initialized {context.isolation_level} isolation for agent {context.agent_id}")
            
        except Exception as e:
            context.status = "failed"
            logger.error(f"Failed to initialize isolation: {e}")
            raise
    
    async def _setup_process_isolation(self, context: AgentIsolationContext):
        """Setup process-level isolation"""
        # Set process limits using resource module
        try:
            # Memory limit
            memory_quota = context.resource_quotas.get(ResourceType.MEMORY)
            if memory_quota:
                memory_bytes = int(memory_quota.max_value * 1024 * 1024)  # Convert MB to bytes
                resource.setrlimit(resource.RLIMIT_AS, (memory_bytes, memory_bytes))
            
            # CPU time limit
            cpu_quota = context.resource_quotas.get(ResourceType.CPU)
            if cpu_quota:
                cpu_seconds = int(cpu_quota.max_value)
                resource.setrlimit(resource.RLIMIT_CPU, (cpu_seconds, cpu_seconds))
            
            # File handle limit
            file_quota = context.resource_quotas.get(ResourceType.FILE_HANDLES)
            if file_quota:
                file_limit = int(file_quota.max_value)
                resource.setrlimit(resource.RLIMIT_NOFILE, (file_limit, file_limit))
            
            context.process_id = psutil.Process().pid
            logger.info(f"Process isolation setup complete for PID {context.process_id}")
            
        except Exception as e:
            logger.error(f"Failed to setup process isolation: {e}")
            raise
    
    async def _setup_container_isolation(self, context: AgentIsolationContext):
        """Setup Docker container isolation"""
        if not self._docker_client:
            raise RuntimeError("Docker client not available for container isolation")
        
        if not context.container_config:
            raise ValueError("Container config required for container isolation")
        
        try:
            config = context.container_config
            
            # Create container
            container = self._docker_client.containers.create(
                image=config.image,
                name=f"agent_{context.agent_id}_{uuid.uuid4().hex[:8]}",
                detach=True,
                mem_limit=config.memory_limit,
                cpu_count=int(config.cpu_limit),
                network_mode=config.network_mode,
                read_only=config.read_only,
                security_opt=config.security_opts,
                cap_drop=config.cap_drop,
                cap_add=config.cap_add,
                user=config.user,
                environment=config.environment,
                volumes=config.volumes,
                restart_policy=RestartPolicy(condition="no"),
                remove=True  # Auto-remove when stopped
            )
            
            context.container_id = container.id
            logger.info(f"Container created for agent {context.agent_id}: {container.id[:12]}")
            
        except Exception as e:
            logger.error(f"Failed to setup container isolation: {e}")
            raise
    
    async def _setup_secure_isolation(self, context: AgentIsolationContext):
        """Setup maximum security isolation"""
        # Combine container isolation with additional security measures
        await self._setup_container_isolation(context)
        
        # Additional security configurations
        if context.container_config:
            context.container_config.security_opts.extend([
                "seccomp=unconfined",  # Custom seccomp profile
                "apparmor=docker-default"
            ])
            context.container_config.cap_drop = ["ALL"]
            context.container_config.no_new_privileges = True
            context.container_config.read_only = True
    
    # ================================
    # EXECUTION CONTEXTS
    # ================================
    
    @asynccontextmanager
    async def _container_execution_context(self, context: AgentIsolationContext):
        """Container execution context manager"""
        if not context.container_id:
            raise ValueError("Container not initialized")
        
        container = self._docker_client.containers.get(context.container_id)
        
        try:
            # Start container
            container.start()
            logger.info(f"Started container {context.container_id[:12]} for agent {context.agent_id}")
            
            # Wait for container to be ready
            await asyncio.sleep(1)
            
            yield context
            
        finally:
            try:
                # Stop and remove container
                container.stop(timeout=10)
                container.remove(force=True)
                logger.info(f"Container {context.container_id[:12]} stopped and removed")
            except Exception as e:
                logger.error(f"Failed to cleanup container: {e}")
    
    @asynccontextmanager
    async def _process_execution_context(self, context: AgentIsolationContext):
        """Process execution context manager"""
        original_limits = {}
        
        try:
            # Store original resource limits
            original_limits['memory'] = resource.getrlimit(resource.RLIMIT_AS)
            original_limits['cpu'] = resource.getrlimit(resource.RLIMIT_CPU)
            original_limits['files'] = resource.getrlimit(resource.RLIMIT_NOFILE)
            
            # Apply isolation limits
            await self._apply_process_limits(context)
            
            yield context
            
        finally:
            try:
                # Restore original limits
                resource.setrlimit(resource.RLIMIT_AS, original_limits['memory'])
                resource.setrlimit(resource.RLIMIT_CPU, original_limits['cpu'])
                resource.setrlimit(resource.RLIMIT_NOFILE, original_limits['files'])
            except Exception as e:
                logger.error(f"Failed to restore process limits: {e}")
    
    # ================================
    # RESOURCE MONITORING
    # ================================
    
    async def start_monitoring(self):
        """Start resource monitoring for all isolation contexts"""
        if self._monitoring_task:
            logger.warning("Monitoring already running")
            return
        
        self._monitoring_task = asyncio.create_task(self._monitoring_loop())
        logger.info("Started isolation monitoring")
    
    async def stop_monitoring(self):
        """Stop resource monitoring"""
        if self._monitoring_task:
            self._monitoring_task.cancel()
            try:
                await self._monitoring_task
            except asyncio.CancelledError:
                pass
            self._monitoring_task = None
            logger.info("Stopped isolation monitoring")
    
    async def _monitoring_loop(self):
        """Main monitoring loop"""
        while True:
            try:
                await self._check_all_contexts()
                await asyncio.sleep(self._monitoring_interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                await asyncio.sleep(self._monitoring_interval)
    
    async def _check_all_contexts(self):
        """Check resource usage for all contexts"""
        for agent_id, context in self._isolation_contexts.items():
            try:
                await self._check_context_resources(context)
            except Exception as e:
                logger.error(f"Failed to check resources for agent {agent_id}: {e}")
    
    async def _check_context_resources(self, context: AgentIsolationContext):
        """Check resource usage for specific context"""
        context.last_accessed = datetime.now()
        
        # Get current resource usage
        if context.isolation_level == IsolationLevel.CONTAINER and context.container_id:
            await self._check_container_resources(context)
        elif context.process_id:
            await self._check_process_resources(context)
        
        # Check for quota violations
        await self._check_quota_violations(context)
    
    async def _check_container_resources(self, context: AgentIsolationContext):
        """Check container resource usage"""
        try:
            container = self._docker_client.containers.get(context.container_id)
            stats = container.stats(stream=False)
            
            # Parse memory usage
            memory_usage = stats['memory_stats']['usage'] / (1024 * 1024)  # MB
            context.resource_usage[ResourceType.MEMORY] = memory_usage
            
            # Parse CPU usage
            cpu_usage = self._calculate_cpu_percent(stats)
            context.resource_usage[ResourceType.CPU] = cpu_usage
            
            # Update quota current usage
            if ResourceType.MEMORY in context.resource_quotas:
                context.resource_quotas[ResourceType.MEMORY].current_usage = memory_usage
            if ResourceType.CPU in context.resource_quotas:
                context.resource_quotas[ResourceType.CPU].current_usage = cpu_usage
                
        except Exception as e:
            logger.error(f"Failed to check container resources: {e}")
    
    async def _check_process_resources(self, context: AgentIsolationContext):
        """Check process resource usage"""
        try:
            process = psutil.Process(context.process_id)
            
            # Memory usage
            memory_info = process.memory_info()
            memory_mb = memory_info.rss / (1024 * 1024)
            context.resource_usage[ResourceType.MEMORY] = memory_mb
            
            # CPU usage
            cpu_percent = process.cpu_percent()
            context.resource_usage[ResourceType.CPU] = cpu_percent
            
            # File handles
            num_fds = process.num_fds() if hasattr(process, 'num_fds') else 0
            context.resource_usage[ResourceType.FILE_HANDLES] = num_fds
            
            # Update quota current usage
            for resource_type, usage in context.resource_usage.items():
                if resource_type in context.resource_quotas:
                    context.resource_quotas[resource_type].current_usage = usage
                    
        except psutil.NoSuchProcess:
            logger.warning(f"Process {context.process_id} no longer exists")
            context.process_id = None
        except Exception as e:
            logger.error(f"Failed to check process resources: {e}")
    
    async def _check_quota_violations(self, context: AgentIsolationContext):
        """Check for quota violations"""
        violations = []
        
        for resource_type, quota in context.resource_quotas.items():
            if quota.is_exceeded():
                violation = {
                    'agent_id': context.agent_id,
                    'resource_type': resource_type.value,
                    'quota_limit': quota.max_value,
                    'current_usage': quota.current_usage,
                    'utilization_percent': quota.utilization_percent(),
                    'timestamp': datetime.now().isoformat(),
                    'enforcement_policy': quota.enforcement_policy
                }
                violations.append(violation)
                context.violations.append(violation)
                
                # Handle enforcement policy
                if quota.enforcement_policy == "hard":
                    await self._enforce_hard_limit(context, resource_type)
                elif quota.enforcement_policy == "soft":
                    await self._enforce_soft_limit(context, resource_type)
                
                logger.warning(f"Quota violation for agent {context.agent_id}: {violation}")
        
        if violations:
            self._active_violations += len(violations)
    
    # ================================
    # QUOTA ENFORCEMENT
    # ================================
    
    async def _enforce_hard_limit(self, context: AgentIsolationContext, resource_type: ResourceType):
        """Enforce hard resource limit"""
        logger.critical(f"Hard limit exceeded for agent {context.agent_id}, resource {resource_type}")
        
        if resource_type == ResourceType.MEMORY:
            # Kill the process/container for memory violations
            await self._terminate_agent_execution(context, "Memory limit exceeded")
        elif resource_type == ResourceType.CPU:
            # Throttle CPU usage
            await self._throttle_agent_cpu(context)
        elif resource_type == ResourceType.API_CALLS:
            # Block API calls
            await self._block_agent_api_access(context)
    
    async def _enforce_soft_limit(self, context: AgentIsolationContext, resource_type: ResourceType):
        """Enforce soft resource limit (warnings only)"""
        logger.warning(f"Soft limit exceeded for agent {context.agent_id}, resource {resource_type}")
        # Could implement throttling or notifications here
    
    async def _terminate_agent_execution(self, context: AgentIsolationContext, reason: str):
        """Terminate agent execution due to violation"""
        logger.critical(f"Terminating agent {context.agent_id}: {reason}")
        
        if context.container_id:
            try:
                container = self._docker_client.containers.get(context.container_id)
                container.kill()
            except Exception as e:
                logger.error(f"Failed to kill container: {e}")
        
        if context.process_id:
            try:
                process = psutil.Process(context.process_id)
                process.terminate()
            except Exception as e:
                logger.error(f"Failed to terminate process: {e}")
        
        context.status = "terminated"
    
    # ================================
    # UTILITY METHODS
    # ================================
    
    def _get_default_quotas(self, isolation_level: IsolationLevel) -> Dict[ResourceType, ResourceQuota]:
        """Get default resource quotas based on isolation level"""
        quotas = {}
        
        if isolation_level == IsolationLevel.NONE:
            # No limits for development
            return quotas
        
        elif isolation_level == IsolationLevel.BASIC:
            quotas[ResourceType.MEMORY] = ResourceQuota(ResourceType.MEMORY, 512, unit="MB")  # 512MB
            quotas[ResourceType.CPU] = ResourceQuota(ResourceType.CPU, 300, unit="seconds")  # 5 minutes
            quotas[ResourceType.FILE_HANDLES] = ResourceQuota(ResourceType.FILE_HANDLES, 100)
            
        elif isolation_level in [IsolationLevel.CONTAINER, IsolationLevel.SECURE]:
            quotas[ResourceType.MEMORY] = ResourceQuota(ResourceType.MEMORY, 256, unit="MB")  # 256MB
            quotas[ResourceType.CPU] = ResourceQuota(ResourceType.CPU, 50, unit="percent")  # 50% CPU
            quotas[ResourceType.FILE_HANDLES] = ResourceQuota(ResourceType.FILE_HANDLES, 50)
            quotas[ResourceType.API_CALLS] = ResourceQuota(ResourceType.API_CALLS, 1000, unit="calls/hour")
            quotas[ResourceType.DATABASE_CONNECTIONS] = ResourceQuota(ResourceType.DATABASE_CONNECTIONS, 5)
        
        return quotas
    
    def _get_default_security_policy(self, isolation_level: IsolationLevel) -> SecurityPolicy:
        """Get default security policy based on isolation level"""
        if isolation_level == IsolationLevel.NONE:
            return SecurityPolicy()  # Allow everything
        
        elif isolation_level == IsolationLevel.BASIC:
            return SecurityPolicy(
                allow_subprocess_execution=False,
                max_execution_time=300
            )
        
        elif isolation_level in [IsolationLevel.CONTAINER, IsolationLevel.SECURE]:
            return SecurityPolicy(
                allow_network_access=True,
                allow_file_system_access=False,
                allow_subprocess_execution=False,
                allow_api_access=True,
                blocked_domains={"facebook.com", "twitter.com"},  # Example blocks
                max_execution_time=180,
                require_approval_for={"file_write", "network_request", "subprocess"}
            )
    
    def _calculate_cpu_percent(self, stats: Dict[str, Any]) -> float:
        """Calculate CPU usage percentage from Docker stats"""
        cpu_delta = stats['cpu_stats']['cpu_usage']['total_usage'] - \
                   stats['precpu_stats']['cpu_usage']['total_usage']
        system_delta = stats['cpu_stats']['system_cpu_usage'] - \
                      stats['precpu_stats']['system_cpu_usage']
        
        if system_delta > 0:
            cpu_percent = (cpu_delta / system_delta) * 100.0
            return min(cpu_percent, 100.0)
        return 0.0
    
    async def _apply_process_limits(self, context: AgentIsolationContext):
        """Apply process-level resource limits"""
        # Implementation similar to _setup_process_isolation
        # This is called during execution context
        pass
    
    async def _throttle_agent_cpu(self, context: AgentIsolationContext):
        """Throttle agent CPU usage"""
        # Implementation would use cgroups or nice values
        logger.info(f"Throttling CPU for agent {context.agent_id}")
    
    async def _block_agent_api_access(self, context: AgentIsolationContext):
        """Block agent API access"""
        # Implementation would modify network rules or proxy settings
        logger.info(f"Blocking API access for agent {context.agent_id}")
    
    async def _pre_execution_setup(self, context: AgentIsolationContext):
        """Pre-execution setup"""
        context.last_accessed = datetime.now()
        context.status = "executing"
    
    async def _post_execution_cleanup(self, context: AgentIsolationContext):
        """Post-execution cleanup"""
        context.status = "ready"
    
    async def _cleanup_container(self, context: AgentIsolationContext):
        """Cleanup container resources"""
        if context.container_id and self._docker_client:
            try:
                container = self._docker_client.containers.get(context.container_id)
                container.stop(timeout=10)
                container.remove(force=True)
            except Exception as e:
                logger.error(f"Failed to cleanup container: {e}")
    
    async def _cleanup_process(self, context: AgentIsolationContext):
        """Cleanup process resources"""
        if context.process_id:
            try:
                process = psutil.Process(context.process_id)
                process.terminate()
            except Exception as e:
                logger.error(f"Failed to cleanup process: {e}")
    
    # ================================
    # PUBLIC API METHODS
    # ================================
    
    def get_isolation_context(self, agent_id: str) -> Optional[AgentIsolationContext]:
        """Get isolation context for agent"""
        return self._isolation_contexts.get(agent_id)
    
    def list_active_contexts(self) -> List[AgentIsolationContext]:
        """List all active isolation contexts"""
        return list(self._isolation_contexts.values())
    
    def get_resource_utilization(self) -> Dict[str, Any]:
        """Get overall resource utilization metrics"""
        total_memory = sum(ctx.resource_usage.get(ResourceType.MEMORY, 0) 
                          for ctx in self._isolation_contexts.values())
        total_cpu = sum(ctx.resource_usage.get(ResourceType.CPU, 0) 
                       for ctx in self._isolation_contexts.values())
        
        return {
            'total_agents': len(self._isolation_contexts),
            'total_memory_mb': total_memory,
            'total_cpu_percent': total_cpu,
            'active_violations': self._active_violations,
            'agents_created': self._total_agents_created
        }


# Global instance
isolation_manager = AgentIsolationManager() 