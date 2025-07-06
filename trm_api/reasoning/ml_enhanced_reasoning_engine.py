"""
ML-Enhanced Reasoning Engine - Advanced Reasoning với Machine Learning
Tích hợp Quantum WIN States, Adaptive Learning, và Advanced Reasoning
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple, Union
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import numpy as np
from uuid import uuid4
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
import joblib

from ..learning.adaptive_learning_system import AdaptiveLearningSystem
from ..learning.learning_types import LearningExperience, ExperienceType
from ..quantum.quantum_system_manager import QuantumSystemManager, OrganizationalSignals
from ..quantum.quantum_types import QuantumState, WINCategory, WINProbability
from ..reasoning.advanced_reasoning_engine import AdvancedReasoningEngine
from ..reasoning.reasoning_types import ReasoningChain, LogicalRule, ReasoningContext as AdvancedReasoningContext, ReasoningGoal
from ..eventbus.system_event_bus import publish_event


class ReasoningType(Enum):
    """Types of reasoning"""
    DEDUCTIVE = "deductive"           # From general to specific
    INDUCTIVE = "inductive"           # From specific to general
    ABDUCTIVE = "abductive"           # Best explanation
    ANALOGICAL = "analogical"         # By analogy
    CAUSAL = "causal"                # Cause-effect relationships
    PROBABILISTIC = "probabilistic"  # Probability-based
    QUANTUM = "quantum"              # Quantum-enhanced reasoning
    HYBRID = "hybrid"                # Multiple reasoning types


class ConfidenceLevel(Enum):
    """Confidence levels for reasoning"""
    VERY_LOW = "very_low"      # 0.0 - 0.2
    LOW = "low"                # 0.2 - 0.4
    MEDIUM = "medium"          # 0.4 - 0.6
    HIGH = "high"              # 0.6 - 0.8
    VERY_HIGH = "very_high"    # 0.8 - 1.0


@dataclass
class ReasoningContext:
    """Context for reasoning operations"""
    context_id: str
    domain: str                       # "agent_creation", "tension_resolution", etc.
    stakeholders: List[str] = field(default_factory=list)
    constraints: Dict[str, Any] = field(default_factory=dict)
    objectives: List[str] = field(default_factory=list)
    available_resources: Dict[str, float] = field(default_factory=dict)
    time_constraints: Optional[datetime] = None
    priority_level: int = 5           # 1-10 scale
    risk_tolerance: float = 0.5       # 0.0 - 1.0
    quantum_context: Dict[str, Any] = field(default_factory=dict)
    
    def to_feature_vector(self) -> List[float]:
        """Convert context to ML feature vector"""
        features = [
            len(self.stakeholders),
            len(self.constraints),
            len(self.objectives),
            len(self.available_resources),
            self.priority_level / 10.0,
            self.risk_tolerance,
            1.0 if self.time_constraints else 0.0,
            sum(self.available_resources.values()) / max(1, len(self.available_resources))
        ]
        return features


@dataclass
class ReasoningResult:
    """Result of reasoning operation"""
    result_id: str
    reasoning_type: ReasoningType
    conclusion: str
    confidence: float
    reasoning_steps: List[str] = field(default_factory=list)
    supporting_evidence: List[str] = field(default_factory=list)
    contradicting_evidence: List[str] = field(default_factory=list)
    assumptions: List[str] = field(default_factory=list)
    alternative_conclusions: List[str] = field(default_factory=list)
    
    # ML enhancements
    ml_confidence: float = 0.0
    quantum_enhancement: float = 0.0
    win_probability_impact: float = 0.0
    
    # Temporal information
    reasoning_time: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)
    
    # Quality metrics
    logical_consistency: float = 0.0
    evidence_strength: float = 0.0
    novelty_score: float = 0.0
    
    def get_confidence_level(self) -> ConfidenceLevel:
        """Get confidence level category"""
        if self.confidence < 0.2:
            return ConfidenceLevel.VERY_LOW
        elif self.confidence < 0.4:
            return ConfidenceLevel.LOW
        elif self.confidence < 0.6:
            return ConfidenceLevel.MEDIUM
        elif self.confidence < 0.8:
            return ConfidenceLevel.HIGH
        else:
            return ConfidenceLevel.VERY_HIGH


@dataclass
class MLReasoningModel:
    """ML model for reasoning enhancement"""
    model_id: str
    model_type: str                   # "classifier", "regressor", "neural_network"
    model: Any                        # Actual ML model
    scaler: StandardScaler
    trained: bool = False
    training_accuracy: float = 0.0
    validation_accuracy: float = 0.0
    feature_importance: Dict[str, float] = field(default_factory=dict)
    last_updated: datetime = field(default_factory=datetime.now)


class MLEnhancedReasoningEngine:
    """
    ML-Enhanced Reasoning Engine
    Combines traditional reasoning với machine learning và quantum enhancements
    """
    
    def __init__(
        self, 
        learning_system: AdaptiveLearningSystem,
        quantum_manager: QuantumSystemManager,
        advanced_reasoning: AdvancedReasoningEngine
    ):
        self.learning_system = learning_system
        self.quantum_manager = quantum_manager
        self.advanced_reasoning = advanced_reasoning
        self.logger = logging.getLogger(__name__)
        
        # ML Models
        self.ml_models: Dict[str, MLReasoningModel] = {}
        self.reasoning_predictor = None
        self.confidence_estimator = None
        self.quantum_enhancer = None
        
        # Reasoning history và analytics
        self.reasoning_history: List[ReasoningResult] = []
        self.reasoning_patterns: Dict[str, Any] = {}
        self.performance_metrics: Dict[str, float] = {}
        
        # Configuration
        self.max_reasoning_steps = 20
        self.confidence_threshold = 0.6
        self.quantum_enhancement_threshold = 0.7
        self.learning_window = 100
        
        # Statistics
        self.reasoning_stats = {
            "total_reasonings": 0,
            "successful_reasonings": 0,
            "average_confidence": 0.0,
            "average_reasoning_time": 0.0,
            "ml_enhancement_rate": 0.0,
            "quantum_enhancement_rate": 0.0
        }
        
        self.logger.info("MLEnhancedReasoningEngine initialized")
    
    async def initialize(self) -> None:
        """Initialize ML-Enhanced Reasoning Engine"""
        
        try:
            self.logger.info("Initializing ML-Enhanced Reasoning Engine...")
            
            # Initialize ML models
            await self._initialize_ml_models()
            
            # Load pre-trained models if available
            await self._load_pretrained_models()
            
            # Initialize reasoning patterns
            await self._initialize_reasoning_patterns()
            
            self.logger.info("ML-Enhanced Reasoning Engine initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize ML-Enhanced Reasoning Engine: {e}")
            raise
    
    async def reason(
        self,
        query: str,
        context: ReasoningContext,
        reasoning_type: ReasoningType = ReasoningType.HYBRID,
        use_quantum_enhancement: bool = True
    ) -> ReasoningResult:
        """
        Perform enhanced reasoning với ML và quantum enhancements
        """
        
        start_time = datetime.now()
        result_id = str(uuid4())
        
        try:
            self.logger.info(f"Starting reasoning for query: {query[:100]}...")
            
            # Step 1: Classical reasoning using AdvancedReasoningEngine
            classical_result = await self._perform_classical_reasoning(query, context, reasoning_type)
            
            # Step 2: ML enhancement
            ml_enhanced_result = await self._apply_ml_enhancement(classical_result, context)
            
            # Step 3: Quantum enhancement (if enabled)
            if use_quantum_enhancement:
                quantum_enhanced_result = await self._apply_quantum_enhancement(
                    ml_enhanced_result, context
                )
            else:
                quantum_enhanced_result = ml_enhanced_result
            
            # Step 4: Confidence calibration
            calibrated_result = await self._calibrate_confidence(quantum_enhanced_result, context)
            
            # Step 5: Quality assessment
            final_result = await self._assess_reasoning_quality(calibrated_result, context)
            
            # Calculate reasoning time
            reasoning_time = (datetime.now() - start_time).total_seconds()
            final_result.reasoning_time = reasoning_time
            
            # Store result
            self.reasoning_history.append(final_result)
            if len(self.reasoning_history) > self.learning_window:
                self.reasoning_history.pop(0)
            
            # Update statistics
            await self._update_reasoning_stats(final_result)
            
            # Learn from reasoning
            await self._learn_from_reasoning(query, context, final_result)
            
            # Record event
            await publish_event(
                event_type="reasoning.completed",
                source_agent_id="ml_enhanced_reasoning_engine",
                entity_id=result_id,
                entity_type="reasoning_result",
                data={
                    "reasoning_type": reasoning_type.value,
                    "confidence": final_result.confidence,
                    "ml_enhanced": final_result.ml_confidence > 0,
                    "quantum_enhanced": final_result.quantum_enhancement > 0,
                    "reasoning_time": reasoning_time
                }
            )
            
            self.logger.info(f"Reasoning completed with confidence: {final_result.confidence:.3f}")
            
            return final_result
            
        except Exception as e:
            self.logger.error(f"Failed to perform reasoning: {e}")
            
            # Return fallback result
            fallback_result = ReasoningResult(
                result_id=result_id,
                reasoning_type=reasoning_type,
                conclusion=f"Unable to complete reasoning: {str(e)}",
                confidence=0.1,
                reasoning_time=(datetime.now() - start_time).total_seconds()
            )
            
            return fallback_result
    
    async def train_ml_models(self, training_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Train ML models với reasoning data"""
        
        try:
            self.logger.info(f"Training ML models with {len(training_data)} samples...")
            
            if len(training_data) < 10:
                return {"error": "Insufficient training data (minimum 10 samples)"}
            
            # Prepare training data
            X, y_confidence, y_reasoning_type = await self._prepare_training_data(training_data)
            
            # Train confidence estimator
            confidence_accuracy = await self._train_confidence_estimator(X, y_confidence)
            
            # Train reasoning predictor
            reasoning_accuracy = await self._train_reasoning_predictor(X, y_reasoning_type)
            
            # Train quantum enhancer
            quantum_accuracy = await self._train_quantum_enhancer(X, y_confidence)
            
            # Update model status
            for model in self.ml_models.values():
                model.trained = True
                model.last_updated = datetime.now()
            
            training_result = {
                "confidence_accuracy": confidence_accuracy,
                "reasoning_accuracy": reasoning_accuracy,
                "quantum_accuracy": quantum_accuracy,
                "training_samples": len(training_data),
                "models_trained": len(self.ml_models)
            }
            
            # Learn from training
            await self._learn_from_training(training_result)
            
            self.logger.info("ML models training completed successfully")
            
            return training_result
            
        except Exception as e:
            self.logger.error(f"Failed to train ML models: {e}")
            return {"error": str(e)}
    
    async def analyze_reasoning_patterns(self) -> Dict[str, Any]:
        """Analyze reasoning patterns từ history"""
        
        if len(self.reasoning_history) < 5:
            return {"error": "Insufficient reasoning history for analysis"}
        
        try:
            # Confidence patterns
            confidences = [r.confidence for r in self.reasoning_history]
            confidence_analysis = {
                "average": np.mean(confidences),
                "std": np.std(confidences),
                "trend": self._calculate_trend(confidences),
                "distribution": self._calculate_confidence_distribution(confidences)
            }
            
            # Reasoning type patterns
            type_counts = {}
            for result in self.reasoning_history:
                type_name = result.reasoning_type.value
                type_counts[type_name] = type_counts.get(type_name, 0) + 1
            
            # Performance patterns
            performance_analysis = {
                "average_reasoning_time": np.mean([r.reasoning_time for r in self.reasoning_history]),
                "success_rate": len([r for r in self.reasoning_history if r.confidence > self.confidence_threshold]) / len(self.reasoning_history),
                "ml_enhancement_rate": len([r for r in self.reasoning_history if r.ml_confidence > 0]) / len(self.reasoning_history),
                "quantum_enhancement_rate": len([r for r in self.reasoning_history if r.quantum_enhancement > 0]) / len(self.reasoning_history)
            }
            
            # Quality patterns
            quality_analysis = {
                "average_logical_consistency": np.mean([r.logical_consistency for r in self.reasoning_history]),
                "average_evidence_strength": np.mean([r.evidence_strength for r in self.reasoning_history]),
                "average_novelty": np.mean([r.novelty_score for r in self.reasoning_history])
            }
            
            pattern_analysis = {
                "confidence_patterns": confidence_analysis,
                "reasoning_type_distribution": type_counts,
                "performance_patterns": performance_analysis,
                "quality_patterns": quality_analysis,
                "total_reasonings": len(self.reasoning_history),
                "analysis_timestamp": datetime.now().isoformat()
            }
            
            # Store patterns
            self.reasoning_patterns.update(pattern_analysis)
            
            return pattern_analysis
            
        except Exception as e:
            self.logger.error(f"Failed to analyze reasoning patterns: {e}")
            return {"error": str(e)}
    
    async def get_reasoning_recommendations(
        self,
        context: ReasoningContext
    ) -> List[Dict[str, Any]]:
        """Get recommendations cho reasoning approach"""
        
        try:
            recommendations = []
            
            # Analyze context
            context_features = context.to_feature_vector()
            
            # Recommend reasoning type
            if self.reasoning_predictor and hasattr(self.reasoning_predictor, 'model'):
                predicted_type = await self._predict_best_reasoning_type(context_features)
                recommendations.append({
                    "type": "reasoning_type",
                    "recommendation": predicted_type,
                    "confidence": 0.8,
                    "reason": "ML model prediction based on context"
                })
            
            # Recommend quantum enhancement
            if context.priority_level >= 7 or context.risk_tolerance < 0.3:
                recommendations.append({
                    "type": "quantum_enhancement",
                    "recommendation": True,
                    "confidence": 0.9,
                    "reason": "High priority or low risk tolerance detected"
                })
            
            # Recommend confidence threshold
            if context.domain in ["tension_resolution", "agent_creation"]:
                recommendations.append({
                    "type": "confidence_threshold",
                    "recommendation": 0.8,
                    "confidence": 0.7,
                    "reason": "Critical domain requires high confidence"
                })
            
            # Resource-based recommendations
            if sum(context.available_resources.values()) > 10:
                recommendations.append({
                    "type": "reasoning_depth",
                    "recommendation": "deep",
                    "confidence": 0.6,
                    "reason": "Sufficient resources for deep reasoning"
                })
            
            return recommendations
            
        except Exception as e:
            self.logger.error(f"Failed to get reasoning recommendations: {e}")
            return []
    
    def get_reasoning_statistics(self) -> Dict[str, Any]:
        """Get comprehensive reasoning statistics"""
        
        return {
            **self.reasoning_stats,
            "ml_models_count": len(self.ml_models),
            "trained_models": len([m for m in self.ml_models.values() if m.trained]),
            "reasoning_history_size": len(self.reasoning_history),
            "patterns_discovered": len(self.reasoning_patterns),
            "average_steps_per_reasoning": np.mean([len(r.reasoning_steps) for r in self.reasoning_history]) if self.reasoning_history else 0
        }
    
    # Private methods
    
    async def _initialize_ml_models(self) -> None:
        """Initialize ML models"""
        
        # Confidence estimator
        confidence_model = MLReasoningModel(
            model_id="confidence_estimator",
            model_type="regressor",
            model=GradientBoostingRegressor(n_estimators=100, random_state=42),
            scaler=StandardScaler()
        )
        self.ml_models["confidence_estimator"] = confidence_model
        self.confidence_estimator = confidence_model
        
        # Reasoning type predictor
        reasoning_model = MLReasoningModel(
            model_id="reasoning_predictor",
            model_type="classifier",
            model=RandomForestClassifier(n_estimators=100, random_state=42),
            scaler=StandardScaler()
        )
        self.ml_models["reasoning_predictor"] = reasoning_model
        self.reasoning_predictor = reasoning_model
        
        # Quantum enhancer
        quantum_model = MLReasoningModel(
            model_id="quantum_enhancer",
            model_type="neural_network",
            model=MLPClassifier(hidden_layer_sizes=(100, 50), random_state=42),
            scaler=StandardScaler()
        )
        self.ml_models["quantum_enhancer"] = quantum_model
        self.quantum_enhancer = quantum_model
        
        self.logger.info("ML models initialized")
    
    async def _load_pretrained_models(self) -> None:
        """Load pre-trained models if available"""
        
        # Placeholder for loading pre-trained models
        # In production, would load from files
        self.logger.info("Pre-trained models loading skipped (not available)")
    
    async def _initialize_reasoning_patterns(self) -> None:
        """Initialize reasoning patterns"""
        
        # Default patterns based on domain knowledge
        self.reasoning_patterns = {
            "default_reasoning_types": {
                "agent_creation": ReasoningType.DEDUCTIVE.value,
                "tension_resolution": ReasoningType.ABDUCTIVE.value,
                "project_planning": ReasoningType.PROBABILISTIC.value,
                "crisis_management": ReasoningType.QUANTUM.value
            },
            "confidence_thresholds": {
                "low_risk": 0.5,
                "medium_risk": 0.7,
                "high_risk": 0.9
            }
        }
        
        self.logger.info("Reasoning patterns initialized")
    
    async def _perform_classical_reasoning(
        self,
        query: str,
        context: ReasoningContext,
        reasoning_type: ReasoningType
    ) -> ReasoningResult:
        """Perform classical reasoning using AdvancedReasoningEngine"""
        
        # Convert ML ReasoningContext to AdvancedReasoningEngine ReasoningContext
        from ..reasoning.reasoning_types import ReasoningContext as AdvancedReasoningContext
        from ..reasoning.reasoning_types import ReasoningGoal
        
        # Create proper context for AdvancedReasoningEngine
        advanced_context = AdvancedReasoningContext(
            domain=context.domain,
            priority_level=context.priority_level,
            current_state={"query": query, "domain": context.domain},
            related_entities={"stakeholders": context.stakeholders}
        )
        
        # Create reasoning goal
        goal = ReasoningGoal(
            goal_type=reasoning_type.value,
            description=query,
            priority=context.priority_level
        )
        
        # Use advanced reasoning engine
        reasoning_result = await self.advanced_reasoning.reason(goal, advanced_context)
        
        # Convert to our result format
        result = ReasoningResult(
            result_id=str(uuid4()),
            reasoning_type=reasoning_type,
            conclusion=reasoning_result.conclusions[0] if reasoning_result.conclusions else "Classical reasoning completed",
            confidence=reasoning_result.overall_confidence,
            reasoning_steps=[step.description for step in reasoning_result.steps],
            logical_consistency=reasoning_result.reasoning_quality,
            evidence_strength=reasoning_result.reasoning_quality * 0.8
        )
        
        return result
    
    async def _apply_ml_enhancement(
        self,
        classical_result: ReasoningResult,
        context: ReasoningContext
    ) -> ReasoningResult:
        """Apply ML enhancement to reasoning result"""
        
        try:
            if not self.confidence_estimator or not self.confidence_estimator.trained:
                # No enhancement if model not trained
                classical_result.ml_confidence = 0.0
                return classical_result
            
            # Prepare features
            features = context.to_feature_vector() + [
                classical_result.confidence,
                len(classical_result.reasoning_steps),
                classical_result.logical_consistency,
                classical_result.evidence_strength
            ]
            
            # Scale features
            features_scaled = self.confidence_estimator.scaler.transform([features])
            
            # Predict enhanced confidence
            ml_confidence = self.confidence_estimator.model.predict(features_scaled)[0]
            ml_confidence = max(0.0, min(1.0, ml_confidence))
            
            # Apply enhancement
            enhanced_confidence = (classical_result.confidence + ml_confidence) / 2
            classical_result.confidence = enhanced_confidence
            classical_result.ml_confidence = ml_confidence
            
            # Add ML reasoning step
            classical_result.reasoning_steps.append(
                f"ML enhancement applied: confidence adjusted to {enhanced_confidence:.3f}"
            )
            
            return classical_result
            
        except Exception as e:
            self.logger.error(f"Failed to apply ML enhancement: {e}")
            classical_result.ml_confidence = 0.0
            return classical_result
    
    async def _apply_quantum_enhancement(
        self,
        ml_result: ReasoningResult,
        context: ReasoningContext
    ) -> ReasoningResult:
        """Apply quantum enhancement to reasoning result"""
        
        try:
            # Get quantum system state
            signals = OrganizationalSignals(
                learning_progress=context.priority_level / 10.0,
                system_coherence=ml_result.confidence,
                adaptation_success_rate=ml_result.logical_consistency
            )
            
            # Get primary quantum system
            if self.quantum_manager.quantum_systems:
                system_id = list(self.quantum_manager.quantum_systems.keys())[0]
                
                # Detect quantum state
                quantum_state = await self.quantum_manager.detect_current_quantum_state(
                    system_id, signals
                )
                
                if quantum_state:
                    # Calculate WIN probability
                    win_prob = await self.quantum_manager.calculate_win_probability(
                        system_id, WINCategory.COMPOSITE, context.__dict__
                    )
                    
                    if win_prob:
                        # Apply quantum enhancement
                        quantum_factor = win_prob.base_probability
                        enhanced_confidence = ml_result.confidence * (1 + quantum_factor * 0.2)
                        enhanced_confidence = max(0.0, min(1.0, enhanced_confidence))
                        
                        ml_result.confidence = enhanced_confidence
                        ml_result.quantum_enhancement = quantum_factor
                        ml_result.win_probability_impact = win_prob.base_probability
                        
                        # Add quantum reasoning step
                        ml_result.reasoning_steps.append(
                            f"Quantum enhancement applied: WIN probability {win_prob.base_probability:.3f}, "
                            f"confidence enhanced to {enhanced_confidence:.3f}"
                        )
            
            return ml_result
            
        except Exception as e:
            self.logger.error(f"Failed to apply quantum enhancement: {e}")
            ml_result.quantum_enhancement = 0.0
            return ml_result
    
    async def _calibrate_confidence(
        self,
        enhanced_result: ReasoningResult,
        context: ReasoningContext
    ) -> ReasoningResult:
        """Calibrate confidence based on context và history"""
        
        # Adjust confidence based on context
        if context.risk_tolerance < 0.3:
            # Conservative adjustment for low risk tolerance
            enhanced_result.confidence *= 0.9
        elif context.risk_tolerance > 0.7:
            # Optimistic adjustment for high risk tolerance
            enhanced_result.confidence *= 1.1
        
        # Adjust based on domain
        domain_adjustments = {
            "tension_resolution": 0.95,  # More conservative
            "agent_creation": 1.0,       # Neutral
            "project_planning": 1.05     # Slightly optimistic
        }
        
        if context.domain in domain_adjustments:
            enhanced_result.confidence *= domain_adjustments[context.domain]
        
        # Ensure bounds
        enhanced_result.confidence = max(0.0, min(1.0, enhanced_result.confidence))
        
        return enhanced_result
    
    async def _assess_reasoning_quality(
        self,
        calibrated_result: ReasoningResult,
        context: ReasoningContext
    ) -> ReasoningResult:
        """Assess overall reasoning quality"""
        
        # Logical consistency assessment
        if len(calibrated_result.reasoning_steps) >= 3:
            calibrated_result.logical_consistency = min(1.0, calibrated_result.confidence + 0.1)
        else:
            calibrated_result.logical_consistency = calibrated_result.confidence * 0.8
        
        # Evidence strength assessment
        evidence_count = len(calibrated_result.supporting_evidence)
        calibrated_result.evidence_strength = min(1.0, evidence_count / 5.0)
        
        # Novelty score assessment
        if calibrated_result.quantum_enhancement > 0:
            calibrated_result.novelty_score = 0.8
        elif calibrated_result.ml_confidence > 0:
            calibrated_result.novelty_score = 0.6
        else:
            calibrated_result.novelty_score = 0.4
        
        return calibrated_result
    
    async def _prepare_training_data(
        self,
        training_data: List[Dict[str, Any]]
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Prepare training data for ML models"""
        
        X = []
        y_confidence = []
        y_reasoning_type = []
        
        for data in training_data:
            # Extract features
            context_dict = data.get("context", {})
            context = ReasoningContext(
                context_id=str(uuid4()),
                domain=context_dict.get("domain", "general"),
                priority_level=context_dict.get("priority_level", 5),
                risk_tolerance=context_dict.get("risk_tolerance", 0.5)
            )
            
            features = context.to_feature_vector()
            features.extend([
                data.get("reasoning_steps_count", 1),
                data.get("evidence_count", 0),
                data.get("complexity_score", 0.5)
            ])
            
            X.append(features)
            y_confidence.append(data.get("confidence", 0.5))
            y_reasoning_type.append(data.get("reasoning_type", "DEDUCTIVE"))
        
        return np.array(X), np.array(y_confidence), np.array(y_reasoning_type)
    
    async def _train_confidence_estimator(self, X: np.ndarray, y: np.ndarray) -> float:
        """Train confidence estimation model"""
        
        try:
            # Scale features
            X_scaled = self.confidence_estimator.scaler.fit_transform(X)
            
            # Train model
            self.confidence_estimator.model.fit(X_scaled, y)
            
            # Calculate accuracy
            predictions = self.confidence_estimator.model.predict(X_scaled)
            accuracy = 1.0 - np.mean(np.abs(predictions - y))
            
            self.confidence_estimator.training_accuracy = accuracy
            
            return accuracy
            
        except Exception as e:
            self.logger.error(f"Failed to train confidence estimator: {e}")
            return 0.0
    
    async def _train_reasoning_predictor(self, X: np.ndarray, y: np.ndarray) -> float:
        """Train reasoning type prediction model"""
        
        try:
            # Scale features
            X_scaled = self.reasoning_predictor.scaler.fit_transform(X)
            
            # Train model
            self.reasoning_predictor.model.fit(X_scaled, y)
            
            # Calculate accuracy
            accuracy = self.reasoning_predictor.model.score(X_scaled, y)
            self.reasoning_predictor.training_accuracy = accuracy
            
            return accuracy
            
        except Exception as e:
            self.logger.error(f"Failed to train reasoning predictor: {e}")
            return 0.0
    
    async def _train_quantum_enhancer(self, X: np.ndarray, y: np.ndarray) -> float:
        """Train quantum enhancement model"""
        
        try:
            # Create binary target for quantum enhancement
            y_binary = (y > 0.7).astype(int)
            
            # Scale features
            X_scaled = self.quantum_enhancer.scaler.fit_transform(X)
            
            # Train model
            self.quantum_enhancer.model.fit(X_scaled, y_binary)
            
            # Calculate accuracy
            accuracy = self.quantum_enhancer.model.score(X_scaled, y_binary)
            self.quantum_enhancer.training_accuracy = accuracy
            
            return accuracy
            
        except Exception as e:
            self.logger.error(f"Failed to train quantum enhancer: {e}")
            return 0.0
    
    async def _update_reasoning_stats(self, result: ReasoningResult) -> None:
        """Update reasoning statistics"""
        
        self.reasoning_stats["total_reasonings"] += 1
        
        if result.confidence > self.confidence_threshold:
            self.reasoning_stats["successful_reasonings"] += 1
        
        # Update averages
        total = self.reasoning_stats["total_reasonings"]
        
        # Average confidence
        avg_conf = self.reasoning_stats["average_confidence"]
        self.reasoning_stats["average_confidence"] = (avg_conf * (total - 1) + result.confidence) / total
        
        # Average reasoning time
        avg_time = self.reasoning_stats["average_reasoning_time"]
        self.reasoning_stats["average_reasoning_time"] = (avg_time * (total - 1) + result.reasoning_time) / total
        
        # Enhancement rates
        if result.ml_confidence > 0:
            self.reasoning_stats["ml_enhancement_rate"] = (
                self.reasoning_stats.get("ml_enhancements", 0) + 1
            ) / total
        
        if result.quantum_enhancement > 0:
            self.reasoning_stats["quantum_enhancement_rate"] = (
                self.reasoning_stats.get("quantum_enhancements", 0) + 1
            ) / total
    
    async def _learn_from_reasoning(
        self,
        query: str,
        context: ReasoningContext,
        result: ReasoningResult
    ) -> None:
        """Learn from reasoning result"""
        
        try:
            # Create learning experience
            experience = LearningExperience(
                agent_id="ml_enhanced_reasoning_engine",
                experience_type=ExperienceType.PATTERN_RECOGNITION,
                action_taken={
                    "action": "enhanced_reasoning",
                    "query": query[:100],
                    "reasoning_type": result.reasoning_type.value,
                    "ml_enhanced": result.ml_confidence > 0,
                    "quantum_enhanced": result.quantum_enhancement > 0
                },
                outcome={
                    "confidence": result.confidence,
                    "reasoning_time": result.reasoning_time,
                    "logical_consistency": result.logical_consistency,
                    "evidence_strength": result.evidence_strength,
                    "novelty_score": result.novelty_score
                },
                success=result.confidence > self.confidence_threshold,
                confidence_level=result.confidence,
                context={
                    "domain": context.domain,
                    "priority_level": context.priority_level,
                    "risk_tolerance": context.risk_tolerance,
                    "reasoning_steps": len(result.reasoning_steps)
                }
            )
            
            # Add to learning system
            await self.learning_system.learn_from_experience(experience)
            
        except Exception as e:
            self.logger.error(f"Failed to learn from reasoning: {e}")
    
    async def _learn_from_training(self, training_result: Dict[str, Any]) -> None:
        """Learn from training result"""
        
        try:
            # Create learning experience
            experience = LearningExperience(
                agent_id="ml_enhanced_reasoning_engine",
                experience_type=ExperienceType.PERFORMANCE_OPTIMIZATION,
                action_taken={
                    "action": "train_ml_models",
                    "training_samples": training_result.get("training_samples", 0),
                    "models_trained": training_result.get("models_trained", 0)
                },
                outcome={
                    "confidence_accuracy": training_result.get("confidence_accuracy", 0.0),
                    "reasoning_accuracy": training_result.get("reasoning_accuracy", 0.0),
                    "quantum_accuracy": training_result.get("quantum_accuracy", 0.0)
                },
                success=training_result.get("confidence_accuracy", 0.0) > 0.7,
                confidence_level=training_result.get("confidence_accuracy", 0.0),
                context={"training_type": "ml_reasoning_models"}
            )
            
            # Add to learning system
            await self.learning_system.learn_from_experience(experience)
            
        except Exception as e:
            self.logger.error(f"Failed to learn from training: {e}")
    
    def _calculate_trend(self, values: List[float]) -> str:
        """Calculate trend direction"""
        if len(values) < 2:
            return "stable"
        
        recent = values[-min(5, len(values)):]
        if len(recent) < 2:
            return "stable"
        
        slope = np.polyfit(range(len(recent)), recent, 1)[0]
        
        if slope > 0.05:
            return "improving"
        elif slope < -0.05:
            return "declining"
        else:
            return "stable"
    
    def _calculate_confidence_distribution(self, confidences: List[float]) -> Dict[str, float]:
        """Calculate confidence level distribution"""
        
        distribution = {level.value: 0 for level in ConfidenceLevel}
        
        for conf in confidences:
            if conf < 0.2:
                distribution["very_low"] += 1
            elif conf < 0.4:
                distribution["low"] += 1
            elif conf < 0.6:
                distribution["medium"] += 1
            elif conf < 0.8:
                distribution["high"] += 1
            else:
                distribution["very_high"] += 1
        
        # Convert to percentages
        total = len(confidences)
        for level in distribution:
            distribution[level] = distribution[level] / total if total > 0 else 0
        
        return distribution
    
    async def _predict_best_reasoning_type(self, features: List[float]) -> str:
        """Predict best reasoning type for given context"""
        
        if not self.reasoning_predictor or not self.reasoning_predictor.trained:
            return ReasoningType.HYBRID.value
        
        try:
            features_scaled = self.reasoning_predictor.scaler.transform([features])
            prediction = self.reasoning_predictor.model.predict(features_scaled)[0]
            return prediction
        except Exception as e:
            self.logger.error(f"Failed to predict reasoning type: {e}")
            return ReasoningType.HYBRID.value 