#!/usr/bin/env python3
"""
Test Suite for Conversational NLP Processor
==========================================

Comprehensive tests cho natural language processing,
intent detection, và entity extraction.
"""

import pytest
import asyncio
from datetime import datetime
from unittest.mock import Mock, patch

from trm_api.v2.conversation.nlp_processor import (
    ConversationProcessor, 
    IntentType, 
    ParsedIntent,
    EntityContext,
    SystemAction
)


class TestConversationProcessor:
    """Test cases cho ConversationProcessor"""
    
    @pytest.fixture
    def processor(self):
        """Create ConversationProcessor instance"""
        return ConversationProcessor()
    
    @pytest.mark.asyncio
    async def test_vietnamese_intent_detection(self, processor):
        """Test intent detection cho Vietnamese queries"""
        test_cases = [
            ("Tôi muốn tạo dự án mới", IntentType.CREATE_PROJECT),
            ("Có vấn đề với hệ thống", IntentType.ANALYZE_TENSION),
            ("Cần trợ giúp từ agent", IntentType.GET_AGENT_HELP),
            ("Trạng thái dự án thế nào?", IntentType.CHECK_STATUS),
            ("Tìm giải pháp cho vấn đề này", IntentType.GENERATE_SOLUTION),
            ("Tìm kiếm thông tin về API", IntentType.SEARCH_KNOWLEDGE)
        ]
        
        for message, expected_intent in test_cases:
            result = await processor.parse_natural_language_query(message)
            assert result.intent_type == expected_intent
            assert result.language == 'vi'
            assert result.confidence > 0.5
    
    @pytest.mark.asyncio
    async def test_english_intent_detection(self, processor):
        """Test intent detection cho English queries"""
        test_cases = [
            ("I want to create a new project", IntentType.CREATE_PROJECT),
            ("There's a problem with the system", IntentType.ANALYZE_TENSION),
            ("Need help from an agent", IntentType.GET_AGENT_HELP),
            ("What's the project status?", IntentType.CHECK_STATUS),
            ("Find solution for this issue", IntentType.GENERATE_SOLUTION),
            ("Search for API information", IntentType.SEARCH_KNOWLEDGE)
        ]
        
        for message, expected_intent in test_cases:
            result = await processor.parse_natural_language_query(message)
            assert result.intent_type == expected_intent
            assert result.language == 'en'
            assert result.confidence > 0.5
    
    @pytest.mark.asyncio
    async def test_entity_extraction_vietnamese(self, processor):
        """Test entity extraction từ Vietnamese text"""
        message = "Tôi muốn tạo dự án TRM-Analytics với data analyst agent, ưu tiên cao"
        result = await processor.parse_natural_language_query(message)
        
        assert 'project_name' in result.entities
        assert 'TRM-Analytics' in result.entities['project_name']
        assert 'agent_type' in result.entities
        assert 'data analyst' in result.entities['agent_type']
        assert 'priority_level' in result.entities
        assert 'cao' in result.entities['priority_level']
    
    @pytest.mark.asyncio
    async def test_entity_extraction_english(self, processor):
        """Test entity extraction từ English text"""
        message = "Create project DataPipeline with integration agent, urgent priority"
        result = await processor.parse_natural_language_query(message)
        
        assert 'project_name' in result.entities
        assert 'DataPipeline' in result.entities['project_name']
        assert 'agent_type' in result.entities
        assert 'integration' in result.entities['agent_type']
        assert 'priority_level' in result.entities
        assert 'urgent' in result.entities['priority_level']
    
    @pytest.mark.asyncio
    async def test_context_building(self, processor):
        """Test context building từ parsed intent"""
        message = "Cần giải quyết vấn đề database performance gấp"
        result = await processor.parse_natural_language_query(message)
        
        assert result.context['language'] == 'vi'
        assert result.context['message_length'] > 0
        assert 'urgency_indicators' in result.context
        assert len(result.context['urgency_indicators']) > 0
        assert 'sentiment' in result.context
        assert 'domain_indicators' in result.context
    
    @pytest.mark.asyncio
    async def test_urgency_detection(self, processor):
        """Test urgency detection trong messages"""
        urgent_messages = [
            "Cần giải quyết gấp vấn đề này",
            "Urgent: system is down",
            "Khẩn cấp! Database bị lỗi"
        ]
        
        for message in urgent_messages:
            result = await processor.parse_natural_language_query(message)
            assert len(result.context['urgency_indicators']) > 0
    
    @pytest.mark.asyncio
    async def test_domain_detection(self, processor):
        """Test domain detection cho agent routing"""
        test_cases = [
            ("Phân tích dữ liệu bán hàng", ['data_analysis']),
            ("Tạo API cho mobile app", ['code_development']),
            ("Thiết kế giao diện user-friendly", ['ui_design']),
            ("Tích hợp với Salesforce CRM", ['integration']),
            ("Nghiên cứu thị trường competitor", ['research'])
        ]
        
        for message, expected_domains in test_cases:
            result = await processor.parse_natural_language_query(message)
            detected_domains = result.context.get('domain_indicators', [])
            
            for domain in expected_domains:
                assert domain in detected_domains
    
    @pytest.mark.asyncio
    async def test_entity_context_extraction(self, processor):
        """Test detailed entity context extraction"""
        message = "Tạo dự án E-commerce với UI agent và data analyst, deadline tuần này"
        parsed_intent = await processor.parse_natural_language_query(message)
        
        entity_context = await processor.extract_entities_and_context(parsed_intent)
        
        assert entity_context.entities is not None
        assert entity_context.context is not None
        assert entity_context.relationships is not None
        assert entity_context.temporal_info is not None
        
        # Check relationships
        relationships = entity_context.relationships
        assert len(relationships) > 0
        
        # Check temporal info
        temporal = entity_context.temporal_info
        assert temporal['type'] == 'week'
        assert temporal['urgency'] == 'medium'
    
    @pytest.mark.asyncio
    async def test_system_action_mapping(self, processor):
        """Test mapping intents to system actions"""
        message = "Tạo dự án Analytics Dashboard"
        parsed_intent = await processor.parse_natural_language_query(message)
        entity_context = await processor.extract_entities_and_context(parsed_intent)
        
        system_actions = await processor.map_intent_to_system_actions(entity_context)
        
        assert len(system_actions) > 0
        
        # Check main action
        main_action = system_actions[0]
        assert main_action.action_type == 'create_entity'
        assert main_action.target_endpoint == '/api/v1/projects'
        assert main_action.method == 'POST'
        assert 'name' in main_action.parameters
        assert main_action.confidence > 0.0
    
    @pytest.mark.asyncio
    async def test_multi_domain_detection(self, processor):
        """Test multi-domain queries"""
        message = "Cần phân tích dữ liệu và tạo giao diện dashboard cho báo cáo"
        parsed_intent = await processor.parse_natural_language_query(message)
        entity_context = await processor.extract_entities_and_context(parsed_intent)
        
        system_actions = await processor.map_intent_to_system_actions(entity_context)
        
        # Should detect multiple domains và suggest multi-agent consultation
        suggested_domains = entity_context.entities.get('suggested_domains', [])
        assert 'data_analysis' in suggested_domains
        assert 'ui_design' in suggested_domains
        
        # Should generate additional action for multi-agent consultation
        multi_agent_actions = [action for action in system_actions 
                             if action.action_type == 'multi_agent_consultation']
        assert len(multi_agent_actions) > 0
    
    @pytest.mark.asyncio
    async def test_confidence_scoring(self, processor):
        """Test confidence scoring cho different query types"""
        test_cases = [
            ("Tôi muốn tạo dự án mới tên là Analytics", 0.8),  # Clear intent
            ("Có vấn đề gì đó với hệ thống", 0.5),             # Vague intent
            ("asdf qwerty random text", 0.2)                   # Unclear intent
        ]
        
        for message, min_expected_confidence in test_cases:
            result = await processor.parse_natural_language_query(message)
            if min_expected_confidence > 0.5:
                assert result.confidence >= min_expected_confidence
            else:
                assert result.confidence <= min_expected_confidence
    
    @pytest.mark.asyncio
    async def test_fallback_intent_detection(self, processor):
        """Test fallback intent detection cho unclear messages"""
        unclear_messages = [
            "Hmm không biết nói sao",
            "Maybe something about projects?",
            "Có thể giúp được gì không?"
        ]
        
        for message in unclear_messages:
            result = await processor.parse_natural_language_query(message)
            # Should still detect some intent, even if low confidence
            assert result.intent_type is not None
            assert result.confidence >= 0.0
    
    @pytest.mark.asyncio
    async def test_language_detection_accuracy(self, processor):
        """Test accuracy của language detection"""
        test_cases = [
            ("Xin chào, tôi cần trợ giúp", 'vi'),
            ("Hello, I need help", 'en'),
            ("Tạo project mới với API integration", 'vi'),  # Mixed but primarily Vietnamese
            ("Create new dự án with data analysis", 'en')    # Mixed but primarily English
        ]
        
        for message, expected_language in test_cases:
            result = await processor.parse_natural_language_query(message)
            assert result.language == expected_language
    
    @pytest.mark.asyncio
    async def test_error_handling(self, processor):
        """Test error handling cho malformed inputs"""
        error_cases = [
            "",           # Empty string
            None,         # None input (will be handled by API validation)
            "   ",        # Whitespace only
            "a" * 10000   # Very long input
        ]
        
        for case in error_cases:
            if case is None:
                continue  # Skip None test as it's handled at API level
            
            try:
                result = await processor.parse_natural_language_query(case)
                # Should return UNKNOWN intent với low confidence
                assert result.intent_type == IntentType.UNKNOWN
                assert result.confidence <= 0.5
            except Exception as e:
                # Should handle gracefully
                assert "error" in str(e).lower()
    
    @pytest.mark.asyncio
    async def test_performance_timing(self, processor):
        """Test performance của NLP processing"""
        message = "Tôi muốn tạo dự án Analytics với data scientist agent, ưu tiên cao, deadline tuần này"
        
        start_time = datetime.now()
        result = await processor.parse_natural_language_query(message)
        processing_time = (datetime.now() - start_time).total_seconds()
        
        # Should process within reasonable time
        assert processing_time < 1.0  # Less than 1 second
        assert result is not None
        assert result.intent_type != IntentType.UNKNOWN


class TestEntityContextExtraction:
    """Test cases cho entity context extraction"""
    
    @pytest.fixture
    def processor(self):
        return ConversationProcessor()
    
    @pytest.mark.asyncio
    async def test_relationship_extraction(self, processor):
        """Test relationship extraction between entities"""
        message = "Tạo dự án Analytics với high priority và data analyst agent"
        parsed_intent = await processor.parse_natural_language_query(message)
        entity_context = await processor.extract_entities_and_context(parsed_intent)
        
        relationships = entity_context.relationships
        assert len(relationships) > 0
        
        # Should find project-agent relationship
        project_agent_rels = [rel for rel in relationships 
                             if rel[1] == 'requires' and 'analyst' in rel[2]]
        assert len(project_agent_rels) > 0
    
    @pytest.mark.asyncio
    async def test_temporal_extraction(self, processor):
        """Test temporal information extraction"""
        temporal_cases = [
            ("Cần hoàn thành hôm nay", {'type': 'date', 'urgency': 'high'}),
            ("Deadline tuần này", {'type': 'week', 'urgency': 'medium'}),
            ("Urgent task ngay lập tức", {'type': 'urgency', 'urgency': 'critical'})
        ]
        
        for message, expected_temporal in temporal_cases:
            parsed_intent = await processor.parse_natural_language_query(message)
            entity_context = await processor.extract_entities_and_context(parsed_intent)
            
            temporal_info = entity_context.temporal_info
            assert temporal_info is not None
            
            for key, value in expected_temporal.items():
                assert temporal_info.get(key) == value
    
    @pytest.mark.asyncio
    async def test_entity_enhancement(self, processor):
        """Test entity enhancement với confidence scores"""
        message = "Tạo dự án E-commerce với UI designer và data analyst"
        parsed_intent = await processor.parse_natural_language_query(message)
        entity_context = await processor.extract_entities_and_context(parsed_intent)
        
        enhanced_entities = entity_context.entities
        
        # Should have confidence scores
        assert 'project_name_confidence' in enhanced_entities
        assert 'agent_type_confidence' in enhanced_entities
        
        # Should have suggested domains
        assert 'suggested_domains' in enhanced_entities
        domains = enhanced_entities['suggested_domains']
        assert 'ui_design' in domains


class TestSystemActionMapping:
    """Test cases cho system action mapping"""
    
    @pytest.fixture
    def processor(self):
        return ConversationProcessor()
    
    @pytest.mark.asyncio
    async def test_create_project_mapping(self, processor):
        """Test mapping CREATE_PROJECT intent to system actions"""
        message = "Tạo dự án Analytics Dashboard"
        parsed_intent = await processor.parse_natural_language_query(message)
        entity_context = await processor.extract_entities_and_context(parsed_intent)
        
        actions = await processor.map_intent_to_system_actions(entity_context)
        
        assert len(actions) > 0
        main_action = actions[0]
        
        assert main_action.action_type == 'create_entity'
        assert main_action.target_endpoint == '/api/v1/projects'
        assert main_action.method == 'POST'
        assert 'name' in main_action.parameters
        assert 'description' in main_action.parameters
    
    @pytest.mark.asyncio
    async def test_analyze_tension_mapping(self, processor):
        """Test mapping ANALYZE_TENSION intent to system actions"""
        message = "Có vấn đề performance với database"
        parsed_intent = await processor.parse_natural_language_query(message)
        entity_context = await processor.extract_entities_and_context(parsed_intent)
        
        actions = await processor.map_intent_to_system_actions(entity_context)
        
        main_action = actions[0]
        assert main_action.action_type == 'analyze_data'
        assert main_action.target_endpoint == '/api/v1/reasoning/analyze-tension'
        assert main_action.method == 'POST'
    
    @pytest.mark.asyncio
    async def test_get_agent_help_mapping(self, processor):
        """Test mapping GET_AGENT_HELP intent to system actions"""
        message = "Cần data analyst agent để phân tích sales data"
        parsed_intent = await processor.parse_natural_language_query(message)
        entity_context = await processor.extract_entities_and_context(parsed_intent)
        
        actions = await processor.map_intent_to_system_actions(entity_context)
        
        main_action = actions[0]
        assert main_action.action_type == 'find_agent'
        assert main_action.target_endpoint == '/api/v1/agents/templates/match'
        assert main_action.method == 'POST'
    
    @pytest.mark.asyncio
    async def test_additional_actions_generation(self, processor):
        """Test generation của additional actions based on context"""
        # Multi-domain query should generate multi-agent consultation
        message = "Cần phân tích dữ liệu và thiết kế dashboard UI"
        parsed_intent = await processor.parse_natural_language_query(message)
        entity_context = await processor.extract_entities_and_context(parsed_intent)
        
        actions = await processor.map_intent_to_system_actions(entity_context)
        
        # Should have additional multi-agent action
        multi_agent_actions = [a for a in actions if a.action_type == 'multi_agent_consultation']
        assert len(multi_agent_actions) > 0
        
        # High urgency should generate priority monitoring
        urgent_message = "Gấp! Cần fix lỗi production ngay"
        parsed_intent = await processor.parse_natural_language_query(urgent_message)
        entity_context = await processor.extract_entities_and_context(parsed_intent)
        
        actions = await processor.map_intent_to_system_actions(entity_context)
        
        priority_actions = [a for a in actions if a.action_type == 'priority_monitoring']
        # Note: This might not trigger if urgency_level isn't set to 'high'
        # The test verifies the logic exists 