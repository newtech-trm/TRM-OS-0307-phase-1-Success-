#!/usr/bin/env python3
"""
Simple test script for ML-Enhanced Reasoning Engine
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from trm_api.reasoning.ml_enhanced_reasoning_engine import (
    MLEnhancedReasoningEngine,
    ReasoningType,
    ReasoningContext
)
from trm_api.learning.adaptive_learning_system import AdaptiveLearningSystem
from trm_api.quantum.quantum_system_manager import QuantumSystemManager
from trm_api.reasoning.advanced_reasoning_engine import AdvancedReasoningEngine


async def test_ml_reasoning_engine():
    """Test ML-Enhanced Reasoning Engine basic functionality"""
    
    print("🚀 Testing ML-Enhanced Reasoning Engine...")
    
    try:
        # Initialize dependencies
        print("📦 Initializing dependencies...")
        learning_system = AdaptiveLearningSystem(agent_id="ml_reasoning_test")
        await learning_system.initialize()
        print("✅ Adaptive Learning System initialized")
        
        quantum_manager = QuantumSystemManager(learning_system=learning_system)
        await quantum_manager.initialize()
        print("✅ Quantum System Manager initialized")
        
        advanced_reasoning = AdvancedReasoningEngine("test_agent")
        print("✅ Advanced Reasoning Engine initialized")
        
        # Create ML-Enhanced Reasoning Engine
        print("🤖 Creating ML-Enhanced Reasoning Engine...")
        ml_engine = MLEnhancedReasoningEngine(
            learning_system=learning_system,
            quantum_manager=quantum_manager,
            advanced_reasoning=advanced_reasoning
        )
        
        await ml_engine.initialize()
        print("✅ ML-Enhanced Reasoning Engine initialized")
        
        # Create test context
        print("📋 Creating test context...")
        context = ReasoningContext(
            context_id="test_context",
            domain="tension_resolution",
            stakeholders=["agent_1", "agent_2"],
            constraints={"time_limit": 60},
            objectives=["resolve_tension", "maintain_harmony"],
            available_resources={"cpu": 0.8, "memory": 0.6},
            priority_level=7,
            risk_tolerance=0.4
        )
        print("✅ Test context created")
        
        # Perform reasoning
        print("🧠 Performing reasoning...")
        result = await ml_engine.reason(
            query="How to resolve tension between two agents with conflicting objectives?",
            context=context,
            reasoning_type=ReasoningType.HYBRID,
            use_quantum_enhancement=True
        )
        
        print("✅ Reasoning completed!")
        
        # Display results
        print("\n📊 REASONING RESULTS:")
        print(f"   Result ID: {result.result_id}")
        print(f"   Reasoning Type: {result.reasoning_type.value}")
        print(f"   Conclusion: {result.conclusion}")
        print(f"   Confidence: {result.confidence:.3f}")
        print(f"   ML Confidence: {result.ml_confidence:.3f}")
        print(f"   Quantum Enhancement: {result.quantum_enhancement:.3f}")
        print(f"   Reasoning Time: {result.reasoning_time:.3f}s")
        print(f"   Logical Consistency: {result.logical_consistency:.3f}")
        print(f"   Evidence Strength: {result.evidence_strength:.3f}")
        print(f"   Novelty Score: {result.novelty_score:.3f}")
        
        print(f"\n📝 REASONING STEPS ({len(result.reasoning_steps)}):")
        for i, step in enumerate(result.reasoning_steps, 1):
            print(f"   {i}. {step}")
        
        # Test statistics
        print("\n📈 ENGINE STATISTICS:")
        stats = ml_engine.get_reasoning_statistics()
        for key, value in stats.items():
            print(f"   {key}: {value}")
        
        # Test pattern analysis
        print("\n🔍 PATTERN ANALYSIS:")
        patterns = await ml_engine.analyze_reasoning_patterns()
        for key, value in patterns.items():
            print(f"   {key}: {value}")
        
        # Test recommendations
        print("\n💡 RECOMMENDATIONS:")
        recommendations = await ml_engine.get_reasoning_recommendations(context)
        for i, rec in enumerate(recommendations, 1):
            print(f"   {i}. {rec}")
        
        print("\n🎉 All tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def test_reasoning_coordinator():
    """Test ReasoningCoordinator with ML-Enhanced Reasoning"""
    
    print("\n🚀 Testing ReasoningCoordinator with ML-Enhanced Reasoning...")
    
    try:
        from trm_api.reasoning.reasoning_coordinator import ReasoningCoordinator, ReasoningRequest
        
        # Create coordinator
        coordinator = ReasoningCoordinator()
        print("✅ ReasoningCoordinator created")
        
        # Create test request
        request = ReasoningRequest(
            tension_id="test_tension_001",
            title="Agent Conflict Resolution",
            description="Two agents have conflicting objectives in a shared workspace. Agent A prioritizes speed while Agent B prioritizes accuracy. This creates tension in collaborative tasks.",
            current_status="Open",
            context={
                "stakeholders": ["agent_a", "agent_b", "project_manager"],
                "constraints": {"deadline": "2024-01-15", "budget": 10000},
                "resources": {"cpu": 0.8, "memory": 0.6, "network": 0.9}
            },
            use_ml_enhancement=True,
            use_quantum_enhancement=True
        )
        print("✅ Test request created")
        
        # Process tension
        print("🧠 Processing tension through complete pipeline...")
        result = await coordinator.process_tension(request)
        
        print("✅ Tension processing completed!")
        
        # Display results
        print("\n📊 REASONING COORDINATOR RESULTS:")
        print(f"   Tension ID: {result.tension_id}")
        print(f"   Success: {result.success}")
        print(f"   Processing Time: {result.processing_time:.3f}s")
        print(f"   Errors: {len(result.errors)}")
        
        if result.analysis:
            print(f"\n📋 TENSION ANALYSIS:")
            print(f"   Type: {result.analysis.tension_type}")
            print(f"   Impact Level: {result.analysis.impact_level}")
            print(f"   Urgency Level: {result.analysis.urgency_level}")
            print(f"   Suggested Priority: {result.analysis.suggested_priority}")
            print(f"   Confidence Score: {result.analysis.confidence_score:.3f}")
        
        if result.ml_reasoning_result:
            print(f"\n🤖 ML REASONING RESULT:")
            ml_result = result.ml_reasoning_result
            print(f"   Conclusion: {ml_result.conclusion}")
            print(f"   Confidence: {ml_result.confidence:.3f}")
            print(f"   ML Enhancement: {ml_result.ml_confidence:.3f}")
            print(f"   Quantum Enhancement: {ml_result.quantum_enhancement:.3f}")
        
        print(f"\n💡 CONSOLIDATED RECOMMENDATIONS ({len(result.recommendations)}):")
        for i, rec in enumerate(result.recommendations, 1):
            print(f"   {i}. {rec}")
        
        # Test performance stats
        print("\n📈 COORDINATOR PERFORMANCE:")
        stats = coordinator.get_performance_stats()
        for key, value in stats.items():
            if isinstance(value, dict):
                print(f"   {key}:")
                for subkey, subvalue in value.items():
                    print(f"     {subkey}: {subvalue}")
            else:
                print(f"   {key}: {value}")
        
        print("\n🎉 ReasoningCoordinator test completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ ReasoningCoordinator test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Main test function"""
    print("=" * 80)
    print("🧪 ML-ENHANCED REASONING ENGINE TEST SUITE")
    print("=" * 80)
    
    # Test 1: ML-Enhanced Reasoning Engine
    success1 = await test_ml_reasoning_engine()
    
    # Test 2: ReasoningCoordinator integration
    success2 = await test_reasoning_coordinator()
    
    print("\n" + "=" * 80)
    print("📊 TEST SUMMARY")
    print("=" * 80)
    print(f"ML-Enhanced Reasoning Engine: {'✅ PASSED' if success1 else '❌ FAILED'}")
    print(f"ReasoningCoordinator Integration: {'✅ PASSED' if success2 else '❌ FAILED'}")
    
    overall_success = success1 and success2
    print(f"\nOverall Result: {'🎉 ALL TESTS PASSED' if overall_success else '❌ SOME TESTS FAILED'}")
    
    return overall_success


if __name__ == "__main__":
    asyncio.run(main()) 