"""
Advanced Agent Creator

Advanced Genesis Engine component cho việc tạo ra sophisticated agents
thông qua template composition và custom agent creation từ requirements.
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional, Type, Union, Tuple
from datetime import datetime
from abc import ABC
import uuid

from ..templates.base_template import BaseAgentTemplate, AgentTemplateMetadata, AgentCapability
from ..templates.template_registry import AgentTemplateRegistry, TemplateMatchResult
from ..base_agent import BaseAgent, AgentMetadata
from ...models.tension import Tension
from ...models.enums import AgentType, TensionType, Priority


class CustomRequirements:
    """Requirements for custom agent creation"""
    
    def __init__(self, name: str, description: str, required_capabilities: List[str], 
                 domain_expertise: List[str], complexity_level: str = "medium"):
        self.name = name
        self.description = description
        self.required_capabilities = required_capabilities
        self.domain_expertise = domain_expertise
        self.complexity_level = complexity_level


class CompositeAgent(BaseAgentTemplate):
    """Agent created by composing multiple templates"""
    
    def __init__(self, base_templates: List[BaseAgentTemplate], composition_metadata: Dict[str, Any], agent_id: Optional[str] = None):
        # Set attributes before calling super().__init__()
        self.base_templates = base_templates
        self.composition_metadata = composition_metadata
        
        # Combine capabilities from all base templates
        combined_capabilities = self._combine_template_capabilities(base_templates)
        
        # Create composite metadata
        template_metadata = AgentTemplateMetadata(
            template_name=f"Composite_{len(base_templates)}_Templates",
            primary_domain="composite",
            capabilities=combined_capabilities,
            domain_expertise=self._combine_domain_expertise(base_templates),
            supported_tension_types=self._combine_supported_tensions(base_templates),
            performance_metrics={"composite_efficiency": 0.85, "synergy_score": 0.8, "flexibility": 0.9},
            version="1.0.0"
        )
        
        super().__init__(agent_id=agent_id or f"composite_{uuid.uuid4().hex[:8]}", template_metadata=template_metadata)
        
        # Store capabilities for test access
        self.capabilities = combined_capabilities
        
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def _combine_template_capabilities(self, templates: List[BaseAgentTemplate]) -> List[AgentCapability]:
        """Combine capabilities from multiple templates"""
        combined_capabilities = []
        seen_capabilities = set()
        
        for template in templates:
            if hasattr(template, 'template_metadata') and template.template_metadata:
                if hasattr(template.template_metadata, 'capabilities') and template.template_metadata.capabilities:
                    for capability in template.template_metadata.capabilities:
                        if capability.name not in seen_capabilities:
                            combined_capabilities.append(capability)
                            seen_capabilities.add(capability.name)
        
        # If no capabilities found, create default ones
        if not combined_capabilities:
            combined_capabilities = [
                AgentCapability(
                    name="composite_processing",
                    description="Combined processing from multiple templates",
                    proficiency_level=0.8,
                    estimated_time_per_task=60.0
                )
            ]
        
        return combined_capabilities
    
    def _combine_domain_expertise(self, templates: List[BaseAgentTemplate]) -> List[str]:
        """Combine domain expertise from multiple templates"""
        combined_expertise = set()
        
        for template in templates:
            if hasattr(template, 'template_metadata') and template.template_metadata:
                if hasattr(template.template_metadata, 'domain_expertise'):
                    combined_expertise.update(template.template_metadata.domain_expertise)
        
        return list(combined_expertise) if combined_expertise else ["general"]
    
    def _combine_supported_tensions(self, templates: List[BaseAgentTemplate]) -> List[TensionType]:
        """Combine supported tension types from multiple templates"""
        combined_tensions = set()
        
        for template in templates:
            if hasattr(template, 'template_metadata') and template.template_metadata:
                if hasattr(template.template_metadata, 'supported_tension_types'):
                    combined_tensions.update(template.template_metadata.supported_tension_types)
        
        return list(combined_tensions) if combined_tensions else [TensionType.UNKNOWN]
    
    def _get_default_template_metadata(self) -> AgentTemplateMetadata:
        """Get default template metadata for composite agent"""
        return AgentTemplateMetadata(
            template_name="CompositeAgent",
            primary_domain="composite",
            capabilities=[
                AgentCapability(
                    name="multi_template_processing",
                    description="Processing using multiple template capabilities",
                    proficiency_level=0.8,
                    estimated_time_per_task=60.0
                )
            ],
            domain_expertise=["general"],
            supported_tension_types=[TensionType.UNKNOWN],
            performance_metrics={"efficiency": 0.8, "flexibility": 0.9},
            version="1.0.0"
        )
    
    async def _register_specialized_handlers(self) -> None:
        """Register specialized event handlers"""
        pass
    
    async def _initialize_specialized_components(self) -> None:
        """Initialize specialized components"""
        pass
    
    async def _handle_specialized_event(self, event) -> None:
        """Handle specialized events"""
        pass

    async def generate_specialized_solutions(self, tension: Tension, requirements: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Generate solutions by leveraging all base templates.
        """
        try:
            all_solutions = []
            
            # Get solutions from each base template that can handle the tension
            for template in self.base_templates:
                if await template.can_handle_tension(tension):
                    template_solutions = await template.generate_specialized_solutions(tension, requirements)
                    if template_solutions:
                        all_solutions.extend(template_solutions)
            
            # If no base template can handle it, use base implementation
            if not all_solutions:
                all_solutions = await super().generate_specialized_solutions(tension, requirements)
            
            self.logger.info(f"CompositeAgent generated {len(all_solutions)} solutions for tension {tension.tensionId}")
            return all_solutions
            
        except Exception as e:
            self.logger.error(f"Error generating solutions: {e}")
            return []


class CustomAgent(BaseAgentTemplate):
    """Agent created from scratch based on custom requirements"""
    
    def __init__(self, requirements: CustomRequirements, agent_id: Optional[str] = None):
        # Set requirements before calling super().__init__()
        self.requirements = requirements
        
        # Create capabilities from requirements
        capabilities = []
        for cap_name in requirements.required_capabilities:
            capabilities.append(AgentCapability(
                name=cap_name,
                description=f"Custom capability: {cap_name}",
                proficiency_level=0.7,
                estimated_time_per_task=60.0
            ))
        
        # Create template metadata
        template_metadata = AgentTemplateMetadata(
            template_name=requirements.name,
            primary_domain=requirements.domain_expertise[0] if requirements.domain_expertise else "general",
            capabilities=capabilities,
            domain_expertise=requirements.domain_expertise,
            supported_tension_types=[TensionType.UNKNOWN],
            performance_metrics={"efficiency": 0.7, "quality": 0.8, "satisfaction": 0.75},
            version="1.0.0"
        )
        
        super().__init__(agent_id=agent_id or f"custom_{uuid.uuid4().hex[:8]}", template_metadata=template_metadata)
        
        self.capabilities = capabilities
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def _get_default_template_metadata(self) -> AgentTemplateMetadata:
        """Get default template metadata for custom agent"""
        return AgentTemplateMetadata(
            template_name=self.requirements.name,
            primary_domain=self.requirements.domain_expertise[0] if self.requirements.domain_expertise else "general",
            capabilities=[],
            domain_expertise=self.requirements.domain_expertise,
            supported_tension_types=[TensionType.UNKNOWN],
            performance_metrics={"efficiency": 0.7, "quality": 0.8, "satisfaction": 0.75},
            version="1.0.0"
        )
    
    async def _register_specialized_handlers(self) -> None:
        """Register specialized event handlers"""
        pass
    
    async def _initialize_specialized_components(self) -> None:
        """Initialize specialized components"""
        pass
    
    async def _handle_specialized_event(self, event) -> None:
        """Handle specialized events"""
        pass

    async def generate_specialized_solutions(self, tension: Tension, requirements: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Generate solutions based on custom capabilities.
        """
        try:
            solutions = []
            
            # Generate one solution per capability
            for capability in self.capabilities:
                solution = {
                    "id": f"custom_solution_{tension.tensionId}_{capability.name}",
                    "type": f"custom_{capability.name}_solution",
                    "description": f"Solution using {capability.name} capability: {capability.description}",
                    "approach": "custom_capability_based",
                    "expected_win_score": 70.0,
                    "confidence": capability.proficiency_level,
                    "estimated_time": capability.estimated_time_per_task,
                    "required_resources": [capability.name],
                    "success_probability": capability.proficiency_level * 100
                }
                solutions.append(solution)
            
            self.logger.info(f"CustomAgent generated {len(solutions)} solutions for tension {tension.tensionId}")
            return solutions
            
        except Exception as e:
            self.logger.error(f"Error generating solutions: {e}")
            return []


class AdvancedAgentCreator:
    """
    Advanced agent creation system for TRM-OS.
    
    Capabilities:
    - Compose multiple templates into composite agents
    - Create custom agents from scratch
    - Optimize agent configurations
    - Track creation performance
    """
    
    def __init__(self, template_registry: AgentTemplateRegistry):
        self.template_registry = template_registry
        self.created_agents: Dict[str, BaseAgentTemplate] = {}
        self.creation_stats = {
            "composite_agents_created": 0,
            "custom_agents_created": 0,
            "total_creation_time": 0.0,
            "average_creation_time": 0.0
        }
        self.logger = logging.getLogger(self.__class__.__name__)
    
    async def compose_multi_template_agent(self, template_names: List[str], requirements: Dict[str, Any]) -> Optional[CompositeAgent]:
        """
        Compose multiple templates into a single composite agent.
        
        Args:
            template_names: List of template names to compose
            requirements: Requirements for the composite agent
            
        Returns:
            CompositeAgent if successful, None otherwise
        """
        try:
            # Validate input
            if not template_names:
                self.logger.error("No template names provided for composition")
                return None
            
            # Get template instances
            base_templates = []
            for template_name in template_names:
                # Check if template exists in registry using proper method
                available_templates = self.template_registry.get_available_templates()
                if template_name not in available_templates:
                    self.logger.error(f"Template '{template_name}' not found in registry")
                    return None
                
                template_instance = await self.template_registry.create_agent_from_template(template_name)
                if template_instance:
                    base_templates.append(template_instance)
                else:
                    self.logger.error(f"Failed to create instance of template: {template_name}")
                    return None
            
            if not base_templates:
                self.logger.error("No valid templates found for composition")
                return None
            
            # Create composition metadata
            composition_metadata = {
                "base_template_names": template_names,
                "requirements": requirements,
                "composition_strategy": "additive",
                "created_at": datetime.now()
            }
            
            # Create composite agent
            composite_agent = CompositeAgent(
                base_templates=base_templates,
                composition_metadata=composition_metadata
            )
            
            # Track the created agent
            self.created_agents[composite_agent.agent_id] = composite_agent
            self.creation_stats["composite_agents_created"] += 1
            
            self.logger.info(f"Successfully created composite agent: {composite_agent.agent_id}")
            return composite_agent
            
        except Exception as e:
            self.logger.error(f"Error creating composite agent: {e}")
            return None
    
    async def create_custom_agent_from_scratch(self, requirements: CustomRequirements) -> Optional[CustomAgent]:
        """
        Create a custom agent from scratch based on requirements.
        
        Args:
            requirements: Custom requirements for the agent
            
        Returns:
            CustomAgent if successful, None otherwise
        """
        try:
            # Validate requirements
            if not requirements.required_capabilities:
                self.logger.error("Custom agent requires at least one capability")
                return None
            
            # Create custom agent
            custom_agent = CustomAgent(requirements)
            
            # Track the created agent
            self.created_agents[custom_agent.agent_id] = custom_agent
            self.creation_stats["custom_agents_created"] += 1
            
            self.logger.info(f"Successfully created custom agent: {custom_agent.agent_id}")
            return custom_agent
            
        except Exception as e:
            self.logger.error(f"Error creating custom agent: {e}")
            return None
    
    async def optimize_agent_configuration(self, agent: BaseAgentTemplate, performance_data: Dict[str, Any]) -> Optional[BaseAgentTemplate]:
        """
        Optimize agent configuration based on performance data.
        
        Args:
            agent: Agent to optimize
            performance_data: Performance metrics
            
        Returns:
            Optimized agent if successful, None otherwise
        """
        try:
            # For CustomAgent, we can modify the requirements
            if isinstance(agent, CustomAgent):
                # Create optimized requirements
                optimized_requirements = CustomRequirements(
                    name=agent.requirements.name,
                    description=agent.requirements.description,
                    required_capabilities=agent.requirements.required_capabilities.copy(),
                    domain_expertise=agent.requirements.domain_expertise.copy(),
                    complexity_level=agent.requirements.complexity_level
                )
                
                # Apply optimizations based on performance data
                efficiency = performance_data.get("efficiency", 100)
                quality = performance_data.get("quality", 100)
                
                # Reduce complexity if performance is poor
                if efficiency < 50:
                    if optimized_requirements.complexity_level == "high":
                        optimized_requirements.complexity_level = "medium"
                    elif optimized_requirements.complexity_level == "medium":
                        optimized_requirements.complexity_level = "low"
                
                # Add capabilities if quality is low
                if quality < 60 and "quality_assurance" not in optimized_requirements.required_capabilities:
                    optimized_requirements.required_capabilities.append("quality_assurance")
                
                # Create optimized agent with same agent_id
                optimized_agent = CustomAgent(optimized_requirements, agent_id=agent.agent_id)
                
                # Update in created_agents
                self.created_agents[agent.agent_id] = optimized_agent
                
                self.logger.info(f"Optimized agent {agent.agent_id} configuration")
                return optimized_agent
            
            else:
                # For other agent types, return the original agent
                self.logger.info(f"Agent {agent.agent_id} optimization not supported for this type")
                return agent
            
        except Exception as e:
            self.logger.error(f"Error optimizing agent configuration: {e}")
            return None
    
    def get_created_agents(self) -> Dict[str, BaseAgentTemplate]:
        """Get all created agents"""
        return self.created_agents.copy()
    
    def get_creation_stats(self) -> Dict[str, Any]:
        """Get creation statistics"""
        total_agents = self.creation_stats["composite_agents_created"] + self.creation_stats["custom_agents_created"]
        
        stats = self.creation_stats.copy()
        stats["total_agents_created"] = total_agents
        
        if total_agents > 0:
            stats["average_creation_time"] = self.creation_stats["total_creation_time"] / total_agents
        
        return stats 