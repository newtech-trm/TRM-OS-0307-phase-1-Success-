#!/usr/bin/env python3
"""
MCP Conversational API Endpoints for TRM-OS v2.2
===============================================

API endpoints cho Natural Language MCP Operations
theo AGE_COMPREHENSIVE_SYSTEM_DESIGN_V2.md
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from datetime import datetime

from trm_api.core.logging_config import get_logger
from trm_api.v2.conversation.mcp_conversational_coordinator import (
    MCPConversationalCoordinator,
    MCPConversationalResult,
    ConversationalMCPIntent
)
from trm_api.v2.conversation.session_manager import ConversationContext

logger = get_logger(__name__)

# Initialize router
router = APIRouter(prefix="/api/v2/mcp/conversational", tags=["MCP Conversational"])

# Initialize coordinator
mcp_coordinator = MCPConversationalCoordinator()


class MCPConversationalRequest(BaseModel):
    """Request cho conversational MCP operations"""
    message: str = Field(..., description="Natural language message từ user")
    user_id: str = Field(..., description="User ID")
    session_id: Optional[str] = Field(None, description="Conversation session ID")
    language: Optional[str] = Field("vi", description="Language preference (vi/en)")
    voice_input: Optional[bool] = Field(False, description="Is this voice input?")


class MCPConversationalResponse(BaseModel):
    """Response cho conversational MCP operations"""
    success: bool
    operation_result: Dict[str, Any]
    natural_response: str
    response_metadata: Dict[str, Any]
    suggested_follow_ups: List[str]
    execution_time: float
    connector_used: str


class MCPHealthCheckResponse(BaseModel):
    """Response cho MCP health check"""
    registry_status: Dict[str, Any]
    connector_health: Dict[str, Any]
    performance_metrics: Dict[str, Any]


@router.post("/process", response_model=MCPConversationalResponse)
async def process_conversational_mcp_request(request: MCPConversationalRequest):
    """
    Process natural language MCP request
    
    Examples:
    - "Kết nối tới Snowflake và lấy danh sách tables"
    - "Gửi tin nhắn 'Hello World' qua RabbitMQ"
    - "Kiểm tra trạng thái tất cả connectors"
    """
    try:
        # Create conversation context
        conversation_context = ConversationContext(
            user_id=request.user_id,
            session_id=request.session_id or f"session_{datetime.now().timestamp()}",
            conversation_history=[],
            user_preferences={"language": request.language},
            context_metadata={"api_request": True}
        )
        
        # Process MCP request
        if request.voice_input:
            result = await mcp_coordinator.handle_voice_activated_mcp(request.message)
        else:
            result = await mcp_coordinator.process_conversational_mcp_request(
                request.message, 
                conversation_context
            )
        
        return MCPConversationalResponse(
            success=result.operation_success,
            operation_result=result.mcp_result,
            natural_response=result.natural_response.text,
            response_metadata=result.natural_response.metadata,
            suggested_follow_ups=result.suggested_follow_ups,
            execution_time=result.execution_time,
            connector_used=result.connector_used
        )
        
    except Exception as e:
        logger.error(f"Error processing conversational MCP request: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health", response_model=MCPHealthCheckResponse)
async def get_mcp_health_status():
    """
    Get comprehensive health status của MCP conversational system
    """
    try:
        # Get performance metrics
        metrics = await mcp_coordinator.get_mcp_performance_metrics()
        
        return MCPHealthCheckResponse(
            registry_status=metrics.get("registry_metrics", {}),
            connector_health=metrics.get("connector_health", {}),
            performance_metrics=metrics.get("cache_metrics", {})
        )
        
    except Exception as e:
        logger.error(f"Error getting MCP health status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/voice")
async def handle_voice_mcp_request(request: MCPConversationalRequest):
    """
    Handle voice-activated MCP operations
    Theo AGE design: Voice-Activated Infrastructure
    """
    try:
        # Process voice input
        result = await mcp_coordinator.handle_voice_activated_mcp(request.message)
        
        return {
            "success": result.operation_success,
            "natural_response": result.natural_response.text,
            "voice_response_ready": True,
            "speech_synthesis_text": result.natural_response.text,
            "execution_time": result.execution_time
        }
        
    except Exception as e:
        logger.error(f"Error handling voice MCP request: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/examples")
async def get_mcp_conversational_examples():
    """
    Get examples của conversational MCP operations
    """
    return {
        "vietnamese_examples": [
            "Kết nối tới Snowflake và show tables",
            "Truy vấn dữ liệu: SELECT * FROM users LIMIT 10",
            "Gửi tin nhắn 'System started' qua RabbitMQ",
            "Kiểm tra trạng thái tất cả connectors",
            "Lấy danh sách connectors đang hoạt động"
        ],
        "english_examples": [
            "Connect to Snowflake and show tables",
            "Query data: SELECT * FROM products WHERE price > 100",
            "Send message 'Order processed' via RabbitMQ",
            "Check status of all connectors",
            "Get list of active connectors"
        ],
        "voice_examples": [
            "Kết nối Snowflake",
            "Gửi tin nhắn test",
            "Kiểm tra trạng thái hệ thống"
        ]
    }


@router.get("/supported-operations")
async def get_supported_mcp_operations():
    """
    Get list of supported MCP operations
    """
    return {
        "conversational_intents": [intent.value for intent in ConversationalMCPIntent],
        "supported_connectors": ["snowflake", "rabbitmq"],
        "languages": ["vi", "en"],
        "voice_enabled": True,
        "features": [
            "Natural Language MCP Operations",
            "Voice-Activated Infrastructure",
            "Commercial AI Coordination",
            "Real-time Health Monitoring",
            "Intelligent Troubleshooting"
        ]
    } 