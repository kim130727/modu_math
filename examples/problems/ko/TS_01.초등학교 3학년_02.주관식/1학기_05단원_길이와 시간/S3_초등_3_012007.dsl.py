"""ModuMath Problem DSL: 시간의 덧셈과 뺄셈 비교하기 2 (S3_초등_3_012007)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
)


PROBLEM_ID = "S3_초등_3_012007"
PROBLEM_TITLE = "시간의 덧셈과 뺄셈 결과 비교하기 (2)"


ANSWER = {
    "type": "short_answer",
    "value": "ㄱ",
    "unit": "",
    "values": ["ㄱ", "㉠"],
    "choices": [],
    "blanks": [
        {
            "id": "slot.answer.input",
            "slot_id": "slot.answer.input",
            "expected": "ㄱ",
        },
    ],
    "answer_key": [
        {
            "slot_id": "slot.answer.input",
            "value": "ㄱ",
            "diagnostics": [
                {
                    "id": "diag.time_comparison_error",
                    "condition": "answer_equals_na",
                    "concept": "시간의 덧셈과 뺄셈",
                    "reason": "분과 초 단위의 덧셈/뺄셈 계산을 잘못하여 ㉡을 선택함",
                    "feedback": "㉠은 34분 15초 + 2분 34초 = 36분 49초이고, ㉡은 56분 45초 - 21분 12초 = 35분 33초이므로 ㉠이 더 깁니다.",
                },
            ],
        },
    ],
}


SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "short_answer_time_arithmetic_comparison",
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
            {"id": "expr.g", "type": "time_expression", "label": "ㄱ", "text": "34분 15초 + 2분 34초", "result_sec": 2209},
            {"id": "expr.n", "type": "time_expression", "label": "ㄴ", "text": "56분 45초 - 21분 12초", "result_sec": 2133},
        ],
        "relations": [
            {
                "id": "relation.longer_time",
                "type": "greater_than",
                "from_id": "expr.g",
                "to_id": "expr.n",
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
        text="시간이 더 긴 것의 기호를 쓰세요.",
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
        x=120,
        y=88,
        width=660,
        height=148,
        fill="#ffffff",
        stroke="#7dd3fc",
        stroke_width=2.2,
    )

    opt_g = TextBoxSlot(
        id="slot.diagram.opt_g",
        prompt="",
        text="㉠  34분 15초 + 2분 34초",
        x=165,
        y=112,
        width=570,
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
        text="㉡  56분 45초 - 21분 12초",
        x=165,
        y=168,
        width=570,
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
        y=266,
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
        y=266,
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
        y=266,
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
        paren_left,
        answer_input,
        paren_right,
    )

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=900,
            height=348,
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
