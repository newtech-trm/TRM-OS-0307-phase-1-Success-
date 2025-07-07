"""
TRM-OS Agent Ecosystem API Endpoints
===================================

REST API endpoints cho Agent Ecosystem management
với specialized agent coordination và task routing
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from uuid import uuid4
from pydantic import BaseModel, Field

from trm_api.agents.ecosystem.ecosystem_manager import (
    AgentEcosystemManager, EcosystemTask, TaskPriority, TaskStatus
)
from trm_api.agents.ecosystem.specialized_agents import AgentSpecialization
from trm_api.core.dependencies import get_current_user

router = APIRouter(prefix="/agent-ecosystem", tags=["Agent Ecosystem"])

# Global ecosystem manager (initialized on startup)
ecosystem_manager: Optional[AgentEcosystemManager] = None


# Pydantic models for API
class TaskCreateRequest(BaseModel):
    """Request model for creating ecosystem task"""
    task_type: str = Field(..., description="Type of task to execute")
    description: str = Field(..., description="Task description")
    required_specializations: List[str] = Field(..., description="Required agent specializations")
    priority: str = Field(default="medium", description="Task priority (critical, high, medium, low, background)")
    deadline: Optional[datetime] = Field(None, description="Task deadline")
    context: Dict[str, Any] = Field(default_factory=dict, description="Additional task context")


class TaskResponse(BaseModel):
    """Response model for task information"""
    task_id: str
    task_type: str
    description: str
    required_specializations: List[str]
    priority: str
    status: str
    assigned_agents: List[str]
    primary_agent: Optional[str]
    created_at: datetime
    assigned_at: Optional[datetime]
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    execution_results: Dict[str, Any]
    success_rate: float


class AgentStatusResponse(BaseModel):
    """Response model for agent status"""
    agent_id: str
    name: str
    specialization: str
    capabilities_count: int
    current_workload: int
    max_concurrent_tasks: int
    availability_score: float
    success_rate: float
    tasks_completed: int
    tasks_failed: int
    average_completion_time: float


class EcosystemStatusResponse(BaseModel):
    """Response model for ecosystem status"""
    system_id: str
    is_running: bool
    total_agents: int
    total_tasks: int
    pending_tasks: int
    in_progress_tasks: int
    completed_tasks: int
    failed_tasks: int
    queue_length: int
    active_tasks: int
    agent_utilization: float
    average_task_completion_time: float
    collaboration_efficiency: float


async def get_ecosystem_manager() -> AgentEcosystemManager:
    """Get ecosystem manager instance"""
    global ecosystem_manager
    if ecosystem_manager is None:
        ecosystem_manager = AgentEcosystemManager()
        await ecosystem_manager.initialize()
    return ecosystem_manager


@router.post("/tasks", response_model=Dict[str, str])
async def create_task(
    task_request: TaskCreateRequest,
    background_tasks: BackgroundTasks,
    ecosystem: AgentEcosystemManager = Depends(get_ecosystem_manager),
    current_user: Dict = Depends(get_current_user)
):
    """
    Create new task trong Agent Ecosystem
    """
    try:
        # Validate specializations
        specializations = []
        for spec_str in task_request.required_specializations:
            try:
                spec = AgentSpecialization(spec_str)
                specializations.append(spec)
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid specialization: {spec_str}"
                )
        
        # Validate priority
        priority_map = {
            "critical": TaskPriority.CRITICAL,
            "high": TaskPriority.HIGH,
            "medium": TaskPriority.MEDIUM,
            "low": TaskPriority.LOW,
            "background": TaskPriority.BACKGROUND
        }
        
        priority = priority_map.get(task_request.priority.lower(), TaskPriority.MEDIUM)
        
        # Create task
        task = EcosystemTask(
            task_id=str(uuid4()),
            task_type=task_request.task_type,
            description=task_request.description,
            required_specializations=specializations,
            priority=priority,
            deadline=task_request.deadline,
            context={
                **task_request.context,
                "created_by": current_user.get("user_id", "unknown"),
                "api_version": "v1"
            }
        )
        
        # Submit task
        task_id = await ecosystem.submit_task(task)
        
        return {
            "task_id": task_id,
            "status": "submitted",
            "message": "Task submitted successfully to Agent Ecosystem"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create task: {str(e)}")


@router.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: str,
    ecosystem: AgentEcosystemManager = Depends(get_ecosystem_manager),
    current_user: Dict = Depends(get_current_user)
):
    """
    Get task details by ID
    """
    if task_id not in ecosystem.tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task = ecosystem.tasks[task_id]
    
    return TaskResponse(
        task_id=task.task_id,
        task_type=task.task_type,
        description=task.description,
        required_specializations=[spec.value for spec in task.required_specializations],
        priority=task.priority.name.lower(),
        status=task.status.value,
        assigned_agents=task.assigned_agents,
        primary_agent=task.primary_agent,
        created_at=task.created_at,
        assigned_at=task.assigned_at,
        started_at=task.started_at,
        completed_at=task.completed_at,
        execution_results=task.execution_results,
        success_rate=task.success_rate
    )


@router.get("/tasks", response_model=List[TaskResponse])
async def list_tasks(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    ecosystem: AgentEcosystemManager = Depends(get_ecosystem_manager),
    current_user: Dict = Depends(get_current_user)
):
    """
    List tasks với filtering options
    """
    tasks = list(ecosystem.tasks.values())
    
    # Filter by status
    if status:
        try:
            status_enum = TaskStatus(status.lower())
            tasks = [task for task in tasks if task.status == status_enum]
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid status: {status}")
    
    # Filter by priority
    if priority:
        try:
            priority_enum = TaskPriority[priority.upper()]
            tasks = [task for task in tasks if task.priority == priority_enum]
        except KeyError:
            raise HTTPException(status_code=400, detail=f"Invalid priority: {priority}")
    
    # Sort by created_at descending
    tasks.sort(key=lambda x: x.created_at, reverse=True)
    
    # Apply pagination
    paginated_tasks = tasks[offset:offset + limit]
    
    return [
        TaskResponse(
            task_id=task.task_id,
            task_type=task.task_type,
            description=task.description,
            required_specializations=[spec.value for spec in task.required_specializations],
            priority=task.priority.name.lower(),
            status=task.status.value,
            assigned_agents=task.assigned_agents,
            primary_agent=task.primary_agent,
            created_at=task.created_at,
            assigned_at=task.assigned_at,
            started_at=task.started_at,
            completed_at=task.completed_at,
            execution_results=task.execution_results,
            success_rate=task.success_rate
        )
        for task in paginated_tasks
    ]


@router.delete("/tasks/{task_id}")
async def cancel_task(
    task_id: str,
    ecosystem: AgentEcosystemManager = Depends(get_ecosystem_manager),
    current_user: Dict = Depends(get_current_user)
):
    """
    Cancel pending task
    """
    if task_id not in ecosystem.tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task = ecosystem.tasks[task_id]
    
    if task.status not in [TaskStatus.PENDING, TaskStatus.ASSIGNED]:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot cancel task with status: {task.status.value}"
        )
    
    task.status = TaskStatus.CANCELLED
    
    # Remove from queue if pending
    if task_id in ecosystem.task_queue:
        ecosystem.task_queue.remove(task_id)
    
    return {"message": "Task cancelled successfully"}


@router.get("/agents", response_model=List[AgentStatusResponse])
async def list_agents(
    specialization: Optional[str] = None,
    ecosystem: AgentEcosystemManager = Depends(get_ecosystem_manager),
    current_user: Dict = Depends(get_current_user)
):
    """
    List all agents trong ecosystem
    """
    agents = []
    
    for agent_id, agent in ecosystem.agents.items():
        metrics = ecosystem.performance_metrics.get(agent_id)
        
        # Filter by specialization if specified
        if specialization and agent.specialization.value != specialization:
            continue
        
        agent_status = AgentStatusResponse(
            agent_id=agent.agent_id,
            name=agent.name,
            specialization=agent.specialization.value,
            capabilities_count=len(agent.capabilities),
            current_workload=metrics.current_workload if metrics else 0,
            max_concurrent_tasks=metrics.max_concurrent_tasks if metrics else 5,
            availability_score=metrics.availability_score if metrics else 1.0,
            success_rate=metrics.success_rate if metrics else 0.0,
            tasks_completed=metrics.tasks_completed if metrics else 0,
            tasks_failed=metrics.tasks_failed if metrics else 0,
            average_completion_time=metrics.average_completion_time if metrics else 0.0
        )
        
        agents.append(agent_status)
    
    return agents


@router.get("/agents/{agent_id}", response_model=Dict[str, Any])
async def get_agent_details(
    agent_id: str,
    ecosystem: AgentEcosystemManager = Depends(get_ecosystem_manager),
    current_user: Dict = Depends(get_current_user)
):
    """
    Get detailed agent information
    """
    if agent_id not in ecosystem.agents:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    agent = ecosystem.agents[agent_id]
    return agent.get_agent_status()


@router.get("/status", response_model=EcosystemStatusResponse)
async def get_ecosystem_status(
    ecosystem: AgentEcosystemManager = Depends(get_ecosystem_manager),
    current_user: Dict = Depends(get_current_user)
):
    """
    Get comprehensive ecosystem status
    """
    status = ecosystem.get_ecosystem_status()
    
    return EcosystemStatusResponse(
        system_id=status["system_id"],
        is_running=status["is_running"],
        total_agents=len(status["agents"]),
        total_tasks=status["tasks"]["total"],
        pending_tasks=status["tasks"]["pending"],
        in_progress_tasks=status["tasks"]["in_progress"],
        completed_tasks=status["tasks"]["completed"],
        failed_tasks=status["tasks"]["failed"],
        queue_length=status["queue_length"],
        active_tasks=status["active_tasks"],
        agent_utilization=status["ecosystem_stats"]["agent_utilization"],
        average_task_completion_time=status["ecosystem_stats"]["average_task_completion_time"],
        collaboration_efficiency=status["ecosystem_stats"]["collaboration_efficiency"]
    )


@router.get("/specializations", response_model=List[Dict[str, str]])
async def list_specializations(
    current_user: Dict = Depends(get_current_user)
):
    """
    List available agent specializations
    """
    return [
        {
            "value": spec.value,
            "name": spec.name.replace("_", " ").title(),
            "description": f"Specialized agent for {spec.value.replace('_', ' ')}"
        }
        for spec in AgentSpecialization
    ]


@router.post("/agents/{agent_id}/collaborate")
async def request_collaboration(
    agent_id: str,
    collaboration_request: Dict[str, Any],
    ecosystem: AgentEcosystemManager = Depends(get_ecosystem_manager),
    current_user: Dict = Depends(get_current_user)
):
    """
    Request collaboration between agents
    """
    if agent_id not in ecosystem.agents:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    agent = ecosystem.agents[agent_id]
    
    target_agent = collaboration_request.get("target_agent")
    if not target_agent or target_agent not in ecosystem.agents:
        raise HTTPException(status_code=400, detail="Invalid target agent")
    
    task_description = collaboration_request.get("task_description", "")
    required_capabilities = collaboration_request.get("required_capabilities", [])
    
    # Request collaboration
    request_id = await agent.request_collaboration(
        target_agent=target_agent,
        task_description=task_description,
        required_capabilities=required_capabilities
    )
    
    return {
        "collaboration_request_id": request_id,
        "status": "requested",
        "message": "Collaboration request submitted successfully"
    }


@router.get("/analytics/performance", response_model=Dict[str, Any])
async def get_performance_analytics(
    time_range: str = "24h",
    ecosystem: AgentEcosystemManager = Depends(get_ecosystem_manager),
    current_user: Dict = Depends(get_current_user)
):
    """
    Get performance analytics cho ecosystem
    """
    # Calculate time range
    now = datetime.now()
    if time_range == "1h":
        start_time = now - timedelta(hours=1)
    elif time_range == "24h":
        start_time = now - timedelta(hours=24)
    elif time_range == "7d":
        start_time = now - timedelta(days=7)
    else:
        start_time = now - timedelta(hours=24)
    
    # Filter tasks by time range
    recent_tasks = [
        task for task in ecosystem.tasks.values()
        if task.created_at >= start_time
    ]
    
    # Calculate analytics
    total_tasks = len(recent_tasks)
    completed_tasks = len([t for t in recent_tasks if t.status == TaskStatus.COMPLETED])
    failed_tasks = len([t for t in recent_tasks if t.status == TaskStatus.FAILED])
    
    success_rate = completed_tasks / total_tasks if total_tasks > 0 else 0.0
    
    # Average completion time
    completed_with_duration = [
        t for t in recent_tasks 
        if t.status == TaskStatus.COMPLETED and t.actual_duration
    ]
    avg_completion_time = (
        sum(t.actual_duration.total_seconds() for t in completed_with_duration) / len(completed_with_duration)
        if completed_with_duration else 0.0
    )
    
    # Task type distribution
    task_types = {}
    for task in recent_tasks:
        task_types[task.task_type] = task_types.get(task.task_type, 0) + 1
    
    return {
        "time_range": time_range,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "failed_tasks": failed_tasks,
        "success_rate": success_rate,
        "average_completion_time": avg_completion_time,
        "task_type_distribution": task_types,
        "ecosystem_stats": ecosystem.ecosystem_stats
    }


@router.get("/health")
async def ecosystem_health_check(
    ecosystem: AgentEcosystemManager = Depends(get_ecosystem_manager)
):
    """
    Health check cho Agent Ecosystem
    """
    return {
        "status": "healthy" if ecosystem.is_running else "unhealthy",
        "system_id": ecosystem.system_id,
        "agents_count": len(ecosystem.agents),
        "active_tasks": len(ecosystem.active_tasks),
        "queue_length": len(ecosystem.task_queue),
        "timestamp": datetime.now().isoformat()
    } 