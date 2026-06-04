# Core Keep List

## Root Files

- README.md
- pyproject.toml
- uv.lock
- .gitignore

## Core Source

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

## Compatibility

- src/modu_semantic/

## Schemas

- schema/semantic/
- schema/layout/
- schema/renderer/
- schema/contract/

## Examples

- examples/problems/0001/input.png
- examples/problems/0001/problem.dsl.py
- examples/problems/0001/problem.semantic.json
- examples/problems/0001/problem.layout.json
- examples/problems/0001/problem.renderer.json
- examples/problems/0001/problem.svg

## Tests (Core-Focused)

- tests/dsl/test_compiler_to_layout.py
- tests/dsl/test_exporter.py
- tests/dsl/test_fraction_slots.py
- tests/test_renderer_compiler_from_layout.py
- tests/test_core_pipeline.py
