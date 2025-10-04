#!/usr/bin/env python3
"""
Simple test script for the Document Chat API
"""

import requests
import json
import time

# API Configuration
BASE_URL = "http://localhost:8080"
CHAT_ENDPOINT = f"{BASE_URL}/api/chat/message"

def test_message(message):
    """Test a single message"""
    try:
        payload = {"message": message}
        response = requests.post(CHAT_ENDPOINT, json=payload, timeout=10)
        print(f"Question: {message}")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {data.get('response', 'No response')}")
            print(f"Source: {data.get('source', 'Unknown')}")
        else:
            print(f"Error: {response.text}")
        print("-" * 50)
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        print("-" * 50)
        return False

def main():
    print("🧪 Testing Document Chat API")
    print("=" * 50)
    
    # Test cases
    test_cases = [
        # Positive cases
        "How many interviews are there in the Google interview process?",
        "What are the four focus areas?",
        "What data structures should I know?",
        "What programming languages are mentioned?",
        "What are the common pitfalls to avoid?",
        
        # Negative cases
        "What is the weather today?",
        "How do I cook pasta?",
        "",
        "asdfghjkl",
        
        # Edge cases
        "interview",
        "coding",
        "INTERVIEW PROCESS?",
        "How many interveiws are there?",  # typo
    ]
    
    results = []
    for i, question in enumerate(test_cases, 1):
        print(f"Test {i}:")
        success = test_message(question)
        results.append(success)
        time.sleep(1)  # Rate limiting
    
    print(f"\nSummary: {sum(results)}/{len(results)} tests passed")

if __name__ == "__main__":
    main()
