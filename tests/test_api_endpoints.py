#!/usr/bin/env python3
"""
Kiểm thử toàn diện các API endpoint của TRM-OS theo GAP Analysis V3.2
Tập trung vào Recognition và các Relationship mới triển khai
"""

import requests
import json
import uuid
import pytest
from datetime import datetime
import time
from pprint import pprint
from typing import Dict, List, Any, Optional, Union

# Thông tin cấu hình API Server
API_BASE_URL = "http://localhost:8002/api/v1"
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# Các hàm tiện ích
def generate_uuid():
    """Tạo UUID ngẫu nhiên"""
    return str(uuid.uuid4())

def print_response(response, label=None):
    """In ra response để debug"""
    if label:
        print(f"\n--- {label} ---")
    
    print(f"Status Code: {response.status_code}")
    try:
        pprint(response.json())
    except Exception:
        print(response.text)
    print()

def api_request(method, endpoint, data=None, params=None):
    """Thực hiện request đến API và xử lý lỗi cơ bản"""
    url = f"{API_BASE_URL}{endpoint}"
    print(f"\n[DEBUG] Gọi API: {method} {url}")
    if data:
        print(f"[DEBUG] Request data: {json.dumps(data, indent=2, ensure_ascii=False)}")
    if params:
        print(f"[DEBUG] Request params: {params}")
        
    try:
        if method == "GET":
            response = requests.get(url, headers=HEADERS, params=params)
        elif method == "POST":
            print(f"[DEBUG] Gửi POST với headers: {HEADERS}")
            response = requests.post(url, headers=HEADERS, json=data)
        elif method == "PUT":
            response = requests.put(url, headers=HEADERS, json=data)
        elif method == "DELETE":
            response = requests.delete(url, headers=HEADERS, params=params)
        else:
            raise ValueError(f"Không hỗ trợ phương thức HTTP: {method}")
        
        # In thông tin chi tiết về response    
        print(f"[DEBUG] Response status: {response.status_code}")
        try:
            print(f"[DEBUG] Response headers: {response.headers}")
            print(f"[DEBUG] Response body: {response.text[:500]}... (truncated)")
        except Exception as e:
            print(f"[DEBUG] Không thể hiển thị response đầy đủ: {str(e)}")
            
        return response
    except requests.exceptions.RequestException as e:
        print(f"\n[LỖI] Lỗi khi gọi API {url}: {str(e)}")
        return None

def assert_status_code(response, expected_code=200):
    """Kiểm tra status code của response"""
    actual_code = response.status_code
    assert actual_code == expected_code, f"Mong đợi status code {expected_code}, nhưng nhận được {actual_code}"
    return True

def assert_response_has_field(response, field_name):
    """Kiểm tra response có chứa trường dữ liệu cụ thể"""
    data = response.json()
    assert field_name in data, f"Response không chứa trường dữ liệu '{field_name}'"
    return True

# Kiểm thử API Recognition
@pytest.mark.skip(reason="External API integration test - requires running server")
def test_recognition_crud():
    """Kiểm tra các chức năng CRUD của Recognition API"""
    print("\n=== KIỂM TRA RECOGNITION API ===\n")
    
    # Lấy danh sách tất cả User để sử dụng cho Recognition
    users_response = api_request("GET", "/users/")
    assert_status_code(users_response)
    users = users_response.json()
    
    if len(users) < 2:
        print("Không đủ user trong hệ thống để kiểm thử Recognition API!")
        return
    
    granter = users[0]
    recipient = users[1]
    
    # Lấy một WIN để liên kết với Recognition
    wins_response = api_request("GET", "/wins/")
    assert_status_code(wins_response)
    wins = wins_response.json()
    
    if not wins:
        print("Không có WIN nào trong hệ thống để kiểm thử Recognition API!")
        return
        
    win = wins[0]
    
    # 1. Tạo Recognition mới
    new_recognition = {
        "title": f"Test Recognition {datetime.now().isoformat()}",
        "description": "Recognition được tạo từ bài kiểm thử tự động",
        "granterId": granter["userId"],
        "recipientIds": [recipient["userId"]],
        "winId": win["winId"],
        "recognitionDate": datetime.now().isoformat()
    }
    
    create_response = api_request("POST", "/recognitions/", data=new_recognition)
    print_response(create_response, "Tạo Recognition mới")
    assert_status_code(create_response, 201)
    
    created_recognition = create_response.json()
    recognition_id = created_recognition["recognitionId"]
    
    # 2. Lấy chi tiết Recognition vừa tạo
    get_response = api_request("GET", f"/recognitions/{recognition_id}")
    print_response(get_response, "Chi tiết Recognition")
    assert_status_code(get_response)
    assert_response_has_field(get_response, "title")
    
    # 3. Cập nhật Recognition
    update_data = {
        "title": f"Updated Recognition {datetime.now().isoformat()}",
        "description": "Recognition được cập nhật từ bài kiểm thử tự động"
    }
    
    update_response = api_request("PUT", f"/recognitions/{recognition_id}", data=update_data)
    print_response(update_response, "Cập nhật Recognition")
    assert_status_code(update_response)
    
    # 4. Lấy danh sách tất cả Recognition
    list_response = api_request("GET", "/recognitions/")
    print_response(list_response, "Danh sách Recognition")
    assert_status_code(list_response)
    
    # 5. Xóa Recognition
    delete_response = api_request("DELETE", f"/recognitions/{recognition_id}")
    print_response(delete_response, "Xóa Recognition")
    assert_status_code(delete_response, 204)
    
    # Kiểm tra xác nhận đã xóa thành công
    get_deleted_response = api_request("GET", f"/recognitions/{recognition_id}")
    assert get_deleted_response.status_code == 404, "Recognition chưa được xóa thành công"
    
    print("✓ Kiểm thử Recognition API thành công!")

# Kiểm thử API Relationship
@pytest.mark.skip(reason="External API integration test - requires running server")
def test_relationship_crud():
    """Kiểm tra các chức năng CRUD của Relationship API"""
    print("\n=== KIỂM TRA RELATIONSHIP API ===\n")
    
    # Lấy dữ liệu cần thiết để tạo các mối quan hệ
    # Lấy danh sách User
    users_response = api_request("GET", "/users/")
    assert_status_code(users_response)
    users = users_response.json()
    
    if not users:
        print("Không có User nào trong hệ thống để kiểm thử Relationship API!")
        return
    
    user = users[0]
    
    # 0.5. Tạo một Project mới để đảm bảo có project_id hợp lệ cho việc lấy Task
    print("\n--- Tạo Project mới cho kiểm thử Task ---")
    project_title = f"Test Project for Tasks {datetime.now().isoformat()}"
    new_project_data = {
        "title": project_title,
        "description": "Một project được tạo tự động để kiểm thử API Task."
    }
    create_project_response = api_request("POST", "/projects/", data=new_project_data)
    print_response(create_project_response, "Tạo Project mới")
    assert_status_code(create_project_response, 201) # HTTP 201 Created
    created_project = create_project_response.json()
    assert_response_has_field(create_project_response, "uid")
    created_project_id = created_project["uid"]
    print(f"✓ Project mới đã được tạo với ID: {created_project_id}")

    # Lấy danh sách Task cho project vừa tạo (mong đợi danh sách rỗng ban đầu)
    print(f"\n--- Lấy danh sách Task cho Project ID: {created_project_id} ---")
    tasks_for_project_response = api_request("GET", "/tasks/", params={"project_id": created_project_id})
    print_response(tasks_for_project_response, f"Danh sách Task cho Project {created_project_id}")
    assert_status_code(tasks_for_project_response)
    tasks_for_project = tasks_for_project_response.json()
    assert isinstance(tasks_for_project, list), "Response trả về cho list tasks phải là một list."
    print(f"✓ Lấy danh sách Task cho project {created_project_id} thành công (có thể rỗng).")

    # Để kiểm thử relationship, chúng ta cần một task. 
    # Nếu project vừa tạo không có task, chúng ta sẽ tạo một task mới cho project đó.
    task_to_use_for_relationship = None
    if tasks_for_project:
        task_to_use_for_relationship = tasks_for_project[0]
        print(f"Sử dụng task hiện có ID: {task_to_use_for_relationship['uid']} từ project {created_project_id}")
    else:
        print(f"Project {created_project_id} chưa có task. Tạo task mới...")
        task_data = {
            "name": f"Test Task for Relationship {datetime.now().isoformat()}",
            "description": "Task được tạo để kiểm thử relationship.",
            "status": "open",
            "project_id": created_project_id,
            "effort": 2  # Thêm trường effort để tránh sử dụng default của model
        }
        create_task_response = api_request("POST", "/tasks/", data=task_data)
        print_response(create_task_response, "Tạo Task mới cho Project")
        assert_status_code(create_task_response, 201)
        task_to_use_for_relationship = create_task_response.json()
        assert_response_has_field(create_task_response, "uid")
        print(f"✓ Task mới đã được tạo với ID: {task_to_use_for_relationship['uid']} cho project {created_project_id}")

    if not task_to_use_for_relationship:
        print("Không thể lấy hoặc tạo Task để kiểm thử Relationship API!")
        return
    
    # Đổi tên biến để rõ ràng hơn, vì 'task' đã được dùng ở scope ngoài
    # Chúng ta sẽ sử dụng task_to_use_for_relationship cho các bước tạo relationship
    # Thay vì 'task' được lấy từ danh sách task chung chung có thể không thuộc project nào
    # Gán lại biến 'task' để các phần code phía dưới không cần thay đổi nhiều
    task = task_to_use_for_relationship
    
    # 1. Tạo mối quan hệ tùy chỉnh
    relationship_data = {
        "source_id": user["userId"],
        "source_type": "User",
        "target_id": task["taskId"],
        "target_type": "Task",
        "relationship_type": "RELATED_TO"
    }
    
    create_response = api_request("POST", "/relationships/", data=relationship_data)
    print_response(create_response, "Tạo Relationship mới")
    assert_status_code(create_response, 200)
    
    # 2. Lấy các mối quan hệ của User
    params = {
        "entity_id": user["userId"],
        "entity_type": "User",
        "direction": "outgoing"
    }
    
    get_response = api_request("GET", "/relationships/", params=params)
    print_response(get_response, "Danh sách Relationship của User")
    assert_status_code(get_response)
    
    # 3. Xóa mối quan hệ đã tạo
    delete_params = {
        "source_id": user["userId"],
        "source_type": "User",
        "target_id": task["taskId"],
        "target_type": "Task",
        "relationship_type": "RELATED_TO"
    }
    
    delete_response = api_request("DELETE", "/relationships/", params=delete_params)
    print_response(delete_response, "Xóa Relationship")
    assert_status_code(delete_response, 204)
    
    print("✓ Kiểm thử Relationship API cơ bản thành công!")
    
    # Kiểm thử các endpoint relationship chuyên biệt
    print("\n=== KIỂM TRA CÁC ENDPOINT RELATIONSHIP CHUYÊN BIỆT ===\n")

    # Tạo một KnowledgeSnippet mới để kiểm thử CREATES_KNOWLEDGE và USES_KNOWLEDGE
    print("\n--- Tạo Knowledge Snippet mới ---")
    ks_content = f"Đây là một ví dụ về knowledge snippet được tạo lúc {datetime.now().isoformat()} cho kiểm thử."
    new_ks_data = {
        "content": ks_content,
        "snippetType": "CodeExample", # Sử dụng alias snippetType
        "sourceEntityId": task["uid"], # Giả sử task được tạo ở trên
        "tags": ["python", "fastapi", "test"]
    }
    create_ks_response = api_request("POST", "/knowledge-snippets/", data=new_ks_data)
    print_response(create_ks_response, "Tạo Knowledge Snippet mới")
    assert_status_code(create_ks_response, 201)
    created_ks = create_ks_response.json()
    # API trả về 'uid' theo model KnowledgeSnippet(KnowledgeSnippetInDB) nhưng KnowledgeSnippetInDB có snippet_id alias "snippetId"
    # Tuy nhiên, service và repo đang trả về uid. Cần kiểm tra response thực tế.
    # Dựa trên log trước đó của các API khác, server trả về 'uid'.
    assert_response_has_field(create_ks_response, "uid") 
    knowledge_snippet_id = created_ks["uid"]
    print(f"✓ Knowledge Snippet mới đã được tạo với ID: {knowledge_snippet_id}")
    
    # Test RELATED_TO relationship
    related_to_data = {
        "source_id": user["userId"],
        "source_type": "User",
        "related_id": task["taskId"],
        "related_type": "Task"
    }
    
    related_to_response = api_request("POST", "/relationships/related-to", data=related_to_data)
    print_response(related_to_response, "Tạo Relationship RELATED_TO")
    if related_to_response and related_to_response.status_code == 200:
        print("✓ Endpoint RELATED_TO hoạt động!")
    else:
        print("✗ Endpoint RELATED_TO không hoạt động.")
    
    # Test TRIGGERS relationship
    triggers_data = {
        "source_id": user["userId"],
        "source_type": "User",
        "target_id": task["taskId"],
        "target_type": "Task"
    }
    
    triggers_response = api_request("POST", "/relationships/triggers", data=triggers_data)
    print_response(triggers_response, "Tạo Relationship TRIGGERS")
    if triggers_response and triggers_response.status_code == 200:
        print("✓ Endpoint TRIGGERS hoạt động!")
    else:
        print("✗ Endpoint TRIGGERS không hoạt động.")
    
    # Test TRIGGERED_BY relationship
    triggered_by_data = {
        "source_id": task["taskId"],
        "source_type": "Task",
        "trigger_id": user["userId"],
        "trigger_type": "User"
    }
    
    triggered_by_response = api_request("POST", "/relationships/triggered-by", data=triggered_by_data)
    print_response(triggered_by_response, "Tạo Relationship TRIGGERED_BY")
    if triggered_by_response and triggered_by_response.status_code == 200:
        print("✓ Endpoint TRIGGERED_BY hoạt động!")
    else:
        print("✗ Endpoint TRIGGERED_BY không hoạt động.")

    # Kiểm thử CREATES_KNOWLEDGE
    creates_knowledge_data = {
        "source_id": user["uid"], # User tạo ra knowledge
        "source_type": "User",
        "knowledge_snippet_id": knowledge_snippet_id
    }
    creates_knowledge_response = api_request("POST", "/relationships/creates-knowledge", data=creates_knowledge_data)
    print_response(creates_knowledge_response, "Tạo Relationship CREATES_KNOWLEDGE")
    if creates_knowledge_response and creates_knowledge_response.status_code == 200:
        print("✓ Endpoint CREATES_KNOWLEDGE hoạt động!")
    else:
        print("✗ Endpoint CREATES_KNOWLEDGE không hoạt động.")

    # Kiểm thử USES_KNOWLEDGE
    uses_knowledge_data = {
        "source_id": task["uid"], # Task sử dụng knowledge
        "source_type": "Task",
        "knowledge_snippet_id": knowledge_snippet_id
    }
    uses_knowledge_response = api_request("POST", "/relationships/uses-knowledge", data=uses_knowledge_data)
    print_response(uses_knowledge_response, "Tạo Relationship USES_KNOWLEDGE")
    if uses_knowledge_response and uses_knowledge_response.status_code == 200:
        print("✓ Endpoint USES_KNOWLEDGE hoạt động!")
    else:
        print("✗ Endpoint USES_KNOWLEDGE không hoạt động.")
    
    print("Hoàn thành kiểm thử Relationship API!")

def main():
    """Hàm chính chạy tất cả các bài kiểm thử"""
    print("=== BẮT ĐẦU KIỂM THỬ API ENDPOINTS ===")
    
    try:
        test_recognition_crud()
    except Exception as e:
        print(f"Lỗi khi kiểm thử Recognition API: {str(e)}")
    
    try:
        test_relationship_crud()
    except Exception as e:
        print(f"Lỗi khi kiểm thử Relationship API: {str(e)}")
    
    print("\n=== HOÀN THÀNH KIỂM THỬ ===")

if __name__ == "__main__":
    main()
