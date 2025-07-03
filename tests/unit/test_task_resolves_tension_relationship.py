import pytest
import uuid
import unittest
from unittest.mock import Mock, patch, MagicMock, AsyncMock
from datetime import datetime

from trm_api.models.relationships import Relationship, RelationshipType, TargetEntityTypeEnum
from trm_api.services.task_service import TaskService
from trm_api.repositories.task_repository import TaskRepository
from trm_api.repositories.tension_repository import TensionRepository


class TestTaskResolvesTensionRelationship(unittest.TestCase):
    """Unit tests for the RESOLVES relationship between Task and Tension according to Ontology V3.2."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.task_repository = TaskRepository()
        self.task_service = TaskService(repository=self.task_repository)
        
        # Sample IDs for testing
        self.task_id = str(uuid.uuid4())
        self.tension_id = str(uuid.uuid4())
        
        # Sample relationship data for Task -> Tension (RESOLVES)
        self.task_tension_relationship = {
            "source_id": self.task_id,
            "source_type": "Task",
            "target_id": self.tension_id,
            "target_type": "Tension",
            "type": "RESOLVES",
            "relationshipId": f"resolves_{self.task_id}_{self.tension_id}_{uuid.uuid4().hex[:8]}",
            "createdAt": datetime.utcnow().isoformat()
        }
        
        # Sample task data
        self.task_data = {
            "uid": self.task_id,
            "title": "Test Task for Resolving Tension",
            "description": "This is a test task created to resolve a specific tension",
            "status": "Open",
            "priority": 2,
            "estimatedEffort": 4.5,
            "dueDate": datetime.utcnow().isoformat()
        }
        
        # Sample tension data
        self.tension_data = {
            "uid": self.tension_id,
            "title": "Test Tension to be Resolved",
            "description": "This is a test tension that needs to be resolved",
            "status": "Open",
            "priority": 1,
            "source": "FounderInput"
        }
    
    @pytest.mark.asyncio
    @patch('trm_api.repositories.task_repository.db')
    async def test_connect_task_to_tension(self, mock_db):
        """Test creating a RESOLVES relationship from Task to Tension."""
        # Mock setup
        mock_transaction = AsyncMock()
        mock_db.transaction = Mock(return_value=mock_transaction)
        
        # Set up the return value for the transaction decorator
        mock_transaction.__aenter__.return_value = None
        mock_transaction.__aexit__.return_value = None
        
        # Mock the Task and Tension nodes
        mock_task = MagicMock()
        mock_task.uid = self.task_id
        
        mock_tension = MagicMock()
        mock_tension.uid = self.tension_id
        
        # Mock the Task.nodes.get method
        with patch('trm_api.repositories.task_repository.Task.nodes') as mock_task_nodes:
            mock_task_nodes.get = AsyncMock(return_value=mock_task)
            
            # Mock the Tension.nodes.get method
            with patch('trm_api.repositories.task_repository.Tension.nodes') as mock_tension_nodes:
                mock_tension_nodes.get = AsyncMock(return_value=mock_tension)
                
                # Mock the connect method on Task object
                mock_task.resolves.connect = AsyncMock()
                
                # Execute test
                result = await self.task_repository.connect_task_to_tension(
                    task_uid=self.task_id,
                    tension_uid=self.tension_id
                )
                
                # Assertions
                assert result is True
                mock_task_nodes.get.assert_awaited_once_with(uid=self.task_id)
                mock_tension_nodes.get.assert_awaited_once_with(uid=self.tension_id)
                mock_task.resolves.connect.assert_awaited_once_with(mock_tension)
    
    @pytest.mark.asyncio
    @patch('trm_api.repositories.task_repository.db')
    async def test_disconnect_task_from_tension(self, mock_db):
        """Test removing a RESOLVES relationship between Task and Tension."""
        # Mock setup
        mock_transaction = AsyncMock()
        mock_db.transaction = Mock(return_value=mock_transaction)
        
        # Set up the return value for the transaction decorator
        mock_transaction.__aenter__.return_value = None
        mock_transaction.__aexit__.return_value = None
        
        # Mock the Task and Tension nodes
        mock_task = MagicMock()
        mock_task.uid = self.task_id
        
        mock_tension = MagicMock()
        mock_tension.uid = self.tension_id
        
        # Mock the Task.nodes.get method
        with patch('trm_api.repositories.task_repository.Task.nodes') as mock_task_nodes:
            mock_task_nodes.get = AsyncMock(return_value=mock_task)
            
            # Mock the Tension.nodes.get method
            with patch('trm_api.repositories.task_repository.Tension.nodes') as mock_tension_nodes:
                mock_tension_nodes.get = AsyncMock(return_value=mock_tension)
                
                # Mock the disconnect method on Task object
                mock_task.resolves.disconnect = AsyncMock()
                
                # Execute test
                result = await self.task_repository.disconnect_task_from_tension(
                    task_uid=self.task_id,
                    tension_uid=self.tension_id
                )
                
                # Assertions
                assert result is True
                mock_task_nodes.get.assert_awaited_once_with(uid=self.task_id)
                mock_tension_nodes.get.assert_awaited_once_with(uid=self.tension_id)
                mock_task.resolves.disconnect.assert_awaited_once_with(mock_tension)
    
    @pytest.mark.asyncio
    @patch('trm_api.repositories.task_repository.db')
    async def test_get_tensions_resolved_by_task(self, mock_db):
        """Test retrieving all tensions resolved by a specific task."""
        # Mock setup
        mock_transaction = AsyncMock()
        mock_db.transaction = Mock(return_value=mock_transaction)
        
        # Set up the return value for the transaction decorator
        mock_transaction.__aenter__.return_value = None
        mock_transaction.__aexit__.return_value = None
        
        # Mock the Task node
        mock_task = MagicMock()
        mock_task.uid = self.task_id
        
        # Mock the Tension node
        mock_tension = MagicMock()
        for key, value in self.tension_data.items():
            setattr(mock_tension, key, value)
        
        # Prepare mock tensions list
        mock_tensions = [mock_tension]
        
        # Mock the Task.nodes.get method
        with patch('trm_api.repositories.task_repository.Task.nodes') as mock_task_nodes:
            mock_task_nodes.get = AsyncMock(return_value=mock_task)
            
            # Mock the resolves.all method
            mock_task.resolves.all = AsyncMock(return_value=mock_tensions)
            
            # Execute test
            result = await self.task_repository.get_tensions_resolved_by_task(
                task_uid=self.task_id,
                skip=0,
                limit=10
            )
            
            # Assertions
            assert result is not None
            assert len(result) == 1
            assert result[0].uid == self.tension_id
            mock_task_nodes.get.assert_awaited_once_with(uid=self.task_id)
            mock_task.resolves.all.assert_awaited_once()
    
    @pytest.mark.asyncio
    @patch('trm_api.repositories.task_repository.db')
    async def test_get_task_with_relationships(self, mock_db):
        """Test retrieving a task with all its relationships including tensions."""
        # Mock setup
        mock_transaction = AsyncMock()
        mock_db.transaction = Mock(return_value=mock_transaction)
        
        # Set up the return value for the transaction decorator
        mock_transaction.__aenter__.return_value = None
        mock_transaction.__aexit__.return_value = None
        
        # Mock the Task node with all attributes
        mock_task = MagicMock()
        for key, value in self.task_data.items():
            setattr(mock_task, key, value)
        
        # Mock the Tension node
        mock_tension = MagicMock()
        for key, value in self.tension_data.items():
            setattr(mock_tension, key, value)
        
        # Prepare mock tensions list
        mock_tensions = [mock_tension]
        
        # Mock the Task.nodes.get method
        with patch('trm_api.repositories.task_repository.Task.nodes') as mock_task_nodes:
            mock_task_nodes.get = AsyncMock(return_value=mock_task)
            
            # Mock various relationship methods
            mock_task.resolves.all = AsyncMock(return_value=mock_tensions)
            mock_task.task_belongs_to_project.all = AsyncMock(return_value=[])
            mock_task.created_by.all = AsyncMock(return_value=[])
            mock_task.task_assigned_to_agent.all = AsyncMock(return_value=[])
            mock_task.task_assigned_to_user.all = AsyncMock(return_value=[])
            
            # Execute test
            result = await self.task_repository.get_task_with_relationships(
                task_uid=self.task_id
            )
            
            # Assertions
            assert result is not None
            assert result['task'] == self.task_data
            assert len(result['resolves_tensions']) == 1
            assert result['resolves_tensions'][0] == self.tension_data
            mock_task_nodes.get.assert_awaited_once_with(uid=self.task_id)
            mock_task.resolves.all.assert_awaited_once()
