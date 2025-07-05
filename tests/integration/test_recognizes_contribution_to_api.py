import pytest
import pytest_asyncio
import uuid
from unittest.mock import patch, MagicMock
from datetime import datetime
import httpx
from fastapi import status
from httpx import AsyncClient, ASGITransport

from trm_api.main import app
from trm_api.models.relationships import Relationship, RelationshipType, TargetEntityTypeEnum
from trm_api.api.v1.endpoints.relationship import ContributionTargetTypeEnum


class TestRecognizesContributionToAPI:
    """Integration tests for the RECOGNIZES_CONTRIBUTION_TO relationship API endpoints."""

    @pytest_asyncio.fixture(autouse=True)
    async def setup_method(self):
        """Setup test fixtures before each test method."""
        # Sample IDs for testing
        self.recognition_id = str(uuid.uuid4())
        self.project_id = str(uuid.uuid4())
        self.task_id = str(uuid.uuid4())
        self.resource_id = str(uuid.uuid4())
        
        # Sample relationships data
        self.recognition_project_relationship = {
            "source_id": self.recognition_id,
            "source_type": "Recognition",
            "target_id": self.project_id,
            "target_type": "Project",
            "type": "RECOGNIZES_CONTRIBUTION_TO",
            "relationshipId": f"recognizes_contribution_{self.recognition_id}_{self.project_id}_abcd1234",
            "contribution_type": "Leadership",
            "contribution_level": "High",
            "impact_notes": "Significant leadership of the project",
            "createdAt": datetime.now()
        }
        
        self.recognition_task_relationship = {
            "source_id": self.recognition_id,
            "source_type": "Recognition",
            "target_id": self.task_id,
            "target_type": "Task",
            "type": "RECOGNIZES_CONTRIBUTION_TO",
            "relationshipId": f"recognizes_contribution_{self.recognition_id}_{self.task_id}_abcd1234",
            "contribution_type": "Technical",
            "contribution_level": "Medium",
            "impact_notes": "Valuable technical contribution",
            "createdAt": datetime.now()
        }
        
        self.recognition_resource_relationship = {
            "source_id": self.recognition_id,
            "source_type": "Recognition",
            "target_id": self.resource_id,
            "target_type": "Resource",
            "type": "RECOGNIZES_CONTRIBUTION_TO",
            "relationshipId": f"recognizes_contribution_{self.recognition_id}_{self.resource_id}_abcd1234",
            "contribution_type": "Documentation",
            "contribution_level": "Medium",
            "impact_notes": "Created useful documentation",
            "createdAt": datetime.now()
        }
        
        # Sample request data
        self.contribution_request = {
            "contribution_type": "Leadership",
            "contribution_level": "High",
            "impact_notes": "Significant leadership of the project"
        }
        
        # Set up async client
        self.client = AsyncClient(transport=ASGITransport(app=app), base_url="http://test")
    
    @pytest.mark.asyncio
    @patch("trm_api.api.v1.endpoints.relationship.relationship_service")
    async def test_create_recognizes_contribution_to_project(self, mock_service):
        """Test creating a RECOGNIZES_CONTRIBUTION_TO relationship from Recognition to Project."""
        # Set up mock
        mock_service.create_relationship.return_value = Relationship(**self.recognition_project_relationship)
        
        # Call API với async client
        response = await self.client.post(
            f"/api/v1/relationships/recognizes-contribution-to?recognition_id={self.recognition_id}&target_id={self.project_id}&target_type=Project",
            json=self.contribution_request
        )
        
        # Assertions
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["source_id"] == self.recognition_id
        assert data["source_type"] == "Recognition"
        assert data["target_id"] == self.project_id
        assert data["target_type"] == "Project"
        assert data["type"] == "RECOGNIZES_CONTRIBUTION_TO"
        
        # Verify service was called correctly
        mock_service.create_relationship.assert_called_once()
    
    @pytest.mark.asyncio
    @patch("trm_api.api.v1.endpoints.relationship.relationship_service")
    async def test_create_recognizes_contribution_to_task(self, mock_service):
        """Test creating a RECOGNIZES_CONTRIBUTION_TO relationship from Recognition to Task."""
        # Set up mock
        mock_service.create_relationship.return_value = Relationship(**self.recognition_task_relationship)
        
        # Call API với async client
        response = await self.client.post(
            f"/api/v1/relationships/recognizes-contribution-to?recognition_id={self.recognition_id}&target_id={self.task_id}&target_type=Task",
            json=self.contribution_request
        )
        
        # Assertions
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["source_id"] == self.recognition_id
        assert data["target_id"] == self.task_id
        assert data["target_type"] == "Task"
        
        # Verify service was called correctly
        mock_service.create_relationship.assert_called_once()
    
    @pytest.mark.asyncio
    @patch("trm_api.api.v1.endpoints.relationship.relationship_service")
    async def test_create_recognizes_contribution_to_resource(self, mock_service):
        """Test creating a RECOGNIZES_CONTRIBUTION_TO relationship from Recognition to Resource."""
        # Set up mock
        mock_service.create_relationship.return_value = Relationship(**self.recognition_resource_relationship)
        
        # Call API
        response = await self.client.post(
            f"/api/v1/relationships/recognizes-contribution-to?recognition_id={self.recognition_id}&target_id={self.resource_id}&target_type=Resource",
            json=self.contribution_request
        )
        
        # Assertions
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["source_id"] == self.recognition_id
        assert data["target_id"] == self.resource_id
        assert data["target_type"] == "Resource"
        
        # Verify service was called correctly
        mock_service.create_relationship.assert_called_once()
    
    @pytest.mark.asyncio
    @patch("trm_api.api.v1.endpoints.relationship.relationship_service")
    async def test_create_recognizes_contribution_to_invalid_type(self, mock_service):
        """Test creating a RECOGNIZES_CONTRIBUTION_TO relationship with invalid target type."""
        # Call API with invalid target type
        response = await self.client.post(
            f"/api/v1/relationships/recognizes-contribution-to?recognition_id={self.recognition_id}&target_id={self.project_id}&target_type=InvalidType",
            json=self.contribution_request
        )
        
        # Assertions - should fail with 422 validation error (enum validation)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
        # Verify service was NOT called
        mock_service.create_relationship.assert_not_called()
    
    @pytest.mark.asyncio
    @patch("trm_api.api.v1.endpoints.relationship.relationship_service")
    async def test_create_recognizes_contribution_to_entity_not_found(self, mock_service):
        """Test creating a RECOGNIZES_CONTRIBUTION_TO relationship when entities don't exist."""
        # Set up mock
        mock_service.create_relationship.return_value = None
        
        # Call API
        response = await self.client.post(
            f"/api/v1/relationships/recognizes-contribution-to?recognition_id={self.recognition_id}&target_id={self.project_id}&target_type=Project",
            json=self.contribution_request
        )
        
        # Assertions
        assert response.status_code == status.HTTP_404_NOT_FOUND
        
        # Verify service was called correctly
        mock_service.create_relationship.assert_called_once()
    
    @pytest.mark.asyncio
    @patch("trm_api.api.v1.endpoints.relationship.relationship_service")
    async def test_get_contributions_recognized_by_recognition(self, mock_service):
        """Test getting all entities that a Recognition recognizes contributions to."""
        # Set up mock
        mock_service.get_relationships.return_value = [
            Relationship(**self.recognition_project_relationship),
            Relationship(**self.recognition_task_relationship),
            Relationship(**self.recognition_resource_relationship)
        ]
        
        # Call API
        response = await self.client.get(f"/api/v1/relationships/recognitions/{self.recognition_id}/recognizes-contributions")
        
        # Assertions
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 3
        assert any(rel["target_id"] == self.project_id and rel["target_type"] == "Project" for rel in data)
        assert any(rel["target_id"] == self.task_id and rel["target_type"] == "Task" for rel in data)
        assert any(rel["target_id"] == self.resource_id and rel["target_type"] == "Resource" for rel in data)
        
        # Verify service was called correctly
        mock_service.get_relationships.assert_called_once()
    
    @pytest.mark.asyncio
    @patch("trm_api.api.v1.endpoints.relationship.relationship_service")
    async def test_get_contributions_recognized_by_recognition_filtered(self, mock_service):
        """Test getting entities of a specific type that a Recognition recognizes contributions to."""
        # Set up mock
        mock_service.get_relationships.return_value = [Relationship(**self.recognition_project_relationship)]
        
        # Call API with target type filter
        response = await self.client.get(
            f"/api/v1/relationships/recognitions/{self.recognition_id}/recognizes-contributions?target_type=Project"
        )
        
        # Assertions
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["target_id"] == self.project_id
        assert data[0]["target_type"] == "Project"
        
        # Verify service was called correctly
        mock_service.get_relationships.assert_called_once()
    
    @pytest.mark.asyncio
    @patch("trm_api.api.v1.endpoints.relationship.relationship_service")
    async def test_get_recognitions_for_project_contribution(self, mock_service):
        """Test getting Recognitions that recognize contributions to a Project."""
        # Set up mock
        mock_service.get_relationships.return_value = [Relationship(**self.recognition_project_relationship)]
        
        # Call API
        response = await self.client.get(f"/api/v1/relationships/projects/{self.project_id}/recognized-contributions")
        
        # Assertions
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["source_id"] == self.recognition_id
        assert data[0]["target_id"] == self.project_id
        assert data[0]["type"] == "RECOGNIZES_CONTRIBUTION_TO"
        
        # Verify service was called correctly
        mock_service.get_relationships.assert_called_once()
    
    @pytest.mark.asyncio
    @patch("trm_api.api.v1.endpoints.relationship.relationship_service")
    async def test_get_recognitions_for_task_contribution(self, mock_service):
        """Test getting Recognitions that recognize contributions to a Task."""
        # Set up mock
        mock_service.get_relationships.return_value = [Relationship(**self.recognition_task_relationship)]
        
        # Call API
        response = await self.client.get(f"/api/v1/relationships/tasks/{self.task_id}/recognized-contributions")
        
        # Assertions
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["source_id"] == self.recognition_id
        assert data[0]["target_id"] == self.task_id
        assert data[0]["type"] == "RECOGNIZES_CONTRIBUTION_TO"
        
        # Verify service was called correctly
        mock_service.get_relationships.assert_called_once()
    
    @pytest.mark.asyncio
    @patch("trm_api.api.v1.endpoints.relationship.relationship_service")
    async def test_delete_recognizes_contribution_to_relationship(self, mock_service):
        """Test deleting a RECOGNIZES_CONTRIBUTION_TO relationship."""
        # Set up mock
        mock_service.delete_relationship.return_value = True
        
        # Call API
        response = await self.client.delete(
            f"/api/v1/relationships/recognizes-contribution-to?recognition_id={self.recognition_id}&target_id={self.project_id}&target_type=Project"
        )
        
        # Assertions
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verify service was called correctly
        mock_service.delete_relationship.assert_called_once()
    
    @pytest.mark.asyncio
    @patch("trm_api.api.v1.endpoints.relationship.relationship_service")
    async def test_delete_recognizes_contribution_to_relationship_not_found(self, mock_service):
        """Test deleting a non-existent RECOGNIZES_CONTRIBUTION_TO relationship."""
        # Set up mock
        mock_service.delete_relationship.return_value = False
        
        # Call API
        response = await self.client.delete(
            f"/api/v1/relationships/recognizes-contribution-to?recognition_id={self.recognition_id}&target_id={self.project_id}&target_type=Project"
        )
        
        # Assertions
        assert response.status_code == status.HTTP_404_NOT_FOUND
        
        # Verify service was called correctly
        mock_service.delete_relationship.assert_called_once()
