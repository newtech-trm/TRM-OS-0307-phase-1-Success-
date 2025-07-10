#!/usr/bin/env python3
"""
Integration Tests for MCP Conversational Intelligence
===================================================

Test MCP Conversational Coordinator và API endpoints
theo AGE_COMPREHENSIVE_SYSTEM_DESIGN_V2.md
"""

import pytest
import asyncio
from unittest.mock import patch, MagicMock
from datetime import datetime

from trm_api.v2.conversation.mcp_conversational_coordinator import (
    MCPConversationalCoordinator,
    ConversationalMCPIntent,
    MCPConversationalContext,
    MCPConversationalResult
)
from trm_api.v2.conversation.session_manager import ConversationContext
from trm_api.v2.conversation.nlp_processor import ParsedIntent, IntentType


class TestMCPConversationalCoordinator:
    """Test MCP Conversational Coordinator functionality"""
    
    @pytest.fixture
    def coordinator(self):
        """Create MCP Conversational Coordinator instance"""
        return MCPConversationalCoordinator()
    
    @pytest.fixture
    def conversation_context(self):
        """Create conversation context for testing"""
        return ConversationContext(
            user_id="test_user",
            session_id="test_session_123",
            conversation_history=[],
            user_preferences={"language": "vi"},
            context_metadata={"test": True}
        )
    
    @pytest.mark.asyncio
    async def test_coordinator_initialization(self, coordinator):
        """Test MCP Conversational Coordinator initialization"""
        # Kiểm tra coordinator được khởi tạo thành công
        assert coordinator is not None
        assert coordinator.mcp_registry is not None
        assert coordinator.conversation_processor is not None
        assert coordinator.response_generator is not None
        assert coordinator.production_logger is not None
        assert coordinator.production_cache is not None
        
        # Kiểm tra MCP patterns được load
        assert coordinator.mcp_patterns is not None
        assert 'vi' in coordinator.mcp_patterns
        assert 'en' in coordinator.mcp_patterns
    
    @pytest.mark.asyncio
    async def test_identify_mcp_intent_snowflake(self, coordinator):
        """Test identification của Snowflake MCP intent"""
        # Test Vietnamese
        parsed_intent_vi = ParsedIntent(
            intent_type=IntentType.SEARCH_KNOWLEDGE,
            confidence=0.8,
            entities={},
            context={},
            original_message="kết nối snowflake và lấy dữ liệu",
            language="vi"
        )
        
        intent = await coordinator._identify_mcp_intent(parsed_intent_vi)
        assert intent == ConversationalMCPIntent.CONNECT_TO_SNOWFLAKE
        
        # Test English
        parsed_intent_en = ParsedIntent(
            intent_type=IntentType.SEARCH_KNOWLEDGE,
            confidence=0.8,
            entities={},
            context={},
            original_message="connect to snowflake and query data",
            language="en"
        )
        
        intent = await coordinator._identify_mcp_intent(parsed_intent_en)
        assert intent == ConversationalMCPIntent.CONNECT_TO_SNOWFLAKE
    
    @pytest.mark.asyncio
    async def test_identify_mcp_intent_rabbitmq(self, coordinator):
        """Test identification của RabbitMQ MCP intent"""
        parsed_intent = ParsedIntent(
            intent_type=IntentType.UPDATE_RESOURCE,
            confidence=0.8,
            entities={},
            context={},
            original_message="gửi tin nhắn test qua rabbitmq",
            language="vi"
        )
        
        intent = await coordinator._identify_mcp_intent(parsed_intent)
        assert intent == ConversationalMCPIntent.SEND_RABBITMQ_MESSAGE
    
    @pytest.mark.asyncio
    async def test_extract_mcp_context_snowflake(self, coordinator, conversation_context):
        """Test extraction của MCP context cho Snowflake operations"""
        parsed_intent = ParsedIntent(
            intent_type=IntentType.SEARCH_KNOWLEDGE,
            confidence=0.8,
            entities={"query": "SELECT * FROM users"},
            context={},
            original_message="truy vấn dữ liệu: SELECT * FROM users",
            language="vi"
        )
        
        mcp_intent = ConversationalMCPIntent.QUERY_SNOWFLAKE_DATA
        
        context = await coordinator._extract_mcp_context(
            parsed_intent, mcp_intent, conversation_context
        )
        
        assert context.mcp_intent == ConversationalMCPIntent.QUERY_SNOWFLAKE_DATA
        assert context.connector_type == "snowflake"
        assert context.natural_language_query == "truy vấn dữ liệu: SELECT * FROM users"
        assert context.conversation_context == conversation_context
    
    @pytest.mark.asyncio
    async def test_extract_mcp_context_rabbitmq(self, coordinator, conversation_context):
        """Test extraction của MCP context cho RabbitMQ operations"""
        parsed_intent = ParsedIntent(
            intent_type=IntentType.UPDATE_RESOURCE,
            confidence=0.8,
            entities={"message_content": "Hello World", "queue_name": "notifications"},
            context={},
            original_message="gửi tin nhắn Hello World tới queue notifications",
            language="vi"
        )
        
        mcp_intent = ConversationalMCPIntent.SEND_RABBITMQ_MESSAGE
        
        context = await coordinator._extract_mcp_context(
            parsed_intent, mcp_intent, conversation_context
        )
        
        assert context.mcp_intent == ConversationalMCPIntent.SEND_RABBITMQ_MESSAGE
        assert context.connector_type == "rabbitmq"
        assert context.operation_params["message"] == "Hello World"
        assert context.operation_params["queue"] == "notifications"
    
    @pytest.mark.asyncio
    async def test_process_conversational_mcp_request_success(self, coordinator, conversation_context):
        """Test successful processing của conversational MCP request"""
        
        # Mock MCP operations để avoid real connections
        with patch.object(coordinator, '_execute_mcp_operation') as mock_execute:
            mock_execute.return_value = {
                "success": True,
                "operation": "test_operation",
                "result": {"data": "test_data"}
            }
            
            with patch.object(coordinator, '_generate_mcp_response') as mock_response:
                mock_response.return_value = MagicMock(
                    text="Operation completed successfully",
                    metadata={"confidence": 0.9}
                )
                
                result = await coordinator.process_conversational_mcp_request(
                    "kiểm tra trạng thái connectors",
                    conversation_context
                )
                
                assert isinstance(result, MCPConversationalResult)
                assert result.operation_success == True
                assert result.execution_time > 0
                assert len(result.suggested_follow_ups) > 0
    
    @pytest.mark.asyncio
    async def test_execute_health_check(self, coordinator):
        """Test health check execution"""
        
        # Mock registry status
        with patch.object(coordinator.mcp_registry, 'get_registry_status') as mock_status:
            mock_status.return_value = MagicMock(
                total_connectors=2,
                active_connectors=2,
                healthy_connectors=2
            )
            
            # Mock connector health checks
            with patch.object(coordinator.mcp_registry, '_connectors', {
                'snowflake': MagicMock(),
                'rabbitmq': MagicMock()
            }):
                # Mock health check responses
                for connector in coordinator.mcp_registry._connectors.values():
                    connector.health_check.return_value = MagicMock(
                        is_healthy=True,
                        response_time=0.1,
                        details={"status": "ok"}
                    )
                
                context = MCPConversationalContext(
                    mcp_intent=ConversationalMCPIntent.CHECK_CONNECTOR_STATUS,
                    connector_type="all",
                    operation_params={"check_type": "health"},
                    natural_language_query="kiểm tra trạng thái",
                    user_intent=MagicMock(),
                    conversation_context=MagicMock()
                )
                
                result = await coordinator._execute_health_check(context)
                
                assert result["success"] == True
                assert "registry_status" in result
                assert "connector_health" in result
                assert len(result["connector_health"]) == 2
    
    @pytest.mark.asyncio
    async def test_handle_voice_activated_mcp(self, coordinator):
        """Test voice-activated MCP operations"""
        
        # Mock conversational MCP processing
        with patch.object(coordinator, 'process_conversational_mcp_request') as mock_process:
            mock_result = MCPConversationalResult(
                operation_success=True,
                mcp_result={"data": "voice_test"},
                natural_response=MagicMock(
                    text="Voice command processed",
                    metadata={}
                ),
                suggested_follow_ups=["Try another command"],
                execution_time=0.5,
                connector_used="test"
            )
            mock_process.return_value = mock_result
            
            result = await coordinator.handle_voice_activated_mcp("kiểm tra hệ thống")
            
            assert result.operation_success == True
            assert result.natural_response.metadata["voice_response"] == True
            assert result.natural_response.metadata["speech_synthesis_ready"] == True
    
    @pytest.mark.asyncio
    async def test_get_mcp_performance_metrics(self, coordinator):
        """Test getting MCP performance metrics"""
        
        # Mock registry status
        with patch.object(coordinator.mcp_registry, 'get_registry_status') as mock_status:
            mock_status.return_value = MagicMock(
                total_connectors=2,
                active_connectors=2
            )
            
            # Mock cache statistics
            with patch.object(coordinator.production_cache, 'get_statistics') as mock_cache:
                mock_cache.return_value = {
                    "hit_rate": 0.85,
                    "total_requests": 100
                }
                
                metrics = await coordinator.get_mcp_performance_metrics()
                
                assert "registry_metrics" in metrics
                assert "cache_metrics" in metrics
                assert metrics["active_connectors"] >= 0
                assert metrics["voice_enabled"] == True
    
    @pytest.mark.asyncio 
    async def test_generate_follow_up_suggestions(self, coordinator):
        """Test generation của follow-up suggestions"""
        
        # Test Snowflake suggestions
        context = MCPConversationalContext(
            mcp_intent=ConversationalMCPIntent.QUERY_SNOWFLAKE_DATA,
            connector_type="snowflake",
            operation_params={},
            natural_language_query="test",
            user_intent=MagicMock(),
            conversation_context=MagicMock()
        )
        
        suggestions = await coordinator._generate_follow_up_suggestions(context, {"success": True})
        
        assert len(suggestions) > 0
        assert any("truy vấn" in s.lower() for s in suggestions)
        
        # Test RabbitMQ suggestions
        context.mcp_intent = ConversationalMCPIntent.SEND_RABBITMQ_MESSAGE
        suggestions = await coordinator._generate_follow_up_suggestions(context, {"success": True})
        
        assert len(suggestions) > 0
        assert any("tin nhắn" in s.lower() for s in suggestions)


class TestMCPConversationalAPI:
    """Test MCP Conversational API endpoints"""
    
    @pytest.mark.asyncio
    async def test_api_integration_available(self):
        """Test that MCP Conversational API integration is available"""
        # Import để verify API endpoints exist
        try:
            from trm_api.v2.endpoints.mcp_conversational import router
            assert router is not None
            
            from trm_api.v2.api import v2_router
            assert v2_router is not None
            
        except ImportError as e:
            pytest.fail(f"MCP Conversational API integration not available: {e}")
    
    @pytest.mark.asyncio
    async def test_mcp_conversational_request_model(self):
        """Test MCP Conversational request model"""
        from trm_api.v2.endpoints.mcp_conversational import MCPConversationalRequest
        
        # Test valid request
        request = MCPConversationalRequest(
            message="kết nối snowflake",
            user_id="test_user",
            session_id="test_session",
            language="vi",
            voice_input=False
        )
        
        assert request.message == "kết nối snowflake"
        assert request.user_id == "test_user"
        assert request.language == "vi"
        assert request.voice_input == False
    
    @pytest.mark.asyncio
    async def test_mcp_conversational_response_model(self):
        """Test MCP Conversational response model"""
        from trm_api.v2.endpoints.mcp_conversational import MCPConversationalResponse
        
        # Test response model structure
        response = MCPConversationalResponse(
            success=True,
            operation_result={"data": "test"},
            natural_response="Kết nối thành công",
            response_metadata={"confidence": 0.9},
            suggested_follow_ups=["Truy vấn dữ liệu"],
            execution_time=0.5,
            connector_used="snowflake"
        )
        
        assert response.success == True
        assert response.natural_response == "Kết nối thành công"
        assert len(response.suggested_follow_ups) == 1
        assert response.execution_time == 0.5 