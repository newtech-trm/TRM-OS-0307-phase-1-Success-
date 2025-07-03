# Core Relationships for TRM-OS MVP

This document defines the core relationships (edges) between the entities for the TRM-OS MVP. These relationships are fundamental to how the knowledge graph is structured in Neo4j and represent the verbs connecting the nouns (entities).

> **Lưu ý về naming convention**: Để đảm bảo sự nhất quán với tài liệu gốc Ontology V3.2, tài liệu này sử dụng quy ước đặt tên `camelCase` cho tất cả các thuộc tính và mối quan hệ.
> 
> **Về sự đơn giản hóa**: Các mối quan hệ trong tài liệu MVP này là phiên bản đơn giản hóa từ tài liệu gốc Ontology V3.2 (ONTOLOGY NỘI BỘ TRM - BẢN THIẾT KẾ THỐNG NHẤT HOÀN CHỈNH V3.2). Các thuộc tính phức tạp sẽ được bổ sung trong các phiên bản sau.

---

## 1. `(Task)-[:RESOLVES]->(Tension)`

- **Description:** This is a primary action-oriented relationship. It signifies that a specific `Task` is created with the intention of resolving a `Tension`.
- **Direction:** `Task` -> `Tension`
- **Source Node:** `Task`
- **Target Node:** `Tension`
- **Properties (Optional for MVP):**
  - `effectivenessScore` (Float): A score indicating how effectively the task resolved the tension, can be added later. [Thay thế cho `effectiveness_score`]
- **Hiện trạng (2025-07-03):** 
  - Đã triển khai đầy đủ trong graph_models, repositories, services và API endpoints
  - Đã cung cấp đầy đủ phương thức connect/disconnect/query trong TaskRepository
  - Đã triển khai các API endpoints trong TaskController: `/tasks/{task_id}/resolves/{tension_id}`, `/tasks/{task_id}/resolves`, và `/tasks/{task_id}/with-relationships`
  - Đã viết test cases cho quan hệ RESOLVES

---

## 2. `(Agent)-[:PERFORMS]->(Task)`

- **Description:** Indicates that an `Agent` (AI or human) is assigned to or has executed a `Task`.
- **Direction:** `Agent` -> `Task`
- **Source Node:** `Agent`
- **Target Node:** `Task`
- **Properties:**
  - `assignedAt` (Datetime): When the task was assigned. [Thay thế cho `assigned_at`]
  - `status` (String): The agent's status regarding the task (e.g., `assigned`, `working`, `completed`). [Đã chuyển về camelCase]
- **Hiện trạng (2025-06-15):** 
  - Đã định nghĩa relationship nhưng chưa triển khai đầy đủ API endpoint
  - Cần lưu ý sử dụng custom Neo4jDateTimeProperty cho trường assignedAt để đảm bảo xử lý đúng datetime (theo bài học từ Event API)

---

## 3. `(Task)-[:PART_OF]->(Project)`

- **Description:** Connects a `Task` to a larger `Project`, providing hierarchical context.
- **Direction:** `Task` -> `Project`
- **Source Node:** `Task`
- **Target Node:** `Project`
- **Hiện trạng (2025-06-15):** 
  - Đã định nghĩa trong mô hình Task nhưng chưa triển khai đầy đủ API endpoint
  - Cần đảm bảo import Project vào task.py để tránh lỗi tương tự như đã gặp với Event API

---

## 4. `(Tension)-[:AFFECTS]->(Project)`

- **Description:** Shows that a `Tension` has an impact on a specific `Project`.
- **Direction:** `Tension` -> `Project`
- **Source Node:** `Tension`
- **Target Node:** `Project`
- **Hiện trạng (2025-06-15):** 
  - Đã định nghĩa trong ontology nhưng chưa triển khai trong code
  - Cần triển khai sau khi hoàn thiện Tension API và Project API

---

## 5. `(Agent)-[:ACTOR_TRIGGERED_EVENT]->(Event)`

- **Description:** Signifies that an `Agent` has performed an action that resulted in a noteworthy `Event` being created.
- **Direction:** `Agent` -> `Event`
- **Source Node:** `Agent`
- **Target Node:** `Event`
- **Hiện trạng (2025-06-15):**
  - Đã triển khai thành công trong Event API, quan hệ được xây dựng qua trường `triggered_by_actor` của `EventGraphModel`
  - Trong `event.py`, được định nghĩa dưới dạng `triggered_by_actor = RelationshipFrom('trm_api.graph_models.agent', 'Agent', 'ACTOR_TRIGGERED_EVENT')`
  - Seed event tạo relationship này thành công thông qua `scripts/seed_event_data.py`

---

## 6. `(Event)-[:EVENT_CONTEXT]->(Entity)`

- **Description:** Quan hệ liên kết từ một `Event` đến entity chính mà sự kiện liên quan đến. Cho phép tạo event log linh hoạt và có thể kiểm tra.
- **Direction:** `Event` -> `Entity`
- **Source Node:** `Event`
- **Target Node:** Có thể là `Agent`, `Project`, `Task`, `Resource` hoặc entity khác.
- **Hiện trạng (2025-06-15):**
  - Ban đầu gặp lỗi với cách tiệp cận dùng BaseNode trừ u tượng (AttributeError: type object 'BaseNode' has no attribute '__label__')
  - Đã refactor thành các relationship riêng biệt cho từng loại entity:

    ```python
    primary_context_agent = RelationshipTo('trm_api.graph_models.agent', 'Agent', 'EVENT_CONTEXT')
    primary_context_project = RelationshipTo('trm_api.graph_models.project', 'Project', 'EVENT_CONTEXT')
    primary_context_task = RelationshipTo('trm_api.graph_models.task', 'Task', 'EVENT_CONTEXT')
    primary_context_resource = RelationshipTo('trm_api.graph_models.resource', 'Resource', 'EVENT_CONTEXT')
    ```

  - Sử dụng trường `context_node_label` trong API payload để xác định loại entity khi tạo relationship
  - Đã sử dụng được trong seed script và tạo relationship thành công

- **Example Usage:**

  ```json

---

## 7. `(Tension)-[:LEADS_TO_WIN]->(WIN)`

- **Description:** Quan hệ thể hiện rằng một `Tension` đã dẫn đến việc tạo ra hoặc đóng góp cho một `WIN` (What's Important Now).
- **Direction:** `Tension` -> `WIN`
- **Source Node:** `Tension`
- **Target Node:** `WIN`
- **Properties:**
  - `contributionLevel` (Integer): Mức độ đóng góp của Tension cho WIN, từ 1 (thấp) đến 5 (cao).
  - `directContribution` (Boolean): Xác định liệu Tension có trực tiếp dẫn đến WIN hay không.
  - `createdAt` (Datetime): Thời điểm thiết lập mối quan hệ.
- **Hiện trạng (2025-07-03):**
  - Đã triển khai đầy đủ trong graph_models (Tension và WIN), repositories, services và API endpoints
  - Đã cung cấp đầy đủ phương thức connect/disconnect/query trong TensionRepository
  - Đã triển khai các API endpoints trong TensionController: `/tensions/{tension_id}/leads-to-win/{win_id}`, `/tensions/{tension_id}/leads-to-win`, và `/tensions/{tension_id}/with-relationships`
  - Đã viết test cases cho quan hệ LEADS_TO_WIN
  {
    "name": "TASK_COMPLETED",
    "description": "A task was completed",
    "context_node_id": "task-123",
    "context_node_label": "Task",  // Sử dụng để định tuyến relationship
    "actor_id": "agent-456",
    "payload": {"completion_time": "2025-06-10T15:30:00", "status": "done"}
  }
  ```
