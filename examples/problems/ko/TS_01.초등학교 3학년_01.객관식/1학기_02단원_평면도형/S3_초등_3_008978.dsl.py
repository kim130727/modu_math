"""ModuMath Problem DSL: 각인지 판별하기 (S3_초등_3_008978)"""

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


PROBLEM_ID = "S3_초등_3_008978"
PROBLEM_TITLE = "각인지 아닌지 판별하기 (13번)"

ANSWER = {
    "type": "choice",
    "value": "○",
    "unit": "",
    "answer_index": 0,
    "values": ["○"],
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
            "slot_id": "slot.choice.option_0",
            "value": "○",
        }
    ],
}

SEMANTIC_OVERRIDE = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_geometry_angle_ox",
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
                "type": "angle",
                "label": "주어진 도형",
                "shares_vertex": True,
                "is_angle": True,
            }
        ],
        "relations": [
            {
                "id": "relation.angle_check",
                "type": "is_angle",
                "from_id": "figure.target",
                "to_id": "concept.angle",
            }
        ],
    },
    "answer": ANSWER,
}


def build_problem_template() -> ProblemTemplate:
    stem_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="13. 각이면 ○, 각이 아니면 ×를 선택하세요.",
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

    # 한 점(위쪽 꼭짓점)에서 그은 두 반직선으로 이루어진 각
    angle_path = PathSlot(
        id="slot.diagram.angle",
        prompt="",
        d="M 402 162 L 502 76 L 606 162",
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
        cx=515,
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
        x=515,
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
        {"ref": "figure.target", "value": "two_rays_from_one_vertex"},
    ],
    "target": {"ref": "slot.choice.option_0", "type": "choice"},
    "method": "angle_definition_check",
    "steps": [
        {
            "id": "step.check_vertex",
            "expr": "shares_vertex(ray_left, ray_right)",
            "value": "○",
            "explanation": "한 점에서 그은 두 반직선으로 이루어져 있으므로 각입니다.",
        }
    ],
    "answer": ANSWER,
    "diagnostics": {
        "skills": ["geometry.angle_definition"],
        "errors": {
            "×": "geometry.misidentified_rotated_angle",
        },
    },
}
