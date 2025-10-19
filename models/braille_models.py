"""
Braille Library Models
Based on 2020 한글점자규정 (Korean Braille Standard)
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class BrailleCategory(str, Enum):
    """Braille character categories"""
    CONSONANT_INITIAL = "consonant_initial"  # 초성 (Initial consonants)
    CONSONANT_FINAL = "consonant_final"  # 종성 (Final consonants)
    VOWEL = "vowel"  # 모음
    VOWEL_SEQUENCE = "vowel_sequence"  # 모음 연쇄
    NUMBER = "number"  # 숫자
    PUNCTUATION = "punctuation"  # 문장부호
    SPECIAL = "special"  # 특수기호
    PREFIX = "prefix"  # 접두어 (숫자표, 대문자표 등)


class BrailleCharacter(BaseModel):
    """Individual braille character entry"""
    id: str = Field(..., description="고유 식별자")
    character: str = Field(..., description="한글 문자 또는 기호")
    braille_dots: List[int] = Field(
        ..., 
        description="점자 점 번호 (1-6)",
        example=[1, 4]
    )
    category: BrailleCategory = Field(..., description="점자 분류")
    name: str = Field(..., description="문자 이름 (예: 기역, 니은)")
    description: Optional[str] = Field(None, description="설명")
    usage_notes: Optional[str] = Field(None, description="사용법 설명")
    rule_reference: Optional[str] = Field(None, description="규정 참조 (예: 제1절)")
    examples: Optional[List[str]] = Field(default_factory=list, description="사용 예시")


class BrailleLibraryResponse(BaseModel):
    """Response model for braille library"""
    total_count: int = Field(..., description="전체 항목 수")
    categories: List[str] = Field(..., description="사용 가능한 카테고리 목록")
    characters: List[BrailleCharacter] = Field(..., description="점자 문자 목록")


class BrailleCategoryFilter(BaseModel):
    """Filter parameters for braille library"""
    category: Optional[BrailleCategory] = Field(None, description="카테고리 필터")
    search: Optional[str] = Field(None, description="검색어 (문자 또는 이름)")
