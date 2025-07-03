import os
import secrets
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    """
    Manages application settings loaded from the .env file.
    """
    # Base Project Settings
    PROJECT_NAME: str = "TRM Ontology Service"
    API_V1_STR: str = "/api/v1"

    # Neo4j Connection
    NEO4J_URI: str
    NEO4J_USER: str
    NEO4J_PASSWORD: str

    # Supabase Connection
    SUPABASE_URL: str
    SUPABASE_ANON_KEY: str
    SUPABASE_SERVICE_KEY: str
    SUPABASE_DB_PASSWORD: str
    
    # RabbitMQ Connection
    RABBITMQ_CLOUD_URL: str

    # Redis Connection
    REDIS_URL: str
    
    # Security Settings
    # Generate a random secret key if not provided
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    model_config = SettingsConfigDict(
        env_file=os.path.join(BASE_DIR, ".env"),
        case_sensitive=True,
        extra='ignore' # Ignore extra fields from .env
    )

# Singleton instance of the settings
settings = Settings()
