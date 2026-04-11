from __future__ import annotations

from ...primitives import Text
from ...problem import Problem


def fraction_compare_problem(problem_id: str = "fraction_compare_001") -> Problem:
    p = Problem(
        width=800,
        height=600,
        problem_id=problem_id,
        problem_type="fraction_compare",
        title="분수 크기 비교",
    )
    p.add(Text(id="q", x=90, y=140, text="3/4 와 5/8 중 더 큰 수는?", font_size=28, semantic_role="question"))
    return p
