import json
import pytest
from unittest.mock import patch, Mock, AsyncMock
from datetime import datetime

from fastapi import Response
from fastapi.responses import JSONResponse

from trm_api.adapters.decorators import (
    adapt_response,
    adapt_datetime_response,
    adapt_win_response,
    adapt_recognition_response,
    adapt_task_response,
    adapt_knowledge_snippet_response,
    adapt_ontology_response,
    _process_items
)

class TestDecorators:
    """Unit tests cho decorators adapter module."""
    
    @pytest.mark.asyncio
    async def test_adapt_response_with_dict(self):
        """Test adapt_response với response là dict."""
        # Mock endpoint function trả về dict đơn giản
        async def mock_endpoint():
            return {"id": "123", "created_at": datetime(2023, 1, 15, 10, 30, 0)}
        
        # Áp dụng decorator
        decorated_endpoint = adapt_response()(mock_endpoint)
        
        # Gọi endpoint và kiểm tra kết quả
        result = await decorated_endpoint()
        print(f"\nDEBUG - result: {result}")
        print(f"DEBUG - result type: {type(result)}")
        if isinstance(result, dict) and "created_at" in result:
            print(f"DEBUG - created_at: {result['created_at']}")
            print(f"DEBUG - created_at type: {type(result['created_at'])}")
        
        # Kiểm tra kết quả
        assert result["id"] == "123", f"Expected id='123' but got {result.get('id')}"
        assert result["created_at"] == "2023-01-15T10:30:00", f"Expected created_at='2023-01-15T10:30:00' but got {result.get('created_at')}"
    
    @pytest.mark.asyncio
    async def test_adapt_response_with_response_item_key(self):
        """Test adapt_response với response_item_key."""
        # Mock endpoint function trả về dict có chứa danh sách items
        async def mock_endpoint():
            return {
                "items": [
                    {"id": "1", "created_at": datetime(2023, 1, 15, 10, 30, 0)},
                    {"id": "2", "created_at": datetime(2023, 1, 15, 11, 30, 0)},
                ],
                "total": 2
            }
        
        # Áp dụng decorator
        decorated_endpoint = adapt_response(response_item_key="items")(mock_endpoint)
        
        # Gọi endpoint và kiểm tra kết quả
        result = await decorated_endpoint()
        print(f"\nDEBUG - result: {result}")
        print(f"DEBUG - items[0] created_at: {result['items'][0].get('created_at')}")
        print(f"DEBUG - items[0] created_at type: {type(result['items'][0].get('created_at'))}")
        
        # Kiểm tra kết quả
        assert result["total"] == 2, f"Expected total=2 but got {result.get('total')}"
        assert result["items"][0]["created_at"] == "2023-01-15T10:30:00", f"Expected created_at='2023-01-15T10:30:00' but got {result['items'][0].get('created_at')}"
        assert result["items"][1]["created_at"] == "2023-01-15T11:30:00", f"Expected created_at='2023-01-15T11:30:00' but got {result['items'][1].get('created_at')}"
    
    @pytest.mark.asyncio
    async def test_adapt_response_with_json_response(self):
        """Test adapt_response với JSONResponse."""
        # Mock endpoint function trả về JSONResponse
        async def mock_endpoint():
            data = {
                "id": "123",
                "created_at": "2023-01-15 10:30:00",  # string cần chuẩn hóa
            }
            return JSONResponse(content=data)
        
        # Áp dụng decorator
        decorated_endpoint = adapt_response()(mock_endpoint)
        
        # Patch json.loads để giả lập parse response body
        with patch("json.loads") as mock_loads:
            mock_loads.return_value = {"id": "123", "created_at": "2023-01-15 10:30:00"}
            
            # Gọi endpoint
            result = await decorated_endpoint()
            
            # Kiểm tra kết quả
            assert isinstance(result, JSONResponse)
            mock_loads.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_adapt_response_with_enums(self):
        """Test adapt_response với adapt_enums."""
        # Mock adapter function
        def mock_status_adapter(value):
            if value == "DRAFT":
                return "draft"
            return value
        
        # Mock endpoint function
        async def mock_endpoint():
            return {"id": "123", "status": "DRAFT"}
        
        # Áp dụng decorator với adapt_enums
        decorated_endpoint = adapt_response(
            adapt_datetime=False,
            adapt_enums=[{"field": "status", "adapter": mock_status_adapter}]
        )(mock_endpoint)
        
        # Gọi endpoint và kiểm tra kết quả
        result = await decorated_endpoint()
        assert result["id"] == "123"
        assert result["status"] == "draft"
    
    @pytest.mark.asyncio
    async def test_adapt_datetime_response(self):
        """Test adapt_datetime_response decorator."""
        # Mock endpoint function
        async def mock_endpoint():
            return {"id": "123", "created_at": datetime(2023, 1, 15, 10, 30, 0)}
        
        # Áp dụng decorator
        decorated_endpoint = adapt_datetime_response()(mock_endpoint)
        
        # Gọi endpoint và kiểm tra kết quả
        result = await decorated_endpoint()
        print(f"\nDEBUG - datetime result: {result}")
        print(f"DEBUG - datetime created_at: {result.get('created_at')}")
        print(f"DEBUG - datetime created_at type: {type(result.get('created_at'))}")
        
        # Kiểm tra kết quả
        assert result["id"] == "123", f"Expected id='123' but got {result.get('id')}"
        assert result["created_at"] == "2023-01-15T10:30:00", f"Expected created_at='2023-01-15T10:30:00' but got {result.get('created_at')}"
    
    @pytest.mark.asyncio
    async def test_adapt_win_response(self):
        """Test adapt_win_response decorator."""
        # Mock endpoint function
        async def mock_endpoint():
            return {
                "id": "123",
                "status": "DRAFT",
                "winType": "Problem Resolution",
                "created_at": datetime(2023, 1, 15, 10, 30, 0)
            }
        
        # Patch normalize functions
        with patch("trm_api.adapters.enum_adapter.normalize_win_status") as mock_status:
            with patch("trm_api.adapters.enum_adapter.normalize_win_type") as mock_type:
                mock_status.return_value = "draft"
                mock_type.return_value = "problem_resolution"
                
                # Áp dụng decorator
                decorated_endpoint = adapt_win_response()(mock_endpoint)
                
                # Gọi endpoint và kiểm tra kết quả
                result = await decorated_endpoint()
                print(f"\nDEBUG - win result: {result}")
                print(f"DEBUG - win created_at: {result.get('created_at')}")
                print(f"DEBUG - win status: {result.get('status')}")
                
                # Kiểm tra kết quả
                assert result["id"] == "123", f"Expected id='123' but got {result.get('id')}"
                assert result["status"] == "draft", f"Expected status='draft' but got {result.get('status')}"
                assert result["winType"] == "problem_resolution", f"Expected winType='problem_resolution' but got {result.get('winType')}"
                assert result["created_at"] == "2023-01-15T10:30:00", f"Expected created_at='2023-01-15T10:30:00' but got {result.get('created_at')}"
                
                # Verify mocks were called
                mock_status.assert_called_once_with("DRAFT")
                mock_type.assert_called_once_with("Problem Resolution")
    
    @pytest.mark.asyncio
    async def test_adapt_recognition_response(self):
        """Test adapt_recognition_response decorator."""
        # Mock endpoint function
        async def mock_endpoint():
            return {
                "id": "123",
                "status": "DRAFT",
                "recognitionType": "Kudos",
                "created_at": datetime(2023, 1, 15, 10, 30, 0)
            }
        
        # Patch normalize functions
        with patch("trm_api.adapters.enum_adapter.normalize_recognition_status") as mock_status:
            with patch("trm_api.adapters.enum_adapter.normalize_recognition_type") as mock_type:
                mock_status.return_value = "draft"
                mock_type.return_value = "kudos"
                
                # Áp dụng decorator
                decorated_endpoint = adapt_recognition_response()(mock_endpoint)
                
                # Gọi endpoint và kiểm tra kết quả
                result = await decorated_endpoint()
                print(f"\nDEBUG - recognition result: {result}")
                print(f"DEBUG - recognition created_at: {result.get('created_at')}")
                print(f"DEBUG - recognition recognitionType: {result.get('recognitionType')}")
                
                # Kiểm tra kết quả
                assert result["id"] == "123", f"Expected id='123' but got {result.get('id')}"
                assert result["status"] == "draft", f"Expected status='draft' but got {result.get('status')}"
                assert result["recognitionType"] == "kudos", f"Expected recognitionType='kudos' but got {result.get('recognitionType')}"
                assert result["created_at"] == "2023-01-15T10:30:00", f"Expected created_at='2023-01-15T10:30:00' but got {result.get('created_at')}"
                
                # Verify mocks were called
                mock_status.assert_called_once_with("DRAFT")
                mock_type.assert_called_once_with("Kudos")
    
    @pytest.mark.asyncio
    async def test_adapt_response_with_error(self):
        """Test adapt_response khi xảy ra lỗi."""
        # Mock endpoint function gây ra exception khi parse JSON
        async def mock_endpoint():
            return JSONResponse(content={"id": "123"})
        
        # Áp dụng decorator
        decorated_endpoint = adapt_response()(mock_endpoint)
        
        # Patch json.loads để giả lập lỗi khi parse
        with patch("json.loads") as mock_loads:
            mock_loads.side_effect = Exception("JSON parse error")
            with patch("logging.error") as mock_log:
                
                # Gọi endpoint
                result = await decorated_endpoint()
                
                # Kiểm tra kết quả
                assert isinstance(result, JSONResponse)
                mock_log.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_adapt_task_response(self):
        """Test adapt_task_response decorator."""
        # Mock endpoint function
        async def mock_endpoint():
            return {
                "id": "123",
                "status": "TODO",
                "task_type": "Feature",
                "created_at": datetime(2023, 1, 15, 10, 30, 0)
            }
        
        # Patch normalize functions
        with patch("trm_api.adapters.enum_adapter.normalize_task_status") as mock_status:
            with patch("trm_api.adapters.enum_adapter.normalize_task_type") as mock_type:
                mock_status.return_value = "todo"
                mock_type.return_value = "feature"
                
                # Áp dụng decorator
                decorated_endpoint = adapt_task_response()(mock_endpoint)
                
                # Gọi endpoint và kiểm tra kết quả
                result = await decorated_endpoint()
                
                # Kiểm tra kết quả
                assert result["id"] == "123", f"Expected id='123' but got {result.get('id')}"
                assert result["status"] == "todo", f"Expected status='todo' but got {result.get('status')}"
                assert result["task_type"] == "feature", f"Expected task_type='feature' but got {result.get('task_type')}"
                assert result["created_at"] == "2023-01-15T10:30:00", f"Expected created_at='2023-01-15T10:30:00' but got {result.get('created_at')}"
                
                # Verify mocks were called
                mock_status.assert_called_once_with("TODO")
                mock_type.assert_called_once_with("Feature")
    
    @pytest.mark.asyncio
    async def test_adapt_knowledge_snippet_response(self):
        """Test adapt_knowledge_snippet_response decorator."""
        # Mock endpoint function
        async def mock_endpoint():
            return {
                "id": "123",
                "snippet_type": "Best Practice",
                "created_at": datetime(2023, 1, 15, 10, 30, 0)
            }
        
        # Patch normalize functions
        with patch("trm_api.adapters.enum_adapter.normalize_knowledge_snippet_type") as mock_type:
            mock_type.return_value = "best_practice"
            
            # Áp dụng decorator
            decorated_endpoint = adapt_knowledge_snippet_response()(mock_endpoint)
            
            # Gọi endpoint và kiểm tra kết quả
            result = await decorated_endpoint()
            
            # Kiểm tra kết quả
            assert result["id"] == "123", f"Expected id='123' but got {result.get('id')}"
            assert result["snippet_type"] == "best_practice", f"Expected snippet_type='best_practice' but got {result.get('snippet_type')}"
            assert result["created_at"] == "2023-01-15T10:30:00", f"Expected created_at='2023-01-15T10:30:00' but got {result.get('created_at')}"
            
            # Verify mocks were called
            mock_type.assert_called_once_with("Best Practice")
    
    @pytest.mark.asyncio
    async def test_adapt_ontology_response_with_win(self):
        """Test adapt_ontology_response decorator với entity_type='win'."""
        # Mock endpoint function
        async def mock_endpoint():
            return {
                "id": "123",
                "status": "DRAFT",
                "winType": "Problem Resolution",
                "created_at": datetime(2023, 1, 15, 10, 30, 0)
            }
        
        # Patch normalize functions
        with patch("trm_api.adapters.enum_adapter.normalize_win_status") as mock_status:
            with patch("trm_api.adapters.enum_adapter.normalize_win_type") as mock_type:
                mock_status.return_value = "draft"
                mock_type.return_value = "problem_resolution"
                
                # Áp dụng decorator
                decorated_endpoint = adapt_ontology_response(entity_type="win")(mock_endpoint)
                
                # Gọi endpoint và kiểm tra kết quả
                result = await decorated_endpoint()
                
                # Kiểm tra kết quả
                assert result["id"] == "123"
                assert result["status"] == "draft"
                assert result["winType"] == "problem_resolution"
                assert result["created_at"] == "2023-01-15T10:30:00"
                
                # Verify mocks were called
                mock_status.assert_called_once_with("DRAFT")
                mock_type.assert_called_once_with("Problem Resolution")
    
    @pytest.mark.asyncio
    async def test_adapt_ontology_response_with_task(self):
        """Test adapt_ontology_response decorator với entity_type='task'."""
        # Mock endpoint function
        async def mock_endpoint():
            return {
                "id": "123",
                "status": "TODO",
                "task_type": "Feature",
                "created_at": datetime(2023, 1, 15, 10, 30, 0)
            }
        
        # Patch normalize functions
        with patch("trm_api.adapters.enum_adapter.normalize_task_status") as mock_status:
            with patch("trm_api.adapters.enum_adapter.normalize_task_type") as mock_type:
                mock_status.return_value = "todo"
                mock_type.return_value = "feature"
                
                # Áp dụng decorator
                decorated_endpoint = adapt_ontology_response(entity_type="task")(mock_endpoint)
                
                # Gọi endpoint và kiểm tra kết quả
                result = await decorated_endpoint()
                
                # Kiểm tra kết quả
                assert result["id"] == "123"
                assert result["status"] == "todo"
                assert result["task_type"] == "feature"
                assert result["created_at"] == "2023-01-15T10:30:00"
                
                # Verify mocks were called
                mock_status.assert_called_once_with("TODO")
                mock_type.assert_called_once_with("Feature")
    
    @pytest.mark.asyncio
    async def test_adapt_ontology_response_with_custom_adapters(self):
        """Test adapt_ontology_response decorator với custom_adapters."""
        # Mock adapter function
        def mock_priority_adapter(value):
            priorities = {"1": "high", "2": "medium", "3": "low"}
            return priorities.get(value, value)
            
        # Mock endpoint function
        async def mock_endpoint():
            return {
                "id": "123",
                "priority": "1",
                "created_at": datetime(2023, 1, 15, 10, 30, 0)
            }
        
        # Áp dụng decorator với custom adapter
        custom_adapters = [{"field": "priority", "adapter": mock_priority_adapter}]
        decorated_endpoint = adapt_ontology_response(
            entity_type=None, custom_adapters=custom_adapters
        )(mock_endpoint)
        
        # Gọi endpoint và kiểm tra kết quả
        result = await decorated_endpoint()
        
        # Kiểm tra kết quả
        assert result["id"] == "123"
        assert result["priority"] == "high"  # Đã được chuyển đổi bởi custom adapter
        assert result["created_at"] == "2023-01-15T10:30:00"
