# CLEAN_CORE_REPORT

## 1) Files Copied

### Root
- README.md (rewritten for clean core)
- pyproject.toml
- uv.lock
- .gitignore

### Core package
- src/modu_math/__init__.py
- src/modu_math/__main__.py
- src/modu_math/cli.py
- src/modu_math/dsl/
- src/modu_math/adapters/
- src/modu_math/semantic/
- src/modu_math/layout/
- src/modu_math/renderer/
- src/modu_math/pipeline/
- src/modu_math/ingest/

### Compatibility
- src/modu_semantic/

### Schemas
- schema/semantic/
- schema/layout/
- schema/renderer/
- schema/contract/

### Example problem
- examples/problems/0001/input.png (from sample_data/problems/raw/0001/0001.png)
- examples/problems/0001/problem.dsl.py
- examples/problems/0001/problem.semantic.json (from 0001.semantic.json)
- examples/problems/0001/problem.layout.json (from 0001.layout.json)
- examples/problems/0001/problem.renderer.json (from 0001.renderer.json)
- examples/problems/0001/problem.svg (from 0001.svg)

### Tests kept (core-focused)
- tests/dsl/test_compiler_to_layout.py
- tests/dsl/test_exporter.py
- tests/dsl/test_fraction_slots.py
- tests/test_renderer_compiler_from_layout.py
- tests/test_core_pipeline.py (added for package import, CLI smoke, semantic/layout/renderer/SVG + contract validation)

### Docs added
- docs/CORE_KEEP_LIST.md
- docs/CLEAN_CORE_REPORT.md

## 2) Files Intentionally Not Copied

- RAG-related modules/tests/files
- OCR experiment scripts and reports
- GPT/VLM experiment scripts and prompts
- webapp/
- reports/
- scratch/tools not needed for core pipeline
- experimental/editor/roundtrip tests not required for core pipeline
- .codex/, .gemini/
- caches and build artifacts: __pycache__, .pytest_cache, .ruff_cache, dist, build

## 3) Commands Run

From inside `_clean_core`:

1. `uv run python -c "import modu_math; print(modu_math.__file__)"`
2. `uv run python -m modu_math --help`
3. `uv run pytest`

Also used for diagnosis/fix verification:

- `uv run python -c "...compile_problem_template_to_layout(...); print(slot)..."`
- `uv run pytest` (rerun after fixes)

## 4) Test Results

- Initial run:
  - Import command failed: `ModuleNotFoundError: No module named 'modu_math.editor'` from `pipeline/compile_problem.py`.
  - CLI help command failed for same reason.
  - `uv run pytest` failed initially because `pytest` was not installed in `_clean_core` environment.

- Fixes applied inside `_clean_core` only:
  - `_clean_core/src/modu_math/pipeline/compile_problem.py`
    - Removed hard runtime dependency on `modu_math.editor` by making `EditorState` type-only.
  - `_clean_core/pyproject.toml`
    - Added `pytest>=8.0.0` to dependencies for `uv run pytest`.
  - `_clean_core/tests/dsl/test_fraction_slots.py`
    - Updated assertion to match current layout output shape (`content` instead of `geometry`).

- Final verification:
  - `uv run python -c "import modu_math; print(modu_math.__file__)"` passed.
  - `uv run python -m modu_math --help` passed.
  - `uv run pytest` passed: `14 passed in 0.33s`.

## 5) Remaining TODOs

- Consider slimming `_clean_core/pyproject.toml` dependencies further if Django is not needed for this core pipeline runtime.
- Optionally add a dedicated end-to-end fixture test that writes semantic/layout/renderer/SVG files from `examples/problems/0001/problem.dsl.py` and validates outputs against schemas.
- Decide whether to keep or remove legacy `build-semantic` CLI behavior if long-term goal is pure core pipeline only.
