# 📁 ReadAble Platform - Project Structure Documentation

## 🎯 Overview

The ReadAble platform has been restructured following **MVC (Model-View-Controller)** architecture principles for better code organization, maintainability, and scalability.

## 📂 New Project Structure

```
hack2025-backend/
├── main.py                          # FastAPI application entry point
├── firebase_config.py               # Firebase Admin SDK configuration
├── requirements.txt                 # Python dependencies
├── .env                            # Environment variables
├── .env.example                    # Environment variables template
│
├── models/                         # 📦 DATA MODELS (Pydantic schemas)
│   ├── __init__.py                 # Models package exports
│   ├── user_models.py              # User data models
│   ├── vocab_models.py             # Vocabulary data models
│   └── quiz_models.py              # Quiz data models
│
├── controllers/                    # 🎮 BUSINESS LOGIC
│   ├── __init__.py                 # Controllers package exports
│   ├── user_controller.py          # User authentication & management logic
│   ├── vocab_controller.py         # Vocabulary management logic
│   └── quiz_controller.py          # Quiz generation & management logic
│
├── routers/                        # 🛣️ API ROUTES
│   ├── __init__.py                 # Routers package initialization
│   ├── users_new.py                # User API endpoints
│   ├── vocab_library_new.py        # Vocabulary API endpoints
│   ├── quiz_new.py                 # Quiz API endpoints
│   │
│   ├── users.py                    # [OLD] Legacy user routes
│   ├── vocab_library.py            # [OLD] Legacy vocabulary routes
│   └── quiz.py                     # [OLD] Legacy quiz routes
│
└── [Documentation & Deployment Files]
    ├── README.md
    ├── DEPLOYMENT_GUIDE.md
    ├── DOCKER_GUIDE.md
    └── ...
```

## 🏗️ Architecture Explanation

### **1. Models Layer** (`models/`)

**Purpose**: Define data structures and schemas  
**Technology**: Pydantic BaseModel  
**Responsibility**: Data validation and serialization

#### Files:

- **`user_models.py`**: User-related data models

  - `User`: Base user model
  - `UserInDB`: User with hashed password
  - `UserSignup`: Signup request model
  - `UserLogin`: Login request model
  - `Token`: JWT token response model

- **`vocab_models.py`**: Vocabulary-related data models

  - `VocabularyItem`: Base vocabulary model
  - `VocabularyCreate`: Creation request model
  - `VocabularyResponse`: API response model
  - `VocabularyStats`: Statistics model
  - `DifficultyLevel`: Enum for difficulty levels
  - `VocabType`: Enum for vocabulary types

- **`quiz_models.py`**: Quiz-related data models
  - `Quiz`: Complete quiz model
  - `QuizQuestion`: Individual question model
  - `QuizRequest`: Quiz generation request
  - `QuizResponse`: Quiz generation response
  - `QuizSubmission`: User answers submission
  - `QuizResult`: Quiz results with scores

**Example Usage**:

```python
from models import User, VocabularyCreate, QuizRequest
```

---

### **2. Controllers Layer** (`controllers/`)

**Purpose**: Business logic and data processing  
**Technology**: Python classes with static methods  
**Responsibility**: Database operations, authentication, AI integration

#### Files:

- **`user_controller.py`**: User management business logic

  - `UserController.signup()`: Create new user account
  - `UserController.login()`: Authenticate user
  - `UserController.create_access_token()`: Generate JWT tokens
  - `UserController.verify_token()`: Validate JWT tokens
  - `UserController.get_user_by_email()`: Fetch user from database
  - `UserController.get_all_users()`: Fetch all users

- **`vocab_controller.py`**: Vocabulary management business logic

  - `VocabController.create_vocabulary_item()`: Add new vocabulary
  - `VocabController.get_vocabulary_items()`: Fetch with filters
  - `VocabController.get_vocabulary_stats()`: Calculate statistics
  - `VocabController.delete_vocabulary_item()`: Remove vocabulary
  - `VocabController.search_vocabulary()`: Search functionality

- **`quiz_controller.py`**: Quiz management business logic
  - `QuizController.generate_quiz()`: Create AI-powered quizzes
  - `QuizController.generate_quiz_with_ai()`: OpenAI integration
  - `QuizController.submit_quiz()`: Process quiz submissions
  - `QuizController.get_quiz_history()`: Fetch quiz history
  - `QuizController.get_quiz_results()`: Fetch quiz results
  - `QuizController.get_quiz_by_id()`: Fetch specific quiz

**Example Usage**:

```python
from controllers import UserController

# In router
user = UserController.signup(user_data)
token = UserController.login(credentials)
```

---

### **3. Routers Layer** (`routers/`)

**Purpose**: API endpoint definitions  
**Technology**: FastAPI APIRouter  
**Responsibility**: HTTP request/response handling, routing

#### New Files:

- **`users_new.py`**: User authentication API endpoints

  - `POST /api/v1/signup`: User registration
  - `POST /api/v1/login`: User authentication
  - `GET /api/v1/me`: Get current user profile
  - `GET /api/v1/users/`: List all users
  - `GET /api/v1/users/{email}`: Get specific user

- **`vocab_library_new.py`**: Vocabulary management API endpoints

  - `POST /api/v1/vocabulary`: Add vocabulary item
  - `GET /api/v1/vocabulary`: List vocabulary items
  - `GET /api/v1/vocabulary/characters`: Get characters only
  - `GET /api/v1/vocabulary/words`: Get words only
  - `GET /api/v1/vocabulary/stats`: Get learning statistics
  - `DELETE /api/v1/vocabulary/{vocab_id}`: Delete item
  - `GET /api/v1/vocabulary/search`: Search vocabulary

- **`quiz_new.py`**: Quiz management API endpoints
  - `POST /api/v1/quiz/generate`: Generate AI-powered quiz
  - `POST /api/v1/quiz/submit`: Submit quiz answers
  - `GET /api/v1/quiz/history`: Get quiz history
  - `GET /api/v1/quiz/results`: Get quiz results
  - `GET /api/v1/quiz/{quiz_id}`: Get specific quiz
  - `GET /api/v1/quiz/test-openai`: Test OpenAI connection

**Example Router**:

```python
from fastapi import APIRouter, Depends
from models import User, UserSignup
from controllers import UserController

router = APIRouter()

@router.post("/signup")
async def signup(user: UserSignup):
    return UserController.signup(user)
```

---

## 🔄 Request Flow

```
Client Request
    ↓
FastAPI (main.py)
    ↓
Router (routers/*.py)
    ↓
Controller (controllers/*.py)
    ↓
Model (models/*.py) + Firebase
    ↓
Response back to Client
```

### Example Flow: User Login

1. **Client** sends POST request to `/api/v1/login`
2. **Router** (`users_new.py`) receives request, validates `UserLogin` model
3. **Router** calls `UserController.login(user)`
4. **Controller** (`user_controller.py`) validates credentials against Firebase
5. **Controller** generates JWT token using `create_access_token()`
6. **Controller** returns `Token` model with user info
7. **Router** sends response back to client

---

## ✨ Benefits of New Structure

### **1. Separation of Concerns**

- **Models**: Only data structure definitions
- **Controllers**: Only business logic
- **Routers**: Only HTTP handling

### **2. Maintainability**

- Easy to locate and modify specific functionality
- Changes in business logic don't affect routes
- Clear responsibility for each layer

### **3. Testability**

- Controllers can be unit tested independently
- Models can be validated separately
- Routes can be integration tested

### **4. Scalability**

- Easy to add new features
- Can replace database without changing routes
- Can add new endpoints without touching business logic

### **5. Code Reusability**

- Controllers can be used by multiple routes
- Models can be shared across features
- Common logic stays in one place

### **6. Team Collaboration**

- Multiple developers can work on different layers
- Clear boundaries reduce merge conflicts
- Easy to onboard new team members

---

## 🚀 Migration Guide

### **Old Structure (Legacy)**

```python
# routers/users.py - Everything in one file
- Models defined in router file
- Business logic in router functions
- Database calls in router functions
- ~200 lines of mixed responsibilities
```

### **New Structure**

```python
# models/user_models.py
- Clean model definitions

# controllers/user_controller.py
- Pure business logic methods

# routers/users_new.py
- Clean, simple route definitions
```

### **How to Use**

#### Old Way:

```python
from routers import users
app.include_router(users.router)
```

#### New Way:

```python
from routers import users_new
app.include_router(users_new.router)
```

---

## 📝 Usage Examples

### **Import Models**

```python
from models import User, VocabularyCreate, QuizRequest
from models.user_models import Token
from models.vocab_models import DifficultyLevel
```

### **Import Controllers**

```python
from controllers import UserController, VocabController, QuizController
```

### **Create New Endpoint**

```python
# In routers/users_new.py
from models import User
from controllers import UserController

@router.get("/profile")
async def get_profile(current_user: User = Depends(get_current_user)):
    # Business logic handled by controller
    return UserController.get_user_profile(current_user)
```

### **Add New Business Logic**

```python
# In controllers/user_controller.py
class UserController:
    @staticmethod
    def get_user_profile(user: User) -> dict:
        # Business logic here
        return {"profile": user.dict()}
```

---

## 🔧 Configuration

### **Environment Variables** (`.env`)

```bash
# Firebase
GOOGLE_APPLICATION_CREDENTIALS=./firebase-service-account.json
FIREBASE_PROJECT_ID=your-project-id

# JWT
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_HOURS=24

# OpenAI
OPENAI_API_KEY=your-openai-api-key

# Application
DEBUG=False
ENVIRONMENT=production
```

---

## 📊 Current Status

### ✅ **Completed**

- ✅ Created `models/` folder with all data models
- ✅ Created `controllers/` folder with all business logic
- ✅ Created new routers with clean separation
- ✅ Updated `main.py` to use new structure
- ✅ Maintained backward compatibility (old files preserved)

### 🔄 **Next Steps** (Optional)

1. Test all endpoints with new structure
2. Remove old router files after verification
3. Add unit tests for controllers
4. Add integration tests for routers
5. Update deployment scripts if needed

---

## 🎓 Best Practices

### **When Adding New Features**

1. **Define Model First**

   ```python
   # models/new_feature_models.py
   class NewFeature(BaseModel):
       field1: str
       field2: int
   ```

2. **Implement Controller Logic**

   ```python
   # controllers/new_feature_controller.py
   class NewFeatureController:
       @staticmethod
       def create_feature(data):
           # Business logic
           pass
   ```

3. **Create Router Endpoint**

   ```python
   # routers/new_feature.py
   @router.post("/feature")
   async def create_feature(data: NewFeature):
       return NewFeatureController.create_feature(data)
   ```

4. **Register Router in main.py**
   ```python
   from routers import new_feature
   app.include_router(new_feature.router, prefix="/api/v1")
   ```

---

## 📚 Additional Resources

- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **Pydantic Models**: https://docs.pydantic.dev/
- **Firebase Admin SDK**: https://firebase.google.com/docs/admin/setup
- **OpenAI API**: https://platform.openai.com/docs/

---

## 🎉 Conclusion

The new structure provides a **clean**, **maintainable**, and **scalable** architecture for the ReadAble platform. Each layer has a clear responsibility, making the codebase easier to understand, test, and extend.

**Happy Coding! 🚀**
