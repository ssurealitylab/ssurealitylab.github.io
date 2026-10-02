# 인수인계 — 이 문서 하나로 시작할 수 있게

숭실대 Reality Lab 홈페이지(<https://reality.ssu.ac.kr>). 이 문서는 **처음 온 사람(또는 새 Claude)이
한 번 읽고 바로 작업할 수 있게** 쓴 것이다. 더 깊은 내용은 각 절 끝의 링크로 넘긴다.

---

## 1. 라이브 구성 — 지금 무엇이 어디서 도는가

```
방문자
  │
  ├── 정적 사이트 ──────► GitHub Pages (저장소 main 브랜치를 직접 빌드)
  │                        Jekyll. 이 저장소의 _data/, _includes/, *.md 가 전부.
  │                        PC 꺼져 있어도 돌아간다.
  │
  ├── 챗봇 (우하단) ────► Cloudflare Worker  (worker/)
  │                        https://reality-lab-chatbot.i0179.workers.dev
  │                        PC 불필요. 지식은 사이트의 kb.json 을 긁어온다.
  │
  └── /admin.html ─────► 이 PC 의 Flask CMS + Cloudflare 터널
                           ★ 유일하게 PC 가 켜져 있어야 하는 것 ★
```

**핵심 한 줄**: 사이트와 챗봇은 PC와 무관하게 돈다. **관리자 CMS만 PC가 필요하다.**

`ai_server/` 는 **옛 챗봇 백엔드**(Flask + 로컬 RAG)다. 2026-08 에 Worker 로 이전해서
**지금은 라이브가 아니다.** 참고용으로 남겨둔 것이니, 챗봇을 고칠 일이 생기면 `worker/` 를 봐야 한다.

---

## 2. 배포 — `main` 에 push 하면 그게 배포다

GitHub Actions 워크플로는 없다. GitHub Pages 가 `main` 을 직접 빌드한다.

```bash
git push origin main      # 1~8분 뒤 라이브 반영
```

반영 확인은 추측하지 말고 실제로 받아서 볼 것:

```bash
curl -s "https://reality.ssu.ac.kr/students.html?cb=$(date +%s)" | grep -c '찾는내용'
curl -sI "https://reality.ssu.ac.kr/students.html" | grep -i last-modified
```

> 사용자는 **묻지 말고 바로 push** 하기를 원한다(비밀파일만 확인하고). 단 push 전에 로컬 빌드로
> 검증할 것 — 아래 4절.

---

## 3. 콘텐츠는 전부 `_data/*.yml`

| 파일 | 나타나는 곳 | 주의 |
|---|---|---|
| `members.yml` | students.html, alumni.html, 챗봇 | 아래 3-1 |
| `publications.yml` | 논문 **모달**, 홈 최신논문 | ★ 3-2 함정 |
| `news.yml` | news.html, 홈 | 파일 순서대로 출력(정렬 안 함). 홈은 위 4개 |
| `chatbot_knowledge.yml` | 챗봇 지식(연구실 소개/위치/Q&A) | 멤버 명단은 여기 두지 말 것(3-1) |

### 3-1. 멤버 — 등록일은 자동으로 기록된다

멤버를 추가하면 `joined`(등록 연월)가 자동으로 찍힌다. 알룸나이로 보낼 때 `period`(활동 기간)의
시작일이 여기서 나온다. 예전엔 이 기록이 없어서 알룸나이 전환 때 기간을 비워둬야 했다.

```bash
python scripts/members_joined.py              # joined 없는 사람에게 기록 (git 이력에서 등록일 추출)
python scripts/members_joined.py --retire "Subin Kang"   # 알룸나이로 이동 + period 자동 계산
```

등록일의 근거는 **git 이력**이다 — 그 이름이 `members.yml` 에 처음 들어간 커밋. 이름 표기가
바뀐 경우(Kho→Koh)를 대비해 영문·한글 이름을 **둘 다** 검색한다. 관리자 CMS 로 추가해도
`joined` 가 찍힌다(`admin_cms/admin_server.py` 의 `stamp_joined`).

멤버 명단은 `members.yml` **한 곳**에만 둔다. 예전엔 `chatbot_knowledge.yml` 에도 고정 명단이
있어서 이미 나간 사람이 계속 현재 멤버로 표시됐다. 지금은 챗봇 쪽도 빌드 시점에 `members.yml`
에서 생성한다(`_includes/chatbot.html` 의 `knowledgeBase.team_members`).

### 3-2. ★ 논문 추가 시 가장 많이 틀리는 지점

`publications.yml` 에 넣으면 **모달만** 생긴다. **International 페이지의 목록 카드는
`international.md` 에 손으로 추가해야 한다.** 안 하면 "분명히 추가했는데 목록에 안 보인다"가 된다.
국내는 `domestic.md`. 인용(citation)은 비워두면 자동 생성된다(`_includes/publication_modals.html`).

---

## 4. 로컬에서 빌드·검증하기 (Windows)

```bash
export PATH="/c/Ruby33-x64/bin:$PATH"
export BUNDLE_PATH="$HOME/Desktop/RS/gems-win"
bundle exec jekyll build          # 결과는 _site/
grep -c '확인할내용' _site/students.html
```

- Ruby 는 **RubyInstaller(MSYS2 포함)** 를 써야 한다. conda ruby 는 mswin 빌드라
  `commonmarker`/`eventmachine` 컴파일이 실패한다.
- `BUNDLE_PATH` 는 **저장소 바깥**(`Desktop/RS/gems-win`)에 둔다. 저장소 안에 두면 Jekyll 이
  gem 안의 템플릿을 파싱하다 빌드가 깨진다.
- Python 은 conda env `RS`: `C:/Users/USER/anaconda3/envs/RS/python.exe`.
  `conda run` 은 여러 줄 스크립트를 망가뜨리고 비 cp949 출력에서 죽으니 **직접 호출**할 것.
- 콘솔이 cp949 라 한글/이모지 출력이 깨지거나 예외가 난다. 스크립트 출력은 파일로 쓰고 읽는 게 안전하다.

---

## 5. 챗봇 (Cloudflare Worker)

자세한 건 **[`worker/README.md`](worker/README.md)**. 요점만:

- 지식은 Worker 에 번들되어 있지 않다. 사이트가 발행하는 `assets/data/kb.json`
  (Jekyll 이 `_data/` 를 jsonify) 을 가져다 쓴다 → **콘텐츠만 고쳐 push 하면 챗봇도 최신**이 된다.
  Worker 재배포 불필요.
- 모델 `gpt-5.6-luna`, 질문당 약 2원. 하루 IP당 15회(Workers KV).
- Worker 코드/설정을 바꿨을 때만: `cd worker && npx wrangler deploy`
- 사이트가 보는 주소는 `_includes/chatbot.html`, `_includes/bug-report.html` 의
  `DIRECT_AI_SERVER_URL`.

---

## 6. 관리자 CMS — 유일하게 PC가 필요한 부분

`admin_cms/` (Flask). `_data/*.yml` 을 웹에서 편집하고, 백업·검증 후 **직접 커밋·push** 한다.
`reality.ssu.ac.kr/admin.html` 은 터널 주소로 보내는 리다이렉트일 뿐이고, 그 주소는 바뀔 때마다
저장소에 자동 커밋된다.

- 작업 스케줄러: `RealityLab-Admin`, `RealityLab-AdminTunnel` → **계속 돌아야 한다.**
- `RealityLab-Chatbot`, `RealityLab-Tunnel` → 챗봇이 Worker 로 가면서 **필요 없어졌다.**
  `tunnel_watchdog.ps1 -Service chatbot` 은 즉시 종료하도록 막아뒀다. 이 가드를 풀면
  quick tunnel 이 떠서 `chatbot.html` 의 Worker 주소를 임시 터널 주소로 덮어쓴다.

---

## 7. 알아두면 시간 아끼는 함정

- **"캐시겠지"로 넘기지 말 것.** 반영이 안 보이면 실제로 받아서 확인한다(2절). 과거에 캐시로
  오진했다가 실제 원인(CSS)이 따로 있던 적이 있다.
- **grep 으로 검증할 때 주석에 속지 말 것.** `grep -c '[W9]'` 가 HTML 주석까지 세서 잘못된
  확신을 준 적이 있다. 여러 줄 패턴은 Python 으로 확인한다.
- **YAML 을 스크립트로 수정할 때**는 마지막 항목의 개행을 잃기 쉽다. 수정 후 반드시
  `yaml.safe_load` 로 파싱하고, **건드리지 않은 항목이 그대로인지**까지 단언(assert)할 것.
  (실제로 이것 때문에 members.yml 이 깨진 적 있다.)
- **CMS 가 쓴 YAML 항목은 키 순서가 다르다**(알파벳순). `- name:` 이 첫 줄이라고 가정하는 코드는
  그런 항목을 놓친다.
- **`.env` 는 BOM 없이 저장.** PowerShell `Set-Content -Encoding utf8` 은 BOM 을 붙이고,
  python-dotenv 가 첫 줄 키를 못 읽는다.
- 그 밖의 함정은 **[`dev/cheatsheet.md`](dev/cheatsheet.md)** 에 모아뒀다
  (한글 파일명, 로컬 Jekyll 이 프로덕션 챗봇에 붙는 문제, 포트 충돌 등).
  단, 그 문서의 챗봇 관련 항목은 **Worker 이전 이전(以前) 기준**이라 지금과 다를 수 있다.

---

## 8. 더 읽을 것

| 문서 | 내용 |
|---|---|
| [`README.md`](README.md) | 저장소 개요·구조 |
| [`worker/README.md`](worker/README.md) | 라이브 챗봇 (Worker) |
| [`dev/DEVELOPMENT.md`](dev/DEVELOPMENT.md) | 개발 환경·시나리오별 워크플로 |
| [`dev/cheatsheet.md`](dev/cheatsheet.md) | 명령어·함정 모음 |
| [`admin_cms/README.md`](admin_cms/README.md) | 관리자 CMS |
| [`_data/README_PUBLICATIONS.md`](_data/README_PUBLICATIONS.md) | 논문 데이터 형식 |
| [`ai_server/README.md`](ai_server/README.md) | 옛 챗봇 백엔드 (**라이브 아님**) |
