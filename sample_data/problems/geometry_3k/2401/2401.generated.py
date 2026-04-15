from __future__ import annotations

from pathlib import Path

from modu_semantic import Circle, Line, Problem, Rect, Text

# source semantic: 2401.semantic.json

PROBLEM_ID = "2401"
PROBLEM_TYPE = "Area::Triangle"
TITLE_TEXT = "Find the area of the figure."
CANVAS_W = 1400.0
CANVAS_H = 980.0
CANVAS_BG = "#FFFFFF"
FONT_SCALE = 1.0


def build() -> Problem:
    p = Problem(width=int(CANVAS_W), height=int(CANVAS_H), background=CANVAS_BG, problem_id=PROBLEM_ID, problem_type=PROBLEM_TYPE)
    p.title = TITLE_TEXT
    p.set_metadata({'source': 'textbook1_chapter_8.pdf', 'warnings': []})
    p.set_domain({'problem_type_goal': ['Area'],
 'problem_type_graph': ['Triangle'],
 'logic_form': {'diagram_logic_form': ['AB선 길이 = 13', 'BC선 길이 = 13', 'AC선 길이 = 10', 'BD선은 AC에 수직'],
                'line_instances': ['AB', 'AC', 'BC', 'BD'],
                'point_positions': {'A': [0.0, 188.0], 'B': [93.0, 1.0], 'C': [185.0, 185.0]},
                'circle_instances': []}})
    p.set_answer(blanks=[], choices=['30', '60', '120', '240'], answer_key=[{'label': 'no.2', 'index': 1, 'value': '60'}])

    # elements
    p.add(
        Rect(
            id="geom_diagram_region",
            x=40.0,
            y=200.0,
            width=752.0,
            height=740.0,
            semantic_role="geometry_diagram_region",
            stroke="#D1D5DB",
            stroke_width=1.0,
            fill="none",
        )
    )

    p.add(
        Line(
            id="geom_line_1",
            x1=73.70053475935828,
            y1=910.4491978609626,
            x2=417.8502673796791,
            y2=224.0000000000001,
            semantic_role="geometry_edge",
            stroke="#374151",
            stroke_width=2.2,
        )
    )

    p.add(
        Line(
            id="geom_line_2",
            x1=73.70053475935828,
            y1=910.4491978609626,
            x2=758.2994652406417,
            y2=910.4491978609626,
            semantic_role="geometry_edge",
            stroke="#374151",
            stroke_width=2.2,
        )
    )

    p.add(
        Line(
            id="geom_line_3",
            x1=417.85026737967917,
            y1=224.0,
            x2=758.2994652406417,
            y2=910.4491978609627,
            semantic_role="geometry_edge",
            stroke="#374151",
            stroke_width=2.2,
        )
    )

    p.add(
        Circle(
            id="geom_point_A",
            cx=73.70053475935828,
            cy=910.4491978609626,
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
            x=79.70053475935828,
            y=904.4491978609626,
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
            id="geom_point_B",
            cx=417.85026737967917,
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
            id="geom_label_B",
            x=423.85026737967917,
            y=218.0,
            text="B",
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
            cx=758.2994652406417,
            cy=910.4491978609626,
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
            x=764.2994652406417,
            y=904.4491978609626,
            text="C",
            font_size=36,
            semantic_role="geometry_point_label",
            fill="#111111",
            font_family="Malgun Gothic",
            anchor="start",
        )
    )

    p.add(
        Text(
            id="geom_len_1_AB",
            x=249.77540106951872,
            y=563.2245989304813,
            text="13",
            font_size=36,
            semantic_role="geometry_length_label",
            fill="#1F2937",
            font_family="Malgun Gothic",
            anchor="start",
        )
    )

    p.add(
        Text(
            id="geom_len_2_BC",
            x=592.0748663101604,
            y=563.2245989304813,
            text="13",
            font_size=36,
            semantic_role="geometry_length_label",
            fill="#1F2937",
            font_family="Malgun Gothic",
            anchor="start",
        )
    )

    p.add(
        Text(
            id="geom_len_3_AC",
            x=420.0,
            y=906.4491978609626,
            text="10",
            font_size=36,
            semantic_role="geometry_length_label",
            fill="#1F2937",
            font_family="Malgun Gothic",
            anchor="start",
        )
    )

    p.add(
        Line(
            id="geom_dim_1_cap_a",
            x1=66.54897667314026,
            y1=906.8637805994085,
            x2=80.8520928455763,
            y2=914.0346151225167,
            semantic_role="geometry_dimension_cap",
            stroke="#111111",
            stroke_width=1.5,
        )
    )

    p.add(
        Line(
            id="geom_dim_1_cap_b",
            x1=410.69870929346115,
            y1=220.41458273844594,
            x2=425.0018254658972,
            y2=227.58541726155406,
            semantic_role="geometry_dimension_cap",
            stroke="#111111",
            stroke_width=1.5,
        )
    )

    p.add(
        Line(
            id="geom_dim_1_arr_a_a",
            x1=75.94142054782955,
            y1=905.9794740570763,
            x2=75.03783756860726,
            y2=914.475563616377,
            semantic_role="geometry_dimension_arrow",
            stroke="#111111",
            stroke_width=1.8,
        )
    )

    p.add(
        Line(
            id="geom_dim_1_arr_a_b",
            x1=75.94142054782955,
            y1=905.9794740570763,
            x2=69.67416900394376,
            y2=911.7865006702116,
            semantic_role="geometry_dimension_arrow",
            stroke="#111111",
            stroke_width=1.8,
        )
    )

    p.add(
        Line(
            id="geom_dim_1_arr_b_a",
            x1=415.60938159120786,
            y1=228.46972380388627,
            x2=416.51296457043014,
            y2=219.9736342445855,
            semantic_role="geometry_dimension_arrow",
            stroke="#111111",
            stroke_width=1.8,
        )
    )

    p.add(
        Line(
            id="geom_dim_1_arr_b_b",
            x1=415.60938159120786,
            y1=228.46972380388627,
            x2=421.87663313509364,
            y2=222.662697190751,
            semantic_role="geometry_dimension_arrow",
            stroke="#111111",
            stroke_width=1.8,
        )
    )

    p.add(
        Line(
            id="geom_dim_2_cap_a",
            x1=425.01723814492664,
            y1=220.44549158812526,
            x2=410.6832966144317,
            y2=227.55450841187474,
            semantic_role="geometry_dimension_cap",
            stroke="#111111",
            stroke_width=1.5,
        )
    )

    p.add(
        Line(
            id="geom_dim_2_cap_b",
            x1=765.4664360058891,
            y1=906.8946894490879,
            x2=751.1324944753942,
            y2=914.0037062728373,
            semantic_role="geometry_dimension_cap",
            stroke="#111111",
            stroke_width=1.5,
        )
    )

    p.add(
        Line(
            id="geom_dim_2_arr_a_a",
            x1=420.0718351371009,
            y1=228.47935672827967,
            x2=413.8297126882584,
            y2=222.64532661748527,
            semantic_role="geometry_dimension_arrow",
            stroke="#111111",
            stroke_width=1.8,
        )
    )

    p.add(
        Line(
            id="geom_dim_2_arr_a_b",
            x1=420.0718351371009,
            y1=228.47935672827967,
            x2=419.2049407621939,
            y2=219.9794453085792,
            semantic_role="geometry_dimension_arrow",
            stroke="#111111",
            stroke_width=1.8,
        )
    )

    p.add(
        Line(
            id="geom_dim_2_arr_b_a",
            x1=756.07789748322,
            y1=905.969841132683,
            x2=762.3200199320626,
            y2=911.8038712434774,
            semantic_role="geometry_dimension_arrow",
            stroke="#111111",
            stroke_width=1.8,
        )
    )

    p.add(
        Line(
            id="geom_dim_2_arr_b_b",
            x1=756.07789748322,
            y1=905.969841132683,
            x2=756.9447918581269,
            y2=914.4697525523835,
            semantic_role="geometry_dimension_arrow",
            stroke="#111111",
            stroke_width=1.8,
        )
    )

    p.add(
        Line(
            id="geom_dim_3_cap_a",
            x1=73.70053475935828,
            y1=902.4491978609626,
            x2=73.70053475935828,
            y2=918.4491978609626,
            semantic_role="geometry_dimension_cap",
            stroke="#111111",
            stroke_width=1.5,
        )
    )

    p.add(
        Line(
            id="geom_dim_3_cap_b",
            x1=758.2994652406417,
            y1=902.4491978609626,
            x2=758.2994652406417,
            y2=918.4491978609626,
            semantic_role="geometry_dimension_cap",
            stroke="#111111",
            stroke_width=1.5,
        )
    )

    p.add(
        Line(
            id="geom_dim_3_arr_a_a",
            x1=78.70053475935828,
            y1=910.4491978609626,
            x2=70.70053475935828,
            y2=913.4491978609626,
            semantic_role="geometry_dimension_arrow",
            stroke="#111111",
            stroke_width=1.8,
        )
    )

    p.add(
        Line(
            id="geom_dim_3_arr_a_b",
            x1=78.70053475935828,
            y1=910.4491978609626,
            x2=70.70053475935828,
            y2=907.4491978609626,
            semantic_role="geometry_dimension_arrow",
            stroke="#111111",
            stroke_width=1.8,
        )
    )

    p.add(
        Line(
            id="geom_dim_3_arr_b_a",
            x1=753.2994652406417,
            y1=910.4491978609626,
            x2=761.2994652406417,
            y2=907.4491978609626,
            semantic_role="geometry_dimension_arrow",
            stroke="#111111",
            stroke_width=1.8,
        )
    )

    p.add(
        Line(
            id="geom_dim_3_arr_b_b",
            x1=753.2994652406417,
            y1=910.4491978609626,
            x2=761.2994652406417,
            y2=913.4491978609626,
            semantic_role="geometry_dimension_arrow",
            stroke="#111111",
            stroke_width=1.8,
        )
    )

    p.add(
        Text(
            id="text.problem",
            x=40.0,
            y=80.0,
            text="Find the area of the figure.",
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
            text="no.1 30",
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
            y=380.0,
            text="no.2 60",
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
            text="no.3 120",
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
            y=540.0,
            text="no.4 240",
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
