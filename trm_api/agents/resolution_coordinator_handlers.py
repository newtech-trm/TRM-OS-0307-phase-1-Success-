import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

from trm_api.eventbus.system_event_bus import SystemEvent, EventType, publish_event

# Thiết lập logger
logger = logging.getLogger("resolution_coordinator_handlers")

# Các hàm xử lý sự kiện được tách riêng để giảm kích thước file chính
async def process_event_handler(agent, event: SystemEvent) -> None:
    """Xử lý các sự kiện nhận được"""
    if event.event_type == EventType.TENSION_CREATED:
        # Xử lý tension mới
        if event.entity_id:
            await start_resolution_process_handler(agent, event.entity_id)
    
    elif event.event_type == EventType.TENSION_UPDATED:
        # Cập nhật thông tin và trạng thái của tension
        if event.entity_id and event.entity_id in agent.active_tensions:
            await update_tension_status_handler(agent, event.entity_id, event.data)
    
    elif event.event_type == EventType.TASK_COMPLETED:
        # Cập nhật nhiệm vụ hoàn thành và kiểm tra tiến độ
        if "tension_id" in event.data and event.data["tension_id"] in agent.active_tensions:
            await process_completed_task_handler(agent, event.data["tension_id"], event.entity_id, event.data)
    
    elif event.event_type == EventType.KNOWLEDGE_CREATED:
        # Xử lý kiến thức mới được tạo liên quan đến tension
        if "related_tension_id" in event.data and event.data["related_tension_id"] in agent.active_tensions:
            await incorporate_knowledge_handler(agent, event.data["related_tension_id"], event.entity_id)

async def start_resolution_process_handler(agent, tension_id: str) -> None:
    """Bắt đầu quy trình giải quyết cho một tension mới"""
    try:
        # Lấy thông tin tension từ database
        tension = await agent.tension_repository.get_tension_by_uid(tension_id)
        if not tension:
            agent.logger.error(f"Cannot find tension with ID {tension_id}")
            return
        
        agent.logger.info(f"Starting resolution process for tension {tension_id}: {tension.title}")
        
        # Phân tích tension để xác định hướng giải quyết
        analysis_result = await analyze_tension_handler(agent, tension)
        priority = analysis_result.get("priority", "medium")
        tension_type = analysis_result.get("type", "general")
        
        # Lưu thông tin vào danh sách đang xử lý
        agent.active_tensions[tension_id] = {
            "tension": tension,
            "start_time": datetime.now(),
            "priority": priority,
            "type": tension_type,
            "status": "processing",
            "assigned_agents": []
        }
        
        # Tạo các nhiệm vụ cần thực hiện
        tasks = await create_resolution_tasks_handler(agent, tension, analysis_result)
        agent.pending_tasks[tension_id] = tasks
        
        # Cập nhật trạng thái tension
        await agent.tension_repository.update_tension_status(tension_id, "in_progress")
        
        # Gửi sự kiện để bắt đầu các nhiệm vụ
        for task in tasks:
            if "agent_type" in task:
                # Gửi nhiệm vụ cho loại agent phù hợp
                await agent.send_event(
                    event_type=EventType.TASK_CREATED,
                    target_agent_ids=[],  # Để trống để tất cả agent loại này đều nhận được
                    entity_id=tension_id,
                    entity_type="tension",
                    data={
                        "task_type": task["task_type"],
                        "tension_id": tension_id,
                        "priority": priority,
                        "agent_type": task["agent_type"],
                        "params": task.get("params", {})
                    }
                )
                agent.active_tensions[tension_id]["assigned_agents"].append(task["agent_type"])
        
        agent.logger.info(f"Resolution process started for tension {tension_id} with {len(tasks)} tasks")
        
    except Exception as e:
        agent.logger.error(f"Error starting resolution for tension {tension_id}: {str(e)}")
        # Cập nhật trạng thái lỗi
        await agent.send_event(
            event_type=EventType.AGENT_ERROR,
            entity_id=tension_id,
            entity_type="tension",
            data={"error": f"Failed to start resolution: {str(e)}"}
        )

async def analyze_tension_handler(agent, tension) -> Dict[str, Any]:
    """Phân tích tension để xác định loại và mức độ ưu tiên"""
    # Phân tích mức độ ưu tiên dựa trên các yếu tố như:
    # - Độ khẩn cấp (urgent flag)
    # - Tầm ảnh hưởng (scope)
    # - Tác động (impact)
    
    priority = "medium"  # Mặc định
    
    if hasattr(tension, "urgent") and tension.urgent:
        priority = "high"
    elif hasattr(tension, "impact") and tension.impact in ["high", "critical"]:
        priority = "high"
    elif hasattr(tension, "scope") and tension.scope == "organization":
        priority = "high"
    
    # Phân loại tension dựa vào nội dung và tags
    tension_type = "general"
    if hasattr(tension, "tags") and tension.tags:
        tags = tension.tags
        if any(tag in ["technical", "bug", "error"] for tag in tags):
            tension_type = "technical"
        elif any(tag in ["process", "workflow", "optimization"] for tag in tags):
            tension_type = "process"
        elif any(tag in ["knowledge", "information", "documentation"] for tag in tags):
            tension_type = "knowledge"
        elif any(tag in ["people", "team", "collaboration"] for tag in tags):
            tension_type = "people"
    
    return {
        "priority": priority,
        "type": tension_type,
        "requires_human": False,  # Mặc định không cần can thiệp của con người
        "estimated_complexity": "medium",
        "suggested_approaches": []
    }

async def create_resolution_tasks_handler(agent, tension, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Tạo các nhiệm vụ cần thiết để giải quyết tension"""
    tasks = []
    tension_type = analysis.get("type", "general")
    
    # Luôn cần phân tích tension chi tiết
    tasks.append({
        "task_type": "analyze_tension",
        "agent_type": "tension_resolution",
        "status": "pending",
        "params": {"detail_level": "high"}
    })
    
    # Tuỳ vào loại tension mà thêm các nhiệm vụ khác nhau
    if tension_type == "technical":
        tasks.append({
            "task_type": "technical_analysis",
            "agent_type": "technical_resolution",
            "status": "pending",
            "params": {}
        })
    elif tension_type == "knowledge":
        tasks.append({
            "task_type": "extract_knowledge",
            "agent_type": "knowledge_extraction",
            "status": "pending",
            "params": {}
        })
    elif tension_type == "process":
        tasks.append({
            "task_type": "process_improvement",
            "agent_type": "strategic_alignment",
            "status": "pending",
            "params": {}
        })
    
    # Thêm nhiệm vụ tạo giải pháp
    tasks.append({
        "task_type": "generate_solution",
        "agent_type": "proposal_generation",
        "status": "pending",
        "params": {"based_on_analysis": True}
    })
    
    return tasks

async def update_tension_status_handler(agent, tension_id: str, data: Dict[str, Any]) -> None:
    """Cập nhật trạng thái của tension"""
    if tension_id not in agent.active_tensions:
        return
        
    if "status" in data:
        agent.active_tensions[tension_id]["status"] = data["status"]
        
        # Nếu đã giải quyết, xử lý kết thúc quy trình
        if data["status"] == "resolved":
            await finalize_resolution_handler(agent, tension_id)

async def process_completed_task_handler(agent, tension_id: str, task_id: str, data: Dict[str, Any]) -> None:
    """Xử lý một nhiệm vụ đã hoàn thành"""
    if tension_id not in agent.pending_tasks or tension_id not in agent.active_tensions:
        return
        
    # Cập nhật trạng thái nhiệm vụ
    for task in agent.pending_tasks[tension_id]:
        if task.get("id") == task_id or task.get("task_type") == data.get("task_type"):
            task["status"] = "completed"
            task["result"] = data.get("result", {})
            break
            
    # Kiểm tra xem tất cả nhiệm vụ đã hoàn thành chưa
    all_completed = all(task["status"] == "completed" for task in agent.pending_tasks[tension_id])
    
    if all_completed:
        await integrate_solutions_handler(agent, tension_id)

async def incorporate_knowledge_handler(agent, tension_id: str, knowledge_id: str) -> None:
    """Tích hợp kiến thức mới vào quá trình giải quyết tension"""
    if tension_id not in agent.active_tensions:
        return
        
    agent.logger.info(f"Incorporating knowledge {knowledge_id} into tension {tension_id}")
    
    # Cập nhật thông tin tension với kiến thức mới
    if "knowledge" not in agent.active_tensions[tension_id]:
        agent.active_tensions[tension_id]["knowledge"] = []
        
    agent.active_tensions[tension_id]["knowledge"].append(knowledge_id)
    
    # Thông báo cho các agent đang xử lý về kiến thức mới
    for agent_type in agent.active_tensions[tension_id]["assigned_agents"]:
        await agent.send_event(
            event_type=EventType.KNOWLEDGE_VALIDATED,
            entity_id=knowledge_id,
            entity_type="knowledge_snippet",
            data={
                "tension_id": tension_id,
                "knowledge_id": knowledge_id,
                "agent_type": agent_type
            }
        )

async def integrate_solutions_handler(agent, tension_id: str) -> None:
    """Tích hợp các giải pháp từ các nhiệm vụ khác nhau"""
    agent.logger.info(f"Integrating solutions for tension {tension_id}")
    
    try:
        # Thu thập kết quả từ tất cả nhiệm vụ
        solutions = []
        for task in agent.pending_tasks[tension_id]:
            if task["status"] == "completed" and "result" in task:
                if "solution" in task["result"]:
                    solutions.append(task["result"]["solution"])
        
        # Tích hợp các giải pháp
        if solutions:
            # Tạo giải pháp tổng thể
            integrated_solution = {
                "description": "Giải pháp tích hợp từ nhiều agent",
                "steps": [],
                "expected_outcome": "",
                "contributors": agent.active_tensions[tension_id]["assigned_agents"]
            }
            
            # Tích hợp các bước từ các giải pháp
            for solution in solutions:
                if isinstance(solution, dict):
                    if "steps" in solution and isinstance(solution["steps"], list):
                        integrated_solution["steps"].extend(solution["steps"])
                    if "expected_outcome" in solution and solution["expected_outcome"]:
                        if integrated_solution["expected_outcome"]:
                            integrated_solution["expected_outcome"] += "\n\n"
                        integrated_solution["expected_outcome"] += solution["expected_outcome"]
            
            # Áp dụng giải pháp
            await apply_solution_handler(agent, tension_id, integrated_solution)
        else:
            agent.logger.warning(f"No solutions found for tension {tension_id}")
            # Tạo một giải pháp mặc định hoặc báo cáo lỗi
            await escalate_tension_handler(agent, tension_id)
    except Exception as e:
        agent.logger.error(f"Error integrating solutions for tension {tension_id}: {str(e)}")
        await escalate_tension_handler(agent, tension_id)

async def apply_solution_handler(agent, tension_id: str, solution: Dict[str, Any]) -> None:
    """Áp dụng giải pháp cho tension"""
    agent.logger.info(f"Applying solution to tension {tension_id}")
    
    # Cập nhật trạng thái tension với giải pháp
    await agent.tension_repository.update_tension(
        tension_id,
        {
            "resolution": solution.get("description", ""),
            "resolution_steps": solution.get("steps", []),
            "status": "resolved",
            "resolved_at": datetime.now()
        }
    )
    
    # Tạo sự kiện WIN nếu giải pháp thành công
    await agent.send_event(
        event_type=EventType.WIN_CREATED,
        entity_id=tension_id,
        entity_type="tension",
        data={
            "description": f"Successfully resolved tension: {agent.active_tensions[tension_id]['tension'].title}",
            "impact": "positive",
            "resolution": solution.get("description", "")
        }
    )
    
    # Tạo sự kiện tension đã giải quyết
    await agent.send_event(
        event_type=EventType.TENSION_RESOLVED,
        entity_id=tension_id,
        entity_type="tension",
        data={
            "resolution": solution.get("description", ""),
            "resolved_by": agent.agent_id
        }
    )
    
    # Đánh dấu tension đã giải quyết
    await finalize_resolution_handler(agent, tension_id)

async def finalize_resolution_handler(agent, tension_id: str) -> None:
    """Hoàn tất quá trình giải quyết tension"""
    if tension_id not in agent.active_tensions:
        return
        
    agent.logger.info(f"Finalizing resolution for tension {tension_id}")
    
    # Xóa khỏi danh sách đang xử lý
    if tension_id in agent.active_tensions:
        del agent.active_tensions[tension_id]
    
    # Xóa các nhiệm vụ đang chờ
    if tension_id in agent.pending_tasks:
        del agent.pending_tasks[tension_id]

async def escalate_tension_handler(agent, tension_id: str) -> None:
    """Leo thang tension khi không thể giải quyết tự động"""
    agent.logger.warning(f"Escalating tension {tension_id}")
    
    try:
        # Cập nhật trạng thái tension
        await agent.tension_repository.update_tension(
            tension_id,
            {
                "status": "escalated",
                "escalated_at": datetime.now(),
                "escalated_reason": "Automatic resolution failed or timeout reached"
            }
        )
        
        # Gửi sự kiện leo thang
        await agent.send_event(
            event_type=EventType.TENSION_UPDATED,
            entity_id=tension_id,
            entity_type="tension",
            data={
                "status": "escalated",
                "requires_human": True,
                "reason": "Automatic resolution failed or timeout reached"
            }
        )
        
        # Đánh dấu là đã xử lý
        await finalize_resolution_handler(agent, tension_id)
        
    except Exception as e:
        agent.logger.error(f"Error escalating tension {tension_id}: {str(e)}")
