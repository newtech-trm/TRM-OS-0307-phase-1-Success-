"""
TRM-OS: Strategy Optimizer
Tối ưu hóa decision-making process và strategic approaches
"""

import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
import logging
from enum import Enum
import numpy as np

logger = logging.getLogger(__name__)

class OptimizationStrategy(Enum):
    """Các strategy optimization có thể áp dụng"""
    ROI_MAXIMIZATION = "roi_maximization"
    RISK_MINIMIZATION = "risk_minimization"
    SPEED_OPTIMIZATION = "speed_optimization"
    QUALITY_OPTIMIZATION = "quality_optimization"
    RESOURCE_EFFICIENCY = "resource_efficiency"
    LEARNING_MAXIMIZATION = "learning_maximization"

class DecisionContext(Enum):
    """Context của decision-making"""
    STRATEGIC = "strategic"
    TACTICAL = "tactical"
    OPERATIONAL = "operational"
    EMERGENCY = "emergency"
    EXPERIMENTAL = "experimental"

@dataclass
class StrategyOption:
    """Một option strategy có thể chọn"""
    option_id: str
    name: str
    description: str
    expected_roi: float
    risk_score: float
    resource_requirements: Dict[str, float]
    implementation_time: float  # days
    success_probability: float
    learning_potential: float
    dependencies: List[str]
    confidence_score: float
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class OptimizationResult:
    """Kết quả optimization"""
    recommendation_id: str
    selected_option: StrategyOption
    reasoning: str
    confidence_score: float
    expected_outcomes: Dict[str, float]
    risk_assessment: Dict[str, Any]
    implementation_plan: List[str]
    monitoring_metrics: List[str]
    fallback_options: List[StrategyOption]
    created_at: datetime

class StrategyOptimizer:
    """
    Hệ thống tối ưu hóa strategic decision-making
    Tuân thủ AGE v2.0 philosophy: Intelligent strategy selection và optimization
    """
    
    def __init__(self):
        self.decision_history: List[Dict[str, Any]] = []
        self.optimization_models: Dict[str, Any] = {}
        self.performance_metrics: Dict[str, float] = {}
        
        # Optimization parameters
        self.roi_weight = 0.3
        self.risk_weight = 0.2
        self.speed_weight = 0.15
        self.quality_weight = 0.15
        self.resource_weight = 0.1
        self.learning_weight = 0.1
        
        # Thresholds
        self.min_confidence_threshold = 0.7
        self.max_risk_tolerance = 0.6
        self.min_roi_threshold = 0.15
        
        logger.info("StrategyOptimizer initialized với intelligent decision-making capabilities")

    async def optimize_strategy_selection(self,
                                        options: List[StrategyOption],
                                        context: DecisionContext,
                                        optimization_strategy: OptimizationStrategy,
                                        constraints: Optional[Dict[str, Any]] = None) -> OptimizationResult:
        """
        Tối ưu hóa việc lựa chọn strategy từ multiple options
        
        Args:
            options: List các strategy options
            context: Decision context
            optimization_strategy: Strategy optimization approach
            constraints: Additional constraints
            
        Returns:
            OptimizationResult với recommendation
        """
        try:
            # 1. Filter options based on constraints
            viable_options = await self._filter_viable_options(options, constraints)
            
            if not viable_options:
                raise ValueError("No viable options found after applying constraints")
            
            # 2. Score options based on optimization strategy
            scored_options = await self._score_options(
                viable_options, context, optimization_strategy
            )
            
            # 3. Select best option
            best_option = await self._select_best_option(scored_options, optimization_strategy)
            
            # 4. Generate reasoning
            reasoning = await self._generate_selection_reasoning(
                best_option, scored_options, optimization_strategy
            )
            
            # 5. Assess risks
            risk_assessment = await self._assess_selection_risks(best_option, context)
            
            # 6. Create implementation plan
            implementation_plan = await self._create_implementation_plan(best_option, context)
            
            # 7. Define monitoring metrics
            monitoring_metrics = await self._define_monitoring_metrics(best_option, optimization_strategy)
            
            # 8. Identify fallback options
            fallback_options = await self._identify_fallback_options(scored_options, best_option)
            
            # 9. Calculate expected outcomes
            expected_outcomes = await self._calculate_expected_outcomes(best_option)
            
            # 10. Calculate overall confidence
            confidence_score = await self._calculate_optimization_confidence(
                best_option, scored_options, context
            )
            
            result = OptimizationResult(
                recommendation_id=f"opt_{datetime.now().timestamp()}",
                selected_option=best_option,
                reasoning=reasoning,
                confidence_score=confidence_score,
                expected_outcomes=expected_outcomes,
                risk_assessment=risk_assessment,
                implementation_plan=implementation_plan,
                monitoring_metrics=monitoring_metrics,
                fallback_options=fallback_options,
                created_at=datetime.now()
            )
            
            # Store decision
            await self._store_decision(result, options, context, optimization_strategy)
            
            logger.info(f"Strategy optimization completed với confidence {confidence_score:.2f}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error optimizing strategy selection: {e}")
            raise

    async def _filter_viable_options(self,
                                    options: List[StrategyOption],
                                    constraints: Optional[Dict[str, Any]] = None) -> List[StrategyOption]:
        """Filter options based on constraints"""
        try:
            if not constraints:
                return options
            
            viable_options = []
            
            for option in options:
                # Check basic viability criteria
                if option.confidence_score < self.min_confidence_threshold:
                    continue
                
                if option.risk_score > self.max_risk_tolerance:
                    continue
                
                if option.expected_roi < self.min_roi_threshold:
                    continue
                
                # Check custom constraints
                viable = True
                for constraint_key, constraint_value in constraints.items():
                    if constraint_key == 'max_implementation_time':
                        if option.implementation_time > constraint_value:
                            viable = False
                            break
                    elif constraint_key == 'required_resources':
                        for resource, max_amount in constraint_value.items():
                            if resource in option.resource_requirements:
                                if option.resource_requirements[resource] > max_amount:
                                    viable = False
                                    break
                    elif constraint_key == 'min_success_probability':
                        if option.success_probability < constraint_value:
                            viable = False
                            break
                
                if viable:
                    viable_options.append(option)
            
            return viable_options
            
        except Exception as e:
            logger.warning(f"Error filtering viable options: {e}")
            return options

    async def _score_options(self,
                           options: List[StrategyOption],
                           context: DecisionContext,
                           optimization_strategy: OptimizationStrategy) -> List[Tuple[StrategyOption, float]]:
        """Score options based on optimization strategy"""
        try:
            scored_options = []
            
            for option in options:
                score = 0.0
                
                # Base scoring components
                roi_score = min(option.expected_roi * 2, 1.0)  # Normalize to 0-1
                risk_score = 1.0 - option.risk_score  # Invert risk (lower risk = higher score)
                speed_score = 1.0 / (1.0 + option.implementation_time / 30)  # Faster = better
                quality_score = option.success_probability
                learning_score = option.learning_potential
                
                # Resource efficiency score
                total_resources = sum(option.resource_requirements.values())
                resource_score = 1.0 / (1.0 + total_resources / 100)  # Lower resource = better
                
                # Apply optimization strategy weights
                if optimization_strategy == OptimizationStrategy.ROI_MAXIMIZATION:
                    score = (roi_score * 0.5 + quality_score * 0.2 + 
                            risk_score * 0.15 + speed_score * 0.1 + learning_score * 0.05)
                
                elif optimization_strategy == OptimizationStrategy.RISK_MINIMIZATION:
                    score = (risk_score * 0.4 + quality_score * 0.25 + 
                            roi_score * 0.2 + resource_score * 0.1 + learning_score * 0.05)
                
                elif optimization_strategy == OptimizationStrategy.SPEED_OPTIMIZATION:
                    score = (speed_score * 0.4 + quality_score * 0.25 + 
                            roi_score * 0.2 + risk_score * 0.1 + learning_score * 0.05)
                
                elif optimization_strategy == OptimizationStrategy.QUALITY_OPTIMIZATION:
                    score = (quality_score * 0.4 + learning_score * 0.25 + 
                            roi_score * 0.2 + risk_score * 0.1 + speed_score * 0.05)
                
                elif optimization_strategy == OptimizationStrategy.RESOURCE_EFFICIENCY:
                    score = (resource_score * 0.35 + roi_score * 0.25 + 
                            quality_score * 0.2 + risk_score * 0.15 + speed_score * 0.05)
                
                elif optimization_strategy == OptimizationStrategy.LEARNING_MAXIMIZATION:
                    score = (learning_score * 0.4 + quality_score * 0.25 + 
                            roi_score * 0.2 + risk_score * 0.1 + speed_score * 0.05)
                
                # Context adjustments
                if context == DecisionContext.EMERGENCY:
                    score = score * 0.7 + speed_score * 0.3  # Prioritize speed
                elif context == DecisionContext.EXPERIMENTAL:
                    score = score * 0.8 + learning_score * 0.2  # Prioritize learning
                elif context == DecisionContext.STRATEGIC:
                    score = score * 0.8 + roi_score * 0.2  # Prioritize ROI
                
                # Apply confidence weighting
                final_score = score * option.confidence_score
                
                scored_options.append((option, final_score))
            
            # Sort by score descending
            scored_options.sort(key=lambda x: x[1], reverse=True)
            
            return scored_options
            
        except Exception as e:
            logger.warning(f"Error scoring options: {e}")
            return [(option, 0.5) for option in options]

    async def _select_best_option(self,
                                scored_options: List[Tuple[StrategyOption, float]],
                                optimization_strategy: OptimizationStrategy) -> StrategyOption:
        """Select best option từ scored options"""
        try:
            if not scored_options:
                raise ValueError("No scored options available")
            
            # Simple selection: highest score
            best_option = scored_options[0][0]
            
            # Additional validation
            if scored_options[0][1] < 0.5:  # Low score threshold
                logger.warning(f"Best option has low score: {scored_options[0][1]:.2f}")
            
            return best_option
            
        except Exception as e:
            logger.error(f"Error selecting best option: {e}")
            return scored_options[0][0] if scored_options else None

    async def _generate_selection_reasoning(self,
                                          selected_option: StrategyOption,
                                          scored_options: List[Tuple[StrategyOption, float]],
                                          optimization_strategy: OptimizationStrategy) -> str:
        """Generate reasoning cho selection"""
        try:
            reasoning_parts = []
            
            # Selection rationale
            reasoning_parts.append(f"Selected '{selected_option.name}' based on {optimization_strategy.value} strategy")
            
            # Key strengths
            strengths = []
            if selected_option.expected_roi > 0.2:
                strengths.append(f"high ROI potential ({selected_option.expected_roi:.1%})")
            if selected_option.risk_score < 0.3:
                strengths.append(f"low risk profile ({selected_option.risk_score:.1%})")
            if selected_option.success_probability > 0.8:
                strengths.append(f"high success probability ({selected_option.success_probability:.1%})")
            if selected_option.implementation_time < 14:
                strengths.append(f"quick implementation ({selected_option.implementation_time:.0f} days)")
            
            if strengths:
                reasoning_parts.append(f"Key strengths: {', '.join(strengths)}")
            
            # Comparison với alternatives
            if len(scored_options) > 1:
                second_best_score = scored_options[1][1]
                selected_score = scored_options[0][1]
                advantage = ((selected_score - second_best_score) / second_best_score) * 100
                reasoning_parts.append(f"Outperformed next best option by {advantage:.1f}%")
            
            # Risk considerations
            if selected_option.risk_score > 0.4:
                reasoning_parts.append(f"Notable risk factors require monitoring and mitigation")
            
            return ". ".join(reasoning_parts) + "."
            
        except Exception as e:
            logger.warning(f"Error generating selection reasoning: {e}")
            return f"Selected {selected_option.name} based on optimization analysis"

    async def _assess_selection_risks(self,
                                    option: StrategyOption,
                                    context: DecisionContext) -> Dict[str, Any]:
        """Assess risks của selected option"""
        try:
            risk_assessment = {
                'overall_risk_score': option.risk_score,
                'risk_categories': {},
                'mitigation_strategies': [],
                'monitoring_requirements': []
            }
            
            # Risk categories
            if option.risk_score > 0.6:
                risk_assessment['risk_categories']['execution'] = 'high'
                risk_assessment['mitigation_strategies'].append("Implement phased rollout approach")
                risk_assessment['monitoring_requirements'].append("Daily progress monitoring required")
            elif option.risk_score > 0.3:
                risk_assessment['risk_categories']['execution'] = 'medium'
                risk_assessment['mitigation_strategies'].append("Weekly checkpoint reviews")
                risk_assessment['monitoring_requirements'].append("Weekly progress monitoring")
            else:
                risk_assessment['risk_categories']['execution'] = 'low'
                risk_assessment['monitoring_requirements'].append("Standard monitoring sufficient")
            
            # Resource risk
            total_resources = sum(option.resource_requirements.values())
            if total_resources > 80:
                risk_assessment['risk_categories']['resource'] = 'high'
                risk_assessment['mitigation_strategies'].append("Secure resource commitments upfront")
            elif total_resources > 50:
                risk_assessment['risk_categories']['resource'] = 'medium'
                risk_assessment['mitigation_strategies'].append("Monitor resource allocation weekly")
            else:
                risk_assessment['risk_categories']['resource'] = 'low'
            
            # Timeline risk
            if option.implementation_time > 30:
                risk_assessment['risk_categories']['timeline'] = 'high'
                risk_assessment['mitigation_strategies'].append("Break into smaller milestones")
            elif option.implementation_time > 14:
                risk_assessment['risk_categories']['timeline'] = 'medium'
                risk_assessment['mitigation_strategies'].append("Bi-weekly milestone tracking")
            else:
                risk_assessment['risk_categories']['timeline'] = 'low'
            
            # Context-specific risks
            if context == DecisionContext.EMERGENCY:
                risk_assessment['risk_categories']['urgency'] = 'high'
                risk_assessment['mitigation_strategies'].append("Continuous monitoring during implementation")
            
            return risk_assessment
            
        except Exception as e:
            logger.warning(f"Error assessing selection risks: {e}")
            return {'overall_risk_score': option.risk_score, 'error': str(e)}

    async def _create_implementation_plan(self,
                                        option: StrategyOption,
                                        context: DecisionContext) -> List[str]:
        """Create implementation plan cho selected option"""
        try:
            plan_steps = []
            
            # Phase 1: Preparation
            plan_steps.append("1. PREPARATION PHASE")
            plan_steps.append("   - Secure necessary resources and approvals")
            plan_steps.append("   - Assemble implementation team")
            plan_steps.append("   - Finalize implementation timeline")
            
            # Phase 2: Initiation
            plan_steps.append("2. INITIATION PHASE")
            plan_steps.append("   - Kick-off implementation activities")
            plan_steps.append("   - Establish monitoring and communication protocols")
            plan_steps.append("   - Begin initial implementation tasks")
            
            # Phase 3: Execution
            plan_steps.append("3. EXECUTION PHASE")
            if option.implementation_time <= 7:
                plan_steps.append("   - Execute all tasks within 1 week timeline")
                plan_steps.append("   - Daily progress reviews")
            elif option.implementation_time <= 30:
                plan_steps.append("   - Execute tasks in 2-week sprints")
                plan_steps.append("   - Weekly progress reviews")
            else:
                plan_steps.append("   - Execute tasks in monthly phases")
                plan_steps.append("   - Bi-weekly progress reviews")
            
            # Phase 4: Validation
            plan_steps.append("4. VALIDATION PHASE")
            plan_steps.append("   - Test and validate implementation results")
            plan_steps.append("   - Measure against success criteria")
            plan_steps.append("   - Document lessons learned")
            
            # Phase 5: Optimization
            plan_steps.append("5. OPTIMIZATION PHASE")
            plan_steps.append("   - Analyze performance data")
            plan_steps.append("   - Implement improvements based on results")
            plan_steps.append("   - Update strategy for future implementations")
            
            return plan_steps
            
        except Exception as e:
            logger.warning(f"Error creating implementation plan: {e}")
            return ["1. Execute selected strategy", "2. Monitor progress", "3. Adjust as needed"]

    async def _define_monitoring_metrics(self,
                                       option: StrategyOption,
                                       optimization_strategy: OptimizationStrategy) -> List[str]:
        """Define monitoring metrics cho implementation"""
        try:
            metrics = []
            
            # Standard metrics
            metrics.append("Implementation progress (% complete)")
            metrics.append("Resource utilization vs. budget")
            metrics.append("Timeline adherence")
            metrics.append("Quality indicators")
            
            # Strategy-specific metrics
            if optimization_strategy == OptimizationStrategy.ROI_MAXIMIZATION:
                metrics.extend([
                    "ROI tracking vs. projections",
                    "Revenue/cost impact measurement",
                    "Financial efficiency indicators"
                ])
            
            elif optimization_strategy == OptimizationStrategy.RISK_MINIMIZATION:
                metrics.extend([
                    "Risk incident tracking",
                    "Risk mitigation effectiveness",
                    "Contingency plan activation rate"
                ])
            
            elif optimization_strategy == OptimizationStrategy.SPEED_OPTIMIZATION:
                metrics.extend([
                    "Milestone completion times",
                    "Process cycle times",
                    "Bottleneck identification"
                ])
            
            elif optimization_strategy == OptimizationStrategy.QUALITY_OPTIMIZATION:
                metrics.extend([
                    "Quality score measurements",
                    "Defect/error rates",
                    "Stakeholder satisfaction"
                ])
            
            elif optimization_strategy == OptimizationStrategy.LEARNING_MAXIMIZATION:
                metrics.extend([
                    "Learning objective achievement",
                    "Knowledge capture and transfer",
                    "Capability development tracking"
                ])
            
            # Option-specific metrics
            if option.success_probability < 0.7:
                metrics.append("Success probability tracking và re-assessment")
            
            if option.risk_score > 0.4:
                metrics.append("Risk indicator monitoring và escalation")
            
            return metrics
            
        except Exception as e:
            logger.warning(f"Error defining monitoring metrics: {e}")
            return ["Basic progress tracking", "Standard performance indicators"]

    async def _identify_fallback_options(self,
                                       scored_options: List[Tuple[StrategyOption, float]],
                                       selected_option: StrategyOption) -> List[StrategyOption]:
        """Identify fallback options nếu primary fails"""
        try:
            fallback_options = []
            
            # Take top 2-3 alternatives excluding selected
            for option, score in scored_options[1:4]:  # Skip first (selected)
                if option != selected_option:
                    fallback_options.append(option)
            
            return fallback_options
            
        except Exception as e:
            logger.warning(f"Error identifying fallback options: {e}")
            return []

    async def _calculate_expected_outcomes(self, option: StrategyOption) -> Dict[str, float]:
        """Calculate expected outcomes từ option"""
        try:
            outcomes = {
                'expected_roi': option.expected_roi,
                'success_probability': option.success_probability,
                'risk_score': option.risk_score,
                'implementation_time': option.implementation_time,
                'learning_value': option.learning_potential,
                'confidence_level': option.confidence_score
            }
            
            # Calculate derived metrics
            outcomes['expected_value'] = option.expected_roi * option.success_probability
            outcomes['risk_adjusted_return'] = outcomes['expected_value'] * (1 - option.risk_score)
            outcomes['time_efficiency'] = outcomes['expected_value'] / max(option.implementation_time, 1)
            
            return outcomes
            
        except Exception as e:
            logger.warning(f"Error calculating expected outcomes: {e}")
            return {'error': str(e)}

    async def _calculate_optimization_confidence(self,
                                               selected_option: StrategyOption,
                                               scored_options: List[Tuple[StrategyOption, float]],
                                               context: DecisionContext) -> float:
        """Calculate confidence trong optimization decision"""
        try:
            confidence_factors = []
            
            # 1. Option quality
            option_confidence = selected_option.confidence_score
            confidence_factors.append(option_confidence * 0.4)
            
            # 2. Score margin
            if len(scored_options) > 1:
                best_score = scored_options[0][1]
                second_score = scored_options[1][1]
                score_margin = (best_score - second_score) / max(best_score, 0.1)
                margin_confidence = min(score_margin * 2, 1.0)
                confidence_factors.append(margin_confidence * 0.3)
            else:
                confidence_factors.append(0.8 * 0.3)  # High confidence if only one option
            
            # 3. Data completeness
            data_completeness = 0.9  # Assume good data quality
            confidence_factors.append(data_completeness * 0.2)
            
            # 4. Context appropriateness
            context_confidence = 0.8  # Default good context understanding
            if context == DecisionContext.EMERGENCY:
                context_confidence = 0.7  # Lower confidence trong emergency
            elif context == DecisionContext.EXPERIMENTAL:
                context_confidence = 0.6  # Lower confidence trong experimental
            
            confidence_factors.append(context_confidence * 0.1)
            
            total_confidence = sum(confidence_factors)
            return round(total_confidence, 3)
            
        except Exception as e:
            logger.warning(f"Error calculating optimization confidence: {e}")
            return 0.7

    async def _store_decision(self,
                            result: OptimizationResult,
                            original_options: List[StrategyOption],
                            context: DecisionContext,
                            optimization_strategy: OptimizationStrategy):
        """Store decision trong history cho learning"""
        try:
            decision_record = {
                'decision_id': result.recommendation_id,
                'timestamp': result.created_at.isoformat(),
                'selected_option_id': result.selected_option.option_id,
                'context': context.value,
                'optimization_strategy': optimization_strategy.value,
                'total_options': len(original_options),
                'confidence_score': result.confidence_score,
                'expected_roi': result.selected_option.expected_roi,
                'risk_score': result.selected_option.risk_score,
                'implementation_time': result.selected_option.implementation_time
            }
            
            self.decision_history.append(decision_record)
            
            # Keep only recent decisions (last 100)
            if len(self.decision_history) > 100:
                self.decision_history = self.decision_history[-100:]
            
            logger.info(f"Stored decision {result.recommendation_id} trong history")
            
        except Exception as e:
            logger.warning(f"Error storing decision: {e}")

    async def analyze_decision_patterns(self) -> Dict[str, Any]:
        """Analyze patterns trong decision history"""
        try:
            if not self.decision_history:
                return {"message": "No decision history available"}
            
            analysis = {
                'total_decisions': len(self.decision_history),
                'average_confidence': 0,
                'optimization_strategy_distribution': {},
                'context_distribution': {},
                'roi_trends': [],
                'risk_trends': [],
                'implementation_time_trends': []
            }
            
            # Calculate averages
            total_confidence = sum(d['confidence_score'] for d in self.decision_history)
            analysis['average_confidence'] = total_confidence / len(self.decision_history)
            
            # Strategy distribution
            strategy_counts = {}
            context_counts = {}
            
            for decision in self.decision_history:
                strategy = decision['optimization_strategy']
                context = decision['context']
                
                strategy_counts[strategy] = strategy_counts.get(strategy, 0) + 1
                context_counts[context] = context_counts.get(context, 0) + 1
                
                analysis['roi_trends'].append(decision['expected_roi'])
                analysis['risk_trends'].append(decision['risk_score'])
                analysis['implementation_time_trends'].append(decision['implementation_time'])
            
            analysis['optimization_strategy_distribution'] = strategy_counts
            analysis['context_distribution'] = context_counts
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing decision patterns: {e}")
            return {"error": str(e)}

    async def get_optimization_recommendations(self) -> Dict[str, Any]:
        """Get recommendations để improve optimization process"""
        try:
            recommendations = {
                'process_improvements': [],
                'parameter_adjustments': [],
                'monitoring_enhancements': [],
                'learning_opportunities': []
            }
            
            analysis = await self.analyze_decision_patterns()
            
            if analysis.get('total_decisions', 0) > 10:
                avg_confidence = analysis.get('average_confidence', 0)
                
                if avg_confidence < 0.7:
                    recommendations['process_improvements'].append(
                        "Consider improving data quality và option analysis depth"
                    )
                
                if avg_confidence > 0.9:
                    recommendations['parameter_adjustments'].append(
                        "Consider increasing risk tolerance để explore more innovative options"
                    )
                
                # ROI trends
                roi_trends = analysis.get('roi_trends', [])
                if roi_trends and len(roi_trends) > 5:
                    recent_roi = np.mean(roi_trends[-5:])
                    earlier_roi = np.mean(roi_trends[:-5]) if len(roi_trends) > 5 else recent_roi
                    
                    if recent_roi < earlier_roi * 0.9:
                        recommendations['monitoring_enhancements'].append(
                            "ROI performance declining - enhance outcome tracking"
                        )
            
            recommendations['learning_opportunities'].extend([
                "Analyze correlation between confidence scores và actual outcomes",
                "Track implementation success rates by optimization strategy",
                "Develop feedback loops từ implemented decisions"
            ])
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating optimization recommendations: {e}")
            return {"error": str(e)}

    def get_system_status(self) -> Dict[str, Any]:
        """Get strategy optimizer system status"""
        return {
            'total_decisions': len(self.decision_history),
            'optimization_parameters': {
                'roi_weight': self.roi_weight,
                'risk_weight': self.risk_weight,
                'speed_weight': self.speed_weight,
                'quality_weight': self.quality_weight,
                'resource_weight': self.resource_weight,
                'learning_weight': self.learning_weight
            },
            'thresholds': {
                'min_confidence': self.min_confidence_threshold,
                'max_risk_tolerance': self.max_risk_tolerance,
                'min_roi': self.min_roi_threshold
            },
            'recent_decisions': len([d for d in self.decision_history 
                                   if (datetime.now() - datetime.fromisoformat(d['timestamp'])).days <= 30])
        } 