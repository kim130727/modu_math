Problem ID: {problem_id}
Input: attached PNG image

Generate a complete `problem.dsl.py` draft for this one math problem image.

Requirements:
- Python code only
- No markdown fence
- No explanation
- Include the problem_id
- `SEMANTIC_OVERRIDE` dict is mandatory
- `SOLVABLE` dict is mandatory
- Use `SOLVABLE["schema"] = "modu.solvable.v1.3"`
- `ProblemTemplate.id`, `SEMANTIC_OVERRIDE["problem_id"]`, and `SOLVABLE["problem_id"]` must all equal `{problem_id}`
- Include Korean text exactly as seen when possible
- Semantic should be concise and domain/answer-centered (avoid slot-by-slot semantic mirroring)
- Include layout intent sufficient for modu_math to render a similar SVG
- SOLVABLE must include schema/problem_id/given/target/method/steps/answer
- SOLVABLE may include problem_type, plan, checks, and diagnostics only when useful
- Do not repeat given as inputs or understanding.facts, and do not repeat target as understanding.unknowns
- Use diagnostics.skills for short concept codes and diagnostics.errors for student_response -> common_error_code
- `SEMANTIC_OVERRIDE["answer"]` and `SOLVABLE["answer"]` must match for strict validation
- Do not directly create semantic JSON, layout JSON, renderer JSON, or SVG
- Do not place renderer-specific details inside semantic meaning
- Add TODO comments for uncertain OCR/image details
