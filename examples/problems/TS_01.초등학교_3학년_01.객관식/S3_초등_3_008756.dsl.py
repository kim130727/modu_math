from __future__ import annotations
from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    Region,
    RectSlot,
    TextSlot,
    LineSlot,
    CircleSlot,
    PathSlot,
    ImageSlot,
)


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008756",
        title="500 mL 생수병을 보고 들이를 어림해 보세요",
        canvas=Canvas(width=940, height=510, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.q1",
                    "slot.bottle_label1",
                    "slot.bottle_label2",
                    "slot.cup_label",
                    "slot.s1",
                    "slot.s2",
                    "slot.arrow",
                    "slot.inserted.image.1",
                    "slot.inserted.image.2",
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="500 mL 생수병을 보고 들이를 어림해 보려고 합니다. 알맞은 것을 선택하세요.",
                style_role="question",
                x=13,
                y=53,
                font_size=28,
                fill="#111111",
            ),
            TextSlot(
                id="slot.bottle_label1",
                prompt="",
                text="생수병",
                style_role="label",
                x=259,
                y=290,
                font_size=28,
                fill="#111111",
            ),
            TextSlot(
                id="slot.bottle_label2",
                prompt="",
                text="500 mL",
                style_role="label",
                x=250,
                y=339,
                font_size=28,
                fill="#111111",
            ),
            TextSlot(
                id="slot.cup_label",
                prompt="",
                text="종이컵",
                style_role="label",
                x=549,
                y=290,
                font_size=28,
                fill="#111111",
            ),
            TextSlot(
                id="slot.s1",
                prompt="",
                text="종이컵의 들이는 500 mL 생수병의 들이보다 ( 많습니다, 적습니다 ).",
                style_role="question",
                x=63,
                y=408,
                font_size=28,
                fill="#111111",
            ),
            TextSlot(
                id="slot.arrow",
                prompt="",
                text="→",
                style_role="question",
                x=185,
                y=456,
                font_size=28,
                fill="#111111",
            ),
            TextSlot(
                id="slot.s2",
                prompt="",
                text="종이컵의 들이는 약 ( 180 mL , 180 L )입니다.",
                style_role="question",
                x=220,
                y=456,
                font_size=28,
                fill="#111111",
            ),
            ImageSlot(
                id="slot.inserted.image.1",
                prompt="",
                href="data:image/png;base64,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",
                x=210,
                y=90,
                width=160,
                height=165,
                preserve_aspect_ratio="xMidYMid meet",
            ),
            ImageSlot(
                id="slot.inserted.image.2",
                prompt="",
                href="data:image/png;base64,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",
                x=525,
                y=115,
                width=120,
                height=100,
                preserve_aspect_ratio="xMidYMid meet",
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008756",
    "problem_type": "volume_estimation_comparison",
    "metadata": {
        "language": "ko",
        "question": "500 mL 생수병을 보고 들이를 어림해 보려고 합니다. 알맞은 것을 선택하세요.",
        "instruction": "종이컵의 들이를 비교하여 알맞은 선택지를 고르기",
    },
    "domain": {
        "objects": [
            {
                "id": "obj.bottle",
                "type": "container",
                "name": "생수병",
                "capacity": {"value": 500, "unit": "mL"},
            },
            {"id": "obj.cup", "type": "container", "name": "종이컵"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.bottle", "obj.cup"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare_volume", "rel.estimate_volume"],
            },
            "plan": {
                "method": "volume_comparison_and_estimation",
                "description": "기준이 되는 500 mL 생수병과 비교하여 종이컵이 더 작은지 판단하고, 들이를 mL 단위의 어림값으로 고른다.",
            },
            "execute": {
                "expected_operations": [
                    "compare_volumes",
                    "select_appropriate_unit",
                    "choose_estimate",
                ]
            },
            "review": {
                "check_methods": [
                    "unit_consistency_check",
                    "comparison_reasonableness_check",
                ]
            },
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "choice",
            "description": "종이컵의 들이는 500 mL 생수병의 들이보다 (많습니다, 적습니다). 종이컵의 들이는 약 (180 mL, 180 L)입니다.",
        },
        "value": 180,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008756",
    "problem_type": "volume_estimation_comparison",
    "inputs": {
        "total_ticks": 1,
        "target_label": "종이컵의 들이",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "mL",
    },
    "given": [
        {"ref": "obj.bottle.capacity", "value": {"value": 500, "unit": "mL"}},
        {"ref": "obj.cup", "value": {"name": "종이컵"}},
    ],
    "target": {"ref": "answer.target", "type": "choice"},
    "method": "volume_comparison_and_estimation",
    "plan": [
        "500 mL 생수병을 기준으로 종이컵의 들이가 더 큰지 더 작은지 비교한다.",
        "어림값 선택지 중 mL 단위가 맞는지를 확인한다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "종이컵의 들이 < 500 mL", "value": "적습니다"},
        {"id": "step.2", "expr": "어림값 선택: 180 mL vs 180 L", "value": "180 mL"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "mL 단위가 들이의 어림값으로 적절한지",
            "expected": "mL",
            "actual": "mL",
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "종이컵이 500 mL 생수병보다 작은지",
            "expected": "적습니다",
            "actual": "적습니다",
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "choice",
            "description": "종이컵의 들이는 500 mL 생수병의 들이보다 (많습니다, 적습니다). 종이컵의 들이는 약 (180 mL, 180 L)입니다.",
        },
        "value": 180,
        "unit": "",
    },
}
