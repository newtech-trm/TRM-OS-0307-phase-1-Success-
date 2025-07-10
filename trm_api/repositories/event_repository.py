#!/usr/bin/env python3
"""
Event Repository - AGE Semantic Architecture
"""

from typing import List, Optional, Dict, Any
from neomodel import DoesNotExist

from trm_api.graph_models.event import Event as GraphEvent
from trm_api.models.event import EventCreate

# AGE Semantic Ontology Imports
from trm_api.graph_models.strategic_project import GraphStrategicProject  # Replaced legacy Project
# TODO: Implement AGEActor ontology integration
# from trm_api.ontology.age_actor import AGEActor  # Future implementation

from trm_api.core.logging_config import get_logger

logger = get_logger(__name__)

class EventRepository:
    """AGE Event Repository - Strategic event orchestration"""
    
    def create_event(self, event_data: EventCreate) -> GraphEvent:
        """Create strategic event in AGE context"""
        try:
            event = GraphEvent(
                event_type=event_data.event_type,
                title=event_data.title,
                description=event_data.description,
                status=event_data.status or "planned",
                strategic_priority=getattr(event_data, 'strategic_priority', 'medium'),
                expected_outcome=getattr(event_data, 'expected_outcome', ''),
                scheduled_date=getattr(event_data, 'scheduled_date', None),
                completion_date=getattr(event_data, 'completion_date', None),
                strategic_context=getattr(event_data, 'strategic_context', {}),
                success_criteria=getattr(event_data, 'success_criteria', []),
                stakeholders_involved=getattr(event_data, 'stakeholders_involved', [])
            ).save()
            
            logger.info(f"AGE Strategic Event created: {event.uid} - {event.title}")
            return event
            
        except Exception as e:
            logger.error(f"AGE Event creation error: {str(e)}")
            raise

    def get_event_by_id(self, event_id: str) -> Optional[GraphEvent]:
        """Get strategic event by ID"""
        try:
            return GraphEvent.nodes.get_or_none(uid=event_id)
        except DoesNotExist:
            return None
        except Exception as e:
            logger.error(f"AGE Event retrieval error: {str(e)}")
            return None

    def list_events(self, skip: int = 0, limit: int = 100) -> List[GraphEvent]:
        """List strategic events"""
        try:
            events = GraphEvent.nodes.all()[skip:skip+limit]
            logger.info(f"AGE Event Repository: Listed {len(events)} strategic events")
            return events
        except Exception as e:
            logger.error(f"AGE Event listing error: {str(e)}")
            return []

    def update_event(self, uid: str, **kwargs) -> Optional[GraphEvent]:
        """Update strategic event"""
        try:
            event = self.get_event_by_id(uid)
            if not event:
                return None
            
            for field, value in kwargs.items():
                if hasattr(event, field):
                    setattr(event, field, value)
            
            event.save()
            logger.info(f"AGE Strategic Event updated: {event.uid}")
            return event
            
        except Exception as e:
            logger.error(f"AGE Event update error: {str(e)}")
            return None

    def delete_event(self, uid: str) -> bool:
        """Delete strategic event"""
        try:
            event = self.get_event_by_id(uid)
            if event:
                event.delete()
                logger.info(f"AGE Strategic Event deleted: {uid}")
                return True
            return False
        except Exception as e:
            logger.error(f"AGE Event deletion error: {str(e)}")
            return False
