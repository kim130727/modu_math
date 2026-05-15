from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="Hpdf_Y5TZAL9Fiw",
        title="세 자리 수 덧셈",
        canvas=Canvas(width=580, height=206, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem", role="stem", flow="absolute", slot_ids=("slot.q1",)
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="각 자리의 숫자가 모두 다른 세 자리 수 ㉠㉡㉢에\n475를 더했더니 자리의 숫자가 모두 같았습니다.\n이와 같은 세 자리 수 ㉠㉡㉢은 모두 몇 개입니까?",
                style_role="question",
                x=18.0,
                y=40.0,
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
    "problem_id": "Hpdf_Y5TZAL9Fiw",
    "problem_type": "digit_sum_counting",
    "metadata": {
        "language": "ko",
        "question": "각 자리의 숫자가 모두 다른 세 자리 수 ㉠㉡㉢에 475를 더했더니 자릿의 숫자가 모두 같았습니다. 이와 같은 세 자리 수 ㉠㉡㉢은 모두 몇 개입니까?",
        "instruction": "세 자리 수의 개수를 구하시오.",
    },
    "domain": {
        "objects": [
            {"id": "obj.number", "type": "three_digit_number", "digit_distinct": True},
            {"id": "obj.addend", "type": "number", "value": 475},
            {"id": "obj.result", "type": "three_digit_number", "digit_same": True},
        ],
        "relations": [
            {
                "id": "rel.addition",
                "type": "addition",
                "from_id": "obj.number",
                "to_id": "obj.result",
                "addend": "obj.addend",
            }
        ],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.number", "obj.addend"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.addition"],
            },
            "plan": {
                "method": "digit_case_analysis",
                "description": "더한 뒤 세 자리 숫자의 각 자리 수가 모두 같아지는 조건을 자릿수별로 따져 가능한 원래 수를 센다.",
            },
            "execute": {
                "expected_operations": [
                    "analyze_digit_constraints",
                    "check_carry_cases",
                    "count_valid_numbers",
                ]
            },
            "review": {
                "check_methods": ["addition_inverse_check", "digit_distinctness_check"]
            },
        },
    },
    "answer": {
        "target": {
            "type": "count",
            "description": "조건을 만족하는 세 자리 수 ㉠㉡㉢의 개수",
        },
        "value": 3,
        "unit": "개",
    },
}
SOLVABLE = {   'schema': 'modu.solvable.v1',
    'problem_id': 'Hpdf_Y5TZAL9Fiw',
    'problem_type': 'digit_sum_counting',
    'given': [   {'ref': 'obj.addend', 'value': 475},
                 {'ref': 'obj.number', 'value': {'digit_distinct': True}}],
    'target': {'ref': 'answer.target', 'type': 'count'},
    'method': 'digit_case_analysis',
    'steps': [   {   'id': 'step.s1',
                     'operation': 'analyze_digit_constraints',
                     'expr': '세 자리 수 + 475의 각 자리가 모두 같아야 함',
                     'value': '가능한 결과는 111, 222, ..., 999 형태'},
                 {   'id': 'step.s2',
                     'operation': 'check_carry_cases',
                     'expr': '원래 수 = 결과 - 475',
                     'value': '각 결과마다 자리별 조건과 서로 다른 숫자 조건을 확인'},
                 {   'id': 'step.s3',
                     'operation': 'count_valid_numbers',
                     'expr': '조건을 만족하는 경우의 수 합산',
                     'value': 3}],
    'checks': [   {   'id': 'check.c1',
                      'type': 'addition_inverse_check',
                      'pass': True,
                      'expected': 1,
                      'actual': 1,
                      'expr': 'check'},
                  {   'id': 'check.c2',
                      'type': 'digit_distinctness_check',
                      'pass': True,
                      'expected': 1,
                      'actual': 1,
                      'expr': 'check'}],
    'answer': {'value': 3, 'unit': '개', 'derived_from': 'step.s3'},
    'inputs': {   'total_ticks': 1,
                  'target_label': '답',
                  'target_ticks': 1,
                  'target_count': 1,
                  'unit': ''},
    'plan': ['풀이 과정 없음']}
