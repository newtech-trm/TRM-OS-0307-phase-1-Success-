"""
User Interface Agent Template

Agent chuyên biệt xử lý các tensions liên quan đến user experience, user interface,
design systems và frontend development trong TRM-OS.
"""

import re
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime

from .base_template import BaseAgentTemplate, AgentTemplateMetadata, AgentCapability
from ..base_agent import AgentMetadata
from ...eventbus.system_event_bus import EventType, SystemEvent
from ...models.tension import Tension


class UserInterfaceAgent(BaseAgentTemplate):
    """
    Agent chuyên biệt cho user interface và user experience design.
    
    Capabilities:
    - UI/UX design và prototyping
    - User research và usability testing
    - Design system development
    - Frontend component creation
    - Accessibility optimization
    - Performance optimization
    """
    
    def __init__(self, agent_id: Optional[str] = None, metadata: Optional[AgentMetadata] = None):
        # Tạo metadata cho UserInterface nếu chưa có
        if not metadata:
            metadata = AgentMetadata(
                name="UserInterfaceAgent",
                agent_type="UserInterface",
                description="AI Agent chuyên biệt xử lý tensions liên quan đến UI/UX và frontend development",
                capabilities=["ui_design", "ux_research", "frontend_development", "design_systems", "accessibility", "performance_optimization"],
                status="active",
                version="1.0.0"
            )
        
        super().__init__(agent_id, metadata)
        
        # UI/UX-specific patterns
        self.ui_patterns = {
            "design_requests": [
                r"(?:design|thiết kế).*(?:ui|interface|giao diện|layout)",
                r"(?:user experience|ux|trải nghiệm người dùng)",
                r"(?:prototype|wireframe|mockup|bản mẫu)",
                r"(?:visual|visual design|thiết kế trực quan)"
            ],
            "usability_issues": [
                r"(?:usability|khả năng sử dụng|user-friendly)",
                r"(?:confusing|khó hiểu|không rõ ràng|phức tạp)",
                r"(?:navigation|điều hướng|menu|nav)",
                r"(?:user flow|luồng người dùng|workflow)"
            ],
            "frontend_issues": [
                r"(?:frontend|front-end|client-side)",
                r"(?:responsive|mobile|tablet|desktop)",
                r"(?:browser|compatibility|tương thích)",
                r"(?:performance|tốc độ|loading|slow|chậm)"
            ],
            "accessibility_needs": [
                r"(?:accessibility|khả năng tiếp cận|a11y)",
                r"(?:screen reader|đọc màn hình)",
                r"(?:keyboard navigation|điều hướng bàn phím)",
                r"(?:color contrast|độ tương phản màu)"
            ]
        }
        
        self.design_tools = {
            "design": ["figma", "sketch", "adobe xd", "invision", "framer"],
            "prototyping": ["figma", "framer", "principle", "protopie"],
            "frontend": ["react", "vue", "angular", "svelte", "html", "css", "javascript"],
            "testing": ["cypress", "selenium", "playwright", "jest"],
            "accessibility": ["axe", "wave", "lighthouse", "screen readers"]
        }
        
        self.design_principles = {
            "usability": ["consistency", "feedback", "visibility", "flexibility", "error_prevention"],
            "visual": ["hierarchy", "contrast", "alignment", "repetition", "proximity"],
            "interaction": ["affordance", "mapping", "feedback", "constraints"],
            "accessibility": ["perceivable", "operable", "understandable", "robust"]
        }
    
    def _get_default_template_metadata(self) -> AgentTemplateMetadata:
        """Trả về metadata mặc định cho UserInterface template"""
        return AgentTemplateMetadata(
            template_name="UserInterfaceAgent",
            template_version="1.0.0",
            description="Agent chuyên biệt xử lý tensions liên quan đến UI/UX và frontend development",
            primary_domain="ui",
            capabilities=[
                AgentCapability(
                    name="ui_ux_design",
                    description="Thiết kế user interface và user experience",
                    required_skills=["design_thinking", "visual_design", "user_research"],
                    complexity_level=4,
                    estimated_time=120
                ),
                AgentCapability(
                    name="user_research",
                    description="Thực hiện user research và usability testing",
                    required_skills=["user_research", "usability_testing", "data_analysis"],
                    complexity_level=3,
                    estimated_time=90
                ),
                AgentCapability(
                    name="frontend_development",
                    description="Phát triển frontend components và interfaces",
                    required_skills=["html", "css", "javascript", "frontend_frameworks"],
                    complexity_level=4,
                    estimated_time=150
                ),
                AgentCapability(
                    name="design_system_creation",
                    description="Tạo và maintain design systems",
                    required_skills=["design_systems", "component_libraries", "documentation"],
                    complexity_level=5,
                    estimated_time=200
                ),
                AgentCapability(
                    name="accessibility_optimization",
                    description="Optimize accessibility và compliance",
                    required_skills=["accessibility_standards", "wcag", "assistive_technologies"],
                    complexity_level=3,
                    estimated_time=60
                ),
                AgentCapability(
                    name="performance_optimization",
                    description="Optimize frontend performance",
                    required_skills=["performance_optimization", "web_vitals", "profiling"],
                    complexity_level=3,
                    estimated_time=45
                )
            ],
            recommended_tensions=[
                "UI/UX Design Issues",
                "Usability Problems",
                "Frontend Performance",
                "Accessibility Compliance",
                "Design System Needs",
                "User Experience Improvements"
            ],
            dependencies=["design_tools", "frontend_frameworks", "testing_tools"],
            performance_metrics=[
                "user_satisfaction_score",
                "usability_test_success_rate",
                "accessibility_compliance_score",
                "page_load_performance",
                "design_consistency_score"
            ]
        )
    
    async def can_handle_tension(self, tension: Tension) -> bool:
        """Kiểm tra xem có thể xử lý tension này không"""
        try:
            description = tension.description.lower()
            title = tension.title.lower()
            
            # Tìm UI/UX-related keywords
            ui_keywords = [
                "ui", "ux", "interface", "giao diện", "design", "thiết kế",
                "user", "người dùng", "frontend", "client", "web", "mobile",
                "usability", "accessibility", "responsive", "layout", "component",
                "visual", "interaction", "navigation", "menu", "button", "form"
            ]
            
            has_ui_keywords = any(keyword in description or keyword in title 
                                for keyword in ui_keywords)
            
            # Kiểm tra UI/UX patterns
            pattern_match = False
            for category, patterns in self.ui_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, description, re.IGNORECASE) or \
                       re.search(pattern, title, re.IGNORECASE):
                        pattern_match = True
                        break
                if pattern_match:
                    break
            
            # Kiểm tra design tool mentions
            has_tool_keywords = any(
                tool in description or tool in title
                for tool_category in self.design_tools.values()
                for tool in tool_category
            )
            
            # Kiểm tra tension type
            suitable_types = ["Problem", "Opportunity", "Idea"]
            type_match = tension.tension_type in suitable_types
            
            # Agent có thể handle nếu có UI/UX indicators
            can_handle = (has_ui_keywords or pattern_match or has_tool_keywords) and type_match
            
            if can_handle:
                self.logger.info(f"UserInterface can handle tension {tension.uid}: {tension.title}")
            
            return can_handle
            
        except Exception as e:
            self.logger.error(f"Error checking tension handleability: {str(e)}")
            return False
    
    async def analyze_tension_requirements(self, tension: Tension) -> Dict[str, Any]:
        """Phân tích requirements cụ thể cho UI/UX tension"""
        requirements = {
            "design_type": "unknown",
            "target_platforms": [],
            "complexity": "medium",
            "urgency": "normal",
            "deliverables": [],
            "tools_needed": [],
            "estimated_effort": 120,
            "success_criteria": [],
            "user_research_needed": False,
            "accessibility_requirements": [],
            "performance_targets": {}
        }
        
        try:
            description = tension.description.lower()
            title = tension.title.lower()
            combined_text = f"{title} {description}"
            
            # Xác định loại design work
            if any(pattern in combined_text for pattern in ["research", "user study", "usability test"]):
                requirements["design_type"] = "user_research"
                requirements["tools_needed"].extend(["survey_tools", "analytics", "testing_platform"])
                requirements["deliverables"].append("User Research Report")
                requirements["user_research_needed"] = True
                requirements["estimated_effort"] = 90
                
            elif any(pattern in combined_text for pattern in ["wireframe", "prototype", "mockup"]):
                requirements["design_type"] = "prototyping"
                requirements["tools_needed"].extend(["design_tool", "prototyping_tool"])
                requirements["deliverables"].append("Interactive Prototype")
                requirements["estimated_effort"] = 120
                
            elif any(pattern in combined_text for pattern in ["design system", "component library"]):
                requirements["design_type"] = "design_system"
                requirements["tools_needed"].extend(["design_tool", "component_library", "documentation_tool"])
                requirements["deliverables"].append("Design System")
                requirements["estimated_effort"] = 200
                
            elif any(pattern in combined_text for pattern in ["frontend", "component", "implementation"]):
                requirements["design_type"] = "frontend_development"
                requirements["tools_needed"].extend(["frontend_framework", "build_tools", "testing_framework"])
                requirements["deliverables"].append("Frontend Implementation")
                requirements["estimated_effort"] = 150
                
            elif any(pattern in combined_text for pattern in ["accessibility", "a11y", "wcag"]):
                requirements["design_type"] = "accessibility"
                requirements["tools_needed"].extend(["accessibility_tools", "screen_reader", "testing_tools"])
                requirements["deliverables"].append("Accessibility Audit & Fixes")
                requirements["estimated_effort"] = 60
                
            elif any(pattern in combined_text for pattern in ["performance", "speed", "loading", "optimization"]):
                requirements["design_type"] = "performance"
                requirements["tools_needed"].extend(["performance_tools", "profiling_tools", "optimization_tools"])
                requirements["deliverables"].append("Performance Optimization")
                requirements["estimated_effort"] = 45
                
            # Detect target platforms
            platform_keywords = {
                "web": ["web", "website", "browser"],
                "mobile": ["mobile", "ios", "android", "app"],
                "tablet": ["tablet", "ipad"],
                "desktop": ["desktop", "electron"]
            }
            
            for platform, keywords in platform_keywords.items():
                if any(keyword in combined_text for keyword in keywords):
                    requirements["target_platforms"].append(platform)
            
            if not requirements["target_platforms"]:
                requirements["target_platforms"] = ["web"]  # Default
            
            # Xác định complexity
            complexity_indicators = {
                "high": ["complex", "phức tạp", "advanced", "enterprise", "large scale", "multi-platform"],
                "low": ["simple", "đơn giản", "basic", "cơ bản", "quick", "nhanh", "minimal"]
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
            
            # Accessibility requirements
            if "accessibility" in combined_text or "a11y" in combined_text:
                requirements["accessibility_requirements"] = [
                    "WCAG 2.1 AA compliance",
                    "Keyboard navigation support",
                    "Screen reader compatibility",
                    "Color contrast compliance",
                    "Focus management"
                ]
            
            # Performance targets
            requirements["performance_targets"] = {
                "page_load_time": "< 3 seconds",
                "first_contentful_paint": "< 1.5 seconds",
                "lighthouse_score": "> 90",
                "core_web_vitals": "Pass"
            }
            
            # Success criteria
            requirements["success_criteria"] = [
                "Meets functional requirements",
                "Passes usability testing",
                "Achieves performance targets",
                "Complies với accessibility standards",
                "Consistent với design system"
            ]
            
            self.logger.info(f"Analyzed requirements for tension {tension.uid}: {requirements['design_type']}")
            
        except Exception as e:
            self.logger.error(f"Error analyzing tension requirements: {str(e)}")
        
        return requirements
    
    async def generate_specialized_solutions(self, tension: Tension, 
                                           requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Tạo solutions chuyên biệt cho UI/UX tasks"""
        solutions = []
        
        try:
            design_type = requirements.get("design_type", "unknown")
            
            if design_type == "user_research":
                solutions.extend(await self._generate_research_solutions(tension, requirements))
                
            elif design_type == "prototyping":
                solutions.extend(await self._generate_prototyping_solutions(tension, requirements))
                
            elif design_type == "design_system":
                solutions.extend(await self._generate_design_system_solutions(tension, requirements))
                
            elif design_type == "frontend_development":
                solutions.extend(await self._generate_frontend_solutions(tension, requirements))
                
            elif design_type == "accessibility":
                solutions.extend(await self._generate_accessibility_solutions(tension, requirements))
                
            elif design_type == "performance":
                solutions.extend(await self._generate_performance_solutions(tension, requirements))
                
            else:
                # Generic UI/UX solutions
                solutions.extend(await self._generate_generic_ui_solutions(tension, requirements))
            
            # Thêm metadata cho tất cả solutions
            for solution in solutions:
                solution.update({
                    "agent_template": "UserInterfaceAgent",
                    "domain": "ui_ux",
                    "estimated_effort": requirements.get("estimated_effort", 120),
                    "complexity": requirements.get("complexity", "medium"),
                    "target_platforms": requirements.get("target_platforms", []),
                    "accessibility_requirements": requirements.get("accessibility_requirements", []),
                    "success_criteria": requirements.get("success_criteria", [])
                })
            
            self.logger.info(f"Generated {len(solutions)} UI/UX solutions for tension {tension.uid}")
            
        except Exception as e:
            self.logger.error(f"Error generating solutions: {str(e)}")
        
        return solutions
    
    async def _generate_research_solutions(self, tension: Tension, 
                                         requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Tạo solutions cho user research"""
        return [
            {
                "title": "Comprehensive User Research Study",
                "description": "Thực hiện comprehensive user research để understand user needs và behaviors",
                "approach": "Mixed-Methods Research",
                "steps": [
                    "Define research objectives và questions",
                    "Design research methodology (surveys, interviews, observations)",
                    "Recruit representative user participants",
                    "Conduct user interviews và usability tests",
                    "Analyze data để identify patterns và insights",
                    "Create user personas và journey maps",
                    "Present findings với actionable recommendations"
                ],
                "tools": ["survey_platform", "interview_tools", "analytics", "data_analysis"],
                "deliverables": ["Research Report", "User Personas", "Journey Maps", "Recommendations"],
                "timeline": "3-4 weeks",
                "priority": 1
            },
            {
                "title": "Usability Testing & Optimization",
                "description": "Conduct usability testing để identify và fix UX issues",
                "approach": "Task-Based Usability Testing",
                "steps": [
                    "Define testing scenarios và tasks",
                    "Setup testing environment (remote/in-person)",
                    "Recruit target users for testing",
                    "Conduct moderated usability sessions",
                    "Analyze user behavior và feedback",
                    "Identify usability issues và improvements",
                    "Create prioritized improvement recommendations"
                ],
                "tools": ["usability_testing_platform", "screen_recording", "analytics"],
                "deliverables": ["Usability Report", "Issue Priority Matrix", "Improvement Roadmap"],
                "timeline": "2-3 weeks",
                "priority": 1
            }
        ]
    
    async def _generate_prototyping_solutions(self, tension: Tension,
                                            requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Tạo solutions cho prototyping"""
        return [
            {
                "title": "Interactive Prototype Development",
                "description": "Tạo high-fidelity interactive prototype để validate design concepts",
                "approach": "Design-First Prototyping",
                "steps": [
                    "Analyze requirements và user flows",
                    "Create wireframes cho key screens",
                    "Design high-fidelity mockups",
                    "Build interactive prototype với realistic interactions",
                    "Add micro-interactions và animations",
                    "Conduct prototype testing với users",
                    "Iterate based on feedback"
                ],
                "tools": ["figma", "framer", "principle", "invision"],
                "deliverables": ["Interactive Prototype", "Design Specifications", "User Flow Diagrams"],
                "timeline": "3-4 weeks",
                "priority": 1
            }
        ]
    
    async def _generate_design_system_solutions(self, tension: Tension,
                                              requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Tạo solutions cho design system"""
        return [
            {
                "title": "Comprehensive Design System",
                "description": "Tạo comprehensive design system với reusable components",
                "approach": "Atomic Design Methodology",
                "steps": [
                    "Audit existing designs để identify patterns",
                    "Define design tokens (colors, typography, spacing)",
                    "Create component library (atoms, molecules, organisms)",
                    "Design templates và page layouts",
                    "Build interactive component documentation",
                    "Create usage guidelines và best practices",
                    "Implement design system trong development"
                ],
                "tools": ["figma", "storybook", "design_tokens", "documentation_platform"],
                "deliverables": ["Design System", "Component Library", "Documentation", "Implementation Guide"],
                "timeline": "6-8 weeks",
                "priority": 1
            }
        ]
    
    async def _generate_frontend_solutions(self, tension: Tension,
                                         requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Tạo solutions cho frontend development"""
        return [
            {
                "title": "Frontend Component Implementation",
                "description": "Implement responsive frontend components với modern frameworks",
                "approach": "Component-Based Development",
                "steps": [
                    "Analyze design specifications",
                    "Setup development environment",
                    "Implement reusable components",
                    "Add responsive design và mobile optimization",
                    "Implement accessibility features",
                    "Add unit và integration tests",
                    "Optimize performance và bundle size"
                ],
                "tools": ["react", "vue", "angular", "css_framework", "testing_framework"],
                "deliverables": ["Frontend Components", "Test Suite", "Documentation", "Performance Report"],
                "timeline": "4-5 weeks",
                "priority": 1
            }
        ]
    
    async def _generate_accessibility_solutions(self, tension: Tension,
                                              requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Tạo solutions cho accessibility"""
        return [
            {
                "title": "Accessibility Audit & Remediation",
                "description": "Comprehensive accessibility audit và remediation để achieve WCAG compliance",
                "approach": "WCAG 2.1 AA Compliance",
                "steps": [
                    "Conduct automated accessibility scanning",
                    "Perform manual accessibility testing",
                    "Test với assistive technologies",
                    "Identify accessibility violations",
                    "Implement fixes cho identified issues",
                    "Add accessibility testing to CI/CD",
                    "Create accessibility guidelines"
                ],
                "tools": ["axe", "wave", "lighthouse", "screen_readers", "keyboard_testing"],
                "deliverables": ["Accessibility Audit Report", "Remediation Plan", "Testing Guidelines"],
                "timeline": "2-3 weeks",
                "priority": 1
            }
        ]
    
    async def _generate_performance_solutions(self, tension: Tension,
                                            requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Tạo solutions cho performance optimization"""
        return [
            {
                "title": "Frontend Performance Optimization",
                "description": "Optimize frontend performance để improve user experience",
                "approach": "Web Performance Best Practices",
                "steps": [
                    "Audit current performance metrics",
                    "Identify performance bottlenecks",
                    "Optimize images và media assets",
                    "Implement code splitting và lazy loading",
                    "Optimize CSS và JavaScript bundles",
                    "Add performance monitoring",
                    "Validate improvements với real user metrics"
                ],
                "tools": ["lighthouse", "webpagetest", "bundle_analyzer", "performance_monitoring"],
                "deliverables": ["Performance Audit", "Optimization Plan", "Monitoring Setup"],
                "timeline": "2-3 weeks",
                "priority": 1
            }
        ]
    
    async def _generate_generic_ui_solutions(self, tension: Tension,
                                           requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Tạo generic UI/UX solutions"""
        return [
            {
                "title": "UI/UX Improvement Initiative",
                "description": "Comprehensive UI/UX improvement based on user feedback",
                "approach": "User-Centered Design",
                "steps": [
                    "Gather user feedback và requirements",
                    "Conduct competitive analysis",
                    "Create improved design concepts",
                    "Build prototype cho validation",
                    "Test với target users",
                    "Implement approved designs",
                    "Monitor user satisfaction metrics"
                ],
                "tools": ["design_tool", "prototyping_tool", "user_testing", "analytics"],
                "deliverables": ["Design Improvements", "Prototype", "Implementation", "Metrics Report"],
                "timeline": "4-5 weeks",
                "priority": 1
            }
        ]
    
    async def execute_solution(self, solution: Dict[str, Any], 
                             context: Dict[str, Any]) -> Dict[str, Any]:
        """Thực thi UI/UX solution"""
        execution_result = {
            "status": "completed",
            "execution_time": datetime.now().isoformat(),
            "results": {},
            "deliverables_created": [],
            "next_steps": [],
            "metrics": {}
        }
        
        try:
            solution_title = solution.get("title", "Unknown Solution")
            self.logger.info(f"Executing UI/UX solution: {solution_title}")
            
            # Simulate solution execution
            await asyncio.sleep(2)  # Simulate design/development time
            
            # Mock results based on solution type
            if "research" in solution_title.lower():
                execution_result["results"] = {
                    "participants_interviewed": 15,
                    "insights_discovered": 23,
                    "personas_created": 4,
                    "user_satisfaction_improvement": 25.0
                }
                execution_result["deliverables_created"] = ["Research Report", "User Personas", "Journey Maps"]
                execution_result["metrics"] = {
                    "research_confidence": 92.0,
                    "actionability_score": 88.5
                }
                
            elif "prototype" in solution_title.lower():
                execution_result["results"] = {
                    "screens_prototyped": 12,
                    "interactions_designed": 35,
                    "user_flows_created": 8,
                    "validation_success_rate": 85.0
                }
                execution_result["deliverables_created"] = ["Interactive Prototype", "Design Specs", "User Flows"]
                execution_result["metrics"] = {
                    "prototype_fidelity": 95.0,
                    "user_feedback_score": 4.3
                }
                
            elif "design system" in solution_title.lower():
                execution_result["results"] = {
                    "components_created": 45,
                    "design_tokens_defined": 120,
                    "documentation_pages": 30,
                    "consistency_improvement": 40.0
                }
                execution_result["deliverables_created"] = ["Design System", "Component Library", "Documentation"]
                execution_result["metrics"] = {
                    "design_consistency": 95.0,
                    "developer_adoption": 78.0
                }
                
            elif "frontend" in solution_title.lower():
                execution_result["results"] = {
                    "components_implemented": 20,
                    "responsive_breakpoints": 4,
                    "performance_improvement": 30.0,
                    "accessibility_score": 92.0
                }
                execution_result["deliverables_created"] = ["Frontend Components", "Test Suite", "Documentation"]
                execution_result["metrics"] = {
                    "code_quality": 88.0,
                    "lighthouse_score": 94.0
                }
                
            elif "accessibility" in solution_title.lower():
                execution_result["results"] = {
                    "accessibility_issues_fixed": 28,
                    "wcag_compliance_score": 95.0,
                    "screen_reader_compatibility": 100.0,
                    "keyboard_navigation_coverage": 98.0
                }
                execution_result["deliverables_created"] = ["Accessibility Fixes", "Audit Report", "Guidelines"]
                execution_result["metrics"] = {
                    "accessibility_score": 95.0,
                    "compliance_level": "WCAG 2.1 AA"
                }
                
            elif "performance" in solution_title.lower():
                execution_result["results"] = {
                    "page_load_improvement": 45.0,
                    "bundle_size_reduction": 35.0,
                    "lighthouse_score": 94.0,
                    "core_web_vitals": "Pass"
                }
                execution_result["deliverables_created"] = ["Performance Optimizations", "Monitoring Setup", "Report"]
                execution_result["metrics"] = {
                    "performance_score": 94.0,
                    "user_experience_improvement": 32.0
                }
                
            else:
                execution_result["results"] = {
                    "design_improvements": 15,
                    "user_satisfaction_increase": 22.0,
                    "usability_score": 4.2,
                    "conversion_rate_improvement": 8.5
                }
                execution_result["deliverables_created"] = ["Design Improvements", "Implementation", "Metrics"]
                execution_result["metrics"] = {
                    "user_satisfaction": 4.2,
                    "usability_score": 85.0
                }
            
            execution_result["next_steps"] = [
                "Conduct user testing với implemented changes",
                "Monitor user engagement metrics",
                "Gather feedback từ stakeholders",
                "Plan next iteration improvements",
                "Update design system nếu applicable"
            ]
            
            self.logger.info(f"Successfully executed solution: {solution_title}")
            
        except Exception as e:
            execution_result["status"] = "failed"
            execution_result["error"] = str(e)
            self.logger.error(f"Error executing solution: {str(e)}")
        
        return execution_result
    
    async def _register_specialized_handlers(self) -> None:
        """Đăng ký specialized event handlers cho UserInterface"""
        # Đăng ký events liên quan đến UI/UX
        self.subscribe_to_event(EventType.USER_FEEDBACK_RECEIVED)
        self.subscribe_to_event(EventType.DESIGN_UPDATED)
        self.subscribe_to_event(EventType.USABILITY_TEST_COMPLETED)
        
    async def _initialize_specialized_components(self) -> None:
        """Khởi tạo UI/UX components"""
        self.logger.info("Initializing UserInterface specialized components")
        
        # Initialize design tools, user analytics, etc.
        # This would be implemented based on actual infrastructure
        
    async def _handle_specialized_event(self, event: SystemEvent) -> None:
        """Xử lý specialized events cho UserInterface"""
        if event.event_type == EventType.USER_FEEDBACK_RECEIVED:
            await self._handle_user_feedback(event)
        elif event.event_type == EventType.DESIGN_UPDATED:
            await self._handle_design_updated(event)
        elif event.event_type == EventType.USABILITY_TEST_COMPLETED:
            await self._handle_usability_test_completed(event)
    
    async def _handle_user_feedback(self, event: SystemEvent) -> None:
        """Xử lý sự kiện user feedback"""
        self.logger.info(f"User feedback received: {event.entity_id}")
        # Implement user feedback handling logic
        
    async def _handle_design_updated(self, event: SystemEvent) -> None:
        """Xử lý sự kiện design updated"""
        self.logger.info(f"Design updated: {event.entity_id}")
        # Implement design update handling logic
        
    async def _handle_usability_test_completed(self, event: SystemEvent) -> None:
        """Xử lý sự kiện usability test completed"""
        self.logger.info(f"Usability test completed: {event.entity_id}")
        # Implement usability test completion handling logic 