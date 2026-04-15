from __future__ import annotations

from pathlib import Path

from modu_semantic import Circle, Line, Problem, Rect, Text

# source semantic: 2407.semantic.json

PROBLEM_ID = "2407"
PROBLEM_TYPE = "Angle::Other"
TITLE_TEXT = "Find the value of x."
CANVAS_W = 1466.0
CANVAS_H = 1363.0
CANVAS_BG = "#FFFFFF"
FONT_SCALE = 1.0


def build() -> Problem:
    p = Problem(width=int(CANVAS_W), height=int(CANVAS_H), background=CANVAS_BG, problem_id=PROBLEM_ID, problem_type=PROBLEM_TYPE)
    p.title = TITLE_TEXT
    p.set_metadata({'source': {'input_type': 'python_dsl', 'generator': 'modu_semantic'}, 'warnings': []})
    p.set_domain({})
    p.set_answer(blanks=[], choices=['56', '68', '74', '84'], answer_key=[{'label': 'no.3', 'index': 2, 'value': '74'}])

    # elements
    p.add(
        Rect(
            id="geom_diagram_region",
            x=40.0,
            y=200.0,
            width=790.28,
            height=1123.0,
            semantic_role="geometry_diagram_region",
            stroke="#D1D5DB",
            stroke_width=1.0,
            fill="none",
        )
    )

    p.add(
        Line(
            id="geom_line_1_AC",
            x1=220.98349869451698,
            y1=688.8224543080939,
            x2=385.7192689295039,
            y2=1101.6309138381203,
            semantic_role="geometry_edge",
            stroke="#0B72B9",
            stroke_width=4.0,
        )
    )

    p.add(
        Line(
            id="geom_line_1_AC_end_ah_l",
            x1=385.7192689295039,
            y1=1101.6309138381203,
            x2=370.3224991315421,
            y2=1081.9347345185524,
            semantic_role="geometry_arrow_head",
            stroke="#0B72B9",
            stroke_width=4.0,
        )
    )

    p.add(
        Line(
            id="geom_line_1_AC_end_ah_r",
            x1=385.7192689295039,
            y1=1101.6309138381203,
            x2=383.3253786380621,
            y2=1076.7457919924764,
            semantic_role="geometry_arrow_head",
            stroke="#0B72B9",
            stroke_width=4.0,
        )
    )

    p.add(
        Line(
            id="geom_line_2_HE",
            x1=319.82496083550916,
            y1=936.8951436031332,
            x2=806.28,
            y2=938.8332114882506,
            semantic_role="geometry_edge",
            stroke="#0B72B9",
            stroke_width=4.0,
        )
    )

    p.add(
        Line(
            id="geom_line_2_HE_end_ah_l",
            x1=806.28,
            y1=938.8332114882506,
            x2=782.2523022460151,
            y2=945.737539163206,
            semantic_role="geometry_arrow_head",
            stroke="#0B72B9",
            stroke_width=4.0,
        )
    )

    p.add(
        Line(
            id="geom_line_2_HE_end_ah_r",
            x1=806.28,
            y1=938.8332114882506,
            x2=782.308078695784,
            y2=931.7376502712308,
            semantic_role="geometry_arrow_head",
            stroke="#0B72B9",
            stroke_width=4.0,
        )
    )

    p.add(
        Line(
            id="geom_line_3_BI",
            x1=476.80845953002614,
            y1=537.6531592689295,
            x2=64.0,
            y2=785.7258485639686,
            semantic_role="geometry_edge",
            stroke="#0B72B9",
            stroke_width=4.0,
        )
    )

    p.add(
        Line(
            id="geom_line_3_BI_end_ah_l",
            x1=64.0,
            y1=785.7258485639686,
            x2=80.96569174216185,
            y2=767.3637870318329,
            semantic_role="geometry_arrow_head",
            stroke="#0B72B9",
            stroke_width=4.0,
        )
    )

    p.add(
        Line(
            id="geom_line_3_BI_end_ah_r",
            x1=64.0,
            y1=785.7258485639686,
            x2=88.17691555666707,
            y2=779.3637141606579,
            semantic_role="geometry_arrow_head",
            stroke="#0B72B9",
            stroke_width=4.0,
        )
    )

    p.add(
        Line(
            id="geom_line_4_DF",
            x1=709.3766057441253,
            y1=696.574725848564,
            x2=304.32041775456923,
            y2=421.36908616187986,
            semantic_role="geometry_edge",
            stroke="#0B72B9",
            stroke_width=4.0,
        )
    )

    p.add(
        Line(
            id="geom_line_4_DF_end_ah_l",
            x1=304.32041775456923,
            y1=421.36908616187986,
            x2=328.1058488072661,
            y2=429.0667007038924,
            semantic_role="geometry_arrow_head",
            stroke="#0B72B9",
            stroke_width=4.0,
        )
    )

    p.add(
        Line(
            id="geom_line_4_DF_end_ah_r",
            x1=304.32041775456923,
            y1=421.36908616187986,
            x2=320.23805564041726,
            y2=440.6467624776347,
            semantic_role="geometry_arrow_head",
            stroke="#0B72B9",
            stroke_width=4.0,
        )
    )

    p.add(
        Line(
            id="geom_line_5_GJ",
            x1=612.4732114882506,
            y1=940.7712793733681,
            x2=773.3328459530027,
            y2=529.9008877284595,
            semantic_role="geometry_edge",
            stroke="#0B72B9",
            stroke_width=4.0,
        )
    )

    p.add(
        Line(
            id="geom_line_5_GJ_end_ah_l",
            x1=773.3328459530027,
            y1=529.9008877284595,
            x2=771.1015327284993,
            y2=554.8011134562346,
            semantic_role="geometry_arrow_head",
            stroke="#0B72B9",
            stroke_width=4.0,
        )
    )

    p.add(
        Line(
            id="geom_line_5_GJ_end_ah_r",
            x1=773.3328459530027,
            y1=529.9008877284595,
            x2=758.0650412908494,
            y2=549.6972040726264,
            semantic_role="geometry_arrow_head",
            stroke="#0B72B9",
            stroke_width=4.0,
        )
    )

    p.add(
        Line(
            id="geom_line_6_AH",
            x1=385.7192689295039,
            y1=1101.6309138381203,
            x2=319.82496083550916,
            y2=936.8951436031332,
            semantic_role="geometry_edge",
            stroke="#0B72B9",
            stroke_width=4.0,
        )
    )

    p.add(
        Line(
            id="geom_line_7_BD",
            x1=476.80845953002614,
            y1=537.6531592689295,
            x2=709.3766057441253,
            y2=696.574725848564,
            semantic_role="geometry_edge",
            stroke="#0B72B9",
            stroke_width=4.0,
        )
    )

    p.add(
        Line(
            id="geom_line_8_BF",
            x1=476.80845953002614,
            y1=537.6531592689295,
            x2=304.32041775456923,
            y2=421.36908616187986,
            semantic_role="geometry_edge",
            stroke="#0B72B9",
            stroke_width=4.0,
        )
    )

    p.add(
        Line(
            id="geom_line_9_CB",
            x1=220.98349869451698,
            y1=688.8224543080939,
            x2=476.80845953002614,
            y2=537.6531592689295,
            semantic_role="geometry_edge",
            stroke="#0B72B9",
            stroke_width=4.0,
        )
    )

    p.add(
        Line(
            id="geom_line_10_CH",
            x1=220.98349869451698,
            y1=688.8224543080939,
            x2=319.82496083550916,
            y2=936.8951436031332,
            semantic_role="geometry_edge",
            stroke="#0B72B9",
            stroke_width=4.0,
        )
    )

    p.add(
        Line(
            id="geom_line_11_CI",
            x1=220.98349869451698,
            y1=688.8224543080939,
            x2=64.0,
            y2=785.7258485639686,
            semantic_role="geometry_edge",
            stroke="#0B72B9",
            stroke_width=4.0,
        )
    )

    p.add(
        Line(
            id="geom_line_12_DG",
            x1=709.3766057441253,
            y1=696.574725848564,
            x2=612.4732114882506,
            y2=940.7712793733681,
            semantic_role="geometry_edge",
            stroke="#0B72B9",
            stroke_width=4.0,
        )
    )

    p.add(
        Line(
            id="geom_line_13_DJ",
            x1=709.3766057441253,
            y1=696.574725848564,
            x2=773.3328459530027,
            y2=529.9008877284595,
            semantic_role="geometry_edge",
            stroke="#0B72B9",
            stroke_width=4.0,
        )
    )

    p.add(
        Line(
            id="geom_line_14_GE",
            x1=612.4732114882506,
            y1=940.7712793733681,
            x2=806.28,
            y2=938.8332114882506,
            semantic_role="geometry_edge",
            stroke="#0B72B9",
            stroke_width=4.0,
        )
    )

    p.add(
        Line(
            id="geom_line_15_HG",
            x1=319.82496083550916,
            y1=936.8951436031332,
            x2=612.4732114882506,
            y2=940.7712793733681,
            semantic_role="geometry_edge",
            stroke="#0B72B9",
            stroke_width=4.0,
        )
    )

    p.add(
        Circle(
            id="geom_point_A",
            cx=385.7192689295039,
            cy=1101.6309138381203,
            r=4.2,
            semantic_role="geometry_point",
            stroke="#111111",
            stroke_width=1.2,
            fill="#111111",
        )
    )

    p.add(
        Circle(
            id="geom_point_B",
            cx=476.80845953002614,
            cy=537.6531592689295,
            r=4.2,
            semantic_role="geometry_point",
            stroke="#111111",
            stroke_width=1.2,
            fill="#111111",
        )
    )

    p.add(
        Circle(
            id="geom_point_C",
            cx=220.98349869451698,
            cy=688.8224543080939,
            r=4.2,
            semantic_role="geometry_point",
            stroke="#111111",
            stroke_width=1.2,
            fill="#111111",
        )
    )

    p.add(
        Circle(
            id="geom_point_D",
            cx=709.3766057441253,
            cy=696.574725848564,
            r=4.2,
            semantic_role="geometry_point",
            stroke="#111111",
            stroke_width=1.2,
            fill="#111111",
        )
    )

    p.add(
        Circle(
            id="geom_point_E",
            cx=806.28,
            cy=938.8332114882506,
            r=4.2,
            semantic_role="geometry_point",
            stroke="#111111",
            stroke_width=1.2,
            fill="#111111",
        )
    )

    p.add(
        Circle(
            id="geom_point_F",
            cx=304.32041775456923,
            cy=421.36908616187986,
            r=4.2,
            semantic_role="geometry_point",
            stroke="#111111",
            stroke_width=1.2,
            fill="#111111",
        )
    )

    p.add(
        Circle(
            id="geom_point_G",
            cx=612.4732114882506,
            cy=940.7712793733681,
            r=4.2,
            semantic_role="geometry_point",
            stroke="#111111",
            stroke_width=1.2,
            fill="#111111",
        )
    )

    p.add(
        Circle(
            id="geom_point_H",
            cx=319.82496083550916,
            cy=936.8951436031332,
            r=4.2,
            semantic_role="geometry_point",
            stroke="#111111",
            stroke_width=1.2,
            fill="#111111",
        )
    )

    p.add(
        Circle(
            id="geom_point_I",
            cx=64.0,
            cy=785.7258485639686,
            r=4.2,
            semantic_role="geometry_point",
            stroke="#111111",
            stroke_width=1.2,
            fill="#111111",
        )
    )

    p.add(
        Circle(
            id="geom_point_J",
            cx=773.3328459530027,
            cy=529.9008877284595,
            r=4.2,
            semantic_role="geometry_point",
            stroke="#111111",
            stroke_width=1.2,
            fill="#111111",
        )
    )

    p.add(
        Text(
            id="geom_angle_x",
            x=155.0,
            y=760.0,
            text="X°",
            font_size=48,
            semantic_role="geometry_angle_label",
            fill="#111111",
            font_family="Malgun Gothic",
            anchor="start",
        )
    )

    p.add(
        Text(
            id="geom_angle_xm6",
            x=250.0,
            y=975.0,
            text="(X-6)°",
            font_size=48,
            semantic_role="geometry_angle_label",
            fill="#111111",
            font_family="Malgun Gothic",
            anchor="start",
        )
    )

    p.add(
        Text(
            id="geom_angle_xp10",
            x=655.0,
            y=1000.0,
            text="(X+10)°",
            font_size=48,
            semantic_role="geometry_angle_label",
            fill="#111111",
            font_family="Malgun Gothic",
            anchor="start",
        )
    )

    p.add(
        Text(
            id="geom_angle_56",
            x=760.0,
            y=620.0,
            text="56°",
            font_size=48,
            semantic_role="geometry_angle_label",
            fill="#111111",
            font_family="Malgun Gothic",
            anchor="start",
        )
    )

    p.add(
        Text(
            id="geom_angle_xp4",
            x=340.0,
            y=505.0,
            text="(X+4)°",
            font_size=48,
            semantic_role="geometry_angle_label",
            fill="#111111",
            font_family="Malgun Gothic",
            anchor="start",
        )
    )

    p.add(
        Text(
            id="text.problem",
            x=40.0,
            y=80.0,
            text="Find the value of x.",
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
            text="no.1 56 / no.2 68 / no.3 74 /",
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
            text="no.4 84",
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
