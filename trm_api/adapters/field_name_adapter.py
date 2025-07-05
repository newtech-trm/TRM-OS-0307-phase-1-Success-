"""
Field Name Adapter cho TRM-OS
=============================

Adapter chuyên biệt để chuẩn hóa field names giữa:
- camelCase (API JSON payload theo Ontology V3.2)
- snake_case (Python model convention)
- Neo4j property names

Đảm bảo consistency trong toàn bộ hệ thống.
"""

import re
from typing import Dict, Any, List, Optional, Union
import logging

logger = logging.getLogger(__name__)


class FieldNameAdapter:
    """Adapter để chuẩn hóa field names giữa các convention khác nhau"""
    
    # Mapping chuẩn từ camelCase (API) sang snake_case (Python)
    CAMEL_TO_SNAKE_MAPPING = {
        # Core entity fields
        "agentId": "agent_id",
        "projectId": "project_id", 
        "taskId": "task_id",
        "winId": "win_id",
        "recognitionId": "recognition_id",
        "eventId": "event_id",
        "knowledgeSnippetId": "knowledge_snippet_id",
        "tensionId": "tension_id",
        "userId": "user_id",
        "skillId": "skill_id",
        "resourceId": "resource_id",
        
        # Timestamp fields
        "createdAt": "created_at",
        "updatedAt": "updated_at",
        "startedAt": "started_at",
        "completedAt": "completed_at",
        "dueAt": "due_at",
        "publishedAt": "published_at",
        "archivedAt": "archived_at",
        
        # Relationship fields
        "assignedTo": "assigned_to",
        "managedBy": "managed_by",
        "createdBy": "created_by",
        "updatedBy": "updated_by",
        "reviewedBy": "reviewed_by",
        "approvedBy": "approved_by",
        "parentProject": "parent_project",
        "parentTask": "parent_task",
        
        # Type and status fields
        "agentType": "agent_type",
        "projectType": "project_type",
        "taskType": "task_type",
        "winType": "win_type",
        "recognitionType": "recognition_type",
        "eventType": "event_type",
        "knowledgeType": "knowledge_type",
        "tensionType": "tension_type",
        "taskStatus": "task_status",
        "projectStatus": "project_status",
        "winStatus": "win_status",
        "recognitionStatus": "recognition_status",
        
        # Extended fields
        "isActive": "is_active",
        "isCompleted": "is_completed",
        "isArchived": "is_archived",
        "isStrategic": "is_strategic",
        "isFounder": "is_founder",
        "isPublic": "is_public",
        "isRequired": "is_required",
        "hasAttachments": "has_attachments",
        "canEdit": "can_edit",
        "canDelete": "can_delete",
        
        # Metrics and counts
        "totalCount": "total_count",
        "activeCount": "active_count",
        "completedCount": "completed_count",
        "pageCount": "page_count",
        "itemCount": "item_count",
        "maxCount": "max_count",
        "minCount": "min_count",
        
        # Date fields
        "startDate": "start_date",
        "endDate": "end_date",
        "dueDate": "due_date",
        "targetDate": "target_date",
        "actualDate": "actual_date",
        "publishDate": "publish_date",
        "archiveDate": "archive_date",
        
        # Nested object fields
        "relationshipProperties": "relationship_properties",
        "entityProperties": "entity_properties",
        "metaData": "meta_data",
        "configData": "config_data",
        "responseData": "response_data",
        "requestData": "request_data",
        
        # API specific fields
        "apiKey": "api_key",
        "apiVersion": "api_version",
        "apiEndpoint": "api_endpoint",
        "responseCode": "response_code",
        "requestId": "request_id",
        "sessionId": "session_id",
        "correlationId": "correlation_id"
    }
    
    # Reverse mapping từ snake_case sang camelCase
    SNAKE_TO_CAMEL_MAPPING = {v: k for k, v in CAMEL_TO_SNAKE_MAPPING.items()}
    
    @classmethod
    def camel_to_snake(cls, camel_str: str) -> str:
        """Chuyển đổi camelCase sang snake_case
        
        Args:
            camel_str: String trong camelCase
            
        Returns:
            String trong snake_case
        """
        if not camel_str:
            return camel_str
            
        # Kiểm tra mapping có sẵn trước
        if camel_str in cls.CAMEL_TO_SNAKE_MAPPING:
            return cls.CAMEL_TO_SNAKE_MAPPING[camel_str]
        
        # Chuyển đổi tự động bằng regex
        # Thêm underscore trước các chữ cái viết hoa
        snake_str = re.sub('([a-z0-9])([A-Z])', r'\1_\2', camel_str)
        return snake_str.lower()
    
    @classmethod
    def snake_to_camel(cls, snake_str: str) -> str:
        """Chuyển đổi snake_case sang camelCase
        
        Args:
            snake_str: String trong snake_case
            
        Returns:
            String trong camelCase
        """
        if not snake_str:
            return snake_str
            
        # Kiểm tra mapping có sẵn trước
        if snake_str in cls.SNAKE_TO_CAMEL_MAPPING:
            return cls.SNAKE_TO_CAMEL_MAPPING[snake_str]
        
        # Chuyển đổi tự động
        components = snake_str.split('_')
        # Giữ nguyên component đầu tiên, viết hoa chữ cái đầu của các component còn lại
        return components[0] + ''.join(word.capitalize() for word in components[1:])
    
    @classmethod
    def normalize_dict_to_snake(cls, data: Union[Dict[str, Any], List, Any]) -> Union[Dict[str, Any], List, Any]:
        """Chuẩn hóa tất cả keys trong dict từ camelCase sang snake_case
        
        Args:
            data: Dict hoặc List cần chuẩn hóa
            
        Returns:
            Dict hoặc List với keys đã được chuẩn hóa
        """
        if isinstance(data, dict):
            result = {}
            for key, value in data.items():
                # Chuyển đổi key
                new_key = cls.camel_to_snake(key)
                # Đệ quy xử lý value
                new_value = cls.normalize_dict_to_snake(value)
                result[new_key] = new_value
            return result
        elif isinstance(data, list):
            return [cls.normalize_dict_to_snake(item) for item in data]
        else:
            return data
    
    @classmethod
    def normalize_dict_to_camel(cls, data: Union[Dict[str, Any], List, Any]) -> Union[Dict[str, Any], List, Any]:
        """Chuẩn hóa tất cả keys trong dict từ snake_case sang camelCase
        
        Args:
            data: Dict hoặc List cần chuẩn hóa
            
        Returns:
            Dict hoặc List với keys đã được chuẩn hóa
        """
        if isinstance(data, dict):
            result = {}
            for key, value in data.items():
                # Chuyển đổi key
                new_key = cls.snake_to_camel(key)
                # Đệ quy xử lý value
                new_value = cls.normalize_dict_to_camel(value)
                result[new_key] = new_value
            return result
        elif isinstance(data, list):
            return [cls.normalize_dict_to_camel(item) for item in data]
        else:
            return data
    
    @classmethod
    def normalize_api_response(cls, data: Union[Dict[str, Any], List[Dict[str, Any]]]) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """Chuẩn hóa API response để trả về camelCase theo Ontology V3.2
        
        Args:
            data: Response data cần chuẩn hóa
            
        Returns:
            Response data với camelCase fields
        """
        try:
            result = cls.normalize_dict_to_camel(data)
            logger.debug(f"Normalized API response: {len(str(result))} characters")
            return result
        except Exception as e:
            logger.error(f"Error normalizing API response: {e}")
            return data
    
    @classmethod
    def normalize_api_request(cls, data: Union[Dict[str, Any], List[Dict[str, Any]]]) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """Chuẩn hóa API request từ camelCase sang snake_case cho Python processing
        
        Args:
            data: Request data cần chuẩn hóa
            
        Returns:
            Request data với snake_case fields
        """
        try:
            result = cls.normalize_dict_to_snake(data)
            logger.debug(f"Normalized API request: {len(str(result))} characters")
            return result
        except Exception as e:
            logger.error(f"Error normalizing API request: {e}")
            return data
    
    @classmethod
    def normalize_neo4j_properties(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """Chuẩn hóa properties cho Neo4j storage
        
        Neo4j properties thường sử dụng camelCase theo Ontology V3.2
        
        Args:
            data: Properties cần chuẩn hóa
            
        Returns:
            Properties đã chuẩn hóa cho Neo4j
        """
        if not isinstance(data, dict):
            return data
            
        result = {}
        for key, value in data.items():
            # Chuyển snake_case sang camelCase cho Neo4j
            if '_' in key:
                new_key = cls.snake_to_camel(key)
            else:
                new_key = key
            result[new_key] = value
        
        return result
    
    @classmethod
    def get_field_mapping_report(cls) -> Dict[str, Any]:
        """Trả về báo cáo về field mapping hiện tại
        
        Returns:
            Dict chứa thông tin về mappings
        """
        return {
            "total_mappings": len(cls.CAMEL_TO_SNAKE_MAPPING),
            "camel_to_snake_count": len(cls.CAMEL_TO_SNAKE_MAPPING),
            "snake_to_camel_count": len(cls.SNAKE_TO_CAMEL_MAPPING),
            "sample_mappings": dict(list(cls.CAMEL_TO_SNAKE_MAPPING.items())[:10]),
            "categories": {
                "id_fields": len([k for k in cls.CAMEL_TO_SNAKE_MAPPING.keys() if k.endswith('Id')]),
                "timestamp_fields": len([k for k in cls.CAMEL_TO_SNAKE_MAPPING.keys() if k.endswith('At')]),
                "type_fields": len([k for k in cls.CAMEL_TO_SNAKE_MAPPING.keys() if k.endswith('Type')]),
                "status_fields": len([k for k in cls.CAMEL_TO_SNAKE_MAPPING.keys() if k.endswith('Status')]),
                "boolean_fields": len([k for k in cls.CAMEL_TO_SNAKE_MAPPING.keys() if k.startswith('is') or k.startswith('has') or k.startswith('can')]),
                "date_fields": len([k for k in cls.CAMEL_TO_SNAKE_MAPPING.keys() if k.endswith('Date')])
            }
        }


# Utility functions cho convenience
def to_snake_case(camel_str: str) -> str:
    """Convenience function để chuyển camelCase sang snake_case"""
    return FieldNameAdapter.camel_to_snake(camel_str)


def to_camel_case(snake_str: str) -> str:
    """Convenience function để chuyển snake_case sang camelCase"""
    return FieldNameAdapter.snake_to_camel(snake_str)


def normalize_for_api(data: Union[Dict[str, Any], List]) -> Union[Dict[str, Any], List]:
    """Convenience function để chuẩn hóa data cho API response (camelCase)"""
    return FieldNameAdapter.normalize_api_response(data)


def normalize_from_api(data: Union[Dict[str, Any], List]) -> Union[Dict[str, Any], List]:
    """Convenience function để chuẩn hóa data từ API request (snake_case)"""
    return FieldNameAdapter.normalize_api_request(data) 