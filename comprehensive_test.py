#!/usr/bin/env python3
"""
Comprehensive test script for the Document Chat API with document upload
"""

import requests
import json
import time
import os

# API Configuration
BASE_URL = "http://localhost:8080"
CHAT_ENDPOINT = f"{BASE_URL}/api/chat/message"
DOCUMENTS_ENDPOINT = f"{BASE_URL}/api/documents"
UPLOAD_ENDPOINT = f"{BASE_URL}/api/documents/upload"

def upload_document():
    """Upload the Google interview guide document"""
    try:
        # Check if document already exists
        response = requests.get(DOCUMENTS_ENDPOINT)
        if response.status_code == 200 and response.json():
            print("✅ Document already uploaded")
            return True
            
        # Upload the document
        pdf_path = "/Users/prashant/Downloads/CodeBase/LLM PROJECT/InterviewGuideAtGoogle.pdf"
        if not os.path.exists(pdf_path):
            print(f"❌ PDF file not found at {pdf_path}")
            return False
            
        with open(pdf_path, 'rb') as f:
            files = {'file': ('InterviewGuideAtGoogle.pdf', f, 'application/pdf')}
            response = requests.post(UPLOAD_ENDPOINT, files=files, timeout=30)
            
        if response.status_code == 200:
            print("✅ Document uploaded successfully")
            return True
        else:
            print(f"❌ Failed to upload document: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error uploading document: {e}")
        return False

def test_message(message, expected_keywords=None, should_be_out_of_scope=False):
    """Test a single message"""
    try:
        payload = {"message": message}
        response = requests.post(CHAT_ENDPOINT, json=payload, timeout=10)
        
        print(f"Question: {message}")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            response_text = data.get('response', 'No response')
            source = data.get('source', 'Unknown')
            
            print(f"Response: {response_text}")
            print(f"Source: {source}")
            
            # Validate response
            if should_be_out_of_scope:
                if "out of scope" in response_text.lower():
                    print("✅ Correctly identified as out of scope")
                    return True
                else:
                    print("❌ Should be out of scope but wasn't")
                    return False
            else:
                if expected_keywords:
                    found_keywords = sum(1 for keyword in expected_keywords if keyword.lower() in response_text.lower())
                    if found_keywords > 0:
                        print(f"✅ Found {found_keywords}/{len(expected_keywords)} expected keywords")
                        return True
                    else:
                        print(f"❌ Missing expected keywords: {expected_keywords}")
                        return False
                else:
                    print("✅ Response received")
                    return True
        else:
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        print("-" * 60)

def main():
    print("🧪 Comprehensive Document Chat API Testing")
    print("=" * 60)
    
    # Upload document first
    print("📄 Uploading document...")
    if not upload_document():
        print("❌ Cannot proceed without document")
        return
    
    print("\n🧪 Running comprehensive tests...")
    
    # Test cases with expected results
    test_cases = [
        # Positive cases - should find relevant information
        {
            "question": "How many interviews are there in the Google interview process?",
            "expected_keywords": ["5", "five", "interview"],
            "should_be_out_of_scope": False
        },
        {
            "question": "What are the four focus areas?",
            "expected_keywords": ["coding", "programming", "design", "integration", "leadership"],
            "should_be_out_of_scope": False
        },
        {
            "question": "What data structures should I know?",
            "expected_keywords": ["array", "tree", "hashtable", "linked list"],
            "should_be_out_of_scope": False
        },
        {
            "question": "What programming languages are mentioned?",
            "expected_keywords": ["java", "python"],
            "should_be_out_of_scope": False
        },
        {
            "question": "What are the common pitfalls to avoid?",
            "expected_keywords": ["jumping", "design", "coding", "talking", "hints"],
            "should_be_out_of_scope": False
        },
        {
            "question": "How long are the interviews?",
            "expected_keywords": ["45", "60", "minute"],
            "should_be_out_of_scope": False
        },
        {
            "question": "What platform is used for interviews?",
            "expected_keywords": ["google", "hangouts"],
            "should_be_out_of_scope": False
        },
        
        # Negative cases - should be out of scope
        {
            "question": "What is the weather today?",
            "expected_keywords": None,
            "should_be_out_of_scope": True
        },
        {
            "question": "How do I cook pasta?",
            "expected_keywords": None,
            "should_be_out_of_scope": True
        },
        {
            "question": "What is the capital of France?",
            "expected_keywords": None,
            "should_be_out_of_scope": True
        },
        {
            "question": "Tell me about quantum physics",
            "expected_keywords": None,
            "should_be_out_of_scope": True
        },
        {
            "question": "",
            "expected_keywords": None,
            "should_be_out_of_scope": True
        },
        {
            "question": "asdfghjkl",
            "expected_keywords": None,
            "should_be_out_of_scope": True
        },
        {
            "question": "What are the salary ranges at Google?",
            "expected_keywords": None,
            "should_be_out_of_scope": True
        },
        
        # Edge cases
        {
            "question": "interview",
            "expected_keywords": ["interview"],
            "should_be_out_of_scope": False
        },
        {
            "question": "INTERVIEW PROCESS?",
            "expected_keywords": ["interview"],
            "should_be_out_of_scope": False
        },
        {
            "question": "How many interveiws are there?",  # typo
            "expected_keywords": ["5", "five", "interview"],
            "should_be_out_of_scope": False
        }
    ]
    
    results = []
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test {i}:")
        success = test_message(
            test_case["question"], 
            test_case["expected_keywords"], 
            test_case["should_be_out_of_scope"]
        )
        results.append(success)
        time.sleep(1)  # Rate limiting
    
    # Summary
    passed = sum(results)
    total = len(results)
    print(f"\n📊 TEST SUMMARY")
    print("=" * 60)
    print(f"Total Tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    
    # Detailed analysis
    positive_tests = [i for i, tc in enumerate(test_cases) if not tc["should_be_out_of_scope"]]
    negative_tests = [i for i, tc in enumerate(test_cases) if tc["should_be_out_of_scope"]]
    
    positive_passed = sum(results[i] for i in positive_tests)
    negative_passed = sum(results[i] for i in negative_tests)
    
    print(f"\nPositive Tests: {positive_passed}/{len(positive_tests)} passed")
    print(f"Negative Tests: {negative_passed}/{len(negative_tests)} passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! The API is working correctly.")
    else:
        print(f"\n⚠️  {total - passed} tests failed. Review the issues above.")

if __name__ == "__main__":
    main()
