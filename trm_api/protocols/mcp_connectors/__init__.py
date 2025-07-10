"""
MCP (Model Context Protocol) Connectors Package

Platform-specific MCP implementations for enterprise integration:
- Snowflake Analytics Connector
- RabbitMQ Messaging Connector  
- Enhanced Supabase Operations
- Enhanced Neo4j Graph Operations
- CODA.io Workspace Integration
- Google Workspace Integration
"""

from .base_mcp_connector import (
    BaseMCPConnector,
    MCPConnectionConfig,
    MCPRequest,
    MCPResponse,
    MCPHealthCheck,
    MCPConnectionStatus,
    MCPOperationType
)
from .mcp_connector_registry import (
    MCPConnectorRegistry,
    RegistryStatus,
    ConnectorRegistration,
    RegistryMetrics,
    get_mcp_registry
)
from .rabbitmq_mcp import RabbitMQMCPConnector, create_rabbitmq_connector

# Import Snowflake connector if available
try:
    from .snowflake_mcp import SnowflakeMCPConnector, create_snowflake_connector
    _HAS_SNOWFLAKE = True
except ImportError:
    _HAS_SNOWFLAKE = False
    SnowflakeMCPConnector = None
    create_snowflake_connector = None

__all__ = [
    "BaseMCPConnector",
    "MCPConnectorRegistry",
    "RegistryStatus",
    "ConnectorRegistration", 
    "RegistryMetrics",
    "get_mcp_registry",
    'MCPConnectionConfig',
    'MCPRequest',
    'MCPResponse',
    'MCPHealthCheck',
    'MCPConnectionStatus',
    'MCPOperationType',
    'RabbitMQMCPConnector',
    'create_rabbitmq_connector'
]

# Add Snowflake exports if available
if _HAS_SNOWFLAKE:
    __all__.extend(['SnowflakeMCPConnector', 'create_snowflake_connector']) 