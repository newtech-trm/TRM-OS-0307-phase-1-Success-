"""
Agent Template Registry

Central registry để quản lý, khởi tạo và orchestrate tất cả agent templates
trong TRM-OS Genesis Engine. Registry cung cấp factory pattern để tạo agents
dựa trên tension requirements và template matching.
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional, Type, Tuple
from datetime import datetime
from abc import ABC

from .base_template import BaseAgentTemplate, AgentTemplateMetadata
from .data_analyst_template import DataAnalystAgent
from .code_generator_template import CodeGeneratorAgent
from .user_interface_template import UserInterfaceAgent
from .integration_template import IntegrationAgent
from .research_template import ResearchAgent
from ..base_agent import AgentMetadata
from ...models.tension import Tension


class TemplateMatchResult:
    """Kết quả matching tension với agent template"""
    
    def __init__(self, template_class: Type[BaseAgentTemplate], confidence: float, 
                 reasoning: str, estimated_effort: int):
        self.template_class = template_class
        self.confidence = confidence
        self.reasoning = reasoning
        self.estimated_effort = estimated_effort
        self.template_name = template_class.__name__
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "template_name": self.template_name,
            "confidence": self.confidence,
            "reasoning": self.reasoning,
            "estimated_effort": self.estimated_effort
        }


class AgentTemplateRegistry:
    """
    Central registry cho tất cả agent templates trong TRM-OS.
    
    Responsibilities:
    - Đăng ký và quản lý agent templates
    - Match tensions với appropriate templates
    - Khởi tạo agent instances từ templates
    - Provide template metadata và capabilities
    - Monitor template performance
    """
    
    def __init__(self):
        self.logger = logging.getLogger("AgentTemplateRegistry")
        self._templates: Dict[str, Type[BaseAgentTemplate]] = {}
        self._template_metadata: Dict[str, AgentTemplateMetadata] = {}
        self._template_instances: Dict[str, BaseAgentTemplate] = {}
        self._performance_stats: Dict[str, Dict[str, Any]] = {}
        
        # Đăng ký tất cả available templates
        self._register_default_templates()
    
    def _register_default_templates(self) -> None:
        """Đăng ký tất cả default agent templates"""
        try:
            # Đăng ký 5 core templates
            self.register_template("DataAnalystAgent", DataAnalystAgent)
            self.register_template("CodeGeneratorAgent", CodeGeneratorAgent)
            self.register_template("UserInterfaceAgent", UserInterfaceAgent)
            self.register_template("IntegrationAgent", IntegrationAgent)
            self.register_template("ResearchAgent", ResearchAgent)
            
            self.logger.info(f"Registered {len(self._templates)} default agent templates")
            
        except Exception as e:
            self.logger.error(f"Error registering default templates: {str(e)}")
    
    def register_template(self, name: str, template_class: Type[BaseAgentTemplate]) -> None:
        """Đăng ký một agent template mới"""
        try:
            if not issubclass(template_class, BaseAgentTemplate):
                raise ValueError(f"Template {name} must inherit from BaseAgentTemplate")
            
            self._templates[name] = template_class
            
            # Tạo temporary instance để lấy metadata
            temp_instance = template_class()
            self._template_metadata[name] = temp_instance.template_metadata
            
            # Khởi tạo performance stats
            self._performance_stats[name] = {
                "instances_created": 0,
                "tensions_processed": 0,
                "success_rate": 0.0,
                "average_confidence": 0.0,
                "last_used": None
            }
            
            self.logger.info(f"Registered template: {name}")
            
        except Exception as e:
            self.logger.error(f"Error registering template {name}: {str(e)}")
    
    def unregister_template(self, name: str) -> None:
        """Hủy đăng ký một agent template"""
        if name in self._templates:
            del self._templates[name]
            del self._template_metadata[name]
            del self._performance_stats[name]
            self.logger.info(f"Unregistered template: {name}")
    
    def get_available_templates(self) -> List[str]:
        """Trả về list tên của tất cả available templates"""
        return list(self._templates.keys())
    
    def get_template_metadata(self, template_name: str) -> Optional[AgentTemplateMetadata]:
        """Trả về metadata của một template"""
        return self._template_metadata.get(template_name)
    
    def get_all_template_metadata(self) -> Dict[str, AgentTemplateMetadata]:
        """Trả về metadata của tất cả templates"""
        return self._template_metadata.copy()
    
    async def match_tension_to_templates(self, tension: Tension, 
                                       top_k: int = 3) -> List[TemplateMatchResult]:
        """
        Match một tension với các agent templates phù hợp nhất.
        
        Args:
            tension: Tension cần match
            top_k: Số lượng top matches trả về
            
        Returns:
            List các TemplateMatchResult được sắp xếp theo confidence
        """
        matches = []
        
        try:
            for template_name, template_class in self._templates.items():
                # Tạo temporary instance để test matching
                temp_instance = template_class()
                
                # Kiểm tra xem template có thể handle tension không
                can_handle = await temp_instance.can_handle_tension(tension)
                
                if can_handle:
                    # Phân tích requirements để tính confidence
                    requirements = await temp_instance.analyze_tension_requirements(tension)
                    
                    # Tính confidence score dựa trên multiple factors
                    confidence = await self._calculate_confidence_score(
                        tension, template_class, requirements
                    )
                    
                    # Tạo reasoning explanation
                    reasoning = await self._generate_match_reasoning(
                        tension, template_name, requirements, confidence
                    )
                    
                    estimated_effort = requirements.get("estimated_effort", 120)
                    
                    match_result = TemplateMatchResult(
                        template_class=template_class,
                        confidence=confidence,
                        reasoning=reasoning,
                        estimated_effort=estimated_effort
                    )
                    
                    matches.append(match_result)
            
            # Sắp xếp theo confidence giảm dần
            matches.sort(key=lambda x: x.confidence, reverse=True)
            
            # Trả về top K matches
            top_matches = matches[:top_k]
            
            self.logger.info(f"Found {len(top_matches)} template matches for tension {tension.uid}")
            
            return top_matches
            
        except Exception as e:
            self.logger.error(f"Error matching tension to templates: {str(e)}")
            return []
    
    async def _calculate_confidence_score(self, tension: Tension, 
                                        template_class: Type[BaseAgentTemplate],
                                        requirements: Dict[str, Any]) -> float:
        """Tính confidence score cho template match"""
        try:
            confidence = 50.0  # Base confidence
            
            # Factor 1: Template domain alignment
            template_name = template_class.__name__
            description = tension.description.lower()
            title = tension.title.lower()
            
            domain_keywords = {
                "DataAnalystAgent": ["data", "analytics", "report", "metrics", "dashboard"],
                "CodeGeneratorAgent": ["code", "development", "api", "bug", "automation"],
                "UserInterfaceAgent": ["ui", "ux", "interface", "design", "frontend"],
                "IntegrationAgent": ["integration", "api", "sync", "connect", "workflow"],
                "ResearchAgent": ["research", "analysis", "study", "market", "trend"]
            }
            
            if template_name in domain_keywords:
                keyword_matches = sum(1 for keyword in domain_keywords[template_name] 
                                    if keyword in description or keyword in title)
                confidence += keyword_matches * 10  # +10 per keyword match
            
            # Factor 2: Complexity alignment
            complexity = requirements.get("complexity", "medium")
            if complexity == "high":
                confidence += 15
            elif complexity == "medium":
                confidence += 10
            else:
                confidence += 5
            
            # Factor 3: Urgency consideration
            urgency = requirements.get("urgency", "normal")
            if urgency == "high":
                confidence += 10
            
            # Factor 4: Template performance history
            template_stats = self._performance_stats.get(template_name, {})
            success_rate = template_stats.get("success_rate", 0.0)
            confidence += success_rate * 0.2  # Performance bonus
            
            # Factor 5: Deliverables alignment
            deliverables = requirements.get("deliverables", [])
            if deliverables:
                confidence += len(deliverables) * 2
            
            # Normalize to 0-100 range
            confidence = min(100.0, max(0.0, confidence))
            
            return round(confidence, 1)
            
        except Exception as e:
            self.logger.error(f"Error calculating confidence score: {str(e)}")
            return 50.0
    
    async def _generate_match_reasoning(self, tension: Tension, template_name: str,
                                      requirements: Dict[str, Any], confidence: float) -> str:
        """Tạo reasoning explanation cho template match"""
        try:
            reasoning_parts = []
            
            # Domain alignment
            domain = self._template_metadata[template_name].primary_domain
            reasoning_parts.append(f"Template specializes in {domain} domain")
            
            # Requirements match
            req_type = requirements.get("development_type") or requirements.get("analysis_type") or \
                      requirements.get("design_type") or requirements.get("integration_type") or \
                      requirements.get("research_type", "general")
            
            if req_type != "unknown":
                reasoning_parts.append(f"Matches {req_type} requirements")
            
            # Complexity handling
            complexity = requirements.get("complexity", "medium")
            reasoning_parts.append(f"Can handle {complexity} complexity tasks")
            
            # Confidence level
            if confidence >= 80:
                reasoning_parts.append("High confidence match")
            elif confidence >= 60:
                reasoning_parts.append("Good confidence match")
            else:
                reasoning_parts.append("Moderate confidence match")
            
            return ". ".join(reasoning_parts)
            
        except Exception as e:
            self.logger.error(f"Error generating match reasoning: {str(e)}")
            return "Template can handle this type of tension"
    
    async def create_agent_from_template(self, template_name: str, 
                                       agent_id: Optional[str] = None,
                                       custom_metadata: Optional[AgentMetadata] = None) -> Optional[BaseAgentTemplate]:
        """
        Tạo agent instance từ template.
        
        Args:
            template_name: Tên template
            agent_id: ID cho agent (optional)
            custom_metadata: Custom metadata (optional)
            
        Returns:
            Agent instance hoặc None nếu failed
        """
        try:
            if template_name not in self._templates:
                self.logger.error(f"Template {template_name} not found")
                return None
            
            template_class = self._templates[template_name]
            
            # Tạo agent instance without metadata parameter
            agent = template_class(agent_id=agent_id)
            
            # Khởi tạo agent
            await agent.initialize()
            
            # Lưu instance reference
            instance_id = agent.agent_id or f"{template_name}_{datetime.now().timestamp()}"
            self._template_instances[instance_id] = agent
            
            # Cập nhật performance stats
            self._performance_stats[template_name]["instances_created"] += 1
            self._performance_stats[template_name]["last_used"] = datetime.now().isoformat()
            
            self.logger.info(f"Created agent {instance_id} from template {template_name}")
            
            return agent
            
        except Exception as e:
            self.logger.error(f"Error creating agent from template {template_name}: {str(e)}")
            return None
    
    async def create_best_match_agent(self, tension: Tension) -> Optional[Tuple[BaseAgentTemplate, TemplateMatchResult]]:
        """
        Tạo agent từ template phù hợp nhất với tension.
        
        Args:
            tension: Tension cần xử lý
            
        Returns:
            Tuple (agent_instance, match_result) hoặc None nếu không match
        """
        try:
            # Tìm best matching template
            matches = await self.match_tension_to_templates(tension, top_k=1)
            
            if not matches:
                self.logger.warning(f"No template matches found for tension {tension.uid}")
                return None
            
            best_match = matches[0]
            template_name = best_match.template_name
            
            # Tạo agent từ best matching template
            agent = await self.create_agent_from_template(template_name)
            
            if agent:
                self.logger.info(f"Created best match agent {template_name} for tension {tension.uid}")
                return (agent, best_match)
            else:
                return None
                
        except Exception as e:
            self.logger.error(f"Error creating best match agent: {str(e)}")
            return None
    
    def get_active_agents(self) -> Dict[str, BaseAgentTemplate]:
        """Trả về tất cả active agent instances"""
        return self._template_instances.copy()
    
    def get_agent_by_id(self, agent_id: str) -> Optional[BaseAgentTemplate]:
        """Trả về agent instance theo ID"""
        return self._template_instances.get(agent_id)
    
    async def stop_agent(self, agent_id: str) -> bool:
        """Dừng và remove agent instance"""
        try:
            if agent_id in self._template_instances:
                agent = self._template_instances[agent_id]
                await agent.stop()
                del self._template_instances[agent_id]
                
                self.logger.info(f"Stopped agent {agent_id}")
                return True
            else:
                self.logger.warning(f"Agent {agent_id} not found")
                return False
                
        except Exception as e:
            self.logger.error(f"Error stopping agent {agent_id}: {str(e)}")
            return False
    
    async def stop_all_agents(self) -> None:
        """Dừng tất cả active agents"""
        try:
            agent_ids = list(self._template_instances.keys())
            for agent_id in agent_ids:
                await self.stop_agent(agent_id)
                
            self.logger.info("Stopped all active agents")
            
        except Exception as e:
            self.logger.error(f"Error stopping all agents: {str(e)}")
    
    def get_template_performance_stats(self) -> Dict[str, Dict[str, Any]]:
        """Trả về performance statistics của tất cả templates"""
        return self._performance_stats.copy()
    
    def update_template_performance(self, template_name: str, 
                                  success: bool, confidence: float) -> None:
        """Cập nhật performance stats cho template"""
        try:
            if template_name in self._performance_stats:
                stats = self._performance_stats[template_name]
                
                stats["tensions_processed"] += 1
                
                # Update success rate
                total_processed = stats["tensions_processed"]
                current_successes = stats["success_rate"] * (total_processed - 1) / 100
                new_successes = current_successes + (1 if success else 0)
                stats["success_rate"] = (new_successes / total_processed) * 100
                
                # Update average confidence
                current_avg = stats["average_confidence"]
                stats["average_confidence"] = ((current_avg * (total_processed - 1)) + confidence) / total_processed
                
        except Exception as e:
            self.logger.error(f"Error updating template performance: {str(e)}")
    
    def get_registry_summary(self) -> Dict[str, Any]:
        """Trả về summary của registry state"""
        return {
            "total_templates": len(self._templates),
            "available_templates": list(self._templates.keys()),
            "active_agents": len(self._template_instances),
            "performance_stats": self._performance_stats,
            "registry_health": "healthy" if self._templates else "no_templates"
        }
    
    async def health_check(self) -> Dict[str, Any]:
        """Thực hiện health check cho registry và templates"""
        health_status = {
            "registry_status": "healthy",
            "template_count": len(self._templates),
            "active_agent_count": len(self._template_instances),
            "template_health": {},
            "issues": []
        }
        
        try:
            # Check each template
            for template_name, template_class in self._templates.items():
                try:
                    # Test template instantiation
                    temp_instance = template_class()
                    template_info = temp_instance.get_template_info()
                    
                    health_status["template_health"][template_name] = {
                        "status": "healthy",
                        "capabilities": len(template_info.get("capabilities", [])),
                        "performance": self._performance_stats.get(template_name, {})
                    }
                    
                except Exception as e:
                    health_status["template_health"][template_name] = {
                        "status": "unhealthy",
                        "error": str(e)
                    }
                    health_status["issues"].append(f"Template {template_name}: {str(e)}")
            
            # Overall health assessment
            unhealthy_templates = [name for name, health in health_status["template_health"].items() 
                                 if health["status"] == "unhealthy"]
            
            if unhealthy_templates:
                health_status["registry_status"] = "degraded"
                health_status["issues"].append(f"Unhealthy templates: {unhealthy_templates}")
            
            if not self._templates:
                health_status["registry_status"] = "critical"
                health_status["issues"].append("No templates registered")
            
        except Exception as e:
            health_status["registry_status"] = "error"
            health_status["issues"].append(f"Health check error: {str(e)}")
        
        return health_status


# Global registry instance
agent_template_registry = AgentTemplateRegistry() 