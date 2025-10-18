"""
Vocabulary library data models
"""
from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime
from enum import Enum


class DifficultyLevel(str, Enum):
    """Difficulty levels for vocabulary items"""
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"


class VocabType(str, Enum):
    """Types of vocabulary items"""
    character = "character"
    word = "word"


class VocabularyItem(BaseModel):
    """Base vocabulary item model"""
    content: str  # The character or word
    vocab_type: VocabType
    difficulty_level: DifficultyLevel
    braille_representation: Optional[str] = None
    learned_at: Optional[datetime] = None


class VocabularyCreate(BaseModel):
    """Vocabulary creation request model"""
    content: str
    vocab_type: VocabType
    difficulty_level: DifficultyLevel
    braille_representation: Optional[str] = None


class VocabularyResponse(VocabularyItem):
    """Vocabulary response model with ID and user email"""
    id: str
    user_email: str


class VocabularyStats(BaseModel):
    """Vocabulary learning statistics model"""
    total_characters: int
    total_words: int
    characters_by_difficulty: Dict[str, int]
    words_by_difficulty: Dict[str, int]
    total_items: int
