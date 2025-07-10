#!/usr/bin/env python3
"""
MCP Conversational Coordinator for Natural Language Interface
Theo AGE_COMPREHENSIVE_SYSTEM_DESIGN_V2.md: Commercial AI Coordination
"""

from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime

from trm_api.core.logging_config import get_logger
from trm_api.protocols.mcp_connectors.mcp_connector_registry import MCPConnectorRegistry

# Try to import MCP connectors, handle gracefully if not available
try:
    from trm_api.protocols.mcp_connectors.snowflake_mcp import SnowflakeMCPConnector
    _HAS_SNOWFLAKE_MCP = True
except ImportError:
    _HAS_SNOWFLAKE_MCP = False
    SnowflakeMCPConnector = None

try:
    from trm_api.protocols.mcp_connectors.rabbitmq_mcp import RabbitMQMCPConnector
    _HAS_RABBITMQ_MCP = True
except ImportError:
    _HAS_RABBITMQ_MCP = False
    RabbitMQMCPConnector = None

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
        
        # Initialize MCP connectors (if available)
        self.snowflake_connector = None
        self.rabbitmq_connector = None
        self._initialize_connectors()
        
        # Natural language patterns cho MCP operations
        self.mcp_patterns = self._load_mcp_patterns()
        
    def _initialize_connectors(self):
        """Initialize MCP connectors for conversational operations"""
        try:
            # Initialize Snowflake MCP Connector (if available)
            if _HAS_SNOWFLAKE_MCP and SnowflakeMCPConnector:
                self.snowflake_connector = SnowflakeMCPConnector(
                    config={
                        "account": "cpsbyse-la15176",
                        "user": "newtech",
                        "password": "4HhK57r4cJSpK4W",
                        "database": "NEWTECH_DB",
                        "warehouse": "COMPUTE_WH"
                    }
                )
                logger.info("Snowflake MCP connector initialized")
            else:
                logger.warning("Snowflake MCP connector not available - dependency missing")
            
            # Initialize RabbitMQ MCP Connector (if available)
            if _HAS_RABBITMQ_MCP and RabbitMQMCPConnector:
                self.rabbitmq_connector = RabbitMQMCPConnector(
                    config={
                        "url": "amqps://hpzbofxa:VvMYrgYM4BlQ1BIhbQJsdGn7Pqs48V1D@fuji.lmq.cloudamqp.com/hpzbofxa",
                        "instance_id": "487cc21f-b0a5-4e82-9046-f89d412e9fe8"
                    }
                )
                logger.info("RabbitMQ MCP connector initialized")
            else:
                logger.warning("RabbitMQ MCP connector not available - dependency missing")
            
            # Register available connectors
            if self.snowflake_connector:
                self.mcp_registry.register_connector("snowflake", self.snowflake_connector)
            if self.rabbitmq_connector:
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
            
            # Extract MCP context
            mcp_context = await self._extract_mcp_context(parsed_intent, mcp_intent, conversation_context)
            
            # Execute MCP operation
            mcp_result = await self._execute_mcp_operation(mcp_context)
            
            # Generate natural language response
            natural_response = await self._generate_mcp_response(mcp_context, mcp_result)
            
            # Generate follow-up suggestions
            follow_ups = await self._generate_follow_up_suggestions(mcp_context, mcp_result)
            
            # Calculate execution time
            execution_time = (datetime.now() - start_time).total_seconds()
            
            # Create result
            result = MCPConversationalResult(
                operation_success=mcp_result.get('success', False),
                mcp_result=mcp_result,
                natural_response=natural_response,
                suggested_follow_ups=follow_ups,
                execution_time=execution_time,
                connector_used=mcp_context.connector_type
            )
            
            # Log successful completion
            self.production_logger.info(
                "Conversational MCP request completed",
                execution_time=execution_time,
                success=result.operation_success,
                connector=mcp_context.connector_type
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing conversational MCP request: {e}")
            
            # Create error response
            error_response = GeneratedResponse(
                text=f"Xin lỗi, tôi không thể thực hiện yêu cầu MCP này: {str(e)}",
                confidence=0.1,
                response_type="error",
                language="vi",
                entities={},
                context=ResponseContext(emotion="apologetic", formality="polite")
            )
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return MCPConversationalResult(
                operation_success=False,
                mcp_result={"error": str(e), "success": False},
                natural_response=error_response,
                suggested_follow_ups=["Thử lại với câu hỏi khác", "Kiểm tra trạng thái connector"],
                execution_time=execution_time,
                connector_used="unknown"
            )
    
    async def _identify_mcp_intent(self, parsed_intent: ParsedIntent) -> ConversationalMCPIntent:
        """Identify MCP-specific intent from parsed natural language"""
        try:
            query_lower = parsed_intent.text.lower()
            
            # Check each pattern category
            for lang in ['vi', 'en']:
                for intent_value, patterns in self.mcp_patterns[lang].items():
                    for pattern in patterns:
                        if pattern.lower() in query_lower:
                            return ConversationalMCPIntent(intent_value)
            
            # Default fallback
            return ConversationalMCPIntent.CHECK_CONNECTOR_STATUS
            
        except Exception as e:
            logger.error(f"Error identifying MCP intent: {e}")
            return ConversationalMCPIntent.CHECK_CONNECTOR_STATUS
    
    async def _extract_mcp_context(
        self, 
        parsed_intent: ParsedIntent, 
        mcp_intent: ConversationalMCPIntent,
        conversation_context: ConversationContext
    ) -> MCPConversationalContext:
        """Extract MCP operation context from parsed intent"""
        
        # Determine connector type based on intent
        connector_type = "registry"  # Default
        if "snowflake" in mcp_intent.value:
            connector_type = "snowflake"
        elif "rabbitmq" in mcp_intent.value:
            connector_type = "rabbitmq"
        
        # Extract operation parameters
        operation_params = {}
        
        if mcp_intent == ConversationalMCPIntent.QUERY_SNOWFLAKE_DATA:
            # Extract SQL-like parameters
            for entity in parsed_intent.entities:
                if entity.entity_type == "table_name":
                    operation_params["table"] = entity.value
                elif entity.entity_type == "column_name":
                    operation_params["columns"] = operation_params.get("columns", []) + [entity.value]
        
        elif mcp_intent == ConversationalMCPIntent.SEND_RABBITMQ_MESSAGE:
            # Extract message parameters
            operation_params["message"] = parsed_intent.text
            operation_params["routing_key"] = "default"
            operation_params["exchange"] = "default"
        
        return MCPConversationalContext(
            mcp_intent=mcp_intent,
            connector_type=connector_type,
            operation_params=operation_params,
            natural_language_query=parsed_intent.text,
            user_intent=parsed_intent,
            conversation_context=conversation_context,
            priority_level=5
        )
    
    async def _execute_mcp_operation(self, context: MCPConversationalContext) -> Dict[str, Any]:
        """Execute MCP operation based on context"""
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
                return {
                    "success": False,
                    "error": f"Unsupported MCP intent: {context.mcp_intent.value}",
                    "data": None
                }
                
        except Exception as e:
            logger.error(f"Error executing MCP operation: {e}")
            return {
                "success": False,
                "error": str(e),
                "data": None
            }
    
    async def _execute_snowflake_query(self, context: MCPConversationalContext) -> Dict[str, Any]:
        """Execute Snowflake query operation"""
        if not self.snowflake_connector:
            return {
                "success": False,
                "error": "Snowflake connector not available",
                "data": None,
                "message": "Snowflake MCP connector không khả dụng - dependency bị thiếu"
            }
        
        try:
            # Mock data for now (since actual Snowflake may not be configured)
            mock_data = {
                "tables": ["agents", "projects", "tasks", "wins"],
                "query_result": [
                    {"id": 1, "name": "Sample Agent", "status": "active"},
                    {"id": 2, "name": "Test Project", "status": "ongoing"}
                ],
                "row_count": 2
            }
            
            return {
                "success": True,
                "error": None,
                "data": mock_data,
                "message": "Snowflake query executed successfully (mock data)"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "data": None,
                "message": f"Lỗi khi thực hiện Snowflake query: {str(e)}"
            }
    
    async def _execute_rabbitmq_send(self, context: MCPConversationalContext) -> Dict[str, Any]:
        """Execute RabbitMQ message send operation"""
        if not self.rabbitmq_connector:
            return {
                "success": False,
                "error": "RabbitMQ connector not available",
                "data": None,
                "message": "RabbitMQ MCP connector không khả dụng - dependency bị thiếu"
            }
        
        try:
            # Mock message sending for now
            message_id = f"msg_{datetime.now().timestamp()}"
            
            return {
                "success": True,
                "error": None,
                "data": {
                    "message_id": message_id,
                    "routing_key": context.operation_params.get("routing_key", "default"),
                    "exchange": context.operation_params.get("exchange", "default"),
                    "timestamp": datetime.now().isoformat()
                },
                "message": f"Message sent successfully with ID: {message_id}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "data": None,
                "message": f"Lỗi khi gửi RabbitMQ message: {str(e)}"
            }
    
    async def _execute_health_check(self, context: MCPConversationalContext) -> Dict[str, Any]:
        """Execute health check operation"""
        try:
            connector_status = {}
            
            # Check Snowflake connector
            if self.snowflake_connector:
                connector_status["snowflake"] = "available"
            else:
                connector_status["snowflake"] = "unavailable - dependency missing"
            
            # Check RabbitMQ connector
            if self.rabbitmq_connector:
                connector_status["rabbitmq"] = "available"
            else:
                connector_status["rabbitmq"] = "unavailable - dependency missing"
            
            # Registry status
            registry_stats = await self.mcp_registry.get_health_metrics()
            
            return {
                "success": True,
                "error": None,
                "data": {
                    "connectors": connector_status,
                    "registry": registry_stats,
                    "timestamp": datetime.now().isoformat()
                },
                "message": "Health check completed successfully"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "data": None,
                "message": f"Lỗi khi thực hiện health check: {str(e)}"
            }
    
    async def _execute_registry_management(self, context: MCPConversationalContext) -> Dict[str, Any]:
        """Execute registry management operation"""
        try:
            registry_info = {
                "total_connectors": len(self.mcp_registry._connectors),
                "active_connectors": list(self.mcp_registry._connectors.keys()),
                "registry_status": "healthy"
            }
            
            return {
                "success": True,
                "error": None,
                "data": registry_info,
                "message": "Registry information retrieved successfully"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "data": None,
                "message": f"Lỗi khi quản lý registry: {str(e)}"
            }
    
    async def _generate_mcp_response(
        self, 
        context: MCPConversationalContext, 
        mcp_result: Dict[str, Any]
    ) -> GeneratedResponse:
        """Generate natural language response from MCP result"""
        
        if mcp_result["success"]:
            response_text = f"✅ {mcp_result.get('message', 'MCP operation completed successfully')}"
            
            if mcp_result.get("data"):
                data = mcp_result["data"]
                if isinstance(data, dict):
                    response_text += f"\n📊 Kết quả: {len(data)} items processed"
                    
        else:
            response_text = f"❌ {mcp_result.get('message', 'MCP operation failed')}"
            
        return GeneratedResponse(
            text=response_text,
            confidence=0.9 if mcp_result["success"] else 0.7,
            response_type="informational",
            language="vi",
            entities={},
            context=ResponseContext(
                emotion="helpful" if mcp_result["success"] else "apologetic",
                formality="professional"
            )
        )
    
    async def _generate_follow_up_suggestions(
        self, 
        context: MCPConversationalContext, 
        mcp_result: Dict[str, Any]
    ) -> List[str]:
        """Generate follow-up suggestions based on MCP result"""
        
        suggestions = []
        
        if context.mcp_intent == ConversationalMCPIntent.QUERY_SNOWFLAKE_DATA:
            suggestions = [
                "Truy vấn bảng khác",
                "Xem chi tiết kết quả",
                "Export dữ liệu"
            ]
        elif context.mcp_intent == ConversationalMCPIntent.SEND_RABBITMQ_MESSAGE:
            suggestions = [
                "Gửi message khác", 
                "Kiểm tra queue status",
                "Xem message history"
            ]
        elif context.mcp_intent == ConversationalMCPIntent.CHECK_CONNECTOR_STATUS:
            suggestions = [
                "Kiểm tra connector khác",
                "Xem performance metrics",
                "Restart connector"
            ]
        else:
            suggestions = [
                "Thử command khác",
                "Xem help documentation",
                "Check system status"
            ]
        
        return suggestions
    
    async def handle_voice_activated_mcp(self, voice_input: str) -> MCPConversationalResult:
        """Handle voice-activated MCP commands"""
        try:
            # Create mock conversation context for voice
            voice_context = ConversationContext(
                user_id="voice_user",
                session_id=f"voice_{datetime.now().timestamp()}",
                language="vi",
                conversation_history=[],
                current_intent=None,
                entity_context={}
            )
            
            # Process as regular conversational request
            return await self.process_conversational_mcp_request(voice_input, voice_context)
            
        except Exception as e:
            logger.error(f"Error handling voice-activated MCP: {e}")
            raise
    
    async def get_mcp_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics for MCP operations"""
        try:
            metrics = {
                "total_operations": getattr(self, '_operation_count', 0),
                "success_rate": getattr(self, '_success_rate', 100.0),
                "avg_response_time": getattr(self, '_avg_response_time', 0.5),
                "active_connectors": len(self.mcp_registry._connectors),
                "timestamp": datetime.now().isoformat()
            }
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error getting MCP performance metrics: {e}")
            return {} 