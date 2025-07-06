"""
Comprehensive Test Suite for Advanced Genesis Engine

Tests cho tất cả components của Advanced Genesis Engine:
- AdvancedAgentCreator
- TemplateGenerator  
- AgentCapabilityEvolver
- EcosystemOptimizer
"""

import pytest
import asyncio
from datetime import datetime
from typing import List, Dict, Any

from trm_api.agents.genesis.advanced_creator import (
    AdvancedAgentCreator, 
    CompositeAgent, 
    CustomAgent, 
    CustomRequirements
)
from trm_api.agents.genesis.template_generator import (
    TemplateGenerator,
    AgentPattern,
    GeneratedTemplate,
    ValidationResult
)
from trm_api.agents.evolution.capability_evolver import (
    AgentCapabilityEvolver,
    PerformanceGap,
    EvolutionResult
)
from trm_api.agents.ecosystem.optimizer import (
    EcosystemOptimizer,
    AgentEcosystem,
    HealthReport,
    OptimizationPlan,
    Workload,
    BalancingResult
)
from trm_api.agents.templates.template_registry import AgentTemplateRegistry
from trm_api.agents.templates.data_analyst_template import DataAnalystAgent
from trm_api.agents.templates.code_generator_template import CodeGeneratorAgent
from trm_api.models.tension import Tension
from trm_api.models.enums import TensionType, Priority


@pytest.fixture
def template_registry():
    """Create template registry for testing"""
    return AgentTemplateRegistry()


@pytest.fixture
def sample_tensions():
    """Create sample tensions for testing"""
    tensions = []
    
    # Data analysis tension
    tension1 = Tension(
        title="Sales Data Analysis Required",
        description="Need to analyze quarterly sales data to identify trends and patterns for strategic planning",
        priority=Priority.HIGH,
        tensionType=TensionType.DATA_ANALYSIS,
        tensionId="test_tension_001",
        status="Open",
        source="TestFixture",
        creationDate=datetime.now(),
        lastModifiedDate=datetime.now()
    )
    tensions.append(tension1)
    
    # Code generation tension
    tension2 = Tension(
        title="API Integration Development",
        description="Develop REST API integration for customer management system with authentication and error handling",
        priority=Priority.MEDIUM,
        tensionType=TensionType.TECHNICAL_DEBT,
        tensionId="test_tension_002",
        status="Open",
        source="TestFixture",
        creationDate=datetime.now(),
        lastModifiedDate=datetime.now()
    )
    tensions.append(tension2)
    
    # UI/UX tension
    tension3 = Tension(
        title="User Interface Redesign",
        description="Redesign user interface for better accessibility and mobile responsiveness",
        priority=Priority.HIGH,
        tensionType=TensionType.COMMUNICATION_BREAKDOWN,
        tensionId="test_tension_003",
        status="Open",
        source="TestFixture",
        creationDate=datetime.now(),
        lastModifiedDate=datetime.now()
    )
    tensions.append(tension3)
    
    return tensions


@pytest.fixture
def sample_agents(template_registry):
    """Create sample agents for testing"""
    agents = []
    
    # Create some template-based agents with proper IDs
    data_agent = DataAnalystAgent(agent_id="data_analyst_001")
    code_agent = CodeGeneratorAgent(agent_id="code_generator_001")
    
    agents.extend([data_agent, code_agent])
    
    return agents


# AdvancedAgentCreator Tests
class TestAdvancedAgentCreator:
    """Test suite for AdvancedAgentCreator"""
    
    def test_creator_initialization(self, template_registry):
        """Test AdvancedAgentCreator initialization"""
        creator = AdvancedAgentCreator(template_registry)
        
        assert creator.template_registry == template_registry
        assert creator.created_agents == {}
        assert creator.creation_stats["composite_agents_created"] == 0
        assert creator.creation_stats["custom_agents_created"] == 0
    
    @pytest.mark.asyncio
    async def test_compose_multi_template_agent(self, template_registry):
        """Test multi-template agent composition"""
        creator = AdvancedAgentCreator(template_registry)
        
        template_names = ["DataAnalystAgent", "CodeGeneratorAgent"]
        requirements = {
            "complexity": "high",
            "performance_target": 90
        }
        
        composite_agent = await creator.compose_multi_template_agent(
            template_names=template_names,
            requirements=requirements
        )
        
        assert composite_agent is not None
        assert isinstance(composite_agent, CompositeAgent)
        assert len(composite_agent.base_templates) == 2
        assert composite_agent.agent_id in creator.created_agents
        assert creator.creation_stats["composite_agents_created"] == 1
    
    @pytest.mark.asyncio
    async def test_compose_with_invalid_templates(self, template_registry):
        """Test composition with invalid template names"""
        creator = AdvancedAgentCreator(template_registry)
        
        template_names = ["InvalidTemplate", "AnotherInvalidTemplate"]
        requirements = {}
        
        composite_agent = await creator.compose_multi_template_agent(
            template_names=template_names,
            requirements=requirements
        )
        
        assert composite_agent is None
        assert creator.creation_stats["composite_agents_created"] == 0
    
    @pytest.mark.asyncio
    async def test_create_custom_agent_from_scratch(self, template_registry):
        """Test custom agent creation từ requirements"""
        creator = AdvancedAgentCreator(template_registry)
        
        requirements = CustomRequirements(
            name="CustomAnalyticsAgent",
            description="Specialized agent for advanced analytics",
            required_capabilities=["statistical_analysis", "data_visualization", "predictive_modeling"],
            domain_expertise=["finance", "marketing"],
            complexity_level="high"
        )
        
        custom_agent = await creator.create_custom_agent_from_scratch(requirements)
        
        assert custom_agent is not None
        assert isinstance(custom_agent, CustomAgent)
        assert custom_agent.requirements == requirements
        assert len(custom_agent.capabilities) == 3
        assert custom_agent.agent_id in creator.created_agents
        assert creator.creation_stats["custom_agents_created"] == 1
    
    @pytest.mark.asyncio
    async def test_create_custom_agent_invalid_requirements(self, template_registry):
        """Test custom agent creation với invalid requirements"""
        creator = AdvancedAgentCreator(template_registry)
        
        # Requirements without capabilities
        requirements = CustomRequirements(
            name="InvalidAgent",
            description="Agent without capabilities",
            required_capabilities=[],  # Empty capabilities
            domain_expertise=["general"]
        )
        
        custom_agent = await creator.create_custom_agent_from_scratch(requirements)
        
        assert custom_agent is None
        assert creator.creation_stats["custom_agents_created"] == 0
    
    @pytest.mark.asyncio
    async def test_optimize_agent_configuration(self, template_registry):
        """Test agent configuration optimization"""
        creator = AdvancedAgentCreator(template_registry)
        
        # Create a custom agent first
        requirements = CustomRequirements(
            name="TestAgent",
            description="Test agent for optimization",
            required_capabilities=["analysis"],
            domain_expertise=["testing"],
            complexity_level="medium"
        )
        
        agent = await creator.create_custom_agent_from_scratch(requirements)
        assert agent is not None
        
        # Optimize với low performance data
        performance_data = {
            "efficiency": 45,  # Low efficiency
            "quality": 60,
            "user_satisfaction": 55
        }
        
        optimized_agent = await creator.optimize_agent_configuration(agent, performance_data)
        
        assert optimized_agent is not None
        assert optimized_agent.agent_id == agent.agent_id
        # Complexity should be reduced due to low efficiency
        assert optimized_agent.requirements.complexity_level in ["low", "medium"]
    
    def test_get_created_agents(self, template_registry):
        """Test getting created agents"""
        creator = AdvancedAgentCreator(template_registry)
        
        # Initially empty
        agents = creator.get_created_agents()
        assert agents == {}
        
        # Add a mock agent
        mock_agent = CustomAgent(CustomRequirements(
            name="MockAgent",
            description="Mock agent",
            required_capabilities=["mock"],
            domain_expertise=["testing"]
        ))
        creator.created_agents[mock_agent.agent_id] = mock_agent
        
        agents = creator.get_created_agents()
        assert len(agents) == 1
        assert mock_agent.agent_id in agents
    
    def test_get_creation_stats(self, template_registry):
        """Test getting creation statistics"""
        creator = AdvancedAgentCreator(template_registry)
        
        stats = creator.get_creation_stats()
        assert "composite_agents_created" in stats
        assert "custom_agents_created" in stats
        assert "total_agents_created" in stats
        assert stats["total_agents_created"] == 0


# CompositeAgent Tests
class TestCompositeAgent:
    """Test suite for CompositeAgent"""
    
    def test_composite_agent_initialization(self, sample_agents):
        """Test CompositeAgent initialization"""
        composition_metadata = {
            "strategy": "multi_capability",
            "created_at": datetime.utcnow()
        }
        
        composite = CompositeAgent(
            base_templates=sample_agents,
            composition_metadata=composition_metadata
        )
        
        assert len(composite.base_templates) == len(sample_agents)
        assert composite.composition_metadata == composition_metadata
        assert len(composite.capabilities) > 0  # Should have combined capabilities
    
    @pytest.mark.asyncio
    async def test_composite_can_handle_tension(self, sample_agents, sample_tensions):
        """Test CompositeAgent tension handling"""
        composite = CompositeAgent(
            base_templates=sample_agents,
            composition_metadata={}
        )
        
        # Test với data analysis tension
        data_tension = sample_tensions[0]
        can_handle = await composite.can_handle_tension(data_tension)
        assert can_handle is True  # Should be able to handle via DataAnalystAgent
    
    @pytest.mark.asyncio
    async def test_composite_generate_solutions(self, sample_agents, sample_tensions):
        """Test CompositeAgent solution generation"""
        composite = CompositeAgent(
            base_templates=sample_agents,
            composition_metadata={}
        )
        
        # Test với code generation tension
        code_tension = sample_tensions[1]
        solutions = await composite.generate_specialized_solutions(code_tension)
        
        assert isinstance(solutions, list)
        assert len(solutions) > 0  # Should generate solutions


# CustomAgent Tests
class TestCustomAgent:
    """Test suite for CustomAgent"""
    
    def test_custom_agent_initialization(self):
        """Test CustomAgent initialization"""
        requirements = CustomRequirements(
            name="TestCustomAgent",
            description="Test custom agent",
            required_capabilities=["testing", "validation"],
            domain_expertise=["quality_assurance"],
            complexity_level="medium"
        )
        
        custom_agent = CustomAgent(requirements)
        
        assert custom_agent.requirements == requirements
        assert len(custom_agent.capabilities) == 2
        assert custom_agent.template_metadata.name == "TestCustomAgent"
    
    @pytest.mark.asyncio
    async def test_custom_agent_can_handle_tension(self, sample_tensions):
        """Test CustomAgent tension handling"""
        requirements = CustomRequirements(
            name="DataAgent",
            description="Data analysis agent",
            required_capabilities=["data_analysis"],
            domain_expertise=["sales", "analytics"]
        )
        
        custom_agent = CustomAgent(requirements)
        
        # Test với data tension
        data_tension = sample_tensions[0]  # Sales data analysis
        can_handle = await custom_agent.can_handle_tension(data_tension)
        assert can_handle is True  # Should match "sales" domain
    
    @pytest.mark.asyncio
    async def test_custom_agent_generate_solutions(self, sample_tensions):
        """Test CustomAgent solution generation"""
        requirements = CustomRequirements(
            name="GeneralAgent",
            description="General purpose agent",
            required_capabilities=["analysis", "problem_solving"],
            domain_expertise=["general"]
        )
        
        custom_agent = CustomAgent(requirements)
        
        solutions = await custom_agent.generate_specialized_solutions(sample_tensions[0])
        
        assert isinstance(solutions, list)
        assert len(solutions) == 2  # One per capability


# TemplateGenerator Tests
class TestTemplateGenerator:
    """Test suite for TemplateGenerator"""
    
    def test_template_generator_initialization(self):
        """Test TemplateGenerator initialization"""
        generator = TemplateGenerator()
        
        assert generator.identified_patterns == {}
        assert generator.generated_templates == {}
        assert generator.generation_stats["patterns_analyzed"] == 0
    
    @pytest.mark.asyncio
    async def test_analyze_successful_agent_patterns(self, sample_agents):
        """Test pattern analysis từ successful agents"""
        generator = TemplateGenerator()
        
        # Mock performance history
        performance_history = {
            sample_agents[0].agent_id: {
                "efficiency": 85,
                "quality": 90,
                "user_satisfaction": 88
            },
            sample_agents[1].agent_id: {
                "efficiency": 80,
                "quality": 85,
                "user_satisfaction": 82
            }
        }
        
        patterns = await generator.analyze_successful_agent_patterns(
            agents=sample_agents,
            performance_history=performance_history
        )
        
        assert isinstance(patterns, list)
        # May or may not find patterns depending on similarity
        assert generator.generation_stats["patterns_analyzed"] >= 0
    
    @pytest.mark.asyncio
    async def test_generate_template_from_pattern(self):
        """Test template generation từ pattern"""
        generator = TemplateGenerator()
        
        # Create a mock pattern
        pattern = AgentPattern(
            pattern_id="test_pattern_001",
            name="TestPattern",
            description="Test pattern for analytics",
            capabilities=["data_analysis", "reporting"],
            domain_expertise=["business", "analytics"],
            success_metrics={"effectiveness": 85},
            usage_frequency=5,
            effectiveness_score=85.0
        )
        
        template = await generator.generate_new_template_from_pattern(
            pattern=pattern,
            template_name="GeneratedAnalyticsTemplate"
        )
        
        assert template is not None
        assert isinstance(template, GeneratedTemplate)
        assert template.source_pattern == pattern
        assert template.template_name == "GeneratedAnalyticsTemplate"
        assert generator.generation_stats["templates_generated"] == 1
    
    @pytest.mark.asyncio
    async def test_validate_template_effectiveness(self, sample_tensions):
        """Test template validation"""
        generator = TemplateGenerator()
        
        # Create a pattern và template
        pattern = AgentPattern(
            pattern_id="test_pattern_002",
            name="HighEffectivePattern",
            description="High effectiveness pattern",
            capabilities=["analysis", "reporting", "visualization"],
            domain_expertise=["data", "business"],
            success_metrics={"effectiveness": 90},
            usage_frequency=8,
            effectiveness_score=90.0
        )
        
        template = GeneratedTemplate(pattern, "TestTemplate")
        
        validation = await generator.validate_template_effectiveness(
            template=template,
            test_tensions=sample_tensions
        )
        
        assert isinstance(validation, ValidationResult)
        assert validation.template_name == "TestTemplate"
        assert validation.validation_score > 0
        assert isinstance(validation.is_valid, bool)
    
    def test_get_generation_stats(self):
        """Test getting generation statistics"""
        generator = TemplateGenerator()
        
        stats = generator.get_generation_stats()
        assert "patterns_analyzed" in stats
        assert "templates_generated" in stats
        assert "average_effectiveness" in stats
        assert "validation_success_rate" in stats


# AgentCapabilityEvolver Tests
class TestAgentCapabilityEvolver:
    """Test suite for AgentCapabilityEvolver"""
    
    def test_evolver_initialization(self):
        """Test AgentCapabilityEvolver initialization"""
        evolver = AgentCapabilityEvolver()
        
        assert evolver.identified_gaps == {}
        assert evolver.evolution_history == {}
        assert len(evolver.evolution_strategies) > 0
        assert evolver.evolution_stats["agents_evolved"] == 0
    
    @pytest.mark.asyncio
    async def test_analyze_agent_performance_gaps(self, sample_agents):
        """Test performance gap analysis"""
        evolver = AgentCapabilityEvolver()
        
        # Mock poor performance data
        performance_data = {
            "efficiency": 45,  # Low efficiency
            "quality": 55,     # Low quality
            "capability_performance": {
                "data_analysis": 40  # Poor capability performance
            },
            "requested_but_missing": ["advanced_analytics"]  # Missing capability
        }
        
        agent = sample_agents[0]
        gaps = await evolver.analyze_agent_performance_gaps(
            agent=agent,
            performance_data=performance_data
        )
        
        assert isinstance(gaps, list)
        assert len(gaps) > 0  # Should identify multiple gaps
        assert agent.agent_id in evolver.identified_gaps
        assert evolver.evolution_stats["gaps_identified"] > 0
    
    @pytest.mark.asyncio
    async def test_evolve_agent_capabilities(self, sample_agents):
        """Test agent capability evolution"""
        evolver = AgentCapabilityEvolver()
        
        # Create some performance gaps
        gaps = [
            PerformanceGap(
                gap_id="gap_001",
                gap_type="efficiency",
                description="Low efficiency performance",
                severity="high",
                affected_capabilities=["data_analysis"],
                impact_score=30,
                recommended_actions=["optimize algorithms"]
            ),
            PerformanceGap(
                gap_id="gap_002",
                gap_type="missing_capability",
                description="Missing advanced analytics",
                severity="medium",
                affected_capabilities=["advanced_analytics"],
                impact_score=25,
                recommended_actions=["add capability"]
            )
        ]
        
        agent = sample_agents[0]
        result = await evolver.evolve_agent_capabilities(agent, gaps)
        
        assert isinstance(result, EvolutionResult)
        assert result.agent_id == agent.agent_id
        assert isinstance(result.success, bool)
        assert len(result.changes_made) >= 0
        assert evolver.evolution_stats["agents_evolved"] == 1
    
    @pytest.mark.asyncio
    async def test_validate_capability_improvements(self, sample_agents, sample_tensions):
        """Test capability improvement validation"""
        evolver = AgentCapabilityEvolver()
        
        before_agent = sample_agents[0]
        
        # Create "after" agent với improved capabilities
        after_agent = sample_agents[0]  # Same agent for simplicity
        
        validation = await evolver.validate_capability_improvements(
            before_agent=before_agent,
            after_agent=after_agent,
            test_tensions=sample_tensions
        )
        
        assert isinstance(validation, dict)
        assert "agent_id" in validation
        assert "capability_changes" in validation
        assert "validation_score" in validation
    
    def test_get_evolution_stats(self):
        """Test getting evolution statistics"""
        evolver = AgentCapabilityEvolver()
        
        stats = evolver.get_evolution_stats()
        assert "agents_evolved" in stats
        assert "gaps_identified" in stats
        assert "successful_evolutions" in stats
        assert "average_improvement" in stats
        assert "success_rate" in stats


# EcosystemOptimizer Tests
class TestEcosystemOptimizer:
    """Test suite for EcosystemOptimizer"""
    
    def test_optimizer_initialization(self):
        """Test EcosystemOptimizer initialization"""
        optimizer = EcosystemOptimizer()
        
        assert optimizer.ecosystems == {}
        assert optimizer.health_reports == {}
        assert optimizer.optimization_stats["ecosystems_optimized"] == 0
    
    def test_create_ecosystem(self):
        """Test ecosystem creation"""
        optimizer = EcosystemOptimizer()
        
        ecosystem = optimizer.create_ecosystem(
            name="TestEcosystem",
            description="Test ecosystem for validation"
        )
        
        assert isinstance(ecosystem, AgentEcosystem)
        assert ecosystem.name == "TestEcosystem"
        assert ecosystem.ecosystem_id in optimizer.ecosystems
    
    @pytest.mark.asyncio
    async def test_analyze_ecosystem_health(self, sample_agents):
        """Test ecosystem health analysis"""
        optimizer = EcosystemOptimizer()
        
        # Create ecosystem với agents
        ecosystem = optimizer.create_ecosystem("HealthTestEcosystem", "Test ecosystem")
        
        for agent in sample_agents:
            ecosystem.add_agent(agent)
        
        # Add some mock performance metrics
        ecosystem.performance_metrics = {
            sample_agents[0].agent_id: {"efficiency": 80, "quality": 85},
            sample_agents[1].agent_id: {"efficiency": 75, "quality": 80}
        }
        
        health_report = await optimizer.analyze_agent_ecosystem_health(ecosystem)
        
        assert isinstance(health_report, HealthReport)
        assert health_report.ecosystem_id == ecosystem.ecosystem_id
        assert health_report.overall_health_score >= 0
        assert len(health_report.agent_health) == len(sample_agents)
    
    @pytest.mark.asyncio
    async def test_optimize_agent_distribution(self, sample_agents, sample_tensions):
        """Test agent distribution optimization"""
        optimizer = EcosystemOptimizer()
        
        plan = await optimizer.optimize_agent_distribution(
            tensions=sample_tensions,
            agents=sample_agents
        )
        
        assert isinstance(plan, OptimizationPlan)
        assert plan.optimization_type == "agent_distribution"
        assert len(plan.actions) >= 0
        assert optimizer.optimization_stats["ecosystems_optimized"] == 1
    
    @pytest.mark.asyncio
    async def test_balance_workload_across_agents(self, sample_tensions):
        """Test workload balancing"""
        optimizer = EcosystemOptimizer()
        
        workload = Workload(
            workload_id="test_workload_001",
            tensions=sample_tensions
        )
        
        result = await optimizer.balance_workload_across_agents(workload)
        
        assert isinstance(result, BalancingResult)
        assert result.ecosystem_id == workload.workload_id
        assert isinstance(result.success, bool)
        assert len(result.redistributions) >= 0
        assert optimizer.optimization_stats["workload_balances_performed"] == 1
    
    def test_get_optimization_stats(self):
        """Test getting optimization statistics"""
        optimizer = EcosystemOptimizer()
        
        stats = optimizer.get_optimization_stats()
        assert "ecosystems_optimized" in stats
        assert "workload_balances_performed" in stats
        assert "average_efficiency_gain" in stats
        assert "total_efficiency_gained" in stats


# Integration Tests
class TestAdvancedGenesisEngineIntegration:
    """Integration tests for Advanced Genesis Engine components"""
    
    @pytest.mark.asyncio
    async def test_full_genesis_workflow(self, template_registry, sample_tensions):
        """Test complete Genesis Engine workflow"""
        # Step 1: Create advanced agent creator
        creator = AdvancedAgentCreator(template_registry)
        
        # Step 2: Create composite agent
        composite_agent = await creator.compose_multi_template_agent(
            template_names=["DataAnalystAgent", "CodeGeneratorAgent"],
            requirements={"complexity": "high"}
        )
        assert composite_agent is not None
        
        # Step 3: Test agent với tensions
        can_handle = await composite_agent.can_handle_tension(sample_tensions[0])
        assert isinstance(can_handle, bool)
        
        # Step 4: Generate solutions
        solutions = await composite_agent.generate_specialized_solutions(sample_tensions[0])
        assert isinstance(solutions, list)
        
        # Step 5: Create ecosystem và add agent
        optimizer = EcosystemOptimizer()
        ecosystem = optimizer.create_ecosystem("IntegrationTest", "Integration test ecosystem")
        ecosystem.add_agent(composite_agent)
        
        # Step 6: Analyze ecosystem health
        health_report = await optimizer.analyze_agent_ecosystem_health(ecosystem)
        assert isinstance(health_report, HealthReport)
        assert health_report.overall_health_score > 0
    
    @pytest.mark.asyncio
    async def test_agent_evolution_workflow(self, sample_agents):
        """Test agent evolution workflow"""
        # Step 1: Analyze performance gaps
        evolver = AgentCapabilityEvolver()
        
        performance_data = {
            "efficiency": 50,
            "quality": 60,
            "capability_performance": {"data_analysis": 45}
        }
        
        agent = sample_agents[0]
        gaps = await evolver.analyze_agent_performance_gaps(agent, performance_data)
        assert len(gaps) > 0
        
        # Step 2: Evolve capabilities
        evolution_result = await evolver.evolve_agent_capabilities(agent, gaps)
        assert isinstance(evolution_result, EvolutionResult)
        
        # Step 3: Validate improvements
        validation = await evolver.validate_capability_improvements(agent, agent)
        assert isinstance(validation, dict)
        assert "validation_score" in validation
    
    @pytest.mark.asyncio
    async def test_template_generation_workflow(self, sample_agents):
        """Test template generation workflow"""
        # Step 1: Analyze patterns
        generator = TemplateGenerator()
        
        patterns = await generator.analyze_successful_agent_patterns(sample_agents)
        assert isinstance(patterns, list)
        
        # Step 2: Generate template nếu có patterns
        if patterns:
            template = await generator.generate_new_template_from_pattern(patterns[0])
            assert template is not None
            
            # Step 3: Validate template
            validation = await generator.validate_template_effectiveness(template)
            assert isinstance(validation, ValidationResult)


# Performance Tests
class TestAdvancedGenesisEnginePerformance:
    """Performance tests for Advanced Genesis Engine"""
    
    @pytest.mark.asyncio
    async def test_agent_creation_performance(self, template_registry):
        """Test agent creation performance"""
        creator = AdvancedAgentCreator(template_registry)
        
        start_time = datetime.utcnow()
        
        # Create multiple agents
        for i in range(5):
            requirements = CustomRequirements(
                name=f"PerfTestAgent_{i}",
                description=f"Performance test agent {i}",
                required_capabilities=["testing"],
                domain_expertise=["performance"]
            )
            
            agent = await creator.create_custom_agent_from_scratch(requirements)
            assert agent is not None
        
        end_time = datetime.utcnow()
        duration = (end_time - start_time).total_seconds()
        
        # Should create 5 agents in reasonable time
        assert duration < 5.0  # Less than 5 seconds
        assert creator.creation_stats["custom_agents_created"] == 5
    
    @pytest.mark.asyncio
    async def test_ecosystem_optimization_performance(self, sample_agents, sample_tensions):
        """Test ecosystem optimization performance"""
        optimizer = EcosystemOptimizer()
        
        start_time = datetime.utcnow()
        
        # Create large ecosystem
        ecosystem = optimizer.create_ecosystem("LargeEcosystem", "Large test ecosystem")
        
        # Add multiple agents
        for i, agent in enumerate(sample_agents * 3):  # Multiply to get more agents
            agent.agent_id = f"{agent.agent_id}_{i}"  # Make unique IDs
            ecosystem.add_agent(agent)
        
        # Add multiple tensions
        ecosystem.active_tensions = sample_tensions * 5
        
        # Analyze health
        health_report = await optimizer.analyze_agent_ecosystem_health(ecosystem)
        
        end_time = datetime.utcnow()
        duration = (end_time - start_time).total_seconds()
        
        # Should complete analysis in reasonable time
        assert duration < 10.0  # Less than 10 seconds
        assert isinstance(health_report, HealthReport)
        assert health_report.overall_health_score >= 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 