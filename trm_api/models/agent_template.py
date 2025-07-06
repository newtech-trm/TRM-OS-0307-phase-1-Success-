"""
Agent Template Models for TRM-OS

Định nghĩa các models cho Agent Templates system tuân thủ triết lý TRM-OS.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field

from .enums import TensionType


class AgentCapability(BaseModel):
    """
    Represents a specific capability of an agent template.
    
    Tuân thủ nguyên tắc TRM-OS về capability-based agent design.
    """
    name: str = Field(..., description="Unique name of the capability")
    description: str = Field(..., description="Detailed description of what this capability does")
    proficiency_level: float = Field(
        default=0.7, 
        ge=0.0, 
        le=1.0, 
        description="Proficiency level from 0.0 to 1.0"
    )
    estimated_time_per_task: float = Field(
        default=60.0,
        gt=0.0,
        description="Estimated time in minutes to complete a typical task using this capability"
    )
    prerequisites: List[str] = Field(
        default_factory=list,
        description="List of prerequisite capabilities or knowledge"
    )
    related_tension_types: List[TensionType] = Field(
        default_factory=list,
        description="Tension types this capability can help resolve"
    )
    win_contribution: Dict[str, float] = Field(
        default_factory=lambda: {"wisdom": 0.3, "intelligence": 0.4, "networking": 0.3},
        description="How this capability contributes to WIN scores"
    )
    
    class Config:
        use_enum_values = True


class AgentTemplateMetadata(BaseModel):
    """
    Metadata for agent templates in TRM-OS.
    
    Defines the core characteristics and capabilities of an agent template
    following TRM-OS ontology-first design principles.
    """
    template_name: str = Field(..., description="Unique name of the template")
    primary_domain: str = Field(..., description="Primary domain of expertise")
    capabilities: List[AgentCapability] = Field(
        default_factory=list,
        description="List of capabilities this template provides"
    )
    domain_expertise: List[str] = Field(
        default_factory=list,
        description="Areas of domain expertise"
    )
    supported_tension_types: List[TensionType] = Field(
        default_factory=list,
        description="Types of tensions this template can handle"
    )
    performance_metrics: Dict[str, float] = Field(
        default_factory=dict,
        description="Historical performance metrics"
    )
    version: str = Field(default="1.0.0", description="Template version")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    # WIN optimization parameters
    win_optimization_weights: Dict[str, float] = Field(
        default_factory=lambda: {"wisdom": 0.4, "intelligence": 0.4, "networking": 0.2},
        description="Weights for WIN score optimization"
    )
    
    # Quantum operating model configuration
    quantum_model_config: Dict[str, Any] = Field(
        default_factory=dict,
        description="Configuration for quantum operating model"
    )
    
    # Strategic alignment
    strategic_alignment: Dict[str, Any] = Field(
        default_factory=dict,
        description="Alignment with TRM-OS strategic objectives"
    )
    
    @property
    def name(self) -> str:
        """Alias for template_name for backward compatibility"""
        return self.template_name
    
    def get_capability_by_name(self, capability_name: str) -> Optional[AgentCapability]:
        """Get a specific capability by name"""
        for capability in self.capabilities:
            if capability.name == capability_name:
                return capability
        return None
    
    def get_capabilities_for_tension_type(self, tension_type: TensionType) -> List[AgentCapability]:
        """Get capabilities that can handle a specific tension type"""
        relevant_capabilities = []
        for capability in self.capabilities:
            if tension_type in capability.related_tension_types:
                relevant_capabilities.append(capability)
        return relevant_capabilities
    
    def calculate_domain_relevance(self, domain: str) -> float:
        """Calculate relevance score for a specific domain"""
        if domain.lower() == self.primary_domain.lower():
            return 1.0
        
        domain_matches = sum(1 for expertise in self.domain_expertise 
                           if domain.lower() in expertise.lower())
        
        return min(1.0, domain_matches / len(self.domain_expertise) if self.domain_expertise else 0.0)
    
    def get_average_proficiency(self) -> float:
        """Get average proficiency across all capabilities"""
        if not self.capabilities:
            return 0.0
        
        total_proficiency = sum(cap.proficiency_level for cap in self.capabilities)
        return total_proficiency / len(self.capabilities)
    
    def estimate_total_task_time(self, task_complexity: str = "medium") -> float:
        """Estimate total time for a task using all capabilities"""
        if not self.capabilities:
            return 60.0  # Default 1 hour
        
        complexity_multipliers = {
            "low": 0.7,
            "medium": 1.0,
            "high": 1.5
        }
        
        multiplier = complexity_multipliers.get(task_complexity, 1.0)
        base_time = sum(cap.estimated_time_per_task for cap in self.capabilities) / len(self.capabilities)
        
        return base_time * multiplier
    
    def get_win_potential(self) -> Dict[str, float]:
        """Calculate WIN potential based on capabilities"""
        if not self.capabilities:
            return {"wisdom": 50.0, "intelligence": 50.0, "networking": 50.0, "total": 50.0}
        
        # Aggregate WIN contributions from all capabilities
        total_wisdom = sum(cap.win_contribution.get("wisdom", 0.3) * cap.proficiency_level 
                          for cap in self.capabilities)
        total_intelligence = sum(cap.win_contribution.get("intelligence", 0.4) * cap.proficiency_level 
                               for cap in self.capabilities)
        total_networking = sum(cap.win_contribution.get("networking", 0.3) * cap.proficiency_level 
                             for cap in self.capabilities)
        
        # Normalize by number of capabilities and scale to 0-100
        num_caps = len(self.capabilities)
        wisdom_score = (total_wisdom / num_caps) * 100
        intelligence_score = (total_intelligence / num_caps) * 100
        networking_score = (total_networking / num_caps) * 100
        
        # Calculate total WIN using TRM-OS weights
        weights = self.win_optimization_weights
        total_win = (wisdom_score * weights["wisdom"] + 
                    intelligence_score * weights["intelligence"] + 
                    networking_score * weights["networking"])
        
        return {
            "wisdom": wisdom_score,
            "intelligence": intelligence_score,
            "networking": networking_score,
            "total": total_win
        }
    
    class Config:
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class TemplatePerformanceMetrics(BaseModel):
    """
    Performance metrics for agent templates.
    
    Tracks WIN-optimized performance over time.
    """
    template_name: str = Field(..., description="Name of the template")
    
    # Core performance metrics
    success_rate: float = Field(default=0.0, ge=0.0, le=1.0)
    average_resolution_time: float = Field(default=0.0, ge=0.0)
    user_satisfaction_score: float = Field(default=0.0, ge=0.0, le=10.0)
    
    # WIN-specific metrics
    average_win_score: float = Field(default=0.0, ge=0.0, le=100.0)
    win_score_trend: List[float] = Field(default_factory=list)
    wisdom_score: float = Field(default=0.0, ge=0.0, le=100.0)
    intelligence_score: float = Field(default=0.0, ge=0.0, le=100.0)
    networking_score: float = Field(default=0.0, ge=0.0, le=100.0)
    
    # Usage statistics
    total_tensions_handled: int = Field(default=0, ge=0)
    total_solutions_generated: int = Field(default=0, ge=0)
    active_deployments: int = Field(default=0, ge=0)
    
    # Quality metrics
    code_quality_score: Optional[float] = Field(default=None, ge=0.0, le=100.0)
    documentation_completeness: Optional[float] = Field(default=None, ge=0.0, le=100.0)
    maintainability_index: Optional[float] = Field(default=None, ge=0.0, le=100.0)
    
    # Time tracking
    last_updated: datetime = Field(default_factory=datetime.now)
    measurement_period_start: datetime = Field(default_factory=datetime.now)
    measurement_period_end: Optional[datetime] = None
    
    def update_win_score(self, new_score: float) -> None:
        """Update WIN score and trend"""
        self.win_score_trend.append(new_score)
        
        # Keep only last 50 scores for trend analysis
        if len(self.win_score_trend) > 50:
            self.win_score_trend = self.win_score_trend[-50:]
        
        # Update average
        self.average_win_score = sum(self.win_score_trend) / len(self.win_score_trend)
        self.last_updated = datetime.now()
    
    def get_performance_grade(self) -> str:
        """Get performance grade based on WIN score"""
        if self.average_win_score >= 90:
            return "A+"
        elif self.average_win_score >= 80:
            return "A"
        elif self.average_win_score >= 70:
            return "B"
        elif self.average_win_score >= 60:
            return "C"
        else:
            return "D"
    
    def is_improving(self) -> bool:
        """Check if performance is improving based on recent trend"""
        if len(self.win_score_trend) < 5:
            return True  # Not enough data, assume improving
        
        recent_scores = self.win_score_trend[-5:]
        early_avg = sum(recent_scores[:2]) / 2
        late_avg = sum(recent_scores[-2:]) / 2
        
        return late_avg > early_avg
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        } 