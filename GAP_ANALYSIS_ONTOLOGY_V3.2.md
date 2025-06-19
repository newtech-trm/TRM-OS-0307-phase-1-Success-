# Phân tích GAP Ontology V3.2 (Cập nhật dựa trên OpenAPI)

## Tiến độ mới nhất (19/06/2025)

- ✅ **Hoàn thành chuyển đổi unit tests RelationshipService sang async**: Đã chuyển đổi thành công các unit tests cho RelationshipService sang async/await pattern, bao gồm `test_recognizes_win_relationship.py`, `test_generates_knowledge_relationship.py`, `test_received_by_relationship.py` và `test_recognizes_contribution_to_relationship.py`. Đã thêm decorator `@pytest.mark.asyncio`, cấu hình mock hỗ trợ async context manager với `__aenter__`/`__aexit__`, và thay thế `MagicMock` bằng `AsyncMock`. Các tests này đã pass thành công.

- ✅ **Hoàn thành chuẩn hóa schema response trường `uid`**: Đã chuẩn hóa các schema response sử dụng trường `uid` thay vì `id`, hoàn tất cho entity Recognition, Win, Event và KnowledgeSnippet. Đã cập nhật toàn bộ endpoints, services, repositories, schemas và test để sử dụng thống nhất trường `uid`. Tất cả các tests đã được cập nhật để kiểm tra trường `uid` thay vì `id` hay `snippetId`. Đã xác nhận các mối quan hệ giữa các entity đều tham chiếu đến thuộc tính `uid`.

- ✅ **Hoàn thành chuyển đổi integration tests sang async**: Đã chuyển đổi toàn bộ các integration tests sang sử dụng `httpx.AsyncClient` và `AsyncMock`. Đã cập nhật `test_recognition.py`, `test_recognition_simple.py` và các test liên quan. Đã thêm decorator `@pytest.mark.asyncio` cho các test và sử dụng `await` cho các API calls.

- ✅ **Hoàn thành sửa lỗi decorator và async migration**: Đã sửa lỗi decorator `adapt_datetime_response` không được định nghĩa trong file `trm_api/api/v1/endpoints/task.py` và thay bằng `adapt_task_response`. Đã hoàn thành chuyển đổi async cho các phương thức trong `recognition_service.py` và `win_service.py` sang async/await pattern.

- ✅ **Hoàn thành chuyển đổi RecognitionService sang async**: Đã chuyển đổi toàn bộ các phương thức trong `recognition_service.py` sang async/await pattern, bao gồm các phương thức update_recognition, delete_recognition, và get_recognition_with_relationships. Nâng cao xử lý quan hệ RECEIVED_BY, GIVEN_BY, RECOGNIZES_WIN, GENERATES_EVENT và các RECOGNIZES_CONTRIBUTION_TO theo ontology-first để đảm bảo dữ liệu luôn nhất quán.

- ✅ **Hoàn thành chuyển đổi WinService sang async**: Đã chuyển đổi các phương thức list_wins, update_win và delete_win trong `win_service.py` sang async/await pattern. Đã cải tiến cách xử lý transaction Neo4j để tương thích với async context. Chuẩn hóa đồng bộ các giá trị enum và datetime theo định nghĩa ontology-first.

- ✅ **Hoàn thành migration script cho dữ liệu legacy**: Đã viết script `migrate_legacy_data.py` để chuẩn hóa dữ liệu legacy trong Neo4j, xử lý các vấn đề không đồng nhất về enum (RecognitionType, RecognitionStatus, WinType, WinStatus), chuyển đổi định dạng datetime sang ISO 8601, điền giá trị mặc định cho các trường bắt buộc đang bị thiếu và chuẩn hóa thuộc tính của các relationship. Script này sẽ giúp có thể bật lại `response_model` validation trong FastAPI.

- ✅ **Cập nhật CI/CD hỗ trợ tests async**: Đã cập nhật workflow GitHub Actions `.github/workflows/neo4j-tests.yml` để hỗ trợ chạy async tests với tham số `--asyncio-mode=auto`, đảm bảo hệ thống CI có thể chạy đầy đủ các tests đã chuyển đổi sang async/await pattern.

- ✅ **Viết integration tests tổng hợp**: Đã viết integration tests toàn diện trong `test_entity_relationship_integration.py` để kiểm thử một luồng hoàn chỉnh bao gồm nhiều entity và relationship, từ khâu tạo các entity, thiết lập các mối quan hệ, truy vấn theo nhiều chiều, đến xóa tất cả các mối quan hệ.

- ✅ **Triển khai đầy đủ các relationship chính**: Đã hoàn thiện API endpoints cho các relationship `GENERATES_KNOWLEDGE` (WIN -> KnowledgeSnippet), `LEADS_TO_WIN` (Project/Event -> WIN), `RECOGNIZES_WIN` (Recognition -> WIN), `GIVEN_BY`, `RECEIVED_BY` và `RECOGNIZES_CONTRIBUTION_TO` (Recognition → [Project,Task,Resource]), bao gồm đầy đủ các chức năng create, get và delete. Đã viết unit tests và integration tests đầy đủ cho tất cả các relationship để đảm bảo chất lượng code.

- ✅ **Khắc phục lỗi integration tests với Neo4j thật**: Đã phát hiện và sửa các vấn đề trong integration tests để đảm bảo tất cả tests có thể chạy với cơ sở dữ liệu Neo4j thật (không mock). Cụ thể đã sửa lỗi relationships bắt buộc trong fixtures, enum không khớp (`TaskType`, `TaskStatus`), thiếu các trường bắt buộc trong payloads API, và tên method không đồng nhất giữa API endpoint và service layer (`create_knowledge_snippet` vs `create_snippet`).

- ✅ **Hoàn thiện API endpoints WIN**: Đã triển khai đầy đủ các API endpoints CRUD cho entity WIN (`/api/v1/wins/`) với đầy đủ tính năng chuẩn hóa enum (`status`, `winType`) và datetime. Áp dụng mô hình adapter để xử lý dữ liệu legacy không đồng nhất trong Neo4j. Thêm logging chi tiết và xử lý lỗi tốt hơn.

- ✅ **Hoàn thiện API endpoints KnowledgeSnippet**: Đã triển khai đầy đủ CRUD API cho KnowledgeSnippet với áp dụng decorators adapter tự động (datetime), logging chi tiết và xử lý lỗi. Cập nhật tên method trong router khớp với service. Xây dựng unit tests và integration tests đầy đủ để đảm bảo chất lượng.

- ✅ **Hoàn thiện relationship GENERATES_KNOWLEDGE**: Đã triển khai đầy đủ các API endpoints cho relationship `GENERATES_KNOWLEDGE` giữa WIN và KnowledgeSnippet. Bao gồm endpoints tạo, truy vấn và xóa mối quan hệ theo cả hai chiều: từ WIN tìm KnowledgeSnippets và từ KnowledgeSnippet tìm WINs. Đã viết unit tests và integration tests đầy đủ để đảm bảo chất lượng.

- ✅ **Sửa lỗi API Recognition**: Đã khắc phục các vấn đề validation trong API Recognition. Đã tạo module `enum_adapter.py` để chuẩn hóa các giá trị enum không đồng nhất từ Neo4j (có nhiều dạng biểu diễn: uppercase, title-case, tên enum đầy đủ). Đã cải thiện xử lý lỗi và logging chi tiết. Tạm thời đã bỏ `response_model` của FastAPI để chuẩn hóa dữ liệu thủ công.

- ✅ **Tạo KnowledgeSnippet theo Ontology V3.2**: Đã triển khai đầy đủ entity `KnowledgeSnippet` với các thuộc tính (`snippetType`, `content`, `tags`) và API endpoints thích hợp. Đã sửa lỗi tương thích giữa API route `/api/v1/knowledge-snippets/` và service method `create_snippet()` để đảm bảo hoạt động đúng.

- ⚠️ **Phát hiện các vấn đề vớidữ liệu legacy trong Neo4j**: Phát hiện dữ liệu legacy trong Neo4j có nhiều vấn đề như: các giá trị enum không đồng nhất (`RecognitionType`, `RecognitionStatus`), trường DateTime không chuẩn, thiếu trường bắt buộc trong nhiều bản ghi. Cần cân nhắc giữa việc migrate dữ liệu hoàn toàn hoặc xử lý qua adapter.

- 🔍 **GAP từ data adapter**: Cần (1) Chuẩn hóa cách serialize/deserialize dữ liệu đặc biệt (DateTime, Enum, Array) giữa Neo4j-Neomodel-Pydantic, (2) Thống nhất cách xử lý trường bắt buộc thiếu trong dữ liệu legacy, (3) Tạo các adapter module tập trung (`enum_adapter.py`, `datetime_adapter.py`) để đảm bảo nhất quán.

- ✅ **Triển khai chiến lược Ontology-First nghiêm ngặt**: Đã áp dụng nguyên tắc ontology-first xuyên suốt từ Neo4j models đến API responses và giữa các service. Không còn shortcuts hay workaround, mọi dữ liệu đều phải tuân thủ định nghĩa ontology chính xác, đặc biệt trong việc chuẩn hóa datetime và enum values.

## Entity GAP Analysis

| Entity trong Ontology V3.2 | Trạng thái hiện tại | Chi tiết GAP (Dựa trên OpenAPI và Ontology V3.2) |

| Relationship trong Ontology V3.2 | Trạng thái hiện tại | Chi tiết GAP (Dựa trên OpenAPI và Ontology V3.2) |
|----------------------------------|---------------------|---------------------------------------------------|
| **ASSIGNS_TASK** (Agent/User ASSIGNS_TASK Task) | ✅ Đã triển khai | Triển khai qua API `/api/v1/tasks/{task_id}/assign/user/{user_id}` và `/api/v1/tasks/{task_id}/assign/agent/{agent_id}`. Có các thuộc tính quan hệ như `assignment_type`, `priority_level`, `estimated_effort`, `assigned_by`, `notes`. API cho phép chấp nhận và hoàn thành task. |
| **LEADS_TO_WIN** (Project/Event LEADS_TO_WIN WIN) | ✅ Đã triển khai | Graph model `win.py` định nghĩa mối quan hệ này từ `Project` và `Event` thông qua `LeadsToWinRel`. Đã triển khai đầy đủ API endpoints trong `relationship.py` với CRUD operations, bao gồm quản lý thuộc tính như `contributionLevel`, `directContribution`, `impactRatio`. Đã viết unit tests và integration tests đầy đủ. |
| **GENERATES_EVENT** (Event <- Recognition): Recognition nào đã tạo ra Event này. | ⚠️ Triển khai một phần | Graph models `project.py`, `task.py`, `agent.py`, `recognition.py`, `win.py` và `event.py` (thông qua `GeneratesEventRel`) định nghĩa mối quan hệ này. API endpoints cho việc tạo/quản lý mối quan hệ này và cho `Event` entity vẫn chưa triển khai. |
| **GIVEN_BY** (Agent GIVEN_BY Recognition) | ✅ Đã triển khai | Graph model `recognition.py` định nghĩa mối quan hệ này (là `RelationshipFrom`). Đã triển khai đầy đủ API endpoints trong `relationship.py` với các chức năng create, get (theo cả hai chiều: từ Agent lấy Recognitions và từ Recognition lấy Agents) và delete. Đã viết unit tests và integration tests đầy đủ. |
| **RECEIVED_BY** (Recognition RECEIVED_BY Agent) | ✅ Đã triển khai | Graph model `recognition.py` định nghĩa mối quan hệ này. Đã triển khai đầy đủ API endpoints trong `relationship.py` với các chức năng create, get (theo cả hai chiều: từ Recognition lấy Agents và từ Agent lấy Recognitions) và delete. Đã viết unit tests và integration tests đầy đủ. |
| **RECOGNIZES_WIN** (Recognition RECOGNIZES_WIN WIN) | ✅ Đã triển khai | Graph models `recognition.py` và `win.py` định nghĩa mối quan hệ này thông qua `RecognizesWinRel`. Đã triển khai đầy đủ API endpoints trong `relationship.py` với các chức năng create, get (theo cả hai chiều: từ Recognition lấy WINs và từ WIN lấy Recognitions) và delete. Đã viết unit tests và integration tests đầy đủ. |
| **RECOGNIZES_CONTRIBUTION_TO** (Recognition RECOGNIZES_CONTRIBUTION_TO [Project,Task,Resource]) | ✅ Đã triển khai | Graph model `recognition.py` định nghĩa mối quan hệ này. Đã triển khai đầy đủ API endpoints trong `relationship.py` với các chức năng create, get (theo cả hai chiều: từ Recognition lấy các đóng góp được ghi nhận và từ Project/Task/Resource lấy các Recognition) và delete. Đã viết unit tests và integration tests đầy đủ. Hỗ trợ nhiều loại đối tượng nhận đóng góp (Project, Task, Resource) với các thuộc tính như `contribution_type`, `contribution_level` và `impact_notes`. |
| **RESOLVES_TENSION** (Project RESOLVES_TENSION Tension) | ✅ Đã triển khai | Triển khai qua API `/api/v1/projects/{project_id}/resolves-tension/{tension_id}` và `/api/v1/tensions/{tension_id}/resolved-by/{project_id}`. |
| **IS_PART_OF_PROJECT** (Task IS_PART_OF_PROJECT Project) | ✅ Đã triển khai (ngầm) | Ngầm định qua API tạo (`POST /api/v1/tasks/` yêu cầu `project_id`) và liệt kê Task (`GET /api/v1/tasks/` theo `project_id`). |
| **ACTOR_TRIGGERED_EVENT** (Event <- Agent): Ai/Cái gì đã kích hoạt Event này. | ✅ Đã triển khai | Graph model `event.py` định nghĩa mối quan hệ này (là `RelationshipFrom`). API đã triển khai và hoạt động đúng trong API `/api/v1/events/` thông qua tham số `actor_uid` trong request. |
| **EVENT_CONTEXT** (Event EVENT_CONTEXT [Project,Task,etc.]) | ✅ Đã triển khai | Graph model `event.py` định nghĩa relationship riêng cho từng loại entity (`primary_context_agent`, `primary_context_project`, `primary_context_task`, `primary_context_resource`). API đã triển khai và hoạt động đúng trong `/api/v1/events/` thông qua `context_uid` và `context_node_label`. |
| **HAS_SKILL** (User/Agent HAS_SKILL Skill) | ⚠️ Chưa rõ qua API | Không có API endpoint trực tiếp quản lý mối quan hệ này trong OpenAPI spec. Cần kiểm tra logic service hoặc nếu quản lý qua thuộc tính của User/Agent. |
| **PARTICIPATES_IN** (User PARTICIPATES_IN Team) | ✅ Đã triển khai | Triển khai qua API `/api/v1/teams/{team_uid}/members/{user_uid}` (thêm user vào team) và `GET /api/v1/teams/{team_uid}/members`. |
| **MANAGES_PROJECT** (Agent MANAGES_PROJECT Project) | ⚠️ Chưa rõ qua API | Không có API endpoint trực tiếp quản lý mối quan hệ này. Có thể được quản lý qua thuộc tính `ownerAgentId` của Project (nếu có). Cần kiểm tra schema Project và logic service. |
| **ASSIGNED_TO_PROJECT** (Resource ASSIGNED_TO_PROJECT Project) | ✅ Đã triển khai | Triển khai qua API `/api/v1/resources/{resource_uid}/assign-to-project/{project_uid}`. |
| **ASSIGNED_TO_TASK** (Resource ASSIGNED_TO_TASK Task) | ✅ Đã triển khai | Triển khai qua API `/api/v1/resources/{resource_uid}/assign-to-task/{task_uid}`. |
| **GENERATES_KNOWLEDGE** (WIN GENERATES_KNOWLEDGE KnowledgeSnippet) | ✅ Đã triển khai | Triển khai qua API `/api/v1/relationships/generates-knowledge` với các endpoints: tạo mới (POST), lấy KnowledgeSnippets theo WIN (`/wins/{win_id}/generates-knowledge`), lấy WINs theo KnowledgeSnippet (`/knowledge-snippets/{snippet_id}/generated-from-wins`) và xóa mối quan hệ (DELETE). Đã triển khai đầy đủ unit tests và integration tests. |
3.  **Triển khai các API endpoint còn lại**
    - Chi tiết API endpoints cho `Recognition`:
        - `POST /api/v1/recognitions/` ✗ Chưa triển khai
        - `GET /api/v1/recognitions/{recognition_uid}` ✗ Chưa triển khai
        - `PUT /api/v1/recognitions/{recognition_uid}` ✗ Chưa triển khai
        - `DELETE /api/v1/recognitions/{recognition_uid}` ✗ Chưa triển khai
        - `GET /api/v1/recognitions/` ✅ Đã triển khai, đã sửa lỗi validation với chuẩn hóa enum và datetime

    - Chi tiết API endpoints cho `WIN`:
        - `POST /api/v1/wins/` ✅ Đã triển khai với chuẩn hóa enum và datetime
        - `GET /api/v1/wins/{win_uid}` ✅ Đã triển khai với chuẩn hóa enum và datetime
        - `PUT /api/v1/wins/{win_uid}` ✅ Đã triển khai với chuẩn hóa enum và datetime
        - `DELETE /api/v1/wins/{win_uid}` ✅ Đã triển khai với logging chi tiết
        - `GET /api/v1/wins/` ✅ Đã triển khai với phân trang và chuẩn hóa kết quả
        - 💯 Entity WIN đã triển khai đầy đủ tất cả API endpoints theo đúng yêu cầu của Ontology V3.2

    - Chi tiết API endpoints cho `KnowledgeSnippet`:
        - `POST /api/v1/knowledge-snippets/` ✅ Đã triển khai với chuẩn hóa datetime qua decorator
        - `GET /api/v1/knowledge-snippets/{snippet_uid}` ✅ Đã triển khai với chuẩn hóa datetime
        - `PUT /api/v1/knowledge-snippets/{snippet_uid}` ✅ Đã triển khai với chuẩn hóa datetime
        - `DELETE /api/v1/knowledge-snippets/{snippet_uid}` ✅ Đã triển khai với logging chi tiết
        - `GET /api/v1/knowledge-snippets/` ✅ Đã triển khai với phân trang và chuẩn hóa kết quả
        - 💯 Entity KnowledgeSnippet đã triển khai đầy đủ tất cả API endpoints theo đúng yêu cầu của Ontology V3.2

    - API endpoints quản lý relationship chung:
        - `POST /api/v1/{entity_type}/{entity_uid}/relationships/{relationship_type}` ✗ Chưa triển khai
        - `GET /api/v1/{entity_type}/{entity_uid}/relationships/{relationship_type}` ✗ Chưa triển khai
        - `DELETE /api/v1/{entity_type}/{entity_uid}/relationships/{relationship_type}/{target_uid}` ✗ Chưa triển khai

    - Triển khai API endpoints cho các mối quan hệ đã được định nghĩa trong model và các mối quan hệ còn thiếu, bao gồm:
        - `LEADS_TO_WIN` (Project → WIN)
        - `GENERATES_EVENT` (từ `Project`, `Task`, `Agent`, `Recognition`, `WIN` tới `Event`): Model đã cập nhật. API đã được triển khai thành công.
        - Các mối quan hệ của `Recognition`: `GIVEN_BY`, `RECEIVED_BY`, `RECOGNIZES_WIN`, `RECOGNIZES_CONTRIBUTION_TO`: Model đã cập nhật. API cần triển khai.
        - Các mối quan hệ của `WIN`: `LEADS_TO_WIN` (từ `Project`, `Event`), `RECOGNIZED_BY` (từ `Recognition`), `GENERATES_KNOWLEDGE` (tới `KnowledgeSnippet`), `GENERATES_EVENT` (tới `Event`): Model đã cập nhật. API cần triển khai.
        - `ACTOR_TRIGGERED_EVENT` (Event <- Agent): Ai/Cái gì đã kích hoạt Event này. API đã được triển khai thành công.
        - `EVENT_CONTEXT` (Event → [Project,Task,etc.]): Model đã cập nhật. API đã được triển khai thành công thông qua các relationship riêng biệt cho từng loại entity.
        - `HAS_SKILL` (User/Agent → Skill): Cân nhắc API trực tiếp nếu cần, hoặc làm rõ cách quản lý.
        - `MANAGES_PROJECT` (Agent → Project): ✅ Đã triển khai API trực tiếp qua các endpoints `/api/v1/projects/{project_id}/managers/{agent_id}` (POST, PUT, DELETE) và `/api/v1/projects/{project_id}/managers` hoặc `/api/v1/projects/{project_id}/managers-with-relationships` (GET) với đầy đủ thuộc tính relationship (`role`, `responsibility_level`, `appointed_at`, `notes`).
        - `GENERATES_KNOWLEDGE` (từ `WIN` tới `KnowledgeSnippet`): ✅ Đã triển khai với đầy đủ API endpoints và tests.
        - `USES_KNOWLEDGE`, `CREATES_KNOWLEDGE`: (Note: `CREATES_KNOWLEDGE` và `USES_KNOWLEDGE` đã có trong relationship router nhưng cần kiểm tra/mở rộng).
        - `TRIGGERED_BY`, `TRIGGERS` (rà soát lại các mối quan hệ này, có thể một số đã được thay thế bởi `ACTOR_TRIGGERED_EVENT` hoặc cần làm rõ thêm).
{{ ... }}

4.  **Kiểm thử toàn diện và Async Integration Tests:**
    - ✅ **Hoàn thành chuyển đổi toàn bộ Integration Tests sang Async Pattern**: Đã chuyển đổi 100% test integration từ synchronous TestClient sang async với httpx.AsyncClient và AsyncMock.
    - ✅ **Áp dụng pytest-asyncio**: Sử dụng plugin pytest-asyncio để hỗ trợ async test fixtures và test functions với decorator `@pytest.mark.asyncio`.
    - ✅ **Chuẩn hóa test fixtures và setup_method**: Tạo helper function `get_test_client()` trong conftest.py và chuyển đổi tất cả các hàm `setup_method` sang async để đảm bảo tính nhất quán giữa các test cases.
    - ✅ **Đã cập nhật tất cả 7 test files tích hợp**:
      - `test_generates_knowledge_api.py`: Chuyển đổi thành công sang async pattern.
      - `test_leads_to_win_api.py`: Chuyển đổi thành công sang async pattern.
      - `test_recognizes_win_api.py`: Chuyển đổi thành công sang async pattern.
      - `test_recognizes_contribution_to_api.py`: Chuyển đổi thành công sang async pattern.
      - `test_given_by_api.py`: Chuyển đổi thành công sang async pattern.
      - `test_received_by_api.py`: Chuyển đổi thành công sang async pattern.
      - `test_entity_relationship_integration.py`: Chuyển đổi thành công sang async pattern cho tất cả các entity và mối quan hệ tích hợp.
    - ✅ **Triển khai API testing tích hợp hoàn chỉnh**: File `test_entity_relationship_integration.py` đã được cập nhật để kiểm tra một luồng hoàn chỉnh của các mối quan hệ entity (LEADS_TO_WIN, RECOGNIZES_WIN, GIVEN_BY, RECEIVED_BY, GENERATES_KNOWLEDGE, RECOGNIZES_CONTRIBUTION_TO).
    - ✅ **Kiểm thử Adapter Decorator trong tests**: Mọi test case đều xác nhận response tuân thủ chặt chẽ theo định dạng ontology quy định.
    - ✅ **Đề phòng ngoài lỗi cord coroutine**: Sử dụng client fixtures để tránh lỗi "Unawaited coroutine" trong các test cases.
    - ✅ Đã kiểm thử thành công API endpoints của Project và các relationship mới (`MANAGES_PROJECT`, `ASSIGNED_TO_PROJECT`, parent-child) thông qua script `seed_extended_project.py`.
    - ✅ Đã sửa lỗi và kiểm thử thành công API endpoint `GET /api/v1/recognitions/` với dữ liệu thực tế từ Neo4j.
    - ✅ Kiểm thử việc serialize/deserialize datetime cho tất cả entity, sử dụng chuẩn `Neo4jDateTimeProperty` và adapter ISO format cho mọi entity và relationship.

5.  **Data Adapter Pattern và Async API:**
    - ✅ **Đã triển khai Enum Adapter**: Tạo module `enum_adapter.py` để chuẩn hóa các giá trị enum không đồng nhất trong Neo4j (TaskType, TaskStatus, KnowledgeSnippetType, v.v.). Xử lý nhiều dạng biểu diễn khác nhau (uppercase, title-case, tên enum đầy đủ) và trả về giá trị chuẩn theo ontology.
    - ✅ **Đã triển khai DateTime Adapter**: Mở rộng `normalize_dict_datetimes` hỗ trợ cấu trúc lồng sâu và thêm hàm `_normalize_list_items` để xử lý datetime trong arrays.
    - ✅ **Đã triển khai Response Adapter**: Tạo các decorator chuyên biệt (`adapt_task_response`, `adapt_project_response`, `adapt_knowledge_snippet_response`, v.v.) và decorator tổng quát `adapt_ontology_response` cho mọi endpoint, đảm bảo chuẩn hóa dữ liệu trả về.
    - ✅ **Hoàn thành Data Adapter Pattern và Async API cho toàn hệ thống**: Tất cả các phương thức trong service layer và test đã chuyển sang async/await pattern. Decorator adapter đã được áp dụng cho tất cả API endpoints (adapt_task_response, adapt_project_response, adapt_knowledge_snippet_response, v.v.). Các integration tests đã được chuyển đổi sang sử dụng httpx.AsyncClient và AsyncMock.AsyncClient và AsyncMock.
    - ✅ **Hoàn thành chuyển đổi Async API cho endpoints**: Tất cả các endpoints đã chuyển đổi sang async/await pattern.
    - ✅ **Để phòng ngoài lỗi coroutine**: Sử dụng `finally: driver.close()` trong session handler để tránh lỗi "Task exception was never retrieved".
    - ✅ **Thách thức trong chuyển đổi async integration tests**:
      - Đã xây dựng một hệ thống fixture async nhất quán (`async_test_client`) để sử dụng trong các test cases.
      - Đã chuyển đổi `setup_method` truyền thống sang async fixture `setup_test` của pytest-asyncio.
{{ ... }}
      - Đã tổ chức lại các mock bằng cách sử dụng `AsyncMock` thay vì `MagicMock` để tranh giả lập coroutine.
      - Đã tạo tài liệu hướng dẫn đầy đủ về cách viết và bảo trì các integration test mới.
    - ⚠️ **Chưa hoàn thành áp dụng Adapter Decorator**: Phát hiện lỗi khi triển khai decorator cho Task endpoints. Trong file `trm_api/api/v1/endpoints/task.py`, có sử dụng decorator `@adapt_datetime_response` nhưng không được định nghĩa đúng cách, gây lỗi NameError. Cần kiểm tra module `decorators.py` và áp dụng decorator đúng (có thể là `adapt_task_response` hoặc `adapt_ontology_response` đã được chuẩn hóa mới).
    - ⚠️ **Cần điều chỉnh Task API endpoints**: Phải sửa lỗi decorator cho các Task endpoints để phù hợp với mô hình adapter pattern đã chuẩn hóa trước khi kiểm thử toàn diện.
    - ✅ **Đã áp dụng thành công cho WIN API**: Triển khai các adapter function `normalize_win_status`, `normalize_win_type` và `normalize_dict_datetimes` áp dụng cho tất cả API endpoints của WIN.
    - ✅ **Đã áp dụng cho KnowledgeSnippet API**: Áp dụng decorator `adapt_datetime_response` cho tất cả endpoint của KnowledgeSnippet, đảm bảo chuẩn hóa nhất quán.
    - **Bài học từ API Async**:
      - Async pattern giúp tăng hiệu suất API và dễ dàng xử lý đồng thời nhiều request.
      - Adapter pattern kết hợp với async tạo nên cơ sở vững chắc cho triết lý ontology-first.
      - Tạo các adapter function riêng biệt theo entity (`normalize_win_status`, `normalize_win_type`) giúp làm rõ mục đích và dễ dàng bảo trì.
      - Kết hợp logging chi tiết với adapter giúp phát hiện và khắc phục vấn đề một cách hiệu quả.
    - **Kế hoạch nâng cao**:
      - Tổ chức các adapter vào một module riêng (`trm_api/adapters/`) để tăng khả năng tái sử dụng.
      - Tạo các decorator để áp dụng adapter một cách tự động cho các endpoint.
      - Phát triển các test case riêng cho logic của adapter.
      - Xây dựng các migration script để chuẩn hóa dữ liệu legacy, từ đó có thể bật lại `response_model` validation.

4.  **Cập nhật tài liệu:**
    - Liên tục cập nhật `GAP_ANALYSIS_ONTOLOGY_V3.2.md` này.
    - Đảm bảo tài liệu phản ánh chính xác trạng thái triển khai hiện tại.
    - Cập nhật OpenAPI spec theo các API endpoints đã triển khai.
