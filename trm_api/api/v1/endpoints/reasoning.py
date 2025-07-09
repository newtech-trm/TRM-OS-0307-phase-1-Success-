"""
Reasoning API Endpoints - REST API for TRM-OS Basic Reasoning Engine

Provides endpoints for:
- Tension analysis
- Solution generation  
- Priority calculation
- Rule evaluation
- Complete reasoning workflow
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import List, Optional, Dict, Any
import logging
from datetime import datetime

from ....reasoning import (
    ReasoningCoordinator, 
    ReasoningRequest, 
    CoordinatorResult as ReasoningResult,
    TensionAnalyzer,
    RuleEngine,
    SolutionGenerator,
    PriorityCalculator
)
from ....core.config import get_settings
from ....models.tension import Tension
from ....repositories.tension_repository import TensionRepository
# from ....db.session import get_db_session  # Not needed for reasoning endpoints

# Initialize router
router = APIRouter(prefix="/reasoning", tags=["reasoning"])
logger = logging.getLogger(__name__)

# Initialize reasoning coordinator (singleton)
reasoning_coordinator = ReasoningCoordinator()

# Pydantic models for API
from pydantic import BaseModel, Field

class AnalysisRequest(BaseModel):
    """Request model for tension analysis"""
    title: str = Field(..., description="Tension title")
    description: str = Field(..., description="Tension description") 
    current_status: str = Field(default="Open", description="Current tension status")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Additional context")

class AnalysisResponse(BaseModel):
    """Response model for tension analysis"""
    tension_type: str
    impact_level: str
    urgency_level: str
    confidence_score: float
    key_themes: List[str]
    extracted_entities: List[str]
    suggested_priority: int
    reasoning: str

class SolutionRequest(BaseModel):
    """Request model for solution generation"""
    title: str
    description: str
    analysis_data: Optional[Dict[str, Any]] = None
    context: Optional[Dict[str, Any]] = None

class SolutionResponse(BaseModel):
    """Response model for generated solution"""
    id: str
    title: str
    description: str
    solution_type: str
    priority: str
    estimated_impact: str
    estimated_effort: str
    success_criteria: List[str]
    steps: List[Dict[str, Any]]
    required_resources: List[str]
    risks: List[str]
    alternatives: List[str]
    confidence_score: float
    reasoning: str

class PriorityRequest(BaseModel):
    """Request model for priority calculation"""
    title: str
    description: str
    analysis_data: Optional[Dict[str, Any]] = None
    context: Optional[Dict[str, Any]] = None
    calculation_method: str = Field(default="weighted_average", description="Priority calculation method")

class PriorityResponse(BaseModel):
    """Response model for priority calculation"""
    final_score: float
    normalized_priority: int
    priority_level: str
    contributing_factors: Dict[str, float]
    calculation_method: str
    confidence_level: float
    reasoning: str
    recommendations: List[str]

class CompleteReasoningRequest(BaseModel):
    """Request model for complete reasoning workflow"""
    tension_id: Optional[str] = None
    title: str
    description: str
    current_status: str = "Open"
    context: Optional[Dict[str, Any]] = None
    requested_services: List[str] = Field(default=["analysis", "rules", "solutions", "priority"])

class CompleteReasoningResponse(BaseModel):
    """Response model for complete reasoning workflow"""
    tension_id: str
    analysis: Optional[AnalysisResponse] = None
    rule_results: List[Dict[str, Any]] = []
    solutions: List[SolutionResponse] = []
    priority_calculation: Optional[PriorityResponse] = None
    processing_time: float
    success: bool
    errors: List[str] = []
    recommendations: List[str] = []

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_tension(request: AnalysisRequest):
    """
    Analyze a tension using AI pattern recognition
    
    Performs intelligent analysis to:
    - Classify tension type (Problem, Opportunity, Risk, Conflict, Idea)
    - Assess impact and urgency levels
    - Extract key themes and entities
    - Suggest priority level
    """
    try:
        logger.info(f"Analyzing tension: {request.title}")
        
        # Perform tension analysis
        analyzer = TensionAnalyzer()
        analysis = analyzer.analyze_tension(
            title=request.title,
            description=request.description,
            current_status=request.current_status
        )
        
        # Convert to response model
        response = AnalysisResponse(
            tension_type=analysis.tension_type.value,
            impact_level=analysis.impact_level.name,
            urgency_level=analysis.urgency_level.name,
            confidence_score=analysis.confidence_score,
            key_themes=analysis.key_themes,
            extracted_entities=analysis.extracted_entities,
            suggested_priority=analysis.suggested_priority,
            reasoning=analysis.reasoning
        )
        
        logger.info(f"Analysis completed: {analysis.tension_type.value} with {analysis.confidence_score:.1%} confidence")
        return response
        
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@router.post("/solutions", response_model=List[SolutionResponse])
async def generate_solutions(request: SolutionRequest):
    """
    Generate intelligent solution recommendations
    
    Creates multiple solution options based on:
    - Tension analysis results
    - Pattern matching templates
    - Context-aware recommendations
    - Risk and effort assessment
    """
    try:
        logger.info(f"Generating solutions for: {request.title}")
        
        # If analysis data provided, use it; otherwise analyze first
        if request.analysis_data:
            # Reconstruct analysis from data
            from ....reasoning.tension_analyzer import TensionType, ImpactLevel, UrgencyLevel, TensionAnalysis
            
            analysis = TensionAnalysis(
                tension_type=TensionType(request.analysis_data.get("tension_type", "Unknown")),
                impact_level=ImpactLevel(request.analysis_data.get("impact_level", 1)),
                urgency_level=UrgencyLevel(request.analysis_data.get("urgency_level", 1)),
                confidence_score=request.analysis_data.get("confidence_score", 0.5),
                key_themes=request.analysis_data.get("key_themes", []),
                extracted_entities=request.analysis_data.get("extracted_entities", []),
                suggested_priority=request.analysis_data.get("suggested_priority", 0),
                reasoning=request.analysis_data.get("reasoning", "")
            )
        else:
            # Perform analysis first
            analyzer = TensionAnalyzer()
            analysis = analyzer.analyze_tension(
                title=request.title,
                description=request.description
            )
        
        # Generate solutions
        generator = SolutionGenerator()
        solutions = generator.generate_solutions(
            tension_analysis=analysis,
            tension_title=request.title,
            tension_description=request.description,
            context=request.context
        )
        
        # Convert to response models
        response_solutions = []
        for solution in solutions:
            solution_response = SolutionResponse(
                id=solution.id,
                title=solution.title,
                description=solution.description,
                solution_type=solution.solution_type.value,
                priority=solution.priority.name,
                estimated_impact=solution.estimated_impact,
                estimated_effort=solution.estimated_effort,
                success_criteria=solution.success_criteria,
                steps=[{
                    "id": step.id,
                    "title": step.title,
                    "description": step.description,
                    "estimated_effort": step.estimated_effort,
                    "required_skills": step.required_skills,
                    "dependencies": step.dependencies
                } for step in solution.steps],
                required_resources=solution.required_resources,
                risks=solution.risks,
                alternatives=solution.alternatives,
                confidence_score=solution.confidence_score,
                reasoning=solution.reasoning
            )
            response_solutions.append(solution_response)
        
        logger.info(f"Generated {len(solutions)} solutions")
        return response_solutions
        
    except Exception as e:
        logger.error(f"Solution generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Solution generation failed: {str(e)}")

@router.post("/priority", response_model=PriorityResponse)
async def calculate_priority(request: PriorityRequest):
    """
    Calculate intelligent priority score
    
    Uses advanced algorithms to calculate priority based on:
    - Multi-dimensional analysis (impact, urgency, complexity, resources)
    - Business context and rules
    - Risk factors and dependencies
    - Strategic alignment
    """
    try:
        logger.info(f"Calculating priority for: {request.title}")
        
        # Get or create analysis
        if request.analysis_data:
            from ....reasoning.tension_analyzer import TensionType, ImpactLevel, UrgencyLevel, TensionAnalysis
            
            analysis = TensionAnalysis(
                tension_type=TensionType(request.analysis_data.get("tension_type", "Unknown")),
                impact_level=ImpactLevel(request.analysis_data.get("impact_level", 1)),
                urgency_level=UrgencyLevel(request.analysis_data.get("urgency_level", 1)),
                confidence_score=request.analysis_data.get("confidence_score", 0.5),
                key_themes=request.analysis_data.get("key_themes", []),
                extracted_entities=request.analysis_data.get("extracted_entities", []),
                suggested_priority=request.analysis_data.get("suggested_priority", 0),
                reasoning=request.analysis_data.get("reasoning", "")
            )
        else:
            analyzer = TensionAnalyzer()
            analysis = analyzer.analyze_tension(
                title=request.title,
                description=request.description
            )
        
        # Calculate priority
        calculator = PriorityCalculator()
        priority_result = calculator.calculate_priority(
            tension_analysis=analysis,
            title=request.title,
            description=request.description,
            context=request.context,
            method=request.calculation_method
        )
        
        # Convert to response model
        response = PriorityResponse(
            final_score=priority_result.final_score,
            normalized_priority=priority_result.normalized_priority,
            priority_level=priority_result.priority_level,
            contributing_factors=priority_result.contributing_factors,
            calculation_method=priority_result.calculation_method,
            confidence_level=priority_result.confidence_level,
            reasoning=priority_result.reasoning,
            recommendations=priority_result.recommendations
        )
        
        logger.info(f"Priority calculated: {priority_result.final_score:.1f} ({priority_result.priority_level})")
        return response
        
    except Exception as e:
        logger.error(f"Priority calculation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Priority calculation failed: {str(e)}")

@router.post("/complete", response_model=CompleteReasoningResponse)
async def complete_reasoning_workflow(request: CompleteReasoningRequest):
    """
    Execute complete reasoning workflow
    
    Performs end-to-end AI reasoning including:
    - Tension analysis
    - Business rule evaluation
    - Solution generation
    - Priority calculation
    - Consolidated recommendations
    """
    try:
        logger.info(f"Starting complete reasoning workflow for: {request.title}")
        
        # Create reasoning request
        reasoning_request = ReasoningRequest(
            tension_id=request.tension_id or f"temp_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            title=request.title,
            description=request.description,
            current_status=request.current_status,
            context=request.context,
            requested_services=request.requested_services
        )
        
        # Process through reasoning coordinator
        result = await reasoning_coordinator.process_tension(reasoning_request)
        
        # Convert to response model
        response = CompleteReasoningResponse(
            tension_id=result.tension_id,
            processing_time=result.processing_time,
            success=result.success,
            errors=result.errors,
            recommendations=result.recommendations
        )
        
        # Add analysis if available
        if result.analysis:
            response.analysis = AnalysisResponse(
                tension_type=result.analysis.tension_type.value,
                impact_level=result.analysis.impact_level.name,
                urgency_level=result.analysis.urgency_level.name,
                confidence_score=result.analysis.confidence_score,
                key_themes=result.analysis.key_themes,
                extracted_entities=result.analysis.extracted_entities,
                suggested_priority=result.analysis.suggested_priority,
                reasoning=result.analysis.reasoning
            )
        
        # Add rule results
        response.rule_results = result.rule_results
        
        # Add solutions if available
        if result.solutions:
            response.solutions = []
            for solution in result.solutions:
                solution_response = SolutionResponse(
                    id=solution.id,
                    title=solution.title,
                    description=solution.description,
                    solution_type=solution.solution_type.value,
                    priority=solution.priority.name,
                    estimated_impact=solution.estimated_impact,
                    estimated_effort=solution.estimated_effort,
                    success_criteria=solution.success_criteria,
                    steps=[{
                        "id": step.id,
                        "title": step.title,
                        "description": step.description,
                        "estimated_effort": step.estimated_effort,
                        "required_skills": step.required_skills,
                        "dependencies": step.dependencies
                    } for step in solution.steps],
                    required_resources=solution.required_resources,
                    risks=solution.risks,
                    alternatives=solution.alternatives,
                    confidence_score=solution.confidence_score,
                    reasoning=solution.reasoning
                )
                response.solutions.append(solution_response)
        
        # Add priority calculation if available
        if result.priority_calculation:
            response.priority_calculation = PriorityResponse(
                final_score=result.priority_calculation.final_score,
                normalized_priority=result.priority_calculation.normalized_priority,
                priority_level=result.priority_calculation.priority_level,
                contributing_factors=result.priority_calculation.contributing_factors,
                calculation_method=result.priority_calculation.calculation_method,
                confidence_level=result.priority_calculation.confidence_level,
                reasoning=result.priority_calculation.reasoning,
                recommendations=result.priority_calculation.recommendations
            )
        
        logger.info(f"Complete reasoning workflow finished in {result.processing_time:.2f}s")
        return response
        
    except Exception as e:
        logger.error(f"Complete reasoning workflow failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Reasoning workflow failed: {str(e)}")

@router.post("/tension/{tension_id}/analyze")
async def analyze_existing_tension(tension_id: str):
    """
    Analyze an existing tension from database
    
    Retrieves tension from database and performs AI analysis
    """
    try:
        logger.info(f"Analyzing existing tension: {tension_id}")
        
        # Get tension from database
        tension_repo = TensionRepository(db_session)
        tension = await tension_repo.get_by_id(tension_id)
        
        if not tension:
            raise HTTPException(status_code=404, detail="Tension not found")
        
        # Create reasoning request
        reasoning_request = ReasoningRequest(
            tension_id=tension_id,
            title=tension.title,
            description=tension.description or "",
            current_status=tension.status,
            context={
                "project_id": tension.project_id,
                "created_at": tension.created_at.isoformat() if tension.created_at else None,
                "priority": tension.priority
            }
        )
        
        # Process through reasoning coordinator
        result = await reasoning_coordinator.process_tension(reasoning_request)
        
        # Convert to response (similar to complete_reasoning_workflow)
        response = CompleteReasoningResponse(
            tension_id=result.tension_id,
            processing_time=result.processing_time,
            success=result.success,
            errors=result.errors,
            recommendations=result.recommendations
        )
        
        # Add analysis if available
        if result.analysis:
            response.analysis = AnalysisResponse(
                tension_type=result.analysis.tension_type.value,
                impact_level=result.analysis.impact_level.name,
                urgency_level=result.analysis.urgency_level.name,
                confidence_score=result.analysis.confidence_score,
                key_themes=result.analysis.key_themes,
                extracted_entities=result.analysis.extracted_entities,
                suggested_priority=result.analysis.suggested_priority,
                reasoning=result.analysis.reasoning
            )
        
        # Add other components...
        response.rule_results = result.rule_results
        
        logger.info(f"Existing tension analysis completed for {tension_id}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Existing tension analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@router.get("/health")
async def reasoning_health_check():
    """
    Health check for reasoning engine components
    
    Validates all reasoning components and returns status
    """
    try:
        logger.info("Performing reasoning engine health check")
        
        # Validate all components
        validation_results = await reasoning_coordinator.validate_reasoning_components()
        
        # Get performance stats
        performance_stats = reasoning_coordinator.get_performance_stats()
        
        # Get rule engine summary
        rule_summary = reasoning_coordinator.get_rule_engine_summary()
        
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "validation": validation_results,
            "performance": performance_stats,
            "rules": rule_summary,
            "version": "1.0.0-mvp"
        }
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {
            "status": "error",
            "timestamp": datetime.now().isoformat(),
            "error": str(e),
            "version": "1.0.0-mvp"
        }

@router.get("/insights")
async def get_reasoning_insights():
    """
    Get insights and analytics from reasoning engine
    
    Returns performance metrics, patterns, and effectiveness data
    """
    try:
        logger.info("Generating reasoning insights")
        
        # Export comprehensive insights
        insights = reasoning_coordinator.export_reasoning_insights()
        
        return {
            "status": "success",
            "insights": insights,
            "generated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Insights generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Insights generation failed: {str(e)}")

@router.post("/batch")
async def process_batch_tensions(
    requests: List[CompleteReasoningRequest],
    background_tasks: BackgroundTasks
):
    """
    Process multiple tensions in parallel
    
    Efficiently processes multiple tensions using async processing
    """
    try:
        logger.info(f"Processing batch of {len(requests)} tensions")
        
        # Convert to reasoning requests
        reasoning_requests = []
        for req in requests:
            reasoning_request = ReasoningRequest(
                tension_id=req.tension_id or f"batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{len(reasoning_requests)}",
                title=req.title,
                description=req.description,
                current_status=req.current_status,
                context=req.context,
                requested_services=req.requested_services
            )
            reasoning_requests.append(reasoning_request)
        
        # Process batch
        results = await reasoning_coordinator.process_batch_tensions(reasoning_requests)
        
        # Convert to response models
        response_results = []
        for result in results:
            response = CompleteReasoningResponse(
                tension_id=result.tension_id,
                processing_time=result.processing_time,
                success=result.success,
                errors=result.errors,
                recommendations=result.recommendations
            )
            
            # Add components if available (simplified for batch processing)
            if result.analysis:
                response.analysis = AnalysisResponse(
                    tension_type=result.analysis.tension_type.value,
                    impact_level=result.analysis.impact_level.name,
                    urgency_level=result.analysis.urgency_level.name,
                    confidence_score=result.analysis.confidence_score,
                    key_themes=result.analysis.key_themes,
                    extracted_entities=result.analysis.extracted_entities,
                    suggested_priority=result.analysis.suggested_priority,
                    reasoning=result.analysis.reasoning
                )
            
            response_results.append(response)
        
        # Calculate batch statistics
        successful_count = sum(1 for r in results if r.success)
        total_processing_time = sum(r.processing_time for r in results)
        
        logger.info(f"Batch processing completed: {successful_count}/{len(requests)} successful")
        
        return {
            "status": "completed",
            "results": response_results,
            "statistics": {
                "total_requests": len(requests),
                "successful_processing": successful_count,
                "failed_processing": len(requests) - successful_count,
                "total_processing_time": total_processing_time,
                "average_processing_time": total_processing_time / len(requests) if requests else 0
            }
        }
        
    except Exception as e:
        logger.error(f"Batch processing failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Batch processing failed: {str(e)}") 