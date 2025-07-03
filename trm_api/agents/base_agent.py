import asyncio
import logging
from typing import Dict, List, Any, Optional, Set, Tuple
from datetime import datetime
from abc import ABC, abstractmethod
from pydantic import BaseModel

from trm_api.eventbus.system_event_bus import SystemEventBus, SystemEvent, EventType, publish_event
from trm_api.repositories.agent_repository import AgentRepository
from trm_api.graph_models.agent import Agent as GraphAgent

class AgentMetadata(BaseModel):
    """Metadata cho một AI Agent"""
    name: str
    agent_type: str
    description: str
    capabilities: List[str] = []
    status: str = "active"
    version: str = "1.0.0"
    created_by: Optional[str] = None
    creation_date: datetime = None

class BaseAgent(ABC):
    """Base class cho tất cả AI Agent trong TRM-OS"""
    
    def __init__(self, agent_id: Optional[str] = None, metadata: Optional[AgentMetadata] = None):
        self.agent_id = agent_id
        self.metadata = metadata
        self.event_bus = SystemEventBus()
        self.repository = AgentRepository()
        self.logger = logging.getLogger(f"agent.{self.__class__.__name__}")
        self._subscribed_events: Set[EventType] = set()
        self._is_running = False
    
    async def initialize(self) -> None:
        """Khởi tạo agent, đăng ký với database nếu chưa tồn tại"""
        try:
            if self.agent_id:
                # Nếu có agent_id, tải từ database
                agent_data = await self.repository.get_agent_by_uid(self.agent_id)
                if agent_data:
                    self.metadata = AgentMetadata(
                        name=agent_data.name,
                        agent_type=agent_data.agent_type,
                        description=agent_data.description,
                        status=agent_data.status,
                        capabilities=agent_data.capabilities if hasattr(agent_data, 'capabilities') else [],
                        version=agent_data.version if hasattr(agent_data, 'version') else "1.0.0",
                        created_by=agent_data.created_by if hasattr(agent_data, 'created_by') else None,
                        creation_date=agent_data.creation_date
                    )
                else:
                    # Không tìm thấy agent với ID cung cấp
                    self.logger.warning(f"Agent with ID {self.agent_id} not found")
                    return
            elif self.metadata:
                # Nếu không có agent_id nhưng có metadata, tạo mới trong database
                from trm_api.models.agent import AgentCreate
                
                # Tìm kiếm agent theo tên trước khi tạo mới
                existing_agent = await self.repository.get_agent_by_name(self.metadata.name)
                if existing_agent:
                    self.agent_id = existing_agent.uid
                    self.logger.info(f"Using existing agent with ID {self.agent_id}")
                else:
                    # Tạo mới
                    agent_create = AgentCreate(
                        name=self.metadata.name,
                        agent_type=self.metadata.agent_type,
                        description=self.metadata.description,
                        status=self.metadata.status,
                        capabilities=self.metadata.capabilities,
                        version=self.metadata.version,
                        created_by=self.metadata.created_by
                    )
                    agent = await self.repository.create_agent(agent_create)
                    self.agent_id = agent.uid
                    self.logger.info(f"Created new agent with ID {self.agent_id}")
            else:
                self.logger.error("Cannot initialize agent without ID or metadata")
                return
            
            # Đăng ký các event handlers
            await self._register_event_handlers()
            
            # Đăng sự kiện agent được kích hoạt
            await publish_event(
                event_type=EventType.AGENT_ACTIVATED,
                source_agent_id=self.agent_id,
                entity_id=self.agent_id,
                entity_type="agent",
                data={"name": self.metadata.name, "type": self.metadata.agent_type}
            )
            
            self.logger.info(f"Agent {self.metadata.name} initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Error initializing agent: {str(e)}")
            # Đăng sự kiện lỗi
            await publish_event(
                event_type=EventType.AGENT_ERROR,
                source_agent_id=self.agent_id if self.agent_id else None,
                entity_id=self.agent_id if self.agent_id else None,
                entity_type="agent",
                data={"error": str(e)}
            )
    
    async def start(self) -> None:
        """Bắt đầu hoạt động của agent"""
        if self._is_running:
            self.logger.warning("Agent is already running")
            return
        
        self._is_running = True
        self.logger.info(f"Agent {self.metadata.name} started")
        
        # Triển khai logic cụ thể trong các lớp con
        await self._start_processing()
    
    async def stop(self) -> None:
        """Dừng hoạt động của agent"""
        if not self._is_running:
            self.logger.warning("Agent is not running")
            return
        
        self._is_running = False
        
        # Hủy đăng ký các event handlers
        await self._unregister_event_handlers()
        
        # Đăng sự kiện agent bị vô hiệu hóa
        await publish_event(
            event_type=EventType.AGENT_DEACTIVATED,
            source_agent_id=self.agent_id,
            entity_id=self.agent_id,
            entity_type="agent",
            data={"name": self.metadata.name, "type": self.metadata.agent_type}
        )
        
        self.logger.info(f"Agent {self.metadata.name} stopped")
    
    async def handle_event(self, event: SystemEvent) -> None:
        """Xử lý sự kiện từ SystemEventBus"""
        self.logger.debug(f"Received event: {event.event_type} - {event.event_id}")
        
        # Gọi method xử lý tương ứng với loại sự kiện
        await self._process_event(event)
    
    async def send_event(self, event_type: EventType, target_agent_ids: Optional[List[str]] = None, 
                      data: Optional[Dict[str, Any]] = None, entity_id: Optional[str] = None,
                      entity_type: Optional[str] = None) -> None:
        """Gửi một sự kiện mới thông qua SystemEventBus"""
        await publish_event(
            event_type=event_type,
            source_agent_id=self.agent_id,
            target_agent_ids=target_agent_ids,
            entity_id=entity_id,
            entity_type=entity_type,
            data=data or {}
        )
    
    @abstractmethod
    async def _register_event_handlers(self) -> None:
        """Đăng ký các event handlers - được triển khai trong lớp con"""
        pass
    
    async def _unregister_event_handlers(self) -> None:
        """Hủy đăng ký tất cả event handlers"""
        for event_type in self._subscribed_events:
            self.event_bus.unsubscribe(event_type, self.handle_event)
        
        self._subscribed_events.clear()
    
    @abstractmethod
    async def _start_processing(self) -> None:
        """Bắt đầu xử lý logic của agent - được triển khai trong lớp con"""
        pass
    
    @abstractmethod
    async def _process_event(self, event: SystemEvent) -> None:
        """Xử lý sự kiện cụ thể - được triển khai trong lớp con"""
        pass

    def subscribe_to_event(self, event_type: EventType) -> None:
        """Đăng ký nhận một loại sự kiện cụ thể"""
        if event_type not in self._subscribed_events:
            self.event_bus.subscribe(event_type, self.handle_event)
            self._subscribed_events.add(event_type)
            self.logger.debug(f"Subscribed to event: {event_type}")
            
    async def execute_task(self, task_type: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Thực hiện một nhiệm vụ cụ thể - được ghi đè trong lớp con"""
        self.logger.warning(f"Task type '{task_type}' not implemented by {self.__class__.__name__}")
        return {"status": "error", "message": f"Task type '{task_type}' not implemented"}
