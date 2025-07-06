"""
Comprehensive Test Suite for TRM-OS Conversational Interface
Tests cho Natural Language Processing với Adaptive Learning Integration
"""

import pytest
import asyncio
from datetime import datetime, timedelta
from unittest.mock import Mock, AsyncMock, patch
from typing import Dict, List, Any

from trm_api.api.v2.conversation_processor import ConversationProcessor, IntentType, ParsedIntent, EntityContext, Action, ActionResult
from trm_api.api.v2.adaptive_conversation_manager import AdaptiveConversationManager, ConversationSession, ConversationMetrics
from trm_api.learning.adaptive_learning_system import AdaptiveLearningSystem
from trm_api.learning.learning_types import LearningExperience, ExperienceType


class TestConversationProcessor:
    """Test suite for ConversationProcessor"""
    
    @pytest.fixture
    def learning_system(self):
        """Create mock learning system"""
        system = Mock(spec=AdaptiveLearningSystem)
        system.learn_from_experience = AsyncMock()
        return system
    
    @pytest.fixture
    def processor(self, learning_system):
        """Create ConversationProcessor instance"""
        return ConversationProcessor(learning_system)
    
    @pytest.mark.asyncio
    async def test_parse_create_agent_intent(self, processor):
        """Test parsing create agent intent"""
        message = "tạo agent code cho dự án mới"
        
        result = await processor.parse_natural_language_query(message)
        
        assert isinstance(result, ParsedIntent)
        assert result.intent == IntentType.CREATE_AGENT
        assert result.confidence > 0.0
        assert "agent_type" in result.entities
        assert result.entities["agent_type"] == "code"
    
    @pytest.mark.asyncio
    async def test_parse_create_project_intent(self, processor):
        """Test parsing create project intent"""
        message = "tạo project WebApp Dashboard"
        
        result = await processor.parse_natural_language_query(message)
        
        assert result.intent == IntentType.CREATE_PROJECT
        assert result.confidence > 0.0
        assert "project_name" in result.entities
        assert "WebApp Dashboard" in result.entities["project_name"]
    
    @pytest.mark.asyncio
    async def test_parse_resolve_tension_intent(self, processor):
        """Test parsing resolve tension intent"""
        message = "giải quyết tension technical trong hệ thống"
        
        result = await processor.parse_natural_language_query(message)
        
        assert result.intent == IntentType.RESOLVE_TENSION
        assert result.confidence > 0.0
        assert "tension_type" in result.entities
        assert result.entities["tension_type"] == "technical"
    
    @pytest.mark.asyncio
    async def test_parse_unknown_intent(self, processor):
        """Test parsing unknown intent"""
        message = "xyz abc random text"
        
        result = await processor.parse_natural_language_query(message)
        
        assert result.intent == IntentType.UNKNOWN
        assert result.confidence <= 0.2
    
    @pytest.mark.asyncio
    async def test_extract_entities_agent_context(self, processor):
        """Test entity extraction for agent context"""
        intent = ParsedIntent(
            intent=IntentType.CREATE_AGENT,
            entities={"agent_type": "research"},
            confidence=0.8,
            raw_message="tạo agent research"
        )
        
        result = await processor.extract_entities_and_context(intent)
        
        assert isinstance(result, EntityContext)
        assert result.primary_entity == "agent"
        assert result.entity_type == "agent"
        assert "agent_type" in result.attributes
        assert result.attributes["agent_type"] == "RESEARCH"
    
    @pytest.mark.asyncio
    async def test_map_agent_creation_actions(self, processor):
        """Test mapping agent creation to actions"""
        context = EntityContext(
            primary_entity="agent",
            entity_type="agent",
            attributes={"agent_type": "CODE_GENERATOR"},
            relationships=[],
            confidence=0.8
        )
        
        result = await processor.map_intent_to_system_actions(context)
        
        assert len(result) == 1
        assert isinstance(result[0], Action)
        assert result[0].action_type == "create_agent"
        assert result[0].target_service == "agent_service"
        assert result[0].parameters["agent_type"] == "CODE_GENERATOR"
    
    @pytest.mark.asyncio
    async def test_generate_success_response(self, processor):
        """Test generating success response"""
        result = ActionResult(
            success=True,
            data={"id": "agent_123", "type": "CODE_GENERATOR"},
            message="Agent created successfully",
            execution_time=0.5
        )
        
        response = await processor.generate_natural_response(result)
        
        assert "✅" in response
        assert "agent_123" in response
        assert "0.50s" in response
    
    @pytest.mark.asyncio
    async def test_generate_error_response(self, processor):
        """Test generating error response"""
        result = ActionResult(
            success=False,
            data=None,
            message="Agent creation failed",
            execution_time=0.2
        )
        
        response = await processor.generate_natural_response(result)
        
        assert "❌" in response
        assert "Agent creation failed" in response
        assert "0.20s" in response
    
    @pytest.mark.asyncio
    async def test_learn_from_conversation_patterns(self, processor):
        """Test learning from conversation patterns"""
        conversations = [
            {
                "input": "tạo agent code",
                "success": True,
                "intent_accuracy": 0.9,
                "entity_accuracy": 0.8,
                "response_quality": 0.85
            },
            {
                "input": "tạo project mới",
                "success": True,
                "intent_accuracy": 0.85,
                "entity_accuracy": 0.9,
                "response_quality": 0.88
            }
        ]
        
        result = await processor.learn_from_conversation_patterns(conversations)
        
        assert result["patterns_learned"] == 2
        assert len(result["learning_updates"]) == 2
        assert processor.learning_system.learn_from_experience.call_count == 2
    
    @pytest.mark.asyncio
    async def test_adapt_nlp_models(self, processor):
        """Test adapting NLP models from feedback"""
        feedback = {
            "feedback_items": [
                {
                    "type": "intent_correction",
                    "message": "tạo agent mới",
                    "correct_intent": "CREATE_AGENT"
                }
            ]
        }
        
        result = await processor.adapt_nlp_models(feedback)
        
        assert result["adaptations_applied"] == 1
        assert len(result["adaptation_results"]) == 1
        assert processor.learning_system.learn_from_experience.call_count == 1


class TestAdaptiveConversationManager:
    """Test suite for AdaptiveConversationManager"""
    
    @pytest.fixture
    def learning_system(self):
        """Create mock learning system"""
        system = Mock(spec=AdaptiveLearningSystem)
        system.learn_from_experience = AsyncMock()
        return system
    
    @pytest.fixture
    def manager(self, learning_system):
        """Create AdaptiveConversationManager instance"""
        manager = AdaptiveConversationManager(learning_system)
        # Mock services
        manager.agent_service = Mock()
        manager.project_service = Mock()
        manager.tension_service = Mock()
        return manager
    
    @pytest.mark.asyncio
    async def test_create_conversation_session(self, manager):
        """Test creating conversation session"""
        user_id = "user_123"
        
        session = await manager.create_learning_conversation_session(user_id)
        
        assert isinstance(session, ConversationSession)
        assert session.user_id == user_id
        assert session.session_id in manager.active_sessions
        assert session.active is True
        assert session.learning_session_id is not None
    
    @pytest.mark.asyncio
    async def test_process_conversation_message_create_agent(self, manager):
        """Test processing create agent message"""
        # Setup session
        session = await manager.create_learning_conversation_session("user_123")
        
        # Mock agent service
        manager.agent_service.create_agent = AsyncMock(return_value={"id": "agent_123", "type": "CODE_GENERATOR"})
        
        message = "tạo agent code cho dự án"
        
        result = await manager.process_conversation_message(session.session_id, message)
        
        assert result["session_id"] == session.session_id
        assert "response" in result
        assert result["intent"] == "create_agent"
        assert result["confidence"] > 0.0
        assert result["actions_executed"] == 1
        assert result["success_rate"] > 0.0
        
        # Check session updates
        assert len(session.messages) == 2  # User message + assistant response
        assert len(session.intents) == 1
        assert len(session.actions) == 1
    
    @pytest.mark.asyncio
    async def test_process_conversation_message_create_project(self, manager):
        """Test processing create project message"""
        # Setup session
        session = await manager.create_learning_conversation_session("user_123")
        
        # Mock project service
        manager.project_service.create_project = AsyncMock(return_value={"id": "project_123", "name": "New Project"})
        
        message = "tạo project WebApp Dashboard"
        
        result = await manager.process_conversation_message(session.session_id, message)
        
        assert result["session_id"] == session.session_id
        assert result["intent"] == "create_project"
        assert result["actions_executed"] == 1
        assert result["success_rate"] > 0.0
        
        # Verify project service was called
        manager.project_service.create_project.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_process_conversation_message_resolve_tension(self, manager):
        """Test processing resolve tension message"""
        # Setup session
        session = await manager.create_learning_conversation_session("user_123")
        
        # Mock tension service
        manager.tension_service.resolve_tension = AsyncMock(return_value={"id": "tension_123", "confidence": 0.85})
        
        message = "giải quyết tension technical"
        
        result = await manager.process_conversation_message(session.session_id, message)
        
        assert result["session_id"] == session.session_id
        assert result["intent"] == "resolve_tension"
        assert result["actions_executed"] == 1
        assert result["success_rate"] > 0.0
        
        # Verify tension service was called
        manager.tension_service.resolve_tension.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_conversation_suggestions_initial(self, manager):
        """Test getting initial conversation suggestions"""
        session = await manager.create_learning_conversation_session("user_123")
        
        suggestions = await manager.get_conversation_suggestions(session.session_id)
        
        assert isinstance(suggestions, list)
        assert len(suggestions) > 0
        assert "Tạo một agent mới cho dự án của tôi" in suggestions
        assert "Kiểm tra trạng thái hệ thống" in suggestions
    
    @pytest.mark.asyncio
    async def test_get_conversation_suggestions_contextual(self, manager):
        """Test getting contextual conversation suggestions"""
        session = await manager.create_learning_conversation_session("user_123")
        
        # Add some conversation history
        session.intents.append(ParsedIntent(
            intent=IntentType.CREATE_AGENT,
            entities={"agent_type": "code"},
            confidence=0.8,
            raw_message="tạo agent code"
        ))
        
        suggestions = await manager.get_conversation_suggestions(session.session_id)
        
        assert isinstance(suggestions, list)
        assert len(suggestions) > 0
        # Should include agent-related suggestions
        assert any("project" in s.lower() for s in suggestions)
    
    @pytest.mark.asyncio
    async def test_apply_user_feedback(self, manager):
        """Test applying user feedback"""
        session = await manager.create_learning_conversation_session("user_123")
        
        feedback = {
            "type": "satisfaction",
            "satisfaction_score": 0.9,
            "comments": "Very helpful response"
        }
        
        result = await manager.apply_user_feedback(session.session_id, feedback)
        
        assert result["feedback_processed"] is True
        assert session.satisfaction_score == 0.9
        assert len(session.user_feedback) == 1
        
        # Verify learning system was called
        assert manager.learning_system.learn_from_experience.call_count > 0
    
    @pytest.mark.asyncio
    async def test_learn_from_conversation_outcomes(self, manager):
        """Test learning from conversation outcomes"""
        session = await manager.create_learning_conversation_session("user_123")
        
        # Setup session with some data
        session.action_success_rate = 0.8
        session.satisfaction_score = 0.9
        session.intent_accuracy = 0.85
        session.entity_accuracy = 0.8
        session.response_quality = 0.82
        
        result = await manager.learn_from_conversation_outcomes(session.session_id)
        
        assert result["learning_completed"] is True
        assert "patterns_discovered" in result
        assert "adaptations_made" in result
        assert "performance_improvement" in result
        
        # Verify learning system was called
        assert manager.learning_system.learn_from_experience.call_count > 0
    
    @pytest.mark.asyncio
    async def test_get_session_analytics(self, manager):
        """Test getting session analytics"""
        session = await manager.create_learning_conversation_session("user_123")
        
        # Add some test data
        session.messages = [{"type": "user", "content": "test"}]
        session.intents = [ParsedIntent(IntentType.CREATE_AGENT, {}, 0.8, "test")]
        session.actions = [Action("create_agent", "agent_service", {}, 1)]
        session.action_success_rate = 0.8
        session.intent_accuracy = 0.85
        session.entity_accuracy = 0.8
        session.response_quality = 0.82
        session.satisfaction_score = 0.9
        
        analytics = await manager.get_conversation_analytics(session.session_id)
        
        assert analytics["session_id"] == session.session_id
        assert analytics["messages"] == 1
        assert analytics["intents"] == 1
        assert analytics["actions"] == 1
        assert analytics["success_rate"] == 0.8
        assert analytics["intent_accuracy"] == 0.85
        assert analytics["entity_accuracy"] == 0.8
        assert analytics["response_quality"] == 0.82
        assert analytics["satisfaction"] == 0.9
    
    @pytest.mark.asyncio
    async def test_get_global_analytics(self, manager):
        """Test getting global analytics"""
        # Setup some test data
        manager.metrics.total_conversations = 10
        manager.metrics.successful_conversations = 8
        manager.metrics.average_intent_accuracy = 0.85
        manager.metrics.average_entity_accuracy = 0.8
        manager.metrics.user_satisfaction = 0.88
        
        analytics = await manager.get_conversation_analytics()
        
        assert analytics["total_sessions"] == 0  # No active sessions yet
        assert analytics["metrics"]["total_conversations"] == 10
        assert analytics["metrics"]["successful_conversations"] == 8
        assert analytics["metrics"]["success_rate"] == 0.8
        assert analytics["metrics"]["average_intent_accuracy"] == 0.85
        assert analytics["metrics"]["user_satisfaction"] == 0.88
    
    @pytest.mark.asyncio
    async def test_session_cleanup(self, manager):
        """Test session cleanup functionality"""
        # Create session
        session = await manager.create_learning_conversation_session("user_123")
        
        # Make it expired
        session.last_activity = datetime.now() - timedelta(hours=2)
        
        # Run cleanup
        cleaned = await manager.cleanup_expired_sessions()
        
        assert cleaned == 1
        assert session.session_id not in manager.active_sessions
        
        # Verify learning was triggered
        assert manager.learning_system.learn_from_experience.call_count > 0
    
    @pytest.mark.asyncio
    async def test_conversation_error_handling(self, manager):
        """Test error handling in conversation processing"""
        session = await manager.create_learning_conversation_session("user_123")
        
        # Mock service to raise error
        manager.agent_service.create_agent = AsyncMock(side_effect=Exception("Service error"))
        
        message = "tạo agent code"
        
        with pytest.raises(Exception) as exc_info:
            await manager.process_conversation_message(session.session_id, message)
        
        assert "Service error" in str(exc_info.value)
        
        # Verify error learning was triggered
        assert manager.learning_system.learn_from_experience.call_count > 0
    
    @pytest.mark.asyncio
    async def test_concurrent_conversation_processing(self, manager):
        """Test concurrent conversation processing"""
        # Create multiple sessions
        sessions = []
        for i in range(3):
            session = await manager.create_learning_conversation_session(f"user_{i}")
            sessions.append(session)
        
        # Mock services
        manager.agent_service.create_agent = AsyncMock(return_value={"id": "agent_123"})
        
        # Process messages concurrently
        tasks = []
        for i, session in enumerate(sessions):
            task = manager.process_conversation_message(session.session_id, f"tạo agent code {i}")
            tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        
        # Verify all processed successfully
        assert len(results) == 3
        for result in results:
            assert result["success_rate"] > 0.0
            assert result["intent"] == "create_agent"
    
    @pytest.mark.asyncio
    async def test_learning_integration(self, manager):
        """Test integration with learning system"""
        session = await manager.create_learning_conversation_session("user_123")
        
        # Mock successful agent creation
        manager.agent_service.create_agent = AsyncMock(return_value={"id": "agent_123"})
        
        # Process message
        await manager.process_conversation_message(session.session_id, "tạo agent code")
        
        # Apply feedback
        await manager.apply_user_feedback(session.session_id, {
            "type": "satisfaction",
            "satisfaction_score": 0.9
        })
        
        # Finalize session
        await manager.learn_from_conversation_outcomes(session.session_id)
        
        # Verify multiple learning experiences were created
        assert manager.learning_system.learn_from_experience.call_count >= 5
        
        # Verify different experience types were used
        call_args = [call[0][0] for call in manager.learning_system.learn_from_experience.call_args_list]
        experience_types = [exp.experience_type for exp in call_args]
        
        assert ExperienceType.CONVERSATION_PATTERN in experience_types
        assert ExperienceType.FEEDBACK_ADAPTATION in experience_types
    
    @pytest.mark.asyncio
    async def test_cleanup_resources(self, manager):
        """Test cleanup of manager resources"""
        # Create some sessions
        session1 = await manager.create_learning_conversation_session("user_1")
        session2 = await manager.create_learning_conversation_session("user_2")
        
        assert len(manager.active_sessions) == 2
        
        # Cleanup
        await manager.cleanup()
        
        # Verify cleanup
        assert len(manager.active_sessions) == 0
        assert manager.learning_system.learn_from_experience.call_count >= 2  # Learning from session outcomes


@pytest.mark.asyncio
async def test_conversation_system_integration():
    """Integration test for complete conversation system"""
    # Create learning system
    learning_system = Mock(spec=AdaptiveLearningSystem)
    learning_system.learn_from_experience = AsyncMock()
    
    # Create conversation manager
    manager = AdaptiveConversationManager(learning_system)
    
    # Mock services
    manager.agent_service = Mock()
    manager.agent_service.create_agent = AsyncMock(return_value={"id": "agent_123", "type": "CODE_GENERATOR"})
    
    try:
        # Full conversation flow
        session = await manager.create_learning_conversation_session("integration_user")
        
        # Process a message
        result = await manager.process_conversation_message(session.session_id, "tạo agent code cho dự án")
        assert result["success_rate"] >= 0.0
        
        # Get suggestions
        suggestions = await manager.get_conversation_suggestions(session.session_id)
        assert len(suggestions) > 0
        
        # Apply feedback
        feedback_result = await manager.apply_user_feedback(session.session_id, {
            "type": "satisfaction",
            "satisfaction_score": 0.85,
            "comments": "Great conversation experience"
        })
        assert feedback_result["feedback_processed"] is True
        
        # Get analytics
        analytics = await manager.get_conversation_analytics(session.session_id)
        assert analytics["messages"] == 2  # 1 user + 1 assistant message
        assert analytics["intents"] >= 1
        assert analytics["satisfaction"] == 0.85
        
        # Finalize session
        learning_result = await manager.learn_from_conversation_outcomes(session.session_id)
        assert learning_result["learning_completed"] is True
        
        # Verify learning occurred
        assert learning_system.learn_from_experience.call_count >= 5
        
    finally:
        await manager.cleanup()


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 