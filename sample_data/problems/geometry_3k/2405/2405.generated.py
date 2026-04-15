from __future__ import annotations

from pathlib import Path

from modu_semantic import Line, Problem, Text

# source semantic: 2405.semantic.json

PROBLEM_ID = "2405"
PROBLEM_TYPE = "Angle::Line"
TITLE_TEXT = "In the figure below, ∠ABC is intersected by parallel lines ℓ and m."
CANVAS_W = 1400.0
CANVAS_H = 960.0
CANVAS_BG = "#FFFFFF"
FONT_SCALE = 1.0


def build() -> Problem:
    p = Problem(width=int(CANVAS_W), height=int(CANVAS_H), background=CANVAS_BG, problem_id=PROBLEM_ID, problem_type=PROBLEM_TYPE)
    p.title = TITLE_TEXT
    p.set_metadata({'source': {'input_type': 'python_dsl', 'generator': 'modu_semantic'}, 'warnings': []})
    p.set_domain({})
    p.set_answer(blanks=[], choices=['33', '38', '61', '71'], answer_key=[{'label': 'no.4', 'index': 3, 'value': '71'}])

    # elements
    p.add(
        Line(
            id="geom_line_l",
            x1=130.0,
            y1=280.0,
            x2=1290.0,
            y2=280.0,
            semantic_role="geometry_edge",
            stroke="#222222",
            stroke_width=4.4,
        )
    )

    p.add(
        Line(
            id="geom_line_l_end_ah_l",
            x1=1290.0,
            y1=280.0,
            x2=1266.0,
            y2=287.0,
            semantic_role="geometry_arrow_head",
            stroke="#222222",
            stroke_width=4.4,
        )
    )

    p.add(
        Line(
            id="geom_line_l_end_ah_r",
            x1=1290.0,
            y1=280.0,
            x2=1266.0,
            y2=273.0,
            semantic_role="geometry_arrow_head",
            stroke="#222222",
            stroke_width=4.4,
        )
    )

    p.add(
        Line(
            id="geom_line_l_start_ah_l",
            x1=130.0,
            y1=280.0,
            x2=154.0,
            y2=273.0,
            semantic_role="geometry_arrow_head",
            stroke="#222222",
            stroke_width=4.4,
        )
    )

    p.add(
        Line(
            id="geom_line_l_start_ah_r",
            x1=130.0,
            y1=280.0,
            x2=154.0,
            y2=287.0,
            semantic_role="geometry_arrow_head",
            stroke="#222222",
            stroke_width=4.4,
        )
    )

    p.add(
        Line(
            id="geom_line_m",
            x1=130.0,
            y1=680.0,
            x2=1290.0,
            y2=680.0,
            semantic_role="geometry_edge",
            stroke="#222222",
            stroke_width=4.4,
        )
    )

    p.add(
        Line(
            id="geom_line_m_end_ah_l",
            x1=1290.0,
            y1=680.0,
            x2=1266.0,
            y2=687.0,
            semantic_role="geometry_arrow_head",
            stroke="#222222",
            stroke_width=4.4,
        )
    )

    p.add(
        Line(
            id="geom_line_m_end_ah_r",
            x1=1290.0,
            y1=680.0,
            x2=1266.0,
            y2=673.0,
            semantic_role="geometry_arrow_head",
            stroke="#222222",
            stroke_width=4.4,
        )
    )

    p.add(
        Line(
            id="geom_line_m_start_ah_l",
            x1=130.0,
            y1=680.0,
            x2=154.0,
            y2=673.0,
            semantic_role="geometry_arrow_head",
            stroke="#222222",
            stroke_width=4.4,
        )
    )

    p.add(
        Line(
            id="geom_line_m_start_ah_r",
            x1=130.0,
            y1=680.0,
            x2=154.0,
            y2=687.0,
            semantic_role="geometry_arrow_head",
            stroke="#222222",
            stroke_width=4.4,
        )
    )

    p.add(
        Line(
            id="geom_line_BA",
            x1=520.0,
            y1=510.0,
            x2=1040.0,
            y2=90.0,
            semantic_role="geometry_edge",
            stroke="#222222",
            stroke_width=4.4,
        )
    )

    p.add(
        Line(
            id="geom_line_BA_end_ah_l",
            x1=1040.0,
            y1=90.0,
            x2=1025.727771424724,
            y2=110.52567883152896,
            semantic_role="geometry_arrow_head",
            stroke="#222222",
            stroke_width=4.4,
        )
    )

    p.add(
        Line(
            id="geom_line_BA_end_ah_r",
            x1=1040.0,
            y1=90.0,
            x2=1016.9310519254973,
            y2=99.63450230867686,
            semantic_role="geometry_arrow_head",
            stroke="#222222",
            stroke_width=4.4,
        )
    )

    p.add(
        Line(
            id="geom_line_BC",
            x1=520.0,
            y1=510.0,
            x2=1160.0,
            y2=890.0,
            semantic_role="geometry_edge",
            stroke="#222222",
            stroke_width=4.4,
        )
    )

    p.add(
        Line(
            id="geom_line_BC_end_ah_l",
            x1=1160.0,
            y1=890.0,
            x2=1135.7897148687343,
            y2=883.7660531071547,
            semantic_role="geometry_arrow_head",
            stroke="#222222",
            stroke_width=4.4,
        )
    )

    p.add(
        Line(
            id="geom_line_BC_end_ah_r",
            x1=1160.0,
            y1=890.0,
            x2=1142.9372574269105,
            y2=871.7280866933843,
            semantic_role="geometry_arrow_head",
            stroke="#222222",
            stroke_width=4.4,
        )
    )

    p.add(
        Text(
            id="geom_label_A",
            x=680.0,
            y=264.0,
            text="A",
            font_size=48,
            semantic_role="geometry_point_label",
            fill="#111111",
            font_family="Malgun Gothic",
            anchor="start",
        )
    )

    p.add(
        Text(
            id="geom_label_B",
            x=528.0,
            y=520.0,
            text="B",
            font_size=48,
            semantic_role="geometry_point_label",
            fill="#111111",
            font_family="Malgun Gothic",
            anchor="start",
        )
    )

    p.add(
        Text(
            id="geom_label_C",
            x=712.0,
            y=732.0,
            text="C",
            font_size=48,
            semantic_role="geometry_point_label",
            fill="#111111",
            font_family="Malgun Gothic",
            anchor="start",
        )
    )

    p.add(
        Text(
            id="geom_label_l",
            x=52.0,
            y=292.0,
            text="ℓ",
            font_size=48,
            semantic_role="geometry_line_label",
            fill="#111111",
            font_family="Malgun Gothic",
            anchor="start",
        )
    )

    p.add(
        Text(
            id="geom_label_m",
            x=52.0,
            y=692.0,
            text="m",
            font_size=48,
            semantic_role="geometry_line_label",
            fill="#111111",
            font_family="Malgun Gothic",
            anchor="start",
        )
    )

    p.add(
        Text(
            id="geom_angle_38",
            x=590.0,
            y=338.0,
            text="38°",
            font_size=48,
            semantic_role="geometry_angle_label",
            fill="#222222",
            font_family="Malgun Gothic",
            anchor="start",
        )
    )

    p.add(
        Text(
            id="geom_angle_33",
            x=646.0,
            y=668.0,
            text="33°",
            font_size=48,
            semantic_role="geometry_angle_label",
            fill="#222222",
            font_family="Malgun Gothic",
            anchor="start",
        )
    )

    p.add(
        Text(
            id="text.problem_ln1",
            x=40.0,
            y=72.0,
            text="In the figure below, ∠ABC is intersected by parallel",
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
            y=136.8,
            text="lines ℓ and m. What is the measure of ∠ABC?",
            font_size=48,
            semantic_role="problem_text",
            fill="#000000",
            font_family="sans-serif",
            anchor="start",
        )
    )

    p.add(
        Text(
            id="text.problem_sub",
            x=40.0,
            y=126.0,
            text="Express your answer in degrees.",
            font_size=48,
            semantic_role="problem_text",
            fill="#000000",
            font_family="sans-serif",
            anchor="start",
        )
    )

    p.add(
        Text(
            id="text.choices_ln1",
            x=860.0,
            y=320.0,
            text="no.1 33 no.2 38 no.3 61 4.",
            font_size=48,
            semantic_role="multiple_choice",
            fill="#000000",
            font_family="sans-serif",
            anchor="start",
        )
    )
    p.add(
        Text(
            id="text.choices_ln2",
            x=860.0,
            y=384.8,
            text="71",
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
