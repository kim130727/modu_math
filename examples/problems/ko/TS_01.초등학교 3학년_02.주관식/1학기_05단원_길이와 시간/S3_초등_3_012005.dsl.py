"""ModuMath Problem DSL: 도착 시각 구하기 (S3_초등_3_012005)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
)


PROBLEM_ID = "S3_초등_3_012005"
PROBLEM_TITLE = "출발 시각과 걸린 시간으로 도착 시각 구하기"


ANSWER = {
    "type": "short_answer",
    "value": "3시 45분",
    "unit": "",
    "values": ["3시 45분", "3시45분"],
    "choices": [],
    "blanks": [
        {
            "id": "slot.answer.input",
            "slot_id": "slot.answer.input",
            "expected": "3시 45분",
        },
    ],
    "answer_key": [
        {
            "slot_id": "slot.answer.input",
            "value": "3시 45분",
            "diagnostics": [
                {
                    "id": "diag.time_addition_error",
                    "condition": "answer_not_equals_3_45",
                    "concept": "시간의 덧셈",
                    "reason": "3시 20분에 25분을 더하는 계산을 잘못함",
                    "feedback": "3시 20분에서 25분이 지나면 분끼리 더해서 20분 + 25분 = 45분이 되므로 3시 45분입니다.",
                },
            ],
        },
    ],
}


SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "short_answer_time_addition_word_problem",
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
            {"id": "time.departure", "type": "time", "label": "출발 시각", "value": "3시 20분"},
            {"id": "duration.walk", "type": "duration", "label": "걸리는 시간", "value_min": 25},
            {"id": "time.arrival", "type": "time", "label": "도착 시각", "value": "3시 45분"},
        ],
        "relations": [
            {
                "id": "relation.time_addition",
                "type": "arrival_time_of",
                "departure": "time.departure",
                "duration": "duration.walk",
                "arrival": "time.arrival",
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
        text="수지네 집에서 민경이네 집까지는 걸어서 25분이 걸립니다. 수지가 민경이네 집에 가려고 3시 20분에 나왔다면 민경이네 집에는 몇 시 몇 분에 도착할까요?",
        x=32,
        y=24,
        width=836,
        height=136,
        font_size=26,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="left",
        valign="top",
        line_height=1.5,
    )

    paren_left = TextBoxSlot(
        id="slot.answer.paren_left",
        prompt="",
        text="(",
        x=480,
        y=190,
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
        x=514,
        y=190,
        width=250,
        height=54,
        fill="#ffffff",
        stroke="#111827",
        stroke_width=1.4,
        interaction={
            "type": "input",
            "role": "answer",
            "value_type": "text",
            "max_length": 15,
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
        y=190,
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
        paren_left,
        answer_input,
        paren_right,
    )

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=900,
            height=276,
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
