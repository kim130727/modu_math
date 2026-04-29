# DSL Generation Rules (Draft v2)

This rulebook is distilled from validated DSL examples under `examples/problems/260427/*.dsl.py`.
Follow this before writing any code.

## 1) Required Module Shape
- Must be valid Python.
- Must include:
  - `from __future__ import annotations`
  - import from `modu_math.dsl`
  - `def build_problem_template() -> ProblemTemplate:`
  - `PROBLEM_TEMPLATE = build_problem_template()`
- `ProblemTemplate(...)` must use:
  - `id=...`
  - `title=...`
  - `canvas=Canvas(...)`
  - `regions=(...)`
  - `slots=(...)`

## 2) Allowed Core Authoring Pattern
- Define at least one `Region(...)` and put all visible content into `slots=(...)`.
- Prefer explicit slot ids:
  - question lines: `slot.q1`, `slot.q2`, ...
  - diagram/grid nodes: `slot.grid.*`, `slot.pt.*`, `slot.lb.*`

## 3) Allowed Slot Classes
- `TextSlot`
- `RectSlot`
- `CircleSlot`
- `LineSlot`
- `PolygonSlot`
- `PathSlot` (only if needed)

## 4) Forbidden Patterns
- Do not use legacy/unknown classes (examples: `ParagraphRegion`, custom `Diagram` wrappers).
- Do not use `problem_id=` in `ProblemTemplate(...)`; use `id=`.
- Do not assign `problem.semantic = ...`, `problem.layout = ...`, `problem.renderer = ...`.
- Do not output json/svg directly in this file.

## 5) Semantic/Solvable Enrichment (Preferred)
When enough information is visible:
- Add `SEMANTIC_OVERRIDE = {...}` with:
  - `problem_type`
  - `metadata.question` and `metadata.instruction`
  - solve-relevant `domain.objects` / `domain.relations`
  - `answer`
- Add `SOLVABLE = {...}` with schema `modu.solvable.v1`.

Keep semantic meaning-focused:
- Avoid duplicating layout-only coordinates/styles into domain objects.
- Use equations/constraints/target relations.

## 6) Layout Guidance
- If uncertain on typography, default `font_size=28`.
- Keep labels and points visually separated.
- Keep coordinates simple and stable; avoid overfitting.

## 6-1) Grid Pattern Rule (Geometry Dot Problems)
- When the image clearly includes a dotted grid, represent it explicitly with `LineSlot` only.
- Build grid as two line families:
  - vertical: `slot.grid.v1`, `slot.grid.v2`, ...
  - horizontal: `slot.grid.h1`, `slot.grid.h2`, ...
- Use stable styling for school worksheet grids:
  - `stroke="#9AA0A6"`
  - `stroke_width=1.2`
  - `stroke_dasharray="5 3"`
- Keep grid spacing uniform. Extend width/height by whole-cell increments only.

## 6-2) Point-on-Grid Rule
- Plot marked points with `CircleSlot(cx=..., cy=..., r=...)`.
- Never use legacy `CircleSlot(x=..., y=...)`.
- Recommended defaults:
  - `r` around `3.5 ~ 4.0`
  - `fill="#222222"`
- Korean point labels (`ㄱ`, `ㄴ`, `ㄷ`, `ㄹ`, `ㅁ`) should be separate `TextSlot`s, not merged into point ids.

## 6-3) Slot Signature Guard
- `style_role` is valid only for `TextSlot`.
- For non-text slots (`RectSlot`, `LineSlot`, `CircleSlot`, `PolygonSlot`, `PathSlot`), do not emit `style_role`.
- Prefer current keyword signatures from `src/modu_math/dsl/models/base.py`.

## 7) Minimal Valid Skeleton
```python
from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot

def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="PROBLEM_ID",
        title="문제 제목",
        canvas=Canvas(width=560, height=520, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q1",),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="문제 문장",
                style_role="question",
                x=12.0,
                y=48.0,
                font_size=28,
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )

PROBLEM_TEMPLATE = build_problem_template()
```

## 8) Continuous Hardening Process
After each successful manual fix:
- Add one short, testable rule from that incident.
- Add a short snippet if the pattern is reusable.
- Keep rules concise and verifiable by local validators.

## 9) Operational Safety Rule
- Do not recover source DSL from `__pycache__` as an automatic generation path.
- `__pycache__` recovery is allowed only as a manual emergency step and must be followed by full visual/semantic review.
