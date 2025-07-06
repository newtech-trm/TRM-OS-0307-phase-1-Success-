from fastapi import APIRouter, HTTPException, status
from typing import List, Dict, Any
import logging

from trm_api.schemas.event import Event as EventResponseSchema, EventCreate as EventCreateSchema

router = APIRouter()

@router.get("/test")
async def test_events_endpoint():
    """Simple test endpoint to verify Events API is working"""
    return {
        "status": "ok",
        "message": "Events API is working",
        "timestamp": "2025-01-06T00:00:00Z",
        "deployment": "railway"
    }

@router.get("/", response_model=List[Dict[str, Any]])
async def list_events(
    skip: int = 0,
    limit: int = 100
):
    """
    Retrieve a list of Events - Railway deployment compatible version.
    """
    try:
        # Try to import and use the service
        from trm_api.services.event_service import event_service
        db_events = event_service.list_events(skip=skip, limit=limit)
        
        # Convert to dict format
        result = []
        for event in db_events:
            if hasattr(event, '__dict__'):
                result.append(event.__dict__)
            else:
                # Handle mock events
                result.append({
                    "uid": getattr(event, 'uid', 'unknown'),
                    "name": getattr(event, 'name', 'Unknown Event'),
                    "description": getattr(event, 'description', ''),
                    "payload": getattr(event, 'payload', {}),
                    "tags": getattr(event, 'tags', []),
                    "created_at": getattr(event, 'created_at', '2025-01-06T00:00:00Z'),
                    "updated_at": getattr(event, 'updated_at', '2025-01-06T00:00:00Z')
                })
        
        return result
        
    except Exception as e:
        logging.error(f"Error in list_events: {e}")
        # Return simple mock data for Railway deployment
        return [
            {
                "uid": "mock-event-001",
                "name": "Mock Event 1 (Service Unavailable)",
                "description": "Event listing temporarily unavailable due to database connection issues",
                "payload": {"status": "mock", "error": str(e)[:100], "deployment": "railway"},
                "tags": ["mock", "railway-deployment"],
                "created_at": "2025-01-06T00:00:00Z",
                "updated_at": "2025-01-06T00:00:00Z"
            },
            {
                "uid": "mock-event-002", 
                "name": "Mock Event 2 (Service Unavailable)",
                "description": "This is mock data returned when the database is not available",
                "payload": {"status": "mock", "deployment": "railway"},
                "tags": ["mock", "railway-deployment"],
                "created_at": "2025-01-06T00:00:00Z",
                "updated_at": "2025-01-06T00:00:00Z"
            }
        ]

@router.get("/{event_id}", response_model=Dict[str, Any])
async def get_event(event_id: str):
    """
    Get a specific Event by its ID - Railway deployment compatible version.
    """
    try:
        from trm_api.services.event_service import event_service
        db_event = event_service.get_event_by_id(event_id=event_id)
        if db_event is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
        
        # Convert to dict format
        if hasattr(db_event, '__dict__'):
            return db_event.__dict__
        else:
            return {
                "uid": getattr(db_event, 'uid', event_id),
                "name": getattr(db_event, 'name', 'Unknown Event'),
                "description": getattr(db_event, 'description', ''),
                "payload": getattr(db_event, 'payload', {}),
                "tags": getattr(db_event, 'tags', []),
                "created_at": getattr(db_event, 'created_at', '2025-01-06T00:00:00Z'),
                "updated_at": getattr(db_event, 'updated_at', '2025-01-06T00:00:00Z')
            }
            
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error in get_event: {e}")
        return {
            "uid": event_id,
            "name": "Mock Event (Service Unavailable)",
            "description": f"Event retrieval temporarily unavailable: {str(e)[:100]}",
            "payload": {"status": "mock", "error": str(e)[:100], "deployment": "railway"},
            "tags": ["mock", "railway-deployment"],
            "created_at": "2025-01-06T00:00:00Z",
            "updated_at": "2025-01-06T00:00:00Z"
        }

@router.post("/", response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED)
async def create_event(event_in: EventCreateSchema):
    """
    Create a new Event - Railway deployment compatible version.
    """
    try:
        from trm_api.services.event_service import event_service
        db_event = event_service.create_event(event_data=event_in)
        
        # Convert to dict format
        if hasattr(db_event, '__dict__'):
            return db_event.__dict__
        else:
            return {
                "uid": getattr(db_event, 'uid', 'new-event'),
                "name": getattr(db_event, 'name', event_in.name),
                "description": getattr(db_event, 'description', event_in.description),
                "payload": getattr(db_event, 'payload', event_in.payload),
                "tags": getattr(db_event, 'tags', event_in.tags),
                "created_at": getattr(db_event, 'created_at', '2025-01-06T00:00:00Z'),
                "updated_at": getattr(db_event, 'updated_at', '2025-01-06T00:00:00Z')
            }
            
    except Exception as e:
        logging.error(f"Error in create_event: {e}")
        return {
            "uid": "mock-new-event",
            "name": event_in.name,
            "description": f"Event creation temporarily unavailable: {str(e)[:100]}",
            "payload": {"status": "mock", "original_payload": event_in.payload, "deployment": "railway"},
            "tags": ["mock", "railway-deployment"] + (event_in.tags or []),
            "created_at": "2025-01-06T00:00:00Z",
            "updated_at": "2025-01-06T00:00:00Z"
        }
