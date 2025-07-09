#!/usr/bin/env python3
"""
Quick test script for Adaptive Learning System
"""

import asyncio
from trm_api.learning.adaptive_learning_system import AdaptiveLearningSystem
from trm_api.learning.learning_types import ExperienceType, MetricType

async def test_adaptive_learning():
    print("🧠 Testing Adaptive Learning System...")
    
    # Create system
    system = AdaptiveLearningSystem('test_agent')
    print("✅ System created")
    
    # Initialize
    await system.initialize()
    print("✅ System initialized")
    
    # Test learning from experience
    experience_id = await system.learn_from_experience(
        experience_type=ExperienceType.AGENT_CREATION,
        context={'task_id': 'test_task', 'project_type': 'analysis'},
        action_taken={'approach': 'systematic'},
        outcome={'result': 'success'},
        success=True,
        performance_metrics={'efficiency': 0.8, 'accuracy': 0.9},
        confidence_level=0.85
    )
    print(f"✅ Experience learned: {experience_id}")
    
    # Test status
    status = system.get_learning_status()
    print("✅ Status retrieved successfully")
    print(f"   - Learning enabled: {status['learning_enabled']}")
    print(f"   - Auto-adaptation enabled: {status['auto_adaptation_enabled']}")
    print(f"   - Learning goals: {len(status['learning_goals'])}")
    
    # Test insights
    insights = system.get_learning_insights()
    print("✅ Insights retrieved successfully")
    print(f"   - Patterns discovered: {len(insights['discovered_patterns'])}")
    print(f"   - Active adaptations: {len(insights['active_adaptations'])}")
    
    print("🎉 All tests passed! Adaptive Learning System is working!")

if __name__ == "__main__":
    asyncio.run(test_adaptive_learning()) 