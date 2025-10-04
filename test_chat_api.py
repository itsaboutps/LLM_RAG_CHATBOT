#!/usr/bin/env python3
"""
Comprehensive test script for the Document Chat API
Tests both positive and negative scenarios to ensure robustness
"""

import requests
import json
import time
from typing import Dict, List, Tuple

# API Configuration
BASE_URL = "http://localhost:8080"
CHAT_ENDPOINT = f"{BASE_URL}/api/chat/message"
DOCUMENTS_ENDPOINT = f"{BASE_URL}/api/documents"

class ChatAPITester:
    def __init__(self):
        self.session = requests.Session()
        self.test_results = []
        
    def send_message(self, message: str) -> Dict:
        """Send a message to the chat API and return the response"""
        try:
            payload = {"message": message}
            response = self.session.post(CHAT_ENDPOINT, json=payload, timeout=30)
            return {
                "status_code": response.status_code,
                "response": response.json() if response.status_code == 200 else response.text,
                "success": response.status_code == 200
            }
        except Exception as e:
            return {
                "status_code": 0,
                "response": str(e),
                "success": False
            }
    
    def test_positive_cases(self) -> List[Dict]:
        """Test 20 positive cases - questions that should be answerable from the document"""
        positive_tests = [
            # Basic interview information
            "How many interviews are there in the Google interview process?",
            "What is the total number of interviews?",
            "How many rounds of interviews are there?",
            
            # Focus areas
            "What are the four focus areas for the Google interview?",
            "What are the different focus areas mentioned?",
            "Tell me about the focus areas for the interview",
            
            # Data structures and programming
            "What data structures should I know for the coding interview?",
            "What programming languages are mentioned for the interview?",
            "What are the important data structures to study?",
            "Should I know Java or Python for the interview?",
            
            # Interview tips and pitfalls
            "What are the common pitfalls to avoid during the interview?",
            "What should I avoid during the interview?",
            "What are the interviewing pitfalls mentioned?",
            "What tips are given for the interview?",
            
            # Technical details
            "What is the duration of each interview?",
            "How long are the interviews?",
            "What platform is used for the interviews?",
            "Are the interviews done over Google Hangouts?",
            
            # General interview preparation
            "What should I prepare for the Google interview?",
            "How should I prepare for the technical interview?",
            "What are the evaluation criteria for coding?"
        ]
        
        print("🧪 Testing 20 Positive Cases...")
        results = []
        for i, question in enumerate(positive_tests, 1):
            print(f"  Test {i:2d}: {question[:60]}...")
            result = self.send_message(question)
            result["test_type"] = "positive"
            result["question"] = question
            result["test_number"] = i
            results.append(result)
            time.sleep(0.5)  # Rate limiting
        
        return results
    
    def test_negative_cases(self) -> List[Dict]:
        """Test 20 negative cases - questions that should not be answerable or should handle errors gracefully"""
        negative_tests = [
            # Out of scope questions
            "What is the weather like today?",
            "How do I cook pasta?",
            "What is the capital of France?",
            "Tell me about quantum physics",
            "What are the latest stock prices?",
            
            # Empty or invalid inputs
            "",
            "   ",
            "!@#$%^&*()",
            "123456789",
            "a" * 1000,  # Very long string
            
            # Nonsensical questions
            "asdfghjkl qwertyuiop",
            "What is the meaning of life?",
            "How do I become a millionaire?",
            "What is love?",
            "Why is the sky blue?",
            
            # Questions about topics not in the document
            "What are the salary ranges at Google?",
            "How do I get a job at Microsoft?",
            "What is the company culture like?",
            "Tell me about Google's benefits",
            "What is the work-life balance like?"
        ]
        
        print("🧪 Testing 20 Negative Cases...")
        results = []
        for i, question in enumerate(negative_tests, 1):
            print(f"  Test {i:2d}: {question[:60] if question else '(empty)'}...")
            result = self.send_message(question)
            result["test_type"] = "negative"
            result["question"] = question
            result["test_number"] = i
            results.append(result)
            time.sleep(0.5)  # Rate limiting
        
        return results
    
    def test_edge_cases(self) -> List[Dict]:
        """Test additional edge cases for robustness"""
        edge_tests = [
            # Special characters and encoding
            "What's the interview process? (with special chars)",
            "Interview process: 5 rounds?",
            "How many interviews? (5 total)",
            
            # Partial matches
            "interview",
            "coding",
            "data structures",
            "Google",
            
            # Very specific questions
            "What is the exact duration of each interview in minutes?",
            "What is the specific platform used for interviews?",
            "What are the exact evaluation criteria?",
            
            # Questions with typos (should still work)
            "How many interveiws are there?",
            "What are the focas areas?",
            "Tell me about data structurs",
            
            # Questions in different formats
            "INTERVIEW PROCESS?",
            "interview process.",
            "Interview Process!",
            "interview process?"
        ]
        
        print("🧪 Testing Edge Cases...")
        results = []
        for i, question in enumerate(edge_tests, 1):
            print(f"  Test {i:2d}: {question[:60]}...")
            result = self.send_message(question)
            result["test_type"] = "edge"
            result["question"] = question
            result["test_number"] = i
            results.append(result)
            time.sleep(0.5)  # Rate limiting
        
        return results
    
    def analyze_results(self, results: List[Dict]) -> Dict:
        """Analyze test results and provide summary"""
        total_tests = len(results)
        successful_tests = sum(1 for r in results if r["success"])
        failed_tests = total_tests - successful_tests
        
        # Analyze by test type
        positive_results = [r for r in results if r["test_type"] == "positive"]
        negative_results = [r for r in results if r["test_type"] == "negative"]
        edge_results = [r for r in results if r["test_type"] == "edge"]
        
        # Check response quality for positive tests
        good_responses = 0
        for result in positive_results:
            if result["success"] and result["response"]:
                response_text = result["response"].get("response", "").lower()
                # Check if response contains relevant information
                if any(keyword in response_text for keyword in ["interview", "5", "five", "coding", "data", "structure"]):
                    good_responses += 1
        
        # Check if negative tests properly return "out of scope" or similar
        proper_rejections = 0
        for result in negative_results:
            if result["success"] and result["response"]:
                response_text = result["response"].get("response", "").lower()
                if any(keyword in response_text for keyword in ["out of scope", "not found", "no documents", "unable"]):
                    proper_rejections += 1
        
        return {
            "total_tests": total_tests,
            "successful_tests": successful_tests,
            "failed_tests": failed_tests,
            "success_rate": (successful_tests / total_tests) * 100,
            "positive_tests": len(positive_results),
            "negative_tests": len(negative_results),
            "edge_tests": len(edge_results),
            "good_responses": good_responses,
            "proper_rejections": proper_rejections,
            "response_quality_rate": (good_responses / len(positive_results)) * 100 if positive_results else 0,
            "rejection_quality_rate": (proper_rejections / len(negative_results)) * 100 if negative_results else 0
        }
    
    def print_detailed_results(self, results: List[Dict]):
        """Print detailed test results"""
        print("\n" + "="*80)
        print("📊 DETAILED TEST RESULTS")
        print("="*80)
        
        for result in results:
            status = "✅ PASS" if result["success"] else "❌ FAIL"
            print(f"\n{status} Test #{result['test_number']} ({result['test_type']})")
            print(f"Question: {result['question']}")
            print(f"Status Code: {result['status_code']}")
            
            if result["success"] and result["response"]:
                response_data = result["response"]
                if isinstance(response_data, dict):
                    print(f"Response: {response_data.get('response', 'No response text')[:200]}...")
                    print(f"Source: {response_data.get('source', 'Unknown')}")
                else:
                    print(f"Response: {str(response_data)[:200]}...")
            else:
                print(f"Error: {result['response']}")
    
    def run_all_tests(self):
        """Run all test suites"""
        print("🚀 Starting Comprehensive API Testing")
        print("="*50)
        
        # Check if server is running
        try:
            response = self.session.get(DOCUMENTS_ENDPOINT, timeout=5)
            if response.status_code == 200:
                print("✅ Server is running and accessible")
            else:
                print("❌ Server returned unexpected status code")
                return
        except Exception as e:
            print(f"❌ Cannot connect to server: {e}")
            return
        
        # Run all test suites
        all_results = []
        
        # Positive tests
        positive_results = self.test_positive_cases()
        all_results.extend(positive_results)
        
        # Negative tests
        negative_results = self.test_negative_cases()
        all_results.extend(negative_results)
        
        # Edge cases
        edge_results = self.test_edge_cases()
        all_results.extend(edge_results)
        
        # Analyze results
        analysis = self.analyze_results(all_results)
        
        # Print summary
        print("\n" + "="*80)
        print("📈 TEST SUMMARY")
        print("="*80)
        print(f"Total Tests: {analysis['total_tests']}")
        print(f"Successful: {analysis['successful_tests']} ({analysis['success_rate']:.1f}%)")
        print(f"Failed: {analysis['failed_tests']}")
        print(f"\nPositive Tests: {analysis['positive_tests']}")
        print(f"Good Responses: {analysis['good_responses']} ({analysis['response_quality_rate']:.1f}%)")
        print(f"\nNegative Tests: {analysis['negative_tests']}")
        print(f"Proper Rejections: {analysis['proper_rejections']} ({analysis['rejection_quality_rate']:.1f}%)")
        print(f"\nEdge Cases: {analysis['edge_tests']}")
        
        # Print detailed results
        self.print_detailed_results(all_results)
        
        # Save results to file
        with open("test_results.json", "w") as f:
            json.dump({
                "summary": analysis,
                "detailed_results": all_results
            }, f, indent=2)
        
        print(f"\n💾 Detailed results saved to test_results.json")
        
        return analysis

if __name__ == "__main__":
    tester = ChatAPITester()
    results = tester.run_all_tests()
