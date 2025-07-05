from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional, Any
from datetime import datetime

from trm_api.models.agent import Agent, AgentCreate, AgentUpdate
from trm_api.models.pagination import PaginatedResponse
from trm_api.repositories.agent_repository import AgentRepository
from trm_api.adapters.decorators import adapt_ontology_response

router = APIRouter()

def get_agent_repository() -> AgentRepository:
    return AgentRepository()

def convert_graph_agent_to_dict(agent) -> dict:
    """Convert GraphAgent to dict format safely"""
    try:
        agent_dict = {
            'id': getattr(agent, 'uid', None),
            'name': getattr(agent, 'name', None),
            'type': getattr(agent, 'type', None),
            'status': getattr(agent, 'status', 'active'),
            'description': getattr(agent, 'description', None),
            'capabilities': getattr(agent, 'capabilities', []),
            'configuration': getattr(agent, 'configuration', {}),
            'metadata': getattr(agent, 'metadata', {})
        }
        
        # Handle datetime fields safely
        created_at = getattr(agent, 'created_at', None)
        if created_at:
            if hasattr(created_at, 'isoformat'):
                agent_dict['created_at'] = created_at.isoformat()
            elif hasattr(created_at, 'to_native'):
                try:
                    native_dt = created_at.to_native()
                    agent_dict['created_at'] = native_dt.isoformat() if isinstance(native_dt, datetime) else str(native_dt)
                except:
                    agent_dict['created_at'] = str(created_at)
            else:
                agent_dict['created_at'] = str(created_at)
        else:
            agent_dict['created_at'] = None
            
        updated_at = getattr(agent, 'updated_at', None)
        if updated_at:
            if hasattr(updated_at, 'isoformat'):
                agent_dict['updated_at'] = updated_at.isoformat()
            elif hasattr(updated_at, 'to_native'):
                try:
                    native_dt = updated_at.to_native()
                    agent_dict['updated_at'] = native_dt.isoformat() if isinstance(native_dt, datetime) else str(native_dt)
                except:
                    agent_dict['updated_at'] = str(updated_at)
            else:
                agent_dict['updated_at'] = str(updated_at)
        else:
            agent_dict['updated_at'] = None
            
        return agent_dict
    except Exception as e:
        # Fallback to minimal dict
        return {
            'id': getattr(agent, 'uid', None) if agent else None,
            'name': getattr(agent, 'name', 'Unknown') if agent else 'Unknown',
            'type': None,
            'status': 'active',
            'created_at': None,
            'updated_at': None,
            'description': None,
            'capabilities': [],
            'configuration': {},
            'metadata': {}
        }

@router.post("/", response_model=Agent, status_code=status.HTTP_201_CREATED)
async def create_agent(
    agent_in: AgentCreate,
    repo: AgentRepository = Depends(get_agent_repository)
):
    """
    Create a new Agent.
    """
    graph_agent = await repo.create_agent(agent_data=agent_in)
    return convert_graph_agent_to_dict(graph_agent)

@router.get("/{agent_id}", response_model=Agent)
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
    return convert_graph_agent_to_dict(db_agent)

@router.get("/", response_model=PaginatedResponse[Agent])
async def list_agents(
    page: int = Query(1, ge=1, description="Page number, 1-indexed"),
    page_size: int = Query(10, ge=1, le=100, description="Number of items per page"),
    repo: AgentRepository = Depends(get_agent_repository)
) -> Any:
    """
    Retrieve a paginated list of Agents.
    """
    # Calculate skip based on page
    skip = (page - 1) * page_size
    
    # Get agents for current page - handle empty case gracefully
    try:
        graph_agents = await repo.list_agents(skip=skip, limit=page_size)
        if not graph_agents:
            graph_agents = []
        
        # Convert GraphAgent objects to dict format
        agents = [convert_graph_agent_to_dict(agent) for agent in graph_agents]
        
    except Exception as e:
        # If repository fails, return empty list instead of crashing
        agents = []
    
    # Get total count
    total_count = len(agents) + skip if len(agents) == page_size else skip + len(agents)
    
    return PaginatedResponse.create(
        items=agents,
        total_count=total_count,
        page=page,
        page_size=page_size
    )

@router.put("/{agent_id}", response_model=Agent)
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
    return convert_graph_agent_to_dict(updated_agent)

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