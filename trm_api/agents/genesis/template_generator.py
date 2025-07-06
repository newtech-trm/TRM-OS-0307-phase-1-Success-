"""
Template Generator

Advanced component của Genesis Engine để phân tích successful agent patterns
và generate new agent templates từ những patterns đó.
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional, Type, Union
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import uuid

from ..templates.base_template import BaseAgentTemplate, AgentTemplateMetadata, AgentCapability
from .advanced_creator import CompositeAgent, CustomAgent
from ...models.tension import Tension
from ...models.enums import TensionType, Priority


class AgentPattern:
    """Pattern được phân tích từ successful agents"""
    
    def __init__(self,
                 pattern_id: str,
                 name: str,
                 description: str,
                 capabilities: List[str],
                 domain_expertise: List[str],
                 success_metrics: Dict[str, float],
                 usage_frequency: int,
                 effectiveness_score: float):
        self.pattern_id = pattern_id
        self.name = name
        self.description = description
        self.capabilities = capabilities
        self.domain_expertise = domain_expertise
        self.success_metrics = success_metrics
        self.usage_frequency = usage_frequency
        self.effectiveness_score = effectiveness_score
        self.created_at = datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "pattern_id": self.pattern_id,
            "name": self.name,
            "description": self.description,
            "capabilities": self.capabilities,
            "domain_expertise": self.domain_expertise,
            "success_metrics": self.success_metrics,
            "usage_frequency": self.usage_frequency,
            "effectiveness_score": self.effectiveness_score,
            "created_at": self.created_at.isoformat()
        }


class GeneratedTemplate(BaseAgentTemplate):
    """Template được generate từ successful patterns"""
    
    def __init__(self, 
                 pattern: AgentPattern,
                 template_name: str,
                 agent_id: Optional[str] = None):
        # Set attributes first before calling super().__init__()
        self.source_pattern = pattern
        self.template_name = template_name
        
        super().__init__(agent_id or f"generated_{uuid.uuid4().hex[:8]}")
        
        # Setup capabilities từ pattern
        self._setup_pattern_capabilities()
        
        # Setup metadata từ pattern
        self._setup_pattern_metadata()
    
    def _setup_pattern_capabilities(self) -> None:
        """Setup capabilities từ pattern data"""
        self.capabilities = []
        
        for cap_name in self.source_pattern.capabilities:
            # Estimate proficiency từ success metrics
            proficiency = min(95, int(self.source_pattern.effectiveness_score))
            
            capability = AgentCapability(
                name=cap_name,
                description=f"Generated capability: {cap_name}",
                proficiency_level=proficiency,
                tools_required=[],
                estimated_time_per_task=self._estimate_task_time(cap_name)
            )
            self.capabilities.append(capability)
    
    def _estimate_task_time(self, capability_name: str) -> int:
        """Estimate task time cho capability"""
        # Base time mapping
        time_mapping = {
            "data_analysis": 90,
            "code_generation": 120,
            "ui_design": 150,
            "integration": 180,
            "research": 60,
            "automation": 75,
            "testing": 45,
            "documentation": 30
        }
        
        # Find closest match
        for key, time in time_mapping.items():
            if key in capability_name.lower():
                return time
        
        return 90  # Default time
    
    def _setup_pattern_metadata(self) -> None:
        """Setup metadata từ pattern"""
        # Map domains to tension types
        supported_types = []
        for domain in self.source_pattern.domain_expertise:
            if "data" in domain.lower():
                supported_types.append(TensionType.RESOURCE_CONSTRAINT)
            elif "code" in domain.lower() or "development" in domain.lower():
                supported_types.append(TensionType.PROCESS_IMPROVEMENT)
            elif "ui" in domain.lower() or "interface" in domain.lower():
                supported_types.append(TensionType.COMMUNICATION_BREAKDOWN)
            else:
                supported_types.append(TensionType.STRATEGIC_MISALIGNMENT)
        
        # Remove duplicates
        supported_types = list(set(supported_types))
        
        self.template_metadata = AgentTemplateMetadata(
            template_name=self.template_name,
            template_version="1.0.0",
            description=self.source_pattern.description,
            primary_domain=self.source_pattern.domain_expertise[0] if self.source_pattern.domain_expertise else "general",
            capabilities=self.capabilities,
            recommended_tensions=["pattern_based", "proven"],
            dependencies=[],
            performance_metrics=["efficiency", "quality", "pattern_match"]
        )
    
    def _determine_complexity_level(self) -> str:
        """Determine complexity level từ pattern metrics"""
        num_capabilities = len(self.source_pattern.capabilities)
        effectiveness = self.source_pattern.effectiveness_score
        
        if num_capabilities >= 6 and effectiveness >= 90:
            return "very_high"
        elif num_capabilities >= 4 and effectiveness >= 80:
            return "high"
        elif num_capabilities >= 2 and effectiveness >= 70:
            return "medium"
        else:
            return "low"
    
    def _estimate_resolution_time(self) -> int:
        """Estimate resolution time từ capabilities"""
        total_time = sum(cap.estimated_time_per_task or 90 for cap in self.capabilities)
        # Average time per capability
        return int(total_time / max(1, len(self.capabilities)))
    
    async def can_handle_tension(self, tension: Tension) -> bool:
        """Check if generated template có thể handle tension"""
        description_lower = tension.description.lower()
        title_lower = tension.title.lower()
        
        # Check domain expertise match
        for domain in self.source_pattern.domain_expertise:
            if domain.lower() in description_lower or domain.lower() in title_lower:
                return True
        
        # Check capability match
        for capability in self.source_pattern.capabilities:
            if capability.lower() in description_lower or capability.lower() in title_lower:
                return True
        
        return False
    
    async def analyze_tension_requirements(self, tension: Tension) -> Dict[str, Any]:
        """Analyze tension requirements"""
        return {
            "pattern_based": True,
            "source_pattern": self.source_pattern.pattern_id,
            "domain_match": self.source_pattern.domain_expertise,
            "capability_match": self.source_pattern.capabilities,
            "effectiveness_score": self.source_pattern.effectiveness_score,
            "estimated_effort": self.template_metadata.estimated_resolution_time
        }
    
    async def generate_specialized_solutions(self, tension: Tension) -> List[Dict[str, Any]]:
        """Generate solutions based on pattern"""
        solutions = []
        
        # Generate solutions cho each relevant capability
        for capability in self.capabilities:
            if await self._is_capability_relevant(capability, tension):
                solution = {
                    "title": f"Pattern-based Solution using {capability.name}",
                    "description": f"Apply {capability.name} pattern to resolve {tension.title}",
                    "approach": "pattern_based",
                    "source_pattern": self.source_pattern.pattern_id,
                    "required_capabilities": [capability.name],
                    "estimated_effort": capability.estimated_time_per_task,
                    "confidence_score": min(95, int(self.source_pattern.effectiveness_score)),
                    "implementation_steps": self._generate_implementation_steps(capability, tension)
                }
                solutions.append(solution)
        
        return solutions
    
    async def _is_capability_relevant(self, capability: AgentCapability, tension: Tension) -> bool:
        """Check if capability is relevant cho tension"""
        description_lower = tension.description.lower()
        title_lower = tension.title.lower()
        capability_lower = capability.name.lower()
        
        return capability_lower in description_lower or capability_lower in title_lower
    
    def _generate_implementation_steps(self, capability: AgentCapability, tension: Tension) -> List[str]:
        """Generate implementation steps cho capability"""
        steps = [
            f"Analyze {tension.title} using {capability.name} approach",
            f"Apply pattern-based methodology from {self.source_pattern.name}",
            f"Implement solution using proven techniques",
            f"Validate results against success metrics",
            f"Optimize based on effectiveness feedback"
        ]
        return steps
    
    async def execute_solution(self, solution: Dict[str, Any], tension: Tension) -> Dict[str, Any]:
        """Execute pattern-based solution"""
        return {
            "status": "completed",
            "agent_id": self.agent_id,
            "solution_type": "pattern_based",
            "source_pattern": self.source_pattern.pattern_id,
            "execution_time": solution.get("estimated_effort", 90),
            "results": {
                "approach_used": solution.get("approach", "pattern_based"),
                "capabilities_applied": solution.get("required_capabilities", []),
                "pattern_effectiveness": self.source_pattern.effectiveness_score,
                "implementation_notes": f"Pattern-based solution executed for {tension.title}"
            },
            "performance_metrics": {
                "efficiency": min(95, int(self.source_pattern.effectiveness_score)),
                "quality": min(90, int(self.source_pattern.effectiveness_score * 0.9)),
                "innovation": 75  # Pattern-based có innovation trung bình
            }
        }

    def _get_default_template_metadata(self) -> AgentTemplateMetadata:
        """Get default template metadata for generated template"""
        # Get template_name if available, otherwise use pattern name
        template_name = getattr(self, 'template_name', None) or self.source_pattern.name
        
        return AgentTemplateMetadata(
            template_name=template_name,
            template_version="1.0.0",
            description=self.source_pattern.description,
            primary_domain=self.source_pattern.domain_expertise[0] if self.source_pattern.domain_expertise else "general",
            capabilities=self.capabilities if hasattr(self, 'capabilities') and self.capabilities else [],
            recommended_tensions=["pattern_based", "proven"],
            dependencies=[],
            performance_metrics=["efficiency", "quality", "pattern_match"]
        )

    async def _register_specialized_handlers(self) -> None:
        """Register specialized event handlers for generated template"""
        # Generated templates handle pattern-based events
        pass

    async def _initialize_specialized_components(self) -> None:
        """Initialize specialized components for generated template"""
        # Initialize pattern-based components
        pass

    async def _handle_specialized_event(self, event) -> None:
        """Handle specialized events for generated template"""
        # Handle pattern-based events
        pass


class ValidationResult:
    """Kết quả validation cho generated template"""
    
    def __init__(self,
                 template_name: str,
                 is_valid: bool,
                 validation_score: float,
                 strengths: List[str],
                 weaknesses: List[str],
                 recommendations: List[str]):
        self.template_name = template_name
        self.is_valid = is_valid
        self.validation_score = validation_score
        self.strengths = strengths
        self.weaknesses = weaknesses
        self.recommendations = recommendations
        self.validated_at = datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "template_name": self.template_name,
            "is_valid": self.is_valid,
            "validation_score": self.validation_score,
            "strengths": self.strengths,
            "weaknesses": self.weaknesses,
            "recommendations": self.recommendations,
            "validated_at": self.validated_at.isoformat()
        }


class TemplateGenerator:
    """
    Template Generator cho TRM-OS Genesis Engine.
    
    Capabilities:
    - Analyze successful agent patterns từ historical data
    - Generate new templates từ identified patterns
    - Validate template effectiveness
    - Optimize template configurations
    """
    
    def __init__(self):
        self.logger = logging.getLogger("TemplateGenerator")
        self.identified_patterns: Dict[str, AgentPattern] = {}
        self.generated_templates: Dict[str, GeneratedTemplate] = {}
        self.validation_results: Dict[str, ValidationResult] = {}
        self.generation_stats = {
            "patterns_analyzed": 0,
            "templates_generated": 0,
            "successful_validations": 0,
            "total_effectiveness_score": 0.0
        }
    
    async def analyze_successful_agent_patterns(self, 
                                              agents: List[Union[CompositeAgent, CustomAgent, BaseAgentTemplate]],
                                              performance_history: Optional[Dict[str, Any]] = None) -> List[AgentPattern]:
        """
        Analyze successful agent patterns từ agent performance data.
        
        Args:
            agents: List agents để analyze
            performance_history: Optional performance history data
            
        Returns:
            List identified patterns
        """
        try:
            self.logger.info(f"Analyzing patterns from {len(agents)} agents")
            
            patterns = []
            
            # Group agents by similar characteristics
            agent_groups = self._group_agents_by_similarity(agents)
            
            for group_key, group_agents in agent_groups.items():
                if len(group_agents) >= 2:  # Need at least 2 agents để form pattern
                    pattern = await self._extract_pattern_from_group(group_agents, performance_history)
                    if pattern and pattern.effectiveness_score >= 70:  # Only successful patterns
                        patterns.append(pattern)
                        self.identified_patterns[pattern.pattern_id] = pattern
            
            self.generation_stats["patterns_analyzed"] += len(patterns)
            
            self.logger.info(f"Identified {len(patterns)} successful patterns")
            return patterns
            
        except Exception as e:
            self.logger.error(f"Error analyzing agent patterns: {str(e)}")
            return []
    
    def _group_agents_by_similarity(self, 
                                   agents: List[Union[CompositeAgent, CustomAgent, BaseAgentTemplate]]) -> Dict[str, List]:
        """Group agents by similar capabilities và domains"""
        groups = defaultdict(list)
        
        for agent in agents:
            # Create group key từ capabilities và domains
            capabilities = [cap.name for cap in agent.capabilities] if hasattr(agent, 'capabilities') else []
            domains = getattr(agent.template_metadata, 'domain_expertise', []) if hasattr(agent, 'template_metadata') else []
            
            # Sort để ensure consistent grouping
            capabilities.sort()
            domains.sort()
            
            group_key = f"{','.join(capabilities[:3])}|{','.join(domains[:2])}"  # Limit key length
            groups[group_key].append(agent)
        
        return groups
    
    async def _extract_pattern_from_group(self, 
                                        group_agents: List[Union[CompositeAgent, CustomAgent, BaseAgentTemplate]],
                                        performance_history: Optional[Dict[str, Any]]) -> Optional[AgentPattern]:
        """Extract pattern từ group of similar agents"""
        try:
            # Collect common capabilities
            capability_counter = Counter()
            domain_counter = Counter()
            
            for agent in group_agents:
                # Count capabilities
                if hasattr(agent, 'capabilities'):
                    for cap in agent.capabilities:
                        capability_counter[cap.name] += 1
                
                # Count domains
                if hasattr(agent, 'template_metadata') and agent.template_metadata:
                    for domain in agent.template_metadata.domain_expertise:
                        domain_counter[domain] += 1
            
            # Get most common capabilities và domains
            common_capabilities = [cap for cap, count in capability_counter.most_common(5)]
            common_domains = [domain for domain, count in domain_counter.most_common(3)]
            
            if not common_capabilities:
                return None
            
            # Calculate pattern metrics
            effectiveness_score = self._calculate_pattern_effectiveness(group_agents, performance_history)
            usage_frequency = len(group_agents)
            
            # Generate pattern name
            pattern_name = f"Pattern_{common_capabilities[0]}_{common_domains[0] if common_domains else 'General'}"
            pattern_id = f"pattern_{uuid.uuid4().hex[:8]}"
            
            # Create success metrics
            success_metrics = {
                "agent_count": len(group_agents),
                "capability_coverage": len(common_capabilities),
                "domain_coverage": len(common_domains),
                "effectiveness": effectiveness_score
            }
            
            pattern = AgentPattern(
                pattern_id=pattern_id,
                name=pattern_name,
                description=f"Successful pattern with {', '.join(common_capabilities[:2])} capabilities in {', '.join(common_domains[:2])} domains",
                capabilities=common_capabilities,
                domain_expertise=common_domains,
                success_metrics=success_metrics,
                usage_frequency=usage_frequency,
                effectiveness_score=effectiveness_score
            )
            
            return pattern
            
        except Exception as e:
            self.logger.error(f"Error extracting pattern from group: {str(e)}")
            return None
    
    def _calculate_pattern_effectiveness(self, 
                                       group_agents: List[Union[CompositeAgent, CustomAgent, BaseAgentTemplate]],
                                       performance_history: Optional[Dict[str, Any]]) -> float:
        """Calculate effectiveness score cho pattern"""
        try:
            if not performance_history:
                # Default scoring based on agent characteristics
                base_score = 75.0
                
                # Bonus cho composite agents (more sophisticated)
                composite_bonus = sum(5 for agent in group_agents if isinstance(agent, CompositeAgent))
                
                # Bonus cho custom agents (specialized)
                custom_bonus = sum(3 for agent in group_agents if isinstance(agent, CustomAgent))
                
                # Capability diversity bonus
                all_capabilities = set()
                for agent in group_agents:
                    if hasattr(agent, 'capabilities'):
                        all_capabilities.update(cap.name for cap in agent.capabilities)
                
                diversity_bonus = min(15, len(all_capabilities) * 2)
                
                total_score = base_score + composite_bonus + custom_bonus + diversity_bonus
                return min(95.0, total_score)
            
            else:
                # Calculate từ actual performance history
                agent_scores = []
                for agent in group_agents:
                    agent_id = getattr(agent, 'agent_id', str(id(agent)))
                    agent_performance = performance_history.get(agent_id, {})
                    
                    efficiency = agent_performance.get("efficiency", 75)
                    quality = agent_performance.get("quality", 75)
                    satisfaction = agent_performance.get("user_satisfaction", 75)
                    
                    agent_score = (efficiency * 0.4 + quality * 0.4 + satisfaction * 0.2)
                    agent_scores.append(agent_score)
                
                return sum(agent_scores) / len(agent_scores) if agent_scores else 75.0
            
        except Exception as e:
            self.logger.error(f"Error calculating pattern effectiveness: {str(e)}")
            return 75.0
    
    async def generate_new_template_from_pattern(self, 
                                               pattern: AgentPattern,
                                               template_name: Optional[str] = None) -> Optional[GeneratedTemplate]:
        """
        Generate new template từ identified pattern.
        
        Args:
            pattern: AgentPattern để generate từ
            template_name: Optional custom template name
            
        Returns:
            GeneratedTemplate instance hoặc None nếu failed
        """
        try:
            if not template_name:
                template_name = f"Generated_{pattern.name}_{uuid.uuid4().hex[:6]}"
            
            self.logger.info(f"Generating template: {template_name} from pattern: {pattern.pattern_id}")
            
            # Create generated template
            generated_template = GeneratedTemplate(
                pattern=pattern,
                template_name=template_name
            )
            
            # Store generated template
            self.generated_templates[template_name] = generated_template
            self.generation_stats["templates_generated"] += 1
            self.generation_stats["total_effectiveness_score"] += pattern.effectiveness_score
            
            self.logger.info(f"Successfully generated template: {template_name}")
            return generated_template
            
        except Exception as e:
            self.logger.error(f"Error generating template from pattern: {str(e)}")
            return None
    
    async def validate_template_effectiveness(self, 
                                            template: GeneratedTemplate,
                                            test_tensions: Optional[List[Tension]] = None) -> ValidationResult:
        """
        Validate effectiveness của generated template.
        
        Args:
            template: GeneratedTemplate để validate
            test_tensions: Optional test tensions cho validation
            
        Returns:
            ValidationResult
        """
        try:
            self.logger.info(f"Validating template: {template.template_name}")
            
            strengths = []
            weaknesses = []
            recommendations = []
            validation_score = 0.0
            
            # Validate pattern foundation
            if template.source_pattern.effectiveness_score >= 80:
                strengths.append("Based on highly effective pattern")
                validation_score += 25
            elif template.source_pattern.effectiveness_score >= 70:
                strengths.append("Based on moderately effective pattern")
                validation_score += 15
            else:
                weaknesses.append("Based on low-effectiveness pattern")
                recommendations.append("Consider improving pattern foundation")
            
            # Validate capability coverage
            if len(template.capabilities) >= 4:
                strengths.append("Comprehensive capability coverage")
                validation_score += 20
            elif len(template.capabilities) >= 2:
                strengths.append("Adequate capability coverage")
                validation_score += 10
            else:
                weaknesses.append("Limited capability coverage")
                recommendations.append("Add more specialized capabilities")
            
            # Validate domain expertise
            if len(template.source_pattern.domain_expertise) >= 3:
                strengths.append("Multi-domain expertise")
                validation_score += 15
            elif len(template.source_pattern.domain_expertise) >= 1:
                strengths.append("Focused domain expertise")
                validation_score += 10
            else:
                weaknesses.append("Unclear domain focus")
                recommendations.append("Define clear domain expertise")
            
            # Test với tensions nếu provided
            if test_tensions:
                tension_test_score = await self._test_template_with_tensions(template, test_tensions)
                validation_score += tension_test_score
                
                if tension_test_score >= 30:
                    strengths.append("Excellent tension handling capability")
                elif tension_test_score >= 20:
                    strengths.append("Good tension handling capability")
                else:
                    weaknesses.append("Limited tension handling capability")
                    recommendations.append("Improve tension analysis algorithms")
            else:
                validation_score += 20  # Default score nếu không có test tensions
            
            # Pattern usage frequency validation
            if template.source_pattern.usage_frequency >= 5:
                strengths.append("Based on frequently used pattern")
                validation_score += 10
            elif template.source_pattern.usage_frequency >= 3:
                strengths.append("Based on moderately used pattern")
                validation_score += 5
            else:
                weaknesses.append("Based on rarely used pattern")
                recommendations.append("Validate pattern applicability")
            
            # Final validation
            is_valid = validation_score >= 60 and len(weaknesses) <= 2
            
            if not is_valid:
                recommendations.append("Consider refining template based on identified weaknesses")
            
            result = ValidationResult(
                template_name=template.template_name,
                is_valid=is_valid,
                validation_score=validation_score,
                strengths=strengths,
                weaknesses=weaknesses,
                recommendations=recommendations
            )
            
            # Store validation result
            self.validation_results[template.template_name] = result
            
            if is_valid:
                self.generation_stats["successful_validations"] += 1
            
            self.logger.info(f"Template validation completed: {template.template_name} - Score: {validation_score:.1f}")
            return result
            
        except Exception as e:
            self.logger.error(f"Error validating template effectiveness: {str(e)}")
            return ValidationResult(
                template_name=template.template_name,
                is_valid=False,
                validation_score=0.0,
                strengths=[],
                weaknesses=["Validation failed due to error"],
                recommendations=["Review template implementation"]
            )
    
    async def _test_template_with_tensions(self, 
                                         template: GeneratedTemplate,
                                         test_tensions: List[Tension]) -> float:
        """Test template với set of tensions"""
        try:
            total_score = 0.0
            tests_run = 0
            
            for tension in test_tensions:
                # Test if template can handle tension
                can_handle = await template.can_handle_tension(tension)
                if can_handle:
                    tests_run += 1
                    
                    # Test solution generation
                    solutions = await template.generate_specialized_solutions(tension)
                    if solutions:
                        # Score based on number và quality of solutions
                        solution_score = min(10, len(solutions) * 2)
                        
                        # Bonus cho high confidence solutions
                        high_confidence_solutions = [s for s in solutions if s.get("confidence_score", 0) >= 80]
                        confidence_bonus = len(high_confidence_solutions) * 2
                        
                        total_score += solution_score + confidence_bonus
            
            # Calculate average score
            if tests_run > 0:
                return min(40, total_score / tests_run * 5)  # Scale to max 40 points
            else:
                return 0.0
            
        except Exception as e:
            self.logger.error(f"Error testing template with tensions: {str(e)}")
            return 0.0
    
    def get_identified_patterns(self) -> Dict[str, AgentPattern]:
        """Trả về tất cả identified patterns"""
        return self.identified_patterns.copy()
    
    def get_generated_templates(self) -> Dict[str, GeneratedTemplate]:
        """Trả về tất cả generated templates"""
        return self.generated_templates.copy()
    
    def get_validation_results(self) -> Dict[str, ValidationResult]:
        """Trả về tất cả validation results"""
        return self.validation_results.copy()
    
    def get_generation_stats(self) -> Dict[str, Any]:
        """Trả về generation statistics"""
        stats = self.generation_stats.copy()
        
        # Calculate additional metrics
        if stats["templates_generated"] > 0:
            stats["average_effectiveness"] = stats["total_effectiveness_score"] / stats["templates_generated"]
            stats["validation_success_rate"] = (stats["successful_validations"] / stats["templates_generated"]) * 100
        else:
            stats["average_effectiveness"] = 0.0
            stats["validation_success_rate"] = 0.0
        
        return stats
    
    def get_pattern_by_id(self, pattern_id: str) -> Optional[AgentPattern]:
        """Trả về pattern theo ID"""
        return self.identified_patterns.get(pattern_id)
    
    def get_template_by_name(self, template_name: str) -> Optional[GeneratedTemplate]:
        """Trả về generated template theo name"""
        return self.generated_templates.get(template_name) 