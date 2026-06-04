from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, RectSlot, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008621",
        title="묶이 다른 하나를 찾아 선택하세요.",
        canvas=Canvas(width=880, height=243, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.header",
                role="stem",
                flow="absolute",
                slot_ids=("slot.chk", "slot.num", "slot.stem"),
            ),
            Region(
                id="region.options",
                role="content",
                flow="absolute",
                slot_ids=("slot.box", "slot.opt1", "slot.opt2", "slot.opt3"),
            ),
            Region(id="region.answer", role="answer", flow="absolute", slot_ids=()),
            Region(
                id="region.explanation",
                role="explanation",
                flow="absolute",
                slot_ids=(),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.chk",
                prompt="",
                text="□",
                style_role="question",
                x=8.0,
                y=22.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.num",
                prompt="",
                text="91.",
                style_role="question",
                x=34.0,
                y=22.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.stem",
                prompt="",
                text="묶이 다른 하나를 찾아 선택하세요.",
                style_role="question",
                x=80.0,
                y=22.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.box", prompt="", x=94.0, y=48.0, width=777.0, height=79.0
            ),
            TextSlot(
                id="slot.opt1",
                prompt="",
                text="24 ÷ 2",
                style_role="content",
                x=185.0,
                y=94.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.opt2",
                prompt="",
                text="48 ÷ 4",
                style_role="content",
                x=433.0,
                y=94.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.opt3",
                prompt="",
                text="77 ÷ 7",
                style_role="content",
                x=680.0,
                y=94.0,
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
    "problem_id": "S3_초등_3_008621",
    "problem_type": "multiple_choice",
    "metadata": {
        "language": "ko",
        "question": "묶이 다른 하나를 찾아 선택하세요.",
        "instruction": "보기 중 묶이 다른 하나를 고르는 문제이다.",
    },
    "domain": {
        "objects": [
            {"id": "obj.opt1", "type": "division_expression", "expression": "24 ÷ 2"},
            {"id": "obj.opt2", "type": "division_expression", "expression": "48 ÷ 4"},
            {"id": "obj.opt3", "type": "division_expression", "expression": "77 ÷ 7"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.opt1", "obj.opt2", "obj.opt3"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.same_form"],
            },
            "plan": {
                "method": "compare_options",
                "description": "보기의 식들을 비교하여 다른 하나를 찾는다.",
            },
            "execute": {"expected_operations": ["compare_division_expressions"]},
            "review": {
                "check_methods": ["verify_option_selection_with_visible_answer"]
            },
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_option", "description": "묶이 다른 하나"},
        "value": 77,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008621",
    "problem_type": "multiple_choice",
    "inputs": {
        "total_ticks": 3,
        "target_label": "묶이 다른 하나",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.opt1", "value": {"expression": "24 ÷ 2"}},
        {"ref": "obj.opt2", "value": {"expression": "48 ÷ 4"}},
        {"ref": "obj.opt3", "value": {"expression": "77 ÷ 7"}},
    ],
    "target": {"ref": "answer.target", "type": "selected_option"},
    "method": "compare_options",
    "plan": ["보기의 식들을 서로 비교한다.", "같은 묶음이 아닌 하나를 찾는다."],
    "steps": [
        {
            "id": "step.1",
            "expr": "compare 24 ÷ 2, 48 ÷ 4, 77 ÷ 7",
            "value": "compare_division_expressions",
        },
        {
            "id": "step.2",
            "expr": "identify the odd one out from the visible options",
            "value": "77 ÷ 7",
        },
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "visible answer label matches selected option",
            "expected": "77 ÷ 7",
            "actual": "77 ÷ 7",
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_option", "description": "묶이 다른 하나"},
        "value": 77,
        "unit": "",
    },
}
