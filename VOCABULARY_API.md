# Vocabulary Library API Documentation

## Overview
The vocabulary library system allows users to track their learned Braille characters and words with timestamps and difficulty levels. All endpoints are protected and require JWT authentication.

## Authentication
All endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <your-jwt-token>
```

## Endpoints

### 1. Register New Learned Vocabulary
**POST** `/api/v1/vocabulary`

Register a new learned character or word for the current user.

**Request Body:**
```json
{
  "content": "안녕",
  "vocab_type": "word",
  "difficulty_level": "beginner",
  "braille_representation": "⠈⠟⠈⠕"
}
```

**Response:**
```json
{
  "id": "abc123",
  "user_email": "user@example.com",
  "content": "안녕",
  "vocab_type": "word",
  "difficulty_level": "beginner",
  "braille_representation": "⠈⠟⠈⠕",
  "learned_at": "2025-08-13T10:30:00Z"
}
```

### 2. Get All Learned Vocabulary
**GET** `/api/v1/vocabulary`

Get list of learned characters and words with optional filters.

**Query Parameters:**
- `vocab_type` (optional): "character" or "word"
- `difficulty_level` (optional): "beginner", "intermediate", or "advanced"
- `limit` (optional): Maximum number of items to return

**Examples:**
```
GET /api/v1/vocabulary                          # All vocabulary
GET /api/v1/vocabulary?vocab_type=character     # Only characters
GET /api/v1/vocabulary?difficulty_level=beginner # Only beginner level
GET /api/v1/vocabulary?limit=10                 # First 10 items
```

### 3. Get Learned Characters Only
**GET** `/api/v1/vocabulary/characters`

Get list of learned characters with optional difficulty filter.

**Query Parameters:**
- `difficulty_level` (optional): "beginner", "intermediate", or "advanced"

### 4. Get Learned Words Only
**GET** `/api/v1/vocabulary/words`

Get list of learned words with optional difficulty filter.

**Query Parameters:**
- `difficulty_level` (optional): "beginner", "intermediate", or "advanced"

### 5. Get Vocabulary Statistics
**GET** `/api/v1/vocabulary/stats`

Get comprehensive statistics about learned vocabulary.

**Response:**
```json
{
  "total_characters": 25,
  "total_words": 18,
  "characters_by_difficulty": {
    "beginner": 15,
    "intermediate": 8,
    "advanced": 2
  },
  "words_by_difficulty": {
    "beginner": 10,
    "intermediate": 6,
    "advanced": 2
  },
  "total_items": 43
}
```

### 6. Search Vocabulary
**GET** `/api/v1/vocabulary/search`

Search vocabulary items by content.

**Query Parameters:**
- `query` (required): Search term
- `vocab_type` (optional): "character" or "word"

**Example:**
```
GET /api/v1/vocabulary/search?query=안&vocab_type=word
```

### 7. Delete Vocabulary Item
**DELETE** `/api/v1/vocabulary/{vocab_id}`

Delete a vocabulary item (only if it belongs to the current user).

**Response:**
```json
{
  "message": "Vocabulary item deleted successfully"
}
```

## Data Models

### Vocabulary Types
- `character`: Individual Braille characters
- `word`: Complete words or phrases

### Difficulty Levels
- `beginner`: Basic level vocabulary
- `intermediate`: Medium difficulty vocabulary
- `advanced`: Complex vocabulary

### Example Usage Flow

1. **User learns a new character:**
```bash
curl -X POST "http://localhost:8000/api/v1/vocabulary" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "ㄱ",
    "vocab_type": "character",
    "difficulty_level": "beginner",
    "braille_representation": "⠈"
  }'
```

2. **Check learning progress:**
```bash
curl "http://localhost:8000/api/v1/vocabulary/stats" \
  -H "Authorization: Bearer <token>"
```

3. **Get recent learned words:**
```bash
curl "http://localhost:8000/api/v1/vocabulary/words?limit=5" \
  -H "Authorization: Bearer <token>"
```

## Features

✅ **Personal Vocabulary Tracking**: Each user maintains their own vocabulary library
✅ **Timestamps**: Automatic tracking of when items were learned
✅ **Difficulty Levels**: Organize vocabulary by learning difficulty
✅ **Statistics**: Comprehensive learning progress statistics
✅ **Search**: Find specific vocabulary items
✅ **Filtering**: Filter by type, difficulty, and other criteria
✅ **Security**: All endpoints are JWT protected

## Integration with ReadAble Platform

This vocabulary system integrates with the broader ReadAble platform to:
- Track learning progress across different difficulty levels
- Provide personalized content based on learned vocabulary
- Generate statistics for the adaptive learning system
- Support the AI-powered quiz generation system
