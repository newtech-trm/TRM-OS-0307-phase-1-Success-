#!/usr/bin/env python3
"""
Test Suite for Conversation Session Manager
==========================================

Comprehensive tests cho conversation session management,
context tracking, và memory management.
"""

import pytest
import asyncio
from datetime import datetime, timedelta
from unittest.mock import Mock, patch

from trm_api.v2.conversation.session_manager import (
    ConversationSessionManager,
    ConversationSession,
    ConversationContext,
    ConversationTurn,
    ConversationMemory
)
from trm_api.v2.conversation.nlp_processor import (
    ParsedIntent,
    IntentType,
    SystemAction
)


class TestConversationSessionManager:
    """Test cases cho ConversationSessionManager"""
    
    @pytest.fixture
    def session_manager(self):
        """Create ConversationSessionManager instance"""
        return ConversationSessionManager()
    
    @pytest.fixture
    def sample_parsed_intent(self):
        """Create sample parsed intent"""
        return ParsedIntent(
            intent_type=IntentType.CREATE_PROJECT,
            confidence=0.85,
            entities={'project_name': ['TestProject']},
            context={'language': 'vi', 'urgency_indicators': []},
            original_message="Tạo dự án TestProject",
            language='vi'
        )
    
    @pytest.mark.asyncio
    async def test_create_conversation_session(self, session_manager):
        """Test tạo conversation session mới"""
        user_id = "test_user_123"
        metadata = {"source": "web_app", "version": "v2.0"}
        
        session = await session_manager.create_conversation_session(user_id, metadata)
        
        assert session is not None
        assert session.user_id == user_id
        assert session.metadata == metadata
        assert session.context.conversation_state == 'active'
        assert len(session.turns) == 0
        assert session.session_id in session_manager.active_sessions
    
    @pytest.mark.asyncio
    async def test_get_session(self, session_manager):
        """Test retrieve conversation session"""
        user_id = "test_user_123"
        session = await session_manager.create_conversation_session(user_id)
        
        # Test successful retrieval
        retrieved_session = await session_manager.get_session(session.session_id)
        assert retrieved_session is not None
        assert retrieved_session.session_id == session.session_id
        assert retrieved_session.user_id == user_id
        
        # Test non-existent session
        non_existent = await session_manager.get_session("non_existent_id")
        assert non_existent is None
    
    @pytest.mark.asyncio
    async def test_session_expiration(self, session_manager):
        """Test session expiration logic"""
        user_id = "test_user_123"
        session = await session_manager.create_conversation_session(user_id)
        
        # Manually set last_activity to past
        session.last_activity = datetime.now() - timedelta(hours=3)
        
        # Should return None for expired session
        retrieved_session = await session_manager.get_session(session.session_id)
        assert retrieved_session is None
        
        # Session should be removed from active sessions
        assert session.session_id not in session_manager.active_sessions
    
    @pytest.mark.asyncio
    async def test_maintain_conversation_context(self, session_manager, sample_parsed_intent):
        """Test conversation context maintenance"""
        user_id = "test_user_123"
        session = await session_manager.create_conversation_session(user_id)
        
        message = "Tạo dự án TestProject"
        context = await session_manager.maintain_conversation_context(
            session.session_id, message, sample_parsed_intent
        )
        
        assert context is not None
        assert context.current_topic == 'project_creation'
        assert context.last_intent == sample_parsed_intent
        assert 'project_name' in context.active_entities
        assert 'TestProject' in context.active_entities['project_name']
        assert context.accumulated_context['last_message'] == message
        assert context.accumulated_context['turn_count'] == 1
    
    @pytest.mark.asyncio
    async def test_entity_merging(self, session_manager):
        """Test entity merging trong conversation context"""
        user_id = "test_user_123"
        session = await session_manager.create_conversation_session(user_id)
        
        # First intent với project entity
        intent1 = ParsedIntent(
            intent_type=IntentType.CREATE_PROJECT,
            confidence=0.8,
            entities={'project_name': ['Project1']},
            context={},
            original_message="Tạo Project1",
            language='vi'
        )
        
        context1 = await session_manager.maintain_conversation_context(
            session.session_id, "Tạo Project1", intent1
        )
        
        # Second intent với agent entity
        intent2 = ParsedIntent(
            intent_type=IntentType.GET_AGENT_HELP,
            confidence=0.9,
            entities={'agent_type': ['data_analyst']},
            context={},
            original_message="Cần data analyst",
            language='vi'
        )
        
        context2 = await session_manager.maintain_conversation_context(
            session.session_id, "Cần data analyst", intent2
        )
        
        # Should have both entities
        assert 'project_name' in context2.active_entities
        assert 'agent_type' in context2.active_entities
        assert 'Project1' in context2.active_entities['project_name']
        assert 'data_analyst' in context2.active_entities['agent_type']
    
    @pytest.mark.asyncio
    async def test_conversation_state_updates(self, session_manager):
        """Test conversation state updates"""
        user_id = "test_user_123"
        session = await session_manager.create_conversation_session(user_id)
        
        # Low confidence intent should set state to waiting
        low_confidence_intent = ParsedIntent(
            intent_type=IntentType.UNKNOWN,
            confidence=0.3,
            entities={},
            context={},
            original_message="Không rõ",
            language='vi'
        )
        
        context = await session_manager.maintain_conversation_context(
            session.session_id, "Không rõ", low_confidence_intent
        )
        
        assert context.conversation_state == 'waiting'
        
        # High confidence intent should set state to active
        high_confidence_intent = ParsedIntent(
            intent_type=IntentType.CREATE_PROJECT,
            confidence=0.9,
            entities={'project_name': ['TestProject']},
            context={},
            original_message="Tạo dự án TestProject",
            language='vi'
        )
        
        context = await session_manager.maintain_conversation_context(
            session.session_id, "Tạo dự án TestProject", high_confidence_intent
        )
        
        assert context.conversation_state == 'active'
    
    @pytest.mark.asyncio
    async def test_add_conversation_turn(self, session_manager, sample_parsed_intent):
        """Test adding conversation turn"""
        user_id = "test_user_123"
        session = await session_manager.create_conversation_session(user_id)
        
        system_actions = [
            SystemAction(
                action_type="create_entity",
                parameters={"name": "TestProject"},
                target_endpoint="/api/v1/projects",
                method="POST",
                confidence=0.85
            )
        ]
        
        await session_manager.add_conversation_turn(
            session.session_id,
            "Tạo dự án TestProject",
            sample_parsed_intent,
            system_actions,
            "Đã tạo dự án TestProject thành công",
            0.15
        )
        
        # Check turn was added
        updated_session = await session_manager.get_session(session.session_id)
        assert len(updated_session.turns) == 1
        
        turn = updated_session.turns[0]
        assert turn.user_message == "Tạo dự án TestProject"
        assert turn.parsed_intent == sample_parsed_intent
        assert len(turn.system_actions) == 1
        assert turn.response == "Đã tạo dự án TestProject thành công"
        assert turn.processing_time == 0.15
    
    @pytest.mark.asyncio
    async def test_get_conversation_history(self, session_manager, sample_parsed_intent):
        """Test getting conversation history"""
        user_id = "test_user_123"
        session = await session_manager.create_conversation_session(user_id)
        
        # Add multiple turns
        for i in range(5):
            await session_manager.add_conversation_turn(
                session.session_id,
                f"Message {i}",
                sample_parsed_intent,
                [],
                f"Response {i}",
                0.1
            )
        
        # Test getting limited history
        history = await session_manager.get_conversation_history(session.session_id, 3)
        assert len(history) == 3
        assert history[0].user_message == "Message 2"  # Last 3 messages
        assert history[2].user_message == "Message 4"
        
        # Test getting all history
        all_history = await session_manager.get_conversation_history(session.session_id, 0)
        assert len(all_history) == 5
    
    @pytest.mark.asyncio
    async def test_contextual_suggestions(self, session_manager):
        """Test contextual suggestions generation"""
        user_id = "test_user_123"
        session = await session_manager.create_conversation_session(user_id)
        
        # Set up context
        session.context.current_topic = 'project_creation'
        session.context.active_entities = {
            'project_name': ['TestProject'],
            'agent_type': ['data_analyst']
        }
        
        current_intent = ParsedIntent(
            intent_type=IntentType.CHECK_STATUS,
            confidence=0.8,
            entities={},
            context={},
            original_message="Trạng thái thế nào?",
            language='vi'
        )
        
        suggestions = await session_manager.get_contextual_suggestions(
            session.session_id, current_intent
        )
        
        assert len(suggestions) > 0
        assert any('TestProject' in suggestion.get('text', '') for suggestion in suggestions)
    
    @pytest.mark.asyncio
    async def test_end_conversation_session(self, session_manager):
        """Test ending conversation session"""
        user_id = "test_user_123"
        session = await session_manager.create_conversation_session(user_id)
        session_id = session.session_id
        
        # End session
        success = await session_manager.end_conversation_session(session_id)
        assert success is True
        
        # Session should be removed
        assert session_id not in session_manager.active_sessions
        
        # Should return False for non-existent session
        success = await session_manager.end_conversation_session("non_existent")
        assert success is False
    
    @pytest.mark.asyncio
    async def test_cleanup_expired_sessions(self, session_manager):
        """Test cleanup của expired sessions"""
        user_id = "test_user_123"
        
        # Create sessions
        session1 = await session_manager.create_conversation_session(user_id)
        session2 = await session_manager.create_conversation_session(user_id)
        
        # Make one session expired
        session1.last_activity = datetime.now() - timedelta(hours=3)
        
        # Run cleanup
        await session_manager.cleanup_expired_sessions()
        
        # Expired session should be removed
        assert session1.session_id not in session_manager.active_sessions
        # Active session should remain
        assert session2.session_id in session_manager.active_sessions
    
    @pytest.mark.asyncio
    async def test_session_analytics(self, session_manager, sample_parsed_intent):
        """Test session analytics generation"""
        user_id = "test_user_123"
        session = await session_manager.create_conversation_session(user_id)
        
        # Add some turns với different intents
        intents = [
            IntentType.CREATE_PROJECT,
            IntentType.ANALYZE_TENSION,
            IntentType.CREATE_PROJECT,
            IntentType.GET_AGENT_HELP
        ]
        
        for i, intent_type in enumerate(intents):
            intent = ParsedIntent(
                intent_type=intent_type,
                confidence=0.8,
                entities={},
                context={},
                original_message=f"Message {i}",
                language='vi'
            )
            
            await session_manager.add_conversation_turn(
                session.session_id,
                f"Message {i}",
                intent,
                [],
                f"Response {i}",
                0.1 + i * 0.05  # Varying processing times
            )
        
        analytics = await session_manager.get_session_analytics(session.session_id)
        
        assert analytics['session_id'] == session.session_id
        assert analytics['turn_count'] == 4
        assert analytics['average_processing_time'] > 0
        assert 'intent_distribution' in analytics
        assert analytics['intent_distribution']['create_project'] == 2
        assert analytics['intent_distribution']['analyze_tension'] == 1
        assert analytics['intent_distribution']['get_agent_help'] == 1


class TestConversationMemory:
    """Test cases cho ConversationMemory"""
    
    @pytest.fixture
    def memory(self):
        """Create ConversationMemory instance"""
        return ConversationMemory(max_memory_size=5)
    
    @pytest.fixture
    def sample_turn(self):
        """Create sample conversation turn"""
        intent = ParsedIntent(
            intent_type=IntentType.CREATE_PROJECT,
            confidence=0.8,
            entities={'project_name': ['TestProject']},
            context={},
            original_message="Tạo dự án TestProject",
            language='vi'
        )
        
        return ConversationTurn(
            turn_id="turn_123",
            user_message="Tạo dự án TestProject",
            parsed_intent=intent,
            system_actions=[],
            response="Đã tạo dự án thành công",
            timestamp=datetime.now(),
            processing_time=0.15
        )
    
    @pytest.mark.asyncio
    async def test_store_turn(self, memory, sample_turn):
        """Test storing conversation turn trong memory"""
        session_id = "session_123"
        
        await memory.store_turn(session_id, sample_turn)
        
        assert session_id in memory.short_term_memory
        assert len(memory.short_term_memory[session_id]) == 1
        assert memory.short_term_memory[session_id][0] == sample_turn
    
    @pytest.mark.asyncio
    async def test_memory_size_limit(self, memory):
        """Test memory size limit và archiving"""
        session_id = "session_123"
        
        # Add more turns than memory limit
        for i in range(7):  # Limit is 5
            turn = ConversationTurn(
                turn_id=f"turn_{i}",
                user_message=f"Message {i}",
                parsed_intent=ParsedIntent(
                    intent_type=IntentType.CREATE_PROJECT,
                    confidence=0.8,
                    entities={},
                    context={},
                    original_message=f"Message {i}",
                    language='vi'
                ),
                system_actions=[],
                response=f"Response {i}",
                timestamp=datetime.now(),
                processing_time=0.1
            )
            
            await memory.store_turn(session_id, turn)
        
        # Should only keep last 5 turns
        assert len(memory.short_term_memory[session_id]) == 5
        
        # Oldest turns should be archived
        assert session_id in memory.long_term_memory
        assert memory.long_term_memory[session_id]['turn_count'] == 2  # 2 archived turns
    
    @pytest.mark.asyncio
    async def test_get_relevant_history(self, memory):
        """Test getting relevant history based on current intent"""
        session_id = "session_123"
        
        # Add turns với different intents
        intents = [
            IntentType.CREATE_PROJECT,
            IntentType.ANALYZE_TENSION,
            IntentType.CREATE_PROJECT,  # Similar to current
            IntentType.GET_AGENT_HELP
        ]
        
        for i, intent_type in enumerate(intents):
            turn = ConversationTurn(
                turn_id=f"turn_{i}",
                user_message=f"Message {i}",
                parsed_intent=ParsedIntent(
                    intent_type=intent_type,
                    confidence=0.8,
                    entities={'project_name': ['TestProject']} if intent_type == IntentType.CREATE_PROJECT else {},
                    context={},
                    original_message=f"Message {i}",
                    language='vi'
                ),
                system_actions=[],
                response=f"Response {i}",
                timestamp=datetime.now() - timedelta(minutes=i),
                processing_time=0.1
            )
            
            await memory.store_turn(session_id, turn)
        
        # Query với CREATE_PROJECT intent
        current_intent = ParsedIntent(
            intent_type=IntentType.CREATE_PROJECT,
            confidence=0.8,
            entities={'project_name': ['TestProject']},
            context={},
            original_message="Tạo dự án mới",
            language='vi'
        )
        
        relevant_history = await memory.get_relevant_history(session_id, current_intent, limit=3)
        
        # Should prioritize similar intents và entity overlap
        assert len(relevant_history) > 0
        assert any(turn.parsed_intent.intent_type == IntentType.CREATE_PROJECT for turn in relevant_history)
    
    @pytest.mark.asyncio
    async def test_relevance_calculation(self, memory):
        """Test relevance calculation between turns"""
        # Create two turns với similar intent và entities
        turn1 = ConversationTurn(
            turn_id="turn_1",
            user_message="Tạo dự án Analytics",
            parsed_intent=ParsedIntent(
                intent_type=IntentType.CREATE_PROJECT,
                confidence=0.8,
                entities={'project_name': ['Analytics']},
                context={},
                original_message="Tạo dự án Analytics",
                language='vi'
            ),
            system_actions=[],
            response="Đã tạo dự án",
            timestamp=datetime.now() - timedelta(minutes=5),
            processing_time=0.1
        )
        
        current_intent = ParsedIntent(
            intent_type=IntentType.CREATE_PROJECT,
            confidence=0.8,
            entities={'project_name': ['Analytics']},
            context={},
            original_message="Kiểm tra dự án Analytics",
            language='vi'
        )
        
        relevance = await memory._calculate_relevance(turn1, current_intent)
        
        # Should have high relevance due to intent match và entity overlap
        assert relevance > 0.5
    
    @pytest.mark.asyncio
    async def test_long_term_memory_statistics(self, memory):
        """Test long-term memory statistics tracking"""
        session_id = "session_123"
        
        # Add turns để trigger archiving
        for i in range(7):
            turn = ConversationTurn(
                turn_id=f"turn_{i}",
                user_message=f"Message {i}",
                parsed_intent=ParsedIntent(
                    intent_type=IntentType.CREATE_PROJECT if i % 2 == 0 else IntentType.ANALYZE_TENSION,
                    confidence=0.8,
                    entities={'project_name': [f'Project{i}']} if i % 2 == 0 else {},
                    context={},
                    original_message=f"Message {i}",
                    language='vi'
                ),
                system_actions=[],
                response=f"Response {i}",
                timestamp=datetime.now(),
                processing_time=0.1
            )
            
            await memory.store_turn(session_id, turn)
        
        # Check long-term memory statistics
        ltm = memory.long_term_memory[session_id]
        
        assert ltm['turn_count'] == 2  # 2 turns archived
        assert 'create_project' in ltm['common_intents']
        assert 'analyze_tension' in ltm['common_intents']
        assert 'project_name' in ltm['frequent_entities']


class TestConversationIntegration:
    """Integration tests cho conversation components"""
    
    @pytest.fixture
    def session_manager(self):
        return ConversationSessionManager()
    
    @pytest.mark.asyncio
    async def test_full_conversation_flow(self, session_manager):
        """Test complete conversation flow từ creation đến completion"""
        user_id = "test_user_123"
        
        # 1. Create session
        session = await session_manager.create_conversation_session(user_id)
        assert session.context.conversation_state == 'active'
        
        # 2. First conversation turn
        intent1 = ParsedIntent(
            intent_type=IntentType.CREATE_PROJECT,
            confidence=0.9,
            entities={'project_name': ['Analytics Dashboard']},
            context={'urgency_indicators': []},
            original_message="Tạo dự án Analytics Dashboard",
            language='vi'
        )
        
        context1 = await session_manager.maintain_conversation_context(
            session.session_id, "Tạo dự án Analytics Dashboard", intent1
        )
        
        await session_manager.add_conversation_turn(
            session.session_id,
            "Tạo dự án Analytics Dashboard",
            intent1,
            [],
            "Đã tạo dự án Analytics Dashboard thành công",
            0.12
        )
        
        # 3. Second conversation turn
        intent2 = ParsedIntent(
            intent_type=IntentType.GET_AGENT_HELP,
            confidence=0.85,
            entities={'agent_type': ['data_analyst']},
            context={},
            original_message="Cần data analyst cho dự án này",
            language='vi'
        )
        
        context2 = await session_manager.maintain_conversation_context(
            session.session_id, "Cần data analyst cho dự án này", intent2
        )
        
        await session_manager.add_conversation_turn(
            session.session_id,
            "Cần data analyst cho dự án này",
            intent2,
            [],
            "Đã tìm thấy data analyst phù hợp",
            0.08
        )
        
        # 4. Check accumulated context
        assert context2.current_topic == 'agent_assistance'
        assert 'project_name' in context2.active_entities
        assert 'agent_type' in context2.active_entities
        assert context2.accumulated_context['turn_count'] == 2
        
        # 5. Get suggestions
        suggestions = await session_manager.get_contextual_suggestions(
            session.session_id, intent2
        )
        assert len(suggestions) > 0
        
        # 6. Get analytics
        analytics = await session_manager.get_session_analytics(session.session_id)
        assert analytics['turn_count'] == 2
        assert 'create_project' in analytics['intent_distribution']
        assert 'get_agent_help' in analytics['intent_distribution']
        
        # 7. End session
        success = await session_manager.end_conversation_session(session.session_id)
        assert success is True
    
    @pytest.mark.asyncio
    async def test_concurrent_sessions(self, session_manager):
        """Test handling multiple concurrent sessions"""
        user_ids = ["user_1", "user_2", "user_3"]
        sessions = []
        
        # Create multiple sessions
        for user_id in user_ids:
            session = await session_manager.create_conversation_session(user_id)
            sessions.append(session)
        
        # Add turns to each session concurrently
        tasks = []
        for i, session in enumerate(sessions):
            intent = ParsedIntent(
                intent_type=IntentType.CREATE_PROJECT,
                confidence=0.8,
                entities={'project_name': [f'Project_{i}']},
                context={},
                original_message=f"Tạo dự án Project_{i}",
                language='vi'
            )
            
            task = session_manager.add_conversation_turn(
                session.session_id,
                f"Tạo dự án Project_{i}",
                intent,
                [],
                f"Đã tạo Project_{i}",
                0.1
            )
            tasks.append(task)
        
        # Wait for all tasks to complete
        await asyncio.gather(*tasks)
        
        # Verify all sessions have their turns
        for session in sessions:
            updated_session = await session_manager.get_session(session.session_id)
            assert len(updated_session.turns) == 1
        
        # Cleanup
        for session in sessions:
            await session_manager.end_conversation_session(session.session_id)
    
    @pytest.mark.asyncio
    async def test_error_handling_and_recovery(self, session_manager):
        """Test error handling và recovery mechanisms"""
        user_id = "test_user_123"
        session = await session_manager.create_conversation_session(user_id)
        
        # Test invalid session ID
        try:
            await session_manager.maintain_conversation_context(
                "invalid_session_id", "Test message", None
            )
            assert False, "Should have raised ValueError"
        except ValueError:
            pass  # Expected
        
        # Test với malformed intent
        malformed_intent = ParsedIntent(
            intent_type=IntentType.UNKNOWN,
            confidence=0.0,
            entities={},
            context={'error': 'Parsing failed'},
            original_message="Invalid input",
            language='unknown'
        )
        
        # Should handle gracefully
        context = await session_manager.maintain_conversation_context(
            session.session_id, "Invalid input", malformed_intent
        )
        
        assert context.conversation_state == 'waiting'  # Low confidence sets to waiting
        assert context.last_intent == malformed_intent 