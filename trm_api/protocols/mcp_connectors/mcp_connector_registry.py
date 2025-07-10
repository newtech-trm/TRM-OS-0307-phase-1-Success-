"""
MCP Connector Registry

Enterprise-grade registry for managing multiple MCP connectors:
- Dynamic connector registration and discovery
- Health monitoring across all connectors
- Load balancing and failover
- Centralized configuration management
- Performance monitoring and analytics
"""

from typing import Dict, Any, List, Optional, Type, Callable
from dataclasses import dataclass, field
from datetime import datetime
import logging
import asyncio
import json
from enum import Enum
from collections import defaultdict

from .base_mcp_connector import (
    BaseMCPConnector, 
    MCPConnectionConfig, 
    MCPRequest, 
    MCPResponse,
    MCPHealthCheck,
    MCPConnectionStatus
)

logger = logging.getLogger(__name__)


class RegistryStatus(str, Enum):
    """Registry status states"""
    INITIALIZING = "initializing"
    ACTIVE = "active"
    DEGRADED = "degraded"
    OFFLINE = "offline"


@dataclass
class ConnectorRegistration:
    """Connector registration information"""
    platform: str
    connector_class: Type[BaseMCPConnector]
    config: MCPConnectionConfig
    instance: Optional[BaseMCPConnector] = None
    priority: int = 1  # Higher number = higher priority
    enabled: bool = True
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    last_health_check: Optional[datetime] = None
    health_status: MCPConnectionStatus = MCPConnectionStatus.DISCONNECTED


@dataclass
class RegistryMetrics:
    """Registry performance metrics"""
    total_connectors: int = 0
    active_connectors: int = 0
    failed_connectors: int = 0
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    avg_response_time: float = 0.0
    uptime_seconds: float = 0.0
    last_updated: datetime = field(default_factory=datetime.now)


class MCPConnectorRegistry:
    """
    Enterprise MCP Connector Registry
    
    Manages multiple MCP connectors with:
    - Dynamic registration and discovery
    - Health monitoring and failover
    - Load balancing and routing
    - Performance analytics
    - Configuration management
    """
    
    def __init__(self):
        """Initialize the MCP connector registry"""
        # Connector storage
        self._connectors: Dict[str, ConnectorRegistration] = {}
        self._connector_instances: Dict[str, BaseMCPConnector] = {}
        
        # Registry state
        self._status: RegistryStatus = RegistryStatus.INITIALIZING
        self._metrics: RegistryMetrics = RegistryMetrics()
        self._is_monitoring = False
        self._monitoring_task: Optional[asyncio.Task] = None
        self._health_check_interval = 30  # seconds
        self._route_cache: Dict[str, str] = {}
        self._start_time = datetime.now()
        
        # Initialize status to ACTIVE
        self._status = RegistryStatus.ACTIVE
        
        # Initialize built-in connectors
        self._register_builtin_connectors()
        
        logger.info("MCP Connector Registry initialized")
    
    # ================================
    # CONNECTOR REGISTRATION
    # ================================
    
    async def register_connector(
        self,
        platform: str,
        connector_class: Type[BaseMCPConnector],
        config: MCPConnectionConfig,
        priority: int = 1,
        tags: List[str] = None,
        auto_connect: bool = True
    ) -> bool:
        """
        Register a new MCP connector
        
        Args:
            platform: Platform identifier (e.g., 'snowflake', 'rabbitmq')
            connector_class: Connector class to instantiate
            config: Connection configuration
            priority: Priority for load balancing (higher = preferred)
            tags: Optional tags for categorization
            auto_connect: Whether to automatically connect after registration
            
        Returns:
            bool: True if registration successful
        """
        try:
            if platform in self._connectors:
                logger.warning(f"Connector for {platform} already registered, updating...")
            
            registration = ConnectorRegistration(
                platform=platform,
                connector_class=connector_class,
                config=config,
                priority=priority,
                tags=tags or [],
            )
            
            self._connectors[platform] = registration
            
            if auto_connect:
                await self._initialize_connector(platform)
            
            self._update_metrics()
            logger.info(f"Successfully registered MCP connector for {platform}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to register connector for {platform}: {str(e)}")
            return False
    
    async def unregister_connector(self, platform: str) -> bool:
        """
        Unregister and disconnect a connector
        
        Args:
            platform: Platform identifier
            
        Returns:
            bool: True if unregistration successful
        """
        try:
            if platform not in self._connectors:
                logger.warning(f"Connector for {platform} not found")
                return False
            
            # Disconnect if connected
            if platform in self._connector_instances:
                await self._connector_instances[platform].disconnect()
                del self._connector_instances[platform]
            
            del self._connectors[platform]
            
            # Clear route cache entries
            self._route_cache = {
                resource: conn for resource, conn in self._route_cache.items()
                if conn != platform
            }
            
            self._update_metrics()
            logger.info(f"Successfully unregistered MCP connector for {platform}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to unregister connector for {platform}: {str(e)}")
            return False
    
    # ================================
    # CONNECTOR OPERATIONS
    # ================================
    
    async def execute_request(
        self, 
        request: MCPRequest,
        preferred_platform: Optional[str] = None
    ) -> MCPResponse:
        """
        Execute request using best available connector
        
        Args:
            request: MCP request to execute
            preferred_platform: Preferred platform (optional)
            
        Returns:
            MCPResponse: Response from selected connector
        """
        try:
            # Route request to appropriate connector
            selected_platform = await self._route_request(request, preferred_platform)
            
            if not selected_platform:
                return MCPResponse(
                    request_id=request.request_id,
                    success=False,
                    error="No suitable connector available for request"
                )
            
            connector = self._connector_instances[selected_platform]
            
            # Execute request
            response = await connector.execute_request(request)
            
            # Update metrics
            self._metrics.total_requests += 1
            if response.success:
                self._metrics.successful_requests += 1
            else:
                self._metrics.failed_requests += 1
            
            # Update average response time
            total_requests = self._metrics.total_requests
            current_avg = self._metrics.avg_response_time
            self._metrics.avg_response_time = (
                (current_avg * (total_requests - 1) + response.execution_time_ms) / total_requests
            )
            
            # Cache successful routes
            if response.success and request.resource:
                self._route_cache[request.resource] = selected_platform
            
            return response
            
        except Exception as e:
            logger.error(f"Failed to execute request {request.request_id}: {str(e)}")
            self._metrics.total_requests += 1
            self._metrics.failed_requests += 1
            
            return MCPResponse(
                request_id=request.request_id,
                success=False,
                error=f"Registry execution error: {str(e)}"
            )
    
    async def batch_execute(
        self, 
        requests: List[MCPRequest],
        load_balance: bool = True
    ) -> List[MCPResponse]:
        """
        Execute multiple requests with optional load balancing
        
        Args:
            requests: List of MCP requests
            load_balance: Whether to distribute across connectors
            
        Returns:
            List[MCPResponse]: Responses in same order as requests
        """
        if not load_balance:
            # Execute all on single best connector
            return await asyncio.gather(*[
                self.execute_request(request) for request in requests
            ])
        
        # Group requests by optimal connector
        connector_groups = defaultdict(list)
        request_indices = {}
        
        for i, request in enumerate(requests):
            selected_platform = await self._route_request(request)
            if selected_platform:
                connector_groups[selected_platform].append(request)
                request_indices[request.request_id] = i
        
        # Execute batches per connector
        all_tasks = []
        for platform, platform_requests in connector_groups.items():
            connector = self._connector_instances[platform]
            task = asyncio.create_task(connector.batch_execute(platform_requests))
            all_tasks.append((platform, task))
        
        # Collect results
        responses = [None] * len(requests)
        
        for platform, task in all_tasks:
            try:
                platform_responses = await task
                for response in platform_responses:
                    idx = request_indices.get(response.request_id)
                    if idx is not None:
                        responses[idx] = response
            except Exception as e:
                logger.error(f"Batch execution failed for {platform}: {str(e)}")
        
        # Fill any missing responses with errors
        for i, response in enumerate(responses):
            if response is None:
                responses[i] = MCPResponse(
                    request_id=requests[i].request_id,
                    success=False,
                    error="Failed to route request to any connector"
                )
        
        return responses
    
    async def health_check_all(self) -> Dict[str, MCPHealthCheck]:
        """
        Perform health check on all registered connectors
        
        Returns:
            Dict[str, MCPHealthCheck]: Health status per platform
        """
        health_results = {}
        
        tasks = []
        for platform in self._connector_instances:
            task = asyncio.create_task(self._health_check_connector(platform))
            tasks.append((platform, task))
        
        for platform, task in tasks:
            try:
                health_result = await task
                health_results[platform] = health_result
                
                # Update registration health status
                if platform in self._connectors:
                    self._connectors[platform].health_status = health_result.status
                    self._connectors[platform].last_health_check = health_result.last_check
                    
            except Exception as e:
                logger.error(f"Health check failed for {platform}: {str(e)}")
                health_results[platform] = MCPHealthCheck(
                    platform=platform,
                    status=MCPConnectionStatus.ERROR,
                    response_time_ms=0.0,
                    error_message=str(e)
                )
        
        self._update_metrics()
        return health_results
    
    # ================================
    # LIFECYCLE MANAGEMENT
    # ================================
    
    async def start(self) -> bool:
        """
        Start the registry and all registered connectors
        
        Returns:
            bool: True if startup successful
        """
        try:
            logger.info("Starting MCP Connector Registry...")
            self._status = RegistryStatus.INITIALIZING
            
            # Initialize all registered connectors
            initialization_tasks = []
            for platform in self._connectors:
                task = asyncio.create_task(self._initialize_connector(platform))
                initialization_tasks.append(task)
            
            results = await asyncio.gather(*initialization_tasks, return_exceptions=True)
            
            # Count successful initializations
            successful = sum(1 for result in results if result is True)
            total = len(self._connectors)
            
            if successful == 0:
                self._status = RegistryStatus.OFFLINE
                logger.error("Failed to initialize any connectors")
                return False
            elif successful < total:
                self._status = RegistryStatus.DEGRADED
                logger.warning(f"Only {successful}/{total} connectors initialized successfully")
            else:
                self._status = RegistryStatus.ACTIVE
                logger.info(f"All {total} connectors initialized successfully")
            
            # Start health check monitoring
            self._health_check_task = asyncio.create_task(self._health_check_loop())
            
            self._update_metrics()
            logger.info("MCP Connector Registry started successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start registry: {str(e)}")
            self._status = RegistryStatus.OFFLINE
            return False
    
    async def stop(self) -> bool:
        """
        Stop the registry and disconnect all connectors
        
        Returns:
            bool: True if shutdown successful
        """
        try:
            logger.info("Stopping MCP Connector Registry...")
            
            # Stop health check monitoring
            if self._health_check_task:
                self._health_check_task.cancel()
                try:
                    await self._health_check_task
                except asyncio.CancelledError:
                    pass
            
            # Disconnect all connectors
            disconnect_tasks = []
            for platform, connector in self._connector_instances.items():
                task = asyncio.create_task(connector.disconnect())
                disconnect_tasks.append(task)
            
            await asyncio.gather(*disconnect_tasks, return_exceptions=True)
            
            self._connector_instances.clear()
            self._status = RegistryStatus.OFFLINE
            
            logger.info("MCP Connector Registry stopped successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to stop registry: {str(e)}")
            return False
    
    # ================================
    # INFORMATION & MONITORING
    # ================================
    
    def get_registry_status(self) -> Dict[str, Any]:
        """Get comprehensive registry status"""
        return {
            'status': self._status.value,
            'uptime_seconds': (datetime.now() - self._start_time).total_seconds(),
            'registered_connectors': len(self._connectors),
            'active_connectors': len(self._connector_instances),
            'metrics': {
                'total_requests': self._metrics.total_requests,
                'successful_requests': self._metrics.successful_requests,
                'failed_requests': self._metrics.failed_requests,
                'success_rate': (
                    self._metrics.successful_requests / max(self._metrics.total_requests, 1)
                ) * 100,
                'avg_response_time_ms': self._metrics.avg_response_time,
            },
            'connectors': {
                platform: {
                    'status': reg.health_status.value,
                    'priority': reg.priority,
                    'enabled': reg.enabled,
                    'tags': reg.tags,
                    'last_health_check': reg.last_health_check.isoformat() if reg.last_health_check else None
                }
                for platform, reg in self._connectors.items()
            }
        }
    
    def list_connectors(self, enabled_only: bool = False) -> List[str]:
        """List registered connector platforms"""
        if enabled_only:
            return [platform for platform, reg in self._connectors.items() if reg.enabled]
        return list(self._connectors.keys())
    
    def get_connector_registration(self, platform: str) -> Optional[ConnectorRegistration]:
        """Get connector registration by platform"""
        return self._connectors.get(platform)
    
    def get_connector_metrics(self, platform: str) -> Optional[Dict[str, Any]]:
        """Get metrics for specific connector"""
        if platform not in self._connector_instances:
            return None
        
        connector = self._connector_instances[platform]
        return connector.get_metrics()
    
    # ================================
    # PRIVATE HELPER METHODS
    # ================================
    
    async def _initialize_connector(self, platform: str) -> bool:
        """Initialize and connect a single connector"""
        try:
            registration = self._connectors[platform]
            
            # Create connector instance
            connector = registration.connector_class(registration.config)
            
            # Attempt connection
            connected = await connector.connect()
            if connected:
                self._connector_instances[platform] = connector
                registration.instance = connector
                registration.health_status = connector.connection_status
                logger.info(f"Successfully initialized connector for {platform}")
                return True
            else:
                logger.error(f"Failed to connect connector for {platform}")
                registration.health_status = MCPConnectionStatus.ERROR
                return False
                
        except Exception as e:
            logger.error(f"Failed to initialize connector for {platform}: {str(e)}")
            if platform in self._connectors:
                self._connectors[platform].health_status = MCPConnectionStatus.ERROR
            return False
    
    async def _route_request(
        self, 
        request: MCPRequest, 
        preferred_platform: Optional[str] = None
    ) -> Optional[str]:
        """Route request to most appropriate connector"""
        
        # Use preferred platform if specified and available
        if preferred_platform and preferred_platform in self._connector_instances:
            registration = self._connectors[preferred_platform]
            if registration.enabled and registration.health_status in [
                MCPConnectionStatus.CONNECTED, MCPConnectionStatus.AUTHENTICATED
            ]:
                return preferred_platform
        
        # Check route cache
        if request.resource in self._route_cache:
            cached_platform = self._route_cache[request.resource]
            if cached_platform in self._connector_instances:
                registration = self._connectors[cached_platform]
                if registration.enabled and registration.health_status in [
                    MCPConnectionStatus.CONNECTED, MCPConnectionStatus.AUTHENTICATED
                ]:
                    return cached_platform
        
        # Find best available connector by priority
        available_connectors = []
        for platform, registration in self._connectors.items():
            if (platform in self._connector_instances and 
                registration.enabled and
                registration.health_status in [
                    MCPConnectionStatus.CONNECTED, MCPConnectionStatus.AUTHENTICATED
                ]):
                available_connectors.append((platform, registration.priority))
        
        if not available_connectors:
            return None
        
        # Sort by priority (descending) and return highest priority
        available_connectors.sort(key=lambda x: x[1], reverse=True)
        return available_connectors[0][0]
    
    async def _health_check_connector(self, platform: str) -> MCPHealthCheck:
        """Perform health check on single connector"""
        if platform not in self._connector_instances:
            return MCPHealthCheck(
                platform=platform,
                status=MCPConnectionStatus.DISCONNECTED,
                response_time_ms=0.0,
                error_message="Connector not initialized"
            )
        
        connector = self._connector_instances[platform]
        return await connector.health_check()
    
    async def _health_check_loop(self):
        """Background health check loop"""
        while True:
            try:
                await asyncio.sleep(self._health_check_interval)
                await self.health_check_all()
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Health check loop error: {str(e)}")
    
    def _update_metrics(self):
        """Update registry metrics"""
        self._metrics.total_connectors = len(self._connectors)
        self._metrics.active_connectors = len(self._connector_instances)
        self._metrics.failed_connectors = sum(
            1 for reg in self._connectors.values()
            if reg.health_status == MCPConnectionStatus.ERROR
        )
        self._metrics.uptime_seconds = (datetime.now() - self._start_time).total_seconds()
        self._metrics.last_updated = datetime.now()

    def _register_builtin_connectors(self):
        """Register built-in MCP connectors"""
        try:
            # Store connector factories for lazy loading
            self._connector_factories = {}
            logger.info("Built-in MCP connector factories initialized")
            
        except Exception as e:
            logger.warning(f"Failed to initialize connector factories: {e}")


# Global registry instance
_registry_instance: Optional[MCPConnectorRegistry] = None


def get_mcp_registry() -> MCPConnectorRegistry:
    """Get or create global MCP connector registry instance"""
    global _registry_instance
    if _registry_instance is None:
        _registry_instance = MCPConnectorRegistry()
    return _registry_instance 