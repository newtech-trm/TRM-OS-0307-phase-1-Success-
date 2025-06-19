import pytest
import pytest_asyncio
import uuid
from unittest.mock import patch, AsyncMock
from datetime import datetime
from httpx import AsyncClient
from fastapi import status

from trm_api.main import app
from trm_api.schemas.recognition import RecognitionCreate, RecognitionType, RecognitionStatus
from tests.conftest import get_test_client


@pytest_asyncio.fixture
async def client():
    return await get_test_client()


@pytest.mark.asyncio
async def test_create_recognition(client):
    """
    Test creating a new recognition and verify the response structure and datetime handling.
    """
    # Tạo dữ liệu cho recognition mới
    recognition_data = {
        "name": "Test Recognition",
        "message": "Công nhận đóng góp tuyệt vời",
        "recognition_type": "GRATITUDE", # Phải khớp với enum RecognitionType
        "status": "GRANTED", # Phải khớp với enum RecognitionStatus  
        "value_level": "3", # string thay vì integer
        "tags": ["test", "api"],
        "given_by_agent_id": f"test_{str(uuid.uuid4())}",
        "received_by_agent_ids": [f"test_{str(uuid.uuid4())}", f"test_{str(uuid.uuid4())}"],
        "recognizes_win_id": None,
        "recognizes_contributions": {
            "project": [f"test_{str(uuid.uuid4())}"],
            "task": [f"test_{str(uuid.uuid4())}"],
            "resource": []
        }
    }
    
    # Gọi API tạo recognition với async client
    response = await client.post("/api/v1/recognitions/", json=recognition_data)
    
    # Kiểm tra response status code
    assert response.status_code == 201
    
    # Kiểm tra response body và cấu trúc
    response_data = response.json()
    
    # Kiểm tra uid field (đã chuẩn hóa từ id)
    assert "uid" in response_data
    assert isinstance(response_data["uid"], str)
    
    # Kiểm tra các trường cơ bản
    assert response_data["name"] == recognition_data["name"]
    assert response_data["message"] == recognition_data["message"]
    assert response_data["recognition_type"] == recognition_data["recognition_type"]
    assert response_data["status"] == recognition_data["status"]
    assert response_data["value_level"] == recognition_data["value_level"]
    assert set(response_data["tags"]) == set(recognition_data["tags"])
    
    # Kiểm tra datetime fields
    assert "created_at" in response_data
    assert "updated_at" in response_data
    
    # Kiểm tra định dạng datetime ISO 8601
    try:
        datetime.fromisoformat(response_data["created_at"].replace("Z", "+00:00"))
        datetime.fromisoformat(response_data["updated_at"].replace("Z", "+00:00"))
    except ValueError:
        pytest.fail("Datetime fields không đúng định dạng ISO 8601")


@pytest.mark.asyncio
async def test_get_recognition(client):
    """
    Kiểm thử việc lấy thông tin recognition.
    """
    # Bước 1: Tạo recognition mới
    recognition_data = {
        "name": "Test Recognition for Get",
        "message": "Công nhận đóng góp",
        "recognition_type": "GRATITUDE",
        "status": "GRANTED",
        "value_level": 3,
        "tags": ["get", "test"],
        "given_by_agent_id": f"test_{str(uuid.uuid4())}"
    }
    creation_response = await client.post("/api/v1/recognitions/", json=recognition_data)
    created_recognition = creation_response.json()
    recognition_id = created_recognition["id"]
    
    # Bước 2: Lấy recognition theo ID
    response = await client.get(f"/api/v1/recognitions/{recognition_id}")
    
    # Kiểm tra response
    assert response.status_code == 200
    
    # Kiểm tra dữ liệu
    response_data = response.json()
    assert response_data["id"] == recognition_id
    assert response_data["name"] == recognition_data["name"]
    
    # Kiểm tra datetime adapter
    assert "created_at" in response_data
    assert "updated_at" in response_data
    try:
        datetime.fromisoformat(response_data["created_at"].replace("Z", "+00:00"))
    except ValueError:
        pytest.fail("created_at field không đúng định dạng ISO 8601")


@pytest.mark.asyncio
async def test_list_recognitions(client):
    """
    Kiểm thử việc lấy danh sách recognition.
    """
    # Bước 1: Tạo một số recognition để đảm bảo có dữ liệu
    for i in range(3):
        recognition_data = {
            "name": f"Test Recognition List {i}",
            "message": f"Công nhận đóng góp {i}",
            "recognition_type": "GRATITUDE",
            "status": "GRANTED",
            "value_level": i + 1,
            "tags": ["list", f"test{i}"],
            "given_by_agent_id": f"test_{str(uuid.uuid4())}"
        }
        await client.post("/api/v1/recognitions/", json=recognition_data)
    
    # Bước 2: Lấy danh sách recognitions
    response = await client.get("/api/v1/recognitions/?skip=0&limit=10")
    
    # Kiểm tra response
    assert response.status_code == 200
    
    # Kiểm tra cấu trúc response
    response_data = response.json()
    assert "items" in response_data
    assert "total" in response_data
    assert "skip" in response_data
    assert "limit" in response_data
    
    # Kiểm tra số lượng item (ít nhất phải có những item vừa tạo)
    assert len(response_data["items"]) >= 3
    
    # Kiểm tra cấu trúc và datetime của từng item
    for item in response_data["items"]:
        assert "id" in item
        assert "name" in item
        assert "created_at" in item
        try:
            datetime.fromisoformat(item["created_at"].replace("Z", "+00:00"))
        except ValueError:
            pytest.fail("created_at field không đúng định dạng ISO 8601")


@pytest.mark.asyncio
async def test_update_recognition(client):
    """
    Kiểm thử việc cập nhật recognition và đảm bảo datetime adapter hoạt động đúng.
    """
    # Bước 1: Tạo recognition mới
    recognition_data = {
        "name": "Test Recognition for Update",
        "message": "Công nhận đóng góp ban đầu",
        "recognition_type": "GRATITUDE",
        "status": "PENDING",
        "value_level": 2,
        "tags": ["update", "test"],
        "given_by_agent_id": f"test_{str(uuid.uuid4())}"
    }
    creation_response = await client.post("/api/v1/recognitions/", json=recognition_data)
    created_recognition = creation_response.json()
    recognition_id = created_recognition["id"]
    
    # Bước 2: Cập nhật recognition
    update_data = {
        "name": "Updated Recognition",
        "message": "Công nhận đóng góp đã cập nhật",
        "status": "GRANTED",
        "value_level": 4
    }
    response = await client.put(f"/api/v1/recognitions/{recognition_id}", json=update_data)
    
    # Kiểm tra response
    assert response.status_code == 200
    
    # Kiểm tra dữ liệu đã cập nhật
    response_data = response.json()
    assert response_data["name"] == update_data["name"]
    assert response_data["message"] == update_data["message"]
    assert response_data["value_level"] == update_data["value_level"]
    
    # Kiểm tra created_at không đổi
    assert response_data["created_at"] == created_recognition["created_at"]
    
    # Kiểm tra updated_at đã thay đổi và theo đúng định dạng ISO
    assert response_data["updated_at"] != created_recognition["updated_at"]
    try:
        datetime.fromisoformat(response_data["updated_at"].replace("Z", "+00:00"))
    except ValueError:
        pytest.fail("updated_at field không đúng định dạng ISO 8601")


@pytest.mark.asyncio
async def test_delete_recognition(client):
    """
    Kiểm thử việc xóa recognition.
    """
    # Bước 1: Tạo recognition mới
    recognition_data = {
        "name": "Test Recognition for Delete",
        "message": "Công nhận đóng góp",
        "recognition_type": "GRATITUDE",
        "status": "GRANTED",
        "value_level": 3,
        "tags": ["delete", "test"],
        "given_by_agent_id": f"test_{str(uuid.uuid4())}"
    }
    creation_response = await client.post("/api/v1/recognitions/", json=recognition_data)
    created_recognition = creation_response.json()
    recognition_id = created_recognition["id"]
    
    # Bước 2: Xóa recognition
    delete_response = await client.delete(f"/api/v1/recognitions/{recognition_id}")
    
    # Kiểm tra response
    assert delete_response.status_code == 204
    
    # Kiểm tra recognition đã bị xóa bằng cách thử get lại
    get_response = await client.get(f"/api/v1/recognitions/{recognition_id}")
    assert get_response.status_code == 404
