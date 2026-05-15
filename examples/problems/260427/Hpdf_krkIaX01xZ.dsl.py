from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, RectSlot, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="Hpdf_krkIaX01xZ",
        title="□ 안에 들어갈 수 있는 세 자리 수",
        canvas=Canvas(width=650, height=260, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q1", "slot.q2", "slot.box", "slot.expr"),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="□ 안에 들어갈 수 있는 세 자리 수는 모두 몇 개인가?",
                style_role="question",
                x=10.0,
                y=34.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q2",
                prompt="",
                text="",
                style_role="question",
                x=0.0,
                y=0.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.box",
                prompt="",
                x=68.0,
                y=118.0,
                width=402.0,
                height=55.0,
                stroke="#8A8A8A",
                stroke_width=1.2,
                rx=7.0,
                ry=7.0,
                fill="none",
            ),
            TextSlot(
                id="slot.expr",
                prompt="",
                text="991−□ > 397+108",
                style_role="equation",
                x=141.0,
                y=152.0,
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
    "problem_id": "Hpdf_krkIaX01xZ",
    "problem_type": "inequality_count",
    "metadata": {
        "language": "ko",
        "question": "□ 안에 들어갈 수 있는 세 자리 수는 모두 몇 개인가?",
        "instruction": "부등식 991－□ > 397+108을 만족하는 세 자리 수 □의 개수를 구한다.",
    },
    "domain": {
        "objects": [
            {"id": "var.box", "type": "integer_variable", "label": "□", "range": [100, 999]},
            {"id": "expr.left", "type": "subtraction_expression", "left": 991, "right": "var.box"},
            {"id": "expr.right", "type": "addition_expression", "left": 397, "right": 108},
        ],
        "relations": [
            {
                "id": "rel.inequality",
                "type": "greater_than",
                "left": "expr.left",
                "right": "expr.right",
            },
            {
                "id": "rel.count_target",
                "type": "count_satisfying_values",
                "variable": "var.box",
                "condition": "rel.inequality",
            },
        ],
        "problem_solving": {
            "understand": {
                "given_refs": ["expr.left", "expr.right"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.inequality"],
            },
            "plan": {
                "method": "inequality_rearrangement",
                "description": "991 - □ > 505 식을 □ < 991 - 505 형태로 변형하여 범위를 구한다.",
            },
            "execute": {
                "expected_operations": [
                    "compute_sum",
                    "compute_difference_limit",
                    "count_integers_in_range",
                ]
            },
            "review": {"check_methods": ["boundary_verification", "range_size_verification"]},
        },
    },
    "answer": {
        "target": {
            "type": "count",
            "ref": "rel.count_target",
            "description": "부등식을 만족하는 세 자리 수 □의 개수",
        },
        "value": 386,
        "unit": "개",
    },
}
SOLVABLE = {   'schema': 'modu.solvable.v1',
    'problem_id': 'Hpdf_krkIaX01xZ',
    'problem_type': 'inequality_count',
    'inputs': {   'total_ticks': 991,
                  'target_label': '조건을 만족하는 세 자리 수의 개수',
                  'target_ticks': 386,
                  'target_count': 386,
                  'unit': '개'},
    'plan': [   '부등식 우변의 합 397 + 108을 먼저 계산한다.',
                '991 - □ > (우변의 합) 식을 정리하여 □의 범위를 찾는다.',
                '□가 세 자리 수(100 이상)라는 조건을 고려하여 가능한 자연수의 개수를 구한다.'],
    'steps': [   {'id': 'step.s1', 'expr': '397 + 108', 'value': 505},
                 {'id': 'step.s2', 'expr': '991 - 505', 'value': 486},
                 {'id': 'step.s3', 'expr': '485 - 100 + 1', 'value': 386}],
    'checks': [   {   'id': 'check.c1',
                      'expr': '□=485일 때 부등식 성립 확인 (991 - 485 > 505)',
                      'expected': True,
                      'actual': True,
                      'pass': True},
                  {   'id': 'check.c2',
                      'expr': '□=486일 때 부등식 불성립 확인 (991 - 486 > 505)',
                      'expected': False,
                      'actual': False,
                      'pass': True}],
    'answer': {'value': 386, 'unit': '개'}}
