# Kiến trúc Ontology-First của TRM-OS (V3.2)

## Tổng quan

Kiến trúc Ontology-First là nền tảng cốt lõi của TRM-OS, đặt ontology (định nghĩa về các thực thể và mối quan hệ giữa chúng) làm trung tâm của toàn bộ hệ thống. Tài liệu này mô tả chi tiết triết lý thiết kế, cách triển khai và hướng dẫn tuân thủ.

## Nguyên tắc cơ bản

1. **Ontology là nguồn sự thật duy nhất**: Tất cả các thực thể, thuộc tính và mối quan hệ phải tuân theo định nghĩa ontology.

2. **Chuẩn hóa dữ liệu**: Tất cả các enum phải ở dạng camelCase không prefix, datetime ở định dạng ISO 8601 UTC.

3. **Phân tách trách nhiệm**: Repository layer chịu trách nhiệm chuẩn hóa dữ liệu trước khi lưu, API layer chịu trách nhiệm chuẩn hóa dữ liệu trước khi trả về.

4. **Adapter pattern**: Sử dụng các adapter để chuẩn hóa dữ liệu đầu vào/ra một cách nhất quán.

5. **Event-driven**: Sử dụng event bus để giao tiếp giữa các thành phần, đảm bảo tính lỏng lẻo và mở rộng được.

## Các thành phần chính

### 1. Neo4j Graph Models

Mỗi entity trong ontology được biểu diễn bằng một graph model (ví dụ: Task, Project, Agent, etc.). Các model này định nghĩa:

- Các thuộc tính (properties) của entity
- Các mối quan hệ (relationships) với các entity khác
- Các constraint và index

Ví dụ về Task entity:

```python
class Task(StructuredNode):
    uid = UniqueIdProperty()
    title = StringProperty(required=True)
    description = StringProperty()
    status = StringProperty(default="todo")  # Lưu ý: Lưu dạng camelCase không prefix
    task_type = StringProperty(default="regular")
    created_at = DateTimeProperty(default=get_utc_now)
    updated_at = DateTimeProperty(default=get_utc_now)
    
    # Relationships
    project = RelationshipTo("Project", "IS_PART_OF_PROJECT")
    assigned_agents = RelationshipFrom("Agent", "ASSIGNS_TASK")
```

### 2. Adapter Layer

Adapter layer đảm bảo dữ liệu được chuẩn hóa khi di chuyển giữa các thành phần của hệ thống:

- **EnumAdapter**: Chuẩn hóa các giá trị enum
- **DateTimeAdapter**: Chuẩn hóa các giá trị datetime
- **Response Decorators**: Chuẩn hóa dữ liệu trả về từ API

### 3. Service Layer

Service layer chịu trách nhiệm cho logic nghiệp vụ, gọi các adapter khi cần thiết và tương tác với repository layer. Tất cả các method trong service layer đều là async để hỗ trợ xử lý đồng thời.

### 4. API Layer

API layer cung cấp các REST endpoint và áp dụng decorator để chuẩn hóa dữ liệu trả về.

### 5. SystemEventBus

EventBus là cơ chế giao tiếp giữa các thành phần trong hệ thống, đặc biệt là giữa các Agent.

## Cách triển khai

### Chuẩn hóa Enum

Mỗi enum phải được chuẩn hóa về dạng camelCase không prefix trước khi lưu vào Neo4j và khi trả về từ API:

```python
from trm_api.adapters.enum_adapter import EnumAdapter

# Chuẩn hóa khi lưu vào database
status_value = EnumAdapter.normalize_task_status(status)

# Chuẩn hóa khi trả về từ API
@adapt_task_response
def get_task(task_uid: str):
    # ...
```

### Chuẩn hóa DateTime

Mọi giá trị datetime phải được chuẩn hóa về ISO 8601 UTC:

```python
from trm_api.adapters.datetime_adapter import normalize_dict_datetimes

# Tự động áp dụng qua decorator
@adapt_task_response
def get_tasks():
    # ...
```

### Triển khai Relationship

Tất cả các mối quan hệ (relationship) phải được định nghĩa trong graph model và có API endpoint tương ứng.

## Kiểm thử

Kiểm thử tích hợp (integration test) phải được viết cho tất cả các entity và relationship để đảm bảo tuân thủ ontology. Sử dụng async test với pytest-asyncio.

## Giai đoạn tiếp theo

Sau khi hoàn thành triển khai Ontology-First, các giai đoạn tiếp theo bao gồm:

1. **Xây dựng Agent Ecosystem**: Phát triển các AI agent dựa trên nền tảng ontology.
2. **Tích hợp Generative AI**: Tích hợp các mô hình AI vào hệ thống.
3. **Phát triển UI/UX**: Xây dựng giao diện người dùng dựa trên ontology.

## Tài liệu liên quan

- [Enum Adapter Pattern](../technical-decisions/enum-adapter-pattern.md)
- [Async API Pattern](../technical-decisions/async-api-pattern.md)
- [Integration Testing Guide](../integration-testing/async-testing-guide.md)
