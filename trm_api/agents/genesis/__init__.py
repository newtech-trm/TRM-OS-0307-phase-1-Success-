"""
TRM-OS Genesis Engine

Advanced agent creation và composition system cho TRM-OS.
Genesis Engine cho phép tạo ra sophisticated agents thông qua:
- Template composition
- Custom agent creation từ requirements
- Pattern analysis và template generation
- Agent capability evolution
- Ecosystem optimization
"""

from .advanced_creator import (
    AdvancedAgentCreator,
    CompositeAgent,
    CustomAgent,
    CustomRequirements
)

from .template_generator import (
    TemplateGenerator,
    AgentPattern,
    GeneratedTemplate,
    ValidationResult
)

__all__ = [
    "AdvancedAgentCreator",
    "CompositeAgent", 
    "CustomAgent",
    "CustomRequirements",
    "TemplateGenerator",
    "AgentPattern",
    "GeneratedTemplate", 
    "ValidationResult"
] 