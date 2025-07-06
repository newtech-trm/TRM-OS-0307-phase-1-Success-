"""
Data Analyst Agent Template

Agent chuyên biệt xử lý các tensions liên quan đến data analysis, data processing,
reporting và business intelligence trong TRM-OS.
"""

import re
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime

from .base_template import BaseAgentTemplate, AgentTemplateMetadata, AgentCapability
from ..base_agent import AgentMetadata
from ...eventbus.system_event_bus import EventType, SystemEvent
from ...models.tension import Tension
from ...models.enums import TensionType


class DataAnalystAgent(BaseAgentTemplate):
    """
    Agent chuyên biệt cho data analysis và business intelligence.
    
    Capabilities:
    - Data quality assessment
    - Statistical analysis
    - Report generation
    - Data visualization recommendations
    - Performance metrics calculation
    - Trend analysis
    """
    
    def __init__(self, agent_id: Optional[str] = None, metadata: Optional[AgentMetadata] = None):
        # Tạo metadata cho DataAnalyst nếu chưa có
        if not metadata:
            metadata = AgentMetadata(
                name="DataAnalystAgent",
                agent_type="DataAnalyst",
                description="AI Agent chuyên biệt xử lý tensions liên quan đến data analysis và business intelligence",
                capabilities=["data_analysis", "statistical_computing", "report_generation", "data_visualization", "performance_metrics"],
                status="active",
                version="1.0.0"
            )
        
        super().__init__(agent_id, metadata)
        
        # Data-specific components
        self.data_patterns = {
            "quality_issues": [
                r"dữ liệu.*(?:thiếu|sai|không chính xác|lỗi)",
                r"data.*(?:missing|incorrect|invalid|corrupted)",
                r"quality.*(?:poor|low|bad)",
                r"report.*(?:sai|không đúng|lỗi)"
            ],
            "analysis_requests": [
                r"phân tích.*(?:dữ liệu|số liệu|báo cáo)",
                r"analyze.*(?:data|metrics|performance|trends)",
                r"statistical.*(?:analysis|report|study)",
                r"dashboard.*(?:cần|thiếu|yêu cầu)"
            ],
            "performance_metrics": [
                r"(?:KPI|metric|chỉ số).*(?:giảm|tăng|thay đổi)",
                r"performance.*(?:drop|increase|change|issue)",
                r"conversion.*(?:rate|tỷ lệ)",
                r"efficiency.*(?:hiệu suất|năng suất)"
            ]
        }
        
        self.analysis_tools = {
            "statistical_methods": ["descriptive_stats", "correlation", "regression", "time_series"],
            "visualization_types": ["charts", "graphs", "dashboards", "heatmaps"],
            "data_sources": ["database", "api", "files", "real_time_streams"],
            "reporting_formats": ["executive_summary", "detailed_report", "dashboard", "presentation"]
        }
    
    def _get_default_template_metadata(self) -> AgentTemplateMetadata:
        """Trả về metadata mặc định cho DataAnalyst template"""
        return AgentTemplateMetadata(
            template_name="DataAnalystAgent",
            template_version="1.0.0",
            description="Agent chuyên biệt xử lý tensions liên quan đến data analysis và business intelligence",
            primary_domain="data",
            capabilities=[
                AgentCapability(
                    name="data_quality_assessment",
                    description="Đánh giá chất lượng dữ liệu và phát hiện issues",
                    required_skills=["data_validation", "statistical_analysis"],
                    complexity_level=3,
                    estimated_time=30
                ),
                AgentCapability(
                    name="statistical_analysis",
                    description="Thực hiện phân tích thống kê và tìm insights",
                    required_skills=["statistics", "data_science", "pattern_recognition"],
                    complexity_level=4,
                    estimated_time=60
                ),
                AgentCapability(
                    name="report_generation",
                    description="Tạo báo cáo và dashboards tự động",
                    required_skills=["reporting", "visualization", "business_intelligence"],
                    complexity_level=3,
                    estimated_time=45
                ),
                AgentCapability(
                    name="performance_monitoring",
                    description="Monitor và phân tích performance metrics",
                    required_skills=["metrics_analysis", "monitoring", "alerting"],
                    complexity_level=2,
                    estimated_time=20
                ),
                AgentCapability(
                    name="trend_analysis",
                    description="Phân tích xu hướng và dự báo",
                    required_skills=["time_series", "forecasting", "trend_detection"],
                    complexity_level=4,
                    estimated_time=90
                )
            ],
            recommended_tensions=[
                "Data Quality Issues",
                "Performance Metrics Problems", 
                "Reporting Requirements",
                "Business Intelligence Needs",
                "Analytics Automation"
            ],
            dependencies=["database_access", "visualization_tools"],
            performance_metrics=[
                "data_accuracy_improvement",
                "report_generation_time",
                "insights_discovery_rate",
                "stakeholder_satisfaction"
            ]
        )
    
    async def can_handle_tension(self, tension: Tension) -> bool:
        """Kiểm tra xem có thể xử lý tension này không"""
        try:
            # Kiểm tra description của tension
            description = tension.description.lower()
            
            # Tìm data-related keywords
            data_keywords = [
                "data", "dữ liệu", "số liệu", "báo cáo", "report", "dashboard",
                "analytics", "phân tích", "thống kê", "statistical", "metrics",
                "KPI", "performance", "hiệu suất", "chỉ số"
            ]
            
            has_data_keywords = any(keyword in description for keyword in data_keywords)
            
            # Kiểm tra patterns cụ thể
            pattern_match = False
            for category, patterns in self.data_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, description, re.IGNORECASE):
                        pattern_match = True
                        break
                if pattern_match:
                    break
            
            # Kiểm tra tension type
            suitable_types = [TensionType.PROBLEM, TensionType.OPPORTUNITY, TensionType.IDEA, TensionType.RESOURCE_CONSTRAINT]
            type_match = tension.tensionType in suitable_types
            
            # Agent có thể handle nếu có data keywords hoặc pattern match
            can_handle = (has_data_keywords or pattern_match) and type_match
            
            if can_handle:
                self.logger.info(f"DataAnalyst can handle tension {tension.uid}: {tension.title}")
            
            return can_handle
            
        except Exception as e:
            self.logger.error(f"Error checking tension handleability: {str(e)}")
            return False
    
    async def analyze_tension_requirements(self, tension: Tension) -> Dict[str, Any]:
        """Phân tích requirements cụ thể cho data tension"""
        requirements = {
            "analysis_type": "unknown",
            "data_sources": [],
            "complexity": "medium",
            "urgency": "normal",
            "deliverables": [],
            "tools_needed": [],
            "estimated_effort": 60,
            "success_criteria": []
        }
        
        try:
            description = tension.description.lower()
            
            # Xác định loại analysis
            if any(pattern in description for pattern in ["quality", "chất lượng", "validation"]):
                requirements["analysis_type"] = "data_quality"
                requirements["tools_needed"].extend(["data_profiling", "validation_rules"])
                requirements["deliverables"].append("Data Quality Report")
                
            elif any(pattern in description for pattern in ["performance", "hiệu suất", "kpi", "metrics"]):
                requirements["analysis_type"] = "performance_analysis"
                requirements["tools_needed"].extend(["metrics_dashboard", "alerting"])
                requirements["deliverables"].append("Performance Dashboard")
                
            elif any(pattern in description for pattern in ["trend", "xu hướng", "forecast", "dự báo"]):
                requirements["analysis_type"] = "trend_analysis"
                requirements["tools_needed"].extend(["time_series_analysis", "forecasting_models"])
                requirements["deliverables"].append("Trend Analysis Report")
                requirements["estimated_effort"] = 90
                
            elif any(pattern in description for pattern in ["report", "báo cáo", "dashboard"]):
                requirements["analysis_type"] = "reporting"
                requirements["tools_needed"].extend(["reporting_engine", "visualization_tools"])
                requirements["deliverables"].append("Custom Report/Dashboard")
                
            # Xác định data sources
            if "database" in description:
                requirements["data_sources"].append("database")
            if any(pattern in description for pattern in ["api", "real-time", "thời gian thực"]):
                requirements["data_sources"].append("api")
            if any(pattern in description for pattern in ["file", "csv", "excel", "tệp"]):
                requirements["data_sources"].append("files")
                
            # Xác định complexity
            complexity_indicators = {
                "high": ["complex", "phức tạp", "advanced", "machine learning", "ai"],
                "low": ["simple", "đơn giản", "basic", "cơ bản"]
            }
            
            for level, indicators in complexity_indicators.items():
                if any(indicator in description for indicator in indicators):
                    requirements["complexity"] = level
                    break
            
            # Xác định urgency
            if any(pattern in description for pattern in ["urgent", "gấp", "asap", "ngay lập tức"]):
                requirements["urgency"] = "high"
                requirements["estimated_effort"] = max(30, requirements["estimated_effort"] // 2)
            
            # Success criteria
            requirements["success_criteria"] = [
                "Data accuracy > 95%",
                "Report generation time < 5 minutes",
                "Stakeholder approval achieved",
                "Insights actionable and clear"
            ]
            
            self.logger.info(f"Analyzed requirements for tension {tension.uid}: {requirements['analysis_type']}")
            
        except Exception as e:
            self.logger.error(f"Error analyzing tension requirements: {str(e)}")
        
        return requirements
    
    async def generate_specialized_solutions(self, tension: Tension, 
                                           requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Tạo solutions chuyên biệt cho data analysis"""
        solutions = []
        
        try:
            analysis_type = requirements.get("analysis_type", "unknown")
            
            if analysis_type == "data_quality":
                solutions.extend(await self._generate_data_quality_solutions(tension, requirements))
                
            elif analysis_type == "performance_analysis":
                solutions.extend(await self._generate_performance_solutions(tension, requirements))
                
            elif analysis_type == "trend_analysis":
                solutions.extend(await self._generate_trend_solutions(tension, requirements))
                
            elif analysis_type == "reporting":
                solutions.extend(await self._generate_reporting_solutions(tension, requirements))
                
            else:
                # Generic data solutions
                solutions.extend(await self._generate_generic_data_solutions(tension, requirements))
            
            # Thêm metadata cho tất cả solutions
            for solution in solutions:
                solution.update({
                    "agent_template": "DataAnalystAgent",
                    "domain": "data_analysis",
                    "estimated_effort": requirements.get("estimated_effort", 60),
                    "complexity": requirements.get("complexity", "medium"),
                    "success_criteria": requirements.get("success_criteria", [])
                })
            
            self.logger.info(f"Generated {len(solutions)} data analysis solutions for tension {tension.uid}")
            
        except Exception as e:
            self.logger.error(f"Error generating solutions: {str(e)}")
        
        return solutions
    
    async def _generate_data_quality_solutions(self, tension: Tension, 
                                             requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Tạo solutions cho data quality issues"""
        return [
            {
                "title": "Data Quality Assessment & Cleanup",
                "description": "Thực hiện đánh giá toàn diện chất lượng dữ liệu và đề xuất cleanup plan",
                "approach": "Automated Data Profiling",
                "steps": [
                    "Chạy data profiling tools để phát hiện issues",
                    "Phân tích missing values, duplicates, outliers",
                    "Tạo data quality rules và validation logic",
                    "Implement automated cleanup procedures",
                    "Setup monitoring cho data quality ongoing"
                ],
                "tools": ["data_profiling", "validation_engine", "cleanup_scripts"],
                "deliverables": ["Data Quality Report", "Cleanup Scripts", "Monitoring Dashboard"],
                "timeline": "2-3 weeks",
                "priority": 2
            },
            {
                "title": "Real-time Data Validation System",
                "description": "Thiết lập hệ thống validation real-time để prevent data quality issues",
                "approach": "Preventive Data Governance",
                "steps": [
                    "Thiết kế validation rules cho data ingestion",
                    "Implement real-time validation pipeline",
                    "Setup alerts cho data quality violations", 
                    "Tạo data quality metrics dashboard",
                    "Train team về data quality best practices"
                ],
                "tools": ["validation_pipeline", "alerting_system", "metrics_dashboard"],
                "deliverables": ["Validation System", "Quality Metrics", "Training Materials"],
                "timeline": "3-4 weeks",
                "priority": 1
            }
        ]
    
    async def _generate_performance_solutions(self, tension: Tension,
                                            requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Tạo solutions cho performance analysis"""
        return [
            {
                "title": "Performance Metrics Dashboard",
                "description": "Tạo dashboard real-time tracking key performance indicators",
                "approach": "Real-time Performance Monitoring",
                "steps": [
                    "Identify key performance metrics cần track",
                    "Setup data collection từ multiple sources",
                    "Design interactive dashboard với drill-down capability",
                    "Implement automated alerting cho performance thresholds",
                    "Create performance trend analysis reports"
                ],
                "tools": ["dashboard_builder", "metrics_collector", "alerting_engine"],
                "deliverables": ["Performance Dashboard", "Alerting System", "Trend Reports"],
                "timeline": "2-3 weeks",
                "priority": 1
            },
            {
                "title": "Advanced Performance Analytics",
                "description": "Phân tích sâu performance patterns và root causes",
                "approach": "Statistical Performance Analysis",
                "steps": [
                    "Collect historical performance data",
                    "Apply statistical analysis để identify patterns",
                    "Perform root cause analysis cho performance issues",
                    "Create predictive models cho performance forecasting",
                    "Generate actionable recommendations"
                ],
                "tools": ["statistical_analysis", "predictive_modeling", "root_cause_analysis"],
                "deliverables": ["Analysis Report", "Predictive Models", "Recommendations"],
                "timeline": "3-4 weeks",
                "priority": 2
            }
        ]
    
    async def _generate_trend_solutions(self, tension: Tension,
                                      requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Tạo solutions cho trend analysis"""
        return [
            {
                "title": "Trend Analysis & Forecasting System",
                "description": "Implement comprehensive trend analysis với forecasting capabilities",
                "approach": "Time Series Analysis & Machine Learning",
                "steps": [
                    "Collect và prepare historical time series data",
                    "Apply time series analysis techniques",
                    "Develop forecasting models (ARIMA, Prophet, etc.)",
                    "Create trend visualization dashboards",
                    "Setup automated forecasting reports"
                ],
                "tools": ["time_series_analysis", "forecasting_models", "trend_visualization"],
                "deliverables": ["Trend Analysis Report", "Forecasting Models", "Prediction Dashboard"],
                "timeline": "4-5 weeks",
                "priority": 1
            }
        ]
    
    async def _generate_reporting_solutions(self, tension: Tension,
                                          requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Tạo solutions cho reporting needs"""
        return [
            {
                "title": "Automated Reporting System",
                "description": "Thiết lập hệ thống báo cáo tự động với customizable templates",
                "approach": "Template-based Automated Reporting",
                "steps": [
                    "Analyze reporting requirements và stakeholder needs",
                    "Design flexible report templates",
                    "Implement automated data collection và processing",
                    "Create scheduling system cho regular reports",
                    "Setup distribution mechanism cho stakeholders"
                ],
                "tools": ["report_generator", "template_engine", "scheduler"],
                "deliverables": ["Report Templates", "Automation System", "Distribution Setup"],
                "timeline": "2-3 weeks",
                "priority": 1
            }
        ]
    
    async def _generate_generic_data_solutions(self, tension: Tension,
                                             requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Tạo generic data solutions"""
        return [
            {
                "title": "Data Analysis & Insights Discovery",
                "description": "Comprehensive data analysis để discover actionable insights",
                "approach": "Exploratory Data Analysis",
                "steps": [
                    "Perform exploratory data analysis",
                    "Apply statistical methods để find patterns",
                    "Create data visualizations",
                    "Generate insights report",
                    "Present findings to stakeholders"
                ],
                "tools": ["data_analysis", "visualization", "statistical_methods"],
                "deliverables": ["Analysis Report", "Visualizations", "Insights Summary"],
                "timeline": "2-3 weeks",
                "priority": 1
            }
        ]
    
    async def execute_solution(self, solution: Dict[str, Any], 
                             context: Dict[str, Any]) -> Dict[str, Any]:
        """Thực thi data analysis solution"""
        execution_result = {
            "status": "completed",
            "execution_time": datetime.now().isoformat(),
            "results": {},
            "deliverables_created": [],
            "next_steps": []
        }
        
        try:
            solution_title = solution.get("title", "Unknown Solution")
            self.logger.info(f"Executing data solution: {solution_title}")
            
            # Simulate solution execution
            await asyncio.sleep(1)  # Simulate processing time
            
            # Mock results based on solution type
            if "quality" in solution_title.lower():
                execution_result["results"] = {
                    "data_quality_score": 85.2,
                    "issues_found": 127,
                    "issues_resolved": 89,
                    "improvement_percentage": 15.3
                }
                execution_result["deliverables_created"] = ["Data Quality Report", "Cleanup Scripts"]
                
            elif "performance" in solution_title.lower():
                execution_result["results"] = {
                    "metrics_tracked": 25,
                    "performance_improvement": 12.7,
                    "alerts_configured": 8,
                    "dashboard_views": 15
                }
                execution_result["deliverables_created"] = ["Performance Dashboard", "Metrics Setup"]
                
            elif "trend" in solution_title.lower():
                execution_result["results"] = {
                    "trends_identified": 7,
                    "forecast_accuracy": 78.5,
                    "prediction_horizon": "3 months",
                    "confidence_level": 85.0
                }
                execution_result["deliverables_created"] = ["Trend Analysis Report", "Forecasting Models"]
                
            else:
                execution_result["results"] = {
                    "insights_discovered": 12,
                    "recommendations_generated": 8,
                    "stakeholder_satisfaction": 4.2,
                    "data_coverage": 95.0
                }
                execution_result["deliverables_created"] = ["Analysis Report", "Insights Dashboard"]
            
            execution_result["next_steps"] = [
                "Review results with stakeholders",
                "Implement recommended improvements",
                "Setup ongoing monitoring",
                "Schedule follow-up analysis"
            ]
            
            self.logger.info(f"Successfully executed solution: {solution_title}")
            
        except Exception as e:
            execution_result["status"] = "failed"
            execution_result["error"] = str(e)
            self.logger.error(f"Error executing solution: {str(e)}")
        
        return execution_result
    
    async def _register_specialized_handlers(self) -> None:
        """Đăng ký specialized event handlers cho DataAnalyst"""
        # Đăng ký events liên quan đến data
        self.subscribe_to_event(EventType.DATA_UPDATED)
        self.subscribe_to_event(EventType.REPORT_REQUESTED)
        
    async def _initialize_specialized_components(self) -> None:
        """Khởi tạo data analysis components"""
        self.logger.info("Initializing DataAnalyst specialized components")
        
        # Initialize data connections, analysis tools, etc.
        # This would be implemented based on actual infrastructure
        
    async def _handle_specialized_event(self, event: SystemEvent) -> None:
        """Xử lý specialized events cho DataAnalyst"""
        if event.event_type == EventType.DATA_UPDATED:
            await self._handle_data_updated(event)
        elif event.event_type == EventType.REPORT_REQUESTED:
            await self._handle_report_requested(event)
    
    async def _handle_data_updated(self, event: SystemEvent) -> None:
        """Xử lý sự kiện data được cập nhật"""
        self.logger.info(f"Data updated event received: {event.entity_id}")
        # Implement data update handling logic
        
    async def _handle_report_requested(self, event: SystemEvent) -> None:
        """Xử lý sự kiện yêu cầu báo cáo"""
        self.logger.info(f"Report requested: {event.entity_id}")
        # Implement report generation logic 