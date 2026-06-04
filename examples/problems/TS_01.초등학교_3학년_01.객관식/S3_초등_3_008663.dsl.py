from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, RectSlot, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008663",
        title="반지름이 3 cm인 원을 그리기 위한 컴퍼스 벌리기",
        canvas=Canvas(width=950, height=370, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q1", "slot.q2"),
            ),
            Region(
                id="region.choices",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.choice1",
                    "slot.choice2",
                    "slot.choice3",
                    "slot.answer_diagram",
                ),
            ),
            Region(
                id="region.explanation",
                role="explanation",
                flow="absolute",
                slot_ids=(),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="□ 38. 다음 중 반지름이 3 cm인 원을 그릴 수 있도록 컴퍼스를 바르게 벌린 것",
                style_role="question",
                x=12.0,
                y=32.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q2",
                prompt="",
                text="을 선택하세요.",
                style_role="question",
                x=12.0,
                y=66.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.choice1",
                prompt="",
                x=170.0,
                y=120.0,
                width=150.0,
                height=120.0,
            ),
            RectSlot(
                id="slot.choice2",
                prompt="",
                x=405.0,
                y=120.0,
                width=150.0,
                height=120.0,
            ),
            RectSlot(
                id="slot.choice3",
                prompt="",
                x=640.0,
                y=120.0,
                width=150.0,
                height=120.0,
            ),
            RectSlot(
                id="slot.answer_diagram",
                prompt="",
                x=40.0,
                y=245.0,
                width=120.0,
                height=95.0,
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=("선택형", "컴퍼스", "반지름", "눈금자"),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008663",
    "problem_type": "multiple_choice_geometry",
    "metadata": {
        "language": "ko",
        "question": "반지름이 3 cm인 원을 그릴 수 있도록 컴퍼스를 바르게 벌린 것을 고르는 문제",
        "instruction": "정답을 선택하세요.",
    },
    "domain": {
        "objects": [
            {
                "id": "obj.radius",
                "type": "length",
                "value": 3,
                "unit": "cm",
                "role": "given_radius",
            },
            {"id": "obj.compass", "type": "compass", "role": "drawing_tool"},
            {"id": "obj.ruler", "type": "ruler", "role": "measurement_tool"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.radius"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compass_spread_matches_radius"],
            },
            "plan": {
                "method": "compare_spread_to_radius",
                "description": "컴퍼스의 벌린 정도가 3 cm와 같은 그림을 찾는다.",
            },
            "execute": {
                "expected_operations": [
                    "look_at_ruler_marks",
                    "compare_compass_opening",
                    "choose_matching_picture",
                ]
            },
            "review": {"check_methods": ["length_match_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "correct_choice",
            "description": "반지름 3 cm에 맞게 컴퍼스를 벌린 그림",
        },
        "value": 1,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008663",
    "problem_type": "multiple_choice_geometry",
    "inputs": {
        "total_ticks": 0,
        "target_label": "반지름 3 cm에 맞는 컴퍼스 벌림",
        "target_ticks": 3,
        "target_count": 1,
        "unit": "cm",
    },
    "given": [{"ref": "obj.radius", "value": {"value": 3, "unit": "cm"}}],
    "target": {"ref": "answer.target", "type": "correct_choice"},
    "method": "compare_spread_to_radius",
    "plan": [
        "컴퍼스의 벌린 정도를 눈금자와 비교한다.",
        "반지름 3 cm와 같은 벌림을 찾는다.",
        "해당하는 그림을 정답으로 고른다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "r = 3 cm", "value": 3},
        {"id": "step.2", "expr": "컴퍼스 벌림과 3 cm 비교", "value": "match"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "컴퍼스의 벌림이 3 cm와 같은가",
            "expected": True,
            "actual": True,
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "correct_choice",
            "description": "반지름 3 cm에 맞게 컴퍼스를 벌린 그림",
        },
        "value": 1,
        "unit": "",
    },
}
