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
    """Requirements cho custom agent creation"""
    
    def __init__(self, 
                 name: str,
                 description: str,
                 required_capabilities: List[str],
                 domain_expertise: List[str],
                 complexity_level: str = "medium",
                 performance_requirements: Optional[Dict[str, Any]] = None,
                 constraints: Optional[Dict[str, Any]] = None):
        self.name = name
        self.description = description
        self.required_capabilities = required_capabilities
        self.domain_expertise = domain_expertise
        self.complexity_level = complexity_level
        self.performance_requirements = performance_requirements or {}
        self.constraints = constraints or {}
        self.created_at = datetime.utcnow()


class CompositeAgent(BaseAgentTemplate):
    """Agent được tạo từ composition của multiple templates"""
    
    def __init__(self, 
                 base_templates: List[BaseAgentTemplate],
                 composition_metadata: Dict[str, Any],
                 agent_id: Optional[str] = None):
        
        # Set attributes before calling super()
        self.base_templates = base_templates
        self.composition_metadata = composition_metadata
        
        # Initialize base
        super().__init__(agent_id or f"composite_{uuid.uuid4().hex[:8]}")
        
        # Combine capabilities từ all templates
        self._combine_template_capabilities()
        
        # Setup composite metadata
        self._setup_composite_metadata()
    
    def _combine_template_capabilities(self) -> None:
        """Combine capabilities từ tất cả base templates"""
        combined_capabilities = []
        
        for template in self.base_templates:
            # Check if template has capabilities attribute
            if hasattr(template, 'capabilities') and template.capabilities:
                for capability in template.capabilities:
                    if capability not in combined_capabilities:
                        combined_capabilities.append(capability)
            elif hasattr(template, 'template_metadata') and template.template_metadata:
                # Fallback to template metadata capabilities
                if hasattr(template.template_metadata, 'capabilities'):
                    for capability in template.template_metadata.capabilities:
                        if capability not in combined_capabilities:
                            combined_capabilities.append(capability)
        
        self.capabilities = combined_capabilities
    
    def _setup_composite_metadata(self) -> None:
        """Setup metadata cho composite agent"""
        template_names = [t.__class__.__name__ for t in self.base_templates]
        
        self.template_metadata = AgentTemplateMetadata(
            template_name=f"CompositeAgent_{self.agent_id}",
            template_version="1.0.0",
            description=f"Composite agent from templates: {', '.join(template_names)}",
            primary_domain="multi_domain",
            capabilities=self.capabilities,
            recommended_tensions=["complex", "multi_domain"],
            dependencies=template_names,
            performance_metrics=["efficiency", "quality", "coverage"]
        )
    
    def _combine_domain_expertise(self) -> List[str]:
        """Combine domain expertise từ all templates"""
        combined_domains = []
        for template in self.base_templates:
            if hasattr(template, 'template_metadata') and template.template_metadata:
                # Check if domain_expertise exists
                if hasattr(template.template_metadata, 'domain_expertise'):
                    for domain in template.template_metadata.domain_expertise:
                        if domain not in combined_domains:
                            combined_domains.append(domain)
                elif hasattr(template.template_metadata, 'primary_domain'):
                    # Fallback to primary_domain if domain_expertise doesn't exist
                    if template.template_metadata.primary_domain not in combined_domains:
                        combined_domains.append(template.template_metadata.primary_domain)
        return combined_domains
    
    def _combine_tension_types(self) -> List[TensionType]:
        """Combine supported tension types"""
        combined_types = []
        for template in self.base_templates:
            if hasattr(template, 'template_metadata') and template.template_metadata:
                # Check if supported_tension_types exists
                if hasattr(template.template_metadata, 'supported_tension_types'):
                    for tension_type in template.template_metadata.supported_tension_types:
                        if tension_type not in combined_types:
                            combined_types.append(tension_type)
                # Default tension types if not specified
                elif not combined_types:
                    combined_types.append(TensionType.PROCESS_IMPROVEMENT)
        
        # Ensure we have at least one tension type
        if not combined_types:
            combined_types.append(TensionType.PROCESS_IMPROVEMENT)
            
        return combined_types
    
    def _estimate_composite_resolution_time(self) -> int:
        """Estimate resolution time cho composite agent"""
        total_time = 0
        template_count = 0
        
        for template in self.base_templates:
            if hasattr(template, 'template_metadata') and template.template_metadata:
                # Check if estimated_resolution_time exists
                if hasattr(template.template_metadata, 'estimated_resolution_time'):
                    total_time += template.template_metadata.estimated_resolution_time
                    template_count += 1
                else:
                    # Default resolution time
                    total_time += 120  # 2 hours default
                    template_count += 1
        
        if template_count == 0:
            return 120  # Default 2 hours
        
        # Average resolution time với efficiency gain
        avg_time = total_time / template_count
        return int(avg_time * 0.8)  # 20% efficiency gain from composition
    
    async def can_handle_tension(self, tension: Tension) -> bool:
        """Check if composite agent có thể handle tension"""
        # Composite agent có thể handle nếu ít nhất 1 template có thể handle
        for template in self.base_templates:
            if await template.can_handle_tension(tension):
                return True
        return False
    
    async def analyze_tension_requirements(self, tension: Tension) -> Dict[str, Any]:
        """Analyze tension requirements using all templates"""
        all_requirements = {}
        
        for template in self.base_templates:
            if await template.can_handle_tension(tension):
                template_reqs = await template.analyze_tension_requirements(tension)
                # Merge requirements
                for key, value in template_reqs.items():
                    if key not in all_requirements:
                        all_requirements[key] = value
                    elif isinstance(value, list):
                        all_requirements[key].extend(value)
        
        return all_requirements
    
    async def generate_specialized_solutions(self, tension: Tension) -> List[Dict[str, Any]]:
        """Generate solutions using all capable templates"""
        all_solutions = []
        
        for template in self.base_templates:
            if await template.can_handle_tension(tension):
                # Analyze requirements for this template
                requirements = await template.analyze_tension_requirements(tension)
                template_solutions = await template.generate_specialized_solutions(tension, requirements)
                all_solutions.extend(template_solutions)
        
        return all_solutions
    
    async def execute_solution(self, solution: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute solution using most appropriate template"""
        # Find best template for this solution
        best_template = None
        best_score = 0
        
        for template in self.base_templates:
            # Simple scoring based on capability match
            template_capabilities = []
            if hasattr(template, 'capabilities') and template.capabilities:
                template_capabilities = [cap.name for cap in template.capabilities]
            elif hasattr(template, 'template_metadata') and template.template_metadata:
                if hasattr(template.template_metadata, 'capabilities'):
                    template_capabilities = [cap.name for cap in template.template_metadata.capabilities]
            
            score = len([cap for cap in template_capabilities 
                       if cap in solution.get("required_capabilities", [])])
            if score > best_score:
                best_score = score
                best_template = template
        
        if best_template:
            return await best_template.execute_solution(solution, context)
        else:
            return {"status": "error", "message": "No suitable template found for execution"}
    
    def _get_default_template_metadata(self) -> AgentTemplateMetadata:
        """Get default template metadata for composite agent"""
        template_names = [t.__class__.__name__ for t in self.base_templates]
        
        # Get capabilities from base templates if not yet combined
        capabilities = []
        if hasattr(self, 'capabilities') and self.capabilities:
            capabilities = self.capabilities
        else:
            # Combine capabilities from base templates
            for template in self.base_templates:
                if hasattr(template, 'capabilities') and template.capabilities:
                    for capability in template.capabilities:
                        if capability not in capabilities:
                            capabilities.append(capability)
                elif hasattr(template, 'template_metadata') and template.template_metadata:
                    # Fallback to template metadata capabilities
                    if hasattr(template.template_metadata, 'capabilities'):
                        for capability in template.template_metadata.capabilities:
                            if capability not in capabilities:
                                capabilities.append(capability)
        
        return AgentTemplateMetadata(
            template_name=f"CompositeAgent_{self.agent_id}",
            template_version="1.0.0",
            description=f"Composite agent from templates: {', '.join(template_names)}",
            primary_domain="multi_domain",
            capabilities=capabilities,
            recommended_tensions=["complex", "multi_domain"],
            dependencies=template_names,
            performance_metrics=["efficiency", "quality", "coverage"]
        )
    
    async def _register_specialized_handlers(self) -> None:
        """Register specialized event handlers for composite agent"""
        # Composite agents handle composition events
        pass
    
    async def _initialize_specialized_components(self) -> None:
        """Initialize specialized components for composite agent"""
        # Initialize coordination between templates
        pass
    
    async def _handle_specialized_event(self, event) -> None:
        """Handle specialized events for composite agent"""
        # Handle composition-specific events
        pass


class CustomAgent(BaseAgentTemplate):
    """Custom agent được tạo từ scratch theo requirements"""
    
    def __init__(self, requirements: CustomRequirements, agent_id: Optional[str] = None):
        # Set requirements before calling super()
        self.requirements = requirements
        
        super().__init__(agent_id or f"custom_{uuid.uuid4().hex[:8]}")
        
        self._setup_custom_capabilities()
        self._setup_custom_metadata()
    
    def _setup_custom_capabilities(self) -> None:
        """Setup capabilities based on requirements"""
        self.capabilities = []
        
        for cap_name in self.requirements.required_capabilities:
            capability = AgentCapability(
                name=cap_name,
                description=f"Custom capability: {cap_name}",
                proficiency_level=85,  # Default proficiency
                tools_required=[],
                estimated_time_per_task=60
            )
            self.capabilities.append(capability)
    
    def _setup_custom_metadata(self) -> None:
        """Setup metadata cho custom agent"""
        self.template_metadata = AgentTemplateMetadata(
            template_name=self.requirements.name,
            template_version="1.0.0",
            description=self.requirements.description,
            primary_domain=self.requirements.domain_expertise[0] if self.requirements.domain_expertise else "general",
            capabilities=self.capabilities,
            recommended_tensions=["custom", "specialized"],
            dependencies=[],
            performance_metrics=["efficiency", "quality", "satisfaction"]
        )
    
    def _estimate_resolution_time(self) -> int:
        """Estimate resolution time based on complexity"""
        base_time = 120  # 2 hours base
        complexity_multiplier = {
            "low": 0.5,
            "medium": 1.0,
            "high": 1.5,
            "very_high": 2.0
        }
        
        multiplier = complexity_multiplier.get(self.requirements.complexity_level, 1.0)
        return int(base_time * multiplier)
    
    async def can_handle_tension(self, tension: Tension) -> bool:
        """Check if custom agent có thể handle tension"""
        # Simple check based on domain expertise và capabilities
        description_lower = tension.description.lower()
        title_lower = tension.title.lower()
        
        # Check domain expertise match
        for domain in self.requirements.domain_expertise:
            if domain.lower() in description_lower or domain.lower() in title_lower:
                return True
        
        # Check capability match
        for cap in self.requirements.required_capabilities:
            if cap.lower() in description_lower or cap.lower() in title_lower:
                return True
        
        return False
    
    async def analyze_tension_requirements(self, tension: Tension) -> Dict[str, Any]:
        """Analyze tension requirements"""
        return {
            "domain_match": self.requirements.domain_expertise,
            "capability_match": self.requirements.required_capabilities,
            "complexity": self.requirements.complexity_level,
            "estimated_effort": self.template_metadata.estimated_resolution_time,
            "custom_constraints": self.requirements.constraints
        }
    
    async def generate_specialized_solutions(self, tension: Tension) -> List[Dict[str, Any]]:
        """Generate custom solutions"""
        solutions = []
        
        # Generate solution based on capabilities
        for capability in self.capabilities:
            solution = {
                "title": f"Custom Solution using {capability.name}",
                "description": f"Apply {capability.name} to address {tension.title}",
                "approach": "custom_implementation",
                "required_capabilities": [capability.name],
                "estimated_effort": capability.estimated_time_per_task,
                "confidence_score": 75,  # Default confidence
                "implementation_steps": [
                    f"Analyze {tension.title} using {capability.name}",
                    f"Design solution approach",
                    f"Implement solution",
                    f"Validate results"
                ]
            }
            solutions.append(solution)
        
        return solutions
    
    async def execute_solution(self, solution: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute custom solution"""
        return {
            "status": "completed",
            "agent_id": self.agent_id,
            "solution_type": "custom_implementation",
            "execution_time": solution.get("estimated_effort", 60),
            "results": {
                "approach_used": solution.get("approach", "custom"),
                "capabilities_applied": solution.get("required_capabilities", []),
                "implementation_notes": f"Custom solution executed"
            },
            "performance_metrics": {
                "efficiency": 85,
                "quality": 80,
                "innovation": 90
            }
        }
    
    def _get_default_template_metadata(self) -> AgentTemplateMetadata:
        """Get default template metadata for custom agent"""
        # Get capabilities if available, otherwise use empty list
        capabilities = []
        if hasattr(self, 'capabilities') and self.capabilities:
            capabilities = self.capabilities
        
        return AgentTemplateMetadata(
            template_name=self.requirements.name,
            template_version="1.0.0",
            description=self.requirements.description,
            primary_domain=self.requirements.domain_expertise[0] if self.requirements.domain_expertise else "general",
            capabilities=capabilities,
            recommended_tensions=["custom", "specialized"],
            dependencies=[],
            performance_metrics=["efficiency", "quality", "satisfaction"]
        )
    
    async def _register_specialized_handlers(self) -> None:
        """Register specialized event handlers for custom agent"""
        # Custom agents handle domain-specific events
        pass
    
    async def _initialize_specialized_components(self) -> None:
        """Initialize specialized components for custom agent"""
        # Initialize custom components based on requirements
        pass
    
    async def _handle_specialized_event(self, event) -> None:
        """Handle specialized events for custom agent"""
        # Handle custom domain events
        pass


class AdvancedAgentCreator:
    """
    Advanced Agent Creator cho TRM-OS Genesis Engine.
    
    Capabilities:
    - Compose multiple templates thành composite agents
    - Create custom agents từ scratch
    - Optimize agent configurations
    - Validate agent effectiveness
    """
    
    def __init__(self, template_registry: AgentTemplateRegistry):
        self.logger = logging.getLogger("AdvancedAgentCreator")
        self.template_registry = template_registry
        self.created_agents: Dict[str, Union[CompositeAgent, CustomAgent]] = {}
        self.creation_stats = {
            "composite_agents_created": 0,
            "custom_agents_created": 0,
            "total_agents_created": 0,
            "success_rate": 0.0
        }
    
    async def compose_multi_template_agent(self, 
                                         template_names: List[str],
                                         requirements: Dict[str, Any],
                                         agent_id: Optional[str] = None) -> Optional[CompositeAgent]:
        """
        Compose multiple templates thành một composite agent.
        
        Args:
            template_names: Danh sách tên templates để compose
            requirements: Requirements và constraints cho composite agent
            agent_id: Optional agent ID
            
        Returns:
            CompositeAgent instance hoặc None nếu failed
        """
        try:
            self.logger.info(f"Composing agent from templates: {template_names}")
            
            # Validate template names
            available_templates = self.template_registry.get_available_templates()
            invalid_templates = [name for name in template_names if name not in available_templates]
            
            if invalid_templates:
                self.logger.error(f"Invalid template names: {invalid_templates}")
                return None
            
            # Create template instances
            base_templates = []
            for template_name in template_names:
                template_instance = await self.template_registry.create_agent_from_template(template_name)
                if template_instance:
                    base_templates.append(template_instance)
                else:
                    self.logger.error(f"Failed to create instance of template: {template_name}")
                    return None
            
            if not base_templates:
                self.logger.error("No template instances created")
                return None
            
            # Create composition metadata
            composition_metadata = {
                "template_names": template_names,
                "requirements": requirements,
                "created_at": datetime.utcnow(),
                "composition_strategy": "multi_template_merge"
            }
            
            # Create composite agent
            composite_agent = CompositeAgent(
                base_templates=base_templates,
                composition_metadata=composition_metadata,
                agent_id=agent_id
            )
            
            # Store created agent
            self.created_agents[composite_agent.agent_id] = composite_agent
            self.creation_stats["composite_agents_created"] += 1
            self.creation_stats["total_agents_created"] += 1
            
            self.logger.info(f"Successfully created composite agent: {composite_agent.agent_id}")
            return composite_agent
            
        except Exception as e:
            self.logger.error(f"Error composing multi-template agent: {str(e)}")
            return None
    
    async def create_custom_agent_from_scratch(self, 
                                             requirements: CustomRequirements,
                                             agent_id: Optional[str] = None) -> Optional[CustomAgent]:
        """
        Tạo custom agent từ scratch theo requirements.
        
        Args:
            requirements: CustomRequirements object
            agent_id: Optional agent ID
            
        Returns:
            CustomAgent instance hoặc None nếu failed
        """
        try:
            self.logger.info(f"Creating custom agent: {requirements.name}")
            
            # Validate requirements
            if not requirements.required_capabilities:
                self.logger.error("No required capabilities specified")
                return None
            
            if not requirements.domain_expertise:
                self.logger.error("No domain expertise specified")
                return None
            
            # Create custom agent
            custom_agent = CustomAgent(requirements=requirements, agent_id=agent_id)
            
            # Store created agent
            self.created_agents[custom_agent.agent_id] = custom_agent
            self.creation_stats["custom_agents_created"] += 1
            self.creation_stats["total_agents_created"] += 1
            
            self.logger.info(f"Successfully created custom agent: {custom_agent.agent_id}")
            return custom_agent
            
        except Exception as e:
            self.logger.error(f"Error creating custom agent: {str(e)}")
            return None
    
    async def optimize_agent_configuration(self, 
                                         agent: Union[CompositeAgent, CustomAgent],
                                         performance_data: Dict[str, Any]) -> Union[CompositeAgent, CustomAgent]:
        """
        Optimize agent configuration dựa trên performance data.
        
        Args:
            agent: Agent cần optimize
            performance_data: Performance metrics và feedback
            
        Returns:
            Optimized agent instance
        """
        try:
            self.logger.info(f"Optimizing agent configuration: {agent.agent_id}")
            
            # Analyze performance data
            efficiency = performance_data.get("efficiency", 50)
            quality = performance_data.get("quality", 50)
            user_satisfaction = performance_data.get("user_satisfaction", 50)
            
            # Optimization strategies
            if isinstance(agent, CompositeAgent):
                # Optimize composite agent
                if efficiency < 70:
                    # Remove underperforming templates
                    self._optimize_composite_templates(agent, performance_data)
                
                if quality < 70:
                    # Adjust capability priorities
                    self._optimize_composite_capabilities(agent, performance_data)
            
            elif isinstance(agent, CustomAgent):
                # Optimize custom agent
                if efficiency < 70:
                    # Adjust complexity level
                    agent.requirements.complexity_level = self._adjust_complexity_level(
                        agent.requirements.complexity_level, performance_data
                    )
                
                if quality < 70:
                    # Add missing capabilities
                    self._optimize_custom_capabilities(agent, performance_data)
            
            self.logger.info(f"Agent optimization completed: {agent.agent_id}")
            return agent
            
        except Exception as e:
            self.logger.error(f"Error optimizing agent configuration: {str(e)}")
            return agent
    
    def _optimize_composite_templates(self, agent: CompositeAgent, performance_data: Dict[str, Any]) -> None:
        """Optimize composite agent templates"""
        # Implementation for template optimization
        pass
    
    def _optimize_composite_capabilities(self, agent: CompositeAgent, performance_data: Dict[str, Any]) -> None:
        """Optimize composite agent capabilities"""
        # Implementation for capability optimization
        pass
    
    def _adjust_complexity_level(self, current_level: str, performance_data: Dict[str, Any]) -> str:
        """Adjust complexity level based on performance"""
        efficiency = performance_data.get("efficiency", 50)
        
        if efficiency < 50:
            # Reduce complexity
            complexity_map = {
                "very_high": "high",
                "high": "medium", 
                "medium": "low",
                "low": "low"
            }
            return complexity_map.get(current_level, current_level)
        elif efficiency > 80:
            # Increase complexity
            complexity_map = {
                "low": "medium",
                "medium": "high",
                "high": "very_high",
                "very_high": "very_high"
            }
            return complexity_map.get(current_level, current_level)
        
        return current_level
    
    def _optimize_custom_capabilities(self, agent: CustomAgent, performance_data: Dict[str, Any]) -> None:
        """Optimize custom agent capabilities"""
        # Implementation for custom capability optimization
        pass
    
    def get_created_agents(self) -> Dict[str, Union[CompositeAgent, CustomAgent]]:
        """Trả về tất cả created agents"""
        return self.created_agents.copy()
    
    def get_agent_by_id(self, agent_id: str) -> Optional[Union[CompositeAgent, CustomAgent]]:
        """Trả về agent theo ID"""
        return self.created_agents.get(agent_id)
    
    def get_creation_stats(self) -> Dict[str, Any]:
        """Trả về creation statistics"""
        return self.creation_stats.copy()
    
    async def validate_agent_effectiveness(self, 
                                         agent: Union[CompositeAgent, CustomAgent],
                                         test_tensions: List[Tension]) -> Dict[str, Any]:
        """
        Validate agent effectiveness với test tensions.
        
        Args:
            agent: Agent cần validate
            test_tensions: List tensions để test
            
        Returns:
            Validation results
        """
        try:
            results = {
                "agent_id": agent.agent_id,
                "total_tensions_tested": len(test_tensions),
                "can_handle_count": 0,
                "average_confidence": 0.0,
                "solutions_generated": 0,
                "validation_score": 0.0
            }
            
            total_confidence = 0.0
            total_solutions = 0
            
            for tension in test_tensions:
                # Test if agent can handle tension
                can_handle = await agent.can_handle_tension(tension)
                if can_handle:
                    results["can_handle_count"] += 1
                    
                    # Generate solutions và count
                    solutions = await agent.generate_specialized_solutions(tension)
                    total_solutions += len(solutions)
                    
                    # Calculate average confidence from solutions
                    if solutions:
                        confidence_sum = sum(s.get("confidence_score", 0) for s in solutions)
                        total_confidence += confidence_sum / len(solutions)
            
            # Calculate metrics
            if results["can_handle_count"] > 0:
                results["average_confidence"] = total_confidence / results["can_handle_count"]
                results["solutions_generated"] = total_solutions
                
                # Calculate overall validation score
                handle_rate = results["can_handle_count"] / len(test_tensions)
                confidence_rate = results["average_confidence"] / 100.0
                solution_rate = min(total_solutions / len(test_tensions), 1.0)
                
                results["validation_score"] = (handle_rate * 0.4 + confidence_rate * 0.3 + solution_rate * 0.3) * 100
            
            self.logger.info(f"Validation completed for agent {agent.agent_id}: score {results['validation_score']:.1f}")
            return results
            
        except Exception as e:
            self.logger.error(f"Error validating agent effectiveness: {str(e)}")
            return {"error": str(e)} 