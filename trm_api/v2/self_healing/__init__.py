"""
TRM-OS v2.3 - Self-Healing Commercial AI Systems
Phase 3A: Autonomous Recovery and Intelligent Troubleshooting

This module implements self-healing capabilities for Commercial AI coordination,
following AGE_COMPREHENSIVE_SYSTEM_DESIGN_V2.md specifications.

Core Components:
- AutonomousRecoverySystem: System-level anomaly detection and recovery
- CommercialAIHealthMonitor: AI service health monitoring and failover
- IntelligentTroubleshooter: Pattern-based problem diagnosis
- PerformanceOptimizer: Learning-based system optimization
"""

from .autonomous_recovery_system import AutonomousRecoverySystem
from .commercial_ai_monitor import CommercialAIHealthMonitor
from .intelligent_troubleshooter import IntelligentTroubleshooter
from .performance_optimizer import PerformanceOptimizer

__all__ = [
    "AutonomousRecoverySystem",
    "CommercialAIHealthMonitor", 
    "IntelligentTroubleshooter",
    "PerformanceOptimizer"
]

__version__ = "2.3.0"
__author__ = "TRM-OS Development Team"
__description__ = "Self-Healing Commercial AI Systems - Phase 3A Implementation" 