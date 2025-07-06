"""
TRM API v2 Endpoints
===================

Conversational intelligence endpoints for natural language interaction.
"""

from .conversation import router as conversation_router

__all__ = ["conversation_router"] 