import pytest
import os
import sys
import json
from unittest.mock import patch, MagicMock
from datetime import datetime

# Đường dẫn tuyệt đối đến thư mục gốc của project
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)

# Import trực tiếp từ module
from tools.ontology_migration import OntologyMigrationTool

# Để tránh conflict với pytest import thông thường
class StubEntityType:
    WIN = "WIN"
    RECOGNITION = "RECOGNITION"
    TASK = "TASK"
    EVENT = "EVENT"
    KNOWLEDGE_SNIPPET = "KNOWLEDGE_SNIPPET"
    
    @classmethod
    def values(cls):
        return [cls.WIN, cls.RECOGNITION, cls.TASK, cls.EVENT, cls.KNOWLEDGE_SNIPPET]


class TestOntologyMigration:
    @pytest.fixture
    def mock_driver(self):
        with patch('neo4j.GraphDatabase.driver') as mock_driver:
            # Mock session
            mock_session = MagicMock()
            mock_driver.return_value.session.return_value.__enter__.return_value = mock_session
            
            # Mock driver.close() method
            mock_driver.return_value.close = MagicMock()
            
            yield mock_driver
    
    @pytest.fixture
    def migration_tool(self, mock_driver):
        return OntologyMigrationTool('bolt://localhost:7687', 'neo4j', 'password', 'neo4j')
    
    def test_init(self, migration_tool):
        """Kiểm tra khởi tạo đúng của OntologyMigrationTool."""
        assert migration_tool is not None
        assert hasattr(migration_tool, 'driver')
        assert hasattr(migration_tool, 'adapters')
        assert len(migration_tool.adapters) == 5  # WIN, RECOGNITION, TASK, EVENT, KNOWLEDGE_SNIPPET
        
        # Kiểm tra stats được khởi tạo đúng
        assert 'total' in migration_tool.migration_stats
        assert 'success' in migration_tool.migration_stats
        assert 'failed' in migration_tool.migration_stats
        assert 'skipped' in migration_tool.migration_stats
        assert 'entity_stats' in migration_tool.migration_stats
        
        for entity_type in StubEntityType.values():
            assert entity_type in migration_tool.migration_stats['entity_stats']
    
    def test_get_all_entities(self, migration_tool, mock_driver):
        """Kiểm tra hàm get_all_entities tạo đúng query và trả về kết quả."""
        # Mock kết quả từ Neo4j
        mock_result = [
            {
                'n': {'uid': '123', 'name': 'Test Win', 'created_at': '2023-01-01T12:00:00Z'},
                'node_id': 1
            }
        ]
        mock_driver.return_value.session.return_value.run.return_value.data.return_value = mock_result
        
        result = migration_tool.get_all_entities(StubEntityType.WIN, limit=10)
        
        # Kiểm tra kết quả trả về
        assert result == mock_result
        
        # Kiểm tra query được tạo đúng
        mock_driver.return_value.session.return_value.run.assert_called_once()
        query_arg = mock_driver.return_value.session.return_value.run.call_args[0][0]
        assert 'MATCH (n:Win)' in query_arg
        assert 'LIMIT 10' in query_arg
    
    def test_migrate_entity(self, migration_tool):
        """Kiểm tra hàm migrate_entity áp dụng đúng adapter."""
        test_data = {
            'uid': '123',
            'name': 'Test Win',
            'win_type': 'personal',  # cần chuẩn hóa thành PERSONAL
            'created_at': '2023-01-01T12:00:00',  # cần chuẩn hóa ISO format
        }
        
        # Mock adapter để theo dõi việc gọi apply_to_entity
        with patch.object(migration_tool.adapters[StubEntityType.WIN], 'apply_to_entity') as mock_apply:
            mock_apply.return_value = {
                'uid': '123',
                'name': 'Test Win',
                'win_type': 'PERSONAL',
                'created_at': '2023-01-01T12:00:00Z',
            }
            
            result = migration_tool.migrate_entity(test_data, StubEntityType.WIN)
            
            # Kiểm tra adapter được gọi với dữ liệu đúng
            mock_apply.assert_called_once_with(test_data)
            
            # Kiểm tra kết quả có chứa giá trị đã chuẩn hóa
            assert result['win_type'] == 'PERSONAL'
            assert result['created_at'] == '2023-01-01T12:00:00Z'
    
    def test_process_entity_batch_dry_run(self, migration_tool, mock_driver):
        """Kiểm tra chế độ dry_run không thực hiện thay đổi nào."""
        # Mock get_all_entities trả về 1 entity
        mock_entity = {
            'n': {'uid': '123', 'name': 'Test Win', 'win_type': 'personal'},
            'node_id': 1
        }
        
        with patch.object(migration_tool, 'get_all_entities') as mock_get_entities, \
             patch.object(migration_tool, 'migrate_entity') as mock_migrate, \
             patch.object(migration_tool, 'update_node') as mock_update:
            
            # Setup mocks
            mock_get_entities.return_value = [mock_entity]
            mock_migrate.return_value = {'uid': '123', 'name': 'Test Win', 'win_type': 'PERSONAL'}
            
            # Chạy trong dry_run mode
            migration_tool.process_entity_batch(StubEntityType.WIN, dry_run=True)
            
            # Kiểm tra update_node không được gọi trong dry_run
            mock_update.assert_not_called()
            
            # Kiểm tra stats được cập nhật
            assert migration_tool.migration_stats['total'] == 1
            assert migration_tool.migration_stats['skipped'] == 1
            assert migration_tool.migration_stats['entity_stats'][StubEntityType.WIN]['total'] == 1
    
    def test_process_entity_batch_real_run(self, migration_tool, mock_driver):
        """Kiểm tra thực thi thật sẽ cập nhật Neo4j."""
        # Mock get_all_entities trả về 1 entity
        mock_entity = {
            'n': {'uid': '123', 'name': 'Test Win', 'win_type': 'personal'},
            'node_id': 1
        }
        
        with patch.object(migration_tool, 'get_all_entities') as mock_get_entities, \
             patch.object(migration_tool, 'migrate_entity') as mock_migrate, \
             patch.object(migration_tool, 'update_node') as mock_update:
            
            # Setup mocks
            mock_get_entities.return_value = [mock_entity]
            mock_migrate.return_value = {'uid': '123', 'name': 'Test Win', 'win_type': 'PERSONAL'}
            
            # Chạy trong normal mode (không phải dry run)
            migration_tool.process_entity_batch(StubEntityType.WIN, dry_run=False)
            
            # Kiểm tra update_node được gọi
            mock_update.assert_called_once()
            
            # Kiểm tra stats được cập nhật
            assert migration_tool.migration_stats['total'] == 1
            assert migration_tool.migration_stats['success'] == 1
            assert migration_tool.migration_stats['entity_stats'][StubEntityType.WIN]['success'] == 1
    
    def test_run_migration(self, migration_tool):
        """Kiểm tra run_migration gọi process_entity_batch cho từng entity type."""
        with patch.object(migration_tool, 'process_entity_batch') as mock_process:
            entity_types = [StubEntityType.WIN, StubEntityType.TASK]
            migration_tool.run_migration(entity_types=entity_types, dry_run=True)
            
            # Kiểm tra process_entity_batch được gọi cho mỗi entity type
            assert mock_process.call_count == len(entity_types)
            
            # Kiểm tra thứ tự các cuộc gọi
            mock_process.assert_any_call(StubEntityType.WIN, True, 100)
            mock_process.assert_any_call(StubEntityType.TASK, True, 100)
