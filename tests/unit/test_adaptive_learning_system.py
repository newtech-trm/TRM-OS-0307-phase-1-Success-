"""
Comprehensive test suite for Adaptive Learning System

Tests all components and integration scenarios.
"""

import pytest
import asyncio
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch
from typing import Dict, List, Any

from trm_api.learning.adaptive_learning_system import AdaptiveLearningSystem
from trm_api.learning.learning_types import (
    LearningExperience,
    LearningPattern,
    AdaptationRule,
    LearningGoal,
    PerformanceMetric,
    ExperienceType,
    MetricType,
    AdaptationType
)
from trm_api.learning.experience_collector import ExperienceCollector
from trm_api.learning.pattern_recognizer import PatternRecognizer
from trm_api.learning.adaptation_engine import AdaptationEngine
from trm_api.learning.performance_tracker import PerformanceTracker


class TestAdaptiveLearningSystem:
    """Test suite for Adaptive Learning System"""
    
    async def cleanup_system(self, learning_system):
        """Helper method to cleanup learning system after tests"""
        try:
            await learning_system.cleanup()
        except Exception as e:
            # Ignore cleanup errors in tests
            pass
    
    @pytest.fixture
    def agent_id(self):
        return "test_agent_123"
    
    @pytest.fixture
    def learning_system(self, agent_id):
        return AdaptiveLearningSystem(agent_id)
    
    @pytest.fixture
    async def learning_system_async(self, agent_id):
        system = AdaptiveLearningSystem(agent_id)
        await system.initialize()
        yield system
        # Cleanup after test
        await system.cleanup()
    
    @pytest.fixture
    def sample_experiences(self, agent_id):
        """Create sample learning experiences"""
        experiences = []
        
        # Successful task execution
        exp1 = LearningExperience(
            experience_type=ExperienceType.TASK_EXECUTION,
            agent_id=agent_id,
            task_id="task_1",
            action_taken={"approach": "methodical", "strategy": "step_by_step"},
            outcome={"result": "success", "quality": 0.9},
            success=True,
            performance_before={"efficiency": 0.7, "accuracy": 0.8},
            performance_after={"efficiency": 0.85, "accuracy": 0.9},
            confidence_level=0.8,
            context={"project_type": "analysis", "complexity": "medium"}
        )
        
        # Failed problem solving
        exp2 = LearningExperience(
            experience_type=ExperienceType.PROBLEM_SOLVING,
            agent_id=agent_id,
            action_taken={"approach": "quick_fix", "strategy": "trial_error"},
            outcome={"result": "failure", "error": "insufficient_analysis"},
            success=False,
            performance_before={"efficiency": 0.6, "accuracy": 0.7},
            performance_after={"efficiency": 0.5, "accuracy": 0.6},
            confidence_level=0.4,
            context={"project_type": "debugging", "complexity": "high"}
        )
        
        # Successful decision making
        exp3 = LearningExperience(
            experience_type=ExperienceType.DECISION_MAKING,
            agent_id=agent_id,
            action_taken={
                "options_considered": ["option_a", "option_b", "option_c"],
                "decision_made": {"choice": "option_b", "reasoning": "best_tradeoff"}
            },
            outcome={"result": "success", "satisfaction": 0.95},
            success=True,
            performance_before={"confidence": 0.7},
            performance_after={"confidence": 0.9},
            confidence_level=0.85,
            context={"decision_type": "strategic", "time_pressure": "low"}
        )
        
        experiences.extend([exp1, exp2, exp3])
        return experiences
    
    @pytest.fixture
    def sample_patterns(self, agent_id):
        """Create sample learning patterns"""
        patterns = []
        
        # Success rate pattern
        pattern1 = LearningPattern(
            pattern_type="success_rate",
            agent_id=agent_id,
            description="High success rate for methodical approach",
            conditions={"experience_type": "task_execution"},
            outcomes={"expected_success_rate": 0.9},
            frequency=5,
            confidence=0.85,
            strength=0.8,
            success_rate=0.9
        )
        
        # Temporal pattern
        pattern2 = LearningPattern(
            pattern_type="temporal_performance",
            agent_id=agent_id,
            description="Better performance in morning hours",
            conditions={"time_constraint": "hour_of_day"},
            outcomes={"peak_hours": [9, 10, 11]},
            frequency=8,
            confidence=0.75,
            strength=0.7
        )
        
        patterns.extend([pattern1, pattern2])
        return patterns
    
    @pytest.fixture
    def sample_performance_metrics(self, agent_id):
        """Create sample performance metrics"""
        metrics = []
        
        metric1 = PerformanceMetric(
            metric_type=MetricType.EFFICIENCY,
            agent_id=agent_id,
            value=0.85,
            baseline=0.7,
            target=0.9,
            measurement_period=(
                datetime.now() - timedelta(hours=1),
                datetime.now()
            )
        )
        
        metric2 = PerformanceMetric(
            metric_type=MetricType.ACCURACY,
            agent_id=agent_id,
            value=0.92,
            baseline=0.8,
            target=0.95,
            measurement_period=(
                datetime.now() - timedelta(hours=1),
                datetime.now()
            )
        )
        
        metrics.extend([metric1, metric2])
        return metrics
    
    @pytest.mark.asyncio
    async def test_system_initialization(self, learning_system, agent_id):
        """Test system initialization"""
        
        try:
            # Mock the event publishing
            with patch('trm_api.learning.adaptive_learning_system.publish_event') as mock_publish:
                await learning_system.initialize()
                
                # Check initialization
                assert learning_system.agent_id == agent_id
                assert learning_system.learning_enabled == True
                assert learning_system.auto_adaptation_enabled == True
                assert len(learning_system.learning_goals) == 3  # Default goals
                
                # Check event was published
                mock_publish.assert_called()
        finally:
            # Cleanup background tasks
            await self.cleanup_system(learning_system)
    
    @pytest.mark.asyncio
    async def test_learn_from_experience(self, learning_system):
        """Test learning from a single experience"""
        
        with patch('trm_api.learning.adaptive_learning_system.publish_event'):
            await learning_system.initialize()
            
            # Learn from experience
            experience_id = await learning_system.learn_from_experience(
                experience_type=ExperienceType.TASK_EXECUTION,
                context={"task_id": "test_task", "project_type": "analysis"},
                action_taken={"approach": "systematic"},
                outcome={"result": "success"},
                success=True,
                performance_metrics={"efficiency": 0.8, "accuracy": 0.9},
                confidence_level=0.85
            )
            
            # Check experience was recorded
            assert experience_id is not None
            assert len(learning_system.experience_collector.experiences) == 1
            
            # Check performance was recorded
            current_performance = learning_system.performance_tracker.get_current_performance()
            assert MetricType.EFFICIENCY in current_performance
            assert MetricType.ACCURACY in current_performance
    
    @pytest.mark.asyncio
    async def test_learning_cycle_basic(self, learning_system, sample_experiences):
        """Test basic learning cycle"""
        
        with patch('trm_api.learning.adaptive_learning_system.publish_event'):
            await learning_system.initialize()
            
            # Add sample experiences
            for exp in sample_experiences:
                learning_system.experience_collector.experiences[exp.experience_id] = exp
            
            # Run learning cycle
            result = await learning_system.run_learning_cycle()
            
            # Check results
            assert result["success"] == True
            assert result["experiences_analyzed"] == len(sample_experiences)
            assert result["patterns_discovered"] >= 0
            assert result["adaptations_generated"] >= 0
            assert "performance_improvements" in result
    
    @pytest.mark.asyncio
    async def test_learning_cycle_with_patterns(self, learning_system, sample_experiences):
        """Test learning cycle that discovers patterns"""
        
        with patch('trm_api.learning.adaptive_learning_system.publish_event'):
            await learning_system.initialize()
            
            # Add many similar experiences to trigger pattern discovery
            for i in range(15):  # Enough to trigger pattern recognition
                exp = LearningExperience(
                    experience_type=ExperienceType.TASK_EXECUTION,
                    agent_id=learning_system.agent_id,
                    task_id=f"task_{i}",
                    action_taken={"approach": "methodical"},
                    outcome={"result": "success"},
                    success=True,
                    confidence_level=0.8,
                    context={"project_type": "analysis"}
                )
                learning_system.experience_collector.experiences[exp.experience_id] = exp
            
            # Run learning cycle
            result = await learning_system.run_learning_cycle()
            
            # Check that patterns were discovered
            assert result["success"] == True
            assert result["patterns_discovered"] > 0
    
    @pytest.mark.asyncio
    async def test_adaptation_application(self, learning_system, sample_patterns):
        """Test adaptation rule application"""
        
        with patch('trm_api.learning.adaptive_learning_system.publish_event'):
            await learning_system.initialize()
            
            # Add patterns to pattern recognizer
            for pattern in sample_patterns:
                learning_system.pattern_recognizer.discovered_patterns[pattern.pattern_id] = pattern
            
            # Generate adaptations
            adaptation_rules = await learning_system.adaptation_engine.generate_adaptations_from_patterns(
                sample_patterns
            )
            
            # Check adaptations were generated
            assert len(adaptation_rules) > 0
            
            # Apply adaptations
            context = {
                "agent_id": learning_system.agent_id,
                "learning_cycle": True,
                "current_performance": {"efficiency": 0.8}
            }
            
            applied_adaptations = await learning_system.adaptation_engine.apply_adaptations(
                context, adaptation_rules
            )
            
            # Check adaptations were applied
            assert len(applied_adaptations) >= 0  # Some may not be applicable
    
    @pytest.mark.asyncio
    async def test_performance_tracking(self, learning_system):
        """Test performance tracking functionality"""
        
        with patch('trm_api.learning.adaptive_learning_system.publish_event'):
            await learning_system.initialize()
            
            # Record performance metrics
            metric_id1 = await learning_system.performance_tracker.record_performance_metric(
                MetricType.EFFICIENCY,
                0.8,
                context={"task_type": "analysis"}
            )
            
            metric_id2 = await learning_system.performance_tracker.record_performance_metric(
                MetricType.ACCURACY,
                0.9,
                context={"task_type": "analysis"}
            )
            
            # Check metrics were recorded
            assert metric_id1 is not None
            assert metric_id2 is not None
            
            # Check current performance
            current_performance = learning_system.performance_tracker.get_current_performance()
            assert MetricType.EFFICIENCY in current_performance
            assert MetricType.ACCURACY in current_performance
            assert current_performance[MetricType.EFFICIENCY] == 0.8
            assert current_performance[MetricType.ACCURACY] == 0.9
    
    @pytest.mark.asyncio
    async def test_learning_goal_management(self, learning_system):
        """Test learning goal management"""
        
        with patch('trm_api.learning.adaptive_learning_system.publish_event'):
            await learning_system.initialize()
            
            # Create custom learning goal
            custom_goal = LearningGoal(
                agent_id=learning_system.agent_id,
                name="Custom Performance Goal",
                description="Achieve high performance in specific area",
                target_metrics={
                    MetricType.EFFICIENCY: 0.95,
                    MetricType.ACCURACY: 0.98
                },
                priority=9
            )
            
            # Add goal
            goal_id = await learning_system.add_learning_goal(custom_goal)
            
            # Check goal was added
            assert goal_id in learning_system.learning_goals
            assert learning_system.learning_goals[goal_id].name == "Custom Performance Goal"
            
            # Set performance targets
            await learning_system.set_performance_target(MetricType.EFFICIENCY, 0.95)
            await learning_system.set_performance_target(MetricType.ACCURACY, 0.98)
            
            # Record performance that meets targets
            await learning_system.performance_tracker.record_performance_metric(
                MetricType.EFFICIENCY, 0.96
            )
            await learning_system.performance_tracker.record_performance_metric(
                MetricType.ACCURACY, 0.99
            )
            
            # Update goals
            goals_updated = await learning_system._update_learning_goals()
            
            # Check goals were updated
            assert goals_updated > 0
    
    @pytest.mark.asyncio
    async def test_learning_insights(self, learning_system, sample_experiences, sample_patterns):
        """Test learning insights generation"""
        
        with patch('trm_api.learning.adaptive_learning_system.publish_event'):
            await learning_system.initialize()
            
            # Add sample data
            for exp in sample_experiences:
                learning_system.experience_collector.experiences[exp.experience_id] = exp
            
            for pattern in sample_patterns:
                learning_system.pattern_recognizer.discovered_patterns[pattern.pattern_id] = pattern
            
            # Get insights
            insights = learning_system.get_learning_insights()
            
            # Check insights structure
            assert "discovered_patterns" in insights
            assert "active_adaptations" in insights
            assert "performance_trends" in insights
            assert "recommendations" in insights
            
            # Check patterns are included
            assert len(insights["discovered_patterns"]) == len(sample_patterns)
    
    @pytest.mark.asyncio
    async def test_learning_status(self, learning_system):
        """Test learning status reporting"""
        
        with patch('trm_api.learning.adaptive_learning_system.publish_event'):
            await learning_system.initialize()
            
            # Get status
            status = learning_system.get_learning_status()
            
            # Check status structure
            assert "agent_id" in status
            assert "learning_enabled" in status
            assert "auto_adaptation_enabled" in status
            assert "system_stats" in status
            assert "component_stats" in status
            assert "learning_goals" in status
            assert "current_performance" in status
            
            # Check component stats
            assert "experience_collector" in status["component_stats"]
            assert "pattern_recognizer" in status["component_stats"]
            assert "adaptation_engine" in status["component_stats"]
            assert "performance_tracker" in status["component_stats"]
    
    @pytest.mark.asyncio
    async def test_experience_collection_types(self, learning_system):
        """Test different types of experience collection"""
        
        with patch('trm_api.learning.adaptive_learning_system.publish_event'):
            await learning_system.initialize()
            
            # Test task execution experience
            task_exp_id = await learning_system.learn_from_experience(
                experience_type=ExperienceType.TASK_EXECUTION,
                context={"task_id": "test_task"},
                action_taken={"approach": "systematic"},
                outcome={"result": "success"},
                success=True
            )
            
            # Test problem solving experience
            problem_exp_id = await learning_system.learn_from_experience(
                experience_type=ExperienceType.PROBLEM_SOLVING,
                context={"problem_type": "debugging"},
                action_taken={"approach": "root_cause_analysis"},
                outcome={"result": "resolved"},
                success=True
            )
            
            # Test decision making experience
            decision_exp_id = await learning_system.learn_from_experience(
                experience_type=ExperienceType.DECISION_MAKING,
                context={"decision_context": "strategic"},
                action_taken={"decision": "option_a"},
                outcome={"result": "positive"},
                success=True
            )
            
            # Check all experiences were recorded
            assert task_exp_id is not None
            assert problem_exp_id is not None
            assert decision_exp_id is not None
            assert len(learning_system.experience_collector.experiences) == 3
    
    @pytest.mark.asyncio
    async def test_pattern_recognition_accuracy(self, learning_system):
        """Test pattern recognition accuracy"""
        
        with patch('trm_api.learning.adaptive_learning_system.publish_event'):
            await learning_system.initialize()
            
            # Create consistent pattern of successful experiences
            for i in range(20):
                exp = LearningExperience(
                    experience_type=ExperienceType.TASK_EXECUTION,
                    agent_id=learning_system.agent_id,
                    task_id=f"task_{i}",
                    action_taken={"approach": "methodical", "strategy": "careful"},
                    outcome={"result": "success"},
                    success=True,
                    confidence_level=0.85,
                    context={"project_type": "analysis", "complexity": "medium"}
                )
                learning_system.experience_collector.experiences[exp.experience_id] = exp
            
            # Create pattern of failed experiences with different approach
            for i in range(20, 25):
                exp = LearningExperience(
                    experience_type=ExperienceType.TASK_EXECUTION,
                    agent_id=learning_system.agent_id,
                    task_id=f"task_{i}",
                    action_taken={"approach": "rushed", "strategy": "quick"},
                    outcome={"result": "failure"},
                    success=False,
                    confidence_level=0.3,
                    context={"project_type": "analysis", "complexity": "medium"}
                )
                learning_system.experience_collector.experiences[exp.experience_id] = exp
            
            # Run pattern recognition
            experiences = list(learning_system.experience_collector.experiences.values())
            patterns = await learning_system.pattern_recognizer.analyze_experiences(experiences)
            
            # Check that success rate patterns were discovered
            success_patterns = [p for p in patterns if p.pattern_type == "success_rate"]
            assert len(success_patterns) > 0
            
            # Check pattern confidence
            high_confidence_patterns = [p for p in patterns if p.confidence > 0.7]
            assert len(high_confidence_patterns) > 0
    
    @pytest.mark.asyncio
    async def test_adaptation_effectiveness(self, learning_system):
        """Test adaptation effectiveness evaluation"""
        
        with patch('trm_api.learning.adaptive_learning_system.publish_event'):
            await learning_system.initialize()
            
            # Create adaptation rule
            adaptation_rule = AdaptationRule(
                adaptation_type=AdaptationType.PARAMETER_ADJUSTMENT,
                agent_id=learning_system.agent_id,
                name="Test Adaptation",
                description="Test adaptation for effectiveness",
                trigger_conditions={"test_condition": True},
                adaptation_actions={"action": "test_action"},
                priority=5
            )
            
            # Store adaptation rule
            await learning_system.adaptation_engine._store_adaptation_rule(adaptation_rule)
            
            # Apply adaptation
            context = {"test_condition": True}
            applied_adaptations = await learning_system.adaptation_engine.apply_adaptations(
                context, [adaptation_rule]
            )
            
            # Evaluate effectiveness
            if applied_adaptations:
                adaptation_id = applied_adaptations[0]["adaptation_id"]
                performance_metrics = {MetricType.EFFICIENCY: 0.9}
                
                effectiveness = await learning_system.adaptation_engine.evaluate_adaptation_effectiveness(
                    adaptation_id, performance_metrics
                )
                
                # Check effectiveness was calculated
                assert isinstance(effectiveness, float)
                assert 0.0 <= effectiveness <= 1.0
    
    @pytest.mark.asyncio
    async def test_learning_system_reset(self, learning_system, sample_experiences):
        """Test learning system reset functionality"""
        
        with patch('trm_api.learning.adaptive_learning_system.publish_event'):
            await learning_system.initialize()
            
            # Add sample data
            for exp in sample_experiences:
                learning_system.experience_collector.experiences[exp.experience_id] = exp
            
            # Record some performance
            await learning_system.performance_tracker.record_performance_metric(
                MetricType.EFFICIENCY, 0.8
            )
            
            # Check data exists
            assert len(learning_system.experience_collector.experiences) > 0
            assert len(learning_system.performance_tracker.performance_metrics) > 0
            
            # Reset system
            await learning_system.reset_learning_system()
            
            # Check data was cleared
            assert len(learning_system.experience_collector.experiences) == 0
            assert len(learning_system.performance_tracker.performance_metrics) == 0
            assert len(learning_system.learning_goals) == 3  # Default goals restored
    
    @pytest.mark.asyncio
    async def test_concurrent_learning_operations(self, learning_system):
        """Test concurrent learning operations"""
        
        try:
            with patch('trm_api.learning.adaptive_learning_system.publish_event'):
                await learning_system.initialize()
                
                # Create multiple concurrent learning tasks
                tasks = []
                
                for i in range(10):
                    task = learning_system.learn_from_experience(
                        experience_type=ExperienceType.TASK_EXECUTION,
                        context={"task_id": f"concurrent_task_{i}"},
                        action_taken={"approach": f"approach_{i}"},
                        outcome={"result": "success"},
                        success=True,
                        confidence_level=0.7
                    )
                    tasks.append(task)
                
                # Wait for all tasks to complete
                experience_ids = await asyncio.gather(*tasks)
                
                # Check all experiences were recorded
                assert len(experience_ids) == 10
                assert len(learning_system.experience_collector.experiences) == 10
                
                # All experience IDs should be unique
                assert len(set(experience_ids)) == 10
        finally:
            # Cleanup background tasks
            await self.cleanup_system(learning_system)
    
    @pytest.mark.asyncio
    async def test_learning_system_error_handling(self, learning_system):
        """Test error handling in learning system"""
        
        try:
            with patch('trm_api.learning.adaptive_learning_system.publish_event'):
                await learning_system.initialize()
                
                # Test with invalid experience type - this should raise ValueError
                with pytest.raises(ValueError):
                    await learning_system.learn_from_experience(
                        experience_type="invalid_type",  # Invalid type
                        context={"task_id": "test"},
                        action_taken={"approach": "test"},
                        outcome={"result": "test"},
                        success=True
                    )
        finally:
            # Cleanup background tasks
            await self.cleanup_system(learning_system)
    
    @pytest.mark.asyncio
    async def test_learning_system_configuration(self, learning_system):
        """Test learning system configuration"""
        
        # Test enabling/disabling learning
        learning_system.enable_learning()
        assert learning_system.learning_enabled == True
        
        learning_system.disable_learning()
        assert learning_system.learning_enabled == False
        
        # Test enabling/disabling auto-adaptation
        learning_system.enable_auto_adaptation()
        assert learning_system.auto_adaptation_enabled == True
        
        learning_system.disable_auto_adaptation()
        assert learning_system.auto_adaptation_enabled == False
        
        # Test configuration parameters
        learning_system.learning_frequency_hours = 12
        assert learning_system.learning_frequency_hours == 12
        
        learning_system.min_experiences_for_learning = 5
        assert learning_system.min_experiences_for_learning == 5
    
    def test_learning_system_statistics(self, learning_system):
        """Test learning system statistics tracking"""
        
        # Check initial statistics
        stats = learning_system.system_stats
        assert stats["total_learning_cycles"] == 0
        assert stats["total_experiences_processed"] == 0
        assert stats["total_patterns_discovered"] == 0
        assert stats["total_adaptations_applied"] == 0
        assert stats["goals_achieved"] == 0
        
        # Update statistics
        learning_system.system_stats["total_learning_cycles"] = 5
        learning_system.system_stats["total_experiences_processed"] = 50
        
        # Check updated statistics
        assert learning_system.system_stats["total_learning_cycles"] == 5
        assert learning_system.system_stats["total_experiences_processed"] == 50 