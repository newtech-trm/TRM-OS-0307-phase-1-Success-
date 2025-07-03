import pytest
import uuid
import unittest
from unittest.mock import Mock, patch, MagicMock, AsyncMock
from datetime import datetime

from trm_api.models.relationships import Relationship, RelationshipType, TargetEntityTypeEnum
from trm_api.services.tension_service import TensionService
from trm_api.repositories.tension_repository import TensionRepository


class TestTensionLeadsToWinRelationship(unittest.TestCase):
    """Unit tests for the LEADS_TO_WIN relationship between Tension and WIN according to Ontology V3.2."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.tension_repository = TensionRepository()
        self.tension_service = TensionService(repository=self.tension_repository)
        
        # Sample IDs for testing
        self.tension_id = str(uuid.uuid4())
        self.win_id = str(uuid.uuid4())
        
        # Sample relationship data for Tension -> WIN
        self.tension_win_relationship = {
            "source_id": self.tension_id,
            "source_type": "Tension",
            "target_id": self.win_id,
            "target_type": "Win",
            "type": "LEADS_TO_WIN",
            "relationshipId": f"leads_to_win_{self.tension_id}_{self.win_id}_{uuid.uuid4().hex[:8]}",
            "contributionLevel": 3,
            "directContribution": True,
            "createdAt": datetime.utcnow().isoformat()
        }
        
        # Sample tension data
        self.tension_data = {
            "uid": self.tension_id,
            "title": "Test Tension Leading to WIN",
            "description": "This is a test tension that leads to a specific WIN",
            "status": "Open",
            "priority": 2,
            "source": "FounderInput",
            "tensionType": "Opportunity"
        }
        
        # Sample WIN data
        self.win_data = {
            "uid": self.win_id,
            "title": "Test WIN from Tension",
            "description": "This is a test WIN that resulted from a tension",
            "impact": "High",
            "category": "Strategic",
            "valueCreated": 10000
        }
    
    @pytest.mark.asyncio
    @patch('trm_api.repositories.tension_repository.db')
    async def test_connect_tension_to_win(self, mock_db):
        """Test creating a LEADS_TO_WIN relationship from Tension to WIN."""
        # Mock setup
        mock_transaction = AsyncMock()
        mock_db.transaction = Mock(return_value=mock_transaction)
        
        # Set up the return value for the transaction decorator
        mock_transaction.__aenter__.return_value = None
        mock_transaction.__aexit__.return_value = None
        
        # Mock the Tension and WIN nodes
        mock_tension = MagicMock()
        mock_tension.uid = self.tension_id
        
        mock_win = MagicMock()
        mock_win.uid = self.win_id
        
        # Mock the Tension.nodes.get method
        with patch('trm_api.repositories.tension_repository.Tension.nodes') as mock_tension_nodes:
            mock_tension_nodes.get = AsyncMock(return_value=mock_tension)
            
            # Mock the WIN.nodes.get method
            with patch('trm_api.repositories.tension_repository.WIN.nodes') as mock_win_nodes:
                mock_win_nodes.get = AsyncMock(return_value=mock_win)
                
                # Mock the connect method on Tension object
                mock_tension.leads_to_win.connect = AsyncMock()
                
                # Execute test
                result = await self.tension_repository.connect_tension_to_win(
                    tension_uid=self.tension_id,
                    win_uid=self.win_id,
                    contribution_level=self.tension_win_relationship["contributionLevel"],
                    direct_contribution=self.tension_win_relationship["directContribution"]
                )
                
                # Assertions
                assert result is True
                mock_tension_nodes.get.assert_awaited_once_with(uid=self.tension_id)
                mock_win_nodes.get.assert_awaited_once_with(uid=self.win_id)
                mock_tension.leads_to_win.connect.assert_awaited_once()
    
    @pytest.mark.asyncio
    @patch('trm_api.repositories.tension_repository.db')
    async def test_disconnect_tension_from_win(self, mock_db):
        """Test removing a LEADS_TO_WIN relationship between Tension and WIN."""
        # Mock setup
        mock_transaction = AsyncMock()
        mock_db.transaction = Mock(return_value=mock_transaction)
        
        # Set up the return value for the transaction decorator
        mock_transaction.__aenter__.return_value = None
        mock_transaction.__aexit__.return_value = None
        
        # Mock the Tension and WIN nodes
        mock_tension = MagicMock()
        mock_tension.uid = self.tension_id
        
        mock_win = MagicMock()
        mock_win.uid = self.win_id
        
        # Mock the Tension.nodes.get method
        with patch('trm_api.repositories.tension_repository.Tension.nodes') as mock_tension_nodes:
            mock_tension_nodes.get = AsyncMock(return_value=mock_tension)
            
            # Mock the WIN.nodes.get method
            with patch('trm_api.repositories.tension_repository.WIN.nodes') as mock_win_nodes:
                mock_win_nodes.get = AsyncMock(return_value=mock_win)
                
                # Mock the disconnect method on Tension object
                mock_tension.leads_to_win.disconnect = AsyncMock()
                
                # Execute test
                result = await self.tension_repository.disconnect_tension_from_win(
                    tension_uid=self.tension_id,
                    win_uid=self.win_id
                )
                
                # Assertions
                assert result is True
                mock_tension_nodes.get.assert_awaited_once_with(uid=self.tension_id)
                mock_win_nodes.get.assert_awaited_once_with(uid=self.win_id)
                mock_tension.leads_to_win.disconnect.assert_awaited_once()
    
    @pytest.mark.asyncio
    @patch('trm_api.repositories.tension_repository.db')
    async def test_get_wins_from_tension(self, mock_db):
        """Test retrieving all WINs that are led to by a specific tension."""
        # Mock setup
        mock_transaction = AsyncMock()
        mock_db.transaction = Mock(return_value=mock_transaction)
        
        # Set up the return value for the transaction decorator
        mock_transaction.__aenter__.return_value = None
        mock_transaction.__aexit__.return_value = None
        
        # Mock the Tension node
        mock_tension = MagicMock()
        mock_tension.uid = self.tension_id
        
        # Mock the WIN node
        mock_win = MagicMock()
        for key, value in self.win_data.items():
            setattr(mock_win, key, value)
        
        # Prepare mock wins list
        mock_wins = [mock_win]
        
        # Mock the Tension.nodes.get method
        with patch('trm_api.repositories.tension_repository.Tension.nodes') as mock_tension_nodes:
            mock_tension_nodes.get = AsyncMock(return_value=mock_tension)
            
            # Mock the leads_to_win.all method
            mock_tension.leads_to_win.all = AsyncMock(return_value=mock_wins)
            
            # Execute test
            result = await self.tension_repository.get_wins_from_tension(
                tension_uid=self.tension_id,
                skip=0,
                limit=10
            )
            
            # Assertions
            assert result is not None
            assert len(result) == 1
            assert result[0].uid == self.win_id
            mock_tension_nodes.get.assert_awaited_once_with(uid=self.tension_id)
            mock_tension.leads_to_win.all.assert_awaited_once()
    
    @pytest.mark.asyncio
    @patch('trm_api.repositories.tension_repository.db')
    async def test_get_tension_with_relationships(self, mock_db):
        """Test retrieving a tension with all its relationships including WINs."""
        # Mock setup
        mock_transaction = AsyncMock()
        mock_db.transaction = Mock(return_value=mock_transaction)
        
        # Set up the return value for the transaction decorator
        mock_transaction.__aenter__.return_value = None
        mock_transaction.__aexit__.return_value = None
        
        # Mock the Tension node with all attributes
        mock_tension = MagicMock()
        for key, value in self.tension_data.items():
            setattr(mock_tension, key, value)
        
        # Mock the WIN node
        mock_win = MagicMock()
        for key, value in self.win_data.items():
            setattr(mock_win, key, value)
        
        # Prepare mock wins list
        mock_wins = [mock_win]
        
        # Mock the Tension.nodes.get method
        with patch('trm_api.repositories.tension_repository.Tension.nodes') as mock_tension_nodes:
            mock_tension_nodes.get = AsyncMock(return_value=mock_tension)
            
            # Mock various relationship methods
            mock_tension.leads_to_win.all = AsyncMock(return_value=mock_wins)
            mock_tension.reported_by.all = AsyncMock(return_value=[])
            mock_tension.owned_by.all = AsyncMock(return_value=[])
            mock_tension.affects.all = AsyncMock(return_value=[])
            mock_tension.resolved_by_tasks.all = AsyncMock(return_value=[])
            mock_tension.resolved_by_projects.all = AsyncMock(return_value=[])
            
            # Execute test
            result = await self.tension_repository.get_tension_with_relationships(
                tension_uid=self.tension_id
            )
            
            # Assertions
            assert result is not None
            assert result['tension'] == self.tension_data
            assert len(result['leads_to_wins']) == 1
            assert result['leads_to_wins'][0] == self.win_data
            mock_tension_nodes.get.assert_awaited_once_with(uid=self.tension_id)
            mock_tension.leads_to_win.all.assert_awaited_once()
