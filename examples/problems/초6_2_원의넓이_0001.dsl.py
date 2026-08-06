from __future__ import annotations

from modu_math.dsl import Canvas, LineSlot, PathSlot, ProblemTemplate, Region


PROBLEM_TEMPLATE = ProblemTemplate(
    id="circle_area_0001",
    title="Circle radius helper guard",
    canvas=Canvas(width=720, height=420, coordinate_mode="logical"),
    regions=(
        Region(
            id="region.diagram",
            role="diagram",
            flow="absolute",
            slot_ids=("slot.radius_10_line", "slot.radius_10_arc"),
        ),
    ),
    slots=(
        LineSlot(
            id="slot.radius_10_line",
            prompt="",
            x1=250.0,
            y1=120.0,
            x2=250.0,
            y2=260.0,
            stroke="#111111",
            stroke_width=2.0,
        ),
        PathSlot(
            id="slot.radius_10_arc",
            prompt="",
            d="M 248 130 Q 292 190 252 250",
            fill="none",
            stroke="#111111",
            stroke_width=2.0,
        ),
    ),
)
