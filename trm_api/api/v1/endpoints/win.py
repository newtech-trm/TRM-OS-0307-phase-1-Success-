from fastapi import APIRouter, Depends, HTTPException, status, Body, Query
from typing import List, Optional, Dict, Any
import logging

# Schema imports
from trm_api.schemas.win import WIN, WINCreate, WINUpdate, WINList

# Service imports
from trm_api.services.win_service import WinService, win_service
from trm_api.services.user_service import get_current_active_user

# Adapter imports
from trm_api.adapters.enum_adapter import normalize_win_status, normalize_win_type
from trm_api.adapters.datetime_adapter import normalize_datetime, normalize_dict_datetimes
from trm_api.adapters.decorators import adapt_win_response

# Repository imports
from trm_api.repositories.win_repository import WINRepository

router = APIRouter()

@router.post("/", response_model=WIN, status_code=status.HTTP_201_CREATED)
@adapt_win_response()
async def create_win(
    win_in: WINCreate,
    service: WinService = Depends(lambda: win_service)
):
    """
    Tạo mới một WIN (Wisdom-Infused Narrative)
    """
    try:
        logging.info(f"Đang tạo mới WIN với dữ liệu: {win_in.model_dump()}")
        
        # Chuẩn hóa enum
        win_data = win_in.model_dump()
        win_data["status"] = normalize_win_status(win_data.get("status"))
        win_data["win_type"] = normalize_win_type(win_data.get("win_type"))
        
        # Tạo WIN
        result = await service.create_win(win_data=win_data)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Không thể tạo WIN. Vui lòng kiểm tra logs."
            )
            
        # Không cần chuẩn hóa datetime ở đây vì decorator adapt_win_response sẽ làm việc đó
        logging.debug(f"Đã tạo WIN thành công: {result}")
        return result
        
    except Exception as e:
        logging.error(f"Lỗi khi tạo WIN: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi khi tạo WIN: {str(e)}"
        )

@router.get("/{win_id}")
async def get_win(
    win_id: str,
    service: WinService = Depends(lambda: win_service)
):
    """
    Lấy thông tin một WIN cụ thể theo ID
    """
    try:
        logging.info(f"Đang lấy thông tin WIN với ID: {win_id}")
        db_win = await service.get_win(win_id=win_id)
        
        if db_win is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Không tìm thấy WIN với ID: {win_id}"
            )
        
        # Chuẩn hóa enum và datetime
        win_data = db_win
        if isinstance(win_data, dict):
            # Chuẩn hóa enum
            if "status" in win_data:
                win_data["status"] = normalize_win_status(win_data.get("status"))
            if "win_type" in win_data:
                win_data["win_type"] = normalize_win_type(win_data.get("win_type"))
            
            # Chuẩn hóa datetime
            win_data = normalize_dict_datetimes(win_data)
            
        logging.debug(f"Đã lấy thành công thông tin WIN: {win_data}")
        return win_data
        
    except HTTPException as e:
        logging.error(f"HTTP Exception khi lấy WIN: {str(e)}")
        raise
    except Exception as e:
        logging.error(f"Lỗi khi lấy thông tin WIN: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi server khi lấy thông tin WIN: {str(e)}"
        )

@router.get("/")
async def list_wins(
    skip: int = Query(0, ge=0, description="Số item bỏ qua (dùng cho phân trang)"),
    limit: int = Query(25, ge=1, le=100, description="Số item tối đa trả về"),
    service: WinService = Depends(lambda: win_service)
):
    """
    Lấy danh sách các WIN
    """
    try:
        logging.info(f"Đang lấy danh sách WINs. Skip: {skip}, Limit: {limit}")
        
        # Lấy dữ liệu từ service
        wins = await service.list_wins(skip=skip, limit=limit)
        
        # Xử lý trường hợp không có kết quả
        if not wins:
            logging.info("Không có WIN nào được tìm thấy")
            return {"items": [], "count": 0}
        
        # Chuẩn hóa dữ liệu trước khi trả về
        normalized_items = []
        error_items = []
        
        for item in wins:
            try:
                if isinstance(item, dict):
                    # Chuẩn hóa enum
                    if "status" in item:
                        item["status"] = normalize_win_status(item.get("status"))
                    if "win_type" in item:
                        item["win_type"] = normalize_win_type(item.get("win_type"))
                        
                    # Chuẩn hóa datetime
                    normalized_item = normalize_dict_datetimes(item)
                    normalized_items.append(normalized_item)
                else:
                    # Có thể đã là model Pydantic
                    normalized_items.append(item)
            except Exception as e:
                logging.error(f"Lỗi khi chuẩn hóa item WIN: {str(e)}. Item: {item}")
                error_items.append({"item": item, "error": str(e)})
        
        # Báo cáo lỗi nếu có
        if error_items:
            logging.warning(f"Có {len(error_items)} item gặp lỗi khi chuẩn hóa")
            
        result = {"items": normalized_items, "count": len(wins)}
        logging.debug(f"Kết quả danh sách WIN: {len(normalized_items)} items")
        return result
        
    except Exception as e:
        logging.error(f"Lỗi khi lấy danh sách WIN: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi server khi lấy danh sách WIN: {str(e)}"
        )

@router.put("/{win_id}")
async def update_win(
    win_id: str,
    win_in: WINUpdate,
    service: WinService = Depends(lambda: win_service)
):
    """
    Cập nhật một WIN đã tồn tại
    """
    try:
        logging.info(f"Đang cập nhật WIN với ID: {win_id}. Dữ liệu: {win_in.model_dump()}")
        
        # Kiểm tra WIN có tồn tại
        db_win = await service.get_win(win_id=win_id)
        if db_win is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Không tìm thấy WIN với ID: {win_id}"
            )
        
        # Cập nhật WIN
        updated_win = await service.update_win(win_id=win_id, win_update=win_in)
        
        if not updated_win:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail="Có lỗi khi cập nhật WIN. Vui lòng kiểm tra logs."
            )
        
        # Chuẩn hóa dữ liệu trước khi trả về
        normalized_result = normalize_dict_datetimes(updated_win)
        logging.debug(f"Đã cập nhật WIN thành công. Kết quả: {normalized_result}")
        return normalized_result
        
    except HTTPException as e:
        logging.error(f"HTTP Exception khi cập nhật WIN: {str(e)}")
        raise
    except Exception as e:
        logging.error(f"Lỗi khi cập nhật WIN: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi server khi cập nhật WIN: {str(e)}"
        )

@router.delete("/{win_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_win(
    win_id: str,
    service: WinService = Depends(lambda: win_service)
):
    """
    Xóa một WIN
    """
    try:
        logging.info(f"Đang xóa WIN với ID: {win_id}")
        
        # Kiểm tra WIN có tồn tại không
        db_win = await service.get_win(win_id=win_id)
        if db_win is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Không tìm thấy WIN với ID: {win_id}"
            )
        
        # Thực hiện xóa WIN
        deleted = await service.delete_win(win_id=win_id)
        
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail="Có lỗi khi xóa WIN. Vui lòng kiểm tra logs."
            )
            
        logging.info(f"Đã xóa thành công WIN với ID: {win_id}")
        return None
        
    except HTTPException as e:
        logging.error(f"HTTP Exception khi xóa WIN: {str(e)}")
        raise
    except Exception as e:
        logging.error(f"Lỗi khi xóa WIN: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi server khi xóa WIN: {str(e)}"
        )

# --- LEADS_TO_WIN Relationship Endpoints ---

@router.get("/{win_id}/sources", response_model=Dict[str, List])
def get_win_sources(
    win_id: str,
    repository: WINRepository = Depends(lambda: WINRepository())
):
    """
    Get the sources (Projects, RecognitionEvents) connected to a WIN via LEADS_TO_WIN relationship.
    """
    sources = repository.get_win_sources(uid=win_id)
    if not sources:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="WIN not found or no sources available")
    return sources

@router.post("/{win_id}/source-projects/{project_id}", status_code=status.HTTP_201_CREATED)
def connect_project_to_win(
    win_id: str,
    project_id: str,
    relationship_data: Dict[str, Any] = Body(...),
    repository: WINRepository = Depends(lambda: WINRepository())
):
    """
    Connect a Project to a WIN via LEADS_TO_WIN relationship.
    
    The relationship_data can include:
    - contribution_level (int): 1-5 (Minimal to Critical)
    - direct_contribution (bool): Whether the contribution was direct
    - impact_ratio (float): 0.0-1.0 for impact
    - recognition_score (int): 1-100 score
    - notes (str): Additional notes
    """
    # Extract relationship properties from request body
    contribution_level = relationship_data.get("contribution_level", 1)
    direct_contribution = relationship_data.get("direct_contribution", True)
    impact_ratio = relationship_data.get("impact_ratio")
    recognition_score = relationship_data.get("recognition_score")
    notes = relationship_data.get("notes")
    
    # Optional: verified_by and verification_date if supported
    verified_by = relationship_data.get("verified_by")
    verification_date = relationship_data.get("verification_date")
    
    result = repository.connect_project_to_win(
        project_uid=project_id,
        win_uid=win_id,
        contribution_level=contribution_level,
        direct_contribution=direct_contribution,
        impact_ratio=impact_ratio,
        recognition_score=recognition_score,
        verified_by=verified_by,
        verification_date=verification_date,
        notes=notes
    )
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project or WIN not found or connection failed"
        )
    
    return {"status": "success", "message": f"Project {project_id} connected to WIN {win_id}"}

@router.delete("/{win_id}/source-projects/{project_id}")
def disconnect_project_from_win(
    win_id: str,
    project_id: str,
    repository: WINRepository = Depends(lambda: WINRepository())
):
    """
    Remove LEADS_TO_WIN relationship between a Project and a WIN.
    """
    result = repository.disconnect_project_from_win(
        project_uid=project_id,
        win_uid=win_id
    )
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project or WIN not found or disconnection failed"
        )
    
    return {"status": "success", "message": f"Project {project_id} disconnected from WIN {win_id}"}
