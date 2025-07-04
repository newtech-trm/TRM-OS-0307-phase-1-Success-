from fastapi import APIRouter, Depends, HTTPException, status, Query, Body
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum
import uuid
from datetime import datetime

from trm_api.models.relationships import Relationship, RelationshipType, TargetEntityTypeEnum
from trm_api.services.relationship_service import relationship_service, RelationshipService
from trm_api.adapters.decorators import adapt_ontology_response

router = APIRouter()

class DirectionEnum(str, Enum):
    OUTGOING = "outgoing"
    INCOMING = "incoming"
    BOTH = "both"

@router.post("/", response_model=Relationship, status_code=status.HTTP_201_CREATED)
@adapt_ontology_response(entity_type="relationship")
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
@adapt_ontology_response(entity_type="relationship")
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
    # Khi cả hai tham số entity_id và entity_type là None, trả về danh sách rỗng thay vì gọi service
    if entity_id is None or entity_type is None:
        print("WARNING: entity_id hoặc entity_type là None, trả về danh sách rỗng")
        return []
    
    try:
        return await service.get_relationships(
            entity_id=entity_id,
            entity_type=entity_type,
            direction=direction,
            relationship_type=relationship_type,
            related_entity_type=related_entity_type
        )
    except Exception as e:
        print(f"Lỗi khi lấy relationships: {str(e)}")
        # Trong trường hợp có lỗi, trả về danh sách rỗng thay vì là lỗi
        return []

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
@adapt_ontology_response(entity_type="relationship")
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

# --- Specific Named Relationship Endpoints ---

@router.post("/creates-knowledge", response_model=Relationship)
@adapt_ontology_response(entity_type="relationship")
async def create_creates_knowledge_relationship(
    source_id: str,
    source_type: TargetEntityTypeEnum,
    knowledge_id: str,
    service: RelationshipService = Depends(lambda: relationship_service)
):
    """
    Create a CREATES_KNOWLEDGE relationship from an entity (User/Agent/Task) to a KnowledgeSnippet.
    
    Parameters:
    - source_id: The ID of the entity creating the knowledge
    - source_type: The type of entity (User, Agent, or Task)
    - knowledge_id: The ID of the KnowledgeSnippet
    
    Returns:
    - The created relationship
    """
    if source_type not in [TargetEntityTypeEnum.USER, TargetEntityTypeEnum.AGENT, TargetEntityTypeEnum.TASK]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid source type. Must be one of: User, Agent, Task."
        )
    
    relationship = await service.create_relationship(
        source_id=source_id,
        source_type=source_type,
        target_id=knowledge_id,
        target_type=TargetEntityTypeEnum.KNOWLEDGE_SNIPPET,
        relationship_type=RelationshipType.CREATES_KNOWLEDGE
    )
    
    if not relationship:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not create relationship. Source or KnowledgeSnippet may not exist."
        )
        
    return relationship

@router.post("/uses-knowledge", response_model=Relationship)
@adapt_ontology_response(entity_type="relationship")
async def create_uses_knowledge_relationship(
    source_id: str,
    source_type: TargetEntityTypeEnum,
    knowledge_id: str,
    service: RelationshipService = Depends(lambda: relationship_service)
):
    """
    Create a USES_KNOWLEDGE relationship from an entity (User/Agent/Task) to a KnowledgeSnippet.
    
    Parameters:
    - source_id: The ID of the entity using the knowledge
    - source_type: The type of entity (User, Agent, or Task)
    - knowledge_id: The ID of the KnowledgeSnippet
    
    Returns:
    - The created relationship
    """
    if source_type not in [TargetEntityTypeEnum.USER, TargetEntityTypeEnum.AGENT, TargetEntityTypeEnum.TASK]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid source type. Must be one of: User, Agent, Task."
        )
    
    relationship = await service.create_relationship(
        source_id=source_id,
        source_type=source_type,
        target_id=knowledge_id,
        target_type=TargetEntityTypeEnum.KNOWLEDGE_SNIPPET,
        relationship_type=RelationshipType.USES_KNOWLEDGE
    )
    
    if not relationship:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not create relationship. Source or KnowledgeSnippet may not exist."
        )
        
    return relationship

@router.post("/triggered-by", response_model=Relationship)
@adapt_ontology_response(entity_type="relationship")
async def create_triggered_by_relationship(
    source_id: str,
    source_type: TargetEntityTypeEnum,
    trigger_id: str,
    trigger_type: TargetEntityTypeEnum,
    service: RelationshipService = Depends(lambda: relationship_service)
):
    """
    Create a TRIGGERED_BY relationship to indicate what triggered an entity.
    
    Parameters:
    - source_id: The ID of the entity that was triggered
    - source_type: The type of entity (e.g., Event, Task, Tension)
    - trigger_id: The ID of the entity that triggered it
    - trigger_type: The type of the trigger entity (e.g., Event, Task, User)
    
    Returns:
    - The created relationship
    """
    valid_source_types = [TargetEntityTypeEnum.EVENT, TargetEntityTypeEnum.TASK, TargetEntityTypeEnum.TENSION]
    valid_trigger_types = [TargetEntityTypeEnum.EVENT, TargetEntityTypeEnum.TASK, TargetEntityTypeEnum.USER]
    
    if source_type not in valid_source_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid source type. Must be one of: Event, Task, Tension."
        )
        
    if trigger_type not in valid_trigger_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid trigger type. Must be one of: Event, Task, User."
        )
    
    relationship = await service.create_relationship(
        source_id=source_id,
        source_type=source_type,
        target_id=trigger_id,
        target_type=trigger_type,
        relationship_type=RelationshipType.TRIGGERED_BY
    )
    
    if not relationship:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not create relationship. Source or trigger entity may not exist."
        )
        
    return relationship

@router.post("/triggers", response_model=Relationship)
def create_triggers_relationship(
    source_id: str,
    source_type: TargetEntityTypeEnum,
    target_id: str,
    target_type: TargetEntityTypeEnum,
    service: RelationshipService = Depends(lambda: relationship_service)
):
    """
    Create a TRIGGERS relationship to indicate what an entity triggers.
    
    Parameters:
    - source_id: The ID of the entity that triggers
    - source_type: The type of entity (e.g., Event, Task, User)
    - target_id: The ID of the entity that is triggered
    - target_type: The type of the triggered entity (e.g., Event, Task, Tension)
    
    Returns:
    - The created relationship
    """
    valid_source_types = [TargetEntityTypeEnum.EVENT, TargetEntityTypeEnum.TASK, TargetEntityTypeEnum.USER]
    valid_target_types = [TargetEntityTypeEnum.EVENT, TargetEntityTypeEnum.TASK, TargetEntityTypeEnum.TENSION]
    
    if source_type not in valid_source_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid source type. Must be one of: Event, Task, User."
        )
        
    if target_type not in valid_target_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid target type. Must be one of: Event, Task, Tension."
        )
    
    relationship = service.create_relationship(
        source_id=source_id,
        source_type=source_type,
        target_id=target_id,
        target_type=target_type,
        relationship_type=RelationshipType.TRIGGERS
    )
    
    if not relationship:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not create relationship. Source or target entity may not exist."
        )
        
    return relationship

@router.post("/related-to", response_model=Relationship)
def create_related_to_relationship(
    source_id: str,
    source_type: TargetEntityTypeEnum,
    related_id: str,
    related_type: TargetEntityTypeEnum,
    service: RelationshipService = Depends(lambda: relationship_service)
):
    """
    Create a RELATED_TO relationship between any two entities.
    
    Parameters:
    - source_id: The ID of the source entity
    - source_type: The type of the source entity
    - related_id: The ID of the related entity
    - related_type: The type of the related entity
    
    Returns:
    - The created relationship
    """
    relationship = service.create_relationship(
        source_id=source_id,
        source_type=source_type,
        target_id=related_id,
        target_type=related_type,
        relationship_type=RelationshipType.RELATED_TO
    )
    
    if not relationship:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not create relationship. One or both entities may not exist."
        )
        
    return relationship

@router.post("/generates-knowledge", response_model=Relationship, status_code=status.HTTP_201_CREATED)
def create_generates_knowledge_relationship(
    win_id: str,
    knowledge_id: str,
    service: RelationshipService = Depends(lambda: relationship_service)
):
    """
    Create a GENERATES_KNOWLEDGE relationship from a WIN to a KnowledgeSnippet.
    
    Parameters:
    - win_id: The ID of the WIN
    - knowledge_id: The ID of the KnowledgeSnippet
    
    Returns:
    - The created relationship
    """
    relationship = service.create_relationship(
        source_id=win_id,
        source_type=TargetEntityTypeEnum.WIN,
        target_id=knowledge_id,
        target_type=TargetEntityTypeEnum.KNOWLEDGE_SNIPPET,
        relationship_type="GENERATES_KNOWLEDGE"
    )
    
    if not relationship:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not create relationship. WIN or KnowledgeSnippet may not exist."
        )
        
    return relationship

@router.get("/wins/{win_id}/generates-knowledge", response_model=List[Relationship])
def get_knowledge_snippets_generated_by_win(
    win_id: str,
    service: RelationshipService = Depends(lambda: relationship_service)
):
    """
    Get all KnowledgeSnippets generated by a specific WIN.
    
    Parameters:
    - win_id: The ID of the WIN
    
    Returns:
    - A list of relationships representing knowledge snippets generated by the WIN
    """
    relationships = service.get_relationships(
        entity_id=win_id,
        entity_type=TargetEntityTypeEnum.WIN,
        direction="outgoing",
        relationship_type="GENERATES_KNOWLEDGE",
        related_entity_type=TargetEntityTypeEnum.KNOWLEDGE_SNIPPET
    )
    
    return relationships

@router.get("/knowledge-snippets/{snippet_id}/generated-from-wins", response_model=List[Relationship])
def get_wins_generating_knowledge_snippet(
    snippet_id: str,
    service: RelationshipService = Depends(lambda: relationship_service)
):
    """
    Get all WINs that generate a specific KnowledgeSnippet.
    
    Parameters:
    - snippet_id: The ID of the KnowledgeSnippet
    
    Returns:
    - A list of relationships representing WINs that generate the knowledge snippet
    """
    relationships = service.get_relationships(
        entity_id=snippet_id,
        entity_type=TargetEntityTypeEnum.KNOWLEDGE_SNIPPET,
        direction="incoming",
        relationship_type="GENERATES_KNOWLEDGE",
        related_entity_type=TargetEntityTypeEnum.WIN
    )
    
    return relationships

@router.delete("/generates-knowledge", status_code=status.HTTP_204_NO_CONTENT)
def delete_generates_knowledge_relationship(
    win_id: str,
    knowledge_id: str,
    service: RelationshipService = Depends(lambda: relationship_service)
):
    """
    Delete a GENERATES_KNOWLEDGE relationship between a WIN and a KnowledgeSnippet.
    
    Parameters:
    - win_id: The ID of the WIN
    - knowledge_id: The ID of the KnowledgeSnippet
    
    Returns:
    - 204 No Content if successful
    """
    success = service.delete_relationship(
        source_id=win_id,
        source_type=TargetEntityTypeEnum.WIN,
        target_id=knowledge_id,
        target_type=TargetEntityTypeEnum.KNOWLEDGE_SNIPPET,
        relationship_type="GENERATES_KNOWLEDGE"
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Relationship not found or could not be deleted."
        )

# LEADS_TO_WIN endpoints

class ContributionLevelEnum(int, Enum):
    MINIMAL = 1
    MINOR = 2
    MODERATE = 3
    SIGNIFICANT = 4
    CRITICAL = 5

class LeadsToWinRequest(BaseModel):
    direct_contribution: Optional[bool] = True
    contribution_level: Optional[ContributionLevelEnum] = ContributionLevelEnum.MODERATE
    impact_ratio: Optional[float] = None
    recognition_score: Optional[int] = None
    verified_by: Optional[str] = None
    notes: Optional[str] = None

@router.post("/leads-to-win", response_model=Relationship)
async def create_leads_to_win_relationship(
    source_id: str,
    win_id: str,
    source_type: str = Query(..., description="Either 'Project' or 'Event'"),
    relationship_data: LeadsToWinRequest = Body(None),
    service: RelationshipService = Depends(lambda: relationship_service)
):
    """
    Create a LEADS_TO_WIN relationship from a Project or Event to a WIN.
    
    Parameters:
    - source_id: The ID of the source entity (Project or Event)
    - source_type: The type of the source entity (must be Project or Event)
    - win_id: The ID of the WIN
    - relationship_data: Optional properties for the relationship
    
    Returns:
    - The created relationship
    """
    # Validate source_type
    if source_type not in [TargetEntityTypeEnum.PROJECT, TargetEntityTypeEnum.EVENT]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid source type. Must be one of: Project, Event."
        )
    
    # Prepare relationship properties
    relationship_props = {}
    if relationship_data:
        if relationship_data.direct_contribution is not None:
            relationship_props["directContribution"] = relationship_data.direct_contribution
        if relationship_data.contribution_level is not None:
            relationship_props["contributionLevel"] = relationship_data.contribution_level
        if relationship_data.impact_ratio is not None:
            if 0 <= relationship_data.impact_ratio <= 1:
                relationship_props["impactRatio"] = relationship_data.impact_ratio
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="impact_ratio must be between 0 and 1"
                )
        if relationship_data.recognition_score is not None:
            if 1 <= relationship_data.recognition_score <= 100:
                relationship_props["recognitionScore"] = relationship_data.recognition_score
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="recognition_score must be between 1 and 100"
                )
        if relationship_data.verified_by:
            relationship_props["verifiedBy"] = relationship_data.verified_by
            relationship_props["verificationDate"] = datetime.utcnow()
        if relationship_data.notes:
            relationship_props["notes"] = relationship_data.notes
    
    # Generate unique relationship ID
    relationship_props["relationshipId"] = f"leads_to_win_{source_id}_{win_id}_{str(uuid.uuid4())[:8]}"
    
    # Create the relationship
    relationship = await service.create_relationship(
        source_id=source_id,
        source_type=source_type,
        target_id=win_id,
        target_type=TargetEntityTypeEnum.WIN,
        relationship_type="LEADS_TO_WIN",
        properties=relationship_props
    )
    
    if not relationship:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not create relationship. Source entity (Project/Event) or WIN may not exist."
        )
        
    return relationship

@router.get("/projects/{project_id}/leads-to-wins", response_model=List[Relationship])
@adapt_ontology_response(entity_type="relationship")
async def get_wins_from_project(
    project_id: str,
    service: RelationshipService = Depends(lambda: relationship_service)
):
    """
    Get all WINs led by a specific Project.
    
    Parameters:
    - project_id: The ID of the Project
    
    Returns:
    - A list of relationships representing WINs led by the Project
    """
    relationships = await service.get_relationships(
        entity_id=project_id,
        entity_type="Project",
        direction="outgoing",
        relationship_type="LEADS_TO_WIN"
    )
    return relationships

@router.get("/events/{event_id}/leads-to-wins", response_model=List[Relationship])
@adapt_ontology_response(entity_type="relationship")
async def get_wins_from_event(
    event_id: str,
    service: RelationshipService = Depends(lambda: relationship_service)
):
    """
    Get all WINs led by a specific Event.
    
    Parameters:
    - event_id: The ID of the Event
    
    Returns:
    - A list of relationships representing WINs led by the Event
    """
    relationships = await service.get_relationships(
        entity_id=event_id,
        entity_type="Event",
        direction="outgoing",
        relationship_type="LEADS_TO_WIN"
    )
    return relationships

@router.get("/wins/{win_id}/led-by", response_model=List[Relationship])
@adapt_ontology_response(entity_type="relationship")
async def get_projects_events_leading_to_win(
    win_id: str,
    source_type: Optional[str] = Query(None, description="Optional filter: 'Project' or 'Event'"),
    service: RelationshipService = Depends(lambda: relationship_service)
):
    """
    Get all Projects and Events leading to a specific WIN.
    
    Parameters:
    - win_id: The ID of the WIN
    - source_type: Optional filter for source type (Project or Event)
    
    Returns:
    - A list of relationships representing Projects and Events leading to the WIN
    """
    relationships = await service.get_relationships(
        entity_id=win_id,
        entity_type="Win",
        direction="incoming",
        relationship_type="LEADS_TO_WIN",
        related_entity_type=source_type if source_type else None
    )
    return relationships

@router.delete("/leads-to-win", status_code=status.HTTP_204_NO_CONTENT)
@adapt_ontology_response(entity_type="relationship")
async def delete_leads_to_win_relationship(
    source_id: str,
    win_id: str,
    source_type: str = Query(..., description="Either 'Project' or 'Event'"),
    service: RelationshipService = Depends(lambda: relationship_service)
):
    """
    Delete a LEADS_TO_WIN relationship from a Project or Event to a WIN.
    
    Parameters:
    - source_id: The ID of the source entity (Project or Event)
    - source_type: The type of the source entity (must be Project or Event)
    - win_id: The ID of the WIN
    
    Returns:
    - 204 No Content if successful
    """
    # Validate source_type
    if source_type not in [TargetEntityTypeEnum.PROJECT, TargetEntityTypeEnum.EVENT]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid source type. Must be one of: Project, Event."
        )
    
    success = await service.delete_relationship(
        source_id=source_id,
        source_type=source_type,
        target_id=win_id,
        target_type=TargetEntityTypeEnum.WIN,
        relationship_type="LEADS_TO_WIN"
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Relationship not found or could not be deleted."
        )

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
            detail="Could not create relationship. Source entity (Project/Event) or WIN may not exist."
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
        direction="outgoing",
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
        direction="incoming",
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


# RECEIVED_BY endpoints

class ReceivedByRequest(BaseModel):
    """Optional properties for the RECEIVED_BY relationship."""
    notes: Optional[str] = None

@router.post("/received-by", response_model=Relationship)
def create_received_by_relationship(
    recognition_id: str,
    agent_id: str,
    relationship_data: ReceivedByRequest = Body(None),
    service: RelationshipService = Depends(lambda: relationship_service)
):
    """
    Create a RECEIVED_BY relationship from a Recognition to an Agent.
    
    Parameters:
    - recognition_id: The ID of the Recognition
    - agent_id: The ID of the Agent receiving the recognition
    - relationship_data: Optional properties for the relationship
    
    Returns:
    - The created relationship
    """
    # Prepare relationship properties
    relationship_props = {}
    
    # Set any custom properties
    if relationship_data and relationship_data.notes:
        relationship_props["notes"] = relationship_data.notes
    
    # Generate unique relationship ID
    relationship_props["relationshipId"] = f"received_by_{recognition_id}_{agent_id}_{str(uuid.uuid4())[:8]}"
    
    # Create the relationship
    relationship = service.create_relationship(
        source_id=recognition_id,
        source_type=TargetEntityTypeEnum.RECOGNITION,
        target_id=agent_id,
        target_type=TargetEntityTypeEnum.AGENT,
        relationship_type="RECEIVED_BY",
        relationship_properties=relationship_props
    )
    
    if not relationship:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not create relationship. Recognition or Agent may not exist."
        )
        
    return relationship

@router.get("/recognitions/{recognition_id}/received-by", response_model=List[Relationship])
def get_agents_receiving_recognition(
    recognition_id: str,
    service: RelationshipService = Depends(lambda: relationship_service)
):
    """
    Get all Agents that received a specific Recognition.
    
    Parameters:
    - recognition_id: The ID of the Recognition
    
    Returns:
    - A list of relationships representing Agents that received the Recognition
    """
    relationships = service.get_relationships(
        entity_id=recognition_id,
        entity_type=TargetEntityTypeEnum.RECOGNITION,
        direction="outgoing",
        relationship_type="RECEIVED_BY",
        related_entity_type=TargetEntityTypeEnum.AGENT
    )
    
    return relationships

@router.get("/agents/{agent_id}/received-recognitions", response_model=List[Relationship])
def get_recognitions_received_by_agent(
    agent_id: str,
    service: RelationshipService = Depends(lambda: relationship_service)
):
    """
    Get all Recognitions received by a specific Agent.
    
    Parameters:
    - agent_id: The ID of the Agent
    
    Returns:
    - A list of relationships representing Recognitions received by the Agent
    """
    relationships = service.get_relationships(
        entity_id=agent_id,
        entity_type=TargetEntityTypeEnum.AGENT,
        direction="incoming",
        relationship_type="RECEIVED_BY",
        related_entity_type=TargetEntityTypeEnum.RECOGNITION
    )
    
    return relationships

@router.delete("/received-by", status_code=status.HTTP_204_NO_CONTENT)
def delete_received_by_relationship(
    recognition_id: str,
    agent_id: str,
    service: RelationshipService = Depends(lambda: relationship_service)
):
    """
    Delete a RECEIVED_BY relationship between a Recognition and an Agent.
    
    Parameters:
    - recognition_id: The ID of the Recognition
    - agent_id: The ID of the Agent
    
    Returns:
    - 204 No Content if successful
    """
    success = service.delete_relationship(
        source_id=recognition_id,
        source_type=TargetEntityTypeEnum.RECOGNITION,
        target_id=agent_id,
        target_type=TargetEntityTypeEnum.AGENT,
        relationship_type="RECEIVED_BY"
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Relationship not found or could not be deleted."
        )


# RECOGNIZES_CONTRIBUTION_TO endpoints

# Enum for supported target entity types in RECOGNIZES_CONTRIBUTION_TO relationship
class ContributionTargetTypeEnum(str, Enum):
    PROJECT = "Project"
    TASK = "Task"
    RESOURCE = "Resource"

class RecognizesContributionRequest(BaseModel):
    """Properties for the RECOGNIZES_CONTRIBUTION_TO relationship."""
    contribution_type: Optional[str] = None
    contribution_level: Optional[str] = None
    impact_notes: Optional[str] = None

@router.post("/recognizes-contribution-to", response_model=Relationship)
def create_recognizes_contribution_relationship(
    recognition_id: str,
    target_id: str,
    target_type: ContributionTargetTypeEnum,
    relationship_data: RecognizesContributionRequest = Body(None),
    service: RelationshipService = Depends(lambda: relationship_service)
):
    """
    Create a RECOGNIZES_CONTRIBUTION_TO relationship from a Recognition to a target entity (Project, Task, Resource).
    
    Parameters:
    - recognition_id: The ID of the Recognition
    - target_id: The ID of the target entity (Project, Task, or Resource)
    - target_type: The type of the target entity
    - relationship_data: Properties for the relationship
    
    Returns:
    - The created relationship
    """
    # Validate target entity type
    if target_type not in ContributionTargetTypeEnum.__members__.values():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid target type. Must be one of: {', '.join([e.value for e in ContributionTargetTypeEnum])}"
        )
    
    # Get the correct TargetEntityTypeEnum for the target entity
    if target_type == ContributionTargetTypeEnum.PROJECT:
        entity_type = TargetEntityTypeEnum.PROJECT
    elif target_type == ContributionTargetTypeEnum.TASK:
        entity_type = TargetEntityTypeEnum.TASK
    elif target_type == ContributionTargetTypeEnum.RESOURCE:
        entity_type = TargetEntityTypeEnum.RESOURCE
    
    # Prepare relationship properties
    relationship_props = {}
    
    # Set any custom properties
    if relationship_data:
        if relationship_data.contribution_type:
            relationship_props["contribution_type"] = relationship_data.contribution_type
        if relationship_data.contribution_level:
            relationship_props["contribution_level"] = relationship_data.contribution_level
        if relationship_data.impact_notes:
            relationship_props["impact_notes"] = relationship_data.impact_notes
    
    # Generate unique relationship ID
    relationship_props["relationshipId"] = f"recognizes_contribution_{recognition_id}_{target_id}_{str(uuid.uuid4())[:8]}"
    
    # Create the relationship
    relationship = service.create_relationship(
        source_id=recognition_id,
        source_type=TargetEntityTypeEnum.RECOGNITION,
        target_id=target_id,
        target_type=entity_type,
        relationship_type="RECOGNIZES_CONTRIBUTION_TO",
        relationship_properties=relationship_props
    )
    
    if not relationship:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not create relationship. Recognition or target entity may not exist."
        )
        
    return relationship

@router.get("/recognitions/{recognition_id}/recognizes-contributions", response_model=List[Relationship])
def get_contributions_recognized_by_recognition(
    recognition_id: str,
    target_type: Optional[ContributionTargetTypeEnum] = None,
    service: RelationshipService = Depends(lambda: relationship_service)
):
    """
    Get all entities that a specific Recognition recognizes contributions to.
    
    Parameters:
    - recognition_id: The ID of the Recognition
    - target_type: Optional filter for the type of target entity
    
    Returns:
    - A list of relationships representing contributions recognized by the Recognition
    """
    # Get the correct TargetEntityTypeEnum for the target entity if provided
    related_entity_type = None
    if target_type:
        if target_type == ContributionTargetTypeEnum.PROJECT:
            related_entity_type = TargetEntityTypeEnum.PROJECT
        elif target_type == ContributionTargetTypeEnum.TASK:
            related_entity_type = TargetEntityTypeEnum.TASK
        elif target_type == ContributionTargetTypeEnum.RESOURCE:
            related_entity_type = TargetEntityTypeEnum.RESOURCE
    
    relationships = service.get_relationships(
        entity_id=recognition_id,
        entity_type=TargetEntityTypeEnum.RECOGNITION,
        direction="outgoing",
        relationship_type="RECOGNIZES_CONTRIBUTION_TO",
        related_entity_type=related_entity_type
    )
    
    return relationships

@router.get("/projects/{project_id}/recognized-contributions", response_model=List[Relationship])
def get_recognitions_for_project_contribution(
    project_id: str,
    service: RelationshipService = Depends(lambda: relationship_service)
):
    """
    Get all Recognitions that recognize contributions to a specific Project.
    
    Parameters:
    - project_id: The ID of the Project
    
    Returns:
    - A list of relationships representing Recognitions for the Project's contributions
    """
    relationships = service.get_relationships(
        entity_id=project_id,
        entity_type=TargetEntityTypeEnum.PROJECT,
        direction="incoming",
        relationship_type="RECOGNIZES_CONTRIBUTION_TO",
        related_entity_type=TargetEntityTypeEnum.RECOGNITION
    )
    
    return relationships

@router.get("/tasks/{task_id}/recognized-contributions", response_model=List[Relationship])
def get_recognitions_for_task_contribution(
    task_id: str,
    service: RelationshipService = Depends(lambda: relationship_service)
):
    """
    Get all Recognitions that recognize contributions to a specific Task.
    
    Parameters:
    - task_id: The ID of the Task
    
    Returns:
    - A list of relationships representing Recognitions for the Task's contributions
    """
    relationships = service.get_relationships(
        entity_id=task_id,
        entity_type=TargetEntityTypeEnum.TASK,
        direction="incoming",
        relationship_type="RECOGNIZES_CONTRIBUTION_TO",
        related_entity_type=TargetEntityTypeEnum.RECOGNITION
    )
    
    return relationships

@router.get("/resources/{resource_id}/recognized-contributions", response_model=List[Relationship])
def get_recognitions_for_resource_contribution(
    resource_id: str,
    service: RelationshipService = Depends(lambda: relationship_service)
):
    """
    Get all Recognitions that recognize contributions to a specific Resource.
    
    Parameters:
    - resource_id: The ID of the Resource
    
    Returns:
    - A list of relationships representing Recognitions for the Resource's contributions
    """
    relationships = service.get_relationships(
        entity_id=resource_id,
        entity_type=TargetEntityTypeEnum.RESOURCE,
        direction="incoming",
        relationship_type="RECOGNIZES_CONTRIBUTION_TO",
        related_entity_type=TargetEntityTypeEnum.RECOGNITION
    )
    
    return relationships

@router.delete("/recognizes-contribution-to", status_code=status.HTTP_204_NO_CONTENT)
def delete_recognizes_contribution_relationship(
    recognition_id: str,
    target_id: str,
    target_type: ContributionTargetTypeEnum,
    service: RelationshipService = Depends(lambda: relationship_service)
):
    """
    Delete a RECOGNIZES_CONTRIBUTION_TO relationship between a Recognition and a target entity.
    
    Parameters:
    - recognition_id: The ID of the Recognition
    - target_id: The ID of the target entity (Project, Task, or Resource)
    - target_type: The type of the target entity
    
    Returns:
    - 204 No Content if successful
    """
    # Get the correct TargetEntityTypeEnum for the target entity
    if target_type == ContributionTargetTypeEnum.PROJECT:
        entity_type = TargetEntityTypeEnum.PROJECT
    elif target_type == ContributionTargetTypeEnum.TASK:
        entity_type = TargetEntityTypeEnum.TASK
    elif target_type == ContributionTargetTypeEnum.RESOURCE:
        entity_type = TargetEntityTypeEnum.RESOURCE
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid target type. Must be one of: {', '.join([e.value for e in ContributionTargetTypeEnum])}"
        )
    
    success = service.delete_relationship(
        source_id=recognition_id,
        source_type=TargetEntityTypeEnum.RECOGNITION,
        target_id=target_id,
        target_type=entity_type,
        relationship_type="RECOGNIZES_CONTRIBUTION_TO"
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Relationship not found or could not be deleted."
        )

