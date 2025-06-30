from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class TargetEntityTypeEnum(str, Enum):
    """Enum for all possible entity types that can be part of a relationship."""
    AGENT = "Agent"
    EVENT = "Event"
    KNOWLEDGE_SNIPPET = "KnowledgeSnippet"
    PROJECT = "Project"
    RECOGNITION = "Recognition"
    SKILL = "Skill"
    TASK = "Task"
    TEAM = "Team"
    TENSION = "Tension"
    TOOL = "Tool"
    USER = "User"
    WIN = "Win"


class RelationshipType(str, Enum):
    """Enum for all possible relationship types in the ontology."""
    # User-centric
    IDENTIFIED = "IDENTIFIED"      # User -> Tension
    PERFORMS = "PERFORMS"          # User -> Task
    HAS_SKILL = "HAS_SKILL"        # User -> Skill
    HAS_MEMBER = "HAS_MEMBER"      # Team -> User
    HAS_PARTICIPANT = "HAS_PARTICIPANT" # Project -> User
    AUTHORED = "AUTHORED"          # User -> KnowledgeSnippet
    RECEIVED = "RECEIVED"          # User -> Recognition
    GAVE = "GAVE"                  # User -> Recognition
    OWNS = "OWNS"                  # User -> Project/Team

    # Task-centric
    RELATES_TO = "RELATES_TO"      # Task -> Tension/Win
    REQUIRES = "REQUIRES"          # Task -> Skill
    USES = "USES"                  # Task -> Tool

    # Project/Team-centric
    HAS_TENSION = "HAS_TENSION"    # Project -> Tension
    RESOLVES_TENSION = "RESOLVES_TENSION"  # Project -> Tension
    ACHIEVED = "ACHIEVED"          # Project -> Win

    # Knowledge-centric
    DOCUMENTS = "DOCUMENTS"        # KnowledgeSnippet -> Win/Tension/Task
    IMPROVES = "IMPROVES"          # KnowledgeSnippet -> Skill
    CREATES_KNOWLEDGE = "CREATES_KNOWLEDGE"  # User/Agent/Task -> KnowledgeSnippet
    USES_KNOWLEDGE = "USES_KNOWLEDGE"        # User/Agent/Task -> KnowledgeSnippet
    
    # Event/Process-centric
    TRIGGERED_BY = "TRIGGERED_BY"  # Event/Task/Tension -> Event/Task/User
    TRIGGERS = "TRIGGERS"          # Event/Task/User -> Event/Task/Tension
    RELATED_TO = "RELATED_TO"      # Any entity -> Any entity


class Relationship(BaseModel):
    """
    Pydantic model representing a generic relationship between two nodes as returned by a Cypher query.
    
    Fields:
        source_id: ID of the source node
        source_type: Type of the source node
        target_id: ID of the target node
        target_type: Type of the target node
        type: Type of relationship
        createdAt: Timestamp when the relationship was created
        contributionLevel: Optional level of contribution (1-5) for certain relationship types
        directContribution: Optional boolean indicating if the contribution was direct
    """
    source_id: str
    source_type: str
    target_id: str
    target_type: str
    type: str
    createdAt: datetime
    contributionLevel: int = None
    directContribution: bool = None
    relationshipId: str = None

    model_config = {
        "from_attributes": True,
        "populate_by_name": True
    }
