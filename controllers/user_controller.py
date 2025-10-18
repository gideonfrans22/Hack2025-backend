"""
User Controller - Business logic for user management and authentication
"""
import os
import bcrypt
from jose import jwt
from datetime import datetime, timedelta
from typing import Optional, List
from fastapi import HTTPException, status
from dotenv import load_dotenv

from firebase_config import firebase_service
from models.user_models import User, UserSignup, UserLogin, Token

# Load environment variables
load_dotenv()

# JWT Configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-default-secret-key-change-this")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_HOURS = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_HOURS", "30"))


class UserController:
    """Controller for handling user-related business logic"""
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """
        Create JWT access token
        
        Args:
            data: Data to encode in the token
            expires_delta: Token expiration time
            
        Returns:
            Encoded JWT token
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str) -> str:
        """
        Verify JWT token and return user email
        
        Args:
            token: JWT token to verify
            
        Returns:
            User email from token
            
        Raises:
            HTTPException: If token is invalid
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        try:
            from jose import JWTError
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                raise credentials_exception
            return email
        except JWTError:
            raise credentials_exception
    
    @staticmethod
    def get_user_by_email(email: str) -> Optional[User]:
        """
        Get user from database by email
        
        Args:
            email: User email
            
        Returns:
            User object if found, None otherwise
        """
        try:
            db = firebase_service.db
            users_ref = db.collection('users')
            docs = users_ref.where('email', '==', email).get()
            
            if not docs:
                return None
                
            user_data = docs[0].to_dict()
            return User(**{k: user_data[k] for k in User.model_fields.keys() if k in user_data})
            
        except Exception:
            return None
    
    @staticmethod
    def signup(user: UserSignup) -> User:
        """
        Create a new user account
        
        Args:
            user: User signup data
            
        Returns:
            Created user object
            
        Raises:
            HTTPException: If user already exists or creation fails
        """
        try:
            db = firebase_service.db
            users_ref = db.collection('users')
            
            # Check if user already exists by email
            existing = users_ref.where('email', '==', user.email).get()
            if existing:
                raise HTTPException(
                    status_code=400, 
                    detail="User with this email already exists"
                )
            
            # Hash password
            hashed_pw = bcrypt.hashpw(
                user.password.encode('utf-8'), 
                bcrypt.gensalt()
            ).decode('utf-8')
            
            user_dict = user.dict()
            user_dict['hashed_password'] = hashed_pw
            del user_dict['password']
            
            # Store user in Firestore
            users_ref.add(user_dict)
            
            return User(**{k: user_dict[k] for k in User.model_fields.keys()})
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=f"Error during signup: {str(e)}"
            )
    
    @staticmethod
    def login(user: UserLogin) -> Token:
        """
        Authenticate user and generate JWT token
        
        Args:
            user: User login credentials
            
        Returns:
            Token with user information
            
        Raises:
            HTTPException: If authentication fails
        """
        try:
            db = firebase_service.db
            users_ref = db.collection('users')
            docs = users_ref.where('email', '==', user.email).get()
            
            if not docs:
                raise HTTPException(
                    status_code=401, 
                    detail="Invalid email or password"
                )
            
            user_data = docs[0].to_dict()
            hashed_pw = user_data.get('hashed_password')
            
            if not hashed_pw or not bcrypt.checkpw(
                user.password.encode('utf-8'), 
                hashed_pw.encode('utf-8')
            ):
                raise HTTPException(
                    status_code=401, 
                    detail="Invalid email or password"
                )
            
            # Create JWT token
            access_token = UserController.create_access_token(
                data={"sub": user_data["email"]}
            )
            
            # Return token and user info (excluding password)
            user_info = User(**{
                k: user_data[k] 
                for k in User.model_fields.keys() 
                if k in user_data
            })
            
            return Token(
                access_token=access_token,
                token_type="bearer",
                user=user_info
            )
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=f"Error during login: {str(e)}"
            )
    
    @staticmethod
    def get_all_users() -> List[User]:
        """
        Get all users from database
        
        Returns:
            List of all users
            
        Raises:
            HTTPException: If fetching fails
        """
        try:
            db = firebase_service.db
            users_ref = db.collection('users')
            docs = users_ref.stream()
            
            users = []
            for doc in docs:
                user_data = doc.to_dict()
                if 'hashed_password' in user_data:
                    del user_data['hashed_password']  # Remove password from response
                users.append(User(**{
                    k: user_data[k] 
                    for k in User.model_fields.keys() 
                    if k in user_data
                }))
            
            return users
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=f"Error fetching users: {str(e)}"
            )
    
    @staticmethod
    def get_user_by_email_detailed(email: str) -> User:
        """
        Get a specific user by email (for API endpoints)
        
        Args:
            email: User email
            
        Returns:
            User object
            
        Raises:
            HTTPException: If user not found or fetch fails
        """
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
                
            return User(**{
                k: user_data[k] 
                for k in User.model_fields.keys() 
                if k in user_data
            })
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=f"Error fetching user: {str(e)}"
            )
