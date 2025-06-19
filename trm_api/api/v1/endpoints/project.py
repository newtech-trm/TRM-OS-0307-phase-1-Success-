from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Any, List, Optional, Dict
from datetime import datetime

from trm_api.models.project import Project, ProjectCreate, ProjectUpdate
from trm_api.repositories.project_repository import ProjectRepository
from trm_api.services.project_service import ProjectService
from trm_api.models.relationships import Relationship
from trm_api.models.pagination import PaginatedResponse
from trm_api.models.resource import Resource
from trm_api.models.agent import Agent
from trm_api.adapters.decorators import adapt_project_response, adapt_ontology_response

router = APIRouter()

# Dependencies to get the repository and service instances
def get_project_repo() -> ProjectRepository:
    return ProjectRepository()

def get_project_service() -> ProjectService:
    return ProjectService()

@router.get("/", response_model=PaginatedResponse[Project])
@adapt_project_response(response_item_key="items")
async def list_projects(
    page: int = Query(1, ge=1, description="Page number, 1-indexed"),
    page_size: int = Query(10, ge=1, le=100, description="Number of items per page"),
    repo: ProjectRepository = Depends(get_project_repo)
) -> Any:
    """
    Retrieve a paginated list of projects.
    """
    projects, total_count, page_count = await repo.get_paginated_projects(page=page, page_size=page_size)
    return PaginatedResponse.create(items=projects, total_count=total_count, page=page, page_size=page_size)

@router.post("/", response_model=Project, status_code=status.HTTP_201_CREATED)
@adapt_project_response()
async def create_project(
    *, 
    project_in: ProjectCreate, 
    repo: ProjectRepository = Depends(get_project_repo)
) -> Any:
    """
    Create a new project.
    """
    try:
        graph_project = await repo.create_project(project_data=project_in)
        return graph_project
    except Exception as e:
        print(f"AN ERROR OCCURRED: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal error occurred during project creation."
        )

@router.get("/{project_id}", response_model=Project)
@adapt_project_response()
async def get_project(
    *, 
    project_id: str, 
    repo: ProjectRepository = Depends(get_project_repo)
) -> Any:
    """
    Get a specific project by its ID.
    """
    project = await repo.get_project_by_id(project_id=project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID {project_id} not found"
        )
    return project

@router.put("/{project_id}", response_model=Project)
@adapt_project_response()
async def update_project(
    *,
    project_id: str,
    project_in: ProjectUpdate,
    repo: ProjectRepository = Depends(get_project_repo)
) -> Any:
    """
    Update a project.
    """
    project = await repo.get_project_by_id(project_id=project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID {project_id} not found"
        )
    updated_project = await repo.update_project(project_id=project_id, project_data=project_in)
    return updated_project

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    *,
    project_id: str,
    repo: ProjectRepository = Depends(get_project_repo)
) -> None:
    """
    Delete a project.
    """
    deleted = repo.delete_project(uid=project_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    return None

# Relationship endpoints for RESOLVES_TENSION
@router.post("/{project_id}/resolves-tension/{tension_id}", response_model=dict, status_code=status.HTTP_201_CREATED)
def add_tension_to_resolve(
    *,
    project_id: str,
    tension_id: str,
    repo: ProjectRepository = Depends(get_project_repo)
) -> Any:
    """
    Establish a RESOLVES_TENSION relationship from a Project to a Tension.
    This indicates that the Project was created to resolve the specified Tension.
    """
    result = repo.add_tension_to_resolve(project_uid=project_id, tension_uid=tension_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project or Tension not found"
        )
    
    project, tension = result
    return {
        "message": f"Project '{project.title}' is now resolving Tension '{tension.title}'",
        "project_id": project.uid,
        "tension_id": tension.uid,
        "relationship": "RESOLVES_TENSION"
    }

@router.get("/{project_id}/resolves-tensions", response_model=PaginatedResponse[dict], status_code=status.HTTP_200_OK)
def get_tensions_resolved_by_project(
    *,
    project_id: str,
    page: int = Query(1, ge=1, description="Page number, 1-indexed"),
    page_size: int = Query(10, ge=1, le=100, description="Number of items per page"),
    repo: ProjectRepository = Depends(get_project_repo)
) -> Any:
    """
    Get all Tensions that are being resolved by a specific Project.
    """
    project = repo.get_project_by_uid(uid=project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    tensions, total_count, page_count = repo.get_paginated_tensions_by_project(
        project_uid=project_id, page=page, page_size=page_size
    )
    
    tension_items = [
        {
            "tension_id": tension.uid,
            "title": tension.title,
            "description": tension.description,
            "status": tension.status,
            "severity": tension.severity
        }
        for tension in tensions
    ]
    
    return PaginatedResponse.create(
        items=tension_items, 
        total_count=total_count, 
        page=page, 
        page_size=page_size
    )

@router.delete("/{project_id}/resolves-tension/{tension_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_tension_from_project(
    *,
    project_id: str,
    tension_id: str,
    repo: ProjectRepository = Depends(get_project_repo)
) -> None:
    """
    Remove the RESOLVES_TENSION relationship between a Project and a Tension.
    """
    success = repo.remove_tension_from_project(project_uid=project_id, tension_uid=tension_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project or Tension not found, or no relationship exists between them"
        )
    return None

# --- Resource-Project Relationship Endpoints (ASSIGNED_TO_PROJECT) ---

@router.post("/{project_id}/resources/{resource_id}", response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED)
def assign_resource_to_project(
    *,
    project_id: str,
    resource_id: str,
    allocation_percentage: int = 100,
    assignment_type: str = "full",  # full, partial, temporary, contract, etc.
    expected_end_date: Optional[str] = None,
    assignment_status: str = "active",  # active, pending, completed, terminated
    notes: Optional[str] = None,
    assigned_by: Optional[str] = None,
    service: ProjectService = Depends(get_project_service)
) -> Any:
    """
    Assign a Resource to a Project with relationship properties as defined in TRM Ontology V3.2.
    """
    result = service.assign_resource_to_project(
        project_id=project_id,
        resource_id=resource_id,
        allocation_percentage=allocation_percentage,
        assignment_type=assignment_type,
        expected_end_date=expected_end_date,
        assignment_status=assignment_status,
        notes=notes,
        assigned_by=assigned_by
    )
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project or Resource not found, or assignment could not be created"
        )
    
    return result

@router.get("/{project_id}/resources", response_model=PaginatedResponse[Resource])
@adapt_ontology_response(entity_type="resource", response_item_key="items")
async def get_project_resources(
    *,
    project_id: str,
    page: int = Query(1, ge=1, description="Page number, 1-indexed"),
    page_size: int = Query(10, ge=1, le=100, description="Number of items per page"),
    service: ProjectService = Depends(get_project_service)
) -> Any:
    """
    Get all Resources assigned to a specific Project with pagination.
    """
    resources, pagination = service.get_paginated_resources_by_project(
        project_id=project_id, page=page, page_size=page_size
    )
    
    if not resources and page > 1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No resources found for this page"
        )
    
    return PaginatedResponse.create(
        items=resources,
        total_count=pagination.total_count,
        page=pagination.page,
        page_size=pagination.page_size
    )

@router.get("/{project_id}/resources-with-relationships", response_model=List[Dict[str, Any]])
@adapt_ontology_response(entity_type="resource")
async def get_project_resources_with_relationships(
    *,
    project_id: str,
    service: ProjectService = Depends(get_project_service)
) -> Any:
    """
    Get all Resources assigned to a specific Project including the relationship properties.
    """
    resources = service.get_project_resources_with_relationships(project_id=project_id)
    
    if not resources:
        return []
    
    return resources

@router.put("/{project_id}/resources/{resource_id}", status_code=status.HTTP_200_OK)
def update_resource_project_relationship(
    *,
    project_id: str,
    resource_id: str,
    allocation_percentage: Optional[int] = None,
    expected_end_date: Optional[str] = None,
    actual_end_date: Optional[str] = None,
    assignment_type: Optional[str] = None,
    assignment_status: Optional[str] = None,
    notes: Optional[str] = None,
    service: ProjectService = Depends(get_project_service)
) -> Any:
    """
    Update the relationship properties between a Resource and a Project.
    """
    success = service.update_resource_project_relationship(
        project_id=project_id,
        resource_id=resource_id,
        allocation_percentage=allocation_percentage,
        expected_end_date=expected_end_date,
        actual_end_date=actual_end_date,
        assignment_type=assignment_type,
        assignment_status=assignment_status,
        notes=notes
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project or Resource not found, or relationship could not be updated"
        )
    
    return {"message": "Resource-Project relationship updated successfully"}

@router.delete("/{project_id}/resources/{resource_id}", status_code=status.HTTP_204_NO_CONTENT)
def unassign_resource_from_project(
    *,
    project_id: str,
    resource_id: str,
    service: ProjectService = Depends(get_project_service)
) -> None:
    """
    Remove the ASSIGNED_TO_PROJECT relationship between a Resource and a Project.
    """
    success = service.unassign_resource_from_project(project_id=project_id, resource_id=resource_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project or Resource not found, or no relationship exists between them"
        )
    
    return None

# --- Agent-Project Relationship Endpoints (MAINTAINS_PROJECT) ---

@router.post("/{project_id}/managers/{agent_id}", response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED)
def assign_manager_to_project(
    *,
    project_id: str,
    agent_id: str,
    role: str = "project_manager",  # project_manager, product_owner, scrum_master, etc.
    responsibility_level: str = "primary",  # primary, secondary, support, etc.
    appointed_at: Optional[str] = None,
    notes: Optional[str] = None,
    service: ProjectService = Depends(get_project_service)
) -> Any:
    """
    Assign an Agent as a manager to a Project with relationship properties as defined in TRM Ontology V3.2.
    """
    result = service.assign_manager_to_project(
        project_id=project_id,
        agent_id=agent_id,
        role=role,
        responsibility_level=responsibility_level,
        appointed_at=appointed_at,
        notes=notes
    )
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project or Agent not found, or assignment could not be created"
        )
    
    return result

@router.get("/{project_id}/managers", response_model=List[Agent])
@adapt_ontology_response(entity_type="agent")
async def get_project_managers(
    *,
    project_id: str,
    service: ProjectService = Depends(get_project_service)
) -> Any:
    """
    Get all Agents managing a specific Project.
    """
    managers = service.get_project_managers(project_id=project_id)
    
    if not managers:
        return []
    
    return managers

@router.get("/{project_id}/managers-with-relationships", response_model=List[Dict[str, Any]])
@adapt_ontology_response(entity_type="agent")
async def get_project_managers_with_relationships(
    *,
    project_id: str,
    service: ProjectService = Depends(get_project_service)
) -> Any:
    """
    Get all Agents managing a specific Project including the relationship properties.
    """
    managers = service.get_project_managers_with_relationships(project_id=project_id)
    
    if not managers:
        return []
    
    return managers

@router.put("/{project_id}/managers/{agent_id}", status_code=status.HTTP_200_OK)
def update_manager_project_relationship(
    *,
    project_id: str,
    agent_id: str,
    role: Optional[str] = None,
    responsibility_level: Optional[str] = None,
    notes: Optional[str] = None,
    service: ProjectService = Depends(get_project_service)
) -> Any:
    """
    Update the relationship properties between an Agent and a Project.
    """
    success = service.update_manager_project_relationship(
        project_id=project_id,
        agent_id=agent_id,
        role=role,
        responsibility_level=responsibility_level,
        notes=notes
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project or Agent not found, or relationship could not be updated"
        )
    
    return {"message": "Manager-Project relationship updated successfully"}

@router.delete("/{project_id}/managers/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_manager_from_project(
    *,
    project_id: str,
    agent_id: str,
    service: ProjectService = Depends(get_project_service)
) -> None:
    """
    Remove the MANAGES_PROJECT relationship between an Agent and a Project.
    """
    success = service.remove_manager_from_project(project_id=project_id, agent_id=agent_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project or Agent not found, or no relationship exists between them"
        )
    
    return None

# --- Project-Project Relationship Endpoints (parent-child) ---

@router.get("/{project_id}/subprojects", response_model=List[Project])
@adapt_project_response()
async def get_project_subprojects(
    *,
    project_id: str,
    service: ProjectService = Depends(get_project_service)
) -> Any:
    """
    Get all subprojects of a specific Project.
    """
    subprojects = service.get_project_subprojects(project_id=project_id)
    
    if not subprojects:
        return []
    
    return subprojects

@router.get("/{project_id}/parent", response_model=Project, status_code=status.HTTP_200_OK)
def get_project_parent(
    *,
    project_id: str,
    service: ProjectService = Depends(get_project_service)
) -> Any:
    """
    Get the parent project of a specific Project, if any.
    """
    parent = service.get_project_parent(project_id=project_id)
    
    if not parent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found or has no parent project"
        )
    
    return parent
