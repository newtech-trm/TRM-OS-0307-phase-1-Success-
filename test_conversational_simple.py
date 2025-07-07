#!/usr/bin/env python3
"""
Simple Test for TRM-OS Conversational Intelligence
=================================================

Test basic conversational capabilities without complex ML reasoning
"""

import asyncio
from datetime import datetime

from trm_api.v2.conversation.nlp_processor import ConversationProcessor
from trm_api.v2.conversation.session_manager import ConversationSessionManager
from trm_api.v2.conversation.response_generator import NaturalResponseGenerator, ResponseContext


async def test_basic_conversation():
    """Test basic conversation flow without ML reasoning"""
    print("🧪 Testing Basic Conversational Intelligence")
    print("=" * 60)
    
    # Initialize components
    print("\n🔧 Initializing components...")
    nlp_processor = ConversationProcessor(agent_id="test_basic")
    session_manager = ConversationSessionManager()
    response_generator = NaturalResponseGenerator()
    
    # Test messages
    test_messages = [
        "Tôi cần tạo dự án mới",
        "I need help with data analysis",
        "What's the status of my work?"
    ]
    
    # Create session
    print("\n📋 Creating session...")
    session = await session_manager.create_conversation_session(
        user_id="test_user",
        metadata={"test": "basic_conversation"}
    )
    print(f"✅ Session: {session.session_id}")
    
    # Process each message
    for i, message in enumerate(test_messages, 1):
        print(f"\n{'='*40}")
        print(f"🧪 Test {i}: {message}")
        
        try:
            # Parse message
            print("📊 Parsing...")
            parsed_intent = await nlp_processor.parse_natural_language_query(message)
            print(f"✅ Intent: {parsed_intent.intent_type.value} (confidence: {parsed_intent.confidence:.3f})")
            
            # Extract entities
            print("🔍 Extracting entities...")
            entity_context = await nlp_processor.extract_entities_and_context(parsed_intent)
            print(f"✅ Entities: {len(entity_context.entities)} types")
            
            # Update context
            print("💬 Updating context...")
            conversation_context = await session_manager.maintain_conversation_context(
                session.session_id, message, parsed_intent
            )
            print(f"✅ Context updated: {conversation_context.turn_count} turns")
            
            # Generate response
            print("📝 Generating response...")
            response_context = ResponseContext(
                intent=parsed_intent,
                conversation_context=conversation_context,
                action_results=[],
                suggestions=[]
            )
            
            generated_response = await response_generator.generate_natural_language_response(response_context)
            print(f"✅ Response: {generated_response.text}")
            print(f"   Type: {generated_response.response_type.value}")
            print(f"   Confidence: {generated_response.confidence:.3f}")
            
            # Add turn
            print("💾 Saving turn...")
            await session_manager.add_conversation_turn(
                session.session_id,
                message,
                parsed_intent,
                [],  # No system actions for basic test
                generated_response.text,
                0.1  # Mock processing time
            )
            print("✅ Turn saved")
            
        except Exception as e:
            print(f"❌ Test {i} failed: {e}")
    
    # Final analytics
    print(f"\n{'='*40}")
    print("📊 Final Analytics")
    try:
        final_session = await session_manager.get_session(session.session_id)
        print(f"✅ Total turns: {final_session.turn_count}")
        print(f"✅ Session status: {final_session.status}")
        
        history = await session_manager.get_conversation_history(session.session_id)
        print(f"✅ History entries: {len(history)}")
        
    except Exception as e:
        print(f"❌ Analytics failed: {e}")
    
    print(f"\n{'='*60}")
    print("🎉 BASIC CONVERSATION TEST COMPLETED!")


if __name__ == "__main__":
    asyncio.run(test_basic_conversation()) 