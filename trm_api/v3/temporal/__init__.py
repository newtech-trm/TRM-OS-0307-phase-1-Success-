"""
TRM-OS v3.0 - Temporal Reasoning Module
Phase 3C: Temporal Reasoning Engine Implementation

Core Temporal Intelligence Components:
- TemporalReasoningEngine: Historical pattern analysis và predictive modeling
- StrategicPlanningAutomator: Multi-horizon planning với resource optimization
- TemporalCommercialAICoordinator: Time-aware AI coordination
- PredictiveAnalyticsEngine: Advanced forecasting capabilities
"""

from .temporal_reasoning_engine import TemporalReasoningEngine
from .strategic_planning_automator import StrategicPlanningAutomator
from .temporal_commercial_ai_coordinator import TemporalCommercialAICoordinator
from .predictive_analytics_engine import PredictiveAnalyticsEngine

__all__ = [
    "TemporalReasoningEngine",
    "StrategicPlanningAutomator", 
    "TemporalCommercialAICoordinator",
    "PredictiveAnalyticsEngine"
]

__version__ = "3.0.0"
__description__ = "Temporal Reasoning - Predictive Intelligence Implementation" 