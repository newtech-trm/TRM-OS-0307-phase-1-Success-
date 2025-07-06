"""
Conversational Intelligence Package
===================================

Natural language processing and conversation management for TRM-OS v2.
"""

from .nlp_processor import ConversationProcessor
from .session_manager import ConversationSessionManager
from .response_generator import NaturalResponseGenerator

__all__ = [
    "ConversationProcessor",
    "ConversationSessionManager", 
    "NaturalResponseGenerator"
] 