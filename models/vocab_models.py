"""
Vocabulary library data models
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, List
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
    braille_representation: Optional[List[List[int]]] = Field(
        default=None,
        description="Electronic braille notation: list of cells, each cell is a list of active dots (1-6). "
                    "Dot numbering: 1=top-left, 2=middle-left, 3=bottom-left, 4=top-right, 5=middle-right, 6=bottom-right. "
                    "Example: [[4]] for 'ㄱ', [[1,2,4,5], [2,4]] for '가다'"
    )
    learned_at: Optional[datetime] = None


class VocabularyCreate(BaseModel):
    """Vocabulary creation request model"""
    content: str
    vocab_type: VocabType
    difficulty_level: DifficultyLevel
    braille_representation: Optional[List[List[int]]] = Field(
        default=None,
        description="Electronic braille notation: list of cells, each cell is a list of active dots (1-6). "
                    "Example: [[4]] for 'ㄱ', [[1,2,4,5], [2,4]] for '가다'"
    )


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
