#!/usr/bin/env python3
"""
Simple MCP Conversational Coordinator for Testing
===============================================

Version đơn giản để test MCP Conversational Intelligence
"""

import asyncio
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime

from trm_api.core.logging_config import get_logger

logger = get_logger(__name__)


@dataclass
class SimpleMCPResult:
    """Simple MCP result for testing"""
    success: bool
    message: str
    operation: str
    execution_time: float


class SimpleMCPCoordinator:
    """Simple MCP coordinator cho testing"""
    
    def __init__(self):
        self.initialized = True
        logger.info("Simple MCP Coordinator initialized")
    
    async def process_simple_request(self, message: str) -> SimpleMCPResult:
        """Process simple MCP request"""
        start_time = datetime.now()
        
        try:
            # Add small delay to simulate processing time
            await asyncio.sleep(0.001)  # 1ms delay
            
            # Simple pattern matching
            if "snowflake" in message.lower():
                operation = "snowflake_query"
                response = "Kết nối Snowflake thành công"
            elif "rabbitmq" in message.lower():
                operation = "rabbitmq_send"
                response = "Gửi tin nhắn RabbitMQ thành công"
            elif any(word in message.lower() for word in ["status", "trạng thái", "hệ thống"]):
                operation = "health_check"
                response = "Trạng thái hệ thống: Tốt"
            else:
                operation = "unknown"
                response = "Không hiểu yêu cầu"
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return SimpleMCPResult(
                success=True,
                message=response,
                operation=operation,
                execution_time=execution_time
            )
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            return SimpleMCPResult(
                success=False,
                message=f"Lỗi: {str(e)}",
                operation="error",
                execution_time=execution_time
            )
    
    def get_supported_operations(self) -> List[str]:
        """Get list of supported operations"""
        return [
            "snowflake_query",
            "rabbitmq_send", 
            "health_check"
        ] 