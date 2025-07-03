# Học Thuyết Thống Nhất TRM-OS - Tập 7: Kiến trúc và các Mẫu hình Hệ thống

**Phiên bản:** 1.0
**Trạng thái:** Bản nháp đầu tiên
**Người biên soạn:** Gemini-Pro Agent & Human Co-founder

---

## **Lời nói đầu: Từ Học thuyết đến Mã nguồn**

Nếu các tập trước của Học thuyết định nghĩa "cái gì" (what) và "tại sao" (why), thì tập này tập trung vào "làm thế nào" (how). Nó mô tả các quyết định kiến trúc và các mẫu hình (patterns) đã được chứng minh là hiệu quả, được đúc kết từ các phiên bản trước, nhằm đảm bảo hệ thống được xây dựng một cách nhất quán, có thể bảo trì và mở rộng.

Đây là cây cầu nối giữa tư duy chiến lược và việc triển khai kỹ thuật.

---

## **1. Mẫu hình Trung tâm: Ontology-First**

**Nguyên tắc:** Toàn bộ hệ thống, từ cơ sở dữ liệu đến API, đều phải là sự phản ánh trực tiếp của các thực thể và mối quan hệ được định nghĩa trong "Tập 2: Từ Điển Các Thực Thể Cốt Lõi".

*   **Không có đường tắt:** Không được phép tạo ra các thuộc tính, các mối quan hệ "ma" trong mã nguồn hoặc database mà không được định nghĩa trước trong Học thuyết.
*   **API là tấm gương:** Các API endpoint phải tuân theo cấu trúc của ontology. Ví dụ, để tạo mối quan hệ `(Task)-[:ASSIGNED_TO]->(Agent)`, endpoint phải có ngữ nghĩa tương ứng, ví dụ: `POST /tasks/{task_uid}/assign-to/{agent_uid}`.
*   **Nguồn sự thật duy nhất:** Khi có bất kỳ sự mơ hồ nào về mặt kỹ thuật, Từ điển Thực thể Cốt lõi (Tập 2) là nơi để tìm câu trả lời, không phải mã nguồn hiện có.

---

## **2. Xương sống Giao tiếp: System Event Bus (Mô hình Publish/Subscribe)**

**Vấn đề:** Các Agent cần giao tiếp với nhau một cách phi đồng bộ (asynchronously) và không phụ thuộc trực tiếp vào nhau (decoupled) để đảm bảo tính linh hoạt và khả năng mở rộng.

**Giải pháp:** Sử dụng một `SystemEventBus` trung tâm, hoạt động theo mô hình Publish/Subscribe.

*   **Luồng hoạt động:**
    1.  Một `Agent` (Publisher) khi thực hiện xong một hành động quan trọng (ví dụ: `TensionResolutionAgent` vừa tạo ra một `Project` mới) sẽ không gọi trực tiếp các agent khác. Thay vào đó, nó sẽ phát (publish) một `Event` lên Event Bus (ví dụ: `Event.type = 'Project.Created'`, `metadata = { projectId: '...' }`).
    2.  Các `Agent` khác (Subscribers) đã đăng ký lắng nghe loại `Event` đó sẽ nhận được thông báo và thực thi logic của riêng mình. Ví dụ, `NotificationAgent` có thể đăng ký `Project.Created` để gửi email thông báo, trong khi `ResourceAllocationAgent` cũng có thể lắng nghe để bắt đầu chuẩn bị nguồn lực.

*   **Lợi ích:**
    *   **Giảm sự phụ thuộc:** Các agent không cần biết về sự tồn tại của nhau.
    *   **Tăng khả năng mở rộng:** Dễ dàng thêm các agent mới để lắng nghe các sự kiện hiện có mà không cần sửa đổi các agent cũ.
    *   **Tăng khả năng phục hồi:** Nếu một agent subscriber bị lỗi, các agent khác vẫn hoạt động bình thường.

---

## **3. Mẫu hình Nền tảng Agent: Lớp trừu tượng `BaseAgent`**

**Vấn đề:** Cần một cấu trúc chuẩn và vòng đời nhất quán cho tất cả các `AI Agent` để dễ quản lý, giám sát và phát triển.

**Giải pháp:** Tất cả các lớp `AIAgent` cụ thể (ví dụ: `DataSensingAgent`, `TensionAnalysisAgent`) đều phải kế thừa từ một lớp trừu tượng `BaseAgent`.

*   **Cấu trúc của `BaseAgent`:**
    *   **Metadata:** Chứa các thông tin mô tả về agent (`name`, `version`, `description`).
    *   **Vòng đời (Lifecycle Methods):** Cung cấp các phương thức async chuẩn mà hệ thống (hoặc `AGE`) có thể gọi:
        *   `initialize()`: Chuẩn bị các tài nguyên cần thiết khi agent khởi động.
        *   `start()`: Bắt đầu vòng lặp hoạt động chính của agent và đăng ký các trình xử lý sự kiện (event handlers) với `SystemEventBus`.
        *   `stop()`: Dọn dẹp tài nguyên và hủy đăng ký khỏi `SystemEventBus` một cách an toàn.
    *   **Trình xử lý Sự kiện (Event Handlers):** Các phương thức được thiết kế để xử lý các loại `Event` cụ thể mà agent đăng ký.

---

## **4. Mẫu hình Phòng vệ: Data Adapter**

**Vấn đề:** Dữ liệu đầu vào từ thế giới bên ngoài (API của bên thứ ba, input của người dùng) hoặc từ các phiên bản legacy của hệ thống thường không nhất quán và không tuân thủ định dạng chuẩn của ontology (ví dụ: định dạng ngày tháng, giá trị enum khác nhau).

**Giải pháp:** Áp dụng `Data Adapter Pattern` tại các "cửa ngõ" của hệ thống (ví dụ: ngay sau khi nhận một request API, trước khi đưa vào service logic).

*   **Luồng hoạt động:**
    1.  Một request API đến với payload chứa `{ "creation_date": "25-04-2025", "status": "IN_PROGRESS" }`.
    2.  Trước khi `ProjectService` xử lý, một `ProjectAdapter` sẽ được áp dụng.
    3.  Adapter này chuẩn hóa dữ liệu:
        *   Chuyển đổi `"25-04-2025"` thành `"2025-04-25T00:00:00Z"`.
        *   Chuyển đổi `"IN_PROGRESS"` thành `"InProgress"`.
    4.  `ProjectService` giờ đây nhận được một đối tượng dữ liệu sạch, đã được chuẩn hóa, và có thể làm việc với nó một cách an toàn.

*   **Lợi ích:**
    *   **Logic nghiệp vụ sạch:** Các lớp service không cần phải bận tâm về việc làm sạch dữ liệu.
    *   **Bảo vệ hệ thống:** Ngăn chặn dữ liệu "bẩn" lọt vào và làm hỏng tính toàn vẹn của cơ sở dữ liệu.
    *   **Dễ bảo trì:** Logic chuẩn hóa được tập trung ở một nơi (các lớp Adapter), thay vì rải rác khắp nơi trong mã nguồn. 