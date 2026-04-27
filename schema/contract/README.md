# JSON Contract Bundle (Canonical)

다른 저장소로 복사해서 사용할 수 있는 canonical 계약 파일입니다.

## Files

- `../semantic/semantic.v1.json`
- `../layout/layout.v1.json`
- `../layout/layout.diff.v1.json`
- `../renderer/renderer.v1.json`
- `canonical_order_profile.json`

경로: `schema/contract/`

## Canonical summary

### semantic root keys

- `problem_id`
- `problem_type`
- `metadata`
- `domain`
- `answer`

### layout root keys

- `schema`
- `problem_id`
- `title`
- `canvas`
- `regions`
- `slots`
- `groups`
- `constraints`
- `diagrams`
- `reading_order`

### layout diff root keys

- `problem_id`
- `patches`

### renderer root keys

- `problem_id`
- `view_box`
- `elements`

## Artifact roles

- canonical contracts: `semantic.json`, `layout.json`, `renderer.json`
- derived artifact: `svg` (renderer 기반 최종 출력)

## Normalization policy

- old alias 허용 후 canonical 이름으로 매핑
- 누락 기본값 보정
- deprecated 필드는 내부 canonical 필드로 치환
- optional/빈 블록(`metadata`, `domain`, `answer`) 처리 규칙 통일
- 최종 출력은 `canonical_order_profile.json` 기준으로 key 순서 고정

## Validation policy

- semantic validation: 의미 계약 필드/타입 검증
- layout validation: 편집 배치 필드/타입/식별자 검증
- renderer validation: 렌더 필드/타입 검증
- cross-layer strict validation: semantic↔layout↔renderer 참조 일관성 검증

### Cross-layer rules (strict mode)

- canonical layout(`regions/slots`) 기준 검증
- `layout` 객체의 `source_ref` (optional) -> semantic id
- required semantic-to-layout mapping:
  - `domain.objects[].layout_required = true`
  - `metadata.required_layout_ids[]`
- `renderer.elements[].refs.layout_*_id` -> layout id
- (legacy `nodes` payload only) `renderer.elements[].id` -> layout node id
- `renderer.elements[].source_ref` 또는
  `renderer.elements[].attributes.source_ref` (optional) -> semantic id or layout id

## Compatibility policy

- 계약 밖 root key가 생기면 실패해야 합니다.
- 계약 변경이 필요하면 schema 파일 버전을 올리고 마이그레이션을 명시합니다.
