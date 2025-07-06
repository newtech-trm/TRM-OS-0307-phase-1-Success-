"""
TRM-OS Agent Evolution System

Advanced agent evolution và capability enhancement system cho TRM-OS Genesis Engine.
Evolution system cho phép:
- Analyze agent performance gaps
- Evolve agent capabilities dynamically
- Validate capability improvements
- Track evolution history và metrics
"""

from .capability_evolver import (
    AgentCapabilityEvolver,
    PerformanceGap,
    EvolutionResult,
    CapabilityEvolutionStrategy
)

__all__ = [
    "AgentCapabilityEvolver",
    "PerformanceGap",
    "EvolutionResult", 
    "CapabilityEvolutionStrategy"
] 