"""
Advanced Reasoning Engine for TRM-OS AI Agents

This module provides sophisticated reasoning capabilities for AI agents including:
- Multi-step logical reasoning
- Causal analysis and dependency tracking  
- Uncertainty handling with probabilistic reasoning
- Context-aware decision making
- Cross-agent knowledge synthesis

Core Principles:
1. Recognition → Event → WIN philosophy integration
2. Ontology-first reasoning based on graph relationships
3. Event-driven architecture compatibility
4. Transparent reasoning audit trails
"""

from .advanced_reasoning_engine import AdvancedReasoningEngine
from .causal_analyzer import CausalAnalyzer  
from .uncertainty_handler import UncertaintyHandler
from .context_manager import ContextManager
from .reasoning_coordinator import ReasoningCoordinator, ReasoningRequest, ReasoningResult as CoordinatorResult
from .tension_analyzer import TensionAnalyzer
from .rule_engine import RuleEngine
from .solution_generator import SolutionGenerator
from .priority_calculator import PriorityCalculator
from .reasoning_types import (
    ReasoningContext,
    ReasoningStep, 
    CausalChain,
    UncertaintyLevel,
    ReasoningResult
)

__all__ = [
    "AdvancedReasoningEngine",
    "CausalAnalyzer", 
    "UncertaintyHandler",
    "ContextManager",
    "ReasoningCoordinator",
    "ReasoningRequest", 
    "CoordinatorResult",
    "TensionAnalyzer",
    "RuleEngine",
    "SolutionGenerator",
    "PriorityCalculator",
    "ReasoningContext",
    "ReasoningStep",
    "CausalChain", 
    "UncertaintyLevel",
    "ReasoningResult"
] 