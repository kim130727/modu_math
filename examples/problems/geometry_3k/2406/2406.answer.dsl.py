from __future__ import annotations
from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    Region,
    TextSlot,
    LineSlot,
    CircleSlot,
)


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="2406.answer",
        title="그림에서 x의 값을 구하시오",
        canvas=Canvas(width=1200, height=900, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem", role="stem", flow="absolute", slot_ids=("slot.q1",)
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.line.d_to_b",
                    "slot.line.d_to_c",
                    "slot.line.d_to_e",
                    "slot.line.d_to_i",
                    "slot.line.d_to_downleft",
                    "slot.line.d_to_upright",
                    "slot.line.d_to_downright",
                    "slot.pt.b",
                    "slot.pt.c",
                    "slot.pt.d",
                    "slot.pt.e",
                    "slot.pt.i",
                    "slot.lb.b",
                    "slot.lb.c",
                    "slot.lb.d",
                    "slot.lb.e",
                    "slot.lb.i",
                    "slot.ang.79",
                    "slot.ang.xm1",
                    "slot.ang.xp10",
                    "slot.ang.2x",
                ),
            ),
            Region(
                id="region.choices",
                role="choices",
                flow="absolute",
                slot_ids=("slot.choice1", "slot.choice2"),
            ),
            Region(
                id="region.answer_overlay",
                role="annotation",
                flow="absolute",
                slot_ids=("slot.answer_overlay",),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="그림에서 x의 값을 구하시오.",
                style_role="question",
                x=40.0,
                y=70.0,
                font_size=28,
            ),
            LineSlot(
                id="slot.line.d_to_b", prompt="", x1=520.0, y1=500.0, x2=360.0, y2=380.0
            ),
            LineSlot(
                id="slot.line.d_to_c", prompt="", x1=520.0, y1=500.0, x2=650.0, y2=360.0
            ),
            LineSlot(
                id="slot.line.d_to_e", prompt="", x1=520.0, y1=500.0, x2=710.0, y2=610.0
            ),
            LineSlot(
                id="slot.line.d_to_i", prompt="", x1=520.0, y1=500.0, x2=470.0, y2=650.0
            ),
            LineSlot(
                id="slot.line.d_to_downleft",
                prompt="",
                x1=520.0,
                y1=500.0,
                x2=410.0,
                y2=690.0,
            ),
            LineSlot(
                id="slot.line.d_to_upright",
                prompt="",
                x1=520.0,
                y1=500.0,
                x2=760.0,
                y2=400.0,
            ),
            LineSlot(
                id="slot.line.d_to_downright",
                prompt="",
                x1=520.0,
                y1=500.0,
                x2=790.0,
                y2=700.0,
            ),
            CircleSlot(
                id="slot.pt.b", prompt="", cx=360.0, cy=380.0, r=4.0, fill="#1f3a93"
            ),
            CircleSlot(
                id="slot.pt.c", prompt="", cx=650.0, cy=360.0, r=4.0, fill="#1f3a93"
            ),
            CircleSlot(
                id="slot.pt.d", prompt="", cx=520.0, cy=500.0, r=4.5, fill="#1f3a93"
            ),
            CircleSlot(
                id="slot.pt.e", prompt="", cx=710.0, cy=610.0, r=4.0, fill="#1f3a93"
            ),
            CircleSlot(
                id="slot.pt.i", prompt="", cx=470.0, cy=650.0, r=4.0, fill="#1f3a93"
            ),
            TextSlot(
                id="slot.lb.b",
                prompt="",
                text="B",
                style_role="label",
                x=336.0,
                y=366.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.lb.c",
                prompt="",
                text="C",
                style_role="label",
                x=662.0,
                y=344.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.lb.d",
                prompt="",
                text="D",
                style_role="label",
                x=528.0,
                y=486.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.lb.e",
                prompt="",
                text="E",
                style_role="label",
                x=722.0,
                y=624.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.lb.i",
                prompt="",
                text="I",
                style_role="label",
                x=450.0,
                y=664.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.ang.79",
                prompt="",
                text="79°",
                style_role="label",
                x=430.0,
                y=330.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.ang.xm1",
                prompt="",
                text="(x−1)°",
                style_role="label",
                x=395.0,
                y=705.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.ang.xp10",
                prompt="",
                text="(x+10)°",
                style_role="label",
                x=745.0,
                y=340.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.ang.2x",
                prompt="",
                text="2x°",
                style_role="label",
                x=755.0,
                y=710.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice1",
                prompt="",
                text="1. 68   /   2. 78   /   3. 79",
                style_role="choice",
                x=900.0,
                y=300.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice2",
                prompt="",
                text="/   4. 136",
                style_role="choice",
                x=900.0,
                y=350.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.answer_overlay",
                prompt="",
                text="정답: A (68)",
                style_role="annotation",
                x=885.0,
                y=820.0,
                font_size=28,
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()
