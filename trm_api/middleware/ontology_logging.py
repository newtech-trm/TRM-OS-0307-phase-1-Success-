from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import logging
import json
import time
from typing import Callable, Dict, Any, Optional
from trm_api.core.config import settings

# Thiết lập logger riêng cho ontology validation
ontology_logger = logging.getLogger("trm_api.ontology")
ontology_logger.setLevel(logging.INFO)

# File handler cho ontology validation logs
if not ontology_logger.handlers:
    file_handler = logging.FileHandler("ontology_validation.log")
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    ontology_logger.addHandler(file_handler)

class OntologyLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware để ghi log các trường hợp data không nhất quán với ontology.
    
    Middleware này sẽ bắt các lỗi từ các adapter và ghi log chi tiết để
    giúp phát hiện và sửa lỗi dữ liệu không nhất quán với ontology.
    """
    
    def __init__(
        self, 
        app: Callable,
        log_request_body: bool = True,
        log_response_body: bool = True,
        log_processing_time: bool = True,
        log_path_prefixes: Optional[list] = None,
    ):
        super().__init__(app)
        self.log_request_body = log_request_body
        self.log_response_body = log_response_body
        self.log_processing_time = log_processing_time
        self.log_path_prefixes = log_path_prefixes or ["/api/v1"]
    
    async def dispatch(self, request: Request, call_next):
        # Chỉ log các request đến API endpoints
        should_log = any(request.url.path.startswith(prefix) for prefix in self.log_path_prefixes)
        
        if not should_log:
            return await call_next(request)
        
        # Log request details
        request_id = str(time.time())
        log_data = {
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "client_ip": request.client.host if request.client else "unknown",
        }
        
        # Bắt đầu đo thời gian xử lý
        start_time = time.time()
        
        # Log request body nếu cần
        if self.log_request_body and request.method in ["POST", "PUT", "PATCH"]:
            try:
                # Clone request để đọc body mà không ảnh hưởng đến xử lý sau này
                body = await request.body()
                # Cố gắng parse body là JSON và log
                try:
                    body_json = json.loads(body)
                    log_data["request_body"] = body_json
                except json.JSONDecodeError:
                    log_data["request_body"] = "[Non-JSON body]"
            except Exception as e:
                log_data["request_body_error"] = str(e)
        
        # Thực hiện request và bắt response
        try:
            response = await call_next(request)
        except Exception as e:
            # Log errors trong quá trình xử lý
            end_time = time.time()
            log_data["error"] = str(e)
            log_data["error_type"] = e.__class__.__name__
            
            if self.log_processing_time:
                log_data["processing_time_ms"] = round((end_time - start_time) * 1000, 2)
                
            ontology_logger.error(
                f"Error processing request: {json.dumps(log_data)}"
            )
            raise  # Re-raise để FastAPI xử lý
            
        # Log response details
        end_time = time.time()
        log_data["status_code"] = response.status_code
        
        if self.log_processing_time:
            log_data["processing_time_ms"] = round((end_time - start_time) * 1000, 2)
        
        # Log response body cho HTTP errors (4xx, 5xx) và các adapter validation errors (422)
        if self.log_response_body and (response.status_code >= 400 or "/validate/" in request.url.path):
            response_body = b""
            async for chunk in response.body_iterator:
                response_body += chunk
            
            try:
                response_json = json.loads(response_body.decode())
                log_data["response_body"] = response_json
                
                # Phát hiện và log các lỗi liên quan đến ontology
                if response.status_code == 422:
                    ontology_logger.warning(
                        f"Ontology validation error: {json.dumps(log_data)}"
                    )
                elif response.status_code >= 400 and response.status_code < 500:
                    ontology_logger.info(
                        f"Client error: {json.dumps(log_data)}"
                    )
                elif response.status_code >= 500:
                    ontology_logger.error(
                        f"Server error: {json.dumps(log_data)}"
                    )
            except json.JSONDecodeError:
                log_data["response_body"] = "[Non-JSON body]"
            
            # Tạo lại response để FastAPI có thể trả về
            return Response(
                content=response_body,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.media_type
            )
        
        # Log validation results từ validate endpoints
        if request.url.path.startswith("/api/v1/validate"):
            if response.status_code == 200:
                ontology_logger.info(
                    f"Ontology validation: {json.dumps(log_data)}"
                )
        
        return response
