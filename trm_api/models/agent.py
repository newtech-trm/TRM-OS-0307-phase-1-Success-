from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
import uuid

class AgentBase(BaseModel):
    name: str = Field(..., description="The unique name of the agent, e.g., 'CodeReviewerAgent'.")
    agent_type: str = Field(..., description="Type of the agent. Must be one of: InternalAgent, ExternalAgent, AIAgent, AGE.", alias="agentType")
    purpose: Optional[str] = Field(None, description="The agent's primary function or goal.")
    description: Optional[str] = Field(None, description="A brief description of the agent.")
    status: str = Field("active", description="The operational status of the agent. E.g., 'active', 'inactive', 'error', 'archived'.")
    capabilities: List[str] = Field(default_factory=list, description="List of capabilities this agent possesses.")
    
    # Fields specific to InternalAgent, including Founder
    job_title: Optional[str] = Field(None, description="Job title, applicable for InternalAgent.", alias="jobTitle")
    department: Optional[str] = Field(None, description="Department, applicable for InternalAgent.")
    is_founder: bool = Field(False, description="Indicates if the agent is a founder.", alias="isFounder")
    founder_recognition_authority: bool = Field(False, description="Indicates if the founder has recognition authority.", alias="founderRecognitionAuthority")
    contact_info: Optional[dict] = Field(None, description="Contact information for the agent.", alias="contactInfo")


    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "name": "FounderTRM",
                "agentType": "InternalAgent",
                "purpose": "To lead and define the vision for TRM.",
                "description": "The primary founder of The Recognition Machine.",
                "status": "active",
                "capabilities": ["vision_setting", "strategic_planning", "resource_allocation"],
                "jobTitle": "CEO & Founder",
                "department": "Executive",
                "isFounder": True,
                "founderRecognitionAuthority": True,
                "contactInfo": {"email": "founder@trm.com"}
            }
        }
    )

class AgentCreate(AgentBase):
    tool_ids: Optional[List[str]] = Field(default_factory=list, alias="toolIds", description="List of tool IDs this agent is equipped to use.")

class AgentUpdate(BaseModel):
    name: Optional[str] = None
    agent_type: Optional[str] = Field(None, alias="agentType")
    purpose: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    capabilities: Optional[List[str]] = None
    job_title: Optional[str] = Field(None, alias="jobTitle")
    department: Optional[str] = None
    is_founder: Optional[bool] = Field(None, alias="isFounder")
    founder_recognition_authority: Optional[bool] = Field(None, alias="founderRecognitionAuthority")
    contact_info: Optional[dict] = Field(None, alias="contactInfo")
    tool_ids: Optional[List[str]] = Field(None, alias="toolIds")

class AgentInDB(AgentBase): 
    uid: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="agentId", description="Unique ID of the agent.") 
    creation_date: datetime = Field(default_factory=datetime.utcnow, alias="creationDate", description="Timestamp of agent creation.")
    last_modified_date: Optional[datetime] = Field(default=None, alias="lastModifiedDate", description="Timestamp of last modification.")
    
    model_config = ConfigDict(
        populate_by_name=True, 
        json_schema_extra={ 
            "example": {
                "agentId": "a1b2c3d4-e5f6-7890-1234-567890abcdef", 
                "name": "FounderTRM",
                "agentType": "InternalAgent",
                "purpose": "To lead and define the vision for TRM.",
                "description": "The primary founder of The Recognition Machine.",
                "status": "active",
                "capabilities": ["vision_setting", "strategic_planning", "resource_allocation"],
                "jobTitle": "CEO & Founder",
                "department": "Executive",
                "isFounder": True,
                "founderRecognitionAuthority": True,
                "contactInfo": {"email": "founder@trm.com"},
                "creationDate": "2023-01-15T10:00:00Z",
                "lastModifiedDate": "2023-01-15T10:00:00Z"
            }
        }
    )

class Agent(AgentInDB):
    tool_ids: List[str] = Field(default_factory=list, alias="toolIds", description="List of tool IDs this agent is equipped to use.")
