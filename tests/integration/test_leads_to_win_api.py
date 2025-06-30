import pytest
import pytest_asyncio
import uuid
from unittest.mock import patch, AsyncMock
from datetime import datetime
from httpx import AsyncClient
from fastapi import status

from trm_api.main import app
from trm_api.models.relationships import Relationship, RelationshipType, TargetEntityTypeEnum


@pytest.fixture(scope="module")
def project_id():
    """Tạo ID cho Project để sử dụng trong các tests."""
    return str(uuid.uuid4())


@pytest.fixture(scope="module")
def event_id():
    """Tạo ID cho Event để sử dụng trong các tests."""
    return str(uuid.uuid4())


@pytest.fixture(scope="module")
def win_id():
    """Tạo ID cho WIN để sử dụng trong các tests."""
    return str(uuid.uuid4())


@pytest.fixture(scope="module")
def project_win_relationship(project_id, win_id):
    """Tạo dữ liệu quan hệ mẫu giữa Project và WIN."""
    created_time = datetime.now()
    return {
        "source_id": project_id,
        "source_type": "Project",
        "target_id": win_id,
        "target_type": "Win",
        "type": "LEADS_TO_WIN",
        "relationshipId": f"leads_to_win_{project_id}_{win_id}_abcd1234",
        "contributionLevel": 3,
        "directContribution": True,
        "createdAt": created_time,
        "impact_ratio": 0.7,
        "notes": "Test relationship from Project to Win"
    }


@pytest.fixture(scope="module")
def event_win_relationship(event_id, win_id):
    """Tạo dữ liệu quan hệ mẫu giữa Event và WIN."""
    created_time = datetime.now()
    return {
        "source_id": event_id,
        "source_type": "Event",
        "target_id": win_id,
        "target_type": "Win",
        "type": "LEADS_TO_WIN",
        "relationshipId": f"leads_to_win_{event_id}_{win_id}_abcd5678",
        "contributionLevel": 4,
        "directContribution": False,
        "createdAt": created_time,
        "impact_ratio": 0.6,
        "notes": "Test relationship from Event to Win"
    }


# Sử dụng fixture async_test_client từ conftest.py


@pytest.fixture(scope="module")
def leads_to_win_request():
    """Dữ liệu yêu cầu tạo quan hệ LEADS_TO_WIN."""
    return {
        "direct_contribution": True,
        "contribution_level": 5,
        "impact_ratio": 0.8,
        "recognition_score": 85,
        "verified_by": "verifier_id",
        "notes": "Project contributed significantly to this WIN"
    }


@pytest.mark.asyncio
@patch("trm_api.api.v1.endpoints.relationship.relationship_service")
async def test_create_project_leads_to_win_relationship(mock_service, async_test_client, project_id, win_id,
                                                  project_win_relationship, leads_to_win_request):
    """Test creating a LEADS_TO_WIN relationship from Project to WIN."""
    # Set up mock
    mock_service.create_relationship = AsyncMock()
    mock_service.create_relationship.return_value = project_win_relationship
    
    # Call API with async client
    response = await async_test_client.post(
        f"/api/v1/relationships/leads-to-win?source_id={project_id}&source_type=Project&win_id={win_id}",
        json=leads_to_win_request
    )
    
    # Assertions
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["source_id"] == project_id
    assert data["source_type"] == "Project"
    assert data["target_id"] == win_id
    assert data["target_type"] == "Win"
    assert data["type"] == "LEADS_TO_WIN"
    
    # Verify service was called correctly
    mock_service.create_relationship.assert_called_once()
    
@pytest.mark.asyncio
@patch("trm_api.api.v1.endpoints.relationship.relationship_service")
async def test_create_event_leads_to_win_relationship(mock_service, async_test_client, event_id, win_id,
                                                 event_win_relationship, leads_to_win_request):
    """Test creating a LEADS_TO_WIN relationship from Event to WIN."""
    # Set up mock
    mock_service.create_relationship = AsyncMock()
    mock_service.create_relationship.return_value = event_win_relationship
    
    # Call API with async client
    response = await async_test_client.post(
        f"/api/v1/relationships/leads-to-win?source_id={event_id}&source_type=Event&win_id={win_id}",
        json=leads_to_win_request
    )
    
    # Assertions
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["source_id"] == event_id
    assert data["source_type"] == "Event"
    assert data["target_id"] == win_id
    assert data["target_type"] == "Win"
    assert data["type"] == "LEADS_TO_WIN"
    
    # Verify service was called correctly
    mock_service.create_relationship.assert_called_once()
    
@pytest.mark.asyncio
@patch("trm_api.api.v1.endpoints.relationship.relationship_service")
async def test_create_leads_to_win_relationship_invalid_source_type(mock_service, async_test_client, project_id, win_id, leads_to_win_request):
    """Test creating a LEADS_TO_WIN relationship with invalid source type."""
    # Call API with invalid source type
    response = await async_test_client.post(
        f"/api/v1/relationships/leads-to-win?source_id={project_id}&source_type=InvalidType&win_id={win_id}",
        json=leads_to_win_request
    )
    
    # Assertions
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    # Verify service was not called
    mock_service.create_relationship.assert_not_called()
    
@pytest.mark.asyncio
@patch("trm_api.api.v1.endpoints.relationship.relationship_service")
async def test_create_leads_to_win_relationship_invalid_properties(mock_service, async_test_client, project_id, win_id):
    """Test creating a LEADS_TO_WIN relationship with invalid properties."""
    # Invalid request with impact_ratio > 1
    invalid_request = {
        "impact_ratio": 1.5  # Invalid: should be 0-1
    }
    
    # Call API
    response = await async_test_client.post(
        f"/api/v1/relationships/leads-to-win?source_id={project_id}&source_type=Project&win_id={win_id}",
        json=invalid_request
    )
    
    # Assertions
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    # Verify service was not called
    mock_service.create_relationship.assert_not_called()
    
@pytest.mark.asyncio
@patch("trm_api.api.v1.endpoints.relationship.relationship_service")
async def test_get_wins_from_project(mock_service, async_test_client, project_id, win_id, project_win_relationship):
    """Test getting WINs led by a Project."""
    # Set up mock
    mock_service.get_relationships = AsyncMock()
    mock_service.get_relationships.return_value = [project_win_relationship]
    
    # Call API
    response = await async_test_client.get(f"/api/v1/relationships/projects/{project_id}/leads-to-wins")
    
    # Assertions
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["source_id"] == project_id
    assert data[0]["target_id"] == win_id
    assert data[0]["type"] == "LEADS_TO_WIN"
    
    # Verify service was called correctly
    mock_service.get_relationships.assert_called_once()

@pytest.mark.asyncio
@patch("trm_api.api.v1.endpoints.relationship.relationship_service")
async def test_get_wins_from_event(mock_service, async_test_client, event_id, win_id, event_win_relationship):
    """Test getting WINs led by an Event."""
    # Set up mock
    mock_service.get_relationships = AsyncMock()
    mock_service.get_relationships.return_value = [event_win_relationship]
    
    # Call API
    response = await async_test_client.get(f"/api/v1/relationships/events/{event_id}/leads-to-wins")
    
    # Assertions
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["source_id"] == event_id
    assert data[0]["target_id"] == win_id
    assert data[0]["type"] == "LEADS_TO_WIN"
    
    # Verify service was called correctly
    mock_service.get_relationships.assert_called_once()

@pytest.mark.asyncio
@patch("trm_api.api.v1.endpoints.relationship.relationship_service")
async def test_get_projects_events_leading_to_win(mock_service, async_test_client, project_id, event_id, win_id, 
                                             project_win_relationship, event_win_relationship):
    """Test getting Projects and Events leading to a WIN."""
    # Set up mock
    mock_service.get_relationships = AsyncMock()
    mock_service.get_relationships.return_value = [
        project_win_relationship,
        event_win_relationship
    ]
    
    # Call API
    response = await async_test_client.get(f"/api/v1/relationships/wins/{win_id}/led-by")
    
    # Assertions
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2
    
    # Verify items are in response - order might not be guaranteed
    source_types = [item["source_type"] for item in data]
    source_ids = [item["source_id"] for item in data]
    
    assert "Project" in source_types
    assert "Event" in source_types
    assert project_id in source_ids
    assert event_id in source_ids
    
    # Verify all items target the same WIN
    for item in data:
        assert item["target_id"] == win_id
        assert item["target_type"] == "Win"
        assert item["type"] == "LEADS_TO_WIN"
    
    # Verify service was called
    mock_service.get_relationships.assert_called_once()

@pytest.mark.asyncio
@patch("trm_api.api.v1.endpoints.relationship.relationship_service")
async def test_get_projects_leading_to_win_with_filter(mock_service, async_test_client, project_id, win_id, project_win_relationship):
    """Test getting only Projects leading to a WIN with source_type filter."""
    # Set up mock
    mock_service.get_relationships = AsyncMock()
    mock_service.get_relationships.return_value = [project_win_relationship]
    
    # Call API with source_type filter
    response = await async_test_client.get(f"/api/v1/relationships/wins/{win_id}/led-by?source_type=Project")
    
    # Assertions
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["source_id"] == project_id
    assert data[0]["source_type"] == "Project"
    
    # Verify service was called correctly
    mock_service.get_relationships.assert_called_once()
    
@pytest.mark.asyncio
@patch("trm_api.api.v1.endpoints.relationship.relationship_service")
async def test_delete_leads_to_win_relationship(mock_service, async_test_client, project_id, win_id):
    """Test deleting a LEADS_TO_WIN relationship."""
    # Set up mock
    mock_service.delete_relationship = AsyncMock()
    mock_service.delete_relationship.return_value = True
    
    # Call API
    response = await async_test_client.delete(
        f"/api/v1/relationships/leads-to-win?source_id={project_id}&source_type=Project&win_id={win_id}"
    )
    
    # Assertions
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Verify service was called correctly
    mock_service.delete_relationship.assert_called_once()
    
@pytest.mark.asyncio
@patch("trm_api.api.v1.endpoints.relationship.relationship_service")
async def test_delete_leads_to_win_relationship_not_found(mock_service, async_test_client, project_id, win_id):
    """Test deleting a non-existent LEADS_TO_WIN relationship."""
    # Set up mock
    mock_service.delete_relationship = AsyncMock()
    mock_service.delete_relationship.return_value = False
    
    # Call API
    response = await async_test_client.delete(
        f"/api/v1/relationships/leads-to-win?source_id={project_id}&source_type=Project&win_id={win_id}"
    )
    
    # Assertions
    assert response.status_code == status.HTTP_404_NOT_FOUND
    
    # Verify service was called correctly
    mock_service.delete_relationship.assert_called_once()
    
@pytest.mark.asyncio
@patch("trm_api.api.v1.endpoints.relationship.relationship_service")
async def test_delete_leads_to_win_relationship_invalid_source_type(mock_service, async_test_client, project_id, win_id):
    """Test deleting a LEADS_TO_WIN relationship with invalid source type."""
    # Call API with invalid source type
    response = await async_test_client.delete(
        f"/api/v1/relationships/leads-to-win?source_id={project_id}&source_type=InvalidType&win_id={win_id}"
    )
    
    # Assertions
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    # Verify service was not called
    mock_service.delete_relationship.assert_not_called()
