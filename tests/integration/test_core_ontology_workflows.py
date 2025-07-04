"""
Integration tests for core ontology workflows.
Tests the complete flow: Agent creates Project → Project creates Task → Agent completes Task → System creates WIN.
These tests run against real Neo4j database to verify ontology relationships work correctly.
"""

import pytest
import pytest_asyncio
import uuid
import logging
from datetime import datetime
from httpx import AsyncClient
from fastapi import status

logger = logging.getLogger(__name__)

from trm_api.main import app
from neomodel import db, clear_neo4j_database
from tests.conftest import async_test_client


class TestCoreOntologyWorkflows:
    """Integration tests for core ontology workflows using real Neo4j database."""
    
    @pytest_asyncio.fixture(autouse=True)
    async def setup_test(self, async_test_client):
        """Setup test fixtures and clean database before each test."""
        # Clean database before each test
        try:
            clear_neo4j_database(db)
        except Exception as e:
            logger.warning("Could not clear database: %s", e)
        
        # Generate unique IDs for this test
        self.agent_id = str(uuid.uuid4())
        self.project_id = str(uuid.uuid4())
        self.task_id = str(uuid.uuid4())
        self.win_id = str(uuid.uuid4())
        self.recognition_id = str(uuid.uuid4())
        
        # Use client from fixture
        self.client = async_test_client
        
        # Test data following ontology v3.2
        self.founder_agent_data = {
            "name": "TRM Founder",
            "agentType": "InternalAgent",
            "purpose": "Lead the TRM organization",
            "description": "Founder of TRM with full authority",
            "status": "active",
            "capabilities": ["strategic_planning", "recognition_authority"],
            "jobTitle": "CEO & Founder",
            "department": "Leadership",
            "isFounder": True,
            "founderRecognitionAuthority": True,
            "contactInfo": {"email": "founder@trm.com"},
            "toolIds": []
        }
        
        self.project_data = {
            "title": "ICON Project - Phase 1",
            "description": "First phase of ICON project to establish TRM brand",
            "status": "active",
            "goal": "Build strong brand recognition and establish market presence",
            "scope": "Brand development, website creation, initial marketing campaigns",
            "priority": 2,
            "project_type": "branding",
            "tags": ["branding", "marketing", "phase1"],
            "is_strategic": True
        }
        
        self.task_data = {
            "name": "Design TRM Logo and Brand Identity",
            "description": "Create comprehensive brand identity including logo, color palette, and brand guidelines",
            "status": "ToDo",
            "taskType": "Creative",
            "priority": 1,
            "estimatedHours": 40,
            "tags": ["design", "branding", "logo"]
        }
        
        self.win_data = {
            "name": "Brand Identity Successfully Created",
            "narrative": "Completed comprehensive brand identity that resonates with target audience. The project involved extensive research into our target market, competitor analysis, and multiple design iterations. The final brand identity includes a distinctive logo, cohesive color palette, and typography that reflects TRM's innovative and professional values. This achievement establishes a strong foundation for all future marketing efforts and provides clear brand guidelines for consistent communication.",
            "status": "published",
            "winType": "strategic_achievement",
            "impact_level": 4,
            "tags": ["branding", "milestone", "design"]
        }
        
        self.recognition_data = {
            "name": "Outstanding Brand Design Work",
            "message": "Exceptional creativity and attention to detail in brand identity creation",
            "recognitionType": "Achievement",
            "status": "GRANTED",
            "impactLevel": "High",
            "recognitionReason": "Delivered brand identity that exceeded expectations",
            "given_by_agent_id": None,  # Will be set dynamically
            "received_by_agent_ids": []  # Will be set dynamically
        }

    @pytest.mark.asyncio
    async def test_complete_ontology_workflow(self):
        """
        Test complete ontology workflow:
        1. Create Founder Agent
        2. Agent creates Project
        3. Project creates Task
        4. Agent completes Task
        5. System creates WIN
        6. Agent creates Recognition for WIN
        7. Verify all relationships are correct
        """
        
        # Step 1: Create Founder Agent
        print("\n=== Step 1: Creating Founder Agent ===")
        agent_response = await self.client.post("/api/v1/agents/", json=self.founder_agent_data)
        assert agent_response.status_code == status.HTTP_201_CREATED
        agent_data = agent_response.json()
        self.agent_id = agent_data["agentId"]
        print(f"Created Agent: {agent_data['name']} (ID: {self.agent_id})")
        
        # Step 2: Agent creates Project
        print("\n=== Step 2: Agent creates Project ===")
        project_payload = self.project_data.copy()
        project_payload["ownerAgentId"] = self.agent_id
        
        project_response = await self.client.post("/api/v1/projects/", json=project_payload)
        assert project_response.status_code == status.HTTP_201_CREATED
        project_data = project_response.json()
        self.project_id = project_data["uid"]
        print(f"Created Project: {project_data['title']} (ID: {self.project_id})")
        
        # Step 3: Project creates Task
        print("\n=== Step 3: Project creates Task ===")
        task_payload = self.task_data.copy()
        task_payload["project_id"] = self.project_id
        
        task_response = await self.client.post("/api/v1/tasks/", json=task_payload)
        assert task_response.status_code == status.HTTP_201_CREATED
        task_data = task_response.json()
        self.task_id = task_data["uid"]
        print(f"Created Task: {task_data['name']} (ID: {self.task_id})")
        
        # Step 4: Assign Task to Agent
        print("\n=== Step 4: Assign Task to Agent ===")
        assign_response = await self.client.post(
            f"/api/v1/tasks/{self.task_id}/assign/agent/{self.agent_id}",
            json={
                "assignment_type": "primary",
                "priority_level": "high",
                "estimated_effort": 40,
                "notes": "Founder taking on this critical branding task"
            }
        )
        assert assign_response.status_code == status.HTTP_200_OK
        print("Task assigned to Agent successfully")
        
        # Step 5: Agent completes Task
        print("\n=== Step 5: Agent completes Task ===")
        complete_response = await self.client.post(
            f"/api/v1/tasks/{self.task_id}/complete?assignee_id={self.agent_id}&actual_effort=35"
        )
        assert complete_response.status_code == status.HTTP_200_OK
        print("Task completed successfully")
        
        # Step 6: Create WIN for completed task
        print("\n=== Step 6: Create WIN for completed task ===")
        win_response = await self.client.post("/api/v1/wins/", json=self.win_data)
        assert win_response.status_code == status.HTTP_201_CREATED
        win_data = win_response.json()
        self.win_id = win_data["uid"]
        print(f"Created WIN: {win_data['name']} (ID: {self.win_id})")
        
        # Step 7: Create relationship Project LEADS_TO_WIN
        print("\n=== Step 7: Create Project LEADS_TO_WIN relationship ===")
        leads_to_win_response = await self.client.post(
            f"/api/v1/relationships/leads-to-win?source_id={self.project_id}&win_id={self.win_id}&source_type=Project",
            json={
                "direct_contribution": True,
                "contribution_level": 4,  # SIGNIFICANT
                "impact_ratio": 0.8,
                "notes": "Project directly led to successful brand identity creation"
            }
        )
        assert leads_to_win_response.status_code == status.HTTP_200_OK
        print("Project LEADS_TO_WIN relationship created")
        
        # Step 8: Agent creates Recognition for WIN
        print("\n=== Step 8: Agent creates Recognition for WIN ===")
        recognition_payload = self.recognition_data.copy()
        recognition_payload["given_by_agent_id"] = self.agent_id
        recognition_payload["received_by_agent_ids"] = [self.agent_id]  # Self-recognition for demo
        recognition_response = await self.client.post("/api/v1/recognitions/", json=recognition_payload)
        assert recognition_response.status_code == status.HTTP_201_CREATED
        recognition_data = recognition_response.json()
        self.recognition_id = recognition_data["uid"]
        print(f"Created Recognition: {recognition_data['name']} (ID: {self.recognition_id})")
        
        # Step 9: Create Recognition RECOGNIZES_WIN relationship
        print("\n=== Step 9: Create Recognition RECOGNIZES_WIN relationship ===")
        recognizes_win_response = await self.client.post(
            "/api/v1/relationships/recognizes-win",
            json={
                "recognition_id": self.recognition_id,
                "win_id": self.win_id,
                "recognition_level": "High",
                "public_recognition": True,
                "notes": "Recognizing exceptional brand design achievement"
            }
        )
        assert recognizes_win_response.status_code == status.HTTP_201_CREATED
        print("Recognition RECOGNIZES_WIN relationship created")
        
        # Step 10: Create Recognition GIVEN_BY Agent relationship
        print("\n=== Step 10: Create Recognition GIVEN_BY Agent relationship ===")
        given_by_response = await self.client.post(
            "/api/v1/relationships/given-by",
            json={
                "recognition_id": self.recognition_id,
                "agent_id": self.agent_id,
                "authority_level": "Founder",
                "given_date": datetime.now().isoformat(),
                "notes": "Founder recognizing outstanding work"
            }
        )
        assert given_by_response.status_code == status.HTTP_201_CREATED
        print("Recognition GIVEN_BY Agent relationship created")
        
        # Step 11: Verify all relationships exist
        print("\n=== Step 11: Verify all relationships ===")
        
        # Verify Project leads to WIN
        project_wins_response = await self.client.get(f"/api/v1/relationships/projects/{self.project_id}/leads-to-wins")
        assert project_wins_response.status_code == status.HTTP_200_OK
        project_wins = project_wins_response.json()
        assert len(project_wins) == 1
        assert project_wins[0]["target_id"] == self.win_id
        print("✓ Project LEADS_TO_WIN relationship verified")
        
        # Verify Recognition recognizes WIN
        recognition_wins_response = await self.client.get(f"/api/v1/relationships/recognitions/{self.recognition_id}/recognizes-wins")
        assert recognition_wins_response.status_code == status.HTTP_200_OK
        recognition_wins = recognition_wins_response.json()
        assert len(recognition_wins) == 1
        assert recognition_wins[0]["target_id"] == self.win_id
        print("✓ Recognition RECOGNIZES_WIN relationship verified")
        
        # Verify Recognition given by Agent
        recognition_agents_response = await self.client.get(f"/api/v1/relationships/recognitions/{self.recognition_id}/given-by")
        assert recognition_agents_response.status_code == status.HTTP_200_OK
        recognition_agents = recognition_agents_response.json()
        assert len(recognition_agents) == 1
        assert recognition_agents[0]["source_id"] == self.agent_id
        print("✓ Recognition GIVEN_BY Agent relationship verified")
        
        print("\n🎉 Complete ontology workflow test PASSED!")
        print("Successfully demonstrated Recognition → Event → WIN philosophy in action")

    @pytest.mark.asyncio
    async def test_tension_to_project_workflow(self):
        """
        Test Tension → Project workflow:
        1. Create Agent
        2. Agent detects Tension
        3. Agent creates Project to resolve Tension
        4. Verify RESOLVES_TENSION relationship
        """
        
        # Step 1: Create Agent
        print("\n=== Step 1: Creating Agent ===")
        agent_response = await self.client.post("/api/v1/agents/", json=self.founder_agent_data)
        assert agent_response.status_code == status.HTTP_201_CREATED
        agent_data = agent_response.json()
        self.agent_id = agent_data["agentId"]
        
        # Step 2: Create Tension
        print("\n=== Step 2: Creating Tension ===")
        tension_data = {
            "title": "Lack of Brand Identity",
            "description": "TRM lacks a cohesive brand identity which affects market recognition",
            "tensionType": "Opportunity",
            "status": "Open",
            "priority": "High",
            "impact": "High",
            "urgency": "Medium",
            "tags": ["branding", "marketing", "identity"]
        }
        
        tension_response = await self.client.post("/api/v1/tensions/", json=tension_data)
        assert tension_response.status_code == status.HTTP_200_OK
        tension_data_response = tension_response.json()
        tension_id = tension_data_response["uid"]
        print(f"Created Tension: {tension_data_response['title']} (ID: {tension_id})")
        
        # Step 3: Create Project to resolve Tension
        print("\n=== Step 3: Creating Project to resolve Tension ===")
        project_payload = self.project_data.copy()
        project_payload["ownerAgentId"] = self.agent_id
        
        project_response = await self.client.post("/api/v1/projects/", json=project_payload)
        assert project_response.status_code == status.HTTP_201_CREATED
        project_data = project_response.json()
        self.project_id = project_data["uid"]
        
        # Step 4: Create RESOLVES_TENSION relationship
        print("\n=== Step 4: Creating RESOLVES_TENSION relationship ===")
        resolves_response = await self.client.post(
            f"/api/v1/projects/{self.project_id}/resolves-tension/{tension_id}",
            json={
                "resolution_approach": "comprehensive",
                "expected_impact": "high",
                "notes": "This project will create a complete brand identity to resolve the tension"
            }
        )
        assert resolves_response.status_code == status.HTTP_200_OK
        print("RESOLVES_TENSION relationship created")
        
        # Step 5: Verify relationship
        print("\n=== Step 5: Verify RESOLVES_TENSION relationship ===")
        project_tensions_response = await self.client.get(f"/api/v1/projects/{self.project_id}/tensions")
        assert project_tensions_response.status_code == status.HTTP_200_OK
        project_tensions = project_tensions_response.json()
        assert len(project_tensions) == 1
        assert project_tensions[0]["uid"] == tension_id
        print("✓ RESOLVES_TENSION relationship verified")
        
        print("\n🎯 Tension → Project workflow test PASSED!")

    @pytest.mark.asyncio
    async def test_knowledge_generation_workflow(self):
        """
        Test Knowledge Generation workflow:
        1. Create WIN
        2. WIN generates KnowledgeSnippet
        3. Verify GENERATES_KNOWLEDGE relationship
        """
        
        # Step 1: Create WIN
        print("\n=== Step 1: Creating WIN ===")
        win_response = await self.client.post("/api/v1/wins/", json=self.win_data)
        assert win_response.status_code == status.HTTP_201_CREATED
        win_data = win_response.json()
        self.win_id = win_data["uid"]
        
        # Step 2: Create KnowledgeSnippet
        print("\n=== Step 2: Creating KnowledgeSnippet ===")
        knowledge_data = {
            "content": "Key learning: Brand identity should reflect core values and resonate with target audience. Use consistent color palette and typography across all materials.",
            "snippetType": "Learning",
            "tags": ["branding", "design", "lesson-learned"]
        }
        
        knowledge_response = await self.client.post("/api/v1/knowledge-snippets/", json=knowledge_data)
        assert knowledge_response.status_code == status.HTTP_201_CREATED
        knowledge_data_response = knowledge_response.json()
        knowledge_id = knowledge_data_response["uid"]
        
        # Step 3: Create GENERATES_KNOWLEDGE relationship
        print("\n=== Step 3: Creating GENERATES_KNOWLEDGE relationship ===")
        generates_response = await self.client.post(
            f"/api/v1/relationships/generates-knowledge?win_id={self.win_id}&knowledge_id={knowledge_id}"
        )
        if generates_response.status_code != status.HTTP_201_CREATED:
            print(f"Error response: {generates_response.status_code}")
            print(f"Error body: {generates_response.text}")
        assert generates_response.status_code == status.HTTP_201_CREATED
        print("GENERATES_KNOWLEDGE relationship created")
        
        # Step 4: Verify relationship
        print("\n=== Step 4: Verify GENERATES_KNOWLEDGE relationship ===")
        win_knowledge_response = await self.client.get(f"/api/v1/relationships/wins/{self.win_id}/generates-knowledge")
        assert win_knowledge_response.status_code == status.HTTP_200_OK
        win_knowledge = win_knowledge_response.json()
        assert len(win_knowledge) == 1
        assert win_knowledge[0]["uid"] == knowledge_id
        print("✓ GENERATES_KNOWLEDGE relationship verified")
        
        print("\n📚 Knowledge Generation workflow test PASSED!")

    async def cleanup_test_data(self):
        """Clean up test data after each test."""
        try:
            # Note: In a real scenario, we might want to clean up specific test data
            # For now, we clear the entire database in setup_test
            pass
        except Exception as e:
            logger.warning("Could not clean up test data: %s", e) 