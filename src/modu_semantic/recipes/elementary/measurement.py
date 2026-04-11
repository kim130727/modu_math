from __future__ import annotations

from ...primitives import Text
from ...problem import Problem


def length_compare_problem(problem_id: str = "length_compare_001") -> Problem:
    p = Problem(
        width=800,
        height=600,
        problem_id=problem_id,
        problem_type="measurement",
        title="길이 비교",
    )
    p.add(Text(id="q", x=90, y=140, text="35cm 와 0.4m 중 더 긴 것은?", font_size=28, semantic_role="question"))
    return p
