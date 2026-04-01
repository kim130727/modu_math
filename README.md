# Math Problem Pipeline

PDF의 초등/중등 수학 문제를 추출하고, 렌더 가능한 semantic JSON으로 정규화한 뒤, **LaTeX/TikZ로 중간 점검**하고 필요 시 Manim으로 정지형 문제 화면을 재생성하는 코드베이스입니다.

## 프로젝트 목적

- `PDF -> semantic JSON -> TikZ(중간 점검) -> Manim(최종/추후)` 파이프라인 구축
- parser 정확도보다 **semantic JSON schema의 구조적 완성도** 우선
- 렌더 실패/단순화 사례를 누적하여 schema를 개선

## 핵심 철학

1. PDF 원본은 비정형이며 불완전하다.
2. semantic JSON은 기계가 렌더할 수 있어야 한다.
3. TikZ는 semantic 중간 점검기, Manim은 최종 출력기다.
4. 렌더 실패는 대개 schema 정보 부족 신호다.
5. 실패 로그를 schema 개선 근거로 남긴다.
6. 문제별 렌더 코드 누적 대신 공통 renderer + 유형별 semantic JSON으로 간다.

## 아키텍처 요약

1. **Raw Extraction**
- PDF에서 페이지 단위 텍스트/도형 bbox를 추출 (`extract/`)

2. **Problem Segmentation**
- 문제 번호/텍스트 패턴 기반으로 문제 후보 분리 (`problem_segmenter.py`)

3. **Problem PDF Split (Optional)**
- input PDF를 문제 1개 단위의 PDF로 분할 (`extract/problem_pdf_splitter.py`)

4. **Semantic Normalization**
- 후보를 유형 분류 후 semantic 모델로 변환 (`normalize/`)

5. **Intermediate Rendering (TikZ)**
- semantic JSON을 standalone `.tex`로 출력하고, 가능하면 `.pdf`까지 컴파일해 시각 점검 (`render/tikz_renderer.py`)

6. **Final Rendering (Manim, Optional)**
- `type` 기준 SceneFactory가 builder를 선택해 Manim 정지형 장면 생성 (`render/`)

7. **Debug Compare**
- raw/semantic/render 사용 필드 비교 및 schema 개선 포인트 리포트 생성 (`compare/`)

## 좌표계 설계

- `source coordinates`: PDF 기준 bbox/page size
- `semantic coordinates`: 도형 관계/정규화 좌표 (vertices, shaded_indices 등)
- `render coordinates`: 렌더러 장면 배치 좌표

`semantic_models.CoordinateSystemRef`로 3층을 명시합니다.

## 지원 문제 유형 (1차)

1. `multiple_choice_text`
2. `arithmetic_expression`
3. `fraction_shaded_area`
4. `clock_reading`
5. `geometry_basic`
6. `table_or_chart_basic`

## 디렉토리 구조

```text
project_root/
  pyproject.toml
  README.md
  src/
    math_problem_pipeline/
      __init__.py
      cli.py
      samples.py
      models/
        __init__.py
        raw_models.py
        problem_models.py
        semantic_models.py
        render_models.py
      extract/
        __init__.py
        pdf_reader.py
        page_extractor.py
        problem_segmenter.py
        problem_pdf_splitter.py
      normalize/
        __init__.py
        semantic_builder.py
        type_classifier.py
        validators.py
      render/
        __init__.py
        manim_renderer.py
        tikz_renderer.py
        scene_factory.py
        layout_engine.py
        figure_builders.py
      compare/
        __init__.py
        debug_report.py
      utils/
        __init__.py
        io.py
        logging_utils.py
        geometry.py
  input/
    sample_semantic/
  output/
    raw/pages/
    raw/problems/
    semantic/
    pdf/
    tikz/
    renders/
    reports/
```

## 설치 방법

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .
```

## 권장 실행 순서

1. input 폴더 PDF를 문제별 PDF로 분할 (선택)
```bash
math-pipeline split-problem-pdfs --input-dir input --output-dir output/pdf
```

2. PDF 페이지 raw 추출
```bash
math-pipeline parse-pdf input/book1.pdf --output-dir output/raw/pages
```

3. 문제 후보 분리
```bash
math-pipeline segment-problems --raw-pages-dir output/raw/pages --output-dir output/raw/problems
```

4. semantic JSON 생성
```bash
math-pipeline build-semantic --raw-problem-dir output/raw/problems --output-dir output/semantic
```

5. TikZ 단일 점검 렌더 (시각 확인 PDF 컴파일 포함)
```bash
math-pipeline render-tikz output/semantic/book1_p0001_q0003.semantic.json --output-dir output/tikz --compile-pdf
```

6. TikZ 전체 점검 렌더 (시각 확인 PDF 컴파일 포함)
```bash
math-pipeline render-tikz-all --semantic-dir output/semantic --output-dir output/tikz --compile-pdf
```

7. Manim 단일 렌더 (선택)
```bash
math-pipeline render-problem output/semantic/book1_p0001_q0003.semantic.json --output-dir output/renders
```

8. Manim 전체 렌더 (선택)
```bash
math-pipeline render-all --semantic-dir output/semantic --output-dir output/renders
```

9. debug compare 리포트
```bash
math-pipeline debug-compare --semantic-dir output/semantic --raw-problem-dir output/raw/problems --render-dir output/renders --report-dir output/reports
```

10. 샘플 semantic JSON 생성
```bash
math-pipeline bootstrap-samples --output-dir input/sample_semantic
```

## 출력 파일 규칙

- `output/raw/pages/{doc}_p0001.json`
- `output/raw/problems/{doc}_p0001_q0003.raw.json`
- `output/semantic/{doc}_p0001_q0003.semantic.json`
- `output/pdf/{doc}/{doc}_p0001_q0003.pdf`
- `output/tikz/{doc}_p0001_q0003.tikz.tex`
- `output/tikz/{doc}_p0001_q0003.tikz.pdf` (pdflatex 사용 가능 시 자동 생성)
- `output/renders/{doc}_p0001_q0003.render.png`
- `output/reports/{doc}_p0001_q0003.report.json`

## Schema Refinement Report

리포트는 다음 정보를 포함합니다.

- raw에서 추출된 필드
- semantic으로 정규화된 필드
- renderer가 사용한 필드
- 누락 정보
- 단순화/추론된 정보
- schema 개선 포인트 (`missing_geometry_vertices`, `ambiguous_fraction_partition`, `fallback_layout_used` 등)

## 확장 계획

- LLM 보조 semantic extraction
- renderer 다변화 (Godot, HTML/SVG)
- dataset 누적 + schema versioning
- 정답/해설 자동 생성
- interactive rendering

## 현재 한계

- 문제 분리/유형 분류는 규칙 기반 heuristic이라 정확도가 제한적
- geometry/table/chart의 추출은 최소 구조 중심
- 문제별 PDF 분할은 bbox 기반 이미지 PDF이므로 벡터 원본 품질과 다를 수 있음
- TikZ 출력은 중간 점검용이며 정교한 최종 스타일링은 Manim 단계에서 수행

## LLM 연동 포인트

- `normalize/semantic_builder.py`
  - 후보 텍스트 + raw visual block을 LLM prompt로 전달해 semantic draft 생성
- `normalize/validators.py`
  - LLM 출력 검증 및 보정 규칙 적용
- `compare/debug_report.py`
  - 실패 패턴 집계 후 프롬프트/스키마 동시 개선
