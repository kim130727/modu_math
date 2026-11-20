"""ModuMath Problem DSL: 걸린 시간 비교하기 (S3_초등_3_012000)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    LineSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
)


PROBLEM_ID = "S3_초등_3_012000"
PROBLEM_TITLE = "청소한 시간이 더 긴 사람 찾기"


ANSWER = {
    "type": "short_answer",
    "value": "초림",
    "unit": "",
    "values": ["초림", "초림이"],
    "choices": [],
    "blanks": [
        {
            "id": "slot.answer.input",
            "slot_id": "slot.answer.input",
            "expected": "초림",
        },
    ],
    "answer_key": [
        {
            "slot_id": "slot.answer.input",
            "value": "초림",
            "diagnostics": [
                {
                    "id": "diag.elapsed_time_error",
                    "condition": "answer_equals_minjae",
                    "concept": "걸린 시간 구하기",
                    "reason": "시작 시각과 끝낸 시각 사이의 시간 계산을 잘못함",
                    "feedback": "민재는 3시 50분부터 4시 15분까지 25분, 초림이는 3시 45분부터 4시 30분까지 45분 동안 청소했습니다.",
                },
            ],
        },
    ],
}


SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "short_answer_elapsed_time_comparison",
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
            {"id": "person.minjae", "type": "person", "label": "민재", "start": "3시 50분", "end": "4시 15분", "duration_min": 25},
            {"id": "person.chorim", "type": "person", "label": "초림", "start": "3시 45분", "end": "4시 30분", "duration_min": 45},
        ],
        "relations": [
            {
                "id": "relation.longer_duration",
                "type": "longer_duration_than",
                "from_id": "person.chorim",
                "to_id": "person.minjae",
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
        text="민재와 초림이가 청소를 시작한 시각과 끝낸 시각을 나타낸 것입니다. 누가 청소를 더 오랫동안 하였을까요?",
        x=32,
        y=24,
        width=836,
        height=96,
        font_size=26,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="left",
        valign="top",
        line_height=1.5,
    )

    table_header_bg = RectSlot(
        id="slot.diagram.table_header_bg",
        prompt="",
        x=90,
        y=136,
        width=720,
        height=52,
        fill="#f9bfa3",
        stroke="#f9bfa3",
        stroke_width=1.4,
    )
    table_body_bg = RectSlot(
        id="slot.diagram.table_body_bg",
        prompt="",
        x=90,
        y=188,
        width=720,
        height=112,
        fill="#ffffff",
        stroke="#f9bfa3",
        stroke_width=1.8,
    )
    row_divider = LineSlot(
        id="slot.diagram.row_divider",
        prompt="",
        x1=90,
        y1=244,
        x2=810,
        y2=244,
        stroke="#f9bfa3",
        stroke_width=1.5,
    )
    col_divider_1 = LineSlot(
        id="slot.diagram.col_divider_1",
        prompt="",
        x1=290,
        y1=136,
        x2=290,
        y2=300,
        stroke="#f9bfa3",
        stroke_width=1.5,
    )
    col_divider_2 = LineSlot(
        id="slot.diagram.col_divider_2",
        prompt="",
        x1=550,
        y1=136,
        x2=550,
        y2=300,
        stroke="#f9bfa3",
        stroke_width=1.5,
    )

    hdr_start = TextBoxSlot(
        id="slot.diagram.hdr_start",
        prompt="",
        text="시작 시각",
        x=290,
        y=136,
        width=260,
        height=52,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        valign="middle",
    )
    hdr_end = TextBoxSlot(
        id="slot.diagram.hdr_end",
        prompt="",
        text="끝낸 시각",
        x=550,
        y=136,
        width=260,
        height=52,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        valign="middle",
    )

    r1_name = TextBoxSlot(
        id="slot.diagram.r1_name",
        prompt="",
        text="민재",
        x=90,
        y=188,
        width=200,
        height=56,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        valign="middle",
    )
    r1_start = TextBoxSlot(
        id="slot.diagram.r1_start",
        prompt="",
        text="3시 50분",
        x=290,
        y=188,
        width=260,
        height=56,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        valign="middle",
    )
    r1_end = TextBoxSlot(
        id="slot.diagram.r1_end",
        prompt="",
        text="4시 15분",
        x=550,
        y=188,
        width=260,
        height=56,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        valign="middle",
    )

    r2_name = TextBoxSlot(
        id="slot.diagram.r2_name",
        prompt="",
        text="초림",
        x=90,
        y=244,
        width=200,
        height=56,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        valign="middle",
    )
    r2_start = TextBoxSlot(
        id="slot.diagram.r2_start",
        prompt="",
        text="3시 45분",
        x=290,
        y=244,
        width=260,
        height=56,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        valign="middle",
    )
    r2_end = TextBoxSlot(
        id="slot.diagram.r2_end",
        prompt="",
        text="4시 30분",
        x=550,
        y=244,
        width=260,
        height=56,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        valign="middle",
    )

    paren_left = TextBoxSlot(
        id="slot.answer.paren_left",
        prompt="",
        text="(",
        x=540,
        y=328,
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
        x=574,
        y=328,
        width=190,
        height=54,
        fill="#ffffff",
        stroke="#111827",
        stroke_width=1.4,
        interaction={
            "type": "input",
            "role": "answer",
            "value_type": "text",
            "max_length": 10,
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
        y=328,
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
        table_header_bg,
        table_body_bg,
        row_divider,
        col_divider_1,
        col_divider_2,
        hdr_start,
        hdr_end,
        r1_name,
        r1_start,
        r1_end,
        r2_name,
        r2_start,
        r2_end,
        paren_left,
        answer_input,
        paren_right,
    )

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=900,
            height=410,
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
