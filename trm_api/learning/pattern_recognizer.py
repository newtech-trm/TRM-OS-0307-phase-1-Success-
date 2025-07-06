"""
Pattern Recognizer for Adaptive Learning System

Identifies patterns in learning experiences and performance data.
Follows TRM-OS philosophy: Recognition → Event → WIN through pattern discovery.
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Set
from collections import defaultdict, Counter
from statistics import mean, stdev
import math

from .learning_types import (
    LearningExperience, 
    LearningPattern,
    PerformanceMetric,
    ExperienceType,
    MetricType,
    safe_enum_value
)
from ..eventbus.system_event_bus import publish_event, EventType


class PatternRecognizer:
    """Recognizes patterns in learning experiences and performance data"""
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.logger = logging.getLogger(f"learning.pattern_recognizer.{agent_id}")
        
        # Pattern storage
        self.discovered_patterns: Dict[str, LearningPattern] = {}
        
        # Recognition parameters
        self.min_pattern_frequency = 3      # Minimum occurrences to consider a pattern
        self.min_pattern_confidence = 0.6   # Minimum confidence for pattern recognition
        self.pattern_analysis_window = 30   # Days to look back for patterns
        
        # Pattern statistics
        self.recognition_stats = {
            "total_patterns_discovered": 0,
            "patterns_by_type": {},
            "avg_pattern_confidence": 0.0,
            "avg_pattern_strength": 0.0
        }
    
    async def analyze_experiences(
        self, 
        experiences: List[LearningExperience],
        focus_types: List[ExperienceType] = None
    ) -> List[LearningPattern]:
        """Analyze experiences to discover patterns"""
        
        if not experiences:
            return []
        
        # Filter experiences if focus types specified
        if focus_types:
            experiences = [
                exp for exp in experiences 
                if exp.experience_type in focus_types
            ]
        
        discovered_patterns = []
        
        # Analyze different types of patterns
        discovered_patterns.extend(await self._analyze_success_patterns(experiences))
        discovered_patterns.extend(await self._analyze_temporal_patterns(experiences))
        discovered_patterns.extend(await self._analyze_context_patterns(experiences))
        discovered_patterns.extend(await self._analyze_performance_patterns(experiences))
        discovered_patterns.extend(await self._analyze_action_outcome_patterns(experiences))
        
        # Store and validate patterns
        validated_patterns = []
        for pattern in discovered_patterns:
            if await self._validate_pattern(pattern, experiences):
                await self._store_pattern(pattern)
                validated_patterns.append(pattern)
        
        self.logger.info(f"Discovered {len(validated_patterns)} patterns from {len(experiences)} experiences")
        
        return validated_patterns
    
    async def _analyze_success_patterns(
        self, 
        experiences: List[LearningExperience]
    ) -> List[LearningPattern]:
        """Analyze patterns related to success/failure"""
        
        patterns = []
        
        # Group by experience type and success
        success_by_type = defaultdict(list)
        for exp in experiences:
            success_by_type[exp.experience_type].append(exp.success)
        
        for exp_type, success_list in success_by_type.items():
            if len(success_list) >= self.min_pattern_frequency:
                success_rate = sum(success_list) / len(success_list)
                
                if success_rate >= 0.8 or success_rate <= 0.2:  # Strong pattern
                    pattern = LearningPattern(
                        pattern_type="success_rate",
                        agent_id=self.agent_id,
                        description=f"High {'success' if success_rate >= 0.8 else 'failure'} rate "
                                  f"for {safe_enum_value(exp_type)} experiences",
                        conditions={"experience_type": safe_enum_value(exp_type)},
                        outcomes={"expected_success_rate": success_rate},
                        frequency=len(success_list),
                        confidence=min(0.9, success_rate if success_rate >= 0.8 else 1 - success_rate),
                        strength=abs(success_rate - 0.5) * 2,  # Distance from random
                        success_rate=success_rate
                    )
                    patterns.append(pattern)
        
        return patterns
    
    async def _analyze_temporal_patterns(
        self, 
        experiences: List[LearningExperience]
    ) -> List[LearningPattern]:
        """Analyze time-based patterns"""
        
        patterns = []
        
        # Analyze patterns by hour of day
        hourly_performance = defaultdict(list)
        for exp in experiences:
            hour = exp.timestamp.hour
            hourly_performance[hour].append(exp.success)
        
        # Find peak performance hours
        peak_hours = []
        for hour, successes in hourly_performance.items():
            if len(successes) >= 3:  # Minimum sample size
                success_rate = sum(successes) / len(successes)
                if success_rate >= 0.8:
                    peak_hours.append((hour, success_rate))
        
        if peak_hours:
            best_hours = [h for h, rate in sorted(peak_hours, key=lambda x: x[1], reverse=True)[:3]]
            pattern = LearningPattern(
                pattern_type="temporal_performance",
                agent_id=self.agent_id,
                description=f"Peak performance during hours: {best_hours}",
                conditions={"time_constraint": "hour_of_day"},
                outcomes={"peak_hours": best_hours},
                frequency=sum(len(hourly_performance[h]) for h in best_hours),
                confidence=0.7,
                strength=0.6
            )
            patterns.append(pattern)
        
        # Analyze day-of-week patterns
        daily_performance = defaultdict(list)
        for exp in experiences:
            day = exp.timestamp.weekday()  # 0=Monday, 6=Sunday
            daily_performance[day].append(exp.success)
        
        best_days = []
        for day, successes in daily_performance.items():
            if len(successes) >= 3:
                success_rate = sum(successes) / len(successes)
                if success_rate >= 0.8:
                    best_days.append((day, success_rate))
        
        if best_days:
            days_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            best_day_names = [days_names[d] for d, rate in sorted(best_days, key=lambda x: x[1], reverse=True)[:3]]
            pattern = LearningPattern(
                pattern_type="weekly_performance",
                agent_id=self.agent_id,
                description=f"Best performance on: {best_day_names}",
                conditions={"time_constraint": "day_of_week"},
                outcomes={"best_days": best_day_names},
                frequency=sum(len(daily_performance[d]) for d, _ in best_days),
                confidence=0.7,
                strength=0.6
            )
            patterns.append(pattern)
        
        return patterns
    
    async def _analyze_context_patterns(
        self, 
        experiences: List[LearningExperience]
    ) -> List[LearningPattern]:
        """Analyze context-based patterns"""
        
        patterns = []
        
        # Analyze common context keys that correlate with success
        context_success_correlation = defaultdict(lambda: {"success": 0, "total": 0})
        
        for exp in experiences:
            for key, value in exp.context.items():
                if isinstance(value, (str, int, float, bool)):
                    context_key = f"{key}:{value}"
                    context_success_correlation[context_key]["total"] += 1
                    if exp.success:
                        context_success_correlation[context_key]["success"] += 1
        
        # Find strong context correlations
        for context_key, stats in context_success_correlation.items():
            if stats["total"] >= self.min_pattern_frequency:
                success_rate = stats["success"] / stats["total"]
                
                if success_rate >= 0.8 or success_rate <= 0.2:
                    key, value = context_key.split(":", 1)
                    pattern = LearningPattern(
                        pattern_type="context_correlation",
                        agent_id=self.agent_id,
                        description=f"Context '{key}={value}' correlates with "
                                  f"{'high' if success_rate >= 0.8 else 'low'} success rate",
                        conditions={"context_key": key, "context_value": value},
                        outcomes={"expected_success_rate": success_rate},
                        frequency=stats["total"],
                        confidence=min(0.9, abs(success_rate - 0.5) * 2),
                        strength=abs(success_rate - 0.5) * 2,
                        success_rate=success_rate
                    )
                    patterns.append(pattern)
        
        return patterns
    
    async def _analyze_performance_patterns(
        self, 
        experiences: List[LearningExperience]
    ) -> List[LearningPattern]:
        """Analyze performance improvement patterns"""
        
        patterns = []
        
        # Analyze improvement patterns by experience type
        improvement_by_type = defaultdict(list)
        for exp in experiences:
            if exp.improvement:
                for metric, improvement in exp.improvement.items():
                    improvement_by_type[f"{exp.safe_enum_value(experience_type)}_{metric}"].append(improvement)
        
        for pattern_key, improvements in improvement_by_type.items():
            if len(improvements) >= self.min_pattern_frequency:
                avg_improvement = mean(improvements)
                
                if avg_improvement > 0.1:  # Significant improvement
                    exp_type, metric = pattern_key.split("_", 1)
                    pattern = LearningPattern(
                        pattern_type="performance_improvement",
                        agent_id=self.agent_id,
                        description=f"Consistent improvement in {metric} for {exp_type} experiences",
                        conditions={"experience_type": exp_type, "metric": metric},
                        outcomes={"expected_improvement": avg_improvement},
                        frequency=len(improvements),
                        confidence=min(0.9, avg_improvement * 2),
                        strength=min(1.0, avg_improvement * 3)
                    )
                    patterns.append(pattern)
        
        return patterns
    
    async def _analyze_action_outcome_patterns(
        self, 
        experiences: List[LearningExperience]
    ) -> List[LearningPattern]:
        """Analyze action-outcome patterns"""
        
        patterns = []
        
        # Group similar actions and their outcomes
        action_outcome_map = defaultdict(list)
        
        for exp in experiences:
            # Create a simplified action signature
            action_sig = self._create_action_signature(exp.action_taken)
            if action_sig:
                action_outcome_map[action_sig].append({
                    "success": exp.success,
                    "outcome": exp.outcome,
                    "confidence": exp.confidence_level
                })
        
        # Find patterns in action-outcome relationships
        for action_sig, outcomes in action_outcome_map.items():
            if len(outcomes) >= self.min_pattern_frequency:
                success_rate = sum(1 for o in outcomes if o["success"]) / len(outcomes)
                avg_confidence = mean(o["confidence"] for o in outcomes)
                
                if success_rate >= 0.8 or success_rate <= 0.2:
                    pattern = LearningPattern(
                        pattern_type="action_outcome",
                        agent_id=self.agent_id,
                        description=f"Action pattern '{action_sig}' leads to "
                                  f"{'high' if success_rate >= 0.8 else 'low'} success rate",
                        conditions={"action_signature": action_sig},
                        outcomes={
                            "expected_success_rate": success_rate,
                            "avg_confidence": avg_confidence
                        },
                        frequency=len(outcomes),
                        confidence=min(0.9, abs(success_rate - 0.5) * 2),
                        strength=abs(success_rate - 0.5) * 2,
                        success_rate=success_rate
                    )
                    patterns.append(pattern)
        
        return patterns
    
    def _create_action_signature(self, action_data: Dict[str, Any]) -> Optional[str]:
        """Create a simplified signature for actions"""
        
        if not action_data:
            return None
        
        # Extract key action characteristics
        signature_parts = []
        
        # Look for common action patterns
        if "action_type" in action_data:
            signature_parts.append(f"type:{action_data['action_type']}")
        
        if "approach" in action_data:
            if isinstance(action_data["approach"], dict):
                if "strategy" in action_data["approach"]:
                    signature_parts.append(f"strategy:{action_data['approach']['strategy']}")
            else:
                signature_parts.append(f"approach:{action_data['approach']}")
        
        if "decision_made" in action_data:
            if isinstance(action_data["decision_made"], dict):
                if "option" in action_data["decision_made"]:
                    signature_parts.append(f"option:{action_data['decision_made']['option']}")
        
        # Generic fallback - use first few keys
        if not signature_parts and len(action_data) > 0:
            for key in sorted(action_data.keys())[:3]:
                value = action_data[key]
                if isinstance(value, (str, int, float, bool)):
                    signature_parts.append(f"{key}:{value}")
        
        return "|".join(signature_parts) if signature_parts else None
    
    async def _validate_pattern(
        self, 
        pattern: LearningPattern, 
        experiences: List[LearningExperience]
    ) -> bool:
        """Validate a discovered pattern"""
        
        # Check minimum frequency
        if pattern.frequency < self.min_pattern_frequency:
            return False
        
        # Check minimum confidence
        if pattern.confidence < self.min_pattern_confidence:
            return False
        
        # Check for statistical significance
        if pattern.pattern_type in ["success_rate", "context_correlation", "action_outcome"]:
            if pattern.success_rate:
                # Simple statistical test - pattern should be significantly different from random
                expected_random = 0.5
                difference = abs(pattern.success_rate - expected_random)
                significance_threshold = 0.2  # 20% difference from random
                
                if difference < significance_threshold:
                    return False
        
        # Pattern-specific validation
        if pattern.pattern_type == "performance_improvement":
            if "expected_improvement" in pattern.outcomes:
                if pattern.outcomes["expected_improvement"] < 0.05:  # Less than 5% improvement
                    return False
        
        return True
    
    async def _store_pattern(self, pattern: LearningPattern) -> None:
        """Store a discovered pattern"""
        
        self.discovered_patterns[pattern.pattern_id] = pattern
        
        # Update statistics
        self.recognition_stats["total_patterns_discovered"] += 1
        
        pattern_type = pattern.pattern_type
        if pattern_type not in self.recognition_stats["patterns_by_type"]:
            self.recognition_stats["patterns_by_type"][pattern_type] = 0
        self.recognition_stats["patterns_by_type"][pattern_type] += 1
        
        # Update averages
        total = self.recognition_stats["total_patterns_discovered"]
        current_avg_conf = self.recognition_stats["avg_pattern_confidence"]
        current_avg_strength = self.recognition_stats["avg_pattern_strength"]
        
        self.recognition_stats["avg_pattern_confidence"] = (
            (current_avg_conf * (total - 1) + pattern.confidence) / total
        )
        
        self.recognition_stats["avg_pattern_strength"] = (
            (current_avg_strength * (total - 1) + pattern.strength) / total
        )
        
        self.logger.info(f"Stored pattern {pattern.pattern_id} of type {pattern.pattern_type}")
        
        # Create pattern discovery event
        await publish_event(
            event_type=EventType.KNOWLEDGE_CREATED,
            source_agent_id=self.agent_id,
            entity_id=pattern.pattern_id,
            entity_type="learning_pattern",
            data={
                "pattern_type": pattern.pattern_type,
                "confidence": pattern.confidence,
                "strength": pattern.strength,
                "frequency": pattern.frequency,
                "description": pattern.description
            }
        )
    
    def get_patterns_by_type(self, pattern_type: str) -> List[LearningPattern]:
        """Get patterns filtered by type"""
        return [
            pattern for pattern in self.discovered_patterns.values()
            if pattern.pattern_type == pattern_type
        ]
    
    def get_patterns_by_confidence(self, min_confidence: float) -> List[LearningPattern]:
        """Get patterns with confidence above threshold"""
        return [
            pattern for pattern in self.discovered_patterns.values()
            if pattern.confidence >= min_confidence
        ]
    
    def get_applicable_patterns(self, context: Dict[str, Any]) -> List[LearningPattern]:
        """Get patterns applicable to given context"""
        applicable = []
        
        for pattern in self.discovered_patterns.values():
            if self._is_pattern_applicable(pattern, context):
                applicable.append(pattern)
        
        return sorted(applicable, key=lambda p: p.confidence, reverse=True)
    
    def _is_pattern_applicable(self, pattern: LearningPattern, context: Dict[str, Any]) -> bool:
        """Check if pattern is applicable to given context"""
        
        # Check context constraints
        if pattern.context_constraints:
            for key, expected_value in pattern.context_constraints.items():
                if key not in context or context[key] != expected_value:
                    return False
        
        # Check pattern conditions
        if pattern.conditions:
            for key, expected_value in pattern.conditions.items():
                if key == "experience_type":
                    # This would be checked when creating experiences
                    continue
                elif key == "context_key":
                    # Check if context has this key
                    context_key = pattern.conditions.get("context_key")
                    context_value = pattern.conditions.get("context_value")
                    if context_key and context_value:
                        if context.get(context_key) != context_value:
                            return False
                elif key in context:
                    if context[key] != expected_value:
                        return False
        
        return True
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get pattern recognition statistics"""
        return self.recognition_stats.copy()
    
    def clear_patterns(self) -> None:
        """Clear all discovered patterns (use with caution)"""
        self.discovered_patterns.clear()
        self.recognition_stats = {
            "total_patterns_discovered": 0,
            "patterns_by_type": {},
            "avg_pattern_confidence": 0.0,
            "avg_pattern_strength": 0.0
        }
        self.logger.info("Cleared all discovered patterns")

    @property
    def patterns(self) -> Dict[str, LearningPattern]:
        """Alias for discovered_patterns for backward compatibility"""
        return self.discovered_patterns
    
    async def discover_patterns(
        self, 
        experiences: List[LearningExperience],
        focus_types: List[ExperienceType] = None
    ) -> List[LearningPattern]:
        """Alias for analyze_experiences method for backward compatibility"""
        return await self.analyze_experiences(experiences, focus_types) 