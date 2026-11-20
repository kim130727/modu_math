"""ModuMath Problem DSL: 시계의 시각 읽기 (S3_초등_3_011908)"""

from __future__ import annotations

import math

from modu_math.dsl import (
    Canvas,
    CircleSlot,
    LineSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
)


PROBLEM_ID = "S3_초등_3_011908"
PROBLEM_TITLE = "초침까지 있는 시계의 시각 읽기"


ANSWER = {
    "type": "short_answer",
    "value": "1시 48분 29초",
    "unit": "",
    "values": ["1시 48분 29초", "1시48분29초"],
    "choices": [],
    "blanks": [
        {
            "id": "slot.answer.input",
            "slot_id": "slot.answer.input",
            "expected": "1시 48분 29초",
        },
    ],
    "answer_key": [
        {
            "slot_id": "slot.answer.input",
            "value": "1시 48분 29초",
            "diagnostics": [
                {
                    "id": "diag.hour_hand_misread",
                    "condition": "answer_starts_with_2",
                    "concept": "시침 읽기",
                    "reason": "시침이 2에 가까워 2시로 잘못 읽음",
                    "feedback": "짧은바늘(시침)이 숫자 1과 2 사이에 있으므로 아직 2시가 되지 않은 1시입니다.",
                },
                {
                    "id": "diag.second_hand_omitted",
                    "condition": "answer_missing_seconds",
                    "concept": "초침 읽기",
                    "reason": "초바늘이 가리키는 초를 읽지 않음",
                    "feedback": "가장 가는 바늘(초바늘)이 숫자 5에서 작은 눈금 4칸 더 간 곳에 있으므로 29초도 함께 읽어 보세요.",
                },
            ],
        },
    ],
}


SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "short_answer_time_clock_reading",
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
            {"id": "clock.main", "type": "analog_clock", "label": "아날로그 시계", "hour": 1, "minute": 48, "second": 29},
        ],
        "relations": [
            {
                "id": "relation.shows_time",
                "type": "displays_time",
                "from_id": "clock.main",
                "to_id": "time.01_48_29",
            },
        ],
    },
    "answer": ANSWER,
}

SEMANTIC_OVERRIDE = SEMANTIC


def _clock_slots(cx: float, cy: float, r: float) -> list[object]:
    slots: list[object] = [
        CircleSlot(
            id="slot.diagram.clock_outer",
            prompt="",
            cx=cx,
            cy=cy,
            r=r,
            fill="#e5e7eb",
            stroke="#374151",
            stroke_width=1.6,
        ),
        CircleSlot(
            id="slot.diagram.clock_inner",
            prompt="",
            cx=cx,
            cy=cy,
            r=r - 12,
            fill="#ffffff",
            stroke="#9ca3af",
            stroke_width=1.0,
        ),
    ]

    for tick in range(60):
        angle = math.radians(tick * 6 - 90)
        is_major = tick % 5 == 0
        r_start = r - (11 if is_major else 8)
        r_end = r - 1
        slots.append(
            LineSlot(
                id=f"slot.diagram.clock_tick_{tick}",
                prompt="",
                x1=round(cx + r_start * math.cos(angle), 2),
                y1=round(cy + r_start * math.sin(angle), 2),
                x2=round(cx + r_end * math.cos(angle), 2),
                y2=round(cy + r_end * math.sin(angle), 2),
                stroke="#111827" if is_major else "#4b5563",
                stroke_width=2.2 if is_major else 1.1,
            )
        )

    for num in range(1, 13):
        angle = math.radians(num * 30 - 90)
        nr = r - 27
        nx = cx + nr * math.cos(angle)
        ny = cy + nr * math.sin(angle)
        slots.append(
            TextBoxSlot(
                id=f"slot.diagram.clock_num_{num}",
                prompt="",
                text=str(num),
                x=round(nx - 16, 2),
                y=round(ny - 14, 2),
                width=32,
                height=28,
                font_size=20,
                font_family='"Noto Sans KR", sans-serif',
                fill="#111827",
                align="center",
                valign="middle",
            )
        )

    # 1시 48분 29초 바늘 각도 계산
    hour_angle = math.radians(((1 + 48.5 / 60.0) * 30.0) - 90.0)
    min_angle = math.radians(((48 + 29 / 60.0) * 6.0) - 90.0)
    sec_angle = math.radians((29 * 6.0) - 90.0)

    slots.extend(
        [
            LineSlot(
                id="slot.diagram.hand_hour",
                prompt="",
                x1=cx,
                y1=cy,
                x2=round(cx + (r - 52) * math.cos(hour_angle), 2),
                y2=round(cy + (r - 52) * math.sin(hour_angle), 2),
                stroke="#6b7280",
                stroke_width=5.0,
            ),
            LineSlot(
                id="slot.diagram.hand_minute",
                prompt="",
                x1=cx,
                y1=cy,
                x2=round(cx + (r - 24) * math.cos(min_angle), 2),
                y2=round(cy + (r - 24) * math.sin(min_angle), 2),
                stroke="#4b5563",
                stroke_width=3.0,
            ),
            LineSlot(
                id="slot.diagram.hand_second",
                prompt="",
                x1=cx,
                y1=cy,
                x2=round(cx + (r - 15) * math.cos(sec_angle), 2),
                y2=round(cy + (r - 15) * math.sin(sec_angle), 2),
                stroke="#111827",
                stroke_width=1.4,
            ),
            CircleSlot(
                id="slot.diagram.clock_center",
                prompt="",
                cx=cx,
                cy=cy,
                r=5.5,
                fill="#111827",
                stroke="#111827",
                stroke_width=1.0,
            ),
        ]
    )
    return slots


def build_problem_template() -> ProblemTemplate:
    stem_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="시계의 시각을 읽어 보세요.",
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

    clock_slots = _clock_slots(450.0, 198.0, 112.0)

    paren_left = TextBoxSlot(
        id="slot.answer.paren_left",
        prompt="",
        text="(",
        x=430,
        y=338,
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
        x=464,
        y=338,
        width=300,
        height=54,
        fill="#ffffff",
        stroke="#111827",
        stroke_width=1.4,
        interaction={
            "type": "input",
            "role": "answer",
            "value_type": "text",
            "max_length": 20,
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
        y=338,
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
        *clock_slots,
        paren_left,
        answer_input,
        paren_right,
    )

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=900,
            height=420,
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
