import pytest
import uuid
from unittest.mock import patch, MagicMock, AsyncMock
from datetime import datetime

from trm_api.models.relationships import Relationship, RelationshipType, TargetEntityTypeEnum
from trm_api.services.relationship_service import RelationshipService


class TestGivenByRelationship:
    """Unit tests for the GIVEN_BY relationship service methods."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.service = RelationshipService()
        
        # Sample IDs for testing
        self.agent_id = str(uuid.uuid4())
        self.recognition_id = str(uuid.uuid4())
        
        # Sample relationship data for Agent -> Recognition
        self.agent_recognition_relationship = {
            "source_id": self.agent_id,
            "source_type": "Agent",
            "target_id": self.recognition_id,
            "target_type": "Recognition",
            "type": "GIVEN_BY",
            "relationshipId": f"given_by_{self.agent_id}_{self.recognition_id}_abcd1234",
            "notes": "Test note for given recognition",
            "createdAt": datetime.utcnow()
        }
    
    @pytest.mark.asyncio
    @patch('trm_api.services.relationship_service.RelationshipService._get_db')
    async def test_create_given_by_relationship(self, mock_get_db):
        """Test creating a GIVEN_BY relationship from Agent to Recognition."""
        # Mock setup
        mock_session = MagicMock()
        mock_tx = MagicMock()
        mock_result = MagicMock()
        mock_record = MagicMock()
        
        mock_record.__getitem__.side_effect = lambda key: self.agent_recognition_relationship.get(key)
        mock_result.single.return_value = mock_record
        mock_tx.run.return_value = mock_result
        
        # Chuẩn bị mock cho async
        relationship_obj = Relationship(**self.agent_recognition_relationship)
        
        # Thiết lập mock đúng cách cho async
        mock_execute_write = AsyncMock()
        mock_execute_write.return_value = relationship_obj
        mock_session.execute_write = mock_execute_write
        
        mock_session_context = AsyncMock()
        mock_session_context.__aenter__.return_value = mock_session
        mock_session_context.__aexit__.return_value = None
        
        # Quan trọng: Cấu hình _get_db để có thể sử dụng với await
        mock_db = MagicMock()
        mock_db.session.return_value = mock_session_context
        mock_get_db.return_value = mock_db
        # Biến _get_db thành AsyncMock để có thể sử dụng với await
        mock_get_db.side_effect = AsyncMock(return_value=mock_db)
        
        # Create relationship properties
        rel_props = {
            "relationshipId": self.agent_recognition_relationship["relationshipId"],
            "notes": self.agent_recognition_relationship["notes"]
        }
        
        # Execute test with await
        result = await self.service.create_relationship(
            source_id=self.agent_id,
            source_type=TargetEntityTypeEnum.AGENT,
            target_id=self.recognition_id,
            target_type=TargetEntityTypeEnum.RECOGNITION,
            relationship_type="GIVEN_BY",
            relationship_properties=rel_props
        )
        
        # Assertions
        assert result is not None
        
        # Kiểm tra kết quả có thể là đối tượng Relationship hoặc dictionary
        if isinstance(result, dict):
            assert result["source_id"] == self.agent_id
            assert result["source_type"] == "Agent"
            assert result["target_id"] == self.recognition_id
            assert result["target_type"] == "Recognition"
            assert result["type"] == "GIVEN_BY"
        else:
            assert result.source_id == self.agent_id
            assert result.source_type == "Agent"
            assert result.target_id == self.recognition_id
            assert result.target_type == "Recognition"
            assert result.type == "GIVEN_BY"
        
        # Verify mock was called correctly
        mock_session.execute_write.assert_called_once()
    
    @pytest.mark.asyncio
    @patch('trm_api.services.relationship_service.RelationshipService._get_db')
    async def test_get_recognitions_given_by_agent(self, mock_get_db):
        """Test getting Recognitions given by an Agent."""
        # Mock setup
        mock_session = MagicMock()
        mock_relationships = [Relationship(**self.agent_recognition_relationship)]
        
        # Thiết lập mock đúng cách cho async
        mock_read_transaction = AsyncMock()
        mock_read_transaction.return_value = mock_relationships
        mock_session.read_transaction = mock_read_transaction
        
        mock_session_context = AsyncMock()
        mock_session_context.__aenter__.return_value = mock_session
        mock_session_context.__aexit__.return_value = None
        
        # Quan trọng: Cấu hình _get_db để có thể sử dụng với await
        mock_db = MagicMock()
        mock_db.session.return_value = mock_session_context
        mock_get_db.return_value = mock_db
        # Biến _get_db thành AsyncMock để có thể sử dụng với await
        mock_get_db.side_effect = AsyncMock(return_value=mock_db)
        
        # Execute test with await
        results = await self.service.get_relationships(
            entity_id=self.agent_id,
            entity_type=TargetEntityTypeEnum.AGENT,
            direction="outgoing",
            relationship_type="GIVEN_BY",
            related_entity_type=TargetEntityTypeEnum.RECOGNITION
        )
        
        # Assertions
        assert len(results) == 1
        assert results[0].source_id == self.agent_id
        assert results[0].target_id == self.recognition_id
        assert results[0].type == "GIVEN_BY"
        
        # Verify mock was called correctly
        mock_session.read_transaction.assert_called_once()
    
    @pytest.mark.asyncio
    @patch('trm_api.services.relationship_service.RelationshipService._get_db')
    async def test_get_agents_giving_recognition(self, mock_get_db):
        """Test getting Agents that gave a Recognition."""
        # Mock setup
        mock_session = MagicMock()
        mock_relationships = [Relationship(**self.agent_recognition_relationship)]
        
        # Thiết lập mock đúng cách cho async
        mock_read_transaction = AsyncMock()
        mock_read_transaction.return_value = mock_relationships
        mock_session.read_transaction = mock_read_transaction
        
        mock_session_context = AsyncMock()
        mock_session_context.__aenter__.return_value = mock_session
        mock_session_context.__aexit__.return_value = None
        
        # Quan trọng: Cấu hình _get_db để có thể sử dụng với await
        mock_db = MagicMock()
        mock_db.session.return_value = mock_session_context
        mock_get_db.return_value = mock_db
        # Biến _get_db thành AsyncMock để có thể sử dụng với await
        mock_get_db.side_effect = AsyncMock(return_value=mock_db)
        
        # Execute test with await
        results = await self.service.get_relationships(
            entity_id=self.recognition_id,
            entity_type=TargetEntityTypeEnum.RECOGNITION,
            direction="incoming",
            relationship_type="GIVEN_BY",
            related_entity_type=TargetEntityTypeEnum.AGENT
        )
        
        # Assertions
        assert len(results) == 1
        assert results[0].source_id == self.agent_id
        assert results[0].target_id == self.recognition_id
        assert results[0].type == "GIVEN_BY"
        
        # Verify mock was called correctly
        mock_session.read_transaction.assert_called_once()
    
    @pytest.mark.asyncio
    @patch('trm_api.services.relationship_service.RelationshipService._get_db')
    async def test_delete_given_by_relationship(self, mock_get_db):
        """Test deleting a GIVEN_BY relationship."""
        # Mock setup
        mock_session = MagicMock()
        mock_summary = MagicMock()
        mock_summary.counters.relationships_deleted = 1
        
        mock_result = MagicMock()
        mock_result.consume.return_value = mock_summary
        
        mock_tx = MagicMock()
        mock_tx.run.return_value = mock_result
        
        # Thiết lập mock đúng cách cho async
        mock_execute_write = AsyncMock()
        mock_execute_write.return_value = True
        mock_session.execute_write = mock_execute_write
        
        mock_session_context = AsyncMock()
        mock_session_context.__aenter__.return_value = mock_session
        mock_session_context.__aexit__.return_value = None
        
        # Quan trọng: Cấu hình _get_db để có thể sử dụng với await
        mock_db = MagicMock()
        mock_db.session.return_value = mock_session_context
        mock_get_db.return_value = mock_db
        # Biến _get_db thành AsyncMock để có thể sử dụng với await
        mock_get_db.side_effect = AsyncMock(return_value=mock_db)
        
        # Execute test with await
        result = await self.service.delete_relationship(
            source_id=self.agent_id,
            source_type=TargetEntityTypeEnum.AGENT,
            target_id=self.recognition_id,
            target_type=TargetEntityTypeEnum.RECOGNITION,
            relationship_type="GIVEN_BY"
        )
        
        # Assertions
        assert result is True
        
        # Verify mock was called correctly
        mock_session.execute_write.assert_called_once()
    
    @pytest.mark.asyncio
    @patch('trm_api.services.relationship_service.RelationshipService._get_db')
    async def test_delete_given_by_relationship_not_found(self, mock_get_db):
        """Test deleting a non-existent GIVEN_BY relationship."""
        # Mock setup
        mock_session = MagicMock()
        mock_summary = MagicMock()
        mock_summary.counters.relationships_deleted = 0
        
        mock_result = MagicMock()
        mock_result.consume.return_value = mock_summary
        
        mock_tx = MagicMock()
        mock_tx.run.return_value = mock_result
        
        # Thiết lập mock đúng cách cho async
        mock_execute_write = AsyncMock()
        mock_execute_write.return_value = False
        mock_session.execute_write = mock_execute_write
        
        mock_session_context = AsyncMock()
        mock_session_context.__aenter__.return_value = mock_session
        mock_session_context.__aexit__.return_value = None
        
        # Quan trọng: Cấu hình _get_db để có thể sử dụng với await
        mock_db = MagicMock()
        mock_db.session.return_value = mock_session_context
        mock_get_db.return_value = mock_db
        # Biến _get_db thành AsyncMock để có thể sử dụng với await
        mock_get_db.side_effect = AsyncMock(return_value=mock_db)
        
        # Execute test with await
        result = await self.service.delete_relationship(
            source_id=self.agent_id,
            source_type=TargetEntityTypeEnum.AGENT,
            target_id=self.recognition_id,
            target_type=TargetEntityTypeEnum.RECOGNITION,
            relationship_type="GIVEN_BY"
        )
        
        # Assertions
        assert result is False
        
        # Verify mock was called correctly
        mock_session.execute_write.assert_called_once()
