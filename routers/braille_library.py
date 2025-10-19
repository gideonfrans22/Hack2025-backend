"""
Braille Library Router
API endpoints for accessing Korean Braille character library
"""
from fastapi import APIRouter, Query, HTTPException
from typing import Optional, List
from models.braille_models import (
    BrailleCharacter,
    BrailleLibraryResponse,
    BrailleCategory
)
from data.braille_library import (
    get_all_braille_characters,
    get_braille_by_category,
    search_braille,
    get_available_categories
)

router = APIRouter(
    prefix="/api/v1/braille",
    tags=["braille_library"]
)


@router.get(
    "/library",
    response_model=BrailleLibraryResponse,
    summary="점자 도서관 조회",
    description="한글 점자 문자 도서관 조회. 카테고리 필터링 및 검색 기능 제공"
)
async def get_braille_library(
    category: Optional[BrailleCategory] = Query(
        None,
        description="카테고리 필터 (consonant_initial, consonant_final, vowel, vowel_sequence, number, punctuation, special, prefix)"
    ),
    search: Optional[str] = Query(
        None,
        description="검색어 (문자 또는 이름으로 검색)",
        min_length=1
    )
) -> BrailleLibraryResponse:
    """
    점자 도서관 조회
    
    - **category**: 특정 카테고리만 조회 (선택사항)
    - **search**: 문자 또는 이름으로 검색 (선택사항)
    - 필터 없이 호출하면 전체 점자 문자 반환
    """
    try:
        # 검색어가 있는 경우
        if search:
            characters = search_braille(search)
            
            # 카테고리 필터도 적용
            if category:
                characters = [char for char in characters if char.category == category]
        
        # 카테고리 필터만 있는 경우
        elif category:
            characters = get_braille_by_category(category)
        
        # 필터 없이 전체 조회
        else:
            characters = get_all_braille_characters()
        
        return BrailleLibraryResponse(
            total_count=len(characters),
            categories=get_available_categories(),
            characters=characters
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"점자 도서관 조회 중 오류가 발생했습니다: {str(e)}"
        )


@router.get(
    "/library/categories",
    response_model=List[str],
    summary="점자 카테고리 목록",
    description="사용 가능한 점자 카테고리 목록 조회"
)
async def get_categories() -> List[str]:
    """
    점자 카테고리 목록 조회
    
    반환되는 카테고리:
    - consonant_initial: 초성 (자음)
    - consonant_final: 종성 (받침)
    - vowel: 모음
    - vowel_sequence: 모음 연쇄
    - number: 숫자
    - punctuation: 문장부호
    - special: 특수기호
    - prefix: 접두어 (수표 등)
    """
    try:
        return get_available_categories()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"카테고리 목록 조회 중 오류가 발생했습니다: {str(e)}"
        )


@router.get(
    "/library/{character_id}",
    response_model=BrailleCharacter,
    summary="점자 문자 상세 조회",
    description="특정 점자 문자의 상세 정보 조회"
)
async def get_braille_character(character_id: str) -> BrailleCharacter:
    """
    점자 문자 상세 조회
    
    - **character_id**: 점자 문자 고유 ID (예: cons_initial_01, vowel_01)
    """
    try:
        all_characters = get_all_braille_characters()
        
        # ID로 검색
        character = next(
            (char for char in all_characters if char.id == character_id),
            None
        )
        
        if not character:
            raise HTTPException(
                status_code=404,
                detail=f"ID '{character_id}'에 해당하는 점자 문자를 찾을 수 없습니다."
            )
        
        return character
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"점자 문자 조회 중 오류가 발생했습니다: {str(e)}"
        )


@router.get(
    "/library/category/{category_name}",
    response_model=BrailleLibraryResponse,
    summary="카테고리별 점자 조회",
    description="특정 카테고리의 점자 문자 목록 조회"
)
async def get_braille_by_category_name(
    category_name: BrailleCategory
) -> BrailleLibraryResponse:
    """
    카테고리별 점자 조회
    
    - **category_name**: 카테고리 이름
      - consonant_initial: 초성
      - consonant_final: 종성
      - vowel: 모음
      - vowel_sequence: 모음 연쇄
      - number: 숫자
      - punctuation: 문장부호
      - special: 특수기호
      - prefix: 접두어
    """
    try:
        characters = get_braille_by_category(category_name)
        
        return BrailleLibraryResponse(
            total_count=len(characters),
            categories=get_available_categories(),
            characters=characters
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"카테고리 '{category_name}' 조회 중 오류가 발생했습니다: {str(e)}"
        )


@router.get(
    "/library/search/{query}",
    response_model=BrailleLibraryResponse,
    summary="점자 검색",
    description="문자 또는 이름으로 점자 검색"
)
async def search_braille_characters(query: str) -> BrailleLibraryResponse:
    """
    점자 검색
    
    - **query**: 검색어 (문자 또는 이름)
    
    예시:
    - "ㄱ" → 기역 관련 점자 검색
    - "기역" → 기역이 포함된 점자 검색
    - "받침" → 받침이 포함된 점자 검색
    """
    try:
        if not query or len(query.strip()) == 0:
            raise HTTPException(
                status_code=400,
                detail="검색어를 입력해주세요."
            )
        
        characters = search_braille(query.strip())
        
        return BrailleLibraryResponse(
            total_count=len(characters),
            categories=get_available_categories(),
            characters=characters
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"점자 검색 중 오류가 발생했습니다: {str(e)}"
        )


@router.get(
    "/convert/{text}",
    summary="텍스트를 점자로 변환 (미리보기)",
    description="한글 텍스트를 점자 점 배열로 변환 (기본 변환만 지원)"
)
async def convert_text_to_braille(text: str):
    """
    텍스트를 점자로 변환 (기본 변환)
    
    ⚠️ 주의: 이 엔드포인트는 기본적인 문자 대 문자 매핑만 수행합니다.
    실제 한글 점자는 복잡한 규칙이 있으므로, 완전한 변환을 위해서는
    별도의 점자 변환 라이브러리를 사용해야 합니다.
    
    - **text**: 변환할 한글 텍스트
    """
    try:
        if not text or len(text.strip()) == 0:
            raise HTTPException(
                status_code=400,
                detail="변환할 텍스트를 입력해주세요."
            )
        
        # 간단한 예시 응답 (실제 변환 로직은 별도 구현 필요)
        return {
            "original_text": text,
            "notice": "이 기능은 기본 미리보기입니다. 완전한 점자 변환은 별도 라이브러리가 필요합니다.",
            "suggestion": "점자 도서관 API를 사용하여 개별 문자의 점자 표현을 확인하세요.",
            "library_endpoint": "/api/v1/braille/library"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"텍스트 변환 중 오류가 발생했습니다: {str(e)}"
        )
