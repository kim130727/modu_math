# modu_math

This directory is an isolated core copy of `modu_math` focused on the canonical pipeline:

`PNG -> Python DSL -> semantic JSON -> solvable JSON -> layout JSON -> renderer JSON -> SVG`

Recommended assisted authoring workflow:

`PNG -> vision_draft.md -> refined_draft.md -> Python DSL -> generated artifacts`

- `vision_draft.md` and `refined_draft.md` are optional assistant artifacts, not canonical contracts.
- `vision_draft.md` is raw visual observation from a vision LLM.
- `refined_draft.md` is a DSL-ready interpretation refined from that raw draft.
- `problem.dsl.py` remains the human-editable canonical authoring source.
- semantic/layout/renderer/solvable JSON and SVG remain generated artifacts.
- Draft JSON is intentionally not introduced yet; the project currently focuses on `refined_draft.md` because it is easier for humans to review and correct.

## Core Contracts

- `semantic JSON`: meaning source of truth
- `Python DSL`: human-editable authoring source
- `layout JSON`: structure and placement contract
- `renderer JSON`: drawable contract
- `SVG`: generated visual artifact

## Directory Overview

- `src/modu_math/`: core compiler, adapters, semantic/layout/renderer/pipeline/ingest modules
- `src/modu_semantic/`: compatibility shim package
- `schema/`: semantic, layout, renderer, and contract schema/profile assets
- `examples/problems/0001/`: representative end-to-end sample bundle
- `tests/`: focused core-pipeline tests only
- `docs/`: keep list and clean-core migration report

## Quick Start

```bash
uv run python -c "import modu_math; print(modu_math.__file__)"
uv run python -m modu_math --help
uv run pytest
```

## Example Artifacts

`examples/problems/0001/` contains the canonical sample names:

- `input.png`
- `vision_draft.md` (optional assistant artifact)
- `refined_draft.md` (optional assistant artifact)
- `problem.dsl.py`
- `problem.semantic.json`
- `problem.solvable.json`
- `problem.layout.json`
- `problem.renderer.json`
- `problem.svg`

## Recommended Commands

```bash
uv run python tools/generate_vision_draft.py \
  --image examples/problems/0001/input.png \
  --problem-id 0001 \
  --out examples/problems/0001/vision_draft.md \
  --force

uv run python tools/refine_vision_draft.py \
  --vision-draft examples/problems/0001/vision_draft.md \
  --image examples/problems/0001/input.png \
  --problem-id 0001 \
  --out examples/problems/0001/refined_draft.md \
  --force

uv run python tools/generate_dsl_from_refined_draft.py \
  --draft examples/problems/0001/refined_draft.md \
  --image examples/problems/0001/input.png \
  --problem-id 0001 \
  --out examples/problems/0001/problem.dsl.py \
  --force

uv run python tools/validate_generated_dsl.py \
  --dsl examples/problems/0001/problem.dsl.py \
  --strict
```

Legacy/direct fallback for quick experiments (no draft files required):

```bash
uv run python tools/generate_dsl_from_png.py \
  --image examples/problems/0001/input.png \
  --problem-id 0001 \
  --out examples/problems/0001/problem.dsl.py \
  --force
```

Do not edit generated JSON/SVG by hand. Edit `problem.dsl.py` first.
If `refined_draft.md` conflicts with the image, trust the image for visible truth.
If DSL conflicts with semantic meaning, fix `problem.dsl.py` and rebuild.
