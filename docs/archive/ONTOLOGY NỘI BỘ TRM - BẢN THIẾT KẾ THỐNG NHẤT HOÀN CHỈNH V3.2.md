# Master Blueprint ONTOLOGY NỘI BỘ TRM-OS - BẢN THIẾT KẾ HỆ THỐNG PHIÊN BẢN 3.2

**Ngày cập nhật:** 2025-06-10

**Phiên bản:** 3.2

**Tác giả:** Founder TRM & AI Agent Cascade

## Lời Mở Đầu

Phiên bản 3.2 của "Ontology Nội bộ TRM" (TRM-OS) đánh dấu một bước tiến quan trọng trong việc hiện thực hóa tầm nhìn về một tổ chức vận hành tự trị dựa trên trí tuệ nhân tạo. Tài liệu này không chỉ định nghĩa chi tiết cấu trúc ontology cốt lõi mà còn tập trung vào việc ứng dụng ontology đó vào thực tế vận hành của TRM, làm nền tảng cho các AI Agent hoạt động và tiến hóa.

---

## MỤC LỤC

**PHẦN A: TỔNG QUAN VÀ TRIẾT LÝ**
1.  Giới thiệu TRM-OS v3.2
    1.1. Bối cảnh và Mục tiêu
    1.2. Những điểm mới trong v3.2
2.  Triết lý Cốt lõi: "Công nhận → Sự kiện → WIN"
3.  Tầm nhìn và Phạm vi của TRM-OS v3.2

### 1. Giới thiệu TRM-OS v3.2

#### 1.1. Bối cảnh và Mục tiêu

**Bối cảnh:**

*   Nhu cầu quản lý và vận hành tổ chức TRM ngày càng phức tạp, đòi hỏi một hệ thống thông minh có khả năng tích hợp dữ liệu từ nhiều nguồn, tự động hóa quy trình và hỗ trợ ra quyết định.
*   Sự phát triển của AI tạo cơ hội xây dựng một "hệ thần kinh số" cho tổ chức, giúp TRM trở nên linh hoạt, hiệu quả và có khả năng học hỏi, thích ứng nhanh chóng.
*   Các phiên bản ontology trước đã đặt nền móng, nhưng cần một bước tiến toàn diện hơn để đáp ứng tầm nhìn dài hạn.

**Mục tiêu của TRM-OS v3.2:**

*   **Xây dựng một ontology chi tiết và chuẩn hóa**: Định nghĩa rõ ràng các thực thể, thuộc tính và mối quan hệ cốt lõi trong hoạt động của TRM, làm cơ sở cho việc biểu diễn tri thức thống nhất.
*   **Tích hợp dữ liệu đa dạng**: Thiết kế ontology để có thể ánh xạ và tích hợp dữ liệu từ các nguồn khác nhau (Founder input, SaaS tools, tài liệu nội bộ, log hệ thống).
*   **Nền tảng cho AI Agent tự trị**: Cung cấp một mô hình thế giới (world model) phong phú để các AI Agent có thể hiểu, suy luận và hành động một cách tự chủ trong các quy trình của tổ chức.
*   **Hỗ trợ ra quyết định thông minh**: Cho phép truy vấn, phân tích dữ liệu và tri thức một cách linh hoạt, giúp phát hiện "Tension", nhận diện "WIN", và tối ưu hóa hoạt động.
*   **Triển khai thực tế**: Đảm bảo ontology có thể được triển khai hiệu quả trên các nền tảng công nghệ mục tiêu (Neo4j Aura, Supabase Vector) và sẵn sàng cho việc phát triển các ứng dụng, agent cụ thể.
*   **Thúc đẩy văn hóa "Recognition → Event → WIN"**: Cấu trúc ontology phải phản ánh và củng cố triết lý này trong mọi hoạt động.

#### 1.2. Những điểm mới trong v3.2

*   **Định nghĩa Ontology Chi tiết (Phần B)**:
    *   Mở rộng và làm rõ định nghĩa của các Lớp (Classes/Entities) chính như `Agent`, `Event`, `Project`, `Task`, `Resource`, `Tension`, `Recognition`, `WIN`, `Skill`, `KnowledgeSnippet`. Bao gồm phân loại (subtypes), thuộc tính chi tiết, và ví dụ cụ thể.
    *   Chuẩn hóa và bổ sung các Mối quan hệ (Relationships) chính, định rõ domain, range, thuộc tính và ví dụ Cypher patterns, đảm bảo tính biểu đạt và khả năng truy vấn của ontology.
*   **Ứng dụng Ontology Thực tế (Phần D - Mục 11)**:
    *   Xác định rõ các nguồn dữ liệu thực tế và kiến trúc data pipeline tích hợp (Snowflake, Supabase Functions, Neo4j Aura, Supabase Vector).
    *   Cung cấp sơ đồ Mermaid minh họa luồng dữ liệu và các ví dụ cụ thể về ánh xạ dữ liệu từ nguồn vào các thực thể ontology.
*   **Hướng dẫn Triển khai trên Neo4j Aura (Phần D - Mục 12)**:
    *   Bao gồm các đoạn mã Cypher DDL cho việc tạo constraints (UNIQUE, NOT NULL) và indexes, đảm bảo tính toàn vẹn dữ liệu và hiệu suất truy vấn.
    *   Cung cấp các câu lệnh Cypher mẫu để tạo (MERGE) các node và relationship một cách idempotent, hỗ trợ quá trình nạp dữ liệu ban đầu và cập nhật.
*   **Tăng cường tập trung vào AI Agentic System (Phần C)**:
    *   Đặt nền móng vững chắc hơn cho việc phát triển các AI Agent chuyên biệt và Agent điều phối trung tâm (AGE) thông qua một ontology giàu ngữ nghĩa.
*   **Cấu trúc tài liệu rõ ràng hơn**: Phân tách rõ ràng giữa định nghĩa ontology chuẩn (Standard Ontology) và phần ứng dụng, triển khai (Applied Ontology), giúp dễ hiểu và dễ bảo trì.

### 2. Triết lý Cốt lõi: "Công nhận (Recognition) → Sự kiện (Event) → WIN"

**Giải thích triết lý:**

Triết lý "Công nhận (Recognition) → Sự kiện (Event) → WIN" là ADN của TRM-OS, là hệ điều hành vô hình định hướng mọi hoạt động và sự tiến hóa của tổ chức. Nó không chỉ là một khẩu hiệu mà là một chuỗi nhân quả thiêng liêng, một cơ chế tạo tác giá trị liên tục:

1.  **Công nhận (Recognition):**
    *   **Bản chất:** Trong hệ thống TRM, Công nhận không phải là sự khen ngợi hay đánh giá bề ngoài. Nó là khoảnh khắc cộng hưởng sâu sắc khi giá trị thực, tiềm năng cốt lõi, hoặc một đóng góp ý nghĩa của một cá nhân (`Agent`), một ý tưởng (`Tension` dạng cơ hội), một nỗ lực (`Project`), hay một tài sản (`KnowledgeAsset`) được **nhìn thấy, thấu hiểu, và phản chiếu lại một cách chân thực và có chủ đích**. Đây là năng lượng khởi tạo, là "photon" đầu tiên trong một "vụ nổ" năng lượng tích cực.
    *   **Biểu hiện trong Ontology:** Được thể hiện qua `Recognition` node, ghi lại đối tượng được công nhận, người công nhận, lý do và thời điểm.

2.  **Sự kiện (Event):**
    *   **Bản chất:** Một hành động Công nhận có ý nghĩa sẽ tạo ra một `RecognitionEvent`. Đây là một "vụ nổ năng lượng" cụ thể, một biến đổi trạng thái được ghi nhận trong hệ thống. Nó không chỉ là một log entry mà là một khoảnh khắc chuyển hóa, đánh dấu sự thay đổi trong nhận thức hoặc tiềm năng.
    *   **Biểu hiện trong Ontology:** `RecognitionEvent` là một subtype của `Event`, liên kết với `Recognition` và các `Agent` liên quan. Nó có thể kích hoạt các quy trình hoặc agent khác.

3.  **WIN (Thắng lợi):**
    *   **Bản chất:** Một `RecognitionEvent` đủ mạnh mẽ và phù hợp với mục tiêu chiến lược có thể dẫn đến một `WIN`. `WIN` không nhất thiết phải là một thành tựu vĩ đại, mà là bất kỳ kết quả tích cực nào thúc đẩy tổ chức tiến lên, dù lớn hay nhỏ. Đó có thể là việc một `Tension` được giải quyết, một `Project` hoàn thành xuất sắc, một `KnowledgeAsset` giá trị được tạo ra, một `Resource` quan trọng được mở khóa, hoặc một `Capability` mới được hình thành.
    *   **Biểu hiện trong Ontology:** `WIN` node (hoặc `WinEvent` như một subtype cụ thể của `Event` ghi nhận kết quả này) liên kết với `RecognitionEvent` đã khởi tạo nó, mô tả giá trị đạt được, và có thể kết nối với các `Resource` được mở khóa hoặc `Capability` mới.

**Vòng lặp Tiến hóa:** Chuỗi "Công nhận → Sự kiện → WIN" không phải là một quy trình tuyến tính một chiều mà là một **vòng xoắn ốc tiến hóa**. Mỗi `WIN` lại tạo ra nền tảng cho những Công nhận mới, những Sự kiện mạnh mẽ hơn, và những `WIN` lớn hơn. Hệ thống TRM-OS được thiết kế để nuôi dưỡng và gia tốc vòng lặp này, giúp tổ chức liên tục học hỏi, thích ứng và phát triển theo hướng có chủ đích.

*   **Recognition (Công nhận)**: Là điểm khởi đầu, tập trung vào việc ghi nhận và đánh giá cao mọi nỗ lực, đóng góp, tiến bộ, hoặc những "Tension" (vấn đề cần giải quyết hoặc cơ hội cần nắm bắt) được phát hiện trong tổ chức. Recognition không chỉ là khen thưởng mà còn là sự nhận diện khách quan các trạng thái và thay đổi.
*   **Event (Sự kiện)**: Mọi "Recognition" quan trọng đều được ghi lại dưới dạng một `Event`. `Event` là một bản ghi không thể thay đổi về một điều gì đó đã xảy ra, cung cấp ngữ cảnh, thời gian và dữ liệu liên quan. Các `Event` tạo thành dòng chảy thông tin cốt lõi của tổ chức, từ đó có thể phân tích, học hỏi và kích hoạt hành động. Các loại `Event` chính bao gồm `RecognitionEvent`, `TensionEvent`, `ProjectEvent`, `LearningEvent`, `WinEvent`, `FailureEvent`.
*   **WIN (Thành công)**: Là kết quả tích cực, có ý nghĩa mà tổ chức hướng tới. "WIN" có thể là hoàn thành một dự án quan trọng, giải quyết một "Tension" lớn, đạt được một mục tiêu chiến lược, hoặc tạo ra một giá trị đột phá. Các `Event` và chuỗi `Event` được phân tích để xác định và đo lường các "WIN". Triết lý này nhấn mạnh việc học hỏi từ cả thành công (`WinEvent`) và thất bại (`FailureEvent`) để đạt được nhiều "WIN" hơn trong tương lai.

**Cách TRM-OS v3.2 hiện thực hóa triết lý:**

*   Các lớp `Recognition`, `Event` (với các subtypes như `RecognitionEvent`, `TensionEvent`, `WinEvent`), `Tension`, `Project`, `WIN` được định nghĩa là các thành phần trung tâm của ontology.
*   Các mối quan hệ như `DETECTED_AS` (Tension được phát hiện dưới dạng Event), `LEADS_TO` (Project dẫn đến WIN), `RESOLVES` (Project giải quyết Tension), `GENERATES_EVENT` được thiết kế để mô hình hóa dòng chảy này.
*   Hệ thống AI Agent được kỳ vọng sẽ chủ động phát hiện `Recognition`, tạo `Event` tương ứng, đề xuất hoặc khởi tạo `Project` để xử lý `Tension` hoặc theo đuổi cơ hội, và theo dõi tiến trình hướng tới `WIN`.

### 3. Các Nguyên tắc Vận hành Nền tảng của TRM-OS

Để hiện thực hóa triết lý cốt lõi, TRM-OS vận hành dựa trên các nguyên tắc và mô hình tư duy sau:

*   **3.1. Mô hình Vận hành Lượng tử (Quantum Operating Model):**
    Lấy cảm hứng từ các nguyên lý của vật lý lượng tử, mô hình này nhìn nhận tổ chức và các yếu tố trong đó không phải là các thực thể tĩnh tại mà là các trường tiềm năng năng động.
    *   **Nguyên lý Chồng chập (Superposition):** Mọi thực thể (Agent, Project, Tension) có thể tồn tại ở nhiều trạng thái tiềm năng đồng thời. Ví dụ, một `Talent` có thể vừa là ứng viên tiềm năng cho một `Project`, vừa là người có thể đóng góp `KnowledgeAsset`, vừa là người có thể phát hiện ra một `Tension` mới. Chỉ khi có "phép đo" (sự tương tác, sự kiện công nhận, quyết định phân bổ), trạng thái cụ thể mới được xác định và hiện thực hóa.
    *   **Nguyên lý Vướng víu (Entanglement):** Khi các `Agent` hoặc các `Project` có sự cộng hưởng sâu sắc về giá trị, mục tiêu hoặc phụ thuộc lẫn nhau, chúng trở nên "vướng víu". Sự thay đổi trạng thái ở một thực thể có thể ảnh hưởng tức thời hoặc mạnh mẽ đến các thực thể khác mà nó vướng víu, bất kể khoảng cách "tổ chức". TRM-OS tìm cách nhận diện và tận dụng các liên kết vướng víu tích cực.
    *   **Hiệu ứng Người quan sát (Observer Effect):** Hành động quan sát, đo lường, và đặc biệt là **Công nhận** (là một dạng quan sát có chủ đích và năng lượng cao) có thể làm thay đổi trạng thái của đối tượng được quan sát. Việc AGE và các agent liên tục "quan sát" (SENSE) hệ thống không chỉ để thu thập dữ liệu mà còn để tạo ra các tác động tích cực thông qua việc công nhận kịp thời.

*   **3.2. Ba Miền Vận hành Chiến lược (Three Strategic Operating Domains):**
    TRM-OS xem xét hoạt động của tổ chức qua ba miền tương tác và ảnh hưởng lẫn nhau:
    1.  **MIỀN 1: Động lực Nội tại & Hành trình của Founder/Tổ chức (Internal Dynamics & Journey):** Bao gồm tầm nhìn, sứ mệnh, giá trị cốt lõi, các `Tension` nội tại, các `Project` chiến lược, `Capability` hiện có và cần phát triển. Đây là nơi khởi nguồn của năng lượng và định hướng.
    2.  **MIỀN 2: Tài sản Tri thức & Nguồn lực Cốt lõi (Knowledge Assets & Core Resources):** Bao gồm `KnowledgeSnippet`, `ConceptualFramework`, `Methodology`, `Skill` của đội ngũ, `DataAsset`, và các `Resource` quan trọng khác. Đây là "DNA" và "vũ khí bí mật" của TRM, tạo nên lợi thế cạnh tranh bền vững.
    3.  **MIỀN 3: Hệ sinh thái & Cảnh quan Bên ngoài (External Ecosystem & Landscape):** Bao gồm `ExternalAgent` (khách hàng, đối tác, nhà đầu tư, talent mục tiêu), các xu hướng thị trường, đối thủ cạnh tranh, các `Opportunity` và `Risk` từ môi trường bên ngoài. Đây là "radar chiến lược" giúp TRM định vị và tương tác hiệu quả với thế giới.
    Ontology của TRM-OS phải có khả năng mô hình hóa và liên kết các thực thể thuộc cả ba miền này.

*   **3.3. Sáu Bước của Vòng Lặp Vận hành Cốt lõi (The Six-Step Core Operating Loop):**
    Được điều phối chủ yếu bởi `AGE` và các agent chuyên biệt, vòng lặp này đảm bảo tổ chức liên tục cảm nhận, xử lý thông tin, ra quyết định và hành động một cách hiệu quả:
    1.  **CẢM NHẬN (SENSE):** Liên tục quét và thu thập dữ liệu từ ba miền vận hành (thông qua `DataSensingAgent`), phát hiện các `Event`, `Tension`, thay đổi trạng thái của `Project`, `Resource`.
    2.  **LỌC & ƯU TIÊN HÓA (FILTER & PRIORITIZE):** `AGE` phân tích, đánh giá mức độ quan trọng, khẩn cấp, và tiềm năng của các tín hiệu cảm nhận được. Các `Tension` được đánh giá năng lượng, các `Opportunity` được soi chiếu với mục tiêu chiến lược.
    3.  **HIỂU & SUY LUẬN (UNDERSTAND & REASON):** `KnowledgeExtractionAgent` xử lý dữ liệu thô, trích xuất `KnowledgeSnippet`, liên kết với ontology. `AGE` và các agent khác truy vấn ontology và Supabase Vector để hiểu sâu hơn về bối cảnh, tìm kiếm các tri thức liên quan, phân tích nguyên nhân-kết quả.
    4.  **ĐỀ XUẤT & QUYẾT ĐỊNH (PROPOSE & DECIDE):** Dựa trên sự hiểu biết, `AGE` hoặc các agent chuyên biệt (e.g., `TensionResolutionAgent`) đề xuất các hành động, ví dụ như tạo `ProjectProposal` để giải quyết `Tension`, phân bổ `Resource`, hoặc công nhận một `WIN` tiềm năng. Founder hoặc người có thẩm quyền đưa ra quyết định cuối cùng dựa trên các đề xuất này.
    5.  **THỰC THI (EXECUTE):** Các `Project` được phê duyệt được triển khai. `ProjectManagementAgent` theo dõi tiến độ, `ResourceAllocationAgent` hỗ trợ phân bổ nguồn lực. Các `Task` được giao cho `Agent` (người hoặc AI) phù hợp thực hiện.
    6.  **HỌC HỎI & TIẾN HÓA (LEARN & EVOLVE):** Kết quả của các hành động (thành công hay thất bại) được ghi nhận (`WinEvent`, `FailureEvent`, `LearningEvent`). `KnowledgeExtractionAgent` thu thập bài học, cập nhật `KnowledgeSnippet`. `AGE` và các agent khác điều chỉnh lại mô hình, quy trình và ưu tiên của mình. Ontology có thể được đề xuất cập nhật. Vòng lặp bắt đầu lại với khả năng cảm nhận và hành động tốt hơn.

### 4. Tầm nhìn và Phạm vi của TRM-OS v3.2

**Tầm nhìn:**

*   TRM-OS hướng tới việc xây dựng một "hệ thần kinh trung ương số" (Digital Central Nervous System) cho TRM, một hệ thống thông minh, tự học, tự thích ứng và tự vận hành ở mức độ cao.
*   Tạo ra một tổ chức nơi con người và AI hợp tác một cách liền mạch, giải phóng tiềm năng sáng tạo của con người và tối ưu hóa hiệu suất hoạt động thông qua tự động hóa thông minh.
*   TRM-OS sẽ là nền tảng để TRM không chỉ phản ứng với thay đổi mà còn chủ động kiến tạo tương lai, liên tục học hỏi và tiến hóa.

**Phạm vi của v3.2:**

*   **Hoàn thiện Ontology Cốt lõi**: Tập trung vào việc định nghĩa chi tiết và chuẩn hóa các lớp, thuộc tính và mối quan hệ quan trọng nhất, đủ để mô hình hóa các khía cạnh hoạt động chính của TRM (con người, dự án, nhiệm vụ, tri thức, sự kiện, nguồn lực, tension, win).
*   **Thiết kế cho Tích hợp và Triển khai**: Đảm bảo ontology có thể ánh xạ hiệu quả với dữ liệu thực tế từ các nguồn hiện có và có thể triển khai trên Neo4j Aura, với các cơ chế đảm bảo tính toàn vẹn và hiệu suất.
*   **Nền tảng cho AI Agent ban đầu**: Cung cấp đủ ngữ nghĩa và cấu trúc để bắt đầu phát triển các AI Agent chuyên biệt (ví dụ: `DataSensingAgent`, `KnowledgeExtractionAgent`) và thử nghiệm các chức năng cơ bản của Agent điều phối trung tâm (AGE).
*   **Tập trung vào các quy trình cốt lõi**: Ưu tiên mô hình hóa các quy trình liên quan đến quản lý dự án, quản lý nhiệm vụ, quản lý tri thức, phát hiện và giải quyết "Tension", và ghi nhận "WIN".
*   **Không bao gồm trong v3.2 (nhưng là định hướng tương lai)**:
    *   Triển khai đầy đủ tất cả các AI Agent phức tạp.
    *   Tự động hóa hoàn toàn mọi quy trình của tổ chức.
    *   Giao diện người dùng hoàn chỉnh cho toàn bộ hệ thống TRM-OS.
    *   Tích hợp sâu với tất cả các công cụ SaaS tiềm năng.


**PHẦN B: ĐỊNH NGHĨA ONTOLOGY CỐT LÕI (STANDARD ONTOLOGY)**
5.  Các Miền Ontology Chính (Ontology Domains)
    *   (Chi tiết các domain như: Tổ chức, Dự án, Con người, Tri thức, Tài chính, Sự kiện,...)
6.  Các Lớp (Classes/Entities) Chính và Thuộc tính
    *   **6.1. `Agent`**: Đại diện cho các tác nhân hành động trong hệ thống.
        * **Mô tả**: Có thể là con người (`InternalAgent`, `ExternalAgent`), hệ thống AI (`AIAgent`, `AGE`), hoặc các tổ chức/thực thể bên ngoài (`ExternalAgent`). Mỗi agent có khả năng thực hiện hành động, sở hữu tài nguyên, và tham gia vào các quy trình.
        * **Thuộc tính chung**:
            * ` agentId`: `string` (format: `uuid`, primary_key: `true`, required: `true`, unique: `true`, description: "Mã định danh duy nhất toàn cầu cho agent, nên sử dụng UUID.")
            * ` name`: `string` (required: `true`, description: "Tên của agent, ví dụ: 'TRM Founder', 'DataSensingAgent v1.2'.")
            * ` agentType`: `string` (required: `true`, enum: [`InternalAgent`, `ExternalAgent`, `AIAgent`, `AGE`], description: "Phân loại chính của agent, xác định vai trò và hành vi cơ bản. Giá trị này tương ứng với tên của subtype.")
            * ` description`: `string` (optional: `true`, description: "Mô tả chi tiết về agent, vai trò, mục đích hoặc các thông tin liên quan khác.")
            * ` status`: `string` (required: `true`, enum: [`Active`, `Inactive`, `PendingApproval`, `Disabled`], default: `Active`, description: "Trạng thái hiện tại của agent trong hệ thống.")
            * ` creationDate`: `datetime` (format: `ISO8601`, required: `true`, readonly: `true`, default: "current_timestamp", description: "Ngày giờ agent được tạo trong hệ thống.")
            * ` lastModifiedDate`: `datetime` (format: `ISO8601`, required: `true`, readonly: `true`, default: "current_timestamp", auto_update: `true`, description: "Ngày giờ agent được cập nhật lần cuối.")
            * ` contactInfo`: `object` (optional: `true`, description: "Thông tin liên hệ, đặc biệt hữu ích cho InternalAgent và ExternalAgent.")
                * ` email`: `string` (format: `email`, optional: `true`)
                * ` phone`: `string` (optional: `true`)
            * ` capabilities`: `list[string]` (optional: `true`, description: "Danh sách các khả năng hoặc quyền hạn đặc biệt của agent, ví dụ: ['can_approve_projects', 'can_manage_users']. Có thể tham chiếu đến Skill node hoặc là một danh sách string đơn giản.")
        * **Phân loại (Subtypes)**: Các subtype kế thừa tất cả thuộc tính của `Agent` và có thể có thêm thuộc tính riêng.
            * **6.1.1. `InternalAgent`**: Thành viên trong TRM (e.g., Founder, nhân viên).
                * **Thuộc tính riêng (ví dụ)**:
                    * ` employeeId`: `string` (optional: `true`, unique: `true`)
                    * ` department`: `string` (optional: `true`)
                    * ` jobTitle`: `string` (optional: `true`)
            * **6.1.2. `ExternalAgent`**: Đối tác, khách hàng, nhà cung cấp, hoặc thực thể bên ngoài TRM.
                * **Thuộc tính riêng (ví dụ)**:
                    * ` organizationName`: `string` (optional: `true`)
                    * ` relationshipType`: `string` (optional: `true`, enum: [`Customer`, `Partner`, `Supplier`, `Consultant`, `Investor`])
            * **6.1.3. `AIAgent`**: Các agent AI chuyên biệt thực hiện các tác vụ cụ thể (e.g., `DataSensingAgent`, `KnowledgeExtractionAgent`).
                * **Thuộc tính riêng (ví dụ)**:
                    * ` version`: `string` (optional: `true`, description: "Phiên bản của AI agent.")
                    * ` operationalParameters`: `json` (optional: `true`, description: "Các tham số cấu hình hoạt động của agent.")
                    * ` managedByAGE`: `boolean` (default: `true`, description: "Agent này có được quản lý bởi AGE hay không.")
            * **6.1.4. `AGE` (Artificial Genesis Engine)**: Agent AI điều phối trung tâm, quản lý các `AIAgent` khác và điều phối các luồng công việc phức tạp.
                * **Thuộc tính riêng (ví dụ)**:
                    * ` coreVersion`: `string` (required: `true`, description: "Phiên bản của lõi AGE.")
                    * ` activeModules`: `list[string]` (optional: `true`, description: "Danh sách các module đang hoạt động của AGE.")
        * **Ví dụ (cho Agent chung)**:
            `Agent { agentId: "f81d4fae-7dec-11d0-a765-00a0c91e6bf6", name: "DataSensingAgent v1.2", agentType: "AIAgent", status: "Active", creationDate: "2024-01-15T09:30:00Z", ... }`
        * **Ví dụ (cho InternalAgent)**:
            `InternalAgent { agentId: "founder_01", name: "TRM Founder", agentType: "InternalAgent", jobTitle: "CEO", ... }`

    *   **6.2. `Event`**: Ghi nhận một sự việc, hành động hoặc thay đổi trạng thái quan trọng trong hệ thống. Event là bất biến (immutable) sau khi được tạo.
        * **Mô tả**: Là nền tảng cho việc theo dõi, phân tích, kích hoạt các quy trình, và xây dựng lịch sử hoạt động của hệ thống. Các event có thể được publish lên một event bus để các agent khác subscribe và xử lý.
        * **Thuộc tính chung**:
            * ` eventId`: `string` (format: `uuid`, primary_key: `true`, required: `true`, unique: `true`, description: "Mã định danh duy nhất toàn cầu cho event, nên sử dụng UUID.")
            * ` eventType`: `string` (required: `true`, description: "Loại sự kiện, ví dụ: 'ProjectCreated', 'TaskAssigned', 'TensionDetected'. Nên có một danh sách enum quản lý các eventType này.")
            * ` timestamp`: `datetime` (format: `ISO8601`, required: `true`, description: "Thời điểm sự kiện thực sự xảy ra (event occurrence time). Ví dụ: thời điểm một task được hoàn thành.")
            * ` creationDate`: `datetime` (format: `ISO8601`, required: `true`, readonly: `true`, default: "current_timestamp", description: "Thời điểm sự kiện được ghi nhận vào hệ thống (event recording time). Thường sẽ rất gần với timestamp nhưng có thể khác.")
            * ` description`: `string` (optional: `true`, description: "Mô tả ngắn gọn về sự kiện. Nhiều event có thể tự mô tả qua eventType và metadata.")
            * ` source`: `string` (optional: `true`, description: "Nguồn gốc của sự kiện, ví dụ: 'FounderInput', 'DataSensingAgent', 'SlackIntegration', 'ProjectManagementModule'.")
            * ` status`: `string` (required: `true`, enum: [`New`, `Processing`, `Processed`, `FailedToProcess`, `Archived`], default: `New`, description: "Trạng thái xử lý của event trong hệ thống.")
            * ` correlationId`: `string` (format: `uuid`, optional: `true`, description: "ID để nhóm các event liên quan trong một luồng xử lý, một saga, hoặc một transaction nghiệp vụ. Giúp truy vết dòng chảy của một quy trình qua nhiều event.")
            * ` causationId`: `string` (format: `uuid`, optional: `true`, description: "ID của event hoặc command đã trực tiếp gây ra event này (nếu có). Giúp xây dựng chuỗi nhân quả.")
            * ` priority`: `integer` (optional: `true`, default: `0`, description: "Mức độ ưu tiên xử lý event, ví dụ: 0 (normal), 1 (high), -1 (low). Có thể dùng để sắp xếp trong hàng đợi event.")
            * ` actorAgentId`: `string` (format: `uuid`, optional: `true`, description: "ID của Agent đã thực hiện hành động gây ra event này (nếu có). Liên kết tới Agent node.")
            * ` targetEntityId`: `string` (format: `uuid`, optional: `true`, description: "ID của thực thể chính mà event này liên quan đến (ví dụ: ProjectId, TaskId, TensionId). Giúp truy vấn event theo thực thể.")
            * ` targetEntityType`: `string` (optional: `true`, description: "Loại của targetEntityId (ví dụ: 'Project', 'Task').")
            * ` metadata`: `json` (optional: `true`, description: "Dữ liệu bổ sung, có cấu trúc, tùy theo từng eventType. Ví dụ, với 'TaskAssignedEvent', metadata có thể chứa { previousAssigneeId: '...', newAssigneeId: '...' }.")
        * **Phân loại (Subtypes) và `eventType` ví dụ** (Đây là một số loại chính, danh sách `eventType` cụ thể sẽ rất đa dạng):
            * **6.2.1. `SystemEvent`**: Sự kiện do hệ thống tự động tạo ra.
                *   *Ví dụ `eventType`*: `System.Backup.Completed`, `System.User.LoggedIn`, `System.Resource.LowWarning`
            * **6.2.2. `HumanInputEvent`**: Sự kiện từ input trực tiếp của con người.
                *   *Ví dụ `eventType`*: `UI.ButtonClicked`, `Form.Submitted`, `Manual.DataEntry`
            * **6.2.3. `RecognitionEvent`**: Sự kiện ghi nhận một thành tựu, đóng góp.
                *   *Ví dụ `eventType`*: `Recognition.Achievement.Noted`, `Recognition.Contribution.Acknowledged`
            * **6.2.4. `TensionEvent`**: Sự kiện ghi nhận một "tension" (vấn đề, cơ hội).
                *   *Ví dụ `eventType`*: `Tension.Detected`, `Tension.Status.Updated`, `Tension.Resolved`
            * **6.2.5. `ProjectEvent`**: Sự kiện liên quan đến vòng đời dự án.
                *   *Ví dụ `eventType`*: `Project.Created`, `Project.Status.Changed`, `Project.Milestone.Reached`, `Project.Budget.Exceeded`
            * **6.2.6. `TaskEvent`**: Sự kiện liên quan đến vòng đời nhiệm vụ.
                *   *Ví dụ `eventType`*: `Task.Created`, `Task.Assigned`, `Task.Status.Updated`, `Task.Completed`, `Task.DueDate.Changed`
            * **6.2.7. `WinEvent`**: Sự kiện đánh dấu một "WIN" - thành công quan trọng.
                *   *Ví dụ `eventType`*: `Win.Achieved`, `Win.Celebrated`
            * **6.2.8. `FailureEvent`**: Sự kiện ghi nhận một thất bại hoặc trở ngại.
                *   *Ví dụ `eventType`*: `Process.Failed`, `System.Error.Occurred`, `Project.Risk.Materialized`
            * **6.2.9. `LearningEvent`**: Sự kiện ghi nhận một bài học hoặc tri thức mới được tạo ra/cập nhật.
                *   *Ví dụ `eventType`*: `KnowledgeSnippet.Created`, `LessonLearned.Documented`, `Ontology.Term.Updated`
            * **6.2.10. `ResourceEvent`**: Sự kiện liên quan đến quản lý và phân bổ nguồn lực.
                *   *Ví dụ `eventType`*: `Resource.Requested`, `Resource.Allocated`, `Resource.Released`
        * **Ví dụ (cho một Event chung)**:
            `Event { eventId: "e45a01f4-2d3b-4c8e-91a0-72db601a5b67", eventType: "Task.Status.Updated", timestamp: "2025-06-10T10:05:00Z", creationDate: "2025-06-10T10:05:02Z", actorAgentId: "founder_01", targetEntityId: "task_001", targetEntityType: "Task", metadata: { previousStatus: "ToDo", newStatus: "InProgress" }, status: "New" }`

    *   **6.3. `Project`**: Đại diện cho một nỗ lực có mục tiêu, thời gian và nguồn lực cụ thể, được thực hiện để đạt được một kết quả hoặc `WIN` cụ thể.
        * **Mô tả**: Thường được tạo ra để giải quyết một hoặc nhiều `Tension`, nắm bắt `Opportunity`, hoặc thực hiện một sáng kiến chiến lược. Dự án có vòng đời xác định và tiêu thụ `Resource`.
        * **Thuộc tính chung**:
            * ` projectId`: `string` (format: `uuid`, primary_key: `true`, required: `true`, unique: `true`, description: "Mã định danh duy nhất toàn cầu cho project.")
            * ` name`: `string` (required: `true`, description: "Tên của dự án, ví dụ: 'Phát triển Ontology TRM-OS v3.2', 'Nghiên cứu Thị trường Q4'.")
            * ` goal`: `string` (required: `true`, description: "Mục tiêu chính, kết quả cụ thể mà dự án hướng tới.")
            * ` description`: `string` (optional: `true`, description: "Mô tả chi tiết hơn về dự án, bao gồm bối cảnh, lý do, và các thông tin liên quan khác.")
            * ` scope`: `string` (optional: `true`, format: `markdown`, description: "Phạm vi của dự án, bao gồm các hạng mục công việc chính (in-scope) và những gì không thuộc phạm vi (out-of-scope).")
            * ` status`: `string` (required: `true`, enum: [`Proposal`, `Planning`, `Active`, `OnHold`, `Completed`, `Cancelled`, `Failed`], default: `Proposal`, description: "Trạng thái hiện tại của dự án trong vòng đời của nó.")
            * ` priority`: `integer` (optional: `true`, default: `0`, description: "Mức độ ưu tiên của dự án (ví dụ: 0-Normal, 1-High, 2-Critical). Cao hơn nghĩa là ưu tiên hơn.")
            * ` creationDate`: `datetime` (format: `ISO8601`, required: `true`, readonly: `true`, default: "current_timestamp", description: "Ngày dự án được tạo trong hệ thống.")
            * ` lastModifiedDate`: `datetime` (format: `ISO8601`, required: `true`, readonly: `true`, default: "current_timestamp", auto_update: `true`, description: "Ngày dự án được cập nhật lần cuối.")
            * ` plannedStartDate`: `date` (format: `YYYY-MM-DD`, optional: `true`, description: "Ngày bắt đầu dự kiến.")
            * ` actualStartDate`: `date` (format: `YYYY-MM-DD`, optional: `true`, description: "Ngày bắt đầu thực tế.")
            * ` plannedEndDate`: `date` (format: `YYYY-MM-DD`, optional: `true`, description: "Ngày kết thúc dự kiến.")
            * ` actualEndDate`: `date` (format: `YYYY-MM-DD`, optional: `true`, description: "Ngày kết thúc thực tế.")
            * ` budget`: `float` (optional: `true`, description: "Ngân sách dự kiến cho dự án.")
            * ` budgetCurrency`: `string` (optional: `true`, default: `VND`, description: "Đơn vị tiền tệ của ngân sách, ví dụ: 'USD', 'VND'.")
            * ` actualCost`: `float` (optional: `true`, description: "Chi phí thực tế đã phát sinh.")
            * ` progressPercentage`: `integer` (optional: `true`, min: `0`, max: `100`, description: "Tỷ lệ phần trăm hoàn thành dự án, có thể được tính toán tự động hoặc cập nhật thủ công.")
            * ` ownerAgentId`: `string` (format: `uuid`, optional: `true`, description: "ID của Agent (thường là InternalAgent) chịu trách nhiệm chính cho dự án.")
            * ` stakeholderAgentIds`: `list[string]` (format: `uuid`, optional: `true`, description: "Danh sách ID của các Agent là bên liên quan quan trọng của dự án.")
            * ` relatedTensionIds`: `list[string]` (format: `uuid`, optional: `true`, description: "Danh sách ID của các Tension mà dự án này nhằm giải quyết.")
            * ` tags`: `list[string]` (optional: `true`, description: "Các từ khóa hoặc nhãn để phân loại, tìm kiếm dự án.")
        * **Phân loại (Subtypes)**: Các subtype có thể được sử dụng để thể hiện các giai đoạn hoặc loại dự án đặc thù, nhưng nhiều trường hợp `status` đã đủ. Ví dụ:
            * ` ProjectProposal`: Thường có `status: 'Proposal'`. Có thể có thêm các thuộc tính như `proposalSubmittedDate`, `proposalReviewerAgentId`.
            * ` StrategicInitiative`: Loại dự án mang tính chiến lược dài hạn.
        * **Ví dụ**:
            `Project { projectId: "prj_001", name: "Develop TRM-OS v3.2 Ontology", goal: "Hoàn thiện và chuẩn hóa ontology cốt lõi cho TRM-OS v3.2 để hỗ trợ phát triển AI Agent.", status: "Active", priority: 2, plannedStartDate: "2024-05-01", ownerAgentId: "founder_01", budget: 50000000, budgetCurrency: "VND", tags: ["ontology", "ai", "trm-os_v3.2"] }`

    *   **6.4. `Task`**: Một công việc hoặc hành động cụ thể, có thể phân công, cần thực hiện để đạt được một mục tiêu nhỏ hơn, thường là một phần của một `Project` hoặc một quy trình vận hành.
        * **Mô tả**: Đơn vị công việc có thể theo dõi, quản lý vòng đời, và thường có kết quả đầu ra (deliverable) cụ thể.
        * **Thuộc tính chung**:
            * ` taskId`: `string` (format: `uuid`, primary_key: `true`, required: `true`, unique: `true`, description: "Mã định danh duy nhất toàn cầu cho task.")
            * ` name`: `string` (required: `true`, description: "Tên hoặc tiêu đề ngắn gọn của công việc, ví dụ: 'Thiết kế API cho module User', 'Viết tài liệu hướng dẫn ABC'.")
            * ` description`: `string` (optional: `true`, format: `markdown`, description: "Mô tả chi tiết về công việc, bao gồm yêu cầu, mục tiêu, tiêu chí hoàn thành (Definition of Done).")
            * ` taskType`: `string` (optional: `true`, enum: [`Feature`, `Bug`, `Chore`, `Research`, `Documentation`, `Meeting`], description: "Phân loại công việc, giúp lọc và báo cáo.")
            * ` status`: `string` (required: `true`, enum: [`ToDo`, `InProgress`, `Blocked`, `InReview`, `Done`, `Cancelled`, `Backlog`], default: `ToDo`, description: "Trạng thái hiện tại của công việc trong quy trình.")
            * ` priority`: `integer` (optional: `true`, default: `0`, description: "Mức độ ưu tiên của công việc (ví dụ: 0-Normal, 1-High, 2-Urgent). Cao hơn nghĩa là ưu tiên hơn.")
            * ` creationDate`: `datetime` (format: `ISO8601`, required: `true`, readonly: `true`, default: "current_timestamp", description: "Ngày công việc được tạo.")
            * ` lastModifiedDate`: `datetime` (format: `ISO8601`, required: `true`, readonly: `true`, default: "current_timestamp", auto_update: `true`, description: "Ngày công việc được cập nhật lần cuối.")
            * ` assigneeAgentId`: `string` (format: `uuid`, optional: `true`, description: "ID của Agent được giao thực hiện công việc này.")
            * ` reporterAgentId`: `string` (format: `uuid`, optional: `true`, description: "ID của Agent đã tạo hoặc báo cáo công việc này.")
            * ` projectId`: `string` (format: `uuid`, optional: `true`, description: "ID của Project mà công việc này thuộc về (nếu có). Giúp nhóm các task theo project.")
            * ` startDate`: `date` (format: `YYYY-MM-DD`, optional: `true`, description: "Ngày bắt đầu dự kiến hoặc thực tế của công việc.")
            * ` dueDate`: `date` (format: `YYYY-MM-DD`, optional: `true`, description: "Hạn chót (deadline) cần hoàn thành công việc.")
            * ` actualCompletionDate`: `date` (format: `YYYY-MM-DD`, optional: `true`, description: "Ngày công việc thực sự được hoàn thành.")
            * ` effortEstimate`: `float` (optional: `true`, description: "Ước tính công sức hoặc thời gian cần thiết để hoàn thành công việc.")
            * ` effortUnit`: `string` (optional: `true`, enum: [`hours`, `days`, `story_points`], default: `hours`, description: "Đơn vị của effortEstimate.")
            * ` dependencies`: `list[string]` (format: `taskId`, optional: `true`, description: "Danh sách các taskId khác mà công việc này phụ thuộc vào (phải hoàn thành trước).")
            * ` subTasks`: `list[string]` (format: `taskId`, optional: `true`, description: "Danh sách các taskId con của công việc này (nếu công việc này được chia nhỏ).")
            * ` tags`: `list[string]` (optional: `true`, description: "Các từ khóa hoặc nhãn để phân loại, tìm kiếm công việc.")
        * **Phân loại (Subtypes)**: Thường được xử lý qua `taskType` và `status`. Nếu cần cấu trúc phức tạp hơn, có thể định nghĩa subtype.
            * ` RecurringTask`: Có thể có thêm thuộc tính như `recurrenceRule` (e.g., cron-like string), `nextDueDate`.
        * **Ví dụ**:
            `Task { taskId: "task_b3f2a1c8", name: "Define Core Classes for Ontology v3.2", description: "Identify and define all core entity classes, their properties, and relationships for the TRM-OS v3.2 ontology.", taskType: "Feature", status: "InProgress", priority: 1, assigneeAgentId: "dev_agent_002", projectId: "prj_001", dueDate: "2025-06-15", effortEstimate: 16, effortUnit: "hours", tags: ["ontology", "core-model"] }`

    *   **6.5. `Resource`**: Các yếu tố đầu vào, tài sản, hoặc năng lực có thể được sử dụng, tiêu thụ, hoặc phân bổ để thực hiện `Task`, `Project`, hoặc các hoạt động khác của tổ chức.
        * **Mô tả**: Bao gồm tài chính, tri thức, con người (thời gian, kỹ năng), công cụ, thiết bị, không gian, v.v. Việc quản lý `Resource` hiệu quả là rất quan trọng.
        * **Thuộc tính chung**:
            * ` resourceId`: `string` (format: `uuid`, primary_key: `true`, required: `true`, unique: `true`, description: "Mã định danh duy nhất toàn cầu cho resource.")
            * ` name`: `string` (required: `true`, description: "Tên của nguồn lực, ví dụ: 'Ngân sách Marketing Q3', 'Phòng họp A101', 'Chuyên gia AI Backend'.")
            * ` resourceType`: `string` (required: `true`, enum: [`Financial`, `Knowledge`, `Human`, `Tool`, `Equipment`, `Space`, `Material`, `Other`], description: "Phân loại chính của nguồn lực.")
            * ` description`: `string` (optional: `true`, format: `markdown`, description: "Mô tả chi tiết về nguồn lực, đặc tính, thông số kỹ thuật (nếu có).")
            * ` status`: `string` (required: `true`, enum: [`Available`, `InUse`, `Allocated`, `Reserved`, `Depleted`, `Maintenance`, `Unavailable`], default: `Available`, description: "Trạng thái hiện tại của nguồn lực.")
            * ` quantity`: `float` (optional: `true`, description: "Số lượng hiện có của nguồn lực. Nếu là nguồn lực không đếm được (ví dụ: một tài liệu), có thể để trống hoặc 1.")
            * ` unitOfMeasure`: `string` (optional: `true`, description: "Đơn vị đo lường cho quantity, ví dụ: 'USD', 'hours', 'licenses', 'items', 'sqm'.")
            * ` costPerUnit`: `float` (optional: `true`, description: "Chi phí cho mỗi đơn vị của nguồn lực (nếu có).")
            * ` currency`: `string` (optional: `true`, default: `VND`, description: "Đơn vị tiền tệ cho costPerUnit.")
            * ` ownerAgentId`: `string` (format: `uuid`, optional: `true`, description: "ID của Agent quản lý hoặc sở hữu nguồn lực này.")
            * ` location`: `string` (optional: `true`, description: "Vị trí vật lý hoặc logic của nguồn lực, ví dụ: 'Kho A', 'Server XYZ', URL đến tài liệu.")
            * ` creationDate`: `datetime` (format: `ISO8601`, required: `true`, readonly: `true`, default: "current_timestamp", description: "Ngày nguồn lực được ghi nhận.")
            * ` lastModifiedDate`: `datetime` (format: `ISO8601`, required: `true`, readonly: `true`, default: "current_timestamp", auto_update: `true`, description: "Ngày thông tin nguồn lực được cập nhật lần cuối.")
            * ` tags`: `list[string]` (optional: `true`, description: "Các từ khóa hoặc nhãn để phân loại, tìm kiếm nguồn lực.")
        * **Phân loại (Subtypes) và thuộc tính ví dụ** (dựa trên `resourceType`):
            * **6.5.1. `FinancialResource`** (`resourceType: 'Financial'`)
                * ` balance`: `float` (description: "Số dư hiện tại cho nguồn lực tài chính này, ví dụ: quỹ dự án.")
                * ` budgetCode`: `string` (optional: `true`, description: "Mã ngân sách liên quan.")
            * **6.5.2. `KnowledgeResource`** (`resourceType: 'Knowledge'`)
                * ` format`: `string` (optional: `true`, enum: [`Document`, `Database`, `API`, `Model`, `Patent`, `Course`], description: "Định dạng của tài sản tri thức.")
                * ` version`: `string` (optional: `true`, description: "Phiên bản của tài sản tri thức.")
                * ` accessUrl`: `string` (format: `url`, optional: `true`, description: "URL để truy cập tài sản tri thức.")
                * ` relatedKnowledgeSnippetIds`: `list[string]` (format: `uuid`, optional: `true`)
            * **6.5.3. `HumanResource`** (`resourceType: 'Human'`) - Đại diện cho năng lực, kỹ năng, hoặc thời gian của một Agent cụ thể.
                * ` agentId`: `string` (format: `uuid`, required: `true`, description: "ID của Agent liên quan.")
                * ` skillSet`: `list[string]` (optional: `true`, description: "Danh sách các kỹ năng chính.")
                * ` availabilitySchedule`: `json` (optional: `true`, description: "Lịch làm việc hoặc tính sẵn sàng.")
            * **6.5.4. `ToolResource`** (`resourceType: 'Tool'`)
                * ` toolType`: `string` (optional: `true`, enum: [`Software`, `Hardware`, `Service`], description: "Loại công cụ.")
                * ` licenseKey`: `string` (optional: `true`, description: "Mã bản quyền (nếu là software).")
                * ` vendor`: `string` (optional: `true`, description: "Nhà cung cấp.")
            * **6.5.5. `EquipmentResource`** (`resourceType: 'Equipment'`)
                * ` serialNumber`: `string` (optional: `true`, unique: `true`)
                * ` purchaseDate`: `date` (optional: `true`)
                * ` warrantyEndDate`: `date` (optional: `true`)
            * **6.5.6. `SpaceResource`** (`resourceType: 'Space'`)
                * ` capacity`: `integer` (optional: `true`, description: "Sức chứa, ví dụ: số người cho phòng họp.")
                * ` amenities`: `list[string]` (optional: `true`, description: "Các tiện nghi có sẵn.")
        * **Ví dụ**:
            `KnowledgeResource { resourceId: "k_res_001", name: "Ontology Design Best Practices v1.2", resourceType: "Knowledge", status: "Available", description: "Tài liệu hướng dẫn các quy tắc tốt nhất khi thiết kế ontology.", format: "Document", version: "1.2", accessUrl: "https://docs.trm.os/ontology/best-practices_v1.2.pdf", ownerAgentId: "knowledge_manager_01", tags: ["ontology", "design", "documentation"] }`
            `FinancialResource { resourceId: "fin_res_002", name: "Q3 Project Alpha Budget", resourceType: "Financial", status: "Allocated", balance: 50000000, unitOfMeasure: "VND", budgetCode: "PROJ_ALPHA_Q3_2025", ownerAgentId: "finance_dept_01"}`

    *   **6.6. `Tension`**: Sự cảm nhận về một khoảng cách (gap) giữa trạng thái thực tế hiện tại và một trạng thái tiềm năng hoặc mong muốn tốt đẹp hơn. Đây là khái niệm trung tâm trong TRM, là động lực cho sự thay đổi và phát triển.
        * **Mô tả**: `Tension` có thể là một vấn đề cần giải quyết, một rủi ro cần giảm thiểu, một cơ hội cần nắm bắt, một ý tưởng cần khám phá, hoặc một sự không rõ ràng cần làm sáng tỏ. `Tension` là đầu vào chính để tạo ra `ProjectProposal` hoặc các hành động khác.
        * **Thuộc tính chung**:
            * ` tensionId`: `string` (format: `uuid`, primary_key: `true`, required: `true`, unique: `true`, description: "Mã định danh duy nhất toàn cầu cho tension.")
            * ` title`: `string` (required: `true`, description: "Tiêu đề ngắn gọn, tóm tắt bản chất của tension.")
            * ` tensionType`: `string` (required: `true`, enum: [`Problem`, `Opportunity`, `Risk`, `Idea`, `Question`, `Concern`], description: "Phân loại tension để dễ quản lý và xử lý.")
            * ` description`: `string` (required: `true`, format: `markdown`, description: "Mô tả chi tiết về tension, bao gồm bối cảnh, các quan sát cụ thể, và tại sao nó lại là một tension.")
            * ` currentState`: `string` (optional: `true`, format: `markdown`, description: "Mô tả trạng thái thực tế hiện tại liên quan đến tension.")
            * ` desiredState`: `string` (optional: `true`, format: `markdown`, description: "Mô tả trạng thái mong muốn hoặc tiềm năng nếu tension được giải quyết/theo đuổi.")
            * ` impactAssessment`: `string` (optional: `true`, format: `markdown`, description: "Đánh giá về tác động tiềm ẩn nếu tension không được xử lý (đối với Problem/Risk) hoặc nếu được theo đuổi (đối với Opportunity/Idea). Có thể bao gồm cả mức độ khẩn cấp.")
            * ` source`: `string` (optional: `true`, description: "Nguồn gốc phát hiện hoặc người/hệ thống ghi nhận tension, ví dụ: 'FounderInput', 'CustomerFeedback', 'DataSensingAgent', 'RetrospectiveMeeting'.")
            * ` priority`: `integer` (optional: `true`, default: `0`, description: "Mức độ ưu tiên xử lý tension (ví dụ: 0-Normal, 1-High, 2-Critical). Cao hơn nghĩa là ưu tiên hơn.")
            * ` status`: `string` (required: `true`, enum: [`Open`, `UnderReview`, `Accepted`, `InProgress`, `OnHold`, `Resolved`, `Rejected`, `Closed`, `Archived`], default: `Open`, description: "Trạng thái của tension trong vòng đời xử lý của nó.")
            * ` creationDate`: `datetime` (format: `ISO8601`, required: `true`, readonly: `true`, default: "current_timestamp", description: "Ngày tension được tạo.")
            * ` lastModifiedDate`: `datetime` (format: `ISO8601`, required: `true`, readonly: `true`, default: "current_timestamp", auto_update: `true`, description: "Ngày tension được cập nhật lần cuối.")
            * ` resolutionDate`: `datetime` (format: `ISO8601`, optional: `true`, description: "Ngày tension được giải quyết hoặc đóng lại.")
            * ` reporterAgentId`: `string` (format: `uuid`, optional: `true`, description: "ID của Agent đã báo cáo hoặc tạo ra tension này.")
            * ` ownerAgentId`: `string` (format: `uuid`, optional: `true`, description: "ID của Agent chịu trách nhiệm chính trong việc xử lý hoặc theo dõi tension này.")
            * ` relatedProjectIds`: `list[string]` (format: `uuid`, optional: `true`, description: "Danh sách ID của các Project được tạo ra để giải quyết tension này.")
            * ` relatedKnowledgeSnippetIds`: `list[string]` (format: `uuid`, optional: `true`, description: "Danh sách ID của các KnowledgeSnippet liên quan đến tension này.")
            * ` tags`: `list[string]` (optional: `true`, description: "Các từ khóa hoặc nhãn để phân loại, tìm kiếm tension.")
        * **Ví dụ**:
            `Tension { tensionId: "ten_c2a1b8e3", title: "Ontology thiếu chi tiết cho AI Agent", tensionType: "Problem", description: "Ontology hiện tại (v3.1) chưa đủ chi tiết về các thuộc tính, mối quan hệ và ràng buộc của các core entity. Điều này gây khó khăn cho AI Agent trong việc hiểu và tự động hóa các quy trình nghiệp vụ một cách chính xác.", currentState: "Ontology v3.1 có định nghĩa cơ bản nhưng thiếu metadata và ví dụ cụ thể.", desiredState: "Ontology v3.2 với định nghĩa chi tiết, đầy đủ constraints, data types, và ví dụ cho từng entity, sẵn sàng cho code generation.", impactAssessment: "Cao - Ảnh hưởng trực tiếp đến khả năng phát triển AI Agent hiệu quả và tiến độ dự án TRM-OS.", source: "FounderReviewSession", priority: 2, status: "Accepted", reporterAgentId: "founder_01", ownerAgentId: "ontology_lead_agent", creationDate: "2025-05-15T09:00:00Z", tags: ["ontology", "ai-enablement", "core-system"] }`

    *   **6.7. `Recognition`**: Sự ghi nhận và đánh giá tích cực đối với một hành động, nỗ lực, kết quả, đóng góp, hoặc phẩm chất đáng khen ngợi của một `Agent` hoặc một nhóm `Agent`.
        * **Mô tả**: `Recognition` là một yếu tố quan trọng trong văn hóa TRM, nhằm khuyến khích hành vi tích cực, củng cố giá trị cốt lõi, và là nguồn thông tin đầu vào để tạo ra các `WinEvent` hoặc các dạng `LearningEvent`. Nó giúp làm nổi bật những đóng góp và thành tựu, từ đó thúc đẩy động lực và sự gắn kết.
        * **Thuộc tính chung**:
            * ` recognitionId`: `string` (format: `uuid`, primary_key: `true`, required: `true`, unique: `true`, description: "Mã định danh duy nhất toàn cầu cho recognition.")
            * ` recognitionType`: `string` (required: `true`, enum: [`Achievement`, `Effort`, `Contribution`, `Behavior`, `SkillDemonstration`, `MilestoneReached`, `ValueAlignment`], default: `Achievement`, description: "Phân loại sự công nhận.")
            * ` description`: `string` (required: `true`, format: `markdown`, description: "Mô tả chi tiết về hành động, kết quả, hoặc phẩm chất được công nhận. Nên cụ thể và nêu bật được giá trị.")
            * ` recipientAgentId`: `string` (format: `uuid`, required: `true`, description: "ID của Agent (hoặc group Agent) nhận được sự công nhận.")
            * ` giverAgentId`: `string` (format: `uuid`, optional: `true`, description: "ID của Agent (hoặc system Agent) đưa ra sự công nhận. Có thể trống nếu là tự công nhận hoặc từ một nguồn không xác định.")
            * ` timestamp`: `datetime` (format: `ISO8601`, required: `true`, description: "Thời điểm hành động/kết quả được công nhận diễn ra hoặc được ghi nhận.")
            * ` creationDate`: `datetime` (format: `ISO8601`, required: `true`, readonly: `true`, default: "current_timestamp", description: "Ngày recognition này được tạo trong hệ thống.")
            * ` context`: `string` (optional: `true`, format: `markdown`, description: "Bối cảnh cụ thể của sự công nhận, ví dụ: tên dự án, mã task, tên sự kiện liên quan.")
            * ` value`: `float` (optional: `true`, description: "Giá trị định lượng của sự công nhận nếu có (ví dụ: điểm thưởng, giá trị tiền tệ của một giải thưởng). Mặc định là 0 nếu không áp dụng.")
            * ` currency`: `string` (optional: `true`, default: `VND`, description: "Đơn vị tiền tệ cho `value` nếu có.")
            * ` relatedEventId`: `string` (format: `uuid`, optional: `true`, description: "ID của Event liên quan trực tiếp đến sự công nhận này (ví dụ: `TaskCompletionEvent`).")
            * ` relatedProjectId`: `string` (format: `uuid`, optional: `true`, description: "ID của Project mà sự công nhận này liên quan đến.")
            * ` relatedTaskId`: `string` (format: `uuid`, optional: `true`, description: "ID của Task mà sự công nhận này liên quan đến.")
            * ` tags`: `list[string]` (optional: `true`, description: "Các từ khóa hoặc nhãn để phân loại, tìm kiếm recognition.")
        * **Ví dụ**:
            `Recognition { recognitionId: "recog_f5b2a1c8", recognitionType: "MilestoneReached", description: "Agent 'dev_agent_002' đã hoàn thành xuất sắc Task 'Define Core Classes for Ontology v3.2' (task_b3f2a1c8) thuộc Project 'Ontology Enhancement Q2' (prj_001) trước thời hạn 2 ngày, với chất lượng định nghĩa rất cao, tạo tiền đề tốt cho giai đoạn phát triển AI Agent.", recipientAgentId: "dev_agent_002", giverAgentId: "project_manager_001", timestamp: "2025-06-13T15:00:00Z", creationDate: "2025-06-13T15:05:00Z", context: "Hoàn thành Task task_b3f2a1c8 trong Project prj_001", relatedProjectId: "prj_001", relatedTaskId: "task_b3f2a1c8", tags: ["ontology", "excellence", "early-completion"] }`

    *   **6.8. `WIN`**: Một thành tựu, kết quả đột phá, hoặc một cột mốc quan trọng đã đạt được, mang lại giá trị và tác động tích cực đáng kể, đóng góp vào việc thực hiện sứ mệnh hoặc mục tiêu chiến lược của TRM.
        * **Mô tả**: `WIN` là đỉnh cao của chu trình `Recognition` -> `Event` -> `WIN`. Nó không chỉ là hoàn thành một công việc, mà là tạo ra một sự thay đổi tích cực có ý nghĩa. `WIN` thường được tổng hợp từ nhiều `Recognition` và có thể liên quan đến việc hoàn thành một `Project` lớn, giải quyết một `Tension` cốt lõi, hoặc đạt được một mục tiêu chiến lược.
        * **Thuộc tính chung**:
            * ` winId`: `string` (format: `uuid`, primary_key: `true`, required: `true`, unique: `true`, description: "Mã định danh duy nhất toàn cầu cho WIN.")
            * ` title`: `string` (required: `true`, description: "Tiêu đề của WIN, ngắn gọn và truyền cảm hứng.")
            * ` winType`: `string` (required: `true`, enum: [`StrategicMilestone`, `ProductLaunch`, `ServiceImprovement`, `ProcessInnovation`, `TeamAchievement`, `SocietalImpact`, `CapabilityDevelopment`, `PartnershipSecured`, `ProblemSolved`], default: `StrategicMilestone`, description: "Phân loại WIN để dễ dàng tổng hợp và báo cáo.")
            * ` description`: `string` (required: `true`, format: `markdown`, description: "Mô tả chi tiết về WIN: nó là gì, tại sao nó quan trọng, nó giải quyết vấn đề gì hoặc tạo ra cơ hội gì, và tác động của nó như thế nào.")
            * ` timestamp`: `datetime` (format: `ISO8601`, required: `true`, description: "Thời điểm WIN được chính thức công nhận hoặc hoàn thành.")
            * ` creationDate`: `datetime` (format: `ISO8601`, required: `true`, readonly: `true`, default: "current_timestamp", description: "Ngày WIN này được tạo trong hệ thống.")
            * ` impactLevel`: `integer` (required: `true`, default: `3`, description: "Đánh giá mức độ tác động của WIN (ví dụ: 1-Low, 2-Moderate, 3-Significant, 4-High, 5-Transformational). Cao hơn nghĩa là tác động lớn hơn.")
            * ` achievedByAgentIds`: `list[string]` (format: `uuid`, optional: `true`, description: "Danh sách ID của các Agent hoặc nhóm Agent chính đã đóng góp vào việc đạt được WIN này.")
            * ` relatedRecognitionIds`: `list[string]` (format: `uuid`, optional: `true`, description: "Danh sách ID của các Recognition cụ thể đã đóng góp hoặc dẫn đến WIN này.")
            * ` relatedProjectIds`: `list[string]` (format: `uuid`, optional: `true`, description: "Danh sách ID của các Project liên quan trực tiếp đến việc tạo ra WIN này.")
            * ` relatedTensionIds`: `list[string]` (format: `uuid`, optional: `true`, description: "Danh sách ID của các Tension đã được giải quyết hoặc thúc đẩy bởi WIN này.")
            * ` evidenceUrls`: `list[string]` (format: `url`, optional: `true`, description: "Danh sách các URL đến bằng chứng cụ thể minh chứng cho WIN (ví dụ: báo cáo, sản phẩm, demo, bài báo).")
            * ` lessonsLearned`: `string` (optional: `true`, format: `markdown`, description: "Những bài học kinh nghiệm quan trọng rút ra từ quá trình đạt được WIN này.")
            * ` nextSteps`: `string` (optional: `true`, format: `markdown`, description: "Các hành động hoặc định hướng tiếp theo được kích hoạt hoặc đề xuất bởi WIN này.")
            * ` tags`: `list[string]` (optional: `true`, description: "Các từ khóa hoặc nhãn để phân loại, tìm kiếm WIN.")
        * **Ví dụ**:
            `WIN { winId: "win_e7d2c1b8", title: "TRM-OS Ontology V3.2 Hoàn Chỉnh và Sẵn Sàng Cho AI", winType: "StrategicMilestone", description: "Phiên bản 3.2 của TRM Internal Ontology đã được hoàn thiện, với đầy đủ các định nghĩa entity, thuộc tính, ràng buộc và ví dụ chi tiết. Ontology này cung cấp một nền tảng vững chắc, cho phép các AI Agent hiểu sâu sắc ngữ cảnh hoạt động của TRM và tự động hóa các tác vụ phức tạp, mở ra kỷ nguyên mới cho TRM-OS.", timestamp: "2025-07-15T10:00:00Z", creationDate: "2025-07-15T10:05:00Z", impactLevel: 5, achievedByAgentIds: ["ontology_lead_agent", "ai_strategy_agent"], relatedRecognitionIds: ["recog_f5b2a1c8", "recog_a1c8e3f5"], relatedProjectIds: ["prj_001"], relatedTensionIds: ["ten_c2a1b8e3"], evidenceUrls: ["https://docs.trm.os/ontology/v3.2/final_spec.pdf", "https://demo.trm.os/ai_ontology_integration_showcase"], lessonsLearned: "Việc đầu tư vào một ontology chi tiết và rõ ràng là cực kỳ quan trọng cho sự thành công của các hệ thống dựa trên AI. Sự hợp tác chặt chẽ giữa các chuyên gia miền và đội ngũ AI là chìa khóa.", nextSteps: "Triển khai AI Agent đầu tiên sử dụng Ontology V3.2 để tự động hóa quy trình xử lý Tension. Bắt đầu phát triển các module code generation từ ontology.", tags: ["ontology", "ai-platform", "strategic-win", "v3.2"] }`

    *   **6.9. `KnowledgeAsset`**: Đại diện cho các tài sản tri thức trong tổ chức. Đây là một lớp trừu tượng, bao gồm các loại tài sản tri thức cụ thể.
        * **Mô tả**: Bất kỳ đơn vị tri thức nào có giá trị, có thể được lưu trữ, quản lý, chia sẻ và tái sử dụng. TRM-OS coi tri thức là một dạng tài sản chiến lược, là "DNA" và "vũ khí bí mật" của tổ chức.
        * **Phân loại (Subtypes) quan trọng:**
            * ` ConceptualFramework`: Một hệ thống các ý tưởng, khái niệm, nguyên tắc và niềm tin cốt lõi định hình cách TRM hiểu và tương tác với thế giới. Ví dụ: Chính triết lý "Recognition → Event → WIN", "Mô hình Vận hành Lượng tử". Chúng là nền tảng cho tư duy chiến lược và văn hóa tổ chức.
            * ` Methodology`: Một tập hợp các phương pháp, quy trình, công cụ và kỹ thuật đã được kiểm chứng để giải quyết các loại vấn đề cụ thể hoặc đạt được các mục tiêu cụ thể. Ví dụ: Quy trình 6 bước vận hành, phương pháp giải quyết `Tension`.
            * ` KnowledgeSnippet`: Đơn vị tri thức nhỏ, cô đọng, thường được trích xuất từ tài liệu hoặc tương tác, có thể kèm embedding vector để tìm kiếm ngữ nghĩa.
            * ` DataAsset`: Các bộ dữ liệu có cấu trúc hoặc bán cấu trúc quan trọng, ví dụ: kết quả phân tích thị trường, cơ sở dữ liệu khách hàng (nếu có), log hệ thống đã được xử lý.
        * **Thuộc tính chung (có thể có thêm tùy subtype)**:
            * ` assetId`: `string` (format: `uuid`, primary_key: `true`, required: `true`, unique: `true`, description: "Mã định danh duy nhất toàn cầu cho tài sản tri thức.")
            * ` name`: `string` (required: `true`, description: "Tên của tài sản tri thức, ví dụ: 'TRM Operating Model v2', 'Customer Persona Analysis Q1'.")
            * ` assetType`: `string` (required: `true`, enum: [`ConceptualFramework`, `Methodology`, `KnowledgeSnippet`, `DataAsset`, `ProcessDefinition`, `Policy`, `Guideline`, `Template`, `TrainingMaterial`, `ResearchReport`, `CaseStudy`, `IntellectualProperty`, `SystemDocumentation`, `UserManual`, `LearningModule`, `OntologyDefinition`, `Other`], description: "Phân loại chính của tài sản tri thức.")
            * ` description`: `string` (optional: `true`, format: `markdown`, description: "Mô tả chi tiết về tài sản tri thức, mục đích, nội dung chính, và phạm vi áp dụng.")
            * ` version`: `string` (optional: `true`, description: "Phiên bản của tài sản tri thức, ví dụ: '1.0', '2025-Q2', 'alpha'.")
            * ` status`: `string` (required: `true`, enum: [`Draft`, `UnderReview`, `Published`, `Active`, `Experimental`, `Archived`, `Deprecated`, `Obsolete`], default: `Draft`, description: "Trạng thái hiện tại của tài sản tri thức trong vòng đời của nó.")
            * ` accessLevel`: `string` (required: `true`, enum: [`Public`, `Internal`, `TeamRestricted`, `RoleRestricted`, `Confidential`, `HighlyConfidential`], default: `Internal`, description: "Mức độ cho phép truy cập tài sản tri thức.")
            * ` ownerAgentId`: `string` (format: `uuid`, optional: `true`, description: "ID của Agent hoặc nhóm Agent chịu trách nhiệm chính về việc tạo, duy trì và cập nhật tài sản tri thức này.")
            * ` source`: `string` (optional: `true`, description: "Nguồn gốc hoặc xuất xứ của tài sản tri thức, ví dụ: 'Founder's Insight', 'Project Phoenix Debrief', 'External Research Paper by XYZ', 'SystemLogAnalysis', 'UserInterview'.")
            * ` creationDate`: `datetime` (format: `ISO8601`, required: `true`, readonly: `true`, default: "current_timestamp", description: "Ngày tài sản tri thức được tạo hoặc ghi nhận lần đầu trong hệ thống.")
            * ` lastModifiedDate`: `datetime` (format: `ISO8601`, required: `true`, readonly: `true`, default: "current_timestamp", auto_update: `true`, description: "Ngày thông tin tài sản tri thức được cập nhật lần cuối.")
            * ` publishedDate`: `datetime` (format: `ISO8601`, optional: `true`, description: "Ngày tài sản tri thức được xuất bản chính thức (nếu có). ")
            * ` validFrom`: `datetime` (format: `ISO8601`, optional: `true`, description: "Ngày tài sản tri thức bắt đầu có hiệu lực hoặc được áp dụng (nếu có). Mặc định là ngày tạo hoặc ngày xuất bản.")
            * ` validTo`: `datetime` (format: `ISO8601`, optional: `true`, description: "Ngày tài sản tri thức hết hiệu lực hoặc không còn được áp dụng (nếu có). Thường dùng cho policy, guideline.")
            * ` relatedTeamId`: `string` (format: `uuid`, optional: `true`, description: "ID của Đội ngũ (Team) liên quan chính hoặc sở hữu tài sản tri thức này.")
            * ` tags`: `list[string]` (optional: `true`, description: "Các từ khóa, chủ đề hoặc nhãn giúp phân loại, tìm kiếm và liên kết tài sản tri thức. Thay thế cho 'keywords' cũ.")
            * ` license`: `string` (optional: `true`, description: "Thông tin bản quyền hoặc giấy phép sử dụng của tài sản tri thức (ví dụ: 'CC BY-SA 4.0', 'Proprietary', 'MIT License').")
            * ` language`: `string` (optional: `true`, default: `vi`, description: "Ngôn ngữ chính của tài sản tri thức (sử dụng mã ISO 639-1, ví dụ: 'vi' cho tiếng Việt, 'en' cho tiếng Anh).")
            * ` relatedAssetIds`: `list[string]` (format: `uuid`, optional: `true`, description: "Danh sách ID của các tài sản tri thức khác có liên quan (ví dụ: phiên bản trước, tài liệu bổ sung, nguồn tham khảo).")
        * **Ví dụ**:
            * ` ConceptualFramework {assetId: "cf_001", name: "TRM Recognition Philosophy", assetType: "ConceptualFramework", version: "1.0", description: "The core philosophy of Recognition -> Event -> WIN."}`
            * ` Methodology {assetId: "meth_001", name: "TRM-OS 6-Step Operating Loop", assetType: "Methodology", description: "The core feedback loop for organizational operation."}`

    *   **6.10. `KnowledgeSnippet` (Subtype của `KnowledgeAsset`)**: Đơn vị tri thức nhỏ, cô đọng, thường được trích xuất từ tài liệu hoặc tương tác.
        * **Mô tả**: Được thiết kế để AI agent dễ dàng truy cập, hiểu và sử dụng. Mỗi snippet tập trung vào một ý tưởng, thông tin hoặc hướng dẫn cụ thể. Có thể được nhúng (embedded) để tìm kiếm ngữ nghĩa.
        * **Thuộc tính (ngoài các thuộc tính kế thừa từ `KnowledgeAsset`)**:
            * ` content`: `string` (required: `true`, description: "Nội dung chính của snippet tri thức. Có thể là văn bản, code, JSON, XML, v.v., tùy thuộc vào `contentType`.")
            * ` contentType`: `string` (required: `true`, enum: [`text/plain`, `text/markdown`, `application/json`, `application/xml`, `text/x-python`, `text/x-javascript`, `text/x-typescript`, `text/x-cypher`, `text/html`, `text/css`, `text/csv`, `image/png`, `image/jpeg`, `image/gif`, `image/svg+xml`, `application/pdf`, `application/octet-stream`, `application/vnd.openai.embedding.v1+json`, `Other`], default: `text/plain`, description: "Định dạng MIME của nội dung snippet. Quan trọng cho việc hiển thị, xử lý và nhúng vector.")
            * ` vectorEmbedding`: `list[float]` (optional: `true`, description: "Vector nhúng ngữ nghĩa của `content` (hoặc một phần của nó), được tạo và lưu trữ trong một cơ sở dữ liệu vector (ví dụ: Supabase Vector). Dùng cho tìm kiếm tương đồng và các tác vụ AI khác. Kích thước vector phụ thuộc vào model embedding được sử dụng.")
            * ` extractedFromAssetId`: `string` (format: `uuid`, optional: `true`, description: "ID của `KnowledgeAsset` (ví dụ: một tài liệu, báo cáo, trang web đã lưu) mà snippet này được trích xuất hoặc có nguồn gốc từ đó.")
            * ` sourceUrl`: `string` (format: `url`, optional: `true`, description: "URL cụ thể trỏ đến nguồn gốc bên ngoài của snippet, nếu có (ví dụ: link đến một bài viết blog, một file cụ thể trong GDrive, một commit trên GitHub).")
            * ` sourceDescription`: `string` (optional: `true`, format: `markdown`, description: "Mô tả ngắn gọn về nguồn gốc nếu không có `extractedFromAssetId` hoặc `sourceUrl` cụ thể, ví dụ: 'Ghi chú cuộc họp Dự án Alpha ngày YYYY-MM-DD', 'Trích từ email của John Doe về vấn đề X', 'Ý tưởng từ buổi brainstorm nhóm Marketing'. Kế thừa `source` từ `KnowledgeAsset` nhưng có thể chi tiết hơn cho snippet.")
            * ` confidenceScore`: `float` (optional: `true`, minimum: `0.0`, maximum: `1.0`, description: "Điểm tin cậy (0.0 đến 1.0) về tính chính xác hoặc độ liên quan của thông tin trong snippet, đặc biệt hữu ích nếu snippet được trích xuất hoặc tạo tự động bởi AI.")
            * ` processingStatus`: `string` (optional: `true`, enum: [`Raw`, `Cleaned`, `Verified`, `Summarized`, `Embedded`, `RequiresReview`, `ProcessingFailed`], default: `Raw`, description: "Trạng thái xử lý của snippet, ví dụ: đã được làm sạch, xác minh, tóm tắt, nhúng vector, hoặc cần review.")
            * ` usageCount`: `integer` (optional: `true`, default: `0`, description: "Số lần snippet này được truy cập, sử dụng hoặc tham chiếu trong các tác vụ hoặc bởi các agent.")
            * ` lastAccessedDate`: `datetime` (format: `ISO8601`, optional: `true`, description: "Ngày giờ snippet này được truy cập hoặc sử dụng lần cuối.")
            * ` relatedTensionIds`: `list[string]` (format: `uuid`, optional: `true`, description: "Danh sách ID của các `Tension` mà snippet này có thể giúp giải quyết, cung cấp thông tin liên quan hoặc là một phần của bối cảnh.")
            * ` relatedProjectIds`: `list[string]` (format: `uuid`, optional: `true`, description: "Danh sách ID của các `Project` mà snippet này liên quan, hỗ trợ hoặc được tạo ra trong khuôn khổ dự án đó.")
            * ` relatedEventIds`: `list[string]` (format: `uuid`, optional: `true`, description: "Danh sách ID của các `Event` mà snippet này có thể liên quan (ví dụ: snippet được tạo ra từ một event cụ thể).")
        * **Ví dụ**: 
            ```yamlyaml
            KnowledgeSnippet:
              # Thuộc tính kế thừa từ KnowledgeAsset
              assetId: "ks_8b1f2c19-51a7-4a8c-9cb0-f8d7e6a2b3c4"
              name: "Cypher Query for Active Projects with Start Dates"
              assetType: "KnowledgeSnippet" # Bắt buộc là KnowledgeSnippet
              description: "Một câu lệnh Cypher để truy vấn tất cả các dự án đang hoạt động (status 'Active') và trả về ID, tên, và ngày bắt đầu của chúng."
              version: "1.1"
              status: "Published"
              accessLevel: "TeamRestricted"
              ownerAgentId: "agent_dev_lead_007"
              source: "Internal Wiki - Neo4j Best Practices"
              creationDate: "2024-06-10T09:30:00Z"
              lastModifiedDate: "2024-06-11T14:15:00Z"
              publishedDate: "2024-06-11T15:00:00Z"
              tags: ["cypher", "neo4j", "project-management", "query", "active-projects"]
              language: "en"
              # Thuộc tính riêng của KnowledgeSnippet
              content: "MATCH (p:Project {status: 'Active'}) WHERE p.startDate IS NOT NULL RETURN p.id AS projectId, p.name AS projectName, p.startDate AS projectStartDate ORDER BY p.startDate DESC"
              contentType: "text/x-cypher"
              # vectorEmbedding: [0.123, -0.045, ..., 0.987] # (Ví dụ, thực tế là vector số thực dài, không hiển thị đầy đủ)
              extractedFromAssetId: "doc_wiki_neo4j_bp_v3"
              sourceUrl: "https://internal.mycompany.com/wiki/Neo4jBestPractices#active-projects-query"
              confidenceScore: 0.98
              processingStatus: "Embedded"
              usageCount: 42
              lastAccessedDate: "2024-07-21T11:05:30Z"
              relatedTensionIds: ["t_uuid_reporting_delay_001", "t_uuid_data_accuracy_005"]
              relatedProjectIds: ["proj_uuid_dashboard_v2", "proj_uuid_data_migration_phase1"]
            ```yaml

    *   **6.11. `Skill`**: Một năng lực hoặc kỹ năng cụ thể mà một `Agent` sở hữu hoặc một `Project`/`Task` yêu cầu.
        * **Mô tả**: Dùng để kết nối `Agent` với công việc phù hợp và xác định nhu cầu đào tạo.
        * **Thuộc tính**:
            * ` skillId`: `string` (format: `uuid`, primary_key: `true`, required: `true`, unique: `true`, description: "Mã định danh duy nhất toàn cầu cho kỹ năng.")
            * ` name`: `string` (required: `true`, unique: `true`, description: "Tên của kỹ năng, ví dụ: 'Python Programming', 'Ontology Design', 'Strategic Planning', 'Communication'.")
            * ` description`: `string` (optional: `true`, format: `markdown`, description: "Mô tả chi tiết về kỹ năng, bao gồm phạm vi, ứng dụng, và các khía cạnh quan trọng.")
            * ` category`: `string` (required: `true`, enum: [`TechnicalHardSkill`, `TechnicalSoftwareSkill`, `TechnicalDataSkill`, `SoftSkillInterpersonal`, `SoftSkillCognitive`, `SoftSkillLeadership`, `DomainExpertiseIndustry`, `DomainExpertiseFunctional`, `LanguageProficiency`, `ToolProficiency`, `MethodologyProficiency`, `Certification`, `Other`], description: "Phân loại chính của kỹ năng để nhóm và quản lý.")
            * ` skillLevel`: `string` (optional: `true`, enum: [`Novice`, `Beginner`, `Intermediate`, `Advanced`, `Expert`, `Master`], description: "Mô tả mức độ thành thạo của kỹ năng. Có thể được sử dụng khi liên kết kỹ năng với Agent.")
            * ` verificationStatus`: `string` (optional: `true`, enum: [`Unverified`, `SelfAssessed`, `PeerVerified`, `ManagerVerified`, `Certified`, `AssessmentPending`], default: `Unverified`, description: "Trạng thái xác minh của kỹ năng, đặc biệt khi liên kết với một Agent cụ thể.")
            * ` relatedTools`: `list[string]` (optional: `true`, description: "Danh sách các công cụ, phần mềm, hoặc nền tảng công nghệ liên quan trực tiếp đến kỹ năng này, ví dụ: ['Python 3.x', 'TensorFlow', 'Keras', 'Jira', 'Figma', 'AWS Sagemaker'].")
            * ` creationDate`: `datetime` (format: `ISO8601`, required: `true`, readonly: `true`, default: "current_timestamp", description: "Ngày kỹ năng này được định nghĩa hoặc ghi nhận lần đầu trong hệ thống.")
            * ` lastModifiedDate`: `datetime` (format: `ISO8601`, required: `true`, readonly: `true`, default: "current_timestamp", auto_update: `true`, description: "Ngày thông tin kỹ năng này được cập nhật lần cuối.")
            * ` tags`: `list[string]` (optional: `true`, description: "Các từ khóa, chủ đề hoặc nhãn giúp phân loại, tìm kiếm và liên kết kỹ năng.")
        * **Ví dụ**:
            ```yamlyaml
            Skill:
              skillId: "skill_a7b3c2d9-e0f1-4a8b-9c7d-6e5f4d3c2b1a"
              name: "Neo4j Cypher Query Language"
              description: "Khả năng viết và tối ưu hóa các truy vấn Cypher phức tạp để thao tác và phân tích dữ liệu trong cơ sở dữ liệu đồ thị Neo4j. Bao gồm hiểu biết về các mệnh đề, hàm, và tối ưu hiệu suất truy vấn."
              category: "TechnicalDataSkill"
              skillLevel: "Advanced" # Ví dụ khi Agent sở hữu kỹ năng này
              verificationStatus: "PeerVerified"
              relatedTools: ["Neo4j Desktop", "Neo4j Browser", "Cypher Shell", "APOC Library"]
              creationDate: "2023-11-15T10:00:00Z"
              lastModifiedDate: "2024-05-20T14:30:00Z"
              tags: ["neo4j", "cypher", "graph-database", "data-query", "database-programming"]
            ```yaml
7. Các Loại Mối Quan hệ (Relationship Types) Chính và Thuộc tính
    *   **7.1. `PERFORMED_ACTION`**
        * **Mô tả**: Ghi lại việc một `Agent` thực hiện một hành động cụ thể (ví dụ: tạo, cập nhật, hoàn thành) trên một thực thể mục tiêu như `Event`, `Task`, `Project`, `Tension`, `KnowledgeSnippet`, `WIN`, `Recognition`, `Resource`, v.v.
        * **Domain (Nguồn)**: `Agent` (Cụ thể là `agentId` của `Agent` thực hiện)
        * **Range (Đích)**: `Event`, `Task`, `Project`, `Tension`, `KnowledgeSnippet`, `WIN`, `Recognition`, `Resource`, hoặc các thực thể khác có thể là đối tượng của hành động. (Cụ thể là `targetEntityId` của thực thể đích)
        * **Thuộc tính của mối quan hệ `PERFORMED_ACTION`**:
            * ` relationshipId`: `string` (format: `uuid`, primary_key: `true`, required: `true`, unique: `true`, description: "Mã định danh duy nhất cho bản ghi mối quan hệ hành động này.")
            * ` agentId`: `string` (format: `uuid`, required: `true`, foreign_key: `Agent.agentId`, description: "ID của `Agent` thực hiện hành động. (Tham chiếu đến Domain)")
            * ` targetEntityId`: `string` (format: `uuid`, required: `true`, description: "ID của thực thể là đối tượng của hành động. (Tham chiếu đến Range)")
            * ` targetEntityType`: `string` (required: `true`, enum: [`Event`, `Task`, `Project`, `Tension`, `KnowledgeSnippet`, `WIN`, `Recognition`, `Resource`, `Comment`, `Document`, `UserAccount`, `SystemLog`, `Team`, `Goal`, `Objective`, `KeyResult`, `Other`], description: "Loại thực thể của `targetEntityId` để phân biệt.")
            * ` actionType`: `string` (required: `true`, enum: [`Created`, `Updated`, `Deleted`, `Completed`, `Started`, `Paused`, `Resumed`, `Assigned`, `Unassigned`, `Commented`, `Approved`, `Rejected`, `Viewed`, `Acknowledged`, `Resolved`, `Reopened`, `Escalated`, `Delegated`, `Submitted`, `Reviewed`, `Notified`, `LoggedIn`, `LoggedOut`, `SystemGenerated`, `CustomAction`, `Linked`, `Unlinked`, `Archived`, `Restored`, `Published`, `Unpublished`, `Followed`, `Unfollowed`, `Rated`, `Flagged`], description: "Loại hành động cụ thể được thực hiện.")
            * ` timestamp`: `datetime` (format: `ISO8601`, required: `true`, default: "current_timestamp", description: "Thời điểm chính xác hành động được thực hiện hoặc ghi nhận.")
            * ` roleInAction`: `string` (optional: `true`, description: "Vai trò của agent trong hành động cụ thể này, ví dụ: 'Creator', 'Assignee', 'Reviewer', 'Approver', 'Reporter', 'Participant', 'Owner', 'Editor', 'Viewer'. Có thể bổ sung cho `actionType`.")
            * ` details`: `string` (optional: `true`, format: `markdown`, description: "Mô tả chi tiết hoặc ghi chú bổ sung về hành động, ví dụ: lý do từ chối, nội dung bình luận, kết quả của việc hoàn thành, thay đổi cụ thể đã thực hiện.")
            * ` sourceApplication`: `string` (optional: `true`, default: `TRM-OS Core`, description: "Ứng dụng, module, hoặc agent (nếu là system agent) nguồn đã ghi nhận hành động này, ví dụ: 'TRM-OS TaskManager', 'TRM-OS NotificationService', 'AIContentGeneratorAgent'.")
            * ` durationMs`: `integer` (optional: `true`, minimum: `0`, description: "Thời gian thực hiện hành động, tính bằng mili giây, nếu có và đo lường được (ví dụ: thời gian hoàn thành một Task, thời gian xử lý một yêu cầu). Mặc định là null nếu không áp dụng.")
            * ` contextSessionId`: `string` (format: `uuid`, optional: `true`, description: "ID của một phiên làm việc hoặc ngữ cảnh rộng hơn mà hành động này thuộc về, giúp nhóm các hành động liên quan.")
        * **Ví dụ**: 
            ```yamlyaml
            PERFORMED_ACTION:
              relationshipId: "pa_0a1b2c3d-4e5f-6a7b-8c9d-0e1f2a3b4c5d"
              agentId: "agent_f0e1d2c3-b4a5-9876-5432-10fedcba9876" # ID của InternalAgent "Founder"
              targetEntityId: "event_cba98765-4321-0fed-cba9-876543210fed" # ID của Event (có thể là TensionEvent)
              targetEntityType: "Event"
              actionType: "Created"
              timestamp: "2024-05-15T10:30:00Z"
              roleInAction: "Creator"
              details: "Initial identification of the need for a revised ontology to support TRM-OS v3.2 development. Event triggered by Tension creation (Tension ID: t_xyz)."
              sourceApplication: "TRM-OS TensionModule"
              durationMs: null
              contextSessionId: "session_fedcba98-7654-3210-fedc-ba9876543210"
            ```yaml

    *   **7.2. `HAS_SKILL`**
        * **Mô tả**: Liên kết một `Agent` với một `Skill` mà Agent đó sở hữu hoặc đã được chứng minh có năng lực.
        * **Domain (Nguồn)**: `Agent` (Cụ thể là `agentId` của `Agent` sở hữu kỹ năng)
        * **Range (Đích)**: `Skill` (Cụ thể là `skillId` của `Skill` được sở hữu)
        * **Thuộc tính của mối quan hệ `HAS_SKILL`**:
            * ` relationshipId`: `string` (format: `uuid`, primary_key: `true`, required: `true`, unique: `true`, description: "Mã định danh duy nhất cho bản ghi mối quan hệ sở hữu kỹ năng này.")
            * ` agentId`: `string` (format: `uuid`, required: `true`, foreign_key: `Agent.agentId`, description: "ID của `Agent` sở hữu kỹ năng. (Tham chiếu đến Domain)")
            * ` skillId`: `string` (format: `uuid`, required: `true`, foreign_key: `Skill.skillId`, description: "ID của `Skill` được sở hữu. (Tham chiếu đến Range)")
            * ` proficiencyLevel`: `string` (required: `true`, enum: [`Novice_1`, `Beginner_2`, `Intermediate_3`, `Advanced_4`, `Expert_5`, `Master_6`], description: "Mức độ thành thạo của Agent đối với Skill này. Có thể dùng thang điểm 1-6 hoặc các giá trị enum tương ứng. Đồng bộ với `Skill.skillLevel` nếu `Skill` đó được định nghĩa chung, hoặc ghi nhận mức độ riêng của Agent này.")
            * ` verificationDate`: `datetime` (format: `ISO8601`, optional: `true`, description: "Ngày kỹ năng này được xác minh cho Agent (ví dụ: qua bài test, chứng chỉ, đánh giá).")
            * ` verifiedByAgentId`: `string` (format: `uuid`, optional: `true`, foreign_key: `Agent.agentId`, description: "ID của Agent (thường là quản lý, người đánh giá) đã xác minh kỹ năng này cho Agent sở hữu.")
            * ` experienceYears`: `float` (optional: `true`, minimum: `0`, description: "Số năm kinh nghiệm Agent có với kỹ năng này.")
            * ` lastUsedDate`: `datetime` (format: `ISO8601`, optional: `true`, description: "Ngày cuối cùng Agent sử dụng hoặc áp dụng kỹ năng này trong công việc.")
            * ` status`: `string` (optional: `true`, enum: [`Active`, `PendingVerification`, `ExpiredCertification`, `NeedsRefreshment`, `Archived`], default: `Active`, description: "Trạng thái của việc sở hữu kỹ năng này đối với Agent (ví dụ: còn hiệu lực, cần xác minh lại, chứng chỉ hết hạn).")
            * ` notes`: `string` (optional: `true`, format: `markdown`, description: "Ghi chú bổ sung về việc Agent sở hữu kỹ năng này, ví dụ: chi tiết về dự án đã áp dụng, điểm mạnh cụ thể, hoặc bằng chứng về năng lực.")
            * ` creationDate`: `datetime` (format: `ISO8601`, required: `true`, readonly: `true`, default: "current_timestamp", description: "Ngày mối quan hệ HAS_SKILL này được tạo.")
            * ` lastModifiedDate`: `datetime` (format: `ISO8601`, required: `true`, readonly: `true`, default: "current_timestamp", auto_update: `true`, description: "Ngày mối quan hệ HAS_SKILL này được cập nhật lần cuối.")
        * **Ví dụ**:
            ```yamlyaml
            HAS_SKILL:
              relationshipId: "hs_1b2c3d4e-5f6a-7b8c-9d0e-1f2a3b4c5d6e"
              agentId: "agent_dev1_c3d4e5f6-a7b8-c9d0-e1f2-a3b4c5d6e7f8"
              skillId: "skill_a7b3c2d9-e0f1-4a8b-9c7d-6e5f4d3c2b1a" # ID của Skill "Neo4j Cypher Query Language"
              proficiencyLevel: "Advanced_4"
              verificationDate: "2024-03-10T00:00:00Z"
              verifiedByAgentId: "agent_manager_b4c5d6e7-f8a9-b0c1-d2e3-f4a5b6c7d8e9"
              experienceYears: 3.5
              lastUsedDate: "2024-07-15T00:00:00Z"
              status: "Active"
              notes: "Successfully applied in Project X, optimized critical queries leading to 30% performance improvement. Verified via internal assessment by Tech Lead."
              creationDate: "2023-09-01T11:00:00Z"
              lastModifiedDate: "2024-07-18T16:45:00Z"
            ```yaml

    *   **7.3. `PARTICIPATES_IN`**
        * **Mô tả**: Liên kết một `Agent` với một `Project` mà Agent đó tham gia, đóng góp hoặc có vai trò trong đó.
        * **Domain (Nguồn)**: `Agent` (Cụ thể là `agentId` của `Agent` tham gia)
        * **Range (Đích)**: `Project` (Cụ thể là `projectId` của `Project` được tham gia)
        * **Thuộc tính của mối quan hệ `PARTICIPATES_IN`**:
            * ` relationshipId`: `string` (format: `uuid`, primary_key: `true`, required: `true`, unique: `true`, description: "Mã định danh duy nhất cho bản ghi mối quan hệ tham gia dự án này.")
            * ` agentId`: `string` (format: `uuid`, required: `true`, foreign_key: `Agent.agentId`, description: "ID của `Agent` tham gia dự án. (Tham chiếu đến Domain)")
            * ` projectId`: `string` (format: `uuid`, required: `true`, foreign_key: `Project.projectId`, description: "ID của `Project` được tham gia. (Tham chiếu đến Range)")
            * ` role`: `string` (required: `true`, enum: [`ProjectLead`, `ProjectManager`, `TeamMember`, `TechnicalLead`, `ProductOwner`, `ScrumMaster`, `Developer`, `QAEngineer`, `Designer`, `Analyst`, `Consultant`, `Stakeholder`, `Sponsor`, `Contributor`, `Observer`, `Advisor`, `SubjectMatterExpert`, `Coordinator`, `Facilitator`, `Other`], description: "Vai trò cụ thể của Agent trong dự án.")
            * ` allocationPercentage`: `float` (optional: `true`, minimum: `0.0`, maximum: `100.0`, description: "Tỷ lệ phần trăm thời gian hoặc nguồn lực mà Agent được phân bổ cho dự án này. Ví dụ: 50.0 cho 50%.")
            * ` commitmentLevel`: `string` (optional: `true`, enum: [`FullTimeEquivalent`, `PartTime`, `AsNeeded`, `Advisory`, `Informational`], description: "Mức độ cam kết của Agent đối với dự án.")
            * ` responsibilities`: `string` (optional: `true`, format: `markdown`, description: "Mô tả các trách nhiệm chính hoặc nhiệm vụ cụ thể của Agent trong dự án này.")
            * ` startDate`: `datetime` (format: `ISO8601`, required: `true`, description: "Ngày Agent bắt đầu tham gia hoặc được phân công vào dự án.")
            * ` endDate`: `datetime` (format: `ISO8601`, optional: `true`, description: "Ngày Agent kết thúc tham gia hoặc được rút khỏi dự án. Null nếu vẫn đang tham gia.")
            * ` status`: `string` (required: `true`, enum: [`Active`, `PendingAssignment`, `OnHold`, `EndedSuccessfully`, `EndedPrematurely`, `Withdrawn`, `Proposed`], default: `Active`, description: "Trạng thái tham gia của Agent trong dự án.")
            * ` creationDate`: `datetime` (format: `ISO8601`, required: `true`, readonly: `true`, default: "current_timestamp", description: "Ngày mối quan hệ PARTICIPATES_IN này được tạo.")
            * ` lastModifiedDate`: `datetime` (format: `ISO8601`, required: `true`, readonly: `true`, default: "current_timestamp", auto_update: `true`, description: "Ngày mối quan hệ PARTICIPATES_IN này được cập nhật lần cuối.")
        * **Ví dụ**:
            ```yamlyaml
            PARTICIPATES_IN:
              relationshipId: "pi_2c3d4e5f-6a7b-8c9d-0e1f-2a3b4c5d6e7f"
              agentId: "agent_ai_pm_b4c5d6e7-f8a9-b0c1-d2e3-f4a5b6c7d8e9" # ID của AIAgent "ProjectMgmtAgent"
              projectId: "proj_ontology_v3_2_a3b4c5d6-e7f8-a9b0-c1d2-e3f4a5b6c7d8" # ID của Project "Ontology V3.2"
              role: "TechnicalLead"
              allocationPercentage: 75.0
              commitmentLevel: "PartTime"
              responsibilities: "- Lead the technical design and implementation of the new ontology structure.\n- Coordinate with development team for integration.\n- Ensure adherence to data modeling best practices."
              startDate: "2024-06-01T09:00:00Z"
              endDate: null # Vẫn đang tham gia
              status: "Active"
              creationDate: "2024-05-28T14:00:00Z"
              lastModifiedDate: "2024-06-05T10:15:00Z"
            ```yaml

    *   **7.4. `GENERATES_EVENT`**
        * **Mô tả**: Liên kết một thực thể nguồn (`Project`, `Task`, hoặc `Agent`) với một `Event` mà nó trực tiếp tạo ra hoặc gây ra.
        * **Domain (Nguồn)**: `Project`, `Task`, `Agent` (Được xác định bởi `sourceEntityId` và `sourceEntityType`)
        * **Range (Đích)**: `Event` (Cụ thể là `eventId` của `Event` được tạo ra)
        * **Thuộc tính của mối quan hệ `GENERATES_EVENT`**:
            * ` relationshipId`: `string` (format: `uuid`, primary_key: `true`, required: `true`, unique: `true`, description: "Mã định danh duy nhất cho bản ghi mối quan hệ tạo event này.")
            * ` sourceEntityId`: `string` (format: `uuid`, required: `true`, description: "ID của thực thể nguồn (Project, Task, Agent) tạo ra Event. (Tham chiếu đến Domain)")
            * ` sourceEntityType`: `string` (required: `true`, enum: [`Project`, `Task`, `Agent`, `System`], description: "Loại của thực thể nguồn.")
            * ` eventId`: `string` (format: `uuid`, required: `true`, foreign_key: `Event.eventId`, description: "ID của `Event` được tạo ra. (Tham chiếu đến Range)")
            * ` timestamp`: `datetime` (format: `ISO8601`, required: `true`, default: "current_timestamp", description: "Thời điểm mà thực thể nguồn tạo ra Event này.")
            * ` triggerDescription`: `string` (optional: `true`, format: `markdown`, description: "Mô tả chi tiết về nguyên nhân, điều kiện hoặc hành động cụ thể đã kích hoạt việc tạo ra Event.")
            * ` causalityType`: `string` (optional: `true`, enum: [`Direct`, `Indirect`, `Scheduled`, `Conditional`, `SystemInitiated`, `UserAction`, `ProcessStep`], default: `Direct`, description: "Loại hình quan hệ nhân quả giữa nguồn và Event được tạo ra.")
            * ` details`: `string` (optional: `true`, format: `markdown`, description: "Thông tin bổ sung hoặc ngữ cảnh về việc tạo ra Event này.")
            * ` creationDate`: `datetime` (format: `ISO8601`, required: `true`, readonly: `true`, default: "current_timestamp", description: "Ngày mối quan hệ GENERATES_EVENT này được tạo.")
            * ` lastModifiedDate`: `datetime` (format: `ISO8601`, required: `true`, readonly: `true`, default: "current_timestamp", auto_update: `true`, description: "Ngày mối quan hệ GENERATES_EVENT này được cập nhật lần cuối.")
        * **Ví dụ**: Một `Task` hoàn thành và tạo ra một `TaskEvent`.
            ```yamlyaml
            GENERATES_EVENT:
              relationshipId: "ge_3d4e5f6a-7b8c-9d0e-1f2a-3b4c5d6e7f8a"
              sourceEntityId: "task_b4c5d6e7-f8a9-b0c1-d2e3-f4a5b6c7d8e9" # ID của một Task
              sourceEntityType: "Task"
              eventId: "event_c5d6e7f8-a9b0-c1d2-e3f4-a5b6c7d8e9f0" # ID của TaskEvent "TaskCompleted"
              timestamp: "2024-07-20T14:35:10Z"
              triggerDescription: "Task 'Develop API Endpoint for User Authentication' marked as completed by assignee."
              causalityType: "Direct"
              details: "Event generated upon status change of the task to 'Completed'. Payload of the event includes task details and completion metrics."
              creationDate: "2024-07-20T14:35:10Z"
              lastModifiedDate: "2024-07-20T14:35:10Z"
            ```yaml

    *   **7.5. `RESOLVES_TENSION`**
        * **Mô tả**: Liên kết một `Project` với một `Tension` mà Project đó được thiết kế, đề xuất hoặc đang thực hiện để giải quyết. Mối quan hệ này thể hiện mục tiêu giải quyết Tension của Project.
        * **Domain (Nguồn)**: `Project` (Cụ thể là `projectId` của `Project` giải quyết)
        * **Range (Đích)**: `Tension` (Cụ thể là `tensionId` của `Tension` được giải quyết)
        * **Thuộc tính của mối quan hệ `RESOLVES_TENSION`**:
            * ` relationshipId`: `string` (format: `uuid`, primary_key: `true`, required: `true`, unique: `true`, description: "Mã định danh duy nhất cho bản ghi mối quan hệ giải quyết tension này.")
            * ` projectId`: `string` (format: `uuid`, required: `true`, foreign_key: `Project.projectId`, description: "ID của `Project` nhằm giải quyết Tension. (Tham chiếu đến Domain)")
            * ` tensionId`: `string` (format: `uuid`, required: `true`, foreign_key: `Tension.tensionId`, description: "ID của `Tension` được giải quyết. (Tham chiếu đến Range)")
            * ` resolutionStatus`: `string` (required: `true`, enum: [`Proposed`, `ApprovedForResolution`, `ResolutionInProgress`, `PartiallyResolved`, `Resolved`, `ResolutionFailed`, `OnHold`, `Cancelled`, `RequiresReview`], default: `Proposed`, description: "Trạng thái của việc giải quyết Tension thông qua Project này.")
            * ` resolutionApproach`: `string` (optional: `true`, format: `markdown`, description: "Mô tả phương pháp hoặc chiến lược mà Project sẽ sử dụng để giải quyết Tension.")
            * ` expectedOutcome`: `string` (optional: `true`, format: `markdown`, description: "Kết quả hoặc trạng thái mong đợi sau khi Tension được giải quyết thành công bởi Project.")
            * ` alignmentScore`: `float` (optional: `true`, minimum: `0.0`, maximum: `1.0`, description: "Điểm số (0-1) đánh giá mức độ phù hợp hoặc tiềm năng của Project trong việc giải quyết Tension này. Ví dụ: 0.85.")
            * ` priority`: `string` (optional: `true`, enum: [`Critical`, `High`, `Medium`, `Low`, `Informational`], default: `Medium`, description: "Mức độ ưu tiên của việc Project này giải quyết Tension cụ thể này so với các Tension khác mà Project có thể giải quyết, hoặc so với các Project khác.")
            * ` startDate`: `datetime` (format: `ISO8601`, optional: `true`, description: "Ngày Project bắt đầu các hoạt động cụ thể nhằm giải quyết Tension này.")
            * ` targetResolutionDate`: `datetime` (format: `ISO8601`, optional: `true`, description: "Ngày dự kiến Tension sẽ được giải quyết hoàn toàn bởi Project này.")
            * ` actualResolutionDate`: `datetime` (format: `ISO8601`, optional: `true`, description: "Ngày thực tế Tension được xác nhận là đã giải quyết bởi Project này.")
            * ` notes`: `string` (optional: `true`, format: `markdown`, description: "Ghi chú bổ sung về mối quan hệ giữa Project và Tension, ví dụ: các rủi ro, phụ thuộc, hoặc các yếu tố ảnh hưởng đến việc giải quyết.")
            * ` creationDate`: `datetime` (format: `ISO8601`, required: `true`, readonly: `true`, default: "current_timestamp", description: "Ngày mối quan hệ RESOLVES_TENSION này được tạo.")
            * ` lastModifiedDate`: `datetime` (format: `ISO8601`, required: `true`, readonly: `true`, default: "current_timestamp", auto_update: `true`, description: "Ngày mối quan hệ RESOLVES_TENSION này được cập nhật lần cuối.")
        * **Ví dụ**: Một `ProjectProposal` được tạo để giải quyết một `Tension` về dữ liệu phân mảnh.
            ```yamlyaml
            RESOLVES_TENSION:
              relationshipId: "rt_4e5f6a7b-8c9d-0e1f-2a3b-4c5d6e7f8a9b"
              projectId: "projprop_crm_int_c9d0e1f2-a3b4-c5d6-e7f8-a9b0c1d2e3f4" # ID của ProjectProposal "New CRM Integration"
              tensionId: "tension_sales_data_frag_a7b8c9d0-e1f2-a3b4-c5d6-e7f8a9b0c1d2" # ID của Tension "Sales data is fragmented"
              resolutionStatus: "Proposed"
              resolutionApproach: "- Implement a centralized CRM system (e.g., HubSpot).\n- Migrate all existing sales data from disparate sources.\n- Establish data governance policies and training for sales team."
              expectedOutcome: "- All sales data consolidated into a single source of truth.\n- Improved data accuracy and accessibility for reporting and analytics.\n- Enhanced sales team efficiency."
              alignmentScore: 0.9
              priority: "High"
              startDate: null # Chưa bắt đầu cụ thể cho tension này, vì đang là proposal
              targetResolutionDate: "2025-03-31T00:00:00Z"
              actualResolutionDate: null
              notes: "This project is critical for achieving Q1 sales targets. Dependent on budget approval."
              creationDate: "2024-07-10T09:00:00Z"
              lastModifiedDate: "2024-07-18T11:30:00Z"
            ```yaml

    *   **7.6. `LEADS_TO_WIN`**
        * **Mô tả**: Liên kết một `RecognitionEvent` đáng chú ý hoặc kết quả thành công của một `Project` với một `WIN` mà nó đã đóng góp đáng kể hoặc trực tiếp dẫn đến. Thể hiện mối quan hệ nhân quả hoặc đóng góp quan trọng.
        * **Domain (Nguồn)**: `RecognitionEvent`, `Project` (Được xác định bởi `sourceEntityId` và `sourceEntityType`)
        * **Range (Đích)**: `WIN` (Cụ thể là `winId` của `WIN` được tạo ra hoặc đạt được)
        * **Thuộc tính của mối quan hệ `LEADS_TO_WIN`**:
            * ` relationshipId`: `string` (format: `uuid`, primary_key: `true`, required: `true`, unique: `true`, description: "Mã định danh duy nhất cho bản ghi mối quan hệ dẫn đến WIN này.")
            * ` sourceEntityId`: `string` (format: `uuid`, required: `true`, description: "ID của thực thể nguồn (RecognitionEvent hoặc Project) dẫn đến WIN. (Tham chiếu đến Domain)")
            * ` sourceEntityType`: `string` (required: `true`, enum: [`RecognitionEvent`, `Project`], description: "Loại của thực thể nguồn.")
            * ` winId`: `string` (format: `uuid`, required: `true`, foreign_key: `WIN.winId`, description: "ID của `WIN` được tạo ra hoặc đạt được. (Tham chiếu đến Range)")
            * ` contributionFactor`: `float` (optional: `true`, minimum: `0.0`, maximum: `1.0`, description: "Hệ số đóng góp ước tính của thực thể nguồn đối với việc đạt được WIN (ví dụ: 0.75 cho 75% đóng góp). Null nếu khó xác định hoặc không áp dụng.")
            * ` description`: `string` (optional: `true`, format: `markdown`, description: "Mô tả chi tiết về cách thức hoặc lý do thực thể nguồn dẫn đến hoặc đóng góp vào WIN này.")
            * ` attributionDate`: `datetime` (format: `ISO8601`, required: `true`, description: "Ngày mà sự đóng góp này được ghi nhận hoặc mối liên kết này được xác định.")
            * ` significanceLevel`: `string` (optional: `true`, enum: [`Pivotal`, `Major`, `Significant`, `Moderate`, `Minor`], default: `Significant`, description: "Mức độ quan trọng của sự đóng góp từ nguồn này đối với việc đạt được WIN.")
            * ` relatedMetrics`: `list[object]` (optional: `true`, description: "Danh sách các chỉ số cụ thể chứng minh sự đóng góp. Mỗi object chứa: `metricName: string`, `value: string | number`, `unit: string`.")
                *   Cấu trúc `relatedMetrics` object:
                    * ` metricName`: `string` (required)
                    * ` value`: `string | number` (required)
                    * ` unit`: `string` (optional)
            * ` verifiedByAgentId`: `string` (format: `uuid`, optional: `true`, foreign_key: `Agent.agentId`, description: "ID của Agent đã xác minh mối liên kết đóng góp này.")
            * ` verificationDate`: `datetime` (format: `ISO8601`, optional: `true`, description: "Ngày xác minh mối liên kết.")
            * ` notes`: `string` (optional: `true`, format: `markdown`, description: "Ghi chú bổ sung về mối quan hệ này.")
            * ` creationDate`: `datetime` (format: `ISO8601`, required: `true`, readonly: `true`, default: "current_timestamp", description: "Ngày mối quan hệ LEADS_TO_WIN này được tạo.")
            * ` lastModifiedDate`: `datetime` (format: `ISO8601`, required: `true`, readonly: `true`, default: "current_timestamp", auto_update: `true`, description: "Ngày mối quan hệ LEADS_TO_WIN này được cập nhật lần cuối.")
        * **Ví dụ**: Hoàn thành `Project` "Launch New Product Line" dẫn đến `WIN` "Increased Market Share Q3".
            ```yamlyaml
            LEADS_TO_WIN:
              relationshipId: "ltw_5f6a7b8c-9d0e-1f2a-3b4c-5d6e7f8a9b0c"
              sourceEntityId: "proj_new_prod_line_9d0e1f2a-3b4c-5d6e-7f8a9b0c1d2e" # ID của Project "Launch New Product Line"
              sourceEntityType: "Project"
              winId: "win_market_share_q3_1f2a3b4c-5d6e-7f8a-9b0c1d2e3f4a" # ID của WIN "Increased Market Share Q3"
              contributionFactor: 0.8
              description: "The successful launch and positive market reception of the new product line were the primary drivers for the 5% market share increase in Q3. Key features X and Y were particularly impactful."
              attributionDate: "2024-10-05T00:00:00Z"
              significanceLevel: "Major"
              relatedMetrics:
                - metricName: "MarketShareIncrease"
                  value: 5
                  unit: "%"
                - metricName: "NewProductSalesVolume"
                  value: 12000
                  unit: "units"
              verifiedByAgentId: "agent_ceo_3b4c5d6e-7f8a-9b0c-1d2e3f4a5b6c"
              verificationDate: "2024-10-04T00:00:00Z"
              notes: "WIN achieved ahead of schedule due to excellent project execution."
              creationDate: "2024-10-05T10:00:00Z"
              lastModifiedDate: "2024-10-05T11:30:00Z"
            ```yaml

    *   **7.7. `REQUIRES_RESOURCE`**
        * **Mô tả**: Liên kết một `Project` hoặc `Task` (thực thể yêu cầu) với một `Resource` mà nó cần để thực hiện hoặc hoàn thành. Mối quan hệ này thể hiện nhu cầu hoặc sự phân bổ tài nguyên.
        * **Domain (Nguồn)**: `Project`, `Task` (Được xác định bởi `requesterEntityId` và `requesterEntityType`)
        * **Range (Đích)**: `Resource` (Cụ thể là `resourceId` của `Resource` được yêu cầu)
        * **Thuộc tính của mối quan hệ `REQUIRES_RESOURCE`**:
            * ` relationshipId`: `string` (format: `uuid`, primary_key: `true`, required: `true`, unique: `true`, description: "Mã định danh duy nhất cho bản ghi mối quan hệ yêu cầu tài nguyên này.")
            * ` requesterEntityId`: `string` (format: `uuid`, required: `true`, description: "ID của thực thể nguồn (Project hoặc Task) yêu cầu Resource. (Tham chiếu đến Domain)")
            * ` requesterEntityType`: `string` (required: `true`, enum: [`Project`, `Task`], description: "Loại của thực thể nguồn yêu cầu.")
            * ` resourceId`: `string` (format: `uuid`, required: `true`, foreign_key: `Resource.resourceId`, description: "ID của `Resource` được yêu cầu. (Tham chiếu đến Range)")
            * ` quantity`: `float` (optional: `true`, minimum: `0`, description: "Số lượng của Resource được yêu cầu. Ví dụ: 5, 10.5. Nếu không có đơn vị, mặc định là số lượng đơn thuần.")
            * ` unit`: `string` (optional: `true`, description: "Đơn vị tính cho `quantity` (ví dụ: 'hours', 'licenses', 'GB', 'cores', 'USD', 'items'). Bắt buộc nếu `quantity` có ý nghĩa về đơn vị.")
            * ` status`: `string` (required: `true`, enum: [`Requested`, `PendingApproval`, `Approved`, `Allocated`, `PartiallyAllocated`, `InUse`, `Consumed`, `Returned`, `Denied`, `Cancelled`, `Fulfilled`], default: `Requested`, description: "Trạng thái của yêu cầu hoặc sự phân bổ Resource này.")
            * ` purpose`: `string` (optional: `true`, format: `markdown`, description: "Mô tả mục đích cụ thể của việc yêu cầu Resource này cho Project/Task.")
            * ` priority`: `string` (optional: `true`, enum: [`Critical`, `High`, `Medium`, `Low`], default: `Medium`, description: "Mức độ ưu tiên của yêu cầu Resource này.")
            * ` requestDate`: `datetime` (format: `ISO8601`, required: `true`, default: "current_timestamp", description: "Ngày Resource này được yêu cầu.")
            * ` allocationDate`: `datetime` (format: `ISO8601`, optional: `true`, description: "Ngày Resource này được phân bổ hoặc phê duyệt để sử dụng.")
            * ` expectedStartDate`: `datetime` (format: `ISO8601`, optional: `true`, description: "Ngày dự kiến bắt đầu sử dụng Resource.")
            * ` expectedEndDate`: `datetime` (format: `ISO8601`, optional: `true`, description: "Ngày dự kiến kết thúc sử dụng hoặc trả lại Resource.")
            * ` actualUsageDurationMs`: `integer` (optional: `true`, minimum: `0`, description: "Thời gian thực tế Resource được sử dụng, tính bằng mili giây, nếu có thể đo lường và phù hợp (ví dụ: thời gian sử dụng máy chủ).")
            * ` notes`: `string` (optional: `true`, format: `markdown`, description: "Ghi chú bổ sung về yêu cầu Resource này.")
            * ` creationDate`: `datetime` (format: `ISO8601`, required: `true`, readonly: `true`, default: "current_timestamp", description: "Ngày mối quan hệ REQUIRES_RESOURCE này được tạo.")
            * ` lastModifiedDate`: `datetime` (format: `ISO8601`, required: `true`, readonly: `true`, default: "current_timestamp", auto_update: `true`, description: "Ngày mối quan hệ REQUIRES_RESOURCE này được cập nhật lần cuối.")
        * **Ví dụ**: Một `Task` yêu cầu 2 licenses của một `SoftwareResource`.
            ```yamlyaml
            REQUIRES_RESOURCE:
              relationshipId: "rr_6a7b8c9d-0e1f-2a3b-4c5d-6e7f8a9b0c1d"
              requesterEntityId: "task_dev_frontend_0e1f2a3b-4c5d-6e7f-8a9b0c1d2e3f" # ID của Task "Develop Frontend UI"
              requesterEntityType: "Task"
              resourceId: "swres_design_tool_x_4c5d6e7f-8a9b-0c1d-2e3f4a5b6c7d" # ID của SoftwareResource "Design Tool X"
              quantity: 2
              unit: "licenses"
              status: "Approved"
              purpose: "For UI/UX design and prototyping by two frontend developers assigned to the task."
              priority: "High"
              requestDate: "2024-07-15T09:00:00Z"
              allocationDate: "2024-07-16T14:00:00Z"
              expectedStartDate: "2024-07-17T00:00:00Z"
              expectedEndDate: "2024-08-30T00:00:00Z"
              actualUsageDurationMs: null
              notes: "Licenses allocated from central pool. Ensure return upon task completion."
              creationDate: "2024-07-15T09:05:00Z"
              lastModifiedDate: "2024-07-16T14:05:00Z"
            ```yaml

    *   **7.8. `HAS_SUBTASK`**
        * **Mô tả**: Liên kết một `Project` hoặc một `Task` (cha) với một `Task` (con) là một phần của nó hoặc phụ thuộc vào nó. Thể hiện cấu trúc phân cấp công việc hoặc mối quan hệ phụ thuộc giữa các task.
        * **Domain (Nguồn/Cha)**: `Project`, `Task` (Được xác định bởi `parentEntityId` và `parentEntityType`)
        * **Range (Đích/Con)**: `Task` (Cụ thể là `childTaskId` của `Task` con)
        * **Thuộc tính của mối quan hệ `HAS_SUBTASK`**:
            * ` relationshipId`: `string` (format: `uuid`, primary_key: `true`, required: `true`, unique: `true`, description: "Mã định danh duy nhất cho bản ghi mối quan hệ cha-con này.")
            * ` parentEntityId`: `string` (format: `uuid`, required: `true`, description: "ID của thực thể cha (Project hoặc Task). (Tham chiếu đến Domain)")
            * ` parentEntityType`: `string` (required: `true`, enum: [`Project`, `Task`], description: "Loại của thực thể cha.")
            * ` childTaskId`: `string` (format: `uuid`, required: `true`, foreign_key: `Task.taskId`, description: "ID của `Task` con. (Tham chiếu đến Range)")
            * ` dependencyType`: `string` (optional: `true`, enum: [`FinishToStart_FS`, `StartToStart_SS`, `FinishToFinish_FF`, `StartToFinish_SF`, `NoDependency`, `BlockedBy`, `Related`], default: `FinishToStart_FS`, description: "Loại phụ thuộc giữa task cha/anh em trước và task con này. 'NoDependency' nếu chỉ là phân rã. 'BlockedBy' nếu task con bị chặn bởi task khác không phải cha trực tiếp.")
            * ` lagDuration`: `string` (optional: `true`, format: `ISO8601_duration`, description: "Thời gian trễ hoặc sớm liên quan đến `dependencyType`. Ví dụ: 'P2D' (trễ 2 ngày), '-PT1H' (sớm 1 giờ). Null nếu không có lag.")
            * ` isCriticalPath`: `boolean` (optional: `true`, default: `false`, description: "Đánh dấu nếu mối quan hệ này (và task con) nằm trên đường găng của project hoặc task cha.")
            * ` sequenceOrder`: `integer` (optional: `true`, minimum: `1`, description: "Thứ tự thực hiện của task con này so với các task con khác cùng cấp, nếu cần thiết và không hoàn toàn do `dependencyType` quyết định.")
            * ` linkType`: `string` (optional: `true`, enum: [`Decomposition`, `Dependency`, `ExecutionOrder`, `Informational`], default: `Decomposition`, description: "Bản chất của liên kết: 'Decomposition' (phân rã công việc), 'Dependency' (phụ thuộc logic), 'ExecutionOrder' (thứ tự thực hiện), 'Informational' (liên quan thông tin).")
            * ` notes`: `string` (optional: `true`, format: `markdown`, description: "Ghi chú bổ sung về mối quan hệ subtask này.")
            * ` creationDate`: `datetime` (format: `ISO8601`, required: `true`, readonly: `true`, default: "current_timestamp", description: "Ngày mối quan hệ HAS_SUBTASK này được tạo.")
            * ` lastModifiedDate`: `datetime` (format: `ISO8601`, required: `true`, readonly: `true`, default: "current_timestamp", auto_update: `true`, description: "Ngày mối quan hệ HAS_SUBTASK này được cập nhật lần cuối.")
        * **Ví dụ**: `Task` "Phase 1 Development" có subtask "Develop UI Mockups" với phụ thuộc Finish-to-Start.
            ```yamlyaml
            HAS_SUBTASK:
              relationshipId: "hst_7b8c9d0e-1f2a-3b4c-5d6e-7f8a9b0c1d2e"
              parentEntityId: "task_phase1_dev_1f2a3b4c-5d6e-7f8a-9b0c1d2e3f4a" # ID của Task "Phase 1 Development"
              parentEntityType: "Task"
              childTaskId: "task_ui_mockups_5d6e7f8a-9b0c-1d2e-3f4a5b6c7d8e" # ID của Task "Develop UI Mockups"
              dependencyType: "FinishToStart_FS"
              lagDuration: "P1D" # Bắt đầu 1 ngày sau khi task cha hoàn thành mục liên quan
              isCriticalPath: true
              sequenceOrder: 1
              linkType: "Decomposition"
              notes: "UI Mockups must be completed before backend development for this feature can begin effectively."
              creationDate: "2024-07-01T10:00:00Z"
              lastModifiedDate: "2024-07-05T11:30:00Z"
            ```yaml

    *   **7.9. `IS_PART_OF_PROJECT`**
        * **Mô tả**: Thiết lập một liên kết trực tiếp chỉ rõ rằng một `Task` thuộc về hoặc là một thành phần của một `Project` cụ thể. Mối quan hệ này tập trung vào vai trò và sự đóng góp của `Task` trong phạm vi `Project` đó.
        * **Domain (Nguồn)**: `Task` (Được xác định bởi `taskId`)
        * **Range (Đích)**: `Project` (Được xác định bởi `projectId`)
        * **Thuộc tính của mối quan hệ `IS_PART_OF_PROJECT`**:
            * ` relationshipId`: `string` (format: `uuid`, primary_key: `true`, required: `true`, unique: `true`, description: "Mã định danh duy nhất cho bản ghi mối quan hệ này.")
            * ` taskId`: `string` (format: `uuid`, required: `true`, foreign_key: `Task.taskId`, description: "ID của `Task` là một phần của Project. (Tham chiếu đến Domain)")
            * ` projectId`: `string` (format: `uuid`, required: `true`, foreign_key: `Project.projectId`, description: "ID của `Project` mà Task này thuộc về. (Tham chiếu đến Range)")
            * ` assignmentType`: `string` (optional: `true`, enum: [`Primary`, `Secondary`, `Support`, `CrossCutting`, `Administrative`], default: `Primary`, description: "Phân loại vai trò của Task trong Project: 'Primary' (nhiệm vụ chính), 'Secondary' (nhiệm vụ phụ), 'Support' (hỗ trợ), 'CrossCutting' (liên quan nhiều mặt), 'Administrative' (quản lý/hành chính).")
            * ` contextualDescription`: `string` (optional: `true`, format: `markdown`, description: "Mô tả vai trò, đóng góp, hoặc sự liên quan cụ thể của Task này trong bối cảnh của Project. Bổ sung cho `Task.description` chung.")
            * ` assignmentDate`: `datetime` (format: `ISO8601`, optional: `true`, default: "current_timestamp", description: "Ngày Task này được chính thức xem là một phần hoặc được gán vào phạm vi của Project.")
            * ` notes`: `string` (optional: `true`, format: `markdown`, description: "Ghi chú bổ sung về sự tham gia của Task này trong Project.")
            * ` creationDate`: `datetime` (format: `ISO8601`, required: `true`, readonly: `true`, default: "current_timestamp", description: "Ngày mối quan hệ IS_PART_OF_PROJECT này được tạo.")
            * ` lastModifiedDate`: `datetime` (format: `ISO8601`, required: `true`, readonly: `true`, default: "current_timestamp", auto_update: `true`, description: "Ngày mối quan hệ IS_PART_OF_PROJECT này được cập nhật lần cuối.")
        * **Lưu ý về mối quan hệ với `HAS_SUBTASK`**: Trong khi `HAS_SUBTASK` (với `parentEntityType: Project`) định nghĩa cấu trúc phân cấp công việc từ `Project` xuống `Task`, `IS_PART_OF_PROJECT` cung cấp một liên kết rõ ràng, trực tiếp từ `Task` đến `Project` của nó. Nó hữu ích cho việc truy vấn trực tiếp tư cách thành viên và vai trò của một `Task` trong một `Project` mà không cần duyệt qua cấu trúc phân cấp.
        * **Ví dụ**: `Task` "Define Database Schema" là một phần chính của `Project` "Ontology V3.2 Development".
            ```yamlyaml
            IS_PART_OF_PROJECT:
              relationshipId: "ipop_8c9d0e1f-2a3b-4c5d-6e7f-8a9b0c1d2e3f"
              taskId: "task_define_schema_2a3b4c5d-6e7f-8a9b-0c1d2e3f4a5b" # ID của Task "Define Database Schema"
              projectId: "proj_ontology_v32_dev_6e7f8a9b-0c1d-2e3f-4a5b6c7d8e9f" # ID của Project "Ontology V3.2 Development"
              assignmentType: "Primary"
              contextualDescription: "Responsible for defining all table structures, relationships, and constraints for the new ontology database as a core deliverable of this project phase."
              assignmentDate: "2024-06-10T10:00:00Z"
              notes: "This task is critical for subsequent data migration and API development tasks within the project."
              creationDate: "2024-06-10T10:05:00Z"
              lastModifiedDate: "2024-06-11T11:30:00Z"
            ```yaml

    *   **7.10. `DETECTED_BY`**
        * **Mô tả**: Liên kết một `Tension` với `Agent` (con người hoặc AI) đã phát hiện hoặc báo cáo `Tension` đó lần đầu tiên. Ghi lại nguồn gốc phát hiện của một `Tension`.
        * **Domain (Nguồn)**: `Tension` (Được xác định bởi `tensionId`)
        * **Range (Đích)**: `Agent` (Được xác định bởi `detectingAgentId`)
        * **Thuộc tính của mối quan hệ `DETECTED_BY`**:
            * ` relationshipId`: `string` (format: `uuid`, primary_key: `true`, required: `true`, unique: `true`, description: "Mã định danh duy nhất cho bản ghi mối quan hệ phát hiện này.")
            * ` tensionId`: `string` (format: `uuid`, required: `true`, foreign_key: `Tension.tensionId`, description: "ID của `Tension` được phát hiện. (Tham chiếu đến Domain)")
            * ` detectingAgentId`: `string` (format: `uuid`, required: `true`, foreign_key: `Agent.agentId`, description: "ID của `Agent` đã phát hiện `Tension`. (Tham chiếu đến Range)")
            * ` detectionMethod`: `string` (required: `true`, enum: [`DirectObservation`, `SystemMonitoringAlert`, `UserFeedback`, `AutomatedAnalysis`, `SensorInput`, `MeetingDiscussion`, `PredictiveModel`, `DataAnomaly`, `AuditFinding`, `SurveyResult`, `Other`], description: "Phương pháp mà `Agent` sử dụng để phát hiện `Tension`.")
            * ` detectionTimestamp`: `datetime` (format: `ISO8601`, required: `true`, default: "current_timestamp", description: "Thời điểm chính xác `Tension` được phát hiện hoặc báo cáo bởi `Agent` này.")
            * ` confidenceLevel`: `float` (optional: `true`, minimum: `0.0`, maximum: `1.0`, description: "Mức độ tin cậy của `Agent` phát hiện về sự tồn tại và bản chất của `Tension` tại thời điểm phát hiện (ví dụ: 0.85 cho 85% tin cậy).")
            * ` initialAssessment`: `string` (optional: `true`, format: `markdown`, description: "Đánh giá hoặc quan sát ban đầu ngắn gọn của `Agent` phát hiện về `Tension`.")
            * ` supportingEvidence`: `string` (optional: `true`, format: `markdown`, description: "Liên kết đến hoặc mô tả về bất kỳ bằng chứng hỗ trợ nào cho việc phát hiện (ví dụ: đoạn log, trích dẫn người dùng, biểu đồ số liệu).")
            * ` status`: `string` (optional: `true`, enum: [`Reported`, `Acknowledged`, `UnderInvestigation`, `FalsePositive`, `Escalated`, `Validated`], default: `Reported`, description: "Trạng thái của sự kiện phát hiện cụ thể này.")
            * ` notes`: `string` (optional: `true`, format: `markdown`, description: "Ghi chú bổ sung liên quan đến sự kiện phát hiện `Tension` này.")
            * ` creationDate`: `datetime` (format: `ISO8601`, required: `true`, readonly: `true`, default: "current_timestamp", description: "Ngày mối quan hệ DETECTED_BY này được tạo.")
            * ` lastModifiedDate`: `datetime` (format: `ISO8601`, required: `true`, readonly: `true`, default: "current_timestamp", auto_update: `true`, description: "Ngày mối quan hệ DETECTED_BY này được cập nhật lần cuối.")
        * **Ví dụ**: Một `AIAgent` giám sát hệ thống phát hiện một `Tension` về hiệu suất API chậm.
            ```yamlyaml
            DETECTED_BY:
              relationshipId: "db_9d0e1f2a-3b4c-5d6e-7f8a-9b0c1d2e3f4a"
              tensionId: "tsn_api_perf_issue_3b4c5d6e-7f8a-9b0c-1d2e3f4a5b6c" # ID của Tension "Slow API Response Time"
              detectingAgentId: "ai_agent_monitor_sys_7f8a9b0c-1d2e-3f4a-5b6c7d8e9f0a" # ID của AIAgent "SystemPerformanceMonitor"
              detectionMethod: "SystemMonitoringAlert"
              detectionTimestamp: "2024-07-20T14:35:10Z"
              confidenceLevel: 0.95
              initialAssessment: "API endpoint /v1/data_query consistently exceeding 2000ms response time threshold over the last 15 minutes. Average response time: 2850ms."
              supportingEvidence: "Link to Grafana dashboard: [API Performance Dashboard](http://grafana.example.com/d/api-perf?var-service=data_query&from=now-1h&to=now)"
              status: "Escalated"
              notes: "Alert triggered based on pre-defined SLOs. Escalated to on-call SRE team."
              creationDate: "2024-07-20T14:35:10Z"
              lastModifiedDate: "2024-07-20T14:40:00Z"
            ```yaml

    *   **7.11. `MANAGES_AGENT`**
        * **Mô tả**: Liên kết một `Agent` (thường là một `Agent` quản lý cấp cao, một `Agentic Governance Engine - AGE`, hoặc một người quản lý) với một `Agent` khác (thường là một `AIAgent` chuyên biệt hoặc một `Agent` cấp dưới) mà nó quản lý, điều phối, giám sát hoặc kiểm soát vòng đời.
        * **Domain (Nguồn)**: `Agent` (Được xác định bởi `managingAgentId` - Agent thực hiện việc quản lý)
        * **Range (Đích)**: `Agent` (Được xác định bởi `managedAgentId` - Agent được quản lý)
        * **Thuộc tính của mối quan hệ `MANAGES_AGENT`**:
            * ` relationshipId`: `string` (format: `uuid`, primary_key: `true`, required: `true`, unique: `true`, description: "Mã định danh duy nhất cho bản ghi mối quan hệ quản lý này.")
            * ` managingAgentId`: `string` (format: `uuid`, required: `true`, foreign_key: `Agent.agentId`, description: "ID của `Agent` thực hiện việc quản lý. (Tham chiếu đến Domain)")
            * ` managedAgentId`: `string` (format: `uuid`, required: `true`, foreign_key: `Agent.agentId`, description: "ID của `Agent` được quản lý. (Tham chiếu đến Range)")
            * ` controlLevel`: `string` (required: `true`, enum: [`DirectControl`, `Supervision`, `Coordination`, `Delegation`, `Orchestration`, `Advisory`, `LifecycleManagement`, `PolicyBased`], default: `Supervision`, description: "Mức độ hoặc loại hình kiểm soát/quản lý được thực hiện.")
            * ` managementFunctions`: `array` of `string` (optional: `true`, enum: [`TaskAssignment`, `PerformanceMonitoring`, `ResourceAllocation`, `LifecycleControl`, `PolicyEnforcement`, `Reporting`, `ErrorHandling`, `LearningSupervision`, `ConfigurationManagement`, `SecurityOversight`, `GoalSetting`], description: "Danh sách các chức năng quản lý cụ thể mà Agent quản lý thực hiện đối với Agent được quản lý.")
            * ` scopeOfManagement`: `string` (optional: `true`, format: `markdown`, description: "Mô tả chi tiết phạm vi quản lý (ví dụ: các tác vụ cụ thể, thông số vận hành, toàn bộ vòng đời, các quyết định chiến lược).")
            * ` isActive`: `boolean` (required: `true`, default: `true`, description: "Cho biết mối quan hệ quản lý này có đang hoạt động hay không.")
            * ` startDate`: `datetime` (format: `ISO8601`, required: `true`, default: "current_timestamp", description: "Ngày và giờ mối quan hệ quản lý này chính thức bắt đầu.")
            * ` endDate`: `datetime` (format: `ISO8601`, optional: `true`, description: "Ngày và giờ mối quan hệ quản lý này kết thúc hoặc dự kiến kết thúc (nếu có).")
            * ` permissionsContext`: `string` (optional: `true`, format: `markdown`, description: "Mô tả các quyền hạn, vai trò hoặc thẩm quyền được cấp cho Agent được quản lý bởi Agent quản lý, hoặc các giới hạn hoạt động được thiết lập.")
            * ` communicationPreferences`: `string` (optional: `true`, format: `markdown`, description: "Các phương thức, kênh hoặc giao thức liên lạc ưu tiên trong mối quan hệ quản lý này (ví dụ: API endpoints, message queues, định dạng báo cáo cụ thể, tần suất họp).")
            * ` notes`: `string` (optional: `true`, format: `markdown`, description: "Ghi chú bổ sung hoặc ngữ cảnh liên quan đến mối quan hệ quản lý này.")
            * ` creationDate`: `datetime` (format: `ISO8601`, required: `true`, readonly: `true`, default: "current_timestamp", description: "Ngày mối quan hệ MANAGES_AGENT này được tạo.")
            * ` lastModifiedDate`: `datetime` (format: `ISO8601`, required: `true`, readonly: `true`, default: "current_timestamp", auto_update: `true`, description: "Ngày mối quan hệ MANAGES_AGENT này được cập nhật lần cuối.")
        * **Ví dụ**: Một `Agent` đóng vai trò `Agentic Governance Engine (AGE)` quản lý vòng đời và chính sách của một `AIAgent` chuyên phân tích dữ liệu.
            ```yamlyaml
            MANAGES_AGENT:
              relationshipId: "ma_0e1f2a3b-4c5d-6e7f-8a9b-0c1d2e3f4a5b"
              managingAgentId: "agent_age_genesis_engine_4c5d6e7f-8a9b-0c1d-2e3f4a5b6c7d" # ID của Agent AGE "GenesisEngine"
              managedAgentId: "agent_ai_data_analyzer_8a9b0c1d-2e3f-4a5b-6c7d8e9f0a1b" # ID của AIAgent "DataAnalyticsSpecialist"
              controlLevel: "LifecycleManagement"
              managementFunctions:
                - "PolicyEnforcement"
                - "PerformanceMonitoring"
                - "ResourceAllocation"
                - "LifecycleControl"
              scopeOfManagement: "Full lifecycle management including deployment, scaling, updates, and decommissioning. Enforces data privacy and operational policies. Monitors performance KPIs and resource consumption."
              isActive: true
              startDate: "2024-01-15T10:00:00Z"
              endDate: null
              permissionsContext: "Managed agent has read-access to specified data sources and can request compute resources within pre-defined limits. All outputs are logged and audited by the managing agent."
              communicationPreferences: "Control commands via secure API. Status reports via gRPC stream. Alerts via dedicated message queue."
              notes: "This AIAgent is critical for real-time business intelligence. Management ensures compliance and optimal performance."
              creationDate: "2024-01-15T10:05:00Z"
              lastModifiedDate: "2024-07-01T11:30:00Z"
            ```yaml

    *   **7.12. `TRIGGERED_BY`**
        * **Mô tả**: Liên kết một `Event` (nguyên nhân hoặc tác nhân kích hoạt) với một `Project` hoặc `Task` (thực thể bị kích hoạt) được khởi tạo, kích hoạt hoặc bị ảnh hưởng như một hệ quả trực tiếp từ sự kiện đó. Ghi lại mối quan hệ nhân quả dẫn đến việc khởi động hoặc thay đổi trạng thái của một Project/Task.
        * **Domain (Nguồn)**: `Event` (Được xác định bởi `triggeringEventId`)
        * **Range (Đích)**: `Project`, `Task` (Được xác định bởi `triggeredEntityId` và `triggeredEntityType`)
        * **Thuộc tính của mối quan hệ `TRIGGERED_BY`**:
            * ` relationshipId`: `string` (format: `uuid`, primary_key: `true`, required: `true`, unique: `true`, description: "Mã định danh duy nhất cho bản ghi mối quan hệ kích hoạt này.")
            * ` triggeringEventId`: `string` (format: `uuid`, required: `true`, foreign_key: `Event.eventId`, description: "ID của `Event` đóng vai trò là tác nhân kích hoạt. (Tham chiếu đến Domain)")
            * ` triggeredEntityId`: `string` (format: `uuid`, required: `true`, description: "ID của `Project` hoặc `Task` bị kích hoạt. (Tham chiếu đến Range)")
            * ` triggeredEntityType`: `string` (required: `true`, enum: [`Project`, `Task`], description: "Loại của thực thể bị kích hoạt. (Tham chiếu đến Range)")
            * ` triggerMechanism`: `string` (optional: `true`, format: `markdown`, description: "Mô tả cách thức cụ thể mà Event gây ra việc Project/Task bị kích hoạt (ví dụ: 'Phản ứng tự động của hệ thống đối với cảnh báo nghiêm trọng', 'Khởi tạo thủ công dựa trên đánh giá sự kiện', 'Quy tắc luồng công việc được xác định trước', 'Giao thức leo thang').")
            * ` triggerTimestamp`: `datetime` (format: `ISO8601`, required: `true`, default: "current_timestamp", description: "Ngày và giờ hành động kích hoạt hoặc liên kết này được chính thức thiết lập hoặc ghi nhận.")
            * ` delayDuration`: `string` (optional: `true`, format: `ISO8601_duration`, description: "Bất kỳ sự chậm trễ nào được lên kế hoạch hoặc quan sát được giữa thời điểm xảy ra Event (`Event.timestamp`) và việc khởi tạo hoặc kích hoạt thực tế của thực thể bị kích hoạt (ví dụ: 'PT1H' cho độ trễ 1 giờ).")
            * ` conditions`: `string` (optional: `true`, format: `markdown`, description: "Bất kỳ điều kiện cụ thể nào cần được đáp ứng cùng với Event để kích hoạt này xảy ra (ví dụ: 'Tính sẵn có của tài nguyên đã được xác nhận', 'Mức độ nghiêm trọng > Cao').")
            * ` expectedOutcomeFromTrigger`: `string` (optional: `true`, format: `markdown`, description: "Kết quả hoặc mục đích chính dự kiến từ việc kích hoạt thực thể này để phản ứng với Event (ví dụ: 'Để giải quyết Tension đã báo cáo', 'Để bắt đầu một chu kỳ phát triển tính năng mới').")
            * ` status`: `string` (optional: `true`, enum: [`PendingInitiation`, `ActivelyProcessing`, `AwaitingResources`, `CompletedSuccessfully`, `Cancelled`, `FailedToExecute`, `OnHold`, `Deferred`], default: `PendingInitiation`, description: "Trạng thái phản ứng hoặc vòng đời của thực thể bị kích hoạt liên quan cụ thể đến kích hoạt này.")
            * ` notes`: `string` (optional: `true`, format: `markdown`, description: "Ghi chú bổ sung hoặc ngữ cảnh liên quan đến mối quan hệ kích hoạt này.")
            * ` creationDate`: `datetime` (format: `ISO8601`, required: `true`, readonly: `true`, default: "current_timestamp", description: "Ngày mối quan hệ TRIGGERED_BY này được tạo.")
            * ` lastModifiedDate`: `datetime` (format: `ISO8601`, required: `true`, readonly: `true`, default: "current_timestamp", auto_update: `true`, description: "Ngày mối quan hệ TRIGGERED_BY này được cập nhật lần cuối.")
        * **Ví dụ**: Một `TensionEvent` về việc website lỗi thời đã kích hoạt việc đề xuất một `Project` mới để làm lại website.
            ```yamlyaml
            TRIGGERED_BY:
              relationshipId: "tb_1f2a3b4c-5d6e-7f8a-9b0c-1d2e3f4a5b6c"
              triggeringEventId: "evt_tension_website_outdated_5d6e7f8a-9b0c-1d2e-3f4a5b6c7d8e" # ID của TensionEvent "Outdated Corporate Website"
              triggeredEntityId: "proj_website_revamp_proposal_9b0c1d2e-3f4a-5b6c-7d8e9f0a1b2c" # ID của Project "Website Revamp Proposal"
              triggeredEntityType: "Project"
              triggerMechanism: "Manual initiation following management review of the tension event and its impact analysis."
              triggerTimestamp: "2024-07-22T10:00:00Z"
              delayDuration: "P2D" # Project proposal initiated 2 days after event was formally logged
              conditions: "- Budget allocation for initial analysis approved.\n- Key stakeholders available for kickoff meeting."
              expectedOutcomeFromTrigger: "Develop a comprehensive project plan and secure funding for a full website overhaul to address the identified tension and improve user engagement."
              status: "PendingInitiation" # Project proposal is pending, awaiting formal start
              notes: "This project aims to modernize the company's online presence."
              creationDate: "2024-07-22T10:05:00Z"
              lastModifiedDate: "2024-07-22T11:30:00Z"
            ```yaml

    *   **7.13. `CREATES_KNOWLEDGE`**
        * **Mô tả**: Liên kết một thực thể nguồn (ví dụ: `Event`, `Project`, `Task`, `AgentAction`) với một `KnowledgeSnippet` được tạo ra hoặc thu thập được như một kết quả hoặc sản phẩm của thực thể nguồn đó. Ghi lại nguồn gốc và ngữ cảnh của việc tạo ra tri thức.
        * **Domain (Nguồn)**: `Event`, `Project`, `Task`, `AgentAction` (Được xác định bởi `sourceEntityId` và `sourceEntityType`)
        * **Range (Đích)**: `KnowledgeSnippet` (Được xác định bởi `knowledgeSnippetId`)
        * **Thuộc tính của mối quan hệ `CREATES_KNOWLEDGE`**:
            * ` relationshipId`: `string` (format: `uuid`, primary_key: `true`, required: `true`, unique: `true`, description: "Mã định danh duy nhất cho bản ghi mối quan hệ tạo tri thức này.")
            * ` sourceEntityId`: `string` (format: `uuid`, required: `true`, description: "ID của `Event`, `Project`, `Task` hoặc `AgentAction` đã tạo ra tri thức. (Tham chiếu đến Domain)")
            * ` sourceEntityType`: `string` (required: `true`, enum: [`Event`, `Project`, `Task`, `AgentAction`], description: "Loại của thực thể nguồn đã tạo ra tri thức. (Tham chiếu đến Domain)")
            * ` knowledgeSnippetId`: `string` (format: `uuid`, required: `true`, foreign_key: `KnowledgeSnippet.snippetId`, description: "ID của `KnowledgeSnippet` được tạo ra. (Tham chiếu đến Range)")
            * ` creationContext`: `string` (optional: `true`, format: `markdown`, description: "Mô tả ngữ cảnh hoặc hoàn cảnh mà tri thức được tạo ra (ví dụ: 'Phân tích sau sự cố của dự án thất bại', 'Bài học từ giai đoạn thử nghiệm A/B', 'Kết quả của một nhiệm vụ nghiên cứu cụ thể').")
            * ` knowledgeType`: `string` (optional: `true`, enum: [`BestPractice`, `LessonLearned`, `FactualData`, `ProcessImprovement`, `TechnicalInsight`, `UserFeedbackSummary`, `CompetitiveAnalysis`, `StandardOperatingProcedure`, `CaseStudy`, `Tutorial`], default: `LessonLearned`, description: "Phân loại loại tri thức được thu thập.")
            * ` relevanceScore`: `float` (optional: `true`, minimum: `0.0`, maximum: `1.0`, description: "Điểm số cho biết mức độ liên quan hoặc tầm quan trọng được nhận thức của đoạn tri thức này, có thể được gán bởi agent hoặc quy trình tạo ra.")
            * ` validationStatus`: `string` (optional: `true`, enum: [`Unvalidated`, `PendingReview`, `Validated`, `Disputed`, `Archived`, `Obsolete`], default: `Unvalidated`, description: "Trạng thái xác thực của tri thức được tạo ra.")
            * ` validatedByAgentId`: `string` (format: `uuid`, optional: `true`, foreign_key: `Agent.agentId`, description: "ID của `Agent` đã xác thực đoạn tri thức này, nếu có.")
            * ` validationDate`: `datetime` (format: `ISO8601`, optional: `true`, description: "Ngày xác thực, nếu có.")
            * ` accessControl`: `string` (optional: `true`, enum: [`Public`, `Internal`, `TeamSpecific`, `RoleBased`, `Restricted`, `Confidential`], default: `Internal`, description: "Xác định mức độ truy cập cho đoạn tri thức này bắt nguồn từ nguồn này.")
            * ` notes`: `string` (optional: `true`, format: `markdown`, description: "Ghi chú bổ sung về quy trình tạo tri thức hoặc chính đoạn tri thức đó.")
            * ` creationDate`: `datetime` (format: `ISO8601`, required: `true`, readonly: `true`, default: "current_timestamp", description: "Ngày mối quan hệ CREATES_KNOWLEDGE này được tạo.")
            * ` lastModifiedDate`: `datetime` (format: `ISO8601`, required: `true`, readonly: `true`, default: "current_timestamp", auto_update: `true`, description: "Ngày mối quan hệ CREATES_KNOWLEDGE này được cập nhật lần cuối.")
        * **Ví dụ**: Một `LearningEvent` phát sinh từ việc hoàn thành một `Project` tạo ra một `KnowledgeSnippet` về một bài học kinh nghiệm.
            ```yamlyaml
            CREATES_KNOWLEDGE:
              relationshipId: "ck_2a3b4c5d-6e7f-8a9b-0c1d-2e3f4a5b6c7d"
              sourceEntityId: "evt_learning_project_alpha_completed_6e7f8a9b-0c1d-2e3f4a5b6c7d8e9f" # ID của LearningEvent "Project Alpha Completion Learnings"
              sourceEntityType: "Event"
              knowledgeSnippetId: "ks_lesson_agile_sprint_planning_0c1d2e3f-4a5b-6c7d-8e9f0a1b2c3d" # ID của KnowledgeSnippet "Effective Agile Sprint Planning Techniques"
              creationContext: "Post-project review meeting for Project Alpha identified key learnings in sprint planning efficiency."
              knowledgeType: "LessonLearned"
              relevanceScore: 0.9
              validationStatus: "Validated"
              validatedByAgentId: "agent_pm_jane_doe_4a5b6c7d-8e9f-0a1b-2c3d4e5f6a7b"
              validationDate: "2024-07-25T16:00:00Z"
              accessControl: "Internal"
              notes: "This snippet details a new approach to backlog grooming that significantly reduced planning overhead."
              creationDate: "2024-07-25T14:30:00Z"
              lastModifiedDate: "2024-07-25T16:05:00Z"
            ```yaml

    *   **7.14. `USES_KNOWLEDGE`**
        * **Mô tả**: Liên kết một thực thể (ví dụ: `Agent`, `Project`, `Task`, `Workflow`, `AgentAction`) sử dụng hoặc áp dụng một `KnowledgeSnippet` trong quá trình hoạt động, ra quyết định hoặc thực thi của nó. Ghi lại việc tiêu thụ và ứng dụng tri thức.
        * **Domain (Nguồn)**: `Agent`, `Project`, `Task`, `Workflow`, `AgentAction` (Được xác định bởi `usingEntityId` và `usingEntityType`)
        * **Range (Đích)**: `KnowledgeSnippet` (Được xác định bởi `knowledgeSnippetId`)
        * **Thuộc tính của mối quan hệ `USES_KNOWLEDGE`**:
            * ` relationshipId`: `string` (format: `uuid`, primary_key: `true`, required: `true`, unique: `true`, description: "Mã định danh duy nhất cho bản ghi mối quan hệ sử dụng tri thức này.")
            * ` usingEntityId`: `string` (format: `uuid`, required: `true`, description: "ID của `Agent`, `Project`, `Task`, hoặc `Workflow` sử dụng tri thức. (Tham chiếu đến Domain)")
            * ` usingEntityType`: `string` (required: `true`, enum: [`Agent`, `Project`, `Task`, `Workflow`, `AgentAction`], description: "Loại của thực thể sử dụng tri thức. (Tham chiếu đến Domain)")
            * ` knowledgeSnippetId`: `string` (format: `uuid`, required: `true`, foreign_key: `KnowledgeSnippet.snippetId`, description: "ID của `KnowledgeSnippet` đang được sử dụng. (Tham chiếu đến Range)")
            * ` usageContext`: `string` (optional: `true`, format: `markdown`, description: "Mô tả cách thức và lý do đoạn tri thức được thực thể sử dụng (ví dụ: 'Áp dụng best practice cho thiết kế API', 'Sử dụng để khắc phục sự cố lặp lại', 'Thông báo quyết định chiến lược cho giai đoạn 2 của dự án').")
            * ` usageTimestamp`: `datetime` (format: `ISO8601`, required: `true`, default: "current_timestamp", description: "Ngày và giờ cụ thể khi tri thức được truy cập hoặc áp dụng.")
            * ` applicationOutcome`: `string` (optional: `true`, format: `markdown`, description: "Kết quả hoặc tác động của việc áp dụng tri thức này (ví dụ: 'Giảm số lượng lỗi xuống 15%', 'Giải quyết thành công khiếu nại của khách hàng', 'Cải thiện hiệu quả quy trình').")
            * ` confidenceInApplicability`: `float` (optional: `true`, minimum: `0.0`, maximum: `1.0`, description: "Mức độ tin cậy của thực thể sử dụng (hoặc người vận hành của nó) rằng đoạn tri thức này có thể áp dụng cho ngữ cảnh hiện tại.")
            * ` feedbackOnUsefulness`: `string` (optional: `true`, format: `markdown`, description: "Phản hồi được cung cấp bởi thực thể sử dụng hoặc người vận hành của nó về tính hữ
            * ` versionUsed`: `string` (optional: `true`, description: "Nếu `KnowledgeSnippet` được phiên bản hóa, điều này cho biết phiên bản cụ thể được sử dụng.")
            * ` notes`: `string` (optional: `true`, format: `markdown`, description: "Ghi chú bổ sung về trường hợp sử dụng tri thức cụ thể này.")
            * ` creationDate`: `datetime` (format: `ISO8601`, required: `true`, readonly: `true`, default: "current_timestamp", description: "Ngày mối quan hệ USES_KNOWLEDGE này được tạo.")
            * ` lastModifiedDate`: `datetime` (format: `ISO8601`, required: `true`, readonly: `true`, default: "current_timestamp", auto_update: `true`, description: "Ngày mối quan hệ USES_KNOWLEDGE này được cập nhật lần cuối.")
        * **Ví dụ**: Một `Agent` (ví dụ: một AI Agent hỗ trợ khách hàng) sử dụng một `KnowledgeSnippet` (ví dụ: một quy trình xử lý sự cố) để thực hiện một `Task` (ví dụ: giải quyết một yêu cầu hỗ trợ của khách hàng).
            ```yamlyaml
            USES_KNOWLEDGE:
              relationshipId: "uk_3b4c5d6e-7f8a-9b0c-1d2e-3f4a5b6c7d8e"
              usingEntityId: "agent_support_bot_alpha_7f8a9b0c-1d2e-3f4a-5b6c-7d8e9f0a1b2c" # ID của Agent "SupportBot Alpha"
              usingEntityType: "Agent"
              knowledgeSnippetId: "ks_troubleshoot_login_issue_1d2e3f4a-5b6c-7d8e-9f0a1b2c3d4e" # ID của KnowledgeSnippet "Troubleshooting Login Issues v1.2"
              usageContext: "Agent applied the troubleshooting steps from the knowledge snippet to guide a user experiencing login difficulties during a support interaction (Task: tsk_resolve_user_login_7f8a)."
              usageTimestamp: "2024-07-28T15:30:00Z"
              applicationOutcome: "User successfully logged in after following step 3 of the provided procedure. Ticket resolved."
              confidenceInApplicability: 0.95
              feedbackOnUsefulness: "The procedure was clear and effective. Step 2 could be clarified slightly for non-technical users."
            * ` relationshipId`: `string` (format: `uuid`, primary_key: `true`, required: `true`, unique: `true`, description: "Mã định danh duy nhất cho bản ghi mối quan hệ này.")
            * ` sourceEntityId`: `string` (format: `uuid`, required: `true`, description: "ID của thực thể nguồn. (Tham chiếu đến Domain)")
            * ` sourceEntityType`: `string` (required: `true`, enum: [`Project`, `Task`, `Agent`, `Resource`, `Tension`, `Event`, `KnowledgeSnippet`, `Goal`, `Metric`, `User`, `Organization`, `Artifact`, `Decision`, `Risk`, `Requirement`, `Comment`, `File`, `Message`, `Workflow`, `AgentAction`, `AnyClass`], description: "Loại của thực thể nguồn. (Tham chiếu đến Domain - danh sách này mang tính minh họa, sẽ bao gồm tất cả các lớp thực thể được định nghĩa trong ontology).")
            * ` targetEntityId`: `string` (format: `uuid`, required: `true`, description: "ID của thực thể đích. (Tham chiếu đến Range)")
            * ` targetEntityType`: `string` (required: `true`, enum: [`Project`, `Task`, `Agent`, `Resource`, `Tension`, `Event`, `KnowledgeSnippet`, `Goal`, `Metric`, `User`, `Organization`, `Artifact`, `Decision`, `Risk`, `Requirement`, `Comment`, `File`, `Message`, `Workflow`, `AgentAction`, `AnyClass`], description: "Loại của thực thể đích. (Tham chiếu đến Range - danh sách này mang tính minh họa).")
            * ` relationType`: `string` (required: `true`, format: `user_defined_tag` or `predefined_enum`, description: "Một thẻ do người dùng định nghĩa hoặc từ một enum được xác định trước, mô tả bản chất của mối quan hệ (ví dụ: `SimilarTo`, `AlternativeFor`, `InspiredBy`, `BlockedBy`, `Complements`, `Contradicts`, `DerivedFrom`, `BasedOn`, `DiscussedIn`, `MentionedIn`, `PotentialDuplicateOf`, `FollowUpTo`, `Precedes`, `Supersedes`, `Exemplifies`, `References`, `Impacts`, `DependsOn`, `RelatedIssue`). Phải cụ thể hơn là chỉ 'Related'.")
            * ` strength`: `float` (optional: `true`, minimum: `0.0`, maximum: `1.0`, description: "Điểm số cho biết sức mạnh hoặc độ tin cậy của mối quan hệ này, nếu có.")
            * ` context`: `string` (optional: `true`, format: `markdown`, description: "Mô tả chi tiết hoặc ngữ cảnh giải thích tại sao và làm thế nào hai thực thể này có liên quan.")
            * ` bidirectional`: `boolean` (optional: `true`, default: `false`, description: "Cho biết liệu mối quan hệ có tính hai chiều với cùng `relationType` hay không (ví dụ: `SimilarTo` thường là hai chiều). Nếu false, mối quan hệ được định hướng từ nguồn đến đích.")
            * ` discoveredByAgentId`: `string` (format: `uuid`, optional: `true`, foreign_key: `Agent.agentId`, description: "ID của `Agent` đã phát hiện hoặc khẳng định mối quan hệ này, nếu có.")
            * ` discoveryTimestamp`: `datetime` (format: `ISO8601`, optional: `true`, description: "Dấu thời gian khi mối quan hệ này được phát hiện hoặc khẳng định.")
            * ` notes`: `string` (optional: `true`, format: `markdown`, description: "Ghi chú bổ sung.")
            * ` creationDate`: `datetime` (format: `ISO8601`, required: `true`, readonly: `true`, default: "current_timestamp", description: "Ngày mối quan hệ RELATED_TO này được tạo.")
            * ` lastModifiedDate`: `datetime` (format: `ISO8601`, required: `true`, readonly: `true`, default: "current_timestamp", auto_update: `true`, description: "Ngày mối quan hệ RELATED_TO này được cập nhật lần cuối.")
        * **Ví dụ**: Một `KnowledgeSnippet` về một kỹ thuật tối ưu hóa code được cho là `SimilarTo` một `KnowledgeSnippet` khác ghi lại một giải pháp tương tự trong một dự án trước đó.
            ```yamlyaml
            RELATED_TO:
              relationshipId: "rt_4c5d6e7f-8a9b-0c1d-2e3f-4a5b6c7d8e9f"
              sourceEntityId: "ks_code_optimization_tech_a_0c1d2e3f-4a5b-6c7d-8e9f0a1b2c3d"
              sourceEntityType: "KnowledgeSnippet"
              targetEntityId: "ks_project_gamma_perf_solution_8e9f0a1b-2c3d-4e5f-6a7b8c9d0e1f"
              targetEntityType: "KnowledgeSnippet"
              relationType: "SimilarTo"
              strength: 0.85
              context: "Both knowledge snippets describe approaches to reduce database query latency, though using slightly different caching strategies. Discovered during a knowledge consolidation effort."
              bidirectional: true
              discoveredByAgentId: "agent_knowledge_curator_1_2c3d4e5f-6a7b-8c9d-0e1f2a3b4c5d"
              discoveryTimestamp: "2024-07-29T11:00:00Z"
              notes: "Consider merging or cross-referencing these snippets more formally."
              creationDate: "2024-07-29T11:05:00Z"
              lastModifiedDate: "2024-07-29T11:05:00Z"
            ```yaml
8. Hệ thống Phân cấp Sự kiện (Event Hierarchy)

**8.1. Giới thiệu (Introduction)**
Mục này định nghĩa hệ thống phân cấp cho các loại `Event` (Sự kiện) khác nhau đã được mô tả trong Mục 6 (Các Thực thể Event). Hệ thống phân cấp sự kiện giúp tổ chức và cấu trúc các loại sự kiện, cho phép xử lý sự kiện một cách đa hình, truy vấn dữ liệu sự kiện hiệu quả hơn, và dễ dàng mở rộng với các loại sự kiện mới trong tương lai. Bằng cách hiểu rõ mối quan hệ cha-con giữa các sự kiện, hệ thống TRM-OS có thể đăng ký lắng nghe các sự kiện ở các mức độ trừu tượng khác nhau (ví dụ: lắng nghe một `SystemEvent` chung chung hoặc một `SecurityEvent` cụ thể).

**8.2. Cấu trúc Phân cấp Sự kiện (Event Hierarchy Structure)**
Tất cả các loại sự kiện đều kế thừa từ một `Event` cơ sở (Mục 6.1). Dưới đây là cấu trúc phân cấp chi tiết, trong đó các mục con thụt vào biểu thị sự kế thừa từ mục cha gần nhất.

*   **`Event`** (Mục 6.1 - Thực thể Event Cơ sở)
    * ` UserInteractionEvent` (Mục 6.2)
    * ` SystemEvent` (Mục 6.3)
        * ` SecurityEvent` (Mục 6.14)
        * ` MetricThresholdEvent` (Mục 6.20)
        * ` AnomalyEvent` (Mục 6.21)
        * ` FailureEvent` (Mục 6.17 - Được xem xét là một loại `SystemEvent` khi phản ánh sự cố kỹ thuật của hệ thống. Nếu phạm vi rộng hơn, có thể được xem xét lại vị trí.)
    * ` TensionEvent` (Mục 6.4)
    * ` GoalLifecycleEvent` (Mục 6.5)
    * ` ProjectLifecycleEvent` (Mục 6.6)
    * ` TaskLifecycleEvent` (Mục 6.7)
    * ` ResourceLifecycleEvent` (Mục 6.8)
    * ` AgentLifecycleEvent` (Mục 6.9)
    * ` KnowledgeLifecycleEvent` (Mục 6.10)
    * ` CommunicationEvent` (Mục 6.11)
    * ` LearningEvent` (Mục 6.12)
    * ` DecisionEvent` (Mục 6.13)
    * ` ExternalEvent` (Mục 6.15)
    * ` WinEvent` (Mục 6.16)
    * ` RecognitionEvent` (Mục 6.18)
    * ` FeedbackEvent` (Mục 6.19)
    * ` CustomBusinessEvent` (Mục 6.22)

*(Lưu ý: Vị trí của `FailureEvent` (6.17) dưới `SystemEvent` phản ánh giả định rằng hầu hết các lỗi được theo dõi ban đầu là lỗi hệ thống. Nếu `FailureEvent` cần bao hàm các loại thất bại nghiệp vụ hoặc quy trình không trực tiếp do lỗi kỹ thuật hệ thống, nó có thể được nâng cấp thành một nhánh riêng hoặc được phân loại dưới một `OutcomeEvent` tổng quát hơn trong tương lai.)*

**8.3. Diễn giải Phân cấp (Hierarchy Interpretation)**
*   **`Event` cơ sở**: Là gốc của tất cả các sự kiện, chứa các thuộc tính chung như `eventId`, `timestamp`, `source`, `eventVersion`, `correlationId`, `metadata`.
*   **Nhánh `SystemEvent`**: Bao gồm các sự kiện liên quan đến hoạt động nội bộ, trạng thái và sự cố của hệ thống TRM-OS.
    * ` SecurityEvent`: Các sự kiện liên quan đến an ninh, quyền truy cập, và các mối đe dọa bảo mật.
    * ` MetricThresholdEvent`: Kích hoạt khi một chỉ số hiệu suất hoặc tài nguyên hệ thống vượt qua ngưỡng đã định.
    * ` AnomalyEvent`: Phát hiện các hành vi, mẫu dữ liệu, hoặc hoạt động bất thường của hệ thống.
    * ` FailureEvent`: Ghi nhận các lỗi, sự cố kỹ thuật, hoặc tình trạng không hoạt động của các thành phần hệ thống.
*   **Các sự kiện vòng đời (Lifecycle Events)**: Như `ProjectLifecycleEvent`, `TaskLifecycleEvent`, `AgentLifecycleEvent`, v.v., theo dõi các giai đoạn và thay đổi trạng thái quan trọng trong vòng đời của các thực thể cốt lõi của TRM-OS. Chúng kế thừa trực tiếp từ `Event` cơ sở.
*   **Các sự kiện tương tác và nghiệp vụ**: Bao gồm `UserInteractionEvent`, `TensionEvent`, `CommunicationEvent`, `LearningEvent`, `DecisionEvent`, `WinEvent`, `FeedbackEvent`, và `CustomBusinessEvent`. Các sự kiện này thể hiện các khía cạnh đa dạng của hoạt động, tương tác, và kết quả trong TRM-OS. Chúng cũng kế thừa trực tiếp từ `Event` cơ sở trong cấu trúc hiện tại.
*   **`ExternalEvent`**: Đại diện cho các sự kiện từ các nguồn hoặc hệ thống bên ngoài có ảnh hưởng hoặc cần được ghi nhận bởi TRM-OS.

Sự phân cấp này, đối với nhiều loại sự kiện, là tương đối "phẳng", nghĩa là nhiều sự kiện chuyên biệt kế thừa trực tiếp từ `Event` gốc. Điều này mang lại sự linh hoạt trong việc định nghĩa các sự kiện mới nhưng vẫn đảm bảo tính nhất quán thông qua các thuộc tính chung của `Event` cơ sở. Các nhánh sâu hơn (như dưới `SystemEvent`) được hình thành khi có một nhóm sự kiện rõ ràng chia sẻ một ngữ cảnh chung cụ thể hơn và có thể có các thuộc tính chung bổ sung cho nhánh đó.

**8.4. Ứng dụng của Phân cấp Sự kiện (Applications of Event Hierarchy)**
*   **Xử lý Sự kiện Đa hình (Polymorphic Event Handling)**: Các thành phần lắng nghe sự kiện (event listeners/subscribers) có thể được thiết kế để xử lý các loại sự kiện cha, và logic này sẽ tự động áp dụng cho tất cả các loại sự kiện con. Ví dụ, một listener cho `SystemEvent` có thể xử lý chung cho `SecurityEvent`, `MetricThresholdEvent`, `AnomalyEvent`, và `FailureEvent`, trong khi các listener chuyên biệt hơn có thể xử lý từng loại con cụ thể.
*   **Truy vấn và Phân tích Dữ liệu (Data Querying and Analysis)**: Cho phép truy vấn và tổng hợp dữ liệu sự kiện một cách hiệu quả. Ví dụ, có thể dễ dàng "lấy tất cả `LifecycleEvent` liên quan đến `Project` X" hoặc "phân tích tần suất của tất cả các loại `SystemEvent` trong tuần qua".
*   **Định tuyến và Lọc Sự kiện (Event Routing and Filtering)**: Hệ thống bus sự kiện hoặc message broker có thể sử dụng thông tin phân cấp để định tuyến hoặc lọc sự kiện đến các consumer phù hợp.
*   **Mở rộng Hệ thống (System Extensibility)**: Khi các yêu cầu mới phát sinh, các loại sự kiện mới có thể được dễ dàng thêm vào hệ thống bằng cách kế thừa từ `Event` cơ sở hoặc từ một loại sự kiện hiện có phù hợp trong hệ thống phân cấp. Điều này đảm bảo tính nhất quán và giảm thiểu tác động đến các thành phần hiện có.
*   **Thông báo và Cảnh báo (Notifications and Alerting)**: Cấu hình các quy tắc thông báo và hệ thống cảnh báo dựa trên các loại sự kiện cụ thể hoặc các nhóm sự kiện trong hệ thống phân cấp (ví dụ: gửi cảnh báo cho tất cả `SecurityEvent` có mức độ nghiêm trọng cao).
9. Các Quy tắc và Ràng buộc Ontology (Ontology Rules & Constraints)

**9.1. Giới thiệu (Introduction)**
Phần này xác định các quy tắc và ràng buộc khác nhau chi phối tính toàn vẹn, nhất quán và hợp lệ của dữ liệu trong ontology TRM-OS. Những quy tắc này rất cần thiết để duy trì chất lượng dữ liệu và đảm bảo rằng ontology phản ánh chính xác logic nghiệp vụ và các ràng buộc hoạt động dự kiến. Các quy tắc và ràng buộc giúp:
*   Đảm bảo tính nhất quán và chính xác của dữ liệu.
*   Hỗ trợ suy luận logic và khám phá tri thức mới.
*   Phát hiện các điểm bất thường, mâu thuẫn hoặc dữ liệu không hợp lệ.
*   Hướng dẫn hành vi của các AI Agent và quy trình tự động, đảm bảo chúng hoạt động dựa trên dữ liệu đáng tin cậy.
*   Tăng cường độ tin cậy và khả năng bảo trì của toàn bộ hệ thống TRM-OS.

**9.2. Các loại Quy tắc và Ràng buộc (Types of Rules and Constraints)**

*   **9.2.1. Ràng buộc về Tính đầy đủ (Completeness Constraints)**
    *   **Mô tả**: Đảm bảo rằng các thông tin thiết yếu luôn có mặt cho một thực thể hoặc mối quan hệ. Các thuộc tính bắt buộc phải được cung cấp.
    *   **Ví dụ TRM-OS**:
        *   Một `Task` phải luôn có giá trị cho các thuộc tính `taskId`, `name`, `status`, và `projectId` (nếu nó là một phần của dự án).
        *   Một `User` phải có `userId` và `email` (hoặc một định danh liên lạc chính khác).
        *   Mối quan hệ `REQUIRES_RESOURCE` phải luôn chỉ định `requesterEntityId`, `requesterEntityType`, `resourceId`, và `quantity`.

*   **9.2.2. Ràng buộc về Tính nhất quán (Consistency Constraints)**
    *   **Mô tả**: Ngăn chặn các mâu thuẫn logic trong dữ liệu. Dữ liệu phải tuân thủ các quy tắc logic nội tại và không được tự mâu thuẫn.
    *   **Ví dụ TRM-OS**:
        *   Một `Task` không thể đồng thời có `status` là `Completed` và `progressPercentage` < 100.
        *   Nếu `Project.status` là `Archived`, thì không có `Task` nào thuộc `Project` đó có thể có `status` là `InProgress`.
        * ` Resource.allocationDate` trong mối quan hệ `REQUIRES_RESOURCE` không được sớm hơn `Resource.requestDate`.

*   **9.2.3. Ràng buộc về Số lượng (Cardinality Constraints)**
    *   **Mô tả**: Xác định số lượng (tối thiểu, tối đa, hoặc chính xác) các thực thể có thể tham gia vào một mối quan hệ hoặc số lần một thuộc tính có thể xuất hiện.
    *   **Ví dụ TRM-OS**:
        *   Một `Project` phải được liên kết với ít nhất một `Goal` (ví dụ, thông qua mối quan hệ `ALIGNED_WITH_GOAL`). (Số lượng: 1..N cho `Goal` trên mỗi `Project`).
        *   Một `Task` chỉ có thể được `ASSIGNED_TO` một `Agent` tại một thời điểm (Số lượng: 0..1 hoặc 1..1 cho `Agent` trên mỗi `Task` cho vai trò người thực hiện chính).
        *   Một `Tension` phải được `DETECTED_BY` đúng một `Agent` (Số lượng: 1..1).

*   **9.2.4. Ràng buộc về Giá trị (Value Constraints)**
    *   **Mô tả**: Giới hạn các giá trị hợp lệ cho một thuộc tính, thường thông qua các tập giá trị được định trước (enum), khoảng giá trị, hoặc các mẫu định dạng.
    *   **Ví dụ TRM-OS**:
        * ` Task.priority` phải là một trong các giá trị enum đã định: `Critical`, `High`, `Medium`, `Low`.
        * ` Resource.quantityAvailable` phải là một số không âm (>= 0).
        * ` Metric.value` khi `Metric.metricType` là `Percentage` phải nằm trong khoảng từ 0 đến 100.
        * ` User.email` phải tuân theo một định dạng email hợp lệ.

*   **9.2.5. Ràng buộc về Mối quan hệ (Relationship Constraints)**
    *   **Mô tả**: Các quy tắc điều chỉnh cách các thực thể cụ thể có thể hoặc không thể liên kết với nhau, bao gồm các ràng buộc về domain và range của mối quan hệ.
    *   **Ví dụ TRM-OS**:
        *   Một `Agent` không thể `MANAGES_AGENT` chính nó (`managingAgentId` != `managedAgentId`).
        *   Trong mối quan hệ `REQUIRES_RESOURCE`, thực thể được tham chiếu bởi `resourceId` phải là một thực thể loại `Resource`.
        *   Một `Task` không thể `HAS_SUBTASK` một `Task` là cha hoặc ông bà của nó (ngăn chặn chu trình trong cấu trúc phân cấp nhiệm vụ).

*   **9.2.6. Ràng buộc về Kiểu dữ liệu (Data Type Constraints)**
    *   **Mô tả**: Đảm bảo rằng các giá trị của thuộc tính tuân theo kiểu dữ liệu đã được định nghĩa trong schema (ví dụ: `string`, `integer`, `float`, `boolean`, `datetime`, `uuid`, `markdown`, `ISO8601_duration`).
    *   **Ví dụ TRM-OS**:
        * ` Project.creationDate` phải là một giá trị `datetime` hợp lệ theo định dạng ISO8601.
        * ` Task.estimatedEffortHours` phải là một số `float`.
        * ` KnowledgeSnippet.snippetId` phải là một `uuid` hợp lệ.

*   **9.2.7. Ràng buộc Suy luận và Tính toán (Inferential and Calculation Rules / Axioms)**
    *   **Mô tả**: Các quy tắc cho phép hệ thống tự động suy ra thông tin mới, mối quan hệ mới, hoặc tính toán các giá trị thuộc tính dựa trên dữ liệu hiện có. Đây có thể là các tiên đề (axioms) của ontology.
    *   **Ví dụ TRM-OS**:
        *   Nếu `TaskA HAS_SUBTASK TaskB` và `TaskB HAS_SUBTASK TaskC`, thì có thể suy ra một mối quan hệ gián tiếp `TaskA HAS_ANCESTOR_OF TaskC` (hoặc tương tự).
        * ` Project.overallProgress` có thể được tính toán dựa trên `progressPercentage` và `weight` của các `Task` con.
        *   Nếu `EventA TRIGGERED_BY EventB`, và `EventB` có `criticality` là `High`, thì `EventA` có thể được kế thừa một mức độ ưu tiên xử lý cao.

*   **9.2.8. Ràng buộc Tạm thời (Temporal Constraints)**
    *   **Mô tả**: Các quy tắc liên quan đến thứ tự thời gian, khoảng thời gian, và các mối quan hệ thời gian giữa các sự kiện hoặc trạng thái của thực thể.
    *   **Ví dụ TRM-OS**:
        * ` Task.actualEndDate` không được sớm hơn `Task.actualStartDate`.
        * ` Project.plannedStartDate` phải trước `Project.plannedEndDate`.
        *   Một `RecognitionEvent.timestamp` phải xảy ra sau hoặc bằng `WinEvent.timestamp` mà nó công nhận.
        *   Nếu một `Task` có `dependencyType` là `FinishToStart_FS` với một `Task` tiền nhiệm, `actualStartDate` của nó không thể bắt đầu trước khi `Task` tiền nhiệm có `status` là `Completed`.

**9.3. Ngôn ngữ Định nghĩa Quy tắc và Tính Chính quy (Rule Definition Language and Formalism)**
Việc định nghĩa và thực thi các quy tắc và ràng buộc này có thể được thực hiện thông qua nhiều cơ chế khác nhau, tùy thuộc vào kiến trúc công nghệ của TRM-OS:
*   **SHACL (Shapes Constraint Language)**: Nếu ontology được triển khai bằng RDF, SHACL là một ngôn ngữ chuẩn của W3C để xác thực đồ thị RDF dựa trên một tập hợp các điều kiện (shapes).
*   **SWRL (Semantic Web Rule Language)**: Cho phép viết các quy tắc suy luận Horn-like trên các ontology OWL.
*   **OWL Axioms**: Nhiều ràng buộc (ví dụ: cardinality, domain/range, disjointness) có thể được biểu diễn trực tiếp bằng các axiom trong OWL.
*   **Quy tắc Nghiệp vụ Tùy chỉnh (Custom Business Rules)**: Được triển khai trong logic ứng dụng (ví dụ: trong các API services, AI agents) để xác thực dữ liệu trước khi lưu trữ hoặc trong quá trình xử lý.
*   **Ràng buộc ở Mức Cơ sở dữ liệu (Database-Level Constraints)**: Sử dụng các tính năng của hệ quản trị cơ sở dữ liệu (ví dụ: `NOT NULL`, `UNIQUE`, `FOREIGN KEY`, `CHECK constraints`, triggers) để thực thi các quy tắc.
*   **JSON Schema / OpenAPI Specs**: Để xác thực cấu trúc và kiểu dữ liệu của các đối tượng dữ liệu và payload API.

Một cách tiếp cận kết hợp thường là hiệu quả nhất, sử dụng các chuẩn ontology khi có thể và bổ sung bằng logic nghiệp vụ tùy chỉnh cho các quy tắc phức tạp hơn.

**9.4. Ví dụ về Quy tắc và Ràng buộc Cụ thể cho TRM-OS (Examples of Specific Rules and Constraints for TRM-OS)**

1.  **Completeness**: `Project.projectId`, `Project.name`, và `Project.status` là các thuộc tính bắt buộc.
2.  **Completeness**: Mọi `Tension` phải có một `description` và một `detectedByAgentId`.
3.  **Consistency**: Nếu `Task.status` là `Completed`, thì `Task.progressPercentage` phải là `100`. Ngược lại, nếu `Task.progressPercentage` là `100`, `Task.status` nên được cập nhật thành `Completed` (có thể là một quy tắc suy luận hoặc một hành động được kích hoạt).
4.  **Consistency**: Một `Resource` không thể có `quantityAllocated` lớn hơn `quantityAvailable` (nếu `quantityAvailable` là tổng số lượng, và `quantityAllocated` là số lượng đã cấp phát từ tổng đó).
5.  **Cardinality**: Một `Goal` phải được liên kết với ít nhất một `Metric` để theo dõi tiến độ của nó (thông qua mối quan hệ `MEASURED_BY`).
6.  **Cardinality**: Một `User` có thể `ASSIGNED_TO` nhiều `Task`, và một `Task` có thể được `ASSIGNED_TO` nhiều `User` (nếu cho phép làm việc nhóm trên một task, nếu không thì là 1 user chính).
7.  **Value**: `Metric.value` khi `Metric.dataType` là `Percentage` phải nằm trong khoảng từ 0 đến 100 (bao gồm cả 0 và 100).
8.  **Value**: `Agent.trustScore` phải nằm trong khoảng từ 0.0 đến 1.0.
9.  **Relationship**: Trong mối quan hệ `MANAGES_AGENT`, `managingAgentId` và `managedAgentId` phải tham chiếu đến các `Agent` hợp lệ và khác nhau.
10. **Relationship**: Nếu `TaskA DEPENDS_ON TaskB` với `dependencyType` là `FinishToStart_FS`, thì `TaskA.status` không thể là `InProgress` hoặc `Completed` trừ khi `TaskB.status` là `Completed`.
11. **Data Type**: `Event.timestamp` phải là một chuỗi `datetime` hợp lệ theo định dạng ISO8601.
12. **Inferential**: Nếu `ProjectA` có `HAS_SUBTASK TaskB`, và `TaskB REQUIRES_RESOURCE ResourceC` (với `quantity` là X), thì có thể suy ra `ProjectA` có một yêu cầu tài nguyên gián tiếp đối với `ResourceC` với số lượng X (cần tổng hợp nếu có nhiều task yêu cầu cùng resource).
13. **Inferential**: Nếu một `Agent` liên tục tạo ra các `Tension` có `severity` cao mà sau đó được xác định là `FalsePositive`, `trustScore` của `Agent` đó nên được giảm đi.
14. **Temporal**: `Task.actualEndDate` không được sớm hơn `Task.actualStartDate`.
15. **Temporal**: `WinEvent.timestamp` phải xảy ra trước hoặc bằng `RecognitionEvent.timestamp` liên quan đến nó (nếu `RecognitionEvent` là để ghi nhận `WinEvent` đó).
16. **Domain/Range**: Trong mối quan hệ `IS_PART_OF_PROJECT`, `taskId` phải tham chiếu đến một `Task` và `projectId` phải tham chiếu đến một `Project`.
17. **Custom Business Rule**: Nếu một `Task` có `priority` là `Critical` và `dueDate` của nó sắp đến (ví dụ, trong vòng 24 giờ) nhưng `progressPercentage` < 50%, một `AlertEvent` (hoặc một loại `TensionEvent` đặc biệt) nên được tạo ra.
18. **Custom Business Rule**: Một `User` không thể phê duyệt (`approve`) một `Decision` mà chính họ đã đề xuất (`proposedByUserId`).

**9.5. Cơ chế Thực thi và Giám sát (Enforcement and Monitoring Mechanisms)**
*   **Thực thi tại Thời điểm Nhập liệu (Data Entry Time Enforcement)**: Các API tạo và cập nhật thực thể phải tích hợp logic xác thực để kiểm tra các ràng buộc trước khi lưu dữ liệu. Phản hồi lỗi rõ ràng cho người dùng hoặc hệ thống gọi nếu vi phạm xảy ra.
*   **Xác thực Batch (Batch Validation)**: Các quy trình định kỳ quét toàn bộ hoặc một phần cơ sở dữ liệu/kho tri thức để phát hiện các vi phạm ràng buộc có thể đã phát sinh do thay đổi logic, lỗi hệ thống, hoặc dữ liệu được nhập từ các nguồn không được kiểm soát chặt chẽ.
*   **Agent Giám sát Chuyên dụng (Dedicated Monitoring Agents)**: Các AI Agent có thể được thiết kế để liên tục theo dõi trạng thái của ontology và phát hiện các vi phạm quy tắc phức tạp hoặc các mẫu bất thường mà việc xác thực đơn giản có thể bỏ sót.
*   **Trigger và Stored Procedure (Database Triggers and Stored Procedures)**: Nếu sử dụng cơ sở dữ liệu quan hệ hoặc đồ thị hỗ trợ, trigger có thể được sử dụng để tự động kiểm tra một số ràng buộc khi dữ liệu thay đổi.
*   **Hệ thống Suy luận (Inference Engines)**: Đối với các quy tắc suy luận, một hệ thống suy luận (ví dụ: dựa trên OWL reasoners) có thể được sử dụng để hiện thực hóa các tri thức ngầm ẩn và kiểm tra tính nhất quán.
*   **Ghi Log và Thông báo Vi phạm (Violation Logging and Alerting)**: Tất cả các vi phạm ràng buộc được phát hiện nên được ghi log chi tiết (quy tắc bị vi phạm, thực thể liên quan, thời gian phát hiện). Các vi phạm nghiêm trọng hoặc có tính hệ thống nên kích hoạt thông báo cho quản trị viên hệ thống hoặc các agent chịu trách nhiệm.
*   **Chính sách Xử lý Vi phạm (Violation Handling Policies)**: Cần xác định rõ cách xử lý khi phát hiện vi phạm: từ chối thay đổi, đánh dấu dữ liệu là không hợp lệ, tạo ra một `Tension` để giải quyết, hoặc tự động sửa lỗi (nếu có thể và an toàn).

Việc triển khai một hệ thống quy tắc và ràng buộc mạnh mẽ là một quá trình liên tục, phát triển cùng với sự trưởng thành của ontology và hệ thống TRM-OS.

**PHẦN C: HỆ THỐNG AI AGENTIC**

10. Kiến trúc Tổng thể Hệ thống AI Agent (Overall AI Agent System Architecture)

**10.1. Giới thiệu (Introduction)**

Hệ thống AI Agent là một phần cốt lõi của TRM-OS, được thiết kế để mang lại khả năng tự động hóa thông minh, hỗ trợ ra quyết định, quản lý tri thức chủ động, và tương tác người dùng một cách linh hoạt và hiệu quả. Các agent hoạt động dựa trên ontology đã được định nghĩa, sử dụng tri thức đó để hiểu ngữ cảnh, suy luận và thực hiện các hành động nhằm đạt được mục tiêu cá nhân và mục tiêu chung của hệ thống.

Triết lý thiết kế của hệ thống AI Agent trong TRM-OS tập trung vào các yếu tố sau:
*   **Tính Module (Modularity)**: Mỗi agent hoặc loại agent có trách nhiệm và khả năng chuyên biệt, dễ dàng phát triển, kiểm thử và bảo trì độc lập.
*   **Khả năng Mở rộng (Scalability)**: Kiến trúc cho phép tăng số lượng agent, loại agent và khối lượng công việc mà không làm suy giảm hiệu suất đáng kể.
*   **Khả năng Hợp tác (Collaboration)**: Các agent có khả năng giao tiếp, phối hợp và đàm phán với nhau để giải quyết các vấn đề phức tạp vượt quá khả năng của một agent đơn lẻ.
*   **Tính Thích ứng (Adaptability)**: Các agent có thể học hỏi từ kinh nghiệm và thích ứng với những thay đổi trong môi trường hoặc yêu cầu người dùng.
*   **Hướng Mục tiêu (Goal-Oriented)**: Hành động của agent được định hướng bởi các mục tiêu rõ ràng, có thể là mục tiêu được giao hoặc mục tiêu tự phát sinh.

**10.2. Các Thành phần Chính (Key Components)**

Kiến trúc hệ thống AI Agent của TRM-OS bao gồm các thành phần chính sau:

*   **10.2.1. Lõi Agent (Agent Core)**
    *   **Mô tả**: Cung cấp các chức năng cơ bản và vòng đời cho mỗi agent, bao gồm khởi tạo, thực thi, tạm dừng, và kết thúc. Quản lý trạng thái nội tại, tài nguyên và cấu hình của agent.
    *   **Chức năng**: Quản lý vòng đời, xử lý thông điệp cơ bản, quản lý danh tính agent.

*   **10.2.2. Cơ sở Tri thức Agent (Agent Knowledge Base Access)**
    *   **Mô tả**: Giao diện và logic cho phép agent truy cập, truy vấn, và cập nhật ontology TRM (Mục 1-9) cũng như các nguồn dữ liệu chuyên biệt khác (ví dụ: cơ sở dữ liệu vận hành, kho tài liệu).
    *   **Chức năng**: Truy vấn SPARQL (hoặc ngôn ngữ truy vấn đồ thị khác), thao tác CRUD trên thực thể ontology, tích hợp dữ liệu từ các nguồn khác nhau.

*   **10.2.3. Module Nhận thức (Perception Module)**
    *   **Mô tả**: Cho phép agent thu thập thông tin và nhận biết các sự kiện từ môi trường của nó. Môi trường này bao gồm các `Event` từ System Event Bus, dữ liệu từ các API, thông tin từ người dùng, hoặc thay đổi trong ontology.
    *   **Chức năng**: Lắng nghe sự kiện, gọi API để lấy dữ liệu, phân tích log, xử lý ngôn ngữ tự nhiên từ đầu vào của người dùng.

*   **10.2.4. Module Hành động (Action Module / Actuators)**
    *   **Mô tả**: Cho phép agent thực hiện các hành động để tác động lên môi trường hoặc trạng thái nội tại của hệ thống. Các hành động có thể bao gồm việc gửi lệnh, tạo ra `Event` mới, cập nhật ontology, giao tiếp với người dùng, hoặc gọi các dịch vụ bên ngoài.
    *   **Chức năng**: Thực thi API, tạo và phát `Event`, cập nhật cơ sở dữ liệu/ontology, gửi thông báo.

*   **10.2.5. Module Lập kế hoạch và Ra quyết định (Planning and Decision-Making Module)**
    *   **Mô tả**: Đây là "bộ não" của agent, chứa logic để phân tích thông tin nhận được, đánh giá các lựa chọn, lập kế hoạch hành động và đưa ra quyết định về hành động nào cần thực hiện để đạt được mục tiêu của agent.
    *   **Chức năng**: Suy luận dựa trên quy tắc, lập kế hoạch (ví dụ: HTN, PDDL-like), học máy (ví dụ: học tăng cường cho một số tác vụ), xử lý `Tension`.

*   **10.2.6. Module Giao tiếp Agent (Agent Communication Module - ACM)**
    *   **Mô tả**: Cung cấp các cơ chế và giao thức để các agent tương tác, trao đổi thông tin, phối hợp và đàm phán với nhau. Điều này có thể bao gồm giao tiếp trực tiếp hoặc gián tiếp qua System Event Bus.
    *   **Chức năng**: Gửi/nhận tin nhắn theo một ngôn ngữ giao tiếp agent (ACL - Agent Communication Language) chuẩn hóa (ví dụ: FIPA ACL), quản lý các cuộc hội thoại, khám phá dịch vụ agent.

*   **10.2.7. Bus Sự kiện Hệ thống (System Event Bus)**
    *   **Mô tả**: Một thành phần trung tâm (ví dụ: sử dụng Kafka, RabbitMQ) cho phép các agent và các thành phần khác của TRM-OS giao tiếp một cách bất đồng bộ và découplé thông qua việc phát và đăng ký các `Event` (đã định nghĩa ở Mục 6 và 8).
    *   **Chức năng**: Định tuyến sự kiện, đảm bảo gửi sự kiện, hỗ trợ mô hình publish-subscribe.

*   **10.2.8. Giao diện Người dùng và API (User Interface and APIs)**
    *   **Mô tả**: Cung cấp các điểm tương tác cho người dùng (ví dụ: qua ứng dụng web, mobile, chat) và các hệ thống bên ngoài để gửi yêu cầu, nhận thông tin, và cấu hình các agent.
    *   **Chức năng**: API Gateway, giao diện quản lý agent, công cụ trực quan hóa hoạt động của agent.

**10.3. Sơ đồ Kiến trúc (Architectural Diagram - Conceptual)**

(Phần này sẽ mô tả bằng văn bản một sơ đồ kiến trúc high-level. Một sơ đồ trực quan sẽ được tạo riêng.)

Sơ đồ kiến trúc TRM-OS Agentic System có thể được hình dung như sau:

1.  **Lớp Tương tác (Interaction Layer)**: Bao gồm Giao diện Người dùng (UI), Giao diện Dòng lệnh (CLI), và các API Ngoài (External APIs). Đây là nơi người dùng và các hệ thống khác tương tác với TRM-OS.
2.  **Lớp Dịch vụ và Điều phối (Service & Orchestration Layer)**:
    *   **API Gateway**: Tiếp nhận và định tuyến các yêu cầu từ Lớp Tương tác.
    *   **Agent Manager**: Quản lý vòng đời của các agent, điều phối các tác vụ cấp cao giữa các agent, và giám sát hiệu suất của chúng.
    *   **Workflow Engine**: Quản lý các quy trình nghiệp vụ phức tạp có sự tham gia của nhiều agent hoặc dịch vụ.
3.  **Lớp Agent (Agent Layer)**: Chứa các AI Agent đa dạng, mỗi agent có thể bao gồm:
    *   Agent Core
    *   Perception Module
    *   Action Module
    *   Planning & Decision-Making Module
    *   Agent Knowledge Base Access
    *   Agent Communication Module
4.  **Lớp Tri thức và Dữ liệu (Knowledge & Data Layer)**:
    *   **TRM Ontology (Graph Database)**: Kho tri thức trung tâm.
    *   **Operational Databases**: Lưu trữ dữ liệu vận hành (ví dụ: logs, metrics, user data).
    *   **Document Stores / Vector Databases**: Lưu trữ tài liệu, kiến thức dạng văn bản cho RAG.
5.  **Lớp Giao tiếp và Sự kiện (Communication & Event Layer)**:
    *   **System Event Bus**: Kênh giao tiếp chính cho các sự kiện bất đồng bộ.
    *   **Agent Communication Channels**: Các kênh cho giao tiếp trực tiếp giữa các agent.

Các luồng tương tác chính thường bắt đầu từ Lớp Tương tác, đi qua Lớp Dịch vụ, kích hoạt một hoặc nhiều Agent trong Lớp Agent. Các Agent này sau đó tương tác với Lớp Tri thức và Dữ liệu, và giao tiếp với nhau hoặc phát các sự kiện thông qua Lớp Giao tiếp và Sự kiện. Kết quả hoặc phản hồi sau đó có thể được truyền ngược lại Lớp Tương tác.

**10.4. Luồng Tương tác Chính (Key Interaction Flows)**

*   **10.4.1. Xử lý một Yêu cầu Người dùng (Processing a User Request)**
    1.  Người dùng gửi yêu cầu (ví dụ: "Tạo một dự án mới để phát triển tính năng X") thông qua UI hoặc API.
    2.  API Gateway nhận yêu cầu, xác thực và chuyển đến Agent Manager.
    3.  Agent Manager xác định loại agent phù hợp (ví dụ: `ProjectManagementAgent`) và ủy quyền yêu cầu.
    4.  `ProjectManagementAgent` (PMA) nhận yêu cầu (Perception Module).
    5.  PMA sử dụng Planning & Decision-Making Module để phân tích yêu cầu, kiểm tra tài nguyên, xác định các bước cần thiết (ví dụ: tạo thực thể `Project`, `Task` ban đầu trong ontology, thông báo cho các bên liên quan).
    6.  PMA sử dụng Agent Knowledge Base Access để tương tác với TRM Ontology (tạo `Project`, `Task`).
    7.  PMA sử dụng Action Module để phát các `Event` (ví dụ: `ProjectCreatedEvent`) lên System Event Bus.
    8.  PMA gửi phản hồi về trạng thái xử lý yêu cầu trở lại Agent Manager, và cuối cùng đến người dùng.

*   **10.4.2. Phát hiện và Giải quyết một `Tension` (Detecting and Resolving a Tension)**
    1.  Một `MonitoringAgent` (Perception Module) phát hiện một `MetricThresholdEvent` từ System Event Bus cho thấy một KPI quan trọng đang giảm sút.
    2.  `MonitoringAgent` (Planning & Decision-Making Module) phân tích sự kiện, truy vấn ontology để lấy thêm ngữ cảnh, và xác định đây là một `Tension` cần được giải quyết.
    3.  `MonitoringAgent` (Action Module) tạo một thực thể `Tension` trong ontology, mô tả vấn đề và mức độ nghiêm trọng.
    4.  `MonitoringAgent` phát một `TensionCreatedEvent` lên System Event Bus.
    5.  Một `ResolutionCoordinatorAgent` đăng ký `TensionCreatedEvent` nhận được thông báo.
    6.  `ResolutionCoordinatorAgent` phân tích `Tension`, xác định các agent chuyên môn cần thiết (ví dụ: `ResourceAllocationAgent`, `ProblemDiagnosisAgent`) và yêu cầu sự hợp tác của chúng thông qua Agent Communication Module.
    7.  Các agent hợp tác để chẩn đoán nguyên nhân, đề xuất giải pháp, và thực hiện các hành động khắc phục. Quá trình này có thể tạo ra thêm các `Task`, `Event`, và cập nhật vào ontology.
    8.  Sau khi `Tension` được giải quyết, trạng thái của nó được cập nhật trong ontology, và một `TensionResolvedEvent` được phát ra.

*   **10.4.3. Một Agent Kích hoạt Agent Khác (Agent-to-Agent Triggering)**
    1.  `LearningAgent` sau khi xử lý một tài liệu mới (ví dụ: thông qua `KnowledgeLifecycleEvent` cho biết có tài liệu mới), đã trích xuất được một `KnowledgeSnippet` quan trọng.
    2.  `LearningAgent` (Action Module) tạo `KnowledgeSnippet` trong ontology và phát một `KnowledgeSnippetCreatedEvent` với metadata về snippet đó.
    3.  `TaskRecommendationAgent` đăng ký loại sự kiện này. Khi nhận được `KnowledgeSnippetCreatedEvent` (Perception Module), nó phân tích snippet.
    4.  `TaskRecommendationAgent` (Planning & Decision-Making Module) xác định rằng snippet này có thể liên quan đến một `Task` đang `InProgress` của một `User` cụ thể.
    5.  `TaskRecommendationAgent` (Action Module) tạo một `Recommendation` (có thể là một loại `Event` hoặc một thực thể riêng) và gửi nó đến `NotificationAgent`.
    6.  `NotificationAgent` gửi thông báo cho `User` về `KnowledgeSnippet` liên quan đến `Task` của họ.

*   **10.4.4. Học hỏi từ Dữ liệu Mới (Learning from New Data)**
    1.  Một `DataIngestionAgent` định kỳ quét các nguồn dữ liệu bên ngoài (ví dụ: kho mã nguồn, hệ thống quản lý lỗi) để tìm thông tin mới.
    2.  Khi có dữ liệu mới, `DataIngestionAgent` (Action Module) phát một `ExternalDataReceivedEvent` chứa dữ liệu hoặc tham chiếu đến dữ liệu.
    3.  Một `KnowledgeExtractionAgent` đăng ký sự kiện này.
    4.  `KnowledgeExtractionAgent` (Perception Module) nhận dữ liệu. Sử dụng các kỹ thuật NLP/ML (Planning & Decision-Making Module), nó trích xuất các thực thể, mối quan hệ, hoặc tri thức tiềm ẩn từ dữ liệu.
    5.  `KnowledgeExtractionAgent` (Action Module) cập nhật ontology với tri thức mới (ví dụ: tạo `KnowledgeSnippet`, liên kết các thực thể hiện có, cập nhật thuộc tính).
    6.  Nếu tri thức mới quan trọng hoặc kích hoạt các quy tắc, các `Event` tiếp theo có thể được phát ra để thông báo cho các agent khác.

**10.5. Lựa chọn Công nghệ (Technology Choices - Preliminary Considerations)**

Việc lựa chọn công nghệ cụ thể sẽ phụ thuộc vào các yêu cầu chi tiết, hiệu suất, và nguồn lực sẵn có. Dưới đây là một số cân nhắc sơ bộ:
*   **Ngôn ngữ Lập trình Chính**: Python (do hệ sinh thái AI/ML phong phú, thư viện mạnh mẽ cho NLP, data science, và phát triển web).
*   **Nền tảng/Framework Agent**: Cân nhắc giữa việc sử dụng các framework agent hiện có (ví dụ: SPADE (Python), JADE (Java), Agents.jl (Julia)) hoặc xây dựng một lõi agent tùy chỉnh nhẹ nhàng nếu các framework hiện có quá cồng kềnh hoặc không hoàn toàn phù hợp. Các thư viện như LangChain, AutoGen có thể cung cấp các khối xây dựng hữu ích.
*   **Cơ sở Tri thức (Ontology Storage)**: Graph Database (ví dụ: Neo4j, Amazon Neptune, JanusGraph, RDF4J/GraphDB) để lưu trữ và truy vấn TRM Ontology hiệu quả.
*   **Cơ sở Dữ liệu Vận hành**: PostgreSQL (cho dữ liệu có cấu trúc), MongoDB (cho dữ liệu phi cấu trúc hoặc bán cấu trúc), Elasticsearch (cho tìm kiếm và phân tích log).
*   **Bus Sự kiện Hệ thống (System Event Bus)**: Apache Kafka (cho khả năng mở rộng cao, thông lượng lớn, và độ bền), RabbitMQ (linh hoạt, dễ sử dụng hơn cho một số trường hợp).
*   **AI/ML Frameworks**: TensorFlow, PyTorch (cho deep learning), scikit-learn (cho machine learning truyền thống), spaCy, NLTK (cho NLP).
*   **Workflow Engine**: Apache Airflow, Prefect, Camunda (để điều phối các quy trình phức tạp, đặc biệt là các quy trình liên quan đến xử lý dữ liệu và học máy).
*   **Containerization & Orchestration**: Docker, Kubernetes (để triển khai và quản lý các agent và dịch vụ một cách nhất quán và có khả năng mở rộng).

**10.6. Các Nguyên tắc Thiết kế (Design Principles)**

Các nguyên tắc sau sẽ hướng dẫn việc thiết kế và phát triển hệ thống AI Agent của TRM-OS:
*   **Tính Module (Modularity)**: Các agent và các module bên trong agent được thiết kế để có tính gắn kết cao (high cohesion) và khớp nối lỏng (low coupling). Mỗi agent nên có một tập hợp trách nhiệm rõ ràng.
*   **Hướng Dịch vụ (Service-Oriented)**: Các khả năng của agent có thể được tiếp xúc dưới dạng dịch vụ mà các agent khác hoặc các thành phần hệ thống có thể sử dụng.
*   **Khả năng Mở rộng (Scalability)**: Thiết kế để có thể dễ dàng thêm agent mới, tăng số lượng instance của một loại agent, và xử lý khối lượng dữ liệu/sự kiện ngày càng tăng.
*   **Khả năng Cấu hình (Configurability)**: Hành vi của agent, các quy tắc ra quyết định, và các tham số hoạt động nên có thể cấu hình được mà không cần thay đổi mã nguồn (ví dụ: qua file cấu hình, biến môi trường, hoặc cập nhật trong ontology).
*   **Khả năng Quan sát (Observability)**: Hệ thống phải cung cấp các cơ chế logging, monitoring, và tracing chi tiết để theo dõi hoạt động của agent, chẩn đoán sự cố, và phân tích hiệu suất.
*   **An ninh và Kiểm soát Truy cập (Security and Access Control)**: Các agent phải hoạt động trong một môi trường an toàn. Quyền truy cập vào dữ liệu và khả năng thực hiện hành động phải được kiểm soát chặt chẽ dựa trên danh tính và vai trò của agent.
*   **Khả năng Phục hồi (Resilience)**: Hệ thống agent nên có khả năng chịu lỗi. Nếu một agent gặp sự cố, nó không nên làm sập toàn bộ hệ thống, và nên có cơ chế để phục hồi hoặc khởi động lại agent đó.
*   **Tính Minh bạch và Giải thích được (Transparency and Explainability - XAI)**: Khi có thể, các quyết định của agent nên có thể giải thích được, đặc biệt là trong các tình huống quan trọng, để người dùng có thể hiểu tại sao agent lại hành động như vậy.
*   **Ưu tiên Ontology (Ontology-Driven)**: Ontology là trung tâm của tri thức và hiểu biết của agent. Hành vi và suy luận của agent nên được định hướng mạnh mẽ bởi cấu trúc và ngữ nghĩa của ontology.
    10.1. Artificial Genesis Engine (AGE) – Vai trò và Năng lực Cốt lõi

**10.1.1. Giới thiệu về AGE (Introduction to AGE)**
*   **Định nghĩa**: Artificial Genesis Engine (AGE) là một thành phần hoặc meta-agent chuyên biệt trong TRM-OS, có trách nhiệm chính trong việc tự động hóa quá trình tạo ra (genesis), cấu hình ban đầu, và triển khai các AI agent chuyên biệt khác. AGE hoạt động như một "nhà máy sản xuất agent" (agent factory) hoặc một "vườn ươm agent" (agent nursery).
*   **Tầm nhìn**: Mục tiêu của AGE là cho phép hệ thống TRM-OS có khả năng tự mở rộng và thích ứng bằng cách tự động sinh ra các agent mới khi cần thiết. Việc này có thể dựa trên các mẫu (templates) được định sẵn, các mục tiêu (goals) mới phát sinh, các `Tension` cần giải quyết, hoặc các yêu cầu cụ thể từ người dùng quản trị hoặc từ các agent cấp cao khác.
*   **Mối quan hệ với Ontology**: AGE phụ thuộc sâu sắc vào TRM Ontology. Ontology cung cấp cho AGE:
    *   Các định nghĩa về các loại agent có thể được tạo (`AgentTypeDefinition`).
    *   Các mẫu agent (agent templates) bao gồm các module, kỹ năng, cấu hình mặc định, và các phụ thuộc cần thiết.
    *   Ngữ cảnh và các ràng buộc để xác định loại agent nào phù hợp cho một yêu cầu cụ thể.
    *   Thông tin để cấu hình agent mới (ví dụ: `Goal` cần theo đuổi, `Resource` cần quản lý).

**10.1.2. Vai trò Chính của AGE (Key Roles of AGE)**
*   **Sinh Agent (Agent Generation)**: Tạo ra các instance mới của các loại agent chuyên biệt (ví dụ: `DataMonitoringAgent`, `TaskExecutionAgent`, `ResourceSchedulingAgent`) dựa trên các yêu cầu đầu vào và các mẫu agent đã được định nghĩa trong ontology hoặc kho lưu trữ mẫu.
*   **Cấu hình Agent (Agent Configuration)**: Thiết lập các tham số hoạt động ban đầu cho agent mới được tạo. Điều này bao gồm việc gán `agentId` duy nhất, thiết lập các mục tiêu ban đầu (`initialGoals`), liên kết với các `Resource` hoặc `KnowledgeSnippet` cần thiết, định nghĩa các quyền truy cập (permissions), và các chính sách hoạt động cơ bản.
*   **Triển khai Agent (Agent Deployment)**: Đưa agent mới vào môi trường hoạt động của TRM-OS. Quá trình này bao gồm việc đăng ký agent với `AgentManager` (xem Mục 10.2), kết nối agent với `SystemEventBus`, và khởi tạo các kết nối cần thiết khác.
*   **Quản lý Mẫu Agent (Agent Template Management)**: Cung cấp giao diện (có thể là lập trình hoặc thông qua công cụ quản trị) để định nghĩa, cập nhật, và quản lý các mẫu agent. Mỗi mẫu sẽ chỉ định kiến trúc cơ bản, các module kỹ năng, các phụ thuộc, và các tham số cấu hình mặc định.
*   **(Nâng cao) Tối ưu hóa và Thích ứng Agent (Agent Optimization and Adaptation Support)**: Trong các phiên bản tương lai, AGE có thể hỗ trợ việc tạo ra các biến thể agent hoặc các thế hệ agent mới dựa trên phân tích hiệu suất của các agent hiện có, nhằm mục đích tối ưu hóa hoặc thích ứng với các điều kiện thay đổi. Điều này có thể liên quan đến việc điều chỉnh cấu hình hoặc thậm chí là thay đổi thành phần module của agent.

**10.1.3. Năng lực Cốt lõi của AGE (Core Capabilities of AGE)**
*   **Sử dụng Mẫu Agent (Agent Templating)**: Khả năng làm việc với một thư viện các mẫu agent. Mỗi mẫu định nghĩa "bản thiết kế" cho một loại agent, bao gồm:
    *   Các module phần mềm (ví dụ: `PerceptionModule`, `ActionModule` cụ thể).
    *   Các kỹ năng (skills) hoặc khả năng (capabilities) được định nghĩa trước.
    *   Các tham số cấu hình mặc định và các biến có thể tùy chỉnh.
    *   Các phụ thuộc tài nguyên hoặc tri thức.
*   **Suy luận dựa trên Ontology (Ontology-based Reasoning for Agent Creation)**: AGE sử dụng TRM Ontology để:
    *   Hiểu yêu cầu tạo agent (ví dụ: phân tích một `Tension` hoặc một yêu cầu từ `User` để xác định loại agent nào là phù hợp nhất).
    *   Xác định các cấu hình cần thiết cho agent dựa trên ngữ cảnh (ví dụ: nếu tạo agent để quản lý một `Project` mới, AGE sẽ lấy `projectId` và các thông tin liên quan từ ontology để cấu hình cho agent).
    *   Kiểm tra các điều kiện tiên quyết và ràng buộc trước khi tạo agent.
*   **Tích hợp với Agent Manager và System Event Bus**: AGE phải giao tiếp hiệu quả với `AgentManager` để đăng ký các agent mới và có thể nhận các yêu cầu quản lý vòng đời cơ bản. Nó cũng đảm bảo agent mới được kết nối đúng cách với `SystemEventBus` để nhận và gửi sự kiện.
*   **Giao diện Lập trình (Programmatic Interface - API)**: Cung cấp một API rõ ràng cho các thành phần khác của TRM-OS (ví dụ: `ResolutionCoordinatorAgent`, các quy trình quản trị hệ thống) hoặc người dùng có thẩm quyền để yêu cầu tạo, cấu hình, và triển khai agent một cách tự động.
*   **Khả năng Mở rộng (Extensibility)**: Kiến trúc của AGE nên cho phép dễ dàng thêm các loại mẫu agent mới hoặc cập nhật các mẫu hiện có khi hệ thống TRM-OS phát triển.

**10.1.4. Tương tác của AGE với các Thành phần Khác (AGE's Interaction with Other Components)**
*   **`AgentManager` (Mục 10.2.x - sẽ được định nghĩa sau)**: AGE tạo agent và đăng ký chúng với `AgentManager`. `AgentManager` chịu trách nhiệm giám sát hoạt động hàng ngày, điều phối, và quản lý vòng đời chi tiết hơn (ví dụ: tạm dừng, tiếp tục, thu hồi dựa trên các chính sách vận hành).
*   **TRM Ontology**: AGE liên tục truy vấn và sử dụng ontology để lấy thông tin về các định nghĩa loại agent, mẫu agent, các thực thể liên quan (ví dụ: `Project`, `Goal`, `Resource` mà agent mới cần tương tác), và các ràng buộc hệ thống.
*   **Người Quản trị Hệ thống / Developer**: Cung cấp và duy trì các mẫu agent, các quy tắc cấu hình, và các chính sách cho AGE. Họ cũng có thể tương tác trực tiếp với AGE để yêu cầu tạo agent thủ công khi cần.
*   **Các Agent Yêu cầu (Requesting Agents)**: Một số agent cấp cao hoặc agent điều phối (ví dụ: `ResolutionCoordinatorAgent` khi xử lý một `Tension` phức tạp) có thể gửi yêu cầu đến AGE để tạo ra các agent chuyên biệt, tạm thời hoặc lâu dài, để thực hiện các tác vụ cụ thể.
*   **Kho lưu trữ Mẫu Agent (Agent Template Repository)**: Một kho lưu trữ (có thể là một phần của ontology hoặc một hệ thống quản lý cấu hình riêng) chứa các định nghĩa chi tiết của các mẫu agent.

**10.1.5. Ví dụ Hoạt động của AGE (Example Scenario of AGE in Action)**

1.  **Kích hoạt**: Một `User` thông qua giao diện quản trị TRM-OS yêu cầu tạo một hệ thống giám sát mới cho một dòng sản phẩm (`ProductLine`) mới vừa được thêm vào ontology. Yêu cầu này bao gồm việc theo dõi các chỉ số hiệu suất chính (KPIs) và phát hiện các `AnomalyEvent` liên quan đến `ProductLine` đó.
2.  **Phân tích Yêu cầu**: Yêu cầu được chuyển đến AGE (có thể thông qua `AgentManager` hoặc một service điều phối). AGE phân tích yêu cầu, truy vấn ontology để hiểu về `ProductLine` cụ thể, các `MetricDefinition` liên quan đến nó, và các loại `AnomalyEvent` cần theo dõi.
3.  **Lựa chọn Mẫu**: Dựa trên phân tích, AGE xác định rằng cần một tập hợp các agent, ví dụ:
    *   Một `DataIngestionAgent` để thu thập dữ liệu từ các nguồn liên quan đến `ProductLine`.
    *   Nhiều `MetricCalculationAgent`, mỗi agent cho một KPI cụ thể.
    *   Một `AnomalyDetectionAgent` chuyên biệt cho `ProductLine` này.
    AGE chọn các mẫu agent tương ứng từ kho lưu trữ mẫu.
4.  **Cấu hình Agent**: AGE tiến hành cấu hình từng instance agent:
    *   Cho `DataIngestionAgent`: chỉ định các nguồn dữ liệu, tần suất thu thập.
    *   Cho `MetricCalculationAgent`: chỉ định `MetricDefinition` cần tính toán, nguồn dữ liệu đầu vào (từ `DataIngestionAgent`).
    *   Cho `AnomalyDetectionAgent`: chỉ định các luồng metric đầu vào, các mô hình phát hiện bất thường, và ngưỡng cảnh báo.
    Tất cả các agent được gán `agentId` duy nhất và các quyền truy cập cần thiết.
5.  **Triển khai và Đăng ký**: AGE triển khai các agent mới này vào môi trường hoạt động. Mỗi agent được đăng ký với `AgentManager` và được kết nối với `SystemEventBus`.
6.  **Kích hoạt Hoạt động**: Các agent mới bắt đầu thực thi các nhiệm vụ được giao: thu thập dữ liệu, tính toán metric, và theo dõi các dấu hiệu bất thường.
7.  **Phản hồi**: AGE thông báo lại cho `User` (thông qua `AgentManager` hoặc service điều phối) rằng hệ thống giám sát cho `ProductLine` đã được thiết lập và đang hoạt động.
    10.2. Các AI Agent Chuyên biệt (Specialized AI Agents)

    *   **10.2.1. `DataSensingAgent` (Agent Cảm biến Dữ liệu)**
        * **10.2.1.1. Mục tiêu (Objective)**
            *   Chủ động và tự động thu thập dữ liệu thô hoặc bán cấu trúc từ các nguồn (`DataSource`) đa dạng đã được xác định trong TRM Ontology.
            *   Thực hiện các bước tiền xử lý cơ bản (basic pre-processing) như kiểm tra định dạng, xác thực sơ bộ, và chuyển đổi cấu trúc đơn giản nếu cần.
            *   Đưa dữ liệu đã thu thập và tiền xử lý vào các giai đoạn tiếp theo của data pipeline (ví dụ: lưu trữ tạm thời, gửi đến `DataProcessingAgent`, hoặc phát sinh `RawDataAvailableEvent`).
            *   Đảm bảo tính kịp thời và độ tin cậy của việc thu thập dữ liệu theo lịch trình hoặc theo sự kiện kích hoạt.

        * **10.2.1.2. Nguồn Dữ liệu Đầu vào (Input Data Sources / Configuration)**
            * **Cấu hình Agent**: Thông tin cấu hình được cung cấp khi agent được tạo hoặc cập nhật, bao gồm:
                * ` dataSourceId`: ID của `DataSource` trong ontology mà agent này chịu trách nhiệm thu thập.
                *   Lịch trình thu thập (ví dụ: cron expression, tần suất).
                *   Phương thức truy cập (API endpoint, DB connection string, file path, credentials được quản lý an toàn).
                *   Các tham số truy vấn cụ thể (ví dụ: query parameters cho API, SQL query cho DB).
                *   Thông tin về định dạng dữ liệu mong đợi.
            * **TRM Ontology**: Agent có thể truy vấn ontology để lấy thêm chi tiết về `DataSource` (ví dụ: metadata, schema kỳ vọng, các `Resource` liên quan).

        * **10.2.1.3. Các Hành động Chính (Key Actions)**
            * **Kết nối Nguồn (Connect to Source)**: Thiết lập và duy trì kết nối đến `DataSource` được chỉ định.
            * **Truy xuất Dữ liệu (Retrieve Data)**: Thực hiện các lệnh gọi API, truy vấn cơ sở dữ liệu, đọc file, hoặc sử dụng các cơ chế khác để lấy dữ liệu.
            * **Tiền xử lý Cơ bản (Basic Pre-processing)**:
                *   Kiểm tra dữ liệu nhận được có trống không.
                *   Xác thực định dạng cơ bản (ví dụ: JSON, XML, CSV có hợp lệ không).
                *   Chuyển đổi encoding nếu cần.
                *   Trích xuất các trường dữ liệu quan trọng theo cấu hình.
            * **Đóng gói Dữ liệu (Package Data)**: Đóng gói dữ liệu thu thập được (ví dụ: thành một `DataChunk` hoặc một `RawDataItem`) cùng với metadata (ví dụ: `timestamp`, `sourceId`, `dataType`).
            * **Gửi Dữ liệu / Phát Sự kiện (Dispatch Data / Emit Event)**: Gửi `DataChunk` đến một hàng đợi (message queue), một data store tạm thời, hoặc trực tiếp đến một agent xử lý khác. Phát ra `RawDataAvailableEvent` lên `SystemEventBus` để thông báo cho các agent khác quan tâm.
            * **Ghi Log và Giám sát (Logging and Monitoring)**: Ghi lại các hoạt động thu thập, các lỗi phát sinh, và các chỉ số hiệu suất (ví dụ: số lượng bản ghi thu thập được, thời gian thu thập).
            * **Xử lý Lỗi (Error Handling)**: Xử lý các lỗi kết nối, lỗi truy xuất dữ liệu, lỗi định dạng, và thông báo cho `AgentManager` hoặc quản trị viên nếu cần.

        * **10.2.1.4. Dữ liệu Đầu ra / Sự kiện Tạo ra (Output Data / Generated Events)**
            * **Dữ liệu**: Các `DataChunk` hoặc `RawDataItem` chứa dữ liệu đã thu thập và tiền xử lý.
            * **Sự kiện (Events)**:
                * ` RawDataAvailableEvent`: Thông báo rằng dữ liệu mới đã được thu thập và sẵn sàng cho xử lý tiếp theo. Payload chứa metadata về dữ liệu (ví dụ: `dataChunkId`, `dataSourceId`, `timestamp`, kích thước, vị trí lưu trữ tạm thời nếu có).
                * ` DataSensingSuccessEvent`: Thông báo thu thập dữ liệu thành công.
                * ` DataSensingFailureEvent`: Thông báo thu thập dữ liệu thất bại, kèm theo thông tin lỗi.
                * ` DataSourceUnreachableEvent`: Thông báo không thể kết nối đến nguồn dữ liệu.

        * **10.2.1.5. Tương tác với các Thành phần Khác (Interaction with Other Components)**
            * **`DataSource` (Ontology Entity)**: Đọc thông tin cấu hình và metadata từ thực thể `DataSource` trong ontology.
            * **`AgentManager`**: Nhận cấu hình, báo cáo trạng thái, log, và nhận lệnh (ví dụ: bắt đầu/dừng thu thập).
            * **`SystemEventBus`**: Phát các sự kiện (ví dụ: `RawDataAvailableEvent`) và có thể lắng nghe các sự kiện kích hoạt (ví dụ: `TriggerDataSensingEvent`).
            * **`DataProcessingAgent` (hoặc các agent xử lý dữ liệu khác)**: Là người tiêu thụ tiềm năng của `RawDataAvailableEvent` hoặc dữ liệu mà `DataSensingAgent` gửi trực tiếp/qua message queue.
            * **Data Storage (Tạm thời/Pipeline)**: Lưu trữ dữ liệu thô đã thu thập trước khi được xử lý sâu hơn.
            * **Secure Credential Store**: Truy cập an toàn các thông tin xác thực cần thiết để kết nối với `DataSource`.

        * **10.2.1.6. Ví dụ Cụ thể (Specific Example)**
            * **Bối cảnh**: TRM-OS cần theo dõi các đề cập (mentions) về công ty "TRM Inc." trên Twitter.
            * **Cấu hình `DataSensingAgent`**: Một instance của `DataSensingAgent` được cấu hình để:
                *   Kết nối với Twitter API (sử dụng `DataSource` có `type = 'TwitterAPI'`).
                *   Sử dụng search query: "TRM Inc." OR "@TRMIncOfficial".
                *   Tần suất thu thập: mỗi 5 phút.
                *   Credentials: lấy từ Secure Credential Store.
            * **Hoạt động**: 
                1.  Agent kết nối Twitter API.
                2.  Thực hiện search query.
                3.  Nhận về một tập các tweets (dưới dạng JSON).
                4.  Tiền xử lý: Trích xuất các trường quan trọng như `tweet_id`, `user_id`, `text`, `created_at`, `user_followers_count`.
                5.  Đóng gói thành một `DataChunk` (ví dụ, một danh sách các đối tượng JSON đã được chuẩn hóa).
                6.  Phát `RawDataAvailableEvent` lên `SystemEventBus` với thông tin về `DataChunk` này (ví dụ: ID của chunk, nguồn là Twitter, thời gian thu thập).
                7.  Một `SocialMediaProcessingAgent` (một loại `DataProcessingAgent`) lắng nghe sự kiện này, nhận `DataChunk` và bắt đầu phân tích sentiment, trích xuất thực thể, v.v.
            * **Nhiệm vụ chính**:
                *   Kết nối với các API, đọc file, truy vấn database theo lịch trình hoặc trigger.
                *   Tiền xử lý dữ liệu thô (làm sạch, chuẩn hóa định dạng cơ bản).
                *   Gửi dữ liệu đã xử lý đến các agent khác (đặc biệt là `KnowledgeExtractionAgent`) hoặc lưu trữ tạm thởi.
                *   Tạo `SystemEvent` trong ontology để ghi nhận hoạt động thu thập dữ liệu (e.g., "DataIngestedFromGoogleSheet").
            * **Tương tác Ontology**: Tạo `RawDataNode` (nếu cần), tạo `SystemEvent`.
            * **Công nghệ tiềm năng**: Python scripts, Apache Airflow (hoặc tương tự cho scheduling), thư viện kết nối API (requests, google-api-python-client), thư viện xử lý dữ liệu (Pandas).

        * **10.2.2. `DataProcessingAgent` (Agent Xử lý Dữ liệu)**
            * **10.2.2.1. Mục tiêu (Objective)**
                *   Tiếp nhận dữ liệu thô hoặc bán cấu trúc (ví dụ: từ `DataSensingAgent` qua `RawDataAvailableEvent`).
                *   Thực hiện các tác vụ xử lý, phân tích, và biến đổi dữ liệu phức tạp để trích xuất thông tin có giá trị và tri thức.
                *   Chuẩn hóa dữ liệu theo các định dạng và cấu trúc được xác định trong TRM Ontology.
                *   Làm giàu dữ liệu bằng cách liên kết nó với các thực thể hiện có trong ontology hoặc bằng cách suy luận ra thông tin mới.
                *   Tạo ra các `KnowledgeSnippet` mới hoặc cập nhật các `KnowledgeSnippet` hiện có, đồng thời tạo các mối quan hệ (`Relationship`) liên quan trong ontology.

            * **10.2.2.2. Dữ liệu Đầu vào (Input Data)**
                * **`RawDataAvailableEvent`**: Lắng nghe sự kiện này để biết có dữ liệu mới từ `DataSensingAgent`.
                * **`DataChunk` / `RawDataItem`**: Dữ liệu thực tế được truyền tải, có thể lấy từ vị trí được chỉ định trong `RawDataAvailableEvent` (ví dụ: message queue, data store tạm thởi).
                * **TRM Ontology**: Truy vấn ontology để lấy thông tin về schema, các quy tắc biến đổi, các thực thể cần liên kết, và ngữ cảnh xử lý.
                * **Cấu hình Agent**: Các tham số cấu hình cụ thể cho loại xử lý dữ liệu mà agent này đảm nhận (ví dụ: mô hình NLP nào cần sử dụng, các quy tắc trích xuất thực thể, các ánh xạ trường).

            * **10.2.2.3. Các Hành động Chính (Key Actions)**
                * **Phân tích cú pháp (Parsing)**: Phân tích dữ liệu đầu vào theo định dạng của nó (JSON, XML, text, HTML, v.v.).
                * **Trích xuất Thông tin (Information Extraction)**:
                    *   Trích xuất thực thể được đặt tên (Named Entity Recognition - NER) (ví dụ: `Person`, `Organization`, `Location`, `Product`, `ProjectID`).
                    *   Trích xuất mối quan hệ (Relation Extraction) giữa các thực thể.
                    *   Trích xuất thuộc tính (Attribute Extraction).
                * **Phân loại (Classification)**: Gán nhãn hoặc danh mục cho dữ liệu (ví dụ: phân loại văn bản theo chủ đề, phân loại email là spam/không spam).
                * **Phân tích Sentiment (Sentiment Analysis)**: Xác định sắc thái tình cảm (tích cực, tiêu cực, trung tính) của văn bản.
                * **Chuẩn hóa Dữ liệu (Data Standardization)**: Đưa dữ liệu về một định dạng thống nhất (ví dụ: chuẩn hóa ngày tháng, đơn vị tiền tệ, mã quốc gia).
                * **Làm giàu Dữ liệu (Data Enrichment)**:
                    *   Liên kết các thực thể được trích xuất với các `OntologyEntity` hiện có trong TRM Ontology (Entity Linking/Resolution).
                    *   Bổ sung thông tin từ các nguồn bên ngoài hoặc từ ontology (ví dụ: thêm thông tin nhân khẩu học cho một `User` dựa trên `userId`).
                * **Tạo/Cập nhật `KnowledgeSnippet`**: Tạo các bản ghi `KnowledgeSnippet` mới từ thông tin đã xử lý, hoặc cập nhật các `KnowledgeSnippet` hiện có. Điều này bao gồm việc điền các trường như `content`, `source`, `type`, `extractedEntities`, `confidenceScore`.
                * **Tạo Mối quan hệ (Relationship Generation)**: Tạo các `Relationship` trong ontology để kết nối `KnowledgeSnippet` mới với các thực thể khác (ví dụ: `KnowledgeSnippet` CREATED_FROM `RawDataItem`, `KnowledgeSnippet` DESCRIBES `Project`).
                * **Quản lý Chất lượng Dữ liệu (Data Quality Management)**: Thực hiện các kiểm tra chất lượng, xác định và gắn cờ các vấn đề về dữ liệu (ví dụ: thiếu thông tin, không nhất quán).
                * **Ghi Log và Phát Sự kiện (Logging and Event Emission)**: Ghi log quá trình xử lý và phát các sự kiện như `KnowledgeSnippetCreatedEvent`, `DataProcessingCompletedEvent`, `DataProcessingFailedEvent`.

            * **10.2.2.4. Dữ liệu Đầu ra / Sự kiện Tạo ra (Output Data / Generated Events)**
                * **Dữ liệu**: Các `KnowledgeSnippet` được lưu trữ trong cơ sở dữ liệu ontology (ví dụ: GraphDB, Supabase).
                * **Sự kiện (Events)**:
                    * ` KnowledgeSnippetCreatedEvent`: Thông báo một `KnowledgeSnippet` mới đã được tạo. Payload chứa `snippetId` và các metadata liên quan.
                    * ` KnowledgeSnippetUpdatedEvent`: Thông báo một `KnowledgeSnippet` đã được cập nhật.
                    * ` EntityLinkedEvent`: Thông báo một thực thể trong dữ liệu đã được liên kết thành công với một `OntologyEntity`.
                    * ` RelationshipCreatedEvent`: Thông báo một `Relationship` mới đã được tạo trong ontology.
                    * ` DataProcessingCompletedEvent`: Thông báo một lô dữ liệu đã được xử lý xong.
                    * ` DataProcessingFailedEvent`: Thông báo lỗi trong quá trình xử lý dữ liệu.
                    * ` NewTensionCandidateIdentifiedEvent`: (Nâng cao) Nếu agent phát hiện ra một sự không nhất quán hoặc một vấn đề tiềm ẩn có thể là một `Tension`.

            * **10.2.2.5. Tương tác với các Thành phần Khác (Interaction with Other Components)**
                * **`DataSensingAgent`**: Nhận dữ liệu thô hoặc thông báo về dữ liệu thô.
                * **TRM Ontology / Knowledge Base**: Đọc schema, quy tắc; ghi `KnowledgeSnippet` và `Relationship` mới; truy vấn các thực thể hiện có để liên kết.
                * **`AgentManager`**: Báo cáo trạng thái, log, nhận cấu hình và lệnh.
                * **`SystemEventBus`**: Lắng nghe `RawDataAvailableEvent` và phát các sự kiện như `KnowledgeSnippetCreatedEvent`.
                * **NLP Services / ML Models**: Có thể gọi các dịch vụ bên ngoài hoặc các mô hình ML được triển khai nội bộ để thực hiện NER, phân tích sentiment, phân loại, v.v.
                * **`KnowledgeValidationAgent` (sẽ định nghĩa sau)**: `KnowledgeSnippet` mới tạo ra có thể được xem xét bởi agent này.
                * **`WorkflowEngine` (nếu có)**: Có thể là một phần của một quy trình công việc lớn hơn được điều phối bởi một workflow engine.

            * **10.2.2.6. Ví dụ Cụ thể (Specific Example)**
                * **Bối cảnh**: Tiếp nối ví dụ của `DataSensingAgent`, `DataProcessingAgent` nhận được `RawDataAvailableEvent` thông báo về các tweets liên quan đến "TRM Inc.".
                * **Cấu hình `DataProcessingAgent`**: Một instance của `DataProcessingAgent` (ví dụ: `SocialMediaProcessingAgent`) được cấu hình để:
                    *   Lắng nghe `RawDataAvailableEvent` từ `DataSource` type 'TwitterAPI'.
                    *   Sử dụng một mô hình NLP để phân tích sentiment và trích xuất thực thể (ví dụ: tên sản phẩm, tên người, các vấn đề được đề cập).
                    *   Liên kết "TRM Inc." với `Organization` entity tương ứng trong ontology.
                * **Hoạt động**:
                    1.  Agent nhận `RawDataAvailableEvent` và lấy `DataChunk` chứa các tweets.
                    2.  Đối với mỗi tweet:
                        a.  Thực hiện phân tích sentiment (ví dụ: tweet "TRM Inc. new product is amazing!" -> Positive).
                        b.  Trích xuất thực thể (ví dụ: "new product" có thể được liên kết với một `ProductConcept` hoặc `Feature` trong ontology nếu có đủ thông tin).
                        c.  Tạo một `KnowledgeSnippet` mới:
                            * ` type`: 'SocialMediaMention'
                            * ` content`: Nội dung tweet.
                            * ` source`: Twitter, `tweet_id`.
                            * ` properties`: `{ "sentiment": "Positive", "author_followers": 1200, ... }`
                            * ` extractedEntities`: Tham chiếu đến các `OntologyEntity` đã được liên kết (ví dụ: `TRM_Inc_Org_ID`).
                        d.  Tạo mối quan hệ: `KnowledgeSnippet` MENTIONS `TRM_Inc_Org_ID`.
                    3.  Phát `KnowledgeSnippetCreatedEvent` cho mỗi snippet được tạo.
                    4.  Nếu một tweet thể hiện một vấn đề nghiêm trọng, agent có thể phát `NewTensionCandidateIdentifiedEvent`.

        * **10.2.3. `KnowledgeExtractionAgent` (Agent Trích xuất Tri thức)**
            * **10.2.3.1. Mục tiêu (Objective)**
                *   Tiếp nhận các `KnowledgeSnippet` đã được xử lý cơ bản (ví dụ: từ `DataProcessingAgent` qua `KnowledgeSnippetCreatedEvent`) hoặc dữ liệu văn bản/tài liệu trực tiếp.
                *   Sử dụng các mô hình ngôn ngữ lớn (LLMs) và các kỹ thuật Xử lý Ngôn ngữ Tự nhiên (NLP) tiên tiến (bao gồm NER, Relation Extraction, Question Answering, Summarization) để thực hiện trích xuất tri thức sâu.
                *   Xác định, phân loại và chuẩn hóa các thực thể (entities), thuộc tính (attributes), và mối quan hệ (relationships) tiềm năng dựa trên định nghĩa trong TRM Ontology.
                *   Tạo ra các `OntologyEntityCandidate` và `RelationshipCandidate` với độ tin cậy (confidence scores) và bằng chứng (evidence) từ nguồn dữ liệu.
                *   Hỗ trợ việc tạo embedding cho các `KnowledgeSnippet` hoặc các phần của tri thức để phục vụ tìm kiếm ngữ nghĩa và các tác vụ khác.
                *   Giảm thiểu sự mơ hồ và giải quyết xung đột thông tin tiềm ẩn trong quá trình trích xuất.

            * **10.2.3.2. Dữ liệu Đầu vào (Input Data)**
                * **`KnowledgeSnippetCreatedEvent` / `KnowledgeSnippetUpdatedEvent`**: Lắng nghe các sự kiện này để xử lý các snippet mới hoặc đã được cập nhật.
                * **`KnowledgeSnippet`**: Đối tượng dữ liệu chứa văn bản đã được tiền xử lý, metadata nguồn, và có thể là các thực thể đã được nhận diện sơ bộ.
                * **Dữ liệu văn bản/tài liệu trực tiếp**: Có thể nhận các file văn bản (txt, pdf, docx), nội dung từ web, hoặc các bản ghi chú.
                * **TRM Ontology**: Truy cập sâu vào schema của ontology, bao gồm định nghĩa các `EntityType`, `PropertyType`, `RelationshipType`, các ràng buộc (constraints), và các tri thức hiện có để định hướng quá trình trích xuất và liên kết.
                * **Cấu hình Agent**:
                    *   Loại mô hình LLM/NLP sẽ sử dụng (ví dụ: GPT-4, Llama, BERT-based models).
                    *   Các prompts hoặc templates cho LLM để hướng dẫn trích xuất.
                    *   Ngưỡng độ tin cậy (confidence thresholds) để chấp nhận các thực thể/mối quan hệ được trích xuất.
                    *   Cấu hình cho việc tạo embedding (ví dụ: mô hình embedding, trường dữ liệu cần embedding).

            * **10.2.3.3. Các Hành động Chính (Key Actions)**
                * **Phân tích Nội dung Nâng cao (Advanced Content Analysis)**:
                    *   Áp dụng các kỹ thuật NLP như phân tích ngữ nghĩa, phân tích diễn ngôn để hiểu sâu hơn về nội dung.
                    *   Thực hiện NER chi tiết để xác định các thực thể phức tạp hoặc chuyên biệt theo domain của TRM.
                    *   Thực hiện Relation Extraction để xác định các mối quan hệ ngữ nghĩa giữa các thực thể, bao gồm cả các mối quan hệ ngầm định.
                * **Chuẩn hóa và Ánh xạ Ontology (Ontology Mapping and Normalization)**:
                    *   Ánh xạ các thực thể và mối quan hệ được trích xuất vào các `EntityType` và `RelationshipType` tương ứng trong TRM Ontology.
                    *   Chuẩn hóa giá trị thuộc tính (ví dụ: "ngày mai" thành YYYY-MM-DD).
                    *   Giải quyết thực thể (Entity Resolution): Xác định xem một thực thể được trích xuất có tương ứng với một `OntologyEntity` đã tồn tại trong knowledge base hay không.
                * **Tạo Ứng viên Tri thức (Knowledge Candidate Generation)**:
                    *   Tạo `OntologyEntityCandidate` cho các thực thể mới được xác định, bao gồm các thuộc tính được trích xuất, nguồn, và điểm tin cậy.
                    *   Tạo `RelationshipCandidate` giữa các `OntologyEntityCandidate` hoặc giữa `OntologyEntityCandidate` và `OntologyEntity` hiện có.
                * **Tính toán Độ tin cậy (Confidence Scoring)**: Gán điểm tin cậy cho mỗi thông tin được trích xuất (thực thể, thuộc tính, mối quan hệ) dựa trên output của mô hình và các quy tắc heuristic.
                * **Trích xuất Bằng chứng (Evidence Extraction)**: Lưu lại đoạn văn bản hoặc ngữ cảnh nguồn gốc đã dẫn đến việc trích xuất một thông tin cụ thể.
                * **Tạo Embedding (Embedding Generation)**: Nếu được cấu hình, tạo vector embedding cho `KnowledgeSnippet` hoặc các phần tri thức quan trọng và chuẩn bị để lưu trữ (ví dụ: trong Supabase Vector).
                * **Ghi Log và Phát Sự kiện (Logging and Event Emission)**:
                    *   Ghi log chi tiết quá trình trích xuất, bao gồm các quyết định và độ tin cậy.
                    *   Phát các sự kiện như `KnowledgeCandidateAvailableEvent` (chứa các `OntologyEntityCandidate` và `RelationshipCandidate`), `EmbeddingGeneratedEvent`.

            * **10.2.3.4. Dữ liệu Đầu ra / Sự kiện Tạo ra (Output Data / Generated Events)**
                * **Dữ liệu**:
                    * ` OntologyEntityCandidate`: Các đối tượng chứa thông tin về thực thể tiềm năng cần được xác thực trước khi thêm vào ontology chính thức.
                    * ` RelationshipCandidate`: Các đối tượng chứa thông tin về mối quan hệ tiềm năng.
                    *   Vector Embeddings: Các vector nhúng của tri thức, sẵn sàng để lưu trữ.
                * **Sự kiện (Events)**:
                    * ` KnowledgeCandidateAvailableEvent`: Thông báo có các ứng viên tri thức mới sẵn sàng để được xem xét hoặc xác thực. Payload chứa danh sách các candidates.
                    * ` EmbeddingGeneratedEvent`: Thông báo vector embedding đã được tạo cho một `KnowledgeSnippet` hoặc thực thể. Payload chứa ID của đối tượng và vector embedding (hoặc tham chiếu đến nơi lưu trữ).
                    * ` ExtractionQualityFeedbackEvent`: (Nâng cao) Sự kiện để thu thập phản hồi về chất lượng trích xuất, có thể được sử dụng để cải thiện mô hình hoặc prompts.

            * **10.2.3.5. Tương tác với các Thành phần Khác (Interaction with Other Components)**
                * **`DataProcessingAgent`**: Nhận `KnowledgeSnippet` đã được xử lý cơ bản.
                * **TRM Ontology / Knowledge Base**: Truy cập sâu để đọc schema, định nghĩa, và các thực thể hiện có. Kết quả trích xuất (candidates) sẽ được đề xuất để cập nhật vào đây sau quá trình xác thực.
                * **`AgentManager`**: Báo cáo trạng thái, log, nhận cấu hình và lệnh.
                * **`SystemEventBus`**: Lắng nghe `KnowledgeSnippetCreatedEvent`, phát `KnowledgeCandidateAvailableEvent`, `EmbeddingGeneratedEvent`.
                * **LLM/NLP Services**: Tương tác mạnh mẽ với các dịch vụ này để thực hiện các tác vụ trích xuất.
                * **`KnowledgeValidationAgent` (sẽ định nghĩa sau)**: Gửi `KnowledgeCandidateAvailableEvent` đến agent này để thực hiện xác thực thủ công hoặc bán tự động.
                * **Vector Database (ví dụ: Supabase Vector)**: Lưu trữ các vector embedding được tạo ra.
                * **`UserInterfaceAgent` (sẽ định nghĩa sau)**: Có thể hiển thị các ứng viên tri thức cho người dùng để xác thực.

            * **10.2.3.6. Ví dụ Cụ thể (Specific Example)**
                * **Bối cảnh**: `KnowledgeExtractionAgent` nhận được một `KnowledgeSnippetCreatedEvent` từ `DataProcessingAgent`. Snippet này chứa một đoạn email: "Project Alpha is facing a delay due to resource unavailability for Task T2. John Doe (john.doe@example.com) is the project manager. Meeting scheduled for next Monday to discuss mitigation."
                * **Cấu hình `KnowledgeExtractionAgent`**:
                    *   Sử dụng LLM (ví dụ: GPT-4) với prompt được thiết kế để trích xuất dự án, nhiệm vụ, nhân sự, vấn đề, và các sự kiện.
                    *   Ontology có các `EntityType` như `Project`, `Task`, `Person`, `Issue`, `MeetingEvent`.
                * **Hoạt động**:
                    1.  Agent nhận `KnowledgeSnippet`.
                    2.  Gửi nội dung snippet và prompt cho LLM.
                    3.  LLM trả về kết quả trích xuất, ví dụ:
                        *   Project: "Project Alpha"
                        *   Task: "Task T2"
                        *   Issue: "delay due to resource unavailability" (liên quan đến "Task T2")
                        *   Person: "John Doe", Email: "john.doe@example.com", Role: "project manager" (cho "Project Alpha")
                        *   MeetingEvent: "meeting", Date: "next Monday" (YYYY-MM-DD được chuẩn hóa), Purpose: "discuss mitigation" (liên quan đến "Issue")
                    4.  Agent thực hiện Entity Resolution:
                        *   Kiểm tra xem "Project Alpha" đã tồn tại trong ontology chưa. Giả sử chưa.
                        *   Kiểm tra "John Doe" / "john.doe@example.com". Giả sử đã có `Person` entity `Person_JD1` với email này.
                    5.  Tạo các `OntologyEntityCandidate` và `RelationshipCandidate`:
                        * ` OntologyEntityCandidate(type=Project, name="Project Alpha", properties={...}, confidence=0.9)`
                        * ` OntologyEntityCandidate(type=Task, name="Task T2", properties={...}, confidence=0.85)`
                        * ` OntologyEntityCandidate(type=Issue, description="delay due to resource unavailability", confidence=0.92)`
                        * ` OntologyEntityCandidate(type=MeetingEvent, purpose="discuss mitigation", scheduledTime="YYYY-MM-DD", confidence=0.88)`
                        * ` RelationshipCandidate(from=ProjectAlpha_candidate, type=HAS_MANAGER, to=Person_JD1, confidence=0.95)`
                        * ` RelationshipCandidate(from=ProjectAlpha_candidate, type=HAS_TASK, to=TaskT2_candidate, confidence=0.9)`
                        * ` RelationshipCandidate(from=TaskT2_candidate, type=HAS_ISSUE, to=Issue_candidate, confidence=0.92)`
                        * ` RelationshipCandidate(from=MeetingEvent_candidate, type=DISCUSSES_ISSUE, to=Issue_candidate, confidence=0.88)`
                    6.  Tạo embedding cho nội dung snippet (nếu được cấu hình).
                    7.  Phát `KnowledgeCandidateAvailableEvent` với các candidates này.
                    8.  (Nếu có) Phát `EmbeddingGeneratedEvent` với ID của snippet và embedding.

        * **10.2.4. `KnowledgeValidationAgent` (Agent Xác thực Tri thức)**
            * **10.2.4.1. Mục tiêu (Objective)**
                *   Tiếp nhận các `OntologyEntityCandidate` và `RelationshipCandidate` từ `KnowledgeExtractionAgent` (thông qua `KnowledgeCandidateAvailableEvent`).
                *   Thực hiện các quy trình xác thực tự động và bán tự động để đánh giá tính đúng đắn, độ tin cậy, và sự phù hợp của các ứng viên tri thức này với TRM Ontology.
                *   Tương tác với người dùng (chuyên gia domain, quản trị viên ontology) để nhận phản hồi và quyết định cuối cùng về việc chấp nhận, từ chối, hoặc sửa đổi các ứng viên.
                *   Đảm bảo rằng chỉ có tri thức chất lượng cao, đã được xác thực mới được tích hợp vào TRM Ontology chính thức.
                *   Cung cấp cơ chế học hỏi từ các quyết định xác thực để cải thiện quy trình trích xuất và xác thực trong tương lai.

            * **10.2.4.2. Dữ liệu Đầu vào (Input Data)**
                * **`KnowledgeCandidateAvailableEvent`**: Lắng nghe sự kiện này để nhận các `OntologyEntityCandidate` và `RelationshipCandidate`.
                * **`OntologyEntityCandidate` / `RelationshipCandidate`**: Các đối tượng chứa thông tin chi tiết về tri thức tiềm năng, bao gồm nội dung, nguồn, bằng chứng, điểm tin cậy, và đề xuất ánh xạ ontology.
                * **TRM Ontology**: Truy cập để so sánh với tri thức hiện có, kiểm tra ràng buộc, và hiểu ngữ cảnh.
                * **Quy tắc Xác thực (Validation Rules)**: Một tập hợp các quy tắc được định cấu hình (có thể lưu trong ontology) để tự động kiểm tra các ứng viên (ví dụ: kiểm tra kiểu dữ liệu, tính nhất quán, xung đột tiềm ẩn).
                * **Phản hồi từ Người dùng (User Feedback)**: Nhận quyết định (chấp nhận, từ chối, sửa đổi) và bình luận từ người dùng thông qua một giao diện (ví dụ: do `UserInterfaceAgent` cung cấp).
                * **Cấu hình Agent**: Ngưỡng tin cậy cho tự động chấp nhận/từ chối, vai trò người dùng được phép xác thực, quy trình leo thang.

            * **10.2.4.3. Các Hành động Chính (Key Actions)**
                * **Tiếp nhận và Ưu tiên Hóa Ứng viên (Candidate Reception and Prioritization)**:
                    *   Nhận danh sách các ứng viên tri thức.
                    *   Ưu tiên hóa việc xem xét dựa trên nguồn, độ tin cậy, loại thực thể/mối quan hệ, hoặc tác động tiềm năng.
                * **Xác thực Tự động (Automated Validation)**:
                    *   Áp dụng các quy tắc xác thực đã định cấu hình (ví dụ: kiểm tra định dạng, giá trị trong phạm vi cho phép, không trùng lặp với thực thể đã tồn tại một cách rõ ràng, tính nhất quán với các mối quan hệ hiện có).
                    *   Kiểm tra chéo với các nguồn dữ liệu đáng tin cậy khác (nếu có).
                    *   Gắn cờ các ứng viên vượt qua hoặc thất bại trong các bước kiểm tra tự động.
                * **Chuẩn bị cho Xác thực Thủ công/Bán tự động (Preparation for Manual/Semi-Automated Validation)**:
                    *   Trình bày thông tin ứng viên một cách rõ ràng cho người dùng, bao gồm bằng chứng, điểm tin cậy, và kết quả xác thực tự động.
                    *   Đề xuất các hành động (ví dụ: chấp nhận, từ chối, yêu cầu thêm thông tin, sửa đổi).
                * **Tương tác Người dùng để Xác thực (User Interaction for Validation)**:
                    *   Thông qua `UserInterfaceAgent` hoặc một cơ chế khác, cho phép người dùng xem xét, sửa đổi, chấp nhận hoặc từ chối các ứng viên.
                    *   Cho phép người dùng cung cấp lý do cho quyết định của họ.
                * **Xử lý Quyết định (Decision Processing)**:
                    *   Nếu được chấp nhận: Chuyển đổi `OntologyEntityCandidate` thành `OntologyEntity` chính thức và `RelationshipCandidate` thành `Relationship` chính thức. Kích hoạt việc lưu trữ vào TRM Ontology.
                    *   Nếu bị từ chối: Ghi lại lý do, có thể cung cấp phản hồi ngược lại cho `KnowledgeExtractionAgent` để cải thiện.
                    *   Nếu cần sửa đổi: Cho phép người dùng chỉnh sửa thông tin trước khi chấp nhận.
                * **Cập nhật Ontology (Ontology Update)**: Kích hoạt việc ghi các thực thể và mối quan hệ đã được xác thực vào cơ sở dữ liệu ontology.
                * **Học hỏi và Cải tiến (Learning and Improvement)**:
                    *   Phân tích các quyết định xác thực (ví dụ: những loại ứng viên nào thường bị từ chối, lý do là gì) để tinh chỉnh các quy tắc xác thực tự động hoặc các prompts cho `KnowledgeExtractionAgent`.
                    *   Cập nhật điểm tin cậy của các nguồn hoặc phương pháp trích xuất.
                * **Ghi Log và Phát Sự kiện (Logging and Event Emission)**:
                    *   Ghi log tất cả các bước xác thực và quyết định.
                    *   Phát các sự kiện như `KnowledgeValidatedEvent` (chứa tri thức đã được chấp nhận), `KnowledgeRejectedEvent`, `OntologyUpdatedEvent`.

            * **10.2.4.4. Dữ liệu Đầu ra / Sự kiện Tạo ra (Output Data / Generated Events)**
                * **Dữ liệu**:
                    *   Các `OntologyEntity` và `Relationship` đã được xác thực và sẵn sàng để tích hợp vào TRM Ontology.
                * **Sự kiện (Events)**:
                    * ` KnowledgeValidatedEvent`: Thông báo một hoặc nhiều ứng viên tri thức đã được xác thực và chấp nhận. Payload chứa các thực thể/mối quan hệ đã được xác thực.
                    * ` KnowledgeRejectedEvent`: Thông báo một hoặc nhiều ứng viên tri thức đã bị từ chối. Payload chứa thông tin về ứng viên và lý do từ chối.
                    * ` OntologyUpdatedEvent`: Thông báo rằng TRM Ontology đã được cập nhật với tri thức mới.
                    * ` ValidationFeedbackLoopEvent`: (Nâng cao) Sự kiện gửi phản hồi về quy trình trích xuất cho `KnowledgeExtractionAgent`.

            * **10.2.4.5. Tương tác với các Thành phần Khác (Interaction with Other Components)**
                * **`KnowledgeExtractionAgent`**: Nhận `KnowledgeCandidateAvailableEvent`. Cung cấp phản hồi (ví dụ: qua `ValidationFeedbackLoopEvent`).
                * **TRM Ontology / Knowledge Base**: Đọc để so sánh, ghi tri thức đã được xác thực.
                * **`AgentManager`**: Báo cáo trạng thái, log, nhận cấu hình.
                * **`SystemEventBus`**: Lắng nghe `KnowledgeCandidateAvailableEvent`, phát `KnowledgeValidatedEvent`, `KnowledgeRejectedEvent`, `OntologyUpdatedEvent`.
                * **`UserInterfaceAgent` (sẽ định nghĩa sau)**: Tương tác chặt chẽ để trình bày ứng viên cho người dùng và nhận phản hồi/quyết định từ họ.
                * **Người dùng (Chuyên gia Domain, Quản trị viên Ontology)**: Là người ra quyết định cuối cùng trong nhiều trường hợp.
                * **Rule Engine (nếu có)**: Có thể sử dụng để thực thi các quy tắc xác thực tự động.

            * **10.2.4.6. Ví dụ Cụ thể (Specific Example)**
                * **Bối cảnh**: `KnowledgeValidationAgent` nhận được `KnowledgeCandidateAvailableEvent` từ `KnowledgeExtractionAgent` với các ứng viên được trích xuất từ email trong ví dụ 10.2.3.6 (Project Alpha, Task T2, John Doe, etc.).
                * **Cấu hình `KnowledgeValidationAgent`**:
                    *   Quy tắc tự động: Nếu `confidenceScore` < 0.7, tự động yêu cầu xác thực thủ công. Nếu một `Person` candidate có email đã tồn tại nhưng tên khác biệt > 2 ký tự, gắn cờ "potential duplicate, needs review".
                    *   Chuyên gia "Alice" được chỉ định để xác thực các `Project` và `Issue` candidates.
                * **Hoạt động**:
                    1.  Agent nhận các candidates.
                    2.  Xác thực tự động:
                        * ` OntologyEntityCandidate(type=Project, name="Project Alpha", confidence=0.9)` -> Vượt qua kiểm tra tin cậy ban đầu.
                        *   Giả sử không có `Project` nào tên "Project Alpha" đã tồn tại.
                    3.  Chuẩn bị cho xác thực thủ công: Gửi thông tin về "Project Alpha" candidate (và các candidates liên quan như Task, Issue) đến `UserInterfaceAgent` để Alice xem xét.
                    4.  Tương tác người dùng:
                        *   Alice xem xét "Project Alpha", các thuộc tính, và mối quan hệ được đề xuất. Cô ấy đồng ý rằng đây là một dự án mới và hợp lệ.
                        *   Alice nhấn "Chấp nhận" cho "Project Alpha" và các mối quan hệ liên quan đến nó.
                    5.  Xử lý quyết định: Agent nhận được quyết định chấp nhận từ Alice.
                    6.  Cập nhật Ontology: Agent kích hoạt việc tạo `OntologyEntity` cho "Project Alpha", "Task T2", "Issue", "MeetingEvent" và các `Relationship` tương ứng trong TRM Ontology.
                    7.  Phát `KnowledgeValidatedEvent` với thông tin về các thực thể và mối quan hệ mới được thêm vào.
                    8.  Phát `OntologyUpdatedEvent`.
                    9.  Ghi log toàn bộ quá trình.

        * **10.2.5. `ProjectManagementAgent` (Agent Quản lý Dự án)**
            * **10.2.5.1. Mục tiêu (Objective)**
                *   Hỗ trợ Founder và các Agent khác trong việc theo dõi, điều phối, cập nhật trạng thái, và báo cáo về các `Project`, `Task`, `SubTask`, `Milestone` và các thực thể liên quan đến quản lý dự án trong TRM Ontology.
                *   Tự động hóa các quy trình quản lý dự án lặp đi lặp lại, chẳng hạn như nhắc nhở deadline, cảnh báo rủi ro tiềm ẩn dựa trên dữ liệu, và tạo báo cáo tiến độ.
                *   Cung cấp một cái nhìn tổng quan và chi tiết về tình hình các dự án cho Founder.
                *   Tạo điều kiện cho việc quản lý dự án dựa trên ontology, đảm bảo tính nhất quán và liên kết dữ liệu.

            * **10.2.5.2. Dữ liệu Đầu vào (Input Data)**
                * **TRM Ontology**: Truy cập liên tục để đọc thông tin về `Project`, `Task`, `SubTask`, `Milestone`, `Person` (vai trò, phân công), `TimeLog`, `Issue`, `Risk`, `Dependency`, `ProjectStatus`, `TaskStatus`, `Priority`, `Deadline`, etc.
                * **Sự kiện Hệ thống (System Events)**:
                    * ` TaskStatusChangedEvent`: Khi trạng thái một `Task` thay đổi (ví dụ: từ `Open` sang `InProgress`).
                    * ` TimeLogCreatedEvent`: Khi một `TimeLog` mới được ghi nhận.
                    * ` IssueReportedEvent`: Khi một `Issue` mới được báo cáo liên quan đến một `Project` hoặc `Task`.
                    * ` DeadlineApproachingEvent`: (Có thể do chính Agent này tạo ra hoặc một `SchedulingAgent` riêng biệt) Thông báo deadline sắp tới.
                    * ` ProjectCreatedEvent`, `TaskCreatedEvent`: Khi các thực thể dự án mới được tạo.
                * **Yêu cầu từ Founder/User (User Requests)**: Ví dụ: "Tạo báo cáo tiến độ cho Project X", "Liệt kê các task quá hạn của John Doe", "Ước tính thời gian hoàn thành Task Y dựa trên TimeLog hiện tại". (Thông qua `UserInterfaceAgent`).
                * **Cấu hình Agent**: Ngưỡng cảnh báo (ví dụ: % hoàn thành task dưới mức kỳ vọng), quy tắc leo thang, mẫu báo cáo.

            * **10.2.5.3. Các Hành động Chính (Key Actions)**
                * **Theo dõi Tiến độ Dự án và Task (Project and Task Progress Monitoring)**:
                    *   Liên tục quét TRM Ontology để cập nhật trạng thái, % hoàn thành, thời gian đã sử dụng so với ước tính cho `Project` và `Task`.
                    *   So sánh tiến độ thực tế với kế hoạch (ví dụ: `Milestone` deadlines).
                * **Quản lý Deadline và Nhắc nhở (Deadline Management and Reminders)**:
                    *   Xác định các `Task` và `Milestone` sắp đến hạn hoặc quá hạn.
                    *   Gửi thông báo/nhắc nhở đến `Person` được phân công hoặc các `Agent` liên quan (ví dụ: qua `NotificationAgent` hoặc trực tiếp đến `UserInterfaceAgent`).
                * **Phân tích Rủi ro Cơ bản (Basic Risk Analysis)**:
                    *   Xác định các rủi ro tiềm ẩn dựa trên dữ liệu, ví dụ: task bị chậm trễ kéo dài, `Issue` nghiêm trọng chưa được giải quyết, `Dependency` bị chặn.
                    *   Gắn cờ các `Project` hoặc `Task` có rủi ro cao.
                * **Tạo Báo cáo (Report Generation)**:
                    *   Tạo các báo cáo tiến độ định kỳ hoặc theo yêu cầu (ví dụ: báo cáo hàng tuần, báo cáo theo `Project`, báo cáo theo `Person`).
                    *   Các báo cáo có thể bao gồm: danh sách task hoàn thành, task đang thực hiện, task quá hạn, % hoàn thành dự án, `TimeLog` summary, `Issue` nổi bật.
                * **Hỗ trợ Ước tính và Lập kế hoạch (Estimation and Planning Support)**:
                    *   Dựa trên dữ liệu `TimeLog` lịch sử và thông tin `Task`, hỗ trợ ước tính thời gian hoàn thành cho các task mới hoặc còn lại.
                    *   Phân tích `Dependency` giữa các `Task` để xác định đường găng (critical path) cơ bản.
                * **Cập nhật Trạng thái Tự động (Automated Status Updates)**:
                    *   Trong một số trường hợp, có thể tự động cập nhật trạng thái `Task` hoặc `Project` dựa trên các sự kiện (ví dụ: tất cả `SubTask` của một `Task` đều `Completed` -> cập nhật `Task` thành `Completed`). Cần có quy tắc rõ ràng.
                * **Quản lý Phân công (Assignment Management)**:
                    *   Theo dõi việc phân công `Task` cho `Person`.
                    *   Cảnh báo nếu có `Person` bị quá tải hoặc `Task` quan trọng chưa được phân công.
                * **Ghi Log và Phát Sự kiện (Logging and Event Emission)**:
                    *   Ghi log các hoạt động quản lý dự án.
                    *   Phát các sự kiện như `ProjectProgressReportGeneratedEvent`, `DeadlineMissedAlertEvent`, `RiskIdentifiedEvent`.

            * **10.2.5.4. Dữ liệu Đầu ra / Sự kiện Tạo ra (Output Data / Generated Events)**
                * **Dữ liệu**:
                    *   Báo cáo tiến độ dự án (dưới dạng văn bản, JSON, hoặc cấu trúc dữ liệu khác).
                    *   Danh sách các task cần chú ý, rủi ro đã xác định.
                    *   Các cập nhật cho các thuộc tính của `Project`, `Task` trong ontology (ví dụ: `calculatedProgress`, `riskLevel`).
                * **Sự kiện (Events)**:
                    * ` ProjectProgressReportGeneratedEvent`: Chứa báo cáo vừa được tạo.
                    * ` DeadlineApproachingAlertEvent`: Thông báo deadline sắp tới.
                    * ` DeadlineMissedAlertEvent`: Thông báo deadline đã bị bỏ lỡ.
                    * ` TaskOverdueAlertEvent`: Thông báo task đã quá hạn.
                    * ` RiskIdentifiedEvent`: Thông báo một rủi ro mới đã được xác định liên quan đến dự án/task.
                    * ` ProjectStatusUpdatedEvent`, `TaskStatusUpdatedEvent`: (Nếu agent tự động cập nhật).

            * **10.2.5.5. Tương tác với các Thành phần Khác (Interaction with Other Components)**
                * **TRM Ontology / Knowledge Base**: Nguồn dữ liệu chính và cũng là nơi lưu trữ các thông tin cập nhật.
                * **`UserInterfaceAgent`**: Hiển thị thông tin, báo cáo, cảnh báo cho Founder/người dùng. Nhận yêu cầu tạo báo cáo hoặc truy vấn thông tin dự án từ người dùng.
                * **`DataSensingAgent` / `DataProcessingAgent` / `KnowledgeExtractionAgent`**: Các agent này cung cấp dữ liệu đầu vào gián tiếp bằng cách cập nhật ontology với thông tin mới (ví dụ: `TimeLog` từ email, `Issue` từ Slack).
                * **`NotificationAgent` (nếu có)**: Gửi các thông báo và cảnh báo đến người dùng.
                * **`AgentManager`**: Báo cáo trạng thái, log, nhận cấu hình.
                * **`SystemEventBus`**: Lắng nghe các sự kiện liên quan đến dự án, phát các sự kiện do chính nó tạo ra.
                * **Founder/Người dùng**: Người tiêu thụ chính của các báo cáo và cảnh báo, người đưa ra yêu cầu.

            * **10.2.5.6. Ví dụ Cụ thể (Specific Example)**
                * **Bối cảnh**: `Project Alpha` đang diễn ra. `Task T2` ("Develop Feature X") được phân công cho "John Doe" với deadline là 2023-12-15. John Doe đã log 10 giờ vào `Task T2` (ước tính ban đầu là 20 giờ). Hôm nay là 2023-12-14.
                * **Hoạt động của `ProjectManagementAgent`**:
                    1.  **Theo dõi Tiến độ**: Agent quét ontology, thấy `Task T2` có `estimatedHours` = 20, `loggedHours` = 10, `status` = `InProgress`, `deadline` = "2023-12-15".
                    2.  **Quản lý Deadline**: Agent xác định `Task T2` có deadline vào ngày mai.
                        *   Phát `DeadlineApproachingAlertEvent` cho `Task T2`.
                        * ` NotificationAgent` (hoặc `UserInterfaceAgent`) có thể bắt sự kiện này và thông báo cho John Doe và Founder.
                    3.  **Tạo Báo cáo (Giả sử có yêu cầu hàng ngày)**:
                        *   Agent tạo báo cáo tiến độ cho `Project Alpha`.
                        *   Báo cáo bao gồm: `Task T2` - 50% hoàn thành (dựa trên logged/estimated hours), deadline 2023-12-15.
                        *   Phát `ProjectProgressReportGeneratedEvent`.
                    4.  **Phân tích Rủi ro (Ví dụ)**: Nếu `Task T1` (một dependency của `Task T2`) bị trễ 2 ngày, agent có thể xác định `Task T2` có nguy cơ bị trễ và tăng `riskLevel` của `Task T2`, đồng thời phát `RiskIdentifiedEvent`.
                    5.  **Sáng hôm sau (2023-12-16)**: Nếu `Task T2` vẫn chưa `Completed`.
                        *   Agent xác định `Task T2` đã quá hạn.
                        *   Phát `TaskOverdueAlertEvent` và `DeadlineMissedAlertEvent`.
                        *   Cập nhật trạng thái của `Task T2` trong báo cáo tiếp theo là "Quá hạn".

        * **10.2.6. `UserInterfaceAgent` (Agent Giao diện Người dùng)**
            * **10.2.6.1. Mục tiêu (Objective)**
                *   Cung cấp một giao diện tương tác (ví dụ: web-based, command-line, hoặc tích hợp vào ứng dụng hiện có) cho Founder và các người dùng được ủy quyền khác để tương tác với Hệ thống AI Agent của TRM.
                *   Hiển thị thông tin từ TRM Ontology và các Agent một cách trực quan, dễ hiểu.
                *   Tiếp nhận yêu cầu, lệnh, và dữ liệu đầu vào từ người dùng và chuyển tiếp đến các Agent hoặc thành phần hệ thống phù hợp.
                *   Hỗ trợ các quy trình làm việc cần sự can thiệp của con người, ví dụ như xác thực tri thức, phê duyệt đề xuất, hoặc cung cấp thông tin bổ sung.
                *   Đảm bảo trải nghiệm người dùng (UX) tốt, hiệu quả và nhất quán.

            * **10.2.6.2. Dữ liệu Đầu vào (Input Data)**
                * **Yêu cầu từ Người dùng (User Input/Commands)**:
                    *   Truy vấn tìm kiếm (ví dụ: "Tìm tất cả dự án liên quan đến 'AI'").
                    *   Lệnh (ví dụ: "Tạo Task mới cho Project Alpha", "Hiển thị chi tiết Tension XYZ").
                    *   Dữ liệu nhập liệu (ví dụ: nội dung mô tả cho một `Issue` mới, phản hồi cho một `KnowledgeCandidate`).
                    *   Lựa chọn từ các tùy chọn (ví dụ: chấp nhận/từ chối một `KnowledgeCandidate`).
                * **Dữ liệu từ các Agent Khác (Data from Other Agents)**:
                    *   Thông tin cần hiển thị (ví dụ: danh sách `KnowledgeCandidate` từ `KnowledgeValidationAgent`, báo cáo từ `ProjectManagementAgent`, cảnh báo từ `NotificationAgent`).
                    *   Yêu cầu tương tác người dùng (ví dụ: `KnowledgeValidationAgent` yêu cầu người dùng xác thực một ứng viên).
                * **Dữ liệu từ TRM Ontology**: Dữ liệu được truy xuất để hiển thị cho người dùng.
                * **Thông tin Người dùng (User Profile/Preferences)**: Vai trò, quyền hạn, cài đặt giao diện (nếu có).
                * **Sự kiện Hệ thống (System Events)**: Một số sự kiện có thể kích hoạt cập nhật giao diện người dùng (ví dụ: `OntologyUpdatedEvent` có thể làm mới một danh sách các thực thể).

            * **10.2.6.3. Các Hành động Chính (Key Actions)**
                * **Hiển thị Dữ liệu (Data Display and Visualization)**:
                    *   Trình bày thông tin từ TRM Ontology (ví dụ: danh sách `Project`, chi tiết `Task`, biểu đồ mối quan hệ).
                    *   Hiển thị kết quả từ các Agent (ví dụ: báo cáo, danh sách ứng viên cần xác thực, thông báo).
                    *   Sử dụng các thành phần UI phù hợp (bảng, biểu đồ, form, danh sách, thông báo pop-up).
                * **Tiếp nhận và Xử lý Đầu vào từ Người dùng (User Input Processing)**:
                    *   Xác thực đầu vào của người dùng.
                    *   Phiên dịch lệnh của người dùng thành các hành động hoặc sự kiện cụ thể cho hệ thống.
                    *   Chuyển tiếp yêu cầu đến `AgentManager` hoặc trực tiếp đến các Agent chuyên biệt.
                * **Quản lý Phiên làm việc Người dùng (User Session Management)**:
                    *   Xác thực và ủy quyền người dùng.
                    *   Duy trì trạng thái phiên làm việc.
                * **Điều hướng và Tổ chức Giao diện (Interface Navigation and Organization)**:
                    *   Cung cấp cấu trúc điều hướng rõ ràng.
                    *   Tổ chức thông tin một cách logic và dễ truy cập.
                * **Tương tác với Agent Chuyên biệt (Interaction with Specialized Agents)**:
                    *   Gửi yêu cầu đến `KnowledgeValidationAgent` để lấy danh sách ứng viên và gửi lại quyết định của người dùng.
                    *   Yêu cầu `ProjectManagementAgent` tạo báo cáo hoặc hiển thị thông tin dự án.
                    *   Nhận và hiển thị thông báo từ `NotificationAgent`.
                    *   Gửi các `Tension` mới được người dùng nhập vào cho `TensionResolutionAgent` (hoặc `AGE`).
                * **Cung cấp Phản hồi cho Người dùng (Providing User Feedback)**:
                    *   Thông báo trạng thái của các yêu cầu (ví dụ: "Đang xử lý...", "Thành công", "Lỗi").
                    *   Hiển thị các thông báo lỗi một cách thân thiện.
                * **Tùy chỉnh Giao diện (Interface Customization - Nâng cao)**:
                    *   Cho phép người dùng tùy chỉnh một số khía cạnh của giao diện dựa trên vai trò hoặc sở thích.
                * **Ghi Log Hoạt động Người dùng (User Activity Logging)**:
                    *   Ghi lại các hành động chính của người dùng cho mục đích kiểm toán hoặc phân tích.

            * **10.2.6.4. Dữ liệu Đầu ra / Sự kiện Tạo ra (Output Data / Generated Events)**
                * **Dữ liệu (Gửi đến các Agent/Hệ thống khác)**:
                    *   Yêu cầu/Lệnh đã được xử lý (ví dụ: `CreateTaskCommand`, `ValidateKnowledgeCandidateDecision`).
                    *   Dữ liệu do người dùng nhập (ví dụ: nội dung của một `Tension` mới).
                * **Sự kiện (Có thể phát ra để các Agent khác lắng nghe)**:
                    * ` UserLoginEvent`, `UserLogoutEvent`.
                    * ` UserActionSubmittedEvent` (chứa chi tiết hành động của người dùng).
                    * ` NewTensionReportedByUserEvent`.
                    * ` KnowledgeCandidateReviewedEvent` (chứa quyết định của người dùng về một ứng viên).

            * **10.2.6.5. Tương tác với các Thành phần Khác (Interaction with Other Components)**
                * **Người dùng (Founder, Chuyên gia Domain, etc.)**: Đối tượng tương tác chính.
                * **Tất cả các Agent Chuyên biệt (Specialized Agents)**: Là cầu nối giữa người dùng và các agent này.
                    * ` KnowledgeValidationAgent`: Hiển thị ứng viên, nhận quyết định.
                    * ` ProjectManagementAgent`: Hiển thị thông tin dự án, nhận yêu cầu báo cáo.
                    * ` TensionResolutionAgent` / `AGE`: Nhận `Tension` mới, hiển thị giải pháp đề xuất.
                    * ` NotificationAgent`: Hiển thị thông báo.
                * **`AgentManager`**: Có thể nhận một số lệnh quản lý hệ thống từ người dùng có quyền.
                * **`SystemEventBus`**: Phát và có thể lắng nghe một số sự kiện để cập nhật UI.
                * **TRM Ontology / Knowledge Base**: Truy vấn dữ liệu để hiển thị.
                * **Hệ thống Xác thực (Authentication System)**: Để quản lý đăng nhập người dùng.

            * **10.2.6.6. Ví dụ Cụ thể (Specific Example)**
                * **Bối cảnh**: Founder muốn xem xét các ứng viên tri thức đang chờ xác thực.
                * **Hoạt động**:
                    1.  Founder đăng nhập vào hệ thống thông qua giao diện do `UserInterfaceAgent` cung cấp.
                    2.  `UserInterfaceAgent` xác thực Founder.
                    3.  Founder điều hướng đến mục "Xác thực Tri thức".
                    4.  `UserInterfaceAgent` gửi yêu cầu đến `KnowledgeValidationAgent` để lấy danh sách các `KnowledgeCandidate` đang chờ xử lý cho Founder.
                    5.  `KnowledgeValidationAgent` trả về danh sách các ứng viên (ví dụ: một `OntologyEntityCandidate` cho "NewMeetingSoftware" và một `RelationshipCandidate` "Project Alpha uses NewMeetingSoftware").
                    6.  `UserInterfaceAgent` hiển thị danh sách này cho Founder, bao gồm bằng chứng, điểm tin cậy, và các đề xuất.
                    7.  Founder xem xét "NewMeetingSoftware", thấy bằng chứng hợp lý và quyết định "Chấp nhận".
                    8.  `UserInterfaceAgent` ghi nhận lựa chọn của Founder và gửi quyết định này (cùng với ID của candidate) đến `KnowledgeValidationAgent`.
                    9.  `UserInterfaceAgent` cập nhật giao diện để hiển thị rằng ứng viên đó đã được xử lý và có thể hiển thị thông báo "Đã chấp nhận ứng viên thành công".
                    10. `KnowledgeValidationAgent` xử lý quyết định và cập nhật ontology, sau đó có thể phát `KnowledgeValidatedEvent`. `UserInterfaceAgent` có thể lắng nghe sự kiện này để làm mới danh sách (nếu cần).

        * **10.2.7. `ResolutionCoordinatorAgent` (Agent Điều phối Giải pháp)**
            * **10.2.7.1. Mục tiêu (Objective)**
                *   Điều phối quá trình giải quyết các `Tension`, `Issue`, hoặc `Problem` đã được xác định trong hệ thống TRM.
                *   Lựa chọn và kích hoạt các `Agent` chuyên biệt phù hợp (ví dụ: `TensionResolutionAgent`, `AutomatedTaskExecutionAgent`, `CommunicationAgent`) hoặc đề xuất các hành động cho Founder để giải quyết một vấn đề cụ thể.
                *   Theo dõi tiến trình giải quyết và đảm bảo các vấn đề được xử lý một cách hiệu quả và kịp thời.
                *   Học hỏi từ các quy trình giải quyết trước đó để tối ưu hóa việc lựa chọn chiến lược và Agent trong tương lai.

            * **10.2.7.2. Dữ liệu Đầu vào (Input Data)**
                * **Sự kiện Vấn đề (Problem Events)**:
                    * ` TensionDetectedEvent` (từ `TensionDetectionAgent`): Chứa thông tin về `Tension` được phát hiện.
                    * ` IssueReportedEvent` (từ `ProjectManagementAgent` hoặc người dùng qua `UserInterfaceAgent`): Thông tin về `Issue`.
                    * ` RiskIdentifiedEvent` (từ `ProjectManagementAgent`): Thông tin về `Risk` cần giải quyết.
                    * ` SystemErrorEvent` (từ `AgentManager` hoặc các Agent khác): Thông báo lỗi hệ thống.
                * **TRM Ontology**:
                    *   Thông tin chi tiết về `Tension`, `Issue`, `Risk`, `Project`, `Task`, `Person` liên quan.
                    *   Kiến thức về các giải pháp đã từng áp dụng (`SolutionPattern`, `PastResolutionRecord`).
                    *   Thông tin về năng lực và trạng thái của các `Agent` khác (`AgentCapability`, `AgentStatus`).
                * **Quy tắc Điều phối (Coordination Rules / Policies)**: Các quy tắc được định cấu hình để hướng dẫn việc lựa chọn Agent hoặc chiến lược giải quyết (ví dụ: "Nếu `Tension` thuộc loại 'Resource Conflict', ưu tiên kích hoạt `ResourceAllocationAgent'").
                * **Phản hồi từ Founder/User** (qua `UserInterfaceAgent`): Quyết định về việc lựa chọn giải pháp được đề xuất, hoặc yêu cầu can thiệp thủ công.
                * **Trạng thái và Kết quả từ các Agent Thực thi (Execution Agent Status/Results)**: Phản hồi từ các Agent được giao nhiệm vụ giải quyết.

            * **10.2.7.3. Các Hành động Chính (Key Actions)**
                * **Tiếp nhận và Phân tích Vấn đề (Problem Reception and Analysis)**:
                    *   Thu thập tất cả thông tin liên quan đến `Tension`, `Issue`, `Risk` từ sự kiện và TRM Ontology.
                    *   Phân loại vấn đề (ví dụ: xung đột tài nguyên, chậm trễ dự án, lỗi kỹ thuật, thiếu thông tin).
                    *   Đánh giá mức độ ưu tiên và tác động của vấn đề.
                * **Lựa chọn Chiến lược và Agent Giải quyết (Strategy and Agent Selection)**:
                    *   Dựa trên loại vấn đề, quy tắc điều phối, và kiến thức từ các giải pháp trước đó, xác định chiến lược giải quyết phù hợp.
                    *   Xác định (các) `Agent` chuyên biệt có khả năng thực hiện chiến lược đó.
                    *   Nếu không có Agent tự động phù hợp, hoặc vấn đề quá phức tạp, chuẩn bị đề xuất cho Founder.
                * **Kích hoạt Agent Thực thi / Đề xuất Hành động (Execution Agent Activation / Action Proposal)**:
                    *   Nếu một Agent tự động được chọn: Gửi yêu cầu hoặc kích hoạt Agent đó với các tham số cần thiết (ví dụ: yêu cầu `TensionResolutionAgent` áp dụng một `SolutionPattern` cụ thể).
                    *   Nếu cần sự can thiệp của con người: Thông báo cho Founder/người dùng có liên quan qua `UserInterfaceAgent` với các đề xuất hành động và thông tin hỗ trợ quyết định.
                * **Theo dõi Tiến trình Giải quyết (Resolution Progress Monitoring)**:
                    *   Lắng nghe các sự kiện phản hồi từ các Agent thực thi (ví dụ: `ResolutionTaskStartedEvent`, `ResolutionStepCompletedEvent`, `ResolutionFailedEvent`).
                    *   Cập nhật trạng thái của `Tension`, `Issue`, `Risk` trong TRM Ontology (ví dụ: từ `Open` sang `ResolutionInProgress`, sau đó là `Resolved` hoặc `Escalated`).
                * **Xử lý Leo thang (Escalation Handling)**:
                    *   Nếu một giải pháp tự động thất bại hoặc không tiến triển, leo thang vấn đề lên Founder hoặc một cấp quản lý cao hơn thông qua `UserInterfaceAgent`.
                    *   Đề xuất các lựa chọn thay thế.
                * **Xác nhận Giải pháp và Đóng Vấn đề (Solution Confirmation and Closure)**:
                    *   Khi một vấn đề được báo cáo là đã giải quyết (bởi Agent hoặc người dùng), xác minh lại (nếu có thể) rằng giải pháp đã hiệu quả.
                    *   Cập nhật trạng thái cuối cùng của `Tension`, `Issue`, `Risk` thành `Resolved` hoặc `Closed` trong TRM Ontology.
                    *   Lưu trữ thông tin về quy trình giải quyết (ví dụ: `ResolutionRecord`) để học hỏi trong tương lai.
                * **Học hỏi và Tinh chỉnh (Learning and Refinement)**:
                    *   Phân tích hiệu quả của các chiến lược và Agent đã được sử dụng.
                    *   Cập nhật các quy tắc điều phối hoặc mô hình lựa chọn Agent dựa trên kết quả.
                * **Ghi Log và Phát Sự kiện (Logging and Event Emission)**:
                    *   Ghi log tất cả các quyết định điều phối và các bước trong quy trình giải quyết.
                    *   Phát các sự kiện như `ResolutionInitiatedEvent`, `ResolutionProgressUpdateEvent`, `IssueResolvedEvent`, `TensionEscalatedEvent`.

            * **10.2.7.4. Dữ liệu Đầu ra / Sự kiện Tạo ra (Output Data / Generated Events)**
                * **Dữ liệu**:
                    *   Cập nhật trạng thái cho `Tension`, `Issue`, `Risk` trong TRM Ontology.
                    * ` ResolutionRecord` chứa chi tiết về cách một vấn đề được giải quyết.
                    *   Đề xuất hành động cho Founder/người dùng (hiển thị qua `UserInterfaceAgent`).
                * **Sự kiện (Events)**:
                    * ` ResolutionInitiatedEvent`: Thông báo một quy trình giải quyết đã bắt đầu cho một vấn đề cụ thể, chỉ định Agent/chiến lược được chọn.
                    * ` ResolutionStepTriggeredEvent`: Gửi đến Agent thực thi cụ thể, chứa thông tin nhiệm vụ.
                    * ` IssueResolvedEvent`, `TensionResolvedEvent`, `RiskMitigatedEvent`: Thông báo vấn đề đã được giải quyết thành công.
                    * ` ResolutionFailedEvent`: Thông báo một nỗ lực giải quyết đã thất bại.
                    * ` IssueEscalatedEvent`: Thông báo một vấn đề đã được leo thang.

            * **10.2.7.5. Tương tác với các Thành phần Khác (Interaction with Other Components)**
                * **`TensionDetectionAgent`, `ProjectManagementAgent`**: Nhận các sự kiện thông báo vấn đề (`TensionDetectedEvent`, `IssueReportedEvent`, `RiskIdentifiedEvent`).
                * **`TensionResolutionAgent`, `AutomatedTaskExecutionAgent`, `CommunicationAgent`, các Agent chuyên biệt khác**: Kích hoạt và gửi nhiệm vụ cho các Agent này để thực hiện các bước giải quyết. Nhận phản hồi về tiến trình và kết quả.
                * **`UserInterfaceAgent`**: Trình bày các vấn đề, đề xuất giải pháp cho Founder/người dùng. Nhận quyết định và yêu cầu can thiệp thủ công từ người dùng.
                * **TRM Ontology / Knowledge Base**: Đọc thông tin vấn đề, ngữ cảnh, giải pháp lịch sử. Ghi lại tiến trình và kết quả giải quyết.
                * **`AgentManager`**: Báo cáo trạng thái, log, nhận cấu hình. Có thể nhận thông báo về lỗi hệ thống cần điều phối giải quyết.
                * **`SystemEventBus`**: Lắng nghe các sự kiện vấn đề, phát các sự kiện điều phối và cập nhật trạng thái.
                * **Founder/Người dùng**: Người đưa ra quyết định cuối cùng cho các vấn đề phức tạp hoặc được leo thang, người có thể khởi tạo yêu cầu giải quyết.

            * **10.2.7.6. Ví dụ Cụ thể (Specific Example)**
                * **Bối cảnh**: `TensionDetectionAgent` phát hiện một `Tension` loại "ResourceOverallocation" cho "John Doe" (được phân công quá nhiều task có deadline gần nhau). Nó phát một `TensionDetectedEvent`.
                * **Hoạt động của `ResolutionCoordinatorAgent`**:
                    1.  **Tiếp nhận và Phân tích**: Agent nhận `TensionDetectedEvent`. Truy vấn Ontology để lấy chi tiết các task của John Doe, deadline, mức độ ưu tiên. Phân loại đây là "Xung đột tài nguyên".
                    2.  **Lựa chọn Chiến lược và Agent**:
                        *   Quy tắc điều phối: "Nếu `TensionType` là 'ResourceOverallocation' và `Severity` > Medium, ưu tiên kích hoạt `TensionResolutionAgent` với `SolutionPattern` là 'RescheduleTasks' hoặc 'DelegateTasks'".
                        *   Agent quyết định thử `TensionResolutionAgent`.
                    3.  **Kích hoạt Agent Thực thi**:
                        * ` ResolutionCoordinatorAgent` phát `ResolutionStepTriggeredEvent` (hoặc gọi API) đến `TensionResolutionAgent`, yêu cầu nó phân tích và đề xuất giải pháp cho việc quá tải của John Doe (ví dụ: đề xuất dời lịch một số task hoặc gợi ý task có thể giao cho người khác).
                    4.  **Theo dõi Tiến trình**:
                        * ` TensionResolutionAgent` sau khi phân tích, có thể phát một `ProposedSolutionAvailableEvent` với các lựa chọn (ví dụ: "Dời Task Z của John Doe sang tuần sau" hoặc "Giao Task Y của John Doe cho Jane Doe (đang rảnh)").
                        * ` ResolutionCoordinatorAgent` nhận sự kiện này.
                    5.  **Đề xuất Hành động cho Người dùng (nếu cần)**:
                        * ` ResolutionCoordinatorAgent` quyết định rằng việc thay đổi lịch hoặc phân công cần sự chấp thuận của Founder. Nó gửi thông tin các giải pháp đề xuất đến `UserInterfaceAgent`.
                        * ` UserInterfaceAgent` hiển thị các lựa chọn cho Founder. Founder chọn "Giao Task Y cho Jane Doe".
                    6.  **Thực thi Quyết định**: `UserInterfaceAgent` gửi lại quyết định. `ResolutionCoordinatorAgent` kích hoạt `TensionResolutionAgent` (hoặc `ProjectManagementAgent`) để cập nhật ontology (thay đổi người được phân công cho Task Y).
                    7.  **Xác nhận và Đóng Vấn đề**: Sau khi ontology được cập nhật, `ProjectManagementAgent` có thể phát `TaskAssignmentChangedEvent`. `ResolutionCoordinatorAgent` xác nhận `Tension` đã được giải quyết.
                        *   Cập nhật `Tension` thành `Resolved` trong Ontology.
                        *   Phát `TensionResolvedEvent`.
                        *   Ghi `ResolutionRecord`.

        * **10.2.8. `TensionResolutionAgent` (Agent Giải quyết Căng thẳng)**
            * **10.2.8.1. Mục tiêu (Objective)**
                *   Chuyên xử lý và giải quyết các `Tension` cụ thể được giao bởi `ResolutionCoordinatorAgent` hoặc được kích hoạt trực tiếp dựa trên các quy tắc định sẵn.
                *   Áp dụng các `SolutionPattern` (Mẫu Giải pháp) hoặc chiến lược cụ thể để giảm thiểu hoặc loại bỏ `Tension`.
                *   Cung cấp các đề xuất giải pháp, thực hiện các thay đổi (nếu được phép), và báo cáo kết quả giải quyết `Tension`.

            * **10.2.8.2. Dữ liệu Đầu vào (Input Data)**
                * **Yêu cầu Giải quyết Căng thẳng (Tension Resolution Request)**:
                    *   Từ `ResolutionCoordinatorAgent` (thường qua `ResolutionStepTriggeredEvent` hoặc một cơ chế gọi API tương đương): Chứa `TensionID`, `TensionType`, ngữ cảnh liên quan, và có thể gợi ý `SolutionPattern` hoặc các ràng buộc.
                    *   Kích hoạt trực tiếp dựa trên quy tắc (ít phổ biến hơn, có thể cho các `Tension` đơn giản, lặp lại).
                * **TRM Ontology**:
                    *   Thông tin chi tiết về `Tension` cần giải quyết (`TensionID`, `Severity`, `Status`, `RelatedEntities` như `Project`, `Task`, `Person`, `Resource`).
                    *   Danh sách các `SolutionPattern` có sẵn và tiêu chí áp dụng của chúng.
                    *   Lịch sử các `Tension` tương tự và các giải pháp đã được áp dụng (`PastResolutionRecord`).
                    *   Thông tin về trạng thái hiện tại của các thực thể liên quan (ví dụ: lịch trình của `Person`, mức độ sử dụng của `Resource`).
                * **Quyền Hạn (Permissions)**: Xác định mức độ tự động hóa mà Agent có thể thực hiện (ví dụ: có thể tự động điều chỉnh lịch task hay chỉ đề xuất).
                * **Phản hồi từ Founder/User** (nếu một giải pháp cần phê duyệt, thường được trung chuyển qua `ResolutionCoordinatorAgent` và `UserInterfaceAgent`): Xác nhận hoặc từ chối một đề xuất giải pháp.

            * **10.2.8.3. Các Hành động Chính (Key Actions)**
                * **Tiếp nhận và Xác thực Yêu cầu (Request Reception and Validation)**:
                    *   Nhận yêu cầu giải quyết `Tension`.
                    *   Xác thực `TensionID` và các thông tin đầu vào.
                * **Phân tích Chi tiết `Tension` (Detailed Tension Analysis)**:
                    *   Truy vấn TRM Ontology để thu thập toàn bộ ngữ cảnh của `Tension`.
                    *   Phân tích nguyên nhân gốc rễ (nếu có thể) và các yếu tố ảnh hưởng.
                * **Lựa chọn/Xây dựng Giải pháp (Solution Selection/Formulation)**:
                    *   Nếu `SolutionPattern` được gợi ý: Đánh giá tính phù hợp của pattern đó với `Tension` hiện tại.
                    *   Nếu không có gợi ý: Tìm kiếm các `SolutionPattern` phù hợp trong Ontology dựa trên `TensionType`, `Severity`, và ngữ cảnh.
                    *   Nếu không có pattern phù hợp: Cố gắng xây dựng một giải pháp tùy chỉnh dựa trên các quy tắc logic hoặc mô hình học máy (nếu có).
                    *   Ví dụ các giải pháp: điều chỉnh lịch trình task, đề xuất phân công lại task, yêu cầu thêm thông tin, cảnh báo về xung đột tài nguyên.
                * **Đánh giá Tác động của Giải pháp Đề xuất (Impact Assessment of Proposed Solution)**:
                    *   Ước tính các tác động tiềm ẩn của giải pháp đề xuất lên các `Project`, `Task`, `Person` khác.
                    *   Kiểm tra xem giải pháp có vi phạm ràng buộc nào không.
                * **Thực thi Giải pháp (Solution Execution) / Đề xuất Giải pháp (Solution Proposal)**:
                    * **Nếu Agent có quyền tự động thực thi và giải pháp được đánh giá là an toàn**:
                        *   Thực hiện các thay đổi cần thiết trong TRM Ontology (ví dụ: cập nhật `Task.ScheduledStartDate`, `Task.AssignedTo`).
                        *   Phát các sự kiện thông báo về thay đổi (ví dụ: `TaskRescheduledEvent`).
                    * **Nếu Agent không có quyền tự động hoặc giải pháp cần phê duyệt**:
                        *   Chuẩn bị một hoặc nhiều đề xuất giải pháp chi tiết.
                        *   Gửi các đề xuất này cho `ResolutionCoordinatorAgent` (thường qua `ProposedSolutionAvailableEvent` hoặc phản hồi API), để Agent này có thể trình bày cho Founder/User qua `UserInterfaceAgent`.
                * **Theo dõi và Cập nhật Trạng thái (Monitoring and Status Update)**:
                    *   Nếu giải pháp được thực thi, theo dõi các chỉ số liên quan để xem `Tension` có giảm bớt hay không.
                    *   Cập nhật trạng thái của `Tension` trong Ontology (ví dụ: `ResolutionInProgress`, `PendingApproval`).
                * **Báo cáo Kết quả (Result Reporting)**:
                    *   Sau khi thực thi hoặc nhận được phản hồi phê duyệt/từ chối:
                        *   Nếu `Tension` được giải quyết: Cập nhật trạng thái thành `Resolved`. Phát `TensionResolvedByAgentEvent`.
                        *   Nếu giải pháp thất bại hoặc bị từ chối: Cập nhật trạng thái (ví dụ: `ResolutionFailed`, `EscalationRequired`). Phát `TensionResolutionAttemptFailedEvent`.
                        *   Gửi báo cáo chi tiết cho `ResolutionCoordinatorAgent`.
                * **Ghi Log (Logging)**: Ghi lại tất cả các bước phân tích, lựa chọn giải pháp, thực thi và kết quả.

            * **10.2.8.4. Dữ liệu Đầu ra / Sự kiện Tạo ra (Output Data / Generated Events)**
                * **Dữ liệu**:
                    *   Cập nhật trạng thái cho `Tension` trong TRM Ontology.
                    *   Đề xuất giải pháp chi tiết (nếu không tự động thực thi).
                    *   Log về quá trình xử lý.
                * **Sự kiện (Events)**:
                    * ` ProposedSolutionAvailableEvent`: Gửi đến `ResolutionCoordinatorAgent` khi có một hoặc nhiều giải pháp được đề xuất.
                    * ` TensionResolutionAttemptedEvent`: Thông báo một nỗ lực giải quyết đã được thực hiện.
                    * ` TensionResolvedByAgentEvent`: Thông báo `Tension` đã được Agent giải quyết thành công (sau khi thực thi).
                    * ` TensionResolutionAttemptFailedEvent`: Thông báo nỗ lực giải quyết `Tension` không thành công hoặc giải pháp bị từ chối.
                    *   Các sự kiện cụ thể liên quan đến thay đổi dữ liệu (ví dụ: `TaskRescheduledEvent`, `ResourceReallocatedEvent`) nếu Agent thực hiện thay đổi.

            * **10.2.8.5. Tương tác với các Thành phần Khác (Interaction with Other Components)**
                * **`ResolutionCoordinatorAgent`**: Nhận yêu cầu giải quyết `Tension`. Gửi lại các đề xuất giải pháp, báo cáo kết quả, và các sự kiện về tiến trình.
                * **TRM Ontology / Knowledge Base**: Đọc thông tin chi tiết về `Tension`, `SolutionPattern`, lịch sử giải quyết. Ghi lại các thay đổi trạng thái, các giải pháp được áp dụng.
                * **`ProjectManagementAgent`** (có thể gián tiếp qua `ResolutionCoordinatorAgent` hoặc trực tiếp nếu có quyền): Thực hiện các thay đổi liên quan đến `Project` và `Task` (ví dụ: cập nhật lịch, phân công).
                * **`UserInterfaceAgent`** (thông qua `ResolutionCoordinatorAgent`): Các đề xuất giải pháp có thể được hiển thị cho người dùng thông qua Agent này.
                * **`SystemEventBus`**: Lắng nghe các yêu cầu (ví dụ: từ `ResolutionCoordinatorAgent`), phát các sự kiện về tiến trình và kết quả giải quyết `Tension`.
                * **`AgentManager`**: Báo cáo trạng thái, log hoạt động.

            * **10.2.8.6. Ví dụ Cụ thể (Specific Example)**
                * **Bối cảnh**: `ResolutionCoordinatorAgent` đã xác định một `Tension` "TaskDependencyConflict" (Task A phải hoàn thành trước Task B, nhưng Task B lại được lên lịch bắt đầu trước Task A). `ResolutionCoordinatorAgent` gửi yêu cầu giải quyết `Tension` này đến `TensionResolutionAgent`, gợi ý `SolutionPattern` là "AdjustTaskSchedule".
                * **Hoạt động của `TensionResolutionAgent`**:
                    1.  **Tiếp nhận và Xác thực**: Nhận yêu cầu, xác thực `TensionID`.
                    2.  **Phân tích Chi tiết**: Truy vấn Ontology, lấy thông tin `ScheduledStartDate`, `ScheduledEndDate`, `Dependencies` của Task A và Task B. Xác nhận xung đột.
                    3.  **Lựa chọn/Xây dựng Giải pháp**:
                        *   Đánh giá `SolutionPattern` "AdjustTaskSchedule".
                        *   Xác định rằng cần dời `ScheduledStartDate` của Task B sau `ScheduledEndDate` của Task A. Tính toán ngày bắt đầu mới cho Task B.
                    4.  **Đánh giá Tác động**: Kiểm tra xem việc dời Task B có ảnh hưởng đến các task phụ thuộc vào Task B hoặc deadline của dự án không. Giả sử trong trường hợp này, tác động là chấp nhận được.
                    5.  **Thực thi Giải pháp (Giả sử Agent có quyền)**:
                        *   Cập nhật `TaskB.ScheduledStartDate` trong TRM Ontology.
                        *   Phát `TaskRescheduledEvent` (cho Task B).
                    6.  **Báo cáo Kết quả**:
                        *   Cập nhật trạng thái `Tension` "TaskDependencyConflict" thành `Resolved`.
                        *   Phát `TensionResolvedByAgentEvent`.
                        *   Gửi báo cáo cho `ResolutionCoordinatorAgent` rằng `Tension` đã được giải quyết bằng cách điều chỉnh lịch Task B.

        * **10.2.9. `ProposalGenerationAgent` (Agent Tạo Đề xuất)**
            * **10.2.9.1. Mục tiêu (Objective)**
                *   Tự động hoặc bán tự động tạo ra các `Proposal` (Đề xuất) có cấu trúc tốt, dựa trên dữ liệu, nhằm đáp ứng các nhu cầu, cơ hội hoặc vấn đề cụ thể được xác định trong hệ thống TRM hoặc bởi Founder.
                *   Đảm bảo các đề xuất được tạo ra phù hợp với các mục tiêu chiến lược (`StrategicGoal`) của TRM, tuân thủ TRM Ontology, và được trình bày một cách rõ ràng, thuyết phục.
                *   Hỗ trợ Founder và các Agent khác trong việc hình thành các kế hoạch hành động, dự án mới, hoặc giải pháp cho các vấn đề.

            * **10.2.9.2. Dữ liệu Đầu vào (Input Data)**
                * **Yêu cầu Tạo Đề xuất (Proposal Request)**:
                    * ` ProposalRequestEvent` (từ Founder qua `UserInterfaceAgent`, hoặc từ các Agent khác như `StrategicAlignmentAgent`, `OpportunityIdentificationAgent`, `ResolutionCoordinatorAgent`).
                    *   Yêu cầu có thể bao gồm: `ProposalType` (ví dụ: `NewProjectProposal`, `IssueSolutionProposal`, `StrategicInitiativeProposal`), chủ đề, mục tiêu chính, các ràng buộc ban đầu.
                * **TRM Ontology**:
                    *   Thông tin về `StrategicGoal`, `Objective`, `Problem`, `Opportunity`, `Tension`, `Risk`.
                    *   Dữ liệu về `Project` hiện tại, `Resource` có sẵn, `KnowledgeItem` liên quan.
                    *   Các `ProposalTemplate` (Mẫu Đề xuất) cho các loại đề xuất khác nhau.
                    *   Lịch sử các `Proposal` đã được tạo và kết quả của chúng (`PastProposalRecord`).
                * **Dữ liệu Bên ngoài (External Data)** (nếu có và được tích hợp): Dữ liệu nghiên cứu thị trường, phân tích đối thủ cạnh tranh, xu hướng công nghệ.
                * **Tiêu chí Người dùng (User-defined Criteria)**: Các ràng buộc, ưu tiên cụ thể do người dùng cung cấp cho đề xuất.
                * **Phản hồi về Đề xuất Trước đó (Feedback on Previous Proposals)**: Dữ liệu học hỏi để cải thiện chất lượng đề xuất.

            * **10.2.9.3. Các Hành động Chính (Key Actions)**
                * **Tiếp nhận và Phân tích Yêu cầu (Request Reception and Analysis)**:
                    *   Thu nhận `ProposalRequestEvent` hoặc các tín hiệu yêu cầu khác.
                    *   Làm rõ mục tiêu cốt lõi, phạm vi, và các ràng buộc của đề xuất cần tạo.
                * **Thu thập Thông tin (Information Gathering)**:
                    *   Truy vấn TRM Ontology để lấy dữ liệu liên quan đến chủ đề đề xuất (ví dụ: `StrategicGoal` liên quan, `Problem` cần giải quyết, `KnowledgeItem` hỗ trợ).
                    *   Truy cập các nguồn dữ liệu bên ngoài (nếu cần và có khả năng).
                * **Xác định và Đánh giá Lựa chọn (Option Generation and Evaluation)**:
                    *   Nếu đề xuất là một giải pháp: Xác định các phương án giải quyết tiềm năng.
                    *   Nếu là một dự án mới: Phác thảo các hướng tiếp cận hoặc phạm vi dự án khả thi.
                    *   Đánh giá các lựa chọn dựa trên các tiêu chí như: tính khả thi, chi phí, lợi ích, rủi ro, mức độ phù hợp với chiến lược.
                * **Lựa chọn Mẫu Đề xuất (Proposal Template Selection)**:
                    *   Chọn một `ProposalTemplate` phù hợp dựa trên `ProposalType`.
                * **Cấu trúc và Soạn thảo Đề xuất (Proposal Structuring and Drafting)**:
                    *   Điền thông tin vào các mục của `ProposalTemplate`, ví dụ:
                        *   Tóm tắt Vấn đề / Cơ hội (Problem Statement / Opportunity).
                        *   Giải pháp / Kế hoạch Hành động Đề xuất (Proposed Solution / Action Plan).
                        *   Mục tiêu / Kết quả Dự kiến (Objectives / Expected Outcomes).
                        *   Yêu cầu Nguồn lực (Resource Requirements: thời gian, ngân sách, nhân sự).
                        *   Đánh giá Rủi ro và Kế hoạch Giảm thiểu (Risk Assessment & Mitigation Plan).
                        *   Chỉ số Đo lường Hiệu suất Chính (Key Performance Indicators - KPIs).
                    *   Sử dụng khả năng của mô hình ngôn ngữ lớn (LLM) để tạo ra nội dung văn bản mạch lạc, chuyên nghiệp và thuyết phục.
                * **Xác thực và Tinh chỉnh Nội bộ (Internal Validation and Refinement)**:
                    *   Kiểm tra tính đầy đủ, nhất quán của đề xuất.
                    *   Đảm bảo sự phù hợp với TRM Ontology và các quy tắc nghiệp vụ.
                    *   Có thể thực hiện các vòng lặp tinh chỉnh dựa trên các quy tắc kiểm tra nội bộ.
                * **Tạo Đối tượng Đề xuất (Proposal Object Creation)**:
                    *   Lưu trữ đề xuất đã hoàn thiện dưới dạng một thực thể `Proposal` trong TRM Ontology, bao gồm tất cả các chi tiết và siêu dữ liệu liên quan.
                * **Trình Đề xuất (Proposal Submission)**:
                    *   Thông báo cho bên yêu cầu (ví dụ: Founder qua `UserInterfaceAgent`) rằng đề xuất đã sẵn sàng để xem xét.
                    *   Phát `ProposalGeneratedEvent`.

            * **10.2.9.4. Dữ liệu Đầu ra / Sự kiện Tạo ra (Output Data / Generated Events)**
                * **Dữ liệu**:
                    *   Một thực thể `Proposal` mới được tạo và lưu trong TRM Ontology. Thực thể này chứa toàn bộ nội dung và cấu trúc của đề xuất.
                * **Sự kiện (Events)**:
                    * ` ProposalGeneratedEvent`: Thông báo một `Proposal` mới đã được tạo, chứa `ProposalID` và các thông tin tóm tắt.
                    * ` ProposalSubmittedEvent`: Thông báo `Proposal` đã được gửi đến người/bộ phận có trách nhiệm xem xét.
                    * ` InformationRequiredForProposalEvent`: Nếu Agent cần thêm thông tin để hoàn thành đề xuất, nó có thể phát sự kiện này.

            * **10.2.9.5. Tương tác với các Thành phần Khác (Interaction with Other Components)**
                * **`UserInterfaceAgent`**: Nhận yêu cầu tạo đề xuất từ Founder. Trình bày các `Proposal` đã tạo cho Founder để xem xét, chỉnh sửa và phê duyệt. Nhận phản hồi về `Proposal`.
                * **TRM Ontology / Knowledge Base**: Nguồn thông tin chính để thu thập dữ liệu và là nơi lưu trữ các `Proposal` được tạo ra. Truy cập `ProposalTemplate`.
                * **`KnowledgeIngestionAgent`, `KnowledgeValidationAgent`**: Cung cấp kiến thức nền tảng và dữ liệu đã được xác thực để làm giàu nội dung đề xuất.
                * **`ProjectManagementAgent`**: Có thể là người yêu cầu tạo đề xuất cho các giai đoạn tiếp theo của dự án, hoặc nhận các `NewProjectProposal` để bắt đầu quy trình quản lý dự án mới.
                * **`StrategicAlignmentAgent`**: Đảm bảo các đề xuất (đặc biệt là `StrategicInitiativeProposal`) phù hợp với `StrategicGoal` của TRM. Có thể là người yêu cầu tạo đề xuất.
                * **`ResolutionCoordinatorAgent`**: Có thể yêu cầu tạo `IssueSolutionProposal` như một phần của quá trình giải quyết `Issue` hoặc `Tension`.
                * **`SystemEventBus`**: Phát và nhận các sự kiện liên quan đến quy trình tạo và trình duyệt đề xuất.
                * **Founder/Người dùng**: Người khởi tạo yêu cầu, xem xét, cung cấp phản hồi và phê duyệt các đề xuất.

            * **10.2.9.6. Ví dụ Cụ thể (Specific Example)**
                * **Bối cảnh**: `StrategicAlignmentAgent` phát hiện một `StrategicGoal` ("Mở rộng sang thị trường giáo dục trực tuyến") chưa có dự án cụ thể nào để thực hiện. Agent này phát một `ProposalRequestEvent` đến `ProposalGenerationAgent` yêu cầu tạo một `NewProjectProposal`.
                * **Hoạt động của `ProposalGenerationAgent`**:
                    1.  **Tiếp nhận và Phân tích**: Nhận `ProposalRequestEvent`. Xác định yêu cầu là tạo `NewProjectProposal` liên quan đến `StrategicGoal` "Mở rộng sang thị trường giáo dục trực tuyến".
                    2.  **Thu thập Thông tin**:
                        *   Truy vấn Ontology về `StrategicGoal` đó, các `KnowledgeItem` liên quan đến "giáo dục trực tuyến", các `Resource` (nhân sự, công nghệ) hiện có của TRM.
                        *   (Giả sử) Truy cập một nguồn dữ liệu bên ngoài về xu hướng thị trường e-learning.
                    3.  **Xác định Lựa chọn**: Phác thảo 2-3 ý tưởng dự án tiềm năng (ví dụ: "Nền tảng học tập tương tác cho doanh nghiệp", "Ứng dụng di động luyện thi AI", "Hệ thống quản lý khóa học thông minh"). Đánh giá sơ bộ. Chọn "Nền tảng học tập tương tác cho doanh nghiệp" là hứa hẹn nhất.
                    4.  **Lựa chọn Mẫu**: Chọn `NewProjectProposalTemplate` từ Ontology.
                    5.  **Cấu trúc và Soạn thảo**:
                        * **Tên Dự án Đề xuất**: "TRM Interactive Learning Platform (TRM-ILP)".
                        * **Mục tiêu Dự án**: Phát triển và ra mắt phiên bản MVP trong 9 tháng, thu hút 5 khách hàng doanh nghiệp đầu tiên.
                        * **Phạm vi**: Xây dựng các module cốt lõi (quản lý nội dung, lớp học ảo, theo dõi tiến độ), tích hợp AI cho cá nhân hóa lộ trình học.
                        * **Nguồn lực**: Team 3 developers, 1 UX designer, 1 Product Manager. Ngân sách $X.
                        * **Rủi ro**: Cạnh tranh cao, thách thức trong việc tạo nội dung hấp dẫn.
                    6.  **Xác thực Nội bộ**: Kiểm tra tính logic, đầy đủ.
                    7.  **Tạo Đối tượng**: Lưu `Proposal` "TRM-ILP" vào Ontology.
                    8.  **Trình Đề xuất**: Phát `ProposalGeneratedEvent` và `ProposalSubmittedEvent`. Thông báo cho `UserInterfaceAgent` để Founder có thể xem xét đề xuất "TRM-ILP".

        * **10.2.10. `LearningAndOptimizationAgent` (Agent Học hỏi và Tối ưu hóa)**
            * **10.2.10.1. Mục tiêu (Objective)**
                *   Liên tục cải thiện hiệu suất tổng thể của hệ thống TRM, hiệu quả của các AI Agent, và chất lượng của các quy trình vận hành (ví dụ: giải quyết `Tension`, tạo `Proposal`).
                *   Tự động xác định các mẫu hình (patterns), điểm nghẽn (bottlenecks), và các cơ hội tối ưu hóa dựa trên phân tích dữ liệu lịch sử và phản hồi.
                *   Đề xuất hoặc tự động (nếu được phép) triển khai các thay đổi để nâng cao kiến thức hệ thống (TRM Ontology), logic của Agent, và các chiến lược hoạt động.
                *   Đảm bảo hệ thống TRM có khả năng thích ứng và học hỏi từ kinh nghiệm để ngày càng trở nên thông minh và hiệu quả hơn.

            * **10.2.10.2. Dữ liệu Đầu vào (Input Data)**
                * **Dữ liệu Hiệu suất Agent (Agent Performance Data)**:
                    *   Log hoạt động, thời gian xử lý, tỷ lệ thành công/thất bại của các hành động từ tất cả các Agent (`AgentActivityLog`, `AgentPerformanceMetrics`).
                * **Kết quả Quy trình (Process Outcomes)**:
                    *   Dữ liệu về kết quả của các `Proposal` (được chấp thuận, từ chối, hiệu quả thực tế).
                    *   Dữ liệu về kết quả của các `TensionResolutionAttempt` (thành công, thất bại, thời gian giải quyết, tài nguyên sử dụng).
                    *   Kết quả của các `Project` và `Task` (hoàn thành, trễ hạn, chất lượng).
                * **Phản hồi Người dùng (User Feedback)**:
                    *   Phản hồi trực tiếp từ Founder/người dùng qua `UserInterfaceAgent` (ví dụ: đánh giá về `Proposal`, mức độ hài lòng với giải pháp).
                    *   Phản hồi gián tiếp (ví dụ: tần suất người dùng phải can thiệp thủ công, các chỉnh sửa người dùng thực hiện trên kết quả của Agent).
                * **Dữ liệu TRM Ontology**:
                    *   Cấu trúc hiện tại của Ontology, bao gồm `SolutionPattern`, `ProposalTemplate`, `Rule`, `Constraint`.
                    *   Tần suất truy cập và sử dụng các `KnowledgeItem`.
                * **Sự kiện Hệ thống (System Events)**:
                    *   Các sự kiện lỗi (`ErrorEvent`), cảnh báo (`WarningEvent`), các sự kiện chỉ ra sự bất thường.
                * **Mục tiêu Chiến lược và KPI Hệ thống (Strategic Goals and System KPIs)**: Để đánh giá mức độ đóng góp của các tối ưu hóa vào mục tiêu lớn hơn.

            * **10.2.10.3. Các Hành động Chính (Key Actions)**
                * **Thu thập và Tổng hợp Dữ liệu (Data Collection and Aggregation)**:
                    *   Liên tục thu thập và lưu trữ dữ liệu đầu vào từ các nguồn khác nhau.
                * **Phân tích Hiệu suất (Performance Analysis)**:
                    *   Phân tích hiệu quả của từng Agent, xác định Agent hoạt động kém hoặc quy trình tốn nhiều tài nguyên.
                    *   Đánh giá tỷ lệ thành công của các `SolutionPattern` và `ProposalTemplate`.
                * **Phân tích Phản hồi (Feedback Analysis)**:
                    *   Xử lý và phân loại phản hồi của người dùng để xác định các điểm cần cải thiện.
                * **Nhận diện Mẫu hình và Phân tích Nguyên nhân Gốc rễ (Pattern Recognition and Root Cause Analysis)**:
                    *   Sử dụng các kỹ thuật học máy (machine learning) hoặc thống kê để tìm ra các mẫu hình trong dữ liệu (ví dụ: loại `Tension` nào thường xuyên không được giải quyết tự động).
                    *   Điều tra nguyên nhân gốc rễ của các vấn đề về hiệu suất hoặc các phản hồi tiêu cực.
                * **Xây dựng Chiến lược Tối ưu hóa (Optimization Strategy Formulation)**:
                    *   Đề xuất các thay đổi cho logic của Agent (ví dụ: cập nhật thuật toán lựa chọn giải pháp trong `TensionResolutionAgent`).
                    *   Đề xuất tạo mới hoặc cập nhật `SolutionPattern`, `ProposalTemplate`, `Rule`, `Constraint` trong TRM Ontology.
                    *   Đề xuất các `KnowledgeItem` mới cần được thu thập.
                * **Đề xuất Cập nhật Knowledge Base (Knowledge Base Update Recommendation)**:
                    *   Tạo ra các `OntologyUpdateRequestSuggestionEvent` hoặc `KnowledgeItemSuggestionEvent`.
                * **Thử nghiệm A/B hoặc Mô phỏng (A/B Testing or Simulation - Advanced)**:
                    *   Nếu có khả năng, thử nghiệm các thay đổi được đề xuất trong một môi trường được kiểm soát trước khi áp dụng rộng rãi.
                * **Theo dõi và Đánh giá Tác động (Impact Monitoring and Evaluation)**:
                    *   Sau khi một tối ưu hóa được triển khai, theo dõi tác động của nó lên hiệu suất hệ thống và các KPI liên quan.
                * **Báo cáo và Cảnh báo (Reporting and Alerting)**:
                    *   Tạo báo cáo định kỳ về hiệu suất hệ thống và các cơ hội tối ưu hóa.
                    *   Cảnh báo cho `AgentManager` hoặc Founder về các vấn đề hiệu suất nghiêm trọng hoặc các cơ hội cải tiến quan trọng.

            * **10.2.10.4. Dữ liệu Đầu ra / Sự kiện Tạo ra (Output Data / Generated Events)**
                * **Dữ liệu**:
                    *   Báo cáo Phân tích Hiệu suất (`PerformanceAnalysisReport`).
                    *   Đề xuất Tối ưu hóa (`OptimizationProposal`).
                    *   Bảng điều khiển Hiệu suất (Performance Dashboards - hiển thị qua `UserInterfaceAgent`).
                * **Sự kiện (Events)**:
                    * ` OntologyUpdateRequestSuggestionEvent`: Đề xuất thay đổi cho TRM Ontology.
                    * ` AgentLogicUpdateSuggestionEvent`: Đề xuất thay đổi logic cho một Agent cụ thể.
                    * ` NewSolutionPatternSuggestionEvent`: Đề xuất một `SolutionPattern` mới.
                    * ` NewKnowledgeItemSuggestionEvent`: Đề xuất thu thập một `KnowledgeItem` mới.
                    * ` SystemOptimizationAlertEvent`: Cảnh báo về một vấn đề hoặc cơ hội tối ưu hóa.
                    * ` LearningCycleCompletedEvent`: Thông báo hoàn thành một chu kỳ học hỏi và phân tích.

            * **10.2.10.5. Tương tác với các Thành phần Khác (Interaction with Other Components)**
                * **Tất cả các AI Agent khác**: Thu thập dữ liệu log và hiệu suất. Các Agent này cũng có thể là đối tượng của các đề xuất tối ưu hóa.
                * **`AgentManager`**: Nhận các đề xuất tối ưu hóa liên quan đến logic hoặc cấu hình Agent. Có thể kích hoạt việc cập nhật Agent dựa trên đề xuất.
                * **`UserInterfaceAgent`**: Trình bày báo cáo, bảng điều khiển và các đề xuất tối ưu hóa cho Founder. Thu thập phản hồi trực tiếp từ Founder.
                * **TRM Ontology / Knowledge Base**: Là đối tượng của các đề xuất cập nhật (ví dụ: `SolutionPattern`, `Rule`). Cũng là nguồn dữ liệu để phân tích (ví dụ: mức độ sử dụng các `KnowledgeItem`).
                * **`KnowledgeIngestionAgent` / `KnowledgeValidationAgent`**: Có thể nhận yêu cầu thu thập hoặc xác thực `KnowledgeItem` mới dựa trên phân tích của `LearningAndOptimizationAgent`.
                * **`SystemEventBus`**: Kênh giao tiếp chính để thu thập dữ liệu sự kiện và phát các sự kiện đề xuất tối ưu hóa.
                * **Founder/Người dùng**: Xem xét các báo cáo và đề xuất tối ưu hóa. Phê duyệt các thay đổi quan trọng. Cung cấp phản hồi.

            * **10.2.10.6. Ví dụ Cụ thể (Specific Example)**
                * **Bối cảnh**: `LearningAndOptimizationAgent` phân tích dữ liệu từ `TensionResolutionAgent` trong 3 tháng qua. Nó phát hiện ra rằng 30% các `Tension` thuộc loại "TaskResourceOverallocation" không được giải quyết tự động và phải cần đến sự can thiệp của Founder, mặc dù có một `SolutionPattern` ("DefaultResourceReallocation") được thiết kế cho việc này.
                * **Hoạt động của `LearningAndOptimizationAgent`**:
                    1.  **Thu thập Dữ liệu**: Tập hợp log giải quyết `Tension` "TaskResourceOverallocation", phản hồi của Founder (nếu có), và chi tiết các lần can thiệp thủ công.
                    2.  **Phân tích Hiệu suất**: Xác nhận tỷ lệ thất bại cao của `SolutionPattern` "DefaultResourceReallocation" cho loại `Tension` này.
                    3.  **Phân tích Nguyên nhân Gốc rễ**: Phát hiện ra rằng `SolutionPattern` này không hiệu quả khi `Resource` bị quá tải là một `KeyResource` (Tài nguyên chủ chốt) có ít lựa chọn thay thế. Logic của pattern quá đơn giản.
                    4.  **Xây dựng Chiến lược Tối ưu hóa**:
                        *   Đề xuất cập nhật `SolutionPattern` "DefaultResourceReallocation" để bao gồm logic kiểm tra xem `Resource` có phải là `KeyResource` không.
                        *   Nếu là `KeyResource`, đề xuất một nhánh logic phức tạp hơn, có thể bao gồm việc đề xuất trì hoãn `Task` có độ ưu tiên thấp hơn hoặc thông báo cho Founder để xem xét.
                    5.  **Đề xuất Cập nhật**: Phát `OntologyUpdateRequestSuggestionEvent` với chi tiết về `SolutionPattern` được đề xuất cập nhật.
                    6.  **Báo cáo**: Thông báo cho `UserInterfaceAgent` để trình bày phát hiện và đề xuất cho Founder, kèm theo dữ liệu minh chứng về tỷ lệ thất bại hiện tại và lợi ích tiềm năng của việc cập nhật.
                    7.  **Theo dõi (Sau khi cập nhật được duyệt)**: Nếu Founder duyệt và `SolutionPattern` được cập nhật, Agent sẽ tiếp tục theo dõi hiệu suất giải quyết `Tension` "TaskResourceOverallocation" để xác nhận sự cải thiện.         
        * **10.2.11. `StrategicAlignmentAgent` (Agent Căn chỉnh Chiến lược)**
            * **Mục tiêu**: Đảm bảo mọi `ProjectProposal`, `Project`, `Task` và các sáng kiến quan trọng khác trong TRM-OS luôn được đánh giá, ưu tiên và thực thi theo hướng phù hợp và đóng góp tối đa cho việc đạt được các `StrategicGoal`, `Objective` và `KeyResult` đã được Founder định nghĩa trong TRM Ontology. Agent này đóng vai trò "người gác cổng chiến lược".
            * **Dữ liệu đầu vào**:
                * ` StrategicGoal`, `Objective`, `KeyResult` (từ TRM Ontology).
                * ` ProjectProposal` mới được tạo (từ Founder, các Agent khác, hoặc `ResolutionCoordinatorAgent`).
                * ` Project` và `Task` đang hoạt động hoặc được đề xuất.
                * ` Metric` liên quan đến tiến độ thực hiện `Objective` và `KeyResult`.
                * ` PolicyNode` và `GuidelineNode` liên quan đến việc triển khai chiến lược.
                * ` RiskNode` và `OpportunityNode` có thể ảnh hưởng đến chiến lược.
                * ` SystemEvent` liên quan đến việc tạo mới hoặc thay đổi trạng thái của các thực thể trên.
            * **Hoạt động chính**:
                1.  **Tiếp nhận và Phân tích Đề xuất/Dự án/Nhiệm vụ mới**:
                    *   Khi một `ProjectProposal`, `Project` hoặc `Task` quan trọng mới được tạo (thông qua `SystemEvent`), Agent sẽ phân tích nội dung, mục tiêu đề xuất của chúng.
                    *   Sử dụng LLM (qua `LLMInterfaceAgent`) để hiểu ngữ nghĩa và mục đích.
                2.  **Đánh giá Mức độ Phù hợp Chiến lược (Strategic Fit Assessment)**:
                    *   Đối chiếu mục tiêu của đề xuất/dự án/nhiệm vụ với các `StrategicGoal`, `Objective` và `KeyResult` hiện có trong TRM Ontology.
                    *   Xác định (các) `Objective` mà đề xuất này đóng góp vào.
                    *   Đánh giá mức độ đóng góp tiềm năng (cao, trung bình, thấp) và mức độ rủi ro chiến lược.
                    *   Sử dụng các `Metric` liên quan đến `Objective` để xem xét bối cảnh.
                3.  **Kiểm tra Xung đột và Tính Khả thi Chiến lược**:
                    *   Phát hiện các xung đột tiềm ẩn với các `Project` đang chạy hoặc các `StrategicGoal` khác.
                    *   Đánh giá sơ bộ về nguồn lực cần thiết và tính khả thi dựa trên các `Policy` và `Guideline` chiến lược.
                4.  **Gán Điểm Ưu tiên Chiến lược (Strategic Priority Scoring)**:
                    *   Dựa trên mức độ phù hợp, đóng góp tiềm năng, và rủi ro, Agent có thể đề xuất một điểm ưu tiên chiến lược.
                    *   Công thức hoặc tiêu chí tính điểm này được định nghĩa trong `Rule` của Ontology hoặc cấu hình của Agent.
                5.  **Tạo Báo cáo Đánh giá Chiến lược**:
                    *   Tạo một `StrategicAlignmentReportNode` liên kết với `ProjectProposal` hoặc `Project`.
                    *   Báo cáo này bao gồm: kết quả đánh giá phù hợp, `Objective` liên quan, điểm ưu tiên, các rủi ro/cơ hội chiến lược, và đề xuất (ví dụ: phê duyệt, yêu cầu làm rõ thêm, từ chối).
                6.  **Thông báo và Yêu cầu Phê duyệt**:
                    *   Phát `StrategicAlignmentAnalysisCompleteEvent` chứa ID của `StrategicAlignmentReportNode`.
                    *   Thông báo cho `UserInterfaceAgent` để trình bày báo cáo cho Founder hoặc `AGE` để ra quyết định.
                    *   Nếu có xung đột hoặc điểm ưu tiên thấp, cảnh báo rõ ràng.
                7.  **Theo dõi và Tái đánh giá Định kỳ**:
                    *   Đối với các `Project` lớn đang chạy, Agent có thể định kỳ (hoặc khi có `SignificantProjectEvent`) rà soát lại mức độ phù hợp chiến lược, đặc biệt nếu `StrategicGoal` có sự thay đổi.
                    *   Cảnh báo nếu một `Project` bắt đầu đi chệch hướng chiến lược.
                8.  **Hỗ trợ Phân tích Danh mục Chiến lược (Strategic Portfolio Analysis Support)**:
                    *   Cung cấp dữ liệu và phân tích tổng hợp về mức độ phù hợp chiến lược của toàn bộ danh mục `Project` và `ProjectProposal`.
                    *   Giúp Founder xác định các khoảng trống chiến lược hoặc các khu vực tập trung quá mức.
            * **Dữ liệu đầu ra và Sự kiện được tạo**:
                * ` StrategicAlignmentReportNode` được tạo và liên kết.
                * ` StrategicAlignmentAnalysisCompleteEvent`.
                * ` PotentialStrategicMisalignmentEvent` (nếu phát hiện nguy cơ chệch hướng).
                *   Cập nhật thuộc tính `strategicPriorityScore` hoặc `alignmentStatus` trên `ProjectProposalNode` hoặc `ProjectNode`.
            * **Tương tác với các Agent và Hệ thống khác**:
                * **`UserInterfaceAgent`**: Trình bày báo cáo đánh giá, cảnh báo và yêu cầu phê duyệt cho Founder.
                * **`TRM Ontology`**: Đọc `StrategicGoal`, `Objective`, `KeyResult`, `ProjectProposal`, `Project`, `Task`, `Metric`, `PolicyNode`, `RiskNode`, `OpportunityNode`. Tạo/cập nhật `StrategicAlignmentReportNode`, các thuộc tính trên `ProjectNode`/`ProjectProposalNode`.
                * **`LLMInterfaceAgent`**: Hỗ trợ phân tích ngữ nghĩa của các đề xuất.
                * **`ProjectManagementAgent`**: Nhận thông tin về các dự án đã được phê duyệt về mặt chiến lược để bắt đầu quản lý. Cung cấp dữ liệu dự án cho việc theo dõi.
                * **`ResolutionCoordinatorAgent`**: Có thể nhận `ProjectProposal` từ Agent này để đánh giá chiến lược.
                * **`LearningAndOptimizationAgent`**: Có thể sử dụng dữ liệu về hiệu quả căn chỉnh chiến lược để tối ưu hóa quy trình đánh giá hoặc các `Rule` liên quan.
                * **`SystemEventBus`**: Lắng nghe các `SystemEvent` liên quan đến tạo mới/thay đổi `ProjectProposal`, `Project`, `Task`. Phát các `Event` của riêng mình.
                * **Founder/`AGE`**: Nhận báo cáo và ra quyết định cuối cùng về việc phê duyệt chiến lược.
            * **Ví dụ Kịch bản**:
                1.  **Bối cảnh**: `ResolutionCoordinatorAgent` sau khi phân tích một `Tension` phức tạp, đã đề xuất tạo một `ProjectProposal` mới để phát triển một module chức năng mới cho TRM-OS. Một `ProjectProposalCreatedEvent` được phát.
                2.  **Tiếp nhận**: `StrategicAlignmentAgent` bắt được `ProjectProposalCreatedEvent`.
                3.  **Phân tích**: Agent đọc chi tiết `ProjectProposalNode` và các `StrategicGoal`, `Objective` hiện tại của TRM (ví dụ: "Mở rộng khả năng tự động hóa của hệ thống", "Nâng cao hiệu quả quản lý tri thức").
                4.  **Đánh giá**: Agent xác định rằng module mới này đóng góp trực tiếp vào `Objective` "Nâng cao hiệu quả quản lý tri thức" và gián tiếp vào "Mở rộng khả năng tự động hóa". Nó cũng kiểm tra xem có xung đột với các dự án khác không.
                5.  **Báo cáo**: Agent tạo một `StrategicAlignmentReportNode`, ghi nhận mức độ phù hợp cao, `Objective` liên quan, và đề xuất điểm ưu tiên "Cao".
                6.  **Thông báo**: Phát `StrategicAlignmentAnalysisCompleteEvent`. `UserInterfaceAgent` hiển thị báo cáo cho Founder.
                7.  **Quyết định**: Founder xem xét báo cáo và phê duyệt đề xuất về mặt chiến lược. `ProjectProposalNode` được cập nhật trạng thái.
                8.  **Chuyển giao**: `ProjectManagementAgent` có thể được thông báo để bắt đầu lập kế hoạch chi tiết cho dự án này.
            * **Công nghệ tiềm năng**: Python, Neo4j client, thư viện LLM (ví dụ: tích hợp qua API), các thuật toán phân tích quyết định đa tiêu chí (MCDA) nếu cần cơ chế scoring phức tạp.    10.3. Luồng Hoạt động và Tương tác giữa các Agent (Agent Communication & Collaboration)

        Hệ thống AI Agent của TRM-OS được thiết kế để hoạt động như một thể thống nhất, nơi các agent chuyên biệt cộng tác với nhau và được điều phối bởi Artificial Genesis Engine (AGE) để đạt được mục tiêu chung của tổ chức.

        **10.3.1. Nguyên tắc Giao tiếp và Phối hợp:**

        * **Dựa trên Ontology (Ontology-driven Communication):** Các agent giao tiếp chủ yếu thông qua việc đọc và ghi vào ontology (Neo4j Aura). Các `Event` đóng vai trò là tín hiệu và cơ chế kích hoạt chính. Ví dụ, `DataSensingAgent` tạo `SystemEvent` sau khi thu thập dữ liệu, `KnowledgeExtractionAgent` có thể được trigger bởi `SystemEvent` này để bắt đầu xử lý.
        * **Thông điệp Trực tiếp (Direct Messaging - Khi cần thiết):** Cung cấp một kênh giao tiếp nhanh chóng và có chủ đích cho các tương tác không phù hợp hoặc không hiệu quả nếu chỉ dựa hoàn toàn vào cơ chế `Event` của ontology. Đặc biệt hữu ích khi cần phản hồi gần như tức thời, truyền tải thông tin chỉ có tính tạm thời, hoặc thực hiện các lệnh điều khiển trực tiếp.
            * **Mục tiêu chính:**
                *   Đảm bảo tính linh hoạt và hiệu quả cho các tình huống cần giao tiếp đồng bộ hoặc bán đồng bộ giữa các agent hoặc giữa agent và AGE.
                *   Giảm tải cho ontology đối với các thông tin không cần lưu trữ lâu dài hoặc không mang tính sự kiện cần lan tỏa rộng trong toàn hệ thống.
            * **Các trường hợp sử dụng điển hình "Khi cần thiết":**
                * **Yêu cầu hành động khẩn cấp hoặc điều khiển trực tiếp:** AGE gửi lệnh cụ thể, có tính ưu tiên cao đến một agent (e.g., `AGE` -> `DataSensingAgent`: "Tạm dừng thu thập từ nguồn X trong 30 phút", `AGE` -> `KnowledgeExtractionAgent`: "Ưu tiên xử lý tài liệu Y ngay bây giờ với cấu hình Z").
                * **Truy vấn thông tin trạng thái tức thời:** Một agent yêu cầu thông tin trạng thái cụ thể từ AGE hoặc một agent khác mà thông tin này chưa được (hoặc không cần) phản ánh qua `Event` trong ontology (e.g., `ProjectManagementAgent` -> `AGE`: "Xác nhận agent `ResourceAllocationAgent` có đang hoạt động và sẵn sàng nhận yêu cầu không?").
                * **Báo cáo lỗi vận hành nghiêm trọng hoặc tình trạng sức khỏe (Health Checks):** Agent báo cáo lỗi vận hành cục bộ, không thể tự khắc phục, trực tiếp cho AGE để xử lý hoặc ghi nhận (e.g., `DataSensingAgent` -> `AGE`: "Lỗi nghiêm trọng: Không thể kết nối tới API nguồn Z sau 3 lần thử. Mã lỗi: 503"). AGE cũng có thể chủ động yêu cầu agent gửi thông tin health status định kỳ qua kênh này.
                * **Yêu cầu dịch vụ đồng bộ đơn giản, có tính chất nội bộ:** Agent A cần một xử lý nhỏ, nhanh từ Agent B và đợi kết quả trực tiếp, không cần tạo `Event` phức tạp (e.g., `TensionResolutionAgent` -> `KnowledgeExtractionAgent` (qua API nội bộ): "Trích xuất nhanh các danh từ riêng (Named Entities) từ đoạn văn bản sau: '...' và trả về danh sách").
                * **Điều phối tác vụ con không qua Event:** AGE giao một tác vụ con cụ thể, không cần tạo `Event` phức tạp trong ontology, cho một agent và chờ xác nhận hoàn thành hoặc kết quả sơ bộ.
            * **Phương thức triển khai "API nội bộ" (Ưu tiên sự đơn giản, phù hợp với việc phát triển bằng CursorAI/WindsurfAI):**
                * **Direct Method Calls (Gọi hàm/phương thức trực tiếp):** Nếu các agent được thiết kế như các module, class trong cùng một ứng dụng hoặc process lớn do AGE quản lý, đây là phương pháp ưu tiên hàng đầu vì tính đơn giản, hiệu năng cao và dễ dàng cho AI (như CursorAI) hỗ trợ tạo mã. AGE hoặc các agent khác có thể gọi trực tiếp các public method của nhau.
                * **Lightweight HTTP/REST APIs nội bộ:** Nếu các agent cần được triển khai như các service riêng biệt (ví dụ, để quản lý tài nguyên độc lập, sử dụng công nghệ khác nhau, hoặc để dễ dàng mở rộng từng agent), có thể sử dụng các API HTTP/REST đơn giản.
                    *   Các agent sẽ expose các endpoint được định nghĩa rõ ràng cho các hành động cụ thể (e.g., `POST /control/{agent_id}/stop_task`, `GET /status/{agent_id}/health`, `POST /service/{agent_id}/process_data`).
                    *   Sử dụng các framework Python nhẹ như FastAPI hoặc Flask để xây dựng các API này, điều mà CursorAI có thể hỗ trợ hiệu quả.
                    *   Giao tiếp nên được bảo vệ trong mạng nội bộ. Cân nhắc sử dụng API key đơn giản cho xác thực giữa các service nếu cần thiết.
                * **Lưu ý:** Tránh sử dụng các message bus phức tạp (như Kafka, RabbitMQ) cho mục đích giao tiếp trực tiếp này ở giai đoạn đầu, trừ khi có yêu cầu rất rõ ràng về khả năng chịu lỗi cao và xử lý hàng đợi quy mô lớn cho các thông điệp này. Cơ chế Pub/Sub qua `Event` của ontology đã đáp ứng phần lớn nhu cầu giao tiếp bất đồng bộ.
            * **Định dạng thông điệp (cho API hoặc tham số method call):**
                *   Sử dụng JSON cho payload của các API request/response hoặc làm cấu trúc cho các tham số phức tạp của method call.
                *   Thông điệp nên bao gồm các trường cơ bản như: `request_id` (để theo dõi và tránh trùng lặp nếu cần), `source_agent_id`, `target_agent_id` (hoặc `target_service_endpoint`), `action_name`, `timestamp`, và `payload` (dữ liệu cụ thể cho hành động, ví dụ: `{ "task_id": "123", "parameters": { ... } }`).
            * **Xử lý phản hồi và lỗi:**
                *   Các yêu cầu trực tiếp (đặc biệt là dạng đồng bộ) cần có cơ chế phản hồi rõ ràng (e.g., HTTP status codes và JSON response body cho API; hoặc giá trị trả về và exceptions cho method calls) để xác nhận việc nhận, trạng thái xử lý, kết quả hoặc lỗi.
                *   Định nghĩa một bộ mã lỗi chuẩn hóa và thông điệp lỗi có ý nghĩa cho các API nội bộ để các agent có thể xử lý một cách nhất quán.
        * **Điều phối bởi AGE:** AGE giám sát trạng thái chung của hệ thống, quản lý vòng đời của các agent chuyên biệt, phân công nhiệm vụ phức tạp, và giải quyết xung đột (nếu có). AGE có thể trực tiếp ra lệnh cho các agent hoặc điều chỉnh ưu tiên của chúng.
        * **Cơ chế Đăng ký và Thông báo (Pub/Sub) dựa trên Ontology:** Các agent chủ động theo dõi hoặc được AGE thông báo về các `Event` và thay đổi trạng thái cụ thể trong ontology mà chúng quan tâm. Điều này cho phép phản ứng linh hoạt với các diễn biến trong hệ thống.
    *   **Phương thức hoạt động:**
        * **Theo dõi chủ động (Agent-initiated Polling):** Các agent có thể định kỳ truy vấn ontology (Neo4j) để tìm các `Event` mới hoặc các thay đổi trên các node/relationship mà chúng đã "đăng ký" quan tâm (ví dụ: `Event` có type cụ thể, `Task` được gán cho agent đó có status thay đổi). Tần suất polling được cấu hình để cân bằng giữa độ trễ và tải hệ thống.
        * **Thông báo qua AGE (AGE-mediated Notification):** AGE, với vai trò giám sát toàn cục, có thể phát hiện các `Event` hoặc thay đổi quan trọng và chủ động thông báo cho các agent liên quan. Thông báo này có thể được thực hiện qua kênh "Thông điệp Trực tiếp" (API nội bộ/method call) đã mô tả ở trên, gửi một thông điệp ngắn gọn chỉ định `Event ID` hoặc `Node ID` cần chú ý.
        * **Sử dụng `Label` và `Property` trong Ontology để "Đăng ký":** Việc "đăng ký" của một agent đối với một loại thông tin có thể được biểu diễn trong ontology. Ví dụ, một node đại diện cho agent có thể có một relationship `INTERESTED_IN` trỏ đến một `EventTypeNode` hoặc một `NodeLabel`. AGE hoặc chính agent đó có thể sử dụng thông tin này để lọc `Event`.
    *   **Ưu điểm:**
        *   Tận dụng ontology làm trung tâm thông tin, đảm bảo tính nhất quán.
        *   Kết hợp giữa polling (đơn giản, dễ triển khai) và thông báo chủ động từ AGE (giảm độ trễ cho các event quan trọng).
        *   Phù hợp với việc phát triển bằng CursorAI/WindsurfAI, vì logic truy vấn ontology và gọi API/method đơn giản có thể được AI hỗ trợ tạo.
    *   **Lưu ý:** Tránh triển khai một hệ thống message broker riêng biệt cho Pub/Sub này nếu ontology và AGE có thể đáp ứng nhu cầu, nhằm giữ sự đơn giản.

        **10.3.2. Các Kịch bản Tương tác Điển hình:**

        * **Kịch bản 1: Từ Dữ liệu thô đến Tri thức trong Ontology (Tích hợp Pub/Sub):**
            1.  **Thu thập Dữ liệu và Tạo `Event` (Publication):** `DataSensingAgent` thu thập dữ liệu mới (e.g., một tài liệu Google Docs) và tạo một `RawDataNode` (chứa link hoặc nội dung thô) trong ontology. Đồng thời, nó "publish" một `SystemEvent(type="NewDocumentDetected", raw_data_id={ID})` vào ontology.
            2.  **`KnowledgeExtractionAgent` Nhận Thông báo (Subscription & Notification):**
                * ` KnowledgeExtractionAgent` đã "đăng ký" (`INTERESTED_IN` relationship trong ontology) với các `SystemEvent` loại `NewDocumentDetected`.
                *   AGE, thông qua cơ chế "Thông báo qua AGE" (AGE-mediated Notification) của Pub/Sub, phát hiện `SystemEvent` mới và gửi một "Thông điệp Trực tiếp" (ví dụ: API call `POST /agent/knowledge_extraction/notify_new_document` với payload `{ "event_id": "...", "raw_data_id": "..." }`) đến `KnowledgeExtractionAgent`.
                *   Hoặc, `KnowledgeExtractionAgent` tự "Theo dõi chủ động" (Agent-initiated Polling) ontology để phát hiện `SystemEvent` mới và đọc `RawDataNode` liên quan.
            3.  **Trích xuất Tri thức và Cập nhật Ontology:** `KnowledgeExtractionAgent` phân tích tài liệu từ `RawDataNode`, trích xuất các `KnowledgeSnippet`, `Project` (nếu có), `Skill` liên quan, tạo embedding và cập nhật ontology. Nó cũng có thể "publish" một `LearningEvent(type="KnowledgeExtracted", source_document_id={ID}, snippets_count={N})`.
            4.  **Giám sát bởi AGE:** AGE có thể giám sát toàn bộ quá trình này, theo dõi các `Event` liên quan và điều phối tài nguyên (ví dụ: ưu tiên xử lý cho `KnowledgeExtractionAgent` nếu hệ thống đang rảnh) nếu cần.

        * **Kịch bản 2: Phát hiện và Giải quyết một "Tension" (Tích hợp Pub/Sub và Direct Messaging):**
            1.  **Phát hiện "Tension" và Tạo `Event` (Publication):**
                * ` TensionDetectionAgent` liên tục phân tích dữ liệu từ các nguồn khác nhau (e.g., `ProjectNode` có rủi ro, `TaskNode` bị trễ hạn, `ResourceNode` bị quá tải, phản hồi tiêu cực từ `FeedbackNode`, mâu thuẫn trong `KnowledgeSnippetNode`) trong ontology.
                *   Khi phát hiện một "Tension" tiềm ẩn hoặc rõ ràng (ví dụ: một `Task` quan trọng trong `Project` "Alpha" bị trễ 3 ngày và chưa có người chịu trách nhiệm cập nhật), `TensionDetectionAgent` tạo một `TensionNode` mới trong ontology, mô tả chi tiết vấn đề, mức độ ưu tiên dự kiến, và các thực thể liên quan.
                *   Đồng thời, nó "publish" một `TensionEvent(type="NewTensionDetected", tension_id={ID}, severity="High", project_id="Alpha")` vào ontology.
            2.  **`ResolutionCoordinatorAgent` Nhận Thông báo (Subscription & Notification):**
                * ` ResolutionCoordinatorAgent` đã "đăng ký" (`INTERESTED_IN` relationship) với các `TensionEvent` loại `NewTensionDetected`.
                *   AGE, thông qua "Thông báo qua AGE", phát hiện `TensionEvent` mới và gửi "Thông điệp Trực tiếp" (ví dụ: API call `POST /agent/resolution_coordinator/notify_new_tension` với payload `{ "event_id": "...", "tension_id": "..." }`) đến `ResolutionCoordinatorAgent`.
                *   Hoặc, `ResolutionCoordinatorAgent` tự "Theo dõi chủ động" ontology.
            3.  **Phân tích và Điều phối Giải quyết:**
                * ` ResolutionCoordinatorAgent` truy cập `TensionNode` và các node liên quan (e.g., `ProjectNode`, `TaskNode`, `UserNode` chịu trách nhiệm) để hiểu rõ bối cảnh.
                *   Dựa trên loại "Tension" và các quy tắc được định nghĩa, `ResolutionCoordinatorAgent` xác định (các) `TensionResolutionAgent` phù hợp để xử lý. Ví dụ, nếu là "Tension" về nguồn lực, nó có thể chọn một `TensionResolutionAgent` chuyên về tối ưu hóa nguồn lực.
                * ` ResolutionCoordinatorAgent` gửi "Thông điệp Trực tiếp" (ví dụ: `POST /agent/tension_resolver_X/assign_tension` với payload `{ "tension_id": "...", "priority": "High" }`) đến (các) `TensionResolutionAgent` được chọn, yêu cầu họ đề xuất giải pháp.
            4.  **`TensionResolutionAgent` Đề xuất và Thực thi Giải pháp:**
                *   (Các) `TensionResolutionAgent` nhận nhiệm vụ, phân tích `TensionNode`.
                *   Agent này có thể tương tác với các agent khác qua "Thông điệp Trực tiếp" để thu thập thêm thông tin hoặc đánh giá các lựa chọn (e.g., hỏi `ProjectManagementAgent` về mức độ linh hoạt của lịch trình, hỏi `ResourceAllocationAgent` về sự sẵn có của nguồn lực thay thế).
                * ` TensionResolutionAgent` đề xuất một hoặc nhiều `ResolutionOptionNode` (liên kết với `TensionNode`), mô tả hành động, chi phí, lợi ích.
                *   Nếu có quyền tự động thực thi và giải pháp rõ ràng, `TensionResolutionAgent` có thể trực tiếp thực hiện hành động (e.g., cập nhật `TaskNode` với người chịu trách nhiệm mới, điều chỉnh ngày hoàn thành dự kiến).
                *   Nếu cần sự chấp thuận của con người hoặc có nhiều lựa chọn phức tạp, `TensionResolutionAgent` cập nhật `TensionNode` với các `ResolutionOptionNode` và thông báo cho `ResolutionCoordinatorAgent` (qua "Thông điệp Trực tiếp"). `ResolutionCoordinatorAgent` sau đó có thể sử dụng `UserInterfaceAgent` để trình bày các lựa chọn cho Founder hoặc người quản lý liên quan.
            5.  **Cập nhật Trạng thái và "Publish" `Event` Kết quả:**
                *   Sau khi giải pháp được thực thi (tự động hoặc sau khi được phê duyệt), `TensionResolutionAgent` (hoặc `ResolutionCoordinatorAgent`) cập nhật trạng thái của `TensionNode` thành "Resolved" (hoặc "PartiallyResolved", "Escalated").
                *   Một `TensionEvent(type="TensionResolved", tension_id={ID}, resolution_details={...})` hoặc `TensionEvent(type="TensionResolutionFailed", tension_id={ID}, reason={...})` được "publish".
            6.  **Giám sát và Học hỏi:**
                *   AGE và `LearningAndOptimizationAgent` có thể theo dõi các `TensionEvent` để đánh giá hiệu quả của quy trình giải quyết "Tension", xác định các mẫu "Tension" thường gặp và đề xuất cải tiến cho hệ thống hoặc quy trình làm việc.
        * **Kịch bản 3: Ghi nhận một "WIN" (Tích hợp Pub/Sub và Direct Messaging):**
            1.  **Hoàn thành `Project` và Tạo `Event` (Publication):** `ProjectManagementAgent` cập nhật `ProjectNode` trong ontology với trạng thái "Completed" và "publish" một `ProjectEvent(type="ProjectCompletedSuccessfully", project_id={ID})`.
            2.  **`WINRecognitionAgent` Nhận Thông báo (Subscription & Notification):**
                * ` WINRecognitionAgent` (hoặc một phần của `KnowledgeSynthesisAgent`) đã "đăng ký" với các `ProjectEvent` loại `ProjectCompletedSuccessfully`.
                *   AGE, thông qua "Thông báo qua AGE", phát hiện `ProjectEvent` và gửi "Thông điệp Trực tiếp" đến `WINRecognitionAgent` (ví dụ: `POST /agent/win_recognition/notify_project_completed` với payload `{ "event_id": "...", "project_id": "..." }`).
                *   Hoặc, `WINRecognitionAgent` tự "Theo dõi chủ động" ontology.
            3.  **Phân tích và Tổng hợp `WIN`:**
                * ` WINRecognitionAgent` truy vấn chi tiết `ProjectNode`, `TensionNode` đã giải quyết, các `KnowledgeSnippetNode` đã sử dụng/tạo ra, và các `ResourceNode` đã đóng góp.
                *   Agent này có thể sử dụng LLM (thông qua `LLMInterfaceAgent` bằng "Thông điệp Trực tiếp") để hỗ trợ tóm tắt bài học, phân tích tác động.
            4.  **Tạo `WINNode` và "Publish" `WINEvent`:**
                * ` WINRecognitionAgent` tạo một `WINNode` mới trong ontology, liên kết tất cả các yếu tố trên, định lượng giá trị (nếu có thể) và "đóng gói" bài học kinh nghiệm.
                *   Một `WINEvent(type="NewWINRecognized", win_id={ID}, project_id={ID})` được "publish".
            5.  **Thông báo `WIN` (Subscription & Direct Messaging):**
                * ` NotificationAgent` đã "đăng ký" với các `WINEvent` loại `NewWINRecognized`.
                *   Khi nhận được thông báo (qua AGE hoặc polling), `NotificationAgent` soạn thảo thông báo và gửi "Thông điệp Trực tiếp" (ví dụ: email, tin nhắn qua API) đến Founder và các bên liên quan về `WIN` mới này.
            6.  **Ghi nhận và Lan tỏa `WIN`:**
                * ` WINRecognitionAgent` ghi nhận `WIN` trong ontology và lan tỏa thông tin về thành tựu này trong hệ thống.
                * ` GoalAlignmentAgent` có thể được thông báo về `WINEvent` mới để phân tích và cập nhật tiến độ thực hiện các mục tiêu chiến lược.

        * **Kịch bản 4: Đảm bảo Dự án phù hợp Mục tiêu Chiến lược (Tích hợp Pub/Sub và Direct Messaging):**
            1.  **Tạo `ProjectProposal` và "Publish" `Event`:** Một `ProjectProposalNode` được tạo trong ontology (bởi Founder qua giao diện, `TensionResolutionAgent` đề xuất, hoặc một agent khác). Một `ProjectProposalEvent(type="NewProposalCreated", proposal_id={ID})` được "publish" vào ontology.
            2.  **`GoalAlignmentAgent` Nhận Thông báo (Subscription & Notification):**
                * ` GoalAlignmentAgent` đã "đăng ký" (`INTERESTED_IN` relationship trong ontology) với các `ProjectProposalEvent` loại `NewProposalCreated`.
                *   AGE, thông qua cơ chế "Thông báo qua AGE" (AGE-mediated Notification) của Pub/Sub, phát hiện `ProjectProposalEvent` mới và gửi "Thông điệp Trực tiếp" đến `GoalAlignmentAgent` (ví dụ: API call `POST /agent/goal_alignment/notify_new_proposal` với payload `{ "event_id": "...", "proposal_id": "..." }`).
                *   Hoặc, `GoalAlignmentAgent` tự "Theo dõi chủ động" (Agent-initiated Polling) ontology để phát hiện `ProjectProposalEvent` mới.
            3.  **Phân tích Sự phù hợp Chiến lược:** `GoalAlignmentAgent` truy cập thông tin chi tiết của `ProjectProposalNode` (mục tiêu, kết quả dự kiến, nguồn lực yêu cầu, các `TensionNode` liên quan) và so sánh với các `ObjectiveNode`, `GoalNode`, và `KeyResultNode` hiện tại của tổ chức được lưu trong ontology.
            4.  **Xử lý Kết quả Phân tích:**
                * **Trường hợp 1: Đề xuất phù hợp rõ ràng với mục tiêu chiến lược:**
                    * ` GoalAlignmentAgent` cập nhật trạng thái của `ProjectProposalNode` thành "AlignedWithStrategy", có thể bổ sung các `Tag` hoặc tạo relationship `CONTRIBUTES_TO` trực tiếp với `ObjectiveNode`/`KeyResultNode` mà nó đóng góp.
                    *   Agent này có thể đề xuất các `MetricNode` cụ thể để theo dõi sự đóng góp của dự án vào `KeyResultNode` nếu được triển khai.
                    * ` GoalAlignmentAgent` "publish" một `AlignmentAssessmentEvent(type="ProposalAligned", proposal_id={ID}, assessment_details={...})`. AGE và các agent liên quan (như `ProjectManagementAgent`, nếu có vai trò trong quy trình duyệt) có thể "đăng ký" `Event` này hoặc nhận "Thông điệp Trực tiếp" từ `GoalAlignmentAgent` (ví dụ: `POST /agent/project_management/proposal_review_update` với payload chứa thông tin đánh giá) để làm cơ sở cho các bước tiếp theo trong quy trình phê duyệt và triển khai dự án.
                * **Trường hợp 2: Đề xuất không phù hợp hoặc mức độ phù hợp chưa rõ ràng:**
                    * ` GoalAlignmentAgent` cập nhật trạng thái của `ProjectProposalNode` thành "AlignmentReviewNeeded" hoặc "PotentiallyMisaligned".
                    *   Agent "publish" một `AlignmentAlertEvent(type="ProposalMisaligned", proposal_id={ID}, alert_details={...})`, chi tiết lý do không phù hợp hoặc các điểm cần làm rõ.
                    *   Đồng thời, `GoalAlignmentAgent` có thể gửi "Thông điệp Trực tiếp" đến AGE và agent/người đã tạo `ProjectProposal` (ví dụ: `POST /age/notify_alignment_issue` hoặc `POST /agent/{creator_agent_id}/proposal_feedback`) với nội dung cảnh báo và các đề xuất (yêu cầu điều chỉnh `ProjectProposal`, cung cấp thêm thông tin, hoặc đề xuất từ chối nếu hoàn toàn không liên quan đến chiến lược hiện tại).
            6.  `AGE` dựa trên phân tích của `GoalAlignmentAgent`, cùng với các yếu tố khác (e.g., nguồn lực, tính khả thi từ `ResourceAllocationAgent`), để ra quyết định cuối cùng về việc phê duyệt, yêu cầu chỉnh sửa, hoặc từ chối `ProjectProposal`.

        * **Kịch bản 5: Giám sát Tuân thủ Đạo đức trong Xử lý Dữ liệu:**
            1.  `KnowledgeExtractionAgent` nhận một `Task` để xử lý một `RawDataNode` mới (e.g., một tập hợp email khách hàng, bản ghi cuộc họp) nhằm trích xuất `KnowledgeSnippet` và các thực thể ontology khác.
            2.  `EthicalComplianceAgent` được thiết kế để giám sát các hoạt động liên quan đến xử lý dữ liệu, đặc biệt là khi có khả năng chứa `PersonalData` hoặc thông tin nhạy cảm khác.
            3.  Khi `KnowledgeExtractionAgent` bắt đầu truy cập và phân tích `RawDataNode`, `EthicalComplianceAgent` kiểm tra:
                *   Nguồn gốc của dữ liệu và sự cho phép sử dụng (nếu cần).
                *   Sự tồn tại của `PersonalData` và liệu các biện pháp bảo vệ (e.g., ẩn danh hóa, mã hóa) có được áp dụng theo `DataPrivacyPolicy` hay không.
                *   Liệu quy trình trích xuất có nguy cơ tạo ra các `KnowledgeSnippet` mang tính thiên kiến (bias) dựa trên các `AIEthicsGuideline` hay không.
            4.  **Trường hợp 1: Hoạt động tuân thủ các chính sách và hướng dẫn:**
                * ` EthicalComplianceAgent` ghi nhận hoạt động là tuân thủ. Có thể tạo một `ComplianceLogEvent` ở mức độ thấp để lưu vết, không cần thông báo rộng rãi.
            5.  **Trường hợp 2: Phát hiện vi phạm hoặc nguy cơ vi phạm tiềm ẩn:**
                * ` EthicalComplianceAgent` ngay lập tức tạo một `ComplianceAlertEvent` với mức độ nghiêm trọng tương ứng và gửi `Notification` đến `AGE`, Founder, hoặc quản trị viên hệ thống được chỉ định.
                *   Tùy theo cấu hình và mức độ nghiêm trọng, `EthicalComplianceAgent` có thể gửi yêu cầu đến `AGE` để tạm dừng `Task` xử lý dữ liệu của `KnowledgeExtractionAgent` đối với `RawDataNode` cụ thể đó cho đến khi vấn đề được giải quyết.
                *   Báo cáo của `EthicalComplianceAgent` sẽ bao gồm chi tiết về vi phạm/nguy cơ và đề xuất các hành động khắc phục, ví dụ: xem xét lại quy trình, xin phép lại người dùng, loại bỏ dữ liệu nhạy cảm, hoặc điều chỉnh thuật toán để giảm thiên kiến.
            6.  `AGE` tiếp nhận cảnh báo, điều phối các hành động tiếp theo (e.g., yêu cầu `KnowledgeExtractionAgent` dừng, giao `Task` cho Founder để xem xét, kích hoạt quy trình xử lý sự cố) để giải quyết vấn đề tuân thủ và đảm bảo hệ thống hoạt động có đạo đức.

        **10.3.3. Vai trò Điều phối của AGE (Artificial Genesis Engine):**

            Artificial Genesis Engine (AGE) là hạt nhân trung tâm, đóng vai trò "bộ não" điều phối và quản lý toàn bộ hệ sinh thái AI agent của TRM-OS. AGE không chỉ là một agent đơn thuần mà là một hệ thống phức hợp với các năng lực sau:

            * **Giám sát Hệ thống Toàn diện (System-wide Monitoring):**
                * **Lắng nghe Event:** AGE đăng ký lắng nghe một loạt các `Event` quan trọng từ ontology, bao gồm `SystemEvent`, `ProjectEvent`, `TensionEvent`, `WinEvent`, `ComplianceAlertEvent`, `AlignmentAlertEvent`, và các `Notification` có mức độ ưu tiên cao.
                * **Theo dõi Trạng thái Agent:** AGE theo dõi trạng thái hoạt động (e.g., idle, busy, error), tài nguyên sử dụng, và hiệu suất của các agent chuyên biệt.
                * **Phân tích `Metric` Chiến lược:** AGE tổng hợp và phân tích các `Metric` liên quan đến `Objective` và `Goal` để có cái nhìn tổng quan về hiệu suất của tổ chức.

            * **Ra Quyết định và Phân công Nhiệm vụ (Decision Making & Task Delegation):**
                * **Ưu tiên hóa:** Dựa trên các `Goal` chiến lược, mức độ khẩn cấp của `Tension`, hoặc tầm quan trọng của `ComplianceAlertEvent`, AGE có thể điều chỉnh mức độ ưu tiên của các `Task` và `Project`.
                * **Phân rã và Giao việc:** Đối với các yêu cầu phức tạp hoặc các `Project` lớn, AGE có thể phân rã thành các `Task` nhỏ hơn và giao cho các agent chuyên biệt phù hợp. Ví dụ, khi một `ProjectProposal` được duyệt, AGE có thể khởi tạo `Project` và giao cho `ProjectManagementAgent` quản lý, đồng thời thông báo cho `ResourceAllocationAgent` và `GoalAlignmentAgent`.
                * **Kích hoạt Agent:** AGE có thể chủ động kích hoạt một agent khi nhận thấy một điều kiện cụ thể được đáp ứng. Ví dụ, nếu một lượng lớn `RawDataNode` mới được tạo, AGE có thể tăng số lượng instance của `KnowledgeExtractionAgent` (nếu kiến trúc cho phép) hoặc điều chỉnh lịch làm việc của nó.

            * **Quản lý Vòng đời Agent (Agent Lifecycle Management):**
                *   Khởi tạo, tạm dừng, tiếp tục, và kết thúc các agent chuyên biệt khi cần thiết.
                *   Cập nhật cấu hình hoặc mô hình của agent (nếu có cơ chế tự học hoặc nâng cấp).

            * **Giải quyết Xung đột và Điều phối Tương tác Phức tạp (Conflict Resolution & Complex Interaction Orchestration):**
                * **Xung đột Tài nguyên:** Nếu nhiều agent cùng yêu cầu một `Resource` hạn chế, AGE sẽ quyết định dựa trên ưu tiên và mục tiêu chiến lược (có thể tham vấn `ResourceAllocationAgent`).
                * **Xung đột Thông tin/Quyết định:** Nếu các agent đưa ra các đề xuất hoặc phân tích trái ngược nhau (e.g., `TensionResolutionAgent` đề xuất một giải pháp, nhưng `GoalAlignmentAgent` thấy nó không phù hợp mục tiêu), AGE sẽ là trọng tài cuối cùng, có thể yêu cầu thêm thông tin, hoặc tham vấn Founder.
                * **Điều phối Chuỗi Công việc Dài:** AGE đảm bảo các agent phối hợp nhịp nhàng trong các chuỗi công việc phức tạp, ví dụ từ khi phát hiện `Tension` đến khi ghi nhận `WIN` từ dự án giải quyết `Tension` đó.

            * **Giao tiếp và Tương tác:**
                * **Qua Ontology:** AGE chủ yếu tương tác bằng cách tạo/cập nhật các node và relationship trong ontology (e.g., tạo `Task` cho agent, thay đổi `status` của `Project`).
                * **Thông điệp Trực tiếp:** Trong trường hợp khẩn cấp hoặc cần chỉ thị rõ ràng, AGE có thể gửi thông điệp trực tiếp đến các agent (e.g., yêu cầu dừng một `Task` ngay lập tức).
                * **Giao diện với Founder:** AGE cung cấp thông tin tổng hợp, cảnh báo, và các điểm quyết định quan trọng cho Founder thông qua một giao diện quản trị, cho phép Founder giám sát và can thiệp khi cần.

            * **Học hỏi và Thích ứng (Learning & Adaptation - Tiềm năng):**
                *   Trong tương lai, AGE có thể được phát triển để học hỏi từ các `WIN`, `Tension` đã giải quyết, và hiệu suất của các agent để tự tối ưu hóa quy trình điều phối và ra quyết định.

            Tóm lại, AGE hoạt động như một người quản lý thông minh và linh hoạt, đảm bảo rằng tất cả các AI agent chuyên biệt hoạt động đồng bộ, hiệu quả, và luôn hướng tới mục tiêu chung của TRM-OS, đồng thời duy trì sự tuân thủ và cân bằng trong hệ thống.
10.4. Ngăn xếp Công nghệ Đề xuất cho Hệ thống AI Agentic (Cập nhật Tháng 6/2025)
    **10.4.1. Nguyên tắc Chỉ đạo Lựa chọn Công nghệ:**

        Việc lựa chọn công nghệ cho hệ thống AI Agentic của TRM-OS phải tuân theo các nguyên tắc chỉ đạo sau để đảm bảo tính bền vững, hiệu quả và khả năng phát triển trong tương lai:

        * **Phù hợp với Kiến trúc Ontology-Driven:** Ưu tiên hàng đầu cho các công nghệ hỗ trợ mạnh mẽ việc xây dựng, truy vấn, và tương tác với knowledge graph (đặc biệt là Neo4j Aura). Công nghệ phải cho phép biểu diễn và xử lý hiệu quả các mối quan hệ phức tạp trong ontology.
        * **Ưu tiên Python và Hệ sinh thái AI của Python:** Python là ngôn ngữ chủ đạo cho phát triển AI, với sự phong phú của các thư viện, framework và cộng đồng hỗ trợ. Các công nghệ được chọn nên tích hợp tốt với Python.
        * **Khả năng Tích hợp và Mở rộng (Interoperability & Scalability):** Lựa chọn các công cụ, thư viện, và nền tảng có khả năng tích hợp liền mạch với nhau. Hệ thống phải được thiết kế để có thể mở rộng quy mô (cả về số lượng agent, lượng dữ liệu xử lý, và độ phức tạp của tác vụ) một cách hiệu quả.
        * **Hỗ trợ bởi Cộng đồng và Hệ sinh thái Phát triển Mạnh mẽ:** Ưu tiên các công nghệ mã nguồn mở (nếu phù hợp) hoặc các giải pháp thương mại có cộng đồng người dùng lớn, tài liệu đầy đủ, lộ trình phát triển rõ ràng và được hỗ trợ tích cực.
        * **Hiệu suất và Độ tin cậy:** Công nghệ phải đảm bảo hiệu suất xử lý đáp ứng yêu cầu của các tác vụ thời gian thực hoặc gần thời gian thực (nếu có), đồng thời duy trì độ ổn định và tin cậy cao cho toàn hệ thống.
        * **An toàn và Bảo mật Dữ liệu (Security & Data Privacy):** Các công nghệ phải tuân thủ các tiêu chuẩn bảo mật quốc tế, cho phép triển khai các biện pháp bảo vệ dữ liệu mạnh mẽ, kiểm soát truy cập chi tiết, và hỗ trợ mã hóa dữ liệu cả khi lưu trữ và truyền tải. Đặc biệt quan trọng khi xử lý `PersonalData` và thông tin nhạy cảm.
        * **Chi phí Vận hành và Phát triển Hợp lý (Cost-Effectiveness):** Cân nhắc kỹ lưỡng giữa chi phí bản quyền (nếu có), chi phí hạ tầng, chi phí vận hành, và lợi ích chiến lược cũng như hiệu quả hoạt động mà công nghệ mang lại.
        * **Dễ dàng Phát triển, Triển khai và Bảo trì (Developer-Friendly & Maintainability):** Lựa chọn công nghệ mà đội ngũ phát triển (bao gồm cả sự hỗ trợ từ AI như CursorAI/WindsurfAI) có thể nhanh chóng làm quen, phát triển, gỡ lỗi và bảo trì. Ưu tiên các giải pháp có công cụ hỗ trợ tốt (monitoring, logging, debugging).
        * **Ưu tiên Giải pháp Cloud-Native và Managed Services:** Tận dụng các dịch vụ quản lý trên nền tảng đám mây (ví dụ: AWS, Google Cloud, Azure) để giảm thiểu gánh nặng quản lý hạ tầng, tăng tính linh hoạt, khả năng tự động co giãn và đảm bảo tính sẵn sàng cao.
        * **Tính Mô-đun và Khả năng Thay thế (Modularity & Replaceability):** Kiến trúc hệ thống và các công nghệ được chọn nên cho phép các thành phần (ví dụ: một mô hình LLM cụ thể, một cơ sở dữ liệu vector) có thể được nâng cấp hoặc thay thế một cách độc lập mà không gây ảnh hưởng lớn đến các phần khác của hệ thống.
        * **Hỗ trợ Xử lý Ngôn ngữ Tự nhiên và Đa phương thức:** Do đặc thù của TRM-OS, các công nghệ liên quan đến LLM, embedding, xử lý giọng nói, hình ảnh (nếu có trong tương lai) cần được xem xét kỹ lưỡng.
    **10.4.2. Framework Phát triển AI Agent (LangChain, CrewAI, AutoGen, etc.):**

        Việc lựa chọn framework phát triển AI agent là một quyết định quan trọng, ảnh hưởng đến tốc độ phát triển, khả năng bảo trì, và hiệu quả của hệ thống. TRM-OS sẽ ưu tiên các framework sau, với khả năng kết hợp các điểm mạnh của từng framework nếu cần thiết:

        * **LangChain (Python/TypeScript):**
            * **Mô tả:** Một framework toàn diện để xây dựng các ứng dụng dựa trên LLM, bao gồm cả các hệ thống agent. Cung cấp các module cho việc quản lý prompt, kết nối LLM, quản lý bộ nhớ, tạo chuỗi (chains), và xây dựng agent.
            * **Ưu điểm:**
                * **Hệ sinh thái lớn:** Rất nhiều tích hợp với các LLM, cơ sở dữ liệu vector, công cụ (tools), và các dịch vụ khác.
                * **Tính linh hoạt cao:** Cho phép tùy chỉnh sâu và xây dựng các luồng logic phức tạp.
                * **Cộng đồng mạnh mẽ:** Được hỗ trợ rộng rãi, nhiều tài liệu và ví dụ.
                * **LangSmith:** Công cụ observability và debugging mạnh mẽ.
            * **Cân nhắc:**
                *   Độ phức tạp có thể cao đối với các agent đơn giản.
                *   Việc quản lý các agent phức tạp và tương tác giữa chúng có thể cần nhiều logic tự xây dựng.
            * **Ứng dụng trong TRM-OS:** Là nền tảng chính để xây dựng các agent chuyên biệt, đặc biệt là các agent cần tương tác nhiều với LLM, sử dụng các công cụ bên ngoài, và có logic xử lý phức tạp. `LLMInterfaceAgent` có thể được xây dựng chủ yếu dựa trên LangChain.

        * **CrewAI (Python):**
            * **Mô tả:** Một framework được thiết kế để điều phối các AI agent tự trị làm việc cộng tác với nhau. Tập trung vào việc định nghĩa vai trò (roles), nhiệm vụ (tasks), và quy trình làm việc (processes) cho một "đội ngũ" (crew) các agent.
            * **Ưu điểm:**
                * **Tập trung vào sự cộng tác:** Dễ dàng định nghĩa cách các agent chia sẻ thông tin và phối hợp để đạt mục tiêu chung.
                * **Cấu trúc rõ ràng:** Cung cấp một mô hình trực quan cho việc thiết kế các hệ thống multi-agent.
                * **Tích hợp LangChain:** Có thể sử dụng các công cụ và LLM của LangChain bên trong các agent của CrewAI.
                * **Hỗ trợ các quy trình tuần tự và phân cấp.**
            * **Cân nhắc:**
                *   Là một framework mới hơn LangChain, hệ sinh thái có thể chưa đa dạng bằng.
                *   Có thể phù hợp hơn cho các tác vụ cộng tác có cấu trúc rõ ràng.
            * **Ứng dụng trong TRM-OS:** Rất phù hợp để triển khai các kịch bản tương tác phức tạp giữa nhiều agent như trong Mục 10.3.2. Ví dụ, một "crew" có thể bao gồm `TensionDetectionAgent`, `ResolutionCoordinatorAgent`, và `TensionResolutionAgent` làm việc cùng nhau. AGE có thể sử dụng các khái niệm của CrewAI để điều phối các nhóm agent.

        * **Microsoft AutoGen (Python):**
            * **Mô tả:** Một framework để đơn giản hóa việc điều phối, tối ưu hóa và tự động hóa các luồng làm việc của LLM. Cho phép xây dựng các agent có khả năng trò chuyện với nhau và với con người, sử dụng code và các công cụ.
            * **Ưu điểm:**
                * **Mô hình hội thoại linh hoạt:** Hỗ trợ các mẫu hội thoại phức tạp giữa nhiều agent.
                * **Khả năng thực thi code:** Agent có thể viết và thực thi code (ví dụ: Python scripts) để giải quyết vấn đề.
                * **Tùy biến cao:** Cho phép tùy chỉnh hành vi của agent.
            * **Cân nhắc:**
                *   Tập trung mạnh vào các tương tác dựa trên hội thoại.
                *   Việc tích hợp sâu với ontology của TRM-OS có thể cần nhiều nỗ lực tùy chỉnh.
            * **Ứng dụng trong TRM-OS:** Có thể hữu ích cho các agent cần khả năng tự giải quyết vấn đề bằng cách sinh và thực thi code, hoặc trong các kịch bản mà nhiều agent cần "thảo luận" để đưa ra giải pháp. `LearningAndOptimizationAgent` có thể sử dụng AutoGen để thử nghiệm và tối ưu hóa các chiến lược.

        * **Lựa chọn Kết hợp và Chiến lược:**
            * **Nền tảng chính:** LangChain sẽ được sử dụng làm nền tảng cơ bản cho việc xây dựng các năng lực cốt lõi của từng agent (kết nối LLM, quản lý bộ nhớ, sử dụng tool).
            * **Điều phối Cộng tác:** CrewAI sẽ được ưu tiên cho việc thiết kế và điều phối các nhóm agent làm việc cộng tác trong các quy trình có cấu trúc. AGE có thể được xem như một "meta-crew" hoặc người quản lý các "crew" nhỏ hơn.
            * **Năng lực Chuyên biệt:** AutoGen có thể được tích hợp cho các agent hoặc tác vụ cụ thể đòi hỏi khả năng hội thoại phức tạp và thực thi code tự động.
            * **Ưu tiên sự đơn giản:** Đối với các agent có logic đơn giản, có thể không cần đến một framework phức tạp mà chỉ cần các thư viện Python cơ bản và SDK của các dịch vụ (ví dụ: Neo4j client, Supabase client).
            * **Phát triển với CursorAI/WindsurfAI:** Lựa chọn framework cũng cần cân nhắc đến khả năng AI (như CursorAI) hỗ trợ tạo, hiểu và bảo trì code cho framework đó. Các framework phổ biến với cấu trúc rõ ràng thường dễ dàng hơn cho AI hỗ trợ.

        Mục tiêu là tạo ra một hệ thống linh hoạt, nơi các agent có thể được phát triển bằng công cụ phù hợp nhất cho nhiệm vụ của chúng, nhưng vẫn có thể tương tác hiệu quả với nhau thông qua các chuẩn giao tiếp đã định nghĩa (Ontology-driven và Direct Messaging).
    **10.4.3. Mô hình AI (LLMs, Multimodal Models, GNNs - truy vấn, Embedding Models):**

        Hệ thống AI Agentic của TRM-OS sẽ tận dụng sức mạnh của nhiều loại mô hình AI khác nhau để thực hiện các tác vụ đa dạng. Việc lựa chọn và tích hợp các mô hình này phải tuân theo các nguyên tắc đã nêu ở mục 10.4.1.

        * **1. Mô hình Ngôn ngữ Lớn (Large Language Models - LLMs):**
            * **Vai trò:** Là "bộ não" ngôn ngữ của nhiều agent, chịu trách nhiệm hiểu yêu cầu, xử lý văn bản, sinh nội dung, tóm tắt, dịch thuật, trả lời câu hỏi, hỗ trợ ra quyết định, và điều khiển các công cụ (tools).
            * **Các lựa chọn tiềm năng (ví dụ, có thể thay đổi theo thời gian):**
                * **OpenAI GPT Series (GPT-4, GPT-4o, GPT-3.5-turbo):** Hiệu suất hàng đầu, khả năng rozum tốt, context window lớn (đặc biệt GPT-4o và các phiên bản mới hơn), hỗ trợ đa phương thức (GPT-4o).
                * **Anthropic Claude Series (Claude 3 Opus, Sonnet, Haiku):** Khả năng rozum mạnh mẽ, context window rất lớn, tập trung vào tính an toàn và độ tin cậy.
                * **Google Gemini Series (Gemini 1.5 Pro, Ultra):** Khả năng đa phương thức mạnh mẽ, context window lớn, hiệu suất cao.
                * **Các mô hình mã nguồn mở (ví dụ: Llama 3, Mixtral):** Cho phép tùy chỉnh sâu, fine-tuning trên dữ liệu cụ thể của TRM, và có thể triển khai on-premise hoặc trong môi trường VPC để tăng cường bảo mật và kiểm soát chi phí.
            * **Tiêu chí lựa chọn:**
                * **Hiệu suất trên các tác vụ cụ thể:** (ví dụ: rozum, sinh code, tóm tắt, tuân theo chỉ dẫn).
                * **Kích thước Context Window:** Quan trọng cho các tác vụ cần xử lý lượng lớn thông tin đầu vào.
                * **Chi phí API/Vận hành:** Cân nhắc giữa hiệu suất và chi phí.
                * **Khả năng Fine-tuning:** Đối với các tác vụ chuyên biệt hoặc để thích ứng với thuật ngữ/domain của TRM.
                * **Tốc độ phản hồi (Latency).**
                * **Hỗ trợ đa phương thức (nếu cần).**
                * **Tính sẵn sàng và độ tin cậy của API.**
            * **Tích hợp:** Chủ yếu thông qua các framework như LangChain, CrewAI. `LLMInterfaceAgent` sẽ đóng vai trò trung gian, quản lý việc truy cập và tối ưu hóa sử dụng LLM.

        * **2. Mô hình Embedding (Embedding Models):**
            * **Vai trò:** Chuyển đổi văn bản (và có thể các loại dữ liệu khác) thành các vector số học biểu diễn ý nghĩa ngữ nghĩa. Cực kỳ quan trọng cho:
                * **Retrieval Augmented Generation (RAG):** Tìm kiếm thông tin liên quan từ cơ sở tri thức (ví dụ: tài liệu, ontology) để cung cấp ngữ cảnh cho LLM.
                * **Semantic Search:** Tìm kiếm tài liệu, đoạn văn, hoặc các thực thể trong ontology dựa trên ý nghĩa thay vì từ khóa.
                * **Phân cụm và Phân loại:** Nhóm các đối tượng tương tự hoặc gán nhãn cho dữ liệu.
                * **Phát hiện Bất thường/Tension:** So sánh embedding của dữ liệu mới với các mẫu đã biết.
            * **Các lựa chọn tiềm năng:**
                * **OpenAI Ada v2:** Phổ biến, hiệu quả về chi phí, hiệu suất tốt cho nhiều tác vụ.
                * **Sentence Transformers (ví dụ: `all-MiniLM-L6-v2`, `multi-qa-mpnet-base-dot-v1`):** Nhiều mô hình mã nguồn mở, có thể fine-tuning, hỗ trợ đa ngôn ngữ.
                * **Cohere Embed:** Các mô hình embedding mạnh mẽ, hỗ trợ đa ngôn ngữ.
                * **Voyage AI:** Cung cấp các mô hình embedding hiệu suất cao.
                * **Google Gecko (trong Vertex AI):** Mô hình embedding của Google.
            * **Tiêu chí lựa chọn:**
                * **Chất lượng Embedding:** Đo lường bằng các benchmark trên tác vụ downstream (ví dụ: RAG, search).
                * **Kích thước Vector:** Ảnh hưởng đến chi phí lưu trữ và tốc độ tìm kiếm.
                * **Tốc độ Embedding và Chi phí.**
                * **Khả năng Fine-tuning.**
                * **Hỗ trợ đa ngôn ngữ (nếu cần).**
            * **Tích hợp:** Sử dụng với các cơ sở dữ liệu vector (Supabase Vector, Pinecone, Weaviate, etc.) và trong các luồng RAG của LangChain. `KnowledgeExtractionAgent` và `OntologyNavigationAgent` sẽ sử dụng nhiều mô hình embedding.

        * **3. Mô hình Đồ thị Nơ-ron (Graph Neural Networks - GNNs):**
            * **Vai trò:** Học trực tiếp trên cấu trúc đồ thị của ontology (Neo4j Aura). Có thể được sử dụng cho:
                * **Dự đoán Liên kết (Link Prediction):** Gợi ý các mối quan hệ tiềm năng giữa các thực thể trong ontology.
                * **Phân loại Nút (Node Classification):** Gán nhãn hoặc thuộc tính cho các nút dựa trên ngữ cảnh đồ thị.
                * **Truy vấn Thông minh trên Đồ thị:** Tìm kiếm các mẫu phức tạp hoặc suy luận ngầm định mà các truy vấn Cypher truyền thống khó thực hiện.
                * **Nhúng Đồ thị (Graph Embeddings):** Tạo vector biểu diễn cho các nút và cạnh, có thể kết hợp với các mô hình khác.
            * **Các lựa chọn tiềm năng:**
                *   Các thư viện GNN như PyTorch Geometric (PyG), Deep Graph Library (DGL).
                *   Neo4j Graph Data Science Library: Cung cấp các thuật toán đồ thị và khả năng huấn luyện mô hình GNN.
            * **Tiêu chí lựa chọn:**
                * **Khả năng tích hợp với Neo4j Aura.**
                * **Hiệu suất trên các tác vụ đồ thị cụ thể.**
                * **Khả năng mở rộng cho các đồ thị lớn.**
            * **Tích hợp:** `OntologyManagementAgent` và `LearningAndOptimizationAgent` có thể khám phá và triển khai GNN để cải thiện sự hiểu biết và tính nhất quán của ontology. Đây có thể là một lĩnh vực phát triển trong tương lai.

        * **4. Mô hình Đa phương thức (Multimodal Models):**
            * **Vai trò:** Xử lý và hiểu thông tin từ nhiều loại dữ liệu khác nhau (ví dụ: văn bản, hình ảnh, âm thanh).
            * **Các lựa chọn tiềm năng:**
                * **OpenAI GPT-4o/GPT-4V:** Hỗ trợ đầu vào hình ảnh.
                * **Google Gemini:** Được thiết kế từ đầu cho đa phương thức.
                * **LLaVA, CLIP:** Các mô hình mã nguồn mở cho thị giác-ngôn ngữ.
            * **Tiêu chí lựa chọn:**
                * **Các phương thức được hỗ trợ.**
                * **Hiệu suất trên các tác vụ đa phương thức cụ thể.**
                * **Chi phí và khả năng tích hợp.**
            * **Tích hợp:** Nếu TRM-OS cần xử lý các yêu cầu hoặc dữ liệu đầu vào đa phương thức (ví dụ: người dùng gửi hình ảnh một vấn đề, hoặc phân tích tài liệu có cả văn bản và biểu đồ), các agent như `DataIngestionAgent` hoặc `UserInteractionAgent` sẽ cần tích hợp các mô hình này. Hiện tại, đây là một xem xét cho tương lai, nhưng việc lựa chọn các LLM có lộ trình hỗ trợ đa phương thức (như GPT-4o, Gemini) là một lợi thế.

        * **Chiến lược Chung:**
            * **Ưu tiên các mô hình có API (Managed Services):** Để giảm gánh nặng vận hành, đặc biệt là đối với các LLM lớn.
            * **Kết hợp mô hình:** Sử dụng các mô hình nhỏ hơn, chuyên biệt hơn cho các tác vụ cụ thể nếu hiệu quả và tiết kiệm chi phí hơn (ví dụ: một mô hình embedding nhỏ cho RAG thay vì dùng LLM lớn).
            * **Thử nghiệm và Đánh giá Liên tục:** Thị trường mô hình AI phát triển rất nhanh. Cần có quy trình để liên tục đánh giá các mô hình mới và cập nhật ngăn xếp công nghệ khi cần.
            * **`LLMInterfaceAgent`:** Đóng vai trò là một lớp trừu tượng, cho phép thay đổi hoặc thử nghiệm các LLM khác nhau ở backend mà không ảnh hưởng lớn đến logic của các agent khác.
    **10.4.4. Cơ sở dữ liệu và Lưu trữ Tri thức (Neo4j Aura, Supabase Vector, Snowflake, etc.):**

        Hệ thống lưu trữ dữ liệu và tri thức là nền tảng cốt lõi của TRM-OS, hỗ trợ các AI agent trong việc hiểu, suy luận và hành động. Lựa chọn công nghệ tập trung vào khả năng biểu diễn ontology, lưu trữ vector, quản lý dữ liệu có cấu trúc và phân tích dữ liệu quy mô lớn.

        * **1. Neo4j Aura (Graph Database - Managed Service):**
            * **Vai trò Chính:** Là kho lưu trữ trung tâm cho **Ontology TRM-OS**. Lưu trữ tất cả các `Entity`, `Relation`, `Property`, `Rule`, `WIN`, `Tension`, `Goal`, `Project`, `Task`, `User`, `AgentProfile`, và các khái niệm nghiệp vụ khác dưới dạng một đồ thị tri thức (knowledge graph) phong phú.
            * **Lý do lựa chọn:**
                * **Mô hình Đồ thị Tự nhiên:** Lý tưởng để biểu diễn các mối quan hệ phức tạp và đa dạng trong ontology.
                * **Ngôn ngữ Truy vấn Cypher:** Mạnh mẽ và trực quan cho việc truy vấn và thao tác trên dữ liệu đồ thị.
                * **Khả năng Suy luận Đồ thị:** Hỗ trợ các thuật toán đồ thị (ví dụ: tìm đường đi ngắn nhất, phân tích cộng đồng) có thể được sử dụng bởi các agent.
                * **Managed Service (AuraDB):** Giảm gánh nặng quản trị, đảm bảo tính sẵn sàng cao, tự động sao lưu và vá lỗi.
                * **Tích hợp Graph Data Science Library:** Cho phép chạy các thuật toán học máy trên đồ thị, bao gồm GNNs.
                * **Hỗ trợ Event Sourcing/CQRS (thông qua Neo4j Streams hoặc tương tự):** Quan trọng cho việc theo dõi thay đổi và cập nhật ontology.
            * **Tương tác của Agent:**
                *   Tất cả các agent đều tương tác với Neo4j Aura để đọc/ghi thông tin ontology liên quan đến vai trò của chúng.
                * ` OntologyManagementAgent`: Chịu trách nhiệm chính trong việc cập nhật, mở rộng và duy trì tính nhất quán của ontology.
                * ` OntologyNavigationAgent`: Giúp các agent khác truy vấn và hiểu các phần của ontology.
                *   Các agent sử dụng thông tin từ ontology để định hướng hành động và hiểu ngữ cảnh.

        * **2. Supabase (PostgreSQL with pgvector / Supabase Vector):**
            * **Vai trò Chính:**
                * **Lưu trữ Dữ liệu có Cấu trúc:** Quản lý dữ liệu người dùng (`UserProfile`, `UserPreferences`), dữ liệu hoạt động của agent (logs, metrics cơ bản), dữ liệu cấu hình ứng dụng.
                * **Lưu trữ Vector Embedding (Supabase Vector hoặc pgvector extension):** Lưu trữ các vector embedding của tài liệu, đoạn văn, các nút ontology, v.v., phục vụ cho RAG và semantic search.
                * **Backend-as-a-Service (BaaS):** Cung cấp các dịch vụ tích hợp sẵn như Authentication (Quản lý Danh tính Người dùng), Realtime Subscriptions (cho thông báo và cập nhật trực tiếp), Storage (lưu trữ file).
            * **Lý do lựa chọn:**
                * **PostgreSQL Mạnh mẽ:** Cơ sở dữ liệu quan hệ đáng tin cậy, hỗ trợ ACID.
                * **Hỗ trợ Vector Tích hợp:** `pgvector` là một extension phổ biến và hiệu quả; Supabase Vector cung cấp giải pháp được quản lý.
                * **Hệ sinh thái Supabase:** Giảm thời gian phát triển các tính năng backend phổ biến.
                * **Khả năng mở rộng tốt.**
                * **Tích hợp tốt với Python và các framework AI.**
            * **Tương tác của Agent:**
                * ` DataIngestionAgent`: Lưu trữ dữ liệu có cấu trúc và vector embedding vào Supabase.
                * ` KnowledgeExtractionAgent`: Truy xuất dữ liệu và embedding để xây dựng tri thức.
                *   Các agent thực hiện RAG sẽ truy vấn Supabase Vector để lấy ngữ cảnh.
                * ` UserInteractionAgent`: Sử dụng Supabase Auth và các bảng dữ liệu người dùng.

        * **3. Snowflake (Cloud Data Warehouse) hoặc giải pháp tương tự (ví dụ: Google BigQuery, AWS Redshift):**
            * **Vai trò Chính (Tiềm năng/Tương lai hoặc cho các module phân tích chuyên sâu):**
                * **Phân tích Dữ liệu Lớn:** Lưu trữ và phân tích khối lượng lớn dữ liệu lịch sử về hoạt động của hệ thống, hiệu suất agent, tương tác người dùng, kết quả dự án.
                * **Business Intelligence (BI):** Cung cấp dữ liệu cho các báo cáo và dashboard quản trị.
                * **Huấn luyện Mô hình AI/ML Quy mô Lớn:** Chuẩn bị dữ liệu và lưu trữ kết quả cho các mô hình học máy phức tạp (ví dụ: mô hình dự đoán, phân tích xu hướng dài hạn).
            * **Lý do lựa chọn:**
                * **Khả năng mở rộng và hiệu suất cao cho truy vấn phân tích.**
                * **Tách biệt lưu trữ và tính toán.**
                * **Tích hợp tốt với các công cụ BI và AI/ML.**
            * **Tương tác của Agent:**
                * ` LearningAndOptimizationAgent`: Có thể truy vấn Snowflake để phân tích sâu về hiệu suất hệ thống và đề xuất các cải tiến dựa trên dữ liệu lịch sử quy mô lớn.
                *   Dữ liệu từ Neo4j và Supabase có thể được ETL (Extract, Transform, Load) vào Snowflake định kỳ.

        * **4. Lưu trữ Đối tượng (Object Storage - ví dụ: AWS S3, Google Cloud Storage, Supabase Storage):**
            * **Vai trò Chính:** Lưu trữ các file lớn, dữ liệu phi cấu trúc như tài liệu gốc, hình ảnh, video, bản ghi âm, log file chi tiết, các model artifact (trọng số mô hình AI).
            * **Lý do lựa chọn:** Chi phí thấp, khả năng mở rộng cao, độ bền tốt.
            * **Tương tác của Agent:**
                * ` DataIngestionAgent`: Lưu trữ các file đầu vào.
                *   Các agent có thể truy cập các file này thông qua URL hoặc SDK.

        * **Luồng Dữ liệu và Tích hợp:**
            * **Ontology là trung tâm:** Neo4j Aura chứa mô hình khái niệm và các mối quan hệ cốt lõi.
            * **Dữ liệu vận hành và Vector:** Supabase lưu trữ dữ liệu hoạt động hàng ngày và các embedding cho tìm kiếm ngữ nghĩa. Các embedding này có thể được liên kết với các nút trong Neo4j (ví dụ: một `DocumentNode` trong Neo4j có thể có một thuộc tính là ID của embedding tương ứng trong Supabase Vector).
            * **Dữ liệu phân tích:** Dữ liệu từ Neo4j và Supabase có thể được tổng hợp và chuyển vào Snowflake để phân tích sâu hơn.
            * **File lớn:** Được lưu trữ trong Object Storage và được tham chiếu từ Neo4j hoặc Supabase.

        Việc lựa chọn này nhằm đảm bảo mỗi loại dữ liệu được lưu trữ và xử lý bằng công nghệ phù hợp nhất, đồng thời cho phép tích hợp chặt chẽ giữa các hệ thống để cung cấp một nền tảng tri thức toàn diện cho các AI agent.
    **10.4.5. Ngôn ngữ Lập trình (Python):**

        Việc lựa chọn ngôn ngữ lập trình chính cho việc phát triển các AI agent và các thành phần cốt lõi của TRM-OS là một quyết định quan trọng, ảnh hưởng đến năng suất phát triển, khả năng bảo trì, hiệu suất và khả năng tiếp cận hệ sinh thái công cụ AI.

        * **1. Python (Ngôn ngữ Chính):**
            * **Vai trò Chính:** Python được chọn là ngôn ngữ lập trình chủ đạo cho việc phát triển hầu hết các AI agent, các thư viện xử lý ngôn ngữ tự nhiên (NLP), các mô hình học máy (ML), các kịch bản tự động hóa, và các API backend của TRM-OS.
            * **Lý do lựa chọn:**
                * **Hệ sinh thái AI/ML Phong phú:** Python sở hữu một bộ sưu tập khổng lồ các thư viện và framework mạnh mẽ cho AI và ML, bao gồm TensorFlow, PyTorch, scikit-learn, spaCy, NLTK, Transformers (Hugging Face), LangChain, CrewAI, AutoGen, Pandas, NumPy, và nhiều hơn nữa. Điều này giúp tăng tốc đáng kể quá trình phát triển.
                * **Cú pháp Đơn giản và Dễ đọc:** Cú pháp của Python gần giống với ngôn ngữ tự nhiên, giúp dễ học, dễ viết và dễ bảo trì code. Điều này đặc biệt quan trọng cho các dự án phức tạp và có sự tham gia của nhiều nhà phát triển.
                * **Cộng đồng Lớn và Hỗ trợ Tích cực:** Python có một cộng đồng phát triển viên toàn cầu đông đảo và năng động, cung cấp nguồn tài liệu phong phú, các diễn đàn hỗ trợ, và các giải pháp cho hầu hết các vấn đề thường gặp.
                * **Khả năng Tích hợp Cao:** Python dễ dàng tích hợp với các ngôn ngữ và hệ thống khác thông qua API, FFI (Foreign Function Interface), hoặc các message queue.
                * **Phù hợp cho Prototyping Nhanh:** Python cho phép phát triển và thử nghiệm ý tưởng một cách nhanh chóng, rất quan trọng trong lĩnh vực AI nơi các thử nghiệm thường xuyên là cần thiết.
                * **Hỗ trợ Đa nền tảng:** Python chạy trên hầu hết các hệ điều hành phổ biến.
                * **Hỗ trợ bởi các Công cụ Phát triển Hiện đại:** Các IDE như VS Code, PyCharm cung cấp hỗ trợ tuyệt vời cho Python, bao gồm gỡ lỗi, gợi ý code, và quản lý dự án. CursorAI/WindsurfAI cũng có khả năng sinh code Python chất lượng cao.
            * **Ứng dụng trong TRM-OS:**
                *   Xây dựng logic cốt lõi của tất cả các AI agent.
                *   Xử lý dữ liệu, tiền xử lý văn bản, trích xuất đặc trưng.
                *   Tương tác với các mô hình AI (LLMs, embedding models, GNNs).
                *   Kết nối và thao tác với các cơ sở dữ liệu (Neo4j, Supabase, Snowflake).
                *   Xây dựng các API endpoint cho giao tiếp giữa các agent hoặc với các hệ thống bên ngoài.
                *   Các kịch bản tự động hóa và điều phối tác vụ.

        * **2. Các Ngôn ngữ Khác (Tiềm năng cho các Thành phần Chuyên biệt):**
            * **JavaScript/TypeScript (Cho Frontend và một số Backend Services):**
                *   Nếu TRM-OS có giao diện người dùng web, JavaScript/TypeScript (với các framework như React, Vue, Angular) sẽ là lựa chọn tự nhiên.
                *   Node.js có thể được sử dụng cho một số microservices I/O-bound hoặc các tác vụ backend yêu cầu hiệu suất cao trong xử lý bất đồng bộ.
            * **Ngôn ngữ Hiệu suất Cao (ví dụ: Rust, Go, C++ - Cho các Module Cực kỳ Nhạy cảm về Hiệu suất):**
                *   Trong trường hợp có các thành phần yêu cầu xử lý tốc độ cực cao hoặc tối ưu hóa tài nguyên ở mức độ thấp (ví dụ: một số thuật toán cốt lõi trong GNNs, hoặc các module xử lý dữ liệu thời gian thực với độ trễ cực thấp), các ngôn ngữ này có thể được xem xét. Tuy nhiên, việc này sẽ làm tăng độ phức tạp của hệ thống và yêu cầu kỹ năng chuyên biệt.
                *   Quyết định sử dụng các ngôn ngữ này sẽ được cân nhắc kỹ lưỡng dựa trên yêu cầu cụ thể và lợi ích mang lại so với chi phí phát triển và bảo trì.

        * **Định hướng Chính:**
            *   Ưu tiên hàng đầu là Python cho toàn bộ hệ sinh thái AI agent và các dịch vụ liên quan để đảm bảo tính đồng nhất, dễ phát triển và tận dụng tối đa hệ sinh thái AI hiện có.
            *   Việc sử dụng các ngôn ngữ khác sẽ được giới hạn ở các trường hợp thực sự cần thiết và có lý do chính đáng, với các giao diện tích hợp rõ ràng với phần còn lại của hệ thống dựa trên Python.

        Sự lựa chọn này nhằm tối ưu hóa tốc độ phát triển, khả năng bảo trì, và khả năng tận dụng các công nghệ AI tiên tiến nhất cho TRM-OS.
    **10.4.6. Hạ tầng Vận hành và Giám sát (Cloud-based, Serverless, Managed Services):**

        Hạ tầng vận hành và giám sát đóng vai trò then chốt trong việc đảm bảo các AI agent của TRM-OS hoạt động ổn định, hiệu quả, an toàn và có khả năng mở rộng. Định hướng chính là ưu tiên sử dụng các giải pháp cloud-based, serverless và managed services để giảm thiểu gánh nặng quản trị hạ tầng, tập trung vào phát triển tính năng và logic nghiệp vụ của agent.

        * **1. Nền tảng Đám mây (Cloud Platform - Ưu tiên AWS, GCP, hoặc Azure):**
            * **Vai trò Chính:** Cung cấp toàn bộ các dịch vụ hạ tầng cần thiết từ máy chủ ảo, lưu trữ, cơ sở dữ liệu, mạng, đến các dịch vụ AI/ML chuyên biệt.
            * **Lý do lựa chọn:**
                * **Khả năng Mở rộng Linh hoạt:** Dễ dàng tăng hoặc giảm tài nguyên theo nhu cầu thực tế.
                * **Tính Sẵn sàng Cao và Độ tin cậy:** Các nhà cung cấp đám mây lớn đảm bảo uptime cao và cơ chế phục hồi sau thảm họa.
                * **Hệ sinh thái Dịch vụ Phong phú:** Cung cấp đa dạng các managed services giúp tăng tốc phát triển.
                * **Bảo mật Toàn diện:** Các biện pháp bảo mật tiên tiến ở nhiều lớp.
                * **Chi phí Tối ưu (Pay-as-you-go):** Chỉ trả tiền cho những gì sử dụng.
            * **Chiến lược:** Có thể bắt đầu với một nhà cung cấp chính (ví dụ: AWS do sự phổ biến và hệ sinh thái AI/ML mạnh mẽ) và xem xét chiến lược multi-cloud hoặc cloud-agnostic cho các thành phần quan trọng trong tương lai để tránh vendor lock-in và tối ưu chi phí/hiệu năng.

        * **2. Dịch vụ Tính toán (Compute Services):**
            * **Serverless Functions (ví dụ: AWS Lambda, Google Cloud Functions, Azure Functions):**
                * **Vai trò:** Lý tưởng cho các tác vụ agent có tính chất event-driven, xử lý ngắn hạn, hoặc các API endpoint đơn giản. Ví dụ: một agent phản hồi một sự kiện từ message queue, một agent thực hiện một tác vụ nhỏ theo lịch trình.
                * **Lợi ích:** Tự động mở rộng, không cần quản lý server, chi phí dựa trên số lần thực thi.
            * **Containerization (Docker, Kubernetes - ví dụ: Amazon EKS, Google GKE, Azure AKS):**
                * **Vai trò:** Triển khai các AI agent phức tạp, các ứng dụng backend, hoặc các dịch vụ yêu cầu tài nguyên lớn, chạy dài hạn. Đảm bảo tính nhất quán môi trường giữa phát triển, kiểm thử và sản xuất.
                * **Lợi ích:** Khả năng đóng gói ứng dụng và dependencies, quản lý vòng đời ứng dụng, tự động phục hồi, cân bằng tải.
            * **Managed AI/ML Platforms (ví dụ: Amazon SageMaker, Google Vertex AI, Azure Machine Learning):**
                * **Vai trò:** Hỗ trợ toàn bộ vòng đời của các mô hình AI/ML, từ chuẩn bị dữ liệu, huấn luyện, triển khai (hosting model endpoints), đến giám sát.
                * **Lợi ích:** Tối ưu hóa cho các tác vụ AI/ML, tích hợp sẵn các công cụ và framework phổ biến, giảm thiểu công sức thiết lập và quản lý hạ tầng ML.

        * **3. Hệ thống Tin nhắn và Sự kiện (Messaging/Eventing Systems - ví dụ: Apache Kafka, RabbitMQ, AWS SQS/SNS, Google Pub/Sub, Azure Service Bus):**
            * **Vai trò Chính:** Cho phép giao tiếp bất đồng bộ và đáng tin cậy giữa các AI agent, giữa agent và các dịch vụ khác. Hỗ trợ kiến trúc event-driven.
            * **Lý do lựa chọn:**
                * **Khớp nối Lỏng (Loose Coupling):** Các agent không cần biết trực tiếp về nhau.
                * **Khả năng Mở rộng:** Dễ dàng thêm các producer hoặc consumer mới.
                * **Độ bền (Durability):** Đảm bảo tin nhắn không bị mất.
                * **Xử lý Tải Cao điểm:** Giúp làm mịn tải bằng cách đưa tin nhắn vào hàng đợi.
            * **Ứng dụng:** `EventDispatcherAgent` có thể sử dụng các hệ thống này để phân phối sự kiện đến các agent liên quan.

        * **4. API Gateway (ví dụ: Amazon API Gateway, Google Cloud API Gateway, Azure API Management):**
            * **Vai trò Chính:** Quản lý, bảo mật, giám sát và điều phối các API endpoint do các AI agent hoặc dịch vụ backend cung cấp.
            * **Lý do lựa chọn:**
                * **Bảo mật:** Xác thực, ủy quyền, giới hạn tốc độ (rate limiting), chống tấn công DDoS.
                * **Quản lý Phiên bản API.**
                * **Giám sát và Logging Request.**
                * **Tích hợp với Serverless Functions và các backend khác.**

        * **5. CI/CD (Continuous Integration/Continuous Deployment):**
            * **Công cụ (ví dụ: GitHub Actions, GitLab CI/CD, Jenkins, AWS CodePipeline):** Tự động hóa quy trình xây dựng, kiểm thử và triển khai code của agent.
            * **Thực hành:**
                *   Mỗi thay đổi code được tự động build và chạy unit test, integration test.
                *   Triển khai tự động lên các môi trường (dev, staging, production) sau khi kiểm thử thành công.
                *   Đảm bảo chất lượng code và giảm thiểu lỗi do con người.

        * **6. Giám sát, Ghi log và Cảnh báo (Monitoring, Logging, Alerting):**
            * **Ghi log (Logging):**
                * **Giải pháp:** Centralized logging (ví dụ: ELK Stack - Elasticsearch, Logstash, Kibana; Splunk; AWS CloudWatch Logs; Google Cloud Logging).
                * **Mục tiêu:** Thu thập log từ tất cả các agent và dịch vụ vào một nơi tập trung để dễ dàng tìm kiếm, phân tích và gỡ lỗi.
            * **Giám sát (Monitoring):**
                * **Giải pháp:** Prometheus, Grafana, Datadog, AWS CloudWatch Metrics, Google Cloud Monitoring.
                * **Mục tiêu:** Theo dõi các chỉ số hiệu suất (CPU, memory, network, latency), tình trạng hoạt động của agent, số lượng tác vụ xử lý, tỷ lệ lỗi.
            * **Cảnh báo (Alerting):**
                * **Giải pháp:** Tích hợp với các công cụ giám sát (ví dụ: Alertmanager cho Prometheus, CloudWatch Alarms) hoặc các dịch vụ chuyên biệt (PagerDuty, Opsgenie).
                * **Mục tiêu:** Thông báo ngay lập tức cho đội vận hành khi có sự cố nghiêm trọng hoặc các chỉ số vượt ngưỡng cho phép.

        * **7. Bảo mật (Security):**
            * **Quản lý Danh tính và Truy cập (IAM - Identity and Access Management):** Kiểm soát chặt chẽ quyền truy cập vào tài nguyên đám mây và các dịch vụ của TRM-OS. Nguyên tắc đặc quyền tối thiểu (least privilege).
            * **Quản lý Bí mật (Secrets Management - ví dụ: HashiCorp Vault, AWS Secrets Manager, Google Secret Manager, Azure Key Vault):** Lưu trữ và quản lý an toàn các thông tin nhạy cảm như API key, mật khẩu cơ sở dữ liệu.
            * **Bảo mật Mạng:** Sử dụng Virtual Private Clouds (VPCs), subnets, security groups, network ACLs, firewalls để cô lập tài nguyên và kiểm soát luồng truy cập mạng.
            * **Mã hóa Dữ liệu:** Mã hóa dữ liệu khi lưu trữ (at rest) và khi truyền (in transit) sử dụng các tiêu chuẩn mạnh.

        * **8. Hạ tầng dưới dạng Mã (Infrastructure as Code - IaC):**
            * **Công cụ (ví dụ: Terraform, AWS CloudFormation, Azure Resource Manager, Google Cloud Deployment Manager, Pulumi):** Định nghĩa và quản lý hạ tầng bằng code, cho phép tự động hóa việc tạo, cập nhật và xóa tài nguyên hạ tầng.
            * **Lợi ích:** Tính nhất quán, khả năng tái sử dụng, kiểm soát phiên bản cho hạ tầng, giảm thiểu lỗi thủ công.

        * **9. Ưu tiên Managed Services:**
            *   Như đã đề cập trong các nguyên tắc lựa chọn công nghệ (10.4.1), việc ưu tiên sử dụng các dịch vụ được quản lý (managed services) cho cơ sở dữ liệu, message queue, AI/ML platforms, v.v., giúp đội ngũ TRM tập trung vào phát triển giá trị cốt lõi thay vì vận hành hạ tầng phức tạp.

        Việc thiết kế và triển khai một hạ tầng vận hành và giám sát mạnh mẽ, linh hoạt và an toàn là yếu tố sống còn cho sự thành công và bền vững của hệ thống AI agent TRM-OS.

### 10.5. Tham chiếu đến các Luồng Tác vụ Chi tiết của AI Agent

Mục này cung cấp các ví dụ minh họa về các luồng tác vụ (workflows) chi tiết, mô tả cách các AI agent trong TRM-OS phối hợp hoạt động để thực hiện các chức năng nghiệp vụ cốt lõi. Các luồng tác vụ này làm rõ sự tương tác giữa các agent, cách chúng sử dụng và cập nhật ontology, cách chúng xử lý dữ liệu và các sự kiện, cũng như cách chúng giao tiếp với người dùng và các hệ thống bên ngoài. Việc hiểu rõ các luồng tác vụ này là rất quan trọng để thiết kế, phát triển, và kiểm thử các agent một cách hiệu quả, đảm bảo tính nhất quán và hiệu năng của toàn bộ hệ thống TRM-OS.

Mỗi luồng tác vụ sẽ được mô tả bao gồm các yếu tố chính sau:
*   **Tên Luồng Tác vụ:** Mô tả ngắn gọn mục tiêu của luồng.
*   **Agents Tham Gia:** Liệt kê các AI agent chính tham gia vào luồng tác vụ.
*   **Điều Kiện Kích Hoạt (Trigger):** Sự kiện hoặc hành động khởi đầu luồng tác vụ.
*   **Mục Tiêu:** Kết quả mong đợi khi luồng tác vụ hoàn thành.
*   **Luồng Các Bước Thực Hiện Chi Tiết:** Mô tả tuần tự các hành động, quyết định, và tương tác.
*   **Tương Tác Dữ liệu và Ontology:** Cách các agent truy vấn, cập nhật Neo4j Aura, Supabase, và các kho dữ liệu khác.
*   **Sự Kiện Phát Sinh:** Các sự kiện quan trọng được tạo ra và truyền đi trong quá trình thực hiện.
*   **Ví dụ Minh Họa Cụ Thể:** Một kịch bản ví dụ để làm rõ luồng tác vụ.

#### 10.5.1. Luồng Tác vụ 1: Tiếp nhận, Xử lý và Phân tích Sơ bộ một WIN (What's Important Now) mới

*   **Agents Tham Gia:**
    * ` UserInteractionAgent`
    * ` DataIngestionAgent`
    * ` KnowledgeExtractionAgent`
    * ` OntologyManagementAgent`
    * ` EventDispatcherAgent`
*   **Điều Kiện Kích Hoạt (Trigger):** Người dùng (ví dụ: CEO, Quản lý Dự án) tạo một WIN mới thông qua giao diện người dùng của TRM-OS.
*   **Mục Tiêu:**
    *   WIN mới được ghi nhận vào hệ thống một cách an toàn và đầy đủ.
    *   Nội dung của WIN được phân tích sơ bộ để trích xuất các thực thể, mối quan hệ và ý định chính.
    *   Các thông tin trích xuất được ánh xạ và lưu trữ vào Ontology TRM-OS (Neo4j Aura).
    *   Các agent liên quan được thông báo về sự xuất hiện của WIN mới để có thể thực hiện các hành động tiếp theo.
*   **Luồng Các Bước Thực Hiện Chi Tiết:**
    1.  **Tiếp nhận WIN từ Người dùng (`UserInteractionAgent`):**
        *   Người dùng nhập thông tin chi tiết cho WIN mới qua giao diện (ví dụ: tiêu đề, mô tả, mức độ ưu tiên, người khởi tạo, các tài liệu/liên kết liên quan).
        * ` UserInteractionAgent` thu thập thông tin, xác thực dữ liệu đầu vào cơ bản (ví dụ: các trường bắt buộc).
        * ` UserInteractionAgent` tạo một `NewWINSubmittedEvent` chứa toàn bộ dữ liệu WIN và gửi nó đến `EventDispatcherAgent`.
    2.  **Điều phối Sự kiện (`EventDispatcherAgent`):**
        * ` EventDispatcherAgent` nhận `NewWINSubmittedEvent`.
        *   Dựa trên loại sự kiện, `EventDispatcherAgent` chuyển tiếp sự kiện này đến `DataIngestionAgent`.
    3.  **Lưu trữ Dữ liệu Thô và Phi cấu trúc (`DataIngestionAgent`):**
        * ` DataIngestionAgent` nhận `NewWINSubmittedEvent`.
        *   Lưu trữ nội dung mô tả chi tiết của WIN và các tài liệu đính kèm (nếu có) vào một kho lưu trữ phù hợp (ví dụ: Supabase Storage cho file, hoặc một bảng trong Supabase PostgreSQL cho nội dung text dài). Gán một ID duy nhất cho WIN.
        *   Tạo vector embedding cho nội dung WIN (sử dụng `EmbeddingModelInterface`) và lưu vào Supabase Vector để phục vụ tìm kiếm ngữ nghĩa sau này.
        *   Sau khi lưu trữ thành công, `DataIngestionAgent` phát một sự kiện `WINDataStoredEvent` chứa ID của WIN và đường dẫn/tham chiếu đến dữ liệu đã lưu, gửi đến `EventDispatcherAgent`.
    4.  **Điều phối Sự kiện (`EventDispatcherAgent`):**
        * ` EventDispatcherAgent` nhận `WINDataStoredEvent`.
        *   Chuyển tiếp sự kiện này đến `KnowledgeExtractionAgent` và `OntologyManagementAgent`.
    5.  **Trích xuất Tri thức từ WIN (`KnowledgeExtractionAgent`):**
        * ` KnowledgeExtractionAgent` nhận `WINDataStoredEvent`.
        *   Truy xuất nội dung WIN từ nơi lưu trữ (Supabase).
        *   Sử dụng các mô hình AI (LLMs, NER models thông qua `LLMInterfaceAgent` hoặc các service chuyên biệt) để:
            *   Phân tích nội dung WIN, xác định các thực thể quan trọng (ví dụ: dự án, mục tiêu, rủi ro, các bên liên quan, nguồn lực được đề cập).
            *   Nhận diện các mối quan hệ tiềm năng giữa các thực thể này và với các thực thể đã có trong ontology.
            *   Phân loại ý định chính của WIN (ví dụ: đề xuất một mục tiêu mới, báo cáo một rủi ro, yêu cầu một nguồn lực).
        * ` KnowledgeExtractionAgent` tạo ra một `WINKnowledgeExtractedEvent` chứa các thực thể, mối quan hệ, và ý định đã được trích xuất, cùng với ID của WIN gốc, gửi đến `EventDispatcherAgent`.
    6.  **Điều phối Sự kiện (`EventDispatcherAgent`):**
        * ` EventDispatcherAgent` nhận `WINKnowledgeExtractedEvent`.
        *   Chuyển tiếp sự kiện này đến `OntologyManagementAgent`.
    7.  **Cập nhật Ontology (`OntologyManagementAgent`):**
        * ` OntologyManagementAgent` nhận `WINDataStoredEvent` (để tạo nút WIN cơ bản) và `WINKnowledgeExtractedEvent` (để làm giàu nút WIN và tạo các liên kết).
        * **Tạo nút WIN:** Dựa trên `WINDataStoredEvent`, tạo một nút `WIN` mới trong Neo4j Aura với các thuộc tính cơ bản (ID, tiêu đề, mô tả tóm tắt, người tạo, ngày tạo, trạng thái ban đầu là "Mới"). Liên kết nút `WIN` này với nút `User` đã tạo ra nó.
        * **Liên kết tri thức:** Dựa trên `WINKnowledgeExtractedEvent`:
            *   Đối với mỗi thực thể được trích xuất, kiểm tra xem nó đã tồn tại trong ontology chưa. Nếu chưa, tạo nút mới (ví dụ: `PotentialGoal`, `PotentialRisk`). Nếu đã có, sử dụng nút hiện tại.
            *   Tạo các mối quan hệ (ví dụ: `RELATES_TO`, `MENTIONS_PROJECT`, `SUGGESTS_GOAL`) giữa nút `WIN` và các nút thực thể này.
            *   Cập nhật các thuộc tính của nút `WIN` với các thông tin phân tích được (ví dụ: ý định chính, mức độ ưu tiên suy luận được).
        *   Sau khi cập nhật ontology thành công, `OntologyManagementAgent` phát một sự kiện `WINProcessedInOntologyEvent` (chứa WIN ID), gửi đến `EventDispatcherAgent`.
    8.  **Thông báo Hoàn tất Xử lý Sơ bộ (`EventDispatcherAgent` và các Agent khác):**
        * ` EventDispatcherAgent` nhận `WINProcessedInOntologyEvent`.
        *   Thông báo này có thể được chuyển tiếp đến các agent khác quan tâm đến WIN mới, ví dụ:
            * ` StrategicAlignmentAgent`: Để bắt đầu đánh giá sự phù hợp của WIN với các mục tiêu chiến lược hiện tại.
            * ` NotificationAgent`: Để thông báo cho người dùng liên quan (ví dụ: người quản lý của người tạo WIN) rằng WIN đã được ghi nhận và đang được xử lý.
            * ` UserInteractionAgent`: Để cập nhật trạng thái của WIN trên giao diện người dùng.
*   **Tương Tác Dữ liệu và Ontology:**
    *   **Supabase PostgreSQL/Storage:** Lưu trữ nội dung chi tiết của WIN, tài liệu đính kèm.
    *   **Supabase Vector:** Lưu trữ vector embedding của nội dung WIN.
    *   **Neo4j Aura:**
        *   Tạo nút `WIN` mới.
        *   Liên kết nút `WIN` với `User` (người tạo).
        *   Tạo/liên kết các nút `Entity` (ví dụ: `Goal`, `Project`, `Risk`, `Resource`) được đề cập trong WIN.
        *   Tạo các `Relation` giữa nút `WIN` và các `Entity` này.
        *   Cập nhật thuộc tính (ví dụ: `status`, `priority`, `extractedIntent`) cho nút `WIN`.
*   **Sự Kiện Phát Sinh (Ví dụ):**
    * ` NewWINSubmittedEvent`
    * ` WINDataStoredEvent`
    * ` WINKnowledgeExtractedEvent`
    * ` WINProcessedInOntologyEvent`
    * ` NotificationEvent` (cho người dùng)
*   **Ví dụ Minh Họa Cụ Thể:**
    *   **Người dùng:** CEO Trần Văn A.
    *   **WIN Input:**
        *   Tiêu đề: "Nghiên cứu ứng dụng AI để tối ưu hóa quy trình chăm sóc khách hàng."
        *   Mô tả: "Hiện tại quy trình CSKH đang tốn nhiều thời gian và nhân lực. Đề xuất phòng R&D nghiên cứu các giải pháp AI (chatbot, phân tích cảm xúc) để giảm thời gian phản hồi và tăng sự hài lòng của khách hàng. Dự kiến hoàn thành nghiên cứu trong Q3. Cần phân bổ 2 nhân sự R&D."
        *   Ưu tiên: Cao.
    *   **Kết quả (trong Ontology sau khi xử lý):**
        *   Một nút `WIN` mới được tạo, liên kết với `User` "Trần Văn A".
        *   Nút `WIN` này có thể liên kết với:
            *   Một nút `PotentialGoal` "Tối ưu hóa quy trình CSKH".
            *   Một nút `Technology` "AI", "Chatbot", "Phân tích cảm xúc".
            *   Một nút `Department` "R&D".
            *   Một nút `ResourceRequirement` "2 nhân sự R&D".
            *   Một nút `TimeConstraint` "Q3".
        *   Trạng thái của WIN được cập nhật thành "Đã xử lý sơ bộ".
        * ` StrategicAlignmentAgent` nhận được thông báo để bắt đầu phân tích WIN này.

#### 10.5.2. Luồng Tác vụ 2: Phân tích Tính phù hợp Chiến lược của một WIN mới

*   **Agents Tham Gia:**
    * ` StrategicAlignmentAgent`
    * ` OntologyManagementAgent`
    * ` KnowledgeExtractionAgent` (có thể được gọi lại nếu cần làm rõ thêm WIN)
    * ` UserInteractionAgent` (để yêu cầu làm rõ từ người dùng nếu cần)
    * ` NotificationAgent`
    * ` EventDispatcherAgent`
*   **Điều Kiện Kích Hoạt (Trigger):** `StrategicAlignmentAgent` nhận được `WINProcessedInOntologyEvent` (hoặc một sự kiện tương tự như `NewWINRequiresStrategicAlignmentEvent`) cho một WIN mới từ `EventDispatcherAgent`.
*   **Mục Tiêu:**
    *   Đánh giá mức độ phù hợp của WIN mới với các Mục tiêu Chiến lược (`StrategicGoal`), Sáng kiến Chiến lược (`StrategicInitiative`), và Rủi ro Chiến lược (`StrategicRisk`) hiện tại của tổ chức, được định nghĩa trong Ontology.
    *   Xác định các xung đột hoặc синергии (synergies) tiềm năng.
    *   Cung cấp một báo cáo phân tích sơ bộ về tính phù hợp chiến lược.
    *   Cập nhật trạng thái của WIN trong ontology với kết quả phân tích.
    *   Thông báo cho các bên liên quan về kết quả phân tích.
*   **Luồng Các Bước Thực Hiện Chi Tiết:**
    1.  **Tiếp nhận Yêu cầu Phân tích (`StrategicAlignmentAgent`):**
        * ` StrategicAlignmentAgent` nhận sự kiện (ví dụ: `WINProcessedInOntologyEvent` hoặc `NewWINRequiresStrategicAlignmentEvent`) từ `EventDispatcherAgent`, chứa WIN ID.
    2.  **Truy xuất Thông tin WIN và Bối cảnh Chiến lược (`StrategicAlignmentAgent` & `OntologyManagementAgent`):**
        * ` StrategicAlignmentAgent` yêu cầu `OntologyManagementAgent` cung cấp chi tiết về WIN (nội dung, các thực thể liên quan đã được trích xuất từ bước 10.5.1) và các `StrategicGoal`, `StrategicInitiative`, `StrategicRisk` hiện hành từ Neo4j Aura.
        * ` OntologyManagementAgent` truy vấn Neo4j và trả về dữ liệu cần thiết.
    3.  **Phân tích Mức độ Phù hợp (`StrategicAlignmentAgent`):**
        *   Sử dụng các kỹ thuật NLP/NLU (thông qua `LLMInterfaceAgent` hoặc gọi lại `KnowledgeExtractionAgent` nếu cần xử lý sâu hơn về ngữ nghĩa của WIN trong bối cảnh chiến lược) và logic dựa trên ontology để:
            *   So sánh các thực thể, từ khóa, và ý định của WIN với mô tả, mục tiêu, và KPI của các `StrategicGoal` và `StrategicInitiative`.
            *   Đánh giá xem WIN có đóng góp vào việc đạt được mục tiêu nào, hoặc có thể cản trở mục tiêu nào không.
            *   Xác định xem WIN có liên quan đến các `StrategicRisk` đã biết hay không (ví dụ: làm tăng nguy cơ, hoặc giúp giảm thiểu nguy cơ).
            *   Sử dụng vector embeddings (của WIN và các mục tiêu/sáng kiến chiến lược đã được tính toán trước và lưu trữ) để tính toán độ tương đồng ngữ nghĩa, hỗ trợ việc đánh giá.
            *   Phân loại mức độ phù hợp: Rất phù hợp, Phù hợp, Trung tính, Không phù hợp, Xung đột. Gán điểm số phù hợp nếu có thể.
    4.  **Xử lý Trường hợp Thông tin Không Đủ (`StrategicAlignmentAgent`, `UserInteractionAgent`, `EventDispatcherAgent`):**
        *   Nếu thông tin trong WIN hoặc ontology không đủ để `StrategicAlignmentAgent` đưa ra đánh giá rõ ràng:
            * ` StrategicAlignmentAgent` tạo một `ClarificationRequiredEvent` (chứa WIN ID và câu hỏi cần làm rõ) gửi đến `EventDispatcherAgent`.
            * ` EventDispatcherAgent` chuyển sự kiện này đến `UserInteractionAgent`.
            * ` UserInteractionAgent` thông báo cho người tạo WIN (hoặc người có thẩm quyền được xác định qua ontology) yêu cầu cung cấp thêm thông tin hoặc làm rõ các điểm cụ thể.
            *   Luồng phân tích chiến lược cho WIN này có thể tạm dừng chờ phản hồi, hoặc tiếp tục với đánh giá sơ bộ dựa trên thông tin hiện có, đồng thời đánh dấu trạng thái WIN là "Cần làm rõ về mặt chiến lược".
    5.  **Tạo Báo cáo Phân tích và Yêu cầu Cập nhật Ontology (`StrategicAlignmentAgent`):**
        * ` StrategicAlignmentAgent` tổng hợp kết quả phân tích thành một cấu trúc dữ liệu (ví dụ: JSON) chứa báo cáo, bao gồm:
            *   Đánh giá tổng quan về mức độ phù hợp (ví dụ: "Rất phù hợp", "Xung đột nhẹ").
            *   Điểm số phù hợp (nếu có).
            *   Các `StrategicGoal`/`StrategicInitiative` cụ thể mà WIN hỗ trợ hoặc xung đột, kèm theo lý giải.
            *   Các `StrategicRisk` liên quan và mức độ ảnh hưởng dự kiến của WIN lên chúng.
            *   Đề xuất (nếu có) về việc điều chỉnh WIN để tăng tính phù hợp hoặc giảm xung đột.
        * ` StrategicAlignmentAgent` gửi yêu cầu cập nhật ontology đến `OntologyManagementAgent` kèm theo dữ liệu phân tích này và WIN ID.
    6.  **Cập nhật Ontology với Kết quả Phân tích (`OntologyManagementAgent`):**
        * ` OntologyManagementAgent` nhận yêu cầu từ `StrategicAlignmentAgent`.
        *   Cập nhật nút `WIN` tương ứng trong Neo4j Aura:
            *   Lưu trữ báo cáo phân tích chi tiết (có thể dưới dạng thuộc tính JSON hoặc liên kết đến một bản ghi báo cáo riêng nếu phức tạp).
            *   Cập nhật các thuộc tính như `strategicAlignmentScore`, `strategicAlignmentStatus` (ví dụ: "Phù hợp cao", "Cần xem xét thêm", "Xung đột"), `strategicAlignmentRationale`.
            *   Tạo hoặc cập nhật các mối quan hệ cụ thể, ví dụ: `ALIGNS_WITH (StrategicGoal)`, `CONFLICTS_WITH (StrategicGoal)`, `SUPPORTS (StrategicInitiative)`, `IMPACTS (StrategicRisk)` với các thuộc tính mô tả chi tiết hơn về mối liên hệ (ví dụ: mức độ hỗ trợ, loại xung đột).
        *   Sau khi cập nhật thành công, `OntologyManagementAgent` phát một sự kiện `WINStrategicAnalysisCompletedEvent` (chứa WIN ID và tóm tắt kết quả phân tích) gửi đến `EventDispatcherAgent`.
    7.  **Thông báo Kết quả Phân tích (`EventDispatcherAgent`, `NotificationAgent`, `UserInteractionAgent`):**
        * ` EventDispatcherAgent` nhận `WINStrategicAnalysisCompletedEvent`.
        *   Chuyển tiếp sự kiện này đến `NotificationAgent` và `UserInteractionAgent`.
        * ` NotificationAgent` thông báo cho các bên liên quan (ví dụ: người tạo WIN, quản lý danh mục đầu tư, các thành viên ban chiến lược được định nghĩa trong ontology) về kết quả phân tích. Thông báo có thể bao gồm tóm tắt và liên kết đến báo cáo chi tiết.
        * ` UserInteractionAgent` cập nhật trạng thái và kết quả phân tích chiến lược của WIN trên giao diện người dùng.
*   **Tương Tác Dữ liệu và Ontology:**
    *   **Neo4j Aura:**
        *   Đọc thông tin chi tiết của nút `WIN` và các thực thể liên quan đã được xử lý ở bước 10.5.1.
        *   Đọc thông tin về các nút `StrategicGoal`, `StrategicInitiative`, `StrategicRisk` và các mối quan hệ của chúng.
        *   Cập nhật nút `WIN` với kết quả phân tích chiến lược (báo cáo, điểm số, trạng thái, lý giải).
        *   Tạo/cập nhật các mối quan hệ định tính và định lượng giữa `WIN` và các thực thể chiến lược.
    *   **Supabase Vector (Tùy chọn):** Có thể được `StrategicAlignmentAgent` sử dụng để truy vấn các WIN tương tự đã được phân tích trước đó, hoặc các tài liệu chiến lược liên quan (nếu có) dựa trên vector embeddings để tìm kiếm sự tương đồng hoặc các mẫu hình.
*   **Sự Kiện Phát Sinh (Ví dụ):**
    * ` WINProcessedInOntologyEvent` (hoặc `NewWINRequiresStrategicAlignmentEvent`) (đầu vào)
    * ` ClarificationRequiredEvent` (nếu cần làm rõ thông tin)
    * ` OntologyUpdateRequest` (từ `StrategicAlignmentAgent` đến `OntologyManagementAgent`)
    * ` WINStrategicAnalysisCompletedEvent` (đầu ra từ `OntologyManagementAgent`)
    * ` NotificationEvent` (thông báo kết quả cho người dùng)
*   **Ví dụ Minh Họa Cụ Thể:**
    *   **WIN:** "Nghiên cứu ứng dụng AI để tối ưu hóa quy trình chăm sóc khách hàng." (từ ví dụ 10.5.1, đã được xử lý sơ bộ).
    *   **Bối cảnh Chiến lược (trong Ontology):**
        * ` StrategicGoal` SG01: "Nâng cao trải nghiệm khách hàng lên 20% trong năm 2024." (KPI: CSAT score > 90%, NPS > 50)
        * ` StrategicInitiative` SI03: "Đầu tư vào công nghệ tự động hóa và cá nhân hóa dịch vụ khách hàng."
        * ` StrategicRisk` SR05: "Rủi ro mất thị phần do đối thủ cạnh tranh áp dụng công nghệ mới nhanh hơn trong lĩnh vực CSKH."
    *   **Kết quả Phân tích (do `StrategicAlignmentAgent` thực hiện):**
        *   WIN này được đánh giá là "Rất phù hợp" với SG01 vì tối ưu hóa quy trình CSKH bằng AI trực tiếp góp phần nâng cao trải nghiệm khách hàng.
        *   WIN này "Hỗ trợ mạnh mẽ" cho SI03 vì AI (chatbot, phân tích cảm xúc) là công nghệ tự động hóa và có thể cá nhân hóa dịch vụ.
        *   WIN này có thể "Giảm thiểu đáng kể" SR05 bằng cách giúp TRM chủ động áp dụng công nghệ mới, nâng cao năng lực cạnh tranh trong CSKH.
        *   Điểm phù hợp chiến lược: 9/10.
    *   **Cập nhật Ontology (do `OntologyManagementAgent` thực hiện):**
        *   Nút `WIN` được cập nhật: `strategicAlignmentStatus: "Rất phù hợp"`, `strategicAlignmentScore: 9`, `strategicAlignmentRationale: "WIN hỗ trợ trực tiếp SG01 và SI03, đồng thời giảm thiểu SR05..."`.
        *   Các mối quan hệ được tạo/cập nhật: `WIN -[ALIGNS_WITH {degree: 'High'}]-> SG01`, `WIN -[SUPPORTS {level: 'Strong'}]-> SI03`, `WIN -[MITIGATES {effectiveness: 'Significant'}]-> SR05`.
    *   **Thông báo:** CEO Trần Văn A và Trưởng phòng R&D (người tạo WIN) nhận được thông báo về kết quả phân tích chiến lược tích cực, kèm theo báo cáo chi tiết. Giao diện TRM-OS cập nhật trạng thái của WIN.

#### 10.5.3. Luồng Tác vụ 3: Ưu tiên hóa WIN và Khảo sát Sơ bộ Nguồn lực

*   **Agents Tham Gia:**
    * ` PrioritizationAgent` (hoặc chức năng trong `ResolutionCoordinatorAgent`)
    * ` OntologyManagementAgent`
    * ` ResourceManagementAgent` (để truy vấn thông tin về các loại nguồn lực sẵn có/khả năng)
    * ` KnowledgeExtractionAgent` (để phân tích sâu hơn về yêu cầu nguồn lực từ WIN)
    * ` NotificationAgent`
    * ` EventDispatcherAgent`
*   **Điều Kiện Kích Hoạt (Trigger):** `PrioritizationAgent` nhận được `WINStrategicAnalysisCompletedEvent` cho một WIN đã được đánh giá là phù hợp chiến lược (ví dụ: trạng thái "Phù hợp cao", "Phù hợp") từ `EventDispatcherAgent`. Hoặc, `PrioritizationAgent` có thể định kỳ quét các WIN đã qua phân tích chiến lược.
*   **Mục Tiêu:**
    *   Xác định mức độ ưu tiên tương đối của WIN mới so với các WIN và dự án đang hoạt động/chờ xử lý khác.
    *   Thực hiện khảo sát sơ bộ về các loại nguồn lực chính (nhân lực, tài chính, công nghệ) có thể cần thiết để thực hiện WIN.
    *   Cung cấp một đánh giá ban đầu về mức độ khẩn cấp, tác động tiềm năng, và độ phức tạp/nỗ lực ước tính.
    *   Cập nhật WIN trong ontology với thông tin ưu tiên và yêu cầu nguồn lực sơ bộ.
    *   Thông báo cho các bên liên quan về mức độ ưu tiên và các bước tiếp theo có thể.
*   **Luồng Các Bước Thực Hiện Chi Tiết:**
    1.  **Tiếp nhận WIN cần Ưu tiên (`PrioritizationAgent`):**
        * ` PrioritizationAgent` nhận sự kiện `WINStrategicAnalysisCompletedEvent` (chứa WIN ID và kết quả phân tích chiến lược) từ `EventDispatcherAgent`.
    2.  **Thu thập Thông tin Ngữ cảnh (`PrioritizationAgent`, `OntologyManagementAgent`):**
        * ` PrioritizationAgent` yêu cầu `OntologyManagementAgent` cung cấp:
            *   Chi tiết về WIN (bao gồm kết quả phân tích chiến lược từ 10.5.2).
            *   Thông tin về các `StrategicGoal` mà WIN này hỗ trợ mạnh mẽ nhất.
            *   Danh sách các WIN khác đang chờ xử lý, các `Project` đang hoạt động, cùng với mức độ ưu tiên, trạng thái, và sự liên kết chiến lược của chúng.
            *   Các tiêu chí ưu tiên hóa được định nghĩa trong ontology (ví dụ: trọng số cho mức độ phù hợp chiến lược, ROI dự kiến, mức độ khẩn cấp, giảm thiểu rủi ro).
    3.  **Phân tích và Gán Mức độ Ưu tiên (`PrioritizationAgent`):**
        * ` PrioritizationAgent` sử dụng các tiêu chí ưu tiên và thông tin ngữ cảnh để:
            *   Đánh giá tác động tiềm năng của WIN (ví dụ: đóng góp vào mục tiêu chiến lược, giải quyết vấn đề cấp bách, tạo cơ hội mới).
            *   Ước tính sơ bộ nỗ lực/độ phức tạp (có thể dựa trên phân tích của `KnowledgeExtractionAgent` về mô tả WIN hoặc các WIN tương tự trước đó).
            *   So sánh WIN với các hạng mục công việc khác để xác định vị trí tương đối trong danh sách ưu tiên.
            *   Gán một mức độ ưu tiên (ví dụ: Rất cao, Cao, Trung bình, Thấp) hoặc một điểm số ưu tiên cho WIN.
    4.  **Khảo sát Sơ bộ Nguồn lực (`PrioritizationAgent`, `KnowledgeExtractionAgent`, `ResourceManagementAgent`):**
        * ` PrioritizationAgent` (có thể phối hợp với `KnowledgeExtractionAgent` để phân tích sâu hơn nội dung WIN) xác định các loại nguồn lực chính có thể cần:
            *   Nhân lực: Số lượng, vai trò, kỹ năng chuyên môn (ví dụ: "2 nhân sự R&D AI", "1 Project Manager").
            *   Tài chính: Ước tính ngân sách sơ bộ (nếu có thể từ thông tin WIN hoặc các dự án tương tự).
            *   Công nghệ/Công cụ: Các nền tảng, phần mềm, giấy phép cần thiết.
            *   Thời gian: Khung thời gian dự kiến hoặc deadline (nếu có).
        * ` PrioritizationAgent` có thể truy vấn `ResourceManagementAgent` để có thông tin tổng quan về sự sẵn có hoặc các ràng buộc liên quan đến các loại nguồn lực này (không phải là phân bổ chi tiết ở giai đoạn này).
    5.  **Tạo Báo cáo Ưu tiên và Yêu cầu Cập nhật Ontology (`PrioritizationAgent`):**
        * ` PrioritizationAgent` tổng hợp kết quả thành một báo cáo/cấu trúc dữ liệu, bao gồm:
            *   Mức độ ưu tiên được gán và lý do.
            *   Đánh giá tác động, nỗ lực sơ bộ.
            *   Danh sách các loại nguồn lực chính cần thiết và ước tính sơ bộ.
            *   Đề xuất các bước tiếp theo (ví dụ: đưa vào quy trình lập kế hoạch dự án chi tiết, yêu cầu phân tích sâu hơn về nguồn lực).
        *   Gửi yêu cầu cập nhật ontology đến `OntologyManagementAgent` với thông tin này.
    6.  **Cập nhật Ontology (`OntologyManagementAgent`):**
        * ` OntologyManagementAgent` nhận yêu cầu.
        *   Cập nhật nút `WIN` trong Neo4j Aura với:
            *   Thuộc tính `priorityLevel` (ví dụ: "Cao"), `priorityScore`.
            *   Thuộc tính `estimatedImpact`, `estimatedEffort`.
            *   Thông tin về `preliminaryResourceRequirements` (có thể là một thuộc tính JSON hoặc các liên kết đến các nút `ResourceType` với số lượng ước tính).
        *   Phát sự kiện `WINPrioritizedEvent` (chứa WIN ID, mức ưu tiên, và tóm tắt yêu cầu nguồn lực) đến `EventDispatcherAgent`.
    7.  **Thông báo Kết quả (`EventDispatcherAgent`, `NotificationAgent`, `UserInteractionAgent`):**
        * ` EventDispatcherAgent` nhận `WINPrioritizedEvent`.
        *   Chuyển tiếp đến `NotificationAgent` và `UserInteractionAgent`.
        * ` NotificationAgent` thông báo cho các bên liên quan (ví dụ: người tạo WIN, quản lý danh mục, ban lãnh đạo) về mức độ ưu tiên của WIN và các yêu cầu nguồn lực sơ bộ.
        * ` UserInteractionAgent` cập nhật thông tin ưu tiên và nguồn lực của WIN trên giao diện.
*   **Tương Tác Dữ liệu và Ontology:**
    *   **Neo4j Aura:**
        *   Đọc thông tin WIN, `StrategicGoal`, các WIN/Project khác, tiêu chí ưu tiên.
        *   Cập nhật nút `WIN` với `priorityLevel`, `priorityScore`, `estimatedImpact`, `estimatedEffort`, `preliminaryResourceRequirements`.
        *   Có thể tạo các mối quan hệ như `WIN -[REQUIRES_RESOURCE_TYPE]-> ResourceType`.
    *   **Có thể truy vấn `ResourceManagementAgent` (thông qua API hoặc sự kiện) để lấy thông tin tổng quan về nguồn lực.**
*   **Sự Kiện Phát Sinh (Ví dụ):**
    * ` WINStrategicAnalysisCompletedEvent` (đầu vào)
    * ` OntologyUpdateRequest` (từ `PrioritizationAgent` đến `OntologyManagementAgent`)
    * ` WINPrioritizedEvent` (đầu ra)
    * ` NotificationEvent`
*   **Ví dụ Minh Họa Cụ Thể:**
    *   **WIN:** "Nghiên cứu ứng dụng AI để tối ưu hóa quy trình chăm sóc khách hàng" (đã được phân tích chiến lược là "Rất phù hợp", điểm 9/10).
    *   **Bối cảnh:** Có 5 WIN khác đang chờ, 2 dự án đang chạy. Tiêu chí ưu tiên: Phù hợp chiến lược (50%), ROI tiềm năng (30%), Khẩn cấp (20%).
    *   **Kết quả Phân tích Ưu tiên (`PrioritizationAgent`):**
        *   WIN này được gán mức ưu tiên "Rất cao" do điểm chiến lược cao và tiềm năng ROI lớn từ việc tối ưu CSKH.
        *   Tác động: Cao (cải thiện CSAT, giảm chi phí vận hành).
        *   Nỗ lực sơ bộ: Trung bình-Cao (cần đội R&D chuyên biệt, thời gian nghiên cứu).
    *   **Khảo sát Nguồn lực Sơ bộ:**
        *   Nhân lực: 2-3 Kỹ sư AI/ML (R&D), 1 Chuyên gia CSKH (để tư vấn).
        *   Công nghệ: Nền tảng thử nghiệm AI, dữ liệu CSKH lịch sử.
        *   Thời gian: 3-6 tháng cho giai đoạn nghiên cứu.
    *   **Cập nhật Ontology:** Nút `WIN` được cập nhật với `priorityLevel: "Rất cao"`, `preliminaryResourceRequirements: {"personnel": [{"role": "AI/ML Engineer", "count": 2-3}, {"role": "CX Specialist", "count": 1}], "technology": ["AI Experimentation Platform"], "duration_months": 3-6}`.
    *   **Thông báo:** Các bên liên quan được thông báo. WIN này có thể được đưa vào danh sách xem xét để chuyển thành dự án chính thức.

#### 10.5.4. Luồng Tác vụ 4: Chuyển đổi WIN thành Dự án Khởi tạo (Project Initiation)

*   **Agents Tham Gia:**
    * ` ProjectInitiationAgent` (có thể là một vai trò chuyên biệt hoặc một phần của `ResolutionCoordinatorAgent`)
    * ` OntologyManagementAgent`
    * ` ResourceManagementAgent` (để phân tích chi tiết hơn và xác nhận sơ bộ nguồn lực)
    * ` RiskAssessmentAgent` (để thực hiện đánh giá rủi ro ban đầu)
    * ` KnowledgeExtractionAgent` (để trích xuất thông tin chi tiết cho việc lập kế hoạch dự án)
    * ` UserInteractionAgent` (để thu thập thêm thông tin từ người dùng nếu cần, và hiển thị thông tin dự án)
    * ` NotificationAgent`
    * ` EventDispatcherAgent`
*   **Điều Kiện Kích Hoạt (Trigger):** `ProjectInitiationAgent` nhận được `WINPrioritizedEvent` cho một WIN có mức độ ưu tiên cao (ví dụ: "Rất cao", "Cao") và kết quả khảo sát nguồn lực sơ bộ khả quan. Hoặc, có thể được kích hoạt thủ công bởi người quản lý dự án/ban lãnh đạo thông qua `UserInteractionAgent`.
*   **Mục Tiêu:**
    *   Chính thức hóa một `WIN` có tiềm năng cao thành một `Project` khởi tạo trong hệ thống.
    *   Xây dựng một `ProjectBrief` hoặc `InitialProjectCharter` sơ bộ, bao gồm mục tiêu, phạm vi ban đầu, các bên liên quan chính, và các giả định.
    *   Thực hiện đánh giá rủi ro ban đầu và xác định các yếu tố thành công quan trọng.
    *   Xác nhận (ở mức độ cao) sự sẵn có của các nguồn lực quan trọng hoặc xác định các thiếu hụt cần giải quyết.
    *   Tạo nút `Project` mới trong ontology, liên kết nó với `WIN` gốc và các `StrategicGoal` liên quan.
    *   Thông báo cho các bên liên quan về việc khởi tạo dự án và các bước tiếp theo.
*   **Luồng Các Bước Thực Hiện Chi Tiết:**
    1.  **Tiếp nhận Yêu cầu Khởi tạo Dự án (`ProjectInitiationAgent`):**
        * ` ProjectInitiationAgent` nhận `WINPrioritizedEvent` (chứa WIN ID, mức ưu tiên, và tóm tắt yêu cầu nguồn lực) từ `EventDispatcherAgent`.
        *   Hoặc, nhận yêu cầu khởi tạo dự án thủ công từ người dùng có thẩm quyền.
    2.  **Thu thập Thông tin Chi tiết (`ProjectInitiationAgent`, `OntologyManagementAgent`, `KnowledgeExtractionAgent`):**
        * ` ProjectInitiationAgent` yêu cầu `OntologyManagementAgent` cung cấp toàn bộ thông tin về `WIN` (bao gồm tất cả các phân tích trước đó: chiến lược, ưu tiên, nguồn lực sơ bộ).
        * ` KnowledgeExtractionAgent` có thể được huy động để phân tích sâu hơn nội dung `WIN`, các tài liệu đính kèm (nếu có) để trích xuất các yêu cầu, ràng buộc, và thông tin hữu ích cho việc lập `ProjectBrief`.
    3.  **Xây dựng Dự thảo Project Brief/Charter (`ProjectInitiationAgent`):**
        *   Dựa trên thông tin thu thập được, `ProjectInitiationAgent` soạn thảo một `ProjectBrief` bao gồm:
            * **Tên Dự án:** (Ví dụ: "Dự án Nghiên cứu AI CSKH")
            * **Mô tả Dự án:** Tóm tắt từ WIN và mục tiêu.
            * **Mục tiêu Dự án (SMART):** Kết quả cụ thể mong đợi.
            * **Phạm vi Ban đầu (High-Level):** Các hạng mục chính sẽ thực hiện, các hạng mục ngoài phạm vi.
            * **Các Bên Liên Quan Chính:** Người quản lý dự án dự kiến, nhà tài trợ, đội ngũ chủ chốt.
            * **Sự liên kết Chiến lược:** Các `StrategicGoal` mà dự án này hỗ trợ.
            * **Kết quả Phân tích WIN:** Tóm tắt các phân tích trước đó.
    4.  **Đánh giá Rủi ro Ban đầu (`RiskAssessmentAgent`):**
        * ` ProjectInitiationAgent` gửi yêu cầu đánh giá rủi ro ban đầu đến `RiskAssessmentAgent` kèm theo `ProjectBrief` dự thảo.
        * ` RiskAssessmentAgent` xác định các rủi ro tiềm ẩn chính (về kỹ thuật, nguồn lực, thị trường, vận hành), đánh giá sơ bộ mức độ ảnh hưởng và khả năng xảy ra.
        *   Kết quả được trả về cho `ProjectInitiationAgent` để bổ sung vào `ProjectBrief`.
    5.  **Phân tích và Xác nhận Nguồn lực Chi tiết hơn (`ResourceManagementAgent`):**
        * ` ProjectInitiationAgent` gửi yêu cầu phân tích nguồn lực chi tiết hơn đến `ResourceManagementAgent`, dựa trên `preliminaryResourceRequirements` từ WIN và `ProjectBrief`.
        * ` ResourceManagementAgent` kiểm tra cụ thể hơn về sự sẵn có của các kỹ năng, công cụ, ngân sách dự kiến (nếu có thể), và xác nhận khả năng đáp ứng hoặc các điểm nghẽn tiềm ẩn.
        *   Thông tin này được cập nhật vào `ProjectBrief`.
    6.  **Hoàn thiện và Yêu cầu Tạo Project trong Ontology (`ProjectInitiationAgent`):**
        * ` ProjectInitiationAgent` hoàn thiện `ProjectBrief` với các thông tin từ đánh giá rủi ro và phân tích nguồn lực.
        *   Nếu cần, `UserInteractionAgent` có thể được sử dụng để trình bày `ProjectBrief` cho người có thẩm quyền phê duyệt (ví dụ: Ban Lãnh Đạo, Quản lý Danh mục) và thu thập quyết định go/no-go.
        *   Nếu được phê duyệt, `ProjectInitiationAgent` gửi yêu cầu tạo `Project` mới đến `OntologyManagementAgent`, kèm theo `ProjectBrief` hoàn chỉnh.
    7.  **Tạo Project trong Ontology (`OntologyManagementAgent`):**
        * ` OntologyManagementAgent` nhận yêu cầu.
        *   Tạo một nút `Project` mới trong Neo4j Aura với các thuộc tính từ `ProjectBrief` (ví dụ: `projectName`, `projectDescription`, `projectStatus: "Khởi tạo"`, `startDate` dự kiến, `projectManager` (nếu có), `budgetEstimate` (nếu có)).
        *   Tạo các mối quan hệ:
            * ` Project -[DERIVED_FROM]-> WIN`
            * ` Project -[ALIGNED_WITH]-> StrategicGoal` (các mục tiêu chiến lược liên quan)
            * ` Project -[HAS_STAKEHOLDER]-> User` (các bên liên quan)
            * ` Project -[HAS_RISK]-> Risk` (các rủi ro đã xác định)
            * ` Project -[REQUIRES_RESOURCE_PROFILE]-> ResourceProfile` (một hồ sơ yêu cầu nguồn lực chi tiết hơn)
        *   Phát sự kiện `ProjectInitiatedEvent` (chứa Project ID, tên dự án) đến `EventDispatcherAgent`.
    8.  **Thông báo và Cập nhật Giao diện (`EventDispatcherAgent`, `NotificationAgent`, `UserInteractionAgent`):**
        * ` EventDispatcherAgent` nhận `ProjectInitiatedEvent`.
        *   Chuyển tiếp đến `NotificationAgent` và `UserInteractionAgent`.
        * ` NotificationAgent` thông báo cho tất cả các bên liên quan về việc dự án đã được khởi tạo chính thức.
        * ` UserInteractionAgent` cập nhật giao diện TRM-OS, hiển thị dự án mới trong danh sách dự án, liên kết với WIN gốc.
*   **Tương Tác Dữ liệu và Ontology:**
    *   **Neo4j Aura:**
        *   Đọc thông tin chi tiết từ nút `WIN`.
        *   Tạo nút `Project` mới và các thuộc tính liên quan.
        *   Tạo các mối quan hệ `DERIVED_FROM`, `ALIGNED_WITH`, `HAS_STAKEHOLDER`, `HAS_RISK`, `REQUIRES_RESOURCE_PROFILE`.
    *   **Supabase (PostgreSQL/Vector - nếu có):** Có thể lưu trữ các tài liệu `ProjectBrief` dạng file hoặc các phiên bản chi tiết.
*   **Sự Kiện Phát Sinh (Ví dụ):**
    * ` WINPrioritizedEvent` (đầu vào)
    * ` RiskAssessmentRequest`, `ResourceAnalysisRequest`
    * ` OntologyUpdateRequest` (tạo `Project`)
    * ` ProjectInitiatedEvent` (đầu ra)
    * ` NotificationEvent`
*   **Ví dụ Minh Họa Cụ Thể:**
    *   **WIN:** "Nghiên cứu ứng dụng AI để tối ưu hóa quy trình chăm sóc khách hàng" (Ưu tiên: "Rất cao", nguồn lực sơ bộ: 2-3 Kỹ sư AI/ML, 1 Chuyên gia CSKH, 3-6 tháng).
    *   **`ProjectInitiationAgent` kích hoạt.**
    *   **`ProjectBrief` được soạn thảo:**
        *   Tên: "Dự án Nghiên cứu AI CSKH Giai đoạn 1"
        *   Mục tiêu: "Đến cuối Q4, phát triển và thử nghiệm thành công 1 PoC (Proof of Concept) ứng dụng AI giúp giảm 15% thời gian xử lý trung bình cho 2 loại yêu cầu CSKH phổ biến nhất."
        *   Phạm vi: Thu thập dữ liệu, lựa chọn mô hình AI, xây dựng PoC, thử nghiệm nội bộ.
        *   Liên kết: `SG01` (Nâng cao trải nghiệm khách hàng).
    *   **`RiskAssessmentAgent`:** Xác định rủi ro "Thiếu dữ liệu chất lượng cao", "Mô hình AI không đạt độ chính xác kỳ vọng".
    *   **`ResourceManagementAgent`:** Xác nhận có thể phân bổ 2 Kỹ sư AI/ML từ đội R&D, cần tuyển thêm 1 nếu dự án mở rộng. Chuyên gia CSKH sẵn sàng tham gia.
    *   **Ontology Update:** Nút `Project: P005 - Dự án Nghiên cứu AI CSKH Giai đoạn 1` được tạo, liên kết với WIN, SG01, các rủi ro, và hồ sơ nguồn lực. Trạng thái: "Khởi tạo".
    *   **Thông báo:** Các bên liên quan (CEO, Trưởng phòng R&D, Trưởng phòng CSKH) nhận thông báo dự án đã khởi tạo. Dự án xuất hiện trên dashboard quản lý dự án.

#### 10.5.5. Luồng Tác vụ 5: Lập Kế hoạch Dự án Chi tiết và Phân bổ Nguồn lực

*   **Agents Tham Gia:**
    * ` ProjectPlanningAgent` (có thể là một vai trò chuyên biệt hoặc một phần của `ResolutionCoordinatorAgent`)
    * ` OntologyManagementAgent`
    * ` ResourceManagementAgent` (để xác nhận và phân bổ nguồn lực cụ thể)
    * ` KnowledgeExtractionAgent` (để phân rã mục tiêu dự án thành các nhiệm vụ, ước tính công việc)
    * ` DependencyAnalysisAgent` (để xác định và quản lý các phụ thuộc giữa các nhiệm vụ)
    * ` UserInteractionAgent` (để thu thập thông tin từ các trưởng nhóm, chuyên gia và hiển thị kế hoạch)
    * ` NotificationAgent`
    * ` EventDispatcherAgent`
*   **Điều Kiện Kích Hoạt (Trigger):** `ProjectPlanningAgent` nhận được `ProjectInitiatedEvent` cho một dự án mới từ `EventDispatcherAgent`. Hoặc, được kích hoạt thủ công bởi Người Quản lý Dự án được chỉ định.
*   **Mục Tiêu:**
    *   Phát triển một kế hoạch dự án chi tiết (`DetailedProjectPlan`) từ `ProjectBrief` đã được phê duyệt.
    *   Phân rã các mục tiêu dự án thành các `Task` cụ thể, có thể đo lường được, có thể đạt được, có liên quan và có giới hạn thời gian (SMART).
    *   Xác định các `Milestone` quan trọng của dự án.
    *   Ước tính nỗ lực, thời gian và nguồn lực cần thiết cho từng `Task`.
    *   Xác định các phụ thuộc giữa các `Task` và xây dựng lịch trình dự án.
    *   Chính thức phân bổ các nguồn lực (nhân lực, tài chính, thiết bị) cho dự án và các `Task` cụ thể.
    *   Cập nhật `Project` trong ontology với kế hoạch chi tiết, các `Task`, `Milestone`, và nguồn lực đã phân bổ.
    *   Thông báo cho đội ngũ dự án và các bên liên quan về kế hoạch đã được phê duyệt.
*   **Luồng Các Bước Thực Hiện Chi Tiết:**
    1.  **Tiếp nhận Yêu cầu Lập Kế hoạch (`ProjectPlanningAgent`):**
        * ` ProjectPlanningAgent` nhận `ProjectInitiatedEvent` (chứa Project ID) từ `EventDispatcherAgent`.
    2.  **Thu thập Thông tin Dự án và Bối cảnh (`ProjectPlanningAgent`, `OntologyManagementAgent`):**
        * ` ProjectPlanningAgent` yêu cầu `OntologyManagementAgent` cung cấp toàn bộ thông tin về `Project` (bao gồm `ProjectBrief`, các rủi ro ban đầu, yêu cầu nguồn lực sơ bộ, liên kết chiến lược).
        *   Thu thập các template kế hoạch dự án, các bài học từ các dự án tương tự (nếu có trong ontology).
    3.  **Phân rã Công việc (WBS - Work Breakdown Structure) (`ProjectPlanningAgent`, `KnowledgeExtractionAgent`):**
        * ` ProjectPlanningAgent` phối hợp với `KnowledgeExtractionAgent` để phân tích `ProjectBrief` và các mục tiêu dự án.
        *   Phân rã các mục tiêu thành các gói công việc (Work Packages) và sau đó thành các `Task` chi tiết.
        *   Mỗi `Task` được định nghĩa rõ ràng về kết quả đầu ra, người chịu trách nhiệm dự kiến.
        * ` UserInteractionAgent` có thể được sử dụng để thu thập ý kiến từ các chuyên gia hoặc trưởng nhóm về việc phân rã công việc.
    4.  **Ước tính Nỗ lực, Thời gian và Nguồn lực cho Tasks (`ProjectPlanningAgent`, `KnowledgeExtractionAgent`):**
        *   Với mỗi `Task`, `ProjectPlanningAgent` (có thể sử dụng `KnowledgeExtractionAgent` để phân tích hoặc so sánh với dữ liệu lịch sử) ước tính:
            *   Nỗ lực (ví dụ: số giờ công, story points).
            *   Thời gian thực hiện.
            *   Các loại và số lượng nguồn lực cần thiết (ví dụ: "Kỹ sư AI - 20 giờ", "Ngân sách - 500 USD cho API").
    5.  **Xác định Phụ thuộc và Xây dựng Lịch trình (`ProjectPlanningAgent`, `DependencyAnalysisAgent`):**
        * ` DependencyAnalysisAgent` được yêu cầu phân tích các `Task` để xác định các mối quan hệ phụ thuộc (ví dụ: Task B chỉ bắt đầu sau khi Task A hoàn thành).
        * ` ProjectPlanningAgent` sử dụng thông tin phụ thuộc, ước tính thời gian để xây dựng lịch trình dự án (ví dụ: biểu đồ Gantt, critical path analysis).
        *   Xác định các `Milestone` quan trọng dựa trên việc hoàn thành các nhóm `Task` hoặc các kết quả đầu ra chính.
    6.  **Yêu cầu và Xác nhận Phân bổ Nguồn lực (`ProjectPlanningAgent`, `ResourceManagementAgent`):**
        * ` ProjectPlanningAgent` tổng hợp yêu cầu nguồn lực chi tiết cho toàn bộ dự án và từng giai đoạn/Task.
        *   Gửi yêu cầu phân bổ nguồn lực chính thức đến `ResourceManagementAgent`.
        * ` ResourceManagementAgent` kiểm tra sự sẵn có, giải quyết các xung đột (nếu có, có thể cần sự can thiệp của `ResolutionCoordinatorAgent`), và xác nhận việc phân bổ nguồn lực (con người, ngân sách, thiết bị) cho dự án.
    7.  **Hoàn thiện Kế hoạch Dự án và Yêu cầu Cập nhật Ontology (`ProjectPlanningAgent`):**
        * ` ProjectPlanningAgent` tổng hợp tất cả thông tin vào một `DetailedProjectPlan`.
        * ` UserInteractionAgent` có thể được sử dụng để trình bày kế hoạch cho Người Quản lý Dự án và các bên liên quan để phê duyệt.
        *   Sau khi phê duyệt, `ProjectPlanningAgent` gửi yêu cầu cập nhật `Project` trong ontology đến `OntologyManagementAgent` với `DetailedProjectPlan`.
    8.  **Cập nhật Ontology (`OntologyManagementAgent`):**
        * ` OntologyManagementAgent` nhận yêu cầu.
        *   Cập nhật nút `Project` với trạng thái mới (ví dụ: `projectStatus: "Đang Lập kế hoạch"` hoặc `projectStatus: "Sẵn sàng Thực thi"`).
        *   Tạo các nút `Task` và `Milestone` trong Neo4j Aura.
        *   Tạo các mối quan hệ:
            * ` Project -[HAS_TASK]-> Task`
            * ` Project -[HAS_MILESTONE]-> Milestone`
            * ` Task -[PRECEDES]-> Task` (thể hiện sự phụ thuộc)
            * ` Task -[ASSIGNED_TO]-> User` (gán người thực hiện)
            * ` Task -[REQUIRES_RESOURCE]-> ResourceInstance` (gán nguồn lực cụ thể)
            * ` Project -[HAS_DETAILED_PLAN]-> DetailedProjectPlanNode` (có thể lưu trữ link tới tài liệu kế hoạch hoặc cấu trúc JSON của kế hoạch).
        *   Phát sự kiện `ProjectPlanningCompletedEvent` (chứa Project ID và tham chiếu đến kế hoạch) đến `EventDispatcherAgent`.
    9.  **Thông báo và Phổ biến Kế hoạch (`EventDispatcherAgent`, `NotificationAgent`, `UserInteractionAgent`):**
        * ` EventDispatcherAgent` nhận `ProjectPlanningCompletedEvent`.
        *   Chuyển tiếp đến `NotificationAgent` và `UserInteractionAgent`.
        * ` NotificationAgent` thông báo cho đội ngũ dự án và các bên liên quan rằng kế hoạch dự án đã hoàn tất và được phê duyệt.
        * ` UserInteractionAgent` cập nhật giao diện TRM-OS, hiển thị kế hoạch chi tiết, danh sách công việc, lịch trình cho các thành viên dự án.
*   **Tương Tác Dữ liệu và Ontology:**
    *   **Neo4j Aura:**
        *   Đọc thông tin từ nút `Project` (bao gồm `ProjectBrief`).
        *   Tạo và liên kết các nút `Task`, `Milestone`.
        *   Cập nhật thuộc tính `projectStatus` và các liên kết đến kế hoạch chi tiết.
        *   Ghi nhận việc phân bổ `User` và `ResourceInstance` cho các `Task`.
    *   **Supabase (PostgreSQL/Vector - nếu có):** Có thể lưu trữ các tài liệu `DetailedProjectPlan` hoặc các file WBS.
*   **Sự Kiện Phát Sinh (Ví dụ):**
    * ` ProjectInitiatedEvent` (đầu vào)
    * ` ResourceAllocationRequest`
    * ` OntologyUpdateRequest` (tạo `Task`, `Milestone`, cập nhật `Project`)
    * ` ProjectPlanningCompletedEvent` (đầu ra)
    * ` NotificationEvent` (thông báo kế hoạch)
    * ` TaskAssignedEvent` (khi một task cụ thể được gán)
*   **Ví dụ Minh Họa Cụ Thể:**
    *   **Dự án:** `P005 - Dự án Nghiên cứu AI CSKH Giai đoạn 1` (Trạng thái: "Khởi tạo").
    *   **`ProjectPlanningAgent` kích hoạt.**
    *   **Phân rã công việc:**
        *   Task 1: Thu thập và tiền xử lý dữ liệu CSKH (Ước tính: 40 giờ).
        *   Task 2: Nghiên cứu và lựa chọn mô hình AI phù hợp (Ước tính: 60 giờ).
        *   Task 3: Xây dựng PoC phiên bản Alpha (Ước tính: 80 giờ).
        *   Task 4: Thử nghiệm nội bộ và thu thập phản hồi (Ước tính: 30 giờ).
        *   Milestone 1: Hoàn thành PoC Alpha.
    *   **Phụ thuộc:** Task 2 sau Task 1; Task 3 sau Task 2; Task 4 sau Task 3.
    *   **`ResourceManagementAgent`:** Xác nhận Kỹ sư AI A và B được phân bổ cho dự án, tổng cộng 210 giờ. Ngân sách 1000 USD được duyệt.
    *   **Ontology Update:**
        * ` Project: P005` cập nhật `projectStatus: "Sẵn sàng Thực thi"`.
        *   Các nút `Task` (T1.1, T1.2, T1.3, T1.4) và `Milestone` (M1.1) được tạo và liên kết.
        * ` Task: T1.1 -[ASSIGNED_TO]-> User: Kỹ sư A`.
    *   **Thông báo:** Đội dự án (Kỹ sư A, B, Chuyên gia CSKH) nhận được kế hoạch chi tiết và phân công công việc.

#### 10.5.6. Luồng Tác vụ 6: Thực thi Dự án, Giám sát Tiến độ và Quản lý Thay đổi

*   **Agents Tham Gia:**
    * ` TaskExecutionAgent` (có thể là một tập hợp các agent chuyên biệt cho từng loại task, hoặc một agent điều phối việc thực thi)
    * ` ProgressTrackingAgent`
    * ` OntologyManagementAgent`
    * ` ResourceManagementAgent` (để theo dõi sử dụng nguồn lực)
    * ` RiskAssessmentAgent` (để đánh giá lại rủi ro khi có thay đổi hoặc vấn đề)
    * ` ChangeManagementAgent` (để xử lý các yêu cầu thay đổi)
    * ` IssueTrackingAgent` (để quản lý các vấn đề phát sinh)
    * ` UserInteractionAgent` (để cập nhật tiến độ từ người dùng, báo cáo)
    * ` NotificationAgent`
    * ` EventDispatcherAgent`
    * ` ResolutionCoordinatorAgent` (khi cần giải quyết xung đột hoặc vấn đề phức tạp)
*   **Điều Kiện Kích Hoạt (Trigger):**
    * ` ProjectPlanningCompletedEvent` được nhận, và dự án có trạng thái "Sẵn sàng Thực thi".
    *   Một `Task` trong kế hoạch dự án đến hạn bắt đầu.
    *   Người dùng (ví dụ: thành viên đội dự án) cập nhật trạng thái hoàn thành một `Task`.
*   **Mục Tiêu:**
    *   Đảm bảo các `Task` của dự án được thực thi theo kế hoạch.
    *   Theo dõi và cập nhật tiến độ thực tế của các `Task` và `Milestone` so với kế hoạch.
    *   Giám sát việc sử dụng nguồn lực (thời gian, ngân sách, nhân lực) và so sánh với phân bổ.
    *   Xác định sớm các sai lệch, vấn đề (issues), và rủi ro mới phát sinh.
    *   Quản lý các yêu cầu thay đổi đối với phạm vi, lịch trình, hoặc nguồn lực của dự án một cách có kiểm soát.
    *   Cập nhật `Project`, `Task`, `Issue`, `ChangeRequest` trong ontology với thông tin mới nhất.
    *   Cung cấp thông tin minh bạch về tiến độ và tình trạng dự án cho các bên liên quan.
*   **Luồng Các Bước Thực Hiện Chi Tiết (Tổng quan - có thể lặp lại cho từng Task/Giai đoạn):**
    1.  **Khởi tạo Thực thi Task (`TaskExecutionAgent`, `UserInteractionAgent`):**
        *   Khi một `Task` đến hạn bắt đầu (dựa trên lịch trình trong ontology), `TaskExecutionAgent` có thể nhắc nhở người được giao (`User`) thông qua `UserInteractionAgent` hoặc `NotificationAgent`.
        *   Người dùng bắt đầu thực hiện `Task`. `UserInteractionAgent` thu thập thông tin cập nhật trạng thái `Task` (ví dụ: "Đang thực hiện").
    2.  **Cập nhật Tiến độ (`ProgressTrackingAgent`, `UserInteractionAgent`, `OntologyManagementAgent`):**
        *   Người dùng cập nhật tiến độ (ví dụ: % hoàn thành, kết quả đầu ra tạm thời) thông qua `UserInteractionAgent`.
        * ` ProgressTrackingAgent` nhận thông tin này, tính toán lại tiến độ tổng thể của dự án, so sánh với kế hoạch.
        * ` ProgressTrackingAgent` yêu cầu `OntologyManagementAgent` cập nhật trạng thái, % hoàn thành, ngày bắt đầu/kết thúc thực tế của `Task` trong ontology.
        *   Khi một `Task` hoàn thành, `OntologyManagementAgent` cập nhật trạng thái thành "Hoàn thành" và phát `TaskCompletedEvent`.
    3.  **Giám sát Nguồn lực (`ResourceManagementAgent`, `OntologyManagementAgent`):**
        * ` ResourceManagementAgent` theo dõi việc sử dụng nguồn lực thực tế (ví dụ: giờ công đã ghi nhận, chi phí đã phát sinh) so với kế hoạch.
        *   Cập nhật thông tin sử dụng nguồn lực trong ontology.
        *   Nếu có nguy cơ vượt ngân sách hoặc thiếu hụt nguồn lực, cảnh báo cho `ProjectPlanningAgent` hoặc Người Quản lý Dự án.
    4.  **Xác định và Theo dõi Vấn đề (`IssueTrackingAgent`, `UserInteractionAgent`, `OntologyManagementAgent`):**
        *   Người dùng hoặc các agent khác (ví dụ: `ProgressTrackingAgent` phát hiện task trễ hạn) có thể báo cáo một vấn đề (issue) thông qua `UserInteractionAgent` hoặc sự kiện.
        * ` IssueTrackingAgent` ghi nhận `Issue` (mô tả, mức độ ưu tiên, người báo cáo) và yêu cầu `OntologyManagementAgent` tạo nút `Issue` và liên kết với `Project` hoặc `Task` liên quan.
        * ` IssueTrackingAgent` theo dõi trạng thái giải quyết `Issue`.
    5.  **Quản lý Yêu cầu Thay đổi (`ChangeManagementAgent`, `UserInteractionAgent`, `OntologyManagementAgent`, `RiskAssessmentAgent`, `ProjectPlanningAgent`):**
        *   Người dùng hoặc các bên liên quan gửi yêu cầu thay đổi (ví dụ: thay đổi phạm vi, thêm tính năng) thông qua `UserInteractionAgent`.
        * ` ChangeManagementAgent` tiếp nhận, ghi nhận `ChangeRequest` và yêu cầu `OntologyManagementAgent` tạo nút `ChangeRequest`.
        * ` ChangeManagementAgent` phối hợp với `RiskAssessmentAgent` để đánh giá tác động của thay đổi (về chi phí, thời gian, rủi ro).
        * ` ProjectPlanningAgent` có thể được yêu cầu cập nhật kế hoạch dự án nếu thay đổi được phê duyệt.
        *   Sau khi có quyết định (phê duyệt/từ chối), `OntologyManagementAgent` cập nhật trạng thái `ChangeRequest` và các `Task`/`Project` liên quan.
    6.  **Đánh giá Rủi ro Định kỳ và Khi có Sự kiện (`RiskAssessmentAgent`, `OntologyManagementAgent`):**
        * ` RiskAssessmentAgent` định kỳ hoặc khi có sự kiện (ví dụ: `Issue` nghiêm trọng, `ChangeRequest` lớn) đánh giá lại các rủi ro của dự án.
        *   Cập nhật thông tin rủi ro trong ontology. Đề xuất các hành động giảm thiểu nếu cần.
    7.  **Giải quyết Xung đột và Vấn đề Phức tạp (`ResolutionCoordinatorAgent`):**
        *   Khi có các vấn đề phức tạp, xung đột nguồn lực, hoặc các `Issue` không thể giải quyết ở cấp độ `TaskExecutionAgent` hoặc `IssueTrackingAgent`, `ResolutionCoordinatorAgent` được kích hoạt.
        * ` ResolutionCoordinatorAgent` điều phối các agent liên quan để tìm giải pháp.
    8.  **Báo cáo và Thông báo (`ProgressTrackingAgent`, `NotificationAgent`, `UserInteractionAgent`):**
        * ` ProgressTrackingAgent` tạo báo cáo tiến độ định kỳ (hoặc theo yêu cầu).
        * ` UserInteractionAgent` hiển thị dashboard tiến độ, các vấn đề, rủi ro cho các bên liên quan.
        * ` NotificationAgent` gửi thông báo về các cập nhật quan trọng (ví dụ: `Milestone` đạt được, `Issue` nghiêm trọng, `ChangeRequest` được phê duyệt).
    9.  **Hoàn thành Milestone và Dự án (`ProgressTrackingAgent`, `OntologyManagementAgent`):**
        *   Khi tất cả các `Task` dẫn đến một `Milestone` hoàn thành, `ProgressTrackingAgent` xác nhận `Milestone` đạt được. `OntologyManagementAgent` cập nhật trạng thái `Milestone`.
        *   Khi tất cả các `Task` và `Milestone` của dự án hoàn thành, `ProgressTrackingAgent` xác nhận dự án hoàn thành. `OntologyManagementAgent` cập nhật trạng thái `Project` thành "Hoàn thành" và phát `ProjectCompletedEvent`.
*   **Tương Tác Dữ liệu và Ontology:**
    *   **Neo4j Aura:**
        *   Đọc kế hoạch chi tiết từ `Project`, `Task`, `Milestone`.
        *   Cập nhật liên tục trạng thái, % hoàn thành, ngày thực tế của `Task` và `Milestone`.
        *   Tạo và quản lý các nút `Issue`, `ChangeRequest`, `Risk`.
        *   Liên kết `Issue`, `ChangeRequest`, `Risk` với `Project` và `Task`.
        *   Cập nhật thông tin sử dụng `ResourceInstance`.
        *   Cập nhật `projectStatus` khi hoàn thành.
    *   **Supabase (PostgreSQL/Vector - nếu có):** Có thể lưu trữ log chi tiết, file đính kèm của `Issue`, `ChangeRequest`, hoặc các báo cáo tiến độ.
*   **Sự Kiện Phát Sinh (Ví dụ):**
    * ` TaskStatusUpdateEvent`
    * ` TaskCompletedEvent`
    * ` MilestoneAchievedEvent`
    * ` IssueLoggedEvent`
    * ` IssueResolvedEvent`
    * ` ChangeRequestSubmittedEvent`
    * ` ChangeRequestApprovedEvent` / `ChangeRequestRejectedEvent`
    * ` RiskIdentifiedEvent`
    * ` ProjectProgressReportEvent`
    * ` ProjectCompletedEvent` (đầu ra cuối cùng của luồng này)
*   **Ví dụ Minh Họa Cụ Thể:**
    *   **Dự án:** `P005 - Dự án Nghiên cứu AI CSKH Giai đoạn 1` (Trạng thái: "Sẵn sàng Thực thi").
    *   **Task 1: "Thu thập và tiền xử lý dữ liệu CSKH"**
        *   Kỹ sư A (User) bắt đầu thực hiện, cập nhật trạng thái "Đang thực hiện" qua `UserInteractionAgent`.
        *   Sau 35 giờ, Kỹ sư A cập nhật "Hoàn thành 100%". `ProgressTrackingAgent` ghi nhận, `OntologyManagementAgent` cập nhật `Task: T1.1` thành "Hoàn thành", `actualEffort: 35 giờ`. `TaskCompletedEvent` được phát.
    *   **Issue:** Trong quá trình thực hiện Task 2 "Nghiên cứu và lựa chọn mô hình AI", Kỹ sư B phát hiện thiếu một số loại dữ liệu quan trọng.
        *   Kỹ sư B báo cáo `Issue` "Thiếu dữ liệu đầu vào cho mô hình X" qua `UserInteractionAgent`.
        * ` IssueTrackingAgent` ghi nhận, `OntologyManagementAgent` tạo nút `Issue: I023` liên kết với `Task: T1.2` và `Project: P005`.
        * ` NotificationAgent` thông báo cho Quản lý Dự án.
    *   **Change Request:** Để giải quyết `Issue: I023`, cần bổ sung Task thu thập thêm dữ liệu.
        *   Quản lý Dự án tạo `ChangeRequest: CR007` "Bổ sung Task thu thập dữ liệu Y".
        * ` ChangeManagementAgent` xử lý, `RiskAssessmentAgent` đánh giá tác động (tăng 5 ngày, 10 giờ công).
        *   CR007 được phê duyệt. `ProjectPlanningAgent` cập nhật kế hoạch. `OntologyManagementAgent` cập nhật ontology.
    *   **Tiến độ:** `ProgressTrackingAgent` báo cáo hàng tuần: Dự án P005 hoàn thành 60%, trễ 2 ngày so với kế hoạch do CR007, rủi ro thiếu dữ liệu đã được giảm thiểu.

#### 10.5.7. Luồng Tác vụ 7: Kết thúc Dự án, Đánh giá và Lưu trữ Tri thức

*   **Agents Tham Gia:**
    * ` ProjectClosureAgent` (có thể là một vai trò của `ResolutionCoordinatorAgent` hoặc `ProjectPlanningAgent`)
    * ` OntologyManagementAgent`
    * ` KnowledgeExtractionAgent` (để thu thập và phân tích bài học kinh nghiệm, kết quả)
    * ` LearningAndOptimizationAgent` (để xử lý các bài học kinh nghiệm và đề xuất cải tiến)
    * ` UserInteractionAgent` (để thu thập phản hồi cuối cùng, báo cáo tổng kết)
    * ` NotificationAgent`
    * ` EventDispatcherAgent`
    * ` ResourceManagementAgent` (để giải phóng nguồn lực)
*   **Điều Kiện Kích Hoạt (Trigger):**
    * ` ProjectCompletedEvent` được nhận từ `ProgressTrackingAgent` (tất cả các `Task` và `Milestone` đã hoàn thành).
    *   Quyết định dừng dự án sớm (ví dụ: do thay đổi chiến lược, không còn khả thi).
*   **Mục Tiêu:**
    *   Chính thức đóng tất cả các hoạt động của dự án.
    *   Xác nhận việc hoàn thành tất cả các sản phẩm bàn giao (deliverables) và đạt được mục tiêu dự án (hoặc ghi nhận lý do nếu không đạt được).
    *   Thực hiện đánh giá sau dự án (Post-Implementation Review - PIR) để xác định các thành công, thất bại, và bài học kinh nghiệm (`LessonLearned`).
    *   Thu thập phản hồi từ các bên liên quan về quá trình và kết quả dự án.
    *   Giải phóng tất cả các nguồn lực đã phân bổ cho dự án.
    *   Lưu trữ tất cả các tài liệu, dữ liệu, và tri thức liên quan đến dự án vào ontology và các hệ thống lưu trữ liên quan.
    *   Cập nhật trạng thái cuối cùng của `Project` trong ontology (ví dụ: "Đã đóng", "Đã hủy").
    *   Thông báo cho tất cả các bên liên quan về việc đóng dự án.
    *   Đảm bảo tri thức thu được được sử dụng để cải thiện các quy trình và dự án trong tương lai.
*   **Luồng Các Bước Thực Hiện Chi Tiết:**
    1.  **Tiếp nhận Yêu cầu Đóng Dự án (`ProjectClosureAgent`):**
        * ` ProjectClosureAgent` nhận `ProjectCompletedEvent` (chứa Project ID) từ `EventDispatcherAgent` hoặc thông báo dừng dự án.
    2.  **Xác minh Hoàn thành và Bàn giao (`ProjectClosureAgent`, `OntologyManagementAgent`, `UserInteractionAgent`):**
        * ` ProjectClosureAgent` kiểm tra với `OntologyManagementAgent` để đảm bảo tất cả `Task` và `Milestone` đã được đánh dấu "Hoàn thành".
        *   Sử dụng `UserInteractionAgent` để xác nhận với các bên liên quan (ví dụ: chủ sở hữu sản phẩm, khách hàng) rằng tất cả các sản phẩm bàn giao đã được chấp nhận.
        *   Nếu có hạng mục chưa hoàn thành, `ProjectClosureAgent` có thể phối hợp với `ResolutionCoordinatorAgent` để xử lý.
    3.  **Thu thập Phản hồi và Bài học Kinh nghiệm (`ProjectClosureAgent`, `KnowledgeExtractionAgent`, `UserInteractionAgent`):**
        * ` ProjectClosureAgent` khởi tạo quy trình thu thập phản hồi từ đội ngũ dự án, khách hàng, và các bên liên quan khác thông qua `UserInteractionAgent` (ví dụ: gửi khảo sát, tổ chức buổi họp review).
        * ` KnowledgeExtractionAgent` hỗ trợ phân tích các phản hồi, biên bản họp, tài liệu dự án để rút ra các `LessonLearned` (cả tích cực và tiêu cực).
        *   Các `LessonLearned` được cấu trúc hóa (ví dụ: vấn đề, nguyên nhân, giải pháp đã thử, kết quả, khuyến nghị).
    4.  **Tạo Báo cáo Tổng kết Dự án (`ProjectClosureAgent`, `KnowledgeExtractionAgent`):**
        * ` ProjectClosureAgent` biên soạn `ProjectClosureReport` bao gồm:
            *   Tổng quan về mục tiêu và kết quả đạt được.
            *   So sánh hiệu suất thực tế với kế hoạch (thời gian, chi phí, phạm vi).
            *   Danh sách các `LessonLearned` quan trọng.
            *   Đánh giá rủi ro và cách quản lý.
            *   Thông tin về việc sử dụng nguồn lực.
        * ` KnowledgeExtractionAgent` có thể hỗ trợ tổng hợp dữ liệu cho báo cáo.
    5.  **Yêu cầu Cập nhật Ontology và Lưu trữ (`ProjectClosureAgent`, `OntologyManagementAgent`, `LearningAndOptimizationAgent`):**
        * ` ProjectClosureAgent` gửi `ProjectClosureReport` và các `LessonLearned` đã cấu trúc cho `OntologyManagementAgent` và `LearningAndOptimizationAgent`.
        *   Yêu cầu `OntologyManagementAgent` cập nhật trạng thái cuối cùng của `Project` (ví dụ: `projectStatus: "Đã đóng"`), liên kết với `ProjectClosureReportNode`, và tạo các nút `LessonLearned` liên kết với `Project`.
        * ` LearningAndOptimizationAgent` tiếp nhận các `LessonLearned` để phân tích sâu hơn, xác định các mẫu, và đề xuất cải tiến cho các quy trình, mẫu dự án, hoặc cơ sở tri thức chung của tổ chức.
    6.  **Cập nhật Ontology và Xử lý Tri thức (`OntologyManagementAgent`, `LearningAndOptimizationAgent`):**
        * ` OntologyManagementAgent` cập nhật nút `Project` và tạo các nút/quan hệ liên quan đến việc đóng dự án.
        *   Lưu trữ các tài liệu quan trọng (ví dụ: `ProjectClosureReport`, kế hoạch cuối cùng) có thể thông qua liên kết tới Supabase hoặc hệ thống quản lý tài liệu.
        * ` LearningAndOptimizationAgent` xử lý các `LessonLearned`:
            *   Phân loại, đánh giá mức độ quan trọng.
            *   Liên kết với các `KnowledgeDomain`, `Process`, `SolutionPattern` liên quan trong ontology.
            *   Có thể tạo ra các `ImprovementProposal` dựa trên các bài học này.
            *   Phát sự kiện `KnowledgeLearnedEvent` hoặc `ImprovementProposalGeneratedEvent`.
    7.  **Giải phóng Nguồn lực (`ResourceManagementAgent`):**
        * ` ProjectClosureAgent` thông báo cho `ResourceManagementAgent` rằng dự án đã đóng.
        * ` ResourceManagementAgent` cập nhật trạng thái của các nguồn lực đã phân bổ (nhân lực, thiết bị) thành "Sẵn sàng" và giải phóng chúng khỏi dự án.
    8.  **Thông báo Đóng Dự án (`NotificationAgent`, `EventDispatcherAgent`):**
        * ` OntologyManagementAgent` phát `ProjectClosedEvent` sau khi cập nhật thành công.
        * ` EventDispatcherAgent` chuyển tiếp sự kiện này đến `NotificationAgent`.
        * ` NotificationAgent` thông báo cho tất cả các bên liên quan rằng dự án đã chính thức đóng, kèm theo link tới `ProjectClosureReport` (nếu phù hợp).
*   **Tương Tác Dữ liệu và Ontology:**
    *   **Neo4j Aura:**
        *   Đọc trạng thái cuối cùng của `Project`, `Task`, `Milestone`.
        *   Cập nhật `projectStatus` thành "Đã đóng" hoặc "Đã hủy".
        *   Tạo các nút `LessonLearned`, `ProjectClosureReportNode`.
        *   Liên kết `LessonLearned` với `Project`, `KnowledgeDomain`, `Process`.
        * ` LearningAndOptimizationAgent` có thể tạo các nút `ImprovementProposal`.
    *   **Supabase (PostgreSQL/Vector - nếu có):** Lưu trữ các tài liệu `ProjectClosureReport`, bản khảo sát phản hồi, biên bản họp cuối cùng.
*   **Sự Kiện Phát Sinh (Ví dụ):**
    * ` ProjectCompletedEvent` (đầu vào)
    * ` ProjectClosureRequest`
    * ` LessonLearnedCapturedEvent`
    * ` OntologyUpdateRequest` (cập nhật `Project`, tạo `LessonLearned`)
    * ` KnowledgeLearnedEvent`
    * ` ResourceReleasedEvent`
    * ` ProjectClosedEvent` (đầu ra)
    * ` NotificationEvent` (thông báo đóng dự án)
*   **Ví dụ Minh Họa Cụ Thể:**
    *   **Dự án:** `P005 - Dự án Nghiên cứu AI CSKH Giai đoạn 1` (Trạng thái: "Hoàn thành").
    *   **`ProjectClosureAgent` kích hoạt.**
    *   **Xác minh:** Tất cả deliverables (PoC Alpha, báo cáo nghiên cứu) đã được chấp nhận.
    *   **Thu thập Bài học:**
        * ` LessonLearned: LL034` - "Việc thiếu dữ liệu đầu vào chi tiết (Issue I023) đã gây trễ 2 ngày. Cần cải thiện quy trình xác định yêu cầu dữ liệu ban đầu."
        * ` LessonLearned: LL035` - "Mô hình AI X cho kết quả khả quan với dữ liệu CSKH hiện tại, vượt kỳ vọng 15% về độ chính xác."
    *   **Báo cáo Tổng kết:** `ProjectClosureReport_P005.pdf` được tạo, ghi nhận dự án hoàn thành trong ngân sách, trễ 2 ngày, đạt mục tiêu PoC.
    *   **Ontology Update:**
        * ` Project: P005` cập nhật `projectStatus: "Đã đóng"`.
        *   Nút `LessonLearned: LL034` liên kết với `Project: P005` và `Process: DataRequirementDefinition`.
        * ` LearningAndOptimizationAgent` phân tích `LL034` và có thể đề xuất cập nhật checklist cho `Process: DataRequirementDefinition`.
    *   **Giải phóng Nguồn lực:** Kỹ sư A, B được `ResourceManagementAgent` đưa trở lại pool nguồn lực sẵn sàng.
    *   **Thông báo:** CEO, Trưởng phòng R&D, CSKH nhận thông báo P005 đã đóng, kèm báo cáo tổng kết.

#### 10.5.8. Luồng Tác vụ 8: Học hỏi Liên tục và Tối ưu hóa Hệ thống Toàn cục (TRM-OS)

*   **Agents Tham Gia Chính:**
    * ` LearningAndOptimizationAgent` (chủ đạo)
    * ` OntologyManagementAgent` (để cập nhật tri thức và cấu trúc)
    * ` KnowledgeExtractionAgent` (để trích xuất thông tin từ nhiều nguồn đa dạng)
    * ` DataCollectionAgent` (hoặc vai trò tương đương, thu thập log, metrics từ các agent và module)
    * ` UserInteractionAgent` (để thu thập phản hồi về đề xuất tối ưu, xác nhận thay đổi)
    * ` NotificationAgent` (thông báo về các thay đổi, cập nhật)
    * ` EventDispatcherAgent` (để nhận và điều phối các sự kiện liên quan đến học hỏi)
    * ` StrategicAlignmentAgent` (để đảm bảo các tối ưu hóa vẫn phù hợp với mục tiêu chiến lược)
*   **Điều Kiện Kích Hoạt (Trigger):**
    *   **Định kỳ:** Theo lịch trình (ví dụ: hàng tuần, hàng tháng) để rà soát hiệu suất và tri thức.
    *   **Sự kiện:**
        *   Tích lũy một số lượng nhất định các `LessonLearned` từ nhiều dự án.
        *   Phát hiện các loại `Tension` hoặc `Issue` lặp đi lặp lại với tần suất cao.
        *   Khi một `Project` hoặc `Process` có độ lệch lớn về hiệu suất (KPIs) so với kỳ vọng.
        *   Yêu cầu trực tiếp từ người quản trị hệ thống hoặc chuyên gia.
        *   Sau khi một `OntologyUpdate` lớn được thực hiện, cần đánh giá tác động và tối ưu.
*   **Mục Tiêu:**
    *   Chủ động xác định các điểm nghẽn, sự không hiệu quả, hoặc các cơ hội cải tiến mang tính hệ thống trong TRM-OS.
    *   Tổng hợp và phân tích tri thức từ nhiều nguồn: kết quả dự án, log hoạt động của agent, phản hồi người dùng, thay đổi trong ontology, xu hướng thị trường (nếu có `MarketAnalysisAgent`).
    *   Đề xuất và (nếu được phê duyệt) hỗ trợ triển khai các tối ưu hóa cho quy trình, hành vi của agent, cấu trúc ontology, chiến lược phân bổ nguồn lực, hoặc các mẫu giải pháp (`SolutionPattern`).
    *   Nâng cao khả năng thích ứng, hiệu quả, và trí tuệ tổng thể của TRM-OS.
    *   Đảm bảo rằng các cải tiến được lan tỏa và áp dụng một cách nhất quán.
*   **Luồng Các Bước Thực Hiện Chi Tiết:**
    1.  **Thu thập và Tổng hợp Dữ liệu Liên tục (`DataCollectionAgent`, `KnowledgeExtractionAgent`, `LearningAndOptimizationAgent`):**
        * ` DataCollectionAgent` thu thập dữ liệu vận hành: logs, metrics hiệu suất từ các agent, module, và cơ sở hạ tầng.
        * ` KnowledgeExtractionAgent` trích xuất thông tin từ các nguồn phi cấu trúc: `LessonLearned` từ các dự án, phản hồi người dùng, tài liệu, báo cáo.
        * ` LearningAndOptimizationAgent` tiếp nhận, tiền xử lý, và tổng hợp dữ liệu này vào một kho dữ liệu/tri thức tạm thời hoặc truy vấn trực tiếp từ ontology và các nguồn khác.
    2.  **Phân tích, Nhận diện Mẫu và Tạo Insight (`LearningAndOptimizationAgent`):**
        *   Sử dụng các kỹ thuật phân tích dữ liệu, machine learning (ví dụ: clustering, anomaly detection, trend analysis) để xác định các mẫu, mối tương quan, và các điểm bất thường.
        *   Ví dụ: Phát hiện rằng các dự án thuộc `KnowledgeDomain: "X"` thường xuyên gặp `IssueType: "Y"`, hoặc một `AgentType: "Z"` có tỷ lệ lỗi cao khi xử lý `EventType: "W"`.
        *   Tạo ra các `SystemInsightNode` trong ontology, mô tả các phát hiện này.
    3.  **Hình thành Giả thuyết và Đề xuất Tối ưu hóa (`LearningAndOptimizationAgent`):**
        *   Dựa trên các `SystemInsight`, `LearningAndOptimizationAgent` hình thành các giả thuyết về nguyên nhân gốc rễ và đề xuất các giải pháp tối ưu hóa (`ImprovementProposal`).
        *   Mỗi `ImprovementProposal` bao gồm: mô tả vấn đề, giải pháp đề xuất, lợi ích kỳ vọng, rủi ro tiềm ẩn, và các chỉ số để đo lường thành công.
        *   Ví dụ: Đề xuất thay đổi một `ProcessTemplate`, cập nhật `AgentConfiguration` cho một loại agent, hoặc giới thiệu một `SolutionPattern` mới.
    4.  **Đánh giá Tác động và Xác thực Đề xuất (`LearningAndOptimizationAgent`, `StrategicAlignmentAgent`, `UserInteractionAgent`):**
        * ` LearningAndOptimizationAgent` thực hiện phân tích tác động của đề xuất (ví dụ: chi phí, nguồn lực cần thiết, ảnh hưởng đến các thành phần khác).
        *   Có thể sử dụng mô phỏng (simulation) nếu hệ thống hỗ trợ.
        * ` StrategicAlignmentAgent` đánh giá xem đề xuất có phù hợp với mục tiêu chiến lược hiện tại của TRM không.
        * ` UserInteractionAgent` có thể trình bày đề xuất cho các chuyên gia hoặc người quản trị để lấy ý kiến phản hồi và phê duyệt.
    5.  **Phê duyệt và Ưu tiên hóa Tối ưu (`LearningAndOptimizationAgent`, người quản trị):**
        *   Dựa trên đánh giá tác động, tính khả thi, và phản hồi, các `ImprovementProposal` được phê duyệt hoặc từ chối.
        *   Các đề xuất được phê duyệt sẽ được ưu tiên hóa để triển khai.
    6.  **Triển khai Tối ưu hóa (`LearningAndOptimizationAgent`, `OntologyManagementAgent`, các agent liên quan):**
        * ` LearningAndOptimizationAgent` điều phối việc triển khai:
            *   Nếu liên quan đến ontology: Yêu cầu `OntologyManagementAgent` thực hiện các thay đổi (ví dụ: cập nhật `ProcessNode`, `AgentProfileNode`, `SolutionPatternNode`).
            *   Nếu liên quan đến cấu hình agent: Gửi yêu cầu cập nhật cấu hình đến các agent liên quan.
            *   Nếu liên quan đến quy trình nghiệp vụ: Cập nhật tài liệu, thông báo cho người dùng.
        *   Phát `SystemOptimizationImplementedEvent`.
    7.  **Giám sát và Đánh giá Hiệu quả Tối ưu hóa (`LearningAndOptimizationAgent`, `DataCollectionAgent`):**
        *   Sau khi triển khai, `LearningAndOptimizationAgent` cùng `DataCollectionAgent` theo dõi các KPIs liên quan để đánh giá hiệu quả của sự thay đổi.
        *   So sánh hiệu suất trước và sau khi tối ưu.
    8.  **Phổ biến Tri thức và Chuẩn hóa (`LearningAndOptimizationAgent`, `OntologyManagementAgent`, `NotificationAgent`):**
        *   Nếu tối ưu hóa thành công, các bài học và kết quả được ghi nhận và cập nhật vào `KnowledgeBase` của TRM-OS thông qua `OntologyManagementAgent`.
        *   Các thay đổi, quy trình mới, hoặc `SolutionPattern` mới được chuẩn hóa và phổ biến.
        * ` NotificationAgent` thông báo cho các agent và người dùng liên quan về các cập nhật và tri thức mới.
*   **Tương Tác Dữ liệu và Ontology:**
    *   **Neo4j Aura:**
        *   Đọc dữ liệu từ nhiều loại nút và quan hệ (`Project`, `Task`, `Issue`, `Tension`, `AgentLog`, `UserFeedback`, `LessonLearned`).
        *   Tạo và quản lý các nút `SystemInsightNode`, `ImprovementProposalNode`.
        *   Cập nhật các nút `ProcessNode`, `AgentProfileNode`, `SolutionPatternNode`, `KnowledgeDomainNode`, `OntologySchemaDefinition` (nếu cần điều chỉnh cấu trúc ontology).
        *   Liên kết các `ImprovementProposal` với các `SystemInsight` và các thành phần ontology mà nó tác động.
    *   **Supabase (PostgreSQL/Vector):**
        *   Lưu trữ logs chi tiết, dữ liệu metrics hiệu suất lớn.
        *   Lưu trữ các phiên bản của mô hình ML được `LearningAndOptimizationAgent` sử dụng (nếu có).
        *   Lưu trữ tài liệu liên quan đến các đề xuất tối ưu hóa và kết quả đánh giá.
*   **Sự Kiện Phát Sinh (Ví dụ):**
    * ` HighFrequencyIssueDetectedEvent` (đầu vào)
    * ` SystemInsightGeneratedEvent`
    * ` ImprovementProposalCreatedEvent`
    * ` ImprovementProposalReviewRequestEvent`
    * ` ImprovementProposalApprovedEvent` / `ImprovementProposalRejectedEvent`
    * ` SystemOptimizationImplementedEvent`
    * ` OptimizationEffectivenessReportedEvent`
    * ` KnowledgeBaseUpdatedEvent` (thông báo về tri thức mới được chuẩn hóa)
*   **Ví dụ Minh Họa Cụ Thể:**
    *   **Kích hoạt:** `LearningAndOptimizationAgent` (LOA) chạy phân tích định kỳ hàng tháng.
    *   **Phân tích:** LOA phát hiện rằng 70% các `Project` thuộc `ProjectType: "InternalToolDevelopment"` vượt quá ngân sách thời gian trung bình 15% ở giai đoạn `Phase: "Testing"`. Đồng thời, nhiều `LessonLearned` từ các dự án này chỉ ra "thiếu kịch bản kiểm thử toàn diện".
    *   **Insight:** `SystemInsight: SI012` - "Quy trình kiểm thử cho dự án phát triển công cụ nội bộ chưa đủ bao quát, dẫn đến kéo dài thời gian và chi phí."
    *   **Đề xuất:** `ImprovementProposal: IP008` - "Cập nhật `ProcessTemplate: PT_InternalToolDev` bằng cách bổ sung một `TaskTemplate: "ComprehensiveTestScenarioDesign"` bắt buộc trong giai đoạn `Planning`, đồng thời cung cấp một `SolutionPattern: SP_TestScenarioChecklist_V1` làm tài liệu tham khảo."
    *   **Xác thực & Phê duyệt:** Đề xuất được gửi tới Trưởng phòng Phát triển và QA Lead qua `UserInteractionAgent`. Sau khi thảo luận và điều chỉnh nhỏ, đề xuất được phê duyệt.
    *   **Triển khai:** `OntologyManagementAgent` cập nhật `ProcessTemplate: PT_InternalToolDev` và tạo mới `SolutionPattern: SP_TestScenarioChecklist_V1`. `NotificationAgent` thông báo cho các PM và team leads.
    *   **Đánh giá:** Sau 3 tháng, LOA phân tích lại và thấy tỷ lệ dự án trễ ở giai đoạn Testing giảm xuống còn 5%.
    *   **Phổ biến:** Kết quả tích cực được ghi nhận, `SP_TestScenarioChecklist_V1` được đánh dấu là "BestPractice".

#### 10.5.9. Luồng Tác vụ 9: Phát hiện, Đánh giá và Giải quyết Căng thẳng/Rủi ro Chủ động Toàn cục (TRM-OS)

*   **Agents Tham Gia Chính:**
    * ` TensionDetectionAgent` (chủ đạo trong việc phát hiện)
    * ` RiskAssessmentAgent` (đánh giá mức độ nghiêm trọng và tác động của rủi ro/căng thẳng)
    * ` ResolutionCoordinatorAgent` (điều phối các nỗ lực giải quyết)
    * ` OntologyManagementAgent` (cung cấp thông tin ngữ cảnh, cập nhật trạng thái)
    * ` StrategicAlignmentAgent` (đảm bảo giải pháp phù hợp chiến lược)
    * ` ResourceManagementAgent` (nếu liên quan đến xung đột nguồn lực)
    * ` LearningAndOptimizationAgent` (ghi nhận bài học từ việc giải quyết căng thẳng/rủi ro)
    * ` UserInteractionAgent` (thông báo, thu thập thông tin từ con người nếu cần)
    * ` NotificationAgent`
    * ` EventDispatcherAgent`
*   **Điều Kiện Kích Hoạt (Trigger):**
    *   **Liên tục/Định kỳ:** `TensionDetectionAgent` và `RiskAssessmentAgent` quét hệ thống theo lịch trình.
    *   **Sự kiện:**
        * ` PotentialSystemicTensionDetectedEvent` do `TensionDetectionAgent` phát hiện (ví dụ: nhiều dự án cùng yêu cầu một nguồn lực khan hiếm sắp tới, một thay đổi trong ontology có thể gây xung đột với các quy trình hiện hành).
        * ` EmergingSystemicRiskIdentifiedEvent` do `RiskAssessmentAgent` phát hiện (ví dụ: một công nghệ chủ chốt sắp lỗi thời, một đối tác quan trọng gặp vấn đề).
        *   Một `Issue` hoặc `Tension` ở cấp độ dự án được leo thang do không giải quyết được và có khả năng ảnh hưởng rộng.
        * ` UserReportedSystemicConcernEvent` từ người dùng thông qua `UserInteractionAgent`.
*   **Mục Tiêu:**
    *   Chủ động xác định và phân tích các căng thẳng, xung đột tiềm ẩn hoặc rủi ro mang tính hệ thống có thể ảnh hưởng đến hoạt động ổn định, hiệu quả hoặc mục tiêu chiến lược của TRM-OS.
    *   Đánh giá mức độ ưu tiên, tác động tiềm tàng và tính khẩn cấp của các căng thẳng/rủi ro được phát hiện.
    *   Xây dựng và điều phối việc thực hiện các kế hoạch giải quyết hoặc giảm thiểu.
    *   Đảm bảo các giải pháp là tối ưu cho toàn hệ thống và phù hợp với chiến lược chung.
    *   Cập nhật ontology với thông tin về các căng thẳng/rủi ro đã xác định, trạng thái giải quyết và các bài học kinh nghiệm.
    *   Giảm thiểu sự gián đoạn và tối đa hóa khả năng phục hồi của TRM-OS.
*   **Luồng Các Bước Thực Hiện Chi Tiết:**
    1.  **Phát hiện Căng thẳng/Rủi ro Hệ thống (`TensionDetectionAgent`, `RiskAssessmentAgent`):**
        * ` TensionDetectionAgent` liên tục phân tích dữ liệu từ ontology (ví dụ: kế hoạch dự án, phân bổ nguồn lực, phụ thuộc giữa các `OntologyElement`) và các nguồn khác để tìm kiếm các dấu hiệu bất thường hoặc xung đột tiềm ẩn.
        * ` RiskAssessmentAgent` phân tích các yếu tố bên trong và bên ngoài (ví dụ: thay đổi công nghệ, thị trường, đối tác) để xác định các rủi ro mới nổi có thể ảnh hưởng đến TRM-OS.
        *   Khi phát hiện, các agent này phát ra `PotentialSystemicTensionDetectedEvent` hoặc `EmergingSystemicRiskIdentifiedEvent` với thông tin chi tiết.
    2.  **Xác minh và Đánh giá Sơ bộ (`ResolutionCoordinatorAgent`, `OntologyManagementAgent`):**
        * ` ResolutionCoordinatorAgent` nhận sự kiện, truy vấn `OntologyManagementAgent` để thu thập thêm ngữ cảnh.
        *   Xác minh tính hợp lệ và phạm vi ảnh hưởng của căng thẳng/rủi ro. Loại bỏ các cảnh báo sai.
        *   Tạo một nút `SystemicIssueNode` (hoặc `SystemicRiskNode`) trong ontology với trạng thái "Mới phát hiện".
    3.  **Phân tích Chi tiết và Đánh giá Tác động (`RiskAssessmentAgent`, `StrategicAlignmentAgent`, `ResourceManagementAgent`):**
        * ` RiskAssessmentAgent` thực hiện phân tích sâu hơn về nguyên nhân, tác động tiềm tàng (về chi phí, thời gian, chất lượng, mục tiêu chiến lược), và xác suất xảy ra.
        * ` StrategicAlignmentAgent` đánh giá mức độ ảnh hưởng đến các mục tiêu chiến lược của TRM.
        * ` ResourceManagementAgent` phân tích nếu căng thẳng/rủi ro liên quan đến nguồn lực.
        *   Kết quả phân tích được cập nhật vào `SystemicIssueNode`/`SystemicRiskNode`.
    4.  **Ưu tiên hóa và Quyết định Hành động (`ResolutionCoordinatorAgent`, `StrategicAlignmentAgent`):**
        *   Dựa trên kết quả phân tích tác động và mức độ khẩn cấp, `ResolutionCoordinatorAgent` phối hợp với `StrategicAlignmentAgent` để ưu tiên các căng thẳng/rủi ro cần giải quyết.
        *   Quyết định về chiến lược tiếp cận: chấp nhận, giảm thiểu, chuyển giao, hoặc né tránh rủi ro/căng thẳng.
    5.  **Xây dựng Kế hoạch Giải quyết/Giảm thiểu (`ResolutionCoordinatorAgent`, các agent chuyên môn liên quan):**
        * ` ResolutionCoordinatorAgent` chủ trì việc xây dựng kế hoạch hành động.
        *   Tùy thuộc vào bản chất của vấn đề, có thể huy động các agent khác:
            * ` ProjectPlanningAgent` nếu cần điều chỉnh kế hoạch nhiều dự án.
            * ` LearningAndOptimizationAgent` nếu cần thay đổi quy trình hoặc `SolutionPattern`.
            * ` ResourceManagementAgent` nếu cần tái phân bổ nguồn lực.
        *   Kế hoạch bao gồm các bước cụ thể, người chịu trách nhiệm (có thể là agent hoặc người), và thời hạn. Kế hoạch được lưu trữ hoặc liên kết với `SystemicIssueNode`/`SystemicRiskNode`.
    6.  **Triển khai Kế hoạch Hành động (`ResolutionCoordinatorAgent` và các agent được phân công):**
        * ` ResolutionCoordinatorAgent` giám sát và điều phối việc thực hiện kế hoạch.
        *   Các agent được phân công thực hiện nhiệm vụ của mình.
        * ` OntologyManagementAgent` cập nhật ontology theo các thay đổi (ví dụ: điều chỉnh `DependencyLink`, cập nhật `ResourceAllocation`).
    7.  **Theo dõi, Đánh giá và Điều chỉnh (`ResolutionCoordinatorAgent`, `ProgressTrackingAgent` - mở rộng):**
        * ` ResolutionCoordinatorAgent` theo dõi tiến độ giải quyết.
        * ` ProgressTrackingAgent` (có thể mở rộng vai trò) theo dõi các chỉ số liên quan đến việc giảm thiểu căng thẳng/rủi ro.
        *   Nếu kế hoạch không hiệu quả, quay lại bước 5 để điều chỉnh.
    8.  **Xác nhận Giải quyết và Lưu trữ Bài học (`ResolutionCoordinatorAgent`, `LearningAndOptimizationAgent`, `OntologyManagementAgent`):**
        *   Khi căng thẳng/rủi ro được giải quyết hoặc giảm thiểu đến mức chấp nhận được, `ResolutionCoordinatorAgent` xác nhận.
        * ` SystemicIssueNode`/`SystemicRiskNode` được cập nhật trạng thái "Đã giải quyết" hoặc "Đã giảm thiểu".
        * ` LearningAndOptimizationAgent` phân tích quá trình giải quyết để rút ra `LessonLearned` cho hệ thống, cập nhật vào `KnowledgeBase`.
        * ` OntologyManagementAgent` lưu trữ các thông tin này.
    9.  **Thông báo Kết quả (`NotificationAgent`, `EventDispatcherAgent`):**
        * ` ResolutionCoordinatorAgent` phát `SystemicIssueResolvedEvent` hoặc `SystemicRiskMitigatedEvent`.
        * ` EventDispatcherAgent` chuyển tiếp sự kiện.
        * ` NotificationAgent` thông báo cho các bên liên quan về kết quả.
*   **Tương Tác Dữ liệu và Ontology:**
    *   **Neo4j Aura:**
        *   Đọc dữ liệu từ toàn bộ ontology để phát hiện căng thẳng/rủi ro.
        *   Tạo và quản lý các nút `SystemicIssueNode`, `SystemicRiskNode`, `ResolutionPlanNode`.
        *   Cập nhật trạng thái, thuộc tính của các nút này và các nút liên quan (ví dụ: `Project`, `Resource`, `Process`) trong quá trình giải quyết.
        *   Liên kết `LessonLearned` với các `SystemicIssueNode`/`SystemicRiskNode` đã giải quyết.
    *   **Supabase (PostgreSQL/Vector):**
        *   Lưu trữ chi tiết các kế hoạch giải quyết phức tạp, báo cáo phân tích rủi ro.
        *   Lưu trữ logs trao đổi, quyết định liên quan đến việc giải quyết căng thẳng/rủi ro.
*   **Sự Kiện Phát Sinh (Ví dụ):**
    * ` PotentialSystemicTensionDetectedEvent` (đầu vào)
    * ` EmergingSystemicRiskIdentifiedEvent` (đầu vào)
    * ` SystemicIssueAnalysisCompletedEvent`
    * ` ResolutionPlanCreatedEvent`
    * ` SystemicIssueResolutionInProgressEvent`
    * ` SystemicIssueResolvedEvent` (đầu ra)
    * ` SystemicRiskMitigatedEvent` (đầu ra)
    * ` SystemicLearningCapturedEvent` (cho `LearningAndOptimizationAgent`)
*   **Ví dụ Minh Họa Cụ Thể:**
    *   **Phát hiện:** `TensionDetectionAgent` phát hiện `Project: P007` và `Project: P008` đều có kế hoạch sử dụng `Resource: QuantumComputingSimulator_License_1` (chỉ có 1 license) trong cùng một khoảng thời gian 2 tuần tới. Phát `PotentialSystemicTensionDetectedEvent: T015 - ResourceConflict`.
    *   **Xác minh & Phân tích:** `ResolutionCoordinatorAgent` xác nhận xung đột. `RiskAssessmentAgent` đánh giá tác động: nếu không giải quyết, cả hai dự án có thể trễ, ảnh hưởng đến mục tiêu ra mắt sản phẩm quý.
    *   **Ưu tiên & Kế hoạch:** `StrategicAlignmentAgent` xác định `P008` có ưu tiên cao hơn. `ResolutionCoordinatorAgent` làm việc với `ProjectPlanningAgent` của `P007` và `P008`, và `ResourceManagementAgent`. Kế hoạch: `P007` lùi lịch sử dụng simulator 1 tuần, đồng thời tìm kiếm khả năng thuê thêm license ngắn hạn.
    *   **Triển khai:** Kế hoạch được thực hiện. `OntologyManagementAgent` cập nhật lịch trình của `P007` và `P008`.
    *   **Xác nhận & Bài học:** Xung đột được giải quyết. `LearningAndOptimizationAgent` ghi nhận `LessonLearned: LL045` - "Cần cải thiện quy trình đăng ký nguồn lực khan hiếm, xem xét cơ chế cảnh báo sớm hơn khi có nhiều hơn X yêu cầu tiềm năng."
    *   **Thông báo:** Các PM của P007, P008 và quản lý nguồn lực được thông báo.



**PHẦN D: ỨNG DỤNG ONTOLOGY VÀO THỰC TẾ VÀ TRIỂN KHAI (APPLIED ONTOLOGY & IMPLEMENTATION)**
11. Ánh xạ Ontology với Dữ liệu và Hệ thống Thực tế của TRM
    11.1. Xác định Nguồn Dữ liệu Thực tế (Ban đầu và Tiềm năng)
        * **11.1.1. Input trực tiếp từ Founder/Thành viên chủ chốt (Ưu tiên cao nhất ban đầu):**
            * **Nội dung:** Các `Tension` (vấn đề, cơ hội, ý tưởng), `Recognition` (ghi nhận), định hướng chiến lược, mục tiêu, các `ProjectProposal` ban đầu.
            * **Hình thức:** Phỏng vấn trực tiếp, ghi chú, email, tin nhắn.
            * **Tần suất:** Liên tục, đặc biệt trong giai đoạn đầu và khi có thay đổi lớn.
        * **11.1.2. Các công cụ SaaS cốt lõi đang sử dụng (Ví dụ):**
            * **Google Workspace (Docs, Sheets, Slides, Calendar, Gmail):**
                * ` KnowledgeSnippet` từ tài liệu, báo cáo, kế hoạch.
                * ` Project` và `Task` từ các file Google Sheets theo dõi công việc.
                * ` Event` từ Lịch (cuộc họp, deadline).
                * ` CommunicationEvent` (một loại `Event`) từ Gmail (cần cân nhắc kỹ về quyền riêng tư và bộ lọc).
            * **Công cụ quản lý dự án (Nếu có, ví dụ: Trello, Asana, Jira, Notion):**
                * ` Project`, `Task`, `status`, `assigneeAgentId`, `dueDate`.
                * ` ProjectEvent` (task created, completed, comment added).
            * **Công cụ Chat/Collaboration (Slack, Microsoft Teams - Nếu có):**
                * ` CommunicationEvent`, `Tension` (thảo luận trong kênh), `Recognition` (public praise).
                *   Cần cơ chế lọc và tóm tắt thông minh để tránh nhiễu.
            * **Công cụ CRM (Nếu có, ví dụ: HubSpot, Salesforce, Pipedrive):**
                * ` ExternalAgent` (khách hàng, đối tác), `CommunicationEvent` (email, call log).
                * ` Tension` (customer feedback, issues).
            * **Công cụ Kế toán/Tài chính (Nếu có, ví dụ: Xero, QuickBooks):**
                * ` FinancialResource`, `Project` (có thể liên kết với chi phí).
        * **11.1.3. Tài liệu nội bộ khác:**
            *   Các quy trình, chính sách, hướng dẫn dưới dạng file (PDF, Word).
            *   Các bản ghi chú cá nhân có cấu trúc (nếu được chia sẻ).
        * **11.1.4. Logs hệ thống (System Logs - cho giai đoạn sau):**
            *   Logs từ các ứng dụng nội bộ, website (nếu có) để phát hiện `SystemEvent`, `FailureEvent`.
    11.2. Data Pipeline: Thu thập, Xử lý và Tích hợp Dữ liệu
        * **11.2.1. Sơ đồ Data Pipeline Tổng quan:**
            * **Mô tả:** Dữ liệu từ các nguồn đa dạng (SaaS, Docs, Founder Input) sẽ được thu thập và xử lý bởi các `DataSensingAgent` (có thể là Python scripts, Supabase Edge Functions, hoặc các công cụ ETL chuyên dụng nếu cần trong tương lai). Dữ liệu thô sau đó được đưa vào một khu vực staging (có thể là Snowflake hoặc một storage tạm thời).
            * ` KnowledgeExtractionAgent` sẽ lấy dữ liệu từ staging, thực hiện các bước: làm sạch, chuẩn hóa, trích xuất thực thể và mối quan hệ theo ontology, tạo `KnowledgeSnippet`, và tạo embeddings (sử dụng các model từ Replicate API hoặc các thư viện embedding). 
            *   Dữ liệu có cấu trúc (nodes, relationships) sẽ được lưu trữ vào **Neo4j Aura**.
            *   Dữ liệu vector (embeddings của `KnowledgeSnippet`, mô tả `Project`, etc.) sẽ được lưu trữ vào **Supabase Vector**.
            * **Snowflake** đóng vai trò là data lake/warehouse trung tâm cho dữ liệu thô, dữ liệu đã xử lý và các phân tích sâu hơn nếu cần.
            *   Các AI Agent (bao gồm AGE) sẽ tương tác chủ yếu với Neo4j Aura (truy vấn graph, cập nhật graph) và Supabase Vector (tìm kiếm ngữ nghĩa) để thực hiện các tác vụ của mình.

            ```yamlmermaid
            graph LR
                A[Founder Input] --> B(DataSensingAgent / Scripts);
                C[SaaS APIs] --> B;
                D[Google Workspace] --> B;
                E[Internal Docs] --> B;
                B --> F{Staging Area / Snowflake Data Lake};
                F --> G(KnowledgeExtractionAgent);
                G -- Text for Embedding --> H(Embedding Model / Replicate API);
                H -- Embeddings --> I[Supabase Vector Store];
                G -- Structured Data --> J[Neo4j Aura Graph DB];
                K[AI Agents / AGE] <--> J;
                K <--> I;
                F --> L[Data Warehouse / Snowflake];
                L --> K;
            ```yaml
            *(Chú thích: Sơ đồ Mermaid trên là minh họa, cần được tích hợp vào file Markdown nếu công cụ hỗ trợ render, nếu không thì giữ dạng text mô tả)*
        * **11.2.2. Vai trò của `DataSensingAgent` trong Data Pipeline:**
            * **Kết nối Nguồn:** `DataSensingAgent` (hoặc các scripts/functions chuyên biệt do nó quản lý) chịu trách nhiệm thiết lập và duy trì kết nối tới các nguồn dữ liệu đã định nghĩa (Google Workspace APIs, Project Management Tool APIs, cơ sở dữ liệu, file systems).
            * **Thu thập Theo lịch trình hoặc Trigger:** Việc thu thập có thể được thực hiện theo lịch trình định sẵn (e.g., quét Google Drive mỗi giờ) hoặc được kích hoạt bởi một `Event` (e.g., Founder gửi email chứa từ khóa đặc biệt).
            * **Tiền xử lý Cơ bản:** Thực hiện các bước làm sạch tối thiểu như loại bỏ ký tự không cần thiết, chuyển đổi encoding, kiểm tra định dạng cơ bản trước khi đẩy vào Staging Area.
            * **Ghi nhận Hoạt động:** Tạo `SystemEvent` trong Neo4j Aura để ghi lại thông tin về mỗi lần thu thập (e.g., `DataIngested {source: "GoogleDrive", timestamp: ..., status: "Success", itemCount: 10}`).
            * **Đẩy vào Staging Area (Snowflake/Storage):** Dữ liệu thô hoặc đã qua tiền xử lý cơ bản được lưu trữ vào Snowflake (hoặc một hệ thống lưu trữ tạm thời khác) để `KnowledgeExtractionAgent` tiếp tục xử lý.

        * **11.2.3. Vai trò của `KnowledgeExtractionAgent` trong Data Pipeline:**
            * **Lấy dữ liệu từ Staging:** Theo dõi Staging Area hoặc được trigger bởi `SystemEvent` từ `DataSensingAgent` để lấy dữ liệu cần xử lý.
            * **Phân tích và Trích xuất Sâu:**
                *   Sử dụng LLMs và các mô hình NLP để hiểu ngữ nghĩa, trích xuất các thực thể (`Project`, `Task`, `Tension`, `Person`, `Organization`, `Skill`, `Recognition`), thuộc tính của chúng, và các mối quan hệ tiềm năng giữa chúng từ dữ liệu phi cấu trúc (văn bản, email) hoặc bán cấu trúc.
                *   Đối với dữ liệu có cấu trúc (e.g., từ Google Sheets, DBs), agent sẽ ánh xạ các trường dữ liệu vào các thuộc tính của ontology theo quy tắc đã định nghĩa.
            * **Tạo và Lưu trữ `KnowledgeSnippet`:** Các đoạn thông tin quan trọng, có thể tái sử dụng được trích xuất và lưu thành các node `KnowledgeSnippet`.
            * **Tạo Embeddings:** Với mỗi `KnowledgeSnippet` hoặc các trường văn bản quan trọng khác (e.g., mô tả `Project`, `Tension`), agent sẽ gọi tới Embedding Model (qua Replicate API hoặc thư viện local) để tạo vector embedding.
            * **Lưu trữ vào Neo4j Aura:** Các node thực thể và mối quan hệ đã được trích xuất và chuẩn hóa sẽ được `MERGE` vào Neo4j Aura, đảm bảo tính idempotent.
            * **Lưu trữ vào Supabase Vector:** Các vector embedding được lưu trữ trong Supabase Vector, liên kết với ID của `KnowledgeSnippet` hoặc thực thể tương ứng trong Neo4j.
            * **Ghi nhận Hoạt động:** Tạo `SystemEvent` hoặc `LearningEvent` để ghi lại kết quả của quá trình trích xuất (e.g., `KnowledgeExtracted {sourceNodeId: ..., newNodesCreated: 5, newRelationsCreated: 3}`).
    11.3. Ánh xạ Thực thể Ontology với Đối tượng Dữ liệu Cụ thể
        * **Ví dụ cụ thể về ánh xạ:**
            * **`Tension` từ Founder Input:**
                * **Nguồn:** Email từ Founder với tiêu đề "Ý tưởng cải thiện quy trình onboarding".
                * **Dữ liệu thô:** Nội dung email mô tả vấn đề: "Quy trình onboarding nhân viên mới hiện tại còn thủ công, mất nhiều thời gian, cần tự động hóa một số bước để nhân viên mới nhanh chóng hòa nhập."
                * **Ánh xạ Ontology:**
                    *   Tạo node `Tension`:
                        * ` tensionId`: "TEN-ONBOARDING-001"
                        * ` description`: "Quy trình onboarding nhân viên mới thủ công, mất thời gian, cần tự động hóa."
                        * ` source`: "Founder Email - 2025-06-10"
                        * ` priority`: (Founder xác định hoặc AGE đề xuất)
                        * ` status`: "Open"
                    *   Tạo node `InternalAgent` (nếu chưa có) cho Founder.
                    *   Tạo mối quan hệ `(Tension)-[:DETECTED_BY]->(InternalAgent_Founder)`.

            * **`Project` và `Task` từ Google Sheet theo dõi dự án "Website Relaunch":**
                * **Nguồn:** Google Sheet "Project Tracker - Website Relaunch".
                * **Dữ liệu thô (một dòng trong Sheet):**
                    *   Cột A (Project Name): Website Relaunch
                    *   Cột B (Task Name): Design Homepage Mockup
                    *   Cột C (Assignee): DesignerX
                    *   Cột D (Status): In Progress
                    *   Cột E (Due Date): 2025-07-15
                * **Ánh xạ Ontology:**
                    *   Tạo/Cập nhật node `ActiveProject` (nếu `Project Name` là mới hoặc đã tồn tại):
                        * ` projectId`: "PRJ-WEBSITE-001"
                        * ` name`: "Website Relaunch"
                        * ` status`: "Active"
                    *   Tạo node `Task`:
                        * ` taskId`: "TASK-WEB-HOME-001"
                        * ` name`: "Design Homepage Mockup"
                        * ` status`: "InProgress"
                        * ` dueDate`: "2025-07-15"
                    *   Tạo node `InternalAgent` cho "DesignerX" (nếu chưa có).
                    *   Tạo mối quan hệ `(Task)-[:IS_PART_OF_PROJECT]->(Project)`.
                    *   Tạo mối quan hệ `(Task)-[:PERFORMED_ACTION {role: "assignee"}]->(InternalAgent_DesignerX)` (hoặc `(InternalAgent_DesignerX)-[:PERFORMED_ACTION {role: "assignee"}]->(Task)` tùy quy ước hướng).

            * **`KnowledgeSnippet` từ Google Doc "Best Practices for API Design":**
                * **Nguồn:** Google Doc ID "abcdef123456".
                * **Dữ liệu thô (một đoạn trong Doc):** "Khi thiết kế API, luôn ưu tiên tính nhất quán trong việc đặt tên endpoint và cấu trúc response. Sử dụng versioning (ví dụ: /v1/, /v2/) để quản lý các thay đổi không tương thích ngược."
                * **Ánh xạ Ontology:**
                    *   Tạo node `KnowledgeSnippet`:
                        * ` snippetId`: "KS-APIDESIGN-001"
                        * ` content`: "Khi thiết kế API, luôn ưu tiên tính nhất quán... thay đổi không tương thích ngược."
                        * ` source`: "Google Doc ID: abcdef123456 - Section: Naming Conventions"
                        * ` keywords`: ["API Design", "Consistency", "Versioning", "Best Practices"]
                        * ` embeddingVector`: (Vector được tạo bởi Embedding Model)
                    *   (Có thể liên kết `KnowledgeSnippet` này với `Skill` "API Design" hoặc các `Project` liên quan đến phát triển API).

        * **(Bảng ánh xạ chi tiết hơn sẽ được xây dựng dần khi triển khai thực tế, bao gồm các quy tắc cụ thể để trích xuất và chuyển đổi dữ liệu từ từng nguồn.)**
12. Triển khai Ontology trên Neo4j Aura
    12.1. Định nghĩa Schema (Node Labels, Relationship Types, Properties) bằng Cypher DDL
        * **12.1.1. Constraints (Ràng buộc):**
            *   Đảm bảo tính duy nhất và sự tồn tại của các thuộc tính định danh quan trọng.
            ```yamlcypher
            // Constraints for Agent
            CREATE CONSTRAINT agent_id_unique IF NOT EXISTS FOR (a:Agent) REQUIRE a.agentId IS UNIQUE;
            CREATE CONSTRAINT agent_id_exists IF NOT EXISTS FOR (a:Agent) REQUIRE a.agentId IS NOT NULL;
            CREATE CONSTRAINT agent_name_exists IF NOT EXISTS FOR (a:Agent) REQUIRE a.name IS NOT NULL; 
            // (Tương tự cho InternalAgent, ExternalAgent, AIAgent, AGE nếu có thuộc tính ID riêng)

            // Constraints for Event
            CREATE CONSTRAINT event_id_unique IF NOT EXISTS FOR (e:Event) REQUIRE e.eventId IS UNIQUE;
            CREATE CONSTRAINT event_id_exists IF NOT EXISTS FOR (e:Event) REQUIRE e.eventId IS NOT NULL;
            CREATE CONSTRAINT event_type_exists IF NOT EXISTS FOR (e:Event) REQUIRE e.eventType IS NOT NULL;
            CREATE CONSTRAINT event_timestamp_exists IF NOT EXISTS FOR (e:Event) REQUIRE e.timestamp IS NOT NULL;

            // Constraints for Project
            CREATE CONSTRAINT project_id_unique IF NOT EXISTS FOR (p:Project) REQUIRE p.projectId IS UNIQUE;
            CREATE CONSTRAINT project_id_exists IF NOT EXISTS FOR (p:Project) REQUIRE p.projectId IS NOT NULL;
            CREATE CONSTRAINT project_name_exists IF NOT EXISTS FOR (p:Project) REQUIRE p.name IS NOT NULL;

            // Constraints for Task
            CREATE CONSTRAINT task_id_unique IF NOT EXISTS FOR (t:Task) REQUIRE t.taskId IS UNIQUE;
            CREATE CONSTRAINT task_id_exists IF NOT EXISTS FOR (t:Task) REQUIRE t.taskId IS NOT NULL;

            // Constraints for Resource
            CREATE CONSTRAINT resource_id_unique IF NOT EXISTS FOR (r:Resource) REQUIRE r.resourceId IS UNIQUE;
            CREATE CONSTRAINT resource_id_exists IF NOT EXISTS FOR (r:Resource) REQUIRE r.resourceId IS NOT NULL;

            // Constraints for Tension
            CREATE CONSTRAINT tension_id_unique IF NOT EXISTS FOR (t:Tension) REQUIRE t.tensionId IS UNIQUE;
            CREATE CONSTRAINT tension_id_exists IF NOT EXISTS FOR (t:Tension) REQUIRE t.tensionId IS NOT NULL;

            // Constraints for Recognition
            CREATE CONSTRAINT recognition_id_unique IF NOT EXISTS FOR (r:Recognition) REQUIRE r.recognitionId IS UNIQUE;
            CREATE CONSTRAINT recognition_id_exists IF NOT EXISTS FOR (r:Recognition) REQUIRE r.recognitionId IS NOT NULL;

            // Constraints for WIN
            CREATE CONSTRAINT win_id_unique IF NOT EXISTS FOR (w:WIN) REQUIRE w.winId IS UNIQUE;
            CREATE CONSTRAINT win_id_exists IF NOT EXISTS FOR (w:WIN) REQUIRE w.winId IS NOT NULL;

            // Constraints for Skill
            CREATE CONSTRAINT skill_id_unique IF NOT EXISTS FOR (s:Skill) REQUIRE s.skillId IS UNIQUE;
            CREATE CONSTRAINT skill_id_exists IF NOT EXISTS FOR (s:Skill) REQUIRE s.skillId IS NOT NULL;
            CREATE CONSTRAINT skill_name_unique IF NOT EXISTS FOR (s:Skill) REQUIRE s.name IS UNIQUE; 

            // Constraints for KnowledgeSnippet
            CREATE CONSTRAINT snippet_id_unique IF NOT EXISTS FOR (ks:KnowledgeSnippet) REQUIRE ks.snippetId IS UNIQUE;
            CREATE CONSTRAINT snippet_id_exists IF NOT EXISTS FOR (ks:KnowledgeSnippet) REQUIRE ks.snippetId IS NOT NULL;
            ```yaml

        * **12.1.2. Indexes (Chỉ mục):**
            *   Tăng tốc độ truy vấn trên các thuộc tính thường xuyên được tìm kiếm.
            ```yamlcypher
            // Indexes for Agent
            CREATE INDEX agent_name_index IF NOT EXISTS FOR (a:Agent) ON (a.name);
            CREATE INDEX agent_type_index IF NOT EXISTS FOR (a:Agent) ON (a.type);

            // Indexes for Event
            CREATE INDEX event_type_index IF NOT EXISTS FOR (e:Event) ON (e.eventType);
            CREATE INDEX event_timestamp_index IF NOT EXISTS FOR (e:Event) ON (e.timestamp);
            CREATE INDEX event_source_index IF NOT EXISTS FOR (e:Event) ON (e.source);

            // Indexes for Project
            CREATE INDEX project_name_index IF NOT EXISTS FOR (p:Project) ON (p.name);
            CREATE INDEX project_status_index IF NOT EXISTS FOR (p:Project) ON (p.status);

            // Indexes for Task
            CREATE INDEX task_status_index IF NOT EXISTS FOR (t:Task) ON (t.status);
            CREATE INDEX task_assignee_index IF NOT EXISTS FOR (t:Task) ON (t.assigneeAgentId);

            // Indexes for Tension
            CREATE INDEX tension_status_index IF NOT EXISTS FOR (t:Tension) ON (t.status);
            CREATE INDEX tension_priority_index IF NOT EXISTS FOR (t:Tension) ON (t.priority);

            // Indexes for KnowledgeSnippet
            CREATE INDEX ks_creation_date_index IF NOT EXISTS FOR (ks:KnowledgeSnippet) ON (ks.creationDate);
            // Lưu ý: Embedding vectors sẽ được tìm kiếm qua Supabase Vector, không phải index trực tiếp trong Neo4j cho tìm kiếm ngữ nghĩa.
            ```yaml

        * **12.1.3. Ví dụ tạo Node và Relationship mẫu (sử dụng MERGE để tránh trùng lặp khi chạy lại):**
            ```yamlcypher
            // Tạo Founder Agent
            MERGE (founder:InternalAgent:Agent {agentId: 'founder_trm_01'})
            ON CREATE SET founder.name = 'TRM Founder', founder.type = 'Internal', founder.description = 'Founding member of TRM', founder.creationDate = datetime()

            // Tạo một AIAgent mẫu
            MERGE (ds_agent:AIAgent:Agent {agentId: 'ai_datasensing_01'})
            ON CREATE SET ds_agent.name = 'DataSensingAgent_Alpha', ds_agent.type = 'AI', ds_agent.description = 'Responsible for collecting data from various sources.', ds_agent.creationDate = datetime()

            // Tạo AGE
            MERGE (age_engine:AGE:Agent {agentId: 'age_core_01'})
            ON CREATE SET age_engine.name = 'GenesisEngine_Prime', age_engine.type = 'AGE', age_engine.description = 'Core Artificial Genesis Engine.', age_engine.creationDate = datetime()
            WITH age_engine, ds_agent
            MERGE (age_engine)-[r:MANAGES_AGENT]->(ds_agent)
            ON CREATE SET r.controlLevel = 'Coordination'

            // Tạo một Skill mẫu
            MERGE (skill_python:Skill {skillId: 'skill_py_001'})
            ON CREATE SET skill_python.name = 'Python Programming', skill_python.category = 'Technical', skill_python.description = 'Proficiency in Python language.'
            WITH founder, skill_python
            MERGE (founder)-[r:HAS_SKILL]->(skill_python)
            ON CREATE SET r.proficiencyLevel = 5, r.lastUsed = date()

            // Tạo một Tension mẫu
            MERGE (tension1:Tension {tensionId: 'ten_init_001'})
            ON CREATE SET 
                tension1.description = 'Initial system setup requires defining core ontology.', 
                tension1.source = 'System Requirement', 
                tension1.priority = 1, 
                tension1.status = 'Open', 
                tension1.creationDate = datetime()
            WITH tension1, founder
            MERGE (tension1)-[r:DETECTED_BY]->(founder)
            ON CREATE SET r.detectionMethod = 'Initial Analysis'

            // Tạo một ProjectProposal từ Tension
            MERGE (pp1:ProjectProposal:Project {projectId: 'pp_ontodev_001'})
            ON CREATE SET 
                pp1.name = 'Develop Core Ontology v3.2', 
                pp1.description = 'Define and implement the foundational TRM Ontology v3.2.', 
                pp1.status = 'Proposal', 
                pp1.priority = 1
            WITH pp1, tension1
            MERGE (pp1)-[r:RESOLVES_TENSION]->(tension1)
            ON CREATE SET r.resolutionStatus = 'Proposed'
            WITH pp1, founder // Founder tạo ra ProjectProposal này
            MERGE (founder)-[rel:PERFORMED_ACTION {role: 'proposer'}]->(pp1)
            ON CREATE SET rel.timestamp = datetime()

            // Tạo một KnowledgeSnippet mẫu
            MERGE (ks1:KnowledgeSnippet {snippetId: 'ks_neo4jbp_001'})
            ON CREATE SET 
                ks1.content = 'Always use MERGE for creating/updating nodes and relationships idempotently in setup scripts.', 
                ks1.source = 'Neo4j Best Practices', 
                ks1.keywords = ['Neo4j', 'Cypher', 'Idempotency', 'MERGE'], 
                ks1.creationDate = datetime()
            ```yaml
    12.2. Quy trình Nạp Dữ liệu Ban đầu (Initial Data Loading)
        * **Mục tiêu:** Đưa một lượng lớn dữ liệu lịch sử và hiện tại vào ontology để khởi tạo hệ thống.
        * **Các bước chính:**
            1.  **Xác định Ưu tiên Nguồn:** Bắt đầu với các nguồn dữ liệu quan trọng nhất và có cấu trúc tốt nhất (e.g., input trực tiếp từ Founder, danh sách dự án từ file Excel/Sheet, tài liệu chiến lược cốt lõi).
            2.  **Chuẩn bị Dữ liệu Thô:** Tập hợp dữ liệu, làm sạch sơ bộ nếu cần.
            3.  **Phát triển Scripts Nạp Một lần (One-time Scripts):** Viết các Python scripts sử dụng `DataSensingAgent` và `KnowledgeExtractionAgent` (hoặc các thành phần logic của chúng) để xử lý và nạp dữ liệu theo từng nguồn.
                *   Các script này cần có khả năng đọc dữ liệu từ nguồn (file, API), biến đổi theo mapping ontology, và ghi vào Neo4j Aura và Supabase Vector.
                *   Sử dụng `MERGE` trong Cypher để tránh tạo trùng lặp node và relationship.
            4.  **Thực thi và Kiểm tra:** Chạy scripts theo từng phần nhỏ, kiểm tra kỹ lưỡng dữ liệu được nạp vào Neo4j và Supabase Vector. So sánh với dữ liệu gốc.
            5.  **Tối ưu hóa:** Điều chỉnh scripts và quá trình nạp dựa trên kết quả kiểm tra và hiệu suất.
        * **Công cụ hỗ trợ:** Python, Pandas (cho xử lý dữ liệu dạng bảng), thư viện Neo4j Python Driver, Supabase Python Client.
        * **Lưu ý:**
            *   Quá trình này có thể mất nhiều thời gian và cần thực hiện cẩn thận.
            *   Ưu tiên tính đúng đắn của dữ liệu hơn là tốc độ trong giai đoạn này.
            *   Ghi log chi tiết quá trình nạp để dễ dàng debug khi có lỗi.

    12.3. Quy trình Cập nhật Dữ liệu Liên tục (Continuous Data Update)
        * **Mục tiêu:** Đảm bảo ontology luôn phản ánh trạng thái mới nhất của tổ chức bằng cách cập nhật thường xuyên các thay đổi từ nguồn dữ liệu.
        * **Cách thức hoạt động:**
            1.  **Lắng nghe Thay đổi (Change Data Capture - CDC) hoặc Quét Định kỳ:**
                * **Lý tưởng:** Sử dụng webhooks hoặc các cơ chế CDC từ SaaS tools để nhận thông báo ngay khi có thay đổi.
                * **Thực tế phổ biến:** `DataSensingAgent` quét các nguồn dữ liệu theo lịch trình (e.g., mỗi 15 phút, mỗi giờ) để phát hiện các bản ghi mới hoặc được cập nhật kể từ lần quét cuối.
            2.  **Xử lý Thay đổi:**
                * ` DataSensingAgent` lấy dữ liệu thay đổi và đưa vào Staging Area.
                * ` KnowledgeExtractionAgent` xử lý dữ liệu này tương tự như quá trình nạp ban đầu, nhưng tập trung vào việc cập nhật các node và relationship hiện có hoặc tạo mới nếu cần.
                *   Sử dụng `MERGE` với `ON CREATE SET` và `ON MATCH SET` trong Cypher để cập nhật thuộc tính của node/relationship một cách chính xác.
            3.  **Xử lý Xóa Dữ liệu (Soft Delete / Hard Delete):**
                *   Nếu một bản ghi bị xóa ở nguồn, cần có cơ chế để phản ánh điều này trong ontology.
                * **Soft Delete:** Thêm một thuộc tính như `isActive: false` hoặc `deletedTimestamp` cho node/relationship thay vì xóa hẳn. Điều này giúp bảo toàn lịch sử.
                * **Hard Delete:** Xóa node và các relationship liên quan (cần cẩn trọng và có quy tắc rõ ràng).
            4.  **Đảm bảo Tính nhất quán:** Xử lý các xung đột tiềm ẩn nếu dữ liệu từ nhiều nguồn cùng cập nhật một thực thể.
        * **Tần suất:** Phụ thuộc vào mức độ thay đổi của từng nguồn dữ liệu và yêu cầu về tính kịp thời của thông tin.
        * **Công cụ:** Tương tự như nạp ban đầu, nhưng tập trung vào các tác vụ lặp lại và tự động hóa (e.g., sử dụng Airflow, Celery, hoặc cron jobs để lên lịch cho các agent).

    13. Vận hành và Tương tác của AI Agent với Ontology

    Các AI Agent (bao gồm AGE) là người dùng chính của ontology. Chúng dựa vào ontology để hiểu bối cảnh, thực hiện suy luận và quyết định hành động. Dưới đây là các cách tương tác chính:

    **13.1. Truy vấn Neo4j Aura (Graph Queries)**
    AI Agents sử dụng Cypher queries để lấy thông tin từ graph database. Các loại truy vấn phổ biến:

    *   **Tìm kiếm Node cụ thể:**
        ```yamlcypher
        // Tìm một Agent theo ID
        MATCH (a:Agent {agentId: $agentIdParam}) RETURN a;

        // Tìm Project đang Active theo tên
        MATCH (p:ActiveProject) WHERE p.name CONTAINS $projectNameParam RETURN p;
        ```yaml

    *   **Lấy các Node liên quan:**
        ```yamlcypher
        // Tìm tất cả Task của một Project cụ thể (ví dụ: Project có projectId là 'proj123')
        MATCH (proj:Project {projectId: 'proj123'})-[:HAS_TASK]->(task:Task)
        RETURN task;

        // Hoặc sử dụng tham số, lấy các thuộc tính cụ thể của Task
        MATCH (proj:Project {projectId: $projectIdParam})-[:HAS_TASK]->(task:Task)
        RETURN task.name, task.status, task.dueDate;

        // Tìm tất cả Resource được gán cho một Task cụ thể
        MATCH (t:Task {taskId: $taskIdParam})-[:ASSIGNED_TO]->(r:Resource)
        RETURN r.name, r.type;

        // Tìm tất cả Event liên quan đến một Goal
        MATCH (g:Goal {goalId: $goalIdParam})<-[:RELATES_TO_GOAL]-(e:Event)
        RETURN e.type, e.description, e.timestamp;

        // Tìm tất cả Agent tham gia vào một Project và vai trò của họ (bao gồm cả thuộc tính của relationship)
        MATCH (agent:Agent)-[rel:PARTICIPATES_IN]->(proj:Project {projectId: $projectIdParam})
        RETURN agent.name, type(rel) AS role, rel.details AS participationDetails;

        // Lấy thông tin chi tiết của một WIN và các Project liên quan
        MATCH (win:WIN {winId: $winIdParam})-[:ACHIEVED_IN_PROJECT]->(project:Project)
        RETURN win, collect(project.name) AS relatedProjects;
        ```yaml

    *   **Đếm số lượng Node (Counting Nodes):**
        ```yamlcypher
        // Đếm tổng số Project đang hoạt động
        MATCH (p:ActiveProject)
        RETURN count(p) AS numberOfActiveProjects;

        // Đếm số Task có trạng thái 'PENDING' trong một Project
        MATCH (proj:Project {projectId: $projectIdParam})-[:HAS_TASK]->(t:Task {status: 'PENDING'})
        RETURN count(t) AS numberOfPendingTasks;
        ```yaml

    *   **Kiểm tra sự tồn tại của Relationship (Checking Relationship Existence):**
        ```yamlcypher
        // Kiểm tra xem một User có được gán cho một Task cụ thể không
        MATCH (u:User {userId: $userIdParam}), (t:Task {taskId: $taskIdParam})
        RETURN EXISTS((u)-[:ASSIGNED_TO]->(t)) AS isAssigned;
        ```yaml

    *   **Truy vấn theo đường dẫn phức tạp (Path Queries):**
        ```yamlcypher
        // Tìm tất cả các Founder và Project mà họ sở hữu, cùng với các Task của những Project đó
        MATCH path = (f:Founder)-[:OWNS_PROJECT]->(p:Project)-[:HAS_TASK]->(t:Task)
        WHERE f.name = 'TRM Founder' // Hoặc sử dụng $founderNameParam
        RETURN f.name AS founderName, p.name AS projectName, collect(t.name) AS tasks;

        // Tìm một đường đi ngắn nhất giữa hai Node (ví dụ: giữa một Resource và một Goal)
        MATCH (startNode:Resource {resourceId: $resourceIdParam}), (endNode:Goal {goalId: $goalIdParam}),
              pth = shortestPath((startNode)-[*]-(endNode)) // Sử dụng pth (path) thay vì p để tránh nhầm lẫn với node p
        RETURN pth;
        ```yaml

    *   **Truy vấn dựa trên Thuộc tính (Property-based Queries with filtering):**
        ```yamlcypher
        // Tìm tất cả các Task có độ ưu tiên 'CAO' và chưa hoàn thành
        MATCH (t:Task)
        WHERE t.priority = 'CAO' AND t.status <> 'COMPLETED'
        RETURN t.name, t.dueDate, t.priority;

        // Tìm các Project được tạo sau một ngày cụ thể và có tag 'AI'
        MATCH (p:Project)
        WHERE p.creationDate > date($dateParam) AND 'AI' IN p.tags
        RETURN p.name, p.creationDate, p.tags;
        ```yaml

    *   **Truy vấn dựa trên Thời gian (Time-based Queries):**
        ```yamlcypher
        // Tìm tất cả Event xảy ra trong một khoảng thời gian cụ thể
        MATCH (e:Event)
        WHERE e.timestamp >= datetime($startTimeParam) AND e.timestamp <= datetime($endTimeParam)
        RETURN e.type, e.description, e.timestamp ORDER BY e.timestamp DESC;
        ```yaml

    *   **Sử dụng APOC Procedures (nếu có và cần thiết):**
        ```yamlcypher
        // Lưu ý: Cần cài đặt thư viện APOC trong Neo4j
        // Ví dụ: Sử dụng APOC để tạo UUID tự động cho node mới
        // CREATE (newNode:Concept)
        // SET newNode.uuid = apoc.create.uuid()
        // RETURN newNode;

        // Ví dụ: Sử dụng APOC để load dữ liệu JSON (nếu agent nhận dữ liệu từ nguồn ngoài)
        // CALL apoc.load.json("file:///path/to/data.json") YIELD value AS data
        // MERGE (item:DataItem {id: data.id})
        // SET item += data.properties
        // RETURN count(item);
        ```yaml
    **13.2. Tạo và Cập nhật Dữ liệu trong Ontology (Data Creation & Modification)**

    Các AI Agent không chỉ truy vấn mà còn chủ động tạo mới, cập nhật và xóa dữ liệu trong ontology. Đây là hoạt động cốt lõi của các agent như `KnowledgeExtractionAgent`, `ProjectManagementAgent`, `WinRecognitionAgent`, và AGE khi điều phối hoạt động. Các hoạt động này phải đảm bảo tính nhất quán và toàn vẹn của dữ liệu.

    *   **Tạo Node mới (CREATE):**
        ```yamlcypher
        // Tạo một Project mới với các thuộc tính cơ bản
        CREATE (p:Project {
          projectId: apoc.create.uuid(), // Sử dụng APOC để tạo UUID
          name: $projectNameParam,
          description: $projectDescParam,
          status: 'Planning',
          startDate: date(), // Ngày hiện tại
          tags: ['new', 'strategic']
        })
        RETURN p;

        // Tạo một KnowledgeSnippet mới
        CREATE (ks:KnowledgeSnippet {
          snippetId: $snippetIdParam,
          content: $contentParam,
          source: $sourceParam,
          embeddingVector: $embeddingVectorParam, // Nếu lưu vector trực tiếp
          createdTimestamp: datetime()
        })
        RETURN ks.snippetId;
        ```yaml

    *   **Tạo Relationship mới (CREATE):**
        Thường đi kèm với `MATCH` hoặc `MERGE` để tìm các node hiện có trước khi tạo mối quan hệ.
        ```yamlcypher
        // Gán một Agent hiện có cho một Task hiện có
        MATCH (a:Agent {agentId: $agentIdParam})
        MATCH (t:Task {taskId: $taskIdParam})
        CREATE (a)-[r:ASSIGNED_TO {assignedDate: date(), role: 'Developer'}]->(t)
        RETURN type(r) AS relationshipType, r.assignedDate;
        ```yaml

    *   **Sử dụng MERGE để Tạo hoặc Cập nhật Node/Relationship (Upsert):**
        `MERGE` đảm bảo rằng một pattern (node hoặc relationship) chỉ được tạo nếu nó chưa tồn tại. Kết hợp với `ON CREATE SET` và `ON MATCH SET` để xử lý các thuộc tính.
        ```yamlcypher
        // Tạo hoặc tìm một User, sau đó cập nhật lastLogin
        MERGE (u:User {email: $emailParam})
        ON CREATE SET
          u.userId = apoc.create.uuid(),
          u.creationDate = datetime(),
          u.lastLogin = datetime(),
          u.isActive = true
        ON MATCH SET
          u.lastLogin = datetime()
        RETURN u.userId, u.lastLogin;

        // Tạo một relationship :HAS_SKILL nếu chưa có, và cập nhật mức độ thành thạo
        MATCH (p:Person {personId: $personIdParam})
        MATCH (s:Skill {name: $skillNameParam})
        MERGE (p)-[r:HAS_SKILL]->(s)
        ON CREATE SET r.proficiency = $proficiencyParam, r.acquiredDate = date()
        ON MATCH SET r.proficiency = $proficiencyParam
        RETURN p.name, type(r), s.name, r.proficiency;
        ```yaml

    *   **Cập nhật Thuộc tính của Node/Relationship (SET):**
        ```yamlcypher
        // Cập nhật trạng thái và ngày hoàn thành của một Task
        MATCH (t:Task {taskId: $taskIdParam})
        SET t.status = 'Completed',
            t.completedDate = date(),
            t.actualEffortHours = $effortParam
        RETURN t.name, t.status, t.completedDate;

        // Thêm một tag mới vào danh sách tags của Project (nếu tags là một list)
        MATCH (p:Project {projectId: $projectIdParam})
        SET p.tags = coalesce(p.tags, []) + $newTagParam // coalesce đảm bảo p.tags không null
        RETURN p.tags;
        ```yaml

    *   **Xóa Node và Relationship (DELETE, DETACH DELETE):**
        Cần cẩn trọng khi xóa để không phá vỡ tính toàn vẹn dữ liệu.
        ```yamlcypher
        // Xóa một relationship cụ thể giữa hai node
        MATCH (u:User {userId: $userIdParam})-[r:FOLLOWS]->(c:Community {communityId: $communityIdParam})
        DELETE r;

        // Xóa một node và tất cả các relationship liên quan đến nó
        MATCH (obs:ObsoleteData {dataId: $obsoleteIdParam})
        DETACH DELETE obs;
        ```yaml

    *   **Lưu ý về Giao tác (Transactions):**
        Đối với các hoạt động ghi phức tạp bao gồm nhiều bước, các agent nên thực hiện chúng trong một giao tác (transaction) duy nhất để đảm bảo tính nguyên tử (atomicity). Nếu một phần của giao tác thất bại, toàn bộ giao tác sẽ được rollback.
        Ví dụ (logic giả định, cách triển khai cụ thể phụ thuộc vào driver Neo4j):
        ```yamlpython
        # conceptual example in Python using a hypothetical driver
        # with driver.session() as session:
        #     with session.begin_transaction() as tx:
        #         tx.run("MATCH (a:Account {id: $fromAccId}) SET a.balance = a.balance - $amount", fromAccId=acc1, amount=100)
        #         tx.run("MATCH (b:Account {id: $toAccId}) SET b.balance = b.balance + $amount", toAccId=acc2, amount=100)
        #         tx.commit()
        ```yaml

    **13.3. Đăng ký và Xử lý Sự kiện Ontology (Ontology Event Handling)**

    Các AI Agent cần có khả năng phản ứng với những thay đổi và sự kiện quan trọng xảy ra trong ontology theo thời gian thực hoặc gần thời gian thực. Điều này cho phép hệ thống hoạt động một cách chủ động và linh hoạt, thay vì chỉ dựa vào việc truy vấn định kỳ. Khái niệm "Ontology-Driven Events" là trung tâm của cơ chế này.

    *   **Khái niệm Ontology-Driven Events:**
        Là các sự kiện được kích hoạt bởi sự thay đổi trạng thái, tạo mới, hoặc xóa các node/relationship cụ thể trong ontology, hoặc khi một pattern dữ liệu cụ thể xuất hiện. Ví dụ:
        *   Một `Tension` mới được tạo với mức độ ưu tiên `CAO`.
        *   Trạng thái của một `Project` chuyển thành `Blocked` hoặc `Completed`.
        *   Một `WIN` được `WinRecognitionAgent` chính thức ghi nhận.
        *   Một `Resource` (ví dụ: chuyên gia) thay đổi trạng thái từ `Busy` thành `Available`.
        *   Một `Goal` quan trọng có tiến độ (`progress`) đạt dưới một ngưỡng nhất định.

    *   **Cơ chế Đăng ký và Thông báo Sự kiện:**
        Có nhiều cách tiếp cận để các agent đăng ký và nhận thông báo về sự kiện:

        1.  **AGE làm Trung tâm Điều phối Sự kiện (AGE as Event Dispatcher):**
            *   Các agent chuyên biệt đăng ký "mối quan tâm" (interests) về các loại node, relationship, hoặc pattern cụ thể với `AGE`. Ví dụ, `ResourceAllocationAgent` có thể quan tâm đến `Event` loại `RESOURCE_AVAILABLE` hoặc `TASK_NEEDS_RESOURCE`.
            * ` AGE`, với vai trò giám sát toàn cục, theo dõi các thay đổi trong ontology (thông qua các truy vấn định kỳ hiệu suất cao, hoặc nhận thông báo từ các agent tạo ra thay đổi).
            *   Khi một thay đổi khớp với "mối quan tâm" đã đăng ký, `AGE` sẽ gửi thông báo (event payload) đến agent tương ứng.
            * **Ưu điểm:** Tập trung logic điều phối, giảm tải cho các agent chuyên biệt.
            * **Nhược điểm:** `AGE` có thể trở thành điểm nghẽn nếu lượng sự kiện lớn; độ trễ phụ thuộc vào tần suất giám sát của `AGE`.

        2.  **Sử dụng Message Queue / Event Bus (ví dụ: Kafka, RabbitMQ, Redis Streams):**
            *   Khi một agent (ví dụ: `KnowledgeExtractionAgent` hoặc `AGE`) thực hiện một thay đổi quan trọng trong ontology, nó đồng thời xuất bản một message/event lên một topic/channel cụ thể trên message queue.
            *   Các agent khác quan tâm đến loại sự kiện đó sẽ đăng ký (subscribe) vào topic/channel tương ứng.
            * **Ưu điểm:** Khả năng mở rộng cao, découpage mạnh mẽ, xử lý bất đồng bộ, độ tin cậy cao.
            * **Nhược điểm:** Tăng thêm thành phần hạ tầng cần quản lý.

        3.  **Neo4j Triggers và APOC (Nâng cao):**
            *   Neo4j Enterprise Edition cung cấp cơ chế trigger cho phép thực thi Cypher hoặc Java code khi có thay đổi dữ liệu.
            *   Thư viện APOC cũng cung cấp các procedure (ví dụ: `apoc.trigger.add`) có thể được sử dụng để kích hoạt hành động khi dữ liệu thay đổi. Hành động này có thể là ghi vào một log, gọi một API, hoặc đẩy message vào một queue.
            * **Ưu điểm:** Phản ứng nhanh chóng ngay tại tầng database.
            * **Nhược điểm:** Logic xử lý sự kiện có thể bị ràng buộc vào database, có thể phức tạp trong việc quản lý và debug; không phải tất cả các phiên bản Neo4j đều hỗ trợ đầy đủ.

        4.  **Polling (Ít được ưu tiên cho các hệ thống cần phản ứng nhanh):**
            *   Các agent định kỳ truy vấn ontology để kiểm tra các thay đổi hoặc điều kiện cụ thể.
            * **Ưu điểm:** Đơn giản để triển khai ban đầu.
            * **Nhược điểm:** Độ trễ cao, tốn tài nguyên nếu polling thường xuyên, khó mở rộng.

    *   **Nội dung Event Payload:**
        Một event được thông báo nên chứa đủ thông tin để agent nhận có thể hành động:
        * ` eventType`: Loại sự kiện (ví dụ: `NEW_TENSION_CREATED`, `PROJECT_STATUS_CHANGED`).
        * ` timestamp`: Thời điểm sự kiện xảy ra.
        * ` sourceAgentId` (tùy chọn): Agent gây ra sự kiện.
        * ` eventData`: Đối tượng chứa các thông tin chi tiết liên quan đến sự kiện. Ví dụ, đối với `PROJECT_STATUS_CHANGED`:
            ```yamljson
            {
              "projectId": "proj_abc",
              "oldStatus": "Active",
              "newStatus": "Blocked",
              "reason": "Resource unavailable" // (tùy chọn)
            }
            ```yaml

    *   **13.3.1. Ví dụ Chi tiết về Event Schemas (Detailed Event Schema Examples)**

        Để đảm bảo tính nhất quán và rõ ràng, dưới đây là một số ví dụ về cấu trúc `eventData` chi tiết cho các loại sự kiện quan trọng:

        * **`TENSION_CREATED`**
            ```yamljson
            {
              "tensionId": "TNS-001",
              "title": "Mâu thuẫn về ưu tiên nguồn lực giữa Project A và Project B",
              "description": "Cả hai dự án đều yêu cầu chuyên gia AI X vào cùng một thời điểm.",
              "priority": "High", // "High", "Medium", "Low"
              "status": "New", // "New", "UnderInvestigation", "ResolutionProposed", "Resolved", "Closed"
              "createdBy": "AgentID_or_UserID",
              "createdAt": "YYYY-MM-DDTHH:mm:ssZ",
              "relatedEntities": [
                {"entityId": "PROJ-A", "entityType": "Project"},
                {"entityId": "PROJ-B", "entityType": "Project"},
                {"entityId": "RES-AI-X", "entityType": "Resource"}
              ]
            }
            ```yaml

        * **`PROJECT_STATUS_CHANGED`**
            ```yamljson
            {
              "projectId": "PROJ-XYZ",
              "oldStatus": "Active",
              "newStatus": "Blocked",
              "reason": "Thiếu hụt nguồn lực tài chính tạm thời.",
              "changedBy": "ResourceManagementAgent_ID", // Hoặc User ID nếu thay đổi thủ công
              "changedAt": "YYYY-MM-DDTHH:mm:ssZ",
              "detailsLink": "/trm-os/projects/PROJ-XYZ/status_log/entry_123" // (Tùy chọn) Link đến log chi tiết
            }
            ```yaml

        * **`KNOWLEDGE_SNIPPET_EMBEDDED`**
            ```yamljson
            {
              "snippetId": "KS-007",
              "sourceNodeIdNeo4j": "neo4j_node_id_abc",
              "embeddingStatus": "Success", // "Success", "Failed"
              "vectorDbId": "supabase_vector_id_123", // ID của bản ghi trong Supabase Vector
              "embeddingModel": "text-embedding-ada-002",
              "embeddedAt": "YYYY-MM-DDTHH:mm:ssZ",
              "failureReason": null // Hoặc mô tả lỗi nếu embeddingStatus là "Failed"
            }
            ```yaml

        * **`RESOURCE_AVAILABILITY_CHANGED`**
            ```yamljson
            {
              "resourceId": "RES-DEV-005",
              "resourceType": "HumanResource", // "HumanResource", "SoftwareLicense", "ComputeInstance"
              "oldAvailability": "Busy", // "Available", "Busy", "PartiallyAvailable", "Unavailable"
              "newAvailability": "Available",
              "availableFrom": "YYYY-MM-DDTHH:mm:ssZ", // (Tùy chọn, nếu có lịch trình cụ thể)
              "availableUntil": "YYYY-MM-DDTHH:mm:ssZ", // (Tùy chọn)
              "reasonForChange": "Hoàn thành Task TSK-123",
              "updatedBy": "ProjectManagementAgent_ID",
              "updatedAt": "YYYY-MM-DDTHH:mm:ssZ"
            }
            ```yaml
        Việc định nghĩa rõ ràng các schema này giúp cho việc phát triển và tích hợp các agent trở nên dễ dàng hơn, đồng thời hỗ trợ việc gỡ lỗi và giám sát hệ thống.

    *   **Xử lý Sự kiện bởi Agent:**
        Khi nhận được một event, agent sẽ:
        1.  Phân tích `eventData`.
        2.  Truy vấn thêm thông tin từ ontology nếu cần.
        3.  Thực hiện logic nghiệp vụ của mình (ví dụ: `TensionResolutionAgent` bắt đầu quy trình giải quyết `Tension`, `GoalAlignmentAgent` đánh giá lại sự phù hợp của `Project` khi có `Goal` thay đổi).
            Có thể tạo ra các node/relationship mới hoặc cập nhật ontology, và có thể kích hoạt các event tiếp theo.

    *   **13.3.2. Đảm bảo Tính tin cậy và Xử lý Lỗi trong Giao tiếp Sự kiện (Ensuring Reliability and Error Handling in Event Communication)**

        Khi sử dụng các hệ thống message queue hoặc event bus, việc đảm bảo tính tin cậy của giao tiếp và xử lý lỗi một cách hiệu quả là rất quan trọng:

        * **Acknowledgement (Xác nhận):**
            * **Publisher Acknowledgements:** Agent xuất bản sự kiện cần nhận được xác nhận từ message broker rằng sự kiện đã được lưu trữ an toàn (ví dụ: ghi vào disk) trước khi coi là đã gửi thành công. Điều này giúp tránh mất mát sự kiện nếu publisher gặp sự cố ngay sau khi gửi.
            * **Subscriber Acknowledgements:** Agent đăng ký nhận sự kiện, sau khi xử lý xong một sự kiện, cần gửi xác nhận lại cho message broker. Broker chỉ xóa (hoặc đánh dấu là đã xử lý) sự kiện khỏi queue sau khi nhận được xác nhận này. Có hai chế độ phổ biến:
                *   *Automatic Acknowledgement:* Broker tự động coi sự kiện là đã xử lý ngay khi gửi cho subscriber. Đơn giản nhưng có thể gây mất sự kiện nếu subscriber gặp lỗi trước khi xử lý xong.
                *   *Manual Acknowledgement:* Subscriber phải chủ động gọi một hàm để xác nhận. An toàn hơn.

        * **Retry Mechanisms (Cơ chế Thử lại):**
            *   Đối với các lỗi tạm thời (ví dụ: mất kết nối mạng tạm thời khi subscriber cố gắng cập nhật Neo4j, dịch vụ bên ngoài không khả dụng), subscriber nên có logic thử lại việc xử lý sự kiện sau một khoảng thời gian chờ tăng dần (exponential backoff).
            *   Cần giới hạn số lần thử lại để tránh vòng lặp vô hạn.

        * **Dead-Letter Queues (DLQ) / Dead-Letter Exchanges (DLX):**
            *   Nếu một sự kiện không thể được xử lý thành công sau nhiều lần thử lại (ví dụ: do dữ liệu không hợp lệ, lỗi logic nghiêm trọng trong subscriber), nó nên được chuyển đến một DLQ riêng.
            *   Việc này giúp các sự kiện lỗi không làm tắc nghẽn queue chính, cho phép các sự kiện khác tiếp tục được xử lý.
            *   Các sự kiện trong DLQ có thể được phân tích thủ công hoặc tự động để tìm ra nguyên nhân lỗi và có biện pháp khắc phục (ví dụ: sửa dữ liệu, cập nhật code của subscriber, hoặc bỏ qua sự kiện nếu không quan trọng).

        * **Idempotency (Tính Lũy đẳng trong Xử lý):**
            *   Trong một số kịch bản (ví dụ: subscriber bị lỗi sau khi xử lý xong nhưng trước khi gửi acknowledgement), một sự kiện có thể được gửi lại và xử lý nhiều lần. Do đó, logic xử lý sự kiện của agent nên được thiết kế để có tính lũy đẳng.
            *   Nghĩa là, việc xử lý cùng một sự kiện nhiều lần phải cho kết quả tương tự như xử lý một lần duy nhất (ví dụ: không tạo ra các bản ghi trùng lặp, không cộng dồn các giá trị một cách sai lệch).
            *   Điều này có thể đạt được bằng cách kiểm tra xem hành động đã được thực hiện trước đó chưa (ví dụ: dựa vào ID của sự kiện hoặc trạng thái của các thực thể liên quan trong Neo4j).

        * **Logging và Monitoring (Ghi Log và Giám sát):**
            *   Toàn bộ quá trình từ khi sự kiện được xuất bản, đưa vào queue, nhận bởi subscriber, xử lý, và acknowledgement cần được ghi log chi tiết.
            *   Thiết lập các công cụ giám sát để theo dõi tình trạng của message queue (số lượng message, tỷ lệ lỗi), hiệu suất của các subscriber, và các sự kiện trong DLQ.

    *   **13.3.3. Gợi ý Quy ước Đặt tên Sự kiện (Suggested Event Naming Conventions)**

        Để duy trì sự rõ ràng và nhất quán khi số lượng loại sự kiện tăng lên, việc áp dụng một quy ước đặt tên cho `eventType` là rất hữu ích. Một số gợi ý:

        * **Cấu trúc:** `SUBJECT_ACTION_STATUS` hoặc `SUBJECT_VERB_OBJECT`.
            *   Ví dụ: `PROJECT_PROPOSAL_SUBMITTED`, `PROJECT_STATUS_UPDATED`, `TENSION_ANALYSIS_COMPLETED`, `USER_LOGIN_FAILED`, `RESOURCE_ALLOCATION_REQUESTED`.
        * **Sử dụng thì quá khứ (Past Tense):** Vì sự kiện thường biểu thị một điều gì đó đã xảy ra.
            *   Ví dụ: `DOCUMENT_UPLOADED`, `PAYMENT_PROCESSED`.
        * **Rõ ràng, Ngắn gọn và Dễ hiểu:** Tên sự kiện nên tự mô tả ý nghĩa của nó.
        * **Thống nhất về viết hoa:** Sử dụng `UPPER_SNAKE_CASE` (như các ví dụ trên) là một lựa chọn phổ biến và dễ đọc.
        * **Tránh viết tắt không cần thiết:** Ưu tiên sự rõ ràng hơn là quá ngắn gọn.

    *   **13.3.4. Khái niệm Danh mục/Sổ đăng ký Sự kiện (Event Catalog/Registry Concept - Future Consideration)**

        Khi hệ thống TRM-OS phát triển và số lượng các loại sự kiện, nhà xuất bản (publishers), và người đăng ký (subscribers) tăng lên, việc duy trì một "Danh mục Sự kiện" hoặc "Sổ đăng ký Sự kiện" (Event Catalog/Registry) tập trung sẽ trở nên cực kỳ quan trọng. Điều này có thể là:

        * **Một tài liệu thiết kế riêng biệt:** Liệt kê tất cả các `eventType` được định nghĩa, schema chi tiết của chúng (tham chiếu đến JSON Schemas), mô tả mục đích, các agent thường xuất bản và các agent thường đăng ký nhận sự kiện này.
        * **Được quản lý trong chính Ontology:** Trong tương lai, các `EventType` có thể được mô hình hóa như các node trong Neo4j, với các thuộc tính mô tả schema, mục đích, và các mối quan hệ `PUBLISHED_BY` và `SUBSCRIBED_BY` đến các `Agent`.

        Lợi ích của Event Catalog/Registry:
        * **Khám phá (Discoverability):** Giúp các nhà phát triển dễ dàng tìm hiểu về các sự kiện hiện có và cách sử dụng chúng.
        * **Quản trị (Governance):** Hỗ trợ việc quản lý vòng đời của các sự kiện, tránh trùng lặp và đảm bảo tính nhất quán.
        * **Phân tích Tác động (Impact Analysis):** Khi cần thay đổi một schema sự kiện, catalog giúp xác định các agent bị ảnh hưởng.
        * **Tài liệu hóa (Documentation):** Là nguồn tài liệu trung tâm cho kiến trúc hướng sự kiện của hệ thống.

    Việc lựa chọn cơ chế xử lý sự kiện phụ thuộc vào yêu cầu về độ trễ, khối lượng sự kiện, độ phức tạp và nguồn lực phát triển. Trong TRM-OS, sự kết hợp giữa **AGE làm điều phối viên chính** và tiềm năng tích hợp **Message Queue** cho các luồng sự kiện quan trọng có thể là một hướng đi cân bằng, với các cơ chế đảm bảo độ tin cậy như trên được cân nhắc kỹ lưỡng.


    **13.4. Tương tác với Supabase Vector (Semantic Search)**

    AI Agents sử dụng Supabase Vector (thông qua `pgvector`) để lưu trữ và tìm kiếm các embeddings văn bản, cho phép thực hiện các truy vấn dựa trên sự tương đồng về ngữ nghĩa. Điều này rất quan trọng cho các tác vụ như tìm kiếm tài liệu liên quan, gợi ý, và hỗ trợ RAG (Retrieval Augmented Generation).

    *   **1. Chi tiết hóa Schema Bảng Vector**

        Một bảng chính trong Supabase (ví dụ: `semantic_embeddings`) có thể được thiết kế với các trường sau để lưu trữ embeddings và metadata liên quan:

        * ` id` (UUID, Primary Key): Khóa chính của bản ghi embedding trong Supabase.
        * ` id_neo4j` (TEXT, Indexed): ID của node gốc trong Neo4j mà embedding này đại diện cho (ví dụ: ID của `KnowledgeSnippet`, `Project`, `Tension`). Giúp liên kết trở lại ontology.
        * ` source_node_label` (TEXT, Indexed): Label của node gốc trong Neo4j (ví dụ: "KnowledgeSnippet", "Project", "Tension"). Hỗ trợ việc lọc theo loại thực thể.
        * ` text_content_raw` (TEXT): Nội dung văn bản gốc đã được sử dụng để tạo embedding. Có thể hữu ích cho việc debug hoặc hiển thị snippet.
        * ` embedding_vector` (VECTOR(N)): Vector embedding được tạo ra từ `text_content_raw`. `N` là số chiều của vector, phụ thuộc vào model embedding được sử dụng (ví dụ: 1536 cho `text-embedding-ada-002` của OpenAI).
        * ` embedding_model_version` (TEXT): Phiên bản của model embedding được sử dụng, để quản lý khi có cập nhật model.
        * ` metadata_custom` (JSONB, Optional): Lưu trữ các metadata bổ sung tùy chỉnh, ví dụ: `{"project_id": "prj-001", "tags": ["AI", "ethics"]}`.
        * ` created_at` (TIMESTAMP WITH TIME ZONE, Default: `now()`): Thời điểm bản ghi embedding được tạo.
        * ` updated_at` (TIMESTAMP WITH TIME ZONE, Default: `now()`): Thời điểm bản ghi embedding được cập nhật lần cuối.

        **Ví dụ câu lệnh tạo bảng (SQL cho Supabase/PostgreSQL):**
        ```yamlsql
        CREATE EXTENSION IF NOT EXISTS vector; -- Đảm bảo extension pgvector được cài đặt

        CREATE TABLE semantic_embeddings (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            id_neo4j TEXT NOT NULL,
            source_node_label TEXT NOT NULL,
            text_content_raw TEXT,
            embedding_vector VECTOR(1536), -- Thay 1536 bằng số chiều của model bạn dùng
            embedding_model_version TEXT,
            metadata_custom JSONB,
            created_at TIMESTAMPTZ DEFAULT now(),
            updated_at TIMESTAMPTZ DEFAULT now()
        );

        -- Tạo index để tăng tốc độ tìm kiếm
        CREATE INDEX ON semantic_embeddings USING ivfflat (embedding_vector vector_l2_ops) WITH (lists = 100);
        -- Hoặc HNSW (thường cho kết quả tốt hơn cho nhiều trường hợp):
        -- CREATE INDEX ON semantic_embeddings USING hnsw (embedding_vector vector_l2_ops);

        CREATE INDEX idx_id_neo4j ON semantic_embeddings (id_neo4j);
        CREATE INDEX idx_source_node_label ON semantic_embeddings (source_node_label);
        ```yaml

    *   **2. Quy trình Embedding Chi tiết**

        * **Agent chịu trách nhiệm:**
            Một agent chuyên biệt, ví dụ `KnowledgeEmbeddingAgent`, sẽ chịu trách nhiệm chính cho việc tạo, cập nhật và quản lý các embeddings. Agent này có thể:
            *   Sử dụng các model embedding tiên tiến (ví dụ: OpenAI, Sentence Transformers).
            *   Xử lý tiền xử lý văn bản (làm sạch, chunking nếu cần) trước khi tạo embedding.
            *   Tương tác với cả Neo4j (để lấy nội dung) và Supabase (để lưu trữ/cập nhật embeddings).

        * **Khi nào embeddings được tạo/cập nhật:**
            Embeddings nên được tạo hoặc cập nhật trong các trường hợp sau:
            1.  **Tạo mới:** Khi một node có nội dung văn bản cần tìm kiếm ngữ nghĩa được tạo trong Neo4j (ví dụ: `KnowledgeSnippet` mới, `LearningResource` mới).
            2.  **Cập nhật:** Khi nội dung văn bản của một node hiện có thay đổi đáng kể (ví dụ: `Project.description` được cập nhật, `Tension.details` được bổ sung).
            3.  **Xóa (Logical/Physical):** Khi node gốc trong Neo4j bị xóa, embedding tương ứng trong Supabase cũng nên được xử lý (xóa hoặc đánh dấu là "stale").
            4.  **Theo lịch trình (Batch Processing):** Có thể có một quy trình chạy định kỳ để rà soát và đảm bảo tất cả các nội dung cần thiết đã được embed và các embedding là mới nhất, đặc biệt hữu ích khi mới triển khai hoặc sau khi thay đổi model embedding.

        * **Loại nội dung nào sẽ được embed:**
            Các thuộc tính văn bản từ nhiều loại node khác nhau có thể được embed để phục vụ các mục đích tìm kiếm khác nhau:
            * ` KnowledgeSnippet.content`: Nội dung chi tiết của snippet tri thức.
            * ` LearningResource.title`, `LearningResource.description`, `LearningResource.content_summary`: Thông tin về tài liệu học tập.
            * ` Tension.title`, `Tension.description`, `Tension.resolution_summary`: Mô tả về các căng thẳng và giải pháp.
            * ` Project.name`, `Project.description`, `Project.goal_summary`: Thông tin tổng quan về dự án.
            * ` Goal.name`, `Goal.description`: Mô tả mục tiêu.
            * ` UserStory.description`, `UserStory.acceptance_criteria`: Chi tiết yêu cầu người dùng.
            * ` FAQ.question`, `FAQ.answer`: Các câu hỏi thường gặp.
            * ` MeetingNote.summary`, `MeetingNote.action_items_text`: Tóm tắt và các mục hành động từ ghi chú cuộc họp.
            *   Nội dung từ các `Document` được tải lên hệ thống.

            **Lưu ý về Chunking:** Đối với các văn bản dài (ví dụ: nội dung đầy đủ của `LearningResource`), việc chia văn bản thành các đoạn (chunks) nhỏ hơn trước khi tạo embedding cho mỗi chunk có thể cải thiện chất lượng tìm kiếm. Mỗi chunk sẽ có `id_neo4j` trỏ về node gốc và có thể thêm metadata về vị trí chunk.

    *   **3. RPC Functions trong Supabase**

        Để thực hiện tìm kiếm vector hiệu quả và đóng gói logic, các hàm Remote Procedure Call (RPC) trong Supabase (PostgreSQL functions) là rất cần thiết.

        * **`match_documents_by_embedding(query_embedding VECTOR, match_threshold FLOAT, match_count INT, filter_label TEXT DEFAULT NULL, filter_metadata JSONB DEFAULT NULL)`:**
            * **Mục đích:** Tìm kiếm các bản ghi trong `semantic_embeddings` có `embedding_vector` gần nhất với `query_embedding` được cung cấp.
            * **Tham số:**
                * ` query_embedding VECTOR`: Vector embedding của truy vấn.
                * ` match_threshold FLOAT`: Ngưỡng tương đồng (ví dụ: cosine similarity). Chỉ trả về các kết quả có độ tương đồng lớn hơn hoặc bằng ngưỡng này.
                * ` match_count INT`: Số lượng kết quả tối đa cần trả về.
                * ` filter_label TEXT` (tùy chọn): Lọc kết quả theo `source_node_label`.
                * ` filter_metadata JSONB` (tùy chọn): Lọc kết quả dựa trên các trường trong `metadata_custom`.
            * **Trả về:** Bảng các bản ghi khớp, bao gồm `id_neo4j`, `source_node_label`, `text_content_raw` (hoặc chỉ ID), và điểm tương đồng.

        **Ví dụ định nghĩa hàm (SQL):**
        ```yamlsql
        CREATE OR REPLACE FUNCTION match_documents_by_embedding(
            query_embedding VECTOR(1536), -- Cùng số chiều với bảng
            match_threshold FLOAT,
            match_count INT,
            filter_label TEXT DEFAULT NULL,
            filter_metadata JSONB DEFAULT NULL
        )
        RETURNS TABLE (
            id_neo4j_match TEXT,
            source_node_label_match TEXT,
            text_content_raw_match TEXT, -- Hoặc chỉ id_neo4j nếu không muốn trả về content
            similarity FLOAT
        )
        LANGUAGE plpgsql
        AS $$
        BEGIN
            RETURN QUERY
            SELECT
                se.id_neo4j,
                se.source_node_label,
                se.text_content_raw,
                1 - (se.embedding_vector <=> query_embedding) AS similarity -- Cosine distance to similarity
            FROM
                semantic_embeddings se
            WHERE
                (1 - (se.embedding_vector <=> query_embedding)) >= match_threshold
                AND (filter_label IS NULL OR se.source_node_label = filter_label)
                AND (filter_metadata IS NULL OR se.metadata_custom @> filter_metadata) -- JSONB containment
            ORDER BY
                se.embedding_vector <=> query_embedding ASC -- ASC for distance (closest first)
            LIMIT match_count;
        END;
        $$;
        ```yaml
        Các agent sẽ gọi hàm RPC này thông qua Supabase client.

    *   **4. Ví dụ Ứng dụng Cụ thể cho các Agent**

        * **`UserQueryAgent`:**
            *   Khi người dùng đặt câu hỏi tự nhiên (ví dụ: "Làm thế nào để giải quyết xung đột tài nguyên trong dự án X?"), `UserQueryAgent` tạo embedding cho câu hỏi.
            *   Gọi RPC `match_documents_by_embedding` để tìm kiếm trong `semantic_embeddings`, lọc theo `source_node_label` là "KnowledgeSnippet", "FAQ", "LearningResource".
            *   Sử dụng các kết quả (ví dụ: `id_neo4j` của các `KnowledgeSnippet` liên quan) để truy vấn Neo4j lấy nội dung đầy đủ.
            *   Tổng hợp thông tin và trả lời người dùng, có thể sử dụng LLM để tạo câu trả lời (RAG).

        * **`TensionResolutionAgent`:**
            *   Khi một `Tension` mới được tạo hoặc cần giải quyết, agent tạo embedding cho `Tension.description`.
            *   Tìm kiếm các `Tension` (đã giải quyết), `LearningEvent` hoặc `KnowledgeSnippet` tương tự trong quá khứ bằng cách gọi RPC, lọc theo các label tương ứng.
            *   Gợi ý các giải pháp hoặc bài học kinh nghiệm đã được áp dụng thành công cho các trường hợp tương tự.

        * **`ProjectPlanningAgent`:**
            *   Khi lập kế hoạch cho một dự án mới, agent có thể tạo embedding cho `Project.description` hoặc `Project.goal_summary` của dự án mới.
            *   Tìm kiếm các `Project` tương tự đã hoàn thành trong quá khứ.
            *   Tham khảo kế hoạch, rủi ro đã gặp, tài nguyên đã sử dụng từ các dự án tương tự để hỗ trợ việc lập kế hoạch hiệu quả hơn.

    *   **5. Cân nhắc về Tần suất Cập nhật và Đồng bộ**

        Đảm bảo tính nhất quán (eventual consistency) giữa dữ liệu trong Neo4j và các embeddings trong Supabase Vector là rất quan trọng.

        * **Event-Driven Updates:**
            *   Sử dụng cơ chế xử lý sự kiện (như đã mô tả ở mục 13.3) để kích hoạt `KnowledgeEmbeddingAgent`.
            *   Ví dụ: Khi một `KnowledgeSnippet` được tạo/cập nhật trong Neo4j, một event được gửi đi. `KnowledgeEmbeddingAgent` nhận event này, lấy dữ liệu từ Neo4j, tạo embedding và upsert vào Supabase.
            *   Tương tự cho việc xóa: khi một node bị xóa, event tương ứng sẽ kích hoạt việc xóa embedding.

        * **Message Queue for Decoupling:**
            Để tăng độ tin cậy và khả năng mở rộng, việc sử dụng một message queue (ví dụ: RabbitMQ, Kafka) giữa Neo4j (hoặc agent thực hiện thay đổi) và `KnowledgeEmbeddingAgent` là một giải pháp tốt.
            *   Agent A thay đổi node X trong Neo4j -> Gửi message {action: "UPSERT", id_neo4j: "X_id", label: "KnowledgeSnippet"} vào queue.
            * ` KnowledgeEmbeddingAgent` tiêu thụ message từ queue, xử lý embedding.

        * **Batch Synchronization:**
            *   Định kỳ (ví dụ: hàng đêm), một quy trình batch có thể chạy để:
                *   Quét các node trong Neo4j chưa có embedding hoặc có `updated_at` mới hơn `updated_at` của embedding tương ứng trong Supabase.
                *   Tạo/cập nhật các embeddings này.
                *   Xóa các embeddings trong Supabase mà không còn node tương ứng trong Neo4j (hoặc node đã bị đánh dấu là không cần embed nữa).
            *   Điều này giúp bắt các trường hợp bị bỏ lỡ do lỗi trong quá trình event-driven.

        * **Quản lý phiên bản Model Embedding:**
            Khi model embedding được cập nhật, tất cả các embeddings hiện có có thể cần được tạo lại để đảm bảo tính nhất quán trong không gian vector. `KnowledgeEmbeddingAgent` cần có khả năng thực hiện việc re-embedding hàng loạt này, và trường `embedding_model_version` trong bảng `semantic_embeddings` sẽ giúp quản lý quá trình này.

    Việc tích hợp Supabase Vector một cách chặt chẽ và có chiến lược sẽ nâng cao đáng kể khả năng tìm kiếm thông minh và hỗ trợ ra quyết định của các AI Agent trong TRM-OS.
**13.5. Ví dụ Luồng Tác vụ Cụ thể do AI Agent Thực hiện**

**13.5.1. Luồng xử lý của TensionResolutionAgent**

1.  **Phát hiện `Tension` và Tạo `Event` (Publication):** Founder nhập một `Tension` mới thông qua giao diện, hoặc `DataSensingAgent` phát hiện từ nguồn khác (email, chat). Một `TensionNode` được tạo trong ontology và một `TensionEvent(type="NewTensionDetected", tension_id={ID})` được "publish" (ghi vào ontology).
2.  **`TensionResolutionAgent` Nhận Thông báo (Subscription & Notification):**
    * ` TensionResolutionAgent` đã "đăng ký" (`INTERESTED_IN` relationship trong ontology) với các `TensionEvent` loại `NewTensionDetected`.
    *   AGE, thông qua cơ chế "Thông báo qua AGE" (AGE-mediated Notification) của Pub/Sub, phát hiện `TensionEvent` mới và gửi một "Thông điệp Trực tiếp" (ví dụ: API call `POST /agent/tension_resolution/notify_new_tension` với payload `{ "event_id": "...", "tension_id": "..." }`) đến `TensionResolutionAgent`.
    *   Hoặc, `TensionResolutionAgent` tự "Theo dõi chủ động" (Agent-initiated Polling) ontology để phát hiện `TensionEvent` mới.
3.  **Phân tích `Tension` và Thu thập Thông tin:**
    * ` TensionResolutionAgent` nhận thông điệp, truy vấn chi tiết `TensionNode` và các `KnowledgeSnippet`, `Skill` liên quan từ ontology.
    *   Nếu cần thêm thông tin chuyên sâu mà một agent khác có thể cung cấp (ví dụ: phân tích kỹ thuật từ một `TechnicalAnalysisAgent` giả định), `TensionResolutionAgent` có thể gửi một "Thông điệp Trực tiếp" (dạng request-response) đến agent đó.
    *   Tương tác với LLM (ví dụ, thông qua một `LLMInterfaceAgent` giả định) để phân tích sâu hơn hoặc gợi ý các hướng giải quyết ban đầu.
4.  **Đề xuất Giải pháp và Tạo `ProjectProposal`:**
    *   Dựa trên phân tích, `TensionResolutionAgent` tạo một `ProjectProposalNode` trong ontology, liên kết nó với `TensionNode` và các `KnowledgeSnippet` liên quan. Một `ProjectProposalEvent(type="NewProposalCreated", proposal_id={ID})` được "publish".
5.  **Duyệt `ProjectProposal` và Khởi tạo `Project`:**
    *   Founder hoặc AGE (dựa trên quy tắc được định sẵn) xem xét `ProjectProposalNode`.
    *   Nếu được duyệt, trạng thái của `ProjectProposalNode` được cập nhật thành "Approved". AGE có thể gửi một "Thông điệp Trực tiếp" đến `ProjectManagementAgent` (ví dụ: `POST /agent/project_management/assign_project` với payload `{ "proposal_id": "...", "project_details": {...} }`) để chính thức giao `Project`.
    * ` ProjectManagementAgent` tạo một `ProjectNode` mới từ `ProjectProposalNode` đã được duyệt và bắt đầu quản lý vòng đời dự án. Một `ProjectEvent(type="ProjectInitiated", project_id={ID})` được "publish".
6.  **Phân bổ Nguồn lực:**
    * ` ResourceAllocationAgent`, đã "đăng ký" với các `ProjectEvent` loại `ProjectInitiated` (hoặc nhận "Thông điệp Trực tiếp" từ `ProjectManagementAgent`), phân tích yêu cầu của `ProjectNode` và hỗ trợ tìm kiếm/đề xuất/phân bổ `ResourceNode` (kỹ năng, con người, công cụ) phù hợp.


**13.5.2. Luồng Tạo và Nhúng KnowledgeSnippet**

Luồng tác vụ này mô tả quy trình end-to-end từ việc thu thập dữ liệu thô, trích xuất thành `KnowledgeSnippet`, và sau đó tạo vector embedding cho snippet đó để phục vụ cho các tác vụ tìm kiếm ngữ nghĩa và phân tích nâng cao trong TRM-OS. Đây là một luồng cốt lõi, đảm bảo tri thức được cập nhật và dễ dàng truy xuất.

*   **Các Agent Tham Gia Chính:**
    * ` DataSensingAgent`: Thu thập dữ liệu từ các nguồn.
    * ` KnowledgeExtractionAgent`: Xử lý dữ liệu thô, tạo/cập nhật `KnowledgeSnippet`.
    * ` KnowledgeEmbeddingAgent`: Tạo và lưu trữ vector embeddings.
*   **Các Hệ Thống Liên Quan:**
    *   Neo4j Aura: Lưu trữ ontology, bao gồm `RawDataPoint` và `KnowledgeSnippet`.
    *   Supabase Vector (pgvector): Lưu trữ vector embeddings.
    *   Message Queue (Tùy chọn, ví dụ: RabbitMQ, Kafka): Để tăng độ tin cậy và khả năng mở rộng cho việc giao tiếp sự kiện.

*   **Các Bước Thực Hiện:**

    1.  **Thu Thập Dữ Liệu Thô (`DataSensingAgent`):**
        * ` DataSensingAgent` theo dõi các nguồn dữ liệu được cấu hình (API, email, web, etc.) để phát hiện thông tin mới.
        *   Khi có dữ liệu mới và được đánh giá là có liên quan, Agent tạo một node `RawDataPoint` trong Neo4j, chứa nội dung gốc, nguồn, và các metadata khác. (Chi tiết xem tại mục 13.5.3, Phần 1).
        *   Agent phát ra sự kiện `NEW_RAW_DATA_POINT_CREATED` để thông báo cho các agent khác.

    2.  **Trích Xuất Tri Thức và Tạo `KnowledgeSnippet` (`KnowledgeExtractionAgent`):**
        * ` KnowledgeExtractionAgent` lắng nghe sự kiện `NEW_RAW_DATA_POINT_CREATED` hoặc định kỳ quét các `RawDataPoint` mới.
        *   Agent truy vấn `RawDataPoint`, sử dụng LLM để trích xuất thông tin quan trọng, tóm tắt, xác định thực thể, và phân loại.
        *   Dựa trên kết quả, Agent tạo một node `KnowledgeSnippet` mới trong Neo4j hoặc cập nhật một `KnowledgeSnippet` hiện có. Node này chứa nội dung đã xử lý, tiêu đề, từ khóa, nguồn, và liên kết `EXTRACTED_FROM` tới `RawDataPoint` gốc. Trạng thái của `RawDataPoint` được cập nhật thành `Processed`. (Chi tiết xem tại mục 13.5.3, Phần 2, bước 1-4).

    3.  **Phát Hành Sự Kiện Kích Hoạt Embedding (`KnowledgeExtractionAgent`):**
        *   Sau khi tạo mới hoặc cập nhật thành công `KnowledgeSnippet` (và nội dung của nó có sự thay đổi đáng kể nếu là cập nhật), `KnowledgeExtractionAgent` phát hành một sự kiện, ví dụ: `KNOWLEDGE_SNIPPET_UPSERTED`.
        *   Payload của sự kiện này bao gồm `snippetId` của `KnowledgeSnippet` vừa được xử lý và có thể một cờ `content_updated_flag` để chỉ ra rằng nội dung đã thay đổi và cần re-embedding. (Tham khảo mục 13.3 về Xử lý Sự kiện và mục 13.5.3, Phần 2, bước 4).

    4.  **Tạo và Lưu Trữ Vector Embedding (`KnowledgeEmbeddingAgent`):**
        * ` KnowledgeEmbeddingAgent` đăng ký lắng nghe sự kiện `KNOWLEDGE_SNIPPET_UPSERTED` (thông qua Message Queue hoặc cơ chế Pub/Sub của AGE).
        *   Khi nhận được sự kiện:
            *   Agent truy vấn Neo4j để lấy nội dung đầy đủ của `KnowledgeSnippet` dựa trên `snippetId`.
            *   Agent sử dụng một model embedding (ví dụ: Sentence Transformers, OpenAI Ada) để chuyển đổi nội dung text của `KnowledgeSnippet` thành một vector embedding.
            *   Agent thực hiện thao tác "upsert" vector embedding này vào bảng `semantic_embeddings` trong Supabase Vector, cùng với `snippetId` (làm khóa ngoại), `embedding_model_version`, và `updated_at`. (Chi tiết về cấu trúc bảng và tương tác xem tại mục 13.4).
        *   Quá trình này đảm bảo rằng mọi `KnowledgeSnippet` quan trọng đều có một vector embedding tương ứng, sẵn sàng cho việc tìm kiếm ngữ nghĩa và các ứng dụng AI khác.

    5.  **Liên Kết Ngữ Cảnh và Thông Báo (Tùy chọn, `KnowledgeExtractionAgent` / `KnowledgeEmbeddingAgent`):**
        *   Sau khi `KnowledgeSnippet` được tạo và/hoặc nhúng, các liên kết ngữ cảnh (`RELATED_TO`, `PROVIDES_EVIDENCE_FOR`, etc.) có thể được tạo ra dựa trên tìm kiếm vector hoặc các quy tắc khác. (Chi tiết xem tại mục 13.5.3, Phần 2, bước 5).
        *   Thông báo có thể được gửi đi nếu `KnowledgeSnippet` có độ quan trọng cao.

*   **Sơ đồ Luồng Tác Vụ (Sequence Diagram):**

    ```yamlplantuml
    @startuml
    actor "User/DataSource" as DataSource
    participant "DataSensingAgent" as DSA
    database "Neo4j" as Neo4jDB
    participant "KnowledgeExtractionAgent" as KEA
    participant "MessageQueue" as MQ
    participant "KnowledgeEmbeddingAgent" as KEmbA
    database "SupabaseVector" as SupabaseDB

    DataSource -> DSA: Cung cấp dữ liệu mới
    activate DSA
    DSA -> Neo4jDB: Tạo RawDataPoint
    DSA -> MQ: Phát hành sự kiện\nNEW_RAW_DATA_POINT_CREATED
    deactivate DSA

    MQ -> KEA: Nhận sự kiện\nNEW_RAW_DATA_POINT_CREATED
    activate KEA
    KEA -> Neo4jDB: Truy vấn RawDataPoint
    KEA -> Neo4jDB: Tạo/Cập nhật KnowledgeSnippet\n(Liên kết với RawDataPoint, cập nhật trạng thái RawDataPoint)
    KEA -> MQ: Phát hành sự kiện\nKNOWLEDGE_SNIPPET_UPSERTED\n(payload: snippetId, content_updated_flag)
    deactivate KEA

    MQ -> KEmbA: Nhận sự kiện\nKNOWLEDGE_SNIPPET_UPSERTED
    activate KEmbA
    KEmbA -> Neo4jDB: Truy vấn nội dung KnowledgeSnippet\n(dựa trên snippetId)
    KEmbA -> KEmbA: Tạo vector embedding
    KEmbA -> SupabaseDB: Upsert vector embedding\n(cùng snippetId, model_version, updated_at)
    deactivate KEmbA

    @enduml
    ```yaml

Luồng tác vụ này là nền tảng cho việc xây dựng một cơ sở tri thức động và thông minh trong TRM-OS, cho phép hệ thống học hỏi và cung cấp insights giá trị từ dữ liệu liên tục được cập nhật.


**13.5.3. Luồng xử lý của DataSensingAgent và KnowledgeExtractionAgent**

***Phần 1: DataSensingAgent - Thu thập và Đưa Dữ liệu Thô vào Ontology***

Luồng tác vụ này mô tả cách `DataSensingAgent` chủ động theo dõi các nguồn dữ liệu bên ngoài và bên trong, phát hiện thông tin liên quan và đưa chúng vào TRM-OS dưới dạng các `RawDataPoint` để các agent khác có thể phân tích sâu hơn.

1.  **Cấu hình và Theo dõi (Configuration & Monitoring):**
    *   Agent được cấu hình để theo dõi một danh sách các nguồn dữ liệu, ví dụ:
        * **API:** Dữ liệu thị trường, tin tức ngành, feed từ các công cụ khác.
        * **Email:** Hòm thư chung cho các yêu cầu hợp tác, hỗ trợ.
        * **Cloud Storage (Google Drive, etc.):** Các thư mục chứa tài liệu nghiên cứu, báo cáo phân tích mới.
        * **Web:** Các trang web của đối thủ, trang tin công nghệ (thông qua cơ chế scraping có kiểm soát).
    *   Agent hoạt động theo lịch trình (ví dụ: 15 phút/lần) hoặc được kích hoạt bởi webhook.

2.  **Thu thập và Tiền xử lý Dữ liệu (Fetching & Pre-processing):**
    *   Agent kết nối tới nguồn và lấy dữ liệu mới kể từ lần kiểm tra cuối cùng.
    *   Thực hiện các bước tiền xử lý cơ bản: trích xuất văn bản từ file PDF/DOCX, phân tích cú pháp JSON/XML, làm sạch HTML.

3.  **Lọc Mức độ Liên quan (Relevance Filtering):**
    *   Dữ liệu thô sau khi xử lý được đưa vào một mô hình ngôn ngữ lớn (LLM).
    *   LLM được yêu cầu đánh giá nhanh xem dữ liệu có liên quan đến các mối quan tâm chiến lược, dự án đang chạy, hay các `Tension` đã biết của TRM hay không.
    *   Nếu không liên quan, dữ liệu sẽ được ghi log và bỏ qua.

4.  **Tạo Node `RawDataPoint`:**
    *   Nếu dữ liệu được xác định là có liên quan, agent sẽ tạo một node `RawDataPoint` trong Neo4j.
    *   Node này chứa nội dung gốc, nguồn, URI, tóm tắt ngắn do LLM tạo ra, và có trạng thái là `New`.
    *   **Cypher Query:**
        ```yamlcypher
        CREATE (rdp:RawDataPoint {
            dataPointId: apoc.create.uuid(),
            source: $source, // e.g., "Web:techcrunch.com"
            sourceUri: $sourceUri,
            content: $content,
            summary: $summaryFromLLM,
            status: 'New',
            detectedAt: datetime()
        })
        RETURN rdp;
        ```yaml

5.  **Phân loại và Gợi ý Liên kết Ban đầu (Initial Classification & Linking):**
    *   Agent sử dụng tóm tắt và nội dung của `RawDataPoint` để thực hiện tìm kiếm vector (Supabase) nhằm tìm các node có ý nghĩa tương đồng trong hệ thống (`Project`, `Goal`, `Tension`, `KnowledgeSnippet`).
    *   Dựa trên các kết quả tương đồng nhất, agent có thể tự động tạo một mối quan hệ `POTENTIALLY_RELATED_TO` đến các node đó. Đây là một liên kết "yếu" để các agent khác hoặc Founder có thể xác thực sau.

6.  **Kích hoạt "Ontology-Driven Event":**
    *   Sau khi tạo node thành công, agent phát ra một sự kiện `NEW_RAW_DATA_POINT_CREATED`.
    *   Sự kiện này thông báo cho `AGE` và các agent chuyên biệt khác (như `TensionResolutionAgent`) rằng có thông tin mới cần được xem xét, phân tích và có thể "nâng cấp" thành các thực thể tri thức quan trọng hơn (`Tension`, `Opportunity`, `Evidence`...).


***Phần 2: KnowledgeExtractionAgent - Trích xuất Tri thức từ Dữ liệu Thô***

Luồng tác vụ này mô tả cách `KnowledgeExtractionAgent` xử lý các `RawDataPoint` do `DataSensingAgent` thu thập, trích xuất thông tin giá trị và chuyển hóa chúng thành các `KnowledgeSnippet` hoặc các thực thể tri thức khác trong TRM-OS.

1.  **Sự kiện Kích hoạt (Triggering Event):**
    * ` KnowledgeExtractionAgent` "đăng ký" (`INTERESTED_IN`) với các sự kiện `NEW_RAW_DATA_POINT_CREATED`.
    *   Hoặc, Agent có thể định kỳ quét (poll) các `RawDataPoint` có trạng thái là `New`.

2.  **Thu thập và Tiền xử lý `RawDataPoint` (Information Gathering & Pre-processing):**
    *   Khi nhận được thông báo hoặc phát hiện `RawDataPoint` mới, Agent truy vấn chi tiết nội dung, nguồn, và tóm tắt của `RawDataPoint` đó.
    *   Có thể thực hiện thêm các bước làm sạch hoặc chuẩn hóa dữ liệu nếu cần thiết cho việc phân tích sâu hơn.

3.  **Trích xuất Tri thức Chuyên sâu (In-depth Knowledge Extraction):**
    *   Agent gửi nội dung của `RawDataPoint` (và có thể cả tóm tắt) cho một mô hình ngôn ngữ lớn (LLM) với các prompt được thiết kế để:
        *   Xác định các thực thể chính (ví dụ: tên công ty, sản phẩm, công nghệ, người).
        *   Trích xuất các thông tin quan trọng, sự kiện, tuyên bố, hoặc các con số cụ thể.
        *   Phân tích tình cảm (sentiment analysis) nếu có liên quan.
        *   Tóm tắt các điểm cốt lõi dưới dạng các "insights" ngắn gọn.
        *   Gợi ý loại tri thức (ví dụ: "Phân tích đối thủ", "Xu hướng công nghệ", "Rủi ro tiềm ẩn", "Cơ hội thị trường").

4.  **Tạo hoặc Cập nhật `KnowledgeSnippet`:**
    *   Dựa trên kết quả từ LLM, Agent quyết định:
        * **Tạo `KnowledgeSnippet` mới:** Nếu thông tin là mới và đủ giá trị. Node `KnowledgeSnippet` sẽ chứa:
            * ` snippetId`: ID duy nhất.
            * ` title`: Tiêu đề do LLM gợi ý hoặc Agent tự sinh.
            * ` content`: Nội dung chi tiết được trích xuất hoặc tóm tắt lại.
            * ` sourceDescription`: Mô tả nguồn (ví dụ: "Bài báo trên TechCrunch ngày YYYY-MM-DD").
            * ` sourceUri`: Link đến nguồn gốc (nếu có).
            * ` keywords`: Các từ khóa chính.
            * ` extractedAt`: Thời điểm trích xuất.
            * ` extractedBy`: "KnowledgeExtractionAgent".
            *   Liên kết `EXTRACTED_FROM` đến `RawDataPoint` gốc.
        * **Cập nhật `KnowledgeSnippet` hiện có:** Nếu thông tin bổ sung hoặc làm rõ một `KnowledgeSnippet` đã tồn tại (có thể tìm thấy qua vector search hoặc liên kết từ `RawDataPoint`).
        * **Đề xuất hành động khác:** Nếu thông tin không phù hợp để tạo `KnowledgeSnippet` trực tiếp nhưng có thể là một `Tension`, `Opportunity`, hoặc cần sự chú ý của Founder, Agent có thể tạo một `Notification` hoặc một `Task` cho agent/người phù hợp.
    *   **Ví dụ Cypher (Tạo `KnowledgeSnippet` mới):**
        ```yamlcypher
        MATCH (rdp:RawDataPoint {dataPointId: $rdpId})
        CREATE (ks:KnowledgeSnippet {
            snippetId: apoc.create.uuid(),
            title: $titleFromLLM,
            content: $contentFromLLM,
            sourceDescription: rdp.source,
            sourceUri: rdp.sourceUri,
            keywords: $keywordsFromLLM, // list of strings
            extractedAt: datetime(),
            extractedBy: "KnowledgeExtractionAgent",
            status: "New"
        })
        MERGE (ks)-[:EXTRACTED_FROM]->(rdp)
        SET rdp.status = 'Processed' // Cập nhật trạng thái RawDataPoint
        RETURN ks;
        ```yaml

        * **Phát hành Sự kiện để Kích hoạt Embedding:**
            *   Sau khi tạo mới hoặc cập nhật thành công một `KnowledgeSnippet`, `KnowledgeExtractionAgent` sẽ phát hành một sự kiện (ví dụ: `KNOWLEDGE_SNIPPET_UPSERTED` với `snippetId` và có thể cả `content_updated_flag`).
            *   Sự kiện này sẽ được `KnowledgeEmbeddingAgent` (như mô tả trong mục 13.4.2 và 13.4.5) lắng nghe để tiến hành tạo hoặc cập nhật embedding cho `KnowledgeSnippet` tương ứng trong Supabase Vector.
            *   Điều này đảm bảo rằng các `KnowledgeSnippet` luôn có embedding cập nhật để phục vụ cho tìm kiếm ngữ nghĩa, đồng thời tối ưu hóa việc chỉ re-embed khi nội dung thực sự thay đổi (nếu `content_updated_flag` được sử dụng).

5.  **Liên kết Ngữ cảnh và Phân loại (Contextual Linking & Classification):**
    *   Agent sử dụng nội dung và từ khóa của `KnowledgeSnippet` mới tạo để tìm kiếm vector (Supabase) các thực thể liên quan trong ontology (`Project`, `Goal`, `Tension`, `Product`, `Technology`, `Expert`).
    *   Tạo các mối quan hệ `RELATED_TO` hoặc các loại quan hệ cụ thể hơn (ví dụ: `PROVIDES_EVIDENCE_FOR`, `HIGHLIGHTS_RISK_FOR`) đến các node được tìm thấy.
    *   Gán các `Category` hoặc `Tag` cho `KnowledgeSnippet` để dễ dàng tìm kiếm và quản lý.

6.  **Thông báo (Notification - Tùy chọn):**
    *   Nếu `KnowledgeSnippet` được đánh giá là có độ quan trọng cao hoặc liên quan trực tiếp đến một `Project` hoặc `Tension` đang hoạt động, Agent có thể tạo một `SystemEvent` hoặc gửi "Thông điệp Trực tiếp" đến các Agent hoặc Founder liên quan.

Luồng này đảm bảo rằng dữ liệu thô được chuyển đổi thành tri thức có cấu trúc, dễ truy cập và có thể hành động được trong TRM-OS.


**13.5.4. Luồng xử lý của GoalAlignmentAgent: Đánh giá `ProjectProposal` dựa trên `StrategicGoal`**

Luồng tác vụ này đảm bảo rằng mọi `ProjectProposal` (đề xuất dự án) đều được đánh giá một cách khách quan về mức độ phù hợp với các `StrategicGoal` (mục tiêu chiến lược) của TRM trước khi được phê duyệt.

1.  **Sự kiện Kích hoạt (Triggering Event):**
    *   Luồng bắt đầu khi một `ProjectProposal` được tạo và có trạng thái là `PendingAlignmentCheck`.
    *   Một "Ontology-Driven Event" được phát ra, thông báo cho `GoalAlignmentAgent`.

2.  **Thu thập Thông tin (Information Gathering):**
    *   Agent nhận `projectProposalId`.
    *   Nó thực thi query để lấy chi tiết của `ProjectProposal` (mô tả, mục tiêu, kết quả kỳ vọng) và toàn bộ các `StrategicGoal` đang hoạt động của công ty.
        ```yamlcypher
        MATCH (pp:ProjectProposal {proposalId: $proposalId})
        WHERE pp.status = 'PendingAlignmentCheck'
        WITH pp
        MATCH (sg:StrategicGoal {status: 'Active'})
        RETURN pp, collect(sg) AS strategicGoals;
        ```yaml

3.  **Phân tích Mức độ Phù hợp (Alignment Analysis):**
    *   **Phân tích Định lượng (Vector Search):** Agent sử dụng mô tả của `ProjectProposal` để tìm kiếm vector trên một tập chỉ mục chứa các `StrategicGoal` và `KeyResult` của chúng. Kết quả trả về là một danh sách các mục tiêu chiến lược phù hợp nhất về mặt ngữ nghĩa, kèm theo điểm số tương đồng.
    *   **Phân tích Định tính (LLM):** Agent gửi thông tin của `ProjectProposal` và top các `StrategicGoal` tương đồng nhất cho LLM. LLM đóng vai trò là một nhà phân tích chiến lược, đưa ra đánh giá chi tiết:
        *   Cho điểm mức độ phù hợp trên thang điểm 10 cho từng mục tiêu.
        *   Giải thích lý do cho điểm số.
        *   Chỉ ra các cơ hội và rủi ro tiềm ẩn nếu dự án được thực hiện.

4.  **Tạo Báo cáo Đánh giá (Generate Alignment Report):**
    *   Agent tổng hợp kết quả từ LLM và Vector Search thành một thuộc tính `alignmentReport` (dạng JSON) trên node `ProjectProposal`. Báo cáo bao gồm:
        * ` overallScore`: Điểm phù hợp tổng thể.
        * ` goalBreakdown`: Chi tiết điểm và lý giải cho từng `StrategicGoal`.
        * ` risksAndOpportunities`: Các rủi ro và cơ hội đã xác định.
        * ` recommendation`: 'Approve' (Phê duyệt), 'Revise' (Cần chỉnh sửa), hoặc 'Reject' (Từ chối) dựa trên điểm số.

5.  **Cập nhật `ProjectProposal` và Tạo Liên kết:**
    *   Agent thực thi query để cập nhật `ProjectProposal`:
        *   Lưu `alignmentReport`.
        *   Cập nhật trạng thái thành `AlignmentChecked`.
        *   Tạo mối quan hệ `ALIGNMENT_ASSESSED_FOR` từ `ProjectProposal` đến các `StrategicGoal` đã được đánh giá, lưu lại điểm số và lý giải trên chính mối quan hệ đó.
        ```yamlcypher
        MATCH (pp:ProjectProposal {proposalId: $proposalId})
        SET pp.status = 'AlignmentChecked',
            pp.alignmentReport = $reportJson
        
        WITH pp
        UNWIND $goalBreakdown AS assessment
        MATCH (sg:StrategicGoal {goalId: assessment.goalId})
        MERGE (pp)-[r:ALIGNMENT_ASSESSED_FOR]->(sg)
        SET r.score = assessment.score,
            r.justification = assessment.justification,
            r.assessedAt = datetime(),
            r.assessedBy = "GoalAlignmentAgent"
        RETURN pp;
        ```yaml

6.  **Thông báo Kết quả:**
    *   Agent phát ra sự kiện `PROJECT_PROPOSAL_ALIGNMENT_CHECKED`.
    *   Sự kiện này thông báo cho Founder hoặc những người có quyền quyết định rằng đề xuất đã sẵn sàng để được xem xét lần cuối. Thông báo bao gồm tóm tắt báo cáo và liên kết trực tiếp đến `ProjectProposal` trong TRM-OS.


**13.5.5. Luồng xử lý của WinRecognitionAgent**

1.  **Founder tạo `RecognitionEvent` (hoặc một Agent khác, hoặc User):**
    *   *Ví dụ Cypher (Người dùng tạo):*
        ```yamlcypher
        CREATE (re:RecognitionEvent {
            eventId: "RE-FDR-005",
            name: "Đề xuất công nhận hoàn thành Milestone quan trọng của Project X",
            description: "Project X đã hoàn thành Milestone Alpha đúng hạn với chất lượng vượt trội.",
            status: "PendingReview",
            createdBy: "Founder",
            createdAt: datetime()
        })
        WITH re
        MATCH (p:Project {projectId: "PROJ-X"})
        MERGE (re)-[:RELATED_TO_PROJECT]->(p)
        RETURN re;
        ```yaml

2.  **Thông báo cho `WinRecognitionAgent`:**
    * ` WinRecognitionAgent` nhận thông báo về `RecognitionEvent` mới.

3.  **`WinRecognitionAgent` Phân tích `RecognitionEvent`:**
    *   **Thu thập Ngữ cảnh (Neo4j):** Agent lấy thông tin về `Project`, `Goal`, `Output` liên quan.
    *   **Đối chiếu Tiêu chí `Win`:** Agent so sánh thành tựu với các tiêu chí được định nghĩa trước (ví dụ: hoàn thành sớm hơn 20% thời gian, vượt KPI 15%, nhận được phản hồi tích cực từ 95% người dùng thử nghiệm).
    *   **Tìm kiếm Tri thức (Supabase):** Tìm kiếm các `WinEvent` tương tự trong quá khứ để có cơ sở so sánh.

4.  **`WinRecognitionAgent` Quyết định và Tạo `WinEvent`:**
    *   Dựa trên phân tích, Agent quyết định phê duyệt `RecognitionEvent`.
    *   Agent hình thành nội dung cho `WinEvent`, mô tả rõ thành tựu và tác động của nó.
    *   Agent thực thi Cypher query để tạo node `WinEvent` và liên kết nó với các thực thể liên quan.
        ```yamlcypher
        MATCH (re:RecognitionEvent {eventId: "RE-FDR-005"})
        // Giả sử re đã được phê duyệt
        CREATE (we:WinEvent {
            winEventId: "WE-WRA-20240521-01",
            name: "Hoàn thành xuất sắc Milestone Alpha - Project X",
            description: "Nhóm dự án X đã hoàn thành Milestone Alpha sớm 3 ngày so với kế hoạch, với tất cả các tiêu chí chất lượng đều đạt mức 'xuất sắc'.",
            winScore: 9, // Ví dụ
            recognizedAt: datetime()
        })
        MERGE (we)-[:BASED_ON_RECOGNITION]->(re)
        SET re.status = "RecognizedAsWin"
        // Liên kết WinEvent với Project, Goal, v.v.
        WITH we, re
        MATCH (re)-[:RELATED_TO_PROJECT]->(p:Project)
        MERGE (we)-[:ACHIEVED_IN_PROJECT]->(p)
        RETURN we;
        ```yaml

5.  **Thông báo và Lan tỏa `WinEvent`:**
    *   Agent tạo `SystemEvent` để thông báo rộng rãi về `WinEvent` mới, lan tỏa văn hóa ghi nhận thành tích.
    *   Các `Learning` từ `WinEvent` (ví dụ: "Quy trình làm việc hiệu quả của nhóm X") có thể được chuyển cho `LearningAgent` để tạo `KnowledgeSnippet` mới, nhân rộng các thực hành tốt.

**13.5.6. Kịch bản: Giải quyết Xung đột Nguồn lực Hệ thống (Dựa trên Luồng Tác vụ 10.5.9)**

Kịch bản này minh họa cách các AI Agent phối hợp để phát hiện, đánh giá và giải quyết một xung đột nguồn lực mang tính hệ thống, dựa trên quy trình được mô tả trong Luồng Tác vụ 10.5.9.

*   **Bối cảnh:** Hai dự án quan trọng, `Project: P007` (Phát triển Module A) và `Project: P008` (Nghiên cứu Giải pháp B), đều yêu cầu sử dụng một nguồn lực khan hiếm là `Resource: QuantumComputingSimulator_License_1` (chỉ có 1 giấy phép) trong cùng một khoảng thời gian 2 tuần tới.

*   **Các Bước Chính và Tương tác Agent:**

    1.  **Phát hiện Xung đột (`TensionDetectionAgent`):**
        * ` TensionDetectionAgent`, trong quá trình quét định kỳ các kế hoạch dự án và phân bổ nguồn lực trong ontology, phát hiện ra sự chồng chéo về yêu cầu sử dụng `QuantumComputingSimulator_License_1` giữa `P007` và `P008`.
        *   Agent phát ra sự kiện: `PotentialSystemicTensionDetectedEvent(tension_id="T015", type="ResourceConflict", conflicting_resources=["QuantumComputingSimulator_License_1"], involved_projects=["P007", "P008"], details="Overlapping demand for Quantum Simulator License 1 by P007 and P008 in the next 2 weeks.")`.
        *   Một `SystemicIssueNode(id="T015", type="ResourceConflict", status="NewDetected")` được tạo trong ontology, liên kết với `P007`, `P008`, và `QuantumComputingSimulator_License_1`.

    2.  **Xác minh và Đánh giá Sơ bộ (`ResolutionCoordinatorAgent`, `OntologyManagementAgent`):**
        * ` ResolutionCoordinatorAgent` nhận `PotentialSystemicTensionDetectedEvent`.
        *   Truy vấn `OntologyManagementAgent` để lấy thông tin chi tiết về `P007`, `P008` (mục tiêu, tiến độ, độ ưu tiên hiện tại) và lịch sử sử dụng `QuantumComputingSimulator_License_1`.
        *   Xác nhận đây là một xung đột thực sự và cập nhật `SystemicIssueNode: T015` với status "Verified".

    3.  **Phân tích Chi tiết và Đánh giá Tác động (`RiskAssessmentAgent`, `StrategicAlignmentAgent`):**
        * ` RiskAssessmentAgent` được `ResolutionCoordinatorAgent` kích hoạt.
        *   Phân tích tác động: Nếu không giải quyết, cả hai dự án có thể bị trễ ít nhất 2 tuần. `P008` liên quan đến mục tiêu chiến lược "Đột phá công nghệ mới" và có mức độ ưu tiên cao hơn `P007` (tập trung vào cải tiến module hiện có). Việc trễ `P008` có thể ảnh hưởng đến mục tiêu ra mắt sản phẩm mới của quý.
        * ` StrategicAlignmentAgent` xác nhận mức độ ưu tiên chiến lược của `P008`.
        *   Kết quả phân tích được cập nhật vào `SystemicIssueNode: T015`.

    4.  **Ưu tiên hóa và Quyết định Hành động (`ResolutionCoordinatorAgent`, `StrategicAlignmentAgent`):**
        *   Dựa trên phân tích, `ResolutionCoordinatorAgent` và `StrategicAlignmentAgent` thống nhất ưu tiên giải quyết cho `P008` được sử dụng tài nguyên theo kế hoạch.
        *   Chiến lược: Tìm giải pháp điều chỉnh cho `P007` và/hoặc tăng cường nguồn lực.

    5.  **Xây dựng Kế hoạch Giải quyết (`ResolutionCoordinatorAgent`, `ProjectPlanningAgent` for P007, `ResourceManagementAgent`):**
        * ` ResolutionCoordinatorAgent` chủ trì cuộc họp (ảo) với các agent liên quan.
        * **Phương án 1 (Điều chỉnh P007):** `ProjectPlanningAgent` của `P007` phân tích và báo cáo rằng việc lùi lịch sử dụng simulator của `P007` đi 1 tuần là khả thi, chỉ gây trễ nhẹ cho một số task phụ thuộc không quan trọng.
        * **Phương án 2 (Tăng cường nguồn lực):** `ResourceManagementAgent` kiểm tra khả năng thuê thêm một license `QuantumComputingSimulator` ngắn hạn. Kết quả: có thể thuê với chi phí X, thời gian chờ 3 ngày.
        * **Quyết định:** Kết hợp cả hai. `P007` sẽ lùi lịch 1 tuần. `ResourceManagementAgent` sẽ tiến hành thuê thêm license để dự phòng và phục vụ các nhu cầu đột xuất khác.
        *   Kế hoạch giải quyết được ghi nhận, liên kết với `SystemicIssueNode: T015`.

    6.  **Triển khai Kế hoạch Hành động (Các agent liên quan, `OntologyManagementAgent`):**
        * ` ProjectPlanningAgent` (P007) cập nhật kế hoạch dự án `P007` trong ontology.
        * ` ResourceManagementAgent` thực hiện quy trình thuê license.
        * ` OntologyManagementAgent` cập nhật các thay đổi về lịch trình và trạng thái nguồn lực trong ontology.
        * ` ResolutionCoordinatorAgent` theo dõi tiến độ.

    7.  **Xác nhận Giải quyết và Lưu trữ Bài học (`ResolutionCoordinatorAgent`, `LearningAndOptimizationAgent`):**
        *   Sau khi `P007` điều chỉnh lịch và license bổ sung được xác nhận, `ResolutionCoordinatorAgent` cập nhật `SystemicIssueNode: T015` thành status "Resolved".
        * ` LearningAndOptimizationAgent` được kích hoạt. Phân tích sự cố và quá trình giải quyết, tạo `LessonLearnedNode(id="LL045")`: "Cần cải thiện quy trình đăng ký nguồn lực khan hiếm. Xem xét triển khai cơ chế cảnh báo sớm hơn khi có nhiều hơn X yêu cầu tiềm năng cho cùng một nguồn lực trong một khoảng thời gian ngắn. Đề xuất: tích hợp module dự báo nhu cầu nguồn lực."
        * ` LL045` được liên kết với `T015` và các `OntologyElement` liên quan (ví dụ: `Process: ResourceBookingProcess`).

    8.  **Thông báo Kết quả (`NotificationAgent`):**
        * ` NotificationAgent` thông báo cho Project Manager của `P007`, `P008`, và người quản lý `ResourceManagementAgent` (nếu là con người) về việc xung đột đã được giải quyết và các thay đổi liên quan.

*   **Kết luận Kịch bản:** Xung đột nguồn lực hệ thống đã được giải quyết một cách chủ động và có hệ thống, đồng thời tạo ra một bài học kinh nghiệm giá trị để cải thiện TRM-OS trong tương lai.


**PHẦN E: QUẢN TRỊ, VẬN HÀNH VÀ LỘ TRÌNH PHÁT TRIỂN (GOVERNANCE, OPERATIONS & ROADMAP)**

14. **Quản trị Ontology và Hệ thống TRM-OS (Ontology & System Governance)**

    Quản trị hiệu quả là yếu tố then chốt để đảm bảo ontology và toàn bộ hệ thống TRM-OS phát triển bền vững, chính xác và phục vụ đúng mục tiêu chiến lược của TRM.

    *   **14.1. Vai trò và Trách nhiệm**
        * **Founder (Với vai trò Ontology Steward chính, đặc biệt trong giai đoạn đầu):**
            *   Định hướng chiến lược và tầm nhìn cho ontology và TRM-OS.
            *   Phê duyệt các thay đổi lớn đối với cấu trúc ontology, đảm bảo chất lượng và sự phù hợp của ontology, và các quyết định quan trọng về hệ thống.
            *   Là người sử dụng chính và cung cấp phản hồi thường xuyên.
        * **AGE (Artificial Genesis Engine - Với sự giám sát của Founder):**
            *   Trong tương lai, AGE có thể được giao một phần trách nhiệm giám sát tính nhất quán của ontology, đề xuất các cải tiến nhỏ dựa trên dữ liệu học được.
            *   Quản lý vòng đời và điều phối các AI Agent chuyên biệt.
        * **Technical Lead/Developer (Nếu có):**
            *   Chịu trách nhiệm kỹ thuật cho việc triển khai, bảo trì và nâng cấp ontology, data pipeline và các AI agent.
            *   Đề xuất các giải pháp công nghệ và tối ưu hóa hệ thống.

    *   **14.2. Quy trình Đề xuất, Phê duyệt và Triển khai Thay đổi Ontology**
        1.  **Đề xuất Thay đổi:** Bất kỳ ai (Founder, agent, hoặc người dùng được ủy quyền trong tương lai) đều có thể đề xuất thay đổi (thêm/sửa/xóa node label, relationship type, property) thông qua một kênh chính thức (e.g., một `Tension` đặc biệt trong hệ thống, một form đề xuất).
        2.  **Phân tích Tác động:** Founder (hoặc Ontology Steward được chỉ định) đánh giá tác động của thay đổi đối với cấu trúc hiện tại, dữ liệu, các agent và quy trình nghiệp vụ.
        3.  **Thảo luận và Tinh chỉnh:** Thảo luận với các bên liên quan (nếu cần) để làm rõ và tinh chỉnh đề xuất.
        4.  **Phê duyệt:** Founder phê duyệt thay đổi.
        5.  **Triển khai Kỹ thuật:** Technical Lead/Developer thực hiện thay đổi trên môi trường staging/dev trước, bao gồm cập nhật schema Cypher, scripts nạp/trích xuất dữ liệu, và logic của các agent bị ảnh hưởng.
        6.  **Kiểm thử:** Kiểm tra kỹ lưỡng để đảm bảo thay đổi không gây lỗi và hoạt động như mong đợi.
        7.  **Triển khai trên Production:** Áp dụng thay đổi vào môi trường production.
        8.  **Thông báo và Tài liệu hóa:** Thông báo cho các bên liên quan và cập nhật tài liệu thiết kế ontology.

    *   **14.3. Quản lý Phiên bản Ontology**
        *   Mỗi thay đổi lớn trong cấu trúc ontology (ví dụ: thêm/sửa/xóa node label, relationship type, hoặc các thuộc tính cốt lõi có ảnh hưởng rộng) nên được ghi nhận như một phiên bản mới của ontology (e.g., sử dụng đánh số phiên bản như v3.2.1, v3.3 để phản ánh mức độ thay đổi).
        *   Sử dụng Git hoặc một hệ thống quản lý phiên bản tương tự để lưu trữ các file định nghĩa schema Cypher và tài liệu thiết kế.
        *   Đảm bảo các AI agent và data pipeline tương thích với phiên bản ontology hiện hành.

    *   **14.4. Giám sát Chất lượng Dữ liệu, Ontology và Sự tuân thủ Triết lý**
        * **Kiểm tra Tính nhất quán Dữ liệu:** `AGE` hoặc các script giám sát định kỳ sẽ kiểm tra các ràng buộc dữ liệu (constraints), phát hiện các node/relationship mồ côi, các giá trị thuộc tính không hợp lệ (ví dụ: sai kiểu dữ liệu, không thuộc danh mục cho phép, giá trị nằm ngoài khoảng mong đợi), hoặc các mâu thuẫn logic trong dữ liệu. **Các phát hiện này nên được ghi log chi tiết (bao gồm cả mức độ nghiêm trọng và nguồn gốc nghi ngờ), phân loại và theo dõi để phân tích nguyên nhân gốc rễ và cải tiến liên tục quy trình nạp dữ liệu cũng như chất lượng nguồn.** Các `DataIngestionAgent` cũng cần có cơ chế xác thực đầu vào mạnh mẽ và báo cáo lại các vấn đề gặp phải.
        * **Đánh giá Mức độ Phủ và Chính xác của Ontology:** Định kỳ rà soát xem ontology có còn phản ánh đúng, đầy đủ và chính xác các khái niệm, thực thể, mối quan hệ và quy trình nghiệp vụ cốt lõi của TRM hay không. Quá trình này bao gồm so sánh với các tài liệu nghiệp vụ hiện hành, phỏng vấn người dùng (bao gồm Founder và các chuyên gia tên miền nếu có), **và có thể sử dụng các công cụ trực quan hóa ontology để hỗ trợ phân tích cấu trúc, phát hiện các khoảng trống, sự dư thừa hoặc sự không nhất quán logic trong mô hình.**
        * **Phản hồi từ Agent về Chất lượng Dữ liệu/Ontology:** Các AI agent được thiết kế để chủ động báo cáo các trường hợp dữ liệu không nhất quán, thiếu thông tin, không rõ ràng, hoặc không thể xử lý được do vấn đề về cấu trúc ontology (ví dụ: thiếu thuộc tính cần thiết, mối quan hệ không phù hợp) hoặc chất lượng dữ liệu đầu vào. **Các báo cáo này (ví dụ: thông qua việc tạo `SystemEvent` loại `DATA_QUALITY_ISSUE` hoặc `ONTOLOGY_FEEDBACK`, hoặc ghi vào hệ thống log tập trung với tag cụ thể) cần được thu thập, phân tích, ưu tiên hóa và giao cho người có trách nhiệm xử lý để cải tiến ontology, quy trình làm sạch dữ liệu và logic của agent.**
        * **Đảm bảo Sự tuân thủ Triết lý (Philosophy Alignment) và Hiệu quả Vận hành:**
            * **Nguyên tắc Thiết kế:** Mọi agent và quy trình mới phải được thiết kế và đánh giá dựa trên sự phù hợp và khả năng củng cố triết lý "Recognition → Event → WIN" và các nguyên tắc vận hành nền tảng (Mô hình Lượng tử, Ba Miền, Sáu Bước).
            * **Kiểm tra Định kỳ:** Thông qua các truy vấn Cypher phức tạp trên graph và phân tích log hoạt động của agent, đánh giá xem các chuỗi nhân quả cốt lõi (ví dụ: một `WIN` có thực sự bắt nguồn từ một `RecognitionEvent` có ý nghĩa không? `Tension` có được xử lý hiệu quả không? Các `Project` có đóng góp vào `Goal` không?) có đang diễn ra như mong đợi và mang lại giá trị thực không. **Kết quả của các kiểm tra này cần được ghi nhận, trực quan hóa (nếu có thể), thảo luận trong các buổi rà soát định kỳ và có thể dẫn đến các điều chỉnh trong ontology, logic agent hoặc quy trình vận hành.**
            * **Cảnh báo Chủ động khi có Độ vênh:** Hệ thống (đặc biệt là `AGE`) có thể được cấu hình để cảnh báo nếu phát hiện các mẫu hành vi đi ngược lại triết lý cốt lõi, các điểm nghẽn trong vòng lặp vận hành (ví dụ: `Resource` được tạo ra mà không có `WIN` tương ứng, `Tension` quan trọng bị bỏ qua quá lâu, tỷ lệ `RecognitionEvent` dẫn đến `WIN` thấp bất thường), hoặc các chỉ số KPI quan trọng về tuân thủ triết lý giảm sút. **Các cảnh báo này nên được gửi đến người có trách nhiệm và kích hoạt một quy trình rà soát, phân tích nguyên nhân và hành động khắc phục cụ thể.**

    *   **14.5. An ninh và Phân quyền Truy cập**
        * **Neo4j Aura:** Sử dụng các cơ chế phân quyền của Neo4j (roles, privileges) để kiểm soát quyền truy cập vào dữ liệu graph. Các agent sẽ có user/role riêng với quyền hạn giới hạn theo nhu cầu (e.g., `KnowledgeExtractionAgent` có quyền ghi, các agent khác chủ yếu có quyền đọc).
        * **Supabase Vector:** Quản lý API keys, sử dụng Row Level Security (RLS) để kiểm soát quyền truy cập chi tiết đến từng dòng dữ liệu, và định nghĩa các chính sách (policies) truy cập của Supabase.
        * **Snowflake:** Sử dụng Role-Based Access Control (RBAC) của Snowflake để phân quyền truy cập chi tiết vào dữ liệu trong data lake/warehouse, bao gồm cả schema, table, view và các đối tượng khác.
        * **API Access:** Bảo vệ các API endpoint của agent và các dịch vụ bên ngoài bằng authentication và authorization.
        * **Dữ liệu Nhạy cảm:** Áp dụng các biện pháp mã hóa (cả khi lưu trữ và truyền tải) và che giấu dữ liệu (data masking) nếu cần thiết đối với các thông tin nhạy cảm.
        * **Nguyên tắc Đặc quyền Tối thiểu (Principle of Least Privilege):** Luôn cấp quyền truy cập tối thiểu cần thiết cho người dùng và agent để thực hiện nhiệm vụ của họ.
        * **Rà soát Quyền Định kỳ:** Các quyền truy cập của người dùng và agent vào các hệ thống (Neo4j, Supabase, Snowflake, API) cần được rà soát định kỳ (ví dụ: hàng quý hoặc sau mỗi thay đổi lớn về nhân sự/hệ thống) để đảm bảo tuân thủ nguyên tắc đặc quyền tối thiểu và loại bỏ các quyền không còn cần thiết.

    *   **14.6. Nguyên tắc Đạo đức và Kiểm soát AI**
        * **Minh bạch (Transparency):** Thiết kế hệ thống sao cho có thể giải thích được (ở một mức độ nhất định) tại sao một agent đưa ra quyết định hoặc hành động cụ thể. AGE và các agent khác có thể ghi log các quyết định quan trọng và các yếu tố chính (ví dụ: `Event` đầu vào, `KnowledgeSnippet` được sử dụng, `Rule` được áp dụng) dẫn đến quyết định đó, trong một định dạng có thể truy vấn và hiểu được bởi con người.
        * **Công bằng (Fairness):** Đảm bảo các thuật toán (bao gồm cả các thuật toán dựa trên quy tắc và các mô hình học máy nếu có trong tương lai) và dữ liệu được sử dụng (bao gồm dữ liệu huấn luyện và dữ liệu vận hành) không tạo ra hoặc duy trì sự thiên vị không mong muốn, dẫn đến phân biệt đối xử hoặc kết quả không công bằng cho các cá nhân hay nhóm đối tượng.
        * **Trách nhiệm giải trình (Accountability):** Luôn có sự giám sát của con người (Founder hoặc người được ủy quyền) đối với các hoạt động và quyết định quan trọng của hệ thống. Con người chịu trách nhiệm cuối cùng trong việc định hướng chiến lược, kiểm tra, đánh giá hiệu quả và can thiệp khi cần thiết để đảm bảo hệ thống hoạt động đúng mục tiêu và tuân thủ các nguyên tắc đã đặt ra.
        * **Quyền riêng tư (Privacy):** Tôn trọng quyền riêng tư dữ liệu, đặc biệt là thông tin cá nhân. Thu thập và sử dụng dữ liệu theo đúng mục đích đã định.
        * **An toàn (Safety):** Thiết kế các cơ chế an toàn để ngăn chặn các hành vi không mong muốn hoặc gây hại từ các agent, bao gồm cả các kịch bản lỗi không lường trước và khả năng bị lạm dụng. Điều này có thể bao gồm các giới hạn về phạm vi hành động của agent (ví dụ: không tự động xóa dữ liệu quan trọng mà không có xác nhận), cơ chế ngắt khẩn cấp (kill switch) hoặc tạm dừng hoạt động được kiểm soát bởi con người, và kiểm thử nghiêm ngặt các kịch bản rủi ro tiềm ẩn.

15. **Vận hành Hệ thống TRM-OS (System Operations)**

    Đảm bảo hệ thống TRM-OS hoạt động ổn định, hiệu quả và an toàn là ưu tiên hàng đầu.

    *   **15.1. Giám sát và Bảo trì Hệ thống**
        * **Dashboards Giám sát Toàn diện:** Thiết lập dashboards (sử dụng công cụ của Neo4j, Supabase, Snowflake hoặc các công cụ giám sát chung như Grafana, Prometheus) để theo dõi:
            *   Tình trạng hoạt động của các database (Neo4j, Supabase, Snowflake) và các thành phần hạ tầng khác (ví dụ: message queues, API gateways).
            *   Hiệu suất truy vấn, tải hệ thống, và tài nguyên hệ thống (CPU, memory, disk I/O, network) của các server/container.
            *   Số lượng `Event`, `Node`, `Relationship` được tạo/cập nhật, và tình trạng hàng đợi sự kiện (event queues) nếu có (ví dụ: độ dài hàng đợi, thời gian xử lý trung bình).
            *   Hoạt động của các AI Agent (số tác vụ xử lý, tỷ lệ lỗi, thời gian phản hồi trung bình, tài nguyên tiêu thụ, tình trạng kết nối đến các dịch vụ phụ thuộc).
        * **Log Analysis and Alerting:** Tập trung và phân tích log (sử dụng các công cụ như ELK stack, Splunk, hoặc dịch vụ cloud logging) từ tất cả các thành phần hệ thống để phát hiện sớm các vấn đề, gỡ lỗi và phân tích xu hướng bất thường. **Thiết lập hệ thống cảnh báo (alerting) tự động dựa trên các mẫu log quan trọng, ngưỡng lỗi, hoặc các sự kiện bất thường để thông báo cho đội ngũ vận hành kịp thời qua các kênh phù hợp (e.g., email, Slack, PagerDuty).**
        * **Bảo trì Chủ động và Định kỳ:** Lên lịch cho các hoạt động bảo trì như tối ưu hóa index, dọn dẹp dữ liệu cũ hoặc không còn liên quan (theo chính sách lưu trữ dữ liệu), cập nhật phiên bản phần mềm, hệ điều hành và các thư viện phụ thuộc (dependencies) của agent và hệ thống sau khi đã kiểm thử kỹ lưỡng. **Thực hiện kiểm tra tính toàn vẹn của các bản sao lưu (backup integrity checks) một cách thường xuyên và tự động nếu có thể.**
        * **Quản lý Cấu hình (Configuration Management):** Đảm bảo tất cả các cấu hình của hệ thống (databases, agents, services, infrastructure) được quản lý bằng mã (ví dụ: sử dụng Terraform, Ansible, Docker Compose), lưu trữ trong hệ thống kiểm soát phiên bản (ví dụ: Git), được kiểm tra, đánh giá và triển khai một cách tự động, nhất quán và có khả năng rollback.

    *   **15.2. Sao lưu và Phục hồi Dữ liệu (Backup & Recovery)**

        Đảm bảo khả năng phục hồi dữ liệu và hệ thống sau sự cố là cực kỳ quan trọng để duy trì hoạt động liên tục và bảo vệ tài sản tri thức của TRM.

        * **Chiến lược Sao lưu (Backup Strategy):**
            * **Phạm vi Sao lưu:** Tất cả các thành phần dữ liệu quan trọng phải được sao lưu, bao gồm:
                * **Neo4j Aura Database:** Dữ liệu đồ thị ontology.
                * **Supabase Database:** Dữ liệu vector embeddings và các bảng phụ trợ.
                * **Snowflake Data Lake/Warehouse:** Dữ liệu thô và đã qua xử lý.
                * **Mã nguồn Agent và Hệ thống:** Lưu trữ trên Git repository (ví dụ: GitHub, GitLab) với các nhánh (branch) và thẻ (tag) phiên bản rõ ràng.
                * **Cấu hình Hệ thống:** Các file cấu hình của agent, database, và các dịch vụ hạ tầng (được quản lý qua Configuration Management như đã đề cập ở 15.1).
            * **Tần suất và Loại Sao lưu:**
                * **Neo4j Aura & Supabase:** Tận dụng tính năng sao lưu tự động, liên tục hoặc hàng ngày (daily backups) do các nhà cung cấp dịch vụ quản lý. Cấu hình Point-in-Time Recovery (PITR) nếu có và phù hợp với RPO.
                * **Snowflake:** Tận dụng Time Travel (lên đến 90 ngày) và Fail-safe. Sao lưu dữ liệu quan trọng định kỳ nếu cần thiết ra ngoài Snowflake cho mục đích lưu trữ dài hạn hoặc tuân thủ quy định.
                * **Mã nguồn và Cấu hình:** Sao lưu mỗi khi có thay đổi (commit) vào Git repository.
            * **Lưu trữ Bản sao lưu:**
                *   Đối với các dịch vụ cloud (Aura, Supabase, Snowflake), bản sao lưu thường được quản lý bởi nhà cung cấp, đảm bảo tính sẵn sàng và đa dạng vùng.
                *   Xem xét việc xuất (export) và lưu trữ bản sao lưu định kỳ của các dữ liệu quan trọng nhất ra một giải pháp lưu trữ độc lập (ví dụ: AWS S3, Azure Blob Storage) với chính sách mã hóa và kiểm soát truy cập nghiêm ngặt, đặc biệt cho mục đích lưu trữ dài hạn (archival) hoặc DR (Disaster Recovery) ở một region khác.
            * **Chính sách Lưu giữ (Retention Policy):** Xác định rõ thời gian lưu giữ cho từng loại bản sao lưu, cân bằng giữa nhu cầu phục hồi và chi phí lưu trữ (ví dụ: bản sao lưu hàng ngày giữ trong 30 ngày, hàng tuần trong 3 tháng, hàng tháng trong 1 năm).
            * **Mã hóa Bản sao lưu:** Đảm bảo tất cả các bản sao lưu được mã hóa cả khi đang truyền (in transit) và khi lưu trữ (at rest).

        * **Quy trình Phục hồi (Recovery Procedures):**
            * **Tài liệu hóa:** Xây dựng và duy trì tài liệu chi tiết về quy trình phục hồi cho từng thành phần hệ thống, bao gồm các bước thực hiện, thông tin đăng nhập cần thiết, và các điểm cần lưu ý.
            * **Xác định RTO và RPO:**
                * **Recovery Time Objective (RTO):** Thời gian tối đa cho phép để phục hồi hệ thống và dịch vụ về trạng thái hoạt động sau sự cố. (Ví dụ: 4 giờ cho hệ thống chính, 24 giờ cho hệ thống phụ).
                * **Recovery Point Objective (RPO):** Lượng dữ liệu tối đa có thể chấp nhận bị mất, tính bằng thời gian từ điểm sự cố trở về trước. (Ví dụ: 15 phút cho dữ liệu giao dịch, 1 ngày cho dữ liệu phân tích).
                Các giá trị RTO/RPO này cần được Founder phê duyệt và rà soát định kỳ.
            * **Kiểm thử Phục hồi (Recovery Drills):**
                *   Lên lịch và thực hiện kiểm thử quy trình phục hồi dữ liệu và hệ thống từ bản sao lưu một cách định kỳ (ví dụ: hàng quý hoặc sau mỗi thay đổi lớn về kiến trúc hệ thống).
                *   Kiểm thử bao gồm các kịch bản khác nhau (ví dụ: mất một phần dữ liệu, mất toàn bộ database, lỗi agent nghiêm trọng).
                *   Ghi nhận lại kết quả kiểm thử, thời gian thực hiện, các vấn đề phát sinh và các bài học kinh nghiệm để cải tiến quy trình và tài liệu phục hồi.

        * **Công cụ và Tự động hóa Sao lưu & Phục hồi:**
            *   Ưu tiên sử dụng các tính năng sao lưu và phục hồi tích hợp sẵn của Neo4j Aura, Supabase, và Snowflake.
            *   Tự động hóa tối đa quy trình sao lưu, giám sát trạng thái hoàn thành của các tác vụ sao lưu, và gửi cảnh báo nếu có lỗi xảy ra.
            *   Sử dụng script hoặc các công cụ IaC (Infrastructure as Code) để tự động hóa việc khôi phục cấu hình hệ thống và triển khai lại agent nếu cần.

        * **Vai trò và Trách nhiệm trong Sao lưu & Phục hồi:**
            *   Xác định rõ vai trò và trách nhiệm của Technical Lead/Developer hoặc người được chỉ định trong việc giám sát hoạt động sao lưu, khởi xướng và thực hiện quy trình phục hồi khi có sự cố, và duy trì tài liệu liên quan.

    *   **15.3. Quản lý Sự cố (Incident Management)**

        Quy trình quản lý sự cố hiệu quả giúp giảm thiểu tác động của các gián đoạn ngoài kế hoạch và khôi phục hoạt động bình thường của hệ thống một cách nhanh chóng.

        1.  **Phát hiện và Ghi nhận (Detection & Logging):**
            *   Sự cố có thể được phát hiện tự động bởi hệ thống giám sát (mục 15.1) hoặc được báo cáo bởi người dùng/agent.
            *   Mọi sự cố đều phải được ghi nhận ngay lập tức vào một hệ thống theo dõi (ví dụ: Jira, một loại `Tension` đặc biệt trong TRM-OS) với các thông tin ban đầu: thời gian, nguồn phát hiện, mô tả triệu chứng, các thành phần bị ảnh hưởng, và mức độ ưu tiên ban đầu.

        2.  **Phân loại và Ưu tiên hóa (Classification & Prioritization):**
            *   Sự cố được phân loại dựa trên lĩnh vực bị ảnh hưởng (ví dụ: database, agent logic, data pipeline, security).
            *   Mức độ ưu tiên được xác định dựa trên tác động kinh doanh (business impact) và tính khẩn cấp (urgency). Ví dụ: P1 (Critical - hệ thống ngừng hoạt động), P2 (High), P3 (Medium), P4 (Low).

        3.  **Ứng phó và Giải quyết (Response & Resolution):**
            *   Chỉ định người chịu trách nhiệm chính (incident commander) cho các sự cố nghiêm trọng.
            *   Thực hiện các bước chẩn đoán để xác định nguyên nhân gốc rễ (root cause).
            *   Áp dụng các giải pháp tạm thời (workaround) để khôi phục dịch vụ nhanh nhất có thể, sau đó mới tiến hành giải pháp triệt để (permanent fix).
            *   Giao tiếp, cập nhật tình hình thường xuyên cho các bên liên quan (stakeholders).

        4.  **Phân tích sau Sự cố (Post-Incident Review):**
            *   Sau khi sự cố được giải quyết, tổ chức một buổi họp "Postmortem" (không đổ lỗi) cho các sự cố nghiêm trọng (P1, P2).
            *   Phân tích chi tiết dòng thời gian sự kiện, nguyên nhân gốc rễ, tác động, các hành động đã thực hiện và hiệu quả của chúng.
            *   Xác định các bài học kinh nghiệm (lessons learned) và các hành động cần thực hiện (action items) để ngăn ngừa sự cố tái diễn trong tương lai. Các `action item` này sẽ được tạo thành các `Task` hoặc `Project` trong TRM-OS để theo dõi.

16. **Lộ trình Phát triển TRM-OS (Roadmap)**

    Lộ trình phát triển TRM-OS được chia thành các giai đoạn logic, tập trung vào việc xây dựng và hoàn thiện hệ thống một cách có hệ thống. Việc triển khai sẽ được thực hiện chủ yếu bởi các AI Agent, với sự giám sát và định hướng chiến lược từ Founder. Mỗi giai đoạn sẽ bao gồm các mục tiêu chính, tính năng cụ thể, công nghệ dự kiến và kết quả mong đợi.

    --- 
**GIAI ĐOẠN 1: XÂY DỰNG NỀN TẢNG VÀ CHỨC NĂNG CỐT LÕI (MVP - MINIMUM VIABLE PRODUCT)**

    Mục tiêu của giai đoạn này là thiết lập một phiên bản hoạt động cơ bản của TRM-OS, bao gồm ontology cốt lõi, các luồng nhập liệu ban đầu, khả năng truy vấn cơ bản, và các quy trình quản trị, vận hành nền tảng. Các AI agent đầu tiên sẽ được triển khai để hỗ trợ các tác vụ này.

    *   **16.1. Mục tiêu chính (Key Objectives):**
        *   Hoàn thiện và triển khai phiên bản đầu tiên (v1.0) của TRM Internal Ontology, tập trung vào các lĩnh vực và khái niệm ưu tiên đã được xác định.
        *   Thiết lập và tự động hóa các luồng nhập liệu (data ingestion pipelines) cho các nguồn dữ liệu quan trọng ban đầu (ví dụ: tài liệu nội bộ, cơ sở dữ liệu hiện có, một số nguồn web chọn lọc).
        *   Xây dựng khả năng truy vấn và khai thác ontology cơ bản cho người dùng (Founder) và các AI agent khác.
        *   Đưa vào vận hành các quy trình Quản trị Ontology (Section 14) và Vận hành Hệ thống (Section 15) đã được định nghĩa.
        *   Triển khai các AI agent cốt lõi đầu tiên để hỗ trợ xây dựng, duy trì và khai thác ontology.
            *   Mở rộng khả năng tương tác đa phương thức (e.g., nhập liệu bằng giọng nói cho Founder).
            *   Nghiên cứu và phát triển các tính năng mới dựa trên tri thức và dữ liệu đã tích lũy (e.g., phân tích xu hướng, tạo báo cáo thông minh).
            *   Khám phá khả năng liên kết ontology của TRM với các nguồn tri thức bên ngoài (Linked Open Data) nếu phù hợp.

    *   **16.2. Các Tính năng Chính và Phạm vi (Key Features and Scope):**
        * **Ontology Schema & Content (v1.0):**
            *   Định nghĩa và triển khai các Lớp (Classes) và Mối quan hệ (Relationships) cốt lõi.
            *   Nhập liệu thủ công và bán tự động cho các thực thể ban đầu quan trọng.
        * **Data Ingestion Agents (MVP):**
            *   Agent cho structured text (Markdown, CSV).
            *   Agent thử nghiệm cho Google Calendar.
        * **Query & Access:**
            *   Giao diện dòng lệnh hoặc script đơn giản để thực hiện Cypher query.
            *   API endpoint cơ bản cho vector search.
        * **Governance & System Operations (MVP):**
            *   Quy trình backup thủ công/bán tự động.
            *   Tài liệu quản lý phiên bản ontology.
            *   Dashboard giám sát cơ bản (Neo4j, Supabase).
        * **AI Agents (MVP):**
            * ` KnowledgeIngestionAgent`: Xử lý các định dạng đơn giản.
            * ` BasicQueryAgent`: Trả lời các câu hỏi dựa trên template Cypher.

    *   **16.3. Công nghệ và Công cụ Dự kiến (Tentative Technologies and Tools):**
        * **Graph Database:** Neo4j Aura.
        * **Vector Database:** Supabase Vector (pgvector).
        * **Data Storage/Staging:** Supabase Storage, Snowflake (cho dữ liệu có cấu trúc lớn nếu cần).
        * **AI Agent Development:** Python, LangChain, OpenAI API (hoặc các LLM tương đương).
        * **Workflow Orchestration (đơn giản):** Python scripts, Supabase Functions.
        * **Monitoring:** Các dashboard tích hợp sẵn của Neo4j Aura, Supabase.
        * **Version Control:** Git (cho code agent, cấu hình, tài liệu ontology).

    *   **16.4. Kết quả mong đợi/Chỉ số thành công (Expected Outcomes/Success Metrics):**
        *   Ontology v1.0 được triển khai và chứa dữ liệu từ ít nhất 2 nguồn.
        *   Ít nhất 2 AI agent MVP hoạt động và thực hiện được các chức năng cơ bản.
        *   Founder có thể thực hiện truy vấn và tìm kiếm cơ bản trên ontology.
        *   Hệ thống có khả năng sao lưu và phục hồi.
        *   Tài liệu kiến trúc và vận hành cơ bản được hoàn thành.
        *   Giảm X% thời gian tìm kiếm thông tin thủ công cho Founder (cần baseline).
        *   Hoàn thành thành công ít nhất một kịch bản kiểm thử phục hồi dữ liệu (disaster recovery drill) cho Neo4j và Supabase.

---

**GIAI ĐOẠN 2: MỞ RỘNG VÀ TINH CHỈNH (EXPANSION AND REFINEMENT)**

    Mục tiêu của giai đoạn này là mở rộng phạm vi của ontology, tích hợp các nguồn dữ liệu phức tạp hơn, nâng cao năng lực của các AI agent hiện có và giới thiệu các agent chuyên biệt mới. Đồng thời, cải thiện các quy trình quản trị, giám sát và bảo mật.

    *   **16.5. Mục tiêu chính (Key Objectives):**
        *   Mở rộng ontology để bao phủ các lĩnh vực kiến thức mới và các loại thực thể/mối quan hệ chi tiết hơn (ví dụ: `FinancialTransaction`, `MarketTrend`, `CompetitorProfile`).
        *   Tích hợp các nguồn dữ liệu phức tạp hơn, bao gồm dữ liệu phi cấu trúc (ví dụ: PDF, email, bản ghi âm cuộc họp) và dữ liệu bán cấu trúc (ví dụ: API từ các SaaS tool khác).
        *   Nâng cấp các AI agent hiện có (ví dụ: `KnowledgeIngestionAgent` để xử lý OCR, `QueryAgent` để hiểu ngôn ngữ tự nhiên phức tạp hơn).
        *   Phát triển và triển khai các AI agent chuyên biệt mới:
            * ` InsightGenerationAgent`: Tự động phát hiện các mẫu, mối tương quan và insight tiềm ẩn trong ontology.
            * ` PredictiveAnalyticsAgent`: Dự đoán các xu hướng hoặc kết quả dựa trên dữ liệu lịch sử và hiện tại.
            * ` TensionDetectionAgent` (nâng cao): Chủ động phát hiện các "Tension" tiềm ẩn từ nhiều nguồn dữ liệu.
            * ` SolutionProposalAgent`: Đề xuất các giải pháp hoặc dự án tiềm năng để giải quyết "Tension".
            * ` ContentSummarizationAgent`: Tóm tắt các tài liệu dài hoặc các cuộc thảo luận.
        *   Cải thiện khả năng trực quan hóa ontology và kết quả phân tích.
        *   Tăng cường các biện pháp an ninh, quản lý truy cập và kiểm toán hệ thống.
        *   Thiết lập quy trình MLOps cơ bản cho việc huấn luyện, đánh giá và triển khai các mô hình AI (nếu có mô hình tùy chỉnh).

    *   **16.6. Các Tính năng Chính và Phạm vi (Key Features and Scope):**
        * **Ontology Expansion & Alignment:**
            *   Thêm các domain mới, classes, relationships.
            *   Công cụ hoặc quy trình để căn chỉnh với các ontology bên ngoài (nếu cần).
        * **Advanced Data Ingestion:**
            *   OCR cho tài liệu PDF.
            *   Speech-to-text cho bản ghi âm.
            *   Kết nối API tới các SaaS tool (ví dụ: CRM, ERP, Google Analytics).
            *   Xử lý email.
        * **Enhanced AI Agents:**
            * ` KnowledgeIngestionAgent` với khả năng xử lý đa định dạng.
            * ` AdvancedQueryAgent` với Natural Language Understanding (NLU) tốt hơn, khả năng đối thoại.
        * **New Specialized AI Agents:**
            * ` InsightGenerationAgent` (ví dụ: phát hiện cộng đồng, phân tích đường dẫn).
            * ` PredictiveAnalyticsAgent` (ví dụ: dự đoán rủi ro dự án).
            * ` ContentSummarizationAgent`.
        * **Ontology Visualization & Exploration:**
            *   Tích hợp với các công cụ trực quan hóa đồ thị (ví dụ: Neo4j Bloom, custom D3.js).
        * **Workflow Orchestration:**
            *   Sử dụng công cụ như Apache Airflow hoặc Temporal.io cho các pipeline dữ liệu và AI phức tạp.
        * **Security & Governance Enhancements:**
            *   Role-Based Access Control (RBAC) chi tiết hơn.
            *   Logging và auditing nâng cao.
            *   Quy trình đánh giá và giảm thiểu thiên kiến trong AI.

    *   **16.7. Công nghệ và Công cụ Dự kiến (Tentative Technologies and Tools):**
        * **OCR:** Tesseract OCR, Google Cloud Vision AI.
        * **Speech-to-text:** OpenAI Whisper, Google Cloud Speech-to-Text.
        * **NLU/NLP Libraries:** spaCy, NLTK, Transformers (Hugging Face).
        * **Workflow Orchestration:** Apache Airflow, Temporal.io, Prefect.
        * **Visualization:** Neo4j Bloom, Gephi, custom solutions (D3.js, Plotly Dash).
        * **MLOps Tools (nếu cần):** MLflow, Kubeflow.
        * **Security Tools:** Vault (quản lý secret), các công cụ quét lỗ hổng.

    *   **16.8. Kết quả mong đợi/Chỉ số thành công (Expected Outcomes/Success Metrics):**
        *   Ontology được mở rộng để bao phủ thêm ít nhất 2-3 lĩnh vực kiến thức mới.
        *   Tích hợp thành công ít nhất 2 loại nguồn dữ liệu phức tạp mới (ví dụ: PDF, API từ SaaS).
        *   Ít nhất 2 AI agent chuyên biệt mới được triển khai và chứng minh giá trị.
        *   Khả năng NLU của `QueryAgent` được cải thiện X%.
        *   Hệ thống có khả năng tạo ra Y insight có giá trị mỗi tháng (cần định nghĩa "giá trị").
        *   Giảm Z% thời gian cho các tác vụ phân tích thủ công.
        *   Hoàn thành kiểm thử thâm nhập (penetration testing) và giải quyết các lỗ hổng nghiêm trọng.
        *   Tỷ lệ tự động hóa cho các quy trình mục tiêu tăng lên W%.

---

**GIAI ĐOẠN 3: VẬN HÀNH THÔNG MINH VÀ TIẾN HÓA TỰ CHỦ (INTELLIGENT OPERATIONS & AUTONOMOUS EVOLUTION)**

    Mục tiêu của giai đoạn này là đạt được mức độ tự động hóa cao, cho phép hệ thống TRM-OS không chỉ vận hành thông minh mà còn có khả năng tự học hỏi, tự tối ưu hóa và đề xuất các cải tiến cho chính ontology và các quy trình vận hành của TRM. Các AI agent sẽ hoạt động như một "bộ não số" thực sự, chủ động và cộng tác.

    *   **16.9. Mục tiêu chính (Key Objectives):**
        *   Đạt được khả năng tự động làm giàu và tinh chỉnh ontology (Ontology Self-Enrichment and Refinement) dựa trên dữ liệu mới và phản hồi từ các agent.
        *   Phát triển các AI agent có khả năng học hỏi liên tục (Continuous Learning Agents) và thích ứng với các thay đổi trong môi trường hoạt động của TRM.
        *   Triển khai các cơ chế tự giám sát, tự chẩn đoán và tự phục hồi (Self-Monitoring, Self-Diagnosis, Self-Healing) cho các thành phần của TRM-OS.
        *   Nâng cao khả năng giải thích (Explainability - XAI) cho các quyết định và đề xuất của AI agent, giúp Founder hiểu rõ hơn về logic hoạt động của hệ thống.
        *   Tích hợp sâu hơn với các quy trình ra quyết định chiến lược của TRM, cung cấp các phân tích dự báo và kịch bản "what-if" phức tạp.
        *   Thử nghiệm các mô hình quản trị phi tập trung (Decentralized Governance) cho một số khía cạnh của ontology hoặc hoạt động của agent, nếu phù hợp.
        *   Xây dựng nền tảng cho việc TRM-OS có thể tự đề xuất các "WIN" mới hoặc các cơ hội cải tiến quy trình.

    *   **16.10. Các Tính năng Chính và Phạm vi (Key Features and Scope):**
        * **Ontology Evolution Framework:**
            *   Agent chuyên biệt (`OntologyEvolutionAgent`) giám sát chất lượng ontology, đề xuất thêm/sửa/xóa schema, và tự động cập nhật (với sự giám sát của Founder).
            *   Cơ chế phát hiện sự trôi dạt khái niệm (concept drift) và đề xuất điều chỉnh.
        * **Advanced Reinforcement Learning Agents:**
            *   Một số agent (ví dụ: `ResourceAllocationAgent`, `WorkflowOptimizationAgent`) sử dụng Reinforcement Learning để tối ưu hóa hành động theo thời gian.
        * **Explainable AI (XAI) Dashboard:**
            *   Giao diện hiển thị lý do đằng sau các đề xuất hoặc quyết định quan trọng của AI.
        * **Proactive System Health Management:**
            *   Agent giám sát hiệu suất, phát hiện bất thường và tự động thực hiện các hành động khắc phục cơ bản.
        * **Strategic Foresight & Scenario Planning Module:**
            *   Agent mô phỏng các kịch bản kinh doanh khác nhau dựa trên ontology và dữ liệu hiện tại.
        * **Automated WIN Discovery:**
            *   Agent phân tích dữ liệu và hoạt động để chủ động xác định các cơ hội "WIN" tiềm năng.
        * **Knowledge Graph Embeddings for Advanced Analytics:**
            *   Sử dụng KGEs cho các tác vụ như link prediction, node classification để làm giàu ontology và hỗ trợ insight.
        * **Federated Learning (Nếu có nguồn dữ liệu phân tán và nhạy cảm):**
            *   Huấn luyện mô hình AI trên nhiều nguồn dữ liệu mà không cần di chuyển dữ liệu.

    *   **16.11. Công nghệ và Công cụ Dự kiến (Tentative Technologies and Tools):**
        * **Reinforcement Learning Frameworks:** OpenAI Gym, Ray RLlib.
        * **XAI Libraries:** SHAP, LIME, Captum.
        * **Probabilistic Graphical Models / Bayesian Networks:** Cho suy luận bất định.
        * **Advanced Anomaly Detection Algorithms.**
        * **Knowledge Graph Embedding Libraries:** PyKEEN, AmpliGraph.
        * **Federated Learning Frameworks:** PySyft, TensorFlow Federated.
        * **Chaos Engineering Tools:** (ví dụ: Chaos Mesh) để kiểm thử khả năng phục hồi của hệ thống.

    *   **16.12. Kết quả mong đợi/Chỉ số thành công (Expected Outcomes/Success Metrics):**
        *   Ontology có khả năng tự cập nhật và mở rộng với tỷ lệ X% các thay đổi được đề xuất tự động và được phê duyệt.
        *   Ít nhất một agent chủ chốt thể hiện khả năng học hỏi và cải thiện hiệu suất theo thời gian (ví dụ: giảm Y% lỗi, tăng Z% hiệu quả).
        *   Hệ thống có khả năng tự động phát hiện và khắc phục A% các sự cố thường gặp.
        *   Mức độ tin cậy và chấp nhận của Founder đối với các đề xuất từ AI tăng (đo bằng khảo sát hoặc tỷ lệ chấp thuận đề xuất).
        *   Số lượng "WIN" được hệ thống tự động đề xuất và được Founder công nhận đạt B mỗi quý.
        *   Giảm thời gian cần thiết để hệ thống thích ứng với các thay đổi lớn trong cấu trúc dữ liệu hoặc quy trình của TRM.
        *   Hoàn thành thành công các kịch bản kiểm thử hỗn loạn (chaos engineering tests) để xác minh tính bền vững.

---

**GIAI ĐOẠN 4: TẦM NHÌN TƯƠNG LAI VÀ ĐỔI MỚI LIÊN TỤC (FUTURE VISION & CONTINUOUS INNOVATION)**

    Giai đoạn này tập trung vào việc duy trì vị thế dẫn đầu của TRM-OS thông qua nghiên cứu và tích hợp các công nghệ AI tiên tiến nhất, mở rộng khả năng của hệ thống vượt ra ngoài các chức năng hiện tại, và khám phá các mô hình tương tác người-máy mới. Mục tiêu là xây dựng một hệ sinh thái tri thức thông minh, có khả năng thích ứng và tiên đoán, phục vụ cho sự phát triển bền vững và đổi mới không ngừng của TRM.

    *   **16.13. Mục tiêu chính (Key Objectives):**
        *   Nghiên cứu và tích hợp các mô hình AI thế hệ mới (e.g., Large Language Models (LLMs) chuyên biệt cho TRM, Generative AI cho việc tạo nội dung/giải pháp).
        *   Khám phá các kiến trúc AI tiên tiến như AI nhận thức (Cognitive AI) để mô phỏng sát hơn quá trình tư duy của con người.
        *   Phát triển khả năng tương tác đa phương thức (Multimodal Interaction) nâng cao, cho phép người dùng và agent tương tác qua giọng nói, hình ảnh, văn bản một cách liền mạch.
        *   Xây dựng các "Digital Twins" của các quy trình hoặc khía cạnh hoạt động của TRM để mô phỏng, phân tích và tối ưu hóa sâu hơn.
        *   Nghiên cứu các mô hình đạo đức AI (AI Ethics) tiên tiến và cơ chế quản trị AI có trách nhiệm, đảm bảo sự phát triển bền vững và tin cậy.
        *   Mở rộng khả năng kết nối và tương tác của TRM-OS với các hệ thống bên ngoài, đối tác tiềm năng hoặc cộng đồng (nếu phù hợp).
        *   Thúc đẩy văn hóa đổi mới liên tục dựa trên dữ liệu và tri thức được quản lý bởi TRM-OS.

    *   **16.14. Các Hướng Nghiên cứu và Phát triển Chính (Key R&D Directions):**
        * **AI Sáng tạo (Generative AI) cho TRM:**
            *   Tự động tạo báo cáo, tóm tắt, đề xuất giải pháp chi tiết.
            *   Hỗ trợ sáng tạo nội dung, ý tưởng mới dựa trên kho tri thức.
        * **AI Nhận thức và Suy luận Phức hợp:**
            *   Nâng cao khả năng suy luận nhân quả, hiểu biết ngữ cảnh sâu.
            *   Phát triển agent có khả năng "hiểu" và "học" như con người.
        * **Tương tác Người-Máy Thế hệ Mới:**
            *   Giao diện tương tác 3D/VR/AR cho việc trực quan hóa ontology và dữ liệu.
            *   Agent có khả năng đối thoại tự nhiên, đồng cảm.
        * **Digital Twin Orchestration:**
            *   Xây dựng và quản lý các bản sao số của các thực thể và quy trình quan trọng.
        * **Explainable & Trustworthy AI at Scale:**
            *   Các kỹ thuật mới để đảm bảo tính minh bạch, công bằng và trách nhiệm của các hệ thống AI phức tạp.
        * **Decentralized AI and Knowledge Sharing (Nghiên cứu):**
            *   Khám phá tiềm năng của blockchain hoặc các công nghệ sổ cái phân tán cho việc chia sẻ tri thức an toàn và minh bạch.

    *   **16.15. Công nghệ Đột phá Tiềm năng (Potential Breakthrough Technologies):**
        * **Quantum AI / Quantum Machine Learning:** (Nghiên cứu dài hạn) Cho các bài toán tối ưu hóa và phân tích cực kỳ phức tạp.
        * **Neuromorphic Computing:** Mô phỏng kiến trúc não bộ để xử lý thông tin hiệu quả hơn.
        * **Advanced Robotics and Embodied AI (Nếu có ứng dụng vật lý):** Agent tương tác với thế giới thực.
        * **Brain-Computer Interfaces (BCI) (Nghiên cứu rất xa):** Cho các hình thức tương tác mới.
        * **Homomorphic Encryption:** Xử lý dữ liệu được mã hóa mà không cần giải mã, tăng cường bảo mật.

    *   **16.16. Tác động Chiến lược và Mở rộng Hệ sinh thái (Strategic Impact & Ecosystem Expansion):**
        *   TRM-OS trở thành một lợi thế cạnh tranh chiến lược cốt lõi, thúc đẩy sự đổi mới và hiệu quả hoạt động vượt trội.
        *   Khả năng tạo ra các mô hình kinh doanh mới hoặc các dịch vụ giá trị gia tăng dựa trên tri thức và AI.
        *   Tiềm năng mở rộng TRM-OS thành một nền tảng, cho phép các bên thứ ba (nếu có) phát triển ứng dụng hoặc tích hợp dịch vụ.
        *   Đóng góp vào sự phát triển của lĩnh vực AI và quản lý tri thức thông qua các nghiên cứu và ứng dụng tiên phong.
        *   Xây dựng một tổ chức học hỏi thực sự, nơi tri thức được chia sẻ, tái sử dụng và phát triển liên tục bởi cả con người và AI.
        *   Đảm bảo sự thích ứng và phát triển bền vững của TRM trong một thế giới thay đổi nhanh chóng.


17. **Đo lường Hiệu quả và Cải tiến Liên tục (Key Performance Indicators - KPIs)**

    Mục tiêu của việc thiết lập và theo dõi KPIs là để đánh giá một cách khách quan mức độ thành công của TRM-OS trong việc hiện thực hóa tầm nhìn và các mục tiêu chiến lược đã đề ra. Quan trọng hơn, KPIs phải phản ánh được giá trị thực tiễn mà TRM-OS mang lại cho hoạt động hàng ngày, khả năng ra quyết định và sự phát triển của TRM – tức là "ontology được áp dụng vào thực tế". Các KPIs này không chỉ là thước đo kỹ thuật mà còn là la bàn định hướng cho các chu trình cải tiến liên tục, đảm bảo TRM-OS luôn phát triển đồng bộ với nhu cầu thực tế và các mục tiêu trong Lộ trình Phát triển.

    Các KPIs được phân loại như sau:

    *   **17.1. KPIs về Chất lượng, Tính Hiện thực và Khả năng Thích ứng của Ontology & Knowledge Base:**
        * **Độ Bao phủ Thực thể và Quy trình Cốt lõi (Core Entity & Process Coverage):**
            *   *Mục tiêu:* >90% các thực thể (`Agent`, `Project`, `Tension`, `WIN`, `KnowledgeDomain`, etc.) và quy trình vận hành chính yếu của TRM được mô hình hóa chính xác và đầy đủ trong ontology.
            *   *Đo lường:* Đánh giá định kỳ (ví dụ: hàng quý) dựa trên checklist các khái niệm/quy trình mục tiêu so với thực tế.
        * **Độ Chính xác và Nhất quán của Ontology (Ontology Accuracy & Consistency):**
            *   *Mục tiêu:* Tỷ lệ các phát biểu (statements, relationships) trong ontology được xác minh là đúng >95%; không có mâu thuẫn logic nội tại.
            *   *Đo lường:* Kiểm tra thủ công ngẫu nhiên; sử dụng các công cụ suy luận (reasoners) để phát hiện mâu thuẫn; phản hồi từ Founder và các agent về tính chính xác.
        * **Độ Sâu và Phong phú của Tri thức (Knowledge Depth & Richness):**
            *   *Mục tiêu:* Gia tăng mật độ kết nối trung bình của ontology (e.g., số lượng mối quan hệ/thuộc tính có ý nghĩa trên mỗi `KnowledgeSnippet` hoặc thực thể quan trọng).
            *   *Đo lường:* Phân tích cấu trúc graph; đánh giá chất lượng của các `KnowledgeSnippet` được liên kết.
        * **Chất lượng và Tính Hành động của `KnowledgeSnippet`:**
            *   *Mục tiêu:* >80% `KnowledgeSnippet` được trích xuất/tạo ra được đánh giá là liên quan, chính xác và cung cấp đủ thông tin để hỗ trợ hành động/quyết định.
            *   *Đo lường:* Số lượt `KnowledgeSnippet` được sử dụng hiệu quả bởi agent/Founder; tỷ lệ snippet được đánh dấu "hữu ích" qua cơ chế phản hồi.
        * **Khả năng Thích ứng của Ontology (Ontology Adaptability):**
            *   *Mục tiêu:* Thời gian trung bình để cập nhật/mở rộng ontology với các khái niệm hoặc cấu trúc dữ liệu mới < X giờ/ngày (tùy độ phức tạp).
            *   *Đo lường:* Theo dõi thời gian từ lúc yêu cầu thay đổi đến khi ontology được cập nhật và xác thực.
        * **Độ Trễ Thông tin (Information Latency):**
            *   *Mục tiêu:* Giảm thiểu độ trễ từ khi một sự kiện thực tế xảy ra đến khi nó được phản ánh chính xác trong ontology (e.g., một `Tension` mới, một `WIN` mới).
            *   *Đo lường:* Thời gian trung bình cập nhật dữ liệu cho các loại sự kiện quan trọng.

    *   **17.2. KPIs về Tác động của TRM-OS lên Vận hành và Ra Quyết định của TRM:**
        * **Hiệu quả Quản lý `Tension`:**
            *   *Mục tiêu:* Giảm Y% thời gian trung bình từ khi `Tension` được ghi nhận đến khi có `ProjectProposal` khả thi; Tăng Z% tỷ lệ `Tension` được giải quyết thành công dẫn đến `Project` hoàn thành.
            *   *Đo lường:* Theo dõi vòng đời của `Tension`; tỷ lệ `Project` được khởi tạo từ `Tension` do AI đề xuất và thành công.
        * **Gia tăng `WIN` và Tác động Tích cực:**
            *   *Mục tiêu:* Số lượng `WIN` được ghi nhận (đặc biệt là các `WIN` được AI hỗ trợ phát hiện/đề xuất) tăng X% mỗi quý; giá trị hoặc tác động ước tính của các `WIN` này.
            *   *Đo lường:* Số lượng `WIN` node; đánh giá định tính và định lượng (nếu có) của từng `WIN`.
        * **Tối ưu hóa `Project` và `Task`:**
            *   *Mục tiêu:* Giảm A% thời gian trung bình hoàn thành các loại `Project` tương tự; Cải thiện B% tỷ lệ thành công của `Project` nhờ thông tin/hỗ trợ từ TRM-OS.
            *   *Đo lường:* So sánh hiệu suất dự án trước/sau TRM-OS; phân tích nguyên nhân thất bại/thành công của dự án liên quan đến việc sử dụng TRM-OS.
        * **Mức độ Tự động hóa và Hỗ trợ Quy trình Thông minh:**
            *   *Mục tiêu:* Tự động hóa >C% các bước lặp lại trong các quy trình mục tiêu (e.g., trích xuất thông tin, phân loại `Tension`, đề xuất `Task`).
            *   *Đo lường:* Phân tích quy trình, xác định số bước được agent thực hiện/hỗ trợ so với tổng số bước.
        * **Chất lượng và Tốc độ Ra Quyết định của Founder:**
            *   *Mục tiêu:* Cải thiện sự tự tin và giảm thời gian cần thiết cho Founder khi ra các quyết định quan trọng dựa trên insight từ TRM-OS.
            *   *Đo lường:* Khảo sát định kỳ Founder; phân tích thời gian ra quyết định cho các tình huống lặp lại.

    *   **17.3. KPIs về Hiệu suất, Độ Tin cậy và Khả năng Học hỏi của Hệ thống và AI Agents:**
        * **Thời gian Phản hồi và Thông lượng của Agent:**
            *   *Mục tiêu:* Thời gian phản hồi trung bình của các agent tương tác (e.g., `QueryAgent`, `InsightAgent`) < S giây; Khả năng xử lý N yêu cầu/phút của các agent xử lý nền (e.g., `IngestionAgent`).
            *   *Đo lường:* Logging và monitoring hiệu suất agent.
        * **Độ Chính xác và Tỷ lệ Lỗi của Agent:**
            *   *Mục tiêu:* Tỷ lệ lỗi nghiêm trọng của agent < E%; Độ chính xác của các tác vụ phân loại/dự đoán của agent (e.g. `TensionClassificationAgent`) > P%.
            *   *Đo lường:* Theo dõi lỗi; đánh giá kết quả đầu ra của agent so với ground truth.
        * **Khả năng Học hỏi và Cải thiện của Agent (Liên kết Giai đoạn 3+):**
            *   *Mục tiêu:* Các agent có khả năng học hỏi (e.g., `OntologyEvolutionAgent`, `WorkflowOptimizationAgent`) cải thiện hiệu suất Z% sau mỗi chu kỳ huấn luyện/tinh chỉnh.
            *   *Đo lường:* Theo dõi sự thay đổi về độ chính xác, hiệu quả của agent theo thời gian.
        * **Mức độ sử dụng Tài nguyên Hệ thống:**
            *   *Mục tiêu:* Duy trì mức sử dụng CPU, memory, storage trong ngưỡng cho phép, đảm bảo tính ổn định và khả năng mở rộng.
            *   *Đo lường:* Giám sát tài nguyên hệ thống (Neo4j, Supabase, Snowflake, servers).
        * **Tính Sẵn sàng và Khả năng Phục hồi của Hệ thống:**
            *   *Mục tiêu:* Uptime > 99.9%; Thời gian phục hồi sau sự cố (RTO) < R giờ.
            *   *Đo lường:* Giám sát uptime; kết quả từ các bài kiểm tra phục hồi (recovery drills).

    *   **17.4. KPIs về Sự Chấp nhận, Mức độ Hài lòng và Giá trị Thực tiễn cho Người dùng (Founder):**
        * **Mức độ Hài lòng của Founder (Founder Satisfaction Score - FSS):**
            *   *Mục tiêu:* Điểm FSS > 8/10 qua các khảo sát định kỳ.
            *   *Đo lường:* Khảo sát chi tiết về các khía cạnh của TRM-OS (tính năng, dễ sử dụng, giá trị mang lại).
        * **Mức độ Tương tác và Sử dụng Hệ thống (User Engagement):**
            *   *Mục tiêu:* Số lượt tương tác có ý nghĩa (truy vấn, tạo `Tension`, sử dụng insight) của Founder với hệ thống đạt M lượt/ngày/tuần.
            *   *Đo lường:* Log tương tác người dùng.
        * **Giá trị Cảm nhận và ROI (Perceived Value & ROI):**
            *   *Mục tiêu:* Founder nhận thấy TRM-OS mang lại giá trị rõ rệt, vượt trội so với chi phí đầu tư và vận hành.
            *   *Đo lường:* Phỏng vấn sâu Founder; phân tích chi phí-lợi ích (nếu có thể định lượng).
        * **Số lượng và Chất lượng Yêu cầu Cải tiến:**
            *   *Mục tiêu:* Ghi nhận và ưu tiên các yêu cầu cải tiến mang tính xây dựng, giúp TRM-OS ngày càng phù hợp hơn.
            *   *Đo lường:* Số lượng yêu cầu; tỷ lệ yêu cầu được đưa vào backlog và triển khai.

    *   **17.5. KPIs về Sự Tiến hóa Tự chủ của Ontology và AI (Liên kết với Lộ trình Giai đoạn 3 & 4):**
        * **Tỷ lệ Tự động Làm giàu Ontology (Automated Ontology Enrichment Rate):**
            *   *Mục tiêu:* X% các khái niệm/mối quan hệ mới trong ontology được đề xuất hoặc tự động tạo ra bởi `OntologyEvolutionAgent` và được phê duyệt.
            *   *Đo lường:* Số lượng thay đổi ontology tự động so với thủ công.
        * **Hiệu quả của Cơ chế Tự giám sát và Tự phục hồi (Self-Monitoring & Healing Effectiveness):**
            *   *Mục tiêu:* Y% các sự cố hệ thống phổ biến được tự động phát hiện và khắc phục mà không cần can thiệp thủ công.
            *   *Đo lường:* Số lượng sự cố được giải quyết tự động; thời gian downtime giảm do tự phục hồi.
        * **Chất lượng Giải thích của AI (XAI Quality Score):**
            *   *Mục tiêu:* Mức độ hiểu và tin tưởng của Founder đối với các giải thích do hệ thống XAI cung cấp đạt Z điểm (theo thang đánh giá).
            *   *Đo lường:* Khảo sát Founder sau khi xem xét các giải thích của AI.
        * **Số lượng "WIN" hoặc Insight Đột phá do AI Tự chủ Đề xuất:**
            *   *Mục tiêu:* Hệ thống tự động đề xuất ít nhất N "WIN" hoặc insight chiến lược có giá trị cao mỗi quý.
            *   *Đo lường:* Số lượng đề xuất được Founder công nhận và triển khai.
        * **Tiến độ Nghiên cứu và Thử nghiệm Công nghệ Mới (R&D Progress - Giai đoạn 4):**
            *   *Mục tiêu:* Hoàn thành K PoC (Proof of Concept) thành công cho các công nghệ đột phá tiềm năng mỗi năm.
            *   *Đo lường:* Số lượng PoC hoàn thành; kết quả đánh giá PoC.

    Các KPIs này sẽ được xem xét và điều chỉnh định kỳ (ví dụ: 6 tháng/1 năm) để đảm bảo chúng luôn phù hợp với giai đoạn phát triển hiện tại của TRM-OS và các mục tiêu chiến lược của TRM. Việc thu thập, phân tích và báo cáo KPIs sẽ được tự động hóa tối đa có thể.

**PHỤ LỤC**

*Mục này sẽ được bổ sung trong quá trình triển khai và vận hành hệ thống. Các phần dự kiến bao gồm:*

**A.1. Bảng thuật ngữ chi tiết (Glossary)**
    *Phần này giải thích các thuật ngữ chuyên môn và các khái niệm đặc thù được sử dụng trong tài liệu TRM-OS. Danh sách này sẽ được mở rộng và cập nhật liên tục.*

    *   **TRM-OS (Total Recall Machine - Operating System):** Hệ thống tổng thể điều khiển bởi AI, được thiết kế cho việc quản lý tri thức, hỗ trợ ra quyết định chiến lược và tối ưu hóa vận hành cho TRM.
    *   **Ontology:** Một đặc tả chính thức, rõ ràng về một nhận thức chung. Trong TRM-OS, đây là cơ sở tri thức có cấu trúc, định nghĩa các thực thể, mối quan hệ và quy tắc.
    *   **AGE (Artificial General Executive):** Agent AI điều phối trung tâm trong TRM-OS, chịu trách nhiệm điều phối các agent khác và đảm bảo các hành động phù hợp với mục tiêu chiến lược.
    *   **Agent (AI Agent):** Một thực thể phần mềm chuyên biệt thực hiện các hành động tự trị để đạt được các mục tiêu cụ thể trong TRM-OS (ví dụ: `DataSensingAgent`, `TensionResolutionAgent`).
    *   **Tension:** Một vấn đề, rủi ro, cơ hội, câu hỏi hoặc sự không nhất quán được nhận diện, đòi hỏi sự chú ý hoặc giải quyết trong TRM.
    *   **WIN (What I Need / What Is Notable):** Một insight, thành tựu, bài học hoặc mẩu thông tin giá trị quan trọng được xác định trong TRM-OS.
    *   **Project (Dự án):** Một tập hợp các nhiệm vụ có kế hoạch, liên quan đến nhau, được thực hiện trong một khoảng thời gian nhất định và trong giới hạn chi phí cũng như các ràng buộc khác, thường nhằm giải quyết một `Tension` hoặc tận dụng một cơ hội.
    *   **KnowledgeSnippet:** Một đơn vị tri thức hoặc thông tin rời rạc, thường được trích xuất từ nhiều nguồn khác nhau, được nhúng và liên kết trong ontology.
    *   **Event (Sự kiện):** Một sự việc hoặc thay đổi trạng thái quan trọng trong TRM-OS hoặc môi trường của nó, được sử dụng để kích hoạt hành động và luồng công việc của agent.
    *   **API Contract:** Một thỏa thuận chính thức định nghĩa cách các AI agent hoặc thành phần hệ thống khác nhau sẽ tương tác, chỉ định định dạng request/response, giao thức và các hành vi mong đợi.
    *   **KPI (Key Performance Indicator - Chỉ số Hiệu suất Chính):** Một giá trị có thể đo lường, cho thấy mức độ hiệu quả của TRM-OS trong việc đạt được các mục tiêu kinh doanh chính.
    *   **Roadmap (Lộ trình Phát triển):** Một kế hoạch phác thảo sự phát triển và tiến hóa trong tương lai của TRM-OS qua các giai đoạn.
    *   **Governance (Quản trị):** Khuôn khổ các quy tắc, thực tiễn và quy trình mà TRM-OS được chỉ đạo và kiểm soát.
    *   **Neo4j Aura:** Công nghệ cơ sở dữ liệu đồ thị được sử dụng để triển khai ontology cốt lõi của TRM-OS.
    *   **Supabase:** Nền tảng cung cấp các chức năng BaaS (Backend as a Service), bao gồm khả năng cơ sở dữ liệu vector cho tìm kiếm ngữ nghĩa và lưu trữ cho TRM-OS.
    *   **Snowflake:** Nền tảng dữ liệu đám mây được sử dụng làm hồ dữ liệu/kho dữ liệu (data lake/warehouse) cho TRM-OS, xử lý lưu trữ và xử lý dữ liệu quy mô lớn.
    *(Các thuật ngữ khác sẽ được bổ sung...)*

**A.2. Sơ đồ Ontology Toàn diện (Comprehensive Ontology Diagrams)**
    *Phần này cung cấp các biểu đồ trực quan hóa cấu trúc, các thành phần chính và mối quan hệ trong TRM-OS Ontology. Các sơ đồ này nhằm mục đích tăng cường sự hiểu biết, hỗ trợ thiết kế và tạo điều kiện giao tiếp giữa các bên liên quan.*

    **Mục tiêu của các sơ đồ:**
    *   Minh họa các thực thể cốt lõi và mối quan hệ giữa chúng.
    *   Thể hiện kiến trúc tổng thể của hệ thống agent và các tương tác chính.
    *   Cung cấp cái nhìn tổng quan về luồng dữ liệu và luồng xử lý chính.

    **Các loại sơ đồ dự kiến (ví dụ):**
    1.  **Sơ đồ Thực thể - Mối quan hệ Chính (Core Entity-Relationship Diagram - ERD):**
        *   Mô tả các loại thực thể trung tâm (ví dụ: `User`, `Project`, `Tension`, `WIN`, `KnowledgeSnippet`, `Agent`, `Resource`) và các mối quan hệ chính giữa chúng (ví dụ: `HAS_PARTICIPANT`, `GENERATES`, `RESOLVES`, `USES_KNOWLEDGE`).
        *   Nên làm nổi bật các thuộc tính quan trọng của mỗi thực thể.
    2.  **Sơ đồ Kiến trúc Agent Tổng quan (High-Level Agent Architecture Diagram):**
        *   Hiển thị các agent chính trong TRM-OS (ví dụ: `AGE`, `DataSensingAgent`, `TensionResolutionAgent`, `KnowledgeManagementAgent`, `LearningAndOptimizationAgent`) và các kênh giao tiếp chính (ví dụ: qua Event Bus, API calls).
        *   Có thể bao gồm các hệ thống bên ngoài mà các agent tương tác.
    3.  **Sơ đồ Phân cấp Ontology (Ontology Hierarchy/Taxonomy Diagram):**
        *   Nếu có các mối quan hệ phân cấp rõ ràng (ví dụ: `is-a`, `part-of`) giữa các khái niệm, sơ đồ này sẽ trực quan hóa chúng.
        *   Ví dụ: các loại `Tension` khác nhau, các loại `Resource`.
    4.  **Sơ đồ Luồng Dữ liệu Tổng quan (High-Level Data Flow Diagram - DFD):**
        *   Minh họa cách dữ liệu được thu thập, xử lý, lưu trữ và sử dụng trong toàn bộ hệ thống TRM-OS.
        *   Tập trung vào các luồng chính liên quan đến việc tạo `Tension`, xử lý `WIN`, cập nhật `KnowledgeSnippet`.

    **Công cụ và Định dạng Đề xuất:**
    *   **Công cụ tạo sơ đồ:** Lucidchart, draw.io (diagrams.net), Microsoft Visio, PlantUML (cho sơ đồ dạng text-to-image), hoặc các công cụ trực quan hóa đồ thị chuyên dụng.
    *   **Định dạng nhúng:** Ưu tiên các định dạng vector có thể mở rộng (ví dụ: SVG) hoặc hình ảnh chất lượng cao (ví dụ: PNG) được nhúng trực tiếp vào tài liệu hoặc liên kết đến.
    *   Các sơ đồ nên được đánh số phiên bản và có ngày cập nhật cuối cùng.

    **Lưu ý:**
    *   Các sơ đồ này nên được duy trì và cập nhật song song với sự phát triển của ontology và hệ thống TRM-OS để đảm bảo tính chính xác và phù hợp.
    *(Các sơ đồ cụ thể sẽ được tạo và nhúng ở đây khi có sẵn)*

**A.3. Sơ đồ Luồng Dữ liệu Chi tiết (Detailed Data Flow Diagrams - DFDs)**
    *Phần này mô tả chi tiết cách dữ liệu di chuyển và được biến đổi trong toàn bộ hệ thống TRM-OS. Các DFDs cung cấp một cái nhìn rõ ràng về các quy trình xử lý dữ liệu, kho dữ liệu và các tương tác dữ liệu giữa các thành phần hệ thống, đặc biệt là các AI agent.*

    **Mục tiêu của DFDs chi tiết:**
    *   Hiểu rõ cách dữ liệu được thu thập, xử lý, lưu trữ và truyền tải giữa các thành phần cốt lõi của TRM-OS.
    *   Xác định các điểm tích hợp dữ liệu quan trọng và các phép biến đổi dữ liệu chính.
    *   Hỗ trợ việc thiết kế cơ sở dữ liệu, phát triển agent và đảm bảo tính toàn vẹn của dữ liệu.

    **Các cấp độ DFDs dự kiến:**
    1.  **Sơ đồ Ngữ cảnh (Context Diagram - Level 0 DFD):**
        *   Thể hiện toàn bộ hệ thống TRM-OS như một quy trình duy nhất.
        *   Hiển thị các thực thể bên ngoài chính (nguồn và đích dữ liệu) tương tác với hệ thống.
        *   Minh họa các luồng dữ liệu chính vào và ra khỏi hệ thống.
    2.  **DFD Cấp 1 (Level 1 DFDs):**
        *   Phân rã quy trình trong Sơ đồ Ngữ cảnh thành các quy trình con chính của TRM-OS.
        *   Ví dụ: "Thu thập Dữ liệu", "Xử lý và Nhúng Tri thức", "Phân tích và Giải quyết Tension", "Giám sát và Tối ưu hóa Hệ thống".
        *   Hiển thị các kho dữ liệu chính (ví dụ: `Staging Area`, `Data Lake/Warehouse`, `Neo4j Aura DB`, `Supabase Vector DB`) và các luồng dữ liệu giữa các quy trình này và kho dữ liệu.
    3.  **DFD Cấp 2+ (Level 2+ DFDs - nếu cần):**
        *   Phân rã thêm các quy trình phức tạp từ DFD Cấp 1 để cung cấp chi tiết hơn.
        *   Ví dụ: Chi tiết hóa quy trình "Xử lý và Nhúng Tri thức" thành các bước như "Trích xuất Thực thể", "Liên kết Tri thức", "Vector hóa Nội dung".

    **Các yếu tố cần thể hiện trong DFDs:**
    *   **Quy trình (Processes):** Các hoạt động hoặc chức năng biến đổi dữ liệu.
    *   **Luồng dữ liệu (Data Flows):** Đường đi của dữ liệu giữa các quy trình, kho dữ liệu và thực thể bên ngoài.
    *   **Kho dữ liệu (Data Stores):** Nơi dữ liệu được lưu trữ (ví dụ: bảng cơ sở dữ liệu, file, bộ nhớ cache).
    *   **Thực thể bên ngoài (External Entities):** Nguồn hoặc đích của dữ liệu bên ngoài hệ thống (ví dụ: người dùng, hệ thống khác).

    **Ký hiệu và Công cụ Đề xuất:**
    *   **Ký hiệu (Notation):** Gane & Sarson hoặc Yourdon & DeMarco là các ký hiệu DFD phổ biến.
    *   **Công cụ tạo sơ đồ:** Tương tự như A.2 (Lucidchart, draw.io, Microsoft Visio, etc.).
    *   Đảm bảo tính nhất quán trong việc sử dụng ký hiệu và đặt tên.

    **Lưu ý:**
    *   DFDs nên được phát triển từ cấp độ tổng quan đến chi tiết.
    *   Cần được cập nhật thường xuyên để phản ánh những thay đổi trong thiết kế hệ thống.
    *   Tập trung vào luồng dữ liệu, không phải luồng kiểm soát (control flow).
    *(Các DFDs cụ thể sẽ được tạo và nhúng ở đây khi có sẵn)*

**A.4. Sequence Diagrams cho các Tương tác Agent Phức tạp**
    *Phần này cung cấp các sơ đồ trình tự (sequence diagrams) để minh họa chi tiết các tương tác động giữa các AI agent trong các kịch bản hoạt động quan trọng hoặc phức tạp của TRM-OS. Các sơ đồ này giúp làm rõ luồng thông điệp, thứ tự thực hiện và sự phối hợp giữa các agent.*

    **Mục tiêu của Sequence Diagrams:**
    *   Trực quan hóa luồng thông điệp (message flow) theo thời gian giữa các agent và các thành phần hệ thống khác.
    *   Hiểu rõ cách các agent hợp tác để hoàn thành một nhiệm vụ hoặc xử lý một sự kiện cụ thể.
    *   Xác định các điểm nghẽn tiềm ẩn, các vấn đề về đồng bộ hóa hoặc các lỗi logic trong tương tác.
    *   Hỗ trợ việc thiết kế API, phát triển agent và gỡ lỗi hệ thống.

    **Các Kịch bản Quan trọng cần Minh họa (ví dụ):**
    1.  **Xử lý một `Tension` mới được tạo:**
        *   Từ khi `DataSensingAgent` phát hiện và tạo `Tension`, đến khi `AGE` điều phối, các agent liên quan (ví dụ: `KnowledgeManagementAgent`, `TensionResolutionAgent`) phân tích, đề xuất giải pháp, và cập nhật trạng thái.
    2.  **Tạo và Nhúng một `KnowledgeSnippet` mới:**
        *   Luồng từ việc thu thập thông tin, xử lý bởi `KnowledgeManagementAgent`, nhúng vector (tương tác với Supabase), lưu trữ trong Neo4j, và thông báo cho các agent liên quan.
    3.  **Một người dùng truy vấn hệ thống:**
        *   Tương tác của `UserInterfaceAgent` (hoặc tương đương) với `QueryProcessingAgent`, `KnowledgeManagementAgent` để lấy và trình bày thông tin.
    4.  **Luồng Tự học và Tối ưu hóa của `LearningAndOptimizationAgent`:**
        *   Cách agent này thu thập dữ liệu hiệu suất, phân tích, đề xuất thay đổi (ví dụ: cho ontology, cho quy trình của agent khác) và cách các thay đổi này được xem xét/áp dụng.
    5.  **Xử lý Xung đột Tài nguyên (ví dụ từ Mục 10.5.9):**
        *   Minh họa cụ thể các bước tương tác giữa các agent để phát hiện, đánh giá và giải quyết xung đột tài nguyên.

    **Các Yếu tố cần Thể hiện trong Sequence Diagrams:**
    *   **Lifelines (Đường đời):** Đại diện cho các agent hoặc thành phần tham gia vào tương tác.
    *   **Messages (Thông điệp):** Các mũi tên chỉ sự giao tiếp giữa các lifelines (ví dụ: gọi hàm, gửi sự kiện, request/response API).
        *   Nên ghi rõ tên thông điệp và các tham số quan trọng.
        *   Phân biệt thông điệp đồng bộ và bất đồng bộ.
    *   **Activations (Kích hoạt):** Các hình chữ nhật trên lifelines cho biết khoảng thời gian một agent đang thực hiện một hành động.
    *   **Combined Fragments (Mảnh kết hợp):** Để biểu diễn các cấu trúc điều khiển như vòng lặp (loop), điều kiện (alt, opt), xử lý song song (par).
    *   **Interaction Use (Sử dụng lại tương tác):** Để tham chiếu đến các sequence diagram khác đã được định nghĩa.

    **Công cụ và Định dạng Đề xuất:**
    *   **Công cụ tạo sơ đồ:** PlantUML (rất mạnh cho sequence diagrams dạng text-to-image), Lucidchart, draw.io, StarUML, Visual Paradigm.
    *   **Định dạng nhúng:** SVG hoặc PNG chất lượng cao.

    **Lưu ý:**
    *   Mỗi sequence diagram nên tập trung vào một kịch bản cụ thể để tránh quá phức tạp.
    *   Cần nhất quán với các định nghĩa API (A.8) và Event (13.3).
    *   Cập nhật khi các kịch bản tương tác hoặc thiết kế agent thay đổi.
    *(Các sequence diagrams cụ thể sẽ được tạo và nhúng ở đây khi có sẵn)*

**A.5. Ví dụ Truy vấn Cypher Nâng cao**
    *Phần này cung cấp một tập hợp các ví dụ truy vấn Cypher nâng cao, được thiết kế để minh họa cách khai thác tri thức và thực hiện các phân tích phức tạp trên TRM-OS Ontology được lưu trữ trong Neo4j. Các ví dụ này phục vụ như một tài liệu tham khảo cho các nhà phát triển, nhà phân tích dữ liệu và quản trị viên ontology.*

    **Mục tiêu của các ví dụ truy vấn:**
    *   Minh họa các kỹ thuật truy vấn Cypher mạnh mẽ để khám phá các mối quan hệ và mẫu hình trong dữ liệu.
    *   Cung cấp các giải pháp mẫu cho các câu hỏi nghiệp vụ hoặc các tác vụ phân tích phổ biến.
    *   Giúp người dùng làm quen với cấu trúc của ontology và cách truy vấn nó một cách hiệu quả.
    *   Chia sẻ các thực hành tốt nhất trong việc viết truy vấn Cypher tối ưu và dễ hiểu.

    **Các loại truy vấn cần minh họa (ví dụ):**
    1.  **Truy vấn Tìm đường (Pathfinding Queries):**
        *   Tìm đường đi ngắn nhất hoặc tất cả các đường đi giữa hai nút cụ thể (ví dụ: tìm tất cả các `Project` liên quan đến một `User` cụ thể thông qua các `Tension` và `WIN`).
        *   Xác định các mối quan hệ gián tiếp phức tạp.
    2.  **Truy vấn Khớp mẫu (Pattern Matching Queries):**
        *   Tìm các cấu trúc hoặc mẫu hình cụ thể trong đồ thị (ví dụ: tìm các `Tension` chưa được giải quyết có độ ưu tiên cao và liên quan đến một `Resource` quan trọng đang cạn kiệt).
        *   Phát hiện các cộng đồng hoặc cụm các nút liên quan chặt chẽ.
    3.  **Truy vấn Tổng hợp và Thống kê (Aggregation and Statistical Queries):**
        *   Tính toán các số liệu thống kê trên đồ thị (ví dụ: số lượng `WIN` được tạo bởi mỗi `Agent` trong một khoảng thời gian, phân phối các loại `Tension`).
        *   Sử dụng các hàm tổng hợp như `COUNT`, `SUM`, `AVG`, `COLLECT`.
    4.  **Truy vấn Đề xuất (Recommendation-style Queries):**
        *   Đề xuất các `KnowledgeSnippet` liên quan cho một `Tension` cụ thể dựa trên các kết nối trong quá khứ hoặc sự tương đồng về nội dung.
        *   Gợi ý các `User` có chuyên môn liên quan đến một `Project`.
    5.  **Truy vấn Cập nhật Đồ thị Phức tạp (Complex Graph Update Queries - sử dụng cẩn thận):**
        *   Ví dụ về cách tạo các mối quan hệ mới dựa trên các điều kiện phức tạp hoặc cập nhật thuộc tính của nhiều nút/mối quan hệ cùng lúc (ví dụ: đánh dấu một loạt `Tension` là `RESOLVED` khi một `Project` hoàn thành).
    6.  **Truy vấn sử dụng APOC Procedures (nếu có):**
        *   Minh họa cách sử dụng các thủ tục mở rộng từ thư viện APOC của Neo4j để thực hiện các tác vụ nâng cao (ví dụ: làm việc với dữ liệu JSON, tính toán đồ thị, v.v.).

    **Cấu trúc cho mỗi ví dụ truy vấn:**
    *   **Mục đích/Câu hỏi nghiệp vụ:** Mô tả rõ ràng truy vấn này giải quyết vấn đề gì hoặc trả lời câu hỏi nào.
    *   **Truy vấn Cypher:** Mã Cypher đầy đủ, được định dạng rõ ràng.
    *   **Giải thích:** Phân tích chi tiết từng phần của truy vấn, giải thích cú pháp và logic.
    *   **Kết quả mẫu (tùy chọn):** Một ví dụ về kết quả mà truy vấn có thể trả về (có thể ở dạng bảng hoặc mô tả).
    *   **Lưu ý/Tối ưu hóa (nếu có):** Bất kỳ cân nhắc đặc biệt nào về hiệu suất hoặc các biến thể của truy vấn.

    **Lưu ý:**
    *   Các truy vấn nên được kiểm thử kỹ lưỡng trên một tập dữ liệu mẫu của ontology.
    *   Khuyến khích sử dụng tham số (`$param`) trong truy vấn để tăng tính tái sử dụng.
    *   Cập nhật các ví dụ khi ontology phát triển hoặc khi các mẫu truy vấn mới hữu ích được phát hiện.
    *(Các ví dụ truy vấn Cypher cụ thể sẽ được bổ sung ở đây)*

**A.6. Chiến lược Xử lý Lỗi và Xác thực Dữ liệu chi tiết**
    *Phần này phác thảo các chiến lược và nguyên tắc cốt lõi cho việc xử lý lỗi và xác thực dữ liệu trong toàn bộ hệ thống TRM-OS. Một hệ thống mạnh mẽ đòi hỏi các cơ chế toàn diện để đảm bảo tính toàn vẹn, nhất quán và đáng tin cậy của dữ liệu, cũng như khả năng phục hồi khi có lỗi xảy ra.*

    **Mục tiêu của Chiến lược:**
    *   Đảm bảo chất lượng và tính nhất quán của dữ liệu đầu vào và dữ liệu được lưu trữ trong ontology.
    *   Phát hiện sớm và xử lý hiệu quả các lỗi dữ liệu và lỗi vận hành.
    *   Giảm thiểu tác động của lỗi đến người dùng và các quy trình hệ thống.
    *   Cung cấp thông tin chẩn đoán đầy đủ để gỡ lỗi và cải thiện hệ thống.

    **Phạm vi Áp dụng:**
    *   **Thu thập Dữ liệu (Data Ingestion):** Xác thực dữ liệu từ các nguồn bên ngoài trước khi đưa vào hệ thống.
    *   **Xử lý Dữ liệu bởi Agent:** Đảm bảo các agent xử lý dữ liệu một cách chính xác và có khả năng xử lý các tình huống ngoại lệ.
    *   **Tương tác API:** Xác thực request và response trong giao tiếp giữa các agent (tham chiếu A.8) và với các hệ thống bên ngoài.
    *   **Lưu trữ Dữ liệu:** Đảm bảo tính toàn vẹn của dữ liệu trong Neo4j, Supabase, Snowflake, và các kho lưu trữ khác.
    *   **Luồng Sự kiện (Event Streams):** Xử lý lỗi trong quá trình sản xuất và tiêu thụ sự kiện (tham chiếu 13.3.2).

    **Các Lĩnh vực Chính cho Xác thực Dữ liệu:**
    1.  **Xác thực Schema (Schema Validation):**
        *   Kiểm tra kiểu dữ liệu, định dạng, các trường bắt buộc, độ dài cho phép.
        *   Sử dụng JSON Schema cho payload sự kiện và API, các ràng buộc của cơ sở dữ liệu.
    2.  **Kiểm tra Tính toàn vẹn Tham chiếu (Referential Integrity):**
        *   Đảm bảo các mối quan hệ trong đồ thị (Neo4j) và các khóa ngoại (nếu có trong các DB khác) là hợp lệ.
    3.  **Xác thực Quy tắc Nghiệp vụ (Business Rule Validation):**
        *   Áp dụng các quy tắc cụ thể của miền TRM (ví dụ: một `Project` phải có ít nhất một `User` là người quản lý, `Tension` không thể được đóng nếu chưa có `WIN` liên quan).
    4.  **Kiểm tra Phạm vi và Giá trị (Range and Value Checks):**
        *   Đảm bảo các giá trị số nằm trong phạm vi cho phép, các giá trị enum là hợp lệ.
    5.  **Kiểm tra Tính Duy nhất (Uniqueness Checks):**
        *   Đảm bảo các định danh (ID) hoặc các tổ hợp thuộc tính quan trọng là duy nhất khi cần thiết.
    6.  **Kiểm tra Tính nhất quán (Consistency Checks):**
        *   Đảm bảo dữ liệu nhất quán giữa các phần khác nhau của hệ thống hoặc qua thời gian.

    **Các Kỹ thuật Xử lý Lỗi Chính:**
    1.  **Ghi log Chi tiết (Comprehensive Logging):**
        *   Sử dụng các cấp độ log (DEBUG, INFO, WARN, ERROR, CRITICAL).
        *   Ghi log có cấu trúc (ví dụ: JSON) để dễ dàng phân tích và truy vấn.
        *   Bao gồm context ID (ví dụ: trace ID, request ID) để theo dõi luồng xử lý.
    2.  **Cơ chế Thông báo và Cảnh báo (Alerting and Notification):**
        *   Thiết lập cảnh báo tự động cho các lỗi nghiêm trọng hoặc các ngưỡng bất thường (ví dụ: số lượng lỗi tăng đột biến).
        *   Thông báo cho đội ngũ vận hành qua email, Slack, PagerDuty, etc.
    3.  **Cơ chế Thử lại (Retry Mechanisms):**
        *   Áp dụng cho các lỗi tạm thời (ví dụ: lỗi mạng, dịch vụ tạm thời không khả dụng).
        *   Sử dụng chiến lược backoff (ví dụ: exponential backoff) để tránh làm quá tải hệ thống.
    4.  **Hàng đợi Thông điệp Chết (Dead-Letter Queues - DLQs):**
        *   Đối với các sự kiện hoặc thông điệp không thể xử lý sau nhiều lần thử lại, chuyển chúng vào DLQ để phân tích và xử lý thủ công sau này.
    5.  **Xử lý Ngoại lệ Tường minh (Explicit Exception Handling):**
        *   Sử dụng các khối try-catch (hoặc tương đương) trong mã của agent để bắt và xử lý các lỗi cụ thể một cách phù hợp.
    6.  **Giao dịch Bù trừ (Compensating Transactions):**
        *   Trong các quy trình gồm nhiều bước, nếu một bước thất bại, thực hiện các hành động để hoàn tác các bước đã thành công trước đó nhằm duy trì tính nhất quán.
    7.  **Thông điệp Lỗi Thân thiện với Người dùng (User-Friendly Error Messages):**
        *   Khi lỗi ảnh hưởng đến người dùng, cung cấp thông báo rõ ràng, dễ hiểu và có hướng dẫn (nếu có thể).

    **Công cụ và Kỹ thuật Hỗ trợ:**
    *   **Thư viện Xác thực:** Ví dụ: Cerberus, Pydantic (Python), Joi (Node.js).
    *   **Hệ thống Giám sát và Ghi log Tập trung:** Prometheus, Grafana, ELK Stack (Elasticsearch, Logstash, Kibana), Splunk.
    *   **Công cụ Quản lý Hàng đợi Thông điệp:** RabbitMQ, Kafka (có hỗ trợ DLQ).

    **Tài liệu hóa và Đánh giá:**
    *   Tất cả các quy tắc xác thực và mã lỗi tiềm năng nên được tài liệu hóa rõ ràng.
    *   Chiến lược xử lý lỗi và xác thực dữ liệu cần được xem xét và cập nhật định kỳ dựa trên kinh nghiệm vận hành và các yêu cầu mới.
    *(Các quy tắc và cơ chế cụ thể hơn sẽ được định nghĩa và tài liệu hóa trong quá trình thiết kế và triển khai chi tiết từng thành phần)*

**A.7. Chi tiết Ánh xạ Schema từ Nguồn Dữ liệu (Detailed Schema Mapping from Data Sources)**
    *Phần này cung cấp tài liệu chi tiết về cách dữ liệu từ các nguồn bên ngoài (ví dụ: CRM, ERP, cơ sở dữ liệu hiện có, file logs, API bên thứ ba) được ánh xạ vào các nút (nodes), thuộc tính (properties), và mối quan hệ (relationships) trong TRM-OS Ontology. Việc ánh xạ schema rõ ràng là rất quan trọng để đảm bảo dữ liệu được tích hợp một cách chính xác và nhất quán.*

    **Mục tiêu của Tài liệu Ánh xạ Schema:**
    *   Cung cấp một bản ghi rõ ràng và chính xác về cách dữ liệu nguồn được chuyển đổi và tải vào ontology.
    *   Hỗ trợ quá trình thiết kế và triển khai các pipeline ETL (Extract, Transform, Load) hoặc ELT.
    *   Tạo điều kiện cho việc gỡ lỗi các vấn đề liên quan đến tích hợp dữ liệu.
    *   Đảm bảo sự hiểu biết chung giữa các nhà phát triển, nhà phân tích dữ liệu và quản trị viên ontology về nguồn gốc và ý nghĩa của dữ liệu trong ontology.

    **Thông tin cần có cho mỗi Ánh xạ Nguồn Dữ liệu:**
    1.  **Thông tin Nguồn Dữ liệu:**
        *   Tên nguồn dữ liệu (ví dụ: Salesforce CRM, SAP ERP, Bảng `UserActivityLog`).
        *   Loại nguồn (ví dụ: Cơ sở dữ liệu quan hệ, API, File CSV, Message Queue).
        *   Mô tả ngắn gọn về dữ liệu chứa trong nguồn.
        *   Tần suất cập nhật hoặc phương thức truy cập dữ liệu nguồn.
    2.  **Bảng Ánh xạ Chi tiết:**
        *   Đối với mỗi thực thể hoặc loại dữ liệu từ nguồn:
            * **Trường Dữ liệu Nguồn:** Tên trường trong hệ thống nguồn.
            * **Kiểu Dữ liệu Nguồn:** Kiểu dữ liệu của trường nguồn.
            * **Mô tả Ngắn gọn (Nguồn):** Ý nghĩa của trường dữ liệu nguồn.
            * **Node Đích trong Ontology:** Tên loại nút (label) trong Neo4j mà dữ liệu này sẽ được ánh xạ tới (ví dụ: `User`, `Project`, `Document`).
            * **Thuộc tính Đích trong Ontology:** Tên thuộc tính trên nút đích (ví dụ: `userId`, `projectName`, `documentTitle`).
            * **Kiểu Dữ liệu Đích:** Kiểu dữ liệu của thuộc tính đích trong ontology.
            * **Quy tắc Biến đổi (Transformation Rules):** Bất kỳ logic biến đổi nào được áp dụng (ví dụ: chuyển đổi định dạng ngày tháng, chuẩn hóa giá trị text, tính toán giá trị mới từ nhiều trường nguồn, ánh xạ giá trị enum).
            * **Xử lý Giá trị Rỗng/Null:** Cách các giá trị rỗng hoặc thiếu từ nguồn được xử lý.
            * **Mối quan hệ được Tạo/Cập nhật:** Nếu dữ liệu nguồn được sử dụng để tạo hoặc cập nhật các mối quan hệ, mô tả rõ các mối quan hệ đó (ví dụ: `(User)-[:PARTICIPATES_IN]->(Project)`).
    3.  **Sơ đồ Ánh xạ (Tùy chọn nhưng khuyến khích):**
        *   Một biểu đồ trực quan (ví dụ: sử dụng các công cụ ETL hoặc công cụ vẽ sơ đồ) thể hiện luồng ánh xạ từ các trường nguồn đến các thực thể và thuộc tính đích.

    **Quy trình Tạo và Duy trì Ánh xạ Schema:**
    *   **Phân tích Nguồn:** Hiểu rõ cấu trúc và ngữ nghĩa của dữ liệu nguồn.
    *   **Thiết kế Ánh xạ:** Xác định cách dữ liệu nguồn phù hợp nhất với mô hình ontology hiện tại.
    *   **Tài liệu hóa:** Ghi lại chi tiết các quyết định ánh xạ.
    *   **Triển khai:** Xây dựng các script hoặc quy trình ETL/ELT dựa trên tài liệu ánh xạ.
    *   **Kiểm thử:** Xác minh rằng dữ liệu được ánh xạ chính xác.
    *   **Đánh giá và Cập nhật:** Khi nguồn dữ liệu thay đổi hoặc ontology phát triển, tài liệu ánh xạ phải được xem xét và cập nhật tương ứng.

    **Ví dụ về các mục cần ánh xạ:**
    *   Thông tin người dùng từ hệ thống quản lý danh tính (IAM) sang nút `User`.
    *   Dữ liệu dự án từ công cụ quản lý dự án sang nút `Project` và các mối quan hệ liên quan.
    *   Nội dung tài liệu từ hệ thống quản lý tài liệu (DMS) sang nút `KnowledgeSnippet` hoặc `Document`.
    *   Log tương tác người dùng từ ứng dụng web sang các nút sự kiện hoặc thuộc tính hoạt động.

    **Lưu ý:**
    *   Tài liệu ánh xạ schema nên được coi là một phần quan trọng của tài liệu hệ thống và được quản lý phiên bản.
    *   Sự rõ ràng và chi tiết trong tài liệu này sẽ giúp giảm thiểu lỗi và tăng tốc độ phát triển trong tương lai.
    *(Chi tiết ánh xạ cho từng nguồn dữ liệu cụ thể sẽ được bổ sung ở đây khi các nguồn được tích hợp)*

**A.8. Đặc tả API Contracts giữa các Agent**
    *Phần này mô tả các nguyên tắc và cấu trúc chung cho việc định nghĩa API contracts cho giao tiếp giữa các AI agent trong TRM-OS. Mục tiêu là đảm bảo tính nhất quán, dễ hiểu, dễ bảo trì và khả năng mở rộng. Các contracts này sẽ bổ sung cho cơ chế giao tiếp dựa trên sự kiện đã được mô tả trong Mục 13.3.*

    *   **A.8.1. Nguyên tắc Thiết kế Chung**
        * **Giao tiếp không đồng bộ (Asynchronous Communication):** Ưu tiên sử dụng hàng đợi tin nhắn (Message Queues như RabbitMQ, Kafka) hoặc các cơ chế pub/sub tương tự cho hầu hết các tương tác giữa agent để tăng khả năng phục hồi và giảm sự phụ thuộc trực tiếp. Điều này phù hợp với kiến trúc hướng sự kiện của TRM-OS.
        * **Giao tiếp đồng bộ (Synchronous Communication):** Trong trường hợp cần thiết phải có phản hồi ngay lập tức (ví dụ: truy vấn dữ liệu quan trọng cho một quyết định tức thời), có thể sử dụng RESTful API hoặc gRPC. Tuy nhiên, cần cân nhắc kỹ lưỡng để tránh tạo ra các điểm nghẽn cổ chai.
        * **Định dạng Dữ liệu (Data Format):** JSON là định dạng chuẩn cho payload của message và request/response API do tính phổ biến và dễ tích hợp.
        * **Tính bất biến (Idempotency):** Các agent xử lý request phải được thiết kế để xử lý các request trùng lặp một cách an toàn (idempotent operations), đặc biệt quan trọng trong môi trường phân tán và không đồng bộ.
        * **Bảo mật (Security):**
            *   Xác thực (Authentication): Mỗi agent phải xác thực danh tính của agent gọi đến.
            *   Ủy quyền (Authorization): Kiểm soát quyền truy cập tài nguyên và thực thi hành động dựa trên vai trò và quyền hạn của agent.
            *   Mã hóa (Encryption): Dữ liệu nhạy cảm phải được mã hóa cả khi truyền (in transit) và khi lưu trữ (at rest).

    *   **A.8.2. Cấu trúc Message/API Request-Response**
        Mỗi message hoặc API call nên bao gồm các thành phần sau:
        * **Header:**
            * ` messageId` (UUID): Định danh duy nhất cho mỗi message/request.
            * ` correlationId` (UUID): Định danh để theo dõi một chuỗi các message/request liên quan trong một workflow.
            * ` sourceAgentId`: Định danh của agent gửi.
            * ` targetAgentId` (nếu có): Định danh của agent nhận (cho direct messaging).
            * ` timestamp` (ISO 8601): Thời điểm message/request được tạo.
            * ` version`: Phiên bản của contract/schema.
            * ` eventType` (cho message queue): Tên sự kiện, tuân theo quy ước đặt tên ở Mục 13.3.3.
        * **Payload:**
            *   Nội dung chính của message/request, được định nghĩa bằng JSON Schema.
            *   Schema phải được quản lý và phiên bản hóa cẩn thận.
        * **Response (cho synchronous API):**
            *   Mã trạng thái HTTP (ví dụ: 200 OK, 201 Created, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 500 Internal Server Error).
            *   Payload chứa dữ liệu trả về hoặc thông tin lỗi.

    *   **A.8.3. Quản lý Phiên bản (Versioning)**
        *   API contracts và message schemas phải được phiên bản hóa.
        *   Có thể sử dụng versioning trong URL (cho REST API, ví dụ: `/v1/resource`) hoặc trong header.
        *   Đảm bảo khả năng tương thích ngược (backward compatibility) khi có thể, hoặc có kế hoạch chuyển đổi rõ ràng cho các breaking changes.

    *   **A.8.4. Xử lý Lỗi (Error Handling)**
        *   Sử dụng mã lỗi chuẩn (ví dụ: HTTP status codes cho REST).
        *   Cung cấp thông điệp lỗi rõ ràng, có cấu trúc (JSON) bao gồm:
            * ` errorCode`: Mã lỗi nội bộ, duy nhất.
            * ` errorMessage`: Mô tả lỗi cho developer.
            * ` errorDetails` (optional): Thông tin chi tiết hơn về lỗi.
        *   Sử dụng Dead-Letter Queues (DLQs) cho các message không thể xử lý được sau một số lần thử lại nhất định (như đã đề cập trong Mục 13.3.2).

    *   **A.8.5. Ví dụ Contracts (Illustrative Examples)**
        * **A.8.5.1. KnowledgeSnippet Retrieval (Agent-to-Agent REST API)**
            * **Kịch bản:** `TensionResolutionAgent` cần thông tin chi tiết về một `KnowledgeSnippet` từ `KnowledgeManagementAgent` (giả sử đây là một tương tác đồng bộ cần thiết).
            * **Endpoint (RESTful):** `GET /api/v1/knowledge-snippets/{snippetId}`
            * **Agent gọi:** `TensionResolutionAgent`
            * **Agent xử lý:** `KnowledgeManagementAgent`
            * **Request Header:**
                ```yamljson
                {
                  "messageId": "uuid-for-request",
                  "correlationId": "uuid-for-workflow",
                  "sourceAgentId": "TensionResolutionAgent_instance_001",
                  "targetAgentId": "KnowledgeManagementAgent_instance_001",
                  "timestamp": "2025-06-11T10:00:00Z",
                  "version": "1.0"
                }
                ```yaml
            * **Request Parameters:**
                * ` snippetId` (Path parameter): ID của `KnowledgeSnippet` cần truy vấn.
            * **Response (200 OK):**
                ```yamljson
                {
                  "header": {
                    "messageId": "uuid-for-response",
                    "correlationId": "uuid-for-workflow", 
                    "sourceAgentId": "KnowledgeManagementAgent_instance_001",
                    "timestamp": "2025-06-11T10:00:05Z",
                    "version": "1.0"
                  },
                  "payload": {
                    "id": "snippetId123",
                    "title": "Example Snippet Title",
                    "content": "Detailed content of the knowledge snippet...",
                    "source": "Source Document XYZ",
                    "type": "BestPractice",
                    "tags": ["ontology", "development", "neo4j"],
                    "relatedEntities": ["ProjectAlpha", "TensionBeta"],
                    "createdAt": "2025-01-15T09:30:00Z",
                    "updatedAt": "2025-01-16T14:45:00Z"
                  }
                }
                ```yaml
            * **Response (404 Not Found):**
                ```yamljson
                {
                  "header": {
                    "messageId": "uuid-for-response-error",
                    "correlationId": "uuid-for-workflow",
                    "sourceAgentId": "KnowledgeManagementAgent_instance_001",
                    "timestamp": "2025-06-11T10:00:06Z",
                    "version": "1.0"
                  },
                  "error": {
                    "errorCode": "KM_ERR_001",
                    "errorMessage": "KnowledgeSnippet not found.",
                    "errorDetails": "No KnowledgeSnippet found with ID: {snippetId}"
                  }
                }
                ```yaml

        * **A.8.5.2 Event: `NEW_RAW_DATA_POINT_CREATED` (Message Queue)**
            * **Mô tả:** Sự kiện được phát hành bởi `DataSensingAgent` khi một điểm dữ liệu thô mới được thu thập và sẵn sàng cho việc trích xuất tri thức.
            * **Kênh (Channel):** Message Queue (ví dụ: RabbitMQ, Kafka)
            * **Topic/Routing Key (ví dụ):** `trm.event.rawdata.created`
            * **Publisher:** `DataSensingAgent`
            * **Consumer dự kiến:** `KnowledgeExtractionAgent`
            * **Cấu trúc Thông điệp (Message Structure):**
                * **Header (theo chuẩn A.8.2):**
                    ```yamljson
                    {
                      "messageId": "uuid-for-event-new-raw-data",
                      "eventType": "NEW_RAW_DATA_POINT_CREATED",
                      "sourceAgentId": "DataSensingAgent_instance_001",
                      "timestamp": "2025-06-12T09:00:00Z",
                      "version": "1.0",
                      "correlationId": "uuid-for-original-trigger-if-any"
                    }
                    ```yaml
                * **Payload:**
                    ```yamljson
                    {
                      "rawDataPointId": "rdp_xyz_789",
                      "sourceSystem": "FounderInput_ManualForm",
                      "dataType": "text/plain",
                      "dataLocation": "s3://trm-raw-data/uploads/rdp_xyz_789.txt",
                      "collectionTimestamp": "2025-06-12T08:55:00Z",
                      "metadata": {
                        "originalFileName": "meeting_notes_project_phoenix.txt",
                        "submitterAgentId": "Founder_TRM"
                      }
                    }
                    ```yaml

        * **A.8.5.3 Event: `KNOWLEDGE_SNIPPET_UPSERTED` (Message Queue)**
            * **Mô tả:** Sự kiện được phát hành bởi `KnowledgeExtractionAgent` sau khi một `KnowledgeSnippet` được tạo mới hoặc cập nhật thành công trong Neo4j. Sự kiện này kích hoạt `KnowledgeEmbeddingAgent`.
            * **Kênh (Channel):** Message Queue (ví dụ: RabbitMQ, Kafka)
            * **Topic/Routing Key (ví dụ):** `trm.event.knowledgesnippet.upserted`
            * **Publisher:** `KnowledgeExtractionAgent`
            * **Consumer dự kiến:** `KnowledgeEmbeddingAgent`
            * **Cấu trúc Thông điệp (Message Structure):**
                * **Header (theo chuẩn A.8.2):**
                    ```yamljson
                    {
                      "messageId": "uuid-for-event-ks-upserted",
                      "eventType": "KNOWLEDGE_SNIPPET_UPSERTED",
                      "sourceAgentId": "KnowledgeExtractionAgent_instance_002",
                      "timestamp": "2025-06-12T10:30:00Z",
                      "version": "1.0",
                      "correlationId": "uuid-for-event-new-raw-data"
                    }
                    ```yaml
                * **Payload:**
                    ```yamljson
                    {
                      "knowledgeSnippetId": "ks_abc_123",
                      "title": "Best Practices for AI Agent Communication",
                      "contentType": "text/markdown",
                      "status": "CREATED",
                      "version": 1,
                      "upsertTimestamp": "2025-06-12T10:29:55Z",
                      "triggeringRawDataPointId": "rdp_xyz_789"
                    }
                    ```yaml

        * **A.8.5.4 Interaction: `KnowledgeEmbeddingAgent` truy vấn `KnowledgeSnippet` từ Neo4j (Internal Service Call / Direct DB Access)**
            * **Mô tả:** Sau khi nhận sự kiện `KNOWLEDGE_SNIPPET_UPSERTED`, `KnowledgeEmbeddingAgent` cần truy vấn nội dung đầy đủ của `KnowledgeSnippet` từ Neo4j để tạo embedding.
            * **Agent gọi:** `KnowledgeEmbeddingAgent`
            * **Dịch vụ/Hệ thống được gọi:** Neo4j Database
            * **Phương thức:** Cypher query qua Neo4j driver.
            * **Request (Cypher Query Example):**
                ```yamlcypher
                MATCH (ks:KnowledgeSnippet {id: $knowledgeSnippetId})
                RETURN ks.id AS id, ks.title AS title, ks.content AS content, ks.tags AS tags
                ```yaml
                *   Tham số: `knowledgeSnippetId` (lấy từ payload của sự kiện `KNOWLEDGE_SNIPPET_UPSERTED`)
            * **Response (Conceptual JSON representation of query result):**
                ```yamljson
                {
                  "id": "ks_abc_123",
                  "title": "Best Practices for AI Agent Communication",
                  "content": "The full textual content of the knowledge snippet...",
                  "tags": ["ai_agent", "communication", "best_practice"]
                }
                ```yaml
            * **Xử lý lỗi:** `KnowledgeEmbeddingAgent` cần xử lý các trường hợp lỗi như snippet không tìm thấy, lỗi kết nối database.

        * **A.8.5.5 Interaction: `KnowledgeEmbeddingAgent` lưu trữ Embedding vào Supabase Vector (API Call)**
            * **Mô tả:** Sau khi tạo vector embedding từ nội dung `KnowledgeSnippet`, `KnowledgeEmbeddingAgent` lưu trữ vector này vào Supabase Vector (pgvector).
            * **Agent gọi:** `KnowledgeEmbeddingAgent`
            * **Dịch vụ được gọi:** Supabase API (cho pgvector)
            * **Endpoint (Ví dụ RESTful, thực tế phụ thuộc Supabase client library):** `POST /rest/v1/knowledge_snippet_embeddings` (tên bảng `knowledge_snippet_embeddings` trong Supabase)
            * **Request Header (Ví dụ, bao gồm Supabase Auth):**
                ```yamljson
                {
                  "apikey": "SUPABASE_ANON_KEY",
                  "Authorization": "Bearer SUPABASE_JWT",
                  "Content-Type": "application/json",
                  "Prefer": "return=representation"
                }
                ```yaml
            * **Request Payload:**
                ```yamljson
                {
                  "knowledge_snippet_id": "ks_abc_123",
                  "embedding_vector": [0.123, 0.456, 0.789],
                  "text_content_hash": "sha256_hash_of_the_content_used_for_embedding",
                  "embedding_model_name": "text-embedding-ada-002",
                  "created_at": "2025-06-12T11:00:00Z"
                }
                ```yaml
            * **Response (201 Created - nếu `Prefer: return=representation`):**
                ```yamljson
                [
                  {
                    "id": "embedding_uuid_123",
                    "knowledge_snippet_id": "ks_abc_123",
                    "embedding_model_name": "text-embedding-ada-002",
                    "created_at": "2025-06-12T11:00:00Z"
                  }
                ]
                ```yaml
            * **Xử lý lỗi:** `KnowledgeEmbeddingAgent` cần xử lý các lỗi API từ Supabase (ví dụ: lỗi xác thực, lỗi ghi dữ liệu, conflict ID).

    *   **A.8.6. Tài liệu và Đăng ký (Documentation & Registry)**
        *   Tất cả các API contracts và message schemas phải được tài liệu hóa chi tiết.
        *   Xem xét việc sử dụng một công cụ như Swagger/OpenAPI cho REST APIs.
        *   Tương tự như Event Catalog (Mục 13.3.4), có thể xây dựng một "API Contract Registry" để quản lý và khám phá các API giữa các agent.

    *Việc tuân thủ các đặc tả này sẽ giúp xây dựng một hệ thống agent TRM-OS mạnh mẽ, linh hoạt và dễ dàng bảo trì.*

---

*Ghi chú: Tài liệu này sẽ được cập nhật và bổ sung chi tiết liên tục trong quá trình phát triển.* 
