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
def agent_id():
    """Tạo ID cho Agent để sử dụng trong các tests."""
    return str(uuid.uuid4())


@pytest.fixture(scope="module")
def recognition_id():
    """Tạo ID cho Recognition để sử dụng trong các tests."""
    return str(uuid.uuid4())


@pytest.fixture(scope="module")
def agent_recognition_relationship(agent_id, recognition_id):
    """Tạo dữ liệu quan hệ mẫu giữa Agent và Recognition."""
    return {
        "source_id": agent_id,
        "source_type": "Agent",
        "target_id": recognition_id,
        "target_type": "Recognition",
        "type": "GIVEN_BY",
        "relationshipId": f"given_by_{agent_id}_{recognition_id}_abcd1234",
        "notes": "Test note for given recognition",
        "createdAt": datetime.now()
    }


@pytest.fixture(scope="module")
def given_by_request():
    """Dữ liệu yêu cầu tạo quan hệ GIVEN_BY."""
    return {"notes": "Agent recognizing outstanding achievements"}


@pytest.mark.asyncio
@patch("trm_api.api.v1.endpoints.relationship.relationship_service")
async def test_create_given_by_relationship(mock_service, async_test_client, agent_id, recognition_id, 
                                           agent_recognition_relationship, given_by_request):
    """Test creating a GIVEN_BY relationship from Agent to Recognition."""
    # Set up mock
    mock_service.create_relationship = AsyncMock(return_value=Relationship(**agent_recognition_relationship))

    # Call API using async client
    response = await async_test_client.post(
        f"/api/v1/relationships/given-by?agent_id={agent_id}&recognition_id={recognition_id}",
        json=given_by_request
    )
    
    # Assertions
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["source_id"] == agent_id
    assert data["target_id"] == recognition_id
    assert data["type"] == "GIVEN_BY"
    
    # Verify service was called correctly
    mock_service.create_relationship.assert_called_once()


@pytest.mark.asyncio
@patch("trm_api.api.v1.endpoints.relationship.relationship_service")
async def test_create_given_by_relationship_entities_not_found(mock_service, async_test_client, agent_id, 
                                                             recognition_id, given_by_request):
    """Test creating a GIVEN_BY relationship when entities don't exist."""
    # Set up mock
    mock_service.create_relationship = AsyncMock(return_value=None)

    # Call API
    response = await async_test_client.post(
        f"/api/v1/relationships/given-by?agent_id={agent_id}&recognition_id={recognition_id}",
        json=given_by_request
    )
    
    # Assertions
    assert response.status_code == status.HTTP_404_NOT_FOUND
    
    # Verify service was called correctly
    mock_service.create_relationship.assert_called_once()


@pytest.mark.asyncio
@patch("trm_api.api.v1.endpoints.relationship.relationship_service")
async def test_get_recognitions_given_by_agent(mock_service, async_test_client, agent_id, recognition_id, 
                                              agent_recognition_relationship):
    """Test getting Recognitions given by an Agent."""
    # Set up mock
    mock_service.get_relationships = AsyncMock(return_value=[Relationship(**agent_recognition_relationship)])

    # Call API
    response = await async_test_client.get(f"/api/v1/relationships/agents/{agent_id}/gives-recognitions")
    
    # Assertions
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["source_id"] == agent_id
    assert data[0]["target_id"] == recognition_id
    assert data[0]["type"] == "GIVEN_BY"
    
    # Verify service was called correctly
    mock_service.get_relationships.assert_called_once()


@pytest.mark.asyncio
@patch("trm_api.api.v1.endpoints.relationship.relationship_service")
async def test_get_agents_giving_recognition(mock_service, async_test_client, agent_id, recognition_id, 
                                            agent_recognition_relationship):
    """Test getting Agents that gave a Recognition."""
    # Set up mock
    mock_service.get_relationships = AsyncMock(return_value=[Relationship(**agent_recognition_relationship)])

    # Call API using async client
    response = await async_test_client.get(f"/api/v1/relationships/recognitions/{recognition_id}/given-by")
    
    # Assertions
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["source_id"] == agent_id
    assert data[0]["target_id"] == recognition_id
    assert data[0]["type"] == "GIVEN_BY"
    
    # Verify service was called correctly
    mock_service.get_relationships.assert_called_once()


@pytest.mark.asyncio
@patch("trm_api.api.v1.endpoints.relationship.relationship_service")
async def test_get_empty_recognitions_given_by_agent(mock_service, async_test_client, agent_id):
    """Test getting Recognitions when Agent has no relationships."""
    # Set up mock
    mock_service.get_relationships = AsyncMock(return_value=[])
    
    # Call API using async client
    response = await async_test_client.get(f"/api/v1/relationships/agents/{agent_id}/gives-recognitions")
    
    # Assertions
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 0
    
    # Verify service was called correctly
    mock_service.get_relationships.assert_called_once()


@pytest.mark.asyncio
@patch("trm_api.api.v1.endpoints.relationship.relationship_service")
async def test_delete_given_by_relationship(mock_service, async_test_client, agent_id, recognition_id):
    """Test deleting a GIVEN_BY relationship."""
    # Set up mock
    mock_service.delete_relationship = AsyncMock(return_value=True)
    
    # Call API using async client
    response = await async_test_client.delete(
        f"/api/v1/relationships/given-by?agent_id={agent_id}&recognition_id={recognition_id}"
    )
    
    # Assertions
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Verify service was called correctly
    mock_service.delete_relationship.assert_called_once()


@pytest.mark.asyncio
@patch("trm_api.api.v1.endpoints.relationship.relationship_service")
async def test_delete_given_by_relationship_not_found(mock_service, async_test_client, agent_id, recognition_id):
    """Test deleting a non-existent GIVEN_BY relationship."""
    # Set up mock
    mock_service.delete_relationship = AsyncMock(return_value=False)

    # Call API using async client
    response = await async_test_client.delete(
        f"/api/v1/relationships/given-by?agent_id={agent_id}&recognition_id={recognition_id}"
    )
    
    # Assertions
    assert response.status_code == status.HTTP_404_NOT_FOUND
    
    # Verify service was called correctly
    mock_service.delete_relationship.assert_called_once()
