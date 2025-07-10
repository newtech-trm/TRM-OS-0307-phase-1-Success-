from typing import Optional, List, Tuple, Union, Dict, Any
from neomodel import db
from datetime import datetime
import uuid

from trm_api.graph_models.event import Event as GraphEvent
from trm_api.graph_models.project import Project as GraphProject
from trm_api.graph_models.task import Task as GraphTask
from trm_api.graph_models.agent import Agent as GraphAgent
from trm_api.models.event import EventCreate  # Pydantic model for API data

class EventRepository:
    def create_event(self, event_data: EventCreate) -> GraphEvent:
        """
        Creates a new event.
        """
        event = GraphEvent(
            name=event_data.event_type,  # Use event_type as name for GraphEvent
            description=getattr(event_data, 'description', None),
            payload=event_data.payload
        ).save()
        return event

    def get_event_by_uid(self, uid: str) -> Optional[GraphEvent]:
        """
        Retrieves an event by its unique ID.
        """
        try:
            return GraphEvent.nodes.get(uid=uid)
        except GraphEvent.DoesNotExist:
            return None

    def list_events(self, skip: int = 0, limit: int = 100, 
                  event_type: str = None) -> List[GraphEvent]:
        """
        Retrieves a list of events with pagination and optional filtering.
        """
        if event_type:
            return GraphEvent.nodes.filter(event_type=event_type)[skip:skip + limit]
        else:
            return GraphEvent.nodes.all()[skip:skip + limit]

    def update_event(self, uid: str, **kwargs) -> Optional[GraphEvent]:
        """
        Updates an existing event.
        Note: In many cases, events should be immutable, but this method is provided
        for completeness and special cases.
        """
        event = self.get_event_by_uid(uid)
        if not event:
            return None

        for key, value in kwargs.items():
            if hasattr(event, key):
                setattr(event, key, value)
        
        event.save()
        return event

    def delete_event(self, uid: str) -> bool:
        """
        Deletes an event by its unique ID.
        Note: In many cases, events should not be deleted, but this method is provided
        for completeness and special cases.
        Returns True if deletion was successful, False otherwise.
        """
        event = self.get_event_by_uid(uid)
        if not event:
            return False
        
        event.delete()
        return True
        
    @db.transaction
    def connect_project_to_event(self, project_uid: str, event_uid: str,
                             generation_type: str = 'Direct',
                             impact: int = None,
                             is_verified: bool = None,
                             verification_source: str = None,
                             context: str = None,
                             notes: str = None) -> Optional[Tuple[GraphProject, GraphEvent]]:
        """
        Establishes a GENERATES_EVENT relationship from a Project to an Event
        with all required properties according to the TRM Ontology V3.2.
        
        Args:
            project_uid: UID of the project
            event_uid: UID of the event
            generation_type: Type of generation ('Direct', 'Indirect', 'Automated', 'Manual', 'System')
            impact: Impact level (1-5)
            is_verified: Whether this relationship is verified
            verification_source: Source of verification
            context: Additional context for this relationship
            notes: Additional notes about this relationship
            
        Returns:
            Tuple of (project, event) if successful, None otherwise
        """
        # 1. Get both the project and event nodes
        try:
            project = GraphProject.nodes.get(uid=project_uid)
        except GraphProject.DoesNotExist:
            return None
            
        try:
            event = GraphEvent.nodes.get(uid=event_uid)
        except GraphEvent.DoesNotExist:
            return None
        
        # 2. Create the GENERATES_EVENT relationship with all properties
        relationship_props = {
            'relationshipId': str(uuid.uuid4()),
            'generationType': generation_type,
            'creationDate': datetime.now(),
            'lastModifiedDate': datetime.now()
        }
        
        # Add optional properties if provided
        if impact is not None:
            relationship_props['impact'] = impact
        if is_verified is not None:
            relationship_props['isVerified'] = is_verified
        if verification_source:
            relationship_props['verificationSource'] = verification_source
        if context:
            relationship_props['context'] = context
        if notes:
            relationship_props['notes'] = notes
        
        # Connect with relationship properties
        project.generates_events.connect(event, relationship_props)
        
        return (project, event)
        
    @db.transaction
    def connect_task_to_event(self, task_uid: str, event_uid: str,
                            generation_type: str = 'Direct',
                            impact: int = None,
                            is_verified: bool = None,
                            verification_source: str = None,
                            context: str = None,
                            notes: str = None) -> Optional[Tuple[GraphTask, GraphEvent]]:
        """
        Establishes a GENERATES_EVENT relationship from a Task to an Event
        with all required properties according to the TRM Ontology V3.2.
        """
        # 1. Get both the task and event nodes
        try:
            task = GraphTask.nodes.get(uid=task_uid)
        except GraphTask.DoesNotExist:
            return None
            
        try:
            event = GraphEvent.nodes.get(uid=event_uid)
        except GraphEvent.DoesNotExist:
            return None
        
        # 2. Create the GENERATES_EVENT relationship with all properties
        relationship_props = {
            'relationshipId': str(uuid.uuid4()),
            'generationType': generation_type,
            'creationDate': datetime.now(),
            'lastModifiedDate': datetime.now()
        }
        
        # Add optional properties if provided
        if impact is not None:
            relationship_props['impact'] = impact
        if is_verified is not None:
            relationship_props['isVerified'] = is_verified
        if verification_source:
            relationship_props['verificationSource'] = verification_source
        if context:
            relationship_props['context'] = context
        if notes:
            relationship_props['notes'] = notes
        
        # Connect with relationship properties
        task.generates_events.connect(event, relationship_props)
        
        return (task, event)
        
    @db.transaction
    def connect_agent_to_event(self, agent_uid: str, event_uid: str,
                            generation_type: str = 'Direct',
                            impact: int = None,
                            is_verified: bool = None,
                            verification_source: str = None,
                            context: str = None,
                            notes: str = None) -> Optional[Tuple[GraphAgent, GraphEvent]]:
        """
        Establishes a GENERATES_EVENT relationship from an Agent to an Event
        with all required properties according to the TRM Ontology V3.2.
        """
        # 1. Get both the agent and event nodes
        try:
            agent = GraphAgent.nodes.get(uid=agent_uid)
        except GraphAgent.DoesNotExist:
            return None
            
        try:
            event = GraphEvent.nodes.get(uid=event_uid)
        except GraphEvent.DoesNotExist:
            return None
        
        # 2. Create the GENERATES_EVENT relationship with all properties
        relationship_props = {
            'relationshipId': str(uuid.uuid4()),
            'generationType': generation_type,
            'creationDate': datetime.now(),
            'lastModifiedDate': datetime.now()
        }
        
        # Add optional properties if provided
        if impact is not None:
            relationship_props['impact'] = impact
        if is_verified is not None:
            relationship_props['isVerified'] = is_verified
        if verification_source:
            relationship_props['verificationSource'] = verification_source
        if context:
            relationship_props['context'] = context
        if notes:
            relationship_props['notes'] = notes
        
        # Connect with relationship properties
        agent.generates_events.connect(event, relationship_props)
        
        return (agent, event)
        
    def get_event_sources(self, event_uid: str) -> Dict[str, List[Union[GraphProject, GraphTask, GraphAgent]]]:
        """
        Retrieves all Projects, Tasks and Agents that generated a specific Event.
        
        Returns:
            Dictionary with keys 'projects', 'tasks', 'agents' and corresponding lists of entities.
        """
        event = self.get_event_by_uid(event_uid)
        if not event:
            return {'projects': [], 'tasks': [], 'agents': []}
            
        # Get all connected entities by relationship type
        result = {
            'projects': list(event.generated_by_projects.all()),
            'tasks': list(event.generated_by_tasks.all()),
            'agents': list(event.generated_by_agents.all())
        }
        
        return result
        
    @db.transaction
    def disconnect_entity_from_event(self, 
                                entity_type: str, 
                                entity_uid: str, 
                                event_uid: str) -> bool:
        """
        Removes the GENERATES_EVENT relationship between an entity (Project, Task, Agent) and an Event.
        
        Args:
            entity_type: Type of entity ('project', 'task', or 'agent')
            entity_uid: UID of the entity
            event_uid: UID of the event
            
        Returns:
            True if disconnection was successful, False otherwise.
        """
        # 1. Validate entity type
        if entity_type not in ['project', 'task', 'agent']:
            return False
            
        # 2. Get the event
        event = self.get_event_by_uid(event_uid)
        if not event:
            return False
            
        # 3. Get the entity and disconnect based on type
        if entity_type == 'project':
            try:
                project = GraphProject.nodes.get(uid=entity_uid)
                project.generates_events.disconnect(event)
                return True
            except GraphProject.DoesNotExist:
                return False
        elif entity_type == 'task':
            try:
                task = GraphTask.nodes.get(uid=entity_uid)
                task.generates_events.disconnect(event)
                return True
            except GraphTask.DoesNotExist:
                return False
        elif entity_type == 'agent':
            try:
                agent = GraphAgent.nodes.get(uid=entity_uid)
                agent.generates_events.disconnect(event)
                return True
            except GraphAgent.DoesNotExist:
                return False
                
        return False
