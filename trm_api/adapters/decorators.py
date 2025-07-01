import functools
import logging
import json
from typing import Any, Optional, TypeVar, Union, List, Dict, Callable
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from datetime import datetime

from fastapi import Response

# Import các adapter mới
from .data_adapters import DatetimeAdapter, EnumAdapter, BaseEntityAdapter
from .entity_adapters import get_entity_adapter
from .datetime_adapter import normalize_dict_datetimes  # Giữ lại để tương thích ngược


def _process_items(items: Any, adapt_datetime: bool, adapt_enums: Optional[List[Dict[str, Any]]]) -> Any:
    """
    Xử lý và chuẩn hóa các item trong response theo nguyên tắc ontology-first nghiêm ngặt.
    Chuyển đổi tất cả datetime sang chuỗi ISO 8601 và chuẩn hóa enum values.
    
    Args:
        items: Item hoặc danh sách item cần xử lý
        adapt_datetime: Nếu True thì chuẩn hóa các trường datetime
        adapt_enums: Danh sách các adapter để chuẩn hóa enum fields
        
    Returns:
        Dữ liệu đã được chuẩn hóa hoàn toàn theo ontology
    """
    try:
        # Xử lý giá trị None
        if items is None:
            return None
        
        # Xử lý datetime object trực tiếp
        if adapt_datetime and isinstance(items, datetime):
            # Đảm bảo chuyển thành chuỗi ISO 8601
            try:
                return items.isoformat()
            except Exception as e:
                logging.error(f"Error converting datetime to ISO 8601: {e}")
                return str(items)  # Fallback cơ bản nếu có lỗi
        
        # Xử lý danh sách các item
        if isinstance(items, list):
            return [_process_items(item, adapt_datetime, adapt_enums) for item in items]
        
        # Xử lý dictionary
        if isinstance(items, dict):
            result = {}
            # Lưu key của các trường datetime đã biết
            datetime_keys = ['created_at', 'createdat', 'updated_at', 'updatedat', 
                          'start_date', 'startdate', 'end_date', 'enddate', 
                          'due_date', 'duedate', 'target_end_date', 
                          'createdAt', 'updatedAt', 'startDate', 'endDate', 
                          'dueDate', 'targetEndDate']
            
            # Xử lý tất cả các trường trong dictionary
            for key, value in items.items():
                # Xử lý trường hợp datetime đặc biệt
                if adapt_datetime and key in datetime_keys:
                    from .datetime_adapter import normalize_datetime
                    iso_value = normalize_datetime(value)
                    result[key] = iso_value if iso_value is not None else value
                # Xử lý datetime objects trực tiếp
                elif adapt_datetime and isinstance(value, datetime):
                    result[key] = value.isoformat()
                # Xử lý nested dictionaries
                elif isinstance(value, dict):
                    result[key] = _process_items(value, adapt_datetime, adapt_enums)
                # Xử lý nested lists
                elif isinstance(value, list):
                    result[key] = _process_items(value, adapt_datetime, adapt_enums)
                # Sử dụng giá trị nguyên thủy cho các trường hợp khác
                else:
                    result[key] = value
            
            # Xử lý enum fields nếu được yêu cầu
            if adapt_enums:
                for enum_config in adapt_enums:
                    field = enum_config.get("field")
                    adapter = enum_config.get("adapter")
                    if field and field in result and adapter and result[field] is not None:
                        try:
                            normalized_value = adapter(result[field])
                            if normalized_value is not None:
                                result[field] = normalized_value
                        except Exception as e:
                            logging.error(f"Error normalizing enum field '{field}': {e}")
                            # Giữ giá trị gốc nếu có lỗi
            
            return result
        
        # Trả về nguyên giá trị cho các trường hợp khác
        return items
    except Exception as e:
        logging.error(f"Unexpected error in _process_items: {e}")
        return items  # Trả về giá trị gốc nếu có lỗi


def adapt_response(
    response_item_key: Optional[str] = None,
    adapt_datetime: bool = True,
    adapt_enums: Optional[List[Dict[str, Any]]] = None
):
    """
    Decorator chính để chuẩn hóa API response theo triết lý ontology-first nghiêm ngặt.
    Chuyển đổi tất cả datetime sang chuỗi ISO 8601 và chuẩn hóa enum values.
    
    Args:
        response_item_key: Key chứa danh sách các item nếu response là collection
        adapt_datetime: Nếu True thì chuẩn hóa các trường datetime sang ISO format
        adapt_enums: Danh sách các adapter để chuẩn hóa enum fields
            [{'field': 'field_name', 'adapter': normalize_function}]
            
    Returns:
        Decorator function đã được wrap
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                # Gọi endpoint function gốc
                response = await func(*args, **kwargs)
                
                # Xử lý giá trị None
                if response is None:
                    return None
                
                # Trường hợp response là Response object (FastAPI response)
                if isinstance(response, Response):
                    try:
                        # Chỉ xử lý nếu là JSONResponse
                        if isinstance(response, JSONResponse):
                            # Extract dữ liệu từ response
                            body_content = response.body
                            if isinstance(body_content, bytes):
                                body_content = body_content.decode('utf-8')
                            
                            data = json.loads(body_content)
                            
                            # Xử lý data theo các tham số
                            if response_item_key and isinstance(data, dict) and response_item_key in data:
                                # Chỉ xử lý các mục cụ thể (như 'items')
                                data[response_item_key] = _process_items(
                                    data[response_item_key], adapt_datetime, adapt_enums
                                )
                            else:
                                # Xử lý toàn bộ data
                                data = _process_items(data, adapt_datetime, adapt_enums)
                            
                            # Tạo JSONResponse mới với data đã xử lý
                            return JSONResponse(
                                content=data,
                                status_code=response.status_code,
                                headers=dict(response.headers),
                                media_type=response.media_type,
                            )
                        
                        # Các loại Response khác giữ nguyên
                        return response
                    except Exception as e:
                        logging.error(f"Error processing Response object: {str(e)}")
                        return response
                
                # Trường hợp response là dict hoặc Pydantic model
                if isinstance(response, dict):
                    # Xử lý collection item nếu được chỉ định
                    if response_item_key and response_item_key in response:
                        # Tạo bản sao của response để tránh thay đổi trực tiếp
                        result = dict(response)
                        # Chỉ xử lý collection item được chỉ định
                        result[response_item_key] = _process_items(
                            result[response_item_key], adapt_datetime, adapt_enums
                        )
                        return result
                    
                    # Xử lý toàn bộ dictionary nếu không có response_item_key
                    return _process_items(response, adapt_datetime, adapt_enums)
                
                # Trường hợp response là list hoặc giá trị khác
                return _process_items(response, adapt_datetime, adapt_enums)
            
            except HTTPException:
                # Cho phép HTTPException được raise lên để FastAPI xử lý
                raise
            except Exception as e:
                # Log lỗi và trả về Response lỗi trong trường hợp có lỗi ngoài ý muốn
                logging.error(f"Unexpected error in adapt_response decorator: {str(e)}")
                return JSONResponse(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    content={"detail": "An internal error occurred while processing the response"}
                )
        
        return wrapper
    
    return decorator


def adapt_datetime_response(response_item_key: Optional[str] = None):
    """
    Decorator để tự động chuẩn hóa datetime fields trong response.
    Đảm bảo tất cả datetime objects đều được chuyển thành chuỗi ISO 8601.
    
    Args:
        response_item_key: Key chứa danh sách các item nếu response là collection
        
    Returns:
        Decorator function đã được wrap
    """
    return adapt_response(response_item_key=response_item_key, adapt_datetime=True, adapt_enums=None)


def adapt_win_response(response_item_key: Optional[str] = None):
    """
    Decorator đặc biệt cho WIN API endpoints theo nguyên tắc ontology-first.
    Tự động chuẩn hóa:
    - Các trường datetime sang chuỗi ISO 8601
    - Trường 'status' sang dạng enum chuẩn ontology
    - Trường 'winType' sang dạng enum chuẩn ontology
    
    Args:
        response_item_key: Key chứa danh sách các item nếu response là collection
        
    Returns:
        Decorator function đã được wrap
    """
    # Import lazy để tránh circular dependency
    from .enum_adapter import normalize_win_status, normalize_win_type
    
    return adapt_response(
        response_item_key=response_item_key,
        adapt_datetime=True,
        adapt_enums=[
            {"field": "status", "adapter": normalize_win_status},
            {"field": "winType", "adapter": normalize_win_type}
        ]
    )


def adapt_recognition_response(response_item_key: Optional[str] = None):
    """
    Decorator đặc biệt cho Recognition API endpoints theo nguyên tắc ontology-first.
    Tự động chuẩn hóa:
    - Các trường datetime sang chuỗi ISO 8601
    - Trường 'status' sang dạng enum chuẩn ontology
    - Trường 'recognitionType' sang dạng enum chuẩn ontology
    
    Args:
        response_item_key: Key chứa danh sách các item nếu response là collection
        
    Returns:
        Decorator function đã được wrap
    """
    # Import lazy để tránh circular dependency
    from .enum_adapter import normalize_recognition_type, normalize_recognition_status
    
    return adapt_response(
        response_item_key=response_item_key,
        adapt_datetime=True,
        adapt_enums=[
            {"field": "status", "adapter": normalize_recognition_status},
            {"field": "recognitionType", "adapter": normalize_recognition_type}
        ]
    )


def adapt_task_response(response_item_key: Optional[str] = None):
    """
    Decorator đặc biệt cho Task API endpoints theo nguyên tắc ontology-first.
    Tự động chuẩn hóa:
    - Các trường datetime sang chuỗi ISO 8601
    - Trường 'task_type' sang dạng enum chuẩn ontology
    - Trường 'status' sang dạng enum chuẩn ontology
    
    Args:
        response_item_key: Key chứa danh sách các item nếu response là collection
        
    Returns:
        Decorator function đã được wrap
    """
    # Import lazy để tránh circular dependency
    from .enum_adapter import normalize_task_type, normalize_task_status
    
    return adapt_response(
        response_item_key=response_item_key,
        adapt_datetime=True,
        adapt_enums=[
            {"field": "task_type", "adapter": normalize_task_type},
            {"field": "status", "adapter": normalize_task_status}
        ]
    )


def adapt_knowledge_snippet_response(response_item_key: Optional[str] = None):
    """
    Decorator đặc biệt cho KnowledgeSnippet API endpoints theo nguyên tắc ontology-first.
    Tự động chuẩn hóa:
    - Các trường datetime sang chuỗi ISO 8601
    - Trường 'snippet_type' sang dạng enum chuẩn ontology
    
    Args:
        response_item_key: Key chứa danh sách các item nếu response là collection
        
    Returns:
        Decorator function đã được wrap
    """
    # Import lazy để tránh circular dependency
    from .enum_adapter import normalize_knowledge_snippet_type
    
    # Định nghĩa các adapter cho enum fields
    enum_adapters = [
        {"field": "snippet_type", "adapter": normalize_knowledge_snippet_type}
    ]
    
    return adapt_response(
        response_item_key=response_item_key,
        adapt_datetime=True,
        adapt_enums=enum_adapters
    )


def adapt_project_response(response_item_key: Optional[str] = None):
    """
    Decorator đặc biệt cho Project API endpoints theo nguyên tắc ontology-first.
    Tự động chuẩn hóa:
    - Các trường datetime sang chuỗi ISO 8601
    - Các trường enum liên quan đến Project (nếu có)
    
    Args:
        response_item_key: Key chứa danh sách các item nếu response là collection
        
    Returns:
        Decorator function đã được wrap
    """
    # Hiện tại chỉ chuẩn hóa datetime, nếu có enum cần chuẩn hóa thì bổ sung sau
    enum_adapters = []
    
    return adapt_response(
        response_item_key=response_item_key,
        adapt_datetime=True,
        adapt_enums=enum_adapters
    )


def adapt_event_response(response_item_key: Optional[str] = None):
    """
    Decorator đặc biệt cho Event API endpoints theo nguyên tắc ontology-first.
    Tự động chuẩn hóa:
    - Các trường datetime sang chuỗi ISO 8601
    - Trường 'eventType' sang dạng enum chuẩn ontology (nếu có)
    
    Args:
        response_item_key: Key chứa danh sách các item nếu response là collection
        
    Returns:
        Decorator function đã được wrap
    """
    # Import lazy để tránh circular dependency
    try:
        from .enum_adapter import normalize_event_type
        enum_adapters = [
            {"field": "eventType", "adapter": normalize_event_type},
        ]
    except (ImportError, AttributeError):
        # Fallback nếu không có enum adapter cho event
        logging.warning("Event enum adapter not available, using datetime only")
        enum_adapters = []
    
    return adapt_response(
        response_item_key=response_item_key,
        adapt_datetime=True,
        adapt_enums=enum_adapters
    )


def adapt_ontology_response(
    entity_type: str = None,
    response_item_key: Optional[str] = None,
    adapt_datetime: bool = True,
    custom_adapters: Optional[List[Dict[str, Any]]] = None
):
    """
    Decorator tổng hợp theo nguyên tắc ontology-first.
    Tự động áp dụng các adapter phù hợp với entity_type được chỉ định.
    
    Args:
        entity_type: Loại entity cần áp dụng adapter (win, recognition, task, knowledge_snippet, project)
        response_item_key: Key chứa danh sách các item nếu response là collection
        adapt_datetime: Nếu True thì chuẩn hóa các trường datetime
        custom_adapters: Các adapter tùy chỉnh bổ sung
        
    Returns:
        Decorator function đã được wrap với các adapter phù hợp
    """
    # Tương thích ngược: Import lazy để tránh circular dependency cho code cũ
    try:
        from .enum_adapter import (
            normalize_win_status, normalize_win_type,
            normalize_recognition_status, normalize_recognition_type,
            normalize_task_status, normalize_task_type,
            normalize_knowledge_snippet_type
        )
        
        # Xem entity_type được chỉ định thuộc loại nào
        adapters = []
        
        if entity_type:
            entity_type = entity_type.lower().strip()
            
            # Áp dụng các adapter cho entity_type tương ứng
            if entity_type == 'win':
                adapters.extend([
                    {"field": "status", "adapter": normalize_win_status},
                    {"field": "winType", "adapter": normalize_win_type}
                ])
            elif entity_type == 'recognition':
                adapters.extend([
                    {"field": "status", "adapter": normalize_recognition_status},
                    {"field": "recognitionType", "adapter": normalize_recognition_type}
                ])
            elif entity_type == 'task':
                adapters.extend([
                    {"field": "task_type", "adapter": normalize_task_type},
                    {"field": "status", "adapter": normalize_task_status}
                ])
            elif entity_type == 'knowledge_snippet':
                adapters.append(
                    {"field": "snippet_type", "adapter": normalize_knowledge_snippet_type}
                )
        
        # Thêm các adapter tùy chỉnh nếu có
        if custom_adapters:
            adapters.extend(custom_adapters)
        
        # Logging về việc sử dụng adapter mới
        logging.info(f"Using new entity adapter system for entity type: {entity_type}")
        
        # Định nghĩa decorator cho phiên bản mới
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                try:
                    # Gọi endpoint function gốc
                    result = await func(*args, **kwargs)
                    
                    # Nếu kết quả là None hoặc Response, trả về ngay
                    if result is None or isinstance(result, Response):
                        return result
                        
                    # Sử dụng adapter mới thông qua factory pattern
                    if entity_type:
                        # Lấy entity adapter phù hợp
                        entity_adapter = get_entity_adapter(entity_type, adapt_datetime, True)
                        
                        # Xử lý trường hợp collection
                        if response_item_key and isinstance(result, dict) and response_item_key in result:
                            # Áp dụng adapter cho collection
                            result[response_item_key] = entity_adapter.apply_to_collection(result[response_item_key])
                        elif isinstance(result, list):
                            # Áp dụng adapter cho danh sách
                            result = entity_adapter.apply_to_collection(result)
                        else:
                            # Áp dụng adapter cho single entity
                            result = entity_adapter.apply_to_entity(result)
                    else:
                        # Nếu không chỉ định entity_type, sử dụng adapter cơ bản
                        base_adapter = BaseEntityAdapter(adapt_datetime, False)
                        
                        # Xử lý trường hợp collection
                        if response_item_key and isinstance(result, dict) and response_item_key in result:
                            # Áp dụng adapter cho collection
                            result[response_item_key] = base_adapter.apply_to_collection(result[response_item_key])
                        elif isinstance(result, list):
                            # Áp dụng adapter cho danh sách
                            result = base_adapter.apply_to_collection(result)
                        else:
                            # Áp dụng adapter cho single entity
                            result = base_adapter.apply_to_entity(result)
                    
                    return result
                    
                except HTTPException as http_ex:
                    # Cho phép FastAPI xử lý HTTPException
                    raise http_ex
                except Exception as e:
                    # Log lỗi và trả về 500
                    logging.error(f"Error in adapt_ontology_response: {str(e)}")
                    error_response = JSONResponse(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        content={"detail": f"Internal Server Error: {str(e)}"})
                    return error_response
            return wrapper
            
        return decorator
            
    except ImportError as e:
        # Fallback cho phiên bản cũ nếu chưa có module mới
        logging.warning(f"Using legacy adapter system: {e}")
        return adapt_response(
            response_item_key=response_item_key,
            adapt_datetime=adapt_datetime,
            adapt_enums=custom_adapters
        )
