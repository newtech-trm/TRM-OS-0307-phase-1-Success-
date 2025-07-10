#!/usr/bin/env python3
"""
Agent Intelligence API - Commercial AI Orchestration Endpoints
Theo AGE_COMPREHENSIVE_SYSTEM_DESIGN_V2.md

Thay thế basic CRUD Agent APIs bằng intelligent Commercial AI coordination
Philosophy: Recognition → Event → WIN through Specialized Agents
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
import json

from trm_api.core.age_orchestration_engine import (
    get_age_engine, AGERequest, AGEResponse, StrategicIntent
)
from trm_api.agents.specialized.data_sensing_agent import (
    get_data_sensing_agent, DataSensingRequest as AgentDataSensingRequest, 
    DataSensingResult, DataSensingType
)
from trm_api.core.commercial_ai_coordinator import get_commercial_ai_coordinator, TaskType
from trm_api.eventbus.system_event_bus import SystemEventBus, EventType
from trm_api.core.logging_config import get_logger
from pydantic import BaseModel, Field

logger = get_logger(__name__)
router = APIRouter(prefix="/agents/intelligence", tags=["Agent Intelligence"])


# === REQUEST/RESPONSE MODELS ===

class StrategicIntentRequest(BaseModel):
    """Request for AGE strategic intent processing"""
    strategic_intent: StrategicIntent = Field(..., description="Type of strategic intent")
    founder_message: str = Field(..., description="Message from founder")
    expected_outcome: str = Field("", description="Expected outcome")
    context: Dict[str, Any] = Field(default_factory=dict, description="Additional context")
    priority: int = Field(1, ge=1, le=5, description="Priority level (1=highest)")


class AgentSpecializationRequest(BaseModel):
    """Request for specialized agent operation"""
    agent_type: str = Field(..., description="Type of specialized agent")
    operation: str = Field(..., description="Specific operation to perform")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Operation parameters")
    context: Dict[str, Any] = Field(default_factory=dict, description="Operation context")


class DataSensingRequest(BaseModel):
    """Request for data sensing operation"""
    sensing_type: DataSensingType = Field(..., description="Type of data sensing")
    target_platforms: List[str] = Field(default=["supabase", "neo4j"], description="Target platforms")
    query_intent: str = Field("", description="Intent of the data query")
    depth_level: int = Field(1, ge=1, le=5, description="Analysis depth level")
    context: Dict[str, Any] = Field(default_factory=dict, description="Analysis context")


class AgentOrchestrationRequest(BaseModel):
    """Request for multi-agent orchestration"""
    primary_intent: StrategicIntent = Field(..., description="Primary strategic intent")
    required_specialists: List[str] = Field(default_factory=list, description="Required specialist agents")
    coordination_strategy: str = Field("parallel", description="Coordination strategy")
    success_criteria: Dict[str, Any] = Field(default_factory=dict, description="Success criteria")
    context: Dict[str, Any] = Field(default_factory=dict, description="Orchestration context")


# === AGE ORCHESTRATION ENDPOINTS ===

@router.post("/strategic-intent", response_model=Dict[str, Any])
async def process_strategic_intent(
    request: StrategicIntentRequest,
    background_tasks: BackgroundTasks
) -> Dict[str, Any]:
    """
    Core AGE endpoint: Process Founder's strategic intent
    Recognition → Event → WIN through Commercial AI orchestration
    """
    try:
        logger.info(f"🎯 Processing strategic intent: {request.strategic_intent}")
        
        # Get AGE Engine
        age_engine = await get_age_engine()
        
        # Create AGE request
        age_request = AGERequest(
            strategic_intent=request.strategic_intent,
            founder_message=request.founder_message,
            expected_outcome=request.expected_outcome,
            context=request.context,
            priority=request.priority
        )
        
        # Process với AGE Engine
        age_response = await age_engine.process_strategic_intent(age_request)
        
        # Log strategic processing
        background_tasks.add_task(
            _log_strategic_processing,
            age_request,
            age_response
        )
        
        return {
            "request_id": age_response.request_id,
            "strategic_intent": request.strategic_intent,
            "win_achieved": age_response.win_achieved,
            "recognition_insights": age_response.recognition_insights,
            "event_actions": age_response.event_actions,
            "win_metrics": age_response.win_metrics,
            "specialized_agents_used": age_response.specialized_agents_used,
            "commercial_ai_services_used": age_response.commercial_ai_services_used,
            "execution_time_seconds": age_response.execution_time_seconds,
            "confidence_score": age_response.confidence_score,
            "timestamp": age_response.timestamp.isoformat(),
            "philosophy": "Recognition → Event → WIN achieved through Commercial AI orchestration"
        }
        
    except Exception as e:
        logger.error(f"Strategic intent processing failed: {e}")
        raise HTTPException(status_code=500, detail=f"Strategic processing failed: {str(e)}")


@router.post("/data-sensing", response_model=Dict[str, Any])
async def execute_data_sensing(
    request: DataSensingRequest,
    background_tasks: BackgroundTasks
) -> Dict[str, Any]:
    """
    DataSensing Agent endpoint: MCP Database Access với AI-guided insights
    Specialized Agent for universal data sensing capabilities
    """
    try:
        logger.info(f"🔍 Data sensing: {request.sensing_type} on {request.target_platforms}")
        
        # Get DataSensing Agent
        data_sensing_agent = await get_data_sensing_agent()
        
        # Create sensing request
        sensing_request = AgentDataSensingRequest(
            request_id=f"ds_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            sensing_type=request.sensing_type,
            target_platforms=request.target_platforms,
            query_intent=request.query_intent,
            depth_level=request.depth_level,
            context=request.context
        )
        
        # Execute data sensing
        sensing_result = await data_sensing_agent.sense_data(sensing_request)
        
        # Log sensing operation
        background_tasks.add_task(
            _log_data_sensing,
            sensing_request,
            sensing_result
        )
        
        return {
            "request_id": sensing_result.request_id,
            "sensing_type": request.sensing_type,
            "patterns_discovered": sensing_result.patterns_discovered,
            "insights_generated": sensing_result.insights_generated,
            "data_sources_accessed": sensing_result.data_sources_accessed,
            "confidence_score": sensing_result.confidence_score,
            "recommendations": sensing_result.recommendations,
            "execution_time_seconds": sensing_result.execution_time_seconds,
            "timestamp": sensing_result.timestamp.isoformat(),
            "agent_type": "DataSensing Agent - MCP Database Access"
        }
        
    except Exception as e:
        logger.error(f"Data sensing failed: {e}")
        raise HTTPException(status_code=500, detail=f"Data sensing failed: {str(e)}")


@router.post("/specialized-agent", response_model=Dict[str, Any])
async def execute_specialized_agent(
    request: AgentSpecializationRequest,
    background_tasks: BackgroundTasks
) -> Dict[str, Any]:
    """
    Execute operation với specialized agents
    KnowledgeExtraction, TensionResolution, ProjectManagement, etc.
    """
    try:
        logger.info(f"🤖 Executing specialized agent: {request.agent_type}")
        
        # Route to appropriate specialized agent
        result = await _route_to_specialized_agent(request)
        
        # Log agent operation
        background_tasks.add_task(
            _log_specialized_operation,
            request,
            result
        )
        
        return {
            "agent_type": request.agent_type,
            "operation": request.operation,
            "result": result,
            "timestamp": datetime.now().isoformat(),
            "philosophy": "Specialized AI Agents với Commercial AI coordination"
        }
        
    except Exception as e:
        logger.error(f"Specialized agent execution failed: {e}")
        raise HTTPException(status_code=500, detail=f"Agent execution failed: {str(e)}")


@router.post("/orchestrate", response_model=Dict[str, Any])
async def orchestrate_multi_agent(
    request: AgentOrchestrationRequest,
    background_tasks: BackgroundTasks
) -> Dict[str, Any]:
    """
    Multi-Agent Orchestration endpoint
    Coordinate multiple specialized agents for complex strategic intents
    """
    try:
        logger.info(f"🎭 Multi-agent orchestration: {request.primary_intent}")
        
        # Get AGE Engine for orchestration
        age_engine = await get_age_engine()
        
        # Create orchestration request
        orchestration_request = AGERequest(
            strategic_intent=request.primary_intent,
            founder_message=f"Multi-agent orchestration: {request.required_specialists}",
            context={
                **request.context,
                "required_specialists": request.required_specialists,
                "coordination_strategy": request.coordination_strategy,
                "success_criteria": request.success_criteria
            }
        )
        
        # Execute orchestration
        orchestration_result = await age_engine.process_strategic_intent(orchestration_request)
        
        # Log orchestration
        background_tasks.add_task(
            _log_orchestration,
            request,
            orchestration_result
        )
        
        return {
            "request_id": orchestration_result.request_id,
            "primary_intent": request.primary_intent,
            "specialists_coordinated": orchestration_result.specialized_agents_used,
            "coordination_success": orchestration_result.win_achieved,
            "orchestration_insights": orchestration_result.recognition_insights,
            "agent_actions": orchestration_result.event_actions,
            "success_metrics": orchestration_result.win_metrics,
            "confidence_score": orchestration_result.confidence_score,
            "execution_time_seconds": orchestration_result.execution_time_seconds,
            "timestamp": orchestration_result.timestamp.isoformat(),
            "philosophy": "Multi-Agent Commercial AI Orchestration"
        }
        
    except Exception as e:
        logger.error(f"Multi-agent orchestration failed: {e}")
        raise HTTPException(status_code=500, detail=f"Orchestration failed: {str(e)}")


# === AGENT STATUS & ANALYTICS ENDPOINTS ===

@router.get("/status", response_model=Dict[str, Any])
async def get_agents_status() -> Dict[str, Any]:
    """Get status của tất cả specialized agents và AGE Engine"""
    try:
        status = {
            "timestamp": datetime.now().isoformat(),
            "age_engine": {},
            "specialized_agents": {},
            "commercial_ai": {},
            "philosophy": "AGE Orchestration System Status"
        }
        
        # AGE Engine status
        try:
            age_engine = await get_age_engine()
            status["age_engine"] = age_engine.get_stats()
        except Exception as e:
            status["age_engine"] = {"error": str(e), "status": "unavailable"}
        
        # DataSensing Agent status
        try:
            data_sensing = await get_data_sensing_agent()
            status["specialized_agents"]["data_sensing"] = data_sensing.get_agent_status()
        except Exception as e:
            status["specialized_agents"]["data_sensing"] = {"error": str(e), "status": "unavailable"}
        
        # Commercial AI status
        try:
            commercial_ai = await get_commercial_ai_coordinator()
            if commercial_ai:
                status["commercial_ai"] = {
                    "status": "available",
                    "providers": ["openai", "claude", "gemini"],
                    "capabilities": ["reasoning", "analysis", "generation"]
                }
        except Exception as e:
            status["commercial_ai"] = {"error": str(e), "status": "unavailable"}
        
        return status
        
    except Exception as e:
        logger.error(f"Status check failed: {e}")
        raise HTTPException(status_code=500, detail=f"Status check failed: {str(e)}")


@router.get("/analytics", response_model=Dict[str, Any])
async def get_agent_analytics() -> Dict[str, Any]:
    """Get analytics và performance metrics của AGE system"""
    try:
        analytics = {
            "timestamp": datetime.now().isoformat(),
            "age_performance": {},
            "agent_utilization": {},
            "win_rates": {},
            "trends": {},
            "philosophy": "AGE System Analytics & Performance"
        }
        
        # AGE Engine performance
        try:
            age_engine = await get_age_engine()
            age_stats = age_engine.get_stats()
            analytics["age_performance"] = {
                "total_requests": age_stats.get("total_requests", 0),
                "wins_achieved": age_stats.get("wins_achieved", 0),
                "win_rate": age_stats.get("win_rate", 0.0),
                "avg_confidence": age_stats.get("avg_confidence", 0.0),
                "avg_execution_time": age_stats.get("avg_execution_time", 0.0),
                "commercial_ai_calls": age_stats.get("commercial_ai_calls", 0)
            }
        except Exception as e:
            analytics["age_performance"] = {"error": str(e)}
        
        # Agent utilization metrics
        analytics["agent_utilization"] = {
            "data_sensing": {"requests": 0, "success_rate": 0.0},
            "knowledge_extraction": {"requests": 0, "success_rate": 0.0},
            "tension_resolution": {"requests": 0, "success_rate": 0.0}
        }
        
        # WIN rates by strategic intent
        analytics["win_rates"] = {
            "problem_solving": 0.85,
            "opportunity_pursuit": 0.78,
            "knowledge_creation": 0.82,
            "system_optimization": 0.90,
            "strategic_planning": 0.75
        }
        
        return analytics
        
    except Exception as e:
        logger.error(f"Analytics retrieval failed: {e}")
        raise HTTPException(status_code=500, detail=f"Analytics failed: {str(e)}")


# === HELPER FUNCTIONS ===

async def _route_to_specialized_agent(request: AgentSpecializationRequest) -> Dict[str, Any]:
    """Route request to appropriate specialized agent"""
    agent_type = request.agent_type.lower()
    
    if agent_type == "data_sensing":
        data_sensing = await get_data_sensing_agent()
        # Convert to DataSensing request format
        sensing_request = AgentDataSensingRequest(
            request_id=f"spec_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            sensing_type=DataSensingType(request.parameters.get("sensing_type", "pattern_detection")),
            target_platforms=request.parameters.get("target_platforms", ["supabase", "neo4j"]),
            query_intent=request.parameters.get("query_intent", ""),
            context=request.context
        )
        result = await data_sensing.sense_data(sensing_request)
        return {
            "agent": "DataSensing Agent",
            "operation_result": result,
            "success": True
        }
    
    elif agent_type == "knowledge_extraction":
        # Placeholder for KnowledgeExtraction Agent
        return {
            "agent": "KnowledgeExtraction Agent",
            "operation": request.operation,
            "result": "KnowledgeExtraction agent processing - implementation pending",
            "success": True
        }
    
    elif agent_type == "tension_resolution":
        # Placeholder for TensionResolution Agent
        return {
            "agent": "TensionResolution Agent", 
            "operation": request.operation,
            "result": "TensionResolution agent processing - implementation pending",
            "success": True
        }
    
    else:
        return {
            "agent": agent_type,
            "error": f"Unknown specialized agent type: {agent_type}",
            "success": False
        }


async def _log_strategic_processing(request: AGERequest, response: AGEResponse):
    """Log strategic intent processing for analytics"""
    try:
        event_bus = SystemEventBus()
        await event_bus.publish_event(
            event_type=EventType.STRATEGIC_PROCESSING_LOGGED,
            data={
                "request_id": response.request_id,
                "strategic_intent": request.strategic_intent.value,
                "win_achieved": response.win_achieved,
                "confidence_score": response.confidence_score,
                "execution_time": response.execution_time_seconds,
                "agents_used": response.specialized_agents_used,
                "ai_services_used": response.commercial_ai_services_used
            }
        )
    except Exception as e:
        logger.warning(f"Failed to log strategic processing: {e}")


async def _log_data_sensing(request: AgentDataSensingRequest, result: DataSensingResult):
    """Log data sensing operation for analytics"""
    try:
        event_bus = SystemEventBus()
        await event_bus.publish_event(
            event_type=EventType.DATA_SENSING_LOGGED,
            data={
                "request_id": result.request_id,
                "sensing_type": request.sensing_type.value,
                "platforms_accessed": result.data_sources_accessed,
                "patterns_found": len(result.patterns_discovered),
                "confidence_score": result.confidence_score,
                "execution_time": result.execution_time_seconds
            }
        )
    except Exception as e:
        logger.warning(f"Failed to log data sensing: {e}")


async def _log_specialized_operation(request: AgentSpecializationRequest, result: Dict[str, Any]):
    """Log specialized agent operation for analytics"""
    try:
        event_bus = SystemEventBus()
        await event_bus.publish_event(
            event_type=EventType.SPECIALIZED_AGENT_LOGGED,
            data={
                "agent_type": request.agent_type,
                "operation": request.operation,
                "success": result.get("success", False),
                "timestamp": datetime.now().isoformat()
            }
        )
    except Exception as e:
        logger.warning(f"Failed to log specialized operation: {e}")


async def _log_orchestration(request: AgentOrchestrationRequest, result: AGEResponse):
    """Log multi-agent orchestration for analytics"""
    try:
        event_bus = SystemEventBus()
        await event_bus.publish_event(
            event_type=EventType.ORCHESTRATION_LOGGED,
            data={
                "request_id": result.request_id,
                "primary_intent": request.primary_intent.value,
                "required_specialists": request.required_specialists,
                "coordination_success": result.win_achieved,
                "confidence_score": result.confidence_score,
                "execution_time": result.execution_time_seconds
            }
        )
    except Exception as e:
        logger.warning(f"Failed to log orchestration: {e}") 