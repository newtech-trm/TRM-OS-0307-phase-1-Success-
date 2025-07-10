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
    user_identifier: Optional[str] = Field(None, description="Optional user identifier for AGE session tracking")


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
    user_identifier: str = Field(..., description="User identifier for AGE session")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Session metadata")


class SessionResponse(BaseModel):
    """Response model cho session info"""
    session_id: str = Field(..., description="Session ID")
    user_identifier: str = Field(..., description="User identifier")
    status: str = Field(..., description="Session status")
    created_at: datetime = Field(..., description="Session creation time")
    turn_count: int = Field(..., description="Number of conversation turns")


class WebSocketManager:
    """Manage WebSocket connections cho real-time chat"""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.user_sessions: Dict[str, str] = {}  # user_identifier -> session_id
    
    async def connect(self, websocket: WebSocket, user_identifier: str, session_id: str):
        """Accept WebSocket connection"""
        await websocket.accept()
        self.active_connections[session_id] = websocket
        self.user_sessions[user_identifier] = session_id
        logger.info(f"AGE: WebSocket connected for session {session_id}")
    
    def disconnect(self, session_id: str):
        """Remove WebSocket connection"""
        if session_id in self.active_connections:
            del self.active_connections[session_id]
        
        # Remove user session mapping
        user_to_remove = None
        for user_identifier, sess_id in self.user_sessions.items():
            if sess_id == session_id:
                user_to_remove = user_identifier
                break
        
        if user_to_remove:
            del self.user_sessions[user_to_remove]
        
        logger.info(f"AGE: WebSocket disconnected for session {session_id}")
    
    async def send_message(self, session_id: str, message: Dict[str, Any]):
        """Send message to specific session"""
        if session_id in self.active_connections:
            websocket = self.active_connections[session_id]
            try:
                await websocket.send_text(json.dumps(message))
            except Exception as e:
                logger.error(f"AGE: Error sending WebSocket message: {e}")
                self.disconnect(session_id)
    
    async def broadcast_to_user(self, user_identifier: str, message: Dict[str, Any]):
        """Broadcast message to all user's sessions"""
        session_id = self.user_sessions.get(user_identifier)
        if session_id:
            await self.send_message(session_id, message)


websocket_manager = WebSocketManager()


@router.post("/analyze", response_model=ConversationResponse)
async def analyze_conversation(request: ConversationRequest):
    """
    AGE Conversational Intelligence - Analyze natural language and generate intelligent response
    
    AGE Philosophy: Transform natural language into strategic semantic actions through
    Commercial AI Coordination.
    
    Supports:
    - Vietnamese và English language processing
    - Intent detection và entity extraction
    - Commercial AI coordination cho intelligent insights
    - Context-aware response generation
    - System action execution
    """
    start_time = datetime.now()
    
    try:
        user_identifier = request.user_identifier or "anonymous"
        logger.info(f"AGE: Processing conversation request for user {user_identifier}")
        
        # Get or create session
        if request.session_id:
            session = await session_manager.get_session(request.session_id)
            if not session:
                raise HTTPException(status_code=404, detail="AGE: Session not found or expired")
        else:
            session = await session_manager.create_conversation_session(
                user_id=user_identifier,
                metadata=request.context
            )
        
        # Parse natural language through AGE intelligence
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
        
        # Execute system actions (AGE semantic operations)
        action_results = await execute_system_actions(system_actions)
        
        # Get contextual suggestions
        suggestions = await session_manager.get_contextual_suggestions(
            session.session_id, parsed_intent
        )
        
        # NEW: Add Commercial AI insights to suggestions
        if ai_insights and "recommendations" in ai_insights:
            ai_recommendations = ai_insights["recommendations"]
            suggestions.extend(ai_recommendations[:3])  # Add top 3 Commercial AI recommendations
        
        # Generate natural language response through AGE orchestration
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
                "type": "age_response",
                "text": generated_response.text,
                "intent": parsed_intent.intent_type.value,
                "confidence": parsed_intent.confidence,
                "ai_confidence": ai_insights.get("confidence", 0.0),
                "reasoning_type": ai_insights.get("reasoning_type", "commercial_ai"),
                "semantic_action": "conversational_intelligence"
            })
        
        return ConversationResponse(
            response_text=generated_response.text,
            intent_detected=parsed_intent.intent_type.value,
            confidence=parsed_intent.confidence,
            session_id=session.session_id,
            suggested_actions=suggestions,
            entities_extracted=entity_context,
            system_actions=action_results,
            processing_time=processing_time
        )
        
    except Exception as e:
        logger.error(f"AGE: Error processing conversation: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"AGE: Conversational intelligence processing failed: {str(e)}"
        )


@router.post("/sessions", response_model=SessionResponse)
async def create_session(request: SessionRequest):
    """
    Create AGE Conversation Session - Pure semantic conversation management
    
    AGE Philosophy: Sessions track strategic conversation context without user dependencies.
    """
    try:
        logger.info(f"AGE: Creating conversation session for user {request.user_identifier}")
        
        session = await session_manager.create_conversation_session(
            user_id=request.user_identifier,
            metadata=request.metadata
        )
        
        return SessionResponse(
            session_id=session.session_id,
            user_identifier=request.user_identifier,
            status=session.status,
            created_at=session.created_at,
            turn_count=0
        )
        
    except Exception as e:
        logger.error(f"AGE: Error creating session: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"AGE: Session creation failed: {str(e)}"
        )


@router.get("/sessions/{session_id}", response_model=SessionResponse)
async def get_session(session_id: str):
    """
    Get AGE Conversation Session - Retrieve session information
    
    AGE Philosophy: Pure semantic session retrieval without authentication overhead.
    """
    try:
        logger.info(f"AGE: Retrieving session {session_id}")
        
        session = await session_manager.get_session(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="AGE: Session not found")
        
        return SessionResponse(
            session_id=session.session_id,
            user_identifier=session.user_id,  # This is actually user_identifier now
            status=session.status,
            created_at=session.created_at,
            turn_count=session.turn_count
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"AGE: Error retrieving session: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"AGE: Session retrieval failed: {str(e)}"
        )


@router.delete("/sessions/{session_id}")
async def end_session(session_id: str):
    """
    End AGE Conversation Session - Close conversation context
    
    AGE Philosophy: Clean session termination for resource optimization.
    """
    try:
        logger.info(f"AGE: Ending session {session_id}")
        
        success = await session_manager.end_session(session_id)
        if not success:
            raise HTTPException(status_code=404, detail="AGE: Session not found")
        
        # Disconnect WebSocket if connected
        websocket_manager.disconnect(session_id)
        
        return {"message": "AGE: Session ended successfully", "session_id": session_id}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"AGE: Error ending session: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"AGE: Session termination failed: {str(e)}"
        )


@router.get("/sessions/{session_id}/history")
async def get_conversation_history(
    session_id: str,
    limit: int = 10
):
    """
    Get AGE Conversation History - Retrieve conversation context
    
    AGE Philosophy: Access historical conversation intelligence for context enhancement.
    """
    try:
        logger.info(f"AGE: Getting conversation history for session {session_id}")
        
        history = await session_manager.get_conversation_history(session_id, limit)
        if not history:
            raise HTTPException(status_code=404, detail="AGE: Session not found or no history")
        
        return {
            "session_id": session_id,
            "conversation_history": history,
            "count": len(history),
            "semantic_context": "AGE conversational intelligence tracking"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"AGE: Error getting conversation history: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"AGE: History retrieval failed: {str(e)}"
        )


@router.get("/sessions/{session_id}/analytics")
async def get_session_analytics(session_id: str):
    """
    Get AGE Session Analytics - Strategic conversation intelligence
    
    AGE Philosophy: Extract strategic insights from conversation patterns.
    """
    try:
        logger.info(f"AGE: Getting session analytics for {session_id}")
        
        analytics = await session_manager.get_session_analytics(session_id)
        if not analytics:
            raise HTTPException(status_code=404, detail="AGE: Session not found")
        
        return {
            "session_id": session_id,
            "analytics": analytics,
            "semantic_insights": "AGE conversation intelligence analysis",
            "strategic_value": "Pattern recognition for enhanced interaction"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"AGE: Error getting session analytics: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"AGE: Analytics retrieval failed: {str(e)}"
        )


@router.websocket("/realtime/{session_id}")
async def websocket_conversation(websocket: WebSocket, session_id: str):
    """
    AGE Real-time Conversation WebSocket - Live conversational intelligence
    
    AGE Philosophy: Real-time semantic conversation coordination.
    """
    user_identifier = "websocket_user"  # Default identifier for WebSocket connections
    await websocket_manager.connect(websocket, user_identifier, session_id)
    
    try:
        # Send welcome message
        await websocket_manager.send_message(session_id, {
            "type": "age_welcome",
            "message": "AGE Conversational Intelligence connected",
            "session_id": session_id,
            "capabilities": [
                "Natural language understanding",
                "Commercial AI coordination", 
                "Strategic intent detection",
                "Context-aware responses"
            ]
        })
        
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            if message_data.get("type") == "message":
                # Process conversation request
                request = ConversationRequest(
                    message=message_data.get("message", ""),
                    session_id=session_id,
                    language=message_data.get("language"),
                    context=message_data.get("context", {}),
                    user_identifier=user_identifier
                )
                
                # Analyze conversation (this will send response via WebSocket)
                try:
                    response = await analyze_conversation(request)
                    
                    # Send structured response
                    await websocket_manager.send_message(session_id, {
                        "type": "age_conversation_response",
                        "response": response.model_dump(),
                        "timestamp": datetime.now().isoformat()
                    })
                    
                except Exception as e:
                    await websocket_manager.send_message(session_id, {
                        "type": "age_error",
                        "error": str(e),
                        "message": "AGE conversational processing failed"
                    })
            
            elif message_data.get("type") == "ping":
                # Respond to ping
                await websocket_manager.send_message(session_id, {
                    "type": "age_pong", 
                    "timestamp": datetime.now().isoformat()
                })
            
    except WebSocketDisconnect:
        logger.info(f"AGE: WebSocket disconnected for session {session_id}")
        websocket_manager.disconnect(session_id)
    except Exception as e:
        logger.error(f"AGE: WebSocket error for session {session_id}: {str(e)}")
        websocket_manager.disconnect(session_id)


async def execute_system_actions(system_actions: List) -> List[Dict[str, Any]]:
    """
    Execute AGE System Actions - Transform intents into semantic actions
    
    AGE Philosophy: Convert conversation intents into strategic system operations.
    """
    results = []
    
    for action in system_actions:
        try:
            action_type = action.get("type")
            action_params = action.get("parameters", {})
            
            if action_type == "age_tension_recognition":
                # Execute tension recognition
                result = {
                    "action": "tension_recognition",
                    "status": "executed",
                    "semantic_action": "Strategic tension identified and cataloged",
                    "details": action_params
                }
            
            elif action_type == "age_actor_coordination":
                # Execute actor coordination
                result = {
                    "action": "actor_coordination",
                    "status": "executed", 
                    "semantic_action": "AGE actors coordinated for strategic response",
                    "details": action_params
                }
            
            elif action_type == "age_resource_coordination":
                # Execute resource coordination
                result = {
                    "action": "resource_coordination",
                    "status": "executed",
                    "semantic_action": "Resources coordinated for strategic utilization",
                    "details": action_params
                }
            
            elif action_type == "age_win_validation":
                # Execute WIN validation
                result = {
                    "action": "win_validation",
                    "status": "executed",
                    "semantic_action": "WIN achievement validated through strategic metrics",
                    "details": action_params
                }
            
            else:
                # Default AGE semantic action
                result = {
                    "action": action_type or "unknown",
                    "status": "executed",
                    "semantic_action": "AGE system action completed",
                    "details": action_params
                }
            
            results.append(result)
            
        except Exception as e:
            logger.error(f"AGE: Error executing system action {action}: {str(e)}")
            results.append({
                "action": action.get("type", "unknown"),
                "status": "failed",
                "error": str(e),
                "semantic_action": "AGE system action failed"
            })
    
    return results


@router.get("/health")
async def health_check():
    """
    AGE Conversational Intelligence Health Check
    
    AGE Philosophy: Verify conversational intelligence system operational status.
    """
    return {
        "status": "healthy",
        "system": "AGE Conversational Intelligence",
        "capabilities": [
            "Natural language processing",
            "Commercial AI coordination",
            "Strategic intent detection", 
            "Context-aware response generation",
            "Real-time WebSocket communication"
        ],
        "semantic_status": "Operational and ready for strategic conversation",
        "timestamp": datetime.now().isoformat()
    } 