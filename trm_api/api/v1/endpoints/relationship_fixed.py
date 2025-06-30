from fastapi import APIRouter, Depends, HTTPException, status, Query, Body
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum
import uuid

from trm_api.models.relationships import Relationship, RelationshipType, TargetEntityTypeEnum
from trm_api.services.relationship import RelationshipService
from trm_api.dependencies.neo4j import relationship_service


class DirectionEnum(str, Enum):
    OUTGOING = "outgoing"
    INCOMING = "incoming"
    BOTH = "both"


@router.post("/", response_model=Relationship, status_code=status.HTTP_201_CREATED)
async def create_relationship(
    source_id: str,
    source_type: TargetEntityTypeEnum,
    target_id: str,
    target_type: TargetEntityTypeEnum,
    relationship_type: RelationshipType,
    service: RelationshipService = Depends(lambda: relationship_service)
):
    """
    Create a new relationship between two entities.
    
    Parameters:
    - source_id: The ID of the source entity
    - source_type: The type of the source entity
    - target_id: The ID of the target entity
    - target_type: The type of the target entity
    - relationship_type: The type of relationship to create
    
    Returns:
    - The created relationship
    """
    relationship = await service.create_relationship(
        source_id=source_id,
        source_type=source_type,
        target_id=target_id,
        target_type=target_type,
        relationship_type=relationship_type
    )
    
    if not relationship:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not create relationship. One or both entities may not exist."
        )
        
    return relationship


@router.get("/", response_model=List[Relationship])
async def get_relationships(
    entity_id: Optional[str] = None,
    entity_type: Optional[str] = None,
    direction: DirectionEnum = DirectionEnum.OUTGOING,
    relationship_type: Optional[RelationshipType] = None,
    related_entity_type: Optional[TargetEntityTypeEnum] = None,
    service: RelationshipService = Depends(lambda: relationship_service)
):
    """
    Get relationships for an entity.
    
    Parameters:
    - entity_id: The ID of the entity
    - entity_type: The type of the entity
    - direction: The direction of the relationships (outgoing, incoming, both)
    - relationship_type: Optional filter for a specific relationship type
    - related_entity_type: Optional filter for a specific related entity type
    
    Returns:
    - A list of relationships
    """
    if not entity_id or not entity_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Entity ID and type must be provided."
        )
        
    relationships = await service.get_relationships(
        entity_id=entity_id,
        entity_type=entity_type,
        direction=direction,
        relationship_type=relationship_type,
        related_entity_type=related_entity_type
    )
    
    return relationships


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_relationship(
    source_id: str,
    source_type: TargetEntityTypeEnum,
    target_id: str,
    target_type: TargetEntityTypeEnum,
    relationship_type: RelationshipType,
    service: RelationshipService = Depends(lambda: relationship_service)
):
    """
    Delete a relationship between two entities.
    
    Parameters:
    - source_id: The ID of the source entity
    - source_type: The type of the source entity
    - target_id: The ID of the target entity
    - target_type: The type of the target entity
    - relationship_type: The type of relationship to delete
    
    Returns:
    - 204 No Content if successful
    """
    success = await service.delete_relationship(
        source_id=source_id,
        source_type=source_type,
        target_id=target_id,
        target_type=target_type,
        relationship_type=relationship_type
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Relationship not found or could not be deleted."
        )
        
    return None


# --- Specific Named Relationship Endpoints ---

# GIVEN_BY endpoints

class GivenByRequest(BaseModel):
    """Optional properties for the GIVEN_BY relationship."""
    notes: Optional[str] = None

@router.post("/given-by", response_model=Relationship, status_code=status.HTTP_201_CREATED)
async def create_given_by_relationship(
    agent_id: str,
    recognition_id: str,
    relationship_data: GivenByRequest = Body(None),
    service: RelationshipService = Depends(lambda: relationship_service)
):
    """
    Create a GIVEN_BY relationship from an Agent to a Recognition.
    
    Parameters:
    - agent_id: The ID of the Agent
    - recognition_id: The ID of the Recognition
    - relationship_data: Optional properties for the relationship
    
    Returns:
    - The created relationship
    """
    relationship_props = {}
    if relationship_data and relationship_data.notes:
        relationship_props["notes"] = relationship_data.notes
    
    relationship_props["relationshipId"] = f"given_by_{agent_id}_{recognition_id}_{str(uuid.uuid4())[:8]}"
    
    relationship = await service.create_relationship(
        source_id=agent_id,
        source_type=TargetEntityTypeEnum.AGENT,
        target_id=recognition_id,
        target_type=TargetEntityTypeEnum.RECOGNITION,
        relationship_type="GIVEN_BY",
        properties=relationship_props
    )
    
    if not relationship:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not create relationship. Agent or Recognition may not exist."
        )
        
    return relationship

@router.get("/agents/{agent_id}/gives-recognitions", response_model=List[Relationship])
async def get_recognitions_given_by_agent(
    agent_id: str,
    service: RelationshipService = Depends(lambda: relationship_service)
):
    """
    Get all Recognitions given by a specific Agent.
    
    Parameters:
    - agent_id: The ID of the Agent
    
    Returns:
    - A list of relationships representing Recognitions given by the Agent
    """
    relationships = await service.get_relationships(
        entity_id=agent_id,
        entity_type=TargetEntityTypeEnum.AGENT,
        direction=DirectionEnum.OUTGOING,
        relationship_type="GIVEN_BY",
        related_entity_type=TargetEntityTypeEnum.RECOGNITION
    )
    
    return relationships

@router.get("/recognitions/{recognition_id}/given-by", response_model=List[Relationship])
async def get_agents_giving_recognition(
    recognition_id: str,
    service: RelationshipService = Depends(lambda: relationship_service)
):
    """
    Get all Agents that have given a specific Recognition.
    
    Parameters:
    - recognition_id: The ID of the Recognition
    
    Returns:
    - A list of relationships representing Agents that have given the Recognition
    """
    relationships = await service.get_relationships(
        entity_id=recognition_id,
        entity_type=TargetEntityTypeEnum.RECOGNITION,
        direction=DirectionEnum.INCOMING,
        relationship_type="GIVEN_BY",
        related_entity_type=TargetEntityTypeEnum.AGENT
    )
    
    return relationships

@router.delete("/given-by", status_code=status.HTTP_204_NO_CONTENT)
async def delete_given_by_relationship(
    agent_id: str,
    recognition_id: str,
    service: RelationshipService = Depends(lambda: relationship_service)
):
    """
    Delete a GIVEN_BY relationship between an Agent and a Recognition.
    
    Parameters:
    - agent_id: The ID of the Agent
    - recognition_id: The ID of the Recognition
    
    Returns:
    - 204 No Content if successful
    """
    success = await service.delete_relationship(
        source_id=agent_id,
        source_type=TargetEntityTypeEnum.AGENT,
        target_id=recognition_id,
        target_type=TargetEntityTypeEnum.RECOGNITION,
        relationship_type="GIVEN_BY"
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Relationship not found or could not be deleted."
        )
