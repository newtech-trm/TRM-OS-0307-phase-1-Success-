import unittest
import pytest
from datetime import datetime, timezone
from enum import Enum

from trm_api.adapters.data_adapters import DatetimeAdapter, EnumAdapter, BaseEntityAdapter
from trm_api.adapters.entity_adapters import WinAdapter, RecognitionAdapter, TaskAdapter, get_entity_adapter
from trm_api.models.enums import WinStatus, WinType, RecognitionStatus, TaskStatus


class TestDatetimeAdapter(unittest.TestCase):
    """Unit test cho DatetimeAdapter."""
    
    def test_to_iso_format(self):
        """Test chuyển đổi datetime sang ISO format."""
        now = datetime.now(timezone.utc)
        iso_str = DatetimeAdapter.to_iso_format(now)
        self.assertIsInstance(iso_str, str)
        self.assertTrue(iso_str.endswith('Z'))
        
    def test_normalize_datetime_field(self):
        """Test chuẩn hóa trường datetime trong entity."""
        now = datetime.now(timezone.utc)
        entity = {
            'created_at': now,
            'updated_at': now,
            'name': 'Test Entity'
        }
        
        result = DatetimeAdapter.normalize_datetime_field(entity, 'created_at')
        
        self.assertIsInstance(result['created_at'], str)
        self.assertTrue(result['created_at'].endswith('Z'))
        
    def test_normalize_dict_datetimes(self):
        """Test chuẩn hóa tất cả các datetime trong dictionary."""
        now = datetime.now(timezone.utc)
        entity = {
            'created_at': now,
            'updated_at': now,
            'name': 'Test Entity',
            'nested': {
                'datetime_field': now
            },
            'list_fields': [
                {'datetime_field': now},
                {'string_field': 'value'}
            ]
        }
        
        result = DatetimeAdapter.normalize_dict_datetimes(entity)
        
        self.assertIsInstance(result['created_at'], str)
        self.assertIsInstance(result['updated_at'], str)
        self.assertIsInstance(result['nested']['datetime_field'], str)
        self.assertIsInstance(result['list_fields'][0]['datetime_field'], str)
        
    def test_none_values(self):
        """Test xử lý None values."""
        entity = {
            'created_at': None,
            'name': 'Test Entity'
        }
        
        result = DatetimeAdapter.normalize_datetime_field(entity, 'created_at')
        self.assertIsNone(result['created_at'])
        
        result = DatetimeAdapter.normalize_dict_datetimes(entity)
        self.assertIsNone(result['created_at'])


class TestEnumAdapter(unittest.TestCase):
    """Unit test cho EnumAdapter."""
    
    def test_normalize_enum_value(self):
        """Test chuẩn hóa các giá trị enum."""
        # Test với WinStatus enum
        self.assertEqual(EnumAdapter.normalize_enum_value(WinStatus, 'draft'), WinStatus.DRAFT.value)
        self.assertEqual(EnumAdapter.normalize_enum_value(WinStatus, 'DRAFT'), WinStatus.DRAFT.value)
        self.assertEqual(EnumAdapter.normalize_enum_value(WinStatus, 'Draft'), WinStatus.DRAFT.value)
        
        # Test với giá trị không tồn tại
        with self.assertRaises(ValueError):
            EnumAdapter.normalize_enum_value(WinStatus, 'unknown_status')
            
    def test_normalize_field(self):
        """Test chuẩn hóa trường enum trong entity."""
        entity = {
            'status': 'draft',
            'name': 'Test Win'
        }
        
        result = EnumAdapter.normalize_field(entity, 'status', WinStatus)
        self.assertEqual(result['status'], WinStatus.DRAFT.value)
        
        # Test với trường không tồn tại
        entity = {'name': 'Test Win'}
        result = EnumAdapter.normalize_field(entity, 'status', WinStatus)
        self.assertEqual(result, entity)  # Không thay đổi
        
    def test_normalize_field_with_fallback(self):
        """Test chuẩn hóa với fallback value."""
        entity = {'status': 'invalid_status'}
        
        # Không có fallback, nên sẽ raise ValueError
        with self.assertRaises(ValueError):
            EnumAdapter.normalize_field(entity, 'status', WinStatus)
            
        # Có fallback
        result = EnumAdapter.normalize_field(
            entity, 'status', WinStatus, 
            fallback_value=WinStatus.DRAFT.value
        )
        self.assertEqual(result['status'], WinStatus.DRAFT.value)


class TestBaseEntityAdapter(unittest.TestCase):
    """Unit test cho BaseEntityAdapter."""
    
    def test_apply_to_entity(self):
        """Test áp dụng adapter cho một entity."""
        now = datetime.now(timezone.utc)
        entity = {
            'created_at': now,
            'updated_at': now,
            'name': 'Test Entity'
        }
        
        adapter = BaseEntityAdapter(adapt_datetime=True, adapt_enums=False)
        result = adapter.apply_to_entity(entity)
        
        self.assertIsInstance(result['created_at'], str)
        self.assertIsInstance(result['updated_at'], str)
        
    def test_apply_to_collection(self):
        """Test áp dụng adapter cho một collection entities."""
        now = datetime.now(timezone.utc)
        entities = [
            {
                'created_at': now,
                'name': 'Entity 1'
            },
            {
                'created_at': now,
                'name': 'Entity 2'
            }
        ]
        
        adapter = BaseEntityAdapter(adapt_datetime=True, adapt_enums=False)
        results = adapter.apply_to_collection(entities)
        
        for result in results:
            self.assertIsInstance(result['created_at'], str)


class TestWinAdapter(unittest.TestCase):
    """Unit test cho WinAdapter."""
    
    def test_apply_enum_adapters(self):
        """Test áp dụng enum adapters cho Win entity."""
        win = {
            'status': 'draft',
            'winType': 'business',
            'name': 'Test Win'
        }
        
        adapter = WinAdapter(adapt_datetime=False, adapt_enums=True)
        result = adapter._apply_enum_adapters(win)
        
        self.assertEqual(result['status'], WinStatus.DRAFT.value)
        self.assertEqual(result['winType'], WinType.BUSINESS.value)


class TestEntityAdapterFactory(unittest.TestCase):
    """Unit test cho Factory method get_entity_adapter."""
    
    def test_get_win_adapter(self):
        """Test lấy Win adapter."""
        adapter = get_entity_adapter('win')
        self.assertIsInstance(adapter, WinAdapter)
        
    def test_get_task_adapter(self):
        """Test lấy Task adapter."""
        adapter = get_entity_adapter('task')
        self.assertIsInstance(adapter, TaskAdapter)
        
    def test_get_recognition_adapter(self):
        """Test lấy Recognition adapter."""
        adapter = get_entity_adapter('recognition')
        self.assertIsInstance(adapter, RecognitionAdapter)
        
    def test_unknown_entity_type(self):
        """Test với entity type không biết."""
        adapter = get_entity_adapter('unknown')
        self.assertIsInstance(adapter, BaseEntityAdapter)


if __name__ == '__main__':
    unittest.main()
