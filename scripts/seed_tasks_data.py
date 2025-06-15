#!/usr/bin/env python
# coding: utf-8

"""
Script để bơm dữ liệu thực tế cho Task và các relationship liên quan.
Đây là phần bổ sung cho script seed_data.py ban đầu, tập trung vào các entity còn thiếu.

Prerequisites:
- API server phải đang chạy trên cổng 8000
- Neo4j đã kết nối
"""

import requests
import uuid
import time
import sys
import os

# Add the project root to the Python path to allow imports from trm_api
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from typing import List, Dict, Any
from trm_api.db.session import get_driver
from rich.console import Console
from rich.table import Table
from datetime import datetime, timedelta

# --- Configuration ---
BASE_URL = "http://127.0.0.1:8000/api/v1"
console = Console()

# --- Sample Data cho Task ---
TASKS_DATA = [
    {
        "name": "Triển khai đầy đủ ontology V3.2", 
        "description": "Triển khai toàn bộ entity và relationship theo ontology V3.2", 
        "status": "in_progress",
        "effort": 8,
        "dueDate": (datetime.now() + timedelta(days=14)).isoformat()
    },
    {
        "name": "Kiểm thử API endpoints", 
        "description": "Kiểm thử toàn bộ API endpoints đã lập trình", 
        "status": "in_progress",
        "effort": 5,
        "dueDate": (datetime.now() + timedelta(days=7)).isoformat()
    },
    {
        "name": "Xây dựng pipeline ETL", 
        "description": "Xây dựng pipeline ETL cho dữ liệu từ các nguồn bên ngoài", 
        "status": "not_started",
        "effort": 13,
        "dueDate": (datetime.now() + timedelta(days=21)).isoformat()
    },
    {
        "name": "Test coverage ontology", 
        "description": "Cải thiện test coverage cho ontology", 
        "status": "not_started",
        "effort": 5,
        "dueDate": (datetime.now() + timedelta(days=10)).isoformat()
    },
    {
        "name": "Tổng hợp gap report", 
        "description": "Tổng hợp báo cáo về các gap còn thiếu", 
        "status": "not_started",
        "effort": 3,
        "dueDate": (datetime.now() + timedelta(days=5)).isoformat()
    },
]

# --- Helper Functions ---

def _post_request(endpoint: str, data: dict, description: str) -> dict:
    """Helper to send POST request and handle response."""
    try:
        response = requests.post(f"{BASE_URL}{endpoint}", json=data)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        console.print(f"✅ [green]Successfully created {description}:[/green] {data.get('name') or data.get('title')}")
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        console.print(f"❌ [bold red]Error creating {description}:[/bold red] {http_err}")
        # In chi tiết lỗi từ response của server
        try:
            error_details = http_err.response.json()
            console.print(f"[red]Server Response:[/red] {error_details}")
        except ValueError:
            console.print(f"[red]Server Response (non-JSON):[/red] {http_err.response.text}")
        return None
    except requests.exceptions.RequestException as req_err:
        console.print(f"❌ [bold red]Error creating {description} (Request failed):[/bold red] {req_err}")
        return None

def _create_relationship_request(endpoint: str, description: str, data=None) -> dict:
    """Helper to send POST request for creating a relationship."""
    try:
        if data:
            response = requests.post(f"{BASE_URL}{endpoint}", json=data)
        else:
            response = requests.post(f"{BASE_URL}{endpoint}")
        response.raise_for_status()
        console.print(f"✅ [green]Successfully created relationship:[/green] {description}")
        return response.json()
    except requests.exceptions.RequestException as e:
        console.print(f"❌ [bold red]Error creating relationship {description}:[/bold red] {e}")
        return None

def health_check(retries=5, delay=2):
    """Checks if the API is running, with a retry mechanism."""
    console.print("Checking API health...", style="bold blue")
    
    for attempt in range(retries):
        try:
            response = requests.get(f"{BASE_URL}/users/")
            if response.status_code == 200:
                console.print("✅ [green]API server is running![/green]")
                return True
            else:
                console.print(f"⚠️ API responded with status code: {response.status_code}. Retrying in {delay} seconds...")
        except requests.exceptions.RequestException:
            if attempt < retries - 1:
                console.print(f"⚠️ API server not responding. Retrying in {delay} seconds... (Attempt {attempt + 1}/{retries})")
                time.sleep(delay)
            else:
                console.print("❌ [bold red]Could not connect to API server after multiple attempts.[/bold red]")
                console.print("Make sure the API server is running on http://127.0.0.1:8000", style="yellow")
                return False
    
    return False

def create_tasks() -> list:
    """Creates tasks from the sample data."""
    console.rule("[bold blue]Creating Tasks[/bold blue]")
    created_tasks = []
    for task_data in TASKS_DATA:
        created_task = _post_request("/tasks/", task_data, "Task")
        if created_task:
            created_tasks.append(created_task)
    return created_tasks

def get_users() -> list:
    """Gets existing users from the API."""
    console.print("Getting existing users...", style="bold blue")
    try:
        response = requests.get(f"{BASE_URL}/users/")
        response.raise_for_status()
        users = response.json()
        if users:
            console.print(f"✅ [green]Found {len(users)} existing users.[/green]")
            return users
        else:
            console.print("⚠️ No existing users found. Please run seed_data.py first.")
            return []
    except requests.exceptions.RequestException as e:
        console.print(f"❌ [bold red]Error getting users:[/bold red] {e}")
        return []

def get_projects() -> list:
    """Gets existing projects from the API."""
    console.print("Getting existing projects...", style="bold blue")
    try:
        response = requests.get(f"{BASE_URL}/projects/")
        response.raise_for_status()
        projects = response.json()
        if projects:
            console.print(f"✅ [green]Found {len(projects)} existing projects.[/green]")
            return projects
        else:
            console.print("⚠️ No existing projects found. Please run seed_data.py first.")
            return []
    except requests.exceptions.RequestException as e:
        console.print(f"❌ [bold red]Error getting projects:[/bold red] {e}")
        return []

def create_task_relationships(tasks: list, users: list, projects: list) -> int:
    """Creates relationships between tasks and other entities."""
    console.rule("[bold blue]Creating Task Relationships[/bold blue]")
    relationships_created_count = 0

    if not tasks or not users or not projects:
        console.print("Missing required entities. Cannot create task relationships.", style="bold red")
        return relationships_created_count

    # --- Assign Tasks to Users (ASSIGNS_TASK) ---
    # First user assigns first 3 tasks, Second user assigns remaining tasks
    user_task_assignments = {}
    if len(users) >= 2:
        user_task_assignments = {
            users[0]["userId"]: tasks[:3],
            users[1]["userId"]: tasks[3:]
        }

    for user_id, assigned_tasks in user_task_assignments.items():
        for task in assigned_tasks:
            endpoint = f"/users/{user_id}/assigns-task/{task['taskId']}"
            rel_data = {
                "assignedDate": datetime.now().isoformat(),
                "notes": f"Task assigned to user {user_id}"
            }
            desc = f"User:{user_id} -> ASSIGNS_TASK -> Task:{task['taskId']}"
            if _create_relationship_request(endpoint, desc, rel_data):
                relationships_created_count += 1

    # --- Link Tasks to Projects (IS_PART_OF) ---
    # First 3 tasks -> First project, Remaining tasks -> Second project
    project_task_assignments = {}
    if len(projects) >= 2:
        project_task_assignments = {
            projects[0]["projectId"]: tasks[:3],
            projects[1]["projectId"]: tasks[3:]
        }

    for project_id, project_tasks in project_task_assignments.items():
        for task in project_tasks:
            endpoint = f"/projects/{project_id}/has-task/{task['taskId']}"
            rel_data = {
                "assignedDate": datetime.now().isoformat(),
                "notes": f"Task is part of project {project_id}"
            }
            desc = f"Task:{task['taskId']} -> IS_PART_OF -> Project:{project_id}"
            if _create_relationship_request(endpoint, desc, rel_data):
                relationships_created_count += 1

    return relationships_created_count

def main():
    console.rule("[bold cyan]🚀 Seeding Tasks and Relationships 🚀[/bold cyan]")

    if not health_check():
        console.rule("[bold red]Seeding Aborted[/bold red]")
        return

    # --- Create Tasks ---
    tasks = create_tasks()

    # --- Get existing entities ---
    users = get_users()
    projects = get_projects()

    if not tasks or not users or not projects:
        console.print("Missing required entities. Aborting further seeding.", style="bold red")
        return

    # --- Create Task Relationships ---
    relationships_count = create_task_relationships(tasks, users, projects)

    # --- Summary ---
    console.rule("[bold blue]Summary of Seeding[/bold blue]")
    table = Table(title="Created Items")
    table.add_column("Item Type", justify="right", style="cyan", no_wrap=True)
    table.add_column("Count", justify="center", style="magenta")
    table.add_row("Tasks", str(len(tasks)))
    table.add_row("Task Relationships", str(relationships_count))
    console.print(table)

    console.rule("[bold green]✅ Task Seeding Completed Successfully ✅[/bold green]")

if __name__ == "__main__":
    main()
