#!/usr/bin/env python3
"""
Kiểm thử API Relationship của TRM-OS theo GAP Analysis V3.2
"""

import requests
import json
import uuid
import pytest
from datetime import datetime
import time
from pprint import pprint
from typing import Dict, List, Any

# Thông tin cấu hình API Server
API_BASE_URL = "http://localhost:8002/api/v1"
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

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
            response = requests.post(url, headers=HEADERS, json=data)
        elif method == "PUT":
            response = requests.put(url, headers=HEADERS, json=data)
        elif method == "DELETE":
            response = requests.delete(url, headers=HEADERS, params=params)
        else:
            raise ValueError(f"Không hỗ trợ phương thức HTTP: {method}")
        
        return response
    except requests.exceptions.RequestException as e:
        print(f"\n[LỖI] Lỗi khi gọi API {url}: {str(e)}")
        return None

@pytest.mark.skip(reason="External API integration test - requires running server")
def test_relationship_creation_and_retrieval():
    """Kiểm tra tạo và lấy relationship"""
    print("\n=== KIỂM TRA RELATIONSHIP API ===\n")
    
    # Lấy danh sách tất cả User để sử dụng cho Relationship
    users_response = api_request("GET", "/users/")
    if users_response.status_code != 200:
        print("Không thể lấy danh sách User.")
        return False
    
    users = users_response.json()
    if not users:
        print("Không có user nào trong hệ thống để kiểm thử!")
        return False
    
    user = users[0]
    
    # Tạo Project để test relationship
    project_data = {
        "title": f"Test Project for Relationship {datetime.now().isoformat()}",
        "description": "Project được tạo để kiểm thử relationship."
    }
    
    create_project_response = api_request("POST", "/projects/", data=project_data)
    print_response(create_project_response, "Tạo Project mới")
    
    if create_project_response.status_code != 201:
        print("Không thể tạo Project mới để kiểm thử!")
        return False
    
    project = create_project_response.json()
    print(f"✓ Project mới đã được tạo với ID: {project['uid']}")
    
    # Tạo Task để test relationship
    task_data = {
        "name": f"Test Task for Relationship {datetime.now().isoformat()}",
        "description": "Task được tạo để kiểm thử relationship.",
        "status": "open",
        "project_id": project["uid"],
        "effort": 2  # Thêm trường effort để tránh sử dụng default của model
    }
    
    create_task_response = api_request("POST", "/tasks/", data=task_data)
    print_response(create_task_response, "Tạo Task mới")
    
    if create_task_response.status_code != 201:
        print("Không thể tạo Task mới để kiểm thử!")
        return False
    
    task = create_task_response.json()
    print(f"✓ Task mới đã được tạo với ID: {task['uid']}")
    
    # Tạo KnowledgeSnippet để test relationship
    knowledge_snippet_data = {
        "title": f"Test Knowledge for Relationship {datetime.now().isoformat()}",
        "content": "Đây là nội dung knowledge snippet để test relationship.",
        "source": "Test API",
        "tags": ["test", "relationship", "knowledge"]
    }
    
    create_ks_response = api_request("POST", "/knowledge-snippets/", data=knowledge_snippet_data)
    print_response(create_ks_response, "Tạo KnowledgeSnippet mới")
    
    if create_ks_response.status_code != 201:
        print("Không thể tạo KnowledgeSnippet mới để kiểm thử!")
        return False
    
    knowledge_snippet = create_ks_response.json()
    print(f"✓ Knowledge Snippet mới đã được tạo với ID: {knowledge_snippet['uid']}")
    
    # Test CREATES_KNOWLEDGE relationship
    creates_knowledge_data = {
        "source_id": user["uid"],
        "source_type": "User",
        "knowledge_snippet_id": knowledge_snippet["uid"]
    }
    
    creates_knowledge_response = api_request("POST", "/relationships/creates-knowledge", data=creates_knowledge_data)
    print_response(creates_knowledge_response, "Tạo Relationship CREATES_KNOWLEDGE")
    
    if creates_knowledge_response.status_code == 200:
        print("✓ Endpoint CREATES_KNOWLEDGE hoạt động!")
    else:
        print("✗ Endpoint CREATES_KNOWLEDGE không hoạt động.")
        
    # Test USES_KNOWLEDGE relationship
    uses_knowledge_data = {
        "source_id": task["uid"],
        "source_type": "Task",
        "knowledge_snippet_id": knowledge_snippet["uid"]
    }
    
    uses_knowledge_response = api_request("POST", "/relationships/uses-knowledge", data=uses_knowledge_data)
    print_response(uses_knowledge_response, "Tạo Relationship USES_KNOWLEDGE")
    
    if uses_knowledge_response.status_code == 200:
        print("✓ Endpoint USES_KNOWLEDGE hoạt động!")
    else:
        print("✗ Endpoint USES_KNOWLEDGE không hoạt động.")

    # Test RELATED_TO relationship
    related_to_data = {
        "source_id": user["uid"],
        "source_type": "User",
        "related_id": task["uid"],
        "related_type": "Task"
    }
    
    related_to_response = api_request("POST", "/relationships/related-to", data=related_to_data)
    print_response(related_to_response, "Tạo Relationship RELATED_TO")
    
    if related_to_response.status_code == 200:
        print("✓ Endpoint RELATED_TO hoạt động!")
    else:
        print("✗ Endpoint RELATED_TO không hoạt động.")

    return True

if __name__ == "__main__":
    test_relationship_creation_and_retrieval()
