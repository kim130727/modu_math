from __future__ import annotations

from pathlib import Path

from modu_semantic import Circle, Line, Problem, Text

# source semantic: 2404.semantic.json

PROBLEM_ID = "2404"
PROBLEM_TYPE = "Angle::Circle"
TITLE_TEXT = "Find m ∠CAM."
CANVAS_W = 960.0
CANVAS_H = 760.0
CANVAS_BG = "#FFFFFF"
FONT_SCALE = 1.0


def build() -> Problem:
    p = Problem(width=int(CANVAS_W), height=int(CANVAS_H), background=CANVAS_BG, problem_id=PROBLEM_ID, problem_type=PROBLEM_TYPE)
    p.title = TITLE_TEXT
    p.set_metadata({'source': {'input_type': 'python_dsl', 'generator': 'modu_semantic'}, 'warnings': []})
    p.set_domain({})
    p.set_answer(blanks=[], choices=['14', '28', '36', '90'], answer_key=[{'label': 'no.2', 'index': 1, 'value': '28'}])

    # elements
    p.add(
        Circle(
            id="geom_circle_main",
            cx=430.0,
            cy=390.0,
            r=250.0,
            semantic_role="geometry_circle",
            stroke="#0B72D9",
            stroke_width=6.0,
            fill="none",
        )
    )

    p.add(
        Line(
            id="geom_seg_CA",
            x1=189.68457601542033,
            y1=321.0906610457501,
            x2=621.5111107797445,
            y2=229.3030975783652,
            semantic_role="geometry_edge",
            stroke="#222222",
            stroke_width=5.0,
        )
    )

    p.add(
        Line(
            id="geom_seg_TA",
            x1=238.4888892202555,
            y1=550.6969024216348,
            x2=621.5111107797445,
            y2=229.3030975783652,
            semantic_role="geometry_edge",
            stroke="#222222",
            stroke_width=5.0,
        )
    )

    p.add(
        Line(
            id="geom_seg_TN",
            x1=238.4888892202555,
            y1=550.6969024216348,
            x2=670.3154239845796,
            y2=458.9093389542498,
            semantic_role="geometry_edge",
            stroke="#222222",
            stroke_width=5.0,
        )
    )

    p.add(
        Line(
            id="geom_perp_M_CA",
            x1=430.0,
            y1=390.0,
            x2=405.59784339758244,
            y2=275.19687931205766,
            semantic_role="geometry_edge",
            stroke="#222222",
            stroke_width=5.0,
        )
    )

    p.add(
        Line(
            id="geom_perp_M_TN",
            x1=430.0,
            y1=390.0,
            x2=454.4021566024176,
            y2=504.8031206879423,
            semantic_role="geometry_edge",
            stroke="#222222",
            stroke_width=5.0,
        )
    )

    p.add(
        Line(
            id="geom_ra_ca_a",
            x1=405.59784339758244,
            y1=275.19687931205766,
            x2=421.2482050093233,
            y2=271.8702922589735,
            semantic_role="geometry_right_angle",
            stroke="#E91E63",
            stroke_width=3.0,
        )
    )

    p.add(
        Line(
            id="geom_ra_ca_b",
            x1=421.2482050093233,
            y1=271.8702922589735,
            x2=424.5747920624075,
            y2=287.5206538707144,
            semantic_role="geometry_right_angle",
            stroke="#E91E63",
            stroke_width=3.0,
        )
    )

    p.add(
        Line(
            id="geom_ra_ca_c",
            x1=424.5747920624075,
            y1=287.5206538707144,
            x2=408.9244304506666,
            y2=290.84724092379855,
            semantic_role="geometry_right_angle",
            stroke="#E91E63",
            stroke_width=3.0,
        )
    )

    p.add(
        Line(
            id="geom_ra_tn_a",
            x1=454.4021566024176,
            y1=504.8031206879423,
            x2=470.0525182141585,
            y2=501.47653363485813,
            semantic_role="geometry_right_angle",
            stroke="#E91E63",
            stroke_width=3.0,
        )
    )

    p.add(
        Line(
            id="geom_ra_tn_b",
            x1=470.0525182141585,
            y1=501.47653363485813,
            x2=466.72593116107436,
            y2=485.82617202311724,
            semantic_role="geometry_right_angle",
            stroke="#E91E63",
            stroke_width=3.0,
        )
    )

    p.add(
        Line(
            id="geom_ra_tn_c",
            x1=466.72593116107436,
            y1=485.82617202311724,
            x2=451.07556954933347,
            y2=489.1527590762014,
            semantic_role="geometry_right_angle",
            stroke="#E91E63",
            stroke_width=3.0,
        )
    )

    p.add(
        Line(
            id="geom_eq_1_1",
            x1=410.7989216987912,
            y1=339.59843965602886,
            x2=424.7989216987912,
            y2=325.59843965602886,
            semantic_role="geometry_equal_mark",
            stroke="#E91E63",
            stroke_width=3.0,
        )
    )

    p.add(
        Line(
            id="geom_eq_2_1",
            x1=435.2010783012088,
            y1=454.40156034397114,
            x2=449.2010783012088,
            y2=440.40156034397114,
            semantic_role="geometry_equal_mark",
            stroke="#E91E63",
            stroke_width=3.0,
        )
    )

    p.add(
        Text(
            id="geom_label_C",
            x=159.68457601542033,
            y=335.0906610457501,
            text="C",
            font_size=48,
            semantic_role="geometry_point_label",
            fill="#000000",
            font_family="sans-serif",
            anchor="start",
        )
    )

    p.add(
        Text(
            id="geom_label_A",
            x=631.5111107797445,
            y=237.3030975783652,
            text="A",
            font_size=48,
            semantic_role="geometry_point_label",
            fill="#000000",
            font_family="sans-serif",
            anchor="start",
        )
    )

    p.add(
        Text(
            id="geom_label_N",
            x=678.3154239845796,
            y=470.9093389542498,
            text="N",
            font_size=48,
            semantic_role="geometry_point_label",
            fill="#000000",
            font_family="sans-serif",
            anchor="start",
        )
    )

    p.add(
        Text(
            id="geom_label_T",
            x=224.4888892202555,
            y=586.6969024216348,
            text="T",
            font_size=48,
            semantic_role="geometry_point_label",
            fill="#000000",
            font_family="sans-serif",
            anchor="start",
        )
    )

    p.add(
        Text(
            id="geom_label_M",
            x=410.0,
            y=378.0,
            text="M",
            font_size=48,
            semantic_role="geometry_point_label",
            fill="#000000",
            font_family="sans-serif",
            anchor="start",
        )
    )

    p.add(
        Text(
            id="geom_label_deg",
            x=312.4888892202555,
            y=602.6969024216348,
            text="28°",
            font_size=48,
            semantic_role="geometry_angle_label",
            fill="#000000",
            font_family="sans-serif",
            anchor="start",
        )
    )

    p.add(
        Text(
            id="text.problem",
            x=40.0,
            y=72.0,
            text="Find m ∠CAM.",
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
            text="1.",
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
            text="14",
            font_size=48,
            semantic_role="multiple_choice",
            fill="#000000",
            font_family="sans-serif",
            anchor="start",
        )
    )
    p.add(
        Text(
            id="text.choices_ln3",
            x=860.0,
            y=449.6,
            text="2.",
            font_size=48,
            semantic_role="multiple_choice",
            fill="#000000",
            font_family="sans-serif",
            anchor="start",
        )
    )
    p.add(
        Text(
            id="text.choices_ln4",
            x=860.0,
            y=514.4000000000001,
            text="28",
            font_size=48,
            semantic_role="multiple_choice",
            fill="#000000",
            font_family="sans-serif",
            anchor="start",
        )
    )
    p.add(
        Text(
            id="text.choices_ln5",
            x=860.0,
            y=579.2,
            text="3.",
            font_size=48,
            semantic_role="multiple_choice",
            fill="#000000",
            font_family="sans-serif",
            anchor="start",
        )
    )
    p.add(
        Text(
            id="text.choices_ln6",
            x=860.0,
            y=644.0,
            text="36",
            font_size=48,
            semantic_role="multiple_choice",
            fill="#000000",
            font_family="sans-serif",
            anchor="start",
        )
    )
    p.add(
        Text(
            id="text.choices_ln7",
            x=860.0,
            y=708.8000000000001,
            text="4.",
            font_size=48,
            semantic_role="multiple_choice",
            fill="#000000",
            font_family="sans-serif",
            anchor="start",
        )
    )
    p.add(
        Text(
            id="text.choices_ln8",
            x=860.0,
            y=773.6000000000001,
            text="90",
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
