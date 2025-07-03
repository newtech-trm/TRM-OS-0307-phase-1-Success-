#!/usr/bin/env python
# coding: utf-8

"""
Script để tạo dữ liệu mẫu cho Tension và các mối quan hệ theo Ontology V3.2:
- RESOLVES: Task -> Tension
- LEADS_TO_WIN: Tension -> WIN

Prerequisites:
- API server phải đang chạy trên cổng 8000
- Neo4j đã kết nối
- Đã có sẵn Task và WIN entities trong database
"""

import requests
import uuid
import time
import sys
import os
import json
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any
from rich.console import Console
from rich.table import Table

# --- Configuration ---
BASE_URL = "http://127.0.0.1:8001/api/v1"
console = Console()

# --- Sample Data cho Tension ---
TENSIONS_DATA = [
    {
        "title": "Thiếu tài liệu API đầy đủ", 
        "description": "Tài liệu API hiện tại không đầy đủ và không phản ánh đúng các mối quan hệ theo Ontology V3.2", 
        "status": "Open",
        "priority": 2,
        "source": "FounderInput",
        "tensionType": "Problem",
        "currentState": "Tài liệu API không đầy đủ",
        "desiredState": "Tài liệu API đầy đủ, chính xác theo Ontology V3.2",
        "impactAssessment": "Cao, ảnh hưởng đến khả năng phát triển của đội",
        "tags": ["documentation", "api", "ontology"]
    },
    {
        "title": "Cần cải thiện hiệu suất truy vấn Neo4j", 
        "description": "Các truy vấn Neo4j hiện tại chưa được tối ưu, dẫn đến tốc độ chậm khi làm việc với dữ liệu lớn", 
        "status": "Open",
        "priority": 3,
        "source": "TeamInput",
        "tensionType": "Problem",
        "currentState": "Truy vấn Neo4j chưa tối ưu, performance chậm",
        "desiredState": "Truy vấn Neo4j được tối ưu, tăng tốc đáng kể",
        "impactAssessment": "Trung bình, ảnh hưởng đến UX khi hệ thống phát triển",
        "tags": ["performance", "neo4j", "optimization"]
    },
    {
        "title": "Cơ hội tích hợp AI vào hệ thống", 
        "description": "Có cơ hội tích hợp AI vào hệ thống để tự động hóa quy trình và tăng hiệu quả", 
        "status": "Open",
        "priority": 2,
        "source": "AIAssistant",
        "tensionType": "Opportunity",
        "currentState": "Chưa có AI trong hệ thống",
        "desiredState": "AI được tích hợp để hỗ trợ người dùng",
        "impactAssessment": "Cao, tiềm năng tăng đáng kể hiệu suất",
        "tags": ["ai", "automation", "innovation"]
    },
    {
        "title": "Thiếu kiểm thử tự động", 
        "description": "Hệ thống còn thiếu kiểm thử tự động cho nhiều phần quan trọng", 
        "status": "Open",
        "priority": 1,
        "source": "TeamInput",
        "tensionType": "Problem",
        "currentState": "Kiểm thử thủ công, thiếu coverage",
        "desiredState": "Kiểm thử tự động với coverage cao",
        "impactAssessment": "Cao, ảnh hưởng đến chất lượng code và tốc độ phát triển",
        "tags": ["testing", "automation", "quality"]
    },
    {
        "title": "Cần cải thiện UX của dashboard", 
        "description": "UX hiện tại của dashboard khó sử dụng và không trực quan", 
        "status": "Open",
        "priority": 2,
        "source": "UserFeedback",
        "tensionType": "Problem",
        "currentState": "Dashboard UX phức tạp, khó sử dụng",
        "desiredState": "Dashboard UX trực quan, dễ sử dụng",
        "impactAssessment": "Trung bình, ảnh hưởng đến trải nghiệm người dùng",
        "tags": ["ux", "dashboard", "design"]
    }
]

# --- Helper Functions ---

def print_status(message, is_success=True):
    """In thông báo trạng thái có định dạng."""
    prefix = "✅ SUCCESS:" if is_success else "❌ ERROR:"
    print(f"{prefix} {message}")

def _post_request(endpoint: str, data: dict, description: str):
    """Helper để gửi POST request và xử lý response."""
    try:
        response = requests.post(
            f"{BASE_URL}/{endpoint}",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()  # Raise an exception for 4XX/5XX responses
        result = response.json()
        print_status(f"{description}: {result}")
        return result
    except requests.exceptions.RequestException as e:
        error_content = e.response.json() if hasattr(e, 'response') and e.response and e.response.headers.get('content-type') == 'application/json' else str(e)
        print_status(f"Failed to {description}. Details: {error_content}", is_success=False)
        return None

def get_entities(entity_name):
    """Lấy tất cả entities của một loại nhất định (ví dụ: 'tasks', 'wins')."""
    try:
        response = requests.get(f"{BASE_URL}/{entity_name}/")
        response.raise_for_status()
        entities = response.json()
        if not entities:
            print_status(f"Không tìm thấy entity nào thuộc loại '{entity_name}'. Không thể tạo mối quan hệ.", is_success=False)
            return []
        print_status(f"Đã lấy thành công {len(entities)} {entity_name}.")
        return entities
    except requests.exceptions.RequestException as e:
        print_status(f"Không thể lấy {entity_name}: {e}", is_success=False)
        return []

def create_relationship(source_type, source_id, relationship_type, target_type, target_id, params=None):
    """Tạo một mối quan hệ giữa hai entities."""
    endpoint = f"{source_type}/{source_id}/{relationship_type}/{target_id}"
    if params:
        endpoint += "?" + "&".join([f"{k}={v}" for k, v in params.items()])
    
    try:
        response = requests.post(f"{BASE_URL}/{endpoint}")
        response.raise_for_status()
        print_status(f"Đã tạo mối quan hệ {relationship_type} giữa {source_type} và {target_type}")
        return response.json()
    except requests.exceptions.RequestException as e:
        error_content = e.response.json() if hasattr(e, 'response') and e.response and e.response.headers.get('content-type') == 'application/json' else str(e)
        print_status(f"Không thể tạo mối quan hệ qua {endpoint}. Details: {error_content}", is_success=False)
        return None

def health_check(retries=5, delay=2):
    """Kiểm tra xem API có đang chạy không, với cơ chế retry."""
    for i in range(retries):
        try:
            response = requests.get(f"{BASE_URL}/health")
            if response.status_code == 200:
                print_status("API server is running and healthy.")
                return True
        except requests.exceptions.ConnectionError:
            pass
        
        if i < retries - 1:
            print(f"API server not available. Retrying in {delay} seconds...")
            time.sleep(delay)
    
    print_status("API server is not running or not healthy. Please start the API server before running this script.", is_success=False)
    return False

def create_tensions():
    """Tạo các tension từ dữ liệu mẫu."""
    created_tensions = []
    for tension_data in TENSIONS_DATA:
        result = _post_request("tensions/", tension_data, f"Created tension '{tension_data['title']}'")
        if result:
            created_tensions.append(result)
    
    console.print(f"Created {len(created_tensions)} tensions")
    return created_tensions

def create_tension_relationships(tensions, tasks, wins):
    """Tạo các mối quan hệ giữa Tension và các entity khác theo Ontology V3.2."""
    # Hiển thị thông tin
    table = Table(title="Entity Counts")
    table.add_column("Entity Type")
    table.add_column("Count")
    table.add_row("Tensions", str(len(tensions)))
    table.add_row("Tasks", str(len(tasks)))
    table.add_row("WINs", str(len(wins)))
    console.print(table)
    
    # 1. Tạo mối quan hệ RESOLVES (Task -> Tension)
    print("\n🔗 Tạo mối quan hệ 'RESOLVES' (Task -> Tension)...")
    if tasks and tensions:
        for i, tension in enumerate(tensions):
            # Assign 1-2 tasks to resolve each tension
            num_tasks = random.randint(1, min(2, len(tasks)))
            selected_tasks = random.sample(tasks, num_tasks)
            
            for task in selected_tasks:
                try:
                    tension_id = tension.get('uid') or tension.get('id') or tension.get('tension_id')
                    task_id = task.get('uid') or task.get('id') or task.get('task_id')
                    
                    if tension_id and task_id:
                        create_relationship(
                            "tasks", task_id,
                            "resolves", "tensions", tension_id
                        )
                except Exception as e:
                    print_status(f"Error creating RESOLVES relationship: {str(e)}", is_success=False)
    
    # 2. Tạo mối quan hệ LEADS_TO_WIN (Tension -> WIN)
    print("\n🔗 Tạo mối quan hệ 'LEADS_TO_WIN' (Tension -> WIN)...")
    if tensions and wins:
        for i, tension in enumerate(tensions):
            # Not every tension leads to a win
            if random.random() < 0.7:  # 70% chance
                selected_win = random.choice(wins)
                
                try:
                    tension_id = tension.get('uid') or tension.get('id') or tension.get('tension_id')
                    win_id = selected_win.get('uid') or selected_win.get('id') or selected_win.get('win_id')
                    
                    if tension_id and win_id:
                        # Add relationship params
                        params = {
                            "contribution_level": random.randint(1, 5),
                            "direct_contribution": random.choice(["true", "false"])
                        }
                        
                        create_relationship(
                            "tensions", tension_id,
                            "leads-to-win", "wins", win_id,
                            params
                        )
                except Exception as e:
                    print_status(f"Error creating LEADS_TO_WIN relationship: {str(e)}", is_success=False)

def main():
    """Hàm chính để tạo dữ liệu mẫu cho Tension và các mối quan hệ."""
    console.print("\n[bold green]🚀 Bắt đầu quá trình tạo dữ liệu mẫu cho Tension và các mối quan hệ[/bold green]\n")
    
    # Kiểm tra kết nối API
    if not health_check():
        return
    
    # 1. Tạo các Tension mới
    console.print("\n[bold blue]Tạo các Tension mới[/bold blue]")
    tensions = create_tensions()
    
    # 2. Lấy các Task và WIN hiện có
    console.print("\n[bold blue]Lấy các Task và WIN hiện có[/bold blue]")
    tasks = get_entities("tasks")
    wins = get_entities("wins")
    
    # 3. Tạo các mối quan hệ
    console.print("\n[bold blue]Tạo các mối quan hệ theo Ontology V3.2[/bold blue]")
    create_tension_relationships(tensions, tasks, wins)
    
    console.print("\n[bold green]🎉 Hoàn thành quá trình tạo dữ liệu mẫu![/bold green]")

if __name__ == "__main__":
    main()
