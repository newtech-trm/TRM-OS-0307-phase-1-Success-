import logging
from typing import Optional, Dict, Any, Union, List
from datetime import datetime

def normalize_datetime(dt_value: Any) -> Optional[str]:
    """
    Chuẩn hóa giá trị datetime thành chuỗi ISO 8601.
    
    Args:
        dt_value: Giá trị datetime từ Neo4j hoặc nguồn khác
        
    Returns:
        Chuỗi ISO 8601 hoặc None nếu không thể chuẩn hóa
    """
    if dt_value is None:
        return None
        
    # Nếu đã có phương thức to_native (Neo4j datetime)
    if hasattr(dt_value, 'to_native'):
        try:
            dt_value = dt_value.to_native()
            logging.debug(f"Converted Neo4j DateTime to native: {dt_value}")
        except Exception as e:
            logging.error(f"Error converting Neo4j DateTime: {e}")
            return None
    
    # Chuyển đổi chuỗi sang datetime nếu cần
    if isinstance(dt_value, str):
        try:
            # Thử parse nhiều định dạng khác nhau
            for fmt in ["%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"]:
                try:
                    dt_value = datetime.strptime(dt_value, fmt)
                    break
                except ValueError:
                    continue
        except Exception as e:
            logging.error(f"Error parsing datetime string '{dt_value}': {e}")
            return None
    
    # Nếu không phải datetime object sau tất cả các chuyển đổi
    if not isinstance(dt_value, datetime):
        logging.error(f"Value is not a datetime object after conversions: {dt_value} ({type(dt_value)})")
        return None
    
    # Chuyển thành chuỗi ISO 8601
    try:
        return dt_value.isoformat()
    except Exception as e:
        logging.error(f"Error converting datetime to ISO format: {e}")
        return None

def normalize_dict_datetimes(data: Dict[str, Any], depth: int = 0, max_depth: int = 10) -> Dict[str, Any]:
    """
    Chuẩn hóa tất cả các trường datetime trong một dictionary, hỗ trợ cấu trúc lồng sâu.
    
    Args:
        data: Dictionary cần xử lý
        depth: Độ sâu hiện tại của đệ quy (mặc định: 0)
        max_depth: Độ sâu tối đa cho phép để tránh đệ quy vô tận (mặc định: 10)
        
    Returns:
        Dictionary với các trường datetime đã được chuẩn hóa
    """
    # Xử lý giá trị None
    if data is None:
        return None
    
    # Trường hợp cơ sở hoặc để tránh đệ quy quá sâu
    if not isinstance(data, dict) or depth >= max_depth:
        if isinstance(data, datetime):
            return normalize_datetime(data)
        elif hasattr(data, 'to_native'):  # Xử lý trường hợp Neo4j datetime trực tiếp
            try:
                return normalize_datetime(data)
            except Exception:
                return data
        return data
        
    # Danh sách các trường có khả năng là datetime
    datetime_fields = [
        # Snake case format
        'created_at', 'createdat', 'updated_at', 'updatedat', 
        'start_date', 'startdate', 'end_date', 'enddate', 
        'due_date', 'duedate', 'target_end_date', 
        'actual_completion_date', 'actualcompletiondate',
        'creation_date', 'creationdate', 'last_modified_date', 
        'lastmodifieddate', 'submission_date', 'submissiondate',
        'expiration_date', 'expirationdate', 'publication_date',
        'publicationdate', 'recognition_date', 'recognitiondate',
        'review_date', 'reviewdate', 'timestamp', 'date',
        
        # Camel case format
        'createdAt', 'updatedAt', 'startDate', 'endDate', 'dueDate', 
        'targetEndDate', 'actualCompletionDate', 'creationDate', 
        'lastModifiedDate', 'submissionDate', 'expirationDate', 
        'publicationDate', 'recognitionDate', 'reviewDate'
    ]
    
    try:
        result = {}
        for key, value in data.items():
            # 1. Xử lý trường hợp value có phương thức to_native như Neo4j datetime
            if hasattr(value, 'to_native'): 
                result[key] = normalize_datetime(value)
                
            # 2. Xử lý các trường thường là datetime (cả snake_case và camelCase)
            elif isinstance(value, datetime) or (key.lower() in datetime_fields or key in datetime_fields):
                result[key] = normalize_datetime(value)
                
            # 3. Xử lý các giá trị là dict lồng nhau
            elif isinstance(value, dict):
                result[key] = normalize_dict_datetimes(value, depth + 1, max_depth)
                
            # 4. Xử lý các trường hợp list chứa dict hoặc list lồng nhau
            elif isinstance(value, list):
                result[key] = _normalize_list_items(value, depth + 1, max_depth)
                
            # 5. Các giá trị khác giữ nguyên
            else:
                result[key] = value
                
        return result
    except Exception as e:
        logging.error(f"Error in normalize_dict_datetimes at depth {depth}: {e}")
        return data  # Trả về dữ liệu gốc nếu có lỗi


def _normalize_list_items(items: List[Any], depth: int = 0, max_depth: int = 10) -> List[Any]:
    """
    Hàm hỗ trợ để chuẩn hóa các phần tử trong danh sách (list).
    
    Args:
        items: Danh sách các phần tử cần chuẩn hóa
        depth: Độ sâu hiện tại của đệ quy
        max_depth: Độ sâu tối đa cho phép
        
    Returns:
        Danh sách sau khi đã chuẩn hóa datetime
    """
    if items is None or depth >= max_depth:
        return items
    
    if not isinstance(items, list):
        # Nếu không phải list, trả về nguyên giá trị
        return items
        
    result = []
    for item in items:
        if isinstance(item, dict):
            # Xử lý dict trong list
            result.append(normalize_dict_datetimes(item, depth + 1, max_depth))
        elif isinstance(item, list):
            # Xử lý list lồng nhau
            result.append(_normalize_list_items(item, depth + 1, max_depth))
        elif isinstance(item, datetime):
            # Xử lý datetime trực tiếp
            result.append(normalize_datetime(item))
        elif hasattr(item, 'to_native'):  # Neo4j datetime
            result.append(normalize_datetime(item))
        else:
            # Các loại dữ liệu khác giữ nguyên
            result.append(item)
    return result
