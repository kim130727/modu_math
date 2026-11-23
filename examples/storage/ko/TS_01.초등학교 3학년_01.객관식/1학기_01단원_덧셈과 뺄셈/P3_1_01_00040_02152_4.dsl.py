from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    CircleSlot,
    LineSlot,
    PathSlot,
    PolygonSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
)


PROBLEM_ID = "P3_1_01_00040_02152_4"
PROBLEM_TITLE = "수 모형으로 알아보는 세 자리 수의 덧셈 (4)"


def _rect_slot(id: str, x: float, y: float, width: float, height: float, fill: str = "#ffffff", stroke: str = "#444444", stroke_width: float = 1.0) -> RectSlot:
    return RectSlot(id=id, x=x, y=y, width=width, height=height, fill=fill, stroke=stroke, stroke_width=stroke_width)


def _answer_input_slot(
    id: str,
    x: float,
    y: float,
    width: float,
    *,
    order: int,
    max_length: int = 1,
) -> RectSlot:
    return RectSlot(
        id=id,
        x=x,
        y=y,
        width=width,
        height=38,
        rx=6,
        ry=6,
        fill="#ffffff",
        stroke="#5C6AC4",
        stroke_width=1.6,
        prompt="숫자를 입력하세요.",
        interaction={
            "type": "input",
            "role": "answer",
            "value_type": "digit" if max_length == 1 else "integer",
            "max_length": max_length,
            "keyboard": "number",
            "include_in_submission": True,
            "order": order,
            "group_id": "final_answer",
            "answer_key_index": order,
            "answer_ref": f"answer_key[{order}]",
            "auto_advance": max_length == 1,
        },
        input_style={
            "font_size_mode": "auto",
            "min_font_size": 16,
            "max_font_size": 28,
            "font_weight": 700,
            "horizontal_align": "center",
            "vertical_align": "middle",
            "padding": 3,
            "text_color": "#202124",
        },
    )


def _segments_path(segments: list[tuple[float, float, float, float]]) -> str:
    return " ".join(f"M {x1:g} {y1:g} L {x2:g} {y2:g}" for x1, y1, x2, y2 in segments)


def _hundred_flat(prefix: str, x: float, y: float, size: float = 34.0) -> tuple:
    slots = [
        _rect_slot(f"{prefix}.body", x, y, size, size, fill="#e7f5d8", stroke="#9cc37f", stroke_width=1.0),
    ]
    step = size / 10
    segments = []
    for i in range(1, 10):
        offset = step * i
        segments.append((x + offset, y, x + offset, y + size))
        segments.append((x, y + offset, x + size, y + offset))
    slots.append(PathSlot(id=f"{prefix}.grid", d=_segments_path(segments), fill="none", stroke="#c9dfb9", stroke_width=0.45))
    return tuple(slots)


def _ten_rod(prefix: str, x: float, y: float, width: float = 9.0, height: float = 38.0) -> tuple:
    slots = [
        _rect_slot(f"{prefix}.body", x, y, width, height, fill="#d9efff", stroke="#6fb6df", stroke_width=1.0),
    ]
    step = height / 10
    segments = []
    for i in range(1, 10):
        offset = step * i
        segments.append((x, y + offset, x + width, y + offset))
    slots.append(PathSlot(id=f"{prefix}.grid", d=_segments_path(segments), fill="none", stroke="#9fd0ed", stroke_width=0.55))
    return tuple(slots)


def _one_dot(prefix: str, x: float, y: float) -> tuple:
    return (CircleSlot(id=f"{prefix}.dot", cx=x, cy=y, r=2.2, fill="#f59ab5", stroke="#d66d91", stroke_width=0.7),)


def _thousand_cube(prefix: str, x: float, y: float, size: float = 38.0) -> tuple:
    depth = 14.0
    slots = [
        PolygonSlot(
            id=f"{prefix}.front",
            points=((x, y + depth), (x + size, y + depth), (x + size, y + depth + size), (x, y + depth + size)),
            fill="#d9f0c8",
            stroke="#8fba72",
            stroke_width=1.0,
        ),
        PolygonSlot(
            id=f"{prefix}.top",
            points=((x, y + depth), (x + depth, y), (x + size + depth, y), (x + size, y + depth)),
            fill="#e8f8dc",
            stroke="#8fba72",
            stroke_width=1.0,
        ),
        PolygonSlot(
            id=f"{prefix}.side",
            points=((x + size, y + depth), (x + size + depth, y), (x + size + depth, y + size), (x + size, y + depth + size)),
            fill="#c6e6b2",
            stroke="#8fba72",
            stroke_width=1.0,
        ),
    ]
    grid = "#a8cc90"
    step = size / 10
    dstep = depth / 10
    front_segments = []
    top_segments = []
    side_segments = []
    for i in range(1, 10):
        offset = step * i
        doffset = dstep * i
        front_segments.append((x + offset, y + depth, x + offset, y + depth + size))
        front_segments.append((x, y + depth + offset, x + size, y + depth + offset))
        top_segments.append((x + doffset, y + depth - doffset, x + size + doffset, y + depth - doffset))
        top_segments.append((x + offset, y + depth, x + offset + depth, y))
        side_segments.append((x + size + doffset, y + depth - doffset, x + size + doffset, y + depth + size - doffset))
        side_segments.append((x + size, y + depth + offset, x + size + depth, y + offset))
    slots.extend(
        (
            PathSlot(id=f"{prefix}.front.grid", d=_segments_path(front_segments), fill="none", stroke=grid, stroke_width=0.45),
            PathSlot(id=f"{prefix}.top.grid", d=_segments_path(top_segments), fill="none", stroke=grid, stroke_width=0.45),
            PathSlot(id=f"{prefix}.side.grid", d=_segments_path(side_segments), fill="none", stroke=grid, stroke_width=0.45),
        )
    )
    return tuple(slots)


def _base_ten_model_slots() -> tuple:
    slots = [
        _rect_slot("slot.diagram.top_box", 50, 74, 800, 208, fill="#ffffff", stroke="#718096", stroke_width=1.2),
        _rect_slot("slot.diagram.bottom_box", 50, 320, 800, 86, fill="#f8fafc", stroke="#5C6AC4", stroke_width=1.5),
        LineSlot(id="slot.diagram.divider", x1=65, y1=156, x2=835, y2=156, stroke="#e2e8f0", stroke_width=1.0),
        LineSlot(id="slot.diagram.arrow_line", x1=450, y1=286, x2=450, y2=306, stroke="#5C6AC4", stroke_width=3.5),
        PolygonSlot(id="slot.diagram.arrow_head", points=((443, 304), (457, 304), (450, 314)), fill="#5C6AC4", stroke="#5C6AC4", stroke_width=1),
        TextBoxSlot(id="slot.diagram.col_hundreds", x=240, y=78, width=120, height=26, text="백 모형", font_size=15, fill="#4a5568", align="center", valign="middle"),
        TextBoxSlot(id="slot.diagram.col_tens", x=470, y=78, width=100, height=26, text="십 모형", font_size=15, fill="#4a5568", align="center", valign="middle"),
        TextBoxSlot(id="slot.diagram.col_ones", x=660, y=78, width=100, height=26, text="낱개 모형", font_size=15, fill="#4a5568", align="center", valign="middle"),
        TextBoxSlot(id="slot.diagram.label_599", x=70, y=110, width=110, height=30, text="위인전 599", font_size=18, fill="#2d3748", align="left", valign="middle"),
        TextBoxSlot(id="slot.diagram.label_837", x=70, y=195, width=110, height=30, text="+ 동화책 837", font_size=18, fill="#2d3748", align="left", valign="middle"),
        TextBoxSlot(id="slot.diagram.arrow_text", x=465, y=288, width=360, height=26, text="10개씩 묶어 윗자리로 받아올림합니다.", font_size=14, fill="#5C6AC4", align="left", valign="middle"),
        TextBoxSlot(id="slot.diagram.label_result", x=70, y=348, width=110, height=30, text="= 모두 1436", font_size=18, fill="#1e293b", align="left", valign="middle"),
    ]

    for index in range(5):
        slots.extend(_hundred_flat(f"slot.model.599.h{index + 1}", 200 + index * 40, 108))
    for index in range(9):
        slots.extend(_ten_rod(f"slot.model.599.t{index + 1}", 440 + index * 15, 106))
    for index in range(9):
        slots.extend(_one_dot(f"slot.model.599.o{index + 1}", 640 + index * 14, 125))

    for index in range(8):
        row = index // 4
        col = index % 4
        slots.extend(_hundred_flat(f"slot.model.837.h{index + 1}", 200 + col * 40, 170 + row * 40))
    for index in range(3):
        slots.extend(_ten_rod(f"slot.model.837.t{index + 1}", 440 + index * 15, 188))
    for index in range(7):
        slots.extend(_one_dot(f"slot.model.837.o{index + 1}", 640 + index * 14, 207))

    slots.extend(_thousand_cube("slot.model.result.thousand1", 200, 336))
    for index in range(4):
        slots.extend(_hundred_flat(f"slot.model.result.h{index + 1}", 275 + index * 40, 346))
    for index in range(3):
        slots.extend(_ten_rod(f"slot.model.result.t{index + 1}", 480 + index * 15, 344))
    for index in range(6):
        slots.extend(_one_dot(f"slot.model.result.o{index + 1}", 640 + index * 14, 363))

    return tuple(slots)


BASE_TEN_MODEL_SLOTS = _base_ten_model_slots()
BASE_TEN_MODEL_SLOT_IDS = tuple(slot.id for slot in BASE_TEN_MODEL_SLOTS)


ANSWER = {
    "value": 1436,
    "unit": "권",
    "values": [1436],
    "choices": [],
    "blanks": [
        {"id": "slot.answer.total_books", "slot_id": "slot.answer.total_books", "expected": 1436},
    ],
    "answer_key": [
        {"slot_id": "slot.answer.total_books", "value": 1436},
    ],
}


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=900,
            height=500,
            coordinate_mode="logical",
        ),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.question",),
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=BASE_TEN_MODEL_SLOT_IDS,
            ),
            Region(
                id="region.answer",
                role="answer",
                flow="absolute",
                slot_ids=(
                    "slot.answer_4",
                    "slot.answer.total_books",
                ),
            ),
        ),
        slots=(
            TextBoxSlot(
                id="slot.question",
                x=30,
                y=18,
                width=840,
                height=48,
                text=(
                    "병현이네 학교 도서관에 위인전이 599권, 동화책이 837권 있습니다. "
                    "모두 몇 권의 책이 있는지 수 모형으로 알아보시오."
                ),
                font_size=22,
                font_family='"Poor Story", "Noto Sans KR", sans-serif',
                fill="#202124",
                align="left",
                valign="middle",
            ),
            *BASE_TEN_MODEL_SLOTS,
            TextBoxSlot(
                id="slot.answer_4",
                x=30,
                y=430,
                width=840,
                height=38,
                text="(4) 도서관의 책 수는 모두               권입니다.",
                font_size=20,
                font_family='"Poor Story", "Noto Sans KR", sans-serif',
                fill="#202124",
                align="left",
                valign="middle",
            ),
            _answer_input_slot("slot.answer.total_books", 300, 430, 72, order=0, max_length=4),
        ),
    )


PROBLEM_TEMPLATE = build_problem_template()


SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "numeric_answer_base_ten_model_addition",
    "metadata": {
        "grade": 3,
        "semester": 1,
        "subject": "수학",
        "topic": "받아올림이 두 번 있는 세 자리 수의 덧셈 (전체 책 수)",
        "language": "ko-KR",
    },
    "domain": {
        "objects": [
            {"id": "book.biography", "type": "book_collection", "label": "위인전", "count": 599, "unit": "권"},
            {"id": "book.fairy_tale", "type": "book_collection", "label": "동화책", "count": 837, "unit": "권"},
            {"id": "book.total", "type": "book_collection", "label": "도서관에 있는 전체 책", "count": 1436, "unit": "권"},
        ],
        "relations": [
            {
                "id": "relation.total_books_sum",
                "type": "sum_of",
                "subject": "book.total",
                "objects": ["book.biography", "book.fairy_tale"],
            },
        ],
    },
    "answer": ANSWER,
}

SEMANTIC_OVERRIDE = SEMANTIC
