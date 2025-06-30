from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class EventBase(BaseModel):
    name: str = Field(..., description="The type or name of the event, e.g., 'TASK_CREATED', 'USER_LOGGED_IN'.")
    description: Optional[str] = Field(None, description="A human-readable description of the event.")
    payload: Optional[Dict[str, Any]] = Field(None, description="A flexible JSON object containing event-specific data.")
    tags: Optional[List[str]] = Field(default_factory=list, description="Tags for categorizing or filtering events.")

class EventCreate(EventBase):
    actor_uid: str = Field(..., description="UID of the Agent that triggered this event.")
    # context_uid and context_node_label are for the primary context entity
    context_uid: Optional[str] = Field(None, description="UID of the primary entity this event relates to (e.g., Project UID, Task UID).")
    context_node_label: Optional[str] = Field(None, description="Node label of the primary context entity (e.g., 'Project', 'Task'). Required if context_uid is provided.")

    model_config = {
        "from_attributes": True,
        # For OpenAPI example
        "json_schema_extra": {
            "example": {
                "name": "TASK_COMPLETED",
                "description": "User John Doe completed task 'Implement Feature X'.",
                "payload": {"task_details": "Details about feature X completion"},
                "tags": ["task", "completion", "feature-X"],
                "actor_uid": "agent_uid_of_john_doe",
                "context_uid": "task_uid_for_feature_x",
                "context_node_label": "Task"
            }
        }
    }

class Event(EventBase): # For response model, inherits from EventBase
    uid: str
    created_at: str # Assuming datetime is converted to string for response
    updated_at: str # Assuming datetime is converted to string for response
    
    # If we want to show resolved relationships in the response:
    # triggered_by_actor: Optional[Any] # Simplified for now, can be a specific Actor schema
    # primary_context_entity: Optional[Any] # Simplified for now

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "uid": "event_unique_id",
                "name": "TASK_COMPLETED",
                "description": "User John Doe completed task 'Implement Feature X'.",
                "payload": {"task_details": "Details about feature X completion"},
                "tags": ["task", "completion", "feature-X"],
                "created_at": "2024-01-01T12:00:00Z",
                "updated_at": "2024-01-01T12:00:00Z"
            }
        }
    }
