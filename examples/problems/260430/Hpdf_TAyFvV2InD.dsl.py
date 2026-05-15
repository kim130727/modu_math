from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot, RectSlot, LineSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="Hpdf_TAyFvV2InD",
        title="정사각형 두 개로 만든 직사각형",
        canvas=Canvas(width=564, height=336, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.q1",
                    "slot.q2",
                    "slot.q3",
                    "slot.q4",
                    "slot.q5",
                    "slot.rect",
                    "slot.midline",
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="정사각형 2개를 겹치지 않게 이어 붙여서 다음",
                style_role="question",
                x=12.0,
                y=28.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q2",
                prompt="",
                text="과 같은 직사각형을 만들었습니다. 굵은 선의",
                style_role="question",
                x=12.0,
                y=64.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q3",
                prompt="",
                text="길이가 30 cm일 때, 정사각형의 한 변은 몇",
                style_role="question",
                x=12.0,
                y=100.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q4",
                prompt="",
                text="cm입니까?",
                style_role="question",
                x=12.0,
                y=136.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.rect",
                prompt="",
                x=175.0,
                y=222.0,
                width=221.0,
                height=108.0,
                stroke="#222222",
                stroke_width=3.0,
                fill="none",
            ),
            LineSlot(
                id="slot.midline",
                prompt="",
                x1=285.5,
                y1=222.0,
                x2=285.5,
                y2=330.0,
                stroke="#222222",
                stroke_width=1.5,
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()
SEMANTIC_OVERRIDE = {
    "problem_id": "Hpdf_TAyFvV2InD",
    "problem_type": "geometry_perimeter",
    "metadata": {
        "language": "ko",
        "question": "정사각형 2개를 겹치지 않게 이어 붙여서 만든 직사각형에서 굵은 선의 길이가 30 cm일 때 정사각형의 한 변을 구하는 문제",
        "instruction": "정사각형의 한 변의 길이를 구하시오.",
    },
    "domain": {
        "objects": [
            {"id": "obj.square_left", "type": "square", "count": 1},
            {"id": "obj.square_right", "type": "square", "count": 1},
            {
                "id": "obj.rectangle",
                "type": "rectangle",
                "composition": ["obj.square_left", "obj.square_right"],
            },
            {
                "id": "obj.given_length",
                "type": "length",
                "role": "displayed_thick_edge",
                "value": 30,
                "unit": "cm",
            },
        ],
        "relations": [
            {
                "id": "rel.compose_rectangle_from_two_squares",
                "type": "composition",
                "from_id": "obj.square_left",
                "to_id": "obj.rectangle",
            },
            {
                "id": "rel.shared_side_inside",
                "type": "shared_edge",
                "from_id": "obj.square_left",
                "to_id": "obj.square_right",
            },
            {
                "id": "rel.thick_edge_length_equals_three_sides",
                "type": "perimeter_relation",
                "from_id": "obj.rectangle",
                "to_id": "obj.given_length",
            },
        ],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "obj.given_length",
                    "obj.square_left",
                    "obj.square_right",
                ],
                "target_ref": "answer.target",
                "condition_refs": ["rel.thick_edge_length_equals_three_sides"],
            },
            "plan": {
                "method": "perimeter_of_two_squares_as_rectangle",
                "description": "두 정사각형을 붙여 만든 직사각형에서 굵은 선은 바깥 둘레의 일부이므로, 한 변을 x로 두고 전체 길이와의 관계를 이용한다.",
            },
            "execute": {
                "expected_operations": [
                    "set_variable_for_square_side",
                    "relate_thick_edge_to_multiple_sides",
                    "solve_for_side_length",
                ]
            },
            "review": {
                "check_methods": [
                    "substitute_back_into_length_relation",
                    "unit_consistency_check",
                ]
            },
        },
    },
    "answer": {
        "target": {
            "type": "square_side_length",
            "description": "정사각형의 한 변의 길이",
        },
        "value": 5,
        "unit": "cm",
    },
}
SOLVABLE = {   'schema': 'modu.solvable.v1',
    'problem_id': 'Hpdf_TAyFvV2InD',
    'problem_type': 'geometry_perimeter',
    'given': [{'ref': 'obj.given_length', 'value': {'length': 30, 'unit': 'cm'}}],
    'target': {'ref': 'answer.target', 'type': 'square_side_length'},
    'method': 'perimeter_of_two_squares_as_rectangle',
    'steps': [   {   'id': 'step.s1',
                     'operation': 'model_thick_edge_as_six_sides_of_square',
                     'expr': '6x = 30',
                     'value': 30},
                 {   'id': 'step.s2',
                     'operation': 'solve_for_side_length',
                     'expr': 'x = 30 ÷ 6',
                     'value': 5}],
    'checks': [   {   'id': 'check.c1',
                      'type': 'unit_consistency_check',
                      'pass': True,
                      'expected': 1,
                      'actual': 1,
                      'expr': 'check'},
                   {   'id': 'check.c2',
                       'type': 'substitution_check',
                       'expr': '6 × 5 = 30',
                       'pass': True,
                       'expected': 1,
                       'actual': 1}],
    'answer': {'value': 5, 'unit': 'cm', 'derived_from': 'step.s2'},
    'inputs': {   'total_ticks': 1,
                  'target_label': '답',
                  'target_ticks': 1,
                  'target_count': 1,
                  'unit': ''},
    'plan': ['풀이 과정 없음']}
