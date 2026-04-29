Problem ID: {problem_id}
Input: attached PNG image

Return Python code only.
You must generate a valid modu_math ProblemTemplate module.
Hard requirements:
- from __future__ import annotations
- from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot, CircleSlot, RectSlot, LineSlot, PolygonSlot
- define def build_problem_template() -> ProblemTemplate
- return ProblemTemplate(id="{problem_id}", title=..., canvas=Canvas(...), regions=(...), slots=(...))
- use only these slot classes: TextSlot, CircleSlot, RectSlot, LineSlot, PolygonSlot
- do not use ParagraphRegion, Diagram, problem.semantic, problem.layout, or dict-based DSL
- include PROBLEM_TEMPLATE = build_problem_template()
- if unsure, prefer fewer slots but valid code
