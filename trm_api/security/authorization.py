"""
Enterprise Authorization System cho TRM-OS Phase 3

Advanced authorization với:
- Role-Based Access Control (RBAC)
- Attribute-Based Access Control (ABAC)
- Dynamic policy evaluation
- Permission inheritance
- Resource-level access control
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Set, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json
from uuid import uuid4

logger = logging.getLogger(__name__)


class ActionType(Enum):
    """Types of actions trong authorization system"""
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    EXECUTE = "execute"
    MANAGE = "manage"
    ADMIN = "admin"


class ResourceType(Enum):
    """Types of resources"""
    USER = "user"
    PROJECT = "project"
    TASK = "task"
    AGENT = "agent"
    TENSION = "tension"
    SYSTEM = "system"
    API = "api"
    DATA = "data"


@dataclass
class Permission:
    """Individual permission"""
    permission_id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    description: str = ""
    resource_type: ResourceType = ResourceType.SYSTEM
    action: ActionType = ActionType.READ
    conditions: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Role:
    """Role với permissions"""
    role_id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    description: str = ""
    permissions: List[Permission] = field(default_factory=list)
    parent_roles: List[str] = field(default_factory=list)  # Role inheritance
    is_system_role: bool = False
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class User:
    """User với roles và permissions"""
    user_id: str
    username: str
    email: str
    roles: List[str] = field(default_factory=list)  # Role IDs
    direct_permissions: List[Permission] = field(default_factory=list)
    attributes: Dict[str, Any] = field(default_factory=dict)
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class AccessRequest:
    """Request cho access authorization"""
    user_id: str
    resource_type: ResourceType
    resource_id: Optional[str] = None
    action: ActionType = ActionType.READ
    context: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class AccessResult:
    """Kết quả authorization"""
    granted: bool
    user_id: str
    resource_type: ResourceType
    action: ActionType
    reason: str = ""
    matched_permissions: List[str] = field(default_factory=list)
    policy_violations: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.utcnow)


class PolicyEngine:
    """Engine cho dynamic policy evaluation"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.policies: Dict[str, Dict[str, Any]] = {}
    
    def add_policy(self, policy_id: str, policy: Dict[str, Any]) -> None:
        """Add policy to engine"""
        self.policies[policy_id] = {
            **policy,
            'created_at': datetime.utcnow()
        }
    
    def evaluate_policy(self, policy_id: str, context: Dict[str, Any]) -> bool:
        """Evaluate policy với given context"""
        try:
            if policy_id not in self.policies:
                return False
            
            policy = self.policies[policy_id]
            conditions = policy.get('conditions', {})
            
            # Simple policy evaluation (would be more complex in production)
            for key, expected_value in conditions.items():
                actual_value = context.get(key)
                
                if isinstance(expected_value, dict):
                    # Handle complex conditions
                    operator = expected_value.get('operator', 'eq')
                    value = expected_value.get('value')
                    
                    if operator == 'eq' and actual_value != value:
                        return False
                    elif operator == 'ne' and actual_value == value:
                        return False
                    elif operator == 'gt' and (actual_value is None or actual_value <= value):
                        return False
                    elif operator == 'lt' and (actual_value is None or actual_value >= value):
                        return False
                    elif operator == 'in' and actual_value not in value:
                        return False
                    elif operator == 'contains' and value not in str(actual_value):
                        return False
                else:
                    # Simple equality check
                    if actual_value != expected_value:
                        return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Policy evaluation failed: {e}")
            return False
    
    def get_applicable_policies(self, resource_type: ResourceType, 
                              action: ActionType) -> List[str]:
        """Get policies applicable to resource và action"""
        applicable = []
        
        for policy_id, policy in self.policies.items():
            policy_resource = policy.get('resource_type')
            policy_action = policy.get('action')
            
            # Check if policy applies
            if (policy_resource == resource_type.value or policy_resource == '*') and \
               (policy_action == action.value or policy_action == '*'):
                applicable.append(policy_id)
        
        return applicable


class RBACManager:
    """Role-Based Access Control Manager"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.roles: Dict[str, Role] = {}
        self.users: Dict[str, User] = {}
        self.permissions: Dict[str, Permission] = {}
        
        # Initialize default roles và permissions
        self._initialize_default_roles()
    
    def _initialize_default_roles(self) -> None:
        """Initialize default system roles"""
        
        # Admin permissions
        admin_permissions = [
            Permission(name="system.admin", description="Full system access", 
                      resource_type=ResourceType.SYSTEM, action=ActionType.ADMIN),
            Permission(name="user.manage", description="Manage users",
                      resource_type=ResourceType.USER, action=ActionType.MANAGE),
            Permission(name="project.manage", description="Manage projects",
                      resource_type=ResourceType.PROJECT, action=ActionType.MANAGE)
        ]
        
        # Manager permissions
        manager_permissions = [
            Permission(name="project.create", description="Create projects",
                      resource_type=ResourceType.PROJECT, action=ActionType.CREATE),
            Permission(name="project.read", description="Read projects",
                      resource_type=ResourceType.PROJECT, action=ActionType.READ),
            Permission(name="project.update", description="Update projects",
                      resource_type=ResourceType.PROJECT, action=ActionType.UPDATE),
            Permission(name="user.read", description="Read user information",
                      resource_type=ResourceType.USER, action=ActionType.READ)
        ]
        
        # User permissions
        user_permissions = [
            Permission(name="project.read", description="Read assigned projects",
                      resource_type=ResourceType.PROJECT, action=ActionType.READ),
            Permission(name="task.create", description="Create tasks",
                      resource_type=ResourceType.TASK, action=ActionType.CREATE),
            Permission(name="task.update", description="Update own tasks",
                      resource_type=ResourceType.TASK, action=ActionType.UPDATE)
        ]
        
        # Create roles
        self.create_role("admin", "System Administrator", admin_permissions, is_system_role=True)
        self.create_role("manager", "Project Manager", manager_permissions, is_system_role=True)
        self.create_role("user", "Regular User", user_permissions, is_system_role=True)
        
        self.logger.info("Default RBAC roles initialized")
    
    def create_role(self, name: str, description: str, permissions: List[Permission],
                   parent_roles: List[str] = None, is_system_role: bool = False) -> Role:
        """Create new role"""
        try:
            role = Role(
                name=name,
                description=description,
                permissions=permissions,
                parent_roles=parent_roles or [],
                is_system_role=is_system_role
            )
            
            self.roles[role.role_id] = role
            
            # Store permissions
            for permission in permissions:
                self.permissions[permission.permission_id] = permission
            
            self.logger.info(f"Role created: {name}")
            return role
            
        except Exception as e:
            self.logger.error(f"Role creation failed: {e}")
            raise
    
    def assign_role_to_user(self, user_id: str, role_name: str) -> bool:
        """Assign role to user"""
        try:
            # Find role by name
            role = self.get_role_by_name(role_name)
            if not role:
                self.logger.error(f"Role not found: {role_name}")
                return False
            
            # Get or create user
            if user_id not in self.users:
                self.users[user_id] = User(
                    user_id=user_id,
                    username=user_id,
                    email=f"{user_id}@example.com"
                )
            
            user = self.users[user_id]
            
            # Add role if not already assigned
            if role.role_id not in user.roles:
                user.roles.append(role.role_id)
                self.logger.info(f"Role {role_name} assigned to user {user_id}")
                return True
            
            return True
            
        except Exception as e:
            self.logger.error(f"Role assignment failed: {e}")
            return False
    
    def remove_role_from_user(self, user_id: str, role_name: str) -> bool:
        """Remove role từ user"""
        try:
            role = self.get_role_by_name(role_name)
            if not role:
                return False
            
            if user_id in self.users:
                user = self.users[user_id]
                if role.role_id in user.roles:
                    user.roles.remove(role.role_id)
                    self.logger.info(f"Role {role_name} removed from user {user_id}")
                    return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Role removal failed: {e}")
            return False
    
    def get_role_by_name(self, role_name: str) -> Optional[Role]:
        """Get role by name"""
        for role in self.roles.values():
            if role.name == role_name:
                return role
        return None
    
    def get_user_permissions(self, user_id: str) -> List[Permission]:
        """Get tất cả permissions cho user (including inherited)"""
        if user_id not in self.users:
            return []
        
        user = self.users[user_id]
        all_permissions = []
        
        # Add direct permissions
        all_permissions.extend(user.direct_permissions)
        
        # Add role permissions (with inheritance)
        for role_id in user.roles:
            if role_id in self.roles:
                role_permissions = self._get_role_permissions_recursive(role_id)
                all_permissions.extend(role_permissions)
        
        # Remove duplicates
        unique_permissions = {}
        for perm in all_permissions:
            key = f"{perm.resource_type.value}:{perm.action.value}"
            if key not in unique_permissions:
                unique_permissions[key] = perm
        
        return list(unique_permissions.values())
    
    def _get_role_permissions_recursive(self, role_id: str, visited: Set[str] = None) -> List[Permission]:
        """Get role permissions với inheritance"""
        if visited is None:
            visited = set()
        
        if role_id in visited or role_id not in self.roles:
            return []
        
        visited.add(role_id)
        role = self.roles[role_id]
        permissions = list(role.permissions)
        
        # Add parent role permissions
        for parent_role_id in role.parent_roles:
            parent_permissions = self._get_role_permissions_recursive(parent_role_id, visited)
            permissions.extend(parent_permissions)
        
        return permissions
    
    def has_permission(self, user_id: str, resource_type: ResourceType, 
                      action: ActionType, resource_id: str = None) -> bool:
        """Check if user has specific permission"""
        user_permissions = self.get_user_permissions(user_id)
        
        for permission in user_permissions:
            if (permission.resource_type == resource_type and 
                permission.action == action):
                
                # Check resource-specific conditions
                if permission.conditions:
                    context = {
                        'user_id': user_id,
                        'resource_id': resource_id,
                        'resource_type': resource_type.value,
                        'action': action.value
                    }
                    
                    # Simple condition checking (would be more sophisticated)
                    if not self._evaluate_conditions(permission.conditions, context):
                        continue
                
                return True
        
        return False
    
    def _evaluate_conditions(self, conditions: Dict[str, Any], context: Dict[str, Any]) -> bool:
        """Evaluate permission conditions"""
        try:
            for key, expected_value in conditions.items():
                actual_value = context.get(key)
                
                if isinstance(expected_value, dict):
                    # Handle complex conditions
                    operator = expected_value.get('operator', 'eq')
                    value = expected_value.get('value')
                    
                    if operator == 'eq' and actual_value != value:
                        return False
                    elif operator == 'ne' and actual_value == value:
                        return False
                    elif operator == 'owner' and actual_value != context.get('user_id'):
                        return False
                else:
                    if actual_value != expected_value:
                        return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Condition evaluation failed: {e}")
            return False


class AuthorizationEngine:
    """Main authorization engine"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.rbac_manager = RBACManager()
        self.policy_engine = PolicyEngine()
        
        # Access history cho auditing
        self.access_history: List[AccessResult] = []
        
        # Initialize default policies
        self._initialize_default_policies()
    
    def _initialize_default_policies(self) -> None:
        """Initialize default security policies"""
        
        # Time-based access policy
        self.policy_engine.add_policy("business_hours", {
            "name": "Business Hours Access",
            "description": "Allow access only during business hours",
            "resource_type": "*",
            "action": "*",
            "conditions": {
                "hour": {"operator": "gte", "value": 9},
                "hour_max": {"operator": "lte", "value": 17}
            }
        })
        
        # IP-based access policy
        self.policy_engine.add_policy("trusted_networks", {
            "name": "Trusted Networks Only",
            "description": "Allow access only from trusted networks",
            "resource_type": "system",
            "action": "admin",
            "conditions": {
                "ip_address": {"operator": "in", "value": ["192.168.1.0/24", "10.0.0.0/8"]}
            }
        })
        
        self.logger.info("Default authorization policies initialized")
    
    async def authorize(self, request: AccessRequest) -> AccessResult:
        """Authorize access request"""
        try:
            # Check RBAC permissions
            has_rbac_permission = self.rbac_manager.has_permission(
                request.user_id,
                request.resource_type,
                request.action,
                request.resource_id
            )
            
            # Get applicable policies
            applicable_policies = self.policy_engine.get_applicable_policies(
                request.resource_type,
                request.action
            )
            
            # Evaluate policies
            policy_violations = []
            for policy_id in applicable_policies:
                if not self.policy_engine.evaluate_policy(policy_id, request.context):
                    policy_violations.append(policy_id)
            
            # Determine final access decision
            granted = has_rbac_permission and len(policy_violations) == 0
            
            # Get matched permissions for audit
            matched_permissions = []
            if has_rbac_permission:
                user_permissions = self.rbac_manager.get_user_permissions(request.user_id)
                for perm in user_permissions:
                    if (perm.resource_type == request.resource_type and 
                        perm.action == request.action):
                        matched_permissions.append(perm.name)
            
            # Create result
            result = AccessResult(
                granted=granted,
                user_id=request.user_id,
                resource_type=request.resource_type,
                action=request.action,
                reason=self._generate_access_reason(granted, has_rbac_permission, policy_violations),
                matched_permissions=matched_permissions,
                policy_violations=policy_violations
            )
            
            # Store for audit
            self.access_history.append(result)
            
            # Log access attempt
            self.logger.info(f"Access {'granted' if granted else 'denied'} for user {request.user_id}: "
                           f"{request.resource_type.value}:{request.action.value}")
            
            return result
            
        except Exception as e:
            self.logger.error(f"Authorization failed: {e}")
            return AccessResult(
                granted=False,
                user_id=request.user_id,
                resource_type=request.resource_type,
                action=request.action,
                reason=f"Authorization error: {e}"
            )
    
    def _generate_access_reason(self, granted: bool, has_rbac_permission: bool, 
                              policy_violations: List[str]) -> str:
        """Generate human-readable access reason"""
        if granted:
            return "Access granted: User has required permissions and meets all policy requirements"
        
        reasons = []
        
        if not has_rbac_permission:
            reasons.append("User lacks required RBAC permissions")
        
        if policy_violations:
            reasons.append(f"Policy violations: {', '.join(policy_violations)}")
        
        return "Access denied: " + "; ".join(reasons)
    
    async def bulk_authorize(self, requests: List[AccessRequest]) -> List[AccessResult]:
        """Authorize multiple requests"""
        results = []
        
        for request in requests:
            result = await self.authorize(request)
            results.append(result)
        
        return results
    
    def get_user_roles(self, user_id: str) -> List[str]:
        """Get user roles"""
        if user_id in self.rbac_manager.users:
            user = self.rbac_manager.users[user_id]
            role_names = []
            for role_id in user.roles:
                if role_id in self.rbac_manager.roles:
                    role_names.append(self.rbac_manager.roles[role_id].name)
            return role_names
        return []
    
    def get_user_permissions_summary(self, user_id: str) -> Dict[str, Any]:
        """Get user permissions summary"""
        permissions = self.rbac_manager.get_user_permissions(user_id)
        roles = self.get_user_roles(user_id)
        
        # Group permissions by resource type
        by_resource = {}
        for perm in permissions:
            resource = perm.resource_type.value
            if resource not in by_resource:
                by_resource[resource] = []
            by_resource[resource].append(perm.action.value)
        
        return {
            'user_id': user_id,
            'roles': roles,
            'permissions_count': len(permissions),
            'permissions_by_resource': by_resource,
            'last_updated': datetime.utcnow().isoformat()
        }
    
    def get_access_history(self, user_id: str = None, limit: int = 100) -> List[AccessResult]:
        """Get access history"""
        history = self.access_history
        
        if user_id:
            history = [result for result in history if result.user_id == user_id]
        
        # Sort by timestamp (newest first)
        history.sort(key=lambda x: x.timestamp, reverse=True)
        
        return history[:limit]
    
    async def cleanup_old_history(self, days: int = 30) -> int:
        """Cleanup old access history"""
        cutoff = datetime.utcnow() - timedelta(days=days)
        
        old_count = len(self.access_history)
        self.access_history = [
            result for result in self.access_history 
            if result.timestamp > cutoff
        ]
        
        removed_count = old_count - len(self.access_history)
        self.logger.info(f"Cleaned up {removed_count} old access history records")
        
        return removed_count 