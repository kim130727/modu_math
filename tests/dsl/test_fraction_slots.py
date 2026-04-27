from __future__ import annotations

from modu_math.dsl import Canvas, ProblemTemplate, Region, compile_problem_template_to_layout, fraction_slots


def test_fraction_slots_compiles_to_layout_slots() -> None:
    problem = ProblemTemplate(
        id="p_fraction_slots_001",
        title="fraction slots",
        canvas=Canvas(width=640, height=360),
        regions=(Region(id="region.stem", role="stem", slot_ids=("slot.eq.left.num", "slot.eq.left.bar", "slot.eq.left.den")),),
        slots=(
            *fraction_slots(
                id_prefix="slot.eq.left",
                numerator="5",
                denominator="8",
                x=48.0,
                numerator_y=533.0,
                bar_y=540.0,
                denominator_y=580.0,
                font_size=30,
                fill="#222222",
                stroke="#222222",
                stroke_width=2.2,
            ),
        ),
    )

    layout = compile_problem_template_to_layout(problem)
    slots = {slot["id"]: slot for slot in layout["slots"]}

    assert "slot.eq.left.num" in slots
    assert "slot.eq.left.bar" in slots
    assert "slot.eq.left.den" in slots

    assert slots["slot.eq.left.num"]["kind"] == "text"
    assert slots["slot.eq.left.num"]["content"]["text"] == "5"
    assert slots["slot.eq.left.den"]["content"]["text"] == "8"

    bar_geom = slots["slot.eq.left.bar"]["content"]
    assert bar_geom["x1"] == 28.0
    assert bar_geom["y1"] == 540.0
    assert bar_geom["x2"] == 68.0
    assert bar_geom["y2"] == 540.0
