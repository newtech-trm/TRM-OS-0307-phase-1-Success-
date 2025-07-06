"""
Core types and data structures for Adaptive Learning System

Follows TRM-OS philosophy: Recognition → Event → WIN through continuous learning
"""

from datetime import datetime
from typing import Dict, List, Any, Optional, Union, Tuple
from enum import Enum
from pydantic import BaseModel, Field, ConfigDict
from uuid import uuid4


def safe_enum_value(enum_obj):
    """Safely get enum value, handling both enum objects and strings"""
    if hasattr(enum_obj, 'value'):
        return enum_obj.value
    return str(enum_obj)


class ExperienceType(Enum):
    """Các loại experience mà hệ thống có thể học"""
    AGENT_CREATION = "agent_creation"
    PROJECT_MANAGEMENT = "project_management"
    TENSION_RESOLUTION = "tension_resolution"
    PERFORMANCE_OPTIMIZATION = "performance_optimization"
    PATTERN_RECOGNITION = "pattern_recognition"
    BEHAVIORAL_ADAPTATION = "behavioral_adaptation"
    GOAL_ACHIEVEMENT = "goal_achievement"
    FEEDBACK_PROCESSING = "feedback_processing"
    # NEW: Conversational Interface Experience Types
    NLP_PARSING = "nlp_parsing"
    ENTITY_EXTRACTION = "entity_extraction"
    ACTION_MAPPING = "action_mapping"
    RESPONSE_GENERATION = "response_generation"
    CONVERSATION_PATTERN = "conversation_pattern"
    FEEDBACK_ADAPTATION = "feedback_adaptation"
    INTENT_RECOGNITION = "intent_recognition"
    CONTEXT_UNDERSTANDING = "context_understanding"
    # NEW: Quantum Experience Types
    QUANTUM_STATE_DETECTION = "quantum_state_detection"
    QUANTUM_OPTIMIZATION = "quantum_optimization"
    STATE_TRANSITION = "state_transition"
    WIN_PROBABILITY_CALCULATION = "win_probability_calculation"
    COHERENCE_MONITORING = "coherence_monitoring"
    QUANTUM_ENTANGLEMENT = "quantum_entanglement"
    QUANTUM_MEASUREMENT = "quantum_measurement"
    QUANTUM_EVOLUTION = "quantum_evolution"


class MetricType(Enum):
    """Types of performance metrics"""
    EFFICIENCY = "efficiency"                  # Time/resource efficiency
    ACCURACY = "accuracy"                     # Correctness of results
    SUCCESS_RATE = "success_rate"             # Success percentage
    CONFIDENCE = "confidence"                 # Confidence levels
    QUALITY = "quality"                       # Output quality scores
    LEARNING_SPEED = "learning_speed"         # Rate of improvement
    ADAPTATION_RATE = "adaptation_rate"       # Speed of behavioral change


class AdaptationType(Enum):
    """Types of adaptations"""
    PARAMETER_ADJUSTMENT = "parameter_adjustment"   # Adjust algorithm parameters
    STRATEGY_CHANGE = "strategy_change"            # Change approach/strategy  
    THRESHOLD_MODIFICATION = "threshold_modification" # Modify decision thresholds
    PRIORITY_REORDERING = "priority_reordering"    # Change task priorities
    RESOURCE_ALLOCATION = "resource_allocation"    # Adjust resource usage
    BEHAVIOR_MODIFICATION = "behavior_modification" # Modify behavioral patterns
    KNOWLEDGE_UPDATE = "knowledge_update"          # Update knowledge base


class LearningExperience(BaseModel):
    """Represents a single learning experience"""
    model_config = ConfigDict(use_enum_values=True)
    
    experience_id: str = Field(default_factory=lambda: str(uuid4()))
    experience_type: ExperienceType
    agent_id: str
    
    # Context information
    context: Dict[str, Any] = {}              # Situational context
    tension_id: Optional[str] = None          # Related tension
    task_id: Optional[str] = None            # Related task
    project_id: Optional[str] = None         # Related project
    
    # Experience details
    action_taken: Dict[str, Any] = {}        # What action was taken
    outcome: Dict[str, Any] = {}             # What was the result
    success: bool = True                     # Was it successful?
    
    # Learning metrics
    performance_before: Dict[str, float] = {} # Performance before action
    performance_after: Dict[str, float] = {}  # Performance after action
    improvement: Dict[str, float] = {}        # Calculated improvement
    
    # Temporal information
    timestamp: datetime = Field(default_factory=datetime.now)
    duration_seconds: float = 0.0
    
    # Meta information
    confidence_level: float = Field(default=0.5, ge=0.0, le=1.0)
    importance_weight: float = Field(default=1.0, ge=0.0, le=10.0)
    tags: List[str] = []                     # Categorization tags
    metadata: Dict[str, Any] = {}            # Additional metadata


class PerformanceMetric(BaseModel):
    """Represents a performance measurement"""
    model_config = ConfigDict(use_enum_values=True)
    
    metric_id: str = Field(default_factory=lambda: str(uuid4()))
    metric_type: MetricType
    agent_id: str
    
    # Metric details
    value: float                             # Current metric value
    baseline: float = 0.0                   # Baseline for comparison
    target: Optional[float] = None          # Target value
    
    # Context
    context: Dict[str, Any] = {}            # Measurement context
    measurement_period: Tuple[datetime, datetime] # Time period measured
    
    # Trend information
    trend_direction: str = "stable"         # "improving", "declining", "stable"
    change_rate: float = 0.0               # Rate of change
    
    # Quality indicators
    reliability: float = Field(default=0.8, ge=0.0, le=1.0)
    sample_size: int = 1                   # Number of samples
    
    timestamp: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = {}


class LearningPattern(BaseModel):
    """Represents an identified learning pattern"""
    model_config = ConfigDict(use_enum_values=True)
    
    pattern_id: str = Field(default_factory=lambda: str(uuid4()))
    pattern_type: str                       # Type of pattern identified
    agent_id: str
    
    # Pattern characteristics
    description: str                        # Human-readable description
    conditions: Dict[str, Any] = {}         # When this pattern applies
    outcomes: Dict[str, Any] = {}          # Expected outcomes
    
    # Statistical information
    frequency: int = 1                     # How often seen
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    strength: float = Field(default=0.5, ge=0.0, le=1.0)
    
    # Supporting evidence
    supporting_experiences: List[str] = []  # Experience IDs that support this pattern
    contradicting_experiences: List[str] = [] # Experience IDs that contradict
    
    # Temporal information
    first_observed: datetime = Field(default_factory=datetime.now)
    last_updated: datetime = Field(default_factory=datetime.now)
    
    # Applicability
    context_constraints: Dict[str, Any] = {} # When pattern is applicable
    success_rate: float = Field(default=0.5, ge=0.0, le=1.0)
    
    metadata: Dict[str, Any] = {}


class AdaptationRule(BaseModel):
    """Represents a rule for behavioral adaptation"""
    model_config = ConfigDict(use_enum_values=True)
    
    rule_id: str = Field(default_factory=lambda: str(uuid4()))
    adaptation_type: AdaptationType
    agent_id: str
    
    # Rule definition
    name: str                              # Rule name
    description: str                       # Rule description
    trigger_conditions: Dict[str, Any] = {} # When to apply this rule
    adaptation_actions: Dict[str, Any] = {} # What changes to make
    
    # Rule parameters
    priority: int = Field(default=5, ge=1, le=10)
    confidence_threshold: float = Field(default=0.7, ge=0.0, le=1.0)
    
    # Effectiveness tracking
    applications: int = 0                  # How many times applied
    successes: int = 0                    # How many times successful
    effectiveness: float = Field(default=0.0, ge=0.0, le=1.0)
    
    # Temporal information
    created_at: datetime = Field(default_factory=datetime.now)
    last_applied: Optional[datetime] = None
    
    # Constraints
    max_applications: Optional[int] = None  # Maximum times to apply
    expiry_date: Optional[datetime] = None  # When rule expires
    
    # Status
    active: bool = True
    metadata: Dict[str, Any] = {}


class LearningGoal(BaseModel):
    """Represents a learning objective"""
    model_config = ConfigDict(use_enum_values=True)
    
    goal_id: str = Field(default_factory=lambda: str(uuid4()))
    agent_id: str
    
    # Goal definition
    name: str                              # Goal name
    description: str                       # Goal description
    target_metrics: Dict[MetricType, float] = {} # Target metric values
    
    # Goal parameters
    priority: int = Field(default=5, ge=1, le=10)
    deadline: Optional[datetime] = None     # Target completion date
    
    # Progress tracking
    current_progress: Dict[MetricType, float] = {} # Current metric values
    completion_percentage: float = Field(default=0.0, ge=0.0, le=100.0)
    
    # Strategy
    learning_strategies: List[str] = []     # Preferred learning approaches
    adaptation_preferences: List[AdaptationType] = [] # Preferred adaptation types
    
    # Status
    status: str = "active"                 # "active", "completed", "paused", "cancelled"
    created_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    
    # Relationships
    parent_goal_id: Optional[str] = None   # Parent goal if this is a sub-goal
    sub_goal_ids: List[str] = []          # Sub-goals
    
    metadata: Dict[str, Any] = {}


class LearningSession(BaseModel):
    """Represents a learning session"""
    model_config = ConfigDict(use_enum_values=True)
    
    session_id: str = Field(default_factory=lambda: str(uuid4()))
    agent_id: str
    
    # Session details
    session_type: str                      # Type of learning session
    goals: List[str] = []                 # Goal IDs for this session
    experiences: List[str] = []           # Experience IDs collected
    patterns_discovered: List[str] = []   # Pattern IDs discovered
    adaptations_made: List[str] = []      # Adaptation rule IDs created/applied
    
    # Performance
    performance_before: Dict[MetricType, float] = {}
    performance_after: Dict[MetricType, float] = {}
    improvement_achieved: Dict[MetricType, float] = {}
    
    # Temporal information
    start_time: datetime = Field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    duration_seconds: float = 0.0
    
    # Quality metrics
    learning_effectiveness: float = Field(default=0.0, ge=0.0, le=1.0)
    knowledge_gain: float = Field(default=0.0, ge=0.0, le=1.0)
    
    # Status
    status: str = "active"                # "active", "completed", "failed"
    success: bool = True
    
    metadata: Dict[str, Any] = {}
    
    def finalize_session(self, success: bool = True) -> None:
        """Finalize the learning session"""
        self.end_time = datetime.now()
        self.success = success
        self.status = "completed" if success else "failed"
        
        if self.start_time and self.end_time:
            self.duration_seconds = (self.end_time - self.start_time).total_seconds()
        
        # Calculate learning effectiveness
        if self.performance_before and self.performance_after:
            improvements = []
            for metric_type in self.performance_before:
                if metric_type in self.performance_after:
                    before = self.performance_before[metric_type]
                    after = self.performance_after[metric_type]
                    if before > 0:
                        improvement = (after - before) / before
                        improvements.append(max(0.0, min(1.0, improvement)))
                        self.improvement_achieved[metric_type] = improvement
            
            if improvements:
                self.learning_effectiveness = sum(improvements) / len(improvements) 