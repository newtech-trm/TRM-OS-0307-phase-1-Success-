# CHỈ DẪN BỐI CẢNH DỰ ÁN TRM-OS

## 1. Tổng quan dự án

TRM-OS là một hệ thống quản lý tri thức và workflow dựa trên ontology, sử dụng Neo4j làm cơ sở dữ liệu đồ thị để lưu trữ các entity, relationship và tổ chức dữ liệu theo mô hình ontology-first.

### File nền tảng quan trọng

- **@ONTOLOGY NỘI BỘ TRM - BẢN THIẾT KẾ THỐNG NHẤT HOÀN CHỈNH V3.2.md** - File "Hiến pháp" chứa đầy đủ định nghĩa ontology
- **@trmos-sumary-documentation.md** - File tóm tắt các thông tin về TRM-OS
- **@GAP_ANALYSIS_ONTOLOGY_V3.2.md** - File phân tích khoảng cách giữa ontology định nghĩa và triển khai thực tế
- **@plan.md** - File kế hoạch triển khai dự án theo phương pháp ontology-first

### Thư mục docs chứa các tài liệu kỹ thuật

- **docs/core-specs/entities-mvp.md** - Định nghĩa chi tiết các entity cho MVP
- **docs/core-specs/relationships-mvp.md** - Định nghĩa chi tiết các relationship cho MVP
- **docs/core-specs/agent-workflows.md** - Mô tả luồng làm việc của các agent
- **docs/core-specs/philosophy-in-code.md** - Triết lý chuyển đổi từ ontology sang code

## 2. Chiến lược triển khai: Ontology-first

- **Nguyên tắc chính**: Xây dựng hệ thống dựa trên ontology đã định nghĩa, không đơn giản hóa hay mock dữ liệu.
- **Cách tiếp cận**: Từ định nghĩa ontology, xây dựng các graph model, API endpoint, và service layer phù hợp.
- **Quy trình**:
  1. Định nghĩa entity trong Neo4j (node class)
  2. Định nghĩa relationship giữa các entity
  3. Xây dựng API endpoint cho entity và relationship
  4. Triển khai service layer để xử lý logic nghiệp vụ
  5. Kiểm thử CRUD và các luồng nghiệp vụ
  6. Seed dữ liệu mẫu để validate hoạt động đúng của ontology

## 3. Hiện trạng dự án

### Kết quả đạt được

- ✅ **Entity Agent**: Đã triển khai đầy đủ, API endpoint hoạt động ổn định
- ✅ **Entity Event**: Đã triển khai thành công, fix hết các lỗi và seed dữ liệu thành công
- ✅ **Entity Recognition**: Đã triển khai thành công, sửa các lỗi validation và enum không đồng nhất
- ✅ **Entity Win**: Đã triển khai đầy đủ, chuyển đổi sang async hoàn chỉnh cho tất cả phương thức
- ✅ **Entity KnowledgeSnippet**: Đã triển khai đầy đủ theo ontology-first
- ✅ **Relationships**: Đã triển khai thành công các relationship chính:
  - ACTOR_TRIGGERED_EVENT (Agent -> Event)
  - EVENT_CONTEXT (Event -> [Agent, Project, Task, Resource])
  - GIVEN_BY và RECEIVED_BY (Recognition <-> Agent)
  - RECOGNIZES_WIN (Recognition -> WIN)
  - RECOGNIZES_CONTRIBUTION_TO (Recognition -> [Project, Task, Resource])
  - GENERATES_KNOWLEDGE (WIN -> KnowledgeSnippet)
  - LEADS_TO_WIN (Project/Event -> WIN)

### Chuyển đổi Async hoàn chỉnh

- ✅ **Project Service**: Đã chuyển đổi toàn bộ phương thức sang async
- ✅ **Task Service**: Đã chuyển đổi toàn bộ phương thức sang async
- ✅ **Recognition Service**: Đã chuyển đổi toàn bộ phương thức sang async bao gồm update_recognition, delete_recognition, get_recognition_with_relationships
- ✅ **Win Service**: Đã chuyển đổi các phương thức list_wins, update_win, delete_win sang async
- ✅ **API Layer**: Đã chuyển đổi các endpoint trong Project, Task, Recognition, Win sang async
- ✅ **Testing**: Đã cập nhật một số test sang async-compatible với pytest-asyncio và AsyncMock

### Fix lỗi đã thực hiện

1. **Neo4jDateTimeProperty**: Tạo custom property type để xử lý đúng định dạng DateTime trong Neo4j
2. **Refactor relationship context**: Chuyển từ relationship trừ u tượng sang concrete relationship cho từng entity type
3. **Serialize DateTime**: Thêm adapter để chuyển đổi datetime object thành string ISO format khi trả về response
4. **Import Class**: Bổ sung đúng các import cho Resource, Project trong agent.py
5. **Async Migration**: Chuyển đổi đúng cách các phương thức từ sync sang async
6. **Transaction Management**: Đảm bảo các phương thức async xử lý transaction Neo4j đúng cách
7. **Capabilities Array**: Refactor từ JSONProperty sang ArrayProperty(StringProperty()) để tương thích với dữ liệu
8. **Enum Adapter**: Tạo module `enum_adapter.py` để chuẩn hóa giá trị enum không đồng nhất trong Neo4j
9. **Response Model Flexibility**: Sử dụng cách tiếp cận linh hoạt với FastAPI response_model để xử lý dữ liệu legacy

### Chi tiết cụ thể việc fix lỗi

1. **Fix lỗi __label__**: Trước đây, code sử dụng BaseNode làm target cho relationship context_node, gây lỗi vì BaseNode là abstract không có __label__. Đã fix bằng cách tạo các relationship cụ thể cho từng loại entity.

```python
# Code cũ - Gây lỗi
context_node = RelationshipTo('trm_api.graph_models.base', 'BaseNode', 'EVENT_CONTEXT')

# Code mới - Đã fix
primary_context_agent = RelationshipTo('trm_api.graph_models.agent', 'Agent', 'EVENT_CONTEXT')
primary_context_project = RelationshipTo('trm_api.graph_models.project', 'Project', 'EVENT_CONTEXT')
primary_context_task = RelationshipTo('trm_api.graph_models.task', 'Task', 'EVENT_CONTEXT')
primary_context_resource = RelationshipTo('trm_api.graph_models.resource', 'Resource', 'EVENT_CONTEXT')
```

2. **Fix lỗi datetime serialization**: Trước đây, API trả về datetime object gây lỗi 500 khi Pydantic cố gắng serialize. Đã fix bằng cách tạo adapter chuyển đổi dữ liệu:

```python
# Tạo adapter function trong endpoint
def convert_event_to_schema(event: EventGraphModel) -> EventSchema:
    return EventSchema(
        uid=event.uid,
        name=event.name,
        description=event.description,
        payload=event.payload,
        tags=event.tags,
        created_at=event.created_at.isoformat() if event.created_at else None,
        updated_at=event.updated_at.isoformat() if event.updated_at else None
    )
```

3. **Fix lỗi enum không đồng nhất trong Recognition API**: Dữ liệu trong Neo4j có nhiều dạng biểu diễn enum khác nhau (uppercase, title-case, tên đầy đủ), gây lỗi validation khi trả về qua API. Đã tạo module `enum_adapter.py` để chuẩn hóa các giá trị này sang dạng chuẩn của ontology.

4. **Xử lý linh hoạt với response_model FastAPI**: Đối với endpoint `list_recognitions`, đã bỏ response_model trong decorator để tránh validation tự động quá nghiêm ngặt. Thay vào đó, chuẩn hóa và xử lý dữ liệu thủ công trước khi trả về.

## 10. Bài học kinh nghiệm và kế hoạch tiếp theo

### Bài học từ việc xử lý Recognition API

1. **Cân bằng giữa ontology và thực tế dữ liệu legacy**:
   - Ontology định nghĩa cấu trúc lý tưởng cho dữ liệu, nhưng dữ liệu thực tế trong Neo4j có thể không hoàn toàn tương thích
   - Giải pháp: Chuẩn hóa dữ liệu thông qua các adapter layer, giữa lấy ra từ Neo4j và trước khi trả về API

2. **Xử lý enum trong Neo4j**:
   - Vấn đề: Neo4j không có kiểu dữ liệu enum nội tại, dẫn đến nhiều cách lưu trữ giá trị enum
   - Giải pháp: Sử dụng `enum_adapter.py` để đọc/ghi chuẩn hóa giá trị enum
   - Đề xuất: Viết migration script để chuẩn hóa dữ liệu trong Neo4j

3. **Không bỏ sót dữ liệu**:
   - Tiếp cận "robust by default": Trả về dữ liệu đầy đủ có thể sử dụng được dù có vài item gặp lỗi
   - Logging chi tiết: Để phát hiện và khắc phục dần các lỗi

4. **Mô hình adapter thiếu hụt cho dữ liệu**:
   - Tạo các mô-đun tiện ích (`datetime_adapter.py`, `enum_adapter.py`) để chuẩn hóa dữ liệu
   - Áp dụng nguyên tắc "Fail gracefully": Hiển thị cảnh báo thay vì crash

### Kế hoạch chi tiết tiếp theo

1. **Hoàn thiện Entity Recognition**:
   - Kiểm tra và fix tiếp các test case còn lại (create, update, delete)
   - Áp dụng chuẩn hóa enum và datetime cho tất cả endpoints
   - Bổ sung thêm các test case chi tiết

2. **Triển khai Entity WIN**:
   - Xây dựng Graph Model cho WIN theo Ontology V3.2
   - Triển khai Schema Pydantic và API endpoints 
   - Xây dựng các service layer cho WIN
   - Tạo các test case cho WIN API

3. **Triển khai các Relationship liên quan đến WIN**:
   - LEADS_TO_WIN (Agent -> WIN)
   - RECOGNIZES_WIN (Recognition -> WIN)
   - GENERATES_KNOWLEDGE (WIN -> Knowledge)
   - RESPONDS_TO (WIN -> Challenge)

4. **Cập nhật GAP Analysis**:
   - Cập nhật GAP_ANALYSIS_ONTOLOGY_V3.2.md với các phát hiện mới
   - Ghi nhận khác biệt giữa dữ liệu thực tế và ontology
   - Đề xuất giải pháp khắc phục khoảng cách này

5. **Cải thiện hệ thống adapter cho toàn dự án**:
   - Tổ chức lại các adapter vào một module thống nhất
   - Cải thiện khả năng tái sử dụng
   - Thêm phân tích hiệu suất và tối ưu hóa nếu cần

## 4. Cấu trúc thư mục và đường dẫn code

### Thư mục gốc (root)

```plaintext
e:\tech\trm-os-branches\
```

### Cấu trúc thư mục chính

- **docs/** - Tài liệu kỹ thuật và đặc tả
  - **core-specs/** - Đặc tả cốt lõi
  - **integration-specs/** - Đặc tả tích hợp
  - **technical-decisions/** - Các quyết định kỹ thuật
- **trm_api/** - Mã nguồn chính của API
  - **api/** - API endpoints và routers
    - **v1/** - API version 1
      - **endpoints/** - Các endpoint cụ thể
      - **schemas/** - Các schema Pydantic
  - **graph_models/** - Models Neo4j dựa trên ontology
  - **services/** - Lớp service xử lý logic nghiệp vụ
- **scripts/** - Các script hỗ trợ, seed dữ liệu

### Đường dẫn chính cần chú ý

1. **Graph Models** (entity và relationship) được định nghĩa tại:

   ```plaintext
   e:\tech\trm-os-branches\trm_api\graph_models\*.py
   ```

   Ví dụ: `agent.py`, `event.py`, `resource.py`, `project.py`, v.v.

2. **API Endpoints** được triển khai tại:

   ```plaintext
   e:\tech\trm-os-branches\trm_api\api\v1\endpoints\*.py
   ```

   Ví dụ: `event.py`, `agent.py`, `project.py`, v.v.

3. **API Schemas** (Pydantic models) được định nghĩa tại:

   ```plaintext
   e:\tech\trm-os-branches\trm_api\api\v1\schemas\*.py
   ```

   Ví dụ: `event.py`, `agent.py`, `project.py`, v.v.

4. **Services** (xử lý logic nghiệp vụ) được triển khai tại:

   ```plaintext
   e:\tech\trm-os-branches\trm_api\services\*.py
   ```

   Ví dụ: `event_service.py`, `agent_service.py`, v.v.

5. **Scripts** (seed dữ liệu, test) được lưu tại:

   ```plaintext
   e:\tech\trm-os-branches\scripts\*.py
   ```

   Ví dụ: `seed_agent_data.py`, `seed_event_data.py`, v.v.

## 5. Bài học kinh nghiệm (Lessons Learned)

### Từ các fix lỗi Event API

1. **Xử lý DateTime trong Neo4j**
   - Luôn sử dụng custom `Neo4jDateTimeProperty` thay cho `DateTimeProperty` của neomodel
   - Đảm bảo signature `inflate()` của Neo4jDateTimeProperty nhận đủ các tham số mà framework truyền vào
   - Code tham khảo trong `trm_api/graph_models/base.py`

2. **Serialize/Deserialize datetime**
   - Thêm adapter function trong endpoint để chuyển đổi các trường datetime sang string ISO format
   - Đảm bảo schema Pydantic định nghĩa các trường datetime dạng string
   - Code tham khảo trong `trm_api/api/v1/endpoints/event.py`

3. **Định nghĩa Relationship**
   - Không sử dụng relationship trừ u tượng cho các node khác loại
   - Sử dụng relationship cụ thể cho từng loại node (ví dụ `AGENT_CONTEXT`, `PROJECT_CONTEXT`)
   - Cân nhắc kiểm tra kỹ RelationshipTo/From, đảm bảo truyền đúng kiểu (class hoặc string tên class)

4. **Xử lý Array/JSON**
   - Sử dụng `ArrayProperty(StringProperty())` thay vì `JSONProperty` cho các trường mang tính array đơn giản
   - Đảm bảo dữ liệu trong Neo4j đúng kiểu với property định nghĩa trong model

### Từ việc fix Integration Tests

1. **Nhất quán tên API giữa các lớp**
   - Đảm bảo tên phương thức trong endpoint gọi đúng tên phương thức trong service
   - Ví dụ: `create_knowledge_snippet()` trong controller phải gọi `create_snippet()` trong service
   - Tuân thủ nguyên tắc đặt tên trong cả dự án, dễ dàng debug và maintain

2. **Xử lý cẩn thận các trả về từ API**
   - Không nên giả định tên trường trong response (`id` vs `recognitionId`)
   - Test API phải kiểm tra chính xác schema trả về khớp với schema Expected
   - Khi gặp KeyError, kiểm tra response.json() để xem tên field chính xác

3. **Neo4j DateTime và Pydantic DateTime**
   - Neo4j DateTime (neo4j.time.DateTime) không tương thích trực tiếp với Pydantic datetime
   - Luôn chuyển đổi qua `.isoformat()` hoặc chuỗi ISO trước khi đưa vào Pydantic model
   - Triển khai adapter giữa các lớp model (Neo4j->Service->API) để serialize đúng kiểu dữ liệu

4. **Xử lý enum cho các field**
   - Đảm bảo giá trị truyền vào API route khớp chính xác với định nghĩa enum (phân biệt hoa/thường)
   - Ví dụ: `source_type="User"` thay vì `source_type="USER"`
   - Mặc định dùng Title Case cho enum hiển thị và lowercase cho key lưu trữ

### Lưu ý cho các phần tiếp theo

1. **Triển khai Recognition API**
   - Tuân thủ các checklist trong GAP Analysis
   - Áp dụng các lesson learned về datetime và relationship
   - Đảm bảo tương thích với các entity đã triển khai

2. **Triển khai WIN API**
   - Tuân thủ các checklist trong GAP Analysis
   - Đặc biệt chú ý các relationship quan trọng: LEADS_TO_WIN, GENERATES_KNOWLEDGE

3. **Triển khai KnowledgeSnippet**
   - Cần làm rõ mối quan hệ với KnowledgeResource trước khi triển khai
   - Tích hợp chặt chẽ với WIN thông qua GENERATES_KNOWLEDGE

### Kiểm soát chất lượng (QA)

1. **Kiểm thử unit test cho từng entity**
   - Mỗi entity cần test CRUD đầy đủ
   - Các validation logic cần được test kỹ

2. **Kiểm thử relationship**
   - Test việc tạo và query các relationship
   - Đảm bảo các relationship hoạt động đúng theo ontology

3. **Seed dữ liệu mẫu**
   - Luôn seed dữ liệu mẫu sau khi triển khai entity mới
   - Kiểm tra tính chất graph traversal của Neo4j qua relationship

## 6. Tiến độ và vấn đề phát hiện gần đây

### Ngày cập nhật: 19/06/2025

**Vấn đề mới phát hiện cần khắc phục gấp:**

Đã phát hiện lỗi khi chạy unit tests:

```
NameError: name 'adapt_datetime_response' is not defined
trm_api\api\v1\endpoints\task.py:111: in <module>
    @adapt_datetime_response
```

Lỗi này xảy ra do decorator `adapt_datetime_response` được sử dụng trong file `task.py` nhưng không được định nghĩa hoặc import đúng cách. Đây là kết quả của quá trình chuẩn hóa adapter pattern có thể đã thay đổi tên các decorator. Cần kiểm tra module `decorators.py` và điều chỉnh import cho đúng.

### Mục tiêu tiếp theo

1. **Khắc phục lỗi decorator trong endpoints**:
   - Sửa lỗi `adapt_datetime_response` trong `task.py`
   - Kiểm tra các endpoints khác có vấn đề tương tự
   - Đảm bảo tất cả endpoint sử dụng các decorator đã chuẩn hóa mới

2. **Hoàn thiện Data Adapter Pattern**:
   - Đảm bảo áp dụng decorator đúng cho mọi endpoint (Task, Project, Recognition, Win, KnowledgeSnippet)
   - Kiểm tra lại decorator `adapt_task_response`, `adapt_knowledge_snippet_response`, `adapt_ontology_response`
   - Cập nhật tài liệu về các adapter đã triển khai

3. **Cập nhật và kiểm tra CI/CD pipeline**:
   - Kiếm thử lại toàn bộ unit tests và integration tests sau khi sửa lỗi
   - Đảm bảo workflow CI hỗ trợ đầy đủ các dependency cho tests async
   - Đánh giá hiệu suất API sau khi chuyển đổi sang async pattern

## 5. Lưu ý quan trọng

- **Nghiêm cấm mock/demo/fake**: Tất cả triển khai phải thực sự hoạt động
- **Nghiêm cấm hardcode**: Phải thực sự liên thông giữa các service
- **Giữ nguyên mục đích**: Không đơn giản hóa mà phải đảm bảo sản phẩm hoàn chỉnh, chính xác
- **Luôn cập nhật GAP Analysis**: Mỗi khi hoàn thành một đoạn dài các việc
- **Chiến lược ontology-first**: Tuân thủ chặt chẽ định nghĩa trong Hiến pháp ontology V3.2

## 6. Tài liệu tham khảo

- [Graph Models](e:\tech\trm-os-branches\trm_api\graph_models\) - Các định nghĩa model cho Neo4j
- [API Endpoints](e:\tech\trm-os-branches\trm_api\api\v1\endpoints\) - Các API endpoint đã triển khai
- [Services](e:\tech\trm-os-branches\trm_api\services\) - Các service xử lý logic nghiệp vụ
- [Schemas](e:\tech\trm-os-branches\trm_api\schemas\) - Các schema Pydantic cho API
