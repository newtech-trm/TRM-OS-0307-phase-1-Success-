#!/usr/bin/env python3
"""
Conversation Session Manager for TRM-OS v2
==========================================

Quản lý conversation sessions, context tracking, và memory management
cho conversational intelligence.
"""

import asyncio
import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from uuid import uuid4

from trm_api.core.logging_config import get_logger
from .nlp_processor import ParsedIntent, EntityContext, SystemAction

logger = get_logger(__name__)


@dataclass
class ConversationTurn:
    """Một turn trong conversation"""
    turn_id: str
    user_message: str
    parsed_intent: ParsedIntent
    system_actions: List[SystemAction]
    response: str
    timestamp: datetime
    processing_time: float
    

@dataclass
class ConversationContext:
    """Context của conversation session"""
    session_id: str
    user_id: str
    current_topic: Optional[str]
    active_entities: Dict[str, Any]
    conversation_state: str  # 'active', 'waiting', 'completed'
    last_intent: Optional[ParsedIntent]
    accumulated_context: Dict[str, Any]
    turn_count: int = 0  # NEW: Track number of turns
    

@dataclass
class ConversationSession:
    """Complete conversation session"""
    session_id: str
    user_id: str
    start_time: datetime
    last_activity: datetime
    context: ConversationContext
    turns: List[ConversationTurn]
    metadata: Dict[str, Any]
    status: str = "active"  # NEW: Session status
    
    @property
    def turn_count(self) -> int:
        """Get current turn count"""
        return len(self.turns)
    
    @property
    def created_at(self) -> datetime:
        """Alias for start_time"""
        return self.start_time


class ConversationMemory:
    """
    Memory system cho conversations
    
    Lưu trữ và retrieve conversation history, context, và learned patterns.
    """
    
    def __init__(self, max_memory_size: int = 1000):
        self.max_memory_size = max_memory_size
        self.short_term_memory: Dict[str, List[ConversationTurn]] = {}
        self.long_term_memory: Dict[str, Dict[str, Any]] = {}
        self.entity_memory: Dict[str, Dict[str, Any]] = {}
        self.pattern_memory: Dict[str, List[Dict[str, Any]]] = {}
    
    async def store_turn(self, session_id: str, turn: ConversationTurn):
        """Store conversation turn trong memory"""
        if session_id not in self.short_term_memory:
            self.short_term_memory[session_id] = []
        
        self.short_term_memory[session_id].append(turn)
        
        # Maintain memory size
        if len(self.short_term_memory[session_id]) > self.max_memory_size:
            # Move oldest to long-term memory
            oldest_turn = self.short_term_memory[session_id].pop(0)
            await self._archive_to_long_term(session_id, oldest_turn)
    
    async def _archive_to_long_term(self, session_id: str, turn: ConversationTurn):
        """Archive turn to long-term memory"""
        if session_id not in self.long_term_memory:
            self.long_term_memory[session_id] = {
                'turn_count': 0,
                'common_intents': {},
                'frequent_entities': {},
                'conversation_patterns': []
            }
        
        # Update statistics
        self.long_term_memory[session_id]['turn_count'] += 1
        
        # Track intent frequency
        intent_type = turn.parsed_intent.intent_type.value
        if intent_type not in self.long_term_memory[session_id]['common_intents']:
            self.long_term_memory[session_id]['common_intents'][intent_type] = 0
        self.long_term_memory[session_id]['common_intents'][intent_type] += 1
        
        # Track entity frequency
        for entity_type, values in turn.parsed_intent.entities.items():
            if entity_type not in self.long_term_memory[session_id]['frequent_entities']:
                self.long_term_memory[session_id]['frequent_entities'][entity_type] = {}
            
            for value in values if isinstance(values, list) else [values]:
                if value not in self.long_term_memory[session_id]['frequent_entities'][entity_type]:
                    self.long_term_memory[session_id]['frequent_entities'][entity_type][value] = 0
                self.long_term_memory[session_id]['frequent_entities'][entity_type][value] += 1
    
    async def get_relevant_history(self, session_id: str, current_intent: ParsedIntent, limit: int = 5) -> List[ConversationTurn]:
        """Get relevant conversation history cho current intent"""
        if session_id not in self.short_term_memory:
            return []
        
        turns = self.short_term_memory[session_id]
        
        # Filter relevant turns based on intent similarity và entity overlap
        relevant_turns = []
        for turn in reversed(turns[-limit*2:]):  # Look at recent turns
            relevance_score = await self._calculate_relevance(turn, current_intent)
            if relevance_score > 0.3:  # Threshold for relevance
                relevant_turns.append((turn, relevance_score))
        
        # Sort by relevance và return top results
        relevant_turns.sort(key=lambda x: x[1], reverse=True)
        return [turn for turn, score in relevant_turns[:limit]]
    
    async def _calculate_relevance(self, turn: ConversationTurn, current_intent: ParsedIntent) -> float:
        """Calculate relevance score between past turn và current intent"""
        score = 0.0
        
        # Intent similarity
        if turn.parsed_intent.intent_type == current_intent.intent_type:
            score += 0.5
        
        # Entity overlap
        past_entities = set()
        current_entities = set()
        
        for entities in turn.parsed_intent.entities.values():
            if isinstance(entities, list):
                past_entities.update(entities)
            else:
                past_entities.add(entities)
        
        for entities in current_intent.entities.values():
            if isinstance(entities, list):
                current_entities.update(entities)
            else:
                current_entities.add(entities)
        
        if past_entities and current_entities:
            overlap = len(past_entities.intersection(current_entities))
            union = len(past_entities.union(current_entities))
            score += 0.3 * (overlap / union) if union > 0 else 0
        
        # Temporal proximity (recent turns more relevant)
        time_diff = (datetime.now() - turn.timestamp).total_seconds()
        time_factor = max(0, 1 - time_diff / 3600)  # Decay over 1 hour
        score *= (0.5 + 0.5 * time_factor)
        
        return score


class ConversationSessionManager:
    """
    Core session manager cho conversational intelligence
    
    Quản lý conversation sessions, context tracking, và memory management.
    """
    
    def __init__(self):
        self.active_sessions: Dict[str, ConversationSession] = {}
        self.memory = ConversationMemory()
        self.session_timeout = timedelta(hours=2)  # Session expires after 2 hours
        
    async def create_conversation_session(self, user_id: str, metadata: Optional[Dict[str, Any]] = None) -> ConversationSession:
        """
        Tạo new conversation session
        
        Args:
            user_id: ID của user
            metadata: Optional metadata cho session
            
        Returns:
            ConversationSession mới được tạo
        """
        try:
            session_id = str(uuid4())
            now = datetime.now()
            
            context = ConversationContext(
                session_id=session_id,
                user_id=user_id,
                current_topic=None,
                active_entities={},
                conversation_state='active',
                last_intent=None,
                accumulated_context={},
                turn_count=0  # Initialize turn count
            )
            
            session = ConversationSession(
                session_id=session_id,
                user_id=user_id,
                start_time=now,
                last_activity=now,
                context=context,
                turns=[],
                metadata=metadata or {}
            )
            
            self.active_sessions[session_id] = session
            
            logger.info(f"Created conversation session {session_id} for user {user_id}")
            return session
            
        except Exception as e:
            logger.error(f"Error creating conversation session: {e}")
            raise
    
    async def get_session(self, session_id: str) -> Optional[ConversationSession]:
        """Get conversation session by ID"""
        session = self.active_sessions.get(session_id)
        
        if session:
            # Check if session has expired
            if datetime.now() - session.last_activity > self.session_timeout:
                await self.end_conversation_session(session_id)
                return None
        
        return session
    
    async def maintain_conversation_context(self, session_id: str, message: str, parsed_intent: ParsedIntent) -> ConversationContext:
        """
        Maintain và update conversation context
        
        Args:
            session_id: Session ID
            message: User message
            parsed_intent: Parsed intent từ NLP processor
            
        Returns:
            Updated ConversationContext
        """
        try:
            session = await self.get_session(session_id)
            if not session:
                raise ValueError(f"Session {session_id} not found or expired")
            
            # Update last activity
            session.last_activity = datetime.now()
            
            # Update context với new information
            context = session.context
            
            # Update current topic based on intent
            await self._update_current_topic(context, parsed_intent)
            
            # Merge entities với accumulated context
            await self._merge_entities(context, parsed_intent.entities)
            
            # Update conversation state
            await self._update_conversation_state(context, parsed_intent)
            
            # Store last intent
            context.last_intent = parsed_intent
            
            # Increment turn count
            context.turn_count += 1
            
            # Add to accumulated context
            context.accumulated_context.update({
                'last_message': message,
                'last_intent_type': parsed_intent.intent_type.value,
                'last_confidence': parsed_intent.confidence,
                'turn_count': context.turn_count
            })
            
            logger.info(f"Updated context for session {session_id}")
            return context
            
        except Exception as e:
            logger.error(f"Error maintaining conversation context: {e}")
            raise
    
    async def _update_current_topic(self, context: ConversationContext, parsed_intent: ParsedIntent):
        """Update current conversation topic"""
        intent_to_topic = {
            'create_project': 'project_creation',
            'analyze_tension': 'problem_analysis',
            'get_agent_help': 'agent_assistance',
            'check_status': 'status_inquiry',
            'generate_solution': 'solution_generation',
            'search_knowledge': 'knowledge_search'
        }
        
        new_topic = intent_to_topic.get(parsed_intent.intent_type.value)
        if new_topic and new_topic != context.current_topic:
            context.current_topic = new_topic
    
    async def _merge_entities(self, context: ConversationContext, new_entities: Dict[str, Any]):
        """Merge new entities với accumulated entities"""
        for entity_type, values in new_entities.items():
            if entity_type not in context.active_entities:
                context.active_entities[entity_type] = []
            
            # Add new values, avoiding duplicates
            if isinstance(values, list):
                for value in values:
                    if value not in context.active_entities[entity_type]:
                        context.active_entities[entity_type].append(value)
            else:
                if values not in context.active_entities[entity_type]:
                    context.active_entities[entity_type].append(values)
    
    async def _update_conversation_state(self, context: ConversationContext, parsed_intent: ParsedIntent):
        """Update conversation state based on intent và context"""
        # If user asks for help or has low confidence intent, set to waiting
        if parsed_intent.intent_type.value == 'get_agent_help' or parsed_intent.confidence < 0.5:
            context.conversation_state = 'waiting'
        
        # If clear actionable intent, set to active
        elif parsed_intent.confidence > 0.7:
            context.conversation_state = 'active'
    
    async def add_conversation_turn(self, session_id: str, user_message: str, parsed_intent: ParsedIntent, 
                                 system_actions: List[SystemAction], response: str, processing_time: float):
        """
        Add conversation turn to session
        
        Args:
            session_id: Session ID
            user_message: User's message
            parsed_intent: Parsed intent
            system_actions: Actions taken by system
            response: System's response
            processing_time: Time taken to process
        """
        try:
            session = await self.get_session(session_id)
            if not session:
                raise ValueError(f"Session {session_id} not found")
            
            turn = ConversationTurn(
                turn_id=str(uuid4()),
                user_message=user_message,
                parsed_intent=parsed_intent,
                system_actions=system_actions,
                response=response,
                timestamp=datetime.now(),
                processing_time=processing_time
            )
            
            session.turns.append(turn)
            
            # Store trong memory
            await self.memory.store_turn(session_id, turn)
            
            logger.info(f"Added turn to session {session_id}")
            
        except Exception as e:
            logger.error(f"Error adding conversation turn: {e}")
            raise
    
    async def get_conversation_history(self, session_id: str, limit: int = 10) -> List[ConversationTurn]:
        """Get conversation history cho session"""
        session = await self.get_session(session_id)
        if not session:
            return []
        
        return session.turns[-limit:] if limit > 0 else session.turns
    
    async def get_contextual_suggestions(self, session_id: str, current_intent: ParsedIntent) -> List[Dict[str, Any]]:
        """
        Get contextual suggestions based on conversation history
        
        Args:
            session_id: Session ID
            current_intent: Current parsed intent
            
        Returns:
            List of suggestions
        """
        try:
            session = await self.get_session(session_id)
            if not session:
                return []
            
            suggestions = []
            
            # Get relevant history
            relevant_turns = await self.memory.get_relevant_history(session_id, current_intent)
            
            # Generate suggestions based on context
            if session.context.current_topic:
                topic_suggestions = await self._get_topic_suggestions(session.context.current_topic, current_intent)
                suggestions.extend(topic_suggestions)
            
            # Generate entity-based suggestions
            if session.context.active_entities:
                entity_suggestions = await self._get_entity_suggestions(session.context.active_entities, current_intent)
                suggestions.extend(entity_suggestions)
            
            # Generate pattern-based suggestions
            if relevant_turns:
                pattern_suggestions = await self._get_pattern_suggestions(relevant_turns, current_intent)
                suggestions.extend(pattern_suggestions)
            
            return suggestions[:5]  # Return top 5 suggestions
            
        except Exception as e:
            logger.error(f"Error getting contextual suggestions: {e}")
            return []
    
    async def _get_topic_suggestions(self, topic: str, current_intent: ParsedIntent) -> List[Dict[str, Any]]:
        """Get suggestions based on current topic"""
        topic_suggestions = {
            'project_creation': [
                {'type': 'action', 'text': 'Bạn có muốn thêm thành viên vào dự án không?'},
                {'type': 'action', 'text': 'Tôi có thể giúp bạn lập timeline cho dự án'},
                {'type': 'question', 'text': 'Dự án này có deadline cụ thể không?'}
            ],
            'problem_analysis': [
                {'type': 'action', 'text': 'Tôi có thể phân tích root cause của vấn đề'},
                {'type': 'action', 'text': 'Bạn có muốn tôi đề xuất giải pháp không?'},
                {'type': 'question', 'text': 'Vấn đề này có ảnh hưởng đến deadline không?'}
            ],
            'agent_assistance': [
                {'type': 'action', 'text': 'Tôi có thể kết nối bạn với agent phù hợp'},
                {'type': 'action', 'text': 'Bạn có muốn xem danh sách agents khả dụng không?'},
                {'type': 'question', 'text': 'Bạn cần hỗ trợ gì cụ thể?'}
            ]
        }
        
        return topic_suggestions.get(topic, [])
    
    async def _get_entity_suggestions(self, active_entities: Dict[str, Any], current_intent: ParsedIntent) -> List[Dict[str, Any]]:
        """Get suggestions based on active entities"""
        suggestions = []
        
        if 'project_name' in active_entities:
            suggestions.append({
                'type': 'action',
                'text': f'Bạn có muốn xem trạng thái của {active_entities["project_name"][0]} không?'
            })
        
        if 'agent_type' in active_entities:
            suggestions.append({
                'type': 'action', 
                'text': f'Tôi có thể kết nối bạn với {active_entities["agent_type"][0]} agent'
            })
        
        return suggestions
    
    async def _get_pattern_suggestions(self, relevant_turns: List[ConversationTurn], current_intent: ParsedIntent) -> List[Dict[str, Any]]:
        """Get suggestions based on conversation patterns"""
        suggestions = []
        
        # Analyze patterns trong relevant turns
        intent_sequence = [turn.parsed_intent.intent_type.value for turn in relevant_turns]
        
        # Common follow-up patterns
        if 'create_project' in intent_sequence and current_intent.intent_type.value == 'get_agent_help':
            suggestions.append({
                'type': 'action',
                'text': 'Bạn có muốn tôi assign agents cho dự án mới không?'
            })
        
        if 'analyze_tension' in intent_sequence and current_intent.intent_type.value == 'generate_solution':
            suggestions.append({
                'type': 'action',
                'text': 'Tôi có thể tạo action plan dựa trên analysis vừa rồi'
            })
        
        return suggestions
    
    async def end_conversation_session(self, session_id: str) -> bool:
        """
        End conversation session và cleanup
        
        Args:
            session_id: Session ID to end
            
        Returns:
            True if successful, False if session not found
        """
        try:
            if session_id in self.active_sessions:
                session = self.active_sessions[session_id]
                session.context.conversation_state = 'completed'
                
                # Archive session data
                await self._archive_session(session)
                
                # Remove từ active sessions
                del self.active_sessions[session_id]
                
                logger.info(f"Ended conversation session {session_id}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error ending conversation session: {e}")
            return False
    
    async def _archive_session(self, session: ConversationSession):
        """Archive completed session"""
        # This could be extended to save to database
        session_data = {
            'session_id': session.session_id,
            'user_id': session.user_id,
            'duration': (session.last_activity - session.start_time).total_seconds(),
            'turn_count': len(session.turns),
            'topics_discussed': [session.context.current_topic] if session.context.current_topic else [],
            'entities_mentioned': list(session.context.active_entities.keys())
        }
        
        logger.info(f"Archived session {session.session_id}: {session_data}")
    
    async def cleanup_expired_sessions(self):
        """Cleanup expired sessions (should be called periodically)"""
        now = datetime.now()
        expired_sessions = []
        
        for session_id, session in self.active_sessions.items():
            if now - session.last_activity > self.session_timeout:
                expired_sessions.append(session_id)
        
        for session_id in expired_sessions:
            await self.end_conversation_session(session_id)
        
        logger.info(f"Cleaned up {len(expired_sessions)} expired sessions")
    
    async def get_session_analytics(self, session_id: str) -> Dict[str, Any]:
        """Get analytics for conversation session"""
        session = await self.get_session(session_id)
        if not session:
            return {}
        
        analytics = {
            'session_id': session_id,
            'duration_minutes': (session.last_activity - session.start_time).total_seconds() / 60,
            'turn_count': len(session.turns),
            'average_processing_time': sum(turn.processing_time for turn in session.turns) / len(session.turns) if session.turns else 0,
            'intent_distribution': {},
            'entity_types_used': list(session.context.active_entities.keys()),
            'current_state': session.context.conversation_state,
            'topics_covered': [session.context.current_topic] if session.context.current_topic else []
        }
        
        # Calculate intent distribution
        for turn in session.turns:
            intent = turn.parsed_intent.intent_type.value
            analytics['intent_distribution'][intent] = analytics['intent_distribution'].get(intent, 0) + 1
        
        return analytics 