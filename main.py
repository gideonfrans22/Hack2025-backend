from typing import Union
import os
from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Import new structured routers
from routers import users_new, quiz_new, vocab_library_new, braille_library
from firebase_config import firebase_service

# Load environment variables
load_dotenv()

app = FastAPI(
    title="ReadAble - Korean Braille Learning Platform",
    version="2.0.0",
    description="AI-powered Korean Braille learning platform with personalized quizzes and vocabulary tracking"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Firebase on startup
@app.on_event("startup")
async def startup_event():
    """Initialize Firebase service on application startup"""
    service_account_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    firebase_service.initialize_firebase(service_account_path)

# Include routers with proper prefixes
app.include_router(users_new.router, prefix="/api/v1", tags=["users"])
app.include_router(quiz_new.router, prefix="/api/v1/quiz", tags=["quiz"])
app.include_router(vocab_library_new.router, prefix="/api/v1", tags=["vocabulary"])
app.include_router(braille_library.router, tags=["braille_library"])

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
def read_root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to ReadAble API",
        "version": "2.0.0",
        "description": "Korean Braille Learning Platform",
        "docs": "/docs",
        "firebase": "Integrated"
    }


@app.get("/health")
def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "service": "ReadAble API",
        "version": "2.0.0"
    }


@app.get("/firebase-status")
def firebase_status():
    """Check if Firebase is properly initialized"""
    try:
        db = firebase_service.db
        return {
            "status": "Firebase connected successfully", 
            "firestore": "available"
        }
    except Exception as e:
        return {
            "status": "Firebase not initialized", 
            "error": str(e)
        }



@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id, "price": item.price}