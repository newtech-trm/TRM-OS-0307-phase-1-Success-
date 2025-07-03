import asyncio
import logging
from typing import Dict, List, Any, Optional, Set
from datetime import datetime

from trm_api.agents.base_agent import BaseAgent, AgentMetadata
from trm_api.eventbus.system_event_bus import SystemEvent, EventType
from trm_api.repositories.tension_repository import TensionRepository

class ResolutionCoordinatorAgent(BaseAgent):
    """ResolutionCoordinatorAgent là agent trung tâm chịu trách nhiệm điều phối quá trình 
    giải quyết các Tension trong TRM-OS theo Ontology V3.2.
    
    Agent này có các chức năng chính:
    1. Phân tích Tension mới được tạo để xác định loại và mức độ ưu tiên
    2. Gửi Tension đến các agent chuyên biệt để xử lý
    3. Theo dõi trạng thái và quá trình giải quyết Tension
    4. Kết hợp dữ liệu từ các agent khác để tạo giải pháp tổng thể
    5. Báo cáo kết quả và cập nhật trạng thái Tension
    """
    
    def __init__(self, agent_id: Optional[str] = None):
        metadata = AgentMetadata(
            name="ResolutionCoordinatorAgent",
            agent_type="coordinator",
            description="Điều phối quá trình giải quyết các Tension trong hệ thống TRM-OS",
            capabilities=[
                "tension_analysis", 
                "priority_assessment", 
                "task_delegation", 
                "process_coordination", 
                "solution_integration"
            ],
            status="active",
            version="1.0.0"
        )
        super().__init__(agent_id=agent_id, metadata=metadata)
        self.tension_repository = TensionRepository()
        self.active_tensions: Dict[str, Dict[str, Any]] = {}  # Lưu trữ các tension đang xử lý
        self.pending_tasks: Dict[str, List[Dict[str, Any]]] = {}  # Các nhiệm vụ đang chờ xử lý cho mỗi tension
    
    async def _register_event_handlers(self) -> None:
        """Đăng ký lắng nghe các sự kiện liên quan đến Tension"""
        self.subscribe_to_event(EventType.TENSION_CREATED)
        self.subscribe_to_event(EventType.TENSION_UPDATED)
        self.subscribe_to_event(EventType.TASK_COMPLETED)
        self.subscribe_to_event(EventType.KNOWLEDGE_CREATED)
    
    async def _start_processing(self) -> None:
        """Bắt đầu hoạt động của agent, quét các tension chưa xử lý"""
        self.logger.info("ResolutionCoordinatorAgent starting processing")
        
        # Tải các tension chưa giải quyết từ database
        try:
            unresolved_tensions = await self.tension_repository.get_unresolved_tensions()
            self.logger.info(f"Found {len(unresolved_tensions)} unresolved tensions")
            
            for tension in unresolved_tensions:
                # Chỉ xử lý các tension chưa được điều phối
                if tension.status == "new" or tension.status == "open":
                    await self._start_resolution_process(tension.uid)
        except Exception as e:
            self.logger.error(f"Error loading unresolved tensions: {str(e)}")
            
        # Bắt đầu vòng lặp kiểm tra định kỳ
        asyncio.create_task(self._periodic_check())
    
    async def _periodic_check(self) -> None:
        """Kiểm tra định kỳ trạng thái của các tension đang xử lý"""
        while self._is_running:
            await asyncio.sleep(300)  # Kiểm tra 5 phút một lần
            
            # Kiểm tra các tension đang xử lý
            for tension_id in list(self.active_tensions.keys()):
                try:
                    # Cập nhật trạng thái từ database
                    tension = await self.tension_repository.get_tension_by_uid(tension_id)
                    if not tension:
                        # Tension không còn tồn tại
                        del self.active_tensions[tension_id]
                        if tension_id in self.pending_tasks:
                            del self.pending_tasks[tension_id]
                        continue
                        
                    if tension.status == "resolved":
                        # Tension đã được giải quyết
                        self.logger.info(f"Tension {tension_id} has been resolved")
                        del self.active_tensions[tension_id]
                        if tension_id in self.pending_tasks:
                            del self.pending_tasks[tension_id]
                    else:
                        # Kiểm tra xem có cần can thiệp không
                        elapsed_time = (datetime.now() - self.active_tensions[tension_id]["start_time"]).total_seconds() / 3600
                        if elapsed_time > 48:  # Nếu đã quá 48 giờ
                            self.logger.warning(f"Tension {tension_id} has been active for over 48 hours")
                            # Cân nhắc can thiệp hoặc leo thang
                            await self._escalate_tension(tension_id)
                except Exception as e:
                    self.logger.error(f"Error checking tension {tension_id}: {str(e)}")
    
    # Phần còn lại của các phương thức sẽ được triển khai trong resolution_coordinator_handlers.py
    
    # Các phương thức phụ thuộc vẫn được khai báo sơ bộ để đảm bảo tính toàn vẹn của class
    async def _process_event(self, event: SystemEvent) -> None:
        """Xử lý các sự kiện nhận được - được triển khai trong handlers"""
        from trm_api.agents.resolution_coordinator_handlers import process_event_handler
        await process_event_handler(self, event)
    
    async def _start_resolution_process(self, tension_id: str) -> None:
        """Bắt đầu quy trình giải quyết cho một tension mới - được triển khai trong handlers"""
        from trm_api.agents.resolution_coordinator_handlers import start_resolution_process_handler
        await start_resolution_process_handler(self, tension_id)
        
    async def _analyze_tension(self, tension) -> Dict[str, Any]:
        """Phân tích tension để xác định loại và mức độ ưu tiên - được triển khai trong handlers"""
        from trm_api.agents.resolution_coordinator_handlers import analyze_tension_handler
        return await analyze_tension_handler(self, tension)
        
    async def _create_resolution_tasks(self, tension, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Tạo các nhiệm vụ cần thiết để giải quyết tension - được triển khai trong handlers"""
        from trm_api.agents.resolution_coordinator_handlers import create_resolution_tasks_handler
        return await create_resolution_tasks_handler(self, tension, analysis)
        
    async def _update_tension_status(self, tension_id: str, data: Dict[str, Any]) -> None:
        """Cập nhật trạng thái của tension - được triển khai trong handlers"""
        from trm_api.agents.resolution_coordinator_handlers import update_tension_status_handler
        await update_tension_status_handler(self, tension_id, data)
        
    async def _process_completed_task(self, tension_id: str, task_id: str, data: Dict[str, Any]) -> None:
        """Xử lý một nhiệm vụ đã hoàn thành - được triển khai trong handlers"""
        from trm_api.agents.resolution_coordinator_handlers import process_completed_task_handler
        await process_completed_task_handler(self, tension_id, task_id, data)
        
    async def _incorporate_knowledge(self, tension_id: str, knowledge_id: str) -> None:
        """Tích hợp kiến thức mới vào quá trình giải quyết tension - được triển khai trong handlers"""
        from trm_api.agents.resolution_coordinator_handlers import incorporate_knowledge_handler
        await incorporate_knowledge_handler(self, tension_id, knowledge_id)
        
    async def _integrate_solutions(self, tension_id: str) -> None:
        """Tích hợp các giải pháp từ các nhiệm vụ khác nhau - được triển khai trong handlers"""
        from trm_api.agents.resolution_coordinator_handlers import integrate_solutions_handler
        await integrate_solutions_handler(self, tension_id)
        
    async def _apply_solution(self, tension_id: str, solution: Dict[str, Any]) -> None:
        """Áp dụng giải pháp cho tension - được triển khai trong handlers"""
        from trm_api.agents.resolution_coordinator_handlers import apply_solution_handler
        await apply_solution_handler(self, tension_id, solution)
        
    async def _finalize_resolution(self, tension_id: str) -> None:
        """Hoàn tất quá trình giải quyết tension - được triển khai trong handlers"""
        from trm_api.agents.resolution_coordinator_handlers import finalize_resolution_handler
        await finalize_resolution_handler(self, tension_id)
        
    async def _escalate_tension(self, tension_id: str) -> None:
        """Leo thang tension khi không thể giải quyết tự động - được triển khai trong handlers"""
        from trm_api.agents.resolution_coordinator_handlers import escalate_tension_handler
        await escalate_tension_handler(self, tension_id)
