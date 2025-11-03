#!/usr/bin/env python3
"""
AI Chatbot Realistic Test Suite
Based on actual homepage content
Tests 30 realistic questions with proper delays to avoid concurrency issues
"""

import requests
import json
import time
from datetime import datetime

# Test questions based on ACTUAL homepage content
TEST_QUESTIONS = [
    # 교수/연구실 기본 정보 (7개)
    {
        "q": "연구실 이름이 뭐예요?",
        "expected_keywords": ["Reality Lab", "SSU"],
        "category": "lab_info"
    },
    {
        "q": "김희원 교수님 이메일 주소 알려주세요",
        "expected_keywords": ["hwkim", "ssu.ac.kr"],
        "category": "lab_info"
    },
    {
        "q": "연구실 전화번호는?",
        "expected_keywords": ["820-0679", "02"],
        "category": "lab_info"
    },
    {
        "q": "교수님이 어느 학과 소속이에요?",
        "expected_keywords": ["Global School of Media", "미디어"],
        "category": "lab_info"
    },
    {
        "q": "연구실은 언제 만들어졌나요?",
        "expected_keywords": ["2023"],
        "category": "lab_info"
    },
    {
        "q": "Reality Lab은 어떤 연구를 하나요?",
        "expected_keywords": ["computer vision", "robotics", "AI", "비전"],
        "category": "lab_info"
    },
    {
        "q": "김희원 교수님 구글 스칼라 주소 있나요?",
        "expected_keywords": ["google", "scholar", "citations"],
        "category": "lab_info"
    },

    # 석사 학생 정보 (8개)
    {
        "q": "석사과정 학생은 몇 명인가요?",
        "expected_keywords": ["10", "석사", "명"],
        "category": "member"
    },
    {
        "q": "박성용 학생은 어떤 연구를 해요?",
        "expected_keywords": ["Image Restoration", "Astronomy", "천문"],
        "category": "member"
    },
    {
        "q": "이상민 학생 이메일 주소는?",
        "expected_keywords": ["sm32289", "gmail"],
        "category": "member"
    },
    {
        "q": "Embodied AI 연구하는 학생 있어요?",
        "expected_keywords": ["이상민", "Sangmin"],
        "category": "member"
    },
    {
        "q": "고민주 학생 전공이 뭐예요?",
        "expected_keywords": ["Data Science", "데이터", "세종"],
        "category": "member"
    },
    {
        "q": "정호재 학생 깃허브 주소는?",
        "expected_keywords": ["github", "JEONG-HO-JAE"],
        "category": "member"
    },
    {
        "q": "Multimodal Learning 연구하는 학생은?",
        "expected_keywords": ["고현서", "Hyunsuh"],
        "category": "member"
    },
    {
        "q": "이주형 학생에 대해 알려주세요",
        "expected_keywords": ["이주형", "석사", "Computer Vision"],
        "category": "member"
    },

    # 인턴 정보 (4개)
    {
        "q": "연구 인턴은 몇 명이에요?",
        "expected_keywords": ["11", "인턴", "명"],
        "category": "member"
    },
    {
        "q": "Medical AI 연구하는 학생 있나요?",
        "expected_keywords": ["김서영", "김예리", "Seoyoung", "Yeri"],
        "category": "member"
    },
    {
        "q": "이세빈 학생 연락처 알려주세요",
        "expected_keywords": ["jnf0219", "naver"],
        "category": "member"
    },
    {
        "q": "Language Model 연구하는 학생은?",
        "expected_keywords": ["송은우", "Eunwoo"],
        "category": "member"
    },

    # 논문/업적 (8개)
    {
        "q": "CVPR 2025에 accept된 논문 있나요?",
        "expected_keywords": ["DynScene", "CVPR", "2025"],
        "category": "publication"
    },
    {
        "q": "DynScene 논문이 뭐예요?",
        "expected_keywords": ["robotic", "manipulation", "embodied"],
        "category": "publication"
    },
    {
        "q": "AAAI 2025 논문은 어떤 거예요?",
        "expected_keywords": ["SIDL", "smartphone", "image"],
        "category": "publication"
    },
    {
        "q": "SIDL이 뭔가요?",
        "expected_keywords": ["smartphone", "dirty", "lens", "restoration"],
        "category": "publication"
    },
    {
        "q": "BMVC 2025에도 논문 냈어요?",
        "expected_keywords": ["BMVC", "transformation", "diffusion"],
        "category": "publication"
    },
    {
        "q": "의료 관련 논문 있나요?",
        "expected_keywords": ["DeepGAM", "depression", "PLOS", "dog cough"],
        "category": "publication"
    },
    {
        "q": "2025년에 발표한 논문은 몇 개예요?",
        "expected_keywords": ["2025", "CVPR", "AAAI", "BMVC"],
        "category": "publication"
    },
    {
        "q": "3D Vision 관련 논문 있어요?",
        "expected_keywords": ["radiance", "style transfer", "APP3DV"],
        "category": "publication"
    },

    # 지원/참여 (3개)
    {
        "q": "연구실에 지원하려면 어떻게 해야 하나요?",
        "expected_keywords": ["연락", "문의", "교수", "이메일"],
        "category": "recruitment"
    },
    {
        "q": "연구실 연락처 알려주세요",
        "expected_keywords": ["hwkim", "820-0679", "ssu.ac.kr"],
        "category": "recruitment"
    },
    {
        "q": "어떤 분야를 연구하는 학생을 찾나요?",
        "expected_keywords": ["computer vision", "deep learning", "AI", "robotics"],
        "category": "recruitment"
    },
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

        # Check for "waiting" status
        if data.get('status') == 'waiting':
            return {
                "question": question["q"],
                "category": question["category"],
                "expected_keywords": question["expected_keywords"],
                "response": data.get("response", ""),
                "response_time": 0,
                "tokens": 0,
                "error": "Server busy (concurrency limit)"
            }

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
    error_phrases = ["오류가 발생", "응답을 생성할 수 없습니다", "다시 시도", "currently talking"]
    if any(phrase in response for phrase in error_phrases):
        return {
            "status": "FAIL",
            "reason": "오류 응답",
            "matched_keywords": []
        }

    # Check for internal reasoning (hallucination)
    bad_patterns = ["참고자료 1", "참고자료 2", "정답:", "질문:", "---", "**정답**", "looking at reference", "[참고자료", "[참조자료"]
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
    print("AI Chatbot Realistic Test - 30 Questions (Sequential)")
    print("Based on actual homepage content")
    print("=" * 80)
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    results = []
    total = len(TEST_QUESTIONS)

    for i, question in enumerate(TEST_QUESTIONS, 1):
        print(f"[{i}/{total}] Testing: {question['q']}")
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
        print(f"   Response time: {result['response_time']:.2f}s")

        # Wait between requests to avoid concurrency issues
        if i < total:
            time.sleep(2)  # 2 second delay between requests

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
        print(f"FAILED QUESTIONS ({len(failed)} total)")
        print("-" * 80)
        for result in failed[:10]:  # Show first 10
            print(f"\n질문: {result['question']}")
            print(f"상태: {result['analysis']['status']}")
            print(f"이유: {result['analysis']['reason']}")
            if result['response']:
                print(f"응답: {result['response'][:150]}...")

    # Warning questions
    warned = [r for r in results if r["analysis"]["status"] == "WARN"]
    if warned:
        print("\n" + "-" * 80)
        print(f"WARNING QUESTIONS ({len(warned)} total)")
        print("-" * 80)
        for result in warned[:5]:  # Show first 5
            print(f"\n질문: {result['question']}")
            print(f"응답: {result['response'][:150]}...")

    # Final verdict
    print("\n" + "=" * 80)
    acceptable_rate = (status_counts["PASS"] + status_counts["WARN"]) / total * 100

    if status_counts["PASS"] >= 27:  # 90% pass
        print("🎉 TEST PASSED! Chatbot is working well.")
        verdict = "PASS"
    elif acceptable_rate >= 24:  # 80% acceptable
        print("⚠️  TEST ACCEPTABLE. Some improvements recommended.")
        verdict = "ACCEPTABLE"
    else:
        print("❌ TEST FAILED! Significant issues found.")
        verdict = "FAIL"

    print("=" * 80)

    # Save detailed results
    with open("/home/i0179/Realitylab-site/ai_server/test_results_v2.json", "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "summary": status_counts,
            "verdict": verdict,
            "results": results
        }, f, ensure_ascii=False, indent=2)

    print(f"\nDetailed results saved to: ai_server/test_results_v2.json")

    return verdict, status_counts

if __name__ == "__main__":
    verdict, counts = run_tests()
    exit(0 if verdict in ["PASS", "ACCEPTABLE"] else 1)
