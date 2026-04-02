# modu_math 전략 재구성 (UTF-8)

이 저장소는 아래 단계형 전략으로만 운영합니다.

## 폴더 구조

```text
problem/
  문제id/
    input/   # 입력 문제 원본(hwp, png 등)
    manim/   # JSON을 코드에 포함한 manim .py, manim 렌더 결과 png
    json/    # manim 결과가 검증 완료된 뒤 생성하는 semantic json
    svg/     # semantic json 기반 생성 + 검증 완료 svg
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

# 2) manim 파일 실행(예시)
# manim -pql problem\문제id\manim\scene.py SceneClass
# 결과 png는 problem\문제id\manim 에 저장

# 3) semantic json 생성(예시)
# uv run python tools\build_semantic_json.py --src problem\문제id\manim\scene.py --out problem\문제id\json\semantic.json

# 4) svg 생성 및 검증(예시)
# uv run python tools\build_svg.py --semantic problem\문제id\json\semantic.json --out problem\문제id\svg\result.svg
# uv run python tools\verify_svg.py --svg problem\문제id\svg\result.svg
```

## 나중에 한꺼번에 실행할 때

`run_all.ps1` 같은 스크립트에 위 2~4단계 명령을 순서대로 넣어 일괄 실행합니다.
(현재 저장소에는 강제 실행 스크립트를 두지 않고, 문제별 커맨드를 명시적으로 관리합니다.)
