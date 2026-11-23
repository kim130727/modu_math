"""ModuMath Problem DSL: 직선 선택하기 (S3_초등_3_008976)"""

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


PROBLEM_ID = "S3_초등_3_008976"
PROBLEM_TITLE = "직선 선택하기"

ANSWER = {
    "type": "choice",
    "value": "3번 도형(직선)",
    "unit": "",
    "answer_index": 2,
    "values": ["3번 도형(직선)"],
    "blanks": [],
    "choices": [
        {
            "id": "slot.choice.option_0",
            "slot_id": "slot.choice.option_0",
            "text": "1번 도형(선분)",
            "value": "1번 도형(선분)",
        },
        {
            "id": "slot.choice.option_1",
            "slot_id": "slot.choice.option_1",
            "text": "2번 도형(굽은 선)",
            "value": "2번 도형(굽은 선)",
        },
        {
            "id": "slot.choice.option_2",
            "slot_id": "slot.choice.option_2",
            "text": "3번 도형(직선)",
            "value": "3번 도형(직선)",
        },
    ],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_2",
            "value": "3번 도형(직선)",
        }
    ],
}

SEMANTIC_OVERRIDE = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_geometry_line",
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
                "type": "line_segment",
                "label": "첫 번째 도형",
                "is_straight": True,
                "extends_both_directions": False,
            },
            {
                "id": "figure.option_1",
                "type": "curved_line",
                "label": "두 번째 도형",
                "is_straight": False,
                "extends_both_directions": True,
            },
            {
                "id": "figure.option_2",
                "type": "straight_line",
                "label": "세 번째 도형",
                "is_straight": True,
                "extends_both_directions": True,
            },
        ],
        "relations": [
            {
                "id": "relation.classification",
                "type": "is_straight_line",
                "from_id": "figure.option_2",
                "to_id": "concept.straight_line",
            }
        ],
    },
    "answer": ANSWER,
}


def build_problem_template() -> ProblemTemplate:
    stem_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="11. 직선을 선택하세요.",
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

    # 1번 도형: 선분 (두 점 사이를 잇는 곧은 선)
    fig0_line = LineSlot(
        id="slot.diagram.fig0_line",
        prompt="",
        x1=180,
        y1=114,
        x2=325,
        y2=114,
        stroke="#111827",
        stroke_width=1.8,
    )
    fig0_dot1 = CircleSlot(
        id="slot.diagram.fig0_dot1",
        prompt="",
        cx=180,
        cy=114,
        r=3.2,
        fill="#111827",
        stroke="#111827",
        stroke_width=1,
    )
    fig0_dot2 = CircleSlot(
        id="slot.diagram.fig0_dot2",
        prompt="",
        cx=325,
        cy=114,
        r=3.2,
        fill="#111827",
        stroke="#111827",
        stroke_width=1,
    )
    choice_0 = RectSlot(
        id="slot.choice.option_0",
        prompt="",
        x=165,
        y=76,
        width=175,
        height=90,
        fill="transparent",
        stroke="none",
        stroke_width=0,
        interaction={
            "type": "choice",
            "role": "answer",
            "choice_index": 0,
            "value": "1번 도형(선분)",
            "group_id": "slot.choice.group",
            "include_in_submission": True,
        },
    )

    # 2번 도형: 굽은 선 (양쪽으로 휘어진 선)
    fig1_curve = PathSlot(
        id="slot.diagram.fig1_curve",
        prompt="",
        d="M 435 78 Q 470 144, 582 137",
        fill="none",
        stroke="#111827",
        stroke_width=1.8,
    )
    fig1_dot1 = CircleSlot(
        id="slot.diagram.fig1_dot1",
        prompt="",
        cx=445,
        cy=94,
        r=3.2,
        fill="#111827",
        stroke="#111827",
        stroke_width=1,
    )
    fig1_dot2 = CircleSlot(
        id="slot.diagram.fig1_dot2",
        prompt="",
        cx=564,
        cy=138,
        r=3.2,
        fill="#111827",
        stroke="#111827",
        stroke_width=1,
    )
    choice_1 = RectSlot(
        id="slot.choice.option_1",
        prompt="",
        x=420,
        y=72,
        width=175,
        height=95,
        fill="transparent",
        stroke="none",
        stroke_width=0,
        interaction={
            "type": "choice",
            "role": "answer",
            "choice_index": 1,
            "value": "2번 도형(굽은 선)",
            "group_id": "slot.choice.group",
            "include_in_submission": True,
        },
    )

    # 3번 도형: 직선 (두 점을 지나 양쪽으로 끝없이 뻗은 곧은 선)
    fig2_line = LineSlot(
        id="slot.diagram.fig2_line",
        prompt="",
        x1=682,
        y1=136,
        x2=842,
        y2=86,
        stroke="#111827",
        stroke_width=1.8,
    )
    fig2_dot1 = CircleSlot(
        id="slot.diagram.fig2_dot1",
        prompt="",
        cx=702,
        cy=130,
        r=3.2,
        fill="#111827",
        stroke="#111827",
        stroke_width=1,
    )
    fig2_dot2 = CircleSlot(
        id="slot.diagram.fig2_dot2",
        prompt="",
        cx=822,
        cy=92,
        r=3.2,
        fill="#111827",
        stroke="#111827",
        stroke_width=1,
    )
    choice_2 = RectSlot(
        id="slot.choice.option_2",
        prompt="",
        x=670,
        y=76,
        width=185,
        height=90,
        fill="transparent",
        stroke="none",
        stroke_width=0,
        interaction={
            "type": "choice",
            "role": "answer",
            "choice_index": 2,
            "value": "3번 도형(직선)",
            "group_id": "slot.choice.group",
            "include_in_submission": True,
        },
    )

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=886,
            height=200,
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
                    "slot.diagram.fig0_line",
                    "slot.diagram.fig0_dot1",
                    "slot.diagram.fig0_dot2",
                    "slot.diagram.fig1_curve",
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
            fig0_line,
            fig0_dot1,
            fig0_dot2,
            fig1_curve,
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
        {"ref": "figure.option_0", "value": "line_segment"},
        {"ref": "figure.option_1", "value": "curved_line"},
        {"ref": "figure.option_2", "value": "straight_line"},
    ],
    "target": {"ref": "slot.choice.option_2", "type": "choice"},
    "method": "straight_line_classification",
    "steps": [
        {
            "id": "step.identify_straight_line",
            "expr": "is_straight(figure) and extends_both_directions(figure)",
            "value": "3번 도형(직선)",
            "explanation": "선분을 양쪽으로 끝없이 늘인 곧은 선을 직선이라고 합니다. 1번은 선분, 2번은 굽은 선이므로 3번 도형이 직선입니다.",
        }
    ],
    "answer": ANSWER,
    "diagnostics": {
        "skills": ["geometry.line_identification"],
        "errors": {
            "1번 도형(선분)": "geometry.confused_segment_with_line",
            "2번 도형(굽은 선)": "geometry.confused_curved_with_line",
        },
    },
}
EDITOR_ANSWER_REVIEW = {'mode': 'canvas_select',
 'show_canvas': True,
 'status': 'pending',
 'note': '',
 'answers': [{'value': '3번 도형(직선)', 'ref': 'slot.choice.option_2'}],
 'choices': [{'id': 'slot.choice.option_0',
              'text': '1번 도형(선분)',
              'correct': False,
              'label': '1',
              'sourceRefs': ['slot.choice.option_0']},
             {'id': 'slot.choice.option_1',
              'text': '2번 도형(굽은 선)',
              'correct': False,
              'label': '2',
              'sourceRefs': ['slot.choice.option_1']},
             {'id': 'slot.choice.option_2',
              'text': '3번 도형(직선)',
              'correct': True,
              'label': '3',
              'sourceRefs': ['slot.choice.option_2']}]}
