#!/usr/bin/env python3
"""
AI Chatbot Comprehensive Test Suite
Tests 50 different questions and analyzes responses
"""

import requests
import json
import time
from datetime import datetime

# Test questions categorized by type
TEST_QUESTIONS = [
    # 멤버 관련 (10개)
    {"q": "이주형이라는 사람이 있어?", "expected_keywords": ["이주형", "석사", "학생"], "category": "member"},
    {"q": "팀 구성원은 누구인가요?", "expected_keywords": ["교수", "학생", "인턴"], "category": "member"},
    {"q": "석사과정 학생은 몇 명인가요?", "expected_keywords": ["석사", "10", "명"], "category": "member"},
    {"q": "박성용 학생 이메일 알려주세요", "expected_keywords": ["ejqdl010", "gmail"], "category": "member"},
    {"q": "김희원 교수님 이메일은?", "expected_keywords": ["hwkim", "ssu.ac.kr"], "category": "member"},
    {"q": "정호재님 깃허브 주소는?", "expected_keywords": ["github", "JEONG-HO-JAE"], "category": "member"},
    {"q": "이세빈 학생에 대해 알려주세요", "expected_keywords": ["이세빈", "컴퓨터", "비전"], "category": "member"},
    {"q": "김도원 학생 연락처는?", "expected_keywords": ["a01066304767"], "category": "member"},
    {"q": "연구 인턴은 몇 명이에요?", "expected_keywords": ["인턴", "11", "명"], "category": "member"},
    {"q": "최영재 학생 전공이 뭐예요?", "expected_keywords": ["통계", "Statistics"], "category": "member"},

    # 교수/연구실 정보 (10개)
    {"q": "연구실 이름이 뭐예요?", "expected_keywords": ["Reality Lab"], "category": "lab_info"},
    {"q": "Reality Lab은 어디에 있나요?", "expected_keywords": ["서울", "동작구", "숭실"], "category": "lab_info"},
    {"q": "연구실 전화번호 알려주세요", "expected_keywords": ["820-0679"], "category": "lab_info"},
    {"q": "김희원 교수님 전공은?", "expected_keywords": ["컴퓨터", "비전", "vision"], "category": "lab_info"},
    {"q": "연구실은 언제 설립되었나요?", "expected_keywords": ["2023"], "category": "lab_info"},
    {"q": "Reality Lab 주소가 어떻게 되나요?", "expected_keywords": ["사당로", "105"], "category": "lab_info"},
    {"q": "어떤 연구를 하나요?", "expected_keywords": ["컴퓨터", "비전", "AI"], "category": "lab_info"},
    {"q": "교수님 소속은?", "expected_keywords": ["Global School of Media", "미디어"], "category": "lab_info"},
    {"q": "연구실 위치 알려주세요", "expected_keywords": ["서울", "숭실"], "category": "lab_info"},
    {"q": "지도 교수님은 누구세요?", "expected_keywords": ["김희원"], "category": "lab_info"},

    # 연구 주제 (10개)
    {"q": "어떤 분야를 연구하나요?", "expected_keywords": ["컴퓨터", "비전", "딥러닝", "AI"], "category": "research"},
    {"q": "로보틱스 연구도 하나요?", "expected_keywords": ["로보틱스", "Robotics"], "category": "research"},
    {"q": "박성용 학생 연구 주제는?", "expected_keywords": ["Image Restoration", "Astronomy"], "category": "research"},
    {"q": "이상민 학생은 무슨 연구해요?", "expected_keywords": ["Embodied AI", "Computer Vision"], "category": "research"},
    {"q": "의료 AI 연구도 하나요?", "expected_keywords": ["의료", "Medical", "AI"], "category": "research"},
    {"q": "3D 비전 연구하는 학생 있어요?", "expected_keywords": ["고민주", "Minjoo"], "category": "research"},
    {"q": "생성 모델 연구는 누가 해요?", "expected_keywords": ["Generative", "생성"], "category": "research"},
    {"q": "스포츠 AI 연구 있나요?", "expected_keywords": ["Sports", "스포츠"], "category": "research"},
    {"q": "멀티모달 연구 하시나요?", "expected_keywords": ["Multimodal", "멀티모달"], "category": "research"},
    {"q": "딥러닝 연구하는 학생은?", "expected_keywords": ["Deep Learning", "딥러닝"], "category": "research"},

    # 논문/업적 (10개)
    {"q": "CVPR 2025에 논문이 있나요?", "expected_keywords": ["CVPR", "2025", "DynScene"], "category": "publication"},
    {"q": "최근 발표한 논문은?", "expected_keywords": ["2025", "CVPR", "AAAI"], "category": "publication"},
    {"q": "AAAI에 논문 냈어요?", "expected_keywords": ["AAAI", "SIDL"], "category": "publication"},
    {"q": "Embodied AI 관련 논문 있어요?", "expected_keywords": ["DynScene", "Embodied"], "category": "publication"},
    {"q": "1등 수상한 적 있나요?", "expected_keywords": ["1st", "ARNOLD", "Challenge"], "category": "publication"},
    {"q": "국제 학회 논문이 몇 개예요?", "expected_keywords": ["CVPR", "ICCV", "AAAI"], "category": "publication"},
    {"q": "TPAMI 저널 논문 있나요?", "expected_keywords": ["TPAMI"], "category": "publication"},
    {"q": "2025년 논문은?", "expected_keywords": ["2025", "CVPR", "AAAI"], "category": "publication"},
    {"q": "Image Restoration 논문 있어요?", "expected_keywords": ["Image Restoration", "SIDL"], "category": "publication"},
    {"q": "최근 연구 성과는?", "expected_keywords": ["CVPR", "AAAI", "2025"], "category": "publication"},

    # 지원/참여 (10개)
    {"q": "연구실에 지원하려면 어떻게 해야 하나요?", "expected_keywords": ["지원", "문의", "연락"], "category": "recruitment"},
    {"q": "석사 과정 지원 방법은?", "expected_keywords": ["석사", "지원", "문의"], "category": "recruitment"},
    {"q": "인턴 모집하나요?", "expected_keywords": ["인턴", "모집"], "category": "recruitment"},
    {"q": "학부생도 참여할 수 있나요?", "expected_keywords": ["학부", "인턴"], "category": "recruitment"},
    {"q": "어떤 학생을 선호하나요?", "expected_keywords": ["컴퓨터", "비전", "딥러닝"], "category": "recruitment"},
    {"q": "지원 자격이 어떻게 되나요?", "expected_keywords": ["컴퓨터", "AI"], "category": "recruitment"},
    {"q": "연락은 어떻게 하나요?", "expected_keywords": ["hwkim", "ssu.ac.kr", "820-0679"], "category": "recruitment"},
    {"q": "면접은 어떻게 진행되나요?", "expected_keywords": ["문의", "연락"], "category": "recruitment"},
    {"q": "필요한 스킬이 뭐예요?", "expected_keywords": ["딥러닝", "컴퓨터", "비전"], "category": "recruitment"},
    {"q": "교수님께 어떻게 연락드리나요?", "expected_keywords": ["hwkim", "ssu.ac.kr"], "category": "recruitment"},
]

def test_question(question, server_url="http://localhost:4005/chat"):
    """Test a single question and return the response"""
    try:
        response = requests.post(
            server_url,
            json={"question": question["q"]},
            headers={"Content-Type": "application/json"},
            timeout=60
        )
        response.raise_for_status()
        data = response.json()
        return {
            "question": question["q"],
            "category": question["category"],
            "expected_keywords": question["expected_keywords"],
            "response": data.get("response", ""),
            "response_time": data.get("response_time", 0),
            "tokens": data.get("tokens", 0),
            "error": None
        }
    except Exception as e:
        return {
            "question": question["q"],
            "category": question["category"],
            "expected_keywords": question["expected_keywords"],
            "response": "",
            "response_time": 0,
            "tokens": 0,
            "error": str(e)
        }

def analyze_response(result):
    """Analyze if response is acceptable"""
    response = result["response"].lower()
    expected = result["expected_keywords"]

    # Check for error
    if result["error"]:
        return {
            "status": "ERROR",
            "reason": result["error"],
            "matched_keywords": []
        }

    # Check for empty response
    if not response or len(response.strip()) < 10:
        return {
            "status": "FAIL",
            "reason": "응답이 너무 짧거나 없음",
            "matched_keywords": []
        }

    # Check for error messages in response
    error_phrases = ["오류가 발생", "죄송합니다", "응답을 생성할 수 없습니다", "다시 시도"]
    if any(phrase in response for phrase in error_phrases):
        return {
            "status": "FAIL",
            "reason": "오류 응답",
            "matched_keywords": []
        }

    # Check for internal reasoning (hallucination)
    bad_patterns = ["참고자료 1", "참고자료 2", "정답:", "질문:", "---", "**정답**", "looking at reference"]
    if any(pattern.lower() in response for pattern in bad_patterns):
        return {
            "status": "WARN",
            "reason": "내부 추론 과정 포함",
            "matched_keywords": []
        }

    # Check keyword matching
    matched = []
    for keyword in expected:
        if keyword.lower() in response:
            matched.append(keyword)

    match_rate = len(matched) / len(expected) if expected else 0

    if match_rate >= 0.5:  # At least 50% keywords matched
        return {
            "status": "PASS",
            "reason": f"키워드 매칭 {match_rate*100:.0f}%",
            "matched_keywords": matched
        }
    else:
        return {
            "status": "FAIL",
            "reason": f"키워드 매칭 부족 ({match_rate*100:.0f}%)",
            "matched_keywords": matched
        }

def run_tests():
    """Run all tests and generate report"""
    print("=" * 80)
    print("AI Chatbot Comprehensive Test - 50 Questions")
    print("=" * 80)
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    results = []
    total = len(TEST_QUESTIONS)

    for i, question in enumerate(TEST_QUESTIONS, 1):
        print(f"[{i}/{total}] Testing: {question['q'][:50]}...")
        result = test_question(question)
        analysis = analyze_response(result)

        result["analysis"] = analysis
        results.append(result)

        # Print status
        status_symbol = {
            "PASS": "✅",
            "WARN": "⚠️",
            "FAIL": "❌",
            "ERROR": "🚨"
        }
        symbol = status_symbol.get(analysis["status"], "❓")
        print(f"   {symbol} {analysis['status']}: {analysis['reason']}")

        # Small delay between requests
        time.sleep(1)

    # Generate summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)

    status_counts = {"PASS": 0, "WARN": 0, "FAIL": 0, "ERROR": 0}
    for result in results:
        status = result["analysis"]["status"]
        status_counts[status] = status_counts.get(status, 0) + 1

    print(f"Total Questions: {total}")
    print(f"✅ PASS: {status_counts['PASS']} ({status_counts['PASS']/total*100:.1f}%)")
    print(f"⚠️  WARN: {status_counts['WARN']} ({status_counts['WARN']/total*100:.1f}%)")
    print(f"❌ FAIL: {status_counts['FAIL']} ({status_counts['FAIL']/total*100:.1f}%)")
    print(f"🚨 ERROR: {status_counts['ERROR']} ({status_counts['ERROR']/total*100:.1f}%)")

    # Category breakdown
    print("\n" + "-" * 80)
    print("CATEGORY BREAKDOWN")
    print("-" * 80)

    categories = {}
    for result in results:
        cat = result["category"]
        if cat not in categories:
            categories[cat] = {"PASS": 0, "WARN": 0, "FAIL": 0, "ERROR": 0, "total": 0}
        categories[cat][result["analysis"]["status"]] += 1
        categories[cat]["total"] += 1

    for cat, counts in sorted(categories.items()):
        pass_rate = counts["PASS"] / counts["total"] * 100
        print(f"{cat:15s}: {counts['PASS']}/{counts['total']} passed ({pass_rate:.0f}%)")

    # Failed questions detail
    failed = [r for r in results if r["analysis"]["status"] in ["FAIL", "ERROR"]]
    if failed:
        print("\n" + "-" * 80)
        print("FAILED QUESTIONS DETAIL")
        print("-" * 80)
        for result in failed:
            print(f"\n질문: {result['question']}")
            print(f"상태: {result['analysis']['status']}")
            print(f"이유: {result['analysis']['reason']}")
            print(f"응답: {result['response'][:200]}...")

    # Warning questions
    warned = [r for r in results if r["analysis"]["status"] == "WARN"]
    if warned:
        print("\n" + "-" * 80)
        print("WARNING QUESTIONS (Internal Reasoning)")
        print("-" * 80)
        for result in warned:
            print(f"\n질문: {result['question']}")
            print(f"응답: {result['response'][:200]}...")

    # Final verdict
    print("\n" + "=" * 80)
    pass_rate = (status_counts["PASS"] + status_counts["WARN"]) / total * 100

    if status_counts["PASS"] >= 45:  # 90% pass
        print("🎉 TEST PASSED! Ready to deploy.")
        verdict = "PASS"
    elif pass_rate >= 40:  # 80% acceptable
        print("⚠️  TEST ACCEPTABLE. Some issues need attention.")
        verdict = "ACCEPTABLE"
    else:
        print("❌ TEST FAILED! Significant issues found.")
        verdict = "FAIL"

    print("=" * 80)

    # Save detailed results
    with open("/home/i0179/Realitylab-site/ai_server/test_results.json", "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "summary": status_counts,
            "verdict": verdict,
            "results": results
        }, f, ensure_ascii=False, indent=2)

    print(f"\nDetailed results saved to: ai_server/test_results.json")

    return verdict, status_counts

if __name__ == "__main__":
    verdict, counts = run_tests()
    exit(0 if verdict == "PASS" else 1)
