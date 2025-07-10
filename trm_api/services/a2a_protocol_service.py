"""
A2A (Agent2Agent) Protocol Service

Enables secure, vendor-agnostic communication between AI agents:
- Cross-platform agent discovery
- Secure agent-to-agent messaging
- Task delegation and coordination
- Agent capability negotiation
- Authentication and authorization

Based on Google's A2A Protocol standard for agent interoperability.
"""

from typing import Dict, Any, List, Optional, Union
from abc import ABC, abstractmethod
from datetime import datetime
import logging
import asyncio
import json
import uuid
from enum import Enum
from dataclasses import dataclass
from .adk_orchestration_service import get_adk_orchestrator, AgentTask, AgentResult

logger = logging.getLogger(__name__)


class A2AMessageType(str, Enum):
    """A2A message types"""
    TASK_REQUEST = "task_request"
    TASK_RESPONSE = "task_response"
    CAPABILITY_INQUIRY = "capability_inquiry"
    CAPABILITY_RESPONSE = "capability_response"
    AGENT_DISCOVERY = "agent_discovery"
    AGENT_ANNOUNCEMENT = "agent_announcement"
    STATUS_UPDATE = "status_update"
    ERROR_NOTIFICATION = "error_notification"


class A2AContentType(str, Enum):
    """A2A content types for multimodal communication"""
    TEXT = "text/plain"
    JSON = "application/json"
    IMAGE = "image/png"
    AUDIO = "audio/wav"
    VIDEO = "video/mp4"
    FORM = "application/x-www-form-urlencoded"


@dataclass
class A2AMessagePart:
    """Part of A2A message supporting multimodal content"""
    content_type: A2AContentType
    content: Union[str, Dict[str, Any], bytes]
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class A2AMessage:
    """A2A protocol message"""
    message_id: str
    sender_agent_id: str
    recipient_agent_id: str
    message_type: A2AMessageType
    parts: List[A2AMessagePart]
    correlation_id: Optional[str] = None
    timestamp: Optional[datetime] = None
    ttl_seconds: int = 300
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
        if self.message_id is None:
            self.message_id = str(uuid.uuid4())


@dataclass
class AgentCard:
    """Agent capability card for A2A discovery"""
    agent_id: str
    name: str
    description: str
    endpoint_url: str
    capabilities: List[str]
    supported_content_types: List[A2AContentType]
    authentication_schemes: List[str]
    version: str = "1.0"
    is_available: bool = True
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "description": self.description,
            "endpoint_url": self.endpoint_url,
            "capabilities": self.capabilities,
            "supported_content_types": [ct.value for ct in self.supported_content_types],
            "authentication_schemes": self.authentication_schemes,
            "version": self.version,
            "is_available": self.is_available,
            "metadata": self.metadata
        }


class A2AAuthenticator:
    """Handles A2A authentication and authorization"""
    
    def __init__(self):
        self.trusted_agents: Dict[str, AgentCard] = {}
        self.api_keys: Dict[str, str] = {}
    
    async def authenticate_agent(self, agent_id: str, credentials: Dict[str, Any]) -> bool:
        """Authenticate incoming agent request"""
        try:
            # Simple API key authentication for now
            if "api_key" in credentials:
                return credentials["api_key"] in self.api_keys.values()
            
            # Could extend with OAuth, JWT, etc.
            return agent_id in self.trusted_agents
            
        except Exception as e:
            logger.error(f"Authentication failed for agent {agent_id}: {e}")
            return False
    
    async def authorize_action(
        self, 
        agent_id: str, 
        action: str, 
        resource: str
    ) -> bool:
        """Authorize agent action on resource"""
        # Simple role-based authorization
        if agent_id not in self.trusted_agents:
            return False
        
        agent_card = self.trusted_agents[agent_id]
        
        # Check if agent has required capability for action
        required_capabilities = {
            "execute_task": ["task_execution", "general_purpose"],
            "query_data": ["data_access", "query_execution"],
            "coordinate_agents": ["agent_coordination", "workflow_management"]
        }
        
        if action in required_capabilities:
            agent_capabilities = agent_card.capabilities
            return any(cap in agent_capabilities for cap in required_capabilities[action])
        
        return True  # Default allow for unknown actions
    
    def register_trusted_agent(self, agent_card: AgentCard, api_key: str):
        """Register trusted agent for future communications"""
        self.trusted_agents[agent_card.agent_id] = agent_card
        self.api_keys[agent_card.agent_id] = api_key


class A2AMessageBroker:
    """Handles A2A message routing and delivery"""
    
    def __init__(self):
        self.message_queue: Dict[str, List[A2AMessage]] = {}
        self.agent_registry: Dict[str, AgentCard] = {}
        self.authenticator = A2AAuthenticator()
    
    async def register_agent(self, agent_card: AgentCard, api_key: str):
        """Register agent for A2A communication"""
        self.agent_registry[agent_card.agent_id] = agent_card
        self.authenticator.register_trusted_agent(agent_card, api_key)
        
        if agent_card.agent_id not in self.message_queue:
            self.message_queue[agent_card.agent_id] = []
        
        logger.info(f"Registered A2A agent: {agent_card.name} ({agent_card.agent_id})")
    
    async def send_message(
        self, 
        message: A2AMessage, 
        sender_credentials: Dict[str, Any]
    ) -> bool:
        """Send A2A message between agents"""
        try:
            # Authenticate sender
            if not await self.authenticator.authenticate_agent(
                message.sender_agent_id, 
                sender_credentials
            ):
                logger.warning(f"Authentication failed for sender: {message.sender_agent_id}")
                return False
            
            # Check if recipient exists
            if message.recipient_agent_id not in self.agent_registry:
                logger.warning(f"Recipient agent not found: {message.recipient_agent_id}")
                return False
            
            # Authorize message sending
            if not await self.authenticator.authorize_action(
                message.sender_agent_id,
                "send_message",
                message.recipient_agent_id
            ):
                logger.warning(f"Authorization failed for message from {message.sender_agent_id}")
                return False
            
            # Queue message for recipient
            self.message_queue[message.recipient_agent_id].append(message)
            
            logger.info(f"A2A message sent: {message.sender_agent_id} -> {message.recipient_agent_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send A2A message: {e}")
            return False
    
    async def receive_messages(self, agent_id: str) -> List[A2AMessage]:
        """Receive pending messages for agent"""
        if agent_id in self.message_queue:
            messages = self.message_queue[agent_id].copy()
            self.message_queue[agent_id].clear()
            return messages
        return []
    
    async def discover_agents(self, capabilities: Optional[List[str]] = None) -> List[AgentCard]:
        """Discover available agents with optional capability filtering"""
        available_agents = [
            agent for agent in self.agent_registry.values() 
            if agent.is_available
        ]
        
        if capabilities:
            # Filter by capabilities
            filtered_agents = []
            for agent in available_agents:
                if any(cap in agent.capabilities for cap in capabilities):
                    filtered_agents.append(agent)
            return filtered_agents
        
        return available_agents


class A2ATaskDelegator:
    """Handles task delegation via A2A protocol"""
    
    def __init__(self, message_broker: A2AMessageBroker):
        self.message_broker = message_broker
        self.pending_tasks: Dict[str, AgentTask] = {}
    
    async def delegate_task(
        self,
        task: AgentTask,
        target_agent_id: str,
        sender_agent_id: str,
        sender_credentials: Dict[str, Any]
    ) -> str:
        """Delegate task to remote agent via A2A"""
        
        # Create A2A task request message
        task_message = A2AMessage(
            message_id=str(uuid.uuid4()),
            sender_agent_id=sender_agent_id,
            recipient_agent_id=target_agent_id,
            message_type=A2AMessageType.TASK_REQUEST,
            parts=[
                A2AMessagePart(
                    content_type=A2AContentType.JSON,
                    content={
                        "task_id": task.task_id,
                        "description": task.description,
                        "context": task.context,
                        "requirements": task.requirements,
                        "expected_output": task.expected_output,
                        "priority": task.priority,
                        "timeout_seconds": task.timeout_seconds
                    }
                )
            ],
            correlation_id=task.task_id
        )
        
        # Send message
        success = await self.message_broker.send_message(task_message, sender_credentials)
        
        if success:
            self.pending_tasks[task.task_id] = task
            logger.info(f"Task {task.task_id} delegated to agent {target_agent_id}")
            return task_message.message_id
        else:
            raise Exception(f"Failed to delegate task to agent {target_agent_id}")
    
    async def handle_task_request(
        self,
        message: A2AMessage,
        local_agent_id: str
    ) -> A2AMessage:
        """Handle incoming task request from remote agent"""
        
        try:
            # Extract task from message
            task_data = message.parts[0].content
            
            # Create AgentTask from A2A message
            task = AgentTask(
                task_id=task_data["task_id"],
                description=task_data["description"],
                context=task_data["context"],
                requirements=task_data["requirements"],
                expected_output=task_data["expected_output"],
                priority=task_data.get("priority", 1),
                timeout_seconds=task_data.get("timeout_seconds", 300)
            )
            
            # Execute task using local ADK orchestrator
            orchestrator = await get_adk_orchestrator()
            results = await orchestrator.execute_sequential_workflow([task], f"a2a-{message.message_id}")
            
            # Create response message
            response = A2AMessage(
                message_id=str(uuid.uuid4()),
                sender_agent_id=local_agent_id,
                recipient_agent_id=message.sender_agent_id,
                message_type=A2AMessageType.TASK_RESPONSE,
                parts=[
                    A2AMessagePart(
                        content_type=A2AContentType.JSON,
                        content={
                            "task_id": task.task_id,
                            "status": results[0].status if results else "failed",
                            "output": results[0].output if results else {"error": "No results"},
                            "execution_time_seconds": results[0].execution_time_seconds if results else 0.0
                        }
                    )
                ],
                correlation_id=message.correlation_id
            )
            
            return response
            
        except Exception as e:
            logger.error(f"Failed to handle task request: {e}")
            
            # Return error response
            return A2AMessage(
                message_id=str(uuid.uuid4()),
                sender_agent_id=local_agent_id,
                recipient_agent_id=message.sender_agent_id,
                message_type=A2AMessageType.ERROR_NOTIFICATION,
                parts=[
                    A2AMessagePart(
                        content_type=A2AContentType.JSON,
                        content={
                            "error": str(e),
                            "original_task_id": message.correlation_id
                        }
                    )
                ],
                correlation_id=message.correlation_id
            )


class A2AProtocolService:
    """Main A2A protocol service"""
    
    def __init__(self):
        self.message_broker = A2AMessageBroker()
        self.task_delegator = A2ATaskDelegator(self.message_broker)
        self.local_agent_id = "trm-os-agent"
        self._setup_local_agent()
    
    def _setup_local_agent(self):
        """Setup local TRM-OS agent for A2A communication"""
        local_agent_card = AgentCard(
            agent_id=self.local_agent_id,
            name="TRM-OS Commercial AI Agent",
            description="TRM-OS agent providing commercial AI coordination and data access",
            endpoint_url="https://trmosngonlanh.up.railway.app/api/v1/a2a",
            capabilities=[
                "commercial_ai_coordination",
                "data_analysis", 
                "knowledge_extraction",
                "strategic_planning",
                "multi_source_synthesis"
            ],
            supported_content_types=[
                A2AContentType.TEXT,
                A2AContentType.JSON,
                A2AContentType.IMAGE
            ],
            authentication_schemes=["api_key", "bearer_token"],
            metadata={
                "platform": "TRM-OS",
                "version": "2.0",
                "commercial_ai_providers": ["openai", "claude", "gemini"]
            }
        )
        
        # Register with self (for local routing)
        asyncio.create_task(
            self.message_broker.register_agent(local_agent_card, "trm-os-api-key")
        )
    
    async def register_external_agent(self, agent_card: AgentCard, api_key: str):
        """Register external agent for A2A communication"""
        await self.message_broker.register_agent(agent_card, api_key)
    
    async def send_message_to_agent(
        self,
        recipient_agent_id: str,
        message_type: A2AMessageType,
        content: Dict[str, Any],
        sender_credentials: Dict[str, Any]
    ) -> bool:
        """Send message to external agent"""
        message = A2AMessage(
            message_id=str(uuid.uuid4()),
            sender_agent_id=self.local_agent_id,
            recipient_agent_id=recipient_agent_id,
            message_type=message_type,
            parts=[
                A2AMessagePart(
                    content_type=A2AContentType.JSON,
                    content=content
                )
            ]
        )
        
        return await self.message_broker.send_message(message, sender_credentials)
    
    async def discover_available_agents(self, capabilities: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """Discover available agents"""
        agents = await self.message_broker.discover_agents(capabilities)
        return [agent.to_dict() for agent in agents]
    
    async def delegate_task_to_agent(
        self,
        task: AgentTask,
        target_agent_id: str,
        sender_credentials: Dict[str, Any]
    ) -> str:
        """Delegate task to external agent"""
        return await self.task_delegator.delegate_task(
            task, target_agent_id, self.local_agent_id, sender_credentials
        )
    
    async def process_incoming_message(self, message: A2AMessage) -> Optional[A2AMessage]:
        """Process incoming A2A message"""
        if message.message_type == A2AMessageType.TASK_REQUEST:
            return await self.task_delegator.handle_task_request(message, self.local_agent_id)
        elif message.message_type == A2AMessageType.CAPABILITY_INQUIRY:
            # Return capability response
            orchestrator = await get_adk_orchestrator()
            agents = orchestrator.list_agents()
            
            return A2AMessage(
                message_id=str(uuid.uuid4()),
                sender_agent_id=self.local_agent_id,
                recipient_agent_id=message.sender_agent_id,
                message_type=A2AMessageType.CAPABILITY_RESPONSE,
                parts=[
                    A2AMessagePart(
                        content_type=A2AContentType.JSON,
                        content={"agents": agents}
                    )
                ],
                correlation_id=message.correlation_id
            )
        
        return None
    
    def get_local_agent_card(self) -> Dict[str, Any]:
        """Get local agent card for publishing"""
        if self.local_agent_id in self.message_broker.agent_registry:
            return self.message_broker.agent_registry[self.local_agent_id].to_dict()
        return {}


# Global A2A service instance  
a2a_service = A2AProtocolService()


async def get_a2a_service() -> A2AProtocolService:
    """Get A2A protocol service instance for dependency injection"""
    return a2a_service 