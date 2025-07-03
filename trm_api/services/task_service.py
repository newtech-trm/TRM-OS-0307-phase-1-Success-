from typing import Optional, List, Tuple, Dict, Any
from datetime import datetime

from trm_api.models.task import TaskCreate, TaskUpdate, Task
from trm_api.models.pagination import PaginatedResponse
from trm_api.repositories.task_repository import TaskRepository

class TaskService:
    """
    Service layer for handling Task business logic according to Ontology V3.2.
    Provides a clean separation between API endpoints and repository operations.
    """

    def __init__(self, repository: TaskRepository = None):
        self.repository = repository or TaskRepository()

    def create_task(self, task_data: TaskCreate) -> Optional[Task]:
        """
        Creates a new task with validation according to Ontology V3.2 requirements.
        
        Args:
            task_data: TaskCreate Pydantic model containing task data
            
        Returns:
            Task object if creation succeeds, None otherwise
        """
        # Perform any additional validation or business logic here
        # For example, we could check if the task name follows certain patterns
        # or if the combination of task properties is valid
        
        # Create the task using the repository
        return self.repository.create_task(task_data=task_data)
    
    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        """
        Retrieves a task by its ID.
        
        Args:
            task_id: Task unique identifier
            
        Returns:
            Task object if found, None otherwise
        """
        return self.repository.get_task_by_uid(uid=task_id)
    
    def update_task(self, task_id: str, task_data: TaskUpdate) -> Optional[Task]:
        """
        Updates an existing task with validation according to Ontology V3.2.
        
        Args:
            task_id: Task unique identifier
            task_data: TaskUpdate Pydantic model containing task update data
            
        Returns:
            Updated Task object if update succeeds, None otherwise
        """
        # Perform any additional validation or business logic here
        # For example, we might want to validate state transitions
        # or ensure certain combinations of fields are valid together
        
        return self.repository.update_task(uid=task_id, task_data=task_data)
    
    def delete_task(self, task_id: str) -> bool:
        """
        Deletes a task by its ID.
        
        Args:
            task_id: Task unique identifier
            
        Returns:
            True if deletion succeeded, False otherwise
        """
        return self.repository.delete_task(uid=task_id)
    
    def list_tasks_for_project(self, project_id: str, skip: int = 0, limit: int = 100) -> List[Task]:
        """
        Lists tasks for a specific project.
        
        Args:
            project_id: Project unique identifier
            skip: Number of items to skip
            limit: Maximum number of items to return
            
        Returns:
            List of tasks belonging to the project
        """
        return self.repository.list_tasks_for_project(project_id=project_id, skip=skip, limit=limit)
    
    def get_paginated_tasks_for_project(self, project_id: str, page: int = 1, page_size: int = 10) -> PaginatedResponse[Task]:
        """
        Gets paginated tasks for a specific project.
        
        Args:
            project_id: Project unique identifier
            page: Page number (1-indexed)
            page_size: Number of items per page
            
        Returns:
            PaginatedResponse containing tasks and pagination metadata
        """
        tasks, total_count, page_count = self.repository.get_paginated_tasks_for_project(
            project_id=project_id, 
            page=page, 
            page_size=page_size
        )
        
        return PaginatedResponse.create(
            items=tasks, 
            total_count=total_count, 
            page=page, 
            page_size=page_size
        )
    
    def assign_task_to_user(self, task_id: str, user_id: str,
                           assignment_type: str = 'Primary',
                           priority_level: int = 3,
                           estimated_effort: float = None,
                           assigned_by: str = None,
                           notes: str = None) -> Optional[Tuple[Task, Any]]:
        """
        Assigns a task to a user with validation according to Ontology V3.2.
        
        Args:
            task_id: Task unique identifier
            user_id: User unique identifier
            assignment_type: Type of assignment ('Primary', 'Supporting', 'Reviewer', 'Observer')
            priority_level: Priority level (1-5)
            estimated_effort: Estimated effort in hours
            assigned_by: ID of the user making the assignment
            notes: Additional notes about this assignment
            
        Returns:
            Tuple of (task, user) if assignment succeeds, None otherwise
        """
        # Validate assignment type
        valid_assignment_types = ['Primary', 'Supporting', 'Reviewer', 'Observer']
        if assignment_type not in valid_assignment_types:
            return None
        
        # Validate priority level
        if priority_level < 1 or priority_level > 5:
            return None
            
        return self.repository.assign_task_to_user(
            task_uid=task_id,
            user_uid=user_id,
            assignment_type=assignment_type,
            priority_level=priority_level,
            estimated_effort=estimated_effort,
            assigned_by=assigned_by,
            notes=notes
        )
    
    def assign_task_to_agent(self, task_id: str, agent_id: str,
                            assignment_type: str = 'Primary',
                            priority_level: int = 3,
                            estimated_effort: float = None,
                            assigned_by: str = None,
                            notes: str = None) -> Optional[Tuple[Task, Any]]:
        """
        Assigns a task to an agent with validation according to Ontology V3.2.
        
        Args:
            task_id: Task unique identifier
            agent_id: Agent unique identifier
            assignment_type: Type of assignment ('Primary', 'Supporting', 'Reviewer', 'Observer')
            priority_level: Priority level (1-5)
            estimated_effort: Estimated effort in hours
            assigned_by: ID of the user making the assignment
            notes: Additional notes about this assignment
            
        Returns:
            Tuple of (task, agent) if assignment succeeds, None otherwise
        """
        # Validate assignment type
        valid_assignment_types = ['Primary', 'Supporting', 'Reviewer', 'Observer']
        if assignment_type not in valid_assignment_types:
            return None
        
        # Validate priority level
        if priority_level < 1 or priority_level > 5:
            return None
            
        return self.repository.assign_task_to_agent(
            task_uid=task_id,
            agent_uid=agent_id,
            assignment_type=assignment_type,
            priority_level=priority_level,
            estimated_effort=estimated_effort,
            assigned_by=assigned_by,
            notes=notes
        )
    
    def get_task_assignees(self, task_id: str, include_relationship_details: bool = False) -> Dict[str, Any]:
        """
        Gets all assignees (users and agents) for a specific task.
        
        Args:
            task_id: Task unique identifier
            include_relationship_details: Whether to include detailed relationship properties
            
        Returns:
            Dictionary with 'users' and 'agents' lists
        """
        if include_relationship_details:
            return self.repository.get_task_assignees_with_relationships(task_uid=task_id)
        else:
            return self.repository.get_task_assignees(task_uid=task_id)
        
    
    def accept_task_assignment(self, task_id: str, assignee_id: str, acceptance_notes: str = None) -> bool:
        """
        Marks a task assignment as accepted by the assignee.
        
        Args:
            task_id: Task unique identifier
            assignee_id: ID of the user or agent accepting the task
            acceptance_notes: Optional notes about the acceptance
            
        Returns:
            True if the acceptance was successful, False otherwise
        """
        return self.repository.accept_task_assignment(
            task_uid=task_id,
            assignee_uid=assignee_id,
            acceptance_notes=acceptance_notes
        )
    
    def complete_task_assignment(self, task_id: str, assignee_id: str, actual_effort: float = None) -> bool:
        """
        Marks a task assignment as completed by the assignee.
        
        Args:
            task_id: Task unique identifier
            assignee_id: ID of the user or agent completing the task
            actual_effort: Actual effort spent in hours
            
        Returns:
            True if the completion was successful, False otherwise
        """
        return self.repository.complete_task_assignment(
            task_uid=task_id,
            assignee_uid=assignee_id,
            actual_effort=actual_effort
        )
    
    def remove_task_assignment(self, task_id: str, assignee_id: str) -> bool:
        """
        Removes a task assignment between a task and an assignee.
        
        Args:
            task_id: Task unique identifier
            assignee_id: ID of the user or agent to unassign
            
        Returns:
            True if the assignment was removed, False otherwise
        """
        return self.repository.remove_assignment(
            task_uid=task_id,
            assignee_uid=assignee_id
        )
        
    # --- Tension relationship methods according to Ontology V3.2 ---
    
    def connect_task_to_tension(self, task_id: str, tension_id: str) -> bool:
        """
        Establishes a RESOLVES relationship from a Task to a Tension.
        This indicates that the Task was created to resolve this Tension.
        
        Args:
            task_id: Task unique identifier
            tension_id: Tension unique identifier
            
        Returns:
            True if connection was successful, False otherwise
        """
        return self.repository.connect_task_to_tension(
            task_uid=task_id,
            tension_uid=tension_id
        )
    
    def disconnect_task_from_tension(self, task_id: str, tension_id: str) -> bool:
        """
        Removes the RESOLVES relationship between a Task and a Tension.
        
        Args:
            task_id: Task unique identifier
            tension_id: Tension unique identifier
            
        Returns:
            True if disconnection was successful, False otherwise
        """
        return self.repository.disconnect_task_from_tension(
            task_uid=task_id,
            tension_uid=tension_id
        )
    
    def get_tensions_resolved_by_task(self, task_id: str, skip: int = 0, limit: int = 100) -> Optional[List]:
        """
        Get all Tensions that are resolved by a specific Task.
        
        Args:
            task_id: Task unique identifier
            skip: Number of items to skip for pagination
            limit: Maximum number of items to return
            
        Returns:
            List of tension objects or None if task not found
        """
        task = self.get_task_by_id(task_id)
        if not task:
            return None
            
        return self.repository.get_tensions_resolved_by_task(
            task_uid=task_id,
            skip=skip,
            limit=limit
        )
    
    def get_task_with_relationships(self, task_id: str) -> Optional[Dict]:
        """
        Get a comprehensive view of a task with all its relationships loaded.
        This method provides a complete picture of the task as defined in Ontology V3.2.
        
        Args:
            task_id: Task unique identifier
            
        Returns:
            Dictionary with task data and all related entities, or None if task not found
        """
        return self.repository.get_task_with_relationships(task_uid=task_id)
