import logging
from typing import Optional, Dict, Any, Union

def normalize_enum_value(value: Optional[str], enum_choices: Dict[str, str], default: Optional[str] = None) -> Optional[str]:
    """
    Chuẩn hóa giá trị enum từ nhiều dạng khác nhau sang dạng chuẩn của enum.
    
    Args:
        value: Giá trị enum cần chuẩn hóa (có thể là None)
        enum_choices: Dictionary chứa các giá trị enum hợp lệ (key là giá trị chuẩn, value là label)
        default: Giá trị mặc định nếu không tìm thấy kết quả phù hợp
        
    Returns:
        Giá trị enum đã chuẩn hóa hoặc default nếu không tìm thấy
    """
    if value is None:
        return default
    
    try:
        # Chuẩn hóa value thành lowercase và loại bỏ dấu cách
        normalized_input = str(value).lower().strip()
        
        # Case 1: Value đã đúng định dạng chuẩn (key của enum_choices)
        if normalized_input in enum_choices:
            return normalized_input
        
        # Case 2: Value tương ứng với một trong các label (value của enum_choices)
        for enum_key, enum_label in enum_choices.items():
            if normalized_input == enum_label.lower().strip():
                return enum_key
        
        # Case 3: Value trùng với một phần của key hoặc label
        best_match = None
        best_match_score = 0
        
        for enum_key, enum_label in enum_choices.items():
            # Kiểm tra xem normalized_input có nằm trong key hoặc label không
            if normalized_input in enum_key.lower() or normalized_input in enum_label.lower().strip():
                # Tính điểm match dựa trên độ dài của chuỗi match
                match_score = len(normalized_input) / max(len(enum_key), len(enum_label.lower()))
                if match_score > best_match_score:
                    best_match = enum_key
                    best_match_score = match_score
        
        if best_match:
            logging.warning(f"Fuzzy matching enum value '{value}' to '{best_match}'")
            return best_match
        
        # Case 4: Không tìm thấy kết quả phù hợp, trả về default hoặc giá trị gốc
        if default is not None:
            logging.warning(f"Could not normalize enum value '{value}', using default: '{default}'")
            return default
        
        logging.warning(f"Could not normalize enum value '{value}', returning as is")
        return value
    except Exception as e:
        logging.error(f"Error in normalize_enum_value for value '{value}': {e}")
        return default if default is not None else value

def normalize_win_status(status: Optional[str]) -> Optional[str]:
    """
    Chuẩn hóa trạng thái của WIN theo ontology.
    """
    WIN_STATUS_CHOICES = {
        "draft": "Draft",
        "under_review": "Under Review",
        "published": "Published",
        "archived": "Archived",
    }
    return normalize_enum_value(status, WIN_STATUS_CHOICES, "draft")

def normalize_win_type(win_type: Optional[str]) -> Optional[str]:
    """
    Chuẩn hóa loại WIN theo ontology.
    """
    WIN_TYPE_CHOICES = {
        "problem_resolution": "Problem Resolution",
        "insight_discovery": "Insight Discovery",
        "process_optimization": "Process Optimization",
        "learning_milestone": "Learning Milestone",
        "strategic_achievement": "Strategic Achievement",
    }
    return normalize_enum_value(win_type, WIN_TYPE_CHOICES, None)

def normalize_recognition_type(recognition_type: Optional[str]) -> Optional[str]:
    """
    Chuẩn hóa loại Recognition theo ontology.
    """
    RECOGNITION_TYPE_CHOICES = {
        "kudos": "Kudos",
        "appreciation": "Appreciation",
        "celebration": "Celebration",
        "achievement": "Achievement",
        "milestone": "Milestone",
        "breakthrough": "Breakthrough"
    }
    return normalize_enum_value(recognition_type, RECOGNITION_TYPE_CHOICES, None)

def normalize_recognition_status(status: Optional[str]) -> Optional[str]:
    """
    Chuẩn hóa trạng thái Recognition theo ontology.
    """
    RECOGNITION_STATUS_CHOICES = {
        "draft": "Draft",
        "published": "Published",
        "acknowledged": "Acknowledged",
        "archived": "Archived"
    }
    return normalize_enum_value(status, RECOGNITION_STATUS_CHOICES, "draft")

def normalize_task_type(task_type: Optional[str]) -> Optional[str]:
    """
    Chuẩn hóa loại Task theo ontology.
    
    Args:
        task_type: Giá trị task_type cần chuẩn hóa
        
    Returns:
        Giá trị task_type đã được chuẩn hóa theo ontology
    """
    if task_type is None:
        return None
        
    TASK_TYPE_CHOICES = {
        "feature": "Feature",
        "bug": "Bug",
        "chore": "Chore",
        "research": "Research",
        "documentation": "Documentation",
        "meeting": "Meeting"
    }
    
    # Xử lý các trường hợp đặc biệt
    normalized_input = str(task_type).lower().strip()
    
    # Xử lý các trường hợp đặc biệt
    if "doc" in normalized_input and "documentation" not in normalized_input:
        logging.warning(f"Special case: Mapping '{task_type}' to 'documentation'")
        return "documentation"
    elif "research" in normalized_input:
        logging.warning(f"Special case: Mapping '{task_type}' to 'research'")
        return "research"
    
    return normalize_enum_value(task_type, TASK_TYPE_CHOICES, None)

def normalize_task_status(status: Optional[str]) -> Optional[str]:
    """
    Chuẩn hóa trạng thái Task theo ontology.
    
    Args:
        status: Giá trị status cần chuẩn hóa
        
    Returns:
        Giá trị status đã được chuẩn hóa theo ontology
    """
    if status is None:
        return "todo"  # Giá trị mặc định
        
    TASK_STATUS_CHOICES = {
        "todo": "ToDo",
        "inprogress": "InProgress",
        "blocked": "Blocked",
        "inreview": "InReview",
        "done": "Done",
        "cancelled": "Cancelled",
        "backlog": "Backlog"
    }
    
    # Xử lý các trường hợp đặc biệt
    normalized_input = str(status).lower().strip()
    
    # Xử lý các trường hợp đặc biệt
    if "progress" in normalized_input and "inprogress" not in normalized_input:
        logging.warning(f"Special case: Mapping '{status}' to 'inprogress'")
        return "inprogress"
    elif "review" in normalized_input and "inreview" not in normalized_input:
        logging.warning(f"Special case: Mapping '{status}' to 'inreview'")
        return "inreview"
    elif "in progress" == normalized_input:
        logging.warning(f"Special case: Mapping '{status}' to 'inprogress'")
        return "inprogress"
    
    return normalize_enum_value(status, TASK_STATUS_CHOICES, "todo")

def normalize_knowledge_snippet_type(snippet_type: Optional[str]) -> Optional[str]:
    """
    Chuẩn hóa loại KnowledgeSnippet theo ontology.
    
    Args:
        snippet_type: Giá trị snippet_type cần chuẩn hóa
        
    Returns:
        Giá trị snippet_type đã được chuẩn hóa theo ontology
    """
    # Dựa trên phân loại kiến thức phổ biến trong ontology của TRM-OS
    KNOWLEDGE_SNIPPET_TYPE_CHOICES = {
        "best_practice": "Best Practice",
        "lesson_learned": "Lesson Learned", 
        "technical_note": "Technical Note",
        "reference_material": "Reference Material",
        "case_study": "Case Study",
        "insight": "Insight",
        "procedure": "Procedure", 
        "definition": "Definition"
    }
    return normalize_enum_value(snippet_type, KNOWLEDGE_SNIPPET_TYPE_CHOICES, None)
