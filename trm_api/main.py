import sys
import os
import datetime

LOG_FILE = "uvicorn_startup_log.txt"

def log_to_file(message):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{datetime.datetime.now()}: {message}\n")

log_to_file("--- Uvicorn/FastAPI Startup --- ")
log_to_file(f"PYTHON_EXECUTABLE_IN_MAIN: {sys.executable}")
log_to_file(f"SYS_PATH_IN_MAIN: {sys.path}")
log_to_file(f"CURRENT_WORKING_DIRECTORY_IN_MAIN: {os.getcwd()}")
log_to_file(f"PYTHONPATH: {os.environ.get('PYTHONPATH')}")
log_to_file(f"VIRTUAL_ENV: {os.environ.get('VIRTUAL_ENV')}")

from fastapi import FastAPI
from contextlib import asynccontextmanager
from trm_api.core.config import settings
from trm_api.db.session import connect_to_db, close_db_connection
from trm_api.core.logging_config import setup_logging
from trm_api.middleware.ontology_logging import OntologyLoggingMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Actions on startup
    setup_logging()
    print("--- Server starting up ---")
    connect_to_db()
    yield
    # Actions on shutdown
    print("--- Server shutting down ---")
    close_db_connection()

# Initialize the FastAPI app with the lifespan manager
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# Thêm middleware để ghi log các trường hợp data không nhất quán
app.add_middleware(
    OntologyLoggingMiddleware,
    log_request_body=True,
    log_response_body=True,
    log_processing_time=True,
    log_path_prefixes=["/api/v1/validate", "/api/v1/wins", "/api/v1/recognitions", "/api/v1/events", "/api/v1/tasks", "/api/v1/knowledge-snippets"]
)

@app.get("/", tags=["Root"])
def read_root():
    """
    Welcome endpoint.
    """
    return {"message": f"Welcome to {settings.PROJECT_NAME}"}

@app.get("/health", tags=["Health Check"])
def health_check():
    """
    Health check endpoint to verify the service is running.
    """
    return {"status": "ok"}

# Include the main API router
from trm_api.api.v1.api import api_router
app.include_router(api_router, prefix=settings.API_V1_STR)

# Kết thúc khởi động server khi chạy trực tiếp (python -m trm_api.main)
if __name__ == "__main__":
    import uvicorn
    import logging
    
    # Cấu hình logging chi tiết hơn
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # Bật logging cho neomodel (xem log truy vấn Neo4j)
    neomodel_logger = logging.getLogger('neomodel')
    neomodel_logger.setLevel(logging.DEBUG)
    
    print(f"[TRM API] Khởi động server trên cổng 8001 với logging cấp độ DEBUG")
    uvicorn.run(app, host="127.0.0.1", port=8001, log_level="debug")
