#!/usr/bin/env python3
"""
Debug script để test can_handle_tension logic
"""

import asyncio
from unittest.mock import Mock
from datetime import datetime
import logging
import json

from trm_api.agents.templates.data_analyst_template import DataAnalystAgent
from trm_api.models.tension import Tension
from trm_api.models.enums import TensionType, Priority
from trm_api.agents.templates.integration_template import IntegrationAgent

def create_debug_tension():
    """Tạo tension cho debug"""
    tension = Mock(spec=Tension)
    tension.uid = f"debug-tension-{datetime.now().timestamp()}"
    tension.tensionId = tension.uid
    tension.title = "Data Quality Issues"
    tension.description = "Dữ liệu trong hệ thống có nhiều lỗi và thiếu sót, cần phân tích và làm sạch"
    tension.tension_type = "Problem"
    tension.tensionType = TensionType.DATA_ANALYSIS
    tension.priority = Priority.MEDIUM
    tension.status = "Open"
    tension.source = "DebugScript"
    tension.creationDate = datetime.now()
    tension.lastModifiedDate = datetime.now()
    return tension

async def debug_can_handle_tension():
    """Debug can_handle_tension step by step"""
    print("=== Debugging can_handle_tension ===")
    
    # Create agent
    agent = DataAnalystAgent()
    print(f"Agent created: {agent.agent_id}")
    
    # Initialize agent
    print("\n--- Initializing agent ---")
    await agent.initialize()
    print(f"Agent initialized: {agent.agent_id}")
    print(f"Agent metadata: {agent.metadata}")
    print(f"Agent capabilities: {len(agent.capabilities) if hasattr(agent, 'capabilities') else 'None'}")
    
    # Create tension
    tension = create_debug_tension()
    print(f"\nTension created: {tension.tensionId}")
    print(f"Tension type: {tension.tensionType}")
    print(f"Tension priority: {tension.priority}")
    print(f"Tension description: {tension.description}")
    
    # Test step by step
    try:
        print("\n--- Step 1: Initial checks ---")
        print(f"Has tensionType: {hasattr(tension, 'tensionType')}")
        print(f"TensionType value: {tension.tensionType}")
        
        print("\n--- Step 2: Supported types check ---")
        supported_types = [
            TensionType.DATA_ANALYSIS,
            TensionType.RESOURCE_CONSTRAINT,
            TensionType.PROCESS_IMPROVEMENT
        ]
        print(f"Supported types: {supported_types}")
        print(f"Is supported: {tension.tensionType in supported_types}")
        
        print("\n--- Step 3: Call can_handle_tension ---")
        
        # Add debug logging
        logging.basicConfig(level=logging.DEBUG)
        
        # Test with try-catch to see exact error
        try:
            print("Calling can_handle_tension...")
            result = await agent.can_handle_tension(tension)
            print(f"Result received: {result}")
        except Exception as e:
            print(f"Exception in can_handle_tension: {e}")
            import traceback
            traceback.print_exc()
        
        return result
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

async def debug_solutions():
    print("=== Debug Generate Specialized Solutions ===")
    
    # Create DataAnalystAgent
    agent = DataAnalystAgent()
    print(f"Agent created: {agent.template_metadata.template_name}")
    print(f"Agent ID: {agent.agent_id}")
    
    # Create mock tension
    tension = Mock()
    tension.tensionId = "debug-tension-solutions"
    tension.title = "Data Quality Issues"
    tension.description = "Dữ liệu có nhiều lỗi, cần data quality assessment và cleanup"
    tension.tensionType = TensionType.DATA_ANALYSIS
    tension.priority = Priority.MEDIUM
    tension.status = "Open"
    tension.source = "Test"
    tension.creationDate = "2024-01-01"
    tension.lastModifiedDate = "2024-01-01"
    
    print(f"Tension: {tension.title}")
    print(f"Description: {tension.description}")
    
    # Test generate_specialized_solutions
    try:
        requirements = await agent.analyze_tension_requirements(tension)
        print(f"Requirements analysis_type: {requirements.get('analysis_type')}")
        
        solutions = await agent.generate_specialized_solutions(tension, requirements)
        print(f"Generated {len(solutions)} solutions")
        
        for i, solution in enumerate(solutions):
            print(f"\n--- Solution {i+1} ---")
            print(f"Keys: {list(solution.keys())}")
            print(f"ID: {solution.get('id', 'NO_ID')}")
            print(f"Type: {solution.get('type', 'NO_TYPE')}")
            print(f"Title: {solution.get('title', 'NO_TITLE')}")
            print(f"Agent Template: {solution.get('agent_template', 'NO_AGENT_TEMPLATE')}")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

async def debug_integration():
    print("=== Debug IntegrationAgent can_handle_tension ===")
    
    # Create IntegrationAgent
    agent = IntegrationAgent()
    print(f"Agent created: {agent.template_metadata.template_name}")
    print(f"Agent ID: {agent.agent_id}")
    
    # Create mock tension
    tension = Mock()
    tension.uid = "debug-integration-tension"
    tension.tensionId = "debug-integration-tension"
    tension.title = "Third-party Integration"
    tension.description = "Cần integrate với Salesforce API để sync customer data"
    tension.tensionType = TensionType.PROCESS_IMPROVEMENT
    tension.priority = Priority.MEDIUM
    tension.status = "Open"
    tension.source = "Test"
    tension.creationDate = "2024-01-01"
    tension.lastModifiedDate = "2024-01-01"
    
    print(f"Tension: {tension.title}")
    print(f"Description: {tension.description}")
    print(f"TensionType: {tension.tensionType}")
    
    # Test can_handle_tension
    try:
        result = await agent.can_handle_tension(tension)
        print(f"can_handle_tension result: {result}")
        
        # Debug the keywords
        description = tension.description.lower()
        title = tension.title.lower()
        print(f"Title lower: {title}")
        print(f"Description lower: {description}")
        
        integration_keywords = [
            "integration", "integrate", "api", "sync", "synchronize",
            "connect", "connection", "third party", "external", "enterprise",
            "workflow", "automation", "data", "system", "service",
            "webhook", "endpoint", "microservice", "etl", "migration",
            "tích hợp", "đồng bộ", "kết nối", "hệ thống", "dịch vụ"
        ]
        
        matching_keywords = [kw for kw in integration_keywords if kw in description or kw in title]
        print(f"Matching keywords: {matching_keywords}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    result = asyncio.run(debug_can_handle_tension())
    print(f"\nFinal result: {result}")
    asyncio.run(debug_solutions())
    asyncio.run(debug_integration()) 