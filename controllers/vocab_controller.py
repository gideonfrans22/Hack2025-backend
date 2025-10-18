"""
Vocabulary Controller - Business logic for vocabulary management
"""
from typing import List, Optional, Dict
from datetime import datetime
from fastapi import HTTPException

from firebase_config import firebase_service
from models.vocab_models import (
    VocabularyCreate,
    VocabularyResponse,
    VocabularyStats,
    VocabType,
    DifficultyLevel
)
from models.user_models import User


class VocabController:
    """Controller for handling vocabulary-related business logic"""
    
    @staticmethod
    def create_vocabulary_item(
        vocab_item: VocabularyCreate, 
        user: User
    ) -> VocabularyResponse:
        """
        Create a new vocabulary item for a user
        
        Args:
            vocab_item: Vocabulary item data
            user: Current user
            
        Returns:
            Created vocabulary item
            
        Raises:
            HTTPException: If item already exists or creation fails
        """
        try:
            db = firebase_service.db
            vocab_ref = db.collection('user_vocabulary')
            
            # Check if the item already exists for this user
            existing_query = vocab_ref.where('user_email', '==', user.email)\
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
                "user_email": user.email,
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
            raise HTTPException(
                status_code=500, 
                detail=f"Error registering vocabulary: {str(e)}"
            )
    
    @staticmethod
    def get_vocabulary_items(
        user: User,
        vocab_type: Optional[VocabType] = None,
        difficulty_level: Optional[DifficultyLevel] = None,
        limit: Optional[int] = None
    ) -> List[VocabularyResponse]:
        """
        Get vocabulary items for a user with optional filters
        
        Args:
            user: Current user
            vocab_type: Filter by vocabulary type
            difficulty_level: Filter by difficulty level
            limit: Maximum number of items to return
            
        Returns:
            List of vocabulary items
            
        Raises:
            HTTPException: If fetching fails
        """
        try:
            db = firebase_service.db
            vocab_ref = db.collection('user_vocabulary')
            
            # Start with user filter
            query = vocab_ref.where('user_email', '==', user.email)
            
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
            raise HTTPException(
                status_code=500, 
                detail=f"Error fetching vocabulary: {str(e)}"
            )
    
    @staticmethod
    def get_vocabulary_stats(user: User) -> VocabularyStats:
        """
        Get vocabulary learning statistics for a user
        
        Args:
            user: Current user
            
        Returns:
            Vocabulary statistics
            
        Raises:
            HTTPException: If fetching fails
        """
        try:
            db = firebase_service.db
            vocab_ref = db.collection('user_vocabulary')
            
            # Get all vocabulary items for the user
            user_vocab = vocab_ref.where('user_email', '==', user.email).get()
            
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
            raise HTTPException(
                status_code=500, 
                detail=f"Error fetching vocabulary stats: {str(e)}"
            )
    
    @staticmethod
    def delete_vocabulary_item(vocab_id: str, user: User) -> Dict[str, str]:
        """
        Delete a vocabulary item (only if it belongs to the user)
        
        Args:
            vocab_id: Vocabulary item ID
            user: Current user
            
        Returns:
            Success message
            
        Raises:
            HTTPException: If item not found or user not authorized
        """
        try:
            db = firebase_service.db
            vocab_ref = db.collection('user_vocabulary')
            
            # Get the document
            doc = vocab_ref.document(vocab_id).get()
            
            if not doc.exists:
                raise HTTPException(
                    status_code=404, 
                    detail="Vocabulary item not found"
                )
            
            # Check if it belongs to the current user
            vocab_data = doc.to_dict()
            if vocab_data.get('user_email') != user.email:
                raise HTTPException(
                    status_code=403, 
                    detail="Not authorized to delete this vocabulary item"
                )
            
            # Delete the document
            vocab_ref.document(vocab_id).delete()
            
            return {"message": "Vocabulary item deleted successfully"}
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=f"Error deleting vocabulary item: {str(e)}"
            )
    
    @staticmethod
    def search_vocabulary(
        query: str,
        user: User,
        vocab_type: Optional[VocabType] = None
    ) -> List[VocabularyResponse]:
        """
        Search vocabulary items by content
        
        Args:
            query: Search query string
            user: Current user
            vocab_type: Optional filter by vocabulary type
            
        Returns:
            List of matching vocabulary items
            
        Raises:
            HTTPException: If search fails
        """
        try:
            db = firebase_service.db
            vocab_ref = db.collection('user_vocabulary')
            
            # Get all user's vocabulary items (Firestore doesn't support text search natively)
            user_query = vocab_ref.where('user_email', '==', user.email)
            
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
            raise HTTPException(
                status_code=500, 
                detail=f"Error searching vocabulary: {str(e)}"
            )
