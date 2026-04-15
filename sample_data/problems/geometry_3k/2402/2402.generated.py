from __future__ import annotations

from pathlib import Path

from modu_semantic import Circle, Line, Problem, Rect, Text

# source semantic: 2402.semantic.json

PROBLEM_ID = "2402"
PROBLEM_TYPE = "Length::Circle"
TITLE_TEXT = "Circle O has a radius of 13 inches. Radius OB is perpendicular to chord CD which is 24 inches long. Find OX."
CANVAS_W = 1400.0
CANVAS_H = 900.0
CANVAS_BG = "#FFFFFF"
FONT_SCALE = 1.0


def build() -> Problem:
    p = Problem(width=int(CANVAS_W), height=int(CANVAS_H), background=CANVAS_BG, problem_id=PROBLEM_ID, problem_type=PROBLEM_TYPE)
    p.title = TITLE_TEXT
    p.set_metadata({'source': 'textbook2_chapter10.pdf page 19', 'warnings': []})
    p.set_domain({})
    p.set_answer(blanks=[], choices=['5', '12', '13', '26'], answer_key=[{'label': 'no.1', 'index': 0, 'value': '5'}])

    # elements
    p.add(
        Rect(
            id="geom_diagram_region",
            x=40.0,
            y=220.0,
            width=760.0,
            height=620.0,
            semantic_role="geometry_diagram_region",
            stroke="#D1D5DB",
            stroke_width=1.0,
            fill="none",
        )
    )

    p.add(
        Circle(
            id="geom_circle_O",
            cx=420.0,
            cy=560.0,
            r=250.0,
            semantic_role="geometry_shape",
            stroke="#1976D2",
            stroke_width=3.0,
            fill="none",
        )
    )

    p.add(
        Line(
            id="geom_line_CD",
            x1=307.93154823138207,
            y1=336.5259251765768,
            x2=669.5684517686179,
            y2=545.3170887827026,
            semantic_role="geometry_edge",
            stroke="#1976D2",
            stroke_width=3.0,
        )
    )

    p.add(
        Line(
            id="geom_line_OB",
            x1=420.0,
            y1=560.0,
            x2=545.0,
            y2=343.49364905389035,
            semantic_role="geometry_edge",
            stroke="#1976D2",
            stroke_width=3.0,
        )
    )

    p.add(
        Line(
            id="geom_line_OX",
            x1=420.0,
            y1=560.0,
            x2=488.75,
            y2=440.9215069796397,
            semantic_role="geometry_edge",
            stroke="#1976D2",
            stroke_width=3.0,
        )
    )

    p.add(
        Line(
            id="geom_line_OC",
            x1=420.0,
            y1=560.0,
            x2=307.93154823138207,
            y2=336.5259251765768,
            semantic_role="geometry_helper",
            stroke="#E91E63",
            stroke_width=3.0,
        )
    )

    p.add(
        Line(
            id="geom_perp_1",
            x1=499.75,
            y1=421.86894809638204,
            x2=518.8025588832577,
            y2=432.86894809638204,
            semantic_role="geometry_right_angle",
            stroke="#E91E63",
            stroke_width=3.0,
        )
    )

    p.add(
        Line(
            id="geom_perp_2",
            x1=518.8025588832577,
            y1=432.86894809638204,
            x2=507.80255888325763,
            y2=451.9215069796397,
            semantic_role="geometry_right_angle",
            stroke="#E91E63",
            stroke_width=3.0,
        )
    )

    p.add(
        Circle(
            id="geom_point_C",
            cx=307.93154823138207,
            cy=336.5259251765768,
            r=5.0,
            semantic_role="geometry_point",
            stroke="#0D47A1",
            stroke_width=1.5,
            fill="#0D47A1",
        )
    )

    p.add(
        Text(
            id="geom_label_C",
            x=317.93154823138207,
            y=326.5259251765768,
            text="C",
            font_size=48,
            semantic_role="geometry_point_label",
            fill="#1F1F1F",
            font_family="Malgun Gothic",
            anchor="start",
        )
    )

    p.add(
        Circle(
            id="geom_point_B",
            cx=545.0,
            cy=343.49364905389035,
            r=5.0,
            semantic_role="geometry_point",
            stroke="#0D47A1",
            stroke_width=1.5,
            fill="#0D47A1",
        )
    )

    p.add(
        Text(
            id="geom_label_B",
            x=555.0,
            y=333.49364905389035,
            text="B",
            font_size=48,
            semantic_role="geometry_point_label",
            fill="#1F1F1F",
            font_family="Malgun Gothic",
            anchor="start",
        )
    )

    p.add(
        Circle(
            id="geom_point_D",
            cx=669.5684517686179,
            cy=545.3170887827026,
            r=5.0,
            semantic_role="geometry_point",
            stroke="#0D47A1",
            stroke_width=1.5,
            fill="#0D47A1",
        )
    )

    p.add(
        Text(
            id="geom_label_D",
            x=679.5684517686179,
            y=535.3170887827026,
            text="D",
            font_size=48,
            semantic_role="geometry_point_label",
            fill="#1F1F1F",
            font_family="Malgun Gothic",
            anchor="start",
        )
    )

    p.add(
        Circle(
            id="geom_point_O",
            cx=420.0,
            cy=560.0,
            r=5.0,
            semantic_role="geometry_point",
            stroke="#0D47A1",
            stroke_width=1.5,
            fill="#0D47A1",
        )
    )

    p.add(
        Text(
            id="geom_label_O",
            x=430.0,
            y=550.0,
            text="O",
            font_size=48,
            semantic_role="geometry_point_label",
            fill="#1F1F1F",
            font_family="Malgun Gothic",
            anchor="start",
        )
    )

    p.add(
        Circle(
            id="geom_point_X",
            cx=488.75,
            cy=440.9215069796397,
            r=5.0,
            semantic_role="geometry_point",
            stroke="#0D47A1",
            stroke_width=1.5,
            fill="#0D47A1",
        )
    )

    p.add(
        Text(
            id="geom_label_X",
            x=498.75,
            y=430.9215069796397,
            text="X",
            font_size=48,
            semantic_role="geometry_point_label",
            fill="#1F1F1F",
            font_family="Malgun Gothic",
            anchor="start",
        )
    )

    p.add(
        Text(
            id="text.problem_ln1",
            x=40.0,
            y=80.0,
            text="Circle O has a radius of 13 inches. Radius OB is",
            font_size=48,
            semantic_role="problem_text",
            fill="#000000",
            font_family="sans-serif",
            anchor="start",
        )
    )
    p.add(
        Text(
            id="text.problem_ln2",
            x=40.0,
            y=144.8,
            text="perpendicular to chord CD, which is 24 inches long.",
            font_size=48,
            semantic_role="problem_text",
            fill="#000000",
            font_family="sans-serif",
            anchor="start",
        )
    )
    p.add(
        Text(
            id="text.problem_ln3",
            x=40.0,
            y=209.60000000000002,
            text="Find OX.",
            font_size=48,
            semantic_role="problem_text",
            fill="#000000",
            font_family="sans-serif",
            anchor="start",
        )
    )

    p.add(
        Text(
            id="text.choice_1",
            x=860.0,
            y=320.0,
            text="no.1 5",
            font_size=48,
            semantic_role="multiple_choice",
            fill="#000000",
            font_family="sans-serif",
            anchor="start",
        )
    )

    p.add(
        Text(
            id="text.choice_2",
            x=860.0,
            y=390.0,
            text="no.2 12",
            font_size=48,
            semantic_role="multiple_choice",
            fill="#000000",
            font_family="sans-serif",
            anchor="start",
        )
    )

    p.add(
        Text(
            id="text.choice_3",
            x=860.0,
            y=460.0,
            text="no.3 13",
            font_size=48,
            semantic_role="multiple_choice",
            fill="#000000",
            font_family="sans-serif",
            anchor="start",
        )
    )

    p.add(
        Text(
            id="text.choice_4",
            x=860.0,
            y=530.0,
            text="no.4 26",
            font_size=48,
            semantic_role="multiple_choice",
            fill="#000000",
            font_family="sans-serif",
            anchor="start",
        )
    )

    return p


CURRENT_DIR = Path(__file__).resolve().parent

if __name__ == "__main__":
    out_prefix = CURRENT_DIR / PROBLEM_ID
    build().save(out_prefix)
