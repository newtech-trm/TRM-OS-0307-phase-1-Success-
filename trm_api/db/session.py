from neomodel import config, db
from neo4j import GraphDatabase
from trm_api.core.config import settings
import logging
import os

logger = logging.getLogger(__name__)

def init_neo4j():
    """
    Initialize Neo4j connection with proper error handling for deployment environments.
    """
    try:
        # Get Neo4j connection details with Railway deployment fallbacks
        neo4j_uri = os.getenv('NEO4J_URI') or settings.NEO4J_URI if hasattr(settings, 'NEO4J_URI') else None
        neo4j_user = os.getenv('NEO4J_USER') or settings.NEO4J_USER if hasattr(settings, 'NEO4J_USER') else None
        neo4j_password = os.getenv('NEO4J_PASSWORD') or settings.NEO4J_PASSWORD if hasattr(settings, 'NEO4J_PASSWORD') else None
        
        # Railway deployment fallback - use Railway-provided Neo4j if available
        if not neo4j_uri:
            # Check for Railway-specific environment variables
            railway_neo4j = os.getenv('DATABASE_URL') or os.getenv('NEO4J_DATABASE_URL')
            if railway_neo4j:
                neo4j_uri = railway_neo4j
                logging.info("Using Railway-provided Neo4j database URL")
            else:
                # Default fallback for production
                neo4j_uri = "neo4j+s://66abf65c.databases.neo4j.io"
                logging.warning("Using default production Neo4j URI as fallback")
        
        if not neo4j_user:
            neo4j_user = os.getenv('DATABASE_USER', 'neo4j')
            logging.warning("Using fallback Neo4j username")
            
        if not neo4j_password:
            neo4j_password = os.getenv('DATABASE_PASSWORD', '')
            logging.warning("Using fallback Neo4j password")
        
        # Validate that we have minimum required connection info
        if not neo4j_uri or not neo4j_user:
            logging.error("❌ Missing critical Neo4j connection parameters")
            raise ValueError("Neo4j connection parameters not properly configured")
        
        # The NEO4J_URI from .env should contain the hostname, e.g., "xxxx.databases.neo4j.io"
        # Extract hostname for neomodel configuration
        host = neo4j_uri
        if '://' in neo4j_uri:
            host = neo4j_uri.split('://')[-1]
        
        # Configure neomodel with proper authentication
        if neo4j_password:
            config.DATABASE_URL = f"neo4j+s://{neo4j_user}:{neo4j_password}@{host}"
        else:
            config.DATABASE_URL = f"neo4j+s://{neo4j_user}@{host}"
        
        logging.info(f"✅ Neo4j configured for host: {host}")
        
        # Test the connection
        try:
            db.cypher_query("RETURN 1 as test", {})
            logging.info("✅ Neo4j connection test successful")
        except Exception as conn_error:
            logging.error(f"❌ Neo4j connection test failed: {conn_error}")
            # For Railway deployment, don't crash the app - use mock mode
            if os.getenv('RAILWAY_ENVIRONMENT') or os.getenv('RAILWAY_PROJECT_ID'):
                logging.warning("🚀 Railway deployment detected - enabling graceful degradation mode")
                return False
            else:
                raise conn_error
                
        return True
        
    except Exception as e:
        logging.error(f"❌ Failed to initialize Neo4j: {e}")
        
        # For Railway deployment, enable graceful degradation
        if os.getenv('RAILWAY_ENVIRONMENT') or os.getenv('RAILWAY_PROJECT_ID'):
            logging.warning("🚀 Railway deployment detected - enabling graceful degradation mode")
            return False
        else:
            raise e


def get_neo4j_connection_status():
    """
    Get current Neo4j connection status for health checks.
    """
    try:
        db.cypher_query("RETURN 1 as test", {})
        return {"status": "connected", "message": "Neo4j connection is healthy"}
    except Exception as e:
        return {"status": "disconnected", "message": f"Neo4j connection failed: {str(e)}"}


# Initialize Neo4j connection on module import
neo4j_available = init_neo4j()


def connect_to_db():
    """
    Connects to the Neo4j database using the settings from the .env file.
    This function configures the neomodel library to use the correct database URL.
    """
    # The NEO4J_URI from .env should contain the hostname, e.g., "xxxx.databases.neo4j.io"
    # We strip any scheme that might be present to avoid creating a malformed URL.
    host = settings.NEO4J_URI
    if "://" in host:
        host = host.split("://")[1]

    # The scheme for AuraDB is 'neo4j+s'. We construct the full URL here.
    connection_url = f"neo4j+s://{settings.NEO4J_USER}:{settings.NEO4J_PASSWORD}@{host}"
    config.DATABASE_URL = connection_url
    logger.debug("Neomodel configured to connect to Neo4j on: {host}")

def close_db_connection():
    """
    In neomodel, connections are managed per-thread and there isn't a global
    disconnect function. This function is a placeholder for potential future cleanup.
    """
    logger.debug("Database connection managed by neomodel's thread-local driver. No explicit close action needed.")
    pass


# Singleton driver instance
_driver = None


def get_driver():
    """
    Returns a Neo4j driver instance for direct Cypher queries.
    This is used alongside neomodel when direct Neo4j driver access is needed.
    """
    global _driver
    if _driver is None:
        host = settings.NEO4J_URI
        if "://" in host:
            host = host.split("://")[1]
        
        uri = f"neo4j+s://{host}"
        _driver = GraphDatabase.driver(
            uri,
            auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
        )
    return _driver
