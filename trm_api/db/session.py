from neomodel import config
from neo4j import GraphDatabase
from trm_api.core.config import settings
import logging

logger = logging.getLogger(__name__)

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
