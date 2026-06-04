from __future__ import annotations

from modu_math.dsl import Canvas, ProblemTemplate, Region, RectSlot, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008549",
        title="500보다 큰 것 고르기",
        canvas=Canvas(width=580, height=200, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.qtext",),
            ),
            Region(
                id="region.options",
                role="diagram",
                flow="absolute",
                slot_ids=("slot.opt1.box", "slot.opt1.text", "slot.opt2.box", "slot.opt2.text"),
            ),
            Region(
                id="region.answer_explain",
                role="supporting",
                flow="absolute",
                slot_ids=( ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.qtext",
                prompt="",
                text="계산 결과가 500보다 큰 것을 선택하세요.",
                style_role="question",
                x = 20, y = 35, font_size=28,
            ),
            RectSlot(id="slot.opt1.box", prompt="", x = 35, y = 70, width=190.0, height=79.0),
            TextSlot(id="slot.opt1.text", prompt="", text="37 × 12", style_role="diagram", x = 70, y = 120, font_size=28),
            RectSlot(id="slot.opt2.box", prompt="", x = 300, y = 70, width=190.0, height=79.0),
            TextSlot(id="slot.opt2.text", prompt="", text="25 × 21", style_role="diagram", x = 345, y = 120, font_size=28),
            
            
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008549",
    "problem_type": "multiple_choice_comparison",
    "metadata": {
        "language": "ko",
        "question": "계산 결과가 500보다 큰 것을 선택하세요.",
        "instruction": "보기 중 계산 결과가 500보다 큰 식을 고른다.",
    },
    "domain": {
        "objects": [
            {"id": "obj.option1", "type": "multiplication_expression", "expression": "37 × 12"},
            {"id": "obj.option2", "type": "multiplication_expression", "expression": "25 × 21"},
            {"id": "obj.threshold", "type": "number", "value": 500},
        ],
        "relations": [],
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_option", "description": "500보다 큰 계산 결과를 만드는 보기"},
        "value": "25 × 21",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008549",
    "problem_type": "multiple_choice_comparison",
    "inputs": {"total_ticks": 2, "target_label": "500보다 큰 식", "target_ticks": 1, "target_count": 1, "unit": ""},
    "given": [
        {"ref": "obj.option1", "value": "37 × 12"},
        {"ref": "obj.option2", "value": "25 × 21"},
        {"ref": "obj.threshold", "value": 500},
    ],
    "target": {"ref": "answer.target", "type": "selected_option"},
    "method": "compute_and_compare",
    "plan": ["각 식의 곱을 계산한다.", "500과 비교한다.", "500보다 큰 식을 선택한다."],
    "steps": [
        {"id": "step.1", "expr": "37 × 12 = 444", "value": 444},
        {"id": "step.2", "expr": "25 × 21 = 525", "value": 525},
        {"id": "step.3", "expr": "444<500, 525>500", "value": "25 × 21"},
    ],
    "checks": [
        {"id": "check.1", "expr": "444 < 500", "expected": True, "actual": True, "pass": True},
        {"id": "check.2", "expr": "525 > 500", "expected": True, "actual": True, "pass": True},
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_option", "description": "500보다 큰 계산 결과를 만드는 보기"},
        "value": "25 × 21",
        "unit": "",
    },
}
