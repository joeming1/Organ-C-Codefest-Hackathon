"""
Admin Authentication Routes

Endpoints for admin login, logout, and session management.
"""

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import timedelta
import logging

from jwt_auth import (
    authenticate_admin,
    create_access_token,
    get_current_admin,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ADMIN_USERNAME
)

logger = logging.getLogger(__name__)

router = APIRouter()


# ============================================
# REQUEST/RESPONSE SCHEMAS
# ============================================

class LoginRequest(BaseModel):
    """Login request schema."""
    username: str
    password: str


class LoginResponse(BaseModel):
    """Login response schema."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int  # minutes
    username: str


class UserResponse(BaseModel):
    """Current user response schema."""
    username: str
    is_admin: bool = True


class LogoutResponse(BaseModel):
    """Logout response schema."""
    message: str


# ============================================
# AUTHENTICATION ENDPOINTS
# ============================================

@router.post("/login", response_model=LoginResponse, tags=["Authentication"], include_in_schema=False)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    🔐 Admin Login Endpoint
    
    Authenticate admin and receive JWT token.
    
    **Note**: Uses OAuth2PasswordRequestForm for compatibility with Swagger UI.
    For JSON requests, use username/password fields.
    
    Returns:
        - 200: Login successful, returns JWT token
        - 401: Invalid credentials
    """
    # Authenticate admin
    if not authenticate_admin(form_data.username, form_data.password):
        logger.warning(f"Failed login attempt for username: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username},
        expires_delta=access_token_expires
    )
    
    logger.info(f"Admin login successful: {form_data.username}")
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES,
        "username": form_data.username
    }


@router.post("/login/json", response_model=LoginResponse, tags=["Authentication"])
async def login_json(credentials: LoginRequest):
    """
    🔐 Admin Login Endpoint (JSON)
    
    Alternative login endpoint that accepts JSON body instead of form data.
    Better for frontend applications.
    
    Returns:
        - 200: Login successful, returns JWT token
        - 401: Invalid credentials
    """
    # Authenticate admin
    if not authenticate_admin(credentials.username, credentials.password):
        logger.warning(f"Failed login attempt for username: {credentials.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": credentials.username},
        expires_delta=access_token_expires
    )
    
    logger.info(f"Admin login successful: {credentials.username}")
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES,
        "username": credentials.username
    }


@router.get("/me", response_model=UserResponse, tags=["Authentication"])
async def get_current_user(admin: str = Depends(get_current_admin)):
    """
    👤 Get Current Admin User
    
    Returns information about the currently authenticated admin.
    Protected endpoint - requires valid JWT token.
    
    Returns:
        - 200: Current user info
        - 401: Not authenticated
    """
    return {
        "username": admin,
        "is_admin": True
    }


@router.post("/logout", response_model=LogoutResponse, tags=["Authentication"])
async def logout(admin: str = Depends(get_current_admin)):
    """
    🚪 Admin Logout
    
    Logout endpoint. In JWT-based auth, logout is typically handled client-side
    by discarding the token. This endpoint exists for API completeness.
    
    **Note**: JWT tokens cannot be invalidated server-side without a token blacklist.
    For production, consider implementing token refresh and blacklisting.
    
    Returns:
        - 200: Logout successful
        - 401: Not authenticated
    """
    logger.info(f"Admin logout: {admin}")
    return {"message": "Logged out successfully"}






