Problem ID: {problem_id}
Input: attached PNG image

Return Python code only.
You must generate a valid modu_math ProblemTemplate module.
Hard requirements:
- from __future__ import annotations
- import required authoring classes/helpers from modu_math.dsl only
- define def build_problem_template() -> ProblemTemplate
- return ProblemTemplate(id="{problem_id}", title=..., canvas=Canvas(...), regions=(...), slots=(...))
- allowed slot classes include TextSlot, TextBoxSlot, CircleSlot, RectSlot, LineSlot, PolygonSlot, PathSlot, ImageSlot, ChoiceSlot, BlankSlot, LabelSlot
- allowed helpers include fraction_slots, table_slots, ruler_slots, compass_slots, compass_on_ruler_slots, paper-folding helpers, speaker/person/place helpers when they simplify visible diagrams
- do not use ParagraphRegion, Diagram, problem.semantic, problem.layout, or dict-based DSL
- include PROBLEM_TEMPLATE = build_problem_template()
- include SEMANTIC_OVERRIDE dict after PROBLEM_TEMPLATE
- include SOLVABLE dict after SEMANTIC_OVERRIDE
- use SOLVABLE["schema"] = "modu.solvable.v1.1"
- ProblemTemplate.id, SEMANTIC_OVERRIDE["problem_id"], and SOLVABLE["problem_id"] must all equal "{problem_id}"
- SEMANTIC_OVERRIDE["answer"] and SOLVABLE["answer"] must match for strict validation
- if unsure, prefer fewer slots but valid code
- keep SEMANTIC_OVERRIDE meaning-only and keep actual calculation steps in SOLVABLE
