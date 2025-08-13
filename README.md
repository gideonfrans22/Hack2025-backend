# 🔤 ReadAble - AI-Powered Braille Learning Platform

> 생성형 AI를 활용한 점자 학습 플랫폼

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.112+-green.svg)](https://fastapi.tiangolo.com)
[![Firebase](https://img.shields.io/badge/Firebase-Integrated-orange.svg)](https://firebase.google.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📖 프로젝트 소개

**ReadAble**은 생성형 AI 기술을 활용하여 개인화된 점자 학습 경험을 제공하는 혁신적인 교육 플랫폼입니다. 사용자의 학습 수준과 관심사를 분석하여 맞춤형 학습 콘텐츠를 생성하고, 체계적인 커리큘럼을 통해 효과적인 점자 학습을 지원합니다.

### ✨ 주요 특징

- 🤖 **AI 기반 개인화**: 사용자의 수준과 관심사에 맞춘 맞춤형 학습 콘텐츠 생성
- 📊 **적응형 난이도 시스템**: 단어 → 짧은 문장 → 긴 문장 → 짧은 문단 → 긴 문단
- 📚 **체계적 커리큘럼**: 국립국어원 점자 문법 규칙 기반의 단계별 학습
- 🎯 **무한 연습 문제**: AI를 통한 무제한 퀴즈 및 연습 문제 생성
- 🔊 **접근성 지원**: 음성 인터페이스 및 입력 보조 장치 지원
- 📈 **학습 진도 관리**: 개인별 학습 성과 추적 및 분석

## 🏗️ 시스템 아키텍처

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API   │    │   Firebase      │
│   (Flutter/Web) │◄──►│   (FastAPI)     │◄──►│   (Database)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                               │
                       ┌─────────────────┐
                       │   AI Service    │
                       │   (OpenAI/etc)  │
                       └─────────────────┘
```

## 🔧 기술 스택

### Backend
- **Framework**: FastAPI 0.112+
- **Runtime**: Python 3.8+
- **Database**: Firebase Firestore
- **Authentication**: Firebase Auth
- **AI Integration**: OpenAI API (계획)

### Infrastructure
- **Deployment**: Docker (예정)
- **Cloud**: Firebase Hosting
- **CI/CD**: GitHub Actions (예정)

## 🚀 빠른 시작

### 사전 요구사항

- Python 3.8 이상
- Firebase 프로젝트
- Git

### 1. 저장소 클론

```bash
git clone https://github.com/your-username/readable-backend.git
cd readable-backend
```

### 2. 가상환경 설정

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

### 3. 의존성 설치

```bash
pip install -r requirements.txt
```

### 4. Firebase 설정

Firebase 설정을 위해 [FIREBASE_SETUP.md](FIREBASE_SETUP.md)를 참고하세요.

### 5. 환경변수 설정

```bash
cp .env.example .env
# .env 파일을 편집하여 Firebase 설정 추가
```

### 6. 서버 실행

```bash
uvicorn main:app --reload
```

서버가 실행되면 다음 주소에서 확인할 수 있습니다:
- API 문서: http://localhost:8000/docs
- Firebase 상태: http://localhost:8000/firebase-status

## 📋 핵심 기능

### 1. 사용자 사전 정보 파악

```python
# 사용자 평가 및 프로필 설정
{
    "difficulty_level": "beginner",  # 단어/짧은문장/긴문장/짧은문단/긴문단
    "age": 30,
    "gender": "male",
    "interests": ["축구", "음악", "독서"],
    "learning_goals": ["일상 대화", "문서 읽기"]
}
```

**예시 개인화 문장 생성**:
- 입력: "30대, 남성, 축구 관심"
- 출력: "아시아 축구 선수 중 1위는 손흥민이라고 생각해"
- 학습 포인트: "받침 ᄀ과 1은 '수표'를 통해 구분한다"

### 2. 점자 문법 커리큘럼

- **기반**: 국립국어원 점자 문법 규칙 해설
- **확장**: 기존 2-3개 예문을 AI로 10개까지 확장
- **개인화**: 사용자 정보 + 문법 규칙 → 맞춤형 문제 생성

### 3. 점자 학습 퀴즈

- **문제 유형**: O/X, 단답형, 객관식
- **입력 방식**: 음성 인식, 키보드, 점자 입력 장치
- **적응형 학습**: 정답률에 따른 자동 난이도 조절
- **무한 연습**: AI 기반 무제한 문제 생성

## 🛠️ API 엔드포인트

### 사용자 관리
```http
GET    /api/v1/users/           # 사용자 목록 조회
POST   /api/v1/users/           # 새 사용자 생성
GET    /api/v1/users/{user_id}  # 특정 사용자 조회
PUT    /api/v1/users/{user_id}  # 사용자 정보 수정
```

### 학습 커리큘럼 (예정)
```http
GET    /api/v1/curriculum/              # 커리큘럼 목록
GET    /api/v1/curriculum/{unit_id}     # 특정 단원 정보
POST   /api/v1/quiz/generate            # AI 퀴즈 생성
POST   /api/v1/quiz/submit              # 퀴즈 답안 제출
```

### 학습 진도 (예정)
```http
GET    /api/v1/progress/{user_id}       # 학습 진도 조회
POST   /api/v1/progress/update          # 진도 업데이트
```

## 📊 데이터베이스 스키마

### Users Collection
```javascript
{
  "user_id": "string",
  "profile": {
    "name": "string",
    "age": "number",
    "gender": "string",
    "interests": ["string"],
    "difficulty_level": "string"
  },
  "learning_progress": {
    "current_unit": "string",
    "completed_units": ["string"],
    "quiz_scores": {}
  },
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

### Curriculum Collection
```javascript
{
  "unit_id": "string",
  "title": "string",
  "difficulty": "string",
  "grammar_rules": ["string"],
  "examples": ["string"],
  "order": "number"
}
```

## 🧪 테스트

```bash
# 단위 테스트 실행
pytest tests/

# 커버리지 포함 테스트
pytest --cov=. tests/

# API 테스트
pytest tests/test_api.py -v
```

## 📦 배포

### Docker를 사용한 배포

```bash
# Docker 이미지 빌드
docker build -t readable-backend .

# 컨테이너 실행
docker run -p 8000:8000 \
  -e GOOGLE_APPLICATION_CREDENTIALS=/app/firebase-key.json \
  readable-backend
```

### Firebase Hosting (프론트엔드)

```bash
# Firebase CLI 설치
npm install -g firebase-tools

# 프로젝트 배포
firebase deploy
```

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참고하세요.

## 👥 팀

- **Frontend**: Flutter/Web 개발팀
- **Backend**: FastAPI/Python 개발팀  
- **AI/ML**: 생성형 AI 모델 개발팀
- **UX/UI**: 접근성 중심 디자인팀

---

<div align="center">
  <strong>💙 ReadAble로 더 나은 점자 학습 경험을 만들어가요! 💙</strong>
</div>
