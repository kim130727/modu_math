import json
from pathlib import Path

from modu_semantic.ir import Formula, Line, Rect, Text
from modu_semantic.problem import Problem


GOLDEN_JSON = Path("tests/goldens/0001/semantic.json")
GOLDEN_LAYOUT_JSON = Path("tests/goldens/0001/layout.json")


def build_sample_problem() -> Problem:
    p = Problem(width=800, height=600, problem_id="sample_001", problem_type="demo_geometry")
    p.add(
        Rect(
            id="box1",
            x=100,
            y=120,
            width=220,
            height=120,
            stroke="#222222",
            stroke_width=2,
            fill="#F5F5F5",
            group="question",
            z_index=1,
        )
    )
    p.add(
        Text(
            id="title",
            x=120,
            y=160,
            text="삼각형의 넓이",
            font_size=24,
            fill="#111111",
            anchor="start",
            group="question",
            z_index=2,
        )
    )
    p.add(
        Line(
            id="divider",
            x1=100,
            y1=190,
            x2=320,
            y2=190,
            stroke="#666666",
            stroke_width=1,
            z_index=2,
        )
    )
    p.add(
        Formula(
            id="eq1",
            x=120,
            y=220,
            expr="A = (b * h) / 2",
            font_size=20,
            fill="#111111",
            group="question",
            z_index=2,
        )
    )
    return p


def test_semantic_json_matches_golden() -> None:
    actual = build_sample_problem().to_semantic_json()
    expected = json.loads(GOLDEN_JSON.read_text(encoding="utf-8"))
    assert actual == expected


def test_layout_json_matches_golden() -> None:
    actual = build_sample_problem().to_layout_json()
    expected = json.loads(GOLDEN_LAYOUT_JSON.read_text(encoding="utf-8"))
    assert actual == expected


