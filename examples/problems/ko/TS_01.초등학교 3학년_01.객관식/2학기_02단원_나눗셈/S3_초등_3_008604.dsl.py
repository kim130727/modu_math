from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    RectSlot,
    Region,
    SpeakerSpec,
    TextSlot,
    speaker_group_slot_ids,
    speaker_group_slots,
)


def build_problem_template() -> ProblemTemplate:
    speakers = (
        SpeakerSpec(
            key="left",
            cx=220.0,
            bubble_cy=195.0,
            head_cy=340.0,
            text="몫은 13이야.",
            name="현태",
            hair="#4b1f16",
            shirt="#D7A0D7",
            bubble_width=150.0,
            bubble_height=82.0,
            tail_y=270.0,
            name_width=80.0,
            name_height=36.0,
            name_y=480.0,
            speech_font_size=24,
        ),
        SpeakerSpec(
            key="right",
            cx=565.0,
            bubble_cy=195.0,
            head_cy=340.0,
            text="나머지는 0으로\n나누어떨어져.",
            name="은수",
            hair="#1d1714",
            shirt="#8ED7E6",
            bubble_width=175.0,
            bubble_height=94.0,
            tail_y=270.0,
            name_width=80.0,
            name_height=36.0,
            name_y=480.0,
            speech_font_size=22,
            speech_text_dy=-3,
        ),
    )
    return ProblemTemplate(
        id="S3_초등_3_008604",
        title="문제를 바르게 설명한 사람의 이름을 선택하세요.",
        canvas=Canvas(width=785.0, height=559.0, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.q1",
                    "slot.expr_box",
                    "slot.expr_text",
                    *speaker_group_slot_ids(speakers),
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="문제를 바르게 설명한 사람의 이름을 선택하세요.",
                style_role="question",
                x=24,
                y=48,
                font_size=28,
                fill="#111111",
            ),
            RectSlot(
                id="slot.expr_box",
                prompt="",
                x=300,
                y=70,
                width=186,
                height=62,
                fill="none",
                stroke="#F4A340",
                stroke_width=2,
            ),
            TextSlot(
                id="slot.expr_text",
                prompt="",
                text="67 ÷ 5",
                style_role="choice",
                x=352,
                y=113,
                font_size=28,
                fill="#111111",
            ),
            *speaker_group_slots(speakers),
        ),
    )


PROBLEM_TEMPLATE = build_problem_template()
SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008604",
    "problem_type": "division_reasoning_multiple_choice",
    "metadata": {
        "language": "ko",
        "question": "67 ÷ 5의 결과를 바르게 설명한 사람을 고르는 문제",
        "instruction": "문제를 바르게 설명한 사람의 이름을 선택하세요.",
    },
    "domain": {
        "objects": [
            {"id": "obj.dividend", "type": "number", "value": 67},
            {"id": "obj.divisor", "type": "number", "value": 5},
            {"id": "obj.speaker.left", "type": "person", "name": "현태"},
            {"id": "obj.speaker.right", "type": "person", "name": "은수"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "obj.dividend",
                    "obj.divisor",
                    "obj.speaker.left",
                    "obj.speaker.right",
                ],
                "target_ref": "answer.target",
                "condition_refs": ["rel.division", "rel.left_statement", "rel.right_statement"],
            },
            "plan": {
                "method": "division_reasoning",
                "description": "나눗셈의 몫과 나머지 설명이 맞는지 비교한다.",
            },
            "execute": {
                "expected_operations": [
                    "interpret_quotient_statement",
                    "interpret_remainder_statement",
                    "compare_with_division_result",
                ]
            },
            "review": {"check_methods": ["statement_match_check", "division_consistency_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "person_name", "description": "문제를 바르게 설명한 사람의 이름"},
        "value": "현태",
        "unit": "",
    },
}
SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008604",
    "problem_type": "division_reasoning_multiple_choice",
    "inputs": {
        "total_ticks": 0,
        "target_label": "문제를 바르게 설명한 사람의 이름",
        "target_ticks": 0,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.dividend", "value": 67},
        {"ref": "obj.divisor", "value": 5},
        {"ref": "obj.speaker.left", "value": "현태"},
        {"ref": "obj.speaker.right", "value": "은수"},
    ],
    "target": {"ref": "answer.target", "type": "person_name"},
    "method": "division_reasoning",
    "plan": [
        "나눗셈의 몫과 나머지 설명을 비교한다.",
        "문장 내용이 67 ÷ 5의 결과와 맞는지 확인한다.",
    ],
    "steps": [
        {
            "id": "step.1",
            "expr": "67 ÷ 5의 몫과 나머지를 해설 표기와 비교",
            "value": {
                "quotient_statement": "몫은 13이야.",
                "remainder_statement": "나머지는 0으로 나누어떨어져.",
            },
        },
        {
            "id": "step.2",
            "expr": "실제 계산 결과와 비교",
            "value": {"quotient": 13, "remainder": 2},
        },
        {"id": "step.3", "expr": "문제를 바르게 설명한 사람 선택", "value": "현태"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "몫 설명이 13인지 확인",
            "expected": True,
            "actual": True,
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "나머지 설명이 0이 아닌지 확인",
            "expected": True,
            "actual": True,
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "person_name", "description": "문제를 바르게 설명한 사람의 이름"},
        "value": "현태",
        "unit": "",
    },
}
