#!/usr/bin/env python3
"""
MCP Conversational Coordinator for TRM-OS v2.2
=============================================

Tích hợp MCP (Model Context Protocol) với Conversational Intelligence
để thực hiện Natural Language MCP Operations theo AGE_COMPREHENSIVE_SYSTEM_DESIGN_V2.md

Core capabilities:
- Natural Language MCP Operations
- Commercial AI Coordination cho conversations
- Voice-Activated Infrastructure integration
- Intelligent MCP connector management
"""

import asyncio
import json
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from enum import Enum
from datetime import datetime

from trm_api.core.logging_config import get_logger
from trm_api.protocols.mcp_connectors.mcp_connector_registry import MCPConnectorRegistry
from trm_api.protocols.mcp_connectors.snowflake_mcp import SnowflakeMCPConnector
from trm_api.protocols.mcp_connectors.rabbitmq_mcp import RabbitMQMCPConnector
from trm_api.enterprise.production_infrastructure import ProductionLogger, ProductionCache
from .nlp_processor import ParsedIntent, EntityContext, ConversationProcessor
from .response_generator import GeneratedResponse, NaturalResponseGenerator, ResponseContext
from .session_manager import ConversationContext

logger = get_logger(__name__)


class MCPOperationType(Enum):
    """Các loại MCP operations có thể thực hiện qua natural language"""
    QUERY_DATABASE = "query_database"
    ANALYZE_DATA = "analyze_data"
    SEND_MESSAGE = "send_message"
    MANAGE_CONNECTOR = "manage_connector"
    CHECK_HEALTH = "check_health"
    EXECUTE_COMMAND = "execute_command"
    STREAM_DATA = "stream_data"
    BATCH_PROCESS = "batch_process"


class ConversationalMCPIntent(Enum):
    """MCP-specific intents từ conversational input"""
    CONNECT_TO_SNOWFLAKE = "connect_to_snowflake"
    QUERY_SNOWFLAKE_DATA = "query_snowflake_data"
    SEND_RABBITMQ_MESSAGE = "send_rabbitmq_message"
    CHECK_CONNECTOR_STATUS = "check_connector_status"
    MANAGE_MCP_REGISTRY = "manage_mcp_registry"
    ANALYZE_ENTERPRISE_DATA = "analyze_enterprise_data"
    STREAM_REAL_TIME_DATA = "stream_real_time_data"
    BATCH_PROCESS_DATA = "batch_process_data"


@dataclass
class MCPConversationalContext:
    """Context cho MCP operations từ natural language"""
    mcp_intent: ConversationalMCPIntent
    connector_type: str
    operation_params: Dict[str, Any]
    natural_language_query: str
    user_intent: ParsedIntent
    conversation_context: ConversationContext
    priority_level: int = 5


@dataclass
class MCPConversationalResult:
    """Kết quả MCP operation với natural language response"""
    operation_success: bool
    mcp_result: Dict[str, Any]
    natural_response: GeneratedResponse
    suggested_follow_ups: List[str]
    execution_time: float
    connector_used: str


class MCPConversationalCoordinator:
    """
    Coordinator cho MCP operations thông qua natural language
    
    Theo AGE_COMPREHENSIVE_SYSTEM_DESIGN_V2.md:
    - MCP Universal Data Access
    - Commercial AI Coordination
    - Natural Language Interface
    - Enterprise Integration
    """
    
    def __init__(self):
        self.mcp_registry = MCPConnectorRegistry()
        self.conversation_processor = ConversationProcessor(agent_id="mcp_conversational_coordinator")
        self.response_generator = NaturalResponseGenerator()
        self.production_logger = ProductionLogger(service_name="mcp_conversational_coordinator")
        self.production_cache = ProductionCache()
        
        # Initialize MCP connectors
        self.snowflake_connector = None
        self.rabbitmq_connector = None
        self._initialize_connectors()
        
        # Natural language patterns cho MCP operations
        self.mcp_patterns = self._load_mcp_patterns()
        
    def _initialize_connectors(self):
        """Initialize MCP connectors for conversational operations"""
        try:
            # Initialize Snowflake MCP Connector
            self.snowflake_connector = SnowflakeMCPConnector(
                config={
                    "account": "cpsbyse-la15176",
                    "user": "newtech",
                    "password": "4HhK57r4cJSpK4W",
                    "database": "NEWTECH_DB",
                    "warehouse": "COMPUTE_WH"
                }
            )
            
            # Initialize RabbitMQ MCP Connector
            self.rabbitmq_connector = RabbitMQMCPConnector(
                config={
                    "url": "amqps://hpzbofxa:VvMYrgYM4BlQ1BIhbQJsdGn7Pqs48V1D@fuji.lmq.cloudamqp.com/hpzbofxa",
                    "instance_id": "487cc21f-b0a5-4e82-9046-f89d412e9fe8"
                }
            )
            
            # Register connectors
            self.mcp_registry.register_connector("snowflake", self.snowflake_connector)
            self.mcp_registry.register_connector("rabbitmq", self.rabbitmq_connector)
            
            logger.info("MCP connectors initialized for conversational operations")
            
        except Exception as e:
            logger.error(f"Failed to initialize MCP connectors: {e}")
    
    def _load_mcp_patterns(self) -> Dict[str, List[str]]:
        """Load natural language patterns cho MCP operations"""
        return {
            'vi': {
                ConversationalMCPIntent.CONNECT_TO_SNOWFLAKE.value: [
                    "kết nối snowflake", "connect snowflake", "kết nối database",
                    "truy cập dữ liệu snowflake", "mở kết nối snowflake"
                ],
                ConversationalMCPIntent.QUERY_SNOWFLAKE_DATA.value: [
                    "truy vấn dữ liệu", "query data", "tìm kiếm trong database",
                    "lấy dữ liệu từ", "select * from", "show tables"
                ],
                ConversationalMCPIntent.SEND_RABBITMQ_MESSAGE.value: [
                    "gửi tin nhắn", "send message", "publish message",
                    "gửi event", "thông báo", "message queue"
                ],
                ConversationalMCPIntent.CHECK_CONNECTOR_STATUS.value: [
                    "kiểm tra trạng thái", "check status", "health check",
                    "connector status", "kết nối có ổn không"
                ],
                ConversationalMCPIntent.MANAGE_MCP_REGISTRY.value: [
                    "quản lý connector", "manage registry", "list connectors",
                    "đăng ký connector", "xóa connector"
                ]
            },
            'en': {
                ConversationalMCPIntent.CONNECT_TO_SNOWFLAKE.value: [
                    "connect to snowflake", "snowflake connection", "database connection",
                    "access snowflake data", "open snowflake connection"
                ],
                ConversationalMCPIntent.QUERY_SNOWFLAKE_DATA.value: [
                    "query data", "search database", "get data from",
                    "select from", "show tables", "database query"
                ],
                ConversationalMCPIntent.SEND_RABBITMQ_MESSAGE.value: [
                    "send message", "publish message", "send event",
                    "notify", "message queue", "publish to queue"
                ],
                ConversationalMCPIntent.CHECK_CONNECTOR_STATUS.value: [
                    "check status", "health check", "connector status",
                    "is connection ok", "system health"
                ],
                ConversationalMCPIntent.MANAGE_MCP_REGISTRY.value: [
                    "manage connectors", "list connectors", "register connector",
                    "remove connector", "connector registry"
                ]
            }
        }
    
    async def process_conversational_mcp_request(
        self, 
        message: str, 
        conversation_context: ConversationContext
    ) -> MCPConversationalResult:
        """
        Process natural language request cho MCP operations
        
        Args:
            message: Natural language message từ user
            conversation_context: Current conversation context
            
        Returns:
            MCPConversationalResult với operation results và natural response
        """
        start_time = datetime.now()
        
        try:
            # Log conversational MCP request
            self.production_logger.info(
                "Processing conversational MCP request",
                message=message,
                user_id=conversation_context.user_id,
                session_id=conversation_context.session_id
            )
            
            # Parse natural language intent
            parsed_intent = await self.conversation_processor.parse_natural_language_query(message)
            
            # Identify MCP-specific intent
            mcp_intent = await self._identify_mcp_intent(parsed_intent)
            
            # Extract MCP operation context
            mcp_context = await self._extract_mcp_context(parsed_intent, mcp_intent, conversation_context)
            
            # Execute MCP operation
            mcp_result = await self._execute_mcp_operation(mcp_context)
            
            # Generate natural language response
            natural_response = await self._generate_mcp_response(mcp_context, mcp_result)
            
            # Calculate execution time
            execution_time = (datetime.now() - start_time).total_seconds()
            
            # Create result
            result = MCPConversationalResult(
                operation_success=mcp_result.get("success", False),
                mcp_result=mcp_result,
                natural_response=natural_response,
                suggested_follow_ups=await self._generate_follow_up_suggestions(mcp_context, mcp_result),
                execution_time=execution_time,
                connector_used=mcp_context.connector_type
            )
            
            # Cache result for performance
            await self.production_cache.set(
                key=f"mcp_conversation:{conversation_context.session_id}:{hash(message)}",
                value=result.__dict__,
                ttl=300  # 5 minutes
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing conversational MCP request: {e}")
            
            # Generate error response
            error_response = await self.response_generator._generate_error_response(
                error_message=f"Xin lỗi, tôi gặp lỗi khi xử lý yêu cầu MCP: {str(e)}",
                language=parsed_intent.language if 'parsed_intent' in locals() else 'vi'
            )
            
            return MCPConversationalResult(
                operation_success=False,
                mcp_result={"error": str(e)},
                natural_response=error_response,
                suggested_follow_ups=["Thử lại sau", "Kiểm tra kết nối", "Liên hệ hỗ trợ"],
                execution_time=(datetime.now() - start_time).total_seconds(),
                connector_used="none"
            )
    
    async def _identify_mcp_intent(self, parsed_intent: ParsedIntent) -> ConversationalMCPIntent:
        """Identify MCP-specific intent từ parsed natural language"""
        message = parsed_intent.original_message.lower()
        language = parsed_intent.language
        
        # Check patterns cho each MCP intent
        for intent_name, patterns in self.mcp_patterns[language].items():
            for pattern in patterns:
                if pattern in message:
                    return ConversationalMCPIntent(intent_name)
        
        # Default fallback
        if "snowflake" in message or "database" in message:
            return ConversationalMCPIntent.QUERY_SNOWFLAKE_DATA
        elif "message" in message or "send" in message:
            return ConversationalMCPIntent.SEND_RABBITMQ_MESSAGE
        elif "status" in message or "health" in message:
            return ConversationalMCPIntent.CHECK_CONNECTOR_STATUS
        else:
            return ConversationalMCPIntent.MANAGE_MCP_REGISTRY
    
    async def _extract_mcp_context(
        self, 
        parsed_intent: ParsedIntent, 
        mcp_intent: ConversationalMCPIntent,
        conversation_context: ConversationContext
    ) -> MCPConversationalContext:
        """Extract MCP operation context từ natural language"""
        
        # Determine connector type
        connector_type = "snowflake"
        if mcp_intent in [ConversationalMCPIntent.SEND_RABBITMQ_MESSAGE]:
            connector_type = "rabbitmq"
        
        # Extract operation parameters
        operation_params = {}
        
        if mcp_intent == ConversationalMCPIntent.QUERY_SNOWFLAKE_DATA:
            # Extract SQL query or table name
            message = parsed_intent.original_message
            if "select" in message.lower():
                operation_params["query"] = message
            elif "table" in message.lower():
                operation_params["operation"] = "show_tables"
            else:
                operation_params["operation"] = "describe_database"
                
        elif mcp_intent == ConversationalMCPIntent.SEND_RABBITMQ_MESSAGE:
            # Extract message content
            operation_params["message"] = parsed_intent.entities.get("message_content", parsed_intent.original_message)
            operation_params["queue"] = parsed_intent.entities.get("queue_name", "default")
            
        elif mcp_intent == ConversationalMCPIntent.CHECK_CONNECTOR_STATUS:
            operation_params["check_type"] = "health"
            
        return MCPConversationalContext(
            mcp_intent=mcp_intent,
            connector_type=connector_type,
            operation_params=operation_params,
            natural_language_query=parsed_intent.original_message,
            user_intent=parsed_intent,
            conversation_context=conversation_context,
            priority_level=5
        )
    
    async def _execute_mcp_operation(self, context: MCPConversationalContext) -> Dict[str, Any]:
        """Execute MCP operation based on conversational context"""
        
        try:
            if context.mcp_intent == ConversationalMCPIntent.QUERY_SNOWFLAKE_DATA:
                return await self._execute_snowflake_query(context)
                
            elif context.mcp_intent == ConversationalMCPIntent.SEND_RABBITMQ_MESSAGE:
                return await self._execute_rabbitmq_send(context)
                
            elif context.mcp_intent == ConversationalMCPIntent.CHECK_CONNECTOR_STATUS:
                return await self._execute_health_check(context)
                
            elif context.mcp_intent == ConversationalMCPIntent.MANAGE_MCP_REGISTRY:
                return await self._execute_registry_management(context)
                
            else:
                return {"success": False, "error": "Unsupported MCP operation"}
                
        except Exception as e:
            logger.error(f"Error executing MCP operation: {e}")
            return {"success": False, "error": str(e)}
    
    async def _execute_snowflake_query(self, context: MCPConversationalContext) -> Dict[str, Any]:
        """Execute Snowflake query operation"""
        if not self.snowflake_connector:
            return {"success": False, "error": "Snowflake connector not available"}
        
        try:
            # Connect to Snowflake
            await self.snowflake_connector.connect()
            
            # Execute query based on operation
            if "query" in context.operation_params:
                result = await self.snowflake_connector.execute_query(context.operation_params["query"])
            elif context.operation_params.get("operation") == "show_tables":
                result = await self.snowflake_connector.execute_query("SHOW TABLES")
            else:
                result = await self.snowflake_connector.execute_query("SELECT CURRENT_DATABASE(), CURRENT_SCHEMA()")
            
            return {
                "success": True,
                "operation": "snowflake_query",
                "result": result,
                "connector": "snowflake"
            }
            
        except Exception as e:
            return {"success": False, "error": f"Snowflake query failed: {str(e)}"}
    
    async def _execute_rabbitmq_send(self, context: MCPConversationalContext) -> Dict[str, Any]:
        """Execute RabbitMQ message send operation"""
        if not self.rabbitmq_connector:
            return {"success": False, "error": "RabbitMQ connector not available"}
        
        try:
            # Connect to RabbitMQ
            await self.rabbitmq_connector.connect()
            
            # Send message
            message = context.operation_params.get("message", "Test message from conversational interface")
            queue = context.operation_params.get("queue", "default")
            
            result = await self.rabbitmq_connector.publish_message(
                message=message,
                queue_name=queue,
                routing_key=queue
            )
            
            return {
                "success": True,
                "operation": "rabbitmq_send",
                "result": result,
                "connector": "rabbitmq"
            }
            
        except Exception as e:
            return {"success": False, "error": f"RabbitMQ send failed: {str(e)}"}
    
    async def _execute_health_check(self, context: MCPConversationalContext) -> Dict[str, Any]:
        """Execute health check operation"""
        try:
            # Check all registered connectors
            registry_status = await self.mcp_registry.get_registry_status()
            
            health_results = {}
            for connector_name, connector in self.mcp_registry._connectors.items():
                try:
                    health_check = await connector.health_check()
                    health_results[connector_name] = {
                        "status": "healthy" if health_check.is_healthy else "unhealthy",
                        "response_time": health_check.response_time,
                        "details": health_check.details
                    }
                except Exception as e:
                    health_results[connector_name] = {
                        "status": "error",
                        "error": str(e)
                    }
            
            return {
                "success": True,
                "operation": "health_check",
                "registry_status": registry_status.__dict__,
                "connector_health": health_results
            }
            
        except Exception as e:
            return {"success": False, "error": f"Health check failed: {str(e)}"}
    
    async def _execute_registry_management(self, context: MCPConversationalContext) -> Dict[str, Any]:
        """Execute registry management operation"""
        try:
            # List all connectors
            connectors = await self.mcp_registry.list_connectors()
            
            return {
                "success": True,
                "operation": "registry_management",
                "connectors": [conn.__dict__ for conn in connectors]
            }
            
        except Exception as e:
            return {"success": False, "error": f"Registry management failed: {str(e)}"}
    
    async def _generate_mcp_response(
        self, 
        context: MCPConversationalContext, 
        mcp_result: Dict[str, Any]
    ) -> GeneratedResponse:
        """Generate natural language response cho MCP operation results"""
        
        # Create response context
        response_context = ResponseContext(
            intent=context.user_intent,
            conversation_context=context.conversation_context,
            action_results=[mcp_result],
            suggestions=[],
            ml_insights={"mcp_operation": context.mcp_intent.value}
        )
        
        # Generate response
        return await self.response_generator.generate_natural_language_response(response_context)
    
    async def _generate_follow_up_suggestions(
        self, 
        context: MCPConversationalContext, 
        mcp_result: Dict[str, Any]
    ) -> List[str]:
        """Generate follow-up suggestions based on MCP operation results"""
        
        suggestions = []
        
        if context.mcp_intent == ConversationalMCPIntent.QUERY_SNOWFLAKE_DATA:
            suggestions.extend([
                "Truy vấn dữ liệu khác",
                "Phân tích kết quả",
                "Xuất dữ liệu ra file"
            ])
        elif context.mcp_intent == ConversationalMCPIntent.SEND_RABBITMQ_MESSAGE:
            suggestions.extend([
                "Gửi tin nhắn khác",
                "Kiểm tra trạng thái queue",
                "Xem message history"
            ])
        elif context.mcp_intent == ConversationalMCPIntent.CHECK_CONNECTOR_STATUS:
            suggestions.extend([
                "Kiểm tra connector khác",
                "Xem performance metrics",
                "Troubleshoot issues"
            ])
        
        return suggestions
    
    async def handle_voice_activated_mcp(self, voice_input: str) -> MCPConversationalResult:
        """
        Handle voice-activated MCP operations
        Theo AGE design: Voice-Activated Infrastructure
        """
        # Convert voice to text (placeholder - would integrate with speech recognition)
        text_input = voice_input  # In production, this would be speech-to-text
        
        # Create dummy conversation context for voice
        voice_context = ConversationContext(
            user_id="voice_user",
            session_id=f"voice_session_{datetime.now().timestamp()}",
            conversation_history=[],
            user_preferences={"language": "vi", "voice_enabled": True},
            context_metadata={"input_type": "voice"}
        )
        
        # Process as normal conversational MCP request
        result = await self.process_conversational_mcp_request(text_input, voice_context)
        
        # Add voice-specific metadata
        result.natural_response.metadata["voice_response"] = True
        result.natural_response.metadata["speech_synthesis_ready"] = True
        
        return result
    
    async def get_mcp_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics cho MCP conversational operations"""
        try:
            # Get registry metrics
            registry_status = await self.mcp_registry.get_registry_status()
            
            # Get cache metrics
            cache_stats = await self.production_cache.get_statistics()
            
            return {
                "registry_metrics": registry_status.__dict__,
                "cache_metrics": cache_stats,
                "active_connectors": len(self.mcp_registry._connectors),
                "supported_operations": len(ConversationalMCPIntent),
                "voice_enabled": True
            }
            
        except Exception as e:
            logger.error(f"Error getting MCP performance metrics: {e}")
            return {"error": str(e)} 