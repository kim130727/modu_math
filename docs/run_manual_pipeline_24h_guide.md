
로컬 PowerShell에서 백그라운드로 띄우면 24시간 이상 계속 돌릴 수 있습니다.

cd c:\projects\modu_math

Start-Process powershell -ArgumentList @(
  '-NoProfile',
  '-ExecutionPolicy', 'Bypass',
  '-File', 'tools/run_manual_pipeline.ps1',
  '-ListFile', 'txt/problems_list.txt',
  '-Provider', 'openai',
  '-Mode', 'api',
  '-DslMaxAttempts', '1'
) -RedirectStandardOutput 'logs/pipeline.out.log' `
  -RedirectStandardError 'logs/pipeline.err.log' `
  -WindowStyle Hidden

  Google로 돌리려면 -Provider google로만 바꾸면 됩니다.

  진행 확인:
Get-Content logs/pipeline.out.log -Wait

## Naming Convention (Avoid JSON Confusion)

- `source problem json`: the existing JSON paired with the image, e.g. `S3_...json`.
- `generated semantic json`: `<prob_id>.semantic.json`.
- `generated layout json`: `<prob_id>.layout.json`.
- `generated renderer json`: `<prob_id>.renderer.json`.
- `generated solvable json`: `<prob_id>.solvable.v1.1.json`.
- `structured vision draft json`: `<prob_id>.vision_structured.json`.

When running manual pipeline from `txt/problem_list.txt` (base path list without extension):

- Use `<base>.png` as primary visual input.
- If `<base>.json` exists, treat it only as optional `source problem json` reference.
- Never treat `source problem json` as semantic/layout/renderer output.

## Structured Vision Draft Sidecar

The manual pipeline now writes an optional assistant sidecar:

- Prompt bundle: `<prob_id>.vision_structured_prompt.md`
- Prompt-mode response file to fill: `<prob_id>.vision_structured_llm_output.txt`
- Validated JSON output: `<prob_id>.vision_structured.json`

This sidecar records image size, approximate normalized bounding boxes, visible text, elements, groups, math structure, DSL hints, and uncertainty notes. It does not replace `problem.dsl.py` or generated contract JSON.

By default, the manual pipeline skips this sidecar. Pass `-UseVisionStructured` to generate `<prob_id>.vision_structured.json` and pass it to `generate_dsl_from_refined_draft.py` as layout constraints via `--vision-structured`.

## Phase Provider Override (new)

`tools/run_manual_pipeline.ps1` now supports per-phase provider override.

- Phase 1 (vision + refine): `-Phase1Provider`
- Phase 2 (dsl generation): `-Phase2Provider`

Examples:
- Phase1=google, Phase2=openai
  - `-Provider openai -Phase1Provider google -Phase2Provider openai`
- Phase1=openai, Phase2=google
  - `-Provider openai -Phase1Provider openai -Phase2Provider google`

If `-Phase1Provider` / `-Phase2Provider` are omitted, both phases use `-Provider`.
