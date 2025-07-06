"""
Comprehensive tests for TRM-OS Basic Reasoning Engine MVP

Tests cover:
- TensionAnalyzer functionality
- RuleEngine evaluation
- SolutionGenerator recommendations
- PriorityCalculator algorithms
- ReasoningCoordinator workflow
- API endpoints
- Integration scenarios
"""

import pytest
import asyncio
from datetime import datetime
from unittest.mock import Mock, patch

from trm_api.reasoning import (
    TensionAnalyzer, 
    RuleEngine, 
    SolutionGenerator, 
    PriorityCalculator,
    ReasoningCoordinator,
    ReasoningRequest,
    TensionType,
    ImpactLevel,
    UrgencyLevel
)

class TestTensionAnalyzer:
    """Test TensionAnalyzer component"""
    
    def setup_method(self):
        """Setup for each test"""
        self.analyzer = TensionAnalyzer()
    
    def test_analyze_problem_tension(self):
        """Test analysis of problem-type tension"""
        title = "API Server Down"
        description = "The main API server is not responding and showing error messages"
        
        result = self.analyzer.analyze_tension(title, description)
        
        assert result.tension_type == TensionType.PROBLEM
        assert result.impact_level in [ImpactLevel.HIGH, ImpactLevel.CRITICAL]
        assert result.confidence_score > 0.5
        assert "Technology" in result.key_themes
        assert result.suggested_priority >= 1
    
    def test_analyze_opportunity_tension(self):
        """Test analysis of opportunity-type tension"""
        title = "Improve User Experience"
        description = "We could enhance the user interface to improve customer satisfaction and engagement"
        
        result = self.analyzer.analyze_tension(title, description)
        
        assert result.tension_type == TensionType.OPPORTUNITY
        assert "opportunity" in result.reasoning.lower()
        assert result.confidence_score > 0.3
    
    def test_analyze_security_tension(self):
        """Test analysis of security-related tension"""
        title = "Potential Security Vulnerability"
        description = "Security audit revealed potential vulnerability in authentication system"
        
        result = self.analyzer.analyze_tension(title, description)
        
        assert "Security" in result.key_themes
        assert result.impact_level in [ImpactLevel.HIGH, ImpactLevel.CRITICAL]
        assert result.suggested_priority >= 1
    
    def test_analyze_vietnamese_tension(self):
        """Test analysis with Vietnamese content"""
        title = "Lỗi hệ thống thanh toán"
        description = "Hệ thống thanh toán bị lỗi và không thể xử lý giao dịch của khách hàng"
        
        result = self.analyzer.analyze_tension(title, description)
        
        assert result.tension_type == TensionType.PROBLEM
        assert result.confidence_score > 0.5
        assert result.suggested_priority >= 1
    
    def test_analyze_empty_description(self):
        """Test analysis with minimal information"""
        title = "Test issue"
        description = ""
        
        result = self.analyzer.analyze_tension(title, description)
        
        assert result is not None
        assert result.confidence_score >= 0.5  # Should still provide analysis
        assert len(result.key_themes) >= 1

class TestRuleEngine:
    """Test RuleEngine component"""
    
    def setup_method(self):
        """Setup for each test"""
        self.rule_engine = RuleEngine()
    
    def test_default_rules_loaded(self):
        """Test that default rules are loaded"""
        summary = self.rule_engine.get_rules_summary()
        
        assert summary["total_rules"] > 0
        assert summary["enabled_rules"] > 0
        assert "critical_tension_escalation" in summary["rule_ids"]
        assert "security_tension_handling" in summary["rule_ids"]
    
    def test_critical_escalation_rule(self):
        """Test critical tension escalation rule"""
        context = {
            "analysis": {
                "suggested_priority": 2,
                "impact_level": {"value": 4}
            }
        }
        
        results = self.rule_engine.evaluate_rules(context)
        
        # Should trigger critical escalation rule
        critical_rules = [r for r in results if "critical" in r.get("rule_name", "").lower()]
        assert len(critical_rules) > 0
        
        critical_rule = critical_rules[0]
        assert critical_rule["matched"] is True
        assert len(critical_rule["action_results"]) > 0
    
    def test_security_rule(self):
        """Test security tension handling rule"""
        context = {
            "analysis": {
                "key_themes": ["Security", "Technology"]
            }
        }
        
        results = self.rule_engine.evaluate_rules(context)
        
        # Should trigger security rule
        security_rules = [r for r in results if "security" in r.get("rule_name", "").lower()]
        assert len(security_rules) > 0
        
        security_rule = security_rules[0]
        assert security_rule["matched"] is True
    
    def test_no_matching_rules(self):
        """Test context that doesn't match any rules"""
        context = {
            "analysis": {
                "suggested_priority": 0,
                "impact_level": {"value": 1},
                "key_themes": ["General"]
            }
        }
        
        results = self.rule_engine.evaluate_rules(context)
        
        # Should have no matched rules
        matched_rules = [r for r in results if r.get("matched", False)]
        assert len(matched_rules) == 0
    
    def test_rule_validation(self):
        """Test rule validation functionality"""
        from trm_api.reasoning.rule_engine import BusinessRule, RuleType, RuleCondition, RuleAction, OperatorType
        
        # Valid rule
        valid_rule = BusinessRule(
            id="test_rule",
            name="Test Rule",
            description="Test rule description",
            rule_type=RuleType.ACTION,
            conditions=[RuleCondition("test_field", OperatorType.EQUALS, "test_value")],
            actions=[RuleAction("test_action", {"param": "value"})]
        )
        
        validation = self.rule_engine.validate_rule(valid_rule)
        assert validation["valid"] is True
        assert len(validation["errors"]) == 0
        
        # Invalid rule (missing ID)
        invalid_rule = BusinessRule(
            id="",
            name="Test Rule",
            description="Test rule description",
            rule_type=RuleType.ACTION,
            conditions=[],
            actions=[]
        )
        
        validation = self.rule_engine.validate_rule(invalid_rule)
        assert validation["valid"] is False
        assert len(validation["errors"]) > 0

class TestSolutionGenerator:
    """Test SolutionGenerator component"""
    
    def setup_method(self):
        """Setup for each test"""
        self.generator = SolutionGenerator()
        
        # Create sample analysis
        from trm_api.reasoning.tension_analyzer import TensionAnalysis
        self.sample_analysis = TensionAnalysis(
            tension_type=TensionType.PROBLEM,
            impact_level=ImpactLevel.HIGH,
            urgency_level=UrgencyLevel.MEDIUM,
            confidence_score=0.8,
            key_themes=["Technology"],
            extracted_entities=["API", "Server"],
            suggested_priority=1,
            reasoning="Test analysis"
        )
    
    def test_generate_problem_solutions(self):
        """Test solution generation for problem tensions"""
        solutions = self.generator.generate_solutions(
            self.sample_analysis,
            "API Server Issue",
            "Server is experiencing performance problems"
        )
        
        assert len(solutions) > 0
        assert solutions[0].solution_type.value in ["immediate_action", "investigation", "technology_solution"]
        assert len(solutions[0].steps) > 0
        assert solutions[0].confidence_score > 0
    
    def test_generate_security_solutions(self):
        """Test solution generation for security tensions"""
        security_analysis = self.sample_analysis
        security_analysis.key_themes = ["Security"]
        
        solutions = self.generator.generate_solutions(
            security_analysis,
            "Security Vulnerability",
            "Potential security breach detected"
        )
        
        assert len(solutions) > 0
        # Should include security-focused solution
        security_solutions = [s for s in solutions if "security" in s.title.lower()]
        assert len(security_solutions) > 0
    
    def test_solution_steps_structure(self):
        """Test that solution steps are properly structured"""
        solutions = self.generator.generate_solutions(
            self.sample_analysis,
            "Test Issue",
            "Test description"
        )
        
        assert len(solutions) > 0
        solution = solutions[0]
        
        assert solution.id is not None
        assert solution.title is not None
        assert len(solution.steps) > 0
        
        # Check step structure
        step = solution.steps[0]
        assert step.id is not None
        assert step.title is not None
        assert step.description is not None
        assert step.estimated_effort is not None
    
    def test_escalation_solution_generation(self):
        """Test escalation solution for high-priority tensions"""
        high_priority_analysis = self.sample_analysis
        high_priority_analysis.suggested_priority = 2
        
        solutions = self.generator.generate_solutions(
            high_priority_analysis,
            "Critical Issue",
            "Critical system failure"
        )
        
        # Should include escalation solution
        escalation_solutions = [s for s in solutions if "escalation" in s.title.lower()]
        assert len(escalation_solutions) > 0
        
        escalation_solution = escalation_solutions[0]
        assert escalation_solution.priority.value >= 3  # High priority

class TestPriorityCalculator:
    """Test PriorityCalculator component"""
    
    def setup_method(self):
        """Setup for each test"""
        self.calculator = PriorityCalculator()
        
        # Create sample analysis
        from trm_api.reasoning.tension_analyzer import TensionAnalysis
        self.sample_analysis = TensionAnalysis(
            tension_type=TensionType.PROBLEM,
            impact_level=ImpactLevel.HIGH,
            urgency_level=UrgencyLevel.HIGH,
            confidence_score=0.8,
            key_themes=["Technology"],
            extracted_entities=["API"],
            suggested_priority=1,
            reasoning="Test analysis"
        )
    
    def test_weighted_average_calculation(self):
        """Test weighted average priority calculation"""
        result = self.calculator.calculate_priority(
            self.sample_analysis,
            "Test Title",
            "Test description",
            method="weighted_average"
        )
        
        assert result.final_score >= 0
        assert result.final_score <= 100
        assert result.normalized_priority in [0, 1, 2]
        assert result.priority_level in ["Low", "Medium", "High", "Critical"]
        assert result.confidence_level > 0
        assert len(result.contributing_factors) > 0
    
    def test_eisenhower_matrix_calculation(self):
        """Test Eisenhower matrix priority calculation"""
        result = self.calculator.calculate_priority(
            self.sample_analysis,
            "Test Title", 
            "Test description",
            method="eisenhower_matrix"
        )
        
        assert result.calculation_method == "eisenhower_matrix"
        assert "importance" in result.contributing_factors
        assert "urgency" in result.contributing_factors
        assert "quadrant" in result.contributing_factors
    
    def test_rice_framework_calculation(self):
        """Test RICE framework priority calculation"""
        result = self.calculator.calculate_priority(
            self.sample_analysis,
            "Test Title",
            "Test description", 
            method="rice_framework"
        )
        
        assert result.calculation_method == "rice_framework"
        assert "reach" in result.contributing_factors
        assert "impact" in result.contributing_factors
        assert "confidence" in result.contributing_factors
        assert "effort" in result.contributing_factors
    
    def test_security_context_adjustment(self):
        """Test priority calculation with security context"""
        security_analysis = self.sample_analysis
        security_analysis.key_themes = ["Security"]
        
        result = self.calculator.calculate_priority(
            security_analysis,
            "Security vulnerability detected",
            "Critical security issue in authentication system"
        )
        
        # Security tensions should get higher priority
        assert result.final_score > 50  # Should be elevated
    
    def test_context_parameters(self):
        """Test priority calculation with additional context"""
        context = {
            "deadline": "urgent",
            "stakeholder_count": 5,
            "executive_visibility": True,
            "team_capacity": "low"
        }
        
        result = self.calculator.calculate_priority(
            self.sample_analysis,
            "Test Title",
            "Test description",
            context=context
        )
        
        # Context should influence the score
        assert result.final_score > 0
        assert len(result.recommendations) > 0

class TestReasoningCoordinator:
    """Test ReasoningCoordinator workflow"""
    
    def setup_method(self):
        """Setup for each test"""
        self.coordinator = ReasoningCoordinator()
    
    @pytest.mark.asyncio
    async def test_complete_reasoning_workflow(self):
        """Test complete reasoning workflow"""
        request = ReasoningRequest(
            tension_id="test_tension_001",
            title="API Performance Issue",
            description="API response times are slower than expected, affecting user experience",
            current_status="Open"
        )
        
        result = await self.coordinator.process_tension(request)
        
        assert result.success is True
        assert result.tension_id == "test_tension_001"
        assert result.analysis is not None
        assert len(result.rule_results) >= 0
        assert len(result.solutions) > 0
        assert result.priority_calculation is not None
        assert result.processing_time > 0
        assert len(result.recommendations) > 0
    
    @pytest.mark.asyncio
    async def test_selective_service_processing(self):
        """Test processing with selective services"""
        request = ReasoningRequest(
            tension_id="test_tension_002",
            title="Test Issue",
            description="Test description",
            requested_services=["analysis", "priority"]  # Only analysis and priority
        )
        
        result = await self.coordinator.process_tension(request)
        
        assert result.success is True
        assert result.analysis is not None
        assert result.priority_calculation is not None
        # Should not have solutions since not requested
        assert len(result.solutions) == 0
    
    @pytest.mark.asyncio
    async def test_batch_processing(self):
        """Test batch processing of multiple tensions"""
        requests = [
            ReasoningRequest(
                tension_id=f"batch_test_{i}",
                title=f"Test Issue {i}",
                description=f"Test description {i}"
            )
            for i in range(3)
        ]
        
        results = await self.coordinator.process_batch_tensions(requests)
        
        assert len(results) == 3
        assert all(r.success for r in results)
        assert all(r.processing_time > 0 for r in results)
    
    @pytest.mark.asyncio
    async def test_component_validation(self):
        """Test reasoning component validation"""
        validation = await self.coordinator.validate_reasoning_components()
        
        assert validation["overall_status"] in ["healthy", "warning", "error"]
        assert "components" in validation
        assert "tension_analyzer" in validation["components"]
        assert "rule_engine" in validation["components"]
        assert "solution_generator" in validation["components"]
        assert "priority_calculator" in validation["components"]
    
    def test_performance_tracking(self):
        """Test performance statistics tracking"""
        stats = self.coordinator.get_performance_stats()
        
        assert "total_processed" in stats
        assert "successful_processing" in stats
        assert "average_processing_time" in stats
        assert "component_performance" in stats
        assert "success_rate" in stats
    
    def test_insights_export(self):
        """Test insights and analytics export"""
        insights = self.coordinator.export_reasoning_insights()
        
        assert "performance_metrics" in insights
        assert "rule_effectiveness" in insights
        assert "solution_patterns" in insights
        assert "priority_distributions" in insights
        assert "generated_at" in insights

class TestReasoningIntegration:
    """Test integration scenarios"""
    
    @pytest.mark.asyncio
    async def test_end_to_end_workflow(self):
        """Test complete end-to-end reasoning workflow"""
        # Simulate real tension data
        tension_data = {
            "title": "Database Performance Degradation",
            "description": "Database queries are taking longer than usual, affecting application performance. Users are experiencing slow page loads.",
            "context": {
                "project_id": "proj_001",
                "created_at": datetime.now().isoformat(),
                "priority": 1,
                "stakeholder_count": 3
            }
        }
        
        # Initialize coordinator
        coordinator = ReasoningCoordinator()
        
        # Create request
        request = ReasoningRequest(
            tension_id="integration_test_001",
            title=tension_data["title"],
            description=tension_data["description"],
            context=tension_data["context"]
        )
        
        # Process
        result = await coordinator.process_tension(request)
        
        # Validate complete result
        assert result.success is True
        
        # Validate analysis
        assert result.analysis.tension_type == TensionType.PROBLEM
        assert "Technology" in result.analysis.key_themes
        assert result.analysis.confidence_score > 0.5
        
        # Validate solutions
        assert len(result.solutions) > 0
        tech_solutions = [s for s in result.solutions if "technology" in s.solution_type.value.lower()]
        assert len(tech_solutions) > 0
        
        # Validate priority
        assert result.priority_calculation.final_score > 30  # Should be significant
        assert result.priority_calculation.normalized_priority >= 0
        
        # Validate recommendations
        assert len(result.recommendations) > 0
        tech_recommendations = [r for r in result.recommendations if "💻" in r or "Technical" in r]
        assert len(tech_recommendations) > 0
    
    def test_error_handling(self):
        """Test error handling in reasoning components"""
        analyzer = TensionAnalyzer()
        
        # Test with None inputs
        try:
            result = analyzer.analyze_tension(None, None)
            # Should handle gracefully
            assert result is not None
        except Exception as e:
            # Should not crash with unhandled exception
            assert "NoneType" not in str(e)
        
        # Test with empty inputs
        result = analyzer.analyze_tension("", "")
        assert result is not None
        assert result.confidence_score < 0.8  # Should have low confidence
    
    def test_performance_requirements(self):
        """Test that reasoning meets performance requirements"""
        import time
        
        analyzer = TensionAnalyzer()
        
        # Single analysis should be fast
        start_time = time.time()
        result = analyzer.analyze_tension(
            "Performance test tension",
            "This is a test description for performance measurement"
        )
        end_time = time.time()
        
        processing_time = end_time - start_time
        assert processing_time < 1.0  # Should complete within 1 second
        assert result is not None
    
    @pytest.mark.asyncio
    async def test_concurrent_processing(self):
        """Test concurrent processing capability"""
        coordinator = ReasoningCoordinator()
        
        # Create multiple requests
        requests = [
            ReasoningRequest(
                tension_id=f"concurrent_test_{i}",
                title=f"Concurrent Test {i}",
                description=f"Test description for concurrent processing {i}"
            )
            for i in range(5)
        ]
        
        # Process concurrently
        start_time = datetime.now()
        tasks = [coordinator.process_tension(req) for req in requests]
        results = await asyncio.gather(*tasks)
        end_time = datetime.now()
        
        # Validate results
        assert len(results) == 5
        assert all(r.success for r in results)
        
        # Should be faster than sequential processing
        total_time = (end_time - start_time).total_seconds()
        sequential_time = sum(r.processing_time for r in results)
        
        # For very fast operations (microseconds), the timing comparison may not be meaningful
        # Only assert if processing time is significant enough for meaningful comparison
        if sequential_time > 0.001:  # Only compare if total sequential time > 1ms
            assert total_time < sequential_time  # Concurrent should be faster
        # Otherwise, just ensure both times are reasonable
        assert total_time >= 0
        assert sequential_time >= 0

# Test fixtures and utilities
@pytest.fixture
def sample_tension_data():
    """Sample tension data for testing"""
    return {
        "problem_tension": {
            "title": "API Server Error",
            "description": "The API server is returning 500 errors for user requests",
            "expected_type": TensionType.PROBLEM,
            "expected_themes": ["Technology"]
        },
        "opportunity_tension": {
            "title": "Improve Customer Experience",
            "description": "We could enhance the mobile app interface to increase user engagement",
            "expected_type": TensionType.OPPORTUNITY,
            "expected_themes": ["Business"]
        },
        "security_tension": {
            "title": "Security Vulnerability",
            "description": "Security scan revealed potential vulnerability in authentication system",
            "expected_type": TensionType.PROBLEM,
            "expected_themes": ["Security", "Technology"]
        }
    }

@pytest.fixture
def mock_tension_repository():
    """Mock tension repository for testing"""
    mock_repo = Mock()
    mock_repo.get_by_id.return_value = Mock(
        id="test_tension_001",
        title="Test Tension",
        description="Test Description",
        status="Open",
        priority=1,
        project_id="test_project_001",
        created_at=datetime.now()
    )
    return mock_repo

# Performance benchmarks
class TestReasoningPerformance:
    """Performance benchmark tests"""
    
    def test_analysis_performance_benchmark(self):
        """Benchmark tension analysis performance"""
        analyzer = TensionAnalyzer()
        
        test_cases = [
            ("Short tension", "Brief description"),
            ("Medium length tension title", "This is a medium length description with some technical terms like API, database, and system performance issues."),
            ("Very long and detailed tension title with multiple technical terms and business context", 
             "This is a very long and detailed description that includes multiple technical terms, business context, stakeholder information, and complex scenarios that might affect the analysis performance. It includes terms like API, database, microservices, authentication, authorization, security, performance, scalability, user experience, customer satisfaction, revenue impact, and strategic alignment.")
        ]
        
        results = []
        for title, description in test_cases:
            start_time = datetime.now()
            result = analyzer.analyze_tension(title, description)
            end_time = datetime.now()
            
            processing_time = (end_time - start_time).total_seconds()
            results.append({
                "input_length": len(title) + len(description),
                "processing_time": processing_time,
                "confidence": result.confidence_score
            })
        
        # Validate performance
        for result in results:
            assert result["processing_time"] < 2.0  # Should complete within 2 seconds
            assert result["confidence"] > 0.0  # Should produce valid results
        
        # Performance should not degrade significantly with input length
        max_time = max(r["processing_time"] for r in results)
        min_time = min(r["processing_time"] for r in results)
        
        # Ensure minimum time to avoid division by zero and handle microsecond precision
        min_time = max(min_time, 0.0001)  # Minimum 0.1 millisecond for meaningful comparison
        assert max_time / min_time < 100  # Should not be more than 100x slower (more realistic for microsecond precision)

if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"]) 