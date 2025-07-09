"""
TRM-OS Core Dependencies
Dependency injection cho các core services
"""

from typing import Optional
from functools import lru_cache
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from ..learning.adaptive_learning_system import AdaptiveLearningSystem


# Global instances
_learning_system: Optional[AdaptiveLearningSystem] = None

# Security
security = HTTPBearer()


@lru_cache()
async def get_learning_system() -> AdaptiveLearningSystem:
    """Get or create adaptive learning system instance"""
    global _learning_system
    if _learning_system is None:
        _learning_system = AdaptiveLearningSystem()
        await _learning_system.initialize()
    return _learning_system


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """Get current authenticated user"""
    # For now, return a mock user
    # In production, this would validate JWT token and return user info
    return {
        "id": "user123",
        "username": "admin",
        "email": "admin@trm-os.com",
        "roles": ["admin"],
        "permissions": ["read", "write", "admin"]
    }


async def get_current_active_user(current_user: dict = Depends(get_current_user)) -> dict:
    """Get current active user"""
    if not current_user.get("active", True):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user


async def cleanup_dependencies():
    """Cleanup all dependencies"""
    global _learning_system
    
    if _learning_system:
        await _learning_system.cleanup()
        _learning_system = None 