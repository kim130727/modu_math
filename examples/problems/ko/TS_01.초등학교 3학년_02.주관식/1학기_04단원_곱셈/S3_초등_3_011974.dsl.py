"""ModuMath Problem DSL: 사과 개수를 곱셈식으로 나타내기 (S3_초등_3_011974)"""

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


PROBLEM_ID = "S3_초등_3_011974"
PROBLEM_TITLE = "사과 묶음을 곱셈식으로 나타내기"


ANSWER = {
    "type": "short_answer",
    "value": "3 × 6 = 18",
    "unit": "",
    "values": ["3 × 6 = 18", "3×6=18", "3 * 6 = 18"],
    "choices": [],
    "blanks": [
        {
            "id": "slot.answer.input",
            "slot_id": "slot.answer.input",
            "expected": "3 × 6 = 18",
        },
    ],
    "answer_key": [
        {
            "slot_id": "slot.answer.input",
            "value": "3 × 6 = 18",
            "diagnostics": [
                {
                    "id": "diag.swapped_factors",
                    "condition": "answer_equals_6_times_3",
                    "concept": "곱셈식의 의미",
                    "reason": "묶음당 개수(3)와 묶음 수(6)의 순서를 바꾸어 씀",
                    "feedback": "한 접시에 사과가 3개씩 6접시 있으므로 '3씩 6묶음'을 나타내는 3 × 6 = 18로 써 보세요.",
                },
            ],
        },
    ],
}


SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "short_answer_multiplication_modeling",
    "metadata": {
        "school": "초등학교",
        "grade": 3,
        "semester": 1,
        "chapter": "04단원_곱셈",
        "subject": "수학",
        "language": "ko-KR",
    },
    "domain": {
        "objects": [
            {"id": "quantity.apples_per_plate", "type": "quantity", "label": "한 접시의 사과 수", "value": 3, "unit": "개"},
            {"id": "quantity.plates", "type": "quantity", "label": "접시 수", "value": 6, "unit": "접시"},
            {"id": "quantity.total_apples", "type": "quantity", "label": "전체 사과 수", "value": 18, "unit": "개"},
        ],
        "relations": [
            {
                "id": "relation.multiplication",
                "type": "product_of",
                "multiplicand": "quantity.apples_per_plate",
                "multiplier": "quantity.plates",
                "product": "quantity.total_apples",
            },
        ],
    },
    "answer": ANSWER,
}

SEMANTIC_OVERRIDE = SEMANTIC


def _plate_with_apples(idx: int, cx: float, cy: float) -> list[object]:
    slots: list[object] = [
        PathSlot(
            id=f"slot.diagram.plate_{idx}",
            prompt="",
            d=f"M {cx - 95} {cy + 18} Q {cx} {cy + 42} {cx + 95} {cy + 18} Q {cx} {cy + 2} {cx - 95} {cy + 18} Z",
            fill="#bae6fd",
            stroke="#0284c7",
            stroke_width=1.4,
        )
    ]
    for k, dx in enumerate((-42, 0, 42), start=1):
        ax = cx + dx
        ay = cy - 4
        slots.append(
            CircleSlot(
                id=f"slot.diagram.plate_{idx}_apple_{k}",
                prompt="",
                cx=ax,
                cy=ay,
                r=18.0,
                fill="#fb7185",
                stroke="#be123c",
                stroke_width=1.3,
            )
        )
        slots.append(
            LineSlot(
                id=f"slot.diagram.plate_{idx}_stem_{k}",
                prompt="",
                x1=ax,
                y1=ay - 17,
                x2=ax + 4,
                y2=ay - 26,
                stroke="#111827",
                stroke_width=1.8,
            )
        )
    return slots


def build_problem_template() -> ProblemTemplate:
    stem_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="그림을 보고 사과는 모두 몇 개인지 곱셈식으로 나타내세요.",
        x=32,
        y=24,
        width=836,
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
        y=84,
        width=760,
        height=278,
        fill="#ffffff",
        stroke="#7dd3fc",
        stroke_width=2.0,
    )

    plate_coords = (
        (220, 134),
        (490, 134),
        (360, 224),
        (640, 224),
        (220, 314),
        (530, 314),
    )
    plate_slots: list[object] = []
    for idx, (px, py) in enumerate(plate_coords, start=1):
        plate_slots.extend(_plate_with_apples(idx, px, py))

    paren_left = TextBoxSlot(
        id="slot.answer.paren_left",
        prompt="",
        text="(",
        x=480,
        y=386,
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
        y=386,
        width=250,
        height=54,
        fill="#ffffff",
        stroke="#111827",
        stroke_width=1.4,
        interaction={
            "type": "input",
            "role": "answer",
            "value_type": "text",
            "max_length": 16,
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
        y=386,
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
        *plate_slots,
        paren_left,
        answer_input,
        paren_right,
    )

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=900,
            height=468,
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
