from enum import Enum, auto

# Enum cho Win
class WinStatus(str, Enum):
    """Các trạng thái của WIN."""
    DRAFT = "DRAFT"
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class WinType(str, Enum):
    """Các loại của WIN."""
    BUSINESS = "BUSINESS"
    PERSONAL = "PERSONAL"
    TEAM = "TEAM"
    PROJECT = "PROJECT"

# Enum cho Recognition
class RecognitionStatus(str, Enum):
    """Các trạng thái của Recognition."""
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"
    ARCHIVED = "ARCHIVED"

class RecognitionType(str, Enum):
    """Các loại của Recognition."""
    ACHIEVEMENT = "ACHIEVEMENT"
    APPRECIATION = "APPRECIATION"
    FEEDBACK = "FEEDBACK"
    MILESTONE = "MILESTONE"

# Enum cho Task
class TaskStatus(str, Enum):
    """Các trạng thái của Task."""
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    BLOCKED = "BLOCKED"
    CANCELLED = "CANCELLED"

class TaskType(str, Enum):
    """Các loại của Task."""
    FEATURE = "FEATURE"
    BUG = "BUG"
    IMPROVEMENT = "IMPROVEMENT"
    DOCUMENTATION = "DOCUMENTATION"
    RESEARCH = "RESEARCH"

# Enum cho KnowledgeSnippet
class KnowledgeSnippetType(str, Enum):
    """Các loại của KnowledgeSnippet."""
    CODE = "CODE"
    DOCUMENT = "DOCUMENT"
    INSIGHT = "INSIGHT"
    LEARNING = "LEARNING"

# Enum cho Event
class EventType(str, Enum):
    """Các loại của Event."""
    TASK_CREATED = "TASK_CREATED"
    TASK_UPDATED = "TASK_UPDATED"
    TASK_COMPLETED = "TASK_COMPLETED"
    WIN_CREATED = "WIN_CREATED"
    WIN_APPROVED = "WIN_APPROVED"
    RECOGNITION_GIVEN = "RECOGNITION_GIVEN"

# Enum cho Entity Types - Ontology V3.2
class EntityType(str, Enum):
    """Các loại entity trong ontology."""
    WIN = "WIN"
    RECOGNITION = "RECOGNITION"
    TASK = "TASK"
    EVENT = "EVENT"
    KNOWLEDGE_SNIPPET = "KNOWLEDGE_SNIPPET"
    PROJECT = "PROJECT"
    AGENT = "AGENT"
    USER = "USER"

# Enum cho Tension Priority
class Priority(str, Enum):
    """Priority levels cho tensions."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

# Enum cho Tension Types
class TensionType(str, Enum):
    """Types of tensions trong TRM-OS."""
    PROBLEM = "Problem"
    OPPORTUNITY = "Opportunity"
    RISK = "Risk"
    CONFLICT = "Conflict"
    IDEA = "Idea"
    RESOURCE_CONSTRAINT = "Resource_Constraint"
    PROCESS_IMPROVEMENT = "Process_Improvement"
    COMMUNICATION_BREAKDOWN = "Communication_Breakdown"
    STRATEGIC_MISALIGNMENT = "Strategic_Misalignment"
    UNKNOWN = "Unknown"

# Enum cho Agent Types
class AgentType(str, Enum):
    """Types of agents trong TRM-OS."""
    AI_AGENT = "AIAgent"
    HUMAN_AGENT = "HumanAgent"
    COMPOSITE_AGENT = "CompositeAgent"
    CUSTOM_AGENT = "CustomAgent"
    TEMPLATE_AGENT = "TemplateAgent"
