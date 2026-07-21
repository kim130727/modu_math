from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    CircleSlot,
    LineSlot,
    PolygonSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextSlot,
)


BLUE = "#1d6fa3"
LIGHT_BLUE = "#5cc6ee"
MID_BLUE = "#35abd8"
PALE_BLUE = "#94dcf6"
ARROW_GRAY = "#8a8a8a"


def _ten_rod(slot_id: str, x: float, y: float, *, cell: float = 8.0) -> tuple:
    width = cell * 1.35
    height = cell * 10
    depth = cell * 0.45
    slots = [
        RectSlot(
            id=f"{slot_id}.front",
            x=x,
            y=y + depth,
            width=width,
            height=height,
            fill=LIGHT_BLUE,
            stroke=BLUE,
            stroke_width=1.2,
        ),
        PolygonSlot(
            id=f"{slot_id}.top",
            points=((x, y + depth), (x + depth, y), (x + width + depth, y), (x + width, y + depth)),
            fill=PALE_BLUE,
            stroke=BLUE,
            stroke_width=1.0,
        ),
        PolygonSlot(
            id=f"{slot_id}.side",
            points=(
                (x + width, y + depth),
                (x + width + depth, y),
                (x + width + depth, y + height),
                (x + width, y + height + depth),
            ),
            fill=MID_BLUE,
            stroke=BLUE,
            stroke_width=1.0,
        ),
    ]
    for index in range(1, 10):
        yy = y + depth + cell * index
        slots.append(
            LineSlot(
                id=f"{slot_id}.cell.{index}",
                x1=x,
                y1=yy,
                x2=x + width,
                y2=yy,
                stroke=BLUE,
                stroke_width=0.7,
            )
        )
    return tuple(slots)


def _one_cube(slot_id: str, x: float, y: float, *, size: float = 11.0) -> tuple:
    depth = size * 0.45
    return (
        RectSlot(
            id=f"{slot_id}.front",
            x=x,
            y=y + depth,
            width=size,
            height=size,
            fill=LIGHT_BLUE,
            stroke=BLUE,
            stroke_width=1.0,
        ),
        PolygonSlot(
            id=f"{slot_id}.top",
            points=((x, y + depth), (x + depth, y), (x + size + depth, y), (x + size, y + depth)),
            fill=PALE_BLUE,
            stroke=BLUE,
            stroke_width=0.9,
        ),
        PolygonSlot(
            id=f"{slot_id}.side",
            points=(
                (x + size, y + depth),
                (x + size + depth, y),
                (x + size + depth, y + size),
                (x + size, y + size + depth),
            ),
            fill=MID_BLUE,
            stroke=BLUE,
            stroke_width=0.9,
        ),
    )


def _base_ten_model(
    slot_id: str,
    x: float,
    y: float,
    *,
    rods: int,
    ones: int,
    rod_gap: float = 24.0,
    cube_x_offset: float = 158.0,
    cube_gap_x: float = 25.0,
    cube_gap_y: float = 21.0,
    rod_cell: float = 8.0,
    cube_size: float = 11.0,
) -> tuple:
    slots: list = []
    for index in range(rods):
        slots.extend(_ten_rod(f"{slot_id}.rod.{index + 1}", x + index * rod_gap, y, cell=rod_cell))

    for index in range(ones):
        # A 5-by-4 staggered stack mirrors the printed base-ten blocks better
        # than a plain rectangular grid.
        col = 0 if index < 5 else 1
        row = index if index < 5 else index - 5
        cube_x = x + cube_x_offset + col * cube_gap_x
        cube_y = y + row * cube_gap_y + (0 if col == 0 else cube_gap_y * 0.8)
        slots.extend(_one_cube(f"{slot_id}.cube.{index + 1}", cube_x, cube_y, size=cube_size))
    return tuple(slots)


def _partition_box(slot_id: str, x: float, y: float) -> tuple:
    return (
        RectSlot(
            id=f"{slot_id}.box",
            x=x,
            y=y,
            width=98,
            height=126,
            fill="none",
            stroke=BLUE,
            stroke_width=1.5,
        ),
        *_base_ten_model(
            slot_id,
            x + 18,
            y + 12,
            rods=2,
            ones=3,
            rod_gap=25,
            cube_x_offset=56,
            cube_gap_x=0,
            cube_gap_y=21,
            rod_cell=8.5,
            cube_size=11,
        ),
    )


def _choice(slot_id: str, number: str, value: str, x: float, y: float) -> tuple:
    return (
        TextSlot(
            id=f"{slot_id}.marker",
            text=number,
            style_role="choice",
            x=x,
            y=y,
            font_size=21,
            fill="#0070c0",
        ),
        TextSlot(
            id=f"{slot_id}.value",
            text=value,
            style_role="choice",
            x=x + 24,
            y=y,
            font_size=24,
        ),
    )


def _all_slot_ids(slots: tuple) -> tuple[str, ...]:
    return tuple(slot.id for slot in slots)


def build_problem_template() -> ProblemTemplate:
    diagram_slots = (
        RectSlot(id="slot.top.box", x = 190, y = 55, width = 245, height = 125, fill="none", stroke=BLUE, stroke_width=1.5),
        *_base_ten_model(
            "slot.figure.top",
            x = ((389) + (-135.0)) + (-45.0), y = (67) + (5.0), rods=6,
            ones=9,
            rod_gap=26,
            cube_x_offset=155,
            cube_gap_x=25,
            cube_gap_y=20,
        ),
        LineSlot(id="slot.arrow.stem", x1 = 315, y1 = 185, x2 = 315, y2 = 210, stroke=ARROW_GRAY, stroke_width=10),
        PolygonSlot(
            id="slot.arrow.head",
            points = [[300.9399108886719, 200.32200622558594], [326.9399108886719, 200.32200622558594], [313.9399108886719, 215.32200622558594]], fill = '#8a8a8a', stroke = '#8a8a8a', stroke_width = 1),
        *_partition_box("slot.figure.group1", x = (315) + (-180.0), y = (225) + (5.0)),
        *_partition_box("slot.figure.group2", x = ((435) + (-75.0)) + (-85.0), y = (225) + (5.0)),
        *_partition_box("slot.figure.group3", x = (555) + (-135.0), y = (225) + (5.0)),
        TextSlot(id="slot.equation", text = '69 ÷ 3 =', style_role="question", x = 250, y = 415, font_size = 25),
        RectSlot(id="slot.blank", x = 360, y = 390, width = 25, height = 25, fill="none", stroke="#111111", stroke_width=1.2),
    )
    choice_slots = (
        *_choice("slot.choice.1", "①", "21", 150, 470),
        *_choice("slot.choice.2", "②", "22", 300, 470),
        *_choice("slot.choice.3", "③", "23", 450, 470),
        *_choice("slot.choice.4", "④", "24", 150, 510),
        *_choice("slot.choice.5", "⑤", "25", 300, 510),
    )
    answer_slots = (
        
        
    )
    stem_slots = (
        TextSlot(id="slot.question.prefix", text="수 모형을 보고", style_role="question", x=62, y=29, font_size=25),
        RectSlot(id="slot.inline_blank", x = 233, y = 7, width=27, height=27, fill="none", stroke="#111111", stroke_width=1.0),
        TextSlot(id="slot.question.suffix", text="안에 알맞은 수를 고르세요.", style_role="question", x = 269, y = 29, font_size=25),
    )
    all_slots = (*stem_slots, *diagram_slots, *choice_slots, *answer_slots)

    return ProblemTemplate(
        id="S3_초등_3_008631",
        title="수 모형을 보고 알맞은 수 고르기",
        canvas=Canvas(width=720, height=590, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=_all_slot_ids(stem_slots)),
            Region(id="region.diagram", role="diagram", flow="absolute", slot_ids=_all_slot_ids(diagram_slots)),
            Region(id="region.choices", role="choices", flow="absolute", slot_ids=_all_slot_ids(choice_slots)),
            Region(id="region.answer", role="answer", flow="absolute", slot_ids=_all_slot_ids(answer_slots)),
        ),
        slots=all_slots,
        diagrams=(),
        groups=(),
        constraints=(),
        tags=("base_ten_model", "division", "multiple_choice"),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008631",
    "problem_type": "multiple_choice_division",
    "metadata": {
        "language": "ko",
        "question": "수 모형을 보고 □ 안에 알맞은 수를 고르세요.",
        "instruction": "69를 3묶음으로 나눈 수 모형을 보고 69 ÷ 3의 몫을 고르는 문제",
    },
    "domain": {
        "objects": [
            {"id": "obj.dividend", "type": "number", "value": 69},
            {"id": "obj.divisor", "type": "number", "value": 3},
            {"id": "obj.blank", "type": "answer_blank"},
            {"id": "obj.options", "type": "choices", "values": [21, 22, 23, 24, 25]},
            {"id": "obj.base_ten.total", "type": "base_ten_model", "tens": 6, "ones": 9},
            {"id": "obj.base_ten.group", "type": "base_ten_model", "tens": 2, "ones": 3, "count": 3},
        ],
        "relations": [
            {"id": "rel.division", "type": "division", "dividend": 69, "divisor": 3, "quotient": 23},
            {"id": "rel.partition", "type": "equal_partition", "total": 69, "parts": 3, "part_value": 23},
        ],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.dividend", "obj.divisor", "obj.options", "obj.base_ten.total"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.division", "rel.partition"],
            },
            "plan": {
                "method": "division_value_selection",
                "description": "69를 3으로 나눈 몫을 구해 보기 중 같은 값을 고른다.",
            },
            "execute": {"expected_operations": ["compute_69_div_3", "match_option_23"]},
            "review": {"check_methods": ["division_inverse_check", "base_ten_partition_check", "option_match_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "division_quotient", "description": "69 ÷ 3의 몫"},
        "value": 23,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008631",
    "problem_type": "multiple_choice_division",
    "inputs": {
        "total_ticks": 69,
        "target_label": "몫",
        "target_ticks": 3,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.dividend", "value": 69},
        {"ref": "obj.divisor", "value": 3},
        {"ref": "obj.options", "value": [21, 22, 23, 24, 25]},
    ],
    "target": {"ref": "answer.target", "type": "division_quotient"},
    "method": "division_value_selection",
    "plan": ["69를 3으로 나눈 몫을 구한다.", "보기 중 계산 결과와 같은 수를 찾는다."],
    "steps": [
        {"id": "step.1", "expr": "69 ÷ 3", "value": 23},
        {"id": "step.2", "expr": "보기에서 23 찾기", "value": 3},
    ],
    "checks": [
        {"id": "check.1", "expr": "23 × 3 = 69", "expected": 69, "actual": 69, "pass": True}
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "division_quotient", "description": "69 ÷ 3의 몫"},
        "value": 23,
        "unit": "",
    },
}
