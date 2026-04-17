from __future__ import annotations

from ...primitives import Line, Polygon, Text
from ...problem import Problem


def triangle_area_problem(problem_id: str = "triangle_area_001") -> Problem:
    p = Problem(
        width=800,
        height=600,
        problem_id=problem_id,
        problem_type="triangle_area",
        title="삼각형의 넓이",
    )

    p.add(
        Polygon(
            id="triangle",
            points=[(180, 420), (420, 420), (300, 220)],
            stroke="#000000",
            stroke_width=2,
            semantic_role="main_shape",
        )
    )
    p.add(
        Line(
            id="base_hint",
            x1=180,
            y1=450,
            x2=420,
            y2=450,
            stroke="#000000",
            stroke_width=1,
            semantic_role="base_hint",
        )
    )
    p.add(
        Text(
            id="instruction",
            x=80,
            y=80,
            text="삼각형의 넓이를 구하시오.",
            font_size=24,
            semantic_role="instruction",
        )
    )

    return p
