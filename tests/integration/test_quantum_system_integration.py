"""
Integration Tests for Quantum System Components
Test toàn bộ quantum system integration với TRM-OS
"""

import pytest
import asyncio
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, patch
import numpy as np

from trm_api.learning.adaptive_learning_system import AdaptiveLearningSystem
from trm_api.quantum.quantum_system_manager import QuantumSystemManager, OrganizationalSignals
from trm_api.quantum.state_transition_engine import StateTransitionEngine, TransitionCondition, TransitionTriggerType
from trm_api.quantum.win_probability_calculator import WINProbabilityCalculator, WINFactor, WINFactorType
from trm_api.quantum.quantum_coherence_monitor import QuantumCoherenceMonitor, CoherenceAlertLevel
from trm_api.quantum.optimization_engine import QuantumOptimizationEngine, OptimizationObjective
from trm_api.quantum.quantum_types import QuantumState, QuantumSystem, WINCategory, QuantumStateType


class TestQuantumSystemIntegration:
    """Test quantum system integration"""
    
    @pytest.fixture
    async def learning_system(self):
        """Create learning system fixture"""
        system = AdaptiveLearningSystem("test_quantum_agent")
        await system.initialize()
        yield system
        await system.cleanup()
    
    @pytest.fixture
    async def quantum_manager(self, learning_system):
        """Create quantum system manager fixture"""
        manager = QuantumSystemManager(learning_system)
        await manager.initialize()
        yield manager
        await manager.cleanup()
    
    @pytest.fixture
    async def transition_engine(self, learning_system):
        """Create state transition engine fixture"""
        engine = StateTransitionEngine(learning_system)
        await engine.initialize()
        return engine
    
    @pytest.fixture
    async def win_calculator(self, learning_system):
        """Create WIN probability calculator fixture"""
        calculator = WINProbabilityCalculator(learning_system)
        await calculator.initialize()
        return calculator
    
    @pytest.fixture
    async def coherence_monitor(self, learning_system):
        """Create coherence monitor fixture"""
        monitor = QuantumCoherenceMonitor(learning_system)
        await monitor.initialize()
        yield monitor
        await monitor.stop_monitoring()
    
    @pytest.fixture
    async def sample_quantum_system(self, quantum_manager):
        """Create sample quantum system"""
        return await quantum_manager.create_quantum_system(
            name="Test Quantum System",
            description="Test system for integration testing"
        )
    
    async def test_quantum_system_creation_and_management(self, quantum_manager):
        """Test quantum system creation và basic management"""
        
        # Create quantum system
        quantum_system = await quantum_manager.create_quantum_system(
            name="Integration Test System",
            description="System for integration testing"
        )
        
        assert quantum_system is not None
        assert quantum_system.system_id is not None
        assert len(quantum_system.quantum_states) > 0
        assert len(quantum_system.state_transitions) > 0
        
        # Check system is tracked
        assert quantum_system.system_id in quantum_manager.quantum_systems
        
        # Get system metrics
        metrics = await quantum_manager.get_system_metrics(quantum_system.system_id)
        assert metrics is not None
        assert metrics.system_coherence >= 0.0
        assert metrics.win_probability >= 0.0
    
    async def test_state_detection_and_transition(self, quantum_manager, transition_engine, sample_quantum_system):
        """Test quantum state detection và transition"""
        
        system_id = sample_quantum_system.system_id
        
        # Create organizational signals
        signals = OrganizationalSignals(
            tension_resolution_rate=0.8,
            project_success_rate=0.75,
            learning_progress=0.7,
            system_coherence=0.65
        )
        
        # Detect current state
        current_state = await quantum_manager.detect_current_quantum_state(system_id, signals)
        assert current_state is not None
        
        # Evaluate transition conditions
        current_metrics = {
            "system_coherence": 0.8,
            "performance_improvement": 0.15,
            "learning_progress": 0.6
        }
        
        possible_transitions = await transition_engine.evaluate_transition_conditions(
            sample_quantum_system, current_metrics
        )
        
        assert isinstance(possible_transitions, list)
        
        # Execute transition if possible
        if possible_transitions:
            from_state, to_state, confidence = possible_transitions[0]
            
            result = await transition_engine.execute_transition(
                sample_quantum_system, from_state, to_state
            )
            
            assert result.success is not None
            assert result.transition_time > 0
            assert result.confidence > 0
    
    async def test_win_probability_calculation_integration(self, quantum_manager, win_calculator, sample_quantum_system):
        """Test WIN probability calculation integration"""
        
        system_id = sample_quantum_system.system_id
        
        # Calculate WIN probability
        win_probability = await win_calculator.calculate_win_probability(
            sample_quantum_system,
            win_category=WINCategory.COMPOSITE,
            context={"high_priority_project": True, "optimal_team_composition": True}
        )
        
        assert win_probability is not None
        assert 0.0 <= win_probability.base_probability <= 1.0
        assert 0.0 <= win_probability.confidence_level <= 1.0
        assert len(win_probability.contributing_factors) > 0
        
        # Analyze WIN factors
        factors = await win_calculator.analyze_win_factors(sample_quantum_system)
        assert len(factors) > 0
        
        for factor in factors:
            assert isinstance(factor, WINFactor)
            assert 0.0 <= factor.current_value <= 1.0
            assert factor.weight > 0.0
    
    async def test_optimization_integration(self, quantum_manager, sample_quantum_system):
        """Test quantum system optimization integration"""
        
        system_id = sample_quantum_system.system_id
        
        # Create optimization objectives
        objectives = [
            OptimizationObjective(
                objective_id="coherence_obj",
                name="Maximize Coherence",
                description="Maximize system coherence",
                weight=0.6
            ),
            OptimizationObjective(
                objective_id="win_obj", 
                name="Maximize WIN Probability",
                description="Maximize WIN state probability",
                weight=0.4
            )
        ]
        
        # Perform optimization
        optimization_result = await quantum_manager.optimize_quantum_system(
            system_id, objectives, method="hybrid_ml_optimization"
        )
        
        assert "optimization_id" in optimization_result
        assert "result" in optimization_result
        assert "system_coherence" in optimization_result
        
        # Check optimization improved system
        new_coherence = optimization_result["system_coherence"]
        assert new_coherence >= 0.0
    
    async def test_coherence_monitoring_integration(self, coherence_monitor, sample_quantum_system):
        """Test coherence monitoring integration"""
        
        # Add system to monitoring
        await coherence_monitor.add_system_to_monitor(sample_quantum_system)
        
        # Get real-time metrics
        metrics = await coherence_monitor.get_real_time_metrics(sample_quantum_system.system_id)
        
        assert "system_id" in metrics
        assert "overall_coherence" in metrics
        assert "metrics" in metrics
        assert "system_status" in metrics
        
        # Generate coherence report
        report = await coherence_monitor.get_coherence_report(sample_quantum_system.system_id)
        
        assert report is not None
        assert report.system_id == sample_quantum_system.system_id
        assert report.overall_coherence >= 0.0
        assert report.coherence_grade in ["A", "B", "C", "D", "F"]
        assert len(report.metrics) > 0
        assert isinstance(report.recommendations, list)
    
    async def test_end_to_end_quantum_workflow(self, quantum_manager, transition_engine, win_calculator, coherence_monitor):
        """Test complete end-to-end quantum workflow"""
        
        # 1. Create quantum system
        quantum_system = await quantum_manager.create_quantum_system(
            name="E2E Test System",
            description="End-to-end test system"
        )
        system_id = quantum_system.system_id
        
        # 2. Add to coherence monitoring
        await coherence_monitor.add_system_to_monitor(quantum_system)
        
        # 3. Detect current state
        signals = OrganizationalSignals(
            tension_resolution_rate=0.7,
            project_success_rate=0.8,
            learning_progress=0.75,
            system_coherence=0.6
        )
        
        current_state = await quantum_manager.detect_current_quantum_state(system_id, signals)
        assert current_state is not None
        
        # 4. Calculate WIN probability
        win_probability = await win_calculator.calculate_win_probability(
            quantum_system, WINCategory.COMPOSITE
        )
        assert win_probability is not None
        initial_win_prob = win_probability.base_probability
        
        # 5. Optimize system
        optimization_result = await quantum_manager.optimize_quantum_system(system_id)
        assert "optimization_id" in optimization_result
        
        # 6. Verify improvement
        new_win_probability = await win_calculator.calculate_win_probability(
            quantum_system, WINCategory.COMPOSITE
        )
        
        # WIN probability should be maintained or improved
        assert new_win_probability.base_probability >= initial_win_prob * 0.9
        
        # 7. Check coherence monitoring
        coherence_report = await coherence_monitor.get_coherence_report(system_id)
        assert coherence_report is not None
        assert coherence_report.overall_coherence > 0.0
        
        # 8. Test state transition
        metrics = {
            "system_coherence": coherence_report.overall_coherence,
            "performance_improvement": 0.1,
            "learning_progress": 0.7
        }
        
        transitions = await transition_engine.evaluate_transition_conditions(quantum_system, metrics)
        assert isinstance(transitions, list)
        
        # 9. Get final system metrics
        final_metrics = await quantum_manager.get_system_metrics(system_id)
        assert final_metrics is not None
        assert final_metrics.system_coherence > 0.0
        assert final_metrics.win_probability > 0.0
    
    async def test_learning_integration_across_components(self, quantum_manager, transition_engine, win_calculator, learning_system):
        """Test learning integration across all quantum components"""
        
        # Create system
        quantum_system = await quantum_manager.create_quantum_system(
            name="Learning Integration Test",
            description="Test learning across components"
        )
        system_id = quantum_system.system_id
        
        # Perform multiple operations to generate learning data
        for i in range(5):
            # State detection
            signals = OrganizationalSignals(
                learning_progress=0.6 + i * 0.05,
                system_coherence=0.5 + i * 0.1
            )
            await quantum_manager.detect_current_quantum_state(system_id, signals)
            
            # WIN probability calculation
            await win_calculator.calculate_win_probability(quantum_system)
            
            # System optimization
            await quantum_manager.optimize_quantum_system(system_id)
        
        # Check learning system has collected experiences
        learning_stats = learning_system.get_statistics()
        
        assert learning_stats["total_experiences"] > 0
        assert learning_stats["patterns_discovered"] >= 0
        assert learning_stats["adaptations_applied"] >= 0
        
        # Verify learning effectiveness
        assert learning_stats.get("learning_effectiveness", 0.0) >= 0.0
    
    async def test_concurrent_quantum_operations(self, quantum_manager, win_calculator):
        """Test concurrent quantum operations"""
        
        # Create multiple systems
        systems = []
        for i in range(3):
            system = await quantum_manager.create_quantum_system(
                name=f"Concurrent Test System {i}",
                description=f"System {i} for concurrent testing"
            )
            systems.append(system)
        
        # Perform concurrent operations
        tasks = []
        
        for system in systems:
            # Concurrent WIN probability calculations
            task = win_calculator.calculate_win_probability(system)
            tasks.append(task)
            
            # Concurrent optimizations
            task = quantum_manager.optimize_quantum_system(system.system_id)
            tasks.append(task)
        
        # Wait for all operations to complete
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Check all operations completed successfully
        for result in results:
            assert not isinstance(result, Exception)
    
    async def test_error_handling_and_recovery(self, quantum_manager, win_calculator):
        """Test error handling và recovery mechanisms"""
        
        # Test with invalid system ID
        invalid_metrics = await quantum_manager.get_system_metrics("invalid_system_id")
        assert invalid_metrics is None
        
        # Test WIN calculation with invalid system
        invalid_system = QuantumSystem(
            system_id="invalid",
            quantum_states={},
            state_transitions={},
            entanglement_network={}
        )
        
        try:
            win_prob = await win_calculator.calculate_win_probability(invalid_system)
            # Should handle gracefully
            assert win_prob is not None
        except Exception as e:
            # Should not raise unhandled exceptions
            pytest.fail(f"Unexpected exception: {e}")
    
    async def test_performance_under_load(self, quantum_manager, win_calculator):
        """Test performance under load"""
        
        # Create system
        quantum_system = await quantum_manager.create_quantum_system(
            name="Load Test System",
            description="System for load testing"
        )
        
        # Measure performance
        start_time = datetime.now()
        
        # Perform many operations
        tasks = []
        for i in range(10):
            task = win_calculator.calculate_win_probability(quantum_system)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        
        end_time = datetime.now()
        total_time = (end_time - start_time).total_seconds()
        
        # Check performance
        assert total_time < 10.0  # Should complete within 10 seconds
        assert len(results) == 10
        assert all(result is not None for result in results)
    
    async def test_quantum_system_statistics_and_monitoring(self, quantum_manager, coherence_monitor, win_calculator):
        """Test statistics và monitoring capabilities"""
        
        # Create system
        quantum_system = await quantum_manager.create_quantum_system(
            name="Statistics Test System",
            description="System for statistics testing"
        )
        
        # Add to monitoring
        await coherence_monitor.add_system_to_monitor(quantum_system)
        
        # Perform operations
        await win_calculator.calculate_win_probability(quantum_system)
        await quantum_manager.optimize_quantum_system(quantum_system.system_id)
        
        # Get statistics
        manager_stats = quantum_manager.get_statistics() if hasattr(quantum_manager, 'get_statistics') else {}
        monitor_stats = coherence_monitor.get_monitoring_statistics()
        calculator_stats = win_calculator.get_calculation_statistics()
        
        # Verify statistics
        assert isinstance(monitor_stats, dict)
        assert isinstance(calculator_stats, dict)
        assert monitor_stats["monitored_systems"] >= 1
        assert calculator_stats["total_calculations"] >= 1


class TestQuantumSystemFailureScenarios:
    """Test failure scenarios và edge cases"""
    
    @pytest.fixture
    async def learning_system(self):
        """Create learning system fixture"""
        system = AdaptiveLearningSystem("test_failure_agent")
        await system.initialize()
        yield system
        await system.cleanup()
    
    async def test_system_coherence_degradation(self, learning_system):
        """Test system behavior when coherence degrades"""
        
        quantum_manager = QuantumSystemManager(learning_system)
        await quantum_manager.initialize()
        
        try:
            # Create system với low coherence
            quantum_system = await quantum_manager.create_quantum_system(
                name="Low Coherence System",
                description="System with degraded coherence"
            )
            
            # Manually degrade coherence
            for state in quantum_system.quantum_states.values():
                state.probability *= 0.3  # Reduce probabilities
                state.amplitude = complex(np.sqrt(state.probability), 0.0)
            
            # System should detect degradation
            metrics = await quantum_manager.get_system_metrics(quantum_system.system_id)
            assert metrics is not None
            assert metrics.system_coherence < 0.5
            
        finally:
            await quantum_manager.cleanup()
    
    async def test_optimization_failure_recovery(self, learning_system):
        """Test recovery from optimization failures"""
        
        quantum_manager = QuantumSystemManager(learning_system)
        await quantum_manager.initialize()
        
        try:
            quantum_system = await quantum_manager.create_quantum_system(
                name="Optimization Failure Test",
                description="Test optimization failure recovery"
            )
            
            # Test với invalid objectives
            invalid_objectives = [
                OptimizationObjective(
                    objective_id="invalid",
                    name="Invalid Objective",
                    description="This should fail",
                    weight=-1.0  # Invalid weight
                )
            ]
            
            # Should handle gracefully
            result = await quantum_manager.optimize_quantum_system(
                quantum_system.system_id, invalid_objectives
            )
            
            # Should return error or handle gracefully
            assert "error" in result or "optimization_id" in result
            
        finally:
            await quantum_manager.cleanup()
    
    async def test_memory_management_under_stress(self, learning_system):
        """Test memory management under stress"""
        
        quantum_manager = QuantumSystemManager(learning_system)
        await quantum_manager.initialize()
        
        try:
            # Create many systems
            systems = []
            for i in range(5):  # Reduced number for testing
                system = await quantum_manager.create_quantum_system(
                    name=f"Stress Test System {i}",
                    description=f"System {i} for stress testing"
                )
                systems.append(system)
            
            # Perform many operations
            for system in systems:
                await quantum_manager.optimize_quantum_system(system.system_id)
            
            # Check system is still responsive
            final_system = await quantum_manager.create_quantum_system(
                name="Final Test System",
                description="Final system to test responsiveness"
            )
            
            assert final_system is not None
            
        finally:
            await quantum_manager.cleanup()


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 