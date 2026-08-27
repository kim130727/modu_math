from __future__ import annotations

from modu_math.dsl import Canvas, ProblemTemplate, Region, circle_fold_sequence_slots, compile_problem_template_to_layout, fraction_slots


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


def test_circle_fold_sequence_slots_compiles_to_layout_slots() -> None:
    problem = ProblemTemplate(
        id="p_circle_fold_sequence_001",
        title="circle fold sequence",
        canvas=Canvas(width=640, height=360),
        regions=(Region(id="region.diagram", role="diagram", flow="absolute", slot_ids=("slot.fold.stage1.paper", "slot.fold.stage5.center")),),
        slots=(
            *circle_fold_sequence_slots(
                "slot.fold",
                x=60.0,
                y=180.0,
                r=42.0,
                gap=110.0,
                stages=("circle", "half", "opened_horizontal", "folded_diagonal", "opened_cross"),
            ),
        ),
    )

    layout = compile_problem_template_to_layout(problem)
    slots = {slot["id"]: slot for slot in layout["slots"]}

    assert slots["slot.fold.stage1.paper"]["kind"] == "circle"
    assert slots["slot.fold.stage3.fold_line"]["kind"] == "line"
    assert slots["slot.fold.stage5.center"]["kind"] == "circle"
    assert "slot.fold.arrow1.body" in slots


def test_fraction_override_expands_into_slots() -> None:
    from modu_math.layout.editor_overrides import apply_editor_overrides

    base_layout = {
        "id": "p_frac_test",
        "canvas": {"width": 640, "height": 360},
        "regions": [{"id": "region.stem", "role": "stem", "slot_ids": []}],
        "slots": [],
    }
    overrides = {
        "version": 1,
        "slots": {
            "slot.math.frac": {
                "text": "\\frac{13}{11}",
                "x": 200.0,
                "y": 150.0,
                "width": 60.0,
                "height": 60.0,
                "font_size": 28,
            }
        },
        "slot_regions": {"slot.math.frac": "region.stem"},
    }

    result = apply_editor_overrides(base_layout, overrides)
    slots = {s["id"]: s for s in result["slots"]}

    assert "slot.math.frac.num" in slots
    assert "slot.math.frac.bar" in slots
    assert "slot.math.frac.den" in slots
    assert slots["slot.math.frac.num"]["content"]["text"] == "13"
    assert slots["slot.math.frac.den"]["content"]["text"] == "11"
    assert slots["slot.math.frac.bar"]["kind"] == "line"


def test_mixed_fraction_override_expands_into_slots() -> None:
    from modu_math.layout.editor_overrides import apply_editor_overrides

    base_layout = {
        "id": "p_mixed_frac_test",
        "canvas": {"width": 640, "height": 360},
        "regions": [{"id": "region.stem", "role": "stem", "slot_ids": []}],
        "slots": [],
    }
    overrides = {
        "version": 1,
        "slots": {
            "slot.math.mixed": {
                "text": "7\\frac{3}{10}",
                "x": 300.0,
                "y": 200.0,
                "width": 80.0,
                "height": 60.0,
                "font_size": 30,
            }
        },
        "slot_regions": {"slot.math.mixed": "region.stem"},
    }

    result = apply_editor_overrides(base_layout, overrides)
    slots = {s["id"]: s for s in result["slots"]}

    assert "slot.math.mixed.whole" in slots
    assert "slot.math.mixed.num" in slots
    assert "slot.math.mixed.bar" in slots
    assert "slot.math.mixed.den" in slots
    assert slots["slot.math.mixed.whole"]["content"]["text"] == "7"
    assert slots["slot.math.mixed.num"]["content"]["text"] == "3"
    assert slots["slot.math.mixed.den"]["content"]["text"] == "10"


def test_fraction_override_without_text_expands_from_existing_slots() -> None:
    from modu_math.layout.editor_overrides import apply_editor_overrides

    base_layout = {
        "id": "p_frac_override_test",
        "canvas": {"width": 640, "height": 360},
        "regions": [
            {
                "id": "region.stem",
                "role": "stem",
                "slot_ids": [
                    "slot.math.fraction.num",
                    "slot.math.fraction.bar",
                    "slot.math.fraction.den",
                ],
            }
        ],
        "slots": [
            {
                "id": "slot.math.fraction.num",
                "kind": "text",
                "content": {"text": "2", "font_size": 30, "x": 260.0, "y": 240.0},
            },
            {
                "id": "slot.math.fraction.bar",
                "kind": "line",
                "content": {"x1": 240.0, "y1": 255.0, "x2": 280.0, "y2": 255.0},
            },
            {
                "id": "slot.math.fraction.den",
                "kind": "text",
                "content": {"text": "8", "font_size": 30, "x": 260.0, "y": 280.0},
            },
        ],
    }
    overrides = {
        "version": 1,
        "slots": {
            "slot.math.fraction": {
                "font_size": 36,
                "x": 254.0,
                "y": 217.0,
                "width": 43.0,
                "height": 70.0,
            }
        },
    }

    result = apply_editor_overrides(base_layout, overrides)
    slots = {s["id"]: s for s in result["slots"]}

    assert "slot.math.fraction.num" in slots
    assert "slot.math.fraction.bar" in slots
    assert "slot.math.fraction.den" in slots
    assert slots["slot.math.fraction.num"]["content"]["text"] == "2"
    assert slots["slot.math.fraction.den"]["content"]["text"] == "8"
    assert slots["slot.math.fraction.num"]["content"]["font_size"] == 36
    assert slots["slot.math.fraction.den"]["content"]["font_size"] == 36

    region_slot_ids = result["regions"][0]["slot_ids"]
    assert "slot.math.fraction.num" in region_slot_ids
    assert "slot.math.fraction.bar" in region_slot_ids
    assert "slot.math.fraction.den" in region_slot_ids


