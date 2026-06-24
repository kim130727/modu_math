from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, RectSlot, TextSlot, LineSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008967",
        title="바르게 계산한 것을 선택하세요",
        canvas=Canvas(width=478.0, height=432.0, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.q1",)),
            Region(
                id="region.options",
                role="body",
                flow="absolute",
                slot_ids=(
                    "slot.opt.left.box",
                    "slot.opt.left.a",
                    "slot.opt.left.b",
                    "slot.opt.left.c",
                    "slot.opt.left.line",
                    "slot.opt.right.box",
                    "slot.opt.right.a",
                    "slot.opt.right.b",
                    "slot.opt.right.c",
                    "slot.opt.right.line",
                ),
            ),
            Region(
                id="region.answer", role="body", flow="absolute", slot_ids=("slot.answer.line",)
            ),
            Region(
                id="region.explanation",
                role="body",
                flow="absolute",
                slot_ids=("slot.explain.left.line", "slot.explain.right.line"),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="1. 바르게 계산한 것을 선택하세요.",
                style_role="question",
                x=12.0,
                y=22.0,
                font_size=28,
            ),
            RectSlot(id="slot.opt.left.box", prompt="", x=116.0, y=29.0, width=131.0, height=75.0),
            TextSlot(
                id="slot.opt.left.a",
                prompt="",
                text="1 8 8",
                style_role="body",
                x=150.0,
                y=50.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.opt.left.b",
                prompt="",
                text="+ 4 5 6",
                style_role="body",
                x=142.0,
                y=78.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.opt.left.c",
                prompt="",
                text="5 3 4",
                style_role="body",
                x=149.0,
                y=105.0,
                font_size=28,
            ),
            LineSlot(id="slot.opt.left.line", prompt="", x1=140.0, y1=92.0, x2=206.0, y2=92.0),
            RectSlot(id="slot.opt.right.box", prompt="", x=333.0, y=29.0, width=131.0, height=75.0),
            TextSlot(
                id="slot.opt.right.a",
                prompt="",
                text="2 6 5",
                style_role="body",
                x=367.0,
                y=50.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.opt.right.b",
                prompt="",
                text="+ 3 4 7",
                style_role="body",
                x=359.0,
                y=78.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.opt.right.c",
                prompt="",
                text="6 1 2",
                style_role="body",
                x=366.0,
                y=105.0,
                font_size=28,
            ),
            LineSlot(id="slot.opt.right.line", prompt="", x1=357.0, y1=92.0, x2=423.0, y2=92.0),
            LineSlot(id="slot.answer.line", prompt="", x1=32.0, y1=249.0, x2=98.0, y2=249.0),
            LineSlot(id="slot.explain.left.line", prompt="", x1=27.0, y1=399.0, x2=93.0, y2=399.0),
            LineSlot(
                id="slot.explain.right.line", prompt="", x1=109.0, y1=399.0, x2=175.0, y2=399.0
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008967",
    "problem_type": "계산판단",
    "metadata": {
        "language": "ko",
        "question": "바르게 계산한 것을 선택하세요.",
        "instruction": "보기 중 바르게 계산한 것을 고르는 문제",
    },
    "domain": {
        "objects": [
            {
                "id": "obj.option.left",
                "type": "vertical_addition",
                "expression": "188 + 456",
                "result": 534,
            },
            {
                "id": "obj.option.right",
                "type": "vertical_addition",
                "expression": "265 + 347",
                "result": 612,
            },
            {
                "id": "obj.answer.display",
                "type": "vertical_addition",
                "expression": "265 + 347",
                "result": 612,
            },
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.option.left", "obj.option.right"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare_options"],
            },
            "plan": {
                "method": "compare_vertical_addition_results",
                "description": "각 보기의 덧셈 결과가 식과 맞는지 확인한다.",
            },
            "execute": {
                "expected_operations": ["check_addition_consistency", "select_matching_option"]
            },
            "review": {"check_methods": ["result_match_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "correct_option", "description": "바르게 계산한 보기"},
        "value": 2,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008967",
    "problem_type": "계산판단",
    "inputs": {
        "total_ticks": 0,
        "target_label": "바르게 계산한 보기",
        "target_ticks": 0,
        "target_count": 2,
        "unit": "",
    },
    "given": [
        {"ref": "obj.option.left", "value": {"expression": "188 + 456", "result": 534}},
        {"ref": "obj.option.right", "value": {"expression": "265 + 347", "result": 612}},
    ],
    "target": {"ref": "answer.target", "type": "correct_option"},
    "method": "compare_vertical_addition_results",
    "plan": ["각 보기의 덧셈 결과가 식과 맞는지 확인한다."],
    "steps": [
        {"id": "step.1", "expr": "188 + 456", "value": 644},
        {"id": "step.2", "expr": "265 + 347", "value": 612},
        {
            "id": "step.3",
            "expr": "보기의 표시값과 계산값을 비교한다.",
            "value": "left_mismatch_right_match",
        },
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "188 + 456 == 534",
            "expected": True,
            "actual": False,
            "pass": False,
        },
        {
            "id": "check.2",
            "expr": "265 + 347 == 612",
            "expected": True,
            "actual": True,
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "correct_option", "description": "바르게 계산한 보기"},
        "value": 2,
        "unit": "",
    },
}
