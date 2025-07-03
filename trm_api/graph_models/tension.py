from neomodel import StringProperty, RelationshipTo, RelationshipFrom, IntegerProperty, DateTimeProperty, ArrayProperty
from trm_api.graph_models.resolves_tension import ResolvesTensionRel
from .base import BaseNode

class Tension(BaseNode):
    """
    Represents a Tension in the TRM-OS ontology.
    A tension is a gap between the current reality and a desired potential state.
    It can be a problem, risk, issue, opportunity, or any discrepancy that needs resolution.
    
    According to Ontology V3.2, Tension is a central concept that drives change and improvement.
    """
    # Core properties based on Ontology V3.2
    title = StringProperty(required=True, index=True, help_text="A concise summary of the tension")
    description = StringProperty(required=True, help_text="Detailed explanation of the tension, its context, and impact in markdown format")
    status = StringProperty(default='Open', help_text="Current state: Open, InProgress, Resolved, Closed")
    priority = IntegerProperty(default=0, help_text="The urgency level: 0-normal, 1-high, 2-critical")
    source = StringProperty(default='FounderInput', help_text="Where the tension was identified: FounderInput, CustomerFeedback, DataSensingAgent")
    sourceRef = StringProperty(required=False, help_text="A reference to the original source, like an email ID or URL")
    
    # DateTime properties
    creationDate = DateTimeProperty(default_now=True, help_text="Timestamp of creation")
    lastModifiedDate = DateTimeProperty(default_now=True, help_text="Timestamp of last update")
    resolutionDate = DateTimeProperty(required=False, help_text="Timestamp when the tension was resolved")
    
    # Extended properties
    tensionType = StringProperty(required=False, help_text="Type of tension: Problem, Opportunity, Risk, Conflict, Idea")
    currentState = StringProperty(required=False, help_text="Description of the current state or situation")
    desiredState = StringProperty(required=False, help_text="Description of the desired future state")
    impactAssessment = StringProperty(required=False, help_text="Assessment of the impact if the tension is not resolved")
    tags = ArrayProperty(StringProperty(), default=[], help_text="Tags for categorization and filtering")

    # --- Relationships as per Ontology V3.2 ---
    # A tension is reported by an agent
    reported_by = RelationshipTo('trm_api.graph_models.agent.Agent', 'REPORTED_BY')
    
    # A tension is owned by an agent responsible for its resolution
    owned_by = RelationshipTo('trm_api.graph_models.agent.Agent', 'OWNED_BY')
    
    # A tension affects specific projects
    affects = RelationshipTo('trm_api.graph_models.project.Project', 'AFFECTS')
    
    # Tasks that resolve this tension
    resolved_by_tasks = RelationshipFrom('trm_api.graph_models.task.Task', 'RESOLVES')
    
    # Projects that resolve this tension
    resolved_by_projects = RelationshipFrom('trm_api.graph_models.project.Project', 'RESOLVES_TENSION', model=ResolvesTensionRel)
    
    # A resolved tension leads to a WIN
    leads_to_win = RelationshipTo('trm_api.graph_models.win.WIN', 'LEADS_TO_WIN')

    def __str__(self):
        return self.title
