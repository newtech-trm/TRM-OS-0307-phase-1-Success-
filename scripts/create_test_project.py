#!/usr/bin/env python
# coding: utf-8

"""
Script để tạo một project test cho việc seed dữ liệu.
"""

import requests
import json
import sys
from rich.console import Console
from datetime import datetime

# --- Configuration ---
BASE_URL = "http://127.0.0.1:8001/api/v1"
console = Console()

# Project ID cụ thể chúng ta muốn sử dụng
CUSTOM_PROJECT_ID = "fe6d41f5-a3c0-4b94-9c4d-88507b58b8f8"

# --- Sample Data cho Project ---
PROJECT_DATA = {
    "uid": CUSTOM_PROJECT_ID,
    "title": "TRM-OS Ontology V3.2 Integration",
    "description": "Dự án tích hợp Ontology V3.2 vào TRM-OS",
    "status": "InProgress",
    "goal": "Hoàn thiện tích hợp Ontology V3.2 vào toàn bộ hệ thống TRM-OS",
    "scope": "API, database relationships, validation và seed data",
    "priority": 1,
    "project_type": "development",
    "tags": ["ontology", "integration", "v3.2"],
    "start_date": datetime.now().isoformat(),
    "target_end_date": datetime(2025, 8, 1).isoformat()
}

def _post_request(endpoint: str, data: dict, description: str):
    """Helper to send POST request and handle response."""
    console.print(f"🚀 [bold blue]{description}...[/bold blue]")
    response = requests.post(f"{BASE_URL}/{endpoint}", json=data)
    
    if response.status_code in [200, 201]:
        console.print(f"✅ Thành công! [green]{description}[/green]")
        return response.json()
    else:
        console.print(f"❌ Lỗi {response.status_code}: {response.text}")
        return None

def health_check(retries=5, delay=2):
    """Checks if the API is running, with a retry mechanism."""
    import time
    
    # Lấy base url chỉ đến domain:port (không bao gồm /api/v1)
    base_server = BASE_URL.split('/api/v1')[0]
    console.print("Checking API health...")
    for attempt in range(retries):
        try:
            # Kiểm tra API bằng cách gọi đến endpoint gốc
            response = requests.get(f"{base_server}/")
            if response.status_code == 200:
                console.print(f"✅ API đang hoạt động!")
                return True
        except requests.RequestException:
            pass
        
        if attempt < retries - 1:
            console.print(f"⚠️ API server not responding. Retrying in {delay} seconds... \n(Attempt {attempt+1}/{retries})")
            time.sleep(delay)
    
    console.print("❌ Could not connect to API server after multiple attempts.")
    console.print(f"Make sure the API server is running on {base_server}")
    return False

def create_project():
    """Create the test project."""
    console.print(f"\n[cyan]Project data being sent:[/cyan]")
    console.print(PROJECT_DATA)
    
    # Thực hiện request tạo project
    project = _post_request("projects/", PROJECT_DATA, "Creating test project")
    
    # Kiểm tra xem project có được tạo không
    if project:
        console.print(f"\n[green]Project created successfully:[/green]")
        console.print(project)
        
        # Kiểm tra xem project có thể được truy xuất không
        console.print(f"\n[cyan]Verifying project was saved in database...[/cyan]")
        verify_url = f"{BASE_URL}/projects/{PROJECT_DATA['uid']}"
        response = requests.get(verify_url)
        if response.status_code == 200:
            console.print(f"[green]Project verified! It exists in the database.[/green]")
        else:
            console.print(f"[red]Project not found in database. Status code: {response.status_code}[/red]")
            console.print(f"Response: {response.text}")
    
    return project

def main():
    console.print("───────── 🚀 Creating Test Project 🚀 ──────────")
    
    if not health_check():
        console.print("──────────────────── Setup Aborted ─────────────────────")
        sys.exit(1)
    
    # Create the project
    project = create_project()
    if not project:
        console.print("Failed to create project. Aborting.")
        sys.exit(1)
    
    console.print("\n───────────────────── Summary ─────────────────────")
    console.print(f"Project created with ID: {CUSTOM_PROJECT_ID}")
    console.print(f"Use this ID in your seed_tasks_data.py script")
    console.print("────────────────────────────────────────────────")

if __name__ == "__main__":
    main()
