"""
SolutionGenerator - AI-powered solution generation engine

Generates intelligent solutions for tensions based on:
- Tension type and analysis
- Historical patterns
- Best practices templates
- Context-aware recommendations
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import uuid
from datetime import datetime

from .tension_analyzer import TensionType, TensionAnalysis

class SolutionType(Enum):
    IMMEDIATE_ACTION = "immediate_action"
    INVESTIGATION = "investigation"
    PROCESS_IMPROVEMENT = "process_improvement"
    TECHNOLOGY_SOLUTION = "technology_solution"
    TRAINING = "training"
    POLICY_CHANGE = "policy_change"
    ESCALATION = "escalation"

class SolutionPriority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

@dataclass
class SolutionStep:
    """Bước thực hiện trong solution"""
    id: str
    title: str
    description: str
    estimated_effort: str  # "1 hour", "2 days", etc.
    required_skills: List[str]
    dependencies: List[str]  # IDs of other steps
    
@dataclass
class GeneratedSolution:
    """Solution được generate bởi AI"""
    id: str
    title: str
    description: str
    solution_type: SolutionType
    priority: SolutionPriority
    estimated_impact: str
    estimated_effort: str
    success_criteria: List[str]
    steps: List[SolutionStep]
    required_resources: List[str]
    risks: List[str]
    alternatives: List[str]
    confidence_score: float  # 0.0 - 1.0
    reasoning: str
    created_at: datetime

class SolutionGenerator:
    """
    AI-powered solution generator for TRM-OS tensions.
    
    Features:
    - Pattern-based solution generation
    - Template-driven recommendations
    - Context-aware suggestions
    - Multi-step solution planning
    - Risk assessment
    """
    
    def __init__(self):
        self._initialize_solution_templates()
        self._initialize_pattern_mappings()
    
    def _initialize_solution_templates(self):
        """Initialize solution templates for different tension types"""
        
        self.problem_templates = {
            "bug_fix": {
                "title": "Bug Investigation and Fix",
                "description": "Systematic approach to identify, reproduce, and fix software bugs",
                "steps": [
                    "Reproduce the issue in controlled environment",
                    "Analyze logs and error messages",
                    "Identify root cause",
                    "Develop and test fix",
                    "Deploy fix and verify resolution"
                ],
                "estimated_effort": "1-3 days",
                "required_skills": ["debugging", "development", "testing"]
            },
            "system_outage": {
                "title": "System Recovery and Stabilization",
                "description": "Emergency response for system outages and service disruptions",
                "steps": [
                    "Assess impact and communicate status",
                    "Implement immediate workaround if available",
                    "Investigate root cause",
                    "Apply permanent fix",
                    "Conduct post-incident review"
                ],
                "estimated_effort": "4-8 hours",
                "required_skills": ["system_administration", "incident_response", "communication"]
            },
            "performance_issue": {
                "title": "Performance Analysis and Optimization",
                "description": "Systematic performance improvement approach",
                "steps": [
                    "Establish performance baseline",
                    "Identify bottlenecks",
                    "Prioritize optimization opportunities",
                    "Implement improvements",
                    "Measure and validate results"
                ],
                "estimated_effort": "1-2 weeks",
                "required_skills": ["performance_analysis", "optimization", "monitoring"]
            }
        }
        
        self.opportunity_templates = {
            "process_improvement": {
                "title": "Process Optimization Initiative",
                "description": "Systematic approach to improve existing processes",
                "steps": [
                    "Map current process",
                    "Identify improvement opportunities",
                    "Design optimized process",
                    "Pilot new process",
                    "Roll out and monitor"
                ],
                "estimated_effort": "2-4 weeks",
                "required_skills": ["process_analysis", "change_management", "stakeholder_engagement"]
            },
            "technology_upgrade": {
                "title": "Technology Enhancement Project",
                "description": "Strategic technology improvement initiative",
                "steps": [
                    "Assess current technology state",
                    "Research and evaluate options",
                    "Create implementation plan",
                    "Execute upgrade",
                    "Validate and optimize"
                ],
                "estimated_effort": "1-3 months",
                "required_skills": ["technology_assessment", "project_management", "implementation"]
            }
        }
        
        self.risk_templates = {
            "risk_mitigation": {
                "title": "Risk Assessment and Mitigation Plan",
                "description": "Comprehensive approach to address identified risks",
                "steps": [
                    "Quantify risk impact and probability",
                    "Develop mitigation strategies",
                    "Implement preventive measures",
                    "Create monitoring system",
                    "Establish response procedures"
                ],
                "estimated_effort": "1-2 weeks",
                "required_skills": ["risk_analysis", "planning", "monitoring"]
            }
        }
        
        self.conflict_templates = {
            "conflict_resolution": {
                "title": "Stakeholder Conflict Resolution",
                "description": "Structured approach to resolve conflicts between stakeholders",
                "steps": [
                    "Understand all perspectives",
                    "Identify common ground",
                    "Facilitate discussion",
                    "Develop compromise solution",
                    "Monitor implementation"
                ],
                "estimated_effort": "1-2 weeks",
                "required_skills": ["mediation", "communication", "stakeholder_management"]
            }
        }
        
        self.idea_templates = {
            "idea_evaluation": {
                "title": "Idea Evaluation and Development",
                "description": "Systematic evaluation and development of new ideas",
                "steps": [
                    "Define idea scope and objectives",
                    "Conduct feasibility analysis",
                    "Develop proof of concept",
                    "Create implementation plan",
                    "Execute pilot project"
                ],
                "estimated_effort": "2-6 weeks",
                "required_skills": ["analysis", "prototyping", "project_management"]
            }
        }
    
    def _initialize_pattern_mappings(self):
        """Initialize mappings between patterns and solution types"""
        
        self.theme_solution_mappings = {
            "Technology": [
                SolutionType.TECHNOLOGY_SOLUTION,
                SolutionType.INVESTIGATION,
                SolutionType.IMMEDIATE_ACTION
            ],
            "Business": [
                SolutionType.PROCESS_IMPROVEMENT,
                SolutionType.INVESTIGATION,
                SolutionType.POLICY_CHANGE
            ],
            "Process": [
                SolutionType.PROCESS_IMPROVEMENT,
                SolutionType.TRAINING,
                SolutionType.POLICY_CHANGE
            ],
            "People": [
                SolutionType.TRAINING,
                SolutionType.PROCESS_IMPROVEMENT,
                SolutionType.ESCALATION
            ],
            "Security": [
                SolutionType.IMMEDIATE_ACTION,
                SolutionType.INVESTIGATION,
                SolutionType.POLICY_CHANGE
            ]
        }
        
        self.urgency_priority_mapping = {
            1: SolutionPriority.LOW,
            2: SolutionPriority.MEDIUM,
            3: SolutionPriority.HIGH,
            4: SolutionPriority.CRITICAL
        }
    
    def generate_solutions(self, tension_analysis: TensionAnalysis, 
                          tension_title: str, tension_description: str,
                          context: Optional[Dict] = None) -> List[GeneratedSolution]:
        """
        Generate multiple solution options for a tension
        
        Args:
            tension_analysis: Result from TensionAnalyzer
            tension_title: Original tension title
            tension_description: Original tension description
            context: Additional context information
            
        Returns:
            List of generated solutions ranked by relevance
        """
        solutions = []
        
        # Generate primary solution based on tension type
        primary_solution = self._generate_primary_solution(
            tension_analysis, tension_title, tension_description, context
        )
        solutions.append(primary_solution)
        
        # Generate alternative solutions based on themes
        for theme in tension_analysis.key_themes:
            if theme in self.theme_solution_mappings:
                alternative = self._generate_theme_based_solution(
                    theme, tension_analysis, tension_title, context
                )
                if alternative and alternative.id != primary_solution.id:
                    solutions.append(alternative)
        
        # Generate escalation solution for high-priority tensions
        if tension_analysis.suggested_priority >= 2:  # Only for really critical tensions
            escalation_solution = self._generate_escalation_solution(
                tension_analysis, tension_title, context
            )
            solutions.append(escalation_solution)
        
        # Sort solutions by priority and confidence
        solutions.sort(key=lambda s: (s.priority.value, s.confidence_score), reverse=True)
        
        return solutions[:5]  # Return top 5 solutions
    
    def _generate_primary_solution(self, analysis: TensionAnalysis, 
                                 title: str, description: str,
                                 context: Optional[Dict] = None) -> GeneratedSolution:
        """Generate primary solution based on tension type"""
        
        solution_id = str(uuid.uuid4())
        
        # Select template based on tension type
        if analysis.tension_type == TensionType.PROBLEM:
            template = self._select_problem_template(title, description)
        elif analysis.tension_type == TensionType.OPPORTUNITY:
            template = self._select_opportunity_template(title, description)
        elif analysis.tension_type == TensionType.RISK:
            template = self.risk_templates["risk_mitigation"]
        elif analysis.tension_type == TensionType.CONFLICT:
            template = self.conflict_templates["conflict_resolution"]
        elif analysis.tension_type == TensionType.IDEA:
            template = self.idea_templates["idea_evaluation"]
        else:
            template = self._get_generic_template()
        
        # Create solution steps
        steps = []
        for i, step_desc in enumerate(template["steps"]):
            step = SolutionStep(
                id=f"{solution_id}_step_{i+1}",
                title=f"Step {i+1}: {step_desc.split(' ')[0]}",
                description=step_desc,
                estimated_effort=self._estimate_step_effort(step_desc),
                required_skills=template.get("required_skills", []),
                dependencies=[f"{solution_id}_step_{i}"] if i > 0 else []
            )
            steps.append(step)
        
        # Determine priority
        priority = self.urgency_priority_mapping.get(
            analysis.urgency_level.value, SolutionPriority.MEDIUM
        )
        
        # Calculate confidence based on analysis confidence and template match
        confidence = analysis.confidence_score * 0.8  # Slightly reduce confidence for generated solutions
        
        return GeneratedSolution(
            id=solution_id,
            title=template["title"],
            description=template["description"],
            solution_type=self._determine_solution_type(analysis.tension_type),
            priority=priority,
            estimated_impact=self._estimate_impact(analysis),
            estimated_effort=template["estimated_effort"],
            success_criteria=self._generate_success_criteria(analysis, title),
            steps=steps,
            required_resources=self._identify_required_resources(template, analysis),
            risks=self._identify_risks(analysis, template),
            alternatives=self._suggest_alternatives(analysis),
            confidence_score=confidence,
            reasoning=self._generate_solution_reasoning(analysis, template),
            created_at=datetime.now()
        )
    
    def _select_problem_template(self, title: str, description: str) -> Dict:
        """Select appropriate problem template based on content"""
        text = f"{title} {description}".lower()
        
        if any(keyword in text for keyword in ["bug", "error", "exception", "crash"]):
            return self.problem_templates["bug_fix"]
        elif any(keyword in text for keyword in ["down", "outage", "unavailable", "offline"]):
            return self.problem_templates["system_outage"]
        elif any(keyword in text for keyword in ["slow", "performance", "latency", "timeout"]):
            return self.problem_templates["performance_issue"]
        else:
            return self.problem_templates["bug_fix"]  # Default
    
    def _select_opportunity_template(self, title: str, description: str) -> Dict:
        """Select appropriate opportunity template based on content"""
        text = f"{title} {description}".lower()
        
        if any(keyword in text for keyword in ["process", "workflow", "efficiency"]):
            return self.opportunity_templates["process_improvement"]
        elif any(keyword in text for keyword in ["technology", "upgrade", "modernize"]):
            return self.opportunity_templates["technology_upgrade"]
        else:
            return self.opportunity_templates["process_improvement"]  # Default
    
    def _get_generic_template(self) -> Dict:
        """Get generic template for unknown tension types"""
        return {
            "title": "General Investigation and Resolution",
            "description": "Systematic approach to investigate and resolve the tension",
            "steps": [
                "Gather additional information",
                "Analyze the situation",
                "Develop action plan",
                "Implement solution",
                "Monitor results"
            ],
            "estimated_effort": "1-2 weeks",
            "required_skills": ["analysis", "problem_solving", "communication"]
        }
    
    def _generate_theme_based_solution(self, theme: str, analysis: TensionAnalysis,
                                     title: str, context: Optional[Dict] = None) -> Optional[GeneratedSolution]:
        """Generate solution based on specific theme"""
        if theme not in self.theme_solution_mappings:
            return None
        
        solution_types = self.theme_solution_mappings[theme]
        primary_type = solution_types[0]
        
        solution_id = str(uuid.uuid4())
        
        # Create theme-specific solution
        if theme == "Technology":
            template_title = "Technology-Focused Solution"
            template_desc = "Technology-centric approach to address the tension"
            steps_list = [
                "Assess current technology state",
                "Identify technical requirements",
                "Design technical solution",
                "Implement and test",
                "Deploy and monitor"
            ]
        elif theme == "Business":
            template_title = "Business Process Solution"
            template_desc = "Business-focused approach to resolve the tension"
            steps_list = [
                "Analyze business impact",
                "Engage stakeholders",
                "Define business requirements",
                "Implement business solution",
                "Measure business outcomes"
            ]
        elif theme == "Security":
            template_title = "Security-Focused Response"
            template_desc = "Security-centric approach to address the tension"
            steps_list = [
                "Assess security implications",
                "Implement immediate security measures",
                "Conduct security review",
                "Apply security controls",
                "Monitor security posture"
            ]
        else:
            return None
        
        steps = []
        for i, step_desc in enumerate(steps_list):
            step = SolutionStep(
                id=f"{solution_id}_step_{i+1}",
                title=f"Step {i+1}: {step_desc.split(' ')[0]}",
                description=step_desc,
                estimated_effort=self._estimate_step_effort(step_desc),
                required_skills=[theme.lower(), "analysis"],
                dependencies=[f"{solution_id}_step_{i}"] if i > 0 else []
            )
            steps.append(step)
        
        return GeneratedSolution(
            id=solution_id,
            title=template_title,
            description=template_desc,
            solution_type=primary_type,
            priority=SolutionPriority.MEDIUM,
            estimated_impact="Medium",
            estimated_effort="1-2 weeks",
            success_criteria=self._generate_success_criteria(analysis, title),
            steps=steps,
            required_resources=[theme.lower() + "_expertise"],
            risks=[f"{theme} complexity", "Resource availability"],
            alternatives=["Generic approach", "Hybrid solution"],
            confidence_score=0.7,
            reasoning=f"Solution focused on {theme} theme identified in analysis",
            created_at=datetime.now()
        )
    
    def _generate_escalation_solution(self, analysis: TensionAnalysis,
                                    title: str, context: Optional[Dict] = None) -> GeneratedSolution:
        """Generate escalation solution for high-priority tensions"""
        
        solution_id = str(uuid.uuid4())
        
        steps = [
            SolutionStep(
                id=f"{solution_id}_step_1",
                title="Step 1: Immediate Escalation",
                description="Escalate to appropriate stakeholders immediately",
                estimated_effort="30 minutes",
                required_skills=["communication", "stakeholder_management"],
                dependencies=[]
            ),
            SolutionStep(
                id=f"{solution_id}_step_2", 
                title="Step 2: Stakeholder Alignment",
                description="Align stakeholders on priority and approach",
                estimated_effort="1 hour",
                required_skills=["facilitation", "communication"],
                dependencies=[f"{solution_id}_step_1"]
            ),
            SolutionStep(
                id=f"{solution_id}_step_3",
                title="Step 3: Resource Allocation",
                description="Allocate necessary resources for resolution",
                estimated_effort="2 hours",
                required_skills=["resource_management", "planning"],
                dependencies=[f"{solution_id}_step_2"]
            )
        ]
        
        return GeneratedSolution(
            id=solution_id,
            title="Escalation and Priority Response",
            description="Immediate escalation and priority handling for critical tension",
            solution_type=SolutionType.ESCALATION,
            priority=SolutionPriority.CRITICAL,
            estimated_impact="High",
            estimated_effort="4-8 hours",
            success_criteria=[
                "Stakeholders notified within 30 minutes",
                "Resources allocated within 4 hours",
                "Resolution plan established within 8 hours"
            ],
            steps=steps,
            required_resources=["management_support", "dedicated_team"],
            risks=["Resource conflicts", "Stakeholder availability"],
            alternatives=["Standard process", "Delayed response"],
            confidence_score=0.9,
            reasoning="High-priority tension requires immediate escalation and resource allocation",
            created_at=datetime.now()
        )
    
    def _determine_solution_type(self, tension_type: TensionType) -> SolutionType:
        """Map tension type to solution type"""
        mapping = {
            TensionType.PROBLEM: SolutionType.IMMEDIATE_ACTION,
            TensionType.OPPORTUNITY: SolutionType.PROCESS_IMPROVEMENT,
            TensionType.RISK: SolutionType.INVESTIGATION,
            TensionType.CONFLICT: SolutionType.ESCALATION,
            TensionType.IDEA: SolutionType.INVESTIGATION,
            TensionType.UNKNOWN: SolutionType.INVESTIGATION
        }
        return mapping.get(tension_type, SolutionType.INVESTIGATION)
    
    def _estimate_step_effort(self, step_description: str) -> str:
        """Estimate effort for individual step"""
        if any(keyword in step_description.lower() for keyword in ["immediate", "quick", "assess"]):
            return "1-2 hours"
        elif any(keyword in step_description.lower() for keyword in ["develop", "implement", "create"]):
            return "1-2 days"
        elif any(keyword in step_description.lower() for keyword in ["analyze", "investigate", "research"]):
            return "2-4 hours"
        else:
            return "4-8 hours"
    
    def _estimate_impact(self, analysis: TensionAnalysis) -> str:
        """Estimate solution impact based on analysis"""
        if analysis.impact_level.value >= 4:
            return "Critical"
        elif analysis.impact_level.value >= 3:
            return "High"
        elif analysis.impact_level.value >= 2:
            return "Medium"
        else:
            return "Low"
    
    def _generate_success_criteria(self, analysis: TensionAnalysis, title: str) -> List[str]:
        """Generate success criteria for solution"""
        criteria = []
        
        # Base criteria
        criteria.append("Tension is resolved and marked as closed")
        criteria.append("Stakeholders confirm satisfaction with resolution")
        
        # Type-specific criteria
        if analysis.tension_type == TensionType.PROBLEM:
            criteria.append("Root cause is identified and addressed")
            criteria.append("No recurrence within 30 days")
        elif analysis.tension_type == TensionType.OPPORTUNITY:
            criteria.append("Measurable improvement is achieved")
            criteria.append("Benefits are documented and validated")
        elif analysis.tension_type == TensionType.RISK:
            criteria.append("Risk is mitigated to acceptable level")
            criteria.append("Monitoring system is in place")
        
        return criteria
    
    def _identify_required_resources(self, template: Dict, analysis: TensionAnalysis) -> List[str]:
        """Identify required resources for solution"""
        resources = []
        
        # Skills-based resources
        for skill in template.get("required_skills", []):
            resources.append(f"{skill}_expertise")
        
        # Theme-based resources
        for theme in analysis.key_themes:
            if theme == "Technology":
                resources.extend(["development_team", "testing_environment"])
            elif theme == "Security":
                resources.extend(["security_team", "security_tools"])
            elif theme == "Business":
                resources.extend(["business_analyst", "stakeholder_time"])
        
        return list(set(resources))  # Remove duplicates
    
    def _identify_risks(self, analysis: TensionAnalysis, template: Dict) -> List[str]:
        """Identify potential risks for solution"""
        risks = []
        
        # General risks
        risks.extend(["Resource unavailability", "Timeline delays", "Scope creep"])
        
        # Type-specific risks
        if analysis.tension_type == TensionType.PROBLEM:
            risks.extend(["Incomplete fix", "Side effects", "Regression"])
        elif analysis.tension_type == TensionType.OPPORTUNITY:
            risks.extend(["ROI not achieved", "Change resistance", "Implementation complexity"])
        
        # Theme-specific risks
        for theme in analysis.key_themes:
            if theme == "Technology":
                risks.extend(["Technical complexity", "Integration issues"])
            elif theme == "Security":
                risks.extend(["Security vulnerabilities", "Compliance issues"])
        
        return list(set(risks))  # Remove duplicates
    
    def _suggest_alternatives(self, analysis: TensionAnalysis) -> List[str]:
        """Suggest alternative approaches"""
        alternatives = []
        
        # Generic alternatives
        alternatives.extend(["Phased approach", "Pilot implementation", "External consultation"])
        
        # Type-specific alternatives
        if analysis.tension_type == TensionType.PROBLEM:
            alternatives.extend(["Workaround solution", "Third-party fix"])
        elif analysis.tension_type == TensionType.OPPORTUNITY:
            alternatives.extend(["Incremental improvement", "Complete redesign"])
        
        return alternatives
    
    def _generate_solution_reasoning(self, analysis: TensionAnalysis, template: Dict) -> str:
        """Generate reasoning for solution recommendation"""
        reasoning_parts = []
        
        reasoning_parts.append(
            f"Solution generated based on {analysis.tension_type.value} classification "
            f"with {analysis.confidence_score:.1%} confidence"
        )
        
        reasoning_parts.append(
            f"Template selected based on content analysis and {', '.join(analysis.key_themes)} themes"
        )
        
        reasoning_parts.append(
            f"Priority set to {analysis.suggested_priority} based on impact ({analysis.impact_level.name}) "
            f"and urgency ({analysis.urgency_level.name})"
        )
        
        return ". ".join(reasoning_parts) + "." 