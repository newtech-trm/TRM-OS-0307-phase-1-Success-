import pytest
import pytest_asyncio
import uuid
from unittest.mock import patch, AsyncMock
from datetime import datetime
from httpx import AsyncClient
from fastapi import status

from trm_api.main import app
from trm_api.models.relationships import Relationship, RelationshipType, TargetEntityTypeEnum
from tests.conftest import async_test_client


class TestReceivedByAPI:
    """Integration tests for the RECEIVED_BY relationship API endpoints."""

    @pytest_asyncio.fixture(autouse=True)
    async def setup_test(self, async_test_client):
        """Setup test fixtures before each test method using pytest-asyncio fixture."""
        # Sample IDs for testing
        self.recognition_id = str(uuid.uuid4())
        self.agent_id = str(uuid.uuid4())
        
        # Sample relationship data
        self.recognition_agent_relationship = {
            "source_id": self.recognition_id,
            "source_type": "Recognition",
            "target_id": self.agent_id,
            "target_type": "Agent",
            "type": "RECEIVED_BY",
            "relationshipId": f"received_by_{self.recognition_id}_{self.agent_id}_abcd1234",
            "notes": "Test note for received recognition",
            "createdAt": datetime.now()
        }
        
        # Sample relationship request data
        self.received_by_request = {
            "notes": "Recognition received for outstanding performance"
        }
        
        # Sử dụng client từ fixture
        self.client = async_test_client
    
    @pytest.mark.asyncio
    @patch("trm_api.api.v1.endpoints.relationship.relationship_service")
    async def test_create_received_by_relationship(self, mock_service):
        """Test creating a RECEIVED_BY relationship from Recognition to Agent."""
        # Set up mock
        mock_service.create_relationship = AsyncMock(return_value=Relationship(**self.recognition_agent_relationship))
        
        # Call API
        response = await self.client.post(
            f"/api/v1/relationships/received-by?recognition_id={self.recognition_id}&agent_id={self.agent_id}",
            json=self.received_by_request
        )
        
        # Assertions
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["source_id"] == self.recognition_id
        assert data["source_type"] == "Recognition"
        assert data["target_id"] == self.agent_id
        assert data["target_type"] == "Agent"
        assert data["type"] == "RECEIVED_BY"
        
        # Verify service was called correctly
        mock_service.create_relationship.assert_called_once()
    
    @pytest.mark.asyncio
    @patch("trm_api.api.v1.endpoints.relationship.relationship_service")
    async def test_create_received_by_relationship_entities_not_found(self, mock_service):
        """Test creating a RECEIVED_BY relationship when entities don't exist."""
        # Set up mock
        mock_service.create_relationship = AsyncMock(return_value=None)
        
        # Call API
        async with httpx.AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                f"/api/v1/relationships/received-by?recognition_id={self.recognition_id}&agent_id={self.agent_id}",
                json=self.received_by_request
            )
        
        # Assertions
        assert response.status_code == status.HTTP_404_NOT_FOUND
        
        # Verify service was called correctly
        mock_service.create_relationship.assert_called_once()
    
    @pytest.mark.asyncio
    @patch("trm_api.api.v1.endpoints.relationship.relationship_service")
    async def test_get_agents_receiving_recognition(self, mock_service):
        """Test getting Agents that received a Recognition."""
        # Set up mock
        mock_service.get_relationships = AsyncMock(return_value=[Relationship(**self.recognition_agent_relationship)])
        
        # Call API
        async with httpx.AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get(f"/api/v1/relationships/recognitions/{self.recognition_id}/received-by")
        
        # Assertions
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["source_id"] == self.recognition_id
        assert data[0]["target_id"] == self.agent_id
        assert data[0]["type"] == "RECEIVED_BY"
        
        # Verify service was called correctly
        mock_service.get_relationships.assert_called_once()
    
    @patch("trm_api.api.v1.endpoints.relationship.relationship_service")
    def test_get_recognitions_received_by_agent(self, mock_service):
        """Test getting Recognitions received by an Agent."""
        # Set up mock
        mock_service.get_relationships.return_value = [Relationship(**self.recognition_agent_relationship)]
        
        # Call API
        response = client.get(f"/api/v1/relationships/agents/{self.agent_id}/received-recognitions")
        
        # Assertions
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["source_id"] == self.recognition_id
        assert data[0]["target_id"] == self.agent_id
        assert data[0]["type"] == "RECEIVED_BY"
        
        # Verify service was called correctly
        mock_service.get_relationships.assert_called_once()
    
    @patch("trm_api.api.v1.endpoints.relationship.relationship_service")
    def test_get_empty_agents_receiving_recognition(self, mock_service):
        """Test getting Agents when Recognition has no relationships."""
        # Set up mock
        mock_service.get_relationships.return_value = []
        
        # Call API
        response = client.get(f"/api/v1/relationships/recognitions/{self.recognition_id}/received-by")
        
        # Assertions
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 0
        
        # Verify service was called correctly
        mock_service.get_relationships.assert_called_once()
    
    @patch("trm_api.api.v1.endpoints.relationship.relationship_service")
    def test_delete_received_by_relationship(self, mock_service):
        """Test deleting a RECEIVED_BY relationship."""
        # Set up mock
        mock_service.delete_relationship.return_value = True
        
        # Call API
        response = client.delete(
            f"/api/v1/relationships/received-by?recognition_id={self.recognition_id}&agent_id={self.agent_id}"
        )
        
        # Assertions
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verify service was called correctly
        mock_service.delete_relationship.assert_called_once()
    
    @patch("trm_api.api.v1.endpoints.relationship.relationship_service")
    def test_delete_received_by_relationship_not_found(self, mock_service):
        """Test deleting a non-existent RECEIVED_BY relationship."""
        # Set up mock
        mock_service.delete_relationship.return_value = False
        
        # Call API
        response = client.delete(
            f"/api/v1/relationships/received-by?recognition_id={self.recognition_id}&agent_id={self.agent_id}"
        )
        
        # Assertions
        assert response.status_code == status.HTTP_404_NOT_FOUND
        
        # Verify service was called correctly
        mock_service.delete_relationship.assert_called_once()
