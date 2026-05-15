from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="Hpdf_J4FL8G67OW",
        title="과일 가게 나눗셈 문제",
        canvas=Canvas(width=640, height=160, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem", role="stem", flow="absolute", slot_ids=("slot.q1",)
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="과일 가게에 참외 748개, 자두 562개가 있었습니다.\n 그중에서 참외는 259개, 자두는 175개 팔았다면\n 남은 참외와 자두는 몇 개인가요?",
                style_role="question",
                x=8.0,
                y=34.0,
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
    "problem_id": "Hpdf_J4FL8G67OW",
    "problem_type": "subtraction_word_problem",
    "metadata": {
        "language": "ko",
        "question": "과일 가게에 참외 748개, 자두 562개가 있었습니다. 그중에서 참외는 259개, 자두는 175개 팔았다면 남은 참외와 자두는 몇 개인가요?",
        "instruction": "남은 참외와 자두의 개수를 구하시오.",
    },
    "domain": {
        "objects": [
            {
                "id": "obj.melon_initial",
                "type": "quantity",
                "item": "참외",
                "value": 748,
                "unit": "개",
            },
            {
                "id": "obj.plum_initial",
                "type": "quantity",
                "item": "자두",
                "value": 562,
                "unit": "개",
            },
            {
                "id": "obj.melon_sold",
                "type": "quantity",
                "item": "참외",
                "value": 259,
                "unit": "개",
            },
            {
                "id": "obj.plum_sold",
                "type": "quantity",
                "item": "자두",
                "value": 175,
                "unit": "개",
            },
            {
                "id": "obj.melon_remaining",
                "type": "quantity",
                "item": "참외",
                "unit": "개",
            },
            {
                "id": "obj.plum_remaining",
                "type": "quantity",
                "item": "자두",
                "unit": "개",
            },
        ],
        "relations": [
            {
                "id": "rel.melon_subtract",
                "type": "remaining_after_subtraction",
                "from_id": "obj.melon_initial",
                "to_id": "obj.melon_remaining",
                "subtrahend_id": "obj.melon_sold",
            },
            {
                "id": "rel.plum_subtract",
                "type": "remaining_after_subtraction",
                "from_id": "obj.plum_initial",
                "to_id": "obj.plum_remaining",
                "subtrahend_id": "obj.plum_sold",
            },
        ],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "obj.melon_initial",
                    "obj.plum_initial",
                    "obj.melon_sold",
                    "obj.plum_sold",
                ],
                "target_ref": "answer.target",
                "condition_refs": ["rel.melon_subtract", "rel.plum_subtract"],
            },
            "plan": {
                "method": "separate_subtraction",
                "description": "참외와 자두를 각각 처음 개수에서 판 개수를 빼서 남은 개수를 구한다.",
            },
            "execute": {"expected_operations": ["748-259", "562-175"]},
            "review": {
                "check_methods": ["subtraction_inverse_check", "unit_consistency_check"]
            },
        },
    },
    "answer": {
        "target": {
            "type": "remaining_quantities",
            "description": "남은 참외와 자두의 개수",
            "components": ["참외", "자두"],
        },
        "value": None,
        "unit": "개",
    },
}
SOLVABLE = {   'schema': 'modu.solvable.v1',
    'problem_id': 'Hpdf_J4FL8G67OW',
    'problem_type': 'subtraction_word_problem',
    'inputs': {   'total_ticks': 1310,
                  'target_label': '남은 참외와 자두의 개수',
                  'target_ticks': 876,
                  'target_count': 876,
                  'unit': '개'},
    'plan': ['처음 있던 참외 수에서 판 참외 수를 빼서 남은 참외 수를 구한다.', '처음 있던 자두 수에서 판 자두 수를 빼서 남은 자두 수를 구한다.'],
    'steps': [   {'id': 'step.s1', 'expr': '748 - 259', 'value': 489},
                 {'id': 'step.s2', 'expr': '562 - 175', 'value': 387}],
    'checks': [   {   'id': 'check.c1',
                      'expr': '남은 참외와 판 참외의 합 (489 + 259)',
                      'expected': 748,
                      'actual': 748,
                      'pass': True},
                  {   'id': 'check.c2',
                      'expr': '남은 자두와 판 자두의 합 (387 + 175)',
                      'expected': 562,
                      'actual': 562,
                      'pass': True}],
    'answer': {'value': 876, 'unit': '개'}}
