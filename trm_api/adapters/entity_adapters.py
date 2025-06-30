from typing import Any, Dict, List, Optional
import logging

from .data_adapters import BaseEntityAdapter, EnumAdapter

# Import các enum cần thiết
from trm_api.models.enums import WinStatus, WinType, RecognitionStatus, RecognitionType
from trm_api.models.enums import TaskStatus, TaskType, KnowledgeSnippetType


class WinAdapter(BaseEntityAdapter):
    """Adapter chuyên biệt cho entity WIN"""
    
    def _apply_enum_adapters(self, entity: Dict[str, Any]) -> Dict[str, Any]:
        """Áp dụng các enum adapter cho entity WIN.
        
        Args:
            entity: WIN entity cần chuẩn hóa
            
        Returns:
            WIN entity đã được chuẩn hóa enum
        """
        result = entity.copy()
        
        # Chuẩn hóa trường status
        if 'status' in result:
            result = EnumAdapter.normalize_field(result, 'status', WinStatus)
        
        # Chuẩn hóa trường winType
        if 'winType' in result:
            result = EnumAdapter.normalize_field(result, 'winType', WinType)
            
        return result


class RecognitionAdapter(BaseEntityAdapter):
    """Adapter chuyên biệt cho entity Recognition"""
    
    def _apply_enum_adapters(self, entity: Dict[str, Any]) -> Dict[str, Any]:
        """Áp dụng các enum adapter cho entity Recognition.
        
        Args:
            entity: Recognition entity cần chuẩn hóa
            
        Returns:
            Recognition entity đã được chuẩn hóa enum
        """
        result = entity.copy()
        
        # Chuẩn hóa trường status
        if 'status' in result:
            result = EnumAdapter.normalize_field(result, 'status', RecognitionStatus)
        
        # Chuẩn hóa trường recognitionType
        if 'recognitionType' in result:
            result = EnumAdapter.normalize_field(result, 'recognitionType', RecognitionType)
            
        return result


class TaskAdapter(BaseEntityAdapter):
    """Adapter chuyên biệt cho entity Task"""
    
    def _apply_enum_adapters(self, entity: Dict[str, Any]) -> Dict[str, Any]:
        """Áp dụng các enum adapter cho entity Task.
        
        Args:
            entity: Task entity cần chuẩn hóa
            
        Returns:
            Task entity đã được chuẩn hóa enum
        """
        result = entity.copy()
        
        # Chuẩn hóa trường status
        if 'status' in result:
            result = EnumAdapter.normalize_field(result, 'status', TaskStatus)
        
        # Chuẩn hóa trường task_type
        if 'task_type' in result:
            result = EnumAdapter.normalize_field(result, 'task_type', TaskType)
            
        return result


class KnowledgeSnippetAdapter(BaseEntityAdapter):
    """Adapter chuyên biệt cho entity KnowledgeSnippet"""
    
    def _apply_enum_adapters(self, entity: Dict[str, Any]) -> Dict[str, Any]:
        """Áp dụng các enum adapter cho entity KnowledgeSnippet.
        
        Args:
            entity: KnowledgeSnippet entity cần chuẩn hóa
            
        Returns:
            KnowledgeSnippet entity đã được chuẩn hóa enum
        """
        result = entity.copy()
        
        # Chuẩn hóa trường snippet_type
        if 'snippet_type' in result:
            result = EnumAdapter.normalize_field(result, 'snippet_type', KnowledgeSnippetType)
            
        return result


class ProjectAdapter(BaseEntityAdapter):
    """Adapter chuyên biệt cho entity Project"""
    
    def _apply_enum_adapters(self, entity: Dict[str, Any]) -> Dict[str, Any]:
        """Áp dụng các enum adapter cho entity Project.
        Hiện tại Project không có trường enum cụ thể cần chuẩn hóa.
        
        Args:
            entity: Project entity cần chuẩn hóa
            
        Returns:
            Project entity đã được chuẩn hóa enum
        """
        # Hiện tại Project không có trường enum đặc biệt
        return entity


class EventAdapter(BaseEntityAdapter):
    """Adapter chuyên biệt cho entity Event"""
    
    def _apply_enum_adapters(self, entity: Dict[str, Any]) -> Dict[str, Any]:
        """Áp dụng các enum adapter cho entity Event.
        
        Args:
            entity: Event entity cần chuẩn hóa
            
        Returns:
            Event entity đã được chuẩn hóa enum
        """
        result = entity.copy()
        
        # Chuẩn hóa trường event_type nếu có
        if 'event_type' in result:
            # Cần import enum EventType nếu có
            # result = EnumAdapter.normalize_field(result, 'event_type', EventType)
            pass
            
        return result


# Factory cho các entity adapter
def get_entity_adapter(entity_type: str, adapt_datetime: bool = True, adapt_enums: bool = True) -> BaseEntityAdapter:
    """Factory method để lấy adapter phù hợp với entity type.
    
    Args:
        entity_type: Loại entity cần adapter
        adapt_datetime: Có chuẩn hóa datetime không
        adapt_enums: Có chuẩn hóa enum không
        
    Returns:
        Adapter phù hợp cho entity type
    """
    entity_type = entity_type.lower()
    
    if entity_type == 'win':
        return WinAdapter(adapt_datetime, adapt_enums)
    elif entity_type == 'recognition':
        return RecognitionAdapter(adapt_datetime, adapt_enums)
    elif entity_type == 'task':
        return TaskAdapter(adapt_datetime, adapt_enums)
    elif entity_type == 'knowledge_snippet':
        return KnowledgeSnippetAdapter(adapt_datetime, adapt_enums)
    elif entity_type == 'project':
        return ProjectAdapter(adapt_datetime, adapt_enums)
    elif entity_type == 'event':
        return EventAdapter(adapt_datetime, adapt_enums)
    else:
        # Trả về adapter cơ bản nếu không tìm thấy adapter chuyên biệt
        logging.warning(f"No specialized adapter found for entity type: {entity_type}. Using base adapter.")
        return BaseEntityAdapter(adapt_datetime, adapt_enums)
