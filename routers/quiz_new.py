"""
Quiz Routes - API endpoints for quiz generation and management
"""
from fastapi import APIRouter, Depends
from typing import List, Optional

from models.quiz_models import (
    Quiz,
    QuizRequest,
    QuizResponse,
    QuizSubmission,
    QuizResult
)
from models.user_models import User
from controllers.quiz_controller import QuizController
from routers.users_new import get_current_user

router = APIRouter()


@router.get("/test-openai")
async def test_openai_connection():
    """
    Test OpenAI connection
    
    Returns:
        Connection test result with status and message
    """
    return QuizController.test_openai_connection()


@router.post("/generate", response_model=QuizResponse)
async def generate_quiz(
    quiz_request: QuizRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Generate a personalized Korean Braille quiz based on user's vocabulary
    
    Args:
        quiz_request: Quiz generation parameters
        current_user: Current authenticated user
        
    Returns:
        Generated quiz with questions
    """
    return await QuizController.generate_quiz(quiz_request, current_user)


@router.post("/submit", response_model=QuizResult)
async def submit_quiz(
    submission: QuizSubmission,
    current_user: User = Depends(get_current_user)
):
    """
    Submit quiz answers and get results
    
    Args:
        submission: Quiz ID and user answers
        current_user: Current authenticated user
        
    Returns:
        Quiz results with score and feedback
    """
    return QuizController.submit_quiz(submission, current_user)


@router.get("/history", response_model=List[Quiz])
async def get_quiz_history(
    current_user: User = Depends(get_current_user),
    limit: Optional[int] = 10
):
    """
    Get user's quiz history
    
    Args:
        current_user: Current authenticated user
        limit: Maximum number of quizzes to return (default: 10)
        
    Returns:
        List of user's past quizzes
    """
    return QuizController.get_quiz_history(current_user, limit)


@router.get("/results", response_model=List[QuizResult])
async def get_quiz_results(
    current_user: User = Depends(get_current_user),
    limit: Optional[int] = 10
):
    """
    Get user's quiz results
    
    Args:
        current_user: Current authenticated user
        limit: Maximum number of results to return (default: 10)
        
    Returns:
        List of user's quiz results with scores
    """
    return QuizController.get_quiz_results(current_user, limit)


@router.get("/{quiz_id}", response_model=Quiz)
async def get_quiz(
    quiz_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific quiz by ID
    
    Args:
        quiz_id: Quiz ID to retrieve
        current_user: Current authenticated user
        
    Returns:
        Quiz details with all questions
    """
    return QuizController.get_quiz_by_id(quiz_id, current_user)
