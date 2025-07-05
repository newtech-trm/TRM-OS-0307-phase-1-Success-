from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
import logging

from trm_api.models.agent import Agent, AgentCreate, AgentUpdate, AgentListResponse
from trm_api.repositories.agent_repository import AgentRepository
from trm_api.adapters.decorators import adapt_ontology_response

logger = logging.getLogger(__name__)
router = APIRouter()

def get_agent_repository() -> AgentRepository:
    return AgentRepository()

@router.post("/", response_model=Agent, status_code=status.HTTP_201_CREATED)
@adapt_ontology_response(entity_type="agent")
async def create_agent(
    agent_in: AgentCreate,
    repo: AgentRepository = Depends(get_agent_repository)
):
    """
    Create a new Agent.
    """
    return await repo.create_agent(agent_data=agent_in)

@router.get("/{agent_id}", response_model=Agent)
@adapt_ontology_response(entity_type="agent")
async def get_agent(
    agent_id: str,
    repo: AgentRepository = Depends(get_agent_repository)
):
    """
    Get a specific Agent by its ID.
    """
    db_agent = await repo.get_agent_by_uid(uid=agent_id)
    if db_agent is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")
    return db_agent

@router.get("/", response_model=AgentListResponse)
@adapt_ontology_response(entity_type="agent", response_item_key="items")
async def list_agents(
    skip: int = 0,
    limit: int = 100,
    repo: AgentRepository = Depends(get_agent_repository)
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
        
        # Get agents
        agents = await repo.list_agents(skip=skip, limit=limit)
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
    repo: AgentRepository = Depends(get_agent_repository)
):
    """
    Update an existing Agent.
    """
    updated_agent = await repo.update_agent(uid=agent_id, agent_data=agent_in)
    if updated_agent is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")
    return updated_agent

@router.delete("/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_agent(
    agent_id: str,
    repo: AgentRepository = Depends(get_agent_repository)
):
    """
    Delete an Agent.
    """
    deleted = await repo.delete_agent(uid=agent_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")
    return
