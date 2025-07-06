#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Service - Triển khai các dịch vụ nghiệp vụ cho Project
theo Ontology V3.2 với đầy đủ thuộc tính mở rộng và relationship.
"""

from typing import List, Optional, Any, Dict, Tuple
from datetime import datetime
from trm_api.models.project import ProjectCreate, ProjectUpdate, Project, ProjectDetail
from trm_api.repositories.project_repository import ProjectRepository
from trm_api.graph_models.project import Project as GraphProject
from trm_api.graph_models.resource import Resource as GraphResource
from trm_api.graph_models.agent import Agent as GraphAgent
# Import PaginationHelper cho phân trang
from trm_api.repositories.pagination_helper import PaginationHelper
# Import PaginationMetadata và PaginatedResponse từ models
from trm_api.models.pagination import PaginationMetadata, PaginatedResponse

class ProjectService:
    """Mock Project Service for testing conversational interface"""
    
    def __init__(self):
        self.projects = {}
    
    async def create_project(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new project"""
        project_id = str(uuid4())
        project_name = parameters.get("name", "New Project")
        
        project = {
            "id": project_id,
            "name": project_name,
            "description": f"Project: {project_name}",
            "status": "active",
            "created_at": datetime.now().isoformat(),
            "progress": 0.0,
            "team_size": 0,
            "estimated_duration": "4 weeks"
        }
        
        self.projects[project_id] = project
        return project
    
    async def get_project(self, project_id: str) -> Optional[Dict[str, Any]]:
        """Get project by ID"""
        return self.projects.get(project_id)
    
    async def list_projects(self) -> list:
        """List all projects"""
        return list(self.projects.values())
    
    async def update_project(self, project_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update project"""
        if project_id in self.projects:
            self.projects[project_id].update(updates)
            return self.projects[project_id]
        return None
    
    async def get_project_by_id(self, project_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves a project by its ID asynchronously.
        """
        project = self.projects.get(project_id)
        return project
    
    async def get_all_projects(self) -> List[Dict[str, Any]]:
        """
        Retrieves all projects asynchronously.
        """
        return list(self.projects.values())
    
    async def get_paginated_projects(self, page: int = 1, page_size: int = 10) -> Tuple[List[Dict[str, Any]], PaginationMetadata]:
        """
        Retrieves a paginated list of projects asynchronously.
        
        Returns a tuple of (projects_list, pagination_metadata)
        """
        projects = list(self.projects.values())
        total_count = len(projects)
        page_count = 1 if total_count <= page_size else (total_count + page_size - 1) // page_size
        
        # Create pagination metadata
        pagination_meta = PaginationMetadata(
            total=total_count,
            page=page,
            page_size=page_size,
            pages=page_count
        )
        
        # Paginate projects
        paginated_projects = projects[(page - 1) * page_size:page * page_size]
        
        return paginated_projects, pagination_meta
    
    async def delete_project(self, project_id: str) -> bool:
        """
        Deletes a project asynchronously.
        """
        return self.projects.pop(project_id, None) is not None
    
    async def get_project_tasks(self, project_id: str) -> List[Dict[str, Any]]:
        """
        Retrieves tasks associated with a project asynchronously.
        """
        project = self.projects.get(project_id)
        if not project:
            return []
        
        return [project]
    
    async def add_task_to_project(self, project_id: str, task_id: str) -> bool:
        """
        Associates a task with a project asynchronously.
        """
        project = self.projects.get(project_id)
        if project:
            project["tasks"] = project.get("tasks", []) + [task_id]
            return True
        return False
    
    async def remove_task_from_project(self, project_id: str, task_id: str) -> bool:
        """
        Removes the association of a task with a project asynchronously.
        """
        project = self.projects.get(project_id)
        if project:
            project["tasks"] = [task for task in project.get("tasks", []) if task != task_id]
            return True
        return False
    
    # --- Resource Management Methods ---
    
    async def assign_resource_to_project(self, project_id: str, resource_id: str,
                                  allocation_percentage: int = 100,
                                  assignment_type: str = "full",
                                  expected_end_date: Optional[str] = None,
                                  assignment_status: str = "active",
                                  notes: Optional[str] = None,
                                  assigned_by: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Assigns a Resource to a Project with relationship properties asynchronously.
        """
        project = self.projects.get(project_id)
        if not project:
            return None
        
        resource = {
            "id": resource_id,
            "relationship": {
                "allocation_percentage": allocation_percentage,
                "assignment_type": assignment_type,
                "assignment_status": assignment_status,
                "assigned_at": datetime.now().isoformat(),
                "expected_end_date": expected_end_date,
                "notes": notes,
                "assigned_by": assigned_by
            }
        }
        
        project["resources"] = project.get("resources", []) + [resource]
        return resource
    
    async def get_project_resources(self, project_id: str, page: int = 1, page_size: int = 10) -> Tuple[List[Dict[str, Any]], PaginationMetadata]:
        """
        Retrieves paginated list of resources assigned to a specific project asynchronously.
        """
        project = self.projects.get(project_id)
        if not project or "resources" not in project:
            return [], PaginationMetadata(total=0, page=page, page_size=page_size, pages=1)
        
        resources = project["resources"]
        total_count = len(resources)
        page_count = 1 if total_count <= page_size else (total_count + page_size - 1) // page_size
        
        # Paginate resources
        paginated_resources = resources[(page - 1) * page_size:page * page_size]
        
        # Create pagination metadata
        pagination = PaginationMetadata(
            page=page,
            page_size=page_size,
            total=total_count,
            pages=page_count
        )
        
        return paginated_resources, pagination
    
    async def get_project_resources_with_relationships(self, project_id: str) -> List[Dict[str, Any]]:
        """
        Retrieves resources assigned to a project including the relationship properties asynchronously.
        """
        project = self.projects.get(project_id)
        if not project or "resources" not in project:
            return []
        
        return [{
            "resource": resource,
            "relationship": relationship
        } for resource, relationship in project["resources"]]
    
    async def update_resource_project_relationship(self, project_id: str, resource_id: str, **relationship_props) -> Optional[Dict[str, Any]]:
        """
        Updates the properties of the ASSIGNED_TO_PROJECT relationship between a Resource and a Project asynchronously.
        """
        project = self.projects.get(project_id)
        if not project or "resources" not in project:
            return None
        
        updated_resources = []
        for resource, relationship in project["resources"]:
            if resource["id"] == resource_id:
                updated_resource = {**resource, **relationship_props}
                updated_resources.append((updated_resource, relationship))
            else:
                updated_resources.append((resource, relationship))
        
        project["resources"] = updated_resources
        return updated_resources[0][0] if updated_resources else None
    
    async def unassign_resource_from_project(self, project_id: str, resource_id: str) -> bool:
        """
        Removes the ASSIGNED_TO_PROJECT relationship between a Resource and a Project asynchronously.
        """
        project = self.projects.get(project_id)
        if not project or "resources" not in project:
            return False
        
        updated_resources = [resource for resource, relationship in project["resources"] if resource["id"] != resource_id]
        project["resources"] = updated_resources
        return True
    
    # --- Project Manager and Agent Methods ---
    
    async def assign_manager_to_project(self, project_id: str, agent_id: str,
                                role: str = 'project_manager',
                                responsibility_level: str = 'primary',
                                appointed_at = None,
                                notes: str = None) -> Optional[Dict[str, Any]]:
        """
        Establishes a MANAGES_PROJECT relationship from an Agent to a Project
        according to the TRM Ontology V3.2 asynchronously.
        """
        project = self.projects.get(project_id)
        if not project:
            return None
        
        agent = {
            "id": agent_id,
            "relationship": {
                "role": role,
                "responsibility_level": responsibility_level,
                "appointed_at": (appointed_at or datetime.now()).isoformat(),
                "notes": notes
            }
        }
        
        project["managers"] = project.get("managers", []) + [agent]
        return agent
    
    async def get_project_managers(self, project_id: str) -> List[Dict[str, Any]]:
        """
        Retrieves all Agents that manage a specific Project asynchronously.
        """
        project = self.projects.get(project_id)
        if not project or "managers" not in project:
            return []
        
        return project["managers"]
    
    async def get_project_managers_with_relationships(self, project_id: str) -> List[Dict[str, Any]]:
        """
        Retrieves all Agents that manage a specific Project,
        including the relationship properties according to the ontology V3.2 asynchronously.
        """
        project = self.projects.get(project_id)
        if not project or "managers" not in project:
            return []
        
        return [{
            "agent": manager,
            "relationship": relationship
        } for manager, relationship in project["managers"]]
    
    async def update_manager_project_relationship(self, project_id: str, agent_id: str,
                                          role: Optional[str] = None,
                                          responsibility_level: Optional[str] = None,
                                          notes: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Updates the relationship properties between an Agent and a Project
        according to the TRM Ontology V3.2 asynchronously.
        """
        project = self.projects.get(project_id)
        if not project or "managers" not in project:
            return None
        
        updated_managers = []
        for manager, relationship in project["managers"]:
            if manager["id"] == agent_id:
                updated_manager = {**manager}
                if role:
                    updated_manager["relationship"]["role"] = role
                if responsibility_level:
                    updated_manager["relationship"]["responsibility_level"] = responsibility_level
                if notes:
                    updated_manager["relationship"]["notes"] = notes
                updated_managers.append((updated_manager, relationship))
            else:
                updated_managers.append((manager, relationship))
        
        project["managers"] = updated_managers
        return updated_managers[0][0] if updated_managers else None
    
    async def remove_manager_from_project(self, project_id: str, agent_id: str) -> bool:
        """
        Removes the MANAGES_PROJECT relationship between an Agent and a Project asynchronously.
        """
        project = self.projects.get(project_id)
        if not project or "managers" not in project:
            return False
        
        updated_managers = [manager for manager, relationship in project["managers"] if manager["id"] != agent_id]
        project["managers"] = updated_managers
        return True
    
    # --- Subproject Methods ---
    
    async def get_parent_project(self, project_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves the parent project of a given project asynchronously, if any.
        """
        project = self.projects.get(project_id)
        if not project:
            return None
        
        parent_projects = project.get("parent_projects", [])
        if not parent_projects:
            return None
            
        return parent_projects[0]
    
    async def get_subprojects(self, project_id: str) -> List[Dict[str, Any]]:
        """
        Retrieves all subprojects of a given project asynchronously.
        """
        project = self.projects.get(project_id)
        if not project:
            return []
        
        return project.get("subprojects", [])
    
    async def add_subproject(self, parent_id: str, child_id: str) -> bool:
        """
        Adds a subproject to a project asynchronously.
        """
        project = self.projects.get(parent_id)
        if not project:
            return False
        
        project["subprojects"] = project.get("subprojects", []) + [child_id]
        return True
    
    async def remove_parent_child_relationship(self, parent_id: str, child_id: str) -> bool:
        """
        Removes a parent-child relationship between two projects asynchronously.
        """
        project = self.projects.get(parent_id)
        if not project or "subprojects" not in project:
            return False
        
        updated_subprojects = [subproject for subproject in project["subprojects"] if subproject != child_id]
        project["subprojects"] = updated_subprojects
        return True
    
    async def get_project_subprojects(self, project_id: str) -> List[Dict[str, Any]]:
        """
        Retrieves all subprojects of a specific Project asynchronously.
        """
        project = self.projects.get(project_id)
        if not project:
            return []
        
        return project.get("subprojects", [])
    
    async def get_project_parent(self, project_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves the parent project of a specific Project asynchronously, if any.
        """
        project = self.projects.get(project_id)
        if not project:
            return None
        
        parent_projects = project.get("parent_projects", [])
        if not parent_projects:
            return None
            
        return parent_projects[0]
