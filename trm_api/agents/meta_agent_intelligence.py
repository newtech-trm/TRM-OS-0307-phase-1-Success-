#!/usr/bin/env python3
"""
Meta-Agent Intelligence System - TRM-OS v2.0

Meta-cognitive agent capabilities với self-improvement:
- Self-monitoring performance across all agents
- Performance analysis với pattern recognition  
- Optimization suggestions cho system evolution
- "Enzyme của hệ tiêu hóa" functionality

Philosophy: Meta-cognitive awareness cho autonomous system improvement
"""

import asyncio
import time
import math
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
import json

from trm_api.core.logging_config import get_logger
from trm_api.agents.base_agent import BaseAgent
from trm_api.eventbus.system_event_bus import SystemEventBus, SystemEvent, EventType
from trm_api.core.semantic_change_detector import SemanticChangeDetector

logger = get_logger(__name__)


class MetricType(str, Enum):
    """Types of metrics monitored"""
    PERFORMANCE = "performance"
    ACCURACY = "accuracy"
    EFFICIENCY = "efficiency"
    RESOURCE_USAGE = "resource_usage"
    SUCCESS_RATE = "success_rate"
    RESPONSE_TIME = "response_time"
    ERROR_RATE = "error_rate"
    LEARNING_RATE = "learning_rate"


class OptimizationCategory(str, Enum):
    """Categories of optimization suggestions"""
    ALGORITHM_IMPROVEMENT = "algorithm_improvement"
    RESOURCE_ALLOCATION = "resource_allocation"
    WORKFLOW_OPTIMIZATION = "workflow_optimization"
    LEARNING_ENHANCEMENT = "learning_enhancement"
    ERROR_REDUCTION = "error_reduction"
    PERFORMANCE_TUNING = "performance_tuning"
    CAPABILITY_EXPANSION = "capability_expansion"
    SYSTEM_INTEGRATION = "system_integration"


class SelfImprovementPriority(str, Enum):
    """Priority levels for self-improvement actions"""
    CRITICAL = "critical"      # System stability issues
    HIGH = "high"             # Performance degradation
    MEDIUM = "medium"         # Efficiency improvements
    LOW = "low"              # Optional enhancements
    EXPERIMENTAL = "experimental"  # Research improvements


@dataclass
class AgentPerformanceMetric:
    """Performance metric cho individual agent"""
    agent_id: str
    metric_type: MetricType
    value: float
    timestamp: datetime
    context: Dict[str, Any] = field(default_factory=dict)
    baseline_value: Optional[float] = None
    improvement_percentage: Optional[float] = None


@dataclass
class SystemPerformanceSnapshot:
    """Snapshot của toàn bộ system performance"""
    timestamp: datetime
    agent_metrics: List[AgentPerformanceMetric]
    system_metrics: Dict[str, float]
    bottlenecks_detected: List[str]
    performance_trends: Dict[str, float]
    overall_health_score: float


@dataclass
class OptimizationSuggestion:
    """Self-improvement optimization suggestion"""
    suggestion_id: str
    category: OptimizationCategory
    priority: SelfImprovementPriority
    target_agent: Optional[str]
    title: str
    description: str
    expected_improvement: float  # Percentage improvement expected
    implementation_effort: str  # "low", "medium", "high"
    risk_level: str  # "low", "medium", "high"
    success_probability: float  # 0.0 - 1.0
    suggested_actions: List[str]
    validation_criteria: List[str]
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class SelfImprovementPlan:
    """Comprehensive self-improvement plan"""
    plan_id: str
    created_at: datetime
    suggestions: List[OptimizationSuggestion]
    implementation_order: List[str]
    expected_total_improvement: float
    estimated_completion_time: timedelta
    risk_assessment: Dict[str, Any]
    success_metrics: Dict[str, float]


class PerformanceAnalyzer:
    """Analyzer cho agent performance patterns"""
    
    def __init__(self):
        self.logger = get_logger("performance_analyzer")
        self.baseline_metrics: Dict[str, Dict[MetricType, float]] = {}
        self.trend_history: Dict[str, List[AgentPerformanceMetric]] = {}
        self.bottleneck_patterns: Dict[str, int] = {}
        
        # Analysis thresholds
        self.performance_thresholds = {
            "degradation_warning": 0.15,  # 15% performance drop
            "degradation_critical": 0.30,  # 30% performance drop
            "improvement_significant": 0.20,  # 20% improvement
            "trend_window_hours": 24,  # Analysis window
            "min_samples_for_trend": 5  # Minimum samples for trend analysis
        }
    
    def update_baseline(self, agent_id: str, metric_type: MetricType, value: float) -> None:
        """Update baseline metrics cho agent"""
        if agent_id not in self.baseline_metrics:
            self.baseline_metrics[agent_id] = {}
        
        # Update baseline với exponential moving average
        if metric_type in self.baseline_metrics[agent_id]:
            current_baseline = self.baseline_metrics[agent_id][metric_type]
            # 90% current baseline, 10% new value
            self.baseline_metrics[agent_id][metric_type] = current_baseline * 0.9 + value * 0.1
        else:
            self.baseline_metrics[agent_id][metric_type] = value
    
    def analyze_performance_trend(
        self, 
        agent_id: str, 
        metric_type: MetricType
    ) -> Tuple[str, float]:
        """
        Analyze performance trend cho agent/metric
        Returns: (trend_direction, trend_strength)
        """
        if agent_id not in self.trend_history:
            return "insufficient_data", 0.0
        
        # Get recent metrics
        cutoff_time = datetime.now() - timedelta(hours=self.performance_thresholds["trend_window_hours"])
        recent_metrics = [
            metric for metric in self.trend_history[agent_id]
            if metric.metric_type == metric_type and metric.timestamp >= cutoff_time
        ]
        
        if len(recent_metrics) < self.performance_thresholds["min_samples_for_trend"]:
            return "insufficient_data", 0.0
        
        # Calculate trend using linear regression
        x_values = [(m.timestamp - recent_metrics[0].timestamp).total_seconds() for m in recent_metrics]
        y_values = [m.value for m in recent_metrics]
        
        if len(x_values) < 2:
            return "stable", 0.0
        
        # Simple linear regression
        n = len(x_values)
        sum_x = sum(x_values)
        sum_y = sum(y_values)
        sum_xy = sum(x * y for x, y in zip(x_values, y_values))
        sum_x2 = sum(x * x for x in x_values)
        
        if n * sum_x2 - sum_x * sum_x == 0:
            return "stable", 0.0
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
        
        # Determine trend direction và strength
        trend_strength = abs(slope) * 100  # Convert to percentage per second
        
        if abs(slope) < 0.001:  # Very small slope
            return "stable", trend_strength
        elif slope > 0:
            return "improving", trend_strength
        else:
            return "degrading", trend_strength
    
    def detect_bottlenecks(self, performance_snapshot: SystemPerformanceSnapshot) -> List[str]:
        """Detect system bottlenecks từ performance data"""
        bottlenecks = []
        
        # Analyze agent metrics for bottlenecks
        agent_response_times = {}
        agent_error_rates = {}
        
        for metric in performance_snapshot.agent_metrics:
            agent_id = metric.agent_id
            
            if metric.metric_type == MetricType.RESPONSE_TIME:
                agent_response_times[agent_id] = metric.value
            elif metric.metric_type == MetricType.ERROR_RATE:
                agent_error_rates[agent_id] = metric.value
        
        # Detect response time bottlenecks
        if agent_response_times:
            avg_response_time = sum(agent_response_times.values()) / len(agent_response_times)
            for agent_id, response_time in agent_response_times.items():
                if response_time > avg_response_time * 2:  # 2x slower than average
                    bottlenecks.append(f"response_time_bottleneck:{agent_id}")
                    self.bottleneck_patterns[f"response_time:{agent_id}"] = (
                        self.bottleneck_patterns.get(f"response_time:{agent_id}", 0) + 1
                    )
        
        # Detect error rate bottlenecks
        for agent_id, error_rate in agent_error_rates.items():
            if error_rate > 0.05:  # More than 5% error rate
                bottlenecks.append(f"error_rate_bottleneck:{agent_id}")
                self.bottleneck_patterns[f"error_rate:{agent_id}"] = (
                    self.bottleneck_patterns.get(f"error_rate:{agent_id}", 0) + 1
                )
        
        return bottlenecks
    
    def calculate_improvement_potential(
        self, 
        agent_id: str, 
        metric_type: MetricType,
        current_value: float
    ) -> float:
        """Calculate improvement potential cho metric"""
        if agent_id not in self.baseline_metrics:
            return 0.0
        
        if metric_type not in self.baseline_metrics[agent_id]:
            return 0.0
        
        baseline = self.baseline_metrics[agent_id][metric_type]
        
        if baseline == 0:
            return 0.0
        
        # Calculate improvement percentage
        improvement = ((current_value - baseline) / baseline) * 100
        return improvement


class SelfImprovementEngine:
    """Engine cho self-improvement suggestions"""
    
    def __init__(self):
        self.logger = get_logger("self_improvement_engine")
        self.suggestion_templates: Dict[OptimizationCategory, List[Dict[str, Any]]] = {}
        self.historical_suggestions: List[OptimizationSuggestion] = []
        self.implemented_suggestions: Dict[str, Dict[str, Any]] = {}
        
        self._initialize_suggestion_templates()
    
    def _initialize_suggestion_templates(self) -> None:
        """Initialize suggestion templates cho different optimization categories"""
        self.suggestion_templates = {
            OptimizationCategory.ALGORITHM_IMPROVEMENT: [
                {
                    "title": "Implement Caching Layer",
                    "description": "Add intelligent caching to reduce redundant computations",
                    "expected_improvement": 25.0,
                    "implementation_effort": "medium",
                    "risk_level": "low"
                },
                {
                    "title": "Optimize Query Patterns",
                    "description": "Refactor database queries for better performance",
                    "expected_improvement": 35.0,
                    "implementation_effort": "high",
                    "risk_level": "medium"
                },
                {
                    "title": "Implement Parallel Processing",
                    "description": "Add parallel processing capabilities cho heavy computations",
                    "expected_improvement": 45.0,
                    "implementation_effort": "high",
                    "risk_level": "medium"
                }
            ],
            OptimizationCategory.RESOURCE_ALLOCATION: [
                {
                    "title": "Dynamic Resource Scaling",
                    "description": "Implement auto-scaling based on workload patterns",
                    "expected_improvement": 30.0,
                    "implementation_effort": "high",
                    "risk_level": "medium"
                },
                {
                    "title": "Memory Pool Optimization",
                    "description": "Optimize memory allocation patterns",
                    "expected_improvement": 20.0,
                    "implementation_effort": "medium",
                    "risk_level": "low"
                }
            ],
            OptimizationCategory.LEARNING_ENHANCEMENT: [
                {
                    "title": "Adaptive Learning Rate",
                    "description": "Implement dynamic learning rate adjustment",
                    "expected_improvement": 40.0,
                    "implementation_effort": "medium",
                    "risk_level": "low"
                },
                {
                    "title": "Transfer Learning Integration",
                    "description": "Add transfer learning capabilities",
                    "expected_improvement": 50.0,
                    "implementation_effort": "high",
                    "risk_level": "medium"
                }
            ],
            OptimizationCategory.ERROR_REDUCTION: [
                {
                    "title": "Enhanced Error Handling",
                    "description": "Implement comprehensive error recovery mechanisms",
                    "expected_improvement": 60.0,
                    "implementation_effort": "medium",
                    "risk_level": "low"
                },
                {
                    "title": "Predictive Error Prevention",
                    "description": "Add predictive models to prevent common errors",
                    "expected_improvement": 70.0,
                    "implementation_effort": "high",
                    "risk_level": "medium"
                }
            ]
        }
    
    def generate_suggestions(
        self, 
        performance_snapshot: SystemPerformanceSnapshot,
        analyzer: PerformanceAnalyzer
    ) -> List[OptimizationSuggestion]:
        """Generate optimization suggestions based on performance analysis"""
        suggestions = []
        
        # Analyze each agent's performance
        for metric in performance_snapshot.agent_metrics:
            agent_id = metric.agent_id
            metric_type = metric.metric_type
            
            # Get trend analysis
            trend_direction, trend_strength = analyzer.analyze_performance_trend(agent_id, metric_type)
            
            # Get improvement potential
            improvement_potential = analyzer.calculate_improvement_potential(
                agent_id, metric_type, metric.value
            )
            
            # Generate suggestions based on analysis
            if trend_direction == "degrading" and trend_strength > 0.01:
                suggestions.extend(self._generate_degradation_suggestions(
                    agent_id, metric_type, trend_strength, improvement_potential
                ))
            
            elif improvement_potential < -20:  # Performance significantly below baseline
                suggestions.extend(self._generate_performance_suggestions(
                    agent_id, metric_type, improvement_potential
                ))
        
        # Generate bottleneck-specific suggestions
        for bottleneck in performance_snapshot.bottlenecks_detected:
            suggestions.extend(self._generate_bottleneck_suggestions(bottleneck))
        
        # Remove duplicates và sort by priority
        unique_suggestions = self._deduplicate_suggestions(suggestions)
        return sorted(unique_suggestions, key=lambda s: (s.priority.value, -s.expected_improvement))
    
    def _generate_degradation_suggestions(
        self, 
        agent_id: str, 
        metric_type: MetricType, 
        trend_strength: float,
        improvement_potential: float
    ) -> List[OptimizationSuggestion]:
        """Generate suggestions cho degrading performance"""
        suggestions = []
        
        if metric_type == MetricType.RESPONSE_TIME:
            template = self.suggestion_templates[OptimizationCategory.ALGORITHM_IMPROVEMENT][0]
            suggestions.append(OptimizationSuggestion(
                suggestion_id=f"cache_{agent_id}_{int(time.time())}",
                category=OptimizationCategory.ALGORITHM_IMPROVEMENT,
                priority=SelfImprovementPriority.HIGH if trend_strength > 0.05 else SelfImprovementPriority.MEDIUM,
                target_agent=agent_id,
                title=template["title"],
                description=f"{template['description']} cho {agent_id}",
                expected_improvement=min(template["expected_improvement"], abs(improvement_potential)),
                implementation_effort=template["implementation_effort"],
                risk_level=template["risk_level"],
                success_probability=0.8,
                suggested_actions=[
                    f"Analyze {agent_id} caching opportunities",
                    f"Implement Redis/in-memory cache for {agent_id}",
                    "Monitor cache hit rates và performance improvement"
                ],
                validation_criteria=[
                    f"Response time improvement > 15% for {agent_id}",
                    "Cache hit rate > 70%",
                    "No increase in error rates"
                ]
            ))
        
        elif metric_type == MetricType.ERROR_RATE:
            template = self.suggestion_templates[OptimizationCategory.ERROR_REDUCTION][0]
            suggestions.append(OptimizationSuggestion(
                suggestion_id=f"error_handling_{agent_id}_{int(time.time())}",
                category=OptimizationCategory.ERROR_REDUCTION,
                priority=SelfImprovementPriority.CRITICAL if trend_strength > 0.1 else SelfImprovementPriority.HIGH,
                target_agent=agent_id,
                title=template["title"],
                description=f"{template['description']} cho {agent_id}",
                expected_improvement=template["expected_improvement"],
                implementation_effort=template["implementation_effort"],
                risk_level=template["risk_level"],
                success_probability=0.9,
                suggested_actions=[
                    f"Audit error patterns in {agent_id}",
                    f"Implement robust error recovery for {agent_id}",
                    "Add error monitoring và alerting"
                ],
                validation_criteria=[
                    f"Error rate reduction > 50% for {agent_id}",
                    "Mean time to recovery < 30 seconds",
                    "No increase in response times"
                ]
            ))
        
        return suggestions
    
    def _generate_performance_suggestions(
        self, 
        agent_id: str, 
        metric_type: MetricType,
        improvement_potential: float
    ) -> List[OptimizationSuggestion]:
        """Generate suggestions cho poor performance"""
        suggestions = []
        
        if abs(improvement_potential) > 30:  # Significant underperformance
            template = self.suggestion_templates[OptimizationCategory.ALGORITHM_IMPROVEMENT][2]
            suggestions.append(OptimizationSuggestion(
                suggestion_id=f"parallel_{agent_id}_{int(time.time())}",
                category=OptimizationCategory.ALGORITHM_IMPROVEMENT,
                priority=SelfImprovementPriority.HIGH,
                target_agent=agent_id,
                title=template["title"],
                description=f"{template['description']} cho {agent_id}",
                expected_improvement=min(template["expected_improvement"], abs(improvement_potential)),
                implementation_effort=template["implementation_effort"],
                risk_level=template["risk_level"],
                success_probability=0.7,
                suggested_actions=[
                    f"Identify parallelizable operations in {agent_id}",
                    f"Implement async/parallel processing for {agent_id}",
                    "Benchmark performance improvements"
                ],
                validation_criteria=[
                    f"Performance improvement > 25% for {agent_id}",
                    "CPU utilization balanced across cores",
                    "No deadlocks or race conditions"
                ]
            ))
        
        return suggestions
    
    def _generate_bottleneck_suggestions(self, bottleneck: str) -> List[OptimizationSuggestion]:
        """Generate suggestions cho specific bottlenecks"""
        suggestions = []
        
        if "response_time_bottleneck" in bottleneck:
            agent_id = bottleneck.split(":")[1]
            template = self.suggestion_templates[OptimizationCategory.RESOURCE_ALLOCATION][0]
            suggestions.append(OptimizationSuggestion(
                suggestion_id=f"scaling_{agent_id}_{int(time.time())}",
                category=OptimizationCategory.RESOURCE_ALLOCATION,
                priority=SelfImprovementPriority.HIGH,
                target_agent=agent_id,
                title=template["title"],
                description=f"{template['description']} cho bottleneck in {agent_id}",
                expected_improvement=template["expected_improvement"],
                implementation_effort=template["implementation_effort"],
                risk_level=template["risk_level"],
                success_probability=0.75,
                suggested_actions=[
                    f"Implement auto-scaling for {agent_id}",
                    "Set up workload monitoring",
                    "Configure scaling thresholds"
                ],
                validation_criteria=[
                    "Response time bottleneck eliminated",
                    "Resource utilization optimized",
                    "Cost increase < 20%"
                ]
            ))
        
        return suggestions
    
    def _deduplicate_suggestions(self, suggestions: List[OptimizationSuggestion]) -> List[OptimizationSuggestion]:
        """Remove duplicate suggestions"""
        seen_combinations = set()
        unique_suggestions = []
        
        for suggestion in suggestions:
            key = (suggestion.category, suggestion.target_agent, suggestion.title)
            if key not in seen_combinations:
                seen_combinations.add(key)
                unique_suggestions.append(suggestion)
        
        return unique_suggestions


class MetaAgentIntelligence(BaseAgent):
    """
    Meta-Agent Intelligence với self-improvement capabilities
    
    "Enzyme của hệ tiêu hóa" - monitors, analyzes, và suggests improvements
    cho toàn bộ agent ecosystem
    """
    
    def __init__(self, agent_id: str = "meta_agent_intelligence"):
        super().__init__(agent_id)
        self.logger = get_logger("meta_agent_intelligence")
        
        # Core components
        self.performance_analyzer = PerformanceAnalyzer()
        self.improvement_engine = SelfImprovementEngine()
        self.semantic_detector = SemanticChangeDetector()
        self.event_bus = SystemEventBus()
        
        # Monitoring configuration
        self.monitoring_config = {
            "analysis_interval_seconds": 300,  # 5 minutes
            "deep_analysis_interval_seconds": 3600,  # 1 hour
            "snapshot_retention_days": 7,
            "auto_suggest_enabled": True,
            "auto_implement_threshold": 0.9  # Auto-implement if success probability > 90%
        }
        
        # State management
        self.performance_snapshots: List[SystemPerformanceSnapshot] = []
        self.active_suggestions: List[OptimizationSuggestion] = []
        self.monitoring_agents: Set[str] = set()
        self.is_monitoring = False
        
        # Statistics
        self.stats = {
            "total_analyses": 0,
            "suggestions_generated": 0,
            "suggestions_implemented": 0,
            "performance_improvements": 0,
            "agents_monitored": 0
        }
    
    async def initialize(self) -> bool:
        """Initialize Meta-Agent Intelligence system"""
        try:
            self.logger.info("Initializing Meta-Agent Intelligence...")
            
            # Subscribe to system events
            await self.event_bus.subscribe("agent.performance", self._handle_performance_event)
            await self.event_bus.subscribe("system.metric", self._handle_metric_event)
            await self.event_bus.subscribe("knowledge.evolved", self._handle_knowledge_evolution)
            
            # Start monitoring task
            asyncio.create_task(self._monitoring_loop())
            
            self.is_monitoring = True
            self.logger.info("Meta-Agent Intelligence initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Meta-Agent Intelligence: {e}")
            return False
    
    async def _monitoring_loop(self) -> None:
        """Main monitoring loop"""
        while self.is_monitoring:
            try:
                # Perform regular analysis
                await self._perform_analysis()
                
                # Wait for next analysis cycle
                await asyncio.sleep(self.monitoring_config["analysis_interval_seconds"])
                
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                await asyncio.sleep(60)  # Sleep longer on error
    
    async def _perform_analysis(self) -> None:
        """Perform comprehensive system analysis"""
        try:
            self.stats["total_analyses"] += 1
            
            # Collect current performance metrics
            snapshot = await self._collect_performance_snapshot()
            
            # Analyze performance trends
            bottlenecks = self.performance_analyzer.detect_bottlenecks(snapshot)
            snapshot.bottlenecks_detected = bottlenecks
            
            # Calculate system health score
            snapshot.overall_health_score = self._calculate_system_health(snapshot)
            
            # Store snapshot
            self.performance_snapshots.append(snapshot)
            self._cleanup_old_snapshots()
            
            # Generate improvement suggestions
            if self.monitoring_config["auto_suggest_enabled"]:
                suggestions = self.improvement_engine.generate_suggestions(
                    snapshot, self.performance_analyzer
                )
                
                self.active_suggestions.extend(suggestions)
                self.stats["suggestions_generated"] += len(suggestions)
                
                # Auto-implement high-confidence suggestions
                await self._process_auto_implementation(suggestions)
            
            # Publish analysis results
            await self.event_bus.publish(SystemEvent(
                event_type="meta_agent.analysis_complete",
                entity_id=self.agent_id,
                data={
                    "health_score": snapshot.overall_health_score,
                    "bottlenecks": len(bottlenecks),
                    "suggestions": len(suggestions) if suggestions else 0,
                    "agents_monitored": len(self.monitoring_agents)
                }
            ))
            
            self.logger.info(f"Analysis complete: Health={snapshot.overall_health_score:.2f}, "
                           f"Bottlenecks={len(bottlenecks)}, Agents={len(self.monitoring_agents)}")
            
        except Exception as e:
            self.logger.error(f"Error in analysis: {e}")
    
    async def _collect_performance_snapshot(self) -> SystemPerformanceSnapshot:
        """Collect current performance snapshot"""
        # This would integrate with actual agent metrics in production
        # For now, simulate metrics collection
        
        agent_metrics = []
        system_metrics = {}
        
        # Simulate collecting metrics from monitored agents
        for agent_id in self.monitoring_agents:
            # Response time metric
            agent_metrics.append(AgentPerformanceMetric(
                agent_id=agent_id,
                metric_type=MetricType.RESPONSE_TIME,
                value=0.5 + (hash(agent_id) % 100) / 200.0,  # Simulated
                timestamp=datetime.now()
            ))
            
            # Success rate metric  
            agent_metrics.append(AgentPerformanceMetric(
                agent_id=agent_id,
                metric_type=MetricType.SUCCESS_RATE,
                value=0.85 + (hash(agent_id) % 30) / 200.0,  # Simulated
                timestamp=datetime.now()
            ))
        
        # System-wide metrics
        system_metrics = {
            "total_throughput": len(self.monitoring_agents) * 100,
            "memory_usage": 0.6,
            "cpu_usage": 0.45,
            "active_connections": len(self.monitoring_agents) * 5
        }
        
        # Calculate performance trends
        performance_trends = {}
        for agent_id in self.monitoring_agents:
            trend_direction, trend_strength = self.performance_analyzer.analyze_performance_trend(
                agent_id, MetricType.RESPONSE_TIME
            )
            performance_trends[f"{agent_id}_response_trend"] = trend_strength if trend_direction == "improving" else -trend_strength
        
        return SystemPerformanceSnapshot(
            timestamp=datetime.now(),
            agent_metrics=agent_metrics,
            system_metrics=system_metrics,
            bottlenecks_detected=[],
            performance_trends=performance_trends,
            overall_health_score=0.0  # Will be calculated
        )
    
    def _calculate_system_health(self, snapshot: SystemPerformanceSnapshot) -> float:
        """Calculate overall system health score (0.0 - 1.0)"""
        health_factors = []
        
        # Agent performance health
        if snapshot.agent_metrics:
            response_times = [m.value for m in snapshot.agent_metrics if m.metric_type == MetricType.RESPONSE_TIME]
            success_rates = [m.value for m in snapshot.agent_metrics if m.metric_type == MetricType.SUCCESS_RATE]
            
            if response_times:
                avg_response_time = sum(response_times) / len(response_times)
                response_health = max(0.0, 1.0 - avg_response_time)  # Lower response time = better health
                health_factors.append(response_health)
            
            if success_rates:
                avg_success_rate = sum(success_rates) / len(success_rates)
                health_factors.append(avg_success_rate)
        
        # System metrics health
        system_metrics = snapshot.system_metrics
        if "memory_usage" in system_metrics:
            memory_health = max(0.0, 1.0 - system_metrics["memory_usage"])
            health_factors.append(memory_health)
        
        if "cpu_usage" in system_metrics:
            cpu_health = max(0.0, 1.0 - system_metrics["cpu_usage"])
            health_factors.append(cpu_health)
        
        # Bottleneck penalty
        bottleneck_penalty = len(snapshot.bottlenecks_detected) * 0.1
        
        # Calculate overall health
        if health_factors:
            base_health = sum(health_factors) / len(health_factors)
            overall_health = max(0.0, base_health - bottleneck_penalty)
        else:
            overall_health = 0.5  # Default health when no data
        
        return min(1.0, overall_health)
    
    async def _process_auto_implementation(self, suggestions: List[OptimizationSuggestion]) -> None:
        """Process suggestions for auto-implementation"""
        auto_threshold = self.monitoring_config["auto_implement_threshold"]
        
        for suggestion in suggestions:
            if (suggestion.success_probability >= auto_threshold and 
                suggestion.risk_level == "low" and
                suggestion.priority in [SelfImprovementPriority.CRITICAL, SelfImprovementPriority.HIGH]):
                
                # Auto-implement suggestion
                success = await self._implement_suggestion(suggestion)
                
                if success:
                    self.stats["suggestions_implemented"] += 1
                    self.logger.info(f"Auto-implemented suggestion: {suggestion.title}")
    
    async def _implement_suggestion(self, suggestion: OptimizationSuggestion) -> bool:
        """Implement optimization suggestion"""
        try:
            self.logger.info(f"Implementing suggestion: {suggestion.title}")
            
            # In production, this would contain actual implementation logic
            # For now, simulate implementation
            await asyncio.sleep(0.1)  # Simulate implementation time
            
            # Mark as implemented
            self.improvement_engine.implemented_suggestions[suggestion.suggestion_id] = {
                "implemented_at": datetime.now(),
                "status": "success",
                "actual_improvement": suggestion.expected_improvement * 0.8  # Simulate 80% of expected
            }
            
            # Publish implementation event
            await self.event_bus.publish(SystemEvent(
                event_type="meta_agent.suggestion_implemented",
                entity_id=suggestion.target_agent or "system",
                data={
                    "suggestion_id": suggestion.suggestion_id,
                    "category": suggestion.category.value,
                    "expected_improvement": suggestion.expected_improvement
                }
            ))
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to implement suggestion {suggestion.suggestion_id}: {e}")
            return False
    
    def _cleanup_old_snapshots(self) -> None:
        """Clean up old performance snapshots"""
        retention_limit = datetime.now() - timedelta(days=self.monitoring_config["snapshot_retention_days"])
        self.performance_snapshots = [
            snapshot for snapshot in self.performance_snapshots
            if snapshot.timestamp >= retention_limit
        ]
    
    async def _handle_performance_event(self, event: SystemEvent) -> None:
        """Handle agent performance events"""
        if event.data and "agent_id" in event.data:
            agent_id = event.data["agent_id"]
            self.monitoring_agents.add(agent_id)
            self.stats["agents_monitored"] = len(self.monitoring_agents)
            
            # Update performance analyzer
            if "metric_type" in event.data and "value" in event.data:
                metric_type = MetricType(event.data["metric_type"])
                value = event.data["value"]
                
                self.performance_analyzer.update_baseline(agent_id, metric_type, value)
                
                # Store in trend history
                if agent_id not in self.performance_analyzer.trend_history:
                    self.performance_analyzer.trend_history[agent_id] = []
                
                self.performance_analyzer.trend_history[agent_id].append(
                    AgentPerformanceMetric(
                        agent_id=agent_id,
                        metric_type=metric_type,
                        value=value,
                        timestamp=datetime.now()
                    )
                )
    
    async def _handle_metric_event(self, event: SystemEvent) -> None:
        """Handle system metric events"""
        # Process system-wide metrics
        pass
    
    async def _handle_knowledge_evolution(self, event: SystemEvent) -> None:
        """Handle knowledge evolution events"""
        # Process knowledge system changes that might affect performance
        pass
    
    def get_optimization_report(self) -> Dict[str, Any]:
        """Get comprehensive optimization report"""
        return {
            "system_status": {
                "monitoring_active": self.is_monitoring,
                "agents_monitored": len(self.monitoring_agents),
                "latest_health_score": (
                    self.performance_snapshots[-1].overall_health_score 
                    if self.performance_snapshots else 0.0
                )
            },
            "performance_statistics": self.stats,
            "active_suggestions": len(self.active_suggestions),
            "implemented_suggestions": len(self.improvement_engine.implemented_suggestions),
            "bottleneck_patterns": dict(self.performance_analyzer.bottleneck_patterns),
            "recent_snapshots": len(self.performance_snapshots)
        }
    
    async def shutdown(self) -> None:
        """Shutdown Meta-Agent Intelligence"""
        self.is_monitoring = False
        await self.event_bus.unsubscribe_all()
        self.logger.info("Meta-Agent Intelligence shut down")
    
    # Implementation của abstract methods từ BaseAgent
    async def _register_event_handlers(self) -> None:
        """Register event handlers cho Meta-Agent Intelligence"""
        try:
            # Subscribe to performance và system events
            self.subscribe_to_event(EventType.AGENT_PERFORMANCE)
            self.subscribe_to_event(EventType.SYSTEM_METRIC)
            self.subscribe_to_event(EventType.KNOWLEDGE_CREATED)
            self.subscribe_to_event(EventType.AGENT_ERROR)
            self.subscribe_to_event(EventType.TASK_COMPLETED)
            
            self.logger.info("Meta-Agent event handlers registered")
            
        except Exception as e:
            self.logger.error(f"Failed to register event handlers: {e}")
    
    async def _start_processing(self) -> None:
        """Start Meta-Agent processing loop"""
        try:
            # Start monitoring loop
            self.is_monitoring = True
            asyncio.create_task(self._monitoring_loop())
            
            self.logger.info("Meta-Agent processing started")
            
        except Exception as e:
            self.logger.error(f"Failed to start processing: {e}")
    
    async def _process_event(self, event: SystemEvent) -> None:
        """Process incoming events"""
        try:
            if event.event_type == "agent.performance":
                await self._handle_performance_event(event)
            elif event.event_type == "system.metric":
                await self._handle_metric_event(event)
            elif event.event_type == "knowledge.created":
                await self._handle_knowledge_evolution(event)
            elif event.event_type == "agent.error":
                await self._handle_agent_error_event(event)
            elif event.event_type == "task.completed":
                await self._handle_task_completion_event(event)
            else:
                self.logger.debug(f"Unhandled event type: {event.event_type}")
                
        except Exception as e:
            self.logger.error(f"Error processing event {event.event_type}: {e}")
    
    async def _handle_agent_error_event(self, event: SystemEvent) -> None:
        """Handle agent error events for meta-analysis"""
        if event.data and "agent_id" in event.data:
            agent_id = event.data["agent_id"]
            error_type = event.data.get("error_type", "unknown")
            
            # Track error patterns
            error_key = f"error:{agent_id}:{error_type}"
            self.performance_analyzer.bottleneck_patterns[error_key] = (
                self.performance_analyzer.bottleneck_patterns.get(error_key, 0) + 1
            )
            
            # Generate error reduction suggestions if pattern detected
            if self.performance_analyzer.bottleneck_patterns[error_key] >= 3:
                suggestions = self.improvement_engine._generate_degradation_suggestions(
                    agent_id, MetricType.ERROR_RATE, 0.1, -50.0
                )
                self.active_suggestions.extend(suggestions)
                self.stats["suggestions_generated"] += len(suggestions)
    
    async def _handle_task_completion_event(self, event: SystemEvent) -> None:
        """Handle task completion events for performance tracking"""
        if event.data and "agent_id" in event.data:
            agent_id = event.data["agent_id"]
            completion_time = event.data.get("completion_time", 0.0)
            success = event.data.get("success", True)
            
            # Update performance metrics
            if completion_time > 0:
                self.performance_analyzer.update_baseline(
                    agent_id, MetricType.RESPONSE_TIME, completion_time
                )
            
            success_rate = 1.0 if success else 0.0
            self.performance_analyzer.update_baseline(
                agent_id, MetricType.SUCCESS_RATE, success_rate
            )
            
            # Add agent to monitoring
            self.monitoring_agents.add(agent_id)
            self.stats["agents_monitored"] = len(self.monitoring_agents)


async def get_meta_agent_intelligence() -> MetaAgentIntelligence:
    """Get Meta-Agent Intelligence singleton"""
    return MetaAgentIntelligence() 