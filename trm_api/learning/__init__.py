"""
TRM-OS v2 Adaptive Learning System

Enables agents to learn from experience and adapt their behavior over time.
Follows TRM-OS philosophy: Recognition → Event → WIN through continuous learning.
"""

from .learning_types import (
    LearningExperience,
    PerformanceMetric,
    AdaptationRule,
    LearningGoal,
    LearningPattern,
    ExperienceType,
    MetricType,
    AdaptationType
)

from .experience_collector import ExperienceCollector
from .pattern_recognizer import PatternRecognizer  
from .adaptation_engine import AdaptationEngine
from .performance_tracker import PerformanceTracker
from .adaptive_learning_system import AdaptiveLearningSystem

__all__ = [
    # Types
    "LearningExperience",
    "PerformanceMetric", 
    "AdaptationRule",
    "LearningGoal",
    "LearningPattern",
    "ExperienceType",
    "MetricType",
    "AdaptationType",
    
    # Components
    "ExperienceCollector",
    "PatternRecognizer",
    "AdaptationEngine", 
    "PerformanceTracker",
    "AdaptiveLearningSystem"
] 