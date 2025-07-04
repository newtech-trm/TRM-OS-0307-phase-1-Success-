from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Any, List, Dict, Optional

from trm_api.adapters.decorators import adapt_task_response, adapt_ontology_response

from trm_api.models.pagination import PaginatedResponse

from trm_api.models.task import Task, TaskCreate, TaskUpdate
from trm_api.services.task_service import TaskService

router = APIRouter()

async def get_task_service() -> TaskService:
    """Async factory để tạo TaskService"""
    return TaskService()

@router.get("/", response_model=PaginatedResponse[Task])
@adapt_task_response(response_item_key="items")
async def list_tasks_for_project(
    *, 
    project_id: str,
    page: int = Query(1, ge=1, description="Page number, 1-indexed"),
    page_size: int = Query(10, ge=1, le=100, description="Number of items per page"),
    service: TaskService = Depends(get_task_service)
) -> Any:
    """
    Retrieve paginated tasks for a specific project.
    """
    # Use TaskService to handle pagination logic
    return service.get_paginated_tasks_for_project(
        project_id=project_id, 
        page=page, 
        page_size=page_size
    )

@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
@adapt_task_response()
async def create_task(
    *, 
    task_in: TaskCreate, 
    service: TaskService = Depends(get_task_service)
) -> Any:
    """
    Create a new task for a project according to Ontology V3.2.
    """
    # The service handles validation, finding the project and linking it
    created_task = service.create_task(task_data=task_in)
    if not created_task:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Could not create task. Ensure project with ID {task_in.project_id} exists."
        )
    return created_task

@router.get("/{task_id}", response_model=Task)
@adapt_task_response()
async def get_task(
    *, 
    task_id: str, 
    service: TaskService = Depends(get_task_service)
) -> Any:
    """
    Get task by ID.
    """
    task = await service.get_task_by_id(task_id=task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task

@router.put("/{task_id}", response_model=Task)
@adapt_task_response()
async def update_task(
    *, 
    task_id: str,
    task_in: TaskUpdate,
    service: TaskService = Depends(get_task_service)
) -> Any:
    """
    Update a task according to Ontology V3.2.
    """
    updated_task = await service.update_task(task_id=task_id, task_data=task_in)
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return updated_task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    *, 
    task_id: str,
    service: TaskService = Depends(get_task_service)
) -> None:
    """
    Delete a task.
    """
    deleted = await service.delete_task(task_id=task_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return None

# --- Task Assignment Endpoints ---

@router.post("/{task_id}/assign/user/{user_id}", status_code=status.HTTP_200_OK)
@adapt_task_response()
async def assign_task_to_user(
    *,
    task_id: str,
    user_id: str,
    assignment_type: str = Query('Primary', description="Type of assignment: Primary, Supporting, Reviewer, Observer"),
    priority_level: int = Query(3, description="Priority level (1-5): 1=Critical, 2=High, 3=Medium, 4=Low, 5=Optional"),
    estimated_effort: Optional[float] = Query(None, description="Estimated effort in hours"),
    assigned_by: Optional[str] = Query(None, description="User ID of the person making the assignment"),
    notes: Optional[str] = Query(None, description="Additional notes about this assignment"),
    service: TaskService = Depends(get_task_service)
) -> Dict[str, Any]:
    """
    Assign a task to a user with ASSIGNS_TASK relationship properties.
    
    This follows the TRM Ontology V3.2 specification for ASSIGNS_TASK relationship.
    """
    result = await service.assign_task_to_user(
        task_id=task_id, 
        user_id=user_id,
        assignment_type=assignment_type,
        priority_level=priority_level,
        estimated_effort=estimated_effort,
        assigned_by=assigned_by,
        notes=notes
    )
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task or user not found"
        )
    
    task, user = result
    return {
        "message": f"Task {task_id} successfully assigned to user {user_id}",
        "task_id": task_id,
        "user_id": user_id,
        "assignment_type": assignment_type,
        "priority_level": priority_level
    }

@router.post("/{task_id}/assign/agent/{agent_id}", status_code=status.HTTP_200_OK)
@adapt_task_response()
async def assign_task_to_agent(
    *,
    task_id: str,
    agent_id: str,
    assignment_type: str = Query('Primary', description="Type of assignment: Primary, Supporting, Reviewer, Observer"),
    priority_level: int = Query(3, description="Priority level (1-5): 1=Critical, 2=High, 3=Medium, 4=Low, 5=Optional"),
    estimated_effort: Optional[float] = Query(None, description="Estimated effort in hours"),
    assigned_by: Optional[str] = Query(None, description="User ID of the person making the assignment"),
    notes: Optional[str] = Query(None, description="Additional notes about this assignment"),
    service: TaskService = Depends(get_task_service)
) -> Dict[str, Any]:
    """
    Assign a task to an agent with ASSIGNS_TASK relationship properties.
    
    This follows the TRM Ontology V3.2 specification for ASSIGNS_TASK relationship.
    """
    result = await service.assign_task_to_agent(
        task_id=task_id, 
        agent_id=agent_id,
        assignment_type=assignment_type,
        priority_level=priority_level,
        estimated_effort=estimated_effort,
        assigned_by=assigned_by,
        notes=notes
    )
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task or agent not found"
        )
    
    task, agent = result
    return {
        "message": f"Task {task_id} successfully assigned to agent {agent_id}",
        "task_id": task_id,
        "agent_id": agent_id,
        "assignment_type": assignment_type,
        "priority_level": priority_level
    }

@router.get("/{task_id}/assignees", status_code=status.HTTP_200_OK)
@adapt_task_response()
async def get_task_assignees(
    *,
    task_id: str,
    include_relationship_details: bool = Query(False, description="Include detailed relationship properties"),
    service: TaskService = Depends(get_task_service)
) -> Dict[str, Any]:
    """
    Get all assignees (users and agents) for a specific task.
    
    If include_relationship_details is True, returns full relationship properties
    according to TRM Ontology V3.2.
    """
    # Check if task exists
    task = await service.get_task_by_id(task_id=task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # Get assignees with relationship details
    assignees = await service.get_task_assignees(task_id=task_id, include_relationship_details=include_relationship_details)
    
    return assignees

@router.post("/{task_id}/accept", status_code=status.HTTP_200_OK)
@adapt_task_response()
async def accept_task_assignment(
    *,
    task_id: str,
    assignee_id: str = Query(..., description="ID of the user or agent accepting the task"),
    acceptance_notes: Optional[str] = Query(None, description="Optional notes about task acceptance"),
    service: TaskService = Depends(get_task_service)
) -> Dict[str, Any]:
    """
    Accept a task assignment by the assigned user or agent.
    
    Updates the ASSIGNS_TASK relationship with acceptance information.
    """
    success = await service.accept_task_assignment(
        task_id=task_id,
        assignee_id=assignee_id,
        acceptance_notes=acceptance_notes
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task, assignee, or assignment relationship not found"
        )
    
    return {
        "message": f"Task {task_id} has been accepted by {assignee_id}",
        "task_id": task_id,
        "assignee_id": assignee_id,
        "accepted": True
    }

@router.post("/{task_id}/complete", status_code=status.HTTP_200_OK)
def complete_task_assignment(
    *,
    task_id: str,
    assignee_id: str = Query(..., description="ID of the user or agent completing the task"),
    actual_effort: Optional[float] = Query(None, description="Actual effort spent in hours"),
    service: TaskService = Depends(get_task_service)
) -> Dict[str, Any]:
    """
    Mark a task assignment as completed by the assigned user or agent.
    
    Updates the ASSIGNS_TASK relationship with completion information.
    """
    success = service.complete_task_assignment(
        task_id=task_id,
        assignee_id=assignee_id,
        actual_effort=actual_effort
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task, assignee, or assignment relationship not found"
        )
    
    return {
        "message": f"Task {task_id} has been completed by {assignee_id}",
        "task_id": task_id,
        "assignee_id": assignee_id,
        "completed": True
    }

@router.delete("/{task_id}/assignee/{assignee_id}")
async def remove_task_assignment(
    *, 
    task_id: str,
    assignee_id: str,
    service: TaskService = Depends(get_task_service)
) -> Any:
    """
    Remove a task assignment (ASSIGNS_TASK relationship) between a task and a user/agent.
    """
    success = await service.remove_task_assignment(task_id=task_id, assignee_id=assignee_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not remove assignment. Either task or assignee not found, or no assignment exists."
        )
    return {"detail": f"Assignment removed between task {task_id} and assignee {assignee_id}"}

# --- Task-Tension Relationship Endpoints ---

@router.post("/{task_id}/resolves/{tension_id}", status_code=status.HTTP_201_CREATED)
async def connect_task_to_tension(
    *, 
    task_id: str,
    tension_id: str,
    service: TaskService = Depends(get_task_service)
) -> Any:
    """
    Establish a RESOLVES relationship from a Task to a Tension.
    This indicates that the Task was created to resolve this Tension.
    
    According to Ontology V3.2, this creates a bidirectional relationship between Task and Tension.
    """
    success = await service.connect_task_to_tension(task_id=task_id, tension_id=tension_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not establish relationship. Either Task or Tension not found."
        )
    return {"detail": f"Task {task_id} now resolves Tension {tension_id}"}

@router.delete("/{task_id}/resolves/{tension_id}")
async def disconnect_task_from_tension(
    *, 
    task_id: str,
    tension_id: str,
    service: TaskService = Depends(get_task_service)
) -> Any:
    """
    Remove the RESOLVES relationship between a Task and a Tension.
    """
    success = await service.disconnect_task_from_tension(task_id=task_id, tension_id=tension_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not remove relationship. Either Task or Tension not found, or no relationship exists."
        )
    return {"detail": f"Task {task_id} no longer resolves Tension {tension_id}"}

@router.get("/{task_id}/resolves", response_model=List[Dict])
async def get_tensions_resolved_by_task(
    *, 
    task_id: str,
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum number of items to return"),
    service: TaskService = Depends(get_task_service)
) -> Any:
    """
    Get all Tensions that are resolved by a specific Task.
    """
    tensions = await service.get_tensions_resolved_by_task(task_id=task_id, skip=skip, limit=limit)
    if tensions is None:  # Different from empty list
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return tensions

@router.get("/{task_id}/with-relationships", response_model=Dict)
async def get_task_with_relationships(
    *, 
    task_id: str,
    service: TaskService = Depends(get_task_service)
) -> Any:
    """
    Get a comprehensive view of a task with all its relationships loaded.
    This endpoint provides a complete picture of the task as defined in Ontology V3.2.
    """
    task_data = await service.get_task_with_relationships(task_id=task_id)
    if not task_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task_data
