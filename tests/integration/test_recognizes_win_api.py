import pytest
import pytest_asyncio
import uuid
from unittest.mock import patch, AsyncMock
from datetime import datetime
from httpx import AsyncClient
from fastapi import status

from trm_api.main import app
from trm_api.models.relationships import Relationship, RelationshipType, TargetEntityTypeEnum
from tests.conftest import get_test_client


class TestRecognizesWinAPI:
    """Integration tests for the RECOGNIZES_WIN relationship API endpoints."""

    async def setup_method(self):
        """Setup test fixtures before each test method."""
        # Sample IDs for testing
        self.recognition_id = str(uuid.uuid4())
        self.win_id = str(uuid.uuid4())
        
        # Sample relationship data
        self.recognition_win_relationship = {
            "source_id": self.recognition_id,
            "source_type": "Recognition",
            "target_id": self.win_id,
            "target_type": "Win",
            "type": "RECOGNIZES_WIN",
            "relationshipId": f"recognizes_win_{self.recognition_id}_{self.win_id}_abcd1234",
            "notes": "Test recognition for outstanding achievements",
            "createdAt": datetime.now()
        }
        
        # Sample relationship request data
        self.recognizes_win_request = {
            "notes": "Recognition for exceptional problem solving"
        }
        
        # Tạo async client
        self.client = await get_test_client()
    
    @pytest.mark.asyncio
    @patch("trm_api.api.v1.endpoints.relationship.relationship_service")
    async def test_create_recognizes_win_relationship(self, mock_service):
        """Test creating a RECOGNIZES_WIN relationship from Recognition to WIN."""
        # Set up mock
        mock_service.create_relationship.return_value = Relationship(**self.recognition_win_relationship)
        mock_service.create_relationship.side_effect = AsyncMock(return_value=Relationship(**self.recognition_win_relationship))
        
        # Call API with async client
        response = await self.client.post(
            f"/api/v1/relationships/recognizes-win?recognition_id={self.recognition_id}&win_id={self.win_id}",
            json=self.recognizes_win_request
        )
        
        # Assertions
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["source_id"] == self.recognition_id
        assert data["source_type"] == "Recognition"
        assert data["target_id"] == self.win_id
        assert data["target_type"] == "Win"
        assert data["type"] == "RECOGNIZES_WIN"
        
        # Verify service was called correctly
        mock_service.create_relationship.assert_called_once()
    
    @pytest.mark.asyncio
    @patch("trm_api.api.v1.endpoints.relationship.relationship_service")
    async def test_create_recognizes_win_relationship_entities_not_found(self, mock_service):
        """Test creating a RECOGNIZES_WIN relationship when entities don't exist."""
        # Set up mock
        mock_service.create_relationship = AsyncMock(return_value=None)
        
        # Call API
        response = await self.client.post(
            f"/api/v1/relationships/recognizes-win?recognition_id={self.recognition_id}&win_id={self.win_id}",
            json=self.recognizes_win_request
        )
        
        # Assertions
        assert response.status_code == status.HTTP_404_NOT_FOUND
        
        # Verify service was called correctly
        mock_service.create_relationship.assert_called_once()
    
    @pytest.mark.asyncio
    @patch("trm_api.api.v1.endpoints.relationship.relationship_service")
    async def test_get_wins_recognized_by_recognition(self, mock_service):
        """Test getting WINs recognized by a Recognition."""
        # Set up mock
        mock_service.get_relationships = AsyncMock(return_value=[Relationship(**self.recognition_win_relationship)])
        
        # Call API
        response = await self.client.get(f"/api/v1/relationships/recognitions/{self.recognition_id}/recognizes-wins")
        
        # Assertions
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["source_id"] == self.recognition_id
        assert data[0]["target_id"] == self.win_id
        assert data[0]["type"] == "RECOGNIZES_WIN"
        
        # Verify service was called correctly
        mock_service.get_relationships.assert_called_once()
    
    @pytest.mark.asyncio
    @patch("trm_api.api.v1.endpoints.relationship.relationship_service")
    async def test_get_recognitions_for_win(self, mock_service):
        """Test getting Recognitions for a WIN."""
        # Set up mock
        mock_service.get_relationships = AsyncMock(return_value=[Relationship(**self.recognition_win_relationship)])
        
        # Call API
        response = await self.client.get(f"/api/v1/relationships/wins/{self.win_id}/recognized-by")
        
        # Assertions
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["source_id"] == self.recognition_id
        assert data[0]["target_id"] == self.win_id
        assert data[0]["type"] == "RECOGNIZES_WIN"
        
        # Verify service was called correctly
        mock_service.get_relationships.assert_called_once()
    
    @pytest.mark.asyncio
    @patch("trm_api.api.v1.endpoints.relationship.relationship_service")
    async def test_get_empty_wins_recognized_by_recognition(self, mock_service):
        """Test getting WINs when Recognition has no relationships."""
        # Set up mock
        mock_service.get_relationships = AsyncMock(return_value=[])
        
        # Call API
        response = await self.client.get(f"/api/v1/relationships/recognitions/{self.recognition_id}/recognizes-wins")
        
        # Assertions
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 0
        
        # Verify service was called correctly
        mock_service.get_relationships.assert_called_once()
    
    @pytest.mark.asyncio
    @patch("trm_api.api.v1.endpoints.relationship.relationship_service")
    async def test_delete_recognizes_win_relationship(self, mock_service):
        """Test deleting a RECOGNIZES_WIN relationship."""
        # Set up mock
        mock_service.delete_relationship = AsyncMock(return_value=True)
        
        # Call API
        response = await self.client.delete(
            f"/api/v1/relationships/recognizes-win?recognition_id={self.recognition_id}&win_id={self.win_id}"
        )
        
        # Assertions
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verify service was called correctly
        mock_service.delete_relationship.assert_called_once()
    
    @pytest.mark.asyncio
    @patch("trm_api.api.v1.endpoints.relationship.relationship_service")
    async def test_delete_recognizes_win_relationship_not_found(self, mock_service):
        """Test deleting a non-existent RECOGNIZES_WIN relationship."""
        # Set up mock
        mock_service.delete_relationship = AsyncMock(return_value=False)
        
        # Call API
        response = await self.client.delete(
            f"/api/v1/relationships/recognizes-win?recognition_id={self.recognition_id}&win_id={self.win_id}"
        )
        
        # Assertions
        assert response.status_code == status.HTTP_404_NOT_FOUND
        
        # Verify service was called correctly
        mock_service.delete_relationship.assert_called_once()
