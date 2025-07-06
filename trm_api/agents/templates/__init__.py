"""
TRM-OS Agent Templates Module

Cung cấp các template cơ bản cho Genesis Engine để tạo ra các AI agents chuyên biệt.
Mỗi template định nghĩa cấu trúc, capabilities và logic xử lý cho một loại agent cụ thể.

Templates bao gồm:
- DataAnalystAgent: Xử lý tensions liên quan đến data analysis
- CodeGeneratorAgent: Xử lý tensions liên quan đến coding/development  
- UserInterfaceAgent: Xử lý tensions liên quan đến UX/UI
- IntegrationAgent: Xử lý tensions liên quan đến system integration
- ResearchAgent: Xử lý tensions liên quan đến knowledge gathering
"""

from .base_template import BaseAgentTemplate
from .data_analyst_template import DataAnalystAgent
from .code_generator_template import CodeGeneratorAgent
from .user_interface_template import UserInterfaceAgent
from .integration_template import IntegrationAgent
from .research_template import ResearchAgent
from .template_registry import AgentTemplateRegistry

__all__ = [
    "BaseAgentTemplate",
    "DataAnalystAgent", 
    "CodeGeneratorAgent",
    "UserInterfaceAgent",
    "IntegrationAgent", 
    "ResearchAgent",
    "AgentTemplateRegistry"
] 