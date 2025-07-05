from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
import logging

from trm_api.models.agent import Agent, AgentCreate, AgentUpdate, AgentListResponse
from trm_api.services.simple_agent_service import simple_agent_service, SimpleAgentService
from trm_api.adapters.decorators import adapt_ontology_response

logger = logging.getLogger(__name__)
router = APIRouter()

def get_agent_service() -> SimpleAgentService:
    return simple_agent_service

@router.post("/", response_model=Agent, status_code=status.HTTP_201_CREATED)
@adapt_ontology_response(entity_type="agent")
async def create_agent(
    agent_in: AgentCreate,
    service: SimpleAgentService = Depends(get_agent_service)
):
    """
    Create a new Agent.
    """
    # TODO: Implement create in SimpleAgentService
    raise HTTPException(status_code=501, detail="Create not implemented yet")

@router.get("/{agent_id}", response_model=Agent)
@adapt_ontology_response(entity_type="agent")
async def get_agent(
    agent_id: str,
    service: SimpleAgentService = Depends(get_agent_service)
):
    """
    Get a specific Agent by its ID.
    """
    db_agent = service.get_agent_by_uid(uid=agent_id)
    if db_agent is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")
    return db_agent

@router.get("/", response_model=AgentListResponse)
@adapt_ontology_response(entity_type="agent", response_item_key="items")
async def list_agents(
    skip: int = 0,
    limit: int = 100,
    service: SimpleAgentService = Depends(get_agent_service)
):
    """
    Retrieve a list of Agents.
    """
    try:
        logger.info(f"Listing agents with skip={skip}, limit={limit}")
        
        # Test database connection first
        from neomodel import db
        try:
            results, meta = db.cypher_query("RETURN 1 as test")
            logger.info("Database connection test successful")
        except Exception as db_error:
            logger.error(f"Database connection failed: {db_error}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Database connection failed: {str(db_error)}"
            )
        
        # Get agents using simple service
        agents = service.list_agents(skip=skip, limit=limit)
        logger.info(f"Successfully retrieved {len(agents)} agents")
        
        return {"items": agents, "total": len(agents), "skip": skip, "limit": limit}
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error in list_agents: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@router.put("/{agent_id}", response_model=Agent)
@adapt_ontology_response(entity_type="agent")
async def update_agent(
    agent_id: str,
    agent_in: AgentUpdate,
    service: SimpleAgentService = Depends(get_agent_service)
):
    """
    Update an existing Agent.
    """
    # TODO: Implement update in SimpleAgentService
    raise HTTPException(status_code=501, detail="Update not implemented yet")

@router.delete("/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_agent(
    agent_id: str,
    service: SimpleAgentService = Depends(get_agent_service)
):
    """
    Delete an Agent.
    """
    # TODO: Implement delete in SimpleAgentService
    raise HTTPException(status_code=501, detail="Delete not implemented yet")
