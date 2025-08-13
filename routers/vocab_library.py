from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
import sys
import os
from enum import Enum

# Add parent directory to path to import firebase_config and users
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from firebase_config import firebase_service
from routers.users import get_current_user, User

router = APIRouter()

class DifficultyLevel(str, Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"

class VocabType(str, Enum):
    character = "character"
    word = "word"

class VocabularyItem(BaseModel):
    content: str  # The character or word
    vocab_type: VocabType
    difficulty_level: DifficultyLevel
    braille_representation: Optional[str] = None
    learned_at: Optional[datetime] = None

class VocabularyCreate(BaseModel):
    content: str
    vocab_type: VocabType
    difficulty_level: DifficultyLevel
    braille_representation: Optional[str] = None

class VocabularyResponse(VocabularyItem):
    id: str
    user_email: str

class VocabularyStats(BaseModel):
    total_characters: int
    total_words: int
    characters_by_difficulty: Dict[str, int]
    words_by_difficulty: Dict[str, int]
    total_items: int

@router.post("/vocabulary", tags=["vocabulary"], response_model=VocabularyResponse)
async def register_learned_vocabulary(
    vocab_item: VocabularyCreate,
    current_user: User = Depends(get_current_user)
):
    """Register a new learned character or word for the current user"""
    try:
        db = firebase_service.db
        vocab_ref = db.collection('user_vocabulary')
        
        # Check if the item already exists for this user
        existing_query = vocab_ref.where('user_email', '==', current_user.email)\
                                 .where('content', '==', vocab_item.content)\
                                 .where('vocab_type', '==', vocab_item.vocab_type.value)
        existing_docs = existing_query.get()
        
        if existing_docs:
            raise HTTPException(
                status_code=400, 
                detail=f"This {vocab_item.vocab_type.value} is already in your vocabulary library"
            )
        
        # Create new vocabulary item
        vocab_data = {
            "user_email": current_user.email,
            "content": vocab_item.content,
            "vocab_type": vocab_item.vocab_type.value,
            "difficulty_level": vocab_item.difficulty_level.value,
            "braille_representation": vocab_item.braille_representation,
            "learned_at": datetime.utcnow()
        }
        
        # Add to Firestore
        doc_ref = vocab_ref.add(vocab_data)
        vocab_data["id"] = doc_ref[1].id
        
        return VocabularyResponse(**vocab_data)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error registering vocabulary: {str(e)}")

@router.get("/vocabulary", tags=["vocabulary"], response_model=List[VocabularyResponse])
async def get_learned_vocabulary(
    vocab_type: Optional[VocabType] = None,
    difficulty_level: Optional[DifficultyLevel] = None,
    limit: Optional[int] = None,
    current_user: User = Depends(get_current_user)
):
    """Get list of learned characters and words for the current user"""
    try:
        db = firebase_service.db
        vocab_ref = db.collection('user_vocabulary')
        
        # Start with user filter
        query = vocab_ref.where('user_email', '==', current_user.email)
        
        # Add filters if provided
        if vocab_type:
            query = query.where('vocab_type', '==', vocab_type.value)
        if difficulty_level:
            query = query.where('difficulty_level', '==', difficulty_level.value)
        
        # Order by learned_at (most recent first)
        query = query.order_by('learned_at', direction='DESCENDING')
        
        # Apply limit if provided
        if limit:
            query = query.limit(limit)
        
        docs = query.get()
        
        vocabulary_items = []
        for doc in docs:
            vocab_data = doc.to_dict()
            vocab_data["id"] = doc.id
            vocabulary_items.append(VocabularyResponse(**vocab_data))
        
        return vocabulary_items
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching vocabulary: {str(e)}")

@router.get("/vocabulary/characters", tags=["vocabulary"], response_model=List[VocabularyResponse])
async def get_learned_characters(
    difficulty_level: Optional[DifficultyLevel] = None,
    current_user: User = Depends(get_current_user)
):
    """Get list of learned characters for the current user"""
    return await get_learned_vocabulary(
        vocab_type=VocabType.character,
        difficulty_level=difficulty_level,
        current_user=current_user
    )

@router.get("/vocabulary/words", tags=["vocabulary"], response_model=List[VocabularyResponse])
async def get_learned_words(
    difficulty_level: Optional[DifficultyLevel] = None,
    current_user: User = Depends(get_current_user)
):
    """Get list of learned words for the current user"""
    return await get_learned_vocabulary(
        vocab_type=VocabType.word,
        difficulty_level=difficulty_level,
        current_user=current_user
    )

@router.get("/vocabulary/stats", tags=["vocabulary"], response_model=VocabularyStats)
async def get_vocabulary_stats(current_user: User = Depends(get_current_user)):
    """Get vocabulary learning statistics for the current user"""
    try:
        db = firebase_service.db
        vocab_ref = db.collection('user_vocabulary')
        
        # Get all vocabulary items for the user
        user_vocab = vocab_ref.where('user_email', '==', current_user.email).get()
        
        # Initialize counters
        total_characters = 0
        total_words = 0
        characters_by_difficulty = {"beginner": 0, "intermediate": 0, "advanced": 0}
        words_by_difficulty = {"beginner": 0, "intermediate": 0, "advanced": 0}
        
        # Count items
        for doc in user_vocab:
            data = doc.to_dict()
            vocab_type = data.get('vocab_type')
            difficulty = data.get('difficulty_level', 'beginner')
            
            if vocab_type == 'character':
                total_characters += 1
                if difficulty in characters_by_difficulty:
                    characters_by_difficulty[difficulty] += 1
            elif vocab_type == 'word':
                total_words += 1
                if difficulty in words_by_difficulty:
                    words_by_difficulty[difficulty] += 1
        
        return VocabularyStats(
            total_characters=total_characters,
            total_words=total_words,
            characters_by_difficulty=characters_by_difficulty,
            words_by_difficulty=words_by_difficulty,
            total_items=total_characters + total_words
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching vocabulary stats: {str(e)}")

@router.delete("/vocabulary/{vocab_id}", tags=["vocabulary"])
async def delete_vocabulary_item(
    vocab_id: str,
    current_user: User = Depends(get_current_user)
):
    """Delete a vocabulary item (only if it belongs to the current user)"""
    try:
        db = firebase_service.db
        vocab_ref = db.collection('user_vocabulary')
        
        # Get the document
        doc = vocab_ref.document(vocab_id).get()
        
        if not doc.exists:
            raise HTTPException(status_code=404, detail="Vocabulary item not found")
        
        # Check if it belongs to the current user
        vocab_data = doc.to_dict()
        if vocab_data.get('user_email') != current_user.email:
            raise HTTPException(status_code=403, detail="Not authorized to delete this vocabulary item")
        
        # Delete the document
        vocab_ref.document(vocab_id).delete()
        
        return {"message": "Vocabulary item deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting vocabulary item: {str(e)}")

@router.get("/vocabulary/search", tags=["vocabulary"], response_model=List[VocabularyResponse])
async def search_vocabulary(
    query: str,
    vocab_type: Optional[VocabType] = None,
    current_user: User = Depends(get_current_user)
):
    """Search vocabulary items by content"""
    try:
        db = firebase_service.db
        vocab_ref = db.collection('user_vocabulary')
        
        # Get all user's vocabulary items (Firestore doesn't support text search natively)
        user_query = vocab_ref.where('user_email', '==', current_user.email)
        
        if vocab_type:
            user_query = user_query.where('vocab_type', '==', vocab_type.value)
        
        docs = user_query.get()
        
        # Filter results based on search query
        matching_items = []
        query_lower = query.lower()
        
        for doc in docs:
            vocab_data = doc.to_dict()
            content = vocab_data.get('content', '').lower()
            
            if query_lower in content:
                vocab_data["id"] = doc.id
                matching_items.append(VocabularyResponse(**vocab_data))
        
        return matching_items
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching vocabulary: {str(e)}")