# modu_math Clean Core

This directory is an isolated core copy of `modu_math` focused on the canonical pipeline:

`PNG -> semantic JSON -> Python DSL -> layout JSON -> renderer JSON -> SVG`

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
- `problem.dsl.py`
- `problem.semantic.json`
- `problem.layout.json`
- `problem.renderer.json`
- `problem.svg`
