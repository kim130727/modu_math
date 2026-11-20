"""ModuMath Problem DSL: 도형을 똑같이 둘로 나눌 수 없는 점선 찾기 (S3_초등_3_012038)"""

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


PROBLEM_ID = "S3_초등_3_012038"
PROBLEM_TITLE = "도형을 똑같이 둘로 나눌 수 없는 점선 찾기"


ANSWER = {
    "type": "short_answer",
    "value": "ㄴ",
    "unit": "",
    "values": ["ㄴ", "㉡"],
    "choices": [],
    "blanks": [
        {
            "id": "slot.answer.input",
            "slot_id": "slot.answer.input",
            "expected": "ㄴ",
        },
    ],
    "answer_key": [
        {
            "slot_id": "slot.answer.input",
            "value": "ㄴ",
            "diagnostics": [
                {
                    "id": "diag.equal_halves_error",
                    "condition": "answer_in_g_d_r",
                    "concept": "똑같이 둘로 나누기",
                    "reason": "도형의 중심을 지나 똑같이 둘로 나누는 점선을 답함",
                    "feedback": "㉠, ㉢, ㉣은 도형을 크기와 모양이 같게 둘로 나누지만, ㉡으로 나누면 위쪽 삼각형과 아래쪽 오각형으로 크기와 모양이 다릅니다.",
                },
            ],
        },
    ],
}


SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "short_answer_fraction_equal_division",
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
            {"id": "line.g", "type": "dividing_line", "label": "ㄱ", "divides_equally": True},
            {"id": "line.n", "type": "dividing_line", "label": "ㄴ", "divides_equally": False},
            {"id": "line.d", "type": "dividing_line", "label": "ㄷ", "divides_equally": True},
            {"id": "line.r", "type": "dividing_line", "label": "ㄹ", "divides_equally": True},
        ],
        "relations": [
            {
                "id": "relation.not_equal_division",
                "type": "does_not_divide_equally",
                "from_id": "line.n",
                "to_id": "shape.hexagon",
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
        text="오른쪽 그림에서 도형을 똑같이 둘로 나눌 수 없는 점선을 찾아 기호를 쓰세요.",
        x=32,
        y=36,
        width=360,
        height=180,
        font_size=26,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="left",
        valign="top",
        line_height=1.55,
    )

    # 정육각형 (중심 660, 175, 반지름 100)
    hex_slot = PolygonSlot(
        id="slot.diagram.hexagon",
        prompt="",
        points=(
            (660.0, 75.0),
            (746.6, 125.0),
            (746.6, 225.0),
            (660.0, 275.0),
            (573.4, 225.0),
            (573.4, 125.0),
        ),
        fill="#d9ead3",
        stroke="#6aa84f",
        stroke_width=1.8,
    )

    line_g = LineSlot(
        id="slot.diagram.line_g",
        prompt="",
        x1=595,
        y1=62,
        x2=725,
        y2=288,
        stroke="#ec4899",
        stroke_width=1.6,
        stroke_dasharray="4 4",
    )
    line_n = LineSlot(
        id="slot.diagram.line_n",
        prompt="",
        x1=550,
        y1=125,
        x2=770,
        y2=125,
        stroke="#ec4899",
        stroke_width=1.6,
        stroke_dasharray="4 4",
    )
    line_d = LineSlot(
        id="slot.diagram.line_d",
        prompt="",
        x1=550,
        y1=175,
        x2=770,
        y2=175,
        stroke="#ec4899",
        stroke_width=1.6,
        stroke_dasharray="4 4",
    )
    line_r = LineSlot(
        id="slot.diagram.line_r",
        prompt="",
        x1=550,
        y1=238,
        x2=770,
        y2=112,
        stroke="#ec4899",
        stroke_width=1.6,
        stroke_dasharray="4 4",
    )

    lbl_g = TextBoxSlot(id="slot.diagram.lbl_g", prompt="", text="㉠", x=562, y=36, width=36, height=34, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", valign="middle")
    lbl_n = TextBoxSlot(id="slot.diagram.lbl_n", prompt="", text="㉡", x=506, y=108, width=36, height=34, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", valign="middle")
    lbl_d = TextBoxSlot(id="slot.diagram.lbl_d", prompt="", text="㉢", x=506, y=158, width=36, height=34, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", valign="middle")
    lbl_r = TextBoxSlot(id="slot.diagram.lbl_r", prompt="", text="㉣", x=506, y=224, width=36, height=34, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", valign="middle")

    paren_left = TextBoxSlot(
        id="slot.answer.paren_left",
        prompt="",
        text="(",
        x=560,
        y=310,
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
        y=310,
        width=170,
        height=54,
        fill="#ffffff",
        stroke="#111827",
        stroke_width=1.4,
        interaction={
            "type": "input",
            "role": "answer",
            "value_type": "text",
            "max_length": 4,
            "include_in_submission": True,
            "order": 0,
            "group_id": "final_answer",
            "auto_advance": False,
            "keyboard": "text",
        },
        input_style={
            "font_size_mode": "auto",
            "font_size_adjust": 0,
            "min_font_size": 16,
            "max_font_size": 26,
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
        y=310,
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
        hex_slot,
        line_g,
        line_n,
        line_d,
        line_r,
        lbl_g,
        lbl_n,
        lbl_d,
        lbl_r,
        paren_left,
        answer_input,
        paren_right,
    )

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=900,
            height=390,
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
