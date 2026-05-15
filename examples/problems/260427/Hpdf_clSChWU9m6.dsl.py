from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="Hpdf_clSChWU9m6",
        title="색종이 문제",
        canvas=Canvas(width=560, height=170, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem", role="stem", flow="absolute", slot_ids=("slot.q1",)
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="색종이를 국진이는 456장, 수지는 372장 가지\n고 있습니다. 국진이와 수지가 가진 색종이의\n수가 같아지려면 국진이는 수지에게 색종이를\n몇 장 주어야 합니까?",
                style_role="question",
                x=10.0,
                y=32.0,
                font_size=28,
                anchor="start",
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()
SEMANTIC_OVERRIDE = {
    "problem_id": "Hpdf_clSChWU9m6",
    "problem_type": "difference_equalization",
    "metadata": {
        "language": "ko",
        "question": "국진이와 수지가 가진 색종이의 수가 같아지려면 국진이는 수지에게 색종이를 몇 장 주어야 하는가?",
        "instruction": "",
    },
    "domain": {
        "objects": [
            {"id": "obj.gukjin", "type": "person", "name": "국진이"},
            {"id": "obj.suji", "type": "person", "name": "수지"},
            {
                "id": "obj.gukjin_papers",
                "type": "quantity",
                "quantity_type": "paper_count",
                "value": 456,
            },
            {
                "id": "obj.suji_papers",
                "type": "quantity",
                "quantity_type": "paper_count",
                "value": 372,
            },
        ],
        "relations": [
            {
                "id": "rel.compare_counts",
                "type": "compare",
                "from_id": "obj.gukjin_papers",
                "to_id": "obj.suji_papers",
                "relation": "greater_than",
            },
            {
                "id": "rel.equalize_by_transfer",
                "type": "transfer_to_equalize",
                "from_id": "obj.gukjin",
                "to_id": "obj.suji",
                "source_quantity": "obj.gukjin_papers",
                "target_quantity": "obj.suji_papers",
            },
        ],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.gukjin_papers", "obj.suji_papers"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.equalize_by_transfer"],
            },
            "plan": {
                "method": "difference_then_half",
                "description": "두 수의 차이를 구한 뒤, 같은 수가 되도록 옮길 양은 그 차이의 절반으로 본다.",
            },
            "execute": {
                "expected_operations": ["compute_difference", "divide_difference_by_2"]
            },
            "review": {"check_methods": ["equal_counts_after_transfer"]},
        },
    },
    "answer": {
        "target": {
            "type": "transfer_amount",
            "description": "국진이가 수지에게 주어야 하는 색종이 수",
        },
        "value": None,
        "unit": "장",
    },
}
SOLVABLE = {   'schema': 'modu.solvable.v1',
    'problem_id': 'Hpdf_clSChWU9m6',
    'problem_type': 'difference_equalization',
    'inputs': {   'total_ticks': 456,
                  'target_label': '국진이가 수지에게 주어야 할 색종이 수',
                  'target_ticks': 42,
                  'target_count': 42,
                  'unit': '장'},
    'plan': ['두 사람의 색종이 수의 차이를 구한다.', '그 차이의 절반을 국진이가 수지에게 주면 두 사람이 갖게 되는 색종이 수가 같아진다.'],
    'steps': [   {'id': 'step.s1', 'expr': '456 - 372', 'value': 84},
                 {'id': 'step.s2', 'expr': '84 / 2', 'value': 42}],
    'checks': [   {   'id': 'check.c1',
                      'expr': '국진이의 남은 색종이 수 (456 - 42)',
                      'expected': 414,
                      'actual': 414,
                      'pass': True},
                  {   'id': 'check.c2',
                      'expr': '수지의 늘어난 색종이 수 (372 + 42)',
                      'expected': 414,
                      'actual': 414,
                      'pass': True}],
    'answer': {'value': 42, 'unit': '장'}}
