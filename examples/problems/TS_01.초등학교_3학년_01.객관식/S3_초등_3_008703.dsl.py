from __future__ import annotations

from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot, compass_on_ruler_slots


ANSWER = {
    "blanks": [],
    "choices": [],
    "answer_key": [],
    "target": {"type": "correct_choice", "description": "컴퍼스를 2 cm가 되도록 벌린 그림"},
    "value": "slot.choice2",
    "unit": "",
}


def build_problem_template() -> ProblemTemplate:
    unit_width = 62.0
    choice1 = compass_on_ruler_slots(
        "slot.choice1",
        x=74.0,
        y=211.0,
        unit_width=unit_width,
        needle_mark=-0.12,
        pencil_mark=2.0,
        hinge_offset_x=73.0,
        hinge_y_offset=-130.0,
        scale=1.08,
    )
    choice2 = compass_on_ruler_slots(
        "slot.choice2",
        x=369.0,
        y=211.0,
        unit_width=unit_width,
        needle_mark=0.0,
        pencil_mark=2.15,
        hinge_offset_x=76.0,
        hinge_y_offset=-130.0,
        scale=1.08,
    )
    choice3 = compass_on_ruler_slots(
        "slot.choice3",
        x=666.0,
        y=211.0,
        unit_width=unit_width,
        needle_mark=0.0,
        pencil_mark=3.0,
        hinge_offset_x=104.0,
        hinge_y_offset=-130.0,
        scale=1.08,
    )

    return ProblemTemplate(
        id="S3_초등_3_008703",
        title="컴퍼스를 2 cm가 되도록 벌린 것 찾기",
        canvas=Canvas(width=920, height=300, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.q.text",)),
            Region(
                id="region.choices",
                role="choices",
                flow="absolute",
                slot_ids=(*(slot.id for slot in choice1), *(slot.id for slot in choice2), *(slot.id for slot in choice3)),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q.text",
                prompt="",
                text="□ 97. 컴퍼스를 2 cm가 되도록 벌린 것을 찾아 선택하세요.",
                style_role="question",
                x=10.0,
                y=31.0,
                font_size=24,
            ),
            *choice1,
            *choice2,
            *choice3,
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=("geometry", "compass", "ruler", "length"),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008703",
    "problem_type": "multiple_choice_geometry",
    "metadata": {
        "language": "ko",
        "question": "컴퍼스를 2 cm가 되도록 벌린 것을 찾아 선택하세요.",
        "instruction": "컴퍼스의 침과 연필심 사이가 자의 0 cm와 2 cm에 맞는 그림을 고른다.",
    },
    "domain": {
        "objects": [
            {"id": "obj.compass", "type": "compass"},
            {"id": "obj.ruler", "type": "ruler", "unit": "cm"},
            {"id": "obj.target_length", "type": "length", "value": 2, "unit": "cm"},
            {"id": "obj.choice.1", "type": "compass_on_ruler", "spread": 2.12, "unit": "cm"},
            {"id": "obj.choice.2", "type": "compass_on_ruler", "spread": 2.0, "unit": "cm"},
            {"id": "obj.choice.3", "type": "compass_on_ruler", "spread": 3.0, "unit": "cm"},
        ],
        "relations": [
            {
                "id": "rel.choice2.matches_target",
                "type": "matches_length",
                "from_id": "obj.choice.2",
                "to_id": "obj.target_length",
                "description": "두 번째 그림은 컴퍼스의 침이 0 cm, 연필심이 2 cm에 정확히 맞는다.",
            }
        ],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.compass", "obj.ruler", "obj.target_length"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.choice2.matches_target"],
            },
            "plan": {
                "method": "visual_match",
                "description": "각 그림에서 컴퍼스의 침과 연필심이 놓인 눈금을 비교한다.",
            },
            "execute": {"expected_operations": ["compare_ruler_marks", "select_matching_picture"]},
            "review": {"check_methods": ["침이 0 cm에 맞는지 확인", "연필심이 2 cm에 맞는지 확인"]},
        },
    },
    "answer": ANSWER,
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008703",
    "problem_type": "multiple_choice_geometry",
    "inputs": {"target_label": "2 cm", "target_length": 2, "unit": "cm", "choices": [2.12, 2.0, 3.0]},
    "given": [
        {"ref": "obj.ruler", "value": {"unit": "cm"}},
        {"ref": "obj.target_length", "value": {"value": 2, "unit": "cm"}},
    ],
    "target": {"ref": "answer.target", "type": "correct_choice"},
    "method": "visual_match",
    "plan": [
        "컴퍼스의 침이 자의 0 cm에 있는지 확인한다.",
        "연필심이 자의 2 cm에 있는 그림을 찾는다.",
        "조건에 맞는 두 번째 그림을 선택한다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "choice2 spread = 2 cm", "value": 2},
        {"id": "step.2", "expr": "target length = 2 cm", "value": 2},
    ],
    "checks": [{"id": "check.1", "expr": "choice2 spread equals target length", "expected": True, "actual": True, "pass": True}],
    "answer": ANSWER,
}
