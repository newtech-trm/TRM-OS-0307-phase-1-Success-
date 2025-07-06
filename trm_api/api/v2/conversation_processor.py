"""
TRM-OS Conversational Interface - Natural Language Processing Engine
Tích hợp với Adaptive Learning System để continuous improvement
"""

import asyncio
import re
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum
import json
from datetime import datetime

from ...learning.adaptive_learning_system import AdaptiveLearningSystem
from ...learning.learning_types import LearningExperience, ExperienceType
from ...models.enums import AgentType, TensionType, TaskStatus
from .mock_services import MockAgentService, MockProjectService, MockTensionService


class IntentType(Enum):
    """Các loại intent mà hệ thống có thể nhận diện"""
    CREATE_AGENT = "create_agent"
    CREATE_PROJECT = "create_project"
    RESOLVE_TENSION = "resolve_tension"
    GET_STATUS = "get_status"
    ANALYZE_PERFORMANCE = "analyze_performance"
    SEARCH_KNOWLEDGE = "search_knowledge"
    UNKNOWN = "unknown"


@dataclass
class ParsedIntent:
    """Kết quả parsing natural language query"""
    intent: IntentType
    entities: Dict[str, Any]
    confidence: float
    raw_message: str
    context: Optional[Dict[str, Any]] = None


@dataclass
class EntityContext:
    """Context được extract từ parsed intent"""
    primary_entity: str
    entity_type: str
    attributes: Dict[str, Any]
    relationships: List[Dict[str, Any]]
    confidence: float


@dataclass
class Action:
    """System action được map từ intent"""
    action_type: str
    target_service: str
    parameters: Dict[str, Any]
    priority: int


@dataclass
class ActionResult:
    """Kết quả thực hiện action"""
    success: bool
    data: Any
    message: str
    execution_time: float


class ConversationProcessor:
    """
    Core NLP Engine cho TRM-OS Conversational Interface
    Tích hợp với Adaptive Learning để continuous improvement
    """
    
    def __init__(self, learning_system: AdaptiveLearningSystem):
        self.learning_system = learning_system
        
        # Use mock services for conversational interface
        self.agent_service = MockAgentService()
        self.project_service = MockProjectService()
        self.tension_service = MockTensionService()
        
        # Intent patterns - sẽ được adaptive learning cải thiện
        self.intent_patterns = {
            IntentType.CREATE_AGENT: [
                r"tạo.*agent.*(?P<agent_type>code|research|data|ui|integration)",
                r"cần.*agent.*(?P<agent_type>code|research|data|ui|integration)",
                r"khởi tạo.*agent.*(?P<agent_type>code|research|data|ui|integration)",
            ],
            IntentType.CREATE_PROJECT: [
                r"tạo.*project.*(?P<project_name>[\w\s]+)",
                r"bắt đầu.*dự án.*(?P<project_name>[\w\s]+)",
                r"khởi tạo.*project.*(?P<project_name>[\w\s]+)",
            ],
            IntentType.RESOLVE_TENSION: [
                r"giải quyết.*tension.*(?P<tension_type>technical|business|resource)",
                r"xử lý.*vấn đề.*(?P<tension_type>technical|business|resource)",
                r"resolve.*tension.*(?P<tension_type>technical|business|resource)",
            ],
            IntentType.GET_STATUS: [
                r"trạng thái.*(?P<entity_type>project|agent|system)",
                r"status.*(?P<entity_type>project|agent|system)",
                r"tình hình.*(?P<entity_type>project|agent|system)",
            ],
            IntentType.ANALYZE_PERFORMANCE: [
                r"phân tích.*performance.*(?P<entity_type>agent|project|system)",
                r"đánh giá.*hiệu suất.*(?P<entity_type>agent|project|system)",
                r"analyze.*performance.*(?P<entity_type>agent|project|system)",
            ],
            IntentType.SEARCH_KNOWLEDGE: [
                r"tìm kiếm.*(?P<query>[\w\s]+)",
                r"search.*(?P<query>[\w\s]+)",
                r"kiến thức.*(?P<query>[\w\s]+)",
            ]
        }
        
        # Entity extractors
        self.entity_extractors = {
            "agent_type": self._extract_agent_type,
            "project_name": self._extract_project_name,
            "tension_type": self._extract_tension_type,
            "entity_type": self._extract_entity_type,
            "query": self._extract_query,
        }
    
    async def parse_natural_language_query(self, message: str) -> ParsedIntent:
        """
        Parse natural language query thành structured intent
        Sử dụng adaptive learning để cải thiện accuracy
        """
        start_time = datetime.now()
        
        # Normalize message
        normalized_message = self._normalize_message(message)
        
        # Try to match intent patterns
        matched_intent = None
        matched_entities = {}
        confidence = 0.0
        
        for intent_type, patterns in self.intent_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, normalized_message, re.IGNORECASE)
                if match:
                    matched_intent = intent_type
                    matched_entities = match.groupdict()
                    confidence = self._calculate_pattern_confidence(pattern, match)
                    break
            if matched_intent:
                break
        
        # Fallback to unknown intent
        if not matched_intent:
            matched_intent = IntentType.UNKNOWN
            confidence = 0.1
        
        # Create parsed intent
        parsed_intent = ParsedIntent(
            intent=matched_intent,
            entities=matched_entities,
            confidence=confidence,
            raw_message=message,
            context={"normalized_message": normalized_message}
        )
        
        # Learn from parsing experience
        processing_time = (datetime.now() - start_time).total_seconds()
        await self._learn_from_parsing_experience(
            message, parsed_intent, processing_time
        )
        
        return parsed_intent
    
    async def extract_entities_and_context(self, intent: ParsedIntent) -> EntityContext:
        """
        Extract entities và context từ parsed intent
        Sử dụng adaptive learning để cải thiện entity recognition
        """
        start_time = datetime.now()
        
        # Determine primary entity
        primary_entity = None
        entity_type = None
        
        if intent.intent == IntentType.CREATE_AGENT:
            primary_entity = "agent"
            entity_type = "agent"
        elif intent.intent == IntentType.CREATE_PROJECT:
            primary_entity = "project"
            entity_type = "project"
        elif intent.intent == IntentType.RESOLVE_TENSION:
            primary_entity = "tension"
            entity_type = "tension"
        else:
            primary_entity = "system"
            entity_type = "system"
        
        # Extract attributes
        attributes = {}
        for entity_name, entity_value in intent.entities.items():
            if entity_name in self.entity_extractors:
                extracted_value = await self.entity_extractors[entity_name](entity_value)
                attributes[entity_name] = extracted_value
        
        # Extract relationships (placeholder - sẽ được mở rộng)
        relationships = []
        
        # Calculate confidence
        confidence = intent.confidence * 0.9  # Slight reduction for entity extraction
        
        # Create entity context
        entity_context = EntityContext(
            primary_entity=primary_entity,
            entity_type=entity_type,
            attributes=attributes,
            relationships=relationships,
            confidence=confidence
        )
        
        # Learn from entity extraction experience
        processing_time = (datetime.now() - start_time).total_seconds()
        await self._learn_from_entity_extraction_experience(
            intent, entity_context, processing_time
        )
        
        return entity_context
    
    async def map_intent_to_system_actions(self, context: EntityContext) -> List[Action]:
        """
        Map intent context thành system actions
        Sử dụng adaptive learning để optimize action selection
        """
        start_time = datetime.now()
        actions = []
        
        if context.entity_type == "agent":
            # Create agent action
            agent_type = context.attributes.get("agent_type", "code")
            actions.append(Action(
                action_type="create_agent",
                target_service="agent_service",
                parameters={
                    "agent_type": agent_type,
                    "auto_configure": True
                },
                priority=1
            ))
        
        elif context.entity_type == "project":
            # Create project action
            project_name = context.attributes.get("project_name", "New Project")
            actions.append(Action(
                action_type="create_project",
                target_service="project_service",
                parameters={
                    "name": project_name,
                    "auto_setup": True
                },
                priority=1
            ))
        
        elif context.entity_type == "tension":
            # Resolve tension action
            tension_type = context.attributes.get("tension_type", "technical")
            actions.append(Action(
                action_type="resolve_tension",
                target_service="tension_service",
                parameters={
                    "tension_type": tension_type,
                    "auto_analyze": True
                },
                priority=1
            ))
        
        else:
            # Default system status action
            actions.append(Action(
                action_type="get_system_status",
                target_service="system_service",
                parameters={},
                priority=1
            ))
        
        # Learn from action mapping experience
        processing_time = (datetime.now() - start_time).total_seconds()
        await self._learn_from_action_mapping_experience(
            context, actions, processing_time
        )
        
        return actions
    
    async def generate_natural_response(self, result: ActionResult) -> str:
        """
        Generate natural language response từ action result
        Sử dụng adaptive learning để cải thiện response quality
        """
        start_time = datetime.now()
        
        if result.success:
            if "agent" in str(result.data):
                response = f"✅ Đã tạo thành công agent với ID: {result.data.get('id', 'unknown')}"
            elif "project" in str(result.data):
                response = f"✅ Đã tạo thành công project '{result.data.get('name', 'unknown')}'"
            elif "tension" in str(result.data):
                response = f"✅ Đã xử lý tension với confidence: {result.data.get('confidence', 0):.2f}"
            else:
                response = f"✅ Thực hiện thành công: {result.message}"
        else:
            response = f"❌ Thực hiện thất bại: {result.message}"
        
        # Add execution time info
        response += f"\n⏱️ Thời gian thực hiện: {result.execution_time:.2f}s"
        
        # Learn from response generation experience
        processing_time = (datetime.now() - start_time).total_seconds()
        await self._learn_from_response_generation_experience(
            result, response, processing_time
        )
        
        return response
    
    async def learn_from_conversation_patterns(self, conversations: List[Dict]) -> Dict:
        """
        Learn từ conversation patterns để cải thiện NLP models
        """
        learning_updates = []
        
        for conversation in conversations:
            # Extract patterns từ successful conversations
            if conversation.get("success", False):
                pattern_data = {
                    "input_pattern": conversation.get("input", ""),
                    "intent_accuracy": conversation.get("intent_accuracy", 0.0),
                    "entity_accuracy": conversation.get("entity_accuracy", 0.0),
                    "response_quality": conversation.get("response_quality", 0.0)
                }
                
                # Create learning experience
                experience = LearningExperience(
                    experience_type=ExperienceType.CONVERSATION_PATTERN,
                    context=pattern_data,
                    action="pattern_recognition",
                    outcome="improved_accuracy",
                    performance_metrics={
                        "intent_accuracy": pattern_data["intent_accuracy"],
                        "entity_accuracy": pattern_data["entity_accuracy"],
                        "response_quality": pattern_data["response_quality"]
                    },
                    confidence=0.8,
                    importance=0.7
                )
                
                await self.learning_system.learn_from_experience(experience)
                learning_updates.append(pattern_data)
        
        return {
            "patterns_learned": len(learning_updates),
            "learning_updates": learning_updates
        }
    
    async def adapt_nlp_models(self, feedback: Dict) -> Dict:
        """
        Adapt NLP models dựa trên user feedback
        """
        adaptation_results = []
        
        # Process feedback data
        for feedback_item in feedback.get("feedback_items", []):
            if feedback_item.get("type") == "intent_correction":
                # Update intent patterns based on correction
                correct_intent = feedback_item.get("correct_intent")
                original_message = feedback_item.get("message")
                
                # Create adaptation experience
                experience = LearningExperience(
                    experience_type=ExperienceType.FEEDBACK_ADAPTATION,
                    context={
                        "original_message": original_message,
                        "correct_intent": correct_intent,
                        "feedback_type": "intent_correction"
                    },
                    action="model_adaptation",
                    outcome="improved_intent_recognition",
                    performance_metrics={"accuracy_improvement": 0.1},
                    confidence=0.9,
                    importance=0.8
                )
                
                await self.learning_system.learn_from_experience(experience)
                adaptation_results.append({
                    "type": "intent_pattern_update",
                    "message": original_message,
                    "correct_intent": correct_intent
                })
        
        return {
            "adaptations_applied": len(adaptation_results),
            "adaptation_results": adaptation_results
        }
    
    # Helper methods
    def _normalize_message(self, message: str) -> str:
        """Normalize message cho better pattern matching"""
        # Convert to lowercase
        normalized = message.lower()
        
        # Remove extra whitespace
        normalized = re.sub(r'\s+', ' ', normalized).strip()
        
        # Replace common variations
        replacements = {
            "tạo ra": "tạo",
            "khởi tạo": "tạo",
            "bắt đầu": "tạo",
            "giải quyết": "resolve",
            "xử lý": "resolve",
        }
        
        for old, new in replacements.items():
            normalized = normalized.replace(old, new)
        
        return normalized
    
    def _calculate_pattern_confidence(self, pattern: str, match: re.Match) -> float:
        """Calculate confidence score cho pattern match"""
        # Base confidence
        confidence = 0.7
        
        # Boost confidence if có named groups
        if match.groupdict():
            confidence += 0.2
        
        # Boost confidence based on pattern complexity
        if len(pattern) > 50:
            confidence += 0.1
        
        return min(confidence, 1.0)
    
    async def _extract_agent_type(self, value: str) -> str:
        """Extract agent type từ entity value"""
        type_mapping = {
            "code": "CODE_GENERATOR",
            "research": "RESEARCH",
            "data": "DATA_ANALYST",
            "ui": "USER_INTERFACE",
            "integration": "INTEGRATION"
        }
        return type_mapping.get(value.lower(), "CODE_GENERATOR")
    
    async def _extract_project_name(self, value: str) -> str:
        """Extract project name từ entity value"""
        # Clean và validate project name
        cleaned_name = re.sub(r'[^\w\s-]', '', value).strip()
        return cleaned_name if cleaned_name else "New Project"
    
    async def _extract_tension_type(self, value: str) -> str:
        """Extract tension type từ entity value"""
        type_mapping = {
            "technical": "TECHNICAL",
            "business": "BUSINESS",
            "resource": "RESOURCE"
        }
        return type_mapping.get(value.lower(), "TECHNICAL")
    
    async def _extract_entity_type(self, value: str) -> str:
        """Extract entity type từ entity value"""
        return value.lower()
    
    async def _extract_query(self, value: str) -> str:
        """Extract search query từ entity value"""
        return value.strip()
    
    # Learning helper methods
    async def _learn_from_parsing_experience(self, message: str, intent: ParsedIntent, processing_time: float):
        """Learn from parsing experience"""
        try:
            experience = LearningExperience(
                experience_type=ExperienceType.NLP_PARSING,
                agent_id="conversation_processor",  # Add required agent_id
                context={
                    "message": message,
                    "intent": intent.intent.value,
                    "confidence": intent.confidence,
                    "processing_time": processing_time
                },
                action_taken={
                    "action": "parse_natural_language",
                    "patterns_matched": len([p for p in self.intent_patterns.get(intent.intent, [])]),
                    "entities_extracted": len(intent.entities)
                },
                outcome={  # Change to Dict format
                    "intent_recognized": intent.intent.value,
                    "confidence_achieved": intent.confidence,
                    "entities_found": intent.entities,
                    "success": intent.intent != IntentType.UNKNOWN
                },
                success=intent.intent != IntentType.UNKNOWN,
                duration_seconds=processing_time,
                confidence_level=intent.confidence,
                importance_weight=0.6
            )
            
            await self.learning_system.learn_from_experience(experience)
        except Exception as e:
            # Don't fail conversation if learning fails
            print(f"Learning error: {e}")
            pass
    
    async def _learn_from_entity_extraction_experience(self, intent: ParsedIntent, context: EntityContext, processing_time: float):
        """Learn from entity extraction experience"""
        try:
            experience = LearningExperience(
                experience_type=ExperienceType.ENTITY_EXTRACTION,
                agent_id="conversation_processor",
                context={
                    "intent": intent.intent.value,
                    "raw_entities": intent.entities,
                    "processing_time": processing_time
                },
                action_taken={
                    "action": "extract_entities",
                    "primary_entity": context.primary_entity,
                    "entity_type": context.entity_type
                },
                outcome={
                    "entities_extracted": context.attributes,
                    "confidence_achieved": context.confidence,
                    "success": context.confidence > 0.5
                },
                success=context.confidence > 0.5,
                duration_seconds=processing_time,
                confidence_level=context.confidence,
                importance_weight=0.7
            )
            
            await self.learning_system.learn_from_experience(experience)
        except Exception as e:
            print(f"Entity extraction learning error: {e}")
            pass
    
    async def _learn_from_action_mapping_experience(self, context: EntityContext, actions: List[Action], processing_time: float):
        """Learn from action mapping experience"""
        try:
            experience = LearningExperience(
                experience_type=ExperienceType.ACTION_MAPPING,
                agent_id="conversation_processor",
                context={
                    "entity_context": context.primary_entity,
                    "entity_type": context.entity_type,
                    "processing_time": processing_time
                },
                action_taken={
                    "action": "map_intent_to_actions",
                    "actions_generated": len(actions),
                    "action_types": [a.action_type for a in actions]
                },
                outcome={
                    "actions_mapped": [{"type": a.action_type, "service": a.target_service} for a in actions],
                    "success": len(actions) > 0
                },
                success=len(actions) > 0,
                duration_seconds=processing_time,
                confidence_level=context.confidence,
                importance_weight=0.8
            )
            
            await self.learning_system.learn_from_experience(experience)
        except Exception as e:
            print(f"Action mapping learning error: {e}")
            pass
    
    async def _learn_from_response_generation_experience(self, result: ActionResult, response: str, processing_time: float):
        """Learn from response generation experience"""
        try:
            experience = LearningExperience(
                experience_type=ExperienceType.RESPONSE_GENERATION,
                agent_id="conversation_processor",
                context={
                    "action_success": result.success,
                    "execution_time": result.execution_time,
                    "processing_time": processing_time
                },
                action_taken={
                    "action": "generate_response",
                    "response_length": len(response),
                    "response_type": "success" if result.success else "error"
                },
                outcome={
                    "response_generated": response,
                    "user_friendly": "✅" in response or "❌" in response,
                    "success": result.success
                },
                success=result.success,
                duration_seconds=processing_time,
                confidence_level=0.8 if result.success else 0.4,
                importance_weight=0.5
            )
            
            await self.learning_system.learn_from_experience(experience)
        except Exception as e:
            print(f"Response generation learning error: {e}")
            pass 