import unittest
import pytest
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

# Import các module cần thiết
from trm_api.adapters.data_adapters import DatetimeAdapter, EnumAdapter
from trm_api.models.enums import WinStatus, WinType, RecognitionStatus, TaskStatus
from trm_api.adapters.entity_adapters import WinAdapter, RecognitionAdapter, TaskAdapter


class TestAdapterIntegration(unittest.TestCase):
    """Bài kiểm tra tích hợp cho các adapter, mô phỏng luồng dữ liệu đầu-cuối."""

    def test_complex_nested_data_normalization(self):
        """Kiểm tra chuẩn hóa dữ liệu lồng nhau phức tạp với nhiều loại cấu trúc."""
        # Tạo dữ liệu mẫu phức tạp
        test_date = datetime.now(timezone.utc)
        complex_data = {
            "id": "123",
            "title": "Test WIN",
            "created_at": test_date,
            "updated_at": test_date,
            "status": WinStatus.DRAFT,  # Enum object
            "winType": WinType.BUSINESS,  # Enum object
            "metrics": [
                {"date": test_date, "value": 100},
                {"date": test_date, "value": 200}
            ],
            "related_items": {
                "tasks": [
                    {"id": "t1", "due_date": test_date, "status": "IN_PROGRESS"},
                    {"id": "t2", "due_date": test_date, "status": TaskStatus.COMPLETED}
                ],
                "events": [test_date, test_date]
            },
            "external_data": None
        }

        # Chuẩn hóa dữ liệu với adapter
        win_adapter = WinAdapter(adapt_datetime=True, adapt_enums=True)
        normalized_data = win_adapter.apply_to_entity(complex_data)

        # Kiểm tra kết quả
        # 1. Kiểm tra các trường datetime
        self.assertIsInstance(normalized_data["created_at"], str)
        self.assertTrue(normalized_data["created_at"].endswith("Z"))
        
        # 2. Kiểm tra các trường enum
        self.assertEqual(normalized_data["status"], "DRAFT")
        self.assertEqual(normalized_data["winType"], "BUSINESS")
        
        # 3. Kiểm tra dữ liệu lồng nhau
        self.assertIsInstance(normalized_data["metrics"][0]["date"], str)
        self.assertIsInstance(normalized_data["related_items"]["tasks"][0]["due_date"], str)
        self.assertEqual(normalized_data["related_items"]["tasks"][0]["status"], "IN_PROGRESS")
        self.assertEqual(normalized_data["related_items"]["tasks"][1]["status"], "COMPLETED")
        self.assertIsInstance(normalized_data["related_items"]["events"][0], str)

    def test_error_handling_invalid_enum(self):
        """Kiểm tra xử lý lỗi khi gặp giá trị enum không hợp lệ."""
        # Tạo dữ liệu với enum không hợp lệ
        invalid_data = {
            "id": "123",
            "status": "invalid_status",  # Giá trị không hợp lệ
            "created_at": datetime.now(timezone.utc)
        }

        # Thử chuẩn hóa và kiểm tra ngoại lệ
        from trm_api.adapters.enum_adapter import normalize_win_status
        
        # Kiểm tra trực tiếp với hàm chuẩn hóa enum
        try:
            value = normalize_win_status("invalid_status")
            self.fail("Expected ValueError but no exception was raised")
        except ValueError as e:
            self.assertIn("invalid_status", str(e))
            self.assertIn("not a valid", str(e))

    def test_fallback_behavior(self):
        """Kiểm tra hành vi fallback khi sử dụng fallback_value trong chuẩn hóa enum."""
        # Tạo dữ liệu với enum không hợp lệ
        invalid_data = {
            "id": "123",
            "status": "invalid_status",  # Giá trị không hợp lệ
            "created_at": datetime.now(timezone.utc)
        }

        # Test với normalize_enum_value trực tiếp với fallback_value
        from trm_api.adapters.enum_adapter import normalize_enum_value
        
        # Chuẩn hóa với fallback value
        CHOICES = {"draft": "DRAFT", "approved": "APPROVED"}
        result = normalize_enum_value("invalid_status", CHOICES, "draft")
        
        # Kiểm tra kết quả
        self.assertEqual(result, "draft")  # fallback value được sử dụng
        
        # Kiểm tra datetime vẫn được chuẩn hóa
        date_adapter = DatetimeAdapter()
        date_str = date_adapter.to_iso_format(invalid_data["created_at"])
        self.assertTrue(date_str.endswith("Z"))  # vẫn chuẩn hóa datetime

    def test_multi_entity_collection(self):
        """Kiểm tra xử lý collection với nhiều entity."""
        # Tạo collection mẫu
        test_date = datetime.now(timezone.utc)
        collection = [
            {"id": "1", "status": WinStatus.DRAFT, "created_at": test_date},
            {"id": "2", "status": WinStatus.APPROVED, "created_at": test_date},
            {"id": "3", "status": WinStatus.PENDING, "created_at": test_date},
        ]

        # Chuẩn hóa collection
        win_adapter = WinAdapter(adapt_datetime=True, adapt_enums=True)
        normalized_collection = win_adapter.apply_to_collection(collection)
        
        # Kiểm tra kết quả
        self.assertEqual(len(normalized_collection), 3)
        self.assertEqual(normalized_collection[0]["status"], "DRAFT")
        self.assertEqual(normalized_collection[1]["status"], "APPROVED")
        self.assertEqual(normalized_collection[2]["status"], "PENDING")
        
        # Kiểm tra datetime
        for item in normalized_collection:
            self.assertIsInstance(item["created_at"], str)
            self.assertTrue(item["created_at"].endswith("Z"))


if __name__ == "__main__":
    pytest.main()
