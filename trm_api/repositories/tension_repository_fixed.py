from typing import Optional, List, Tuple, Dict, Any
from datetime import datetime
import uuid
from neomodel import db

from trm_api.models.tension import TensionCreate, TensionUpdate
from trm_api.graph_models.tension import Tension as GraphTension
from trm_api.graph_models.project import Project as GraphProject
from trm_api.graph_models.agent import Agent as GraphAgent
from trm_api.graph_models.task import Task as GraphTask
from trm_api.graph_models.win import WIN as GraphWIN

class TensionRepository:
    """
    Repository for handling all database operations related to Tensions.
    """

    @db.transaction
    def create_tension(self, tension_data: TensionCreate) -> Optional[GraphTension]:
        """
        Creates a new Tension and connects it to its Project context according to Ontology V3.2.
        """
        # 1. Find the project that this tension affects
        try:
            project = GraphProject.nodes.get(uid=tension_data.projectId)
        except GraphProject.DoesNotExist:
            # Can't create a tension for a non-existent project
            return None

        # 2. Create the new tension node with properties following Ontology V3.2
        tension_dict = tension_data.model_dump(exclude={'projectId', 'reporterAgentId', 'ownerAgentId'})
        
        # Set default dates if not provided
        if 'creationDate' not in tension_dict:
            tension_dict['creationDate'] = datetime.utcnow()
        if 'lastModifiedDate' not in tension_dict:
            tension_dict['lastModifiedDate'] = datetime.utcnow()
            
        new_tension = GraphTension(**tension_dict).save()

        # 3. Connect the tension to the affected project using AFFECTS relationship
        new_tension.affects.connect(project)

        # 4. Connect to reporter agent if specified
        if hasattr(tension_data, 'reporterAgentId') and tension_data.reporterAgentId:
            try:
                reporter_agent = GraphAgent.nodes.get(uid=tension_data.reporterAgentId)
                new_tension.reported_by.connect(reporter_agent)
            except GraphAgent.DoesNotExist:
                # Log this, but continue with tension creation
                print(f"Warning: Reporter agent {tension_data.reporterAgentId} not found")

        # 5. Connect to owner agent if specified
        if hasattr(tension_data, 'ownerAgentId') and tension_data.ownerAgentId:
            try:
                owner_agent = GraphAgent.nodes.get(uid=tension_data.ownerAgentId)
                new_tension.owned_by.connect(owner_agent)
            except GraphAgent.DoesNotExist:
                # Log this, but continue with tension creation
                print(f"Warning: Owner agent {tension_data.ownerAgentId} not found")

        return new_tension

    def get_tension_by_uid(self, uid: str) -> Optional[GraphTension]:
        """
        Retrieves a Tension node by its unique ID.
        """
        try:
            return GraphTension.nodes.get(uid=uid)
        except GraphTension.DoesNotExist:
            return None

    def list_tensions_for_project(self, project_id: str, skip: int = 0, limit: int = 100) -> List[GraphTension]:
        """
        Lists all tensions that are related to a specific project.
        This includes both tensions that AFFECT the project and tensions that the project RESOLVES.
        
        Following Ontology V3.2, tensions can be related to projects in two ways:
        1. Tension -[:AFFECTS]-> Project
        2. Project -[:RESOLVES_TENSION]-> Tension
        """
        try:
            project = GraphProject.nodes.get(uid=project_id)
        except GraphProject.DoesNotExist:
            return []

        # Query tensions related to this project via both relationship types
        results, meta = db.cypher_query(
            """
            MATCH (t:Tension)
            WHERE (t)-[:AFFECTS]->(:Project {uid: $project_id}) OR 
                  (:Project {uid: $project_id})-[:RESOLVES_TENSION]->(t)
            RETURN DISTINCT t
            SKIP $skip LIMIT $limit
            """,
            {'project_id': project_id, 'skip': skip, 'limit': limit}
        )

        # Convert the results to GraphTension objects
        return [GraphTension.inflate(row[0]) for row in results]

    def update_tension(self, uid: str, tension_data: TensionUpdate) -> Optional[GraphTension]:
        """
        Updates an existing tension following Ontology V3.2.
        """
        tension = self.get_tension_by_uid(uid)
        if not tension:
            return None

        # Prepare data for update, excluding relationship fields
        update_dict = tension_data.model_dump(
            exclude_unset=True,
            exclude={'ownerAgentId'}
        )
            
        # Update the tension node properties
        for key, value in update_dict.items():
            setattr(tension, key, value)

        # Handle ownerAgentId separately to update the relationship
        if hasattr(tension_data, 'ownerAgentId') and tension_data.ownerAgentId is not None:
            # Disconnect any existing owner agents
            for owner in tension.owned_by.all():
                tension.owned_by.disconnect(owner)
                
            # Connect to new owner agent if provided and not None
            if tension_data.ownerAgentId:
                try:
                    new_owner = GraphAgent.nodes.get(uid=tension_data.ownerAgentId)
                    tension.owned_by.connect(new_owner)
                except GraphAgent.DoesNotExist:
                    # Log but continue with other updates
                    print(f"Warning: Owner agent {tension_data.ownerAgentId} not found")

        # Update resolution date if status is now Resolved and no resolution date exists
        if hasattr(tension_data, 'status') and tension_data.status == 'Resolved' and not tension.resolutionDate:
            tension.resolutionDate = datetime.utcnow()

        # Update lastModifiedDate
        tension.lastModifiedDate = datetime.utcnow()
        tension.save()

        return tension

    def delete_tension(self, uid: str) -> bool:
        """
        Deletes a tension by its unique ID.
        """
        tension = self.get_tension_by_uid(uid)
        if not tension:
            return False
        
        tension.delete()
        return True

    # New methods to support additional Ontology V3.2 relationships
    
    @db.transaction
    def connect_task_to_tension(self, tension_id: str, task_id: str) -> bool:
        """
        Establishes a RESOLVES relationship from a Task to a Tension.
        This indicates that the Task was created to resolve the specified Tension.
        
        According to Ontology V3.2, the RESOLVES relationship is a key connection.
        """
        # Get the nodes
        tension = self.get_tension_by_uid(tension_id)
        if not tension:
            return False
        
        try:
            task = GraphTask.nodes.get(uid=task_id)
        except GraphTask.DoesNotExist:
            return False
        
        # Create the relationship
        task.resolves.connect(tension)
        return True
        
    @db.transaction
    def disconnect_task_from_tension(self, tension_id: str, task_id: str) -> bool:
        """
        Remove the RESOLVES relationship between a Task and a Tension.
        """
        # Get the nodes
        tension = self.get_tension_by_uid(tension_id)
        if not tension:
            return False
        
        try:
            task = GraphTask.nodes.get(uid=task_id)
        except GraphTask.DoesNotExist:
            return False
        
        # Remove the relationship
        task.resolves.disconnect(tension)
        return True
    
    def get_tasks_resolving_tension(self, tension_id: str, skip: int = 0, limit: int = 100) -> List[GraphTask]:
        """
        Get all tasks that are working to resolve a tension.
        Uses the RESOLVES relationship as defined in Ontology V3.2.
        """
        tension = self.get_tension_by_uid(tension_id)
        if not tension:
            return []
        
        return list(tension.resolved_by_tasks.all()[skip:skip+limit])
        
    @db.transaction
    def connect_tension_to_win(self, tension_id: str, win_id: str) -> bool:
        """
        Establishes a LEADS_TO_WIN relationship from a Tension to a WIN.
        This indicates that resolving the Tension led to the specified WIN.
        
        According to Ontology V3.2, this relationship captures the value creation process.
        """
        # Get the nodes
        tension = self.get_tension_by_uid(tension_id)
        if not tension:
            return False
        
        try:
            win = GraphWIN.nodes.get(uid=win_id)
        except GraphWIN.DoesNotExist:
            return False
        
        # Create the relationship
        tension.leads_to_win.connect(win)
        return True
    
    @db.transaction
    def disconnect_tension_from_win(self, tension_id: str, win_id: str) -> bool:
        """
        Remove the LEADS_TO_WIN relationship between a Tension and a WIN.
        """
        # Get the nodes
        tension = self.get_tension_by_uid(tension_id)
        if not tension:
            return False
        
        try:
            win = GraphWIN.nodes.get(uid=win_id)
        except GraphWIN.DoesNotExist:
            return False
        
        # Remove the relationship
        tension.leads_to_win.disconnect(win)
        return True
    
    def get_tension_with_relationships(self, tension_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a tension with all its relationships loaded.
        This provides a comprehensive view of the tension as defined in Ontology V3.2.
        """
        tension = self.get_tension_by_uid(tension_id)
        if not tension:
            return None
        
        # Create a dictionary to hold all the tension data including relationships
        tension_data = {
            # Basic properties
            "uid": tension.uid,
            "title": tension.title,
            "description": tension.description,
            "status": tension.status,
            "priority": tension.priority,
            "source": tension.source if hasattr(tension, 'source') else None,
            "sourceRef": tension.sourceRef if hasattr(tension, 'sourceRef') else None,
            "creationDate": tension.creationDate.isoformat() if hasattr(tension, 'creationDate') else None,
            "lastModifiedDate": tension.lastModifiedDate.isoformat() if hasattr(tension, 'lastModifiedDate') else None,
            "resolutionDate": tension.resolutionDate.isoformat() if hasattr(tension, 'resolutionDate') and tension.resolutionDate else None,
            
            # Extended properties
            "tensionType": tension.tensionType if hasattr(tension, 'tensionType') else None,
            "currentState": tension.currentState if hasattr(tension, 'currentState') else None,
            "desiredState": tension.desiredState if hasattr(tension, 'desiredState') else None,
            "impactAssessment": tension.impactAssessment if hasattr(tension, 'impactAssessment') else None,
            "tags": tension.tags if hasattr(tension, 'tags') else [],
            
            # Relationships
            "reporterAgents": [{
                "uid": agent.uid,
                "name": agent.name
            } for agent in tension.reported_by.all()],
            
            "ownerAgents": [{
                "uid": agent.uid,
                "name": agent.name
            } for agent in tension.owned_by.all()],
            
            "affectedProjects": [{
                "uid": project.uid,
                "name": project.name
            } for project in tension.affects.all()],
            
            "resolvingTasks": [{
                "uid": task.uid,
                "title": task.title
            } for task in tension.resolved_by_tasks.all()],
            
            "resolvingProjects": [{
                "uid": project.uid,
                "name": project.name
            } for project in tension.resolved_by_projects.all()],
            
            "resultingWins": [{
                "uid": win.uid,
                "title": win.title
            } for win in tension.leads_to_win.all()]
        }
        
        return tension_data
    
    @db.transaction
    def connect_tension_to_project(self, tension_uid: str, project_uid: str,
                            resolution_status: str = 'Proposed',
                            resolution_approach: str = None,
                            expected_outcome: str = None,
                            alignment_score: float = None,
                            priority: int = 0,  # Updated to use int priority per Ontology V3.2
                            start_date = None,
                            target_resolution_date = None,
                            actual_resolution_date = None,
                            notes: str = None) -> Optional[Tuple[GraphTension, GraphProject]]:
        """
        Establishes a RESOLVES_TENSION relationship from a Project to a Tension
        with all required properties according to the TRM Ontology V3.2.
        
        Args:
            tension_uid: UID of the tension
            project_uid: UID of the project
            resolution_status: Status of the resolution (e.g. 'Proposed', 'ResolutionInProgress')
            resolution_approach: Description of the approach to resolve the tension
            expected_outcome: Expected outcome after tension resolution
            alignment_score: Score (0.0-1.0) evaluating how well the project fits for resolving this tension
            priority: Priority level (0-normal, 1-high, 2-critical)
            start_date: Date when project started resolving this tension
            target_resolution_date: Target date for tension resolution
            actual_resolution_date: Actual date when tension was resolved
            notes: Additional notes about this relationship
        
        Returns:
            Tuple of (tension, project) if successful, None otherwise
        """
        # 1. Get both the tension and project nodes
        tension = self.get_tension_by_uid(tension_uid)
        if not tension:
            return None
            
        try:
            project = GraphProject.nodes.get(uid=project_uid)
        except GraphProject.DoesNotExist:
            return None
        
        # 2. Create the RESOLVES_TENSION relationship with all properties
        relationship_props = {
            'relationshipId': str(uuid.uuid4()),
            'resolutionStatus': resolution_status,
            'creationDate': datetime.now(),
            'lastModifiedDate': datetime.now()
        }
        
        # Add optional properties if provided
        if resolution_approach:
            relationship_props['resolutionApproach'] = resolution_approach
        if expected_outcome:
            relationship_props['expectedOutcome'] = expected_outcome
        if alignment_score is not None:
            relationship_props['alignmentScore'] = alignment_score
        if priority:
            relationship_props['priority'] = priority
        if start_date:
            relationship_props['startDate'] = start_date
        if target_resolution_date:
            relationship_props['targetResolutionDate'] = target_resolution_date
        if actual_resolution_date:
            relationship_props['actualResolutionDate'] = actual_resolution_date
        if notes:
            relationship_props['notes'] = notes
            
        # Connect with relationship properties
        project.resolves_tension.connect(tension, relationship_props)
        
        return (tension, project)
        
    def get_projects_resolving_tension(self, tension_uid: str, skip: int = 0, limit: int = 100) -> List[GraphProject]:
        """
        Retrieves all Projects that are resolving a specific Tension.
        Uses the RESOLVES_TENSION relationship as defined in Ontology V3.2.
        """
        tension = self.get_tension_by_uid(tension_uid)
        if not tension:
            return []
            
        # Get all projects connected with RESOLVES_TENSION relationship
        return list(tension.resolved_by_projects.all()[skip:skip+limit])
        
    @db.transaction
    def disconnect_project_from_tension(self, tension_uid: str, project_uid: str) -> bool:
        """
        Removes the RESOLVES_TENSION relationship between a Project and a Tension.
        
        Returns True if disconnection was successful, False otherwise.
        """
        # Get the nodes
        tension = self.get_tension_by_uid(tension_uid)
        if not tension:
            return False
            
        try:
            project = GraphProject.nodes.get(uid=project_uid)
        except GraphProject.DoesNotExist:
            return False
            
        # Remove the relationship
        project.resolves_tension.disconnect(tension)
        
        return True
