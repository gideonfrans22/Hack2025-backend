from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import sys
import os
import bcrypt
from jose import JWTError, jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add parent directory to path to import firebase_config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from firebase_config import firebase_service

router = APIRouter()

# Security scheme for JWT
security = HTTPBearer()

# JWT Configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-default-secret-key-change-this")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token and return current user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # Get user from database
    try:
        db = firebase_service.db
        users_ref = db.collection('users')
        docs = users_ref.where('email', '==', email).get()
        
        if not docs:
            raise credentials_exception
            
        user_data = docs[0].to_dict()
        return User(**{k: user_data[k] for k in User.model_fields.keys() if k in user_data})
        
    except Exception:
        raise credentials_exception

class User(BaseModel):
    name: str
    age: int
    gender: str
    email: EmailStr
    hobby: Optional[str] = None

class UserInDB(User):
    hashed_password: str

class UserSignup(BaseModel):
    name: str
    age: int
    gender: str
    email: EmailStr
    password: str
    hobby: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user: User

@router.post("/signup", tags=["users"], response_model=User)
async def signup(user: UserSignup):
    """User signup endpoint with password encryption and Firestore storage"""
    try:
        db = firebase_service.db
        users_ref = db.collection('users')
        # Check if user already exists by email
        existing = users_ref.where('email', '==', user.email).get()
        if existing:
            raise HTTPException(status_code=400, detail="User with this email already exists")
        # Hash password
        hashed_pw = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user_dict = user.dict()
        user_dict['hashed_password'] = hashed_pw
        del user_dict['password']
        # Store user in Firestore
        users_ref.add(user_dict)
        return User(**{k: user_dict[k] for k in User.model_fields.keys()})
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during signup: {str(e)}")

@router.post("/login", tags=["users"], response_model=Token)
async def login(user: UserLogin):
    """User login endpoint. Returns JWT token on successful authentication."""
    try:
        db = firebase_service.db
        users_ref = db.collection('users')
        docs = users_ref.where('email', '==', user.email).get()
        
        if not docs:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        user_data = docs[0].to_dict()
        hashed_pw = user_data.get('hashed_password')
        
        if not hashed_pw or not bcrypt.checkpw(user.password.encode('utf-8'), hashed_pw.encode('utf-8')):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        # Create JWT token
        access_token = create_access_token(data={"sub": user_data["email"]})
        
        # Return token and user info (excluding password)
        user_info = User(**{k: user_data[k] for k in User.model_fields.keys() if k in user_data})
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            user=user_info
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during login: {str(e)}")

@router.get("/me", tags=["users"], response_model=User)
async def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """Get current user profile (protected endpoint)"""
    return current_user

@router.get("/users/", tags=["users"], response_model=List[User])
async def read_users(current_user: User = Depends(get_current_user)):
    """Get all users from Firestore (protected endpoint)"""
    try:
        db = firebase_service.db
        users_ref = db.collection('users')
        docs = users_ref.stream()
        
        users = []
        for doc in docs:
            user_data = doc.to_dict()
            if 'hashed_password' in user_data:
                del user_data['hashed_password']  # Remove password from response
            users.append(User(**{k: user_data[k] for k in User.model_fields.keys() if k in user_data}))
        
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching users: {str(e)}")

@router.get("/users/{email}", tags=["users"], response_model=User)
async def read_user_by_email(email: str, current_user: User = Depends(get_current_user)):
    """Get a specific user by email from Firestore (protected endpoint)"""
    try:
        db = firebase_service.db
        users_ref = db.collection('users')
        
        # Query for user by email
        query = users_ref.where('email', '==', email).limit(1)
        docs = list(query.stream())
        
        if not docs:
            raise HTTPException(status_code=404, detail="User not found")
        
        user_data = docs[0].to_dict()
        if 'hashed_password' in user_data:
            del user_data['hashed_password']  # Remove password from response
            
        return User(**{k: user_data[k] for k in User.model_fields.keys() if k in user_data})
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching user: {str(e)}")