from typing import Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
import uuid

class UserBase(BaseModel):
    """Base User model with common properties"""
    username: str = Field(..., description="Unique username for the user", example="john_doe")
    email: Optional[EmailStr] = Field(None, description="Email address", example="john.doe@example.com")
    full_name: Optional[str] = Field(None, description="User's full name", example="John Doe")
    profile_image_url: Optional[str] = Field(None, description="URL to profile image")
    bio: Optional[str] = Field(None, description="Short biography")
    is_active: bool = Field(True, description="Whether the user account is active")
    is_superuser: bool = Field(False, description="Whether the user has superuser privileges")


class UserCreate(UserBase):
    """Model for creating a new user, including password"""
    password: str = Field(..., min_length=8, description="User password, must be at least 8 characters")
    
    class Config:
        schema_extra = {
            "example": {
                "username": "john_doe",
                "email": "john.doe@example.com",
                "password": "securepassword123",
                "full_name": "John Doe",
                "is_active": True,
                "is_superuser": False
            }
        }


class UserUpdate(BaseModel):
    """Model for updating user information"""
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    profile_image_url: Optional[str] = None
    bio: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    
    class Config:
        schema_extra = {
            "example": {
                "full_name": "John Smith",
                "email": "john.smith@example.com"
            }
        }


class UserInDB(UserBase):
    """Internal representation of a user with hashed_password"""
    uid: str
    hashed_password: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True


class UserResponse(UserBase):
    """Public representation of a user for API responses"""
    uid: str
    created_at: str
    updated_at: str
    
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "uid": "550e8400-e29b-41d4-a716-446655440000",
                "username": "john_doe",
                "email": "john.doe@example.com",
                "full_name": "John Doe",
                "is_active": True,
                "is_superuser": False,
                "created_at": "2025-06-01T12:00:00Z",
                "updated_at": "2025-06-01T12:00:00Z"
            }
        }


class Token(BaseModel):
    """OAuth2 token model"""
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    """Token payload model"""
    sub: Optional[str] = None
    exp: Optional[int] = None
