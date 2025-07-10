#!/usr/bin/env python3
"""
Strategic Unit - Tension-Driven Strategic Response (Not Project CRUD)

Philosophy: Strategic Units are purposeful responses to existential tensions.
They orchestrate AGE Actors to achieve measurable strategic outcomes (WINs).

Semantic Principle: Every Strategic Unit exists to resolve specific tension
through Recognition → Event → WIN orchestration.

ELIMINATION: No more Project CRUD. Only strategic tension resolution.
"""

from neomodel import (
    StructuredNode, StringProperty, DateTimeProperty, FloatProperty,
    JSONProperty, RelationshipTo, RelationshipFrom, ArrayProperty,
    BooleanProperty, IntegerProperty
)
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
from enum import Enum
import json
import uuid

from trm_api.graph_models.base import BaseNode


class StrategicUnitType(str, Enum):
    """Types of Strategic Units based on tension resolution approach"""
    CRISIS_RESPONSE_UNIT = "crisis_response_unit"              # Respond to existential crisis
    OPPORTUNITY_CAPTURE_UNIT = "opportunity_capture_unit"      # Capture strategic opportunities
    KNOWLEDGE_ACQUISITION_UNIT = "knowledge_acquisition_unit"  # Acquire critical knowledge
    RESOURCE_OPTIMIZATION_UNIT = "resource_optimization_unit"  # Optimize resource deployment
    STAKEHOLDER_ALIGNMENT_UNIT = "stakeholder_alignment_unit"  # Align stakeholder interests
    EXECUTION_ACCELERATION_UNIT = "execution_acceleration_unit"  # Accelerate strategic execution
    INNOVATION_BREAKTHROUGH_UNIT = "innovation_breakthrough_unit"  # Create innovation breakthroughs
    CULTURAL_TRANSFORMATION_UNIT = "cultural_transformation_unit"  # Transform organizational culture
    MARKET_RESPONSE_UNIT = "market_response_unit"              # Respond to market forces
    SYSTEMIC_IMPROVEMENT_UNIT = "systemic_improvement_unit"    # Improve system performance


class AGEOrchestrationPhase(str, Enum):
    """Phases of AGE orchestration within Strategic Unit"""
    TENSION_RECOGNITION = "tension_recognition"      # Recognizing and analyzing tension
    ACTOR_COORDINATION = "actor_coordination"        # Coordinating AGE actors
    EVENT_EXECUTION = "event_execution"              # Executing strategic events
    WIN_VALIDATION = "win_validation"                # Validating WIN achievement
    LEARNING_INTEGRATION = "learning_integration"    # Integrating lessons learned
    STRATEGIC_COMPLETION = "strategic_completion"    # Strategic unit completed


class WinAchievementStatus(str, Enum):
    """Status of WIN achievement for Strategic Unit"""
    WIN_PENDING = "win_pending"                      # WIN criteria not yet met
    WIN_IN_PROGRESS = "win_in_progress"             # Working toward WIN criteria
    WIN_ACHIEVED = "win_achieved"                    # WIN criteria successfully met
    WIN_EXCEEDED = "win_exceeded"                    # WIN criteria exceeded expectations
    WIN_FAILED = "win_failed"                       # WIN criteria could not be met
    WIN_REDEFINED = "win_redefined"                 # WIN criteria have been redefined


class StrategicUnit(BaseNode):
    """
    Strategic Unit - Purposeful response to existential tension
    
    Semantic Foundation: Strategic Units orchestrate AGE Actors to resolve
    specific tensions through measurable strategic outcomes.
    
    Architecture: Tension → Recognition → Event → WIN → Learning
    """
    
    # === STRATEGIC IDENTITY ===
    unit_identity = StringProperty(required=True, unique_index=True)
    strategic_intent = StringProperty(required=True)  # "Eliminate customer confusion"
    semantic_purpose = StringProperty(required=True)   # Clear purpose statement
    
    unit_type = StringProperty(
        choices=[(t.value, t.value) for t in StrategicUnitType],
        required=True,
        index=True
    )
    
    # === TENSION-DRIVEN FOUNDATION ===
    originating_tension_identity = StringProperty(required=True, index=True)
    tension_resolution_approach = StringProperty(required=True)
    strategic_significance = FloatProperty(default=0.5)  # 0-1 significance score
    existential_importance = FloatProperty(default=0.0)  # 0-1 importance to organization
    
    # === WIN CRITERIA & VALIDATION ===
    win_criteria = JSONProperty(required=True)        # Measurable WIN conditions
    win_achievement_status = StringProperty(
        choices=[(w.value, w.value) for w in WinAchievementStatus],
        default=WinAchievementStatus.WIN_PENDING.value,
        index=True
    )
    
    # WIN measurement data
    baseline_metrics = JSONProperty(default=dict)      # State before unit activation
    target_metrics = JSONProperty(default=dict)        # Target state to achieve
    current_metrics = JSONProperty(default=dict)       # Current measured state
    win_validation_evidence = JSONProperty(default=dict)  # Evidence of WIN achievement
    
    # === AGE ORCHESTRATION STATE ===
    current_age_phase = StringProperty(
        choices=[(p.value, p.value) for p in AGEOrchestrationPhase],
        default=AGEOrchestrationPhase.TENSION_RECOGNITION.value,
        index=True
    )
    
    orchestration_intelligence = JSONProperty(default=dict)   # AGE orchestration insights
    actor_coordination_plan = JSONProperty(default=dict)      # How actors are coordinated
    active_age_actors = ArrayProperty(StringProperty())       # Currently active actors
    
    # === EVENT-DRIVEN EXECUTION ===
    strategic_events_log = JSONProperty(default=list)         # Log of strategic events
    execution_timeline = JSONProperty(default=dict)           # Timeline of key events
    next_planned_events = JSONProperty(default=list)          # Upcoming strategic events
    
    # Event coordination
    event_triggers = JSONProperty(default=list)               # Conditions that trigger events
    event_execution_patterns = JSONProperty(default=dict)     # Learned execution patterns
    
    # === RESOURCE COORDINATION ===
    coordinated_resources = JSONProperty(default=dict)        # Resources being coordinated
    resource_optimization_status = JSONProperty(default=dict) # Resource optimization state
    resource_constraints = JSONProperty(default=list)         # Current resource constraints
    
    # === TEMPORAL DYNAMICS ===
    unit_activation_date = DateTimeProperty(default_now=True)
    tension_escalation_deadline = DateTimeProperty()
    target_win_achievement_date = DateTimeProperty()
    actual_win_achievement_date = DateTimeProperty()
    unit_completion_date = DateTimeProperty()
    
    # Temporal intelligence
    optimal_execution_window = JSONProperty(default=dict)     # Optimal timing for actions
    velocity_requirements = JSONProperty(default=dict)        # Required execution velocity
    temporal_constraints = JSONProperty(default=list)         # Time-based constraints
    
    # === STAKEHOLDER DYNAMICS ===
    primary_stakeholders = ArrayProperty(StringProperty())    # Key stakeholders
    stakeholder_alignment_status = JSONProperty(default=dict) # Stakeholder alignment state
    communication_strategy = JSONProperty(default=dict)       # How to communicate with stakeholders
    
    # === LEARNING & ADAPTATION ===
    strategic_intelligence_gained = JSONProperty(default=dict)  # Intelligence accumulated
    execution_lessons_learned = JSONProperty(default=list)     # Lessons from execution
    adaptation_triggers = JSONProperty(default=list)           # Conditions requiring adaptation
    success_patterns_identified = JSONProperty(default=dict)   # Patterns of successful execution
    
    # === STRATEGIC RELATIONSHIPS ===
    
    # Responds to Strategic Tension (Core relationship)
    responds_to_tension = RelationshipTo(
        'trm_api.ontology.strategic_tension.StrategicTension',
        'RESPONDS_TO_TENSION'
    )
    
    # Orchestrates AGE Actors
    orchestrates_actors = RelationshipTo(
        'trm_api.ontology.age_actor.AGEActor',
        'ORCHESTRATES_ACTOR'
    )
    
    # Generates Strategic Events
    generates_events = RelationshipTo(
        'trm_api.ontology.strategic_event.StrategicEvent',
        'GENERATES_EVENT'
    )
    
    # Coordinates Resources
    coordinates_resources = RelationshipTo(
        'trm_api.ontology.coordinated_resource.CoordinatedResource',
        'COORDINATES_RESOURCE'
    )
    
    # Impacts Stakeholders
    impacts_stakeholders = RelationshipTo(
        'trm_api.ontology.stakeholder.Stakeholder',
        'IMPACTS_STAKEHOLDER'
    )
    
    # Managed by AGE Orchestrator
    managed_by_orchestrator = RelationshipFrom(
        'trm_api.ontology.age_orchestrator.AGEOrchestrator',
        'MANAGES_STRATEGIC_UNIT'
    )
    
    # Strategic Unit Dependencies
    depends_on_units = RelationshipTo('StrategicUnit', 'DEPENDS_ON')
    enables_units = RelationshipFrom('StrategicUnit', 'DEPENDS_ON')
    
    # WIN Relationships
    achieves_wins = RelationshipTo(
        'trm_api.ontology.win_validation.WinValidation',
        'ACHIEVES_WIN'
    )
    
    # === CORE ORCHESTRATION METHODS ===
    
    def initiate_tension_recognition_phase(self, tension_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Initiate Recognition phase for originating tension
        First phase of Recognition → Event → WIN
        """
        self.current_age_phase = AGEOrchestrationPhase.TENSION_RECOGNITION.value
        
        recognition_data = {
            "originating_tension": self.originating_tension_identity,
            "strategic_intent": self.strategic_intent,
            "tension_context": tension_context,
            "recognition_approach": tension_context.get("recognition_approach", "comprehensive"),
            "stakeholders_involved": self.primary_stakeholders,
            "recognition_initiated_at": datetime.now().isoformat()
        }
        
        # Initialize strategic events log
        if not self.strategic_events_log:
            self.strategic_events_log = []
        
        self.strategic_events_log.append({
            "event_type": "tension_recognition_initiated",
            "timestamp": datetime.now().isoformat(),
            "data": recognition_data
        })
        
        return {
            "recognition_phase": "initiated",
            "unit_identity": self.unit_identity,
            "tension_identity": self.originating_tension_identity,
            "strategic_intent": self.strategic_intent,
            "next_phase": "actor_coordination"
        }
    
    def orchestrate_age_actors(self, orchestration_plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        Orchestrate AGE Actors for strategic execution
        Coordination phase of strategic response
        """
        self.current_age_phase = AGEOrchestrationPhase.ACTOR_COORDINATION.value
        
        # Store orchestration plan
        self.actor_coordination_plan = orchestration_plan
        self.active_age_actors = orchestration_plan.get("assigned_actors", [])
        
        orchestration_data = {
            "coordination_strategy": orchestration_plan.get("strategy", "parallel"),
            "assigned_actors": self.active_age_actors,
            "actor_roles": orchestration_plan.get("actor_roles", {}),
            "coordination_objectives": orchestration_plan.get("objectives", []),
            "expected_outcomes": orchestration_plan.get("expected_outcomes", []),
            "orchestration_initiated_at": datetime.now().isoformat()
        }
        
        self.strategic_events_log.append({
            "event_type": "actor_orchestration_initiated",
            "timestamp": datetime.now().isoformat(),
            "data": orchestration_data
        })
        
        # Update orchestration intelligence
        self.orchestration_intelligence.update({
            "current_coordination": orchestration_data,
            "orchestration_complexity": len(self.active_age_actors),
            "coordination_dependencies": orchestration_plan.get("dependencies", [])
        })
        
        return {
            "orchestration_phase": "initiated",
            "unit_identity": self.unit_identity,
            "actors_orchestrated": len(self.active_age_actors),
            "coordination_plan": orchestration_data,
            "next_phase": "event_execution"
        }
    
    def execute_strategic_events(self, event_execution_plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute Strategic Events - real actions toward WIN
        Event phase of Recognition → Event → WIN
        """
        self.current_age_phase = AGEOrchestrationPhase.EVENT_EXECUTION.value
        
        execution_data = {
            "execution_plan": event_execution_plan,
            "planned_events": event_execution_plan.get("events", []),
            "execution_sequence": event_execution_plan.get("sequence", "parallel"),
            "success_criteria": event_execution_plan.get("success_criteria", {}),
            "execution_initiated_at": datetime.now().isoformat()
        }
        
        # Schedule events for execution
        self.next_planned_events = event_execution_plan.get("events", [])
        
        # Update execution timeline
        current_timeline = self.execution_timeline or {}
        current_timeline.update({
            "event_execution_start": datetime.now().isoformat(),
            "planned_completion": event_execution_plan.get("target_completion"),
            "execution_milestones": event_execution_plan.get("milestones", [])
        })
        self.execution_timeline = current_timeline
        
        self.strategic_events_log.append({
            "event_type": "strategic_execution_initiated",
            "timestamp": datetime.now().isoformat(),
            "data": execution_data
        })
        
        return {
            "execution_phase": "initiated",
            "unit_identity": self.unit_identity,
            "events_planned": len(self.next_planned_events),
            "execution_data": execution_data,
            "next_phase": "win_validation"
        }
    
    def validate_win_achievement(self, validation_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate WIN achievement - measure strategic success
        WIN phase of Recognition → Event → WIN
        """
        self.current_age_phase = AGEOrchestrationPhase.WIN_VALIDATION.value
        
        # Update current metrics
        self.current_metrics = validation_data.get("current_metrics", {})
        self.win_validation_evidence = validation_data.get("evidence", {})
        
        # Evaluate WIN criteria
        win_evaluation = self._evaluate_win_criteria(validation_data)
        
        # Update WIN status
        if win_evaluation["win_achieved"]:
            self.win_achievement_status = WinAchievementStatus.WIN_ACHIEVED.value
            self.actual_win_achievement_date = datetime.now()
            
            if win_evaluation.get("exceeded_expectations", False):
                self.win_achievement_status = WinAchievementStatus.WIN_EXCEEDED.value
        else:
            self.win_achievement_status = WinAchievementStatus.WIN_FAILED.value
        
        validation_result = {
            "win_achieved": win_evaluation["win_achieved"],
            "unit_identity": self.unit_identity,
            "win_status": self.win_achievement_status,
            "validation_evidence": self.win_validation_evidence,
            "criteria_evaluation": win_evaluation,
            "validation_timestamp": datetime.now().isoformat()
        }
        
        self.strategic_events_log.append({
            "event_type": "win_validation_completed",
            "timestamp": datetime.now().isoformat(),
            "data": validation_result
        })
        
        return validation_result
    
    def integrate_strategic_learning(self, learning_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Integrate learning from strategic execution
        Learning phase - final step before completion
        """
        self.current_age_phase = AGEOrchestrationPhase.LEARNING_INTEGRATION.value
        
        # Update strategic intelligence
        intelligence_gained = learning_data.get("intelligence", {})
        current_intelligence = self.strategic_intelligence_gained or {}
        current_intelligence.update(intelligence_gained)
        self.strategic_intelligence_gained = current_intelligence
        
        # Record lessons learned
        lessons = learning_data.get("lessons", [])
        current_lessons = self.execution_lessons_learned or []
        current_lessons.extend(lessons)
        self.execution_lessons_learned = current_lessons
        
        # Identify success patterns
        patterns = learning_data.get("success_patterns", {})
        current_patterns = self.success_patterns_identified or {}
        current_patterns.update(patterns)
        self.success_patterns_identified = current_patterns
        
        learning_summary = {
            "intelligence_integrated": len(intelligence_gained),
            "lessons_recorded": len(lessons),
            "patterns_identified": len(patterns),
            "learning_timestamp": datetime.now().isoformat()
        }
        
        self.strategic_events_log.append({
            "event_type": "learning_integration_completed",
            "timestamp": datetime.now().isoformat(),
            "data": learning_summary
        })
        
        # Check if unit can be completed
        if self.win_achievement_status in [WinAchievementStatus.WIN_ACHIEVED.value, 
                                         WinAchievementStatus.WIN_EXCEEDED.value]:
            self.current_age_phase = AGEOrchestrationPhase.STRATEGIC_COMPLETION.value
            self.unit_completion_date = datetime.now()
        
        return {
            "learning_integrated": True,
            "unit_identity": self.unit_identity,
            "unit_status": self.current_age_phase,
            "learning_summary": learning_summary
        }
    
    def coordinate_resource_utilization(self, coordination_request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Coordinate resource utilization for strategic objectives
        Intelligent resource coordination, not assignment
        """
        resource_type = coordination_request.get("resource_type")
        utilization_purpose = coordination_request.get("purpose")
        coordination_strategy = coordination_request.get("strategy", "optimal")
        
        coordination_result = {
            "resource_type": resource_type,
            "coordination_strategy": coordination_strategy,
            "utilization_purpose": utilization_purpose,
            "coordination_timestamp": datetime.now().isoformat(),
            "optimization_applied": True
        }
        
        # Update coordinated resources
        current_resources = self.coordinated_resources or {}
        if resource_type not in current_resources:
            current_resources[resource_type] = []
        
        current_resources[resource_type].append(coordination_result)
        self.coordinated_resources = current_resources
        
        self.strategic_events_log.append({
            "event_type": "resource_coordination_executed",
            "timestamp": datetime.now().isoformat(),
            "data": coordination_result
        })
        
        return {
            "coordination_completed": True,
            "unit_identity": self.unit_identity,
            "resource_type": resource_type,
            "coordination_result": coordination_result
        }
    
    def trigger_strategic_adaptation(self, adaptation_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Trigger strategic adaptation based on changing conditions
        Dynamic response to new information or changing context
        """
        adaptation_trigger = adaptation_context.get("trigger_type")
        adaptation_reason = adaptation_context.get("reason")
        proposed_changes = adaptation_context.get("proposed_changes", {})
        
        adaptation_data = {
            "trigger_type": adaptation_trigger,
            "reason": adaptation_reason,
            "proposed_changes": proposed_changes,
            "current_phase": self.current_age_phase,
            "adaptation_timestamp": datetime.now().isoformat()
        }
        
        # Apply adaptations
        if "win_criteria" in proposed_changes:
            self.win_criteria.update(proposed_changes["win_criteria"])
            self.win_achievement_status = WinAchievementStatus.WIN_REDEFINED.value
        
        if "strategic_intent" in proposed_changes:
            self.strategic_intent = proposed_changes["strategic_intent"]
        
        if "actor_coordination" in proposed_changes:
            self.actor_coordination_plan.update(proposed_changes["actor_coordination"])
        
        self.strategic_events_log.append({
            "event_type": "strategic_adaptation_triggered",
            "timestamp": datetime.now().isoformat(),
            "data": adaptation_data
        })
        
        return {
            "adaptation_applied": True,
            "unit_identity": self.unit_identity,
            "adaptation_summary": adaptation_data
        }
    
    def get_strategic_status_summary(self) -> Dict[str, Any]:
        """Get comprehensive strategic status of this unit"""
        progress_score = self._calculate_strategic_progress()
        
        return {
            "unit_identity": self.unit_identity,
            "strategic_intent": self.strategic_intent,
            "unit_type": self.unit_type,
            "originating_tension": self.originating_tension_identity,
            "current_age_phase": self.current_age_phase,
            "win_achievement_status": self.win_achievement_status,
            "strategic_significance": self.strategic_significance,
            "active_age_actors": len(self.active_age_actors or []),
            "coordinated_resources": len(self.coordinated_resources or {}),
            "strategic_events_count": len(self.strategic_events_log or []),
            "strategic_progress": f"{progress_score:.1%}",
            "days_since_activation": (datetime.now() - self.unit_activation_date).days if self.unit_activation_date else 0,
            "completion_status": self._get_completion_status()
        }
    
    # === UTILITY METHODS ===
    
    def _evaluate_win_criteria(self, validation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate if WIN criteria have been met"""
        current_metrics = validation_data.get("current_metrics", {})
        target_metrics = self.target_metrics or {}
        
        if not target_metrics:
            return {"win_achieved": False, "reason": "no_target_metrics_defined"}
        
        criteria_results = {}
        criteria_met = 0
        total_criteria = len(target_metrics)
        
        for criterion, target_value in target_metrics.items():
            current_value = current_metrics.get(criterion)
            
            if current_value is not None:
                if isinstance(target_value, (int, float)) and isinstance(current_value, (int, float)):
                    met = current_value >= target_value
                    criteria_results[criterion] = {
                        "met": met,
                        "current": current_value,
                        "target": target_value,
                        "percentage": (current_value / target_value * 100) if target_value > 0 else 0
                    }
                    if met:
                        criteria_met += 1
                else:
                    # String comparison
                    met = str(current_value).lower() == str(target_value).lower()
                    criteria_results[criterion] = {
                        "met": met,
                        "current": current_value,
                        "target": target_value
                    }
                    if met:
                        criteria_met += 1
            else:
                criteria_results[criterion] = {
                    "met": False,
                    "current": None,
                    "target": target_value,
                    "reason": "metric_not_available"
                }
        
        win_threshold = 0.8  # 80% of criteria must be met
        win_achieved = (criteria_met / total_criteria) >= win_threshold if total_criteria > 0 else False
        
        # Check for exceeded expectations
        exceeded_expectations = False
        if win_achieved:
            exceeded_count = sum(1 for result in criteria_results.values() 
                               if result.get("percentage", 0) > 120)  # 20% above target
            exceeded_expectations = (exceeded_count / total_criteria) >= 0.5
        
        return {
            "win_achieved": win_achieved,
            "exceeded_expectations": exceeded_expectations,
            "criteria_met": criteria_met,
            "total_criteria": total_criteria,
            "criteria_percentage": (criteria_met / total_criteria * 100) if total_criteria > 0 else 0,
            "detailed_results": criteria_results
        }
    
    def _calculate_strategic_progress(self) -> float:
        """Calculate overall strategic progress as 0-1 score"""
        phase_weights = {
            AGEOrchestrationPhase.TENSION_RECOGNITION.value: 0.1,
            AGEOrchestrationPhase.ACTOR_COORDINATION.value: 0.3,
            AGEOrchestrationPhase.EVENT_EXECUTION.value: 0.6,
            AGEOrchestrationPhase.WIN_VALIDATION.value: 0.8,
            AGEOrchestrationPhase.LEARNING_INTEGRATION.value: 0.9,
            AGEOrchestrationPhase.STRATEGIC_COMPLETION.value: 1.0
        }
        
        base_progress = phase_weights.get(self.current_age_phase, 0.0)
        
        # Adjust based on WIN status
        if self.win_achievement_status == WinAchievementStatus.WIN_ACHIEVED.value:
            base_progress += 0.1
        elif self.win_achievement_status == WinAchievementStatus.WIN_EXCEEDED.value:
            base_progress += 0.2
        
        return min(base_progress, 1.0)
    
    def _get_completion_status(self) -> str:
        """Get human-readable completion status"""
        if self.current_age_phase == AGEOrchestrationPhase.STRATEGIC_COMPLETION.value:
            if self.win_achievement_status == WinAchievementStatus.WIN_ACHIEVED.value:
                return "Successfully Completed"
            elif self.win_achievement_status == WinAchievementStatus.WIN_EXCEEDED.value:
                return "Completed with Excellence"
            else:
                return "Completed"
        elif self.win_achievement_status == WinAchievementStatus.WIN_FAILED.value:
            return "Failed - WIN Not Achieved"
        else:
            return f"In Progress - {self.current_age_phase.replace('_', ' ').title()}"
    
    @property
    def is_strategically_complete(self) -> bool:
        """Check if strategic unit has achieved its purpose"""
        return (self.current_age_phase == AGEOrchestrationPhase.STRATEGIC_COMPLETION.value and
                self.win_achievement_status in [WinAchievementStatus.WIN_ACHIEVED.value,
                                               WinAchievementStatus.WIN_EXCEEDED.value])
    
    @property
    def requires_immediate_attention(self) -> bool:
        """Check if unit requires immediate strategic attention"""
        return (self.win_achievement_status == WinAchievementStatus.WIN_FAILED.value or
                self.existential_importance >= 0.8)
    
    @property
    def is_high_strategic_value(self) -> bool:
        """Check if unit provides high strategic value"""
        return (self.strategic_significance >= 0.8 and
                self.win_achievement_status in [WinAchievementStatus.WIN_ACHIEVED.value,
                                               WinAchievementStatus.WIN_EXCEEDED.value])
    
    class Meta:
        app_label = 'trm_api'
        verbose_name = 'Strategic Unit'
        verbose_name_plural = 'Strategic Units' 