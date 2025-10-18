"""
User data models for authentication and user management
"""
from pydantic import BaseModel, EmailStr
from typing import Optional


class User(BaseModel):
    """Base user model"""
    name: str
    age: int
    gender: str
    email: EmailStr
    hobby: Optional[str] = None


class UserInDB(User):
    """User model with hashed password for database storage"""
    hashed_password: str


class UserSignup(BaseModel):
    """User signup request model"""
    name: str
    age: int
    gender: str
    email: EmailStr
    password: str
    hobby: Optional[str] = None


class UserLogin(BaseModel):
    """User login request model"""
    email: EmailStr
    password: str


class Token(BaseModel):
    """JWT token response model"""
    access_token: str
    token_type: str
    user: User
