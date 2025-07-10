"""
Comprehensive integration tests for TRM-OS Tension API

This module tests all Tension entity operations including CRUD operations,
validation, relationships, and performance characteristics.
"""

import asyncio
import json
import pytest
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from urllib.parse import urljoin

import httpx
from fastapi.testclient import TestClient

# Internal imports
from trm_api.main import app

import uuid

class TestTensionAPIIntegration:
    """Comprehensive Tension API integration tests"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup for each test method"""
        self.client = TestClient(app)
        self.base_url = "http://testserver/api/v1"
        
        self.test_tension_data = {
            "title": "Test Tension for Integration Testing",
            "description": "This is a detailed description of the test tension created for integration testing purposes. It describes the gap between current state and desired state.",
            "tensionType": "Problem",
            "status": "Open",
            "priority": "medium",
            "source": "FounderInput",
            "currentState": "Current situation has inefficiencies in the testing process",
            "desiredState": "Comprehensive automated testing with full coverage",
            "impactAssessment": "Without proper testing, system reliability is at risk",
            "tags": ["testing", "integration", "quality", "automation"]
        }
        
        self.created_tensions = []  # Track for cleanup
        yield
        
        # Cleanup after each test method
        for tension_uid in self.created_tensions:
            try:
                self.client.delete(f"/api/v1/tensions/{tension_uid}")
            except:
                pass  # Ignore cleanup errors
    
    # ========================================
    # CREATE TESTS
    # ========================================
    
    def test_create_tension_success(self):
        """Test successful tension creation"""
        # Create tension using TestClient
        response = self.client.post("/api/v1/tensions/", json=self.test_tension_data)
        
        assert response.status_code == 201
        created_tension = response.json()
        
        # Verify response structure
        assert "uid" in created_tension or "tensionId" in created_tension
        tension_id = created_tension.get("uid") or created_tension.get("tensionId")
        
        assert created_tension["title"] == self.test_tension_data["title"]
        assert created_tension["description"] == self.test_tension_data["description"]
        assert created_tension["tensionType"] == self.test_tension_data["tensionType"]
        assert created_tension["status"] == self.test_tension_data["status"]
        assert created_tension["priority"] == self.test_tension_data["priority"]
        assert created_tension["source"] == self.test_tension_data["source"]
        assert created_tension["currentState"] == self.test_tension_data["currentState"]
        assert created_tension["desiredState"] == self.test_tension_data["desiredState"]
        assert created_tension["impactAssessment"] == self.test_tension_data["impactAssessment"]
        assert created_tension["tags"] == self.test_tension_data["tags"]
        assert "creationDate" in created_tension
        assert "lastModifiedDate" in created_tension
        
        # Track for cleanup
        self.created_tensions.append(tension_id)
    
    def test_create_tension_minimal_data(self):
        """Test tension creation with minimal required data"""
        minimal_data = {
            "title": "Minimal Test Tension",
            "description": "This is the minimum required description for a tension that must be at least this long to pass validation."
        }
        
        response = self.client.post("/api/v1/tensions/", json=minimal_data)
        
        assert response.status_code == 201
        created_tension = response.json()
        
        assert created_tension["title"] == minimal_data["title"]
        assert created_tension["description"] == minimal_data["description"]
        
        # Verify default values
        assert created_tension["status"] == "Open"  # Default status
        assert created_tension["priority"] in ["medium", "Medium", 0]  # Default priority
        assert created_tension["source"] == "FounderInput"  # Default source
        
        tension_id = created_tension.get("uid") or created_tension.get("tensionId")
        self.created_tensions.append(tension_id)
    
    def test_create_tension_validation_error(self):
        """Test tension creation with invalid data"""
        invalid_data_cases = [
            # Missing required title
            {
                "description": "Description without title"
            },
            # Missing required description  
            {
                "title": "Title without description"
            },
            # Title too short
            {
                "title": "Short",
                "description": "This description is long enough but title is too short"
            },
            # Invalid tension type
            {
                "title": "Valid Title Length",
                "description": "Valid description that is long enough to pass validation",
                "tensionType": "InvalidType"
            },
            # Invalid priority
            {
                "title": "Valid Title Length",
                "description": "Valid description that is long enough to pass validation", 
                "priority": "invalid_priority"
            },
            # Invalid status
            {
                "title": "Valid Title Length",
                "description": "Valid description that is long enough to pass validation",
                "status": "InvalidStatus"
            }
        ]
        
        for invalid_data in invalid_data_cases:
            response = self.client.post("/api/v1/tensions/", json=invalid_data)
            # Should return validation error (422) or bad request (400)
            assert response.status_code in [400, 422], f"Failed for data: {invalid_data}"
    
    def test_create_tension_all_types(self):
        """Test creating tensions of all valid types"""
        tension_types = ["Problem", "Opportunity", "Risk", "Idea", "Question", "Concern"]
        
        for tension_type in tension_types:
            tension_data = {
                "title": f"Test {tension_type} Tension",
                "description": f"This is a test {tension_type.lower()} tension created for validation testing purposes.",
                "tensionType": tension_type,
                "tags": ["test", tension_type.lower()]
            }
            
            response = self.client.post("/api/v1/tensions/", json=tension_data)
            
            assert response.status_code == 201, f"Failed to create {tension_type} tension"
            created_tension = response.json()
            assert created_tension["tensionType"] == tension_type
            
            tension_id = created_tension.get("uid") or created_tension.get("tensionId")
            self.created_tensions.append(tension_id)
    
    def test_create_tension_all_priorities(self):
        """Test creating tensions with all valid priorities"""
        priorities = ["low", "medium", "high", "critical"]
        
        for priority in priorities:
            tension_data = {
                "title": f"Test {priority.title()} Priority Tension",
                "description": f"This is a test tension with {priority} priority level for validation testing.",
                "priority": priority,
                "tags": ["test", "priority", priority]
            }
            
            response = self.client.post("/api/v1/tensions/", json=tension_data)
            
            assert response.status_code == 201, f"Failed to create {priority} priority tension"
            created_tension = response.json()
            assert created_tension["priority"] in [priority, priority.title()]
            
            tension_id = created_tension.get("uid") or created_tension.get("tensionId")
            self.created_tensions.append(tension_id)
    
    # ========================================
    # READ TESTS  
    # ========================================
    
    def test_get_tension_by_id_success(self):
        """Test retrieving tension by ID"""
        # First create a tension
        create_response = self.client.post("/api/v1/tensions/", json=self.test_tension_data)
        assert create_response.status_code == 201
        created_tension = create_response.json()
        tension_id = created_tension.get("uid") or created_tension.get("tensionId")
        
        # Get the tension by ID
        get_response = self.client.get(f"/api/v1/tensions/{tension_id}")
        
        assert get_response.status_code == 200
        retrieved_tension = get_response.json()
        
        # Verify data matches
        retrieved_id = retrieved_tension.get("uid") or retrieved_tension.get("tensionId")
        assert retrieved_id == tension_id
        assert retrieved_tension["title"] == self.test_tension_data["title"]
        assert retrieved_tension["description"] == self.test_tension_data["description"]
        assert retrieved_tension["tensionType"] == self.test_tension_data["tensionType"]
        assert retrieved_tension["status"] == self.test_tension_data["status"]
        assert retrieved_tension["currentState"] == self.test_tension_data["currentState"]
        assert retrieved_tension["desiredState"] == self.test_tension_data["desiredState"]
        
        self.created_tensions.append(tension_id)
    
    def test_get_tension_not_found(self):
        """Test retrieving non-existent tension"""
        fake_uid = str(uuid.uuid4())
        
        response = self.client.get(f"/api/v1/tensions/{fake_uid}")
        
        assert response.status_code == 404
    
    def test_list_tensions_success(self):
        """Test listing all tensions"""
        # Create multiple tensions for testing
        tensions_to_create = [
            {
                "title": f"List Test Tension Number {i}",
                "description": f"This is tension {i} created for list testing purposes with sufficient description length.",
                "tensionType": ["Problem", "Opportunity", "Risk"][i % 3],
                "tags": ["list-test", f"tension-{i}"]
            }
            for i in range(1, 4)
        ]
        
        created_ids = []
        for tension_data in tensions_to_create:
            response = self.client.post("/api/v1/tensions/", json=tension_data)
            assert response.status_code == 201
            created_tension = response.json()
            tension_id = created_tension.get("uid") or created_tension.get("tensionId")
            created_ids.append(tension_id)
            self.created_tensions.append(tension_id)
        
        # List tensions
        list_response = self.client.get("/api/v1/tensions/")
        
        assert list_response.status_code == 200
        tensions_list = list_response.json()
        
        # Verify response is a list
        assert isinstance(tensions_list, list)
        assert len(tensions_list) >= len(tensions_to_create)
        
        # Verify our created tensions are in the list
        tension_ids_in_list = [t.get("uid") or t.get("tensionId") for t in tensions_list]
        for created_id in created_ids:
            assert created_id in tension_ids_in_list
    
    def test_list_tensions_pagination(self):
        """Test listing tensions with pagination"""
        # Test with pagination parameters
        response = self.client.get("/api/v1/tensions/?skip=0&limit=5")
        
        assert response.status_code == 200
        tensions_list = response.json()
        
        assert isinstance(tensions_list, list)
        assert len(tensions_list) <= 5  # Should respect limit
    
    # ========================================
    # UPDATE TESTS
    # ========================================
    
    def test_update_tension_success(self):
        """Test successful tension update"""
        # First create a tension
        create_response = self.client.post("/api/v1/tensions/", json=self.test_tension_data)
        assert create_response.status_code == 201
        created_tension = create_response.json()
        tension_id = created_tension.get("uid") or created_tension.get("tensionId")
        
        # Update the tension
        update_data = {
            "title": "Updated Test Tension Title",
            "description": "This is the updated description for the test tension with sufficient length for validation.",
            "status": "InProgress",
            "priority": "high",
            "tensionType": "Opportunity",
            "currentState": "Updated current state description",
            "desiredState": "Updated desired state description",
            "impactAssessment": "Updated impact assessment",
            "tags": ["updated", "test", "modified"]
        }
        
        update_response = self.client.put(f"/api/v1/tensions/{tension_id}", json=update_data)
        
        assert update_response.status_code == 200
        updated_tension = update_response.json()
        
        # Verify updates
        updated_id = updated_tension.get("uid") or updated_tension.get("tensionId")
        assert updated_id == tension_id
        assert updated_tension["title"] == update_data["title"]
        assert updated_tension["description"] == update_data["description"]
        assert updated_tension["status"] == update_data["status"]
        assert updated_tension["priority"] in [update_data["priority"], update_data["priority"].title()]
        assert updated_tension["tensionType"] == update_data["tensionType"]
        assert updated_tension["currentState"] == update_data["currentState"]
        assert updated_tension["desiredState"] == update_data["desiredState"]
        assert updated_tension["impactAssessment"] == update_data["impactAssessment"]
        assert updated_tension["tags"] == update_data["tags"]
        
        # Verify lastModifiedDate changed
        assert updated_tension["lastModifiedDate"] != created_tension["lastModifiedDate"]
        
        self.created_tensions.append(tension_id)
    
    def test_update_tension_partial(self):
        """Test partial tension update"""
        # Create a tension
        create_response = self.client.post("/api/v1/tensions/", json=self.test_tension_data)
        assert create_response.status_code == 201
        created_tension = create_response.json()
        tension_id = created_tension.get("uid") or created_tension.get("tensionId")
        
        # Partial update - only status and priority
        partial_update = {
            "status": "Resolved",
            "priority": "low"
        }
        
        update_response = self.client.put(f"/api/v1/tensions/{tension_id}", json=partial_update)
        
        assert update_response.status_code == 200
        updated_tension = update_response.json()
        
        # Verify only specified fields changed
        assert updated_tension["status"] == partial_update["status"]
        assert updated_tension["priority"] in [partial_update["priority"], partial_update["priority"].title()]
        assert updated_tension["title"] == self.test_tension_data["title"]  # Unchanged
        assert updated_tension["description"] == self.test_tension_data["description"]  # Unchanged
        
        self.created_tensions.append(tension_id)
    
    def test_update_tension_status_progression(self):
        """Test tension status progression workflow"""
        # Create a tension
        create_response = self.client.post("/api/v1/tensions/", json=self.test_tension_data)
        assert create_response.status_code == 201
        created_tension = create_response.json()
        tension_id = created_tension.get("uid") or created_tension.get("tensionId")
        
        # Test status progression: Open -> InProgress -> Resolved -> Closed
        status_progression = ["InProgress", "Resolved", "Closed"]
        
        for status in status_progression:
            update_data = {"status": status}
            if status == "Resolved":
                update_data["resolutionDate"] = datetime.now().isoformat()
            
            update_response = self.client.put(f"/api/v1/tensions/{tension_id}", json=update_data)
            assert update_response.status_code == 200
            
            updated_tension = update_response.json()
            assert updated_tension["status"] == status
            
            if status == "Resolved":
                # Verify resolution date is set
                assert "resolutionDate" in updated_tension
        
        self.created_tensions.append(tension_id)
    
    def test_update_tension_not_found(self):
        """Test updating non-existent tension"""
        fake_uid = str(uuid.uuid4())
        update_data = {"title": "Updated Non-existent Tension"}
        
        response = self.client.put(f"/api/v1/tensions/{fake_uid}", json=update_data)
        
        assert response.status_code == 404
    
    # ========================================
    # DELETE TESTS
    # ========================================
    
    def test_delete_tension_success(self):
        """Test successful tension deletion"""
        # Create a tension
        create_response = self.client.post("/api/v1/tensions/", json=self.test_tension_data)
        assert create_response.status_code == 201
        created_tension = create_response.json()
        tension_id = created_tension.get("uid") or created_tension.get("tensionId")
        
        # Delete the tension
        delete_response = self.client.delete(f"/api/v1/tensions/{tension_id}")
        
        assert delete_response.status_code == 204  # No content
        
        # Verify tension is deleted by trying to get it
        get_response = self.client.get(f"/api/v1/tensions/{tension_id}")
        assert get_response.status_code == 404
        
        # Don't add to cleanup list since it's already deleted
    
    def test_delete_tension_not_found(self):
        """Test deleting non-existent tension"""
        fake_uid = str(uuid.uuid4())
        
        response = self.client.delete(f"/api/v1/tensions/{fake_uid}")
        
        assert response.status_code == 404
    
    def test_delete_tension_cascade_behavior(self):
        """Test tension deletion and related data cleanup"""
        # Create a tension with relationships (if applicable)
        create_response = self.client.post("/api/v1/tensions/", json=self.test_tension_data)
        assert create_response.status_code == 201
        created_tension = create_response.json()
        tension_id = created_tension.get("uid") or created_tension.get("tensionId")
        
        # TODO: If Tensions have relationships to other entities,
        # test that deletion handles them properly
        # (e.g., relationships to Tasks, Projects, Agents, WINs)
        
        # Delete the tension
        delete_response = self.client.delete(f"/api/v1/tensions/{tension_id}")
        assert delete_response.status_code == 204
        
        # Verify deletion
        get_response = self.client.get(f"/api/v1/tensions/{tension_id}")
        assert get_response.status_code == 404
    
    # ========================================
    # EDGE CASES & ERROR HANDLING
    # ========================================
    
    def test_tension_markdown_description(self):
        """Test tension with markdown-formatted description"""
        markdown_data = {
            "title": "Tension with Markdown Description",
            "description": """# Detailed Tension Description

This tension involves multiple aspects:

## Current State
- **Problem**: System lacks proper monitoring
- **Impact**: *Downtime goes unnoticed*
- **Frequency**: `~3 times per month`

## Desired State
1. Real-time monitoring dashboard
2. Automated alerting system
3. Performance metrics tracking

### Technical Requirements
```python
def monitor_system():
    return check_health_status()
```

**Priority**: High due to customer impact.""",
            "tensionType": "Problem",
            "tags": ["monitoring", "technical-debt", "customer-impact"]
        }
        
        response = self.client.post("/api/v1/tensions/", json=markdown_data)
        
        assert response.status_code == 201
        created_tension = response.json()
        
        # Verify markdown content preserved
        assert created_tension["description"] == markdown_data["description"]
        assert "```python" in created_tension["description"]
        assert "**Priority**" in created_tension["description"]
        
        tension_id = created_tension.get("uid") or created_tension.get("tensionId")
        self.created_tensions.append(tension_id)
    
    def test_tension_special_characters(self):
        """Test tension with special characters and Unicode"""
        special_data = {
            "title": "Tension with Special Characters: áéíóú ñ 中文 🚀",
            "description": "This tension contains special characters and Unicode text: 中文测试 العربية עברית русский. Special chars: !@#$%^&*()_+-=[]{}|;:'\",.<>?/`~",
            "tensionType": "Idea",
            "currentState": "Current state with emoji: 😢 😞",
            "desiredState": "Desired state with emoji: 😊 🎉 ✅",
            "tags": ["unicode", "special", "characters", "🔥", "测试"]
        }
        
        response = self.client.post("/api/v1/tensions/", json=special_data)
        
        assert response.status_code == 201
        created_tension = response.json()
        
        # Verify special characters preserved
        assert created_tension["title"] == special_data["title"]
        assert created_tension["description"] == special_data["description"]
        assert created_tension["currentState"] == special_data["currentState"]
        assert created_tension["desiredState"] == special_data["desiredState"]
        assert created_tension["tags"] == special_data["tags"]
        
        tension_id = created_tension.get("uid") or created_tension.get("tensionId")
        self.created_tensions.append(tension_id)
    
    def test_tension_long_content(self):
        """Test tension with very long content"""
        long_description = "This is a very long description. " * 1000  # ~32KB
        long_current_state = "Current state details. " * 500  # ~16KB
        long_desired_state = "Desired state details. " * 500  # ~16KB
        
        long_content_data = {
            "title": "Tension with Extremely Long Content",
            "description": long_description,
            "currentState": long_current_state,
            "desiredState": long_desired_state,
            "tensionType": "Problem",
            "tags": ["long-content", "stress-test"]
        }
        
        response = self.client.post("/api/v1/tensions/", json=long_content_data)
        
        # Should either succeed or return appropriate error for oversized content
        if response.status_code == 201:
            created_tension = response.json()
            assert len(created_tension["description"]) > 30000
            tension_id = created_tension.get("uid") or created_tension.get("tensionId")
            self.created_tensions.append(tension_id)
        else:
            # If there are size limits, expect appropriate error
            assert response.status_code in [400, 413]  # Bad Request or Payload Too Large


class TestTensionAPIValidation:
    """Test Tension API validation behavior"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup for validation tests"""
        self.client = TestClient(app)
        yield
    
    def test_tension_title_validation(self):
        """Test tension title field validation"""
        base_description = "This is a valid description that meets the minimum length requirements for tension creation."
        
        test_cases = [
            ("", 400),  # Empty title
            ("Short", 400),  # Too short (less than 10 chars)
            ("a" * 300, 400),  # Too long (over 200 chars)
            ("Valid Test Title", 201),  # Valid title
            ("Title with Special Chars: áéíóú", 201),  # Unicode chars
            ("Title with Numbers 123", 201),  # Numbers
            ("Title-with-dashes", 201),  # Dashes
            ("Title_with_underscores", 201),  # Underscores
        ]
        
        created_tensions = []
        
        for title, expected_status in test_cases:
            tension_data = {
                "title": title,
                "description": base_description
            }
            response = self.client.post("/api/v1/tensions/", json=tension_data)
            
            assert response.status_code == expected_status, f"Failed for title: '{title}'"
            
            if response.status_code == 201:
                created_tension = response.json()
                tension_id = created_tension.get("uid") or created_tension.get("tensionId")
                created_tensions.append(tension_id)
        
        # Cleanup
        for tension_id in created_tensions:
            try:
                self.client.delete(f"/api/v1/tensions/{tension_id}")
            except:
                pass
    
    def test_tension_tags_validation(self):
        """Test tension tags field validation"""
        valid_tags_tension = {
            "title": "Tags Validation Test Tension",
            "description": "This tension is created to test the tags field validation with various tag formats.",
            "tags": ["valid", "tags", "list", "with-dashes", "with_underscores", "123numbers", "🔥emoji"]
        }
        
        response = self.client.post("/api/v1/tensions/", json=valid_tags_tension)
        assert response.status_code == 201
        
        created_tension = response.json()
        assert created_tension["tags"] == valid_tags_tension["tags"]
        
        # Cleanup
        tension_id = created_tension.get("uid") or created_tension.get("tensionId")
        self.client.delete(f"/api/v1/tensions/{tension_id}")


class TestTensionAPIPerformance:
    """Test Tension API performance characteristics"""
    
    @pytest.fixture(autouse=True) 
    def setup(self):
        """Setup for performance tests"""
        self.client = TestClient(app)
        yield
    
    def test_bulk_tension_creation(self):
        """Test creating multiple tensions in sequence"""
        num_tensions = 10
        created_tensions = []
        
        start_time = datetime.now()
        
        for i in range(num_tensions):
            tension_data = {
                "title": f"Bulk Test Tension Number {i}",
                "description": f"This is bulk tension number {i} created for performance testing purposes with sufficient description length.",
                "tensionType": ["Problem", "Opportunity", "Risk"][i % 3],
                "priority": ["low", "medium", "high", "critical"][i % 4],
                "tags": ["bulk", "performance", f"tension-{i}"]
            }
            
            response = self.client.post("/api/v1/tensions/", json=tension_data)
            assert response.status_code == 201
            
            created_tension = response.json()
            tension_id = created_tension.get("uid") or created_tension.get("tensionId")
            created_tensions.append(tension_id)
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        # Performance assertion - should create 10 tensions in reasonable time
        assert duration < 15.0, f"Bulk creation took too long: {duration} seconds"
        assert len(created_tensions) == num_tensions
        
        # Cleanup
        for tension_id in created_tensions:
            try:
                self.client.delete(f"/api/v1/tensions/{tension_id}")
            except:
                pass 