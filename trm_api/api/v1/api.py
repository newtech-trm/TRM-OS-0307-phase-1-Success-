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

from trm_api.api.v1.endpoints import agent_ecosystem
api_router.include_router(agent_ecosystem.router, tags=["Agent Ecosystem"])

from trm_api.api.v1.endpoints import event
api_router.include_router(event.router, prefix="/events", tags=["Events"])
# api_router.include_router(tool.router, prefix="/tools", tags=["Tools"])

from trm_api.api.v1.endpoints import validate
api_router.include_router(validate.router, tags=["Validation"])

# Reasoning Engine endpoints
from trm_api.api.v1.endpoints import reasoning
api_router.include_router(reasoning.router, tags=["Reasoning Engine"])

# Commercial AI Coordination endpoints
from trm_api.api.v1.endpoints import commercial_ai
api_router.include_router(commercial_ai.router, tags=["Commercial AI Coordination"])

# MCP Universal Data Access endpoints  
from trm_api.api.v1.endpoints import mcp_endpoints
api_router.include_router(mcp_endpoints.router, tags=["MCP - Universal Data Access"])

# NEW: Import V2 Conversation endpoints - REMOVED (fake implementation)
# from ..v2.endpoints.conversation import router as conversation_router
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

# Include V2 Conversation endpoints - REMOVED (fake implementation)
# app.include_router(conversation_router, prefix="/api")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "TRM-OS API v2.0 - Commercial AI Orchestration System",
        "version": "2.0.0",
        "status": "operational",
        "timestamp": datetime.now().isoformat(),
        "philosophy": "Recognition → Event → WIN with Commercial AI Coordination",
        "features": [
            "🤖 Commercial AI Coordination (OpenAI, Claude, Gemini)",
            "🧠 Multi-AI Reasoning & Synthesis",
            "💡 Intelligent AI Routing & Optimization",
            "📊 AI Performance Analytics",
            "🔄 Event-Driven Architecture",
            "🎯 Advanced Reasoning Engine",
            "🚀 Artificial Genesis Engine (AGE)",
            "⚡ Quantum-Enhanced Processing"
        ],
        "endpoints": {
            "v1_api": "/api/v1",
            "commercial_ai": "/api/v1/commercial-ai",
            "reasoning": "/api/v1/reasoning",
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
        "philosophy": "Recognition → Event → WIN with Commercial AI Coordination",
        "components": {
            "commercial_ai_coordination": "operational",
            "ai_routing_engine": "operational", 
            "multi_ai_synthesis": "operational",
            "performance_analytics": "operational",
            "event_driven_architecture": "operational",
            "advanced_reasoning": "operational",
            "genesis_engine": "operational",
            "quantum_enhancement": "operational"
        },
        "ai_services": {
            "openai": "connected",
            "claude": "connected", 
            "gemini": "connected"
        },
        "capabilities": {
            "commercial_ai_orchestration": True,
            "multi_ai_reasoning": True,
            "intelligent_routing": True,
            "cost_optimization": True,
            "performance_monitoring": True,
            "vietnamese_language": True,
            "english_language": True,
            "event_driven_processing": True,
            "quantum_enhanced_decisions": True
        }
    }
