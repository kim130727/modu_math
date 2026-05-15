from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot, RectSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="Hpdf_IfXEqd2FAo",
        title="세 자리 수 만들기",
        canvas=Canvas(width=750, height=380, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.q1",
                    "slot.box",
                    "slot.b1",
                    "slot.b2",
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="1부터 9까지의 숫자를 모두 한 번씩만 사용하여\n 3개의 세 자리 수 529, ㉠, ㉡를 만들려고 합니다.\n세 수가 다음을 모두 만족시킬 때, 가장 작은 수 ㉠를 구하시오.",
                style_role="question",
                x=12.0,
                y=34.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.box",
                prompt="",
                x=12.0,
                y=148.0,
                width=524.0,
                height=162.0,
                stroke="#777777",
                stroke_width=1.4,
                rx=6.0,
                ry=6.0,
                fill="none",
            ),
            TextSlot(
                id="slot.b1",
                prompt="",
                text="• ㉠는 ㉡보다 작은 수입니다.",
                style_role="question",
                x=38.0,
                y=206.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.b2",
                prompt="",
                text="• 세 수의 합과 1000의 차가 가장 작습니다.",
                style_role="question",
                x=38.0,
                y=252.0,
                font_size=28,
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=("세 자리 수", "조건", "합", "최솟값"),
    )


PROBLEM_TEMPLATE = build_problem_template()
SEMANTIC_OVERRIDE = {
    "problem_id": "Hpdf_IfXEqd2FAo",
    "problem_type": "number_construction",
    "metadata": {
        "language": "ko",
        "question": "1부터 9까지의 숫자를 모두 한 번씩만 사용하여 3개의 세 자리 수 529, ㉠, ㉡를 만들고, 조건을 만족할 때 가장 작은 수 ㉠를 구하는 문제",
        "instruction": "가장 작은 수 ㉠를 구하시오.",
    },
    "domain": {
        "objects": [
            {"id": "obj.fixed_number", "type": "three_digit_number", "value": 529},
            {"id": "obj.var_a", "type": "three_digit_number", "label": "㉠"},
            {"id": "obj.var_b", "type": "three_digit_number", "label": "㉡"},
            {
                "id": "obj.digits",
                "type": "digit_set",
                "range": "1-9",
                "usage": "each exactly once",
            },
        ],
        "relations": [
            {
                "id": "rel.use_digits_once",
                "type": "digit_partition",
                "from_id": "obj.digits",
                "to_id": "obj.fixed_number",
            },
            {
                "id": "rel.order",
                "type": "less_than",
                "from_id": "obj.var_a",
                "to_id": "obj.var_b",
            },
            {
                "id": "rel.sum_closest_to_1000",
                "type": "minimize_distance_to_target",
                "from_id": "obj.fixed_number",
                "to_id": "obj.var_a",
                "target": 1000,
            },
        ],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.fixed_number", "obj.digits"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.order", "rel.sum_closest_to_1000"],
            },
            "plan": {
                "method": "digit_partition_and_minimize_gap",
                "description": "1부터 9까지의 숫자를 한 번씩만 나누어 529, ㉠, ㉡를 만들고, 세 수의 합이 1000에 가장 가까워지도록 한다. 그중 ㉠가 ㉡보다 작아야 한다.",
            },
            "execute": {
                "expected_operations": [
                    "partition_digits",
                    "compare_possible_numbers",
                    "choose_minimum_valid_a",
                ]
            },
            "review": {
                "check_methods": [
                    "all_digits_used_once",
                    "a_less_than_b",
                    "sum_closest_to_1000",
                ]
            },
        },
    },
    "answer": {
        "target": {
            "type": "smallest_three_digit_number",
            "description": "조건을 모두 만족하는 가장 작은 수 ㉠",
        },
        "value": None,
        "unit": "",
    },
}
SOLVABLE = {   'schema': 'modu.solvable.v1',
    'problem_id': 'Hpdf_IfXEqd2FAo',
    'problem_type': 'number_construction',
    'inputs': {   'total_ticks': 9,
                  'target_label': 'smallest_three_digit_number',
                  'target_ticks': 3,
                  'target_count': 1,
                  'unit': ''},
    'plan': [   'Use digits 1..9 exactly once to form 529, A, and B.',
                'Keep A < B and make 529 + A + B closest to 1000.',
                'Among valid cases, choose the minimum A.'],
    'steps': [   {   'id': 's1',
                     'expr': 'generate candidates for A and B from remaining digits',
                     'value': 'candidate enumeration'},
                 {   'id': 's2',
                     'expr': 'minimize abs((529 + A + B) - 1000) with A < B',
                     'value': 'best candidate selected'},
                 {'id': 's3', 'expr': 'final A', 'value': 136}],
    'checks': [   {   'id': 'c1',
                      'expr': 'digits 1..9 used exactly once',
                      'expected': True,
                      'actual': True,
                      'pass': True},
                  {'id': 'c2', 'expr': 'A < B', 'expected': True, 'actual': True, 'pass': True},
                  {   'id': 'c3',
                      'expr': 'abs((529 + A + B) - 1000) is minimal',
                      'expected': True,
                      'actual': True,
                      'pass': True}],
    'answer': {'value': 136, 'unit': ''}}
