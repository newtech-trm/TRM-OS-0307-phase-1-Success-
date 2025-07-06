from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum
import uuid


class EventType(Enum):
    """Event types for TRM-OS system"""
    SYSTEM_INITIALIZED = "system.initialized"
    KNOWLEDGE_CREATED = "knowledge.created"
    AGENT_ACTION_COMPLETED = "agent.action.completed"
    AGENT_ACTION_FAILED = "agent.action.failed"
    QUANTUM_STATE_DETECTED = "quantum.state.detected"
    QUANTUM_OPTIMIZATION_COMPLETED = "quantum.optimization.completed"
    COHERENCE_ALERT = "coherence.alert"
    WIN_PROBABILITY_CALCULATED = "win.probability.calculated"


class EventBase(BaseModel):
    # e.g., 'tension.created', 'task.status.changed', 'agent.action.completed'
    event_type: str = Field(..., alias="eventType", description="A unique identifier for the type of event.")
    source: str = Field(..., description="The component or entity that generated the event, e.g., 'APIService' or 'CodeReviewerAgent'.")
    payload: Dict[str, Any] = Field(..., description="A JSON object containing the data associated with the event.")
    correlation_id: Optional[str] = Field(None, alias="correlationId", description="An ID to trace a sequence of related events.")

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "eventType": "task.status.changed",
                "source": "TaskService",
                "payload": {
                    "taskId": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
                    "oldStatus": "in_progress",
                    "newStatus": "done"
                },
                "correlationId": "corr-xyz-123"
            }
        }
    )

class EventCreate(EventBase):
    pass

# Events are typically immutable, so we don't define an EventUpdate model.

class EventInDB(EventBase):
    event_id: str = Field(alias="eventId", default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class Event(EventInDB):
    pass
