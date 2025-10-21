# Publications 관리 가이드

## 개요
이제 모든 publication 데이터는 `_data/publications.yml` 파일 하나에서 관리됩니다. 이 파일에 새 논문을 추가하면 자동으로 다음 위치에 반영됩니다:

1. **홈페이지** - Latest Publications 섹션 (최신 6개)
2. **홈페이지** - Latest Publications (With Images) 섹션 (최신 6개)
3. **홈페이지** - Publication 모달 (클릭 시 팝업)

## 새 Publication 추가하기

### 1단계: publications.yml 파일 열기
파일 경로: `_data/publications.yml`

### 2단계: 새 Publication 데이터 추가
파일 **맨 위**에 다음 형식으로 추가하세요 (최신 논문이 맨 위에 오도록):

```yaml
  - id: c25                    # 고유 ID (conference는 c, journal은 j)
    title: "논문 제목"           # 논문 전체 제목
    authors: "저자1, 저자2, 저자3"  # 저자 목록
    venue: "학회/저널 전체 이름"    # 예: IEEE Conference on Computer Vision
    venue_short: "CVPR25"      # 짧은 이름 (배지에 표시됨)
    year: 2025                 # 출판 연도
    type: conference           # conference 또는 journal
    status: accepted           # accepted, published, submitted 등
    citation: "[C25] 전체 citation 텍스트..."  # 인용 형식
    image: "img/publications/cvpr2025.jpg"     # Architecture 이미지 경로
    notes: "* Equal contribution"              # 각주 (선택사항)
    links:                     # 외부 링크 (선택사항)
      pdf: "https://..."       # PDF 링크
      website: "https://..."   # 프로젝트 웹사이트
      github: "https://..."    # GitHub 저장소
    badge_style: challenge-badge  # 배지 스타일 (선택사항)
```

### 3단계: Architecture 이미지 준비
- Architecture 이미지를 `img/publications/` 폴더에 저장
- 파일명 예시: `cvpr2025.jpg`, `iccv2025.png` 등
- `image` 필드에 경로 지정

### 4단계: Jekyll 빌드
```bash
cd /home/i0179/Realitylab-site
bundle exec jekyll build
```

### 5단계: Git에 커밋
```bash
git add _data/publications.yml img/publications/your_new_image.jpg
git commit -m "Add new publication: [논문 제목]"
git push
```

## 예시

### Conference Paper 추가 예시
```yaml
  - id: c26
    title: "Advanced Vision Transformer for 3D Scene Understanding"
    authors: "John Doe*, Jane Smith*, Heewon Kim"
    venue: "IEEE/CVF International Conference on Computer Vision (ICCV)"
    venue_short: "ICCV25"
    year: 2025
    type: conference
    status: accepted
    citation: "[C26] John Doe*, Jane Smith*, and Heewon Kim, \"Advanced Vision Transformer for 3D Scene Understanding,\" Proc. IEEE/CVF International Conference on Computer Vision (ICCV), 2025 (accepted)"
    image: "img/publications/iccv2025.jpg"
    notes: "* Equal contribution"
    links:
      pdf: "https://arxiv.org/pdf/xxxxx"
      website: "https://project-website.com"
      github: "https://github.com/realitylab/project"
```

### Journal Paper 추가 예시
```yaml
  - id: j13
    title: "Deep Learning Approach for Medical Image Analysis"
    authors: "Alice Lee†, Bob Kim†, Heewon Kim"
    venue: "Nature Machine Intelligence"
    venue_short: "Nature MI"
    year: 2025
    type: journal
    status: published
    citation: "[J13] Alice Lee†, Bob Kim†, and Heewon Kim, \"Deep Learning Approach for Medical Image Analysis,\" Nature Machine Intelligence, vol. 10, no. 5, pp. 123-145, 2025"
    image: "img/publications/nature_mi_2025.jpg"
    notes: "† Undergraduate student"
    links:
      pdf: "https://www.nature.com/articles/xxxxx"
```

## 필드 설명

### 필수 필드
- `id`: 고유 식별자 (중복 불가)
- `title`: 논문 제목
- `authors`: 저자 목록
- `venue`: 학회/저널 이름
- `venue_short`: 배지에 표시될 짧은 이름
- `year`: 출판 연도
- `type`: conference 또는 journal
- `citation`: 전체 인용 텍스트
- `image`: Architecture 이미지 경로

### 선택 필드
- `status`: accepted, published, submitted, in press 등
- `notes`: 각주 (Equal contribution, Undergraduate student 등)
- `links`: 외부 링크 (pdf, website, github, video 등)
- `badge_style`: 특별한 배지 스타일 (예: challenge-badge)

## 자동 반영 위치

### 1. 홈페이지 Latest Publications (리스트 형태)
- 파일: `_includes/latest_publications.html`
- 자동으로 최신 6개 표시
- 수동 편집 불필요

### 2. 홈페이지 Latest Publications (이미지 카드)
- 파일: `_includes/latest_publications.html`
- 자동으로 최신 6개 표시
- Architecture 이미지 포함

### 3. Publication 모달
- 파일: `_includes/home_publication_modals.html`
- 클릭 시 팝업으로 표시
- Architecture 이미지 + Citation 정보

## 주의사항

1. **최신 논문을 맨 위에 추가**: 파일 맨 위에 추가해야 Latest Publications에 표시됩니다
2. **ID 중복 방지**: 각 publication의 `id`는 고유해야 합니다
3. **YAML 형식 준수**: 들여쓰기와 형식을 정확히 지켜야 합니다
4. **이미지 경로 확인**: Architecture 이미지가 올바른 경로에 있는지 확인하세요
5. **빌드 후 확인**: Jekyll 빌드 후 에러가 없는지 확인하세요

## 문제 해결

### Jekyll 빌드 에러 발생 시
```bash
# YAML 형식 오류 확인
bundle exec jekyll build --trace
```

### Publication이 표시되지 않을 때
1. `_data/publications.yml` 파일 저장 확인
2. Jekyll 빌드 실행 확인
3. 브라우저 캐시 삭제 후 새로고침

## 팁

- 홈페이지에는 최신 6개만 표시되므로, 가장 중요한 논문을 맨 위에 배치하세요
- Architecture 이미지는 가로 비율 이미지가 권장됩니다
- Links는 선택사항이므로, PDF나 웹사이트가 없어도 됩니다
