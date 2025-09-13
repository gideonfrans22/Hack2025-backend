from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
import sys
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Add parent directory to path to import dependencies
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from firebase_config import firebase_service
from routers.users import get_current_user, User

router = APIRouter()

# Configure OpenAI
from openai import OpenAI

def get_openai_client():
    """Get OpenAI client with proper error handling"""
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        return None
    
    try:
        # For OpenAI v1.x, create client instance
        client = OpenAI(api_key=openai_api_key)
        return client
    except Exception as e:
        print(f"Warning: Failed to initialize OpenAI client: {e}")
        return None

# Initialize client as None, will be set when needed
client = None

class QuizDifficulty(str):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class QuizType(str):
    MULTIPLE_CHOICE = "multiple_choice"
    TRUE_FALSE = "true_false"
    FILL_BLANK = "fill_blank"

class QuizQuestion(BaseModel):
    question: str
    options: Optional[List[str]] = None  # For multiple choice
    correct_answer: str
    explanation: str
    braille_content: Optional[str] = None

class Quiz(BaseModel):
    id: Optional[str] = None
    user_email: str
    title: str
    questions: List[QuizQuestion]
    difficulty_level: str
    quiz_type: str
    created_at: datetime
    based_on_vocabulary: List[str]  # List of vocabulary items used

class QuizRequest(BaseModel):
    difficulty_level: Optional[str] = "beginner"
    quiz_type: Optional[str] = "multiple_choice"
    num_questions: Optional[int] = 5
    focus_words: Optional[List[str]] = None  # Specific words to focus on

class QuizResponse(BaseModel):
    quiz: Quiz
    message: str

class QuizAnswer(BaseModel):
    question_index: int
    user_answer: str

class QuizSubmission(BaseModel):
    quiz_id: str
    answers: List[QuizAnswer]

class QuizResult(BaseModel):
    quiz_id: str
    score: int
    total_questions: int
    percentage: float
    feedback: List[Dict[str, Any]]
    completed_at: datetime

async def get_user_vocabulary(user_email: str, difficulty_level: str = None) -> List[Dict]:
    """Get user's learned vocabulary from Firestore"""
    try:
        db = firebase_service.db
        vocab_ref = db.collection('user_vocabulary')
        
        query = vocab_ref.where('user_email', '==', user_email)
        if difficulty_level:
            query = query.where('difficulty_level', '==', difficulty_level)
        
        docs = query.get()
        vocabulary = []
        
        for doc in docs:
            vocab_data = doc.to_dict()
            vocabulary.append(vocab_data)
        
        return vocabulary
    except Exception as e:
        print(f"Error fetching vocabulary: {e}")
        return []

async def generate_quiz_with_ai(vocabulary: List[Dict], quiz_request: QuizRequest, user_profile: User) -> Quiz:
    """Generate quiz using OpenAI based on user's vocabulary"""
    
    if not vocabulary:
        # If no vocabulary, create basic Korean quiz
        vocabulary_text = "기본 한국어 단어: 안녕, 사랑, 친구, 가족, 학교"
    else:
        # Extract vocabulary content
        vocab_words = [item.get('content', '') for item in vocabulary[:20]]  # Limit to 20 words
        vocabulary_text = ", ".join(vocab_words)
    
    # Create prompt based on user preferences and vocabulary
    prompt = f"""
사용자 정보:
- 이름: {user_profile.name}
- 나이: {user_profile.age}
- 관심사: {user_profile.hobby or '일반'}
- 학습한 단어들: {vocabulary_text}

다음 조건에 맞는 한국어 점자 학습 퀴즈를 {quiz_request.num_questions}문제 생성해주세요:

1. 난이도: {quiz_request.difficulty_level}
2. 퀴즈 타입: {quiz_request.quiz_type}
3. 각 문제는 10단어 이하의 짧은 문장 사용
4. 사용자가 학습한 단어들을 기반으로 문제 생성
5. 점자 문법 규칙 포함 (받침, 수표 등)

퀴즈 형식:
- multiple_choice: 4개 선택지
- true_false: 참/거짓 문제
- fill_blank: 빈칸 채우기

응답은 반드시 다음 JSON 형식으로 작성:
{{
    "title": "퀴즈 제목",
    "questions": [
        {{
            "question": "문제 내용 (10단어 이하)",
            "options": ["선택지1", "선택지2", "선택지3", "선택지4"] (multiple_choice만),
            "correct_answer": "정답",
            "explanation": "해설",
            "braille_content": "관련 점자 표현"
        }}
    ]
}}

예시 문제:
- "다음 중 받침 'ㄱ'의 점자 표현은?"
- "'안녕하세요'에서 수표가 필요한 부분은?"
- "점자에서 숫자 1의 표현은 무엇인가요?"
"""

    try:
        # Get OpenAI client
        openai_client = get_openai_client()
        if not openai_client:
            raise Exception("OpenAI client not configured")
            
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",  # Use newer, more capable model
            messages=[
                {
                    "role": "system", 
                    "content": "당신은 한국어 점자 교육 전문가입니다. 사용자의 학습 수준에 맞는 개인화된 점자 퀴즈를 생성합니다. 반드시 JSON 형식으로 응답하세요."
                },
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.7,
            response_format={"type": "json_object"}  # Ensure JSON response
        )
        
        # Parse AI response
        ai_content = response.choices[0].message.content
        
        # Parse JSON from the response
        try:
            quiz_data = json.loads(ai_content)
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            print(f"AI response: {ai_content}")
            # Fallback quiz data
            quiz_data = {
                "title": f"{quiz_request.difficulty_level.title()} 점자 학습 퀴즈",
                "questions": [
                    {
                        "question": "점자에서 'ㄱ' 받침의 표현은 무엇인가요?",
                        "options": ["⠁", "⠂", "⠃", "⠄"] if quiz_request.quiz_type == "multiple_choice" else None,
                        "correct_answer": "⠁",
                        "explanation": "점자에서 'ㄱ' 받침은 ⠁로 표현됩니다.",
                        "braille_content": "⠁"
                    }
                ]
            }
        
        # Create quiz questions
        questions = []
        for q_data in quiz_data.get("questions", []):
            question = QuizQuestion(
                question=q_data.get("question", ""),
                options=q_data.get("options") if quiz_request.quiz_type == "multiple_choice" else None,
                correct_answer=q_data.get("correct_answer", ""),
                explanation=q_data.get("explanation", ""),
                braille_content=q_data.get("braille_content")
            )
            questions.append(question)
        
        # Create quiz object
        quiz = Quiz(
            user_email=user_profile.email,
            title=quiz_data.get("title", f"{quiz_request.difficulty_level.title()} 퀴즈"),
            questions=questions,
            difficulty_level=quiz_request.difficulty_level,
            quiz_type=quiz_request.quiz_type,
            created_at=datetime.utcnow(),
            based_on_vocabulary=[item.get('content', '') for item in vocabulary[:10]]
        )
        
        return quiz
        
    except Exception as e:
        print(f"Error generating quiz with AI: {e}")
        # Fallback quiz
        fallback_question = QuizQuestion(
            question="점자 학습에서 가장 중요한 것은 무엇인가요?",
            options=["정확한 손가락 위치", "빠른 속도", "암기", "모든 것"] if quiz_request.quiz_type == "multiple_choice" else None,
            correct_answer="정확한 손가락 위치",
            explanation="점자 학습에서는 정확한 손가락 위치가 가장 중요합니다.",
            braille_content="⠏⠕⠎⠊⠞⠊⠕⠝"
        )
        
        return Quiz(
            user_email=user_profile.email,
            title="기본 점자 퀴즈",
            questions=[fallback_question],
            difficulty_level=quiz_request.difficulty_level,
            quiz_type=quiz_request.quiz_type,
            created_at=datetime.utcnow(),
            based_on_vocabulary=[]
        )

@router.get("/test-openai", tags=["quiz"])
async def test_openai_connection():
    """Test OpenAI connection"""
    try:
        openai_client = get_openai_client()
        if not openai_client:
            return {"status": "error", "message": "OpenAI client not configured. Please set OPENAI_API_KEY."}
        
        # Test with a simple request
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Say 'Hello' in Korean"}],
            max_tokens=10
        )
        
        return {
            "status": "success", 
            "message": "OpenAI connection working",
            "test_response": response.choices[0].message.content
        }
    except Exception as e:
        return {"status": "error", "message": f"OpenAI connection failed: {str(e)}"}

@router.post("/generate", tags=["quiz"], response_model=QuizResponse)
async def generate_quiz(
    quiz_request: QuizRequest,
    current_user: User = Depends(get_current_user)
):
    """Generate a personalized Korean Braille quiz based on user's vocabulary"""
    try:
        # Get user's vocabulary
        vocabulary = await get_user_vocabulary(
            current_user.email, 
            quiz_request.difficulty_level
        )
        
        # Generate quiz using AI
        quiz = await generate_quiz_with_ai(vocabulary, quiz_request, current_user)
        
        # Save quiz to Firestore
        db = firebase_service.db
        quiz_ref = db.collection('quizzes')
        
        quiz_dict = quiz.dict()
        quiz_dict['created_at'] = quiz.created_at
        doc_ref = quiz_ref.add(quiz_dict)
        quiz.id = doc_ref[1].id
        
        return QuizResponse(
            quiz=quiz,
            message=f"{len(quiz.questions)}문제의 개인화된 퀴즈가 생성되었습니다."
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"퀴즈 생성 중 오류가 발생했습니다: {str(e)}")

@router.post("/submit", tags=["quiz"], response_model=QuizResult)
async def submit_quiz(
    submission: QuizSubmission,
    current_user: User = Depends(get_current_user)
):
    """Submit quiz answers and get results"""
    try:
        db = firebase_service.db
        quiz_ref = db.collection('quizzes').document(submission.quiz_id)
        quiz_doc = quiz_ref.get()
        
        if not quiz_doc.exists:
            raise HTTPException(status_code=404, detail="퀴즈를 찾을 수 없습니다.")
        
        quiz_data = quiz_doc.to_dict()
        
        # Check if quiz belongs to user
        if quiz_data.get('user_email') != current_user.email:
            raise HTTPException(status_code=403, detail="이 퀴즈에 접근할 권한이 없습니다.")
        
        # Calculate score
        questions = quiz_data.get('questions', [])
        correct_count = 0
        feedback = []
        
        for i, answer in enumerate(submission.answers):
            if i < len(questions):
                question = questions[i]
                is_correct = answer.user_answer.strip() == question.get('correct_answer', '').strip()
                
                if is_correct:
                    correct_count += 1
                
                feedback.append({
                    "question_index": i,
                    "question": question.get('question', ''),
                    "user_answer": answer.user_answer,
                    "correct_answer": question.get('correct_answer', ''),
                    "is_correct": is_correct,
                    "explanation": question.get('explanation', '')
                })
        
        total_questions = len(questions)
        percentage = (correct_count / total_questions) * 100 if total_questions > 0 else 0
        
        # Save result to Firestore
        result_data = {
            "quiz_id": submission.quiz_id,
            "user_email": current_user.email,
            "score": correct_count,
            "total_questions": total_questions,
            "percentage": percentage,
            "feedback": feedback,
            "completed_at": datetime.utcnow()
        }
        
        results_ref = db.collection('quiz_results')
        results_ref.add(result_data)
        
        return QuizResult(**result_data)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"퀴즈 제출 중 오류가 발생했습니다: {str(e)}")

@router.get("/history", tags=["quiz"], response_model=List[Quiz])
async def get_quiz_history(
    current_user: User = Depends(get_current_user),
    limit: Optional[int] = 10
):
    """Get user's quiz history"""
    try:
        db = firebase_service.db
        quiz_ref = db.collection('quizzes')
        
        query = quiz_ref.where('user_email', '==', current_user.email)\
                        .order_by('created_at', direction='DESCENDING')
        
        if limit:
            query = query.limit(limit)
        
        docs = query.get()
        quizzes = []
        
        for doc in docs:
            quiz_data = doc.to_dict()
            quiz_data['id'] = doc.id
            
            # Convert questions to QuizQuestion objects
            questions = []
            for q_data in quiz_data.get('questions', []):
                questions.append(QuizQuestion(**q_data))
            
            quiz_data['questions'] = questions
            quizzes.append(Quiz(**quiz_data))
        
        return quizzes
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"퀴즈 이력 조회 중 오류가 발생했습니다: {str(e)}")

@router.get("/results", tags=["quiz"], response_model=List[QuizResult])
async def get_quiz_results(
    current_user: User = Depends(get_current_user),
    limit: Optional[int] = 10
):
    """Get user's quiz results"""
    try:
        db = firebase_service.db
        results_ref = db.collection('quiz_results')
        
        query = results_ref.where('user_email', '==', current_user.email)\
                          .order_by('completed_at', direction='DESCENDING')
        
        if limit:
            query = query.limit(limit)
        
        docs = query.get()
        results = []
        
        for doc in docs:
            result_data = doc.to_dict()
            results.append(QuizResult(**result_data))
        
        return results
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"퀴즈 결과 조회 중 오류가 발생했습니다: {str(e)}")

@router.get("/{quiz_id}", tags=["quiz"], response_model=Quiz)
async def get_quiz(
    quiz_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get a specific quiz by ID"""
    try:
        db = firebase_service.db
        quiz_ref = db.collection('quizzes').document(quiz_id)
        quiz_doc = quiz_ref.get()
        
        if not quiz_doc.exists:
            raise HTTPException(status_code=404, detail="퀴즈를 찾을 수 없습니다.")
        
        quiz_data = quiz_doc.to_dict()
        
        # Check if quiz belongs to user
        if quiz_data.get('user_email') != current_user.email:
            raise HTTPException(status_code=403, detail="이 퀴즈에 접근할 권한이 없습니다.")
        
        quiz_data['id'] = quiz_id
        
        # Convert questions to QuizQuestion objects
        questions = []
        for q_data in quiz_data.get('questions', []):
            questions.append(QuizQuestion(**q_data))
        
        quiz_data['questions'] = questions
        
        return Quiz(**quiz_data)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"퀴즈 조회 중 오류가 발생했습니다: {str(e)}")