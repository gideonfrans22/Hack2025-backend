# 📚 Braille Library API Documentation

## Overview

The Braille Library API provides access to a comprehensive Korean Braille character database based on the **2020 한글점자규정** (Korean Braille Standard). This API serves as a reference library for the ReadAble platform, offering detailed information about Korean braille characters, their dot patterns, and usage rules.

## Base URL

```
http://localhost:8000/api/v1/braille
```

## Coverage

The braille library covers:

- ✅ **제1절**: 자음자 (Consonants) - Initial consonants and double consonants
- ✅ **제2절**: 종성 (Final consonants/받침)
- ✅ **제3절**: 모음 (Vowels) - Simple vowels
- ✅ **제4절**: 이중모음 (Diphthongs)
- ✅ **제5절**: 모음 연쇄 (Vowel sequences)
- ✅ **숫자** (Numbers) - With number prefix (수표)
- ✅ **문장부호** (Punctuation marks)

## 📌 API Endpoints

### 1. Get All Braille Characters

**Endpoint**: `GET /api/v1/braille/library`

Retrieves the complete braille library with optional filtering.

**Query Parameters**:

- `category` (optional): Filter by category
  - `consonant_initial` - 초성 (자음)
  - `consonant_final` - 종성 (받침)
  - `vowel` - 모음
  - `vowel_sequence` - 모음 연쇄
  - `number` - 숫자
  - `punctuation` - 문장부호
  - `special` - 특수기호
  - `prefix` - 접두어 (수표)
- `search` (optional): Search by character or name

**Example Requests**:

```bash
# Get all braille characters
curl http://localhost:8000/api/v1/braille/library

# Get only consonants
curl "http://localhost:8000/api/v1/braille/library?category=consonant_initial"

# Search for "기역"
curl "http://localhost:8000/api/v1/braille/library?search=기역"

# Get vowels and search for "ㅏ"
curl "http://localhost:8000/api/v1/braille/library?category=vowel&search=ㅏ"
```

**Response Example**:

```json
{
  "total_count": 95,
  "categories": [
    "consonant_initial",
    "consonant_final",
    "vowel",
    "vowel_sequence",
    "number",
    "punctuation",
    "special",
    "prefix"
  ],
  "characters": [
    {
      "id": "cons_initial_01",
      "character": "ㄱ",
      "braille_dots": [4],
      "category": "consonant_initial",
      "name": "기역",
      "description": "초성 기역",
      "usage_notes": null,
      "rule_reference": "제1절 제1항",
      "examples": ["가", "고", "구"]
    },
    {
      "id": "vowel_01",
      "character": "ㅏ",
      "braille_dots": [1, 2, 6],
      "category": "vowel",
      "name": "모음 아",
      "description": "단모음 ㅏ",
      "usage_notes": null,
      "rule_reference": "제3절",
      "examples": ["아", "가", "나"]
    }
  ]
}
```

---

### 2. Get Category List

**Endpoint**: `GET /api/v1/braille/library/categories`

Returns all available braille categories.

**Example Request**:

```bash
curl http://localhost:8000/api/v1/braille/library/categories
```

**Response Example**:

```json
[
  "consonant_initial",
  "consonant_final",
  "vowel",
  "vowel_sequence",
  "number",
  "punctuation",
  "special",
  "prefix"
]
```

---

### 3. Get Braille Character by ID

**Endpoint**: `GET /api/v1/braille/library/{character_id}`

Retrieves detailed information for a specific braille character.

**Path Parameters**:

- `character_id`: Unique identifier (e.g., `cons_initial_01`, `vowel_01`)

**Example Request**:

```bash
curl http://localhost:8000/api/v1/braille/library/cons_initial_01
```

**Response Example**:

```json
{
  "id": "cons_initial_01",
  "character": "ㄱ",
  "braille_dots": [4],
  "category": "consonant_initial",
  "name": "기역",
  "description": "초성 기역",
  "usage_notes": null,
  "rule_reference": "제1절 제1항",
  "examples": ["가", "고", "구"]
}
```

**Error Response** (404):

```json
{
  "detail": "ID 'invalid_id'에 해당하는 점자 문자를 찾을 수 없습니다."
}
```

---

### 4. Get Braille by Category

**Endpoint**: `GET /api/v1/braille/library/category/{category_name}`

Retrieves all braille characters in a specific category.

**Path Parameters**:

- `category_name`: Category identifier
  - `consonant_initial` - 초성
  - `consonant_final` - 종성 (받침)
  - `vowel` - 모음
  - `vowel_sequence` - 모음 연쇄
  - `number` - 숫자
  - `punctuation` - 문장부호
  - `special` - 특수기호
  - `prefix` - 접두어

**Example Request**:

```bash
# Get all initial consonants
curl http://localhost:8000/api/v1/braille/library/category/consonant_initial

# Get all vowels
curl http://localhost:8000/api/v1/braille/library/category/vowel

# Get all numbers
curl http://localhost:8000/api/v1/braille/library/category/number
```

**Response Example**:

```json
{
  "total_count": 19,
  "categories": ["consonant_initial", "consonant_final", "vowel", ...],
  "characters": [
    {
      "id": "cons_initial_01",
      "character": "ㄱ",
      "braille_dots": [4],
      "category": "consonant_initial",
      "name": "기역",
      "description": "초성 기역",
      "rule_reference": "제1절 제1항",
      "examples": ["가", "고", "구"]
    },
    ...
  ]
}
```

---

### 5. Search Braille Characters

**Endpoint**: `GET /api/v1/braille/library/search/{query}`

Search braille characters by text or name.

**Path Parameters**:

- `query`: Search term (character or name)

**Example Requests**:

```bash
# Search for "ㄱ"
curl http://localhost:8000/api/v1/braille/library/search/ㄱ

# Search for "기역"
curl http://localhost:8000/api/v1/braille/library/search/기역

# Search for "받침"
curl http://localhost:8000/api/v1/braille/library/search/받침

# Search for "모음"
curl http://localhost:8000/api/v1/braille/library/search/모음
```

**Response Example**:

```json
{
  "total_count": 2,
  "categories": [...],
  "characters": [
    {
      "id": "cons_initial_01",
      "character": "ㄱ",
      "braille_dots": [4],
      "category": "consonant_initial",
      "name": "기역",
      "description": "초성 기역",
      "rule_reference": "제1절 제1항",
      "examples": ["가", "고", "구"]
    },
    {
      "id": "cons_final_01",
      "character": "ㄱ",
      "braille_dots": [1],
      "category": "consonant_final",
      "name": "받침 기역",
      "description": "종성 기역",
      "rule_reference": "제2절",
      "examples": ["악", "국", "격"]
    }
  ]
}
```

---

### 6. Text to Braille Converter (Preview)

**Endpoint**: `GET /api/v1/braille/convert/{text}`

Provides information about text-to-braille conversion. This is a preview endpoint.

⚠️ **Note**: This endpoint does NOT perform actual conversion. It provides guidance for using the library API.

**Path Parameters**:

- `text`: Korean text to get information about

**Example Request**:

```bash
curl http://localhost:8000/api/v1/braille/convert/안녕
```

**Response Example**:

```json
{
  "original_text": "안녕",
  "notice": "이 기능은 기본 미리보기입니다. 완전한 점자 변환은 별도 라이브러리가 필요합니다.",
  "suggestion": "점자 도서관 API를 사용하여 개별 문자의 점자 표현을 확인하세요.",
  "library_endpoint": "/api/v1/braille/library"
}
```

---

## 📊 Data Structure

### BrailleCharacter Model

```typescript
{
  id: string;                    // Unique identifier
  character: string;             // Korean character or symbol
  braille_dots: number[];        // Array of active dots (1-6)
  category: BrailleCategory;     // Character category
  name: string;                  // Character name (e.g., "기역", "니은")
  description: string | null;    // Description
  usage_notes: string | null;    // Usage guidelines
  rule_reference: string | null; // Reference to braille standard (e.g., "제1절")
  examples: string[];            // Usage examples
}
```

### BrailleCategory Enum

```typescript
enum BrailleCategory {
  CONSONANT_INITIAL = "consonant_initial", // 초성
  CONSONANT_FINAL = "consonant_final", // 종성
  VOWEL = "vowel", // 모음
  VOWEL_SEQUENCE = "vowel_sequence", // 모음 연쇄
  NUMBER = "number", // 숫자
  PUNCTUATION = "punctuation", // 문장부호
  SPECIAL = "special", // 특수기호
  PREFIX = "prefix" // 접두어
}
```

---

## 🎯 Use Cases

### 1. Display Braille Alphabet

```python
import requests

# Get all initial consonants
response = requests.get(
    "http://localhost:8000/api/v1/braille/library/category/consonant_initial"
)
consonants = response.json()["characters"]

for char in consonants:
    print(f"{char['character']} ({char['name']}): {char['braille_dots']}")
```

Output:

```
ㄱ (기역): [4]
ㄴ (니은): [1, 4]
ㄷ (디귿): [2, 4]
...
```

### 2. Search for Specific Character

```python
import requests

# Search for "기역"
response = requests.get(
    "http://localhost:8000/api/v1/braille/library/search/기역"
)
results = response.json()["characters"]

for char in results:
    print(f"Category: {char['category']}")
    print(f"Character: {char['character']}")
    print(f"Dots: {char['braille_dots']}")
    print(f"Examples: {', '.join(char['examples'])}")
    print("---")
```

### 3. Get Character Details

```python
import requests

# Get details for specific character
response = requests.get(
    "http://localhost:8000/api/v1/braille/library/cons_initial_01"
)
character = response.json()

print(f"Character: {character['character']}")
print(f"Name: {character['name']}")
print(f"Dots: {character['braille_dots']}")
print(f"Rule: {character['rule_reference']}")
```

### 4. Filter and Search

```python
import requests

# Get all vowels containing "ㅏ"
response = requests.get(
    "http://localhost:8000/api/v1/braille/library",
    params={"category": "vowel", "search": "ㅏ"}
)
vowels = response.json()["characters"]
```

---

## 📖 Braille Character Reference

### Initial Consonants (초성)

| Character | Name | Dots              | Visual |
| --------- | ---- | ----------------- | ------ |
| ㄱ        | 기역 | `[4]`             | ⠈      |
| ㄴ        | 니은 | `[1, 4]`          | ⠉      |
| ㄷ        | 디귿 | `[2, 4]`          | ⠊      |
| ㄹ        | 리을 | `[5]`             | ⠐      |
| ㅁ        | 미음 | `[1, 5]`          | ⠑      |
| ㅂ        | 비읍 | `[4, 5]`          | ⠘      |
| ㅅ        | 시옷 | `[1, 2, 3]`       | ⠇      |
| ㅇ        | 이응 | `[1, 2, 4, 5]`    | ⠛      |
| ㅈ        | 지읒 | `[4, 6]`          | ⠨      |
| ㅊ        | 치읓 | `[5, 6]`          | ⠰      |
| ㅋ        | 키읔 | `[1, 2, 4, 5, 6]` | ⠻      |
| ㅌ        | 티읕 | `[1, 2, 5, 6]`    | ⠳      |
| ㅍ        | 피읖 | `[1, 4, 5, 6]`    | ⠹      |
| ㅎ        | 히읗 | `[2, 4, 5, 6]`    | ⠺      |

### Double Consonants (된소리)

| Character | Name   | Dots                 | Usage           |
| --------- | ------ | -------------------- | --------------- |
| ㄲ        | 쌍기역 | `[4, 4]`             | 같은 자음 두 번 |
| ㄸ        | 쌍디귿 | `[2, 4, 2, 4]`       | 같은 자음 두 번 |
| ㅃ        | 쌍비읍 | `[4, 5, 4, 5]`       | 같은 자음 두 번 |
| ㅆ        | 쌍시옷 | `[1, 2, 3, 1, 2, 3]` | 같은 자음 두 번 |
| ㅉ        | 쌍지읒 | `[4, 6, 4, 6]`       | 같은 자음 두 번 |

### Basic Vowels (단모음)

| Character | Name | Dots              | Visual |
| --------- | ---- | ----------------- | ------ |
| ㅏ        | 아   | `[1, 2, 6]`       | ⠣      |
| ㅑ        | 야   | `[3, 4, 5]`       | ⠜      |
| ㅓ        | 어   | `[2, 3, 5]`       | ⠎      |
| ㅕ        | 여   | `[1, 3, 4, 6]`    | ⠱      |
| ㅗ        | 오   | `[1, 3, 6]`       | ⠡      |
| ㅛ        | 요   | `[3, 4, 6]`       | ⠬      |
| ㅜ        | 우   | `[1, 3, 4]`       | ⠕      |
| ㅠ        | 유   | `[1, 3, 4, 5, 6]` | ⠽      |
| ㅡ        | 으   | `[2, 4, 6]`       | ⠪      |
| ㅣ        | 이   | `[1, 3, 5]`       | ⠕      |

### Numbers (숫자)

| Character | Dots           | Usage          |
| --------- | -------------- | -------------- |
| # (수표)  | `[3, 4, 5, 6]` | 숫자 앞에 표시 |
| 0         | `[2, 4, 5]`    | 수표 뒤        |
| 1         | `[1]`          | 수표 뒤        |
| 2         | `[1, 2]`       | 수표 뒤        |
| 3         | `[1, 4]`       | 수표 뒤        |
| 4         | `[1, 4, 5]`    | 수표 뒤        |
| 5         | `[1, 5]`       | 수표 뒤        |
| 6         | `[1, 2, 4]`    | 수표 뒤        |
| 7         | `[1, 2, 4, 5]` | 수표 뒤        |
| 8         | `[1, 2, 5]`    | 수표 뒤        |
| 9         | `[2, 4]`       | 수표 뒤        |

---

## 🔧 Frontend Integration

### React Component Example

```jsx
import React, { useEffect, useState } from "react";
import axios from "axios";

const BrailleLibrary = () => {
  const [characters, setCharacters] = useState([]);
  const [category, setCategory] = useState("consonant_initial");

  useEffect(() => {
    const fetchBraille = async () => {
      const response = await axios.get(
        `http://localhost:8000/api/v1/braille/library/category/${category}`
      );
      setCharacters(response.data.characters);
    };

    fetchBraille();
  }, [category]);

  return (
    <div>
      <select onChange={(e) => setCategory(e.target.value)} value={category}>
        <option value="consonant_initial">초성</option>
        <option value="consonant_final">종성</option>
        <option value="vowel">모음</option>
        <option value="number">숫자</option>
      </select>

      <div className="braille-grid">
        {characters.map((char) => (
          <div key={char.id} className="braille-card">
            <h3>{char.character}</h3>
            <p>{char.name}</p>
            <p>Dots: {char.braille_dots.join(", ")}</p>
            <div className="examples">
              {char.examples.map((ex, i) => (
                <span key={i}>{ex}</span>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default BrailleLibrary;
```

---

## ✅ Testing the API

### Using cURL

```bash
# Test get all
curl http://localhost:8000/api/v1/braille/library

# Test category filter
curl "http://localhost:8000/api/v1/braille/library?category=vowel"

# Test search
curl "http://localhost:8000/api/v1/braille/library?search=기역"

# Test get by ID
curl http://localhost:8000/api/v1/braille/library/cons_initial_01

# Test category endpoint
curl http://localhost:8000/api/v1/braille/library/category/number
```

### Using Python

```python
import requests

BASE_URL = "http://localhost:8000/api/v1/braille"

# Get all characters
response = requests.get(f"{BASE_URL}/library")
print(f"Total characters: {response.json()['total_count']}")

# Get specific category
response = requests.get(f"{BASE_URL}/library/category/consonant_initial")
print(f"Initial consonants: {len(response.json()['characters'])}")

# Search
response = requests.get(f"{BASE_URL}/library/search/모음")
print(f"Found {response.json()['total_count']} results")
```

---

## 📝 Notes

1. **Data Source**: Based on 2020 한글점자규정해설서 (Korean Braille Standard Guide)
2. **Coverage**: Sections 1-5 (제1절 ~ 제5절) + Numbers + Basic punctuation
3. **Storage**: All data stored locally in `data/braille_library.py`
4. **No Authentication**: Public API, no authentication required
5. **Read-Only**: This is a reference library (no POST/PUT/DELETE)

---

## 🚀 Next Steps

To extend the braille library:

1. **Add more punctuation marks** (제2장 문장부호)
2. **Add special symbols** (특수기호)
3. **Add abbreviations** (약자)
4. **Add contractions** (약어)
5. **Implement full text-to-braille conversion**

---

## 📞 Support

For questions or issues with the Braille Library API, refer to the main ReadAble API documentation or check the Korean Braille Standard reference document.

**API Version**: 2.0.0  
**Last Updated**: 2025-10-19
