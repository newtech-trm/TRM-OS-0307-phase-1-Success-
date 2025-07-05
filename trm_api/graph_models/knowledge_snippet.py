from neomodel import StringProperty, RelationshipFrom
from .base import BaseNode

class KnowledgeSnippet(BaseNode):
    """
    Represents a Knowledge Snippet in the TRM-OS ontology.
    A discrete piece of information or learning that can be reused.
    """
    # Core properties
    content = StringProperty(required=True)
    # Type of knowledge, e.g., 'Best Practice', 'Lesson Learned', 'Technical Note'
    snippet_type = StringProperty(required=True, index=True)
    status = StringProperty(default='validated') # e.g., 'candidate', 'validated', 'archived'

    # --- Relationships ---
    # A knowledge snippet can be generated from a WIN.
    source_win = RelationshipFrom('.win.WIN', 'GENERATES_KNOWLEDGE')

    def __str__(self):
        # Return the first 80 characters of the content for a concise representation
        return (self.content[:77] + '...') if len(self.content) > 80 else self.content
