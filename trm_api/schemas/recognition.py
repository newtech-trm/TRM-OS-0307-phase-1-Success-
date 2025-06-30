from datetime import datetime
from typing import List, Optional, Dict, Any, Union
from enum import Enum
from pydantic import BaseModel, Field


class RecognitionType(str, Enum):
    """Recognition type enum matching Ontology V3.2"""
    GRATITUDE = "GRATITUDE"
    IMPACT = "IMPACT"
    INNOVATION = "INNOVATION"
    ENDORSEMENT = "ENDORSEMENT"
    ACHIEVEMENT = "ACHIEVEMENT"
    KUDOS = "KUDOS"  # Bổ sung để tương thích với dữ liệu hiện có trong DB


class RecognitionStatus(str, Enum):
    """Recognition status enum matching Ontology V3.2"""
    PROPOSED = "PROPOSED"
    GRANTED = "GRANTED"
    ARCHIVED = "ARCHIVED"


class RecognitionBase(BaseModel):
    """Base Pydantic model for Recognition shared properties"""
    name: str = Field(..., description="A concise title for the recognition")
    message: str = Field(..., description="Detailed message or description")
    recognition_type: RecognitionType = Field(
        default=RecognitionType.GRATITUDE,
        description="Type of recognition"
    )
    status: RecognitionStatus = Field(
        default=RecognitionStatus.GRANTED,
        description="Status of the recognition"
    )
    value_level: Optional[str] = Field(
        None,
        description="Qualitative or quantitative score of the value"
    )
    tags: List[str] = Field(
        default_factory=list,
        description="Tags associated with this recognition"
    )


class RecognitionCreate(RecognitionBase):
    """Pydantic model for creating a new Recognition"""
    given_by_agent_id: str = Field(
        ...,
        description="ID of the agent giving the recognition"
    )
    received_by_agent_ids: List[str] = Field(
        ...,
        description="IDs of agents receiving the recognition"
    )
    recognizes_win_id: Optional[str] = Field(
        None,
        description="ID of the WIN being recognized (if applicable)"
    )
    # Optional relationships
    recognizes_contributions: Optional[Dict[str, List[str]]] = Field(
        None,
        description="Dictionary mapping entity types to lists of IDs, e.g. {'project': ['id1', 'id2'], 'task': ['id3']}"
    )


class Recognition(RecognitionBase):
    """Pydantic model for representing a Recognition in API responses"""
    uid: str = Field(..., description="Unique identifier for the recognition")
    created_at: Optional[str] = Field(None, description="Creation timestamp (ISO format)")
    updated_at: Optional[str] = Field(None, description="Last update timestamp (ISO format)")

    model_config = {
        "from_attributes": True
    }


class RecognitionUpdate(BaseModel):
    """Pydantic model for updating an existing Recognition"""
    name: Optional[str] = Field(None, description="A concise title for the recognition")
    message: Optional[str] = Field(None, description="Detailed message or description")
    recognition_type: Optional[RecognitionType] = Field(
        None,
        description="Type of recognition"
    )
    status: Optional[RecognitionStatus] = Field(
        None,
        description="Status of the recognition"
    )
    value_level: Optional[str] = Field(
        None,
        description="Qualitative or quantitative score of the value"
    )
    tags: Optional[List[str]] = Field(
        None,
        description="Tags associated with this recognition"
    )


class RecognitionWithRelationships(Recognition):
    """Pydantic model for Recognition with relationships included"""
    given_by: Optional[Dict[str, Any]] = Field(None, description="Agent who gave the recognition")
    received_by: Optional[List[Dict[str, Any]]] = Field(None, description="Agents who received the recognition")
    recognizes_win: Optional[Dict[str, Any]] = Field(None, description="WIN that this recognition recognizes")
    recognizes_contributions: Optional[Dict[str, List[Dict[str, Any]]]] = Field(
        None,
        description="Contributions recognized by this recognition"
    )


class RecognitionList(BaseModel):
    """Pydantic model for paginated list of Recognition items"""
    items: List[Recognition] = Field(..., description="List of Recognition items")
    total: int = Field(..., description="Total number of items")
    skip: int = Field(0, description="Number of items skipped (offset)")
    limit: int = Field(100, description="Maximum number of items to return")
