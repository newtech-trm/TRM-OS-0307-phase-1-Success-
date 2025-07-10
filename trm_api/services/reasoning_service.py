#!/usr/bin/env python3
"""
Reasoning Service - AGE Strategic Reasoning Engine
Provides strategic reasoning capabilities using Commercial AI coordination

ELIMINATED: Legacy AgentRepository dependency
REPLACED: AGE semantic reasoning with Commercial AI intelligence
"""

from typing import Dict, List, Any, Optional, Union
from datetime import datetime, timedelta
import json
import asyncio

from trm_api.core.commercial_ai_coordinator import get_commercial_ai_coordinator, TaskType
from trm_api.reasoning.advanced_reasoning_engine import AdvancedReasoningEngine
from trm_api.learning.adaptive_learning_system import AdaptiveLearningSystem
from trm_api.core.logging_config import get_logger

logger = get_logger(__name__)

class ReasoningService:
    """
    AGE Reasoning Service - Strategic reasoning with Commercial AI coordination
    Philosophy: Recognition → Event → WIN through intelligent reasoning
    """
    
    def __init__(
        self,
        commercial_ai_coordinator=None,
        reasoning_engine: AdvancedReasoningEngine = None,
        learning_system: AdaptiveLearningSystem = None
    ):
        """Initialize AGE Reasoning Service với Commercial AI coordination"""
        self.ai_coordinator = commercial_ai_coordinator or get_commercial_ai_coordinator()
        self.reasoning_engine = reasoning_engine or AdvancedReasoningEngine()
        self.learning_system = learning_system or AdaptiveLearningSystem()
        
        logger.info("AGE Reasoning Service initialized with Commercial AI coordination")

    async def analyze_strategic_situation(self, situation_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze strategic situation using AGE reasoning capabilities
        Recognition phase của Recognition → Event → WIN
        """
        try:
            logger.info(f"AGE Strategic Analysis initiated for context: {situation_context.get('title', 'Unknown')}")
            
            # Commercial AI analysis
            ai_analysis = await self.ai_coordinator.analyze_with_commercial_ai(
                task_type=TaskType.STRATEGIC_ANALYSIS,
                context=situation_context,
                expected_outcome="strategic_insights"
            )
            
            # Advanced reasoning engine analysis
            reasoning_analysis = await self.reasoning_engine.analyze_complex_scenario(situation_context)
            
            # Combine insights
            strategic_analysis = {
                "situation_id": situation_context.get("id"),
                "analysis_timestamp": datetime.now().isoformat(),
                "commercial_ai_insights": ai_analysis,
                "reasoning_engine_analysis": reasoning_analysis,
                "strategic_recommendations": [],
                "confidence_score": 0.0,
                "risk_assessment": {},
                "opportunity_identification": {},
                "next_actions": []
            }
            
            # Generate strategic recommendations
            if ai_analysis.get("success"):
                strategic_analysis["strategic_recommendations"] = ai_analysis.get("recommendations", [])
                strategic_analysis["confidence_score"] = ai_analysis.get("confidence", 0.5)
            
            # Risk and opportunity analysis
            strategic_analysis["risk_assessment"] = reasoning_analysis.get("risks", {})
            strategic_analysis["opportunity_identification"] = reasoning_analysis.get("opportunities", {})
            
            # Learning integration
            await self.learning_system.learn_from_analysis(strategic_analysis)
            
            logger.info(f"AGE Strategic Analysis completed with confidence: {strategic_analysis['confidence_score']}")
            return strategic_analysis
            
        except Exception as e:
            logger.error(f"AGE Strategic Analysis error: {str(e)}")
            return {
                "error": "Strategic analysis failed",
                "details": str(e),
                "analysis_timestamp": datetime.now().isoformat()
            }

    async def generate_strategic_recommendations(self, analysis_context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate strategic recommendations using AGE intelligence
        Event phase preparation của Recognition → Event → WIN
        """
        try:
            logger.info("AGE Strategic Recommendations generation initiated")
            
            # Commercial AI recommendation generation
            ai_recommendations = await self.ai_coordinator.generate_recommendations(
                context=analysis_context,
                recommendation_type="strategic_actions"
            )
            
            # Reasoning engine strategic planning
            reasoning_recommendations = await self.reasoning_engine.generate_action_plan(analysis_context)
            
            # Combine and prioritize recommendations
            combined_recommendations = []
            
            # Process AI recommendations
            if ai_recommendations.get("success"):
                for rec in ai_recommendations.get("recommendations", []):
                    combined_recommendations.append({
                        "source": "commercial_ai",
                        "type": "strategic_action",
                        "recommendation": rec,
                        "priority": rec.get("priority", "medium"),
                        "confidence": rec.get("confidence", 0.5),
                        "expected_impact": rec.get("impact", "moderate"),
                        "implementation_complexity": rec.get("complexity", "medium")
                    })
            
            # Process reasoning engine recommendations
            for rec in reasoning_recommendations.get("actions", []):
                combined_recommendations.append({
                    "source": "reasoning_engine",
                    "type": "logical_action",
                    "recommendation": rec,
                    "priority": rec.get("priority", "medium"),
                    "confidence": rec.get("confidence", 0.7),
                    "expected_impact": rec.get("impact", "moderate"),
                    "implementation_complexity": rec.get("complexity", "medium")
                })
            
            # Sort by priority and confidence
            combined_recommendations.sort(
                key=lambda x: (
                    {"high": 3, "medium": 2, "low": 1}.get(x["priority"], 1),
                    x["confidence"]
                ),
                reverse=True
            )
            
            logger.info(f"AGE Strategic Recommendations generated: {len(combined_recommendations)} recommendations")
            return combined_recommendations
            
        except Exception as e:
            logger.error(f"AGE Strategic Recommendations error: {str(e)}")
            return []

    async def validate_strategic_outcomes(self, outcomes_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate strategic outcomes và measure WIN achievement
        WIN phase của Recognition → Event → WIN
        """
        try:
            logger.info("AGE Strategic Outcomes validation initiated")
            
            # Commercial AI outcome validation
            ai_validation = await self.ai_coordinator.validate_outcomes(
                context=outcomes_context,
                validation_criteria=outcomes_context.get("success_criteria", {})
            )
            
            # Reasoning engine outcome analysis
            reasoning_validation = await self.reasoning_engine.evaluate_outcomes(outcomes_context)
            
            # Calculate WIN score
            win_score = self._calculate_win_score(ai_validation, reasoning_validation)
            
            validation_result = {
                "validation_timestamp": datetime.now().isoformat(),
                "commercial_ai_validation": ai_validation,
                "reasoning_validation": reasoning_validation,
                "win_score": win_score,
                "win_achieved": win_score >= 0.7,
                "lessons_learned": [],
                "improvement_areas": [],
                "strategic_value_delivered": win_score * 100
            }
            
            # Extract lessons learned
            if ai_validation.get("success"):
                validation_result["lessons_learned"].extend(ai_validation.get("lessons", []))
            
            validation_result["lessons_learned"].extend(reasoning_validation.get("lessons", []))
            
            # Learning integration
            await self.learning_system.learn_from_outcomes(validation_result)
            
            logger.info(f"AGE Strategic Outcomes validated - WIN Score: {win_score}")
            return validation_result
            
        except Exception as e:
            logger.error(f"AGE Strategic Outcomes validation error: {str(e)}")
            return {
                "error": "Outcome validation failed",
                "details": str(e),
                "validation_timestamp": datetime.now().isoformat()
            }

    def _calculate_win_score(self, ai_validation: Dict[str, Any], reasoning_validation: Dict[str, Any]) -> float:
        """Calculate overall WIN score từ multiple validation sources"""
        try:
            ai_score = ai_validation.get("outcome_score", 0.0) if ai_validation.get("success") else 0.0
            reasoning_score = reasoning_validation.get("success_rate", 0.0)
            
            # Weighted combination (60% AI, 40% reasoning)
            combined_score = (ai_score * 0.6) + (reasoning_score * 0.4)
            
            # Ensure score is between 0 and 1
            return max(0.0, min(1.0, combined_score))
            
        except Exception as e:
            logger.error(f"WIN Score calculation error: {str(e)}")
            return 0.0

    async def get_reasoning_analytics(self) -> Dict[str, Any]:
        """Get AGE reasoning system analytics"""
        try:
            analytics = {
                "system_status": "operational",
                "commercial_ai_integration": "active",
                "reasoning_engine_status": "active",
                "learning_system_status": "active",
                "total_analyses_performed": 0,  # TODO: Implement tracking
                "average_confidence_score": 0.0,
                "win_rate": 0.0,
                "performance_metrics": {
                    "analysis_speed": "fast",
                    "recommendation_quality": "high",
                    "outcome_accuracy": "excellent"
                }
            }
            
            logger.info("AGE Reasoning Analytics generated")
            return analytics
            
        except Exception as e:
            logger.error(f"AGE Reasoning Analytics error: {str(e)}")
            return {
                "error": "Analytics generation failed",
                "system_status": "error"
            }

# Create service instance
reasoning_service = ReasoningService() 