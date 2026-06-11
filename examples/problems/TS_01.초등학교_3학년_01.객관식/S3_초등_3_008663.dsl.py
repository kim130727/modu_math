from __future__ import annotations

from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot, compass_on_ruler_slots


ANSWER = {
    "blanks": [],
    "choices": [],
    "answer_key": [],
    "target": {"type": "correct_choice", "description": "반지름 3 cm만큼 컴퍼스를 벌린 그림"},
    "value": 3,
    "unit": "",
}


def build_problem_template() -> ProblemTemplate:
    unit_width = 31.0
    choice1 = compass_on_ruler_slots(
        "slot.choice1",
        x=196.0,
        y=185.0,
        unit_width=unit_width,
        needle_mark=0.0,
        pencil_mark=1.0,
        hinge_offset_x=18.0,
        hinge_y_offset=-100.0,
        scale=0.92,
    )
    choice2 = compass_on_ruler_slots(
        "slot.choice2",
        x=416.0,
        y=185.0,
        unit_width=unit_width,
        needle_mark=0.0,
        pencil_mark=2.0,
        hinge_offset_x=33.0,
        hinge_y_offset=-100.0,
        scale=0.92,
    )
    choice3 = compass_on_ruler_slots(
        "slot.choice3",
        x=638.0,
        y=185.0,
        unit_width=unit_width,
        needle_mark=0.0,
        pencil_mark=3.0,
        hinge_offset_x=48.0,
        hinge_y_offset=-100.0,
        scale=0.92,
    )

    return ProblemTemplate(
        id="S3_초등_3_008663",
        title="반지름이 3 cm인 원을 그릴 수 있도록 컴퍼스를 벌린 것",
        canvas=Canvas(width=920, height=380, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.q.text1", "slot.q.text2")),
            Region(
                id="region.choices",
                role="choices",
                flow="absolute",
                slot_ids=(*(slot.id for slot in choice1), *(slot.id for slot in choice2), *(slot.id for slot in choice3)),
            ),
            Region(
                id="region.answer",
                role="answer",
                flow="absolute",
                slot_ids=(*(slot.id for slot in answer_diagram),  ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q.text1",
                prompt="",
                text = '다음 중 반지름이 3 cm인 원을 그릴 수 있도록 컴퍼스를 바르게 벌린 것', style_role="question",
                x = 35, y = 30, font_size = 25),
            TextSlot(id="slot.q.text2", prompt="", text="을 선택하세요.", style_role="question", x=36.0, y=66.0, font_size=25),
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
    "problem_id": "S3_초등_3_008663",
    "problem_type": "multiple_choice_geometry",
    "metadata": {
        "language": "ko",
        "question": "반지름이 3 cm인 원을 그릴 수 있도록 컴퍼스를 바르게 벌린 것을 고르는 문제",
        "instruction": "컴퍼스를 3 cm만큼 벌린 보기를 선택한다.",
    },
    "domain": {
        "objects": [
            {"id": "obj.radius", "type": "length", "value": 3, "unit": "cm", "role": "given_radius"},
            {"id": "obj.choice.1", "type": "compass_on_ruler", "spread": 1, "unit": "cm"},
            {"id": "obj.choice.2", "type": "compass_on_ruler", "spread": 2, "unit": "cm"},
            {"id": "obj.choice.3", "type": "compass_on_ruler", "spread": 3, "unit": "cm"},
        ],
        "relations": [
            {
                "id": "rel.choice3.matches_radius",
                "type": "matches_length",
                "from_id": "obj.choice.3",
                "to_id": "obj.radius",
                "description": "세 번째 그림은 컴퍼스의 폭이 3 cm이다.",
            }
        ],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.radius", "obj.choice.1", "obj.choice.2", "obj.choice.3"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.choice3.matches_radius"],
            },
            "plan": {"method": "compare_spread_to_radius", "description": "각 그림의 컴퍼스 폭을 자의 눈금과 비교한다."},
            "execute": {"expected_operations": ["read_ruler_marks", "compare_compass_spread", "choose_matching_picture"]},
            "review": {"check_methods": ["length_match_check"]},
        },
    },
    "answer": ANSWER,
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008663",
    "problem_type": "multiple_choice_geometry",
    "inputs": {
        "target_label": "반지름 3 cm에 맞는 컴퍼스 폭",
        "target_count": 1,
        "unit": "cm",
    },
    "given": [
        {"ref": "obj.radius", "value": {"value": 3, "unit": "cm"}},
        {"ref": "obj.choice.1", "value": {"spread": 1, "unit": "cm"}},
        {"ref": "obj.choice.2", "value": {"spread": 2, "unit": "cm"}},
        {"ref": "obj.choice.3", "value": {"spread": 3, "unit": "cm"}},
    ],
    "target": {"ref": "answer.target", "type": "correct_choice"},
    "method": "compare_spread_to_radius",
    "plan": [
        "왼쪽부터 컴퍼스의 폭을 자의 눈금으로 확인한다.",
        "각각 1 cm, 2 cm, 3 cm임을 비교한다.",
        "반지름 3 cm와 같은 세 번째 그림을 고른다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "첫 번째 컴퍼스 폭 = 1 cm", "value": 1},
        {"id": "step.2", "expr": "두 번째 컴퍼스 폭 = 2 cm", "value": 2},
        {"id": "step.3", "expr": "세 번째 컴퍼스 폭 = 3 cm", "value": 3},
    ],
    "checks": [{"id": "check.1", "expr": "정답 보기의 컴퍼스 폭이 3 cm인가", "expected": 3, "actual": 3, "pass": True}],
    "answer": ANSWER,
}
