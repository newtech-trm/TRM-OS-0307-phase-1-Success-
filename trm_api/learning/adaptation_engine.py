"""
Adaptation Engine for Adaptive Learning System

Adjusts agent behavior based on learned patterns and performance data.
Follows TRM-OS philosophy: Recognition → Event → WIN through behavioral adaptation.
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from uuid import uuid4
import json

from .learning_types import (
    LearningPattern,
    AdaptationRule,
    AdaptationType,
    LearningExperience,
    PerformanceMetric,
    MetricType,
    safe_enum_value
)
from ..eventbus.system_event_bus import publish_event, EventType


class AdaptationEngine:
    """Manages behavioral adaptations based on learning patterns"""
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.logger = logging.getLogger(f"learning.adaptation_engine.{agent_id}")
        
        # Adaptation storage
        self.adaptation_rules: Dict[str, AdaptationRule] = {}
        self.adaptation_history: List[Dict[str, Any]] = []
        
        # Current adaptations applied
        self.active_adaptations: Dict[str, Any] = {}
        
        # Adaptation parameters
        self.adaptation_threshold = 0.7        # Minimum confidence to apply adaptation
        self.max_concurrent_adaptations = 5    # Maximum simultaneous adaptations
        self.adaptation_cooldown = 3600        # Seconds between same adaptations
        
        # Performance tracking
        self.adaptation_stats = {
            "total_adaptations_applied": 0,
            "successful_adaptations": 0,
            "failed_adaptations": 0,
            "adaptations_by_type": {},
            "avg_effectiveness": 0.0
        }
    
    async def generate_adaptations_from_patterns(
        self, 
        patterns: List[LearningPattern],
        current_performance: Dict[MetricType, float] = None
    ) -> List[AdaptationRule]:
        """Generate adaptation rules from discovered patterns"""
        
        adaptation_rules = []
        
        for pattern in patterns:
            # Generate adaptations based on pattern type
            if pattern.pattern_type == "success_rate":
                rules = await self._generate_success_rate_adaptations(pattern)
                adaptation_rules.extend(rules)
            
            elif pattern.pattern_type == "temporal_performance":
                rules = await self._generate_temporal_adaptations(pattern)
                adaptation_rules.extend(rules)
            
            elif pattern.pattern_type == "context_correlation":
                rules = await self._generate_context_adaptations(pattern)
                adaptation_rules.extend(rules)
            
            elif pattern.pattern_type == "performance_improvement":
                rules = await self._generate_performance_adaptations(pattern)
                adaptation_rules.extend(rules)
            
            elif pattern.pattern_type == "action_outcome":
                rules = await self._generate_action_adaptations(pattern)
                adaptation_rules.extend(rules)
        
        # Store valid adaptation rules
        valid_rules = []
        for rule in adaptation_rules:
            if await self._validate_adaptation_rule(rule):
                await self._store_adaptation_rule(rule)
                valid_rules.append(rule)
        
        self.logger.info(f"Generated {len(valid_rules)} adaptation rules from {len(patterns)} patterns")
        
        return valid_rules
    
    async def _generate_success_rate_adaptations(
        self, 
        pattern: LearningPattern
    ) -> List[AdaptationRule]:
        """Generate adaptations for success rate patterns"""
        
        rules = []
        
        if pattern.success_rate >= 0.8:
            # High success rate - prioritize this approach
            rule = AdaptationRule(
                adaptation_type=AdaptationType.PRIORITY_REORDERING,
                agent_id=self.agent_id,
                name=f"Prioritize {pattern.conditions.get('experience_type', 'unknown')} approach",
                description=f"Increase priority for {pattern.conditions.get('experience_type')} "
                          f"based on {pattern.success_rate:.1%} success rate",
                trigger_conditions={
                    "experience_type": pattern.conditions.get("experience_type"),
                    "min_confidence": 0.6
                },
                adaptation_actions={
                    "action": "increase_priority",
                    "experience_type": pattern.conditions.get("experience_type"),
                    "priority_boost": 2
                },
                priority=8,
                confidence_threshold=0.6
            )
            rules.append(rule)
        
        elif pattern.success_rate <= 0.2:
            # Low success rate - avoid this approach
            rule = AdaptationRule(
                adaptation_type=AdaptationType.STRATEGY_CHANGE,
                agent_id=self.agent_id,
                name=f"Avoid {pattern.conditions.get('experience_type', 'unknown')} approach",
                description=f"Avoid {pattern.conditions.get('experience_type')} "
                          f"due to {pattern.success_rate:.1%} success rate",
                trigger_conditions={
                    "experience_type": pattern.conditions.get("experience_type"),
                    "min_confidence": 0.5
                },
                adaptation_actions={
                    "action": "avoid_approach",
                    "experience_type": pattern.conditions.get("experience_type"),
                    "alternative_required": True
                },
                priority=7,
                confidence_threshold=0.5
            )
            rules.append(rule)
        
        return rules
    
    async def _generate_temporal_adaptations(
        self, 
        pattern: LearningPattern
    ) -> List[AdaptationRule]:
        """Generate adaptations for temporal patterns"""
        
        rules = []
        
        if pattern.pattern_type == "temporal_performance":
            if "peak_hours" in pattern.outcomes:
                peak_hours = pattern.outcomes["peak_hours"]
                rule = AdaptationRule(
                    adaptation_type=AdaptationType.RESOURCE_ALLOCATION,
                    agent_id=self.agent_id,
                    name="Optimize scheduling for peak hours",
                    description=f"Schedule important tasks during peak hours: {peak_hours}",
                    trigger_conditions={
                        "scheduling_decision": True,
                        "task_importance": "high"
                    },
                    adaptation_actions={
                        "action": "prefer_time_slots",
                        "preferred_hours": peak_hours,
                        "importance_threshold": 0.7
                    },
                    priority=6,
                    confidence_threshold=0.6
                )
                rules.append(rule)
            
            if "best_days" in pattern.outcomes:
                best_days = pattern.outcomes["best_days"]
                rule = AdaptationRule(
                    adaptation_type=AdaptationType.RESOURCE_ALLOCATION,
                    agent_id=self.agent_id,
                    name="Optimize scheduling for best days",
                    description=f"Schedule important tasks on best days: {best_days}",
                    trigger_conditions={
                        "weekly_planning": True,
                        "task_importance": "high"
                    },
                    adaptation_actions={
                        "action": "prefer_days",
                        "preferred_days": best_days,
                        "importance_threshold": 0.7
                    },
                    priority=5,
                    confidence_threshold=0.6
                )
                rules.append(rule)
        
        return rules
    
    async def _generate_context_adaptations(
        self, 
        pattern: LearningPattern
    ) -> List[AdaptationRule]:
        """Generate adaptations for context correlation patterns"""
        
        rules = []
        
        context_key = pattern.conditions.get("context_key")
        context_value = pattern.conditions.get("context_value")
        
        if context_key and context_value and pattern.success_rate:
            if pattern.success_rate >= 0.8:
                # Favorable context - seek it out
                rule = AdaptationRule(
                    adaptation_type=AdaptationType.BEHAVIOR_MODIFICATION,
                    agent_id=self.agent_id,
                    name=f"Seek favorable context: {context_key}={context_value}",
                    description=f"Prefer contexts where {context_key}={context_value} "
                              f"(success rate: {pattern.success_rate:.1%})",
                    trigger_conditions={
                        "context_selection": True,
                        "alternatives_available": True
                    },
                    adaptation_actions={
                        "action": "prefer_context",
                        "context_key": context_key,
                        "context_value": context_value,
                        "preference_weight": pattern.confidence
                    },
                    priority=6,
                    confidence_threshold=0.6
                )
                rules.append(rule)
            
            elif pattern.success_rate <= 0.2:
                # Unfavorable context - avoid it
                rule = AdaptationRule(
                    adaptation_type=AdaptationType.BEHAVIOR_MODIFICATION,
                    agent_id=self.agent_id,
                    name=f"Avoid unfavorable context: {context_key}={context_value}",
                    description=f"Avoid contexts where {context_key}={context_value} "
                              f"(success rate: {pattern.success_rate:.1%})",
                    trigger_conditions={
                        "context_selection": True,
                        "alternatives_available": True
                    },
                    adaptation_actions={
                        "action": "avoid_context",
                        "context_key": context_key,
                        "context_value": context_value,
                        "avoidance_weight": pattern.confidence
                    },
                    priority=7,
                    confidence_threshold=0.5
                )
                rules.append(rule)
        
        return rules
    
    async def _generate_performance_adaptations(
        self, 
        pattern: LearningPattern
    ) -> List[AdaptationRule]:
        """Generate adaptations for performance improvement patterns"""
        
        rules = []
        
        experience_type = pattern.conditions.get("experience_type")
        metric = pattern.conditions.get("metric")
        expected_improvement = pattern.outcomes.get("expected_improvement")
        
        if experience_type and metric and expected_improvement:
            rule = AdaptationRule(
                adaptation_type=AdaptationType.PARAMETER_ADJUSTMENT,
                agent_id=self.agent_id,
                name=f"Optimize {metric} for {experience_type}",
                description=f"Apply optimizations that improve {metric} "
                          f"by {expected_improvement:.1%} for {experience_type}",
                trigger_conditions={
                    "experience_type": experience_type,
                    "metric_focus": metric,
                    "improvement_target": expected_improvement
                },
                adaptation_actions={
                    "action": "apply_optimization",
                    "experience_type": experience_type,
                    "target_metric": metric,
                    "expected_improvement": expected_improvement
                },
                priority=6,
                confidence_threshold=0.6
            )
            rules.append(rule)
        
        return rules
    
    async def _generate_action_adaptations(
        self, 
        pattern: LearningPattern
    ) -> List[AdaptationRule]:
        """Generate adaptations for action-outcome patterns"""
        
        rules = []
        
        action_signature = pattern.conditions.get("action_signature")
        success_rate = pattern.success_rate
        
        if action_signature and success_rate is not None:
            if success_rate >= 0.8:
                # Successful action pattern - use more often
                rule = AdaptationRule(
                    adaptation_type=AdaptationType.STRATEGY_CHANGE,
                    agent_id=self.agent_id,
                    name=f"Favor successful action pattern",
                    description=f"Increase usage of action pattern '{action_signature}' "
                              f"(success rate: {success_rate:.1%})",
                    trigger_conditions={
                        "action_selection": True,
                        "pattern_match": action_signature
                    },
                    adaptation_actions={
                        "action": "increase_pattern_usage",
                        "action_signature": action_signature,
                        "usage_boost": pattern.confidence
                    },
                    priority=7,
                    confidence_threshold=0.6
                )
                rules.append(rule)
            
            elif success_rate <= 0.2:
                # Unsuccessful action pattern - use less often
                rule = AdaptationRule(
                    adaptation_type=AdaptationType.STRATEGY_CHANGE,
                    agent_id=self.agent_id,
                    name=f"Reduce unsuccessful action pattern",
                    description=f"Decrease usage of action pattern '{action_signature}' "
                              f"(success rate: {success_rate:.1%})",
                    trigger_conditions={
                        "action_selection": True,
                        "pattern_match": action_signature
                    },
                    adaptation_actions={
                        "action": "decrease_pattern_usage",
                        "action_signature": action_signature,
                        "usage_reduction": pattern.confidence
                    },
                    priority=6,
                    confidence_threshold=0.5
                )
                rules.append(rule)
        
        return rules
    
    async def apply_adaptations(
        self, 
        context: Dict[str, Any],
        available_rules: List[AdaptationRule] = None
    ) -> List[Dict[str, Any]]:
        """Apply relevant adaptations based on current context"""
        
        if available_rules is None:
            available_rules = list(self.adaptation_rules.values())
        
        # Filter applicable rules
        applicable_rules = []
        for rule in available_rules:
            if await self._is_rule_applicable(rule, context):
                applicable_rules.append(rule)
        
        # Sort by priority and confidence
        applicable_rules.sort(
            key=lambda r: (r.priority, r.confidence_threshold), 
            reverse=True
        )
        
        # Apply adaptations (respecting concurrent limit)
        applied_adaptations = []
        current_concurrent = len(self.active_adaptations)
        
        for rule in applicable_rules:
            if current_concurrent >= self.max_concurrent_adaptations:
                break
            
            if await self._can_apply_rule(rule):
                adaptation_result = await self._apply_adaptation_rule(rule, context)
                if adaptation_result:
                    applied_adaptations.append(adaptation_result)
                    current_concurrent += 1
        
        self.logger.info(f"Applied {len(applied_adaptations)} adaptations from {len(applicable_rules)} applicable rules")
        
        return applied_adaptations
    
    async def _is_rule_applicable(
        self, 
        rule: AdaptationRule, 
        context: Dict[str, Any]
    ) -> bool:
        """Check if adaptation rule is applicable to current context"""
        
        # Check if rule is active
        if not rule.active:
            return False
        
        # Check expiry
        if rule.expiry_date and datetime.now() > rule.expiry_date:
            rule.active = False
            return False
        
        # Check maximum applications
        if rule.max_applications and rule.applications >= rule.max_applications:
            rule.active = False
            return False
        
        # Check cooldown period
        if rule.last_applied:
            time_since_last = (datetime.now() - rule.last_applied).total_seconds()
            if time_since_last < self.adaptation_cooldown:
                return False
        
        # Check trigger conditions
        for condition_key, condition_value in rule.trigger_conditions.items():
            if condition_key not in context:
                return False
            
            context_value = context[condition_key]
            
            # Handle different condition types
            if isinstance(condition_value, bool):
                if context_value != condition_value:
                    return False
            elif isinstance(condition_value, (int, float)):
                if isinstance(context_value, (int, float)):
                    if context_value < condition_value:
                        return False
                else:
                    return False
            elif isinstance(condition_value, str):
                if context_value != condition_value:
                    return False
            elif isinstance(condition_value, list):
                if context_value not in condition_value:
                    return False
        
        return True
    
    async def _can_apply_rule(self, rule: AdaptationRule) -> bool:
        """Check if rule can be applied (not conflicting with active adaptations)"""
        
        # Check for conflicts with active adaptations
        for active_adaptation in self.active_adaptations.values():
            if active_adaptation.get("rule_id") == rule.rule_id:
                return False  # Already applied
            
            # Check for type conflicts
            if active_adaptation.get("adaptation_type") == safe_enum_value(rule.adaptation_type):
                # Same type adaptations might conflict
                if self._adaptations_conflict(active_adaptation, rule):
                    return False
        
        return True
    
    def _adaptations_conflict(
        self, 
        active_adaptation: Dict[str, Any], 
        new_rule: AdaptationRule
    ) -> bool:
        """Check if adaptations conflict with each other"""
        
        # Simple conflict detection - can be made more sophisticated
        active_actions = active_adaptation.get("actions", {})
        new_actions = new_rule.adaptation_actions
        
        # Check for direct conflicts
        for key in active_actions:
            if key in new_actions:
                if active_actions[key] != new_actions[key]:
                    return True  # Conflicting values for same parameter
        
        return False
    
    async def _apply_adaptation_rule(
        self, 
        rule: AdaptationRule, 
        context: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Apply a specific adaptation rule"""
        
        try:
            # Create adaptation instance
            adaptation_id = str(uuid4())
            adaptation = {
                "adaptation_id": adaptation_id,
                "rule_id": rule.rule_id,
                "rule_name": rule.name,
                "adaptation_type": safe_enum_value(rule.adaptation_type),
                "actions": rule.adaptation_actions.copy(),
                "context": context.copy(),
                "applied_at": datetime.now(),
                "status": "active"
            }
            
            # Apply the adaptation
            success = await self._execute_adaptation_actions(rule.adaptation_actions, context)
            
            if success:
                # Store as active adaptation
                self.active_adaptations[adaptation_id] = adaptation
                
                # Update rule statistics
                rule.applications += 1
                rule.last_applied = datetime.now()
                
                # Update global statistics
                self.adaptation_stats["total_adaptations_applied"] += 1
                
                adaptation_type = safe_enum_value(rule.adaptation_type)
                if adaptation_type not in self.adaptation_stats["adaptations_by_type"]:
                    self.adaptation_stats["adaptations_by_type"][adaptation_type] = 0
                self.adaptation_stats["adaptations_by_type"][adaptation_type] += 1
                
                # Add to history
                self.adaptation_history.append({
                    "adaptation_id": adaptation_id,
                    "rule_id": rule.rule_id,
                    "applied_at": datetime.now(),
                    "success": True,
                    "context": context.copy()
                })
                
                self.logger.info(f"Applied adaptation rule {rule.name} (ID: {rule.rule_id})")
                
                # Create adaptation event
                await publish_event(
                    event_type=EventType.AGENT_ACTION_COMPLETED,
                    source_agent_id=self.agent_id,
                    entity_id=adaptation_id,
                    entity_type="adaptation",
                    data={
                        "action": "adaptation_applied",
                        "rule_name": rule.name,
                        "adaptation_type": safe_enum_value(rule.adaptation_type),
                        "priority": rule.priority
                    }
                )
                
                return adaptation
            
            else:
                self.logger.warning(f"Failed to apply adaptation rule {rule.name}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error applying adaptation rule {rule.name}: {str(e)}")
            return None
    
    async def _execute_adaptation_actions(
        self, 
        actions: Dict[str, Any], 
        context: Dict[str, Any]
    ) -> bool:
        """Execute the actual adaptation actions"""
        
        try:
            action_type = actions.get("action")
            
            if action_type == "increase_priority":
                # Increase priority for specific experience type
                experience_type = actions.get("experience_type")
                priority_boost = actions.get("priority_boost", 1)
                
                # This would integrate with agent's decision-making system
                # For now, just log the action
                self.logger.info(f"Increasing priority for {experience_type} by {priority_boost}")
                return True
            
            elif action_type == "avoid_approach":
                # Avoid specific approach
                experience_type = actions.get("experience_type")
                self.logger.info(f"Avoiding approach for {experience_type}")
                return True
            
            elif action_type == "prefer_time_slots":
                # Prefer specific time slots
                preferred_hours = actions.get("preferred_hours", [])
                self.logger.info(f"Preferring time slots: {preferred_hours}")
                return True
            
            elif action_type == "prefer_context":
                # Prefer specific context
                context_key = actions.get("context_key")
                context_value = actions.get("context_value")
                self.logger.info(f"Preferring context {context_key}={context_value}")
                return True
            
            elif action_type == "apply_optimization":
                # Apply performance optimization
                experience_type = actions.get("experience_type")
                target_metric = actions.get("target_metric")
                self.logger.info(f"Applying optimization for {target_metric} in {experience_type}")
                return True
            
            elif action_type == "increase_pattern_usage":
                # Increase usage of successful pattern
                action_signature = actions.get("action_signature")
                self.logger.info(f"Increasing usage of pattern: {action_signature}")
                return True
            
            elif action_type == "decrease_pattern_usage":
                # Decrease usage of unsuccessful pattern
                action_signature = actions.get("action_signature")
                self.logger.info(f"Decreasing usage of pattern: {action_signature}")
                return True
            
            else:
                self.logger.warning(f"Unknown adaptation action: {action_type}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error executing adaptation actions: {str(e)}")
            return False
    
    async def _validate_adaptation_rule(self, rule: AdaptationRule) -> bool:
        """Validate an adaptation rule before storing"""
        
        # Check required fields
        if not rule.name or not rule.description:
            return False
        
        if not rule.trigger_conditions or not rule.adaptation_actions:
            return False
        
        # Check confidence threshold
        if rule.confidence_threshold < 0.0 or rule.confidence_threshold > 1.0:
            return False
        
        # Check priority
        if rule.priority < 1 or rule.priority > 10:
            return False
        
        # Check adaptation actions have required action field
        if "action" not in rule.adaptation_actions:
            return False
        
        return True
    
    async def _store_adaptation_rule(self, rule: AdaptationRule) -> None:
        """Store an adaptation rule"""
        
        self.adaptation_rules[rule.rule_id] = rule
        
        self.logger.info(f"Stored adaptation rule {rule.name} (ID: {rule.rule_id})")
        
        # Create rule creation event
        await publish_event(
            event_type=EventType.KNOWLEDGE_CREATED,
            source_agent_id=self.agent_id,
            entity_id=rule.rule_id,
            entity_type="adaptation_rule",
            data={
                "rule_name": rule.name,
                "adaptation_type": safe_enum_value(rule.adaptation_type),
                "priority": rule.priority,
                "confidence_threshold": rule.confidence_threshold
            }
        )
    
    async def evaluate_adaptation_effectiveness(
        self, 
        adaptation_id: str,
        performance_metrics: Dict[MetricType, float]
    ) -> float:
        """Evaluate the effectiveness of an applied adaptation"""
        
        if adaptation_id not in self.active_adaptations:
            return 0.0
        
        adaptation = self.active_adaptations[adaptation_id]
        rule_id = adaptation["rule_id"]
        
        if rule_id not in self.adaptation_rules:
            return 0.0
        
        rule = self.adaptation_rules[rule_id]
        
        # Simple effectiveness calculation
        # In a real system, this would compare before/after performance
        effectiveness = 0.5  # Default neutral effectiveness
        
        # Update rule effectiveness
        total_applications = rule.applications
        current_effectiveness = rule.effectiveness
        
        # Weighted average of effectiveness
        rule.effectiveness = (
            (current_effectiveness * (total_applications - 1) + effectiveness) / total_applications
        )
        
        # Update global statistics
        if effectiveness > 0.5:
            self.adaptation_stats["successful_adaptations"] += 1
        else:
            self.adaptation_stats["failed_adaptations"] += 1
        
        # Update average effectiveness
        total_adaptations = self.adaptation_stats["total_adaptations_applied"]
        current_avg = self.adaptation_stats["avg_effectiveness"]
        
        self.adaptation_stats["avg_effectiveness"] = (
            (current_avg * (total_adaptations - 1) + effectiveness) / total_adaptations
        )
        
        return effectiveness
    
    def get_active_adaptations(self) -> List[Dict[str, Any]]:
        """Get currently active adaptations"""
        return list(self.active_adaptations.values())
    
    def get_adaptation_rules(self) -> List[AdaptationRule]:
        """Get all adaptation rules"""
        return list(self.adaptation_rules.values())
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get adaptation statistics"""
        return self.adaptation_stats.copy()
    
    def deactivate_adaptation(self, adaptation_id: str) -> bool:
        """Deactivate a specific adaptation"""
        if adaptation_id in self.active_adaptations:
            adaptation = self.active_adaptations.pop(adaptation_id)
            adaptation["status"] = "deactivated"
            adaptation["deactivated_at"] = datetime.now()
            
            self.adaptation_history.append({
                "adaptation_id": adaptation_id,
                "deactivated_at": datetime.now(),
                "reason": "manual_deactivation"
            })
            
            self.logger.info(f"Deactivated adaptation {adaptation_id}")
            return True
        
        return False
    
    def clear_adaptations(self) -> None:
        """Clear all adaptations and rules (use with caution)"""
        self.adaptation_rules.clear()
        self.active_adaptations.clear()
        self.adaptation_history.clear()
        
        self.adaptation_stats = {
            "total_adaptations_applied": 0,
            "successful_adaptations": 0,
            "failed_adaptations": 0,
            "adaptations_by_type": {},
            "avg_effectiveness": 0.0
        }
        
        self.logger.info("Cleared all adaptations and rules")
    
    async def apply_adaptation(
        self, 
        adaptation_rule: AdaptationRule,
        context: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """Apply a single adaptation rule - alias for apply_adaptations"""
        return await self.apply_adaptations(
            context or {},
            available_rules=[adaptation_rule]
        ) 