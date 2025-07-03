from neomodel import StringProperty, DateTimeProperty, RelationshipTo, RelationshipFrom, ZeroOrMore, ArrayProperty
from .base import BaseNode
from trm_api.graph_models.assigns_task import AssignsTaskRel

class User(BaseNode):
    """
    Represents a User in the TRM-OS ontology.
    A user is a person who interacts with the system.
    This model is aligned with the Ontology V3.2.
    """
    # --- Core properties aligned with Ontology V3.2 ---
    username = StringProperty(required=True, unique_index=True)
    email = StringProperty(index=True)
    full_name = StringProperty()
    hashed_password = StringProperty()
    is_active = StringProperty(default="true")
    is_superuser = StringProperty(default="false")
    
    # Extended properties
    profile_image_url = StringProperty()
    bio = StringProperty()
    preferences = ArrayProperty(StringProperty())
    
    # --- Relationships as per Ontology V3.2 ---
    # User assigns tasks
    assigns_tasks = RelationshipTo('trm_api.graph_models.task.Task', 'ASSIGNS_TASK', model=AssignsTaskRel)
    
    # User manages projects
    manages_projects = RelationshipTo('trm_api.graph_models.project.Project', 'MANAGES_PROJECT')
    
    # User has skills
    has_skills = RelationshipTo('trm_api.graph_models.skill.GraphSkill', 'HAS_SKILL')
    
    def __str__(self):
        return self.username or self.uid
