from typing import List, Optional, Dict, Any, Union
from uuid import uuid4
from datetime import datetime

from trm_api.repositories.tension_repository import TensionRepository
from trm_api.models.tension import TensionCreate, TensionUpdate, Tension
from trm_api.models.relationships import Relationship, RelationshipType, TargetEntityTypeEnum


class TensionService:
    """
    Service for handling all business logic related to Tensions according to Ontology V3.2.
    """
    
    def __init__(self, repository: TensionRepository):
        self.repository = repository
    
    async def create_tension(self, tension_data: TensionCreate) -> Optional[Dict[str, Any]]:
        """
        Creates a new Tension following the Ontology V3.2 specifications.
        """
        tension = self.repository.create_tension(tension_data)
        if not tension:
            return None
        
        # Convert to API response format
        return {
            "uid": tension.uid,
            "title": tension.title,
            "description": tension.description,
            "status": tension.status,
            "priority": tension.priority,
            "source": tension.source,
            "tensionType": tension.tensionType,
            "creationDate": tension.creationDate.isoformat() if tension.creationDate else None,
            "lastModifiedDate": tension.lastModifiedDate.isoformat() if tension.lastModifiedDate else None
        }
    
    async def get_tension(self, uid: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves a Tension by its unique ID.
        """
        tension = self.repository.get_tension_by_uid(uid)
        if not tension:
            return None
        
        # Convert to API response format
        return {
            "uid": tension.uid,
            "title": tension.title,
            "description": tension.description,
            "status": tension.status,
            "priority": tension.priority,
            "source": tension.source,
            "tensionType": tension.tensionType,
            "creationDate": tension.creationDate.isoformat() if tension.creationDate else None,
            "lastModifiedDate": tension.lastModifiedDate.isoformat() if tension.lastModifiedDate else None
        }
    
    async def update_tension(self, uid: str, tension_data: TensionUpdate) -> Optional[Dict[str, Any]]:
        """
        Updates an existing tension.
        """
        updated_tension = self.repository.update_tension(uid, tension_data)
        if not updated_tension:
            return None
        
        return await self.get_tension(uid)
    
    async def delete_tension(self, uid: str) -> bool:
        """
        Deletes a tension.
        """
        return self.repository.delete_tension(uid)
    
    async def get_tension_with_relationships(self, tension_id: str) -> Optional[Dict[str, Any]]:
        """
        Gets a tension with all its relationships loaded.
        """
        return self.repository.get_tension_with_relationships(tension_id)
    
    async def connect_task_to_tension(self, tension_id: str, task_id: str) -> bool:
        """
        Establishes a RESOLVES relationship from a Task to a Tension.
        """
        result = self.repository.connect_task_to_tension(tension_id, task_id)
        return result is not None
    
    async def disconnect_task_from_tension(self, tension_id: str, task_id: str) -> bool:
        """
        Removes the RESOLVES relationship between a Task and a Tension.
        """
        return self.repository.disconnect_task_from_tension(tension_id, task_id)
    
    async def get_tasks_resolving_tension(self, tension_id: str, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get all tasks that are working to resolve a tension.
        """
        tasks = self.repository.get_tasks_resolving_tension(tension_id, skip, limit)
        return [
            {
                "uid": task.uid,
                "title": task.title,
                "status": task.status,
                "priority": task.priority
            } for task in tasks
        ]
    
    async def connect_tension_to_win(self, tension_id: str, win_id: str, 
                                    contribution_level: int = 3, 
                                    direct_contribution: bool = True) -> Optional[Dict[str, Any]]:
        """
        Establishes a LEADS_TO_WIN relationship from a Tension to a WIN.
        This indicates that resolving the Tension led to the specified WIN.
        
        According to Ontology V3.2, this relationship captures the value creation process.
        
        Args:
            tension_id: The unique identifier of the tension
            win_id: The unique identifier of the WIN
            contribution_level: Level of contribution (1-5) with 5 being highest
            direct_contribution: Whether the tension directly contributed to the WIN
        """
        result = self.repository.connect_tension_to_win(tension_id, win_id)
        if not result:
            return None
            
        tension, win = result
        
        # Create the relationship data object
        relationship_data = {
            "source_id": tension_id,
            "source_type": "Tension",
            "target_id": win_id,
            "target_type": "Win",
            "type": "LEADS_TO_WIN",
            "relationshipId": f"leads_to_win_{tension_id}_{win_id}_{uuid4().hex[:8]}",
            "contributionLevel": contribution_level,
            "directContribution": direct_contribution,
            "createdAt": datetime.utcnow().isoformat()
        }
        
        return relationship_data
    
    async def disconnect_tension_from_win(self, tension_id: str, win_id: str) -> bool:
        """
        Remove the LEADS_TO_WIN relationship between a Tension and a WIN.
        """
        return self.repository.disconnect_tension_from_win(tension_id, win_id)
    
    async def get_wins_from_tension(self, tension_id: str) -> List[Dict[str, Any]]:
        """
        Get all WINs that resulted from resolving a specific tension.
        """
        tension_data = self.repository.get_tension_with_relationships(tension_id)
        if not tension_data:
            return []
            
        return tension_data.get("resultingWins", [])
    
    async def connect_tension_to_project(self, tension_id: str, project_id: str,
                                    resolution_status: str = 'Proposed',
                                    resolution_approach: str = None,
                                    expected_outcome: str = None,
                                    alignment_score: float = None,
                                    priority: int = 0,
                                    start_date = None,
                                    target_resolution_date = None,
                                    actual_resolution_date = None,
                                    notes: str = None) -> Optional[Dict[str, Any]]:
        """
        Establishes a RESOLVES_TENSION relationship from a Project to a Tension
        according to the TRM Ontology V3.2.
        """
        result = self.repository.connect_tension_to_project(
            tension_id, project_id, resolution_status, resolution_approach,
            expected_outcome, alignment_score, priority, start_date,
            target_resolution_date, actual_resolution_date, notes
        )
        
        if not result:
            return None
            
        tension, project = result
        
        return {
            "tension": {
                "uid": tension.uid,
                "title": tension.title
            },
            "project": {
                "uid": project.uid,
                "name": project.name
            },
            "relationship": {
                "type": "RESOLVES_TENSION",
                "resolutionStatus": resolution_status,
                "priority": priority,
                "alignmentScore": alignment_score
            }
        }
    
    async def disconnect_project_from_tension(self, tension_id: str, project_id: str) -> bool:
        """
        Removes the RESOLVES_TENSION relationship between a Project and a Tension.
        """
        return self.repository.disconnect_project_from_tension(tension_id, project_id)
    
    async def get_projects_resolving_tension(self, tension_id: str, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Retrieves all Projects that are resolving a specific Tension.
        """
        projects = self.repository.get_projects_resolving_tension(tension_id, skip, limit)
        return [
            {
                "uid": project.uid,
                "name": project.name,
                "description": project.description,
                "status": project.status,
                "startDate": project.startDate.isoformat() if project.startDate else None,
                "endDate": project.endDate.isoformat() if project.endDate else None
            } for project in projects
        ]
