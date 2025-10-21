# User Questions

이 폴더에는 웹사이트 챗봇에서 사용자가 제출한 질문들이 저장됩니다.

## 파일 형식
- `question_YYYYMMDD_HHMMSS_####.json`

## JSON 구조
```json
{
  "id": 1234,
  "timestamp": "2025-10-22 02:56:30",
  "question": "사용자가 입력한 질문",
  "censored_question": "욕설이 검열된 질문",
  "has_profanity": false,
  "status": "pending"
}
```

## 처리 방법
1. 질문 확인
2. `_data/vector_db/documents.json`에 답변 추가
3. 파일의 `status`를 `"answered"`로 변경 또는 파일 삭제
