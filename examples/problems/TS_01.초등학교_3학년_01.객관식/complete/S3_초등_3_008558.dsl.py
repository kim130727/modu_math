from __future__ import annotations

from modu_math.dsl import Canvas, LineSlot, ProblemTemplate, RectSlot, Region, TextSlot


PROBLEM_ID = "S3_초등_3_008558"
QUESTION_TEXT = "바르게 계산한 것을 선택하세요."
ANSWER_EXPR = "50 × 60 = 3000"
TARGET_LABEL = "바르게 계산한 것"


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id=PROBLEM_ID,
        title=QUESTION_TEXT,
        canvas=Canvas(width=900, height=420, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.q.text",
                    "slot.b1",
                    "slot.b2",
                    "slot.t1",
                    "slot.t2",
                    "slot.l1",
                    "slot.t3",
                    "slot.t4",
                    "slot.t5",
                    "slot.l2",
                    "slot.t6",
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q.text",
                prompt="",
                text=QUESTION_TEXT,
                style_role="question",
                x=60,
                y=55,
                font_size=45,
            ),
            RectSlot(
                id="slot.b1",
                prompt="",
                x=120,
                y=90,
                width=180,
                height=180,
                fill="none",
                stroke="#8E44AD",
                stroke_width=2.0,
            ),
            RectSlot(
                id="slot.b2",
                prompt="",
                x=405,
                y=90,
                width=170,
                height=180,
                fill="none",
                stroke="#8E44AD",
                stroke_width=2.0,
            ),
            TextSlot(id="slot.t1", prompt="", text="5  0", style_role="diagram", x=200, y=140, font_size=45),
            TextSlot(id="slot.t2", prompt="", text="× 6  0", style_role="diagram", x=145, y=190, font_size=44),
            LineSlot(id="slot.l1", prompt="", x1=148, y1=210, x2=270, y2=210),
            TextSlot(id="slot.t3", prompt="", text="3  0  0", style_role="diagram", x=165, y=250, font_size=45),
            TextSlot(id="slot.t4", prompt="", text="5  0", style_role="diagram", x=500, y=140, font_size=44),
            TextSlot(id="slot.t5", prompt="", text="× 6  0", style_role="diagram", x=445, y=195, font_size=44),
            LineSlot(id="slot.l2", prompt="", x1=435, y1=205, x2=560, y2=205),
            TextSlot(id="slot.t6", prompt="", text="3  0  0  0", style_role="diagram", x=430, y=250, font_size=44),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiplication_place_value_choice",
    "metadata": {
        "language": "ko",
        "question": QUESTION_TEXT,
        "instruction": "보기에서 바르게 계산한 것을 고르세요.",
    },
    "domain": {
        "objects": [{"id": "obj.target", "type": "expression", "text": ANSWER_EXPR}],
        "relations": [],
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_expression", "description": TARGET_LABEL},
        "value": ANSWER_EXPR,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": PROBLEM_ID,
    "problem_type": "multiplication_place_value_choice",
    "inputs": {"total_ticks": 0, "target_label": TARGET_LABEL, "target_ticks": 0, "target_count": 1, "unit": ""},
    "given": [{"ref": "obj.target", "value": ANSWER_EXPR}],
    "target": {"ref": "answer.target", "type": "selected_expression"},
    "method": "multiplication_by_tens",
    "plan": ["50 × 60의 계산 원리를 확인한다.", "결과가 3000인 보기를 고른다."],
    "steps": [{"id": "step.1", "expr": "50 × 60", "value": "3000"}],
    "checks": [{"id": "check.1", "expr": "5 × 6 = 30, 0을 2개 붙임", "expected": "3000", "actual": "3000", "pass": True}],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_expression", "description": TARGET_LABEL},
        "value": ANSWER_EXPR,
        "unit": "",
    },
}
