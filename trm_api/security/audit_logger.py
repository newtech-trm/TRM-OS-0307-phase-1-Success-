"""
Audit Logging System cho TRM-OS Phase 3

Comprehensive audit logging cho:
- Security events tracking
- User activity monitoring
- System access logging
- Compliance reporting
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json
from uuid import uuid4

logger = logging.getLogger(__name__)


class SecurityEventType(Enum):
    """Types of security events"""
    LOGIN_SUCCESS = "login_success"
    LOGIN_FAILED = "login_failed"
    LOGOUT = "logout"
    PERMISSION_GRANTED = "permission_granted"
    PERMISSION_DENIED = "permission_denied"
    PASSWORD_CHANGE = "password_change"
    MFA_ENABLED = "mfa_enabled"
    MFA_DISABLED = "mfa_disabled"
    ROLE_ASSIGNED = "role_assigned"
    ROLE_REMOVED = "role_removed"
    SUSPICIOUS_ACTIVITY = "suspicious_activity"
    SYSTEM_ACCESS = "system_access"


@dataclass
class SecurityEvent:
    """Security event record"""
    event_id: str = field(default_factory=lambda: str(uuid4()))
    event_type: SecurityEventType = SecurityEventType.SYSTEM_ACCESS
    user_id: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    resource: Optional[str] = None
    action: Optional[str] = None
    success: bool = True
    details: Dict[str, Any] = field(default_factory=dict)
    risk_level: str = "low"  # low, medium, high, critical


class AuditLogger:
    """Main audit logging system"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.events: List[SecurityEvent] = []
        self.max_events = 10000  # Keep last 10k events in memory
    
    async def log_event(self, event: SecurityEvent) -> None:
        """Log security event"""
        try:
            # Add to in-memory storage
            self.events.append(event)
            
            # Maintain max events limit
            if len(self.events) > self.max_events:
                self.events = self.events[-self.max_events:]
            
            # Log to standard logger
            self.logger.info(f"Security Event: {event.event_type.value} - "
                           f"User: {event.user_id} - Success: {event.success}")
            
        except Exception as e:
            self.logger.error(f"Failed to log security event: {e}")
    
    async def log_login_success(self, user_id: str, ip_address: str, 
                              user_agent: str, session_id: str) -> None:
        """Log successful login"""
        event = SecurityEvent(
            event_type=SecurityEventType.LOGIN_SUCCESS,
            user_id=user_id,
            ip_address=ip_address,
            user_agent=user_agent,
            success=True,
            details={"session_id": session_id},
            risk_level="low"
        )
        await self.log_event(event)
    
    async def log_login_failed(self, user_id: str, ip_address: str, 
                             user_agent: str, reason: str) -> None:
        """Log failed login"""
        event = SecurityEvent(
            event_type=SecurityEventType.LOGIN_FAILED,
            user_id=user_id,
            ip_address=ip_address,
            user_agent=user_agent,
            success=False,
            details={"reason": reason},
            risk_level="medium"
        )
        await self.log_event(event)
    
    def get_events(self, user_id: Optional[str] = None, 
                  event_type: Optional[SecurityEventType] = None,
                  limit: int = 100) -> List[SecurityEvent]:
        """Get filtered security events"""
        filtered_events = self.events
        
        if user_id:
            filtered_events = [e for e in filtered_events if e.user_id == user_id]
        
        if event_type:
            filtered_events = [e for e in filtered_events if e.event_type == event_type]
        
        # Sort by timestamp (newest first)
        filtered_events.sort(key=lambda x: x.timestamp, reverse=True)
        
        return filtered_events[:limit]


class SecurityEventLogger:
    """Specialized security event logger"""
    
    def __init__(self):
        self.audit_logger = AuditLogger()
    
    async def log_permission_check(self, user_id: str, resource: str, 
                                 action: str, granted: bool, reason: str) -> None:
        """Log permission check event"""
        event_type = SecurityEventType.PERMISSION_GRANTED if granted else SecurityEventType.PERMISSION_DENIED
        risk_level = "low" if granted else "medium"
        
        event = SecurityEvent(
            event_type=event_type,
            user_id=user_id,
            resource=resource,
            action=action,
            success=granted,
            details={"reason": reason},
            risk_level=risk_level
        )
        
        await self.audit_logger.log_event(event)
    
    async def log_suspicious_activity(self, user_id: str, activity: str, 
                                    ip_address: str, details: Dict[str, Any]) -> None:
        """Log suspicious activity"""
        event = SecurityEvent(
            event_type=SecurityEventType.SUSPICIOUS_ACTIVITY,
            user_id=user_id,
            ip_address=ip_address,
            success=False,
            details={"activity": activity, **details},
            risk_level="high"
        )
        
        await self.audit_logger.log_event(event) 