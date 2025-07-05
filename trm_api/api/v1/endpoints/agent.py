from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional, Any

from trm_api.models.agent import Agent, AgentCreate, AgentUpdate
from trm_api.models.pagination import PaginatedResponse
from trm_api.repositories.agent_repository import AgentRepository
from trm_api.adapters.decorators import adapt_ontology_response

router = APIRouter()

def get_agent_repository() -> AgentRepository:
    return AgentRepository()

@router.post("/seed", response_model=dict, status_code=status.HTTP_201_CREATED)
async def seed_agents(
    repo: AgentRepository = Depends(get_agent_repository)
):
    """
    Seed test agents data to database.
    """
    # Production-ready agents data
    production_agents = [
        AgentCreate(
            name="TRM AI Assistant",
            agent_type="AIAgent",
            status="active",
            description="Primary AI assistant for TRM operations",
            capabilities=["natural_language_processing", "task_automation", "data_analysis"]
        ),
        AgentCreate(
            name="TRM AGE System",
            agent_type="AGE",
            status="active",
            description="Artificial Genesis Engine for TRM ecosystem orchestration",
            capabilities=["system_orchestration", "automated_decision_making", "resource_optimization"]
        ),
        AgentCreate(
            name="TRM Project Manager",
            agent_type="InternalAgent",
            status="active",
            description="Internal project management agent",
            job_title="Project Manager",
            department="Operations",
            capabilities=["project_planning", "resource_allocation", "timeline_management"]
        ),
        AgentCreate(
            name="TRM Founder",
            agent_type="InternalAgent",
            status="active",
            description="TRM Founder with full system authority",
            job_title="Founder & CEO",
            department="Executive",
            is_founder=True,
            founder_recognition_authority=True,
            capabilities=["strategic_leadership", "recognition_authority", "system_governance"]
        ),
        AgentCreate(
            name="TRM External Consultant",
            agent_type="ExternalAgent",
            status="active",
            description="External consulting agent for specialized tasks",
            contact_info={"email": "consultant@trm.com", "role": "Strategic Advisor"},
            capabilities=["strategic_consulting", "market_analysis", "business_development"]
        )
    ]
    
    created_agents = []
    errors = []
    
    for agent_data in production_agents:
        try:
            # Check if agent already exists
            existing = await repo.get_agent_by_name(agent_data.name)
            if existing:
                continue  # Skip if already exists
                
            agent = await repo.create_agent(agent_data)
            created_agents.append({
                "name": agent.name,
                "agent_type": agent.agent_type,
                "uid": agent.uid
            })
        except Exception as e:
            errors.append({
                "name": agent_data.name,
                "error": str(e)
            })
    
    return {
        "message": f"Successfully seeded {len(created_agents)} agents",
        "created_agents": created_agents,
        "errors": errors,
        "total_created": len(created_agents),
        "total_errors": len(errors)
    }

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

@router.get("/", response_model=PaginatedResponse[Agent])
@adapt_ontology_response(entity_type="agent", response_item_key="items")
async def list_agents(
    page: int = Query(1, ge=1, description="Page number, 1-indexed"),
    page_size: int = Query(10, ge=1, le=100, description="Number of items per page"),
    repo: AgentRepository = Depends(get_agent_repository)
) -> Any:
    """
    Retrieve a paginated list of Agents.
    """
    try:
        # Calculate skip based on page
        skip = (page - 1) * page_size
        
        # Get agents for current page with error handling
        agents = await repo.list_agents(skip=skip, limit=page_size)
        
        # Handle None or empty results
        if agents is None:
            agents = []
        
        # Get total count (for now, we'll use a simple approach)
        # In production, you might want to implement a count method in repository
        total_count = len(agents) + skip if len(agents) == page_size else skip + len(agents)
        
        return PaginatedResponse.create(
            items=agents,
            total_count=total_count,
            page=page,
            page_size=page_size
        )
    except Exception as e:
        # Log error for debugging
        print(f"Error in list_agents: {str(e)}")
        # Return empty result instead of 500 error
        return PaginatedResponse.create(
            items=[],
            total_count=0,
            page=page,
            page_size=page_size
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
