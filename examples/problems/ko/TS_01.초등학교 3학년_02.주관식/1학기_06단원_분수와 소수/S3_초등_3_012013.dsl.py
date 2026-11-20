"""ModuMath Problem DSL: 전체를 6으로 나눈 것 중의 부분 구하기 (1) (S3_초등_3_012013)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    LineSlot,
    PolygonSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
)


PROBLEM_ID = "S3_초등_3_012013"
PROBLEM_TITLE = "전체를 6으로 나눈 것 중의 몇인지 구하기 (1)"


ANSWER = {
    "type": "short_answer",
    "value": 2,
    "unit": "",
    "values": [2],
    "choices": [],
    "blanks": [
        {
            "id": "slot.answer.input",
            "slot_id": "slot.answer.input",
            "expected": 2,
        },
    ],
    "answer_key": [
        {
            "slot_id": "slot.answer.input",
            "value": 2,
            "diagnostics": [
                {
                    "id": "diag.part_counting_error",
                    "condition": "answer_not_equals_2",
                    "concept": "전체를 똑같이 나누기",
                    "reason": "부분 도형이 전체 6조각 중 몇 조각에 해당하는지 잘못 셈",
                    "feedback": "전체 사다리꼴을 똑같이 6개의 삼각형으로 나누었을 때, 주어진 평행사변형은 작은 삼각형 2개가 합쳐진 모양이므로 2입니다.",
                },
            ],
        },
    ],
}


SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "short_answer_fraction_part_of_whole",
    "metadata": {
        "school": "초등학교",
        "grade": 3,
        "semester": 1,
        "chapter": "06단원_분수와 소수",
        "subject": "수학",
        "language": "ko-KR",
    },
    "domain": {
        "objects": [
            {"id": "shape.whole", "type": "trapezoid", "label": "전체 도형", "total_parts": 6},
            {"id": "shape.part", "type": "parallelogram", "label": "부분 도형", "parts_count": 2},
        ],
        "relations": [
            {
                "id": "relation.part_of_whole",
                "type": "equal_parts_count",
                "whole": "shape.whole",
                "part": "shape.part",
                "value": 2,
            },
        ],
    },
    "answer": ANSWER,
}

SEMANTIC_OVERRIDE = SEMANTIC


def build_problem_template() -> ProblemTemplate:
    stem_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="다음 부분은 전체 사다리꼴을 똑같이 6으로 나눈 것 중의 몇일까요?",
        x=32,
        y=24,
        width=820,
        height=44,
        font_size=26,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="left",
        valign="top",
        line_height=1.45,
    )

    # 전체 도형 (6등분된 사다리꼴)
    whole_trap = PolygonSlot(
        id="slot.diagram.whole_trap",
        prompt="",
        points=((390, 92), (490, 92), (540, 178), (340, 178)),
        fill="#ede9fe",
        stroke="#7e22ce",
        stroke_width=2.0,
    )
    div_1 = LineSlot(id="slot.diagram.div_1", prompt="", x1=390, y1=92, x2=390, y2=178, stroke="#7e22ce", stroke_width=1.2, stroke_dasharray="3 3")
    div_2 = LineSlot(id="slot.diagram.div_2", prompt="", x1=440, y1=92, x2=390, y2=178, stroke="#7e22ce", stroke_width=1.2, stroke_dasharray="3 3")
    div_3 = LineSlot(id="slot.diagram.div_3", prompt="", x1=440, y1=92, x2=440, y2=178, stroke="#7e22ce", stroke_width=1.2, stroke_dasharray="3 3")
    div_4 = LineSlot(id="slot.diagram.div_4", prompt="", x1=490, y1=92, x2=440, y2=178, stroke="#7e22ce", stroke_width=1.2, stroke_dasharray="3 3")
    div_5 = LineSlot(id="slot.diagram.div_5", prompt="", x1=490, y1=92, x2=490, y2=178, stroke="#7e22ce", stroke_width=1.2, stroke_dasharray="3 3")

    sub_label = TextBoxSlot(
        id="slot.stem.sublabel",
        prompt="",
        text="(1)",
        x=60,
        y=232,
        width=50,
        height=40,
        font_size=26,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="left",
        valign="middle",
    )

    part_para = PolygonSlot(
        id="slot.diagram.part_para",
        prompt="",
        points=((230, 224), (280, 224), (230, 310), (180, 310)),
        fill="#ede9fe",
        stroke="#7e22ce",
        stroke_width=2.0,
    )

    paren_left = TextBoxSlot(
        id="slot.answer.paren_left",
        prompt="",
        text="(",
        x=560,
        y=252,
        width=28,
        height=54,
        font_size=28,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="center",
        valign="middle",
    )

    answer_input = RectSlot(
        id="slot.answer.input",
        prompt="",
        x=594,
        y=252,
        width=170,
        height=54,
        fill="#ffffff",
        stroke="#111827",
        stroke_width=1.4,
        interaction={
            "type": "input",
            "role": "answer",
            "value_type": "integer",
            "max_length": 2,
            "include_in_submission": True,
            "order": 0,
            "group_id": "final_answer",
            "auto_advance": False,
            "keyboard": "number",
        },
        input_style={
            "font_size_mode": "auto",
            "font_size_adjust": 0,
            "min_font_size": 16,
            "max_font_size": 28,
            "font_weight": 700,
            "horizontal_align": "center",
            "vertical_align": "middle",
            "padding": 6,
            "text_color": "#222222",
        },
    )

    paren_right = TextBoxSlot(
        id="slot.answer.paren_right",
        prompt="",
        text=")",
        x=770,
        y=252,
        width=28,
        height=54,
        font_size=28,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="center",
        valign="middle",
    )

    slots = (
        stem_slot,
        whole_trap,
        div_1,
        div_2,
        div_3,
        div_4,
        div_5,
        sub_label,
        part_para,
        paren_left,
        answer_input,
        paren_right,
    )

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=900,
            height=344,
            coordinate_mode="logical",
        ),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=tuple(slot.id for slot in slots),
            ),
        ),
        slots=slots,
    )


PROBLEM_TEMPLATE = build_problem_template()
