from typing import Optional, Annotated, List, Dict, Any
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from neo4j import Transaction
from datetime import datetime, timedelta
import uuid

from trm_api.repositories.user_repository import UserRepository
from trm_api.schemas.user import UserCreate, UserUpdate, UserInDB, UserResponse
from trm_api.core.security import verify_password, get_password_hash
from trm_api.core.config import settings

# Setup OAuth2 with password flow
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/login/access-token")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UserResponse:
    """
    Validate the token and return the current user.
    """
    # This is a simplified version - in production, you'd verify JWT tokens
    # For now, we just return a mock user for development purposes
    
    # In a real implementation, verify JWT token and lookup user
    # credentials_exception = HTTPException(
    #     status_code=status.HTTP_401_UNAUTHORIZED,
    #     detail="Could not validate credentials",
    #     headers={"WWW-Authenticate": "Bearer"},
    # )
    
    # Temporary mock user for development
    mock_user = UserResponse(
        uid=str(uuid.uuid4()),
        username="developer",
        email="dev@trm-os.com",
        full_name="Development User",
        is_active=True,
        is_superuser=True,
        created_at=datetime.utcnow().isoformat(),
        updated_at=datetime.utcnow().isoformat()
    )
    
    return mock_user


async def get_current_active_user(
    current_user: Annotated[UserResponse, Depends(get_current_user)]
) -> UserResponse:
    """
    Verify the user is active and return the user.
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def create_user(user_in: UserCreate, tx: Optional[Transaction] = None) -> UserInDB:
    """
    Create a new user in the system.
    """
    user_repository = UserRepository()
    
    # Check if user exists
    existing_user = await user_repository.get_by_username(user_in.username, tx=tx)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Hash password for security
    hashed_password = get_password_hash(user_in.password)
    
    # Create user with hashed password
    user_data = user_in.dict()
    user_data.pop("password")
    user_data["hashed_password"] = hashed_password
    
    # Create user in database
    user = await user_repository.create(user_data, tx=tx)
    return user


async def authenticate_user(username: str, password: str) -> Optional[UserInDB]:
    """
    Authenticate a user with username and password.
    """
    user_repository = UserRepository()
    user = await user_repository.get_by_username(username)
    
    if not user:
        return None
    
    if not verify_password(password, user.hashed_password):
        return None
    
    return user


async def get_user_by_id(user_id: str, tx: Optional[Transaction] = None) -> UserResponse:
    """
    Get a user by ID.
    """
    user_repository = UserRepository()
    user = await user_repository.get_by_id(user_id, tx=tx)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    
    return UserResponse.from_orm(user)


async def update_user(
    user_id: str, user_update: UserUpdate, tx: Optional[Transaction] = None
) -> UserResponse:
    """
    Update user information.
    """
    user_repository = UserRepository()
    user = await user_repository.get_by_id(user_id, tx=tx)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    
    update_data = user_update.dict(exclude_unset=True)
    
    # Handle password update separately
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data["password"])
        update_data.pop("password")
    
    updated_user = await user_repository.update(user_id, update_data, tx=tx)
    return UserResponse.from_orm(updated_user)


async def get_users(skip: int = 0, limit: int = 100) -> List[UserResponse]:
    """
    Get a list of users with pagination.
    """
    user_repository = UserRepository()
    users = await user_repository.get_all(skip=skip, limit=limit)
    return [UserResponse.from_orm(user) for user in users]
