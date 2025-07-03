# Học Thuyết Thống Nhất TRM-OS - Tập 2: Từ Điển Các Thực Thể Cốt Lõi

**Phiên bản:** 4.2
**Trạng thái:** Hoàn thiện (Bản Nâng cấp Toàn diện)
**Người biên soạn:** Gemini-Pro Agent & Human Co-founder

---

## **Lời nói đầu**
Đây là tài liệu tham khảo kỹ thuật trung tâm, định nghĩa các "danh từ" – những khối xây dựng hữu hình của hệ thống. Mỗi thực thể được mô tả qua 4 lăng kính:
1.  **Định nghĩa Chuẩn:** Phát biểu ngắn gọn.
2.  **Bản chất - Góc nhìn Kiến trúc:** Diễn giải "tại sao" nó tồn tại và vai trò của nó.
3.  **Thuộc tính Kỹ thuật:** Đặc tả chi tiết các trường dữ liệu, kế thừa và mở rộng từ V3.2.
4.  **Ví dụ Đa dạng & Phản-ví dụ:** Các ví dụ cụ thể, bao phủ nhiều trường hợp và các ví dụ chống lại sự nhầm lẫn.

Để có một góc nhìn tường thuật, xin tham khảo tài liệu `01.1_Narrative_Walkthrough.md`.

---
## **Chương 1: Các Thực Thể (Entities) Cốt Lõi**

### **1. `Event` (Sự Kiện)**
*   **Định nghĩa Chuẩn:** `Event` là một bản ghi bất biến về một sự thật đã xảy ra tại một thời điểm nhất định.
*   **Bản chất - Góc nhìn Kiến trúc:** Giá trị của một `Event` không nằm ở bản thân nó, mà ở **tiềm năng gây cộng hưởng (Resonance Potential)**. Hệ thống không chỉ hỏi "Chuyện gì đã xảy ra?" mà liên tục hỏi **"Thông tin này có thể thay đổi cuộc chơi không?"**.
*   **Thuộc tính Kỹ thuật:**
    *   `uid`: **UUID** `(Primary Key)`
    *   `eventType`: **String (Enum)** `(Required)`
    *   `timestamp`: **ISO 8601 String** `(Required)`
    *   `source`: **String** `(Required)`
    *   `description`: **String**
    *   `metadata`: **JSON** `(Required)` - Chứa các thuộc tính động như `signal_strength`, `information_energy`, `keywords`.
    *   `causationId`: **UUID** - ID của event đã gây ra event này.
*   **Ví dụ Đa dạng & Phản-ví dụ:**
    *   **Ví dụ 1: External Signal (Cộng hưởng cao)** - Kịch bản Zuckerberg
        ```json
        {
          "uid": "evt_7a8b3c4d",
          "eventType": "External.Signal.LeaderIntent",
          "source": "Agent/TechNews-Sensing-Agent",
          "metadata": {
            "source_url": "https://forbes.com/...",
            "publication": "Forbes",
            "signal_strength": 0.9,
            "information_energy": 0.85
          }
        }
        ```
    *   **Ví dụ 2: Internal Alert (Cộng hưởng thấp)**
        ```json
        {
          "uid": "evt_b4a2c1e8",
          "eventType": "Internal.System.Alert",
          "source": "Agent/MonitoringAgent",
          "metadata": { "service": "auth-service", "metric": "cpu_utilization", "value": "85%" }
        }
        ```
    *   **Ví dụ 3: Founder Input**
        ```json
        {
          "uid": "evt_c9d8e7f6",
          "eventType": "Manual.Founder.StrategicInput",
          "source": "User/founder_username",
          "description": "We need to explore the Southeast Asia market in Q4.",
          "metadata": { "signal_strength": 1.0, "information_energy": 0.7 }
        }
        ```
    *   **Phản-ví dụ:** Một `cron job` chạy hàng ngày để xóa log cũ. Về mặt kỹ thuật, nó tạo ra một log entry, nhưng nó không phải là một `Event` theo học thuyết vì nó có `information_energy` và `signal_strength` bằng 0, không có khả năng gây cộng hưởng chiến lược.

### **2. `Tension` (Sức Căng / Cơ Hội Chiến Lược)**
*   **Định nghĩa Chuẩn:** `Tension` là một đối tượng dữ liệu được tạo ra khi phát hiện sự cộng hưởng, nhằm lượng hóa một cơ hội chiến lược.
*   **Bản chất - Góc nhìn Kiến trúc:** `Tension` là **sự chênh lệch điện thế được lượng hóa giữa "thực tại" và "tiềm năng"**. Nó biến một sự kiện mơ hồ thành một giả thuyết chiến lược rõ ràng, một "vector lực" thúc đẩy hệ thống hành động.
*   **Thuộc tính Kỹ thuật:**
    *   `uid`: **UUID** `(Primary Key)`
    *   `title`: **String** `(Required)`
    *   `status`: **String (Enum)** `(New, UnderAnalysis, Resolved, ...)`
    *   `priority`: **Integer** `(1-Critical, 2-High, ...)`
    *   `sourceEventUid`: **UUID** `(Required)`
    *   `current_state`: **String** `(Required)`
    *   `desired_state`: **String** `(Required)`
    *   `impact_assessment`: **String**
*   **Ví dụ Đa dạng & Phản-ví dụ:**
    *   **Ví dụ 1: Cơ hội từ External Signal** - Kịch bản Zuckerberg
        ```json
        {
          "uid": "ten_1a2b3c4d",
          "title": "Cơ hội M&A với Meta khi Mark Zuckerberg tìm giải pháp Agentic AI",
          "priority": 1,
          "sourceEventUid": "evt_7a8b3c4d",
          "current_state": "TRM-OS chưa được các nhà lãnh đạo công nghệ hàng đầu biết đến.",
          "desired_state": "Mark Zuckerberg và đội ngũ Meta đánh giá cao TRM-OS, dẫn đến một cuộc họp chiến lược."
        }
        ```
    *   **Ví dụ 2: Vấn đề từ Internal Alert**
        ```json
        {
          "uid": "ten_f8e7d6c5",
          "title": "Rủi ro hiệu năng dịch vụ Auth gây ảnh hưởng trải nghiệm người dùng",
          "priority": 2,
          "sourceEventUid": "evt_b4a2c1e8",
          "current_state": "Dịch vụ Auth có CPU trung bình 85% trong giờ cao điểm.",
          "desired_state": "Dịch vụ Auth có CPU trung bình dưới 50% và P99 response time < 200ms."
        }
        ```
    *   **Phản-ví dụ:** Một ticket bug thông thường như "Nút bấm bị lệch 2 pixel". Đây là một `Task`, không phải `Tension`, vì nó không mô tả một sự chênh lệch chiến lược giữa thực tại và tiềm năng, mà là một sai sót cần sửa chữa.

### **3. `Project` (Dự án)**
*   **Định nghĩa Chuẩn:** `Project` là một thực thể quản lý bao gồm toàn bộ `Tasks`, `Resources`, và `Agents` được tập hợp lại để giải quyết một `Tension` cụ thể.
*   **Bản chất - Góc nhìn Kiến trúc:** `Project` là một **cỗ máy tạm thời được xây dựng để giải quyết một `Tension` duy nhất**. Hiệu quả của nó được đo bằng **tỷ lệ chuyển đổi (transformation ratio)**: (giá trị của `WIN` tạo ra) / (chi phí tài nguyên đã tiêu thụ).
*   **Thuộc tính Kỹ thuật:**
    *   `uid`: **UUID** `(Primary Key)`
    *   `title`: **String** `(Required)`
    *   `goal`: **String** `(Required)`
    *   `status`: **String (Enum)** `(Planning, Active, Completed, ...)`
    *   `source_tension_uid`: **UUID** `(Required)`
    *   `target_win_description`: **String`
*   **Ví dụ Đa dạng & Phản-ví dụ:**
    *   **Ví dụ 1: Dự án Chiến lược** - Kịch bản Zuckerberg
        ```json
        {
          "uid": "proj_9f8e7d6c",
          "title": "Chiến dịch Tiếp cận Mark Zuckerberg (Project 'Leviathan')",
          "goal": "Tạo ra một 'Commitment WIN': có được một buổi thuyết trình 30 phút với Mark Zuckerberg trong vòng 3 tháng tới.",
          "source_tension_uid": "ten_1a2b3c4d"
        }
        ```
    *   **Ví dụ 2: Dự án Kỹ thuật**
        ```json
        {
          "uid": "proj_a1b2c3d4",
          "title": "Tái cấu trúc (Refactor) dịch vụ Authentication",
          "goal": "Giảm P99 response time xuống dưới 200ms và CPU utilization xuống dưới 50%.",
          "source_tension_uid": "ten_f8e7d6c5"
        }
        ```
    *   **Phản-ví dụ:** "Bảo trì hệ thống hàng tuần". Đây là một hoạt động vận hành (Operations), không phải là một `Project` vì nó không giải quyết một `Tension` cụ thể để tạo ra một `WIN` mới, mà là để duy trì trạng thái hiện tại.

### **4. `WIN` (Chiến Thắng)**
*   **Định nghĩa Chuẩn:** Một `WIN` là bằng chứng cho thấy một `Tension` đã được giải quyết và giá trị mới đã được tạo ra cho hệ thống.
*   **Bản chất - Góc nhìn Kiến trúc:** `WIN` là sự **kết tinh của nỗ lực**, biến nó thành tài sản mới và động năng cho các vòng lặp tiếp theo. Nó không phải là điểm kết thúc.
*   **Phân loại:**
    *   **`Commitment WIN`**: Cam kết tài nguyên hữu hình (tiền, hợp đồng, nhân lực).
    *   **`Recognition Signal`**: Tài sản uy tín vô hình (sự công nhận, sự chú ý).
*   **Thuộc tính Kỹ thuật:**
    *   `uid`: **UUID** `(Primary Key)`
    *   `name`: **String** `(Required)`
    *   `win_class`: **Enum** `(CommitmentWIN, RecognitionSignal)` `(Required)`
    *   `narrative`: **String (Markdown)**
    *   `generated_assets`: **JSON**
*   **Ví dụ Đa dạng & Phản-ví dụ:**
    *   **Ví dụ 1: `Commitment WIN` (External)** - Kịch bản Zuckerberg
        ```json
        {
          "uid": "win_5e4f3g2h",
          "name": "Secured: 30-Min Pitch with Mark Zuckerberg",
          "win_class": "CommitmentWIN",
          "narrative": "Project 'Leviathan' đã thành công có được một buổi hẹn chiến lược...",
          "generated_assets": [{ "asset_type": "Opportunity", "description": "30-min pitch session...", "value": { "status": "Scheduled" } }]
        }
        ```
    *   **Ví dụ 2: `Recognition Signal` (External)**
        ```json
        {
          "uid": "win_b1a2c3d4",
          "name": "Signal: Andrew Bosworth (Meta CTO) followed Founder on Twitter",
          "win_class": "RecognitionSignal",
          "narrative": "Trong quá trình thực hiện Project 'Leviathan', Andrew Bosworth đã follow Founder của chúng ta...",
          "generated_assets": [{ "asset_type": "Reputation", "description": "Follow relationship from a key industry leader" }]
        }
        ```
    *   **Ví dụ 3: `Commitment WIN` (Internal)**
        ```json
        {
          "uid": "win_c3d4e5f6",
          "name": "Completed: Auth Service Refactor with 70% performance gain",
          "win_class": "CommitmentWIN",
          "narrative": "Project tái cấu trúc dịch vụ Auth đã hoàn thành, P99 giảm từ 800ms xuống 240ms.",
          "generated_assets": [{ "asset_type": "Knowledge", "description": "Best practices for scaling NodeJS services", "ref": "ks_9z8y7x6w" }]
        }
        ```
    *   **Phản-ví dụ:** Hoàn thành một `Task` như "Viết tài liệu cho API". Đây là một `Task` được đánh dấu `Done`, không phải là một `WIN`. Nó là một bước trong quá trình, nhưng tự nó không tạo ra một tài sản chiến lược mới hay giải quyết một `Tension` ở cấp độ vĩ mô.

### **5. `Agent` (Tác Nhân)**
*   **Định nghĩa Chuẩn:** `Agent` là một thực thể trong hệ thống có quyền tự quyết và khả năng hành động để thay đổi trạng thái của các thực thể khác.
*   **Bản chất - Góc nhìn Kiến trúc:** `Agent` là những "người thực thi". Vai trò của chúng được phân chia rạch ròi để tối ưu hóa sự kết hợp giữa trí tuệ con người và năng lực tính toán của máy.
    *   **`Human Agent`**: Là người ra quyết định dựa trên **trực giác, kinh nghiệm, và bối cảnh phức tạp**. Họ định nghĩa "ý nghĩa" và chịu trách nhiệm chiến lược.
    *   **`AI Agentic (AGE)`**: Là các thực thể phần mềm tự hành, hoạt động dựa trên **logic và dữ liệu**. Chúng thực thi, tối ưu, và mở rộng quy mô. Chúng thực hiện "công việc".
*   **Thuộc tính Kỹ thuật:**
    *   `uid`: **UUID** `(Primary Key)`
    *   `agent_type`: **Enum** `(Human, AI)` `(Required)`
    *   `name`: **String** `(Required)`
    *   `role`: **String** `(e.g., Founder, SensingAgent, ReasoningAgent)`
    *   `capabilities`: **Array of Strings** `(e.g., "market_analysis", "code_generation")`
*   **Ví dụ Đa dạng & Phản-ví dụ:**
    *   **Ví dụ 1: Human Agent**
        ```json
        {
          "uid": "agent_human_001",
          "agent_type": "Human",
          "name": "ten_founder",
          "role": "Founder",
          "capabilities": ["strategic_decision_making", "resource_allocation", "final_approval"]
        }
        ```
    *   **Ví dụ 2: AI Sensing Agent**
        ```json
        {
          "uid": "agent_ai_001",
          "agent_type": "AI",
          "name": "TechNews-Sensing-Agent",
          "role": "SensingAgent",
          "capabilities": ["news_aggregation", "sentiment_analysis", "event_creation"]
        }
        ```
    *   **Phản-ví dụ:** Một `User` (người dùng) có tài khoản đăng nhập để xem dashboard. Nếu người dùng này không có quyền thực hiện hành động (tạo `Project`, phê duyệt `WIN`), họ chỉ là một `Viewer`, không phải là một `Agent`. Trong TRM-OS, `Agent` phải có năng lực hành động.

---
## **Chương 2: Các Mối quan hệ (Relationships) - Dòng chảy Năng lượng**

Các mối quan hệ trong TRM-OS không phải là những đường kẻ tĩnh. Chúng là các **kênh dẫn truyền năng lượng và ngữ cảnh**, mang theo các thuộc tính quan trọng.

*   **(Event) -[:TRIGGERS {resonance_score: 0.9}]-> (Tension)**
    *   **Ý nghĩa:** `Event` này đã kích hoạt `Tension` với mức độ cộng hưởng là 0.9.
*   **(Tension) -[:SPAWNS]-> (Project)**
    *   **Ý nghĩa:** `Tension` này đã được cụ thể hóa thành một `Project` để giải quyết.
*   **(Project) -[:RESOLVES]-> (Tension)**
    *   **Ý nghĩa:** `Project` này tồn tại để giải quyết `Tension` này.
*   **(Project) -[:AIMS_FOR]-> (WIN)**
    *   **Ý nghĩa:** `Project` này có mục tiêu tạo ra `WIN` này.
*   **(Agent) -[:EXECUTES {role: "Lead"}]-> (Project)**
    *   **Ý nghĩa:** `Agent` này là người dẫn dắt, chịu trách nhiệm chính cho `Project`.
*   **(WIN) -[:GENERATES]-> (Resource/Asset)**
    *   **Ý nghĩa:** `WIN` này đã kết tinh thành `Tài sản` này.
*   **(WIN) -[:CLOSES]-> (Tension)**
    *   **Ý nghĩa:** Việc ghi nhận `WIN` này là bằng chứng cho thấy `Tension` đã được giải quyết.