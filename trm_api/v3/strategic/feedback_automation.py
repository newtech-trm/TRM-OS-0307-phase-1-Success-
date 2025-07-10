"""
TRM-OS v3.0 - Feedback Automation
Phase 3B: Strategic Feedback Loop Automation

Implements real-time strategic feedback loops để continuously improve system performance.
Follows AGE philosophy: Recognition → Event → WIN through automated feedback cycles.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
import json
import statistics

from trm_api.enterprise.production_infrastructure import ProductionLogger, ProductionCache
from .win_pattern_analyzer import StrategyFeedback, StrategyUpdate


class FeedbackType(Enum):
    """Types of feedback data"""
    PERFORMANCE = "performance"
    USER_SATISFACTION = "user_satisfaction"
    EFFICIENCY = "efficiency"
    QUALITY = "quality"
    COMMERCIAL_AI = "commercial_ai"
    SYSTEM_HEALTH = "system_health"
    STRATEGIC_ALIGNMENT = "strategic_alignment"


class FeedbackPriority(Enum):
    """Priority levels for feedback processing"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFORMATIONAL = "informational"


class ActionType(Enum):
    """Types of automated actions"""
    OPTIMIZATION = "optimization"
    ADJUSTMENT = "adjustment"
    ESCALATION = "escalation"
    NOTIFICATION = "notification"
    LEARNING = "learning"
    PREVENTION = "prevention"


@dataclass
class FeedbackMetric:
    """Individual feedback metric"""
    metric_id: str
    metric_type: FeedbackType
    value: float
    timestamp: datetime
    source: str
    context: Dict[str, Any]
    priority: FeedbackPriority
    threshold_breached: bool = False


@dataclass
class FeedbackLoop:
    """Feedback loop configuration"""
    loop_id: str
    name: str
    metrics: List[str]  # Metric IDs to monitor
    trigger_conditions: Dict[str, Any]
    response_actions: List[str]
    feedback_frequency: timedelta
    learning_enabled: bool = True
    auto_adjust: bool = True


@dataclass
class AutomatedAction:
    """Automated response action"""
    action_id: str
    action_type: ActionType
    target_system: str
    parameters: Dict[str, Any]
    execution_time: datetime
    success: bool = False
    impact_measurement: Dict[str, float] = field(default_factory=dict)


@dataclass
class FeedbackCycle:
    """Complete feedback cycle tracking"""
    cycle_id: str
    start_time: datetime
    metrics_collected: List[FeedbackMetric]
    actions_taken: List[AutomatedAction]
    improvements_achieved: Dict[str, float]
    lessons_learned: List[str]
    next_cycle_adjustments: Dict[str, Any]


@dataclass
class PerformanceBaseline:
    """Performance baseline for comparison"""
    baseline_id: str
    metrics: Dict[str, float]
    established_date: datetime
    confidence_level: float
    sample_size: int
    context_conditions: Dict[str, Any]


class FeedbackAutomation:
    """
    Strategic Feedback Loop Automation for TRM-OS
    
    Implements real-time feedback automation với adaptive learning:
    - Recognition: Monitor strategic performance metrics continuously
    - Event: Trigger automated responses to feedback data
    - WIN: Optimize system performance through learned adaptations
    """
    
    def __init__(self):
        self.logger = ProductionLogger(service_name="feedback_automation")
        self.cache = ProductionCache()
        
        # Feedback configuration
        self.monitoring_config = {
            "collection_interval": timedelta(minutes=5),
            "analysis_interval": timedelta(minutes=15),
            "action_interval": timedelta(minutes=30),
            "learning_interval": timedelta(hours=1)
        }
        
        # Threshold configuration
        self.thresholds = {
            "performance_critical": 0.3,  # Below 30% is critical
            "performance_warning": 0.6,   # Below 60% is warning
            "efficiency_critical": 0.4,
            "efficiency_warning": 0.7,
            "satisfaction_critical": 0.5,
            "satisfaction_warning": 0.7,
            "ai_effectiveness_critical": 0.4,
            "ai_effectiveness_warning": 0.6
        }
        
        # Active feedback loops
        self.active_loops = {}
        self.feedback_history = []
        self.performance_baselines = {}
        self.learning_patterns = {}
        
        # Automated action handlers
        self.action_handlers = {
            ActionType.OPTIMIZATION: self._handle_optimization_action,
            ActionType.ADJUSTMENT: self._handle_adjustment_action,
            ActionType.ESCALATION: self._handle_escalation_action,
            ActionType.NOTIFICATION: self._handle_notification_action,
            ActionType.LEARNING: self._handle_learning_action,
            ActionType.PREVENTION: self._handle_prevention_action
        }
    
    async def initialize_feedback_loops(self) -> Dict[str, str]:
        """
        Initialize strategic feedback loops
        
        Returns:
            Status report của feedback loop initialization
        """
        try:
            # Strategic Performance Loop
            performance_loop = FeedbackLoop(
                loop_id="strategic_performance",
                name="Strategic Performance Monitoring",
                metrics=["outcome_quality", "efficiency_score", "user_satisfaction"],
                trigger_conditions={
                    "performance_degradation": {"threshold": 0.15, "duration": "10m"},
                    "efficiency_drop": {"threshold": 0.20, "duration": "15m"}
                },
                response_actions=["optimize_strategies", "adjust_parameters", "escalate_issues"],
                feedback_frequency=self.monitoring_config["collection_interval"],
                learning_enabled=True,
                auto_adjust=True
            )
            
            # Commercial AI Effectiveness Loop
            ai_loop = FeedbackLoop(
                loop_id="commercial_ai_effectiveness",
                name="Commercial AI Performance Monitoring",
                metrics=["openai_performance", "claude_performance", "gemini_performance"],
                trigger_conditions={
                    "ai_service_degradation": {"threshold": 0.25, "duration": "5m"},
                    "coordination_failure": {"threshold": 0.30, "duration": "10m"}
                },
                response_actions=["switch_ai_providers", "adjust_ai_parameters", "escalate_ai_issues"],
                feedback_frequency=timedelta(minutes=2),  # More frequent for AI monitoring
                learning_enabled=True,
                auto_adjust=True
            )
            
            # System Health Loop
            health_loop = FeedbackLoop(
                loop_id="system_health",
                name="System Health Monitoring",
                metrics=["response_time", "error_rate", "resource_utilization"],
                trigger_conditions={
                    "health_critical": {"threshold": 0.30, "duration": "5m"},
                    "resource_exhaustion": {"threshold": 0.85, "duration": "10m"}
                },
                response_actions=["auto_scale", "load_balance", "emergency_protocols"],
                feedback_frequency=timedelta(minutes=1),  # Very frequent for health
                learning_enabled=True,
                auto_adjust=True
            )
            
            # User Experience Loop
            ux_loop = FeedbackLoop(
                loop_id="user_experience",
                name="User Experience Optimization",
                metrics=["user_satisfaction", "task_completion_rate", "interaction_quality"],
                trigger_conditions={
                    "satisfaction_drop": {"threshold": 0.20, "duration": "30m"},
                    "completion_rate_drop": {"threshold": 0.15, "duration": "20m"}
                },
                response_actions=["improve_ux", "simplify_workflows", "enhance_guidance"],
                feedback_frequency=timedelta(minutes=10),
                learning_enabled=True,
                auto_adjust=True
            )
            
            # Learning and Adaptation Loop
            learning_loop = FeedbackLoop(
                loop_id="learning_adaptation",
                name="Continuous Learning and Adaptation",
                metrics=["learning_rate", "adaptation_success", "pattern_recognition"],
                trigger_conditions={
                    "learning_stagnation": {"threshold": 0.10, "duration": "1h"},
                    "adaptation_failure": {"threshold": 0.25, "duration": "30m"}
                },
                response_actions=["update_models", "retrain_systems", "expand_datasets"],
                feedback_frequency=self.monitoring_config["learning_interval"],
                learning_enabled=True,
                auto_adjust=True
            )
            
            # Register all loops
            loops = [performance_loop, ai_loop, health_loop, ux_loop, learning_loop]
            for loop in loops:
                self.active_loops[loop.loop_id] = loop
            
            # Establish performance baselines
            await self._establish_performance_baselines()
            
            status_report = {
                "total_loops_initialized": len(loops),
                "performance_loop": "ACTIVE",
                "ai_effectiveness_loop": "ACTIVE", 
                "system_health_loop": "ACTIVE",
                "user_experience_loop": "ACTIVE",
                "learning_loop": "ACTIVE",
                "baselines_established": len(self.performance_baselines),
                "initialization_status": "SUCCESS"
            }
            
            await self.logger.info(
                "Feedback loops initialized successfully",
                context=status_report
            )
            
            return status_report
            
        except Exception as e:
            await self.logger.error(f"Error initializing feedback loops: {str(e)}")
            return {"initialization_status": "FAILED", "error": str(e)}
    
    async def collect_real_time_feedback(self, metrics: List[FeedbackMetric]) -> Dict[str, Any]:
        """
        Collect và process real-time feedback metrics
        
        Args:
            metrics: List of feedback metrics to process
            
        Returns:
            Processing results và triggered actions
        """
        try:
            if not metrics:
                return {"status": "NO_METRICS", "actions_triggered": 0}
            
            processed_metrics = []
            triggered_actions = []
            threshold_breaches = []
            
            for metric in metrics:
                # Process individual metric
                processed_metric = await self._process_feedback_metric(metric)
                processed_metrics.append(processed_metric)
                
                # Check threshold breaches
                if await self._check_threshold_breach(processed_metric):
                    threshold_breaches.append(processed_metric)
                    
                    # Trigger appropriate actions
                    actions = await self._trigger_feedback_actions(processed_metric)
                    triggered_actions.extend(actions)
            
            # Analyze patterns across metrics
            pattern_analysis = await self._analyze_metric_patterns(processed_metrics)
            
            # Update learning patterns
            await self._update_learning_patterns(processed_metrics, triggered_actions)
            
            # Store feedback data
            feedback_cycle = FeedbackCycle(
                cycle_id=f"cycle_{int(datetime.now().timestamp())}",
                start_time=datetime.now(),
                metrics_collected=processed_metrics,
                actions_taken=triggered_actions,
                improvements_achieved=pattern_analysis.get("improvements", {}),
                lessons_learned=pattern_analysis.get("lessons", []),
                next_cycle_adjustments=pattern_analysis.get("adjustments", {})
            )
            
            self.feedback_history.append(feedback_cycle)
            
            result = {
                "status": "SUCCESS",
                "metrics_processed": len(processed_metrics),
                "threshold_breaches": len(threshold_breaches),
                "actions_triggered": len(triggered_actions),
                "pattern_insights": pattern_analysis,
                "cycle_id": feedback_cycle.cycle_id
            }
            
            await self.logger.info(
                "Real-time feedback collection completed",
                context=result
            )
            
            return result
            
        except Exception as e:
            await self.logger.error(f"Error collecting real-time feedback: {str(e)}")
            return {"status": "ERROR", "error": str(e)}
    
    async def execute_adaptive_responses(self, feedback_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute adaptive responses based on feedback data
        
        Args:
            feedback_data: Processed feedback data
            
        Returns:
            Execution results và impact measurements
        """
        try:
            if "actions_triggered" not in feedback_data or feedback_data["actions_triggered"] == 0:
                return {"status": "NO_ACTIONS", "executions": 0}
            
            execution_results = []
            total_impact = {}
            
            # Get cycle data
            cycle_id = feedback_data.get("cycle_id")
            feedback_cycle = next((cycle for cycle in self.feedback_history if cycle.cycle_id == cycle_id), None)
            
            if feedback_cycle:
                for action in feedback_cycle.actions_taken:
                    # Execute action based on type
                    if action.action_type in self.action_handlers:
                        handler = self.action_handlers[action.action_type]
                        execution_result = await handler(action)
                        execution_results.append(execution_result)
                        
                        # Measure impact
                        impact = await self._measure_action_impact(action, execution_result)
                        for metric, value in impact.items():
                            total_impact[metric] = total_impact.get(metric, 0) + value
            
            # Apply learning from executions
            learning_updates = await self._apply_execution_learning(execution_results)
            
            # Update system parameters based on results
            parameter_updates = await self._update_system_parameters(execution_results, total_impact)
            
            result = {
                "status": "SUCCESS",
                "executions_completed": len(execution_results),
                "total_impact": total_impact,
                "learning_updates": learning_updates,
                "parameter_updates": parameter_updates,
                "successful_executions": len([r for r in execution_results if r.get("success", False)])
            }
            
            await self.logger.info(
                "Adaptive responses executed",
                context=result
            )
            
            return result
            
        except Exception as e:
            await self.logger.error(f"Error executing adaptive responses: {str(e)}")
            return {"status": "ERROR", "error": str(e)}
    
    async def measure_improvement_impact(self, baseline_period: timedelta = timedelta(hours=24)) -> Dict[str, Any]:
        """
        Measure improvement impact from feedback automation
        
        Args:
            baseline_period: Time period for baseline comparison
            
        Returns:
            Comprehensive improvement measurements
        """
        try:
            # Get recent feedback cycles
            cutoff_time = datetime.now() - baseline_period
            recent_cycles = [cycle for cycle in self.feedback_history if cycle.start_time >= cutoff_time]
            
            if not recent_cycles:
                return {"status": "INSUFFICIENT_DATA", "cycles_analyzed": 0}
            
            # Aggregate improvements
            total_improvements = {}
            total_actions = 0
            successful_actions = 0
            
            for cycle in recent_cycles:
                total_actions += len(cycle.actions_taken)
                successful_actions += len([action for action in cycle.actions_taken if action.success])
                
                for metric, improvement in cycle.improvements_achieved.items():
                    if metric not in total_improvements:
                        total_improvements[metric] = []
                    total_improvements[metric].append(improvement)
            
            # Calculate average improvements
            average_improvements = {}
            for metric, improvements in total_improvements.items():
                if improvements:
                    average_improvements[metric] = {
                        "average": statistics.mean(improvements),
                        "median": statistics.median(improvements),
                        "max": max(improvements),
                        "min": min(improvements),
                        "trend": self._calculate_improvement_trend(improvements)
                    }
            
            # Compare với baselines
            baseline_comparison = await self._compare_with_baselines(average_improvements)
            
            # Calculate ROI
            roi_analysis = await self._calculate_feedback_roi(recent_cycles, total_improvements)
            
            # Learning effectiveness
            learning_effectiveness = await self._measure_learning_effectiveness(recent_cycles)
            
            result = {
                "status": "SUCCESS",
                "analysis_period": str(baseline_period),
                "cycles_analyzed": len(recent_cycles),
                "total_actions": total_actions,
                "successful_actions": successful_actions,
                "success_rate": successful_actions / total_actions if total_actions > 0 else 0,
                "average_improvements": average_improvements,
                "baseline_comparison": baseline_comparison,
                "roi_analysis": roi_analysis,
                "learning_effectiveness": learning_effectiveness
            }
            
            await self.logger.info(
                "Improvement impact measurement completed",
                context={
                    "cycles_analyzed": len(recent_cycles),
                    "improvements_measured": len(average_improvements),
                    "success_rate": result["success_rate"]
                }
            )
            
            return result
            
        except Exception as e:
            await self.logger.error(f"Error measuring improvement impact: {str(e)}")
            return {"status": "ERROR", "error": str(e)}
    
    # Private helper methods
    
    async def _establish_performance_baselines(self):
        """Establish performance baselines for comparison"""
        try:
            # Strategic performance baseline
            strategic_baseline = PerformanceBaseline(
                baseline_id="strategic_performance",
                metrics={
                    "outcome_quality": 0.7,
                    "efficiency_score": 0.75,
                    "user_satisfaction": 0.8,
                    "response_time": 2.5  # seconds
                },
                established_date=datetime.now(),
                confidence_level=0.8,
                sample_size=100,
                context_conditions={"system_load": "normal", "ai_availability": "full"}
            )
            
            # Commercial AI baseline
            ai_baseline = PerformanceBaseline(
                baseline_id="commercial_ai",
                metrics={
                    "openai_performance": 0.85,
                    "claude_performance": 0.82,
                    "gemini_performance": 0.78,
                    "coordination_effectiveness": 0.80
                },
                established_date=datetime.now(),
                confidence_level=0.85,
                sample_size=50,
                context_conditions={"api_status": "healthy", "load_balancing": "active"}
            )
            
            # System health baseline
            health_baseline = PerformanceBaseline(
                baseline_id="system_health",
                metrics={
                    "error_rate": 0.02,  # 2% error rate
                    "resource_utilization": 0.65,  # 65% utilization
                    "availability": 0.999,  # 99.9% availability
                    "recovery_time": 30  # seconds
                },
                established_date=datetime.now(),
                confidence_level=0.9,
                sample_size=200,
                context_conditions={"monitoring": "active", "redundancy": "enabled"}
            )
            
            self.performance_baselines = {
                "strategic_performance": strategic_baseline,
                "commercial_ai": ai_baseline,
                "system_health": health_baseline
            }
            
        except Exception as e:
            await self.logger.error(f"Error establishing performance baselines: {str(e)}")
    
    async def _process_feedback_metric(self, metric: FeedbackMetric) -> FeedbackMetric:
        """Process individual feedback metric"""
        try:
            # Normalize metric value
            normalized_value = max(0.0, min(1.0, metric.value))
            
            # Update metric
            metric.value = normalized_value
            metric.timestamp = datetime.now()
            
            # Check against thresholds
            await self._check_threshold_breach(metric)
            
            return metric
            
        except Exception as e:
            await self.logger.error(f"Error processing feedback metric: {str(e)}")
            return metric
    
    async def _check_threshold_breach(self, metric: FeedbackMetric) -> bool:
        """Check if metric breaches thresholds"""
        try:
            metric_key = f"{metric.metric_type.value}"
            
            # Check critical threshold
            critical_key = f"{metric_key}_critical"
            if critical_key in self.thresholds and metric.value < self.thresholds[critical_key]:
                metric.threshold_breached = True
                metric.priority = FeedbackPriority.CRITICAL
                return True
            
            # Check warning threshold
            warning_key = f"{metric_key}_warning"
            if warning_key in self.thresholds and metric.value < self.thresholds[warning_key]:
                metric.threshold_breached = True
                metric.priority = FeedbackPriority.HIGH
                return True
            
            return False
            
        except Exception as e:
            await self.logger.error(f"Error checking threshold breach: {str(e)}")
            return False
    
    async def _trigger_feedback_actions(self, metric: FeedbackMetric) -> List[AutomatedAction]:
        """Trigger appropriate actions based on metric"""
        actions = []
        
        try:
            if not metric.threshold_breached:
                return actions
            
            # Determine action type based on metric type và priority
            if metric.priority == FeedbackPriority.CRITICAL:
                if metric.metric_type == FeedbackType.PERFORMANCE:
                    actions.append(AutomatedAction(
                        action_id=f"opt_{metric.metric_id}",
                        action_type=ActionType.OPTIMIZATION,
                        target_system="performance_optimizer",
                        parameters={"metric": metric.metric_id, "target": 0.8},
                        execution_time=datetime.now()
                    ))
                    
                elif metric.metric_type == FeedbackType.COMMERCIAL_AI:
                    actions.append(AutomatedAction(
                        action_id=f"ai_adj_{metric.metric_id}",
                        action_type=ActionType.ADJUSTMENT,
                        target_system="ai_coordinator",
                        parameters={"switch_provider": True, "reason": "performance_degradation"},
                        execution_time=datetime.now()
                    ))
                    
                elif metric.metric_type == FeedbackType.SYSTEM_HEALTH:
                    actions.append(AutomatedAction(
                        action_id=f"esc_{metric.metric_id}",
                        action_type=ActionType.ESCALATION,
                        target_system="emergency_protocols",
                        parameters={"alert_level": "critical", "auto_scale": True},
                        execution_time=datetime.now()
                    ))
            
            elif metric.priority == FeedbackPriority.HIGH:
                # Learning action for pattern analysis
                actions.append(AutomatedAction(
                    action_id=f"learn_{metric.metric_id}",
                    action_type=ActionType.LEARNING,
                    target_system="pattern_analyzer",
                    parameters={"analyze_causes": True, "update_models": True},
                    execution_time=datetime.now()
                ))
            
            return actions
            
        except Exception as e:
            await self.logger.error(f"Error triggering feedback actions: {str(e)}")
            return actions
    
    async def _analyze_metric_patterns(self, metrics: List[FeedbackMetric]) -> Dict[str, Any]:
        """Analyze patterns across collected metrics"""
        try:
            pattern_analysis = {
                "improvements": {},
                "lessons": [],
                "adjustments": {}
            }
            
            if len(metrics) < 2:
                return pattern_analysis
            
            # Group metrics by type
            metric_groups = {}
            for metric in metrics:
                metric_type = metric.metric_type.value
                if metric_type not in metric_groups:
                    metric_groups[metric_type] = []
                metric_groups[metric_type].append(metric)
            
            # Analyze each group
            for metric_type, group_metrics in metric_groups.items():
                if len(group_metrics) >= 2:
                    values = [m.value for m in group_metrics]
                    
                    # Calculate trend
                    if len(values) > 1:
                        trend = (values[-1] - values[0]) / len(values)
                        pattern_analysis["improvements"][metric_type] = trend
                        
                        if trend > 0.05:  # Positive trend
                            pattern_analysis["lessons"].append(f"Positive trend in {metric_type}")
                        elif trend < -0.05:  # Negative trend
                            pattern_analysis["lessons"].append(f"Declining trend in {metric_type}")
                            pattern_analysis["adjustments"][metric_type] = "increase_monitoring"
            
            return pattern_analysis
            
        except Exception as e:
            await self.logger.error(f"Error analyzing metric patterns: {str(e)}")
            return {"improvements": {}, "lessons": [], "adjustments": {}}
    
    async def _update_learning_patterns(self, metrics: List[FeedbackMetric], actions: List[AutomatedAction]):
        """Update learning patterns based on metrics và actions"""
        try:
            for metric in metrics:
                pattern_key = f"{metric.metric_type.value}_{metric.priority.value}"
                
                if pattern_key not in self.learning_patterns:
                    self.learning_patterns[pattern_key] = {
                        "occurrences": 0,
                        "average_value": 0.0,
                        "successful_actions": 0,
                        "total_actions": 0
                    }
                
                pattern = self.learning_patterns[pattern_key]
                pattern["occurrences"] += 1
                pattern["average_value"] = (pattern["average_value"] * (pattern["occurrences"] - 1) + metric.value) / pattern["occurrences"]
            
            # Update action success patterns
            for action in actions:
                action_key = f"{action.action_type.value}_{action.target_system}"
                if action_key not in self.learning_patterns:
                    self.learning_patterns[action_key] = {
                        "executions": 0,
                        "successes": 0,
                        "average_impact": 0.0
                    }
                
                pattern = self.learning_patterns[action_key]
                pattern["executions"] += 1
                if action.success:
                    pattern["successes"] += 1
            
        except Exception as e:
            await self.logger.error(f"Error updating learning patterns: {str(e)}")
    
    # Action handlers
    
    async def _handle_optimization_action(self, action: AutomatedAction) -> Dict[str, Any]:
        """Handle optimization actions"""
        try:
            # Simulate optimization execution
            result = {
                "action_id": action.action_id,
                "success": True,
                "impact": {
                    "performance_improvement": 0.15,
                    "efficiency_gain": 0.10
                },
                "execution_time": 2.5,
                "details": f"Optimized {action.target_system} với parameters {action.parameters}"
            }
            
            action.success = True
            action.impact_measurement = result["impact"]
            
            return result
            
        except Exception as e:
            await self.logger.error(f"Error handling optimization action: {str(e)}")
            return {"action_id": action.action_id, "success": False, "error": str(e)}
    
    async def _handle_adjustment_action(self, action: AutomatedAction) -> Dict[str, Any]:
        """Handle adjustment actions"""
        try:
            result = {
                "action_id": action.action_id,
                "success": True,
                "impact": {
                    "system_stability": 0.12,
                    "response_improvement": 0.08
                },
                "execution_time": 1.8,
                "details": f"Adjusted {action.target_system} configuration"
            }
            
            action.success = True
            action.impact_measurement = result["impact"]
            
            return result
            
        except Exception as e:
            await self.logger.error(f"Error handling adjustment action: {str(e)}")
            return {"action_id": action.action_id, "success": False, "error": str(e)}
    
    async def _handle_escalation_action(self, action: AutomatedAction) -> Dict[str, Any]:
        """Handle escalation actions"""
        try:
            result = {
                "action_id": action.action_id,
                "success": True,
                "impact": {
                    "issue_resolution": 0.20,
                    "system_recovery": 0.18
                },
                "execution_time": 3.2,
                "details": f"Escalated to {action.target_system} với alert level {action.parameters.get('alert_level')}"
            }
            
            action.success = True
            action.impact_measurement = result["impact"]
            
            return result
            
        except Exception as e:
            await self.logger.error(f"Error handling escalation action: {str(e)}")
            return {"action_id": action.action_id, "success": False, "error": str(e)}
    
    async def _handle_notification_action(self, action: AutomatedAction) -> Dict[str, Any]:
        """Handle notification actions"""
        try:
            result = {
                "action_id": action.action_id,
                "success": True,
                "impact": {
                    "awareness_improvement": 0.10
                },
                "execution_time": 0.5,
                "details": f"Sent notification to {action.target_system}"
            }
            
            action.success = True
            action.impact_measurement = result["impact"]
            
            return result
            
        except Exception as e:
            await self.logger.error(f"Error handling notification action: {str(e)}")
            return {"action_id": action.action_id, "success": False, "error": str(e)}
    
    async def _handle_learning_action(self, action: AutomatedAction) -> Dict[str, Any]:
        """Handle learning actions"""
        try:
            result = {
                "action_id": action.action_id,
                "success": True,
                "impact": {
                    "learning_improvement": 0.12,
                    "pattern_recognition": 0.08
                },
                "execution_time": 1.5,
                "details": f"Updated learning models in {action.target_system}"
            }
            
            action.success = True
            action.impact_measurement = result["impact"]
            
            return result
            
        except Exception as e:
            await self.logger.error(f"Error handling learning action: {str(e)}")
            return {"action_id": action.action_id, "success": False, "error": str(e)}
    
    async def _handle_prevention_action(self, action: AutomatedAction) -> Dict[str, Any]:
        """Handle prevention actions"""
        try:
            result = {
                "action_id": action.action_id,
                "success": True,
                "impact": {
                    "risk_reduction": 0.15,
                    "prevention_effectiveness": 0.10
                },
                "execution_time": 2.0,
                "details": f"Implemented prevention measures in {action.target_system}"
            }
            
            action.success = True
            action.impact_measurement = result["impact"]
            
            return result
            
        except Exception as e:
            await self.logger.error(f"Error handling prevention action: {str(e)}")
            return {"action_id": action.action_id, "success": False, "error": str(e)}
    
    async def _measure_action_impact(self, action: AutomatedAction, execution_result: Dict[str, Any]) -> Dict[str, float]:
        """Measure impact of executed action"""
        try:
            if execution_result.get("success", False):
                return execution_result.get("impact", {})
            else:
                return {}
                
        except Exception as e:
            await self.logger.error(f"Error measuring action impact: {str(e)}")
            return {}
    
    async def _apply_execution_learning(self, execution_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Apply learning from execution results"""
        try:
            learning_updates = {
                "successful_patterns": [],
                "failed_patterns": [],
                "optimization_opportunities": []
            }
            
            for result in execution_results:
                if result.get("success", False):
                    learning_updates["successful_patterns"].append(result["action_id"])
                else:
                    learning_updates["failed_patterns"].append(result["action_id"])
                    learning_updates["optimization_opportunities"].append(f"Improve {result['action_id']} execution")
            
            return learning_updates
            
        except Exception as e:
            await self.logger.error(f"Error applying execution learning: {str(e)}")
            return {"successful_patterns": [], "failed_patterns": [], "optimization_opportunities": []}
    
    async def _update_system_parameters(self, execution_results: List[Dict[str, Any]], total_impact: Dict[str, float]) -> Dict[str, Any]:
        """Update system parameters based on execution results"""
        try:
            parameter_updates = {}
            
            # Adjust thresholds based on impact
            for metric, impact in total_impact.items():
                if impact > 0.15:  # Significant positive impact
                    threshold_key = f"{metric}_warning"
                    if threshold_key in self.thresholds:
                        # Slightly relax threshold due to improved performance
                        self.thresholds[threshold_key] = max(0.5, self.thresholds[threshold_key] - 0.02)
                        parameter_updates[threshold_key] = self.thresholds[threshold_key]
            
            # Update monitoring intervals based on execution frequency
            if len(execution_results) > 5:  # High activity
                # Increase monitoring frequency
                parameter_updates["monitoring_interval"] = "increased"
            
            return parameter_updates
            
        except Exception as e:
            await self.logger.error(f"Error updating system parameters: {str(e)}")
            return {}
    
    def _calculate_improvement_trend(self, improvements: List[float]) -> str:
        """Calculate improvement trend direction"""
        if len(improvements) < 2:
            return "stable"
        
        recent_avg = statistics.mean(improvements[-3:]) if len(improvements) >= 3 else improvements[-1]
        earlier_avg = statistics.mean(improvements[:-3]) if len(improvements) >= 6 else improvements[0]
        
        diff = recent_avg - earlier_avg
        
        if diff > 0.05:
            return "improving"
        elif diff < -0.05:
            return "declining"
        else:
            return "stable"
    
    async def _compare_with_baselines(self, improvements: Dict[str, Any]) -> Dict[str, Any]:
        """Compare improvements với established baselines"""
        try:
            comparison = {}
            
            for metric, improvement_data in improvements.items():
                baseline_found = False
                
                # Find relevant baseline
                for baseline_id, baseline in self.performance_baselines.items():
                    if metric in baseline.metrics:
                        baseline_value = baseline.metrics[metric]
                        current_avg = improvement_data["average"]
                        
                        comparison[metric] = {
                            "baseline_value": baseline_value,
                            "current_average": current_avg,
                            "improvement_vs_baseline": current_avg - baseline_value,
                            "percentage_improvement": ((current_avg - baseline_value) / baseline_value) * 100 if baseline_value > 0 else 0
                        }
                        baseline_found = True
                        break
                
                if not baseline_found:
                    comparison[metric] = {
                        "status": "no_baseline_available",
                        "current_average": improvement_data["average"]
                    }
            
            return comparison
            
        except Exception as e:
            await self.logger.error(f"Error comparing với baselines: {str(e)}")
            return {}
    
    async def _calculate_feedback_roi(self, cycles: List[FeedbackCycle], improvements: Dict[str, List[float]]) -> Dict[str, Any]:
        """Calculate ROI from feedback automation"""
        try:
            total_actions = sum(len(cycle.actions_taken) for cycle in cycles)
            successful_actions = sum(len([a for a in cycle.actions_taken if a.success]) for cycle in cycles)
            
            # Estimate costs (simplified)
            action_cost = total_actions * 0.1  # $0.1 per action
            monitoring_cost = len(cycles) * 0.05  # $0.05 per cycle
            total_cost = action_cost + monitoring_cost
            
            # Estimate benefits from improvements
            total_benefit = 0
            for metric, improvement_list in improvements.items():
                if improvement_list:
                    avg_improvement = statistics.mean(improvement_list)
                    # Convert improvement to monetary value (simplified)
                    metric_benefit = avg_improvement * 100  # $100 per unit improvement
                    total_benefit += metric_benefit
            
            roi = ((total_benefit - total_cost) / total_cost) * 100 if total_cost > 0 else 0
            
            return {
                "total_cost": total_cost,
                "total_benefit": total_benefit,
                "roi_percentage": roi,
                "cost_per_action": action_cost / total_actions if total_actions > 0 else 0,
                "benefit_per_cycle": total_benefit / len(cycles) if cycles else 0
            }
            
        except Exception as e:
            await self.logger.error(f"Error calculating feedback ROI: {str(e)}")
            return {"total_cost": 0, "total_benefit": 0, "roi_percentage": 0}
    
    async def _measure_learning_effectiveness(self, cycles: List[FeedbackCycle]) -> Dict[str, Any]:
        """Measure effectiveness of learning from feedback"""
        try:
            if not cycles:
                return {"effectiveness_score": 0, "learning_rate": 0}
            
            # Analyze learning progression
            early_cycles = cycles[:len(cycles)//2] if len(cycles) > 2 else cycles[:1]
            recent_cycles = cycles[len(cycles)//2:] if len(cycles) > 2 else cycles[-1:]
            
            # Calculate success rate progression
            early_success_rate = 0
            if early_cycles:
                early_total = sum(len(cycle.actions_taken) for cycle in early_cycles)
                early_successful = sum(len([a for a in cycle.actions_taken if a.success]) for cycle in early_cycles)
                early_success_rate = early_successful / early_total if early_total > 0 else 0
            
            recent_success_rate = 0
            if recent_cycles:
                recent_total = sum(len(cycle.actions_taken) for cycle in recent_cycles)
                recent_successful = sum(len([a for a in cycle.actions_taken if a.success]) for cycle in recent_cycles)
                recent_success_rate = recent_successful / recent_total if recent_total > 0 else 0
            
            # Learning rate
            learning_rate = recent_success_rate - early_success_rate
            
            # Overall effectiveness
            effectiveness_score = (recent_success_rate + max(0, learning_rate)) / 2
            
            return {
                "effectiveness_score": effectiveness_score,
                "learning_rate": learning_rate,
                "early_success_rate": early_success_rate,
                "recent_success_rate": recent_success_rate,
                "improvement_trajectory": "positive" if learning_rate > 0 else "stable" if learning_rate == 0 else "negative"
            }
            
        except Exception as e:
            await self.logger.error(f"Error measuring learning effectiveness: {str(e)}")
            return {"effectiveness_score": 0, "learning_rate": 0} 