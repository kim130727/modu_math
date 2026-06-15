from __future__ import annotations

from modu_math.dsl import Canvas, CircleSlot, LineSlot, ProblemTemplate, RectSlot, Region, TextSlot


PROBLEM_ID = "S3_초등_3_008670"
GRID_BLUE = "#1EA7FF"
BLACK = "#222222"
CELL = 20.0
GRID_COLS = 24
GRID_ROWS = 8
GRID_W = GRID_COLS * CELL
GRID_H = GRID_ROWS * CELL


def grid_slots(prefix: str, x: float, y: float) -> tuple:
    slots = [
        RectSlot(
            id=f"{prefix}.box",
            prompt="",
            x=x,
            y=y,
            width=GRID_W,
            height=GRID_H,
            fill="none",
            stroke=GRID_BLUE,
            stroke_width=2.0,
        )
    ]
    for col in range(1, GRID_COLS):
        gx = x + col * CELL
        slots.append(
            LineSlot(
                id=f"{prefix}.grid.v{col}",
                prompt="",
                x1=gx,
                y1=y,
                x2=gx,
                y2=y + GRID_H,
                stroke=GRID_BLUE,
                stroke_width=1.0,
            )
        )
    for row in range(1, GRID_ROWS):
        gy = y + row * CELL
        slots.append(
            LineSlot(
                id=f"{prefix}.grid.h{row}",
                prompt="",
                x1=x,
                y1=gy,
                x2=x + GRID_W,
                y2=gy,
                stroke=GRID_BLUE,
                stroke_width=1.0,
            )
        )
    return tuple(slots)


def circle_pair_slots(prefix: str, x: float, y: float, items: tuple[tuple[int, int, str], ...]) -> tuple:
    slots = []
    for idx, (grid_x, grid_y, color) in enumerate(items, start=1):
        cx = x + grid_x * CELL
        cy = y + grid_y * CELL
        slots.extend(
            [
                CircleSlot(
                    id=f"{prefix}.c{idx}.r3",
                    prompt="",
                    cx=cx,
                    cy=cy,
                    r=3 * CELL,
                    fill="none",
                    stroke=color,
                    stroke_width=2.2,
                ),
                CircleSlot(
                    id=f"{prefix}.c{idx}.r1",
                    prompt="",
                    cx=cx,
                    cy=cy,
                    r=CELL,
                    fill="none",
                    stroke=color,
                    stroke_width=2.2,
                ),
            ]
        )
    return tuple(slots)


TOP1_X = 70.0
TOP1_Y = 95.0
TOP2_X = 70.0
TOP2_Y = 305.0

TOP1_CIRCLES = (
    (4, 4, BLACK),
    (8, 4, BLACK),
    (12, 4, BLACK),
    (15, 4, GRID_BLUE),
    (18, 4, GRID_BLUE),
)
TOP2_CIRCLES = (
    (4, 4, BLACK),
    (8, 4, BLACK),
    (12, 4, BLACK),
    (16, 4, GRID_BLUE),
    (20, 4, GRID_BLUE),
)

TOP1_SLOT_IDS = tuple(slot.id for slot in grid_slots("slot.top1", TOP1_X, TOP1_Y)) + tuple(
    slot.id for slot in circle_pair_slots("slot.top1", TOP1_X, TOP1_Y, TOP1_CIRCLES)
)
TOP2_SLOT_IDS = tuple(slot.id for slot in grid_slots("slot.top2", TOP2_X, TOP2_Y)) + tuple(
    slot.id for slot in circle_pair_slots("slot.top2", TOP2_X, TOP2_Y, TOP2_CIRCLES)
)


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id=PROBLEM_ID,
        title="규칙에 따라 원을 4개 더 그리기",
        canvas=Canvas(width=640, height=520, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q1",),
            ),
            Region(
                id="region.diagram.top1",
                role="diagram",
                flow="absolute",
                slot_ids=TOP1_SLOT_IDS,
            ),
            Region(
                id="region.diagram.top2",
                role="diagram",
                flow="absolute",
                slot_ids=TOP2_SLOT_IDS,
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="규칙에 따라 원을 4개 더 그리려고 합니다. 바르게 그린 것을 선택하세요.",
                style_role="question",
                x=35.0,
                y=42.0,
                font_size=24,
                max_width=560,
            ),
            CircleSlot(
                id="slot.pt.center", prompt="", cx = 600, cy = 195, r = 5, fill="#ff2aa1"
            ),
            *grid_slots("slot.top1", TOP1_X, TOP1_Y),
            *circle_pair_slots("slot.top1", TOP1_X, TOP1_Y, TOP1_CIRCLES),
            *grid_slots("slot.top2", TOP2_X, TOP2_Y),
            *circle_pair_slots("slot.top2", TOP2_X, TOP2_Y, TOP2_CIRCLES),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": PROBLEM_ID,
    "problem_type": "pattern_selection",
    "metadata": {
        "language": "ko",
        "question": "규칙에 따라 원을 4개 더 그리려고 합니다. 바르게 그린 것을 선택하세요.",
        "instruction": "두 모눈 그림만 제시한다.",
    },
    "domain": {
        "objects": [
            {"id": "obj.top1", "type": "concentric_circle_pattern"},
            {"id": "obj.top2", "type": "concentric_circle_pattern"},
            {
                "id": "obj.rule",
                "type": "pattern_rule",
                "description": "반지름 1과 3인 동심원을 같은 높이에 배치하고, 새로 그린 파란 원의 위치를 비교한다.",
            },
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.top1", "obj.top2", "obj.rule"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.pattern_applies"],
            },
            "plan": {
                "method": "pattern_matching",
                "description": "검은 원의 간격 규칙에 맞게 파란 원 2개가 이어졌는지 비교한다.",
            },
            "execute": {"expected_operations": ["compare_circle_positions"]},
            "review": {"check_methods": ["rule_consistency_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "correct_choice", "description": "규칙에 맞게 이어 그린 그림"},
        "value": 2,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": PROBLEM_ID,
    "problem_type": "pattern_selection",
    "inputs": {
        "total_ticks": 4,
        "target_label": "바르게 그린 것",
        "target_ticks": 4,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {
            "ref": "obj.rule",
            "value": {
                "description": "첫 그림은 파란 원이 (14,4), (18,4)에 있고, 두 번째 그림은 (16,4), (20,4)에 있다."
            },
        }
    ],
    "target": {"ref": "answer.target", "type": "correct_choice"},
    "plan": ["검은 원이 (4,4), (8,4), (12,4)에 놓였으므로 4칸 간격으로 이어지는 그림을 찾는다."],
    "method": "pattern_matching",
    "steps": [
        {"id": "step.1", "expr": "검은 원의 x좌표 간격 확인", "value": 4},
        {"id": "step.2", "expr": "다음 두 위치는 (16,4), (20,4)", "value": 2},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "두 번째 모눈의 파란 원이 4칸 간격을 유지한다.",
            "expected": True,
            "actual": True,
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "correct_choice", "description": "규칙에 맞게 이어 그린 그림"},
        "value": 2,
        "unit": "",
    },
}
