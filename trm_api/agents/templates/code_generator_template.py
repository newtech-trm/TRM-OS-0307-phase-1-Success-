"""
Code Generator Agent Template

Agent chuyên biệt xử lý các tensions liên quan đến coding, development,
automation và technical implementation trong TRM-OS.
"""

import re
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

from .base_template import BaseAgentTemplate, AgentTemplateMetadata, AgentCapability
from ..base_agent import AgentMetadata
from ...eventbus.system_event_bus import EventType, SystemEvent
from ...models.tension import Tension
from ...models.enums import TensionType, Priority


class CodeGeneratorAgent(BaseAgentTemplate):
    """
    Specialized agent template for code generation and development tasks.
    
    Tuân thủ đầy đủ triết lý TRM-OS:
    - Tension-based operation với proper enum handling
    - WIN optimization trong code generation decisions
    - Quantum Operating Model implementation
    - Strategic alignment với software development best practices
    """
    
    def __init__(self, agent_id: Optional[str] = None):
        # Define capabilities trước khi gọi super().__init__()
        capabilities = [
            AgentCapability(
                name="api_development",
                description="Design and implement RESTful APIs and microservices",
                proficiency_level=0.9,
                estimated_time_per_task=120.0,
                related_tension_types=[TensionType.TECHNICAL_DEBT, TensionType.COMMUNICATION_BREAKDOWN, TensionType.PROCESS_IMPROVEMENT]
            ),
            AgentCapability(
                name="database_integration",
                description="Database design, ORM implementation, and data access layers",
                proficiency_level=0.85,
                estimated_time_per_task=90.0,
                related_tension_types=[TensionType.TECHNICAL_DEBT, TensionType.PROCESS_IMPROVEMENT, TensionType.RESOURCE_CONSTRAINT]
            ),
            AgentCapability(
                name="frontend_development",
                description="Modern frontend frameworks and responsive UI development",
                proficiency_level=0.8,
                estimated_time_per_task=150.0,
                related_tension_types=[TensionType.TECHNICAL_DEBT, TensionType.COMMUNICATION_BREAKDOWN, TensionType.PROCESS_IMPROVEMENT]
            ),
            AgentCapability(
                name="testing_automation",
                description="Unit testing, integration testing, and test automation",
                proficiency_level=0.9,
                estimated_time_per_task=60.0,
                related_tension_types=[TensionType.TECHNICAL_DEBT, TensionType.PROCESS_IMPROVEMENT, TensionType.RESOURCE_CONSTRAINT]
            ),
            AgentCapability(
                name="code_optimization",
                description="Performance optimization and code refactoring",
                proficiency_level=0.85,
                estimated_time_per_task=75.0,
                related_tension_types=[TensionType.TECHNICAL_DEBT, TensionType.PROCESS_IMPROVEMENT, TensionType.RESOURCE_CONSTRAINT]
            ),
            AgentCapability(
                name="security_implementation",
                description="Security best practices and vulnerability mitigation",
                proficiency_level=0.8,
                estimated_time_per_task=90.0,
                related_tension_types=[TensionType.TECHNICAL_DEBT, TensionType.PROCESS_IMPROVEMENT, TensionType.RESOURCE_CONSTRAINT]
            )
        ]
        
        # Create metadata với proper template info
        metadata = AgentMetadata(
            name="CodeGeneratorAgent",
            agent_type="template",
            description="Specialized agent for high-quality code generation and software development",
            capabilities=[cap.name for cap in capabilities],
            status="active",
            version="2.0.0"
        )
        
        template_metadata = AgentTemplateMetadata(
            template_name="CodeGeneratorAgent",
            primary_domain="software_development",
            capabilities=capabilities,
            domain_expertise=["python", "javascript", "typescript", "react", "fastapi", "postgresql", "testing"],
            supported_tension_types=[
                TensionType.TECHNICAL_DEBT,
                TensionType.PROCESS_IMPROVEMENT,
                TensionType.RESOURCE_CONSTRAINT,
                TensionType.COMMUNICATION_BREAKDOWN  # API integration issues
            ],
            performance_metrics={
                "code_quality": 0.92,
                "delivery_speed": 0.88,
                "bug_rate": 0.05,
                "maintainability": 0.90
            },
            version="2.0.0",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        super().__init__(agent_id=agent_id, template_metadata=template_metadata)
        
        # Specialized components for code generation
        self.development_tools = {
            "languages": ["python", "javascript", "typescript", "sql"],
            "frameworks": ["fastapi", "react", "nextjs", "express", "django"],
            "databases": ["postgresql", "mongodb", "redis"],
            "testing_frameworks": ["pytest", "jest", "cypress"],
            "deployment_tools": ["docker", "kubernetes", "railway", "vercel"]
        }
        
        self.coding_standards = {
            "python": {
                "style_guide": "PEP8",
                "type_hints": "required",
                "docstrings": "google_style",
                "testing": "pytest_with_coverage"
            },
            "javascript": {
                "style_guide": "ESLint_Airbnb",
                "type_checking": "typescript_preferred",
                "testing": "jest_with_rtl",
                "bundling": "vite_or_webpack"
            }
        }
        
        self.architecture_patterns = {
            "backend": ["microservices", "clean_architecture", "repository_pattern"],
            "frontend": ["component_composition", "state_management", "responsive_design"],
            "database": ["normalization", "indexing_strategy", "migration_management"]
        }
    
    def _get_default_template_metadata(self) -> AgentTemplateMetadata:
        """Return default template metadata for CodeGeneratorAgent"""
        capabilities = [
            AgentCapability(
                name="api_development",
                description="RESTful API development",
                proficiency_level=0.9,
                estimated_time_per_task=120.0
            )
        ]
        
        return AgentTemplateMetadata(
            template_name="CodeGeneratorAgent",
            primary_domain="software_development",
            capabilities=capabilities,
            domain_expertise=["python", "javascript"],
            supported_tension_types=[TensionType.TECHNICAL_DEBT],
            performance_metrics={"code_quality": 0.9},
            version="2.0.0",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
    
    async def can_handle_tension(self, tension: Tension) -> bool:
        """
        Đánh giá khả năng xử lý tension theo triết lý TRM-OS.
        Sử dụng proper enum comparison và WIN optimization.
        """
        try:
            # Kiểm tra tension type với proper enum handling
            if not tension.tensionType:
                self.logger.warning(f"Tension {tension.tensionId} has no tensionType")
                return False
            
            # Code Generator có thể handle các tension types sau
            supported_types = [
                TensionType.TECHNICAL_DEBT,
                TensionType.PROCESS_IMPROVEMENT,  # Automation, optimization
                TensionType.RESOURCE_CONSTRAINT,  # Efficiency improvements
                TensionType.COMMUNICATION_BREAKDOWN  # API integration issues
            ]
            
            # Primary capability check
            if tension.tensionType not in supported_types:
                self.logger.debug(f"Tension type {tension.tensionType} not in supported types")
                return False
            
            # Sử dụng quantum model để assess fit
            can_handle = await super().can_handle_tension(tension)
            
            # Additional domain-specific checks
            if can_handle and tension.description:
                description_lower = tension.description.lower()
                
                # Check for development-related keywords
                dev_keywords = ["code", "api", "database", "frontend", "backend", "integration", 
                              "development", "programming", "software", "application", "system",
                              "bug", "feature", "refactor", "optimize", "test", "deploy"]
                
                keyword_match = any(keyword in description_lower for keyword in dev_keywords)
                
                if not keyword_match:
                    self.logger.debug(f"No development-related keywords found in tension description")
                    can_handle = False
                
                # Assess technical complexity và WIN potential
                if can_handle:
                    complexity = self._assess_technical_complexity(tension)
                    win_potential = self._calculate_win_potential(tension, complexity)
                    
                    # Only handle if WIN potential >= 60
                    if win_potential < 60.0:
                        self.logger.info(f"WIN potential {win_potential} below threshold for tension {tension.tensionId}")
                        can_handle = False
                    else:
                        self.logger.info(f"CodeGenerator can handle tension {tension.tensionId} with WIN potential {win_potential}")
            
            return can_handle
            
        except Exception as e:
            self.logger.error(f"Error in can_handle_tension: {e}")
            return False
    
    def _assess_technical_complexity(self, tension: Tension) -> str:
        """Assess technical complexity of development task"""
        if not tension.description:
            return "medium"
        
        description = tension.description.lower()
        
        # High complexity indicators
        high_complexity_keywords = [
            "microservices", "distributed system", "machine learning integration",
            "real-time", "high performance", "scalability", "architecture redesign",
            "migration", "complex algorithm", "multi-tenant"
        ]
        
        # Medium complexity indicators
        medium_complexity_keywords = [
            "api integration", "database design", "authentication", "testing suite",
            "frontend framework", "state management", "responsive design", "optimization"
        ]
        
        # Low complexity indicators
        low_complexity_keywords = [
            "simple crud", "basic form", "static page", "configuration", "minor bug fix"
        ]
        
        if any(keyword in description for keyword in high_complexity_keywords):
            return "high"
        elif any(keyword in description for keyword in low_complexity_keywords):
            return "low"
        elif any(keyword in description for keyword in medium_complexity_keywords):
            return "medium"
        else:
            return "medium"  # Default to medium
    
    def _calculate_win_potential(self, tension: Tension, complexity: str) -> float:
        """Calculate potential WIN score for this development tension"""
        base_score = 50.0
        
        # Wisdom component (understanding technical and business context)
        wisdom_score = 75.0
        if tension.priority == Priority.HIGH:
            wisdom_score += 10.0
        elif tension.priority == Priority.CRITICAL:
            wisdom_score += 20.0
        
        # Intelligence component (technical capability and solution quality)
        intelligence_score = 85.0  # Base development capability
        if complexity == "high":
            intelligence_score += 15.0  # Complex problems showcase intelligence
        elif complexity == "low":
            intelligence_score -= 5.0  # Simple tasks don't showcase full capability
        
        # Networking component (collaboration and code maintainability)
        networking_score = 70.0
        if tension.description:
            desc = tension.description.lower()
            if any(word in desc for word in ["team", "collaboration", "integration", "api"]):
                networking_score += 15.0
            if any(word in desc for word in ["documentation", "maintainable", "reusable"]):
                networking_score += 10.0
        
        # Calculate total WIN using TRM-OS formula
        total_win = (wisdom_score * 0.4 + intelligence_score * 0.4 + networking_score * 0.2)
        
        return min(100.0, max(0.0, total_win))
    
    async def analyze_tension_requirements(self, tension: Tension) -> Dict[str, Any]:
        """
        Analyze development requirements for the tension.
        Extends base quantum model với domain-specific analysis.
        """
        # Get base requirements from quantum model
        base_requirements = await super().analyze_tension_requirements(tension)
        
        # Add development-specific requirements
        dev_requirements = {
            "development_type": self._determine_development_type(tension),
            "technical_stack": self._determine_tech_stack(tension),
            "development_approach": self._determine_dev_approach(tension),
            "architecture_pattern": self._select_architecture_pattern(tension),
            "testing_strategy": self._define_testing_strategy(tension),
            "testing_requirements": self._define_testing_strategy(tension),  # Add for test compatibility
            "deployment_strategy": self._define_deployment_strategy(tension),
            "code_quality_requirements": self._define_quality_requirements(tension),
            "performance_requirements": self._define_performance_requirements(tension),
            "security_requirements": self._define_security_requirements(tension),
            "estimated_effort": self._estimate_development_effort(tension).get("hours", 40),  # Convert to numeric for tests
            "deliverables": self._define_development_deliverables(tension)
        }
        
        # Merge với base requirements
        base_requirements.update(dev_requirements)
        
        return base_requirements
    
    def _determine_tech_stack(self, tension: Tension) -> Dict[str, str]:
        """Determine appropriate technology stack"""
        stack = {
            "backend": "fastapi",
            "frontend": "react",
            "database": "postgresql",
            "testing": "pytest"
        }
        
        if tension.description:
            desc = tension.description.lower()
            
            # Backend framework selection
            if "django" in desc:
                stack["backend"] = "django"
            elif "express" in desc or "node" in desc:
                stack["backend"] = "express"
            
            # Frontend framework selection
            if "nextjs" in desc or "next.js" in desc:
                stack["frontend"] = "nextjs"
            elif "vue" in desc:
                stack["frontend"] = "vue"
            
            # Database selection
            if "mongodb" in desc or "nosql" in desc:
                stack["database"] = "mongodb"
            elif "redis" in desc:
                stack["database"] = "redis"
        
        return stack
    
    def _determine_dev_approach(self, tension: Tension) -> str:
        """Determine development approach"""
        complexity = self._assess_technical_complexity(tension)
        
        if complexity == "high":
            return "iterative_with_prototyping"
        elif complexity == "low":
            return "direct_implementation"
        else:
            return "agile_incremental"
    
    def _select_architecture_pattern(self, tension: Tension) -> str:
        """Select appropriate architecture pattern"""
        if not tension.description:
            return "clean_architecture"
        
        desc = tension.description.lower()
        
        if "microservice" in desc:
            return "microservices"
        elif "api" in desc:
            return "api_first"
        elif "component" in desc:
            return "component_based"
        else:
            return "clean_architecture"
    
    def _define_testing_strategy(self, tension: Tension) -> Dict[str, Any]:
        """Define comprehensive testing strategy"""
        complexity = self._assess_technical_complexity(tension)
        
        strategy = {
            "unit_tests": True,
            "integration_tests": True,
            "coverage_target": 80
        }
        
        if complexity == "high":
            strategy.update({
                "e2e_tests": True,
                "performance_tests": True,
                "coverage_target": 90
            })
        elif complexity == "medium":
            strategy.update({
                "e2e_tests": True,
                "coverage_target": 85
            })
        
        return strategy
    
    def _define_deployment_strategy(self, tension: Tension) -> Dict[str, Any]:
        """Define deployment strategy"""
        return {
            "containerization": "docker",
            "orchestration": "kubernetes" if self._assess_technical_complexity(tension) == "high" else "docker_compose",
            "ci_cd": "github_actions",
            "monitoring": "prometheus_grafana",
            "logging": "structured_logging"
        }
    
    def _define_quality_requirements(self, tension: Tension) -> Dict[str, Any]:
        """Define code quality requirements"""
        return {
            "code_style": "automated_formatting",
            "type_safety": "strict_typing",
            "documentation": "comprehensive_docstrings",
            "code_review": "mandatory_peer_review",
            "static_analysis": "linting_and_security_scan",
            "maintainability_index": "> 75"
        }
    
    def _define_performance_requirements(self, tension: Tension) -> Dict[str, Any]:
        """Define performance requirements"""
        complexity = self._assess_technical_complexity(tension)
        
        if complexity == "high":
            return {
                "response_time": "< 200ms",
                "throughput": "> 1000 req/sec",
                "memory_usage": "< 512MB",
                "cpu_usage": "< 70%"
            }
        elif complexity == "medium":
            return {
                "response_time": "< 500ms",
                "throughput": "> 500 req/sec",
                "memory_usage": "< 256MB",
                "cpu_usage": "< 60%"
            }
        else:
            return {
                "response_time": "< 1000ms",
                "throughput": "> 100 req/sec",
                "memory_usage": "< 128MB",
                "cpu_usage": "< 50%"
            }
    
    def _define_security_requirements(self, tension: Tension) -> List[str]:
        """Define security requirements"""
        base_requirements = [
            "input_validation",
            "sql_injection_prevention",
            "xss_protection",
            "authentication",
            "authorization"
        ]
        
        if tension.description and "sensitive" in tension.description.lower():
            base_requirements.extend([
                "data_encryption",
                "audit_logging",
                "security_headers",
                "rate_limiting"
            ])
        
        return base_requirements
    
    def _estimate_development_effort(self, tension: Tension) -> Dict[str, Any]:
        """Estimate development effort"""
        complexity = self._assess_technical_complexity(tension)
        
        effort_map = {
            "low": {"days": 2, "hours": 16, "story_points": 3},
            "medium": {"days": 5, "hours": 40, "story_points": 8},
            "high": {"days": 10, "hours": 80, "story_points": 21}
        }
        
        base_effort = effort_map.get(complexity, effort_map["medium"])
        
        # Adjust based on priority (rush jobs take more effort)
        if tension.priority == Priority.CRITICAL:
            base_effort = {k: int(v * 1.3) if isinstance(v, (int, float)) else v 
                          for k, v in base_effort.items()}
        
        return base_effort
    
    def _define_development_deliverables(self, tension: Tension) -> List[str]:
        """Define development deliverables based on tension content and development type"""
        deliverables = [
            "working_code",
            "unit_tests",
            "technical_documentation",
            "deployment_instructions"
        ]
        
        # Add specific deliverables based on tension title and description
        if tension.title:
            title_lower = tension.title.lower()
            if "automation" in title_lower or "script" in title_lower:
                deliverables.append("Automation Script")
            elif "api" in title_lower:
                deliverables.append("API Implementation")
            elif "ui" in title_lower or "interface" in title_lower:
                deliverables.append("User Interface")
            elif "integration" in title_lower:
                deliverables.append("Integration Solution")
        
        complexity = self._assess_technical_complexity(tension)
        
        if complexity in ["medium", "high"]:
            deliverables.extend([
                "integration_tests",
                "api_documentation",
                "performance_benchmarks"
            ])
        
        if complexity == "high":
            deliverables.extend([
                "architecture_documentation",
                "security_analysis",
                "monitoring_setup"
            ])
        
        return deliverables
    
    async def generate_specialized_solutions(self, tension: Tension, requirements: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Generate development solutions optimized for WIN score.
        """
        if not requirements:
            requirements = await self.analyze_tension_requirements(tension)
        
        # Get base solutions from quantum model
        base_solutions = await super().generate_specialized_solutions(tension, requirements)
        
        # Enhance with development-specific solutions
        complexity = self._assess_technical_complexity(tension)
        tech_stack = requirements.get("technical_stack", {})
        
        enhanced_solutions = []
        
        for solution in base_solutions:
            # Enhance base solution with development-specific details
            enhanced_solution = solution.copy()
            enhanced_solution.update({
                "agent_template": "CodeGeneratorAgent",  # Add agent_template field for tests
                "technical_implementation": self._design_technical_implementation(requirements),
                "development_phases": self._plan_development_phases(complexity),
                "risk_mitigation": self._identify_technical_risks(tension, complexity),
                "quality_gates": self._define_quality_gates(requirements),
                "business_value": self._calculate_business_value(tension, complexity)
            })
            
            # Recalculate WIN score with development expertise
            enhanced_solution["expected_win_score"] = self._calculate_enhanced_win_score(
                enhanced_solution, tension, requirements
            )
            
            enhanced_solutions.append(enhanced_solution)
        
        # Add specialized development solution
        specialized_solution = {
            "id": f"dev_solution_{tension.tensionId}_specialized",
            "type": "comprehensive_development_solution",
            "agent_template": "CodeGeneratorAgent",  # Add agent_template field for tests
            "title": self._generate_development_solution_title(tension, requirements.get("development_type", "general")),  # Add intelligent title
            "description": f"Full-stack development solution with {complexity} complexity",
            "approach": "clean_architecture_with_testing",
            "technical_stack": tech_stack,
            "development_methodology": requirements.get("development_approach", "agile_incremental"),
            "deliverables": requirements.get("deliverables", []),
            "effort_estimate": requirements.get("estimated_effort", {}),
            "quality_assurance": requirements.get("testing_strategy", {}),
            "expected_win_score": self._calculate_specialized_win_score(tension, complexity),
            "confidence": 0.9,
            "business_impact": "high" if complexity == "high" else "medium",
            "technical_debt_reduction": True,
            "maintainability_improvement": True,
            "scalability_enhancement": complexity in ["medium", "high"],
            "success_probability": 95.0
        }
        
        enhanced_solutions.append(specialized_solution)
        
        # Sort by WIN score descending
        enhanced_solutions.sort(key=lambda x: x.get("expected_win_score", 0), reverse=True)
        
        return enhanced_solutions
    
    def _design_technical_implementation(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Design detailed technical implementation"""
        return {
            "architecture": requirements.get("architecture_pattern", "clean_architecture"),
            "tech_stack": requirements.get("technical_stack", {}),
            "data_layer": "repository_pattern_with_orm",
            "business_logic": "service_layer_with_dependency_injection",
            "api_layer": "restful_with_openapi_spec",
            "frontend_layer": "component_based_with_state_management",
            "testing_pyramid": "unit_integration_e2e",
            "deployment": requirements.get("deployment_strategy", {})
        }
    
    def _plan_development_phases(self, complexity: str) -> List[Dict[str, Any]]:
        """Plan development phases"""
        if complexity == "high":
            return [
                {"phase": "discovery", "duration_days": 2, "deliverables": ["technical_spec", "architecture_design"]},
                {"phase": "foundation", "duration_days": 3, "deliverables": ["project_setup", "core_models", "basic_tests"]},
                {"phase": "core_development", "duration_days": 4, "deliverables": ["business_logic", "api_endpoints", "integration_tests"]},
                {"phase": "integration", "duration_days": 2, "deliverables": ["frontend_integration", "e2e_tests"]},
                {"phase": "optimization", "duration_days": 1, "deliverables": ["performance_tuning", "security_hardening"]}
            ]
        elif complexity == "medium":
            return [
                {"phase": "planning", "duration_days": 1, "deliverables": ["technical_spec"]},
                {"phase": "development", "duration_days": 3, "deliverables": ["core_functionality", "tests"]},
                {"phase": "integration", "duration_days": 1, "deliverables": ["integration_tests", "documentation"]}
            ]
        else:
            return [
                {"phase": "development", "duration_days": 1, "deliverables": ["implementation", "unit_tests"]},
                {"phase": "testing", "duration_days": 0.5, "deliverables": ["validation", "documentation"]}
            ]
    
    def _identify_technical_risks(self, tension: Tension, complexity: str) -> List[Dict[str, Any]]:
        """Identify and plan mitigation for technical risks"""
        risks = []
        
        if complexity == "high":
            risks.extend([
                {
                    "risk": "architecture_complexity",
                    "probability": "medium",
                    "impact": "high",
                    "mitigation": "iterative_development_with_prototyping"
                },
                {
                    "risk": "performance_bottlenecks",
                    "probability": "medium",
                    "impact": "medium",
                    "mitigation": "early_performance_testing"
                }
            ])
        
        # Common risks for all complexities
        risks.extend([
            {
                "risk": "requirement_changes",
                "probability": "medium",
                "impact": "medium",
                "mitigation": "agile_methodology_with_frequent_feedback"
            },
            {
                "risk": "integration_issues",
                "probability": "low",
                "impact": "medium",
                "mitigation": "comprehensive_integration_testing"
            }
        ])
        
        return risks
    
    def _define_quality_gates(self, requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Define quality gates for development process"""
        return [
            {
                "gate": "code_quality",
                "criteria": ["linting_passes", "type_checking_passes", "code_coverage >= 80%"],
                "automated": True
            },
            {
                "gate": "functionality",
                "criteria": ["all_tests_pass", "acceptance_criteria_met"],
                "automated": True
            },
            {
                "gate": "performance",
                "criteria": requirements.get("performance_requirements", {}),
                "automated": True
            },
            {
                "gate": "security",
                "criteria": ["security_scan_passes", "vulnerability_assessment_clean"],
                "automated": True
            },
            {
                "gate": "documentation",
                "criteria": ["api_docs_complete", "code_documented", "deployment_guide_ready"],
                "automated": False
            }
        ]
    
    def _calculate_business_value(self, tension: Tension, complexity: str) -> Dict[str, Any]:
        """Calculate expected business value of development work"""
        base_value = 75000  # Base value for development work
        
        multipliers = {
            "low": 0.5,
            "medium": 1.0,
            "high": 2.5
        }
        
        priority_multipliers = {
            Priority.LOW: 0.8,
            Priority.NORMAL: 1.0,
            Priority.HIGH: 1.3,
            Priority.CRITICAL: 1.8
        }
        
        estimated_value = (base_value * 
                          multipliers.get(complexity, 1.0) * 
                          priority_multipliers.get(tension.priority, 1.0))
        
        return {
            "estimated_value_usd": estimated_value,
            "value_drivers": [
                "operational_efficiency",
                "technical_debt_reduction", 
                "scalability_improvement",
                "maintenance_cost_reduction"
            ],
            "roi_timeframe": "6-12 months",
            "productivity_gain": f"{20 if complexity == 'high' else 10}% improvement"
        }
    
    def _calculate_enhanced_win_score(self, solution: Dict[str, Any], tension: Tension, requirements: Dict[str, Any]) -> float:
        """Calculate enhanced WIN score with development expertise"""
        base_score = solution.get("expected_win_score", 50.0)
        
        # Wisdom enhancement (business and technical understanding)
        wisdom_boost = 0.0
        if solution.get("business_value", {}).get("estimated_value_usd", 0) > 150000:
            wisdom_boost += 15.0
        if "technical_debt_reduction" in solution.get("value_drivers", []):
            wisdom_boost += 10.0
        
        # Intelligence enhancement (technical sophistication)
        intelligence_boost = 0.0
        if "clean_architecture" in solution.get("technical_implementation", {}).get("architecture", ""):
            intelligence_boost += 12.0
        if solution.get("quality_assurance", {}).get("coverage_target", 0) >= 90:
            intelligence_boost += 8.0
        
        # Networking enhancement (collaboration and maintainability)
        networking_boost = 0.0
        if solution.get("maintainability_improvement", False):
            networking_boost += 15.0
        if len(solution.get("deliverables", [])) > 5:
            networking_boost += 10.0
        
        enhanced_score = base_score + (wisdom_boost * 0.4 + intelligence_boost * 0.4 + networking_boost * 0.2)
        
        return min(100.0, enhanced_score)
    
    def _calculate_specialized_win_score(self, tension: Tension, complexity: str) -> float:
        """Calculate WIN score for specialized development solution"""
        # Base score for development expertise
        wisdom = 88.0  # Deep understanding of technical and business requirements
        intelligence = 92.0  # High technical proficiency
        networking = 80.0  # Strong collaboration through clean code and documentation
        
        # Adjust based on complexity
        complexity_multipliers = {
            "low": 0.85,
            "medium": 1.0,
            "high": 1.15
        }
        
        multiplier = complexity_multipliers.get(complexity, 1.0)
        
        total_win = ((wisdom * multiplier) * 0.4 + 
                    (intelligence * multiplier) * 0.4 + 
                    (networking * multiplier) * 0.2)
        
        return min(100.0, total_win)
    
    async def _register_specialized_handlers(self) -> None:
        """Register development-specific event handlers"""
        # Subscribe to development-related events
        self.subscribe_to_event(EventType.CODE_REVIEW_REQUESTED)
        self.subscribe_to_event(EventType.DEPLOYMENT_REQUESTED)
        self.subscribe_to_event(EventType.BUG_REPORTED)
        self.subscribe_to_event(EventType.FEATURE_REQUESTED)
    
    async def _initialize_specialized_components(self) -> None:
        """Initialize development-specific components"""
        self.logger.info(f"Initializing CodeGenerator specialized components for {self.agent_id}")
        
        # Initialize development session
        self.development_tools["current_session"] = {
            "start_time": datetime.now(),
            "active_projects": [],
            "completed_projects": [],
            "code_quality_metrics": {
                "lines_of_code": 0,
                "test_coverage": 0.0,
                "bug_count": 0,
                "performance_score": 0.0
            }
        }
        
        # Load coding standards for session
        self.coding_standards["session_preferences"] = {
            "preferred_language": "python",
            "preferred_framework": "fastapi",
            "testing_approach": "tdd",
            "documentation_level": "comprehensive"
        }
    
    async def _handle_specialized_event(self, event: SystemEvent) -> None:
        """Handle development-specific events"""
        try:
            if event.event_type == EventType.CODE_REVIEW_REQUESTED:
                await self._handle_code_review_requested(event)
            elif event.event_type == EventType.DEPLOYMENT_REQUESTED:
                await self._handle_deployment_requested(event)
            elif event.event_type == EventType.BUG_REPORTED:
                await self._handle_bug_reported(event)
            elif event.event_type == EventType.FEATURE_REQUESTED:
                await self._handle_feature_requested(event)
            else:
                self.logger.debug(f"Unhandled specialized event: {event.event_type}")
                
        except Exception as e:
            self.logger.error(f"Error handling specialized event {event.event_type}: {e}")
    
    async def _handle_code_review_requested(self, event: SystemEvent) -> None:
        """Handle code review request events"""
        self.logger.info(f"Code review requested: {event.data}")
        
        # Create review entry
        review_entry = {
            "id": f"review_{datetime.now().timestamp()}",
            "code_location": event.data.get("code_location"),
            "review_type": event.data.get("review_type", "standard"),
            "status": "queued",
            "created_at": datetime.now()
        }
        
        # Send acknowledgment
        await self.send_event(
            event_type=EventType.CODE_REVIEW_QUEUED,
            data={"review_id": review_entry["id"], "estimated_completion": "2-4 hours"}
        )
    
    async def _handle_deployment_requested(self, event: SystemEvent) -> None:
        """Handle deployment request events"""
        self.logger.info(f"Deployment requested: {event.data}")
        
        # Validate deployment readiness
        deployment_checks = [
            "tests_passing",
            "code_review_approved", 
            "security_scan_clean",
            "performance_benchmarks_met"
        ]
        
        # Send deployment status
        await self.send_event(
            event_type=EventType.DEPLOYMENT_VALIDATION_STARTED,
            data={
                "deployment_id": event.data.get("deployment_id"),
                "checks_required": deployment_checks
            }
        )
    
    async def _handle_bug_reported(self, event: SystemEvent) -> None:
        """Handle bug report events"""
        self.logger.info(f"Bug reported: {event.data}")
        
        # Assess bug severity and priority
        bug_data = event.data
        severity = bug_data.get("severity", "medium")
        
        # Create bug fix entry
        bug_fix_entry = {
            "id": f"bugfix_{datetime.now().timestamp()}",
            "bug_id": bug_data.get("bug_id"),
            "severity": severity,
            "estimated_effort": self._estimate_bug_fix_effort(severity),
            "status": "triaged",
            "created_at": datetime.now()
        }
        
        # Add to active projects
        self.development_tools["current_session"]["active_projects"].append(bug_fix_entry)
        
        # Send acknowledgment
        await self.send_event(
            event_type=EventType.BUG_FIX_QUEUED,
            data={
                "bug_fix_id": bug_fix_entry["id"],
                "estimated_completion": bug_fix_entry["estimated_effort"]
            }
        )
    
    async def _handle_feature_requested(self, event: SystemEvent) -> None:
        """Handle feature request events"""
        self.logger.info(f"Feature requested: {event.data}")
        
        # Analyze feature complexity
        feature_data = event.data
        complexity = self._assess_feature_complexity(feature_data.get("description", ""))
        
        # Create feature development entry
        feature_entry = {
            "id": f"feature_{datetime.now().timestamp()}",
            "feature_id": feature_data.get("feature_id"),
            "complexity": complexity,
            "estimated_effort": self._estimate_feature_effort(complexity),
            "status": "analyzed",
            "created_at": datetime.now()
        }
        
        # Send analysis results
        await self.send_event(
            event_type=EventType.FEATURE_ANALYSIS_COMPLETE,
            data={
                "feature_id": feature_entry["feature_id"],
                "complexity": complexity,
                "estimated_effort": feature_entry["estimated_effort"],
                "recommended_approach": self._recommend_development_approach(complexity)
            }
        )
    
    def _estimate_bug_fix_effort(self, severity: str) -> str:
        """Estimate effort required for bug fix"""
        effort_map = {
            "critical": "4-8 hours",
            "high": "2-4 hours", 
            "medium": "1-2 hours",
            "low": "0.5-1 hour"
        }
        return effort_map.get(severity, "1-2 hours")
    
    def _assess_feature_complexity(self, description: str) -> str:
        """Assess complexity of feature request"""
        if not description:
            return "medium"
        
        desc = description.lower()
        
        if any(word in desc for word in ["integration", "api", "database", "complex"]):
            return "high"
        elif any(word in desc for word in ["simple", "basic", "minor"]):
            return "low"
        else:
            return "medium"
    
    def _estimate_feature_effort(self, complexity: str) -> str:
        """Estimate effort for feature development"""
        effort_map = {
            "low": "1-2 days",
            "medium": "3-5 days",
            "high": "1-2 weeks"
        }
        return effort_map.get(complexity, "3-5 days")
    
    def _recommend_development_approach(self, complexity: str) -> str:
        """Recommend development approach based on complexity"""
        approach_map = {
            "low": "direct_implementation",
            "medium": "agile_with_testing",
            "high": "iterative_with_prototyping"
        }
        return approach_map.get(complexity, "agile_with_testing")

    def _determine_development_type(self, tension: Tension) -> str:
        """Determine type of development needed with intelligent keyword matching"""
        if not tension.description:
            return "general_development"
        
        desc = tension.description.lower()
        
        # Automation development keywords
        automation_keywords = ["automation", "script", "deploy", "streamline", "automate", 
                             "tự động", "kịch bản", "triển khai"]
        
        # API development keywords  
        api_keywords = ["api", "rest", "endpoint", "integration", "service",
                       "giao diện", "tích hợp", "dịch vụ"]
        
        # Frontend development keywords
        frontend_keywords = ["ui", "frontend", "interface", "web", "react", "vue",
                           "giao diện", "trang web", "frontend"]
        
        # Backend development keywords
        backend_keywords = ["backend", "server", "database", "microservice",
                          "backend", "máy chủ", "cơ sở dữ liệu"]
        
        # Bug fix keywords
        bugfix_keywords = ["bug", "fix", "error", "issue", "problem",
                         "lỗi", "sửa", "vấn đề"]
        
        # Check for specific development types
        if any(keyword in desc for keyword in automation_keywords):
            return "automation"
        elif any(keyword in desc for keyword in api_keywords):
            return "api_development"
        elif any(keyword in desc for keyword in frontend_keywords):
            return "frontend_development"
        elif any(keyword in desc for keyword in backend_keywords):
            return "backend_development"
        elif any(keyword in desc for keyword in bugfix_keywords):
            return "bug_fix"
        else:
            return "general_development"

    def _generate_development_solution_title(self, tension: Tension, development_type: str) -> str:
        """Generate intelligent solution title based on development type and tension content"""
        if development_type == "automation":
            return "Automation Script Development"
        elif development_type == "api_development":
            return "REST API Integration Solution"
        elif development_type == "frontend_development":
            return "Frontend Component Development"
        elif development_type == "backend_development":
            return "Backend Service Implementation"
        elif development_type == "bug_fix":
            return "Bug Fix & Code Improvement"
        else:
            return "Full-Stack Development Solution" 