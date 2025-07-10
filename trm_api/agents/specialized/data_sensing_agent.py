#!/usr/bin/env python3
"""
DataSensing Agent - MCP Database Access
Theo AGE_COMPREHENSIVE_SYSTEM_DESIGN_V2.md: Specialized Agents - CrewAI Integration

Purpose: MCP Database Access với universal data sensing capabilities
Philosophy: Recognition → Event → WIN through intelligent data discovery
"""

import asyncio
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, field
from enum import Enum
import json

from trm_api.services.mcp_service import get_mcp_coordinator, MCPResourceType
from trm_api.protocols.mcp_connectors.mcp_connector_registry import get_mcp_registry
from trm_api.core.commercial_ai_coordinator import get_commercial_ai_coordinator, TaskType
from trm_api.core.logging_config import get_logger
from trm_api.eventbus.system_event_bus import SystemEventBus, EventType

logger = get_logger(__name__)


class DataSensingType(str, Enum):
    """Types of data sensing operations"""
    PATTERN_DETECTION = "pattern_detection"
    ANOMALY_DISCOVERY = "anomaly_discovery"
    CORRELATION_ANALYSIS = "correlation_analysis"
    TREND_IDENTIFICATION = "trend_identification"
    RELATIONSHIP_MAPPING = "relationship_mapping"
    KNOWLEDGE_EXTRACTION = "knowledge_extraction"


@dataclass
class DataSensingRequest:
    """Request for data sensing operation"""
    request_id: str
    sensing_type: DataSensingType
    target_platforms: List[str] = field(default_factory=lambda: ["supabase", "neo4j"])
    query_intent: str = ""
    context: Dict[str, Any] = field(default_factory=dict)
    depth_level: int = 1  # 1=surface, 5=deep analysis
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class DataSensingResult:
    """Result from data sensing operation"""
    request_id: str
    patterns_discovered: List[Dict[str, Any]]
    insights_generated: Dict[str, Any]
    data_sources_accessed: List[str]
    confidence_score: float
    recommendations: List[str]
    execution_time_seconds: float
    timestamp: datetime = field(default_factory=datetime.now)


class DataSensingAgent:
    """
    DataSensing Agent - Specialized AI Agent for MCP Database Access
    
    Capabilities:
    - Universal data access via MCP protocol
    - Pattern recognition across multiple data sources
    - Intelligent data correlation và analysis
    - Commercial AI-guided data insights
    - Real-time anomaly detection
    """
    
    def __init__(self):
        self.agent_id = "data_sensing_agent"
        self.agent_name = "DataSensing Agent"
        self.logger = get_logger(f"agents.{self.agent_id}")
        self.event_bus = SystemEventBus()
        
        # MCP integration
        self.mcp_coordinator = None
        self.mcp_registry = None
        
        # Commercial AI integration
        self.commercial_ai_coordinator = None
        
        # Agent capabilities
        self.capabilities = [
            "mcp_database_access",
            "pattern_detection",
            "anomaly_discovery", 
            "cross_platform_correlation",
            "ai_guided_insights",
            "real_time_monitoring"
        ]
        
        # Statistics
        self.stats = {
            "total_requests": 0,
            "patterns_discovered": 0,
            "platforms_accessed": 0,
            "avg_confidence": 0.0,
            "avg_execution_time": 0.0
        }
        
        self.logger.info(f"DataSensing Agent initialized - ID: {self.agent_id}")
    
    async def initialize(self) -> bool:
        """Initialize DataSensing Agent components"""
        try:
            self.logger.info("Initializing DataSensing Agent...")
            
            # Initialize MCP components
            self.mcp_coordinator = await get_mcp_coordinator()
            self.mcp_registry = get_mcp_registry()
            self.logger.info("✅ MCP components initialized")
            
            # Initialize Commercial AI
            self.commercial_ai_coordinator = await get_commercial_ai_coordinator()
            if self.commercial_ai_coordinator:
                await self.commercial_ai_coordinator.initialize()
                self.logger.info("✅ Commercial AI coordinator initialized")
            
            # Publish agent ready event
            await self.event_bus.publish_event(
                event_type=EventType.AGENT_READY,
                data={
                    "agent_id": self.agent_id,
                    "agent_name": self.agent_name,
                    "capabilities": self.capabilities,
                    "mcp_enabled": self.mcp_coordinator is not None,
                    "ai_enabled": self.commercial_ai_coordinator is not None
                }
            )
            
            self.logger.info("🎯 DataSensing Agent ready for intelligent data operations")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize DataSensing Agent: {e}")
            return False
    
    async def sense_data(self, request: DataSensingRequest) -> DataSensingResult:
        """
        Core data sensing operation: Recognition → Event → WIN
        Intelligent data discovery across MCP-connected platforms
        """
        start_time = datetime.now()
        self.stats["total_requests"] += 1
        
        try:
            self.logger.info(f"🔍 Data sensing: {request.sensing_type} on {request.target_platforms}")
            
            # RECOGNITION PHASE: Analyze sensing intent
            recognition_result = await self._recognize_data_intent(request)
            
            # EVENT PHASE: Execute data sensing across platforms
            sensing_result = await self._execute_data_sensing(request, recognition_result)
            
            # WIN PHASE: Generate insights và recommendations
            insights_result = await self._generate_insights(request, sensing_result)
            
            # Calculate metrics
            execution_time = (datetime.now() - start_time).total_seconds()
            confidence_score = self._calculate_confidence(recognition_result, sensing_result, insights_result)
            
            # Update statistics
            self.stats["patterns_discovered"] += len(insights_result.get("patterns", []))
            self.stats["platforms_accessed"] += len(sensing_result.get("platforms_accessed", []))
            self.stats["avg_execution_time"] = (
                (self.stats["avg_execution_time"] * (self.stats["total_requests"] - 1) + execution_time) 
                / self.stats["total_requests"]
            )
            
            result = DataSensingResult(
                request_id=request.request_id,
                patterns_discovered=insights_result.get("patterns", []),
                insights_generated=insights_result.get("insights", {}),
                data_sources_accessed=sensing_result.get("platforms_accessed", []),
                confidence_score=confidence_score,
                recommendations=insights_result.get("recommendations", []),
                execution_time_seconds=execution_time
            )
            
            # Publish completion event
            await self.event_bus.publish_event(
                event_type=EventType.DATA_SENSING_COMPLETE,
                data={
                    "agent_id": self.agent_id,
                    "request_id": request.request_id,
                    "patterns_found": len(result.patterns_discovered),
                    "confidence": confidence_score,
                    "platforms_accessed": result.data_sources_accessed
                }
            )
            
            self.logger.info(f"✅ Data sensing complete - {len(result.patterns_discovered)} patterns discovered")
            return result
            
        except Exception as e:
            self.logger.error(f"Data sensing failed: {e}")
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return DataSensingResult(
                request_id=request.request_id,
                patterns_discovered=[],
                insights_generated={"error": str(e)},
                data_sources_accessed=[],
                confidence_score=0.0,
                recommendations=[],
                execution_time_seconds=execution_time
            )
    
    async def _recognize_data_intent(self, request: DataSensingRequest) -> Dict[str, Any]:
        """RECOGNITION: Analyze data sensing intent với Commercial AI guidance"""
        self.logger.info("🔍 RECOGNITION: Analyzing data sensing intent...")
        
        recognition_result = {
            "intent_analysis": {},
            "optimal_strategies": [],
            "platform_prioritization": {},
            "confidence": 0.0
        }
        
        try:
            if self.commercial_ai_coordinator:
                analysis_prompt = f"""
                Analyze data sensing request for AGE DataSensing Agent:
                
                Sensing Type: {request.sensing_type}
                Target Platforms: {request.target_platforms}
                Query Intent: {request.query_intent}
                Context: {json.dumps(request.context, indent=2)}
                Depth Level: {request.depth_level}/5
                
                Provide strategic analysis:
                1. Data sensing strategy recommendations
                2. Platform access optimization
                3. Pattern detection approaches
                4. Expected data insights
                5. Risk assessment và mitigation
                """
                
                ai_analysis = await self.commercial_ai_coordinator.process_request(
                    content=analysis_prompt,
                    task_type=TaskType.ANALYSIS,
                    context={"agent": "data_sensing", "operation": "recognition"}
                )
                
                recognition_result["intent_analysis"] = ai_analysis.content
                recognition_result["confidence"] = ai_analysis.confidence_score
            
            # Generate optimal sensing strategies
            recognition_result["optimal_strategies"] = self._generate_sensing_strategies(request)
            
            # Prioritize platforms based on sensing type
            recognition_result["platform_prioritization"] = self._prioritize_platforms(request)
            
            return recognition_result
            
        except Exception as e:
            self.logger.error(f"Recognition phase failed: {e}")
            recognition_result["error"] = str(e)
            return recognition_result
    
    async def _execute_data_sensing(self, request: DataSensingRequest, recognition: Dict[str, Any]) -> Dict[str, Any]:
        """EVENT: Execute data sensing operations across MCP platforms"""
        self.logger.info("⚡ EVENT: Executing data sensing operations...")
        
        sensing_result = {
            "platforms_accessed": [],
            "data_collected": {},
            "patterns_raw": [],
            "anomalies_detected": [],
            "success_rate": 0.0
        }
        
        try:
            # Access data from prioritized platforms
            platform_priority = recognition.get("platform_prioritization", {})
            
            for platform in request.target_platforms:
                try:
                    platform_data = await self._access_platform_data(platform, request)
                    sensing_result["data_collected"][platform] = platform_data
                    sensing_result["platforms_accessed"].append(platform)
                    
                    # Detect patterns in platform data
                    platform_patterns = await self._detect_platform_patterns(platform, platform_data, request)
                    sensing_result["patterns_raw"].extend(platform_patterns)
                    
                except Exception as e:
                    self.logger.warning(f"Failed to access {platform}: {e}")
            
            # Cross-platform correlation analysis
            if len(sensing_result["platforms_accessed"]) > 1:
                correlations = await self._analyze_cross_platform_correlations(sensing_result["data_collected"])
                sensing_result["patterns_raw"].extend(correlations)
            
            # Anomaly detection
            sensing_result["anomalies_detected"] = await self._detect_anomalies(sensing_result["data_collected"])
            
            # Calculate success rate
            sensing_result["success_rate"] = len(sensing_result["platforms_accessed"]) / len(request.target_platforms)
            
            return sensing_result
            
        except Exception as e:
            self.logger.error(f"Data sensing execution failed: {e}")
            sensing_result["error"] = str(e)
            return sensing_result
    
    async def _generate_insights(self, request: DataSensingRequest, sensing_data: Dict[str, Any]) -> Dict[str, Any]:
        """WIN: Generate actionable insights từ sensing data"""
        self.logger.info("🏆 WIN: Generating actionable insights...")
        
        insights_result = {
            "patterns": [],
            "insights": {},
            "recommendations": [],
            "strategic_value": 0.0
        }
        
        try:
            if self.commercial_ai_coordinator:
                insights_prompt = f"""
                Generate strategic insights from DataSensing Agent results:
                
                Platforms Accessed: {sensing_data.get('platforms_accessed', [])}
                Raw Patterns Found: {len(sensing_data.get('patterns_raw', []))}
                Anomalies Detected: {len(sensing_data.get('anomalies_detected', []))}
                Success Rate: {sensing_data.get('success_rate', 0):.2%}
                
                Data Summary: {json.dumps(sensing_data.get('data_collected', {}), default=str)[:1000]}...
                
                Provide:
                1. Key patterns và their strategic significance
                2. Actionable insights for decision making
                3. Recommendations for next steps
                4. Strategic value assessment (0-1 scale)
                5. Risk factors và opportunities
                """
                
                ai_insights = await self.commercial_ai_coordinator.process_request(
                    content=insights_prompt,
                    task_type=TaskType.ANALYSIS,
                    context={"agent": "data_sensing", "operation": "insight_generation"}
                )
                
                insights_result["insights"] = ai_insights.content
            
            # Process raw patterns into structured insights
            insights_result["patterns"] = self._structure_patterns(sensing_data.get("patterns_raw", []))
            
            # Generate specific recommendations
            insights_result["recommendations"] = self._generate_recommendations(request, sensing_data)
            
            # Calculate strategic value
            insights_result["strategic_value"] = self._calculate_strategic_value(sensing_data)
            
            return insights_result
            
        except Exception as e:
            self.logger.error(f"Insight generation failed: {e}")
            insights_result["error"] = str(e)
            return insights_result
    
    async def _access_platform_data(self, platform: str, request: DataSensingRequest) -> Dict[str, Any]:
        """Access data from specific MCP platform"""
        if not self.mcp_coordinator:
            return {"error": "MCP coordinator not available"}
        
        try:
            # Example MCP data access - can be expanded based on platform
            platform_data = {
                "platform": platform,
                "query_intent": request.query_intent,
                "sensing_type": request.sensing_type.value,
                "timestamp": datetime.now().isoformat(),
                "data_points": [],
                "metadata": {}
            }
            
            # Platform-specific data access logic would go here
            if platform == "supabase":
                platform_data["data_points"] = await self._access_supabase_data(request)
            elif platform == "neo4j":
                platform_data["data_points"] = await self._access_neo4j_data(request)
            elif platform == "snowflake":
                platform_data["data_points"] = await self._access_snowflake_data(request)
            
            return platform_data
            
        except Exception as e:
            return {"platform": platform, "error": str(e)}
    
    async def _access_supabase_data(self, request: DataSensingRequest) -> List[Dict[str, Any]]:
        """Access Supabase data via MCP"""
        # Mock implementation - would use real MCP connector
        return [
            {"type": "user_activity", "value": "sample_data", "timestamp": datetime.now().isoformat()},
            {"type": "system_event", "value": "sample_event", "timestamp": datetime.now().isoformat()}
        ]
    
    async def _access_neo4j_data(self, request: DataSensingRequest) -> List[Dict[str, Any]]:
        """Access Neo4j data via MCP"""
        # Mock implementation - would use real MCP connector
        return [
            {"type": "relationship", "source": "agent", "target": "project", "strength": 0.8},
            {"type": "node_property", "node": "resource", "property": "utilization", "value": 0.75}
        ]
    
    async def _access_snowflake_data(self, request: DataSensingRequest) -> List[Dict[str, Any]]:
        """Access Snowflake data via MCP"""
        # Mock implementation - would use real MCP connector
        return [
            {"type": "analytics", "metric": "performance", "value": 0.92, "period": "daily"},
            {"type": "trend", "metric": "growth", "value": 0.15, "period": "monthly"}
        ]
    
    async def _detect_platform_patterns(self, platform: str, data: Dict[str, Any], request: DataSensingRequest) -> List[Dict[str, Any]]:
        """Detect patterns in platform-specific data"""
        patterns = []
        
        try:
            data_points = data.get("data_points", [])
            if len(data_points) > 1:
                pattern = {
                    "type": "data_volume_pattern",
                    "platform": platform,
                    "pattern": f"{len(data_points)} data points detected",
                    "confidence": 0.8,
                    "strategic_relevance": "medium"
                }
                patterns.append(pattern)
            
            return patterns
            
        except Exception as e:
            self.logger.warning(f"Pattern detection failed for {platform}: {e}")
            return []
    
    async def _analyze_cross_platform_correlations(self, platform_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze correlations across multiple platforms"""
        correlations = []
        
        try:
            platforms = list(platform_data.keys())
            if len(platforms) >= 2:
                correlation = {
                    "type": "cross_platform_correlation",
                    "platforms": platforms,
                    "correlation_strength": 0.7,
                    "insight": f"Data correlation detected between {platforms[0]} and {platforms[1]}",
                    "strategic_value": "high"
                }
                correlations.append(correlation)
            
            return correlations
            
        except Exception as e:
            self.logger.warning(f"Cross-platform correlation analysis failed: {e}")
            return []
    
    async def _detect_anomalies(self, platform_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Detect anomalies in collected data"""
        anomalies = []
        
        try:
            for platform, data in platform_data.items():
                if data.get("error"):
                    anomaly = {
                        "type": "platform_access_anomaly",
                        "platform": platform,
                        "description": f"Access error: {data['error']}",
                        "severity": "medium",
                        "requires_attention": True
                    }
                    anomalies.append(anomaly)
            
            return anomalies
            
        except Exception as e:
            self.logger.warning(f"Anomaly detection failed: {e}")
            return []
    
    def _generate_sensing_strategies(self, request: DataSensingRequest) -> List[str]:
        """Generate optimal sensing strategies based on request type"""
        strategies = []
        
        strategy_mapping = {
            DataSensingType.PATTERN_DETECTION: ["time_series_analysis", "frequency_analysis", "trend_detection"],
            DataSensingType.ANOMALY_DISCOVERY: ["statistical_outlier_detection", "behavioral_analysis"],
            DataSensingType.CORRELATION_ANALYSIS: ["cross_platform_correlation", "temporal_correlation"],
            DataSensingType.TREND_IDENTIFICATION: ["trend_analysis", "seasonal_decomposition"],
            DataSensingType.RELATIONSHIP_MAPPING: ["graph_analysis", "network_topology"],
            DataSensingType.KNOWLEDGE_EXTRACTION: ["semantic_analysis", "entity_extraction"]
        }
        
        return strategy_mapping.get(request.sensing_type, ["general_data_analysis"])
    
    def _prioritize_platforms(self, request: DataSensingRequest) -> Dict[str, int]:
        """Prioritize platforms based on sensing type"""
        # Priority: 1=highest, 5=lowest
        platform_priority = {}
        
        for platform in request.target_platforms:
            if request.sensing_type == DataSensingType.RELATIONSHIP_MAPPING and platform == "neo4j":
                platform_priority[platform] = 1
            elif request.sensing_type == DataSensingType.TREND_IDENTIFICATION and platform == "snowflake":
                platform_priority[platform] = 1
            else:
                platform_priority[platform] = 3  # Default priority
        
        return platform_priority
    
    def _structure_patterns(self, raw_patterns: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Structure raw patterns into actionable insights"""
        structured = []
        
        for pattern in raw_patterns:
            structured_pattern = {
                "id": f"pattern_{len(structured)}",
                "type": pattern.get("type", "unknown"),
                "confidence": pattern.get("confidence", 0.5),
                "strategic_relevance": pattern.get("strategic_relevance", "medium"),
                "description": pattern.get("pattern", pattern.get("insight", "Pattern detected")),
                "source_platforms": [pattern.get("platform", "unknown")],
                "actionable": True
            }
            structured.append(structured_pattern)
        
        return structured
    
    def _generate_recommendations(self, request: DataSensingRequest, sensing_data: Dict[str, Any]) -> List[str]:
        """Generate actionable recommendations based on sensing results"""
        recommendations = []
        
        success_rate = sensing_data.get("success_rate", 0)
        patterns_found = len(sensing_data.get("patterns_raw", []))
        
        if success_rate < 0.5:
            recommendations.append("Consider improving MCP connector reliability for better data access")
        
        if patterns_found > 5:
            recommendations.append("High pattern density detected - consider deeper analysis with increased depth level")
        
        if len(sensing_data.get("anomalies_detected", [])) > 0:
            recommendations.append("Anomalies detected - recommend immediate investigation")
        
        recommendations.append(f"Expand sensing to additional platforms for {request.sensing_type} analysis")
        
        return recommendations
    
    def _calculate_strategic_value(self, sensing_data: Dict[str, Any]) -> float:
        """Calculate strategic value of sensing results"""
        success_rate = sensing_data.get("success_rate", 0)
        patterns_count = len(sensing_data.get("patterns_raw", []))
        platforms_count = len(sensing_data.get("platforms_accessed", []))
        
        # Strategic value formula
        value = (success_rate * 0.4 + 
                min(patterns_count / 10, 1.0) * 0.4 + 
                min(platforms_count / 3, 1.0) * 0.2)
        
        return round(value, 2)
    
    def _calculate_confidence(self, recognition: Dict[str, Any], sensing: Dict[str, Any], insights: Dict[str, Any]) -> float:
        """Calculate overall confidence score"""
        recognition_confidence = recognition.get("confidence", 0.0)
        sensing_success = sensing.get("success_rate", 0.0)
        insights_value = insights.get("strategic_value", 0.0)
        
        return (recognition_confidence * 0.3 + sensing_success * 0.4 + insights_value * 0.3)
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get agent status và statistics"""
        return {
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "capabilities": self.capabilities,
            "stats": self.stats,
            "mcp_enabled": self.mcp_coordinator is not None,
            "ai_enabled": self.commercial_ai_coordinator is not None,
            "status": "ready"
        }


# Global DataSensing Agent instance
_data_sensing_agent: Optional[DataSensingAgent] = None

async def get_data_sensing_agent() -> DataSensingAgent:
    """Get DataSensing Agent singleton"""
    global _data_sensing_agent
    if _data_sensing_agent is None:
        _data_sensing_agent = DataSensingAgent()
        await _data_sensing_agent.initialize()
    return _data_sensing_agent 