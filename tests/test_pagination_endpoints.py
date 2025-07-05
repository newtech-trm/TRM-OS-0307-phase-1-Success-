import pytest
import requests
import json
import os
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

# Tải các biến môi trường
load_dotenv()

# Cấu hình API
BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:8000')
console = Console()

@pytest.mark.skip(reason="Fixture endpoint not found - needs parametrize decorator")
def test_pagination_endpoint(endpoint, description, params=None):
    """
    Kiểm thử endpoint pagination và hiển thị kết quả dưới dạng bảng
    
    Args:
        endpoint: Đường dẫn API endpoint (ví dụ: "/api/v1/projects/")
        description: Mô tả endpoint để hiển thị
        params: Tham số truy vấn bổ sung (dict)
    """
    url = f"{BASE_URL}{endpoint}"
    
    # Tham số mặc định cho pagination
    pagination_params = {
        "page": 1,
        "page_size": 10
    }
    
    # Kết hợp các tham số
    if params:
        pagination_params.update(params)
    
    try:
        # Gọi API với tham số pagination
        response = requests.get(url, params=pagination_params)
        response.raise_for_status()
        
        # Phân tích kết quả
        result = response.json()
        
        # Kiểm tra cấu trúc response pagination đúng
        assert "items" in result, "Response không chứa trường 'items'"
        assert "metadata" in result, "Response không chứa trường 'metadata'"
        assert "total_count" in result["metadata"], "Metadata thiếu trường 'total_count'"
        assert "page" in result["metadata"], "Metadata thiếu trường 'page'"
        assert "page_size" in result["metadata"], "Metadata thiếu trường 'page_size'"
        assert "page_count" in result["metadata"], "Metadata thiếu trường 'page_count'"
        assert "has_next" in result["metadata"], "Metadata thiếu trường 'has_next'"
        assert "has_previous" in result["metadata"], "Metadata thiếu trường 'has_previous'"
        
        # Hiển thị kết quả
        console.print(f"\n[bold green]✓ Endpoint: {description} - Thành công![/bold green]")
        
        metadata_table = Table(title="Metadata", show_header=True, header_style="bold blue")
        metadata_table.add_column("Trường")
        metadata_table.add_column("Giá trị")
        
        for key, value in result["metadata"].items():
            metadata_table.add_row(key, str(value))
        
        console.print(metadata_table)
        
        items_table = Table(title="Items", show_header=True, header_style="bold blue")
        
        # Nếu có kết quả, hiển thị danh sách items
        if len(result["items"]) > 0:
            # Lấy một số trường cơ bản để hiển thị
            sample_item = result["items"][0]
            
            # Tùy chọn trường hiển thị dựa trên loại đối tượng
            if "title" in sample_item:
                items_table.add_column("Title")
                title_key = "title"
            elif "name" in sample_item:
                items_table.add_column("Name")
                title_key = "name"
            else:
                items_table.add_column("ID")
                title_key = "uid"
                
            items_table.add_column("UID")
            
            # Hiển thị thông tin các items
            for item in result["items"]:
                item_title = item.get(title_key, "N/A")
                item_uid = item.get("uid", "N/A")
                items_table.add_row(str(item_title), str(item_uid))
            
            console.print(items_table)
        else:
            console.print("[yellow]Không có items nào trong kết quả trả về[/yellow]")
        
        # Kiểm tra phân trang với page thứ 2
        if result["metadata"]["page_count"] > 1:
            console.print("\n[bold]Kiểm tra trang tiếp theo...[/bold]")
            pagination_params["page"] = 2
            
            response2 = requests.get(url, params=pagination_params)
            response2.raise_for_status()
            result2 = response2.json()
            
            console.print(f"[green]Trang 2 có {len(result2['items'])} items[/green]")
            
            # Kiểm tra dữ liệu ở hai trang khác nhau
            if len(result["items"]) > 0 and len(result2["items"]) > 0:
                items1_uids = [item["uid"] for item in result["items"]]
                items2_uids = [item["uid"] for item in result2["items"]]
                
                # Kiểm tra không trùng lặp giữa hai trang
                has_duplicate = any(uid in items2_uids for uid in items1_uids)
                if not has_duplicate:
                    console.print("[bold green]✓ Không có items trùng lặp giữa các trang[/bold green]")
                else:
                    console.print("[bold red]✗ Phát hiện items trùng lặp giữa các trang[/bold red]")
        
        return True
    except requests.exceptions.RequestException as e:
        console.print(f"[bold red]✗ Endpoint: {description} - Lỗi kết nối: {str(e)}[/bold red]")
        return False
    except AssertionError as e:
        console.print(f"[bold red]✗ Endpoint: {description} - Lỗi cấu trúc: {str(e)}[/bold red]")
        return False
    except Exception as e:
        console.print(f"[bold red]✗ Endpoint: {description} - Lỗi không mong đợi: {str(e)}[/bold red]")
        return False

def run_tests():
    """
    Chạy tất cả các test cho các endpoint đã chuẩn hóa pagination
    """
    console.print(Panel(
        Text("KIỂM TRA PAGINATION API", justify="center"),
        style="bold green"
    ))
    
    # Danh sách các endpoint cần kiểm tra
    endpoints = [
        {
            "endpoint": "/api/v1/projects/",
            "description": "Project Listing",
            "params": {}
        },
        {
            "endpoint": "/api/v1/resources/",
            "description": "Resource Listing",
            "params": {}
        },
        {
            "endpoint": "/api/v1/tasks/",
            "description": "Task Listing",
            "params": {"project_id": "get-first-project-id-or-input"}
        },
        {
            "endpoint": "/api/v1/users/",
            "description": "User Listing",
            "params": {}
        }
    ]
    
    # Trước tiên cần lấy ID của một project để test Task API
    try:
        project_response = requests.get(f"{BASE_URL}/api/v1/projects/", params={"page": 1, "page_size": 1})
        project_response.raise_for_status()
        projects = project_response.json()
        
        if projects and "items" in projects and len(projects["items"]) > 0:
            project_id = projects["items"][0]["uid"]
            
            # Cập nhật project_id cho endpoint Task
            for endpoint in endpoints:
                if "project_id" in endpoint["params"]:
                    if endpoint["params"]["project_id"] == "get-first-project-id-or-input":
                        endpoint["params"]["project_id"] = project_id
                        console.print(f"[green]Tìm thấy Project ID: {project_id} để kiểm tra Task API[/green]\n")
        else:
            console.print("[yellow]Không tìm thấy project nào. Task API test có thể thất bại.[/yellow]\n")
            
    except Exception as e:
        console.print(f"[yellow]Không thể lấy project ID: {str(e)}[/yellow]\n")
        
    # Chạy test cho từng endpoint
    results = []
    for endpoint_info in endpoints:
        result = test_pagination_endpoint(
            endpoint_info["endpoint"],
            endpoint_info["description"],
            endpoint_info["params"]
        )
        results.append((endpoint_info["description"], result))
    
    # Hiển thị kết quả tổng hợp
    summary_table = Table(title="\nKẾT QUẢ KIỂM TRA", show_header=True, header_style="bold")
    summary_table.add_column("Endpoint")
    summary_table.add_column("Kết quả")
    
    all_passed = True
    for name, passed in results:
        status = "[green]PASSED[/green]" if passed else "[red]FAILED[/red]"
        summary_table.add_row(name, status)
        if not passed:
            all_passed = False
    
    console.print(summary_table)
    
    if all_passed:
        console.print(Panel(
            Text("TẤT CẢ TEST ĐỀU THÀNH CÔNG", justify="center"),
            style="bold green"
        ))
    else:
        console.print(Panel(
            Text("MỘT SỐ TEST THẤT BẠI", justify="center"),
            style="bold red"
        ))

if __name__ == "__main__":
    run_tests()
