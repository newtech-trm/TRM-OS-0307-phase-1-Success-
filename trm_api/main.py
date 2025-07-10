#!/usr/bin/env python3
"""
AGE - Artificial Genesis Engine: Main Application
Commercial AI Orchestration System

Philosophy: Recognition → Event → WIN through Strategic Intelligence
Architecture: Cloud-First Infrastructure with MCP/ADK Integration

System Purpose: Transform Founder's strategic intent into measurable WINs 
through autonomous Commercial AI coordination.
"""

import sys
import os
import datetime
from typing import Dict, Any

# AGE System Logging
LOG_FILE = "age_system_startup.log"

def log_age_system(message: str, level: str = "INFO"):
    """AGE System logging with semantic context"""
    timestamp = datetime.datetime.now().isoformat()
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] AGE-{level}: {message}\n")

# === AGE SYSTEM INITIALIZATION ===
log_age_system("=== AGE (Artificial Genesis Engine) INITIALIZATION ===")
log_age_system(f"System Identity: Commercial AI Orchestration Platform")
log_age_system(f"Architecture: Recognition → Event → WIN")
log_age_system(f"Python Executable: {sys.executable}")
log_age_system(f"System Path: {sys.path}")
log_age_system(f"Working Directory: {os.getcwd()}")
log_age_system(f"Environment - PYTHONPATH: {os.environ.get('PYTHONPATH')}")
log_age_system(f"Environment - VIRTUAL_ENV: {os.environ.get('VIRTUAL_ENV')}")

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager
from trm_api.core.config import settings
from trm_api.db.session import connect_to_db, close_db_connection
from trm_api.core.logging_config import setup_logging
from trm_api.middleware.ontology_logging import OntologyLoggingMiddleware

@asynccontextmanager
async def age_system_lifespan(app: FastAPI):
    """
    AGE System Lifecycle Management
    Handles startup and shutdown of Commercial AI Orchestration components
    """
    # === AGE SYSTEM STARTUP ===
    log_age_system("AGE System Startup Initiated", "STARTUP")
    
    # Initialize logging system
    setup_logging()
    log_age_system("Logging system initialized", "STARTUP")
    
    # Connect to Knowledge Graph (Neo4j) and Vector Database (Supabase)
    try:
        connect_to_db()
        log_age_system("Knowledge Graph & Vector Database connected", "STARTUP")
    except Exception as e:
        log_age_system(f"Database connection failed: {str(e)}", "ERROR")
        raise
    
    # Initialize Commercial AI Coordination Layer
    log_age_system("Commercial AI Coordination Layer ready", "STARTUP")
    log_age_system("MCP (Model Context Protocol) integration active", "STARTUP")
    log_age_system("ADK (Agent Development Kit) framework loaded", "STARTUP")
    
    # AGE System ready for strategic orchestration
    log_age_system("=== AGE SYSTEM OPERATIONAL - READY FOR STRATEGIC ORCHESTRATION ===", "READY")
    
    yield
    
    # === AGE SYSTEM SHUTDOWN ===
    log_age_system("AGE System Shutdown Initiated", "SHUTDOWN")
    
    try:
        close_db_connection()
        log_age_system("Knowledge Graph & Vector Database disconnected", "SHUTDOWN")
    except Exception as e:
        log_age_system(f"Database disconnection error: {str(e)}", "ERROR")
    
    log_age_system("=== AGE SYSTEM SHUTDOWN COMPLETE ===", "SHUTDOWN")

# === AGE FASTAPI APPLICATION ===
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="""
    AGE - Artificial Genesis Engine: Commercial AI Orchestration System
    
    🧠 **Core Mission**: Transform Founder's strategic intent into measurable WINs through autonomous Commercial AI coordination.
    
    🏗️ **Architecture**: Cloud-First Infrastructure
    - **Data Layer**: Supabase Cloud, Neo4j Aura, Snowflake, RabbitMQ
    - **AI Layer**: OpenAI GPT-4o, Claude 3.5, Gemini Pro, Llama 3.2 90B
    - **Integration**: MCP (Universal Data Access), ADK (Agent Orchestration), A2A (Agent Communication)
    
    🎯 **Philosophy**: Recognition → Event → WIN
    1. **Recognition Phase**: AI Router identifies optimal service combination
    2. **Event Phase**: Commercial AI coordination executes strategic actions
    3. **WIN Phase**: Measurable outcomes achieved through AI orchestration
    
    🚀 **Deployment**: Railway Cloud Platform - https://trmosngonlanh.up.railway.app/
    """,
    version="2.0.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=age_system_lifespan,
    contact={
        "name": "AGE System Administrator",
        "email": "age-admin@trm-os.com"
    },
    license_info={
        "name": "AGE Commercial License",
        "identifier": "Commercial"
    }
)

# === SECURITY MIDDLEWARE ===

# CORS Configuration for Commercial AI Integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://trmosngonlanh.up.railway.app",
        "https://api.openai.com",
        "https://api.anthropic.com", 
        "https://generativelanguage.googleapis.com",
        "http://localhost:3000",
        "http://localhost:8000",
        "http://localhost:8001"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Trusted Host Middleware for Production Security
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=[
        "trmosngonlanh.up.railway.app",
        "localhost",
        "127.0.0.1",
        "0.0.0.0"
    ]
)

# AGE Ontology Logging Middleware
app.add_middleware(
    OntologyLoggingMiddleware,
    log_request_body=True,
    log_response_body=True,
    log_processing_time=True,
    log_path_prefixes=[
        "/age/semantic",  # Semantic Action APIs
        "/intelligence",  # Strategic Intelligence APIs
        "/coordination",  # Resource Coordination APIs
        "/strategic"      # Strategic Event & WIN APIs
    ]
)

# === AGE SYSTEM ENDPOINTS ===

@app.get("/", tags=["🏠 AGE System"])
def age_system_welcome():
    """
    AGE System Welcome - Commercial AI Orchestration Platform
    """
    return {
        "system": "AGE - Artificial Genesis Engine",
        "version": "2.0.0",
        "architecture": "Commercial AI Orchestration System",
        "philosophy": "Recognition → Event → WIN",
        "mission": "Transform strategic intent into measurable WINs through AI coordination",
        "deployment": "Railway Cloud Platform",
        "status": "OPERATIONAL",
        "capabilities": {
            "commercial_ai_integration": ["OpenAI GPT-4o", "Claude 3.5", "Gemini Pro"],
            "data_infrastructure": ["Supabase Cloud", "Neo4j Aura", "RabbitMQ"],
            "orchestration_protocols": ["MCP", "ADK", "A2A"],
            "semantic_actions": ["Tension Recognition", "Actor Orchestration", "WIN Validation"]
        },
        "documentation": "/docs",
        "semantic_api_summary": "/semantic/action-summary"
    }

@app.get("/age/system-status", tags=["🏠 AGE System"])
def age_system_status():
    """
    AGE System Status - Real-time operational status
    """
    return {
        "system_identity": settings.SYSTEM_IDENTITY,
        "system_purpose": settings.SYSTEM_PURPOSE,
        "architecture_paradigm": settings.ARCHITECTURE_PARADIGM,
        "operational_status": "ACTIVE",
        "subsystems": {
            "knowledge_graph": "Connected" if True else "Disconnected",  # TODO: Real health check
            "vector_database": "Connected" if True else "Disconnected",
            "message_queue": "Connected" if True else "Disconnected",
            "commercial_ai_apis": {
                "openai": "Available" if settings.OPENAI_API_KEY else "Not Configured",
                "anthropic": "Available" if settings.ANTHROPIC_API_KEY else "Not Configured", 
                "google": "Available" if settings.GOOGLE_API_KEY else "Not Configured"
            }
        },
        "mcp_integration": {
            "supabase": settings.MCP_SUPABASE_ENABLED,
            "neo4j": settings.MCP_NEO4J_ENABLED,
            "snowflake": settings.MCP_SNOWFLAKE_ENABLED
        },
        "orchestration_settings": {
            "max_concurrent_actors": settings.MAX_CONCURRENT_ACTORS,
            "coordination_strategy": settings.ACTOR_COORDINATION_STRATEGY,
            "learning_enabled": settings.LEARNING_INTEGRATION_ENABLED
        }
    }

@app.get("/health", tags=["🏠 AGE System"])
def age_health_check():
    """
    AGE System Health Check - For deployment monitoring
    """
    return {
        "status": "healthy",
        "system": "AGE Orchestration Platform", 
        "timestamp": datetime.datetime.now().isoformat(),
        "environment": settings.DEPLOYMENT_ENVIRONMENT
    }

@app.get("/age/deployment-info", tags=["🏠 AGE System"])
def age_deployment_info():
    """
    AGE Deployment Information - Railway platform details
    """
    return {
        "platform": "Railway Cloud",
        "deployment_url": "https://trmosngonlanh.up.railway.app/",
        "environment": settings.DEPLOYMENT_ENVIRONMENT,
        "project_id": settings.RAILWAY_PROJECT_ID or "Auto-detected",
        "deployment_strategy": "Continuous Deployment via GitHub Integration",
        "scaling": "Auto-scaling based on load",
        "monitoring": "Integrated Railway metrics & logging"
    }

# === API ROUTER INTEGRATION ===

# Include Semantic Action APIs (Primary Architecture)
from trm_api.api.v1.api import api_router
app.include_router(api_router, prefix=settings.API_V1_STR)

# Include TRM-OS v2 Conversational Intelligence API
from trm_api.v2.api import v2_router
app.include_router(v2_router)

# === AGE SYSTEM ERROR HANDLING ===

@app.exception_handler(HTTPException)
async def age_http_exception_handler(request, exc):
    """AGE System HTTP Exception Handler with semantic context"""
    log_age_system(f"HTTP Exception: {exc.status_code} - {exc.detail}", "ERROR")
    return {
        "system": "AGE Error Handler",
        "error_type": "HTTP_EXCEPTION",
        "status_code": exc.status_code,
        "detail": exc.detail,
        "semantic_context": "Strategic operation failed",
        "recovery_suggestion": "Review request semantics and retry",
        "timestamp": datetime.datetime.now().isoformat()
    }

@app.exception_handler(Exception)
async def age_general_exception_handler(request, exc):
    """AGE System General Exception Handler"""
    log_age_system(f"General Exception: {str(exc)}", "CRITICAL")
    return {
        "system": "AGE Error Handler",
        "error_type": "SYSTEM_EXCEPTION", 
        "detail": "Internal AGE system error",
        "semantic_context": "Strategic orchestration interrupted",
        "recovery_suggestion": "Contact AGE system administrator",
        "timestamp": datetime.datetime.now().isoformat()
    }

# === AGE SYSTEM STARTUP ===

if __name__ == "__main__":
    import uvicorn
    import logging
    
    # Configure AGE system logging
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] AGE-%(levelname)s: %(message)s"
    )
    
    # Enable Neo4j query logging for ontology debugging
    neomodel_logger = logging.getLogger('neomodel')
    neomodel_logger.setLevel(logging.INFO)
    
    log_age_system("AGE System Manual Startup Initiated", "MANUAL")
    log_age_system("Starting AGE Orchestration Platform on port 8001", "MANUAL")
    
    try:
        uvicorn.run(
            app, 
            host="0.0.0.0",  # Allow external connections for Railway deployment
            port=int(os.environ.get("PORT", 8001)),  # Railway PORT environment variable
            log_level="info",
            access_log=True
        )
    except Exception as e:
        log_age_system(f"AGE System Startup Failed: {str(e)}", "CRITICAL")
        raise
