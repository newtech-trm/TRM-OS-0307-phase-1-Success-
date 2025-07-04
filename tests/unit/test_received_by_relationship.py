import pytest
import uuid
from unittest.mock import Mock, patch, MagicMock, AsyncMock
from datetime import datetime

from trm_api.models.relationships import Relationship, RelationshipType, TargetEntityTypeEnum
from trm_api.services.relationship_service import RelationshipService


class TestReceivedByRelationship:
    """Unit tests for the RECEIVED_BY relationship service methods."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.service = RelationshipService()
        
        # Sample IDs for testing
        self.recognition_id = str(uuid.uuid4())
        self.agent_id = str(uuid.uuid4())
        
        # Sample relationship data for Recognition -> Agent
        self.recognition_agent_relationship = {
            "source_id": self.recognition_id,
            "source_type": "Recognition",
            "target_id": self.agent_id,
            "target_type": "Agent",
            "type": "RECEIVED_BY",
            "relationshipId": f"received_by_{self.recognition_id}_{self.agent_id}_abcd1234",
            "notes": "Test note for received recognition",
            "createdAt": datetime.utcnow()
        }
    
    @pytest.mark.asyncio
    @patch('trm_api.services.relationship_service.RelationshipService._get_db')
    async def test_create_received_by_relationship(self, mock_get_db):
        """Test creating a RECEIVED_BY relationship from Recognition to Agent."""
        # Mock setup
        mock_session = MagicMock()
        mock_db = MagicMock()
        mock_tx = MagicMock()
        mock_result = MagicMock()
        mock_record = MagicMock()
        
        mock_record.__getitem__.side_effect = lambda key: self.recognition_agent_relationship.get(key)
        mock_result.single.return_value = mock_record
        mock_tx.run.return_value = mock_result
        
        # Cấu hình mock để hỗ trợ async context manager
        mock_session.execute_write = AsyncMock(return_value=Relationship(**self.recognition_agent_relationship))
        mock_session_ctx = MagicMock()
        mock_session_ctx.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session_ctx.__aexit__ = AsyncMock(return_value=None)
        mock_db.session.return_value = mock_session_ctx
        
        # Biến _get_db thành AsyncMock để có thể sử dụng với await
        mock_get_db.side_effect = AsyncMock(return_value=mock_db)
        
        # Create relationship properties
        rel_props = {
            "relationshipId": self.recognition_agent_relationship["relationshipId"],
            "notes": self.recognition_agent_relationship["notes"]
        }
        
        # Execute test
        result = await self.service.create_relationship(
            source_id=self.recognition_id,
            source_type=TargetEntityTypeEnum.RECOGNITION,
            target_id=self.agent_id,
            target_type=TargetEntityTypeEnum.AGENT,
            relationship_type="RECEIVED_BY",
            relationship_properties=rel_props
        )
        
        # Assertions
        assert result is not None
        assert result.source_id == self.recognition_id
        assert result.source_type == "Recognition"
        assert result.target_id == self.agent_id
        assert result.target_type == "Agent"
        assert result.type == "RECEIVED_BY"
        
        # Verify mock was called correctly
        mock_session.execute_write.assert_called_once()
    
    @pytest.mark.asyncio
    @patch('trm_api.services.relationship_service.RelationshipService._get_db')
    async def test_get_agents_receiving_recognition(self, mock_get_db):
        """Test getting Agents that received a Recognition."""
        # Mock setup
        mock_session = MagicMock()
        mock_db = MagicMock()
        mock_relationships = [Relationship(**self.recognition_agent_relationship)]
        
        # Cấu hình mock để hỗ trợ async context manager
        mock_session.read_transaction = AsyncMock(return_value=mock_relationships)
        mock_session_ctx = MagicMock()
        mock_session_ctx.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session_ctx.__aexit__ = AsyncMock(return_value=None)
        mock_db.session.return_value = mock_session_ctx
        
        # Biến _get_db thành AsyncMock để có thể sử dụng với await
        mock_get_db.side_effect = AsyncMock(return_value=mock_db)
        
        # Execute test
        results = await self.service.get_relationships(
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
        mock_session.read_transaction.assert_called_once()
    
    @pytest.mark.asyncio
    @patch('trm_api.services.relationship_service.RelationshipService._get_db')
    async def test_get_recognitions_received_by_agent(self, mock_get_db):
        """Test getting Recognitions received by an Agent."""
        # Mock setup
        mock_session = MagicMock()
        mock_db = MagicMock()
        mock_relationships = [Relationship(**self.recognition_agent_relationship)]
        
        # Cấu hình mock để hỗ trợ async context manager
        mock_session.read_transaction = AsyncMock(return_value=mock_relationships)
        mock_session_ctx = MagicMock()
        mock_session_ctx.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session_ctx.__aexit__ = AsyncMock(return_value=None)
        mock_db.session.return_value = mock_session_ctx
        
        # Biến _get_db thành AsyncMock để có thể sử dụng với await
        mock_get_db.side_effect = AsyncMock(return_value=mock_db)
        
        # Execute test
        results = await self.service.get_relationships(
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
        mock_session.read_transaction.assert_called_once()
    
    @pytest.mark.asyncio
    @patch('trm_api.services.relationship_service.RelationshipService._get_db')
    async def test_delete_received_by_relationship(self, mock_get_db):
        """Test deleting a RECEIVED_BY relationship."""
        # Mock setup
        mock_session = MagicMock()
        mock_db = MagicMock()
        mock_summary = MagicMock()
        mock_summary.counters.relationships_deleted = 1
        
        mock_result = MagicMock()
        mock_result.consume.return_value = mock_summary
        
        mock_tx = MagicMock()
        mock_tx.run.return_value = mock_result
        
        # Cấu hình mock để hỗ trợ async context manager
        mock_session.execute_write = AsyncMock(return_value=True)
        mock_session_ctx = MagicMock()
        mock_session_ctx.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session_ctx.__aexit__ = AsyncMock(return_value=None)
        mock_db.session.return_value = mock_session_ctx
        
        # Biến _get_db thành AsyncMock để có thể sử dụng với await
        mock_get_db.side_effect = AsyncMock(return_value=mock_db)
        
        # Execute test
        result = await self.service.delete_relationship(
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
    
    @pytest.mark.asyncio
    @patch('trm_api.services.relationship_service.RelationshipService._get_db')
    async def test_delete_received_by_relationship_not_found(self, mock_get_db):
        """Test deleting a non-existent RECEIVED_BY relationship."""
        # Mock setup
        mock_session = MagicMock()
        mock_db = MagicMock()
        mock_summary = MagicMock()
        mock_summary.counters.relationships_deleted = 0
        
        mock_result = MagicMock()
        mock_result.consume.return_value = mock_summary
        
        mock_tx = MagicMock()
        mock_tx.run.return_value = mock_result
        
        # Cấu hình mock để hỗ trợ async context manager
        mock_session.execute_write = AsyncMock(return_value=False)
        mock_session_ctx = MagicMock()
        mock_session_ctx.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session_ctx.__aexit__ = AsyncMock(return_value=None)
        mock_db.session.return_value = mock_session_ctx
        
        # Biến _get_db thành AsyncMock để có thể sử dụng với await
        mock_get_db.side_effect = AsyncMock(return_value=mock_db)
        
        # Execute test
        result = await self.service.delete_relationship(
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
