# 자동 빌드 Workflow 설정 가이드

## 📌 중요 안내
GitHub Personal Access Token에 `workflow` 권한이 없어 자동으로 workflow 파일을 생성할 수 없습니다.
아래 방법으로 수동으로 설정해주세요.

## 🚀 설정 방법

### 1단계: GitHub 웹사이트에서 Workflow 파일 생성
1. https://github.com/ssurealitylab/Realitylab-site 접속
2. `.github/workflows/` 디렉토리로 이동
3. **Add file** → **Create new file** 클릭
4. 파일명: `auto-build.yml`
5. 아래 내용 복사 붙여넣기

### 2단계: Workflow 파일 내용

```yaml
name: Auto Build and Deploy

on:
  schedule:
    - cron: '0 0 1,15 * *'  # 매월 1일, 15일 00:00 UTC
  workflow_dispatch:  # 수동 실행 가능
  push:
    branches:
      - main

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Ruby
        uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.1'
          bundler-cache: true

      - name: Setup Pages
        id: pages
        uses: actions/configure-pages@v4

      - name: Build with Jekyll
        run: bundle exec jekyll build --baseurl "${{ steps.pages.outputs.base_path }}"
        env:
          JEKYLL_ENV: production

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

### 3단계: GitHub Pages 활성화
1. 저장소 → **Settings** → **Pages**
2. **Source**: "**GitHub Actions**" 선택
3. Save

### 4단계: 파일 정리
설정 완료 후 이 가이드 파일을 삭제해도 됩니다:
```bash
git rm WORKFLOW_SETUP.md
git commit -m "Remove workflow setup guide"
git push
```

## ✅ 완료 후 기능

- 📅 **자동 빌드**: 매월 1일, 15일 00:00 UTC
- 🚀 **푸시 시 빌드**: main 브랜치 푸시할 때마다
- 🔧 **수동 실행**: GitHub Actions 탭에서 가능
- 🔄 **자동 배포**: GitHub Pages에 자동 배포

---

💡 **참고**: yml 파일 업데이트만으로 학생 achievements가 자동으로 반영됩니다!
