import pytest
from fastapi.testclient import TestClient
import uuid
from datetime import datetime
from unittest.mock import patch, MagicMock

from trm_api.main import app
from trm_api.services.knowledge_snippet_service import knowledge_snippet_service

# Setup test client
client = TestClient(app)

class TestKnowledgeSnippetEndpoints:
    """Integration tests for Knowledge Snippet API endpoints."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        # Sample knowledge snippet data
        self.snippet_id = str(uuid.uuid4())
        self.sample_snippet = {
            "uid": self.snippet_id,  # Sử dụng uid theo chuẩn mới
            "snippetId": self.snippet_id,  # Giữ lại snippetId cho tương thích ngược
            "content": "Test knowledge snippet content",
            "snippetType": "BestPractice",
            "sourceEntityId": "win_123",
            "tags": ["test", "knowledge"],
            "version": 1,
            "createdAt": datetime.utcnow(),
            "updatedAt": None
        }
        
        # Sample create payload
        self.create_payload = {
            "content": "New knowledge snippet for testing",
            "snippetType": "CodeExample",
            "sourceEntityId": "win_456",
            "tags": ["test", "integration"]
        }
        
        # Sample update payload
        self.update_payload = {
            "content": "Updated content for testing",
            "snippetType": "HowToGuide"
        }
    
    @patch.object(knowledge_snippet_service, 'create_snippet')
    def test_create_knowledge_snippet(self, mock_create):
        """Test creating a new knowledge snippet."""
        # Setup mock
        mock_create.return_value = self.sample_snippet
        
        # Make API request
        response = client.post(
            "/api/v1/knowledge-snippets/",
            json=self.create_payload
        )
        
        # Assert response
        assert response.status_code == 201
        assert "uid" in response.json()  # Kiểm tra trường uid theo chuẩn mới
        assert "snippetId" in response.json()  # Vẫn kiểm tra snippetId cho tương thích ngược
        assert response.json()["content"] == self.sample_snippet["content"]
        
        # Verify mock called correctly
        mock_create.assert_called_once()
    
    @patch.object(knowledge_snippet_service, 'get_snippet_by_id')
    def test_get_knowledge_snippet(self, mock_get):
        """Test retrieving a knowledge snippet by ID."""
        # Setup mock
        mock_get.return_value = self.sample_snippet
        
        # Make API request
        response = client.get(f"/api/v1/knowledge-snippets/{self.snippet_id}")
        
        # Assert response
        assert response.status_code == 200
        assert response.json()["uid"] == self.snippet_id  # Kiểm tra trường uid
        assert response.json()["snippetId"] == self.snippet_id  # Vẫn kiểm tra snippetId cho tương thích ngược
        assert "createdAt" in response.json()
        
        # Verify mock called correctly
        mock_get.assert_called_once_with(snippet_id=self.snippet_id)
    
    @patch.object(knowledge_snippet_service, 'get_snippet_by_id')
    def test_get_knowledge_snippet_not_found(self, mock_get):
        """Test retrieving a non-existent knowledge snippet."""
        # Setup mock
        mock_get.return_value = None
        
        # Make API request
        response = client.get("/api/v1/knowledge-snippets/non_existent_id")
        
        # Assert response
        assert response.status_code == 404
        assert "detail" in response.json()
    
    @patch.object(knowledge_snippet_service, 'list_snippets')
    def test_list_knowledge_snippets(self, mock_list):
        """Test listing knowledge snippets with pagination."""
        # Setup mock
        second_id = str(uuid.uuid4())
        mock_list.return_value = [
            self.sample_snippet, 
            {
                **self.sample_snippet, 
                "uid": second_id,  # Trường uid mới cho item thứ hai
                "snippetId": second_id  # Giữ snippetId cho tương thích ngược
            }
        ]
        
        # Make API request
        response = client.get("/api/v1/knowledge-snippets/?skip=0&limit=10")
        
        # Assert response
        assert response.status_code == 200
        assert "items" in response.json()
        assert len(response.json()["items"]) == 2
        
        # Kiểm tra trường uid trong các item trả về
        for item in response.json()["items"]:
            assert "uid" in item
            assert "snippetId" in item  # Vẫn kiểm tra trường snippetId
            
        assert "total" in response.json()
        
        # Verify mock called correctly
        mock_list.assert_called_once_with(skip=0, limit=10)
    
    @patch.object(knowledge_snippet_service, 'update_snippet')
    def test_update_knowledge_snippet(self, mock_update):
        """Test updating a knowledge snippet."""
        # Setup mock
        updated_snippet = {
            **self.sample_snippet,
            "content": "Updated content for testing",
            "snippetType": "HowToGuide",
            "version": 2,
            "updatedAt": datetime.utcnow()
        }
        mock_update.return_value = updated_snippet
        
        # Make API request
        response = client.put(
            f"/api/v1/knowledge-snippets/{self.snippet_id}",
            json=self.update_payload
        )
        
        # Assert response
        assert response.status_code == 200
        assert response.json()["uid"] == self.snippet_id  # Kiểm tra trường uid
        assert response.json()["snippetId"] == self.snippet_id  # Vẫn kiểm tra trường snippetId
        assert response.json()["content"] == "Updated content for testing"
        assert response.json()["snippetType"] == "HowToGuide"
        
        # Verify mock called correctly
        mock_update.assert_called_once()
    
    @patch.object(knowledge_snippet_service, 'update_snippet')
    def test_update_knowledge_snippet_not_found(self, mock_update):
        """Test updating a non-existent knowledge snippet."""
        # Setup mock
        mock_update.return_value = None
        
        # Make API request
        response = client.put(
            "/api/v1/knowledge-snippets/non_existent_id",
            json=self.update_payload
        )
        
        # Assert response
        assert response.status_code == 404
        assert "detail" in response.json()
    
    @patch.object(knowledge_snippet_service, 'delete_snippet')
    def test_delete_knowledge_snippet(self, mock_delete):
        """Test deleting a knowledge snippet."""
        # Setup mock
        mock_delete.return_value = True
        
        # Make API request
        response = client.delete(f"/api/v1/knowledge-snippets/{self.snippet_id}")
        
        # Assert response
        assert response.status_code == 204
        
        # Verify mock called correctly - service vẫn dùng snippet_id làm tham số cho tương thích
        # nhưng giá trị truyền vào là uid theo chuẩn mới
        mock_delete.assert_called_once_with(snippet_id=self.snippet_id)
    
    @patch.object(knowledge_snippet_service, 'delete_snippet')
    def test_delete_knowledge_snippet_not_found(self, mock_delete):
        """Test deleting a non-existent knowledge snippet."""
        # Setup mock
        mock_delete.return_value = False
        
        # Make API request
        response = client.delete("/api/v1/knowledge-snippets/non_existent_id")
        
        # Assert response
        assert response.status_code == 404
        assert "detail" in response.json()
