"""ModuMath Problem DSL: 반직선 선택하기 (S3_초등_3_008975)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    CircleSlot,
    LineSlot,
    PathSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
)


PROBLEM_ID = "S3_초등_3_008975"
PROBLEM_TITLE = "반직선 선택하기"

ANSWER = {
    "type": "choice",
    "value": "3번 도형(반직선)",
    "unit": "",
    "answer_index": 2,
    "values": ["3번 도형(반직선)"],
    "blanks": [],
    "choices": [
        {
            "id": "slot.choice.option_0",
            "slot_id": "slot.choice.option_0",
            "text": "1번 도형(굽은 선)",
            "value": "1번 도형(굽은 선)",
        },
        {
            "id": "slot.choice.option_1",
            "slot_id": "slot.choice.option_1",
            "text": "2번 도형(꺾인 선)",
            "value": "2번 도형(꺾인 선)",
        },
        {
            "id": "slot.choice.option_2",
            "slot_id": "slot.choice.option_2",
            "text": "3번 도형(반직선)",
            "value": "3번 도형(반직선)",
        },
    ],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_2",
            "value": "3번 도형(반직선)",
        }
    ],
}

SEMANTIC_OVERRIDE = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_geometry_ray",
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
                "id": "figure.option_0",
                "type": "curved_line",
                "label": "첫 번째 도형",
                "is_straight": False,
                "extends_one_direction": True,
            },
            {
                "id": "figure.option_1",
                "type": "broken_line",
                "label": "두 번째 도형",
                "is_straight": False,
                "extends_one_direction": True,
            },
            {
                "id": "figure.option_2",
                "type": "ray",
                "label": "세 번째 도형",
                "is_straight": True,
                "extends_one_direction": True,
            },
        ],
        "relations": [
            {
                "id": "relation.classification",
                "type": "is_ray",
                "from_id": "figure.option_2",
                "to_id": "concept.ray",
            }
        ],
    },
    "answer": ANSWER,
}


def build_problem_template() -> ProblemTemplate:
    stem_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="10. 반직선을 선택하세요.",
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

    # 1번 도형: 굽은 선 (한 점에서 다른 점을 지나 휘어지며 뻗은 선)
    fig0_curve = PathSlot(
        id="slot.diagram.fig0_curve",
        prompt="",
        d="M 195 170 Q 235 95, 315 88",
        fill="none",
        stroke="#111827",
        stroke_width=1.8,
    )
    fig0_dot1 = CircleSlot(
        id="slot.diagram.fig0_dot1",
        prompt="",
        cx=215,
        cy=138,
        r=3.2,
        fill="#111827",
        stroke="#111827",
        stroke_width=1,
    )
    fig0_dot2 = CircleSlot(
        id="slot.diagram.fig0_dot2",
        prompt="",
        cx=315,
        cy=88,
        r=3.2,
        fill="#111827",
        stroke="#111827",
        stroke_width=1,
    )
    choice_0 = RectSlot(
        id="slot.choice.option_0",
        prompt="",
        x=175,
        y=76,
        width=160,
        height=110,
        fill="transparent",
        stroke="none",
        stroke_width=0,
        interaction={
            "type": "choice",
            "role": "answer",
            "choice_index": 0,
            "value": "1번 도형(굽은 선)",
            "group_id": "slot.choice.group",
            "include_in_submission": True,
        },
    )

    # 2번 도형: 꺾인 선
    fig1_path = PathSlot(
        id="slot.diagram.fig1_path",
        prompt="",
        d="M 415 95 L 432 162 L 575 135",
        fill="none",
        stroke="#111827",
        stroke_width=1.8,
    )
    fig1_dot1 = CircleSlot(
        id="slot.diagram.fig1_dot1",
        prompt="",
        cx=415,
        cy=95,
        r=3.2,
        fill="#111827",
        stroke="#111827",
        stroke_width=1,
    )
    fig1_dot2 = CircleSlot(
        id="slot.diagram.fig1_dot2",
        prompt="",
        cx=542,
        cy=141,
        r=3.2,
        fill="#111827",
        stroke="#111827",
        stroke_width=1,
    )
    choice_1 = RectSlot(
        id="slot.choice.option_1",
        prompt="",
        x=395,
        y=76,
        width=200,
        height=110,
        fill="transparent",
        stroke="none",
        stroke_width=0,
        interaction={
            "type": "choice",
            "role": "answer",
            "choice_index": 1,
            "value": "2번 도형(꺾인 선)",
            "group_id": "slot.choice.group",
            "include_in_submission": True,
        },
    )

    # 3번 도형: 반직선 (오른쪽 끝점에서 시작하여 왼쪽 점을 지나 끝없이 뻗은 곧은 선)
    fig2_line = LineSlot(
        id="slot.diagram.fig2_line",
        prompt="",
        x1=662,
        y1=94,
        x2=815,
        y2=155,
        stroke="#111827",
        stroke_width=1.8,
    )
    fig2_dot1 = CircleSlot(
        id="slot.diagram.fig2_dot1",
        prompt="",
        cx=682,
        cy=102,
        r=3.2,
        fill="#111827",
        stroke="#111827",
        stroke_width=1,
    )
    fig2_dot2 = CircleSlot(
        id="slot.diagram.fig2_dot2",
        prompt="",
        cx=815,
        cy=155,
        r=3.2,
        fill="#111827",
        stroke="#111827",
        stroke_width=1,
    )
    choice_2 = RectSlot(
        id="slot.choice.option_2",
        prompt="",
        x=645,
        y=76,
        width=190,
        height=110,
        fill="transparent",
        stroke="none",
        stroke_width=0,
        interaction={
            "type": "choice",
            "role": "answer",
            "choice_index": 2,
            "value": "3번 도형(반직선)",
            "group_id": "slot.choice.group",
            "include_in_submission": True,
        },
    )

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=886,
            height=220,
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
                slot_ids=(
                    "slot.diagram.fig0_curve",
                    "slot.diagram.fig0_dot1",
                    "slot.diagram.fig0_dot2",
                    "slot.diagram.fig1_path",
                    "slot.diagram.fig1_dot1",
                    "slot.diagram.fig1_dot2",
                    "slot.diagram.fig2_line",
                    "slot.diagram.fig2_dot1",
                    "slot.diagram.fig2_dot2",
                ),
            ),
            Region(
                id="region.choices",
                role="choices",
                flow="absolute",
                slot_ids=(
                    "slot.choice.option_0",
                    "slot.choice.option_1",
                    "slot.choice.option_2",
                ),
            ),
        ),
        slots=(
            stem_slot,
            fig0_curve,
            fig0_dot1,
            fig0_dot2,
            fig1_path,
            fig1_dot1,
            fig1_dot2,
            fig2_line,
            fig2_dot1,
            fig2_dot2,
            choice_0,
            choice_1,
            choice_2,
        ),
    )


PROBLEM_TEMPLATE = build_problem_template()

SOLVABLE = {
    "schema": "modu.solvable.v1.3",
    "problem_id": PROBLEM_ID,
    "given": [
        {"ref": "figure.option_0", "value": "curved_line"},
        {"ref": "figure.option_1", "value": "broken_line"},
        {"ref": "figure.option_2", "value": "ray"},
    ],
    "target": {"ref": "slot.choice.option_2", "type": "choice"},
    "method": "ray_classification",
    "steps": [
        {
            "id": "step.identify_ray",
            "expr": "is_straight(figure) and extends_one_direction(figure)",
            "value": "3번 도형(반직선)",
            "explanation": "한 점에서 시작하여 한쪽으로 끝없이 늘인 곧은 선을 반직선이라고 합니다. 1번은 굽은 선, 2번은 꺾인 선이므로 3번 도형이 반직선입니다.",
        }
    ],
    "answer": ANSWER,
    "diagnostics": {
        "skills": ["geometry.ray_identification"],
        "errors": {
            "1번 도형(굽은 선)": "geometry.confused_curved_with_ray",
            "2번 도형(꺾인 선)": "geometry.confused_broken_with_ray",
        },
    },
}
EDITOR_ANSWER_REVIEW = {'mode': 'canvas_select',
 'show_canvas': True,
 'status': 'pending',
 'note': '',
 'answers': [{'value': '3번 도형(반직선)', 'ref': 'slot.choice.option_2'}],
 'choices': [{'id': 'slot.choice.option_0',
              'text': '1번 도형(굽은 선)',
              'correct': False,
              'label': '1',
              'sourceRefs': ['slot.choice.option_0']},
             {'id': 'slot.choice.option_1',
              'text': '2번 도형(꺾인 선)',
              'correct': False,
              'label': '2',
              'sourceRefs': ['slot.choice.option_1']},
             {'id': 'slot.choice.option_2',
              'text': '3번 도형(반직선)',
              'correct': True,
              'label': '3',
              'sourceRefs': ['slot.choice.option_2']}]}
