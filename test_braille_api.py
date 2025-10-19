"""
Test script for Braille Library API
Quick verification of all endpoints
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1/braille"

def print_result(title, response):
    """Print formatted API response"""
    print("\n" + "="*60)
    print(f"📌 {title}")
    print("="*60)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print(f"Error: {response.text}")
    print()


def test_braille_library():
    """Test all Braille Library API endpoints"""
    
    print("\n🎯 Testing Braille Library API")
    print("="*60)
    
    # Test 1: Get all categories
    print("\n✅ Test 1: Get all categories")
    response = requests.get(f"{BASE_URL}/library/categories")
    print_result("Categories", response)
    
    # Test 2: Get all braille characters
    print("\n✅ Test 2: Get all braille characters (first 3)")
    response = requests.get(f"{BASE_URL}/library")
    if response.status_code == 200:
        data = response.json()
        print(f"Total count: {data['total_count']}")
        print(f"First 3 characters:")
        for char in data['characters'][:3]:
            print(f"  - {char['character']} ({char['name']}): {char['braille_dots']}")
    
    # Test 3: Filter by category - Initial Consonants
    print("\n✅ Test 3: Get initial consonants (초성)")
    response = requests.get(f"{BASE_URL}/library?category=consonant_initial")
    if response.status_code == 200:
        data = response.json()
        print(f"Found {data['total_count']} initial consonants")
        for char in data['characters'][:5]:
            print(f"  - {char['character']} ({char['name']}): {char['braille_dots']}")
    
    # Test 4: Filter by category - Vowels
    print("\n✅ Test 4: Get vowels (모음)")
    response = requests.get(f"{BASE_URL}/library?category=vowel")
    if response.status_code == 200:
        data = response.json()
        print(f"Found {data['total_count']} vowels")
        for char in data['characters'][:5]:
            print(f"  - {char['character']} ({char['name']}): {char['braille_dots']}")
    
    # Test 5: Filter by category - Numbers
    print("\n✅ Test 5: Get numbers (숫자)")
    response = requests.get(f"{BASE_URL}/library?category=number")
    if response.status_code == 200:
        data = response.json()
        print(f"Found {data['total_count']} numbers")
        for char in data['characters']:
            print(f"  - {char['character']} ({char['name']}): {char['braille_dots']}")
    
    # Test 6: Search by character
    print("\n✅ Test 6: Search for 'ㄱ'")
    response = requests.get(f"{BASE_URL}/library?search=ㄱ")
    if response.status_code == 200:
        data = response.json()
        print(f"Found {data['total_count']} results for 'ㄱ'")
        for char in data['characters']:
            print(f"  - {char['character']} ({char['name']}) [{char['category']}]: {char['braille_dots']}")
    
    # Test 7: Search by name
    print("\n✅ Test 7: Search for '기역'")
    response = requests.get(f"{BASE_URL}/library?search=기역")
    if response.status_code == 200:
        data = response.json()
        print(f"Found {data['total_count']} results for '기역'")
        for char in data['characters']:
            print(f"  - {char['character']} ({char['name']}) [{char['category']}]: {char['braille_dots']}")
    
    # Test 8: Get specific character by ID
    print("\n✅ Test 8: Get character by ID (cons_initial_01)")
    response = requests.get(f"{BASE_URL}/library/cons_initial_01")
    print_result("Character Details", response)
    
    # Test 9: Get category endpoint - vowels
    print("\n✅ Test 9: Get vowels using category endpoint")
    response = requests.get(f"{BASE_URL}/library/category/vowel")
    if response.status_code == 200:
        data = response.json()
        print(f"Found {data['total_count']} vowels")
        for char in data['characters'][:5]:
            print(f"  - {char['character']} ({char['name']}): {char['braille_dots']}")
    
    # Test 10: Search endpoint
    print("\n✅ Test 10: Search endpoint for '모음'")
    response = requests.get(f"{BASE_URL}/library/search/모음")
    if response.status_code == 200:
        data = response.json()
        print(f"Found {data['total_count']} results for '모음'")
        for char in data['characters'][:5]:
            print(f"  - {char['character']} ({char['name']}): {char['braille_dots']}")
    
    # Test 11: Combined filter - vowel + search
    print("\n✅ Test 11: Combined filter (vowel category + search 'ㅏ')")
    response = requests.get(f"{BASE_URL}/library?category=vowel&search=ㅏ")
    if response.status_code == 200:
        data = response.json()
        print(f"Found {data['total_count']} vowels containing 'ㅏ'")
        for char in data['characters']:
            print(f"  - {char['character']} ({char['name']}): {char['braille_dots']}")
    
    # Test 12: Text conversion endpoint
    print("\n✅ Test 12: Text conversion endpoint")
    response = requests.get(f"{BASE_URL}/convert/안녕")
    print_result("Conversion Info", response)
    
    print("\n" + "="*60)
    print("🎉 All tests completed!")
    print("="*60)


if __name__ == "__main__":
    try:
        test_braille_library()
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Cannot connect to the API server.")
        print("Make sure the FastAPI server is running:")
        print("  uvicorn main:app --reload")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
