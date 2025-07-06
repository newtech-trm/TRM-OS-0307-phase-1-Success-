"""
TRM-OS Quantum Optimization Engine
ML-powered optimization cho quantum WIN states
"""

import asyncio
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from scipy.optimize import minimize, differential_evolution
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, WhiteKernel
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
    
    # ML insights
    ml_predictions: Dict[str, Any] = None
    feature_importance: Dict[str, float] = None
    
    def __post_init__(self):
        if self.ml_predictions is None:
            self.ml_predictions = {}
        if self.feature_importance is None:
            self.feature_importance = {}


class QuantumOptimizationEngine:
    """
    Advanced optimization engine cho quantum WIN states
    Sử dụng multiple optimization algorithms và ML predictions
    """
    
    def __init__(self, learning_system: AdaptiveLearningSystem):
        self.learning_system = learning_system
        
        # Optimization algorithms
        self.optimization_methods = [
            "gradient_descent",
            "genetic_algorithm", 
            "bayesian_optimization",
            "quantum_annealing_simulation",
            "hybrid_ml_optimization"
        ]
        
        # ML Models for optimization
        self.objective_predictor = GaussianProcessRegressor(
            kernel=RBF(length_scale=1.0) + WhiteKernel(noise_level=0.1),
            alpha=1e-6,
            normalize_y=True,
            n_restarts_optimizer=10
        )
        self.constraint_predictor = GaussianProcessRegressor(
            kernel=RBF(length_scale=1.0) + WhiteKernel(noise_level=0.1),
            alpha=1e-6,
            normalize_y=True
        )
        
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
        
        # ML training data
        self.training_data = []
        self.models_trained = False
    
    async def optimize_quantum_system(self, quantum_system: QuantumSystem, 
                                    objectives: List[OptimizationObjective],
                                    method: str = "hybrid_ml_optimization") -> OptimizationResult:
        """
        Optimize quantum system để maximize WIN probabilities
        """
        start_time = datetime.now()
        optimization_id = f"opt_{start_time.strftime('%Y%m%d_%H%M%S')}"
        
        # Validate inputs
        if not objectives:
            raise ValueError("At least one optimization objective required")
        
        if method not in self.optimization_methods:
            method = "hybrid_ml_optimization"  # Default fallback
        
        # Extract current system state
        initial_state_vector = self._encode_system_state(quantum_system)
        baseline_objective = await self._evaluate_objectives(quantum_system, objectives)
        
        # Perform optimization based on method
        if method == "hybrid_ml_optimization":
            optimal_state_vector, final_objective = await self._hybrid_ml_optimization(
                initial_state_vector, quantum_system, objectives
            )
        elif method == "bayesian_optimization":
            optimal_state_vector, final_objective = await self._bayesian_optimization(
                initial_state_vector, quantum_system, objectives
            )
        elif method == "genetic_algorithm":
            optimal_state_vector, final_objective = await self._genetic_algorithm_optimization(
                initial_state_vector, quantum_system, objectives
            )
        elif method == "quantum_annealing_simulation":
            optimal_state_vector, final_objective = await self._quantum_annealing_simulation(
                initial_state_vector, quantum_system, objectives
            )
        else:
            # Gradient descent fallback
            optimal_state_vector, final_objective = await self._gradient_descent_optimization(
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
        
        # Generate ML insights
        ml_predictions = {}
        feature_importance = {}
        if self.models_trained:
            ml_predictions = await self._generate_ml_insights(optimal_system)
            feature_importance = await self._calculate_feature_importance(optimal_state_vector)
        
        # Create optimization result
        result = OptimizationResult(
            optimization_id=optimization_id,
            optimal_states=optimal_states,
            optimal_transitions=optimal_transitions,
            optimal_win_probabilities=optimal_win_probabilities,
            objective_value=final_objective,
            improvement_ratio=improvement_ratio,
            convergence_iterations=100,  # Placeholder - would track actual iterations
            optimization_time=optimization_time,
            solution_confidence=solution_confidence,
            robustness_score=robustness_score,
            ml_predictions=ml_predictions,
            feature_importance=feature_importance
        )
        
        # Learn from optimization
        await self._learn_from_optimization(quantum_system, objectives, result)
        
        # Update optimization history
        self.optimization_history.append(result)
        await self._update_performance_metrics()
        
        return result
    
    async def optimize_win_probability(self, win_probability: WINProbability,
                                     constraints: Dict[str, Any] = None) -> WINProbability:
        """
        Optimize individual WIN probability
        """
        if constraints is None:
            constraints = {}
        
        # Create optimization objective
        objective = OptimizationObjective(
            objective_id="win_prob_opt",
            name="Maximize WIN Probability",
            description=f"Optimize probability for WIN: {win_probability.win_description}",
            weight=1.0,
            maximize=True,
            constraints=constraints
        )
        
        # Current probability as baseline
        baseline_prob = win_probability.quantum_probability
        
        # Optimization parameters to tune
        parameters = {
            "superposition_factor": win_probability.superposition_factor,
            "entanglement_boost": win_probability.entanglement_boost,
            "time_sensitivity": win_probability.time_sensitivity
        }
        
        # Optimize parameters
        optimal_params = await self._optimize_win_parameters(parameters, constraints)
        
        # Update WIN probability with optimal parameters
        optimized_win = WINProbability(
            win_id=win_probability.win_id,
            win_description=win_probability.win_description,
            win_category=win_probability.win_category,
            base_probability=win_probability.base_probability,
            quantum_probability=optimal_params.get("quantum_probability", baseline_prob),
            superposition_factor=optimal_params.get("superposition_factor", win_probability.superposition_factor),
            entanglement_boost=optimal_params.get("entanglement_boost", win_probability.entanglement_boost),
            confidence_level=win_probability.confidence_level,
            prediction_accuracy=win_probability.prediction_accuracy,
            contributing_factors=win_probability.contributing_factors,
            risk_factors=win_probability.risk_factors,
            probability_trend="increasing",  # Assume optimization improves trend
            optimal_timing=win_probability.optimal_timing,
            time_sensitivity=optimal_params.get("time_sensitivity", win_probability.time_sensitivity),
            prerequisite_states=win_probability.prerequisite_states,
            blocking_states=win_probability.blocking_states
        )
        
        # Learn from WIN optimization
        await self._learn_from_win_optimization(win_probability, optimized_win)
        
        return optimized_win
    
    async def train_optimization_models(self, training_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Train ML models cho optimization guidance
        """
        if not training_data:
            return {"error": "No training data provided"}
        
        # Prepare training data
        X = []  # System state features
        y_objectives = []  # Objective function values
        y_constraints = []  # Constraint satisfaction
        
        for data_point in training_data:
            features = data_point.get("state_features", [])
            objective_value = data_point.get("objective_value", 0.0)
            constraint_satisfaction = data_point.get("constraint_satisfaction", 1.0)
            
            X.append(features)
            y_objectives.append(objective_value)
            y_constraints.append(constraint_satisfaction)
        
        # Convert to numpy arrays
        X = np.array(X)
        y_objectives = np.array(y_objectives)
        y_constraints = np.array(y_constraints)
        
        # Train objective predictor
        self.objective_predictor.fit(X, y_objectives)
        
        # Train constraint predictor
        self.constraint_predictor.fit(X, y_constraints)
        
        # Update training status
        self.models_trained = True
        self.training_data = training_data
        
        # Calculate training metrics
        objective_score = self.objective_predictor.score(X, y_objectives)
        constraint_score = self.constraint_predictor.score(X, y_constraints)
        
        training_result = {
            "models_trained": True,
            "training_samples": len(training_data),
            "objective_prediction_r2": objective_score,
            "constraint_prediction_r2": constraint_score,
            "feature_count": X.shape[1] if X.shape[0] > 0 else 0
        }
        
        # Learn from training
        await self._learn_from_model_training(training_result)
        
        return training_result
    
    async def get_optimization_recommendations(self, quantum_system: QuantumSystem) -> Dict[str, Any]:
        """
        Get ML-powered recommendations cho system optimization
        """
        recommendations = {
            "state_modifications": [],
            "transition_optimizations": [],
            "parameter_adjustments": [],
            "strategic_insights": []
        }
        
        # Analyze current system
        current_coherence = quantum_system.calculate_system_coherence()
        state_count = len(quantum_system.quantum_states)
        entanglement_count = sum(len(states) for states in quantum_system.entanglement_network.values())
        
        # State modification recommendations
        if current_coherence < 0.5:
            recommendations["state_modifications"].append({
                "type": "increase_coherence",
                "description": "System coherence is low. Consider reducing decoherence rates.",
                "priority": "high",
                "expected_improvement": 0.3
            })
        
        if state_count < 3:
            recommendations["state_modifications"].append({
                "type": "add_superposition_states",
                "description": "Add more superposition states to increase WIN potential.",
                "priority": "medium",
                "expected_improvement": 0.2
            })
        
        # Transition optimization recommendations
        for transition_id, transition in quantum_system.state_transitions.items():
            if transition.transition_probability < 0.3:
                recommendations["transition_optimizations"].append({
                    "transition_id": transition_id,
                    "type": "increase_transition_probability",
                    "description": f"Low transition probability from {transition.from_state} to {transition.to_state}",
                    "priority": "medium",
                    "suggested_probability": min(0.7, transition.transition_probability * 2)
                })
        
        # Parameter adjustment recommendations
        if entanglement_count < state_count / 2:
            recommendations["parameter_adjustments"].append({
                "type": "increase_entanglement",
                "description": "Increase entanglement between states to boost WIN probabilities.",
                "priority": "high",
                "target_entanglement_ratio": 0.6
            })
        
        # Strategic insights
        if self.models_trained and len(self.optimization_history) > 5:
            avg_improvement = np.mean([r.improvement_ratio for r in self.optimization_history[-5:]])
            if avg_improvement > 0.2:
                recommendations["strategic_insights"].append({
                    "type": "optimization_trend",
                    "description": f"Recent optimizations show {avg_improvement:.1%} average improvement. Continue current strategy.",
                    "confidence": 0.8
                })
        
        return recommendations
    
    def _encode_system_state(self, quantum_system: QuantumSystem) -> np.ndarray:
        """Encode quantum system state as feature vector"""
        features = []
        
        # System-level features
        features.extend([
            quantum_system.total_coherence,
            quantum_system.system_entropy,
            len(quantum_system.quantum_states),
            len(quantum_system.state_transitions),
            len(quantum_system.entanglement_network)
        ])
        
        # State features (aggregate)
        if quantum_system.quantum_states:
            probabilities = [s.probability for s in quantum_system.quantum_states.values()]
            features.extend([
                np.mean(probabilities),
                np.std(probabilities),
                np.max(probabilities),
                np.min(probabilities)
            ])
        else:
            features.extend([0.0, 0.0, 0.0, 0.0])
        
        # Transition features (aggregate)
        if quantum_system.state_transitions:
            trans_probs = [t.transition_probability for t in quantum_system.state_transitions.values()]
            features.extend([
                np.mean(trans_probs),
                np.std(trans_probs),
                np.max(trans_probs),
                np.min(trans_probs)
            ])
        else:
            features.extend([0.0, 0.0, 0.0, 0.0])
        
        # Pad to fixed size
        target_size = 20
        if len(features) < target_size:
            features.extend([0.0] * (target_size - len(features)))
        elif len(features) > target_size:
            features = features[:target_size]
        
        return np.array(features)
    
    def _decode_system_state(self, state_vector: np.ndarray, original_system: QuantumSystem) -> QuantumSystem:
        """Decode feature vector back to quantum system"""
        # This is a simplified implementation
        # In practice, this would involve more sophisticated state reconstruction
        
        # Create modified system
        optimized_system = QuantumSystem(
            system_id=f"optimized_{original_system.system_id}",
            quantum_states=original_system.quantum_states.copy(),
            state_transitions=original_system.state_transitions.copy(),
            entanglement_network=original_system.entanglement_network.copy()
        )
        
        # Apply optimizations based on state vector
        target_coherence = min(1.0, max(0.0, state_vector[0]))
        optimized_system.total_coherence = target_coherence
        
        # Adjust state probabilities proportionally
        if state_vector[5] > 0:  # Mean probability target
            target_mean_prob = min(1.0, max(0.0, state_vector[5]))
            current_mean_prob = np.mean([s.probability for s in optimized_system.quantum_states.values()])
            
            if current_mean_prob > 0:
                adjustment_factor = target_mean_prob / current_mean_prob
                for state in optimized_system.quantum_states.values():
                    state.probability = min(1.0, state.probability * adjustment_factor)
                    state.amplitude = complex(np.sqrt(state.probability), 0.0)
        
        return optimized_system
    
    async def _evaluate_objectives(self, quantum_system: QuantumSystem, 
                                 objectives: List[OptimizationObjective]) -> float:
        """Evaluate objective function for quantum system"""
        total_objective = 0.0
        
        for objective in objectives:
            if objective.name == "Maximize System Coherence":
                value = quantum_system.total_coherence
            elif objective.name == "Maximize WIN Probabilities":
                if quantum_system.quantum_states:
                    value = np.mean([s.probability for s in quantum_system.quantum_states.values()])
                else:
                    value = 0.0
            elif objective.name == "Minimize System Entropy":
                value = -quantum_system.system_entropy  # Negative because we want to minimize
            else:
                # Default: use system coherence
                value = quantum_system.total_coherence
            
            # Apply objective weight and direction
            if not objective.maximize:
                value = -value
            
            total_objective += objective.weight * value
        
        return total_objective
    
    async def _hybrid_ml_optimization(self, initial_state: np.ndarray, quantum_system: QuantumSystem,
                                    objectives: List[OptimizationObjective]) -> Tuple[np.ndarray, float]:
        """Hybrid ML-guided optimization"""
        best_state = initial_state.copy()
        best_objective = await self._evaluate_objectives(quantum_system, objectives)
        
        # If models are trained, use ML guidance
        if self.models_trained:
            # Predict optimal direction using ML
            predicted_objective = self.objective_predictor.predict([initial_state])[0]
            
            # Use acquisition function to guide search
            for iteration in range(100):
                # Generate candidate states around current best
                candidate_state = best_state + np.random.normal(0, 0.1, size=best_state.shape)
                candidate_state = np.clip(candidate_state, 0, 1)  # Ensure valid bounds
                
                # Evaluate candidate
                candidate_system = self._decode_system_state(candidate_state, quantum_system)
                candidate_objective = await self._evaluate_objectives(candidate_system, objectives)
                
                # Accept if better
                if candidate_objective > best_objective:
                    best_state = candidate_state
                    best_objective = candidate_objective
        else:
            # Fallback to random search
            for iteration in range(50):
                candidate_state = initial_state + np.random.normal(0, 0.2, size=initial_state.shape)
                candidate_state = np.clip(candidate_state, 0, 1)
                
                candidate_system = self._decode_system_state(candidate_state, quantum_system)
                candidate_objective = await self._evaluate_objectives(candidate_system, objectives)
                
                if candidate_objective > best_objective:
                    best_state = candidate_state
                    best_objective = candidate_objective
        
        return best_state, best_objective
    
    async def _bayesian_optimization(self, initial_state: np.ndarray, quantum_system: QuantumSystem,
                                   objectives: List[OptimizationObjective]) -> Tuple[np.ndarray, float]:
        """Bayesian optimization implementation"""
        # Simplified Bayesian optimization
        best_state = initial_state.copy()
        best_objective = await self._evaluate_objectives(quantum_system, objectives)
        
        # Sample points for Gaussian Process
        n_samples = 20
        X_samples = []
        y_samples = []
        
        for _ in range(n_samples):
            sample_state = np.random.uniform(0, 1, size=initial_state.shape)
            sample_system = self._decode_system_state(sample_state, quantum_system)
            sample_objective = await self._evaluate_objectives(sample_system, objectives)
            
            X_samples.append(sample_state)
            y_samples.append(sample_objective)
            
            if sample_objective > best_objective:
                best_state = sample_state
                best_objective = sample_objective
        
        return best_state, best_objective
    
    async def _genetic_algorithm_optimization(self, initial_state: np.ndarray, quantum_system: QuantumSystem,
                                            objectives: List[OptimizationObjective]) -> Tuple[np.ndarray, float]:
        """Genetic algorithm optimization"""
        population_size = min(self.population_size, 30)  # Limit for performance
        population = []
        
        # Initialize population
        for _ in range(population_size):
            individual = initial_state + np.random.normal(0, 0.3, size=initial_state.shape)
            individual = np.clip(individual, 0, 1)
            population.append(individual)
        
        best_state = initial_state.copy()
        best_objective = await self._evaluate_objectives(quantum_system, objectives)
        
        # Evolution loop
        for generation in range(20):  # Limited generations for performance
            # Evaluate population
            fitness_scores = []
            for individual in population:
                individual_system = self._decode_system_state(individual, quantum_system)
                fitness = await self._evaluate_objectives(individual_system, objectives)
                fitness_scores.append(fitness)
                
                if fitness > best_objective:
                    best_state = individual.copy()
                    best_objective = fitness
            
            # Selection and reproduction (simplified)
            # Keep top 50% and generate new 50%
            sorted_indices = np.argsort(fitness_scores)[::-1]
            elite_count = population_size // 2
            
            new_population = []
            # Keep elite
            for i in range(elite_count):
                new_population.append(population[sorted_indices[i]])
            
            # Generate offspring
            for _ in range(population_size - elite_count):
                parent1 = population[sorted_indices[random.randint(0, elite_count - 1)]]
                parent2 = population[sorted_indices[random.randint(0, elite_count - 1)]]
                
                # Crossover and mutation
                child = (parent1 + parent2) / 2 + np.random.normal(0, 0.1, size=parent1.shape)
                child = np.clip(child, 0, 1)
                new_population.append(child)
            
            population = new_population
        
        return best_state, best_objective
    
    async def _quantum_annealing_simulation(self, initial_state: np.ndarray, quantum_system: QuantumSystem,
                                          objectives: List[OptimizationObjective]) -> Tuple[np.ndarray, float]:
        """Simulated quantum annealing"""
        current_state = initial_state.copy()
        current_objective = await self._evaluate_objectives(quantum_system, objectives)
        
        best_state = current_state.copy()
        best_objective = current_objective
        
        temperature = self.temperature
        cooling_rate = 0.95
        
        for iteration in range(100):
            # Generate neighbor state
            neighbor_state = current_state + np.random.normal(0, temperature * 0.1, size=current_state.shape)
            neighbor_state = np.clip(neighbor_state, 0, 1)
            
            # Evaluate neighbor
            neighbor_system = self._decode_system_state(neighbor_state, quantum_system)
            neighbor_objective = await self._evaluate_objectives(neighbor_system, objectives)
            
            # Accept or reject based on simulated annealing criteria
            delta = neighbor_objective - current_objective
            if delta > 0 or np.random.random() < np.exp(delta / temperature):
                current_state = neighbor_state
                current_objective = neighbor_objective
                
                if neighbor_objective > best_objective:
                    best_state = neighbor_state.copy()
                    best_objective = neighbor_objective
            
            # Cool down
            temperature *= cooling_rate
        
        return best_state, best_objective
    
    async def _gradient_descent_optimization(self, initial_state: np.ndarray, quantum_system: QuantumSystem,
                                           objectives: List[OptimizationObjective]) -> Tuple[np.ndarray, float]:
        """Gradient descent optimization"""
        current_state = initial_state.copy()
        learning_rate = self.learning_rate
        
        for iteration in range(50):
            # Numerical gradient estimation
            gradient = np.zeros_like(current_state)
            epsilon = 1e-6
            
            current_objective = await self._evaluate_objectives(
                self._decode_system_state(current_state, quantum_system), objectives
            )
            
            for i in range(len(current_state)):
                # Forward difference
                perturbed_state = current_state.copy()
                perturbed_state[i] += epsilon
                perturbed_state = np.clip(perturbed_state, 0, 1)
                
                perturbed_system = self._decode_system_state(perturbed_state, quantum_system)
                perturbed_objective = await self._evaluate_objectives(perturbed_system, objectives)
                
                gradient[i] = (perturbed_objective - current_objective) / epsilon
            
            # Update state
            current_state += learning_rate * gradient
            current_state = np.clip(current_state, 0, 1)
        
        final_objective = await self._evaluate_objectives(
            self._decode_system_state(current_state, quantum_system), objectives
        )
        
        return current_state, final_objective
    
    async def _optimize_win_parameters(self, parameters: Dict[str, float], 
                                     constraints: Dict[str, Any]) -> Dict[str, float]:
        """Optimize WIN probability parameters"""
        # Simple parameter optimization
        optimal_params = parameters.copy()
        
        # Increase superposition factor if not constrained
        if "max_superposition" not in constraints:
            optimal_params["superposition_factor"] = min(1.0, parameters["superposition_factor"] * 1.2)
        
        # Increase entanglement boost
        if "max_entanglement" not in constraints:
            optimal_params["entanglement_boost"] = min(0.5, parameters["entanglement_boost"] * 1.15)
        
        # Calculate optimized quantum probability
        base_prob = 0.5  # Placeholder
        optimal_params["quantum_probability"] = min(1.0, 
            base_prob + optimal_params["superposition_factor"] + optimal_params["entanglement_boost"]
        )
        
        return optimal_params
    
    async def _calculate_solution_confidence(self, quantum_system: QuantumSystem, 
                                           objectives: List[OptimizationObjective]) -> float:
        """Calculate confidence in optimization solution"""
        # Based on system coherence and objective achievement
        coherence_factor = quantum_system.total_coherence
        
        # Check objective achievement
        objective_achievement = 0.0
        for objective in objectives:
            if objective.target_value is not None:
                current_value = quantum_system.total_coherence  # Simplified
                achievement = min(1.0, current_value / objective.target_value)
                objective_achievement += objective.weight * achievement
        
        if objectives:
            objective_achievement /= sum(obj.weight for obj in objectives)
        
        return (coherence_factor + objective_achievement) / 2
    
    async def _calculate_robustness_score(self, quantum_system: QuantumSystem,
                                        objectives: List[OptimizationObjective]) -> float:
        """Calculate solution robustness score"""
        # Test robustness by perturbing system and measuring objective stability
        base_objective = await self._evaluate_objectives(quantum_system, objectives)
        
        perturbation_scores = []
        for _ in range(5):  # Limited perturbations for performance
            # Create perturbed system
            perturbed_system = QuantumSystem(
                system_id=f"perturbed_{quantum_system.system_id}",
                quantum_states=quantum_system.quantum_states.copy(),
                state_transitions=quantum_system.state_transitions.copy()
            )
            
            # Add small perturbations to state probabilities
            for state in perturbed_system.quantum_states.values():
                perturbation = np.random.normal(0, 0.05)
                state.probability = max(0.0, min(1.0, state.probability + perturbation))
                state.amplitude = complex(np.sqrt(state.probability), 0.0)
            
            # Evaluate perturbed objective
            perturbed_objective = await self._evaluate_objectives(perturbed_system, objectives)
            
            # Calculate stability
            if base_objective != 0:
                stability = 1.0 - abs(perturbed_objective - base_objective) / abs(base_objective)
            else:
                stability = 1.0 if perturbed_objective == 0 else 0.0
            
            perturbation_scores.append(max(0.0, stability))
        
        return np.mean(perturbation_scores)
    
    async def _generate_ml_insights(self, quantum_system: QuantumSystem) -> Dict[str, Any]:
        """Generate ML-powered insights about optimized system"""
        insights = {}
        
        if self.models_trained:
            # Encode system state
            state_features = self._encode_system_state(quantum_system)
            
            # Predict objective value
            predicted_objective = self.objective_predictor.predict([state_features])[0]
            objective_uncertainty = np.sqrt(self.objective_predictor.predict([state_features], return_std=True)[1][0])
            
            insights["predicted_objective"] = predicted_objective
            insights["prediction_uncertainty"] = objective_uncertainty
            insights["prediction_confidence"] = max(0.0, 1.0 - objective_uncertainty)
        
        return insights
    
    async def _calculate_feature_importance(self, state_vector: np.ndarray) -> Dict[str, float]:
        """Calculate feature importance for optimization"""
        feature_names = [
            "total_coherence", "system_entropy", "state_count", "transition_count", "entanglement_count",
            "mean_probability", "std_probability", "max_probability", "min_probability",
            "mean_transition_prob", "std_transition_prob", "max_transition_prob", "min_transition_prob"
        ]
        
        # Simple importance based on feature magnitudes
        importance = {}
        for i, name in enumerate(feature_names[:len(state_vector)]):
            importance[name] = abs(state_vector[i])
        
        # Normalize importance scores
        total_importance = sum(importance.values())
        if total_importance > 0:
            importance = {k: v / total_importance for k, v in importance.items()}
        
        return importance
    
    async def _learn_from_optimization(self, quantum_system: QuantumSystem, 
                                     objectives: List[OptimizationObjective],
                                     result: OptimizationResult) -> None:
        """Learn from optimization experience"""
        try:
            experience = LearningExperience(
                experience_type=ExperienceType.PERFORMANCE_OPTIMIZATION,
                agent_id="quantum_optimization_engine",
                context={
                    "initial_coherence": quantum_system.total_coherence,
                    "state_count": len(quantum_system.quantum_states),
                    "objective_count": len(objectives),
                    "optimization_time": result.optimization_time
                },
                action_taken={
                    "action": "optimize_quantum_system",
                    "optimization_method": "hybrid_ml_optimization",
                    "iterations": result.convergence_iterations
                },
                outcome={
                    "objective_value": result.objective_value,
                    "improvement_ratio": result.improvement_ratio,
                    "solution_confidence": result.solution_confidence,
                    "robustness_score": result.robustness_score,
                    "success": result.improvement_ratio > 0
                },
                success=result.improvement_ratio > 0,
                duration_seconds=result.optimization_time,
                confidence_level=result.solution_confidence,
                importance_weight=1.0
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
                    "parameters_optimized": ["superposition_factor", "entanglement_boost", "time_sensitivity"]
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
    
    async def _learn_from_model_training(self, training_result: Dict[str, Any]) -> None:
        """Learn from ML model training"""
        try:
            experience = LearningExperience(
                experience_type=ExperienceType.PERFORMANCE_OPTIMIZATION,
                agent_id="quantum_optimization_engine",
                context={
                    "training_samples": training_result["training_samples"],
                    "feature_count": training_result["feature_count"]
                },
                action_taken={
                    "action": "train_optimization_models",
                    "models": ["objective_predictor", "constraint_predictor"]
                },
                outcome={
                    "objective_prediction_r2": training_result["objective_prediction_r2"],
                    "constraint_prediction_r2": training_result["constraint_prediction_r2"],
                    "models_trained": training_result["models_trained"],
                    "success": training_result["models_trained"]
                },
                success=training_result["models_trained"],
                confidence_level=training_result["objective_prediction_r2"],
                importance_weight=1.0
            )
            
            await self.learning_system.learn_from_experience(experience)
        except Exception as e:
            print(f"Model training learning error: {e}")
    
    async def _update_performance_metrics(self) -> None:
        """Update optimization performance metrics"""
        if not self.optimization_history:
            return
        
        recent_results = self.optimization_history[-10:]  # Last 10 optimizations
        
        # Calculate metrics
        improvements = [r.improvement_ratio for r in recent_results]
        self.performance_metrics["average_improvement"] = np.mean(improvements)
        self.performance_metrics["success_rate"] = sum(1 for imp in improvements if imp > 0) / len(improvements)
        
        convergence_times = [r.optimization_time for r in recent_results]
        self.performance_metrics["average_convergence_time"] = np.mean(convergence_times) 