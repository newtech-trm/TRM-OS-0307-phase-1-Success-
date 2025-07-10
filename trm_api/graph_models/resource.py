from neomodel import (
    StructuredNode, StringProperty, UniqueIdProperty,
    DateTimeProperty, JSONProperty, RelationshipTo, RelationshipFrom
)
from datetime import datetime
import uuid

from trm_api.graph_models.base import BaseNode
from trm_api.graph_models.assigned_to_project import AssignedToProjectRel

class Resource(BaseNode):
    """
    Neo4j node representing a Resource in the system.
    Resources can be of different types: Financial, Knowledge, Human, Tool, Equipment, Space.
    """
    name = StringProperty(required=True)
    description = StringProperty()
    resourceType = StringProperty(required=True)
    status = StringProperty(default="available")
    ownerAgentId = StringProperty()
    details = JSONProperty(default={})

    # Relationships
    used_by_projects = RelationshipFrom('trm_api.graph_models.project.Project', 'HAS_RESOURCE')
    used_by_tasks = RelationshipFrom('trm_api.graph_models.task.Task', 'USES_RESOURCE')
    
    # AssignedToProject relationship - Resource được assign to Project
    assigned_to_projects = RelationshipTo('trm_api.graph_models.project.Project', 'ASSIGNED_TO_PROJECT', 
                                         model=AssignedToProjectRel)
    
    @classmethod
    def create_single(cls, **props):
        """
        Create a single new Resource node.
        Returns a single Resource instance.
        """
        # Create instance và save
        instance = cls(**props)
        instance.save()
        return instance
