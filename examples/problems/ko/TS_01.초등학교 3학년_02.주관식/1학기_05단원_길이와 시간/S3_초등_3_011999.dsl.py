"""ModuMath Problem DSL: 길이가 가장 긴 것 찾아 기호 쓰기 (S3_초등_3_011999)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
)


PROBLEM_ID = "S3_초등_3_011999"
PROBLEM_TITLE = "단위가 다른 길이 비교하여 가장 긴 것 찾기"


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
                    "id": "diag.unit_conversion_error",
                    "condition": "answer_in_ga_da_ra",
                    "concept": "m와 cm의 단위 환산",
                    "reason": "m와 cm를 같은 단위로 통일하지 않고 숫자 크기만 비교함",
                    "feedback": "1 m = 100 cm이므로 ㉠은 205 cm, ㉡은 250 cm, ㉢은 97 cm, ㉣은 210 cm입니다. 가장 긴 것은 ㉡입니다.",
                },
            ],
        },
    ],
}


SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "short_answer_length_comparison",
    "metadata": {
        "school": "초등학교",
        "grade": 3,
        "semester": 1,
        "chapter": "05단원_길이와 시간",
        "subject": "수학",
        "language": "ko-KR",
    },
    "domain": {
        "objects": [
            {"id": "length.g", "type": "length", "label": "ㄱ", "text": "2 m 5 cm", "cm_value": 205},
            {"id": "length.n", "type": "length", "label": "ㄴ", "text": "250 cm", "cm_value": 250},
            {"id": "length.d", "type": "length", "label": "ㄷ", "text": "97 cm", "cm_value": 97},
            {"id": "length.r", "type": "length", "label": "ㄹ", "text": "2 m 10 cm", "cm_value": 210},
        ],
        "relations": [
            {
                "id": "relation.longest",
                "type": "longest_among",
                "from_id": "length.n",
                "to_id": "concept.length",
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
        text="길이가 가장 긴 것을 찾아 기호를 쓰세요.",
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

    box_outer = RectSlot(
        id="slot.diagram.box_outer",
        prompt="",
        x=70,
        y=88,
        width=760,
        height=164,
        fill="#ffffff",
        stroke="#7dd3fc",
        stroke_width=2.2,
    )

    opt_g = TextBoxSlot(
        id="slot.diagram.opt_g",
        prompt="",
        text="㉠  2 m 5 cm",
        x=130,
        y=114,
        width=280,
        height=44,
        font_size=28,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="left",
        valign="middle",
    )
    opt_n = TextBoxSlot(
        id="slot.diagram.opt_n",
        prompt="",
        text="㉡  250 cm",
        x=480,
        y=114,
        width=280,
        height=44,
        font_size=28,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="left",
        valign="middle",
    )
    opt_d = TextBoxSlot(
        id="slot.diagram.opt_d",
        prompt="",
        text="㉢  97 cm",
        x=130,
        y=180,
        width=280,
        height=44,
        font_size=28,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="left",
        valign="middle",
    )
    opt_r = TextBoxSlot(
        id="slot.diagram.opt_r",
        prompt="",
        text="㉣  2 m 10 cm",
        x=480,
        y=180,
        width=280,
        height=44,
        font_size=28,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="left",
        valign="middle",
    )

    paren_left = TextBoxSlot(
        id="slot.answer.paren_left",
        prompt="",
        text="(",
        x=560,
        y=282,
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
        y=282,
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
        y=282,
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
        box_outer,
        opt_g,
        opt_n,
        opt_d,
        opt_r,
        paren_left,
        answer_input,
        paren_right,
    )

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=900,
            height=364,
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
