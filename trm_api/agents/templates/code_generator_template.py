"""
Code Generator Agent Template

Agent chuyên biệt xử lý các tensions liên quan đến coding, development,
automation và technical implementation trong TRM-OS.
"""

import re
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime

from .base_template import BaseAgentTemplate, AgentTemplateMetadata, AgentCapability
from ..base_agent import AgentMetadata
from ...eventbus.system_event_bus import EventType, SystemEvent
from ...models.tension import Tension


class CodeGeneratorAgent(BaseAgentTemplate):
    """
    Agent chuyên biệt cho code generation và development automation.
    
    Capabilities:
    - Code generation và refactoring
    - API development
    - Automation scripts
    - Testing code generation
    - Documentation generation
    - Code review và optimization
    """
    
    def __init__(self, agent_id: Optional[str] = None, metadata: Optional[AgentMetadata] = None):
        # Tạo metadata cho CodeGenerator nếu chưa có
        if not metadata:
            metadata = AgentMetadata(
                name="CodeGeneratorAgent",
                agent_type="CodeGenerator",
                description="AI Agent chuyên biệt xử lý tensions liên quan đến coding và development automation",
                capabilities=["code_generation", "api_development", "automation_scripting", "testing", "documentation", "code_review"],
                status="active",
                version="1.0.0"
            )
        
        super().__init__(agent_id, metadata)
        
        # Code-specific patterns
        self.code_patterns = {
            "development_requests": [
                r"(?:tạo|viết|develop|create).*(?:code|api|function|module)",
                r"implement.*(?:feature|functionality|logic)",
                r"automation.*(?:script|tool|process)",
                r"refactor.*(?:code|codebase|function)"
            ],
            "bug_fixes": [
                r"(?:fix|sửa|debug).*(?:bug|lỗi|error|issue)",
                r"(?:not working|không hoạt động|broken|hỏng)",
                r"exception.*(?:error|lỗi)",
                r"performance.*(?:slow|chậm|issue|problem)"
            ],
            "testing_needs": [
                r"(?:test|testing|unit test|integration test)",
                r"(?:coverage|test coverage)",
                r"(?:quality assurance|qa)",
                r"(?:validation|verify|kiểm tra)"
            ],
            "documentation": [
                r"(?:document|documentation|docs|tài liệu)",
                r"(?:readme|guide|hướng dẫn)",
                r"(?:api doc|api documentation)",
                r"(?:comment|ghi chú|annotation)"
            ]
        }
        
        self.programming_languages = {
            "backend": ["python", "java", "node.js", "go", "c#"],
            "frontend": ["javascript", "typescript", "react", "vue", "angular"],
            "mobile": ["swift", "kotlin", "react native", "flutter"],
            "data": ["python", "r", "sql", "scala"],
            "devops": ["bash", "powershell", "terraform", "docker"]
        }
        
        self.development_patterns = {
            "api_development": ["REST", "GraphQL", "gRPC", "WebSocket"],
            "architecture_patterns": ["MVC", "MVP", "MVVM", "Clean Architecture", "Microservices"],
            "testing_frameworks": ["pytest", "jest", "junit", "mocha", "cypress"],
            "automation_tools": ["selenium", "playwright", "github actions", "jenkins"]
        }
    
    def _get_default_template_metadata(self) -> AgentTemplateMetadata:
        """Trả về metadata mặc định cho CodeGenerator template"""
        return AgentTemplateMetadata(
            template_name="CodeGeneratorAgent",
            template_version="1.0.0",
            description="Agent chuyên biệt xử lý tensions liên quan đến coding và development automation",
            primary_domain="code",
            capabilities=[
                AgentCapability(
                    name="code_generation",
                    description="Tạo code tự động theo specifications",
                    required_skills=["programming", "software_design", "best_practices"],
                    complexity_level=4,
                    estimated_time=120
                ),
                AgentCapability(
                    name="api_development",
                    description="Phát triển APIs và web services",
                    required_skills=["api_design", "backend_development", "database_integration"],
                    complexity_level=4,
                    estimated_time=180
                ),
                AgentCapability(
                    name="automation_scripting",
                    description="Tạo automation scripts và tools",
                    required_skills=["scripting", "automation", "workflow_optimization"],
                    complexity_level=3,
                    estimated_time=90
                ),
                AgentCapability(
                    name="testing_automation",
                    description="Tạo automated tests và test frameworks",
                    required_skills=["testing", "quality_assurance", "test_automation"],
                    complexity_level=3,
                    estimated_time=60
                ),
                AgentCapability(
                    name="code_review_optimization",
                    description="Review và optimize existing code",
                    required_skills=["code_review", "performance_optimization", "refactoring"],
                    complexity_level=3,
                    estimated_time=45
                ),
                AgentCapability(
                    name="documentation_generation",
                    description="Tạo technical documentation tự động",
                    required_skills=["technical_writing", "documentation", "code_analysis"],
                    complexity_level=2,
                    estimated_time=30
                )
            ],
            recommended_tensions=[
                "Development Tasks",
                "Bug Fixes",
                "Automation Needs",
                "Testing Requirements",
                "Code Quality Issues",
                "Documentation Gaps"
            ],
            dependencies=["development_environment", "version_control", "testing_tools"],
            performance_metrics=[
                "code_quality_score",
                "development_velocity",
                "bug_reduction_rate",
                "test_coverage_improvement",
                "automation_efficiency"
            ]
        )
    
    async def can_handle_tension(self, tension: Tension) -> bool:
        """Kiểm tra xem có thể xử lý tension này không"""
        try:
            description = tension.description.lower()
            title = tension.title.lower()
            
            # Tìm coding-related keywords
            code_keywords = [
                "code", "coding", "develop", "development", "api", "function",
                "script", "automation", "bug", "lỗi", "test", "testing",
                "refactor", "optimize", "documentation", "docs", "implement",
                "feature", "module", "component", "library", "framework"
            ]
            
            has_code_keywords = any(keyword in description or keyword in title 
                                  for keyword in code_keywords)
            
            # Kiểm tra programming language mentions
            has_language_keywords = any(
                lang in description or lang in title
                for lang_category in self.programming_languages.values()
                for lang in lang_category
            )
            
            # Kiểm tra code patterns
            pattern_match = False
            for category, patterns in self.code_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, description, re.IGNORECASE) or \
                       re.search(pattern, title, re.IGNORECASE):
                        pattern_match = True
                        break
                if pattern_match:
                    break
            
            # Kiểm tra tension type
            suitable_types = ["Problem", "Opportunity", "Idea"]
            type_match = tension.tension_type in suitable_types
            
            # Agent có thể handle nếu có code indicators
            can_handle = (has_code_keywords or has_language_keywords or pattern_match) and type_match
            
            if can_handle:
                self.logger.info(f"CodeGenerator can handle tension {tension.uid}: {tension.title}")
            
            return can_handle
            
        except Exception as e:
            self.logger.error(f"Error checking tension handleability: {str(e)}")
            return False
    
    async def analyze_tension_requirements(self, tension: Tension) -> Dict[str, Any]:
        """Phân tích requirements cụ thể cho coding tension"""
        requirements = {
            "development_type": "unknown",
            "programming_languages": [],
            "complexity": "medium",
            "urgency": "normal",
            "deliverables": [],
            "tools_needed": [],
            "estimated_effort": 120,
            "success_criteria": [],
            "testing_requirements": [],
            "documentation_needs": []
        }
        
        try:
            description = tension.description.lower()
            title = tension.title.lower()
            combined_text = f"{title} {description}"
            
            # Xác định loại development
            if any(pattern in combined_text for pattern in ["api", "web service", "endpoint"]):
                requirements["development_type"] = "api_development"
                requirements["tools_needed"].extend(["api_framework", "database", "testing_tools"])
                requirements["deliverables"].append("API Implementation")
                requirements["estimated_effort"] = 180
                
            elif any(pattern in combined_text for pattern in ["automation", "script", "tool"]):
                requirements["development_type"] = "automation"
                requirements["tools_needed"].extend(["scripting_environment", "automation_framework"])
                requirements["deliverables"].append("Automation Script")
                requirements["estimated_effort"] = 90
                
            elif any(pattern in combined_text for pattern in ["test", "testing", "qa"]):
                requirements["development_type"] = "testing"
                requirements["tools_needed"].extend(["testing_framework", "test_data"])
                requirements["deliverables"].append("Test Suite")
                requirements["estimated_effort"] = 60
                
            elif any(pattern in combined_text for pattern in ["bug", "fix", "debug", "lỗi"]):
                requirements["development_type"] = "bug_fix"
                requirements["tools_needed"].extend(["debugging_tools", "profiling_tools"])
                requirements["deliverables"].append("Bug Fix")
                requirements["estimated_effort"] = 45
                
            elif any(pattern in combined_text for pattern in ["refactor", "optimize", "improve"]):
                requirements["development_type"] = "refactoring"
                requirements["tools_needed"].extend(["code_analysis", "performance_tools"])
                requirements["deliverables"].append("Refactored Code")
                requirements["estimated_effort"] = 90
                
            elif any(pattern in combined_text for pattern in ["document", "docs", "readme"]):
                requirements["development_type"] = "documentation"
                requirements["tools_needed"].extend(["documentation_tools", "code_analysis"])
                requirements["deliverables"].append("Technical Documentation")
                requirements["estimated_effort"] = 30
                
            # Detect programming languages
            for category, languages in self.programming_languages.items():
                for lang in languages:
                    if lang in combined_text:
                        requirements["programming_languages"].append(lang)
            
            # Xác định complexity
            complexity_indicators = {
                "high": ["complex", "phức tạp", "advanced", "enterprise", "scalable", "microservice"],
                "low": ["simple", "đơn giản", "basic", "cơ bản", "quick", "nhanh"]
            }
            
            for level, indicators in complexity_indicators.items():
                if any(indicator in combined_text for indicator in indicators):
                    requirements["complexity"] = level
                    break
            
            # Adjust effort based on complexity
            if requirements["complexity"] == "high":
                requirements["estimated_effort"] = int(requirements["estimated_effort"] * 1.5)
            elif requirements["complexity"] == "low":
                requirements["estimated_effort"] = int(requirements["estimated_effort"] * 0.7)
            
            # Xác định urgency
            if any(pattern in combined_text for pattern in ["urgent", "gấp", "asap", "critical"]):
                requirements["urgency"] = "high"
                requirements["estimated_effort"] = max(30, requirements["estimated_effort"] // 2)
            
            # Testing requirements
            if requirements["development_type"] != "testing":
                requirements["testing_requirements"] = [
                    "Unit tests cho core functionality",
                    "Integration tests nếu có external dependencies",
                    "Code coverage > 80%"
                ]
            
            # Documentation needs
            if requirements["development_type"] != "documentation":
                requirements["documentation_needs"] = [
                    "Code comments cho complex logic",
                    "README với usage instructions",
                    "API documentation nếu applicable"
                ]
            
            # Success criteria
            requirements["success_criteria"] = [
                "Code passes all tests",
                "Meets functional requirements",
                "Follows coding standards",
                "Performance meets expectations",
                "Documentation is complete"
            ]
            
            self.logger.info(f"Analyzed requirements for tension {tension.uid}: {requirements['development_type']}")
            
        except Exception as e:
            self.logger.error(f"Error analyzing tension requirements: {str(e)}")
        
        return requirements
    
    async def generate_specialized_solutions(self, tension: Tension, 
                                           requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Tạo solutions chuyên biệt cho coding tasks"""
        solutions = []
        
        try:
            development_type = requirements.get("development_type", "unknown")
            
            if development_type == "api_development":
                solutions.extend(await self._generate_api_solutions(tension, requirements))
                
            elif development_type == "automation":
                solutions.extend(await self._generate_automation_solutions(tension, requirements))
                
            elif development_type == "testing":
                solutions.extend(await self._generate_testing_solutions(tension, requirements))
                
            elif development_type == "bug_fix":
                solutions.extend(await self._generate_bugfix_solutions(tension, requirements))
                
            elif development_type == "refactoring":
                solutions.extend(await self._generate_refactoring_solutions(tension, requirements))
                
            elif development_type == "documentation":
                solutions.extend(await self._generate_documentation_solutions(tension, requirements))
                
            else:
                # Generic development solutions
                solutions.extend(await self._generate_generic_development_solutions(tension, requirements))
            
            # Thêm metadata cho tất cả solutions
            for solution in solutions:
                solution.update({
                    "agent_template": "CodeGeneratorAgent",
                    "domain": "development",
                    "estimated_effort": requirements.get("estimated_effort", 120),
                    "complexity": requirements.get("complexity", "medium"),
                    "programming_languages": requirements.get("programming_languages", []),
                    "testing_requirements": requirements.get("testing_requirements", []),
                    "success_criteria": requirements.get("success_criteria", [])
                })
            
            self.logger.info(f"Generated {len(solutions)} development solutions for tension {tension.uid}")
            
        except Exception as e:
            self.logger.error(f"Error generating solutions: {str(e)}")
        
        return solutions
    
    async def _generate_api_solutions(self, tension: Tension, 
                                    requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Tạo solutions cho API development"""
        return [
            {
                "title": "RESTful API Development",
                "description": "Phát triển RESTful API với best practices và security",
                "approach": "API-First Development",
                "steps": [
                    "Design API specification (OpenAPI/Swagger)",
                    "Implement core API endpoints",
                    "Add authentication và authorization",
                    "Implement input validation và error handling",
                    "Add logging và monitoring",
                    "Create comprehensive API documentation",
                    "Write integration tests"
                ],
                "tools": ["api_framework", "database_orm", "authentication_lib", "testing_framework"],
                "deliverables": ["API Implementation", "API Documentation", "Test Suite", "Deployment Guide"],
                "timeline": "3-4 weeks",
                "priority": 1
            },
            {
                "title": "GraphQL API Implementation",
                "description": "Implement GraphQL API với type-safe schema",
                "approach": "Schema-First GraphQL Development",
                "steps": [
                    "Design GraphQL schema",
                    "Implement resolvers và data loaders",
                    "Add query optimization và caching",
                    "Implement real-time subscriptions nếu cần",
                    "Add security layers (rate limiting, depth limiting)",
                    "Create GraphQL playground documentation",
                    "Write comprehensive tests"
                ],
                "tools": ["graphql_framework", "schema_tools", "caching_layer", "testing_tools"],
                "deliverables": ["GraphQL API", "Schema Documentation", "Test Coverage", "Performance Benchmarks"],
                "timeline": "4-5 weeks",
                "priority": 2
            }
        ]
    
    async def _generate_automation_solutions(self, tension: Tension,
                                           requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Tạo solutions cho automation tasks"""
        return [
            {
                "title": "Process Automation Script",
                "description": "Tạo automation script để streamline manual processes",
                "approach": "Script-based Automation",
                "steps": [
                    "Analyze current manual process",
                    "Identify automation opportunities",
                    "Design automation workflow",
                    "Implement automation script với error handling",
                    "Add logging và monitoring",
                    "Create configuration management",
                    "Test automation với various scenarios"
                ],
                "tools": ["scripting_language", "workflow_engine", "monitoring_tools", "config_management"],
                "deliverables": ["Automation Script", "Configuration Files", "Documentation", "Test Results"],
                "timeline": "2-3 weeks",
                "priority": 1
            },
            {
                "title": "CI/CD Pipeline Automation",
                "description": "Thiết lập automated CI/CD pipeline",
                "approach": "DevOps Automation",
                "steps": [
                    "Analyze current deployment process",
                    "Design CI/CD pipeline architecture",
                    "Implement automated testing stages",
                    "Setup automated deployment với rollback capability",
                    "Add monitoring và alerting",
                    "Create deployment documentation",
                    "Train team về new process"
                ],
                "tools": ["ci_cd_platform", "containerization", "orchestration", "monitoring"],
                "deliverables": ["CI/CD Pipeline", "Deployment Scripts", "Monitoring Setup", "Team Training"],
                "timeline": "3-4 weeks",
                "priority": 2
            }
        ]
    
    async def _generate_testing_solutions(self, tension: Tension,
                                        requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Tạo solutions cho testing needs"""
        return [
            {
                "title": "Comprehensive Test Suite",
                "description": "Tạo comprehensive test suite với high coverage",
                "approach": "Test-Driven Development",
                "steps": [
                    "Analyze codebase để identify test gaps",
                    "Design test strategy (unit, integration, e2e)",
                    "Implement unit tests cho core functionality",
                    "Create integration tests cho system interactions",
                    "Add end-to-end tests cho critical user flows",
                    "Setup test automation trong CI/CD",
                    "Generate test coverage reports"
                ],
                "tools": ["testing_framework", "mocking_library", "test_runner", "coverage_tools"],
                "deliverables": ["Test Suite", "Coverage Reports", "Test Documentation", "CI Integration"],
                "timeline": "2-3 weeks",
                "priority": 1
            },
            {
                "title": "Automated Testing Framework",
                "description": "Thiết lập automated testing framework cho long-term maintainability",
                "approach": "Framework-based Testing",
                "steps": [
                    "Design testing framework architecture",
                    "Implement test utilities và helpers",
                    "Create test data management system",
                    "Setup parallel test execution",
                    "Add visual regression testing nếu applicable",
                    "Implement test reporting dashboard",
                    "Create testing guidelines và best practices"
                ],
                "tools": ["test_framework", "test_utilities", "parallel_execution", "reporting_tools"],
                "deliverables": ["Testing Framework", "Test Utilities", "Reporting Dashboard", "Guidelines"],
                "timeline": "3-4 weeks",
                "priority": 2
            }
        ]
    
    async def _generate_bugfix_solutions(self, tension: Tension,
                                       requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Tạo solutions cho bug fixes"""
        return [
            {
                "title": "Bug Investigation & Fix",
                "description": "Systematic bug investigation và resolution",
                "approach": "Root Cause Analysis",
                "steps": [
                    "Reproduce bug trong controlled environment",
                    "Analyze logs và error traces",
                    "Identify root cause using debugging tools",
                    "Design fix với minimal impact",
                    "Implement fix với proper testing",
                    "Add regression tests",
                    "Deploy fix với monitoring"
                ],
                "tools": ["debugging_tools", "profiling_tools", "logging_analysis", "testing_framework"],
                "deliverables": ["Bug Fix", "Root Cause Analysis", "Regression Tests", "Fix Documentation"],
                "timeline": "1-2 weeks",
                "priority": 1
            }
        ]
    
    async def _generate_refactoring_solutions(self, tension: Tension,
                                            requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Tạo solutions cho code refactoring"""
        return [
            {
                "title": "Code Refactoring & Optimization",
                "description": "Systematic code refactoring để improve maintainability và performance",
                "approach": "Incremental Refactoring",
                "steps": [
                    "Analyze code quality metrics",
                    "Identify refactoring opportunities",
                    "Create comprehensive test coverage trước refactoring",
                    "Implement refactoring trong small, safe steps",
                    "Optimize performance bottlenecks",
                    "Update documentation",
                    "Validate improvements với metrics"
                ],
                "tools": ["code_analysis", "refactoring_tools", "performance_profiling", "testing_framework"],
                "deliverables": ["Refactored Code", "Performance Improvements", "Updated Documentation", "Quality Metrics"],
                "timeline": "2-3 weeks",
                "priority": 1
            }
        ]
    
    async def _generate_documentation_solutions(self, tension: Tension,
                                              requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Tạo solutions cho documentation needs"""
        return [
            {
                "title": "Comprehensive Technical Documentation",
                "description": "Tạo comprehensive technical documentation cho codebase",
                "approach": "Documentation-as-Code",
                "steps": [
                    "Analyze existing codebase để understand functionality",
                    "Create architecture documentation",
                    "Generate API documentation từ code",
                    "Write user guides và tutorials",
                    "Create deployment và maintenance guides",
                    "Setup automated documentation generation",
                    "Implement documentation review process"
                ],
                "tools": ["documentation_generator", "diagram_tools", "static_site_generator", "version_control"],
                "deliverables": ["Technical Documentation", "API Docs", "User Guides", "Architecture Diagrams"],
                "timeline": "1-2 weeks",
                "priority": 1
            }
        ]
    
    async def _generate_generic_development_solutions(self, tension: Tension,
                                                    requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Tạo generic development solutions"""
        return [
            {
                "title": "Custom Development Solution",
                "description": "Tailored development solution based on specific requirements",
                "approach": "Agile Development",
                "steps": [
                    "Gather detailed requirements",
                    "Design solution architecture",
                    "Implement core functionality",
                    "Add proper error handling và validation",
                    "Create comprehensive tests",
                    "Write documentation",
                    "Deploy và monitor solution"
                ],
                "tools": ["development_framework", "testing_tools", "deployment_platform", "monitoring"],
                "deliverables": ["Custom Implementation", "Test Suite", "Documentation", "Deployment Guide"],
                "timeline": "3-4 weeks",
                "priority": 1
            }
        ]
    
    async def execute_solution(self, solution: Dict[str, Any], 
                             context: Dict[str, Any]) -> Dict[str, Any]:
        """Thực thi coding solution"""
        execution_result = {
            "status": "completed",
            "execution_time": datetime.now().isoformat(),
            "results": {},
            "deliverables_created": [],
            "next_steps": [],
            "code_metrics": {}
        }
        
        try:
            solution_title = solution.get("title", "Unknown Solution")
            self.logger.info(f"Executing coding solution: {solution_title}")
            
            # Simulate solution execution
            await asyncio.sleep(2)  # Simulate development time
            
            # Mock results based on solution type
            if "api" in solution_title.lower():
                execution_result["results"] = {
                    "endpoints_created": 8,
                    "test_coverage": 92.5,
                    "performance_score": 85.0,
                    "security_score": 88.0
                }
                execution_result["deliverables_created"] = ["API Implementation", "API Documentation", "Test Suite"]
                execution_result["code_metrics"] = {
                    "lines_of_code": 1250,
                    "complexity_score": 15.2,
                    "maintainability_index": 78.5
                }
                
            elif "automation" in solution_title.lower():
                execution_result["results"] = {
                    "processes_automated": 5,
                    "time_saved_per_day": 180,  # minutes
                    "error_reduction": 85.0,
                    "efficiency_improvement": 65.0
                }
                execution_result["deliverables_created"] = ["Automation Script", "Configuration", "Documentation"]
                
            elif "test" in solution_title.lower():
                execution_result["results"] = {
                    "test_cases_created": 45,
                    "code_coverage": 94.2,
                    "bugs_found": 12,
                    "execution_time": 3.5  # minutes
                }
                execution_result["deliverables_created"] = ["Test Suite", "Coverage Report", "Test Documentation"]
                
            elif "bug" in solution_title.lower():
                execution_result["results"] = {
                    "bugs_fixed": 3,
                    "root_causes_identified": 2,
                    "regression_tests_added": 8,
                    "performance_improvement": 15.0
                }
                execution_result["deliverables_created"] = ["Bug Fix", "Regression Tests", "Root Cause Analysis"]
                
            elif "refactor" in solution_title.lower():
                execution_result["results"] = {
                    "code_complexity_reduced": 25.0,
                    "performance_improvement": 18.5,
                    "maintainability_improved": 30.0,
                    "technical_debt_reduced": 40.0
                }
                execution_result["deliverables_created"] = ["Refactored Code", "Performance Report", "Quality Metrics"]
                
            elif "documentation" in solution_title.lower():
                execution_result["results"] = {
                    "documentation_pages": 25,
                    "api_endpoints_documented": 15,
                    "code_coverage_documented": 88.0,
                    "readability_score": 92.0
                }
                execution_result["deliverables_created"] = ["Technical Documentation", "API Docs", "User Guides"]
                
            else:
                execution_result["results"] = {
                    "features_implemented": 5,
                    "test_coverage": 87.0,
                    "code_quality_score": 82.5,
                    "performance_score": 80.0
                }
                execution_result["deliverables_created"] = ["Implementation", "Tests", "Documentation"]
            
            execution_result["next_steps"] = [
                "Code review với team members",
                "Deploy to staging environment",
                "Conduct user acceptance testing",
                "Monitor performance metrics",
                "Plan next iteration improvements"
            ]
            
            self.logger.info(f"Successfully executed solution: {solution_title}")
            
        except Exception as e:
            execution_result["status"] = "failed"
            execution_result["error"] = str(e)
            self.logger.error(f"Error executing solution: {str(e)}")
        
        return execution_result
    
    async def _register_specialized_handlers(self) -> None:
        """Đăng ký specialized event handlers cho CodeGenerator"""
        # Đăng ký events liên quan đến development
        self.subscribe_to_event(EventType.CODE_COMMIT)
        self.subscribe_to_event(EventType.BUILD_COMPLETED)
        self.subscribe_to_event(EventType.DEPLOYMENT_REQUESTED)
        
    async def _initialize_specialized_components(self) -> None:
        """Khởi tạo development components"""
        self.logger.info("Initializing CodeGenerator specialized components")
        
        # Initialize development tools, IDE connections, etc.
        # This would be implemented based on actual infrastructure
        
    async def _handle_specialized_event(self, event: SystemEvent) -> None:
        """Xử lý specialized events cho CodeGenerator"""
        if event.event_type == EventType.CODE_COMMIT:
            await self._handle_code_commit(event)
        elif event.event_type == EventType.BUILD_COMPLETED:
            await self._handle_build_completed(event)
        elif event.event_type == EventType.DEPLOYMENT_REQUESTED:
            await self._handle_deployment_requested(event)
    
    async def _handle_code_commit(self, event: SystemEvent) -> None:
        """Xử lý sự kiện code commit"""
        self.logger.info(f"Code commit event received: {event.entity_id}")
        # Implement code commit handling logic
        
    async def _handle_build_completed(self, event: SystemEvent) -> None:
        """Xử lý sự kiện build completed"""
        self.logger.info(f"Build completed: {event.entity_id}")
        # Implement build completion handling logic
        
    async def _handle_deployment_requested(self, event: SystemEvent) -> None:
        """Xử lý sự kiện deployment requested"""
        self.logger.info(f"Deployment requested: {event.entity_id}")
        # Implement deployment handling logic 