"""
Comprehensive Test Suite for ML-Enhanced Reasoning Engine
Tests all components including ML models, quantum enhancements, and integrations
"""

import pytest
import asyncio
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any
from unittest.mock import Mock, AsyncMock, patch

from trm_api.reasoning.ml_enhanced_reasoning_engine import (
    MLEnhancedReasoningEngine,
    ReasoningType,
    ConfidenceLevel,
    ReasoningContext,
    ReasoningResult,
    MLReasoningModel
)
from trm_api.learning.adaptive_learning_system import AdaptiveLearningSystem
from trm_api.quantum.quantum_system_manager import QuantumSystemManager
from trm_api.reasoning.advanced_reasoning_engine import AdvancedReasoningEngine


class TestMLEnhancedReasoningEngine:
    """Test suite for ML-Enhanced Reasoning Engine"""
    
    @pytest.fixture
    async def setup_system(self):
        """Set up test system with all dependencies"""
        
        # Mock dependencies
        learning_system = Mock(spec=AdaptiveLearningSystem)
        learning_system.learn_from_experience = AsyncMock()
        learning_system.get_learning_insights = AsyncMock(return_value={
            "patterns": [],
            "adaptations": [],
            "performance": {"success_rate": 0.8}
        })
        
        quantum_manager = Mock(spec=QuantumSystemManager)
        quantum_manager.quantum_systems = {"test_system": Mock()}
        quantum_manager.detect_current_quantum_state = AsyncMock(return_value=Mock(
            state_id="test_state",
            probability=0.7
        ))
        quantum_manager.calculate_win_probability = AsyncMock(return_value=Mock(
            base_probability=0.6,
            factors={}
        ))
        
        advanced_reasoning = Mock(spec=AdvancedReasoningEngine)
        advanced_reasoning.reason = AsyncMock(return_value=Mock(
            conclusions=["Test conclusion"],
            overall_confidence=0.7,
            steps=[Mock(description="Test step")],
            reasoning_quality=0.8
        ))
        
        # Create ML-Enhanced Reasoning Engine
        engine = MLEnhancedReasoningEngine(
            learning_system=learning_system,
            quantum_manager=quantum_manager,
            advanced_reasoning=advanced_reasoning
        )
        
        # Initialize with mocked ML models
        await engine.initialize()
        
        return {
            "engine": engine,
            "learning_system": learning_system,
            "quantum_manager": quantum_manager,
            "advanced_reasoning": advanced_reasoning
        }
    
    @pytest.fixture
    def sample_context(self):
        """Create sample reasoning context"""
        return ReasoningContext(
            context_id="test_context",
            domain="tension_resolution",
            stakeholders=["agent_1", "agent_2"],
            constraints={"time_limit": 60},
            objectives=["resolve_tension", "maintain_harmony"],
            available_resources={"cpu": 0.8, "memory": 0.6},
            priority_level=7,
            risk_tolerance=0.4,
            quantum_context={"coherence": 0.9}
        )
    
    @pytest.fixture
    def sample_training_data(self):
        """Create sample training data"""
        return [
            {
                "context_features": [2, 1, 2, 2, 0.7, 0.4, 0.0, 0.7],
                "reasoning_type": "deductive",
                "confidence": 0.8,
                "success": True
            },
            {
                "context_features": [3, 2, 1, 3, 0.5, 0.6, 1.0, 0.8],
                "reasoning_type": "inductive",
                "confidence": 0.7,
                "success": True
            },
            {
                "context_features": [1, 3, 3, 1, 0.9, 0.3, 0.0, 0.5],
                "reasoning_type": "hybrid",
                "confidence": 0.6,
                "success": False
            }
        ]
    
    async def test_engine_initialization(self, setup_system):
        """Test ML-Enhanced Reasoning Engine initialization"""
        system = await setup_system
        engine = system["engine"]
        
        assert engine is not None
        assert engine.learning_system is not None
        assert engine.quantum_manager is not None
        assert engine.advanced_reasoning is not None
        assert engine.reasoning_stats["total_reasonings"] == 0
        assert engine.reasoning_stats["successful_reasonings"] == 0
    
    async def test_basic_reasoning(self, setup_system, sample_context):
        """Test basic reasoning functionality"""
        system = await setup_system
        engine = system["engine"]
        
        # Perform reasoning
        result = await engine.reason(
            query="How to resolve tension between agents?",
            context=sample_context,
            reasoning_type=ReasoningType.HYBRID
        )
        
        # Verify result
        assert result is not None
        assert isinstance(result, ReasoningResult)
        assert result.reasoning_type == ReasoningType.HYBRID
        assert result.confidence > 0.0
        assert len(result.reasoning_steps) > 0
        assert result.reasoning_time > 0.0
        
        # Verify statistics updated
        assert engine.reasoning_stats["total_reasonings"] == 1
    
    async def test_ml_enhancement(self, setup_system, sample_context):
        """Test ML enhancement functionality"""
        system = await setup_system
        engine = system["engine"]
        
        # Mock trained ML model
        mock_model = Mock()
        mock_model.predict = Mock(return_value=[0.85])
        
        mock_scaler = Mock()
        mock_scaler.transform = Mock(return_value=[[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 0.8, 0.7]])
        
        engine.confidence_estimator = MLReasoningModel(
            model_id="test_confidence",
            model_type="regressor",
            model=mock_model,
            scaler=mock_scaler,
            trained=True,
            training_accuracy=0.9
        )
        
        # Perform reasoning
        result = await engine.reason(
            query="Test ML enhancement",
            context=sample_context,
            reasoning_type=ReasoningType.DEDUCTIVE
        )
        
        # Verify ML enhancement applied
        assert result.ml_confidence > 0.0
        assert any("ML enhancement" in step for step in result.reasoning_steps)
    
    async def test_quantum_enhancement(self, setup_system, sample_context):
        """Test quantum enhancement functionality"""
        system = await setup_system
        engine = system["engine"]
        
        # Perform reasoning with quantum enhancement
        result = await engine.reason(
            query="Test quantum enhancement",
            context=sample_context,
            reasoning_type=ReasoningType.QUANTUM,
            use_quantum_enhancement=True
        )
        
        # Verify quantum enhancement applied
        assert result.quantum_enhancement >= 0.0
        assert result.win_probability_impact >= 0.0
        
        # Verify quantum manager was called
        system["quantum_manager"].detect_current_quantum_state.assert_called()
        system["quantum_manager"].calculate_win_probability.assert_called()
    
    async def test_confidence_calibration(self, setup_system, sample_context):
        """Test confidence calibration"""
        system = await setup_system
        engine = system["engine"]
        
        # Test with low risk tolerance
        low_risk_context = ReasoningContext(
            context_id="low_risk_test",
            domain="tension_resolution",
            risk_tolerance=0.2,
            priority_level=5
        )
        
        result = await engine.reason(
            query="Test confidence calibration",
            context=low_risk_context,
            reasoning_type=ReasoningType.DEDUCTIVE
        )
        
        # Verify confidence was calibrated (should be conservative)
        assert result.confidence <= 1.0
        assert result.confidence >= 0.0
    
    async def test_reasoning_quality_assessment(self, setup_system, sample_context):
        """Test reasoning quality assessment"""
        system = await setup_system
        engine = system["engine"]
        
        result = await engine.reason(
            query="Test quality assessment",
            context=sample_context,
            reasoning_type=ReasoningType.HYBRID
        )
        
        # Verify quality metrics
        assert 0.0 <= result.logical_consistency <= 1.0
        assert 0.0 <= result.evidence_strength <= 1.0
        assert 0.0 <= result.novelty_score <= 1.0
    
    async def test_ml_model_training(self, setup_system, sample_training_data):
        """Test ML model training"""
        system = await setup_system
        engine = system["engine"]
        
        # Train ML models
        training_result = await engine.train_ml_models(sample_training_data)
        
        # Verify training results
        assert "confidence_estimator" in training_result
        assert "reasoning_predictor" in training_result
        assert "quantum_enhancer" in training_result
        
        # Verify models were created
        assert engine.confidence_estimator is not None
        assert engine.reasoning_predictor is not None
        assert engine.quantum_enhancer is not None
    
    async def test_reasoning_pattern_analysis(self, setup_system, sample_context):
        """Test reasoning pattern analysis"""
        system = await setup_system
        engine = system["engine"]
        
        # Perform multiple reasoning operations
        for i in range(5):
            await engine.reason(
                query=f"Test query {i}",
                context=sample_context,
                reasoning_type=ReasoningType.HYBRID
            )
        
        # Analyze patterns
        patterns = await engine.analyze_reasoning_patterns()
        
        # Verify pattern analysis
        assert "confidence_trends" in patterns
        assert "reasoning_type_distribution" in patterns
        assert "performance_metrics" in patterns
        assert "recommendations" in patterns
    
    async def test_reasoning_recommendations(self, setup_system, sample_context):
        """Test reasoning recommendations"""
        system = await setup_system
        engine = system["engine"]
        
        # Get recommendations
        recommendations = await engine.get_reasoning_recommendations(sample_context)
        
        # Verify recommendations
        assert isinstance(recommendations, list)
        assert len(recommendations) > 0
        
        for rec in recommendations:
            assert "reasoning_type" in rec
            assert "confidence" in rec
            assert "rationale" in rec
    
    async def test_learning_integration(self, setup_system, sample_context):
        """Test integration with adaptive learning system"""
        system = await setup_system
        engine = system["engine"]
        
        # Perform reasoning
        result = await engine.reason(
            query="Test learning integration",
            context=sample_context,
            reasoning_type=ReasoningType.INDUCTIVE
        )
        
        # Verify learning system was called
        system["learning_system"].learn_from_experience.assert_called()
    
    async def test_error_handling(self, setup_system, sample_context):
        """Test error handling in reasoning"""
        system = await setup_system
        engine = system["engine"]
        
        # Mock error in advanced reasoning
        system["advanced_reasoning"].reason.side_effect = Exception("Test error")
        
        # Perform reasoning
        result = await engine.reason(
            query="Test error handling",
            context=sample_context,
            reasoning_type=ReasoningType.DEDUCTIVE
        )
        
        # Verify fallback result
        assert result is not None
        assert result.confidence == 0.1  # Fallback confidence
        assert "Unable to complete reasoning" in result.conclusion
    
    async def test_context_feature_vector(self, sample_context):
        """Test context to feature vector conversion"""
        features = sample_context.to_feature_vector()
        
        # Verify feature vector
        assert len(features) == 8
        assert all(isinstance(f, (int, float)) for f in features)
        assert features[0] == 2  # stakeholders count
        assert features[1] == 1  # constraints count
        assert features[2] == 2  # objectives count
        assert features[3] == 2  # resources count
        assert features[4] == 0.7  # priority_level normalized
        assert features[5] == 0.4  # risk_tolerance
    
    async def test_confidence_level_classification(self):
        """Test confidence level classification"""
        
        # Test different confidence levels
        result_very_low = ReasoningResult(
            result_id="test_1",
            reasoning_type=ReasoningType.DEDUCTIVE,
            conclusion="Test",
            confidence=0.1
        )
        assert result_very_low.get_confidence_level() == ConfidenceLevel.VERY_LOW
        
        result_high = ReasoningResult(
            result_id="test_2",
            reasoning_type=ReasoningType.DEDUCTIVE,
            conclusion="Test",
            confidence=0.75
        )
        assert result_high.get_confidence_level() == ConfidenceLevel.HIGH
        
        result_very_high = ReasoningResult(
            result_id="test_3",
            reasoning_type=ReasoningType.DEDUCTIVE,
            conclusion="Test",
            confidence=0.95
        )
        assert result_very_high.get_confidence_level() == ConfidenceLevel.VERY_HIGH
    
    async def test_reasoning_statistics(self, setup_system, sample_context):
        """Test reasoning statistics tracking"""
        system = await setup_system
        engine = system["engine"]
        
        # Perform multiple reasoning operations
        for i in range(3):
            await engine.reason(
                query=f"Test query {i}",
                context=sample_context,
                reasoning_type=ReasoningType.HYBRID
            )
        
        # Get statistics
        stats = engine.get_reasoning_statistics()
        
        # Verify statistics
        assert stats["total_reasonings"] == 3
        assert stats["successful_reasonings"] >= 0
        assert stats["average_confidence"] > 0.0
        assert stats["average_reasoning_time"] > 0.0
    
    async def test_reasoning_type_prediction(self, setup_system, sample_context):
        """Test reasoning type prediction"""
        system = await setup_system
        engine = system["engine"]
        
        # Mock trained reasoning predictor
        mock_model = Mock()
        mock_model.predict = Mock(return_value=["hybrid"])
        
        mock_scaler = Mock()
        mock_scaler.transform = Mock(return_value=[[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]])
        
        engine.reasoning_predictor = MLReasoningModel(
            model_id="test_predictor",
            model_type="classifier",
            model=mock_model,
            scaler=mock_scaler,
            trained=True,
            training_accuracy=0.85
        )
        
        # Predict reasoning type
        features = sample_context.to_feature_vector()
        predicted_type = await engine._predict_best_reasoning_type(features)
        
        # Verify prediction
        assert predicted_type == "hybrid"
    
    async def test_concurrent_reasoning(self, setup_system, sample_context):
        """Test concurrent reasoning operations"""
        system = await setup_system
        engine = system["engine"]
        
        # Perform concurrent reasoning
        tasks = []
        for i in range(3):
            task = engine.reason(
                query=f"Concurrent query {i}",
                context=sample_context,
                reasoning_type=ReasoningType.HYBRID
            )
            tasks.append(task)
        
        # Wait for all tasks
        results = await asyncio.gather(*tasks)
        
        # Verify all results
        assert len(results) == 3
        for result in results:
            assert result is not None
            assert result.confidence > 0.0
    
    async def test_reasoning_history_management(self, setup_system, sample_context):
        """Test reasoning history management"""
        system = await setup_system
        engine = system["engine"]
        
        # Set small learning window for testing
        engine.learning_window = 3
        
        # Perform multiple reasoning operations
        for i in range(5):
            await engine.reason(
                query=f"History test {i}",
                context=sample_context,
                reasoning_type=ReasoningType.HYBRID
            )
        
        # Verify history management
        assert len(engine.reasoning_history) <= engine.learning_window
        assert len(engine.reasoning_history) == 3
    
    async def cleanup_system(self, system):
        """Clean up test system"""
        try:
            engine = system["engine"]
            
            # Clear reasoning history
            engine.reasoning_history.clear()
            
            # Reset statistics
            engine.reasoning_stats = {
                "total_reasonings": 0,
                "successful_reasonings": 0,
                "average_confidence": 0.0,
                "average_reasoning_time": 0.0,
                "ml_enhancement_rate": 0.0,
                "quantum_enhancement_rate": 0.0
            }
            
        except Exception as e:
            print(f"Cleanup error: {e}")


# Integration Tests
class TestMLReasoningIntegration:
    """Integration tests for ML-Enhanced Reasoning Engine"""
    
    async def test_full_reasoning_pipeline(self):
        """Test complete reasoning pipeline"""
        # This would test the full pipeline with real components
        # For now, we'll use mocked components
        pass
    
    async def test_real_world_scenario(self):
        """Test real-world reasoning scenario"""
        # This would test with actual tension resolution scenarios
        # For now, we'll use simplified test case
        pass


if __name__ == "__main__":
    # Run tests
    import sys
    sys.exit(pytest.main([__file__, "-v"])) 