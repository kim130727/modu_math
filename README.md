# modu_math Pipeline (Staged)

이 저장소는 문제별로 아래 단계 파이프라인을 사용합니다.

1. `stage1`: `input -> manim -> json/semantic -> svg -> json/layout`
2. `stage2`: 사람이 `svg/edit`를 편집한 뒤 `json/semantic_edit`, `json/layout_edit` 생성
3. `final`: `semantic_edit`를 기준으로 `json/semantic_final`, `json/layout_final`, `svg/final` 생성

기존 `baseline` 폴더는 사용하지 않습니다.

## Directory Structure

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
        semantic.json
      layout/
        layout.json
      semantic_edit/
        semantic_edit.json
      layout_edit/
        layout_edit.json
        layout_diff_stage1_to_edit.json
      semantic_final/
        semantic_final.json
      layout_final/
        layout_final.json
    svg/
      semantic.svg
      edit/
        semantic_edit.svg
      final/
        semantic_final.svg
```

## Quick Start

아래 명령은 `0003` 기준 예시입니다.

```powershell
# 0) 구조 초기화(필요 폴더/편집용 manim 파일 자동 생성)
.\.venv\Scripts\python.exe problem\common\stage_cli.py --problem-id 0003 --step init

# 1) 1단계 실행
.\.venv\Scripts\python.exe problem\common\stage_cli.py --problem-id 0003 --step stage1

# 2) 2단계 실행
# - svg/edit/semantic_edit.svg가 없으면 stage1 svg를 자동 복사해 seed 파일 생성
.\.venv\Scripts\python.exe problem\common\stage_cli.py --problem-id 0003 --step stage2

# 3) final 실행
.\.venv\Scripts\python.exe problem\common\stage_cli.py --problem-id 0003 --step final
```

한 번에 전체 실행:

```powershell
.\.venv\Scripts\python.exe problem\common\stage_cli.py --problem-id 0003 --step all
```

## Notes

- 문제별 기존 스크립트(`problem/{id}/manim/{id}_manim.py`)는 기본 semantic 출력 경로가 `json/semantic/semantic.json`으로 변경되었습니다.
- `stage2`에서는 `svg/semantic.svg`와 `svg/edit/semantic_edit.svg`의 레이아웃 차이를 `json/layout_edit/layout_diff_stage1_to_edit.json`에 저장합니다.
- 사람이 편집한 파일이 아직 없어도 바로 실행할 수 있도록 `stage2`에서 edit SVG seed를 자동 생성합니다.
