from __future__ import annotations

from pathlib import Path

from modu_semantic import Circle, Line, Problem, Rect, Text

# source semantic: 2408.semantic.json

PROBLEM_ID = "2408"
PROBLEM_TYPE = "Length::Line,Triangle"
TITLE_TEXT = "If XN = 6, XM = 2, and XY = 10, find NZ."
CANVAS_W = 1400.0
CANVAS_H = 900.0
CANVAS_BG = "#FFFFFF"
FONT_SCALE = 1.0


def build() -> Problem:
    p = Problem(width=int(CANVAS_W), height=int(CANVAS_H), background=CANVAS_BG, problem_id=PROBLEM_ID, problem_type=PROBLEM_TYPE)
    p.title = TITLE_TEXT
    p.set_metadata({'source': 'textbook1_chapter_7.pdf',
 'warnings': [],
 'annot_id': 'Shibiao_2020-03-22_11_34_08',
 'is_standard': False,
 'data_type': 'test',
 'date': 'Fri Sep 18 22:23:14 2020',
 'system': 'linux',
 'legacy': {'id': 2408,
            'comment': '',
            'unit': '',
            'compact_text': 'If XN = 6, XM = 2, and XY = 10, find NZ.',
            'annotat_text': 'If $XN=6,XM=2$, and $XY=10$, find $NZ$.',
            'compact_choices': ['12', '16', '24', '32'],
            'precise_value': [12.0, 16.0, 24.0, 32.0],
            'rough_value': [12, 16, 24, 32]}})
    p.set_domain({'problem_type_goal': ['Length'],
 'problem_type_graph': ['Line', 'Triangle'],
 'logic_form': {'text_logic_form': ['XN선 길이 = 6', 'XM선 길이 = 2', 'XY선 길이 = 10', 'NZ선 길이 구하기'],
                'dissolved_text_logic_form': ['XN선 길이 = 6',
                                              'XM선 길이 = 2',
                                              'XY선 길이 = 10',
                                              'NZ선 길이 구하기'],
                'diagram_logic_form': ['점 N는 XZ선 위', '점 M는 XY선 위', 'ZY선 ∥ NM선'],
                'line_instances': ['XZ', 'XY', 'XN', 'XM', 'ZY', 'ZN', 'YM', 'NM'],
                'point_positions': {'X': [1.0883534136546302, 166.33333333333331],
                                    'Z': [270.87824351297405, 166.33333333333331],
                                    'Y': [210.5024928459746, 0.7964421630232721],
                                    'N': [97.62903225806451, 167.0],
                                    'M': [75.35924694144197, 106.96840479866967]},
                'circle_instances': []}})
    p.set_answer(blanks=[], choices=['12', '16', '24', '32'], answer_key=[{'label': 'no.3', 'index': 2, 'value': '24'}])

    # elements
    p.add(
        Rect(
            id="geom_diagram_region",
            x=40.0,
            y=200.0,
            width=752.0,
            height=660.0,
            semantic_role="geometry_diagram_region",
            stroke="#D1D5DB",
            stroke_width=1.0,
            fill="none",
        )
    )

    p.add(
        Line(
            id="geom_line_1",
            x1=64.0,
            y1=745.9791297980003,
            x2=767.9999999999998,
            y2=745.9791297980003,
            semantic_role="geometry_edge",
            stroke="#374151",
            stroke_width=2.2,
        )
    )

    p.add(
        Line(
            id="geom_line_2",
            x1=64.0,
            y1=745.9791297980003,
            x2=610.4532199708439,
            y2=314.0208702019998,
            semantic_role="geometry_edge",
            stroke="#374151",
            stroke_width=2.2,
        )
    )

    p.add(
        Line(
            id="geom_line_3",
            x1=610.453219970844,
            y1=314.0208702019997,
            x2=767.9999999999998,
            y2=745.9791297980003,
            semantic_role="geometry_edge",
            stroke="#374151",
            stroke_width=2.2,
        )
    )

    p.add(
        Line(
            id="geom_line_4",
            x1=258.6375011754847,
            y1=592.122819344998,
            x2=315.9169190566938,
            y2=745.9791297980003,
            semantic_role="geometry_edge",
            stroke="#374151",
            stroke_width=2.2,
        )
    )

    p.add(
        Circle(
            id="geom_point_X",
            cx=64.0,
            cy=745.9791297980003,
            r=3.8,
            semantic_role="geometry_point",
            stroke="#111111",
            stroke_width=1.0,
            fill="#111111",
        )
    )

    p.add(
        Text(
            id="geom_label_X",
            x=70.0,
            y=739.9791297980003,
            text="X",
            font_size=36,
            semantic_role="geometry_point_label",
            fill="#111111",
            font_family="Malgun Gothic",
            anchor="start",
        )
    )

    p.add(
        Circle(
            id="geom_point_Z",
            cx=767.9999999999998,
            cy=745.9791297980003,
            r=3.8,
            semantic_role="geometry_point",
            stroke="#111111",
            stroke_width=1.0,
            fill="#111111",
        )
    )

    p.add(
        Text(
            id="geom_label_Z",
            x=773.9999999999998,
            y=739.9791297980003,
            text="Z",
            font_size=36,
            semantic_role="geometry_point_label",
            fill="#111111",
            font_family="Malgun Gothic",
            anchor="start",
        )
    )

    p.add(
        Circle(
            id="geom_point_Y",
            cx=610.453219970844,
            cy=314.02087020199974,
            r=3.8,
            semantic_role="geometry_point",
            stroke="#111111",
            stroke_width=1.0,
            fill="#111111",
        )
    )

    p.add(
        Text(
            id="geom_label_Y",
            x=616.453219970844,
            y=308.02087020199974,
            text="Y",
            font_size=36,
            semantic_role="geometry_point_label",
            fill="#111111",
            font_family="Malgun Gothic",
            anchor="start",
        )
    )

    p.add(
        Circle(
            id="geom_point_N",
            cx=315.9169190566938,
            cy=745.9791297980003,
            r=3.8,
            semantic_role="geometry_point",
            stroke="#111111",
            stroke_width=1.0,
            fill="#111111",
        )
    )

    p.add(
        Text(
            id="geom_label_N",
            x=321.9169190566938,
            y=739.9791297980003,
            text="N",
            font_size=36,
            semantic_role="geometry_point_label",
            fill="#111111",
            font_family="Malgun Gothic",
            anchor="start",
        )
    )

    p.add(
        Circle(
            id="geom_point_M",
            cx=258.6375011754847,
            cy=592.122819344998,
            r=3.8,
            semantic_role="geometry_point",
            stroke="#111111",
            stroke_width=1.0,
            fill="#111111",
        )
    )

    p.add(
        Text(
            id="geom_label_M",
            x=264.6375011754847,
            y=586.122819344998,
            text="M",
            font_size=36,
            semantic_role="geometry_point_label",
            fill="#111111",
            font_family="Malgun Gothic",
            anchor="start",
        )
    )

    p.add(
        Line(
            id="geom_parallel_1_ab_base",
            x1=691.2824964246211,
            y1=535.6367837415602,
            x2=687.1707235462227,
            y2=524.3632162584398,
            semantic_role="geometry_parallel_marker",
            stroke="#2563EB",
            stroke_width=1.8,
        )
    )

    p.add(
        Line(
            id="geom_parallel_1_ab_w1",
            x1=687.1707235462227,
            y1=524.3632162584398,
            x2=693.3671690733704,
            y2=529.0220452775272,
            semantic_role="geometry_parallel_marker",
            stroke="#2563EB",
            stroke_width=1.8,
        )
    )

    p.add(
        Line(
            id="geom_parallel_1_ab_w2",
            x1=687.1707235462227,
            y1=524.3632162584398,
            x2=685.42869863734,
            y2=531.9174186793994,
            semantic_role="geometry_parallel_marker",
            stroke="#2563EB",
            stroke_width=1.8,
        )
    )

    p.add(
        Line(
            id="geom_parallel_1_cd_base",
            x1=289.3705933414726,
            y1=674.6739405745694,
            x2=285.18382689070586,
            y2=663.4280085684289,
            semantic_role="geometry_parallel_marker",
            stroke="#2563EB",
            stroke_width=1.8,
        )
    )

    p.add(
        Line(
            id="geom_parallel_1_cd_w1",
            x1=285.18382689070586,
            y1=663.4280085684289,
            x2=291.41116394536647,
            y2=668.0454643838809,
            semantic_role="geometry_parallel_marker",
            stroke="#2563EB",
            stroke_width=1.8,
        )
    )

    p.add(
        Line(
            id="geom_parallel_1_cd_w2",
            x1=285.18382689070586,
            y1=663.4280085684289,
            x2=283.49215349104253,
            y2=670.9936457596291,
            semantic_role="geometry_parallel_marker",
            stroke="#2563EB",
            stroke_width=1.8,
        )
    )

    p.add(
        Text(
            id="text.problem",
            x=40.0,
            y=80.0,
            text="If X N = 6, X M = 2, and X Y = 10, find N Z.",
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
            text="no.1 12 / no.2 16 / no.3 24",
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
            text="/ no.4 32",
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
