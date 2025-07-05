#!/usr/bin/env python3
"""
Script to seed agents data directly to production database
Run this via Railway CLI or deployment
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Set up environment for production
os.environ.setdefault('NEO4J_URI', 'neo4j+s://databases.neo4j.io')
os.environ.setdefault('NEO4J_USERNAME', 'neo4j')

# Import after setting environment
from trm_api.core.config import settings
from trm_api.db.session import init_db
from neomodel import config as neomodel_config

async def setup_production_db():
    """Setup production database connection"""
    try:
        # Initialize database connection
        init_db()
        print("✅ Connected to production Neo4j database")
        return True
    except Exception as e:
        print(f"❌ Failed to connect to production database: {e}")
        return False

async def seed_agents():
    """Seed agents data to production"""
    if not await setup_production_db():
        return
    
    from trm_api.repositories.agent_repository import AgentRepository
    from trm_api.models.agent import AgentCreate
    
    repo = AgentRepository()
    
    # Production-ready agents data
    production_agents = [
        AgentCreate(
            name="TRM AI Assistant",
            agent_type="AIAgent",
            status="active",
            description="Primary AI assistant for TRM operations",
            capabilities=["natural_language_processing", "task_automation", "data_analysis"]
        ),
        AgentCreate(
            name="TRM AGE System",
            agent_type="AGE",
            status="active",
            description="Artificial Genesis Engine for TRM ecosystem orchestration",
            capabilities=["system_orchestration", "automated_decision_making", "resource_optimization"]
        ),
        AgentCreate(
            name="TRM Project Manager",
            agent_type="InternalAgent",
            status="active",
            description="Internal project management agent",
            job_title="Project Manager",
            department="Operations",
            capabilities=["project_planning", "resource_allocation", "timeline_management"]
        ),
        AgentCreate(
            name="TRM Founder",
            agent_type="InternalAgent",
            status="active",
            description="TRM Founder with full system authority",
            job_title="Founder & CEO",
            department="Executive",
            is_founder=True,
            founder_recognition_authority=True,
            capabilities=["strategic_leadership", "recognition_authority", "system_governance"]
        ),
        AgentCreate(
            name="TRM External Consultant",
            agent_type="ExternalAgent",
            status="active",
            description="External consulting agent for specialized tasks",
            contact_info={"email": "consultant@trm.com", "role": "Strategic Advisor"},
            capabilities=["strategic_consulting", "market_analysis", "business_development"]
        )
    ]
    
    created_agents = []
    for agent_data in production_agents:
        try:
            agent = await repo.create_agent(agent_data)
            created_agents.append(agent)
            print(f"✅ Created agent: {agent.name} ({agent.agent_type})")
        except Exception as e:
            print(f"❌ Failed to create agent {agent_data.name}: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n🎉 Successfully seeded {len(created_agents)} production agents!")
    
    # Test list agents
    try:
        all_agents = await repo.list_agents(skip=0, limit=10)
        print(f"\n📊 Total agents in database: {len(all_agents)}")
        for agent in all_agents:
            print(f"  - {agent.name} ({agent.agent_type})")
    except Exception as e:
        print(f"❌ Failed to list agents: {e}")
    
    return created_agents

if __name__ == "__main__":
    print("🚀 Starting production agent seeding...")
    asyncio.run(seed_agents()) 