from __future__ import annotations

from modu_math.dsl import Canvas, ProblemTemplate, RectSlot, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008555",
        title="500보다 큰 계산 결과 찾기",
        canvas=Canvas(width=600, height=250, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=( "slot.question")),
            Region(
                id="region.choices",
                role="choices",
                flow="absolute",
                slot_ids=("slot.choice1_box", "slot.choice1_text", "slot.choice2_box", "slot.choice2_text"),
            ),
            Region(
                id="region.answer_explain",
                role="supporting",
                flow="absolute",
                slot_ids=("slot.answer", "slot.explain1", "slot.explain2"),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.question",
                prompt="",
                text="계산 결과가 500보다 큰 것을 선택해 보세요.",
                style_role="question",
<<<<<<< HEAD:examples/problems/TS_01.초등학교_3학년_01.객관식/S3_초등_3_008555.dsl.py
                x = 70, y = 35, font_size=28,
            ),
            RectSlot(id="slot.choice1_box", prompt="", x = 105, y = 70, width=178.0, height=76.0),
            TextSlot(id="slot.choice1_text", prompt="", text="35 × 13", style_role="choice", x = 140, y = 120, font_size=28),
            RectSlot(id="slot.choice2_box", prompt="", x = 365, y = 70, width=178.0, height=76.0),
            TextSlot(id="slot.choice2_text", prompt="", text="28 × 19", style_role="choice", x = 400, y = 120, font_size=28),
=======
                x=40.0,
                y=60.0,
                font_size=28,
            ),
            RectSlot(id="slot.choice1_box", prompt="", x=60.0, y=120.0, width=178.0, height=76.0),
            TextSlot(id="slot.choice1_text", prompt="", text="35 × 13", style_role="choice", x=100.0, y=163.0, font_size=28),
            RectSlot(id="slot.choice2_box", prompt="", x=300.0, y=120.0, width=178.0, height=76.0),
            TextSlot(id="slot.choice2_text", prompt="", text="28 × 19", style_role="choice", x=340.0, y=163.0, font_size=28),
>>>>>>> 71a328bd333ac522efc2b16e3372d00a762fe4a9:examples/problems/TS_01.초등학교_3학년_01.객관식/complete/S3_초등_3_008555.dsl.py
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008555",
    "problem_type": "multiple_choice_comparison",
    "metadata": {
        "language": "ko",
        "question": "계산 결과가 500보다 큰 것을 선택해 보세요.",
        "instruction": "두 계산 결과를 500과 비교해 큰 것을 선택한다.",
    },
    "domain": {
        "objects": [
            {"id": "obj.choice1", "type": "multiplication_expression", "expression": "35 × 13"},
            {"id": "obj.choice2", "type": "multiplication_expression", "expression": "28 × 19"},
            {"id": "obj.threshold", "type": "number", "value": 500},
        ],
        "relations": [],
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "correct_choice", "description": "500보다 큰 계산 결과"},
        "value": "28 × 19",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008555",
    "problem_type": "multiple_choice_comparison",
    "inputs": {"total_ticks": 2, "target_label": "500보다 큰 계산 결과", "target_ticks": 1, "target_count": 1, "unit": ""},
    "given": [
        {"ref": "obj.choice1", "value": "35 × 13"},
        {"ref": "obj.choice2", "value": "28 × 19"},
        {"ref": "obj.threshold", "value": 500},
    ],
    "target": {"ref": "answer.target", "type": "correct_choice"},
    "method": "compute_and_compare",
    "plan": ["각 식의 곱을 구한다.", "500과 비교한다.", "500보다 큰 식을 고른다."],
    "steps": [
        {"id": "step.1", "expr": "35 × 13 = 455", "value": 455},
        {"id": "step.2", "expr": "28 × 19 = 532", "value": 532},
        {"id": "step.3", "expr": "455<500, 532>500", "value": "28 × 19"},
    ],
    "checks": [
        {"id": "check.1", "expr": "455 < 500", "expected": True, "actual": True, "pass": True},
        {"id": "check.2", "expr": "532 > 500", "expected": True, "actual": True, "pass": True},
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "correct_choice", "description": "500보다 큰 계산 결과"},
        "value": "28 × 19",
        "unit": "",
    },
}
