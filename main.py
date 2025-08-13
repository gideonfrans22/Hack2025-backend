from typing import Union
import os
from dotenv import load_dotenv

from fastapi import FastAPI
from pydantic import BaseModel
from routers import users, quiz, vocab_library
from firebase_config import firebase_service

# Load environment variables
load_dotenv()

app = FastAPI(title="Hackathon 2025 Backend", version="1.0.0")

# Initialize Firebase on startup
@app.on_event("startup")
async def startup_event():
    # Try to initialize Firebase with service account file
    service_account_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    firebase_service.initialize_firebase(service_account_path)

app.include_router(users.router, prefix="/api/v1", tags=["users"])
app.include_router(quiz.router, prefix="/api/v1", tags=["quiz"])
app.include_router(vocab_library.router, prefix="/api/v1", tags=["vocabulary"])

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
def read_root():
    return {"Hello": "World", "Firebase": "Integrated"}


@app.get("/firebase-status")
def firebase_status():
    """Check if Firebase is properly initialized"""
    try:
        # Try to access Firestore
        db = firebase_service.db
        return {"status": "Firebase connected successfully", "firestore": "available"}
    except Exception as e:
        return {"status": "Firebase not initialized", "error": str(e)}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id, "price": item.price}