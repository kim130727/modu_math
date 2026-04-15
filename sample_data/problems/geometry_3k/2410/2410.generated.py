from __future__ import annotations

from pathlib import Path

from modu_semantic import Circle, Line, Problem, Rect, Text

# source semantic: 2410.semantic.json

PROBLEM_ID = "2410"
PROBLEM_TYPE = "Length::Triangle"
TITLE_TEXT = "Find CD if AC = x-3, BE = 20, AB = 16, and CD = x+5."
CANVAS_W = 1400.0
CANVAS_H = 900.0
CANVAS_BG = "#FFFFFF"
FONT_SCALE = 1.0


def build() -> Problem:
    p = Problem(width=int(CANVAS_W), height=int(CANVAS_H), background=CANVAS_BG, problem_id=PROBLEM_ID, problem_type=PROBLEM_TYPE)
    p.title = TITLE_TEXT
    p.set_metadata({'source': {'input_type': 'python_dsl', 'generator': 'modu_semantic'}, 'warnings': []})
    p.set_domain({'logic_form': {'text_logic_form': ['AC선 길이 = x-3',
                                    'BE선 길이 = 20',
                                    'AB선 길이 = 16',
                                    'CD선 길이 = x+5',
                                    'CD선 길이 구하기'],
                'dissolved_text_logic_form': ['AC선 길이 = x-3',
                                              'BE선 길이 = 20',
                                              'AB선 길이 = 16',
                                              'CD선 길이 = x+5',
                                              'CD선 길이 구하기'],
                'diagram_logic_form': ['점 B는 EA선 위', '점 C는 AD선 위', 'BC선 ∥ ED선'],
                'line_instances': ['EA', 'ED', 'EB', 'AD', 'AC', 'AB', 'DC', 'BC'],
                'circle_instances': [],
                'point_positions': {'E': [180.6676116548543, 166.15686803914951],
                                    'A': [1.2257546348972568, 82.92903197019388],
                                    'D': [180.3382457072048, 1.482120729332621],
                                    'C': [88.96836628511966, 42.85411030176899],
                                    'B': [86.02023591620906, 122.45363026235509]}}})
    p.set_answer(blanks=[], choices=['32', '35', '36', '40'], answer_key=[{'label': 'no.4', 'index': 3, 'value': '40'}])

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
            x1=82.55963257802125,
            y1=526.6906705108124,
            x2=749.4403674219787,
            y2=836.0,
            semantic_role="geometry_edge",
            stroke="#374151",
            stroke_width=2.2,
        )
    )

    p.add(
        Line(
            id="geom_line_2",
            x1=748.2163062756619,
            y1=224.0,
            x2=749.4403674219787,
            y2=836.0,
            semantic_role="geometry_edge",
            stroke="#374151",
            stroke_width=2.2,
        )
    )

    p.add(
        Line(
            id="geom_line_3",
            x1=82.5596325780212,
            y1=526.6906705108124,
            x2=748.2163062756617,
            y2=224.0,
            semantic_role="geometry_edge",
            stroke="#374151",
            stroke_width=2.2,
        )
    )

    p.add(
        Line(
            id="geom_line_4",
            x1=397.96879724589485,
            y1=672.982191829077,
            x2=408.894456269918,
            y2=378.2980974361288,
            semantic_role="geometry_edge",
            stroke="#374151",
            stroke_width=2.2,
        )
    )

    p.add(
        Circle(
            id="geom_point_E",
            cx=749.4403674219787,
            cy=836.0,
            r=3.8,
            semantic_role="geometry_point",
            stroke="#111111",
            stroke_width=1.0,
            fill="#111111",
        )
    )

    p.add(
        Text(
            id="geom_label_E",
            x=755.4403674219787,
            y=830.0,
            text="E",
            font_size=36,
            semantic_role="geometry_point_label",
            fill="#111111",
            font_family="Malgun Gothic",
            anchor="start",
        )
    )

    p.add(
        Circle(
            id="geom_point_A",
            cx=82.5596325780212,
            cy=526.6906705108124,
            r=3.8,
            semantic_role="geometry_point",
            stroke="#111111",
            stroke_width=1.0,
            fill="#111111",
        )
    )

    p.add(
        Text(
            id="geom_label_A",
            x=88.5596325780212,
            y=520.6906705108124,
            text="A",
            font_size=36,
            semantic_role="geometry_point_label",
            fill="#111111",
            font_family="Malgun Gothic",
            anchor="start",
        )
    )

    p.add(
        Circle(
            id="geom_point_D",
            cx=748.2163062756619,
            cy=224.0,
            r=3.8,
            semantic_role="geometry_point",
            stroke="#111111",
            stroke_width=1.0,
            fill="#111111",
        )
    )

    p.add(
        Text(
            id="geom_label_D",
            x=754.2163062756619,
            y=218.0,
            text="D",
            font_size=36,
            semantic_role="geometry_point_label",
            fill="#111111",
            font_family="Malgun Gothic",
            anchor="start",
        )
    )

    p.add(
        Circle(
            id="geom_point_C",
            cx=408.894456269918,
            cy=378.2980974361288,
            r=3.8,
            semantic_role="geometry_point",
            stroke="#111111",
            stroke_width=1.0,
            fill="#111111",
        )
    )

    p.add(
        Text(
            id="geom_label_C",
            x=414.894456269918,
            y=372.2980974361288,
            text="C",
            font_size=36,
            semantic_role="geometry_point_label",
            fill="#111111",
            font_family="Malgun Gothic",
            anchor="start",
        )
    )

    p.add(
        Circle(
            id="geom_point_B",
            cx=397.96879724589485,
            cy=672.982191829077,
            r=3.8,
            semantic_role="geometry_point",
            stroke="#111111",
            stroke_width=1.0,
            fill="#111111",
        )
    )

    p.add(
        Text(
            id="geom_label_B",
            x=403.96879724589485,
            y=666.982191829077,
            text="B",
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
            x1=403.20932448242104,
            y1=531.6360250265328,
            x2=403.6539290333918,
            y2=519.6442642386729,
            semantic_role="geometry_parallel_marker",
            stroke="#2563EB",
            stroke_width=1.8,
        )
    )

    p.add(
        Line(
            id="geom_parallel_1_ab_w1",
            x1=403.6539290333918,
            y1=519.6442642386729,
            x2=407.63520067900834,
            y2=526.296339184418,
            semantic_role="geometry_parallel_marker",
            stroke="#2563EB",
            stroke_width=1.8,
        )
    )

    p.add(
        Line(
            id="geom_parallel_1_ab_w2",
            x1=403.6539290333918,
            y1=519.6442642386729,
            x2=399.1910024575569,
            y2=525.983263479776,
            semantic_role="geometry_parallel_marker",
            stroke="#2563EB",
            stroke_width=1.8,
        )
    )

    p.add(
        Line(
            id="geom_parallel_1_cd_base",
            x1=748.8403374242905,
            y1=535.999987998837,
            x2=748.8163362733501,
            y2=524.000012001163,
            semantic_role="geometry_parallel_marker",
            stroke="#2563EB",
            stroke_width=1.8,
        )
    )

    p.add(
        Line(
            id="geom_parallel_1_cd_w1",
            x1=748.8163362733501,
            y1=524.000012001163,
            x2=753.0543284459571,
            y2=530.4915485946763,
            semantic_role="geometry_parallel_marker",
            stroke="#2563EB",
            stroke_width=1.8,
        )
    )

    p.add(
        Line(
            id="geom_parallel_1_cd_w2",
            x1=748.8163362733501,
            y1=524.000012001163,
            x2=744.6043453475951,
            y2=530.50844940513,
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
            text="Find CD if AC = x-3, BE = 20, AB = 16, and CD = x+5.",
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
            text="no.1 32 / no.2 35 / no.3 36",
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
            text="/ no.4 40",
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
