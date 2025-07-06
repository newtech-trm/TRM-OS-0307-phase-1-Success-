"""
Agent Capability Evolver

Advanced component của Genesis Engine để phân tích performance gaps
và evolve agent capabilities dynamically dựa trên feedback và performance data.
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional, Union, Tuple
from datetime import datetime, timedelta
from collections import defaultdict
import uuid

from ..templates.base_template import BaseAgentTemplate, AgentCapability
from ..genesis.advanced_creator import CompositeAgent, CustomAgent
from ...models.tension import Tension
from ...models.enums import TensionType, Priority


class PerformanceGap:
    """Performance gap được identify trong agent"""
    
    def __init__(self,
                 gap_id: str,
                 gap_type: str,
                 description: str,
                 severity: str,
                 affected_capabilities: List[str],
                 impact_score: float,
                 recommended_actions: List[str]):
        self.gap_id = gap_id
        self.gap_type = gap_type
        self.description = description
        self.severity = severity  # low, medium, high, critical
        self.affected_capabilities = affected_capabilities
        self.impact_score = impact_score  # 0-100
        self.recommended_actions = recommended_actions
        self.identified_at = datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "gap_id": self.gap_id,
            "gap_type": self.gap_type,
            "description": self.description,
            "severity": self.severity,
            "affected_capabilities": self.affected_capabilities,
            "impact_score": self.impact_score,
            "recommended_actions": self.recommended_actions,
            "identified_at": self.identified_at.isoformat()
        }


class EvolutionResult:
    """Kết quả evolution của agent capabilities"""
    
    def __init__(self,
                 agent_id: str,
                 evolution_type: str,
                 changes_made: List[Dict[str, Any]],
                 performance_improvement: Dict[str, float],
                 success: bool,
                 notes: str):
        self.agent_id = agent_id
        self.evolution_type = evolution_type
        self.changes_made = changes_made
        self.performance_improvement = performance_improvement
        self.success = success
        self.notes = notes
        self.evolved_at = datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "evolution_type": self.evolution_type,
            "changes_made": self.changes_made,
            "performance_improvement": self.performance_improvement,
            "success": self.success,
            "notes": self.notes,
            "evolved_at": self.evolved_at.isoformat()
        }


class CapabilityEvolutionStrategy:
    """Strategy cho capability evolution"""
    
    def __init__(self,
                 strategy_name: str,
                 description: str,
                 applicable_gaps: List[str],
                 evolution_steps: List[str],
                 expected_improvement: float):
        self.strategy_name = strategy_name
        self.description = description
        self.applicable_gaps = applicable_gaps
        self.evolution_steps = evolution_steps
        self.expected_improvement = expected_improvement


class AgentCapabilityEvolver:
    """
    Agent Capability Evolver cho TRM-OS Genesis Engine.
    
    Capabilities:
    - Analyze agent performance gaps
    - Evolve agent capabilities dynamically
    - Validate capability improvements
    - Track evolution history
    """
    
    def __init__(self):
        self.logger = logging.getLogger("AgentCapabilityEvolver")
        self.identified_gaps: Dict[str, List[PerformanceGap]] = defaultdict(list)
        self.evolution_history: Dict[str, List[EvolutionResult]] = defaultdict(list)
        self.evolution_strategies = self._initialize_evolution_strategies()
        self.evolution_stats = {
            "agents_evolved": 0,
            "gaps_identified": 0,
            "successful_evolutions": 0,
            "total_performance_improvement": 0.0
        }
    
    def _initialize_evolution_strategies(self) -> Dict[str, CapabilityEvolutionStrategy]:
        """Initialize evolution strategies"""
        strategies = {}
        
        # Strategy 1: Capability Enhancement
        strategies["capability_enhancement"] = CapabilityEvolutionStrategy(
            strategy_name="Capability Enhancement",
            description="Improve existing capabilities through proficiency increase",
            applicable_gaps=["low_proficiency", "slow_execution", "quality_issues"],
            evolution_steps=[
                "Analyze capability performance metrics",
                "Identify specific improvement areas",
                "Apply targeted enhancements",
                "Validate improvement"
            ],
            expected_improvement=15.0
        )
        
        # Strategy 2: Capability Addition
        strategies["capability_addition"] = CapabilityEvolutionStrategy(
            strategy_name="Capability Addition",
            description="Add new capabilities to address gaps",
            applicable_gaps=["missing_capability", "limited_scope", "domain_gap"],
            evolution_steps=[
                "Identify required new capabilities",
                "Design capability specifications",
                "Integrate new capabilities",
                "Test capability integration"
            ],
            expected_improvement=25.0
        )
        
        # Strategy 3: Capability Optimization
        strategies["capability_optimization"] = CapabilityEvolutionStrategy(
            strategy_name="Capability Optimization",
            description="Optimize capability configurations for better performance",
            applicable_gaps=["inefficient_execution", "resource_waste", "poor_coordination"],
            evolution_steps=[
                "Analyze capability usage patterns",
                "Identify optimization opportunities",
                "Apply optimization changes",
                "Monitor performance impact"
            ],
            expected_improvement=20.0
        )
        
        # Strategy 4: Capability Specialization
        strategies["capability_specialization"] = CapabilityEvolutionStrategy(
            strategy_name="Capability Specialization",
            description="Specialize capabilities for specific domains or tasks",
            applicable_gaps=["generic_approach", "domain_mismatch", "task_specific_issues"],
            evolution_steps=[
                "Analyze domain-specific requirements",
                "Design specialized capability variants",
                "Implement specialization logic",
                "Validate specialization effectiveness"
            ],
            expected_improvement=30.0
        )
        
        return strategies
    
    async def analyze_agent_performance_gaps(self, 
                                           agent: Union[CompositeAgent, CustomAgent, BaseAgentTemplate],
                                           performance_data: Dict[str, Any],
                                           historical_data: Optional[Dict[str, Any]] = None) -> List[PerformanceGap]:
        """
        Analyze agent performance để identify gaps.
        
        Args:
            agent: Agent cần analyze
            performance_data: Current performance metrics
            historical_data: Optional historical performance data
            
        Returns:
            List identified performance gaps
        """
        try:
            self.logger.info(f"Analyzing performance gaps for agent: {agent.agent_id}")
            
            gaps = []
            
            # Analyze efficiency gaps
            efficiency_gaps = await self._analyze_efficiency_gaps(agent, performance_data)
            gaps.extend(efficiency_gaps)
            
            # Analyze quality gaps
            quality_gaps = await self._analyze_quality_gaps(agent, performance_data)
            gaps.extend(quality_gaps)
            
            # Analyze capability gaps
            capability_gaps = await self._analyze_capability_gaps(agent, performance_data)
            gaps.extend(capability_gaps)
            
            # Analyze domain expertise gaps
            domain_gaps = await self._analyze_domain_gaps(agent, performance_data)
            gaps.extend(domain_gaps)
            
            # Analyze historical performance trends nếu có data
            if historical_data:
                trend_gaps = await self._analyze_performance_trends(agent, performance_data, historical_data)
                gaps.extend(trend_gaps)
            
            # Store identified gaps
            self.identified_gaps[agent.agent_id] = gaps
            self.evolution_stats["gaps_identified"] += len(gaps)
            
            self.logger.info(f"Identified {len(gaps)} performance gaps for agent {agent.agent_id}")
            return gaps
            
        except Exception as e:
            self.logger.error(f"Error analyzing agent performance gaps: {str(e)}")
            return []
    
    async def _analyze_efficiency_gaps(self, 
                                     agent: Union[CompositeAgent, CustomAgent, BaseAgentTemplate],
                                     performance_data: Dict[str, Any]) -> List[PerformanceGap]:
        """Analyze efficiency-related gaps"""
        gaps = []
        efficiency = performance_data.get("efficiency", 50)
        
        if efficiency < 60:
            gap = PerformanceGap(
                gap_id=f"efficiency_{uuid.uuid4().hex[:8]}",
                gap_type="efficiency",
                description=f"Low efficiency score: {efficiency}%. Agent is performing below acceptable threshold.",
                severity="high" if efficiency < 40 else "medium",
                affected_capabilities=[cap.name for cap in agent.capabilities] if hasattr(agent, 'capabilities') else [],
                impact_score=80 - efficiency,
                recommended_actions=[
                    "Optimize capability execution algorithms",
                    "Reduce unnecessary processing steps",
                    "Implement caching mechanisms",
                    "Parallelize independent operations"
                ]
            )
            gaps.append(gap)
        
        return gaps
    
    async def _analyze_quality_gaps(self, 
                                  agent: Union[CompositeAgent, CustomAgent, BaseAgentTemplate],
                                  performance_data: Dict[str, Any]) -> List[PerformanceGap]:
        """Analyze quality-related gaps"""
        gaps = []
        quality = performance_data.get("quality", 50)
        
        if quality < 70:
            gap = PerformanceGap(
                gap_id=f"quality_{uuid.uuid4().hex[:8]}",
                gap_type="quality",
                description=f"Low quality score: {quality}%. Output quality needs improvement.",
                severity="high" if quality < 50 else "medium",
                affected_capabilities=[cap.name for cap in agent.capabilities] if hasattr(agent, 'capabilities') else [],
                impact_score=90 - quality,
                recommended_actions=[
                    "Implement quality validation checks",
                    "Add peer review mechanisms",
                    "Enhance solution verification",
                    "Improve error detection and correction"
                ]
            )
            gaps.append(gap)
        
        return gaps
    
    async def _analyze_capability_gaps(self, 
                                     agent: Union[CompositeAgent, CustomAgent, BaseAgentTemplate],
                                     performance_data: Dict[str, Any]) -> List[PerformanceGap]:
        """Analyze capability-related gaps"""
        gaps = []
        
        if hasattr(agent, 'capabilities'):
            # Check for low-performing capabilities
            capability_performance = performance_data.get("capability_performance", {})
            
            for capability in agent.capabilities:
                cap_performance = capability_performance.get(capability.name, 70)
                
                if cap_performance < 60:
                    gap = PerformanceGap(
                        gap_id=f"capability_{uuid.uuid4().hex[:8]}",
                        gap_type="capability_performance",
                        description=f"Low performance in {capability.name}: {cap_performance}%",
                        severity="medium",
                        affected_capabilities=[capability.name],
                        impact_score=80 - cap_performance,
                        recommended_actions=[
                            f"Enhance {capability.name} algorithms",
                            f"Add specialized tools for {capability.name}",
                            f"Improve {capability.name} training data",
                            f"Optimize {capability.name} execution flow"
                        ]
                    )
                    gaps.append(gap)
            
            # Check for missing capabilities
            requested_capabilities = performance_data.get("requested_but_missing", [])
            if requested_capabilities:
                gap = PerformanceGap(
                    gap_id=f"missing_cap_{uuid.uuid4().hex[:8]}",
                    gap_type="missing_capability",
                    description=f"Missing requested capabilities: {', '.join(requested_capabilities)}",
                    severity="high",
                    affected_capabilities=requested_capabilities,
                    impact_score=50,
                    recommended_actions=[
                        "Add missing capabilities to agent",
                        "Train agent in new capability areas",
                        "Integrate capability-specific tools",
                        "Validate new capability effectiveness"
                    ]
                )
                gaps.append(gap)
        
        return gaps
    
    async def _analyze_domain_gaps(self, 
                                 agent: Union[CompositeAgent, CustomAgent, BaseAgentTemplate],
                                 performance_data: Dict[str, Any]) -> List[PerformanceGap]:
        """Analyze domain expertise gaps"""
        gaps = []
        
        # Check domain coverage
        domain_performance = performance_data.get("domain_performance", {})
        weak_domains = [domain for domain, score in domain_performance.items() if score < 60]
        
        if weak_domains:
            gap = PerformanceGap(
                gap_id=f"domain_{uuid.uuid4().hex[:8]}",
                gap_type="domain_expertise",
                description=f"Weak performance in domains: {', '.join(weak_domains)}",
                severity="medium",
                affected_capabilities=[],
                impact_score=len(weak_domains) * 10,
                recommended_actions=[
                    "Enhance domain-specific knowledge",
                    "Add domain-specific capabilities",
                    "Improve domain pattern recognition",
                    "Integrate domain expert feedback"
                ]
            )
            gaps.append(gap)
        
        return gaps
    
    async def _analyze_performance_trends(self, 
                                        agent: Union[CompositeAgent, CustomAgent, BaseAgentTemplate],
                                        current_data: Dict[str, Any],
                                        historical_data: Dict[str, Any]) -> List[PerformanceGap]:
        """Analyze performance trends from historical data"""
        gaps = []
        
        # Check for declining trends
        current_efficiency = current_data.get("efficiency", 50)
        historical_efficiency = historical_data.get("average_efficiency", 50)
        
        if current_efficiency < historical_efficiency - 10:
            gap = PerformanceGap(
                gap_id=f"trend_{uuid.uuid4().hex[:8]}",
                gap_type="performance_decline",
                description=f"Efficiency declining: {historical_efficiency}% → {current_efficiency}%",
                severity="medium",
                affected_capabilities=[],
                impact_score=historical_efficiency - current_efficiency,
                recommended_actions=[
                    "Investigate performance degradation causes",
                    "Reset agent to previous configuration",
                    "Update agent training data",
                    "Optimize agent resource usage"
                ]
            )
            gaps.append(gap)
        
        return gaps
    
    async def evolve_agent_capabilities(self, 
                                      agent: Union[CompositeAgent, CustomAgent, BaseAgentTemplate],
                                      gaps: List[PerformanceGap]) -> EvolutionResult:
        """
        Evolve agent capabilities để address identified gaps.
        
        Args:
            agent: Agent cần evolve
            gaps: List performance gaps cần address
            
        Returns:
            EvolutionResult
        """
        try:
            self.logger.info(f"Evolving capabilities for agent: {agent.agent_id}")
            
            changes_made = []
            performance_improvement = {}
            
            # Group gaps by type
            gaps_by_type = defaultdict(list)
            for gap in gaps:
                gaps_by_type[gap.gap_type].append(gap)
            
            # Apply appropriate evolution strategies
            for gap_type, type_gaps in gaps_by_type.items():
                strategy = self._select_evolution_strategy(gap_type, type_gaps)
                
                if strategy:
                    evolution_changes = await self._apply_evolution_strategy(agent, strategy, type_gaps)
                    changes_made.extend(evolution_changes)
            
            # Calculate expected performance improvement
            total_improvement = sum(change.get("improvement_estimate", 0) for change in changes_made)
            performance_improvement = {
                "efficiency": min(20, total_improvement * 0.4),
                "quality": min(15, total_improvement * 0.3),
                "capability_coverage": min(25, total_improvement * 0.3)
            }
            
            # Create evolution result
            success = len(changes_made) > 0
            notes = f"Applied {len(changes_made)} capability changes to address {len(gaps)} performance gaps"
            
            result = EvolutionResult(
                agent_id=agent.agent_id,
                evolution_type="capability_evolution",
                changes_made=changes_made,
                performance_improvement=performance_improvement,
                success=success,
                notes=notes
            )
            
            # Store evolution result
            self.evolution_history[agent.agent_id].append(result)
            
            if success:
                self.evolution_stats["successful_evolutions"] += 1
                self.evolution_stats["total_performance_improvement"] += total_improvement
            
            self.evolution_stats["agents_evolved"] += 1
            
            self.logger.info(f"Agent evolution completed: {agent.agent_id} - Success: {success}")
            return result
            
        except Exception as e:
            self.logger.error(f"Error evolving agent capabilities: {str(e)}")
            return EvolutionResult(
                agent_id=agent.agent_id,
                evolution_type="capability_evolution",
                changes_made=[],
                performance_improvement={},
                success=False,
                notes=f"Evolution failed: {str(e)}"
            )
    
    def _select_evolution_strategy(self, 
                                  gap_type: str,
                                  gaps: List[PerformanceGap]) -> Optional[CapabilityEvolutionStrategy]:
        """Select appropriate evolution strategy cho gap type"""
        
        # Strategy selection logic
        strategy_mapping = {
            "efficiency": "capability_optimization",
            "quality": "capability_enhancement",
            "capability_performance": "capability_enhancement",
            "missing_capability": "capability_addition",
            "domain_expertise": "capability_specialization",
            "performance_decline": "capability_optimization"
        }
        
        strategy_name = strategy_mapping.get(gap_type)
        return self.evolution_strategies.get(strategy_name) if strategy_name else None
    
    async def _apply_evolution_strategy(self, 
                                      agent: Union[CompositeAgent, CustomAgent, BaseAgentTemplate],
                                      strategy: CapabilityEvolutionStrategy,
                                      gaps: List[PerformanceGap]) -> List[Dict[str, Any]]:
        """Apply evolution strategy to agent"""
        changes = []
        
        try:
            if strategy.strategy_name == "Capability Enhancement":
                changes = await self._enhance_capabilities(agent, gaps)
            
            elif strategy.strategy_name == "Capability Addition":
                changes = await self._add_capabilities(agent, gaps)
            
            elif strategy.strategy_name == "Capability Optimization":
                changes = await self._optimize_capabilities(agent, gaps)
            
            elif strategy.strategy_name == "Capability Specialization":
                changes = await self._specialize_capabilities(agent, gaps)
            
        except Exception as e:
            self.logger.error(f"Error applying evolution strategy {strategy.strategy_name}: {str(e)}")
        
        return changes
    
    async def _enhance_capabilities(self, 
                                  agent: Union[CompositeAgent, CustomAgent, BaseAgentTemplate],
                                  gaps: List[PerformanceGap]) -> List[Dict[str, Any]]:
        """Enhance existing capabilities"""
        changes = []
        
        if hasattr(agent, 'capabilities'):
            for gap in gaps:
                for cap_name in gap.affected_capabilities:
                    # Find capability to enhance
                    for capability in agent.capabilities:
                        if capability.name == cap_name:
                            # Increase proficiency
                            old_proficiency = capability.proficiency_level
                            capability.proficiency_level = min(95, capability.proficiency_level + 10)
                            
                            # Reduce task time
                            old_time = capability.estimated_time_per_task
                            capability.estimated_time_per_task = max(30, int(capability.estimated_time_per_task * 0.9))
                            
                            change = {
                                "type": "capability_enhancement",
                                "capability": cap_name,
                                "proficiency_change": f"{old_proficiency} → {capability.proficiency_level}",
                                "time_change": f"{old_time} → {capability.estimated_time_per_task}",
                                "improvement_estimate": 15
                            }
                            changes.append(change)
                            break
        
        return changes
    
    async def _add_capabilities(self, 
                              agent: Union[CompositeAgent, CustomAgent, BaseAgentTemplate],
                              gaps: List[PerformanceGap]) -> List[Dict[str, Any]]:
        """Add new capabilities to agent"""
        changes = []
        
        if hasattr(agent, 'capabilities'):
            for gap in gaps:
                for cap_name in gap.affected_capabilities:
                    # Check if capability already exists
                    existing_caps = [cap.name for cap in agent.capabilities]
                    
                    if cap_name not in existing_caps:
                        # Add new capability
                        new_capability = AgentCapability(
                            name=cap_name,
                            description=f"Added capability: {cap_name}",
                            proficiency_level=75,  # Start với moderate proficiency
                            tools_required=[],
                            estimated_time_per_task=90
                        )
                        
                        agent.capabilities.append(new_capability)
                        
                        change = {
                            "type": "capability_addition",
                            "capability": cap_name,
                            "proficiency": new_capability.proficiency_level,
                            "estimated_time": new_capability.estimated_time_per_task,
                            "improvement_estimate": 25
                        }
                        changes.append(change)
        
        return changes
    
    async def _optimize_capabilities(self, 
                                   agent: Union[CompositeAgent, CustomAgent, BaseAgentTemplate],
                                   gaps: List[PerformanceGap]) -> List[Dict[str, Any]]:
        """Optimize capability configurations"""
        changes = []
        
        if hasattr(agent, 'capabilities'):
            # Optimize task time estimates
            for capability in agent.capabilities:
                old_time = capability.estimated_time_per_task
                capability.estimated_time_per_task = max(30, int(capability.estimated_time_per_task * 0.85))
                
                change = {
                    "type": "capability_optimization",
                    "capability": capability.name,
                    "time_optimization": f"{old_time} → {capability.estimated_time_per_task}",
                    "improvement_estimate": 20
                }
                changes.append(change)
        
        return changes
    
    async def _specialize_capabilities(self, 
                                     agent: Union[CompositeAgent, CustomAgent, BaseAgentTemplate],
                                     gaps: List[PerformanceGap]) -> List[Dict[str, Any]]:
        """Specialize capabilities for specific domains"""
        changes = []
        
        if hasattr(agent, 'capabilities'):
            for gap in gaps:
                # Add domain-specific tools và enhance proficiency
                for capability in agent.capabilities:
                    old_proficiency = capability.proficiency_level
                    capability.proficiency_level = min(90, capability.proficiency_level + 15)
                    
                    # Add domain-specific tools
                    domain_tools = [f"domain_specific_tool_{i}" for i in range(2)]
                    capability.tools_required.extend(domain_tools)
                    
                    change = {
                        "type": "capability_specialization",
                        "capability": capability.name,
                        "proficiency_boost": f"{old_proficiency} → {capability.proficiency_level}",
                        "tools_added": domain_tools,
                        "improvement_estimate": 30
                    }
                    changes.append(change)
        
        return changes
    
    async def validate_capability_improvements(self, 
                                             before_agent: Union[CompositeAgent, CustomAgent, BaseAgentTemplate],
                                             after_agent: Union[CompositeAgent, CustomAgent, BaseAgentTemplate],
                                             test_tensions: Optional[List[Tension]] = None) -> Dict[str, Any]:
        """
        Validate capability improvements sau evolution.
        
        Args:
            before_agent: Agent state trước evolution
            after_agent: Agent state sau evolution
            test_tensions: Optional test tensions cho validation
            
        Returns:
            Validation results
        """
        try:
            self.logger.info(f"Validating capability improvements for agent: {after_agent.agent_id}")
            
            validation_results = {
                "agent_id": after_agent.agent_id,
                "capability_changes": self._compare_capabilities(before_agent, after_agent),
                "improvement_metrics": {},
                "validation_score": 0.0,
                "recommendations": []
            }
            
            # Compare capability counts
            before_cap_count = len(before_agent.capabilities) if hasattr(before_agent, 'capabilities') else 0
            after_cap_count = len(after_agent.capabilities) if hasattr(after_agent, 'capabilities') else 0
            
            validation_results["improvement_metrics"]["capability_count_change"] = after_cap_count - before_cap_count
            
            # Compare proficiency levels
            if hasattr(before_agent, 'capabilities') and hasattr(after_agent, 'capabilities'):
                before_avg_proficiency = sum(cap.proficiency_level for cap in before_agent.capabilities) / max(1, len(before_agent.capabilities))
                after_avg_proficiency = sum(cap.proficiency_level for cap in after_agent.capabilities) / max(1, len(after_agent.capabilities))
                
                validation_results["improvement_metrics"]["proficiency_improvement"] = after_avg_proficiency - before_avg_proficiency
            
            # Test với tensions nếu provided
            if test_tensions:
                tension_results = await self._test_evolution_with_tensions(before_agent, after_agent, test_tensions)
                validation_results["improvement_metrics"]["tension_handling"] = tension_results
            
            # Calculate validation score
            score = 50  # Base score
            
            if validation_results["improvement_metrics"].get("capability_count_change", 0) > 0:
                score += 20
            
            if validation_results["improvement_metrics"].get("proficiency_improvement", 0) > 0:
                score += 20
            
            if validation_results["improvement_metrics"].get("tension_handling", {}).get("improvement", 0) > 0:
                score += 10
            
            validation_results["validation_score"] = min(100, score)
            
            # Generate recommendations
            if validation_results["validation_score"] < 70:
                validation_results["recommendations"].append("Consider additional capability enhancements")
            
            if validation_results["improvement_metrics"].get("capability_count_change", 0) == 0:
                validation_results["recommendations"].append("Add new capabilities to expand agent scope")
            
            self.logger.info(f"Capability validation completed: score {validation_results['validation_score']}")
            return validation_results
            
        except Exception as e:
            self.logger.error(f"Error validating capability improvements: {str(e)}")
            return {"error": str(e)}
    
    def _compare_capabilities(self, 
                            before_agent: Union[CompositeAgent, CustomAgent, BaseAgentTemplate],
                            after_agent: Union[CompositeAgent, CustomAgent, BaseAgentTemplate]) -> Dict[str, Any]:
        """Compare capabilities between before và after states"""
        comparison = {
            "added_capabilities": [],
            "enhanced_capabilities": [],
            "removed_capabilities": []
        }
        
        if hasattr(before_agent, 'capabilities') and hasattr(after_agent, 'capabilities'):
            before_caps = {cap.name: cap for cap in before_agent.capabilities}
            after_caps = {cap.name: cap for cap in after_agent.capabilities}
            
            # Find added capabilities
            for cap_name in after_caps:
                if cap_name not in before_caps:
                    comparison["added_capabilities"].append(cap_name)
            
            # Find removed capabilities
            for cap_name in before_caps:
                if cap_name not in after_caps:
                    comparison["removed_capabilities"].append(cap_name)
            
            # Find enhanced capabilities
            for cap_name in before_caps:
                if cap_name in after_caps:
                    before_prof = before_caps[cap_name].proficiency_level
                    after_prof = after_caps[cap_name].proficiency_level
                    
                    if after_prof > before_prof:
                        comparison["enhanced_capabilities"].append({
                            "capability": cap_name,
                            "proficiency_change": f"{before_prof} → {after_prof}"
                        })
        
        return comparison
    
    async def _test_evolution_with_tensions(self, 
                                          before_agent: Union[CompositeAgent, CustomAgent, BaseAgentTemplate],
                                          after_agent: Union[CompositeAgent, CustomAgent, BaseAgentTemplate],
                                          test_tensions: List[Tension]) -> Dict[str, Any]:
        """Test evolution improvements với tensions"""
        try:
            before_results = {"handled": 0, "solutions": 0}
            after_results = {"handled": 0, "solutions": 0}
            
            for tension in test_tensions:
                # Test before agent
                if await before_agent.can_handle_tension(tension):
                    before_results["handled"] += 1
                    before_solutions = await before_agent.generate_specialized_solutions(tension)
                    before_results["solutions"] += len(before_solutions)
                
                # Test after agent
                if await after_agent.can_handle_tension(tension):
                    after_results["handled"] += 1
                    after_solutions = await after_agent.generate_specialized_solutions(tension)
                    after_results["solutions"] += len(after_solutions)
            
            return {
                "before": before_results,
                "after": after_results,
                "improvement": after_results["handled"] - before_results["handled"]
            }
            
        except Exception as e:
            self.logger.error(f"Error testing evolution with tensions: {str(e)}")
            return {"error": str(e)}
    
    def get_identified_gaps(self, agent_id: str) -> List[PerformanceGap]:
        """Trả về identified gaps cho agent"""
        return self.identified_gaps.get(agent_id, [])
    
    def get_evolution_history(self, agent_id: str) -> List[EvolutionResult]:
        """Trả về evolution history cho agent"""
        return self.evolution_history.get(agent_id, [])
    
    def get_evolution_stats(self) -> Dict[str, Any]:
        """Trả về evolution statistics"""
        stats = self.evolution_stats.copy()
        
        if stats["agents_evolved"] > 0:
            stats["average_improvement"] = stats["total_performance_improvement"] / stats["agents_evolved"]
            stats["success_rate"] = (stats["successful_evolutions"] / stats["agents_evolved"]) * 100
        else:
            stats["average_improvement"] = 0.0
            stats["success_rate"] = 0.0
        
        return stats
    
    def get_available_strategies(self) -> Dict[str, CapabilityEvolutionStrategy]:
        """Trả về available evolution strategies"""
        return self.evolution_strategies.copy() 