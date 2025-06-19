import pytest
from datetime import datetime
from unittest.mock import Mock, patch

from trm_api.adapters.datetime_adapter import normalize_datetime, normalize_dict_datetimes, _normalize_list_items

class TestDatetimeAdapter:
    """Unit tests cho datetime_adapter module."""
    
    def test_normalize_datetime_with_none(self):
        """Test normalize_datetime với giá trị None."""
        assert normalize_datetime(None) is None
    
    def test_normalize_datetime_with_neo4j_datetime(self):
        """Test normalize_datetime với Neo4j datetime object."""
        # Tạo mock cho Neo4j datetime object
        neo4j_dt = Mock()
        neo4j_dt.to_native.return_value = datetime(2023, 1, 15, 10, 30, 0)
        
        result = normalize_datetime(neo4j_dt)
        assert result == "2023-01-15T10:30:00"
        neo4j_dt.to_native.assert_called_once()
    
    def test_normalize_datetime_with_neo4j_datetime_error(self):
        """Test normalize_datetime khi Neo4j datetime object lỗi."""
        # Mock Neo4j datetime object nhưng gây ra exception khi gọi to_native()
        neo4j_dt = Mock()
        neo4j_dt.to_native.side_effect = Exception("Neo4j datetime error")
        
        with patch("logging.error") as mock_log:
            result = normalize_datetime(neo4j_dt)
            assert result is None
            mock_log.assert_called_once()
    
    def test_normalize_datetime_with_datetime_object(self):
        """Test normalize_datetime với Python datetime object."""
        dt = datetime(2023, 1, 15, 10, 30, 0)
        result = normalize_datetime(dt)
        assert result == "2023-01-15T10:30:00"
    
    def test_normalize_datetime_with_iso_string(self):
        """Test normalize_datetime với ISO 8601 string."""
        dt_str = "2023-01-15T10:30:00Z"
        result = normalize_datetime(dt_str)
        assert result == "2023-01-15T10:30:00"
    
    def test_normalize_datetime_with_custom_format_string(self):
        """Test normalize_datetime với chuỗi có định dạng tùy chỉnh."""
        dt_str = "2023-01-15 10:30:00"
        result = normalize_datetime(dt_str)
        assert result == "2023-01-15T10:30:00"
    
    def test_normalize_datetime_with_date_only_string(self):
        """Test normalize_datetime với chuỗi chỉ chứa ngày tháng năm."""
        dt_str = "2023-01-15"
        result = normalize_datetime(dt_str)
        assert result == "2023-01-15T00:00:00"
    
    def test_normalize_datetime_with_invalid_string(self):
        """Test normalize_datetime với chuỗi không hợp lệ."""
        dt_str = "not-a-datetime"
        with patch("logging.error") as mock_log:
            result = normalize_datetime(dt_str)
            assert result is None
            mock_log.assert_called_once()
    
    def test_normalize_dict_datetimes_with_none(self):
        """Test normalize_dict_datetimes với giá trị không phải dictionary."""
        assert normalize_dict_datetimes(None) is None
    
    def test_normalize_dict_datetimes_empty_dict(self):
        """Test normalize_dict_datetimes với dictionary rỗng."""
        assert normalize_dict_datetimes({}) == {}
    
    def test_normalize_dict_datetimes_with_datetime_fields(self):
        """Test normalize_dict_datetimes với dictionary chứa trường datetime."""
        dt = datetime(2023, 1, 15, 10, 30, 0)
        data = {
            "id": "123",
            "name": "Test",
            "created_at": dt,
            "updated_at": dt
        }
        
        expected = {
            "id": "123",
            "name": "Test",
            "created_at": "2023-01-15T10:30:00",
            "updated_at": "2023-01-15T10:30:00"
        }
        
        result = normalize_dict_datetimes(data)
        assert result == expected
    
    def test_normalize_dict_datetimes_with_nested_dict(self):
        """Test normalize_dict_datetimes với dictionary lồng nhau."""
        dt = datetime(2023, 1, 15, 10, 30, 0)
        data = {
            "id": "123",
            "name": "Test",
            "metadata": {
                "created_at": dt,
                "other_field": "value"
            }
        }
        
        expected = {
            "id": "123",
            "name": "Test",
            "metadata": {
                "created_at": "2023-01-15T10:30:00",
                "other_field": "value"
            }
        }
        
        result = normalize_dict_datetimes(data)
        assert result == expected
    
    def test_normalize_dict_datetimes_with_list(self):
        """Test normalize_dict_datetimes với dictionary chứa list."""
        dt = datetime(2023, 1, 15, 10, 30, 0)
        data = {
            "id": "123",
            "records": [
                {"id": "1", "created_at": dt},
                {"id": "2", "created_at": dt}
            ]
        }
        
        expected = {
            "id": "123",
            "records": [
                {"id": "1", "created_at": "2023-01-15T10:30:00"},
                {"id": "2", "created_at": "2023-01-15T10:30:00"}
            ]
        }
        
        result = normalize_dict_datetimes(data)
        assert result == expected
        
    def test_normalize_dict_datetimes_with_deeply_nested_structure(self):
        """Test normalize_dict_datetimes với cấu trúc lồng sâu phức tạp."""
        dt = datetime(2023, 1, 15, 10, 30, 0)
        data = {
            "id": "123",
            "metadata": {
                "created": dt,
                "stats": {
                    "last_updated": dt,
                    "history": [
                        {"date": dt, "user": "admin"},
                        {"date": dt, "user": "system"}
                    ]
                }
            },
            "related_items": [
                {
                    "id": "item-1",
                    "timestamps": {
                        "created": dt,
                        "modified": dt
                    },
                    "tags": ["tag1", "tag2"]
                },
                {
                    "id": "item-2",
                    "timestamps": {
                        "created": dt,
                        "sub_dates": [dt, dt]
                    }
                }
            ]
        }
        
        expected = {
            "id": "123",
            "metadata": {
                "created": "2023-01-15T10:30:00",
                "stats": {
                    "last_updated": "2023-01-15T10:30:00",
                    "history": [
                        {"date": "2023-01-15T10:30:00", "user": "admin"},
                        {"date": "2023-01-15T10:30:00", "user": "system"}
                    ]
                }
            },
            "related_items": [
                {
                    "id": "item-1",
                    "timestamps": {
                        "created": "2023-01-15T10:30:00",
                        "modified": "2023-01-15T10:30:00"
                    },
                    "tags": ["tag1", "tag2"]
                },
                {
                    "id": "item-2",
                    "timestamps": {
                        "created": "2023-01-15T10:30:00",
                        "sub_dates": ["2023-01-15T10:30:00", "2023-01-15T10:30:00"]
                    }
                }
            ]
        }
        
        result = normalize_dict_datetimes(data)
        assert result == expected
    
    def test_normalize_dict_datetimes_with_max_depth(self):
        """Test normalize_dict_datetimes với max_depth."""
        dt = datetime(2023, 1, 15, 10, 30, 0)
        data = {
            "id": "123",
            "created_at": dt,
            "metadata": {
                "updated_at": dt,
                "nested": {
                    "deep_date": dt
                }
            }
        }
        
        # Với max_depth=1, chỉ các trường ở mức đầu tiên sẽ được chuẩn hóa
        expected = {
            "id": "123",
            "created_at": "2023-01-15T10:30:00",
            "metadata": {
                "updated_at": dt,  # Không được chuẩn hóa
                "nested": {
                    "deep_date": dt  # Không được chuẩn hóa
                }
            }
        }
        
        result = normalize_dict_datetimes(data, max_depth=1)
        assert result == expected
        
        # Với max_depth=2, các trường ở mức thứ hai cũng được chuẩn hóa
        expected = {
            "id": "123",
            "created_at": "2023-01-15T10:30:00",
            "metadata": {
                "updated_at": "2023-01-15T10:30:00",
                "nested": {
                    "deep_date": dt  # Vẫn không được chuẩn hóa
                }
            }
        }
        
        result = normalize_dict_datetimes(data, max_depth=2)
        assert result == expected
    
    def test_normalize_list_items(self):
        """Test hàm _normalize_list_items."""
        dt = datetime(2023, 1, 15, 10, 30, 0)
        
        # Danh sách các dictionary
        data = [
            {"id": "1", "date": dt},
            {"id": "2", "date": dt}
        ]
        
        expected = [
            {"id": "1", "date": "2023-01-15T10:30:00"},
            {"id": "2", "date": "2023-01-15T10:30:00"}
        ]
        
        result = _normalize_list_items(data)
        assert result == expected
        
        # Danh sách các datetime
        data = [dt, dt]
        expected = ["2023-01-15T10:30:00", "2023-01-15T10:30:00"]
        
        result = _normalize_list_items(data)
        assert result == expected
        
        # Danh sách hỗn hợp
        data = [
            dt,
            {"date": dt},
            "string",
            123,
            None
        ]
        
        expected = [
            "2023-01-15T10:30:00",
            {"date": "2023-01-15T10:30:00"},
            "string",
            123,
            None
        ]
        
        result = _normalize_list_items(data)
        assert result == expected
    
    def test_normalize_dict_datetimes_with_neo4j_datetime(self):
        """Test normalize_dict_datetimes với Neo4j datetime object."""
        # Tạo mock cho Neo4j datetime object
        neo4j_dt = Mock()
        neo4j_dt.to_native.return_value = datetime(2023, 1, 15, 10, 30, 0)
        
        data = {
            "id": "123",
            "created_at": neo4j_dt,
            "records": [
                {"date": neo4j_dt}
            ]
        }
        
        expected = {
            "id": "123",
            "created_at": "2023-01-15T10:30:00",
            "records": [
                {"date": "2023-01-15T10:30:00"}
            ]
        }
        
        result = normalize_dict_datetimes(data)
        assert result == expected
        # Verify to_native was called twice (once for each datetime)
        assert neo4j_dt.to_native.call_count == 2
