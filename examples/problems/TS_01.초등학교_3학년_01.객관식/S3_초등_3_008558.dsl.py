from __future__ import annotations

from modu_math.dsl import Canvas, LineSlot, ProblemTemplate, RectSlot, Region, TextSlot


QUESTION = "바르게 계산한 것을 선택하세요."
TARGET_EXPRESSION = "50 × 60 = 3000"
TARGET_DESCRIPTION = "바르게 계산한 식"


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008558",
        title=QUESTION,
        canvas=Canvas(width=700, height=420, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.q.text",)),
        ),
        slots=(
            TextSlot(id="slot.q.text", prompt="", text=QUESTION, style_role="question", x=50, y=50, font_size=44),
            RectSlot(id="slot.b1", prompt="", x=125, y=105, width=155, height=160, fill="none"),
            RectSlot(id="slot.b2", prompt="", x=385, y=105, width=165, height=160, fill="none"),
            TextSlot(id="slot.t1", prompt="", text="5  0", style_role="diagram", x=185, y=155, font_size=44),
            TextSlot(id="slot.t2", prompt="", text="× 6  0", style_role="diagram", x=155, y=200, font_size=44),
            LineSlot(id="slot.l1", prompt="", x1=145, y1=210, x2=240, y2=210),
            TextSlot(id="slot.t3", prompt="", text="3  0  0", style_role="diagram", x=150, y=250, font_size=44),
            TextSlot(id="slot.t4", prompt="", text="5  0", style_role="diagram", x=475, y=155, font_size=44),
            TextSlot(id="slot.t5", prompt="", text="× 6  0", style_role="diagram", x=440, y=200, font_size=44),
            LineSlot(id="slot.l2", prompt="", x1=405, y1=210, x2=530, y2=210),
            TextSlot(id="slot.t6", prompt="", text="3  0  0  0", style_role="diagram", x=405, y=255, font_size=44),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=("초등", "수학", "곱셈", "계산", "선택"),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008558",
    "problem_type": "multiplication_correct_calculation_choice",
    "metadata": {
        "language": "ko",
        "question": QUESTION,
        "instruction": "두 계산 중 바르게 계산한 것을 고르세요.",
    },
    "domain": {
        "objects": [
            {"id": "obj.choice1", "type": "equation", "text": "50 × 60 = 300"},
            {"id": "obj.choice2", "type": "equation", "text": TARGET_EXPRESSION},
        ],
        "relations": [],
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_expression", "description": TARGET_DESCRIPTION},
        "value": TARGET_EXPRESSION,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008558",
    "problem_type": "multiplication_correct_calculation_choice",
    "inputs": {
        "total_ticks": 0,
        "target_label": TARGET_DESCRIPTION,
        "target_ticks": 0,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.choice1", "value": "50 × 60 = 300"},
        {"ref": "obj.choice2", "value": TARGET_EXPRESSION},
    ],
    "target": {"ref": "answer.target", "type": "selected_expression"},
    "method": "compute_and_compare",
    "plan": [
        "50 × 60의 값을 계산합니다.",
        "50 × 60 = 3000이므로 3000이라고 쓴 계산을 고릅니다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "50 × 60 = 3000", "value": 3000},
        {"id": "step.2", "expr": "바르게 계산한 식", "value": TARGET_EXPRESSION},
    ],
    "checks": [
        {"id": "check.1", "expr": "50 × 60 = 3000", "expected": True, "actual": True, "pass": True},
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_expression", "description": TARGET_DESCRIPTION},
        "value": TARGET_EXPRESSION,
        "unit": "",
    },
}
