"""
User Routes - API endpoints for user management and authentication
"""
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List

from models.user_models import User, UserSignup, UserLogin, Token
from controllers.user_controller import UserController

router = APIRouter()
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    """
    Dependency to get current authenticated user from JWT token
    
    Args:
        credentials: HTTP Bearer token credentials
        
    Returns:
        Current user object
        
    Raises:
        HTTPException: If authentication fails
    """
    # Verify token and get email
    email = UserController.verify_token(credentials.credentials)
    
    # Get user from database
    user = UserController.get_user_by_email(email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


@router.post("/signup", response_model=User)
async def signup(user: UserSignup):
    """
    User signup endpoint with password encryption and Firestore storage
    
    Args:
        user: User signup data
        
    Returns:
        Created user object (without password)
    """
    return UserController.signup(user)


@router.post("/login", response_model=Token)
async def login(user: UserLogin):
    """
    User login endpoint. Returns JWT token on successful authentication.
    
    Args:
        user: User login credentials
        
    Returns:
        JWT token and user information
    """
    return UserController.login(user)


@router.get("/me", response_model=User)
async def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """
    Get current user profile (protected endpoint)
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        User profile information
    """
    return current_user


@router.get("/users/", response_model=List[User])
async def read_users(current_user: User = Depends(get_current_user)):
    """
    Get all users from Firestore (protected endpoint)
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        List of all users (without passwords)
    """
    return UserController.get_all_users()


@router.get("/users/{email}", response_model=User)
async def read_user_by_email(
    email: str, 
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific user by email from Firestore (protected endpoint)
    
    Args:
        email: User email to lookup
        current_user: Current authenticated user
        
    Returns:
        User information (without password)
    """
    return UserController.get_user_by_email_detailed(email)
