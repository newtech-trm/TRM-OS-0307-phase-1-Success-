"""
TRM-OS v3.0 - Strategic Intelligence Module
Phase 3B: Strategic Feedback Loop Automation

Core Strategic Intelligence Components:
- WINPatternAnalyzer: Success pattern recognition và analysis
- FailureLessonExtractor: Automated failure analysis và learning
- StrategyOptimizer: Decision-making process optimization
- FeedbackAutomation: Real-time feedback loop management
- CommercialAIStrategicCoordinator: Multi-AI strategic insights
"""

from .win_pattern_analyzer import WINPatternAnalyzer
from .failure_lesson_extractor import FailureLessonExtractor
from .strategy_optimizer import StrategyOptimizer
from .feedback_automation import FeedbackAutomation
from .commercial_ai_strategic_coordinator import CommercialAIStrategicCoordinator

__all__ = [
    "WINPatternAnalyzer",
    "FailureLessonExtractor",
    "StrategyOptimizer", 
    "FeedbackAutomation",
    "CommercialAIStrategicCoordinator"
]

__version__ = "3.0.0"
__description__ = "Strategic Intelligence - Automated Feedback Loop Implementation" 