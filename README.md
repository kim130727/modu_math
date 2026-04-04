# modu_math 작업 흐름 안내 (UTF-8)

이 프로젝트는 문제별로 아래 3단계(옵션 A)로 작업합니다.

1. `stage1`  
   입력(`input/problem.json`)으로 기본 산출물 생성  
   - `json/semantic/semantic.json`
   - `svg/semantic.svg`
   - `json/layout/layout.json`

2. `stage2`  
   사람이 `svg/edit/semantic_edit.svg`를 수정한 뒤 편집 산출물 생성  
   - `json/semantic_edit/semantic_edit.json`
   - `json/layout_edit/layout_edit.json`
   - `json/layout_edit/layout_diff_stage1_to_edit.json`
   - (선택) 위 JSON을 참고해 `manim/final/{id}_manim_final.py`를 보정

3. `final`  
   편집 결과를 최종본으로 확정 (source-of-truth: `semantic_edit`)  
   - `json/semantic_final/semantic_final.json` (`semantic_edit` 복사/확정)
   - `json/layout_final/layout_final.json`
   - `svg/final/semantic_final.svg`

`baseline` 폴더는 더 이상 사용하지 않습니다.

## 폴더 구조 예시

```text
problem/
  0003/
    input/
      problem.json
    manim/
      0003_manim.py
      edit/
        0003_manim_edit.py
      final/
        0003_manim_final.py
    json/
      semantic/
      layout/
      semantic_edit/
      layout_edit/
      semantic_final/
      layout_final/
    svg/
      semantic.svg
      edit/
        semantic_edit.svg
      final/
        semantic_final.svg
```

## 가장 많이 쓰는 명령

아래는 `0003` 예시입니다.

```powershell
# 0) 폴더/편집용 파일 초기화
.\.venv\Scripts\python.exe problem\common\stage_cli.py --problem-id 0003 --step init

# 1) 기본 산출물 생성
.\.venv\Scripts\python.exe problem\common\stage_cli.py --problem-id 0003 --step stage1

# 2) 편집 반영
.\.venv\Scripts\python.exe problem\common\stage_cli.py --problem-id 0003 --step stage2

# 3) 최종 확정
.\.venv\Scripts\python.exe problem\common\stage_cli.py --problem-id 0003 --step final
```

한 번에 모두 실행:

```powershell
.\.venv\Scripts\python.exe problem\common\stage_cli.py --problem-id 0003 --step all
```

## 자주 묻는 점

- `stage2`에서 `svg/edit/semantic_edit.svg`가 없으면?
  - `svg/semantic.svg`를 자동 복사해서 편집용 파일을 만들어 줍니다.

- `stage2`에서 SVG에서 지운 요소가 `final`에도 반영되나요?
  - 네. `stage2` 변환 시 SVG에 없는 요소는 `semantic_edit`에서 제거되어 `final`에 반영됩니다.

- `manim/edit/*.py` / `manim/final/*.py`는 자동으로 좌표를 다시 쓰나요?
  - 아니요. 두 파일 모두 JSON(`semantic_edit` / `semantic_final`)을 읽어 렌더하는 템플릿입니다.
  - 따라서 사람이 JSON/SVG를 편집하면 코드 수정 없이도 결과가 반영됩니다.

- `manim/final` 재검증(옵션 B)은 꼭 필요하나요?
  - 필수는 아닙니다. 큰 수정이나 배포 전 QA에서 선택적으로 수행하는 것을 권장합니다.
