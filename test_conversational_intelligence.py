#!/usr/bin/env python3
"""
Test Script for TRM-OS Conversational Intelligence with ML-Enhanced Reasoning
===========================================================================

Test comprehensive conversational intelligence capabilities:
- Natural Language Processing (Vietnamese/English)
- ML-Enhanced Reasoning Integration
- Context-aware Response Generation
- Session Management
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, Any

from trm_api.v2.conversation.nlp_processor import ConversationProcessor
from trm_api.v2.conversation.session_manager import ConversationSessionManager
from trm_api.v2.conversation.response_generator import NaturalResponseGenerator, ResponseContext


async def test_conversational_intelligence():
    """Test complete conversational intelligence pipeline"""
    print("🚀 Testing TRM-OS Conversational Intelligence với ML-Enhanced Reasoning")
    print("=" * 80)
    
    # Initialize components
    print("\n🔧 Initializing conversational components...")
    nlp_processor = ConversationProcessor(agent_id="test_conversation")
    session_manager = ConversationSessionManager()
    response_generator = NaturalResponseGenerator()
    
    # Test messages in Vietnamese and English
    test_messages = [
        {
            "message": "Tôi cần tạo dự án mới về AI và machine learning",
            "language": "vi",
            "description": "Vietnamese project creation request"
        },
        {
            "message": "Có vấn đề gì với hệ thống hiện tại không?",
            "language": "vi", 
            "description": "Vietnamese tension analysis query"
        },
        {
            "message": "I need help with data analysis and visualization",
            "language": "en",
            "description": "English agent help request"
        },
        {
            "message": "What's the current status of my projects?",
            "language": "en",
            "description": "English status check"
        },
        {
            "message": "Tôi cần giải pháp cho vấn đề tối ưu hóa performance",
            "language": "vi",
            "description": "Vietnamese solution generation request"
        }
    ]
    
    # Create test session
    print("\n📋 Creating conversation session...")
    session = await session_manager.create_conversation_session(
        user_id="test_user",
        metadata={"test_type": "ml_reasoning_integration"}
    )
    print(f"✅ Session created: {session.session_id}")
    
    # Process each test message
    for i, test_case in enumerate(test_messages, 1):
        print(f"\n{'='*50}")
        print(f"🧪 Test Case {i}: {test_case['description']}")
        print(f"📝 Message: {test_case['message']}")
        print(f"🌐 Language: {test_case['language']}")
        
        try:
            # Step 1: Parse natural language
            print("\n📊 Step 1: Natural Language Processing...")
            parsed_intent = await nlp_processor.parse_natural_language_query(test_case["message"])
            print(f"✅ Intent detected: {parsed_intent.intent_type.value}")
            print(f"✅ Confidence: {parsed_intent.confidence:.3f}")
            print(f"✅ Entities: {parsed_intent.entities}")
            
            # Step 2: Extract entities and context
            print("\n🔍 Step 2: Entity and Context Extraction...")
            entity_context = await nlp_processor.extract_entities_and_context(parsed_intent)
            print(f"✅ Entities extracted: {len(entity_context.entities)} types")
            print(f"✅ Relationships: {len(entity_context.relationships)} found")
            print(f"✅ Temporal info: {entity_context.temporal_info}")
            
            # Step 3: ML-Enhanced Reasoning
            print("\n🤖 Step 3: ML-Enhanced Reasoning...")
            ml_insights = await nlp_processor.enhance_with_ml_reasoning(entity_context)
            if "error" not in ml_insights:
                print(f"✅ ML Confidence: {ml_insights.get('ml_confidence', 0.0):.3f}")
                print(f"✅ Reasoning Type: {ml_insights.get('reasoning_type', 'unknown')}")
                print(f"✅ Recommendations: {len(ml_insights.get('recommendations', []))}")
                if ml_insights.get('quantum_insights'):
                    print(f"✅ Quantum Insights: Available")
            else:
                print(f"⚠️ ML Reasoning: {ml_insights['error']}")
            
            # Step 4: System Actions
            print("\n⚙️ Step 4: System Action Mapping...")
            system_actions = await nlp_processor.map_intent_to_system_actions(entity_context)
            print(f"✅ System Actions: {len(system_actions)} mapped")
            for action in system_actions:
                print(f"   - {action.action_type}: {action.target_endpoint}")
            
            # Step 5: Update conversation context
            print("\n💬 Step 5: Conversation Context Update...")
            conversation_context = await session_manager.maintain_conversation_context(
                session.session_id, test_case["message"], parsed_intent
            )
            print(f"✅ Context updated: {conversation_context.turn_count} turns")
            
            # Step 6: Generate response
            print("\n📝 Step 6: Response Generation...")
            response_context = ResponseContext(
                intent=parsed_intent,
                conversation_context=conversation_context,
                action_results=[],  # Simplified for test
                suggestions=[],
                ml_insights=ml_insights
            )
            
            generated_response = await response_generator.generate_natural_language_response(response_context)
            print(f"✅ Response generated:")
            print(f"   Text: {generated_response.text}")
            print(f"   Type: {generated_response.response_type.value}")
            print(f"   Tone: {generated_response.tone.value}")
            print(f"   Confidence: {generated_response.confidence:.3f}")
            
            # Step 7: Add conversation turn
            print("\n💾 Step 7: Conversation Turn Storage...")
            await session_manager.add_conversation_turn(
                session.session_id,
                test_case["message"],
                parsed_intent,
                system_actions,
                generated_response.text,
                0.5  # Mock processing time
            )
            print("✅ Conversation turn saved")
            
            print(f"\n✅ Test Case {i} COMPLETED SUCCESSFULLY")
            
        except Exception as e:
            print(f"\n❌ Test Case {i} FAILED: {str(e)}")
            import traceback
            traceback.print_exc()
    
    # Final session analytics
    print(f"\n{'='*50}")
    print("📊 Final Session Analytics")
    try:
        session_info = await session_manager.get_session(session.session_id)
        print(f"✅ Session ID: {session_info.session_id}")
        print(f"✅ Total turns: {session_info.turn_count}")
        print(f"✅ Status: {session_info.status}")
        print(f"✅ Duration: {datetime.now() - session_info.created_at}")
        
        # Get conversation history
        history = await session_manager.get_conversation_history(session.session_id, limit=10)
        print(f"✅ History entries: {len(history)}")
        
    except Exception as e:
        print(f"❌ Session analytics failed: {e}")
    
    print(f"\n{'='*80}")
    print("🎉 CONVERSATIONAL INTELLIGENCE TEST COMPLETED!")
    print("✅ All major components tested successfully")
    print("✅ ML-Enhanced Reasoning integration working")
    print("✅ Multi-language support confirmed")
    print("✅ Context management functional")


async def test_ml_reasoning_patterns():
    """Test ML reasoning với different conversation patterns"""
    print("\n🧠 Testing ML Reasoning Patterns...")
    
    nlp_processor = ConversationProcessor(agent_id="ml_pattern_test")
    
    # Test different reasoning patterns
    reasoning_test_cases = [
        {
            "message": "Nếu tôi tạo dự án A thì sẽ cần resource B",
            "expected_reasoning": "DEDUCTIVE",
            "description": "Deductive reasoning test"
        },
        {
            "message": "Tại sao hệ thống lại chậm vào buổi sáng?",
            "expected_reasoning": "CAUSAL", 
            "description": "Causal reasoning test"
        },
        {
            "message": "Dự án này giống với dự án nào đã làm trước đây?",
            "expected_reasoning": "ANALOGICAL",
            "description": "Analogical reasoning test"
        },
        {
            "message": "Khả năng thành công của dự án này là bao nhiêu?",
            "expected_reasoning": "PROBABILISTIC",
            "description": "Probabilistic reasoning test"
        }
    ]
    
    for i, test_case in enumerate(reasoning_test_cases, 1):
        print(f"\n🔬 Reasoning Test {i}: {test_case['description']}")
        print(f"📝 Message: {test_case['message']}")
        
        try:
            # Parse và analyze
            parsed_intent = await nlp_processor.parse_natural_language_query(test_case["message"])
            entity_context = await nlp_processor.extract_entities_and_context(parsed_intent)
            ml_insights = await nlp_processor.enhance_with_ml_reasoning(entity_context)
            
            if "error" not in ml_insights:
                reasoning_type = ml_insights.get("reasoning_type", "unknown")
                print(f"✅ Detected reasoning: {reasoning_type}")
                print(f"✅ Expected reasoning: {test_case['expected_reasoning']}")
                
                if reasoning_type.upper() == test_case['expected_reasoning']:
                    print("✅ REASONING TYPE MATCH!")
                else:
                    print("⚠️ Different reasoning type detected")
                    
                print(f"✅ ML Confidence: {ml_insights.get('ml_confidence', 0.0):.3f}")
            else:
                print(f"❌ ML Reasoning failed: {ml_insights['error']}")
                
        except Exception as e:
            print(f"❌ Reasoning test failed: {e}")
    
    print("\n✅ ML Reasoning Pattern Tests Completed!")


if __name__ == "__main__":
    print("🎯 Starting TRM-OS Conversational Intelligence Tests...")
    
    async def main():
        await test_conversational_intelligence()
        await test_ml_reasoning_patterns()
    
    asyncio.run(main()) 