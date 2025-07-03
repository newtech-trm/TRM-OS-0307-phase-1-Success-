# Học Thuyết Thống Nhất TRM-OS - Tập 8: Lộ trình Nâng cấp API (v1 -> v2)

**Phiên bản:** 1.0
**Trạng thái:** Bản nháp đầu tiên
**Người biên soạn:** Gemini-Pro Agent & Human Co-founder

---

## **1. Mục đích**

Tài liệu này không thay thế tài liệu API chi tiết (OpenAPI spec), mà đóng vai trò là một **kim chỉ nam chiến lược** cho việc phát triển API của TRM-OS. Nó trả lời câu hỏi: "Làm thế nào để các endpoint của chúng ta phản ánh được triết lý và học thuyết cốt lõi, thay vì chỉ là các CRUD endpoint thông thường?"

Mục tiêu là đảm bảo API phiên bản v2 sẽ:
*   **Tương thích với Học thuyết:** Các model và endpoint phải "nói" bằng ngôn ngữ của các thực thể đã được định nghĩa trong Tập 2 (v4.1).
*   **Thông minh hơn:** API không chỉ lưu trữ và truy xuất dữ liệu, mà còn phải có khả năng tính toán các thuộc tính mang tính triết lý (ví dụ: `resonance_score`).
*   **Hướng hành động:** Các endpoint phải được thiết kế để phục vụ cho các vòng lặp vận hành của `AI Agentic`.

---

## **2. Phân tích Lỗ hổng API v1 (Dựa trên `allendpoint.txt`)**

API v1, được thiết kế cho Ontology v3.2, là một nền tảng tốt nhưng có những lỗ hổng triết lý quan trọng khi so sánh với Học thuyết v4.x.

| Endpoint API v1 | Dữ liệu & Logic Hiện tại | Lỗ hổng Triết lý (so với Học thuyết v4.x) |
| :--- | :--- | :--- |
| **`POST /api/v1/events/`** | Tạo `Event` với `name`, `payload`. | **Thiếu ngữ cảnh Cộng hưởng:** Event chỉ là một bản ghi. API không có cách nào để ghi nhận `signal_strength`, `information_energy`, hay nguồn gốc có thẩm quyền. Nó chỉ ghi nhận "cái gì xảy ra" chứ không phải "tín hiệu này mạnh yếu ra sao". |
| **`POST /api/v1/projects/`** | Tạo `Project` với `title`, `description`. | **Nguồn gốc bị cắt đứt:** Không có trường bắt buộc nào để liên kết `Project` với `Tension` mà nó được sinh ra để giải quyết. Điều này biến `Project` thành một thực thể mồ côi, vi phạm nguyên tắc "Biểu hiện có Chủ đích". |
| **`GET /api/v1/projects/{id}`** | Trả về thông tin cơ bản của Project. | **Thiếu đo lường hiệu quả:** Không có trường nào để đo lường `transformation_ratio` (tỷ lệ chuyển đổi) hoặc hiệu quả thực sự của Project trong việc giải quyết `Tension` và tạo ra `WIN`. |
| **`POST /api/v1/wins/`** | Tạo `WIN` với `name`, `narrative`. | **Giá trị không được kết tinh:** `WIN` chỉ là một "câu chuyện". Không có cơ chế để ghi nhận các `generated_assets` (tài sản được tạo ra) một cách có cấu trúc. `WIN` chưa phải là một "trạm biến áp năng lượng" mà chỉ là một điểm cuối. |
| **`GET /api/v1/agents/{id}`** | Trả về thông tin của `Agent`. | **Năng lực bị ẩn:** Không có cách nào để truy vấn hoặc tính toán các chỉ số hiệu suất của `Agent` dựa trên học thuyết, ví dụ như "Agent này đã tạo ra bao nhiêu `resonance_score`?" hay "Tỷ lệ chuyển đổi `Tension` thành `WIN` của Agent này là bao nhiêu?". |

---

## **3. Đặc tả Yêu cầu cho API v2**

Để vá các lỗ hổng trên, API v2 cần có những thay đổi và bổ sung sau:

### **3.1. Sửa đổi các Model Dữ liệu (Schemas)**

*   **`EventCreate_v2`**:
    *   Bổ sung: `signal_strength: float (optional)`, `source_authority: string (optional)`, `tags: List[string]`.
*   **`ProjectCreate_v2`**:
    *   **Bắt buộc:** `source_tension_uid: string`.
    *   Bổ sung: `target_win_narrative: string (optional)`.
*   **`WIN_v2` (Response Model)**:
    *   Bổ sung: `win_class: Enum (CommitmentWIN, RecognitionSignal)`.
    *   Bổ sung: `generated_assets: List[Asset_v2]`.
*   **`Asset_v2`**:
    *   Là một schema mới: `{ "asset_type": string, "asset_id": string, "description": string }`.
*   **`Agent_v2` (Response Model)**:
    *   Bổ sung các trường được tính toán (computed fields): `resonance_impact_score: float`, `win_generation_rate: float`.

### **3.2. Endpoints Mới và Nâng cấp**

*   **(Mới) `POST /api/v2/events/assess-resonance`**:
    *   **Mục đích:** Cung cấp chức năng cốt lõi cho `Sense` và `Reasoning Agents`.
    *   **Request Body:** `{ "event_payload": Event_v2 }`.
    *   **Response Body:** `{ "resonance_score": float, "related_tensions": List[Tension_v2], "is_significant": boolean }`.
    *   **Logic:** Endpoint này sẽ gọi đến `Genesis Engine` để phân tích sự kiện và trả về tiềm năng cộng hưởng của nó.

*   **(Nâng cấp) `POST /api/v2/projects/`**:
    *   **Request Body:** Sử dụng `ProjectCreate_v2`.
    *   **Logic:** Bắt buộc phải tồn tại `Tension` với `source_tension_uid` được cung cấp.

*   **(Nâng cấp) `POST /api/v2/wins/{win_id}/crystallize-asset`**:
    *   **Mục đích:** Biến `WIN` thành "trạm biến áp".
    *   **Request Body:** `{ "asset_type": string, "asset_data": object }`.
    *   **Logic:** Endpoint này sẽ tạo ra một thực thể `Resource` hoặc `KnowledgeSnippet` mới và tạo quan hệ `GENERATES` từ `WIN` đến thực thể đó.

*   **(Mới) `GET /api/v2/dashboard/strategic-overview`**:
    *   **Mục đích:** Cung cấp dữ liệu cho "Bảng điều khiển Chiến lược" của `Human Agent`.
    *   **Response Body:** Trả về một cấu trúc JSON phức hợp, tổng hợp các `Tension` có `resonance_score` cao nhất, các `Project` đang `AtRisk`, và các `WIN` vừa đạt được.

---

## **4. Lộ trình Triển khai Đề xuất**

1.  **Giai đoạn 1: Nâng cấp Nền tảng (Core Models)**
    *   Triển khai các schema `*_v2` cho `Event`, `Project`, `WIN`.
    *   Nâng cấp các endpoint `POST`, `GET`, `PUT` tương ứng để hỗ trợ các schema mới. API v1 có thể được duy trì song song trong giai đoạn này.
2.  **Giai đoạn 2: Xây dựng các Endpoint Thông minh**
    *   Triển khai `POST /api/v2/events/assess-resonance`. Đây là ưu tiên hàng đầu vì nó khởi động toàn bộ vòng lặp vận hành.
    *   Triển khai `POST /api/v2/wins/{win_id}/crystallize-asset`.
3.  **Giai đoạn 3: Xây dựng các Endpoint Tổng hợp**
    *   Triển khai `GET /api/v2/dashboard/strategic-overview` và các API tổng hợp khác phục vụ cho giao diện người dùng và agent quản lý.
4.  **Giai đoạn 4: Ngừng hỗ trợ API v1**
    *   Sau khi tất cả các client đã chuyển sang v2, các endpoint v1 sẽ được loại bỏ. 