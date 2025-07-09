#!/usr/bin/env python3
"""
Conversational API Endpoints for TRM-OS v2
==========================================

Natural language interface endpoints với WebSocket support
cho real-time conversational intelligence.
"""

import asyncio
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException, Depends
from pydantic import BaseModel, Field

from trm_api.core.logging_config import get_logger
from trm_api.v2.conversation.nlp_processor import ConversationProcessor
from trm_api.v2.conversation.session_manager import ConversationSessionManager
from trm_api.v2.conversation.response_generator import NaturalResponseGenerator, ResponseContext
from trm_api.services.user_service import get_current_user  # Fixed import path
from trm_api.schemas.user import UserResponse  # Import UserResponse

logger = get_logger(__name__)

# Initialize conversational components
nlp_processor = ConversationProcessor()
session_manager = ConversationSessionManager()
response_generator = NaturalResponseGenerator()

router = APIRouter(prefix="/conversations", tags=["Conversational Intelligence"])


# Pydantic models
class ConversationRequest(BaseModel):
    """Request model cho conversation analysis"""
    message: str = Field(..., description="User's natural language message")
    session_id: Optional[str] = Field(None, description="Optional session ID for context")
    language: Optional[str] = Field(None, description="Preferred language (vi/en)")
    context: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional context")


class ConversationResponse(BaseModel):
    """Response model cho conversation"""
    response_text: str = Field(..., description="Natural language response")
    intent_detected: str = Field(..., description="Detected intent type")
    confidence: float = Field(..., description="Confidence score 0-1")
    session_id: str = Field(..., description="Session ID for context tracking")
    suggested_actions: List[str] = Field(default_factory=list, description="Suggested follow-up actions")
    entities_extracted: Dict[str, Any] = Field(default_factory=dict, description="Extracted entities")
    system_actions: List[Dict[str, Any]] = Field(default_factory=list, description="System actions taken")
    processing_time: float = Field(..., description="Processing time in seconds")


class SessionRequest(BaseModel):
    """Request model cho session management"""
    user_id: str = Field(..., description="User ID")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Session metadata")


class SessionResponse(BaseModel):
    """Response model cho session info"""
    session_id: str = Field(..., description="Session ID")
    user_id: str = Field(..., description="User ID")
    status: str = Field(..., description="Session status")
    created_at: datetime = Field(..., description="Session creation time")
    turn_count: int = Field(..., description="Number of conversation turns")


class WebSocketManager:
    """Manage WebSocket connections cho real-time chat"""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.user_sessions: Dict[str, str] = {}  # user_id -> session_id
    
    async def connect(self, websocket: WebSocket, user_id: str, session_id: str):
        """Accept WebSocket connection"""
        await websocket.accept()
        self.active_connections[session_id] = websocket
        self.user_sessions[user_id] = session_id
        logger.info(f"WebSocket connected for session {session_id}")
    
    def disconnect(self, session_id: str):
        """Remove WebSocket connection"""
        if session_id in self.active_connections:
            del self.active_connections[session_id]
        
        # Remove user session mapping
        user_to_remove = None
        for user_id, sess_id in self.user_sessions.items():
            if sess_id == session_id:
                user_to_remove = user_id
                break
        
        if user_to_remove:
            del self.user_sessions[user_to_remove]
        
        logger.info(f"WebSocket disconnected for session {session_id}")
    
    async def send_message(self, session_id: str, message: Dict[str, Any]):
        """Send message to specific session"""
        if session_id in self.active_connections:
            websocket = self.active_connections[session_id]
            try:
                await websocket.send_text(json.dumps(message))
            except Exception as e:
                logger.error(f"Error sending WebSocket message: {e}")
                self.disconnect(session_id)
    
    async def broadcast_to_user(self, user_id: str, message: Dict[str, Any]):
        """Broadcast message to all user's sessions"""
        session_id = self.user_sessions.get(user_id)
        if session_id:
            await self.send_message(session_id, message)


websocket_manager = WebSocketManager()


@router.post("/analyze", response_model=ConversationResponse)
async def analyze_conversation(
    request: ConversationRequest,
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Analyze natural language message và generate intelligent response với Commercial AI Coordination
    
    Supports:
    - Vietnamese và English language processing
    - Intent detection và entity extraction
    - Commercial AI coordination cho intelligent insights
    - Context-aware response generation
    - System action execution
    """
    start_time = datetime.now()
    
    try:
        logger.info(f"Processing conversation request for user {current_user.uid}")
        
        # Get or create session
        if request.session_id:
            session = await session_manager.get_session(request.session_id)
            if not session:
                raise HTTPException(status_code=404, detail="Session not found or expired")
        else:
            session = await session_manager.create_conversation_session(
                user_id=current_user.uid,
                metadata=request.context
            )
        
        # Parse natural language
        parsed_intent = await nlp_processor.parse_natural_language_query(request.message)
        
        # Update conversation context
        conversation_context = await session_manager.maintain_conversation_context(
            session.session_id, request.message, parsed_intent
        )
        
        # Extract entities và context
        entity_context = await nlp_processor.extract_entities_and_context(parsed_intent)
        
        # NEW: Enhance với Commercial AI coordination
        ai_insights = await nlp_processor.enhance_with_commercial_ai(entity_context)
        
        # Map intent to system actions
        system_actions = await nlp_processor.map_intent_to_system_actions(entity_context)
        
        # Execute system actions (simplified for MVP)
        action_results = await execute_system_actions(system_actions)
        
        # Get contextual suggestions
        suggestions = await session_manager.get_contextual_suggestions(
            session.session_id, parsed_intent
        )
        
        # NEW: Add Commercial AI insights to suggestions
        if ai_insights and "recommendations" in ai_insights:
            ai_recommendations = ai_insights["recommendations"]
            suggestions.extend(ai_recommendations[:3])  # Add top 3 Commercial AI recommendations
        
        # Generate natural language response
        response_context = ResponseContext(
            intent=parsed_intent,
            conversation_context=conversation_context,
            action_results=action_results,
            suggestions=suggestions,
            ai_insights=ai_insights  # Pass Commercial AI insights to response generator
        )
        
        generated_response = await response_generator.generate_natural_language_response(response_context)
        
        # Add conversation turn
        processing_time = (datetime.now() - start_time).total_seconds()
        await session_manager.add_conversation_turn(
            session.session_id,
            request.message,
            parsed_intent,
            system_actions,
            generated_response.text,
            processing_time
        )
        
        # Send WebSocket notification if connected
        if session.session_id in websocket_manager.active_connections:
            await websocket_manager.send_message(session.session_id, {
                "type": "response",
                "text": generated_response.text,
                "intent": parsed_intent.intent_type.value,
                "confidence": parsed_intent.confidence,
                "ai_confidence": ai_insights.get("confidence", 0.0),
                "reasoning_type": ai_insights.get("reasoning_type", "commercial_ai")
            })
        
        return ConversationResponse(
            response_text=generated_response.text,
            intent_detected=parsed_intent.intent_type.value,
            confidence=parsed_intent.confidence,
            session_id=session.session_id,
            suggested_actions=suggestions,
            entities_extracted=entity_context.entities,
            system_actions=[action.dict() for action in system_actions],
            processing_time=processing_time
        )
        
    except Exception as e:
        logger.error(f"Error processing conversation: {e}")
        raise HTTPException(status_code=500, detail=f"Conversation processing failed: {str(e)}")


@router.post("/sessions", response_model=SessionResponse)
async def create_session(
    request: SessionRequest,
    current_user: UserResponse = Depends(get_current_user)
):
    """Create new conversation session"""
    try:
        session = await session_manager.create_conversation_session(
            user_id=request.user_id,
            metadata=request.metadata
        )
        
        return SessionResponse(
            session_id=session.session_id,
            user_id=session.user_id,
            status=session.context.conversation_state,
            created_at=session.start_time,
            turn_count=len(session.turns)
        )
        
    except Exception as e:
        logger.error(f"Error creating session: {e}")
        raise HTTPException(status_code=500, detail=f"Session creation failed: {str(e)}")


@router.get("/sessions/{session_id}", response_model=SessionResponse)
async def get_session(
    session_id: str,
    current_user: UserResponse = Depends(get_current_user)
):
    """Get conversation session info"""
    try:
        session = await session_manager.get_session(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        return SessionResponse(
            session_id=session.session_id,
            user_id=session.user_id,
            status=session.context.conversation_state,
            created_at=session.start_time,
            turn_count=len(session.turns)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting session: {e}")
        raise HTTPException(status_code=500, detail=f"Session retrieval failed: {str(e)}")


@router.delete("/sessions/{session_id}")
async def end_session(
    session_id: str,
    current_user: UserResponse = Depends(get_current_user)
):
    """End conversation session"""
    try:
        success = await session_manager.end_conversation_session(session_id)
        if not success:
            raise HTTPException(status_code=404, detail="Session not found")
        
        # Disconnect WebSocket if active
        websocket_manager.disconnect(session_id)
        
        return {"message": "Session ended successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error ending session: {e}")
        raise HTTPException(status_code=500, detail=f"Session termination failed: {str(e)}")


@router.get("/sessions/{session_id}/history")
async def get_conversation_history(
    session_id: str,
    limit: int = 10,
    current_user: UserResponse = Depends(get_current_user)
):
    """Get conversation history for session"""
    try:
        history = await session_manager.get_conversation_history(session_id, limit)
        
        return {
            "session_id": session_id,
            "turn_count": len(history),
            "turns": [
                {
                    "turn_id": turn.turn_id,
                    "user_message": turn.user_message,
                    "response": turn.response,
                    "intent": turn.parsed_intent.intent_type.value,
                    "confidence": turn.parsed_intent.confidence,
                    "timestamp": turn.timestamp.isoformat(),
                    "processing_time": turn.processing_time
                }
                for turn in history
            ]
        }
        
    except Exception as e:
        logger.error(f"Error getting conversation history: {e}")
        raise HTTPException(status_code=500, detail=f"History retrieval failed: {str(e)}")


@router.get("/sessions/{session_id}/analytics")
async def get_session_analytics(
    session_id: str,
    current_user: UserResponse = Depends(get_current_user)
):
    """Get analytics for conversation session"""
    try:
        analytics = await session_manager.get_session_analytics(session_id)
        if not analytics:
            raise HTTPException(status_code=404, detail="Session not found")
        
        return analytics
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting session analytics: {e}")
        raise HTTPException(status_code=500, detail=f"Analytics retrieval failed: {str(e)}")


@router.websocket("/realtime/{session_id}")
async def websocket_conversation(websocket: WebSocket, session_id: str):
    """
    WebSocket endpoint cho real-time conversation
    
    Supports:
    - Real-time message exchange
    - Typing indicators
    - Connection health monitoring
    """
    await websocket.accept()
    user_id = None
    
    try:
        # Get session info
        session = await session_manager.get_session(session_id)
        if not session:
            await websocket.send_text(json.dumps({
                "type": "error",
                "message": "Session not found"
            }))
            await websocket.close()
            return
        
        user_id = session.user_id
        await websocket_manager.connect(websocket, user_id, session_id)
        
        # Send welcome message
        await websocket.send_text(json.dumps({
            "type": "connected",
            "session_id": session_id,
            "message": "Connected to TRM-OS Conversational Intelligence"
        }))
        
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            if message_data.get("type") == "message":
                user_message = message_data.get("message", "")
                
                # Send typing indicator
                await websocket.send_text(json.dumps({
                    "type": "typing",
                    "message": "TRM-OS is thinking..."
                }))
                
                # Process message through conversation pipeline
                try:
                    # Parse natural language
                    parsed_intent = await nlp_processor.parse_natural_language_query(user_message)
                    
                    # Update conversation context
                    conversation_context = await session_manager.maintain_conversation_context(
                        session_id, user_message, parsed_intent
                    )
                    
                    # Extract entities và context
                    entity_context = await nlp_processor.extract_entities_and_context(parsed_intent)
                    
                    # Map intent to system actions
                    system_actions = await nlp_processor.map_intent_to_system_actions(entity_context)
                    
                    # Execute system actions
                    action_results = await execute_system_actions(system_actions)
                    
                    # Get contextual suggestions
                    suggestions = await session_manager.get_contextual_suggestions(
                        session_id, parsed_intent
                    )
                    
                    # Generate response
                    response_context = ResponseContext(
                        intent=parsed_intent,
                        conversation_context=conversation_context,
                        action_results=action_results,
                        suggestions=suggestions
                    )
                    
                    generated_response = await response_generator.generate_natural_language_response(response_context)
                    
                    # Add conversation turn
                    await session_manager.add_conversation_turn(
                        session_id,
                        user_message,
                        parsed_intent,
                        system_actions,
                        generated_response.text,
                        0.1  # WebSocket processing time placeholder
                    )
                    
                    # Send response
                    await websocket.send_text(json.dumps({
                        "type": "response",
                        "message": generated_response.text,
                        "intent": parsed_intent.intent_type.value,
                        "confidence": parsed_intent.confidence,
                        "suggested_actions": generated_response.suggested_actions,
                        "entities": parsed_intent.entities
                    }))
                    
                except Exception as e:
                    logger.error(f"Error processing WebSocket message: {e}")
                    await websocket.send_text(json.dumps({
                        "type": "error",
                        "message": f"Processing error: {str(e)}"
                    }))
            
            elif message_data.get("type") == "ping":
                # Health check
                await websocket.send_text(json.dumps({
                    "type": "pong",
                    "timestamp": datetime.now().isoformat()
                }))
                
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for session {session_id}")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        websocket_manager.disconnect(session_id)


async def execute_system_actions(system_actions: List) -> List[Dict[str, Any]]:
    """
    Execute system actions (simplified for MVP)
    
    Args:
        system_actions: List of SystemAction objects
        
    Returns:
        List of action results
    """
    results = []
    
    for action in system_actions:
        try:
            # Simplified action execution - in production, would call actual v1 API endpoints
            result = {
                "action_type": action.action_type,
                "status": "simulated",
                "message": f"Simulated execution of {action.action_type}",
                "parameters": action.parameters,
                "endpoint": action.target_endpoint,
                "method": action.method
            }
            
            # Add specific handling based on action type
            if action.action_type == "create_entity":
                result["created_id"] = f"mock_{action.action_type}_{len(results)}"
            elif action.action_type == "analyze_data":
                result["analysis_result"] = "Mock analysis completed"
            elif action.action_type == "find_agent":
                result["recommended_agents"] = ["data_analyst", "integration_specialist"]
            
            results.append(result)
            
        except Exception as e:
            logger.error(f"Error executing action {action.action_type}: {e}")
            results.append({
                "action_type": action.action_type,
                "status": "error",
                "error": str(e)
            })
    
    return results


@router.get("/health")
async def health_check():
    """Health check cho conversation endpoints"""
    active_sessions_count = len(session_manager.active_sessions)
    websocket_connections_count = len(websocket_manager.active_connections)
    
    return {
        "status": "healthy",
        "service": "Conversational Intelligence",
        "components": {
            "nlp_processor": "active",
            "session_manager": "active", 
            "response_generator": "active",
            "websocket_manager": f"{websocket_connections_count} active connections"
        },
        "active_sessions": active_sessions_count,
        "websocket_connections": websocket_connections_count,
        "timestamp": datetime.now().isoformat()
    } 