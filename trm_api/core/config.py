import os
import secrets
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    """
    AGE (Artificial Genesis Engine) Configuration
    Commercial AI Orchestration System Settings
    
    Philosophy: Recognition → Event → WIN through Strategic Intelligence
    """
    # === AGE SEMANTIC IDENTITY ===
    PROJECT_NAME: str = "AGE - Artificial Genesis Engine: Commercial AI Orchestration System"
    API_V1_STR: str = "/api/v1"
    
    # AGE System Identification
    SYSTEM_IDENTITY: str = "AGE_ORCHESTRATION_PLATFORM"
    SYSTEM_PURPOSE: str = "Commercial AI Coordination for Strategic Intelligence"
    ARCHITECTURE_PARADIGM: str = "Recognition_Event_WIN"

    # === CLOUD-FIRST INFRASTRUCTURE (AGE Design V2.0) ===
    
    # Neo4j Aura Cloud - Knowledge Graph & Ontology
    NEO4J_URI: str
    NEO4J_USER: str
    NEO4J_PASSWORD: str

    # Supabase Cloud - Primary Database & Vector Embeddings
    SUPABASE_URL: str
    SUPABASE_ANON_KEY: str
    SUPABASE_SERVICE_KEY: str
    SUPABASE_DB_PASSWORD: str
    
    # RabbitMQ Cloud - Message Queuing & Event Processing
    RABBITMQ_CLOUD_URL: str

    # Redis Connection - Made optional for deployment flexibility
    REDIS_URL: Optional[str] = "redis://localhost:6379"
    
    # === COMMERCIAL AI CONFIGURATION ===
    
    # OpenAI GPT-4o Integration
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4o"
    
    # Claude 3.5 Sonnet Integration  
    ANTHROPIC_API_KEY: Optional[str] = None
    ANTHROPIC_MODEL: str = "claude-3-5-sonnet-20241022"
    
    # Gemini Pro Integration
    GOOGLE_API_KEY: Optional[str] = None
    GEMINI_MODEL: str = "gemini-pro"
    
    # === MCP (Model Context Protocol) CONFIGURATION ===
    
    # MCP Database Access Configuration
    MCP_SUPABASE_ENABLED: bool = True
    MCP_NEO4J_ENABLED: bool = True
    MCP_SNOWFLAKE_ENABLED: bool = False  # Future implementation
    
    # === AGE ORCHESTRATION SETTINGS ===
    
    # Strategic Intelligence Configuration
    AGE_RECOGNITION_TIMEOUT: int = 300  # 5 minutes for Recognition phase
    AGE_EVENT_EXECUTION_TIMEOUT: int = 1800  # 30 minutes for Event execution
    AGE_WIN_VALIDATION_TIMEOUT: int = 600  # 10 minutes for WIN validation
    
    # AI Actor Configuration
    MAX_CONCURRENT_ACTORS: int = 10
    ACTOR_EXECUTION_RETRY_LIMIT: int = 3
    ACTOR_COORDINATION_STRATEGY: str = "parallel"
    
    # Strategic Learning Configuration
    LEARNING_INTEGRATION_ENABLED: bool = True
    SUCCESS_PATTERN_RETENTION: int = 1000  # Number of success patterns to retain
    FAILURE_MITIGATION_RETENTION: int = 500  # Number of failure patterns to retain
    
    # === ENTERPRISE INTEGRATION ===
    
    # CODA.io Enterprise Management
    CODA_API_TOKEN: Optional[str] = None
    CODA_DOC_ID: Optional[str] = None
    
    # Railway Deployment Configuration
    RAILWAY_PROJECT_ID: Optional[str] = None
    DEPLOYMENT_ENVIRONMENT: str = "production"
    
    # === SECURITY & COMPLIANCE ===
    
    # Security Settings
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Enterprise Security
    ZERO_TRUST_ENABLED: bool = True
    AUDIT_TRAIL_ENABLED: bool = True
    DATA_ENCRYPTION_ENABLED: bool = True

    model_config = SettingsConfigDict(
        env_file=os.path.join(BASE_DIR, ".env"),
        case_sensitive=True,
        extra='ignore' # Ignore extra fields from .env
    )

# Singleton instance of the AGE settings
settings = Settings()

def get_age_settings() -> Settings:
    """Get AGE Orchestration System settings instance"""
    return settings

def get_settings() -> Settings:
    """Legacy function name - maintained for compatibility"""
    return settings
