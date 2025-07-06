#!/usr/bin/env python3
"""
Script kiểm thử mối quan hệ RESOLVES_TENSION giữa Project và Tension.
Sử dụng API và repository trực tiếp để xác nhận tính đúng đắn của việc triển khai.
"""
import sys
import os
import uuid
import asyncio
import pytest
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from neomodel import config as neomodel_config

# Tải biến môi trường từ file .env
env_path = Path(os.path.dirname(os.path.abspath(__file__))) / '..' / '.env'
load_dotenv(env_path)

# Cấu hình kết nối Neo4j từ biến môi trường
NEO4J_URI = os.getenv('NEO4J_URI', 'neo4j+s://66abf65c.databases.neo4j.io')
NEO4J_USER = os.getenv('NEO4J_USER', 'neo4j')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD')

# Cấu hình neomodel để sử dụng kết nối Neo4j từ biến môi trường
# Neo4j Aura sử dụng bolt+s:// thay vì neo4j+s://
# Format: bolt+s://user:password@instance-id.databases.neo4j.io:7687
host = NEO4J_URI.split('://')[-1]  # Lấy phần host/instance-id
bolt_url = f"bolt+s://{NEO4J_USER}:{NEO4J_PASSWORD}@{host}:7687"
neomodel_config.DATABASE_URL = bolt_url

print(f"Đang kết nối đến Neo4j tại: {NEO4J_URI}")
print(f"URL kết nối neomodel: {bolt_url.replace(NEO4J_PASSWORD, '****')}")

# Thiết lập timeout dài hơn cho kết nối cloud
neomodel_config.MAX_CONNECTION_POOL_SIZE = 50
neomodel_config.CONNECTION_RETRY_COUNT = 3
neomodel_config.CONNECTION_TIMEOUT = 10  # seconds

# Thêm thư mục trm_api vào Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import các module cần thiết
from trm_api.repositories.project_repository import ProjectRepository
from trm_api.repositories.tension_repository import TensionRepository
from trm_api.models.project import ProjectCreate
from trm_api.models.tension import TensionCreate

# Khởi tạo repositories
project_repo = ProjectRepository()
tension_repo = TensionRepository()

def print_header(message):
    """In tiêu đề cho các bước kiểm thử."""
    print("\n" + "=" * 80)
    print(f" {message.upper()} ".center(80, "="))
    print("=" * 80)

@pytest.mark.asyncio
async def test_create_project_and_tension():
    """Tạo Project và Tension mới để kiểm thử."""
    print_header("Tạo project và tension mới")
    
    # Tạo project mới
    new_project_data = ProjectCreate(
        title=f"Test Project {uuid.uuid4().hex[:8]}",
        description="Dự án kiểm thử mối quan hệ RESOLVES_TENSION",
        status="active"
    )
    project = await project_repo.create_project(new_project_data)
    print(f"Đã tạo Project: {project.title} (UID: {project.uid})", flush=True)
    
    # Tạo tension mới với schema đúng
    new_tension_data = TensionCreate(
        title=f"Test Tension {uuid.uuid4().hex[:8]} - Kiểm thử mối quan hệ RESOLVES_TENSION",
        description="Tension kiểm thử mối quan hệ RESOLVES_TENSION với schema mới",
        status="Open",
        projectId=project.uid,  # Sử dụng projectId thay vì project_id
        priority=1  # Sử dụng int thay vì string
    )
    tension = tension_repo.create_tension(new_tension_data)
    print(f"Đã tạo Tension: {tension.title} (UID: {tension.uid})", flush=True)
    
    # Cleanup
    tension_repo.delete_tension(tension.uid)
    await project_repo.delete_project(project.uid)
    
    assert project.title.startswith("Test Project")
    assert tension.title.startswith("Test Tension")

@pytest.mark.asyncio
async def test_connect_project_to_tension():
    """Kiểm thử việc tạo mối quan hệ RESOLVES_TENSION từ Project đến Tension."""
    print_header("Tạo mối quan hệ RESOLVES_TENSION")
    
    # Tạo test data
    new_project_data = ProjectCreate(
        title=f"Test Project {uuid.uuid4().hex[:8]}",
        description="Dự án kiểm thử mối quan hệ RESOLVES_TENSION",
        status="active"
    )
    project = await project_repo.create_project(new_project_data)
    
    new_tension_data = TensionCreate(
        title=f"Test Tension {uuid.uuid4().hex[:8]} - Kiểm thử mối quan hệ RESOLVES_TENSION",
        description="Tension kiểm thử mối quan hệ RESOLVES_TENSION với schema mới",
        status="Open",
        projectId=project.uid,
        priority=1
    )
    tension = tension_repo.create_tension(new_tension_data)
    
    try:
        # Sử dụng repository của Tension
        result = tension_repo.connect_tension_to_project(
            tension_uid=tension.uid,
            project_uid=project.uid
        )
        
        if result:
            connected_tension, connected_project = result
            print(f"Đã kết nối thành công: Project '{connected_project.title}' đang giải quyết Tension '{connected_tension.title}'")
            assert True
        else:
            print("Lỗi: Không thể tạo mối quan hệ RESOLVES_TENSION")
            assert False
            
    finally:
        # Cleanup
        tension_repo.delete_tension(tension.uid)
        await project_repo.delete_project(project.uid)

@pytest.mark.asyncio
async def test_query_related_items():
    """Kiểm thử truy vấn các items đã liên kết qua mối quan hệ RESOLVES_TENSION."""
    print_header("Kiểm tra mối quan hệ đã được tạo")
    
    # Tạo test data
    new_project_data = ProjectCreate(
        title=f"Test Project {uuid.uuid4().hex[:8]}",
        description="Dự án kiểm thử mối quan hệ RESOLVES_TENSION",
        status="active"
    )
    project = await project_repo.create_project(new_project_data)
    
    new_tension_data = TensionCreate(
        title=f"Test Tension {uuid.uuid4().hex[:8]} - Kiểm thử mối quan hệ RESOLVES_TENSION",
        description="Tension kiểm thử mối quan hệ RESOLVES_TENSION với schema mới",
        status="Open",
        projectId=project.uid,
        priority=1
    )
    tension = tension_repo.create_tension(new_tension_data)
    
    try:
        # 1. Truy vấn từ phía Tension - kiểm tra các Project đang giải quyết tension
        projects_resolving = tension_repo.get_projects_resolving_tension(tension.uid)
        print(f"Có {len(projects_resolving)} project đang giải quyết Tension '{tension.title}':", flush=True)
        
        # 2. Truy vấn từ phía Project - kiểm tra các Tension đang được giải quyết bởi project
        tensions_resolved = await project_repo.get_tensions_resolved_by_project(project.uid)
        print(f"\nDự án '{project.title}' đang giải quyết {len(tensions_resolved)} tension:", flush=True)
        
        # Basic assertions
        assert isinstance(projects_resolving, list)
        assert isinstance(tensions_resolved, list)
        
    finally:
        # Cleanup
        tension_repo.delete_tension(tension.uid)
        await project_repo.delete_project(project.uid)

# End of pytest tests - the rest are helper functions for standalone script execution
