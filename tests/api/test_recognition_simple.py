import pytest
import pytest_asyncio
from httpx import AsyncClient
from datetime import datetime
import uuid

from trm_api.main import app
from tests.conftest import get_test_client


@pytest_asyncio.fixture
async def client():
    return await get_test_client()


@pytest.mark.asyncio
async def test_simple_recognition(client):
    """
    Test tối thiểu chỉ tạo Recognition với các trường bắt buộc và không có relationship.
    Đã cập nhật để sử dụng AsyncClient và kiểm tra trường uid thay vì id.
    """
    # Tạo dữ liệu tối thiểu cho recognition với các trường bắt buộc
    recognition_data = {
        "name": "Simple Test Recognition",
        "message": "Test đơn giản để xác định lỗi",
        "recognition_type": "GRATITUDE", 
        "status": "GRANTED",
        "given_by_agent_id": f"test_{str(uuid.uuid4())}",
        "received_by_agent_ids": [f"test_{str(uuid.uuid4())}"],
        "value_level": "3"
    }
    
    # Gọi API tạo recognition với async client
    response = await client.post("/api/v1/recognitions/", json=recognition_data)
    
    # In response để debug
    print("Response status code:", response.status_code)
    print("Response body:", response.json() if response.status_code != 500 else "Internal Server Error")
    
    # Kiểm tra response status code
    assert response.status_code == 201
    
    # Kiểm tra kết quả trả về có trường uid
    response_data = response.json()
    assert "uid" in response_data
    assert isinstance(response_data["uid"], str)
