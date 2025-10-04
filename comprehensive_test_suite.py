#!/usr/bin/env python3

import requests
import json
import time

BASE_URL = "http://localhost:8080/api"
DOCUMENTS_ENDPOINT = f"{BASE_URL}/documents"
CHAT_ENDPOINT = f"{BASE_URL}/chat/message"
DOCUMENT_PATH = "/Users/prashant/Downloads/CodeBase/LLM PROJECT/InterviewGuideAtGoogle.pdf"

def upload_document():
    print("📄 Uploading document...")
    with open(DOCUMENT_PATH, 'rb') as f:
        files = {'file': (DOCUMENT_PATH.split('/')[-1], f, 'application/pdf')}
        try:
            response = requests.post(f"{DOCUMENTS_ENDPOINT}/upload", files=files)
            response.raise_for_status()
            print("✅ Document uploaded successfully")
            return response.json()
        except requests.exceptions.RequestException as e:
            if response.status_code == 409:  # Conflict, document already exists
                print("✅ Document already uploaded")
                return {"message": "Document already exists"}
            print(f"❌ Error uploading document: {e}")
            return None

def send_chat_message(question):
    payload = {"message": question}
    try:
        response = requests.post(CHAT_ENDPOINT, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError as e:
        print(f"❌ Cannot connect to server: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Error sending chat message: {e}")
        return None

def run_comprehensive_tests():
    print("🧪 Running Comprehensive Test Suite...")
    print("=" * 80)
    
    # Upload document first
    upload_document()
    time.sleep(3)  # Give time for processing
    
    # 50 POSITIVE TEST CASES (should return document-based answers)
    positive_tests = [
        # Interview count questions
        {"question": "How many interviews are there?", "expected_keywords": ["5", "total", "interviews"]},
        {"question": "How many interview rounds I have to give?", "expected_keywords": ["5", "total", "interviews"]},
        {"question": "What is the total number of interviews?", "expected_keywords": ["5", "total", "interviews"]},
        {"question": "How many rounds of interviews?", "expected_keywords": ["5", "total", "interviews"]},
        {"question": "Number of interview rounds?", "expected_keywords": ["5", "total", "interviews"]},
        
        # Focus areas questions
        {"question": "What are the four focus areas?", "expected_keywords": ["coding", "programming", "application design", "system integration", "googleyness", "leadership"]},
        {"question": "What focus areas are there?", "expected_keywords": ["coding", "programming", "application design", "system integration", "googleyness", "leadership"]},
        {"question": "Tell me about the focus areas", "expected_keywords": ["coding", "programming", "application design", "system integration", "googleyness", "leadership"]},
        {"question": "What are the interview focus areas?", "expected_keywords": ["coding", "programming", "application design", "system integration", "googleyness", "leadership"]},
        {"question": "Focus areas for Google interview?", "expected_keywords": ["coding", "programming", "application design", "system integration", "googleyness", "leadership"]},
        
        # Data structures questions
        {"question": "What data structures should I know?", "expected_keywords": ["array", "tree", "hashtable", "linked list"]},
        {"question": "Which data structures are important?", "expected_keywords": ["array", "tree", "hashtable", "linked list"]},
        {"question": "Tell me about data structures", "expected_keywords": ["array", "tree", "hashtable", "linked list"]},
        {"question": "What data structures to study?", "expected_keywords": ["array", "tree", "hashtable", "linked list"]},
        {"question": "Data structures for coding interview?", "expected_keywords": ["array", "tree", "hashtable", "linked list"]},
        
        # Programming languages questions
        {"question": "What programming languages are mentioned?", "expected_keywords": ["java", "python"]},
        {"question": "Which programming languages to use?", "expected_keywords": ["java", "python"]},
        {"question": "Tell me about programming languages", "expected_keywords": ["java", "python"]},
        {"question": "What languages are recommended?", "expected_keywords": ["java", "python"]},
        {"question": "Programming languages for interview?", "expected_keywords": ["java", "python"]},
        
        # Pitfalls questions
        {"question": "What are the common pitfalls?", "expected_keywords": ["jumping into design", "not talking out loud", "not picking up on hints", "suggesting an algorithm"]},
        {"question": "What pitfalls should I avoid?", "expected_keywords": ["jumping into design", "not talking out loud", "not picking up on hints", "suggesting an algorithm"]},
        {"question": "Tell me about interview pitfalls", "expected_keywords": ["jumping into design", "not talking out loud", "not picking up on hints", "suggesting an algorithm"]},
        {"question": "What mistakes to avoid?", "expected_keywords": ["jumping into design", "not talking out loud", "not picking up on hints", "suggesting an algorithm"]},
        {"question": "Common interview mistakes?", "expected_keywords": ["jumping into design", "not talking out loud", "not picking up on hints", "suggesting an algorithm"]},
        
        # Duration questions
        {"question": "How long are the interviews?", "expected_keywords": ["45", "60", "minute"]},
        {"question": "What is the interview duration?", "expected_keywords": ["45", "60", "minute"]},
        {"question": "Tell me about interview length", "expected_keywords": ["45", "60", "minute"]},
        {"question": "How long does each interview last?", "expected_keywords": ["45", "60", "minute"]},
        {"question": "Interview time duration?", "expected_keywords": ["45", "60", "minute"]},
        
        # Platform questions
        {"question": "What platform is used for interviews?", "expected_keywords": ["google", "hangouts"]},
        {"question": "Where are interviews conducted?", "expected_keywords": ["google", "hangouts"]},
        {"question": "Tell me about interview platform", "expected_keywords": ["google", "hangouts"]},
        {"question": "What technology is used?", "expected_keywords": ["google", "hangouts"]},
        {"question": "Interview platform details?", "expected_keywords": ["google", "hangouts"]},
        
        # General interview questions
        {"question": "Tell me about the interview process", "expected_keywords": ["interview", "process"]},
        {"question": "What is the interview like?", "expected_keywords": ["interview", "process"]},
        {"question": "How does the interview work?", "expected_keywords": ["interview", "process"]},
        {"question": "Interview process details?", "expected_keywords": ["interview", "process"]},
        {"question": "What happens in the interview?", "expected_keywords": ["interview", "process"]},
        
        # Tips and advice questions
        {"question": "What tips are given?", "expected_keywords": ["tips", "advice", "practice"]},
        {"question": "Any advice for the interview?", "expected_keywords": ["tips", "advice", "practice"]},
        {"question": "Tell me about interview tips", "expected_keywords": ["tips", "advice", "practice"]},
        {"question": "What recommendations are there?", "expected_keywords": ["tips", "advice", "practice"]},
        {"question": "Interview preparation tips?", "expected_keywords": ["tips", "advice", "practice"]},
        
        # Algorithm questions
        {"question": "What algorithms should I know?", "expected_keywords": ["algorithm", "data structure"]},
        {"question": "Tell me about algorithms", "expected_keywords": ["algorithm", "data structure"]},
        {"question": "Algorithm questions in interview?", "expected_keywords": ["algorithm", "data structure"]},
        {"question": "What algorithm topics are covered?", "expected_keywords": ["algorithm", "data structure"]},
        {"question": "Algorithm preparation tips?", "expected_keywords": ["algorithm", "data structure"]},
        
        # SQL questions
        {"question": "What about SQL questions?", "expected_keywords": ["sql", "database", "query"]},
        {"question": "Tell me about SQL in interviews", "expected_keywords": ["sql", "database", "query"]},
        {"question": "SQL interview preparation?", "expected_keywords": ["sql", "database", "query"]},
        {"question": "Database questions in interview?", "expected_keywords": ["sql", "database", "query"]},
        {"question": "What SQL topics to study?", "expected_keywords": ["sql", "database", "query"]},
        
        # General questions
        {"question": "interview", "expected_keywords": ["interview"]},
        {"question": "INTERVIEW", "expected_keywords": ["interview"]},
        {"question": "interview process", "expected_keywords": ["interview", "process"]},
        {"question": "google interview", "expected_keywords": ["google", "interview"]},
        {"question": "coding interview", "expected_keywords": ["coding", "interview"]}
    ]
    
    # 50 NEGATIVE TEST CASES (should return "Out of scope")
    negative_tests = [
        # Weather questions
        {"question": "What is the weather today?", "expected_response": "Out of scope."},
        {"question": "Will it rain tomorrow?", "expected_response": "Out of scope."},
        {"question": "Is it sunny outside?", "expected_response": "Out of scope."},
        {"question": "What's the temperature?", "expected_response": "Out of scope."},
        {"question": "Weather forecast for this week?", "expected_response": "Out of scope."},
        
        # Cooking questions
        {"question": "How do I cook pasta?", "expected_response": "Out of scope."},
        {"question": "What's a good recipe for chicken?", "expected_response": "Out of scope."},
        {"question": "How to make pizza?", "expected_response": "Out of scope."},
        {"question": "Cooking tips for beginners?", "expected_response": "Out of scope."},
        {"question": "Best way to cook rice?", "expected_response": "Out of scope."},
        
        # Geography questions
        {"question": "What is the capital of France?", "expected_response": "Out of scope."},
        {"question": "Where is Tokyo located?", "expected_response": "Out of scope."},
        {"question": "Tell me about geography", "expected_response": "Out of scope."},
        {"question": "What countries are in Europe?", "expected_response": "Out of scope."},
        {"question": "Geography facts?", "expected_response": "Out of scope."},
        
        # Science questions
        {"question": "Tell me about quantum physics", "expected_response": "Out of scope."},
        {"question": "What is the theory of relativity?", "expected_response": "Out of scope."},
        {"question": "How does gravity work?", "expected_response": "Out of scope."},
        {"question": "Explain DNA structure", "expected_response": "Out of scope."},
        {"question": "What is photosynthesis?", "expected_response": "Out of scope."},
        
        # Technology questions (not related to Google interview)
        {"question": "How does blockchain work?", "expected_response": "Out of scope."},
        {"question": "Tell me about machine learning", "expected_response": "Out of scope."},
        {"question": "What is artificial intelligence?", "expected_response": "Out of scope."},
        {"question": "How to build a website?", "expected_response": "Out of scope."},
        {"question": "What is cloud computing?", "expected_response": "Out of scope."},
        
        # Personal questions
        {"question": "What is the meaning of life?", "expected_response": "Out of scope."},
        {"question": "How to find love?", "expected_response": "Out of scope."},
        {"question": "What should I do with my life?", "expected_response": "Out of scope."},
        {"question": "How to be happy?", "expected_response": "Out of scope."},
        {"question": "What is success?", "expected_response": "Out of scope."},
        
        # Business questions (not Google interview related)
        {"question": "How to start a business?", "expected_response": "Out of scope."},
        {"question": "What is marketing?", "expected_response": "Out of scope."},
        {"question": "Tell me about finance", "expected_response": "Out of scope."},
        {"question": "How to invest money?", "expected_response": "Out of scope."},
        {"question": "What is entrepreneurship?", "expected_response": "Out of scope."},
        
        # Entertainment questions
        {"question": "What's the best movie?", "expected_response": "Out of scope."},
        {"question": "Tell me about music", "expected_response": "Out of scope."},
        {"question": "What books should I read?", "expected_response": "Out of scope."},
        {"question": "How to play guitar?", "expected_response": "Out of scope."},
        {"question": "What games are popular?", "expected_response": "Out of scope."},
        
        # Health questions
        {"question": "How to lose weight?", "expected_response": "Out of scope."},
        {"question": "What is a healthy diet?", "expected_response": "Out of scope."},
        {"question": "How to exercise properly?", "expected_response": "Out of scope."},
        {"question": "What vitamins should I take?", "expected_response": "Out of scope."},
        {"question": "How to sleep better?", "expected_response": "Out of scope."},
        
        # Empty/nonsensical questions
        {"question": "", "expected_response": "Out of scope."},
        {"question": "asdfghjkl", "expected_response": "Out of scope."},
        {"question": "123456789", "expected_response": "Out of scope."},
        {"question": "!@#$%^&*()", "expected_response": "Out of scope."},
        {"question": "qwertyuiop", "expected_response": "Out of scope."}
    ]
    
    # 20 FALSE POSITIVE TEST CASES (might incorrectly return document answers)
    false_positive_tests = [
        # Questions that contain interview-related keywords but are not about Google interview
        {"question": "How to prepare for a Microsoft interview?", "expected_response": "Out of scope."},
        {"question": "What about Amazon interview process?", "expected_response": "Out of scope."},
        {"question": "Tell me about Facebook interview", "expected_response": "Out of scope."},
        {"question": "Apple interview questions", "expected_response": "Out of scope."},
        {"question": "Netflix interview experience", "expected_response": "Out of scope."},
        
        # Questions about other companies' processes
        {"question": "How many rounds in Microsoft interview?", "expected_response": "Out of scope."},
        {"question": "Amazon interview duration?", "expected_response": "Out of scope."},
        {"question": "Facebook interview platform?", "expected_response": "Out of scope."},
        {"question": "Apple interview focus areas?", "expected_response": "Out of scope."},
        {"question": "Netflix interview tips?", "expected_response": "Out of scope."},
        
        # Questions about general interview topics not in the document
        {"question": "How to answer behavioral questions?", "expected_response": "Out of scope."},
        {"question": "What to wear for an interview?", "expected_response": "Out of scope."},
        {"question": "How to follow up after interview?", "expected_response": "Out of scope."},
        {"question": "What questions to ask interviewer?", "expected_response": "Out of scope."},
        {"question": "How to negotiate salary?", "expected_response": "Out of scope."},
        
        # Questions about other types of interviews
        {"question": "How to prepare for phone interview?", "expected_response": "Out of scope."},
        {"question": "Video interview best practices?", "expected_response": "Out of scope."},
        {"question": "Panel interview tips?", "expected_response": "Out of scope."},
        {"question": "Group interview strategies?", "expected_response": "Out of scope."},
        {"question": "Technical interview vs behavioral?", "expected_response": "Out of scope."}
    ]
    
    # Run tests
    all_tests = [
        ("POSITIVE TESTS", positive_tests, "positive"),
        ("NEGATIVE TESTS", negative_tests, "negative"),
        ("FALSE POSITIVE TESTS", false_positive_tests, "false_positive")
    ]
    
    total_passed = 0
    total_tests = 0
    results = {}
    
    for test_category, tests, test_type in all_tests:
        print(f"\n🔍 {test_category} ({len(tests)} tests)")
        print("-" * 60)
        
        category_passed = 0
        category_results = []
        
        for i, test in enumerate(tests):
            print(f"\nTest {i+1}: {test['question']}")
            
            response_json = send_chat_message(test['question'])
            
            if response_json is None:
                print("❌ Test failed due to server connection issue.")
                category_results.append({"status": "failed", "reason": "server_error"})
                continue
            
            response_text = response_json.get('response', '').lower()
            source = response_json.get('source', '')
            
            print(f"Response: {response_json.get('response')}")
            print(f"Source: {source}")
            
            if test_type == "negative" or test_type == "false_positive":
                # Should return "Out of scope"
                if response_text == test["expected_response"].lower():
                    print("✅ Correctly identified as out of scope")
                    category_passed += 1
                    category_results.append({"status": "passed"})
                else:
                    print(f"❌ Expected '{test['expected_response']}', but got '{response_json.get('response')}'")
                    category_results.append({"status": "failed", "reason": "wrong_response", "expected": test["expected_response"], "actual": response_json.get('response')})
            else:  # positive tests
                # Should return document-based answer with keywords
                if source == "documents":
                    found_keywords = 0
                    for keyword in test["expected_keywords"]:
                        if keyword.lower() in response_text:
                            found_keywords += 1
                    
                    if found_keywords >= len(test["expected_keywords"]) / 2:  # At least half keywords found
                        print(f"✅ Found {found_keywords}/{len(test['expected_keywords'])} expected keywords")
                        category_passed += 1
                        category_results.append({"status": "passed", "keywords_found": found_keywords, "total_keywords": len(test["expected_keywords"])})
                    else:
                        print(f"❌ Missing expected keywords: {test['expected_keywords']}")
                        category_results.append({"status": "failed", "reason": "missing_keywords", "keywords_found": found_keywords, "expected_keywords": test["expected_keywords"]})
                else:
                    print(f"❌ Expected document-based answer, but got source: {source}")
                    category_results.append({"status": "failed", "reason": "wrong_source", "expected_source": "documents", "actual_source": source})
            
            total_tests += 1
        
        total_passed += category_passed
        results[test_category] = {
            "passed": category_passed,
            "total": len(tests),
            "details": category_results
        }
        
        print(f"\n📊 {test_category} Summary: {category_passed}/{len(tests)} passed ({category_passed/len(tests)*100:.1f}%)")
    
    # Final summary
    print("\n" + "=" * 80)
    print("📊 COMPREHENSIVE TEST SUMMARY")
    print("=" * 80)
    print(f"Total Tests: {total_tests}")
    print(f"Total Passed: {total_passed}")
    print(f"Total Failed: {total_tests - total_passed}")
    print(f"Overall Success Rate: {total_passed / total_tests * 100:.1f}%")
    
    for category, result in results.items():
        print(f"\n{category}: {result['passed']}/{result['total']} passed ({result['passed']/result['total']*100:.1f}%)")
    
    if total_passed != total_tests:
        print(f"\n⚠️  {total_tests - total_passed} tests failed. Review the issues above.")
    else:
        print("\n🎉 All tests passed!")
    
    return results

if __name__ == "__main__":
    run_comprehensive_tests()
