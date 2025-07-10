#!/usr/bin/env python3
"""
Event Service - AGE Semantic Architecture  
Handles Event phase của Recognition → Event → WIN pattern

ELIMINATED: Legacy Agent, Project models
REPLACED: AGEActor, StrategicUnit semantic ontology
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from neomodel import DoesNotExist

from trm_api.graph_models.event import Event as GraphEvent
from trm_api.models.event import EventCreate, EventUpdate, Event

# AGE Semantic Ontology Imports
# TODO: Implement full AGE ontology integration in future iterations
# from trm_api.ontology.age_actor import AGEActor  # Future implementation
# from trm_api.ontology.strategic_unit import StrategicUnit  # Future implementation

from trm_api.repositories.event_repository import EventRepository
from trm_api.core.logging_config import get_logger

logger = get_logger(__name__)

class EventService:
    """
    AGE Event Service - Semantic event orchestration
    Handles the Event phase of Recognition → Event → WIN cycle
    """
    
    def __init__(self):
        self.repository = EventRepository()
    
    def create_event(self, event_data: EventCreate) -> Optional[Event]:
        """Create strategic event using AGE semantic orchestration"""
        try:
            logger.info(f"AGE Event Service: Creating strategic event of type: {event_data.event_type}")
            
            graph_event = self.repository.create_event(event_data)
            
            if graph_event:
                event = Event(
                    uid=graph_event.uid,
                    event_type=graph_event.event_type,
                    title=graph_event.title,
                    description=graph_event.description,
                    status=graph_event.status,
                    strategic_priority=graph_event.strategic_priority,
                    expected_outcome=graph_event.expected_outcome,
                    created_at=graph_event.created_at,
                    updated_at=graph_event.updated_at
                )
                
                logger.info(f"AGE Strategic Event created: {event.uid}")
                return event
            else:
                logger.error("Failed to create strategic event in AGE system")
                return None
                
        except Exception as e:
            logger.error(f"AGE Event Service error: {str(e)}")
            return None

    def get_event_by_id(self, event_id: str) -> Optional[Event]:
        """Get strategic event by ID with AGE context"""
        try:
            graph_event = self.repository.get_event_by_id(event_id)
            
            if graph_event:
                return Event(
                    uid=graph_event.uid,
                    event_type=graph_event.event_type,
                    title=graph_event.title,
                    description=graph_event.description,
                    status=graph_event.status,
                    strategic_priority=graph_event.strategic_priority,
                    expected_outcome=graph_event.expected_outcome,
                    created_at=graph_event.created_at,
                    updated_at=graph_event.updated_at
                )
            return None
            
        except Exception as e:
            logger.error(f"AGE Event retrieval error: {str(e)}")
            return None

    def update_event(self, event_id: str, update_data: EventUpdate) -> Optional[Event]:
        """Update strategic event with AGE intelligence"""
        try:
            updated_graph = self.repository.update_event(event_id, **update_data.dict(exclude_unset=True))
            
            if updated_graph:
                return Event(
                    uid=updated_graph.uid,
                    event_type=updated_graph.event_type,
                    title=updated_graph.title,
                    description=updated_graph.description,
                    status=updated_graph.status,
                    strategic_priority=updated_graph.strategic_priority,
                    expected_outcome=updated_graph.expected_outcome,
                    created_at=updated_graph.created_at,
                    updated_at=updated_graph.updated_at
                )
            return None
            
        except Exception as e:
            logger.error(f"AGE Event update error: {str(e)}")
            return None

    def delete_event(self, event_id: str) -> bool:
        """Delete strategic event with AGE validation"""
        try:
            return self.repository.delete_event(event_id)
        except Exception as e:
            logger.error(f"AGE Event deletion error: {str(e)}")
            return False

    def list_events(self, skip: int = 0, limit: int = 100) -> List[Event]:
        """List strategic events with AGE semantic context"""
        try:
            graph_events = self.repository.list_events(skip=skip, limit=limit)
            
            events = []
            for graph_event in graph_events:
                event = Event(
                    uid=graph_event.uid,
                    event_type=graph_event.event_type,
                    title=graph_event.title,
                    description=graph_event.description,
                    status=graph_event.status,
                    strategic_priority=graph_event.strategic_priority,
                    expected_outcome=graph_event.expected_outcome,
                    created_at=graph_event.created_at,
                    updated_at=graph_event.updated_at
                )
                events.append(event)
                
            logger.info(f"AGE Event Service: Listed {len(events)} strategic events")
            return events
            
        except Exception as e:
            logger.error(f"AGE Event listing error: {str(e)}")
            return []

    def get_strategic_events_analytics(self) -> Dict[str, Any]:
        """Get strategic event analytics using AGE intelligence"""
        try:
            all_events = self.list_events(limit=1000)
            
            analytics = {
                "total_events": len(all_events),
                "event_types": {},
                "status_distribution": {},
                "priority_distribution": {},
                "age_strategic_insights": {
                    "high_priority_events": 0,
                    "completion_rate": 0.0,
                    "strategic_recommendation": ""
                }
            }
            
            completed_events = 0
            high_priority_events = 0
            
            for event in all_events:
                # Event types
                event_type = event.event_type
                analytics["event_types"][event_type] = analytics["event_types"].get(event_type, 0) + 1
                
                # Status distribution
                status = event.status
                analytics["status_distribution"][status] = analytics["status_distribution"].get(status, 0) + 1
                
                if status in ['completed', 'successful', 'achieved']:
                    completed_events += 1
                
                # Priority distribution
                if hasattr(event, 'strategic_priority') and event.strategic_priority:
                    priority = event.strategic_priority
                    analytics["priority_distribution"][priority] = analytics["priority_distribution"].get(priority, 0) + 1
                    
                    if priority in ['high', 'critical']:
                        high_priority_events += 1
            
            # Calculate strategic insights
            if len(all_events) > 0:
                completion_rate = completed_events / len(all_events)
                analytics["age_strategic_insights"]["completion_rate"] = completion_rate
                analytics["age_strategic_insights"]["high_priority_events"] = high_priority_events
                
                # AGE strategic recommendation
                if completion_rate < 0.6:
                    analytics["age_strategic_insights"]["strategic_recommendation"] = "Focus on improving event execution and completion rates"
                elif high_priority_events > len(all_events) * 0.8:
                    analytics["age_strategic_insights"]["strategic_recommendation"] = "Consider balancing high-priority events with strategic planning"
                else:
                    analytics["age_strategic_insights"]["strategic_recommendation"] = "Strong strategic event execution performance"
            
            logger.info(f"AGE Event Analytics: {analytics['total_events']} strategic events analyzed")
            return analytics
            
        except Exception as e:
            logger.error(f"AGE Event analytics error: {str(e)}")
            return {
                "error": "Failed to generate AGE event analytics",
                "total_events": 0
            }
