"""
ReasoningCoordinator - Central orchestrator for TRM-OS reasoning engine

Coordinates:
- Tension analysis workflow
- Rule evaluation and execution
- Solution generation
- Priority calculation
- Integration with existing services
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import asyncio
import logging

from .tension_analyzer import TensionAnalyzer, TensionAnalysis
from .rule_engine import RuleEngine, RuleType
from .solution_generator import SolutionGenerator, GeneratedSolution
from .priority_calculator import PriorityCalculator, PriorityCalculationResult

@dataclass
class ReasoningRequest:
    """Request for reasoning engine processing"""
    tension_id: str
    title: str
    description: str
    current_status: str = "Open"
    context: Optional[Dict[str, Any]] = None
    requested_services: List[str] = None  # ["analysis", "rules", "solutions", "priority"]
    
    def __post_init__(self):
        if self.requested_services is None:
            self.requested_services = ["analysis", "rules", "solutions", "priority"]

@dataclass
class ReasoningResult:
    """Complete reasoning result"""
    tension_id: str
    analysis: Optional[TensionAnalysis] = None
    rule_results: List[Dict[str, Any]] = None
    solutions: List[GeneratedSolution] = None
    priority_calculation: Optional[PriorityCalculationResult] = None
    processing_time: float = 0.0
    success: bool = True
    errors: List[str] = None
    recommendations: List[str] = None
    
    def __post_init__(self):
        if self.rule_results is None:
            self.rule_results = []
        if self.solutions is None:
            self.solutions = []
        if self.errors is None:
            self.errors = []
        if self.recommendations is None:
            self.recommendations = []

class ReasoningCoordinator:
    """
    Central coordinator for TRM-OS Basic Reasoning Engine MVP.
    
    Orchestrates the complete reasoning workflow:
    1. Tension Analysis
    2. Rule Evaluation
    3. Solution Generation
    4. Priority Calculation
    5. Result Integration
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Initialize reasoning components
        self.tension_analyzer = TensionAnalyzer()
        self.rule_engine = RuleEngine()
        self.solution_generator = SolutionGenerator()
        self.priority_calculator = PriorityCalculator()
        
        # Performance tracking
        self.processing_stats = {
            "total_processed": 0,
            "successful_processing": 0,
            "average_processing_time": 0.0,
            "component_performance": {
                "analysis": {"count": 0, "total_time": 0.0},
                "rules": {"count": 0, "total_time": 0.0},
                "solutions": {"count": 0, "total_time": 0.0},
                "priority": {"count": 0, "total_time": 0.0}
            }
        }
    
    async def process_tension(self, request: ReasoningRequest) -> ReasoningResult:
        """
        Process tension through complete reasoning pipeline
        
        Args:
            request: ReasoningRequest with tension details
            
        Returns:
            ReasoningResult with all analysis results
        """
        start_time = datetime.now()
        result = ReasoningResult(tension_id=request.tension_id)
        
        try:
            self.logger.info(f"Starting reasoning process for tension {request.tension_id}")
            
            # Step 1: Tension Analysis
            if "analysis" in request.requested_services:
                result.analysis = await self._perform_tension_analysis(request)
                if not result.analysis:
                    result.errors.append("Failed to analyze tension")
                    result.success = False
                    return result
            
            # Step 2: Rule Evaluation
            if "rules" in request.requested_services and result.analysis:
                result.rule_results = await self._evaluate_rules(request, result.analysis)
            
            # Step 3: Solution Generation
            if "solutions" in request.requested_services and result.analysis:
                result.solutions = await self._generate_solutions(request, result.analysis)
            
            # Step 4: Priority Calculation
            if "priority" in request.requested_services and result.analysis:
                result.priority_calculation = await self._calculate_priority(request, result.analysis)
            
            # Step 5: Generate consolidated recommendations
            result.recommendations = self._generate_consolidated_recommendations(result)
            
            # Update statistics
            self._update_processing_stats(start_time, result.success)
            
            self.logger.info(f"Completed reasoning process for tension {request.tension_id}")
            
        except Exception as e:
            self.logger.error(f"Error processing tension {request.tension_id}: {str(e)}")
            result.errors.append(f"Processing error: {str(e)}")
            result.success = False
        
        finally:
            end_time = datetime.now()
            result.processing_time = (end_time - start_time).total_seconds()
        
        return result
    
    async def _perform_tension_analysis(self, request: ReasoningRequest) -> Optional[TensionAnalysis]:
        """Perform tension analysis"""
        start_time = datetime.now()
        
        try:
            self.logger.debug(f"Analyzing tension: {request.title}")
            
            # Run tension analysis
            analysis = self.tension_analyzer.analyze_tension(
                title=request.title,
                description=request.description,
                current_status=request.current_status
            )
            
            self._update_component_stats("analysis", start_time)
            return analysis
            
        except Exception as e:
            self.logger.error(f"Tension analysis failed: {str(e)}")
            return None
    
    async def _evaluate_rules(self, request: ReasoningRequest, 
                            analysis: TensionAnalysis) -> List[Dict[str, Any]]:
        """Evaluate business rules"""
        start_time = datetime.now()
        
        try:
            self.logger.debug(f"Evaluating rules for tension: {request.tension_id}")
            
            # Prepare context for rule evaluation
            rule_context = {
                "tension_id": request.tension_id,
                "title": request.title,
                "description": request.description,
                "analysis": {
                    "tension_type": analysis.tension_type,
                    "impact_level": analysis.impact_level,
                    "urgency_level": analysis.urgency_level,
                    "suggested_priority": analysis.suggested_priority,
                    "key_themes": analysis.key_themes,
                    "confidence_score": analysis.confidence_score
                }
            }
            
            # Add context if provided
            if request.context:
                rule_context.update(request.context)
            
            # Evaluate all rules
            rule_results = self.rule_engine.evaluate_rules(rule_context)
            
            self._update_component_stats("rules", start_time)
            return rule_results
            
        except Exception as e:
            self.logger.error(f"Rule evaluation failed: {str(e)}")
            return []
    
    async def _generate_solutions(self, request: ReasoningRequest,
                                analysis: TensionAnalysis) -> List[GeneratedSolution]:
        """Generate solution recommendations"""
        start_time = datetime.now()
        
        try:
            self.logger.debug(f"Generating solutions for tension: {request.tension_id}")
            
            # Generate solutions
            solutions = self.solution_generator.generate_solutions(
                tension_analysis=analysis,
                tension_title=request.title,
                tension_description=request.description,
                context=request.context
            )
            
            self._update_component_stats("solutions", start_time)
            return solutions
            
        except Exception as e:
            self.logger.error(f"Solution generation failed: {str(e)}")
            return []
    
    async def _calculate_priority(self, request: ReasoningRequest,
                                analysis: TensionAnalysis) -> Optional[PriorityCalculationResult]:
        """Calculate priority score"""
        start_time = datetime.now()
        
        try:
            self.logger.debug(f"Calculating priority for tension: {request.tension_id}")
            
            # Determine calculation method from context
            method = "weighted_average"
            if request.context:
                method = request.context.get("priority_method", "weighted_average")
            
            # Calculate priority
            priority_result = self.priority_calculator.calculate_priority(
                tension_analysis=analysis,
                title=request.title,
                description=request.description,
                context=request.context,
                method=method
            )
            
            self._update_component_stats("priority", start_time)
            return priority_result
            
        except Exception as e:
            self.logger.error(f"Priority calculation failed: {str(e)}")
            return None
    
    def _generate_consolidated_recommendations(self, result: ReasoningResult) -> List[str]:
        """Generate consolidated recommendations from all components"""
        recommendations = []
        
        # Analysis-based recommendations
        if result.analysis:
            if result.analysis.suggested_priority == 2:
                recommendations.append("🚨 Critical tension - immediate action required")
            elif result.analysis.suggested_priority == 1:
                recommendations.append("⚠️ High priority - schedule for next iteration")
            
            # Theme-based recommendations
            if "Security" in result.analysis.key_themes:
                recommendations.append("🔐 Security review required")
            if "Technology" in result.analysis.key_themes:
                recommendations.append("💻 Technical expertise needed")
            if "Business" in result.analysis.key_themes:
                recommendations.append("📊 Business stakeholder involvement recommended")
        
        # Rule-based recommendations
        if result.rule_results:
            for rule_result in result.rule_results:
                if rule_result.get("matched", False):
                    rule_name = rule_result.get("rule_name", "Unknown")
                    recommendations.append(f"📋 Rule triggered: {rule_name}")
        
        # Solution-based recommendations
        if result.solutions:
            top_solution = result.solutions[0]  # Highest priority solution
            recommendations.append(f"💡 Recommended approach: {top_solution.title}")
            
            if top_solution.priority.value >= 3:
                recommendations.append("⏰ Time-sensitive solution required")
        
        # Priority-based recommendations
        if result.priority_calculation:
            if result.priority_calculation.final_score >= 80:
                recommendations.append("🎯 Top priority for immediate execution")
            elif result.priority_calculation.final_score >= 60:
                recommendations.append("📅 Schedule for upcoming sprint")
            
            # Add specific priority recommendations
            recommendations.extend(result.priority_calculation.recommendations)
        
        # Remove duplicates and limit to top 10
        unique_recommendations = list(dict.fromkeys(recommendations))
        return unique_recommendations[:10]
    
    def _update_component_stats(self, component: str, start_time: datetime):
        """Update performance statistics for component"""
        processing_time = (datetime.now() - start_time).total_seconds()
        
        stats = self.processing_stats["component_performance"][component]
        stats["count"] += 1
        stats["total_time"] += processing_time
    
    def _update_processing_stats(self, start_time: datetime, success: bool):
        """Update overall processing statistics"""
        processing_time = (datetime.now() - start_time).total_seconds()
        
        self.processing_stats["total_processed"] += 1
        if success:
            self.processing_stats["successful_processing"] += 1
        
        # Update average processing time
        total_time = (self.processing_stats["average_processing_time"] * 
                     (self.processing_stats["total_processed"] - 1) + processing_time)
        self.processing_stats["average_processing_time"] = total_time / self.processing_stats["total_processed"]
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get current performance statistics"""
        stats = self.processing_stats.copy()
        
        # Calculate component averages
        for component, component_stats in stats["component_performance"].items():
            if component_stats["count"] > 0:
                component_stats["average_time"] = component_stats["total_time"] / component_stats["count"]
            else:
                component_stats["average_time"] = 0.0
        
        # Calculate success rate
        if stats["total_processed"] > 0:
            stats["success_rate"] = stats["successful_processing"] / stats["total_processed"]
        else:
            stats["success_rate"] = 0.0
        
        return stats
    
    def get_rule_engine_summary(self) -> Dict[str, Any]:
        """Get rule engine summary"""
        return self.rule_engine.get_rules_summary()
    
    async def validate_reasoning_components(self) -> Dict[str, Any]:
        """Validate all reasoning components"""
        validation_results = {
            "overall_status": "healthy",
            "components": {},
            "issues": []
        }
        
        try:
            # Test tension analyzer
            test_analysis = self.tension_analyzer.analyze_tension(
                "Test tension", "This is a test description for validation"
            )
            validation_results["components"]["tension_analyzer"] = {
                "status": "healthy" if test_analysis else "error",
                "last_test": datetime.now().isoformat()
            }
            
            # Test rule engine
            rule_summary = self.rule_engine.get_rules_summary()
            validation_results["components"]["rule_engine"] = {
                "status": "healthy" if rule_summary["total_rules"] > 0 else "warning",
                "total_rules": rule_summary["total_rules"],
                "enabled_rules": rule_summary["enabled_rules"]
            }
            
            # Test solution generator
            if test_analysis:
                test_solutions = self.solution_generator.generate_solutions(
                    test_analysis, "Test", "Test description"
                )
                validation_results["components"]["solution_generator"] = {
                    "status": "healthy" if test_solutions else "error",
                    "solutions_generated": len(test_solutions)
                }
            
            # Test priority calculator
            if test_analysis:
                test_priority = self.priority_calculator.calculate_priority(
                    test_analysis, "Test", "Test description"
                )
                validation_results["components"]["priority_calculator"] = {
                    "status": "healthy" if test_priority else "error",
                    "calculation_method": test_priority.calculation_method if test_priority else None
                }
            
        except Exception as e:
            validation_results["overall_status"] = "error"
            validation_results["issues"].append(f"Validation error: {str(e)}")
        
        return validation_results
    
    async def process_batch_tensions(self, requests: List[ReasoningRequest]) -> List[ReasoningResult]:
        """Process multiple tensions in parallel"""
        self.logger.info(f"Processing batch of {len(requests)} tensions")
        
        # Process tensions in parallel
        tasks = [self.process_tension(request) for request in requests]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle any exceptions
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                error_result = ReasoningResult(
                    tension_id=requests[i].tension_id,
                    success=False,
                    errors=[f"Processing exception: {str(result)}"]
                )
                processed_results.append(error_result)
            else:
                processed_results.append(result)
        
        return processed_results
    
    def export_reasoning_insights(self) -> Dict[str, Any]:
        """Export insights and patterns from reasoning engine"""
        insights = {
            "performance_metrics": self.get_performance_stats(),
            "rule_effectiveness": self._analyze_rule_effectiveness(),
            "solution_patterns": self._analyze_solution_patterns(),
            "priority_distributions": self._analyze_priority_distributions(),
            "generated_at": datetime.now().isoformat()
        }
        
        return insights
    
    def _analyze_rule_effectiveness(self) -> Dict[str, Any]:
        """Analyze rule engine effectiveness"""
        # In a real implementation, this would analyze historical rule matches
        return {
            "total_rules": len(self.rule_engine.rules),
            "active_rules": len([r for r in self.rule_engine.rules.values() if r.enabled]),
            "rule_conflicts": len(self.rule_engine.detect_rule_conflicts()),
            "most_triggered_rules": []  # Would be populated from historical data
        }
    
    def _analyze_solution_patterns(self) -> Dict[str, Any]:
        """Analyze solution generation patterns"""
        # In a real implementation, this would analyze historical solution data
        return {
            "solution_types_distribution": {},
            "average_solutions_per_tension": 0,
            "most_effective_templates": [],
            "solution_success_rates": {}
        }
    
    def _analyze_priority_distributions(self) -> Dict[str, Any]:
        """Analyze priority calculation distributions"""
        # In a real implementation, this would analyze historical priority data
        return {
            "priority_level_distribution": {
                "critical": 0,
                "high": 0,
                "medium": 0,
                "low": 0
            },
            "average_priority_score": 0,
            "calculation_method_usage": {},
            "priority_accuracy": 0  # Based on actual outcomes
        } 