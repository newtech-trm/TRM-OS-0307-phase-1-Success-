#!/usr/bin/env python3
"""
Strategic Project - AGE Enhanced Project Model
Theo AGE_COMPREHENSIVE_SYSTEM_DESIGN_V2.md

Transform basic Project CRUD thành Strategic Intelligence với:
- Temporal reasoning capabilities
- Commercial AI strategic planning
- Recognition → Event → WIN pattern tracking
- Strategic feedback loop automation
"""

from neomodel import (
    StructuredNode, StringProperty, DateTimeProperty, IntegerProperty,
    FloatProperty, JSONProperty, RelationshipTo, RelationshipFrom,
    ArrayProperty, BooleanProperty
)
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
from enum import Enum
import json

from trm_api.graph_models.base import BaseNode


class StrategicProjectStatus(str, Enum):
    """Strategic Project Status - không chỉ basic status"""
    STRATEGIC_PLANNING = "strategic_planning"      # AI-guided strategic planning phase
    ACTIVE_EXECUTION = "active_execution"          # Active với temporal reasoning
    STRATEGIC_OPTIMIZATION = "strategic_optimization"  # AI optimization in progress
    WIN_VALIDATION = "win_validation"              # Validating WIN achievements
    STRATEGIC_COMPLETE = "strategic_complete"      # Strategic objectives achieved
    LEARNING_EXTRACTION = "learning_extraction"   # Post-project learning capture
    STRATEGIC_ARCHIVED = "strategic_archived"     # Archived với strategic insights


class StrategicProjectType(str, Enum):
    """Strategic Project Types theo AGE philosophy"""
    PROBLEM_SOLVING_PROJECT = "problem_solving_project"
    OPPORTUNITY_PURSUIT = "opportunity_pursuit"
    KNOWLEDGE_CREATION = "knowledge_creation"
    SYSTEM_OPTIMIZATION = "system_optimization"
    INNOVATION_INITIATIVE = "innovation_initiative"
    STRATEGIC_TRANSFORMATION = "strategic_transformation"


class TemporalPhase(str, Enum):
    """Temporal phases cho strategic planning"""
    RECOGNITION_PHASE = "recognition"    # AI analysis & strategy formation
    EVENT_PHASE = "event"               # Active execution với monitoring
    WIN_PHASE = "win"                   # Outcome achievement & validation
    LEARNING_PHASE = "learning"         # Post-completion knowledge extraction


class GraphStrategicProject(BaseNode):
    """
    Strategic Project - AGE Enhanced Project với Strategic Intelligence
    
    Philosophy: Projects không chỉ là containers, mà là strategic entities
    với temporal reasoning, AI coordination, và automatic strategic feedback.
    """
    
    # === CORE STRATEGIC ATTRIBUTES ===
    title = StringProperty(required=True, index=True)
    strategic_description = StringProperty()
    
    # Strategic classification
    strategic_type = StringProperty(
        choices=[(status.value, status.value) for status in StrategicProjectType],
        default=StrategicProjectType.PROBLEM_SOLVING_PROJECT.value
    )
    
    status = StringProperty(
        choices=[(status.value, status.value) for status in StrategicProjectStatus],
        default=StrategicProjectStatus.STRATEGIC_PLANNING.value,
        index=True
    )
    
    # === TEMPORAL REASONING ATTRIBUTES ===
    current_temporal_phase = StringProperty(
        choices=[(phase.value, phase.value) for phase in TemporalPhase],
        default=TemporalPhase.RECOGNITION_PHASE.value
    )
    
    strategic_start_date = DateTimeProperty()
    strategic_target_date = DateTimeProperty()
    actual_completion_date = DateTimeProperty()
    
    # Temporal intelligence
    phase_transitions = JSONProperty(default=dict)  # Track phase transitions
    temporal_adjustments = JSONProperty(default=list)  # AI-recommended adjustments
    strategic_milestones = JSONProperty(default=list)  # Key strategic milestones
    
    # === STRATEGIC INTELLIGENCE ATTRIBUTES ===
    strategic_objectives = JSONProperty(default=list)  # High-level strategic goals
    success_criteria = JSONProperty(default=dict)      # Measurable success criteria
    strategic_context = JSONProperty(default=dict)     # Business context & rationale
    
    # AI Coordination tracking
    commercial_ai_insights = JSONProperty(default=dict)  # AI-generated strategic insights
    ai_recommendations = JSONProperty(default=list)      # Active AI recommendations
    ai_coordination_history = JSONProperty(default=list) # History of AI interactions
    
    # === WIN PATTERN TRACKING ===
    recognition_insights = JSONProperty(default=dict)   # Recognition phase insights
    event_executions = JSONProperty(default=list)       # Event phase actions
    win_achievements = JSONProperty(default=dict)       # WIN phase outcomes
    
    # WIN metrics
    strategic_win_score = FloatProperty(default=0.0)    # Overall strategic WIN score
    confidence_level = FloatProperty(default=0.5)       # AI confidence in success
    strategic_value_delivered = FloatProperty(default=0.0)  # Measured strategic value
    
    # === STRATEGIC FEEDBACK LOOP ===
    lessons_learned = JSONProperty(default=list)        # Captured learning points
    strategic_patterns = JSONProperty(default=dict)     # Identified strategic patterns
    improvement_recommendations = JSONProperty(default=list)  # For future projects
    
    # Feedback automation
    auto_feedback_enabled = BooleanProperty(default=True)
    last_feedback_analysis = DateTimeProperty()
    feedback_frequency_days = IntegerProperty(default=7)
    
    # === RESOURCE COORDINATION ===
    resource_utilization_efficiency = FloatProperty(default=0.0)
    mcp_resource_coordination = JSONProperty(default=dict)  # MCP-coordinated resources
    cross_platform_resources = JSONProperty(default=list)  # Multi-platform resources
    
    # === COLLABORATION & STAKEHOLDERS ===
    founder_involvement_level = StringProperty(default="high")  # Founder engagement level
    stakeholder_alignment_score = FloatProperty(default=0.5)    # Stakeholder alignment
    collaboration_patterns = JSONProperty(default=dict)        # Team collaboration insights
    
    # === RISK & ADAPTATION ===
    strategic_risks = JSONProperty(default=list)        # Identified strategic risks
    risk_mitigation_actions = JSONProperty(default=list) # Active risk mitigation
    adaptation_events = JSONProperty(default=list)      # Strategic adaptations made
    
    # === PERFORMANCE METRICS ===
    execution_velocity = FloatProperty(default=0.0)     # Speed of execution
    strategic_alignment_score = FloatProperty(default=0.5)  # Alignment to strategy
    innovation_index = FloatProperty(default=0.0)       # Innovation measurement
    learning_coefficient = FloatProperty(default=0.0)   # Learning rate từ project
    
    # === RELATIONSHIPS === 
    # Note: Relationship models will be implemented in future iterations
    # For now, keeping the model simple to avoid import errors
    
    # TODO: Implement these relationships when target models are available:
    # - assigned_resources -> CoordinatedResource
    # - managed_by_agents -> AGEActor  
    # - strategic_tasks -> StrategicTask
    
    # === STRATEGIC METHODS ===
    
    def initiate_strategic_planning(self, founder_intent: Dict[str, Any]) -> Dict[str, Any]:
        """
        Initiate strategic planning phase với Commercial AI guidance
        Recognition phase của Recognition → Event → WIN
        """
        self.current_temporal_phase = TemporalPhase.RECOGNITION_PHASE.value
        self.strategic_context = founder_intent
        self.strategic_start_date = datetime.now()
        
        # Initialize strategic objectives từ founder intent
        self.strategic_objectives = founder_intent.get("objectives", [])
        self.success_criteria = founder_intent.get("success_criteria", {})
        
        # Phase transition tracking
        self.phase_transitions[TemporalPhase.RECOGNITION_PHASE.value] = {
            "started_at": datetime.now().isoformat(),
            "trigger": "strategic_planning_initiated",
            "founder_intent": founder_intent
        }
        
        return {
            "phase": TemporalPhase.RECOGNITION_PHASE.value,
            "strategic_planning_initiated": True,
            "objectives_count": len(self.strategic_objectives),
            "success_criteria_defined": bool(self.success_criteria)
        }
    
    def transition_to_execution(self, execution_plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transition to active execution phase
        Event phase của Recognition → Event → WIN
        """
        self.current_temporal_phase = TemporalPhase.EVENT_PHASE.value
        self.status = StrategicProjectStatus.ACTIVE_EXECUTION.value
        
        # Record transition
        self.phase_transitions[TemporalPhase.EVENT_PHASE.value] = {
            "started_at": datetime.now().isoformat(),
            "trigger": "execution_phase_initiated",
            "execution_plan": execution_plan
        }
        
        # Initialize event executions tracking
        self.event_executions = [{
            "phase_start": datetime.now().isoformat(),
            "execution_plan": execution_plan,
            "expected_outcomes": execution_plan.get("expected_outcomes", [])
        }]
        
        return {
            "phase": TemporalPhase.EVENT_PHASE.value,
            "execution_initiated": True,
            "execution_plan_loaded": True
        }
    
    def validate_win_achievement(self, outcomes: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate WIN achievement và transition to WIN phase
        WIN phase của Recognition → Event → WIN
        """
        self.current_temporal_phase = TemporalPhase.WIN_PHASE.value
        self.status = StrategicProjectStatus.WIN_VALIDATION.value
        
        # Record WIN validation
        self.phase_transitions[TemporalPhase.WIN_PHASE.value] = {
            "started_at": datetime.now().isoformat(),
            "trigger": "win_validation_initiated",
            "outcomes": outcomes
        }
        
        # Calculate strategic WIN score
        self.win_achievements = outcomes
        self.strategic_win_score = self._calculate_strategic_win_score(outcomes)
        
        # Determine if WIN is achieved
        win_achieved = self.strategic_win_score >= 0.7
        if win_achieved:
            self.status = StrategicProjectStatus.STRATEGIC_COMPLETE.value
            self.actual_completion_date = datetime.now()
        
        return {
            "phase": TemporalPhase.WIN_PHASE.value,
            "win_achieved": win_achieved,
            "strategic_win_score": self.strategic_win_score,
            "completion_status": self.status
        }
    
    def capture_strategic_learning(self, learning_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Capture strategic learning for feedback loop
        Learning phase - post-completion knowledge extraction
        """
        self.current_temporal_phase = TemporalPhase.LEARNING_PHASE.value
        self.status = StrategicProjectStatus.LEARNING_EXTRACTION.value
        
        # Record learning phase
        self.phase_transitions[TemporalPhase.LEARNING_PHASE.value] = {
            "started_at": datetime.now().isoformat(),
            "trigger": "learning_extraction_initiated",
            "learning_scope": learning_data
        }
        
        # Extract lessons learned
        self.lessons_learned = learning_data.get("lessons", [])
        self.strategic_patterns = learning_data.get("patterns", {})
        self.improvement_recommendations = learning_data.get("improvements", [])
        
        # Calculate learning coefficient
        self.learning_coefficient = self._calculate_learning_coefficient(learning_data)
        
        # Archive project với strategic insights
        self.status = StrategicProjectStatus.STRATEGIC_ARCHIVED.value
        
        return {
            "phase": TemporalPhase.LEARNING_PHASE.value,
            "learning_captured": True,
            "lessons_count": len(self.lessons_learned),
            "learning_coefficient": self.learning_coefficient,
            "strategic_patterns_identified": len(self.strategic_patterns)
        }
    
    def add_ai_insight(self, ai_provider: str, insight_type: str, insight_data: Dict[str, Any]) -> None:
        """Add Commercial AI insight to project"""
        if not self.commercial_ai_insights:
            self.commercial_ai_insights = {}
        
        if ai_provider not in self.commercial_ai_insights:
            self.commercial_ai_insights[ai_provider] = []
        
        insight_entry = {
            "timestamp": datetime.now().isoformat(),
            "type": insight_type,
            "data": insight_data,
            "phase": self.current_temporal_phase
        }
        
        self.commercial_ai_insights[ai_provider].append(insight_entry)
    
    def add_ai_recommendation(self, recommendation: Dict[str, Any]) -> None:
        """Add AI recommendation to project"""
        if not self.ai_recommendations:
            self.ai_recommendations = []
        
        recommendation_entry = {
            "timestamp": datetime.now().isoformat(),
            "recommendation": recommendation,
            "phase": self.current_temporal_phase,
            "status": "active"
        }
        
        self.ai_recommendations.append(recommendation_entry)
    
    def update_strategic_metrics(self, metrics: Dict[str, float]) -> None:
        """Update strategic performance metrics"""
        self.execution_velocity = metrics.get("execution_velocity", self.execution_velocity)
        self.strategic_alignment_score = metrics.get("alignment_score", self.strategic_alignment_score)
        self.innovation_index = metrics.get("innovation_index", self.innovation_index)
        self.confidence_level = metrics.get("confidence_level", self.confidence_level)
        self.stakeholder_alignment_score = metrics.get("stakeholder_alignment", self.stakeholder_alignment_score)
    
    def trigger_strategic_feedback_analysis(self) -> Dict[str, Any]:
        """Trigger automated strategic feedback analysis"""
        if not self.auto_feedback_enabled:
            return {"feedback_analysis": False, "reason": "auto_feedback_disabled"}
        
        # Check if feedback analysis is due
        if self.last_feedback_analysis:
            days_since_last = (datetime.now() - self.last_feedback_analysis).days
            if days_since_last < self.feedback_frequency_days:
                return {
                    "feedback_analysis": False, 
                    "reason": f"feedback_not_due_for_{self.feedback_frequency_days - days_since_last}_days"
                }
        
        # Update last feedback timestamp
        self.last_feedback_analysis = datetime.now()
        
        # Generate feedback analysis request
        return {
            "feedback_analysis": True,
            "analysis_timestamp": datetime.now().isoformat(),
            "project_phase": self.current_temporal_phase,
            "strategic_context": self.strategic_context,
            "current_metrics": {
                "win_score": self.strategic_win_score,
                "confidence": self.confidence_level,
                "alignment": self.strategic_alignment_score,
                "execution_velocity": self.execution_velocity
            }
        }
    
    def _calculate_strategic_win_score(self, outcomes: Dict[str, Any]) -> float:
        """Calculate strategic WIN score based on outcomes"""
        if not self.success_criteria or not outcomes:
            return 0.0
        
        total_criteria = len(self.success_criteria)
        met_criteria = 0
        
        for criterion, expected in self.success_criteria.items():
            if criterion in outcomes:
                actual = outcomes[criterion]
                # Simple comparison - can be enhanced với sophisticated scoring
                if isinstance(expected, (int, float)) and isinstance(actual, (int, float)):
                    if actual >= expected:
                        met_criteria += 1
                elif str(actual).lower() == str(expected).lower():
                    met_criteria += 1
        
        return met_criteria / total_criteria if total_criteria > 0 else 0.0
    
    def _calculate_learning_coefficient(self, learning_data: Dict[str, Any]) -> float:
        """Calculate learning coefficient from project experience"""
        lessons_count = len(learning_data.get("lessons", []))
        patterns_count = len(learning_data.get("patterns", {}))
        improvements_count = len(learning_data.get("improvements", []))
        
        # Learning coefficient formula
        coefficient = (lessons_count * 0.4 + patterns_count * 0.3 + improvements_count * 0.3) / 10
        return min(coefficient, 1.0)  # Cap at 1.0
    
    def get_strategic_summary(self) -> Dict[str, Any]:
        """Get comprehensive strategic summary"""
        return {
            "project_id": self.uid,
            "title": self.title,
            "strategic_type": self.strategic_type,
            "current_status": self.status,
            "temporal_phase": self.current_temporal_phase,
            "strategic_metrics": {
                "win_score": self.strategic_win_score,
                "confidence_level": self.confidence_level,
                "strategic_alignment": self.strategic_alignment_score,
                "execution_velocity": self.execution_velocity,
                "innovation_index": self.innovation_index,
                "learning_coefficient": self.learning_coefficient
            },
            "phase_history": self.phase_transitions,
            "objectives_count": len(self.strategic_objectives or []),
            "ai_insights_count": sum(len(insights) for insights in (self.commercial_ai_insights or {}).values()),
            "active_recommendations": len([r for r in (self.ai_recommendations or []) if r.get("status") == "active"]),
            "lessons_learned_count": len(self.lessons_learned or []),
            "strategic_patterns_count": len(self.strategic_patterns or {}),
            "philosophy": "Recognition → Event → WIN through Strategic Intelligence"
        }
    
    @property
    def is_strategic_success(self) -> bool:
        """Check if project achieved strategic success"""
        return (self.strategic_win_score >= 0.7 and 
                self.status == StrategicProjectStatus.STRATEGIC_COMPLETE.value)
    
    @property
    def strategic_health_score(self) -> float:
        """Calculate overall strategic health score"""
        metrics = [
            self.strategic_win_score,
            self.confidence_level,
            self.strategic_alignment_score,
            self.execution_velocity,
            self.stakeholder_alignment_score
        ]
        return sum(metrics) / len(metrics)
    
    class Meta:
        app_label = 'trm_api'


# Alias for backward compatibility
GraphProject = GraphStrategicProject 