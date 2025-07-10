"""
MCP (Model Context Protocol) API Endpoints

Exposes universal data access capabilities across:
- Supabase Cloud (database, auth, vector)
- Neo4j Aura Cloud (knowledge graph)
- Snowflake Cloud (analytics warehouse)
- RabbitMQ Cloud (message queuing)
- CODA.io (enterprise management)
- Google Workspace (collaboration)
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks, Query
from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field
from datetime import datetime
import logging

from ....services.mcp_service import get_mcp_coordinator, MCPResourceType

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/mcp", tags=["MCP - Universal Data Access"])


# Request/Response Models
class MCPResourceRequest(BaseModel):
    """Request to read MCP resource"""
    server_name: str = Field(..., description="MCP server name (supabase, neo4j, etc.)")
    resource_uri: str = Field(..., description="Resource URI to access")
    
    class Config:
        schema_extra = {
            "example": {
                "server_name": "supabase",
                "resource_uri": "supabase://tables/entities"
            }
        }


class MCPToolRequest(BaseModel):
    """Request to execute MCP tool"""
    server_name: str = Field(..., description="MCP server name")
    tool_name: str = Field(..., description="Tool name to execute")
    arguments: Dict[str, Any] = Field(..., description="Tool arguments")
    
    class Config:
        schema_extra = {
            "example": {
                "server_name": "supabase",
                "tool_name": "query_database",
                "arguments": {
                    "query": "SELECT * FROM entities WHERE type = 'project'",
                    "params": {}
                }
            }
        }


class MCPUnifiedQueryRequest(BaseModel):
    """Request for unified query across multiple data sources"""
    query: str = Field(..., description="Query to execute across data sources")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context")
    preferred_sources: Optional[List[str]] = Field(None, description="Preferred data sources")
    
    class Config:
        schema_extra = {
            "example": {
                "query": "Find all projects related to user john@example.com",
                "context": {"user_id": "user123"},
                "preferred_sources": ["supabase", "neo4j"]
            }
        }


class MCPResourceResponse(BaseModel):
    """Response from MCP resource access"""
    server_name: str
    resource_uri: str
    data: Dict[str, Any]
    timestamp: datetime
    
    class Config:
        schema_extra = {
            "example": {
                "server_name": "supabase",
                "resource_uri": "supabase://tables/entities",
                "data": {"status": "success", "records": []},
                "timestamp": "2024-12-28T10:00:00Z"
            }
        }


class MCPToolResponse(BaseModel):
    """Response from MCP tool execution"""
    server_name: str
    tool_name: str
    result: Dict[str, Any]
    execution_time_seconds: float
    timestamp: datetime
    
    class Config:
        schema_extra = {
            "example": {
                "server_name": "supabase",
                "tool_name": "query_database",
                "result": {"status": "success", "records": []},
                "execution_time_seconds": 0.25,
                "timestamp": "2024-12-28T10:00:00Z"
            }
        }


class MCPUnifiedQueryResponse(BaseModel):
    """Response from unified MCP query"""
    query: str
    context: Optional[Dict[str, Any]]
    results: Dict[str, Any]
    sources_accessed: List[str]
    timestamp: datetime
    
    class Config:
        schema_extra = {
            "example": {
                "query": "Find all projects",
                "context": {},
                "results": {"supabase": {}, "neo4j": {}},
                "sources_accessed": ["supabase", "neo4j"],
                "timestamp": "2024-12-28T10:00:00Z"
            }
        }


# API Endpoints
@router.get("/resources", summary="List all available MCP resources")
async def list_mcp_resources(
    resource_type: Optional[MCPResourceType] = Query(None, description="Filter by resource type"),
    mcp = Depends(get_mcp_coordinator)
):
    """
    List all available MCP resources across data sources.
    
    Returns resources from:
    - Supabase Cloud (database, vector store, auth)
    - Neo4j Aura Cloud (knowledge graph, ontology)  
    - Snowflake Cloud (analytics warehouse)
    - RabbitMQ Cloud (message queuing)
    - CODA.io (enterprise management)
    - Google Workspace (collaboration)
    """
    try:
        all_resources = await mcp.list_all_resources()
        
        # Flatten and optionally filter resources
        flattened_resources = []
        for server_name, resources in all_resources.items():
            for resource in resources:
                if resource_type is None or resource.resource_type == resource_type:
                    flattened_resources.append({
                        "server_name": server_name,
                        "uri": resource.uri,
                        "name": resource.name,
                        "description": resource.description,
                        "resource_type": resource.resource_type.value,
                        "metadata": resource.metadata,
                        "created_at": resource.created_at.isoformat()
                    })
        
        return {
            "resources": flattened_resources,
            "total_count": len(flattened_resources),
            "resource_type_filter": resource_type.value if resource_type else None,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error listing MCP resources: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to list MCP resources: {str(e)}")


@router.post("/resource/read", response_model=MCPResourceResponse, summary="Read MCP resource")
async def read_mcp_resource(
    request: MCPResourceRequest,
    mcp = Depends(get_mcp_coordinator)
):
    """
    Read data from specific MCP resource.
    
    Supports reading from any registered MCP server:
    - supabase: Database tables, vector embeddings, auth data
    - neo4j: Knowledge graph nodes/relationships, ontology schema
    - snowflake: Analytics data, business intelligence
    - rabbitmq: Message queues, event streams
    """
    try:
        start_time = datetime.now()
        
        data = await mcp.read_resource(request.server_name, request.resource_uri)
        
        return MCPResourceResponse(
            server_name=request.server_name,
            resource_uri=request.resource_uri,
            data=data,
            timestamp=start_time
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error reading MCP resource: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to read MCP resource: {str(e)}")


@router.post("/tool/execute", response_model=MCPToolResponse, summary="Execute MCP tool")
async def execute_mcp_tool(
    request: MCPToolRequest,
    mcp = Depends(get_mcp_coordinator)
):
    """
    Execute tool on specific MCP server.
    
    Available tools by server:
    - supabase: query_database, vector_search, auth_operations
    - neo4j: cypher_query, graph_analysis, relationship_traversal
    - snowflake: analytics_query, data_warehouse_operations
    - rabbitmq: publish_message, subscribe_queue, queue_management
    """
    try:
        start_time = datetime.now()
        
        result = await mcp.call_tool(
            request.server_name,
            request.tool_name,
            request.arguments
        )
        
        execution_time = (datetime.now() - start_time).total_seconds()
        
        return MCPToolResponse(
            server_name=request.server_name,
            tool_name=request.tool_name,
            result=result,
            execution_time_seconds=execution_time,
            timestamp=start_time
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error executing MCP tool: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to execute MCP tool: {str(e)}")


@router.post("/query/unified", response_model=MCPUnifiedQueryResponse, summary="Unified query across data sources")
async def unified_mcp_query(
    request: MCPUnifiedQueryRequest,
    mcp = Depends(get_mcp_coordinator)
):
    """
    Execute unified query across multiple MCP data sources.
    
    Intelligently routes queries to appropriate data sources:
    - Graph/relationship queries → Neo4j Aura
    - User/auth queries → Supabase Cloud  
    - Analytics queries → Snowflake Cloud
    - Event/message queries → RabbitMQ Cloud
    - Enterprise data → CODA.io
    - Document queries → Google Workspace
    
    Returns combined results with source attribution.
    """
    try:
        start_time = datetime.now()
        
        result = await mcp.unified_query(request.query, request.context)
        
        return MCPUnifiedQueryResponse(
            query=request.query,
            context=request.context,
            results=result["results"],
            sources_accessed=list(result["results"].keys()),
            timestamp=start_time
        )
        
    except Exception as e:
        logger.error(f"Error executing unified MCP query: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to execute unified query: {str(e)}")


@router.get("/servers", summary="List registered MCP servers")
async def list_mcp_servers(mcp = Depends(get_mcp_coordinator)):
    """
    List all registered MCP servers and their capabilities.
    
    Returns information about available data sources and their tools.
    """
    try:
        servers_info = []
        
        for server_name, server in mcp.servers.items():
            servers_info.append({
                "name": server_name,
                "description": server.description,
                "resource_count": len(server.resources),
                "tool_count": len(server.tools),
                "resources": [
                    {
                        "uri": res.uri,
                        "name": res.name,
                        "type": res.resource_type.value
                    } for res in server.resources
                ],
                "tools": [
                    {
                        "name": tool.name,
                        "description": tool.description,
                        "resource_types": [rt.value for rt in tool.resource_types]
                    } for tool in server.tools
                ]
            })
        
        return {
            "servers": servers_info,
            "total_servers": len(servers_info),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error listing MCP servers: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to list MCP servers: {str(e)}")


@router.get("/health", summary="MCP system health check")
async def mcp_health_check(mcp = Depends(get_mcp_coordinator)):
    """
    Check health of all MCP servers and connections.
    
    Returns status of:
    - Supabase Cloud connection
    - Neo4j Aura Cloud connection
    - Snowflake Cloud connection
    - RabbitMQ Cloud connection
    - CODA.io integration
    - Google Workspace integration
    """
    try:
        health_status = {}
        
        for server_name, server in mcp.servers.items():
            try:
                # Test basic connectivity by listing resources
                resources = await server.list_resources()
                health_status[server_name] = {
                    "status": "healthy",
                    "resource_count": len(resources),
                    "last_check": datetime.now().isoformat()
                }
            except Exception as e:
                health_status[server_name] = {
                    "status": "unhealthy",
                    "error": str(e),
                    "last_check": datetime.now().isoformat()
                }
        
        overall_status = "healthy" if all(
            status["status"] == "healthy" 
            for status in health_status.values()
        ) else "degraded"
        
        return {
            "overall_status": overall_status,
            "servers": health_status,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error checking MCP health: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to check MCP health: {str(e)}") 