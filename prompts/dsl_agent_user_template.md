Problem ID: {problem_id}
Input: attached PNG image

Generate a complete `problem.dsl.py` draft for this one math problem image.

Requirements:
- Python code only
- No markdown fence
- No explanation
- Include the problem_id
- Include Korean text exactly as seen when possible
- Include semantic information needed to solve the problem
- Include layout intent sufficient for modu_math to render a similar SVG
- Do not directly create semantic JSON, layout JSON, renderer JSON, or SVG
- Do not place renderer-specific details inside semantic meaning
- Add TODO comments for uncertain OCR/image details
