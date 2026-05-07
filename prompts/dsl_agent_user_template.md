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
- Include Korean text exactly as seen when possible
- Semantic should be concise and domain/answer-centered (avoid slot-by-slot semantic mirroring)
- Include layout intent sufficient for modu_math to render a similar SVG
- SOLVABLE must include schema/problem_id and non-empty plan/steps/checks
- Do not directly create semantic JSON, layout JSON, renderer JSON, or SVG
- Do not place renderer-specific details inside semantic meaning
- Add TODO comments for uncertain OCR/image details
