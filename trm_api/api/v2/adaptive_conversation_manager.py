"""
TRM-OS Adaptive Conversation Manager
Quản lý conversation sessions với adaptive learning capabilities
"""

import asyncio
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from uuid import uuid4
import json

from ...learning.adaptive_learning_system import AdaptiveLearningSystem
from ...learning.learning_types import LearningExperience, ExperienceType, LearningSession
from .conversation_processor import ConversationProcessor, ParsedIntent, EntityContext, Action, ActionResult
from ...services.agent_service import AgentService
from ...services.project_service import ProjectService
from ...services.tension_service import TensionService


@dataclass
class ConversationSession:
    """Represents an active conversation session"""
    session_id: str = field(default_factory=lambda: str(uuid4()))
    user_id: str = ""
    agent_id: str = ""
    start_time: datetime = field(default_factory=datetime.now)
    
    # Conversation history
    messages: List[Dict[str, Any]] = field(default_factory=list)
    intents: List[ParsedIntent] = field(default_factory=list)
    actions: List[Action] = field(default_factory=list)
    results: List[ActionResult] = field(default_factory=list)
    
    # Learning tracking
    learning_session_id: Optional[str] = None
    patterns_discovered: List[str] = field(default_factory=list)
    adaptations_made: List[str] = field(default_factory=list)
    
    # Performance metrics
    intent_accuracy: float = 0.0
    entity_accuracy: float = 0.0
    action_success_rate: float = 0.0
    response_quality: float = 0.0
    
    # Session state
    active: bool = True
    last_activity: datetime = field(default_factory=datetime.now)
    context: Dict[str, Any] = field(default_factory=dict)
    
    # Feedback
    user_feedback: List[Dict[str, Any]] = field(default_factory=list)
    satisfaction_score: Optional[float] = None


@dataclass
class ConversationMetrics:
    """Conversation performance metrics"""
    total_conversations: int = 0
    successful_conversations: int = 0
    average_intent_accuracy: float = 0.0
    average_entity_accuracy: float = 0.0
    average_response_time: float = 0.0
    user_satisfaction: float = 0.0
    
    # Learning metrics
    patterns_discovered: int = 0
    adaptations_applied: int = 0
    improvement_rate: float = 0.0


class AdaptiveConversationManager:
    """
    Quản lý conversation sessions với adaptive learning
    Tích hợp với AdaptiveLearningSystem để continuous improvement
    """
    
    def __init__(self, learning_system: AdaptiveLearningSystem):
        self.learning_system = learning_system
        self.conversation_processor = ConversationProcessor(learning_system)
        
        # Services
        self.agent_service = AgentService()
        self.project_service = ProjectService()
        self.tension_service = TensionService()
        
        # Active sessions
        self.active_sessions: Dict[str, ConversationSession] = {}
        
        # Conversation metrics
        self.metrics = ConversationMetrics()
        
        # Learning configuration
        self.learning_config = {
            "min_sessions_for_pattern": 5,
            "confidence_threshold": 0.7,
            "adaptation_cooldown": 300,  # 5 minutes
            "session_timeout": 3600,     # 1 hour
            "max_active_sessions": 100
        }
        
        # Start background tasks
        self._background_tasks = []
        self._start_background_tasks()
    
    async def create_learning_conversation_session(self, user_id: str, agent_id: str = None) -> ConversationSession:
        """
        Tạo conversation session mới với learning capabilities
        """
        # Auto-assign agent if not provided
        if not agent_id:
            agent_id = await self._select_optimal_agent(user_id)
        
        # Create conversation session
        session = ConversationSession(
            user_id=user_id,
            agent_id=agent_id
        )
        
        # Create learning session
        learning_session = LearningSession(
            agent_id=agent_id,
            session_type="conversation",
            goals=[],  # Will be populated based on conversation
        )
        
        session.learning_session_id = learning_session.session_id
        
        # Store active session
        self.active_sessions[session.session_id] = session
        
        # Learn from session creation
        await self._learn_from_session_creation(session)
        
        return session
    
    async def process_conversation_message(self, session_id: str, message: str) -> Dict[str, Any]:
        """
        Process conversation message với full adaptive learning pipeline
        """
        session = self.active_sessions.get(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        start_time = datetime.now()
        
        try:
            # Step 1: Parse natural language
            parsed_intent = await self.conversation_processor.parse_natural_language_query(message)
            session.intents.append(parsed_intent)
            
            # Step 2: Extract entities and context
            entity_context = await self.conversation_processor.extract_entities_and_context(parsed_intent)
            
            # Step 3: Map to system actions
            actions = await self.conversation_processor.map_intent_to_system_actions(entity_context)
            session.actions.extend(actions)
            
            # Step 4: Execute actions
            results = []
            for action in actions:
                result = await self._execute_action(action)
                results.append(result)
                session.results.append(result)
            
            # Step 5: Generate response
            response = await self._generate_comprehensive_response(results)
            
            # Step 6: Update session
            session.messages.append({
                "type": "user",
                "content": message,
                "timestamp": start_time,
                "intent": parsed_intent.intent.value,
                "confidence": parsed_intent.confidence
            })
            
            session.messages.append({
                "type": "assistant",
                "content": response,
                "timestamp": datetime.now(),
                "actions_count": len(actions),
                "success_rate": sum(1 for r in results if r.success) / len(results) if results else 0
            })
            
            # Step 7: Update metrics
            processing_time = (datetime.now() - start_time).total_seconds()
            await self._update_session_metrics(session, parsed_intent, entity_context, results, processing_time)
            
            # Step 8: Learn from conversation
            await self._learn_from_conversation_interaction(session, message, parsed_intent, entity_context, actions, results, response)
            
            return {
                "session_id": session_id,
                "response": response,
                "intent": parsed_intent.intent.value,
                "confidence": parsed_intent.confidence,
                "actions_executed": len(actions),
                "success_rate": sum(1 for r in results if r.success) / len(results) if results else 0,
                "processing_time": processing_time
            }
            
        except Exception as e:
            # Learn from errors
            await self._learn_from_conversation_error(session, message, str(e))
            raise
        
        finally:
            session.last_activity = datetime.now()
    
    async def get_conversation_suggestions(self, session_id: str) -> List[str]:
        """
        Generate conversation suggestions based on learned patterns
        """
        session = self.active_sessions.get(session_id)
        if not session:
            return []
        
        # Analyze conversation context
        context = await self._analyze_conversation_context(session)
        
        # Generate suggestions based on patterns
        suggestions = []
        
        # Based on conversation history
        if len(session.messages) == 0:
            suggestions.extend([
                "Tạo một agent mới cho dự án của tôi",
                "Kiểm tra trạng thái hệ thống",
                "Phân tích hiệu suất của các agent"
            ])
        else:
            # Analyze recent intents
            recent_intents = [intent.intent.value for intent in session.intents[-3:]]
            
            if "create_agent" in recent_intents:
                suggestions.extend([
                    "Tạo project mới cho agent này",
                    "Cấu hình agent với các capabilities đặc biệt",
                    "Kiểm tra performance của agent"
                ])
            
            if "create_project" in recent_intents:
                suggestions.extend([
                    "Assign agents vào project",
                    "Tạo tasks cho project",
                    "Thiết lập timeline cho project"
                ])
        
        # Learn from suggestion generation
        await self._learn_from_suggestion_generation(session, suggestions)
        
        return suggestions[:5]  # Return top 5 suggestions
    
    async def apply_user_feedback(self, session_id: str, feedback: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply user feedback và learn from it
        """
        session = self.active_sessions.get(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        # Store feedback
        session.user_feedback.append({
            "feedback": feedback,
            "timestamp": datetime.now()
        })
        
        # Process feedback
        adaptation_results = await self.conversation_processor.adapt_nlp_models({"feedback_items": [feedback]})
        
        # Update session metrics
        if "satisfaction_score" in feedback:
            session.satisfaction_score = feedback["satisfaction_score"]
        
        # Learn from feedback
        await self._learn_from_user_feedback(session, feedback)
        
        return {
            "feedback_processed": True,
            "adaptations_applied": adaptation_results.get("adaptations_applied", 0),
            "session_updated": True
        }
    
    async def learn_from_conversation_outcomes(self, session_id: str) -> Dict[str, Any]:
        """
        Learn from overall conversation outcomes
        """
        session = self.active_sessions.get(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        # Analyze conversation success
        success_rate = session.action_success_rate
        satisfaction = session.satisfaction_score or 0.5
        
        # Create comprehensive learning experience
        experience = LearningExperience(
            experience_type=ExperienceType.CONVERSATION_PATTERN,
            agent_id=session.agent_id,
            context={
                "session_id": session_id,
                "message_count": len(session.messages),
                "intent_types": [intent.intent.value for intent in session.intents],
                "user_id": session.user_id
            },
            action_taken={
                "conversation_management": True,
                "intents_processed": len(session.intents),
                "actions_executed": len(session.actions)
            },
            outcome={
                "success_rate": success_rate,
                "satisfaction": satisfaction,
                "learning_patterns": len(session.patterns_discovered),
                "adaptations": len(session.adaptations_made)
            },
            success=success_rate > 0.7 and satisfaction > 0.6,
            performance_before={"baseline_accuracy": 0.5},
            performance_after={
                "intent_accuracy": session.intent_accuracy,
                "entity_accuracy": session.entity_accuracy,
                "response_quality": session.response_quality
            },
            improvement={
                "intent_accuracy": session.intent_accuracy - 0.5,
                "entity_accuracy": session.entity_accuracy - 0.5,
                "response_quality": session.response_quality - 0.5
            },
            confidence_level=0.8,
            importance_weight=1.5,
            tags=["conversation", "nlp", "user_interaction"]
        )
        
        await self.learning_system.learn_from_experience(experience)
        
        # Update global metrics
        await self._update_global_metrics(session)
        
        return {
            "learning_completed": True,
            "patterns_discovered": len(session.patterns_discovered),
            "adaptations_made": len(session.adaptations_made),
            "performance_improvement": session.intent_accuracy - 0.5
        }
    
    async def get_conversation_analytics(self, session_id: str = None) -> Dict[str, Any]:
        """
        Get conversation analytics and learning insights
        """
        if session_id:
            # Single session analytics
            session = self.active_sessions.get(session_id)
            if not session:
                raise ValueError(f"Session {session_id} not found")
            
            return {
                "session_id": session_id,
                "duration": (datetime.now() - session.start_time).total_seconds(),
                "messages": len(session.messages),
                "intents": len(session.intents),
                "actions": len(session.actions),
                "success_rate": session.action_success_rate,
                "intent_accuracy": session.intent_accuracy,
                "entity_accuracy": session.entity_accuracy,
                "response_quality": session.response_quality,
                "satisfaction": session.satisfaction_score,
                "patterns_discovered": len(session.patterns_discovered),
                "adaptations_made": len(session.adaptations_made)
            }
        else:
            # Global analytics
            return {
                "total_sessions": len(self.active_sessions),
                "metrics": {
                    "total_conversations": self.metrics.total_conversations,
                    "successful_conversations": self.metrics.successful_conversations,
                    "success_rate": self.metrics.successful_conversations / max(1, self.metrics.total_conversations),
                    "average_intent_accuracy": self.metrics.average_intent_accuracy,
                    "average_entity_accuracy": self.metrics.average_entity_accuracy,
                    "average_response_time": self.metrics.average_response_time,
                    "user_satisfaction": self.metrics.user_satisfaction,
                    "patterns_discovered": self.metrics.patterns_discovered,
                    "adaptations_applied": self.metrics.adaptations_applied,
                    "improvement_rate": self.metrics.improvement_rate
                }
            }
    
    async def cleanup_expired_sessions(self) -> int:
        """
        Cleanup expired sessions
        """
        expired_sessions = []
        cutoff_time = datetime.now() - timedelta(seconds=self.learning_config["session_timeout"])
        
        for session_id, session in self.active_sessions.items():
            if session.last_activity < cutoff_time:
                expired_sessions.append(session_id)
        
        # Finalize learning for expired sessions
        for session_id in expired_sessions:
            session = self.active_sessions[session_id]
            await self.learn_from_conversation_outcomes(session_id)
            del self.active_sessions[session_id]
        
        return len(expired_sessions)
    
    # Private helper methods
    async def _select_optimal_agent(self, user_id: str) -> str:
        """Select optimal agent based on user history and learning"""
        # Placeholder - would use learning system to select best agent
        return "default_conversation_agent"
    
    async def _execute_action(self, action: Action) -> ActionResult:
        """Execute system action"""
        start_time = datetime.now()
        
        try:
            if action.target_service == "agent_service":
                if action.action_type == "create_agent":
                    result = await self.agent_service.create_agent(action.parameters)
                    return ActionResult(
                        success=True,
                        data=result,
                        message="Agent created successfully",
                        execution_time=(datetime.now() - start_time).total_seconds()
                    )
            
            elif action.target_service == "project_service":
                if action.action_type == "create_project":
                    result = await self.project_service.create_project(action.parameters)
                    return ActionResult(
                        success=True,
                        data=result,
                        message="Project created successfully",
                        execution_time=(datetime.now() - start_time).total_seconds()
                    )
            
            elif action.target_service == "tension_service":
                if action.action_type == "resolve_tension":
                    result = await self.tension_service.resolve_tension(action.parameters)
                    return ActionResult(
                        success=True,
                        data=result,
                        message="Tension resolved successfully",
                        execution_time=(datetime.now() - start_time).total_seconds()
                    )
            
            # Default fallback
            return ActionResult(
                success=False,
                data=None,
                message=f"Unknown action: {action.action_type}",
                execution_time=(datetime.now() - start_time).total_seconds()
            )
            
        except Exception as e:
            return ActionResult(
                success=False,
                data=None,
                message=f"Action failed: {str(e)}",
                execution_time=(datetime.now() - start_time).total_seconds()
            )
    
    async def _generate_comprehensive_response(self, results: List[ActionResult]) -> str:
        """Generate comprehensive response from multiple results"""
        if not results:
            return "❌ Không thể thực hiện yêu cầu"
        
        successful_results = [r for r in results if r.success]
        failed_results = [r for r in results if not r.success]
        
        response_parts = []
        
        # Success messages
        if successful_results:
            response_parts.append(f"✅ Thành công: {len(successful_results)}/{len(results)} actions")
            for result in successful_results:
                response_parts.append(f"  • {result.message}")
        
        # Failure messages
        if failed_results:
            response_parts.append(f"❌ Thất bại: {len(failed_results)}/{len(results)} actions")
            for result in failed_results:
                response_parts.append(f"  • {result.message}")
        
        # Performance summary
        total_time = sum(r.execution_time for r in results)
        response_parts.append(f"⏱️ Tổng thời gian: {total_time:.2f}s")
        
        return "\n".join(response_parts)
    
    async def _update_session_metrics(self, session: ConversationSession, intent: ParsedIntent, 
                                    context: EntityContext, results: List[ActionResult], processing_time: float):
        """Update session performance metrics"""
        # Intent accuracy
        session.intent_accuracy = intent.confidence
        
        # Entity accuracy
        session.entity_accuracy = context.confidence
        
        # Action success rate
        if results:
            session.action_success_rate = sum(1 for r in results if r.success) / len(results)
        
        # Response quality (placeholder - would use more sophisticated metrics)
        session.response_quality = (session.intent_accuracy + session.entity_accuracy + session.action_success_rate) / 3
    
    async def _analyze_conversation_context(self, session: ConversationSession) -> Dict[str, Any]:
        """Analyze conversation context for pattern recognition"""
        return {
            "recent_intents": [intent.intent.value for intent in session.intents[-5:]],
            "success_pattern": session.action_success_rate > 0.7,
            "conversation_length": len(session.messages),
            "time_since_start": (datetime.now() - session.start_time).total_seconds()
        }
    
    async def _learn_from_session_creation(self, session: ConversationSession):
        """Learn from session creation"""
        experience = LearningExperience(
            experience_type=ExperienceType.CONTEXT_UNDERSTANDING,
            agent_id=session.agent_id,
            context={"user_id": session.user_id, "session_type": "conversation"},
            action_taken={"session_created": True},
            outcome={"session_id": session.session_id},
            success=True,
            confidence_level=0.7,
            importance_weight=0.5,
            tags=["session_management", "conversation"]
        )
        await self.learning_system.learn_from_experience(experience)
    
    async def _learn_from_conversation_interaction(self, session: ConversationSession, message: str,
                                                 intent: ParsedIntent, context: EntityContext,
                                                 actions: List[Action], results: List[ActionResult], response: str):
        """Learn from conversation interaction"""
        experience = LearningExperience(
            experience_type=ExperienceType.CONVERSATION_PATTERN,
            agent_id=session.agent_id,
            context={
                "message": message,
                "intent": intent.intent.value,
                "entity_count": len(context.attributes)
            },
            action_taken={
                "actions_executed": len(actions),
                "response_generated": True
            },
            outcome={
                "success_rate": sum(1 for r in results if r.success) / len(results) if results else 0,
                "intent_confidence": intent.confidence,
                "entity_confidence": context.confidence
            },
            success=session.action_success_rate > 0.7,
            performance_before={"baseline": 0.5},
            performance_after={
                "intent_accuracy": session.intent_accuracy,
                "entity_accuracy": session.entity_accuracy,
                "response_quality": session.response_quality
            },
            confidence_level=0.8,
            importance_weight=1.0,
            tags=["conversation", "interaction", "nlp"]
        )
        await self.learning_system.learn_from_experience(experience)
    
    async def _learn_from_conversation_error(self, session: ConversationSession, message: str, error: str):
        """Learn from conversation errors"""
        experience = LearningExperience(
            experience_type=ExperienceType.FEEDBACK_PROCESSING,
            agent_id=session.agent_id,
            context={"message": message, "error": error},
            action_taken={"error_handling": True},
            outcome={"error_occurred": True},
            success=False,
            confidence_level=0.9,
            importance_weight=1.5,
            tags=["error", "conversation", "debugging"]
        )
        await self.learning_system.learn_from_experience(experience)
    
    async def _learn_from_suggestion_generation(self, session: ConversationSession, suggestions: List[str]):
        """Learn from suggestion generation"""
        experience = LearningExperience(
            experience_type=ExperienceType.PATTERN_RECOGNITION,
            agent_id=session.agent_id,
            context={"conversation_context": len(session.messages)},
            action_taken={"suggestions_generated": len(suggestions)},
            outcome={"suggestions": suggestions},
            success=len(suggestions) > 0,
            confidence_level=0.6,
            importance_weight=0.7,
            tags=["suggestions", "pattern_recognition"]
        )
        await self.learning_system.learn_from_experience(experience)
    
    async def _learn_from_user_feedback(self, session: ConversationSession, feedback: Dict[str, Any]):
        """Learn from user feedback"""
        experience = LearningExperience(
            experience_type=ExperienceType.FEEDBACK_ADAPTATION,
            agent_id=session.agent_id,
            context={"feedback_type": feedback.get("type", "general")},
            action_taken={"feedback_processed": True},
            outcome={"feedback_data": feedback},
            success=feedback.get("satisfaction_score", 0.5) > 0.6,
            confidence_level=0.9,
            importance_weight=2.0,
            tags=["feedback", "user_satisfaction", "adaptation"]
        )
        await self.learning_system.learn_from_experience(experience)
    
    async def _update_global_metrics(self, session: ConversationSession):
        """Update global conversation metrics"""
        self.metrics.total_conversations += 1
        
        if session.action_success_rate > 0.7:
            self.metrics.successful_conversations += 1
        
        # Update running averages
        self.metrics.average_intent_accuracy = (
            (self.metrics.average_intent_accuracy * (self.metrics.total_conversations - 1) + session.intent_accuracy) 
            / self.metrics.total_conversations
        )
        
        self.metrics.average_entity_accuracy = (
            (self.metrics.average_entity_accuracy * (self.metrics.total_conversations - 1) + session.entity_accuracy) 
            / self.metrics.total_conversations
        )
        
        if session.satisfaction_score:
            self.metrics.user_satisfaction = (
                (self.metrics.user_satisfaction * (self.metrics.total_conversations - 1) + session.satisfaction_score) 
                / self.metrics.total_conversations
            )
    
    def _start_background_tasks(self):
        """Start background maintenance tasks"""
        # Cleanup task
        cleanup_task = asyncio.create_task(self._background_cleanup())
        self._background_tasks.append(cleanup_task)
        
        # Metrics update task
        metrics_task = asyncio.create_task(self._background_metrics_update())
        self._background_tasks.append(metrics_task)
    
    async def _background_cleanup(self):
        """Background task for session cleanup"""
        while True:
            try:
                await asyncio.sleep(300)  # Run every 5 minutes
                cleaned = await self.cleanup_expired_sessions()
                if cleaned > 0:
                    print(f"Cleaned up {cleaned} expired conversation sessions")
            except Exception as e:
                print(f"Error in background cleanup: {e}")
    
    async def _background_metrics_update(self):
        """Background task for metrics updates"""
        while True:
            try:
                await asyncio.sleep(60)  # Run every minute
                # Update improvement rate based on recent performance
                if self.metrics.total_conversations > 10:
                    recent_success_rate = self.metrics.successful_conversations / self.metrics.total_conversations
                    self.metrics.improvement_rate = recent_success_rate - 0.5  # Baseline improvement
            except Exception as e:
                print(f"Error in background metrics update: {e}")
    
    async def cleanup(self):
        """Cleanup resources"""
        # Cancel background tasks
        for task in self._background_tasks:
            task.cancel()
        
        # Finalize all active sessions
        for session_id in list(self.active_sessions.keys()):
            await self.learn_from_conversation_outcomes(session_id)
        
        self.active_sessions.clear() 