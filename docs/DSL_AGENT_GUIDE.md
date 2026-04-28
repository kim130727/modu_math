# DSL Agent Guide

## Architecture

`PNG -> Python DSL -> semantic JSON -> layout JSON -> renderer JSON -> SVG`

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

Generate one DSL:

```bash
uv run python tools/generate_dsl_from_png.py \
  --image examples/problems/0001/input.png \
  --problem-id 0001 \
  --out examples/problems/0001/problem.dsl.py
```

Validate one DSL:

```bash
uv run python tools/validate_generated_dsl.py \
  --dsl examples/problems/0001/problem.dsl.py \
  --strict
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
  problem.dsl.py
  problem.semantic.json
  problem.layout.json
  problem.renderer.json
  problem.svg
  build_report.json
  agent_trace.json
```

## Rules

- Do not edit generated JSON by hand.
- Edit `problem.dsl.py` instead.
- Do not put API code in `src/modu_math`.
- Do not put renderer details in semantic.
- Keep Korean text as direct UTF-8.

## Known Limitations

- PNG recognition can be wrong.
- Generated DSL must be human-reviewed.
- Keep repair loops limited.
- Visual SVG similarity does not prove semantic correctness.
