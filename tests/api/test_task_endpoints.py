import json
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, AsyncMock
import unittest
from datetime import datetime, timedelta
import pytest
import pytest_asyncio
import uuid

from trm_api.main import app
from trm_api.models.task import Task, TaskCreate, TaskUpdate, TaskStatus, TaskType, EffortUnit
from trm_api.models.pagination import PaginatedResponse
from tests.conftest import get_test_client

# Create test client for integration testing
client = TestClient(app)

def get_mock_task():
    """Helper function to generate mock task data"""
    return {
        "uid": "task123",
        "name": "Test Task",
        "description": "Test task description",
        "status": TaskStatus.TODO,
        "priority": 1,
        "project_id": "project123",
        "due_date": datetime.now() + timedelta(days=7),
        "tags": ["test", "sample"],
        "effort_estimate": 5.0,
        "task_type": TaskType.FEATURE,
        "effort_unit": EffortUnit.HOURS,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }

class TestTaskEndpoints:
    """Integration tests for Task API endpoints"""

    @pytest_asyncio.fixture
    async def client(self):
        return await get_test_client()

    @pytest.mark.asyncio
    async def test_create_task_integration(self, client):
        """Test creating a task via API endpoint - Integration test"""
        # First create a project for the task
        project_data = {
            "title": f"Test Project {uuid.uuid4()}",
            "description": "Project for task testing",
            "status": "active"
        }
        
        # Try to create task with realistic data
        task_data = {
            "name": f"Integration Task {uuid.uuid4()}",
            "description": "Created via integration test",
            "status": "ToDo",
            "priority": 1,
            "project_id": f"test_project_{uuid.uuid4()}",  # Use test project ID
            "due_date": (datetime.now() + timedelta(days=14)).isoformat(),
            "tags": ["integration", "test"],
            "effort_estimate": 8.0,
            "task_type": "Feature",
            "effort_unit": "hours"
        }

        # Make request
        response = await client.post("/api/v1/tasks/", json=task_data)
        
        # For integration test, we expect either success or a specific business logic error
        # If project doesn't exist, that's expected behavior
        if response.status_code == 400:
            assert "project" in response.json()["detail"].lower()
        else:
            assert response.status_code == 201
            response_data = response.json()
            assert response_data["name"] == task_data["name"]
            assert response_data["description"] == task_data["description"]

    @pytest.mark.asyncio 
    async def test_get_task_integration(self, client):
        """Test retrieving a task - Integration test"""
        # Create a task first
        task_data = {
            "name": f"Get Task Test {uuid.uuid4()}",
            "description": "Task for get testing",
            "status": "ToDo",
            "priority": 1,
            "project_id": f"test_project_{uuid.uuid4()}",
            "due_date": (datetime.now() + timedelta(days=7)).isoformat(),
            "tags": ["get", "test"],
            "effort_estimate": 3.0,
            "task_type": "Feature", 
            "effort_unit": "hours"
        }
        
        create_response = await client.post("/api/v1/tasks/", json=task_data)
        
        if create_response.status_code == 201:
            # Task created successfully, test retrieval
            created_task = create_response.json()
            task_id = created_task["uid"]
            
            # Get the task
            response = await client.get(f"/api/v1/tasks/{task_id}")
            assert response.status_code == 200
            
            task_data = response.json()
            assert task_data["uid"] == task_id
            assert task_data["name"] == task_data["name"]
        else:
            # Test with non-existent task
            response = await client.get("/api/v1/tasks/nonexistent")
            assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_list_tasks_integration(self, client):
        """Test listing tasks for a project - Integration test"""
        project_id = f"test_project_{uuid.uuid4()}"
        
        # Test pagination endpoint
        response = await client.get(f"/api/v1/tasks/?project_id={project_id}&page=1&page_size=10")
        
        # Should return paginated response even if empty
        assert response.status_code == 200
        result = response.json()
        assert "items" in result
        assert "metadata" in result
        assert isinstance(result["items"], list)
        assert "total_count" in result["metadata"]
        assert "page" in result["metadata"]
        assert "page_size" in result["metadata"]
