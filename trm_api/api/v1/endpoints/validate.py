from fastapi import APIRouter, Body, HTTPException, status
from typing import Dict, Any, List, Optional, Union

from trm_api.adapters.data_adapters import BaseEntityAdapter
from trm_api.adapters.entity_adapters import (
    WinAdapter, 
    RecognitionAdapter, 
    TaskAdapter, 
    EventAdapter,
    KnowledgeSnippetAdapter
)
from trm_api.models.enums import EntityType
from trm_api.adapters.enum_adapter import (
    normalize_win_status, 
    normalize_win_type,
    normalize_recognition_status,
    normalize_task_status,
    normalize_event_type,
    normalize_knowledge_snippet_type
)

router = APIRouter(prefix="/validate", tags=["validate"])


@router.post("/entity/{entity_type}")
async def validate_entity_data(
    entity_type: EntityType,
    data: Dict[str, Any] = Body(...)
) -> Dict[str, Any]:
    """Validate entity data against ontology schema and normalize it.
    
    This endpoint takes raw entity data and applies ontology-first validation and normalization.
    It returns the normalized data that would be returned by the API, or appropriate error messages.
    
    Args:
        entity_type: The type of entity to validate
        data: The raw entity data to validate
        
    Returns:
        The normalized entity data according to ontology
    """
    # Select the appropriate adapter based on entity type
    adapter: Optional[BaseEntityAdapter] = None
    
    if entity_type == EntityType.WIN:
        adapter = WinAdapter()
    elif entity_type == EntityType.RECOGNITION:
        adapter = RecognitionAdapter()
    elif entity_type == EntityType.TASK:
        adapter = TaskAdapter()
    elif entity_type == EntityType.EVENT:
        adapter = EventAdapter()
    elif entity_type == EntityType.KNOWLEDGE_SNIPPET:
        adapter = KnowledgeSnippetAdapter()
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported entity type: {entity_type}"
        )
    
    try:
        # Apply the adapter to normalize the data
        normalized_data = adapter.apply_to_entity(data)
        return {
            "status": "valid",
            "normalized_data": normalized_data
        }
    except Exception as e:
        # Return detailed validation errors
        return {
            "status": "invalid",
            "error": str(e),
            "original_data": data
        }


@router.post("/enum/{enum_type}")
async def validate_enum_value(
    enum_type: str,
    value: str = Body(..., embed=True),
    fallback: Optional[str] = Body(None, embed=True)
) -> Dict[str, Any]:
    """Validate and normalize a single enum value.
    
    This endpoint takes an enum type and value and applies ontology-first normalization.
    It returns the normalized enum value or appropriate error messages.
    
    Args:
        enum_type: The type of enum to validate (win_status, win_type, etc.)
        value: The enum value to validate
        fallback: Optional fallback value if validation fails
        
    Returns:
        The validation result with normalized value or error
    """
    try:
        normalized_value = None
        
        if enum_type == "win_status":
            normalized_value = normalize_win_status(value, fallback)
        elif enum_type == "win_type":
            normalized_value = normalize_win_type(value, fallback)
        elif enum_type == "recognition_status":
            normalized_value = normalize_recognition_status(value, fallback)
        elif enum_type == "task_status":
            normalized_value = normalize_task_status(value, fallback)
        elif enum_type == "event_type":
            normalized_value = normalize_event_type(value, fallback)
        elif enum_type == "knowledge_snippet_type":
            normalized_value = normalize_knowledge_snippet_type(value, fallback)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported enum type: {enum_type}"
            )
        
        return {
            "status": "valid",
            "original_value": value,
            "normalized_value": normalized_value
        }
    except ValueError as e:
        return {
            "status": "invalid",
            "error": str(e),
            "original_value": value,
            "fallback_attempted": fallback is not None
        }
