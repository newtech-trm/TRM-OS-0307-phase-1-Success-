"""
Data Analyst Agent Template

Agent chuyên biệt xử lý các tensions liên quan đến data analysis, data processing,
reporting và business intelligence trong TRM-OS.
"""

import re
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

from trm_api.agents.templates.base_template import BaseAgentTemplate
from trm_api.agents.base_agent import AgentMetadata
from trm_api.models.agent_template import AgentTemplateMetadata, AgentCapability
from trm_api.models.tension import Tension
from trm_api.models.enums import TensionType, Priority
from trm_api.eventbus.system_event_bus import SystemEvent, EventType


class DataAnalystAgent(BaseAgentTemplate):
    """
    Specialized agent template for data analysis tasks.
    
    Tuân thủ đầy đủ triết lý TRM-OS:
    - Tension-based operation với proper enum handling
    - WIN optimization trong mọi quyết định
    - Quantum Operating Model implementation
    - Strategic alignment với domain expertise
    """
    
    def __init__(self, agent_id: Optional[str] = None):
        # Define capabilities trước khi gọi super().__init__()
        capabilities = [
            AgentCapability(
                name="statistical_analysis",
                description="Perform comprehensive statistical analysis including descriptive stats, hypothesis testing, and advanced modeling",
                proficiency_level=0.95,
                estimated_time_per_task=45.0,
                related_tension_types=[TensionType.DATA_ANALYSIS, TensionType.PROCESS_IMPROVEMENT]
            ),
            AgentCapability(
                name="data_visualization",
                description="Create compelling data visualizations and interactive dashboards",
                proficiency_level=0.90,
                estimated_time_per_task=30.0,
                related_tension_types=[TensionType.DATA_ANALYSIS, TensionType.COMMUNICATION_BREAKDOWN]
            ),
            AgentCapability(
                name="business_intelligence",
                description="Transform data into actionable business insights and strategic recommendations",
                proficiency_level=0.88,
                estimated_time_per_task=60.0,
                related_tension_types=[TensionType.DATA_ANALYSIS, TensionType.PROCESS_IMPROVEMENT, TensionType.RESOURCE_CONSTRAINT]
            ),
            AgentCapability(
                name="predictive_modeling",
                description="Build and validate predictive models for forecasting and trend analysis",
                proficiency_level=0.85,
                estimated_time_per_task=120.0,
                related_tension_types=[TensionType.DATA_ANALYSIS, TensionType.OPPORTUNITY]
            ),
            AgentCapability(
                name="data_quality_assessment",
                description="Assess and improve data quality, identify anomalies and inconsistencies",
                proficiency_level=0.92,
                estimated_time_per_task=25.0,
                related_tension_types=[TensionType.DATA_ANALYSIS, TensionType.TECHNICAL_DEBT, TensionType.PROCESS_IMPROVEMENT]
            )
        ]
        
        # Store capabilities as instance attribute
        self.capabilities = capabilities
        
        # Create template metadata với comprehensive configuration
        template_metadata = AgentTemplateMetadata(
            template_name="DataAnalystAgent",
            primary_domain="data",
            capabilities=capabilities,
            domain_expertise=["statistics", "business_intelligence", "data_science", "reporting"],
            supported_tension_types=[
                TensionType.DATA_ANALYSIS,
                TensionType.RESOURCE_CONSTRAINT,
                TensionType.PROCESS_IMPROVEMENT
            ],
            performance_metrics={
                "accuracy": 0.92,
                "efficiency": 0.88,
                "user_satisfaction": 0.90
            },
            version="2.0.0"
        )
        
        super().__init__(agent_id=agent_id, template_metadata=template_metadata)
        
        # Specialized components for data analysis
        self.analysis_tools = {
            "statistical_tests": ["t_test", "chi_square", "anova", "regression"],
            "visualization_types": ["histogram", "scatter", "line", "heatmap", "box_plot"],
            "modeling_algorithms": ["linear_regression", "random_forest", "clustering", "time_series"]
        }
        
        self.domain_knowledge = {
            "business_metrics": ["revenue", "conversion_rate", "churn", "cac", "ltv"],
            "statistical_concepts": ["correlation", "causation", "significance", "confidence_interval"],
            "data_types": ["numerical", "categorical", "time_series", "text", "geospatial"]
        }
    
    def _get_default_template_metadata(self) -> AgentTemplateMetadata:
        """Return default template metadata for DataAnalystAgent"""
        capabilities = [
            AgentCapability(
                name="statistical_analysis",
                description="Advanced statistical analysis",
                proficiency_level=0.9,
                estimated_time_per_task=30.0
            )
        ]
        
        return AgentTemplateMetadata(
            template_name="DataAnalystAgent",
            primary_domain="data", 
            capabilities=capabilities,
            domain_expertise=["statistics", "data_science"],
            supported_tension_types=[TensionType.DATA_ANALYSIS],
            performance_metrics={"accuracy": 0.9},
            version="2.0.0",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
    
    async def can_handle_tension(self, tension: Tension) -> bool:
        """
        Đánh giá khả năng xử lý tension theo triết lý TRM-OS.
        Sử dụng proper enum comparison và WIN optimization.
        """
        try:
            # Kiểm tra tension type với proper enum handling
            if not tension.tensionType:
                self.logger.warning(f"Tension {tension.tensionId} has no tensionType")
                return False
            
            # Data Analyst có thể handle các tension types sau
            supported_types = [
                TensionType.DATA_ANALYSIS,
                TensionType.RESOURCE_CONSTRAINT,  # Nếu liên quan đến data resources
                TensionType.PROCESS_IMPROVEMENT   # Nếu cần data-driven insights
            ]
            
            # Primary capability check
            if tension.tensionType not in supported_types:
                self.logger.debug(f"Tension type {tension.tensionType} not in supported types")
                return False
            
            # Sử dụng quantum model để assess fit
            can_handle = await super().can_handle_tension(tension)
            
            # Additional domain-specific checks
            if can_handle and tension.description:
                description_lower = tension.description.lower()
                
                # Check for data-related keywords (English and Vietnamese)
                data_keywords = ["data", "analysis", "statistics", "report", "dashboard", 
                               "metrics", "kpi", "trend", "pattern", "insight",
                               "dữ liệu", "phân tích", "thống kê", "báo cáo", "biểu đồ",
                               "chỉ số", "xu hướng", "mẫu", "thông tin"]
                
                keyword_match = any(keyword in description_lower for keyword in data_keywords)
                
                if not keyword_match:
                    self.logger.debug(f"No data-related keywords found in tension description")
                    can_handle = False
                
                # Assess complexity và WIN potential
                if can_handle:
                    complexity = self._assess_data_complexity(tension)
                    win_potential = self._calculate_win_potential(tension, complexity)
                    
                    # Only handle if WIN potential >= 60
                    if win_potential < 60.0:
                        self.logger.info(f"WIN potential {win_potential} below threshold for tension {tension.tensionId}")
                        can_handle = False
                    else:
                        self.logger.info(f"DataAnalyst can handle tension {tension.tensionId} with WIN potential {win_potential}")
            
            return can_handle
            
        except Exception as e:
            self.logger.error(f"Error in can_handle_tension: {e}")
            return False
    
    def _assess_data_complexity(self, tension: Tension) -> str:
        """Assess complexity of data analysis required"""
        if not tension.description:
            return "low"
        
        description = tension.description.lower()
        
        # High complexity indicators
        high_complexity_keywords = [
            "machine learning", "predictive model", "advanced analytics", 
            "statistical modeling", "multivariate", "time series forecasting"
        ]
        
        # Medium complexity indicators  
        medium_complexity_keywords = [
            "correlation analysis", "regression", "segmentation",
            "a/b test", "statistical test", "trend analysis"
        ]
        
        if any(keyword in description for keyword in high_complexity_keywords):
            return "high"
        elif any(keyword in description for keyword in medium_complexity_keywords):
            return "medium"
        else:
            return "low"
    
    def _calculate_win_potential(self, tension: Tension, complexity: str) -> float:
        """Calculate potential WIN score for this tension"""
        base_score = 50.0
        
        # Wisdom component (understanding business context)
        wisdom_score = 70.0
        if tension.priority == Priority.HIGH:
            wisdom_score += 15.0
        elif tension.priority == Priority.CRITICAL:
            wisdom_score += 25.0
        
        # Intelligence component (technical capability match)
        intelligence_score = 80.0  # Base data analysis capability
        if complexity == "high":
            intelligence_score += 10.0  # Challenging problems = higher intelligence demonstration
        elif complexity == "low":
            intelligence_score -= 10.0
        
        # Networking component (collaboration potential)
        networking_score = 60.0
        if tension.description and ("stakeholder" in tension.description.lower() or 
                                   "business" in tension.description.lower()):
            networking_score += 20.0
        
        # Calculate total WIN using TRM-OS formula
        total_win = (wisdom_score * 0.4 + intelligence_score * 0.4 + networking_score * 0.2)
        
        return min(100.0, max(0.0, total_win))
    
    async def analyze_tension_requirements(self, tension: Tension) -> Dict[str, Any]:
        """
        Analyze data analysis requirements for the tension.
        Extends base quantum model với domain-specific analysis.
        """
        # Get base requirements from quantum model
        base_requirements = await super().analyze_tension_requirements(tension)
        
        # Add data-specific requirements
        data_requirements = {
            "data_sources_needed": self._identify_data_sources(tension),
            "analysis_type": self._determine_analysis_type(tension),
            "deliverables": self._define_deliverables(tension),
            "tools_required": self._select_analysis_tools(tension),
            "estimated_timeline": self._estimate_timeline(tension),
            "estimated_effort": self._estimate_timeline(tension).get("hours", 24),  # Convert to numeric for tests
            "success_criteria": self._define_success_criteria(tension),
            "stakeholders": self._identify_stakeholders(tension)
        }
        
        # Merge với base requirements
        base_requirements.update(data_requirements)
        
        return base_requirements
    
    def _identify_data_sources(self, tension: Tension) -> List[str]:
        """Identify required data sources"""
        sources = ["database", "analytics_platform"]
        
        if tension.description:
            desc = tension.description.lower()
            if "sales" in desc:
                sources.append("crm_system")
            if "user" in desc or "customer" in desc:
                sources.append("user_analytics")
            if "financial" in desc:
                sources.append("financial_system")
            if "marketing" in desc:
                sources.append("marketing_platform")
        
        return sources
    
    def _determine_analysis_type(self, tension: Tension) -> str:
        """Determine type of analysis needed with intelligent keyword matching"""
        if not tension.description:
            return "descriptive"
        
        desc = tension.description.lower()
        
        # Performance analysis keywords (English and Vietnamese)
        performance_keywords = ["performance", "metrics", "kpi", "dashboard", "monitor", 
                              "hiệu suất", "chỉ số", "đo lường", "theo dõi", "giám sát"]
        
        # Predictive analysis keywords
        predictive_keywords = ["predict", "forecast", "future", "model", "trend", "projection",
                             "dự đoán", "dự báo", "tương lai", "mô hình", "xu hướng"]
        
        # Diagnostic analysis keywords  
        diagnostic_keywords = ["why", "cause", "impact", "effect", "root cause", "analysis",
                             "tại sao", "nguyên nhân", "ảnh hưởng", "tác động", "phân tích"]
        
        # Prescriptive analysis keywords
        prescriptive_keywords = ["recommend", "optimize", "should", "best", "improve", "solution",
                               "khuyến nghị", "tối ưu", "nên", "tốt nhất", "cải thiện", "giải pháp"]
        
        # Check for specific analysis types
        if any(keyword in desc for keyword in performance_keywords):
            return "performance_analysis"
        elif any(keyword in desc for keyword in predictive_keywords):
            return "predictive"
        elif any(keyword in desc for keyword in diagnostic_keywords):
            return "diagnostic"
        elif any(keyword in desc for keyword in prescriptive_keywords):
            return "prescriptive"
        else:
            return "descriptive"
    
    def _define_deliverables(self, tension: Tension) -> List[str]:
        """Define expected deliverables with intelligent content-based determination"""
        deliverables = ["analysis_report", "data_insights"]
        
        if tension.description:
            desc = tension.description.lower()
            
            # Performance analysis deliverables
            if any(keyword in desc for keyword in ["performance", "metrics", "kpi", "hiệu suất", "chỉ số"]):
                deliverables.append("Performance Dashboard")
                deliverables.append("performance_metrics_report")
            
            # Dashboard/visualization deliverables
            if "dashboard" in desc or "visualization" in desc or "biểu đồ" in desc:
                deliverables.append("interactive_dashboard")
            
            # Presentation deliverables
            if "presentation" in desc or "báo cáo" in desc or "management" in desc:
                deliverables.append("executive_presentation")
            
            # Recommendation deliverables
            if "recommendation" in desc or "khuyến nghị" in desc or "solution" in desc:
                deliverables.append("action_recommendations")
            
            # Quality assessment deliverables
            if "quality" in desc or "cleanup" in desc or "chất lượng" in desc:
                deliverables.append("data_quality_report")
                deliverables.append("cleanup_recommendations")
        
        return deliverables
    
    def _select_analysis_tools(self, tension: Tension) -> List[str]:
        """Select appropriate analysis tools"""
        tools = ["statistical_analysis"]
        
        complexity = self._assess_data_complexity(tension)
        
        if complexity == "high":
            tools.extend(["machine_learning", "advanced_modeling"])
        elif complexity == "medium":
            tools.extend(["regression_analysis", "segmentation"])
        
        tools.append("data_visualization")
        return tools
    
    def _estimate_timeline(self, tension: Tension) -> Dict[str, Any]:
        """Estimate project timeline"""
        complexity = self._assess_data_complexity(tension)
        
        timeline_map = {
            "low": {"days": 3, "hours": 24},
            "medium": {"days": 7, "hours": 56}, 
            "high": {"days": 14, "hours": 112}
        }
        
        base_timeline = timeline_map.get(complexity, timeline_map["medium"])
        
        # Adjust based on priority
        if tension.priority == Priority.CRITICAL:
            base_timeline["days"] = int(base_timeline["days"] * 0.7)  # Rush job
            base_timeline["hours"] = int(base_timeline["hours"] * 0.7)
        
        return base_timeline
    
    def _define_success_criteria(self, tension: Tension) -> List[str]:
        """Define success criteria for the analysis"""
        criteria = [
            "actionable_insights_generated",
            "stakeholder_questions_answered",
            "data_quality_validated"
        ]
        
        if tension.priority in [Priority.HIGH, Priority.CRITICAL]:
            criteria.append("business_impact_quantified")
        
        return criteria
    
    def _identify_stakeholders(self, tension: Tension) -> List[str]:
        """Identify key stakeholders"""
        stakeholders = ["data_requester"]
        
        if tension.description:
            desc = tension.description.lower()
            if "executive" in desc or "management" in desc:
                stakeholders.append("executive_team")
            if "business" in desc:
                stakeholders.append("business_analysts")
            if "technical" in desc:
                stakeholders.append("technical_team")
        
        return stakeholders
    
    async def generate_specialized_solutions(self, tension: Tension, requirements: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Generate data analysis solutions optimized for WIN score.
        """
        if not requirements:
            requirements = await self.analyze_tension_requirements(tension)
        
        # Get base solutions from quantum model
        base_solutions = await super().generate_specialized_solutions(tension, requirements)
        
        # Enhance with data-specific solutions
        analysis_type = requirements.get("analysis_type", "descriptive")
        complexity = self._assess_data_complexity(tension)
        
        enhanced_solutions = []
        
        for solution in base_solutions:
            # Enhance base solution with data-specific details
            enhanced_solution = solution.copy()
            
            # Generate intelligent title based on analysis type and tension description
            if "quality" in tension.description.lower() or "cleanup" in tension.description.lower():
                enhanced_solution["title"] = "Data Quality Assessment & Improvement"
            elif analysis_type == "performance_analysis":
                enhanced_solution["title"] = "Performance Analytics Dashboard"
            elif analysis_type == "predictive":
                enhanced_solution["title"] = "Predictive Data Modeling"
            elif analysis_type == "diagnostic":
                enhanced_solution["title"] = "Root Cause Data Analysis"
            else:
                enhanced_solution["title"] = f"Comprehensive {analysis_type.title()} Analysis"
            
            enhanced_solution.update({
                "agent_template": "DataAnalystAgent",  # Add agent_template field for tests
                "analysis_approach": self._get_analysis_approach(analysis_type, complexity),
                "data_pipeline": self._design_data_pipeline(requirements),
                "visualization_strategy": self._design_visualization(requirements),
                "quality_assurance": self._define_qa_process(),
                "business_value": self._calculate_business_value(tension, complexity)
            })
            
            # Recalculate WIN score with domain expertise
            enhanced_solution["expected_win_score"] = self._calculate_enhanced_win_score(
                enhanced_solution, tension, requirements
            )
            
            enhanced_solutions.append(enhanced_solution)
        
        # Add specialized data analysis solution
        specialized_solution = {
            "id": f"data_solution_{tension.tensionId}_specialized",
            "type": "comprehensive_data_analysis",
            "agent_template": "DataAnalystAgent",  # Add agent_template field for tests
            "title": self._generate_solution_title(tension, analysis_type),  # Add intelligent title
            "description": f"Comprehensive {analysis_type} analysis with {complexity} complexity",
            "approach": "data_driven_insights",
            "analysis_methodology": self._get_analysis_methodology(analysis_type),
            "deliverables": requirements.get("deliverables", []),
            "timeline": requirements.get("estimated_timeline", {}),
            "tools": requirements.get("tools_required", []),
            "expected_win_score": self._calculate_specialized_win_score(tension, complexity),
            "confidence": 0.85,
            "business_impact": "high" if complexity == "high" else "medium",
            "risk_level": "low",
            "success_probability": 90.0
        }
        
        enhanced_solutions.append(specialized_solution)
        
        # Sort by WIN score descending
        enhanced_solutions.sort(key=lambda x: x.get("expected_win_score", 0), reverse=True)
        
        return enhanced_solutions
    
    def _get_analysis_approach(self, analysis_type: str, complexity: str) -> Dict[str, Any]:
        """Get detailed analysis approach"""
        approaches = {
            "descriptive": {
                "methods": ["summary_statistics", "data_profiling", "trend_analysis"],
                "focus": "understanding_current_state"
            },
            "diagnostic": {
                "methods": ["correlation_analysis", "root_cause_analysis", "comparative_analysis"], 
                "focus": "explaining_why_something_happened"
            },
            "predictive": {
                "methods": ["regression_modeling", "time_series_forecasting", "machine_learning"],
                "focus": "predicting_future_outcomes"
            },
            "prescriptive": {
                "methods": ["optimization_modeling", "simulation", "recommendation_engines"],
                "focus": "recommending_actions"
            }
        }
        
        approach = approaches.get(analysis_type, approaches["descriptive"])
        
        # Adjust based on complexity
        if complexity == "high":
            approach["methods"].append("advanced_statistical_modeling")
        elif complexity == "low":
            approach["methods"] = approach["methods"][:2]  # Simplify
        
        return approach
    
    def _design_data_pipeline(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Design data processing pipeline"""
        return {
            "data_sources": requirements.get("data_sources_needed", []),
            "extraction": "automated_etl",
            "transformation": ["data_cleaning", "feature_engineering", "normalization"],
            "validation": ["quality_checks", "completeness_validation", "consistency_checks"],
            "storage": "analytical_datastore"
        }
    
    def _design_visualization(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Design visualization strategy"""
        deliverables = requirements.get("deliverables", [])
        
        viz_strategy = {
            "chart_types": ["bar_chart", "line_chart", "scatter_plot"],
            "interactive_elements": False,
            "dashboard_required": False
        }
        
        if "interactive_dashboard" in deliverables:
            viz_strategy["interactive_elements"] = True
            viz_strategy["dashboard_required"] = True
            viz_strategy["chart_types"].extend(["heatmap", "treemap", "gauge"])
        
        return viz_strategy
    
    def _define_qa_process(self) -> Dict[str, Any]:
        """Define quality assurance process"""
        return {
            "data_validation": ["completeness", "accuracy", "consistency"],
            "analysis_review": ["methodology_check", "statistical_significance", "business_logic"],
            "output_verification": ["cross_validation", "peer_review", "stakeholder_feedback"]
        }
    
    def _calculate_business_value(self, tension: Tension, complexity: str) -> Dict[str, Any]:
        """Calculate expected business value"""
        base_value = 50000  # Base value in USD
        
        multipliers = {
            "low": 1.0,
            "medium": 2.0, 
            "high": 4.0
        }
        
        priority_multipliers = {
            Priority.LOW: 0.8,
            Priority.NORMAL: 1.0,
            Priority.HIGH: 1.5,
            Priority.CRITICAL: 2.0
        }
        
        estimated_value = (base_value * 
                          multipliers.get(complexity, 1.0) * 
                          priority_multipliers.get(tension.priority, 1.0))
        
        return {
            "estimated_value_usd": estimated_value,
            "value_drivers": ["improved_decision_making", "operational_efficiency", "risk_reduction"],
            "roi_timeframe": "3-6 months"
        }
    
    def _calculate_enhanced_win_score(self, solution: Dict[str, Any], tension: Tension, requirements: Dict[str, Any]) -> float:
        """Calculate enhanced WIN score with domain expertise"""
        base_score = solution.get("expected_win_score", 50.0)
        
        # Wisdom enhancement (domain knowledge application)
        wisdom_boost = 0.0
        if solution.get("business_value", {}).get("estimated_value_usd", 0) > 100000:
            wisdom_boost += 10.0
        
        # Intelligence enhancement (technical sophistication)
        intelligence_boost = 0.0
        if "advanced_statistical_modeling" in solution.get("analysis_approach", {}).get("methods", []):
            intelligence_boost += 15.0
        
        # Networking enhancement (stakeholder engagement)
        networking_boost = 0.0
        if len(requirements.get("stakeholders", [])) > 2:
            networking_boost += 10.0
        
        enhanced_score = base_score + (wisdom_boost * 0.4 + intelligence_boost * 0.4 + networking_boost * 0.2)
        
        return min(100.0, enhanced_score)
    
    def _calculate_specialized_win_score(self, tension: Tension, complexity: str) -> float:
        """Calculate WIN score for specialized data solution"""
        # Base score for data analysis expertise
        wisdom = 85.0  # Deep understanding of data and business context
        intelligence = 90.0  # Technical proficiency in data analysis
        networking = 75.0  # Collaboration with stakeholders
        
        # Adjust based on complexity
        complexity_multipliers = {
            "low": 0.9,
            "medium": 1.0,
            "high": 1.1
        }
        
        multiplier = complexity_multipliers.get(complexity, 1.0)
        
        total_win = ((wisdom * multiplier) * 0.4 + 
                    (intelligence * multiplier) * 0.4 + 
                    (networking * multiplier) * 0.2)
        
        return min(100.0, total_win)
    
    def _get_analysis_methodology(self, analysis_type: str) -> str:
        """Get detailed methodology for analysis type"""
        methodologies = {
            "descriptive": "Exploratory Data Analysis (EDA) with statistical summarization",
            "diagnostic": "Hypothesis-driven analysis with causal inference techniques",
            "predictive": "Machine learning pipeline with cross-validation and model selection",
            "prescriptive": "Optimization modeling with scenario analysis and sensitivity testing"
        }
        
        return methodologies.get(analysis_type, methodologies["descriptive"])
    
    async def _register_specialized_handlers(self) -> None:
        """Register data analysis specific event handlers"""
        # Subscribe to data-related events
        self.subscribe_to_event(EventType.DATA_UPDATED)
        self.subscribe_to_event(EventType.ANALYSIS_REQUESTED) 
        self.subscribe_to_event(EventType.REPORT_GENERATED)
    
    async def _initialize_specialized_components(self) -> None:
        """Initialize data analysis specific components"""
        self.logger.info(f"Initializing DataAnalyst specialized components for {self.agent_id}")
        
        # Initialize analysis tools
        self.analysis_tools["current_session"] = {
            "start_time": datetime.now(),
            "active_analyses": [],
            "completed_analyses": []
        }
        
        # Load domain knowledge
        self.domain_knowledge["session_context"] = {
            "preferred_tools": self.analysis_tools["statistical_tests"][:3],
            "default_visualizations": self.analysis_tools["visualization_types"][:4]
        }
    
    async def _handle_specialized_event(self, event: SystemEvent) -> None:
        """Handle data analysis specific events"""
        try:
            if event.event_type == EventType.DATA_UPDATED:
                await self._handle_data_updated(event)
            elif event.event_type == EventType.ANALYSIS_REQUESTED:
                await self._handle_analysis_requested(event)
            elif event.event_type == EventType.REPORT_GENERATED:
                await self._handle_report_generated(event)
            else:
                self.logger.debug(f"Unhandled specialized event: {event.event_type}")
                
        except Exception as e:
            self.logger.error(f"Error handling specialized event {event.event_type}: {e}")
    
    async def _handle_data_updated(self, event: SystemEvent) -> None:
        """Handle data update events"""
        self.logger.info(f"Data updated event received: {event.data}")
        
        # Check if any active analyses need to be refreshed
        active_analyses = self.analysis_tools["current_session"].get("active_analyses", [])
        
        for analysis in active_analyses:
            if analysis.get("data_source") == event.data.get("source"):
                self.logger.info(f"Refreshing analysis {analysis['id']} due to data update")
                # Trigger analysis refresh
                await self.send_event(
                    event_type=EventType.ANALYSIS_REFRESH_REQUESTED,
                    data={"analysis_id": analysis["id"], "reason": "data_updated"}
                )
    
    async def _handle_analysis_requested(self, event: SystemEvent) -> None:
        """Handle analysis request events"""
        self.logger.info(f"Analysis requested: {event.data}")
        
        # Create new analysis entry
        analysis_entry = {
            "id": f"analysis_{datetime.now().timestamp()}",
            "request_data": event.data,
            "status": "queued",
            "created_at": datetime.now()
        }
        
        self.analysis_tools["current_session"]["active_analyses"].append(analysis_entry)
        
        # Send acknowledgment
        await self.send_event(
            event_type=EventType.ANALYSIS_QUEUED,
            data={"analysis_id": analysis_entry["id"], "estimated_completion": "2-4 hours"}
        )
    
    async def _handle_report_generated(self, event: SystemEvent) -> None:
        """Handle report generation events"""
        self.logger.info(f"Report generated: {event.data}")
        
        # Move completed analysis to completed list
        analysis_id = event.data.get("analysis_id")
        active_analyses = self.analysis_tools["current_session"]["active_analyses"]
        
        for analysis in active_analyses[:]:  # Copy to avoid modification during iteration
            if analysis["id"] == analysis_id:
                analysis["status"] = "completed"
                analysis["completed_at"] = datetime.now()
                
                self.analysis_tools["current_session"]["completed_analyses"].append(analysis)
                active_analyses.remove(analysis)
                
                self.logger.info(f"Moved analysis {analysis_id} to completed")
                break 
    
    def _generate_solution_title(self, tension: Tension, analysis_type: str) -> str:
        """Generate intelligent solution title based on tension content and analysis type"""
        if not tension.description:
            return f"{analysis_type.title()} Analysis Solution"
        
        desc = tension.description.lower()
        
        # Quality-related solutions
        if "quality" in desc or "cleanup" in desc or "chất lượng" in desc:
            return "Data Quality Assessment & Improvement"
        
        # Performance-related solutions
        if "performance" in desc or "metrics" in desc or "hiệu suất" in desc:
            return "Performance Analytics Dashboard"
        
        # Reporting solutions
        if "report" in desc or "báo cáo" in desc or "management" in desc:
            return "Executive Data Reporting Solution"
        
        # Analysis type specific titles
        if analysis_type == "performance_analysis":
            return "Performance Analytics Dashboard"
        elif analysis_type == "predictive":
            return "Predictive Data Modeling Solution"
        elif analysis_type == "diagnostic":
            return "Root Cause Data Analysis"
        elif analysis_type == "prescriptive":
            return "Data-Driven Optimization Recommendations"
        else:
            return "Comprehensive Data Analysis Solution" 