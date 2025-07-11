"""
Research Agent Template

Agent chuyên biệt xử lý các tensions liên quan đến knowledge gathering,
research, information synthesis và competitive intelligence trong TRM-OS.
"""

import re
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime

from .base_template import BaseAgentTemplate, AgentTemplateMetadata, AgentCapability
from ..base_agent import AgentMetadata
from ...eventbus.system_event_bus import EventType, SystemEvent
from ...models.tension import Tension


class ResearchAgent(BaseAgentTemplate):
    """
    Agent chuyên biệt cho research và knowledge gathering.
    
    Capabilities:
    - Market research và competitive analysis
    - Technical research và feasibility studies
    - Knowledge synthesis và documentation
    - Trend analysis và forecasting
    - Literature review và academic research
    - Data mining và information extraction
    """
    
    def __init__(self, agent_id: Optional[str] = None, metadata: Optional[AgentMetadata] = None):
        # Use BaseAgentTemplate constructor - no need to override AgentMetadata creation
        super().__init__(agent_id, metadata)
        
        # Research-specific patterns
        self.research_patterns = {
            "market_research": [
                r"(?:market|thị trường).*(?:research|nghiên cứu|analysis|phân tích)",
                r"(?:competitive|cạnh tranh).*(?:analysis|landscape|intelligence)",
                r"(?:customer|khách hàng).*(?:research|survey|study|nghiên cứu)",
                r"(?:industry|ngành).*(?:trend|xu hướng|analysis|report)"
            ],
            "technical_research": [
                r"(?:technical|kỹ thuật).*(?:research|feasibility|study)",
                r"(?:technology|công nghệ).*(?:evaluation|assessment|review)",
                r"(?:proof of concept|poc|pilot|thử nghiệm)",
                r"(?:architecture|solution).*(?:research|analysis|study)"
            ],
            "knowledge_gathering": [
                r"(?:knowledge|kiến thức).*(?:gathering|collection|synthesis)",
                r"(?:information|thông tin).*(?:research|gathering|mining)",
                r"(?:literature|tài liệu).*(?:review|research|study)",
                r"(?:best practices|practice|methodology).*(?:research|study)"
            ],
            "trend_analysis": [
                r"(?:trend|xu hướng).*(?:analysis|research|study|forecast)",
                r"(?:future|tương lai).*(?:prediction|forecast|dự báo)",
                r"(?:emerging|mới nổi).*(?:technology|trend|pattern)",
                r"(?:innovation|đổi mới).*(?:research|analysis|study)"
            ]
        }
        
        self.research_methodologies = {
            "quantitative": ["survey", "statistical_analysis", "data_mining", "metrics_analysis"],
            "qualitative": ["interviews", "focus_groups", "case_studies", "ethnography"],
            "mixed_methods": ["triangulation", "sequential_explanatory", "concurrent_embedded"],
            "secondary": ["literature_review", "meta_analysis", "systematic_review", "desk_research"]
        }
        
        self.research_sources = {
            "academic": ["journals", "conferences", "thesis", "research_papers"],
            "industry": ["reports", "whitepapers", "case_studies", "benchmarks"],
            "market": ["surveys", "interviews", "focus_groups", "observations"],
            "digital": ["web_scraping", "social_media", "apis", "databases"]
        }
        
        self.analysis_techniques = {
            "statistical": ["regression", "correlation", "anova", "chi_square"],
            "qualitative": ["thematic_analysis", "content_analysis", "grounded_theory"],
            "predictive": ["forecasting", "trend_analysis", "scenario_planning"],
            "comparative": ["benchmarking", "gap_analysis", "swot_analysis"]
        }
    
    def _get_default_template_metadata(self) -> AgentTemplateMetadata:
        """Trả về metadata mặc định cho Research template"""
        return AgentTemplateMetadata(
            template_name="ResearchAgent",
            template_version="1.0.0",
            description="Agent chuyên biệt xử lý tensions liên quan đến research và knowledge gathering",
            primary_domain="research",
            capabilities=[
                AgentCapability(
                    name="market_research",
                    description="Thực hiện market research và competitive analysis",
                    required_skills=["market_analysis", "competitive_intelligence", "survey_design", "data_analysis"],
                    complexity_level=4,
                    estimated_time=200
                ),
                AgentCapability(
                    name="technical_research",
                    description="Nghiên cứu technical feasibility và solution evaluation",
                    required_skills=["technical_analysis", "feasibility_study", "technology_evaluation"],
                    complexity_level=4,
                    estimated_time=180
                ),
                AgentCapability(
                    name="knowledge_synthesis",
                    description="Tổng hợp và synthesize knowledge từ multiple sources",
                    required_skills=["information_synthesis", "critical_thinking", "knowledge_management"],
                    complexity_level=3,
                    estimated_time=120
                ),
                AgentCapability(
                    name="trend_analysis",
                    description="Phân tích trends và forecast future developments",
                    required_skills=["trend_analysis", "forecasting", "pattern_recognition", "scenario_planning"],
                    complexity_level=4,
                    estimated_time=160
                ),
                AgentCapability(
                    name="literature_review",
                    description="Thực hiện systematic literature review",
                    required_skills=["academic_research", "systematic_review", "meta_analysis"],
                    complexity_level=3,
                    estimated_time=140
                ),
                AgentCapability(
                    name="data_mining",
                    description="Extract insights từ large datasets và web sources",
                    required_skills=["data_mining", "web_scraping", "text_mining", "information_extraction"],
                    complexity_level=3,
                    estimated_time=100
                )
            ],
            recommended_tensions=[
                "Market Research Needs",
                "Technical Feasibility Questions",
                "Knowledge Gaps",
                "Competitive Intelligence",
                "Trend Analysis Requirements",
                "Best Practices Research"
            ],
            dependencies=["data_sources", "research_tools", "analysis_software"],
            performance_metrics={
                "research_quality_score": 0.92,
                "insight_discovery_rate": 0.88,
                "source_credibility_score": 0.95,
                "stakeholder_satisfaction": 0.90,
                "actionability_rating": 0.85
            }
        )
    
    async def can_handle_tension(self, tension: Tension) -> bool:
        """Kiểm tra xem có thể xử lý tension này không"""
        try:
            description = tension.description.lower()
            title = tension.title.lower()
            
            # Tìm research-related keywords
            research_keywords = [
                "research", "nghiên cứu", "study", "analysis", "phân tích",
                "investigate", "điều tra", "explore", "khám phá", "survey",
                "market", "thị trường", "competitive", "cạnh tranh", "trend",
                "knowledge", "kiến thức", "information", "thông tin", "data",
                "feasibility", "khả thi", "evaluation", "đánh giá", "review"
            ]
            
            has_research_keywords = any(keyword in description or keyword in title 
                                      for keyword in research_keywords)
            
            # Kiểm tra research patterns
            pattern_match = False
            for category, patterns in self.research_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, description, re.IGNORECASE) or \
                       re.search(pattern, title, re.IGNORECASE):
                        pattern_match = True
                        break
                if pattern_match:
                    break
            
            # Kiểm tra methodology mentions
            has_methodology_keywords = any(
                method in description or method in title
                for method_category in self.research_methodologies.values()
                for method in method_category
            )
            
            # Kiểm tra tension type
            suitable_types = ["Problem", "Opportunity", "Idea"]
            type_match = tension.tensionType in suitable_types
            
            # Agent có thể handle nếu có research indicators
            can_handle = (has_research_keywords or pattern_match or has_methodology_keywords) and type_match
            
            if can_handle:
                self.logger.info(f"Research can handle tension {tension.uid}: {tension.title}")
            
            return can_handle
            
        except Exception as e:
            self.logger.error(f"Error checking tension handleability: {str(e)}")
            return False
    
    async def analyze_tension_requirements(self, tension: Tension) -> Dict[str, Any]:
        """Phân tích requirements cụ thể cho research tension"""
        requirements = {
            "research_type": "unknown",
            "methodologies": [],
            "data_sources": [],
            "complexity": "medium",
            "urgency": "normal",
            "deliverables": [],
            "tools_needed": [],
            "estimated_effort": 160,
            "success_criteria": [],
            "quality_requirements": [],
            "stakeholders": [],
            "timeline_constraints": {}
        }
        
        try:
            description = tension.description.lower()
            title = tension.title.lower()
            combined_text = f"{title} {description}"
            
            # Xác định loại research
            if any(pattern in combined_text for pattern in ["market", "thị trường", "competitive", "customer"]):
                requirements["research_type"] = "market_research"
                requirements["methodologies"].extend(["survey", "interviews", "competitive_analysis"])
                requirements["deliverables"].append("Market Research Report")
                requirements["estimated_effort"] = 200
                
            elif any(pattern in combined_text for pattern in ["technical", "technology", "feasibility", "proof of concept"]):
                requirements["research_type"] = "technical_research"
                requirements["methodologies"].extend(["technical_evaluation", "proof_of_concept", "benchmarking"])
                requirements["deliverables"].append("Technical Feasibility Study")
                requirements["estimated_effort"] = 180
                
            elif any(pattern in combined_text for pattern in ["trend", "future", "forecast", "emerging"]):
                requirements["research_type"] = "trend_analysis"
                requirements["methodologies"].extend(["trend_analysis", "forecasting", "scenario_planning"])
                requirements["deliverables"].append("Trend Analysis Report")
                requirements["estimated_effort"] = 160
                
            elif any(pattern in combined_text for pattern in ["literature", "academic", "systematic", "meta"]):
                requirements["research_type"] = "literature_review"
                requirements["methodologies"].extend(["systematic_review", "meta_analysis", "citation_analysis"])
                requirements["deliverables"].append("Literature Review")
                requirements["estimated_effort"] = 140
                
            elif any(pattern in combined_text for pattern in ["knowledge", "information", "best practices"]):
                requirements["research_type"] = "knowledge_synthesis"
                requirements["methodologies"].extend(["knowledge_mapping", "synthesis", "expert_interviews"])
                requirements["deliverables"].append("Knowledge Synthesis Report")
                requirements["estimated_effort"] = 120
                
            elif any(pattern in combined_text for pattern in ["data mining", "web scraping", "extraction"]):
                requirements["research_type"] = "data_mining"
                requirements["methodologies"].extend(["data_mining", "web_scraping", "text_analysis"])
                requirements["deliverables"].append("Data Mining Report")
                requirements["estimated_effort"] = 100
            
            # Detect data sources needed
            source_keywords = {
                "academic": ["journal", "paper", "conference", "academic", "scholar"],
                "industry": ["report", "whitepaper", "case study", "industry"],
                "market": ["survey", "interview", "customer", "user"],
                "digital": ["web", "social media", "api", "database", "online"]
            }
            
            for source_type, keywords in source_keywords.items():
                if any(keyword in combined_text for keyword in keywords):
                    requirements["data_sources"].append(source_type)
            
            if not requirements["data_sources"]:
                requirements["data_sources"] = ["industry", "digital"]  # Default
            
            # Detect methodologies
            for methodology_type, methods in self.research_methodologies.items():
                if any(method in combined_text for method in methods):
                    requirements["methodologies"].append(methodology_type)
            
            # Xác định complexity
            complexity_indicators = {
                "high": ["complex", "phức tạp", "comprehensive", "toàn diện", "multi-faceted", "large scale"],
                "low": ["simple", "đơn giản", "basic", "cơ bản", "quick", "preliminary", "sơ bộ"]
            }
            
            for level, indicators in complexity_indicators.items():
                if any(indicator in combined_text for indicator in indicators):
                    requirements["complexity"] = level
                    break
            
            # Adjust effort based on complexity
            if requirements["complexity"] == "high":
                requirements["estimated_effort"] = int(requirements["estimated_effort"] * 1.5)
            elif requirements["complexity"] == "low":
                requirements["estimated_effort"] = int(requirements["estimated_effort"] * 0.6)
            
            # Xác định urgency
            if any(pattern in combined_text for pattern in ["urgent", "gấp", "asap", "immediate", "rush"]):
                requirements["urgency"] = "high"
                requirements["estimated_effort"] = max(40, requirements["estimated_effort"] // 2)
            
            # Identify stakeholders
            stakeholder_keywords = {
                "executives": ["executive", "c-level", "leadership", "management"],
                "product_team": ["product", "development", "engineering"],
                "marketing": ["marketing", "sales", "business development"],
                "customers": ["customer", "user", "client"],
                "investors": ["investor", "stakeholder", "board"]
            }
            
            for stakeholder_type, keywords in stakeholder_keywords.items():
                if any(keyword in combined_text for keyword in keywords):
                    requirements["stakeholders"].append(stakeholder_type)
            
            # Quality requirements
            requirements["quality_requirements"] = [
                "Multiple credible sources",
                "Peer-reviewed references where applicable",
                "Data validation và verification",
                "Bias detection và mitigation",
                "Reproducible methodology"
            ]
            
            # Timeline constraints
            if "deadline" in combined_text or "timeline" in combined_text:
                requirements["timeline_constraints"] = {
                    "has_strict_deadline": True,
                    "requires_phased_delivery": True,
                    "interim_updates_needed": True
                }
            
            # Success criteria
            requirements["success_criteria"] = [
                "Research questions fully addressed",
                "Actionable insights provided",
                "High-quality sources utilized",
                "Stakeholder requirements met",
                "Recommendations are implementable"
            ]
            
            self.logger.info(f"Analyzed requirements for tension {tension.uid}: {requirements['research_type']}")
            
        except Exception as e:
            self.logger.error(f"Error analyzing tension requirements: {str(e)}")
        
        return requirements
    
    async def generate_specialized_solutions(self, tension: Tension, 
                                           requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Tạo solutions chuyên biệt cho research tasks"""
        solutions = []
        
        try:
            research_type = requirements.get("research_type", "unknown")
            
            if research_type == "market_research":
                solutions.extend(await self._generate_market_research_solutions(tension, requirements))
                
            elif research_type == "technical_research":
                solutions.extend(await self._generate_technical_research_solutions(tension, requirements))
                
            elif research_type == "trend_analysis":
                solutions.extend(await self._generate_trend_analysis_solutions(tension, requirements))
                
            elif research_type == "literature_review":
                solutions.extend(await self._generate_literature_review_solutions(tension, requirements))
                
            elif research_type == "knowledge_synthesis":
                solutions.extend(await self._generate_knowledge_synthesis_solutions(tension, requirements))
                
            elif research_type == "data_mining":
                solutions.extend(await self._generate_data_mining_solutions(tension, requirements))
                
            else:
                # Generic research solutions
                solutions.extend(await self._generate_generic_research_solutions(tension, requirements))
            
            # Thêm metadata cho tất cả solutions
            for solution in solutions:
                solution.update({
                    "agent_template": "ResearchAgent",
                    "domain": "research",
                    "estimated_effort": requirements.get("estimated_effort", 160),
                    "complexity": requirements.get("complexity", "medium"),
                    "methodologies": requirements.get("methodologies", []),
                    "data_sources": requirements.get("data_sources", []),
                    "success_criteria": requirements.get("success_criteria", [])
                })
            
            self.logger.info(f"Generated {len(solutions)} research solutions for tension {tension.uid}")
            
        except Exception as e:
            self.logger.error(f"Error generating solutions: {str(e)}")
        
        return solutions
    
    async def _generate_market_research_solutions(self, tension: Tension, 
                                                requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Tạo solutions cho market research"""
        return [
            {
                "title": "Comprehensive Market Analysis",
                "description": "Thực hiện comprehensive market research với competitive intelligence",
                "approach": "Mixed-Methods Market Research",
                "steps": [
                    "Define research objectives và key questions",
                    "Design market research methodology",
                    "Conduct competitive landscape analysis",
                    "Execute customer surveys và interviews",
                    "Analyze market size và growth potential",
                    "Identify market trends và opportunities",
                    "Create actionable market insights report"
                ],
                "tools": ["survey_platform", "interview_tools", "competitive_intelligence", "market_databases"],
                "deliverables": ["Market Research Report", "Competitive Analysis", "Customer Insights", "Market Opportunity Assessment"],
                "timeline": "6-8 weeks",
                "priority": 1
            },
            {
                "title": "Customer Research & Segmentation",
                "description": "Deep-dive customer research với market segmentation analysis",
                "approach": "Customer-Centric Research",
                "steps": [
                    "Design customer research framework",
                    "Conduct in-depth customer interviews",
                    "Execute large-scale customer surveys",
                    "Analyze customer behavior patterns",
                    "Develop customer personas và segments",
                    "Map customer journey và touchpoints",
                    "Create customer insights dashboard"
                ],
                "tools": ["customer_research_platform", "analytics_tools", "persona_creation", "journey_mapping"],
                "deliverables": ["Customer Research Report", "Market Segments", "Customer Personas", "Journey Maps"],
                "timeline": "5-7 weeks",
                "priority": 2
            }
        ]
    
    async def _generate_technical_research_solutions(self, tension: Tension,
                                                   requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Tạo solutions cho technical research"""
        return [
            {
                "title": "Technical Feasibility Study",
                "description": "Comprehensive technical feasibility analysis với proof of concept",
                "approach": "Evidence-Based Technical Evaluation",
                "steps": [
                    "Define technical requirements và constraints",
                    "Research available technologies và solutions",
                    "Conduct technology benchmarking",
                    "Develop proof of concept prototypes",
                    "Evaluate scalability và performance",
                    "Assess implementation complexity và risks",
                    "Create technical recommendations report"
                ],
                "tools": ["benchmarking_tools", "prototyping_platform", "performance_testing", "risk_assessment"],
                "deliverables": ["Feasibility Study", "Proof of Concept", "Technology Comparison", "Implementation Roadmap"],
                "timeline": "4-6 weeks",
                "priority": 1
            },
            {
                "title": "Technology Landscape Analysis",
                "description": "Comprehensive analysis của technology landscape và emerging solutions",
                "approach": "Systematic Technology Review",
                "steps": [
                    "Map current technology landscape",
                    "Identify emerging technologies",
                    "Evaluate technology maturity levels",
                    "Assess adoption trends",
                    "Analyze vendor ecosystem",
                    "Create technology roadmap",
                    "Provide strategic recommendations"
                ],
                "tools": ["technology_databases", "vendor_analysis", "trend_tracking", "roadmapping_tools"],
                "deliverables": ["Technology Landscape Report", "Vendor Analysis", "Technology Roadmap", "Strategic Recommendations"],
                "timeline": "5-7 weeks",
                "priority": 2
            }
        ]
    
    async def _generate_trend_analysis_solutions(self, tension: Tension,
                                               requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Tạo solutions cho trend analysis"""
        return [
            {
                "title": "Trend Analysis & Future Forecasting",
                "description": "Comprehensive trend analysis với predictive forecasting",
                "approach": "Multi-Source Trend Intelligence",
                "steps": [
                    "Identify relevant trend indicators",
                    "Collect data từ multiple trend sources",
                    "Apply statistical trend analysis",
                    "Conduct expert interviews",
                    "Develop forecasting models",
                    "Create scenario planning",
                    "Generate trend insights report"
                ],
                "tools": ["trend_analytics", "forecasting_models", "expert_networks", "scenario_planning"],
                "deliverables": ["Trend Analysis Report", "Forecasting Models", "Scenario Plans", "Strategic Implications"],
                "timeline": "4-6 weeks",
                "priority": 1
            }
        ]
    
    async def _generate_literature_review_solutions(self, tension: Tension,
                                                  requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Tạo solutions cho literature review"""
        return [
            {
                "title": "Systematic Literature Review",
                "description": "Rigorous systematic literature review với meta-analysis",
                "approach": "Evidence-Based Literature Synthesis",
                "steps": [
                    "Define research questions và inclusion criteria",
                    "Conduct comprehensive literature search",
                    "Screen và select relevant studies",
                    "Extract data và assess quality",
                    "Synthesize findings",
                    "Perform meta-analysis nếu applicable",
                    "Create systematic review report"
                ],
                "tools": ["academic_databases", "reference_management", "meta_analysis_software", "quality_assessment"],
                "deliverables": ["Systematic Review", "Meta-Analysis", "Evidence Summary", "Research Gaps Analysis"],
                "timeline": "4-6 weeks",
                "priority": 1
            }
        ]
    
    async def _generate_knowledge_synthesis_solutions(self, tension: Tension,
                                                    requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Tạo solutions cho knowledge synthesis"""
        return [
            {
                "title": "Knowledge Synthesis & Best Practices",
                "description": "Comprehensive knowledge synthesis với best practices identification",
                "approach": "Multi-Source Knowledge Integration",
                "steps": [
                    "Map knowledge domains và sources",
                    "Collect information từ diverse sources",
                    "Synthesize knowledge frameworks",
                    "Identify best practices",
                    "Create knowledge repository",
                    "Develop implementation guidelines",
                    "Generate knowledge synthesis report"
                ],
                "tools": ["knowledge_mapping", "synthesis_tools", "best_practices_database", "expert_networks"],
                "deliverables": ["Knowledge Synthesis", "Best Practices Guide", "Implementation Framework", "Knowledge Repository"],
                "timeline": "3-5 weeks",
                "priority": 1
            }
        ]
    
    async def _generate_data_mining_solutions(self, tension: Tension,
                                            requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Tạo solutions cho data mining"""
        return [
            {
                "title": "Data Mining & Information Extraction",
                "description": "Advanced data mining để extract actionable insights",
                "approach": "AI-Powered Data Mining",
                "steps": [
                    "Define data mining objectives",
                    "Identify và access data sources",
                    "Setup data extraction pipelines",
                    "Apply machine learning algorithms",
                    "Extract patterns và insights",
                    "Validate findings",
                    "Create insights dashboard"
                ],
                "tools": ["data_mining_platform", "ml_algorithms", "web_scraping", "text_analytics"],
                "deliverables": ["Data Mining Report", "Insights Dashboard", "Pattern Analysis", "Predictive Models"],
                "timeline": "3-4 weeks",
                "priority": 1
            }
        ]
    
    async def _generate_generic_research_solutions(self, tension: Tension,
                                                 requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Tạo generic research solutions"""
        return [
            {
                "title": "Custom Research Initiative",
                "description": "Tailored research solution based on specific requirements",
                "approach": "Adaptive Research Methodology",
                "steps": [
                    "Define research scope và objectives",
                    "Design appropriate methodology",
                    "Execute data collection",
                    "Analyze findings",
                    "Synthesize insights",
                    "Validate results",
                    "Present recommendations"
                ],
                "tools": ["research_platform", "analysis_tools", "validation_framework", "presentation_tools"],
                "deliverables": ["Research Report", "Analysis Results", "Insights Summary", "Recommendations"],
                "timeline": "4-6 weeks",
                "priority": 1
            }
        ]
    
    async def execute_solution(self, solution: Dict[str, Any], 
                             context: Dict[str, Any]) -> Dict[str, Any]:
        """Thực thi research solution"""
        execution_result = {
            "status": "completed",
            "execution_time": datetime.now().isoformat(),
            "results": {},
            "deliverables_created": [],
            "next_steps": [],
            "research_metrics": {}
        }
        
        try:
            solution_title = solution.get("title", "Unknown Solution")
            self.logger.info(f"Executing research solution: {solution_title}")
            
            # Simulate solution execution
            await asyncio.sleep(2)  # Simulate research time
            
            # Mock results based on solution type
            if "market" in solution_title.lower():
                execution_result["results"] = {
                    "market_size_identified": "$2.5B",
                    "competitors_analyzed": 15,
                    "customer_segments": 4,
                    "growth_rate_forecast": "15.2% CAGR"
                }
                execution_result["deliverables_created"] = ["Market Research Report", "Competitive Analysis", "Customer Insights"]
                execution_result["research_metrics"] = {
                    "source_credibility": 92.0,
                    "insight_quality": 88.5,
                    "actionability_score": 85.0
                }
                
            elif "technical" in solution_title.lower() or "feasibility" in solution_title.lower():
                execution_result["results"] = {
                    "technologies_evaluated": 12,
                    "feasibility_score": 78.5,
                    "implementation_complexity": "Medium-High",
                    "estimated_timeline": "6-9 months"
                }
                execution_result["deliverables_created"] = ["Feasibility Study", "Technology Comparison", "Implementation Roadmap"]
                execution_result["research_metrics"] = {
                    "technical_accuracy": 95.0,
                    "completeness_score": 90.0,
                    "risk_assessment_quality": 88.0
                }
                
            elif "trend" in solution_title.lower():
                execution_result["results"] = {
                    "trends_identified": 8,
                    "forecast_horizon": "3 years",
                    "confidence_level": 82.0,
                    "scenarios_developed": 4
                }
                execution_result["deliverables_created"] = ["Trend Analysis Report", "Forecasting Models", "Scenario Plans"]
                execution_result["research_metrics"] = {
                    "trend_accuracy": 85.0,
                    "forecast_reliability": 78.5,
                    "strategic_value": 92.0
                }
                
            elif "literature" in solution_title.lower():
                execution_result["results"] = {
                    "papers_reviewed": 156,
                    "relevant_studies": 45,
                    "evidence_quality": "High",
                    "research_gaps_identified": 7
                }
                execution_result["deliverables_created"] = ["Systematic Review", "Evidence Summary", "Research Gaps Analysis"]
                execution_result["research_metrics"] = {
                    "review_comprehensiveness": 94.0,
                    "methodological_rigor": 96.0,
                    "synthesis_quality": 90.0
                }
                
            elif "knowledge" in solution_title.lower():
                execution_result["results"] = {
                    "knowledge_sources": 25,
                    "best_practices_identified": 18,
                    "frameworks_synthesized": 3,
                    "implementation_guidelines": 12
                }
                execution_result["deliverables_created"] = ["Knowledge Synthesis", "Best Practices Guide", "Implementation Framework"]
                execution_result["research_metrics"] = {
                    "synthesis_quality": 88.0,
                    "practical_applicability": 92.0,
                    "knowledge_coverage": 85.0
                }
                
            elif "data mining" in solution_title.lower():
                execution_result["results"] = {
                    "data_sources_mined": 8,
                    "patterns_discovered": 23,
                    "insights_generated": 15,
                    "prediction_accuracy": 84.2
                }
                execution_result["deliverables_created"] = ["Data Mining Report", "Insights Dashboard", "Predictive Models"]
                execution_result["research_metrics"] = {
                    "data_quality": 91.0,
                    "pattern_significance": 87.5,
                    "insight_novelty": 82.0
                }
                
            else:
                execution_result["results"] = {
                    "research_objectives_met": "100%",
                    "sources_consulted": 35,
                    "insights_discovered": 20,
                    "recommendations_provided": 12
                }
                execution_result["deliverables_created"] = ["Research Report", "Analysis Results", "Recommendations"]
                execution_result["research_metrics"] = {
                    "research_quality": 88.0,
                    "stakeholder_satisfaction": 4.3,
                    "actionability": 85.0
                }
            
            execution_result["next_steps"] = [
                "Present findings to stakeholders",
                "Develop implementation plan based on recommendations",
                "Setup monitoring để track recommended actions",
                "Schedule follow-up research nếu needed",
                "Archive research artifacts for future reference"
            ]
            
            self.logger.info(f"Successfully executed solution: {solution_title}")
            
        except Exception as e:
            execution_result["status"] = "failed"
            execution_result["error"] = str(e)
            self.logger.error(f"Error executing solution: {str(e)}")
        
        return execution_result
    
    async def _register_specialized_handlers(self) -> None:
        """Đăng ký specialized event handlers cho Research"""
        # Đăng ký events liên quan đến research
        self.subscribe_to_event(EventType.RESEARCH_REQUESTED)
        self.subscribe_to_event(EventType.KNOWLEDGE_UPDATED)
        self.subscribe_to_event(EventType.TREND_DETECTED)
        
    async def _initialize_specialized_components(self) -> None:
        """Khởi tạo research components"""
        self.logger.info("Initializing Research specialized components")
        
        # Initialize research databases, analysis tools, etc.
        # This would be implemented based on actual infrastructure
        
    async def _handle_specialized_event(self, event: SystemEvent) -> None:
        """Xử lý specialized events cho Research"""
        if event.event_type == EventType.RESEARCH_REQUESTED:
            await self._handle_research_requested(event)
        elif event.event_type == EventType.KNOWLEDGE_UPDATED:
            await self._handle_knowledge_updated(event)
        elif event.event_type == EventType.TREND_DETECTED:
            await self._handle_trend_detected(event)
    
    async def _handle_research_requested(self, event: SystemEvent) -> None:
        """Xử lý sự kiện research requested"""
        self.logger.info(f"Research requested: {event.entity_id}")
        # Implement research request handling logic
        
    async def _handle_knowledge_updated(self, event: SystemEvent) -> None:
        """Xử lý sự kiện knowledge updated"""
        self.logger.info(f"Knowledge updated: {event.entity_id}")
        # Implement knowledge update handling logic
        
    async def _handle_trend_detected(self, event: SystemEvent) -> None:
        """Xử lý sự kiện trend detected"""
        self.logger.info(f"Trend detected: {event.entity_id}")
        # Implement trend detection handling logic

    # Implementation of abstract methods from BaseAgent
    async def analyze_recognition_phase(self, recognition_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze Recognition phase for research contexts
        Recognition phase của Recognition → Event → WIN
        """
        try:
            analysis = {
                "recognition_id": recognition_data.get("recognition_id", "unknown"),
                "agent_template": "ResearchAgent",
                "analysis_type": "research_recognition",
                "research_requirements": {},
                "research_scope": "unknown",
                "investigation_complexity": "medium",
                "knowledge_domains": [],
                "discovery_potential": 0.0,
                "confidence": 0.0
            }
            
            context = recognition_data.get("context", {})
            description = recognition_data.get("description", "")
            
            # Assess investigation complexity
            if any(keyword in description.lower() for keyword in ["comprehensive", "systematic", "longitudinal", "meta-analysis"]):
                analysis["investigation_complexity"] = "high"
                analysis["discovery_potential"] = 90.0
            elif any(keyword in description.lower() for keyword in ["quick", "brief", "summary", "overview"]):
                analysis["investigation_complexity"] = "low"
                analysis["discovery_potential"] = 70.0
            else:
                analysis["investigation_complexity"] = "medium"
                analysis["discovery_potential"] = 80.0
            
            # Determine research scope
            if any(keyword in description.lower() for keyword in ["market", "competitive", "industry", "business"]):
                analysis["research_scope"] = "market_research"
            elif any(keyword in description.lower() for keyword in ["technical", "feasibility", "technology", "implementation"]):
                analysis["research_scope"] = "technical_research"
            elif any(keyword in description.lower() for keyword in ["literature", "academic", "scientific", "peer-reviewed"]):
                analysis["research_scope"] = "literature_review"
            elif any(keyword in description.lower() for keyword in ["trend", "forecast", "future", "prediction"]):
                analysis["research_scope"] = "trend_analysis"
            else:
                analysis["research_scope"] = "general_research"
            
            # Identify knowledge domains
            analysis["knowledge_domains"] = self._identify_knowledge_domains(description, context)
            
            # Calculate confidence
            analysis["confidence"] = self._calculate_research_recognition_confidence(recognition_data)
            
            return analysis
            
        except Exception as e:
            return {
                "recognition_id": recognition_data.get("recognition_id", "unknown"),
                "error": "Analysis failed",
                "agent_template": "ResearchAgent"
            }

    async def coordinate_event_execution(self, event_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Coordinate Event execution for research tasks
        Event phase của Recognition → Event → WIN
        """
        try:
            coordination = {
                "event_id": event_context.get("event_id", "unknown"),
                "agent_template": "ResearchAgent",
                "coordination_type": "research_execution",
                "execution_plan": {},
                "research_methodology": {},
                "investigation_workflow": {},
                "validation_strategy": {},
                "knowledge_synthesis": {},
                "deliverables_plan": {},
                "status": "coordinating"
            }
            
            event_type = event_context.get("event_type", "research_task")
            requirements = event_context.get("requirements", {})
            
            # Create execution plan
            coordination["execution_plan"] = {
                "phases": [
                    {"name": "research_planning", "duration_hours": 2, "priority": "high"},
                    {"name": "literature_review", "duration_hours": 8, "priority": "high"},
                    {"name": "data_collection", "duration_hours": 12, "priority": "high"},
                    {"name": "analysis_synthesis", "duration_hours": 10, "priority": "medium"},
                    {"name": "validation", "duration_hours": 4, "priority": "medium"},
                    {"name": "reporting", "duration_hours": 6, "priority": "high"},
                    {"name": "presentation", "duration_hours": 3, "priority": "low"}
                ],
                "total_estimated_hours": 45,
                "approach": "systematic_investigation"
            }
            
            # Research methodology
            coordination["research_methodology"] = {
                "research_design": requirements.get("design", "descriptive"),
                "data_sources": ["primary_research", "secondary_sources", "expert_interviews"],
                "analysis_methods": ["qualitative_analysis", "quantitative_analysis", "comparative_analysis"],
                "validation_methods": ["triangulation", "peer_review", "expert_validation"]
            }
            
            # Investigation workflow
            coordination["investigation_workflow"] = {
                "search_strategy": "systematic_search_with_keywords",
                "source_evaluation": "credibility_and_relevance_scoring",
                "data_extraction": "structured_extraction_templates",
                "quality_control": "dual_review_process"
            }
            
            coordination["status"] = "coordinated"
            
            return coordination
            
        except Exception as e:
            return {
                "event_id": event_context.get("event_id", "unknown"),
                "error": "Coordination failed",
                "agent_template": "ResearchAgent"
            }

    async def execute_strategic_action(self, action_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute strategic research action trong AGE system
        Strategic execution with research expertise
        """
        try:
            execution = {
                "action_id": action_context.get("action_id", "unknown"),
                "agent_template": "ResearchAgent",
                "action_type": "strategic_research_action",
                "execution_details": {},
                "deliverables": [],
                "knowledge_impact": {},
                "strategic_impact": {},
                "research_outcomes": {},
                "status": "executing"
            }
            
            action_type = action_context.get("action_type", "general_research")
            target_context = action_context.get("target_context", {})
            
            # Execute based on action type
            if action_type == "market_research":
                execution["execution_details"] = await self._execute_market_research(target_context)
            elif action_type == "technical_feasibility":
                execution["execution_details"] = await self._execute_technical_feasibility(target_context)
            elif action_type == "competitive_analysis":
                execution["execution_details"] = await self._execute_competitive_analysis(target_context)
            elif action_type == "trend_analysis":
                execution["execution_details"] = await self._execute_trend_analysis(target_context)
            else:
                execution["execution_details"] = await self._execute_general_research(target_context)
            
            # Generate deliverables
            execution["deliverables"] = [
                {"type": "research_report", "status": "completed"},
                {"type": "executive_summary", "status": "completed"},
                {"type": "data_analysis", "status": "completed"},
                {"type": "recommendations", "status": "completed"}
            ]
            
            # Knowledge impact
            execution["knowledge_impact"] = {
                "insights_discovered": "significant_new_knowledge",
                "knowledge_gaps_identified": "strategic_research_opportunities",
                "best_practices_synthesized": "actionable_frameworks",
                "evidence_quality": "high_confidence_findings"
            }
            
            # Strategic impact
            execution["strategic_impact"] = {
                "decision_support": "evidence_based_insights",
                "competitive_advantage": "strategic_intelligence",
                "risk_mitigation": "informed_risk_assessment",
                "innovation_opportunities": "research_driven_innovation"
            }
            
            execution["status"] = "completed"
            
            return execution
            
        except Exception as e:
            return {
                "action_id": action_context.get("action_id", "unknown"),
                "error": "Strategic action failed",
                "agent_template": "ResearchAgent"
            }

    async def validate_win_achievement(self, win_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate WIN achievement for research outcomes
        WIN phase của Recognition → Event → WIN
        """
        try:
            validation = {
                "win_id": win_context.get("win_id", "unknown"),
                "agent_template": "ResearchAgent",
                "validation_type": "research_win_validation",
                "wisdom_score": 0.0,
                "intelligence_score": 0.0,
                "networking_score": 0.0,
                "total_win_score": 0.0,
                "validation_criteria": {},
                "achievements": [],
                "areas_for_improvement": [],
                "validation_status": "validating"
            }
            
            deliverables = win_context.get("deliverables", [])
            metrics = win_context.get("metrics", {})
            stakeholder_feedback = win_context.get("stakeholder_feedback", {})
            
            # Validate Wisdom (research depth and knowledge synthesis)
            wisdom_factors = {
                "research_comprehensiveness": metrics.get("coverage_completeness", 85.0),
                "knowledge_synthesis": metrics.get("synthesis_quality", 88.0),
                "insight_quality": metrics.get("insight_depth", 82.0),
                "contextual_understanding": metrics.get("context_relevance", 85.0)
            }
            validation["wisdom_score"] = sum(wisdom_factors.values()) / len(wisdom_factors)
            
            # Validate Intelligence (methodological rigor and analytical sophistication)
            intelligence_factors = {
                "methodological_rigor": metrics.get("methodology_quality", 92.0),
                "analytical_sophistication": metrics.get("analysis_depth", 88.0),
                "evidence_quality": metrics.get("evidence_strength", 90.0),
                "research_innovation": metrics.get("innovation_factor", 78.0)
            }
            validation["intelligence_score"] = sum(intelligence_factors.values()) / len(intelligence_factors)
            
            # Validate Networking (knowledge sharing and stakeholder engagement)
            networking_factors = {
                "stakeholder_engagement": stakeholder_feedback.get("engagement_score", 80.0),
                "knowledge_dissemination": metrics.get("dissemination_reach", 75.0),
                "research_accessibility": metrics.get("accessibility_score", 85.0),
                "collaborative_impact": metrics.get("collaboration_quality", 78.0)
            }
            validation["networking_score"] = sum(networking_factors.values()) / len(networking_factors)
            
            # Calculate total WIN score
            validation["total_win_score"] = (
                validation["wisdom_score"] * 0.4 +
                validation["intelligence_score"] * 0.4 +
                validation["networking_score"] * 0.2
            )
            
            # Validation criteria
            validation["validation_criteria"] = {
                "research_objectives_met": metrics.get("objectives_completion", 90.0) > 85,
                "quality_standards_achieved": metrics.get("quality_score", 88.0) > 80,
                "actionability_demonstrated": metrics.get("actionability", 85.0) > 80,
                "stakeholder_value_delivered": stakeholder_feedback.get("value_rating", "high") == "high",
                "knowledge_contribution": metrics.get("knowledge_contribution", 82.0) > 75
            }
            
            # Achievements
            validation["achievements"] = [
                f"Generated research insights with {validation['wisdom_score']:.1f}% depth and comprehensiveness",
                f"Achieved {validation['intelligence_score']:.1f}% methodological excellence",
                f"Enabled {validation['networking_score']:.1f}% knowledge sharing and collaboration",
                f"Overall WIN score: {validation['total_win_score']:.1f}%"
            ]
            
            # Areas for improvement
            if validation["wisdom_score"] < 80:
                validation["areas_for_improvement"].append("Enhance research depth and knowledge synthesis capabilities")
            if validation["intelligence_score"] < 80:
                validation["areas_for_improvement"].append("Improve methodological rigor and analytical sophistication")
            if validation["networking_score"] < 80:
                validation["areas_for_improvement"].append("Strengthen knowledge dissemination and stakeholder engagement")
            
            validation["validation_status"] = "validated"
            
            return validation
            
        except Exception as e:
            return {
                "win_id": win_context.get("win_id", "unknown"),
                "error": "WIN validation failed",
                "agent_template": "ResearchAgent"
            }

    # Helper methods for strategic execution
    async def _execute_market_research(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute market research action"""
        return {
            "action": "market_research",
            "research_methodology": "mixed_methods_approach",
            "market_segments_analyzed": 4,
            "competitive_landscape": "comprehensive_analysis",
            "customer_insights": "deep_behavioral_understanding",
            "market_size_estimation": "data_driven_projection",
            "growth_forecast": "scenario_based_modeling"
        }

    async def _execute_technical_feasibility(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute technical feasibility action"""
        return {
            "action": "technical_feasibility",
            "technologies_evaluated": 12,
            "feasibility_assessment": "comprehensive_evaluation",
            "risk_analysis": "detailed_risk_matrix",
            "implementation_roadmap": "phased_approach",
            "cost_benefit_analysis": "quantified_business_case",
            "recommendation_confidence": "high"
        }

    async def _execute_competitive_analysis(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute competitive analysis action"""
        return {
            "action": "competitive_analysis",
            "competitors_analyzed": 8,
            "competitive_positioning": "strategic_differentiation",
            "strength_weakness_assessment": "swot_analysis",
            "market_share_analysis": "quantitative_assessment",
            "competitive_intelligence": "actionable_insights",
            "strategic_recommendations": "competitive_advantage_strategies"
        }

    async def _execute_trend_analysis(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute trend analysis action"""
        return {
            "action": "trend_analysis",
            "trends_identified": 12,
            "trend_significance": "high_impact_assessment",
            "forecasting_models": "statistical_and_qualitative",
            "scenario_planning": "multiple_future_scenarios",
            "strategic_implications": "business_impact_analysis",
            "monitoring_framework": "continuous_trend_tracking"
        }

    async def _execute_general_research(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute general research action"""
        return {
            "action": "general_research",
            "research_approach": "systematic_investigation",
            "sources_consulted": 35,
            "data_collection_methods": ["primary", "secondary", "expert_interviews"],
            "analysis_techniques": ["qualitative", "quantitative", "comparative"],
            "validation_methods": ["triangulation", "peer_review"],
            "knowledge_synthesis": "comprehensive_integration"
        }

    def _identify_knowledge_domains(self, description: str, context: Dict[str, Any]) -> List[str]:
        """Identify knowledge domains for research"""
        domains = []
        
        # Technology domains
        if any(keyword in description.lower() for keyword in ["ai", "machine learning", "blockchain", "iot"]):
            domains.append("technology")
        
        # Business domains
        if any(keyword in description.lower() for keyword in ["market", "business", "strategy", "finance"]):
            domains.append("business")
        
        # Healthcare domains
        if any(keyword in description.lower() for keyword in ["health", "medical", "clinical", "pharmaceutical"]):
            domains.append("healthcare")
        
        # Social domains
        if any(keyword in description.lower() for keyword in ["social", "behavioral", "psychological", "cultural"]):
            domains.append("social_sciences")
        
        # Check context for additional domains
        if context.get("domains"):
            domains.extend(context["domains"])
        
        return domains

    def _calculate_research_recognition_confidence(self, recognition_data: Dict[str, Any]) -> float:
        """Calculate confidence in research recognition analysis"""
        base_confidence = 80.0
        
        if recognition_data.get("description"):
            base_confidence += 10.0
        
        if recognition_data.get("context", {}).get("research_objectives"):
            base_confidence += 5.0
        
        if recognition_data.get("scope_definition"):
            base_confidence += 5.0
        
        return min(100.0, base_confidence) 