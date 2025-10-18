"""
Quiz Controller - Business logic for quiz generation and management
"""
import os
import json
from typing import List, Optional, Dict, Any
from datetime import datetime
from fastapi import HTTPException
from dotenv import load_dotenv

from firebase_config import firebase_service
from models.quiz_models import (
    Quiz,
    QuizQuestion,
    QuizRequest,
    QuizResponse,
    QuizSubmission,
    QuizResult
)
from models.user_models import User

# Load environment variables
load_dotenv()

# OpenAI Configuration
from openai import OpenAI


class QuizController:
    """Controller for handling quiz-related business logic"""
    
    @staticmethod
    def get_openai_client():
        """
        Get OpenAI client with proper error handling
        
        Returns:
            OpenAI client instance or None if not configured
        """
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            return None
        
        try:
            client = OpenAI(api_key=openai_api_key)
            return client
        except Exception as e:
            print(f"Warning: Failed to initialize OpenAI client: {e}")
            return None
    
    @staticmethod
    async def get_user_vocabulary(
        user_email: str, 
        difficulty_level: str = None
    ) -> List[Dict]:
        """
        Get user's learned vocabulary from Firestore
        
        Args:
            user_email: User email
            difficulty_level: Optional filter by difficulty
            
        Returns:
            List of vocabulary items
        """
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
    
    @staticmethod
    async def generate_quiz_with_ai(
        vocabulary: List[Dict], 
        quiz_request: QuizRequest, 
        user_profile: User
    ) -> Quiz:
        """
        Generate quiz using OpenAI based on user's vocabulary
        
        Args:
            vocabulary: User's vocabulary items
            quiz_request: Quiz generation parameters
            user_profile: User information
            
        Returns:
            Generated quiz
        """
        if not vocabulary:
            vocabulary_text = "기본 한국어 단어: 안녕, 사랑, 친구, 가족, 학교"
        else:
            vocab_words = [item.get('content', '') for item in vocabulary[:20]]
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
"""
        
        try:
            openai_client = QuizController.get_openai_client()
            if not openai_client:
                raise Exception("OpenAI client not configured")
                
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system", 
                        "content": "당신은 한국어 점자 교육 전문가입니다. 사용자의 학습 수준에 맞는 개인화된 점자 퀴즈를 생성합니다. 반드시 JSON 형식으로 응답하세요."
                    },
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            ai_content = response.choices[0].message.content
            
            try:
                quiz_data = json.loads(ai_content)
            except json.JSONDecodeError as e:
                print(f"JSON parsing error: {e}")
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
    
    @staticmethod
    def test_openai_connection() -> Dict[str, Any]:
        """
        Test OpenAI connection
        
        Returns:
            Connection test result
        """
        try:
            openai_client = QuizController.get_openai_client()
            if not openai_client:
                return {
                    "status": "error", 
                    "message": "OpenAI client not configured. Please set OPENAI_API_KEY."
                }
            
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
            return {
                "status": "error", 
                "message": f"OpenAI connection failed: {str(e)}"
            }
    
    @staticmethod
    async def generate_quiz(
        quiz_request: QuizRequest, 
        user: User
    ) -> QuizResponse:
        """
        Generate a personalized Korean Braille quiz
        
        Args:
            quiz_request: Quiz generation parameters
            user: Current user
            
        Returns:
            Generated quiz response
            
        Raises:
            HTTPException: If quiz generation fails
        """
        try:
            # Get user's vocabulary
            vocabulary = await QuizController.get_user_vocabulary(
                user.email, 
                quiz_request.difficulty_level
            )
            
            # Generate quiz using AI
            quiz = await QuizController.generate_quiz_with_ai(
                vocabulary, 
                quiz_request, 
                user
            )
            
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
            raise HTTPException(
                status_code=500, 
                detail=f"퀴즈 생성 중 오류가 발생했습니다: {str(e)}"
            )
    
    @staticmethod
    def submit_quiz(submission: QuizSubmission, user: User) -> QuizResult:
        """
        Submit quiz answers and calculate results
        
        Args:
            submission: Quiz submission with answers
            user: Current user
            
        Returns:
            Quiz result with score and feedback
            
        Raises:
            HTTPException: If submission fails
        """
        try:
            db = firebase_service.db
            quiz_ref = db.collection('quizzes').document(submission.quiz_id)
            quiz_doc = quiz_ref.get()
            
            if not quiz_doc.exists:
                raise HTTPException(status_code=404, detail="퀴즈를 찾을 수 없습니다.")
            
            quiz_data = quiz_doc.to_dict()
            
            # Check if quiz belongs to user
            if quiz_data.get('user_email') != user.email:
                raise HTTPException(
                    status_code=403, 
                    detail="이 퀴즈에 접근할 권한이 없습니다."
                )
            
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
                "user_email": user.email,
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
            raise HTTPException(
                status_code=500, 
                detail=f"퀴즈 제출 중 오류가 발생했습니다: {str(e)}"
            )
    
    @staticmethod
    def get_quiz_history(user: User, limit: Optional[int] = 10) -> List[Quiz]:
        """
        Get user's quiz history
        
        Args:
            user: Current user
            limit: Maximum number of quizzes to return
            
        Returns:
            List of quizzes
            
        Raises:
            HTTPException: If fetching fails
        """
        try:
            db = firebase_service.db
            quiz_ref = db.collection('quizzes')
            
            query = quiz_ref.where('user_email', '==', user.email)\
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
            raise HTTPException(
                status_code=500, 
                detail=f"퀴즈 이력 조회 중 오류가 발생했습니다: {str(e)}"
            )
    
    @staticmethod
    def get_quiz_results(user: User, limit: Optional[int] = 10) -> List[QuizResult]:
        """
        Get user's quiz results
        
        Args:
            user: Current user
            limit: Maximum number of results to return
            
        Returns:
            List of quiz results
            
        Raises:
            HTTPException: If fetching fails
        """
        try:
            db = firebase_service.db
            results_ref = db.collection('quiz_results')
            
            query = results_ref.where('user_email', '==', user.email)\
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
            raise HTTPException(
                status_code=500, 
                detail=f"퀴즈 결과 조회 중 오류가 발생했습니다: {str(e)}"
            )
    
    @staticmethod
    def get_quiz_by_id(quiz_id: str, user: User) -> Quiz:
        """
        Get a specific quiz by ID
        
        Args:
            quiz_id: Quiz ID
            user: Current user
            
        Returns:
            Quiz object
            
        Raises:
            HTTPException: If quiz not found or user not authorized
        """
        try:
            db = firebase_service.db
            quiz_ref = db.collection('quizzes').document(quiz_id)
            quiz_doc = quiz_ref.get()
            
            if not quiz_doc.exists:
                raise HTTPException(status_code=404, detail="퀴즈를 찾을 수 없습니다.")
            
            quiz_data = quiz_doc.to_dict()
            
            # Check if quiz belongs to user
            if quiz_data.get('user_email') != user.email:
                raise HTTPException(
                    status_code=403, 
                    detail="이 퀴즈에 접근할 권한이 없습니다."
                )
            
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
            raise HTTPException(
                status_code=500, 
                detail=f"퀴즈 조회 중 오류가 발생했습니다: {str(e)}"
            )
