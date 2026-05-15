from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot, RectSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="Hpdf_WOZc0ipjaC",
        title="기호 규칙 계산",
        canvas=Canvas(width=600, height=264, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q1", "slot.q2", "slot.note", "slot.box", "slot.expr"),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="기호 ◉를 ㉠◉㉡=㉠+㉡-482와 같이",
                style_role="question",
                x=12.0,
                y=42.0,
                font_size=35,
            ),
            TextSlot(
                id="slot.q2",
                prompt="",
                text="약속할 때 다음을 계산하시오.",
                style_role="question",
                x=12.0,
                y=92.0,
                font_size=35,
            ),
            TextSlot(
                id="slot.note",
                prompt="",
                text="(단, 기호 ◉를 먼저 계산합니다.)",
                style_role="question",
                x=12.0,
                y=142.0,
                font_size=35,
            ),
            RectSlot(
                id="slot.box",
                prompt="",
                x=90.0,
                y=180.0,
                width=380.0,
                height=70.0,
                stroke="#8A8A8A",
                stroke_width=1.5,
                rx=10.0,
                ry=10.0,
                fill="#FFFFFF",
            ),
            TextSlot(
                id="slot.expr",
                prompt="",
                text="197 ◉ 631 + 197",
                style_role="expression",
                x=280.0,
                y=228.0,
                font_size=35,
                anchor="middle",
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()
SEMANTIC_OVERRIDE = {
    "problem_id": "Hpdf_WOZc0ipjaC",
    "problem_type": "symbol_rule_calculation",
    "metadata": {
        "language": "ko",
        "question": "기호 ◉를 ㉠◉㉡=㉠+㉡-482와 같이 약속할 때 다음을 계산하는 문제",
        "instruction": "기호 ◉를 먼저 계산합니다.",
    },
    "domain": {
        "objects": [
            {
                "id": "obj.rule",
                "type": "custom_operation_rule",
                "description": "㉠ ◉ ㉡ = ㉠ + ㉡ - 482",
            },
            {
                "id": "obj.expression",
                "type": "expression",
                "description": "197 ◉ 631 + 197",
            },
        ],
        "relations": [
            {
                "id": "rel.apply_rule",
                "type": "operation_definition_applied_to_expression",
                "from_id": "obj.rule",
                "to_id": "obj.expression",
            }
        ],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.rule", "obj.expression"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.apply_rule"],
            },
            "plan": {
                "method": "define_operation_then_substitute",
                "description": "기호 ◉의 뜻을 식에 대입한 뒤, 먼저 ◉ 부분을 계산하고 그 결과에 197을 더한다.",
            },
            "execute": {
                "expected_operations": [
                    "evaluate_custom_operation",
                    "add_remaining_number",
                ]
            },
            "review": {
                "check_methods": [
                    "definition_substitution_check",
                    "arithmetic_consistency_check",
                ]
            },
        },
    },
    "answer": {
        "target": {
            "type": "value_of_expression",
            "description": "197 ◉ 631 + 197의 값",
        },
        "value": 543,
        "unit": "",
    },
}
SOLVABLE = {   'schema': 'modu.solvable.v1',
    'problem_id': 'Hpdf_WOZc0ipjaC',
    'problem_type': 'symbol_rule_calculation',
    'given': [   {'ref': 'obj.rule', 'value': {'definition': 'a ◉ b = a + b - 482'}},
                 {'ref': 'obj.expression', 'value': '197 ◉ 631 + 197'}],
    'target': {'ref': 'answer.target', 'type': 'value_of_expression'},
    'method': 'define_operation_then_substitute',
    'steps': [   {   'id': 'step.s1',
                     'operation': 'evaluate_custom_operation',
                     'expr': '197 ◉ 631 = 197 + 631 - 482',
                     'value': 346},
                 {   'id': 'step.s2',
                     'operation': 'add_remaining_number',
                     'expr': '346 + 197',
                     'value': 543}],
    'checks': [   {   'id': 'check.c1',
                      'type': 'definition_substitution_check',
                      'pass': True,
                      'expected': 1,
                      'actual': 1,
                      'expr': 'check'},
                  {   'id': 'check.c2',
                      'type': 'arithmetic_consistency_check',
                      'pass': True,
                      'expected': 1,
                      'actual': 1,
                      'expr': 'check'}],
    'answer': {'value': 543, 'unit': '', 'derived_from': 'step.s2'},
    'inputs': {   'total_ticks': 1,
                  'target_label': '답',
                  'target_ticks': 1,
                  'target_count': 1,
                  'unit': ''},
    'plan': ['풀이 과정 없음']}
