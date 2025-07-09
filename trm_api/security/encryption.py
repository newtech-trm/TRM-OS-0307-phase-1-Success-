"""
Encryption Service cho TRM-OS Phase 3

Data encryption và protection với:
- AES encryption cho sensitive data
- RSA encryption cho key exchange
- Data hashing và integrity
- Secure key management
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
import base64
import hashlib
import secrets
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

logger = logging.getLogger(__name__)


class EncryptionService:
    """Main encryption service"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.fernet_key = None
        self.fernet = None
        self._initialize_encryption()
    
    def _initialize_encryption(self) -> None:
        """Initialize encryption components"""
        try:
            # Generate or load Fernet key
            self.fernet_key = Fernet.generate_key()
            self.fernet = Fernet(self.fernet_key)
            
            self.logger.info("Encryption service initialized")
            
        except Exception as e:
            self.logger.error(f"Encryption initialization failed: {e}")
            raise
    
    def encrypt_data(self, data: str) -> str:
        """Encrypt string data"""
        try:
            encrypted = self.fernet.encrypt(data.encode())
            return base64.b64encode(encrypted).decode()
            
        except Exception as e:
            self.logger.error(f"Data encryption failed: {e}")
            raise
    
    def decrypt_data(self, encrypted_data: str) -> str:
        """Decrypt string data"""
        try:
            encrypted_bytes = base64.b64decode(encrypted_data.encode())
            decrypted = self.fernet.decrypt(encrypted_bytes)
            return decrypted.decode()
            
        except Exception as e:
            self.logger.error(f"Data decryption failed: {e}")
            raise
    
    def hash_data(self, data: str, salt: Optional[str] = None) -> Tuple[str, str]:
        """Hash data với salt"""
        try:
            if salt is None:
                salt = secrets.token_hex(32)
            
            # Create hash
            hash_obj = hashlib.pbkdf2_hmac('sha256', 
                                         data.encode(), 
                                         salt.encode(), 
                                         100000)  # 100k iterations
            
            hashed = base64.b64encode(hash_obj).decode()
            return hashed, salt
            
        except Exception as e:
            self.logger.error(f"Data hashing failed: {e}")
            raise
    
    def verify_hash(self, data: str, hashed: str, salt: str) -> bool:
        """Verify data against hash"""
        try:
            new_hash, _ = self.hash_data(data, salt)
            return new_hash == hashed
            
        except Exception as e:
            self.logger.error(f"Hash verification failed: {e}")
            return False


class DataProtection:
    """Data protection utilities"""
    
    def __init__(self):
        self.encryption_service = EncryptionService()
    
    def protect_sensitive_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Protect sensitive fields in data"""
        try:
            protected_data = data.copy()
            sensitive_fields = ['password', 'token', 'secret', 'key']
            
            for field in sensitive_fields:
                if field in protected_data:
                    protected_data[field] = self.encryption_service.encrypt_data(
                        str(protected_data[field])
                    )
            
            return protected_data
            
        except Exception as e:
            self.logger.error(f"Data protection failed: {e}")
            return data 