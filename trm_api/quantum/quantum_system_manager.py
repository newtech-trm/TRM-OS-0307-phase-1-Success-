"""
Quantum System Manager - Main Orchestrator cho TRM-OS Quantum Intelligence
Tích hợp toàn bộ quantum capabilities với existing TRM-OS architecture
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
from ..learning.learning_types import LearningExperience, ExperienceType, MetricType
from ..eventbus.system_event_bus import publish_event
from .quantum_types import (
    QuantumState, QuantumSystem, StateTransition, WINProbability,
    QuantumStateType, WINCategory, ProbabilityDistribution
)
from .optimization_engine import QuantumOptimizationEngine, OptimizationObjective
from .state_detector import AdaptiveStateDetector


class QuantumSystemStatus(Enum):
    """Status của quantum system"""
    INITIALIZING = "initializing"
    ACTIVE = "active"
    OPTIMIZING = "optimizing"
    COHERENCE_DEGRADED = "coherence_degraded"
    MAINTENANCE = "maintenance"
    ERROR = "error"


@dataclass
class OrganizationalSignals:
    """Organizational signals cho quantum state detection"""
    tension_resolution_rate: float = 0.0
    project_success_rate: float = 0.0
    agent_performance_metrics: Dict[str, float] = field(default_factory=dict)
    resource_utilization: float = 0.0
    communication_effectiveness: float = 0.0
    learning_progress: float = 0.0
    adaptation_success_rate: float = 0.0
    system_coherence: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class QuantumSystemMetrics:
    """Comprehensive metrics cho quantum system"""
    system_coherence: float = 0.0
    win_probability: float = 0.0
    state_stability: float = 0.0
    transition_efficiency: float = 0.0
    optimization_effectiveness: float = 0.0
    learning_integration: float = 0.0
    prediction_accuracy: float = 0.0
    adaptation_speed: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "system_coherence": self.system_coherence,
            "win_probability": self.win_probability,
            "state_stability": self.state_stability,
            "transition_efficiency": self.transition_efficiency,
            "optimization_effectiveness": self.optimization_effectiveness,
            "learning_integration": self.learning_integration,
            "prediction_accuracy": self.prediction_accuracy,
            "adaptation_speed": self.adaptation_speed
        }


class QuantumSystemManager:
    """
    Main orchestrator cho TRM-OS Quantum Intelligence System
    Tích hợp tất cả quantum capabilities với existing architecture
    """
    
    def __init__(self, learning_system: AdaptiveLearningSystem):
        self.learning_system = learning_system
        self.logger = logging.getLogger(__name__)
        
        # Core components
        self.optimization_engine = QuantumOptimizationEngine(learning_system)
        self.state_detector = AdaptiveStateDetector(learning_system)
        
        # System state
        self.system_id = str(uuid4())
        self.status = QuantumSystemStatus.INITIALIZING
        self.quantum_systems: Dict[str, QuantumSystem] = {}
        self.active_optimizations: Dict[str, Any] = {}
        
        # Metrics và monitoring
        self.metrics_history: List[QuantumSystemMetrics] = []
        self.organizational_signals_history: List[OrganizationalSignals] = []
        
        # Configuration
        self.max_concurrent_optimizations = 3
        self.coherence_threshold = 0.5
        self.optimization_interval = 300  # 5 minutes
        self.metrics_collection_interval = 60  # 1 minute
        
        # Background tasks
        self.background_tasks: List[asyncio.Task] = []
        self.is_running = False
        
        self.logger.info(f"QuantumSystemManager initialized with ID: {self.system_id}")
    
    async def initialize(self) -> None:
        """Initialize quantum system manager"""
        try:
            self.logger.info("Initializing Quantum System Manager...")
            
            # Initialize components (state_detector doesn't need initialization)
            # await self.state_detector.initialize()  # Removed - not needed
            
            # Create default quantum system
            default_system = await self.create_quantum_system(
                name="TRM-OS-Primary",
                description="Primary quantum system for TRM-OS organizational intelligence"
            )
            
            # Start background processes
            await self.start_background_processes()
            
            self.status = QuantumSystemStatus.ACTIVE
            self.is_running = True
            
            # Record initialization event
            await publish_event(
                event_type="knowledge.created",
                source_agent_id=self.system_id,
                entity_id=self.system_id,
                entity_type="quantum_system_manager",
                data={
                    "status": self.status.value,
                    "default_system_id": default_system.system_id,
                    "components_initialized": ["state_detector", "optimization_engine"]
                }
            )
            
            self.logger.info("Quantum System Manager initialized successfully")
            
        except Exception as e:
            self.status = QuantumSystemStatus.ERROR
            self.logger.error(f"Failed to initialize Quantum System Manager: {e}")
            raise
    
    async def create_quantum_system(
        self,
        name: str,
        description: str = "",
        initial_states: List[QuantumState] = None
    ) -> QuantumSystem:
        """Create a new quantum system"""
        
        system_id = str(uuid4())
        
        # Create initial states if not provided
        if initial_states is None:
            initial_states = await self._create_default_states(system_id)
        
        # Create quantum system
        quantum_system = QuantumSystem(
            system_id=system_id,
            quantum_states={state.state_id: state for state in initial_states},
            state_transitions={},
            entanglement_network={}
        )
        
        # Add to managed systems
        self.quantum_systems[system_id] = quantum_system
        
        # Initialize state transitions
        await self._initialize_state_transitions(quantum_system)
        
        # Record creation event
        await publish_event(
            event_type="knowledge.created",
            source_agent_id=self.system_id,
            entity_id=system_id,
            entity_type="quantum_system",
            data={
                "name": name,
                "description": description,
                "state_count": len(initial_states),
                "system_coherence": quantum_system.calculate_system_coherence()
            }
        )
        
        self.logger.info(f"Created quantum system: {name} ({system_id})")
        
        return quantum_system
    
    async def detect_current_quantum_state(
        self,
        system_id: str,
        organizational_signals: OrganizationalSignals = None
    ) -> Optional[QuantumState]:
        """Detect current quantum state của organization"""
        
        if system_id not in self.quantum_systems:
            self.logger.error(f"Quantum system not found: {system_id}")
            return None
        
        try:
            quantum_system = self.quantum_systems[system_id]
            
            # Get organizational signals
            if organizational_signals is None:
                organizational_signals = await self._collect_organizational_signals()
            
            # Store signals history
            self.organizational_signals_history.append(organizational_signals)
            
            # Try ML detection first
            try:
                detected_state = await self.state_detector.detect_quantum_state(
                    organizational_signals.__dict__
                )
                
                # Update quantum system
                if detected_state and detected_state.state_id in quantum_system.quantum_states:
                    current_state = quantum_system.quantum_states[detected_state.state_id]
                    
                    # Learn from state detection
                    await self._learn_from_state_detection(
                        system_id, organizational_signals, detected_state
                    )
                    
                    return current_state
            except Exception as e:
                self.logger.warning(f"ML state detection failed: {e}")
            
            # Fallback: return first available state with highest probability
            if quantum_system.quantum_states:
                best_state = None
                best_probability = 0.0
                
                for state in quantum_system.quantum_states.values():
                    if state.probability > best_probability:
                        best_state = state
                        best_probability = state.probability
                
                if best_state:
                    return best_state
                else:
                    # Return first state as last resort
                    return list(quantum_system.quantum_states.values())[0]
            
            return None
            
        except Exception as e:
            self.logger.error(f"Failed to detect quantum state: {e}")
            return None
    
    async def optimize_quantum_system(
        self,
        system_id: str,
        objectives: List[OptimizationObjective] = None,
        method: str = "hybrid_ml_optimization"
    ) -> Dict[str, Any]:
        """Optimize quantum system cho maximum WIN probability"""
        
        if system_id not in self.quantum_systems:
            return {"error": "Quantum system not found"}
        
        if len(self.active_optimizations) >= self.max_concurrent_optimizations:
            return {"error": "Maximum concurrent optimizations reached"}
        
        try:
            quantum_system = self.quantum_systems[system_id]
            
            # Default objectives
            if objectives is None:
                objectives = [
                    OptimizationObjective(
                        objective_id=str(uuid4()),
                        name="Maximize System Coherence",
                        description="Maximize quantum system coherence",
                        weight=0.4
                    ),
                    OptimizationObjective(
                        objective_id=str(uuid4()),
                        name="Maximize WIN Probabilities",
                        description="Maximize WIN state probabilities",
                        weight=0.6
                    )
                ]
            
            # Start optimization
            optimization_id = str(uuid4())
            self.active_optimizations[optimization_id] = {
                "system_id": system_id,
                "start_time": datetime.now(),
                "status": "running",
                "method": method
            }
            
            # Perform optimization
            optimization_result = await self.optimization_engine.optimize_quantum_system(
                quantum_system, objectives, method
            )
            
            # Update system với optimized states
            if optimization_result.optimal_states:
                for state in optimization_result.optimal_states:
                    quantum_system.quantum_states[state.state_id] = state
            
            # Update optimization status
            self.active_optimizations[optimization_id]["status"] = "completed"
            self.active_optimizations[optimization_id]["result"] = optimization_result
            
            # Learn from optimization
            await self._learn_from_optimization(system_id, optimization_result)
            
            # Record optimization event
            await publish_event(
                event_type="agent.action.completed",
                source_agent_id=self.system_id,
                entity_id=system_id,
                entity_type="quantum_optimization",
                data={
                    "optimization_id": optimization_id,
                    "method": method,
                    "objective_value": optimization_result.objective_value,
                    "improvement_ratio": optimization_result.improvement_ratio,
                    "convergence_iterations": optimization_result.convergence_iterations
                }
            )
            
            return {
                "optimization_id": optimization_id,
                "result": optimization_result,
                "system_coherence": quantum_system.calculate_system_coherence()
            }
            
        except Exception as e:
            self.logger.error(f"Failed to optimize quantum system: {e}")
            return {"error": str(e)}
    
    async def calculate_win_probability(
        self,
        system_id: str,
        win_category: WINCategory = WINCategory.COMPOSITE,
        context: Dict[str, Any] = None
    ) -> Optional[WINProbability]:
        """Calculate WIN probability cho current system state"""
        
        if system_id not in self.quantum_systems:
            return None
        
        try:
            quantum_system = self.quantum_systems[system_id]
            
            # Get current state
            current_state = await self.detect_current_quantum_state(system_id)
            if not current_state:
                return None
            
            # Calculate WIN probability
            win_probability = WINProbability(
                probability_id=str(uuid4()),
                win_category=win_category,
                base_probability=current_state.probability,
                confidence_level=0.8,
                contributing_factors={
                    "system_coherence": quantum_system.calculate_system_coherence(),
                    "state_stability": current_state.probability,
                    "optimization_effectiveness": self._calculate_optimization_effectiveness()
                }
            )
            
            # Enhanced calculation với context
            if context:
                win_probability = await self._enhance_win_probability_with_context(
                    win_probability, context
                )
            
            return win_probability
            
        except Exception as e:
            self.logger.error(f"Failed to calculate WIN probability: {e}")
            return None
    
    async def get_system_metrics(self, system_id: str) -> Optional[QuantumSystemMetrics]:
        """Get comprehensive metrics cho quantum system"""
        
        if system_id not in self.quantum_systems:
            return None
        
        try:
            quantum_system = self.quantum_systems[system_id]
            
            # Calculate metrics
            metrics = QuantumSystemMetrics(
                system_coherence=quantum_system.calculate_system_coherence(),
                win_probability=await self._calculate_average_win_probability(system_id),
                state_stability=await self._calculate_state_stability(system_id),
                transition_efficiency=await self._calculate_transition_efficiency(system_id),
                optimization_effectiveness=self._calculate_optimization_effectiveness(),
                learning_integration=await self._calculate_learning_integration(),
                prediction_accuracy=await self._calculate_prediction_accuracy(system_id),
                adaptation_speed=await self._calculate_adaptation_speed(system_id)
            )
            
            # Store metrics history
            self.metrics_history.append(metrics)
            
            return metrics
            
        except Exception as e:
            self.logger.error(f"Failed to get system metrics: {e}")
            return None
    
    async def start_background_processes(self) -> None:
        """Start background monitoring và optimization processes"""
        
        if self.background_tasks:
            await self.stop_background_processes()
        
        # Metrics collection task
        metrics_task = asyncio.create_task(self._metrics_collection_loop())
        self.background_tasks.append(metrics_task)
        
        # Optimization task
        optimization_task = asyncio.create_task(self._optimization_loop())
        self.background_tasks.append(optimization_task)
        
        # Coherence monitoring task
        coherence_task = asyncio.create_task(self._coherence_monitoring_loop())
        self.background_tasks.append(coherence_task)
        
        self.logger.info("Background processes started")
    
    async def stop_background_processes(self) -> None:
        """Stop all background processes"""
        
        for task in self.background_tasks:
            if not task.done():
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass
        
        self.background_tasks.clear()
        self.is_running = False
        self.logger.info("Background processes stopped")
    
    async def cleanup(self) -> None:
        """Cleanup resources"""
        
        await self.stop_background_processes()
        
        # Cleanup components
        if hasattr(self.state_detector, 'cleanup'):
            await self.state_detector.cleanup()
        
        self.quantum_systems.clear()
        self.active_optimizations.clear()
        
        self.logger.info("Quantum System Manager cleaned up")
    
    # Private methods
    
    async def _create_default_states(self, system_id: str) -> List[QuantumState]:
        """Create default quantum states cho new system"""
        
        states = []
        
        # WIN states
        win_states = [
            ("HIGH_PERFORMANCE", QuantumStateType.WIN, 0.3, "High organizational performance"),
            ("OPTIMAL_COLLABORATION", QuantumStateType.WIN, 0.25, "Optimal team collaboration"),
            ("INNOVATION_FLOW", QuantumStateType.WIN, 0.2, "Innovation and creativity flow")
        ]
        
        # Superposition states
        superposition_states = [
            ("ADAPTIVE_LEARNING", QuantumStateType.SUPERPOSITION, 0.15, "Adaptive learning state"),
            ("QUANTUM_COHERENCE", QuantumStateType.SUPERPOSITION, 0.1, "Quantum coherence state")
        ]
        
        # Create states
        for name, state_type, probability, description in win_states + superposition_states:
            state = QuantumState(
                state_id=str(uuid4()),
                state_type=state_type,
                amplitude=complex(np.sqrt(probability), 0.0),
                phase=0.0,
                probability=probability,
                description=description
            )
            states.append(state)
        
        return states
    
    async def _initialize_state_transitions(self, quantum_system: QuantumSystem) -> None:
        """Initialize state transitions cho quantum system"""
        
        states = list(quantum_system.quantum_states.values())
        
        # Create transitions between states
        for i, from_state in enumerate(states):
            for j, to_state in enumerate(states):
                if i != j:
                    transition_id = str(uuid4())
                    
                    # Calculate transition probability based on state types
                    if from_state.state_type == QuantumStateType.WIN and to_state.state_type == QuantumStateType.WIN:
                        transition_prob = 0.3
                    elif from_state.state_type == QuantumStateType.SUPERPOSITION:
                        transition_prob = 0.7
                    else:
                        transition_prob = 0.5
                    
                    transition = StateTransition(
                        transition_id=transition_id,
                        from_state=from_state.state_id,
                        to_state=to_state.state_id,
                        transition_probability=transition_prob,
                        trigger_conditions={"coherence_threshold": 0.5}
                    )
                    
                    quantum_system.state_transitions[transition_id] = transition
    
    async def _collect_organizational_signals(self) -> OrganizationalSignals:
        """Collect organizational signals từ TRM-OS systems"""
        
        # Get metrics từ learning system
        learning_stats = self.learning_system.get_statistics()
        
        # Calculate signals
        signals = OrganizationalSignals(
            tension_resolution_rate=0.75,  # Would get from tension service
            project_success_rate=0.68,     # Would get from project service
            agent_performance_metrics=learning_stats.get("performance_metrics", {}),
            resource_utilization=0.82,     # Would get from resource service
            communication_effectiveness=0.71,  # Would get from communication metrics
            learning_progress=learning_stats.get("learning_progress", 0.0),
            adaptation_success_rate=learning_stats.get("adaptation_success_rate", 0.0),
            system_coherence=0.65,          # Would calculate from system metrics
            timestamp=datetime.now()
        )
        
        return signals
    
    async def _learn_from_state_detection(
        self,
        system_id: str,
        signals: OrganizationalSignals,
        detected_state: QuantumState
    ) -> None:
        """Learn from state detection results"""
        
        try:
            # Create learning experience
            experience = LearningExperience(
                agent_id=self.system_id,
                experience_type=ExperienceType.QUANTUM_STATE_DETECTION,
                action_taken={
                    "action": "detect_quantum_state",
                    "system_id": system_id,
                    "signals": signals.__dict__
                },
                outcome={
                    "detected_state_id": detected_state.state_id,
                    "state_type": detected_state.state_type.value,
                    "probability": detected_state.probability
                },
                success=True,
                confidence=0.8,
                context={
                    "system_coherence": signals.system_coherence,
                    "learning_progress": signals.learning_progress
                }
            )
            
            # Add to learning system
            await self.learning_system.learn_from_experience(experience)
            
        except Exception as e:
            self.logger.error(f"Failed to learn from state detection: {e}")
    
    async def _learn_from_optimization(
        self,
        system_id: str,
        optimization_result: Any
    ) -> None:
        """Learn from optimization results"""
        
        try:
            # Create learning experience
            experience = LearningExperience(
                agent_id=self.system_id,
                experience_type=ExperienceType.QUANTUM_OPTIMIZATION,
                action_taken={
                    "action": "optimize_quantum_system",
                    "system_id": system_id,
                    "method": "hybrid_ml_optimization"
                },
                outcome={
                    "objective_value": optimization_result.objective_value,
                    "improvement_ratio": optimization_result.improvement_ratio,
                    "convergence_iterations": optimization_result.convergence_iterations
                },
                success=optimization_result.improvement_ratio > 0,
                confidence=optimization_result.solution_confidence,
                context={
                    "optimization_time": optimization_result.optimization_time,
                    "robustness_score": optimization_result.robustness_score
                }
            )
            
            # Add to learning system
            await self.learning_system.learn_from_experience(experience)
            
        except Exception as e:
            self.logger.error(f"Failed to learn from optimization: {e}")
    
    async def _metrics_collection_loop(self) -> None:
        """Background metrics collection loop"""
        
        while self.is_running:
            try:
                # Collect metrics for all systems
                for system_id in self.quantum_systems:
                    metrics = await self.get_system_metrics(system_id)
                    if metrics:
                        # Record metrics event
                        await publish_event(
                            event_type="knowledge.created",
                            source_agent_id=self.system_id,
                            entity_id=system_id,
                            entity_type="quantum_metrics",
                            data=metrics.to_dict()
                        )
                
                await asyncio.sleep(self.metrics_collection_interval)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error in metrics collection loop: {e}")
                await asyncio.sleep(self.metrics_collection_interval)
    
    async def _optimization_loop(self) -> None:
        """Background optimization loop"""
        
        while self.is_running:
            try:
                # Optimize systems that need it
                for system_id, quantum_system in self.quantum_systems.items():
                    coherence = quantum_system.calculate_system_coherence()
                    
                    if coherence < self.coherence_threshold:
                        await self.optimize_quantum_system(system_id)
                
                await asyncio.sleep(self.optimization_interval)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error in optimization loop: {e}")
                await asyncio.sleep(self.optimization_interval)
    
    async def _coherence_monitoring_loop(self) -> None:
        """Background coherence monitoring loop"""
        
        while self.is_running:
            try:
                # Monitor coherence for all systems
                for system_id, quantum_system in self.quantum_systems.items():
                    coherence = quantum_system.calculate_system_coherence()
                    
                    if coherence < self.coherence_threshold:
                        self.status = QuantumSystemStatus.COHERENCE_DEGRADED
                        
                        # Record coherence degradation event
                        await publish_event(
                            event_type="agent.action.failed",
                            source_agent_id=self.system_id,
                            entity_id=system_id,
                            entity_type="coherence_alert",
                            data={
                                "coherence": coherence,
                                "threshold": self.coherence_threshold,
                                "status": self.status.value
                            }
                        )
                    else:
                        if self.status == QuantumSystemStatus.COHERENCE_DEGRADED:
                            self.status = QuantumSystemStatus.ACTIVE
                
                await asyncio.sleep(60)  # Check every minute
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error in coherence monitoring loop: {e}")
                await asyncio.sleep(60)
    
    def _calculate_optimization_effectiveness(self) -> float:
        """Calculate optimization effectiveness từ history"""
        
        if not self.active_optimizations:
            return 0.0
        
        completed_optimizations = [
            opt for opt in self.active_optimizations.values()
            if opt.get("status") == "completed" and opt.get("result")
        ]
        
        if not completed_optimizations:
            return 0.0
        
        improvement_ratios = [
            opt["result"].improvement_ratio
            for opt in completed_optimizations
        ]
        
        return np.mean(improvement_ratios)
    
    async def _calculate_average_win_probability(self, system_id: str) -> float:
        """Calculate average WIN probability cho system"""
        
        quantum_system = self.quantum_systems[system_id]
        win_states = [
            state for state in quantum_system.quantum_states.values()
            if state.state_type == QuantumStateType.WIN
        ]
        
        if not win_states:
            return 0.0
        
        return np.mean([state.probability for state in win_states])
    
    async def _calculate_state_stability(self, system_id: str) -> float:
        """Calculate state stability"""
        
        # Would calculate from state transition history
        return 0.75  # Placeholder
    
    async def _calculate_transition_efficiency(self, system_id: str) -> float:
        """Calculate transition efficiency"""
        
        # Would calculate from transition success rate
        return 0.68  # Placeholder
    
    async def _calculate_learning_integration(self) -> float:
        """Calculate learning integration effectiveness"""
        
        learning_stats = self.learning_system.get_statistics()
        return learning_stats.get("learning_effectiveness", 0.0)
    
    async def _calculate_prediction_accuracy(self, system_id: str) -> float:
        """Calculate prediction accuracy"""
        
        # Would calculate from prediction vs actual results
        return 0.82  # Placeholder
    
    async def _calculate_adaptation_speed(self, system_id: str) -> float:
        """Calculate adaptation speed"""
        
        # Would calculate from adaptation response time
        return 0.77  # Placeholder
    
    async def _enhance_win_probability_with_context(
        self,
        win_probability: WINProbability,
        context: Dict[str, Any]
    ) -> WINProbability:
        """Enhance WIN probability calculation với context"""
        
        # Context-based enhancements
        context_factor = 1.0
        
        if context.get("high_priority_project"):
            context_factor *= 1.2
        
        if context.get("optimal_team_composition"):
            context_factor *= 1.15
        
        if context.get("resource_constraints"):
            context_factor *= 0.9
        
        # Update probability
        win_probability.base_probability = min(1.0, win_probability.base_probability * context_factor)
        win_probability.contributing_factors.update(context)
        
        return win_probability 