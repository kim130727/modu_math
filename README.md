# modu-semantic

`modu-semantic`은 수학 문제/도형을 Python으로 정의하고, semantic JSON을 중심 계약으로 내보내는 라이브러리입니다.

## 핵심 방향

- 겉보기 API는 단순하게: `Problem`, `Rect`, `Text` 등 바로 import
- semantic JSON을 canonical contract로 고정
- SVG는 렌더러 중 하나로 유지

## Canonical Contract (v3/v1)

기준 문서의 우선순위는 다음과 같습니다.

1. `schema/contract/semantic_v3.schema.json`
2. `schema/contract/layout_v1.schema.json`
3. `schema/contract/layout_diff_v1.schema.json`
4. `schema/contract/canonical_order_profile.json`

### semantic top-level 필수 키

- `schema_version` (`modu_math.semantic.v3`)
- `render_contract_version` (`modu_math.render.v1`)
- `problem_id`
- `problem_type`
- `metadata`
- `domain`
- `render`
- `answer`
- `title`은 optional

### semantic 블록 위치 규약

- `metadata`, `domain`, `render`, `answer`는 항상 root 바로 아래에 둡니다.
- `render` 내부는 `canvas`, `elements` 순서입니다.
- `answer` 내부는 `blanks`, `choices`, `answer_key` 순서입니다.

### 좌표/요소 기준

- 모든 좌표는 `render.canvas` 기준 절대 좌표입니다.
- `Region` 헬퍼(`inset`, `split_rows/split_cols`, `split_v/split_h`)가 반환하는 자식 `Region`의 `x/y`도 항상 canvas 절대 좌표입니다.
- 공통 요소 필드 이름은 snake_case 정식 표기를 사용합니다.
  - 예: `semantic_role`, `z_index`, `stroke_width`, `font_family`, `font_size`, `font_weight`
- canonical element type
  - `rect`, `circle`, `line`, `polygon`, `text`, `formula`
- 텍스트 콘텐츠 필드 규약
  - `Text`는 `text`
  - `Formula`는 `expr` (legacy 입력의 `text`는 normalize 단계에서 `expr`로 매핑)

### canonical key order

- semantic/layout/layout_diff root key 순서는 반드시 `schema/contract/canonical_order_profile.json`을 따릅니다.
- 저장 경로(`Problem.save()`/bundle)는 normalize -> canonical order -> validate 파이프라인으로 출력됩니다.

## 빠른 시작

```python
from modu_semantic import Problem, Rect, Text

p = Problem(width=800, height=600, problem_id="demo_001")
p.add(Rect(id="box", x=100, y=100, width=200, height=100))
p.add(Text(id="label", x=120, y=160, text="Hello modu"))

p.save("out/demo")
```

생성 결과:

- `out/demo.semantic.json`
- `out/demo.layout.json`
- `out/demo.svg`

## CLI

```bash
modu build examples/01_basic_rect_text.py -o out/basic_rect_text
```

입력 파일은 `build() -> Problem` 함수를 정의해야 합니다.

`semantic.json`에서 바로 DSL build를 재생성하려면:

```bash
modu build-semantic examples/korea_elementary/3rd_addition_subtraction_0001/output/json/3rd_addition_subtraction_0001.semantic.json -o out/from_semantic/3rd_addition_subtraction_0001 --emit-py out/from_semantic/3rd_addition_subtraction_0001.generated.py
```

생성 결과:

- `out/from_semantic/3rd_addition_subtraction_0001.semantic.json`
- `out/from_semantic/3rd_addition_subtraction_0001.layout.json`
- `out/from_semantic/3rd_addition_subtraction_0001.svg`
- `out/from_semantic/3rd_addition_subtraction_0001.generated.py`

## RAG 보조 파이프라인 (Opt-in)

기존 성공 예제를 검색해 few-shot prompt를 조립하고, 생성 DSL을 로컬 build/validate로 확인하는 보조 흐름입니다.
모델 자동 학습이 아니라 retrieval + reuse + validation 구조입니다.

```bash
python tools/build_rag_index.py
python tools/run_rag_generation.py --meta-json "{\"problem_type\":\"geometry\",\"tags\":[\"triangle\"],\"visual_primitives\":[\"polygon\",\"text\"]}"
```

이미지 입력 기반으로 시작할 수도 있습니다.

```bash
python tools/run_rag_generation.py --image-path examples/problem/0017/input/0017.png --persist-output
```

동작 규칙:

- `--image-path`가 있으면 파일명 + 기존 `index.jsonl` 기반으로 `input_meta`를 자동 추천합니다.
- OCR 환경(Pillow + pytesseract + tesseract 실행파일)이 있으면 텍스트/박스 추출을 추가 태그로 반영합니다.
- OCR이 없어도 파이프라인은 계속 진행됩니다. (retrieval + prompt + validate)
- OCR을 강제로 끄려면 `--disable-ocr`를 사용합니다.

OCR 설치(Windows 예시):

```bash
winget install -e --id tesseract-ocr.tesseract
python -m pip install pytesseract pillow
```

정상 OCR 확인 기준:

- 실행 로그에 `ocr_status: ok`
- `examples/problem/_rag/runs.jsonl` 마지막 run의 `input_meta`에 `ocr_available: true`
- 같은 `input_meta`에 `ocr_text_lines`, `ocr_boxes`가 채워짐

출력을 실제 파일로 남기려면 `--persist-output`을 사용합니다.

```bash
python tools/run_rag_generation.py --meta-path examples/problem/_rag/input_meta.sample.json --persist-output
```

가독성 개선:

- 기본 파일명 prefix는 `problem_id`를 사용합니다. (없으면 `run_id`)
- `problem_id`가 있으면 `latest` 별칭도 함께 갱신됩니다.
  - 예: `0016.latest.generated.py`, `0016.latest.prompt.txt`
  - `--persist-output` 사용 시 `0016.latest.semantic.json`, `0016.latest.layout.json`, `0016.latest.svg`
- 필요하면 `--artifact-prefix my_name`으로 직접 지정할 수 있습니다.

생성 산출물:

- `examples/problem/_rag/index.jsonl`
- `examples/problem/_rag/runs.jsonl`
- `examples/problem/_rag/generated/<prefix>.prompt.txt`
- `examples/problem/_rag/generated/<prefix>.generated.py`
- (`--persist-output` 사용 시) `examples/problem/_rag/generated/<prefix>_built.semantic.json`
- (`--persist-output` 사용 시) `examples/problem/_rag/generated/<prefix>_built.layout.json`
- (`--persist-output` 사용 시) `examples/problem/_rag/generated/<prefix>_built.svg`

정리 팁:

- 실패 run에서 나온 생성 파일만 정리(기본 dry-run):
  - `python tools/cleanup_rag_generated.py --delete-failed`
- 실제 삭제:
  - `python tools/cleanup_rag_generated.py --delete-failed --apply`

## 패키지 구조

- `src/modu_semantic/__init__.py`: 공개 API
- `src/modu_semantic/problem.py`: 사용자 진입점 모델
- `src/modu_semantic/primitives.py`: 기본 요소
- `src/modu_semantic/groups.py`: 그룹 모델
- `src/modu_semantic/regions.py`: 박스 기반 레이아웃 분할
- `src/modu_semantic/compiler_json.py`: canonical semantic/layout 컴파일러
- `src/modu_semantic/compiler_svg.py`: SVG 렌더러
- `src/modu_semantic/recipes/`: 도메인 템플릿
- `schema/contract/`: semantic/layout 스키마 및 canonical order 프로파일

## 테스트

```bash
pytest
```

## Django Web Editor MVP

같은 리포 안에서 코어(`src/modu_semantic`)와 웹 에디터(`webapp/`)를 분리한 MVP 구조입니다.

### 폴더

- `webapp/config/settings/base.py|local.py|prod.py`: settings 분리
- `webapp/apps/editor`: 편집 UI + 저장/검증/내보내기
- `webapp/apps/problems`: 문제 관리용 앱(초기 메타 모델)
- `sample_data/problems/<problem_id>/semantic.json`: canonical semantic 원본 저장소

### 실행

```bash
uv sync
uv run python webapp/manage.py migrate
uv run python webapp/manage.py runserver
```

접속:

- `http://127.0.0.1:8000/editor/`
- 샘플 문제: `demo_0001`

## 인코딩/커밋 규칙

- 한글은 반드시 **UTF-8 리터럴(직접 한글)** 로 작성합니다.
- `\uXXXX`, `\xNN` 같은 유니코드 이스케이프 표기는 사용하지 않습니다.
- 커밋 전 자동 검사 훅(pre-commit)으로 위 규칙을 확인합니다.
  - 훅 스크립트: `.githooks/pre-commit`
  - 검사 코드: `tools/check_utf8_no_unicode_escape.py`

### `--no-verify` 사용 정책

- 원칙: `git commit --no-verify`는 사용하지 않습니다.
- 예외(긴급 상황)에서만 허용:
  1. 검사 스크립트 오작동이 확인된 경우
  2. 배포/핫픽스 등 시간 제한이 명확한 경우
- 예외 사용 시 필수:
  1. 커밋 메시지에 `no-verify 사유`를 명시
  2. 같은 날 후속 커밋으로 훅 검사를 통과하도록 즉시 보정
  3. PR/작업 기록에 원인과 재발 방지 조치를 남김

## 참고

기존 계약 번들 파이프라인(`include_layout_diff`, `baseline_layout_path`)도 `Problem.save()`에서 호환 모드로 유지됩니다.

## 빌드 파이프라인 용어

1. Semantic JSON 기반 생성 (`semantic-json build`)
- 입력: `semantic JSON`
- 엔진: 규칙/템플릿(필요 시 LLM 보조 가능)
- 출력: `py`, `json`, `svg`
- 성격: 의미 구조를 직접 변환하는 구조 기반 파이프라인

2. OCR+OpenCV 기반 생성 (`ocr-opencv build`)
- 입력: `png`
- 엔진: OCR + CV(OpenCV) 중심 (비-LLM)
- 출력: `py`, `json`, `svg`
- 성격: 텍스트/도형 인식 중심의 전통 CV 파이프라인

3. PNG 직접 파싱 기반 생성 (`png-direct-parse build`)
- 입력: `png`
- 엔진: 픽셀/레이아웃 직접 해석 (비-LLM)
- 출력: `py`, `json`, `svg`
- 성격: OCR 없이 처리하는 저수준 파싱 파이프라인

4. VLM/LLM 비전 해석 기반 생성 (`vlm-interpret build` 또는 `llm-vision build`)
- 입력: `png` (또는 `png+prompt`)
- 엔진: 멀티모달 LLM/VLM
- 출력: `py`, `json`, `svg`
- 성격: 의미 추론 중심의 LLM 기반 비전 파이프라인

## Semantic JSON 생성 규칙 (`semantic-json build`)

`examples/problem/**/input/semantic.json` 13,286개 전수 기준으로 입력 패턴을 규칙화합니다.

### 1) 입력 스키마 게이트

- `schema_version == "modu_math.semantic.v3"`를 강제합니다.
- root 필수 키: `schema_version`, `render_contract_version`, `problem_id`, `problem_type`, `title`, `metadata`, `domain`, `render`, `answer`
- `render` 필수 키: `canvas`, `elements`
- `canvas` 필수 키: `width`, `height`, `background`
- 현재 전수 데이터에서 `render.elements` 경로만 사용하며, root `elements`는 사용하지 않습니다.

### 2) 요소 타입 분기

- 공통 필수 요소: `problem_text` 1개 (`id`, `type`, `text`)
- 확장 요소(기하 선택형 문제): `multiple_choice`, `diagram_logic`
- 관측 빈도:
  - `problem_text`: 13,286/13,286
  - `multiple_choice`: 1,202/13,286
  - `diagram_logic`: 1,202/13,286

### 3) 답안 스키마 분기

- 주관식(OpenResponse) 패턴
  - `answer.blanks`: `[{"id":"blank_1","type":"numeric_or_text"}]`
  - `answer.choices`: `[]`
  - `answer.answer_key`: `[{"blank_id":"blank_1","value": <number>}]`
- 객관식(Geometry 선택형) 패턴
  - `answer.blanks`: `[]`
  - `answer.choices`: 문자열 배열
  - `answer.answer_key`: `[{"label":"A|B|...","index": <int>,"value": <string>}]`

### 4) 메타데이터 처리 규칙

- `metadata`, `domain`은 공통 필드와 데이터셋 확장 필드가 섞여 있으므로 pass-through를 기본으로 합니다.
- 생성기에서 의미 해석이 필요한 최소 필드만 참조합니다.
  - `domain.question_text` 또는 `domain.question_expression`
  - `domain.equation_or_reasoning` (있을 때만)
  - `domain.logic_form` (있을 때만)
- 그 외 필드는 손실 없이 유지합니다.

### 5) 산출물 생성 규칙

- `json`:
  - 입력 semantic을 canonical key order로 정렬 후 저장
  - 타입/필수 키 검증 실패 시 생성 중단
- `py`:
  - `problem_text` 기반으로 기본 DSL 뼈대를 생성
  - `multiple_choice`, `diagram_logic` 존재 시 기하 선택형 템플릿으로 분기
  - `answer.answer_key` 형태에 따라 주관식/객관식 오버레이 로직 분기
- `svg`:
  - 문제 SVG는 semantic 기반 기본 렌더
  - 정답 SVG는 `answer.answer_key`를 우선 사용해 오버레이 생성

### 6) 최소 구현 순서

1. 스키마 게이트 + key order 정규화
2. `problem_text` 전용 템플릿 완성 (OpenResponse)
3. `multiple_choice` + `diagram_logic` 템플릿 추가
4. 데이터셋별 예외는 `metadata.source` 기준으로 별도 규칙 파일에 분리
