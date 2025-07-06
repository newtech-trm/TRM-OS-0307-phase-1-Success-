"""
Base Agent Template

Lớp cơ sở cho tất cả agent templates trong TRM-OS Genesis Engine.
Định nghĩa interface và functionality chung cho việc tạo và quản lý specialized agents.
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional, Type
from abc import ABC, abstractmethod
from datetime import datetime
from pydantic import BaseModel

from ..base_agent import BaseAgent, AgentMetadata
from ...eventbus.system_event_bus import EventType, SystemEvent
from ...models.tension import Tension
from ...reasoning.tension_analyzer import TensionAnalyzer
from ...reasoning.solution_generator import SolutionGenerator


class AgentCapability(BaseModel):
    """Định nghĩa một capability của agent"""
    name: str
    description: str
    required_skills: List[str] = []
    complexity_level: int = 1  # 1-5, 5 là phức tạp nhất
    estimated_time: Optional[int] = None  # Thời gian ước tính (phút)
    
    @property
    def estimated_time_per_task(self) -> Optional[int]:
        """Compatibility property for estimated_time"""
        return self.estimated_time


class AgentTemplateMetadata(BaseModel):
    """Metadata cho agent template"""
    template_name: str
    template_version: str = "1.0.0"
    description: str
    primary_domain: str  # Lĩnh vực chính (data, code, ui, integration, research)
    capabilities: List[AgentCapability]
    recommended_tensions: List[str] = []  # Các loại tension phù hợp
    dependencies: List[str] = []  # Dependencies với templates khác
    performance_metrics: List[str] = []  # Metrics để đánh giá performance
    
    @property
    def name(self) -> str:
        """Compatibility property for template_name"""
        return self.template_name


class BaseAgentTemplate(BaseAgent, ABC):
    """
    Base class cho tất cả agent templates trong TRM-OS.
    
    Mỗi template định nghĩa:
    - Capabilities cụ thể cho domain
    - Logic xử lý tensions chuyên biệt
    - Patterns tạo solutions
    - Performance metrics
    """
    
    def __init__(self, agent_id: Optional[str] = None, metadata: Optional[AgentMetadata] = None,
                 template_metadata: Optional[AgentTemplateMetadata] = None):
        super().__init__(agent_id, metadata)
        self.template_metadata = template_metadata or self._get_default_template_metadata()
        self.tension_analyzer = TensionAnalyzer()
        self.solution_generator = SolutionGenerator()
        self.active_tensions: Dict[str, Tension] = {}
        self.completed_tasks: List[Dict[str, Any]] = []
        self.performance_stats = {
            "tensions_processed": 0,
            "solutions_generated": 0,
            "success_rate": 0.0,
            "average_resolution_time": 0.0
        }
    
    @abstractmethod
    def _get_default_template_metadata(self) -> AgentTemplateMetadata:
        """Trả về metadata mặc định cho template - phải được implement trong subclass"""
        pass
    
    @abstractmethod
    async def can_handle_tension(self, tension: Tension) -> bool:
        """
        Kiểm tra xem agent template này có thể xử lý tension không.
        
        Args:
            tension: Tension cần kiểm tra
            
        Returns:
            True nếu có thể xử lý, False nếu không
        """
        pass
    
    @abstractmethod
    async def analyze_tension_requirements(self, tension: Tension) -> Dict[str, Any]:
        """
        Phân tích tension để xác định requirements cụ thể.
        
        Args:
            tension: Tension cần phân tích
            
        Returns:
            Dictionary chứa requirements và recommendations
        """
        pass
    
    @abstractmethod
    async def generate_specialized_solutions(self, tension: Tension, 
                                           requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Tạo solutions chuyên biệt cho tension dựa trên template domain.
        
        Args:
            tension: Tension cần giải quyết
            requirements: Requirements đã phân tích
            
        Returns:
            List các solutions chuyên biệt
        """
        pass
    
    @abstractmethod
    async def execute_solution(self, solution: Dict[str, Any], 
                             context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Thực thi một solution cụ thể.
        
        Args:
            solution: Solution cần thực thi
            context: Context thực thi
            
        Returns:
            Kết quả thực thi
        """
        pass
    
    async def _register_event_handlers(self) -> None:
        """Đăng ký các event handlers cho template"""
        # Đăng ký các events cơ bản
        self.subscribe_to_event(EventType.TENSION_CREATED)
        self.subscribe_to_event(EventType.TENSION_UPDATED)
        self.subscribe_to_event(EventType.TASK_CREATED)
        
        # Đăng ký các events chuyên biệt cho template
        await self._register_specialized_handlers()
    
    @abstractmethod
    async def _register_specialized_handlers(self) -> None:
        """Đăng ký các event handlers chuyên biệt cho template"""
        pass
    
    async def _start_processing(self) -> None:
        """Bắt đầu processing loop của agent template"""
        self.logger.info(f"Starting {self.template_metadata.template_name} processing")
        
        # Khởi tạo các components cần thiết
        await self._initialize_specialized_components()
        
        # Bắt đầu monitoring loop
        asyncio.create_task(self._monitoring_loop())
    
    @abstractmethod
    async def _initialize_specialized_components(self) -> None:
        """Khởi tạo các components chuyên biệt cho template"""
        pass
    
    async def _process_event(self, event: SystemEvent) -> None:
        """Xử lý sự kiện từ SystemEventBus"""
        try:
            if event.event_type == EventType.TENSION_CREATED:
                await self._handle_tension_created(event)
            elif event.event_type == EventType.TENSION_UPDATED:
                await self._handle_tension_updated(event)
            elif event.event_type == EventType.TASK_CREATED:
                await self._handle_task_created(event)
            else:
                # Gọi handler chuyên biệt
                await self._handle_specialized_event(event)
                
        except Exception as e:
            self.logger.error(f"Error processing event {event.event_type}: {str(e)}")
    
    async def _handle_tension_created(self, event: SystemEvent) -> None:
        """Xử lý sự kiện tension được tạo"""
        try:
            tension_id = event.entity_id
            if not tension_id:
                return
            
            # Load tension data (giả sử có service để load)
            # tension = await self._load_tension(tension_id)
            # 
            # if await self.can_handle_tension(tension):
            #     await self._process_tension(tension)
            
            self.logger.info(f"Tension {tension_id} evaluated for handling")
            
        except Exception as e:
            self.logger.error(f"Error handling tension created event: {str(e)}")
    
    async def _handle_tension_updated(self, event: SystemEvent) -> None:
        """Xử lý sự kiện tension được cập nhật"""
        tension_id = event.entity_id
        if tension_id in self.active_tensions:
            # Cập nhật tension và re-evaluate
            self.logger.info(f"Re-evaluating updated tension {tension_id}")
    
    async def _handle_task_created(self, event: SystemEvent) -> None:
        """Xử lý sự kiện task được tạo"""
        task_id = event.entity_id
        self.logger.info(f"New task {task_id} available for processing")
    
    @abstractmethod
    async def _handle_specialized_event(self, event: SystemEvent) -> None:
        """Xử lý các sự kiện chuyên biệt cho template"""
        pass
    
    async def _process_tension(self, tension: Tension) -> None:
        """Xử lý một tension cụ thể"""
        start_time = datetime.now()
        
        try:
            # Phân tích requirements
            requirements = await self.analyze_tension_requirements(tension)
            
            # Tạo solutions
            solutions = await self.generate_specialized_solutions(tension, requirements)
            
            # Lưu tension vào active list
            self.active_tensions[tension.uid] = tension
            
            # Cập nhật performance stats
            self.performance_stats["tensions_processed"] += 1
            self.performance_stats["solutions_generated"] += len(solutions)
            
            # Gửi event về solutions được tạo
            await self.send_event(
                event_type=EventType.AGENT_TASK_COMPLETED,
                entity_id=tension.uid,
                entity_type="tension",
                data={
                    "agent_template": self.template_metadata.template_name,
                    "solutions_count": len(solutions),
                    "processing_time": (datetime.now() - start_time).total_seconds()
                }
            )
            
            self.logger.info(f"Processed tension {tension.uid} with {len(solutions)} solutions")
            
        except Exception as e:
            self.logger.error(f"Error processing tension {tension.uid}: {str(e)}")
    
    async def _monitoring_loop(self) -> None:
        """Loop monitoring performance và health của agent"""
        while self._is_running:
            try:
                await self._update_performance_metrics()
                await self._health_check()
                await asyncio.sleep(60)  # Check every minute
                
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {str(e)}")
                await asyncio.sleep(30)  # Shorter sleep on error
    
    async def _update_performance_metrics(self) -> None:
        """Cập nhật performance metrics"""
        if self.performance_stats["tensions_processed"] > 0:
            # Calculate success rate based on completed tasks
            completed_count = len(self.completed_tasks)
            self.performance_stats["success_rate"] = completed_count / self.performance_stats["tensions_processed"]
            
            # Calculate average resolution time
            if self.completed_tasks:
                total_time = sum(task.get("resolution_time", 0) for task in self.completed_tasks)
                self.performance_stats["average_resolution_time"] = total_time / len(self.completed_tasks)
    
    async def _health_check(self) -> None:
        """Kiểm tra health của agent template"""
        health_status = {
            "template_name": self.template_metadata.template_name,
            "is_running": self._is_running,
            "active_tensions": len(self.active_tensions),
            "performance_stats": self.performance_stats,
            "last_check": datetime.now().isoformat()
        }
        
        # Log health status
        self.logger.debug(f"Health check: {health_status}")
        
        # Gửi health event nếu cần
        if self.performance_stats["success_rate"] < 0.5 and self.performance_stats["tensions_processed"] > 10:
            await self.send_event(
                event_type=EventType.AGENT_ERROR,
                entity_id=self.agent_id,
                entity_type="agent",
                data={"health_warning": "Low success rate detected"}
            )
    
    def get_template_info(self) -> Dict[str, Any]:
        """Trả về thông tin về template"""
        return {
            "template_name": self.template_metadata.template_name,
            "template_version": self.template_metadata.template_version,
            "description": self.template_metadata.description,
            "primary_domain": self.template_metadata.primary_domain,
            "capabilities": [cap.dict() for cap in self.template_metadata.capabilities],
            "performance_stats": self.performance_stats,
            "active_tensions": len(self.active_tensions)
        } 