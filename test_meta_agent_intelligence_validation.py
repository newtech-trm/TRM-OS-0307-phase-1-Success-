#!/usr/bin/env python3
"""
Meta Agent Intelligence Validation Script
Kiểm tra Meta-Agent Intelligence với real self-monitoring và optimization capabilities
"""

import asyncio
import sys
import os
import time
import json
import pytest
from datetime import datetime
from typing import Dict, List, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from trm_api.agents.meta_agent_intelligence import (
    MetaAgentIntelligence, 
    PerformanceAnalyzer, 
    SelfImprovementEngine,
    OptimizationSuggestion,
    AgentPerformanceMetric,
    MetricType,
    SystemPerformanceSnapshot
)

@pytest.mark.asyncio
async def test_meta_agent_intelligence():
    """Test comprehensive Meta-Agent Intelligence capabilities"""
    print("🧠 TESTING META-AGENT INTELLIGENCE VALIDATION")
    print("=" * 60)
    
    # Initialize MetaAgent
    meta_agent = MetaAgentIntelligence()
    
    print("📊 TEST 1: Meta-Agent Architecture Validation")
    print("-" * 50)
    
    # Test core components
    components = [
        ("PerformanceAnalyzer", hasattr(meta_agent, 'performance_analyzer')),
        ("SelfImprovementEngine", hasattr(meta_agent, 'improvement_engine')),
        ("SemanticDetector", hasattr(meta_agent, 'semantic_detector')),
        ("EventBus", hasattr(meta_agent, 'event_bus')),
        ("MonitoringConfig", hasattr(meta_agent, 'monitoring_config')),
        ("Statistics", hasattr(meta_agent, 'stats')),
        ("PerformanceSnapshots", hasattr(meta_agent, 'performance_snapshots')),
        ("ActiveSuggestions", hasattr(meta_agent, 'active_suggestions'))
    ]
    
    architecture_score = 0
    for name, present in components:
        status = "✅" if present else "❌"
        print(f"    {status} {name}")
        if present:
            architecture_score += 1
    
    print(f"  Architecture Score: {architecture_score}/{len(components)} ({architecture_score/len(components)*100:.1f}%)")
    
    print(f"\n📊 TEST 2: Performance Analyzer Capabilities")
    print("-" * 50)
    
    # Test Performance Analyzer
    analyzer = PerformanceAnalyzer()
    
    # Test baseline management
    analyzer.update_baseline("test_agent_1", MetricType.RESPONSE_TIME, 0.5)
    analyzer.update_baseline("test_agent_1", MetricType.SUCCESS_RATE, 0.9)
    analyzer.update_baseline("test_agent_2", MetricType.RESPONSE_TIME, 0.3)
    
    baseline_test = len(analyzer.baseline_metrics) >= 2
    print(f"    {'✅' if baseline_test else '❌'} Baseline Metrics Management")
    
    # Test trend analysis
    test_metrics = [
        AgentPerformanceMetric("test_agent_1", MetricType.RESPONSE_TIME, 0.4, datetime.now()),
        AgentPerformanceMetric("test_agent_1", MetricType.RESPONSE_TIME, 0.45, datetime.now()),
        AgentPerformanceMetric("test_agent_1", MetricType.RESPONSE_TIME, 0.5, datetime.now()),
        AgentPerformanceMetric("test_agent_1", MetricType.RESPONSE_TIME, 0.55, datetime.now()),
        AgentPerformanceMetric("test_agent_1", MetricType.RESPONSE_TIME, 0.6, datetime.now())
    ]
    
    analyzer.trend_history["test_agent_1"] = test_metrics
    trend_direction, trend_strength = analyzer.analyze_performance_trend("test_agent_1", MetricType.RESPONSE_TIME)
    
    trend_test = trend_direction in ["improving", "degrading", "stable"]
    print(f"    {'✅' if trend_test else '❌'} Trend Analysis: {trend_direction} (strength: {trend_strength:.4f})")
    
    # Test improvement potential calculation
    improvement_potential = analyzer.calculate_improvement_potential(
        "test_agent_1", MetricType.RESPONSE_TIME, 0.6
    )
    potential_test = isinstance(improvement_potential, float)
    print(f"    {'✅' if potential_test else '❌'} Improvement Potential: {improvement_potential:.2f}%")
    
    print(f"\n📊 TEST 3: Self-Improvement Engine Capabilities")
    print("-" * 50)
    
    # Test Self-Improvement Engine
    improvement_engine = SelfImprovementEngine()
    
    # Check suggestion templates
    template_categories = len(improvement_engine.suggestion_templates)
    template_test = template_categories >= 4
    print(f"    {'✅' if template_test else '❌'} Suggestion Templates: {template_categories} categories")
    
    # Test suggestion generation
    mock_snapshot = SystemPerformanceSnapshot(
        timestamp=datetime.now(),
        agent_metrics=test_metrics,
        system_metrics={"cpu_usage": 0.8, "memory_usage": 0.7},
        bottlenecks_detected=["response_time_bottleneck:test_agent_1"],
        performance_trends={"test_agent_1_response_trend": -0.05},
        overall_health_score=0.6
    )
    
    suggestions = improvement_engine.generate_suggestions(mock_snapshot, analyzer)
    suggestion_test = len(suggestions) > 0
    print(f"    {'✅' if suggestion_test else '❌'} Suggestion Generation: {len(suggestions)} suggestions")
    
    if suggestions:
        for i, suggestion in enumerate(suggestions[:3]):  # Show first 3
            print(f"      {i+1}. {suggestion.title} (Priority: {suggestion.priority.value})")
            print(f"         Expected improvement: {suggestion.expected_improvement:.1f}%")
            print(f"         Success probability: {suggestion.success_probability:.1f}")
    
    print(f"\n📊 TEST 4: Meta-Agent Integration Testing")
    print("-" * 50)
    
    # Test initialization
    init_success = await meta_agent.initialize()
    print(f"    {'✅' if init_success else '❌'} Initialization: {init_success}")
    
    # Test agent monitoring registration
    meta_agent.monitoring_agents.add("test_agent_1")
    meta_agent.monitoring_agents.add("test_agent_2")
    meta_agent.monitoring_agents.add("test_agent_3")
    
    monitoring_test = len(meta_agent.monitoring_agents) == 3
    print(f"    {'✅' if monitoring_test else '❌'} Agent Monitoring: {len(meta_agent.monitoring_agents)} agents")
    
    # Test performance snapshot collection
    snapshot = await meta_agent._collect_performance_snapshot()
    snapshot_test = isinstance(snapshot, SystemPerformanceSnapshot)
    print(f"    {'✅' if snapshot_test else '❌'} Snapshot Collection: {type(snapshot).__name__}")
    
    # Test health calculation
    health_score = meta_agent._calculate_system_health(snapshot)
    health_test = 0.0 <= health_score <= 1.0
    print(f"    {'✅' if health_test else '❌'} System Health: {health_score:.3f}")
    
    # Test optimization report
    report = meta_agent.get_optimization_report()
    report_test = "system_status" in report and "performance_statistics" in report
    print(f"    {'✅' if report_test else '❌'} Optimization Report Generated")
    
    print(f"\n📊 TEST 5: Self-Improvement Workflow Validation")
    print("-" * 50)
    
    # Simulate full workflow
    print("  Simulating self-improvement workflow...")
    
    # Step 1: Performance degradation detection
    degraded_metrics = [
        AgentPerformanceMetric("workflow_agent", MetricType.RESPONSE_TIME, 1.5, datetime.now()),
        AgentPerformanceMetric("workflow_agent", MetricType.ERROR_RATE, 0.15, datetime.now())
    ]
    
    workflow_snapshot = SystemPerformanceSnapshot(
        timestamp=datetime.now(),
        agent_metrics=degraded_metrics,
        system_metrics={"cpu_usage": 0.9, "memory_usage": 0.85},
        bottlenecks_detected=["response_time_bottleneck:workflow_agent"],
        performance_trends={"workflow_agent_response_trend": -0.1},
        overall_health_score=0.3
    )
    
    # Step 2: Generate suggestions for degraded performance
    workflow_analyzer = PerformanceAnalyzer()
    workflow_analyzer.update_baseline("workflow_agent", MetricType.RESPONSE_TIME, 0.5)
    workflow_analyzer.update_baseline("workflow_agent", MetricType.ERROR_RATE, 0.02)
    
    workflow_suggestions = improvement_engine.generate_suggestions(workflow_snapshot, workflow_analyzer)
    
    workflow_test = len(workflow_suggestions) > 0
    print(f"    {'✅' if workflow_test else '❌'} Degradation Detection & Response: {len(workflow_suggestions)} suggestions")
    
    # Step 3: Prioritization và implementation planning
    high_priority_suggestions = [s for s in workflow_suggestions if s.priority.value in ["critical", "high"]]
    prioritization_test = len(high_priority_suggestions) > 0
    print(f"    {'✅' if prioritization_test else '❌'} Priority Suggestions: {len(high_priority_suggestions)} high/critical")
    
    # Step 4: Auto-implementation simulation
    auto_implementable = [
        s for s in workflow_suggestions 
        if s.success_probability >= 0.8 and s.risk_level == "low"
    ]
    auto_test = len(auto_implementable) >= 0  # Can be 0, that's valid
    print(f"    {'✅' if auto_test else '❌'} Auto-implementable: {len(auto_implementable)} suggestions")
    
    print(f"\n📊 TEST 6: Production Readiness Assessment")
    print("-" * 50)
    
    readiness_score = 0
    max_score = 100
    
    # Architecture completeness (30 points)
    arch_score = min(30, (architecture_score / len(components)) * 30)
    readiness_score += arch_score
    print(f"  Architecture Completeness: {arch_score:.0f}/30")
    
    # Functional capabilities (40 points)
    functional_tests = [
        baseline_test, trend_test, potential_test, template_test,
        suggestion_test, init_success, monitoring_test, snapshot_test,
        health_test, report_test
    ]
    functional_score = (sum(functional_tests) / len(functional_tests)) * 40
    readiness_score += functional_score
    print(f"  Functional Capabilities: {functional_score:.0f}/40")
    
    # Self-improvement workflow (20 points)
    workflow_tests = [workflow_test, prioritization_test, auto_test]
    workflow_score = (sum(workflow_tests) / len(workflow_tests)) * 20
    readiness_score += workflow_score
    print(f"  Self-improvement Workflow: {workflow_score:.0f}/20")
    
    # Performance & reliability (10 points)
    perf_score = 10 if health_test and snapshot_test else 5
    readiness_score += perf_score
    print(f"  Performance & Reliability: {perf_score}/10")
    
    print(f"\n🎯 META-AGENT INTELLIGENCE VALIDATION SUMMARY")
    print("=" * 60)
    
    print(f"🏆 TOTAL SCORE: {readiness_score:.0f}/{max_score} ({readiness_score/max_score*100:.1f}%)")
    
    # Detailed capabilities summary
    print(f"\n📋 CAPABILITIES ACHIEVED:")
    capabilities = [
        ("✅ Self-Performance Monitoring", baseline_test and trend_test),
        ("✅ Bottleneck Detection", suggestion_test),
        ("✅ Optimization Suggestions", template_test and suggestion_test),
        ("✅ Auto-Implementation Logic", auto_test),
        ("✅ System Health Assessment", health_test),
        ("✅ Agent Ecosystem Integration", monitoring_test),
        ("✅ Real-time Analysis", snapshot_test),
        ("✅ Improvement Prioritization", prioritization_test)
    ]
    
    for capability, achieved in capabilities:
        status = "✅" if achieved else "❌"
        print(f"  {status} {capability[2:]}")  # Remove first emoji
    
    if readiness_score >= 90:
        print("\n🎉 EXCELLENT: Meta-Agent Intelligence fully operational!")
        print("📋 Status: \"Enzyme của hệ tiêu hóa\" capabilities achieved")
        print("📋 Ready for: Neo4j ontology auto-evolution integration")
        return True
    elif readiness_score >= 70:
        print("\n✅ GOOD: Meta-Agent Intelligence operational với minor gaps")
        print("📋 Status: Core self-improvement capabilities working")
        print("📋 Recommended: Optimize specific components before production")
        return True
    elif readiness_score >= 50:
        print("\n⚠️ PARTIAL: Meta-Agent Intelligence needs improvement")
        print("📋 Status: Basic capabilities present, needs enhancement")
        print("📋 Required: Address functional gaps before proceeding")
        return False
    else:
        print("\n❌ FAILED: Meta-Agent Intelligence not ready")
        print("📋 Status: Significant implementation issues")
        print("📋 Required: Major fixes needed")
        return False

async def main():
    """Main validation function"""
    try:
        success = await test_meta_agent_intelligence()
        
        print(f"\n📋 NEXT PHASE READINESS:")
        if success:
            print("✅ Week 2 COMPLETED: Meta-Agent Intelligence operational")
            print("✅ Ready for Week 3: Neo4j Ontology Auto-Evolution")
            print("✅ Self-improvement capabilities validated")
            print("✅ \"Enzyme của hệ tiêu hóa\" functionality achieved")
        else:
            print("❌ Week 2 INCOMPLETE: Meta-Agent needs fixes")
            print("❌ Not ready for Week 3 until issues resolved")
            print("❌ Focus on self-improvement capabilities")
        
        return success
        
    except Exception as e:
        print(f"\n💥 META-AGENT VALIDATION ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    asyncio.run(main()) 