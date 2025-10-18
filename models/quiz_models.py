"""
Quiz generation and management data models
"""
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime


class QuizDifficulty(str):
    """Quiz difficulty levels"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class QuizType(str):
    """Quiz types"""
    MULTIPLE_CHOICE = "multiple_choice"
    TRUE_FALSE = "true_false"
    FILL_BLANK = "fill_blank"


class QuizQuestion(BaseModel):
    """Individual quiz question model"""
    question: str
    options: Optional[List[str]] = None  # For multiple choice
    correct_answer: str
    explanation: str
    braille_content: Optional[str] = None


class Quiz(BaseModel):
    """Complete quiz model"""
    id: Optional[str] = None
    user_email: str
    title: str
    questions: List[QuizQuestion]
    difficulty_level: str
    quiz_type: str
    created_at: datetime
    based_on_vocabulary: List[str]  # List of vocabulary items used


class QuizRequest(BaseModel):
    """Quiz generation request model"""
    difficulty_level: Optional[str] = "beginner"
    quiz_type: Optional[str] = "multiple_choice"
    num_questions: Optional[int] = 5
    focus_words: Optional[List[str]] = None  # Specific words to focus on


class QuizResponse(BaseModel):
    """Quiz generation response model"""
    quiz: Quiz
    message: str


class QuizAnswer(BaseModel):
    """Single quiz answer submission"""
    question_index: int
    user_answer: str


class QuizSubmission(BaseModel):
    """Complete quiz submission model"""
    quiz_id: str
    answers: List[QuizAnswer]


class QuizResult(BaseModel):
    """Quiz result model"""
    quiz_id: str
    score: int
    total_questions: int
    percentage: float
    feedback: List[Dict[str, Any]]
    completed_at: datetime
