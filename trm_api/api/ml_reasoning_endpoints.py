"""
API Endpoints for ML-Enhanced Reasoning Engine
Provides REST API access to advanced reasoning capabilities
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime
import logging

from ..reasoning.ml_enhanced_reasoning_engine import (
    MLEnhancedReasoningEngine,
    ReasoningType,
    ConfidenceLevel,
    ReasoningContext,
    ReasoningResult
)
from ..learning.adaptive_learning_system import AdaptiveLearningSystem
from ..quantum.quantum_system_manager import QuantumSystemManager
from ..reasoning.advanced_reasoning_engine import AdvancedReasoningEngine
from ..dependencies import get_current_user


# Router setup
router = APIRouter(prefix="/api/v1/ml-reasoning", tags=["ML-Enhanced Reasoning"])
logger = logging.getLogger(__name__)


# Request/Response Models
class ReasoningRequest(BaseModel):
    """Request model for reasoning operations"""
    query: str = Field(..., description="The reasoning query")
    domain: str = Field(..., description="Domain context (e.g., 'tension_resolution')")
    reasoning_type: ReasoningType = Field(default=ReasoningType.HYBRID, description="Type of reasoning to perform")
    stakeholders: List[str] = Field(default_factory=list, description="Involved stakeholders")
    constraints: Dict[str, Any] = Field(default_factory=dict, description="Reasoning constraints")
    objectives: List[str] = Field(default_factory=list, description="Reasoning objectives")
    available_resources: Dict[str, float] = Field(default_factory=dict, description="Available resources")
    priority_level: int = Field(default=5, ge=1, le=10, description="Priority level (1-10)")
    risk_tolerance: float = Field(default=0.5, ge=0.0, le=1.0, description="Risk tolerance (0.0-1.0)")
    use_quantum_enhancement: bool = Field(default=True, description="Enable quantum enhancement")
    quantum_context: Dict[str, Any] = Field(default_factory=dict, description="Quantum context data")


class ReasoningResponse(BaseModel):
    """Response model for reasoning operations"""
    result_id: str
    reasoning_type: ReasoningType
    conclusion: str
    confidence: float
    confidence_level: ConfidenceLevel
    reasoning_steps: List[str]
    supporting_evidence: List[str]
    contradicting_evidence: List[str]
    assumptions: List[str]
    alternative_conclusions: List[str]
    ml_confidence: float
    quantum_enhancement: float
    win_probability_impact: float
    reasoning_time: float
    timestamp: datetime
    logical_consistency: float
    evidence_strength: float
    novelty_score: float


class TrainingRequest(BaseModel):
    """Request model for ML model training"""
    training_data: List[Dict[str, Any]] = Field(..., description="Training data for ML models")
    model_types: List[str] = Field(default=["confidence_estimator", "reasoning_predictor", "quantum_enhancer"], 
                                  description="Types of models to train")


class TrainingResponse(BaseModel):
    """Response model for ML model training"""
    training_id: str
    status: str
    models_trained: Dict[str, Any]
    training_metrics: Dict[str, float]
    timestamp: datetime


class PatternAnalysisResponse(BaseModel):
    """Response model for pattern analysis"""
    analysis_id: str
    confidence_trends: Dict[str, Any]
    reasoning_type_distribution: Dict[str, float]
    performance_metrics: Dict[str, float]
    recommendations: List[Dict[str, Any]]
    timestamp: datetime


class RecommendationResponse(BaseModel):
    """Response model for reasoning recommendations"""
    recommendations: List[Dict[str, Any]]
    context_analysis: Dict[str, Any]
    confidence_scores: Dict[str, float]
    timestamp: datetime


class StatisticsResponse(BaseModel):
    """Response model for reasoning statistics"""
    total_reasonings: int
    successful_reasonings: int
    success_rate: float
    average_confidence: float
    average_reasoning_time: float
    ml_enhancement_rate: float
    quantum_enhancement_rate: float
    confidence_distribution: Dict[str, float]
    reasoning_type_distribution: Dict[str, float]


# Global ML-Enhanced Reasoning Engine instance
ml_reasoning_engine: Optional[MLEnhancedReasoningEngine] = None


async def get_ml_reasoning_engine() -> MLEnhancedReasoningEngine:
    """Get ML-Enhanced Reasoning Engine instance"""
    global ml_reasoning_engine
    
    if ml_reasoning_engine is None:
        # Initialize dependencies
        learning_system = AdaptiveLearningSystem(agent_id="ml_reasoning_api")
        await learning_system.initialize()
        
        quantum_manager = QuantumSystemManager(learning_system=learning_system)
        await quantum_manager.initialize()
        
        advanced_reasoning = AdvancedReasoningEngine("ml_reasoning_api")
        
        # Create ML-Enhanced Reasoning Engine
        ml_reasoning_engine = MLEnhancedReasoningEngine(
            learning_system=learning_system,
            quantum_manager=quantum_manager,
            advanced_reasoning=advanced_reasoning
        )
        
        await ml_reasoning_engine.initialize()
        logger.info("ML-Enhanced Reasoning Engine initialized for API")
    
    return ml_reasoning_engine


@router.post("/reason", response_model=ReasoningResponse)
async def perform_reasoning(
    request: ReasoningRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
    engine: MLEnhancedReasoningEngine = Depends(get_ml_reasoning_engine)
) -> ReasoningResponse:
    """
    Perform ML-enhanced reasoning operation
    
    This endpoint provides access to the complete ML-Enhanced Reasoning Engine
    including classical reasoning, ML enhancement, and quantum enhancement.
    """
    try:
        logger.info(f"Reasoning request from user {current_user.get('user_id', 'unknown')}: {request.query[:100]}...")
        
        # Create reasoning context
        context = ReasoningContext(
            context_id=f"api_request_{datetime.now().timestamp()}",
            domain=request.domain,
            stakeholders=request.stakeholders,
            constraints=request.constraints,
            objectives=request.objectives,
            available_resources=request.available_resources,
            priority_level=request.priority_level,
            risk_tolerance=request.risk_tolerance,
            quantum_context=request.quantum_context
        )
        
        # Perform reasoning
        result = await engine.reason(
            query=request.query,
            context=context,
            reasoning_type=request.reasoning_type,
            use_quantum_enhancement=request.use_quantum_enhancement
        )
        
        # Convert to response model
        response = ReasoningResponse(
            result_id=result.result_id,
            reasoning_type=result.reasoning_type,
            conclusion=result.conclusion,
            confidence=result.confidence,
            confidence_level=result.get_confidence_level(),
            reasoning_steps=result.reasoning_steps,
            supporting_evidence=result.supporting_evidence,
            contradicting_evidence=result.contradicting_evidence,
            assumptions=result.assumptions,
            alternative_conclusions=result.alternative_conclusions,
            ml_confidence=result.ml_confidence,
            quantum_enhancement=result.quantum_enhancement,
            win_probability_impact=result.win_probability_impact,
            reasoning_time=result.reasoning_time,
            timestamp=result.timestamp,
            logical_consistency=result.logical_consistency,
            evidence_strength=result.evidence_strength,
            novelty_score=result.novelty_score
        )
        
        logger.info(f"Reasoning completed successfully: {result.result_id}")
        return response
        
    except Exception as e:
        logger.error(f"Reasoning failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Reasoning failed: {str(e)}")


@router.post("/train", response_model=TrainingResponse)
async def train_ml_models(
    request: TrainingRequest,
    background_tasks: BackgroundTasks,
    current_user: Dict[str, Any] = Depends(get_current_user),
    engine: MLEnhancedReasoningEngine = Depends(get_ml_reasoning_engine)
) -> TrainingResponse:
    """
    Train ML models for enhanced reasoning
    
    This endpoint allows training of ML models used for reasoning enhancement.
    Training is performed in the background to avoid blocking the API.
    """
    try:
        logger.info(f"ML model training request from user {current_user.get('user_id', 'unknown')}")
        
        # Start background training
        training_id = f"training_{datetime.now().timestamp()}"
        
        async def train_models():
            try:
                training_result = await engine.train_ml_models(request.training_data)
                logger.info(f"ML model training completed: {training_id}")
                return training_result
            except Exception as e:
                logger.error(f"ML model training failed: {str(e)}")
                raise
        
        background_tasks.add_task(train_models)
        
        # Return immediate response
        response = TrainingResponse(
            training_id=training_id,
            status="started",
            models_trained={},
            training_metrics={},
            timestamp=datetime.now()
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Training initiation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Training failed: {str(e)}")


@router.get("/patterns", response_model=PatternAnalysisResponse)
async def analyze_reasoning_patterns(
    current_user: Dict[str, Any] = Depends(get_current_user),
    engine: MLEnhancedReasoningEngine = Depends(get_ml_reasoning_engine)
) -> PatternAnalysisResponse:
    """
    Analyze reasoning patterns and trends
    
    This endpoint provides insights into reasoning patterns, performance trends,
    and recommendations for improvement.
    """
    try:
        logger.info(f"Pattern analysis request from user {current_user.get('user_id', 'unknown')}")
        
        # Analyze patterns
        patterns = await engine.analyze_reasoning_patterns()
        
        # Convert to response model
        response = PatternAnalysisResponse(
            analysis_id=f"analysis_{datetime.now().timestamp()}",
            confidence_trends=patterns.get("confidence_trends", {}),
            reasoning_type_distribution=patterns.get("reasoning_type_distribution", {}),
            performance_metrics=patterns.get("performance_metrics", {}),
            recommendations=patterns.get("recommendations", []),
            timestamp=datetime.now()
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Pattern analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Pattern analysis failed: {str(e)}")


@router.post("/recommendations", response_model=RecommendationResponse)
async def get_reasoning_recommendations(
    request: ReasoningRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
    engine: MLEnhancedReasoningEngine = Depends(get_ml_reasoning_engine)
) -> RecommendationResponse:
    """
    Get reasoning recommendations for a given context
    
    This endpoint provides recommendations for the best reasoning approach
    based on the context and historical performance.
    """
    try:
        logger.info(f"Recommendations request from user {current_user.get('user_id', 'unknown')}")
        
        # Create reasoning context
        context = ReasoningContext(
            context_id=f"recommendations_{datetime.now().timestamp()}",
            domain=request.domain,
            stakeholders=request.stakeholders,
            constraints=request.constraints,
            objectives=request.objectives,
            available_resources=request.available_resources,
            priority_level=request.priority_level,
            risk_tolerance=request.risk_tolerance,
            quantum_context=request.quantum_context
        )
        
        # Get recommendations
        recommendations = await engine.get_reasoning_recommendations(context)
        
        # Convert to response model
        response = RecommendationResponse(
            recommendations=recommendations,
            context_analysis={
                "domain": request.domain,
                "complexity": len(request.stakeholders) + len(request.constraints) + len(request.objectives),
                "priority": request.priority_level,
                "risk_tolerance": request.risk_tolerance
            },
            confidence_scores={rec["reasoning_type"]: rec["confidence"] for rec in recommendations},
            timestamp=datetime.now()
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Recommendations failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Recommendations failed: {str(e)}")


@router.get("/statistics", response_model=StatisticsResponse)
async def get_reasoning_statistics(
    current_user: Dict[str, Any] = Depends(get_current_user),
    engine: MLEnhancedReasoningEngine = Depends(get_ml_reasoning_engine)
) -> StatisticsResponse:
    """
    Get reasoning engine statistics and performance metrics
    
    This endpoint provides comprehensive statistics about the reasoning engine's
    performance, including success rates, confidence distributions, and usage patterns.
    """
    try:
        logger.info(f"Statistics request from user {current_user.get('user_id', 'unknown')}")
        
        # Get statistics
        stats = engine.get_reasoning_statistics()
        
        # Calculate additional metrics
        success_rate = stats["successful_reasonings"] / max(1, stats["total_reasonings"])
        
        # Convert to response model
        response = StatisticsResponse(
            total_reasonings=stats["total_reasonings"],
            successful_reasonings=stats["successful_reasonings"],
            success_rate=success_rate,
            average_confidence=stats["average_confidence"],
            average_reasoning_time=stats["average_reasoning_time"],
            ml_enhancement_rate=stats["ml_enhancement_rate"],
            quantum_enhancement_rate=stats["quantum_enhancement_rate"],
            confidence_distribution=stats.get("confidence_distribution", {}),
            reasoning_type_distribution=stats.get("reasoning_type_distribution", {})
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Statistics retrieval failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Statistics failed: {str(e)}")


@router.get("/health")
async def health_check(
    engine: MLEnhancedReasoningEngine = Depends(get_ml_reasoning_engine)
) -> JSONResponse:
    """
    Health check endpoint for ML-Enhanced Reasoning Engine
    """
    try:
        # Check engine status
        stats = engine.get_reasoning_statistics()
        
        # Check component health
        health_status = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "components": {
                "ml_reasoning_engine": "operational",
                "learning_system": "operational" if engine.learning_system else "unavailable",
                "quantum_manager": "operational" if engine.quantum_manager else "unavailable",
                "advanced_reasoning": "operational" if engine.advanced_reasoning else "unavailable"
            },
            "performance": {
                "total_reasonings": stats["total_reasonings"],
                "average_confidence": stats["average_confidence"],
                "average_reasoning_time": stats["average_reasoning_time"]
            }
        }
        
        return JSONResponse(content=health_status)
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
        )


# Error handlers
@router.exception_handler(ValueError)
async def value_error_handler(request, exc):
    """Handle value errors"""
    logger.error(f"Value error in ML reasoning API: {str(exc)}")
    return JSONResponse(
        status_code=400,
        content={"error": "Invalid input", "detail": str(exc)}
    )


@router.exception_handler(Exception)
async def general_error_handler(request, exc):
    """Handle general errors"""
    logger.error(f"Unexpected error in ML reasoning API: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": "An unexpected error occurred"}
    ) 