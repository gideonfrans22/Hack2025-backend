# Controllers package initialization
from .user_controller import UserController
from .vocab_controller import VocabController
from .quiz_controller import QuizController

__all__ = [
    "UserController",
    "VocabController",
    "QuizController",
]
