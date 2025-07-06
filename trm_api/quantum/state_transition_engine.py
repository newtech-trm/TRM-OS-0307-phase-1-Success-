"""
State Transition Engine - ML-Enhanced Quantum State Transitions
Quản lý transitions giữa quantum states với machine learning optimization
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import numpy as np
from uuid import uuid4

from ..learning.adaptive_learning_system import AdaptiveLearningSystem
from ..learning.learning_types import LearningExperience, ExperienceType
from ..eventbus.system_event_bus import publish_event
from ..models.event import EventType
from .quantum_types import (
    QuantumState, QuantumSystem, StateTransition, QuantumStateType,
    ProbabilityDistribution
)


class TransitionTriggerType(Enum):
    """Types of transition triggers"""
    COHERENCE_THRESHOLD = "coherence_threshold"
    PERFORMANCE_METRIC = "performance_metric"
    TIME_BASED = "time_based"
    EVENT_DRIVEN = "event_driven"
    ML_PREDICTED = "ml_predicted"
    MANUAL = "manual"


@dataclass
class TransitionCondition:
    """Condition for state transition"""
    condition_id: str
    trigger_type: TransitionTriggerType
    threshold_value: float
    metric_name: str
    operator: str = "greater_than"  # greater_than, less_than, equals
    weight: float = 1.0
    
    def evaluate(self, current_metrics: Dict[str, Any]) -> bool:
        """Evaluate if condition is met"""
        
        if self.metric_name not in current_metrics:
            return False
        
        current_value = current_metrics[self.metric_name]
        
        if self.operator == "greater_than":
            return current_value > self.threshold_value
        elif self.operator == "less_than":
            return current_value < self.threshold_value
        elif self.operator == "equals":
            return abs(current_value - self.threshold_value) < 0.01
        
        return False


@dataclass
class TransitionResult:
    """Result of state transition"""
    transition_id: str
    from_state_id: str
    to_state_id: str
    success: bool
    transition_time: float
    confidence: float
    conditions_met: List[str]
    metrics_before: Dict[str, Any]
    metrics_after: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)


class StateTransitionEngine:
    """
    ML-Enhanced State Transition Engine
    Quản lý transitions giữa quantum states với intelligent decision making
    """
    
    def __init__(self, learning_system: AdaptiveLearningSystem):
        self.learning_system = learning_system
        self.logger = logging.getLogger(__name__)
        
        # Transition management
        self.transition_conditions: Dict[str, List[TransitionCondition]] = {}
        self.transition_history: List[TransitionResult] = []
        self.active_transitions: Dict[str, Any] = {}
        
        # ML models for transition prediction
        self.transition_success_predictor = None
        self.transition_timing_predictor = None
        
        # Configuration
        self.max_concurrent_transitions = 5
        self.transition_timeout = 30.0  # seconds
        self.prediction_confidence_threshold = 0.7
        
        # Statistics
        self.transition_stats = {
            "total_transitions": 0,
            "successful_transitions": 0,
            "failed_transitions": 0,
            "average_transition_time": 0.0,
            "prediction_accuracy": 0.0
        }
        
        self.logger.info("StateTransitionEngine initialized")
    
    async def initialize(self) -> None:
        """Initialize transition engine"""
        
        try:
            # Initialize ML models
            await self._initialize_ml_models()
            
            # Setup default transition conditions
            await self._setup_default_conditions()
            
            self.logger.info("StateTransitionEngine initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize StateTransitionEngine: {e}")
            raise
    
    async def evaluate_transition_conditions(
        self,
        quantum_system: QuantumSystem,
        current_metrics: Dict[str, Any]
    ) -> List[Tuple[str, str, float]]:
        """
        Evaluate transition conditions và return possible transitions
        Returns: List of (from_state_id, to_state_id, confidence)
        """
        
        possible_transitions = []
        
        try:
            # Evaluate all transitions
            for transition_id, transition in quantum_system.state_transitions.items():
                
                # Get conditions for this transition
                conditions = self.transition_conditions.get(transition_id, [])
                
                if not conditions:
                    # Use default transition probability
                    confidence = transition.transition_probability
                else:
                    # Evaluate conditions
                    met_conditions = []
                    total_weight = 0.0
                    met_weight = 0.0
                    
                    for condition in conditions:
                        total_weight += condition.weight
                        if condition.evaluate(current_metrics):
                            met_conditions.append(condition.condition_id)
                            met_weight += condition.weight
                    
                    # Calculate confidence based on met conditions
                    if total_weight > 0:
                        confidence = (met_weight / total_weight) * transition.transition_probability
                    else:
                        confidence = transition.transition_probability
                
                # Apply ML prediction enhancement
                if self.transition_success_predictor:
                    ml_confidence = await self._predict_transition_success(
                        transition, current_metrics
                    )
                    confidence = (confidence + ml_confidence) / 2
                
                # Add to possible transitions if confidence is high enough
                if confidence >= self.prediction_confidence_threshold:
                    possible_transitions.append((
                        transition.from_state,
                        transition.to_state,
                        confidence
                    ))
            
            # Sort by confidence
            possible_transitions.sort(key=lambda x: x[2], reverse=True)
            
            return possible_transitions
            
        except Exception as e:
            self.logger.error(f"Failed to evaluate transition conditions: {e}")
            return []
    
    async def execute_transition(
        self,
        quantum_system: QuantumSystem,
        from_state_id: str,
        to_state_id: str,
        force: bool = False
    ) -> TransitionResult:
        """Execute state transition"""
        
        if len(self.active_transitions) >= self.max_concurrent_transitions:
            raise ValueError("Maximum concurrent transitions reached")
        
        transition_id = str(uuid4())
        start_time = datetime.now()
        
        try:
            # Find transition
            target_transition = None
            for trans_id, transition in quantum_system.state_transitions.items():
                if transition.from_state == from_state_id and transition.to_state == to_state_id:
                    target_transition = transition
                    break
            
            if not target_transition and not force:
                raise ValueError(f"No transition found from {from_state_id} to {to_state_id}")
            
            # Mark as active
            self.active_transitions[transition_id] = {
                "from_state": from_state_id,
                "to_state": to_state_id,
                "start_time": start_time,
                "status": "executing"
            }
            
            # Get current metrics
            metrics_before = await self._get_current_metrics(quantum_system)
            
            # Execute transition
            success = await self._perform_transition(
                quantum_system, from_state_id, to_state_id, target_transition
            )
            
            # Get metrics after transition
            metrics_after = await self._get_current_metrics(quantum_system)
            
            # Calculate transition time
            transition_time = (datetime.now() - start_time).total_seconds()
            
            # Create result
            result = TransitionResult(
                transition_id=transition_id,
                from_state_id=from_state_id,
                to_state_id=to_state_id,
                success=success,
                transition_time=transition_time,
                confidence=target_transition.transition_probability if target_transition else 0.5,
                conditions_met=[],
                metrics_before=metrics_before,
                metrics_after=metrics_after
            )
            
            # Store result
            self.transition_history.append(result)
            
            # Update statistics
            self._update_transition_stats(result)
            
            # Learn from transition
            await self._learn_from_transition(result)
            
            # Remove from active transitions
            del self.active_transitions[transition_id]
            
            # Record event
            await publish_event(
                event_type=EventType.AGENT_ACTION_COMPLETED if success else EventType.AGENT_ACTION_FAILED,
                source_agent_id="state_transition_engine",
                entity_id=transition_id,
                entity_type="quantum_state_transition",
                data={
                    "from_state": from_state_id,
                    "to_state": to_state_id,
                    "success": success,
                    "transition_time": transition_time,
                    "confidence": result.confidence
                }
            )
            
            return result
            
        except Exception as e:
            # Clean up
            if transition_id in self.active_transitions:
                del self.active_transitions[transition_id]
            
            self.logger.error(f"Failed to execute transition: {e}")
            raise
    
    async def predict_optimal_transition_path(
        self,
        quantum_system: QuantumSystem,
        current_state_id: str,
        target_state_id: str,
        max_steps: int = 5
    ) -> List[Tuple[str, str, float]]:
        """Predict optimal transition path to target state"""
        
        try:
            # Use A* algorithm with ML-enhanced heuristics
            path = await self._find_optimal_path(
                quantum_system, current_state_id, target_state_id, max_steps
            )
            
            return path
            
        except Exception as e:
            self.logger.error(f"Failed to predict optimal transition path: {e}")
            return []
    
    async def add_transition_condition(
        self,
        transition_id: str,
        condition: TransitionCondition
    ) -> None:
        """Add condition for transition"""
        
        if transition_id not in self.transition_conditions:
            self.transition_conditions[transition_id] = []
        
        self.transition_conditions[transition_id].append(condition)
        
        self.logger.info(f"Added condition {condition.condition_id} for transition {transition_id}")
    
    async def remove_transition_condition(
        self,
        transition_id: str,
        condition_id: str
    ) -> bool:
        """Remove condition from transition"""
        
        if transition_id not in self.transition_conditions:
            return False
        
        conditions = self.transition_conditions[transition_id]
        for i, condition in enumerate(conditions):
            if condition.condition_id == condition_id:
                del conditions[i]
                self.logger.info(f"Removed condition {condition_id} from transition {transition_id}")
                return True
        
        return False
    
    def get_transition_statistics(self) -> Dict[str, Any]:
        """Get transition statistics"""
        
        return {
            **self.transition_stats,
            "active_transitions": len(self.active_transitions),
            "total_conditions": sum(len(conditions) for conditions in self.transition_conditions.values()),
            "history_size": len(self.transition_history)
        }
    
    def get_transition_history(
        self,
        limit: int = 100,
        successful_only: bool = False
    ) -> List[TransitionResult]:
        """Get transition history"""
        
        history = self.transition_history
        
        if successful_only:
            history = [result for result in history if result.success]
        
        return history[-limit:]
    
    # Private methods
    
    async def _initialize_ml_models(self) -> None:
        """Initialize ML models for transition prediction"""
        
        # Placeholder for ML model initialization
        # Would use sklearn models in real implementation
        self.transition_success_predictor = "initialized"
        self.transition_timing_predictor = "initialized"
        
        self.logger.info("ML models initialized")
    
    async def _setup_default_conditions(self) -> None:
        """Setup default transition conditions"""
        
        # Default conditions based on common organizational metrics
        default_conditions = [
            TransitionCondition(
                condition_id="coherence_high",
                trigger_type=TransitionTriggerType.COHERENCE_THRESHOLD,
                threshold_value=0.8,
                metric_name="system_coherence",
                operator="greater_than",
                weight=1.0
            ),
            TransitionCondition(
                condition_id="performance_improvement",
                trigger_type=TransitionTriggerType.PERFORMANCE_METRIC,
                threshold_value=0.1,
                metric_name="performance_improvement",
                operator="greater_than",
                weight=0.8
            ),
            TransitionCondition(
                condition_id="learning_progress",
                trigger_type=TransitionTriggerType.PERFORMANCE_METRIC,
                threshold_value=0.5,
                metric_name="learning_progress",
                operator="greater_than",
                weight=0.6
            )
        ]
        
        # These would be applied to specific transitions
        # For now, store as default conditions
        self.default_conditions = default_conditions
        
        self.logger.info("Default transition conditions setup")
    
    async def _predict_transition_success(
        self,
        transition: StateTransition,
        current_metrics: Dict[str, Any]
    ) -> float:
        """Predict transition success probability using ML"""
        
        # Placeholder for ML prediction
        # Would use trained model to predict success probability
        
        # Simple heuristic for now
        base_prob = transition.transition_probability
        
        # Adjust based on metrics
        if current_metrics.get("system_coherence", 0) > 0.7:
            base_prob *= 1.2
        
        if current_metrics.get("learning_progress", 0) > 0.5:
            base_prob *= 1.1
        
        return min(1.0, base_prob)
    
    async def _perform_transition(
        self,
        quantum_system: QuantumSystem,
        from_state_id: str,
        to_state_id: str,
        transition: Optional[StateTransition]
    ) -> bool:
        """Perform actual state transition"""
        
        try:
            # Get states
            from_state = quantum_system.quantum_states.get(from_state_id)
            to_state = quantum_system.quantum_states.get(to_state_id)
            
            if not from_state or not to_state:
                return False
            
            # Transfer probability (simplified)
            probability_transfer = from_state.probability * 0.5
            
            # Update states
            from_state.probability = max(0.0, from_state.probability - probability_transfer)
            to_state.probability = min(1.0, to_state.probability + probability_transfer)
            
            # Update amplitudes
            from_state.amplitude = complex(np.sqrt(from_state.probability), 0.0)
            to_state.amplitude = complex(np.sqrt(to_state.probability), 0.0)
            
            # Update system coherence
            quantum_system.total_coherence = quantum_system.calculate_system_coherence()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to perform transition: {e}")
            return False
    
    async def _get_current_metrics(self, quantum_system: QuantumSystem) -> Dict[str, Any]:
        """Get current system metrics"""
        
        return {
            "system_coherence": quantum_system.calculate_system_coherence(),
            "total_states": len(quantum_system.quantum_states),
            "total_transitions": len(quantum_system.state_transitions),
            "entropy": quantum_system.system_entropy,
            "timestamp": datetime.now().isoformat()
        }
    
    async def _find_optimal_path(
        self,
        quantum_system: QuantumSystem,
        start_state: str,
        target_state: str,
        max_steps: int
    ) -> List[Tuple[str, str, float]]:
        """Find optimal transition path using A* algorithm"""
        
        # Simplified path finding
        # In real implementation, would use A* with ML-enhanced heuristics
        
        path = []
        current_state = start_state
        
        for step in range(max_steps):
            if current_state == target_state:
                break
            
            # Find best transition from current state
            best_transition = None
            best_confidence = 0.0
            
            for transition in quantum_system.state_transitions.values():
                if transition.from_state == current_state:
                    confidence = transition.transition_probability
                    if confidence > best_confidence:
                        best_confidence = confidence
                        best_transition = transition
            
            if best_transition:
                path.append((
                    best_transition.from_state,
                    best_transition.to_state,
                    best_confidence
                ))
                current_state = best_transition.to_state
            else:
                break
        
        return path
    
    def _update_transition_stats(self, result: TransitionResult) -> None:
        """Update transition statistics"""
        
        self.transition_stats["total_transitions"] += 1
        
        if result.success:
            self.transition_stats["successful_transitions"] += 1
        else:
            self.transition_stats["failed_transitions"] += 1
        
        # Update average transition time
        total_time = (self.transition_stats["average_transition_time"] * 
                     (self.transition_stats["total_transitions"] - 1) + 
                     result.transition_time)
        self.transition_stats["average_transition_time"] = total_time / self.transition_stats["total_transitions"]
        
        # Update prediction accuracy (simplified)
        if self.transition_stats["total_transitions"] > 0:
            self.transition_stats["prediction_accuracy"] = (
                self.transition_stats["successful_transitions"] / 
                self.transition_stats["total_transitions"]
            )
    
    async def _learn_from_transition(self, result: TransitionResult) -> None:
        """Learn from transition result"""
        
        try:
            # Create learning experience
            experience = LearningExperience(
                agent_id="state_transition_engine",
                experience_type=ExperienceType.STATE_TRANSITION,
                action_taken={
                    "action": "execute_transition",
                    "from_state": result.from_state_id,
                    "to_state": result.to_state_id,
                    "transition_time": result.transition_time
                },
                outcome={
                    "success": result.success,
                    "confidence": result.confidence,
                    "metrics_change": self._calculate_metrics_change(
                        result.metrics_before, result.metrics_after
                    )
                },
                success=result.success,
                confidence=result.confidence,
                context={
                    "conditions_met": result.conditions_met,
                    "transition_time": result.transition_time
                }
            )
            
            # Add to learning system
            await self.learning_system.learn_from_experience(experience)
            
        except Exception as e:
            self.logger.error(f"Failed to learn from transition: {e}")
    
    def _calculate_metrics_change(
        self,
        metrics_before: Dict[str, Any],
        metrics_after: Dict[str, Any]
    ) -> Dict[str, float]:
        """Calculate metrics change from transition"""
        
        changes = {}
        
        for key in metrics_before:
            if key in metrics_after and isinstance(metrics_before[key], (int, float)):
                before_val = metrics_before[key]
                after_val = metrics_after[key]
                
                if before_val != 0:
                    change = (after_val - before_val) / before_val
                else:
                    change = after_val
                
                changes[key] = change
        
        return changes 