"""
TRM-OS Adaptive State Detector
Machine Learning-powered quantum state detection và analysis
"""

import asyncio
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import joblib

from .quantum_types import QuantumState, QuantumStateType, WINCategory, ProbabilityDistribution
from ..learning.adaptive_learning_system import AdaptiveLearningSystem
from ..learning.learning_types import LearningExperience, ExperienceType


@dataclass
class StateDetectionResult:
    """Result of quantum state detection"""
    detected_states: List[QuantumState]
    confidence_scores: Dict[str, float]
    probability_distribution: ProbabilityDistribution
    detection_time: float
    ml_predictions: Dict[str, Any]
    anomaly_score: float = 0.0


@dataclass
class OrganizationalSignal:
    """Signal from organizational data for state detection"""
    signal_id: str
    signal_type: str                     # "performance", "communication", "decision", "outcome"
    source: str                          # Data source
    value: float                         # Normalized signal value
    timestamp: datetime
    context: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.context is None:
            self.context = {}


class AdaptiveStateDetector:
    """
    Machine Learning-powered detector cho quantum organizational states
    Sử dụng multiple ML models để detect và predict quantum states
    """
    
    def __init__(self, learning_system: AdaptiveLearningSystem):
        self.learning_system = learning_system
        
        # ML Models
        self.state_classifier = RandomForestClassifier(
            n_estimators=100, 
            max_depth=10, 
            random_state=42
        )
        self.probability_regressor = GradientBoostingRegressor(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=6,
            random_state=42
        )
        self.anomaly_detector = KMeans(n_clusters=5, random_state=42)
        self.feature_scaler = StandardScaler()
        
        # Model training status
        self.models_trained = False
        self.training_data = []
        self.feature_names = []
        
        # Detection parameters
        self.detection_threshold = 0.7      # Minimum confidence for state detection
        self.coherence_threshold = 0.5      # Minimum coherence for quantum state
        self.anomaly_threshold = 2.0        # Threshold for anomaly detection
        
        # State tracking
        self.detected_states_history = []
        self.detection_patterns = {}
        
        # Performance metrics
        self.detection_accuracy = 0.0
        self.false_positive_rate = 0.0
        self.detection_latency = 0.0
        
        # Adaptive parameters
        self.adaptation_rate = 0.1
        self.learning_window = 100          # Number of detections to keep for learning
    
    async def detect_quantum_states(self, organizational_signals: List[OrganizationalSignal]) -> StateDetectionResult:
        """
        Detect quantum states from organizational signals using ML
        """
        start_time = datetime.now()
        
        # Extract features from signals
        features = await self._extract_features(organizational_signals)
        
        # Normalize features
        if self.models_trained:
            normalized_features = self.feature_scaler.transform([features])
        else:
            # First time - fit scaler
            normalized_features = self.feature_scaler.fit_transform([features])
        
        # Detect states using ML models
        detected_states = []
        confidence_scores = {}
        ml_predictions = {}
        
        if self.models_trained:
            # Use trained models
            state_predictions = self.state_classifier.predict_proba(normalized_features)[0]
            probability_predictions = self.probability_regressor.predict(normalized_features)[0]
            anomaly_score = self._calculate_anomaly_score(normalized_features[0])
            
            # Create quantum states from predictions
            for i, (state_type, confidence) in enumerate(zip(QuantumStateType, state_predictions)):
                if confidence > self.detection_threshold:
                    quantum_state = await self._create_quantum_state(
                        state_type, confidence, features, organizational_signals
                    )
                    detected_states.append(quantum_state)
                    confidence_scores[quantum_state.state_id] = confidence
            
            ml_predictions = {
                "state_probabilities": dict(zip([s.value for s in QuantumStateType], state_predictions)),
                "win_probability": probability_predictions,
                "anomaly_score": anomaly_score
            }
        else:
            # Fallback to heuristic detection
            detected_states, confidence_scores = await self._heuristic_detection(
                organizational_signals, features
            )
            anomaly_score = 0.0
        
        # Create probability distribution
        prob_dist = ProbabilityDistribution(
            states={state.state_id: state.probability for state in detected_states},
            confidence=np.mean(list(confidence_scores.values())) if confidence_scores else 0.0
        )
        prob_dist.normalize()
        prob_dist.calculate_entropy()
        
        # Calculate detection time
        detection_time = (datetime.now() - start_time).total_seconds()
        
        # Create result
        result = StateDetectionResult(
            detected_states=detected_states,
            confidence_scores=confidence_scores,
            probability_distribution=prob_dist,
            detection_time=detection_time,
            ml_predictions=ml_predictions,
            anomaly_score=anomaly_score
        )
        
        # Learn from detection
        await self._learn_from_detection(organizational_signals, result)
        
        # Update detection history
        self.detected_states_history.append(result)
        if len(self.detected_states_history) > self.learning_window:
            self.detected_states_history.pop(0)
        
        return result
    
    async def train_models(self, training_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Train ML models với historical data
        """
        if not training_data:
            return {"error": "No training data provided"}
        
        # Prepare training data
        X = []  # Features
        y_states = []  # State labels
        y_probabilities = []  # WIN probabilities
        
        for data_point in training_data:
            features = data_point.get("features", [])
            state_label = data_point.get("state_type", "COHERENCE")
            win_probability = data_point.get("win_probability", 0.5)
            
            X.append(features)
            y_states.append(state_label)
            y_probabilities.append(win_probability)
        
        # Convert to numpy arrays
        X = np.array(X)
        y_states = np.array(y_states)
        y_probabilities = np.array(y_probabilities)
        
        # Scale features
        X_scaled = self.feature_scaler.fit_transform(X)
        
        # Train state classifier
        self.state_classifier.fit(X_scaled, y_states)
        
        # Train probability regressor
        self.probability_regressor.fit(X_scaled, y_probabilities)
        
        # Train anomaly detector
        self.anomaly_detector.fit(X_scaled)
        
        # Update training status
        self.models_trained = True
        self.training_data = training_data
        
        # Calculate training metrics
        state_accuracy = self.state_classifier.score(X_scaled, y_states)
        prob_r2_score = self.probability_regressor.score(X_scaled, y_probabilities)
        
        training_result = {
            "models_trained": True,
            "training_samples": len(training_data),
            "state_classification_accuracy": state_accuracy,
            "probability_prediction_r2": prob_r2_score,
            "feature_count": X.shape[1] if X.shape[0] > 0 else 0
        }
        
        # Learn from training
        await self._learn_from_training(training_result)
        
        return training_result
    
    async def adapt_detection_parameters(self, feedback: Dict[str, Any]) -> Dict[str, Any]:
        """
        Adapt detection parameters based on feedback
        """
        adaptations_made = []
        
        # Adapt detection threshold
        if "detection_accuracy" in feedback:
            accuracy = feedback["detection_accuracy"]
            if accuracy < 0.7:
                # Lower threshold to detect more states
                old_threshold = self.detection_threshold
                self.detection_threshold = max(0.5, self.detection_threshold - 0.1)
                adaptations_made.append(f"Detection threshold: {old_threshold} -> {self.detection_threshold}")
            elif accuracy > 0.9:
                # Raise threshold to be more selective
                old_threshold = self.detection_threshold
                self.detection_threshold = min(0.9, self.detection_threshold + 0.05)
                adaptations_made.append(f"Detection threshold: {old_threshold} -> {self.detection_threshold}")
        
        # Adapt coherence threshold
        if "false_positive_rate" in feedback:
            fp_rate = feedback["false_positive_rate"]
            if fp_rate > 0.2:
                old_coherence = self.coherence_threshold
                self.coherence_threshold = min(0.8, self.coherence_threshold + 0.1)
                adaptations_made.append(f"Coherence threshold: {old_coherence} -> {self.coherence_threshold}")
        
        # Adapt anomaly threshold
        if "anomaly_detection_feedback" in feedback:
            anomaly_feedback = feedback["anomaly_detection_feedback"]
            if anomaly_feedback == "too_sensitive":
                old_anomaly = self.anomaly_threshold
                self.anomaly_threshold *= 1.2
                adaptations_made.append(f"Anomaly threshold: {old_anomaly} -> {self.anomaly_threshold}")
            elif anomaly_feedback == "not_sensitive":
                old_anomaly = self.anomaly_threshold
                self.anomaly_threshold *= 0.8
                adaptations_made.append(f"Anomaly threshold: {old_anomaly} -> {self.anomaly_threshold}")
        
        # Update performance metrics
        if "detection_latency" in feedback:
            self.detection_latency = feedback["detection_latency"]
        
        adaptation_result = {
            "adaptations_made": adaptations_made,
            "new_parameters": {
                "detection_threshold": self.detection_threshold,
                "coherence_threshold": self.coherence_threshold,
                "anomaly_threshold": self.anomaly_threshold
            }
        }
        
        # Learn from adaptation
        await self._learn_from_adaptation(feedback, adaptation_result)
        
        return adaptation_result
    
    async def get_detection_analytics(self) -> Dict[str, Any]:
        """
        Get analytics về detection performance
        """
        if not self.detected_states_history:
            return {"error": "No detection history available"}
        
        # Calculate analytics
        total_detections = len(self.detected_states_history)
        avg_detection_time = np.mean([r.detection_time for r in self.detected_states_history])
        avg_confidence = np.mean([
            np.mean(list(r.confidence_scores.values())) if r.confidence_scores else 0.0
            for r in self.detected_states_history
        ])
        
        # State type distribution
        state_counts = {}
        for result in self.detected_states_history:
            for state in result.detected_states:
                state_type = state.state_type.value
                state_counts[state_type] = state_counts.get(state_type, 0) + 1
        
        # Anomaly statistics
        anomaly_scores = [r.anomaly_score for r in self.detected_states_history]
        avg_anomaly_score = np.mean(anomaly_scores)
        anomaly_count = sum(1 for score in anomaly_scores if score > self.anomaly_threshold)
        
        return {
            "total_detections": total_detections,
            "average_detection_time": avg_detection_time,
            "average_confidence": avg_confidence,
            "state_type_distribution": state_counts,
            "models_trained": self.models_trained,
            "detection_parameters": {
                "detection_threshold": self.detection_threshold,
                "coherence_threshold": self.coherence_threshold,
                "anomaly_threshold": self.anomaly_threshold
            },
            "anomaly_statistics": {
                "average_anomaly_score": avg_anomaly_score,
                "anomaly_detections": anomaly_count,
                "anomaly_rate": anomaly_count / total_detections if total_detections > 0 else 0.0
            }
        }
    
    async def _extract_features(self, signals: List[OrganizationalSignal]) -> List[float]:
        """Extract ML features from organizational signals"""
        if not signals:
            return [0.0] * 20  # Default feature vector
        
        features = []
        
        # Basic signal statistics
        values = [s.value for s in signals]
        features.extend([
            np.mean(values),          # Mean signal value
            np.std(values),           # Signal variance
            np.min(values),           # Minimum value
            np.max(values),           # Maximum value
            len(signals)              # Signal count
        ])
        
        # Signal type distribution
        signal_types = ["performance", "communication", "decision", "outcome"]
        for signal_type in signal_types:
            count = sum(1 for s in signals if s.signal_type == signal_type)
            features.append(count / len(signals) if signals else 0.0)
        
        # Temporal features
        if len(signals) > 1:
            timestamps = [s.timestamp for s in signals]
            time_span = (max(timestamps) - min(timestamps)).total_seconds()
            features.extend([
                time_span,                # Time span of signals
                len(signals) / max(1, time_span)  # Signal frequency
            ])
        else:
            features.extend([0.0, 0.0])
        
        # Signal trend (if enough signals)
        if len(values) >= 3:
            # Simple linear trend
            x = np.arange(len(values))
            trend = np.polyfit(x, values, 1)[0]
            features.append(trend)
        else:
            features.append(0.0)
        
        # Cross-correlation features (simplified)
        if len(signals) >= 2:
            perf_signals = [s.value for s in signals if s.signal_type == "performance"]
            comm_signals = [s.value for s in signals if s.signal_type == "communication"]
            
            if perf_signals and comm_signals:
                # Simple correlation proxy
                perf_avg = np.mean(perf_signals)
                comm_avg = np.mean(comm_signals)
                features.append(perf_avg * comm_avg)  # Interaction term
            else:
                features.append(0.0)
        else:
            features.append(0.0)
        
        # Pad or truncate to fixed size
        target_size = 20
        if len(features) < target_size:
            features.extend([0.0] * (target_size - len(features)))
        elif len(features) > target_size:
            features = features[:target_size]
        
        return features
    
    async def _create_quantum_state(self, state_type: QuantumStateType, confidence: float, 
                                  features: List[float], signals: List[OrganizationalSignal]) -> QuantumState:
        """Create quantum state from detection results"""
        state_id = f"{state_type.value}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Calculate quantum properties
        amplitude = complex(np.sqrt(confidence), 0.0)  # Real amplitude for simplicity
        phase = 0.0  # No phase for basic implementation
        
        # Determine WIN category based on signal types
        signal_types = [s.signal_type for s in signals]
        if "performance" in signal_types:
            win_category = WINCategory.EFFICIENCY
        elif "innovation" in signal_types:
            win_category = WINCategory.INNOVATION
        else:
            win_category = WINCategory.BUSINESS_VALUE
        
        # Extract stakeholders from signals
        stakeholders = []
        for signal in signals:
            if "stakeholder" in signal.context:
                stakeholders.append(signal.context["stakeholder"])
        
        # Calculate decoherence rate based on signal volatility
        signal_values = [s.value for s in signals]
        volatility = np.std(signal_values) if len(signal_values) > 1 else 0.0
        decoherence_rate = volatility * 0.1  # Scale volatility to decoherence rate
        
        return QuantumState(
            state_id=state_id,
            state_type=state_type,
            amplitude=amplitude,
            phase=phase,
            probability=confidence,
            win_category=win_category,
            organizational_level="team",  # Default level
            stakeholders=list(set(stakeholders)),
            coherence_time=1.0 / max(decoherence_rate, 0.01),
            decoherence_rate=decoherence_rate,
            created_at=datetime.now()
        )
    
    async def _heuristic_detection(self, signals: List[OrganizationalSignal], 
                                 features: List[float]) -> Tuple[List[QuantumState], Dict[str, float]]:
        """Fallback heuristic detection when ML models not trained"""
        detected_states = []
        confidence_scores = {}
        
        if not signals:
            return detected_states, confidence_scores
        
        # Simple heuristic rules
        avg_signal_value = np.mean([s.value for s in signals])
        signal_variance = np.std([s.value for s in signals])
        
        # Detect superposition state if high variance
        if signal_variance > 0.3:
            state = await self._create_quantum_state(
                QuantumStateType.SUPERPOSITION, 0.8, features, signals
            )
            detected_states.append(state)
            confidence_scores[state.state_id] = 0.8
        
        # Detect coherence state if high average value and low variance
        if avg_signal_value > 0.7 and signal_variance < 0.2:
            state = await self._create_quantum_state(
                QuantumStateType.COHERENCE, 0.9, features, signals
            )
            detected_states.append(state)
            confidence_scores[state.state_id] = 0.9
        
        # Detect decoherence if low average and high variance
        if avg_signal_value < 0.3 and signal_variance > 0.4:
            state = await self._create_quantum_state(
                QuantumStateType.DECOHERENCE, 0.7, features, signals
            )
            detected_states.append(state)
            confidence_scores[state.state_id] = 0.7
        
        return detected_states, confidence_scores
    
    def _calculate_anomaly_score(self, features: np.ndarray) -> float:
        """Calculate anomaly score using trained anomaly detector"""
        if not self.models_trained:
            return 0.0
        
        # Get cluster assignment and distance
        cluster_id = self.anomaly_detector.predict([features])[0]
        cluster_center = self.anomaly_detector.cluster_centers_[cluster_id]
        
        # Calculate distance to cluster center
        distance = np.linalg.norm(features - cluster_center)
        
        return distance
    
    async def _learn_from_detection(self, signals: List[OrganizationalSignal], 
                                  result: StateDetectionResult) -> None:
        """Learn from detection experience"""
        try:
            experience = LearningExperience(
                experience_type=ExperienceType.PATTERN_RECOGNITION,
                agent_id="quantum_state_detector",
                context={
                    "signal_count": len(signals),
                    "states_detected": len(result.detected_states),
                    "detection_time": result.detection_time,
                    "anomaly_score": result.anomaly_score
                },
                action_taken={
                    "action": "detect_quantum_states",
                    "ml_models_used": self.models_trained,
                    "detection_method": "ml" if self.models_trained else "heuristic"
                },
                outcome={
                    "states_detected": [s.state_type.value for s in result.detected_states],
                    "confidence_scores": result.confidence_scores,
                    "probability_distribution": result.probability_distribution.states,
                    "success": len(result.detected_states) > 0
                },
                success=len(result.detected_states) > 0,
                duration_seconds=result.detection_time,
                confidence_level=result.probability_distribution.confidence,
                importance_weight=0.8
            )
            
            await self.learning_system.learn_from_experience(experience)
        except Exception as e:
            print(f"Detection learning error: {e}")
    
    async def _learn_from_training(self, training_result: Dict[str, Any]) -> None:
        """Learn from model training experience"""
        try:
            experience = LearningExperience(
                experience_type=ExperienceType.PERFORMANCE_OPTIMIZATION,
                agent_id="quantum_state_detector",
                context={
                    "training_samples": training_result["training_samples"],
                    "feature_count": training_result["feature_count"]
                },
                action_taken={
                    "action": "train_ml_models",
                    "models": ["state_classifier", "probability_regressor", "anomaly_detector"]
                },
                outcome={
                    "state_classification_accuracy": training_result["state_classification_accuracy"],
                    "probability_prediction_r2": training_result["probability_prediction_r2"],
                    "models_trained": training_result["models_trained"],
                    "success": training_result["models_trained"]
                },
                success=training_result["models_trained"],
                confidence_level=training_result["state_classification_accuracy"],
                importance_weight=1.0
            )
            
            await self.learning_system.learn_from_experience(experience)
        except Exception as e:
            print(f"Training learning error: {e}")
    
    async def _learn_from_adaptation(self, feedback: Dict[str, Any], 
                                   adaptation_result: Dict[str, Any]) -> None:
        """Learn from parameter adaptation experience"""
        try:
            experience = LearningExperience(
                experience_type=ExperienceType.BEHAVIORAL_ADAPTATION,
                agent_id="quantum_state_detector",
                context=feedback,
                action_taken={
                    "action": "adapt_detection_parameters",
                    "adaptations_count": len(adaptation_result["adaptations_made"])
                },
                outcome={
                    "adaptations_made": adaptation_result["adaptations_made"],
                    "new_parameters": adaptation_result["new_parameters"],
                    "success": len(adaptation_result["adaptations_made"]) > 0
                },
                success=len(adaptation_result["adaptations_made"]) > 0,
                confidence_level=0.7,
                importance_weight=0.9
            )
            
            await self.learning_system.learn_from_experience(experience)
        except Exception as e:
            print(f"Adaptation learning error: {e}")
    
    async def save_models(self, filepath: str) -> bool:
        """Save trained models to file"""
        try:
            if self.models_trained:
                model_data = {
                    "state_classifier": self.state_classifier,
                    "probability_regressor": self.probability_regressor,
                    "anomaly_detector": self.anomaly_detector,
                    "feature_scaler": self.feature_scaler,
                    "detection_threshold": self.detection_threshold,
                    "coherence_threshold": self.coherence_threshold,
                    "anomaly_threshold": self.anomaly_threshold
                }
                joblib.dump(model_data, filepath)
                return True
            return False
        except Exception as e:
            print(f"Model save error: {e}")
            return False
    
    async def load_models(self, filepath: str) -> bool:
        """Load trained models from file"""
        try:
            model_data = joblib.load(filepath)
            self.state_classifier = model_data["state_classifier"]
            self.probability_regressor = model_data["probability_regressor"]
            self.anomaly_detector = model_data["anomaly_detector"]
            self.feature_scaler = model_data["feature_scaler"]
            self.detection_threshold = model_data.get("detection_threshold", 0.7)
            self.coherence_threshold = model_data.get("coherence_threshold", 0.5)
            self.anomaly_threshold = model_data.get("anomaly_threshold", 2.0)
            self.models_trained = True
            return True
        except Exception as e:
            print(f"Model load error: {e}")
            return False 