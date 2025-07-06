"""
PriorityCalculator - Advanced priority calculation engine

Calculates intelligent priority scores based on:
- Multi-dimensional analysis (impact, urgency, complexity, resources)
- Historical data patterns
- Business context and rules
- Risk factors and dependencies
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import math
from datetime import datetime, timedelta

from .tension_analyzer import TensionAnalysis, ImpactLevel, UrgencyLevel

class PriorityDimension(Enum):
    IMPACT = "impact"
    URGENCY = "urgency"
    COMPLEXITY = "complexity"
    RESOURCE_AVAILABILITY = "resource_availability"
    BUSINESS_VALUE = "business_value"
    RISK_LEVEL = "risk_level"
    STAKEHOLDER_INTEREST = "stakeholder_interest"

@dataclass
class PriorityFactors:
    """Các yếu tố ảnh hưởng đến priority calculation"""
    impact_score: float  # 0.0 - 1.0
    urgency_score: float  # 0.0 - 1.0
    complexity_score: float  # 0.0 - 1.0 (higher = more complex)
    resource_availability_score: float  # 0.0 - 1.0 (higher = more available)
    business_value_score: float  # 0.0 - 1.0
    risk_level_score: float  # 0.0 - 1.0 (higher = more risky)
    stakeholder_interest_score: float  # 0.0 - 1.0
    
    # Contextual factors
    deadline_pressure: float = 0.0  # 0.0 - 1.0
    dependency_factor: float = 0.0  # 0.0 - 1.0 (higher = more dependencies)
    strategic_alignment: float = 0.0  # 0.0 - 1.0

@dataclass
class PriorityCalculationResult:
    """Kết quả tính toán priority"""
    final_score: float  # 0.0 - 100.0
    normalized_priority: int  # 0, 1, 2 (normal, high, critical)
    priority_level: str  # "Low", "Medium", "High", "Critical"
    contributing_factors: Dict[str, float]
    calculation_method: str
    confidence_level: float  # 0.0 - 1.0
    reasoning: str
    recommendations: List[str]

class PriorityCalculator:
    """
    Advanced priority calculation engine for TRM-OS tensions.
    
    Features:
    - Multi-dimensional priority scoring
    - Weighted factor analysis
    - Context-aware calculations
    - Historical pattern learning
    - Business rule integration
    """
    
    def __init__(self):
        self._initialize_weights()
        self._initialize_calculation_methods()
        self._initialize_business_contexts()
    
    def _initialize_weights(self):
        """Initialize default weights for priority dimensions"""
        
        # Default weights (can be customized per organization)
        self.default_weights = {
            PriorityDimension.IMPACT: 0.25,
            PriorityDimension.URGENCY: 0.25,
            PriorityDimension.COMPLEXITY: 0.15,
            PriorityDimension.RESOURCE_AVAILABILITY: 0.10,
            PriorityDimension.BUSINESS_VALUE: 0.15,
            PriorityDimension.RISK_LEVEL: 0.05,
            PriorityDimension.STAKEHOLDER_INTEREST: 0.05
        }
        
        # Context-specific weight adjustments
        self.context_weight_adjustments = {
            "security_incident": {
                PriorityDimension.URGENCY: 0.4,
                PriorityDimension.RISK_LEVEL: 0.2,
                PriorityDimension.IMPACT: 0.3
            },
            "business_critical": {
                PriorityDimension.BUSINESS_VALUE: 0.3,
                PriorityDimension.IMPACT: 0.3,
                PriorityDimension.STAKEHOLDER_INTEREST: 0.2
            },
            "technical_debt": {
                PriorityDimension.COMPLEXITY: 0.3,
                PriorityDimension.RISK_LEVEL: 0.2,
                PriorityDimension.RESOURCE_AVAILABILITY: 0.2
            }
        }
    
    def _initialize_calculation_methods(self):
        """Initialize different calculation methods"""
        
        self.calculation_methods = {
            "weighted_average": self._calculate_weighted_average,
            "eisenhower_matrix": self._calculate_eisenhower_matrix,
            "rice_framework": self._calculate_rice_framework,
            "value_complexity": self._calculate_value_complexity,
            "risk_adjusted": self._calculate_risk_adjusted
        }
    
    def _initialize_business_contexts(self):
        """Initialize business context patterns"""
        
        self.business_contexts = {
            "customer_facing": {
                "impact_multiplier": 1.3,
                "urgency_multiplier": 1.2,
                "stakeholder_multiplier": 1.4
            },
            "internal_operations": {
                "complexity_multiplier": 1.1,
                "resource_multiplier": 1.2,
                "business_value_multiplier": 0.9
            },
            "compliance_related": {
                "risk_multiplier": 1.5,
                "urgency_multiplier": 1.3,
                "impact_multiplier": 1.2
            },
            "innovation_project": {
                "business_value_multiplier": 1.4,
                "complexity_multiplier": 1.2,
                "resource_multiplier": 0.8
            }
        }
    
    def calculate_priority(self, tension_analysis: TensionAnalysis,
                          title: str, description: str,
                          context: Optional[Dict] = None,
                          method: str = "weighted_average") -> PriorityCalculationResult:
        """
        Calculate comprehensive priority score for a tension
        
        Args:
            tension_analysis: Analysis result from TensionAnalyzer
            title: Tension title
            description: Tension description
            context: Additional context information
            method: Calculation method to use
            
        Returns:
            PriorityCalculationResult with detailed scoring
        """
        
        # Extract priority factors from analysis and context
        factors = self._extract_priority_factors(tension_analysis, title, description, context)
        
        # Determine business context
        business_context = self._determine_business_context(tension_analysis, title, description)
        
        # Apply context-specific adjustments
        adjusted_factors = self._apply_context_adjustments(factors, business_context)
        
        # Calculate priority using specified method
        if method in self.calculation_methods:
            calculation_result = self.calculation_methods[method](adjusted_factors, business_context)
        else:
            calculation_result = self._calculate_weighted_average(adjusted_factors, business_context)
        
        # Add metadata
        calculation_result.calculation_method = method
        calculation_result.reasoning = self._generate_priority_reasoning(
            factors, adjusted_factors, business_context, calculation_result
        )
        calculation_result.recommendations = self._generate_recommendations(
            calculation_result, factors, business_context
        )
        
        return calculation_result
    
    def _extract_priority_factors(self, analysis: TensionAnalysis, 
                                title: str, description: str,
                                context: Optional[Dict] = None) -> PriorityFactors:
        """Extract priority factors from tension analysis and context"""
        
        # Convert analysis values to normalized scores (0.0 - 1.0)
        impact_score = analysis.impact_level.value / 4.0
        urgency_score = analysis.urgency_level.value / 4.0
        
        # Estimate complexity based on description length and themes
        complexity_score = self._estimate_complexity(analysis, title, description)
        
        # Estimate resource availability (simplified)
        resource_availability_score = self._estimate_resource_availability(analysis, context)
        
        # Estimate business value based on themes and impact
        business_value_score = self._estimate_business_value(analysis, title, description)
        
        # Convert suggested priority to risk level
        risk_level_score = analysis.suggested_priority / 2.0  # 0-2 -> 0.0-1.0
        
        # Estimate stakeholder interest
        stakeholder_interest_score = self._estimate_stakeholder_interest(analysis, context)
        
        # Extract contextual factors
        deadline_pressure = self._calculate_deadline_pressure(context)
        dependency_factor = self._calculate_dependency_factor(context)
        strategic_alignment = self._calculate_strategic_alignment(analysis, context)
        
        return PriorityFactors(
            impact_score=impact_score,
            urgency_score=urgency_score,
            complexity_score=complexity_score,
            resource_availability_score=resource_availability_score,
            business_value_score=business_value_score,
            risk_level_score=risk_level_score,
            stakeholder_interest_score=stakeholder_interest_score,
            deadline_pressure=deadline_pressure,
            dependency_factor=dependency_factor,
            strategic_alignment=strategic_alignment
        )
    
    def _estimate_complexity(self, analysis: TensionAnalysis, title: str, description: str) -> float:
        """Estimate complexity score based on various factors"""
        complexity_indicators = 0
        
        # Text length indicates complexity
        text_length = len(title) + len(description)
        if text_length > 500:
            complexity_indicators += 0.3
        elif text_length > 200:
            complexity_indicators += 0.2
        else:
            complexity_indicators += 0.1
        
        # Multiple themes indicate complexity
        theme_count = len(analysis.key_themes)
        complexity_indicators += min(theme_count * 0.15, 0.4)
        
        # Certain themes are inherently complex
        complex_themes = ["Technology", "Security", "Business"]
        for theme in analysis.key_themes:
            if theme in complex_themes:
                complexity_indicators += 0.1
        
        # Extracted entities indicate complexity
        entity_count = len(analysis.extracted_entities)
        complexity_indicators += min(entity_count * 0.05, 0.2)
        
        return min(complexity_indicators, 1.0)
    
    def _estimate_resource_availability(self, analysis: TensionAnalysis, 
                                      context: Optional[Dict] = None) -> float:
        """Estimate resource availability score"""
        # Default to medium availability
        base_score = 0.6
        
        # Adjust based on themes (some require specialized resources)
        specialized_themes = ["Security", "Technology"]
        for theme in analysis.key_themes:
            if theme in specialized_themes:
                base_score -= 0.15
        
        # Adjust based on context
        if context:
            if context.get("team_capacity", "medium") == "high":
                base_score += 0.2
            elif context.get("team_capacity", "medium") == "low":
                base_score -= 0.2
            
            if context.get("budget_available", True):
                base_score += 0.1
            else:
                base_score -= 0.2
        
        return max(0.0, min(1.0, base_score))
    
    def _estimate_business_value(self, analysis: TensionAnalysis, title: str, description: str) -> float:
        """Estimate business value score"""
        value_score = 0.0
        
        # Base value from impact
        value_score += analysis.impact_level.value / 4.0 * 0.4
        
        # Value keywords
        value_keywords = [
            "revenue", "customer", "efficiency", "cost", "profit", "market",
            "competitive", "strategic", "growth", "innovation"
        ]
        text = f"{title} {description}".lower()
        keyword_matches = sum(1 for keyword in value_keywords if keyword in text)
        value_score += min(keyword_matches * 0.1, 0.4)
        
        # Business theme adds value
        if "Business" in analysis.key_themes:
            value_score += 0.2
        
        return min(value_score, 1.0)
    
    def _estimate_stakeholder_interest(self, analysis: TensionAnalysis, 
                                     context: Optional[Dict] = None) -> float:
        """Estimate stakeholder interest level"""
        interest_score = 0.5  # Default medium interest
        
        # High impact tensions get more stakeholder attention
        interest_score += analysis.impact_level.value / 4.0 * 0.3
        
        # Customer-facing themes increase stakeholder interest
        customer_themes = ["Business", "Security"]
        for theme in analysis.key_themes:
            if theme in customer_themes:
                interest_score += 0.15
        
        # Context adjustments
        if context:
            stakeholder_count = context.get("stakeholder_count", 1)
            interest_score += min(stakeholder_count * 0.05, 0.2)
            
            if context.get("executive_visibility", False):
                interest_score += 0.3
        
        return min(interest_score, 1.0)
    
    def _calculate_deadline_pressure(self, context: Optional[Dict] = None) -> float:
        """Calculate deadline pressure factor"""
        if not context or "deadline" not in context:
            return 0.0
        
        deadline = context.get("deadline")
        if isinstance(deadline, str):
            # Simple parsing for demo
            if "urgent" in deadline.lower():
                return 0.8
            elif "asap" in deadline.lower():
                return 1.0
            else:
                return 0.3
        
        return 0.0
    
    def _calculate_dependency_factor(self, context: Optional[Dict] = None) -> float:
        """Calculate dependency factor"""
        if not context:
            return 0.0
        
        dependencies = context.get("dependencies", [])
        if isinstance(dependencies, list):
            return min(len(dependencies) * 0.2, 1.0)
        
        return 0.0
    
    def _calculate_strategic_alignment(self, analysis: TensionAnalysis, 
                                     context: Optional[Dict] = None) -> float:
        """Calculate strategic alignment score"""
        alignment_score = 0.5  # Default medium alignment
        
        # Business and opportunity tensions often align with strategy
        if analysis.tension_type.value in ["Opportunity", "Business"]:
            alignment_score += 0.2
        
        # Context adjustments
        if context:
            if context.get("strategic_initiative", False):
                alignment_score += 0.3
            
            if context.get("okr_related", False):
                alignment_score += 0.2
        
        return min(alignment_score, 1.0)
    
    def _determine_business_context(self, analysis: TensionAnalysis, 
                                  title: str, description: str) -> str:
        """Determine business context for weight adjustments"""
        text = f"{title} {description}".lower()
        
        # Security context
        if "Security" in analysis.key_themes or any(keyword in text for keyword in ["security", "breach", "hack"]):
            return "security_incident"
        
        # Customer-facing context
        if any(keyword in text for keyword in ["customer", "user", "client", "public"]):
            return "customer_facing"
        
        # Compliance context
        if any(keyword in text for keyword in ["compliance", "regulation", "audit", "legal"]):
            return "compliance_related"
        
        # Innovation context
        if analysis.tension_type.value == "Opportunity" or any(keyword in text for keyword in ["innovation", "new", "experiment"]):
            return "innovation_project"
        
        # Default to internal operations
        return "internal_operations"
    
    def _apply_context_adjustments(self, factors: PriorityFactors, 
                                 business_context: str) -> PriorityFactors:
        """Apply business context adjustments to factors"""
        if business_context not in self.business_contexts:
            return factors
        
        adjustments = self.business_contexts[business_context]
        
        # Apply multipliers
        adjusted_factors = PriorityFactors(
            impact_score=min(1.0, factors.impact_score * adjustments.get("impact_multiplier", 1.0)),
            urgency_score=min(1.0, factors.urgency_score * adjustments.get("urgency_multiplier", 1.0)),
            complexity_score=min(1.0, factors.complexity_score * adjustments.get("complexity_multiplier", 1.0)),
            resource_availability_score=min(1.0, factors.resource_availability_score * adjustments.get("resource_multiplier", 1.0)),
            business_value_score=min(1.0, factors.business_value_score * adjustments.get("business_value_multiplier", 1.0)),
            risk_level_score=min(1.0, factors.risk_level_score * adjustments.get("risk_multiplier", 1.0)),
            stakeholder_interest_score=min(1.0, factors.stakeholder_interest_score * adjustments.get("stakeholder_multiplier", 1.0)),
            deadline_pressure=factors.deadline_pressure,
            dependency_factor=factors.dependency_factor,
            strategic_alignment=factors.strategic_alignment
        )
        
        return adjusted_factors
    
    def _calculate_weighted_average(self, factors: PriorityFactors, 
                                  business_context: str) -> PriorityCalculationResult:
        """Calculate priority using weighted average method"""
        
        # Get weights (with context adjustments if applicable)
        weights = self.default_weights.copy()
        if business_context in self.context_weight_adjustments:
            context_weights = self.context_weight_adjustments[business_context]
            # Normalize context weights
            total_context_weight = sum(context_weights.values())
            for dimension, weight in context_weights.items():
                weights[dimension] = weight / total_context_weight
        
        # Calculate weighted score
        weighted_score = (
            factors.impact_score * weights[PriorityDimension.IMPACT] +
            factors.urgency_score * weights[PriorityDimension.URGENCY] +
            (1 - factors.complexity_score) * weights[PriorityDimension.COMPLEXITY] +  # Invert complexity
            factors.resource_availability_score * weights[PriorityDimension.RESOURCE_AVAILABILITY] +
            factors.business_value_score * weights[PriorityDimension.BUSINESS_VALUE] +
            factors.risk_level_score * weights[PriorityDimension.RISK_LEVEL] +
            factors.stakeholder_interest_score * weights[PriorityDimension.STAKEHOLDER_INTEREST]
        )
        
        # Apply contextual adjustments
        contextual_boost = (
            factors.deadline_pressure * 0.1 +
            factors.dependency_factor * 0.05 +
            factors.strategic_alignment * 0.05
        )
        
        final_score = min(1.0, weighted_score + contextual_boost) * 100
        
        # Determine priority level
        normalized_priority, priority_level = self._normalize_priority(final_score)
        
        # Calculate confidence
        confidence = self._calculate_confidence(factors, weights)
        
        return PriorityCalculationResult(
            final_score=final_score,
            normalized_priority=normalized_priority,
            priority_level=priority_level,
            contributing_factors={
                "impact": factors.impact_score * weights[PriorityDimension.IMPACT],
                "urgency": factors.urgency_score * weights[PriorityDimension.URGENCY],
                "complexity": (1 - factors.complexity_score) * weights[PriorityDimension.COMPLEXITY],
                "resources": factors.resource_availability_score * weights[PriorityDimension.RESOURCE_AVAILABILITY],
                "business_value": factors.business_value_score * weights[PriorityDimension.BUSINESS_VALUE],
                "risk": factors.risk_level_score * weights[PriorityDimension.RISK_LEVEL],
                "stakeholder": factors.stakeholder_interest_score * weights[PriorityDimension.STAKEHOLDER_INTEREST],
                "contextual_boost": contextual_boost
            },
            calculation_method="weighted_average",
            confidence_level=confidence,
            reasoning="",  # Will be filled later
            recommendations=[]  # Will be filled later
        )
    
    def _calculate_eisenhower_matrix(self, factors: PriorityFactors, 
                                   business_context: str) -> PriorityCalculationResult:
        """Calculate priority using Eisenhower Matrix (Important vs Urgent)"""
        
        importance = (factors.impact_score + factors.business_value_score + factors.strategic_alignment) / 3
        urgency = (factors.urgency_score + factors.deadline_pressure + factors.risk_level_score) / 3
        
        # Eisenhower quadrants
        if urgency >= 0.7 and importance >= 0.7:
            # Quadrant 1: Do First (Critical)
            final_score = 90 + (urgency + importance) * 5
            normalized_priority = 2
            priority_level = "Critical"
        elif urgency < 0.7 and importance >= 0.7:
            # Quadrant 2: Schedule (High)
            final_score = 70 + importance * 15
            normalized_priority = 1
            priority_level = "High"
        elif urgency >= 0.7 and importance < 0.7:
            # Quadrant 3: Delegate (Medium)
            final_score = 50 + urgency * 15
            normalized_priority = 1
            priority_level = "Medium"
        else:
            # Quadrant 4: Eliminate (Low)
            final_score = 30 + (urgency + importance) * 10
            normalized_priority = 0
            priority_level = "Low"
        
        confidence = min(abs(urgency - 0.5) + abs(importance - 0.5), 1.0)
        
        return PriorityCalculationResult(
            final_score=min(final_score, 100),
            normalized_priority=normalized_priority,
            priority_level=priority_level,
            contributing_factors={
                "importance": importance,
                "urgency": urgency,
                "quadrant": f"Q{1 if urgency >= 0.7 and importance >= 0.7 else 2 if importance >= 0.7 else 3 if urgency >= 0.7 else 4}"
            },
            calculation_method="eisenhower_matrix",
            confidence_level=confidence,
            reasoning="",
            recommendations=[]
        )
    
    def _calculate_rice_framework(self, factors: PriorityFactors, 
                                business_context: str) -> PriorityCalculationResult:
        """Calculate priority using RICE framework (Reach, Impact, Confidence, Effort)"""
        
        reach = factors.stakeholder_interest_score
        impact = factors.impact_score
        confidence = (factors.impact_score + factors.urgency_score + factors.business_value_score) / 3
        effort = factors.complexity_score  # Higher complexity = more effort
        
        # RICE Score = (Reach × Impact × Confidence) / Effort
        # Avoid division by zero
        effort_adjusted = max(effort, 0.1)
        rice_score = (reach * impact * confidence) / effort_adjusted
        
        # Normalize to 0-100 scale
        final_score = min(rice_score * 100, 100)
        
        normalized_priority, priority_level = self._normalize_priority(final_score)
        
        return PriorityCalculationResult(
            final_score=final_score,
            normalized_priority=normalized_priority,
            priority_level=priority_level,
            contributing_factors={
                "reach": reach,
                "impact": impact,
                "confidence": confidence,
                "effort": effort,
                "rice_score": rice_score
            },
            calculation_method="rice_framework",
            confidence_level=confidence,
            reasoning="",
            recommendations=[]
        )
    
    def _calculate_value_complexity(self, factors: PriorityFactors, 
                                  business_context: str) -> PriorityCalculationResult:
        """Calculate priority using Value vs Complexity matrix"""
        
        value = (factors.business_value_score + factors.impact_score + factors.strategic_alignment) / 3
        complexity = factors.complexity_score
        
        # Value/Complexity quadrants
        if value >= 0.7 and complexity <= 0.3:
            # High Value, Low Complexity - Quick Wins
            final_score = 85 + value * 10
            normalized_priority = 2
            priority_level = "Critical"
        elif value >= 0.7 and complexity > 0.3:
            # High Value, High Complexity - Major Projects
            final_score = 75 + (value - complexity) * 10
            normalized_priority = 1
            priority_level = "High"
        elif value < 0.7 and complexity <= 0.3:
            # Low Value, Low Complexity - Fill-ins
            final_score = 45 + value * 15
            normalized_priority = 0
            priority_level = "Medium"
        else:
            # Low Value, High Complexity - Questionable
            final_score = 25 + (value - complexity) * 20
            normalized_priority = 0
            priority_level = "Low"
        
        confidence = min(abs(value - 0.5) + abs(complexity - 0.5), 1.0)
        
        return PriorityCalculationResult(
            final_score=max(0, min(final_score, 100)),
            normalized_priority=normalized_priority,
            priority_level=priority_level,
            contributing_factors={
                "value": value,
                "complexity": complexity,
                "value_complexity_ratio": value / max(complexity, 0.1)
            },
            calculation_method="value_complexity",
            confidence_level=confidence,
            reasoning="",
            recommendations=[]
        )
    
    def _calculate_risk_adjusted(self, factors: PriorityFactors, 
                               business_context: str) -> PriorityCalculationResult:
        """Calculate priority with risk adjustment"""
        
        base_priority = (factors.impact_score + factors.urgency_score + factors.business_value_score) / 3
        risk_adjustment = factors.risk_level_score * 0.3
        resource_adjustment = (1 - factors.resource_availability_score) * 0.2
        
        final_score = (base_priority + risk_adjustment - resource_adjustment) * 100
        final_score = max(0, min(final_score, 100))
        
        normalized_priority, priority_level = self._normalize_priority(final_score)
        
        confidence = (base_priority + factors.risk_level_score + factors.resource_availability_score) / 3
        
        return PriorityCalculationResult(
            final_score=final_score,
            normalized_priority=normalized_priority,
            priority_level=priority_level,
            contributing_factors={
                "base_priority": base_priority,
                "risk_adjustment": risk_adjustment,
                "resource_adjustment": resource_adjustment
            },
            calculation_method="risk_adjusted",
            confidence_level=confidence,
            reasoning="",
            recommendations=[]
        )
    
    def _normalize_priority(self, score: float) -> Tuple[int, str]:
        """Normalize score to priority level"""
        if score >= 80:
            return 2, "Critical"
        elif score >= 60:
            return 1, "High"
        elif score >= 40:
            return 0, "Medium"
        else:
            return 0, "Low"
    
    def _calculate_confidence(self, factors: PriorityFactors, weights: Dict) -> float:
        """Calculate confidence in priority calculation"""
        # Higher confidence when factors are more extreme (closer to 0 or 1)
        factor_values = [
            factors.impact_score, factors.urgency_score, factors.business_value_score,
            factors.complexity_score, factors.resource_availability_score,
            factors.risk_level_score, factors.stakeholder_interest_score
        ]
        
        extremeness = sum(abs(value - 0.5) * 2 for value in factor_values) / len(factor_values)
        return min(extremeness + 0.3, 1.0)  # Base confidence of 0.3
    
    def _generate_priority_reasoning(self, original_factors: PriorityFactors,
                                   adjusted_factors: PriorityFactors,
                                   business_context: str,
                                   result: PriorityCalculationResult) -> str:
        """Generate human-readable reasoning for priority calculation"""
        reasoning_parts = []
        
        reasoning_parts.append(
            f"Priority calculated using {result.calculation_method} method with {result.confidence_level:.1%} confidence"
        )
        
        reasoning_parts.append(
            f"Business context identified as '{business_context}' affecting weight distribution"
        )
        
        # Identify top contributing factors (only numeric values)
        numeric_factors = {k: v for k, v in result.contributing_factors.items() if isinstance(v, (int, float))}
        string_factors = {k: v for k, v in result.contributing_factors.items() if isinstance(v, str)}
        
        top_factors = sorted(numeric_factors.items(), key=lambda x: x[1], reverse=True)[:3]
        factor_names = [f"{name} ({value:.2f})" for name, value in top_factors]
        
        # Add string factors if any
        if string_factors:
            string_factor_names = [f"{name} ({value})" for name, value in string_factors.items()]
            factor_names.extend(string_factor_names)
        
        reasoning_parts.append(
            f"Primary contributing factors: {', '.join(factor_names)}"
        )
        
        reasoning_parts.append(
            f"Final score: {result.final_score:.1f}/100 → {result.priority_level} priority"
        )
        
        return ". ".join(reasoning_parts) + "."
    
    def _generate_recommendations(self, result: PriorityCalculationResult,
                                factors: PriorityFactors,
                                business_context: str) -> List[str]:
        """Generate actionable recommendations based on priority calculation"""
        recommendations = []
        
        # Priority-based recommendations
        if result.normalized_priority == 2:
            recommendations.append("Immediate attention required - allocate dedicated resources")
            recommendations.append("Consider escalating to stakeholders")
        elif result.normalized_priority == 1:
            recommendations.append("Schedule for next sprint/iteration")
            recommendations.append("Ensure adequate resource allocation")
        else:
            recommendations.append("Add to backlog for future consideration")
            recommendations.append("Monitor for changes in priority factors")
        
        # Factor-specific recommendations
        if factors.complexity_score > 0.7:
            recommendations.append("Break down into smaller, manageable tasks")
            recommendations.append("Consider proof-of-concept or pilot approach")
        
        if factors.resource_availability_score < 0.3:
            recommendations.append("Secure additional resources before starting")
            recommendations.append("Consider external expertise or consulting")
        
        if factors.risk_level_score > 0.7:
            recommendations.append("Develop comprehensive risk mitigation plan")
            recommendations.append("Implement monitoring and early warning systems")
        
        # Context-specific recommendations
        if business_context == "security_incident":
            recommendations.append("Follow security incident response procedures")
            recommendations.append("Communicate with security team immediately")
        elif business_context == "customer_facing":
            recommendations.append("Prioritize customer communication and updates")
            recommendations.append("Monitor customer impact metrics closely")
        
        return list(set(recommendations))  # Remove duplicates 