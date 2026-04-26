"""
API Integration Tests
"""
import httpx
import asyncio
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000"

async def test_health():
    """Test health endpoint"""
    print("Testing /health endpoint...")
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

async def test_chat():
    """Test chat endpoint"""
    print("Testing /chat endpoint...")
    payload = {
        "content": "I have a fever and cough",
        "user_id": "test_user_123"
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/chat", json=payload)
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2, default=str)}")
    print()

async def test_feedback():
    """Test feedback endpoint"""
    print("Testing /feedback endpoint...")
    payload = {
        "message_id": "test_message_123",
        "is_helpful": True,
        "category": "general",
        "comment": "This was helpful"
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/feedback", json=payload)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

async def test_insights():
    """Test insights endpoint"""
    print("Testing /insights endpoint...")
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/insights")
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2, default=str)}")
    print()

async def test_security():
    """Test security status endpoint"""
    print("Testing /security/status endpoint...")
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/security/status")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

async def main():
    """Run all tests"""
    print("=" * 60)
    print("API Integration Tests")
    print("=" * 60)
    print()
    
    try:
        await test_health()
        await test_chat()
        await test_feedback()
        await test_insights()
        await test_security()
        print("✓ All tests completed!")
        
    except Exception as e:
        print(f"✗ Test failed: {str(e)}")
        print("\nMake sure backend is running: python -m uvicorn app.main:app --reload")

if __name__ == "__main__":
    asyncio.run(main())
