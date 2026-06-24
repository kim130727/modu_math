from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot, RectSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008796",
        title="들이가 1 L보다 더 적은 그릇 선택",
        canvas=Canvas(width=790, height=382, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.header",
                role="stem",
                flow="absolute",
                slot_ids=("slot.qmark", "slot.qnum", "slot.stem"),
            ),
            Region(
                id="region.choices",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.choice.left",
                    "slot.choice.middle",
                    "slot.choice.right",
                    "slot.choice.cross",
                ),
            ),
            Region(
                id="region.answer", role="answer", flow="absolute", slot_ids=("slot.answer.cup",)
            ),
            Region(id="region.explanation", role="explanation", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.qmark",
                prompt="",
                text="□",
                style_role="question",
                x=4.0,
                y=24.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.qnum",
                prompt="",
                text="23.",
                style_role="question",
                x=26.0,
                y=24.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.stem",
                prompt="",
                text="들이가 1 L보다 더 적은 그릇을 선택하세요.",
                style_role="question",
                x=78.0,
                y=24.0,
                font_size=28,
            ),
            RectSlot(id="slot.choice.left", prompt="", x=210.0, y=55.0, width=92.0, height=94.0),
            RectSlot(
                id="slot.choice.middle", prompt="", x=455.0, y=45.0, width=132.0, height=120.0
            ),
            RectSlot(id="slot.choice.right", prompt="", x=684.0, y=86.0, width=62.0, height=62.0),
            TextSlot(
                id="slot.choice.cross",
                prompt="",
                text="X",
                style_role="diagram",
                x=505.0,
                y=128.0,
                font_size=110,
            ),
            RectSlot(id="slot.answer.cup", prompt="", x=61.0, y=195.0, width=62.0, height=62.0),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008796",
    "problem_type": "comparison_selection",
    "metadata": {
        "language": "ko",
        "question": "들이가 1 L보다 더 적은 그릇을 선택하는 문제",
        "instruction": "들이가 1 L보다 더 적은 그릇을 선택하세요.",
    },
    "domain": {
        "objects": [
            {"id": "obj.container_left", "type": "container"},
            {"id": "obj.container_middle", "type": "container"},
            {"id": "obj.cup", "type": "cup"},
            {"id": "obj.unit_1l", "type": "capacity_unit", "value": 1, "unit": "L"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.unit_1l", "obj.cup"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.select_less_than_1l"],
            },
            "plan": {
                "method": "visual_selection",
                "description": "1 L보다 작은 들이를 가진 그릇을 고른다.",
            },
            "execute": {"expected_operations": ["compare_capacity", "choose_matching_object"]},
            "review": {"check_methods": ["condition_match_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_container", "description": "1 L보다 더 적은 들이의 그릇"},
        "value": 1,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008796",
    "problem_type": "comparison_selection",
    "inputs": {
        "total_ticks": 1,
        "target_label": "1 L보다 더 적은 그릇",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "L",
    },
    "given": [
        {"ref": "obj.unit_1l", "value": {"value": 1, "unit": "L"}},
        {"ref": "obj.cup", "value": {"type": "cup"}},
    ],
    "target": {"ref": "answer.target", "type": "selected_container"},
    "method": "visual_selection",
    "plan": [
        "1 L보다 더 적은 들이를 가진 그릇을 찾는다.",
        "해설에 제시된 컵이 조건에 맞는지 확인한다.",
    ],
    "steps": [{"id": "step.1", "expr": "컵의 들이 < 1 L", "value": True}],
    "checks": [
        {
            "id": "check.1",
            "expr": "선택 대상이 1 L보다 더 적은 들이의 그릇인지 확인",
            "expected": True,
            "actual": True,
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_container", "description": "1 L보다 더 적은 들이의 그릇"},
        "value": 1,
        "unit": "",
    },
}
