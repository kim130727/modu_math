from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    CircleSlot,
    LineSlot,
    ProblemTemplate,
    Region,
    TextSlot,
)


def build_problem_template() -> ProblemTemplate:
    canvas = Canvas(
        width=720,
        height=440,
        coordinate_mode="logical",
    )
    
    # 10x10 square graph paper: origin (210, 90), step 30
    x0, y0 = 210, 90
    step = 30
    n = 10
    
    v_slot_ids = tuple(f"slot.graphpaper.v{i}" for i in range(n + 1))
    h_slot_ids = tuple(f"slot.graphpaper.h{i}" for i in range(n + 1))
    
    regions = (
        Region(
            id="region.stem",
            role="stem",
            flow="absolute",
            slot_ids=("slot.header.text",),
        ),
        Region(
            id="region.diagram",
            role="diagram",
            flow="absolute",
            slot_ids=(
                *v_slot_ids,
                *h_slot_ids,
                "slot.circle.outer",
                "slot.pt.ga",
                "slot.pt.na",
                "slot.pt.da",
                "slot.pt.ra",
                "slot.lb.ga",
                "slot.lb.na",
                "slot.lb.da",
                "slot.lb.ra",
            ),
        ),
        Region(
            id="region.answer",
            role="answer",
            flow="absolute",
            slot_ids=(),
        ),
    )
    
    grid_lines = []
    # Vertical grid lines
    for i in range(n + 1):
        x = x0 + i * step
        grid_lines.append(
            LineSlot(
                id=f"slot.graphpaper.v{i}",
                prompt="",
                x1=x,
                y1=y0,
                x2=x,
                y2=y0 + n * step,
                stroke="#0284c7",
                stroke_width=1.2,
                stroke_dasharray="4 3",
            )
        )
    # Horizontal grid lines
    for j in range(n + 1):
        y = y0 + j * step
        grid_lines.append(
            LineSlot(
                id=f"slot.graphpaper.h{j}",
                prompt="",
                x1=x0,
                y1=y,
                x2=x0 + n * step,
                y2=y,
                stroke="#0284c7",
                stroke_width=1.2,
                stroke_dasharray="4 3",
            )
        )

    slots = (
        TextSlot(
            id="slot.header.text",
            prompt="",
            text="원의 중심을 찾아 기호를 선택해 보세요.",
            style_role="question",
            x=35,
            y=35,
            font_size=26,
        ),
        *grid_lines,
        # Circle: center at grid (5, 5) -> (360, 240), radius = 4 * 30 = 120
        CircleSlot(
            id="slot.circle.outer",
            prompt="",
            cx=360,
            cy=240,
            r=120,
            fill="none",
            stroke="#111111",
            stroke_width=2,
        ),
        # Point ㄱ: grid (5, 3) -> (360, 180)
        CircleSlot(
            id="slot.pt.ga",
            prompt="",
            cx=360,
            cy=180,
            r=4,
            fill="#d81b60",
        ),
        TextSlot(
            id="slot.lb.ga",
            prompt="",
            text="ㄱ",
            style_role="label",
            x=338,
            y=172,
            font_size=22,
            fill="#111111",
        ),
        # Point ㄴ: grid (5, 5) -> (360, 240) [Actual center]
        CircleSlot(
            id="slot.pt.na",
            prompt="",
            cx=360,
            cy=240,
            r=4,
            fill="#d81b60",
        ),
        TextSlot(
            id="slot.lb.na",
            prompt="",
            text="ㄴ",
            style_role="label",
            x=338,
            y=232,
            font_size=22,
            fill="#111111",
        ),
        # Point ㄷ: grid (3, 7) -> (300, 300)
        CircleSlot(
            id="slot.pt.da",
            prompt="",
            cx=300,
            cy=300,
            r=4,
            fill="#d81b60",
        ),
        TextSlot(
            id="slot.lb.da",
            prompt="",
            text="ㄷ",
            style_role="label",
            x=278,
            y=292,
            font_size=22,
            fill="#111111",
        ),
        # Point ㄹ: grid (8, 5) -> (450, 240)
        CircleSlot(
            id="slot.pt.ra",
            prompt="",
            cx=450,
            cy=240,
            r=4,
            fill="#d81b60",
        ),
        TextSlot(
            id="slot.lb.ra",
            prompt="",
            text="ㄹ",
            style_role="label",
            x=460,
            y=232,
            font_size=22,
            fill="#111111",
        ),
    )
    
    return ProblemTemplate(
        id="S3_초등_3_008692",
        title="원의 중심을 찾아 기호를 선택해 보세요",
        canvas=canvas,
        regions=regions,
        slots=slots,
        diagrams=(),
        groups=(),
        constraints=(),
    )


PROBLEM_TEMPLATE = build_problem_template()


SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008692",
    "problem_type": "multiple_choice",
    "metadata": {
        "language": "ko",
        "question": "원의 중심을 찾아 기호를 선택해 보세요.",
        "instruction": "원의 중심을 찾아 기호를 선택해 보세요.",
    },
    "domain": {
        "objects": [
            {"id": "obj.circle", "type": "circle"},
            {"id": "obj.pt.ga", "type": "point", "symbol": "ㄱ"},
            {"id": "obj.pt.na", "type": "point", "symbol": "ㄴ"},
            {"id": "obj.pt.da", "type": "point", "symbol": "ㄷ"},
            {"id": "obj.pt.ra", "type": "point", "symbol": "ㄹ"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.circle", "obj.pt.ga", "obj.pt.na", "obj.pt.da", "obj.pt.ra"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.center"],
            },
            "plan": {
                "method": "visual_identification",
                "description": "모눈종이에서 원의 중심 위치에 해당하는 점을 찾는다.",
            },
            "execute": {
                "expected_operations": ["identify_center_point"]
            },
            "review": {"check_methods": ["grid_distance_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": ["ㄱ", "ㄴ", "ㄷ", "ㄹ"],
        "answer_key": ["ㄴ"],
        "target": {"type": "symbol_selection", "description": "원의 중심을 나타내는 기호"},
        "value": "ㄴ",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008692",
    "problem_type": "multiple_choice",
    "inputs": {
        "total_ticks": 4,
        "target_label": "원의 중심을 나타내는 기호",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.pt.ga", "value": {"symbol": "ㄱ"}},
        {"ref": "obj.pt.na", "value": {"symbol": "ㄴ"}},
        {"ref": "obj.pt.da", "value": {"symbol": "ㄷ"}},
        {"ref": "obj.pt.ra", "value": {"symbol": "ㄹ"}},
    ],
    "target": {"ref": "answer.target", "type": "symbol_selection"},
    "method": "visual_identification",
    "plan": [
        "모눈종이 위 원에서 상하좌우 거리가 같은 중심점을 찾는다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "원의 중심에 해당하는 기호를 찾는다.", "value": "ㄴ"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "점 ㄴ이 원의 중심인가",
            "expected": True,
            "actual": True,
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": ["ㄱ", "ㄴ", "ㄷ", "ㄹ"],
        "answer_key": ["ㄴ"],
        "target": {"type": "symbol_selection", "description": "원의 중심을 나타내는 기호"},
        "value": "ㄴ",
        "unit": "",
    },
}
