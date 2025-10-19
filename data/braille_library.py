"""
Braille Library Data
Based on 2020 한글점자규정해설서 (Korean Braille Standard Guide)
Sections covered: 제1절 ~ 제5절 (Sections 1-5)
"""
from typing import List, Dict
from models.braille_models import BrailleCharacter, BrailleCategory


# 제1절: 자음자 (Consonants)
INITIAL_CONSONANTS: List[Dict] = [
    {
        "id": "cons_initial_01",
        "character": "ㄱ",
        "braille_dots": [4],
        "category": BrailleCategory.CONSONANT_INITIAL,
        "name": "기역",
        "description": "초성 기역",
        "rule_reference": "제1절 제1항",
        "examples": ["가", "고", "구"]
    },
    {
        "id": "cons_initial_02",
        "character": "ㄴ",
        "braille_dots": [1, 4],
        "category": BrailleCategory.CONSONANT_INITIAL,
        "name": "니은",
        "description": "초성 니은",
        "rule_reference": "제1절 제1항",
        "examples": ["나", "노", "누"]
    },
    {
        "id": "cons_initial_03",
        "character": "ㄷ",
        "braille_dots": [2, 4],
        "category": BrailleCategory.CONSONANT_INITIAL,
        "name": "디귿",
        "description": "초성 디귿",
        "rule_reference": "제1절 제1항",
        "examples": ["다", "도", "두"]
    },
    {
        "id": "cons_initial_04",
        "character": "ㄹ",
        "braille_dots": [5],
        "category": BrailleCategory.CONSONANT_INITIAL,
        "name": "리을",
        "description": "초성 리을",
        "rule_reference": "제1절 제1항",
        "examples": ["라", "로", "루"]
    },
    {
        "id": "cons_initial_05",
        "character": "ㅁ",
        "braille_dots": [1, 5],
        "category": BrailleCategory.CONSONANT_INITIAL,
        "name": "미음",
        "description": "초성 미음",
        "rule_reference": "제1절 제1항",
        "examples": ["마", "모", "무"]
    },
    {
        "id": "cons_initial_06",
        "character": "ㅂ",
        "braille_dots": [4, 5],
        "category": BrailleCategory.CONSONANT_INITIAL,
        "name": "비읍",
        "description": "초성 비읍",
        "rule_reference": "제1절 제1항",
        "examples": ["바", "보", "부"]
    },
    {
        "id": "cons_initial_07",
        "character": "ㅅ",
        "braille_dots": [1, 2, 3],
        "category": BrailleCategory.CONSONANT_INITIAL,
        "name": "시옷",
        "description": "초성 시옷",
        "rule_reference": "제1절 제1항",
        "examples": ["사", "소", "수"]
    },
    {
        "id": "cons_initial_08",
        "character": "ㅇ",
        "braille_dots": [1, 2, 4, 5],
        "category": BrailleCategory.CONSONANT_INITIAL,
        "name": "이응",
        "description": "초성 이응 (무음)",
        "rule_reference": "제1절 제1항",
        "examples": ["아", "오", "우"],
        "usage_notes": "초성에서 무음을 나타냄"
    },
    {
        "id": "cons_initial_09",
        "character": "ㅈ",
        "braille_dots": [4, 6],
        "category": BrailleCategory.CONSONANT_INITIAL,
        "name": "지읒",
        "description": "초성 지읒",
        "rule_reference": "제1절 제1항",
        "examples": ["자", "조", "주"]
    },
    {
        "id": "cons_initial_10",
        "character": "ㅊ",
        "braille_dots": [5, 6],
        "category": BrailleCategory.CONSONANT_INITIAL,
        "name": "치읓",
        "description": "초성 치읓",
        "rule_reference": "제1절 제1항",
        "examples": ["차", "초", "추"]
    },
    {
        "id": "cons_initial_11",
        "character": "ㅋ",
        "braille_dots": [1, 2, 4, 5, 6],
        "category": BrailleCategory.CONSONANT_INITIAL,
        "name": "키읔",
        "description": "초성 키읔",
        "rule_reference": "제1절 제1항",
        "examples": ["카", "코", "쿠"]
    },
    {
        "id": "cons_initial_12",
        "character": "ㅌ",
        "braille_dots": [1, 2, 5, 6],
        "category": BrailleCategory.CONSONANT_INITIAL,
        "name": "티읕",
        "description": "초성 티읕",
        "rule_reference": "제1절 제1항",
        "examples": ["타", "토", "투"]
    },
    {
        "id": "cons_initial_13",
        "character": "ㅍ",
        "braille_dots": [1, 4, 5, 6],
        "category": BrailleCategory.CONSONANT_INITIAL,
        "name": "피읖",
        "description": "초성 피읖",
        "rule_reference": "제1절 제1항",
        "examples": ["파", "포", "푸"]
    },
    {
        "id": "cons_initial_14",
        "character": "ㅎ",
        "braille_dots": [2, 4, 5, 6],
        "category": BrailleCategory.CONSONANT_INITIAL,
        "name": "히읗",
        "description": "초성 히읗",
        "rule_reference": "제1절 제1항",
        "examples": ["하", "호", "후"]
    },
    # 된소리 (Double consonants)
    {
        "id": "cons_initial_15",
        "character": "ㄲ",
        "braille_dots": [4, 4],
        "category": BrailleCategory.CONSONANT_INITIAL,
        "name": "쌍기역",
        "description": "된소리 기역",
        "rule_reference": "제1절 제2항",
        "examples": ["까", "꼬", "꾸"],
        "usage_notes": "같은 자음을 두 번 적음"
    },
    {
        "id": "cons_initial_16",
        "character": "ㄸ",
        "braille_dots": [2, 4, 2, 4],
        "category": BrailleCategory.CONSONANT_INITIAL,
        "name": "쌍디귿",
        "description": "된소리 디귿",
        "rule_reference": "제1절 제2항",
        "examples": ["따", "또", "뚜"],
        "usage_notes": "같은 자음을 두 번 적음"
    },
    {
        "id": "cons_initial_17",
        "character": "ㅃ",
        "braille_dots": [4, 5, 4, 5],
        "category": BrailleCategory.CONSONANT_INITIAL,
        "name": "쌍비읍",
        "description": "된소리 비읍",
        "rule_reference": "제1절 제2항",
        "examples": ["빠", "뽀", "뿌"],
        "usage_notes": "같은 자음을 두 번 적음"
    },
    {
        "id": "cons_initial_18",
        "character": "ㅆ",
        "braille_dots": [1, 2, 3, 1, 2, 3],
        "category": BrailleCategory.CONSONANT_INITIAL,
        "name": "쌍시옷",
        "description": "된소리 시옷",
        "rule_reference": "제1절 제2항",
        "examples": ["싸", "쏘", "쑤"],
        "usage_notes": "같은 자음을 두 번 적음"
    },
    {
        "id": "cons_initial_19",
        "character": "ㅉ",
        "braille_dots": [4, 6, 4, 6],
        "category": BrailleCategory.CONSONANT_INITIAL,
        "name": "쌍지읒",
        "description": "된소리 지읒",
        "rule_reference": "제1절 제2항",
        "examples": ["짜", "쪼", "쭈"],
        "usage_notes": "같은 자음을 두 번 적음"
    }
]

# 제2절: 종성 (Final consonants)
FINAL_CONSONANTS: List[Dict] = [
    {
        "id": "cons_final_01",
        "character": "ㄱ",
        "braille_dots": [1],
        "category": BrailleCategory.CONSONANT_FINAL,
        "name": "받침 기역",
        "description": "종성 기역",
        "rule_reference": "제2절",
        "examples": ["악", "국", "격"]
    },
    {
        "id": "cons_final_02",
        "character": "ㄴ",
        "braille_dots": [2, 5],
        "category": BrailleCategory.CONSONANT_FINAL,
        "name": "받침 니은",
        "description": "종성 니은",
        "rule_reference": "제2절",
        "examples": ["안", "눈", "던"]
    },
    {
        "id": "cons_final_03",
        "character": "ㄷ",
        "braille_dots": [2, 4, 6],
        "category": BrailleCategory.CONSONANT_FINAL,
        "name": "받침 디귿",
        "description": "종성 디귿",
        "rule_reference": "제2절",
        "examples": ["앋", "곧", "믿"]
    },
    {
        "id": "cons_final_04",
        "character": "ㄹ",
        "braille_dots": [2],
        "category": BrailleCategory.CONSONANT_FINAL,
        "name": "받침 리을",
        "description": "종성 리을",
        "rule_reference": "제2절",
        "examples": ["알", "길", "물"]
    },
    {
        "id": "cons_final_05",
        "character": "ㅁ",
        "braille_dots": [2, 6],
        "category": BrailleCategory.CONSONANT_FINAL,
        "name": "받침 미음",
        "description": "종성 미음",
        "rule_reference": "제2절",
        "examples": ["암", "금", "심"]
    },
    {
        "id": "cons_final_06",
        "character": "ㅂ",
        "braille_dots": [1, 2],
        "category": BrailleCategory.CONSONANT_FINAL,
        "name": "받침 비읍",
        "description": "종성 비읍",
        "rule_reference": "제2절",
        "examples": ["압", "급", "입"]
    },
    {
        "id": "cons_final_07",
        "character": "ㅅ",
        "braille_dots": [3, 4],
        "category": BrailleCategory.CONSONANT_FINAL,
        "name": "받침 시옷",
        "description": "종성 시옷",
        "rule_reference": "제2절",
        "examples": ["았", "곧", "있"]
    },
    {
        "id": "cons_final_08",
        "character": "ㅇ",
        "braille_dots": [2, 6],
        "category": BrailleCategory.CONSONANT_FINAL,
        "name": "받침 이응",
        "description": "종성 이응",
        "rule_reference": "제2절",
        "examples": ["앙", "공", "강"]
    },
    {
        "id": "cons_final_09",
        "character": "ㅈ",
        "braille_dots": [3, 5],
        "category": BrailleCategory.CONSONANT_FINAL,
        "name": "받침 지읒",
        "description": "종성 지읒",
        "rule_reference": "제2절",
        "examples": ["앚", "곶"]
    },
    {
        "id": "cons_final_10",
        "character": "ㅊ",
        "braille_dots": [3, 6],
        "category": BrailleCategory.CONSONANT_FINAL,
        "name": "받침 치읓",
        "description": "종성 치읓",
        "rule_reference": "제2절",
        "examples": ["앟", "곾"]
    },
    {
        "id": "cons_final_11",
        "character": "ㅋ",
        "braille_dots": [1, 3, 4, 5, 6],
        "category": BrailleCategory.CONSONANT_FINAL,
        "name": "받침 키읔",
        "description": "종성 키읔",
        "rule_reference": "제2절",
        "examples": ["앜"]
    },
    {
        "id": "cons_final_12",
        "character": "ㅌ",
        "braille_dots": [3, 4, 5, 6],
        "category": BrailleCategory.CONSONANT_FINAL,
        "name": "받침 티읕",
        "description": "종성 티읕",
        "rule_reference": "제2절",
        "examples": ["앝", "핥"]
    },
    {
        "id": "cons_final_13",
        "character": "ㅍ",
        "braille_dots": [1, 3, 5, 6],
        "category": BrailleCategory.CONSONANT_FINAL,
        "name": "받침 피읖",
        "description": "종성 피읖",
        "rule_reference": "제2절",
        "examples": ["앞", "잎"]
    },
    {
        "id": "cons_final_14",
        "character": "ㅎ",
        "braille_dots": [3, 4, 6],
        "category": BrailleCategory.CONSONANT_FINAL,
        "name": "받침 히읗",
        "description": "종성 히읗",
        "rule_reference": "제2절",
        "examples": ["앟", "놓", "좋"]
    }
]

# 제3절: 모음 (Vowels)
VOWELS: List[Dict] = [
    {
        "id": "vowel_01",
        "character": "ㅏ",
        "braille_dots": [1, 2, 6],
        "category": BrailleCategory.VOWEL,
        "name": "모음 아",
        "description": "단모음 ㅏ",
        "rule_reference": "제3절",
        "examples": ["아", "가", "나"]
    },
    {
        "id": "vowel_02",
        "character": "ㅑ",
        "braille_dots": [3, 4, 5],
        "category": BrailleCategory.VOWEL,
        "name": "모음 야",
        "description": "단모음 ㅑ",
        "rule_reference": "제3절",
        "examples": ["야", "갸", "냐"]
    },
    {
        "id": "vowel_03",
        "character": "ㅓ",
        "braille_dots": [2, 3, 5],
        "category": BrailleCategory.VOWEL,
        "name": "모음 어",
        "description": "단모음 ㅓ",
        "rule_reference": "제3절",
        "examples": ["어", "거", "너"]
    },
    {
        "id": "vowel_04",
        "character": "ㅕ",
        "braille_dots": [1, 3, 4, 6],
        "category": BrailleCategory.VOWEL,
        "name": "모음 여",
        "description": "단모음 ㅕ",
        "rule_reference": "제3절",
        "examples": ["여", "겨", "녀"]
    },
    {
        "id": "vowel_05",
        "character": "ㅗ",
        "braille_dots": [1, 3, 6],
        "category": BrailleCategory.VOWEL,
        "name": "모음 오",
        "description": "단모음 ㅗ",
        "rule_reference": "제3절",
        "examples": ["오", "고", "노"]
    },
    {
        "id": "vowel_06",
        "character": "ㅛ",
        "braille_dots": [3, 4, 6],
        "category": BrailleCategory.VOWEL,
        "name": "모음 요",
        "description": "단모음 ㅛ",
        "rule_reference": "제3절",
        "examples": ["요", "교", "뇨"]
    },
    {
        "id": "vowel_07",
        "character": "ㅜ",
        "braille_dots": [1, 3, 4],
        "category": BrailleCategory.VOWEL,
        "name": "모음 우",
        "description": "단모음 ㅜ",
        "rule_reference": "제3절",
        "examples": ["우", "구", "누"]
    },
    {
        "id": "vowel_08",
        "character": "ㅠ",
        "braille_dots": [1, 3, 4, 5, 6],
        "category": BrailleCategory.VOWEL,
        "name": "모음 유",
        "description": "단모음 ㅠ",
        "rule_reference": "제3절",
        "examples": ["유", "규", "뉴"]
    },
    {
        "id": "vowel_09",
        "character": "ㅡ",
        "braille_dots": [2, 4, 6],
        "category": BrailleCategory.VOWEL,
        "name": "모음 으",
        "description": "단모음 ㅡ",
        "rule_reference": "제3절",
        "examples": ["으", "그", "느"]
    },
    {
        "id": "vowel_10",
        "character": "ㅣ",
        "braille_dots": [1, 3, 5],
        "category": BrailleCategory.VOWEL,
        "name": "모음 이",
        "description": "단모음 ㅣ",
        "rule_reference": "제3절",
        "examples": ["이", "기", "니"]
    },
    # 이중모음 (Diphthongs) - 제4절
    {
        "id": "vowel_11",
        "character": "ㅐ",
        "braille_dots": [1, 2, 3, 5],
        "category": BrailleCategory.VOWEL,
        "name": "모음 애",
        "description": "이중모음 ㅐ",
        "rule_reference": "제4절",
        "examples": ["애", "개", "내"]
    },
    {
        "id": "vowel_12",
        "character": "ㅒ",
        "braille_dots": [3, 4, 5, 1, 3, 5],
        "category": BrailleCategory.VOWEL,
        "name": "모음 얘",
        "description": "이중모음 ㅒ",
        "rule_reference": "제4절",
        "examples": ["얘", "걔", "냬"],
        "usage_notes": "ㅑ + ㅣ로 적음"
    },
    {
        "id": "vowel_13",
        "character": "ㅔ",
        "braille_dots": [1, 3, 4, 5],
        "category": BrailleCategory.VOWEL,
        "name": "모음 에",
        "description": "이중모음 ㅔ",
        "rule_reference": "제4절",
        "examples": ["에", "게", "네"]
    },
    {
        "id": "vowel_14",
        "character": "ㅖ",
        "braille_dots": [1, 3, 4, 6, 1, 3, 5],
        "category": BrailleCategory.VOWEL,
        "name": "모음 예",
        "description": "이중모음 ㅖ",
        "rule_reference": "제4절",
        "examples": ["예", "계", "녜"],
        "usage_notes": "ㅕ + ㅣ로 적음"
    },
    {
        "id": "vowel_15",
        "character": "ㅘ",
        "braille_dots": [1, 3, 6, 1, 2, 6],
        "category": BrailleCategory.VOWEL,
        "name": "모음 와",
        "description": "이중모음 ㅘ",
        "rule_reference": "제4절",
        "examples": ["와", "과", "놔"],
        "usage_notes": "ㅗ + ㅏ로 적음"
    },
    {
        "id": "vowel_16",
        "character": "ㅙ",
        "braille_dots": [1, 3, 6, 1, 2, 3, 5],
        "category": BrailleCategory.VOWEL,
        "name": "모음 왜",
        "description": "이중모음 ㅙ",
        "rule_reference": "제4절",
        "examples": ["왜", "괘", "놰"],
        "usage_notes": "ㅗ + ㅐ로 적음"
    },
    {
        "id": "vowel_17",
        "character": "ㅚ",
        "braille_dots": [1, 3, 6, 1, 3, 5],
        "category": BrailleCategory.VOWEL,
        "name": "모음 외",
        "description": "이중모음 ㅚ",
        "rule_reference": "제4절",
        "examples": ["외", "괴", "뇌"],
        "usage_notes": "ㅗ + ㅣ로 적음"
    },
    {
        "id": "vowel_18",
        "character": "ㅝ",
        "braille_dots": [1, 3, 4, 2, 3, 5],
        "category": BrailleCategory.VOWEL,
        "name": "모음 워",
        "description": "이중모음 ㅝ",
        "rule_reference": "제4절",
        "examples": ["워", "궈", "눠"],
        "usage_notes": "ㅜ + ㅓ로 적음"
    },
    {
        "id": "vowel_19",
        "character": "ㅞ",
        "braille_dots": [1, 3, 4, 1, 3, 4, 5],
        "category": BrailleCategory.VOWEL,
        "name": "모음 웨",
        "description": "이중모음 ㅞ",
        "rule_reference": "제4절",
        "examples": ["웨", "궤", "눼"],
        "usage_notes": "ㅜ + ㅔ로 적음"
    },
    {
        "id": "vowel_20",
        "character": "ㅟ",
        "braille_dots": [1, 3, 4, 1, 3, 5],
        "category": BrailleCategory.VOWEL,
        "name": "모음 위",
        "description": "이중모음 ㅟ",
        "rule_reference": "제4절",
        "examples": ["위", "귀", "뉘"],
        "usage_notes": "ㅜ + ㅣ로 적음"
    },
    {
        "id": "vowel_21",
        "character": "ㅢ",
        "braille_dots": [2, 4, 6, 1, 3, 5],
        "category": BrailleCategory.VOWEL,
        "name": "모음 의",
        "description": "이중모음 ㅢ",
        "rule_reference": "제4절",
        "examples": ["의", "희"],
        "usage_notes": "ㅡ + ㅣ로 적음"
    }
]

# 제5절: 모음 연쇄 (Vowel Sequences)
VOWEL_SEQUENCES: List[Dict] = [
    {
        "id": "vowel_seq_01",
        "character": "ㅑㅣ",
        "braille_dots": [3, 4, 5, 1, 3, 5],
        "category": BrailleCategory.VOWEL_SEQUENCE,
        "name": "모음 연쇄 ㅑㅣ",
        "description": "야 + 이 연쇄",
        "rule_reference": "제5절",
        "examples": ["야이", "먀이"],
        "usage_notes": "두 모음을 각각 적음"
    },
    {
        "id": "vowel_seq_02",
        "character": "ㅕㅣ",
        "braille_dots": [1, 3, 4, 6, 1, 3, 5],
        "category": BrailleCategory.VOWEL_SEQUENCE,
        "name": "모음 연쇄 ㅕㅣ",
        "description": "여 + 이 연쇄",
        "rule_reference": "제5절",
        "examples": ["여이", "며이"],
        "usage_notes": "두 모음을 각각 적음"
    },
    {
        "id": "vowel_seq_03",
        "character": "ㅗㅏ",
        "braille_dots": [1, 3, 6, 1, 2, 6],
        "category": BrailleCategory.VOWEL_SEQUENCE,
        "name": "모음 연쇄 ㅗㅏ",
        "description": "오 + 아 연쇄",
        "rule_reference": "제5절",
        "examples": ["오아", "보아"],
        "usage_notes": "두 모음을 각각 적음"
    },
    {
        "id": "vowel_seq_04",
        "character": "ㅗㅐ",
        "braille_dots": [1, 3, 6, 1, 2, 3, 5],
        "category": BrailleCategory.VOWEL_SEQUENCE,
        "name": "모음 연쇄 ㅗㅐ",
        "description": "오 + 애 연쇄",
        "rule_reference": "제5절",
        "examples": ["오애", "보애"],
        "usage_notes": "두 모음을 각각 적음"
    },
    {
        "id": "vowel_seq_05",
        "character": "ㅜㅓ",
        "braille_dots": [1, 3, 4, 2, 3, 5],
        "category": BrailleCategory.VOWEL_SEQUENCE,
        "name": "모음 연쇄 ㅜㅓ",
        "description": "우 + 어 연쇄",
        "rule_reference": "제5절",
        "examples": ["우어", "구어"],
        "usage_notes": "두 모음을 각각 적음"
    },
    {
        "id": "vowel_seq_06",
        "character": "ㅜㅔ",
        "braille_dots": [1, 3, 4, 1, 3, 4, 5],
        "category": BrailleCategory.VOWEL_SEQUENCE,
        "name": "모음 연쇄 ㅜㅔ",
        "description": "우 + 에 연쇄",
        "rule_reference": "제5절",
        "examples": ["우에", "구에"],
        "usage_notes": "두 모음을 각각 적음"
    },
    {
        "id": "vowel_seq_07",
        "character": "ㅜㅣ",
        "braille_dots": [1, 3, 4, 1, 3, 5],
        "category": BrailleCategory.VOWEL_SEQUENCE,
        "name": "모음 연쇄 ㅜㅣ",
        "description": "우 + 이 연쇄",
        "rule_reference": "제5절",
        "examples": ["우이", "구이"],
        "usage_notes": "두 모음을 각각 적음"
    },
    {
        "id": "vowel_seq_08",
        "character": "ㅡㅣ",
        "braille_dots": [2, 4, 6, 1, 3, 5],
        "category": BrailleCategory.VOWEL_SEQUENCE,
        "name": "모음 연쇄 ㅡㅣ",
        "description": "으 + 이 연쇄",
        "rule_reference": "제5절",
        "examples": ["으이", "그이"],
        "usage_notes": "두 모음을 각각 적음"
    }
]

# 숫자 (Numbers)
NUMBERS: List[Dict] = [
    {
        "id": "number_prefix",
        "character": "#",
        "braille_dots": [3, 4, 5, 6],
        "category": BrailleCategory.PREFIX,
        "name": "수표",
        "description": "숫자 시작을 나타내는 표시",
        "rule_reference": "제3장 수학 및 과학",
        "usage_notes": "숫자 앞에 붙여 숫자임을 표시"
    },
    {
        "id": "number_01",
        "character": "1",
        "braille_dots": [1],
        "category": BrailleCategory.NUMBER,
        "name": "숫자 1",
        "description": "숫자 일",
        "rule_reference": "제3장",
        "examples": ["#1"],
        "usage_notes": "수표 뒤에 사용"
    },
    {
        "id": "number_02",
        "character": "2",
        "braille_dots": [1, 2],
        "category": BrailleCategory.NUMBER,
        "name": "숫자 2",
        "description": "숫자 이",
        "rule_reference": "제3장",
        "examples": ["#2"],
        "usage_notes": "수표 뒤에 사용"
    },
    {
        "id": "number_03",
        "character": "3",
        "braille_dots": [1, 4],
        "category": BrailleCategory.NUMBER,
        "name": "숫자 3",
        "description": "숫자 삼",
        "rule_reference": "제3장",
        "examples": ["#3"],
        "usage_notes": "수표 뒤에 사용"
    },
    {
        "id": "number_04",
        "character": "4",
        "braille_dots": [1, 4, 5],
        "category": BrailleCategory.NUMBER,
        "name": "숫자 4",
        "description": "숫자 사",
        "rule_reference": "제3장",
        "examples": ["#4"],
        "usage_notes": "수표 뒤에 사용"
    },
    {
        "id": "number_05",
        "character": "5",
        "braille_dots": [1, 5],
        "category": BrailleCategory.NUMBER,
        "name": "숫자 5",
        "description": "숫자 오",
        "rule_reference": "제3장",
        "examples": ["#5"],
        "usage_notes": "수표 뒤에 사용"
    },
    {
        "id": "number_06",
        "character": "6",
        "braille_dots": [1, 2, 4],
        "category": BrailleCategory.NUMBER,
        "name": "숫자 6",
        "description": "숫자 육",
        "rule_reference": "제3장",
        "examples": ["#6"],
        "usage_notes": "수표 뒤에 사용"
    },
    {
        "id": "number_07",
        "character": "7",
        "braille_dots": [1, 2, 4, 5],
        "category": BrailleCategory.NUMBER,
        "name": "숫자 7",
        "description": "숫자 칠",
        "rule_reference": "제3장",
        "examples": ["#7"],
        "usage_notes": "수표 뒤에 사용"
    },
    {
        "id": "number_08",
        "character": "8",
        "braille_dots": [1, 2, 5],
        "category": BrailleCategory.NUMBER,
        "name": "숫자 8",
        "description": "숫자 팔",
        "rule_reference": "제3장",
        "examples": ["#8"],
        "usage_notes": "수표 뒤에 사용"
    },
    {
        "id": "number_09",
        "character": "9",
        "braille_dots": [2, 4],
        "category": BrailleCategory.NUMBER,
        "name": "숫자 9",
        "description": "숫자 구",
        "rule_reference": "제3장",
        "examples": ["#9"],
        "usage_notes": "수표 뒤에 사용"
    },
    {
        "id": "number_00",
        "character": "0",
        "braille_dots": [2, 4, 5],
        "category": BrailleCategory.NUMBER,
        "name": "숫자 0",
        "description": "숫자 영",
        "rule_reference": "제3장",
        "examples": ["#0"],
        "usage_notes": "수표 뒤에 사용"
    }
]

# 기본 문장부호 (Punctuation)
PUNCTUATION: List[Dict] = [
    {
        "id": "punct_01",
        "character": ".",
        "braille_dots": [2, 5, 6],
        "category": BrailleCategory.PUNCTUATION,
        "name": "마침표",
        "description": "문장의 끝",
        "rule_reference": "제2장 문장부호",
        "examples": ["안녕."]
    },
    {
        "id": "punct_02",
        "character": ",",
        "braille_dots": [5],
        "category": BrailleCategory.PUNCTUATION,
        "name": "쉼표",
        "description": "문장 내 쉼",
        "rule_reference": "제2장 문장부호",
        "examples": ["가, 나, 다"]
    },
    {
        "id": "punct_03",
        "character": "?",
        "braille_dots": [2, 3, 6],
        "category": BrailleCategory.PUNCTUATION,
        "name": "물음표",
        "description": "의문문의 끝",
        "rule_reference": "제2장 문장부호",
        "examples": ["왜?"]
    },
    {
        "id": "punct_04",
        "character": "!",
        "braille_dots": [2, 3, 5],
        "category": BrailleCategory.PUNCTUATION,
        "name": "느낌표",
        "description": "감탄문의 끝",
        "rule_reference": "제2장 문장부호",
        "examples": ["와!"]
    },
    {
        "id": "punct_05",
        "character": ":",
        "braille_dots": [5, 2],
        "category": BrailleCategory.PUNCTUATION,
        "name": "쌍점",
        "description": "설명이나 열거",
        "rule_reference": "제2장 문장부호",
        "examples": ["시간: 3시"]
    },
    {
        "id": "punct_06",
        "character": ";",
        "braille_dots": [5, 6],
        "category": BrailleCategory.PUNCTUATION,
        "name": "쌍반점",
        "description": "문장 구분",
        "rule_reference": "제2장 문장부호",
        "examples": ["가; 나"]
    },
    {
        "id": "punct_07",
        "character": "-",
        "braille_dots": [3, 6],
        "category": BrailleCategory.PUNCTUATION,
        "name": "붙임표",
        "description": "단어 연결",
        "rule_reference": "제2장 문장부호",
        "examples": ["서울-부산"]
    },
    {
        "id": "punct_08",
        "character": " ",
        "braille_dots": [],
        "category": BrailleCategory.SPECIAL,
        "name": "띄어쓰기",
        "description": "단어 사이 공백",
        "rule_reference": "제1장",
        "usage_notes": "한 칸 띄움"
    }
]

# 모든 점자 데이터 통합
ALL_BRAILLE_DATA = (
    INITIAL_CONSONANTS +
    FINAL_CONSONANTS +
    VOWELS +
    VOWEL_SEQUENCES +
    NUMBERS +
    PUNCTUATION
)


def get_all_braille_characters() -> List[BrailleCharacter]:
    """모든 점자 문자 반환"""
    return [BrailleCharacter(**char) for char in ALL_BRAILLE_DATA]


def get_braille_by_category(category: BrailleCategory) -> List[BrailleCharacter]:
    """카테고리별 점자 문자 반환"""
    filtered = [char for char in ALL_BRAILLE_DATA if char["category"] == category]
    return [BrailleCharacter(**char) for char in filtered]


def search_braille(query: str) -> List[BrailleCharacter]:
    """점자 검색 (문자 또는 이름)"""
    query_lower = query.lower()
    filtered = [
        char for char in ALL_BRAILLE_DATA
        if query_lower in char["character"].lower() or
           query_lower in char["name"].lower()
    ]
    return [BrailleCharacter(**char) for char in filtered]


def get_available_categories() -> List[str]:
    """사용 가능한 카테고리 목록 반환"""
    return [category.value for category in BrailleCategory]
