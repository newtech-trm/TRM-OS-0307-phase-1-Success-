#!/usr/bin/env python3
"""
Script to create test agents in production database
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from trm_api.repositories.agent_repository import AgentRepository
from trm_api.models.agent import AgentCreate

async def create_test_agents():
    """Create test agents in the database"""
    repo = AgentRepository()
    
    # Test agents data
    test_agents = [
        AgentCreate(
            name="Test AI Agent 1",
            agent_type="AIAgent",
            status="active",
            description="Test AI Agent for system testing",
            capabilities=["data_analysis", "report_generation"]
        ),
        AgentCreate(
            name="Test Internal Agent 1",
            agent_type="InternalAgent",
            status="active",
            description="Test Internal Agent for system testing",
            job_title="Test Manager",
            department="Testing",
            capabilities=["project_management", "team_coordination"]
        ),
        AgentCreate(
            name="Test External Agent 1",
            agent_type="ExternalAgent",
            status="active",
            description="Test External Agent for system testing",
            contact_info={"email": "external@test.com"},
            capabilities=["consulting", "advisory"]
        ),
        AgentCreate(
            name="Test AGE Agent 1",
            agent_type="AGE",
            status="active",
            description="Test AGE Agent for system testing",
            capabilities=["automation", "orchestration", "decision_making"]
        ),
        AgentCreate(
            name="Test Founder Agent",
            agent_type="InternalAgent",
            status="active",
            description="Test Founder Agent with special authorities",
            job_title="Founder",
            department="Executive",
            is_founder=True,
            founder_recognition_authority=True,
            capabilities=["leadership", "strategic_planning", "recognition_authority"]
        )
    ]
    
    created_agents = []
    for agent_data in test_agents:
        try:
            agent = await repo.create_agent(agent_data)
            created_agents.append(agent)
            print(f"✅ Created agent: {agent.name} ({agent.agent_type})")
        except Exception as e:
            print(f"❌ Failed to create agent {agent_data.name}: {e}")
    
    print(f"\n🎉 Successfully created {len(created_agents)} test agents!")
    return created_agents

if __name__ == "__main__":
    asyncio.run(create_test_agents()) 