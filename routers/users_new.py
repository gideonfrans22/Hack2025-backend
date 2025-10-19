"""
User Routes - API endpoints for user management and authentication
"""
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List

from models.user_models import (
    User, UserSignup, UserLogin, Token,
    KakaoLogin, NaverLogin, UserProfileUpdate,
    OAuthLoginResponse, UserProfile
)
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
            detail="사용자를 찾을 수 없습니다",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


@router.post("/signup", response_model=Token)
async def signup(user: UserSignup):
    """
    User signup endpoint with password encryption, Firestore storage, and JWT token generation
    
    Args:
        user: User signup data
        
    Returns:
        JWT token and user information (without password)
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


@router.post("/auth/kakao/login", response_model=OAuthLoginResponse)
async def kakao_login(kakao_data: KakaoLogin):
    """
    Kakao OAuth login endpoint
    
    Authenticates user with Kakao OAuth token and creates/updates user account.
    Returns JWT token for backend authentication.
    
    Args:
        kakao_data: Kakao OAuth login data including access_token, kakao_id, email, nickname, profile_image
        
    Returns:
        OAuth login response with:
        - success: True if login successful
        - data:
            - token: Backend JWT token
            - user: User profile (id, email, nickname)
            - is_new_user: True if this is a new account
    """
    return UserController.kakao_login(kakao_data)


@router.post("/auth/naver/login", response_model=OAuthLoginResponse)
async def naver_login(naver_data: NaverLogin):
    """
    Naver OAuth login endpoint
    
    Authenticates user with Naver OAuth token and creates/updates user account.
    Returns JWT token for backend authentication.
    
    Args:
        naver_data: Naver OAuth login data including access_token, naver_id, email, nickname, profile_image
        
    Returns:
        OAuth login response with:
        - success: True if login successful
        - data:
            - token: Backend JWT token
            - user: User profile (id, email, nickname)
            - is_new_user: True if this is a new account
    """
    return UserController.naver_login(naver_data)


@router.put("/user/profile", response_model=UserProfile)
async def update_user_profile(
    profile_data: UserProfileUpdate,
    current_user: User = Depends(get_current_user)
):
    """
    Update user profile (protected endpoint)
    
    Updates user profile information for the currently authenticated user.
    Only provided fields will be updated (partial update supported).
    
    Args:
        profile_data: Profile update data (all fields optional)
        current_user: Current authenticated user from JWT token
        
    Returns:
        Updated user profile
    """
    return UserController.update_profile(current_user.email, profile_data)
