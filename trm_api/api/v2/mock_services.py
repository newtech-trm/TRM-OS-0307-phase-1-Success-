"""
Mock Services for Conversational Interface
Đảm bảo conversational interface có thể hoạt động độc lập
"""

from typing import Dict, Any, Optional
import asyncio
from datetime import datetime
from uuid import uuid4
from unittest.mock import AsyncMock
import random


class MockAgentService:
    """Mock Agent Service for conversational interface"""
    
    def __init__(self):
        self.agents = {}
    
    async def create_agent(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new agent"""
        agent_id = str(uuid4())
        agent_type = parameters.get("agent_type", "CODE_GENERATOR")
        
        agent = {
            "id": agent_id,
            "type": agent_type,
            "name": f"Agent {agent_type}",
            "status": "active",
            "created_at": datetime.now().isoformat(),
            "capabilities": self._get_agent_capabilities(agent_type)
        }
        
        self.agents[agent_id] = agent
        return agent
    
    async def get_agent(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get agent by ID"""
        return self.agents.get(agent_id)
    
    async def list_agents(self) -> list:
        """List all agents"""
        return list(self.agents.values())
    
    def _get_agent_capabilities(self, agent_type: str) -> list:
        """Get capabilities for agent type"""
        capabilities_map = {
            "CODE_GENERATOR": ["code_generation", "debugging", "testing"],
            "RESEARCH": ["research", "analysis", "documentation"],
            "DATA_ANALYST": ["data_analysis", "visualization", "reporting"],
            "USER_INTERFACE": ["ui_design", "ux_optimization", "prototyping"],
            "INTEGRATION": ["api_integration", "system_connection", "workflow_automation"]
        }
        return capabilities_map.get(agent_type, ["general_assistance"])


class MockProjectService:
    """Mock Project Service for conversational interface"""
    
    def __init__(self):
        self.projects = {}
    
    async def create_project(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new project"""
        project_id = str(uuid4())
        project_name = parameters.get("name", "New Project")
        
        project = {
            "id": project_id,
            "name": project_name,
            "description": f"Project: {project_name}",
            "status": "active",
            "created_at": datetime.now().isoformat(),
            "progress": 0.0,
            "team_size": 0,
            "estimated_duration": "4 weeks"
        }
        
        self.projects[project_id] = project
        return project
    
    async def get_project(self, project_id: str) -> Optional[Dict[str, Any]]:
        """Get project by ID"""
        return self.projects.get(project_id)
    
    async def list_projects(self) -> list:
        """List all projects"""
        return list(self.projects.values())
    
    async def update_project(self, project_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update project"""
        if project_id in self.projects:
            self.projects[project_id].update(updates)
            return self.projects[project_id]
        return None


class MockTensionService:
    """Mock Tension Service for conversational interface"""
    
    def __init__(self):
        self.tensions = {}
        self.resolutions = {}
    
    async def resolve_tension(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Resolve a tension"""
        tension_id = str(uuid4())
        tension_type = parameters.get("tension_type", "TECHNICAL")
        
        # Simulate resolution process
        confidence = random.uniform(0.7, 0.95)
        resolution_time = random.uniform(1.0, 5.0)
        
        resolution = {
            "id": tension_id,
            "type": tension_type,
            "confidence": confidence,
            "resolution_time": resolution_time,
            "status": "resolved",
            "created_at": datetime.now().isoformat(),
            "resolution_strategy": self._get_resolution_strategy(tension_type),
            "impact_assessment": self._get_impact_assessment(confidence)
        }
        
        self.resolutions[tension_id] = resolution
        return resolution
    
    async def get_tension(self, tension_id: str) -> Optional[Dict[str, Any]]:
        """Get tension by ID"""
        return self.tensions.get(tension_id)
    
    async def list_tensions(self) -> list:
        """List all tensions"""
        return list(self.tensions.values())
    
    def _get_resolution_strategy(self, tension_type: str) -> str:
        """Get resolution strategy for tension type"""
        strategies = {
            "TECHNICAL": "automated_analysis_and_fix",
            "BUSINESS": "stakeholder_alignment",
            "RESOURCE": "resource_reallocation",
            "PROCESS": "workflow_optimization"
        }
        return strategies.get(tension_type, "general_problem_solving")
    
    def _get_impact_assessment(self, confidence: float) -> str:
        """Get impact assessment based on confidence"""
        if confidence > 0.9:
            return "high_positive_impact"
        elif confidence > 0.8:
            return "moderate_positive_impact"
        else:
            return "low_positive_impact" 