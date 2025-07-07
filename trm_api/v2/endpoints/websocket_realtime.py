"""
TRM-OS WebSocket Real-time Communication
========================================

Real-time WebSocket endpoints cho conversational interface
với ML-enhanced reasoning integration
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
from fastapi.security import HTTPBearer
from typing import Dict, List, Any, Optional
import asyncio
import json
import logging
from datetime import datetime
from uuid import uuid4

from trm_api.v2.conversation.nlp_processor import ConversationProcessor
from trm_api.v2.conversation.session_manager import ConversationSessionManager
from trm_api.v2.conversation.response_generator import NaturalResponseGenerator, ResponseContext
from trm_api.reasoning.ml_enhanced_reasoning_engine import MLEnhancedReasoningEngine
from trm_api.reasoning.reasoning_types import ReasoningContext, ReasoningType
from trm_api.learning.adaptive_learning_system import AdaptiveLearningSystem
from trm_api.quantum.quantum_system_manager import QuantumSystemManager
from trm_api.reasoning.advanced_reasoning_engine import AdvancedReasoningEngine

router = APIRouter(prefix="/api/v2/realtime", tags=["Real-time Communication"])
security = HTTPBearer()
logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manages WebSocket connections"""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.user_sessions: Dict[str, str] = {}  # user_id -> session_id
        self.session_connections: Dict[str, List[str]] = {}  # session_id -> [connection_ids]
        
    async def connect(self, websocket: WebSocket, connection_id: str, user_id: str) -> None:
        """Accept WebSocket connection"""
        await websocket.accept()
        self.active_connections[connection_id] = websocket
        self.user_sessions[user_id] = connection_id
        logger.info(f"WebSocket connected: {connection_id} for user {user_id}")
        
    def disconnect(self, connection_id: str) -> None:
        """Remove WebSocket connection"""
        if connection_id in self.active_connections:
            del self.active_connections[connection_id]
            
        # Remove from user sessions
        user_to_remove = None
        for user_id, conn_id in self.user_sessions.items():
            if conn_id == connection_id:
                user_to_remove = user_id
                break
        if user_to_remove:
            del self.user_sessions[user_to_remove]
            
        logger.info(f"WebSocket disconnected: {connection_id}")
        
    async def send_personal_message(self, message: str, connection_id: str) -> None:
        """Send message to specific connection"""
        if connection_id in self.active_connections:
            websocket = self.active_connections[connection_id]
            await websocket.send_text(message)
            
    async def send_json_message(self, data: Dict[str, Any], connection_id: str) -> None:
        """Send JSON message to specific connection"""
        if connection_id in self.active_connections:
            websocket = self.active_connections[connection_id]
            await websocket.send_json(data)
            
    async def broadcast_to_session(self, message: str, session_id: str) -> None:
        """Broadcast message to all connections in session"""
        if session_id in self.session_connections:
            for connection_id in self.session_connections[session_id]:
                await self.send_personal_message(message, connection_id)


# Global connection manager
manager = ConnectionManager()

# Global components (initialized on startup)
nlp_processor: Optional[ConversationProcessor] = None
session_manager: Optional[ConversationSessionManager] = None
response_generator: Optional[NaturalResponseGenerator] = None
ml_reasoning_engine: Optional[MLEnhancedReasoningEngine] = None


async def initialize_realtime_components():
    """Initialize real-time communication components"""
    global nlp_processor, session_manager, response_generator, ml_reasoning_engine
    
    try:
        # Initialize conversation components
        nlp_processor = ConversationProcessor(agent_id="realtime_websocket")
        session_manager = ConversationSessionManager()
        response_generator = NaturalResponseGenerator()
        
        # Initialize ML reasoning components
        learning_system = AdaptiveLearningSystem(agent_id="realtime_ml")
        quantum_manager = QuantumSystemManager(learning_system=learning_system)
        advanced_reasoning = AdvancedReasoningEngine(agent_id="realtime_reasoning")
        
        ml_reasoning_engine = MLEnhancedReasoningEngine(
            learning_system=learning_system,
            quantum_manager=quantum_manager,
            advanced_reasoning=advanced_reasoning
        )
        
        logger.info("Real-time components initialized successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize real-time components: {e}")
        raise


@router.websocket("/chat/{user_id}")
async def websocket_chat_endpoint(websocket: WebSocket, user_id: str):
    """
    WebSocket endpoint cho real-time chat
    """
    connection_id = str(uuid4())
    
    try:
        # Initialize components if not already done
        if nlp_processor is None:
            await initialize_realtime_components()
            
        # Accept connection
        await manager.connect(websocket, connection_id, user_id)
        
        # Create or get existing session
        session = await session_manager.create_conversation_session(
            user_id=user_id,
            metadata={"connection_type": "websocket", "connection_id": connection_id}
        )
        
        # Send welcome message
        welcome_message = {
            "type": "system",
            "message": "Connected to TRM-OS Real-time Intelligence",
            "session_id": session.session_id,
            "timestamp": datetime.now().isoformat(),
            "capabilities": [
                "Vietnamese/English conversation",
                "ML-enhanced reasoning",
                "Real-time response generation",
                "Context-aware interactions"
            ]
        }
        await manager.send_json_message(welcome_message, connection_id)
        
        # Main message loop
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            
            try:
                # Parse message
                message_data = json.loads(data)
                user_message = message_data.get("message", "")
                language = message_data.get("language", "auto")
                enable_ml_reasoning = message_data.get("ml_reasoning", True)
                
                if not user_message.strip():
                    continue
                
                # Send typing indicator
                typing_message = {
                    "type": "typing",
                    "message": "TRM-OS đang xử lý...",
                    "timestamp": datetime.now().isoformat()
                }
                await manager.send_json_message(typing_message, connection_id)
                
                # Process message with timing
                start_time = datetime.now()
                
                # Parse natural language
                parsed_intent = await nlp_processor.parse_natural_language_query(user_message)
                
                # Extract entities and context
                entity_context = await nlp_processor.extract_entities_and_context(parsed_intent)
                
                # Update conversation context
                conversation_context = await session_manager.maintain_conversation_context(
                    session.session_id, user_message, parsed_intent
                )
                
                # ML reasoning enhancement (if enabled)
                ml_insights = {}
                if enable_ml_reasoning and ml_reasoning_engine:
                    try:
                        # Create reasoning context
                        reasoning_context = ReasoningContext(
                            context_id=f"realtime_{session.session_id}",
                            domain="conversational_ai",
                            constraints={"real_time": True},
                            objectives=["provide_helpful_response"],
                            available_resources={"websocket": True},
                            priority_level=conversation_context.turn_count,
                            risk_tolerance=0.7
                        )
                        
                        # Perform ML reasoning
                        reasoning_result = await ml_reasoning_engine.reason(
                            query=user_message,
                            context=reasoning_context,
                            reasoning_type=ReasoningType.HYBRID
                        )
                        
                        if reasoning_result:
                            ml_insights = {
                                "reasoning_type": reasoning_result.reasoning_type.value,
                                "confidence": reasoning_result.confidence,
                                "ml_confidence": getattr(reasoning_result, 'ml_confidence', 0.0),
                                "quantum_enhancement": getattr(reasoning_result, 'quantum_enhancement', 0.0),
                                "conclusion": reasoning_result.conclusion
                            }
                            
                    except Exception as e:
                        logger.warning(f"ML reasoning failed: {e}")
                        ml_insights = {"error": "ML reasoning unavailable"}
                
                # Generate response
                response_context = ResponseContext(
                    intent=parsed_intent,
                    conversation_context=conversation_context,
                    action_results=[],
                    suggestions=[],
                    ml_insights=ml_insights
                )
                
                generated_response = await response_generator.generate_natural_language_response(response_context)
                
                # Calculate processing time
                processing_time = (datetime.now() - start_time).total_seconds()
                
                # Add conversation turn
                await session_manager.add_conversation_turn(
                    session.session_id,
                    user_message,
                    parsed_intent,
                    [],  # system_actions
                    generated_response.text,
                    processing_time
                )
                
                # Send response to client
                response_message = {
                    "type": "response",
                    "message": generated_response.text,
                    "response_type": generated_response.response_type.value,
                    "confidence": generated_response.confidence,
                    "processing_time": processing_time,
                    "timestamp": datetime.now().isoformat(),
                    "intent_detected": {
                        "type": parsed_intent.intent_type.value,
                        "confidence": parsed_intent.confidence
                    },
                    "entities_found": len(entity_context.entities),
                    "turn_count": conversation_context.turn_count,
                    "ml_insights": ml_insights if ml_insights else None
                }
                
                await manager.send_json_message(response_message, connection_id)
                
                # Send suggestions if available
                if generated_response.suggestions:
                    suggestions_message = {
                        "type": "suggestions",
                        "suggestions": generated_response.suggestions,
                        "timestamp": datetime.now().isoformat()
                    }
                    await manager.send_json_message(suggestions_message, connection_id)
                
            except json.JSONDecodeError:
                # Handle plain text messages
                error_message = {
                    "type": "error",
                    "message": "Please send messages in JSON format: {\"message\": \"your text\"}",
                    "timestamp": datetime.now().isoformat()
                }
                await manager.send_json_message(error_message, connection_id)
                
            except Exception as e:
                logger.error(f"Error processing message: {e}")
                error_message = {
                    "type": "error",
                    "message": f"Error processing message: {str(e)}",
                    "timestamp": datetime.now().isoformat()
                }
                await manager.send_json_message(error_message, connection_id)
                
    except WebSocketDisconnect:
        manager.disconnect(connection_id)
        logger.info(f"WebSocket disconnected: {connection_id}")
        
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(connection_id)


@router.websocket("/system/{system_channel}")
async def websocket_system_channel(websocket: WebSocket, system_channel: str):
    """
    WebSocket endpoint cho system-level real-time updates
    """
    connection_id = str(uuid4())
    
    try:
        await manager.connect(websocket, connection_id, f"system_{system_channel}")
        
        # Send system status
        system_status = {
            "type": "system_status",
            "channel": system_channel,
            "status": "connected",
            "timestamp": datetime.now().isoformat(),
            "capabilities": [
                "Real-time system monitoring",
                "ML reasoning updates",
                "Performance metrics",
                "System health status"
            ]
        }
        await manager.send_json_message(system_status, connection_id)
        
        # Keep connection alive with periodic updates
        while True:
            await asyncio.sleep(30)  # Send update every 30 seconds
            
            health_update = {
                "type": "health_update",
                "timestamp": datetime.now().isoformat(),
                "active_connections": len(manager.active_connections),
                "system_status": "operational"
            }
            await manager.send_json_message(health_update, connection_id)
            
    except WebSocketDisconnect:
        manager.disconnect(connection_id)
        
    except Exception as e:
        logger.error(f"System WebSocket error: {e}")
        manager.disconnect(connection_id)


@router.get("/connections/status")
async def get_connection_status():
    """Get current WebSocket connection status"""
    return {
        "active_connections": len(manager.active_connections),
        "user_sessions": len(manager.user_sessions),
        "connection_ids": list(manager.active_connections.keys()),
        "timestamp": datetime.now().isoformat()
    }


@router.post("/broadcast/{session_id}")
async def broadcast_message(session_id: str, message: Dict[str, Any]):
    """Broadcast message to all connections in a session"""
    try:
        message_text = json.dumps(message)
        await manager.broadcast_to_session(message_text, session_id)
        return {"status": "broadcast_sent", "session_id": session_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Startup event để initialize components
@router.on_event("startup")
async def startup_event():
    """Initialize real-time components on startup"""
    await initialize_realtime_components() 