#!/usr/bin/env python3
"""Test the chat endpoint"""
import requests
import json

url = "http://127.0.0.1:8000/chat"
payload = {
    "content": "hello",
    "user_id": "test"
}

try:
    response = requests.post(url, json=payload, timeout=10)
    response.raise_for_status()
    data = response.json()
    
    print("✅ Chat endpoint response:")
    print(f"\nResponse text:\n{data.get('response', 'NO RESPONSE')[:300]}")
    print(f"\nHealthcare mode: {data.get('healthcare_mode', False)}")
    print(f"\nDetected symptoms: {data.get('detected_symptoms', [])}")
    
except Exception as e:
    print(f"❌ Error: {e}")
