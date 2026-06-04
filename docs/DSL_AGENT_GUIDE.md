# DSL Agent Guide

## Architecture

Canonical pipeline:

`PNG -> Python DSL -> semantic JSON -> solvable JSON -> layout JSON -> renderer JSON -> SVG`

Recommended assisted authoring workflow:

`PNG -> vision_draft.md -> refined_draft.md -> problem.dsl.py -> semantic JSON -> layout JSON -> renderer JSON -> SVG`

- `vision_draft.md` and `refined_draft.md` are optional assistant artifacts, not canonical contracts.
- `vision_draft.md`: raw visual observation from a vision LLM.
- `refined_draft.md`: DSL-ready interpretation refined from the raw draft.
- `problem.dsl.py` remains the human-editable canonical authoring source.
- semantic/layout/renderer/solvable JSON and SVG remain generated artifacts.
- Draft JSON is intentionally not introduced yet; the project focuses on `refined_draft.md` first because it is easier for humans to review and correct.

## Role Separation

- ChatGPT API tools generate a `problem.dsl.py` draft.
- `modu_math` core compiles and validates artifacts.
- Human reviews and edits `problem.dsl.py`.
- JSON and SVG are generated artifacts, not authoring sources.

## Commands

Install extras:

```bash
uv sync --extra dev --extra llm
```

Generate raw vision draft:

```bash
uv run python tools/generate_vision_draft.py \
  --image examples/problems/0001/input.png \
  --problem-id 0001 \
  --out examples/problems/0001/vision_draft.md \
  --force
```

Refine the vision draft:

```bash
uv run python tools/refine_vision_draft.py \
  --vision-draft examples/problems/0001/vision_draft.md \
  --image examples/problems/0001/input.png \
  --problem-id 0001 \
  --out examples/problems/0001/refined_draft.md \
  --force
```

Generate DSL from refined draft (recommended):

```bash
uv run python tools/generate_dsl_from_refined_draft.py \
  --draft examples/problems/0001/refined_draft.md \
  --image examples/problems/0001/input.png \
  --problem-id 0001 \
  --out examples/problems/0001/problem.dsl.py \
  --force
```

Validate generated DSL:

```bash
uv run python tools/validate_generated_dsl.py \
  --dsl examples/problems/0001/problem.dsl.py \
  --strict
```

Optional direct PNG-to-DSL fallback (legacy/direct mode):

```bash
uv run python tools/generate_dsl_from_png.py \
  --image examples/problems/0001/input.png \
  --problem-id 0001 \
  --out examples/problems/0001/problem.dsl.py \
  --force
```

Repair one DSL (human edit loop):

```bash
# 1) Edit problem.dsl.py manually
# 2) Re-validate
uv run python tools/validate_generated_dsl.py \
  --dsl examples/problems/0001/problem.dsl.py \
  --strict
```

Batch generate:

```bash
uv run python tools/batch_generate_dsl.py \
  --root examples/problems \
  --validate
```

## File Layout

```text
examples/problems/0001/
  input.png
  vision_draft.md
  refined_draft.md
  problem.dsl.py
  problem.semantic.json
  problem.solvable.json
  problem.layout.json
  problem.renderer.json
  problem.svg
```

## Rules

- Do not edit generated JSON/SVG by hand.
- Edit `problem.dsl.py` first.
- Use `refined_draft.md` only as an assistant artifact before DSL generation.
- `refined_draft.md` may contain TODOs and uncertainty notes.
- If `refined_draft.md` conflicts with the image, the image is the source of visible truth.
- If DSL conflicts with semantic meaning, fix `problem.dsl.py` and rebuild.
- Do not put API code in `src/modu_math`.
- Do not put renderer details in semantic.
- Keep Korean text as direct UTF-8.

## Known Limitations

- PNG recognition can be wrong.
- Generated DSL must be human-reviewed.
- Keep repair loops limited.
- Visual SVG similarity does not prove semantic correctness.
