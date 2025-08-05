from fastapi import APIRouter, HTTPException, Depends
from typing import List
from pydantic import BaseModel

router = APIRouter(prefix="/quiz", tags=["quiz"])

# Example Pydantic models (adjust fields as per your README)
class QuizCreate(BaseModel):
    title: str

class Quiz(BaseModel):
    id: int
    title: str
    description: str

class QuizUpdate(BaseModel):
    title: str = None
    description: str = None

# Dummy in-memory storage
quizzes = []
quiz_id_counter = 1

@router.post("/", response_model=Quiz)
def create_quiz(quiz: QuizCreate):
    global quiz_id_counter
    new_quiz = Quiz(id=quiz_id_counter, title=quiz.title, description=quiz.description)
    quizzes.append(new_quiz)
    quiz_id_counter += 1
    return new_quiz

@router.get("/", response_model=List[Quiz])
def list_quizzes():
    return quizzes

@router.get("/{quiz_id}", response_model=Quiz)
def get_quiz(quiz_id: int):
    for quiz in quizzes:
        if quiz.id == quiz_id:
            return quiz
    raise HTTPException(status_code=404, detail="Quiz not found")

@router.put("/{quiz_id}", response_model=Quiz)
def update_quiz(quiz_id: int, quiz_update: QuizUpdate):
    for quiz in quizzes:
        if quiz.id == quiz_id:
            if quiz_update.title is not None:
                quiz.title = quiz_update.title
            if quiz_update.description is not None:
                quiz.description = quiz_update.description
            return quiz
    raise HTTPException(status_code=404, detail="Quiz not found")

@router.delete("/{quiz_id}", response_model=dict)
def delete_quiz(quiz_id: int):
    for i, quiz in enumerate(quizzes):
        if quiz.id == quiz_id:
            quizzes.pop(i)
            return {"detail": "Quiz deleted"}
    raise HTTPException(status_code=404, detail="Quiz not found")