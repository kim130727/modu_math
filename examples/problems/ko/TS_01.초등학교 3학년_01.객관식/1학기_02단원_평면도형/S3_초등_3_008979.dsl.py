"""ModuMath Problem DSL: 직각인지 판별하기 (S3_초등_3_008979)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    CircleSlot,
    PathSlot,
    ProblemTemplate,
    Region,
    TextBoxSlot,
    TextSlot,
)


PROBLEM_ID = "S3_초등_3_008979"
PROBLEM_TITLE = "직각인지 아닌지 판별하기 (14번)"

ANSWER = {
    "type": "choice",
    "value": "×",
    "unit": "",
    "answer_index": 1,
    "values": ["×"],
    "blanks": [],
    "choices": [
        {
            "id": "slot.choice.option_0",
            "slot_id": "slot.choice.option_0",
            "text": "○",
            "value": "○",
        },
        {
            "id": "slot.choice.option_1",
            "slot_id": "slot.choice.option_1",
            "text": "×",
            "value": "×",
        },
    ],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_1",
            "value": "×",
        }
    ],
}

SEMANTIC_OVERRIDE = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_geometry_right_angle_ox",
    "metadata": {
        "grade": 3,
        "semester": 1,
        "subject": "수학",
        "chapter": "02단원_평면도형",
        "language": "ko-KR",
    },
    "domain": {
        "objects": [
            {
                "id": "figure.target",
                "type": "acute_angle",
                "label": "주어진 각",
                "is_right_angle": False,
            }
        ],
        "relations": [
            {
                "id": "relation.right_angle_check",
                "type": "is_not_right_angle",
                "from_id": "figure.target",
                "to_id": "concept.right_angle",
            }
        ],
    },
    "answer": ANSWER,
}


def build_problem_template() -> ProblemTemplate:
    stem_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="14. 직각이면 ○, 직각이 아니면 ×를 선택하세요.",
        x=32,
        y=22,
        width=820,
        height=44,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="left",
        valign="top",
        line_height=1.5,
    )

    # 직각보다 작은 예각
    angle_path = PathSlot(
        id="slot.diagram.angle",
        prompt="",
        d="M 495 76 L 380 156 L 540 156",
        fill="none",
        stroke="#111827",
        stroke_width=1.8,
    )

    # 선택지 ○, ×
    circle_o = CircleSlot(
        id="slot.choice.circle_0",
        prompt="",
        cx=42,
        cy=192,
        r=12,
        fill="#ffffff",
        stroke="#2563eb",
        stroke_width=1.5,
    )
    choice_o = TextSlot(
        id="slot.choice.option_0",
        prompt="",
        text="○",
        x=42,
        y=192,
        font_size=18,
        font_family='"Noto Sans KR", sans-serif',
        fill="#2563eb",
        align="center",
        interaction={
            "type": "choice",
            "role": "answer",
            "choice_index": 0,
            "value": "○",
            "group_id": "slot.choice.group",
            "include_in_submission": True,
        },
    )

    circle_x = CircleSlot(
        id="slot.choice.circle_1",
        prompt="",
        cx=465,
        cy=192,
        r=12,
        fill="#ffffff",
        stroke="#2563eb",
        stroke_width=1.5,
    )
    choice_x = TextSlot(
        id="slot.choice.option_1",
        prompt="",
        text="×",
        x=465,
        y=192,
        font_size=18,
        font_family='"Noto Sans KR", sans-serif',
        fill="#2563eb",
        align="center",
        interaction={
            "type": "choice",
            "role": "answer",
            "choice_index": 1,
            "value": "×",
            "group_id": "slot.choice.group",
            "include_in_submission": True,
        },
    )

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=886,
            height=230,
            coordinate_mode="logical",
        ),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.stem.question",),
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=("slot.diagram.angle",),
            ),
            Region(
                id="region.choices",
                role="choices",
                flow="absolute",
                slot_ids=(
                    "slot.choice.circle_0",
                    "slot.choice.option_0",
                    "slot.choice.circle_1",
                    "slot.choice.option_1",
                ),
            ),
        ),
        slots=(
            stem_slot,
            angle_path,
            circle_o,
            choice_o,
            circle_x,
            choice_x,
        ),
    )


PROBLEM_TEMPLATE = build_problem_template()

SOLVABLE = {
    "schema": "modu.solvable.v1.3",
    "problem_id": PROBLEM_ID,
    "given": [
        {"ref": "figure.target", "value": "acute_angle"},
    ],
    "target": {"ref": "slot.choice.option_1", "type": "choice"},
    "method": "right_angle_check",
    "steps": [
        {
            "id": "step.compare_with_right_angle",
            "expr": "angle < 90_deg",
            "value": "×",
            "explanation": "직각 삼각자의 직각 부분을 대어 보았을 때 꼭 맞게 겹쳐지지 않고 더 좁으므로 직각이 아닙니다.",
        }
    ],
    "answer": ANSWER,
    "diagnostics": {
        "skills": ["geometry.right_angle_identification"],
        "errors": {
            "○": "geometry.confused_acute_with_right_angle",
        },
    },
}
