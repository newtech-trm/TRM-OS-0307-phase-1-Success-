"""
WIN Probability Calculator - Advanced ML-Enhanced WIN Probability Computation
Tính toán WIN probabilities với machine learning và contextual analysis
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import numpy as np
from uuid import uuid4
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import joblib

from ..learning.adaptive_learning_system import AdaptiveLearningSystem
from ..learning.learning_types import LearningExperience, ExperienceType
from ..eventbus.system_event_bus import publish_event
from ..models.event import EventType
from .quantum_types import (
    QuantumState, QuantumSystem, WINProbability, WINCategory,
    ProbabilityDistribution, QuantumStateType
)


class WINFactorType(Enum):
    """Types of WIN contributing factors"""
    SYSTEM_COHERENCE = "system_coherence"
    TEAM_PERFORMANCE = "team_performance"
    RESOURCE_AVAILABILITY = "resource_availability"
    LEARNING_PROGRESS = "learning_progress"
    ADAPTATION_SUCCESS = "adaptation_success"
    COMMUNICATION_EFFECTIVENESS = "communication_effectiveness"
    INNOVATION_CAPACITY = "innovation_capacity"
    RISK_MITIGATION = "risk_mitigation"
    STAKEHOLDER_SATISFACTION = "stakeholder_satisfaction"
    STRATEGIC_ALIGNMENT = "strategic_alignment"


@dataclass
class WINFactor:
    """Individual factor contributing to WIN probability"""
    factor_id: str
    factor_type: WINFactorType
    name: str
    description: str
    current_value: float
    weight: float
    confidence: float
    trend: str = "stable"  # improving, declining, stable
    impact_score: float = 0.0
    
    def calculate_contribution(self) -> float:
        """Calculate factor's contribution to WIN probability"""
        base_contribution = self.current_value * self.weight * self.confidence
        
        # Apply trend adjustment
        if self.trend == "improving":
            base_contribution *= 1.1
        elif self.trend == "declining":
            base_contribution *= 0.9
        
        return min(1.0, max(0.0, base_contribution))


@dataclass
class WINScenario:
    """WIN probability scenario with different conditions"""
    scenario_id: str
    name: str
    description: str
    conditions: Dict[str, Any]
    probability: float
    confidence: float
    factors: List[WINFactor]
    timeline: str = "short_term"  # short_term, medium_term, long_term
    
    def calculate_scenario_probability(self) -> float:
        """Calculate overall scenario probability"""
        if not self.factors:
            return self.probability
        
        factor_contributions = [factor.calculate_contribution() for factor in self.factors]
        weighted_average = np.average(factor_contributions, weights=[f.weight for f in self.factors])
        
        # Combine with base probability
        combined_probability = (self.probability + weighted_average) / 2
        
        return min(1.0, max(0.0, combined_probability))


class WINProbabilityCalculator:
    """
    Advanced WIN Probability Calculator với ML-Enhanced Calculations
    Tính toán WIN probabilities với contextual analysis và machine learning
    """
    
    def __init__(self, learning_system: AdaptiveLearningSystem):
        self.learning_system = learning_system
        self.logger = logging.getLogger(__name__)
        
        # ML models
        self.probability_predictor = RandomForestRegressor(n_estimators=100, random_state=42)
        self.factor_analyzer = RandomForestRegressor(n_estimators=50, random_state=42)
        self.scaler = StandardScaler()
        
        # WIN factors và scenarios
        self.win_factors: Dict[str, WINFactor] = {}
        self.win_scenarios: Dict[str, WINScenario] = {}
        self.probability_history: List[WINProbability] = []
        
        # Configuration
        self.default_factor_weights = {
            WINFactorType.SYSTEM_COHERENCE: 0.15,
            WINFactorType.TEAM_PERFORMANCE: 0.12,
            WINFactorType.RESOURCE_AVAILABILITY: 0.10,
            WINFactorType.LEARNING_PROGRESS: 0.08,
            WINFactorType.ADAPTATION_SUCCESS: 0.08,
            WINFactorType.COMMUNICATION_EFFECTIVENESS: 0.10,
            WINFactorType.INNOVATION_CAPACITY: 0.07,
            WINFactorType.RISK_MITIGATION: 0.10,
            WINFactorType.STAKEHOLDER_SATISFACTION: 0.12,
            WINFactorType.STRATEGIC_ALIGNMENT: 0.08
        }
        
        # Models training status
        self.models_trained = False
        self.training_data_size = 0
        
        # Statistics
        self.calculation_stats = {
            "total_calculations": 0,
            "average_probability": 0.0,
            "prediction_accuracy": 0.0,
            "factor_analysis_count": 0,
            "scenario_evaluations": 0
        }
        
        self.logger.info("WINProbabilityCalculator initialized")
    
    async def initialize(self) -> None:
        """Initialize WIN probability calculator"""
        
        try:
            # Setup default WIN factors
            await self._setup_default_factors()
            
            # Create default scenarios
            await self._create_default_scenarios()
            
            # Initialize ML models với synthetic data
            await self._initialize_ml_models()
            
            self.logger.info("WINProbabilityCalculator initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize WINProbabilityCalculator: {e}")
            raise
    
    async def calculate_win_probability(
        self,
        quantum_system: QuantumSystem,
        win_category: WINCategory = WINCategory.COMPOSITE,
        context: Dict[str, Any] = None,
        scenario_id: str = None
    ) -> WINProbability:
        """Calculate WIN probability cho quantum system"""
        
        try:
            # Get current system state
            current_factors = await self._analyze_current_factors(quantum_system, context)
            
            # Base probability calculation
            base_probability = await self._calculate_base_probability(
                quantum_system, win_category, current_factors
            )
            
            # Apply scenario-specific adjustments
            if scenario_id and scenario_id in self.win_scenarios:
                scenario = self.win_scenarios[scenario_id]
                scenario_probability = scenario.calculate_scenario_probability()
                base_probability = (base_probability + scenario_probability) / 2
            
            # ML-enhanced prediction
            if self.models_trained:
                ml_probability = await self._predict_with_ml(quantum_system, current_factors)
                base_probability = (base_probability + ml_probability) / 2
            
            # Calculate confidence
            confidence = await self._calculate_confidence(current_factors, base_probability)
            
            # Create WIN probability object
            win_probability = WINProbability(
                probability_id=str(uuid4()),
                win_category=win_category,
                base_probability=base_probability,
                confidence_level=confidence,
                contributing_factors={
                    factor.factor_id: factor.calculate_contribution() 
                    for factor in current_factors
                },
                calculation_context=context or {},
                timestamp=datetime.now()
            )
            
            # Store in history
            self.probability_history.append(win_probability)
            
            # Update statistics
            self._update_calculation_stats(win_probability)
            
            # Learn from calculation
            await self._learn_from_calculation(win_probability, current_factors)
            
            # Record event
            await publish_event(
                event_type=EventType.KNOWLEDGE_CREATED,
                source_agent_id="win_probability_calculator",
                entity_id=win_probability.probability_id,
                entity_type="win_probability",
                data={
                    "win_category": win_category.value,
                    "base_probability": base_probability,
                    "confidence": confidence,
                    "factors_count": len(current_factors)
                }
            )
            
            return win_probability
            
        except Exception as e:
            self.logger.error(f"Failed to calculate WIN probability: {e}")
            raise
    
    async def analyze_win_factors(
        self,
        quantum_system: QuantumSystem,
        context: Dict[str, Any] = None
    ) -> List[WINFactor]:
        """Analyze current WIN factors"""
        
        try:
            factors = []
            
            # System coherence factor
            coherence_factor = await self._analyze_coherence_factor(quantum_system)
            factors.append(coherence_factor)
            
            # Performance factors
            performance_factors = await self._analyze_performance_factors(quantum_system)
            factors.extend(performance_factors)
            
            # Learning factors
            learning_factors = await self._analyze_learning_factors()
            factors.extend(learning_factors)
            
            # Context-specific factors
            if context:
                context_factors = await self._analyze_context_factors(context)
                factors.extend(context_factors)
            
            # Update factor trends
            await self._update_factor_trends(factors)
            
            # Store factors
            for factor in factors:
                self.win_factors[factor.factor_id] = factor
            
            self.calculation_stats["factor_analysis_count"] += 1
            
            return factors
            
        except Exception as e:
            self.logger.error(f"Failed to analyze WIN factors: {e}")
            return []
    
    async def create_win_scenario(
        self,
        name: str,
        description: str,
        conditions: Dict[str, Any],
        factors: List[WINFactor] = None
    ) -> WINScenario:
        """Create new WIN scenario"""
        
        scenario_id = str(uuid4())
        
        # Calculate base probability từ conditions
        base_probability = await self._calculate_scenario_base_probability(conditions)
        
        # Calculate confidence
        confidence = await self._calculate_scenario_confidence(conditions, factors or [])
        
        scenario = WINScenario(
            scenario_id=scenario_id,
            name=name,
            description=description,
            conditions=conditions,
            probability=base_probability,
            confidence=confidence,
            factors=factors or []
        )
        
        self.win_scenarios[scenario_id] = scenario
        
        self.logger.info(f"Created WIN scenario: {name} ({scenario_id})")
        
        return scenario
    
    async def evaluate_scenario(
        self,
        scenario_id: str,
        quantum_system: QuantumSystem,
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Evaluate WIN scenario against current system state"""
        
        if scenario_id not in self.win_scenarios:
            raise ValueError(f"Scenario not found: {scenario_id}")
        
        try:
            scenario = self.win_scenarios[scenario_id]
            
            # Get current factors
            current_factors = await self._analyze_current_factors(quantum_system, context)
            
            # Calculate scenario probability
            scenario_probability = scenario.calculate_scenario_probability()
            
            # Compare với current state
            current_probability = await self._calculate_base_probability(
                quantum_system, WINCategory.COMPOSITE, current_factors
            )
            
            # Calculate gap analysis
            gap_analysis = await self._calculate_scenario_gap(
                scenario, current_factors, quantum_system
            )
            
            # Recommendations
            recommendations = await self._generate_scenario_recommendations(
                scenario, gap_analysis
            )
            
            evaluation_result = {
                "scenario_id": scenario_id,
                "scenario_name": scenario.name,
                "scenario_probability": scenario_probability,
                "current_probability": current_probability,
                "probability_gap": scenario_probability - current_probability,
                "gap_analysis": gap_analysis,
                "recommendations": recommendations,
                "feasibility": await self._assess_scenario_feasibility(scenario, current_factors)
            }
            
            self.calculation_stats["scenario_evaluations"] += 1
            
            return evaluation_result
            
        except Exception as e:
            self.logger.error(f"Failed to evaluate scenario: {e}")
            raise
    
    async def get_win_probability_trends(
        self,
        days: int = 30,
        win_category: WINCategory = None
    ) -> Dict[str, Any]:
        """Get WIN probability trends over time"""
        
        cutoff_date = datetime.now() - timedelta(days=days)
        
        # Filter history
        relevant_history = [
            prob for prob in self.probability_history
            if prob.timestamp >= cutoff_date and 
            (win_category is None or prob.win_category == win_category)
        ]
        
        if not relevant_history:
            return {"error": "No data available for specified period"}
        
        # Calculate trends
        probabilities = [prob.base_probability for prob in relevant_history]
        confidences = [prob.confidence_level for prob in relevant_history]
        timestamps = [prob.timestamp for prob in relevant_history]
        
        # Trend analysis
        trend_analysis = {
            "period_days": days,
            "data_points": len(relevant_history),
            "average_probability": np.mean(probabilities),
            "probability_std": np.std(probabilities),
            "min_probability": np.min(probabilities),
            "max_probability": np.max(probabilities),
            "average_confidence": np.mean(confidences),
            "trend_direction": self._calculate_trend_direction(probabilities),
            "volatility": np.std(probabilities) / np.mean(probabilities) if np.mean(probabilities) > 0 else 0,
            "improvement_rate": self._calculate_improvement_rate(probabilities, timestamps)
        }
        
        return trend_analysis
    
    def get_calculation_statistics(self) -> Dict[str, Any]:
        """Get calculation statistics"""
        
        return {
            **self.calculation_stats,
            "models_trained": self.models_trained,
            "training_data_size": self.training_data_size,
            "factors_count": len(self.win_factors),
            "scenarios_count": len(self.win_scenarios),
            "history_size": len(self.probability_history)
        }
    
    # Private methods
    
    async def _setup_default_factors(self) -> None:
        """Setup default WIN factors"""
        
        default_factors = [
            WINFactor(
                factor_id="system_coherence",
                factor_type=WINFactorType.SYSTEM_COHERENCE,
                name="System Coherence",
                description="Overall quantum system coherence",
                current_value=0.75,
                weight=self.default_factor_weights[WINFactorType.SYSTEM_COHERENCE],
                confidence=0.8
            ),
            WINFactor(
                factor_id="team_performance",
                factor_type=WINFactorType.TEAM_PERFORMANCE,
                name="Team Performance",
                description="Overall team performance metrics",
                current_value=0.68,
                weight=self.default_factor_weights[WINFactorType.TEAM_PERFORMANCE],
                confidence=0.7
            ),
            WINFactor(
                factor_id="learning_progress",
                factor_type=WINFactorType.LEARNING_PROGRESS,
                name="Learning Progress",
                description="Adaptive learning system progress",
                current_value=0.72,
                weight=self.default_factor_weights[WINFactorType.LEARNING_PROGRESS],
                confidence=0.85
            )
        ]
        
        for factor in default_factors:
            self.win_factors[factor.factor_id] = factor
        
        self.logger.info("Default WIN factors setup completed")
    
    async def _create_default_scenarios(self) -> None:
        """Create default WIN scenarios"""
        
        # High performance scenario
        high_perf_scenario = await self.create_win_scenario(
            name="High Performance State",
            description="Scenario where all systems operate at peak performance",
            conditions={
                "system_coherence": 0.9,
                "team_performance": 0.85,
                "resource_availability": 0.8,
                "learning_progress": 0.9
            }
        )
        
        # Innovation scenario
        innovation_scenario = await self.create_win_scenario(
            name="Innovation Breakthrough",
            description="Scenario focused on innovation and breakthrough achievements",
            conditions={
                "innovation_capacity": 0.9,
                "learning_progress": 0.85,
                "communication_effectiveness": 0.8,
                "strategic_alignment": 0.75
            }
        )
        
        # Stability scenario
        stability_scenario = await self.create_win_scenario(
            name="Stable Operations",
            description="Scenario focused on stable, consistent operations",
            conditions={
                "system_coherence": 0.8,
                "risk_mitigation": 0.9,
                "resource_availability": 0.85,
                "stakeholder_satisfaction": 0.8
            }
        )
        
        self.logger.info("Default WIN scenarios created")
    
    async def _initialize_ml_models(self) -> None:
        """Initialize ML models với synthetic training data"""
        
        try:
            # Generate synthetic training data
            training_data = await self._generate_synthetic_training_data(1000)
            
            if training_data:
                X, y = training_data
                
                # Scale features
                X_scaled = self.scaler.fit_transform(X)
                
                # Train models
                self.probability_predictor.fit(X_scaled, y)
                self.factor_analyzer.fit(X_scaled, y)
                
                self.models_trained = True
                self.training_data_size = len(X)
                
                self.logger.info(f"ML models trained with {len(X)} samples")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize ML models: {e}")
    
    async def _generate_synthetic_training_data(self, size: int) -> Tuple[np.ndarray, np.ndarray]:
        """Generate synthetic training data cho ML models"""
        
        np.random.seed(42)
        
        # Features: system_coherence, team_performance, learning_progress, etc.
        features = []
        targets = []
        
        for _ in range(size):
            # Random feature values
            coherence = np.random.beta(2, 2)
            performance = np.random.beta(2, 2)
            learning = np.random.beta(2, 2)
            resources = np.random.beta(2, 2)
            communication = np.random.beta(2, 2)
            
            feature_vector = [coherence, performance, learning, resources, communication]
            features.append(feature_vector)
            
            # Target WIN probability (synthetic function)
            win_prob = (
                coherence * 0.3 + 
                performance * 0.25 + 
                learning * 0.2 + 
                resources * 0.15 + 
                communication * 0.1 +
                np.random.normal(0, 0.05)  # Noise
            )
            win_prob = max(0, min(1, win_prob))  # Clamp to [0, 1]
            targets.append(win_prob)
        
        return np.array(features), np.array(targets)
    
    async def _analyze_current_factors(
        self,
        quantum_system: QuantumSystem,
        context: Dict[str, Any] = None
    ) -> List[WINFactor]:
        """Analyze current WIN factors"""
        
        factors = []
        
        # System coherence
        coherence = quantum_system.calculate_system_coherence()
        coherence_factor = WINFactor(
            factor_id="current_coherence",
            factor_type=WINFactorType.SYSTEM_COHERENCE,
            name="Current System Coherence",
            description="Current quantum system coherence level",
            current_value=coherence,
            weight=self.default_factor_weights[WINFactorType.SYSTEM_COHERENCE],
            confidence=0.9
        )
        factors.append(coherence_factor)
        
        # Learning progress
        learning_stats = self.learning_system.get_statistics()
        learning_progress = learning_stats.get("learning_effectiveness", 0.0)
        learning_factor = WINFactor(
            factor_id="current_learning",
            factor_type=WINFactorType.LEARNING_PROGRESS,
            name="Current Learning Progress",
            description="Current adaptive learning progress",
            current_value=learning_progress,
            weight=self.default_factor_weights[WINFactorType.LEARNING_PROGRESS],
            confidence=0.85
        )
        factors.append(learning_factor)
        
        # Context-based factors
        if context:
            for key, value in context.items():
                if isinstance(value, (int, float)) and 0 <= value <= 1:
                    factor = WINFactor(
                        factor_id=f"context_{key}",
                        factor_type=WINFactorType.STRATEGIC_ALIGNMENT,
                        name=f"Context {key}",
                        description=f"Context-based factor: {key}",
                        current_value=value,
                        weight=0.05,
                        confidence=0.6
                    )
                    factors.append(factor)
        
        return factors
    
    async def _calculate_base_probability(
        self,
        quantum_system: QuantumSystem,
        win_category: WINCategory,
        factors: List[WINFactor]
    ) -> float:
        """Calculate base WIN probability"""
        
        if not factors:
            return 0.5  # Default probability
        
        # Weighted average of factor contributions
        contributions = [factor.calculate_contribution() for factor in factors]
        weights = [factor.weight for factor in factors]
        
        if sum(weights) == 0:
            return np.mean(contributions)
        
        weighted_probability = np.average(contributions, weights=weights)
        
        # Category-specific adjustments
        if win_category == WINCategory.WISDOM:
            weighted_probability *= 0.9  # Wisdom is harder to achieve
        elif win_category == WINCategory.INTELLIGENCE:
            weighted_probability *= 1.1  # Intelligence is more achievable
        elif win_category == WINCategory.NETWORKING:
            weighted_probability *= 1.05  # Networking benefits from connections
        
        return min(1.0, max(0.0, weighted_probability))
    
    async def _predict_with_ml(
        self,
        quantum_system: QuantumSystem,
        factors: List[WINFactor]
    ) -> float:
        """Predict WIN probability using ML models"""
        
        try:
            # Prepare feature vector
            feature_vector = [
                quantum_system.calculate_system_coherence(),
                np.mean([f.current_value for f in factors]),
                len(factors),
                np.mean([f.confidence for f in factors]),
                quantum_system.system_entropy
            ]
            
            # Scale features
            feature_vector_scaled = self.scaler.transform([feature_vector])
            
            # Predict
            prediction = self.probability_predictor.predict(feature_vector_scaled)[0]
            
            return max(0.0, min(1.0, prediction))
            
        except Exception as e:
            self.logger.error(f"Failed to predict with ML: {e}")
            return 0.5
    
    async def _calculate_confidence(
        self,
        factors: List[WINFactor],
        probability: float
    ) -> float:
        """Calculate confidence in WIN probability"""
        
        if not factors:
            return 0.5
        
        # Base confidence from factors
        factor_confidences = [f.confidence for f in factors]
        base_confidence = np.mean(factor_confidences)
        
        # Adjust based on probability extremes
        if probability < 0.1 or probability > 0.9:
            base_confidence *= 0.8  # Less confident at extremes
        
        # Adjust based on factor consistency
        factor_values = [f.current_value for f in factors]
        if len(factor_values) > 1:
            consistency = 1.0 - np.std(factor_values)
            base_confidence *= (0.5 + consistency * 0.5)
        
        return max(0.1, min(0.95, base_confidence))
    
    def _update_calculation_stats(self, win_probability: WINProbability) -> None:
        """Update calculation statistics"""
        
        self.calculation_stats["total_calculations"] += 1
        
        # Update average probability
        total_prob = (self.calculation_stats["average_probability"] * 
                     (self.calculation_stats["total_calculations"] - 1) + 
                     win_probability.base_probability)
        self.calculation_stats["average_probability"] = total_prob / self.calculation_stats["total_calculations"]
    
    async def _learn_from_calculation(
        self,
        win_probability: WINProbability,
        factors: List[WINFactor]
    ) -> None:
        """Learn from WIN probability calculation"""
        
        try:
            # Create learning experience
            experience = LearningExperience(
                agent_id="win_probability_calculator",
                experience_type=ExperienceType.WIN_PROBABILITY_CALCULATION,
                action_taken={
                    "action": "calculate_win_probability",
                    "win_category": win_probability.win_category.value,
                    "factors_count": len(factors)
                },
                outcome={
                    "probability": win_probability.base_probability,
                    "confidence": win_probability.confidence_level,
                    "contributing_factors": win_probability.contributing_factors
                },
                success=True,
                confidence=win_probability.confidence_level,
                context={
                    "calculation_context": win_probability.calculation_context,
                    "factors": [f.factor_id for f in factors]
                }
            )
            
            # Add to learning system
            await self.learning_system.learn_from_experience(experience)
            
        except Exception as e:
            self.logger.error(f"Failed to learn from calculation: {e}")
    
    def _calculate_trend_direction(self, probabilities: List[float]) -> str:
        """Calculate trend direction từ probability history"""
        
        if len(probabilities) < 2:
            return "stable"
        
        # Simple linear trend
        x = np.arange(len(probabilities))
        slope = np.polyfit(x, probabilities, 1)[0]
        
        if slope > 0.01:
            return "improving"
        elif slope < -0.01:
            return "declining"
        else:
            return "stable"
    
    def _calculate_improvement_rate(
        self,
        probabilities: List[float],
        timestamps: List[datetime]
    ) -> float:
        """Calculate improvement rate over time"""
        
        if len(probabilities) < 2:
            return 0.0
        
        # Calculate rate of change
        time_diff = (timestamps[-1] - timestamps[0]).total_seconds() / 3600  # Hours
        prob_diff = probabilities[-1] - probabilities[0]
        
        if time_diff > 0:
            return prob_diff / time_diff
        else:
            return 0.0
    
    async def _analyze_coherence_factor(self, quantum_system: QuantumSystem) -> WINFactor:
        """Analyze system coherence factor"""
        
        coherence = quantum_system.calculate_system_coherence()
        
        return WINFactor(
            factor_id="coherence_analysis",
            factor_type=WINFactorType.SYSTEM_COHERENCE,
            name="System Coherence Analysis",
            description="Detailed analysis of quantum system coherence",
            current_value=coherence,
            weight=self.default_factor_weights[WINFactorType.SYSTEM_COHERENCE],
            confidence=0.9,
            trend="stable",
            impact_score=coherence * 0.15
        )
    
    async def _analyze_performance_factors(self, quantum_system: QuantumSystem) -> List[WINFactor]:
        """Analyze performance-related factors"""
        
        factors = []
        
        # Team performance (mock data)
        team_performance = WINFactor(
            factor_id="team_performance_analysis",
            factor_type=WINFactorType.TEAM_PERFORMANCE,
            name="Team Performance Analysis",
            description="Analysis of team performance metrics",
            current_value=0.72,
            weight=self.default_factor_weights[WINFactorType.TEAM_PERFORMANCE],
            confidence=0.8,
            trend="improving"
        )
        factors.append(team_performance)
        
        # Resource availability (mock data)
        resource_availability = WINFactor(
            factor_id="resource_availability_analysis",
            factor_type=WINFactorType.RESOURCE_AVAILABILITY,
            name="Resource Availability Analysis",
            description="Analysis of resource availability and utilization",
            current_value=0.68,
            weight=self.default_factor_weights[WINFactorType.RESOURCE_AVAILABILITY],
            confidence=0.7,
            trend="stable"
        )
        factors.append(resource_availability)
        
        return factors
    
    async def _analyze_learning_factors(self) -> List[WINFactor]:
        """Analyze learning-related factors"""
        
        factors = []
        
        # Get learning statistics
        learning_stats = self.learning_system.get_statistics()
        
        # Learning progress
        learning_progress = WINFactor(
            factor_id="learning_progress_analysis",
            factor_type=WINFactorType.LEARNING_PROGRESS,
            name="Learning Progress Analysis",
            description="Analysis of adaptive learning progress",
            current_value=learning_stats.get("learning_effectiveness", 0.0),
            weight=self.default_factor_weights[WINFactorType.LEARNING_PROGRESS],
            confidence=0.85,
            trend="improving"
        )
        factors.append(learning_progress)
        
        # Adaptation success
        adaptation_success = WINFactor(
            factor_id="adaptation_success_analysis",
            factor_type=WINFactorType.ADAPTATION_SUCCESS,
            name="Adaptation Success Analysis",
            description="Analysis of behavioral adaptation success",
            current_value=learning_stats.get("adaptation_success_rate", 0.0),
            weight=self.default_factor_weights[WINFactorType.ADAPTATION_SUCCESS],
            confidence=0.8,
            trend="stable"
        )
        factors.append(adaptation_success)
        
        return factors
    
    async def _analyze_context_factors(self, context: Dict[str, Any]) -> List[WINFactor]:
        """Analyze context-specific factors"""
        
        factors = []
        
        # Convert context items to factors
        for key, value in context.items():
            if isinstance(value, (int, float)) and 0 <= value <= 1:
                factor = WINFactor(
                    factor_id=f"context_{key}",
                    factor_type=WINFactorType.STRATEGIC_ALIGNMENT,
                    name=f"Context: {key}",
                    description=f"Context-based factor from {key}",
                    current_value=value,
                    weight=0.05,
                    confidence=0.6,
                    trend="stable"
                )
                factors.append(factor)
        
        return factors
    
    async def _update_factor_trends(self, factors: List[WINFactor]) -> None:
        """Update factor trends based on history"""
        
        # This would analyze historical factor values to determine trends
        # For now, using simple heuristics
        
        for factor in factors:
            # Mock trend analysis
            if factor.current_value > 0.8:
                factor.trend = "improving"
            elif factor.current_value < 0.4:
                factor.trend = "declining"
            else:
                factor.trend = "stable"
    
    async def _calculate_scenario_base_probability(self, conditions: Dict[str, Any]) -> float:
        """Calculate base probability for scenario"""
        
        if not conditions:
            return 0.5
        
        # Average of condition values
        values = [v for v in conditions.values() if isinstance(v, (int, float))]
        
        if values:
            return np.mean(values)
        else:
            return 0.5
    
    async def _calculate_scenario_confidence(
        self,
        conditions: Dict[str, Any],
        factors: List[WINFactor]
    ) -> float:
        """Calculate confidence for scenario"""
        
        # Base confidence from conditions
        base_confidence = 0.7
        
        # Adjust based on factors
        if factors:
            factor_confidences = [f.confidence for f in factors]
            base_confidence = np.mean(factor_confidences)
        
        # Adjust based on condition realism
        condition_values = [v for v in conditions.values() if isinstance(v, (int, float))]
        if condition_values:
            # Lower confidence for extreme values
            extreme_penalty = sum(1 for v in condition_values if v > 0.9 or v < 0.1) * 0.1
            base_confidence = max(0.1, base_confidence - extreme_penalty)
        
        return base_confidence
    
    async def _calculate_scenario_gap(
        self,
        scenario: WINScenario,
        current_factors: List[WINFactor],
        quantum_system: QuantumSystem
    ) -> Dict[str, Any]:
        """Calculate gap between scenario và current state"""
        
        gap_analysis = {
            "overall_gap": 0.0,
            "factor_gaps": {},
            "critical_gaps": [],
            "improvement_areas": []
        }
        
        # Calculate gaps for each condition
        current_values = {f.factor_type.value: f.current_value for f in current_factors}
        
        for condition_key, target_value in scenario.conditions.items():
            if isinstance(target_value, (int, float)):
                current_value = current_values.get(condition_key, 0.0)
                gap = target_value - current_value
                
                gap_analysis["factor_gaps"][condition_key] = {
                    "target": target_value,
                    "current": current_value,
                    "gap": gap,
                    "gap_percentage": (gap / target_value) * 100 if target_value > 0 else 0
                }
                
                # Identify critical gaps
                if gap > 0.3:
                    gap_analysis["critical_gaps"].append(condition_key)
                elif gap > 0.1:
                    gap_analysis["improvement_areas"].append(condition_key)
        
        # Calculate overall gap
        gaps = [info["gap"] for info in gap_analysis["factor_gaps"].values()]
        if gaps:
            gap_analysis["overall_gap"] = np.mean(gaps)
        
        return gap_analysis
    
    async def _generate_scenario_recommendations(
        self,
        scenario: WINScenario,
        gap_analysis: Dict[str, Any]
    ) -> List[str]:
        """Generate recommendations for achieving scenario"""
        
        recommendations = []
        
        # Recommendations based on critical gaps
        for gap_area in gap_analysis["critical_gaps"]:
            gap_info = gap_analysis["factor_gaps"][gap_area]
            recommendations.append(
                f"Critical improvement needed in {gap_area}: "
                f"increase from {gap_info['current']:.2f} to {gap_info['target']:.2f}"
            )
        
        # Recommendations based on improvement areas
        for improvement_area in gap_analysis["improvement_areas"]:
            gap_info = gap_analysis["factor_gaps"][improvement_area]
            recommendations.append(
                f"Moderate improvement in {improvement_area}: "
                f"target increase of {gap_info['gap']:.2f}"
            )
        
        # General recommendations
        if gap_analysis["overall_gap"] > 0.2:
            recommendations.append("Consider systematic approach to address multiple gaps simultaneously")
        
        return recommendations
    
    async def _assess_scenario_feasibility(
        self,
        scenario: WINScenario,
        current_factors: List[WINFactor]
    ) -> Dict[str, Any]:
        """Assess feasibility of achieving scenario"""
        
        feasibility = {
            "overall_feasibility": "medium",
            "feasibility_score": 0.5,
            "timeline_estimate": "medium_term",
            "resource_requirements": "moderate",
            "risk_factors": []
        }
        
        # Calculate feasibility score
        current_values = {f.factor_type.value: f.current_value for f in current_factors}
        
        gaps = []
        for condition_key, target_value in scenario.conditions.items():
            if isinstance(target_value, (int, float)):
                current_value = current_values.get(condition_key, 0.0)
                gap = abs(target_value - current_value)
                gaps.append(gap)
        
        if gaps:
            avg_gap = np.mean(gaps)
            feasibility["feasibility_score"] = max(0.1, 1.0 - avg_gap)
            
            if avg_gap < 0.2:
                feasibility["overall_feasibility"] = "high"
                feasibility["timeline_estimate"] = "short_term"
            elif avg_gap > 0.5:
                feasibility["overall_feasibility"] = "low"
                feasibility["timeline_estimate"] = "long_term"
                feasibility["resource_requirements"] = "high"
        
        return feasibility 