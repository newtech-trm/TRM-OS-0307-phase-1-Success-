# Enum Adapter Pattern trong TRM-OS

**Ngày tạo:** 2025-07-03

**Phiên bản:** 1.0

**Tác giả:** TRM Engineering Team

## Vấn đề

Trong dự án TRM-OS, chúng ta đối mặt với nhiều thách thức khi làm việc với các giá trị enum giữa các lớp của hệ thống:

1. **Không nhất quán về định dạng**: Enum được biểu diễn dưới nhiều dạng khác nhau (`UPPERCASE`, `lowercase`, `camelCase`, `PascalCase`)
2. **Sự hiện diện của prefix**: Một số giá trị enum chứa prefix lớp enum (ví dụ: `TaskStatus.TODO` thay vì chỉ `TODO`)
3. **Xung đột với Neo4j**: Neo4j yêu cầu các giá trị enum được lưu trữ theo định dạng cụ thể (camelCase không có prefix)
4. **InflateError trong Neo4j**: Lỗi thường gặp khi deserialize các đối tượng từ Neo4j do không nhất quán về enum

## Giải pháp: Enum Adapter Pattern

### Nguyên tắc cốt lõi

Chúng tôi triển khai một Enum Adapter Pattern để tự động chuẩn hóa giá trị enum ở lớp gần với cơ sở dữ liệu nhất, đảm bảo tất cả enum được lưu theo định dạng chuẩn của Neo4j.

### Đặc điểm chính

1. **Chuẩn hóa tại Repository Layer**: Thực hiện chuẩn hóa enum tại lớp repository, ngay trước khi tương tác với Neo4j
2. **Tự động loại bỏ prefix enum**: Loại bỏ các prefix như `TaskStatus.`, `TaskType.`, v.v.
3. **Chuyển đổi sang định dạng chuẩn**: Chuyển đổi tất cả enum về định dạng camelCase không có prefix
4. **Logging chi tiết**: Ghi nhật ký quá trình chuẩn hóa để dễ dàng debug khi cần thiết

## Triển khai

### Lớp EnumAdapter

```python
class EnumAdapter:
    @staticmethod
    def normalize_enum_value(enum_class: Optional[Enum], value: Any) -> Any:
        if value is None or enum_class is None:
            return value
            
        if isinstance(value, enum_class):
            return value
            
        str_value = str(value).strip()
        
        # Loại bỏ prefix nếu có
        if '.' in str_value:
            parts = str_value.split('.')
            if len(parts) == 2 and parts[0] == enum_class.__name__:
                enum_key = parts[1]
                for enum_item in enum_class:
                    if enum_item.name == enum_key:
                        return enum_item
        
        # Tìm enum phù hợp
        try:
            return enum_class(str_value)
        except (ValueError, KeyError):
            # Thử tìm theo tên
            for enum_item in enum_class:
                if enum_item.name.lower() == str_value.lower():
                    return enum_item
            
            # Thử tìm theo giá trị
            for enum_item in enum_class:
                if str(enum_item.value).lower() == str_value.lower():
                    return enum_item
            
            # Không tìm thấy, trả về giá trị gốc
            return value
```

### Sử dụng trong Task Repository

```python
def create_task(self, task_data: dict) -> dict:
    # Chuẩn hóa enum trước khi lưu vào Neo4j
    if "status" in task_data:
        task_data["status"] = EnumAdapter.normalize_enum_value(
            TaskStatus, task_data["status"]
        )
    
    if "task_type" in task_data:
        task_data["task_type"] = EnumAdapter.normalize_enum_value(
            TaskType, task_data["task_type"]
        )
    
    if "effort_unit" in task_data:
        task_data["effort_unit"] = EnumAdapter.normalize_enum_value(
            EffortUnit, task_data["effort_unit"]
        )
    
    # Tiếp tục tạo task trong Neo4j
    # ...
```

## Lợi ích

1. **Tính nhất quán**: Đảm bảo tất cả enum được lưu trong Neo4j theo định dạng chuẩn
2. **Linh hoạt**: Hỗ trợ nhiều định dạng đầu vào khác nhau, tăng khả năng tương thích
3. **Dễ bảo trì**: Logic chuẩn hóa enum được tập trung tại một nơi, dễ dàng cập nhật
4. **Ngăn ngừa lỗi**: Giảm thiểu các lỗi InflateError khi deserialize dữ liệu từ Neo4j

## Hướng dẫn sử dụng

1. **Trong repository**: Sử dụng `EnumAdapter.normalize_enum_value(enum_class, value)` cho mỗi trường enum
2. **Trong code khác**: Khi làm việc trực tiếp với Neo4j, hãy đảm bảo enum được chuẩn hóa trước khi truyền vào

## Tài liệu liên quan

- [Ontology Nội bộ TRM v3.2](../ONTOLOGY%20NỘI%20BỘ%20TRM%20-%20BẢN%20THIẾT%20KẾ%20THỐNG%20NHẤT%20HOÀN%20CHỈNH%20V3.2.md)
- [GAP Analysis Ontology V3.2](../GAP_ANALYSIS_ONTOLOGY_V3.2.md)
