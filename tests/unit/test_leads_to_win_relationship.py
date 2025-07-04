import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime

from trm_api.services.relationship_service import RelationshipService
from trm_api.models.relationships import Relationship, TargetEntityTypeEnum


class TestLeadsToWinRelationship:
    """Test cases for LEADS_TO_WIN relationship between Project/Event and Win."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.service = RelationshipService()
        self.project_id = "project-123"
        self.event_id = "event-456"
        self.win_id = "win-789"
        
        # Sample relationship data for Project -> Win
        self.project_win_relationship = {
            "source_id": self.project_id,
            "source_type": "Project",
            "target_id": self.win_id,
            "target_type": "Win",
            "type": "LEADS_TO_WIN",
            "createdAt": datetime.now(),
            "relationshipId": "rel-project-win-123",
            "notes": "Project completion led to business win"
        }
        
        # Sample relationship data for Event -> Win
        self.event_win_relationship = {
            "source_id": self.event_id,
            "source_type": "Event",
            "target_id": self.win_id,
            "target_type": "Win",
            "type": "LEADS_TO_WIN",
            "createdAt": datetime.now(),
            "relationshipId": "rel-event-win-456",
            "notes": "Event execution led to business win"
        }
    
    @patch('trm_api.services.relationship_service.RelationshipService._get_db')
    def test_create_project_leads_to_win_relationship(self, mock_get_db):
        """Test creating a LEADS_TO_WIN relationship from Project to Win."""
        # Mock setup
        mock_session = MagicMock()
        mock_tx = MagicMock()
        mock_result = MagicMock()
        mock_record = MagicMock()
        
        mock_record.__getitem__.side_effect = lambda key: self.project_win_relationship.get(key)
        mock_result.single.return_value = mock_record
        mock_tx.run.return_value = mock_result
        
        # Chuẩn bị mock cho sync
        relationship_obj = Relationship(**self.project_win_relationship)
        
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
            "relationshipId": self.project_win_relationship["relationshipId"],
            "notes": self.project_win_relationship["notes"]
        }
        
        # Execute test without await
        result = self.service.create_relationship(
            source_id=self.project_id,
            source_type=TargetEntityTypeEnum.PROJECT,
            target_id=self.win_id,
            target_type=TargetEntityTypeEnum.WIN,
            relationship_type="LEADS_TO_WIN",
            relationship_properties=rel_props
        )
        
        # Assertions
        assert result is not None
        
        # Kiểm tra kết quả có thể là đối tượng Relationship hoặc dictionary
        if isinstance(result, dict):
            assert result["source_id"] == self.project_id
            assert result["source_type"] == "Project"
            assert result["target_id"] == self.win_id
            assert result["target_type"] == "Win"
            assert result["type"] == "LEADS_TO_WIN"
        else:
            assert result.source_id == self.project_id
            assert result.source_type == "Project"
            assert result.target_id == self.win_id
            assert result.target_type == "Win"
            assert result.type == "LEADS_TO_WIN"
        
        # Verify mock was called correctly
        mock_session.execute_write.assert_called_once()
    
    @patch('trm_api.services.relationship_service.RelationshipService._get_db')
    def test_create_event_leads_to_win_relationship(self, mock_get_db):
        """Test creating a LEADS_TO_WIN relationship from Event to Win."""
        # Mock setup
        mock_session = MagicMock()
        mock_tx = MagicMock()
        mock_result = MagicMock()
        mock_record = MagicMock()
        
        mock_record.__getitem__.side_effect = lambda key: self.event_win_relationship.get(key)
        mock_result.single.return_value = mock_record
        mock_tx.run.return_value = mock_result
        
        # Chuẩn bị mock cho sync
        relationship_obj = Relationship(**self.event_win_relationship)
        
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
            "relationshipId": self.event_win_relationship["relationshipId"],
            "notes": self.event_win_relationship["notes"]
        }
        
        # Execute test without await
        result = self.service.create_relationship(
            source_id=self.event_id,
            source_type=TargetEntityTypeEnum.EVENT,
            target_id=self.win_id,
            target_type=TargetEntityTypeEnum.WIN,
            relationship_type="LEADS_TO_WIN",
            relationship_properties=rel_props
        )
        
        # Assertions
        assert result is not None
        
        # Kiểm tra kết quả có thể là đối tượng Relationship hoặc dictionary
        if isinstance(result, dict):
            assert result["source_id"] == self.event_id
            assert result["source_type"] == "Event"
            assert result["target_id"] == self.win_id
            assert result["target_type"] == "Win"
            assert result["type"] == "LEADS_TO_WIN"
        else:
            assert result.source_id == self.event_id
            assert result.source_type == "Event"
            assert result.target_id == self.win_id
            assert result.target_type == "Win"
            assert result.type == "LEADS_TO_WIN"
        
        # Verify mock was called correctly
        mock_session.execute_write.assert_called_once()
    
    @patch('trm_api.services.relationship_service.RelationshipService._get_db')
    def test_get_wins_from_project(self, mock_get_db):
        """Test getting Wins from a Project."""
        # Mock setup
        mock_session = MagicMock()
        mock_relationships = [Relationship(**self.project_win_relationship)]
        
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
            direction="outgoing",
            relationship_type="LEADS_TO_WIN",
            related_entity_type=TargetEntityTypeEnum.WIN
        )
        
        # Assertions
        assert len(results) == 1
        assert results[0].source_id == self.project_id
        assert results[0].target_id == self.win_id
        assert results[0].type == "LEADS_TO_WIN"
        
        # Verify mock was called correctly
        mock_session.execute_read.assert_called_once()
    
    @patch('trm_api.services.relationship_service.RelationshipService._get_db')
    def test_get_wins_from_event(self, mock_get_db):
        """Test getting Wins from an Event."""
        # Mock setup
        mock_session = MagicMock()
        mock_relationships = [Relationship(**self.event_win_relationship)]
        
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
            entity_id=self.event_id,
            entity_type=TargetEntityTypeEnum.EVENT,
            direction="outgoing",
            relationship_type="LEADS_TO_WIN",
            related_entity_type=TargetEntityTypeEnum.WIN
        )
        
        # Assertions
        assert len(results) == 1
        assert results[0].source_id == self.event_id
        assert results[0].target_id == self.win_id
        assert results[0].type == "LEADS_TO_WIN"
        
        # Verify mock was called correctly
        mock_session.execute_read.assert_called_once()
    
    @patch('trm_api.services.relationship_service.RelationshipService._get_db')
    def test_get_projects_events_leading_to_win(self, mock_get_db):
        """Test getting Projects and Events that lead to a Win."""
        # Mock setup
        mock_session = MagicMock()
        mock_relationships = [
            Relationship(**self.project_win_relationship),
            Relationship(**self.event_win_relationship)
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
            entity_id=self.win_id,
            entity_type=TargetEntityTypeEnum.WIN,
            direction="incoming",
            relationship_type="LEADS_TO_WIN"
        )
        
        # Assertions
        assert len(results) == 2
        
        # Check that we have both project and event relationships
        source_ids = [r.source_id for r in results]
        assert self.project_id in source_ids
        assert self.event_id in source_ids
        
        # Verify mock was called correctly
        mock_session.execute_read.assert_called_once()
    
    @patch('trm_api.services.relationship_service.RelationshipService._get_db')
    def test_delete_leads_to_win_relationship(self, mock_get_db):
        """Test deleting a LEADS_TO_WIN relationship."""
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
            source_id=self.project_id,
            source_type=TargetEntityTypeEnum.PROJECT,
            target_id=self.win_id,
            target_type=TargetEntityTypeEnum.WIN,
            relationship_type="LEADS_TO_WIN"
        )
        
        # Assertions
        assert result is True
        
        # Verify mock was called correctly
        mock_session.execute_write.assert_called_once()
    
    @patch('trm_api.services.relationship_service.RelationshipService._get_db')
    def test_delete_leads_to_win_relationship_not_found(self, mock_get_db):
        """Test deleting a non-existent LEADS_TO_WIN relationship."""
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
            source_id=self.project_id,
            source_type=TargetEntityTypeEnum.PROJECT,
            target_id=self.win_id,
            target_type=TargetEntityTypeEnum.WIN,
            relationship_type="LEADS_TO_WIN"
        )
        
        # Assertions
        assert result is False
        
        # Verify mock was called correctly
        mock_session.execute_write.assert_called_once()
