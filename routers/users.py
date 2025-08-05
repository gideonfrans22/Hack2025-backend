from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
import sys
import os

# Add parent directory to path to import firebase_config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from firebase_config import firebase_service

router = APIRouter()

class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None

class UserCreate(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None

@router.get("/users/", tags=["users"], response_model=List[User])
async def read_users():
    """Get all users from Firestore"""
    try:
        db = firebase_service.db
        users_ref = db.collection('users')
        docs = users_ref.stream()
        
        users = []
        for doc in docs:
            user_data = doc.to_dict()
            user_data['id'] = doc.id
            users.append(user_data)
        
        # Return sample data if no users in Firestore yet
        if not users:
            return [
                {"username": "Rick", "email": "rick@example.com", "full_name": "Rick Sanchez"},
                {"username": "Morty", "email": "morty@example.com", "full_name": "Morty Smith"}
            ]
        
        return users
    except Exception as e:
        # Fallback to sample data if Firebase is not available
        return [
            {"username": "Rick", "email": "rick@example.com", "full_name": "Rick Sanchez"},
            {"username": "Morty", "email": "morty@example.com", "full_name": "Morty Smith"}
        ]


@router.post("/users/", tags=["users"], response_model=User)
async def create_user(user: UserCreate):
    """Create a new user in Firestore"""
    try:
        db = firebase_service.db
        users_ref = db.collection('users')
        
        # Check if user already exists
        existing_users = users_ref.where('username', '==', user.username).get()
        if existing_users:
            raise HTTPException(status_code=400, detail="User already exists")
        
        # Create new user document
        user_dict = user.dict()
        doc_ref = users_ref.add(user_dict)
        
        return user_dict
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")


@router.get("/users/me", tags=["users"])
async def read_user_me():
    return {"username": "fakecurrentuser"}


@router.get("/users/{username}", tags=["users"], response_model=User)
async def read_user(username: str):
    """Get a specific user by username from Firestore"""
    try:
        db = firebase_service.db
        users_ref = db.collection('users')
        
        # Query for user by username
        query = users_ref.where('username', '==', username).limit(1)
        docs = list(query.stream())
        
        if not docs:
            raise HTTPException(status_code=404, detail="User not found")
        
        user_data = docs[0].to_dict()
        user_data['id'] = docs[0].id
        return user_data
        
    except HTTPException:
        raise
    except Exception as e:
        # Fallback response if Firebase is not available
        return {"username": username, "email": f"{username}@example.com", "full_name": f"User {username}"}