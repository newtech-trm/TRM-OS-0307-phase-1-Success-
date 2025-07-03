# Hướng dẫn kiểm thử không đồng bộ (Async Testing Guide)

**Ngày tạo:** 2025-07-03

**Phiên bản:** 1.0

**Tác giả:** TRM Engineering Team

## Giới thiệu

Tài liệu này cung cấp hướng dẫn chi tiết về cách viết và bảo trì các bài kiểm thử không đồng bộ (async tests) cho hệ thống TRM-OS. Khi toàn bộ hệ thống đã chuyển sang sử dụng mô hình API không đồng bộ (async/await), các bài kiểm thử cũng phải được viết theo cùng một mô hình.

## Công cụ và thư viện

1. **pytest-asyncio**: Plugin cho pytest hỗ trợ kiểm thử không đồng bộ
2. **httpx**: Thay thế cho requests, hỗ trợ HTTP client không đồng bộ
3. **AsyncMock**: Thay thế cho MagicMock, hỗ trợ mock các coroutine

## Cài đặt

```bash
pip install pytest-asyncio httpx pytest-mock
```

## Cấu trúc bài kiểm thử không đồng bộ

### 1. Fixture không đồng bộ

```python
@pytest.fixture
async def async_test_client():
    """Create async test client for FastAPI app"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture
async def setup_test_data():
    """Create test data before test and cleanup after"""
    # Setup test data
    test_data = {...}
    
    # Tạo dữ liệu test trong database
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/v1/tasks/", json=test_data)
        test_id = response.json()["uid"]
    
    yield test_data, test_id
    
    # Cleanup after test
    async with AsyncClient(app=app, base_url="http://test") as client:
        await client.delete(f"/api/v1/tasks/{test_id}")
```

### 2. Bài kiểm thử không đồng bộ

```python
@pytest.mark.asyncio
async def test_get_task(async_test_client, setup_test_data):
    # Lấy dữ liệu test từ fixture
    test_data, test_id = setup_test_data
    
    # Gọi API để lấy task
    response = await async_test_client.get(f"/api/v1/tasks/{test_id}")
    
    # Kiểm tra kết quả
    assert response.status_code == 200
    data = response.json()
    assert data["uid"] == test_id
    assert data["title"] == test_data["title"]
    assert data["status"] == "todo"  # Kiểm tra giá trị enum đã chuẩn hóa
```

### 3. Mock không đồng bộ

```python
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_service_with_mock(monkeypatch):
    # Tạo mock cho repository
    mock_repo = AsyncMock()
    mock_repo.get_task.return_value = {"uid": "test-123", "title": "Test Task"}
    
    # Áp dụng mock vào service
    service = TaskService(repository=mock_repo)
    
    # Gọi method của service
    result = await service.get_task("test-123")
    
    # Kiểm tra kết quả và việc gọi mock
    assert result["uid"] == "test-123"
    mock_repo.get_task.assert_called_once_with("test-123")
```

## Chuyển đổi từ kiểm thử đồng bộ sang không đồng bộ

### Trước khi chuyển đổi

```python
class TestTaskAPI:
    def setup_method(self):
        self.client = TestClient(app)
        self.test_task = {
            "title": "Test Task",
            "status": "TODO"
        }
        response = self.client.post("/api/v1/tasks/", json=self.test_task)
        self.task_id = response.json()["uid"]
    
    def teardown_method(self):
        self.client.delete(f"/api/v1/tasks/{self.task_id}")
    
    def test_get_task(self):
        response = self.client.get(f"/api/v1/tasks/{self.task_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == self.test_task["title"]
```

### Sau khi chuyển đổi

```python
class TestTaskAPI:
    @pytest.fixture
    async def setup_test(self):
        # Setup
        self.test_task = {
            "title": "Test Task",
            "status": "TODO"
        }
        
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post("/api/v1/tasks/", json=self.test_task)
            self.task_id = response.json()["uid"]
        
        yield
        
        # Teardown
        async with AsyncClient(app=app, base_url="http://test") as ac:
            await ac.delete(f"/api/v1/tasks/{self.task_id}")
    
    @pytest.mark.asyncio
    async def test_get_task(self, setup_test):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get(f"/api/v1/tasks/{self.task_id}")
            assert response.status_code == 200
            data = response.json()
            assert data["title"] == self.test_task["title"]
```

## Best Practices

### 1. Luôn sử dụng `@pytest.mark.asyncio`

Đảm bảo mọi test không đồng bộ đều có decorator này để pytest biết cách chạy coroutine.

```python
@pytest.mark.asyncio
async def test_example():
    # ...
```

### 2. Ưu tiên AsyncMock thay vì MagicMock

```python
# Không tốt
from unittest.mock import MagicMock
mock_service = MagicMock()
mock_service.get_task.return_value = {...}

# Tốt
from unittest.mock import AsyncMock
mock_service = AsyncMock()
mock_service.get_task.return_value = {...}
```

### 3. Sử dụng async context manager

```python
async with AsyncClient(app=app, base_url="http://test") as client:
    # ...
```

### 4. Xử lý ngoại lệ không đồng bộ

```python
@pytest.mark.asyncio
async def test_exception_handling():
    with pytest.raises(ValueError):
        await service.method_that_raises_exception()
```

### 5. Mocking cho async context manager

```python
@pytest.mark.asyncio
async def test_with_context_manager_mock(monkeypatch):
    mock_session = AsyncMock()
    mock_db = AsyncMock()
    mock_db.session.return_value.__aenter__.return_value = mock_session
    
    # Inject mock
    service = TaskService(db=mock_db)
    
    # Test
    await service.some_method()
```

## Kiểm thử các adapter và decorator

### Kiểm thử EnumAdapter

```python
@pytest.mark.asyncio
async def test_enum_adapter_in_api(async_test_client):
    # Tạo task với enum value không chuẩn
    task_data = {
        "title": "Test Task",
        "status": "TaskStatus.TODO",  # Enum không chuẩn hóa
        "task_type": "REGULAR"        # Enum không chuẩn hóa
    }
    
    # Tạo task mới
    response = await async_test_client.post("/api/v1/tasks/", json=task_data)
    assert response.status_code == 200
    task_id = response.json()["uid"]
    
    # Lấy task để kiểm tra chuẩn hóa
    response = await async_test_client.get(f"/api/v1/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    
    # Kiểm tra giá trị enum đã được chuẩn hóa
    assert data["status"] == "todo"       # camelCase không prefix
    assert data["task_type"] == "regular"  # camelCase không prefix
    
    # Cleanup
    await async_test_client.delete(f"/api/v1/tasks/{task_id}")
```

### Kiểm thử Response Decorator

```python
@pytest.mark.asyncio
async def test_response_adapter_decorator(async_test_client):
    # Tạo task với datetime
    task_data = {
        "title": "Test Task",
        "due_date": datetime.utcnow().isoformat()
    }
    
    # Tạo task mới
    response = await async_test_client.post("/api/v1/tasks/", json=task_data)
    assert response.status_code == 200
    data = response.json()
    
    # Kiểm tra datetime đã được chuẩn hóa
    assert "created_at" in data
    assert "Z" in data["created_at"]  # Đảm bảo định dạng UTC ISO 8601
    
    # Kiểm tra due_date đã được chuẩn hóa
    assert "due_date" in data
    assert "Z" in data["due_date"]  # Đảm bảo định dạng UTC ISO 8601
```

## Xử lý các vấn đề phổ biến

### 1. Lỗi "Task exception was never retrieved"

**Vấn đề**: Quên đóng resource trong coroutine.

**Giải pháp**: Sử dụng finally clause hoặc async context manager.

```python
async def example():
    connection = await create_connection()
    try:
        await connection.execute(query)
    finally:
        await connection.close()
```

### 2. Lỗi "'MagicMock' object has no attribute '__aenter__'"

**Vấn đề**: Sử dụng MagicMock thay vì AsyncMock cho async context manager.

**Giải pháp**: Sử dụng AsyncMock và thiết lập __aenter__ và __aexit__.

```python
from unittest.mock import AsyncMock

mock_db = AsyncMock()
mock_session = AsyncMock()
mock_db.session.return_value.__aenter__.return_value = mock_session
```

### 3. Lỗi "The object should be a coroutine"

**Vấn đề**: Thiếu từ khóa await khi gọi một coroutine.

**Giải pháp**: Đảm bảo sử dụng await cho tất cả các coroutine.

```python
# Không đúng
result = service.get_task("123")  # Thiếu await

# Đúng
result = await service.get_task("123")
```

## Tài liệu liên quan

- [Ontology-First Approach](../architecture/ontology-first-approach.md)
- [Async API Pattern](../technical-decisions/async-api-pattern.md)
- [Enum Adapter Pattern](../technical-decisions/enum-adapter-pattern.md)
