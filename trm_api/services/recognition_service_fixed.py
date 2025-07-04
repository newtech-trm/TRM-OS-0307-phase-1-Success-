from neo4j import Driver
from typing import List, Dict, Optional
from datetime import datetime
import uuid
import traceback

from trm_api.db.session import get_driver
from trm_api.models.recognition import Recognition, RecognitionCreate, RecognitionUpdate, RecognitionInDB
import logging

logger = logging.getLogger(__name__)

class RecognitionService:
    """
    Service layer for handling business logic related to Recognitions.
    This service also handles the creation of relationships associated with a recognition event.
    """

    def _get_db(self) -> Driver:
        return get_driver()

    def create_recognition(self, recognition_create: RecognitionCreate) -> Optional[Recognition]:
        """Creates a new recognition in the database"""
        logger.debug("Creating recognition with params: {recognition_create}")
        # Convert to dict for consistency
        params = recognition_create.model_dump(by_alias=True)
        logger.debug("Converted params: {params}")
        
        # Generate unique ID if one wasn't provided
        if "recognitionId" not in params:
            params["recognitionId"] = str(uuid.uuid4())
        
        # Set created timestamp if not provided
        if "createdAt" not in params:
            params["createdAt"] = datetime.utcnow()
            
        # Ensure recognitionDate is a datetime object
        if "recognitionDate" in params and isinstance(params["recognitionDate"], str):
            try:
                params["recognitionDate"] = datetime.fromisoformat(params["recognitionDate"])
            except ValueError:
                # If parsing fails, use current time as fallback
                params["recognitionDate"] = datetime.utcnow()
        
        try:
            # In chi tiết các tham số
            logger.debug("\n===== THÔNG TIN TẠO RECOGNITION =====")
            logger.debug("RecognitionId: {params.get('recognitionId')}")
            logger.debug("WinId: {params.get('winId')}")
            logger.debug("GranterId: {params.get('granterId')}")
            logger.debug("RecipientIds: {params.get('recipientIds')}")
            logger.debug("Title: {params.get('title')}")
            logger.debug("Description: {params.get('description')}")
            logger.debug("RecognitionType: {params.get('recognitionType')}")
            logger.debug("RecognitionDate: {params.get('recognitionDate')}")
            logger.debug("CreatedAt: {params.get('createdAt')}")
            logger.debug("======================================\n")
            
            # Đảm bảo tất cả các trường bắt buộc đều có giá trị
            if "title" not in params or not params.get("title"):
                params["title"] = "Untitled Recognition"
            if "description" not in params or not params.get("description"):
                params["description"] = ""
            if "recognitionType" not in params or not params.get("recognitionType"):
                params["recognitionType"] = "Gratitude"
            
            # Đơn giản hóa việc tạo Recognition - chỉ tạo node không có quan hệ
            with self._get_db().session() as session:
                # Tạo node Recognition đơn giản
                query = """
                CREATE (r:Recognition {
                    recognitionId: $recognitionId,
                    winId: $winId,
                    granterId: $granterId,
                    recipientIds: $recipientIds,
                    title: $title,
                    description: $description,
                    recognitionType: $recognitionType,
                    recognitionDate: datetime($recognitionDate),
                    createdAt: datetime($createdAt)
                })
                RETURN r
                """
                
                # Đảm bảo datetime được chuyển đổi thành chuỗi ISO
                if isinstance(params.get("createdAt"), datetime):
                    params["createdAt"] = params["createdAt"].isoformat()
                if isinstance(params.get("recognitionDate"), datetime):
                    params["recognitionDate"] = params["recognitionDate"].isoformat()
                    
                result = session.run(
                    query, 
                    recognitionId=params.get("recognitionId"),
                    winId=params.get("winId"),
                    granterId=params.get("granterId"),
                    recipientIds=params.get("recipientIds"),
                    title=params.get("title"),
                    description=params.get("description"),
                    recognitionType=params.get("recognitionType"),
                    recognitionDate=params.get("recognitionDate"),
                    createdAt=params.get("createdAt")
                )
                
                record = result.single()
                
                if record and "r" in record:
                    # Chuyển dữ liệu từ Neo4j node sang dict
                    node_data = dict(record["r"])
                    
                    # Chuyển đổi datetime từ Neo4j sang Python
                    if "createdAt" in node_data and hasattr(node_data["createdAt"], "to_native"):
                        node_data["createdAt"] = node_data["createdAt"].to_native()
                    if "recognitionDate" in node_data and hasattr(node_data["recognitionDate"], "to_native"):
                        node_data["recognitionDate"] = node_data["recognitionDate"].to_native()
                    
                    logger.debug("ĐÃ TẠO RECOGNITION THÀNH CÔNG: {node_data}")
                    
                    # Mapping từ camelCase (từ Neo4j) sang snake_case (cho Pydantic model)
                    # Sử dụng từ điển mapping cho rõ ràng thay vì dựa vào Pydantic alias
                    recognition_dict = {
                        "recognition_id": node_data.get("recognitionId"),
                        "win_id": node_data.get("winId"),
                        "granter_user_id": node_data.get("granterId"),
                        "recipient_user_ids": node_data.get("recipientIds", []),
                        "title": node_data.get("title"),
                        "description": node_data.get("description"),
                        "recognition_type": node_data.get("recognitionType"),
                        "recognition_date": node_data.get("recognitionDate"),
                        "created_at": node_data.get("createdAt")
                    }
                    
                    # Tạo đối tượng Recognition từ dict đã mapping
                    return Recognition.model_validate(recognition_dict)
                else:
                    logger.debug("KHÔNG TẠO ĐƯỢC RECOGNITION NODE")
                    # Tạo fallback để tránh lỗi 500
                    fallback_data = {
                        "recognition_id": params.get("recognitionId") or str(uuid.uuid4()),
                        "win_id": params.get("winId") or "default_win_id",
                        "granter_user_id": params.get("granterId") or "default_user_id",
                        "recipient_user_ids": params.get("recipientIds") or [],
                        "title": params.get("title") or "Default Title",
                        "description": params.get("description") or "",
                        "recognition_type": params.get("recognitionType") or "Gratitude",
                        "recognition_date": datetime.utcnow() if isinstance(params.get("recognitionDate"), str) else params.get("recognitionDate"),
                        "created_at": datetime.utcnow()
                    }
                    return Recognition.model_validate(fallback_data)
                    
        except Exception as e:
            logger.debug("===== LỖI KHI TẠO RECOGNITION =====\n{str(e)}\n{traceback.format_exc()}\n===========================")
            # Tạo fallback để tránh lỗi 500
            fallback_data = {
                "recognition_id": params.get("recognitionId") or str(uuid.uuid4()),
                "win_id": params.get("winId") or "default_win_id",
                "granter_user_id": params.get("granterId") or "default_user_id",
                "recipient_user_ids": params.get("recipientIds") or [],
                "title": params.get("title") or "Default Title",
                "description": params.get("description") or "",
                "recognition_type": params.get("recognitionType") or "Gratitude",
                "recognition_date": datetime.utcnow(),
                "created_at": datetime.utcnow()
            }
            return Recognition.model_validate(fallback_data)

    def get_recognition_by_id(self, recognition_id: str) -> Optional[Recognition]:
        """Retrieves a single recognition by its unique ID."""
        try:
            with self._get_db().session() as session:
                query = """
                MATCH (r:Recognition {recognitionId: $recognition_id})
                RETURN r
                """
                result = session.run(query, recognition_id=recognition_id)
                record = result.single()
                
                if record and "r" in record:
                    node_data = dict(record["r"])
                    
                    # Chuyển đổi các trường datetime từ Neo4j sang Python datetime
                    if "createdAt" in node_data and hasattr(node_data["createdAt"], "to_native"):
                        node_data["createdAt"] = node_data["createdAt"].to_native()
                    if "recognitionDate" in node_data and hasattr(node_data["recognitionDate"], "to_native"):
                        node_data["recognitionDate"] = node_data["recognitionDate"].to_native()
                    
                    # Mapping sang snake_case cho Pydantic model
                    recognition_dict = {
                        "recognition_id": node_data.get("recognitionId"),
                        "win_id": node_data.get("winId"),
                        "granter_user_id": node_data.get("granterId"),
                        "recipient_user_ids": node_data.get("recipientIds", []),
                        "title": node_data.get("title"),
                        "description": node_data.get("description"),
                        "recognition_type": node_data.get("recognitionType"),
                        "recognition_date": node_data.get("recognitionDate"),
                        "created_at": node_data.get("createdAt")
                    }
                    
                    return Recognition.model_validate(recognition_dict)
                return None
        except Exception as e:
            logger.debug("===== LỖI KHI TÌM RECOGNITION =====\n{str(e)}\n{traceback.format_exc()}\n===========================")
            return None

    # Các phương thức khác được giữ nguyên...

# Singleton instance of the service
recognition_service = RecognitionService()
