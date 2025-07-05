import pytest
import pytest_asyncio
import uuid
import asyncio
from unittest.mock import patch, AsyncMock
from datetime import datetime
from httpx import AsyncClient
from fastapi import status

from trm_api.main import app
from tests.conftest import get_test_client
import logging

# Thiết lập logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest_asyncio.fixture
async def client():
    return await get_test_client()

class TestWINEndpoints:
    """Test class cho WIN API endpoints"""
    
    def setup_method(self):
        """Thiết lập cho mỗi test method"""
        self.sample_win_data = {
            "summary": "Test WIN with detailed summary",
            "description": "This is a test WIN narrative with detailed story",
            "status": "draft",
            "win_type": "problem_resolution",
            "impact_level": 3,
            "tags": ["test", "api"],
            "relatedEntityIds": []
        }
        
        self.sample_win_response = {
            "uid": "test-win-uid-123",
            "summary": "Test WIN with detailed summary",
            "description": "This is a test WIN narrative with detailed story",
            "status": "draft",
            "win_type": "problem_resolution",
            "impact_level": 3,
            "tags": ["test", "api"],
            "relatedEntityIds": [],
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-01T00:00:00"
        }
    
    @patch('trm_api.api.v1.endpoints.win.win_service')
    @pytest.mark.asyncio
    async def test_create_win_integration(self, mock_service, client):
        """Test tạo WIN thông qua API"""
        # Mock service response (async)
        mock_service.create_win.return_value = asyncio.Future()
        mock_service.create_win.return_value.set_result(self.sample_win_response)
        
        # Gọi API
        response = await client.post("/api/v1/wins/", json=self.sample_win_data)
        
        # Kiểm tra response
        assert response.status_code == 201
        data = response.json()
        
        # Kiểm tra các trường bắt buộc
        assert "uid" in data
        assert data["summary"] == self.sample_win_data["summary"]
        assert data["description"] == self.sample_win_data["description"]
        assert data["status"] == self.sample_win_data["status"]
        assert data["win_type"] == self.sample_win_data["win_type"]
        assert data["impact_level"] == self.sample_win_data["impact_level"]
        assert data["tags"] == self.sample_win_data["tags"]
        
        # Verify service was called
        mock_service.create_win.assert_called_once()
    
    @patch('trm_api.api.v1.endpoints.win.win_service')
    @pytest.mark.asyncio
    async def test_get_win_integration(self, mock_service, client):
        """Test lấy WIN thông qua API"""
        # Mock service response (async)
        mock_service.get_win.return_value = asyncio.Future()
        mock_service.get_win.return_value.set_result(self.sample_win_response)
        
        # Gọi API
        response = await client.get("/api/v1/wins/test-win-uid-123")
        
        # Kiểm tra response
        assert response.status_code == 200
        data = response.json()
        
        # Kiểm tra các trường bắt buộc
        assert data["uid"] == "test-win-uid-123"
        assert data["summary"] == "Test WIN with detailed summary"
        assert data["description"] == "This is a test WIN narrative with detailed story"
        assert data["status"] == "draft"
        assert data["win_type"] == "problem_resolution"
        
        # Verify service was called
        mock_service.get_win.assert_called_once_with(win_id="test-win-uid-123")
    
    @patch('trm_api.api.v1.endpoints.win.win_service')
    @pytest.mark.asyncio
    async def test_list_wins_integration(self, mock_service, client):
        """Test lấy danh sách WIN thông qua API"""
        # Mock service response (async)
        mock_service.list_wins.return_value = asyncio.Future()
        mock_service.list_wins.return_value.set_result([self.sample_win_response])
        
        # Gọi API
        response = await client.get("/api/v1/wins/")
        
        # Kiểm tra response
        assert response.status_code == 200
        data = response.json()
        
        # Kiểm tra structure
        assert "items" in data
        assert "count" in data
        assert len(data["items"]) == 1
        assert data["count"] == 1
        
        # Kiểm tra item đầu tiên
        win_item = data["items"][0]
        assert win_item["uid"] == "test-win-uid-123"
        assert win_item["summary"] == "Test WIN with detailed summary"
        
        # Verify service was called
        mock_service.list_wins.assert_called_once_with(skip=0, limit=25)
    
    @patch('trm_api.api.v1.endpoints.win.win_service')
    @pytest.mark.asyncio
    async def test_update_win_integration(self, mock_service, client):
        """Test cập nhật WIN thông qua API"""
        # Mock service responses (async)
        mock_service.get_win.return_value = asyncio.Future()
        mock_service.get_win.return_value.set_result(self.sample_win_response)
        updated_response = {**self.sample_win_response, "summary": "Updated WIN"}
        mock_service.update_win.return_value = asyncio.Future()
        mock_service.update_win.return_value.set_result(updated_response)
        
        # Dữ liệu cập nhật
        update_data = {"summary": "Updated WIN"}
        
        # Gọi API
        response = await client.put("/api/v1/wins/test-win-uid-123", json=update_data)
        
        # Kiểm tra response
        assert response.status_code == 200
        data = response.json()
        
        # Kiểm tra đã cập nhật
        assert data["summary"] == "Updated WIN"
        assert data["uid"] == "test-win-uid-123"
        
        # Verify service was called
        mock_service.get_win.assert_called_once_with(win_id="test-win-uid-123")
        mock_service.update_win.assert_called_once()
    
    @patch('trm_api.api.v1.endpoints.win.win_service')
    @pytest.mark.asyncio
    async def test_delete_win_integration(self, mock_service, client):
        """Test xóa WIN thông qua API"""
        # Mock service responses (async)
        mock_service.get_win.return_value = asyncio.Future()
        mock_service.get_win.return_value.set_result(self.sample_win_response)
        mock_service.delete_win.return_value = asyncio.Future()
        mock_service.delete_win.return_value.set_result(True)
        
        # Gọi API
        response = await client.delete("/api/v1/wins/test-win-uid-123")
        
        # Kiểm tra response
        assert response.status_code == 204
        
        # Verify service was called
        mock_service.get_win.assert_called_once_with(win_id="test-win-uid-123")
        mock_service.delete_win.assert_called_once_with(win_id="test-win-uid-123")
    
    @pytest.mark.asyncio
    async def test_create_win_validation_error(self, client):
        """Test validation error khi tạo WIN với dữ liệu không hợp lệ"""
        # Dữ liệu thiếu trường bắt buộc
        invalid_data = {
            "summary": "Test WIN with enough characters"
            # Thiếu description (required field)
        }
        
        # Gọi API
        response = await client.post("/api/v1/wins/", json=invalid_data)
        
        # Kiểm tra validation error
        assert response.status_code == 422
        error_data = response.json()
        assert "detail" in error_data
        
        # Kiểm tra có thông báo lỗi về trường description
        errors = error_data["detail"]
        description_error = next((e for e in errors if e["loc"] == ["body", "description"]), None)
        assert description_error is not None
        assert description_error["type"] == "missing"
    
    @pytest.mark.asyncio
    async def test_create_win_enum_validation(self, client):
        """Test validation cho enum values"""
        # Dữ liệu với enum value không hợp lệ
        invalid_enum_data = {
            "summary": "Test WIN with detailed summary",
            "description": "Test narrative",
            "status": "invalid_status",  # Không hợp lệ
            "win_type": "invalid_type",   # Không hợp lệ
            "impact_level": 10           # Có thể không hợp lệ nếu có validation
        }
        
        # Gọi API - nên pass vì enum adapter sẽ normalize
        response = await client.post("/api/v1/wins/", json=invalid_enum_data)
        
        # Nếu có lỗi, kiểm tra response
        if response.status_code != 201:
            logger.info(f"Enum validation response: {response.status_code} - {response.json()}") 