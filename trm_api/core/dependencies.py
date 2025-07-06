"""
TRM-OS Core Dependencies
Dependency injection cho các core services
"""

from typing import Optional
from functools import lru_cache

from ..learning.adaptive_learning_system import AdaptiveLearningSystem
from ..api.v2.adaptive_conversation_manager import AdaptiveConversationManager


# Global instances
_learning_system: Optional[AdaptiveLearningSystem] = None
_conversation_manager: Optional[AdaptiveConversationManager] = None


@lru_cache()
async def get_learning_system() -> AdaptiveLearningSystem:
    """Get or create adaptive learning system instance"""
    global _learning_system
    if _learning_system is None:
        _learning_system = AdaptiveLearningSystem()
        await _learning_system.initialize()
    return _learning_system


async def get_conversation_manager() -> AdaptiveConversationManager:
    """Get or create conversation manager instance"""
    global _conversation_manager
    if _conversation_manager is None:
        learning_system = await get_learning_system()
        _conversation_manager = AdaptiveConversationManager(learning_system)
    return _conversation_manager


async def cleanup_dependencies():
    """Cleanup all dependencies"""
    global _learning_system, _conversation_manager
    
    if _conversation_manager:
        await _conversation_manager.cleanup()
        _conversation_manager = None
    
    if _learning_system:
        await _learning_system.cleanup()
        _learning_system = None 