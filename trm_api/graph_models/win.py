from neomodel import StringProperty, RelationshipFrom, RelationshipTo, IntegerProperty, ArrayProperty

from .base import BaseNode
# Assuming relationship models are in the same directory or a 'relationships' subdirectory handled by __init__.py
from .leads_to_win import LeadsToWinRel
from .recognizes_win import RecognizesWinRel # Assumes recognizes_win.py defines RecognizesWinRel
from .generates_event import GeneratesEventRel # Assumes generates_event.py defines GeneratesEventRel

# Define choices for status and winType to ensure consistency
WIN_STATUS_CHOICES = {
    "draft": "Draft",
    "under_review": "Under Review",
    "published": "Published",
    "archived": "Archived",
}

WIN_TYPE_CHOICES = {
    "problem_resolution": "Problem Resolution",
    "insight_discovery": "Insight Discovery",
    "process_optimization": "Process Optimization",
    "learning_milestone": "Learning Milestone",
    "strategic_achievement": "Strategic Achievement",
}

class WIN(BaseNode):
    """
    Represents a WIN (Wisdom-Infused Narrative) in the TRM-OS ontology.
    A WIN is a significant, valuable outcome, insight, learning, or solution, often resulting 
    from resolving a tension or completing a project/task.
    """
    # Core properties from BaseNode: uid, created_at, updated_at

    # Specific WIN properties
    name = StringProperty(required=True, index=True, description="A concise and descriptive name for the WIN.")
    narrative = StringProperty(required=True, description="The detailed story of the WIN, including context, actions, outcomes, and key learnings.")
    status = StringProperty(choices=WIN_STATUS_CHOICES, default="draft", description="The current status of the WIN in its lifecycle.")
    winType = StringProperty(choices=WIN_TYPE_CHOICES, description="The category or type of the WIN.")
    impact_level = IntegerProperty(default=1, description="A numerical representation of the WIN's perceived impact or significance (e.g., 1-Low to 5-High).")
    tags = ArrayProperty(StringProperty(), default=list, description="Relevant tags for categorizing and searching WINs.")

    # --- Relationships ---

    # How this WIN came to be (sources)
    # '.event.Event' assumes event.py exists in the current package (graph_models)
    led_to_by_events = RelationshipFrom('.event.Event', 'LEADS_TO_WIN', model=LeadsToWinRel)
    led_to_by_projects = RelationshipFrom('.project.Project', 'LEADS_TO_WIN', model=LeadsToWinRel)
    led_to_by_tensions = RelationshipFrom('.tension.Tension', 'LEADS_TO_WIN', model=LeadsToWinRel)
    # Ontology V3.2 defines that Tensions can lead to WINs through the LEADS_TO_WIN relationship

    # What this WIN is recognized by
    # '.recognition.Recognition' assumes recognition.py exists here
    recognized_by_recognitions = RelationshipFrom('.recognition.Recognition', 'RECOGNIZES_WIN', model=RecognizesWinRel)

    # What this WIN generates
    # '.knowledge_snippet.KnowledgeSnippet' assumes knowledge_snippet.py defines KnowledgeSnippet.
    # Ontology V3.2 might specify KnowledgeAsset instead or a specific relationship model for GENERATES_KNOWLEDGE.
    generates_knowledge_snippets = RelationshipTo('.knowledge_snippet.KnowledgeSnippet', 'GENERATES_KNOWLEDGE')

    # Events generated by this WIN (e.g., WIN_PUBLISHED_EVENT)
    generates_events = RelationshipTo('.event.Event', 'GENERATES_EVENT', model=GeneratesEventRel)

    def __str__(self):
        return self.name
