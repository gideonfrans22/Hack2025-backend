"""
Vocabulary Routes - API endpoints for vocabulary library management
"""
from fastapi import APIRouter, Depends
from typing import List, Optional

from models.vocab_models import (
    VocabularyCreate,
    VocabularyResponse,
    VocabularyStats,
    VocabType,
    DifficultyLevel
)
from models.user_models import User
from controllers.vocab_controller import VocabController
from routers.users_new import get_current_user

router = APIRouter()


@router.post("/vocabulary", response_model=VocabularyResponse)
async def register_learned_vocabulary(
    vocab_item: VocabularyCreate,
    current_user: User = Depends(get_current_user)
):
    """
    Register a new learned character or word for the current user
    
    Args:
        vocab_item: Vocabulary item data
        current_user: Current authenticated user
        
    Returns:
        Created vocabulary item with ID
    """
    return VocabController.create_vocabulary_item(vocab_item, current_user)


@router.get("/vocabulary", response_model=List[VocabularyResponse])
async def get_learned_vocabulary(
    vocab_type: Optional[VocabType] = None,
    difficulty_level: Optional[DifficultyLevel] = None,
    limit: Optional[int] = None,
    current_user: User = Depends(get_current_user)
):
    """
    Get list of learned characters and words for the current user
    
    Args:
        vocab_type: Optional filter by vocabulary type (character/word)
        difficulty_level: Optional filter by difficulty level
        limit: Optional maximum number of items to return
        current_user: Current authenticated user
        
    Returns:
        List of vocabulary items
    """
    return VocabController.get_vocabulary_items(
        current_user, 
        vocab_type, 
        difficulty_level, 
        limit
    )


@router.get("/vocabulary/characters", response_model=List[VocabularyResponse])
async def get_learned_characters(
    difficulty_level: Optional[DifficultyLevel] = None,
    current_user: User = Depends(get_current_user)
):
    """
    Get list of learned characters for the current user
    
    Args:
        difficulty_level: Optional filter by difficulty level
        current_user: Current authenticated user
        
    Returns:
        List of character vocabulary items
    """
    return VocabController.get_vocabulary_items(
        current_user,
        vocab_type=VocabType.character,
        difficulty_level=difficulty_level
    )


@router.get("/vocabulary/words", response_model=List[VocabularyResponse])
async def get_learned_words(
    difficulty_level: Optional[DifficultyLevel] = None,
    current_user: User = Depends(get_current_user)
):
    """
    Get list of learned words for the current user
    
    Args:
        difficulty_level: Optional filter by difficulty level
        current_user: Current authenticated user
        
    Returns:
        List of word vocabulary items
    """
    return VocabController.get_vocabulary_items(
        current_user,
        vocab_type=VocabType.word,
        difficulty_level=difficulty_level
    )


@router.get("/vocabulary/stats", response_model=VocabularyStats)
async def get_vocabulary_stats(current_user: User = Depends(get_current_user)):
    """
    Get vocabulary learning statistics for the current user
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        Vocabulary statistics including counts by difficulty
    """
    return VocabController.get_vocabulary_stats(current_user)


@router.delete("/vocabulary/{vocab_id}")
async def delete_vocabulary_item(
    vocab_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Delete a vocabulary item (only if it belongs to the current user)
    
    Args:
        vocab_id: Vocabulary item ID to delete
        current_user: Current authenticated user
        
    Returns:
        Success message
    """
    return VocabController.delete_vocabulary_item(vocab_id, current_user)


@router.get("/vocabulary/search", response_model=List[VocabularyResponse])
async def search_vocabulary(
    query: str,
    vocab_type: Optional[VocabType] = None,
    current_user: User = Depends(get_current_user)
):
    """
    Search vocabulary items by content
    
    Args:
        query: Search query string
        vocab_type: Optional filter by vocabulary type
        current_user: Current authenticated user
        
    Returns:
        List of matching vocabulary items
    """
    return VocabController.search_vocabulary(query, current_user, vocab_type)
