"""
Base MCP (Model Context Protocol) Connector

Enterprise-grade foundation for all platform-specific MCP implementations.
Provides standardized interface, error handling, monitoring, and security.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Union, AsyncIterator
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import logging
import uuid
import asyncio
import json
from contextlib import asynccontextmanager
import hashlib

logger = logging.getLogger(__name__)


class MCPConnectionStatus(str, Enum):
    """MCP connection status enum"""
    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    ERROR = "error"
    AUTHENTICATING = "authenticating"
    AUTHENTICATED = "authenticated"


class MCPOperationType(str, Enum):
    """MCP operation types"""
    QUERY = "query"
    EXECUTE = "execute"
    STREAM = "stream"
    BATCH = "batch"
    TRANSACTION = "transaction"


@dataclass
class MCPConnectionConfig:
    """MCP connection configuration"""
    platform: str
    connection_string: str
    credentials: Dict[str, Any] = field(default_factory=dict)
    timeout: int = 30
    max_retries: int = 3
    ssl_enabled: bool = True
    connection_pool_size: int = 10
    enable_monitoring: bool = True
    enable_caching: bool = True
    cache_ttl: int = 300  # 5 minutes


@dataclass
class MCPRequest:
    """MCP request structure"""
    request_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    operation_type: MCPOperationType = MCPOperationType.QUERY
    resource: str = ""
    method: str = ""
    parameters: Dict[str, Any] = field(default_factory=dict)
    headers: Dict[str, str] = field(default_factory=dict)
    timeout: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class MCPResponse:
    """MCP response structure"""
    request_id: str
    success: bool
    data: Any = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    execution_time_ms: float = 0.0
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class MCPHealthCheck:
    """MCP health check result"""
    platform: str
    status: MCPConnectionStatus
    response_time_ms: float
    last_check: datetime = field(default_factory=datetime.now)
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class BaseMCPConnector(ABC):
    """
    Base MCP Connector for enterprise platform integration
    
    Provides standardized interface for all MCP connectors with:
    - Connection management and pooling
    - Authentication and security
    - Error handling and retry logic
    - Monitoring and health checks
    - Caching and performance optimization
    """
    
    def __init__(self, config: MCPConnectionConfig):
        self.config = config
        self.connection_status = MCPConnectionStatus.DISCONNECTED
        self.connection_pool = []
        self.metrics = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'avg_response_time': 0.0,
            'last_health_check': None
        }
        self._cache = {} if config.enable_caching else None
        self._session_id = str(uuid.uuid4())
        
    # ================================
    # ABSTRACT METHODS - Platform Specific
    # ================================
    
    @abstractmethod
    async def _platform_connect(self) -> bool:
        """Platform-specific connection implementation"""
        pass
        
    @abstractmethod
    async def _platform_disconnect(self) -> bool:
        """Platform-specific disconnection implementation"""
        pass
        
    @abstractmethod
    async def _platform_authenticate(self) -> bool:
        """Platform-specific authentication implementation"""
        pass
        
    @abstractmethod
    async def _platform_execute_request(self, request: MCPRequest) -> MCPResponse:
        """Platform-specific request execution"""
        pass
        
    @abstractmethod
    async def _platform_health_check(self) -> MCPHealthCheck:
        """Platform-specific health check"""
        pass
    
    # ================================
    # PUBLIC INTERFACE
    # ================================
    
    async def connect(self) -> bool:
        """
        Establish connection to platform
        
        Returns:
            bool: True if connection successful
        """
        try:
            logger.info(f"Connecting to {self.config.platform}...")
            self.connection_status = MCPConnectionStatus.CONNECTING
            
            # Platform-specific connection
            connected = await self._platform_connect()
            if not connected:
                self.connection_status = MCPConnectionStatus.ERROR
                return False
                
            self.connection_status = MCPConnectionStatus.CONNECTED
            
            # Authenticate if credentials provided
            if self.config.credentials:
                self.connection_status = MCPConnectionStatus.AUTHENTICATING
                authenticated = await self._platform_authenticate()
                if not authenticated:
                    self.connection_status = MCPConnectionStatus.ERROR
                    return False
                self.connection_status = MCPConnectionStatus.AUTHENTICATED
            
            logger.info(f"Successfully connected to {self.config.platform}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect to {self.config.platform}: {str(e)}")
            self.connection_status = MCPConnectionStatus.ERROR
            return False
    
    async def disconnect(self) -> bool:
        """
        Disconnect from platform
        
        Returns:
            bool: True if disconnection successful
        """
        try:
            logger.info(f"Disconnecting from {self.config.platform}...")
            
            disconnected = await self._platform_disconnect()
            self.connection_status = MCPConnectionStatus.DISCONNECTED
            
            logger.info(f"Successfully disconnected from {self.config.platform}")
            return disconnected
            
        except Exception as e:
            logger.error(f"Failed to disconnect from {self.config.platform}: {str(e)}")
            return False
    
    async def execute_request(self, request: MCPRequest) -> MCPResponse:
        """
        Execute MCP request with retry logic and monitoring
        
        Args:
            request: MCP request to execute
            
        Returns:
            MCPResponse: Response with data or error
        """
        start_time = datetime.now()
        self.metrics['total_requests'] += 1
        
        # Check cache first
        if self._cache and request.operation_type == MCPOperationType.QUERY:
            cache_key = self._get_cache_key(request)
            if cache_key in self._cache:
                cached_response = self._cache[cache_key]
                if self._is_cache_valid(cached_response):
                    logger.debug(f"Cache hit for request {request.request_id}")
                    return cached_response
        
        # Execute with retry logic
        last_error = None
        for attempt in range(self.config.max_retries + 1):
            try:
                if self.connection_status not in [MCPConnectionStatus.CONNECTED, MCPConnectionStatus.AUTHENTICATED]:
                    await self.connect()
                
                response = await self._platform_execute_request(request)
                
                # Calculate execution time
                execution_time = (datetime.now() - start_time).total_seconds() * 1000
                response.execution_time_ms = execution_time
                
                # Update metrics
                if response.success:
                    self.metrics['successful_requests'] += 1
                    
                    # Cache successful query responses
                    if (self._cache and 
                        request.operation_type == MCPOperationType.QUERY and
                        response.success):
                        cache_key = self._get_cache_key(request)
                        self._cache[cache_key] = response
                else:
                    self.metrics['failed_requests'] += 1
                
                # Update average response time
                total_requests = self.metrics['total_requests']
                current_avg = self.metrics['avg_response_time']
                self.metrics['avg_response_time'] = (
                    (current_avg * (total_requests - 1) + execution_time) / total_requests
                )
                
                return response
                
            except Exception as e:
                last_error = e
                logger.warning(
                    f"Attempt {attempt + 1} failed for request {request.request_id}: {str(e)}"
                )
                
                if attempt < self.config.max_retries:
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
        
        # All retries failed
        self.metrics['failed_requests'] += 1
        execution_time = (datetime.now() - start_time).total_seconds() * 1000
        
        return MCPResponse(
            request_id=request.request_id,
            success=False,
            error=f"Request failed after {self.config.max_retries + 1} attempts: {str(last_error)}",
            execution_time_ms=execution_time
        )
    
    async def health_check(self) -> MCPHealthCheck:
        """
        Perform health check on platform connection
        
        Returns:
            MCPHealthCheck: Health status result
        """
        try:
            health_result = await self._platform_health_check()
            self.metrics['last_health_check'] = health_result.last_check
            return health_result
            
        except Exception as e:
            logger.error(f"Health check failed for {self.config.platform}: {str(e)}")
            return MCPHealthCheck(
                platform=self.config.platform,
                status=MCPConnectionStatus.ERROR,
                response_time_ms=0.0,
                error_message=str(e)
            )
    
    async def batch_execute(self, requests: List[MCPRequest]) -> List[MCPResponse]:
        """
        Execute multiple requests in batch
        
        Args:
            requests: List of MCP requests
            
        Returns:
            List[MCPResponse]: List of responses in same order
        """
        tasks = []
        for request in requests:
            task = asyncio.create_task(self.execute_request(request))
            tasks.append(task)
        
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Convert exceptions to error responses
        result = []
        for i, response in enumerate(responses):
            if isinstance(response, Exception):
                result.append(MCPResponse(
                    request_id=requests[i].request_id,
                    success=False,
                    error=str(response)
                ))
            else:
                result.append(response)
        
        return result
    
    @asynccontextmanager
    async def transaction(self):
        """
        Context manager for transactional operations
        
        Usage:
            async with connector.transaction():
                await connector.execute_request(request1)
                await connector.execute_request(request2)
        """
        try:
            logger.debug(f"Starting transaction on {self.config.platform}")
            yield self
            logger.debug(f"Committing transaction on {self.config.platform}")
        except Exception as e:
            logger.error(f"Rolling back transaction on {self.config.platform}: {str(e)}")
            raise
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get connector performance metrics"""
        return {
            **self.metrics,
            'platform': self.config.platform,
            'connection_status': self.connection_status.value,
            'session_id': self._session_id,
            'cache_size': len(self._cache) if self._cache else 0
        }
    
    # ================================
    # PRIVATE HELPER METHODS
    # ================================
    
    def _get_cache_key(self, request: MCPRequest) -> str:
        """Generate cache key for request"""
        key_parts = [
            request.resource,
            request.method,
            json.dumps(request.parameters, sort_keys=True)
        ]
        return hashlib.md5('|'.join(key_parts).encode()).hexdigest()
    
    def _is_cache_valid(self, response: MCPResponse) -> bool:
        """Check if cached response is still valid"""
        if not response:
            return False
        
        cache_age = (datetime.now() - response.created_at).total_seconds()
        return cache_age < self.config.cache_ttl
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}({self.config.platform}, {self.connection_status})>" 