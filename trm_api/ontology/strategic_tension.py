#!/usr/bin/env python3
"""
Strategic Tension - Core Ontological Foundation
The fundamental semantic entity that drives all action in TRM-OS AGE system

Philosophy: Every action, every agent, every strategic unit exists to resolve 
existential tensions. No CRUD operations - only tension-driven responses.

Semantic Principle: Recognition → Event → WIN begins with tension recognition.
"""

from neomodel import (
    StructuredNode, StringProperty, DateTimeProperty, IntegerProperty,
    FloatProperty, JSONProperty, RelationshipTo, RelationshipFrom,
    ArrayProperty, BooleanProperty, UniqueIdProperty
)
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union, Tuple
from enum import Enum
import json
import uuid

from trm_api.graph_models.base import BaseNode


class TensionType(str, Enum):
    """Types of strategic tensions in TRM ontology"""
    EXISTENTIAL_CRISIS = "existential_crisis"        # Threats to organizational existence
    OPPORTUNITY_GAP = "opportunity_gap"              # Missed strategic opportunities  
    KNOWLEDGE_DEFICIT = "knowledge_deficit"          # Critical knowledge gaps
    RESOURCE_MISALIGNMENT = "resource_misalignment"  # Resources not optimally deployed
    STAKEHOLDER_DISCORD = "stakeholder_discord"     # Conflicting stakeholder interests
    EXECUTION_PARALYSIS = "execution_paralysis"     # Inability to execute strategic vision
    MARKET_DISRUPTION = "market_disruption"         # External market forces
    INNOVATION_STAGNATION = "innovation_stagnation" # Lack of strategic innovation
    CULTURAL_MISALIGNMENT = "cultural_misalignment" # Culture vs strategy conflicts
    SYSTEMIC_INEFFICIENCY = "systemic_inefficiency" # System-wide performance issues


class TensionUrgency(str, Enum):
    """Urgency levels for strategic tension resolution"""
    CRITICAL = "critical"      # Immediate AGE response required
    HIGH = "high"             # AGE response within 24 hours
    MEDIUM = "medium"         # AGE response within week
    LOW = "low"              # AGE response when capacity available
    MONITORING = "monitoring" # AGE continuous monitoring


class TensionResolutionPhase(str, Enum):
    """Phases of tension resolution following Recognition → Event → WIN"""
    RECOGNITION = "recognition"  # Tension identified and analyzed
    ORCHESTRATION = "orchestration"  # AGE actors coordinated for response
    EVENT_EXECUTION = "event_execution"  # Strategic actions being executed
    WIN_VALIDATION = "win_validation"  # Measuring resolution success
    LEARNING_INTEGRATION = "learning_integration"  # Integrating lessons learned
    RESOLVED = "resolved"  # Tension successfully resolved


class StrategicTension(BaseNode):
    """
    Strategic Tension - The fundamental driver of all AGE system activity
    
    Semantic Foundation: Everything in TRM-OS exists to identify, analyze, and resolve
    strategic tensions. No entity exists without tension-driven purpose.
    
    Ontological Role: Core semantic entity that triggers Recognition → Event → WIN
    """
    
    # === CORE TENSION IDENTITY ===
    tension_identity = StringProperty(required=True, unique_index=True)
    semantic_description = StringProperty(required=True)
    
    # Tension Classification
    tension_type = StringProperty(
        choices=[(t.value, t.value) for t in TensionType],
        required=True,
        index=True
    )
    
    urgency_level = StringProperty(
        choices=[(u.value, u.value) for u in TensionUrgency],
        default=TensionUrgency.MEDIUM.value,
        index=True
    )
    
    # === SEMANTIC CONTEXT ===
    originating_context = JSONProperty(required=True)    # Context where tension emerged
    stakeholder_impact = JSONProperty(default=dict)      # Who/what is affected
    strategic_significance = FloatProperty(default=0.5)  # 0-1 significance score
    existential_threat_level = FloatProperty(default=0.0) # 0-1 threat to existence
    
    # === TENSION DYNAMICS ===
    current_resolution_phase = StringProperty(
        choices=[(p.value, p.value) for p in TensionResolutionPhase],
        default=TensionResolutionPhase.RECOGNITION.value,
        index=True
    )
    
    tension_evolution = JSONProperty(default=list)       # How tension has evolved
    resolution_attempts = JSONProperty(default=list)     # Previous resolution attempts
    learned_patterns = JSONProperty(default=dict)        # Patterns discovered about this tension
    
    # === AGE ORCHESTRATION STATE ===
    age_analysis_complete = BooleanProperty(default=False)
    optimal_response_strategy = JSONProperty(default=dict)
    required_age_actors = ArrayProperty(StringProperty(), default=list)
    resource_coordination_needs = JSONProperty(default=dict)
    
    # === TEMPORAL DYNAMICS ===
    tension_emergence_date = DateTimeProperty(default_now=True)
    tension_escalation_threshold = DateTimeProperty()
    target_resolution_date = DateTimeProperty()
    actual_resolution_date = DateTimeProperty()
    
    # Resolution timing intelligence
    optimal_resolution_window = JSONProperty(default=dict)
    escalation_triggers = JSONProperty(default=list)
    resolution_velocity_required = FloatProperty(default=1.0)
    
    # === MEASUREMENT & VALIDATION ===
    pre_resolution_metrics = JSONProperty(default=dict)   # State before resolution
    resolution_success_criteria = JSONProperty(default=dict) # What defines success
    post_resolution_metrics = JSONProperty(default=dict)  # State after resolution
    win_validation_status = StringProperty(default="pending")
    
    # === STRATEGIC RELATIONSHIPS ===
    
    # Triggers Strategic Units (Response to tension)
    triggered_strategic_units = RelationshipTo(
        'trm_api.ontology.strategic_unit.StrategicUnit',
        'TRIGGERS_STRATEGIC_RESPONSE'
    )
    
    # Analyzed by AGE Actors
    analyzed_by_age_actors = RelationshipFrom(
        'trm_api.ontology.age_actor.AGEActor',
        'ANALYZES_TENSION'
    )
    
    # Orchestrated by AGE Orchestrator
    orchestrated_by = RelationshipFrom(
        'trm_api.ontology.age_orchestrator.AGEOrchestrator',
        'ORCHESTRATES_TENSION_RESOLUTION'
    )
    
    # Related Tensions (Compound/cascading tensions)
    related_tensions = RelationshipTo('StrategicTension', 'CASCADES_TO')
    cascaded_from = RelationshipFrom('StrategicTension', 'CASCADES_TO')
    
    # Generated Events (Actions taken in response)
    resolution_events = RelationshipTo(
        'trm_api.ontology.strategic_event.StrategicEvent',
        'GENERATES_RESOLUTION_EVENT'
    )
    
    # Stakeholder Impact
    impacts_stakeholders = RelationshipTo(
        'trm_api.ontology.stakeholder.Stakeholder',
        'IMPACTS_STAKEHOLDER'
    )
    
    # === CORE METHODS ===
    
    def initiate_age_recognition_phase(self) -> Dict[str, Any]:
        """
        Initiate Recognition phase of Recognition → Event → WIN
        Core method that triggers AGE system response to tension
        """
        self.current_resolution_phase = TensionResolutionPhase.RECOGNITION.value
        
        recognition_context = {
            "tension_identity": self.tension_identity,
            "tension_type": self.tension_type,
            "urgency_level": self.urgency_level,
            "strategic_significance": self.strategic_significance,
            "originating_context": self.originating_context,
            "stakeholder_impact": self.stakeholder_impact,
            "recognition_initiated_at": datetime.now().isoformat()
        }
        
        # Add to tension evolution log
        if not self.tension_evolution:
            self.tension_evolution = []
        
        self.tension_evolution.append({
            "phase": "recognition_initiated",
            "timestamp": datetime.now().isoformat(),
            "context": recognition_context
        })
        
        return {
            "recognition_phase": "initiated",
            "tension_identity": self.tension_identity,
            "age_analysis_required": True,
            "recognition_context": recognition_context
        }
    
    def record_age_analysis(self, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """Record AGE actor analysis of this tension"""
        self.age_analysis_complete = True
        self.optimal_response_strategy = analysis_result.get("response_strategy", {})
        self.required_age_actors = analysis_result.get("required_actors", [])
        self.resource_coordination_needs = analysis_result.get("resource_needs", {})
        
        # Add to evolution log
        self.tension_evolution.append({
            "phase": "age_analysis_complete",
            "timestamp": datetime.now().isoformat(),
            "analysis_result": analysis_result
        })
        
        return {
            "analysis_recorded": True,
            "response_strategy": self.optimal_response_strategy,
            "required_actors": self.required_age_actors
        }
    
    def transition_to_orchestration_phase(self) -> Dict[str, Any]:
        """Transition to orchestration phase - coordinating AGE response"""
        if not self.age_analysis_complete:
            return {
                "error": "Cannot transition to orchestration without completed AGE analysis",
                "required_action": "complete_age_analysis_first"
            }
        
        self.current_resolution_phase = TensionResolutionPhase.ORCHESTRATION.value
        
        orchestration_context = {
            "optimal_strategy": self.optimal_response_strategy,
            "required_actors": self.required_age_actors,
            "resource_needs": self.resource_coordination_needs,
            "orchestration_initiated_at": datetime.now().isoformat()
        }
        
        self.tension_evolution.append({
            "phase": "orchestration_initiated",
            "timestamp": datetime.now().isoformat(),
            "context": orchestration_context
        })
        
        return {
            "orchestration_phase": "initiated",
            "tension_identity": self.tension_identity,
            "orchestration_context": orchestration_context
        }
    
    def initiate_event_execution_phase(self, execution_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Initiate Event phase - actual strategic actions execution"""
        self.current_resolution_phase = TensionResolutionPhase.EVENT_EXECUTION.value
        
        execution_context = {
            "execution_plan": execution_plan,
            "expected_outcomes": execution_plan.get("expected_outcomes", []),
            "success_criteria": self.resolution_success_criteria,
            "execution_initiated_at": datetime.now().isoformat()
        }
        
        self.tension_evolution.append({
            "phase": "event_execution_initiated",
            "timestamp": datetime.now().isoformat(),
            "context": execution_context
        })
        
        return {
            "event_execution_phase": "initiated",
            "tension_identity": self.tension_identity,
            "execution_context": execution_context
        }
    
    def validate_resolution_win(self, resolution_evidence: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate WIN achievement - tension successfully resolved
        WIN phase of Recognition → Event → WIN
        """
        self.current_resolution_phase = TensionResolutionPhase.WIN_VALIDATION.value
        
        # Record post-resolution metrics
        self.post_resolution_metrics = resolution_evidence.get("metrics", {})
        
        # Evaluate WIN criteria
        win_achieved = self._evaluate_win_criteria(resolution_evidence)
        
        if win_achieved:
            self.win_validation_status = "win_achieved"
            self.actual_resolution_date = datetime.now()
            self.current_resolution_phase = TensionResolutionPhase.LEARNING_INTEGRATION.value
        else:
            self.win_validation_status = "win_not_achieved"
            # Tension remains in validation phase for further action
        
        validation_result = {
            "win_achieved": win_achieved,
            "tension_identity": self.tension_identity,
            "resolution_evidence": resolution_evidence,
            "validation_timestamp": datetime.now().isoformat()
        }
        
        self.tension_evolution.append({
            "phase": "win_validation",
            "timestamp": datetime.now().isoformat(),
            "result": validation_result
        })
        
        return validation_result
    
    def integrate_resolution_learning(self, learning_data: Dict[str, Any]) -> Dict[str, Any]:
        """Integrate learning from tension resolution for future improvements"""
        self.learned_patterns.update(learning_data.get("patterns", {}))
        
        learning_integration = {
            "patterns_learned": learning_data.get("patterns", {}),
            "improvements_identified": learning_data.get("improvements", []),
            "strategic_insights": learning_data.get("insights", []),
            "integration_timestamp": datetime.now().isoformat()
        }
        
        self.tension_evolution.append({
            "phase": "learning_integration",
            "timestamp": datetime.now().isoformat(),
            "learning": learning_integration
        })
        
        if self.win_validation_status == "win_achieved":
            self.current_resolution_phase = TensionResolutionPhase.RESOLVED.value
        
        return {
            "learning_integrated": True,
            "tension_status": self.current_resolution_phase,
            "learning_summary": learning_integration
        }
    
    def escalate_tension_urgency(self, escalation_reason: str) -> Dict[str, Any]:
        """Escalate tension urgency based on new conditions"""
        current_urgency = TensionUrgency(self.urgency_level)
        
        if current_urgency == TensionUrgency.LOW:
            new_urgency = TensionUrgency.MEDIUM
        elif current_urgency == TensionUrgency.MEDIUM:
            new_urgency = TensionUrgency.HIGH
        elif current_urgency == TensionUrgency.HIGH:
            new_urgency = TensionUrgency.CRITICAL
        else:
            new_urgency = current_urgency  # Already at maximum
        
        old_urgency = self.urgency_level
        self.urgency_level = new_urgency.value
        
        escalation_event = {
            "escalation_reason": escalation_reason,
            "old_urgency": old_urgency,
            "new_urgency": new_urgency.value,
            "escalation_timestamp": datetime.now().isoformat()
        }
        
        self.tension_evolution.append({
            "phase": "urgency_escalation",
            "timestamp": datetime.now().isoformat(),
            "escalation": escalation_event
        })
        
        return {
            "urgency_escalated": True,
            "old_urgency": old_urgency,
            "new_urgency": new_urgency.value,
            "immediate_action_required": new_urgency == TensionUrgency.CRITICAL
        }
    
    def _evaluate_win_criteria(self, resolution_evidence: Dict[str, Any]) -> bool:
        """Evaluate if WIN criteria have been met"""
        if not self.resolution_success_criteria:
            return False
        
        evidence_metrics = resolution_evidence.get("metrics", {})
        
        criteria_met = 0
        total_criteria = len(self.resolution_success_criteria)
        
        for criterion, expected_value in self.resolution_success_criteria.items():
            if criterion in evidence_metrics:
                actual_value = evidence_metrics[criterion]
                
                # Simple comparison logic - can be enhanced with sophisticated evaluation
                if isinstance(expected_value, (int, float)) and isinstance(actual_value, (int, float)):
                    if actual_value >= expected_value:
                        criteria_met += 1
                elif str(actual_value).lower() == str(expected_value).lower():
                    criteria_met += 1
        
        # WIN achieved if 80% or more criteria met
        win_threshold = 0.8
        return (criteria_met / total_criteria) >= win_threshold if total_criteria > 0 else False
    
    def get_tension_status_summary(self) -> Dict[str, Any]:
        """Get comprehensive status summary of this tension"""
        return {
            "tension_identity": self.tension_identity,
            "tension_type": self.tension_type,
            "urgency_level": self.urgency_level,
            "current_phase": self.current_resolution_phase,
            "strategic_significance": self.strategic_significance,
            "existential_threat_level": self.existential_threat_level,
            "age_analysis_complete": self.age_analysis_complete,
            "win_validation_status": self.win_validation_status,
            "evolution_events": len(self.tension_evolution or []),
            "required_age_actors": self.required_age_actors or [],
            "days_since_emergence": (datetime.now() - self.tension_emergence_date).days if self.tension_emergence_date else 0,
            "resolution_progress": self._calculate_resolution_progress()
        }
    
    def _calculate_resolution_progress(self) -> float:
        """Calculate resolution progress as 0-1 score"""
        phase_progress = {
            TensionResolutionPhase.RECOGNITION.value: 0.2,
            TensionResolutionPhase.ORCHESTRATION.value: 0.4,
            TensionResolutionPhase.EVENT_EXECUTION.value: 0.6,
            TensionResolutionPhase.WIN_VALIDATION.value: 0.8,
            TensionResolutionPhase.LEARNING_INTEGRATION.value: 0.9,
            TensionResolutionPhase.RESOLVED.value: 1.0
        }
        
        return phase_progress.get(self.current_resolution_phase, 0.0)
    
    @property
    def is_resolved(self) -> bool:
        """Check if tension has been successfully resolved"""
        return (self.current_resolution_phase == TensionResolutionPhase.RESOLVED.value and 
                self.win_validation_status == "win_achieved")
    
    @property
    def requires_immediate_attention(self) -> bool:
        """Check if tension requires immediate AGE attention"""
        return (self.urgency_level == TensionUrgency.CRITICAL.value or
                self.existential_threat_level >= 0.7)
    
    @property
    def is_age_ready(self) -> bool:
        """Check if tension is ready for AGE orchestration"""
        return (self.age_analysis_complete and 
                self.current_resolution_phase in [
                    TensionResolutionPhase.ORCHESTRATION.value,
                    TensionResolutionPhase.EVENT_EXECUTION.value
                ])
    
    class Meta:
        app_label = 'trm_api'
        verbose_name = 'Strategic Tension'
        verbose_name_plural = 'Strategic Tensions'


# === TENSION ANALYSIS UTILITIES ===

class TensionAnalyzer:
    """Utility class for analyzing strategic tensions"""
    
    @staticmethod
    def identify_tension_patterns(tensions: List[StrategicTension]) -> Dict[str, Any]:
        """Identify patterns across multiple tensions"""
        patterns = {
            "common_types": {},
            "urgency_distribution": {},
            "resolution_velocity": {},
            "stakeholder_impact_patterns": {}
        }
        
        for tension in tensions:
            # Count tension types
            tension_type = tension.tension_type
            patterns["common_types"][tension_type] = patterns["common_types"].get(tension_type, 0) + 1
            
            # Count urgency levels
            urgency = tension.urgency_level
            patterns["urgency_distribution"][urgency] = patterns["urgency_distribution"].get(urgency, 0) + 1
        
        return patterns
    
    @staticmethod
    def recommend_age_strategy(tension: StrategicTension) -> Dict[str, Any]:
        """Recommend AGE orchestration strategy for tension"""
        strategy = {
            "recommended_actors": [],
            "response_urgency": tension.urgency_level,
            "resource_requirements": {},
            "success_probability": 0.0
        }
        
        # Actor recommendations based on tension type
        actor_mapping = {
            TensionType.KNOWLEDGE_DEFICIT: ["KnowledgeExtractionActor", "DataSensingActor"],
            TensionType.RESOURCE_MISALIGNMENT: ["ResourceCoordinationActor", "OptimizationActor"],
            TensionType.EXECUTION_PARALYSIS: ["ProjectManagementActor", "TensionResolutionActor"],
            TensionType.STAKEHOLDER_DISCORD: ["TensionResolutionActor", "CommunicationActor"]
        }
        
        tension_type_enum = TensionType(tension.tension_type)
        strategy["recommended_actors"] = actor_mapping.get(tension_type_enum, ["TensionResolutionActor"])
        
        # Success probability based on tension characteristics
        base_probability = 0.7
        if tension.urgency_level == TensionUrgency.CRITICAL.value:
            base_probability += 0.1  # Higher success with critical urgency
        if tension.strategic_significance > 0.8:
            base_probability += 0.1  # Higher success with high significance
        
        strategy["success_probability"] = min(base_probability, 1.0)
        
        return strategy 