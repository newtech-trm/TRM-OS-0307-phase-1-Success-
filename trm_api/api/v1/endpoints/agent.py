from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional, Any

from trm_api.models.agent import Agent, AgentCreate, AgentUpdate
from trm_api.models.pagination import PaginatedResponse
from trm_api.repositories.agent_repository import AgentRepository
from trm_api.adapters.decorators import adapt_ontology_response

router = APIRouter()

def get_agent_repository() -> AgentRepository:
    return AgentRepository()

@router.post("/", response_model=Agent, status_code=status.HTTP_201_CREATED)
async def create_agent(
    agent_in: AgentCreate,
    repo: AgentRepository = Depends(get_agent_repository)
):
    """
    Create a new Agent.
    """
    db_agent = await repo.create_agent(agent_data=agent_in)
    
    # Convert GraphAgent to dict format
    agent_dict = {
        'id': getattr(db_agent, 'uid', None),
        'name': getattr(db_agent, 'name', None),
        'type': getattr(db_agent, 'type', None),
        'status': getattr(db_agent, 'status', 'active'),
        'created_at': getattr(db_agent, 'created_at', None),
        'updated_at': getattr(db_agent, 'updated_at', None),
        'description': getattr(db_agent, 'description', None),
        'capabilities': getattr(db_agent, 'capabilities', []),
        'configuration': getattr(db_agent, 'configuration', {}),
        'metadata': getattr(db_agent, 'metadata', {})
    }
    
    # Convert datetime objects to ISO strings
    if agent_dict['created_at'] and hasattr(agent_dict['created_at'], 'isoformat'):
        agent_dict['created_at'] = agent_dict['created_at'].isoformat()
    if agent_dict['updated_at'] and hasattr(agent_dict['updated_at'], 'isoformat'):
        agent_dict['updated_at'] = agent_dict['updated_at'].isoformat()
    
    return agent_dict

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
    
    # Convert GraphAgent to dict format
    agent_dict = {
        'id': getattr(db_agent, 'uid', None),
        'name': getattr(db_agent, 'name', None),
        'type': getattr(db_agent, 'type', None),
        'status': getattr(db_agent, 'status', 'active'),
        'created_at': getattr(db_agent, 'created_at', None),
        'updated_at': getattr(db_agent, 'updated_at', None),
        'description': getattr(db_agent, 'description', None),
        'capabilities': getattr(db_agent, 'capabilities', []),
        'configuration': getattr(db_agent, 'configuration', {}),
        'metadata': getattr(db_agent, 'metadata', {})
    }
    
    # Convert datetime objects to ISO strings
    if agent_dict['created_at'] and hasattr(agent_dict['created_at'], 'isoformat'):
        agent_dict['created_at'] = agent_dict['created_at'].isoformat()
    if agent_dict['updated_at'] and hasattr(agent_dict['updated_at'], 'isoformat'):
        agent_dict['updated_at'] = agent_dict['updated_at'].isoformat()
    
    return agent_dict

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
    
    # Get agents for current page
    agents = await repo.list_agents(skip=skip, limit=page_size)
    
    # Convert GraphAgent objects to dict format
    agent_dicts = []
    for agent in agents:
        try:
            agent_dict = {
                'id': getattr(agent, 'uid', None),
                'name': getattr(agent, 'name', None),
                'type': getattr(agent, 'type', None),
                'status': getattr(agent, 'status', 'active'),
                'created_at': getattr(agent, 'created_at', None),
                'updated_at': getattr(agent, 'updated_at', None),
                'description': getattr(agent, 'description', None),
                'capabilities': getattr(agent, 'capabilities', []),
                'configuration': getattr(agent, 'configuration', {}),
                'metadata': getattr(agent, 'metadata', {})
            }
            # Convert datetime objects to ISO strings
            if agent_dict['created_at'] and hasattr(agent_dict['created_at'], 'isoformat'):
                agent_dict['created_at'] = agent_dict['created_at'].isoformat()
            if agent_dict['updated_at'] and hasattr(agent_dict['updated_at'], 'isoformat'):
                agent_dict['updated_at'] = agent_dict['updated_at'].isoformat()
            agent_dicts.append(agent_dict)
        except Exception as e:
            # Skip problematic agents
            continue
    
    # Get total count (for now, we'll use a simple approach)
    total_count = len(agent_dicts) + skip if len(agent_dicts) == page_size else skip + len(agent_dicts)
    
    return PaginatedResponse.create(
        items=agent_dicts,
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
    
    # Convert GraphAgent to dict format
    agent_dict = {
        'id': getattr(updated_agent, 'uid', None),
        'name': getattr(updated_agent, 'name', None),
        'type': getattr(updated_agent, 'type', None),
        'status': getattr(updated_agent, 'status', 'active'),
        'created_at': getattr(updated_agent, 'created_at', None),
        'updated_at': getattr(updated_agent, 'updated_at', None),
        'description': getattr(updated_agent, 'description', None),
        'capabilities': getattr(updated_agent, 'capabilities', []),
        'configuration': getattr(updated_agent, 'configuration', {}),
        'metadata': getattr(updated_agent, 'metadata', {})
    }
    
    # Convert datetime objects to ISO strings
    if agent_dict['created_at'] and hasattr(agent_dict['created_at'], 'isoformat'):
        agent_dict['created_at'] = agent_dict['created_at'].isoformat()
    if agent_dict['updated_at'] and hasattr(agent_dict['updated_at'], 'isoformat'):
        agent_dict['updated_at'] = agent_dict['updated_at'].isoformat()
    
    return agent_dict

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
