from neomodel import StringProperty, RelationshipTo, RelationshipFrom, ArrayProperty, DateTimeProperty, JSONProperty, BooleanProperty, IntegerProperty
from trm_api.graph_models.resolves_tension import ResolvesTensionRel
from trm_api.graph_models.generates_event import GeneratesEventRel
from trm_api.graph_models.leads_to_win import LeadsToWinRel
from trm_api.graph_models.is_part_of_project import IsPartOfProjectRel
from trm_api.graph_models.manages_project import ManagesProjectRel
from trm_api.graph_models.assigned_to_project import AssignedToProjectRel
from trm_api.graph_models.requires_resource import RequiresResourceRel
from .base import BaseNode

class Project(BaseNode):
    """
    Represents a Project in the TRM-OS ontology.
    
    Projects are strategic initiatives with defined goals, resources, and timelines
    that respond to tensions or pursue opportunities within TRM.
    """
    # Core properties
    title = StringProperty(required=True, index=True)
    description = StringProperty()
    status = StringProperty(default='active') # e.g., 'active', 'completed', 'on_hold'
    
    # Extended properties from Ontology V3.2
    goal = StringProperty(help_text="The primary objective that this project aims to achieve")
    scope = StringProperty(help_text="Boundaries and limitations of the project")
    priority = IntegerProperty(default=3, help_text="Priority level from 1 (highest) to 5 (lowest)")
    project_type = StringProperty(help_text="Type of project, e.g., 'development', 'research', 'improvement'")
    tags = ArrayProperty(StringProperty(), default=[], help_text="Keywords for easier categorization and search")
    start_date = DateTimeProperty(help_text="When the project was started or is scheduled to start")
    target_end_date = DateTimeProperty(help_text="Target date for project completion")
    actual_end_date = DateTimeProperty(help_text="Actual date when project was completed")
    health = StringProperty(default='normal', help_text="Current health status of the project, e.g., 'at_risk', 'normal', 'excelling'")
    metrics = JSONProperty(help_text="Key performance indicators and success metrics for the project")
    is_strategic = BooleanProperty(default=False, help_text="Whether this is a strategic project aligned with organizational goals")

    # --- Relationships ---
    # A project consists of multiple tasks.
    # Use a full path forward reference to avoid circular import issues
    # Use IsPartOfProjectRel to store relationship properties according to ontology V3.2
    tasks = RelationshipTo('trm_api.graph_models.task.Task', 'HAS_TASK', model=IsPartOfProjectRel)
    
    # A project can resolve multiple tensions
    # Use ResolvesTensionRel to store relationship properties according to ontology V3.2
    resolves_tensions = RelationshipTo('trm_api.graph_models.tension.Tension', 'RESOLVES_TENSION', model=ResolvesTensionRel)
    
    # A project can generate events
    # Use GeneratesEventRel to store relationship properties according to ontology V3.2
    generates_events = RelationshipTo('trm_api.graph_models.event.Event', 'GENERATES_EVENT', model=GeneratesEventRel)
    
    # A project can lead to WINs (Wisdom-Infused Narratives)
    # Use LeadsToWinRel to store relationship properties according to ontology V3.2
    leads_to_wins = RelationshipTo('trm_api.graph_models.win.WIN', 'LEADS_TO_WIN', model=LeadsToWinRel)
    
    # Resources assigned to this project
    # Use AssignedToProjectRel to store relationship properties according to ontology V3.2
    assigned_resources = RelationshipFrom('trm_api.graph_models.resource.Resource', 'ASSIGNED_TO_PROJECT', model=AssignedToProjectRel)
    
    # Resources required by this project
    # Use RequiresResourceRel to store relationship properties according to ontology V3.2
    requires_resources = RelationshipTo('trm_api.graph_models.resource.Resource', 'REQUIRES_RESOURCE', model=RequiresResourceRel)
    
    # Agents and Users who manage this project
    # Use ManagesProjectRel to store relationship properties according to ontology V3.2
    managed_by_agents = RelationshipFrom('trm_api.graph_models.agent.Agent', 'MANAGES_PROJECT', model=ManagesProjectRel)
    managed_by_users = RelationshipFrom('trm_api.graph_models.user.User', 'MANAGES_PROJECT', model=ManagesProjectRel)
    
    @property
    def managed_by(self):
        """Combined managers (both agents and users)"""
        return list(self.managed_by_agents.all()) + list(self.managed_by_users.all())
    
    # Parent project (if this is a sub-project)
    parent_project = RelationshipTo('Project', 'IS_SUBPROJECT_OF')
    
    # Child projects (if this is a parent project)
    sub_projects = RelationshipFrom('Project', 'IS_SUBPROJECT_OF')
    
    # Knowledge assets created or used by this project
    uses_knowledge = RelationshipTo('trm_api.graph_models.knowledge_asset.KnowledgeAsset', 'USES_KNOWLEDGE')
    creates_knowledge = RelationshipTo('trm_api.graph_models.knowledge_asset.KnowledgeAsset', 'CREATES_KNOWLEDGE')

    def __str__(self):
        return self.title
