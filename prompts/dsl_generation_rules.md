네. 아래는 **`dsl_generation_rules.md` 최종완성본**입니다.
현재 올려주신 파일은 `5-1`의 Python 코드블록이 닫히지 않아 `## 6)` 이후가 코드블록 안으로 들어가는 문제가 있습니다. 그 부분까지 수정해서 완성했습니다. 

````md
# DSL Generation Rules (Draft v3)

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
- Keep the DSL readable and maintainable.
- Prefer stable, simple layout intent over pixel-perfect overfitting.

## 3) Allowed Slot Classes

- `TextSlot`
- `RectSlot`
- `CircleSlot`
- `LineSlot`
- `PolygonSlot`
- `PathSlot` only if needed

## 4) Forbidden Patterns

- Do not use legacy/unknown classes.
  - Examples: `ParagraphRegion`, custom `Diagram` wrappers.
- Do not use `problem_id=` in `ProblemTemplate(...)`; use `id=`.
- Do not assign:
  - `problem.semantic = ...`
  - `problem.layout = ...`
  - `problem.renderer = ...`
- Do not output JSON or SVG directly in this file.
- Do not put renderer-specific details inside semantic meaning.
- Do not put SVG paths, stroke widths, colors, or coordinates into semantic objects.

## 5) Semantic/Solvable Enrichment (Preferred)

When enough information is visible, add optional constants after `PROBLEM_TEMPLATE`:

- `SEMANTIC_OVERRIDE = {...}`
- `SOLVABLE = {...}`

`SEMANTIC_OVERRIDE` should contain:

- `problem_id`
- `problem_type`
- `metadata.question`
- `metadata.instruction`
- solve-relevant `domain.objects`
- solve-relevant `domain.relations`
- `domain.problem_solving` if useful
- `answer`

`SOLVABLE` should contain:

- `schema`
- `problem_id`
- `problem_type`
- `given`
- `target`
- `method`
- `steps`
- `checks`
- `answer`

Keep semantic meaning-focused:

- Avoid duplicating layout-only coordinates/styles into domain objects.
- Use equations, constraints, quantities, objects, and target relations.
- In semantic, describe what the problem means.
- In solvable, describe how the problem is actually solved.

## 5-1) Problem-Solving Hint Rule

When enough information is visible, `SEMANTIC_OVERRIDE["domain"]` may include a lightweight `problem_solving` block.

This block is inspired by the four problem-solving stages:

1. understand
2. plan
3. execute
4. review

Use this shape:

```python
"problem_solving": {
    "understand": {
        "given_refs": [],
        "target_ref": "answer.target",
        "condition_refs": [],
    },
    "plan": {
        "method": "",
        "description": "",
    },
    "execute": {
        "expected_operations": [],
    },
    "review": {
        "check_methods": [],
    },
}
````

Rules:

* `problem_solving` belongs inside semantic `domain`.
* It is a meaning-level solving hint, not the actual worked solution.
* Do not put detailed arithmetic steps in semantic `problem_solving`.
* Do not put final computed values in semantic `problem_solving`.
* Do not put layout coordinates, renderer styles, SVG paths, or visual slot ids in `problem_solving`.
* Use object/relation refs from `domain.objects` and `domain.relations` when possible.
* Put actual calculated steps in `SOLVABLE["steps"]`.
* Put the final computed value in `SOLVABLE["answer"]`.
* In `SEMANTIC_OVERRIDE["answer"]`, prefer `target` and leave `value` as `None` unless the answer is explicitly printed in the image.
* If uncertain, keep `problem_solving` minimal and add a TODO comment in the DSL instead of inventing a complete solution.

## 5-2) Minimal SOLVABLE Shape

When adding `SOLVABLE`, prefer this minimal shape:

```python
SOLVABLE = {
    "schema": "modu.solvable.v1",
    "problem_id": "...",
    "problem_type": "...",
    "given": [],
    "target": {},
    "method": "",
    "steps": [],
    "checks": [],
    "answer": {},
}
```

Rules:

* `given` should be derived from semantic domain objects.
* `target` should match `SEMANTIC_OVERRIDE["answer"]["target"]`.
* `method` should match `SEMANTIC_OVERRIDE["domain"]["problem_solving"]["plan"]["method"]` when available.
* `steps` should contain concrete operations and values.
* `checks` should verify the final answer, inverse relation, or unit consistency.
* `answer.value` should be derived from the last relevant step.
* Keep `SOLVABLE` small and verifiable.
* Do not force a full solution when the image is ambiguous.
* If the solution cannot be derived confidently, leave TODO comments and use conservative values.

## 5-3) Semantic Answer vs Solvable Answer

Use this distinction:

* `SEMANTIC_OVERRIDE["answer"]` describes what must be found.
* `SOLVABLE["answer"]` contains the computed result.

Recommended semantic answer shape:

```python
"answer": {
    "target": {
        "type": "",
        "description": "",
    },
    "value": None,
    "unit": "",
}
```

Recommended solvable answer shape:

```python
"answer": {
    "value": None,
    "unit": "",
    "derived_from": "",
}
```

Rules:

* If the answer is printed in the image, semantic `answer.value` may be filled.
* If the answer must be computed, semantic `answer.value` should usually be `None`.
* The computed value should appear in `SOLVABLE["answer"]["value"]`.
* `SOLVABLE["answer"]["derived_from"]` should point to the step that produced the answer when possible.

## 5-4) Example Semantic/Solvable Pattern

Example pattern for a time-addition problem:

```python
SEMANTIC_OVERRIDE = {
    "problem_id": "time_0001",
    "problem_type": "time_addition",
    "metadata": {
        "language": "ko",
        "question": "17분 25초에서 36분 47초 후의 시각을 구하는 문제",
        "instruction": "㉠+㉡+㉢을 구하시오.",
    },
    "domain": {
        "objects": [
            {
                "id": "obj.start_time",
                "type": "time",
                "minute": 17,
                "second": 25,
            },
            {
                "id": "obj.duration",
                "type": "duration",
                "minute": 36,
                "second": 47,
            },
        ],
        "relations": [
            {
                "id": "rel.add_duration",
                "type": "time_after",
                "from": "obj.start_time",
                "duration": "obj.duration",
                "result": "obj.end_time",
            },
        ],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.start_time", "obj.duration"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.add_duration"],
            },
            "plan": {
                "method": "unit_carrying",
                "description": "초를 먼저 더하고 60초 이상이면 분으로 올림한 뒤, 분을 더한다.",
            },
            "execute": {
                "expected_operations": [
                    "add_seconds",
                    "carry_seconds_to_minutes",
                    "add_minutes",
                    "sum_answer_parts",
                ],
            },
            "review": {
                "check_methods": [
                    "unit_consistency_check",
                    "reverse_duration_check",
                ],
            },
        },
    },
    "answer": {
        "target": {
            "type": "sum_of_time_parts",
            "description": "㉠+㉡+㉢",
            "components": ["hour", "minute", "second"],
        },
        "value": None,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1",
    "problem_id": "time_0001",
    "problem_type": "time_addition",
    "given": [
        {
            "ref": "obj.start_time",
            "value": {
                "minute": 17,
                "second": 25,
            },
        },
        {
            "ref": "obj.duration",
            "value": {
                "minute": 36,
                "second": 47,
            },
        },
    ],
    "target": {
        "ref": "answer.target",
        "type": "sum_of_time_parts",
    },
    "method": "unit_carrying",
    "steps": [
        {
            "id": "step.s1",
            "operation": "add_seconds",
            "expr": "25 + 47",
            "value": 72,
        },
        {
            "id": "step.s2",
            "operation": "carry_seconds_to_minutes",
            "expr": "72초 = 1분 12초",
            "value": {
                "carry_minute": 1,
                "second": 12,
            },
        },
        {
            "id": "step.s3",
            "operation": "add_minutes",
            "expr": "17 + 36 + 1",
            "value": 54,
        },
        {
            "id": "step.s4",
            "operation": "sum_answer_parts",
            "expr": "0 + 54 + 12",
            "value": 66,
        },
    ],
    "checks": [
        {
            "id": "check.c1",
            "type": "unit_consistency_check",
            "pass": True,
        },
    ],
    "answer": {
        "value": 66,
        "unit": "",
        "derived_from": "step.s4",
    },
}
```

## 6) Layout Guidance

* If uncertain on typography, default `font_size=28`.
* Keep labels and points visually separated.
* Keep coordinates simple and stable.
* Avoid overfitting to exact pixels.
* Prefer logical layout intent that can survive renderer changes.
* Layout slots may contain coordinates and visual placement.
* Semantic objects must not contain layout coordinates.

## 6-1) Grid Pattern Rule (Geometry Dot Problems)

* When the image clearly includes a dotted grid, represent it explicitly with `LineSlot` only.
* Build grid as two line families:

  * vertical: `slot.grid.v1`, `slot.grid.v2`, ...
  * horizontal: `slot.grid.h1`, `slot.grid.h2`, ...
* Use stable styling for school worksheet grids:

  * `stroke="#9AA0A6"`
  * `stroke_width=1.2`
  * `stroke_dasharray="5 3"`
* Keep grid spacing uniform.
* Extend width/height by whole-cell increments only.

## 6-2) Point-on-Grid Rule

* Plot marked points with `CircleSlot(cx=..., cy=..., r=...)`.
* Never use legacy `CircleSlot(x=..., y=...)`.
* Recommended defaults:

  * `r` around `3.5 ~ 4.0`
  * `fill="#222222"`
* Korean point labels such as `ㄱ`, `ㄴ`, `ㄷ`, `ㄹ`, `ㅁ` should be separate `TextSlot`s.
* Do not merge point labels into point ids.

## 6-3) Slot Signature Guard

* `style_role` is valid only for `TextSlot`.
* For non-text slots, do not emit `style_role`.
* This applies to:

  * `RectSlot`
  * `LineSlot`
  * `CircleSlot`
  * `PolygonSlot`
  * `PathSlot`
* Prefer current keyword signatures from `src/modu_math/dsl/models/base.py`.

## 6-4) Circle Slot Rule

Use current `CircleSlot` signature:

```python
CircleSlot(
    id="slot.pt.a",
    prompt="",
    cx=100.0,
    cy=120.0,
    r=4.0,
    fill="#222222",
)
```

Do not use:

```python
CircleSlot(
    id="slot.pt.a",
    x=100.0,
    y=120.0,
)
```

## 6-5) Text Slot Rule

Use `TextSlot` for all visible Korean text, labels, numbers, operators, and instructions.

Recommended pattern:

```python
TextSlot(
    id="slot.q1",
    prompt="",
    text="문제 문장",
    style_role="question",
    x=12.0,
    y=48.0,
    font_size=28,
)
```

Rules:

* Use UTF-8 Korean text directly.
* Do not use unicode escape sequences for Korean unless unavoidable.
* If OCR is uncertain, add a TODO comment.
* Keep text slots separate from diagram slots.

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

## 8) Minimal Valid Skeleton With Semantic/Solvable

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


SEMANTIC_OVERRIDE = {
    "problem_id": "PROBLEM_ID",
    "problem_type": "unknown",
    "metadata": {
        "language": "ko",
        "question": "",
        "instruction": "",
    },
    "domain": {
        "objects": [],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": [],
                "target_ref": "answer.target",
                "condition_refs": [],
            },
            "plan": {
                "method": "",
                "description": "",
            },
            "execute": {
                "expected_operations": [],
            },
            "review": {
                "check_methods": [],
            },
        },
    },
    "answer": {
        "target": {
            "type": "",
            "description": "",
        },
        "value": None,
        "unit": "",
    },
}


SOLVABLE = {
    "schema": "modu.solvable.v1",
    "problem_id": "PROBLEM_ID",
    "problem_type": "unknown",
    "given": [],
    "target": {},
    "method": "",
    "steps": [],
    "checks": [],
    "answer": {},
}
```

## 9) Continuous Hardening Process

After each successful manual fix:

* Add one short, testable rule from that incident.
* Add a short snippet if the pattern is reusable.
* Keep rules concise and verifiable by local validators.
* Prefer adding narrow guardrails over broad vague instructions.

## 10) Operational Safety Rule

* Do not recover source DSL from `__pycache__` as an automatic generation path.
* `__pycache__` recovery is allowed only as a manual emergency step.
* Any recovered source must be followed by full visual and semantic review.
* Do not treat visual SVG similarity as proof of semantic correctness.

## 11) Pipeline Assumption

Canonical authoring pipeline:

```text
PNG -> Python DSL -> semantic JSON -> solvable JSON -> layout JSON -> renderer JSON -> SVG
```

Artifact roles:

* `problem.dsl.py`: human-editable canonical authoring source
* `problem.semantic.json`: meaning contract
* `problem.solvable.json`: concrete solution/check contract
* `problem.layout.json`: structure and placement contract
* `problem.renderer.json`: drawable contract
* `problem.svg`: derived visual artifact

Rules:

* Edit `problem.dsl.py` first.
* Regenerate JSON/SVG artifacts from DSL.
* Do not manually edit generated JSON unless doing emergency repair.
* Do not use SVG as the source of mathematical meaning.