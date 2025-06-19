import pytest
from unittest.mock import Mock, patch, MagicMock
import uuid
from datetime import datetime

from trm_api.services.knowledge_snippet_service import KnowledgeSnippetService
from trm_api.models.knowledge_snippet import KnowledgeSnippetCreate, KnowledgeSnippetUpdate

class TestKnowledgeSnippetService:
    """Unit tests for the KnowledgeSnippetService."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.service = KnowledgeSnippetService()
        
        # Create a sample snippet data
        sample_id = str(uuid.uuid4())
        self.sample_snippet = {
            "uid": sample_id,  # Sử dụng uid làm trường định danh chính theo chuẩn mới
            "snippetId": sample_id,  # Giữ lại snippetId cho tương thích ngược
            "content": "Test knowledge snippet content",
            "snippetType": "BestPractice",
            "sourceEntityId": "win_123",
            "tags": ["test", "knowledge"],
            "version": 1,
            "createdAt": datetime.utcnow(),
            "updatedAt": None
        }
        
        # Sample create data
        self.create_data = KnowledgeSnippetCreate(
            content="Test knowledge snippet content",
            snippetType="BestPractice",
            sourceEntityId="win_123",
            tags=["test", "knowledge"]
        )
        
        # Sample update data
        self.update_data = KnowledgeSnippetUpdate(
            content="Updated content",
            snippetType="CodeExample"
        )
    
    @patch('trm_api.services.knowledge_snippet_service.get_driver')
    def test_create_snippet(self, mock_get_driver):
        """Test creating a new knowledge snippet."""
        # Mock setup
        mock_session = MagicMock()
        mock_tx = MagicMock()
        mock_tx.run.return_value.single.return_value = {'ks': self.sample_snippet}
        mock_session.write_transaction.return_value = self.sample_snippet
        mock_driver = MagicMock()
        mock_driver.session.return_value.__enter__.return_value = mock_session
        mock_get_driver.return_value = mock_driver
        
        # Call the service method
        result = self.service.create_snippet(snippet_create=self.create_data)
        
        # Assert expected behavior
        mock_session.write_transaction.assert_called_once()
        assert result["content"] == self.sample_snippet["content"]
        assert result["snippetType"] == self.sample_snippet["snippetType"]
    
    @patch('trm_api.services.knowledge_snippet_service.get_driver')
    def test_get_snippet_by_id(self, mock_get_driver):
        """Test retrieving a snippet by ID."""
        # Mock setup
        mock_session = MagicMock()
        mock_session.read_transaction.return_value = self.sample_snippet
        mock_driver = MagicMock()
        mock_driver.session.return_value.__enter__.return_value = mock_session
        mock_get_driver.return_value = mock_driver
        
        # Call the service method
        result = self.service.get_snippet_by_id(snippet_id=self.sample_snippet["uid"])
        
        # Assert expected behavior
        mock_session.read_transaction.assert_called_once()
        assert result["uid"] == self.sample_snippet["uid"]  # Kiểm tra trường uid
        assert result["snippetId"] == self.sample_snippet["snippetId"]  # Kiểm tra cả trường snippetId
        assert result["content"] == self.sample_snippet["content"]
    
    @patch('trm_api.services.knowledge_snippet_service.get_driver')
    def test_get_snippet_by_id_not_found(self, mock_get_driver):
        """Test retrieving a non-existent snippet."""
        # Mock setup
        mock_session = MagicMock()
        mock_session.read_transaction.return_value = None
        mock_driver = MagicMock()
        mock_driver.session.return_value.__enter__.return_value = mock_session
        mock_get_driver.return_value = mock_driver
        
        # Call the service method
        result = self.service.get_snippet_by_id(snippet_id="non_existent_id")
        
        # Assert expected behavior
        mock_session.read_transaction.assert_called_once()
        assert result is None
    
    @patch('trm_api.services.knowledge_snippet_service.get_driver')
    def test_list_snippets(self, mock_get_driver):
        """Test listing snippets with pagination."""
        # Sample list of snippets
        snippets = [self.sample_snippet, {**self.sample_snippet, "snippetId": str(uuid.uuid4())}]
        
        # Mock setup
        mock_session = MagicMock()
        mock_session.read_transaction.return_value = snippets
        mock_driver = MagicMock()
        mock_driver.session.return_value.__enter__.return_value = mock_session
        mock_get_driver.return_value = mock_driver
        
        # Call the service method
        result = self.service.list_snippets(skip=0, limit=10)
        
        # Assert expected behavior
        mock_session.read_transaction.assert_called_once_with(
            self.service._list_snippets_tx, 0, 10
        )
        assert len(result) == 2
        assert result[0]["snippetId"] == snippets[0]["snippetId"]
    
    @patch('trm_api.services.knowledge_snippet_service.get_driver')
    def test_update_snippet(self, mock_get_driver):
        """Test updating a snippet."""
        # Create an updated snippet for the mock
        updated_snippet = self.sample_snippet.copy()
        updated_snippet["content"] = "Updated content"
        updated_snippet["snippetType"] = "CodeExample"
        updated_snippet["version"] = 2
        updated_snippet["updatedAt"] = datetime.utcnow()
        
        # Mock setup
        mock_session = MagicMock()
        mock_session.write_transaction.return_value = updated_snippet
        mock_driver = MagicMock()
        mock_driver.session.return_value.__enter__.return_value = mock_session
        mock_get_driver.return_value = mock_driver
        
        # Call the service method
        result = self.service.update_snippet(
            snippet_id=self.sample_snippet["uid"],  # Sử dụng trường uid 
            snippet_update=self.update_data
        )
        
        # Assert expected behavior
        mock_session.write_transaction.assert_called_once()
        assert result["uid"] == self.sample_snippet["uid"]  # Kiểm tra trường uid
        assert result["snippetId"] == self.sample_snippet["snippetId"]  # Kiểm tra trường snippetId
        assert result["content"] == updated_snippet["content"]
        assert result["snippetType"] == updated_snippet["snippetType"]
        assert result["version"] == 2
    
    @patch('trm_api.services.knowledge_snippet_service.get_driver')
    def test_update_snippet_not_found(self, mock_get_driver):
        """Test updating a non-existent snippet."""
        # Mock setup
        mock_session = MagicMock()
        mock_session.write_transaction.return_value = None
        mock_driver = MagicMock()
        mock_driver.session.return_value.__enter__.return_value = mock_session
        mock_get_driver.return_value = mock_driver
        
        # Call the service method
        result = self.service.update_snippet(
            snippet_id="non_existent_id",
            snippet_update=self.update_data
        )
        
        # Assert expected behavior
        assert result is None
    
    @patch('trm_api.services.knowledge_snippet_service.get_driver')
    def test_delete_snippet(self, mock_get_driver):
        """Test deleting a snippet."""
        # Mock setup
        mock_session = MagicMock()
        mock_session.write_transaction.return_value = True
        mock_driver = MagicMock()
        mock_driver.session.return_value.__enter__.return_value = mock_session
        mock_get_driver.return_value = mock_driver
        
        # Call the service method
        result = self.service.delete_snippet(snippet_id=self.sample_snippet["snippetId"])
        
        # Assert expected behavior
        mock_session.write_transaction.assert_called_once()
        assert result is True
    
    @patch('trm_api.services.knowledge_snippet_service.get_driver')
    def test_delete_snippet_not_found(self, mock_get_driver):
        """Test deleting a non-existent snippet."""
        # Mock setup
        mock_session = MagicMock()
        mock_session.write_transaction.return_value = False
        mock_driver = MagicMock()
        mock_driver.session.return_value.__enter__.return_value = mock_session
        mock_get_driver.return_value = mock_driver
        
        # Call the service method
        result = self.service.delete_snippet(snippet_id="non_existent_id")
        
        # Assert expected behavior
        assert result is False
