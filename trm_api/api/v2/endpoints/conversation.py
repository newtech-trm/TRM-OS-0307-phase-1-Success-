"""
TRM-OS API v2 - Conversation Endpoints
Natural Language Interface với Adaptive Learning
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime
import json
import asyncio

from ....learning.adaptive_learning_system import AdaptiveLearningSystem
from ..adaptive_conversation_manager import AdaptiveConversationManager, ConversationSession
from ....core.dependencies import get_learning_system


# Request/Response Models
class ConversationRequest(BaseModel):
    """Request model for conversation analysis"""
    message: str = Field(..., description="User message to process")
    user_id: str = Field(..., description="User ID")
    session_id: Optional[str] = Field(None, description="Existing session ID")
    context: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional context")


class ConversationResponse(BaseModel):
    """Response model for conversation analysis"""
    session_id: str
    response: str
    intent: str
    confidence: float
    actions_executed: int
    success_rate: float
    processing_time: float
    suggestions: List[str] = Field(default_factory=list)


class FeedbackRequest(BaseModel):
    """Request model for user feedback"""
    session_id: str
    feedback_type: str = Field(..., description="Type of feedback (correction, satisfaction, etc.)")
    satisfaction_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    corrections: Optional[Dict[str, Any]] = Field(default_factory=dict)
    comments: Optional[str] = None


class SessionAnalyticsResponse(BaseModel):
    """Response model for session analytics"""
    session_id: str
    duration: float
    messages: int
    intents: int
    actions: int
    success_rate: float
    intent_accuracy: float
    entity_accuracy: float
    response_quality: float
    satisfaction: Optional[float]
    patterns_discovered: int
    adaptations_made: int


# Router setup
router = APIRouter(prefix="/v2/conversation", tags=["Conversation"])

# Global conversation manager (will be initialized with dependency injection)
conversation_manager: Optional[AdaptiveConversationManager] = None


async def get_conversation_manager() -> AdaptiveConversationManager:
    """Get conversation manager instance"""
    global conversation_manager
    if conversation_manager is None:
        learning_system = await get_learning_system()
        conversation_manager = AdaptiveConversationManager(learning_system)
    return conversation_manager


@router.post("/analyze", response_model=ConversationResponse)
async def analyze_conversation(
    request: ConversationRequest,
    manager: AdaptiveConversationManager = Depends(get_conversation_manager)
) -> ConversationResponse:
    """
    Analyze natural language conversation với adaptive learning
    """
    try:
        # Get or create session
        if request.session_id:
            if request.session_id not in manager.active_sessions:
                raise HTTPException(status_code=404, detail="Session not found")
            session_id = request.session_id
        else:
            session = await manager.create_learning_conversation_session(request.user_id)
            session_id = session.session_id
        
        # Process message
        result = await manager.process_conversation_message(session_id, request.message)
        
        # Get suggestions
        suggestions = await manager.get_conversation_suggestions(session_id)
        
        return ConversationResponse(
            session_id=result["session_id"],
            response=result["response"],
            intent=result["intent"],
            confidence=result["confidence"],
            actions_executed=result["actions_executed"],
            success_rate=result["success_rate"],
            processing_time=result["processing_time"],
            suggestions=suggestions
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Conversation analysis failed: {str(e)}")


@router.post("/feedback")
async def submit_feedback(
    request: FeedbackRequest,
    manager: AdaptiveConversationManager = Depends(get_conversation_manager)
) -> Dict[str, Any]:
    """
    Submit user feedback để improve conversation quality
    """
    try:
        feedback_data = {
            "type": request.feedback_type,
            "satisfaction_score": request.satisfaction_score,
            "corrections": request.corrections,
            "comments": request.comments
        }
        
        result = await manager.apply_user_feedback(request.session_id, feedback_data)
        
        return {
            "status": "success",
            "message": "Feedback processed successfully",
            "result": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Feedback processing failed: {str(e)}")


@router.get("/session/{session_id}/analytics", response_model=SessionAnalyticsResponse)
async def get_session_analytics(
    session_id: str,
    manager: AdaptiveConversationManager = Depends(get_conversation_manager)
) -> SessionAnalyticsResponse:
    """
    Get analytics for specific conversation session
    """
    try:
        analytics = await manager.get_conversation_analytics(session_id)
        
        return SessionAnalyticsResponse(
            session_id=analytics["session_id"],
            duration=analytics["duration"],
            messages=analytics["messages"],
            intents=analytics["intents"],
            actions=analytics["actions"],
            success_rate=analytics["success_rate"],
            intent_accuracy=analytics["intent_accuracy"],
            entity_accuracy=analytics["entity_accuracy"],
            response_quality=analytics["response_quality"],
            satisfaction=analytics["satisfaction"],
            patterns_discovered=analytics["patterns_discovered"],
            adaptations_made=analytics["adaptations_made"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analytics retrieval failed: {str(e)}")


@router.get("/analytics")
async def get_global_analytics(
    manager: AdaptiveConversationManager = Depends(get_conversation_manager)
) -> Dict[str, Any]:
    """
    Get global conversation analytics
    """
    try:
        analytics = await manager.get_conversation_analytics()
        
        return {
            "status": "success",
            "data": analytics
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Global analytics retrieval failed: {str(e)}")


@router.get("/session/{session_id}/suggestions")
async def get_conversation_suggestions(
    session_id: str,
    manager: AdaptiveConversationManager = Depends(get_conversation_manager)
) -> Dict[str, Any]:
    """
    Get conversation suggestions based on learned patterns
    """
    try:
        suggestions = await manager.get_conversation_suggestions(session_id)
        
        return {
            "status": "success",
            "session_id": session_id,
            "suggestions": suggestions
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Suggestions retrieval failed: {str(e)}")


@router.post("/session/{session_id}/finalize")
async def finalize_conversation_session(
    session_id: str,
    manager: AdaptiveConversationManager = Depends(get_conversation_manager)
) -> Dict[str, Any]:
    """
    Finalize conversation session và learn from outcomes
    """
    try:
        result = await manager.learn_from_conversation_outcomes(session_id)
        
        return {
            "status": "success",
            "message": "Session finalized successfully",
            "learning_results": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Session finalization failed: {str(e)}")


# WebSocket Connection Manager
class WebSocketConnectionManager:
    """Manage WebSocket connections for real-time conversations"""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.session_connections: Dict[str, str] = {}  # session_id -> connection_id
    
    async def connect(self, websocket: WebSocket, connection_id: str):
        await websocket.accept()
        self.active_connections[connection_id] = websocket
    
    def disconnect(self, connection_id: str):
        if connection_id in self.active_connections:
            del self.active_connections[connection_id]
        
        # Remove session mapping
        session_to_remove = None
        for session_id, conn_id in self.session_connections.items():
            if conn_id == connection_id:
                session_to_remove = session_id
                break
        
        if session_to_remove:
            del self.session_connections[session_to_remove]
    
    async def send_message(self, connection_id: str, message: Dict[str, Any]):
        if connection_id in self.active_connections:
            websocket = self.active_connections[connection_id]
            await websocket.send_text(json.dumps(message))
    
    def link_session(self, session_id: str, connection_id: str):
        self.session_connections[session_id] = connection_id


# WebSocket manager instance
websocket_manager = WebSocketConnectionManager()


@router.websocket("/realtime/{user_id}")
async def realtime_conversation(
    websocket: WebSocket,
    user_id: str,
    manager: AdaptiveConversationManager = Depends(get_conversation_manager)
):
    """
    WebSocket endpoint for real-time conversation
    """
    connection_id = f"{user_id}_{datetime.now().timestamp()}"
    
    await websocket_manager.connect(websocket, connection_id)
    
    # Create conversation session
    session = await manager.create_learning_conversation_session(user_id)
    websocket_manager.link_session(session.session_id, connection_id)
    
    try:
        # Send welcome message
        await websocket_manager.send_message(connection_id, {
            "type": "welcome",
            "session_id": session.session_id,
            "message": "🤖 Chào mừng bạn đến với TRM-OS! Tôi có thể giúp gì cho bạn?",
            "suggestions": await manager.get_conversation_suggestions(session.session_id)
        })
        
        while True:
            # Receive message
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            if message_data.get("type") == "message":
                # Process conversation message
                message = message_data.get("message", "")
                
                try:
                    # Process message
                    result = await manager.process_conversation_message(session.session_id, message)
                    
                    # Send response
                    await websocket_manager.send_message(connection_id, {
                        "type": "response",
                        "session_id": session.session_id,
                        "response": result["response"],
                        "intent": result["intent"],
                        "confidence": result["confidence"],
                        "actions_executed": result["actions_executed"],
                        "success_rate": result["success_rate"],
                        "processing_time": result["processing_time"],
                        "suggestions": await manager.get_conversation_suggestions(session.session_id)
                    })
                    
                except Exception as e:
                    await websocket_manager.send_message(connection_id, {
                        "type": "error",
                        "message": f"❌ Lỗi xử lý: {str(e)}"
                    })
            
            elif message_data.get("type") == "feedback":
                # Process feedback
                try:
                    feedback_data = message_data.get("feedback", {})
                    await manager.apply_user_feedback(session.session_id, feedback_data)
                    
                    await websocket_manager.send_message(connection_id, {
                        "type": "feedback_received",
                        "message": "✅ Cảm ơn feedback của bạn! Tôi sẽ học hỏi để cải thiện."
                    })
                    
                except Exception as e:
                    await websocket_manager.send_message(connection_id, {
                        "type": "error",
                        "message": f"❌ Lỗi xử lý feedback: {str(e)}"
                    })
            
            elif message_data.get("type") == "get_analytics":
                # Send analytics
                try:
                    analytics = await manager.get_conversation_analytics(session.session_id)
                    
                    await websocket_manager.send_message(connection_id, {
                        "type": "analytics",
                        "data": analytics
                    })
                    
                except Exception as e:
                    await websocket_manager.send_message(connection_id, {
                        "type": "error",
                        "message": f"❌ Lỗi lấy analytics: {str(e)}"
                    })
    
    except WebSocketDisconnect:
        # Finalize session when disconnected
        try:
            await manager.learn_from_conversation_outcomes(session.session_id)
        except Exception as e:
            print(f"Error finalizing session {session.session_id}: {e}")
    
    finally:
        websocket_manager.disconnect(connection_id)


@router.get("/health")
async def conversation_health_check():
    """Health check for conversation service"""
    return {
        "status": "healthy",
        "service": "conversation",
        "version": "2.0",
        "timestamp": datetime.now().isoformat(),
        "features": [
            "natural_language_processing",
            "adaptive_learning",
            "real_time_websocket",
            "conversation_analytics",
            "user_feedback_processing"
        ]
    } 