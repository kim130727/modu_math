# Math Problem Pipeline

HWPX 수학 문서를 보수적으로 추출하고 문제 단위 산출물로 정리하는 파이프라인입니다.

## 목표

- `HWPX -> problem bundle(raw + semantic + svg)` 단순 파이프라인
- 보수적 분류/최소 추론(모르면 `unknown`)
- 디버깅이 쉬운 문제별 출력 구조

## 핵심 명령

1. 단일 실행 (권장)
```bash
math-pipeline run-pipeline input/book1.hwpx --output-root output
```

2. 단계 실행 (선택)
```bash
math-pipeline parse-hwpx input/book1.hwpx --output-dir output/raw/pages --images-dir output/images
math-pipeline segment-problems --raw-pages-dir output/raw/pages --output-dir output/raw/problems --rejected-output-dir output/raw/rejected
math-pipeline build-semantic --raw-problem-dir output/raw/problems --output-dir output/semantic --rejected-output-dir output/semantic_rejected
math-pipeline render-svg-all --semantic-dir output/semantic --output-dir output/svg
```

## 출력 구조 (`run-pipeline` 기준)

- `output/images/*` (HWPX에서 파싱된 이미지 자산)
- `output/problems/<problem_id>/raw.json`
- `output/problems/<problem_id>/semantic.json`
- `output/problems/<problem_id>/render.svg`

`report.json`은 생성하지 않습니다.

## 비고

- 현재 추출기는 HWPX XML 텍스트 기반 보수 추출기입니다.
- 시각 구조(도형/표/그래프) 신뢰도가 낮으면 `unknown_visual_math_problem`으로 유지합니다.
- SVG 렌더 단계는 invalid 구조에서 자동 fallback(text only) 됩니다.