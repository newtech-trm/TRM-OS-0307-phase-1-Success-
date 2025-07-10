"""
Comprehensive integration tests for GeneratesEventRel (GENERATES_EVENT) relationships.
Tests Project->Event, Task->Event, Agent->Event relationships.
"""

import pytest
import uuid
from datetime import datetime
from fastapi.testclient import TestClient
from trm_api.main import app
from trm_api.repositories.event_repository import EventRepository
from trm_api.db.session import db

class TestGeneratesEventRelationship:
    """Test class for GeneratesEventRel relationship operations"""
    
    def setup_method(self):
        """Setup for each test"""
        self.client = TestClient(app)
        self.event_repo = EventRepository()
        self.created_entities = []
        self.created_relationships = []
    
    def teardown_method(self):
        """Cleanup after each test"""
        # Clean up relationships and entities
        for entity_type, entity_uid in self.created_entities:
            try:
                if entity_type == "project":
                    self.client.delete(f"/api/v1/projects/{entity_uid}")
                elif entity_type == "task":
                    self.client.delete(f"/api/v1/tasks/{entity_uid}")
                elif entity_type == "agent":
                    self.client.delete(f"/api/v1/agents/{entity_uid}")
                elif entity_type == "event":
                    # Use repository to delete real GraphEvent
                    self.event_repo.delete_event(entity_uid)
            except Exception:
                pass
        
        self.created_entities = []
        self.created_relationships = []
    
    def _create_test_project(self, name_suffix="test"):
        """Helper to create a test project"""
        project_data = {
            "title": f"Test Project {name_suffix}",
            "description": f"Test project for GeneratesEvent relationship testing - {name_suffix}",
            "status": "active",
            "priority": 3
        }
        response = self.client.post("/api/v1/projects/", json=project_data)
        assert response.status_code == 201
        project = response.json()
        self.created_entities.append(("project", project["uid"]))
        return project
    
    def _create_test_task(self, name_suffix="test"):
        """Helper to create a test task"""
        # First create a project for the task
        project = self._create_test_project(f"project_for_task_{name_suffix}")
        
        task_data = {
            "name": f"Test Task {name_suffix}",
            "description": f"Test task for GeneratesEvent relationship testing - {name_suffix}",
            "status": "ToDo",
            "priority": 1,
            "project_id": project["uid"]
        }
        response = self.client.post("/api/v1/tasks/", json=task_data)
        assert response.status_code == 201
        task = response.json()
        self.created_entities.append(("task", task["uid"]))
        return task
    
    def _create_test_agent(self, name_suffix="test"):
        """Helper to create a test agent"""
        agent_data = {
            "name": f"Test Agent {name_suffix}",
            "agentType": "InternalAgent",
            "description": f"Test agent for GeneratesEvent relationship testing - {name_suffix}"
        }
        response = self.client.post("/api/v1/agents/", json=agent_data)
        assert response.status_code == 201
        agent = response.json()
        # Agent API returns "agentId" field, not "uid"
        self.created_entities.append(("agent", agent["agentId"]))
        # Add uid field for consistency with other entities
        agent["uid"] = agent["agentId"]
        return agent
    
    def _create_test_event(self, name_suffix="test", actor_uid=None):
        """Helper to create a test event using GraphEvent directly"""
        from trm_api.graph_models.event import Event as GraphEvent
        
        # Create event directly in Neo4j using GraphEvent
        graph_event = GraphEvent(
            name=f"TEST_EVENT_{name_suffix.upper()}",
            description=f"Test event for GeneratesEvent relationship testing - {name_suffix}",
            payload={"test": True, "suffix": name_suffix, "actor_uid": actor_uid}
        ).save()
        
        # Convert to dict format for consistency with API response
        event = {
            "uid": graph_event.uid,
            "name": graph_event.name,
            "description": graph_event.description,
            "payload": graph_event.payload,
            "created_at": graph_event.created_at.isoformat() if graph_event.created_at else None,
            "updated_at": graph_event.updated_at.isoformat() if graph_event.updated_at else None
        }
        
        self.created_entities.append(("event", event["uid"]))
        return event
    
    # ========== PROJECT->EVENT RELATIONSHIP TESTS ==========
    
    def test_create_project_generates_event_direct(self):
        """Test creating a direct Project->Event relationship"""
        # Create test entities
        project = self._create_test_project("project_direct")
        event = self._create_test_event("project_generated", project["uid"])
        
        # Create relationship using repository
        result = self.event_repo.connect_project_to_event(
            project_uid=project["uid"],
            event_uid=event["uid"],
            generation_type="Direct",
            impact=4,
            is_verified=True,
            verification_source="Integration Test",
            context="Direct project milestone completion",
            notes="Test project generates completion event"
        )
        
        assert result is not None
        project_node, event_node = result
        assert project_node.uid == project["uid"]
        assert event_node.uid == event["uid"]
        
        # Verify relationship properties via graph
        relationships = project_node.generates_events.all()
        assert len(relationships) == 1
        
        # Get relationship details
        rel = project_node.generates_events.relationship(event_node)
        assert rel.generationType == "Direct"
        assert rel.impact == 4
        assert rel.isVerified == True
        assert rel.verificationSource == "Integration Test"
        assert rel.context == "Direct project milestone completion"
        assert rel.notes == "Test project generates completion event"
    
    def test_create_project_generates_event_automated(self):
        """Test creating an automated Project->Event relationship"""
        project = self._create_test_project("project_automated")
        event = self._create_test_event("automated_update", project["uid"])
        
        result = self.event_repo.connect_project_to_event(
            project_uid=project["uid"],
            event_uid=event["uid"],
            generation_type="Automated",
            impact=2,
            context="Automated status update system"
        )
        
        assert result is not None
        project_node, event_node = result
        
        # Verify automated relationship
        rel = project_node.generates_events.relationship(event_node)
        assert rel.generationType == "Automated"
        assert rel.impact == 2
        assert rel.isVerified == False  # Default
        assert rel.context == "Automated status update system"
    
    def test_create_project_generates_multiple_events(self):
        """Test project generating multiple events"""
        project = self._create_test_project("multi_events")
        event1 = self._create_test_event("milestone1", project["uid"])
        event2 = self._create_test_event("milestone2", project["uid"])
        event3 = self._create_test_event("completion", project["uid"])
        
        # Create multiple relationships
        results = []
        generation_types = ["Direct", "Automated", "Manual"]
        impacts = [5, 3, 4]
        
        for i, (event, gen_type, impact) in enumerate(zip([event1, event2, event3], generation_types, impacts)):
            result = self.event_repo.connect_project_to_event(
                project_uid=project["uid"],
                event_uid=event["uid"],
                generation_type=gen_type,
                impact=impact,
                context=f"Project milestone {i+1}"
            )
            results.append(result)
            assert result is not None
        
        # Verify all relationships exist
        from trm_api.graph_models.project import Project as GraphProject
        project_node = GraphProject.nodes.get(uid=project["uid"])
        events = project_node.generates_events.all()
        assert len(events) == 3
        
        # Verify different generation types
        gen_types = []
        for event_node in events:
            rel = project_node.generates_events.relationship(event_node)
            gen_types.append(rel.generationType)
        
        assert "Direct" in gen_types
        assert "Automated" in gen_types
        assert "Manual" in gen_types
    
    # ========== TASK->EVENT RELATIONSHIP TESTS ==========
    
    def test_create_task_generates_event_direct(self):
        """Test creating a direct Task->Event relationship"""
        task = self._create_test_task("task_direct")
        event = self._create_test_event("task_completed", task["uid"])
        
        result = self.event_repo.connect_task_to_event(
            task_uid=task["uid"],
            event_uid=event["uid"],
            generation_type="Direct",
            impact=3,
            is_verified=True,
            verification_source="Task Manager",
            context="Task completion event",
            notes="Direct task completion generates status event"
        )
        
        assert result is not None
        task_node, event_node = result
        assert task_node.uid == task["uid"]
        assert event_node.uid == event["uid"]
        
        # Verify relationship properties
        rel = task_node.generates_events.relationship(event_node)
        assert rel.generationType == "Direct"
        assert rel.impact == 3
        assert rel.isVerified == True
        assert rel.verificationSource == "Task Manager"
        assert rel.context == "Task completion event"
    
    def test_create_task_generates_event_system(self):
        """Test creating a system-generated Task->Event relationship"""
        task = self._create_test_task("task_system")
        event = self._create_test_event("system_notification", task["uid"])
        
        result = self.event_repo.connect_task_to_event(
            task_uid=task["uid"],
            event_uid=event["uid"],
            generation_type="System",
            impact=1,
            context="System automated notification"
        )
        
        assert result is not None
        task_node, event_node = result
        
        rel = task_node.generates_events.relationship(event_node)
        assert rel.generationType == "System"
        assert rel.impact == 1
        assert rel.context == "System automated notification"
    
    def test_task_generates_workflow_events(self):
        """Test task generating multiple workflow events"""
        task = self._create_test_task("workflow_task")
        
        # Create workflow events
        start_event = self._create_test_event("task_started", task["uid"])
        progress_event = self._create_test_event("task_progress", task["uid"])
        complete_event = self._create_test_event("task_completed", task["uid"])
        
        # Create workflow relationships
        workflows = [
            (start_event, "Manual", 2, "Task initiation"),
            (progress_event, "Automated", 2, "Progress tracking"),
            (complete_event, "Direct", 4, "Task completion")
        ]
        
        for event, gen_type, impact, context in workflows:
            result = self.event_repo.connect_task_to_event(
                task_uid=task["uid"],
                event_uid=event["uid"],
                generation_type=gen_type,
                impact=impact,
                context=context
            )
            assert result is not None
        
        # Verify workflow sequence
        from trm_api.graph_models.task import Task as GraphTask
        task_node = GraphTask.nodes.get(uid=task["uid"])
        events = task_node.generates_events.all()
        assert len(events) == 3
    
    # ========== AGENT->EVENT RELATIONSHIP TESTS ==========
    
    def test_create_agent_generates_event_direct(self):
        """Test creating a direct Agent->Event relationship"""
        agent = self._create_test_agent("agent_direct")
        event = self._create_test_event("agent_action", agent["uid"])
        
        result = self.event_repo.connect_agent_to_event(
            agent_uid=agent["uid"],
            event_uid=event["uid"],
            generation_type="Direct",
            impact=4,
            is_verified=True,
            verification_source="Agent Monitor",
            context="Direct agent action",
            notes="Agent performs action generating event"
        )
        
        assert result is not None
        agent_node, event_node = result
        assert agent_node.uid == agent["uid"]
        assert event_node.uid == event["uid"]
        
        # Verify relationship properties
        rel = agent_node.generates_events.relationship(event_node)
        assert rel.generationType == "Direct"
        assert rel.impact == 4
        assert rel.isVerified == True
        assert rel.verificationSource == "Agent Monitor"
        assert rel.context == "Direct agent action"
    
    def test_create_agent_generates_event_manual(self):
        """Test creating a manual Agent->Event relationship"""
        agent = self._create_test_agent("agent_manual")
        event = self._create_test_event("manual_log", agent["uid"])
        
        result = self.event_repo.connect_agent_to_event(
            agent_uid=agent["uid"],
            event_uid=event["uid"],
            generation_type="Manual",
            impact=3,
            context="Manual agent logging"
        )
        
        assert result is not None
        agent_node, event_node = result
        
        rel = agent_node.generates_events.relationship(event_node)
        assert rel.generationType == "Manual"
        assert rel.impact == 3
        assert rel.context == "Manual agent logging"
    
    def test_agent_generates_activity_events(self):
        """Test agent generating multiple activity events"""
        agent = self._create_test_agent("active_agent")
        
        # Create activity events
        login_event = self._create_test_event("agent_login", agent["uid"])
        work_event = self._create_test_event("agent_work", agent["uid"])
        logout_event = self._create_test_event("agent_logout", agent["uid"])
        
        # Create activity relationships
        activities = [
            (login_event, "System", 1, "Agent login"),
            (work_event, "Direct", 3, "Agent work session"),
            (logout_event, "System", 1, "Agent logout")
        ]
        
        for event, gen_type, impact, context in activities:
            result = self.event_repo.connect_agent_to_event(
                agent_uid=agent["uid"],
                event_uid=event["uid"],
                generation_type=gen_type,
                impact=impact,
                context=context
            )
            assert result is not None
        
        # Verify activity tracking
        from trm_api.graph_models.agent import Agent
        agent_node = Agent.nodes.get(uid=agent["uid"])
        events = agent_node.generates_events.all()
        assert len(events) == 3
    
    # ========== VALIDATION TESTS ==========
    
    def test_invalid_project_generates_event(self):
        """Test generating event with invalid project"""
        event = self._create_test_event("invalid_project")
        
        result = self.event_repo.connect_project_to_event(
            project_uid="invalid-project-uid",
            event_uid=event["uid"],
            generation_type="Direct"
        )
        
        assert result is None
    
    def test_invalid_event_generates_relationship(self):
        """Test generating relationship with invalid event"""
        project = self._create_test_project("invalid_event")
        
        result = self.event_repo.connect_project_to_event(
            project_uid=project["uid"],
            event_uid="invalid-event-uid",
            generation_type="Direct"
        )
        
        assert result is None
    
    def test_generation_type_validation(self):
        """Test all valid generation types"""
        project = self._create_test_project("gen_types")
        
        valid_types = ["Direct", "Indirect", "Automated", "Manual", "System"]
        
        for gen_type in valid_types:
            event = self._create_test_event(f"type_{gen_type.lower()}", project["uid"])
            
            result = self.event_repo.connect_project_to_event(
                project_uid=project["uid"],
                event_uid=event["uid"],
                generation_type=gen_type,
                impact=2
            )
            
            assert result is not None
            project_node, event_node = result
            rel = project_node.generates_events.relationship(event_node)
            assert rel.generationType == gen_type
    
    def test_impact_level_validation(self):
        """Test impact levels 1-5"""
        task = self._create_test_task("impact_levels")
        
        for impact_level in range(1, 6):
            event = self._create_test_event(f"impact_{impact_level}", task["uid"])
            
            result = self.event_repo.connect_task_to_event(
                task_uid=task["uid"],
                event_uid=event["uid"],
                generation_type="Direct",
                impact=impact_level
            )
            
            assert result is not None
            task_node, event_node = result
            rel = task_node.generates_events.relationship(event_node)
            assert rel.impact == impact_level
    
    # ========== PERFORMANCE TESTS ==========
    
    def test_bulk_event_generation(self):
        """Test generating multiple events efficiently"""
        project = self._create_test_project("bulk_events")
        
        # Create 10 events and relationships
        for i in range(10):
            event = self._create_test_event(f"bulk_event_{i}", project["uid"])
            
            result = self.event_repo.connect_project_to_event(
                project_uid=project["uid"],
                event_uid=event["uid"],
                generation_type="Automated",
                impact=2,
                context=f"Bulk event generation test {i}"
            )
            assert result is not None
        
        # Verify all relationships
        from trm_api.graph_models.project import Project as GraphProject
        project_node = GraphProject.nodes.get(uid=project["uid"])
        events = project_node.generates_events.all()
        assert len(events) == 10
    
    def test_cross_entity_event_generation(self):
        """Test multiple entity types generating the same event"""
        # Create entities
        project = self._create_test_project("cross_entity")
        task = self._create_test_task("cross_entity")
        agent = self._create_test_agent("cross_entity")
        event = self._create_test_event("shared_event", agent["uid"])
        
        # All entities generate the same event
        results = []
        
        # Project generates event
        result1 = self.event_repo.connect_project_to_event(
            project_uid=project["uid"],
            event_uid=event["uid"],
            generation_type="Direct",
            context="Project milestone"
        )
        results.append(result1)
        
        # Task generates event
        result2 = self.event_repo.connect_task_to_event(
            task_uid=task["uid"],
            event_uid=event["uid"],
            generation_type="Direct",
            context="Task completion"
        )
        results.append(result2)
        
        # Agent generates event
        result3 = self.event_repo.connect_agent_to_event(
            agent_uid=agent["uid"],
            event_uid=event["uid"],
            generation_type="Direct",
            context="Agent action"
        )
        results.append(result3)
        
        # Verify all relationships
        assert all(result is not None for result in results)
        
        # Verify event has multiple generators
        from trm_api.graph_models.event import Event
        event_node = Event.nodes.get(uid=event["uid"])
        
        # Count incoming GENERATES_EVENT relationships
        projects = event_node.generated_by_projects.all()
        tasks = event_node.generated_by_tasks.all()
        agents = event_node.generated_by_agents.all()
        
        assert len(projects) == 1
        assert len(tasks) == 1
        assert len(agents) == 1


class TestGeneratesEventRelationshipValidation:
    """Test class for GeneratesEventRel validation and error handling"""
    
    def setup_method(self):
        """Setup for each test"""
        self.client = TestClient(app)
        self.event_repo = EventRepository()
        self.created_entities = []
    
    def teardown_method(self):
        """Cleanup after each test"""
        for entity_type, entity_uid in self.created_entities:
            try:
                if entity_type == "project":
                    self.client.delete(f"/api/v1/projects/{entity_uid}")
                elif entity_type == "event":
                    # Use repository to delete real GraphEvent
                    self.event_repo.delete_event(entity_uid)
            except Exception:
                pass
        self.created_entities = []
    
    def test_relationship_id_uniqueness(self):
        """Test that relationship IDs are unique"""
        # Create test entities
        project_data = {
            "title": "Test Project Unique",
            "description": "Test project for unique relationship ID",
            "status": "active",
            "priority": 3
        }
        response = self.client.post("/api/v1/projects/", json=project_data)
        assert response.status_code == 201
        project = response.json()
        self.created_entities.append(("project", project["uid"]))
        
        # Create event using GraphEvent directly
        from trm_api.graph_models.event import Event as GraphEvent
        graph_event = GraphEvent(
            name="TEST_UNIQUE_REL",
            description="Test event for unique relationship ID",
            payload={"test": True, "actor_uid": project["uid"]}
        ).save()
        event = {"uid": graph_event.uid}
        self.created_entities.append(("event", event["uid"]))
        
        # Create first relationship
        result1 = self.event_repo.connect_project_to_event(
            project_uid=project["uid"],
            event_uid=event["uid"],
            generation_type="Direct"
        )
        assert result1 is not None
        
        project_node, event_node = result1
        rel1 = project_node.generates_events.relationship(event_node)
        
        # Verify relationship ID exists and is a valid UUID
        assert rel1.relationshipId is not None
        import uuid
        try:
            uuid.UUID(rel1.relationshipId)
        except ValueError:
            pytest.fail("Relationship ID is not a valid UUID")
    
    def test_timestamp_properties(self):
        """Test that timestamps are properly set"""
        project_data = {
            "title": "Test Project Timestamps",
            "description": "Test project for timestamp validation",
            "status": "active",
            "priority": 3
        }
        response = self.client.post("/api/v1/projects/", json=project_data)
        assert response.status_code == 201
        project = response.json()
        self.created_entities.append(("project", project["uid"]))
        
        # Create event using GraphEvent directly
        from trm_api.graph_models.event import Event as GraphEvent
        graph_event = GraphEvent(
            name="TEST_TIMESTAMPS",
            description="Test event for timestamp validation",
            payload={"test": True, "actor_uid": project["uid"]}
        ).save()
        event = {"uid": graph_event.uid}
        self.created_entities.append(("event", event["uid"]))
        
        # Record time before creating relationship (with timezone)
        from datetime import timezone
        before_creation = datetime.now(timezone.utc)
        
        result = self.event_repo.connect_project_to_event(
            project_uid=project["uid"],
            event_uid=event["uid"],
            generation_type="Direct"
        )
        
        # Record time after creating relationship
        after_creation = datetime.now(timezone.utc)
        
        assert result is not None
        project_node, event_node = result
        rel = project_node.generates_events.relationship(event_node)
        
        # Verify timestamps are within expected range
        assert rel.creationDate is not None
        assert rel.lastModifiedDate is not None
        
        # Convert to UTC if needed for comparison
        creation_date = rel.creationDate
        if hasattr(creation_date, 'replace') and creation_date.tzinfo is None:
            creation_date = creation_date.replace(tzinfo=timezone.utc)
        
        modified_date = rel.lastModifiedDate    
        if hasattr(modified_date, 'replace') and modified_date.tzinfo is None:
            modified_date = modified_date.replace(tzinfo=timezone.utc)
            
        assert before_creation <= creation_date <= after_creation
        assert before_creation <= modified_date <= after_creation


class TestGeneratesEventRelationshipPerformance:
    """Performance test class for GeneratesEventRel operations"""
    
    def setup_method(self):
        """Setup for each test"""
        self.client = TestClient(app)
        self.event_repo = EventRepository()
        self.created_entities = []
    
    def teardown_method(self):
        """Cleanup after each test"""
        for entity_type, entity_uid in self.created_entities:
            try:
                if entity_type == "project":
                    self.client.delete(f"/api/v1/projects/{entity_uid}")
                elif entity_type == "event":
                    # Use repository to delete real GraphEvent
                    self.event_repo.delete_event(entity_uid)
            except Exception:
                pass
        self.created_entities = []
    
    def test_large_scale_event_generation(self):
        """Test performance with large number of event generations"""
        # Create one project
        project_data = {
            "title": "Performance Test Project",
            "description": "Project for large scale event generation testing",
            "status": "active",
            "priority": 3
        }
        response = self.client.post("/api/v1/projects/", json=project_data)
        assert response.status_code == 201
        project = response.json()
        self.created_entities.append(("project", project["uid"]))
        
        # Create 50 events and relationships
        import time
        start_time = time.time()
        
        for i in range(50):
            # Create event using GraphEvent directly
            from trm_api.graph_models.event import Event as GraphEvent
            graph_event = GraphEvent(
                name=f"PERFORMANCE_EVENT_{i}",
                description=f"Performance test event {i}",
                payload={"test": True, "actor_uid": project["uid"], "index": i}
            ).save()
            event = {"uid": graph_event.uid}
            self.created_entities.append(("event", event["uid"]))
            
            # Create relationship
            result = self.event_repo.connect_project_to_event(
                project_uid=project["uid"],
                event_uid=event["uid"],
                generation_type="Automated",
                impact=2
            )
            assert result is not None
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Verify all relationships created successfully
        from trm_api.graph_models.project import Project as GraphProject
        project_node = GraphProject.nodes.get(uid=project["uid"])
        events = project_node.generates_events.all()
        assert len(events) == 50
        
        # Performance should complete within reasonable time (adjust as needed)
        assert execution_time < 30.0  # 30 seconds max for 50 relationships
        print(f"Created 50 GeneratesEvent relationships in {execution_time:.2f} seconds") 