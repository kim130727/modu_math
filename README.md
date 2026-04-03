# modu_math 전략 재구성 (UTF-8)

이 저장소는 아래 단계형 전략으로만 운영합니다.

## 폴더 구조

```text
problem/
  문제id/
    input/   # 입력 문제 원본(hwp, png 등) + 문제 데이터(problem.json)
    manim/   # manim .py, manim 렌더 결과 png
    json/    # manim 결과가 검증 완료된 뒤 생성하는 semantic json
    svg/     # semantic json 기반 생성 + 검증 완료 svg
    baseline/# 회귀 검증용 기준 semantic/svg/png
```

## 사용 원칙

1. 문제별로 `problem/문제id`를 생성합니다.
2. `input -> manim -> json -> svg` 순서로만 진행합니다.
3. 각 단계 명령은 개별 실행 가능해야 하며, 필요 시 마지막에 일괄 실행합니다.

## 단계별 개별 명령어 (PowerShell)

아래에서 `문제id`는 실제 ID로 바꿔서 사용하세요.

```powershell
# 0) 문제 디렉터리 생성
New-Item -ItemType Directory -Force `
  problem\문제id, `
  problem\문제id\input, `
  problem\문제id\manim, `
  problem\문제id\json, `
  problem\문제id\svg

# 1) 입력 데이터 배치 (예시)
# problem\문제id\input 안에 hwp/png 파일 복사
# 문제 데이터는 problem\문제id\input\problem.json 에 저장

# 2) manim 파일 실행(예시)
# manim -ql -s problem\문제id\manim\문제id_manim.py SceneClass
# 위의 SceneClass는 자리표시자이며, 실제 코드의 Scene 클래스명을 넣어야 함
# 예) manim -ql -s problem\0002\manim\0002_manim.py RulerEraserProblem
# 결과 png는 problem\문제id\manim\images 에 저장
# (미리보기까지 원하면 -p 추가. 단, Windows 파일 연결이 없으면 preview 단계에서 오류가 날 수 있음)

# 3) semantic json 생성(예시)
# python problem\문제id\manim\문제id_manim.py --export-semantic
# (문제 데이터 경로를 직접 지정할 때)
# python problem\문제id\manim\문제id_manim.py --export-semantic --problem-in problem\문제id\input\problem.json

# 4) svg 생성 및 검증(예시)
# python problem\문제id\manim\문제id_manim.py --validate
# python problem\문제id\manim\문제id_manim.py --render-svg
# (한 번에 실행) python problem\문제id\manim\문제id_manim.py --all

# 5) 회귀 검증(예시)
# .\.venv\Scripts\python.exe -m pytest -q tests\test_regression_render.py
# (캐시 폴더 생성 없이 실행)
# $env:PYTHONDONTWRITEBYTECODE=1
# .\.venv\Scripts\python.exe -m pytest -q -p no:cacheprovider tests\test_regression_render.py

# 6) 신규 src 기반 러너(점진 이전용)
# python src\modu_math\cli\run_problem.py --problem-id 0001 --all
# python src\modu_math\cli\validate_problem.py --semantic problem\0001\json\semantic.json
```

## 나중에 한꺼번에 실행할 때

`run_all.ps1` 같은 스크립트에 위 2~4단계 명령을 순서대로 넣어 일괄 실행합니다.
(현재 저장소에는 강제 실행 스크립트를 두지 않고, 문제별 커맨드를 명시적으로 관리합니다.)

## ?? ?? import (UTF-8)

?? ?? ????? `problem.common`?? ?? ??? ? ?? ??? ? ????.

```python
from problem.common import (
    find_problem_dir,
    problem_input_json_path,
    semantic_json_path,
    semantic_svg_path,
    render_svg_from_semantic,
    render_manim_from_semantic,  # manim ??? ????? None? ? ??
    validate_structure,
    validate_logic,
)
```

??: ?? ??? ????? `src/modu_math/...` ?? import? ?????.
??: ?? ??? `problem.common` import? ??? ???? ?????.

