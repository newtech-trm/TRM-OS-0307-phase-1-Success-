from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Any, Dict
from datetime import datetime
import uuid

class TensionBase(BaseModel):
    """Base model for Tension, following Ontology V3.2 specification"""
    # Core fields required in Ontology V3.2
    title: str = Field(..., min_length=10, max_length=200, description="A concise summary of the tension.")
    description: str = Field(..., description="Detailed explanation of the tension, its context, and impact in markdown format")
    status: str = Field("Open", description="Current state: Open, InProgress, Resolved, Closed")
    priority: int = Field(0, description="The urgency level: 0-normal, 1-high, 2-critical")
    source: str = Field("FounderInput", description="Where the tension was identified: FounderInput, CustomerFeedback, DataSensingAgent")
    sourceRef: Optional[str] = Field(None, description="A reference to the original source, like an email ID or URL")
    
    # Extended properties
    tensionType: Optional[str] = Field(None, description="Type of tension: Problem, Opportunity, Risk, Conflict, Idea")
    currentState: Optional[str] = Field(None, description="Description of the current state or situation")
    desiredState: Optional[str] = Field(None, description="Description of the desired future state")
    impactAssessment: Optional[str] = Field(None, description="Assessment of the impact if the tension is not resolved")
    tags: List[str] = Field(default_factory=list, description="Tags for categorization and filtering")

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "title": "Ontology missing details for AI Agent implementation",
                "description": "The current ontology (v3.1) lacks detailed properties, relationships and constraints for core entities. This makes it difficult for AI Agents to accurately understand and automate business processes.",
                "status": "Open",
                "priority": 2,
                "source": "FounderReviewSession",
                "tensionType": "Problem",
                "currentState": "Ontology v3.1 has basic definitions but lacks metadata and concrete examples.",
                "desiredState": "Ontology v3.2 with detailed definitions, complete constraints, data types, and examples for each entity.",
                "impactAssessment": "High - Directly impacts ability to develop effective AI Agents and project timeline.",
                "tags": ["ontology", "ai-enablement", "core-system"]
            }
        }
    )

class TensionCreate(TensionBase):
    # When creating a tension, we need to know which project it belongs to or is affecting
    projectId: str = Field(..., description="The ID of the project this tension is related to")
    # Optional fields for agent associations
    reporterAgentId: Optional[str] = Field(None, description="ID of the agent reporting this tension")
    ownerAgentId: Optional[str] = Field(None, description="ID of the agent responsible for resolving this tension")

class TensionUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=10, max_length=200)
    description: Optional[str] = Field(None)
    status: Optional[str] = Field(None)
    priority: Optional[int] = Field(None)
    source: Optional[str] = Field(None)
    sourceRef: Optional[str] = Field(None)
    tensionType: Optional[str] = Field(None)
    currentState: Optional[str] = Field(None)
    desiredState: Optional[str] = Field(None)
    impactAssessment: Optional[str] = Field(None)
    tags: Optional[List[str]] = Field(None)
    resolutionDate: Optional[datetime] = Field(None)
    ownerAgentId: Optional[str] = Field(None)

    model_config = ConfigDict(populate_by_name=True)

class TensionInDB(TensionBase):
    tensionId: str = Field(default_factory=lambda: str(uuid.uuid4()))
    creationDate: datetime = Field(default_factory=datetime.utcnow)
    lastModifiedDate: datetime = Field(default_factory=datetime.utcnow)
    resolutionDate: Optional[datetime] = Field(None)

    # Properties for related entities
    reporterAgent: Optional[Dict[str, Any]] = Field(None, description="Agent who reported this tension")
    ownerAgent: Optional[Dict[str, Any]] = Field(None, description="Agent who owns this tension's resolution")
    affectedProjects: List[Dict[str, Any]] = Field(default_factory=list, description="Projects affected by this tension")
    resolvingTasks: List[Dict[str, Any]] = Field(default_factory=list, description="Tasks that resolve this tension")
    resolvingProjects: List[Dict[str, Any]] = Field(default_factory=list, description="Projects that resolve this tension")
    resultingWins: List[Dict[str, Any]] = Field(default_factory=list, description="WINs resulting from resolving this tension")
    
    model_config = ConfigDict(populate_by_name=True)

class Tension(TensionInDB):
    """Complete Tension model with all properties and relationships"""
    pass
