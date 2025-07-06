"""
Uncertainty Handler - Component for handling uncertainty in reasoning

Provides probabilistic reasoning and uncertainty quantification capabilities
for the Advanced Reasoning Engine.
"""

import logging
import math
from typing import Dict, List, Any, Optional, Tuple
from statistics import mean, stdev
from collections import Counter

from .reasoning_types import ReasoningResult, ReasoningStep, UncertaintyLevel


class UncertaintyHandler:
    """
    Handles uncertainty quantification and probabilistic reasoning
    
    Core capabilities:
    1. Confidence level assessment and propagation
    2. Uncertainty source identification
    3. Probabilistic inference
    4. Risk assessment for reasoning conclusions
    5. Uncertainty-aware decision recommendations
    """
    
    def __init__(self):
        self.logger = logging.getLogger("reasoning.uncertainty_handler")
        
        # Uncertainty models and thresholds
        self.confidence_thresholds = {
            UncertaintyLevel.CERTAIN: 0.9,
            UncertaintyLevel.HIGH_CONFIDENCE: 0.7,
            UncertaintyLevel.MODERATE: 0.5,
            UncertaintyLevel.LOW_CONFIDENCE: 0.3,
            UncertaintyLevel.UNCERTAIN: 0.0
        }
        
        # Factors that affect uncertainty
        self.uncertainty_factors = {
            "data_quality": {
                "high": 0.1,      # Low uncertainty addition
                "medium": 0.2,
                "low": 0.4        # High uncertainty addition
            },
            "data_completeness": {
                "complete": 0.05,
                "partial": 0.15,
                "sparse": 0.3
            },
            "temporal_distance": {
                "immediate": 0.05,
                "recent": 0.1,
                "historical": 0.2,
                "ancient": 0.35
            },
            "complexity": {
                "simple": 0.05,
                "moderate": 0.15,
                "complex": 0.25,
                "very_complex": 0.4
            }
        }
    
    async def assess_uncertainty(self, result: ReasoningResult) -> Dict[str, Any]:
        """
        Assess overall uncertainty in reasoning results
        
        Args:
            result: ReasoningResult to analyze
            
        Returns:
            Dictionary with uncertainty assessment details
        """
        self.logger.info(f"Assessing uncertainty for reasoning session {result.result_id}")
        
        assessment = {
            "overall_level": UncertaintyLevel.MODERATE,
            "overall_score": 0.5,
            "confidence_variance": 0.0,
            "sources": [],
            "risk_factors": [],
            "recommendations": []
        }
        
        try:
            # Analyze confidence distribution across steps
            confidence_analysis = self._analyze_confidence_distribution(result.steps)
            assessment.update(confidence_analysis)
            
            # Identify uncertainty sources
            uncertainty_sources = self._identify_uncertainty_sources(result)
            assessment["sources"] = uncertainty_sources
            
            # Assess data quality factors
            data_quality_assessment = self._assess_data_quality(result)
            assessment["data_quality"] = data_quality_assessment
            
            # Calculate overall uncertainty score
            overall_score = self._calculate_overall_uncertainty(
                confidence_analysis, uncertainty_sources, data_quality_assessment
            )
            assessment["overall_score"] = overall_score
            assessment["overall_level"] = self._score_to_uncertainty_level(overall_score)
            
            # Generate risk factors and recommendations
            assessment["risk_factors"] = self._identify_risk_factors(result, overall_score)
            assessment["recommendations"] = self._generate_uncertainty_recommendations(
                overall_score, uncertainty_sources
            )
            
            # Safe access to enum value
            uncertainty_level_value = assessment['overall_level'].value if hasattr(assessment['overall_level'], 'value') else str(assessment['overall_level'])
            self.logger.info(
                f"Uncertainty assessment complete: {uncertainty_level_value} "
                f"(score: {overall_score:.3f})"
            )
            
        except Exception as e:
            self.logger.error(f"Error in uncertainty assessment: {str(e)}")
            assessment["error"] = str(e)
        
        return assessment
    
    def propagate_uncertainty(
        self, 
        input_confidences: List[float], 
        operation_type: str = "conjunction"
    ) -> float:
        """
        Propagate uncertainty through reasoning operations
        
        Args:
            input_confidences: List of input confidence values
            operation_type: Type of logical operation (conjunction, disjunction, etc.)
            
        Returns:
            Propagated confidence value
        """
        if not input_confidences:
            return 0.0
        
        if operation_type == "conjunction":
            # For AND operations, use product (weakest link)
            result = 1.0
            for conf in input_confidences:
                result *= conf
            return result
            
        elif operation_type == "disjunction":
            # For OR operations, use probabilistic sum
            result = 0.0
            for conf in input_confidences:
                result = result + conf - (result * conf)
            return result
            
        elif operation_type == "weighted_average":
            # Weighted average with higher weight for higher confidence
            weights = [conf ** 2 for conf in input_confidences]  # Square for emphasis
            if sum(weights) == 0:
                return mean(input_confidences)
            return sum(c * w for c, w in zip(input_confidences, weights)) / sum(weights)
            
        elif operation_type == "conservative":
            # Conservative approach - use minimum confidence
            return min(input_confidences)
            
        elif operation_type == "optimistic":
            # Optimistic approach - use maximum confidence
            return max(input_confidences)
            
        else:
            # Default to arithmetic mean
            return mean(input_confidences)
    
    def calculate_epistemic_uncertainty(
        self, 
        predictions: List[Dict[str, Any]]
    ) -> float:
        """
        Calculate epistemic uncertainty (model uncertainty)
        
        Args:
            predictions: List of predictions with confidence scores
            
        Returns:
            Epistemic uncertainty score (0-1)
        """
        if len(predictions) <= 1:
            return 0.5  # High uncertainty with single prediction
        
        confidences = [p.get("confidence", 0.5) for p in predictions]
        
        # Calculate variance in predictions
        confidence_variance = stdev(confidences) if len(confidences) > 1 else 0
        
        # Calculate disagreement between predictions
        prediction_types = [p.get("prediction_type", "unknown") for p in predictions]
        type_counts = Counter(prediction_types)
        disagreement = 1 - (max(type_counts.values()) / len(predictions))
        
        # Combine variance and disagreement
        epistemic_uncertainty = (confidence_variance + disagreement) / 2
        
        return min(1.0, epistemic_uncertainty)
    
    def calculate_aleatoric_uncertainty(
        self, 
        data_quality: Dict[str, Any]
    ) -> float:
        """
        Calculate aleatoric uncertainty (data uncertainty)
        
        Args:
            data_quality: Data quality assessment
            
        Returns:
            Aleatoric uncertainty score (0-1)
        """
        uncertainty_score = 0.0
        
        # Data completeness factor
        completeness = data_quality.get("completeness", 0.5)
        uncertainty_score += (1 - completeness) * 0.3
        
        # Data freshness factor
        freshness = data_quality.get("freshness", 0.5)
        uncertainty_score += (1 - freshness) * 0.2
        
        # Data consistency factor
        consistency = data_quality.get("consistency", 0.5)
        uncertainty_score += (1 - consistency) * 0.3
        
        # Data source reliability
        reliability = data_quality.get("source_reliability", 0.5)
        uncertainty_score += (1 - reliability) * 0.2
        
        return min(1.0, uncertainty_score)
    
    def _analyze_confidence_distribution(
        self, 
        steps: List[ReasoningStep]
    ) -> Dict[str, Any]:
        """Analyze confidence distribution across reasoning steps"""
        
        if not steps:
            return {
                "mean_confidence": 0.5,
                "confidence_variance": 0.0,
                "min_confidence": 0.0,
                "max_confidence": 0.0,
                "step_consistency": 0.0
            }
        
        confidences = [step.confidence for step in steps]
        
        mean_conf = mean(confidences)
        variance = stdev(confidences) if len(confidences) > 1 else 0.0
        min_conf = min(confidences)
        max_conf = max(confidences)
        
        # Calculate consistency (low variance = high consistency)
        step_consistency = max(0.0, 1.0 - (variance / max_conf if max_conf > 0 else 1.0))
        
        return {
            "mean_confidence": mean_conf,
            "confidence_variance": variance,
            "min_confidence": min_conf,
            "max_confidence": max_conf,
            "step_consistency": step_consistency
        }
    
    def _identify_uncertainty_sources(
        self, 
        result: ReasoningResult
    ) -> List[Dict[str, Any]]:
        """Identify sources of uncertainty in reasoning"""
        
        sources = []
        
        # Analyze reasoning steps for uncertainty indicators
        for step in result.steps:
            if step.confidence < 0.6:
                sources.append({
                    "source_type": "low_confidence_step",
                    "step_id": step.step_id,
                    "description": step.description,
                    "confidence": step.confidence,
                    "impact": "medium"
                })
            
            if len(step.assumptions) > 2:
                sources.append({
                    "source_type": "multiple_assumptions",
                    "step_id": step.step_id,
                    "assumption_count": len(step.assumptions),
                    "impact": "high"
                })
            
            if not step.evidence:
                sources.append({
                    "source_type": "no_evidence",
                    "step_id": step.step_id,
                    "description": "Step lacks supporting evidence",
                    "impact": "high"
                })
        
        # Analyze causal chains for uncertainty
        for chain in result.causal_chains:
            if chain.confidence < 0.7:
                sources.append({
                    "source_type": "weak_causal_link",
                    "chain_id": chain.chain_id,
                    "confidence": chain.confidence,
                    "impact": "medium"
                })
        
        # Analyze context for data limitations
        context = result.context
        if len(context.historical_events) < 5:
            sources.append({
                "source_type": "limited_historical_data",
                "event_count": len(context.historical_events),
                "impact": "high"
            })
        
        if not context.related_entities:
            sources.append({
                "source_type": "limited_context",
                "description": "Insufficient related entities for comprehensive analysis",
                "impact": "medium"
            })
        
        return sources
    
    def _assess_data_quality(self, result: ReasoningResult) -> Dict[str, Any]:
        """Assess quality of data used in reasoning"""
        
        context = result.context
        
        # Assess completeness
        completeness = self._assess_data_completeness(context)
        
        # Assess freshness
        freshness = self._assess_data_freshness(context)
        
        # Assess consistency
        consistency = self._assess_data_consistency(result)
        
        # Assess source reliability
        reliability = self._assess_source_reliability(context)
        
        overall_quality = (completeness + freshness + consistency + reliability) / 4
        
        return {
            "completeness": completeness,
            "freshness": freshness,
            "consistency": consistency,
            "source_reliability": reliability,
            "overall_quality": overall_quality,
            "quality_level": self._quality_score_to_level(overall_quality)
        }
    
    def _assess_data_completeness(self, context) -> float:
        """Assess completeness of available data"""
        
        completeness_score = 0.0
        
        # Check entity coverage
        if context.tension_id:
            completeness_score += 0.3
        if context.task_ids:
            completeness_score += 0.2
        if context.agent_id:
            completeness_score += 0.1
        if context.project_id:
            completeness_score += 0.1
        
        # Check historical data
        if len(context.historical_events) >= 20:
            completeness_score += 0.2
        elif len(context.historical_events) >= 10:
            completeness_score += 0.15
        elif len(context.historical_events) >= 5:
            completeness_score += 0.1
        
        # Check related entities
        entity_types = len(context.related_entities.keys())
        if entity_types >= 3:
            completeness_score += 0.1
        elif entity_types >= 2:
            completeness_score += 0.05
        
        return min(1.0, completeness_score)
    
    def _assess_data_freshness(self, context) -> float:
        """Assess freshness of available data"""
        
        if not context.historical_events:
            return 0.3  # Default low freshness
        
        from datetime import datetime, timedelta
        
        now = datetime.now()
        recent_threshold = now - timedelta(hours=24)
        
        recent_events = [
            event for event in context.historical_events
            if event.get("timestamp", datetime.min) > recent_threshold
        ]
        
        freshness_ratio = len(recent_events) / len(context.historical_events)
        
        # Scale freshness score
        if freshness_ratio >= 0.5:
            return 1.0
        elif freshness_ratio >= 0.3:
            return 0.8
        elif freshness_ratio >= 0.1:
            return 0.6
        else:
            return 0.4
    
    def _assess_data_consistency(self, result: ReasoningResult) -> float:
        """Assess consistency of reasoning steps and conclusions"""
        
        if not result.steps:
            return 0.5
        
        # Check confidence consistency
        confidences = [step.confidence for step in result.steps]
        confidence_variance = stdev(confidences) if len(confidences) > 1 else 0
        
        consistency_score = max(0.0, 1.0 - (confidence_variance * 2))
        
        # Check for contradictory conclusions
        if result.conclusions:
            # Simple check for contradictory language
            contradiction_indicators = ["however", "but", "contradicts", "inconsistent"]
            contradictions = sum(
                1 for conclusion in result.conclusions
                for indicator in contradiction_indicators
                if indicator in conclusion.lower()
            )
            
            if contradictions > 0:
                consistency_score *= 0.8
        
        return consistency_score
    
    def _assess_source_reliability(self, context) -> float:
        """Assess reliability of data sources"""
        
        # Base reliability score
        reliability = 0.7
        
        # Check for system-generated vs user-generated events
        if context.historical_events:
            system_events = sum(
                1 for event in context.historical_events
                if event.get("data", {}).get("source_type") == "system"
            )
            
            reliability += (system_events / len(context.historical_events)) * 0.2
        
        # Check for verified vs unverified data
        # (This would be enhanced with actual verification metadata)
        
        return min(1.0, reliability)
    
    def _calculate_overall_uncertainty(
        self, 
        confidence_analysis: Dict[str, Any],
        uncertainty_sources: List[Dict[str, Any]], 
        data_quality: Dict[str, Any]
    ) -> float:
        """Calculate overall uncertainty score"""
        
        # Start with confidence-based uncertainty
        mean_confidence = confidence_analysis["mean_confidence"]
        base_uncertainty = 1.0 - mean_confidence
        
        # Add uncertainty from variance in steps
        variance_penalty = confidence_analysis["confidence_variance"] * 0.3
        
        # Add uncertainty from identified sources
        source_penalty = len(uncertainty_sources) * 0.05
        
        # Add uncertainty from data quality issues
        data_quality_penalty = (1.0 - data_quality["overall_quality"]) * 0.2
        
        total_uncertainty = base_uncertainty + variance_penalty + source_penalty + data_quality_penalty
        
        return min(1.0, total_uncertainty)
    
    def _score_to_uncertainty_level(self, score: float) -> UncertaintyLevel:
        """Convert uncertainty score to uncertainty level"""
        
        if score <= 0.1:
            return UncertaintyLevel.CERTAIN
        elif score <= 0.3:
            return UncertaintyLevel.HIGH_CONFIDENCE
        elif score <= 0.5:
            return UncertaintyLevel.MODERATE
        elif score <= 0.7:
            return UncertaintyLevel.LOW_CONFIDENCE
        else:
            return UncertaintyLevel.UNCERTAIN
    
    def _quality_score_to_level(self, score: float) -> str:
        """Convert quality score to quality level"""
        
        if score >= 0.8:
            return "high"
        elif score >= 0.6:
            return "medium"
        else:
            return "low"
    
    def _identify_risk_factors(
        self, 
        result: ReasoningResult, 
        uncertainty_score: float
    ) -> List[Dict[str, Any]]:
        """Identify risk factors based on uncertainty analysis"""
        
        risk_factors = []
        
        if uncertainty_score > 0.7:
            risk_factors.append({
                "risk_type": "high_overall_uncertainty",
                "severity": "high",
                "description": "Overall uncertainty is very high, conclusions may be unreliable",
                "mitigation": "Gather more data or use conservative decision making"
            })
        
        # Check for steps with very low confidence
        low_confidence_steps = [
            step for step in result.steps 
            if step.confidence < 0.4
        ]
        
        if low_confidence_steps:
            risk_factors.append({
                "risk_type": "low_confidence_steps",
                "severity": "medium",
                "description": f"{len(low_confidence_steps)} reasoning steps have very low confidence",
                "affected_steps": [step.step_id for step in low_confidence_steps],
                "mitigation": "Review and strengthen evidence for low-confidence steps"
            })
        
        # Check for weak causal relationships
        weak_causal_chains = [
            chain for chain in result.causal_chains
            if chain.confidence < 0.5
        ]
        
        if weak_causal_chains:
            risk_factors.append({
                "risk_type": "weak_causal_relationships",
                "severity": "medium", 
                "description": f"{len(weak_causal_chains)} causal relationships have low confidence",
                "mitigation": "Validate causal assumptions with additional evidence"
            })
        
        # Check for insufficient evidence
        steps_without_evidence = [
            step for step in result.steps
            if not step.evidence
        ]
        
        if len(steps_without_evidence) > len(result.steps) * 0.3:
            risk_factors.append({
                "risk_type": "insufficient_evidence",
                "severity": "high",
                "description": "Many reasoning steps lack supporting evidence",
                "mitigation": "Collect additional evidence before making decisions"
            })
        
        return risk_factors
    
    def _generate_uncertainty_recommendations(
        self, 
        uncertainty_score: float, 
        uncertainty_sources: List[Dict[str, Any]]
    ) -> List[str]:
        """Generate recommendations for handling uncertainty"""
        
        recommendations = []
        
        if uncertainty_score > 0.6:
            recommendations.append(
                "Consider gathering additional data before making critical decisions"
            )
            recommendations.append(
                "Use conservative estimates and include uncertainty bounds in conclusions"
            )
        
        # Source-specific recommendations
        source_types = [source["source_type"] for source in uncertainty_sources]
        
        if "limited_historical_data" in source_types:
            recommendations.append(
                "Expand the time window for historical analysis to include more events"
            )
        
        if "multiple_assumptions" in source_types:
            recommendations.append(
                "Validate key assumptions with additional evidence or expert consultation"
            )
        
        if "weak_causal_link" in source_types:
            recommendations.append(
                "Strengthen causal analysis with temporal correlation studies"
            )
        
        if "no_evidence" in source_types:
            recommendations.append(
                "Prioritize evidence collection for unsupported reasoning steps"
            )
        
        if uncertainty_score < 0.3:
            recommendations.append(
                "Uncertainty levels are acceptably low for confident decision making"
            )
        
        return recommendations 