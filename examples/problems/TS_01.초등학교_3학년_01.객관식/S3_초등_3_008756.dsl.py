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
                    "slot.bottle",
                    "slot.bottle_label1",
                    "slot.bottle_label2",
                    "slot.cup",
                    "slot.cup_label",
                    "slot.s1",
                    "slot.s2",
                    "slot.arrow",
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="53. 500 mL 생수병을 보고 들이를 어림해 보려고 합니다. 알맞은 것을 선택하세요.",
                style_role="question",
                x=18.0,
                y=28.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.bottle", prompt="", x=333.0, y=54.0, width=36.0, height=78.0
            ),
            LineSlot(
                id="slot.bottle.line1", prompt="", x1=333.0, y1=66.0, x2=369.0, y2=66.0
            ),
            LineSlot(
                id="slot.bottle.line2", prompt="", x1=333.0, y1=78.0, x2=369.0, y2=78.0
            ),
            LineSlot(
                id="slot.bottle.line3", prompt="", x1=333.0, y1=90.0, x2=369.0, y2=90.0
            ),
            LineSlot(
                id="slot.bottle.line4",
                prompt="",
                x1=333.0,
                y1=102.0,
                x2=369.0,
                y2=102.0,
            ),
            TextSlot(
                id="slot.bottle_label1",
                prompt="",
                text="생수병",
                style_role="label",
                x=314.0,
                y=165.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.bottle_label2",
                prompt="",
                text="500 mL",
                style_role="label",
                x=315.0,
                y=224.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.cup", prompt="", x=670.0, y=121.0, width=48.0, height=32.0
            ),
            PathSlot(
                id="slot.cup.detail",
                prompt="",
                d="M 670 127 C 676 114, 712 114, 718 127",
            ),
            TextSlot(
                id="slot.cup_label",
                prompt="",
                text="종이컵",
                style_role="label",
                x=654.0,
                y=165.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.s1",
                prompt="",
                text="종이컵의 들이는 500 mL 생수병의 들이보다 ( 많습니다, 적습니다 ).",
                style_role="question",
                x=68.0,
                y=298.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.arrow",
                prompt="",
                text="→",
                style_role="question",
                x=190.0,
                y=346.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.s2",
                prompt="",
                text="종이컵의 들이는 약 ( 180 mL , 180 L )입니다.",
                style_role="question",
                x=225.0,
                y=346.0,
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
