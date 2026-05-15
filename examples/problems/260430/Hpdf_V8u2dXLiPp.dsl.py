from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="Hpdf_V8u2dXLiPp",
        title="수 카드로 만들 수 있는 수",
        canvas=Canvas(width=568, height=353, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q1", "slot.q2", "slot.q3", "slot.q4", "slot.q5"),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="민하와 하리는 0부터 9까지의 수 카드를 5장",
                style_role="question",
                x=20.0,
                y=40.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q2",
                prompt="",
                text="씩 똑같이 나누어 가졌습니다. 민하가 수 카드",
                style_role="question",
                x=20.0,
                y=84.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q3",
                prompt="",
                text="로 만든 가장 큰 네 자리 수는 8742이고, 가장",
                style_role="question",
                x=20.0,
                y=128.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q4",
                prompt="",
                text="작은 네 자리 수는 2047입니다. 두 사람이 만",
                style_role="question",
                x=20.0,
                y=172.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q5",
                prompt="",
                text="들 수 있는 가장 큰 세 자리 수의 합을 구하시오.",
                style_role="question",
                x=20.0,
                y=216.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q6",
                prompt="",
                text="(단, 수를 만들 때 수 카드를 한 번씩만 사용합니다.)",
                style_role="question",
                x=20.0,
                y=260.0,
                font_size=28,
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()
SEMANTIC_OVERRIDE = {
    "problem_id": "Hpdf_V8u2dXLiPp",
    "problem_type": "number_construction",
    "metadata": {
        "language": "ko",
        "question": "수 카드로 만들 수 있는 가장 큰 세 자리 수의 합을 구하는 문제",
        "instruction": "두 사람이 만들 수 있는 가장 큰 세 자리 수의 합을 구하시오.",
    },
    "domain": {
        "objects": [
            {
                "id": "obj.cards",
                "type": "digit_cards",
                "digits": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                "count_each_per_person": 5,
            },
            {"id": "obj.minha_max", "type": "number", "value": 8742},
            {"id": "obj.minha_min", "type": "number", "value": 2047},
            {"id": "obj.hari_max3", "type": "number", "value": None},
            {"id": "obj.minha_max3", "type": "number", "value": None},
        ],
        "relations": [
            {
                "id": "rel.partition_cards",
                "type": "disjoint_partition",
                "from_id": "obj.cards",
                "to_id": "obj.minha_max",
            },
            {
                "id": "rel.construct_max",
                "type": "make_largest_number",
                "from_id": "obj.cards",
                "to_id": "obj.minha_max",
            },
            {
                "id": "rel.construct_min",
                "type": "make_smallest_number",
                "from_id": "obj.cards",
                "to_id": "obj.minha_min",
            },
            {
                "id": "rel.find_sum",
                "type": "sum_numbers",
                "from_id": "obj.minha_max3",
                "to_id": "obj.hari_max3",
            },
        ],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.cards", "obj.minha_max", "obj.minha_min"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.construct_max", "rel.construct_min"],
            },
            "plan": {
                "method": "digit_complement_and_maximum_construction",
                "description": "민하가 사용한 숫자를 제외해 하리가 가진 숫자를 찾고, 각 사람이 만들 수 있는 가장 큰 세 자리 수를 만든 뒤 합한다.",
            },
            "execute": {
                "expected_operations": [
                    "identify_remaining_digits",
                    "construct_largest_three_digit_number_for_each_person",
                    "add_two_numbers",
                ]
            },
            "review": {
                "check_methods": ["digit_usage_check", "sum_reasonableness_check"]
            },
        },
    },
    "answer": {
        "target": {
            "type": "sum_of_largest_three_digit_numbers",
            "description": "두 사람이 만들 수 있는 가장 큰 세 자리 수의 합",
        },
        "value": 1839,
        "unit": "",
    },
}
SOLVABLE = {   'schema': 'modu.solvable.v1',
    'problem_id': 'Hpdf_V8u2dXLiPp',
    'problem_type': 'number_construction',
    'given': [   {'ref': 'obj.minha_max', 'value': 8742},
                 {'ref': 'obj.minha_min', 'value': 2047},
                 {   'ref': 'obj.cards',
                     'value': {   'digits': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                                  'count_each_per_person': 5}}],
    'target': {'ref': 'answer.target', 'type': 'sum_of_largest_three_digit_numbers'},
    'method': 'digit_complement_and_maximum_construction',
    'steps': [   {   'id': 'step.s1',
                     'operation': 'identify_used_digits',
                     'expr': '8742와 2047에 사용된 숫자 파악',
                     'value': {'minha_used': [8, 7, 4, 2, 0], 'minha_unused': [1, 3, 5, 6, 9]}},
                 {   'id': 'step.s2',
                     'operation': 'identify_remaining_digits',
                     'expr': '0~9 중 민하가 쓰지 않은 숫자',
                     'value': [1, 3, 5, 6, 9]},
                 {   'id': 'step.s3',
                     'operation': 'construct_largest_three_digit_number',
                     'expr': '민하의 가장 큰 세 자리 수',
                     'value': 874},
                 {   'id': 'step.s4',
                     'operation': 'construct_largest_three_digit_number',
                     'expr': '하리의 가장 큰 세 자리 수',
                     'value': 965},
                 {   'id': 'step.s5',
                     'operation': 'add_two_numbers',
                     'expr': '874 + 965',
                     'value': 1839}],
    'checks': [   {   'id': 'check.c1',
                      'type': 'digit_usage_check',
                      'pass': True,
                      'expected': 1,
                      'actual': 1,
                      'expr': 'check'},
                  {   'id': 'check.c2',
                      'type': 'arithmetic_check',
                      'pass': True,
                      'expected': 1,
                      'actual': 1,
                      'expr': 'check'}],
    'answer': {'value': 1839, 'unit': '', 'derived_from': 'step.s5'},
    'inputs': {   'total_ticks': 1,
                  'target_label': '답',
                  'target_ticks': 1,
                  'target_count': 1,
                  'unit': ''},
    'plan': ['풀이 과정 없음']}
