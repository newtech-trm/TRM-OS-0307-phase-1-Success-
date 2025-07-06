"""
Test suite for Advanced Reasoning Engine

Comprehensive tests covering all reasoning capabilities following TRM-OS philosophy.
"""

import pytest
import asyncio
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

from trm_api.reasoning.advanced_reasoning_engine import AdvancedReasoningEngine
from trm_api.reasoning.reasoning_types import (
    ReasoningContext, ReasoningGoal, ReasoningConstraint, ReasoningType,
    UncertaintyLevel, ReasoningResult, CausalChain
)


class TestAdvancedReasoningEngine:
    """Test suite for Advanced Reasoning Engine core functionality"""
    
    @pytest.fixture
    def engine(self):
        """Create reasoning engine instance for testing"""
        return AdvancedReasoningEngine(agent_id="test_agent_123")
    
    @pytest.fixture
    def sample_context(self):
        """Create sample reasoning context"""
        return ReasoningContext(
            tension_id="tension_123",
            task_ids=["task_456", "task_789"],
            agent_id="agent_123",
            project_id="project_456",
            current_state={
                "tension_status": "open",
                "task_task_456_status": "in_progress",
                "task_task_789_status": "todo"
            },
            historical_events=[
                {
                    "event_id": "event_001",
                    "event_type": "TENSION_CREATED",
                    "timestamp": datetime.now() - timedelta(days=2),
                    "entity_id": "tension_123",
                    "data": {"priority": 8}
                },
                {
                    "event_id": "event_002", 
                    "event_type": "TASK_CREATED",
                    "timestamp": datetime.now() - timedelta(days=1),
                    "entity_id": "task_456",
                    "data": {"assigned_to": "agent_123"}
                },
                {
                    "event_id": "event_003",
                    "event_type": "TASK_UPDATED",
                    "timestamp": datetime.now() - timedelta(hours=6),
                    "entity_id": "task_456", 
                    "data": {"status": "in_progress"}
                }
            ],
            related_entities={
                "tension": ["tension_123"],
                "task": ["task_456", "task_789"],
                "agent": ["agent_123"]
            },
            priority_level=8
        )
    
    @pytest.fixture
    def explanation_goal(self):
        """Create explanation reasoning goal"""
        return ReasoningGoal(
            goal_type="explanation",
            description="Explain why tension_123 was created and current resolution status",
            success_criteria=[
                "Identify root causes of tension",
                "Explain current resolution progress", 
                "Provide clear causal relationships"
            ]
        )
    
    @pytest.fixture
    def recommendation_goal(self):
        """Create recommendation reasoning goal"""
        return ReasoningGoal(
            goal_type="recommendation",
            description="Recommend actions to resolve tension_123 efficiently",
            success_criteria=[
                "Provide actionable recommendations",
                "Prioritize by impact and feasibility",
                "Consider resource constraints"
            ]
        )
    
    @pytest.mark.asyncio
    async def test_basic_reasoning_flow(self, engine, sample_context, explanation_goal):
        """Test basic reasoning flow for explanation goal"""
        
        # Mock repository dependencies
        with patch.object(engine.context_manager, 'enrich_context', new_callable=AsyncMock) as mock_enrich:
            mock_enrich.return_value = sample_context
            
            # Execute reasoning
            result = await engine.reason(explanation_goal, sample_context)
            
            # Verify basic result structure
            assert isinstance(result, ReasoningResult)
            assert result.reasoning_type == ReasoningType.CAUSAL.value
            assert result.success is True
            assert len(result.steps) > 0
            assert result.overall_confidence > 0
            
            # Verify reasoning steps were executed
            step_types = [step.step_type for step in result.steps]
            assert ReasoningType.CONTEXTUAL.value in step_types  # Context preparation
            assert ReasoningType.DEDUCTIVE.value in step_types   # Explanation synthesis
            
            # Verify events were created
            assert len(result.generated_events) > 0
            assert any(event["event_type"] == "REASONING_COMPLETED" for event in result.generated_events)
    
    @pytest.mark.asyncio
    async def test_explanation_reasoning_chain(self, engine, sample_context, explanation_goal):
        """Test explanation-specific reasoning chain"""
        
        with patch.object(engine.context_manager, 'enrich_context', new_callable=AsyncMock) as mock_enrich:
            mock_enrich.return_value = sample_context
            
            with patch.object(engine.causal_analyzer, 'analyze_relationships', new_callable=AsyncMock) as mock_causal:
                # Mock causal analysis results
                mock_causal_chain = CausalChain(
                    root_cause="tension_123",
                    final_effect="task_456",
                    confidence=0.8,
                    strength=0.75,
                    evidence=[{"type": "ontology_pattern", "relationship": "creates"}]
                )
                mock_causal.return_value = [mock_causal_chain]
                
                result = await engine.reason(explanation_goal, sample_context)
                
                # Verify explanation-specific behavior
                assert result.reasoning_type == ReasoningType.CAUSAL.value
                assert len(result.causal_chains) > 0
                assert len(result.conclusions) > 0
                
                # Verify causal analysis was performed
                mock_causal.assert_called_once()
                
                # Check for explanation content
                explanation_steps = [
                    step for step in result.steps 
                    if "explanation" in step.description.lower()
                ]
                assert len(explanation_steps) > 0
    
    @pytest.mark.asyncio
    async def test_recommendation_reasoning_chain(self, engine, sample_context, recommendation_goal):
        """Test recommendation-specific reasoning chain"""
        
        with patch.object(engine.context_manager, 'enrich_context', new_callable=AsyncMock) as mock_enrich:
            # Return actual context instead of mock to avoid AsyncMock issues
            mock_enrich.return_value = sample_context
            
            result = await engine.reason(recommendation_goal, sample_context)
            
            # Verify recommendation-specific behavior
            assert result.reasoning_type == ReasoningType.INDUCTIVE.value
            assert len(result.recommendations) > 0
            assert len(result.steps) >= 3  # Situation analysis, action generation, evaluation
            
            # Verify recommendation quality
            for recommendation in result.recommendations:
                if isinstance(recommendation, dict):
                    assert "action" in recommendation or "description" in recommendation
                    assert recommendation.get("confidence", 0) > 0
            
            # Check for situation analysis step
            situation_steps = [
                step for step in result.steps
                if "situation" in step.description.lower()
            ]
            assert len(situation_steps) > 0
    
    @pytest.mark.asyncio
    async def test_uncertainty_assessment(self, engine, sample_context, explanation_goal):
        """Test uncertainty assessment functionality"""
        
        with patch.object(engine.uncertainty_handler, 'assess_uncertainty', new_callable=AsyncMock) as mock_uncertainty:
            # Mock uncertainty assessment
            mock_uncertainty.return_value = {
                "overall_level": UncertaintyLevel.MODERATE,
                "overall_score": 0.4,
                "confidence_variance": 0.15,
                "sources": [
                    {"source_type": "limited_historical_data", "impact": "medium"}
                ],
                "recommendations": ["Gather more historical data"]
            }
            
            with patch.object(engine.context_manager, 'enrich_context', new_callable=AsyncMock) as mock_enrich:
                mock_enrich.return_value = sample_context
                
                result = await engine.reason(explanation_goal, sample_context)
                
                # Verify uncertainty assessment was performed
                mock_uncertainty.assert_called_once()
                
                # Check uncertainty-related steps
                uncertainty_steps = [
                    step for step in result.steps
                    if step.step_type == ReasoningType.PROBABILISTIC.value
                ]
                assert len(uncertainty_steps) > 0
    
    @pytest.mark.asyncio
    async def test_causal_analysis_integration(self, engine, sample_context, explanation_goal):
        """Test causal analysis integration"""
        
        with patch.object(engine.causal_analyzer, 'analyze_relationships', new_callable=AsyncMock) as mock_causal:
            # Create multiple causal chains
            causal_chains = [
                CausalChain(
                    root_cause="tension_123",
                    final_effect="task_456", 
                    confidence=0.85,
                    strength=0.8
                ),
                CausalChain(
                    root_cause="task_456",
                    final_effect="event_002",
                    confidence=0.9,
                    strength=0.9
                )
            ]
            mock_causal.return_value = causal_chains
            
            with patch.object(engine.context_manager, 'enrich_context', new_callable=AsyncMock) as mock_enrich:
                mock_enrich.return_value = sample_context
                
                result = await engine.reason(explanation_goal, sample_context)
                
                # Verify causal chains were integrated
                assert len(result.causal_chains) >= len(causal_chains)
                
                # Verify causal analysis influenced conclusions
                causal_conclusions = [
                    conclusion for conclusion in result.conclusions
                    if "causal" in conclusion.lower()
                ]
                assert len(causal_conclusions) > 0
    
    @pytest.mark.asyncio
    async def test_constraint_handling(self, engine, sample_context, recommendation_goal):
        """Test reasoning constraint handling"""
        
        # Create time constraint
        time_constraint = ReasoningConstraint(
            constraint_type="time",
            description="Complete reasoning within 30 minutes",
            parameters={"max_duration_minutes": 30},
            strict=True
        )
        
        # Create complexity constraint  
        complexity_constraint = ReasoningConstraint(
            constraint_type="complexity",
            description="Limit complexity to moderate level",
            parameters={"max_complexity": 0.6},
            strict=False
        )
        
        constraints = [time_constraint, complexity_constraint]
        
        with patch.object(engine.context_manager, 'enrich_context', new_callable=AsyncMock) as mock_enrich:
            mock_enrich.return_value = sample_context
            
            result = await engine.reason(recommendation_goal, sample_context, constraints)
            
            # Verify constraints were applied
            assert result.success is True
            
            # Check that time window was set
            if result.context.time_window:
                time_diff = result.context.time_window[1] - result.context.time_window[0]
                assert time_diff.total_seconds() <= 30 * 60  # 30 minutes
            
            # Check complexity limitation
            assert result.context.complexity_score <= 0.6
    
    @pytest.mark.asyncio
    async def test_error_handling(self, engine, sample_context, explanation_goal):
        """Test error handling in reasoning process"""
        
        # Mock context manager to raise exception
        with patch.object(engine.context_manager, 'enrich_context', new_callable=AsyncMock) as mock_enrich:
            mock_enrich.side_effect = Exception("Context enrichment failed")
            
            result = await engine.reason(explanation_goal, sample_context)
            
            # Verify error was handled gracefully
            assert result.success is False
            assert result.error_message == "Context enrichment failed"
            assert len(result.generated_events) > 0  # Error event should be created
    
    def test_reasoning_type_determination(self, engine):
        """Test reasoning type determination based on goal"""
        
        explanation_goal = ReasoningGoal(goal_type="explanation", description="Test")
        assert engine._determine_reasoning_type(explanation_goal) == ReasoningType.CAUSAL.value
        
        prediction_goal = ReasoningGoal(goal_type="prediction", description="Test")
        assert engine._determine_reasoning_type(prediction_goal) == ReasoningType.PROBABILISTIC.value
        
        recommendation_goal = ReasoningGoal(goal_type="recommendation", description="Test")
        assert engine._determine_reasoning_type(recommendation_goal) == ReasoningType.INDUCTIVE.value
        
        analysis_goal = ReasoningGoal(goal_type="analysis", description="Test")
        assert engine._determine_reasoning_type(analysis_goal) == ReasoningType.DEDUCTIVE.value
        
        unknown_goal = ReasoningGoal(goal_type="unknown", description="Test")
        assert engine._determine_reasoning_type(unknown_goal) == ReasoningType.CONTEXTUAL.value
    
    @pytest.mark.asyncio
    async def test_prediction_reasoning_chain(self, engine, sample_context):
        """Test prediction-specific reasoning chain"""
        
        prediction_goal = ReasoningGoal(
            goal_type="prediction",
            description="Predict likely outcomes for tension_123 resolution"
        )
        
        with patch.object(engine.context_manager, 'enrich_context', new_callable=AsyncMock) as mock_enrich:
            mock_enrich.return_value = sample_context
            
            result = await engine.reason(prediction_goal, sample_context)
            
            # Verify prediction-specific behavior
            assert result.reasoning_type == ReasoningType.PROBABILISTIC.value
            assert len(result.predictions) > 0
            
            # Check for temporal analysis
            temporal_steps = [
                step for step in result.steps
                if step.step_type == ReasoningType.TEMPORAL.value
            ]
            assert len(temporal_steps) > 0
            
            # Verify predictions have required fields
            for prediction in result.predictions:
                assert "prediction_type" in prediction
                assert "probability" in prediction or "confidence" in prediction
    
    @pytest.mark.asyncio
    async def test_analysis_reasoning_chain(self, engine, sample_context):
        """Test analysis-specific reasoning chain"""
        
        analysis_goal = ReasoningGoal(
            goal_type="analysis",
            description="Analyze current state and trends for tension_123"
        )
        
        with patch.object(engine.context_manager, 'enrich_context', new_callable=AsyncMock) as mock_enrich:
            mock_enrich.return_value = sample_context
            
            result = await engine.reason(analysis_goal, sample_context)
            
            # Verify analysis-specific behavior
            assert result.reasoning_type == ReasoningType.DEDUCTIVE.value
            assert len(result.steps) >= 2  # Data aggregation + statistical analysis
            
            # Check for data aggregation step
            aggregation_steps = [
                step for step in result.steps
                if "aggregat" in step.description.lower()
            ]
            assert len(aggregation_steps) > 0
            
            # Check for statistical analysis step
            analysis_steps = [
                step for step in result.steps
                if "statistical" in step.description.lower() or "analysis" in step.description.lower()
            ]
            assert len(analysis_steps) > 0
    
    @pytest.mark.asyncio
    async def test_knowledge_integration(self, engine, sample_context, explanation_goal):
        """Test knowledge base integration"""
        
        # Add knowledge to engine
        from trm_api.reasoning.reasoning_types import KnowledgeNode
        
        knowledge = KnowledgeNode(
            node_type="fact",
            content="Tensions of type 'system_issue' typically require 3-5 days to resolve",
            confidence=0.8,
            source="historical_analysis"
        )
        
        await engine.add_knowledge(knowledge)
        
        # Test knowledge querying
        results = await engine.query_knowledge("tension", ["fact"])
        assert len(results) == 1
        assert results[0].content == knowledge.content
        
        # Test reasoning with knowledge
        with patch.object(engine.context_manager, 'enrich_context', new_callable=AsyncMock) as mock_enrich:
            mock_enrich.return_value = sample_context
            
            result = await engine.reason(explanation_goal, sample_context)
            
            # Knowledge should influence reasoning quality
            assert result.success is True
            assert result.overall_confidence > 0
    
    def test_statistics_tracking(self, engine):
        """Test reasoning statistics tracking"""
        
        # Get initial stats
        initial_stats = engine.get_statistics()
        assert initial_stats["total_sessions"] == 0
        assert initial_stats["successful_sessions"] == 0
        
        # Simulate reasoning session
        mock_result = ReasoningResult(
            reasoning_type=ReasoningType.DEDUCTIVE.value,
            context=ReasoningContext(),
            overall_confidence=0.8,
            success=True
        )
        mock_result.start_time = datetime.now() - timedelta(seconds=10)
        mock_result.end_time = datetime.now()
        
        engine._update_reasoning_stats(mock_result)
        
        # Check updated stats
        updated_stats = engine.get_statistics()
        assert updated_stats["total_sessions"] == 1
        assert updated_stats["successful_sessions"] == 1
        assert updated_stats["avg_confidence"] == 0.8
        assert updated_stats["avg_duration"] == 10.0
    
    @pytest.mark.asyncio
    async def test_context_quality_influence(self, engine, sample_context, explanation_goal):
        """Test how context quality influences reasoning"""
        
        # Test with high-quality context
        high_quality_context = sample_context.copy(deep=True)
        high_quality_context.historical_events.extend([
            {
                "event_id": f"event_{i}",
                "event_type": "TASK_UPDATED",
                "timestamp": datetime.now() - timedelta(hours=i),
                "entity_id": "task_456",
                "data": {"progress": i * 10}
            } for i in range(4, 20)  # Add many more events
        ])
        
        with patch.object(engine.context_manager, 'enrich_context', new_callable=AsyncMock) as mock_enrich:
            mock_enrich.return_value = high_quality_context
            
            result_high_quality = await engine.reason(explanation_goal, high_quality_context)
            
            # Test with low-quality context
            low_quality_context = ReasoningContext(
                tension_id="tension_123",
                historical_events=[],  # No historical data
                related_entities={}
            )
            
            mock_enrich.return_value = low_quality_context
            result_low_quality = await engine.reason(explanation_goal, low_quality_context)
            
            # High-quality context should yield better results
            assert result_high_quality.overall_confidence >= result_low_quality.overall_confidence
            assert len(result_high_quality.steps) >= len(result_low_quality.steps)
    
    @pytest.mark.asyncio
    async def test_concurrent_reasoning_sessions(self, engine, sample_context):
        """Test handling of concurrent reasoning sessions"""
        
        goals = [
            ReasoningGoal(goal_type="explanation", description=f"Goal {i}")
            for i in range(3)
        ]
        
        with patch.object(engine.context_manager, 'enrich_context', new_callable=AsyncMock) as mock_enrich:
            mock_enrich.return_value = sample_context
            
            # Run concurrent reasoning sessions
            tasks = [
                engine.reason(goal, sample_context)
                for goal in goals
            ]
            
            results = await asyncio.gather(*tasks)
            
            # Verify all sessions completed successfully
            assert len(results) == 3
            for result in results:
                assert result.success is True
                assert len(result.steps) > 0
            
            # Verify session isolation (different result IDs)
            result_ids = {result.result_id for result in results}
            assert len(result_ids) == 3
    
    @pytest.mark.asyncio
    async def test_reasoning_audit_trail(self, engine, sample_context, explanation_goal):
        """Test comprehensive audit trail creation"""
        
        with patch.object(engine.context_manager, 'enrich_context', new_callable=AsyncMock) as mock_enrich:
            mock_enrich.return_value = sample_context
            
            result = await engine.reason(explanation_goal, sample_context)
            
            # Verify comprehensive audit trail
            assert result.start_time is not None
            assert result.end_time is not None
            assert result.duration_seconds() > 0
            assert result.total_steps == len(result.steps)
            
            # Verify step dependencies and evidence
            for step in result.steps:
                assert step.step_id is not None
                assert step.execution_time is not None
                assert step.confidence >= 0 and step.confidence <= 1
                assert step.uncertainty_level is not None
            
            # Verify event generation for audit
            assert len(result.generated_events) > 0
            reasoning_completed_events = [
                event for event in result.generated_events
                if event["event_type"] == "REASONING_COMPLETED"
            ]
            assert len(reasoning_completed_events) > 0 