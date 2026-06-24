from __future__ import annotations
from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    Region,
    TextSlot,
    RectSlot,
    CircleSlot,
    LineSlot,
    PathSlot,
)


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008832",
        title="보온병의 들이 비교",
        canvas=Canvas(width=870, height=486, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.q1",
                    "slot.bubble.left.l1",
                    "slot.bubble.left.l2",
                    "slot.bubble.left.l3",
                    "slot.bubble.right.l1",
                    "slot.bubble.right.l2",
                    "slot.bubble.right.l3",
                    "slot.name.left",
                    "slot.name.right",
                ),
            ),
            Region(id="region.diagram", role="diagram", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="69. 보온병의 들이를 더 적절히 어린 친구는 누구인지 선택해 보세요.",
                style_role="question",
                x=18.0,
                y=28.0,
                font_size=28,
            ),
            RectSlot(id="slot.name.left.box", prompt="", x=250.0, y=301.0, width=68.0, height=38.0),
            RectSlot(
                id="slot.name.right.box", prompt="", x=676.0, y=301.0, width=68.0, height=38.0
            ),
            TextSlot(
                id="slot.bubble.left.l1",
                prompt="",
                text="보온병에 200 mL 우유갑으로",
                style_role="text",
                x=122.0,
                y=76.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.bubble.left.l2",
                prompt="",
                text="4번쯤 들어갈 것 같아.",
                style_role="text",
                x=138.0,
                y=112.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.bubble.left.l3",
                prompt="",
                text="들이는 약 600 mL야.",
                style_role="text",
                x=145.0,
                y=148.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.bubble.right.l1",
                prompt="",
                text="보온병은 1 L 우유갑과",
                style_role="text",
                x=545.0,
                y=76.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.bubble.right.l2",
                prompt="",
                text="들이가 비슷할 것 같아.",
                style_role="text",
                x=536.0,
                y=112.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.bubble.right.l3",
                prompt="",
                text="들이는 약 1000 mL야.",
                style_role="text",
                x=541.0,
                y=148.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.name.left",
                prompt="",
                text="나래",
                style_role="label",
                x=257.0,
                y=329.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.name.right",
                prompt="",
                text="재석",
                style_role="label",
                x=691.0,
                y=329.0,
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
    "problem_id": "S3_초등_3_008832",
    "problem_type": "compare_capacity_choice",
    "metadata": {
        "language": "ko",
        "question": "보온병의 들이를 더 적절히 설명한 어린 친구를 고르는 문제",
        "instruction": "누가 더 적절히 말했는지 선택하시오.",
    },
    "domain": {
        "objects": [
            {"id": "obj.thermos", "type": "container", "name": "보온병"},
            {
                "id": "obj.narae.statement",
                "type": "claim",
                "speaker": "나래",
                "reference_amount": "200 mL 우유갑 4번쯤",
                "stated_capacity": "약 600 mL",
            },
            {
                "id": "obj.jaesuk.statement",
                "type": "claim",
                "speaker": "재석",
                "reference_amount": "1 L 우유갑",
                "stated_capacity": "약 1000 mL",
            },
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.narae.statement", "obj.jaesuk.statement"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare.capacity"],
            },
            "plan": {
                "method": "compare_descriptions",
                "description": "두 설명 중 보온병의 들이를 더 적절히 나타내는 쪽을 고른다.",
            },
            "execute": {
                "expected_operations": ["compare_reference_amounts", "judge_appropriateness"]
            },
            "review": {"check_methods": ["statement_match_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "selected_student",
            "description": "보온병의 들이를 더 적절히 말한 어린 친구",
        },
        "value": 1,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008832",
    "problem_type": "compare_capacity_choice",
    "inputs": {
        "total_ticks": 0,
        "target_label": "선택된 어린 친구",
        "target_ticks": 0,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {
            "ref": "obj.narae.statement",
            "value": {"reference_amount": "200 mL 우유갑 4번쯤", "stated_capacity": "약 600 mL"},
        },
        {
            "ref": "obj.jaesuk.statement",
            "value": {"reference_amount": "1 L 우유갑", "stated_capacity": "약 1000 mL"},
        },
    ],
    "target": {"ref": "answer.target", "type": "selected_student"},
    "method": "compare_descriptions",
    "plan": [
        "두 학생의 설명이 보온병의 들이를 더 적절하게 나타내는지 비교한다.",
        "보이는 정답 표기를 기준으로 선택 결과를 기록한다.",
    ],
    "steps": [{"id": "step.1", "expr": "보이는 정답 표기 확인", "value": "재석"}],
    "checks": [
        {
            "id": "check.1",
            "expr": "정답 표기와 선택 결과가 일치하는가",
            "expected": "재석",
            "actual": "재석",
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "selected_student",
            "description": "보온병의 들이를 더 적절히 말한 어린 친구",
        },
        "value": 1,
        "unit": "",
    },
}
