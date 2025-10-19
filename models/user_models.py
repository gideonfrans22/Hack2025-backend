"""
User data models for authentication and user management
"""
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


class User(BaseModel):
    """Base user model"""
    name: str
    age: int
    gender: str
    email: EmailStr
    hobby: Optional[str] = None
    nickname: Optional[str] = None
    profile_image: Optional[str] = None
    interests: Optional[List[str]] = None  # List of user interests


class UserInDB(User):
    """User model with hashed password for database storage"""
    hashed_password: Optional[str] = None  # Optional for OAuth users
    oauth_provider: Optional[str] = None  # 'kakao', 'naver', or None for regular users
    oauth_id: Optional[str] = None  # Provider-specific user ID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class UserSignup(BaseModel):
    """User signup request model"""
    name: str
    age: int
    gender: str
    email: EmailStr
    password: str
    hobby: Optional[str] = None
    interests: Optional[List[str]] = None  # List of user interests


class UserLogin(BaseModel):
    """User login request model"""
    email: EmailStr
    password: str


class KakaoLogin(BaseModel):
    """Kakao OAuth login request model"""
    access_token: str
    kakao_id: str
    email: EmailStr
    nickname: str
    profile_image: Optional[str] = None


class NaverLogin(BaseModel):
    """Naver OAuth login request model"""
    access_token: str
    naver_id: str
    email: EmailStr
    nickname: str
    profile_image: Optional[str] = None


class UserProfileUpdate(BaseModel):
    """User profile update request model"""
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    hobby: Optional[str] = None
    nickname: Optional[str] = None
    profile_image: Optional[str] = None
    interests: Optional[List[str]] = None  # List of user interests


class Token(BaseModel):
    """JWT token response model"""
    access_token: str
    token_type: str
    user: User


class OAuthLoginResponse(BaseModel):
    """OAuth login response model"""
    success: bool
    data: dict  # Contains token, user, and is_new_user


class UserProfile(BaseModel):
    """User profile response model"""
    id: int
    email: str
    nickname: Optional[str] = None
    name: Optional[str] = None
    profile_image: Optional[str] = None
    oauth_provider: Optional[str] = None
    interests: Optional[List[str]] = None  # List of user interests
