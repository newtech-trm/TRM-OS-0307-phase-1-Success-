"""
Event API Integration Tests
==========================

Tests for Event entity CRUD operations.
Covers all requirements from COMPREHENSIVE_COVERAGE_ANALYSIS.md:
- Create Test ✅
- Read Test ✅ 
- Update Test ✅
- Delete Test ✅
"""

import pytest
import requests
from datetime import datetime
from typing import Dict, Any, List
import uuid
from fastapi.testclient import TestClient

from trm_api.main import app

class TestEventAPIIntegration:
    """Comprehensive Event API integration tests"""
    
    def setup_method(self):
        """Setup for each test method"""
        self.client = TestClient(app)
        self.base_url = "http://testserver/api/v1"
        
        self.test_event_data = {
            "name": "TEST_EVENT_CREATED",
            "description": "Test event created for integration testing",
            "actor_uid": str(uuid.uuid4()),  # Required field
            "payload": {
                "test_type": "integration",
                "entity": "event",
                "operation": "crud"
            },
            "tags": ["test", "integration", "crud"]
        }
        
        self.created_events = []  # Track for cleanup
    
    def teardown_method(self):
        """Cleanup after each test method"""
        # Clean up any created events
        for event_uid in self.created_events:
            try:
                self.client.delete(f"/api/v1/events/{event_uid}")
            except:
                pass  # Ignore cleanup errors
    
    def delete_entity(self, entity_type: str, entity_id: str):
        """Helper method to delete an entity"""
        return self.client.delete(f"/api/v1/{entity_type}/{entity_id}")
    
    # ========================================
    # CREATE TESTS
    # ========================================
    
    def test_create_event_success(self):
        """Test successful event creation"""
        # Create event
        response = self.client.post("/api/v1/events/", json=self.test_event_data)
        
        assert response.status_code == 201
        created_event = response.json()
        
        # Verify response structure
        assert "uid" in created_event
        assert created_event["name"] == self.test_event_data["name"]
        assert created_event["description"] == self.test_event_data["description"]
        assert created_event["payload"] == self.test_event_data["payload"]
        assert created_event["tags"] == self.test_event_data["tags"]
        assert "created_at" in created_event
        assert "updated_at" in created_event
        
        # Track for cleanup
        self.created_events.append(created_event["uid"])
    
    def test_create_event_minimal_data(self):
        """Test event creation with minimal required data"""
        minimal_data = {
            "name": "MINIMAL_TEST_EVENT"
        }
        
        response = self.client.post("/api/v1/events/", json=minimal_data)
        
        assert response.status_code == 201
        created_event = response.json()
        
        assert created_event["name"] == minimal_data["name"]
        assert created_event["description"] is None or created_event["description"] == ""
        assert created_event["payload"] is None or created_event["payload"] == {}
        assert created_event["tags"] == [] or created_event["tags"] is None
        
        self.created_events.append(created_event["uid"])
    
    def test_create_event_validation_error(self):
        """Test event creation with invalid data"""
        invalid_data = {
            # Missing required 'name' field
            "description": "Event without name"
        }
        
        response = requests.post(f"{self.base_url}/events/", json=invalid_data)
        
        # Should return validation error (422) or bad request (400)
        assert response.status_code in [400, 422]
    
    def test_create_event_with_complex_payload(self):
        """Test event creation with complex payload structure"""
        complex_data = {
            "name": "COMPLEX_EVENT_TEST",
            "description": "Event with complex nested payload",
            "payload": {
                "user_action": {
                    "type": "task_completion",
                    "task_id": str(uuid.uuid4()),
                    "metadata": {
                        "completion_time": "2025-01-07T10:00:00Z",
                        "quality_score": 95.5,
                        "tags": ["high-priority", "feature-dev"]
                    }
                },
                "system_context": {
                    "agent_id": str(uuid.uuid4()),
                    "session_id": str(uuid.uuid4()),
                    "environment": "production"
                }
            },
            "tags": ["complex", "nested", "production"]
        }
        
        response = requests.post(f"{self.base_url}/events/", json=complex_data)
        
        assert response.status_code == 201
        created_event = response.json()
        assert created_event["payload"] == complex_data["payload"]
        
        self.created_events.append(created_event["uid"])
    
    # ========================================
    # READ TESTS  
    # ========================================
    
    def test_get_event_by_id_success(self):
        """Test retrieving event by ID"""
        # First create an event
        create_response = requests.post(f"{self.base_url}/events/", json=self.test_event_data)
        assert create_response.status_code == 201
        created_event = create_response.json()
        event_uid = created_event["uid"]
        
        # Get the event by ID
        get_response = requests.get(f"{self.base_url}/events/{event_uid}")
        
        assert get_response.status_code == 200
        retrieved_event = get_response.json()
        
        # Verify data matches
        assert retrieved_event["uid"] == event_uid
        assert retrieved_event["name"] == self.test_event_data["name"]
        assert retrieved_event["description"] == self.test_event_data["description"]
        assert retrieved_event["payload"] == self.test_event_data["payload"]
        assert retrieved_event["tags"] == self.test_event_data["tags"]
        
        self.created_events.append(event_uid)
    
    def test_get_event_not_found(self):
        """Test retrieving non-existent event"""
        fake_uid = str(uuid.uuid4())
        
        response = requests.get(f"{self.base_url}/events/{fake_uid}")
        
        assert response.status_code == 404
    
    def test_list_events_success(self):
        """Test listing all events"""
        # Create multiple events for testing
        events_to_create = [
            {
                "name": f"LIST_TEST_EVENT_{i}",
                "description": f"Event {i} for list testing",
                "tags": ["list-test", f"event-{i}"]
            }
            for i in range(1, 4)
        ]
        
        created_uids = []
        for event_data in events_to_create:
            response = requests.post(f"{self.base_url}/events/", json=event_data)
            assert response.status_code == 201
            created_event = response.json()
            created_uids.append(created_event["uid"])
            self.created_events.append(created_event["uid"])
        
        # List events
        list_response = requests.get(f"{self.base_url}/events/")
        
        assert list_response.status_code == 200
        events_list = list_response.json()
        
        # Verify response is a list
        assert isinstance(events_list, list)
        assert len(events_list) >= len(events_to_create)
        
        # Verify our created events are in the list
        event_uids_in_list = [event["uid"] for event in events_list]
        for created_uid in created_uids:
            assert created_uid in event_uids_in_list
    
    def test_list_events_pagination(self):
        """Test listing events with pagination"""
        # Test with pagination parameters
        response = requests.get(f"{self.base_url}/events/?skip=0&limit=5")
        
        assert response.status_code == 200
        events_list = response.json()
        
        assert isinstance(events_list, list)
        assert len(events_list) <= 5  # Should respect limit
    
    # ========================================
    # UPDATE TESTS
    # ========================================
    
    def test_update_event_success(self):
        """Test successful event update"""
        # First create an event
        create_response = requests.post(f"{self.base_url}/events/", json=self.test_event_data)
        assert create_response.status_code == 201
        created_event = create_response.json()
        event_uid = created_event["uid"]
        
        # Update the event
        update_data = {
            "name": "UPDATED_TEST_EVENT",
            "description": "Updated description for testing",
            "payload": {
                "updated": True,
                "update_time": datetime.now().isoformat()
            },
            "tags": ["updated", "test", "modified"]
        }
        
        update_response = requests.put(f"{self.base_url}/events/{event_uid}", json=update_data)
        
        assert update_response.status_code == 200
        updated_event = update_response.json()
        
        # Verify updates
        assert updated_event["uid"] == event_uid
        assert updated_event["name"] == update_data["name"]
        assert updated_event["description"] == update_data["description"]
        assert updated_event["payload"] == update_data["payload"]
        assert updated_event["tags"] == update_data["tags"]
        
        # Verify updated_at changed
        assert updated_event["updated_at"] != created_event["updated_at"]
        
        self.created_events.append(event_uid)
    
    def test_update_event_partial(self):
        """Test partial event update"""
        # Create an event
        create_response = requests.post(f"{self.base_url}/events/", json=self.test_event_data)
        assert create_response.status_code == 201
        created_event = create_response.json()
        event_uid = created_event["uid"]
        
        # Partial update - only description
        partial_update = {
            "description": "Partially updated description"
        }
        
        update_response = requests.put(f"{self.base_url}/events/{event_uid}", json=partial_update)
        
        assert update_response.status_code == 200
        updated_event = update_response.json()
        
        # Verify only description changed
        assert updated_event["description"] == partial_update["description"]
        assert updated_event["name"] == self.test_event_data["name"]  # Unchanged
        assert updated_event["payload"] == self.test_event_data["payload"]  # Unchanged
        
        self.created_events.append(event_uid)
    
    def test_update_event_not_found(self):
        """Test updating non-existent event"""
        fake_uid = str(uuid.uuid4())
        update_data = {"name": "Updated Non-existent Event"}
        
        response = requests.put(f"{self.base_url}/events/{fake_uid}", json=update_data)
        
        assert response.status_code == 404
    
    # ========================================
    # DELETE TESTS
    # ========================================
    
    def test_delete_event_success(self):
        """Test successful event deletion"""
        # Create an event
        create_response = requests.post(f"{self.base_url}/events/", json=self.test_event_data)
        assert create_response.status_code == 201
        created_event = create_response.json()
        event_uid = created_event["uid"]
        
        # Delete the event
        delete_response = requests.delete(f"{self.base_url}/events/{event_uid}")
        
        assert delete_response.status_code == 204  # No content
        
        # Verify event is deleted by trying to get it
        get_response = requests.get(f"{self.base_url}/events/{event_uid}")
        assert get_response.status_code == 404
        
        # Don't add to cleanup list since it's already deleted
    
    def test_delete_event_not_found(self):
        """Test deleting non-existent event"""
        fake_uid = str(uuid.uuid4())
        
        response = requests.delete(f"{self.base_url}/events/{fake_uid}")
        
        assert response.status_code == 404
    
    def test_delete_event_cascade_behavior(self):
        """Test event deletion and related data cleanup"""
        # Create an event with relationships (if applicable)
        create_response = requests.post(f"{self.base_url}/events/", json=self.test_event_data)
        assert create_response.status_code == 201
        created_event = create_response.json()
        event_uid = created_event["uid"]
        
        # TODO: If Events have relationships to other entities,
        # test that deletion handles them properly
        
        # Delete the event
        delete_response = requests.delete(f"{self.base_url}/events/{event_uid}")
        assert delete_response.status_code == 204
        
        # Verify deletion
        get_response = requests.get(f"{self.base_url}/events/{event_uid}")
        assert get_response.status_code == 404
    
    # ========================================
    # EDGE CASES & ERROR HANDLING
    # ========================================
    
    def test_event_immutability_concept(self):
        """Test event immutability concept (if implemented)"""
        # Note: Events are often considered immutable in event-driven systems
        # This test checks if the system enforces any immutability rules
        
        # Create an event
        create_response = requests.post(f"{self.base_url}/events/", json=self.test_event_data)
        assert create_response.status_code == 201
        created_event = create_response.json()
        event_uid = created_event["uid"]
        
        # Try to update core immutable fields (like event name or timestamp)
        immutable_update = {
            "name": "CHANGED_IMMUTABLE_NAME",
            "created_at": "2020-01-01T00:00:00Z"  # Try to change creation time
        }
        
        update_response = requests.put(f"{self.base_url}/events/{event_uid}", json=immutable_update)
        
        # Depending on implementation:
        # - Might succeed but ignore immutable fields
        # - Might return error for immutable field updates
        # - Might succeed and allow changes (if not enforcing immutability)
        
        if update_response.status_code == 200:
            updated_event = update_response.json()
            # Verify created_at wasn't changed
            assert updated_event["created_at"] == created_event["created_at"]
        
        self.created_events.append(event_uid)
    
    def test_event_large_payload(self):
        """Test event with large payload data"""
        large_payload = {
            "large_data": "x" * 10000,  # 10KB string
            "repeated_data": [{"item": i, "data": "test" * 100} for i in range(100)]
        }
        
        large_event_data = {
            "name": "LARGE_PAYLOAD_EVENT",
            "description": "Event with large payload for testing limits",
            "payload": large_payload,
            "tags": ["large", "payload", "test"]
        }
        
        response = requests.post(f"{self.base_url}/events/", json=large_event_data)
        
        # Should either succeed or return appropriate error for oversized payload
        if response.status_code == 201:
            created_event = response.json()
            assert len(str(created_event["payload"])) > 5000  # Verify large payload preserved
            self.created_events.append(created_event["uid"])
        else:
            # If there are size limits, expect appropriate error
            assert response.status_code in [400, 413]  # Bad Request or Payload Too Large
    
    def test_event_special_characters(self):
        """Test event with special characters and Unicode"""
        special_data = {
            "name": "SPECIAL_CHARS_EVENT",
            "description": "Event with special chars: áéíóú ñ 中文 🚀 💯 \\n\\t\\r",
            "payload": {
                "unicode_text": "Testing Unicode: 中文测试 العربية עברית русский",
                "special_chars": "!@#$%^&*()_+-=[]{}|;:'\",.<>?/`~",
                "escaped_chars": "\\n\\t\\r\\\"\\'\\\\"
            },
            "tags": ["unicode", "special", "characters", "🔥"]
        }
        
        response = requests.post(f"{self.base_url}/events/", json=special_data)
        
        assert response.status_code == 201
        created_event = response.json()
        
        # Verify special characters preserved
        assert created_event["description"] == special_data["description"]
        assert created_event["payload"]["unicode_text"] == special_data["payload"]["unicode_text"]
        
        self.created_events.append(created_event["uid"])


class TestEventAPIValidation:
    """Additional validation tests for Event API"""
    
    def setup_method(self):
        """Setup for each test method"""
        self.client = TestClient(app)
        self.base_url = "http://testserver/api/v1"
    
    def test_event_name_validation(self):
        """Test event name field validation"""
        test_cases = [
            ("", 400),  # Empty name
            ("a" * 1000, 400),  # Very long name
            ("VALID_EVENT_NAME", 201),  # Valid name
            ("Event With Spaces", 201),  # Name with spaces
            ("Event-With-Dashes", 201),  # Name with dashes
            ("Event_With_Underscores", 201),  # Name with underscores
        ]
        
        created_events = []
        
        for name, expected_status in test_cases:
            event_data = {"name": name}
            response = requests.post(f"{self.base_url}/events/", json=event_data)
            
            assert response.status_code == expected_status, f"Failed for name: '{name}'"
            
            if response.status_code == 201:
                created_event = response.json()
                created_events.append(created_event["uid"])
        
        # Cleanup
        for event_uid in created_events:
            try:
                requests.delete(f"{self.base_url}/events/{event_uid}")
            except:
                pass
    
    def test_event_tags_validation(self):
        """Test event tags field validation"""
        valid_tags_event = {
            "name": "TAGS_TEST_EVENT",
            "tags": ["valid", "tags", "list"]
        }
        
        response = requests.post(f"{self.base_url}/events/", json=valid_tags_event)
        assert response.status_code == 201
        
        created_event = response.json()
        assert created_event["tags"] == valid_tags_event["tags"]
        
        # Cleanup
        requests.delete(f"{self.base_url}/events/{created_event['uid']}")


class TestEventAPIPerformance:
    """Performance tests for Event API"""
    
    def setup_method(self):
        """Setup for each test method"""
        self.client = TestClient(app)
        self.base_url = "http://testserver/api/v1"
    
    def test_bulk_event_creation(self):
        """Test creating multiple events in sequence"""
        num_events = 10
        created_events = []
        
        start_time = datetime.now()
        
        for i in range(num_events):
            event_data = {
                "name": f"BULK_EVENT_{i}",
                "description": f"Bulk event number {i}",
                "payload": {"index": i, "test": "bulk_creation"},
                "tags": ["bulk", "performance", f"event-{i}"]
            }
            
            response = requests.post(f"{self.base_url}/events/", json=event_data)
            assert response.status_code == 201
            
            created_event = response.json()
            created_events.append(created_event["uid"])
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        # Performance assertion - should create 10 events in reasonable time
        assert duration < 10.0, f"Bulk creation took too long: {duration} seconds"
        assert len(created_events) == num_events
        
        # Cleanup
        for event_uid in created_events:
            try:
                requests.delete(f"{self.base_url}/events/{event_uid}")
            except:
                pass 