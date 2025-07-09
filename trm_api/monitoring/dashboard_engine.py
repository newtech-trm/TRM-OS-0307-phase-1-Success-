"""
Dashboard Engine cho TRM-OS Phase 3

Real-time monitoring dashboard với:
- Interactive charts và graphs
- Custom dashboard layouts
- Real-time data streaming
- Export capabilities
- Multi-tenant support
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import json
import base64
from io import BytesIO

logger = logging.getLogger(__name__)

# Optional dependencies for visualization
try:
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    from matplotlib.figure import Figure
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False


class ChartType(Enum):
    """Chart types"""
    LINE = "line"
    BAR = "bar"
    PIE = "pie"
    SCATTER = "scatter"
    HISTOGRAM = "histogram"
    HEATMAP = "heatmap"
    GAUGE = "gauge"
    TABLE = "table"


class TimeRange(Enum):
    """Time range options"""
    LAST_HOUR = "1h"
    LAST_6_HOURS = "6h"
    LAST_24_HOURS = "24h"
    LAST_7_DAYS = "7d"
    LAST_30_DAYS = "30d"
    CUSTOM = "custom"


@dataclass
class ChartConfig:
    """Chart configuration"""
    id: str
    title: str
    chart_type: ChartType
    data_source: str
    
    # Display settings
    width: int = 400
    height: int = 300
    refresh_interval: int = 30  # seconds
    
    # Chart-specific settings
    x_axis_label: str = ""
    y_axis_label: str = ""
    show_legend: bool = True
    show_grid: bool = True
    
    # Data settings
    time_range: TimeRange = TimeRange.LAST_HOUR
    custom_start: Optional[datetime] = None
    custom_end: Optional[datetime] = None
    
    # Filters
    filters: Dict[str, Any] = field(default_factory=dict)
    
    # Styling
    colors: List[str] = field(default_factory=list)
    theme: str = "default"
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class DashboardLayout:
    """Dashboard layout configuration"""
    id: str
    name: str
    description: str
    
    # Layout
    columns: int = 12
    rows: int = 8
    
    # Charts
    charts: List[ChartConfig] = field(default_factory=list)
    
    # Permissions
    owner: str = ""
    shared_with: List[str] = field(default_factory=list)
    public: bool = False
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    tags: List[str] = field(default_factory=list)


@dataclass
class DashboardData:
    """Dashboard data response"""
    timestamp: datetime
    chart_id: str
    data: Dict[str, Any]
    metadata: Dict[str, Any] = field(default_factory=dict)


class DashboardEngine:
    """Main dashboard engine"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.is_running = False
        
        # Storage
        self.dashboards: Dict[str, DashboardLayout] = {}
        self.chart_configs: Dict[str, ChartConfig] = {}
        
        # Data sources
        self.data_sources: Dict[str, Any] = {}
        self.data_cache: Dict[str, Dict[str, Any]] = {}
        
        # Real-time connections
        self.websocket_connections: Dict[str, List[Any]] = {}
        
        # Configuration
        self.cache_ttl = 30  # seconds
        self.max_data_points = 1000
        
        # Default color schemes
        self.color_schemes = {
            'default': ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'],
            'pastel': ['#AEC7E8', '#FFBB78', '#98DF8A', '#FF9896', '#C5B0D5'],
            'dark': ['#1f1f1f', '#ff6b6b', '#4ecdc4', '#45b7d1', '#f9ca24'],
            'corporate': ['#2c3e50', '#3498db', '#e74c3c', '#f39c12', '#9b59b6']
        }
        
        # Setup default dashboards
        self._setup_default_dashboards()
    
    def _setup_default_dashboards(self):
        """Setup default dashboard layouts"""
        try:
            # System Overview Dashboard
            system_dashboard = DashboardLayout(
                id="system_overview",
                name="System Overview",
                description="Main system monitoring dashboard",
                columns=12,
                rows=8
            )
            
            # Add system charts
            system_charts = [
                ChartConfig(
                    id="cpu_usage",
                    title="CPU Usage",
                    chart_type=ChartType.LINE,
                    data_source="system_metrics",
                    width=6,
                    height=4,
                    y_axis_label="CPU %"
                ),
                ChartConfig(
                    id="memory_usage",
                    title="Memory Usage",
                    chart_type=ChartType.LINE,
                    data_source="system_metrics",
                    width=6,
                    height=4,
                    y_axis_label="Memory %"
                ),
                ChartConfig(
                    id="disk_usage",
                    title="Disk Usage",
                    chart_type=ChartType.BAR,
                    data_source="system_metrics",
                    width=4,
                    height=4,
                    y_axis_label="Disk %"
                ),
                ChartConfig(
                    id="network_io",
                    title="Network I/O",
                    chart_type=ChartType.LINE,
                    data_source="system_metrics",
                    width=8,
                    height=4,
                    y_axis_label="Bytes/sec"
                )
            ]
            
            system_dashboard.charts = system_charts
            self.dashboards["system_overview"] = system_dashboard
            
            # Performance Dashboard
            performance_dashboard = DashboardLayout(
                id="performance",
                name="Performance Metrics",
                description="Application performance monitoring",
                columns=12,
                rows=8
            )
            
            performance_charts = [
                ChartConfig(
                    id="response_time",
                    title="Response Time",
                    chart_type=ChartType.LINE,
                    data_source="performance_metrics",
                    width=6,
                    height=4,
                    y_axis_label="Response Time (ms)"
                ),
                ChartConfig(
                    id="throughput",
                    title="Throughput",
                    chart_type=ChartType.LINE,
                    data_source="performance_metrics",
                    width=6,
                    height=4,
                    y_axis_label="Requests/sec"
                ),
                ChartConfig(
                    id="error_rate",
                    title="Error Rate",
                    chart_type=ChartType.LINE,
                    data_source="performance_metrics",
                    width=6,
                    height=4,
                    y_axis_label="Error %"
                ),
                ChartConfig(
                    id="active_alerts",
                    title="Active Alerts",
                    chart_type=ChartType.PIE,
                    data_source="alert_metrics",
                    width=6,
                    height=4
                )
            ]
            
            performance_dashboard.charts = performance_charts
            self.dashboards["performance"] = performance_dashboard
            
            # Store chart configs
            for dashboard in self.dashboards.values():
                for chart in dashboard.charts:
                    self.chart_configs[chart.id] = chart
            
        except Exception as e:
            self.logger.error(f"Failed to setup default dashboards: {e}")
    
    async def start(self) -> None:
        """Start dashboard engine"""
        try:
            if self.is_running:
                self.logger.warning("Dashboard engine already running")
                return
            
            self.is_running = True
            self.logger.info("Starting dashboard engine...")
            
            # Start data refresh loop
            refresh_task = asyncio.create_task(self._data_refresh_loop())
            await refresh_task
            
        except Exception as e:
            self.logger.error(f"Failed to start dashboard engine: {e}")
            self.is_running = False
            raise
    
    async def stop(self) -> None:
        """Stop dashboard engine"""
        self.is_running = False
        self.logger.info("Dashboard engine stopped")
    
    async def _data_refresh_loop(self) -> None:
        """Data refresh loop"""
        while self.is_running:
            try:
                # Refresh data for all charts
                for chart_id, chart_config in self.chart_configs.items():
                    await self._refresh_chart_data(chart_config)
                
                # Broadcast updates to websocket connections
                await self._broadcast_updates()
                
                # Wait before next refresh
                await asyncio.sleep(30)
                
            except Exception as e:
                self.logger.error(f"Data refresh error: {e}")
                await asyncio.sleep(30)
    
    async def _refresh_chart_data(self, chart_config: ChartConfig) -> None:
        """Refresh data for a specific chart"""
        try:
            # Check cache first
            cache_key = f"{chart_config.id}_{chart_config.data_source}"
            cached_data = self.data_cache.get(cache_key)
            
            if cached_data:
                cache_time = cached_data.get('timestamp', datetime.min)
                if (datetime.utcnow() - cache_time).seconds < self.cache_ttl:
                    return  # Use cached data
            
            # Fetch new data
            data = await self._fetch_chart_data(chart_config)
            
            if data:
                # Cache the data
                self.data_cache[cache_key] = {
                    'timestamp': datetime.utcnow(),
                    'data': data,
                    'chart_id': chart_config.id
                }
            
        except Exception as e:
            self.logger.error(f"Chart data refresh failed for {chart_config.id}: {e}")
    
    async def _fetch_chart_data(self, chart_config: ChartConfig) -> Optional[Dict[str, Any]]:
        """Fetch data for chart from data source"""
        try:
            data_source = chart_config.data_source
            
            # Get time range
            start_time, end_time = self._get_time_range(chart_config)
            
            # Simulate data fetching based on data source
            if data_source == "system_metrics":
                return await self._fetch_system_metrics(chart_config, start_time, end_time)
            elif data_source == "performance_metrics":
                return await self._fetch_performance_metrics(chart_config, start_time, end_time)
            elif data_source == "alert_metrics":
                return await self._fetch_alert_metrics(chart_config, start_time, end_time)
            else:
                # Custom data source
                if data_source in self.data_sources:
                    return await self.data_sources[data_source](chart_config, start_time, end_time)
            
            return None
            
        except Exception as e:
            self.logger.error(f"Data fetch failed for {chart_config.id}: {e}")
            return None
    
    def _get_time_range(self, chart_config: ChartConfig) -> tuple:
        """Get time range for chart"""
        end_time = datetime.utcnow()
        
        if chart_config.time_range == TimeRange.LAST_HOUR:
            start_time = end_time - timedelta(hours=1)
        elif chart_config.time_range == TimeRange.LAST_6_HOURS:
            start_time = end_time - timedelta(hours=6)
        elif chart_config.time_range == TimeRange.LAST_24_HOURS:
            start_time = end_time - timedelta(hours=24)
        elif chart_config.time_range == TimeRange.LAST_7_DAYS:
            start_time = end_time - timedelta(days=7)
        elif chart_config.time_range == TimeRange.LAST_30_DAYS:
            start_time = end_time - timedelta(days=30)
        elif chart_config.time_range == TimeRange.CUSTOM:
            start_time = chart_config.custom_start or (end_time - timedelta(hours=1))
            end_time = chart_config.custom_end or end_time
        else:
            start_time = end_time - timedelta(hours=1)
        
        return start_time, end_time
    
    async def _fetch_system_metrics(self, chart_config: ChartConfig, 
                                   start_time: datetime, end_time: datetime) -> Dict[str, Any]:
        """Fetch system metrics data"""
        try:
            # Simulate system metrics data
            import random
            
            # Generate time series data
            time_points = []
            current_time = start_time
            while current_time <= end_time:
                time_points.append(current_time)
                current_time += timedelta(minutes=5)
            
            if chart_config.id == "cpu_usage":
                values = [random.uniform(10, 90) for _ in time_points]
                return {
                    'labels': [t.isoformat() for t in time_points],
                    'datasets': [{
                        'label': 'CPU Usage',
                        'data': values,
                        'borderColor': '#1f77b4',
                        'backgroundColor': 'rgba(31, 119, 180, 0.1)'
                    }]
                }
            
            elif chart_config.id == "memory_usage":
                values = [random.uniform(30, 80) for _ in time_points]
                return {
                    'labels': [t.isoformat() for t in time_points],
                    'datasets': [{
                        'label': 'Memory Usage',
                        'data': values,
                        'borderColor': '#ff7f0e',
                        'backgroundColor': 'rgba(255, 127, 14, 0.1)'
                    }]
                }
            
            elif chart_config.id == "disk_usage":
                return {
                    'labels': ['Root', 'Home', 'Var', 'Tmp'],
                    'datasets': [{
                        'label': 'Disk Usage',
                        'data': [random.uniform(20, 80) for _ in range(4)],
                        'backgroundColor': ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
                    }]
                }
            
            elif chart_config.id == "network_io":
                rx_values = [random.uniform(1000, 10000) for _ in time_points]
                tx_values = [random.uniform(500, 5000) for _ in time_points]
                return {
                    'labels': [t.isoformat() for t in time_points],
                    'datasets': [
                        {
                            'label': 'RX',
                            'data': rx_values,
                            'borderColor': '#2ca02c',
                            'backgroundColor': 'rgba(44, 160, 44, 0.1)'
                        },
                        {
                            'label': 'TX',
                            'data': tx_values,
                            'borderColor': '#d62728',
                            'backgroundColor': 'rgba(214, 39, 40, 0.1)'
                        }
                    ]
                }
            
            return {}
            
        except Exception as e:
            self.logger.error(f"System metrics fetch failed: {e}")
            return {}
    
    async def _fetch_performance_metrics(self, chart_config: ChartConfig, 
                                        start_time: datetime, end_time: datetime) -> Dict[str, Any]:
        """Fetch performance metrics data"""
        try:
            import random
            
            # Generate time series data
            time_points = []
            current_time = start_time
            while current_time <= end_time:
                time_points.append(current_time)
                current_time += timedelta(minutes=5)
            
            if chart_config.id == "response_time":
                values = [random.uniform(50, 500) for _ in time_points]
                return {
                    'labels': [t.isoformat() for t in time_points],
                    'datasets': [{
                        'label': 'Avg Response Time',
                        'data': values,
                        'borderColor': '#9467bd',
                        'backgroundColor': 'rgba(148, 103, 189, 0.1)'
                    }]
                }
            
            elif chart_config.id == "throughput":
                values = [random.uniform(100, 1000) for _ in time_points]
                return {
                    'labels': [t.isoformat() for t in time_points],
                    'datasets': [{
                        'label': 'Requests/sec',
                        'data': values,
                        'borderColor': '#17becf',
                        'backgroundColor': 'rgba(23, 190, 207, 0.1)'
                    }]
                }
            
            elif chart_config.id == "error_rate":
                values = [random.uniform(0, 10) for _ in time_points]
                return {
                    'labels': [t.isoformat() for t in time_points],
                    'datasets': [{
                        'label': 'Error Rate %',
                        'data': values,
                        'borderColor': '#d62728',
                        'backgroundColor': 'rgba(214, 39, 40, 0.1)'
                    }]
                }
            
            return {}
            
        except Exception as e:
            self.logger.error(f"Performance metrics fetch failed: {e}")
            return {}
    
    async def _fetch_alert_metrics(self, chart_config: ChartConfig, 
                                  start_time: datetime, end_time: datetime) -> Dict[str, Any]:
        """Fetch alert metrics data"""
        try:
            import random
            
            if chart_config.id == "active_alerts":
                return {
                    'labels': ['Critical', 'High', 'Medium', 'Low'],
                    'datasets': [{
                        'data': [
                            random.randint(0, 5),
                            random.randint(0, 10),
                            random.randint(0, 15),
                            random.randint(0, 20)
                        ],
                        'backgroundColor': ['#d62728', '#ff7f0e', '#2ca02c', '#1f77b4']
                    }]
                }
            
            return {}
            
        except Exception as e:
            self.logger.error(f"Alert metrics fetch failed: {e}")
            return {}
    
    async def _broadcast_updates(self) -> None:
        """Broadcast updates to connected websockets"""
        try:
            # In a real implementation, this would send updates to websocket connections
            # For now, just log the update
            if self.websocket_connections:
                self.logger.debug(f"Broadcasting updates to {len(self.websocket_connections)} connections")
            
        except Exception as e:
            self.logger.error(f"Broadcast failed: {e}")
    
    # Public API methods
    
    def create_dashboard(self, layout: DashboardLayout) -> bool:
        """Create new dashboard"""
        try:
            self.dashboards[layout.id] = layout
            
            # Add charts to chart configs
            for chart in layout.charts:
                self.chart_configs[chart.id] = chart
            
            self.logger.info(f"Dashboard created: {layout.name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Dashboard creation failed: {e}")
            return False
    
    def update_dashboard(self, dashboard_id: str, layout: DashboardLayout) -> bool:
        """Update existing dashboard"""
        try:
            if dashboard_id not in self.dashboards:
                return False
            
            layout.updated_at = datetime.utcnow()
            self.dashboards[dashboard_id] = layout
            
            # Update chart configs
            for chart in layout.charts:
                chart.updated_at = datetime.utcnow()
                self.chart_configs[chart.id] = chart
            
            self.logger.info(f"Dashboard updated: {layout.name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Dashboard update failed: {e}")
            return False
    
    def delete_dashboard(self, dashboard_id: str) -> bool:
        """Delete dashboard"""
        try:
            if dashboard_id not in self.dashboards:
                return False
            
            dashboard = self.dashboards[dashboard_id]
            
            # Remove chart configs
            for chart in dashboard.charts:
                if chart.id in self.chart_configs:
                    del self.chart_configs[chart.id]
            
            del self.dashboards[dashboard_id]
            
            self.logger.info(f"Dashboard deleted: {dashboard_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Dashboard deletion failed: {e}")
            return False
    
    def get_dashboard(self, dashboard_id: str) -> Optional[DashboardLayout]:
        """Get dashboard by ID"""
        return self.dashboards.get(dashboard_id)
    
    def list_dashboards(self, user: str = None) -> List[DashboardLayout]:
        """List available dashboards"""
        dashboards = list(self.dashboards.values())
        
        if user:
            # Filter by user permissions
            dashboards = [
                d for d in dashboards 
                if d.owner == user or user in d.shared_with or d.public
            ]
        
        return sorted(dashboards, key=lambda d: d.updated_at, reverse=True)
    
    async def get_chart_data(self, chart_id: str, refresh: bool = False) -> Optional[Dict[str, Any]]:
        """Get data for specific chart"""
        try:
            chart_config = self.chart_configs.get(chart_id)
            if not chart_config:
                return None
            
            # Check cache first
            cache_key = f"{chart_id}_{chart_config.data_source}"
            
            if not refresh and cache_key in self.data_cache:
                cached_data = self.data_cache[cache_key]
                cache_time = cached_data.get('timestamp', datetime.min)
                
                if (datetime.utcnow() - cache_time).seconds < self.cache_ttl:
                    return cached_data.get('data')
            
            # Fetch fresh data
            await self._refresh_chart_data(chart_config)
            
            # Return cached data
            if cache_key in self.data_cache:
                return self.data_cache[cache_key].get('data')
            
            return None
            
        except Exception as e:
            self.logger.error(f"Chart data retrieval failed: {e}")
            return None
    
    def register_data_source(self, name: str, callback: callable) -> None:
        """Register custom data source"""
        self.data_sources[name] = callback
        self.logger.info(f"Data source registered: {name}")
    
    async def export_dashboard(self, dashboard_id: str, format: str = "json") -> Optional[str]:
        """Export dashboard configuration"""
        try:
            dashboard = self.get_dashboard(dashboard_id)
            if not dashboard:
                return None
            
            if format.lower() == "json":
                # Convert to JSON
                dashboard_dict = {
                    'id': dashboard.id,
                    'name': dashboard.name,
                    'description': dashboard.description,
                    'columns': dashboard.columns,
                    'rows': dashboard.rows,
                    'charts': [
                        {
                            'id': chart.id,
                            'title': chart.title,
                            'chart_type': chart.chart_type.value,
                            'data_source': chart.data_source,
                            'width': chart.width,
                            'height': chart.height,
                            'time_range': chart.time_range.value,
                            'filters': chart.filters,
                            'colors': chart.colors,
                            'theme': chart.theme
                        }
                        for chart in dashboard.charts
                    ],
                    'created_at': dashboard.created_at.isoformat(),
                    'updated_at': dashboard.updated_at.isoformat()
                }
                
                return json.dumps(dashboard_dict, indent=2)
            
            return None
            
        except Exception as e:
            self.logger.error(f"Dashboard export failed: {e}")
            return None
    
    async def import_dashboard(self, dashboard_json: str) -> bool:
        """Import dashboard from JSON"""
        try:
            dashboard_dict = json.loads(dashboard_json)
            
            # Create dashboard layout
            layout = DashboardLayout(
                id=dashboard_dict['id'],
                name=dashboard_dict['name'],
                description=dashboard_dict['description'],
                columns=dashboard_dict.get('columns', 12),
                rows=dashboard_dict.get('rows', 8)
            )
            
            # Create charts
            for chart_dict in dashboard_dict.get('charts', []):
                chart = ChartConfig(
                    id=chart_dict['id'],
                    title=chart_dict['title'],
                    chart_type=ChartType(chart_dict['chart_type']),
                    data_source=chart_dict['data_source'],
                    width=chart_dict.get('width', 400),
                    height=chart_dict.get('height', 300),
                    time_range=TimeRange(chart_dict.get('time_range', '1h')),
                    filters=chart_dict.get('filters', {}),
                    colors=chart_dict.get('colors', []),
                    theme=chart_dict.get('theme', 'default')
                )
                layout.charts.append(chart)
            
            # Create dashboard
            return self.create_dashboard(layout)
            
        except Exception as e:
            self.logger.error(f"Dashboard import failed: {e}")
            return False
    
    async def generate_chart_image(self, chart_id: str) -> Optional[str]:
        """Generate chart image (base64 encoded)"""
        try:
            if not HAS_MATPLOTLIB:
                self.logger.warning("Matplotlib not available for chart generation")
                return None
            
            chart_config = self.chart_configs.get(chart_id)
            if not chart_config:
                return None
            
            # Get chart data
            data = await self.get_chart_data(chart_id)
            if not data:
                return None
            
            # Create matplotlib figure
            fig, ax = plt.subplots(figsize=(chart_config.width/100, chart_config.height/100))
            
            # Generate chart based on type
            if chart_config.chart_type == ChartType.LINE:
                self._generate_line_chart(ax, data, chart_config)
            elif chart_config.chart_type == ChartType.BAR:
                self._generate_bar_chart(ax, data, chart_config)
            elif chart_config.chart_type == ChartType.PIE:
                self._generate_pie_chart(ax, data, chart_config)
            
            # Save to base64
            buffer = BytesIO()
            fig.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
            buffer.seek(0)
            
            image_base64 = base64.b64encode(buffer.getvalue()).decode()
            
            plt.close(fig)
            
            return image_base64
            
        except Exception as e:
            self.logger.error(f"Chart image generation failed: {e}")
            return None
    
    def _generate_line_chart(self, ax, data: Dict[str, Any], chart_config: ChartConfig) -> None:
        """Generate line chart"""
        try:
            labels = data.get('labels', [])
            datasets = data.get('datasets', [])
            
            for dataset in datasets:
                ax.plot(labels, dataset['data'], 
                       label=dataset.get('label', ''),
                       color=dataset.get('borderColor', '#1f77b4'))
            
            ax.set_title(chart_config.title)
            ax.set_xlabel(chart_config.x_axis_label)
            ax.set_ylabel(chart_config.y_axis_label)
            
            if chart_config.show_legend and datasets:
                ax.legend()
            
            if chart_config.show_grid:
                ax.grid(True, alpha=0.3)
            
        except Exception as e:
            self.logger.error(f"Line chart generation failed: {e}")
    
    def _generate_bar_chart(self, ax, data: Dict[str, Any], chart_config: ChartConfig) -> None:
        """Generate bar chart"""
        try:
            labels = data.get('labels', [])
            datasets = data.get('datasets', [])
            
            if datasets:
                dataset = datasets[0]
                colors = dataset.get('backgroundColor', chart_config.colors or '#1f77b4')
                ax.bar(labels, dataset['data'], color=colors)
            
            ax.set_title(chart_config.title)
            ax.set_xlabel(chart_config.x_axis_label)
            ax.set_ylabel(chart_config.y_axis_label)
            
            if chart_config.show_grid:
                ax.grid(True, alpha=0.3)
            
        except Exception as e:
            self.logger.error(f"Bar chart generation failed: {e}")
    
    def _generate_pie_chart(self, ax, data: Dict[str, Any], chart_config: ChartConfig) -> None:
        """Generate pie chart"""
        try:
            labels = data.get('labels', [])
            datasets = data.get('datasets', [])
            
            if datasets:
                dataset = datasets[0]
                colors = dataset.get('backgroundColor', chart_config.colors)
                ax.pie(dataset['data'], labels=labels, colors=colors, autopct='%1.1f%%')
            
            ax.set_title(chart_config.title)
            
        except Exception as e:
            self.logger.error(f"Pie chart generation failed: {e}")
    
    def get_dashboard_statistics(self) -> Dict[str, Any]:
        """Get dashboard statistics"""
        try:
            total_dashboards = len(self.dashboards)
            total_charts = len(self.chart_configs)
            
            # Count by chart type
            chart_types = {}
            for chart in self.chart_configs.values():
                chart_type = chart.chart_type.value
                chart_types[chart_type] = chart_types.get(chart_type, 0) + 1
            
            return {
                'total_dashboards': total_dashboards,
                'total_charts': total_charts,
                'chart_types': chart_types,
                'data_sources': list(self.data_sources.keys()),
                'cached_datasets': len(self.data_cache),
                'active_connections': sum(len(conns) for conns in self.websocket_connections.values())
            }
            
        except Exception as e:
            self.logger.error(f"Dashboard statistics failed: {e}")
            return {} 