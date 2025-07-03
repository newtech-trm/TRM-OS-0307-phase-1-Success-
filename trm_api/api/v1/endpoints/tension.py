from fastapi import APIRouter, Depends, HTTPException, status
from typing import Any, List

from trm_api.models.tension import Tension, TensionCreate, TensionUpdate
from trm_api.models.relationships import Relationship
from trm_api.repositories.tension_repository import TensionRepository

router = APIRouter()

def get_tension_repo() -> TensionRepository:
    return TensionRepository()

@router.get("/", response_model=List[Tension])
def list_tensions_for_project(
    *, 
    project_id: str,
    skip: int = 0,
    limit: int = 100,
    repo: TensionRepository = Depends(get_tension_repo)
) -> Any:
    """
    Retrieve tensions for a specific project.
    """
    tensions = repo.list_tensions_for_project(project_id=project_id, skip=skip, limit=limit)
    return tensions

@router.post("/", response_model=Tension, status_code=status.HTTP_201_CREATED)
def create_tension(
    *, 
    tension_in: TensionCreate, 
    repo: TensionRepository = Depends(get_tension_repo)
) -> Any:
    """
    Create new tension for a project.
    """
    created_tension = repo.create_tension(tension_data=tension_in)
    if not created_tension:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Could not create tension. Project with ID {tension_in.project_id} not found."
        )
    return created_tension

@router.get("/{tension_id}", response_model=Tension)
def get_tension(
    *, 
    tension_id: str, 
    repo: TensionRepository = Depends(get_tension_repo)
) -> Any:
    """
    Get tension by ID.
    """
    tension = repo.get_tension_by_uid(uid=tension_id)
    if not tension:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Tension not found"
        )
    return tension

@router.put("/{tension_id}", response_model=Tension)
def update_tension(
    *, 
    tension_id: str,
    tension_in: TensionUpdate,
    repo: TensionRepository = Depends(get_tension_repo)
) -> Any:
    """
    Update a tension.
    """
    updated_tension = repo.update_tension(uid=tension_id, tension_data=tension_in)
    if not updated_tension:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Tension not found"
        )
    return updated_tension

@router.delete("/{tension_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tension(
    *, 
    tension_id: str,
    repo: TensionRepository = Depends(get_tension_repo)
) -> None:
    """
    Delete a tension.
    """
    deleted = repo.delete_tension(uid=tension_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tension not found"
        )
    return None

# Relationship endpoints for RESOLVES_TENSION
@router.post("/{tension_id}/resolved-by/{project_id}", response_model=dict, status_code=status.HTTP_201_CREATED)
def connect_project_to_tension(
    *,
    tension_id: str,
    project_id: str,
    repo: TensionRepository = Depends(get_tension_repo)
) -> Any:
    """
    Establish a RESOLVES_TENSION relationship from a Project to a Tension.
    This indicates that the Project was created to resolve the specified Tension.
    """
    result = repo.connect_tension_to_project(tension_uid=tension_id, project_uid=project_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tension or Project not found"
        )
    
    tension, project = result
    return {
        "message": f"Project '{project.title}' is now resolving Tension '{tension.title}'",
        "tension_id": tension.uid,
        "project_id": project.uid,
        "relationship": "RESOLVES_TENSION"
    }

@router.get("/{tension_id}/resolved-by", response_model=List[dict], status_code=status.HTTP_200_OK)
def get_projects_resolving_tension(
    *,
    tension_id: str,
    skip: int = 0,
    limit: int = 100,
    repo: TensionRepository = Depends(get_tension_repo)
) -> Any:
    """
    Get all Projects that are resolving a specific Tension.
    """
    tension = repo.get_tension_by_uid(uid=tension_id)
    if not tension:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tension not found"
        )
    
    projects = repo.get_projects_resolving_tension(tension_uid=tension_id, skip=skip, limit=limit)
    return [
        {
            "project_id": project.uid,
            "title": project.title,
            "description": project.description,
            "status": project.status
        }
        for project in projects
    ]

@router.delete("/{tension_id}/resolved-by/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def disconnect_project_from_tension(
    *,
    tension_id: str,
    project_id: str,
    repo: TensionRepository = Depends(get_tension_repo)
) -> None:
    """
    Remove the RESOLVES_TENSION relationship between a Project and a Tension.
    """
    success = repo.disconnect_project_from_tension(tension_uid=tension_id, project_uid=project_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tension or Project not found, or no relationship exists between them"
        )
    return None

# Task - Tension relationship endpoints (RESOLVES)
@router.post("/{tension_id}/resolved-by-task/{task_id}", status_code=status.HTTP_201_CREATED)
def connect_task_to_tension(
    *,
    tension_id: str,
    task_id: str,
    repo: TensionRepository = Depends(get_tension_repo)
) -> Any:
    """
    Establish a RESOLVES relationship from a Task to a Tension.
    This indicates that the Task was created to resolve this Tension.
    """
    success = repo.connect_task_to_tension(tension_id=tension_id, task_id=task_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not establish relationship. Either Tension or Task not found."
        )
    return {"detail": f"Task {task_id} now resolves Tension {tension_id}"}

@router.get("/{tension_id}/resolving-tasks", response_model=List[dict])
def get_tasks_resolving_tension(
    *,
    tension_id: str,
    skip: int = 0,
    limit: int = 100,
    repo: TensionRepository = Depends(get_tension_repo)
) -> Any:
    """
    Get all Tasks that are resolving a specific Tension.
    """
    tasks = repo.get_tasks_resolving_tension(tension_id=tension_id, skip=skip, limit=limit)
    if not tasks and not repo.get_tension_by_uid(tension_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tension not found"
        )
    return [{
        "uid": task.uid,
        "name": task.name,
        "description": task.description,
        "status": task.status,
        "priority": task.priority
    } for task in tasks]

@router.delete("/{tension_id}/resolved-by-task/{task_id}")
def disconnect_task_from_tension(
    *,
    tension_id: str,
    task_id: str,
    repo: TensionRepository = Depends(get_tension_repo)
) -> Any:
    """
    Remove the RESOLVES relationship between a Task and a Tension.
    """
    success = repo.disconnect_task_from_tension(tension_id=tension_id, task_id=task_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not remove relationship. Either Tension or Task not found."
        )
    return {"detail": f"Task {task_id} no longer resolves Tension {tension_id}"}

# Tension - WIN relationship endpoints (LEADS_TO_WIN)
@router.post("/{tension_id}/leads-to-win/{win_id}", status_code=status.HTTP_201_CREATED)
def connect_tension_to_win(
    *,
    tension_id: str,
    win_id: str,
    repo: TensionRepository = Depends(get_tension_repo)
) -> Any:
    """
    Establish a LEADS_TO_WIN relationship from a Tension to a WIN.
    This indicates that resolving the Tension led to this WIN.
    """
    success = repo.connect_tension_to_win(tension_id=tension_id, win_id=win_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not establish relationship. Either Tension or WIN not found."
        )
    return {"detail": f"Tension {tension_id} now leads to WIN {win_id}"}

@router.delete("/{tension_id}/leads-to-win/{win_id}")
def disconnect_tension_from_win(
    *,
    tension_id: str,
    win_id: str,
    repo: TensionRepository = Depends(get_tension_repo)
) -> Any:
    """
    Remove the LEADS_TO_WIN relationship between a Tension and a WIN.
    """
    success = repo.disconnect_tension_from_win(tension_id=tension_id, win_id=win_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not remove relationship. Either Tension or WIN not found."
        )
    return {"detail": f"Tension {tension_id} no longer leads to WIN {win_id}"}

@router.get("/{tension_id}/with-relationships", response_model=dict)
def get_tension_with_relationships(
    *,
    tension_id: str,
    repo: TensionRepository = Depends(get_tension_repo)
) -> Any:
    """
    Get a comprehensive view of a tension with all its relationships loaded.
    This endpoint provides a complete picture of the tension as defined in Ontology V3.2.
    """
    tension_data = repo.get_tension_with_relationships(tension_id=tension_id)
    if not tension_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tension not found"
        )
    return tension_data

# TODO: Refactor this relationship endpoint using the repository pattern.
# @router.post("/{tension_id}/identified-by/{user_id}", response_model=Relationship, status_code=status.HTTP_201_CREATED)
# def identify_tension_by_user(
#     *,
#     tension_id: str,
#     user_id: str,
#     # service: TensionService = Depends(get_tension_service) # This needs to be replaced with a repository call
# ) -> Any:
#     """
#     Creates an IDENTIFIED relationship from a User to a Tension.
#     """
#     # relationship = service.identify_tension_by_user(tension_id=tension_id, user_id=user_id)
#     # if relationship is None:
#     #     raise HTTPException(
#     #         status_code=status.HTTP_404_NOT_FOUND,
#     #         detail="Tension or User not found, or relationship could not be created"
#     #     )
#     # return relationship
