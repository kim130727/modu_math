from __future__ import annotations

from ...primitives import Text
from ...problem import Problem


def elapsed_time_problem(problem_id: str = "elapsed_time_001") -> Problem:
    p = Problem(
        width=800,
        height=600,
        problem_id=problem_id,
        problem_type="time",
        title="걸린 시간",
    )
    p.add(Text(id="q", x=90, y=140, text="오전 9:20 시작, 11:05 종료. 걸린 시간은?", font_size=24, semantic_role="question"))
    return p
