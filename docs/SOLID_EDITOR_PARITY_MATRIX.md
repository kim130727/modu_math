# SOLID_EDITOR_PARITY_MATRIX

본 문서는 기존 웹 에디터와 새 SolidJS + TypeScript 에디터 간의 기능 동등성(Feature Parity) 현황을 추적하는 매트릭스입니다.

| ID | 기능 | 기존 에디터 | SolidJS 에디터 | 자동 테스트 | 수동 테스트 | 상태 |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **F001** | 문제 목록 로딩 | 있음 | 있음 | 통과 | 통과 | **완료** |
| **F002** | 단일 선택 | 있음 | 있음 | 통과 | 통과 | **완료** |
| **F003** | 다중 선택 (Marquee) | 있음 | 있음 | 통과 | 통과 | **완료** |
| **F004** | 드래그 이동 (스냅) | 있음 | 있음 | 통과 | 통과 | **완료** |
| **F005** | 8방향 리사이즈 | 있음 | 있음 | 통과 | 통과 | **완료** |
| **F006** | 도형 갤러리 삽입 | 있음 | 미흡 (일부) | 미실행 | 미실행 | **미완료** |
| **F007** | 슬롯 삭제 | 있음 | 있음 | 통과 | 통과 | **완료** |
| **F008** | 속성 편집 (인스펙터) | 있음 | 있음 | 통과 | 통과 | **완료** |
| **F009** | 인라인 텍스트 편집 | 있음 | 없음 | 미실행 | 미실행 | **미완료** |
| **F010** | 정렬 도구 (Align) | 있음 | 없음 | 미실행 | 미실행 | **미완료** |
| **F011** | 레이어 순서 조절 (Layer) | 있음 | 없음 | 미실행 | 미실행 | **미완료** |
| **F012** | Undo / Redo | 있음 | 있음 | 통과 | 통과 | **완료** |
| **F013** | DSL 포맷 | 있음 | 있음 | 통과 | 통과 | **완료** |
| **F014** | 문제 빌드 | 있음 | 있음 | 통과 | 통과 | **완료** |
| **F015** | Zoom 및 Pan | 있음 | 있음 | 통과 | 통과 | **완료** |
| **F016** | Hit Proxy 보조 도구 | 있음 | 없음 | 미실행 | 미실행 | **미완료** |
| **F017** | 키보드 미세 이동 디바운스 | 있음 | 미흡 | 미실행 | 미실행 | **미완료** |
| **F018** | 빌드 후 선택 상태 복구 | 있음 | 없음 | 미실행 | 미실행 | **미완료** |
| **F019** | 동시 수정 충돌 방지 | 있음 | 없음 | 미실행 | 미실행 | **미완료** |

## 2026-07-04 Progress Note

| ID | Area | SolidJS status | Verification |
| :--- | :--- | :--- | :--- |
| F009 | Inline text edit | Partial: double-click server-rendered SVG text to open an overlay input; Enter/blur commits through the existing property patch path; Escape cancels. | Not run: npm install/typecheck blocked by npm EPERM while creating cache folders. Manual browser check still required. |
| F016 | Hit proxy / SVG element hit testing | Partial: selection now prioritizes actual SVG elements and geometric hit boxes for text, line, path, polygon, circle, image, and rect; overlay bounds prefer actual SVG element bounds before falling back to layout bounds. | Not run: npm install/typecheck blocked by npm EPERM while creating cache folders. Manual browser check still required. |
| F010 | Align controls | Partial: SolidJS toolbar now exposes left/center/right/top/middle/bottom alignment for two or more selected slots, using existing move patch-and-build flow with undo/redo snapshots. | `uv run --with pytest pytest tests/web/test_editor_api.py -q -p no:cacheprovider` passed with temp/cache redirected to `.tmp`. Frontend typecheck still blocked by missing `tsc` / npm EPERM. |
| F011 | Layer controls | Partial: SolidJS toolbar now exposes front/back/forward/backward layer ordering, using existing `layer` patch payloads and inverse layer patches for undo/redo. | `uv run --with pytest pytest tests/web/test_editor_api.py -q -p no:cacheprovider` passed with temp/cache redirected to `.tmp`. Frontend typecheck still blocked by missing `tsc` / npm EPERM. |
