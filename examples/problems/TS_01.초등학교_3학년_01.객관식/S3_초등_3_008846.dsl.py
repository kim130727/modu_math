from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008846",
        title="양배추의 무게를 어림하기",
        canvas=Canvas(width=856.0, height=328.0, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.header",
                role="stem",
                flow="absolute",
                slot_ids=("slot.header.num", "slot.header.text"),
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=("slot.cabbage", "slot.bubble.line1", "slot.bubble.line2", "slot.child"),
            ),
            Region(
                id="region.choices",
                role="choices",
                flow="absolute",
                slot_ids=("slot.choice.1", "slot.choice.2", "slot.choice.3"),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.header.num",
                prompt="",
                text="85.",
                style_role="question",
                x=13.0,
                y=24.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.header.text",
                prompt="",
                text="양배추의 무게를 어림하려고 합니다. 알맞은 것을 선택하세요.",
                style_role="question",
                x=52.0,
                y=24.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.cabbage",
                prompt="",
                text="양배추 그림",
                style_role="diagram",
                x=192.0,
                y=96.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.bubble.line1",
                prompt="",
                text="1 kg인 밀가루와 100 g인 귤로",
                style_role="speech",
                x=410.0,
                y=94.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.bubble.line2",
                prompt="",
                text="양배추의 무게를 어림해 볼까?",
                style_role="speech",
                x=446.0,
                y=126.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.child",
                prompt="",
                text="아이 그림",
                style_role="diagram",
                x=739.0,
                y=94.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice.1",
                prompt="",
                text="(2) 양배추의 무게는 귤 9개와 비슷하므로 약 ( 900 g , 900 kg )입니다.",
                style_role="choice",
                x=10.0,
                y=212.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice.2",
                prompt="",
                text="(2) 양배추의 무게는 100 g인 귤 9개와 비슷하므로 약 900 g입니다.",
                style_role="choice",
                x=10.0,
                y=265.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice.3",
                prompt="",
                text="(2) 900 g",
                style_role="choice",
                x=10.0,
                y=311.0,
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
    "problem_id": "S3_초등_3_008846",
    "problem_type": "estimate_weight_choice",
    "metadata": {
        "language": "ko",
        "question": "양배추의 무게를 어림하는 알맞은 것을 선택하는 문제",
        "instruction": "알맞은 것을 선택하세요.",
    },
    "domain": {
        "objects": [
            {"id": "obj.cabbage", "type": "vegetable", "name": "양배추"},
            {
                "id": "obj.flour",
                "type": "food",
                "name": "밀가루",
                "mass_unit": "kg",
                "mass_value": 1,
            },
            {
                "id": "obj.orange",
                "type": "fruit",
                "name": "귤",
                "mass_unit": "g",
                "mass_value": 100,
            },
            {"id": "obj.orange_group", "type": "group", "name": "귤 9개", "count": 9},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.flour", "obj.orange", "obj.orange_group", "obj.cabbage"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.estimate_by_comparison"],
            },
            "plan": {
                "method": "comparison_estimation",
                "description": "기준 물체의 무게를 바탕으로 양배추의 무게를 어림하고, 보기에서 알맞은 값을 고른다.",
            },
            "execute": {
                "expected_operations": ["compare_reference_mass", "choose_reasonable_estimate"]
            },
            "review": {"check_methods": ["unit_consistency_check", "reasonableness_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "estimated_mass_choice",
            "description": "양배추의 무게를 어림한 알맞은 보기",
        },
        "value": 900,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008846",
    "problem_type": "estimate_weight_choice",
    "inputs": {
        "total_ticks": 1,
        "target_label": "estimated_mass_choice",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.flour", "value": {"mass_unit": "kg", "mass_value": 1}},
        {"ref": "obj.orange", "value": {"mass_unit": "g", "mass_value": 100}},
        {"ref": "obj.orange_group", "value": {"count": 9}},
    ],
    "target": {"ref": "answer.target", "type": "estimated_mass_choice"},
    "method": "comparison_estimation",
    "plan": [
        "기준 물체인 100 g 귤 9개의 무게를 보고 양배추와 비교한다.",
        "보기 중에서 양배추의 무게로 어울리는 값을 선택한다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "100 g × 9", "value": 900},
        {"id": "step.2", "expr": "귤 9개의 무게를 g로 나타내면 900 g", "value": 900},
        {"id": "step.3", "expr": "양배추의 무게를 어림한 알맞은 보기 선택", "value": 900},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "단위가 g인지 확인",
            "expected": "g",
            "actual": "g",
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "보기 중 900 g이 있는지 확인",
            "expected": True,
            "actual": True,
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "estimated_mass_choice",
            "description": "양배추의 무게를 어림한 알맞은 보기",
        },
        "value": 900,
        "unit": "",
    },
}
