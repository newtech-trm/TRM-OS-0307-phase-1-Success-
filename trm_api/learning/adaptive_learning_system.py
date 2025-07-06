"""
Adaptive Learning System - Main Orchestrator

Coordinates all learning components and integrates with TRM-OS systems.
Follows TRM-OS philosophy: Recognition → Event → WIN through continuous learning.
"""

import logging
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Union, Set
from uuid import uuid4

from .learning_types import (
    LearningExperience,
    LearningPattern,
    AdaptationRule,
    LearningGoal,
    LearningSession,
    ExperienceType,
    MetricType,
    AdaptationType,
    safe_enum_value
)
from .experience_collector import ExperienceCollector
from .pattern_recognizer import PatternRecognizer
from .adaptation_engine import AdaptationEngine
from .performance_tracker import PerformanceTracker

from ..eventbus.system_event_bus import publish_event, EventType
from ..reasoning.advanced_reasoning_engine import AdvancedReasoningEngine


class AdaptiveLearningSystem:
    """Main orchestrator for adaptive learning capabilities"""
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.logger = logging.getLogger(f"learning.adaptive_system.{agent_id}")
        
        # Core components
        self.experience_collector = ExperienceCollector(agent_id)
        self.pattern_recognizer = PatternRecognizer(agent_id)
        self.adaptation_engine = AdaptationEngine(agent_id)
        self.performance_tracker = PerformanceTracker(agent_id)
        
        # Learning configuration
        self.learning_enabled = True
        self.auto_adaptation_enabled = True
        self.learning_frequency_hours = 24  # Run learning cycle every 24 hours
        self.min_experiences_for_learning = 10  # Minimum experiences needed to trigger learning
        
        # Learning goals and state
        self.learning_goals: Dict[str, LearningGoal] = {}
        self.active_learning_sessions: Dict[str, LearningSession] = {}
        self.last_learning_cycle: Optional[datetime] = None
        self.reasoning_engine: Optional[AdvancedReasoningEngine] = None
        
        # Background task management
        self.background_tasks: Set[asyncio.Task] = set()
        self.learning_cycle_task: Optional[asyncio.Task] = None
        
        # System statistics
        self.system_stats = {
            "total_learning_cycles": 0,
            "total_experiences_processed": 0,
            "total_patterns_discovered": 0,
            "total_adaptations_applied": 0,
            "goals_achieved": 0,
            "average_cycle_time": 0.0
        }
        
        self.logger.info(f"Initialized Adaptive Learning System for agent {agent_id}")
    
    async def initialize(self, reasoning_engine: Optional[AdvancedReasoningEngine] = None) -> None:
        """Initialize the learning system with optional reasoning engine integration"""
        
        self.reasoning_engine = reasoning_engine
        
        # Set up default learning goals
        await self._setup_default_goals()
        
        # Start background learning cycle
        if self.learning_enabled:
            self.learning_cycle_task = asyncio.create_task(self._learning_cycle_loop())
            self.background_tasks.add(self.learning_cycle_task)
        
        self.logger.info("Adaptive Learning System initialized and ready")
        
        # Create system initialization event
        await publish_event(
            event_type=EventType.AGENT_ACTION_COMPLETED,
            source_agent_id=self.agent_id,
            entity_id=f"learning_system_{self.agent_id}",
            entity_type="learning_system",
            data={
                "action": "system_initialized",
                "learning_enabled": self.learning_enabled,
                "auto_adaptation_enabled": self.auto_adaptation_enabled
            }
        )
    
    async def _setup_default_goals(self) -> None:
        """Set up default learning goals for the agent"""
        
        # Goal 1: Improve task execution efficiency
        efficiency_goal = LearningGoal(
            agent_id=self.agent_id,
            name="Improve Task Execution Efficiency",
            description="Continuously improve the efficiency of task execution",
            target_metrics={
                MetricType.EFFICIENCY: 0.9,
                MetricType.SUCCESS_RATE: 0.95
            },
            priority=8,
            learning_strategies=["pattern_recognition", "performance_optimization"],
            adaptation_preferences=[
                AdaptationType.PARAMETER_ADJUSTMENT,
                AdaptationType.STRATEGY_CHANGE
            ]
        )
        
        # Goal 2: Enhance decision-making accuracy
        accuracy_goal = LearningGoal(
            agent_id=self.agent_id,
            name="Enhance Decision-Making Accuracy",
            description="Improve the accuracy of decisions and predictions",
            target_metrics={
                MetricType.ACCURACY: 0.92,
                MetricType.CONFIDENCE: 0.85
            },
            priority=7,
            learning_strategies=["causal_analysis", "context_learning"],
            adaptation_preferences=[
                AdaptationType.THRESHOLD_MODIFICATION,
                AdaptationType.BEHAVIOR_MODIFICATION
            ]
        )
        
        # Goal 3: Optimize learning speed
        learning_goal = LearningGoal(
            agent_id=self.agent_id,
            name="Optimize Learning Speed",
            description="Improve the rate at which new patterns are learned and applied",
            target_metrics={
                MetricType.LEARNING_SPEED: 0.8,
                MetricType.ADAPTATION_RATE: 0.7
            },
            priority=6,
            learning_strategies=["meta_learning", "transfer_learning"],
            adaptation_preferences=[
                AdaptationType.KNOWLEDGE_UPDATE,
                AdaptationType.PARAMETER_ADJUSTMENT
            ]
        )
        
        # Store goals
        self.learning_goals[efficiency_goal.goal_id] = efficiency_goal
        self.learning_goals[accuracy_goal.goal_id] = accuracy_goal
        self.learning_goals[learning_goal.goal_id] = learning_goal
        
        self.logger.info(f"Set up {len(self.learning_goals)} default learning goals")
    
    async def learn_from_experience(
        self,
        experience_type_or_obj,
        context: Dict[str, Any] = None,
        action_taken: Dict[str, Any] = None,
        outcome: Dict[str, Any] = None,
        success: bool = None,
        performance_metrics: Dict[str, float] = None,
        confidence_level: float = 0.5
    ) -> str:
        """Learn from a single experience - supports both individual parameters and LearningExperience object"""
        
        # Check if first parameter is a LearningExperience object
        if hasattr(experience_type_or_obj, 'experience_type'):
            # It's a LearningExperience object
            experience = experience_type_or_obj
            experience_type = experience.experience_type
            context = experience.context
            action_taken = experience.action_taken
            outcome = experience.outcome
            success = experience.success
            performance_metrics = getattr(experience, 'performance_metrics', None)
            confidence_level = experience.confidence_level
        else:
            # It's individual parameters
            experience_type = experience_type_or_obj
            
            # Validate required parameters
            if context is None or action_taken is None or outcome is None or success is None:
                raise ValueError("Missing required parameters for learn_from_experience")
        
        # Validate experience_type
        if isinstance(experience_type, str):
            try:
                experience_type = ExperienceType(experience_type)
            except ValueError:
                raise ValueError(f"Invalid experience type: {experience_type}")
        elif not isinstance(experience_type, ExperienceType):
            raise ValueError(f"Experience type must be ExperienceType enum or valid string, got: {type(experience_type)}")
        
        # Collect the experience
        experience_id = await self.experience_collector.collect_task_experience(
            task_id=context.get("task_id", str(uuid4())),
            action_taken=action_taken,
            outcome=outcome,
            success=success,
            performance_before=performance_metrics or {},
            performance_after=performance_metrics or {},
            context=context
        )
        
        # Record performance metrics if provided
        if performance_metrics:
            for metric_name, value in performance_metrics.items():
                try:
                    metric_type = MetricType(metric_name)
                    await self.performance_tracker.record_performance_metric(
                        metric_type=metric_type,
                        value=value,
                        context=context
                    )
                except ValueError:
                    # Skip unknown metric types
                    pass
        
        # Check if we should trigger immediate learning
        total_experiences = len(self.experience_collector.experiences)
        if total_experiences >= self.min_experiences_for_learning:
            # Trigger learning cycle if enough new experiences
            if self.last_learning_cycle is None or \
               (datetime.now() - self.last_learning_cycle).total_seconds() > 3600:  # 1 hour
                asyncio.create_task(self.run_learning_cycle())
        
        return experience_id
    
    async def learn_from_experience_obj(self, experience: LearningExperience) -> str:
        """Learn from a LearningExperience object (deprecated - use learn_from_experience)"""
        return await self.learn_from_experience(experience)
    
    async def run_learning_cycle(self) -> Dict[str, Any]:
        """Run a complete learning cycle"""
        
        if not self.learning_enabled:
            return {"status": "disabled", "message": "Learning is disabled"}
        
        cycle_start = datetime.now()
        self.logger.info("Starting learning cycle")
        
        cycle_results = {
            "cycle_id": str(uuid4()),
            "started_at": cycle_start,
            "experiences_analyzed": 0,
            "patterns_discovered": 0,
            "adaptations_generated": 0,
            "adaptations_applied": 0,
            "goals_updated": 0,
            "performance_improvements": {},
            "success": False
        }
        
        try:
            # Step 1: Analyze experiences to discover patterns
            experiences = list(self.experience_collector.experiences.values())
            cycle_results["experiences_analyzed"] = len(experiences)
            
            if len(experiences) >= self.min_experiences_for_learning:
                # Discover patterns
                patterns = await self.pattern_recognizer.analyze_experiences(experiences)
                cycle_results["patterns_discovered"] = len(patterns)
                
                # Step 2: Generate adaptations from patterns
                if patterns:
                    current_performance = self.performance_tracker.get_current_performance()
                    adaptation_rules = await self.adaptation_engine.generate_adaptations_from_patterns(
                        patterns, current_performance
                    )
                    cycle_results["adaptations_generated"] = len(adaptation_rules)
                    
                    # Step 3: Apply adaptations if auto-adaptation is enabled
                    if self.auto_adaptation_enabled and adaptation_rules:
                        # Create context for adaptation
                        adaptation_context = {
                            "agent_id": self.agent_id,
                            "learning_cycle": True,
                            "current_performance": current_performance,
                            "available_patterns": len(patterns)
                        }
                        
                        applied_adaptations = await self.adaptation_engine.apply_adaptations(
                            adaptation_context, adaptation_rules
                        )
                        cycle_results["adaptations_applied"] = len(applied_adaptations)
                
                # Step 4: Update learning goals based on progress
                goals_updated = await self._update_learning_goals()
                cycle_results["goals_updated"] = goals_updated
                
                # Step 5: Analyze performance improvements
                performance_analysis = await self.performance_tracker.analyze_performance_trends()
                cycle_results["performance_improvements"] = performance_analysis
                
                # Step 6: Integration with reasoning engine
                if self.reasoning_engine:
                    await self._integrate_with_reasoning_engine(patterns, adaptation_rules)
            
            # Update system statistics
            self.system_stats["total_learning_cycles"] += 1
            self.system_stats["total_experiences_processed"] += len(experiences)
            self.system_stats["total_patterns_discovered"] += cycle_results["patterns_discovered"]
            self.system_stats["total_adaptations_applied"] += cycle_results["adaptations_applied"]
            
            self.last_learning_cycle = cycle_start
            cycle_results["success"] = True
            
            cycle_end = datetime.now()
            cycle_duration = (cycle_end - cycle_start).total_seconds()
            
            self.system_stats["average_cycle_time"] = (
                self.system_stats["average_cycle_time"] * 0.9 + cycle_duration * 0.1
            )
            
            self.logger.info(
                f"Learning cycle completed in {cycle_duration:.2f}s: "
                f"{cycle_results['patterns_discovered']} patterns, "
                f"{cycle_results['adaptations_applied']} adaptations applied"
            )
            
            # Create learning cycle completion event
            await publish_event(
                event_type=EventType.KNOWLEDGE_CREATED,
                source_agent_id=self.agent_id,
                entity_id=cycle_results["cycle_id"],
                entity_type="learning_cycle",
                data={
                    "experiences_analyzed": cycle_results["experiences_analyzed"],
                    "patterns_discovered": cycle_results["patterns_discovered"],
                    "adaptations_applied": cycle_results["adaptations_applied"],
                    "duration_seconds": cycle_duration
                }
            )
            
        except Exception as e:
            self.logger.error(f"Learning cycle failed: {str(e)}")
            cycle_results["success"] = False
            cycle_results["error"] = str(e)
        
        cycle_results["completed_at"] = datetime.now()
        cycle_results["duration_seconds"] = (cycle_results["completed_at"] - cycle_start).total_seconds()
        
        return cycle_results
    
    async def _update_learning_goals(self) -> int:
        """Update learning goals based on current performance"""
        
        goals_updated = 0
        current_performance = self.performance_tracker.get_current_performance()
        
        self.logger.debug(f"Updating learning goals. Current performance: {current_performance}")
        self.logger.debug(f"Number of learning goals: {len(self.learning_goals)}")
        
        for goal in self.learning_goals.values():
            updated = False
            
            self.logger.debug(f"Processing goal: {goal.name}, target_metrics: {goal.target_metrics}")
            
            # Update current progress
            for metric_type, target_value in goal.target_metrics.items():
                current_value = None
                
                # Handle both string and enum keys
                if isinstance(metric_type, str):
                    # Convert string to enum
                    for enum_metric, perf_value in current_performance.items():
                        if enum_metric.value == metric_type:
                            current_value = perf_value
                            break
                else:
                    # Direct enum lookup
                    if metric_type in current_performance:
                        current_value = current_performance[metric_type]
                
                if current_value is not None:
                    goal.current_progress[metric_type] = current_value
                    updated = True
                    self.logger.debug(f"Updated progress for {metric_type}: {current_value} (target: {target_value})")
                else:
                    self.logger.debug(f"No current performance data for {metric_type}")
            
            # Calculate completion percentage
            if goal.target_metrics and goal.current_progress:
                completion_scores = []
                for metric_type, target_value in goal.target_metrics.items():
                    if metric_type in goal.current_progress:
                        current_value = goal.current_progress[metric_type]
                        if target_value > 0:
                            completion_score = min(1.0, current_value / target_value)
                        else:
                            completion_score = 1.0 if current_value >= target_value else 0.0
                        completion_scores.append(completion_score)
                        self.logger.debug(f"Completion score for {metric_type}: {completion_score}")
                
                if completion_scores:
                    goal.completion_percentage = (sum(completion_scores) / len(completion_scores)) * 100
                    updated = True
                    self.logger.debug(f"Goal completion percentage: {goal.completion_percentage}%")
            
            # Check if goal is completed
            if goal.completion_percentage >= 100 and goal.status == "active":
                goal.status = "completed"
                goal.completed_at = datetime.now()
                self.system_stats["goals_achieved"] += 1
                updated = True
                
                self.logger.info(f"Learning goal achieved: {goal.name}")
                
                # Create goal achievement event
                await publish_event(
                    event_type=EventType.AGENT_ACTION_COMPLETED,
                    source_agent_id=self.agent_id,
                    entity_id=goal.goal_id,
                    entity_type="learning_goal",
                    data={
                        "action": "goal_achieved",
                        "goal_name": goal.name,
                        "completion_percentage": goal.completion_percentage,
                        "target_metrics": goal.target_metrics
                    }
                )
            
            if updated:
                goals_updated += 1
                self.logger.debug(f"Goal {goal.name} was updated")
        
        self.logger.debug(f"Total goals updated: {goals_updated}")
        return goals_updated
    
    async def _integrate_with_reasoning_engine(
        self,
        patterns: List[LearningPattern],
        adaptation_rules: List[AdaptationRule]
    ) -> None:
        """Integrate learning insights with reasoning engine"""
        
        if not self.reasoning_engine:
            return
        
        # Create reasoning context with learning insights
        learning_context = {
            "agent_id": self.agent_id,
            "learning_patterns": [
                {
                    "pattern_type": pattern.pattern_type,
                    "confidence": pattern.confidence,
                    "description": pattern.description
                }
                for pattern in patterns
            ],
            "adaptation_rules": [
                {
                    "rule_name": rule.name,
                    "adaptation_type": rule.adaptation_type.value,
                    "priority": rule.priority
                }
                for rule in adaptation_rules
            ],
            "performance_trends": self.performance_tracker.get_current_performance()
        }
        
        # This would integrate with the reasoning engine
        # For now, just log the integration
        self.logger.info(f"Integrated {len(patterns)} patterns and {len(adaptation_rules)} adaptations with reasoning engine")
    
    async def _learning_cycle_loop(self) -> None:
        """Background loop for periodic learning cycles"""
        
        try:
            while self.learning_enabled:
                try:
                    # Wait for the specified interval
                    await asyncio.sleep(self.learning_frequency_hours * 3600)
                    
                    # Run learning cycle if we have enough experiences
                    if len(self.experience_collector.experiences) >= self.min_experiences_for_learning:
                        await self.run_learning_cycle()
                    
                except asyncio.CancelledError:
                    # Task was cancelled, break the loop
                    self.logger.info("Learning cycle loop cancelled")
                    break
                except Exception as e:
                    self.logger.error(f"Error in learning cycle loop: {str(e)}")
                    # Wait 1 hour before retrying, but allow cancellation
                    try:
                        await asyncio.sleep(3600)
                    except asyncio.CancelledError:
                        self.logger.info("Learning cycle loop cancelled during retry wait")
                        break
        except asyncio.CancelledError:
            # Handle cancellation at the top level
            self.logger.info("Learning cycle loop task cancelled")
        finally:
            # Cleanup when loop ends
            self.logger.info("Learning cycle loop ended")
    
    async def add_learning_goal(self, goal: LearningGoal) -> str:
        """Add a new learning goal"""
        
        self.learning_goals[goal.goal_id] = goal
        
        self.logger.info(f"Added learning goal: {goal.name}")
        
        # Create goal creation event
        await publish_event(
            event_type=EventType.KNOWLEDGE_CREATED,
            source_agent_id=self.agent_id,
            entity_id=goal.goal_id,
            entity_type="learning_goal",
            data={
                "goal_name": goal.name,
                "priority": goal.priority,
                "target_metrics": goal.target_metrics
            }
        )
        
        return goal.goal_id
    
    async def set_performance_target(
        self,
        metric_type: MetricType,
        target_value: float
    ) -> None:
        """Set a performance target"""
        
        self.performance_tracker.set_performance_target(metric_type, target_value)
        
        self.logger.info(f"Set performance target: {metric_type.value} = {target_value}")
    
    def get_learning_status(self) -> Dict[str, Any]:
        """Get comprehensive learning system status"""
        
        return {
            "agent_id": self.agent_id,
            "learning_enabled": self.learning_enabled,
            "auto_adaptation_enabled": self.auto_adaptation_enabled,
            "last_learning_cycle": self.last_learning_cycle,
            "system_stats": self.system_stats.copy(),
            "component_stats": {
                "experience_collector": self.experience_collector.get_statistics(),
                "pattern_recognizer": self.pattern_recognizer.get_statistics(),
                "adaptation_engine": self.adaptation_engine.get_statistics(),
                "performance_tracker": self.performance_tracker.get_statistics()
            },
            "learning_goals": {
                goal_id: {
                    "name": goal.name,
                    "status": goal.status,
                    "completion_percentage": goal.completion_percentage,
                    "priority": goal.priority
                }
                for goal_id, goal in self.learning_goals.items()
            },
            "active_adaptations": self.adaptation_engine.get_active_adaptations(),
            "current_performance": self.performance_tracker.get_current_performance()
        }
    
    def get_learning_insights(self) -> Dict[str, Any]:
        """Get learning insights and recommendations"""
        
        insights = {
            "discovered_patterns": [
                {
                    "pattern_type": pattern.pattern_type,
                    "confidence": pattern.confidence,
                    "strength": pattern.strength,
                    "description": pattern.description
                }
                for pattern in self.pattern_recognizer.discovered_patterns.values()
            ],
            "active_adaptations": self.adaptation_engine.get_active_adaptations(),
            "performance_trends": {},
            "recommendations": []
        }
        
        # Add performance trend analysis (sync version)
        try:
            # Get basic trend information from performance tracker
            current_performance = self.performance_tracker.get_current_performance()
            insights["performance_trends"] = {
                safe_enum_value(metric_type): value
                for metric_type, value in current_performance.items()
            }
        except Exception as e:
            self.logger.error(f"Error analyzing performance trends: {str(e)}")
        
        # Generate recommendations
        recommendations = []
        
        # Check for goals that need attention
        for goal in self.learning_goals.values():
            if goal.status == "active" and goal.completion_percentage < 50:
                recommendations.append({
                    "type": "goal_attention",
                    "priority": "medium",
                    "description": f"Goal '{goal.name}' is at {goal.completion_percentage:.1f}% completion and may need attention"
                })
        
        # Check for patterns that suggest improvements
        high_confidence_patterns = [
            pattern for pattern in self.pattern_recognizer.discovered_patterns.values()
            if pattern.confidence > 0.8
        ]
        
        if high_confidence_patterns:
            recommendations.append({
                "type": "pattern_exploitation",
                "priority": "high",
                "description": f"Found {len(high_confidence_patterns)} high-confidence patterns that could be leveraged for better performance"
            })
        
        insights["recommendations"] = recommendations
        
        return insights
    
    def enable_learning(self) -> None:
        """Enable learning system"""
        self.learning_enabled = True
        self.logger.info("Learning system enabled")
    
    def disable_learning(self) -> None:
        """Disable learning system"""
        self.learning_enabled = False
        self.logger.info("Learning system disabled")
    
    def enable_auto_adaptation(self) -> None:
        """Enable automatic adaptation"""
        self.auto_adaptation_enabled = True
        self.logger.info("Auto-adaptation enabled")
    
    def disable_auto_adaptation(self) -> None:
        """Disable automatic adaptation"""
        self.auto_adaptation_enabled = False
        self.logger.info("Auto-adaptation disabled")
    
    async def cleanup(self) -> None:
        """Clean up background tasks and resources"""
        
        # Cancel background tasks
        for task in self.background_tasks:
            if not task.done():
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass
        
        self.background_tasks.clear()
        self.learning_cycle_task = None
        
        self.logger.info("Adaptive Learning System cleaned up")
    
    async def reset_learning_system(self) -> None:
        """Reset the entire learning system"""
        
        # Cancel background tasks first
        await self.cleanup()
        
        # Reset all components
        self.experience_collector.clear_experiences()
        self.pattern_recognizer.clear_patterns()
        self.adaptation_engine.clear_adaptations()
        self.performance_tracker.clear_performance_data()
        
        # Reset learning goals and state
        self.learning_goals.clear()
        self.last_learning_cycle = None
        
        # Reset system statistics
        self.system_stats = {
            "total_learning_cycles": 0,
            "total_experiences_processed": 0,
            "total_patterns_discovered": 0,
            "total_adaptations_applied": 0,
            "goals_achieved": 0,
            "average_cycle_time": 0.0
        }
        
        # Set up default goals again
        await self._setup_default_goals()
        
        self.logger.info("Learning system reset completed")
        
        # Restart background tasks if learning is enabled
        if self.learning_enabled:
            self.learning_cycle_task = asyncio.create_task(self._learning_cycle_loop())
            self.background_tasks.add(self.learning_cycle_task)
        
        # Create reset event
        await publish_event(
            event_type=EventType.AGENT_ACTION_COMPLETED,
            source_agent_id=self.agent_id,
            entity_id=f"learning_system_{self.agent_id}",
            entity_type="learning_system",
            data={
                "action": "system_reset",
                "reset_at": datetime.now()
            }
        )
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get system statistics for compatibility with other components"""
        status = self.get_learning_status()
        return {
            "learning_effectiveness": status["system_stats"]["average_cycle_time"],
            "adaptation_success_rate": status["system_stats"]["total_adaptations_applied"] / max(1, status["system_stats"]["total_learning_cycles"]),
            "total_learning_cycles": status["system_stats"]["total_learning_cycles"],
            "total_experiences_processed": status["system_stats"]["total_experiences_processed"],
            "total_patterns_discovered": status["system_stats"]["total_patterns_discovered"],
            "total_adaptations_applied": status["system_stats"]["total_adaptations_applied"],
            "goals_achieved": status["system_stats"]["goals_achieved"],
            "average_cycle_time": status["system_stats"]["average_cycle_time"]
        }
    
    async def start_learning_cycle(self) -> None:
        # Implementation of start_learning_cycle method
        pass 