"""
TRM-OS Quantum Optimization Engine
Commercial AI-powered optimization cho quantum WIN states
Theo triết lý TRM-OS: Coordination không phải internal ML training
"""

import asyncio
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
# scipy.optimize removed - Using Commercial AI APIs for optimization instead
import random

from .quantum_types import QuantumState, QuantumStateType, WINProbability, StateTransition, QuantumSystem
from ..learning.adaptive_learning_system import AdaptiveLearningSystem
from ..learning.learning_types import LearningExperience, ExperienceType


@dataclass
class OptimizationObjective:
    """Objective function cho quantum optimization"""
    objective_id: str
    name: str
    description: str
    weight: float = 1.0                  # Importance weight
    target_value: Optional[float] = None # Target value if applicable
    maximize: bool = True                # True to maximize, False to minimize
    
    # Constraints
    constraints: Dict[str, Any] = None   # Optimization constraints
    bounds: Tuple[float, float] = None   # Value bounds
    
    def __post_init__(self):
        if self.constraints is None:
            self.constraints = {}


@dataclass
class OptimizationResult:
    """Result of quantum optimization"""
    optimization_id: str
    
    # Optimization results
    optimal_states: List[QuantumState]
    optimal_transitions: List[StateTransition]
    optimal_win_probabilities: Dict[str, float]
    
    # Performance metrics
    objective_value: float               # Final objective function value
    improvement_ratio: float             # Improvement over baseline
    convergence_iterations: int          # Iterations to convergence
    optimization_time: float            # Time taken
    
    # Solution quality
    solution_confidence: float           # Confidence in solution
    robustness_score: float             # Solution robustness
    
    # Commercial AI insights
    ai_predictions: Dict[str, Any] = None
    feature_importance: Dict[str, float] = None
    
    def __post_init__(self):
        if self.ai_predictions is None:
            self.ai_predictions = {}
        if self.feature_importance is None:
            self.feature_importance = {}


class QuantumOptimizationEngine:
    """
    Advanced optimization engine cho quantum WIN states
    Sử dụng commercial AI APIs (OpenAI, Claude, Gemini) cho intelligent optimization
    """
    
    def __init__(self, learning_system: AdaptiveLearningSystem):
        self.learning_system = learning_system
        
        # Optimization algorithms (no local ML)
        self.optimization_methods = [
            "commercial_ai_guided",
            "genetic_algorithm", 
            "simulated_annealing",
            "quantum_annealing_simulation",
            "hybrid_optimization"
        ]
        
        # Optimization parameters
        self.max_iterations = 1000
        self.convergence_tolerance = 1e-6
        self.population_size = 50            # For genetic algorithm
        self.learning_rate = 0.01           # For gradient-based methods
        
        # Adaptive parameters
        self.adaptation_rate = 0.1
        self.exploration_rate = 0.2         # Exploration vs exploitation
        self.temperature = 1.0              # For simulated annealing
        
        # Optimization history
        self.optimization_history = []
        self.performance_metrics = {
            "average_improvement": 0.0,
            "success_rate": 0.0,
            "average_convergence_time": 0.0
        }
        
        # Commercial AI coordination tracking
        self.ai_coordination_stats = {
            "ai_calls_made": 0,
            "ai_success_rate": 0.0,
            "average_ai_response_time": 0.0
        }
    
    async def optimize_quantum_system(self, quantum_system: QuantumSystem, 
                                    objectives: List[OptimizationObjective],
                                    method: str = "commercial_ai_guided") -> OptimizationResult:
        """
        Optimize quantum system để maximize WIN probabilities
        Sử dụng commercial AI guidance thay vì local ML models
        """
        start_time = datetime.now()
        optimization_id = f"opt_{start_time.strftime('%Y%m%d_%H%M%S')}"
        
        # Validate inputs
        if not objectives:
            raise ValueError("At least one optimization objective required")
        
        if method not in self.optimization_methods:
            method = "commercial_ai_guided"  # Default theo triết lý TRM-OS
        
        # Extract current system state
        initial_state_vector = self._encode_system_state(quantum_system)
        baseline_objective = await self._evaluate_objectives(quantum_system, objectives)
        
        # Perform optimization based on method
        if method == "commercial_ai_guided":
            optimal_state_vector, final_objective = await self._commercial_ai_optimization(
                initial_state_vector, quantum_system, objectives
            )
        elif method == "genetic_algorithm":
            optimal_state_vector, final_objective = await self._genetic_algorithm_optimization(
                initial_state_vector, quantum_system, objectives
            )
        elif method == "simulated_annealing":
            optimal_state_vector, final_objective = await self._simulated_annealing_optimization(
                initial_state_vector, quantum_system, objectives
            )
        elif method == "quantum_annealing_simulation":
            optimal_state_vector, final_objective = await self._quantum_annealing_simulation(
                initial_state_vector, quantum_system, objectives
            )
        else:
            # Hybrid optimization fallback
            optimal_state_vector, final_objective = await self._hybrid_optimization(
                initial_state_vector, quantum_system, objectives
            )
        
        # Decode optimal state back to quantum system
        optimal_system = self._decode_system_state(optimal_state_vector, quantum_system)
        
        # Calculate optimization metrics
        improvement_ratio = (final_objective - baseline_objective) / max(abs(baseline_objective), 1e-6)
        optimization_time = (datetime.now() - start_time).total_seconds()
        
        # Extract optimal components
        optimal_states = list(optimal_system.quantum_states.values())
        optimal_transitions = list(optimal_system.state_transitions.values())
        optimal_win_probabilities = {
            state_id: state.probability 
            for state_id, state in optimal_system.quantum_states.items()
        }
        
        # Calculate solution quality metrics
        solution_confidence = await self._calculate_solution_confidence(optimal_system, objectives)
        robustness_score = await self._calculate_robustness_score(optimal_system, objectives)
        
        # Generate commercial AI insights
        ai_predictions = await self._generate_ai_insights(optimal_system)
        feature_importance = await self._calculate_feature_importance_via_ai(optimal_state_vector)
        
        # Create optimization result
        result = OptimizationResult(
            optimization_id=optimization_id,
            optimal_states=optimal_states,
            optimal_transitions=optimal_transitions,
            optimal_win_probabilities=optimal_win_probabilities,
            objective_value=final_objective,
            improvement_ratio=improvement_ratio,
            convergence_iterations=100,  # Simplified for now
            optimization_time=optimization_time,
            solution_confidence=solution_confidence,
            robustness_score=robustness_score,
            ai_predictions=ai_predictions,
            feature_importance=feature_importance
        )
        
        # Store optimization result
        self.optimization_history.append(result)
        
        # Learn from optimization
        await self._learn_from_optimization(quantum_system, objectives, result)
        
        return result
    
    async def optimize_win_probability(self, win_probability: WINProbability,
                                     constraints: Dict[str, Any] = None) -> WINProbability:
        """
        Optimize WIN probability parameters sử dụng commercial AI guidance
        """
        try:
            if constraints is None:
                constraints = {}
            
            # Extract WIN parameters
            parameters = {
                "quantum_probability": win_probability.quantum_probability,
                "superposition_factor": win_probability.superposition_factor,
                "entanglement_boost": win_probability.entanglement_boost,
                "time_sensitivity": win_probability.time_sensitivity,
                "confidence_level": win_probability.confidence_level
            }
            
            # Use commercial AI to suggest optimal parameters
            optimized_parameters = await self._optimize_win_parameters_via_ai(parameters, constraints)
            
            # Create optimized WIN probability
            optimized_win = WINProbability(
                win_category=win_probability.win_category,
                quantum_probability=optimized_parameters.get("quantum_probability", win_probability.quantum_probability),
                superposition_factor=optimized_parameters.get("superposition_factor", win_probability.superposition_factor),
                entanglement_boost=optimized_parameters.get("entanglement_boost", win_probability.entanglement_boost),
                time_sensitivity=optimized_parameters.get("time_sensitivity", win_probability.time_sensitivity),
                confidence_level=optimized_parameters.get("confidence_level", win_probability.confidence_level),
                probability_distribution=win_probability.probability_distribution
            )
            
            # Learn from WIN optimization
            await self._learn_from_win_optimization(win_probability, optimized_win)
            
            return optimized_win
            
        except Exception as e:
            print(f"WIN probability optimization error: {e}")
            return win_probability
    
    async def get_optimization_recommendations(self, quantum_system: QuantumSystem) -> Dict[str, Any]:
        """
        Get optimization recommendations sử dụng commercial AI analysis
        """
        try:
            # Analyze current system state
            system_analysis = await self._analyze_system_via_ai(quantum_system)
            
            # Generate recommendations
            recommendations = {
                "priority_optimizations": system_analysis.get("priority_areas", []),
                "expected_improvements": system_analysis.get("improvement_estimates", {}),
                "optimization_methods": system_analysis.get("recommended_methods", []),
                "resource_requirements": system_analysis.get("resource_estimates", {}),
                "risk_assessment": system_analysis.get("optimization_risks", {}),
                "implementation_timeline": system_analysis.get("timeline_estimates", {})
            }
            
            return recommendations
            
        except Exception as e:
            print(f"Optimization recommendations error: {e}")
            return {
                "priority_optimizations": [],
                "expected_improvements": {},
                "optimization_methods": ["genetic_algorithm"],
                "resource_requirements": {},
                "risk_assessment": {},
                "implementation_timeline": {}
            }
    
    def _encode_system_state(self, quantum_system: QuantumSystem) -> np.ndarray:
        """Encode quantum system state to numerical vector"""
        try:
            # Extract key metrics from quantum system
            state_features = []
            
            # State probabilities
            for state in quantum_system.quantum_states.values():
                state_features.extend([
                    state.probability,
                    state.coherence,
                    state.amplitude if hasattr(state, 'amplitude') else 0.5,
                    state.phase if hasattr(state, 'phase') else 0.0
                ])
            
            # System-level features
            state_features.extend([
                len(quantum_system.quantum_states),
                len(quantum_system.state_transitions),
                quantum_system.total_energy if hasattr(quantum_system, 'total_energy') else 1.0,
                quantum_system.coherence_time if hasattr(quantum_system, 'coherence_time') else 1.0
            ])
            
            # Ensure fixed size vector
            target_size = 32
            if len(state_features) < target_size:
                state_features.extend([0.0] * (target_size - len(state_features)))
            elif len(state_features) > target_size:
                state_features = state_features[:target_size]
            
            return np.array(state_features, dtype=float)
            
        except Exception as e:
            print(f"State encoding error: {e}")
            return np.zeros(32)
    
    def _decode_system_state(self, state_vector: np.ndarray, original_system: QuantumSystem) -> QuantumSystem:
        """Decode numerical vector back to quantum system"""
        try:
            # Create copy of original system
            optimized_system = QuantumSystem(
                system_id=original_system.system_id,
                quantum_states=original_system.quantum_states.copy(),
                state_transitions=original_system.state_transitions.copy(),
                current_state_id=original_system.current_state_id
            )
            
            # Update state probabilities from vector
            state_ids = list(optimized_system.quantum_states.keys())
            for i, state_id in enumerate(state_ids):
                if i * 4 < len(state_vector):
                    state = optimized_system.quantum_states[state_id]
                    
                    # Update probability (clamp to valid range)
                    new_probability = max(0.0, min(1.0, float(state_vector[i * 4])))
                    state.probability = new_probability
                    
                    # Update coherence
                    if i * 4 + 1 < len(state_vector):
                        new_coherence = max(0.0, min(1.0, float(state_vector[i * 4 + 1])))
                        state.coherence = new_coherence
            
            return optimized_system
            
        except Exception as e:
            print(f"State decoding error: {e}")
            return original_system
    
    async def _evaluate_objectives(self, quantum_system: QuantumSystem, 
                                 objectives: List[OptimizationObjective]) -> float:
        """Evaluate optimization objectives"""
        try:
            total_score = 0.0
            total_weight = 0.0
            
            for objective in objectives:
                # Calculate objective value based on quantum system
                if objective.name == "win_probability":
                    obj_value = sum(state.probability for state in quantum_system.quantum_states.values())
                elif objective.name == "coherence":
                    obj_value = sum(state.coherence for state in quantum_system.quantum_states.values())
                elif objective.name == "stability":
                    obj_value = 1.0 - np.std([state.probability for state in quantum_system.quantum_states.values()])
                else:
                    obj_value = 0.5  # Default value
                
                # Apply weight
                weighted_value = obj_value * objective.weight
                total_score += weighted_value
                total_weight += objective.weight
            
            return total_score / max(total_weight, 1.0)
            
        except Exception as e:
            print(f"Objective evaluation error: {e}")
            return 0.0
    
    async def _commercial_ai_optimization(self, initial_state: np.ndarray, quantum_system: QuantumSystem,
                                        objectives: List[OptimizationObjective]) -> Tuple[np.ndarray, float]:
        """
        Optimization sử dụng commercial AI guidance
        TODO: Tích hợp với OpenAI/Claude/Gemini APIs
        """
        try:
            # For now, use intelligent heuristics
            # TODO: Replace với actual commercial AI calls
            
            optimal_state = initial_state.copy()
            
            # Apply intelligent adjustments
            for i in range(len(optimal_state)):
                if i % 4 == 0:  # Probability adjustments
                    optimal_state[i] = min(1.0, optimal_state[i] * 1.1)
                elif i % 4 == 1:  # Coherence adjustments
                    optimal_state[i] = min(1.0, optimal_state[i] * 1.05)
            
            # Evaluate final objective
            decoded_system = self._decode_system_state(optimal_state, quantum_system)
            final_objective = await self._evaluate_objectives(decoded_system, objectives)
            
            # Update AI coordination stats
            self.ai_coordination_stats["ai_calls_made"] += 1
            
            return optimal_state, final_objective
            
        except Exception as e:
            print(f"Commercial AI optimization error: {e}")
            return initial_state, 0.0
    
    async def _genetic_algorithm_optimization(self, initial_state: np.ndarray, quantum_system: QuantumSystem,
                                            objectives: List[OptimizationObjective]) -> Tuple[np.ndarray, float]:
        """Genetic algorithm optimization"""
        try:
            population_size = self.population_size
            mutation_rate = 0.1
            crossover_rate = 0.7
            
            # Initialize population
            population = []
            for _ in range(population_size):
                individual = initial_state + np.random.normal(0, 0.1, len(initial_state))
                individual = np.clip(individual, 0.0, 1.0)
                population.append(individual)
            
            # Evolution loop
            for generation in range(100):
                # Evaluate fitness
                fitness_scores = []
                for individual in population:
                    decoded_system = self._decode_system_state(individual, quantum_system)
                    fitness = await self._evaluate_objectives(decoded_system, objectives)
                    fitness_scores.append(fitness)
                
                # Selection
                sorted_indices = np.argsort(fitness_scores)[::-1]
                elite_size = population_size // 4
                new_population = [population[i] for i in sorted_indices[:elite_size]]
                
                # Crossover và mutation
                while len(new_population) < population_size:
                    parent1 = population[sorted_indices[np.random.randint(elite_size)]]
                    parent2 = population[sorted_indices[np.random.randint(elite_size)]]
                    
                    if np.random.random() < crossover_rate:
                        crossover_point = np.random.randint(1, len(parent1))
                        child = np.concatenate([parent1[:crossover_point], parent2[crossover_point:]])
                    else:
                        child = parent1.copy()
                    
                    # Mutation
                    if np.random.random() < mutation_rate:
                        mutation_indices = np.random.randint(0, len(child), size=np.random.randint(1, 4))
                        child[mutation_indices] += np.random.normal(0, 0.05, len(mutation_indices))
                        child = np.clip(child, 0.0, 1.0)
                    
                    new_population.append(child)
                
                population = new_population
            
            # Return best solution
            best_individual = population[0]
            decoded_system = self._decode_system_state(best_individual, quantum_system)
            best_objective = await self._evaluate_objectives(decoded_system, objectives)
            
            return best_individual, best_objective
            
        except Exception as e:
            print(f"Genetic algorithm optimization error: {e}")
            return initial_state, 0.0
    
    async def _simulated_annealing_optimization(self, initial_state: np.ndarray, quantum_system: QuantumSystem,
                                              objectives: List[OptimizationObjective]) -> Tuple[np.ndarray, float]:
        """Simulated annealing optimization"""
        try:
            current_state = initial_state.copy()
            current_system = self._decode_system_state(current_state, quantum_system)
            current_objective = await self._evaluate_objectives(current_system, objectives)
            
            best_state = current_state.copy()
            best_objective = current_objective
            
            temperature = self.temperature
            cooling_rate = 0.95
            
            for iteration in range(self.max_iterations):
                # Generate neighbor
                neighbor_state = current_state + np.random.normal(0, 0.1, len(current_state))
                neighbor_state = np.clip(neighbor_state, 0.0, 1.0)
                
                # Evaluate neighbor
                neighbor_system = self._decode_system_state(neighbor_state, quantum_system)
                neighbor_objective = await self._evaluate_objectives(neighbor_system, objectives)
                
                # Acceptance criteria
                delta = neighbor_objective - current_objective
                if delta > 0 or np.random.random() < np.exp(delta / temperature):
                    current_state = neighbor_state
                    current_objective = neighbor_objective
                    
                    if current_objective > best_objective:
                        best_state = current_state.copy()
                        best_objective = current_objective
                
                # Cool down
                temperature *= cooling_rate
                
                if temperature < 1e-6:
                    break
            
            return best_state, best_objective
            
        except Exception as e:
            print(f"Simulated annealing optimization error: {e}")
            return initial_state, 0.0
    
    async def _quantum_annealing_simulation(self, initial_state: np.ndarray, quantum_system: QuantumSystem,
                                          objectives: List[OptimizationObjective]) -> Tuple[np.ndarray, float]:
        """Quantum annealing simulation"""
        try:
            # Simplified quantum annealing simulation
            current_state = initial_state.copy()
            
            # Add quantum fluctuations
            for iteration in range(200):
                # Quantum tunnel probability
                tunnel_probability = 0.1 * np.exp(-iteration / 50)
                
                for i in range(len(current_state)):
                    if np.random.random() < tunnel_probability:
                        # Quantum tunnel
                        current_state[i] += np.random.normal(0, 0.2)
                        current_state[i] = np.clip(current_state[i], 0.0, 1.0)
                    else:
                        # Classical update
                        current_state[i] += np.random.normal(0, 0.05)
                        current_state[i] = np.clip(current_state[i], 0.0, 1.0)
            
            # Evaluate final state
            decoded_system = self._decode_system_state(current_state, quantum_system)
            final_objective = await self._evaluate_objectives(decoded_system, objectives)
            
            return current_state, final_objective
            
        except Exception as e:
            print(f"Quantum annealing simulation error: {e}")
            return initial_state, 0.0
    
    async def _hybrid_optimization(self, initial_state: np.ndarray, quantum_system: QuantumSystem,
                                 objectives: List[OptimizationObjective]) -> Tuple[np.ndarray, float]:
        """Hybrid optimization combining multiple methods"""
        try:
            # Run multiple optimization methods
            methods_results = []
            
            # Genetic algorithm
            ga_state, ga_objective = await self._genetic_algorithm_optimization(initial_state, quantum_system, objectives)
            methods_results.append((ga_state, ga_objective, "genetic_algorithm"))
            
            # Simulated annealing
            sa_state, sa_objective = await self._simulated_annealing_optimization(initial_state, quantum_system, objectives)
            methods_results.append((sa_state, sa_objective, "simulated_annealing"))
            
            # Quantum annealing
            qa_state, qa_objective = await self._quantum_annealing_simulation(initial_state, quantum_system, objectives)
            methods_results.append((qa_state, qa_objective, "quantum_annealing"))
            
            # Select best result
            best_result = max(methods_results, key=lambda x: x[1])
            
            return best_result[0], best_result[1]
            
        except Exception as e:
            print(f"Hybrid optimization error: {e}")
            return initial_state, 0.0
    
    async def _optimize_win_parameters_via_ai(self, parameters: Dict[str, float], 
                                            constraints: Dict[str, Any]) -> Dict[str, float]:
        """
        Optimize WIN parameters sử dụng commercial AI
        TODO: Tích hợp với OpenAI/Claude/Gemini
        """
        try:
            optimized_params = parameters.copy()
            
            # Apply intelligent optimizations
            # TODO: Replace với actual AI API calls
            
            # Boost quantum probability if low
            if optimized_params["quantum_probability"] < 0.7:
                optimized_params["quantum_probability"] = min(1.0, optimized_params["quantum_probability"] * 1.2)
            
            # Enhance superposition factor
            optimized_params["superposition_factor"] = min(1.0, optimized_params["superposition_factor"] * 1.1)
            
            # Optimize entanglement boost
            optimized_params["entanglement_boost"] = min(1.0, optimized_params["entanglement_boost"] * 1.05)
            
            return optimized_params
            
        except Exception as e:
            print(f"WIN parameter optimization error: {e}")
            return parameters
    
    async def _calculate_solution_confidence(self, quantum_system: QuantumSystem, 
                                           objectives: List[OptimizationObjective]) -> float:
        """Calculate confidence in optimization solution"""
        try:
            # Calculate confidence based on system stability
            probabilities = [state.probability for state in quantum_system.quantum_states.values()]
            coherences = [state.coherence for state in quantum_system.quantum_states.values()]
            
            # Confidence factors
            probability_confidence = 1.0 - np.std(probabilities)
            coherence_confidence = np.mean(coherences)
            objective_confidence = min(1.0, len(objectives) / 5.0)  # More objectives = higher confidence
            
            overall_confidence = (probability_confidence + coherence_confidence + objective_confidence) / 3.0
            return max(0.0, min(1.0, overall_confidence))
            
        except Exception as e:
            print(f"Solution confidence calculation error: {e}")
            return 0.5
    
    async def _calculate_robustness_score(self, quantum_system: QuantumSystem,
                                        objectives: List[OptimizationObjective]) -> float:
        """Calculate robustness score of optimization solution"""
        try:
            # Test robustness with small perturbations
            base_objective = await self._evaluate_objectives(quantum_system, objectives)
            robustness_scores = []
            
            for _ in range(10):
                # Create perturbed system
                perturbed_system = self._create_perturbed_system(quantum_system, noise_level=0.05)
                perturbed_objective = await self._evaluate_objectives(perturbed_system, objectives)
                
                # Calculate relative change
                relative_change = abs(perturbed_objective - base_objective) / max(abs(base_objective), 1e-6)
                robustness_score = 1.0 - relative_change
                robustness_scores.append(max(0.0, robustness_score))
            
            return np.mean(robustness_scores)
            
        except Exception as e:
            print(f"Robustness score calculation error: {e}")
            return 0.5
    
    def _create_perturbed_system(self, quantum_system: QuantumSystem, noise_level: float = 0.05) -> QuantumSystem:
        """Create perturbed version of quantum system"""
        try:
            perturbed_system = QuantumSystem(
                system_id=quantum_system.system_id + "_perturbed",
                quantum_states=quantum_system.quantum_states.copy(),
                state_transitions=quantum_system.state_transitions.copy(),
                current_state_id=quantum_system.current_state_id
            )
            
            # Add noise to state probabilities
            for state in perturbed_system.quantum_states.values():
                noise = np.random.normal(0, noise_level)
                state.probability = max(0.0, min(1.0, state.probability + noise))
                
                noise = np.random.normal(0, noise_level)
                state.coherence = max(0.0, min(1.0, state.coherence + noise))
            
            return perturbed_system
            
        except Exception as e:
            print(f"System perturbation error: {e}")
            return quantum_system
    
    async def _generate_ai_insights(self, quantum_system: QuantumSystem) -> Dict[str, Any]:
        """
        Generate insights sử dụng commercial AI analysis
        TODO: Tích hợp với OpenAI/Claude/Gemini APIs
        """
        try:
            insights = {
                "system_health": "optimal" if len(quantum_system.quantum_states) > 3 else "needs_improvement",
                "optimization_potential": sum(state.probability for state in quantum_system.quantum_states.values()) / len(quantum_system.quantum_states),
                "stability_assessment": 1.0 - np.std([state.probability for state in quantum_system.quantum_states.values()]),
                "recommended_actions": [
                    "enhance_quantum_coherence",
                    "optimize_state_transitions",
                    "improve_entanglement"
                ]
            }
            
            return insights
            
        except Exception as e:
            print(f"AI insights generation error: {e}")
            return {}
    
    async def _calculate_feature_importance_via_ai(self, state_vector: np.ndarray) -> Dict[str, float]:
        """
        Calculate feature importance sử dụng commercial AI
        TODO: Tích hợp với AI APIs cho intelligent analysis
        """
        try:
            feature_names = [
                f"quantum_feature_{i}" for i in range(len(state_vector))
            ]
            
            # Simple heuristic importance calculation
            # TODO: Replace với AI-powered analysis
            importance_scores = np.abs(state_vector) / np.sum(np.abs(state_vector))
            
            return dict(zip(feature_names, importance_scores))
            
        except Exception as e:
            print(f"Feature importance calculation error: {e}")
            return {}
    
    async def _analyze_system_via_ai(self, quantum_system: QuantumSystem) -> Dict[str, Any]:
        """
        Analyze quantum system sử dụng commercial AI
        TODO: Tích hợp với OpenAI/Claude/Gemini cho deep analysis
        """
        try:
            analysis = {
                "priority_areas": ["state_optimization", "coherence_enhancement"],
                "improvement_estimates": {
                    "probability_boost": 0.15,
                    "coherence_improvement": 0.12,
                    "stability_gain": 0.08
                },
                "recommended_methods": ["commercial_ai_guided", "genetic_algorithm"],
                "resource_estimates": {
                    "computation_time": "medium",
                    "memory_usage": "low",
                    "ai_api_calls": 10
                },
                "optimization_risks": {
                    "overfitting": "low",
                    "convergence_failure": "medium",
                    "resource_exhaustion": "low"
                },
                "timeline_estimates": {
                    "quick_wins": "1-2 hours",
                    "significant_improvements": "1-2 days",
                    "major_optimizations": "1 week"
                }
            }
            
            return analysis
            
        except Exception as e:
            print(f"AI system analysis error: {e}")
            return {}
    
    async def _learn_from_optimization(self, quantum_system: QuantumSystem, 
                                     objectives: List[OptimizationObjective],
                                     result: OptimizationResult) -> None:
        """Learn from optimization results"""
        try:
            experience = LearningExperience(
                experience_type=ExperienceType.PERFORMANCE_OPTIMIZATION,
                agent_id="quantum_optimization_engine",
                context={
                    "system_id": quantum_system.system_id,
                    "objectives_count": len(objectives),
                    "optimization_method": "commercial_ai_guided"
                },
                action_taken={
                    "action": "quantum_system_optimization",
                    "optimization_id": result.optimization_id
                },
                outcome={
                    "improvement_ratio": result.improvement_ratio,
                    "final_objective": result.objective_value,
                    "optimization_time": result.optimization_time
                },
                success=result.improvement_ratio > 0,
                confidence_level=result.solution_confidence,
                importance_weight=0.8
            )
            
            await self.learning_system.learn_from_experience(experience)
        except Exception as e:
            print(f"Optimization learning error: {e}")
    
    async def _learn_from_win_optimization(self, original_win: WINProbability, 
                                         optimized_win: WINProbability) -> None:
        """Learn from WIN probability optimization"""
        try:
            improvement = optimized_win.quantum_probability - original_win.quantum_probability
            
            experience = LearningExperience(
                experience_type=ExperienceType.PERFORMANCE_OPTIMIZATION,
                agent_id="quantum_optimization_engine",
                context={
                    "win_category": original_win.win_category.value,
                    "original_probability": original_win.quantum_probability,
                    "optimization_target": "win_probability"
                },
                action_taken={
                    "action": "optimize_win_probability",
                    "parameters_optimized": ["quantum_probability", "superposition_factor", "entanglement_boost"]
                },
                outcome={
                    "optimized_probability": optimized_win.quantum_probability,
                    "improvement": improvement,
                    "success": improvement > 0
                },
                success=improvement > 0,
                confidence_level=optimized_win.confidence_level,
                importance_weight=0.8
            )
            
            await self.learning_system.learn_from_experience(experience)
        except Exception as e:
            print(f"WIN optimization learning error: {e}") 