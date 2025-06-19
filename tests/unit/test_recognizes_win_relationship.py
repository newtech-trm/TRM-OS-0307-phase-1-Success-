import pytest
import uuid
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

from trm_api.models.relationships import Relationship, RelationshipType, TargetEntityTypeEnum
from trm_api.services.relationship_service import RelationshipService


class TestRecognizesWinRelationship:
    """Unit tests for the RECOGNIZES_WIN relationship service methods."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.service = RelationshipService()
        
        # Sample IDs for testing
        self.recognition_id = str(uuid.uuid4())
        self.win_id = str(uuid.uuid4())
        
        # Sample relationship data for Recognition -> WIN
        self.recognition_win_relationship = {
            "source_id": self.recognition_id,
            "source_type": "Recognition",
            "target_id": self.win_id,
            "target_type": "Win",
            "type": "RECOGNIZES_WIN",
            "relationshipId": f"recognizes_win_{self.recognition_id}_{self.win_id}_abcd1234",
            "notes": "Test recognition for outstanding achievements",
            "createdAt": datetime.utcnow()
        }
    
    @patch('trm_api.services.relationship_service.RelationshipService._get_db')
    def test_create_recognizes_win_relationship(self, mock_get_db):
        """Test creating a RECOGNIZES_WIN relationship from Recognition to WIN."""
        # Mock setup
        mock_session = MagicMock()
        mock_tx = MagicMock()
        mock_result = MagicMock()
        mock_record = MagicMock()
        
        mock_record.__getitem__.side_effect = lambda key: self.recognition_win_relationship.get(key)
        mock_result.single.return_value = mock_record
        mock_tx.run.return_value = mock_result
        
        mock_session.execute_write = Mock(return_value=Relationship(**self.recognition_win_relationship))
        mock_get_db.return_value.session.return_value.__enter__.return_value = mock_session
        
        # Create relationship properties
        rel_props = {
            "relationshipId": self.recognition_win_relationship["relationshipId"],
            "notes": self.recognition_win_relationship["notes"]
        }
        
        # Execute test
        result = self.service.create_relationship(
            source_id=self.recognition_id,
            source_type=TargetEntityTypeEnum.RECOGNITION,
            target_id=self.win_id,
            target_type=TargetEntityTypeEnum.WIN,
            relationship_type="RECOGNIZES_WIN",
            relationship_properties=rel_props
        )
        
        # Assertions
        assert result is not None
        assert result.source_id == self.recognition_id
        assert result.source_type == "Recognition"
        assert result.target_id == self.win_id
        assert result.target_type == "Win"
        assert result.type == "RECOGNIZES_WIN"
        
        # Verify mock was called correctly
        mock_session.execute_write.assert_called_once()
    
    @patch('trm_api.services.relationship_service.RelationshipService._get_db')
    def test_get_wins_recognized_by_recognition(self, mock_get_db):
        """Test getting WINs recognized by a Recognition."""
        # Mock setup
        mock_session = MagicMock()
        mock_relationships = [Relationship(**self.recognition_win_relationship)]
        
        mock_session.read_transaction = Mock(return_value=mock_relationships)
        mock_get_db.return_value.session.return_value.__enter__.return_value = mock_session
        
        # Execute test
        results = self.service.get_relationships(
            entity_id=self.recognition_id,
            entity_type=TargetEntityTypeEnum.RECOGNITION,
            direction="outgoing",
            relationship_type="RECOGNIZES_WIN",
            related_entity_type=TargetEntityTypeEnum.WIN
        )
        
        # Assertions
        assert len(results) == 1
        assert results[0].source_id == self.recognition_id
        assert results[0].target_id == self.win_id
        assert results[0].type == "RECOGNIZES_WIN"
        
        # Verify mock was called correctly
        mock_session.read_transaction.assert_called_once()
    
    @patch('trm_api.services.relationship_service.RelationshipService._get_db')
    def test_get_recognitions_for_win(self, mock_get_db):
        """Test getting Recognitions for a WIN."""
        # Mock setup
        mock_session = MagicMock()
        mock_relationships = [Relationship(**self.recognition_win_relationship)]
        
        mock_session.read_transaction = Mock(return_value=mock_relationships)
        mock_get_db.return_value.session.return_value.__enter__.return_value = mock_session
        
        # Execute test
        results = self.service.get_relationships(
            entity_id=self.win_id,
            entity_type=TargetEntityTypeEnum.WIN,
            direction="incoming",
            relationship_type="RECOGNIZES_WIN",
            related_entity_type=TargetEntityTypeEnum.RECOGNITION
        )
        
        # Assertions
        assert len(results) == 1
        assert results[0].source_id == self.recognition_id
        assert results[0].target_id == self.win_id
        assert results[0].type == "RECOGNIZES_WIN"
        
        # Verify mock was called correctly
        mock_session.read_transaction.assert_called_once()
    
    @patch('trm_api.services.relationship_service.RelationshipService._get_db')
    def test_delete_recognizes_win_relationship(self, mock_get_db):
        """Test deleting a RECOGNIZES_WIN relationship."""
        # Mock setup
        mock_session = MagicMock()
        mock_summary = MagicMock()
        mock_summary.counters.relationships_deleted = 1
        
        mock_result = MagicMock()
        mock_result.consume.return_value = mock_summary
        
        mock_tx = MagicMock()
        mock_tx.run.return_value = mock_result
        
        mock_session.execute_write = Mock(return_value=True)
        mock_get_db.return_value.session.return_value.__enter__.return_value = mock_session
        
        # Execute test
        result = self.service.delete_relationship(
            source_id=self.recognition_id,
            source_type=TargetEntityTypeEnum.RECOGNITION,
            target_id=self.win_id,
            target_type=TargetEntityTypeEnum.WIN,
            relationship_type="RECOGNIZES_WIN"
        )
        
        # Assertions
        assert result is True
        
        # Verify mock was called correctly
        mock_session.execute_write.assert_called_once()
    
    @patch('trm_api.services.relationship_service.RelationshipService._get_db')
    def test_delete_recognizes_win_relationship_not_found(self, mock_get_db):
        """Test deleting a non-existent RECOGNIZES_WIN relationship."""
        # Mock setup
        mock_session = MagicMock()
        mock_summary = MagicMock()
        mock_summary.counters.relationships_deleted = 0
        
        mock_result = MagicMock()
        mock_result.consume.return_value = mock_summary
        
        mock_tx = MagicMock()
        mock_tx.run.return_value = mock_result
        
        mock_session.execute_write = Mock(return_value=False)
        mock_get_db.return_value.session.return_value.__enter__.return_value = mock_session
        
        # Execute test
        result = self.service.delete_relationship(
            source_id=self.recognition_id,
            source_type=TargetEntityTypeEnum.RECOGNITION,
            target_id=self.win_id,
            target_type=TargetEntityTypeEnum.WIN,
            relationship_type="RECOGNIZES_WIN"
        )
        
        # Assertions
        assert result is False
        
        # Verify mock was called correctly
        mock_session.execute_write.assert_called_once()
