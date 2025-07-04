import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime

from trm_api.services.relationship_service import RelationshipService
from trm_api.models.relationships import Relationship, TargetEntityTypeEnum


class TestRecognizesContributionToRelationship:
    """Test cases for RECOGNIZES_CONTRIBUTION_TO relationship between Recognition and Project."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.service = RelationshipService()
        self.recognition_id = "recognition-123"
        self.project_id = "project-456"
        
        # Sample relationship data
        self.recognition_project_relationship = {
            "source_id": self.recognition_id,
            "source_type": "Recognition",
            "target_id": self.project_id,
            "target_type": "Project",
            "type": "RECOGNIZES_CONTRIBUTION_TO",
            "createdAt": datetime.now(),
            "relationshipId": "rel-789",
            "notes": "Recognition for project contribution"
        }
    
    @patch('trm_api.services.relationship_service.RelationshipService._get_db')
    def test_create_recognizes_contribution_to_relationship(self, mock_get_db):
        """Test creating a RECOGNIZES_CONTRIBUTION_TO relationship from Recognition to Project."""
        # Mock setup
        mock_session = MagicMock()
        mock_tx = MagicMock()
        mock_result = MagicMock()
        mock_record = MagicMock()
        
        mock_record.__getitem__.side_effect = lambda key: self.recognition_project_relationship.get(key)
        mock_result.single.return_value = mock_record
        mock_tx.run.return_value = mock_result
        
        # Chuẩn bị mock cho sync
        relationship_obj = Relationship(**self.recognition_project_relationship)
        
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
            "relationshipId": self.recognition_project_relationship["relationshipId"],
            "notes": self.recognition_project_relationship["notes"]
        }
        
        # Execute test without await
        result = self.service.create_relationship(
            source_id=self.recognition_id,
            source_type=TargetEntityTypeEnum.RECOGNITION,
            target_id=self.project_id,
            target_type=TargetEntityTypeEnum.PROJECT,
            relationship_type="RECOGNIZES_CONTRIBUTION_TO",
            relationship_properties=rel_props
        )
        
        # Assertions
        assert result is not None
        
        # Kiểm tra kết quả có thể là đối tượng Relationship hoặc dictionary
        if isinstance(result, dict):
            assert result["source_id"] == self.recognition_id
            assert result["source_type"] == "Recognition"
            assert result["target_id"] == self.project_id
            assert result["target_type"] == "Project"
            assert result["type"] == "RECOGNIZES_CONTRIBUTION_TO"
        else:
            assert result.source_id == self.recognition_id
            assert result.source_type == "Recognition"
            assert result.target_id == self.project_id
            assert result.target_type == "Project"
            assert result.type == "RECOGNIZES_CONTRIBUTION_TO"
        
        # Verify mock was called correctly
        mock_session.execute_write.assert_called_once()
    
    @patch('trm_api.services.relationship_service.RelationshipService._get_db')
    def test_get_contributions_recognized_by_recognition(self, mock_get_db):
        """Test getting contributions recognized by a Recognition."""
        # Mock setup
        mock_session = MagicMock()
        mock_relationships = [
            Relationship(**self.recognition_project_relationship),
            Relationship(**{**self.recognition_project_relationship, "target_id": "project-789"}),
            Relationship(**{**self.recognition_project_relationship, "target_id": "project-012"})
        ]
        
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
            relationship_type="RECOGNIZES_CONTRIBUTION_TO",
            related_entity_type=TargetEntityTypeEnum.PROJECT
        )
        
        # Assertions
        assert len(results) == 3
        assert results[0].source_id == self.recognition_id
        assert results[0].type == "RECOGNIZES_CONTRIBUTION_TO"
        
        # Verify mock was called correctly
        mock_session.execute_read.assert_called_once()
    
    @patch('trm_api.services.relationship_service.RelationshipService._get_db')
    def test_get_recognitions_for_project_contribution(self, mock_get_db):
        """Test getting recognitions for a project contribution."""
        # Mock setup
        mock_session = MagicMock()
        mock_relationships = [Relationship(**self.recognition_project_relationship)]
        
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
            entity_id=self.project_id,
            entity_type=TargetEntityTypeEnum.PROJECT,
            direction="incoming",
            relationship_type="RECOGNIZES_CONTRIBUTION_TO",
            related_entity_type=TargetEntityTypeEnum.RECOGNITION
        )
        
        # Assertions
        assert len(results) == 1
        assert results[0].source_id == self.recognition_id
        assert results[0].target_id == self.project_id
        assert results[0].type == "RECOGNIZES_CONTRIBUTION_TO"
        
        # Verify mock was called correctly
        mock_session.execute_read.assert_called_once()
    
    @patch('trm_api.services.relationship_service.RelationshipService._get_db')
    def test_delete_recognizes_contribution_to_relationship(self, mock_get_db):
        """Test deleting a RECOGNIZES_CONTRIBUTION_TO relationship."""
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
            target_id=self.project_id,
            target_type=TargetEntityTypeEnum.PROJECT,
            relationship_type="RECOGNIZES_CONTRIBUTION_TO"
        )
        
        # Assertions
        assert result is True
        
        # Verify mock was called correctly
        mock_session.execute_write.assert_called_once()
    
    @patch('trm_api.services.relationship_service.RelationshipService._get_db')
    def test_delete_recognizes_contribution_to_relationship_not_found(self, mock_get_db):
        """Test deleting a non-existent RECOGNIZES_CONTRIBUTION_TO relationship."""
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
            target_id=self.project_id,
            target_type=TargetEntityTypeEnum.PROJECT,
            relationship_type="RECOGNIZES_CONTRIBUTION_TO"
        )
        
        # Assertions
        assert result is False
        
        # Verify mock was called correctly
        mock_session.execute_write.assert_called_once()
