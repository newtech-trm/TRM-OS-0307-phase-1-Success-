#!/usr/bin/env python3
"""
Task Repository - AGE Semantic Architecture
Handles strategic task coordination in AGE system
"""

from typing import List, Optional, Dict, Any
from neomodel import DoesNotExist
from datetime import datetime

from trm_api.graph_models.task import Task as GraphTask
from trm_api.models.task import TaskCreate, TaskUpdate

# AGE Semantic Ontology Imports
from trm_api.graph_models.strategic_project import GraphStrategicProject  # Replaced legacy Project
# TODO: Implement AGEActor ontology integration
# from trm_api.ontology.age_actor import AGEActor  # Future implementation
from trm_api.graph_models.tension import Tension as GraphTension

from trm_api.core.logging_config import get_logger

logger = get_logger(__name__)

class TaskRepository:
    """AGE Task Repository - Strategic task coordination"""
    
    def create_task(self, task_data: TaskCreate) -> Optional[GraphTask]:
        """Create strategic task in AGE semantic context"""
        try:
            task = GraphTask(
                title=task_data.title,
                description=task_data.description,
                task_type=task_data.task_type,
                status=task_data.status or "pending",
                priority=task_data.priority or "medium",
                estimated_effort=task_data.estimated_effort,
                actual_effort=task_data.actual_effort,
                due_date=task_data.due_date,
                completion_criteria=task_data.completion_criteria or [],
                strategic_context=task_data.strategic_context or {},
                required_capabilities=task_data.required_capabilities or [],
                expected_outcomes=task_data.expected_outcomes or []
            ).save()
            
            logger.info(f"AGE Strategic Task created: {task.uid} - {task.title}")
            return task
            
        except Exception as e:
            logger.error(f"AGE Task creation error: {str(e)}")
            return None

    def get_task_by_id(self, task_id: str) -> Optional[GraphTask]:
        """Get strategic task by ID"""
        try:
            return GraphTask.nodes.get_or_none(uid=task_id)
        except DoesNotExist:
            return None
        except Exception as e:
            logger.error(f"AGE Task retrieval error: {str(e)}")
            return None

    def list_tasks(self, skip: int = 0, limit: int = 100) -> List[GraphTask]:
        """List strategic tasks with AGE semantic context"""
        try:
            tasks = GraphTask.nodes.all()[skip:skip+limit]
            logger.info(f"AGE Task Repository: Listed {len(tasks)} strategic tasks")
            return tasks
        except Exception as e:
            logger.error(f"AGE Task listing error: {str(e)}")
            return []

    def update_task(self, uid: str, task_data: TaskUpdate) -> Optional[GraphTask]:
        """Update strategic task with AGE intelligence"""
        try:
            task = self.get_task_by_id(uid)
            if not task:
                return None
            
            update_fields = task_data.dict(exclude_unset=True)
            for field, value in update_fields.items():
                if hasattr(task, field):
                    setattr(task, field, value)
            
            task.updated_at = datetime.now()
            task.save()
            
            logger.info(f"AGE Strategic Task updated: {task.uid}")
            return task
            
        except Exception as e:
            logger.error(f"AGE Task update error: {str(e)}")
            return None

    def delete_task(self, uid: str) -> bool:
        """Delete strategic task with AGE validation"""
        try:
            task = self.get_task_by_id(uid)
            if task:
                task.delete()
                logger.info(f"AGE Strategic Task deleted: {uid}")
                return True
            return False
        except Exception as e:
            logger.error(f"AGE Task deletion error: {str(e)}")
            return False

    def get_tasks_by_strategic_project(self, project_id: str) -> List[GraphTask]:
        """Get tasks associated with strategic project"""
        try:
            strategic_project = GraphStrategicProject.nodes.get_or_none(uid=project_id)
            if strategic_project:
                # Get tasks related to this strategic project
                # Note: This requires proper relationship setup in graph models
                return []  # Placeholder for now
            return []
        except Exception as e:
            logger.error(f"AGE Task by project retrieval error: {str(e)}")
            return []

    def get_tasks_by_age_actor(self, actor_id: str) -> List[GraphTask]:
        """Get tasks assigned to AGE actor"""
        try:
            # Note: This requires proper AGE Actor integration
            # For now, return empty list until AGE Actor relationships are established
            return []
        except Exception as e:
            logger.error(f"AGE Task by actor retrieval error: {str(e)}")
            return []
