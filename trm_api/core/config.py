import os
import secrets
from typing import Optional
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

    # Neo4j Connection - with Railway fallback
    NEO4J_URI: str = os.environ.get("NEO4J_URI", "neo4j+s://ffcbb268.databases.neo4j.io")
    NEO4J_USER: str = os.environ.get("NEO4J_USER", "neo4j")
    NEO4J_PASSWORD: str = os.environ.get("NEO4J_PASSWORD", "cjXFyq4SMEcXKdlM6y3eN8Pd0kUSMuolnG3tGwYLSEI")

    # Supabase Connection - with Railway fallback
    SUPABASE_URL: str = os.environ.get("SUPABASE_URL", "https://ohihvimnbrqigcehyjuy.supabase.co")
    SUPABASE_ANON_KEY: str = os.environ.get("SUPABASE_ANON_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9oaWh2aW1uYnJxaWdjZWh5anV5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDg1OTU0ODUsImV4cCI6MjA2NDE3MTQ4NX0.m4x7-BlMjlwb1oarrMIhdZuerza5JIaVkfC768mooKQ")
    SUPABASE_SERVICE_KEY: str = os.environ.get("SUPABASE_SERVICE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9oaWh2aW1uYnJxaWdjZWh5anV5Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0ODU5NTQ4NSwiZXhwIjoyMDY0MTcxNDg1fQ.Od2k-j1HjbZsIn4ZqkZncK07VBJ0hK9cqNtioS9KoHg")
    SUPABASE_DB_PASSWORD: str = os.environ.get("SUPABASE_DB_PASSWORD", "Mangtienvechome123#")
    
    # RabbitMQ Connection - with Railway fallback
    RABBITMQ_CLOUD_URL: str = os.environ.get("RABBITMQ_CLOUD_URL", "amqps://hpzbofxa:VvMYrgYM4BlQ1BlhbQJsdGn7Pqs48V1D@fuji.lmq.cloudamqp.com/hpzbofxa")

    # Redis Connection - Made optional for deployment flexibility
    REDIS_URL: Optional[str] = "redis://localhost:6379"
    
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
