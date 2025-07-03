# Async API Pattern trong TRM-OS

**Ngày tạo:** 2025-07-03

**Phiên bản:** 1.0

**Tác giả:** TRM Engineering Team

## Vấn đề

API endpoints trong ứng dụng web thường xử lý nhiều yêu cầu đồng thời, liên quan đến các hoạt động tốn thời gian như:

1. Truy vấn cơ sở dữ liệu
2. Gọi các dịch vụ bên ngoài
3. Xử lý tệp và I/O
4. Gửi email hoặc thông báo

Khi sử dụng mô hình đồng bộ (synchronous), các yêu cầu này chiếm giữ tài nguyên máy chủ và chặn các yêu cầu khác, dẫn đến hiệu suất kém khi số lượng người dùng tăng lên.

## Giải pháp: Async API Pattern

### Nguyên tắc cốt lõi

TRM-OS áp dụng mô hình API không đồng bộ (asynchronous) dựa trên FastAPI và asyncio để tối ưu hóa throughput và khả năng phản hồi:

1. **Non-blocking I/O**: Xử lý nhiều yêu cầu cùng lúc mà không chặn luồng chính
2. **Event Loop**: Sử dụng event loop của asyncio để quản lý các coroutine
3. **Async/Await syntax**: Sử dụng cú pháp async/await để viết code không đồng bộ một cách rõ ràng
4. **End-to-End Async**: Đảm bảo tính không đồng bộ xuyên suốt từ API controller đến database access

## Triển khai

### Async FastAPI Endpoints

```python
@router.get("/tasks/", response_model=List[TaskResponseSchema])
@adapt_task_response
async def get_tasks(
    project_id: Optional[str] = None,
    status: Optional[str] = None,
    service: TaskService = Depends(get_task_service)
):
    """Get list of tasks with optional filtering"""
    filters = {}
    if project_id:
        filters["project_id"] = project_id
    if status:
        filters["status"] = status
        
    return await service.get_tasks(filters)

@router.post("/tasks/", response_model=TaskResponseSchema)
@adapt_task_response
async def create_task(
    task: TaskCreateSchema,
    service: TaskService = Depends(get_task_service)
):
    """Create a new task"""
    return await service.create_task(task.model_dump())
```

### Async Service Layer

```python
class TaskService:
    def __init__(self, repository: TaskRepository = Depends(get_task_repository)):
        self.repository = repository
    
    async def get_tasks(self, filters: dict = None) -> List[dict]:
        """Get tasks with optional filtering"""
        return await self.repository.get_tasks(filters or {})
    
    async def create_task(self, task_data: dict) -> dict:
        """Create a new task"""
        # Validate required fields
        if not task_data.get("title"):
            raise ValueError("Task title is required")
        
        return await self.repository.create_task(task_data)
```

### Async Repository Layer

```python
class TaskRepository:
    def __init__(self, db: Neo4jDatabase = Depends(get_database)):
        self.db = db
    
    async def get_tasks(self, filters: dict = None) -> List[dict]:
        """Get tasks with optional filtering"""
        query = "MATCH (t:Task)"
        params = {}
        
        # Apply filters
        if filters:
            conditions = []
            if "project_id" in filters:
                query += " MATCH (t)-[:IS_PART_OF_PROJECT]->(p:Project)"
                conditions.append("p.uid = $project_id")
                params["project_id"] = filters["project_id"]
            
            if "status" in filters:
                normalized_status = EnumAdapter.normalize_task_status(filters["status"])
                conditions.append("t.status = $status")
                params["status"] = normalized_status
            
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
        
        query += " RETURN t"
        
        async with self.db.session() as session:
            result = await session.run(query, params)
            tasks = await result.data()
            return [dict(task["t"]) for task in tasks]
    
    async def create_task(self, task_data: dict) -> dict:
        """Create a new task"""
        # Normalize enum values
        if "status" in task_data:
            task_data["status"] = EnumAdapter.normalize_task_status(task_data["status"])
        
        if "task_type" in task_data:
            task_data["task_type"] = EnumAdapter.normalize_task_type(task_data["task_type"])
        
        # Set default values
        if "created_at" not in task_data:
            task_data["created_at"] = datetime.utcnow()
        
        task_data["uid"] = str(uuid.uuid4())
        
        # Create task in database
        query = """
        CREATE (t:Task $task_data)
        RETURN t
        """
        
        async with self.db.session() as session:
            result = await session.run(query, {"task_data": task_data})
            data = await result.single()
            return dict(data["t"])
```

### Async Database Connection

```python
class Neo4jDatabase:
    def __init__(self, config: Neo4jConfig):
        self.config = config
        self._driver = None
    
    @property
    async def driver(self):
        if self._driver is None:
            self._driver = GraphDatabase.driver(
                self.config.uri,
                auth=(self.config.username, self.config.password)
            )
        return self._driver
    
    @contextlib.asynccontextmanager
    async def session(self):
        driver = await self.driver
        session = driver.session()
        try:
            yield session
        finally:
            session.close()
```

### Async Integration Testing

```python
class TestTaskAPI:
    @pytest.fixture
    async def setup_test(self):
        # Setup test data
        self.test_task = {
            "title": "Test Task",
            "description": "This is a test task",
            "status": "todo",
            "project_id": "project-123"
        }
        
        # Clean up after test
        yield
        # Delete test data
        async with AsyncClient(app=app, base_url="http://test") as ac:
            await ac.delete(f"/api/v1/tasks/{self.created_task_id}")
    
    @pytest.mark.asyncio
    async def test_create_task(self, setup_test):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post("/api/v1/tasks/", json=self.test_task)
            assert response.status_code == 200
            data = response.json()
            assert "uid" in data
            assert data["title"] == self.test_task["title"]
            assert data["status"] == "todo"  # Normalized value
            
            # Save for cleanup
            self.created_task_id = data["uid"]
```

## Lợi ích

1. **Hiệu suất cao**: Xử lý nhiều yêu cầu cùng lúc, tăng throughput của API
2. **Tối ưu tài nguyên**: Sử dụng hiệu quả CPU và bộ nhớ bằng cách giảm thời gian chờ I/O
3. **Khả năng mở rộng**: Dễ dàng xử lý lượng lớn yêu cầu đồng thời
4. **Tích hợp tốt**: Hoạt động hiệu quả với event-driven architecture và SystemEventBus

## Thách thức và giải pháp

1. **Độ phức tạp trong debug**: 
   - *Giải pháp*: Sử dụng logging chi tiết và theo dõi các coroutine

2. **Tương thích với thư viện bên thứ ba**:
   - *Giải pháp*: Sử dụng các wrapper async hoặc chạy các thư viện đồng bộ trong ThreadPoolExecutor

3. **Testing phức tạp hơn**:
   - *Giải pháp*: Sử dụng pytest-asyncio và AsyncMock thay vì MagicMock

4. **Xử lý lỗi**:
   - *Giải pháp*: Sử dụng try/except/finally trong coroutine và đảm bảo tài nguyên được giải phóng

## Best Practices

1. **Luôn đóng kết nối**:
   ```python
   try:
       # Async operations
   finally:
       await connection.close()
   ```

2. **Sử dụng async context manager**:
   ```python
   async with db.session() as session:
       # Database operations
   ```

3. **Tránh chặn event loop**:
   ```python
   # Không tốt
   time.sleep(1)
   
   # Tốt
   await asyncio.sleep(1)
   ```

4. **Sử dụng asyncio.gather cho các tác vụ song song**:
   ```python
   results = await asyncio.gather(
       service.get_tasks(),
       service.get_projects(),
       service.get_users()
   )
   ```

## Các mẫu thức liên quan

1. **[Ontology-First Approach](../architecture/ontology-first-approach.md)**
2. **[Event-Driven Architecture](../architecture/event-driven-architecture.md)**
3. **[Enum Adapter Pattern](./enum-adapter-pattern.md)**
