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
from models.user_models import (
    User, UserSignup, UserLogin, Token, 
    KakaoLogin, NaverLogin, UserProfileUpdate,
    OAuthLoginResponse, UserProfile
)

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
            
            # Add default values for OAuth fields (for regular signup)
            user_dict['nickname'] = user_dict.get('nickname') or user_dict.get('name')
            user_dict['profile_image'] = user_dict.get('profile_image')
            user_dict['oauth_provider'] = None
            user_dict['oauth_id'] = None
            user_dict['created_at'] = datetime.utcnow()
            user_dict['updated_at'] = datetime.utcnow()
            
            # Store user in Firestore
            users_ref.add(user_dict)
            
            # Return User object with only the fields it expects
            return User(**{k: user_dict[k] for k in User.model_fields.keys() if k in user_dict})
            
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
    
    @staticmethod
    def kakao_login(kakao_data: KakaoLogin) -> OAuthLoginResponse:
        """
        Authenticate user with Kakao OAuth
        
        Args:
            kakao_data: Kakao login data
            
        Returns:
            OAuth login response with token and user info
            
        Raises:
            HTTPException: If authentication fails
        """
        try:
            db = firebase_service.db
            users_ref = db.collection('users')
            
            # Check if user exists by kakao_id or email
            existing_docs = users_ref.where('oauth_id', '==', kakao_data.kakao_id).where('oauth_provider', '==', 'kakao').get()
            
            is_new_user = False
            
            if not existing_docs:
                # Check by email
                email_docs = users_ref.where('email', '==', kakao_data.email).get()
                
                if email_docs:
                    # User exists with same email but different OAuth provider
                    # Update existing user with Kakao info
                    doc = email_docs[0]
                    user_data = doc.to_dict()
                    user_id = doc.id
                    
                    # Update with Kakao OAuth info
                    users_ref.document(user_id).update({
                        'oauth_provider': 'kakao',
                        'oauth_id': kakao_data.kakao_id,
                        'nickname': kakao_data.nickname,
                        'profile_image': kakao_data.profile_image,
                        'updated_at': datetime.utcnow()
                    })
                else:
                    # Create new user
                    is_new_user = True
                    user_dict = {
                        'email': kakao_data.email,
                        'nickname': kakao_data.nickname,
                        'name': kakao_data.nickname,  # Use nickname as name initially
                        'profile_image': kakao_data.profile_image,
                        'oauth_provider': 'kakao',
                        'oauth_id': kakao_data.kakao_id,
                        'age': 0,  # Default, should be updated later
                        'gender': '',  # Default, should be updated later
                        'created_at': datetime.utcnow(),
                        'updated_at': datetime.utcnow()
                    }
                    doc_ref = users_ref.add(user_dict)
                    user_id = doc_ref[1].id
                    user_data = user_dict
            else:
                # User exists, update last login
                doc = existing_docs[0]
                user_data = doc.to_dict()
                user_id = doc.id
                
                users_ref.document(user_id).update({
                    'updated_at': datetime.utcnow(),
                    'nickname': kakao_data.nickname,
                    'profile_image': kakao_data.profile_image
                })
            
            # Create JWT token
            access_token = UserController.create_access_token(
                data={"sub": user_data["email"], "user_id": user_id}
            )
            
            # Return response
            return OAuthLoginResponse(
                success=True,
                data={
                    "token": access_token,
                    "user": {
                        "id": user_id,
                        "email": user_data.get("email"),
                        "nickname": user_data.get("nickname"),
                        "profile_image": user_data.get("profile_image")
                    },
                    "is_new_user": is_new_user
                }
            )
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error during Kakao login: {str(e)}"
            )
    
    @staticmethod
    def naver_login(naver_data: NaverLogin) -> OAuthLoginResponse:
        """
        Authenticate user with Naver OAuth
        
        Args:
            naver_data: Naver login data
            
        Returns:
            OAuth login response with token and user info
            
        Raises:
            HTTPException: If authentication fails
        """
        try:
            db = firebase_service.db
            users_ref = db.collection('users')
            
            # Check if user exists by naver_id or email
            existing_docs = users_ref.where('oauth_id', '==', naver_data.naver_id).where('oauth_provider', '==', 'naver').get()
            
            is_new_user = False
            
            if not existing_docs:
                # Check by email
                email_docs = users_ref.where('email', '==', naver_data.email).get()
                
                if email_docs:
                    # User exists with same email but different OAuth provider
                    # Update existing user with Naver info
                    doc = email_docs[0]
                    user_data = doc.to_dict()
                    user_id = doc.id
                    
                    # Update with Naver OAuth info
                    users_ref.document(user_id).update({
                        'oauth_provider': 'naver',
                        'oauth_id': naver_data.naver_id,
                        'nickname': naver_data.nickname,
                        'profile_image': naver_data.profile_image,
                        'updated_at': datetime.utcnow()
                    })
                else:
                    # Create new user
                    is_new_user = True
                    user_dict = {
                        'email': naver_data.email,
                        'nickname': naver_data.nickname,
                        'name': naver_data.nickname,  # Use nickname as name initially
                        'profile_image': naver_data.profile_image,
                        'oauth_provider': 'naver',
                        'oauth_id': naver_data.naver_id,
                        'age': 0,  # Default, should be updated later
                        'gender': '',  # Default, should be updated later
                        'created_at': datetime.utcnow(),
                        'updated_at': datetime.utcnow()
                    }
                    doc_ref = users_ref.add(user_dict)
                    user_id = doc_ref[1].id
                    user_data = user_dict
            else:
                # User exists, update last login
                doc = existing_docs[0]
                user_data = doc.to_dict()
                user_id = doc.id
                
                users_ref.document(user_id).update({
                    'updated_at': datetime.utcnow(),
                    'nickname': naver_data.nickname,
                    'profile_image': naver_data.profile_image
                })
            
            # Create JWT token
            access_token = UserController.create_access_token(
                data={"sub": user_data["email"], "user_id": user_id}
            )
            
            # Return response
            return OAuthLoginResponse(
                success=True,
                data={
                    "token": access_token,
                    "user": {
                        "id": user_id,
                        "email": user_data.get("email"),
                        "nickname": user_data.get("nickname"),
                        "profile_image": user_data.get("profile_image")
                    },
                    "is_new_user": is_new_user
                }
            )
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error during Naver login: {str(e)}"
            )
    
    @staticmethod
    def update_profile(email: str, profile_data: UserProfileUpdate) -> UserProfile:
        """
        Update user profile
        
        Args:
            email: User email from JWT token
            profile_data: Profile update data
            
        Returns:
            Updated user profile
            
        Raises:
            HTTPException: If update fails
        """
        try:
            db = firebase_service.db
            users_ref = db.collection('users')
            
            # Find user by email
            docs = users_ref.where('email', '==', email).get()
            
            if not docs:
                raise HTTPException(status_code=404, detail="User not found")
            
            doc = docs[0]
            user_id = doc.id
            user_data = doc.to_dict()
            
            # Prepare update data (only non-None fields)
            update_data = {
                k: v for k, v in profile_data.dict().items() 
                if v is not None
            }
            update_data['updated_at'] = datetime.utcnow()
            
            # Update user in Firestore
            users_ref.document(user_id).update(update_data)
            
            # Get updated user data
            updated_doc = users_ref.document(user_id).get()
            updated_data = updated_doc.to_dict()
            
            return UserProfile(
                id=user_id,
                email=updated_data.get('email'),
                nickname=updated_data.get('nickname'),
                name=updated_data.get('name'),
                profile_image=updated_data.get('profile_image'),
                oauth_provider=updated_data.get('oauth_provider')
            )
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error updating profile: {str(e)}"
            )
