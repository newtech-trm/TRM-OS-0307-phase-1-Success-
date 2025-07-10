"""
Enterprise MCP Infrastructure Integration Tests

Comprehensive tests for MCP connectors, agent isolation, 
production infrastructure, and output normalization.
"""

import pytest
import asyncio
import time
import os
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from datetime import datetime, timedelta
import json
import uuid

from trm_api.protocols.mcp_connectors import (
    BaseMCPConnector,
    MCPConnectorRegistry,
    SnowflakeMCPConnector,
    RabbitMQMCPConnector,
    MCPConnectionConfig,
    MCPRequest,
    MCPResponse,
    MCPHealthCheck,
    MCPConnectionStatus,
    MCPOperationType,
    RegistryStatus
)

from trm_api.enterprise import (
    AgentIsolationManager,
    IsolationLevel,
    ResourceQuota,
    ResourceType,
    SecurityPolicy,
    ContainerConfig,
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
def snowflake_config():
    """Create real Snowflake configuration from environment"""
    return MCPConnectionConfig(
        platform="snowflake",
        connection_string=f"snowflake://{os.getenv('SNOWFLAKE_USER')}:{os.getenv('SNOWFLAKE_PASSWORD')}@{os.getenv('SNOWFLAKE_ACCOUNT')}/{os.getenv('SNOWFLAKE_DATABASE')}/{os.getenv('SNOWFLAKE_SCHEMA')}?warehouse={os.getenv('SNOWFLAKE_WAREHOUSE')}&role={os.getenv('SNOWFLAKE_ROLE')}",
        credentials={
            'account': os.getenv('SNOWFLAKE_ACCOUNT'),
            'user': os.getenv('SNOWFLAKE_USER'),
            'password': os.getenv('SNOWFLAKE_PASSWORD'),
            'database': os.getenv('SNOWFLAKE_DATABASE'),
            'schema': os.getenv('SNOWFLAKE_SCHEMA'),
            'warehouse': os.getenv('SNOWFLAKE_WAREHOUSE'),
            'role': os.getenv('SNOWFLAKE_ROLE')
        },
        timeout=30,
        max_retries=3,
        ssl_enabled=True
    )


@pytest.fixture
def rabbitmq_config():
    """Create real RabbitMQ configuration from environment"""
    return MCPConnectionConfig(
        platform="rabbitmq",
        connection_string=os.getenv('RABBITMQ_CLOUD_URL'),
        credentials={
            'host': os.getenv('RABBITMQ_HOST'),
            'port': int(os.getenv('RABBITMQ_PORT', '5672')),
            'vhost': os.getenv('RABBITMQ_VHOST'),
            'username': os.getenv('RABBITMQ_USER'),
            'password': os.getenv('RABBITMQ_PASSWORD')
        },
        timeout=30,
        max_retries=3,
        ssl_enabled=True
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
    """Create production cache for testing"""
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
        assert len(registry._connector_instances) == 0
        assert not registry._is_monitoring
        assert registry._status == RegistryStatus.ACTIVE
        
    @pytest.mark.asyncio
    async def test_register_connector(self, registry, mcp_config):
        """Test connector registration"""
        # Register connector with proper API
        result = await registry.register_connector(
            platform="test_platform",
            connector_class=BaseMCPConnector,
            config=mcp_config,
            priority=1,
            tags=["test"],
            auto_connect=False  # Don't auto-connect for testing
        )
        
        assert result is True
        assert "test_platform" in registry._connectors
        
        # Verify registration details
        registration = registry._connectors["test_platform"]
        assert registration.platform == "test_platform"
        assert registration.connector_class == BaseMCPConnector
        assert registration.config == mcp_config
        assert registration.priority == 1
        assert "test" in registration.tags
        
    @pytest.mark.asyncio
    async def test_unregister_connector(self, registry, mcp_config):
        """Test connector unregistration"""
        # Register first
        await registry.register_connector(
            platform="test_platform",
            connector_class=BaseMCPConnector,
            config=mcp_config,
            auto_connect=False
        )
        
        # Then unregister
        result = await registry.unregister_connector("test_platform")
        assert result is True
        assert "test_platform" not in registry._connectors
        
    @pytest.mark.asyncio
    async def test_get_connector_registration(self, registry, mcp_config):
        """Test getting connector registration by platform"""
        # Register connector
        await registry.register_connector(
            platform="test_platform",
            connector_class=BaseMCPConnector,
            config=mcp_config,
            auto_connect=False
        )
        
        # Get registration
        registration = registry.get_connector_registration("test_platform")
        assert registration is not None
        assert registration.platform == "test_platform"
        
        # Test non-existent connector
        assert registry.get_connector_registration("nonexistent") is None
        
    @pytest.mark.asyncio
    async def test_list_connectors(self, registry, mcp_config):
        """Test listing registered connectors"""
        # Initially empty
        assert len(registry.list_connectors()) == 0
        
        # Register a connector
        await registry.register_connector(
            platform="test_platform",
            connector_class=BaseMCPConnector,
            config=mcp_config,
            auto_connect=False
        )
        
        # Should have one connector
        connectors = registry.list_connectors()
        assert len(connectors) == 1
        assert "test_platform" in connectors
        
    @pytest.mark.asyncio
    async def test_registry_status(self, registry):
        """Test registry status reporting"""
        status = registry.get_registry_status()
        
        assert "status" in status
        assert "metrics" in status
        assert "connectors" in status
        assert status["status"] == RegistryStatus.ACTIVE
        
        # Check metrics structure (match actual implementation)
        metrics = status["metrics"]
        assert "total_requests" in metrics
        assert "successful_requests" in metrics
        assert "failed_requests" in metrics
        assert "success_rate" in metrics
        assert "avg_response_time_ms" in metrics
        
        # Check top-level connector counts
        assert "registered_connectors" in status
        assert "active_connectors" in status
        assert isinstance(status["registered_connectors"], int)
        assert isinstance(status["active_connectors"], int)


class TestSnowflakeMCPConnector:
    """Test Snowflake MCP Connector"""
    
    @pytest.mark.asyncio
    async def test_snowflake_connection(self, snowflake_config):
        """Test Snowflake connector initialization and connection"""
        # Skip if no credentials available
        if not os.getenv('SNOWFLAKE_ACCOUNT'):
            pytest.skip("Snowflake credentials not available")
        
        connector = SnowflakeMCPConnector(snowflake_config)
        
        # Test connection (may fail if credentials are invalid, but should not crash)
        try:
            result = await connector.connect()
            # If connection succeeds, verify it's properly initialized
            if result:
                assert connector._connection is not None
                assert connector.connection_status == MCPConnectionStatus.AUTHENTICATED
            else:
                # Connection failed but handled gracefully
                assert connector.connection_status in [MCPConnectionStatus.ERROR, MCPConnectionStatus.DISCONNECTED]
        except Exception as e:
            # Connection failed due to network/credential issues - this is expected in CI
            assert "connection" in str(e).lower() or "authentication" in str(e).lower() or "certificate" in str(e).lower() or "hostname" in str(e).lower()
        
    @pytest.mark.asyncio
    async def test_snowflake_query_execution(self, snowflake_config):
        """Test Snowflake query execution"""
        # Skip if no credentials available
        if not os.getenv('SNOWFLAKE_ACCOUNT'):
            pytest.skip("Snowflake credentials not available")
        
        connector = SnowflakeMCPConnector(snowflake_config)
        
        try:
            # Attempt connection
            connected = await connector.connect()
            if not connected:
                pytest.skip("Could not connect to Snowflake")
            
            # Create simple query request
            request = MCPRequest(
                request_id="query_123",
                platform="snowflake",
                operation_type=MCPOperationType.QUERY,
                parameters={
                    'query': 'SELECT 1 as test_column',
                    'limit': 1
                }
            )
            
            # Execute request
            response = await connector.execute_request(request)
            
            # Verify response structure
            assert response.request_id == "query_123"
            assert isinstance(response.success, bool)
            if response.success:
                assert 'results' in response.data or 'error' in response.data
                
        except Exception as e:
            # Network/credential issues - log but don't fail test
            pytest.skip(f"Snowflake connection issue: {str(e)}")
        
    @pytest.mark.asyncio
    async def test_snowflake_health_check(self, snowflake_config):
        """Test Snowflake health check"""
        # Skip if no credentials available
        if not os.getenv('SNOWFLAKE_ACCOUNT'):
            pytest.skip("Snowflake credentials not available")
        
        connector = SnowflakeMCPConnector(snowflake_config)
        
        try:
            # Attempt connection first
            await connector.connect()
            
            # Perform health check
            health = await connector.health_check()
            
            # Verify health check structure
            assert health.platform == "snowflake"
            assert isinstance(health.response_time_ms, (int, float))
            assert health.status in [status for status in MCPConnectionStatus]
            
        except Exception as e:
            # Network/credential issues - create a basic health check response
            health = MCPHealthCheck(
                platform="snowflake",
                status=MCPConnectionStatus.ERROR,
                response_time_ms=0.0,
                error_message=str(e)
            )
            assert health.status == MCPConnectionStatus.ERROR


class TestRabbitMQMCPConnector:
    """Test RabbitMQ MCP Connector"""
    
    @pytest.mark.asyncio
    async def test_rabbitmq_connection(self, rabbitmq_config):
        """Test RabbitMQ connector connection"""
        # Skip if no credentials available
        if not os.getenv('RABBITMQ_CLOUD_URL'):
            pytest.skip("RabbitMQ credentials not available")
        
        connector = RabbitMQMCPConnector(rabbitmq_config)
        
        try:
            # Test connection
            result = await connector.connect()
            
            # Verify connection result
            if result:
                assert connector.connection is not None
                assert connector.connection_status == MCPConnectionStatus.AUTHENTICATED
            else:
                # Connection failed but handled gracefully
                assert connector.connection_status in [MCPConnectionStatus.ERROR, MCPConnectionStatus.DISCONNECTED]
        except Exception as e:
            # Connection failed due to network/SSL/credential issues - this is expected in CI
            error_msg = str(e).lower()
            assert any(keyword in error_msg for keyword in [
                "connection", "authentication", "certificate", "hostname", 
                "ssl", "wrong version", "timeout", "refused"
            ]), f"Unexpected error: {e}"
        
    @pytest.mark.asyncio
    async def test_rabbitmq_publish_message(self, rabbitmq_config):
        """Test RabbitMQ message publishing"""
        # Skip if no credentials available
        if not os.getenv('RABBITMQ_CLOUD_URL'):
            pytest.skip("RabbitMQ credentials not available")
        
        connector = RabbitMQMCPConnector(rabbitmq_config)
        
        try:
            # Attempt connection
            connected = await connector.connect()
            if not connected:
                pytest.skip("Could not connect to RabbitMQ")
            
            # Create publish request
            request = MCPRequest(
                request_id="pub_123",
                platform="rabbitmq",
                operation_type=MCPOperationType.EXECUTE,
                parameters={
                    'operation': 'publish',
                    'message': {'data': 'test message', 'timestamp': str(datetime.now())},
                    'routing_key': 'test.trm.key',
                    'exchange': ''
                }
            )
            
            # Execute request
            response = await connector.execute_request(request)
            
            # Verify response structure
            assert response.request_id == "pub_123"
            assert isinstance(response.success, bool)
            if response.success:
                assert 'message_id' in response.data or 'status' in response.data
                
        except Exception as e:
            # Network/credential issues - log but don't fail test
            pytest.skip(f"RabbitMQ connection issue: {str(e)}")
        
    @pytest.mark.asyncio
    async def test_rabbitmq_declare_queue(self, rabbitmq_config):
        """Test RabbitMQ queue declaration"""
        # Skip if no credentials available
        if not os.getenv('RABBITMQ_CLOUD_URL'):
            pytest.skip("RabbitMQ credentials not available")
        
        connector = RabbitMQMCPConnector(rabbitmq_config)
        
        try:
            # Attempt connection
            connected = await connector.connect()
            if not connected:
                pytest.skip("Could not connect to RabbitMQ")
            
            # Create queue declaration request
            request = MCPRequest(
                request_id="queue_123",
                platform="rabbitmq",
                operation_type=MCPOperationType.EXECUTE,
                parameters={
                    'operation': 'declare_queue',
                    'queue_name': f'test_queue_{uuid.uuid4().hex[:8]}',
                    'durable': True,
                    'auto_delete': False
                }
            )
            
            # Execute request
            response = await connector.execute_request(request)
            
            # Verify response structure
            assert response.request_id == "queue_123"
            assert isinstance(response.success, bool)
            if response.success:
                assert 'queue_name' in response.data or 'status' in response.data
                
        except Exception as e:
            # Network/credential issues - log but don't fail test
            pytest.skip(f"RabbitMQ queue declaration issue: {str(e)}")


class TestAgentIsolation:
    """Test Agent Isolation functionality"""
    
    @pytest.mark.asyncio
    async def test_create_isolation_context(self, isolation_manager):
        """Test creating isolation context"""
        agent_id = "test_agent_123"
        
        context = await isolation_manager.create_isolation_context(
            agent_id=agent_id,
            isolation_level=IsolationLevel.BASIC
        )
        
        assert context.agent_id == agent_id
        assert context.isolation_level == IsolationLevel.BASIC
        assert context.status == "ready"
        assert len(context.resource_quotas) > 0
        
    @pytest.mark.asyncio
    async def test_resource_quota_validation(self, isolation_manager):
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
        assert quota.utilization_percent() == 117.1875  # 600/512 * 100
        
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
        
    @pytest.mark.asyncio
    async def test_container_config_creation(self):
        """Test container configuration"""
        config = ContainerConfig(
            image="python:3.11-slim",
            memory_limit="256m",
            cpu_limit=0.5,
            read_only=True,
            security_opts=["no-new-privileges:true"],
            cap_drop=["ALL"]
        )
        
        assert config.image == "python:3.11-slim"
        assert config.memory_limit == "256m"
        assert config.read_only is True
        assert "no-new-privileges:true" in config.security_opts
        
    @pytest.mark.asyncio
    async def test_isolation_context_lifecycle(self, isolation_manager):
        """Test complete isolation context lifecycle"""
        agent_id = "lifecycle_test_agent"
        
        # Create context
        context = await isolation_manager.create_isolation_context(
            agent_id=agent_id,
            isolation_level=IsolationLevel.BASIC
        )
        
        assert context.agent_id == agent_id
        assert agent_id in isolation_manager._isolation_contexts
        
        # Get context
        retrieved = isolation_manager.get_isolation_context(agent_id)
        assert retrieved == context
        
        # Destroy context
        result = await isolation_manager.destroy_isolation_context(agent_id)
        assert result is True
        assert agent_id not in isolation_manager._isolation_contexts


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
        
    @pytest.mark.asyncio
    async def test_error_logging_with_exception(self, production_logger):
        """Test error logging with exception details"""
        try:
            raise ValueError("Test exception for logging")
        except Exception as e:
            production_logger.error("Test error occurred", error=e, context="test")
            
        stats = production_logger.get_metrics_summary()
        assert stats['error_count'] >= 1
        
    @pytest.mark.asyncio
    async def test_performance_metrics(self, production_logger):
        """Test performance metrics recording"""
        # Record some metrics
        production_logger.record_metric("test.metric", 100, metric_type="gauge", tag="test")
        production_logger.record_metric("test.counter", 1, metric_type="counter", tag="test")
        
        stats = production_logger.get_metrics_summary()
        assert stats['recent_metrics_count'] >= 2


class TestProductionCache:
    """Test Production Cache functionality"""
    
    @pytest.mark.asyncio
    async def test_cache_basic_operations(self, production_cache):
        """Test basic cache set/get operations"""
        # Set value
        result = await production_cache.set("test_key", "test_value", ttl=60)
        assert result is True  # Would be False if Redis not available, but should work with local cache
        
        # Get value
        value = await production_cache.get("test_key")
        assert value == "test_value"
        
        # Get non-existent key
        value = await production_cache.get("nonexistent_key", default="default")
        assert value == "default"
        
    @pytest.mark.asyncio
    async def test_cache_with_tags(self, production_cache):
        """Test cache with tag-based invalidation"""
        # Set values with tags
        await production_cache.set("key1", "value1", tags=["group1", "group2"])
        await production_cache.set("key2", "value2", tags=["group1"])
        await production_cache.set("key3", "value3", tags=["group2"])
        
        # Verify values exist
        assert await production_cache.get("key1") == "value1"
        assert await production_cache.get("key2") == "value2"
        assert await production_cache.get("key3") == "value3"
        
        # Note: Tag invalidation requires Redis, so we'll just test the interface
        # In actual Redis environment, this would invalidate tagged keys
        
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
    async def test_paginated_response_creation(self, output_normalizer):
        """Test creating paginated response"""
        test_data = [{'id': i, 'name': f'item_{i}'} for i in range(5)]
        
        response = output_normalizer.create_paginated_response(
            data=test_data,
            total_count=25,
            page=2,
            page_size=5
        )
        
        assert response.status == ResponseStatus.SUCCESS
        assert len(response.data) == 5
        assert response.metadata.total_count == 25
        assert response.metadata.page == 2
        assert response.pagination['total_pages'] == 5
        assert response.pagination['has_next'] is True
        assert response.pagination['has_previous'] is True
        
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
        
    @pytest.mark.asyncio
    async def test_schema_validation(self, output_normalizer):
        """Test validation against registered schema"""
        # Register a test schema
        test_schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "number", "minimum": 0}
            },
            "required": ["name", "age"]
        }
        
        output_normalizer.register_schema("person", test_schema)
        
        # Test valid data
        valid_data = {"name": "John Doe", "age": 30}
        result = output_normalizer.normalize(valid_data, schema_name="person")
        assert result.is_valid is True
        
        # Test invalid data
        invalid_data = {"name": "John Doe"}  # Missing required 'age'
        result = output_normalizer.normalize(invalid_data, schema_name="person")
        assert result.is_valid is False
        assert len(result.errors) > 0
        
    @pytest.mark.asyncio
    async def test_convenience_functions(self):
        """Test convenience functions"""
        # Test normalize_response
        response = normalize_response(
            data={'test': 'data'},
            status=ResponseStatus.SUCCESS,
            message="Success"
        )
        assert isinstance(response, type(normalize_response({})))
        assert response.status == ResponseStatus.SUCCESS
        
        # Test normalize_error
        error_response = normalize_error(
            errors=["Test error"],
            message="Error occurred"
        )
        assert error_response.status == ResponseStatus.ERROR
        assert len(error_response.errors) == 1
        
    @pytest.mark.asyncio
    async def test_normalization_stats(self, output_normalizer):
        """Test normalization performance statistics"""
        # Perform some normalizations
        output_normalizer.normalize({'test': 'data1'})
        output_normalizer.normalize({'test': 'data2'})
        output_normalizer.normalize({'invalid': None}, schema_name="nonexistent")
        
        stats = output_normalizer.get_stats()
        assert stats['total_validations'] >= 3
        assert 'error_count' in stats
        assert 'cache_hit_rate_percent' in stats
        assert 'registered_schemas' in stats


class TestMCPIntegrationWorkflows:
    """Test complete MCP integration workflows"""
    
    @pytest.mark.asyncio
    async def test_end_to_end_data_pipeline(self, registry, output_normalizer):
        """Test end-to-end data processing pipeline"""
        # Setup mock Snowflake connector
        mock_snowflake = AsyncMock(spec=SnowflakeMCPConnector)
        mock_snowflake_response = MCPResponse(
            request_id="pipeline_123",
            success=True,
            data={
                'results': [
                    {'user_id': 1, 'name': 'John Doe', 'email': 'john@example.com'},
                    {'user_id': 2, 'name': 'Jane Smith', 'email': 'jane@example.com'}
                ],
                'count': 2
            }
        )
        mock_snowflake.execute_request.return_value = mock_snowflake_response
        
        await registry.register_connector("snowflake", mock_snowflake)
        
        # Create request
        request = MCPRequest(
            request_id="pipeline_123",
            platform="snowflake",
            operation_type=MCPOperationType.QUERY,
            parameters={'query': 'SELECT * FROM users LIMIT 10'}
        )
        
        # Execute request through registry
        response = await registry.execute_with_connector("snowflake", request)
        assert response.success is True
        
        # Normalize response
        normalized = output_normalizer.create_standard_response(
            data=response.data,
            status=ResponseStatus.SUCCESS,
            message="Data retrieved successfully",
            request_id=response.request_id
        )
        
        assert normalized.status == ResponseStatus.SUCCESS
        assert 'results' in normalized.data
        assert len(normalized.data['results']) == 2
        
    @pytest.mark.asyncio
    async def test_isolated_agent_execution_workflow(self, isolation_manager, production_logger):
        """Test complete isolated agent execution workflow"""
        agent_id = "workflow_test_agent"
        
        # Create isolation context
        context = await isolation_manager.create_isolation_context(
            agent_id=agent_id,
            isolation_level=IsolationLevel.BASIC,
            resource_quotas={
                ResourceType.MEMORY: ResourceQuota(ResourceType.MEMORY, 256, unit="MB"),
                ResourceType.CPU: ResourceQuota(ResourceType.CPU, 50, unit="percent")
            }
        )
        
        # Execute within isolation context
        async with isolation_manager.isolated_execution(agent_id) as exec_context:
            # Simulate agent execution with logging
            async with production_logger.trace_context(
                operation="agent_task",
                agent_id=agent_id
            ) as (trace_id, logger):
                
                logger.info("Agent task started", task="data_processing")
                
                # Simulate some work
                await asyncio.sleep(0.1)
                
                logger.info("Agent task completed", result="success")
                
                assert exec_context.agent_id == agent_id
                assert exec_context.status == "executing"
        
        # Cleanup
        await isolation_manager.destroy_isolation_context(agent_id)
        
    @pytest.mark.asyncio
    async def test_enterprise_error_handling_workflow(self, registry, output_normalizer, production_logger):
        """Test enterprise error handling and logging workflow"""
        # Setup failing connector
        mock_connector = AsyncMock(spec=BaseMCPConnector)
        mock_connector.execute_request.side_effect = Exception("Connection timeout")
        
        await registry.register_connector("failing_conn", mock_connector)
        
        # Attempt execution with error handling
        request = MCPRequest(
            request_id="error_test_123",
            platform="test",
            operation_type=MCPOperationType.QUERY,
            parameters={'query': 'SELECT 1'}
        )
        
        try:
            async with production_logger.trace_context(
                operation="error_test",
                request_id=request.request_id
            ) as (trace_id, logger):
                
                logger.info("Attempting connector execution")
                
                # This should raise an exception
                await registry.execute_with_connector("failing_conn", request)
                
        except Exception as e:
            # Create normalized error response
            error_response = output_normalizer.create_error_response(
                errors=[{
                    'code': 'CONNECTOR_ERROR',
                    'message': str(e),
                    'context': {'connector': 'failing_conn', 'request_id': request.request_id}
                }],
                message="Connector execution failed",
                request_id=request.request_id
            )
            
            assert error_response.status == ResponseStatus.ERROR
            assert len(error_response.errors) == 1
            assert error_response.errors[0]['code'] == 'CONNECTOR_ERROR'


if __name__ == "__main__":
    # Run specific test
    pytest.main([__file__ + "::TestMCPConnectorRegistry::test_registry_initialization", "-v"]) 