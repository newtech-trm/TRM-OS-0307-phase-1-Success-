import pytest
import uuid
from unittest.mock import Mock, patch, MagicMock, AsyncMock
from datetime import datetime

from trm_api.models.relationships import Relationship, RelationshipType, TargetEntityTypeEnum
from trm_api.services.relationship_service import RelationshipService
from trm_api.api.v1.endpoints.relationship import ContributionTargetTypeEnum


class TestRecognizesContributionToRelationship:
    """Unit tests for the RECOGNIZES_CONTRIBUTION_TO relationship service methods."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.service = RelationshipService()
        
        # Sample IDs for testing
        self.recognition_id = str(uuid.uuid4())
        self.project_id = str(uuid.uuid4())
        self.task_id = str(uuid.uuid4())
        self.resource_id = str(uuid.uuid4())
        
        # Sample relationship data for Recognition -> Project
        self.recognition_project_relationship = {
            "source_id": self.recognition_id,
            "source_type": "Recognition",
            "target_id": self.project_id,
            "target_type": "Project",
            "type": "RECOGNIZES_CONTRIBUTION_TO",
            "relationshipId": f"recognizes_contribution_{self.recognition_id}_{self.project_id}_abcd1234",
            "contribution_type": "Leadership",
            "contribution_level": "High",
            "impact_notes": "Significant leadership of the project",
            "createdAt": datetime.utcnow()
        }

        # Sample relationship data for Recognition -> Task
        self.recognition_task_relationship = {
            "source_id": self.recognition_id,
            "source_type": "Recognition",
            "target_id": self.task_id,
            "target_type": "Task",
            "type": "RECOGNIZES_CONTRIBUTION_TO",
            "relationshipId": f"recognizes_contribution_{self.recognition_id}_{self.task_id}_abcd1234",
            "contribution_type": "Technical",
            "contribution_level": "Medium",
            "impact_notes": "Valuable technical contribution",
            "createdAt": datetime.utcnow()
        }

        # Sample relationship data for Recognition -> Resource
        self.recognition_resource_relationship = {
            "source_id": self.recognition_id,
            "source_type": "Recognition",
            "target_id": self.resource_id,
            "target_type": "Resource",
            "type": "RECOGNIZES_CONTRIBUTION_TO",
            "relationshipId": f"recognizes_contribution_{self.recognition_id}_{self.resource_id}_abcd1234",
            "contribution_type": "Documentation",
            "contribution_level": "Medium",
            "impact_notes": "Created useful documentation",
            "createdAt": datetime.utcnow()
        }

    @pytest.mark.asyncio
    @patch('trm_api.services.relationship_service.RelationshipService._get_db')
    async def test_create_recognizes_contribution_to_project_relationship(self, mock_get_db):
        """Test creating a RECOGNIZES_CONTRIBUTION_TO relationship from Recognition to Project."""
        # Mock setup
        mock_session = MagicMock()
        mock_db = MagicMock()
        mock_tx = MagicMock()
        mock_result = MagicMock()
        mock_record = MagicMock()

        mock_record.__getitem__.side_effect = lambda key: self.recognition_project_relationship.get(key)
        mock_result.single.return_value = mock_record
        mock_tx.run.return_value = mock_result

        # Cấu hình mock để hỗ trợ async context manager
        mock_session.execute_write = AsyncMock(return_value=Relationship(**self.recognition_project_relationship))
        mock_session_ctx = MagicMock()
        mock_session_ctx.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session_ctx.__aexit__ = AsyncMock(return_value=None)
        mock_db.session.return_value = mock_session_ctx

        # Biến _get_db thành AsyncMock để có thể sử dụng với await
        mock_get_db.side_effect = AsyncMock(return_value=mock_db)

        # Create relationship properties
        rel_props = {
            "relationshipId": self.recognition_project_relationship["relationshipId"],
            "contribution_type": self.recognition_project_relationship["contribution_type"],
            "contribution_level": self.recognition_project_relationship["contribution_level"],
            "impact_notes": self.recognition_project_relationship["impact_notes"]
        }

        # Execute test
        result = await self.service.create_relationship(
            source_id=self.recognition_id,
            source_type=TargetEntityTypeEnum.RECOGNITION,
            target_id=self.project_id,
            target_type=TargetEntityTypeEnum.PROJECT,
            relationship_type="RECOGNIZES_CONTRIBUTION_TO",
            relationship_properties=rel_props
        )

        # Assertions
        assert result is not None
        assert result.source_id == self.recognition_id
        assert result.source_type == "Recognition"
        assert result.target_id == self.project_id
        assert result.target_type == "Project"
        assert result.type == "RECOGNIZES_CONTRIBUTION_TO"

        # Verify mock was called correctly
        mock_session.execute_write.assert_called_once()

    @pytest.mark.asyncio
    @patch('trm_api.services.relationship_service.RelationshipService._get_db')
    async def test_get_contributions_recognized_by_recognition(self, mock_get_db):
        """Test getting all entities that a Recognition recognizes contributions to."""
        # Mock setup
        mock_session = MagicMock()
        mock_db = MagicMock()
        mock_relationships = [
            Relationship(**self.recognition_project_relationship),
            Relationship(**self.recognition_task_relationship),
            Relationship(**self.recognition_resource_relationship)
        ]

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
            relationship_type="RECOGNIZES_CONTRIBUTION_TO"
        )

        # Assertions
        assert len(results) == 3
        assert any(rel.target_id == self.project_id and rel.target_type == "Project" for rel in results)
        assert any(rel.target_id == self.task_id and rel.target_type == "Task" for rel in results)
        assert any(rel.target_id == self.resource_id and rel.target_type == "Resource" for rel in results)

        # Verify mock was called correctly
        mock_session.read_transaction.assert_called_once()

    @pytest.mark.asyncio
    @patch('trm_api.services.relationship_service.RelationshipService._get_db')
    async def test_get_recognitions_for_project_contribution(self, mock_get_db):
        """Test getting Recognitions that recognize contributions to a Project."""
        # Mock setup
        mock_session = MagicMock()
        mock_db = MagicMock()
        mock_relationships = [Relationship(**self.recognition_project_relationship)]

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
        mock_session.read_transaction.assert_called_once()

    @pytest.mark.asyncio
    @patch('trm_api.services.relationship_service.RelationshipService._get_db')
    async def test_delete_recognizes_contribution_to_relationship(self, mock_get_db):
        """Test deleting a RECOGNIZES_CONTRIBUTION_TO relationship."""
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
            target_id=self.project_id,
            target_type=TargetEntityTypeEnum.PROJECT,
            relationship_type="RECOGNIZES_CONTRIBUTION_TO"
        )

        # Assertions
        assert result is True

        # Verify mock was called correctly
        mock_session.execute_write.assert_called_once()

    @pytest.mark.asyncio
    @patch('trm_api.services.relationship_service.RelationshipService._get_db')
    async def test_delete_recognizes_contribution_to_relationship_not_found(self, mock_get_db):
        """Test deleting a non-existent RECOGNIZES_CONTRIBUTION_TO relationship."""
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
            target_id="non-existent-id",
            target_type=TargetEntityTypeEnum.PROJECT,
            relationship_type="RECOGNIZES_CONTRIBUTION_TO"
        )

        # Assertions
        assert result is False

        # Verify mock was called correctly
        mock_session.execute_write.assert_called_once()
