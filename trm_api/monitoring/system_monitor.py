"""
System Monitor cho TRM-OS Phase 3

Real-time system monitoring với:
- CPU, Memory, Disk, Network metrics
- Process monitoring
- Service health checks
- Resource utilization tracking
- Performance bottleneck detection
"""

import asyncio
import logging
import psutil
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import json

logger = logging.getLogger(__name__)


class HealthStatus(Enum):
    """System health status levels"""
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"
    DOWN = "down"


@dataclass
class SystemMetrics:
    """System metrics snapshot"""
    timestamp: datetime = field(default_factory=datetime.utcnow)
    
    # CPU metrics
    cpu_percent: float = 0.0
    cpu_count: int = 0
    cpu_freq: float = 0.0
    load_average: List[float] = field(default_factory=list)
    
    # Memory metrics
    memory_total: int = 0
    memory_available: int = 0
    memory_used: int = 0
    memory_percent: float = 0.0
    swap_total: int = 0
    swap_used: int = 0
    swap_percent: float = 0.0
    
    # Disk metrics
    disk_usage: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    disk_io: Dict[str, Any] = field(default_factory=dict)
    
    # Network metrics
    network_io: Dict[str, Any] = field(default_factory=dict)
    network_connections: int = 0
    
    # Process metrics
    process_count: int = 0
    thread_count: int = 0
    
    # System info
    boot_time: datetime = field(default_factory=datetime.utcnow)
    uptime_seconds: float = 0.0
    
    # Health status
    overall_health: HealthStatus = HealthStatus.HEALTHY
    health_score: float = 100.0


@dataclass
class ProcessInfo:
    """Process information"""
    pid: int
    name: str
    cpu_percent: float
    memory_percent: float
    memory_rss: int
    status: str
    create_time: datetime
    num_threads: int


class SystemMonitor:
    """Main system monitoring class"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.is_monitoring = False
        self.metrics_history: List[SystemMetrics] = []
        self.max_history = 1000  # Keep last 1000 metrics
        
        # Monitoring intervals
        self.collection_interval = 5  # seconds
        self.cleanup_interval = 300  # 5 minutes
        
        # Health thresholds
        self.cpu_warning_threshold = 80.0
        self.cpu_critical_threshold = 95.0
        self.memory_warning_threshold = 80.0
        self.memory_critical_threshold = 95.0
        self.disk_warning_threshold = 80.0
        self.disk_critical_threshold = 95.0
        
        # Performance tracking
        self.performance_stats = {
            'total_collections': 0,
            'average_collection_time': 0.0,
            'last_collection_time': None
        }
    
    async def start_monitoring(self) -> None:
        """Start system monitoring"""
        try:
            if self.is_monitoring:
                self.logger.warning("Monitoring already started")
                return
            
            self.is_monitoring = True
            self.logger.info("Starting system monitoring...")
            
            # Start monitoring tasks
            monitoring_task = asyncio.create_task(self._monitoring_loop())
            cleanup_task = asyncio.create_task(self._cleanup_loop())
            
            # Wait for tasks
            await asyncio.gather(monitoring_task, cleanup_task)
            
        except Exception as e:
            self.logger.error(f"Failed to start monitoring: {e}")
            self.is_monitoring = False
            raise
    
    async def stop_monitoring(self) -> None:
        """Stop system monitoring"""
        self.is_monitoring = False
        self.logger.info("System monitoring stopped")
    
    async def _monitoring_loop(self) -> None:
        """Main monitoring loop"""
        while self.is_monitoring:
            try:
                start_time = time.time()
                
                # Collect system metrics
                metrics = await self.collect_system_metrics()
                
                # Store metrics
                self.metrics_history.append(metrics)
                
                # Update performance stats
                collection_time = time.time() - start_time
                self._update_performance_stats(collection_time)
                
                # Log health status changes
                if len(self.metrics_history) > 1:
                    prev_health = self.metrics_history[-2].overall_health
                    if metrics.overall_health != prev_health:
                        self.logger.warning(f"Health status changed: {prev_health.value} -> {metrics.overall_health.value}")
                
                # Wait for next collection
                await asyncio.sleep(self.collection_interval)
                
            except Exception as e:
                self.logger.error(f"Monitoring loop error: {e}")
                await asyncio.sleep(self.collection_interval)
    
    async def _cleanup_loop(self) -> None:
        """Cleanup old metrics"""
        while self.is_monitoring:
            try:
                # Remove old metrics
                if len(self.metrics_history) > self.max_history:
                    self.metrics_history = self.metrics_history[-self.max_history:]
                
                await asyncio.sleep(self.cleanup_interval)
                
            except Exception as e:
                self.logger.error(f"Cleanup loop error: {e}")
                await asyncio.sleep(self.cleanup_interval)
    
    async def collect_system_metrics(self) -> SystemMetrics:
        """Collect current system metrics"""
        try:
            metrics = SystemMetrics()
            
            # CPU metrics
            metrics.cpu_percent = psutil.cpu_percent(interval=1)
            metrics.cpu_count = psutil.cpu_count()
            
            try:
                cpu_freq = psutil.cpu_freq()
                metrics.cpu_freq = cpu_freq.current if cpu_freq else 0.0
            except:
                metrics.cpu_freq = 0.0
            
            try:
                metrics.load_average = list(psutil.getloadavg())
            except AttributeError:
                # Windows doesn't have getloadavg
                metrics.load_average = [0.0, 0.0, 0.0]
            
            # Memory metrics
            memory = psutil.virtual_memory()
            metrics.memory_total = memory.total
            metrics.memory_available = memory.available
            metrics.memory_used = memory.used
            metrics.memory_percent = memory.percent
            
            swap = psutil.swap_memory()
            metrics.swap_total = swap.total
            metrics.swap_used = swap.used
            metrics.swap_percent = swap.percent
            
            # Disk metrics
            metrics.disk_usage = {}
            for partition in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    metrics.disk_usage[partition.device] = {
                        'total': usage.total,
                        'used': usage.used,
                        'free': usage.free,
                        'percent': (usage.used / usage.total) * 100 if usage.total > 0 else 0
                    }
                except PermissionError:
                    continue
            
            # Disk I/O
            try:
                disk_io = psutil.disk_io_counters()
                if disk_io:
                    metrics.disk_io = {
                        'read_count': disk_io.read_count,
                        'write_count': disk_io.write_count,
                        'read_bytes': disk_io.read_bytes,
                        'write_bytes': disk_io.write_bytes
                    }
            except:
                metrics.disk_io = {}
            
            # Network metrics
            try:
                network_io = psutil.net_io_counters()
                if network_io:
                    metrics.network_io = {
                        'bytes_sent': network_io.bytes_sent,
                        'bytes_recv': network_io.bytes_recv,
                        'packets_sent': network_io.packets_sent,
                        'packets_recv': network_io.packets_recv
                    }
                
                metrics.network_connections = len(psutil.net_connections())
            except:
                metrics.network_io = {}
                metrics.network_connections = 0
            
            # Process metrics
            metrics.process_count = len(psutil.pids())
            
            total_threads = 0
            for proc in psutil.process_iter(['num_threads']):
                try:
                    total_threads += proc.info['num_threads'] or 0
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            metrics.thread_count = total_threads
            
            # System info
            metrics.boot_time = datetime.fromtimestamp(psutil.boot_time())
            metrics.uptime_seconds = time.time() - psutil.boot_time()
            
            # Calculate health status
            metrics.overall_health, metrics.health_score = self._calculate_health_status(metrics)
            
            return metrics
            
        except Exception as e:
            self.logger.error(f"Failed to collect system metrics: {e}")
            # Return empty metrics with error status
            metrics = SystemMetrics()
            metrics.overall_health = HealthStatus.DOWN
            metrics.health_score = 0.0
            return metrics
    
    def _calculate_health_status(self, metrics: SystemMetrics) -> tuple[HealthStatus, float]:
        """Calculate overall health status"""
        try:
            health_factors = []
            
            # CPU health
            if metrics.cpu_percent >= self.cpu_critical_threshold:
                cpu_health = 0.0
            elif metrics.cpu_percent >= self.cpu_warning_threshold:
                cpu_health = 0.5
            else:
                cpu_health = 1.0
            health_factors.append(cpu_health)
            
            # Memory health
            if metrics.memory_percent >= self.memory_critical_threshold:
                memory_health = 0.0
            elif metrics.memory_percent >= self.memory_warning_threshold:
                memory_health = 0.5
            else:
                memory_health = 1.0
            health_factors.append(memory_health)
            
            # Disk health (average across all disks)
            disk_healths = []
            for device, usage in metrics.disk_usage.items():
                disk_percent = usage['percent']
                if disk_percent >= self.disk_critical_threshold:
                    disk_healths.append(0.0)
                elif disk_percent >= self.disk_warning_threshold:
                    disk_healths.append(0.5)
                else:
                    disk_healths.append(1.0)
            
            if disk_healths:
                disk_health = sum(disk_healths) / len(disk_healths)
                health_factors.append(disk_health)
            
            # Calculate overall health score
            health_score = (sum(health_factors) / len(health_factors)) * 100 if health_factors else 0.0
            
            # Determine status
            if health_score >= 80:
                status = HealthStatus.HEALTHY
            elif health_score >= 50:
                status = HealthStatus.WARNING
            elif health_score > 0:
                status = HealthStatus.CRITICAL
            else:
                status = HealthStatus.DOWN
            
            return status, health_score
            
        except Exception as e:
            self.logger.error(f"Health calculation failed: {e}")
            return HealthStatus.DOWN, 0.0
    
    def _update_performance_stats(self, collection_time: float) -> None:
        """Update performance statistics"""
        self.performance_stats['total_collections'] += 1
        self.performance_stats['last_collection_time'] = datetime.utcnow()
        
        # Update rolling average
        total = self.performance_stats['total_collections']
        current_avg = self.performance_stats['average_collection_time']
        self.performance_stats['average_collection_time'] = (
            (current_avg * (total - 1) + collection_time) / total
        )
    
    def get_current_metrics(self) -> Optional[SystemMetrics]:
        """Get latest system metrics"""
        return self.metrics_history[-1] if self.metrics_history else None
    
    def get_metrics_history(self, minutes: int = 60) -> List[SystemMetrics]:
        """Get metrics history for specified time period"""
        if not self.metrics_history:
            return []
        
        cutoff_time = datetime.utcnow() - timedelta(minutes=minutes)
        
        return [
            metrics for metrics in self.metrics_history
            if metrics.timestamp >= cutoff_time
        ]
    
    def get_health_summary(self) -> Dict[str, Any]:
        """Get system health summary"""
        current_metrics = self.get_current_metrics()
        
        if not current_metrics:
            return {
                'status': HealthStatus.DOWN.value,
                'score': 0.0,
                'message': 'No metrics available'
            }
        
        # Get recent trends
        recent_metrics = self.get_metrics_history(30)  # Last 30 minutes
        
        if len(recent_metrics) > 1:
            # Calculate trends
            cpu_trend = self._calculate_trend([m.cpu_percent for m in recent_metrics])
            memory_trend = self._calculate_trend([m.memory_percent for m in recent_metrics])
        else:
            cpu_trend = 0.0
            memory_trend = 0.0
        
        return {
            'status': current_metrics.overall_health.value,
            'score': current_metrics.health_score,
            'cpu_percent': current_metrics.cpu_percent,
            'memory_percent': current_metrics.memory_percent,
            'disk_usage': current_metrics.disk_usage,
            'uptime_hours': current_metrics.uptime_seconds / 3600,
            'trends': {
                'cpu': cpu_trend,
                'memory': memory_trend
            },
            'last_updated': current_metrics.timestamp.isoformat(),
            'monitoring_stats': self.performance_stats
        }
    
    def _calculate_trend(self, values: List[float]) -> float:
        """Calculate trend direction (-1 to 1)"""
        if len(values) < 2:
            return 0.0
        
        # Simple linear trend calculation
        n = len(values)
        x_sum = sum(range(n))
        y_sum = sum(values)
        xy_sum = sum(i * values[i] for i in range(n))
        x2_sum = sum(i * i for i in range(n))
        
        # Calculate slope
        denominator = n * x2_sum - x_sum * x_sum
        if denominator == 0:
            return 0.0
        
        slope = (n * xy_sum - x_sum * y_sum) / denominator
        
        # Normalize to -1 to 1 range
        max_value = max(values) if values else 1
        normalized_slope = slope / max_value if max_value > 0 else 0
        
        return max(-1.0, min(1.0, normalized_slope))
    
    async def get_top_processes(self, limit: int = 10) -> List[ProcessInfo]:
        """Get top processes by CPU usage"""
        try:
            processes = []
            
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 
                                           'memory_info', 'status', 'create_time', 'num_threads']):
                try:
                    pinfo = ProcessInfo(
                        pid=proc.info['pid'],
                        name=proc.info['name'],
                        cpu_percent=proc.info['cpu_percent'] or 0.0,
                        memory_percent=proc.info['memory_percent'] or 0.0,
                        memory_rss=proc.info['memory_info'].rss if proc.info['memory_info'] else 0,
                        status=proc.info['status'],
                        create_time=datetime.fromtimestamp(proc.info['create_time']),
                        num_threads=proc.info['num_threads'] or 0
                    )
                    processes.append(pinfo)
                    
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            # Sort by CPU usage
            processes.sort(key=lambda x: x.cpu_percent, reverse=True)
            
            return processes[:limit]
            
        except Exception as e:
            self.logger.error(f"Failed to get top processes: {e}")
            return []
    
    async def check_service_health(self, service_name: str) -> Dict[str, Any]:
        """Check health of specific service"""
        try:
            # Find process by name
            for proc in psutil.process_iter(['pid', 'name', 'status', 'cpu_percent', 'memory_percent']):
                try:
                    if service_name.lower() in proc.info['name'].lower():
                        return {
                            'service': service_name,
                            'status': 'running',
                            'pid': proc.info['pid'],
                            'cpu_percent': proc.info['cpu_percent'],
                            'memory_percent': proc.info['memory_percent'],
                            'process_status': proc.info['status']
                        }
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            return {
                'service': service_name,
                'status': 'not_found',
                'message': f'Service {service_name} not found'
            }
            
        except Exception as e:
            self.logger.error(f"Service health check failed: {e}")
            return {
                'service': service_name,
                'status': 'error',
                'error': str(e)
            }
    
    async def generate_health_report(self) -> Dict[str, Any]:
        """Generate comprehensive health report"""
        try:
            current_metrics = self.get_current_metrics()
            if not current_metrics:
                return {'error': 'No metrics available'}
            
            # Get top processes
            top_processes = await self.get_top_processes(5)
            
            # Get health summary
            health_summary = self.get_health_summary()
            
            # Generate recommendations
            recommendations = self._generate_recommendations(current_metrics)
            
            return {
                'timestamp': datetime.utcnow().isoformat(),
                'health_summary': health_summary,
                'system_metrics': {
                    'cpu': {
                        'percent': current_metrics.cpu_percent,
                        'count': current_metrics.cpu_count,
                        'frequency': current_metrics.cpu_freq
                    },
                    'memory': {
                        'total_gb': current_metrics.memory_total / (1024**3),
                        'used_gb': current_metrics.memory_used / (1024**3),
                        'percent': current_metrics.memory_percent
                    },
                    'disk': current_metrics.disk_usage,
                    'network': current_metrics.network_io,
                    'processes': current_metrics.process_count,
                    'uptime_hours': current_metrics.uptime_seconds / 3600
                },
                'top_processes': [
                    {
                        'name': p.name,
                        'pid': p.pid,
                        'cpu_percent': p.cpu_percent,
                        'memory_percent': p.memory_percent
                    } for p in top_processes
                ],
                'recommendations': recommendations
            }
            
        except Exception as e:
            self.logger.error(f"Health report generation failed: {e}")
            return {'error': str(e)}
    
    def _generate_recommendations(self, metrics: SystemMetrics) -> List[str]:
        """Generate performance recommendations"""
        recommendations = []
        
        # CPU recommendations
        if metrics.cpu_percent > self.cpu_critical_threshold:
            recommendations.append("Critical: CPU usage is very high. Consider scaling or optimizing workloads.")
        elif metrics.cpu_percent > self.cpu_warning_threshold:
            recommendations.append("Warning: CPU usage is elevated. Monitor for performance issues.")
        
        # Memory recommendations
        if metrics.memory_percent > self.memory_critical_threshold:
            recommendations.append("Critical: Memory usage is very high. Consider adding more RAM or optimizing memory usage.")
        elif metrics.memory_percent > self.memory_warning_threshold:
            recommendations.append("Warning: Memory usage is elevated. Monitor for memory leaks.")
        
        # Disk recommendations
        for device, usage in metrics.disk_usage.items():
            if usage['percent'] > self.disk_critical_threshold:
                recommendations.append(f"Critical: Disk {device} is almost full ({usage['percent']:.1f}%). Clean up or expand storage.")
            elif usage['percent'] > self.disk_warning_threshold:
                recommendations.append(f"Warning: Disk {device} usage is high ({usage['percent']:.1f}%).")
        
        # Process recommendations
        if metrics.process_count > 1000:
            recommendations.append("High number of processes detected. Consider reviewing running services.")
        
        if not recommendations:
            recommendations.append("System is running optimally. No immediate actions required.")
        
        return recommendations 