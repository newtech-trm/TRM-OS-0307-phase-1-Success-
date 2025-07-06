"""
Advanced Reasoning Engine - Core implementation

Provides sophisticated reasoning capabilities for TRM-OS AI agents following 
the Recognition → Event → WIN philosophy.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union, Tuple
from uuid import uuid4

from .reasoning_types import (
    ReasoningContext, ReasoningStep, ReasoningResult, ReasoningType,
    UncertaintyLevel, CausalChain, KnowledgeNode, ReasoningGoal,
    ReasoningConstraint
)
from .causal_analyzer import CausalAnalyzer
from .uncertainty_handler import UncertaintyHandler  
from .context_manager import ContextManager
from trm_api.eventbus.system_event_bus import publish_event, EventType


class AdvancedReasoningEngine:
    """
    Advanced Reasoning Engine for intelligent agent decision making
    
    Core capabilities:
    1. Multi-step logical reasoning with chain-of-thought
    2. Causal analysis and dependency tracking
    3. Uncertainty quantification and handling
    4. Context-aware reasoning with ontology integration
    5. Event-driven reasoning following TRM-OS philosophy
    """
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.logger = logging.getLogger(f"reasoning.{agent_id}")
        
        # Sub-components
        self.causal_analyzer = CausalAnalyzer()
        self.uncertainty_handler = UncertaintyHandler()
        self.context_manager = ContextManager()
        
        # Knowledge base for reasoning
        self.knowledge_base: Dict[str, KnowledgeNode] = {}
        
        # Active reasoning sessions
        self.active_sessions: Dict[str, ReasoningResult] = {}
        
        # Reasoning statistics
        self.reasoning_stats = {
            "total_sessions": 0,
            "successful_sessions": 0,
            "avg_confidence": 0.0,
            "avg_duration": 0.0
        }
    
    async def reason(
        self,
        goal: ReasoningGoal,
        context: ReasoningContext,
        constraints: Optional[List[ReasoningConstraint]] = None
    ) -> ReasoningResult:
        """
        Main reasoning entry point
        
        Args:
            goal: What we want to achieve through reasoning
            context: Current situation and available information
            constraints: Limitations and boundaries for reasoning
            
        Returns:
            ReasoningResult with conclusions, recommendations, and audit trail
        """
        session_id = str(uuid4())
        self.logger.info(f"Starting reasoning session {session_id} for goal: {goal.description}")
        
        # Initialize reasoning result
        result = ReasoningResult(
            result_id=session_id,
            reasoning_type=self._determine_reasoning_type(goal),
            context=context
        )
        
        self.active_sessions[session_id] = result
        
        try:
            # Step 1: Context Analysis and Preparation
            await self._prepare_reasoning_context(result, constraints or [])
            
            # Step 2: Multi-step reasoning execution
            await self._execute_reasoning_chain(result, goal)
            
            # Step 3: Causal analysis if needed
            if goal.goal_type in ["explanation", "analysis"]:
                await self._perform_causal_analysis(result)
            
            # Step 4: Uncertainty assessment
            await self._assess_uncertainty(result)
            
            # Step 5: Generate conclusions and recommendations
            await self._generate_conclusions(result, goal)
            
            # Step 6: Create events following TRM-OS philosophy
            await self._create_reasoning_events(result)
            
            result.finalize(success=True)
            self.logger.info(f"Reasoning session {session_id} completed successfully")
            
        except Exception as e:
            self.logger.error(f"Reasoning session {session_id} failed: {str(e)}")
            result.finalize(success=False, error=str(e))
            
            # Create error event
            try:
                # Ensure entity_id is a valid string for error events
                error_entity_id = None
                if hasattr(context, 'tension_id') and context.tension_id:
                    error_entity_id = str(context.tension_id)
                elif hasattr(context, 'agent_id') and context.agent_id:
                    error_entity_id = str(context.agent_id)
                else:
                    error_entity_id = session_id  # Use session ID as fallback
                    
                await publish_event(
                    event_type=EventType.AGENT_ERROR,
                    source_agent_id=self.agent_id,
                    entity_id=error_entity_id,
                    entity_type="reasoning_session",
                    data={
                        "session_id": session_id,
                        "error": str(e),
                        "goal": goal.description
                    }
                )
                
                # Add the error event to generated_events
                result.generated_events.append({
                    "event_type": "REASONING_ERROR",
                    "data": {
                        "session_id": session_id,
                        "error": str(e),
                        "goal": goal.description
                    }
                })
                
            except Exception:
                pass  # Don't fail on event creation error
        
        finally:
            # Update statistics
            self._update_reasoning_stats(result)
            
            # Clean up active session
            if session_id in self.active_sessions:
                del self.active_sessions[session_id]
        
        return result
    
    async def _prepare_reasoning_context(
        self, 
        result: ReasoningResult, 
        constraints: List[ReasoningConstraint]
    ) -> None:
        """Prepare and enrich reasoning context with relevant information"""
        
        step = ReasoningStep(
            step_type=ReasoningType.CONTEXTUAL,
            description="Preparing reasoning context with ontology data",
            input_data={"context_id": result.context.context_id},
            reasoning_logic="Load and analyze relevant ontology entities and historical events",
            output_data={},
            confidence=0.9,
            uncertainty_level=UncertaintyLevel.HIGH_CONFIDENCE,
            execution_time=datetime.now()
        )
        
        try:
            # Enrich context with ontology data
            enriched_context = await self.context_manager.enrich_context(result.context)
            result.context = enriched_context
            
                    # For initial implementation, use existing historical events
        # In full implementation, this would load from event repository
            
            # Apply constraints
            for constraint in constraints:
                await self._apply_constraint(result.context, constraint)
            
            step.output_data = {
                "entities_loaded": len(result.context.related_entities),
                "events_loaded": len(result.context.historical_events),
                "constraints_applied": len(constraints)
            }
            step.confidence = 0.95
            
        except Exception as e:
            step.confidence = 0.3
            step.uncertainty_level = UncertaintyLevel.UNCERTAIN
            step.output_data = {"error": str(e)}
            result.add_step(step)
            # Re-raise the exception to fail the entire reasoning session
            raise e
        
        result.add_step(step)
    
    async def _execute_reasoning_chain(
        self, 
        result: ReasoningResult, 
        goal: ReasoningGoal
    ) -> None:
        """Execute multi-step reasoning chain based on goal type"""
        
        if goal.goal_type == "explanation":
            await self._reasoning_chain_explanation(result, goal)
        elif goal.goal_type == "prediction":
            await self._reasoning_chain_prediction(result, goal)
        elif goal.goal_type == "recommendation":
            await self._reasoning_chain_recommendation(result, goal)
        elif goal.goal_type == "analysis":
            await self._reasoning_chain_analysis(result, goal)
        else:
            # Generic reasoning chain
            await self._reasoning_chain_generic(result, goal)
    
    async def _reasoning_chain_explanation(
        self, 
        result: ReasoningResult, 
        goal: ReasoningGoal
    ) -> None:
        """Reasoning chain for explanation goals"""
        
        # Step 1: Identify what needs explaining
        step1 = ReasoningStep(
            step_type=ReasoningType.DEDUCTIVE,
            description="Identify core phenomena to explain",
            input_data={"goal": goal.description},
            reasoning_logic="Analyze goal and context to identify key phenomena requiring explanation",
            output_data={},
            confidence=0.8,
            uncertainty_level=UncertaintyLevel.HIGH_CONFIDENCE,
            execution_time=datetime.now()
        )
        
        # Extract key entities and their states
        phenomena = []
        if result.context.tension_id:
            phenomena.append(f"tension_{result.context.tension_id}")
        if result.context.task_ids:
            phenomena.extend([f"task_{tid}" for tid in result.context.task_ids])
        
        step1.output_data = {"phenomena": phenomena}
        result.add_step(step1)
        
        # Step 2: Analyze causal relationships
        step2 = ReasoningStep(
            step_type=ReasoningType.CAUSAL,
            description="Analyze causal relationships between entities",
            input_data={"phenomena": phenomena},
            reasoning_logic="Use causal analysis to understand how entities relate and influence each other",
            output_data={},
            confidence=0.7,
            uncertainty_level=UncertaintyLevel.MODERATE,
            execution_time=datetime.now(),
            dependencies=[step1.step_id]
        )
        
        # Perform causal analysis
        if len(phenomena) > 1:
            causal_chains = await self.causal_analyzer.analyze_relationships(
                phenomena, result.context
            )
            result.causal_chains.extend(causal_chains)
            step2.output_data = {"causal_chains": len(causal_chains)}
            step2.confidence = 0.85
        else:
            step2.output_data = {"causal_chains": 0}
            step2.confidence = 0.6
        
        result.add_step(step2)
        
        # Step 3: Synthesize explanation
        step3 = ReasoningStep(
            step_type=ReasoningType.INDUCTIVE,
            description="Synthesize comprehensive explanation",
            input_data={"causal_chains": len(result.causal_chains)},
            reasoning_logic="Combine causal analysis with context to generate coherent explanation",
            output_data={},
            confidence=0.8,
            uncertainty_level=UncertaintyLevel.HIGH_CONFIDENCE,
            execution_time=datetime.now(),
            dependencies=[step2.step_id]
        )
        
        explanation = self._synthesize_explanation(result.causal_chains, result.context)
        step3.output_data = {"explanation": explanation}
        result.add_step(step3)
    
    async def _reasoning_chain_recommendation(
        self, 
        result: ReasoningResult, 
        goal: ReasoningGoal
    ) -> None:
        """Reasoning chain for recommendation goals"""
        
        # Step 1: Analyze current situation
        step1 = ReasoningStep(
            step_type=ReasoningType.CONTEXTUAL,
            description="Analyze current situation and constraints",
            input_data={"context": result.context.context_id},
            reasoning_logic="Evaluate current state, available resources, and constraints",
            output_data={},
            confidence=0.85,
            uncertainty_level=UncertaintyLevel.HIGH_CONFIDENCE,
            execution_time=datetime.now()
        )
        
        situation_analysis = await self._analyze_current_situation(result.context)
        step1.output_data = situation_analysis
        result.add_step(step1)
        
        # Step 2: Generate possible actions
        step2 = ReasoningStep(
            step_type=ReasoningType.INDUCTIVE,
            description="Generate possible actions and solutions",
            input_data=situation_analysis,
            reasoning_logic="Based on situation analysis, generate viable action alternatives",
            output_data={},
            confidence=0.75,
            uncertainty_level=UncertaintyLevel.MODERATE,
            execution_time=datetime.now(),
            dependencies=[step1.step_id]
        )
        
        possible_actions = await self._generate_possible_actions(result.context, goal)
        step2.output_data = {"actions": possible_actions}
        result.add_step(step2)
        
        # Step 3: Evaluate and rank recommendations
        step3 = ReasoningStep(
            step_type=ReasoningType.PROBABILISTIC,
            description="Evaluate and rank action alternatives",
            input_data={"actions": possible_actions},
            reasoning_logic="Score actions based on feasibility, impact, and success probability",
            output_data={},
            confidence=0.8,
            uncertainty_level=UncertaintyLevel.HIGH_CONFIDENCE,
            execution_time=datetime.now(),
            dependencies=[step2.step_id]
        )
        
        ranked_recommendations = await self._evaluate_and_rank_actions(
            possible_actions, result.context
        )
        step3.output_data = {"recommendations": ranked_recommendations}
        
        # Set the recommendations directly on the result
        result.recommendations = ranked_recommendations
        
        result.add_step(step3)
    
    async def _perform_causal_analysis(self, result: ReasoningResult) -> None:
        """Perform detailed causal analysis"""
        
        if not result.context.historical_events:
            return
        
        step = ReasoningStep(
            step_type=ReasoningType.CAUSAL,
            description="Perform detailed causal analysis of historical events",
            input_data={"events": len(result.context.historical_events)},
            reasoning_logic="Analyze temporal patterns and causal relationships in event history",
            output_data={},
            confidence=0.7,
            uncertainty_level=UncertaintyLevel.MODERATE,
            execution_time=datetime.now()
        )
        
        try:
            causal_chains = await self.causal_analyzer.analyze_event_sequences(
                result.context.historical_events
            )
            result.causal_chains.extend(causal_chains)
            
            step.output_data = {"causal_chains_found": len(causal_chains)}
            step.confidence = 0.8
            
        except Exception as e:
            step.output_data = {"error": str(e)}
            step.confidence = 0.3
        
        result.add_step(step)
    
    async def _assess_uncertainty(self, result: ReasoningResult) -> None:
        """Assess and handle uncertainty in reasoning results"""
        
        step = ReasoningStep(
            step_type=ReasoningType.PROBABILISTIC,
            description="Assess uncertainty in reasoning conclusions",
            input_data={"steps": len(result.steps)},
            reasoning_logic="Analyze confidence levels and identify uncertainty sources",
            output_data={},
            confidence=0.9,
            uncertainty_level=UncertaintyLevel.HIGH_CONFIDENCE,
            execution_time=datetime.now()
        )
        
        uncertainty_assessment = await self.uncertainty_handler.assess_uncertainty(result)
        
        step.output_data = {
            "overall_uncertainty": uncertainty_assessment["overall_level"],
            "uncertainty_sources": uncertainty_assessment["sources"],
            "confidence_variance": uncertainty_assessment["confidence_variance"]
        }
        
        result.add_step(step)
    
    async def _generate_conclusions(
        self, 
        result: ReasoningResult, 
        goal: ReasoningGoal
    ) -> None:
        """Generate final conclusions and recommendations"""
        
        step = ReasoningStep(
            step_type=ReasoningType.DEDUCTIVE,
            description="Generate final conclusions and actionable recommendations",
            input_data={"goal_type": goal.goal_type},
            reasoning_logic="Synthesize reasoning steps into coherent conclusions and actions",
            output_data={},
            confidence=0.85,
            uncertainty_level=UncertaintyLevel.HIGH_CONFIDENCE,
            execution_time=datetime.now()
        )
        
        # Generate conclusions based on reasoning steps
        conclusions = []
        recommendations = []
        
        for reasoning_step in result.steps:
            if reasoning_step.confidence >= 0.7:
                if "explanation" in reasoning_step.output_data:
                    conclusions.append(reasoning_step.output_data["explanation"])
                if "recommendations" in reasoning_step.output_data:
                    recommendations.extend(reasoning_step.output_data["recommendations"])
        
        # Add causal insights
        for chain in result.causal_chains:
            if chain.confidence >= 0.6:
                conclusions.append(
                    f"Causal relationship identified: {chain.root_cause} → {chain.final_effect} "
                    f"(confidence: {chain.confidence:.2f})"
                )
        
        # Set the results - only update if not already set by specific reasoning chains
        if not result.conclusions:
            result.conclusions = conclusions
        if not result.recommendations:
            result.recommendations = recommendations
        
        step.output_data = {
            "conclusions_generated": len(result.conclusions),
            "recommendations_generated": len(result.recommendations)
        }
        
        result.add_step(step)
    
    async def _create_reasoning_events(self, result: ReasoningResult) -> None:
        """Create events following TRM-OS Recognition → Event → WIN philosophy"""
        
        # Create reasoning completed event
        reasoning_type_value = result.reasoning_type if hasattr(result.reasoning_type, 'value') else str(result.reasoning_type)
        event_data = {
            "session_id": result.result_id,
            "reasoning_type": reasoning_type_value,
            "confidence": result.overall_confidence,
            "conclusions_count": len(result.conclusions),
            "recommendations_count": len(result.recommendations),
            "duration_seconds": result.duration_seconds()
        }
        
        # Ensure entity_id is a valid string
        entity_id = None
        if hasattr(result.context, 'tension_id') and result.context.tension_id:
            entity_id = str(result.context.tension_id)
        elif hasattr(result.context, 'agent_id') and result.context.agent_id:
            entity_id = str(result.context.agent_id)
        else:
            entity_id = result.result_id  # Use session ID as fallback
            
        await publish_event(
            event_type=EventType.KNOWLEDGE_CREATED,
            source_agent_id=self.agent_id,
            entity_id=entity_id,
            entity_type="reasoning_result",
            data=event_data
        )
        
        result.generated_events.append({
            "event_type": "REASONING_COMPLETED",
            "data": event_data
        })
        
        # Create specific events for high-confidence recommendations
        # But don't let these events fail the reasoning session
        for i, recommendation in enumerate(result.recommendations):
            if isinstance(recommendation, dict) and recommendation.get("confidence", 0) >= 0.8:
                try:
                    # Ensure valid entity_id for recommendation events
                    rec_entity_id = entity_id
                    if hasattr(result.context, 'tension_id') and result.context.tension_id:
                        rec_entity_id = str(result.context.tension_id)
                        
                    await publish_event(
                        event_type=EventType.AGENT_ACTION_SUGGESTED,
                        source_agent_id=self.agent_id,
                        entity_id=rec_entity_id,
                        entity_type="recommendation",
                        data={
                            "recommendation_id": f"{result.result_id}_{i}",
                            "action": recommendation.get("action"),
                            "confidence": recommendation.get("confidence"),
                            "priority": recommendation.get("priority", 5)
                        }
                    )
                except Exception as e:
                    # Log but don't fail the session
                    self.logger.warning(f"Failed to create recommendation event: {str(e)}")
                    pass
    
    def _determine_reasoning_type(self, goal: ReasoningGoal) -> str:
        """Determine primary reasoning type based on goal"""
        
        goal_type_mapping = {
            "explanation": ReasoningType.CAUSAL.value,
            "prediction": ReasoningType.PROBABILISTIC.value,
            "recommendation": ReasoningType.INDUCTIVE.value,
            "analysis": ReasoningType.DEDUCTIVE.value
        }
        
        return goal_type_mapping.get(goal.goal_type, ReasoningType.CONTEXTUAL.value)
    
    async def _apply_constraint(
        self, 
        context: ReasoningContext, 
        constraint: ReasoningConstraint
    ) -> None:
        """Apply reasoning constraint to context"""
        
        if constraint.constraint_type == "time":
            # Apply time constraints
            max_duration = constraint.parameters.get("max_duration_minutes", 60)
            context.time_window = (
                datetime.now(),
                datetime.now() + timedelta(minutes=max_duration)
            )
        
        elif constraint.constraint_type == "resource":
            # Apply resource constraints
            max_complexity = constraint.parameters.get("max_complexity", 0.8)
            context.complexity_score = min(context.complexity_score, max_complexity)
    
    def _synthesize_explanation(
        self, 
        causal_chains: List[CausalChain], 
        context: ReasoningContext
    ) -> str:
        """Synthesize explanation from causal analysis"""
        
        if not causal_chains:
            return "No clear causal relationships identified in the available data."
        
        # Find the strongest causal chain
        strongest_chain = max(causal_chains, key=lambda c: c.confidence * c.strength)
        
        explanation = f"The primary causal relationship shows that {strongest_chain.root_cause} "
        
        if strongest_chain.intermediate_causes:
            explanation += f"leads to {' which leads to '.join(strongest_chain.intermediate_causes)}, "
        
        explanation += f"ultimately resulting in {strongest_chain.final_effect}. "
        explanation += f"This relationship has a confidence level of {strongest_chain.confidence:.2f} "
        explanation += f"and causal strength of {strongest_chain.strength:.2f}."
        
        return explanation
    
    async def _analyze_current_situation(self, context: ReasoningContext) -> Dict[str, Any]:
        """Analyze current situation for recommendation generation"""
        
        situation = {
            "entity_states": {},
            "available_resources": [],
            "constraints": [],
            "opportunities": []
        }
        
        # Analyze tension state if present
        if context.tension_id:
            situation["entity_states"]["tension"] = {
                "id": context.tension_id,
                "status": context.current_state.get("tension_status", "unknown"),
                "priority": context.priority_level
            }
        
        # Analyze task states
        for task_id in context.task_ids:
            task_status = context.current_state.get(f"task_{task_id}_status", "unknown")
            situation["entity_states"][f"task_{task_id}"] = {
                "status": task_status,
                "id": task_id
            }
        
        return situation
    
    async def _generate_possible_actions(
        self, 
        context: ReasoningContext, 
        goal: ReasoningGoal
    ) -> List[Dict[str, Any]]:
        """Generate possible actions based on context and goal"""
        
        actions = []
        
        # Generate actions based on tension state
        if context.tension_id:
            tension_status = context.current_state.get("tension_status", "open")
            
            if tension_status == "open":
                actions.extend([
                    {
                        "action": "create_analysis_task",
                        "description": "Create task to analyze tension in detail",
                        "feasibility": 0.9,
                        "impact": 0.7,
                        "resource_required": "low"
                    },
                    {
                        "action": "assign_specialist_agent",
                        "description": "Assign specialist agent to handle tension",
                        "feasibility": 0.8,
                        "impact": 0.8,
                        "resource_required": "medium"
                    },
                    {
                        "action": "escalate_to_human",
                        "description": "Escalate tension to human oversight",
                        "feasibility": 1.0,
                        "impact": 0.9,
                        "resource_required": "high"
                    }
                ])
        
        # Generate actions based on task states
        for task_id in context.task_ids:
            task_status = context.current_state.get(f"task_{task_id}_status", "todo")
            
            if task_status == "todo":
                actions.append({
                    "action": f"prioritize_task_{task_id}",
                    "description": f"Increase priority of task {task_id}",
                    "feasibility": 0.9,
                    "impact": 0.6,
                    "resource_required": "low"
                })
        
        return actions
    
    async def _evaluate_and_rank_actions(
        self, 
        actions: List[Dict[str, Any]], 
        context: ReasoningContext
    ) -> List[Dict[str, Any]]:
        """Evaluate and rank actions by priority"""
        
        ranked_actions = []
        
        for action in actions:
            # Calculate score based on feasibility, impact, and resource efficiency
            feasibility = action.get("feasibility", 0.5)
            impact = action.get("impact", 0.5)
            
            # Resource efficiency (inverse of resource requirement)
            resource_map = {"low": 0.9, "medium": 0.6, "high": 0.3}
            resource_efficiency = resource_map.get(action.get("resource_required", "medium"), 0.5)
            
            # Weight factors
            score = (feasibility * 0.3) + (impact * 0.5) + (resource_efficiency * 0.2)
            
            # Adjust based on context priority
            if context.priority_level >= 8:  # High priority
                score += 0.1
            
            ranked_action = action.copy()
            ranked_action["score"] = score
            ranked_action["confidence"] = min(0.95, feasibility * impact + 0.1)
            ranked_actions.append(ranked_action)
        
        # Sort by score descending
        ranked_actions.sort(key=lambda x: x["score"], reverse=True)
        
        return ranked_actions
    
    async def _reasoning_chain_prediction(
        self, 
        result: ReasoningResult, 
        goal: ReasoningGoal
    ) -> None:
        """Reasoning chain for prediction goals"""
        
        # Step 1: Analyze historical patterns
        step1 = ReasoningStep(
            step_type=ReasoningType.TEMPORAL,
            description="Analyze historical patterns and trends",
            input_data={"events": len(result.context.historical_events)},
            reasoning_logic="Identify patterns in historical events to predict future outcomes",
            output_data={},
            confidence=0.7,
            uncertainty_level=UncertaintyLevel.MODERATE,
            execution_time=datetime.now()
        )
        
        patterns = await self._analyze_temporal_patterns(result.context.historical_events)
        step1.output_data = {"patterns_found": len(patterns)}
        result.add_step(step1)
        
        # Step 2: Generate predictions
        step2 = ReasoningStep(
            step_type=ReasoningType.PROBABILISTIC,
            description="Generate probabilistic predictions",
            input_data={"patterns": len(patterns)},
            reasoning_logic="Use identified patterns to generate future state predictions",
            output_data={},
            confidence=0.6,
            uncertainty_level=UncertaintyLevel.MODERATE,
            execution_time=datetime.now(),
            dependencies=[step1.step_id]
        )
        
        predictions = await self._generate_predictions(patterns, result.context)
        step2.output_data = {"predictions": predictions}
        result.predictions = predictions
        result.add_step(step2)
    
    async def _reasoning_chain_analysis(
        self, 
        result: ReasoningResult, 
        goal: ReasoningGoal
    ) -> None:
        """Reasoning chain for analysis goals"""
        
        # Step 1: Data aggregation and preparation
        step1 = ReasoningStep(
            step_type=ReasoningType.CONTEXTUAL,
            description="Aggregate and prepare data for analysis",
            input_data={"context": result.context.context_id},
            reasoning_logic="Collect and structure all relevant data for comprehensive analysis",
            output_data={},
            confidence=0.9,
            uncertainty_level=UncertaintyLevel.HIGH_CONFIDENCE,
            execution_time=datetime.now()
        )
        
        aggregated_data = await self._aggregate_analysis_data(result.context)
        step1.output_data = aggregated_data
        result.add_step(step1)
        
        # Step 2: Statistical analysis
        step2 = ReasoningStep(
            step_type=ReasoningType.DEDUCTIVE,
            description="Perform statistical analysis on aggregated data",
            input_data=aggregated_data,
            reasoning_logic="Apply statistical methods to identify significant patterns and correlations",
            output_data={},
            confidence=0.8,
            uncertainty_level=UncertaintyLevel.HIGH_CONFIDENCE,
            execution_time=datetime.now(),
            dependencies=[step1.step_id]
        )
        
        analysis_results = await self._perform_statistical_analysis(aggregated_data)
        step2.output_data = analysis_results
        result.add_step(step2)
    
    async def _reasoning_chain_generic(
        self, 
        result: ReasoningResult, 
        goal: ReasoningGoal
    ) -> None:
        """Generic reasoning chain for unknown goal types"""
        
        step = ReasoningStep(
            step_type=ReasoningType.CONTEXTUAL,
            description="Generic reasoning approach",
            input_data={"goal": goal.description},
            reasoning_logic="Apply general reasoning principles to understand and address the goal",
            output_data={},
            confidence=0.6,
            uncertainty_level=UncertaintyLevel.MODERATE,
            execution_time=datetime.now()
        )
        
        # Basic analysis of available information
        analysis = {
            "context_entities": len(result.context.related_entities),
            "historical_events": len(result.context.historical_events),
            "goal_complexity": len(goal.description.split()) / 20  # Simple complexity measure
        }
        
        step.output_data = analysis
        result.add_step(step)
    
    async def _analyze_temporal_patterns(
        self, 
        events: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Analyze temporal patterns in historical events"""
        
        patterns = []
        
        if len(events) < 2:
            return patterns
        
        # Sort events by timestamp
        sorted_events = sorted(events, key=lambda e: e.get("timestamp", datetime.min))
        
        # Find recurring event types
        event_types = {}
        for event in sorted_events:
            event_type = event.get("event_type", "unknown")
            if event_type not in event_types:
                event_types[event_type] = []
            event_types[event_type].append(event)
        
        for event_type, type_events in event_types.items():
            if len(type_events) >= 2:
                patterns.append({
                    "type": "recurring_event",
                    "event_type": event_type,
                    "frequency": len(type_events),
                    "pattern_strength": min(1.0, len(type_events) / len(events))
                })
        
        return patterns
    
    async def _generate_predictions(
        self, 
        patterns: List[Dict[str, Any]], 
        context: ReasoningContext
    ) -> List[Dict[str, Any]]:
        """Generate predictions based on identified patterns"""
        
        predictions = []
        
        # Generate predictions from patterns
        for pattern in patterns:
            if pattern["type"] == "recurring_event":
                prediction = {
                    "prediction_type": "event_recurrence",
                    "predicted_event": pattern["event_type"],
                    "probability": pattern["pattern_strength"],
                    "confidence": pattern["pattern_strength"] * 0.8,
                    "time_horizon": "short_term"
                }
                predictions.append(prediction)
        
        # If no pattern-based predictions, generate contextual predictions
        if not predictions and context.historical_events:
            # Generate predictions based on current state
            if context.tension_id:
                tension_status = context.current_state.get("tension_status", "open")
                if tension_status == "open":
                    predictions.append({
                        "prediction_type": "tension_resolution",
                        "predicted_outcome": "tension_will_be_resolved",
                        "probability": 0.7,
                        "confidence": 0.6,
                        "time_horizon": "medium_term",
                        "factors": ["active_tasks", "agent_assignment"]
                    })
            
            # Generate task-based predictions
            for task_id in context.task_ids:
                task_status = context.current_state.get(f"task_{task_id}_status", "unknown")
                if task_status == "in_progress":
                    predictions.append({
                        "prediction_type": "task_completion",
                        "predicted_outcome": f"task_{task_id}_will_complete",
                        "probability": 0.8,
                        "confidence": 0.7,
                        "time_horizon": "short_term",
                        "factors": ["current_progress", "resource_availability"]
                    })
        
        return predictions
    
    async def _aggregate_analysis_data(
        self, 
        context: ReasoningContext
    ) -> Dict[str, Any]:
        """Aggregate data for analysis"""
        
        return {
            "entity_count": len(context.related_entities),
            "event_count": len(context.historical_events),
            "time_span_days": self._calculate_time_span(context.historical_events),
            "complexity_indicators": {
                "entity_diversity": len(context.related_entities.keys()),
                "event_diversity": len(set(e.get("event_type") for e in context.historical_events))
            }
        }
    
    async def _perform_statistical_analysis(
        self, 
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Perform statistical analysis on aggregated data"""
        
        return {
            "summary_stats": {
                "total_entities": data.get("entity_count", 0),
                "total_events": data.get("event_count", 0),
                "analysis_period_days": data.get("time_span_days", 0)
            },
            "complexity_score": (
                data.get("complexity_indicators", {}).get("entity_diversity", 0) +
                data.get("complexity_indicators", {}).get("event_diversity", 0)
            ) / 2,
            "data_quality": "high" if data.get("event_count", 0) > 10 else "low"
        }
    
    def _calculate_time_span(self, events: List[Dict[str, Any]]) -> int:
        """Calculate time span of events in days"""
        
        if len(events) < 2:
            return 0
        
        timestamps = [
            event.get("timestamp", datetime.min) 
            for event in events 
            if "timestamp" in event
        ]
        
        if not timestamps:
            return 0
        
        earliest = min(timestamps)
        latest = max(timestamps)
        
        return (latest - earliest).days
    
    def _update_reasoning_stats(self, result: ReasoningResult) -> None:
        """Update reasoning engine statistics"""
        
        self.reasoning_stats["total_sessions"] += 1
        
        if result.success:
            self.reasoning_stats["successful_sessions"] += 1
        
        # Update average confidence
        total_confidence = (
            self.reasoning_stats["avg_confidence"] * (self.reasoning_stats["total_sessions"] - 1) +
            result.overall_confidence
        )
        self.reasoning_stats["avg_confidence"] = total_confidence / self.reasoning_stats["total_sessions"]
        
        # Update average duration
        duration = result.duration_seconds()
        total_duration = (
            self.reasoning_stats["avg_duration"] * (self.reasoning_stats["total_sessions"] - 1) +
            duration
        )
        self.reasoning_stats["avg_duration"] = total_duration / self.reasoning_stats["total_sessions"]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get reasoning engine performance statistics"""
        return self.reasoning_stats.copy()
    
    async def add_knowledge(self, knowledge: KnowledgeNode) -> None:
        """Add knowledge to the reasoning engine's knowledge base"""
        self.knowledge_base[knowledge.node_id] = knowledge
        self.logger.info(f"Added knowledge node: {knowledge.node_type} - {knowledge.content[:50]}...")
    
    async def query_knowledge(
        self, 
        query: str, 
        node_types: Optional[List[str]] = None
    ) -> List[KnowledgeNode]:
        """Query knowledge base for relevant information"""
        
        results = []
        query_lower = query.lower()
        
        for knowledge in self.knowledge_base.values():
            # Filter by node type if specified
            if node_types and knowledge.node_type not in node_types:
                continue
            
            # Simple text matching (can be enhanced with semantic search)
            if query_lower in knowledge.content.lower():
                results.append(knowledge)
        
        # Sort by confidence and relevance
        results.sort(key=lambda k: k.confidence, reverse=True)
        
        return results 