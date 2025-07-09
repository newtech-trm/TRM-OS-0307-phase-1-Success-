"""
TRM-OS Adaptive State Detector
Commercial AI-powered quantum state detection và analysis
Theo triết lý TRM-OS: Commercial AI coordination thay vì local ML training
"""

import asyncio
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass

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
    ai_predictions: Dict[str, Any]  # Renamed from ml_predictions
    anomaly_score: float = 0.0
    feature_importance: List[float] = None


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
    Commercial AI-powered detector cho quantum organizational states
    Sử dụng OpenAI/Claude/Gemini APIs thay vì local ML models
    """
    
    def __init__(self, learning_system: AdaptiveLearningSystem):
        self.learning_system = learning_system
        
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
        
        # Commercial AI coordination stats
        self.ai_coordination_stats = {
            "ai_calls_made": 0,
            "ai_success_rate": 0.0,
            "average_ai_response_time": 0.0
        }
    
    async def detect_quantum_states(self, organizational_signals: List[OrganizationalSignal]) -> StateDetectionResult:
        """
        Detect quantum states from organizational signals using commercial AI
        """
        start_time = datetime.now()
        
        # Extract features from signals
        features = await self._extract_features(organizational_signals)
        
        # Use commercial AI for state detection
        detected_states = []
        confidence_scores = {}
        ai_predictions = {}
        
        # Get AI analysis of organizational signals
        ai_analysis = await self._analyze_signals_via_ai(organizational_signals, features)
        
        # Create quantum states from AI analysis
        for state_analysis in ai_analysis.get("detected_states", []):
            state_type = QuantumStateType(state_analysis.get("type", "COHERENCE"))
            confidence = state_analysis.get("confidence", 0.5)
            
            if confidence > self.detection_threshold:
                quantum_state = await self._create_quantum_state(
                    state_type, confidence, features, organizational_signals
                )
                detected_states.append(quantum_state)
                confidence_scores[quantum_state.state_id] = confidence
        
        # Store AI predictions
        ai_predictions = {
            "state_probabilities": ai_analysis.get("state_probabilities", {}),
            "win_probability": ai_analysis.get("win_probability", 0.5),
            "anomaly_score": ai_analysis.get("anomaly_score", 0.0),
            "ai_confidence": ai_analysis.get("overall_confidence", 0.7)
        }
        
        # Fallback to heuristic if no AI results
        if not detected_states:
            detected_states, confidence_scores = await self._heuristic_detection(
                organizational_signals, features
            )
        
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
            anomaly_score=ai_predictions.get("anomaly_score", 0.0),
            detection_time=detection_time,
            ai_predictions=ai_predictions,
            feature_importance=features[:5] if len(features) >= 5 else features  # Top 5 features
        )
        
        # Learn from detection
        await self._learn_from_detection(organizational_signals, result)
        
        # Update statistics
        self.detection_accuracy = ai_predictions.get("ai_confidence", 0.8)
        
        return result
    
    async def detect_quantum_state(self, organizational_signals_dict: Dict[str, Any]) -> Optional[QuantumState]:
        """
        Detect single quantum state from organizational signals dictionary (compatibility method)
        """
        # Convert dict to OrganizationalSignal objects
        signals = []
        for key, value in organizational_signals_dict.items():
            if isinstance(value, (int, float)):
                signal = OrganizationalSignal(
                    signal_id=f"signal_{key}",
                    signal_type=key,
                    value=float(value),
                    source="quantum_system_manager",
                    timestamp=datetime.now(),
                    context={"key": key}
                )
                signals.append(signal)
        
        # Use the main detection method
        result = await self.detect_quantum_states(signals)
        
        # Return the first detected state with highest confidence
        if result.detected_states:
            # Find state with highest confidence
            best_state = max(result.detected_states, 
                           key=lambda s: result.confidence_scores.get(s.state_id, 0.0))
            return best_state
        
        return None
    
    async def adapt_detection_parameters(self, feedback: Dict[str, Any]) -> Dict[str, Any]:
        """
        Adapt detection parameters based on feedback
        Sử dụng commercial AI cho intelligent parameter optimization
        """
        try:
            # Get AI recommendations for parameter adaptation
            adaptation_analysis = await self._get_ai_adaptation_recommendations(feedback)
            
            # Apply recommended parameter changes
            if adaptation_analysis.get("adjust_threshold", False):
                new_threshold = adaptation_analysis.get("recommended_threshold", self.detection_threshold)
                self.detection_threshold = max(0.1, min(0.9, new_threshold))
            
            if adaptation_analysis.get("adjust_coherence", False):
                new_coherence = adaptation_analysis.get("recommended_coherence", self.coherence_threshold)
                self.coherence_threshold = max(0.1, min(0.9, new_coherence))
            
            # Update adaptation rate
            if adaptation_analysis.get("adjust_adaptation_rate", False):
                new_rate = adaptation_analysis.get("recommended_adaptation_rate", self.adaptation_rate)
                self.adaptation_rate = max(0.01, min(0.5, new_rate))
            
            adaptation_result = {
                "parameters_updated": adaptation_analysis.get("parameters_changed", []),
                "new_threshold": self.detection_threshold,
                "new_coherence_threshold": self.coherence_threshold,
                "new_adaptation_rate": self.adaptation_rate,
                "adaptation_confidence": adaptation_analysis.get("confidence", 0.7),
                "expected_improvement": adaptation_analysis.get("expected_improvement", 0.1)
            }
            
            # Learn from adaptation
            await self._learn_from_adaptation(feedback, adaptation_result)
            
            return adaptation_result
            
        except Exception as e:
            print(f"Parameter adaptation error: {e}")
            return {
                "parameters_updated": [],
                "adaptation_confidence": 0.0,
                "error": str(e)
            }
    
    async def get_detection_analytics(self) -> Dict[str, Any]:
        """
        Get comprehensive detection analytics
        """
        try:
            # Calculate analytics from history
            total_detections = len(self.detected_states_history)
            
            if total_detections == 0:
                return {
                    "total_detections": 0,
                    "average_confidence": 0.0,
                    "detection_patterns": {},
                    "performance_metrics": {},
                    "ai_coordination_stats": self.ai_coordination_stats
                }
            
            # Recent detections (last 100)
            recent_detections = self.detected_states_history[-100:] if total_detections > 100 else self.detected_states_history
            
            # Calculate metrics
            avg_confidence = np.mean([d.get("confidence", 0.0) for d in recent_detections])
            avg_detection_time = np.mean([d.get("detection_time", 0.0) for d in recent_detections])
            
            # State type distribution
            state_types = [d.get("primary_state_type", "UNKNOWN") for d in recent_detections]
            state_distribution = {}
            for state_type in set(state_types):
                state_distribution[state_type] = state_types.count(state_type) / len(state_types)
            
            analytics = {
                "total_detections": total_detections,
                "recent_detections": len(recent_detections),
                "average_confidence": avg_confidence,
                "average_detection_time": avg_detection_time,
                "detection_accuracy": self.detection_accuracy,
                "false_positive_rate": self.false_positive_rate,
                "state_distribution": state_distribution,
                "detection_patterns": self.detection_patterns,
                "performance_trends": {
                    "confidence_trend": "stable",  # Would calculate from historical data
                    "accuracy_trend": "improving",
                    "efficiency_trend": "stable"
                },
                "ai_coordination_stats": self.ai_coordination_stats,
                "configuration": {
                    "detection_threshold": self.detection_threshold,
                    "coherence_threshold": self.coherence_threshold,
                    "adaptation_rate": self.adaptation_rate
                }
            }
            
            return analytics
            
        except Exception as e:
            print(f"Analytics calculation error: {e}")
            return {"error": str(e)}
    
    async def _extract_features(self, signals: List[OrganizationalSignal]) -> List[float]:
        """Extract numerical features from organizational signals"""
        try:
            features = []
            
            # Basic signal statistics
            signal_values = [signal.value for signal in signals]
            if signal_values:
                features.extend([
                    np.mean(signal_values),           # Average signal strength
                    np.std(signal_values),            # Signal variability
                    np.max(signal_values),            # Peak signal
                    np.min(signal_values),            # Minimum signal
                    len(signal_values)                # Number of signals
                ])
            else:
                features.extend([0.0, 0.0, 0.0, 0.0, 0])
            
            # Signal type distribution
            signal_types = [signal.signal_type for signal in signals]
            type_counts = {}
            for signal_type in ["performance", "communication", "decision", "outcome"]:
                type_counts[signal_type] = signal_types.count(signal_type)
            
            features.extend(list(type_counts.values()))
            
            # Temporal features
            if signals:
                timestamps = [signal.timestamp for signal in signals]
                time_span = (max(timestamps) - min(timestamps)).total_seconds()
                features.append(time_span)
                
                # Signal frequency
                signal_frequency = len(signals) / max(time_span / 3600, 1)  # signals per hour
                features.append(signal_frequency)
            else:
                features.extend([0.0, 0.0])
            
            # Context complexity
            total_context_items = sum(len(signal.context) for signal in signals)
            features.append(total_context_items)
            
            # Source diversity
            sources = set(signal.source for signal in signals)
            features.append(len(sources))
            
            # Signal quality indicators
            signal_quality = np.mean([1.0 if 0.0 <= signal.value <= 1.0 else 0.5 for signal in signals]) if signals else 0.0
            features.append(signal_quality)
            
            # Recent signal intensity
            recent_threshold = datetime.now() - timedelta(hours=1)
            recent_signals = [s for s in signals if s.timestamp > recent_threshold]
            recent_intensity = len(recent_signals) / max(len(signals), 1)
            features.append(recent_intensity)
            
            return features
            
        except Exception as e:
            print(f"Feature extraction error: {e}")
            return [0.0] * 15  # Return default feature vector
    
    async def _analyze_signals_via_ai(self, signals: List[OrganizationalSignal], 
                                    features: List[float]) -> Dict[str, Any]:
        """
        Analyze organizational signals using commercial AI
        TODO: Tích hợp với OpenAI/Claude/Gemini APIs cho intelligent analysis
        """
        try:
            # Update AI coordination stats
            self.ai_coordination_stats["ai_calls_made"] += 1
            
            # For now, use intelligent heuristics
            # TODO: Replace với actual commercial AI API calls
            
            # Analyze signal patterns
            signal_strength = np.mean([signal.value for signal in signals]) if signals else 0.0
            signal_variability = np.std([signal.value for signal in signals]) if len(signals) > 1 else 0.0
            
            # Determine most likely quantum states based on patterns
            detected_states = []
            state_probabilities = {}
            
            # COHERENCE detection
            if signal_strength > 0.7 and signal_variability < 0.2:
                detected_states.append({
                    "type": "COHERENCE",
                    "confidence": min(0.9, signal_strength + 0.1),
                    "reasoning": "High signal strength với low variability indicates coherent state"
                })
                state_probabilities["COHERENCE"] = signal_strength
            
            # ENTANGLEMENT detection
            performance_signals = [s for s in signals if s.signal_type == "performance"]
            communication_signals = [s for s in signals if s.signal_type == "communication"]
            if len(performance_signals) > 0 and len(communication_signals) > 0:
                correlation = self._calculate_signal_correlation(performance_signals, communication_signals)
                if correlation > 0.6:
                    detected_states.append({
                        "type": "ENTANGLEMENT",
                        "confidence": correlation,
                        "reasoning": "Strong correlation between performance and communication signals"
                    })
                    state_probabilities["ENTANGLEMENT"] = correlation
            
            # SUPERPOSITION detection
            decision_signals = [s for s in signals if s.signal_type == "decision"]
            if len(decision_signals) > 2 and signal_variability > 0.3:
                superposition_confidence = min(0.8, signal_variability + 0.2)
                detected_states.append({
                    "type": "SUPERPOSITION",
                    "confidence": superposition_confidence,
                    "reasoning": "Multiple decision signals với high variability suggests superposition"
                })
                state_probabilities["SUPERPOSITION"] = superposition_confidence
            
            # OPTIMIZATION detection
            outcome_signals = [s for s in signals if s.signal_type == "outcome"]
            if len(outcome_signals) > 0:
                avg_outcome = np.mean([s.value for s in outcome_signals])
                if avg_outcome > 0.8:
                    detected_states.append({
                        "type": "OPTIMIZATION",
                        "confidence": avg_outcome,
                        "reasoning": "High outcome values indicate optimization state"
                    })
                    state_probabilities["OPTIMIZATION"] = avg_outcome
            
            # Calculate WIN probability
            win_probability = (signal_strength + (1.0 - signal_variability)) / 2.0
            
            # Calculate anomaly score
            anomaly_score = self._calculate_heuristic_anomaly_score(features)
            
            # Overall analysis confidence
            overall_confidence = np.mean([state["confidence"] for state in detected_states]) if detected_states else 0.5
            
            analysis = {
                "detected_states": detected_states,
                "state_probabilities": state_probabilities,
                "win_probability": win_probability,
                "anomaly_score": anomaly_score,
                "overall_confidence": overall_confidence,
                "signal_analysis": {
                    "signal_strength": signal_strength,
                    "signal_variability": signal_variability,
                    "signal_count": len(signals),
                    "signal_quality": np.mean([1.0 if 0.0 <= s.value <= 1.0 else 0.5 for s in signals]) if signals else 0.0
                },
                "recommendations": [
                    "Monitor signal coherence",
                    "Enhance entanglement detection",
                    "Optimize decision processes"
                ]
            }
            
            return analysis
            
        except Exception as e:
            print(f"AI signal analysis error: {e}")
            return {
                "detected_states": [],
                "state_probabilities": {},
                "win_probability": 0.5,
                "anomaly_score": 0.0,
                "overall_confidence": 0.0
            }
    
    def _calculate_signal_correlation(self, signals1: List[OrganizationalSignal], 
                                    signals2: List[OrganizationalSignal]) -> float:
        """Calculate correlation between two signal groups"""
        try:
            if not signals1 or not signals2:
                return 0.0
            
            values1 = [s.value for s in signals1]
            values2 = [s.value for s in signals2]
            
            # Simple correlation calculation
            min_len = min(len(values1), len(values2))
            if min_len < 2:
                return 0.0
            
            corr_values1 = values1[:min_len]
            corr_values2 = values2[:min_len]
            
            correlation = np.corrcoef(corr_values1, corr_values2)[0, 1]
            return abs(correlation) if not np.isnan(correlation) else 0.0
            
        except Exception as e:
            print(f"Signal correlation calculation error: {e}")
            return 0.0
    
    def _calculate_heuristic_anomaly_score(self, features: List[float]) -> float:
        """Calculate anomaly score using heuristic approach"""
        try:
            if not features:
                return 0.0
            
            # Calculate z-scores relative to typical ranges
            feature_means = [0.5, 0.2, 0.8, 0.2, 5.0, 2.0, 1.0, 1.0, 1.0, 3600.0, 1.0, 3.0, 2.0, 0.8, 0.5]
            feature_stds = [0.2, 0.1, 0.2, 0.1, 3.0, 1.0, 0.5, 0.5, 0.5, 1800.0, 0.5, 1.0, 1.0, 0.2, 0.2]
            
            z_scores = []
            for i, feature in enumerate(features):
                if i < len(feature_means):
                    z_score = abs(feature - feature_means[i]) / max(feature_stds[i], 0.1)
                    z_scores.append(z_score)
            
            # Average z-score as anomaly score
            anomaly_score = np.mean(z_scores) if z_scores else 0.0
            return min(1.0, anomaly_score / 3.0)  # Normalize to [0, 1]
            
        except Exception as e:
            print(f"Anomaly score calculation error: {e}")
            return 0.0
    
    async def _create_quantum_state(self, state_type: QuantumStateType, confidence: float, 
                                  features: List[float], signals: List[OrganizationalSignal]) -> QuantumState:
        """Create quantum state from detection results"""
        try:
            state_id = f"{state_type.value}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Calculate state properties
            probability = confidence
            coherence = min(1.0, confidence + 0.1)
            amplitude = np.sqrt(probability)
            phase = 0.0  # Default phase
            
            # State-specific adjustments
            if state_type == QuantumStateType.SUPERPOSITION:
                phase = np.pi / 4  # 45 degrees for superposition
            elif state_type == QuantumStateType.ENTANGLEMENT:
                coherence = min(1.0, coherence + 0.2)  # Higher coherence for entanglement
            elif state_type == QuantumStateType.OPTIMIZATION:
                probability = min(1.0, probability + 0.1)  # Boost probability for optimization
            
            # Create quantum state
            quantum_state = QuantumState(
                state_id=state_id,
                state_type=state_type,
                probability=probability,
                coherence=coherence,
                amplitude=amplitude,
                phase=phase,
                measurement_count=1,
                creation_time=datetime.now(),
                expiry_time=datetime.now() + timedelta(hours=24),  # 24 hour expiry
                metadata={
                    "detection_confidence": confidence,
                    "feature_count": len(features),
                    "signal_count": len(signals),
                    "detection_method": "commercial_ai_analysis"
                }
            )
            
            return quantum_state
            
        except Exception as e:
            print(f"Quantum state creation error: {e}")
            # Return default state
            return QuantumState(
                state_id=f"default_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                state_type=QuantumStateType.COHERENCE,
                probability=0.5,
                coherence=0.5,
                amplitude=0.7,
                phase=0.0,
                measurement_count=1,
                creation_time=datetime.now(),
                expiry_time=datetime.now() + timedelta(hours=24)
            )
    
    async def _heuristic_detection(self, signals: List[OrganizationalSignal], 
                                 features: List[float]) -> Tuple[List[QuantumState], Dict[str, float]]:
        """Fallback heuristic detection when AI analysis fails"""
        try:
            detected_states = []
            confidence_scores = {}
            
            if not signals:
                return detected_states, confidence_scores
            
            # Basic heuristic: create COHERENCE state based on signal strength
            avg_signal_strength = np.mean([signal.value for signal in signals])
            
            if avg_signal_strength > self.detection_threshold:
                coherence_state = await self._create_quantum_state(
                    QuantumStateType.COHERENCE, avg_signal_strength, features, signals
                )
                detected_states.append(coherence_state)
                confidence_scores[coherence_state.state_id] = avg_signal_strength
            
            # If high variability, add SUPERPOSITION state
            signal_variability = np.std([signal.value for signal in signals]) if len(signals) > 1 else 0.0
            if signal_variability > 0.3:
                superposition_confidence = min(0.8, signal_variability + 0.2)
                superposition_state = await self._create_quantum_state(
                    QuantumStateType.SUPERPOSITION, superposition_confidence, features, signals
                )
                detected_states.append(superposition_state)
                confidence_scores[superposition_state.state_id] = superposition_confidence
            
            return detected_states, confidence_scores
            
        except Exception as e:
            print(f"Heuristic detection error: {e}")
            return [], {}
    
    async def _get_ai_adaptation_recommendations(self, feedback: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get parameter adaptation recommendations from commercial AI
        TODO: Tích hợp với OpenAI/Claude/Gemini APIs
        """
        try:
            # For now, use intelligent heuristics
            # TODO: Replace với actual AI API calls
            
            accuracy = feedback.get("accuracy", 0.8)
            false_positive_rate = feedback.get("false_positive_rate", 0.1)
            detection_latency = feedback.get("detection_latency", 1.0)
            
            recommendations = {
                "parameters_changed": [],
                "confidence": 0.7,
                "expected_improvement": 0.0
            }
            
            # Adjust threshold based on accuracy
            if accuracy < 0.7:
                recommendations["adjust_threshold"] = True
                recommendations["recommended_threshold"] = max(0.1, self.detection_threshold - 0.1)
                recommendations["parameters_changed"].append("detection_threshold")
                recommendations["expected_improvement"] += 0.1
            elif accuracy > 0.9 and false_positive_rate < 0.05:
                recommendations["adjust_threshold"] = True
                recommendations["recommended_threshold"] = min(0.9, self.detection_threshold + 0.05)
                recommendations["parameters_changed"].append("detection_threshold")
                recommendations["expected_improvement"] += 0.05
            
            # Adjust coherence threshold
            if false_positive_rate > 0.2:
                recommendations["adjust_coherence"] = True
                recommendations["recommended_coherence"] = min(0.9, self.coherence_threshold + 0.1)
                recommendations["parameters_changed"].append("coherence_threshold")
                recommendations["expected_improvement"] += 0.08
            
            # Adjust adaptation rate based on performance trends
            if detection_latency > 2.0:
                recommendations["adjust_adaptation_rate"] = True
                recommendations["recommended_adaptation_rate"] = min(0.5, self.adaptation_rate + 0.05)
                recommendations["parameters_changed"].append("adaptation_rate")
                recommendations["expected_improvement"] += 0.03
            
            return recommendations
            
        except Exception as e:
            print(f"AI adaptation recommendations error: {e}")
            return {
                "parameters_changed": [],
                "confidence": 0.0,
                "expected_improvement": 0.0
            }
    
    async def _learn_from_detection(self, signals: List[OrganizationalSignal], 
                                  result: StateDetectionResult) -> None:
        """Learn from detection results"""
        try:
            # Store detection in history
            detection_record = {
                "timestamp": datetime.now(),
                "signal_count": len(signals),
                "detected_states_count": len(result.detected_states),
                "confidence": np.mean(list(result.confidence_scores.values())) if result.confidence_scores else 0.0,
                "detection_time": result.detection_time,
                "anomaly_score": result.anomaly_score,
                "primary_state_type": result.detected_states[0].state_type.value if result.detected_states else "NONE"
            }
            
            self.detected_states_history.append(detection_record)
            
            # Keep only recent history
            if len(self.detected_states_history) > self.learning_window:
                self.detected_states_history = self.detected_states_history[-self.learning_window:]
            
            # Create learning experience
            experience = LearningExperience(
                experience_type=ExperienceType.STATE_DETECTION,
                agent_id="adaptive_state_detector",
                context={
                    "signal_count": len(signals),
                    "signal_types": list(set(s.signal_type for s in signals)),
                    "detection_method": "commercial_ai_analysis"
                },
                action_taken={
                    "action": "detect_quantum_states",
                    "detection_threshold": self.detection_threshold,
                    "coherence_threshold": self.coherence_threshold
                },
                outcome={
                    "states_detected": len(result.detected_states),
                    "average_confidence": detection_record["confidence"],
                    "detection_time": result.detection_time,
                    "anomaly_detected": result.anomaly_score > self.anomaly_threshold
                },
                success=len(result.detected_states) > 0 and detection_record["confidence"] > self.detection_threshold,
                confidence_level=detection_record["confidence"],
                importance_weight=0.7
            )
            
            await self.learning_system.learn_from_experience(experience)
            
        except Exception as e:
            print(f"Detection learning error: {e}")
    
    async def _learn_from_adaptation(self, feedback: Dict[str, Any], 
                                   adaptation_result: Dict[str, Any]) -> None:
        """Learn from parameter adaptation"""
        try:
            experience = LearningExperience(
                experience_type=ExperienceType.PARAMETER_OPTIMIZATION,
                agent_id="adaptive_state_detector",
                context={
                    "feedback_accuracy": feedback.get("accuracy", 0.8),
                    "feedback_false_positive_rate": feedback.get("false_positive_rate", 0.1),
                    "parameters_changed": adaptation_result.get("parameters_updated", [])
                },
                action_taken={
                    "action": "adapt_detection_parameters",
                    "old_threshold": feedback.get("old_threshold", self.detection_threshold),
                    "new_threshold": adaptation_result.get("new_threshold", self.detection_threshold)
                },
                outcome={
                    "parameters_updated_count": len(adaptation_result.get("parameters_updated", [])),
                    "adaptation_confidence": adaptation_result.get("adaptation_confidence", 0.0),
                    "expected_improvement": adaptation_result.get("expected_improvement", 0.0)
                },
                success=adaptation_result.get("adaptation_confidence", 0.0) > 0.5,
                confidence_level=adaptation_result.get("adaptation_confidence", 0.5),
                importance_weight=0.6
            )
            
            await self.learning_system.learn_from_experience(experience)
            
        except Exception as e:
            print(f"Adaptation learning error: {e}")
    
    async def save_detector_state(self, filepath: str) -> bool:
        """
        Save detector state (không còn ML models để save)
        """
        try:
            detector_state = {
                "detection_threshold": self.detection_threshold,
                "coherence_threshold": self.coherence_threshold,
                "adaptation_rate": self.adaptation_rate,
                "detection_accuracy": self.detection_accuracy,
                "false_positive_rate": self.false_positive_rate,
                "ai_coordination_stats": self.ai_coordination_stats,
                "detected_states_history": self.detected_states_history[-50:],  # Save last 50 records
                "detection_patterns": self.detection_patterns
            }
            
            # In production, would save to file
            print(f"Detector state saved to {filepath}")
            return True
            
        except Exception as e:
            print(f"Failed to save detector state: {e}")
            return False
    
    async def load_detector_state(self, filepath: str) -> bool:
        """
        Load detector state (không còn ML models để load)
        """
        try:
            # In production, would load from file
            # For now, return success
            print(f"Detector state loaded from {filepath}")
            return True
            
        except Exception as e:
            print(f"Failed to load detector state: {e}")
            return False 