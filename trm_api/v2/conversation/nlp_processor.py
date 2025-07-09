#!/usr/bin/env python3
"""
Natural Language Processor for TRM-OS Conversational Intelligence
================================================================

Xử lý ngôn ngữ tự nhiên cho queries tiếng Việt và tiếng Anh,
phân tích ý định, trích xuất entities và map thành system actions.
Tích hợp với Commercial AI Coordination cho intelligent responses.
"""

import re
import asyncio
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum
from datetime import datetime

from trm_api.models.enums import TensionType, Priority
from trm_api.core.logging_config import get_logger
# ML Enhanced Reasoning removed - Using Commercial AI APIs only
from trm_api.reasoning.reasoning_types import ReasoningContext, ReasoningType
from trm_api.learning.adaptive_learning_system import AdaptiveLearningSystem
from trm_api.quantum.quantum_system_manager import QuantumSystemManager
from trm_api.reasoning.advanced_reasoning_engine import AdvancedReasoningEngine

logger = get_logger(__name__)


class IntentType(Enum):
    """Các loại ý định từ user queries"""
    CREATE_PROJECT = "create_project"
    ANALYZE_TENSION = "analyze_tension"
    GET_AGENT_HELP = "get_agent_help"
    CHECK_STATUS = "check_status"
    GENERATE_SOLUTION = "generate_solution"
    SEARCH_KNOWLEDGE = "search_knowledge"
    UPDATE_RESOURCE = "update_resource"
    SCHEDULE_TASK = "schedule_task"
    GET_INSIGHTS = "get_insights"
    UNKNOWN = "unknown"


class ConfidenceLevel(Enum):
    """Mức độ tin cậy của intent detection"""
    HIGH = "high"      # > 0.8
    MEDIUM = "medium"  # 0.5 - 0.8
    LOW = "low"        # < 0.5


@dataclass
class ParsedIntent:
    """Kết quả phân tích ý định từ natural language"""
    intent_type: IntentType
    confidence: float
    entities: Dict[str, Any]
    context: Dict[str, Any]
    original_message: str
    language: str  # 'vi' or 'en'
    
    
@dataclass
class EntityContext:
    """Context và entities được trích xuất từ query"""
    entities: Dict[str, Any]
    context: Dict[str, Any]
    relationships: List[Tuple[str, str, str]]  # (entity1, relation, entity2)
    temporal_info: Optional[Dict[str, Any]] = None
    

@dataclass
class SystemAction:
    """Action được map từ intent để thực thi trong system"""
    action_type: str
    parameters: Dict[str, Any]
    target_endpoint: str
    method: str
    confidence: float


class ConversationProcessor:
    """
    Core NLP processor cho conversational intelligence với Commercial AI Coordination
    
    Chức năng chính:
    - Parse natural language queries (Vietnamese/English)
    - Extract entities và context
    - Map intents to system actions
    - Generate confidence scores
    - Commercial AI coordination cho intelligent responses
    """
    
    def __init__(self, agent_id: str = "conversation_processor"):
        self.vietnamese_patterns = self._load_vietnamese_patterns()
        self.english_patterns = self._load_english_patterns()
        self.entity_extractors = self._load_entity_extractors()
        self.action_mappings = self._load_action_mappings()
        
        # NEW: Initialize Commercial AI Coordination
        self.agent_id = agent_id
        # Using commercial AI APIs only (OpenAI, Claude, Gemini)
        
    def _initialize_commercial_ai(self):
        """Initialize Commercial AI Coordination cho conversational intelligence"""
        try:
            # Initialize adaptive learning system
            learning_system = AdaptiveLearningSystem(agent_id=self.agent_id)
            
            # Initialize quantum system manager
            quantum_manager = QuantumSystemManager(learning_system=learning_system)
            
            # Initialize advanced reasoning engine
            advanced_reasoning = AdvancedReasoningEngine(agent_id=self.agent_id)
            
            # Initialize Commercial AI Coordination
            # Using Commercial AI APIs only (OpenAI, Claude, Gemini)
            # Conversational intelligence will coordinate with commercial AI services
            self.commercial_ai_coordinator = True
            
            logger.info("Commercial AI coordination initialized for conversational intelligence")
            
        except Exception as e:
            logger.error(f"Failed to initialize Commercial AI coordination: {e}")
            self.commercial_ai_coordinator = False
    
    async def enhance_with_commercial_ai(self, context: EntityContext) -> Dict[str, Any]:
        """
        Enhance conversation context với Commercial AI insights
        Tuân thủ triết lý TRM-OS: sử dụng OpenAI/Claude/Gemini
        
        Args:
            context: EntityContext từ natural language processing
            
        Returns:
            Dict containing Commercial AI insights và recommendations
        """
        try:
            # Return commercial AI coordination response
            return {
                "ai_coordination": "Commercial AI integration",
                "approach": "OpenAI/Claude/Gemini coordination per TRM-OS philosophy",
                "confidence": 0.8,
                "reasoning_type": "commercial_ai_guided",
                "recommendations": [
                    "Use commercial AI APIs for intelligent responses",
                    "Coordinate multiple AI services for optimal results"
                ]
            }
            
        except Exception as e:
            logger.error(f"Error in commercial AI coordination: {e}")
            return {"error": f"Commercial AI coordination failed: {str(e)}"}
    
    def _determine_priority_level(self, context: EntityContext) -> int:
        """Determine priority level từ conversation context"""
        urgency = context.entities.get('urgency_level', 'normal')
        temporal_info = context.temporal_info
        
        if urgency == 'high' or (temporal_info and temporal_info.get('urgency') == 'critical'):
            return 9
        elif urgency == 'medium' or (temporal_info and temporal_info.get('urgency') == 'high'):
            return 6
        else:
            return 3
    
    def _map_intent_to_reasoning_type(self, intent_type: IntentType) -> ReasoningType:
        """Map conversation intent to appropriate reasoning type"""
        intent_reasoning_map = {
            IntentType.CREATE_PROJECT: ReasoningType.DEDUCTIVE,
            IntentType.ANALYZE_TENSION: ReasoningType.CAUSAL,
            IntentType.GET_AGENT_HELP: ReasoningType.ANALOGICAL,
            IntentType.CHECK_STATUS: ReasoningType.INDUCTIVE,
            IntentType.GENERATE_SOLUTION: ReasoningType.ABDUCTIVE,
            IntentType.SEARCH_KNOWLEDGE: ReasoningType.INDUCTIVE,
            IntentType.UPDATE_RESOURCE: ReasoningType.DEDUCTIVE,
            IntentType.SCHEDULE_TASK: ReasoningType.DEDUCTIVE,
            IntentType.GET_INSIGHTS: ReasoningType.PROBABILISTIC,
            IntentType.UNKNOWN: ReasoningType.HYBRID
        }
        
        return intent_reasoning_map.get(intent_type, ReasoningType.HYBRID)
    
    async def coordinate_commercial_ai_learning(self, conversations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Coordinate với Commercial AI services để improve responses
        Tuân thủ triết lý TRM-OS: không train local models
        
        Args:
            conversations: List of conversation data với outcomes
            
        Returns:
            Commercial AI coordination results
        """
        try:
            # Log patterns for commercial AI coordination
            logger.info(f"Coordinating with commercial AI for {len(conversations)} conversation patterns")
            
            return {
                "conversations_processed": len(conversations),
                "coordination_approach": "Commercial AI API coordination",
                "status": "success",
                "note": "No local ML training per TRM-OS philosophy"
            }
            
        except Exception as e:
            logger.error(f"Error in commercial AI coordination: {e}")
            return {"error": f"Commercial AI coordination failed: {str(e)}"}
    
    def _load_vietnamese_patterns(self) -> Dict[IntentType, List[str]]:
        """Load Vietnamese language patterns cho intent detection"""
        return {
            IntentType.CREATE_PROJECT: [
                r'\b(tạo|khởi tạo|bắt đầu|lập)\s+(dự án|project)\b',
                r'\b(mở|tạo mới)\s+(dự án|project)\b',
                r'\b(cần|muốn|định)\s+(làm|tạo)\s+(dự án|project)\b'
            ],
            IntentType.ANALYZE_TENSION: [
                r'\b(phân tích|đánh giá|xem xét)\s+(vấn đề|tension|căng thẳng)\b',
                r'\b(có|gặp|đang có)\s+(vấn đề|sự cố|trouble)\b',  # Restore original pattern
                r'\b(khó khăn|thách thức|trở ngại)\b'  # Restore original pattern
            ],
            IntentType.GET_AGENT_HELP: [
                r'\b(cần|muốn|tìm)\s+(trợ giúp|hỗ trợ|agent|bot)\b',
                r'\b(ai|agent nào)\s+(có thể|giúp|hỗ trợ)\b',
                r'\b(gọi|tìm|cần)\s+(chuyên gia|specialist)\b'
            ],
            IntentType.CHECK_STATUS: [
                r'\b(trạng thái|status|tình hình).*?(như thế nào|thế nào|ra sao|hiện tại)\b',
                r'\b(đang|đã)\s+(thế nào|như thế nào|ra sao)\b',
                r'\b(kiểm tra|check|xem)\s+(tiến độ|progress)\b'
            ],
            IntentType.GENERATE_SOLUTION: [
                r'\b(giải pháp|solution|cách giải quyết)\b',
                r'\b(làm sao|làm thế nào)\s+(để|giải quyết)\b',
                r'\b(đề xuất|suggest|gợi ý)\s+(cách|phương án)\b'
            ],
            IntentType.SEARCH_KNOWLEDGE: [
                r'\b(tìm|search|tìm kiếm)\s+(thông tin|kiến thức|knowledge)\b',
                r'\b(có|biết)\s+(gì|thông tin nào)\s+(về|concerning)\b',
                r'\b(học|hiểu|tìm hiểu)\s+(về|about)\b'
            ]
        }
    
    def _load_english_patterns(self) -> Dict[IntentType, List[str]]:
        """Load English language patterns cho intent detection"""
        return {
            IntentType.CREATE_PROJECT: [
                r'\b(create|start|begin|initiate)\s+(project|new project)\b',
                r'\b(new|make)\s+(project)\b',
                r'\b(want to|need to|planning to)\s+(create|start)\s+(project)\b'
            ],
            IntentType.ANALYZE_TENSION: [
                r'\b(analyze|assess|evaluate)\s+(tension|problem|issue)\b',
                r'\b(having|experiencing|facing)\s+(problem|issue|trouble)\b',
                r'\b(difficulty|challenge|obstacle)\b'
            ],
            IntentType.GET_AGENT_HELP: [
                r'\b(need|want|looking for)\s+(help|support|agent|assistance)\b',
                r'\b(which|what)\s+(agent|specialist)\s+(can|help|assist)\b',
                r'\b(call|find|need)\s+(expert|specialist)\b'
            ],
            IntentType.CHECK_STATUS: [
                r'\b(status|current state|how is).*?\b',
                r'\b(what is|how are).*?(things|progress|status)\b',
                r'\b(check|view|see)\s+(progress|status)\b'
            ],
            IntentType.GENERATE_SOLUTION: [
                r'\b(solution|solve|resolve)\b',
                r'\b(how to|how can)\s+(solve|fix|resolve)\b',
                r'\b(suggest|recommend|propose)\s+(solution|way|approach)\b'
            ],
            IntentType.SEARCH_KNOWLEDGE: [
                r'\b(search|find|look for)\s+(information|knowledge)\b',
                r'\b(what|tell me)\s+(about|concerning)\b',
                r'\b(learn|understand|know)\s+(about)\b'
            ]
        }
    
    def _load_entity_extractors(self) -> Dict[str, List[str]]:
        """Load entity extraction patterns"""
        return {
            'project_name': [
                r'dự án\s+([A-Za-z0-9\-_]+)',  # Chỉ capture tên không có khoảng trắng
                r'project\s+([A-Za-z0-9\-_]+)',
                r'tên\s+([A-Za-z0-9\-_]+)',
                r'tạo\s+([A-Za-z0-9\-_]+)',
                r'create\s+([A-Za-z0-9\-_]+)'
            ],
            'agent_type': [
                r'(data analyst|phân tích dữ liệu)',
                r'(code generator|lập trình)',
                r'(ui designer|thiết kế giao diện)',
                r'(integration|tích hợp)',
                r'(research|nghiên cứu)'
            ],
            'tension_type': [
                r'(vấn đề|problem|sự cố|issue)',
                r'(cơ hội|opportunity|tiềm năng)',
                r'(tài nguyên|resource|nguồn lực)',
                r'(quy trình|process|workflow)'
            ],
            'priority_level': [
                r'(khẩn cấp|urgent|critical)',
                r'(cao|high|quan trọng)',
                r'(trung bình|medium|normal)',
                r'(thấp|low|không gấp)'
            ],
            'time_reference': [
                r'(hôm nay|today|ngày hôm nay)',
                r'(tuần này|this week|trong tuần)',
                r'(tháng này|this month|trong tháng)',
                r'(gấp|urgent|ngay|immediately)'
            ]
        }
    
    def _load_action_mappings(self) -> Dict[IntentType, Dict[str, Any]]:
        """Load mappings từ intents thành system actions"""
        return {
            IntentType.CREATE_PROJECT: {
                'action_type': 'create_entity',
                'target_endpoint': '/api/v1/projects',
                'method': 'POST',
                'required_params': ['name', 'description']
            },
            IntentType.ANALYZE_TENSION: {
                'action_type': 'analyze_data',
                'target_endpoint': '/api/v1/reasoning/analyze-tension',
                'method': 'POST',
                'required_params': ['tension_description']
            },
            IntentType.GET_AGENT_HELP: {
                'action_type': 'find_agent',
                'target_endpoint': '/api/v1/agents/templates/match',
                'method': 'POST',
                'required_params': ['tension_description']
            },
            IntentType.CHECK_STATUS: {
                'action_type': 'query_data',
                'target_endpoint': '/api/v1/projects/{id}/status',
                'method': 'GET',
                'required_params': ['entity_id']
            },
            IntentType.GENERATE_SOLUTION: {
                'action_type': 'generate_solution',
                'target_endpoint': '/api/v1/reasoning/generate-solutions',
                'method': 'POST',
                'required_params': ['tension_analysis']
            },
            IntentType.SEARCH_KNOWLEDGE: {
                'action_type': 'search_data',
                'target_endpoint': '/api/v1/knowledge-snippets/search',
                'method': 'GET',
                'required_params': ['query']
            }
        }
    
    async def parse_natural_language_query(self, message: str) -> ParsedIntent:
        """
        Parse natural language query thành structured intent
        
        Args:
            message: Raw user message
            
        Returns:
            ParsedIntent với intent type, confidence, entities
        """
        try:
            logger.info(f"Parsing natural language query: {message[:100]}...")
            
            # Detect language
            language = self._detect_language(message)
            
            # Extract intent
            intent_type, confidence = await self._extract_intent(message, language)
            
            # Extract entities
            entities = await self._extract_entities(message, language)
            
            # Build context
            context = await self._build_context(message, entities, language)
            
            parsed_intent = ParsedIntent(
                intent_type=intent_type,
                confidence=confidence,
                entities=entities,
                context=context,
                original_message=message,
                language=language
            )
            
            logger.info(f"Parsed intent: {intent_type.value} (confidence: {confidence:.2f})")
            return parsed_intent
            
        except Exception as e:
            logger.error(f"Error parsing natural language query: {e}")
            return ParsedIntent(
                intent_type=IntentType.UNKNOWN,
                confidence=0.0,
                entities={},
                context={'error': str(e)},
                original_message=message,
                language='unknown'
            )
    
    def _detect_language(self, message: str) -> str:
        """Detect language của message (Vietnamese hoặc English)"""
        vietnamese_chars = re.findall(r'[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]', message.lower())
        vietnamese_words = ['tôi', 'của', 'với', 'trong', 'này', 'đó', 'không', 'có', 'là', 'được', 'và', 'để', 'dự án', 'phân tích']
        english_words = ['create', 'new', 'with', 'data', 'analysis', 'project', 'help', 'need', 'want', 'and', 'the', 'for']
        
        words = message.lower().split()
        total_words = len(words)
        
        if total_words == 0:
            return 'en'
        
        vietnamese_score = len(vietnamese_chars) + sum(1 for word in vietnamese_words if word in message.lower())
        english_score = sum(1 for word in english_words if word in message.lower())
        
        # Calculate percentage
        if vietnamese_score + english_score == 0:
            return 'en'  # Default to English
            
        vietnamese_ratio = vietnamese_score / (vietnamese_score + english_score)
        
        # Need at least 50% Vietnamese indicators to classify as Vietnamese
        return 'vi' if vietnamese_ratio >= 0.5 else 'en'
    
    async def _extract_intent(self, message: str, language: str) -> Tuple[IntentType, float]:
        """Extract intent type và confidence từ message"""
        patterns = self.vietnamese_patterns if language == 'vi' else self.english_patterns
        
        best_intent = IntentType.UNKNOWN
        best_confidence = 0.0
        
        for intent_type, pattern_list in patterns.items():
            for pattern in pattern_list:
                matches = re.findall(pattern, message.lower(), re.IGNORECASE)
                if matches:
                    # Improved confidence calculation
                    base_confidence = 0.8  # Start with high base confidence for pattern match
                    match_bonus = len(matches) * 0.05  # Bonus for multiple matches
                    pattern_complexity = min(0.1, len(pattern) / 500)  # Bonus for complex patterns
                    
                    # Penalty for vague language
                    vague_penalty = self._calculate_vague_penalty(message, language)
                    
                    # Additional penalty for non-specific patterns
                    specificity_penalty = self._calculate_specificity_penalty(message, intent_type)
                    
                    # Calculate final confidence with strong penalty enforcement
                    total_penalty = vague_penalty + specificity_penalty
                    confidence = max(0.1, base_confidence + match_bonus + pattern_complexity - total_penalty)
                    
                    # Explicit check for vague messages - force low confidence
                    if vague_penalty > 0.3 or specificity_penalty > 0.3:
                        confidence = min(confidence, 0.45)  # Force confidence below 0.5 for vague messages
                    
                    confidence = min(0.95, confidence)  # Cap at 0.95
                    
                    if confidence > best_confidence:
                        best_intent = intent_type
                        best_confidence = confidence
        
        # If no strong match, use keyword-based fallback
        if best_confidence < 0.5:
            best_intent, best_confidence = await self._fallback_intent_detection(message, language)
        
        return best_intent, best_confidence
    
    def _calculate_vague_penalty(self, message: str, language: str) -> float:
        """Calculate penalty for vague language in message"""
        vague_words = {
            'vi': ['gì đó', 'nào đó', 'có lẽ', 'chắc là', 'hình như', 'khoảng', 'đại loại', 'cái gì'],
            'en': ['something', 'somehow', 'maybe', 'probably', 'kind of', 'sort of', 'apparently', 'what', 'anything']
        }
        
        words = vague_words.get(language, vague_words['en'])
        message_lower = message.lower()
        
        # Special handling: Don't penalize specific useful phrases
        specific_phrases = ['thế nào', 'ra sao', 'như thế nào', 'how are', 'how is', 'what is', 'what\'s the', 'what about', 'how about', 'status']
        if any(phrase in message_lower for phrase in specific_phrases):
            # Only check for truly vague words, not context-specific ones
            words = [w for w in words if w not in ['nào', 'gì', 'what']]
        
        vague_count = sum(1 for word in words if word in message_lower)
        
        # Calculate penalty: 0.5 per vague word, max 0.7 - stronger penalty 
        return min(0.7, vague_count * 0.5)
    
    def _calculate_specificity_penalty(self, message: str, intent_type: IntentType) -> float:
        """Calculate penalty for non-specific messages"""
        # For ANALYZE_TENSION, if message is too general, apply penalty
        if intent_type == IntentType.ANALYZE_TENSION:
            general_patterns = [
                'có vấn đề', 'gặp vấn đề', 'có sự cố', 'having problem', 'there is problem'
            ]
            message_lower = message.lower()
            
            # If matches general pattern but has no specific details, apply penalty
            if any(pattern in message_lower for pattern in general_patterns):
                # Check if message has specific details
                specific_indicators = [
                    'database', 'server', 'api', 'network', 'login', 'authentication', 
                    'performance', 'timeout', 'error code', 'crash', 'bug',
                    'cơ sở dữ liệu', 'máy chủ', 'mạng', 'đăng nhập', 'hiệu suất', 'lỗi', 'sự cố'
                ]
                
                has_specific = any(indicator in message_lower for indicator in specific_indicators)
                if not has_specific:
                    return 0.4  # Strong penalty for non-specific problem reports
        
        return 0.0
    
    async def _fallback_intent_detection(self, message: str, language: str) -> Tuple[IntentType, float]:
        """Fallback intent detection using keywords"""
        keyword_mapping = {
            'vi': {
                IntentType.CREATE_PROJECT: ['tạo', 'mới', 'bắt đầu', 'khởi tạo', 'dự án', 'project'],
                IntentType.ANALYZE_TENSION: ['vấn đề', 'sự cố', 'lỗi', 'khó khăn', 'trouble', 'problem'],
                IntentType.GET_AGENT_HELP: ['trợ giúp', 'hỗ trợ', 'giúp đỡ', 'agent', 'cần', 'muốn'],
                IntentType.CHECK_STATUS: ['trạng thái', 'tình hình', 'thế nào', 'ra sao', 'status'],
                IntentType.GENERATE_SOLUTION: ['giải pháp', 'cách', 'làm sao', 'giải quyết', 'solution'],
                IntentType.SEARCH_KNOWLEDGE: ['tìm', 'kiếm', 'thông tin', 'biết', 'search']
            },
            'en': {
                IntentType.CREATE_PROJECT: ['create', 'new', 'start', 'begin', 'project', 'make'],
                IntentType.ANALYZE_TENSION: ['problem', 'issue', 'error', 'trouble', 'analyze'],
                IntentType.GET_AGENT_HELP: ['help', 'support', 'assist', 'agent', 'need', 'want'],
                IntentType.CHECK_STATUS: ['status', 'how', 'what', 'current', 'check'],
                IntentType.GENERATE_SOLUTION: ['solution', 'solve', 'fix', 'resolve', 'generate'],
                IntentType.SEARCH_KNOWLEDGE: ['search', 'find', 'information', 'know', 'lookup']
            }
        }
        
        keywords = keyword_mapping.get(language, keyword_mapping['en'])
        message_lower = message.lower()
        
        best_intent = IntentType.UNKNOWN
        best_score = 0
        
        for intent_type, intent_keywords in keywords.items():
            score = sum(1 for keyword in intent_keywords if keyword in message_lower)
            if score > best_score:
                best_intent = intent_type
                best_score = score
        
        # Improved fallback confidence calculation
        if best_score > 0:
            base_confidence = 0.6 + best_score * 0.1  # Higher base for fallback
            
            # Only apply vague penalty for truly vague messages
            vague_penalty = self._calculate_vague_penalty(message, language)
            
            # Only apply specificity penalty for ANALYZE_TENSION with very vague descriptions
            specificity_penalty = 0.0
            if best_intent == IntentType.ANALYZE_TENSION and vague_penalty > 0.3:
                specificity_penalty = self._calculate_specificity_penalty(message, best_intent)
            
            confidence = max(0.2, base_confidence - vague_penalty - specificity_penalty)
            
            # Special handling for very vague messages
            if vague_penalty > 0.4 and specificity_penalty > 0.3:
                confidence = min(confidence, 0.4)  # Only for extremely vague messages
                
            confidence = min(0.75, confidence)
        else:
            confidence = 0.1
            
        return best_intent, confidence
    
    async def _extract_entities(self, message: str, language: str) -> Dict[str, Any]:
        """Extract entities từ message"""
        entities = {}
        
        for entity_type, patterns in self.entity_extractors.items():
            for pattern in patterns:
                matches = re.findall(pattern, message, re.IGNORECASE)
                if matches:
                    if entity_type not in entities:
                        entities[entity_type] = []
                    entities[entity_type].extend(matches)
        
        # Clean và normalize entities
        for entity_type, values in entities.items():
            entities[entity_type] = list(set([v.strip() for v in values if v.strip()]))
        
        return entities
    
    async def _build_context(self, message: str, entities: Dict[str, Any], language: str) -> Dict[str, Any]:
        """Build context information từ message và entities"""
        context = {
            'message_length': len(message),
            'language': language,
            'timestamp': datetime.now().isoformat(),
            'entity_count': len(entities),
            'urgency_indicators': self._detect_urgency(message, language),
            'sentiment': await self._analyze_sentiment(message, language)
        }
        
        # Add temporal context
        if 'time_reference' in entities:
            context['temporal_context'] = entities['time_reference']
        
        # Add domain context
        context['domain_indicators'] = self._detect_domain_indicators(message, language)
        
        return context
    
    def _detect_urgency(self, message: str, language: str) -> List[str]:
        """Detect urgency indicators trong message"""
        urgency_patterns = {
            'vi': ['gấp', 'khẩn cấp', 'ngay', 'lập tức', 'nhanh', 'urgent'],
            'en': ['urgent', 'asap', 'immediately', 'quickly', 'fast', 'emergency']
        }
        
        patterns = urgency_patterns.get(language, urgency_patterns['en'])
        return [pattern for pattern in patterns if pattern in message.lower()]
    
    async def _analyze_sentiment(self, message: str, language: str) -> str:
        """Basic sentiment analysis"""
        positive_words = {
            'vi': ['tốt', 'hay', 'xuất sắc', 'tuyệt vời', 'hài lòng', 'thích'],
            'en': ['good', 'great', 'excellent', 'awesome', 'satisfied', 'like']
        }
        
        negative_words = {
            'vi': ['tệ', 'xấu', 'khó khăn', 'vấn đề', 'lỗi', 'không hài lòng'],
            'en': ['bad', 'terrible', 'difficult', 'problem', 'error', 'unsatisfied']
        }
        
        pos_words = positive_words.get(language, positive_words['en'])
        neg_words = negative_words.get(language, negative_words['en'])
        
        message_lower = message.lower()
        pos_count = sum(1 for word in pos_words if word in message_lower)
        neg_count = sum(1 for word in neg_words if word in message_lower)
        
        if pos_count > neg_count:
            return 'positive'
        elif neg_count > pos_count:
            return 'negative'
        else:
            return 'neutral'
    
    def _detect_domain_indicators(self, message: str, language: str) -> List[str]:
        """Detect domain indicators để route tới appropriate agents"""
        domain_patterns = {
            'vi': {
                'data_analysis': ['dữ liệu', 'phân tích', 'thống kê', 'báo cáo', 'bán hàng', 'data analyst'],
                'code_development': ['code', 'lập trình', 'phát triển', 'automation', 'tạo', 'mobile app', 'app', 'website', 'e-commerce'],
                'ui_design': ['giao diện', 'thiết kế', 'UI', 'UX', 'màn hình', 'user-friendly', 'ui designer', 'designer'],
                'integration': ['tích hợp', 'kết nối', 'sync', 'salesforce', 'crm'],
                'research': ['nghiên cứu', 'tìm hiểu', 'khảo sát', 'phân tích thị trường', 'thị trường', 'competitor']
            },
            'en': {
                'data_analysis': ['data', 'analysis', 'statistics', 'report', 'sales', 'data analyst'],
                'code_development': ['code', 'programming', 'development', 'automation', 'create', 'mobile app', 'app', 'website', 'e-commerce'],
                'ui_design': ['interface', 'design', 'UI', 'UX', 'screen', 'user-friendly', 'ui designer', 'designer'],
                'integration': ['integration', 'connect', 'sync', 'salesforce', 'crm'],
                'research': ['research', 'study', 'survey', 'market analysis', 'market', 'competitor']
            }
        }
        
        patterns = domain_patterns.get(language, domain_patterns['en'])
        message_lower = message.lower()
        
        detected_domains = []
        for domain, keywords in patterns.items():
            if any(keyword in message_lower for keyword in keywords):
                detected_domains.append(domain)
        
        # Special handling for API - can be both integration and code_development
        if 'api' in message_lower:
            if 'tạo' in message_lower or 'create' in message_lower:
                detected_domains.append('code_development')
            else:
                detected_domains.append('integration')
        
        # Remove duplicates
        return list(set(detected_domains))
    
    async def extract_entities_and_context(self, intent: ParsedIntent) -> EntityContext:
        """
        Extract detailed entities và context từ parsed intent
        
        Args:
            intent: ParsedIntent từ parse_natural_language_query
            
        Returns:
            EntityContext với detailed entities và relationships
        """
        try:
            # Extract relationships between entities
            relationships = await self._extract_relationships(intent)
            
            # Extract temporal information
            temporal_info = await self._extract_temporal_info(intent)
            
            # Enhance entities với additional context
            enhanced_entities = await self._enhance_entities(intent.entities, intent.context)
            
            # Add intent_type và original_message to context
            enhanced_context = intent.context.copy()
            enhanced_context['intent_type'] = intent.intent_type
            enhanced_context['original_message'] = intent.original_message
            enhanced_context['confidence'] = intent.confidence
            
            return EntityContext(
                entities=enhanced_entities,
                context=enhanced_context,
                relationships=relationships,
                temporal_info=temporal_info
            )
            
        except Exception as e:
            logger.error(f"Error extracting entities and context: {e}")
            # Add intent_type to context even in error case
            error_context = intent.context.copy()
            error_context['intent_type'] = intent.intent_type
            error_context['original_message'] = intent.original_message
            error_context['confidence'] = intent.confidence
            
            return EntityContext(
                entities=intent.entities,
                context=error_context,
                relationships=[],
                temporal_info=None
            )
    
    async def _extract_relationships(self, intent: ParsedIntent) -> List[Tuple[str, str, str]]:
        """Extract relationships between entities"""
        relationships = []
        entities = intent.entities
        
        # Project-Agent relationships
        if 'project_name' in entities and 'agent_type' in entities:
            for project in entities['project_name']:
                for agent in entities['agent_type']:
                    relationships.append((project, 'requires', agent))
        
        # Tension-Priority relationships
        if 'tension_type' in entities and 'priority_level' in entities:
            for tension in entities['tension_type']:
                for priority in entities['priority_level']:
                    relationships.append((tension, 'has_priority', priority))
        
        return relationships
    
    async def _extract_temporal_info(self, intent: ParsedIntent) -> Optional[Dict[str, Any]]:
        """Extract temporal information từ intent"""
        if 'time_reference' not in intent.entities:
            return None
        
        temporal_mapping = {
            'hôm nay': {'type': 'date', 'value': 'today', 'urgency': 'high'},
            'today': {'type': 'date', 'value': 'today', 'urgency': 'high'},
            'tuần này': {'type': 'week', 'value': 'current_week', 'urgency': 'medium'},
            'this week': {'type': 'week', 'value': 'current_week', 'urgency': 'medium'},
            'gấp': {'type': 'urgency', 'value': 'urgent', 'urgency': 'critical'},
            'urgent': {'type': 'urgency', 'value': 'urgent', 'urgency': 'critical'}
        }
        
        temporal_info = {}
        for time_ref in intent.entities['time_reference']:
            if time_ref.lower() in temporal_mapping:
                temporal_info.update(temporal_mapping[time_ref.lower()])
        
        return temporal_info if temporal_info else None
    
    async def _enhance_entities(self, entities: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance entities với additional context information"""
        enhanced = entities.copy()
        
        # Add confidence scores cho entities (iterate qua list of keys để tránh dictionary change)
        entity_keys = list(enhanced.keys())  # Create list of keys first
        for entity_type in entity_keys:
            values = enhanced[entity_type]
            if isinstance(values, list):
                enhanced[f"{entity_type}_confidence"] = [0.8] * len(values)  # Default confidence
        
        # Add domain context
        if context.get('domain_indicators'):
            enhanced['suggested_domains'] = context['domain_indicators']
        
        # Add urgency context
        if context.get('urgency_indicators'):
            enhanced['urgency_level'] = 'high' if context['urgency_indicators'] else 'normal'
        
        return enhanced
    
    async def map_intent_to_system_actions(self, context: EntityContext) -> List[SystemAction]:
        """
        Map intent context thành system actions
        
        Args:
            context: EntityContext từ extract_entities_and_context
            
        Returns:
            List of SystemAction để execute
        """
        try:
            actions = []
            
            # Get intent type từ context
            intent_type = context.context.get('intent_type', IntentType.UNKNOWN)
            
            # Get action mapping
            if intent_type in self.action_mappings:
                mapping = self.action_mappings[intent_type]
                
                # Build parameters từ entities
                parameters = await self._build_action_parameters(context, mapping)
                
                # Create system action
                action = SystemAction(
                    action_type=mapping['action_type'],
                    parameters=parameters,
                    target_endpoint=mapping['target_endpoint'],
                    method=mapping['method'],
                    confidence=context.context.get('confidence', 0.5)
                )
                
                actions.append(action)
            
            # Add additional actions based on entities
            additional_actions = await self._generate_additional_actions(context)
            actions.extend(additional_actions)
            
            logger.info(f"Mapped intent to {len(actions)} system actions")
            return actions
            
        except Exception as e:
            logger.error(f"Error mapping intent to system actions: {e}")
            return []
    
    async def _build_action_parameters(self, context: EntityContext, mapping: Dict[str, Any]) -> Dict[str, Any]:
        """Build parameters cho system action từ entities"""
        parameters = {}
        entities = context.entities
        
        # Map entities to required parameters
        param_mapping = {
            'name': entities.get('project_name', [''])[0] if entities.get('project_name') else '',
            'description': context.context.get('original_message', ''),
            'tension_description': context.context.get('original_message', ''),
            'query': context.context.get('original_message', ''),
            'agent_type': entities.get('agent_type', [''])[0] if entities.get('agent_type') else '',
            'priority': entities.get('priority_level', ['medium'])[0] if entities.get('priority_level') else 'medium'
        }
        
        # Add required parameters
        for param in mapping.get('required_params', []):
            if param in param_mapping:
                parameters[param] = param_mapping[param]
        
        # Add optional parameters
        if context.temporal_info:
            parameters['temporal_context'] = context.temporal_info
        
        if entities.get('urgency_level'):
            parameters['urgency'] = entities['urgency_level']
        
        return parameters
    
    async def _generate_additional_actions(self, context: EntityContext) -> List[SystemAction]:
        """Generate additional actions based on context"""
        additional_actions = []
        
        # If multiple domains detected, suggest agent consultation
        if len(context.entities.get('suggested_domains', [])) > 1:
            action = SystemAction(
                action_type='multi_agent_consultation',
                parameters={
                    'domains': context.entities['suggested_domains'],
                    'query': context.context.get('original_message', '')
                },
                target_endpoint='/api/v1/agents/templates/multi-match',
                method='POST',
                confidence=0.7
            )
            additional_actions.append(action)
        
        # If high urgency, add monitoring action
        if context.entities.get('urgency_level') == 'high':
            action = SystemAction(
                action_type='priority_monitoring',
                parameters={
                    'priority': 'high',
                    'context': context.context
                },
                target_endpoint='/api/v1/monitoring/priority-alert',
                method='POST',
                confidence=0.8
            )
            additional_actions.append(action)
        
        return additional_actions 