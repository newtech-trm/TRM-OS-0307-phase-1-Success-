"""
Performance Analyzer cho TRM-OS Phase 3

Advanced performance analytics với:
- Response time analysis
- Throughput monitoring
- Bottleneck detection
- Performance trend analysis
- Resource optimization recommendations
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import statistics
import json

logger = logging.getLogger(__name__)


class PerformanceLevel(Enum):
    """Performance levels"""
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    CRITICAL = "critical"


@dataclass
class PerformanceMetrics:
    """Performance metrics snapshot"""
    timestamp: datetime = field(default_factory=datetime.utcnow)
    
    # Response time metrics (milliseconds)
    avg_response_time: float = 0.0
    min_response_time: float = 0.0
    max_response_time: float = 0.0
    p50_response_time: float = 0.0
    p95_response_time: float = 0.0
    p99_response_time: float = 0.0
    
    # Throughput metrics
    requests_per_second: float = 0.0
    requests_per_minute: float = 0.0
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    
    # Error metrics
    error_rate: float = 0.0
    timeout_rate: float = 0.0
    
    # Resource utilization
    cpu_utilization: float = 0.0
    memory_utilization: float = 0.0
    disk_io_rate: float = 0.0
    network_io_rate: float = 0.0
    
    # Concurrency metrics
    active_connections: int = 0
    queue_length: int = 0
    thread_pool_utilization: float = 0.0
    
    # Performance level
    overall_performance: PerformanceLevel = PerformanceLevel.GOOD
    performance_score: float = 100.0


@dataclass
class RequestMetric:
    """Individual request metric"""
    timestamp: datetime
    endpoint: str
    method: str
    response_time: float
    status_code: int
    success: bool
    user_id: Optional[str] = None
    ip_address: Optional[str] = None


@dataclass
class BottleneckAlert:
    """Performance bottleneck alert"""
    timestamp: datetime
    type: str
    severity: str
    description: str
    affected_component: str
    recommended_action: str
    metrics: Dict[str, Any] = field(default_factory=dict)


class PerformanceAnalyzer:
    """Main performance analysis engine"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.is_analyzing = False
        
        # Metrics storage
        self.performance_history: List[PerformanceMetrics] = []
        self.request_metrics: List[RequestMetric] = []
        self.bottleneck_alerts: List[BottleneckAlert] = []
        
        # Configuration
        self.max_history = 1000
        self.max_requests = 10000
        self.analysis_interval = 30  # seconds
        
        # Performance thresholds
        self.response_time_thresholds = {
            'excellent': 100,    # < 100ms
            'good': 500,         # < 500ms
            'fair': 1000,        # < 1s
            'poor': 3000,        # < 3s
            'critical': float('inf')  # >= 3s
        }
        
        self.throughput_thresholds = {
            'excellent': 1000,   # > 1000 req/s
            'good': 500,         # > 500 req/s
            'fair': 100,         # > 100 req/s
            'poor': 10,          # > 10 req/s
            'critical': 0        # <= 10 req/s
        }
        
        # Analytics cache
        self.analytics_cache: Dict[str, Any] = {}
        self.cache_ttl = 60  # seconds
    
    async def start_analysis(self) -> None:
        """Start performance analysis"""
        try:
            if self.is_analyzing:
                self.logger.warning("Performance analysis already started")
                return
            
            self.is_analyzing = True
            self.logger.info("Starting performance analysis...")
            
            # Start analysis loop
            analysis_task = asyncio.create_task(self._analysis_loop())
            await analysis_task
            
        except Exception as e:
            self.logger.error(f"Failed to start performance analysis: {e}")
            self.is_analyzing = False
            raise
    
    async def stop_analysis(self) -> None:
        """Stop performance analysis"""
        self.is_analyzing = False
        self.logger.info("Performance analysis stopped")
    
    async def _analysis_loop(self) -> None:
        """Main analysis loop"""
        while self.is_analyzing:
            try:
                # Perform analysis
                await self._analyze_performance()
                
                # Check for bottlenecks
                await self._detect_bottlenecks()
                
                # Cleanup old data
                await self._cleanup_old_data()
                
                # Wait for next analysis
                await asyncio.sleep(self.analysis_interval)
                
            except Exception as e:
                self.logger.error(f"Analysis loop error: {e}")
                await asyncio.sleep(self.analysis_interval)
    
    async def record_request(self, endpoint: str, method: str, response_time: float,
                           status_code: int, user_id: str = None, ip_address: str = None) -> None:
        """Record individual request metric"""
        try:
            request_metric = RequestMetric(
                timestamp=datetime.utcnow(),
                endpoint=endpoint,
                method=method,
                response_time=response_time,
                status_code=status_code,
                success=200 <= status_code < 400,
                user_id=user_id,
                ip_address=ip_address
            )
            
            self.request_metrics.append(request_metric)
            
            # Maintain max requests limit
            if len(self.request_metrics) > self.max_requests:
                self.request_metrics = self.request_metrics[-self.max_requests:]
            
        except Exception as e:
            self.logger.error(f"Failed to record request metric: {e}")
    
    async def _analyze_performance(self) -> None:
        """Analyze current performance"""
        try:
            # Get recent requests (last 5 minutes)
            recent_requests = self._get_recent_requests(minutes=5)
            
            if not recent_requests:
                return
            
            # Calculate metrics
            metrics = PerformanceMetrics()
            
            # Response time analysis
            response_times = [r.response_time for r in recent_requests]
            if response_times:
                metrics.avg_response_time = statistics.mean(response_times)
                metrics.min_response_time = min(response_times)
                metrics.max_response_time = max(response_times)
                metrics.p50_response_time = statistics.median(response_times)
                
                # Calculate percentiles
                sorted_times = sorted(response_times)
                n = len(sorted_times)
                metrics.p95_response_time = sorted_times[int(0.95 * n)] if n > 0 else 0
                metrics.p99_response_time = sorted_times[int(0.99 * n)] if n > 0 else 0
            
            # Throughput analysis
            time_window = 300  # 5 minutes in seconds
            metrics.total_requests = len(recent_requests)
            metrics.requests_per_second = metrics.total_requests / time_window
            metrics.requests_per_minute = metrics.requests_per_second * 60
            
            # Success/error analysis
            successful = sum(1 for r in recent_requests if r.success)
            failed = metrics.total_requests - successful
            
            metrics.successful_requests = successful
            metrics.failed_requests = failed
            metrics.error_rate = (failed / metrics.total_requests) * 100 if metrics.total_requests > 0 else 0
            
            # Timeout analysis (assuming timeouts are > 30s)
            timeouts = sum(1 for r in recent_requests if r.response_time > 30000)
            metrics.timeout_rate = (timeouts / metrics.total_requests) * 100 if metrics.total_requests > 0 else 0
            
            # Calculate performance level and score
            metrics.overall_performance, metrics.performance_score = self._calculate_performance_level(metrics)
            
            # Store metrics
            self.performance_history.append(metrics)
            
            # Maintain history limit
            if len(self.performance_history) > self.max_history:
                self.performance_history = self.performance_history[-self.max_history:]
            
        except Exception as e:
            self.logger.error(f"Performance analysis failed: {e}")
    
    def _get_recent_requests(self, minutes: int = 5) -> List[RequestMetric]:
        """Get requests from last N minutes"""
        cutoff_time = datetime.utcnow() - timedelta(minutes=minutes)
        return [r for r in self.request_metrics if r.timestamp >= cutoff_time]
    
    def _calculate_performance_level(self, metrics: PerformanceMetrics) -> Tuple[PerformanceLevel, float]:
        """Calculate overall performance level and score"""
        try:
            scores = []
            
            # Response time score
            avg_time = metrics.avg_response_time
            if avg_time <= self.response_time_thresholds['excellent']:
                response_score = 100
            elif avg_time <= self.response_time_thresholds['good']:
                response_score = 80
            elif avg_time <= self.response_time_thresholds['fair']:
                response_score = 60
            elif avg_time <= self.response_time_thresholds['poor']:
                response_score = 40
            else:
                response_score = 20
            scores.append(response_score)
            
            # Throughput score
            rps = metrics.requests_per_second
            if rps >= self.throughput_thresholds['excellent']:
                throughput_score = 100
            elif rps >= self.throughput_thresholds['good']:
                throughput_score = 80
            elif rps >= self.throughput_thresholds['fair']:
                throughput_score = 60
            elif rps >= self.throughput_thresholds['poor']:
                throughput_score = 40
            else:
                throughput_score = 20
            scores.append(throughput_score)
            
            # Error rate score
            error_rate = metrics.error_rate
            if error_rate <= 1:
                error_score = 100
            elif error_rate <= 5:
                error_score = 80
            elif error_rate <= 10:
                error_score = 60
            elif error_rate <= 20:
                error_score = 40
            else:
                error_score = 20
            scores.append(error_score)
            
            # Calculate overall score
            overall_score = sum(scores) / len(scores)
            
            # Determine performance level
            if overall_score >= 90:
                level = PerformanceLevel.EXCELLENT
            elif overall_score >= 70:
                level = PerformanceLevel.GOOD
            elif overall_score >= 50:
                level = PerformanceLevel.FAIR
            elif overall_score >= 30:
                level = PerformanceLevel.POOR
            else:
                level = PerformanceLevel.CRITICAL
            
            return level, overall_score
            
        except Exception as e:
            self.logger.error(f"Performance level calculation failed: {e}")
            return PerformanceLevel.CRITICAL, 0.0
    
    async def _detect_bottlenecks(self) -> None:
        """Detect performance bottlenecks"""
        try:
            current_metrics = self.get_current_metrics()
            if not current_metrics:
                return
            
            alerts = []
            
            # High response time bottleneck
            if current_metrics.avg_response_time > 2000:  # > 2 seconds
                alerts.append(BottleneckAlert(
                    timestamp=datetime.utcnow(),
                    type="high_response_time",
                    severity="high",
                    description=f"Average response time is {current_metrics.avg_response_time:.0f}ms",
                    affected_component="application",
                    recommended_action="Optimize slow endpoints, add caching, or scale resources",
                    metrics={"avg_response_time": current_metrics.avg_response_time}
                ))
            
            # High error rate bottleneck
            if current_metrics.error_rate > 10:  # > 10%
                alerts.append(BottleneckAlert(
                    timestamp=datetime.utcnow(),
                    type="high_error_rate",
                    severity="high",
                    description=f"Error rate is {current_metrics.error_rate:.1f}%",
                    affected_component="application",
                    recommended_action="Investigate failing endpoints and fix underlying issues",
                    metrics={"error_rate": current_metrics.error_rate}
                ))
            
            # Low throughput bottleneck
            if current_metrics.requests_per_second < 10:  # < 10 req/s
                alerts.append(BottleneckAlert(
                    timestamp=datetime.utcnow(),
                    type="low_throughput",
                    severity="medium",
                    description=f"Throughput is only {current_metrics.requests_per_second:.1f} req/s",
                    affected_component="system",
                    recommended_action="Check for resource constraints or scaling issues",
                    metrics={"requests_per_second": current_metrics.requests_per_second}
                ))
            
            # Store alerts
            self.bottleneck_alerts.extend(alerts)
            
            # Log new alerts
            for alert in alerts:
                self.logger.warning(f"Bottleneck detected: {alert.type} - {alert.description}")
            
        except Exception as e:
            self.logger.error(f"Bottleneck detection failed: {e}")
    
    async def _cleanup_old_data(self) -> None:
        """Cleanup old performance data"""
        try:
            # Remove old bottleneck alerts (keep last 24 hours)
            cutoff_time = datetime.utcnow() - timedelta(hours=24)
            self.bottleneck_alerts = [
                alert for alert in self.bottleneck_alerts
                if alert.timestamp >= cutoff_time
            ]
            
            # Clear analytics cache
            self.analytics_cache.clear()
            
        except Exception as e:
            self.logger.error(f"Cleanup failed: {e}")
    
    def get_current_metrics(self) -> Optional[PerformanceMetrics]:
        """Get latest performance metrics"""
        return self.performance_history[-1] if self.performance_history else None
    
    def get_performance_history(self, hours: int = 24) -> List[PerformanceMetrics]:
        """Get performance history for specified time period"""
        if not self.performance_history:
            return []
        
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        
        return [
            metrics for metrics in self.performance_history
            if metrics.timestamp >= cutoff_time
        ]
    
    async def get_endpoint_performance(self, endpoint: str = None, hours: int = 24) -> Dict[str, Any]:
        """Get performance analysis for specific endpoint"""
        try:
            # Get recent requests
            cutoff_time = datetime.utcnow() - timedelta(hours=hours)
            recent_requests = [
                r for r in self.request_metrics
                if r.timestamp >= cutoff_time and (endpoint is None or r.endpoint == endpoint)
            ]
            
            if not recent_requests:
                return {'error': 'No data available for the specified period'}
            
            # Group by endpoint if no specific endpoint requested
            if endpoint is None:
                endpoint_stats = {}
                for request in recent_requests:
                    ep = request.endpoint
                    if ep not in endpoint_stats:
                        endpoint_stats[ep] = []
                    endpoint_stats[ep].append(request)
                
                results = {}
                for ep, requests in endpoint_stats.items():
                    results[ep] = self._calculate_endpoint_stats(requests)
                
                return results
            else:
                return {endpoint: self._calculate_endpoint_stats(recent_requests)}
            
        except Exception as e:
            self.logger.error(f"Endpoint performance analysis failed: {e}")
            return {'error': str(e)}
    
    def _calculate_endpoint_stats(self, requests: List[RequestMetric]) -> Dict[str, Any]:
        """Calculate statistics for endpoint requests"""
        if not requests:
            return {}
        
        response_times = [r.response_time for r in requests]
        successful = sum(1 for r in requests if r.success)
        
        return {
            'total_requests': len(requests),
            'successful_requests': successful,
            'error_rate': ((len(requests) - successful) / len(requests)) * 100,
            'avg_response_time': statistics.mean(response_times),
            'min_response_time': min(response_times),
            'max_response_time': max(response_times),
            'median_response_time': statistics.median(response_times),
            'requests_per_hour': len(requests),  # Assuming 1 hour period
            'last_request': max(r.timestamp for r in requests).isoformat()
        }
    
    async def get_performance_trends(self, hours: int = 24) -> Dict[str, Any]:
        """Get performance trends analysis"""
        try:
            cache_key = f"trends_{hours}"
            
            # Check cache
            if cache_key in self.analytics_cache:
                cached_time, cached_data = self.analytics_cache[cache_key]
                if (datetime.utcnow() - cached_time).seconds < self.cache_ttl:
                    return cached_data
            
            # Get historical data
            history = self.get_performance_history(hours)
            
            if len(history) < 2:
                return {'error': 'Insufficient data for trend analysis'}
            
            # Calculate trends
            response_times = [m.avg_response_time for m in history]
            throughputs = [m.requests_per_second for m in history]
            error_rates = [m.error_rate for m in history]
            
            trends = {
                'response_time_trend': self._calculate_trend(response_times),
                'throughput_trend': self._calculate_trend(throughputs),
                'error_rate_trend': self._calculate_trend(error_rates),
                'performance_score_trend': self._calculate_trend([m.performance_score for m in history]),
                'data_points': len(history),
                'time_period_hours': hours,
                'last_updated': datetime.utcnow().isoformat()
            }
            
            # Cache results
            self.analytics_cache[cache_key] = (datetime.utcnow(), trends)
            
            return trends
            
        except Exception as e:
            self.logger.error(f"Performance trends analysis failed: {e}")
            return {'error': str(e)}
    
    def _calculate_trend(self, values: List[float]) -> Dict[str, Any]:
        """Calculate trend for a series of values"""
        if len(values) < 2:
            return {'direction': 'stable', 'change_percent': 0.0}
        
        # Simple trend calculation
        first_half = values[:len(values)//2]
        second_half = values[len(values)//2:]
        
        first_avg = statistics.mean(first_half)
        second_avg = statistics.mean(second_half)
        
        if first_avg == 0:
            change_percent = 0.0
        else:
            change_percent = ((second_avg - first_avg) / first_avg) * 100
        
        # Determine direction
        if abs(change_percent) < 5:
            direction = 'stable'
        elif change_percent > 0:
            direction = 'increasing'
        else:
            direction = 'decreasing'
        
        return {
            'direction': direction,
            'change_percent': change_percent,
            'first_period_avg': first_avg,
            'second_period_avg': second_avg
        }
    
    async def get_bottleneck_alerts(self, hours: int = 24) -> List[Dict[str, Any]]:
        """Get recent bottleneck alerts"""
        try:
            cutoff_time = datetime.utcnow() - timedelta(hours=hours)
            
            recent_alerts = [
                alert for alert in self.bottleneck_alerts
                if alert.timestamp >= cutoff_time
            ]
            
            return [
                {
                    'timestamp': alert.timestamp.isoformat(),
                    'type': alert.type,
                    'severity': alert.severity,
                    'description': alert.description,
                    'affected_component': alert.affected_component,
                    'recommended_action': alert.recommended_action,
                    'metrics': alert.metrics
                }
                for alert in recent_alerts
            ]
            
        except Exception as e:
            self.logger.error(f"Failed to get bottleneck alerts: {e}")
            return []
    
    async def generate_performance_report(self) -> Dict[str, Any]:
        """Generate comprehensive performance report"""
        try:
            current_metrics = self.get_current_metrics()
            if not current_metrics:
                return {'error': 'No performance data available'}
            
            # Get trends
            trends = await self.get_performance_trends(24)
            
            # Get bottlenecks
            bottlenecks = await self.get_bottleneck_alerts(24)
            
            # Get top endpoints
            endpoint_performance = await self.get_endpoint_performance(hours=24)
            
            return {
                'timestamp': datetime.utcnow().isoformat(),
                'current_performance': {
                    'level': current_metrics.overall_performance.value,
                    'score': current_metrics.performance_score,
                    'avg_response_time': current_metrics.avg_response_time,
                    'requests_per_second': current_metrics.requests_per_second,
                    'error_rate': current_metrics.error_rate,
                    'p95_response_time': current_metrics.p95_response_time
                },
                'trends': trends,
                'bottlenecks': bottlenecks,
                'endpoint_performance': endpoint_performance,
                'recommendations': self._generate_performance_recommendations(current_metrics, bottlenecks)
            }
            
        except Exception as e:
            self.logger.error(f"Performance report generation failed: {e}")
            return {'error': str(e)}
    
    def _generate_performance_recommendations(self, metrics: PerformanceMetrics, 
                                            bottlenecks: List[Dict[str, Any]]) -> List[str]:
        """Generate performance optimization recommendations"""
        recommendations = []
        
        # Response time recommendations
        if metrics.avg_response_time > 1000:
            recommendations.append("Consider implementing caching to reduce response times")
            recommendations.append("Optimize database queries and add appropriate indexes")
        
        # Throughput recommendations
        if metrics.requests_per_second < 50:
            recommendations.append("Consider horizontal scaling to increase throughput")
            recommendations.append("Optimize application code for better concurrency")
        
        # Error rate recommendations
        if metrics.error_rate > 5:
            recommendations.append("Investigate and fix sources of errors")
            recommendations.append("Implement better error handling and retry mechanisms")
        
        # Bottleneck-specific recommendations
        if bottlenecks:
            recommendations.append("Address identified bottlenecks as high priority")
        
        if not recommendations:
            recommendations.append("Performance is good. Continue monitoring for any changes.")
        
        return recommendations 