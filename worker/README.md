# 챗봇 백엔드 — Cloudflare Worker

홈페이지 우하단 챗봇과 버그리포트가 실제로 호출하는 서버. **라이브는 여기다.**
(`../ai_server/` 는 이전 세대인 Flask+RAG 서버로, 지금은 쓰이지 않는다.)

- 주소: <https://reality-lab-chatbot.i0179.workers.dev>
- 계정: Cloudflare `i0179` / workers.dev 서브도메인 `i0179`
- 무료 티어. **PC 가 켜져 있을 필요가 없다.**

전 세대에서는 이 PC 가 Flask 서버를 띄우고 Cloudflare quick tunnel 로 노출했는데,
quick tunnel 은 뜰 때마다 주소가 바뀌어서 그때마다 사이트에 새 주소를 커밋해야 했고,
반영되는 2~4분 동안 챗봇이 502 였다. Worker 로 옮기면서 주소가 고정됐다.

---

## 지식은 번들되어 있지 않다

Worker 는 기동 시 사이트에서 지식을 가져온다:

```
_data/*.yml  ──(Jekyll)──►  https://reality.ssu.ac.kr/assets/data/kb.json  ──(fetch)──►  Worker
```

`assets/data/kb.json` 은 Jekyll 템플릿(`permalink: /assets/data/kb.json`)이라, `_data/` 를
고쳐서 push 하면 사이트와 함께 발행된다. Worker 는 이를 10분 캐시한다.

> **그래서 멤버·논문·뉴스를 고쳤을 때 Worker 를 재배포할 필요가 없다.** push 만 하면 된다.
> 재배포가 필요한 건 이 폴더의 코드나 `wrangler.toml` 을 바꿨을 때뿐이다.

임베딩/RAG 는 쓰지 않는다. 지식 전체(약 8k 토큰)를 그대로 프롬프트에 넣는다
(`gpt-5.6-luna` 는 컨텍스트가 넉넉하다). 질문당 비용 약 2원.

---

## 배포

```bash
cd worker
npx wrangler deploy
```

OpenAI 키는 저장소에 두지 않는다. Cloudflare 에 보관:

```bash
npx wrangler secret put OPENAI_API_KEY
```

처음 세팅할 때 하루 할당량용 KV 네임스페이스가 필요하다(이미 만들어져 있다):

```bash
npx wrangler kv namespace create RL     # 출력된 id 를 wrangler.toml 에 적는다
```

> `npx wrangler login` 이 "state mismatch" 로 실패하면, 이전 로그인 시도의 node 프로세스가
> 콜백 포트를 잡고 있는 경우다. 그 프로세스를 죽이고 다시 하면 된다.

---

## 설정 (`wrangler.toml`)

| 변수 | 지금 값 | 뜻 |
|---|---|---|
| `KB_URL` | 사이트의 kb.json | 지식 출처 |
| `OPENAI_MODEL` | `gpt-5.6-luna` | 생성 모델 |
| `RATE_LIMIT_PER_DAY` | `15` | 방문자(IP)당 하루 질문 수 |
| `RATE_LIMIT_GLOBAL_PER_MIN` | `60` | 전체 분당 상한 |
| `REST_WINDOW` | `1` | 04:00–08:00 KST 휴식. `0` 이면 24시간 응답 |

하루 할당량은 KV 에 `rl:<KST날짜>:<IP>` 로 기록되어 **매일 자정(KST)에 자동 리셋**된다.
방문자 IP 는 `CF-Connecting-IP` 로 본다. 한도를 넘기면 OpenAI 를 **호출하지 않고**(토큰 0)
"내일 다시 찾아와달라"는 안내를 돌려준다.

---

## 엔드포인트

| 경로 | 용도 |
|---|---|
| `GET /health` | 모델·지식 적재·할당량 상태 |
| `GET /heartbeat` | 살아있는지만 |
| `POST /chat` | 한 번에 답변 |
| `POST /chat/stream` | SSE 스트리밍 (사이트가 쓰는 쪽) |

```bash
curl -s https://reality-lab-chatbot.i0179.workers.dev/health
curl -s -X POST https://reality-lab-chatbot.i0179.workers.dev/chat \
     -H 'Content-Type: application/json' -d '{"question":"연구실 위치가 어디인가요?"}'
```

---

## 알아둘 것

- **`worker/` 는 `_config.yml` 의 `exclude` 에 있다.** 빼면 Jekyll 이 이 폴더를 빌드하려 든다.
- **사이트가 보는 주소**는 `_includes/chatbot.html` 과 `_includes/bug-report.html` 의
  `DIRECT_AI_SERVER_URL`. 둘 다 같이 고쳐야 한다.
- **`tunnel_watchdog.ps1 -Service chatbot` 은 즉시 종료하도록 막아뒀다.** 이 가드를 풀면
  quick tunnel 이 떠서 위 주소를 임시 터널 주소로 덮어쓰고, 챗봇이 PC 의존으로 되돌아간다.
  (`-Service admin` 은 관리자 CMS 용이라 **계속 필요하다.**)
- 멤버 명단 같은 건 `chatbot_knowledge.yml` 에 적지 말 것. 고정 명단은 반드시 낡는다.
  명단은 `_data/members.yml` 하나가 출처다.
