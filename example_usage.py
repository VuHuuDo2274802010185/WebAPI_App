#!/usr/bin/env python3
"""
Ví dụ sử dụng Web API
Chạy api_server.py trước khi chạy script này
"""

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Cấu hình API
API_BASE_URL = "http://localhost:8000"
ACCESS_TOKEN = os.getenv("BASE_TOKEN", "")
OPENING_ID = os.getenv("OPENING_ID", "9346")
STAGE_ID = os.getenv("STAGE_ID", "75440")


def test_health_check():
    """Test health check endpoint"""
    print("=" * 60)
    print("1. Testing Health Check Endpoint")
    print("=" * 60)
    
    response = requests.get(f"{API_BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()


def test_get_candidates_post():
    """Test GET candidates với POST method"""
    print("=" * 60)
    print("2. Testing GET Candidates (POST method)")
    print("=" * 60)
    
    if not ACCESS_TOKEN:
        print("⚠️  WARNING: BASE_TOKEN not found in .env file")
        print("Please add your Base.vn access token to .env file")
        print()
        return
    
    # Payload
    payload = {
        "access_token": ACCESS_TOKEN,
        "opening_id": OPENING_ID,
        "stage": STAGE_ID,
        "page": 1,
        "num_per_page": 5  # Chỉ lấy 5 kết quả để demo
    }
    
    print(f"Request Payload:")
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    print()
    
    response = requests.post(
        f"{API_BASE_URL}/api/v1/candidates",
        json=payload
    )
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            print(f"✅ Success! Found {data['data']['count']} candidates")
            print(f"\nMetrics:")
            print(f"  - Total: {data['data']['metrics']['total']}")
            print(f"  - Count: {data['data']['metrics']['count']}")
            print(f"  - Page: {data['data']['metrics']['page']}")
            
            print(f"\nCandidates:")
            for i, candidate in enumerate(data['data']['candidates'][:3], 1):
                print(f"  {i}. {candidate.get('Họ & Tên', 'N/A')}")
                print(f"     Email: {candidate.get('Email', 'N/A')}")
                print(f"     Position: {candidate.get('Vị trí ứng tuyển', 'N/A')}")
        else:
            print(f"❌ Error: {data.get('message')}")
    else:
        print(f"❌ Request failed")
        print(f"Response: {response.text}")
    print()


def test_get_candidates_get():
    """Test GET candidates với GET method"""
    print("=" * 60)
    print("3. Testing GET Candidates (GET method with query params)")
    print("=" * 60)
    
    if not ACCESS_TOKEN:
        print("⚠️  WARNING: BASE_TOKEN not found in .env file")
        print()
        return
    
    # Query parameters
    params = {
        "access_token": ACCESS_TOKEN,
        "opening_id": OPENING_ID,
        "stage": STAGE_ID,
        "page": 1,
        "num_per_page": 3  # Chỉ lấy 3 kết quả để demo
    }
    
    response = requests.get(
        f"{API_BASE_URL}/api/v1/candidates",
        params=params
    )
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            print(f"✅ Success! Found {data['data']['count']} candidates")
        else:
            print(f"❌ Error: {data.get('message')}")
    else:
        print(f"❌ Request failed")
    print()


def main():
    """Main function"""
    print("\n")
    print("🚀 Base.vn Candidate API - Example Usage")
    print("=" * 60)
    print(f"API Base URL: {API_BASE_URL}")
    print(f"Opening ID: {OPENING_ID}")
    print(f"Stage ID: {STAGE_ID}")
    print()
    
    # Test các endpoints
    try:
        test_health_check()
        test_get_candidates_post()
        test_get_candidates_get()
        
        print("=" * 60)
        print("✅ All tests completed!")
        print("=" * 60)
        print()
        print("📚 For interactive API documentation, visit:")
        print(f"   - Swagger UI: {API_BASE_URL}/docs")
        print(f"   - ReDoc: {API_BASE_URL}/redoc")
        print()
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to API server")
        print("Make sure api_server.py is running:")
        print("  python api_server.py")
        print()


if __name__ == "__main__":
    main()
