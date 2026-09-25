# Modu Math (모두의 수학)

초등 수학 문제의 저작, 컴파일, 렌더링, 웹 검수 및 모바일 풀이까지 전 과정을 아우르는 오픈소스 멀티모달 수학 학습 플랫폼입니다.

---

## 📌 프로젝트 개요 및 현재 진행 현황 (Current Status)

`modu_math`는 종이 교재 및 이미지(PNG) 형태의 수학 문제를 고도화된 정형 데이터(DSL & JSON 계약)로 변환하고, 이를 웹 에디터와 크로스 플랫폼(Flutter) 모바일 앱을 통해 학생들에게 인터랙티브하게 전달하는 모노레포 프로젝트입니다.

### 핵심 구성요소 및 진행 현황

| 구성 요소 | 위치 | 기술 스택 | 현재 구현 및 진행 상태 |
| :--- | :--- | :--- | :--- |
| **Core DSL & Compiler** | `src/modu_math/` | Python 3.12, libcst, jsonschema | **완료/안정화**<br>• Canonical 파이프라인 구축 (`PNG` → `DSL` → `semantic/solvable/layout/renderer JSON` → `SVG`)<br>• 빈칸/선택지/연산 세로셈(Columnar)/사다리타기/OX 판정/선택지 그룹 등 다양한 수학 UI 지원<br>• Vision LLM 보조 저작 도구 (`tools/generate_vision_draft.py` 등)<br>• 배치 및 실시간 감시 빌더 (`mb.bat`, `mw.bat`, `mb_all.bat`) |
| **Web Backend & Learning API** | `src/modu_math_web/` | Django 4.2+, DRF, PostgreSQL, SQLite | **완료/안정화**<br>• 문제 카탈로그 API (`/api/v1/problems/`) 및 다국어 필터링<br>• 학생 풀이 세션, 제출 채점 및 학습 로그 기록 (`/api/v1/attempts/`)<br>• 단원/개념별 숙련도(Mastery) 집계 및 통계<br>• 문제 자동 태깅, 진단 및 추천 서비스 (`ProblemTagging`, Diagnostic & Recommendation)<br>• AI 튜터 프록시 엔드포인트 (`/api/v1/tutor/`) |
| **Web Editor (Konva)** | `src/modu_math_web/editor_next/` | React 19, Konva, TypeScript, Vite | **완료/개선 중**<br>• 캔버스 기반 시각적 문제 레이아웃 편집기 (`/editor-konva/`)<br>• 정답 검수 패널 (`AnswerReviewPanel`) 및 다국어 배치 동기화<br>• 텍스트 앵커 조작, 눈금자 라벨 보존, 힌트 편집기<br>• 수채화 캐릭터 아바타 교체 및 레이어 렌더링 |
| **Mobile App** | `apps/mobile/` | Flutter 3.44+, Dart, flutter_dotenv | **완료/고도화 중**<br>• Django REST API 연동 및 오프라인 번들 에셋 fallback 지원<br>• 6개 다국어 지원 (한국어, 영어, 일본어, 크메르어, 우크라이나어, 중국어)<br>• 어린이 친화적 UI: OX 전용 카드, 세로셈 입력 슬롯, 아바타 반응<br>• 음성 안내 (TTS) 및 음성 입력 (STT) 지원 |
| **CI/CD & DevOps** | `.github/workflows/ci.yml`, `compose.yaml` | GitHub Actions, Docker Compose | **구축 완료**<br>• Python 테스트, Web Editor 테스트/타입체크/빌드, Flutter 분석 및 테스트 자동화<br>• Docker Compose (PostgreSQL 16 + Django Gunicorn) 원클릭 환경 |

---

## 🔄 Core Pipeline & Contracts

모든 수학 문제는 사람이 직접 편집 가능한 `problem.dsl.py`를 단일 진실 공급원(SSOT)으로 삼으며, 생성된 JSON/SVG는 직접 수정하지 않고 DSL 빌드를 통해 생성됩니다.

```text
PNG / Vision Draft
        ↓
Python DSL (problem.dsl.py)
        ↓
┌─────────────────┬─────────────────┐
│  semantic JSON  │  solvable JSON  │ (의미 및 풀이 계약: v1.1, v1.2)
└────────┬────────┴─────────────────┘
         ↓
    layout JSON   (위치 및 배치 구조 계약)
         ↓
   renderer JSON  (시각적 렌더링 계약)
         ↓
        SVG       (최종 벡터 그래픽 아티팩트)
```

### 추천 저작 워크플로우 (Vision-Assisted Workflow)

```text
PNG -> vision_draft.md + vision_structured.json -> refined_draft.md -> Python DSL -> Generated Artifacts
```

- `vision_draft.md`: Vision LLM의 원시 시각 관찰 결과
- `vision_structured.json`: 이미지 크기, 대략적인 좌표 박스, 가시 텍스트, 요소 그룹 정보를 담은 보조 JSON
- `refined_draft.md`: DSL 변환에 최적화된 중간 해석 문서
- `problem.dsl.py`: 사람이 편집하고 유지보수하는 공식 저작 원본

---

## 📁 디렉토리 구조 (Directory Structure)

```text
modu_math/
├── apps/
│   └── mobile/                  # Flutter 앱과 ko/uk UI 번역·빌드 결과물
├── src/
│   ├── modu_math/               # 핵심 컴파일러, 파이프라인, 어댑터, 렌더러
│   ├── modu_math_web/           # Django 백엔드
│   │   ├── learning/            # 학습 REST API, 채점, 숙련도, 진단/추천
│   │   ├── editor/              # 레거시 에디터 API 및 상태 관리
│   │   └── editor_next/         # React 19 + Konva 차세대 웹 에디터
│   └── modu_semantic/           # 하위 호환성 래퍼
├── examples/
│   └── problems/
│       └── ko/                  # 한국어 DSL 원본 + 문제별 *.i18n.json
├── schema/                      # semantic, layout, renderer JSON Schema
├── scripts/                     # 모노레포 관리, 빌드 및 동기화 스크립트
├── tools/                       # Vision 드래프트 생성, DSL 변환 보조 도구
├── docs/                        # 아키텍처, 진단 체계, 아바타, 백엔드 가이드
├── compose.yaml                 # PostgreSQL + Django Docker Compose 구성
├── Dockerfile                   # Django 백엔드 컨테이너 빌드 파일
├── pyproject.toml               # Python 의존성 및 프로젝트 메타데이터
└── README.md                    # 본 문서
```

문제 번역은 별도 `locales/` 트리가 아니라 각 한국어 원본 옆의
`*.i18n.json`에서 관리합니다. 한국어 원본과 우크라이나어 차이 데이터가 한
문서에 있으므로 파일 이름 매칭과 중복 동기화가 필요하지 않습니다. 모바일 앱의
메뉴·버튼 번역은 `apps/mobile/assets/i18n/{ko,uk}.json`, 빌드된 문제 데이터는
`apps/mobile/generated/examples/problems/{ko,uk}/`에 위치합니다. 자세한 작업
흐름은 `docs/single_source_localization.md`를 참고하세요.

---

## 🚀 빠른 시작 (Quick Start)

### 1. 사전 요구사항
- **Python**: 3.10 이상 (3.12 권장, `uv` 패키지 관리자 권장)
- **Node.js**: 20 이상 (npm 포함)
- **Flutter**: 3.44 이상
- **Docker & Docker Compose** (선택 사항)

### 2. Python 환경 구축 및 핵심 컴파일러 테스트

```bash
# 의존성 설치
uv sync --extra dev

# Python 핵심 테스트 실행
uv run pytest
```

### 3. DSL 빌드 도구 사용법

문제 ID 또는 DSL 파일 경로를 지정하여 빌드할 수 있습니다:

```bash
# 단일 문제 빌드 (Windows)
mb 0001
# 또는
mb examples\problems\0001\problem.dsl.py

# 파일 변경 감시(Watch) 자동 빌드
mw 0001

# 폴더 내 모든 문제 일괄 빌드
mb_all examples\problems
```

### 4. Django 백엔드 & 학습 API 실행

#### 로컬 SQLite 환경:
```bash
uv run python manage.py migrate
uv run python manage.py sync_problems   # JSON 문제를 DB로 동기화
uv run python manage.py runserver 127.0.0.1:8000
```

#### Docker Compose 환경 (Docker Desktop & PostgreSQL):

1. **Docker Desktop 실행**: 시작 메뉴에서 Docker Desktop을 실행하거나 PowerShell에서 `docker desktop start`를 입력한 뒤 `Engine running` 상태가 될 때까지 대기합니다.
2. **컨테이너 빌드 및 실행**:
   ```powershell
   docker compose up --build -d
   docker compose ps
   ```
3. **문제 데이터베이스 동기화**:
   ```powershell
   docker compose exec web python manage.py sync_problems
   ```
4. **브라우저 접속**:
   - **웹 에디터 (Konva)**: [http://localhost:8000/editor-konva/](http://localhost:8000/editor-konva/) (또는 루트 [http://localhost:8000/](http://localhost:8000/))
   - **레거시 에디터**: [http://localhost:8000/editor/](http://localhost:8000/editor/)
   - **학습 REST API**: [http://localhost:8000/api/v1/](http://localhost:8000/api/v1/)

> **Tip (엔진 오류 시 재시작)**:
> Docker Desktop 실행 후 엔진이 멈춰있다면 `wsl --shutdown` 후 `docker desktop restart`를 수행합니다.

### 5. Web Editor (Konva) 개발

```bash
cd src/modu_math_web/editor_next
npm install
npm run dev        # 로컬 Vite 개발 서버 (포트 5174)
npm run typecheck  # TypeScript 타입 검사
npm run build      # 정적 번들 빌드 -> static/editor_next/konva_assets/
```

### 6. Flutter 모바일 앱 실행

```bash
cd apps/mobile

# 에셋 링크 및 패키지 설치
flutter pub get

# 정적 분석 및 테스트
flutter analyze
flutter test

# 앱 실행 (데스크톱, 에뮬레이터 또는 실기기)
flutter run
```

앱 설정은 `apps/mobile/.env` 파일에서 지정할 수 있습니다:
```dotenv
AI_TUTOR_MODE=backend
BACKEND_API_BASE_URL=http://127.0.0.1:8000
```

---

## 🛠️ 모노레포 관리 및 CI/CD

Windows PowerShell 환경에서 전체 모노레포 검사를 일괄 수행할 수 있습니다:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\modu_monorepo.ps1 -Task check
```

지원 태스크: `setup`, `python-test`, `flutter-analyze`, `flutter-test`, `check`

### GitHub Actions CI (`.github/workflows/ci.yml`)
- **Python**: Python 3.12 환경에서 pytest 실행
- **Web Editor**: Node.js 20 환경에서 타입 체크(`tsc`), 텍스트 인코딩/앵커/정답 검수 단위 테스트 및 프로덕션 빌드
- **Flutter**: Flutter 3.44.8 환경에서 에셋 심볼릭 링크 생성, `flutter analyze` 및 `flutter test` 통과 검증

---

## 📚 추가 참고 문서 (Documentation)

- [백엔드 구조 및 데이터 모델 가이드](file:///c:/projects/modu_math/docs/backend.md)
- [문제 진단 분류 및 추천 체계](file:///c:/projects/modu_math/docs/taxonomy_and_diagnostics.md)
- [수채화 아바타 사양서](file:///c:/projects/modu_math/docs/WATERCOLOR_AVATARS.md)
- [Web Editor Konva 안내](file:///c:/projects/modu_math/src/modu_math_web/editor_next/README.md)
- [Flutter 백엔드 연동 문서](file:///c:/projects/modu_math/apps/mobile/backend/README.md)
