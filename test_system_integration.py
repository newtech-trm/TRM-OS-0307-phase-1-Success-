#!/usr/bin/env python3
"""
TRM-OS System Integration Test
============================

Comprehensive test for all major system components:
- Core API endpoints
- ML-Enhanced Reasoning Engine
- Conversational Intelligence
- Adaptive Learning System
- Quantum System Manager
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, Any
from uuid import uuid4

# Core imports
from trm_api.reasoning.ml_enhanced_reasoning_engine import MLEnhancedReasoningEngine
from trm_api.reasoning.reasoning_types import ReasoningContext, ReasoningType
from trm_api.learning.adaptive_learning_system import AdaptiveLearningSystem
from trm_api.quantum.quantum_system_manager import QuantumSystemManager
from trm_api.reasoning.advanced_reasoning_engine import AdvancedReasoningEngine
from trm_api.learning.learning_types import LearningExperience, ExperienceType
from trm_api.quantum.quantum_types import WINCategory

# Conversational imports
from trm_api.v2.conversation.nlp_processor import ConversationProcessor
from trm_api.v2.conversation.session_manager import ConversationSessionManager
from trm_api.v2.conversation.response_generator import NaturalResponseGenerator, ResponseContext


async def test_system_integration():
    """Test complete system integration"""
    print("🚀 TRM-OS SYSTEM INTEGRATION TEST")
    print("=" * 80)
    
    results = {
        "ml_reasoning": False,
        "conversational_intelligence": False,
        "adaptive_learning": False,
        "quantum_system": False,
        "integration": False
    }
    
    # Test 1: ML-Enhanced Reasoning Engine
    print("\n🧠 Testing ML-Enhanced Reasoning Engine...")
    try:
        learning_system = AdaptiveLearningSystem(agent_id="integration_test")
        quantum_manager = QuantumSystemManager(learning_system=learning_system)
        advanced_reasoning = AdvancedReasoningEngine(agent_id="integration_test")
        
        ml_engine = MLEnhancedReasoningEngine(
            learning_system=learning_system,
            quantum_manager=quantum_manager,
            advanced_reasoning=advanced_reasoning
        )
        
        # Test reasoning
        context = ReasoningContext(
            context_id="integration_test",
            domain="system_integration",
            constraints={"test": True},
            objectives=["test_reasoning"],
            available_resources={"cpu": 1.0},
            priority_level=5,
            risk_tolerance=0.5
        )
        
        result = await ml_engine.reason(
            query="Test system integration reasoning",
            context=context,
            reasoning_type=ReasoningType.HYBRID
        )
        
        if result and result.confidence > 0:
            print("✅ ML-Enhanced Reasoning Engine: PASSED")
            results["ml_reasoning"] = True
        else:
            print("❌ ML-Enhanced Reasoning Engine: FAILED")
            
    except Exception as e:
        print(f"❌ ML-Enhanced Reasoning Engine: FAILED - {e}")
    
    # Test 2: Conversational Intelligence
    print("\n💬 Testing Conversational Intelligence...")
    try:
        nlp_processor = ConversationProcessor(agent_id="integration_test")
        session_manager = ConversationSessionManager()
        response_generator = NaturalResponseGenerator()
        
        # Create session
        session = await session_manager.create_conversation_session(
            user_id="integration_test",
            metadata={"test": "system_integration"}
        )
        
        # Test conversation flow
        test_message = "Tôi cần kiểm tra hệ thống integration"
        
        # Parse message
        parsed_intent = await nlp_processor.parse_natural_language_query(test_message)
        
        # Extract entities
        entity_context = await nlp_processor.extract_entities_and_context(parsed_intent)
        
        # Update context
        conversation_context = await session_manager.maintain_conversation_context(
            session.session_id, test_message, parsed_intent
        )
        
        # Generate response
        response_context = ResponseContext(
            intent=parsed_intent,
            conversation_context=conversation_context,
            action_results=[],
            suggestions=[]
        )
        
        generated_response = await response_generator.generate_natural_language_response(response_context)
        
        if (parsed_intent.confidence > 0.5 and 
            generated_response.confidence > 0.5 and
            conversation_context.turn_count > 0):
            print("✅ Conversational Intelligence: PASSED")
            results["conversational_intelligence"] = True
        else:
            print("❌ Conversational Intelligence: FAILED")
            
    except Exception as e:
        print(f"❌ Conversational Intelligence: FAILED - {e}")
    
    # Test 3: Adaptive Learning System
    print("\n🧠 Testing Adaptive Learning System...")
    try:
        learning_system = AdaptiveLearningSystem(agent_id="integration_test")
        
        # Test learning capability với correct method call
        learning_result = await learning_system.learn_from_experience(
            experience_type_or_obj=ExperienceType.PATTERN_RECOGNITION,
            context={"domain": "integration_test"},
            action_taken={"type": "test_action"},
            outcome={"success": True, "score": 0.8},
            success=True,
            performance_metrics={"accuracy": 0.9},
            confidence_level=0.9
        )
        
        if learning_result and isinstance(learning_result, str):
            print("✅ Adaptive Learning System: PASSED")
            results["adaptive_learning"] = True
        else:
            print("❌ Adaptive Learning System: FAILED")
            
    except Exception as e:
        print(f"❌ Adaptive Learning System: FAILED - {e}")
    
    # Test 4: Quantum System Manager
    print("\n⚛️ Testing Quantum System Manager...")
    try:
        learning_system = AdaptiveLearningSystem(agent_id="integration_test")
        quantum_manager = QuantumSystemManager(learning_system=learning_system)
        
        # Initialize quantum manager
        await quantum_manager.initialize()
        
        # Get first quantum system ID
        if quantum_manager.quantum_systems:
            system_id = list(quantum_manager.quantum_systems.keys())[0]
            
            # Test quantum capabilities with correct signature
            win_probability = await quantum_manager.calculate_win_probability(
                system_id=system_id,
                win_category=WINCategory.COMPOSITE,
                context={"test": True}
            )
            
            if win_probability is not None:
                print("✅ Quantum System Manager: PASSED")
                results["quantum_system"] = True
            else:
                print("❌ Quantum System Manager: FAILED")
        else:
            print("❌ Quantum System Manager: FAILED - No quantum systems")
            
    except Exception as e:
        print(f"❌ Quantum System Manager: FAILED - {e}")
    
    # Test 5: Full Integration
    print("\n🔗 Testing Full System Integration...")
    try:
        # Test conversation with ML reasoning
        nlp_processor = ConversationProcessor(agent_id="full_integration_test")
        
        # Parse complex message
        complex_message = "Tôi cần phân tích tension về performance và tạo solution với AI"
        parsed_intent = await nlp_processor.parse_natural_language_query(complex_message)
        entity_context = await nlp_processor.extract_entities_and_context(parsed_intent)
        
        # Try ML reasoning (may fail but should not crash)
        try:
            ml_insights = await nlp_processor.enhance_with_ml_reasoning(entity_context)
            ml_working = "error" not in ml_insights
        except:
            ml_working = False
        
        # Test system actions
        system_actions = await nlp_processor.map_intent_to_system_actions(entity_context)
        
        if (parsed_intent.confidence > 0.5 and 
            len(system_actions) > 0 and
            entity_context.entities):
            print("✅ Full System Integration: PASSED")
            results["integration"] = True
        else:
            print("❌ Full System Integration: FAILED")
            
    except Exception as e:
        print(f"❌ Full System Integration: FAILED - {e}")
    
    # Final Results
    print(f"\n{'='*80}")
    print("📊 INTEGRATION TEST RESULTS")
    print(f"{'='*80}")
    
    passed_tests = sum(results.values())
    total_tests = len(results)
    
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name.replace('_', ' ').title()}: {status}")
    
    print(f"\n📈 Overall Score: {passed_tests}/{total_tests} ({passed_tests/total_tests*100:.1f}%)")
    
    if passed_tests >= 4:  # At least 80% pass rate
        print("🎉 SYSTEM INTEGRATION: SUCCESS!")
        print("✅ TRM-OS is ready for production deployment")
    elif passed_tests >= 3:
        print("⚠️ SYSTEM INTEGRATION: PARTIAL SUCCESS")
        print("🔧 Some components need attention before production")
    else:
        print("❌ SYSTEM INTEGRATION: NEEDS WORK")
        print("🚧 System requires significant fixes before deployment")
    
    return results


async def test_performance_metrics():
    """Test system performance metrics"""
    print(f"\n{'='*80}")
    print("⚡ PERFORMANCE METRICS TEST")
    print(f"{'='*80}")
    
    # Test conversation processing speed
    print("\n💬 Testing Conversation Processing Speed...")
    start_time = datetime.now()
    
    nlp_processor = ConversationProcessor(agent_id="perf_test")
    
    # Process multiple messages
    test_messages = [
        "Tôi cần tạo dự án mới",
        "I need help with analysis",
        "What's the status?",
        "Analyze this tension",
        "Generate solution please"
    ]
    
    total_processed = 0
    for message in test_messages:
        try:
            parsed_intent = await nlp_processor.parse_natural_language_query(message)
            if parsed_intent.confidence > 0:
                total_processed += 1
        except:
            pass
    
    processing_time = (datetime.now() - start_time).total_seconds()
    messages_per_second = len(test_messages) / processing_time if processing_time > 0 else 0
    
    print(f"✅ Processed: {total_processed}/{len(test_messages)} messages")
    print(f"✅ Processing time: {processing_time:.3f}s")
    print(f"✅ Throughput: {messages_per_second:.1f} messages/second")
    
    # Performance thresholds
    if messages_per_second > 10:
        print("🚀 Performance: EXCELLENT")
    elif messages_per_second > 5:
        print("✅ Performance: GOOD")
    elif messages_per_second > 1:
        print("⚠️ Performance: ACCEPTABLE")
    else:
        print("❌ Performance: NEEDS OPTIMIZATION")


if __name__ == "__main__":
    print("🎯 Starting TRM-OS System Integration Test...")
    
    async def main():
        integration_results = await test_system_integration()
        await test_performance_metrics()
        
        print(f"\n{'='*80}")
        print("🏁 INTEGRATION TEST COMPLETED")
        print(f"{'='*80}")
        
        return integration_results
    
    results = asyncio.run(main()) 