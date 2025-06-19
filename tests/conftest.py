#!/usr/bin/env python3
"""
Cấu hình và Fixtures cho pytest trong TRM-OS
Cung cấp fixtures để kết nối Neo4j thật cho các integration tests,
tuân theo nguyên tắc ontology-first, không mock/fake kết nối.
"""

import pytest
# Chỉ import pytest_asyncio trong try-except để tránh lỗi khi chạy những test không cần nó
try:
    import pytest_asyncio
except ImportError:
    pass

import httpx
from datetime import datetime
import neomodel
from enum import Enum

# Áp dụng mark asyncio chọn lọc thay vì toàn bộ file
# pytestmark = pytest.mark.asyncio

from trm_api.main import app
from trm_api.db.session import connect_to_db, get_driver
from trm_api.core.config import settings

# Định nghĩa các enum cần thiết
class ProjectStatus(str, Enum):
    IN_PROGRESS = 'active'
    COMPLETED = 'completed'
    ON_HOLD = 'on_hold'
    CANCELED = 'canceled'

class TaskStatus(str, Enum):
    TODO = 'ToDo'  # Phải viết hoa chữ đầu để khớp model Task
    IN_PROGRESS = 'InProgress'  # Không phải 'in_progress'
    DONE = 'Done'
    BLOCKED = 'Blocked'
    CANCELED = 'Cancelled'  # Đặt lưu ý đây là 'Cancelled' với 2 chữ 'l'
    BACKLOG = 'Backlog'  # Thêm Backlog theo model

class TaskType(str, Enum):
    FEATURE = 'Feature'
    BUG = 'Bug'
    IMPROVEMENT = 'Improvement'
    RESEARCH = 'Research'
    DOCUMENTATION = 'Documentation'
    MEETING = 'Meeting'
    CHORE = 'Chore'  # Thêm để khớp với model Task

class EffortUnit(str, Enum):
    HOURS = 'hours'
    DAYS = 'days'
    POINTS = 'points'


@pytest.fixture(scope="session", autouse=True)
def setup_neo4j_connection():
    """
    Fixture tự động chạy khi bắt đầu test session để cấu hình kết nối Neo4j.
    Sử dụng thông tin kết nối từ settings (từ file .env)
    """
    print(f"Thiết lập kết nối Neo4j tới: {settings.NEO4J_URI}")
    connect_to_db()
    yield
    # Không cần đóng kết nối vì neomodel quản lý kết nối theo thread


@pytest.fixture
async def test_client():
    """
    Fixture tạo client để test các API endpoints.
    Sử dụng kết nối Neo4j thật từ fixture setup_neo4j_connection.
    """
    # Tạo client async mới cho mỗi test sử dụng ASGITransport cho FastAPI
    from httpx import AsyncClient, ASGITransport
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client

@pytest.fixture
async def async_test_client():
    """
    Fixture tạo client async để test các API endpoints.
    Sử dụng kết nối Neo4j thật từ fixture setup_neo4j_connection.
    """
    # Tạo client async mới cho mỗi test sử dụng ASGITransport cho FastAPI
    from httpx import AsyncClient, ASGITransport
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client

async def get_test_client():
    """
    Hàm hỗ trợ cho các test cases để tạo async client
    Sử dụng cho các test không sử dụng fixture test_client
    """
    from httpx import AsyncClient, ASGITransport
    return AsyncClient(transport=ASGITransport(app=app), base_url="http://test")


@pytest.fixture
def seed_test_data():
    """
    Tạo dữ liệu test cơ bản cho Neo4j database.
    Sử dụng transaction để mọi thay đổi có thể rollback nếu cần.
    
    Trả về dictionary các ID của entities đã tạo để test cases có thể sử dụng.
    """
    from neomodel import db
    from trm_api.graph_models.user import User
    from trm_api.graph_models.project import Project
    from trm_api.graph_models.task import Task
    from trm_api.graph_models.win import WIN as Win  # Class tên là WIN nhưng import lại alias là Win
    from trm_api.graph_models.knowledge_snippet import KnowledgeSnippet
    
    # Tạo timestamp để đánh dấu các test data
    timestamp = datetime.now()  
    test_data_ids = {}
    
    # Cleanup: Tìm dữ liệu test cũ để xóa trước khi seed mới
    # NOTE: Đây là phương pháp an toàn nhất để tránh trùng lặp dữ liệu test
    # Chú ý sử dụng tag "test_data" để đảm bảo không ảnh hưởng dữ liệu thật
    query = """
    MATCH (n {is_test_data: true})
    OPTIONAL MATCH (n)-[r]-()
    DELETE r, n
    """
    db.cypher_query(query)
    
    # Tạo Users cho test
    test_user1 = User(
        username="test_user1",
        email="test1@example.com",
        full_name="Test User 1",
        hashed_password="test_hashed_password_not_real",  # Giá trị giả cho test
        is_active=True,
        is_test_data=True,
        created_at=timestamp,
        updated_at=timestamp
    ).save()
    
    test_user2 = User(
        username="test_user2", 
        email="test2@example.com",
        full_name="Test User 2",
        hashed_password="test_hashed_password_not_real",  # Giá trị giả cho test
        is_active=True,
        is_test_data=True,
        created_at=timestamp,
        updated_at=timestamp
    ).save()
    
    # Tạo Projects
    test_project = Project(
        title="Test Project",
        description="Project created for testing",
        status=ProjectStatus.IN_PROGRESS.value,
        is_test_data=True,
        tags=["test", "integration"],
        created_at=timestamp,
        updated_at=timestamp
    ).save()
    
    # Tạo Tasks
    test_task = Task(
        name="Test Task",
        description="Task created for testing",
        status=TaskStatus.TODO.value,
        task_type=TaskType.FEATURE.value,
        priority=0,  # Normal
        effort_estimate=10.0,
        effort_unit=EffortUnit.HOURS.value,
        is_test_data=True,
        tags=["test", "integration"],
        created_at=timestamp,
        updated_at=timestamp
    ).save()
    
    # Tạo WIN
    test_win = Win(
        name="Test WIN",  
        narrative="WIN created for testing",  
        impact_level=5,  
        status="draft",  
        is_test_data=True,
        created_at=timestamp,
        updated_at=timestamp
    ).save()
    
    # Tạo KnowledgeSnippet
    test_knowledge_snippet = KnowledgeSnippet(
        title="Test Knowledge Snippet",
        content="This is a test knowledge snippet content",
        snippet_type="Documentation",  # Sử dụng enum_adapter.KnowledgeSnippetType
        tags=["test", "documentation", "knowledge"],
        source="Test Suite",
        source_url="https://example.com/test",
        is_test_data=True,
        created_at=timestamp,
        updated_at=timestamp
    ).save()
    
    # Tạo các mối quan hệ giữa các entities
    # User1 quản lý Project
    # Bỏ properties vì User.managed_projects không có model định nghĩa
    test_user1.managed_projects.connect(test_project)
    
    # TODO: Relationship assigned_to_projects không tồn tại trong User model
    # Cần xem xét Ontology V3.2 để đồng bộ mối quan hệ User-Project
    # test_user2.assigned_to_projects.connect(test_project, {
    #     "role": "Developer",
    #     "created_at": timestamp 
    # })
    
    # Tạo Task cho Project
    import uuid
    test_project.tasks.connect(test_task, {
        "relationshipId": str(uuid.uuid4()),  # Thêm thuộc tính bắt buộc
        "created_at": timestamp
    })
    
    # Gán Task cho User2
    test_user2.assigned_tasks.connect(test_task, {
        "assignment_type": "Primary",
        "priority_level": 1,
        "created_at": timestamp,
        "status": "assigned"
    })
    
    # Lưu IDs để sử dụng trong tests
    test_data_ids = {
        "user1_id": test_user1.uid,
        "user2_id": test_user2.uid,
        "project_id": test_project.uid,
        "task_id": test_task.uid,
        "win_id": test_win.uid,
        "knowledge_snippet_id": test_knowledge_snippet.uid,  # Thêm uid của KnowledgeSnippet
        "timestamp": timestamp
    }
    
    # Trả về dictionary các ID để tests sử dụng
    yield test_data_ids
    
    # Cleanup sau tests
    try:
        # Xóa tất cả dữ liệu test
        query = """
        MATCH (n {is_test_data: true})
        OPTIONAL MATCH (n)-[r]-()
        DELETE r, n
        """
        db.cypher_query(query)
        print("Đã dọn dẹp dữ liệu test từ Neo4j")
    except Exception as e:
        print(f"Lỗi khi dọn dẹp dữ liệu test: {e}")


# Các fixture bổ sung có thể được thêm vào đây khi cần
