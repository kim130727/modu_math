from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot, RectSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008741",
        title="분수의 크기 비교",
        canvas=Canvas(width=945, height=945, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.q1", "slot.q2")),
            Region(
                id="region.diagram1",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.d1.root",
                    "slot.d1.mid.left",
                    "slot.d1.mid.right",
                    "slot.d1.leaf.l1",
                    "slot.d1.leaf.l2",
                    "slot.d1.leaf.r1",
                    "slot.d1.leaf.r2",
                ),
            ),
            Region(id="region.diagram2", role="diagram", flow="absolute", slot_ids=()),
            Region(id="region.explain", role="explanation", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="□ 27. 두 분수의 크기를 비교하여 더 큰 분수만 비켜나 써보려고 합니다.",
                style_role="question",
                x=20.0,
                y=35.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q2",
                prompt="",
                text="⑦에 들어갈 분수로 알맞은 것을 가장 아래 칸의 분수들 중에 선택해 보세요.",
                style_role="question",
                x=20.0,
                y=72.0,
                font_size=28,
            ),
            RectSlot(id="slot.d1.root", prompt="", x=465.0, y=110.0, width=80.0, height=80.0),
            RectSlot(id="slot.d1.mid.left", prompt="", x=360.0, y=215.0, width=80.0, height=80.0),
            RectSlot(id="slot.d1.mid.right", prompt="", x=550.0, y=215.0, width=80.0, height=80.0),
            RectSlot(id="slot.d1.leaf.l1", prompt="", x=310.0, y=350.0, width=70.0, height=80.0),
            RectSlot(id="slot.d1.leaf.l2", prompt="", x=395.0, y=350.0, width=70.0, height=80.0),
            RectSlot(id="slot.d1.leaf.r1", prompt="", x=500.0, y=350.0, width=70.0, height=80.0),
            RectSlot(id="slot.d1.leaf.r2", prompt="", x=585.0, y=350.0, width=70.0, height=80.0),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008741",
    "problem_type": "fraction_comparison",
    "metadata": {
        "language": "ko",
        "question": "두 분수의 크기를 비교하여 더 큰 분수만 비켜나 써보려고 합니다.",
        "instruction": "⑦에 들어갈 분수로 알맞은 것을 가장 아래 칸의 분수들 중에 선택해 보세요.",
    },
    "domain": {
        "objects": [
            {"id": "obj.f1", "type": "fraction", "value": "34/9"},
            {"id": "obj.f2", "type": "mixed_fraction", "value": "3 5/9"},
            {"id": "obj.f3", "type": "mixed_fraction", "value": "4 1/9"},
            {"id": "obj.f4", "type": "fraction", "value": "31/9"},
            {"id": "obj.target", "type": "blank", "label": "⑦"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.f1", "obj.f2", "obj.f3", "obj.f4", "obj.target"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.c1", "rel.c2", "rel.c3", "rel.c4"],
            },
            "plan": {
                "method": "fraction_comparison_with_mixed_number",
                "description": "같은 크기로 바꾸어 비교한 뒤 더 큰 분수를 고른다.",
            },
            "execute": {
                "expected_operations": [
                    "convert_fraction_to_mixed_number",
                    "compare_fractions",
                    "choose_larger_fraction",
                ]
            },
            "review": {"check_methods": ["equivalent_value_check", "inequality_direction_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_fraction", "description": "⑦에 들어갈 분수"},
        "value": "4 1/9",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008741",
    "problem_type": "fraction_comparison",
    "inputs": {
        "total_ticks": 1,
        "target_label": "⑦",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "plan": "같은 크기로 바꾸어 비교한 뒤 더 큰 분수를 선택한다.",
    "given": [
        {"ref": "obj.f1", "value": "34/9"},
        {"ref": "obj.f2", "value": "3 5/9"},
        {"ref": "obj.f3", "value": "4 1/9"},
        {"ref": "obj.f4", "value": "31/9"},
    ],
    "target": {"ref": "answer.target", "type": "selected_fraction"},
    "method": "fraction_comparison_with_mixed_number",
    "steps": [
        {"id": "step.1", "expr": "34/9 = 3 7/9", "value": "3 7/9"},
        {"id": "step.2", "expr": "31/9 < 34/9", "value": True},
        {"id": "step.3", "expr": "3 5/9 < 4 1/9", "value": True},
        {"id": "step.4", "expr": "34/9 < 4 1/9", "value": True},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "34/9 와 4 1/9의 크기 비교가 올바른가",
            "expected": True,
            "actual": True,
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "⑦에 선택되는 분수가 더 큰 분수인가",
            "expected": True,
            "actual": True,
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_fraction", "description": "⑦에 들어갈 분수"},
        "value": "4 1/9",
        "unit": "",
    },
}
