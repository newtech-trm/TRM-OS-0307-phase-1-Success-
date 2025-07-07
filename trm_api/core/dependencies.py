"""
TRM-OS Core Dependencies
Dependency injection cho các core services
"""

from typing import Optional
from functools import lru_cache

from ..learning.adaptive_learning_system import AdaptiveLearningSystem


# Global instances
_learning_system: Optional[AdaptiveLearningSystem] = None


@lru_cache()
async def get_learning_system() -> AdaptiveLearningSystem:
    """Get or create adaptive learning system instance"""
    global _learning_system
    if _learning_system is None:
        _learning_system = AdaptiveLearningSystem()
        await _learning_system.initialize()
    return _learning_system


async def cleanup_dependencies():
    """Cleanup all dependencies"""
    global _learning_system
    
    if _learning_system:
        await _learning_system.cleanup()
        _learning_system = None 