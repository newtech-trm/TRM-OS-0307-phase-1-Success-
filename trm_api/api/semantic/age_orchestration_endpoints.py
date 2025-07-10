#!/usr/bin/env python3
"""
AGE Orchestration Semantic APIs - NO MORE CRUD

Philosophy: APIs that trigger semantic actions, not data mutations.
Every endpoint orchestrates strategic intelligence toward WIN achievement.

Semantic Principle: Recognition → Event → WIN driven by strategic tensions.

ELIMINATION: No POST/GET/PUT/DELETE. Only strategic action endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import uuid
import asyncio

from pydantic import BaseModel, Field
from trm_api.ontology.strategic_tension import StrategicTension, TensionType, TensionUrgency
from trm_api.ontology.age_actor import AGEActor, ActorType, ActorExecutionState
from trm_api.ontology.strategic_unit import StrategicUnit, StrategicUnitType, AGEOrchestrationPhase


# === SEMANTIC REQUEST/RESPONSE MODELS ===

class TensionRecognitionRequest(BaseModel):
    """Request to initiate tension recognition"""
    tension_identity: str = Field(..., description="Unique identifier for the tension")
    semantic_description: str = Field(..., description="Clear description of the tension")
    tension_type: TensionType = Field(..., description="Type of strategic tension")
    urgency_level: TensionUrgency = Field(default=TensionUrgency.MEDIUM, description="Urgency level")
    originating_context: Dict[str, Any] = Field(..., description="Context where tension emerged")
    stakeholder_impact: Dict[str, Any] = Field(default_factory=dict, description="Stakeholder impact analysis")
    strategic_significance: float = Field(default=0.5, ge=0.0, le=1.0, description="Strategic significance (0-1)")
    existential_threat_level: float = Field(default=0.0, ge=0.0, le=1.0, description="Existential threat level (0-1)")


class AGEActorOrchestrationRequest(BaseModel):
    """Request to orchestrate AGE actors for strategic response"""
    tension_identity: str = Field(..., description="Target tension to resolve")
    required_actor_types: List[ActorType] = Field(..., description="Required types of AGE actors")
    orchestration_strategy: str = Field(default="parallel", description="Actor coordination strategy")
    strategic_objectives: List[str] = Field(..., description="Strategic objectives to achieve")
    resource_requirements: Dict[str, Any] = Field(default_factory=dict, description="Required resources")
    timeline_constraints: Dict[str, Any] = Field(default_factory=dict, description="Timeline constraints")


class StrategicEventExecutionRequest(BaseModel):
    """Request to execute strategic events"""
    strategic_unit_identity: str = Field(..., description="Strategic unit executing events")
    event_execution_plan: Dict[str, Any] = Field(..., description="Plan for event execution")
    success_criteria: Dict[str, Any] = Field(..., description="Criteria for successful execution")
    coordination_requirements: Dict[str, Any] = Field(default_factory=dict, description="Coordination requirements")


class WinValidationRequest(BaseModel):
    """Request to validate WIN achievement"""
    strategic_unit_identity: str = Field(..., description="Strategic unit to validate")
    current_metrics: Dict[str, Any] = Field(..., description="Current measured metrics")
    validation_evidence: Dict[str, Any] = Field(..., description="Evidence of WIN achievement")
    stakeholder_feedback: Dict[str, Any] = Field(default_factory=dict, description="Stakeholder feedback")


class ResourceCoordinationRequest(BaseModel):
    """Request to coordinate resource utilization"""
    strategic_unit_identity: str = Field(..., description="Strategic unit requiring resources")
    resource_type: str = Field(..., description="Type of resource to coordinate")
    utilization_purpose: str = Field(..., description="Purpose of resource utilization")
    coordination_strategy: str = Field(default="optimal", description="Resource coordination strategy")
    optimization_criteria: Dict[str, Any] = Field(default_factory=dict, description="Optimization criteria")


class StrategicAdaptationRequest(BaseModel):
    """Request to trigger strategic adaptation"""
    target_identity: str = Field(..., description="Strategic unit or tension to adapt")
    adaptation_trigger: str = Field(..., description="What triggered the adaptation need")
    adaptation_reason: str = Field(..., description="Reason for adaptation")
    proposed_changes: Dict[str, Any] = Field(..., description="Proposed strategic changes")
    impact_assessment: Dict[str, Any] = Field(default_factory=dict, description="Impact assessment")


# === SEMANTIC RESPONSE MODELS ===

class TensionRecognitionResponse(BaseModel):
    """Response from tension recognition initiation"""
    recognition_initiated: bool
    tension_identity: str
    age_analysis_triggered: bool
    recognition_context: Dict[str, Any]
    next_recommended_action: str
    estimated_resolution_timeline: Optional[Dict[str, Any]] = None


class AGEOrchestrationResponse(BaseModel):
    """Response from AGE actor orchestration"""
    orchestration_successful: bool
    orchestrated_actors: List[str]
    coordination_plan: Dict[str, Any]
    strategic_unit_created: bool
    strategic_unit_identity: Optional[str] = None
    execution_timeline: Dict[str, Any]


class StrategicEventResponse(BaseModel):
    """Response from strategic event execution"""
    execution_initiated: bool
    events_scheduled: int
    execution_plan: Dict[str, Any]
    estimated_completion: str
    success_probability: float


class WinValidationResponse(BaseModel):
    """Response from WIN validation"""
    win_achieved: bool
    win_status: str
    criteria_evaluation: Dict[str, Any]
    strategic_outcome: Dict[str, Any]
    next_strategic_actions: List[str]


class ResourceCoordinationResponse(BaseModel):
    """Response from resource coordination"""
    coordination_successful: bool
    resource_optimization_applied: bool
    coordination_strategy: str
    utilization_efficiency: float
    coordination_summary: Dict[str, Any]


class StrategicStatusResponse(BaseModel):
    """Response with strategic status summary"""
    entity_identity: str
    entity_type: str
    strategic_status: str
    progress_percentage: float
    current_phase: str
    key_metrics: Dict[str, Any]
    strategic_intelligence: Dict[str, Any]


# === SEMANTIC ACTION ROUTER ===

router = APIRouter(prefix="/age/semantic", tags=["AGE Semantic Actions"])


# === TENSION RECOGNITION ACTIONS ===

@router.post("/recognize-strategic-tension", response_model=TensionRecognitionResponse)
async def recognize_strategic_tension(
    recognition_request: TensionRecognitionRequest,
    background_tasks: BackgroundTasks
) -> TensionRecognitionResponse:
    """
    SEMANTIC ACTION: Recognize and analyze strategic tension
    
    This initiates the Recognition phase of Recognition → Event → WIN.
    Creates strategic tension and triggers AGE analysis.
    """
    try:
        # Create strategic tension entity
        tension = StrategicTension(
            tension_identity=recognition_request.tension_identity,
            semantic_description=recognition_request.semantic_description,
            tension_type=recognition_request.tension_type.value,
            urgency_level=recognition_request.urgency_level.value,
            originating_context=recognition_request.originating_context,
            stakeholder_impact=recognition_request.stakeholder_impact,
            strategic_significance=recognition_request.strategic_significance,
            existential_threat_level=recognition_request.existential_threat_level
        )
        tension.save()
        
        # Initiate Recognition phase
        recognition_result = tension.initiate_age_recognition_phase()
        
        # Schedule AGE analysis in background
        background_tasks.add_task(
            _schedule_age_analysis,
            recognition_request.tension_identity,
            recognition_request.originating_context
        )
        
        return TensionRecognitionResponse(
            recognition_initiated=True,
            tension_identity=recognition_request.tension_identity,
            age_analysis_triggered=True,
            recognition_context=recognition_result["recognition_context"],
            next_recommended_action="await_age_analysis_completion",
            estimated_resolution_timeline={
                "analysis_completion": "2-6 hours",
                "orchestration_start": "6-24 hours",
                "initial_events": "1-3 days"
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Tension recognition failed: {str(e)}"
        )


@router.post("/orchestrate-age-response", response_model=AGEOrchestrationResponse)
async def orchestrate_age_response(
    orchestration_request: AGEActorOrchestrationRequest,
    background_tasks: BackgroundTasks
) -> AGEOrchestrationResponse:
    """
    SEMANTIC ACTION: Orchestrate AGE actors for strategic response
    
    This coordinates AGE actors to respond to recognized tension,
    creating a Strategic Unit for coordinated action.
    """
    try:
        # Retrieve tension
        tension = StrategicTension.nodes.get_or_none(
            tension_identity=orchestration_request.tension_identity
        )
        
        if not tension:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tension {orchestration_request.tension_identity} not found"
            )
        
        # Create Strategic Unit
        unit_identity = f"strategic_unit_{uuid.uuid4().hex[:8]}"
        strategic_unit = StrategicUnit(
            unit_identity=unit_identity,
            strategic_intent=f"Resolve {tension.semantic_description}",
            semantic_purpose=f"Coordinated response to {tension.tension_type} tension",
            unit_type=_determine_unit_type(tension.tension_type),
            originating_tension_identity=tension.tension_identity,
            tension_resolution_approach=orchestration_request.orchestration_strategy,
            strategic_significance=tension.strategic_significance,
            win_criteria=_generate_win_criteria(tension, orchestration_request.strategic_objectives)
        )
        strategic_unit.save()
        
        # Connect to tension
        strategic_unit.responds_to_tension.connect(tension)
        
        # Orchestrate AGE actors
        orchestration_plan = await _orchestrate_age_actors(
            orchestration_request.required_actor_types,
            orchestration_request.orchestration_strategy,
            orchestration_request.strategic_objectives,
            orchestration_request.resource_requirements
        )
        
        # Apply orchestration to strategic unit
        orchestration_result = strategic_unit.orchestrate_age_actors(orchestration_plan)
        strategic_unit.save()
        
        # Schedule execution planning in background
        background_tasks.add_task(
            _schedule_execution_planning,
            unit_identity,
            orchestration_plan
        )
        
        return AGEOrchestrationResponse(
            orchestration_successful=True,
            orchestrated_actors=orchestration_plan["assigned_actors"],
            coordination_plan=orchestration_plan,
            strategic_unit_created=True,
            strategic_unit_identity=unit_identity,
            execution_timeline={
                "orchestration_completion": datetime.now().isoformat(),
                "execution_start": orchestration_plan.get("execution_start"),
                "target_completion": orchestration_plan.get("target_completion")
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AGE orchestration failed: {str(e)}"
        )


@router.post("/execute-strategic-events", response_model=StrategicEventResponse)
async def execute_strategic_events(
    execution_request: StrategicEventExecutionRequest,
    background_tasks: BackgroundTasks
) -> StrategicEventResponse:
    """
    SEMANTIC ACTION: Execute strategic events
    
    This triggers the Event phase of Recognition → Event → WIN,
    executing real strategic actions through coordinated AGE actors.
    """
    try:
        # Retrieve strategic unit
        strategic_unit = StrategicUnit.nodes.get_or_none(
            unit_identity=execution_request.strategic_unit_identity
        )
        
        if not strategic_unit:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Strategic unit {execution_request.strategic_unit_identity} not found"
            )
        
        # Execute strategic events
        execution_result = strategic_unit.execute_strategic_events(
            execution_request.event_execution_plan
        )
        strategic_unit.save()
        
        # Schedule actual event execution in background
        background_tasks.add_task(
            _execute_strategic_events_background,
            execution_request.strategic_unit_identity,
            execution_request.event_execution_plan,
            execution_request.success_criteria
        )
        
        # Calculate success probability
        success_probability = _calculate_execution_success_probability(
            strategic_unit,
            execution_request.event_execution_plan
        )
        
        return StrategicEventResponse(
            execution_initiated=True,
            events_scheduled=len(execution_request.event_execution_plan.get("events", [])),
            execution_plan=execution_result["execution_data"],
            estimated_completion=execution_request.event_execution_plan.get("target_completion", "unknown"),
            success_probability=success_probability
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Strategic event execution failed: {str(e)}"
        )


@router.post("/validate-win-achievement", response_model=WinValidationResponse)
async def validate_win_achievement(
    validation_request: WinValidationRequest
) -> WinValidationResponse:
    """
    SEMANTIC ACTION: Validate WIN achievement
    
    This executes the WIN phase of Recognition → Event → WIN,
    measuring strategic success and validating outcomes.
    """
    try:
        # Retrieve strategic unit
        strategic_unit = StrategicUnit.nodes.get_or_none(
            unit_identity=validation_request.strategic_unit_identity
        )
        
        if not strategic_unit:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Strategic unit {validation_request.strategic_unit_identity} not found"
            )
        
        # Validate WIN achievement
        validation_data = {
            "current_metrics": validation_request.current_metrics,
            "evidence": validation_request.validation_evidence,
            "stakeholder_feedback": validation_request.stakeholder_feedback
        }
        
        validation_result = strategic_unit.validate_win_achievement(validation_data)
        strategic_unit.save()
        
        # Determine next strategic actions
        next_actions = _determine_next_strategic_actions(
            strategic_unit,
            validation_result
        )
        
        return WinValidationResponse(
            win_achieved=validation_result["win_achieved"],
            win_status=validation_result["win_status"],
            criteria_evaluation=validation_result["criteria_evaluation"],
            strategic_outcome={
                "unit_identity": validation_request.strategic_unit_identity,
                "outcome_summary": validation_result,
                "strategic_impact": _assess_strategic_impact(strategic_unit, validation_result)
            },
            next_strategic_actions=next_actions
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"WIN validation failed: {str(e)}"
        )


@router.post("/coordinate-resource-utilization", response_model=ResourceCoordinationResponse)
async def coordinate_resource_utilization(
    coordination_request: ResourceCoordinationRequest
) -> ResourceCoordinationResponse:
    """
    SEMANTIC ACTION: Coordinate resource utilization
    
    This intelligently coordinates resources for strategic objectives,
    optimizing utilization rather than basic assignment.
    """
    try:
        # Retrieve strategic unit
        strategic_unit = StrategicUnit.nodes.get_or_none(
            unit_identity=coordination_request.strategic_unit_identity
        )
        
        if not strategic_unit:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Strategic unit {coordination_request.strategic_unit_identity} not found"
            )
        
        # Coordinate resource utilization
        coordination_data = {
            "resource_type": coordination_request.resource_type,
            "purpose": coordination_request.utilization_purpose,
            "strategy": coordination_request.coordination_strategy,
            "optimization_criteria": coordination_request.optimization_criteria
        }
        
        coordination_result = strategic_unit.coordinate_resource_utilization(coordination_data)
        strategic_unit.save()
        
        # Calculate utilization efficiency
        efficiency = _calculate_resource_efficiency(
            coordination_request.resource_type,
            coordination_request.coordination_strategy,
            coordination_request.optimization_criteria
        )
        
        return ResourceCoordinationResponse(
            coordination_successful=True,
            resource_optimization_applied=True,
            coordination_strategy=coordination_request.coordination_strategy,
            utilization_efficiency=efficiency,
            coordination_summary=coordination_result
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Resource coordination failed: {str(e)}"
        )


@router.post("/trigger-strategic-adaptation", response_model=Dict[str, Any])
async def trigger_strategic_adaptation(
    adaptation_request: StrategicAdaptationRequest
) -> Dict[str, Any]:
    """
    SEMANTIC ACTION: Trigger strategic adaptation
    
    This adapts strategic approach based on new intelligence,
    enabling dynamic response to changing conditions.
    """
    try:
        # Determine target type (Strategic Unit or Tension)
        strategic_unit = StrategicUnit.nodes.get_or_none(
            unit_identity=adaptation_request.target_identity
        )
        
        if strategic_unit:
            # Adapt Strategic Unit
            adaptation_context = {
                "trigger_type": adaptation_request.adaptation_trigger,
                "reason": adaptation_request.adaptation_reason,
                "proposed_changes": adaptation_request.proposed_changes,
                "impact_assessment": adaptation_request.impact_assessment
            }
            
            adaptation_result = strategic_unit.trigger_strategic_adaptation(adaptation_context)
            strategic_unit.save()
            
            return {
                "adaptation_successful": True,
                "target_type": "strategic_unit",
                "target_identity": adaptation_request.target_identity,
                "adaptation_summary": adaptation_result
            }
        
        else:
            # Try to adapt Strategic Tension
            tension = StrategicTension.nodes.get_or_none(
                tension_identity=adaptation_request.target_identity
            )
            
            if tension:
                # Adapt tension (e.g., escalate urgency)
                if adaptation_request.adaptation_trigger == "urgency_escalation":
                    escalation_result = tension.escalate_tension_urgency(
                        adaptation_request.adaptation_reason
                    )
                    tension.save()
                    
                    return {
                        "adaptation_successful": True,
                        "target_type": "strategic_tension",
                        "target_identity": adaptation_request.target_identity,
                        "adaptation_summary": escalation_result
                    }
            
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Target {adaptation_request.target_identity} not found"
            )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Strategic adaptation failed: {str(e)}"
        )


@router.get("/strategic-status/{entity_identity}", response_model=StrategicStatusResponse)
async def get_strategic_status(entity_identity: str) -> StrategicStatusResponse:
    """
    SEMANTIC QUERY: Get strategic status of entity
    
    This provides comprehensive strategic intelligence about
    tensions, units, or actors without CRUD operations.
    """
    try:
        # Try to find Strategic Unit first
        strategic_unit = StrategicUnit.nodes.get_or_none(unit_identity=entity_identity)
        
        if strategic_unit:
            status_summary = strategic_unit.get_strategic_status_summary()
            
            return StrategicStatusResponse(
                entity_identity=entity_identity,
                entity_type="strategic_unit",
                strategic_status=status_summary["completion_status"],
                progress_percentage=float(status_summary["strategic_progress"].rstrip('%')),
                current_phase=status_summary["current_age_phase"],
                key_metrics={
                    "active_actors": status_summary["active_age_actors"],
                    "coordinated_resources": status_summary["coordinated_resources"],
                    "events_executed": status_summary["strategic_events_count"],
                    "win_status": status_summary["win_achievement_status"]
                },
                strategic_intelligence={
                    "strategic_significance": status_summary["strategic_significance"],
                    "days_active": status_summary["days_since_activation"],
                    "originating_tension": status_summary["originating_tension"]
                }
            )
        
        # Try to find Strategic Tension
        tension = StrategicTension.nodes.get_or_none(tension_identity=entity_identity)
        
        if tension:
            status_summary = tension.get_tension_status_summary()
            
            return StrategicStatusResponse(
                entity_identity=entity_identity,
                entity_type="strategic_tension",
                strategic_status=status_summary["current_phase"],
                progress_percentage=status_summary["resolution_progress"] * 100,
                current_phase=status_summary["current_phase"],
                key_metrics={
                    "urgency_level": status_summary["urgency_level"],
                    "strategic_significance": status_summary["strategic_significance"],
                    "threat_level": status_summary["existential_threat_level"],
                    "required_actors": len(status_summary["required_age_actors"])
                },
                strategic_intelligence={
                    "tension_type": status_summary["tension_type"],
                    "days_since_emergence": status_summary["days_since_emergence"],
                    "evolution_events": status_summary["evolution_events"],
                    "win_validation_status": status_summary["win_validation_status"]
                }
            )
        
        # Try to find AGE Actor
        actor = AGEActor.nodes.get_or_none(actor_identity=entity_identity)
        
        if actor:
            status_summary = actor.get_actor_status_summary()
            
            return StrategicStatusResponse(
                entity_identity=entity_identity,
                entity_type="age_actor",
                strategic_status=status_summary["current_execution_state"],
                progress_percentage=status_summary["execution_success_rate"] * 100,
                current_phase=status_summary["current_execution_state"],
                key_metrics={
                    "total_executions": status_summary["total_executions"],
                    "success_rate": status_summary["execution_success_rate"],
                    "strategic_impact": status_summary["strategic_impact_score"],
                    "active_capabilities": len(status_summary["active_capabilities"])
                },
                strategic_intelligence={
                    "actor_type": status_summary["actor_type"],
                    "semantic_purpose": status_summary["semantic_purpose"],
                    "integration_type": status_summary["integration_type"],
                    "performance_summary": status_summary["performance_summary"]
                }
            )
        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Entity {entity_identity} not found"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Strategic status query failed: {str(e)}"
        )


# === BACKGROUND TASK FUNCTIONS ===

async def _schedule_age_analysis(tension_identity: str, context: Dict[str, Any]):
    """Schedule AGE analysis of tension in background"""
    # Simulate AGE analysis (would be real AI analysis in production)
    await asyncio.sleep(2)  # Simulate analysis time
    
    tension = StrategicTension.nodes.get_or_none(tension_identity=tension_identity)
    if tension:
        analysis_result = {
            "response_strategy": {"approach": "multi_actor_coordination"},
            "required_actors": ["DataSensingActor", "TensionResolutionActor"],
            "resource_needs": {"ai_capabilities": ["nlp", "analysis"], "compute_resources": "medium"}
        }
        
        tension.record_age_analysis(analysis_result)
        tension.save()


async def _schedule_execution_planning(unit_identity: str, orchestration_plan: Dict[str, Any]):
    """Schedule execution planning in background"""
    # Simulate execution planning
    await asyncio.sleep(1)  # Simulate planning time
    
    strategic_unit = StrategicUnit.nodes.get_or_none(unit_identity=unit_identity)
    if strategic_unit:
        strategic_unit.transition_to_orchestration_phase()
        strategic_unit.save()


async def _execute_strategic_events_background(unit_identity: str, execution_plan: Dict[str, Any], 
                                             success_criteria: Dict[str, Any]):
    """Execute strategic events in background"""
    # Simulate event execution
    events = execution_plan.get("events", [])
    
    for event in events:
        await asyncio.sleep(0.5)  # Simulate event execution time
        # In production, this would trigger real AGE actor execution


# === UTILITY FUNCTIONS ===

def _determine_unit_type(tension_type: str) -> str:
    """Determine Strategic Unit type based on tension type"""
    mapping = {
        "existential_crisis": StrategicUnitType.CRISIS_RESPONSE_UNIT.value,
        "opportunity_gap": StrategicUnitType.OPPORTUNITY_CAPTURE_UNIT.value,
        "knowledge_deficit": StrategicUnitType.KNOWLEDGE_ACQUISITION_UNIT.value,
        "resource_misalignment": StrategicUnitType.RESOURCE_OPTIMIZATION_UNIT.value,
        "stakeholder_discord": StrategicUnitType.STAKEHOLDER_ALIGNMENT_UNIT.value
    }
    return mapping.get(tension_type, StrategicUnitType.CRISIS_RESPONSE_UNIT.value)


def _generate_win_criteria(tension: StrategicTension, objectives: List[str]) -> Dict[str, Any]:
    """Generate WIN criteria based on tension and objectives"""
    return {
        "tension_resolution_confirmed": True,
        "stakeholder_satisfaction_score": 0.8,
        "strategic_objectives_achieved": len(objectives),
        "measurable_improvement_demonstrated": True
    }


async def _orchestrate_age_actors(actor_types: List[ActorType], strategy: str, 
                                objectives: List[str], resource_requirements: Dict[str, Any]) -> Dict[str, Any]:
    """Orchestrate AGE actors for strategic response"""
    assigned_actors = []
    
    for actor_type in actor_types:
        # Find or create appropriate AGE actor
        actor_identity = f"{actor_type.value}_{uuid.uuid4().hex[:6]}"
        assigned_actors.append(actor_identity)
    
    return {
        "strategy": strategy,
        "assigned_actors": assigned_actors,
        "actor_roles": {actor: f"Execute {actor} responsibilities" for actor in assigned_actors},
        "objectives": objectives,
        "expected_outcomes": [f"Outcome for {obj}" for obj in objectives],
        "execution_start": (datetime.now() + timedelta(hours=1)).isoformat(),
        "target_completion": (datetime.now() + timedelta(days=7)).isoformat(),
        "dependencies": []
    }


def _calculate_execution_success_probability(strategic_unit: StrategicUnit, 
                                           execution_plan: Dict[str, Any]) -> float:
    """Calculate probability of successful execution"""
    base_probability = 0.7
    
    # Adjust based on strategic significance
    if strategic_unit.strategic_significance > 0.8:
        base_probability += 0.1
    
    # Adjust based on number of events
    event_count = len(execution_plan.get("events", []))
    if event_count > 5:
        base_probability -= 0.1  # More complex execution
    
    return min(base_probability, 1.0)


def _determine_next_strategic_actions(strategic_unit: StrategicUnit, 
                                    validation_result: Dict[str, Any]) -> List[str]:
    """Determine next strategic actions based on WIN validation"""
    if validation_result["win_achieved"]:
        return [
            "Integrate strategic learning",
            "Document success patterns",
            "Plan strategic unit completion",
            "Identify follow-up opportunities"
        ]
    else:
        return [
            "Analyze failure causes",
            "Adapt strategic approach",
            "Re-coordinate AGE actors",
            "Revise WIN criteria if needed"
        ]


def _assess_strategic_impact(strategic_unit: StrategicUnit, 
                           validation_result: Dict[str, Any]) -> Dict[str, Any]:
    """Assess strategic impact of unit execution"""
    return {
        "organizational_impact": "High" if strategic_unit.strategic_significance > 0.7 else "Medium",
        "stakeholder_value_created": validation_result.get("win_achieved", False),
        "knowledge_gained": len(strategic_unit.strategic_intelligence_gained or {}),
        "capability_enhancement": "Significant" if validation_result.get("win_achieved") else "Limited"
    }


def _calculate_resource_efficiency(resource_type: str, strategy: str, 
                                 optimization_criteria: Dict[str, Any]) -> float:
    """Calculate resource utilization efficiency"""
    base_efficiency = 0.8
    
    if strategy == "optimal":
        base_efficiency += 0.1
    
    if optimization_criteria:
        base_efficiency += 0.05
    
    return min(base_efficiency, 1.0) 