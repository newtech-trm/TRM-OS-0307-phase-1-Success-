import asyncio
import logging
from typing import Dict, List, Any, Callable, Coroutine, Optional, Set, TypeVar, Generic, Union
import json
from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field

from trm_api.core.config import settings

class EventType(str, Enum):
    """Các loại sự kiện trong hệ thống TRM-OS theo Ontology V3.2"""
    # Tension events
    TENSION_CREATED = "tension.created"
    TENSION_UPDATED = "tension.updated"
    TENSION_RESOLVED = "tension.resolved"
    
    # Task events
    TASK_CREATED = "task.created"
    TASK_UPDATED = "task.updated"
    TASK_COMPLETED = "task.completed"
    
    # Project events
    PROJECT_CREATED = "project.created"
    PROJECT_UPDATED = "project.updated"
    PROJECT_COMPLETED = "project.completed"
    
    # Agent events
    AGENT_ACTIVATED = "agent.activated"
    AGENT_DEACTIVATED = "agent.deactivated"
    AGENT_ERROR = "agent.error"
    
    # Knowledge events
    KNOWLEDGE_CREATED = "knowledge.created"
    KNOWLEDGE_VALIDATED = "knowledge.validated"
    
    # Recognition events
    RECOGNITION_CREATED = "recognition.created"
    
    # WIN events
    WIN_CREATED = "win.created"

class SystemEvent(BaseModel):
    """Định nghĩa cấu trúc của một sự kiện trong hệ thống"""
    event_type: EventType
    event_id: str = Field(default_factory=lambda: f"evt_{datetime.now().strftime('%Y%m%d%H%M%S')}_{id(object())}")
    timestamp: datetime = Field(default_factory=datetime.now)
    source_agent_id: Optional[str] = None
    target_agent_ids: List[str] = Field(default_factory=list)
    entity_id: Optional[str] = None
    entity_type: Optional[str] = None
    data: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)

EventHandler = Callable[[SystemEvent], Coroutine[Any, Any, None]]

class SystemEventBus:
    """Triển khai Event Bus cho giao tiếp giữa các AI Agent trong TRM-OS"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SystemEventBus, cls).__new__(cls)
            cls._instance._subscribers: Dict[EventType, List[EventHandler]] = {}
            cls._instance._logger = logging.getLogger("system_event_bus")
            cls._instance._event_history: List[SystemEvent] = []
            cls._instance._max_history_size = 1000
        return cls._instance
    
    async def publish(self, event: SystemEvent) -> None:
        """Đăng một sự kiện lên event bus và thông báo cho tất cả subscribers"""
        self._logger.info(f"Publishing event: {event.event_type} - {event.event_id}")
        
        # Lưu sự kiện vào lịch sử
        self._event_history.append(event)
        if len(self._event_history) > self._max_history_size:
            self._event_history.pop(0)
        
        # Kiểm tra nếu có subscribers
        if event.event_type in self._subscribers:
            coroutines = [handler(event) for handler in self._subscribers[event.event_type]]
            if coroutines:
                await asyncio.gather(*coroutines, return_exceptions=True)
        
        self._logger.debug(f"Event {event.event_id} processed successfully")
    
    def subscribe(self, event_type: EventType, handler: EventHandler) -> None:
        """Đăng ký một handler để nhận sự kiện có type cụ thể"""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        
        if handler not in self._subscribers[event_type]:
            self._subscribers[event_type].append(handler)
            self._logger.info(f"Handler {handler.__name__} subscribed to {event_type}")
    
    def unsubscribe(self, event_type: EventType, handler: EventHandler) -> None:
        """Hủy đăng ký một handler khỏi sự kiện có type cụ thể"""
        if event_type in self._subscribers and handler in self._subscribers[event_type]:
            self._subscribers[event_type].remove(handler)
            self._logger.info(f"Handler {handler.__name__} unsubscribed from {event_type}")
    
    def get_event_history(self, limit: int = 100, event_type: Optional[EventType] = None, 
                        entity_id: Optional[str] = None) -> List[SystemEvent]:
        """Lấy lịch sử sự kiện với các bộ lọc"""
        filtered_events = self._event_history
        
        if event_type:
            filtered_events = [e for e in filtered_events if e.event_type == event_type]
        
        if entity_id:
            filtered_events = [e for e in filtered_events if e.entity_id == entity_id]
        
        # Trả về các sự kiện mới nhất trước
        return list(reversed(filtered_events))[:limit]

# Singleton instance
system_event_bus = SystemEventBus()

# Các tiện ích helper
async def publish_event(event_type: EventType, 
                       source_agent_id: Optional[str] = None,
                       target_agent_ids: Optional[List[str]] = None,
                       entity_id: Optional[str] = None,
                       entity_type: Optional[str] = None,
                       data: Optional[Dict[str, Any]] = None,
                       metadata: Optional[Dict[str, Any]] = None) -> SystemEvent:
    """Helper function để dễ dàng đăng một sự kiện"""
    event = SystemEvent(
        event_type=event_type,
        source_agent_id=source_agent_id,
        target_agent_ids=target_agent_ids or [],
        entity_id=entity_id,
        entity_type=entity_type,
        data=data or {},
        metadata=metadata or {}
    )
    await system_event_bus.publish(event)
    return event
