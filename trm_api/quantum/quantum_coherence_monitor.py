"""
Quantum Coherence Monitor - Real-time System Coherence Tracking
Monitor và maintain quantum system coherence với intelligent alerts
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import numpy as np
from uuid import uuid4

from ..learning.adaptive_learning_system import AdaptiveLearningSystem
from ..learning.learning_types import LearningExperience, ExperienceType
from ..eventbus.system_event_bus import publish_event
from .quantum_types import QuantumState, QuantumSystem, QuantumStateType


class CoherenceAlertLevel(Enum):
    """Levels of coherence alerts"""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"


class CoherenceMetricType(Enum):
    """Types of coherence metrics"""
    SYSTEM_COHERENCE = "system_coherence"
    STATE_STABILITY = "state_stability"
    ENTANGLEMENT_STRENGTH = "entanglement_strength"
    DECOHERENCE_RATE = "decoherence_rate"
    TRANSITION_SMOOTHNESS = "transition_smoothness"
    QUANTUM_FIDELITY = "quantum_fidelity"


@dataclass
class CoherenceMetric:
    """Individual coherence metric"""
    metric_id: str
    metric_type: CoherenceMetricType
    name: str
    description: str
    current_value: float
    threshold_warning: float
    threshold_critical: float
    threshold_emergency: float
    trend: str = "stable"  # improving, declining, stable
    history: List[Tuple[datetime, float]] = field(default_factory=list)
    
    def get_alert_level(self) -> CoherenceAlertLevel:
        """Get current alert level based on value"""
        if self.current_value <= self.threshold_emergency:
            return CoherenceAlertLevel.EMERGENCY
        elif self.current_value <= self.threshold_critical:
            return CoherenceAlertLevel.CRITICAL
        elif self.current_value <= self.threshold_warning:
            return CoherenceAlertLevel.WARNING
        else:
            return CoherenceAlertLevel.INFO
    
    def update_value(self, new_value: float) -> None:
        """Update metric value và history"""
        self.history.append((datetime.now(), self.current_value))
        self.current_value = new_value
        
        # Keep only last 100 values
        if len(self.history) > 100:
            self.history = self.history[-100:]
        
        # Update trend
        self._update_trend()
    
    def _update_trend(self) -> None:
        """Update trend based on recent history"""
        if len(self.history) < 3:
            self.trend = "stable"
            return
        
        recent_values = [val for _, val in self.history[-3:]]
        recent_values.append(self.current_value)
        
        # Simple trend calculation
        if recent_values[-1] > recent_values[0] * 1.05:
            self.trend = "improving"
        elif recent_values[-1] < recent_values[0] * 0.95:
            self.trend = "declining"
        else:
            self.trend = "stable"


@dataclass
class CoherenceAlert:
    """Coherence alert notification"""
    alert_id: str
    alert_level: CoherenceAlertLevel
    metric_type: CoherenceMetricType
    message: str
    current_value: float
    threshold_value: float
    system_id: str
    timestamp: datetime = field(default_factory=datetime.now)
    acknowledged: bool = False
    resolved: bool = False


@dataclass
class CoherenceReport:
    """Comprehensive coherence report"""
    report_id: str
    system_id: str
    overall_coherence: float
    coherence_grade: str  # A, B, C, D, F
    metrics: List[CoherenceMetric]
    alerts: List[CoherenceAlert]
    recommendations: List[str]
    timestamp: datetime = field(default_factory=datetime.now)


class QuantumCoherenceMonitor:
    """
    Real-time Quantum Coherence Monitor
    Monitor và maintain quantum system coherence với intelligent alerts
    """
    
    def __init__(self, learning_system: AdaptiveLearningSystem):
        self.learning_system = learning_system
        self.logger = logging.getLogger(__name__)
        
        # Monitoring state
        self.monitored_systems: Dict[str, QuantumSystem] = {}
        self.coherence_metrics: Dict[str, Dict[str, CoherenceMetric]] = {}
        self.active_alerts: Dict[str, CoherenceAlert] = {}
        self.coherence_history: List[CoherenceReport] = {}
        
        # Configuration
        self.monitoring_interval = 30  # seconds
        self.alert_cooldown = 300  # 5 minutes
        self.history_retention_days = 30
        
        # Thresholds
        self.default_thresholds = {
            CoherenceMetricType.SYSTEM_COHERENCE: {
                "warning": 0.5,
                "critical": 0.3,
                "emergency": 0.1
            },
            CoherenceMetricType.STATE_STABILITY: {
                "warning": 0.6,
                "critical": 0.4,
                "emergency": 0.2
            },
            CoherenceMetricType.ENTANGLEMENT_STRENGTH: {
                "warning": 0.4,
                "critical": 0.2,
                "emergency": 0.1
            },
            CoherenceMetricType.DECOHERENCE_RATE: {
                "warning": 0.3,  # Higher is worse for decoherence
                "critical": 0.5,
                "emergency": 0.7
            }
        }
        
        # Background tasks
        self.monitoring_task: Optional[asyncio.Task] = None
        self.is_monitoring = False
        
        # Statistics
        self.monitoring_stats = {
            "total_measurements": 0,
            "alerts_generated": 0,
            "critical_incidents": 0,
            "average_coherence": 0.0,
            "uptime_percentage": 100.0
        }
        
        self.logger.info("QuantumCoherenceMonitor initialized")
    
    async def initialize(self) -> None:
        """Initialize coherence monitor"""
        
        try:
            # Setup default metrics
            await self._setup_default_metrics()
            
            # Start monitoring
            await self.start_monitoring()
            
            self.logger.info("QuantumCoherenceMonitor initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize QuantumCoherenceMonitor: {e}")
            raise
    
    async def add_system_to_monitor(self, quantum_system: QuantumSystem) -> None:
        """Add quantum system to monitoring"""
        
        system_id = quantum_system.system_id
        self.monitored_systems[system_id] = quantum_system
        
        # Initialize metrics for this system
        await self._initialize_system_metrics(system_id)
        
        self.logger.info(f"Added system to monitoring: {system_id}")
    
    async def remove_system_from_monitor(self, system_id: str) -> None:
        """Remove quantum system from monitoring"""
        
        if system_id in self.monitored_systems:
            del self.monitored_systems[system_id]
        
        if system_id in self.coherence_metrics:
            del self.coherence_metrics[system_id]
        
        # Remove related alerts
        alerts_to_remove = [
            alert_id for alert_id, alert in self.active_alerts.items()
            if alert.system_id == system_id
        ]
        for alert_id in alerts_to_remove:
            del self.active_alerts[alert_id]
        
        self.logger.info(f"Removed system from monitoring: {system_id}")
    
    async def get_coherence_report(self, system_id: str) -> Optional[CoherenceReport]:
        """Get comprehensive coherence report for system"""
        
        if system_id not in self.monitored_systems:
            return None
        
        try:
            quantum_system = self.monitored_systems[system_id]
            metrics = self.coherence_metrics.get(system_id, {})
            
            # Calculate overall coherence
            overall_coherence = await self._calculate_overall_coherence(system_id)
            
            # Determine coherence grade
            coherence_grade = self._calculate_coherence_grade(overall_coherence)
            
            # Get active alerts for this system
            system_alerts = [
                alert for alert in self.active_alerts.values()
                if alert.system_id == system_id and not alert.resolved
            ]
            
            # Generate recommendations
            recommendations = await self._generate_coherence_recommendations(
                system_id, overall_coherence, system_alerts
            )
            
            report = CoherenceReport(
                report_id=str(uuid4()),
                system_id=system_id,
                overall_coherence=overall_coherence,
                coherence_grade=coherence_grade,
                metrics=list(metrics.values()),
                alerts=system_alerts,
                recommendations=recommendations
            )
            
            # Store report
            if system_id not in self.coherence_history:
                self.coherence_history[system_id] = []
            self.coherence_history[system_id].append(report)
            
            # Cleanup old reports
            await self._cleanup_old_reports(system_id)
            
            return report
            
        except Exception as e:
            self.logger.error(f"Failed to generate coherence report: {e}")
            return None
    
    async def get_real_time_metrics(self, system_id: str) -> Dict[str, Any]:
        """Get real-time coherence metrics"""
        
        if system_id not in self.monitored_systems:
            return {"error": "System not found"}
        
        try:
            quantum_system = self.monitored_systems[system_id]
            metrics = self.coherence_metrics.get(system_id, {})
            
            # Update metrics
            await self._update_system_metrics(system_id)
            
            real_time_data = {
                "system_id": system_id,
                "timestamp": datetime.now().isoformat(),
                "overall_coherence": quantum_system.calculate_system_coherence(),
                "metrics": {
                    metric_id: {
                        "type": metric.metric_type.value,
                        "name": metric.name,
                        "current_value": metric.current_value,
                        "trend": metric.trend,
                        "alert_level": metric.get_alert_level().value
                    }
                    for metric_id, metric in metrics.items()
                },
                "active_alerts_count": len([
                    alert for alert in self.active_alerts.values()
                    if alert.system_id == system_id and not alert.resolved
                ]),
                "system_status": await self._determine_system_status(system_id)
            }
            
            return real_time_data
            
        except Exception as e:
            self.logger.error(f"Failed to get real-time metrics: {e}")
            return {"error": str(e)}
    
    async def acknowledge_alert(self, alert_id: str, acknowledged_by: str = "system") -> bool:
        """Acknowledge coherence alert"""
        
        if alert_id not in self.active_alerts:
            return False
        
        alert = self.active_alerts[alert_id]
        alert.acknowledged = True
        
        # Record acknowledgment event
        await publish_event(
            event_type="coherence_alert_ack",
            source_agent_id="coherence_monitor",
            entity_id=alert_id,
            entity_type="coherence_alert_ack",
            data={
                "alert_level": alert.alert_level.value,
                "metric_type": alert.metric_type.value,
                "acknowledged_by": acknowledged_by,
                "system_id": alert.system_id
            }
        )
        
        self.logger.info(f"Alert acknowledged: {alert_id} by {acknowledged_by}")
        return True
    
    async def resolve_alert(self, alert_id: str, resolved_by: str = "system") -> bool:
        """Resolve coherence alert"""
        
        if alert_id not in self.active_alerts:
            return False
        
        alert = self.active_alerts[alert_id]
        alert.resolved = True
        
        # Record resolution event
        await publish_event(
            event_type="coherence_alert_resolved",
            source_agent_id="coherence_monitor",
            entity_id=alert_id,
            entity_type="coherence_alert_resolved",
            data={
                "alert_level": alert.alert_level.value,
                "metric_type": alert.metric_type.value,
                "resolved_by": resolved_by,
                "system_id": alert.system_id,
                "resolution_time": (datetime.now() - alert.timestamp).total_seconds()
            }
        )
        
        self.logger.info(f"Alert resolved: {alert_id} by {resolved_by}")
        return True
    
    async def start_monitoring(self) -> None:
        """Start coherence monitoring"""
        
        if self.is_monitoring:
            return
        
        self.is_monitoring = True
        self.monitoring_task = asyncio.create_task(self._monitoring_loop())
        
        self.logger.info("Coherence monitoring started")
    
    async def stop_monitoring(self) -> None:
        """Stop coherence monitoring"""
        
        self.is_monitoring = False
        
        if self.monitoring_task and not self.monitoring_task.done():
            self.monitoring_task.cancel()
            try:
                await self.monitoring_task
            except asyncio.CancelledError:
                pass
        
        self.logger.info("Coherence monitoring stopped")
    
    def get_monitoring_statistics(self) -> Dict[str, Any]:
        """Get monitoring statistics"""
        
        return {
            **self.monitoring_stats,
            "monitored_systems": len(self.monitored_systems),
            "active_alerts": len([a for a in self.active_alerts.values() if not a.resolved]),
            "total_metrics": sum(len(metrics) for metrics in self.coherence_metrics.values()),
            "is_monitoring": self.is_monitoring
        }
    
    # Private methods
    
    async def _setup_default_metrics(self) -> None:
        """Setup default coherence metrics"""
        
        self.default_metric_configs = [
            {
                "type": CoherenceMetricType.SYSTEM_COHERENCE,
                "name": "System Coherence",
                "description": "Overall quantum system coherence level"
            },
            {
                "type": CoherenceMetricType.STATE_STABILITY,
                "name": "State Stability",
                "description": "Stability of quantum states"
            },
            {
                "type": CoherenceMetricType.ENTANGLEMENT_STRENGTH,
                "name": "Entanglement Strength",
                "description": "Strength of quantum entanglements"
            },
            {
                "type": CoherenceMetricType.DECOHERENCE_RATE,
                "name": "Decoherence Rate",
                "description": "Rate of quantum decoherence"
            }
        ]
        
        self.logger.info("Default metrics configuration setup")
    
    async def _initialize_system_metrics(self, system_id: str) -> None:
        """Initialize metrics for a system"""
        
        self.coherence_metrics[system_id] = {}
        
        for config in self.default_metric_configs:
            metric_id = f"{system_id}_{config['type'].value}"
            thresholds = self.default_thresholds[config['type']]
            
            metric = CoherenceMetric(
                metric_id=metric_id,
                metric_type=config['type'],
                name=config['name'],
                description=config['description'],
                current_value=0.5,  # Default value
                threshold_warning=thresholds['warning'],
                threshold_critical=thresholds['critical'],
                threshold_emergency=thresholds['emergency']
            )
            
            self.coherence_metrics[system_id][metric_id] = metric
        
        self.logger.info(f"Initialized metrics for system: {system_id}")
    
    async def _monitoring_loop(self) -> None:
        """Main monitoring loop"""
        
        while self.is_monitoring:
            try:
                # Update metrics for all systems
                for system_id in self.monitored_systems:
                    await self._update_system_metrics(system_id)
                    await self._check_alerts(system_id)
                
                # Update statistics
                await self._update_monitoring_stats()
                
                # Learn from monitoring data
                await self._learn_from_monitoring()
                
                await asyncio.sleep(self.monitoring_interval)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                await asyncio.sleep(self.monitoring_interval)
    
    async def _update_system_metrics(self, system_id: str) -> None:
        """Update metrics for a specific system"""
        
        if system_id not in self.monitored_systems or system_id not in self.coherence_metrics:
            return
        
        quantum_system = self.monitored_systems[system_id]
        metrics = self.coherence_metrics[system_id]
        
        # Calculate current metric values
        metric_values = await self._calculate_metric_values(quantum_system)
        
        # Update each metric
        for metric_id, metric in metrics.items():
            if metric.metric_type in metric_values:
                new_value = metric_values[metric.metric_type]
                metric.update_value(new_value)
        
        self.monitoring_stats["total_measurements"] += 1
    
    async def _calculate_metric_values(self, quantum_system: QuantumSystem) -> Dict[CoherenceMetricType, float]:
        """Calculate current metric values for system"""
        
        values = {}
        
        # System coherence
        values[CoherenceMetricType.SYSTEM_COHERENCE] = quantum_system.calculate_system_coherence()
        
        # State stability (average of state probabilities)
        if quantum_system.quantum_states:
            state_probs = [state.probability for state in quantum_system.quantum_states.values()]
            values[CoherenceMetricType.STATE_STABILITY] = np.mean(state_probs)
        else:
            values[CoherenceMetricType.STATE_STABILITY] = 0.0
        
        # Entanglement strength (mock calculation)
        entanglement_count = sum(len(states) for states in quantum_system.entanglement_network.values())
        total_possible = len(quantum_system.quantum_states) * (len(quantum_system.quantum_states) - 1)
        if total_possible > 0:
            values[CoherenceMetricType.ENTANGLEMENT_STRENGTH] = entanglement_count / total_possible
        else:
            values[CoherenceMetricType.ENTANGLEMENT_STRENGTH] = 0.0
        
        # Decoherence rate (inverse of coherence)
        values[CoherenceMetricType.DECOHERENCE_RATE] = 1.0 - values[CoherenceMetricType.SYSTEM_COHERENCE]
        
        return values
    
    async def _check_alerts(self, system_id: str) -> None:
        """Check for alert conditions"""
        
        if system_id not in self.coherence_metrics:
            return
        
        metrics = self.coherence_metrics[system_id]
        
        for metric_id, metric in metrics.items():
            alert_level = metric.get_alert_level()
            
            # Only create alert if not INFO level và not recently alerted
            if alert_level != CoherenceAlertLevel.INFO:
                if not await self._has_recent_alert(system_id, metric.metric_type, alert_level):
                    await self._create_alert(system_id, metric, alert_level)
    
    async def _has_recent_alert(
        self,
        system_id: str,
        metric_type: CoherenceMetricType,
        alert_level: CoherenceAlertLevel
    ) -> bool:
        """Check if there's a recent alert for this metric"""
        
        cutoff_time = datetime.now() - timedelta(seconds=self.alert_cooldown)
        
        for alert in self.active_alerts.values():
            if (alert.system_id == system_id and 
                alert.metric_type == metric_type and
                alert.alert_level == alert_level and
                alert.timestamp > cutoff_time and
                not alert.resolved):
                return True
        
        return False
    
    async def _create_alert(
        self,
        system_id: str,
        metric: CoherenceMetric,
        alert_level: CoherenceAlertLevel
    ) -> None:
        """Create new coherence alert"""
        
        alert_id = str(uuid4())
        
        # Determine threshold value
        if alert_level == CoherenceAlertLevel.EMERGENCY:
            threshold = metric.threshold_emergency
        elif alert_level == CoherenceAlertLevel.CRITICAL:
            threshold = metric.threshold_critical
        else:
            threshold = metric.threshold_warning
        
        # Create alert message
        message = (
            f"{alert_level.value.upper()}: {metric.name} is {metric.current_value:.3f}, "
            f"below threshold of {threshold:.3f} for system {system_id}"
        )
        
        alert = CoherenceAlert(
            alert_id=alert_id,
            alert_level=alert_level,
            metric_type=metric.metric_type,
            message=message,
            current_value=metric.current_value,
            threshold_value=threshold,
            system_id=system_id
        )
        
        self.active_alerts[alert_id] = alert
        self.monitoring_stats["alerts_generated"] += 1
        
        if alert_level in [CoherenceAlertLevel.CRITICAL, CoherenceAlertLevel.EMERGENCY]:
            self.monitoring_stats["critical_incidents"] += 1
        
        # Publish alert event
        await publish_event(
            event_type="coherence_alert",
            source_agent_id="coherence_monitor",
            entity_id=alert_id,
            entity_type="coherence_alert",
            data={
                "alert_level": alert_level.value,
                "metric_type": metric.metric_type.value,
                "current_value": metric.current_value,
                "threshold_value": threshold,
                "system_id": system_id,
                "message": message
            }
        )
        
        self.logger.warning(f"Coherence alert created: {message}")
    
    async def _calculate_overall_coherence(self, system_id: str) -> float:
        """Calculate overall coherence score for system"""
        
        if system_id not in self.coherence_metrics:
            return 0.0
        
        metrics = self.coherence_metrics[system_id]
        
        # Weighted average of coherence metrics
        weights = {
            CoherenceMetricType.SYSTEM_COHERENCE: 0.4,
            CoherenceMetricType.STATE_STABILITY: 0.3,
            CoherenceMetricType.ENTANGLEMENT_STRENGTH: 0.2,
            CoherenceMetricType.DECOHERENCE_RATE: -0.1  # Negative because lower is better
        }
        
        total_score = 0.0
        total_weight = 0.0
        
        for metric in metrics.values():
            weight = weights.get(metric.metric_type, 0.0)
            if weight != 0:
                if metric.metric_type == CoherenceMetricType.DECOHERENCE_RATE:
                    # For decoherence, invert the value (lower is better)
                    score = (1.0 - metric.current_value) * abs(weight)
                else:
                    score = metric.current_value * weight
                
                total_score += score
                total_weight += abs(weight)
        
        if total_weight > 0:
            return total_score / total_weight
        else:
            return 0.0
    
    def _calculate_coherence_grade(self, coherence: float) -> str:
        """Calculate coherence grade (A-F)"""
        
        if coherence >= 0.9:
            return "A"
        elif coherence >= 0.8:
            return "B"
        elif coherence >= 0.7:
            return "C"
        elif coherence >= 0.6:
            return "D"
        else:
            return "F"
    
    async def _generate_coherence_recommendations(
        self,
        system_id: str,
        overall_coherence: float,
        alerts: List[CoherenceAlert]
    ) -> List[str]:
        """Generate recommendations for improving coherence"""
        
        recommendations = []
        
        # General recommendations based on coherence level
        if overall_coherence < 0.5:
            recommendations.append("Critical: System coherence is very low. Consider immediate intervention.")
            recommendations.append("Review quantum state configurations and reduce decoherence sources.")
        elif overall_coherence < 0.7:
            recommendations.append("System coherence needs improvement. Focus on state stabilization.")
        
        # Specific recommendations based on alerts
        critical_alerts = [a for a in alerts if a.alert_level == CoherenceAlertLevel.CRITICAL]
        if critical_alerts:
            recommendations.append(f"Address {len(critical_alerts)} critical coherence issues immediately.")
        
        # Metric-specific recommendations
        if system_id in self.coherence_metrics:
            metrics = self.coherence_metrics[system_id]
            
            for metric in metrics.values():
                if metric.current_value < metric.threshold_warning:
                    if metric.metric_type == CoherenceMetricType.SYSTEM_COHERENCE:
                        recommendations.append("Improve system coherence by optimizing quantum state interactions.")
                    elif metric.metric_type == CoherenceMetricType.STATE_STABILITY:
                        recommendations.append("Stabilize quantum states by reducing external interference.")
                    elif metric.metric_type == CoherenceMetricType.ENTANGLEMENT_STRENGTH:
                        recommendations.append("Strengthen quantum entanglements between related states.")
                    elif metric.metric_type == CoherenceMetricType.DECOHERENCE_RATE:
                        recommendations.append("Reduce decoherence rate by improving environmental isolation.")
        
        return recommendations
    
    async def _determine_system_status(self, system_id: str) -> str:
        """Determine overall system status"""
        
        if system_id not in self.coherence_metrics:
            return "unknown"
        
        # Check for critical alerts
        critical_alerts = [
            alert for alert in self.active_alerts.values()
            if alert.system_id == system_id and 
               alert.alert_level in [CoherenceAlertLevel.CRITICAL, CoherenceAlertLevel.EMERGENCY] and
               not alert.resolved
        ]
        
        if critical_alerts:
            return "critical"
        
        # Check overall coherence
        overall_coherence = await self._calculate_overall_coherence(system_id)
        
        if overall_coherence >= 0.8:
            return "optimal"
        elif overall_coherence >= 0.6:
            return "good"
        elif overall_coherence >= 0.4:
            return "degraded"
        else:
            return "critical"
    
    async def _update_monitoring_stats(self) -> None:
        """Update monitoring statistics"""
        
        if self.monitored_systems:
            # Calculate average coherence across all systems
            coherences = []
            for system_id in self.monitored_systems:
                coherence = await self._calculate_overall_coherence(system_id)
                coherences.append(coherence)
            
            if coherences:
                self.monitoring_stats["average_coherence"] = np.mean(coherences)
        
        # Update uptime (simplified)
        self.monitoring_stats["uptime_percentage"] = 99.5  # Mock value
    
    async def _learn_from_monitoring(self) -> None:
        """Learn from monitoring data"""
        
        try:
            # Create learning experience from monitoring
            experience = LearningExperience(
                agent_id="coherence_monitor",
                experience_type=ExperienceType.COHERENCE_MONITORING,
                action_taken={
                    "action": "monitor_coherence",
                    "systems_count": len(self.monitored_systems),
                    "metrics_count": sum(len(metrics) for metrics in self.coherence_metrics.values())
                },
                outcome={
                    "average_coherence": self.monitoring_stats["average_coherence"],
                    "alerts_generated": len([a for a in self.active_alerts.values() if not a.resolved]),
                    "critical_incidents": self.monitoring_stats.get("critical_incidents", 0)
                },
                success=self.monitoring_stats["average_coherence"] > 0.6,
                confidence=0.8,
                context={
                    "monitoring_interval": self.monitoring_interval,
                    "total_measurements": self.monitoring_stats["total_measurements"]
                }
            )
            
            # Add to learning system
            await self.learning_system.learn_from_experience(experience)
            
        except Exception as e:
            self.logger.error(f"Failed to learn from monitoring: {e}")
    
    async def _cleanup_old_reports(self, system_id: str) -> None:
        """Cleanup old coherence reports"""
        
        if system_id not in self.coherence_history:
            return
        
        cutoff_date = datetime.now() - timedelta(days=self.history_retention_days)
        
        self.coherence_history[system_id] = [
            report for report in self.coherence_history[system_id]
            if report.timestamp > cutoff_date
        ] 