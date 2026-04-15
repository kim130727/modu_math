from __future__ import annotations

from pathlib import Path

from modu_semantic import Circle, Line, Problem, Rect, Text

# source semantic: 2409.semantic.json

PROBLEM_ID = "2409"
PROBLEM_TYPE = "Length::Triangle"
TITLE_TEXT = "Find y."
CANVAS_W = 1400.0
CANVAS_H = 939.0
CANVAS_BG = "#FFFFFF"
FONT_SCALE = 1.0


def build() -> Problem:
    p = Problem(width=int(CANVAS_W), height=int(CANVAS_H), background=CANVAS_BG, problem_id=PROBLEM_ID, problem_type=PROBLEM_TYPE)
    p.title = TITLE_TEXT
    p.set_metadata({'source': 'textbook1_chapter_8.pdf',
 'warnings': [],
 'annot_id': 'pan_2020-03-24_00_30_23',
 'is_standard': False,
 'data_type': 'test',
 'date': 'Fri Sep 18 22:23:14 2020',
 'system': 'linux',
 'legacy': {'id': 2409,
            'comment': '',
            'unit': '',
            'compact_text': 'Find y.',
            'annotat_text': 'Find y.',
            'compact_choices': ['21', '21\\sqrt{2}', '21\\sqrt{3}', '42'],
            'precise_value': [21.0, 29.698484809834998, 36.373066958946424, 42.0],
            'rough_value': [21, 29.7, 36.37, 42]}})
    p.set_domain({'problem_type_goal': ['Length'],
 'problem_type_graph': ['Triangle'],
 'logic_form': {'text_logic_form': ['y 구하기'],
                'dissolved_text_logic_form': ['y 구하기'],
                'diagram_logic_form': ['AC선 길이 = 21',
                                       'MeasureOf(Angle(A = C, B), 60)',
                                       'AB선 길이 = y',
                                       'MeasureOf(Angle(C = B, A), 30)',
                                       'BC선 길이 = x',
                                       'AB선 ⟂ AC선'],
                'line_instances': ['AB', 'AC', 'BC'],
                'point_positions': {'A': [75.06045424181697, 218.54342017368072],
                                    'B': [0.0, 0.0],
                                    'C': [205.28453217210728, 176.57761461280103]},
                'circle_instances': []}})
    p.set_answer(blanks=[], choices=['21', '21 √(2)', '21 √(3)', '42'], answer_key=[{'label': 'no.3', 'index': 2, 'value': '21 √(3)'}])

    # elements
    p.add(
        Rect(
            id="geom_diagram_region",
            x=40.0,
            y=200.0,
            width=752.0,
            height=699.0,
            semantic_role="geometry_diagram_region",
            stroke="#D1D5DB",
            stroke_width=1.0,
            fill="none",
        )
    )

    p.add(
        Line(
            id="geom_line_1",
            x1=110.2478745463136,
            y1=224.0,
            x2=333.8389379267137,
            y2=875.0,
            semantic_role="geometry_edge",
            stroke="#374151",
            stroke_width=2.2,
        )
    )

    p.add(
        Line(
            id="geom_line_2",
            x1=333.8389379267137,
            y1=875.0,
            x2=721.7521254536864,
            y2=749.9917092062477,
            semantic_role="geometry_edge",
            stroke="#374151",
            stroke_width=2.2,
        )
    )

    p.add(
        Line(
            id="geom_line_3",
            x1=110.2478745463136,
            y1=224.0,
            x2=721.7521254536864,
            y2=749.9917092062477,
            semantic_role="geometry_edge",
            stroke="#374151",
            stroke_width=2.2,
        )
    )

    p.add(
        Circle(
            id="geom_point_A",
            cx=333.8389379267137,
            cy=875.0,
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
            x=339.8389379267137,
            y=869.0,
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
            cx=110.2478745463136,
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
            x=116.2478745463136,
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
            cx=721.7521254536864,
            cy=749.9917092062477,
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
            x=727.7521254536864,
            y=743.9917092062477,
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
            id="geom_len_1_AC",
            x=531.7955316902,
            y=808.4958546031239,
            text="21",
            font_size=36,
            semantic_role="geometry_length_label",
            fill="#1F2937",
            font_family="Malgun Gothic",
            anchor="start",
        )
    )

    p.add(
        Text(
            id="geom_len_2_AB",
            x=226.04340623651365,
            y=545.5,
            text="y",
            font_size=36,
            semantic_role="geometry_length_label",
            fill="#1F2937",
            font_family="Malgun Gothic",
            anchor="start",
        )
    )

    p.add(
        Text(
            id="geom_len_3_BC",
            x=420.0,
            y=482.99585460312386,
            text="x",
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
            x1=331.38513809210417,
            y1=867.3856145112248,
            x2=336.2927377613232,
            y2=882.6143854887752,
            semantic_role="geometry_dimension_cap",
            stroke="#111111",
            stroke_width=1.5,
        )
    )

    p.add(
        Line(
            id="geom_dim_1_cap_b",
            x1=719.2983256190769,
            y1=742.3773237174726,
            x2=724.2059252882959,
            y2=757.6060946950229,
            semantic_role="geometry_dimension_cap",
            stroke="#111111",
            stroke_width=1.5,
        )
    )

    p.add(
        Line(
            id="geom_dim_1_arr_a_a",
            x1=338.5979288571982,
            y1=873.466375103369,
            x2=331.9037183064016,
            y2=878.7755694962693,
            semantic_role="geometry_dimension_arrow",
            stroke="#111111",
            stroke_width=1.8,
        )
    )

    p.add(
        Line(
            id="geom_dim_1_arr_a_b",
            x1=338.5979288571982,
            y1=873.466375103369,
            x2=330.0633684304444,
            y2=873.0647803796878,
            semantic_role="geometry_dimension_arrow",
            stroke="#111111",
            stroke_width=1.8,
        )
    )

    p.add(
        Line(
            id="geom_dim_1_arr_b_a",
            x1=716.9931345232019,
            y1=751.5253341028787,
            x2=723.6873450739985,
            y2=746.2161397099784,
            semantic_role="geometry_dimension_arrow",
            stroke="#111111",
            stroke_width=1.8,
        )
    )

    p.add(
        Line(
            id="geom_dim_1_arr_b_b",
            x1=716.9931345232019,
            y1=751.5253341028787,
            x2=725.5276949499556,
            y2=751.9269288265599,
            semantic_role="geometry_dimension_arrow",
            stroke="#111111",
            stroke_width=1.8,
        )
    )

    p.add(
        Line(
            id="geom_dim_2_cap_a",
            x1=326.27276585471265,
            y1=877.5986612278,
            x2=341.40510999871475,
            y2=872.4013387722,
            semantic_role="geometry_dimension_cap",
            stroke="#111111",
            stroke_width=1.5,
        )
    )

    p.add(
        Line(
            id="geom_dim_2_cap_b",
            x1=102.68170247431253,
            y1=226.5986612278,
            x2=117.81404661831466,
            y2=221.4013387722,
            semantic_role="geometry_dimension_cap",
            stroke="#111111",
            stroke_width=1.5,
        )
    )

    p.add(
        Line(
            id="geom_dim_2_arr_a_a",
            x1=332.2147746593387,
            y1=870.2711424549993,
            x2=337.65075041413905,
            y2=876.8628165665755,
            semantic_role="geometry_dimension_arrow",
            stroke="#111111",
            stroke_width=1.8,
        )
    )

    p.add(
        Line(
            id="geom_dim_2_arr_a_b",
            x1=332.2147746593387,
            y1=870.2711424549993,
            x2=331.9761213601383,
            y2=878.8118124874254,
            semantic_role="geometry_dimension_arrow",
            stroke="#111111",
            stroke_width=1.8,
        )
    )

    p.add(
        Line(
            id="geom_dim_2_arr_b_a",
            x1=111.8720378136886,
            y1=228.72885754500066,
            x2=106.4360620588882,
            y2=222.13718343342458,
            semantic_role="geometry_dimension_arrow",
            stroke="#111111",
            stroke_width=1.8,
        )
    )

    p.add(
        Line(
            id="geom_dim_2_arr_b_b",
            x1=111.8720378136886,
            y1=228.72885754500066,
            x2=112.110691112889,
            y2=220.1881875125746,
            semantic_role="geometry_dimension_arrow",
            stroke="#111111",
            stroke_width=1.8,
        )
    )

    p.add(
        Line(
            id="geom_dim_3_cap_a",
            x1=115.46474771718863,
            y1=217.9349992317392,
            x2=105.03100137543856,
            y2=230.0650007682608,
            semantic_role="geometry_dimension_cap",
            stroke="#111111",
            stroke_width=1.5,
        )
    )

    p.add(
        Line(
            id="geom_dim_3_cap_b",
            x1=726.9689986245614,
            y1=743.9267084379869,
            x2=716.5352522828114,
            y2=756.0567099745085,
            semantic_role="geometry_dimension_cap",
            stroke="#111111",
            stroke_width=1.5,
        )
    )

    p.add(
        Line(
            id="geom_dim_3_arr_a_a",
            x1=114.0385000264766,
            y1=227.2605457317969,
            x2=106.01717181913764,
            y2=224.31804784901968,
            semantic_role="geometry_dimension_arrow",
            stroke="#111111",
            stroke_width=1.8,
        )
    )

    p.add(
        Line(
            id="geom_dim_3_arr_a_b",
            x1=114.0385000264766,
            y1=227.2605457317969,
            x2=109.92982669729392,
            y2=219.76929727282405,
            semantic_role="geometry_dimension_arrow",
            stroke="#111111",
            stroke_width=1.8,
        )
    )

    p.add(
        Line(
            id="geom_dim_3_arr_b_a",
            x1=717.9614999735234,
            y1=746.7311634744508,
            x2=725.9828281808623,
            y2=749.6736613572281,
            semantic_role="geometry_dimension_arrow",
            stroke="#111111",
            stroke_width=1.8,
        )
    )

    p.add(
        Line(
            id="geom_dim_3_arr_b_b",
            x1=717.9614999735234,
            y1=746.7311634744508,
            x2=722.070173302706,
            y2=754.2224119334236,
            semantic_role="geometry_dimension_arrow",
            stroke="#111111",
            stroke_width=1.8,
        )
    )

    p.add(
        Line(
            id="geom_angle_1_01",
            x1=704.6197581039422,
            y1=753.672408958162,
            x2=704.2626737901023,
            y2=752.8294767566025,
            semantic_role="geometry_angle_marker",
            stroke="#7C3AED",
            stroke_width=2.0,
        )
    )

    p.add(
        Line(
            id="geom_angle_1_02",
            x1=704.2626737901023,
            y1=752.8294767566025,
            x2=703.9987700507371,
            y2=751.9714254526461,
            semantic_role="geometry_angle_marker",
            stroke="#7C3AED",
            stroke_width=2.0,
        )
    )

    p.add(
        Line(
            id="geom_angle_1_03",
            x1=703.9987700507371,
            y1=751.9714254526461,
            x2=703.8294529163222,
            y2=751.1028265854679,
            semantic_role="geometry_angle_marker",
            stroke="#7C3AED",
            stroke_width=2.0,
        )
    )

    p.add(
        Line(
            id="geom_angle_1_04",
            x1=703.8294529163222,
            y1=751.1028265854679,
            x2=703.7556244773381,
            y2=750.2283078897156,
            semantic_role="geometry_angle_marker",
            stroke="#7C3AED",
            stroke_width=2.0,
        )
    )

    p.add(
        Line(
            id="geom_angle_1_05",
            x1=703.7556244773381,
            y1=750.2283078897156,
            x2=703.777678078098,
            y2=749.352528639792,
            semantic_role="geometry_angle_marker",
            stroke="#7C3AED",
            stroke_width=2.0,
        )
    )

    p.add(
        Line(
            id="geom_angle_1_06",
            x1=703.777678078098,
            y1=749.352528639792,
            x2=703.8954962210826,
            y2=748.4801548261006,
            semantic_role="geometry_angle_marker",
            stroke="#7C3AED",
            stroke_width=2.0,
        )
    )

    p.add(
        Line(
            id="geom_angle_1_07",
            x1=703.8954962210826,
            y1=748.4801548261006,
            x2=704.1084511929445,
            y2=747.6158342955082,
            semantic_role="geometry_angle_marker",
            stroke="#7C3AED",
            stroke_width=2.0,
        )
    )

    p.add(
        Line(
            id="geom_angle_1_08",
            x1=704.1084511929445,
            y1=747.6158342955082,
            x2=704.4154084088495,
            y2=746.7641719884737,
            semantic_role="geometry_angle_marker",
            stroke="#7C3AED",
            stroke_width=2.0,
        )
    )

    p.add(
        Line(
            id="geom_angle_1_09",
            x1=704.4154084088495,
            y1=746.7641719884737,
            x2=704.8147324573356,
            y2=745.9297054047743,
            semantic_role="geometry_angle_marker",
            stroke="#7C3AED",
            stroke_width=2.0,
        )
    )

    p.add(
        Line(
            id="geom_angle_1_10",
            x1=704.8147324573356,
            y1=745.9297054047743,
            x2=705.3042958134832,
            y2=745.1168804285433,
            semantic_role="geometry_angle_marker",
            stroke="#7C3AED",
            stroke_width=2.0,
        )
    )

    p.add(
        Line(
            id="geom_angle_1_11",
            x1=705.3042958134832,
            y1=745.1168804285433,
            x2=705.8814901739768,
            y2=744.3300276414185,
            semantic_role="geometry_angle_marker",
            stroke="#7C3AED",
            stroke_width=2.0,
        )
    )

    p.add(
        Line(
            id="geom_angle_1_12",
            x1=705.8814901739768,
            y1=744.3300276414185,
            x2=706.5432403536627,
            y2=743.5733392500023,
            semantic_role="geometry_angle_marker",
            stroke="#7C3AED",
            stroke_width=2.0,
        )
    )

    p.add(
        Line(
            id="geom_angle_1_13",
            x1=706.5432403536627,
            y1=743.5733392500023,
            x2=707.2860206695702,
            y2=742.8508467505567,
            semantic_role="geometry_angle_marker",
            stroke="#7C3AED",
            stroke_width=2.0,
        )
    )

    p.add(
        Line(
            id="geom_angle_1_14",
            x1=707.2860206695702,
            y1=742.8508467505567,
            x2=708.1058737250996,
            y2=742.1663994499352,
            semantic_role="geometry_angle_marker",
            stroke="#7C3AED",
            stroke_width=2.0,
        )
    )

    p.add(
        Text(
            id="geom_angle_label_1",
            x=692.3460016857832,
            y=745.6359385365586,
            text="60",
            font_size=36,
            semantic_role="geometry_angle_label",
            fill="#111111",
            font_family="Malgun Gothic",
            anchor="start",
        )
    )

    p.add(
        Line(
            id="geom_angle_2_01",
            x1=123.89412627490043,
            y1=231.82530975631255,
            x2=123.44044042590701,
            y2=232.16377378728973,
            semantic_role="geometry_angle_marker",
            stroke="#7C3AED",
            stroke_width=2.0,
        )
    )

    p.add(
        Line(
            id="geom_angle_2_02",
            x1=123.44044042590701,
            y1=232.16377378728973,
            x2=122.96787837167527,
            y2=232.4905569162396,
            semantic_role="geometry_angle_marker",
            stroke="#7C3AED",
            stroke_width=2.0,
        )
    )

    p.add(
        Line(
            id="geom_angle_2_03",
            x1=122.96787837167527,
            y1=232.4905569162396,
            x2=122.47711626409291,
            y2=232.80519157487663,
            semantic_role="geometry_angle_marker",
            stroke="#7C3AED",
            stroke_width=2.0,
        )
    )

    p.add(
        Line(
            id="geom_angle_2_04",
            x1=122.47711626409291,
            y1=232.80519157487663,
            x2=121.96885629607303,
            y2=233.1072275772062,
            semantic_role="geometry_angle_marker",
            stroke="#7C3AED",
            stroke_width=2.0,
        )
    )

    p.add(
        Line(
            id="geom_angle_2_05",
            x1=121.96885629607303,
            y1=233.1072275772062,
            x2=121.4438256968414,
            y2=233.3962327636605,
            semantic_role="geometry_angle_marker",
            stroke="#7C3AED",
            stroke_width=2.0,
        )
    )

    p.add(
        Line(
            id="geom_angle_2_06",
            x1=121.4438256968414,
            y1=233.3962327636605,
            x2=120.90277569140142,
            y2=233.6717936194415,
            semantic_role="geometry_angle_marker",
            stroke="#7C3AED",
            stroke_width=2.0,
        )
    )

    p.add(
        Line(
            id="geom_angle_2_07",
            x1=120.90277569140142,
            y1=233.6717936194415,
            x2=120.34648042566526,
            y2=233.93351586618698,
            semantic_role="geometry_angle_marker",
            stroke="#7C3AED",
            stroke_width=2.0,
        )
    )

    p.add(
        Line(
            id="geom_angle_2_08",
            x1=120.34648042566526,
            y1=233.93351586618698,
            x2=119.77573585878939,
            y2=234.18102502611222,
            semantic_role="geometry_angle_marker",
            stroke="#7C3AED",
            stroke_width=2.0,
        )
    )

    p.add(
        Line(
            id="geom_angle_2_09",
            x1=119.77573585878939,
            y1=234.18102502611222,
            x2=119.19135862429917,
            y2=234.41396695782092,
            semantic_role="geometry_angle_marker",
            stroke="#7C3AED",
            stroke_width=2.0,
        )
    )

    p.add(
        Line(
            id="geom_angle_2_10",
            x1=119.19135862429917,
            y1=234.41396695782092,
            x2=118.59418486163221,
            y2=234.63200836301831,
            semantic_role="geometry_angle_marker",
            stroke="#7C3AED",
            stroke_width=2.0,
        )
    )

    p.add(
        Line(
            id="geom_angle_2_11",
            x1=118.59418486163221,
            y1=234.63200836301831,
            x2=117.98506901977213,
            y2=234.83483726340143,
            semantic_role="geometry_angle_marker",
            stroke="#7C3AED",
            stroke_width=2.0,
        )
    )

    p.add(
        Line(
            id="geom_angle_2_12",
            x1=117.98506901977213,
            y1=234.83483726340143,
            x2=117.36488263468466,
            y2=235.02216344704433,
            semantic_role="geometry_angle_marker",
            stroke="#7C3AED",
            stroke_width=2.0,
        )
    )

    p.add(
        Line(
            id="geom_angle_2_13",
            x1=117.36488263468466,
            y1=235.02216344704433,
            x2=116.73451308230547,
            y2=235.19371888363958,
            semantic_role="geometry_angle_marker",
            stroke="#7C3AED",
            stroke_width=2.0,
        )
    )

    p.add(
        Line(
            id="geom_angle_2_14",
            x1=116.73451308230547,
            y1=235.19371888363958,
            x2=116.09486230886361,
            y2=235.3492581080016,
            semantic_role="geometry_angle_marker",
            stroke="#7C3AED",
            stroke_width=2.0,
        )
    )

    p.add(
        Text(
            id="geom_angle_label_2",
            x=127.07888434523304,
            y=242.21144575467613,
            text="30",
            font_size=36,
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
            text="Find y.",
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
            text="no.1 21 / no.2 21 √(2) /",
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
            text="no.3 21 √(3) / 4.",
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
