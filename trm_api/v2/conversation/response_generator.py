#!/usr/bin/env python3
"""
Natural Language Response Generator for TRM-OS v2
================================================

Generate natural language responses in Vietnamese and English
với context awareness và intelligent formatting.
"""

import asyncio
import json
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from enum import Enum
from datetime import datetime

from trm_api.core.logging_config import get_logger
from .nlp_processor import ParsedIntent, SystemAction, IntentType
from .session_manager import ConversationContext, ConversationTurn

logger = get_logger(__name__)


class ResponseType(Enum):
    """Các loại response"""
    ACKNOWLEDGMENT = "acknowledgment"      # Xác nhận đã hiểu
    INFORMATION = "information"            # Cung cấp thông tin
    ACTION_RESULT = "action_result"        # Kết quả của action
    QUESTION = "question"                  # Đặt câu hỏi
    SUGGESTION = "suggestion"              # Đề xuất
    ERROR = "error"                        # Thông báo lỗi
    CLARIFICATION = "clarification"        # Yêu cầu làm rõ


class ResponseTone(Enum):
    """Tone của response"""
    PROFESSIONAL = "professional"
    FRIENDLY = "friendly"
    HELPFUL = "helpful"
    URGENT = "urgent"
    APOLOGETIC = "apologetic"


@dataclass
class ResponseContext:
    """Context cho response generation với ML insights"""
    intent: ParsedIntent
    conversation_context: ConversationContext
    action_results: List[Dict[str, Any]]
    suggestions: List[Dict[str, Any]]
    error_info: Optional[Dict[str, Any]] = None
    ml_insights: Optional[Dict[str, Any]] = None  # NEW: ML reasoning insights
    

@dataclass
class GeneratedResponse:
    """Generated response với metadata"""
    text: str
    response_type: ResponseType
    tone: ResponseTone
    language: str
    confidence: float
    metadata: Dict[str, Any]
    suggested_actions: List[str]


class NaturalResponseGenerator:
    """
    Core response generator cho conversational intelligence
    
    Generate natural language responses với:
    - Vietnamese/English support
    - Context awareness
    - Tone adaptation
    - Action result formatting
    """
    
    def __init__(self):
        self.response_templates = self._load_response_templates()
        self.tone_modifiers = self._load_tone_modifiers()
        self.action_formatters = self._load_action_formatters()
        
    def _load_response_templates(self) -> Dict[str, Dict[str, List[str]]]:
        """Load response templates cho different intents và languages"""
        return {
            'vi': {
                IntentType.CREATE_PROJECT.value: [
                    "Tôi đã hiểu bạn muốn tạo dự án mới. {details}",
                    "Được rồi, tôi sẽ giúp bạn tạo dự án {project_name}. {next_steps}",
                    "Tôi đã khởi tạo dự án cho bạn. {status}"
                ],
                IntentType.ANALYZE_TENSION.value: [
                    "Tôi đã phân tích vấn đề của bạn. {analysis_result}",
                    "Dựa trên thông tin bạn cung cấp, {assessment}",
                    "Vấn đề này có vẻ {severity}. {recommendations}"
                ],
                IntentType.GET_AGENT_HELP.value: [
                    "Tôi đã tìm thấy {agent_count} agent phù hợp cho bạn. {agent_list}",
                    "Agent {agent_type} sẽ giúp bạn tốt nhất cho vấn đề này. {details}",
                    "Tôi khuyên bạn nên liên hệ với {recommended_agent}. {reason}"
                ],
                IntentType.CHECK_STATUS.value: [
                    "Trạng thái hiện tại: {current_status}. {details}",
                    "Dự án đang {progress_status}. {timeline}",
                    "Tình hình cập nhật: {update_info}"
                ],
                IntentType.GENERATE_SOLUTION.value: [
                    "Tôi đã tạo {solution_count} giải pháp cho bạn. {solutions}",
                    "Giải pháp tốt nhất là: {best_solution}. {explanation}",
                    "Dựa trên phân tích, tôi đề xuất {recommendation}"
                ],
                IntentType.SEARCH_KNOWLEDGE.value: [
                    "Tôi đã tìm thấy {result_count} thông tin liên quan. {results}",
                    "Dựa trên kiến thức có sẵn: {knowledge_summary}",
                    "Thông tin bạn cần: {information}"
                ],
                IntentType.UNKNOWN.value: [
                    "Tôi chưa hiểu rõ ý bạn. Bạn có thể nói rõ hơn được không?",
                    "Có vẻ như tôi cần thêm thông tin. Bạn muốn làm gì cụ thể?",
                    "Xin lỗi, tôi không chắc hiểu đúng. Bạn có thể giải thích thêm?"
                ]
            },
            'en': {
                IntentType.CREATE_PROJECT.value: [
                    "I understand you want to create a new project. {details}",
                    "Alright, I'll help you create project {project_name}. {next_steps}",
                    "I've initiated the project for you. {status}"
                ],
                IntentType.ANALYZE_TENSION.value: [
                    "I've analyzed your problem. {analysis_result}",
                    "Based on the information you provided, {assessment}",
                    "This issue appears to be {severity}. {recommendations}"
                ],
                IntentType.GET_AGENT_HELP.value: [
                    "I found {agent_count} suitable agents for you. {agent_list}",
                    "The {agent_type} agent would help you best with this issue. {details}",
                    "I recommend contacting {recommended_agent}. {reason}"
                ],
                IntentType.CHECK_STATUS.value: [
                    "Current status: {current_status}. {details}",
                    "The project is {progress_status}. {timeline}",
                    "Status update: {update_info}"
                ],
                IntentType.GENERATE_SOLUTION.value: [
                    "I've generated {solution_count} solutions for you. {solutions}",
                    "The best solution is: {best_solution}. {explanation}",
                    "Based on analysis, I recommend {recommendation}"
                ],
                IntentType.SEARCH_KNOWLEDGE.value: [
                    "I found {result_count} relevant information. {results}",
                    "Based on available knowledge: {knowledge_summary}",
                    "Here's the information you need: {information}"
                ],
                IntentType.UNKNOWN.value: [
                    "I don't quite understand. Could you clarify?",
                    "It seems I need more information. What specifically would you like to do?",
                    "Sorry, I'm not sure I understand correctly. Could you explain more?"
                ]
            }
        }
    
    def _load_tone_modifiers(self) -> Dict[str, Dict[ResponseTone, Dict[str, str]]]:
        """Load tone modifiers cho responses"""
        return {
            'vi': {
                ResponseTone.PROFESSIONAL: {
                    'prefix': '',
                    'suffix': '. Tôi sẵn sàng hỗ trợ thêm nếu cần.',
                    'style': 'formal'
                },
                ResponseTone.FRIENDLY: {
                    'prefix': 'Chào bạn! ',
                    'suffix': ' 😊 Còn gì khác tôi có thể giúp không?',
                    'style': 'casual'
                },
                ResponseTone.HELPFUL: {
                    'prefix': '',
                    'suffix': '. Bạn có cần tôi giải thích thêm gì không?',
                    'style': 'supportive'
                },
                ResponseTone.URGENT: {
                    'prefix': 'Tôi hiểu đây là vấn đề gấp. ',
                    'suffix': '. Tôi sẽ ưu tiên xử lý ngay.',
                    'style': 'immediate'
                },
                ResponseTone.APOLOGETIC: {
                    'prefix': 'Xin lỗi vì sự bất tiện. ',
                    'suffix': '. Tôi sẽ cố gắng khắc phục.',
                    'style': 'apologetic'
                }
            },
            'en': {
                ResponseTone.PROFESSIONAL: {
                    'prefix': '',
                    'suffix': '. I\'m ready to assist further if needed.',
                    'style': 'formal'
                },
                ResponseTone.FRIENDLY: {
                    'prefix': 'Hi there! ',
                    'suffix': ' 😊 Is there anything else I can help with?',
                    'style': 'casual'
                },
                ResponseTone.HELPFUL: {
                    'prefix': '',
                    'suffix': '. Would you like me to explain anything further?',
                    'style': 'supportive'
                },
                ResponseTone.URGENT: {
                    'prefix': 'I understand this is urgent. ',
                    'suffix': '. I\'ll prioritize this immediately.',
                    'style': 'immediate'
                },
                ResponseTone.APOLOGETIC: {
                    'prefix': 'I apologize for the inconvenience. ',
                    'suffix': '. I\'ll work to resolve this.',
                    'style': 'apologetic'
                }
            }
        }
    
    def _load_action_formatters(self) -> Dict[str, Dict[str, str]]:
        """Load formatters cho action results"""
        return {
            'vi': {
                'create_entity': 'Đã tạo {entity_type} "{entity_name}" thành công',
                'analyze_data': 'Phân tích hoàn tất với độ tin cậy {confidence}%',
                'find_agent': 'Tìm thấy {count} agent phù hợp: {agents}',
                'query_data': 'Truy vấn thành công, tìm thấy {count} kết quả',
                'generate_solution': 'Đã tạo {count} giải pháp với độ khả thi cao',
                'search_data': 'Tìm kiếm hoàn tất, {count} kết quả phù hợp',
                'error': 'Có lỗi xảy ra: {error_message}'
            },
            'en': {
                'create_entity': 'Successfully created {entity_type} "{entity_name}"',
                'analyze_data': 'Analysis completed with {confidence}% confidence',
                'find_agent': 'Found {count} suitable agents: {agents}',
                'query_data': 'Query successful, found {count} results',
                'generate_solution': 'Generated {count} high-feasibility solutions',
                'search_data': 'Search completed, {count} relevant results',
                'error': 'An error occurred: {error_message}'
            }
        }
    
    async def generate_natural_language_response(self, context: ResponseContext) -> GeneratedResponse:
        """
        Generate natural language response từ context
        
        Args:
            context: ResponseContext với intent, actions, results
            
        Returns:
            GeneratedResponse với formatted text và metadata
        """
        try:
            language = context.intent.language
            intent_type = context.intent.intent_type
            
            # Determine response type và tone
            response_type = await self._determine_response_type(context)
            tone = await self._determine_tone(context)
            
            # Generate base response
            base_response = await self._generate_base_response(context, response_type)
            
            # Format action results
            action_text = await self._format_action_results(context.action_results, language)
            
            # Add suggestions
            suggestions_text = await self._format_suggestions(context.suggestions, language)
            
            # Combine response parts
            full_text = await self._combine_response_parts(
                base_response, action_text, suggestions_text, tone, language
            )
            
            # Generate suggested actions
            suggested_actions = await self._generate_suggested_actions(context)
            
            # Calculate confidence
            confidence = await self._calculate_response_confidence(context)
            
            response = GeneratedResponse(
                text=full_text,
                response_type=response_type,
                tone=tone,
                language=language,
                confidence=confidence,
                metadata={
                    'intent_type': intent_type.value,
                    'action_count': len(context.action_results),
                    'suggestion_count': len(context.suggestions),
                    'has_error': context.error_info is not None
                },
                suggested_actions=suggested_actions
            )
            
            logger.info(f"Generated response: {response_type.value} in {language}")
            return response
            
        except Exception as e:
            logger.error(f"Error generating natural language response: {e}")
            return await self._generate_error_response(str(e), context.intent.language)
    
    async def _determine_response_type(self, context: ResponseContext) -> ResponseType:
        """Determine appropriate response type"""
        if context.error_info:
            return ResponseType.ERROR
        
        if context.intent.confidence < 0.5:
            return ResponseType.CLARIFICATION
        
        if context.action_results:
            return ResponseType.ACTION_RESULT
        
        if context.suggestions:
            return ResponseType.SUGGESTION
        
        # Based on intent type
        intent_to_response = {
            IntentType.CREATE_PROJECT: ResponseType.ACTION_RESULT,
            IntentType.ANALYZE_TENSION: ResponseType.INFORMATION,
            IntentType.GET_AGENT_HELP: ResponseType.SUGGESTION,
            IntentType.CHECK_STATUS: ResponseType.INFORMATION,
            IntentType.GENERATE_SOLUTION: ResponseType.SUGGESTION,
            IntentType.SEARCH_KNOWLEDGE: ResponseType.INFORMATION,
            IntentType.UNKNOWN: ResponseType.CLARIFICATION
        }
        
        return intent_to_response.get(context.intent.intent_type, ResponseType.ACKNOWLEDGMENT)
    
    async def _determine_tone(self, context: ResponseContext) -> ResponseTone:
        """Determine appropriate tone"""
        # Check for urgency indicators
        if context.intent.context.get('urgency_indicators'):
            return ResponseTone.URGENT
        
        # Check for errors
        if context.error_info:
            return ResponseTone.APOLOGETIC
        
        # Check confidence level
        if context.intent.confidence < 0.5:
            return ResponseTone.HELPFUL
        
        # Default based on intent
        if context.intent.intent_type in [IntentType.GET_AGENT_HELP, IntentType.UNKNOWN]:
            return ResponseTone.HELPFUL
        
        return ResponseTone.PROFESSIONAL
    
    async def _generate_base_response(self, context: ResponseContext, response_type: ResponseType) -> str:
        """Generate base response text"""
        language = context.intent.language
        intent_type = context.intent.intent_type
        
        # Get templates
        templates = self.response_templates.get(language, self.response_templates['en'])
        intent_templates = templates.get(intent_type.value, templates[IntentType.UNKNOWN.value])
        
        # Select template based on context
        template = await self._select_template(intent_templates, context)
        
        # Fill template placeholders
        filled_template = await self._fill_template_placeholders(template, context)
        
        return filled_template
    
    async def _select_template(self, templates: List[str], context: ResponseContext) -> str:
        """Select most appropriate template"""
        # Simple selection based on action results
        if context.action_results:
            return templates[min(2, len(templates) - 1)]  # Use result-oriented template
        elif context.suggestions:
            return templates[min(1, len(templates) - 1)]  # Use suggestion-oriented template
        else:
            return templates[0]  # Use basic template
    
    async def _fill_template_placeholders(self, template: str, context: ResponseContext) -> str:
        """Fill template placeholders với actual data"""
        placeholders = {}
        
        # Extract entities
        entities = context.intent.entities
        
        # Common placeholders
        if 'project_name' in entities and entities['project_name']:
            placeholders['project_name'] = entities['project_name'][0]
        
        if 'agent_type' in entities and entities['agent_type']:
            placeholders['agent_type'] = entities['agent_type'][0]
        
        # Action-specific placeholders
        if context.action_results:
            result = context.action_results[0]
            placeholders.update({
                'result_count': str(len(context.action_results)),
                'confidence': str(int(result.get('confidence', 0) * 100)) if 'confidence' in result else '85',
                'status': result.get('status', 'completed')
            })
        
        # Fill template
        filled = template
        for key, value in placeholders.items():
            filled = filled.replace(f'{{{key}}}', str(value))
        
        # Remove unfilled placeholders
        import re
        filled = re.sub(r'\{[^}]+\}', '', filled)
        
        return filled.strip()
    
    async def _format_action_results(self, action_results: List[Dict[str, Any]], language: str) -> str:
        """Format action results into readable text"""
        if not action_results:
            return ""
        
        formatters = self.action_formatters.get(language, self.action_formatters['en'])
        formatted_results = []
        
        for result in action_results:
            action_type = result.get('action_type', 'unknown')
            formatter = formatters.get(action_type, formatters.get('error', '{error_message}'))
            
            # Fill formatter placeholders
            formatted = formatter
            for key, value in result.items():
                if isinstance(value, (str, int, float)):
                    formatted = formatted.replace(f'{{{key}}}', str(value))
            
            formatted_results.append(formatted)
        
        return ' '.join(formatted_results)
    
    async def _format_suggestions(self, suggestions: List[Dict[str, Any]], language: str) -> str:
        """Format suggestions into readable text"""
        if not suggestions:
            return ""
        
        if language == 'vi':
            prefix = "Tôi cũng có thể giúp bạn:"
            bullet = "• "
        else:
            prefix = "I can also help you with:"
            bullet = "• "
        
        suggestion_texts = []
        for suggestion in suggestions[:3]:  # Limit to 3 suggestions
            text = suggestion.get('text', '')
            if text:
                suggestion_texts.append(f"{bullet}{text}")
        
        if suggestion_texts:
            return f"\n\n{prefix}\n" + "\n".join(suggestion_texts)
        
        return ""
    
    async def _combine_response_parts(self, base_response: str, action_text: str, 
                                    suggestions_text: str, tone: ResponseTone, language: str) -> str:
        """Combine all response parts với appropriate tone"""
        # Get tone modifiers
        tone_modifiers = self.tone_modifiers.get(language, self.tone_modifiers['en'])
        modifier = tone_modifiers.get(tone, tone_modifiers[ResponseTone.PROFESSIONAL])
        
        # Combine parts
        parts = [base_response]
        
        if action_text:
            parts.append(action_text)
        
        combined = ' '.join(parts)
        
        # Apply tone
        final_response = modifier['prefix'] + combined + modifier['suffix']
        
        # Add suggestions
        if suggestions_text:
            final_response += suggestions_text
        
        return final_response.strip()
    
    async def _generate_suggested_actions(self, context: ResponseContext) -> List[str]:
        """Generate suggested follow-up actions"""
        suggestions = []
        intent_type = context.intent.intent_type
        language = context.intent.language
        
        # Intent-specific suggestions
        if intent_type == IntentType.CREATE_PROJECT:
            if language == 'vi':
                suggestions.extend([
                    "Thêm thành viên vào dự án",
                    "Tạo timeline chi tiết",
                    "Assign tasks cho team members"
                ])
            else:
                suggestions.extend([
                    "Add team members to project",
                    "Create detailed timeline",
                    "Assign tasks to team members"
                ])
        
        elif intent_type == IntentType.ANALYZE_TENSION:
            if language == 'vi':
                suggestions.extend([
                    "Tạo giải pháp cho vấn đề",
                    "Assign agent để xử lý",
                    "Thiết lập monitoring"
                ])
            else:
                suggestions.extend([
                    "Generate solutions",
                    "Assign agent to handle",
                    "Set up monitoring"
                ])
        
        elif intent_type == IntentType.GET_AGENT_HELP:
            if language == 'vi':
                suggestions.extend([
                    "Kết nối với agent được đề xuất",
                    "Xem profile của agents",
                    "Tạo task cho agent"
                ])
            else:
                suggestions.extend([
                    "Connect with recommended agent",
                    "View agent profiles",
                    "Create task for agent"
                ])
        
        return suggestions[:3]  # Return top 3
    
    async def _calculate_response_confidence(self, context: ResponseContext) -> float:
        """Calculate confidence score cho generated response"""
        base_confidence = context.intent.confidence
        
        # Boost confidence if we have action results
        if context.action_results:
            base_confidence += 0.1
        
        # Reduce confidence for errors
        if context.error_info:
            base_confidence -= 0.3
        
        # Boost confidence for clear intents
        if context.intent.intent_type != IntentType.UNKNOWN:
            base_confidence += 0.05
        
        return max(0.0, min(1.0, base_confidence))
    
    async def _generate_error_response(self, error_message: str, language: str) -> GeneratedResponse:
        """Generate error response"""
        if language == 'vi':
            text = f"Xin lỗi, có lỗi xảy ra: {error_message}. Tôi sẽ cố gắng khắc phục."
        else:
            text = f"Sorry, an error occurred: {error_message}. I'll try to resolve this."
        
        return GeneratedResponse(
            text=text,
            response_type=ResponseType.ERROR,
            tone=ResponseTone.APOLOGETIC,
            language=language,
            confidence=0.9,
            metadata={'error': error_message},
            suggested_actions=[]
        )
    
    async def format_agent_response(self, agent_result: Dict[str, Any], language: str) -> str:
        """Format agent-specific response"""
        agent_name = agent_result.get('agent_name', 'Unknown Agent')
        confidence = agent_result.get('confidence', 0)
        capabilities = agent_result.get('capabilities', [])
        
        if language == 'vi':
            response = f"Agent {agent_name} phù hợp {confidence:.0%} với yêu cầu của bạn."
            if capabilities:
                cap_text = ', '.join(capabilities[:3])
                response += f" Chuyên môn: {cap_text}."
        else:
            response = f"Agent {agent_name} is {confidence:.0%} suitable for your request."
            if capabilities:
                cap_text = ', '.join(capabilities[:3])
                response += f" Expertise: {cap_text}."
        
        return response
    
    async def format_solution_response(self, solutions: List[Dict[str, Any]], language: str) -> str:
        """Format solution generation response"""
        if not solutions:
            return "Không tìm thấy giải pháp phù hợp." if language == 'vi' else "No suitable solutions found."
        
        best_solution = max(solutions, key=lambda s: s.get('confidence', 0))
        
        if language == 'vi':
            response = f"Giải pháp tốt nhất: {best_solution.get('title', 'Unnamed Solution')}"
            if 'description' in best_solution:
                response += f"\n{best_solution['description']}"
            response += f"\nĐộ tin cậy: {best_solution.get('confidence', 0):.0%}"
        else:
            response = f"Best solution: {best_solution.get('title', 'Unnamed Solution')}"
            if 'description' in best_solution:
                response += f"\n{best_solution['description']}"
            response += f"\nConfidence: {best_solution.get('confidence', 0):.0%}"
        
        return response
    
    async def format_status_response(self, status_data: Dict[str, Any], language: str) -> str:
        """Format status check response"""
        entity_type = status_data.get('entity_type', 'entity')
        status = status_data.get('status', 'unknown')
        progress = status_data.get('progress', 0)
        
        if language == 'vi':
            response = f"Trạng thái {entity_type}: {status}"
            if progress > 0:
                response += f" (Tiến độ: {progress}%)"
            
            if 'next_milestone' in status_data:
                response += f"\nMục tiêu tiếp theo: {status_data['next_milestone']}"
        else:
            response = f"{entity_type.title()} status: {status}"
            if progress > 0:
                response += f" (Progress: {progress}%)"
            
            if 'next_milestone' in status_data:
                response += f"\nNext milestone: {status_data['next_milestone']}"
        
        return response 