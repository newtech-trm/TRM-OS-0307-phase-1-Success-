import os
import logging
from neo4j import Driver
from typing import List, Optional, Dict, Any
from datetime import datetime

from fastapi import HTTPException, status
from trm_api.graph_models.event import Event as EventGraphModel
from trm_api.graph_models.agent import Agent as AgentGraphModel
from trm_api.graph_models.project import Project as ProjectGraphModel # Example, add others as needed
from trm_api.graph_models.task import Task as TaskGraphModel       # Example, add others as needed
from trm_api.graph_models.base import BaseNode # For type hinting context_node
from trm_api.schemas.event import EventCreate as EventCreateSchema, Event as EventResponseSchema

# Map for resolving context node labels to their neomodel classes
NODE_MODEL_MAP = {
    "Agent": AgentGraphModel,
    "Project": ProjectGraphModel,
    "Task": TaskGraphModel,
    # Add other models that can be an event context here
}

class EventService:
    """
    Service layer for handling business logic related to Events.
    Events are immutable; they can only be created and retrieved.
    Includes graceful degradation for deployment environments.
    """

    def __init__(self):
        self.neo4j_available = self._check_neo4j_availability()
        
    def _check_neo4j_availability(self) -> bool:
        """Check if Neo4j is available for operations"""
        try:
            # Import here to avoid circular imports
            from ..db.session import neo4j_available
            return neo4j_available
        except Exception as e:
            logging.warning(f"Neo4j availability check failed: {e}")
            return False

    def _get_mock_event(self, event_id: str = None) -> Dict[str, Any]:
        """Return mock event data when Neo4j is not available"""
        return {
            "uid": event_id or "mock-event-001",
            "name": "Mock Event (Database Unavailable)",
            "description": "This is a mock event returned when the database is not available",
            "payload": {"status": "mock", "reason": "database_unavailable"},
            "tags": ["mock", "system"],
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }

    def create_event(self, event_data: EventCreateSchema) -> EventGraphModel:
        """Creates a new Event node and its relationships using neomodel."""
        if not self.neo4j_available:
            logging.warning("Neo4j not available - returning mock event for create_event")
            mock_data = self._get_mock_event()
            # Create a mock EventGraphModel-like object
            class MockEvent:
                def __init__(self, data):
                    for key, value in data.items():
                        setattr(self, key, value)
            return MockEvent(mock_data)
        
        try:
            actor_node = AgentGraphModel.nodes.get_or_none(uid=event_data.actor_uid)
            if not actor_node:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Actor with UID {event_data.actor_uid} not found.")

            context_node: Optional[BaseNode] = None
            if event_data.context_uid and event_data.context_node_label:
                ContextModelClass = NODE_MODEL_MAP.get(event_data.context_node_label)
                if not ContextModelClass:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Invalid context node label: {event_data.context_node_label}. Supported labels are: {list(NODE_MODEL_MAP.keys())}"
                    )
                context_node = ContextModelClass.nodes.get_or_none(uid=event_data.context_uid)
                if not context_node:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"{event_data.context_node_label} context node with UID {event_data.context_uid} not found."
                    )
            elif event_data.context_uid or event_data.context_node_label: # XOR condition: if one is provided, the other must be too
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Both context_uid and context_node_label must be provided if one is present."
                )

            # Create the Event node
            new_event = EventGraphModel(
                name=event_data.name,
                description=event_data.description,
                payload=event_data.payload,
                tags=event_data.tags
            ).save()

            # Connect relationships
            actor_node.triggered_events.connect(new_event)

            if context_node:
                # Kết nối với relationship thích hợp dựa trên loại node context
                if event_data.context_node_label == "Agent":
                    new_event.primary_context_agent.connect(context_node)
                elif event_data.context_node_label == "Project":
                    new_event.primary_context_project.connect(context_node)
                elif event_data.context_node_label == "Task":
                    new_event.primary_context_task.connect(context_node)
                elif event_data.context_node_label == "Resource":
                    new_event.primary_context_resource.connect(context_node)
                else:
                    # Nếu có thêm loại node khác, cần bổ sung thêm ở đây và trong event.py
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Unsupported context node type for relationship: {event_data.context_node_label}"
                    )
            
            return new_event
            
        except Exception as e:
            if self.neo4j_available:
                raise e
            else:
                logging.warning(f"Event creation failed, returning mock: {e}")
                mock_data = self._get_mock_event()
                class MockEvent:
                    def __init__(self, data):
                        for key, value in data.items():
                            setattr(self, key, value)
                return MockEvent(mock_data)

    def get_event_by_id(self, event_id: str) -> Optional[EventGraphModel]:
        """Retrieves a single event by its unique ID using neomodel."""
        if not self.neo4j_available:
            logging.warning("Neo4j not available - returning mock event for get_event_by_id")
            mock_data = self._get_mock_event(event_id)
            class MockEvent:
                def __init__(self, data):
                    for key, value in data.items():
                        setattr(self, key, value)
            return MockEvent(mock_data)
        
        try:
            return EventGraphModel.nodes.get(uid=event_id)
        except EventGraphModel.DoesNotExist:
            return None
        except Exception as e:
            logging.warning(f"Event retrieval failed: {e}")
            if "connection" in str(e).lower() or "unavailable" in str(e).lower():
                self.neo4j_available = False
                return self.get_event_by_id(event_id)  # Retry with mock
            return None

    def list_events(self, skip: int = 0, limit: int = 100) -> List[EventGraphModel]:
        """Retrieves a list of events with pagination using neomodel."""
        if not self.neo4j_available:
            logging.warning("Neo4j not available - returning mock events for list_events")
            mock_events = []
            for i in range(min(limit, 5)):  # Return max 5 mock events
                mock_data = self._get_mock_event(f"mock-event-{i+1:03d}")
                class MockEvent:
                    def __init__(self, data):
                        for key, value in data.items():
                            setattr(self, key, value)
                mock_events.append(MockEvent(mock_data))
            return mock_events
        
        try:
            return list(EventGraphModel.nodes.all()[skip:skip+limit])
        except Exception as e:
            logging.warning(f"Event listing failed: {e}")
            if "connection" in str(e).lower() or "unavailable" in str(e).lower():
                self.neo4j_available = False
                return self.list_events(skip, limit)  # Retry with mock
            return []

# Singleton instance of the service
event_service = EventService()
