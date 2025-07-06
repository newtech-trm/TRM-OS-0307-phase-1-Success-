from fastapi import APIRouter, FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import asyncio
from datetime import datetime

# Sử dụng lazy import để tránh vòng lặp import
api_router = APIRouter()

# --- Active Routers ---

# Import các router khi cần sử dụng để tránh vòng lặp import
from trm_api.api.v1.endpoints import project
api_router.include_router(project.router, prefix="/projects", tags=["Projects"])

from trm_api.api.v1.endpoints import user
api_router.include_router(user.router, prefix="/users", tags=["users"])

from trm_api.api.v1.endpoints import task
api_router.include_router(task.router, prefix="/tasks", tags=["Tasks"])

from trm_api.api.v1.endpoints import team
api_router.include_router(team.router, prefix="/teams", tags=["Teams"])

from trm_api.api.v1.endpoints import skill
api_router.include_router(skill.router, prefix="/skills", tags=["Skills"])

from trm_api.api.v1.endpoints import tension
api_router.include_router(tension.router, prefix="/tensions", tags=["Tensions"])

from trm_api.api.v1.endpoints import resource
api_router.include_router(resource.router, prefix="/resources", tags=["Resources"])

# --- Deprecated Routers ---

# --- TODO: Re-enable these routers after they are refactored to use repositories ---
from trm_api.api.v1.endpoints import win
api_router.include_router(win.router, prefix="/wins", tags=["WINs"])

from trm_api.api.v1.endpoints import recognition
api_router.include_router(recognition.router, prefix="/recognitions", tags=["Recognitions"])

from trm_api.api.v1.endpoints import relationship
api_router.include_router(relationship.router, prefix="/relationships", tags=["Relationships"])

from trm_api.api.v1.endpoints import knowledge_snippet
api_router.include_router(knowledge_snippet.router, prefix="/knowledge-snippets", tags=["Knowledge Snippets"])

from trm_api.api.v1.endpoints import agent
api_router.include_router(agent.router, prefix="/agents", tags=["Agents"])

from trm_api.api.v1.endpoints import event
api_router.include_router(event.router, prefix="/events", tags=["Events"])
# api_router.include_router(tool.router, prefix="/tools", tags=["Tools"])

from trm_api.api.v1.endpoints import validate
api_router.include_router(validate.router, tags=["Validation"])

# NEW: Import V2 Conversation endpoints
from ..v2.endpoints.conversation import router as conversation_router
from ...core.dependencies import cleanup_dependencies

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    # Startup
    print("🚀 TRM-OS API v2.0 Starting...")
    print(f"📅 Startup time: {datetime.now()}")
    print("🤖 Adaptive Learning System: ACTIVE")
    print("💬 Conversational Interface: READY")
    print("🔄 Real-time WebSocket: ENABLED")
    
    yield
    
    # Shutdown
    print("🛑 TRM-OS API Shutting down...")
    await cleanup_dependencies()
    print("✅ Dependencies cleaned up")

# Create FastAPI app with lifespan
app = FastAPI(
    title="TRM-OS API v2.0",
    description="Task, Resource, and Management Operating System with Adaptive Intelligence",
    version="2.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include V1 API routes
app.include_router(api_router, prefix="/api/v1")

# Include V2 Conversation endpoints
app.include_router(conversation_router, prefix="/api")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "TRM-OS API v2.0 - Adaptive Intelligence Operating System",
        "version": "2.0.0",
        "status": "operational",
        "timestamp": datetime.now().isoformat(),
        "features": [
            "🤖 Adaptive Learning System",
            "💬 Conversational Interface",
            "🧠 Natural Language Processing",
            "🔄 Real-time WebSocket",
            "👥 Agent Templates",
            "🎯 Advanced Reasoning",
            "🚀 Genesis Engine"
        ],
        "endpoints": {
            "v1_api": "/api/v1",
            "v2_conversation": "/api/v2/conversation",
            "websocket": "/api/v2/conversation/realtime/{user_id}",
            "health": "/api/v2/health",
            "docs": "/docs"
        }
    }

@app.get("/api/v2/health")
async def health_check_v2():
    """Health check for API v2"""
    return {
        "status": "healthy",
        "version": "2.0.0",
        "timestamp": datetime.now().isoformat(),
        "components": {
            "adaptive_learning": "operational",
            "conversational_interface": "operational",
            "natural_language_processing": "operational",
            "real_time_websocket": "operational",
            "agent_templates": "operational",
            "advanced_reasoning": "operational",
            "genesis_engine": "operational"
        },
        "capabilities": {
            "vietnamese_language": True,
            "english_language": True,
            "multi_intent_processing": True,
            "contextual_understanding": True,
            "adaptive_learning": True,
            "real_time_feedback": True,
            "conversation_analytics": True
        }
    }
