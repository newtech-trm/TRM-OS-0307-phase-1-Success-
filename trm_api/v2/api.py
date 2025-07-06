#!/usr/bin/env python3
"""
TRM API v2 - Main Integration
============================

Integration point cho TRM-OS v2 Conversational Intelligence
với existing v1 API infrastructure.
"""

from fastapi import APIRouter
from trm_api.v2.endpoints.conversation import router as conversation_router

# Create main v2 router
v2_router = APIRouter(prefix="/v2", tags=["TRM-OS v2 - Conversational Intelligence"])

# Include all v2 endpoints
v2_router.include_router(conversation_router)

# Health check cho v2 API
@v2_router.get("/health")
async def v2_health_check():
    """Health check cho TRM-OS v2 API"""
    return {
        "status": "healthy",
        "version": "2.0.0",
        "service": "TRM-OS Conversational Intelligence",
        "features": [
            "Natural Language Processing (Vietnamese/English)",
            "Conversation Session Management", 
            "Real-time WebSocket Chat",
            "Context-aware Response Generation",
            "Agent Integration"
        ]
    } 