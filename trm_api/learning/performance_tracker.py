"""
Performance Tracker for Adaptive Learning System

Monitors and evaluates agent performance improvements over time.
Follows TRM-OS philosophy: Recognition → Event → WIN through performance measurement.
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict, deque
from statistics import mean, stdev
import math

from .learning_types import (
    PerformanceMetric,
    MetricType,
    LearningExperience,
    AdaptationRule,
    safe_enum_value
)
from ..eventbus.system_event_bus import publish_event, EventType


class PerformanceTracker:
    """Tracks and analyzes agent performance over time"""
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.logger = logging.getLogger(f"learning.performance_tracker.{agent_id}")
        
        # Performance data storage
        self.performance_metrics: Dict[str, PerformanceMetric] = {}
        self.performance_history: Dict[MetricType, deque] = defaultdict(lambda: deque(maxlen=1000))
        self.baseline_metrics: Dict[MetricType, float] = {}
        self.baseline_established: Dict[MetricType, bool] = defaultdict(bool)
        self.performance_targets: Dict[MetricType, float] = {}
        
        # Configuration
        self.baseline_sample_size = 10  # Number of samples needed to establish baseline
        self.significant_change_threshold = 0.1  # 10% change threshold
        
        # Statistics
        self.tracking_stats = {
            "total_measurements": 0,
            "metrics_tracked": 0,
            "improvements_detected": 0,
            "deteriorations_detected": 0,
            "baselines_established": 0,
            "targets_achieved": 0
        }
        
        # Initialize performance history for all metric types
        for metric_type in MetricType:
            self.performance_history[metric_type] = deque(maxlen=1000)
            self.baseline_established[metric_type] = False
        
        # Tracking configuration
        self.tracking_window_days = 30      # Days to keep in active tracking
    
    async def record_performance_metric(
        self,
        metric_type: MetricType,
        value: float,
        context: Dict[str, Any] = None,
        measurement_period: Tuple[datetime, datetime] = None
    ) -> str:
        """Record a performance measurement"""
        
        # Create measurement period if not provided
        if measurement_period is None:
            now = datetime.now()
            measurement_period = (now - timedelta(hours=1), now)
        
        # Create performance metric
        metric = PerformanceMetric(
            metric_type=metric_type,
            agent_id=self.agent_id,
            value=value,
            context=context or {},
            measurement_period=measurement_period
        )
        
        # Set baseline if not established
        if not self.baseline_established[metric_type]:
            if metric_type not in self.baseline_metrics:
                self.baseline_metrics[metric_type] = value
            metric.baseline = self.baseline_metrics[metric_type]
        else:
            metric.baseline = self.baseline_metrics[metric_type]
        
        # Set target if available
        if metric_type in self.performance_targets:
            metric.target = self.performance_targets[metric_type]
        
        # Calculate trend information
        await self._calculate_trend_info(metric)
        
        # Store metric
        self.performance_metrics[metric.metric_id] = metric
        
        # Add to history
        self.performance_history[metric_type].append({
            "timestamp": metric.timestamp,
            "value": value,
            "context": context or {}
        })
        
        # Update statistics
        self.tracking_stats["total_measurements"] += 1
        
        # Check for baseline establishment
        if not self.baseline_established[metric_type]:
            await self._check_baseline_establishment(metric_type)
        
        # Check for significant changes
        await self._check_significant_changes(metric)
        
        # Check target achievement
        await self._check_target_achievement(metric)
        
        self.logger.debug(f"Recorded {safe_enum_value(metric_type)} metric: {value}")
        
        # Create performance measurement event
        await publish_event(
            event_type=EventType.KNOWLEDGE_CREATED,
            source_agent_id=self.agent_id,
            entity_id=metric.metric_id,
            entity_type="performance_metric",
            data={
                "metric_type": safe_enum_value(metric_type),
                "value": value,
                "baseline": metric.baseline,
                "trend": metric.trend_direction,
                "change_rate": metric.change_rate
            }
        )
        
        return metric.metric_id
    
    async def _calculate_trend_info(self, metric: PerformanceMetric) -> None:
        """Calculate trend information for a metric"""
        
        history = self.performance_history[metric.metric_type]
        
        if len(history) < 2:
            metric.trend_direction = "stable"
            metric.change_rate = 0.0
            return
        
        # Get recent values for trend calculation
        recent_values = [item["value"] for item in list(history)[-10:]]  # Last 10 values
        
        if len(recent_values) < 2:
            metric.trend_direction = "stable"
            metric.change_rate = 0.0
            return
        
        # Calculate trend using linear regression slope
        n = len(recent_values)
        x_values = list(range(n))
        
        # Calculate slope
        x_mean = sum(x_values) / n
        y_mean = sum(recent_values) / n
        
        numerator = sum((x_values[i] - x_mean) * (recent_values[i] - y_mean) for i in range(n))
        denominator = sum((x_values[i] - x_mean) ** 2 for i in range(n))
        
        if denominator == 0:
            slope = 0
        else:
            slope = numerator / denominator
        
        # Determine trend direction
        if abs(slope) < 0.01:  # Very small slope
            metric.trend_direction = "stable"
        elif slope > 0:
            metric.trend_direction = "improving"
        else:
            metric.trend_direction = "declining"
        
        # Calculate change rate as percentage
        if len(recent_values) >= 2:
            first_value = recent_values[0]
            last_value = recent_values[-1]
            
            if first_value != 0:
                metric.change_rate = (last_value - first_value) / abs(first_value)
            else:
                metric.change_rate = last_value
        else:
            metric.change_rate = 0.0
    
    async def _check_baseline_establishment(self, metric_type: MetricType) -> None:
        """Check if we have enough data to establish a baseline"""
        
        history = self.performance_history[metric_type]
        
        if len(history) >= self.baseline_sample_size:
            # Calculate baseline as average of first samples
            baseline_values = [item["value"] for item in list(history)[:self.baseline_sample_size]]
            self.baseline_metrics[metric_type] = mean(baseline_values)
            self.baseline_established[metric_type] = True
            
            # Update all existing metrics with baseline
            for metric in self.performance_metrics.values():
                if metric.metric_type == metric_type:
                    metric.baseline = self.baseline_metrics[metric_type]
            
            self.tracking_stats["baselines_established"] += 1
            
            self.logger.info(f"Established baseline for {safe_enum_value(metric_type)}: {self.baseline_metrics[metric_type]:.3f}")
            
            # Create baseline establishment event
            await publish_event(
                event_type=EventType.KNOWLEDGE_CREATED,
                source_agent_id=self.agent_id,
                entity_id=f"baseline_{safe_enum_value(metric_type)}",
                entity_type="performance_baseline",
                data={
                    "metric_type": safe_enum_value(metric_type),
                    "baseline_value": self.baseline_metrics[metric_type],
                    "sample_size": self.baseline_sample_size
                }
            )
    
    async def _check_significant_changes(self, metric: PerformanceMetric) -> None:
        """Check for significant performance changes"""
        
        if not self.baseline_established[metric.metric_type]:
            return
        
        baseline = self.baseline_metrics[metric.metric_type]
        current_value = metric.value
        
        if baseline == 0:
            change_percentage = current_value
        else:
            change_percentage = abs(current_value - baseline) / abs(baseline)
        
        if change_percentage >= self.significant_change_threshold:
            is_improvement = current_value > baseline
            
            if is_improvement:
                self.tracking_stats["improvements_detected"] += 1
                change_type = "improvement"
            else:
                self.tracking_stats["deteriorations_detected"] += 1
                change_type = "deterioration"
            
            self.logger.info(
                f"Significant {change_type} detected in {safe_enum_value(metric.metric_type)}: "
                f"{current_value:.3f} vs baseline {baseline:.3f} "
                f"({change_percentage:.1%} change)"
            )
            
            # Create significant change event
            await publish_event(
                event_type=EventType.KNOWLEDGE_CREATED,
                source_agent_id=self.agent_id,
                entity_id=metric.metric_id,
                entity_type="performance_change",
                data={
                    "metric_type": safe_enum_value(metric.metric_type),
                    "change_type": change_type,
                    "current_value": current_value,
                    "baseline_value": baseline,
                    "change_percentage": change_percentage
                }
            )
    
    async def _check_target_achievement(self, metric: PerformanceMetric) -> None:
        """Check if performance targets have been achieved"""
        
        if metric.target is None:
            return
        
        target_achieved = metric.value >= metric.target
        
        if target_achieved:
            self.tracking_stats["targets_achieved"] += 1
            
            self.logger.info(
                f"Target achieved for {safe_enum_value(metric.metric_type)}: "
                f"{metric.value:.3f} >= {metric.target:.3f}"
            )
            
            # Create target achievement event
            await publish_event(
                event_type=EventType.AGENT_ACTION_COMPLETED,
                source_agent_id=self.agent_id,
                entity_id=metric.metric_id,
                entity_type="performance_target",
                data={
                    "metric_type": safe_enum_value(metric.metric_type),
                    "achieved_value": metric.value,
                    "target_value": metric.target
                }
            )
    
    async def analyze_performance_trends(
        self,
        metric_types: List[MetricType] = None,
        time_window_days: int = 30
    ) -> Dict[MetricType, Dict[str, Any]]:
        """Analyze performance trends over time"""
        
        if metric_types is None:
            metric_types = list(self.performance_history.keys())
        
        cutoff_date = datetime.now() - timedelta(days=time_window_days)
        trend_analysis = {}
        
        for metric_type in metric_types:
            history = self.performance_history[metric_type]
            
            # Filter to time window
            recent_data = [
                item for item in history
                if item["timestamp"] >= cutoff_date
            ]
            
            if len(recent_data) < 2:
                continue
            
            values = [item["value"] for item in recent_data]
            timestamps = [item["timestamp"] for item in recent_data]
            
            # Calculate trend statistics
            trend_stats = {
                "metric_type": safe_enum_value(metric_type),
                "sample_count": len(values),
                "time_span_days": (timestamps[-1] - timestamps[0]).days,
                "current_value": values[-1],
                "average_value": mean(values),
                "min_value": min(values),
                "max_value": max(values),
                "trend_direction": "stable",
                "improvement_rate": 0.0,
                "volatility": 0.0
            }
            
            # Calculate trend direction and rate
            if len(values) >= 2:
                first_half = values[:len(values)//2]
                second_half = values[len(values)//2:]
                
                if len(first_half) > 0 and len(second_half) > 0:
                    first_avg = mean(first_half)
                    second_avg = mean(second_half)
                    
                    if first_avg != 0:
                        improvement_rate = (second_avg - first_avg) / abs(first_avg)
                        trend_stats["improvement_rate"] = improvement_rate
                        
                        if improvement_rate > 0.05:  # 5% improvement
                            trend_stats["trend_direction"] = "improving"
                        elif improvement_rate < -0.05:  # 5% decline
                            trend_stats["trend_direction"] = "declining"
                        else:
                            trend_stats["trend_direction"] = "stable"
            
            # Calculate volatility (standard deviation)
            if len(values) > 1:
                trend_stats["volatility"] = stdev(values)
            
            # Add baseline comparison if available
            if self.baseline_established[metric_type]:
                baseline = self.baseline_metrics[metric_type]
                trend_stats["baseline_value"] = baseline
                
                if baseline != 0:
                    trend_stats["baseline_improvement"] = (values[-1] - baseline) / abs(baseline)
                else:
                    trend_stats["baseline_improvement"] = values[-1]
            
            trend_analysis[metric_type] = trend_stats
        
        return trend_analysis
    
    async def evaluate_adaptation_impact(
        self,
        adaptation_rules: List[AdaptationRule],
        time_window_days: int = 7
    ) -> Dict[str, Dict[str, Any]]:
        """Evaluate the impact of adaptations on performance"""
        
        impact_analysis = {}
        cutoff_date = datetime.now() - timedelta(days=time_window_days)
        
        for rule in adaptation_rules:
            if not rule.last_applied or rule.last_applied < cutoff_date:
                continue
            
            rule_impact = {
                "rule_id": rule.rule_id,
                "rule_name": rule.name,
                "adaptation_type": rule.safe_enum_value(adaptation_type),
                "applied_at": rule.last_applied,
                "applications": rule.applications,
                "effectiveness": rule.effectiveness,
                "performance_changes": {}
            }
            
            # Analyze performance changes after adaptation
            for metric_type, history in self.performance_history.items():
                # Get measurements before and after adaptation
                before_adaptation = [
                    item for item in history
                    if item["timestamp"] < rule.last_applied
                ]
                
                after_adaptation = [
                    item for item in history
                    if item["timestamp"] >= rule.last_applied
                ]
                
                if len(before_adaptation) >= 3 and len(after_adaptation) >= 3:
                    before_avg = mean([item["value"] for item in before_adaptation[-5:]])
                    after_avg = mean([item["value"] for item in after_adaptation[:5]])
                    
                    if before_avg != 0:
                        change_percentage = (after_avg - before_avg) / abs(before_avg)
                    else:
                        change_percentage = after_avg
                    
                    rule_impact["performance_changes"][safe_enum_value(metric_type)] = {
                        "before_average": before_avg,
                        "after_average": after_avg,
                        "change_percentage": change_percentage,
                        "improvement": change_percentage > 0
                    }
            
            impact_analysis[rule.rule_id] = rule_impact
        
        return impact_analysis
    
    def set_performance_target(
        self,
        metric_type: MetricType,
        target_value: float
    ) -> None:
        """Set a performance target for a metric"""
        
        self.performance_targets[metric_type] = target_value
        
        # Update existing metrics with target
        for metric in self.performance_metrics.values():
            if metric.metric_type == metric_type:
                metric.target = target_value
        
        self.logger.info(f"Set target for {safe_enum_value(metric_type)}: {target_value}")
    
    def get_current_performance(self) -> Dict[MetricType, float]:
        """Get current performance values for all tracked metrics"""
        
        current_performance = {}
        
        for metric_type, history in self.performance_history.items():
            if history:
                current_performance[metric_type] = history[-1]["value"]
        
        return current_performance
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get a comprehensive performance summary"""
        
        summary = {
            "agent_id": self.agent_id,
            "tracking_stats": self.tracking_stats.copy(),
            "metrics_tracked": len(self.performance_history),
            "baselines_established": len([
                metric_type for metric_type, established in self.baseline_established.items()
                if established
            ]),
            "targets_set": len(self.performance_targets),
            "current_performance": self.get_current_performance(),
            "baseline_metrics": self.baseline_metrics.copy(),
            "performance_targets": self.performance_targets.copy()
        }
        
        # Add recent trend information
        recent_trends = {}
        for metric_type, history in self.performance_history.items():
            if len(history) >= 2:
                recent_values = [item["value"] for item in list(history)[-5:]]
                if len(recent_values) >= 2:
                    first_val = recent_values[0]
                    last_val = recent_values[-1]
                    
                    if first_val != 0:
                        trend_change = (last_val - first_val) / abs(first_val)
                    else:
                        trend_change = last_val
                    
                    recent_trends[safe_enum_value(metric_type)] = {
                        "change_percentage": trend_change,
                        "direction": "improving" if trend_change > 0.01 else "declining" if trend_change < -0.01 else "stable"
                    }
        
        summary["recent_trends"] = recent_trends
        
        return summary
    
    def get_metric_history(
        self,
        metric_type: MetricType,
        days: int = 30
    ) -> List[Dict[str, Any]]:
        """Get historical data for a specific metric"""
        
        cutoff_date = datetime.now() - timedelta(days=days)
        history = self.performance_history[metric_type]
        
        return [
            item for item in history
            if item["timestamp"] >= cutoff_date
        ]
    
    def clear_performance_data(self) -> None:
        """Clear all performance data (use with caution)"""
        
        self.performance_metrics.clear()
        self.performance_history.clear()
        self.baseline_metrics.clear()
        self.baseline_established.clear()
        self.performance_targets.clear()
        
        self.tracking_stats = {
            "total_measurements": 0,
            "metrics_tracked": 0,
            "improvements_detected": 0,
            "deteriorations_detected": 0,
            "baselines_established": 0,
            "targets_achieved": 0
        }
        
        # Initialize performance history for all metric types
        for metric_type in MetricType:
            self.performance_history[metric_type] = deque(maxlen=1000)
            self.baseline_established[metric_type] = False
        
        self.logger.info("Cleared all performance data")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get performance tracking statistics"""
        return self.tracking_stats.copy()
    
    async def record_metric(
        self,
        metric_type: MetricType,
        value: float,
        context: Dict[str, Any] = None,
        measurement_period: Tuple[datetime, datetime] = None
    ) -> str:
        """Alias for record_performance_metric for backward compatibility"""
        return await self.record_performance_metric(metric_type, value, context, measurement_period)
    
    async def get_performance_trends(
        self,
        metric_types: List[MetricType] = None,
        time_window_days: int = 30
    ) -> Dict[MetricType, Dict[str, Any]]:
        """Alias for analyze_performance_trends for backward compatibility"""
        return await self.analyze_performance_trends(metric_types, time_window_days) 