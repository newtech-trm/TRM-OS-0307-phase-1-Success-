from neomodel import StructuredRel, StringProperty, DateTimeProperty, BooleanProperty
from datetime import datetime

class ManagesProjectRel(StructuredRel):
    """
    Relationship representing an Agent managing a Project.
    
    This relationship captures the management responsibility of an Agent over a Project,
    including role type, assignment date, and management context.
    """
    role = StringProperty(default="project_manager", 
                        help_text="Role of the agent in managing this project (e.g., project_manager, sponsor, coordinator)")
    
    assigned_at = DateTimeProperty(default=datetime.now,
                                help_text="When the agent was assigned to manage this project")
    
    context = StringProperty(help_text="Additional context about the management relationship")
    
    notes = StringProperty(help_text="Notes about this management relationship")
    
    is_primary = BooleanProperty(default=True, 
                                help_text="Whether this agent is the primary manager for the project")
    
    def __str__(self):
        return f"ManagesProject({self.role})"
