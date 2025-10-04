#!/usr/bin/env python3
"""
Performance Test Suite for Document Chat System
Tests performance with and without Gemini API key
"""

import requests
import time
import json
import statistics
from typing import List, Dict, Tuple

class PerformanceTester:
    def __init__(self, base_url: str = "http://localhost:8080"):
        self.base_url = base_url
        self.test_questions = [
            # Interview count questions
            "how many interview rounds I have to give in this interview",
            "how many interviews are there",
            "what is the total number of interviews",
            "how many rounds do I need to complete",
            
            # Company/position questions
            "which company interview is it",
            "which position is this interview document about",
            "what company is this for",
            
            # Focus areas questions
            "what are the focus areas",
            "tell me about the focus areas",
            "what are the four focus areas",
            
            # Data structures questions
            "what data structures should I know",
            "which data structures are important",
            "tell me about data structures for coding",
            
            # Programming languages
            "what programming languages are mentioned",
            "which languages should I use",
            "java or python for interview",
            
            # Pitfalls and tips
            "what are the common pitfalls",
            "what should I avoid during interview",
            "give me some interview tips",
            "any advice for the interview",
            
            # Duration and platform
            "how long is each interview",
            "what platform is used for interviews",
            "where are interviews conducted",
            
            # Algorithm questions
            "what algorithms should I know",
            "algorithm topics for interview",
            "big-o complexity questions",
            
            # SQL questions
            "what SQL topics are covered",
            "database questions in interview",
            "SQL preparation topics",
            
            # General process
            "how does the interview process work",
            "what is the interview like",
            "tell me about the interview process",
            
            # Out of scope questions (should be rejected)
            "what is the weather today",
            "how to cook pasta",
            "what is the capital of France",
            "tell me about quantum physics",
            "what stocks should I buy",
            "how to lose weight",
            "best movies to watch",
            "guitar lessons online"
        ]
    
    def upload_document(self) -> bool:
        """Upload the test document"""
        try:
            with open("InterviewGuideAtGoogle.pdf", "rb") as f:
                files = {"file": f}
                response = requests.post(f"{self.base_url}/api/documents/upload", files=files)
                return response.status_code == 200
        except Exception as e:
            print(f"Error uploading document: {e}")
            return False
    
    def test_single_question(self, question: str) -> Dict:
        """Test a single question and measure performance"""
        start_time = time.time()
        
        try:
            response = requests.post(
                f"{self.base_url}/api/chat/message",
                json={"message": question},
                timeout=30
            )
            
            end_time = time.time()
            response_time = end_time - start_time
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "question": question,
                    "response_time": response_time,
                    "status_code": response.status_code,
                    "response": data.get("response", ""),
                    "source": data.get("source", ""),
                    "success": True,
                    "error": None
                }
            else:
                return {
                    "question": question,
                    "response_time": response_time,
                    "status_code": response.status_code,
                    "response": None,
                    "source": None,
                    "success": False,
                    "error": f"HTTP {response.status_code}"
                }
        except Exception as e:
            end_time = time.time()
            return {
                "question": question,
                "response_time": end_time - start_time,
                "status_code": None,
                "response": None,
                "source": None,
                "success": False,
                "error": str(e)
            }
    
    def run_performance_test(self, test_name: str) -> Dict:
        """Run comprehensive performance test"""
        print(f"\n{'='*60}")
        print(f"Running Performance Test: {test_name}")
        print(f"{'='*60}")
        
        # Upload document first
        print("Uploading document...")
        if not self.upload_document():
            return {"error": "Failed to upload document"}
        
        time.sleep(2)  # Wait for document processing
        
        results = []
        response_times = []
        success_count = 0
        out_of_scope_count = 0
        
        print(f"Testing {len(self.test_questions)} questions...")
        
        for i, question in enumerate(self.test_questions, 1):
            print(f"Testing {i}/{len(self.test_questions)}: {question[:50]}...")
            result = self.test_single_question(question)
            results.append(result)
            
            if result["success"]:
                response_times.append(result["response_time"])
                success_count += 1
                
                # Check if response is "Out of scope" for out-of-scope questions
                if i > 30 and "out of scope" in result["response"].lower():
                    out_of_scope_count += 1
            
            # Small delay between requests
            time.sleep(0.1)
        
        # Calculate statistics
        if response_times:
            avg_response_time = statistics.mean(response_times)
            median_response_time = statistics.median(response_times)
            min_response_time = min(response_times)
            max_response_time = max(response_times)
            std_dev = statistics.stdev(response_times) if len(response_times) > 1 else 0
        else:
            avg_response_time = median_response_time = min_response_time = max_response_time = std_dev = 0
        
        # Analyze response quality
        relevant_questions = self.test_questions[:30]  # First 30 are relevant
        out_of_scope_questions = self.test_questions[30:]  # Last 8 are out of scope
        
        relevant_results = results[:30]
        out_of_scope_results = results[30:]
        
        # Count relevant questions that got good responses
        good_relevant_responses = 0
        for result in relevant_results:
            if result["success"] and result["response"] and "out of scope" not in result["response"].lower():
                good_relevant_responses += 1
        
        # Count out-of-scope questions that were properly rejected
        properly_rejected = 0
        for result in out_of_scope_results:
            if result["success"] and result["response"] and "out of scope" in result["response"].lower():
                properly_rejected += 1
        
        return {
            "test_name": test_name,
            "total_questions": len(self.test_questions),
            "successful_requests": success_count,
            "success_rate": (success_count / len(self.test_questions)) * 100,
            "response_times": {
                "average": avg_response_time,
                "median": median_response_time,
                "min": min_response_time,
                "max": max_response_time,
                "std_dev": std_dev
            },
            "quality_metrics": {
                "relevant_questions_answered": good_relevant_responses,
                "relevant_questions_total": len(relevant_questions),
                "relevant_accuracy": (good_relevant_responses / len(relevant_questions)) * 100,
                "out_of_scope_properly_rejected": properly_rejected,
                "out_of_scope_total": len(out_of_scope_questions),
                "out_of_scope_accuracy": (properly_rejected / len(out_of_scope_questions)) * 100
            },
            "detailed_results": results
        }
    
    def compare_performance(self, with_gemini_results: Dict, without_gemini_results: Dict):
        """Compare performance between two test runs"""
        print(f"\n{'='*80}")
        print("PERFORMANCE COMPARISON")
        print(f"{'='*80}")
        
        print(f"\n📊 RESPONSE TIME COMPARISON:")
        print(f"{'Metric':<20} {'With Gemini':<15} {'Without Gemini':<15} {'Difference':<15}")
        print("-" * 65)
        
        with_times = with_gemini_results["response_times"]
        without_times = without_gemini_results["response_times"]
        
        metrics = [
            ("Average (s)", with_times["average"], without_times["average"]),
            ("Median (s)", with_times["median"], without_times["median"]),
            ("Min (s)", with_times["min"], without_times["min"]),
            ("Max (s)", with_times["max"], without_times["max"]),
            ("Std Dev (s)", with_times["std_dev"], without_times["std_dev"])
        ]
        
        for metric, with_val, without_val in metrics:
            diff = without_val - with_val
            diff_pct = ((without_val - with_val) / with_val * 100) if with_val > 0 else 0
            print(f"{metric:<20} {with_val:<15.3f} {without_val:<15.3f} {diff:+.3f} ({diff_pct:+.1f}%)")
        
        print(f"\n🎯 ACCURACY COMPARISON:")
        print(f"{'Metric':<30} {'With Gemini':<15} {'Without Gemini':<15} {'Difference':<15}")
        print("-" * 75)
        
        with_quality = with_gemini_results["quality_metrics"]
        without_quality = without_gemini_results["quality_metrics"]
        
        quality_metrics = [
            ("Relevant Accuracy (%)", with_quality["relevant_accuracy"], without_quality["relevant_accuracy"]),
            ("Out-of-Scope Accuracy (%)", with_quality["out_of_scope_accuracy"], without_quality["out_of_scope_accuracy"]),
            ("Success Rate (%)", with_gemini_results["success_rate"], without_gemini_results["success_rate"])
        ]
        
        for metric, with_val, without_val in quality_metrics:
            diff = without_val - with_val
            print(f"{metric:<30} {with_val:<15.1f} {without_val:<15.1f} {diff:+.1f}")
        
        print(f"\n💡 SUMMARY:")
        avg_with = with_times["average"]
        avg_without = without_times["average"]
        speed_improvement = ((avg_with - avg_without) / avg_with * 100) if avg_with > 0 else 0
        
        print(f"• Speed: {'Faster' if avg_without < avg_with else 'Slower'} by {abs(speed_improvement):.1f}%")
        print(f"• Relevant Accuracy: {without_quality['relevant_accuracy']:.1f}% vs {with_quality['relevant_accuracy']:.1f}%")
        print(f"• Out-of-Scope Accuracy: {without_quality['out_of_scope_accuracy']:.1f}% vs {with_quality['out_of_scope_accuracy']:.1f}%")
        
        if avg_without < avg_with:
            print(f"✅ WITHOUT Gemini is {abs(speed_improvement):.1f}% FASTER")
        else:
            print(f"⚠️  WITH Gemini is {abs(speed_improvement):.1f}% FASTER")
        
        if without_quality['relevant_accuracy'] >= with_quality['relevant_accuracy']:
            print("✅ WITHOUT Gemini has EQUAL or BETTER accuracy")
        else:
            print("⚠️  WITH Gemini has BETTER accuracy")

def main():
    tester = PerformanceTester()
    
    print("🚀 Starting Performance Test Suite")
    print("This will test the system with and without Gemini API key")
    
    # Test 1: With Gemini API key (current configuration)
    print("\n" + "="*60)
    print("TEST 1: WITH GEMINI API KEY")
    print("="*60)
    
    with_gemini_results = tester.run_performance_test("With Gemini API Key")
    
    if "error" in with_gemini_results:
        print(f"❌ Test failed: {with_gemini_results['error']}")
        return
    
    # Test 2: Without Gemini API key
    print("\n" + "="*60)
    print("TEST 2: WITHOUT GEMINI API KEY")
    print("="*60)
    print("Please remove or comment out the Gemini API key in application.properties")
    print("Then restart the server and press Enter to continue...")
    input()
    
    without_gemini_results = tester.run_performance_test("Without Gemini API Key")
    
    if "error" in without_gemini_results:
        print(f"❌ Test failed: {without_gemini_results['error']}")
        return
    
    # Compare results
    tester.compare_performance(with_gemini_results, without_gemini_results)
    
    # Save detailed results
    with open("performance_results.json", "w") as f:
        json.dump({
            "with_gemini": with_gemini_results,
            "without_gemini": without_gemini_results,
            "timestamp": time.time()
        }, f, indent=2)
    
    print(f"\n📁 Detailed results saved to performance_results.json")

if __name__ == "__main__":
    main()
