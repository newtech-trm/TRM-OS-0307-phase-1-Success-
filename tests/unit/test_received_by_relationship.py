import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime

from trm_api.services.relationship_service import RelationshipService
from trm_api.models.relationships import Relationship, TargetEntityTypeEnum


class TestReceivedByRelationship:
    """Test cases for RECEIVED_BY relationship between Recognition and Agent."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.service = RelationshipService()
        self.recognition_id = "recognition-123"
        self.agent_id = "agent-456"
        
        # Sample relationship data
        self.recognition_agent_relationship = {
            "source_id": self.recognition_id,
            "source_type": "Recognition",
            "target_id": self.agent_id,
            "target_type": "Agent",
            "type": "RECEIVED_BY",
            "createdAt": datetime.now(),
            "relationshipId": "rel-789",
            "notes": "Recognition received by agent"
        }
    
    @patch('trm_api.services.relationship_service.RelationshipService._get_db')
    def test_create_received_by_relationship(self, mock_get_db):
        """Test creating a RECEIVED_BY relationship from Recognition to Agent."""
        # Mock setup
        mock_session = MagicMock()
        mock_tx = MagicMock()
        mock_result = MagicMock()
        mock_record = MagicMock()
        
        mock_record.__getitem__.side_effect = lambda key: self.recognition_agent_relationship.get(key)
        mock_result.single.return_value = mock_record
        mock_tx.run.return_value = mock_result
        
        # Chuẩn bị mock cho sync
        relationship_obj = Relationship(**self.recognition_agent_relationship)
        
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
            "relationshipId": self.recognition_agent_relationship["relationshipId"],
            "notes": self.recognition_agent_relationship["notes"]
        }
        
        # Execute test without await
        result = self.service.create_relationship(
            source_id=self.recognition_id,
            source_type=TargetEntityTypeEnum.RECOGNITION,
            target_id=self.agent_id,
            target_type=TargetEntityTypeEnum.AGENT,
            relationship_type="RECEIVED_BY",
            relationship_properties=rel_props
        )
        
        # Assertions
        assert result is not None
        
        # Kiểm tra kết quả có thể là đối tượng Relationship hoặc dictionary
        if isinstance(result, dict):
            assert result["source_id"] == self.recognition_id
            assert result["source_type"] == "Recognition"
            assert result["target_id"] == self.agent_id
            assert result["target_type"] == "Agent"
            assert result["type"] == "RECEIVED_BY"
        else:
            assert result.source_id == self.recognition_id
            assert result.source_type == "Recognition"
            assert result.target_id == self.agent_id
            assert result.target_type == "Agent"
            assert result.type == "RECEIVED_BY"
        
        # Verify mock was called correctly
        mock_session.execute_write.assert_called_once()
    
    @patch('trm_api.services.relationship_service.RelationshipService._get_db')
    def test_get_agents_receiving_recognition(self, mock_get_db):
        """Test getting Agents receiving a Recognition."""
        # Mock setup
        mock_session = MagicMock()
        mock_relationships = [Relationship(**self.recognition_agent_relationship)]
        
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
            relationship_type="RECEIVED_BY",
            related_entity_type=TargetEntityTypeEnum.AGENT
        )
        
        # Assertions
        assert len(results) == 1
        assert results[0].source_id == self.recognition_id
        assert results[0].target_id == self.agent_id
        assert results[0].type == "RECEIVED_BY"
        
        # Verify mock was called correctly
        mock_session.execute_read.assert_called_once()
    
    @patch('trm_api.services.relationship_service.RelationshipService._get_db')
    def test_get_recognitions_received_by_agent(self, mock_get_db):
        """Test getting Recognitions received by an Agent."""
        # Mock setup
        mock_session = MagicMock()
        mock_relationships = [Relationship(**self.recognition_agent_relationship)]
        
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
            entity_id=self.agent_id,
            entity_type=TargetEntityTypeEnum.AGENT,
            direction="incoming",
            relationship_type="RECEIVED_BY",
            related_entity_type=TargetEntityTypeEnum.RECOGNITION
        )
        
        # Assertions
        assert len(results) == 1
        assert results[0].source_id == self.recognition_id
        assert results[0].target_id == self.agent_id
        assert results[0].type == "RECEIVED_BY"
        
        # Verify mock was called correctly
        mock_session.execute_read.assert_called_once()
    
    @patch('trm_api.services.relationship_service.RelationshipService._get_db')
    def test_delete_received_by_relationship(self, mock_get_db):
        """Test deleting a RECEIVED_BY relationship."""
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
            target_id=self.agent_id,
            target_type=TargetEntityTypeEnum.AGENT,
            relationship_type="RECEIVED_BY"
        )
        
        # Assertions
        assert result is True
        
        # Verify mock was called correctly
        mock_session.execute_write.assert_called_once()
    
    @patch('trm_api.services.relationship_service.RelationshipService._get_db')
    def test_delete_received_by_relationship_not_found(self, mock_get_db):
        """Test deleting a non-existent RECEIVED_BY relationship."""
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
            target_id=self.agent_id,
            target_type=TargetEntityTypeEnum.AGENT,
            relationship_type="RECEIVED_BY"
        )
        
        # Assertions
        assert result is False
        
        # Verify mock was called correctly
        mock_session.execute_write.assert_called_once()
