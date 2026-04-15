from __future__ import annotations

from pathlib import Path

from modu_semantic import Line, Problem, Rect, Text

# source semantic: 2403.semantic.json

PROBLEM_ID = "2403"
PROBLEM_TYPE = "Length::Triangle"
TITLE_TEXT = "Find x. Round to the nearest tenth."
CANVAS_W = 1400.0
CANVAS_H = 900.0
CANVAS_BG = "#FFFFFF"
FONT_SCALE = 1.0


def build() -> Problem:
    p = Problem(width=int(CANVAS_W), height=int(CANVAS_H), background=CANVAS_BG, problem_id=PROBLEM_ID, problem_type=PROBLEM_TYPE)
    p.title = TITLE_TEXT
    p.set_metadata({'source': 'textbook1_chapter_8.pdf', 'warnings': []})
    p.set_domain({})
    p.set_answer(blanks=[], choices=['18.8', '23.2', '25.9', '44.0'], answer_key=[{'label': 'no.1', 'index': 0, 'value': '18.8'}])

    # elements
    p.add(
        Rect(
            id="geom_diagram_region",
            x=40.0,
            y=200.0,
            width=760.0,
            height=620.0,
            semantic_role="geometry_diagram_region",
            stroke="#D1D5DB",
            stroke_width=1.0,
            fill="none",
        )
    )

    p.add(
        Line(
            id="geom_line_AB",
            x1=410.62892619128183,
            y1=250.0,
            x2=140.0,
            y2=700.0,
            semantic_role="geometry_edge",
            stroke="#1976D2",
            stroke_width=4.0,
        )
    )

    p.add(
        Line(
            id="geom_line_AC",
            x1=410.62892619128183,
            y1=250.0,
            x2=680.0,
            y2=700.0,
            semantic_role="geometry_edge",
            stroke="#1976D2",
            stroke_width=4.0,
        )
    )

    p.add(
        Line(
            id="geom_line_BC",
            x1=140.0,
            y1=700.0,
            x2=680.0,
            y2=700.0,
            semantic_role="geometry_edge",
            stroke="#1976D2",
            stroke_width=4.0,
        )
    )

    p.add(
        Line(
            id="geom_line_AD",
            x1=410.62892619128183,
            y1=250.0,
            x2=406.0371029673547,
            y2=700.0,
            semantic_role="geometry_edge",
            stroke="#1976D2",
            stroke_width=4.0,
        )
    )

    p.add(
        Line(
            id="geom_perp_D_1",
            x1=406.3840226614193,
            y1=666.0017699471595,
            x2=440.3840226614193,
            y2=666.0017699471595,
            semantic_role="geometry_right_angle",
            stroke="#111111",
            stroke_width=2.4,
        )
    )

    p.add(
        Line(
            id="geom_perp_D_2",
            x1=440.0371029673547,
            y1=700.0,
            x2=440.3840226614193,
            y2=666.0017699471595,
            semantic_role="geometry_right_angle",
            stroke="#111111",
            stroke_width=2.4,
        )
    )

    p.add(
        Line(
            id="geom_tick_1",
            x1=269.36029641591455,
            y1=508.18451379241895,
            x2=248.79315863241342,
            y2=495.81548620758105,
            semantic_role="geometry_tick",
            stroke="#E91E63",
            stroke_width=3.0,
        )
    )

    p.add(
        Line(
            id="geom_tick_2",
            x1=571.7729858067509,
            y1=495.83663522268375,
            x2=551.1804692415773,
            y2=508.16336477731625,
            semantic_role="geometry_tick",
            stroke="#E91E63",
            stroke_width=3.0,
        )
    )

    p.add(
        Text(
            id="geom_len_left",
            x=227.31446309564092,
            y=465.0,
            text="32",
            font_size=48,
            semantic_role="geometry_length_label",
            fill="#1F1F1F",
            font_family="Malgun Gothic",
            anchor="start",
        )
    )

    p.add(
        Text(
            id="geom_len_x",
            x=255.01855148367736,
            y=758.0,
            text="x",
            font_size=48,
            semantic_role="geometry_length_label",
            fill="#1F1F1F",
            font_family="Malgun Gothic",
            anchor="start",
        )
    )

    p.add(
        Text(
            id="geom_len_y",
            x=422.3330145793183,
            y=483.0,
            text="y",
            font_size=48,
            semantic_role="geometry_length_label",
            fill="#1F1F1F",
            font_family="Malgun Gothic",
            anchor="start",
        )
    )

    p.add(
        Text(
            id="geom_angle_54",
            x=594.0,
            y=682.0,
            text="54°",
            font_size=48,
            semantic_role="geometry_angle_label",
            fill="#1F1F1F",
            font_family="Malgun Gothic",
            anchor="start",
        )
    )

    p.add(
        Text(
            id="text.problem",
            x=40.0,
            y=90.0,
            text="Find x. Round to the nearest tenth.",
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
            text="no.1 18.8",
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
            text="no.2 23.2",
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
            text="no.3 25.9",
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
            text="no.4 44.0",
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
