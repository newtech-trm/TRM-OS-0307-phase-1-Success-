#!/usr/bin/env python3
"""
TRM API v2 - Main Integration
============================

Integration point cho TRM-OS v2 Conversational Intelligence
với existing v1 API infrastructure.
"""

from fastapi import APIRouter
from trm_api.v2.endpoints.conversation import router as conversation_router
from trm_api.v2.endpoints.websocket_realtime import router as websocket_router

# Try to import MCP Conversational endpoints, handle gracefully if dependencies missing
try:
    from trm_api.v2.endpoints import mcp_conversational
    _HAS_MCP_CONVERSATIONAL = True
except ImportError as e:
    _HAS_MCP_CONVERSATIONAL = False
    mcp_conversational = None
    print(f"Warning: MCP Conversational endpoints not available: {e}")

# Create main v2 router
v2_router = APIRouter(prefix="/v2", tags=["TRM-OS v2 - Conversational Intelligence"])

# Include all v2 endpoints
v2_router.include_router(conversation_router)
v2_router.include_router(websocket_router)

# Include MCP Conversational router if available
if _HAS_MCP_CONVERSATIONAL and mcp_conversational:
    v2_router.include_router(mcp_conversational.router)
    print("✅ MCP Conversational endpoints loaded successfully")
else:
    print("⚠️  MCP Conversational endpoints disabled - dependencies missing")

# Health check cho v2 API
@v2_router.get("/health")
async def v2_health_check():
    """Health check cho TRM-OS v2 API"""
    features = [
        "Natural Language Processing (Vietnamese/English)",
        "Conversation Session Management", 
        "Real-time WebSocket Chat",
        "Context-aware Response Generation",
        "Agent Integration",
        "Commercial AI Coordination Real-time Communication"
    ]
    
    # Add MCP status
    if _HAS_MCP_CONVERSATIONAL:
        features.append("MCP Conversational Interface (Available)")
    else:
        features.append("MCP Conversational Interface (Dependencies Missing)")
    
    return {
        "status": "healthy",
        "version": "2.0.0",
        "service": "TRM-OS Conversational Intelligence",
        "features": features,
        "mcp_available": _HAS_MCP_CONVERSATIONAL
    } 