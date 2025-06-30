from typing import Optional, List, Any
from datetime import datetime
from pydantic import BaseModel, Field
from uuid import UUID, uuid4

# Enum giá trị cho status và winType để đảm bảo tính nhất quán
# (Phản ánh từ WIN_STATUS_CHOICES và WIN_TYPE_CHOICES trong graph_models/win.py)

class WINStatus:
    DRAFT = "draft"
    UNDER_REVIEW = "under_review"
    PUBLISHED = "published" 
    ARCHIVED = "archived"

class WINType:
    PROBLEM_RESOLUTION = "problem_resolution"
    INSIGHT_DISCOVERY = "insight_discovery"
    PROCESS_OPTIMIZATION = "process_optimization"
    LEARNING_MILESTONE = "learning_milestone"
    STRATEGIC_ACHIEVEMENT = "strategic_achievement"

# Base schema với các thuộc tính chung
class WINBase(BaseModel):
    """
    Schema base cho WIN (Wisdom-Infused Narrative) trong TRM-OS.
    Chứa các thuộc tính chung cho mọi chức năng liên quan.
    """
    name: str = Field(..., description="Tên mô tả ngắn gọn cho WIN")
    narrative: str = Field(..., description="Chi tiết câu chuyện WIN, bao gồm context, actions, outcomes, và key learnings")
    status: str = Field(default=WINStatus.DRAFT, description="Trạng thái hiện tại của WIN")
    winType: Optional[str] = Field(None, description="Phân loại hoặc loại WIN")
    impact_level: int = Field(default=1, description="Đại diện số cho mức độ ảnh hưởng của WIN (1-Low đến 5-High)")
    tags: List[str] = Field(default_factory=list, description="Các tag liên quan để phân loại và tìm kiếm WINs")

# Schema cho việc tạo mới WIN
class WINCreate(WINBase):
    """Schema cho việc tạo mới một WIN"""
    # Cho phép uid được tạo tự động nếu không được cung cấp
    uid: Optional[str] = Field(default=None, description="Unique ID cho WIN, được tạo tự động nếu không được cung cấp")

# Schema cho việc cập nhật WIN
class WINUpdate(BaseModel):
    """Schema cho việc cập nhật một WIN hiện có"""
    name: Optional[str] = Field(None, description="Tên mô tả ngắn gọn cho WIN")
    narrative: Optional[str] = Field(None, description="Chi tiết câu chuyện WIN")
    status: Optional[str] = Field(None, description="Trạng thái hiện tại của WIN")
    winType: Optional[str] = Field(None, description="Phân loại hoặc loại WIN")
    impact_level: Optional[int] = Field(None, description="Đại diện số cho mức độ ảnh hưởng của WIN")
    tags: Optional[List[str]] = Field(None, description="Các tag liên quan để phân loại và tìm kiếm WINs")

# Schema đầy đủ cho WIN bao gồm thông tin từ database
class WINInDB(WINBase):
    """Schema cho WIN đã được lưu trữ trong database"""
    uid: str = Field(..., description="Unique ID của WIN")
    created_at: datetime = Field(..., description="Thời điểm WIN được tạo")
    updated_at: datetime = Field(..., description="Thời điểm WIN được cập nhật lần cuối")

    model_config = {
        "from_attributes": True,
        "populate_by_name": True
    }

# Schema cho việc hiển thị WIN
class WIN(WINInDB):
    """Schema cho việc trả về thông tin WIN đầy đủ"""
    # Có thể bổ sung thêm các trường tính toán hoặc quan hệ khác
    pass

# Schema cho việc liệt kê nhiều WINs
class WINList(BaseModel):
    """Schema cho danh sách các WINs"""
    items: List[WIN] = []
    count: int = 0
