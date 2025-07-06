"""
Core types and data structures for Advanced Reasoning Engine

Follows TRM-OS philosophy: Recognition → Event → WIN
"""

from datetime import datetime
from typing import Dict, List, Any, Optional, Union, Tuple
from enum import Enum
from pydantic import BaseModel, Field, ConfigDict
from uuid import uuid4


class UncertaintyLevel(Enum):
    """Levels of uncertainty in reasoning"""
    CERTAIN = "certain"           # 0.9-1.0 confidence
    HIGH_CONFIDENCE = "high"      # 0.7-0.9 confidence  
    MODERATE = "moderate"         # 0.5-0.7 confidence
    LOW_CONFIDENCE = "low"        # 0.3-0.5 confidence
    UNCERTAIN = "uncertain"       # 0.0-0.3 confidence


class ReasoningType(Enum):
    """Types of reasoning processes"""
    DEDUCTIVE = "deductive"       # Logic-based reasoning
    INDUCTIVE = "inductive"       # Pattern-based reasoning
    CAUSAL = "causal"            # Cause-effect reasoning
    TEMPORAL = "temporal"        # Time-based reasoning
    CONTEXTUAL = "contextual"    # Context-aware reasoning
    PROBABILISTIC = "probabilistic"  # Uncertainty-based reasoning


class ReasoningStep(BaseModel):
    """Single step in multi-step reasoning process"""
    model_config = ConfigDict(use_enum_values=True)
    
    step_id: str = Field(default_factory=lambda: str(uuid4()))
    step_type: ReasoningType
    description: str
    input_data: Dict[str, Any]
    reasoning_logic: str
    output_data: Dict[str, Any] 
    confidence: float = Field(ge=0.0, le=1.0)
    uncertainty_level: UncertaintyLevel
    execution_time: datetime
    dependencies: List[str] = []  # IDs of dependent steps
    evidence: List[Dict[str, Any]] = []  # Supporting evidence
    assumptions: List[str] = []   # Made assumptions


class CausalChain(BaseModel):
    """Represents a causal relationship chain"""
    chain_id: str = Field(default_factory=lambda: str(uuid4()))
    root_cause: str
    intermediate_causes: List[str] = []
    final_effect: str
    confidence: float = Field(ge=0.0, le=1.0)
    strength: float = Field(ge=0.0, le=1.0)  # Causal strength
    evidence: List[Dict[str, Any]] = []
    relationships: List[Tuple[str, str, float]] = []  # (cause, effect, strength)
    
    
class ReasoningContext(BaseModel):
    """Context for reasoning process following TRM-OS ontology"""
    context_id: str = Field(default_factory=lambda: str(uuid4()))
    
    # Core ontology entities
    tension_id: Optional[str] = None
    task_ids: List[str] = []
    agent_id: Optional[str] = None
    project_id: Optional[str] = None
    
    # Context data
    current_state: Dict[str, Any] = {}
    historical_events: List[Dict[str, Any]] = []
    related_entities: Dict[str, List[str]] = {}  # entity_type -> [entity_ids]
    
    # Temporal context
    timestamp: datetime = Field(default_factory=datetime.now)
    time_window: Optional[Tuple[datetime, datetime]] = None
    
    # Meta context
    domain: Optional[str] = None
    priority_level: int = Field(default=5, ge=1, le=10)
    complexity_score: float = Field(default=0.5, ge=0.0, le=1.0)


class ReasoningResult(BaseModel):
    """Result of reasoning process"""
    model_config = ConfigDict(use_enum_values=True)
    
    result_id: str = Field(default_factory=lambda: str(uuid4()))
    reasoning_type: ReasoningType
    context: ReasoningContext
    
    # Reasoning process
    steps: List[ReasoningStep] = []
    causal_chains: List[CausalChain] = []
    
    # Results
    conclusions: List[str] = []
    recommendations: List[Dict[str, Any]] = []
    predictions: List[Dict[str, Any]] = []
    
    # Quality metrics
    overall_confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    uncertainty_level: UncertaintyLevel = Field(default=UncertaintyLevel.MODERATE)
    reasoning_quality: float = Field(default=0.5, ge=0.0, le=1.0)
    
    # Audit trail
    start_time: datetime = Field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    total_steps: int = 0
    success: bool = True
    error_message: Optional[str] = None
    
    # TRM-OS integration
    generated_events: List[Dict[str, Any]] = []  # Events to be created
    suggested_actions: List[Dict[str, Any]] = []  # Suggested agent actions
        
    def duration_seconds(self) -> float:
        """Calculate reasoning duration in seconds"""
        if self.end_time and self.start_time:
            duration = (self.end_time - self.start_time).total_seconds()
            # Ensure minimum duration for audit trail purposes
            return max(0.001, duration)
        return 0.001  # Minimum duration if times not set
    
    def add_step(self, step: ReasoningStep) -> None:
        """Add a reasoning step"""
        self.steps.append(step)
        self.total_steps = len(self.steps)
        
    def finalize(self, success: bool = True, error: Optional[str] = None) -> None:
        """Finalize reasoning result"""
        self.end_time = datetime.now()
        self.success = success
        self.error_message = error
        
        # Calculate overall confidence from steps and context quality
        if self.steps:
            step_confidence = sum(step.confidence for step in self.steps) / len(self.steps)
            
            # Adjust confidence based on context quality
            context_quality_factor = self._calculate_context_quality_factor()
            self.overall_confidence = min(1.0, step_confidence * context_quality_factor)
            
            # Determine uncertainty level
            if self.overall_confidence >= 0.9:
                self.uncertainty_level = UncertaintyLevel.CERTAIN
            elif self.overall_confidence >= 0.7:
                self.uncertainty_level = UncertaintyLevel.HIGH_CONFIDENCE
            elif self.overall_confidence >= 0.5:
                self.uncertainty_level = UncertaintyLevel.MODERATE
            elif self.overall_confidence >= 0.3:
                self.uncertainty_level = UncertaintyLevel.LOW_CONFIDENCE
            else:
                self.uncertainty_level = UncertaintyLevel.UNCERTAIN
                
            # Calculate quality based on confidence and step consistency
            step_variance = sum((step.confidence - step_confidence) ** 2 for step in self.steps) / len(self.steps)
            self.reasoning_quality = max(0.0, self.overall_confidence - step_variance)
    
    def _calculate_context_quality_factor(self) -> float:
        """Calculate context quality factor to adjust confidence"""
        quality_factors = []
        
        # Historical data richness
        if self.context.historical_events:
            event_richness = min(1.0, len(self.context.historical_events) / 10)  # Normalize to 10 events
            quality_factors.append(event_richness)
        else:
            quality_factors.append(0.3)  # Low quality for no historical data
            
        # Entity relationship richness
        if self.context.related_entities:
            entity_richness = min(1.0, len(self.context.related_entities) / 5)  # Normalize to 5 entity types
            quality_factors.append(entity_richness)
        else:
            quality_factors.append(0.4)  # Low quality for no entity relationships
            
        # Current state completeness
        if self.context.current_state:
            state_completeness = min(1.0, len(self.context.current_state) / 5)  # Normalize to 5 state items
            quality_factors.append(state_completeness)
        else:
            quality_factors.append(0.5)  # Medium quality for no current state
            
        # Causal chain richness
        if self.causal_chains:
            causal_richness = min(1.0, len(self.causal_chains) / 3)  # Normalize to 3 causal chains
            quality_factors.append(causal_richness)
        else:
            quality_factors.append(0.6)  # Medium quality for no causal chains
        
        # Return weighted average with emphasis on data richness
        if quality_factors:
            return sum(quality_factors) / len(quality_factors)
        return 0.5  # Default medium quality


class KnowledgeNode(BaseModel):
    """Knowledge representation for reasoning"""
    node_id: str = Field(default_factory=lambda: str(uuid4()))
    node_type: str  # "fact", "rule", "pattern", "hypothesis"
    content: str
    confidence: float = Field(ge=0.0, le=1.0)
    source: str  # Source of knowledge
    related_entities: List[str] = []  # Related ontology entity IDs
    metadata: Dict[str, Any] = {}
    created_at: datetime = Field(default_factory=datetime.now)


class ReasoningConstraint(BaseModel):
    """Constraints for reasoning process"""
    constraint_id: str = Field(default_factory=lambda: str(uuid4()))
    constraint_type: str  # "time", "resource", "logical", "domain"
    description: str
    parameters: Dict[str, Any] = {}
    strict: bool = True  # Whether constraint is hard or soft
    
    
class ReasoningGoal(BaseModel):
    """Goal for reasoning process"""
    goal_id: str = Field(default_factory=lambda: str(uuid4()))
    goal_type: str  # "explanation", "prediction", "recommendation", "analysis"
    description: str
    success_criteria: List[str] = []
    constraints: List[ReasoningConstraint] = []
    priority: int = Field(default=5, ge=1, le=10) 