# JSON Contract Bundle (Canonical)

다른 저장소로 복사해서 사용할 수 있는 canonical 계약 파일입니다.

## Files

- `semantic_v3.schema.json`
- `layout_v1.schema.json`
- `layout_diff_v1.schema.json`
- `../renderer/renderer.v1.json`
- `canonical_order_profile.json`

경로: `schema/contract/`

## Canonical summary

### semantic root keys

- `schema_version`
- `render_contract_version`
- `problem_id`
- `problem_type`
- `title` (optional)
- `metadata`
- `domain`
- `render`
- `answer`

### semantic nested order

- `render`: `canvas`, `elements`
- `canvas`: `width`, `height`, `background`
- `answer`: `blanks`, `choices`, `answer_key`

### layout root keys

- `schema_version`
- `problem_id`
- `metadata`
- `canvas`
- `summary`
- `elements`

### layout diff root keys

- `schema_version`
- `problem_id`
- `metadata`
- `diff`
- `metrics`

### renderer root keys

- `problem_id`
- `view_box`
- `elements`

## Normalization policy (v3 유지)

- old alias 허용 후 canonical 이름으로 매핑
- 누락 기본값 보정
- deprecated 필드는 내부 canonical 필드로 치환
- optional/빈 블록(`metadata`, `domain`, `answer`, `summary` 등) 처리 규칙 통일
- 최종 출력은 `canonical_order_profile.json` 기준으로 key 순서 고정

## Validation policy (v3 정밀화)

- 필수 필드 누락 검출
- enum 오류 검출
- 타입 오류 검출
- 금지 조합 검출
- canonical order 검사

## Compatibility policy

- 계약 밖 root key가 생기면 실패해야 합니다.
- 계약 변경이 필요하면 schema 파일 버전을 올리고 마이그레이션을 명시합니다.
