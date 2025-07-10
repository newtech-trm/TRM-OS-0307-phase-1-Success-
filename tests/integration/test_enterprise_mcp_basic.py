"""
Basic Enterprise MCP Integration Tests

Basic tests for core enterprise components that work on Windows
without requiring external services like Docker or Redis.
"""

import pytest
import asyncio
import sys
import time
from datetime import datetime
from unittest.mock import Mock, AsyncMock, patch

# Add project root to path
sys.path.insert(0, '.')

from trm_api.protocols.mcp_connectors import (
    BaseMCPConnector,
    MCPConnectorRegistry,
    MCPConnectionConfig,
    MCPRequest,
    MCPResponse,
    MCPHealthCheck,
    MCPConnectionStatus,
    MCPOperationType
)

from trm_api.enterprise import (
    AgentIsolationManager,
    IsolationLevel,
    ResourceQuota,
    ResourceType,
    SecurityPolicy,
    ProductionLogger,
    ProductionCache,
    LogLevel,
    OutputNormalizer,
    ResponseStatus,
    normalize_response,
    normalize_error
)


@pytest.fixture
def mcp_config():
    """Create test MCP configuration"""
    return MCPConnectionConfig(
        platform="test",
        connection_string="test://localhost:5432",
        credentials={
            'username': 'test_user',
            'password': 'test_pass',
            'database': 'test_db'
        },
        timeout=30,
        max_retries=3,
        ssl_enabled=False
    )


@pytest.fixture
def registry():
    """Create MCP connector registry for testing"""
    return MCPConnectorRegistry()


@pytest.fixture 
def isolation_manager():
    """Create agent isolation manager for testing"""
    return AgentIsolationManager()


@pytest.fixture
def production_logger():
    """Create production logger for testing"""
    return ProductionLogger(service_name="test-service")


@pytest.fixture
def production_cache():
    """Create production cache for testing (local only)"""
    # Use local cache only for Windows testing
    cache = ProductionCache(redis_url="redis://fake-redis:6379")
    return cache


@pytest.fixture
def output_normalizer():
    """Create output normalizer for testing"""
    return OutputNormalizer()


class TestMCPConnectorRegistry:
    """Test MCP Connector Registry functionality"""
    
    @pytest.mark.asyncio
    async def test_registry_initialization(self, registry):
        """Test registry initialization"""
        assert len(registry._connectors) == 0
        assert not registry._is_monitoring
        
    @pytest.mark.asyncio
    async def test_register_connector(self, registry, mcp_config):
        """Test connector registration"""
        # Create mock connector class (not instance)
        class MockConnectorClass:
            def __init__(self, config):
                self.config = config
                
            def get_platform(self):
                return "test"
                
            async def connect(self):
                return True
                
            async def disconnect(self):
                return True
        
        # Register connector with correct signature
        result = await registry.register_connector(
            platform="test",
            connector_class=MockConnectorClass,
            config=mcp_config,
            priority=1,
            auto_connect=False  # Don't auto-connect for test
        )
        assert result is True
        assert "test" in registry._connectors
        
    @pytest.mark.asyncio
    async def test_get_connector_registration(self, registry, mcp_config):
        """Test getting connector registration info"""
        # Create and register mock connector
        class MockConnectorClass:
            def __init__(self, config):
                self.config = config
                
            def get_platform(self):
                return "test"
                
            async def connect(self):
                return True
                
            async def disconnect(self):
                return True
        
        await registry.register_connector(
            platform="test_conn",
            connector_class=MockConnectorClass,
            config=mcp_config,
            auto_connect=False
        )
        
        # Test getting connector info
        connectors = registry.list_connectors()
        assert "test_conn" in connectors
        
        # Test non-existent connector
        assert "nonexistent" not in connectors
        
    @pytest.mark.asyncio
    async def test_registry_status(self, registry):
        """Test registry status reporting"""
        status = registry.get_registry_status()
        
        assert 'status' in status
        assert 'registered_connectors' in status
        assert 'active_connectors' in status
        assert 'metrics' in status
        assert isinstance(status['metrics'], dict)


class TestAgentIsolation:
    """Test Agent Isolation functionality (Windows compatible)"""
    
    @pytest.mark.asyncio
    async def test_create_isolation_context(self, isolation_manager):
        """Test creating isolation context"""
        agent_id = "test_agent_123"
        
        context = await isolation_manager.create_isolation_context(
            agent_id=agent_id,
            isolation_level=IsolationLevel.BASIC  # Use BASIC instead of CONTAINER for Windows
        )
        
        assert context.agent_id == agent_id
        assert context.isolation_level == IsolationLevel.BASIC
        assert context.status == "ready"
        assert len(context.resource_quotas) > 0
        
    @pytest.mark.asyncio
    async def test_resource_quota_validation(self):
        """Test resource quota creation and validation"""
        quota = ResourceQuota(
            resource_type=ResourceType.MEMORY,
            max_value=512,  # 512MB
            unit="MB"
        )
        
        # Test quota not exceeded
        quota.current_usage = 256
        assert not quota.is_exceeded()
        assert quota.utilization_percent() == 50.0
        
        # Test quota exceeded
        quota.current_usage = 600
        assert quota.is_exceeded()
        assert quota.utilization_percent() > 100
        
    @pytest.mark.asyncio
    async def test_security_policy_creation(self):
        """Test security policy configuration"""
        policy = SecurityPolicy(
            allow_network_access=True,
            allow_file_system_access=False,
            allow_subprocess_execution=False,
            max_execution_time=300,
            allowed_domains={"api.openai.com", "api.anthropic.com"},
            blocked_domains={"facebook.com", "twitter.com"}
        )
        
        assert policy.allow_network_access is True
        assert policy.allow_file_system_access is False
        assert "api.openai.com" in policy.allowed_domains
        assert "facebook.com" in policy.blocked_domains


class TestProductionLogging:
    """Test Production Logging functionality"""
    
    @pytest.mark.asyncio
    async def test_logger_initialization(self, production_logger):
        """Test logger initialization"""
        assert production_logger.service_name == "test-service"
        assert production_logger.log_level == LogLevel.INFO
        assert production_logger._error_count == 0
        
    @pytest.mark.asyncio
    async def test_structured_logging(self, production_logger):
        """Test structured logging with context"""
        test_context = {
            'user_id': 'user_123',
            'operation': 'test_operation',
            'custom_field': 'custom_value'
        }
        
        # Test different log levels
        production_logger.debug("Debug message", **test_context)
        production_logger.info("Info message", **test_context)
        production_logger.warning("Warning message", **test_context)
        production_logger.error("Error message", **test_context)
        
        # Check log counts
        stats = production_logger.get_metrics_summary()
        assert stats['log_counts'][LogLevel.DEBUG.value] >= 1
        assert stats['log_counts'][LogLevel.INFO.value] >= 1
        assert stats['log_counts'][LogLevel.WARNING.value] >= 1
        assert stats['log_counts'][LogLevel.ERROR.value] >= 1
        
    @pytest.mark.asyncio
    async def test_trace_context(self, production_logger):
        """Test distributed tracing context"""
        async with production_logger.trace_context(
            operation="test_operation",
            user_id="user_123",
            custom_data="test"
        ) as (trace_id, logger):
            
            assert trace_id is not None
            assert len(trace_id) > 0
            
            # Log within trace context
            logger.info("Operation in progress", step="validation")
            logger.info("Operation completed", result="success")
            
        # Trace should be cleaned up
        assert trace_id not in production_logger._active_traces


class TestProductionCache:
    """Test Production Cache functionality (local cache only for Windows)"""
    
    @pytest.mark.asyncio
    async def test_cache_basic_operations(self, production_cache):
        """Test basic cache set/get operations using local cache"""
        # Set value
        result = await production_cache.set("test_key", "test_value", ttl=60)
        # Will be True for local cache even without Redis
        
        # Get value
        value = await production_cache.get("test_key")
        assert value == "test_value"
        
        # Get non-existent key
        value = await production_cache.get("nonexistent_key", default="default")
        assert value == "default"
        
    @pytest.mark.asyncio
    async def test_cache_stats(self, production_cache):
        """Test cache performance statistics"""
        # Perform some cache operations
        await production_cache.set("stat_key1", "value1")
        await production_cache.get("stat_key1")  # Hit
        await production_cache.get("nonexistent")  # Miss
        
        stats = production_cache.get_cache_stats()
        assert 'hit_count' in stats
        assert 'miss_count' in stats
        assert 'hit_rate_percent' in stats
        assert stats['hit_count'] >= 1
        assert stats['miss_count'] >= 1
        
    @pytest.mark.asyncio
    async def test_cache_serialization(self, production_cache):
        """Test cache value serialization/deserialization"""
        # Test different data types
        test_data = {
            'string': 'test_string',
            'number': 123,
            'float': 45.67,
            'boolean': True,
            'list': [1, 2, 3],
            'dict': {'nested': 'value'}
        }
        
        await production_cache.set("complex_data", test_data)
        retrieved = await production_cache.get("complex_data")
        
        assert retrieved == test_data
        assert isinstance(retrieved, dict)
        assert retrieved['string'] == 'test_string'
        assert retrieved['number'] == 123


class TestOutputNormalization:
    """Test Output Normalization functionality"""
    
    @pytest.mark.asyncio
    async def test_normalizer_initialization(self, output_normalizer):
        """Test normalizer initialization"""
        assert len(output_normalizer._schemas) > 0  # Built-in schemas
        assert 'standard_response' in output_normalizer._schemas
        
    @pytest.mark.asyncio
    async def test_standard_response_creation(self, output_normalizer):
        """Test creating standard response"""
        response = output_normalizer.create_standard_response(
            data={'result': 'test'},
            status=ResponseStatus.SUCCESS,
            message="Operation completed successfully",
            request_id="test_123"
        )
        
        assert response.status == ResponseStatus.SUCCESS
        assert response.data == {'result': 'test'}
        assert response.message == "Operation completed successfully"
        assert response.metadata.request_id == "test_123"
        assert isinstance(response.metadata.timestamp, datetime)
        
    @pytest.mark.asyncio
    async def test_error_response_creation(self, output_normalizer):
        """Test creating error response"""
        errors = [
            "First error message",
            {"code": "VALIDATION_ERROR", "message": "Field is required", "field": "name"}
        ]
        
        response = output_normalizer.create_error_response(
            errors=errors,
            message="Validation failed",
            status=ResponseStatus.VALIDATION_ERROR
        )
        
        assert response.status == ResponseStatus.VALIDATION_ERROR
        assert response.message == "Validation failed"
        assert len(response.errors) == 2
        assert response.errors[0]['code'] == 'GENERAL_ERROR'
        assert response.errors[1]['code'] == 'VALIDATION_ERROR'
        
    @pytest.mark.asyncio
    async def test_data_normalization(self, output_normalizer):
        """Test data normalization and validation"""
        test_data = {
            'name': '  Test Name  ',  # Extra whitespace
            'value': 123,
            'nested': {
                'field': 'value'
            }
        }
        
        result = output_normalizer.normalize(test_data)
        
        assert result.is_valid is True
        assert result.normalized_data['name'] == 'Test Name'  # Whitespace trimmed
        assert result.normalized_data['value'] == 123
        assert 'nested' in result.normalized_data


class TestIntegrationWorkflows:
    """Test basic integration workflows"""
    
    @pytest.mark.asyncio
    async def test_logging_and_normalization_workflow(self, production_logger, output_normalizer):
        """Test workflow combining logging and output normalization"""
        
        # Simulate operation with logging
        async with production_logger.trace_context(
            operation="data_processing",
            user_id="user_123"
        ) as (trace_id, logger):
            
            logger.info("Starting data processing")
            
            # Simulate some processing
            await asyncio.sleep(0.01)
            
            # Create result data
            result_data = {
                'processed_records': 100,
                'success_count': 95,
                'error_count': 5
            }
            
            logger.info("Data processing completed", **result_data)
            
            # Normalize the response
            response = output_normalizer.create_standard_response(
                data=result_data,
                status=ResponseStatus.SUCCESS,
                message="Data processing completed successfully",
                request_id=trace_id,
                processing_time_ms=10.0
            )
            
            assert response.status == ResponseStatus.SUCCESS
            assert response.data == result_data
            assert response.metadata.request_id == trace_id
            
    @pytest.mark.asyncio
    async def test_error_handling_workflow(self, production_logger, output_normalizer):
        """Test error handling workflow across components"""
        
        try:
            async with production_logger.trace_context(
                operation="error_test",
                user_id="user_123"
            ) as (trace_id, logger):
                
                logger.info("Starting operation that will fail")
                
                # Simulate an error
                raise ValueError("Test error for workflow")
                
        except Exception as e:
            # Create normalized error response
            error_response = output_normalizer.create_error_response(
                errors=[{
                    'code': 'OPERATION_ERROR',
                    'message': str(e),
                    'context': {'operation': 'error_test'}
                }],
                message="Operation failed",
                status=ResponseStatus.ERROR
            )
            
            assert error_response.status == ResponseStatus.ERROR
            assert len(error_response.errors) == 1
            assert error_response.errors[0]['code'] == 'OPERATION_ERROR'


if __name__ == "__main__":
    # Run basic tests
    import subprocess
    result = subprocess.run([
        "python", "-m", "pytest", 
        __file__, 
        "-v", 
        "--tb=short"
    ], capture_output=True, text=True)
    
    print("STDOUT:")
    print(result.stdout)
    print("STDERR:")
    print(result.stderr)
    print(f"Return code: {result.returncode}") 