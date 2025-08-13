# AI-Powered Korean Braille Quiz System

## Overview
The quiz system generates personalized Korean Braille quizzes using OpenAI's GPT API, based on each user's learned vocabulary and preferences. All quizzes are limited to 10 words or less per question for optimal learning.

## Features

### ✨ AI-Generated Content
- **Personalized Questions**: Based on user's vocabulary library
- **Korean Language**: All questions generated in Korean
- **Short Sentences**: Maximum 10 words per question
- **Braille Integration**: Includes Braille representations and grammar rules

### 🎯 Adaptive Difficulty
- **Beginner**: Basic characters and simple words
- **Intermediate**: Complex words and grammar rules
- **Advanced**: Advanced Braille concepts and long sentences

### 📝 Quiz Types
- **Multiple Choice**: 4-option questions about Braille rules
- **True/False**: Simple true/false questions
- **Fill in the Blank**: Complete the missing Braille characters

## Authentication
All endpoints require JWT authentication:
```
Authorization: Bearer <your-jwt-token>
```

## API Endpoints

### 1. Generate Quiz
**POST** `/api/v1/quiz/generate`

Generate a personalized quiz based on user's vocabulary.

**Request Body:**
```json
{
  "difficulty_level": "beginner",
  "quiz_type": "multiple_choice",
  "num_questions": 5,
  "focus_words": ["안녕", "사랑"] // optional
}
```

**Response:**
```json
{
  "quiz": {
    "id": "quiz_123",
    "user_email": "user@example.com",
    "title": "개인화된 점자 학습 퀴즈",
    "questions": [
      {
        "question": "다음 중 '안녕'의 점자 표현은?",
        "options": ["⠈⠟⠈⠕", "⠈⠟⠈⠏", "⠈⠟⠈⠑", "⠈⠟⠈⠥"],
        "correct_answer": "⠈⠟⠈⠕",
        "explanation": "'안녕'은 점자로 ⠈⠟⠈⠕로 표현됩니다.",
        "braille_content": "⠈⠟⠈⠕"
      }
    ],
    "difficulty_level": "beginner",
    "quiz_type": "multiple_choice",
    "created_at": "2025-08-13T10:30:00Z",
    "based_on_vocabulary": ["안녕", "사랑", "친구"]
  },
  "message": "5문제의 개인화된 퀴즈가 생성되었습니다."
}
```

### 2. Submit Quiz
**POST** `/api/v1/quiz/submit`

Submit quiz answers and get results.

**Request Body:**
```json
{
  "quiz_id": "quiz_123",
  "answers": [
    {
      "question_index": 0,
      "user_answer": "⠈⠟⠈⠕"
    }
  ]
}
```

**Response:**
```json
{
  "quiz_id": "quiz_123",
  "score": 4,
  "total_questions": 5,
  "percentage": 80.0,
  "feedback": [
    {
      "question_index": 0,
      "question": "다음 중 '안녕'의 점자 표현은?",
      "user_answer": "⠈⠟⠈⠕",
      "correct_answer": "⠈⠟⠈⠕",
      "is_correct": true,
      "explanation": "'안녕'은 점자로 ⠈⠟⠈⠕로 표현됩니다."
    }
  ],
  "completed_at": "2025-08-13T10:35:00Z"
}
```

### 3. Quiz History
**GET** `/api/v1/quiz/history?limit=10`

Get user's quiz history.

### 4. Quiz Results
**GET** `/api/v1/quiz/results?limit=10`

Get user's quiz results and performance.

### 5. Get Specific Quiz
**GET** `/api/v1/quiz/{quiz_id}`

Retrieve a specific quiz by ID.

## AI Prompt System

The system uses sophisticated prompts to generate contextual quizzes:

### User Context Integration
```
사용자 정보:
- 이름: {user.name}
- 나이: {user.age}
- 관심사: {user.hobby}
- 학습한 단어들: {vocabulary}
```

### Quiz Generation Rules
1. **10단어 이하**: Each question limited to 10 Korean words
2. **Vocabulary-based**: Uses user's learned words as foundation
3. **Grammar Focus**: Includes Braille grammar rules (받침, 수표 등)
4. **Personalization**: Adapts to user's interests and age

### Example AI Prompts
- "다음 중 받침 'ㄱ'의 점자 표현은?"
- "'안녕하세요'에서 수표가 필요한 부분은?"
- "점자에서 숫자 1의 표현은 무엇인가요?"

## Setup Instructions

### 1. OpenAI API Configuration
1. Get an OpenAI API key from https://platform.openai.com/
2. Add to your `.env` file:
   ```
   OPENAI_API_KEY=your-openai-api-key-here
   ```

### 2. Environment Variables
Update `.env.example` and `.env`:
```bash
# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key-here
```

### 3. Dependencies
The system requires:
- `openai==1.35.0` - OpenAI API client
- `python-dotenv` - Environment configuration
- User vocabulary system integration

## Fallback System

When OpenAI is unavailable:
- **Graceful Degradation**: System continues to work with pre-defined questions
- **Error Handling**: Clear error messages for users
- **Basic Quizzes**: Fallback to fundamental Braille questions

## Integration with ReadAble Platform

### Vocabulary Integration
- **Automatic**: Pulls from user's vocabulary library
- **Contextual**: Uses learned words to generate relevant questions
- **Progressive**: Difficulty adapts to learning progress

### Learning Analytics
- **Performance Tracking**: Stores quiz results for progress analysis
- **Adaptive Learning**: Future quizzes adapt to past performance
- **Statistics**: Comprehensive learning analytics

## Example Usage Flow

1. **User learns vocabulary** (using vocabulary API)
2. **Request personalized quiz**:
   ```bash
   curl -X POST "http://localhost:8000/api/v1/quiz/generate" \
     -H "Authorization: Bearer <token>" \
     -H "Content-Type: application/json" \
     -d '{
       "difficulty_level": "beginner",
       "quiz_type": "multiple_choice",
       "num_questions": 5
     }'
   ```

3. **Take quiz** and submit answers
4. **Receive immediate feedback** with explanations
5. **Track progress** through quiz history

## Benefits

✅ **Personalized Learning**: AI generates content based on individual progress
✅ **Korean Native**: All content in Korean for local users
✅ **Bite-sized**: 10-word limit ensures manageable learning chunks  
✅ **Grammar-focused**: Emphasizes important Braille grammar rules
✅ **Adaptive**: Difficulty adjusts to user capability
✅ **Comprehensive**: Tracks detailed learning analytics
✅ **Accessible**: Designed for visually impaired users

This AI-powered quiz system transforms Braille learning into an engaging, personalized experience! 🎉
