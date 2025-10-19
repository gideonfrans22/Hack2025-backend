# ⠃ Korean Braille Electronic Notation System

## Overview

The ReadAble platform uses an electronic braille notation system for Korean language braille. This system represents braille cells as arrays of active dots, making it easy to programmatically generate, store, and render braille characters.

## 🔢 Braille Cell Structure

Korean braille uses **6-dot cells** arranged in **3 rows and 2 columns**:

```
┌─────┬─────┐
│  1  │  4  │  ← Top row
├─────┼─────┤
│  2  │  5  │  ← Middle row
├─────┼─────┤
│  3  │  6  │  ← Bottom row
└─────┴─────┘
 Left  Right
Column Column
```

### Dot Numbering

- **Dot 1**: Top left
- **Dot 2**: Middle left
- **Dot 3**: Bottom left
- **Dot 4**: Top right
- **Dot 5**: Middle right
- **Dot 6**: Bottom right

## 💻 Electronic Notation Format

### Data Type

```python
braille_representation: Optional[List[List[int]]]
```

### Structure

- **Outer array**: Represents multiple braille cells (for words/phrases)
- **Inner array**: Contains active dot numbers (1-6) for each cell
- **Empty array `[]`**: Represents a space or empty cell

### Examples

#### Single Character (ㄱ)

```json
{
  "content": "ㄱ",
  "braille_representation": [[4]]
}
```

Visual representation:

```
⠈
(Only dot 4 is active)
```

#### Single Character (ㄴ)

```json
{
  "content": "ㄴ",
  "braille_representation": [[1, 4]]
}
```

Visual representation:

```
⠉
(Dots 1 and 4 are active)
```

#### Word (가다)

```json
{
  "content": "가다",
  "braille_representation": [
    [1, 2, 4, 5],
    [2, 4]
  ]
}
```

Visual representation:

```
⠿ ⠊
(First cell: dots 1,2,4,5 | Second cell: dots 2,4)
```

## 📋 Common Korean Braille Characters

### Basic Consonants (초성)

| Character | Dots      | Notation            | Visual |
| --------- | --------- | ------------------- | ------ |
| ㄱ        | 4         | `[[4]]`             | ⠈      |
| ㄴ        | 1,4       | `[[1, 4]]`          | ⠉      |
| ㄷ        | 2,4       | `[[2, 4]]`          | ⠊      |
| ㄹ        | 5         | `[[5]]`             | ⠐      |
| ㅁ        | 1,5       | `[[1, 5]]`          | ⠑      |
| ㅂ        | 4,5       | `[[4, 5]]`          | ⠘      |
| ㅅ        | 1,2,4     | `[[1, 2, 4]]`       | ⠋      |
| ㅇ        | 1,2,4,5   | `[[1, 2, 4, 5]]`    | ⠛      |
| ㅈ        | 4,6       | `[[4, 6]]`          | ⠨      |
| ㅊ        | 5,6       | `[[5, 6]]`          | ⠰      |
| ㅋ        | 1,2,4,5,6 | `[[1, 2, 4, 5, 6]]` | ⠻      |
| ㅌ        | 1,2,5,6   | `[[1, 2, 5, 6]]`    | ⠳      |
| ㅍ        | 1,4,5,6   | `[[1, 4, 5, 6]]`    | ⠹      |
| ㅎ        | 2,4,5,6   | `[[2, 4, 5, 6]]`    | ⠺      |

### Basic Vowels (중성)

| Character | Dots      | Notation            | Visual |
| --------- | --------- | ------------------- | ------ |
| ㅏ        | 1,2,6     | `[[1, 2, 6]]`       | ⠣      |
| ㅑ        | 3,4,5     | `[[3, 4, 5]]`       | ⠜      |
| ㅓ        | 2,3,5     | `[[2, 3, 5]]`       | ⠎      |
| ㅕ        | 1,3,4,6   | `[[1, 3, 4, 6]]`    | ⠱      |
| ㅗ        | 1,2,6     | `[[1, 2, 6]]`       | ⠣      |
| ㅛ        | 3,4,5     | `[[3, 4, 5]]`       | ⠜      |
| ㅜ        | 1,3,4,6   | `[[1, 3, 4, 6]]`    | ⠱      |
| ㅠ        | 1,3,4,5,6 | `[[1, 3, 4, 5, 6]]` | ⠽      |
| ㅡ        | 2,4,6     | `[[2, 4, 6]]`       | ⠪      |
| ㅣ        | 1,3,5     | `[[1, 3, 5]]`       | ⠕      |

## 📝 API Usage Examples

### 1. Create Single Character Vocabulary

**Request**:

```bash
curl -X POST http://localhost:8000/api/v1/vocab/add \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "content": "ㄱ",
    "vocab_type": "character",
    "difficulty_level": "beginner",
    "braille_representation": [[4]]
  }'
```

**Response**:

```json
{
  "id": "vocab_doc_id",
  "user_email": "user@example.com",
  "content": "ㄱ",
  "vocab_type": "character",
  "difficulty_level": "beginner",
  "braille_representation": [[4]],
  "learned_at": "2025-10-19T10:00:00Z"
}
```

### 2. Create Word Vocabulary

**Request**:

```bash
curl -X POST http://localhost:8000/api/v1/vocab/add \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "content": "가다",
    "vocab_type": "word",
    "difficulty_level": "intermediate",
    "braille_representation": [[1, 2, 4, 5], [2, 4]]
  }'
```

**Response**:

```json
{
  "id": "vocab_doc_id",
  "user_email": "user@example.com",
  "content": "가다",
  "vocab_type": "word",
  "difficulty_level": "intermediate",
  "braille_representation": [
    [1, 2, 4, 5],
    [2, 4]
  ],
  "learned_at": "2025-10-19T10:00:00Z"
}
```

### 3. Create Multiple Character Word

**Request**:

```bash
curl -X POST http://localhost:8000/api/v1/vocab/add \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "content": "한글",
    "vocab_type": "word",
    "difficulty_level": "beginner",
    "braille_representation": [[2, 4, 5, 6], [1, 2, 4], [4], [2, 4, 6]]
  }'
```

## 🎨 Frontend Rendering

### React Component Example

```jsx
const BrailleCell = ({ dots = [] }) => {
  // dots is an array like [1, 2, 4, 5]
  const isDotActive = (dotNumber) => dots.includes(dotNumber);

  return (
    <div className="braille-cell">
      <div className="braille-row">
        <span className={isDotActive(1) ? "dot active" : "dot"}>⚫</span>
        <span className={isDotActive(4) ? "dot active" : "dot"}>⚫</span>
      </div>
      <div className="braille-row">
        <span className={isDotActive(2) ? "dot active" : "dot"}>⚫</span>
        <span className={isDotActive(5) ? "dot active" : "dot"}>⚫</span>
      </div>
      <div className="braille-row">
        <span className={isDotActive(3) ? "dot active" : "dot"}>⚫</span>
        <span className={isDotActive(6) ? "dot active" : "dot"}>⚫</span>
      </div>
    </div>
  );
};

const BrailleWord = ({ brailleRepresentation = [] }) => {
  // brailleRepresentation is like [[4], [1, 4], [2, 4]]
  return (
    <div className="braille-word">
      {brailleRepresentation.map((cellDots, index) => (
        <BrailleCell key={index} dots={cellDots} />
      ))}
    </div>
  );
};

// Usage
<BrailleWord
  brailleRepresentation={[
    [1, 2, 4, 5],
    [2, 4]
  ]}
/>;
```

### CSS Styling

```css
.braille-cell {
  display: inline-block;
  margin: 0 10px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 8px;
}

.braille-row {
  display: flex;
  justify-content: space-between;
  gap: 15px;
  margin: 8px 0;
}

.dot {
  display: inline-block;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background-color: #e0e0e0;
  transition: background-color 0.3s;
}

.dot.active {
  background-color: #2196f3;
  box-shadow: 0 0 10px rgba(33, 150, 243, 0.5);
}
```

## 🔄 Conversion Utilities

### Python Helper Function

```python
def dots_to_unicode_braille(dots: List[int]) -> str:
    """
    Convert dot notation to Unicode braille character

    Args:
        dots: List of active dots (1-6)

    Returns:
        Unicode braille character
    """
    # Unicode braille patterns start at U+2800
    base = 0x2800

    # Calculate the offset based on active dots
    offset = sum(2 ** (dot - 1) for dot in dots)

    return chr(base + offset)

# Example usage
print(dots_to_unicode_braille([4]))  # Output: ⠈ (ㄱ)
print(dots_to_unicode_braille([1, 2, 4, 5]))  # Output: ⠛ (ㅇ)
```

### JavaScript Helper Function

```javascript
function dotsToUnicodeBraille(dots) {
  // Unicode braille patterns start at U+2800
  const base = 0x2800;

  // Calculate the offset based on active dots
  const offset = dots.reduce((sum, dot) => sum + Math.pow(2, dot - 1), 0);

  return String.fromCodePoint(base + offset);
}

// Example usage
console.log(dotsToUnicodeBraille([4])); // Output: ⠈ (ㄱ)
console.log(dotsToUnicodeBraille([1, 2, 4, 5])); // Output: ⠛ (ㅇ)
```

## 🧪 Validation

### Pydantic Validation

The model automatically validates:

- ✅ `braille_representation` is a list of lists
- ✅ Inner lists contain integers
- ✅ Optional field (can be `null`)

### Custom Validation (Optional)

You can add custom validators to ensure dot numbers are 1-6:

```python
from pydantic import validator

class VocabularyItem(BaseModel):
    # ... other fields
    braille_representation: Optional[List[List[int]]] = None

    @validator('braille_representation')
    def validate_braille_dots(cls, v):
        if v is not None:
            for cell in v:
                for dot in cell:
                    if dot < 1 or dot > 6:
                        raise ValueError(f'점자 도트 번호는 1-6 사이여야 합니다 (입력값: {dot})')
        return v
```

## 📊 Database Storage

### Firestore Document Example

```json
{
  "content": "가다",
  "vocab_type": "word",
  "difficulty_level": "intermediate",
  "braille_representation": [
    [1, 2, 4, 5],
    [2, 4]
  ],
  "learned_at": "2025-10-19T10:00:00.000Z",
  "user_email": "user@example.com"
}
```

## 🎯 Benefits of This System

### 1. **Programmatic Generation**

```python
# Easy to generate braille programmatically
braille_for_giyeok = [[4]]
braille_for_nieun = [[1, 4]]
```

### 2. **Easy Rendering**

- Simple to render on screen
- Convert to tactile braille displays
- Generate audio descriptions

### 3. **Flexible Storage**

- Compact JSON format
- Easy to query and filter
- Language-agnostic

### 4. **Accessibility**

- Can be converted to Unicode braille: ⠀⠁⠂⠃⠄⠅⠆⠇⠈⠉⠊⠋⠌⠍⠎⠏
- Compatible with screen readers
- Support for braille displays

## 📚 Resources

- **Unicode Braille Patterns**: U+2800 to U+28FF
- **Korean Braille**: 6-dot system
- **International Braille**: Used worldwide

## ✅ Migration from Old Format

If you had old string-based braille representations, migrate them:

### Old Format (String)

```json
{
  "braille_representation": "⠈⠉⠊"
}
```

### New Format (Array)

```json
{
  "braille_representation": [[4], [1, 4], [2, 4]]
}
```

## 🎉 Complete!

The braille notation system is now ready to use for the ReadAble Korean Braille learning platform! This electronic format makes it easy to:

- Store braille representations
- Render braille visually
- Convert to tactile output
- Generate AI-powered quizzes
- Track user progress

**Ready for braille-based learning!** ⠃⠗⠁⠊⠇⠇⠑
