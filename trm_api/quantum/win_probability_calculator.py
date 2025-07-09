"""
TRM-OS WIN Probability Calculator
Commercial AI-powered WIN probability calculations và analysis
Theo triết lý TRM-OS: Commercial AI coordination thay vì local ML training
"""

import asyncio
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import json

from .quantum_types import QuantumState, QuantumStateType, WINCategory, WINProbability, StateTransition, ProbabilityDistribution
from ..learning.adaptive_learning_system import AdaptiveLearningSystem
from ..learning.learning_types import LearningExperience, ExperienceType


@dataclass
class WINFactor:
    """Factor affecting WIN probability"""
    factor_id: str
    factor_type: 'WINFactorType'
    name: str
    description: str
    
    # Current values
    current_value: float                 # Current factor value [0.0, 1.0]
    baseline_value: float               # Baseline/expected value
    impact_weight: float                # How much this factor impacts WIN probability
    
    # Temporal properties
    trend_direction: str                # "increasing", "decreasing", "stable"
    trend_strength: float               # Strength of trend [0.0, 1.0]
    volatility: float                   # Factor volatility [0.0, 1.0]
    
    # Context
    measurement_time: datetime
    confidence_level: float             # Confidence in measurement [0.0, 1.0]
    data_quality: float                 # Quality of underlying data [0.0, 1.0]
    
    # Metadata
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class WINFactorType(Enum):
    """Types of factors affecting WIN probability"""
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
class WINScenario:
    """Scenario for WIN probability calculation"""
    scenario_id: str
    name: str
    description: str
    
    # Scenario parameters
    time_horizon: timedelta             # How far into the future
    uncertainty_level: float            # Scenario uncertainty [0.0, 1.0]
    external_factors: Dict[str, float]  # External factors affecting this scenario
    
    # WIN factors specific to this scenario
    factor_adjustments: Dict[str, float] # Adjustments to base factors
    quantum_modifiers: Dict[str, float]  # Quantum effects for this scenario
    
    # Probability and confidence
    scenario_probability: float         # Probability of this scenario occurring
    confidence_level: float             # Confidence in scenario definition
    
    # Metadata
    created_time: datetime
    last_updated: datetime
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class WINProbabilityCalculator:
    """
    Advanced WIN Probability Calculator với Commercial AI-Enhanced Calculations
    Tính toán WIN probabilities với contextual analysis và commercial AI guidance
    """
    
    def __init__(self, learning_system: AdaptiveLearningSystem):
        self.learning_system = learning_system
        self.logger = None  # Would initialize proper logger in production
        
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
        
        # Statistics
        self.calculation_stats = {
            "total_calculations": 0,
            "average_probability": 0.0,
            "prediction_accuracy": 0.0,
            "factor_analysis_count": 0,
            "scenario_evaluations": 0
        }
        
        # Commercial AI coordination stats
        self.ai_coordination_stats = {
            "ai_calls_made": 0,
            "ai_success_rate": 0.0,
            "average_ai_response_time": 0.0
        }
        
        print("WINProbabilityCalculator initialized with commercial AI coordination")
    
    async def calculate_win_probability(self, win_category: WINCategory,
                                      quantum_states: List[QuantumState],
                                      contextual_factors: Dict[str, Any] = None,
                                      time_horizon: timedelta = None) -> WINProbability:
        """
        Calculate WIN probability sử dụng commercial AI analysis
        """
        try:
            if contextual_factors is None:
                contextual_factors = {}
            if time_horizon is None:
                time_horizon = timedelta(hours=24)
            
            # Get AI analysis of WIN factors
            ai_analysis = await self._analyze_win_factors_via_ai(
                win_category, quantum_states, contextual_factors, time_horizon
            )
            
            # Extract AI-suggested probabilities
            base_probability = ai_analysis.get("base_probability", 0.5)
            quantum_enhancement = ai_analysis.get("quantum_enhancement", 0.1)
            contextual_adjustment = ai_analysis.get("contextual_adjustment", 0.0)
            
            # Calculate final quantum probability
            quantum_probability = min(1.0, base_probability + quantum_enhancement + contextual_adjustment)
            
            # Get AI-suggested quantum parameters
            superposition_factor = ai_analysis.get("superposition_factor", 0.3)
            entanglement_boost = ai_analysis.get("entanglement_boost", 0.2)
            time_sensitivity = ai_analysis.get("time_sensitivity", 0.5)
            confidence_level = ai_analysis.get("confidence_level", 0.7)
            
            # Create probability distribution
            prob_dist = ProbabilityDistribution(
                states=ai_analysis.get("state_distribution", {}),
                confidence=confidence_level
            )
            prob_dist.normalize()
            prob_dist.calculate_entropy()
            
            # Create WIN probability object
            win_probability = WINProbability(
                win_category=win_category,
                quantum_probability=quantum_probability,
                superposition_factor=superposition_factor,
                entanglement_boost=entanglement_boost,
                time_sensitivity=time_sensitivity,
                confidence_level=confidence_level,
                probability_distribution=prob_dist,
                calculation_time=datetime.now(),
                factors_analyzed=ai_analysis.get("factors_considered", []),
                scenarios_considered=ai_analysis.get("scenarios_evaluated", []),
                quantum_states_used=[state.state_id for state in quantum_states],
                metadata={
                    "ai_analysis": ai_analysis,
                    "contextual_factors": contextual_factors,
                    "time_horizon_hours": time_horizon.total_seconds() / 3600,
                    "calculation_method": "commercial_ai_enhanced"
                }
            )
            
            # Store calculation
            self.probability_history.append(win_probability)
            
            # Update statistics
            self.calculation_stats["total_calculations"] += 1
            self.calculation_stats["average_probability"] = np.mean([
                p.quantum_probability for p in self.probability_history[-100:]
            ]) if self.probability_history else quantum_probability
            
            # Learn from calculation
            await self._learn_from_win_calculation(win_probability, contextual_factors)
            
            print(f"WIN probability calculated: {quantum_probability:.3f} for {win_category.value}")
            return win_probability
            
        except Exception as e:
            print(f"WIN probability calculation error: {e}")
            # Return default probability
            return self._create_default_win_probability(win_category)
    
    async def analyze_win_factors(self, quantum_states: List[QuantumState],
                                contextual_data: Dict[str, Any] = None) -> Dict[str, WINFactor]:
        """
        Analyze WIN factors sử dụng commercial AI
        """
        try:
            if contextual_data is None:
                contextual_data = {}
            
            # Get AI analysis of current situation
            factor_analysis = await self._analyze_factors_via_ai(quantum_states, contextual_data)
            
            analyzed_factors = {}
            
            # Create WIN factors based on AI analysis
            for factor_type in WINFactorType:
                factor_data = factor_analysis.get(factor_type.value, {})
                
                factor = WINFactor(
                    factor_id=f"{factor_type.value}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    factor_type=factor_type,
                    name=factor_type.value.replace('_', ' ').title(),
                    description=factor_data.get("description", f"Analysis of {factor_type.value}"),
                    current_value=factor_data.get("current_value", 0.5),
                    baseline_value=factor_data.get("baseline_value", 0.5),
                    impact_weight=self.default_factor_weights.get(factor_type, 0.1),
                    trend_direction=factor_data.get("trend_direction", "stable"),
                    trend_strength=factor_data.get("trend_strength", 0.0),
                    volatility=factor_data.get("volatility", 0.2),
                    measurement_time=datetime.now(),
                    confidence_level=factor_data.get("confidence", 0.7),
                    data_quality=factor_data.get("data_quality", 0.8),
                    metadata={
                        "ai_analysis": factor_data,
                        "quantum_states_analyzed": len(quantum_states),
                        "contextual_data_size": len(contextual_data)
                    }
                )
                
                analyzed_factors[factor.factor_id] = factor
                self.win_factors[factor.factor_id] = factor
            
            self.calculation_stats["factor_analysis_count"] += 1
            
            return analyzed_factors
            
        except Exception as e:
            print(f"WIN factor analysis error: {e}")
            return {}
    
    async def evaluate_win_scenarios(self, base_win_probability: WINProbability,
                                   scenario_parameters: Dict[str, Any] = None) -> List[WINScenario]:
        """
        Evaluate different WIN scenarios sử dụng commercial AI
        """
        try:
            if scenario_parameters is None:
                scenario_parameters = {}
            
            # Get AI scenario analysis
            scenario_analysis = await self._analyze_scenarios_via_ai(
                base_win_probability, scenario_parameters
            )
            
            evaluated_scenarios = []
            
            # Create scenarios from AI analysis
            scenario_configs = scenario_analysis.get("scenarios", [])
            
            for i, scenario_config in enumerate(scenario_configs):
                scenario = WINScenario(
                    scenario_id=f"scenario_{i+1}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    name=scenario_config.get("name", f"Scenario {i+1}"),
                    description=scenario_config.get("description", "AI-generated scenario"),
                    time_horizon=timedelta(hours=scenario_config.get("time_horizon_hours", 24)),
                    uncertainty_level=scenario_config.get("uncertainty", 0.3),
                    external_factors=scenario_config.get("external_factors", {}),
                    factor_adjustments=scenario_config.get("factor_adjustments", {}),
                    quantum_modifiers=scenario_config.get("quantum_modifiers", {}),
                    scenario_probability=scenario_config.get("probability", 0.33),
                    confidence_level=scenario_config.get("confidence", 0.7),
                    created_time=datetime.now(),
                    last_updated=datetime.now(),
                    metadata={
                        "ai_analysis": scenario_config,
                        "base_win_category": base_win_probability.win_category.value
                    }
                )
                
                evaluated_scenarios.append(scenario)
                self.win_scenarios[scenario.scenario_id] = scenario
            
            self.calculation_stats["scenario_evaluations"] += len(evaluated_scenarios)
            
            return evaluated_scenarios
            
        except Exception as e:
            print(f"WIN scenario evaluation error: {e}")
            return []
    
    async def predict_win_probability_trend(self, win_category: WINCategory,
                                          prediction_horizon: timedelta = None) -> Dict[str, Any]:
        """
        Predict WIN probability trends sử dụng commercial AI
        """
        try:
            if prediction_horizon is None:
                prediction_horizon = timedelta(days=7)
            
            # Get AI trend prediction
            trend_analysis = await self._predict_trends_via_ai(win_category, prediction_horizon)
            
            prediction_result = {
                "win_category": win_category.value,
                "prediction_horizon_days": prediction_horizon.days,
                "trend_direction": trend_analysis.get("trend_direction", "stable"),
                "trend_strength": trend_analysis.get("trend_strength", 0.0),
                "predicted_probability_range": trend_analysis.get("probability_range", (0.4, 0.6)),
                "confidence_level": trend_analysis.get("confidence", 0.6),
                "key_factors": trend_analysis.get("key_factors", []),
                "risk_factors": trend_analysis.get("risk_factors", []),
                "opportunities": trend_analysis.get("opportunities", []),
                "recommended_actions": trend_analysis.get("recommendations", []),
                "prediction_accuracy_estimate": trend_analysis.get("accuracy_estimate", 0.7),
                "prediction_time": datetime.now(),
                "metadata": {
                    "ai_analysis": trend_analysis,
                    "historical_data_points": len(self.probability_history),
                    "prediction_method": "commercial_ai_enhanced"
                }
            }
            
            return prediction_result
            
        except Exception as e:
            print(f"WIN probability trend prediction error: {e}")
            return {
                "win_category": win_category.value,
                "trend_direction": "unknown",
                "confidence_level": 0.0,
                "error": str(e)
            }
    
    async def _analyze_win_factors_via_ai(self, win_category: WINCategory,
                                        quantum_states: List[QuantumState],
                                        contextual_factors: Dict[str, Any],
                                        time_horizon: timedelta) -> Dict[str, Any]:
        """
        Analyze WIN factors using commercial AI
        TODO: Tích hợp với OpenAI/Claude/Gemini APIs
        """
        try:
            # Update AI coordination stats
            self.ai_coordination_stats["ai_calls_made"] += 1
            
            # For now, use intelligent heuristics
            # TODO: Replace với actual commercial AI API calls
            
            # Analyze quantum states
            state_coherence = np.mean([state.coherence for state in quantum_states]) if quantum_states else 0.5
            state_probability = np.mean([state.probability for state in quantum_states]) if quantum_states else 0.5
            
            # Analyze contextual factors
            performance_indicator = contextual_factors.get("performance", 0.7)
            resource_availability = contextual_factors.get("resources", 0.8)
            team_coherence = contextual_factors.get("team_coherence", state_coherence)
            
            # Base probability calculation
            base_probability = (state_probability + performance_indicator + team_coherence) / 3.0
            
            # Quantum enhancement based on state quality
            quantum_enhancement = state_coherence * 0.2
            
            # Contextual adjustments
            contextual_adjustment = (resource_availability - 0.5) * 0.1
            
            # Time horizon effects
            time_hours = time_horizon.total_seconds() / 3600
            time_factor = max(0.5, min(1.0, 24 / max(time_hours, 1)))  # Closer time = higher confidence
            
            # Category-specific adjustments
            category_multiplier = {
                WINCategory.STRATEGIC: 1.0,
                WINCategory.OPERATIONAL: 1.1,
                WINCategory.TACTICAL: 1.2,
                WINCategory.PERSONAL: 0.9,
                WINCategory.TEAM: 1.0,
                WINCategory.ORGANIZATIONAL: 0.8
            }.get(win_category, 1.0)
            
            base_probability *= category_multiplier
            
            analysis = {
                "base_probability": min(1.0, base_probability),
                "quantum_enhancement": quantum_enhancement,
                "contextual_adjustment": contextual_adjustment,
                "superposition_factor": min(1.0, state_coherence + 0.1),
                "entanglement_boost": min(1.0, team_coherence * 0.5),
                "time_sensitivity": time_factor,
                "confidence_level": min(1.0, (state_coherence + performance_indicator) / 2.0),
                "state_distribution": {
                    state.state_id: state.probability for state in quantum_states
                },
                "factors_considered": [
                    "quantum_state_coherence",
                    "performance_indicators", 
                    "resource_availability",
                    "team_coherence",
                    "time_horizon"
                ],
                "scenarios_evaluated": ["base_case", "optimistic", "conservative"],
                "ai_insights": {
                    "primary_drivers": ["quantum_coherence", "team_performance"],
                    "risk_factors": ["resource_constraints", "time_pressure"],
                    "opportunities": ["quantum_enhancement", "team_synergy"]
                }
            }
            
            return analysis
            
        except Exception as e:
            print(f"AI WIN factor analysis error: {e}")
            return {
                "base_probability": 0.5,
                "quantum_enhancement": 0.1,
                "contextual_adjustment": 0.0,
                "confidence_level": 0.5
            }
    
    async def _analyze_factors_via_ai(self, quantum_states: List[QuantumState],
                                    contextual_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze individual WIN factors using commercial AI
        TODO: Tích hợp với AI APIs cho detailed factor analysis
        """
        try:
            factor_analysis = {}
            
            # Analyze each factor type
            for factor_type in WINFactorType:
                factor_data = await self._analyze_single_factor_via_ai(
                    factor_type, quantum_states, contextual_data
                )
                factor_analysis[factor_type.value] = factor_data
            
            return factor_analysis
            
        except Exception as e:
            print(f"AI factor analysis error: {e}")
            return {}
    
    async def _analyze_single_factor_via_ai(self, factor_type: WINFactorType,
                                          quantum_states: List[QuantumState],
                                          contextual_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze single WIN factor using commercial AI
        """
        try:
            # Get relevant data for this factor
            state_coherence = np.mean([state.coherence for state in quantum_states]) if quantum_states else 0.5
            
            # Factor-specific analysis
            if factor_type == WINFactorType.SYSTEM_COHERENCE:
                current_value = state_coherence
                trend_direction = "stable" if 0.4 <= current_value <= 0.7 else "improving" if current_value > 0.7 else "declining"
            elif factor_type == WINFactorType.TEAM_PERFORMANCE:
                current_value = contextual_data.get("team_performance", state_coherence * 0.9)
                trend_direction = "improving" if current_value > 0.6 else "stable"
            elif factor_type == WINFactorType.RESOURCE_AVAILABILITY:
                current_value = contextual_data.get("resources", 0.7)
                trend_direction = "stable"
            else:
                # Default analysis
                current_value = 0.5 + np.random.normal(0, 0.1)  # Add some variation
                current_value = max(0.0, min(1.0, current_value))
                trend_direction = "stable"
            
            factor_data = {
                "current_value": current_value,
                "baseline_value": 0.5,
                "trend_direction": trend_direction,
                "trend_strength": abs(current_value - 0.5),
                "volatility": 0.1 + np.random.normal(0, 0.05),
                "confidence": 0.7 + (state_coherence * 0.2),
                "data_quality": 0.8,
                "description": f"AI analysis of {factor_type.value.replace('_', ' ')}"
            }
            
            # Ensure valid ranges
            factor_data["volatility"] = max(0.0, min(1.0, factor_data["volatility"]))
            factor_data["confidence"] = max(0.0, min(1.0, factor_data["confidence"]))
            
            return factor_data
            
        except Exception as e:
            print(f"Single factor analysis error: {e}")
            return {
                "current_value": 0.5,
                "baseline_value": 0.5,
                "trend_direction": "stable",
                "confidence": 0.5
            }
    
    async def _analyze_scenarios_via_ai(self, base_win_probability: WINProbability,
                                      scenario_parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze WIN scenarios using commercial AI
        TODO: Tích hợp với AI APIs cho scenario generation
        """
        try:
            # Generate 3 standard scenarios: optimistic, base, pessimistic
            scenarios = [
                {
                    "name": "Optimistic Scenario",
                    "description": "Best-case scenario với optimal conditions",
                    "probability": 0.25,
                    "time_horizon_hours": 24,
                    "uncertainty": 0.2,
                    "external_factors": {"market_conditions": 0.8, "team_morale": 0.9},
                    "factor_adjustments": {"performance": 0.2, "resources": 0.1},
                    "quantum_modifiers": {"coherence_boost": 0.15, "entanglement_enhancement": 0.1},
                    "confidence": 0.7
                },
                {
                    "name": "Base Scenario", 
                    "description": "Most likely scenario với current trends",
                    "probability": 0.5,
                    "time_horizon_hours": 24,
                    "uncertainty": 0.3,
                    "external_factors": {"market_conditions": 0.6, "team_morale": 0.7},
                    "factor_adjustments": {},
                    "quantum_modifiers": {},
                    "confidence": 0.8
                },
                {
                    "name": "Conservative Scenario",
                    "description": "Worst-case scenario với potential challenges",
                    "probability": 0.25,
                    "time_horizon_hours": 48,
                    "uncertainty": 0.4,
                    "external_factors": {"market_conditions": 0.4, "team_morale": 0.5},
                    "factor_adjustments": {"performance": -0.1, "resources": -0.2},
                    "quantum_modifiers": {"coherence_reduction": 0.1},
                    "confidence": 0.6
                }
            ]
            
            return {"scenarios": scenarios}
            
        except Exception as e:
            print(f"AI scenario analysis error: {e}")
            return {"scenarios": []}
    
    async def _predict_trends_via_ai(self, win_category: WINCategory,
                                   prediction_horizon: timedelta) -> Dict[str, Any]:
        """
        Predict WIN probability trends using commercial AI
        TODO: Tích hợp với AI APIs cho trend prediction
        """
        try:
            # Simple trend analysis based on recent history
            recent_probabilities = [
                p.quantum_probability for p in self.probability_history[-10:]
                if p.win_category == win_category
            ]
            
            if len(recent_probabilities) >= 2:
                trend_slope = (recent_probabilities[-1] - recent_probabilities[0]) / max(len(recent_probabilities) - 1, 1)
                trend_direction = "improving" if trend_slope > 0.05 else "declining" if trend_slope < -0.05 else "stable"
                trend_strength = abs(trend_slope)
            else:
                trend_direction = "stable"
                trend_strength = 0.0
            
            # Predict future range
            current_prob = recent_probabilities[-1] if recent_probabilities else 0.5
            future_variance = 0.1  # Default variance
            prob_range = (
                max(0.0, current_prob - future_variance),
                min(1.0, current_prob + future_variance)
            )
            
            trend_analysis = {
                "trend_direction": trend_direction,
                "trend_strength": trend_strength,
                "probability_range": prob_range,
                "confidence": 0.7 if len(recent_probabilities) >= 5 else 0.5,
                "key_factors": ["system_coherence", "team_performance", "resource_availability"],
                "risk_factors": ["external_volatility", "resource_constraints"],
                "opportunities": ["process_optimization", "team_enhancement"],
                "recommendations": [
                    "Monitor system coherence closely",
                    "Enhance team coordination",
                    "Optimize resource allocation"
                ],
                "accuracy_estimate": 0.7
            }
            
            return trend_analysis
            
        except Exception as e:
            print(f"AI trend prediction error: {e}")
            return {
                "trend_direction": "unknown",
                "confidence": 0.0,
                "error": str(e)
            }
    
    def _create_default_win_probability(self, win_category: WINCategory) -> WINProbability:
        """Create default WIN probability when calculation fails"""
        try:
            default_prob_dist = ProbabilityDistribution(
                states={"default": 0.5},
                confidence=0.5
            )
            default_prob_dist.normalize()
            default_prob_dist.calculate_entropy()
            
            return WINProbability(
                win_category=win_category,
                quantum_probability=0.5,
                superposition_factor=0.3,
                entanglement_boost=0.2,
                time_sensitivity=0.5,
                confidence_level=0.5,
                probability_distribution=default_prob_dist,
                calculation_time=datetime.now(),
                factors_analyzed=[],
                scenarios_considered=[],
                quantum_states_used=[],
                metadata={"calculation_method": "default_fallback"}
            )
            
        except Exception as e:
            print(f"Default WIN probability creation error: {e}")
            # Return minimal viable object
            return WINProbability(
                win_category=win_category,
                quantum_probability=0.5
            )
    
    async def _learn_from_win_calculation(self, win_probability: WINProbability,
                                        contextual_factors: Dict[str, Any]) -> None:
        """Learn from WIN probability calculation"""
        try:
            experience = LearningExperience(
                experience_type=ExperienceType.WIN_CALCULATION,
                agent_id="win_probability_calculator",
                context={
                    "win_category": win_probability.win_category.value,
                    "contextual_factors_count": len(contextual_factors),
                    "quantum_states_analyzed": len(win_probability.quantum_states_used)
                },
                action_taken={
                    "action": "calculate_win_probability",
                    "calculation_method": "commercial_ai_enhanced"
                },
                outcome={
                    "quantum_probability": win_probability.quantum_probability,
                    "confidence_level": win_probability.confidence_level,
                    "factors_analyzed_count": len(win_probability.factors_analyzed)
                },
                success=win_probability.confidence_level > 0.6,
                confidence_level=win_probability.confidence_level,
                importance_weight=0.8
            )
            
            await self.learning_system.learn_from_experience(experience)
            
        except Exception as e:
            print(f"WIN calculation learning error: {e}")
    
    def get_calculation_statistics(self) -> Dict[str, Any]:
        """Get comprehensive calculation statistics"""
        try:
            stats = self.calculation_stats.copy()
            stats["ai_coordination_stats"] = self.ai_coordination_stats
            stats["probability_history_size"] = len(self.probability_history)
            stats["win_factors_tracked"] = len(self.win_factors)
            stats["scenarios_available"] = len(self.win_scenarios)
            
            if self.probability_history:
                recent_probs = [p.quantum_probability for p in self.probability_history[-50:]]
                stats["recent_average_probability"] = np.mean(recent_probs)
                stats["recent_probability_std"] = np.std(recent_probs)
                stats["recent_max_probability"] = np.max(recent_probs)
                stats["recent_min_probability"] = np.min(recent_probs)
            
            return stats
            
        except Exception as e:
            print(f"Statistics calculation error: {e}")
            return self.calculation_stats 