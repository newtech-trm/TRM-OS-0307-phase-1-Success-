from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any, Optional

from trm_api.schemas.event import Event as EventResponseSchema, EventCreate as EventCreateSchema
from trm_api.services.event_service import event_service, EventService
from trm_api.graph_models.event import Event as EventGraphModel
# Import mới - sử dụng adapters.decorators thay vì utils.datetime_adapter
from trm_api.adapters.decorators import adapt_event_response

router = APIRouter()

# Sử dụng decorator adapt_event_response cho ontology-first pattern

@router.post("/", response_model=EventResponseSchema, status_code=status.HTTP_201_CREATED)
@adapt_event_response()
async def create_event(
    event_in: EventCreateSchema,
    service: EventService = Depends(lambda: event_service)
):
    """
    Create a new Event. Events are immutable.
    """
    # The service now expects event_data as the parameter name
    db_event = service.create_event(event_data=event_in)
    # Không cần phải gọi adapt_model_to_schema nữa vì decorator adapt_event_response sẽ tự động làm việc này
    return db_event

@router.get("/{event_id}", response_model=EventResponseSchema)
@adapt_event_response()
async def get_event(
    event_id: str,
    service: EventService = Depends(lambda: event_service)
):
    """
    Get a specific Event by its ID.
    """
    db_event = service.get_event_by_id(event_id=event_id)
    if db_event is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    # Decorator adapt_event_response sẽ tự động chuyển đổi id và chuẩn hóa các trường
    return db_event

@router.get("/", response_model=List[EventResponseSchema])
@adapt_event_response()
async def list_events(
    skip: int = 0,
    limit: int = 100,
    service: EventService = Depends(lambda: event_service)
):
    """
    Retrieve a list of Events.
    """
    db_events = service.list_events(skip=skip, limit=limit)
    # Decorator adapt_event_response sẽ tự động xử lý collection
    return db_events
