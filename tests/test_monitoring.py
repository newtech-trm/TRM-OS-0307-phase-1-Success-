"""
Tests for TRM-OS Monitoring System
"""

import pytest
import asyncio
import logging
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, AsyncMock

from trm_api.monitoring.system_monitor import SystemMonitor, SystemMetrics, HealthStatus
from trm_api.monitoring.performance_analyzer import PerformanceAnalyzer, PerformanceMetrics, PerformanceLevel
from trm_api.monitoring.alerting_system import AlertingSystem, AlertRule, Alert, AlertSeverity, NotificationChannel
from trm_api.monitoring.dashboard_engine import DashboardEngine, DashboardLayout, ChartConfig, ChartType, TimeRange


class TestSystemMonitor:
    """Test SystemMonitor functionality"""
    
    @pytest.fixture
    def system_monitor(self):
        return SystemMonitor()
    
    @pytest.mark.asyncio
    async def test_system_monitor_initialization(self, system_monitor):
        """Test system monitor initialization"""
        assert system_monitor is not None
        assert system_monitor.is_monitoring == False
        assert system_monitor.metrics_history == []
        assert system_monitor.health_checks == {}
    
    @pytest.mark.asyncio
    async def test_collect_system_metrics(self, system_monitor):
        """Test system metrics collection"""
        # Mock system calls
        with patch('psutil.cpu_percent', return_value=50.0), \
             patch('psutil.virtual_memory') as mock_memory, \
             patch('psutil.disk_usage') as mock_disk:
            
            # Setup mocks
            mock_memory.return_value = Mock(percent=60.0, available=4000000000, used=6000000000, total=10000000000)
            mock_disk.return_value = Mock(percent=70.0, free=300000000000, used=700000000000, total=1000000000000)
            
            # Collect metrics
            metrics = await system_monitor._collect_system_metrics()
            
            # Verify metrics
            assert isinstance(metrics, SystemMetrics)
            assert metrics.cpu_usage == 50.0
            assert metrics.memory_usage == 60.0
            assert metrics.disk_usage == 70.0
            assert metrics.memory_available > 0
            assert metrics.disk_free > 0
    
    @pytest.mark.asyncio
    async def test_health_status_calculation(self, system_monitor):
        """Test health status calculation"""
        # Test healthy system
        metrics = SystemMetrics(
            cpu_usage=30.0,
            memory_usage=40.0,
            disk_usage=50.0,
            memory_available=6000000000,
            disk_free=500000000000
        )
        
        health_status = system_monitor._calculate_health_status(metrics)
        assert health_status == HealthStatus.HEALTHY
        
        # Test degraded system
        metrics.cpu_usage = 85.0
        health_status = system_monitor._calculate_health_status(metrics)
        assert health_status == HealthStatus.DEGRADED
        
        # Test unhealthy system
        metrics.memory_usage = 95.0
        health_status = system_monitor._calculate_health_status(metrics)
        assert health_status == HealthStatus.UNHEALTHY
    
    @pytest.mark.asyncio
    async def test_register_health_check(self, system_monitor):
        """Test health check registration"""
        # Mock health check function
        async def mock_health_check():
            return True, "Service is healthy"
        
        # Register health check
        system_monitor.register_health_check("test_service", mock_health_check)
        
        # Verify registration
        assert "test_service" in system_monitor.health_checks
        assert system_monitor.health_checks["test_service"] == mock_health_check
    
    @pytest.mark.asyncio
    async def test_get_current_metrics(self, system_monitor):
        """Test getting current metrics"""
        # Add some metrics to history
        metrics = SystemMetrics(cpu_usage=50.0, memory_usage=60.0, disk_usage=70.0)
        system_monitor.metrics_history.append(metrics)
        
        # Get current metrics
        current = system_monitor.get_current_metrics()
        
        # Verify
        assert current is not None
        assert current.cpu_usage == 50.0
        assert current.memory_usage == 60.0
        assert current.disk_usage == 70.0
    
    @pytest.mark.asyncio
    async def test_get_metrics_history(self, system_monitor):
        """Test getting metrics history"""
        # Add metrics with different timestamps
        now = datetime.utcnow()
        
        for i in range(5):
            metrics = SystemMetrics(
                timestamp=now - timedelta(hours=i),
                cpu_usage=50.0 + i,
                memory_usage=60.0 + i,
                disk_usage=70.0 + i
            )
            system_monitor.metrics_history.append(metrics)
        
        # Get last 3 hours
        history = system_monitor.get_metrics_history(hours=3)
        
        # Verify
        assert len(history) == 4  # 0, 1, 2, 3 hours ago
        assert all(m.timestamp >= now - timedelta(hours=3) for m in history)


class TestPerformanceAnalyzer:
    """Test PerformanceAnalyzer functionality"""
    
    @pytest.fixture
    def performance_analyzer(self):
        return PerformanceAnalyzer()
    
    @pytest.mark.asyncio
    async def test_performance_analyzer_initialization(self, performance_analyzer):
        """Test performance analyzer initialization"""
        assert performance_analyzer is not None
        assert performance_analyzer.is_analyzing == False
        assert performance_analyzer.performance_history == []
        assert performance_analyzer.request_metrics == []
    
    @pytest.mark.asyncio
    async def test_record_request(self, performance_analyzer):
        """Test recording request metrics"""
        # Record a request
        await performance_analyzer.record_request(
            endpoint="/api/test",
            method="GET",
            response_time=150.0,
            status_code=200,
            user_id="user123"
        )
        
        # Verify request was recorded
        assert len(performance_analyzer.request_metrics) == 1
        
        request = performance_analyzer.request_metrics[0]
        assert request.endpoint == "/api/test"
        assert request.method == "GET"
        assert request.response_time == 150.0
        assert request.status_code == 200
        assert request.success == True
        assert request.user_id == "user123"
    
    @pytest.mark.asyncio
    async def test_performance_level_calculation(self, performance_analyzer):
        """Test performance level calculation"""
        # Test excellent performance
        metrics = PerformanceMetrics(
            avg_response_time=50.0,
            requests_per_second=1500.0,
            error_rate=0.5
        )
        
        level, score = performance_analyzer._calculate_performance_level(metrics)
        assert level == PerformanceLevel.EXCELLENT
        assert score >= 90
        
        # Test poor performance
        metrics = PerformanceMetrics(
            avg_response_time=5000.0,
            requests_per_second=5.0,
            error_rate=25.0
        )
        
        level, score = performance_analyzer._calculate_performance_level(metrics)
        assert level == PerformanceLevel.CRITICAL
        assert score < 30
    
    @pytest.mark.asyncio
    async def test_endpoint_performance_analysis(self, performance_analyzer):
        """Test endpoint performance analysis"""
        # Add some request metrics
        endpoints = ["/api/users", "/api/orders", "/api/products"]
        
        for i, endpoint in enumerate(endpoints):
            for j in range(10):
                await performance_analyzer.record_request(
                    endpoint=endpoint,
                    method="GET",
                    response_time=100.0 + (i * 50) + (j * 10),
                    status_code=200 if j < 9 else 500
                )
        
        # Analyze endpoint performance
        analysis = await performance_analyzer.get_endpoint_performance(hours=1)
        
        # Verify analysis
        assert isinstance(analysis, dict)
        assert len(analysis) == 3
        
        for endpoint in endpoints:
            assert endpoint in analysis
            stats = analysis[endpoint]
            assert stats['total_requests'] == 10
            assert stats['successful_requests'] == 9
            assert stats['error_rate'] == 10.0
    
    @pytest.mark.asyncio
    async def test_performance_trends(self, performance_analyzer):
        """Test performance trends analysis"""
        # Add historical performance data
        now = datetime.utcnow()
        
        for i in range(10):
            metrics = PerformanceMetrics(
                timestamp=now - timedelta(hours=i),
                avg_response_time=100.0 + (i * 20),  # Increasing trend
                requests_per_second=1000.0 - (i * 50),  # Decreasing trend
                error_rate=1.0 + (i * 0.5)  # Increasing trend
            )
            performance_analyzer.performance_history.append(metrics)
        
        # Get trends
        trends = await performance_analyzer.get_performance_trends(hours=10)
        
        # Verify trends
        assert isinstance(trends, dict)
        assert 'response_time_trend' in trends
        assert 'throughput_trend' in trends
        assert 'error_rate_trend' in trends
        
        # Response time should be increasing
        assert trends['response_time_trend']['direction'] == 'increasing'
        # Throughput should be decreasing
        assert trends['throughput_trend']['direction'] == 'decreasing'


class TestAlertingSystem:
    """Test AlertingSystem functionality"""
    
    @pytest.fixture
    def alerting_system(self):
        return AlertingSystem()
    
    @pytest.mark.asyncio
    async def test_alerting_system_initialization(self, alerting_system):
        """Test alerting system initialization"""
        assert alerting_system is not None
        assert alerting_system.is_running == False
        assert alerting_system.alert_rules == {}
        assert alerting_system.active_alerts == {}
    
    @pytest.mark.asyncio
    async def test_add_alert_rule(self, alerting_system):
        """Test adding alert rule"""
        # Create alert rule
        rule = AlertRule(
            id="cpu_high",
            name="High CPU Usage",
            description="CPU usage is too high",
            condition="cpu_usage",
            severity=AlertSeverity.HIGH,
            threshold_value=80.0,
            threshold_operator=">",
            notification_channels=[NotificationChannel.EMAIL],
            notification_recipients=["admin@test.com"]
        )
        
        # Add rule
        alerting_system.add_alert_rule(rule)
        
        # Verify rule was added
        assert "cpu_high" in alerting_system.alert_rules
        assert alerting_system.alert_rules["cpu_high"] == rule
    
    @pytest.mark.asyncio
    async def test_condition_evaluation(self, alerting_system):
        """Test alert condition evaluation"""
        # Test different operators
        assert alerting_system._evaluate_condition(90.0, ">", 80.0) == True
        assert alerting_system._evaluate_condition(70.0, ">", 80.0) == False
        assert alerting_system._evaluate_condition(70.0, "<", 80.0) == True
        assert alerting_system._evaluate_condition(90.0, "<", 80.0) == False
        assert alerting_system._evaluate_condition(80.0, ">=", 80.0) == True
        assert alerting_system._evaluate_condition(80.0, "<=", 80.0) == True
        assert alerting_system._evaluate_condition(80.0, "==", 80.0) == True
        assert alerting_system._evaluate_condition(80.0, "!=", 90.0) == True
    
    @pytest.mark.asyncio
    async def test_rate_limiting(self, alerting_system):
        """Test notification rate limiting"""
        alert_id = "test_alert"
        
        # Should allow first notification
        assert alerting_system._check_rate_limit(alert_id) == True
        
        # Fill up rate limit
        for i in range(alerting_system.max_notifications_per_hour - 1):
            assert alerting_system._check_rate_limit(alert_id) == True
        
        # Should now be rate limited
        assert alerting_system._check_rate_limit(alert_id) == False
    
    @pytest.mark.asyncio
    async def test_acknowledge_alert(self, alerting_system):
        """Test alert acknowledgment"""
        # Create and add alert
        alert = Alert(
            id="test_alert",
            rule_id="test_rule",
            rule_name="Test Rule",
            severity=AlertSeverity.HIGH,
            status=AlertingSystem.AlertStatus.ACTIVE,
            title="Test Alert",
            description="Test alert description",
            message="Test message",
            triggered_at=datetime.utcnow()
        )
        
        alerting_system.active_alerts["test_alert"] = alert
        
        # Acknowledge alert
        result = await alerting_system.acknowledge_alert("test_alert", "admin")
        
        # Verify acknowledgment
        assert result == True
        assert alert.status == AlertingSystem.AlertStatus.ACKNOWLEDGED
        assert alert.acknowledged_at is not None
        assert alert.annotations.get('acknowledged_by') == "admin"
    
    @pytest.mark.asyncio
    async def test_alert_statistics(self, alerting_system):
        """Test alert statistics"""
        # Add some alerts
        for i, severity in enumerate([AlertSeverity.LOW, AlertSeverity.MEDIUM, AlertSeverity.HIGH, AlertSeverity.CRITICAL]):
            alert = Alert(
                id=f"alert_{i}",
                rule_id=f"rule_{i}",
                rule_name=f"Rule {i}",
                severity=severity,
                status=AlertingSystem.AlertStatus.ACTIVE,
                title=f"Alert {i}",
                description=f"Description {i}",
                message=f"Message {i}",
                triggered_at=datetime.utcnow()
            )
            alerting_system.active_alerts[f"alert_{i}"] = alert
        
        # Get statistics
        stats = alerting_system.get_alert_statistics()
        
        # Verify statistics
        assert stats['active_alerts'] == 4
        assert stats['severity_breakdown']['low'] == 1
        assert stats['severity_breakdown']['medium'] == 1
        assert stats['severity_breakdown']['high'] == 1
        assert stats['severity_breakdown']['critical'] == 1


class TestDashboardEngine:
    """Test DashboardEngine functionality"""
    
    @pytest.fixture
    def dashboard_engine(self):
        return DashboardEngine()
    
    @pytest.mark.asyncio
    async def test_dashboard_engine_initialization(self, dashboard_engine):
        """Test dashboard engine initialization"""
        assert dashboard_engine is not None
        assert dashboard_engine.is_running == False
        assert len(dashboard_engine.dashboards) > 0  # Should have default dashboards
        assert len(dashboard_engine.chart_configs) > 0
    
    @pytest.mark.asyncio
    async def test_create_dashboard(self, dashboard_engine):
        """Test dashboard creation"""
        # Create dashboard layout
        layout = DashboardLayout(
            id="test_dashboard",
            name="Test Dashboard",
            description="Test dashboard description",
            columns=12,
            rows=8
        )
        
        # Add a chart
        chart = ChartConfig(
            id="test_chart",
            title="Test Chart",
            chart_type=ChartType.LINE,
            data_source="test_data",
            width=6,
            height=4
        )
        layout.charts.append(chart)
        
        # Create dashboard
        result = dashboard_engine.create_dashboard(layout)
        
        # Verify creation
        assert result == True
        assert "test_dashboard" in dashboard_engine.dashboards
        assert "test_chart" in dashboard_engine.chart_configs
    
    @pytest.mark.asyncio
    async def test_update_dashboard(self, dashboard_engine):
        """Test dashboard update"""
        # Create initial dashboard
        layout = DashboardLayout(
            id="test_dashboard",
            name="Test Dashboard",
            description="Initial description"
        )
        dashboard_engine.create_dashboard(layout)
        
        # Update dashboard
        layout.description = "Updated description"
        layout.name = "Updated Dashboard"
        
        result = dashboard_engine.update_dashboard("test_dashboard", layout)
        
        # Verify update
        assert result == True
        updated_dashboard = dashboard_engine.get_dashboard("test_dashboard")
        assert updated_dashboard.description == "Updated description"
        assert updated_dashboard.name == "Updated Dashboard"
    
    @pytest.mark.asyncio
    async def test_delete_dashboard(self, dashboard_engine):
        """Test dashboard deletion"""
        # Create dashboard
        layout = DashboardLayout(
            id="test_dashboard",
            name="Test Dashboard"
        )
        dashboard_engine.create_dashboard(layout)
        
        # Verify it exists
        assert "test_dashboard" in dashboard_engine.dashboards
        
        # Delete dashboard
        result = dashboard_engine.delete_dashboard("test_dashboard")
        
        # Verify deletion
        assert result == True
        assert "test_dashboard" not in dashboard_engine.dashboards
    
    @pytest.mark.asyncio
    async def test_list_dashboards(self, dashboard_engine):
        """Test dashboard listing"""
        # Get all dashboards
        dashboards = dashboard_engine.list_dashboards()
        
        # Verify list
        assert isinstance(dashboards, list)
        assert len(dashboards) > 0  # Should have default dashboards
        assert all(isinstance(d, DashboardLayout) for d in dashboards)
    
    @pytest.mark.asyncio
    async def test_time_range_calculation(self, dashboard_engine):
        """Test time range calculation"""
        chart_config = ChartConfig(
            id="test_chart",
            title="Test Chart",
            chart_type=ChartType.LINE,
            data_source="test_data",
            time_range=TimeRange.LAST_HOUR
        )
        
        start_time, end_time = dashboard_engine._get_time_range(chart_config)
        
        # Verify time range
        assert isinstance(start_time, datetime)
        assert isinstance(end_time, datetime)
        assert start_time < end_time
        assert (end_time - start_time).total_seconds() == 3600  # 1 hour
    
    @pytest.mark.asyncio
    async def test_register_data_source(self, dashboard_engine):
        """Test data source registration"""
        # Mock data source function
        async def mock_data_source(chart_config, start_time, end_time):
            return {'labels': ['A', 'B', 'C'], 'data': [1, 2, 3]}
        
        # Register data source
        dashboard_engine.register_data_source("mock_data", mock_data_source)
        
        # Verify registration
        assert "mock_data" in dashboard_engine.data_sources
        assert dashboard_engine.data_sources["mock_data"] == mock_data_source
    
    @pytest.mark.asyncio
    async def test_export_dashboard(self, dashboard_engine):
        """Test dashboard export"""
        # Create dashboard
        layout = DashboardLayout(
            id="test_dashboard",
            name="Test Dashboard",
            description="Test description"
        )
        dashboard_engine.create_dashboard(layout)
        
        # Export dashboard
        exported = await dashboard_engine.export_dashboard("test_dashboard", "json")
        
        # Verify export
        assert exported is not None
        assert isinstance(exported, str)
        assert "test_dashboard" in exported
        assert "Test Dashboard" in exported
    
    @pytest.mark.asyncio
    async def test_import_dashboard(self, dashboard_engine):
        """Test dashboard import"""
        # Create dashboard JSON
        dashboard_json = '''
        {
            "id": "imported_dashboard",
            "name": "Imported Dashboard",
            "description": "Imported from JSON",
            "columns": 12,
            "rows": 8,
            "charts": [
                {
                    "id": "imported_chart",
                    "title": "Imported Chart",
                    "chart_type": "line",
                    "data_source": "test_data",
                    "width": 6,
                    "height": 4,
                    "time_range": "1h",
                    "filters": {},
                    "colors": [],
                    "theme": "default"
                }
            ]
        }
        '''
        
        # Import dashboard
        result = await dashboard_engine.import_dashboard(dashboard_json)
        
        # Verify import
        assert result == True
        assert "imported_dashboard" in dashboard_engine.dashboards
        assert "imported_chart" in dashboard_engine.chart_configs
        
        imported_dashboard = dashboard_engine.get_dashboard("imported_dashboard")
        assert imported_dashboard.name == "Imported Dashboard"
        assert len(imported_dashboard.charts) == 1
    
    @pytest.mark.asyncio
    async def test_dashboard_statistics(self, dashboard_engine):
        """Test dashboard statistics"""
        # Get statistics
        stats = dashboard_engine.get_dashboard_statistics()
        
        # Verify statistics
        assert isinstance(stats, dict)
        assert 'total_dashboards' in stats
        assert 'total_charts' in stats
        assert 'chart_types' in stats
        assert 'data_sources' in stats
        assert stats['total_dashboards'] >= 0
        assert stats['total_charts'] >= 0


@pytest.mark.asyncio
async def test_monitoring_system_integration():
    """Test integration between monitoring components"""
    # Initialize components
    system_monitor = SystemMonitor()
    performance_analyzer = PerformanceAnalyzer()
    alerting_system = AlertingSystem()
    dashboard_engine = DashboardEngine()
    
    # Test system monitor integration
    assert system_monitor is not None
    
    # Test performance analyzer integration
    assert performance_analyzer is not None
    
    # Test alerting system integration
    assert alerting_system is not None
    
    # Test dashboard engine integration
    assert dashboard_engine is not None
    
    # Test data flow between components
    # System monitor -> Performance analyzer
    await performance_analyzer.record_request("/api/test", "GET", 150.0, 200)
    assert len(performance_analyzer.request_metrics) == 1
    
    # Performance analyzer -> Alerting system
    rule = AlertRule(
        id="response_time_high",
        name="High Response Time",
        description="Response time is too high",
        condition="response_time",
        severity=AlertSeverity.HIGH,
        threshold_value=1000.0,
        threshold_operator=">",
        notification_channels=[NotificationChannel.EMAIL],
        notification_recipients=["admin@test.com"]
    )
    alerting_system.add_alert_rule(rule)
    assert "response_time_high" in alerting_system.alert_rules
    
    # Alerting system -> Dashboard engine
    dashboard = dashboard_engine.get_dashboard("system_overview")
    assert dashboard is not None
    assert len(dashboard.charts) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 