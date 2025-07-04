import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime

from trm_api.services.relationship_service import RelationshipService
from trm_api.models.relationships import Relationship, TargetEntityTypeEnum


class TestRecognizesWinRelationship:
    """Test cases for RECOGNIZES_WIN relationship between Recognition and Win."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.service = RelationshipService()
        self.recognition_id = "recognition-123"
        self.win_id = "win-456"
        
        # Sample relationship data
        self.recognition_win_relationship = {
            "source_id": self.recognition_id,
            "source_type": "Recognition",
            "target_id": self.win_id,
            "target_type": "Win",
            "type": "RECOGNIZES_WIN",
            "createdAt": datetime.now(),
            "relationshipId": "rel-789",
            "notes": "Recognition for achieving win"
        }
    
    @patch('trm_api.services.relationship_service.RelationshipService._get_db')
    def test_create_recognizes_win_relationship(self, mock_get_db):
        """Test creating a RECOGNIZES_WIN relationship from Recognition to Win."""
        # Mock setup
        mock_session = MagicMock()
        mock_tx = MagicMock()
        mock_result = MagicMock()
        mock_record = MagicMock()
        
        mock_record.__getitem__.side_effect = lambda key: self.recognition_win_relationship.get(key)
        mock_result.single.return_value = mock_record
        mock_tx.run.return_value = mock_result
        
        # Chuẩn bị mock cho sync
        relationship_obj = Relationship(**self.recognition_win_relationship)
        
        # Thiết lập mock đúng cách cho sync
        mock_session.execute_write.return_value = relationship_obj
        
        mock_session_context = MagicMock()
        mock_session_context.__enter__.return_value = mock_session
        mock_session_context.__exit__.return_value = None
        
        # Quan trọng: Cấu hình _get_db để có thể sử dụng với sync
        mock_db = MagicMock()
        mock_db.session.return_value = mock_session_context
        mock_get_db.return_value = mock_db
        
        # Create relationship properties
        rel_props = {
            "relationshipId": self.recognition_win_relationship["relationshipId"],
            "notes": self.recognition_win_relationship["notes"]
        }
        
        # Execute test without await
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
        
        # Kiểm tra kết quả có thể là đối tượng Relationship hoặc dictionary
        if isinstance(result, dict):
            assert result["source_id"] == self.recognition_id
            assert result["source_type"] == "Recognition"
            assert result["target_id"] == self.win_id
            assert result["target_type"] == "Win"
            assert result["type"] == "RECOGNIZES_WIN"
        else:
            assert result.source_id == self.recognition_id
            assert result.source_type == "Recognition"
            assert result.target_id == self.win_id
            assert result.target_type == "Win"
            assert result.type == "RECOGNIZES_WIN"
        
        # Verify mock was called correctly
        mock_session.execute_write.assert_called_once()
    
    @patch('trm_api.services.relationship_service.RelationshipService._get_db')
    def test_get_wins_recognized_by_recognition(self, mock_get_db):
        """Test getting Wins recognized by a Recognition."""
        # Mock setup
        mock_session = MagicMock()
        mock_relationships = [Relationship(**self.recognition_win_relationship)]
        
        # Thiết lập mock đúng cách cho sync
        mock_session.execute_read.return_value = mock_relationships
        
        mock_session_context = MagicMock()
        mock_session_context.__enter__.return_value = mock_session
        mock_session_context.__exit__.return_value = None
        
        # Quan trọng: Cấu hình _get_db để có thể sử dụng với sync
        mock_db = MagicMock()
        mock_db.session.return_value = mock_session_context
        mock_get_db.return_value = mock_db
        
        # Execute test without await
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
        mock_session.execute_read.assert_called_once()
    
    @patch('trm_api.services.relationship_service.RelationshipService._get_db')
    def test_get_recognitions_for_win(self, mock_get_db):
        """Test getting Recognitions for a Win."""
        # Mock setup
        mock_session = MagicMock()
        mock_relationships = [Relationship(**self.recognition_win_relationship)]
        
        # Thiết lập mock đúng cách cho sync
        mock_session.execute_read.return_value = mock_relationships
        
        mock_session_context = MagicMock()
        mock_session_context.__enter__.return_value = mock_session
        mock_session_context.__exit__.return_value = None
        
        # Quan trọng: Cấu hình _get_db để có thể sử dụng với sync
        mock_db = MagicMock()
        mock_db.session.return_value = mock_session_context
        mock_get_db.return_value = mock_db
        
        # Execute test without await
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
        mock_session.execute_read.assert_called_once()
    
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
        
        # Thiết lập mock đúng cách cho sync
        mock_session.execute_write.return_value = True
        
        mock_session_context = MagicMock()
        mock_session_context.__enter__.return_value = mock_session
        mock_session_context.__exit__.return_value = None
        
        # Quan trọng: Cấu hình _get_db để có thể sử dụng với sync
        mock_db = MagicMock()
        mock_db.session.return_value = mock_session_context
        mock_get_db.return_value = mock_db
        
        # Execute test without await
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
        
        # Thiết lập mock đúng cách cho sync
        mock_session.execute_write.return_value = False
        
        mock_session_context = MagicMock()
        mock_session_context.__enter__.return_value = mock_session
        mock_session_context.__exit__.return_value = None
        
        # Quan trọng: Cấu hình _get_db để có thể sử dụng với sync
        mock_db = MagicMock()
        mock_db.session.return_value = mock_session_context
        mock_get_db.return_value = mock_db
        
        # Execute test without await
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
