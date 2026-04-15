from __future__ import annotations

from pathlib import Path

from modu_semantic import Circle, Line, Problem, Text

# source semantic: 2406.semantic.json

PROBLEM_ID = "2406"
PROBLEM_TYPE = "Angle::Other"
TITLE_TEXT = "Find the value of x in the diagram."
CANVAS_W = 1400.0
CANVAS_H = 900.0
CANVAS_BG = "#FFFFFF"
FONT_SCALE = 1.0


def build() -> Problem:
    p = Problem(width=int(CANVAS_W), height=int(CANVAS_H), background=CANVAS_BG, problem_id=PROBLEM_ID, problem_type=PROBLEM_TYPE)
    p.title = TITLE_TEXT
    p.set_metadata({'source': {'input_type': 'python_dsl', 'generator': 'modu_semantic'}, 'warnings': []})
    p.set_domain({})
    p.set_answer(blanks=[], choices=['68', '78', '79', '136'], answer_key=[{'label': 'no.1', 'index': 0, 'value': '68'}])

    # elements
    p.add(
        Line(
            id="geom_base_line",
            x1=170.0,
            y1=610.0,
            x2=1120.0,
            y2=610.0,
            semantic_role="geometry_edge",
            stroke="#0B72B9",
            stroke_width=5.2,
        )
    )

    p.add(
        Line(
            id="geom_base_line_start_ah_l",
            x1=170.0,
            y1=610.0,
            x2=194.0,
            y2=603.0,
            semantic_role="geometry_arrow_head",
            stroke="#0B72B9",
            stroke_width=5.2,
        )
    )

    p.add(
        Line(
            id="geom_base_line_start_ah_r",
            x1=170.0,
            y1=610.0,
            x2=194.0,
            y2=617.0,
            semantic_role="geometry_arrow_head",
            stroke="#0B72B9",
            stroke_width=5.2,
        )
    )

    p.add(
        Line(
            id="geom_left_up_ray",
            x1=360.0,
            y1=420.0,
            x2=250.0,
            y2=180.0,
            semantic_role="geometry_edge",
            stroke="#0B72B9",
            stroke_width=5.2,
        )
    )

    p.add(
        Line(
            id="geom_left_up_ray_end_ah_l",
            x1=250.0,
            y1=180.0,
            x2=266.3631668120971,
            y2=198.90097277601032,
            semantic_role="geometry_arrow_head",
            stroke="#0B72B9",
            stroke_width=5.2,
        )
    )

    p.add(
        Line(
            id="geom_left_up_ray_end_ah_r",
            x1=250.0,
            y1=180.0,
            x2=253.63625929157715,
            y2=204.73413872291533,
            semantic_role="geometry_arrow_head",
            stroke="#0B72B9",
            stroke_width=5.2,
        )
    )

    p.add(
        Line(
            id="geom_left_down_seg",
            x1=360.0,
            y1=420.0,
            x2=430.0,
            y2=610.0,
            semantic_role="geometry_edge",
            stroke="#0B72B9",
            stroke_width=5.2,
        )
    )

    p.add(
        Line(
            id="geom_upper_ray",
            x1=359.9343,
            y1=420.09879,
            x2=783.35156,
            y2=222.02281,
            semantic_role="geometry_edge",
            stroke="#0B72B9",
            stroke_width=5.2,
        )
    )

    p.add(
        Line(
            id="geom_upper_ray_end_ah_l",
            x1=783.35156,
            y1=222.02281,
            x2=764.5787575800495,
            y2=238.53286418832724,
            semantic_role="geometry_arrow_head",
            stroke="#0B72B9",
            stroke_width=5.2,
        )
    )

    p.add(
        Line(
            id="geom_upper_ray_end_ah_r",
            x1=783.35156,
            y1=222.02281,
            x2=758.646527867853,
            y2=225.85182911063217,
            semantic_role="geometry_arrow_head",
            stroke="#0B72B9",
            stroke_width=5.2,
        )
    )

    p.add(
        Line(
            id="geom_diag_ray",
            x1=619.95795,
            y1=299.95432,
            x2=1086.2775,
            y2=768.19574,
            semantic_role="geometry_edge",
            stroke="#0B72B9",
            stroke_width=5.2,
        )
    )

    p.add(
        Line(
            id="geom_diag_ray_end_ah_l",
            x1=1086.2775,
            y1=768.19574,
            x2=1064.3819561846499,
            y2=756.1298723962973,
            semantic_role="geometry_arrow_head",
            stroke="#0B72B9",
            stroke_width=5.2,
        )
    )

    p.add(
        Line(
            id="geom_diag_ray_end_ah_r",
            x1=1086.2775,
            y1=768.19574,
            x2=1074.3017878786472,
            y2=746.2507560814256,
            semantic_role="geometry_arrow_head",
            stroke="#0B72B9",
            stroke_width=5.2,
        )
    )

    p.add(
        Line(
            id="geom_upper_to_c",
            x1=360.0,
            y1=420.0,
            x2=620.0,
            y2=300.0,
            semantic_role="geometry_edge",
            stroke="#0B72B9",
            stroke_width=5.2,
        )
    )

    p.add(
        Circle(
            id="geom_point_B",
            cx=430.0,
            cy=610.0,
            r=4.6,
            semantic_role="geometry_point",
            stroke="#0B3A5E",
            stroke_width=1.4,
            fill="#0B3A5E",
        )
    )

    p.add(
        Circle(
            id="geom_point_C",
            cx=620.0,
            cy=300.0,
            r=4.6,
            semantic_role="geometry_point",
            stroke="#0B3A5E",
            stroke_width=1.4,
            fill="#0B3A5E",
        )
    )

    p.add(
        Circle(
            id="geom_point_D",
            cx=360.0,
            cy=420.0,
            r=4.6,
            semantic_role="geometry_point",
            stroke="#0B3A5E",
            stroke_width=1.4,
            fill="#0B3A5E",
        )
    )

    p.add(
        Circle(
            id="geom_point_E",
            cx=250.0,
            cy=180.0,
            r=4.6,
            semantic_role="geometry_point",
            stroke="#0B3A5E",
            stroke_width=1.4,
            fill="#0B3A5E",
        )
    )

    p.add(
        Circle(
            id="geom_point_I",
            cx=930.0,
            cy=610.0,
            r=4.6,
            semantic_role="geometry_point",
            stroke="#0B3A5E",
            stroke_width=1.4,
            fill="#0B3A5E",
        )
    )

    p.add(
        Text(
            id="geom_angle_79",
            x=359.37903,
            y=363.07892,
            text="79°",
            font_size=48,
            semantic_role="geometry_angle_label",
            fill="#1F1F1F",
            font_family="Malgun Gothic",
            anchor="start",
        )
    )

    p.add(
        Text(
            id="geom_angle_xm1",
            x=263.89392,
            y=574.92883,
            text="(x−1)°",
            font_size=48,
            semantic_role="geometry_angle_label",
            fill="#1F1F1F",
            font_family="Malgun Gothic",
            anchor="start",
        )
    )

    p.add(
        Text(
            id="geom_angle_xp10",
            x=700.0,
            y=320.0,
            text="(x+10)°",
            font_size=48,
            semantic_role="geometry_angle_label",
            fill="#1F1F1F",
            font_family="Malgun Gothic",
            anchor="start",
        )
    )

    p.add(
        Text(
            id="geom_angle_2x",
            x=870.89264,
            y=666.44244,
            text="2x°",
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
            y=70.0,
            text="Find the value of x in the diagram.",
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
            text="no.1 68 / no.2 78 / no.3 79",
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
            text="/ no.4 136",
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
