#!/usr/bin/env python3
"""Test the chat endpoint with health question"""
import requests
import json

url = "http://127.0.0.1:8000/chat"
payload = {
    "content": "I have a fever and cough",
    "user_id": "test"
}

try:
    response = requests.post(url, json=payload, timeout=15)
    response.raise_for_status()
    data = response.json()
    
    print("✅ Chat endpoint response:")
    print(f"\nResponse (first 500 chars):\n{data.get('response', 'NO RESPONSE')[:500]}")
    print(f"\nHealthcare mode: {data.get('healthcare_mode', False)}")
    print(f"\nDetected symptoms: {data.get('detected_symptoms', [])}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
