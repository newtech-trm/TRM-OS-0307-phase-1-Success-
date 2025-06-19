from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid

class KnowledgeSnippetBase(BaseModel):
    content: str = Field(..., description="The actual piece of knowledge, which could be text, code, or a structured description.")
    snippet_type: str = Field(..., alias="snippetType", description="The type of snippet, e.g., 'HowToGuide', 'CodeExample', 'BestPractice', 'Troubleshooting'.")
    source_entity_id: Optional[str] = Field(None, alias="sourceEntityId", description="The ID of the entity (e.g., Task, Tension) from which this knowledge was derived.")
    tags: Optional[List[str]] = Field(None, description="Keywords or tags to make the snippet easily searchable.")

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "content": "To connect to the production database, always use the read-only replica endpoint and wrap the connection in a 'with' statement to ensure it's closed properly.",
                "snippetType": "BestPractice",
                "sourceEntityId": "task_id_xyz_789",
                "tags": ["database", "connection", "python", "best-practice"]
            }
        }
    )

class KnowledgeSnippetCreate(KnowledgeSnippetBase):
    pass

class KnowledgeSnippetUpdate(BaseModel):
    content: Optional[str] = None
    snippet_type: Optional[str] = Field(None, alias="snippetType")
    tags: Optional[List[str]] = None

class KnowledgeSnippetInDB(KnowledgeSnippetBase):
    uid: str = Field(default_factory=lambda: str(uuid.uuid4()))
    snippet_id: Optional[str] = Field(alias="snippetId", default=None, description="Legacy ID field, maintained for backward compatibility")
    created_at: datetime = Field(alias="createdAt", default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(alias="updatedAt", default=None)
    version: int = Field(1, description="Version number, incremented on each update.")

class KnowledgeSnippet(KnowledgeSnippetInDB):
    pass
