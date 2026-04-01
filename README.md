# Math Problem Pipeline

HWPX의 수학 문서를 추출하고, semantic JSON으로 정규화한 뒤 SVG/Manim으로 점검하는 파이프라인입니다.

## 목표

- `HWPX -> raw -> semantic -> render` 단순 파이프라인
- 보수적 분류/최소 추론(모르면 `unknown`)
- 디버깅이 쉬운 단계별 출력

## 핵심 명령

1. HWPX raw 추출
```bash
math-pipeline parse-hwpx input/book1.hwpx --output-dir output/raw/pages
```

2. 문제 분리 + 비문항 거절
```bash
math-pipeline segment-problems --raw-pages-dir output/raw/pages --output-dir output/raw/problems --rejected-output-dir output/raw/rejected
```

3. semantic 생성
```bash
math-pipeline build-semantic --raw-problem-dir output/raw/problems --output-dir output/semantic --rejected-output-dir output/semantic_rejected
```

4. SVG 중간 점검
```bash
math-pipeline render-svg-all --semantic-dir output/semantic --output-dir output/svg
```

5. 전체 자동 파이프라인
```bash
math-pipeline run-pipeline input/book1.hwpx --output-root output
```

## 출력 구조

- `output/raw/pages/*.json`
- `output/raw/problems/*.raw.json`
- `output/raw/rejected/*.raw.json`
- `output/semantic/*.semantic.json`
- `output/semantic_rejected/*.semantic.json`
- `output/svg/*.render.svg`
- `output/reports/*.report.json`

## 비고

- 현재 추출기는 HWPX XML 텍스트 기반 보수 추출기입니다.
- 시각 구조(도형/표/그래프) 신뢰도가 낮으면 `unknown_visual_math_problem`으로 유지합니다.
- 렌더 단계는 invalid 구조에서 자동 fallback(text only) 됩니다.
- SVG 렌더는 semantic 이상치가 있으면 자동 fallback(text only)로 내려갑니다.


