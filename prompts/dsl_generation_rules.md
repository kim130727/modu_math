# DSL Generation Rules

## Terminology Guard

- `source problem json`: original dataset JSON paired with the input PNG.
- `problem.dsl.py`: human-editable canonical authoring source.
- `semantic/layout/renderer/solvable json`: generated pipeline artifacts derived from DSL.
- `SVG`: derived renderer output only.

Never confuse `source problem json` with generated semantic/layout/renderer JSON.
If source JSON contains answer or explanation text, use it only in `SEMANTIC_OVERRIDE` and `SOLVABLE`.
Do not place source-json answer/explanation text in visible layout slots unless it is visibly printed in the image.

## 1) Required Module Shape

The output must be valid Python code only. Do not output markdown fences or explanations.

Every generated DSL module must include:

- `from __future__ import annotations`
- imports from `modu_math.dsl` only
- `def build_problem_template() -> ProblemTemplate:`
- `PROBLEM_TEMPLATE = build_problem_template()`
- `SEMANTIC_OVERRIDE = {...}`
- `SOLVABLE = {...}`

`ProblemTemplate(...)` must use:

- `id=...`
- `title=...`
- `canvas=Canvas(...)`
- `regions=(...)`
- `slots=(...)`

Use `id=`, not `problem_id=`.

## 2) Allowed Authoring Surface

Allowed slot classes include:

- `TextSlot`
- `TextBoxSlot`
- `ChoiceSlot`
- `BlankSlot`
- `LabelSlot`
- `RectSlot`
- `LineSlot`
- `CircleSlot`
- `PolygonSlot`
- `PathSlot`
- `ImageSlot`

Allowed helpers include current exports from `modu_math.dsl`, especially when they simplify visible repeated structures:

- `fraction_slots`
- `table_slots`
- `ruler_slots`
- `compass_slots`
- `compass_on_ruler_slots`
- paper-folding helpers
- speaker/person/place helpers

Prefer readable helper use over hundreds of hand-written primitive slots when the helper accurately represents the visible diagram.

## 3) Layout Rules

- Define meaningful `Region(...)` entries and put visible content into `slots=(...)`.
- Keep slot ids stable and readable, such as `slot.question.1`, `slot.diagram.circle`, `slot.choice.1.label`.
- Use visible worksheet text exactly as shown.
- Use Korean text directly in UTF-8.
- Keep ordinary labels as `TextSlot`.
- Use `TextBoxSlot` only when a fixed PowerPoint-like text box is needed.
- Use `PathSlot` for arcs, curves, irregular shapes, folded paper, or shapes not represented by simpler primitives.
- Add TODO comments for uncertain OCR or unclear image details.
- Prefer valid, maintainable layout intent over pixel-perfect overfitting.

## 4) Forbidden Patterns

Do not use:

- legacy or unknown classes such as `ParagraphRegion` or custom `Diagram` wrappers
- `from modu_math import ProblemTemplate`
- `problem.semantic = ...`
- `problem.layout = ...`
- `problem.renderer = ...`
- generated semantic/layout/renderer JSON directly in the file
- generated SVG directly in the file

Do not put layout-only coordinates, colors, stroke widths, SVG paths, or renderer details into semantic meaning.

## 5) Semantic Override

`SEMANTIC_OVERRIDE` is mandatory and should be concise, domain-centered, and answer-centered.

Required top-level fields:

- `problem_id`: must match `ProblemTemplate.id`
- `problem_type`
- `domain`: object
- `answer`: object

Recommended fields:

- `metadata.language`
- `metadata.question`
- `metadata.instruction`
- `domain.objects`
- `domain.relations`
- `domain.problem_solving`

`domain.problem_solving` is a lightweight meaning-level hint, not a worked solution. Use this shape when helpful:

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
```

Rules:

- Keep semantic objects solve-relevant.
- Avoid slot-by-slot semantic mirroring.
- Use object/relation refs from `domain.objects` and `domain.relations` when possible.
- Put concrete arithmetic or selection steps in `SOLVABLE["steps"]`, not in semantic.
- Do not put final computed values inside `domain.problem_solving`.

## 6) Solvable Contract

`SOLVABLE` is mandatory and must use the current manual-pipeline schema:

```python
SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "...",
    "problem_type": "...",
    "inputs": {},
    "plan": [],
    "steps": [
        {
            "id": "step.1",
            "expr": "...",
            "value": "...",
        }
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "...",
            "expected": "...",
            "actual": "...",
            "pass": True,
        }
    ],
    "answer": {
        "value": "...",
        "unit": "",
        "derived_from": "step.1",
    },
}
```

Rules:

- `SOLVABLE["schema"]` must be exactly `"modu.solvable.v1.1"`.
- `SOLVABLE["problem_id"]` must match `ProblemTemplate.id`.
- `inputs`, `plan`, `steps`, `checks`, and `answer` must be present.
- Every step must include at least `id`, `expr`, and `value`.
- Every check must include at least `id`, `expr`, `expected`, `actual`, and `pass`.
- Use conservative explicit placeholders plus TODO comments when a value is uncertain.
- Keep `SOLVABLE` small and verifiable.
- For geometry problems, include the geometric reason behind any non-obvious relation in `SOLVABLE["steps"][].explanation` or `SOLVABLE["plan"]`; for example, explain why an inscribed regular hexagon has side length equal to the circle radius before using that relation.

## 7) Answer Synchronization

Strict validation compares `SEMANTIC_OVERRIDE["answer"]` and `SOLVABLE["answer"]`.
They must match as answer payloads.

Recommended pattern:

```python
SEMANTIC_OVERRIDE = {
    ...
    "answer": {
        "value": "...",
        "unit": "",
        "derived_from": "step.1",
    },
}

SOLVABLE = {
    ...
    "answer": {
        "value": "...",
        "unit": "",
        "derived_from": "step.1",
    },
}
```

If the answer is unknown, do not set one answer to `None` and the other to a computed value. Use a matching placeholder and add a TODO comment.

## 8) Manual Pipeline Fit

Generated DSL must be ready for:

```powershell
uv run python tools/validate_generated_dsl.py --dsl <problem.dsl.py> --strict --emit-solvable
```

This means:

- `ProblemTemplate.id`, `SEMANTIC_OVERRIDE["problem_id"]`, and `SOLVABLE["problem_id"]` match.
- `SOLVABLE` validates against `schema/solvable/solvable.v1.1.json`.
- semantic answer and solvable answer match.
- semantic remains meaning-only.
- layout/renderer/SVG remain generated artifacts.
