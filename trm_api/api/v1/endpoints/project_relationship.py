from fastapi import APIRouter, Depends, HTTPException, status, Query, Body
from pydantic import BaseModel
from typing import List, Optional
import uuid
from datetime import datetime

from trm_api.models.relationships import Relationship, TargetEntityTypeEnum
from trm_api.services.relationship_service import relationship_service, RelationshipService
from trm_api.adapters.decorators import adapt_ontology_response

router = APIRouter()

# MANAGES_PROJECT endpoints

class ManagesProjectRequest(BaseModel):
    """Optional properties for the MANAGES_PROJECT relationship."""
    start_date: Optional[datetime] = None
    role: Optional[str] = None
    notes: Optional[str] = None

@router.post("/agents/{agent_id}/manages-project/{project_id}", status_code=status.HTTP_201_CREATED)
@adapt_ontology_response(entity_type="relationship")
async def create_manages_project_relationship(
    agent_id: str,
    project_id: str,
    relationship_data: ManagesProjectRequest = Body(None),
    service: RelationshipService = Depends(lambda: relationship_service)
):
    """
    Create a MANAGES_PROJECT relationship from an Agent to a Project.
    
    Parameters:
    - agent_id: The ID of the Agent
    - project_id: The ID of the Project
    - relationship_data: Optional properties for the relationship
    
    Returns:
    - The created relationship
    """
    # Prepare optional properties
    properties = {}
    if relationship_data:
        if relationship_data.start_date:
            properties['start_date'] = relationship_data.start_date
        if relationship_data.role:
            properties['role'] = relationship_data.role
        if relationship_data.notes:
            properties['notes'] = relationship_data.notes
    
    relationship = await service.create_relationship(
        source_id=agent_id,
        source_type=TargetEntityTypeEnum.AGENT,
        target_id=project_id,
        target_type=TargetEntityTypeEnum.PROJECT,
        relationship_type="MANAGES_PROJECT",
        properties=properties
    )
    
    if not relationship:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent or Project not found or relationship could not be created."
        )
    
    return relationship

@router.get("/agents/{agent_id}/managed-projects")
@adapt_ontology_response(entity_type="relationship")
async def get_projects_managed_by_agent(
    agent_id: str,
    service: RelationshipService = Depends(lambda: relationship_service)
):
    """
    Get all Projects that a specific Agent manages.
    
    Parameters:
    - agent_id: The ID of the Agent
    
    Returns:
    - A list of relationships representing Projects that the Agent manages
    """
    relationships = await service.get_relationships(
        entity_id=agent_id,
        entity_type=TargetEntityTypeEnum.AGENT,
        direction="outgoing",
        relationship_type="MANAGES_PROJECT",
        related_entity_type=TargetEntityTypeEnum.PROJECT
    )
    
    return relationships

@router.get("/projects/{project_id}/managers")
@adapt_ontology_response(entity_type="relationship")
async def get_managers_of_project(
    project_id: str,
    service: RelationshipService = Depends(lambda: relationship_service)
):
    """
    Get all Agents that manage a specific Project.
    
    Parameters:
    - project_id: The ID of the Project
    
    Returns:
    - A list of relationships representing Agents that manage the Project
    """
    relationships = await service.get_relationships(
        entity_id=project_id,
        entity_type=TargetEntityTypeEnum.PROJECT,
        direction="incoming",
        relationship_type="MANAGES_PROJECT",
        related_entity_type=TargetEntityTypeEnum.AGENT
    )
    
    return relationships

@router.delete("/agents/{agent_id}/manages-project/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_manages_project_relationship(
    agent_id: str,
    project_id: str,
    service: RelationshipService = Depends(lambda: relationship_service)
):
    """
    Delete a MANAGES_PROJECT relationship between an Agent and a Project.
    
    Parameters:
    - agent_id: The ID of the Agent
    - project_id: The ID of the Project
    
    Returns:
    - 204 No Content if successful
    """
    success = await service.delete_relationship(
        source_id=agent_id,
        source_type=TargetEntityTypeEnum.AGENT,
        target_id=project_id,
        target_type=TargetEntityTypeEnum.PROJECT,
        relationship_type="MANAGES_PROJECT"
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Relationship not found or could not be deleted."
        )
