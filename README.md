# modu_math 작업 흐름 안내 (UTF-8)

이 프로젝트는 문제별로 아래 3단계로 작업합니다.

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
3. `final`  
   편집 결과를 최종본으로 확정  
   - `json/semantic_final/semantic_final.json`
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
- `manim/edit/*.py`는 자동으로 숫자 좌표를 다시 쓰나요?
  - 아니요. 이 파일은 `semantic_edit.json`을 읽어 렌더하는 템플릿입니다.
  - 그래서 코드 자체를 고치지 않아도 편집 결과가 반영됩니다.
