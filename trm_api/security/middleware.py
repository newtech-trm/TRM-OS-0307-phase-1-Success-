"""
Security Middleware cho TRM-OS Phase 3

Security middleware components cho:
- Request validation
- Rate limiting
- Security headers
- Input sanitization
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import re

logger = logging.getLogger(__name__)


class SecurityMiddleware:
    """Main security middleware"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.rate_limiter = RateLimiter()
        self.request_validator = RequestValidator()
    
    async def process_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process request through security middleware"""
        try:
            # Rate limiting
            if not await self.rate_limiter.check_rate_limit(request_data.get('ip_address', '')):
                return {'error': 'Rate limit exceeded', 'status': 429}
            
            # Request validation
            validation_result = await self.request_validator.validate_request(request_data)
            if not validation_result['valid']:
                return {'error': validation_result['error'], 'status': 400}
            
            return {'status': 200, 'processed': True}
            
        except Exception as e:
            self.logger.error(f"Security middleware processing failed: {e}")
            return {'error': 'Security processing failed', 'status': 500}


class RateLimiter:
    """Rate limiting implementation"""
    
    def __init__(self):
        self.requests: Dict[str, List[datetime]] = {}
        self.max_requests = 100  # per window
        self.window_minutes = 15
    
    async def check_rate_limit(self, identifier: str) -> bool:
        """Check if request is within rate limit"""
        try:
            now = datetime.utcnow()
            window_start = now - timedelta(minutes=self.window_minutes)
            
            # Get requests for identifier
            if identifier not in self.requests:
                self.requests[identifier] = []
            
            # Remove old requests
            self.requests[identifier] = [
                req_time for req_time in self.requests[identifier]
                if req_time > window_start
            ]
            
            # Check limit
            if len(self.requests[identifier]) >= self.max_requests:
                return False
            
            # Add current request
            self.requests[identifier].append(now)
            return True
            
        except Exception as e:
            logger.error(f"Rate limiting check failed: {e}")
            return True  # Allow on error


class RequestValidator:
    """Request validation utilities"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    async def validate_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate incoming request"""
        try:
            # Basic validation
            if not request_data:
                return {'valid': False, 'error': 'Empty request data'}
            
            # Sanitize inputs
            sanitized_data = self._sanitize_inputs(request_data)
            
            return {'valid': True, 'sanitized_data': sanitized_data}
            
        except Exception as e:
            self.logger.error(f"Request validation failed: {e}")
            return {'valid': False, 'error': 'Validation error'}
    
    def _sanitize_inputs(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitize input data"""
        sanitized = {}
        
        for key, value in data.items():
            if isinstance(value, str):
                # Remove potentially dangerous characters
                sanitized_value = re.sub(r'[<>"\']', '', value)
                sanitized[key] = sanitized_value
            else:
                sanitized[key] = value
        
        return sanitized 