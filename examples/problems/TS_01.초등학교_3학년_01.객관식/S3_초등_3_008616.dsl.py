from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, RectSlot, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008616",
        title="문제를 바르게 설명한 사람 찾기",
        canvas=Canvas(width=872, height=650, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.q.box",
                    "slot.q.num",
                    "slot.q.text",
                    "slot.eq.box",
                    "slot.sp1",
                    "slot.sp2",
                    "slot.sp3",
                    "slot.balloon.left",
                    "slot.balloon.mid",
                    "slot.balloon.right",
                    "slot.name.left",
                    "slot.name.mid",
                    "slot.name.right",
                ),
            ),
        ),
        slots=(
            RectSlot(
                id="slot.q.box", prompt="", x=18.0, y=14.0, width=14.0, height=14.0
            ),
            TextSlot(
                id="slot.q.num",
                prompt="",
                text="86.",
                style_role="question",
                x=42.0,
                y=28.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q.text",
                prompt="",
                text="문제를 바르게 설명한 사람이 누구인지 찾아 선택하세요.",
                style_role="question",
                x=96.0,
                y=28.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.eq.box", prompt="", x=308.0, y=44.0, width=370.0, height=78.0
            ),
            RectSlot(
                id="slot.sp1", prompt="", x=489.0, y=72.0, width=24.0, height=24.0
            ),
            TextSlot(
                id="slot.sp2",
                prompt="",
                text="···",
                style_role="math",
                x=518.0,
                y=92.0,
                font_size=30,
            ),
            RectSlot(
                id="slot.sp3", prompt="", x=562.0, y=72.0, width=24.0, height=24.0
            ),
            TextSlot(
                id="slot.balloon.left",
                prompt="",
                text="묶은\n10보다 작아.",
                style_role="speech",
                x=186.0,
                y=214.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.balloon.mid",
                prompt="",
                text="나머지는 0으로\n나누어떨어져.",
                style_role="speech",
                x=434.0,
                y=214.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.balloon.right",
                prompt="",
                text="나머지는\n8보다 작아.",
                style_role="speech",
                x=674.0,
                y=214.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.name.left",
                prompt="",
                text="근희",
                style_role="label",
                x=228.0,
                y=402.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.name.mid",
                prompt="",
                text="영표",
                style_role="label",
                x=474.0,
                y=402.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.name.right",
                prompt="",
                text="슬기",
                style_role="label",
                x=710.0,
                y=402.0,
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
    "problem_id": "S3_초등_3_008616",
    "problem_type": "division_reasoning",
    "metadata": {
        "language": "ko",
        "question": "문제를 바르게 설명한 사람이 누구인지 찾아 선택하는 문제",
        "instruction": "문제를 바르게 설명한 사람이 누구인지 찾아 선택하세요.",
    },
    "domain": {
        "objects": [
            {"id": "obj.dividend", "type": "number", "value": 99},
            {"id": "obj.divisor", "type": "number", "value": 8},
            {
                "id": "obj.claim.left",
                "type": "student_claim",
                "speaker": "근희",
                "statement_type": "quotient_comparison",
            },
            {
                "id": "obj.claim.mid",
                "type": "student_claim",
                "speaker": "영표",
                "statement_type": "remainder_divisibility",
            },
            {
                "id": "obj.claim.right",
                "type": "student_claim",
                "speaker": "슬기",
                "statement_type": "remainder_less_than_divisor",
            },
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "obj.dividend",
                    "obj.divisor",
                    "obj.claim.left",
                    "obj.claim.mid",
                    "obj.claim.right",
                ],
                "target_ref": "answer.target",
                "condition_refs": ["rel.division_result", "rel.correct_speaker"],
            },
            "plan": {
                "method": "division_with_remainder_check",
                "description": "나눗셈의 몫과 나머지를 확인한 뒤 각 설명이 맞는지 비교한다.",
            },
            "execute": {
                "expected_operations": [
                    "compute_quotient",
                    "compute_remainder",
                    "compare_statement_truths",
                ]
            },
            "review": {
                "check_methods": [
                    "remainder_less_than_divisor",
                    "division_identity_check",
                ]
            },
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "correct_speaker",
            "description": "문제를 바르게 설명한 사람",
        },
        "value": "슬기",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008616",
    "problem_type": "division_reasoning",
    "inputs": {
        "total_ticks": 1,
        "target_label": "문제를 바르게 설명한 사람",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.dividend", "value": 99},
        {"ref": "obj.divisor", "value": 8},
        {"ref": "obj.claim.left", "value": "묶은 10보다 작아."},
        {"ref": "obj.claim.mid", "value": "나머지는 0으로 나누어떨어져."},
        {"ref": "obj.claim.right", "value": "나머지는 8보다 작아."},
    ],
    "target": {"ref": "answer.target", "type": "correct_speaker"},
    "method": "division_with_remainder_check",
    "plan": [
        "99를 8로 나눈 몫과 나머지를 확인한다.",
        "각 학생의 설명이 몫 또는 나머지의 성질과 맞는지 비교한다.",
    ],
    "steps": [
        {
            "id": "step.1",
            "expr": "99 ÷ 8의 몫과 나머지를 구한다",
            "value": {"quotient": 12, "remainder": 3},
        },
        {"id": "step.2", "expr": "나머지 3은 8보다 작은지 확인한다", "value": True},
        {"id": "step.3", "expr": "나머지가 0인지 확인한다", "value": False},
        {"id": "step.4", "expr": "몫이 10보다 작은지 확인한다", "value": False},
        {"id": "step.5", "expr": "바른 설명을 한 사람을 고른다", "value": "슬기"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "99 = 8 × 12 + 3",
            "expected": True,
            "actual": True,
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "3 < 8",
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
            "type": "correct_speaker",
            "description": "문제를 바르게 설명한 사람",
        },
        "value": "슬기",
        "unit": "",
    },
}
