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
