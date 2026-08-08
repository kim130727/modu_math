from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    CircleSlot,
    LineSlot,
    PolygonSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
)


PROBLEM_ID = "P3_1_01_00040_02152"
PROBLEM_TITLE = "수 모형으로 알아보는 세 자리 수의 덧셈"


def _rect_slot(id: str, x: float, y: float, width: float, height: float, fill: str = "#ffffff", stroke: str = "#444444", stroke_width: float = 1.0) -> RectSlot:
    return RectSlot(id=id, x=x, y=y, width=width, height=height, fill=fill, stroke=stroke, stroke_width=stroke_width)


def _hundred_flat(prefix: str, x: float, y: float, size: float = 34.0) -> tuple:
    slots = [
        _rect_slot(f"{prefix}.body", x, y, size, size, fill="#e7f5d8", stroke="#9cc37f", stroke_width=1.0),
    ]
    step = size / 10
    for i in range(1, 10):
        slots.append(LineSlot(id=f"{prefix}.v{i}", x1=x + step * i, y1=y, x2=x + step * i, y2=y + size, stroke="#c9dfb9", stroke_width=0.45))
        slots.append(LineSlot(id=f"{prefix}.h{i}", x1=x, y1=y + step * i, x2=x + size, y2=y + step * i, stroke="#c9dfb9", stroke_width=0.45))
    return tuple(slots)


def _ten_rod(prefix: str, x: float, y: float, width: float = 9.0, height: float = 38.0) -> tuple:
    slots = [
        _rect_slot(f"{prefix}.body", x, y, width, height, fill="#d9efff", stroke="#6fb6df", stroke_width=1.0),
    ]
    step = height / 10
    for i in range(1, 10):
        slots.append(LineSlot(id=f"{prefix}.s{i}", x1=x, y1=y + step * i, x2=x + width, y2=y + step * i, stroke="#9fd0ed", stroke_width=0.55))
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
    for i in range(1, 10):
        offset = step * i
        doffset = dstep * i
        slots.extend(
            (
                LineSlot(id=f"{prefix}.front.v{i}", x1=x + offset, y1=y + depth, x2=x + offset, y2=y + depth + size, stroke=grid, stroke_width=0.45),
                LineSlot(id=f"{prefix}.front.h{i}", x1=x, y1=y + depth + offset, x2=x + size, y2=y + depth + offset, stroke=grid, stroke_width=0.45),
                LineSlot(id=f"{prefix}.top.depth{i}", x1=x + doffset, y1=y + depth - doffset, x2=x + size + doffset, y2=y + depth - doffset, stroke=grid, stroke_width=0.45),
                LineSlot(id=f"{prefix}.top.width{i}", x1=x + offset, y1=y + depth, x2=x + offset + depth, y2=y, stroke=grid, stroke_width=0.45),
                LineSlot(id=f"{prefix}.side.depth{i}", x1=x + size + doffset, y1=y + depth - doffset, x2=x + size + doffset, y2=y + depth + size - doffset, stroke=grid, stroke_width=0.45),
                LineSlot(id=f"{prefix}.side.height{i}", x1=x + size, y1=y + depth + offset, x2=x + size + depth, y2=y + offset, stroke=grid, stroke_width=0.45),
            )
        )
    return tuple(slots)


def _base_ten_model_slots() -> tuple:
    slots = [
        _rect_slot("slot.diagram.top_box", 35, 98, 405, 212, fill="#ffffff", stroke="#6f6f6f", stroke_width=1.2),
        _rect_slot("slot.diagram.bottom_box", 35, 338, 405, 112, fill="#ffffff", stroke="#6f6f6f", stroke_width=1.2),
        LineSlot(id="slot.diagram.arrow_line", x1=238, y1=315, x2=238, y2=333, stroke="#9a9a9a", stroke_width=5),
        PolygonSlot(id="slot.diagram.arrow_head", points=((229, 326), (247, 326), (238, 340)), fill="#9a9a9a", stroke="#9a9a9a", stroke_width=1),
    ]

    # 599: 5 hundreds, 9 tens, 9 ones
    for index in range(5):
        slots.extend(_hundred_flat(f"slot.model.599.h{index + 1}", 50 + index * 45, 122))
    for index in range(9):
        slots.extend(_ten_rod(f"slot.model.599.t{index + 1}", 275 + index * 13, 118))
    for index in range(9):
        slots.extend(_one_dot(f"slot.model.599.o{index + 1}", 396, 119 + index * 9))

    # 837: 8 hundreds, 3 tens, 7 ones
    for index in range(8):
        row = index // 5
        col = index % 5
        slots.extend(_hundred_flat(f"slot.model.837.h{index + 1}", 50 + col * 45, 178 + row * 46))
    for index in range(3):
        slots.extend(_ten_rod(f"slot.model.837.t{index + 1}", 275 + index * 13, 182))
    for index in range(7):
        slots.extend(_one_dot(f"slot.model.837.o{index + 1}", 396, 184 + index * 9))

    # Regrouped 1436: 1 thousand, 4 hundreds, 3 tens, 6 ones
    slots.extend(_thousand_cube("slot.model.result.thousand1", 52, 352))
    for index in range(4):
        slots.extend(_hundred_flat(f"slot.model.result.h{index + 1}", 142 + index * 46, 370))
    for index in range(3):
        slots.extend(_ten_rod(f"slot.model.result.t{index + 1}", 336 + index * 14, 368))
    for index in range(6):
        slots.extend(_one_dot(f"slot.model.result.o{index + 1}", 407 + (index % 2) * 12, 368 + (index // 2) * 13))

    return tuple(slots)


BASE_TEN_MODEL_SLOTS = _base_ten_model_slots()
BASE_TEN_MODEL_SLOT_IDS = tuple(slot.id for slot in BASE_TEN_MODEL_SLOTS)


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=900,
            height=650,
            coordinate_mode="logical",
        ),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.question",
                ),
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    *BASE_TEN_MODEL_SLOT_IDS,
                    "slot.model_legend",
                    "slot.first_number_label",
                    "slot.first_number_models",
                    "slot.second_number_label",
                    "slot.second_number_models",
                    "slot.combine_arrow",
                    "slot.regrouped_models",
                ),
            ),
            Region(
                id="region.answer",
                role="answer",
                flow="absolute",
                slot_ids=(
                    "slot.answer_1",
                    "slot.answer_2",
                    "slot.answer_3",
                    "slot.answer_4",
                ),
            ),
        ),
        slots=(
            TextBoxSlot(
                id="slot.question",
                x=28,
                y=18,
                width=844,
                height=66,
                text=(
                    "병현이네 학교 도서관에 위인전이 599권, 동화책이 837권 있습니다. "
                    "모두 몇 권의 책이 있는지 수 모형으로 알아보시오."
                ),
                font_size=22,
                font_family="Noto Sans KR",
                fill="#202124",
                align="left",
                valign="middle",
            ),
            *BASE_TEN_MODEL_SLOTS,
            TextBoxSlot(
                id="slot.model_legend",
                x=30,
                y=98,
                width=840,
                height=38,
                text="천 모형  ▰     백 모형  ▣     십 모형  ▮     낱개 모형  ●",
                font_size=19,
                font_family="Noto Sans KR",
                fill="#4B5563",
                align="left",
                valign="middle",
                transform="translate(1000 0)",
            ),
            TextBoxSlot(
                id="slot.first_number_label",
                x=30,
                y=146,
                width=90,
                height=42,
                text="599",
                font_size=28,
                font_family="Noto Sans KR",
                fill="#202124",
                align="center",
                valign="middle",
                transform="translate(1000 0)",
            ),
            TextBoxSlot(
                id="slot.first_number_models",
                x=125,
                y=140,
                width=730,
                height=54,
                text=(
                    "백 모형 5개     십 모형 9개     낱개 모형 9개"
                ),
                font_size=22,
                font_family="Noto Sans KR",
                fill="#202124",
                align="left",
                valign="middle",
                transform="translate(1000 0)",
            ),
            TextBoxSlot(
                id="slot.second_number_label",
                x=30,
                y=204,
                width=90,
                height=42,
                text="+ 837",
                font_size=28,
                font_family="Noto Sans KR",
                fill="#202124",
                align="center",
                valign="middle",
                transform="translate(1000 0)",
            ),
            TextBoxSlot(
                id="slot.second_number_models",
                x=125,
                y=198,
                width=730,
                height=54,
                text=(
                    "백 모형 8개     십 모형 3개     낱개 모형 7개"
                ),
                font_size=22,
                font_family="Noto Sans KR",
                fill="#202124",
                align="left",
                valign="middle",
                transform="translate(1000 0)",
            ),
            TextBoxSlot(
                id="slot.combine_arrow",
                x=30,
                y=266,
                width=840,
                height=52,
                text="↓  같은 자리의 수 모형끼리 더하고 10개씩 묶어 윗자리로 바꿉니다.",
                font_size=21,
                font_family="Noto Sans KR",
                fill="#4B5563",
                align="center",
                valign="middle",
                transform="translate(1000 0)",
            ),
            TextBoxSlot(
                id="slot.regrouped_models",
                x=30,
                y=326,
                width=840,
                height=62,
                text=(
                    "천 모형 1개     백 모형 4개     십 모형 3개     낱개 모형 6개"
                ),
                font_size=24,
                font_family="Noto Sans KR",
                fill="#202124",
                align="center",
                valign="middle",
                transform="translate(1000 0)",
            ),
            TextBoxSlot(
                id="slot.answer_1",
                x=28,
                y=470,
                width=844,
                height=42,
                text=(
                    "(1) 낱개 모형끼리 더하면 십 모형 (   )개와 "
                    "낱개 모형 (   )개입니다."
                ),
                font_size=21,
                font_family="Noto Sans KR",
                fill="#202124",
                align="left",
                valign="middle",
            ),
            TextBoxSlot(
                id="slot.answer_2",
                x=28,
                y=516,
                width=844,
                height=42,
                text=(
                    "(2) 십 모형끼리 더하면 백 모형 (   )개와 "
                    "십 모형 (   )개입니다."
                ),
                font_size=21,
                font_family="Noto Sans KR",
                fill="#202124",
                align="left",
                valign="middle",
            ),
            TextBoxSlot(
                id="slot.answer_3",
                x=28,
                y=562,
                width=844,
                height=42,
                text=(
                    "(3) 백 모형끼리 더하면 천 모형 (   )개와 "
                    "백 모형 (   )개입니다."
                ),
                font_size=21,
                font_family="Noto Sans KR",
                fill="#202124",
                align="left",
                valign="middle",
            ),
            TextBoxSlot(
                id="slot.answer_4",
                x=28,
                y=608,
                width=844,
                height=42,
                text="(4) 도서관의 책 수는 모두 (     )권입니다.",
                font_size=21,
                font_family="Noto Sans KR",
                fill="#202124",
                align="left",
                valign="middle",
            ),
        ),
    )


PROBLEM_TEMPLATE = build_problem_template()


SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multi_answer_base_ten_model_addition",
    "metadata": {
        "grade": 3,
        "semester": 1,
        "subject": "수학",
        "topic": "받아올림이 두 번 있는 세 자리 수의 덧셈",
        "language": "ko-KR",
    },
    "domain": {
        "objects": [
            {
                "id": "place.school_library",
                "type": "place",
                "label": "병현이네 학교 도서관",
            },
            {
                "id": "book.biography",
                "type": "book_collection",
                "label": "위인전",
                "count": 599,
                "unit": "권",
            },
            {
                "id": "book.fairy_tale",
                "type": "book_collection",
                "label": "동화책",
                "count": 837,
                "unit": "권",
            },
            {
                "id": "model.ones_before_regrouping",
                "type": "base_ten_model_group",
                "label": "더한 낱개 모형",
                "place": "ones",
                "count": 16,
            },
            {
                "id": "model.ones_regrouped_tens",
                "type": "base_ten_model_group",
                "label": "낱개 모형에서 바꾼 십 모형",
                "place": "tens",
                "count": 1,
            },
            {
                "id": "model.ones_remaining",
                "type": "base_ten_model_group",
                "label": "남은 낱개 모형",
                "place": "ones",
                "count": 6,
            },
            {
                "id": "model.tens_before_regrouping",
                "type": "base_ten_model_group",
                "label": "받아올림을 포함하여 더한 십 모형",
                "place": "tens",
                "count": 13,
            },
            {
                "id": "model.tens_regrouped_hundreds",
                "type": "base_ten_model_group",
                "label": "십 모형에서 바꾼 백 모형",
                "place": "hundreds",
                "count": 1,
            },
            {
                "id": "model.tens_remaining",
                "type": "base_ten_model_group",
                "label": "남은 십 모형",
                "place": "tens",
                "count": 3,
            },
            {
                "id": "model.hundreds_before_regrouping",
                "type": "base_ten_model_group",
                "label": "받아올림을 포함하여 더한 백 모형",
                "place": "hundreds",
                "count": 14,
            },
            {
                "id": "model.hundreds_regrouped_thousands",
                "type": "base_ten_model_group",
                "label": "백 모형에서 바꾼 천 모형",
                "place": "thousands",
                "count": 1,
            },
            {
                "id": "model.hundreds_remaining",
                "type": "base_ten_model_group",
                "label": "남은 백 모형",
                "place": "hundreds",
                "count": 4,
            },
            {
                "id": "book.total",
                "type": "book_collection",
                "label": "도서관에 있는 전체 책",
                "count": 1436,
                "unit": "권",
            },
        ],
        "relations": [
            {
                "id": "relation.biography_in_library",
                "type": "located_in",
                "subject": "book.biography",
                "object": "place.school_library",
            },
            {
                "id": "relation.fairy_tale_in_library",
                "type": "located_in",
                "subject": "book.fairy_tale",
                "object": "place.school_library",
            },
            {
                "id": "relation.total_books_sum",
                "type": "sum_of",
                "subject": "book.total",
                "objects": [
                    "book.biography",
                    "book.fairy_tale",
                ],
            },
            {
                "id": "relation.ones_regrouping",
                "type": "regroup",
                "subject": "model.ones_before_regrouping",
                "result": [
                    "model.ones_regrouped_tens",
                    "model.ones_remaining",
                ],
            },
            {
                "id": "relation.tens_regrouping",
                "type": "regroup",
                "subject": "model.tens_before_regrouping",
                "result": [
                    "model.tens_regrouped_hundreds",
                    "model.tens_remaining",
                ],
            },
            {
                "id": "relation.hundreds_regrouping",
                "type": "regroup",
                "subject": "model.hundreds_before_regrouping",
                "result": [
                    "model.hundreds_regrouped_thousands",
                    "model.hundreds_remaining",
                ],
            },
        ],
    },
    "answer": {
        "value": [1, 6, 1, 3, 1, 4, 1436],
        "unit": "",
        "expression": "599 + 837 = 1436",
        "items": [
            {
                "id": "answer.ones_to_tens",
                "value": 1,
                "unit": "개",
            },
            {
                "id": "answer.remaining_ones",
                "value": 6,
                "unit": "개",
            },
            {
                "id": "answer.tens_to_hundreds",
                "value": 1,
                "unit": "개",
            },
            {
                "id": "answer.remaining_tens",
                "value": 3,
                "unit": "개",
            },
            {
                "id": "answer.hundreds_to_thousands",
                "value": 1,
                "unit": "개",
            },
            {
                "id": "answer.remaining_hundreds",
                "value": 4,
                "unit": "개",
            },
            {
                "id": "answer.total_books",
                "value": 1436,
                "unit": "권",
            },
        ],
    },
}

SEMANTIC_OVERRIDE = SEMANTIC


SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": PROBLEM_ID,
    "problem_type": "multi_answer_base_ten_model_addition",
    "inputs": {
        "target_label": "수 모형을 다시 묶은 결과와 도서관의 전체 책 수",
        "unit": "",
        "answer_type": "mixed_integer_list",
        "quantities": {
            "biography_count": 599,
            "fairy_tale_count": 837,
            "ones_from_biographies": 9,
            "ones_from_fairy_tales": 7,
            "tens_from_biographies": 9,
            "tens_from_fairy_tales": 3,
            "hundreds_from_biographies": 5,
            "hundreds_from_fairy_tales": 8,
        },
        "conditions": [
            "위인전 599권은 백 모형 5개, 십 모형 9개, 낱개 모형 9개로 나타냅니다.",
            "동화책 837권은 백 모형 8개, 십 모형 3개, 낱개 모형 7개로 나타냅니다.",
            "낱개 모형 10개는 십 모형 1개로 바꿉니다.",
            "십 모형 10개는 백 모형 1개로 바꿉니다.",
            "백 모형 10개는 천 모형 1개로 바꿉니다.",
        ],
    },
    "given": [
        {
            "ref": "book.biography",
            "value": {
                "count": 599,
                "unit": "권",
                "place_values": {
                    "hundreds": 5,
                    "tens": 9,
                    "ones": 9,
                },
            },
        },
        {
            "ref": "book.fairy_tale",
            "value": {
                "count": 837,
                "unit": "권",
                "place_values": {
                    "hundreds": 8,
                    "tens": 3,
                    "ones": 7,
                },
            },
        },
    ],
    "target": {
        "ref": "answer.base_ten_regrouping_and_total",
        "type": "mixed_integer_list",
    },
    "method": (
        "같은 자리의 수 모형끼리 더한 뒤, 모형 10개를 "
        "바로 윗자리 모형 1개로 바꾼다."
    ),
    "plan": [
        "두 수의 낱개 모형을 더하고 10개를 십 모형으로 바꾼다.",
        "두 수의 십 모형과 낱개 자리에서 바꾼 십 모형을 더한다.",
        "십 모형 10개를 백 모형으로 바꾼다.",
        "두 수의 백 모형과 십의 자리에서 바꾼 백 모형을 더한다.",
        "백 모형 10개를 천 모형으로 바꾼다.",
        "천, 백, 십, 낱개 모형의 수를 차례대로 읽어 전체 책 수를 구한다.",
    ],
    "steps": [
        {
            "id": "step.add_ones",
            "expr": "9 + 7",
            "value": 16,
            "explanation": "낱개 모형 9개와 7개를 더하면 16개입니다.",
        },
        {
            "id": "step.regroup_ones",
            "expr": "16 = 1 * 10 + 6",
            "value": {
                "tens_models": 1,
                "ones_models": 6,
            },
            "explanation": "낱개 모형 16개는 십 모형 1개와 낱개 모형 6개입니다.",
        },
        {
            "id": "step.add_tens",
            "expr": "9 + 3 + 1",
            "value": 13,
            "explanation": (
                "십 모형 9개와 3개에 낱개 자리에서 바꾼 "
                "십 모형 1개를 더하면 13개입니다."
            ),
        },
        {
            "id": "step.regroup_tens",
            "expr": "13 = 1 * 10 + 3",
            "value": {
                "hundreds_models": 1,
                "tens_models": 3,
            },
            "explanation": "십 모형 13개는 백 모형 1개와 십 모형 3개입니다.",
        },
        {
            "id": "step.add_hundreds",
            "expr": "5 + 8 + 1",
            "value": 14,
            "explanation": (
                "백 모형 5개와 8개에 십의 자리에서 바꾼 "
                "백 모형 1개를 더하면 14개입니다."
            ),
        },
        {
            "id": "step.regroup_hundreds",
            "expr": "14 = 1 * 10 + 4",
            "value": {
                "thousands_models": 1,
                "hundreds_models": 4,
            },
            "explanation": "백 모형 14개는 천 모형 1개와 백 모형 4개입니다.",
        },
        {
            "id": "step.compose_total",
            "expr": "1000 + 400 + 30 + 6",
            "value": 1436,
            "explanation": (
                "천 모형 1개, 백 모형 4개, 십 모형 3개, "
                "낱개 모형 6개이므로 모두 1436권입니다."
            ),
        },
    ],
    "checks": [
        {
            "id": "check.ones_regrouping",
            "expr": "9 + 7 == 1 * 10 + 6",
            "expected": True,
            "actual": True,
            "pass": True,
        },
        {
            "id": "check.tens_regrouping",
            "expr": "9 + 3 + 1 == 1 * 10 + 3",
            "expected": True,
            "actual": True,
            "pass": True,
        },
        {
            "id": "check.hundreds_regrouping",
            "expr": "5 + 8 + 1 == 1 * 10 + 4",
            "expected": True,
            "actual": True,
            "pass": True,
        },
        {
            "id": "check_place_value_total",
            "expr": "1 * 1000 + 4 * 100 + 3 * 10 + 6",
            "expected": 1436,
            "actual": 1436,
            "pass": True,
        },
        {
            "id": "check_total_addition",
            "expr": "599 + 837",
            "expected": 1436,
            "actual": 1436,
            "pass": True,
        },
        {
            "id": "check_inverse_operation",
            "expr": "1436 - 837",
            "expected": 599,
            "actual": 599,
            "pass": True,
        },
    ],
    "answer": {
        "value": [1, 6, 1, 3, 1, 4, 1436],
        "unit": "",
        "expression": "599 + 837 = 1436",
        "items": [
            {
                "id": "answer.ones_to_tens",
                "value": 1,
                "unit": "개",
            },
            {
                "id": "answer.remaining_ones",
                "value": 6,
                "unit": "개",
            },
            {
                "id": "answer.tens_to_hundreds",
                "value": 1,
                "unit": "개",
            },
            {
                "id": "answer.remaining_tens",
                "value": 3,
                "unit": "개",
            },
            {
                "id": "answer.hundreds_to_thousands",
                "value": 1,
                "unit": "개",
            },
            {
                "id": "answer.remaining_hundreds",
                "value": 4,
                "unit": "개",
            },
            {
                "id": "answer.total_books",
                "value": 1436,
                "unit": "권",
            },
        ],
    },
}

SEMANTIC_ANSWER = SOLVABLE["answer"]
