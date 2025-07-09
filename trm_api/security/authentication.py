"""
Enterprise Authentication System cho TRM-OS Phase 3

Advanced authentication với:
- JWT tokens với refresh mechanism
- Multi-factor authentication (MFA)
- Session management
- Password security
- Rate limiting
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
from uuid import uuid4
import hashlib
import secrets
import jwt
import bcrypt
import pyotp
from email_validator import validate_email, EmailNotValidError

from ..core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


@dataclass
class UserCredentials:
    """User credentials cho authentication"""
    username: Optional[str] = None
    email: Optional[str] = None
    password: str = ""
    mfa_token: Optional[str] = None
    user_id: Optional[str] = None
    remember_me: bool = False


@dataclass
class AuthResult:
    """Kết quả authentication"""
    success: bool
    user_id: Optional[str] = None
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    expires_at: Optional[datetime] = None
    requires_mfa: bool = False
    mfa_secret: Optional[str] = None
    error_message: Optional[str] = None
    session_id: Optional[str] = None
    permissions: List[str] = None


@dataclass
class UserSession:
    """User session data"""
    session_id: str
    user_id: str
    created_at: datetime
    last_activity: datetime
    expires_at: datetime
    ip_address: str
    user_agent: str
    is_active: bool = True
    mfa_verified: bool = False


class PasswordManager:
    """Manager cho password security"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.min_length = 8
        self.require_uppercase = True
        self.require_lowercase = True
        self.require_digits = True
        self.require_special = True
        self.special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        try:
            # Generate salt và hash password
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
            return hashed.decode('utf-8')
            
        except Exception as e:
            self.logger.error(f"Password hashing failed: {e}")
            raise
    
    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
            
        except Exception as e:
            self.logger.error(f"Password verification failed: {e}")
            return False
    
    def validate_password_strength(self, password: str) -> Tuple[bool, List[str]]:
        """Validate password strength"""
        errors = []
        
        # Check length
        if len(password) < self.min_length:
            errors.append(f"Password must be at least {self.min_length} characters long")
        
        # Check uppercase
        if self.require_uppercase and not any(c.isupper() for c in password):
            errors.append("Password must contain at least one uppercase letter")
        
        # Check lowercase
        if self.require_lowercase and not any(c.islower() for c in password):
            errors.append("Password must contain at least one lowercase letter")
        
        # Check digits
        if self.require_digits and not any(c.isdigit() for c in password):
            errors.append("Password must contain at least one digit")
        
        # Check special characters
        if self.require_special and not any(c in self.special_chars for c in password):
            errors.append("Password must contain at least one special character")
        
        return len(errors) == 0, errors
    
    def generate_secure_password(self, length: int = 12) -> str:
        """Generate secure random password"""
        import string
        
        # Ensure we have all required character types
        chars = []
        
        if self.require_uppercase:
            chars.extend(string.ascii_uppercase)
        if self.require_lowercase:
            chars.extend(string.ascii_lowercase)
        if self.require_digits:
            chars.extend(string.digits)
        if self.require_special:
            chars.extend(self.special_chars)
        
        # Generate password
        password = ''.join(secrets.choice(chars) for _ in range(length))
        
        return password


class MFAManager:
    """Manager cho Multi-Factor Authentication"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.issuer_name = "TRM-OS"
        self.token_validity = 30  # seconds
    
    def generate_mfa_secret(self, user_id: str) -> str:
        """Generate MFA secret cho user"""
        try:
            secret = pyotp.random_base32()
            return secret
            
        except Exception as e:
            self.logger.error(f"MFA secret generation failed: {e}")
            raise
    
    def generate_qr_code_url(self, user_email: str, secret: str) -> str:
        """Generate QR code URL cho MFA setup"""
        try:
            totp = pyotp.TOTP(secret)
            qr_url = totp.provisioning_uri(
                name=user_email,
                issuer_name=self.issuer_name
            )
            return qr_url
            
        except Exception as e:
            self.logger.error(f"QR code URL generation failed: {e}")
            raise
    
    def verify_mfa_token(self, secret: str, token: str) -> bool:
        """Verify MFA token"""
        try:
            totp = pyotp.TOTP(secret)
            return totp.verify(token, valid_window=1)  # Allow 1 time step tolerance
            
        except Exception as e:
            self.logger.error(f"MFA token verification failed: {e}")
            return False
    
    def generate_backup_codes(self, count: int = 10) -> List[str]:
        """Generate backup codes cho MFA"""
        try:
            codes = []
            for _ in range(count):
                # Generate 8-character alphanumeric code
                code = ''.join(secrets.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(8))
                codes.append(code)
            
            return codes
            
        except Exception as e:
            self.logger.error(f"Backup codes generation failed: {e}")
            raise


class JWTManager:
    """Manager cho JWT tokens"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.secret_key = settings.SECRET_KEY
        self.algorithm = settings.ALGORITHM
        self.access_token_expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
        self.refresh_token_expire_days = 30
    
    def create_access_token(self, user_id: str, permissions: List[str] = None) -> str:
        """Create JWT access token"""
        try:
            # Token payload
            payload = {
                "sub": user_id,
                "type": "access",
                "iat": datetime.utcnow(),
                "exp": datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes),
                "jti": str(uuid4()),  # JWT ID cho token tracking
                "permissions": permissions or []
            }
            
            # Create token
            token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
            return token
            
        except Exception as e:
            self.logger.error(f"Access token creation failed: {e}")
            raise
    
    def create_refresh_token(self, user_id: str) -> str:
        """Create JWT refresh token"""
        try:
            # Token payload
            payload = {
                "sub": user_id,
                "type": "refresh",
                "iat": datetime.utcnow(),
                "exp": datetime.utcnow() + timedelta(days=self.refresh_token_expire_days),
                "jti": str(uuid4())
            }
            
            # Create token
            token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
            return token
            
        except Exception as e:
            self.logger.error(f"Refresh token creation failed: {e}")
            raise
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify và decode JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            
            # Check if token is expired
            exp = payload.get('exp')
            if exp and datetime.fromtimestamp(exp) < datetime.utcnow():
                return None
            
            return payload
            
        except jwt.ExpiredSignatureError:
            self.logger.warning("Token has expired")
            return None
        except jwt.InvalidTokenError as e:
            self.logger.warning(f"Invalid token: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Token verification failed: {e}")
            return None
    
    def refresh_access_token(self, refresh_token: str) -> Optional[str]:
        """Refresh access token using refresh token"""
        try:
            # Verify refresh token
            payload = self.verify_token(refresh_token)
            if not payload or payload.get('type') != 'refresh':
                return None
            
            user_id = payload.get('sub')
            if not user_id:
                return None
            
            # Create new access token
            # Note: Would need to fetch user permissions from database
            new_access_token = self.create_access_token(user_id)
            return new_access_token
            
        except Exception as e:
            self.logger.error(f"Token refresh failed: {e}")
            return None


class SessionManager:
    """Manager cho user sessions"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.sessions: Dict[str, UserSession] = {}
        self.max_sessions_per_user = 5
        self.session_timeout_minutes = 30
    
    def create_session(self, user_id: str, ip_address: str, user_agent: str) -> UserSession:
        """Create new user session"""
        try:
            session_id = str(uuid4())
            now = datetime.utcnow()
            
            session = UserSession(
                session_id=session_id,
                user_id=user_id,
                created_at=now,
                last_activity=now,
                expires_at=now + timedelta(minutes=self.session_timeout_minutes),
                ip_address=ip_address,
                user_agent=user_agent
            )
            
            # Cleanup old sessions cho user
            self._cleanup_user_sessions(user_id)
            
            # Store session
            self.sessions[session_id] = session
            
            return session
            
        except Exception as e:
            self.logger.error(f"Session creation failed: {e}")
            raise
    
    def get_session(self, session_id: str) -> Optional[UserSession]:
        """Get session by ID"""
        session = self.sessions.get(session_id)
        
        if session and session.is_active:
            # Check if session is expired
            if datetime.utcnow() > session.expires_at:
                self.invalidate_session(session_id)
                return None
            
            # Update last activity
            session.last_activity = datetime.utcnow()
            session.expires_at = datetime.utcnow() + timedelta(minutes=self.session_timeout_minutes)
            
            return session
        
        return None
    
    def invalidate_session(self, session_id: str) -> bool:
        """Invalidate session"""
        if session_id in self.sessions:
            self.sessions[session_id].is_active = False
            del self.sessions[session_id]
            return True
        return False
    
    def invalidate_user_sessions(self, user_id: str) -> int:
        """Invalidate tất cả sessions cho user"""
        count = 0
        sessions_to_remove = []
        
        for session_id, session in self.sessions.items():
            if session.user_id == user_id:
                sessions_to_remove.append(session_id)
                count += 1
        
        for session_id in sessions_to_remove:
            self.invalidate_session(session_id)
        
        return count
    
    def _cleanup_user_sessions(self, user_id: str) -> None:
        """Cleanup old sessions cho user"""
        user_sessions = [
            (session_id, session) for session_id, session in self.sessions.items()
            if session.user_id == user_id and session.is_active
        ]
        
        # Sort by creation time
        user_sessions.sort(key=lambda x: x[1].created_at)
        
        # Remove oldest sessions if exceeding limit
        while len(user_sessions) >= self.max_sessions_per_user:
            oldest_session_id = user_sessions.pop(0)[0]
            self.invalidate_session(oldest_session_id)


class AuthenticationManager:
    """Main authentication manager"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.password_manager = PasswordManager()
        self.mfa_manager = MFAManager()
        self.jwt_manager = JWTManager()
        self.session_manager = SessionManager()
        
        # Rate limiting
        self.login_attempts: Dict[str, List[datetime]] = {}
        self.max_attempts = 5
        self.lockout_duration_minutes = 15
        
        # User database (in production, would use real database)
        self.users: Dict[str, Dict[str, Any]] = {}
    
    async def register_user(self, credentials: UserCredentials) -> AuthResult:
        """Register new user"""
        try:
            # Validate email
            if credentials.email:
                try:
                    validate_email(credentials.email)
                except EmailNotValidError:
                    return AuthResult(
                        success=False,
                        error_message="Invalid email address"
                    )
            
            # Validate password strength
            is_strong, errors = self.password_manager.validate_password_strength(credentials.password)
            if not is_strong:
                return AuthResult(
                    success=False,
                    error_message="; ".join(errors)
                )
            
            # Check if user already exists
            user_id = credentials.email or credentials.username
            if user_id in self.users:
                return AuthResult(
                    success=False,
                    error_message="User already exists"
                )
            
            # Hash password
            hashed_password = self.password_manager.hash_password(credentials.password)
            
            # Generate MFA secret
            mfa_secret = self.mfa_manager.generate_mfa_secret(user_id)
            
            # Store user
            self.users[user_id] = {
                'user_id': user_id,
                'email': credentials.email,
                'username': credentials.username,
                'password_hash': hashed_password,
                'mfa_secret': mfa_secret,
                'mfa_enabled': False,
                'created_at': datetime.utcnow(),
                'is_active': True,
                'permissions': ['user']  # Default permissions
            }
            
            return AuthResult(
                success=True,
                user_id=user_id,
                mfa_secret=mfa_secret
            )
            
        except Exception as e:
            self.logger.error(f"User registration failed: {e}")
            return AuthResult(
                success=False,
                error_message=str(e)
            )
    
    async def authenticate_user(self, credentials: UserCredentials, 
                              ip_address: str = "", user_agent: str = "") -> AuthResult:
        """Authenticate user với credentials"""
        try:
            user_id = credentials.email or credentials.username
            
            # Check rate limiting
            if self._is_rate_limited(user_id):
                return AuthResult(
                    success=False,
                    error_message="Too many login attempts. Please try again later."
                )
            
            # Get user
            user = self.users.get(user_id)
            if not user or not user['is_active']:
                self._record_failed_attempt(user_id)
                return AuthResult(
                    success=False,
                    error_message="Invalid credentials"
                )
            
            # Verify password
            if not self.password_manager.verify_password(credentials.password, user['password_hash']):
                self._record_failed_attempt(user_id)
                return AuthResult(
                    success=False,
                    error_message="Invalid credentials"
                )
            
            # Check MFA if enabled
            if user['mfa_enabled']:
                if not credentials.mfa_token:
                    return AuthResult(
                        success=False,
                        requires_mfa=True,
                        user_id=user_id,
                        error_message="MFA token required"
                    )
                
                if not self.mfa_manager.verify_mfa_token(user['mfa_secret'], credentials.mfa_token):
                    self._record_failed_attempt(user_id)
                    return AuthResult(
                        success=False,
                        error_message="Invalid MFA token"
                    )
            
            # Create session
            session = self.session_manager.create_session(user_id, ip_address, user_agent)
            
            # Create tokens
            access_token = self.jwt_manager.create_access_token(user_id, user['permissions'])
            refresh_token = self.jwt_manager.create_refresh_token(user_id)
            
            # Clear failed attempts
            self._clear_failed_attempts(user_id)
            
            return AuthResult(
                success=True,
                user_id=user_id,
                access_token=access_token,
                refresh_token=refresh_token,
                expires_at=session.expires_at,
                session_id=session.session_id,
                permissions=user['permissions']
            )
            
        except Exception as e:
            self.logger.error(f"Authentication failed: {e}")
            return AuthResult(
                success=False,
                error_message=str(e)
            )
    
    def _is_rate_limited(self, user_id: str) -> bool:
        """Check if user is rate limited"""
        now = datetime.utcnow()
        cutoff = now - timedelta(minutes=self.lockout_duration_minutes)
        
        attempts = self.login_attempts.get(user_id, [])
        recent_attempts = [attempt for attempt in attempts if attempt > cutoff]
        
        return len(recent_attempts) >= self.max_attempts
    
    def _record_failed_attempt(self, user_id: str) -> None:
        """Record failed login attempt"""
        now = datetime.utcnow()
        
        if user_id not in self.login_attempts:
            self.login_attempts[user_id] = []
        
        self.login_attempts[user_id].append(now)
        
        # Keep only recent attempts
        cutoff = now - timedelta(minutes=self.lockout_duration_minutes)
        self.login_attempts[user_id] = [
            attempt for attempt in self.login_attempts[user_id] if attempt > cutoff
        ]
    
    def _clear_failed_attempts(self, user_id: str) -> None:
        """Clear failed login attempts"""
        if user_id in self.login_attempts:
            del self.login_attempts[user_id]
    
    async def logout_user(self, session_id: str) -> bool:
        """Logout user by invalidating session"""
        try:
            return self.session_manager.invalidate_session(session_id)
            
        except Exception as e:
            self.logger.error(f"Logout failed: {e}")
            return False
    
    async def verify_session(self, session_id: str) -> Optional[UserSession]:
        """Verify user session"""
        try:
            return self.session_manager.get_session(session_id)
            
        except Exception as e:
            self.logger.error(f"Session verification failed: {e}")
            return None
    
    async def enable_mfa(self, user_id: str) -> bool:
        """Enable MFA cho user"""
        try:
            if user_id in self.users:
                self.users[user_id]['mfa_enabled'] = True
                return True
            return False
            
        except Exception as e:
            self.logger.error(f"MFA enable failed: {e}")
            return False
    
    async def disable_mfa(self, user_id: str) -> bool:
        """Disable MFA cho user"""
        try:
            if user_id in self.users:
                self.users[user_id]['mfa_enabled'] = False
                return True
            return False
            
        except Exception as e:
            self.logger.error(f"MFA disable failed: {e}")
            return False
    
    async def get_user_info(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user information"""
        user = self.users.get(user_id)
        if user:
            # Return safe user info (no password hash)
            return {
                'user_id': user['user_id'],
                'email': user['email'],
                'username': user['username'],
                'mfa_enabled': user['mfa_enabled'],
                'created_at': user['created_at'],
                'permissions': user['permissions']
            }
        return None 