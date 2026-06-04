from __future__ import annotations

import json

from modu_math.dsl import (
    Arrow,
    Canvas,
    ChoiceSlot,
    Circle,
    Constraint,
    Cube,
    DiagramTemplate,
    FractionAreaModel,
    Grid,
    Group,
    LabelSlot,
    ProblemTemplate,
    Region,
    TextSlot,
    Triangle,
    compile_problem_template_to_layout,
)


def test_compile_to_layout_multiple_choice_example() -> None:
    problem = ProblemTemplate(
        id="p_mc_001",
        title="MC Example",
        canvas=Canvas(width=800, height=600),
        regions=(
            Region(id="region.stem", role="stem", slot_ids=("slot.stem",)),
            Region(id="region.choices", role="choices", slot_ids=("slot.choice",)),
        ),
        slots=(
            TextSlot(id="slot.stem", text="2 + 3 = ?"),
            ChoiceSlot(id="slot.choice", choices=("4", "5", "6"), answer_key=("5",)),
        ),
    )

    layout = compile_problem_template_to_layout(problem)

    assert layout["problem_id"] == "p_mc_001"
    assert layout["canvas"]["coordinate_mode"] == "logical"
    assert layout["regions"][0]["slot_ids"] == ["slot.stem"]
    assert layout["regions"][1]["slot_ids"] == ["slot.choice"]
    assert layout["slots"][0]["kind"] == "text"
    assert layout["slots"][1]["content"]["choices"] == ["4", "5", "6"]
    assert layout["reading_order"][:4] == [
        "region.stem",
        "slot.stem",
        "region.choices",
        "slot.choice",
    ]


def test_compile_to_layout_preserves_high_level_diagram_objects() -> None:
    diagram = DiagramTemplate(
        id="diagram.geom",
        objects=(
            Cube(id="obj.cube"),
            Triangle(id="obj.triangle", variant="isosceles"),
            Circle(id="obj.circle", mark_center=True),
            Grid(id="obj.grid", rows=3, cols=4),
            Arrow(id="obj.arrow", direction="down"),
            FractionAreaModel(id="obj.fraction", partitions=8, shaded=3),
        ),
        label_slots=(
            LabelSlot(id="slot.label", text="A", target_object_id="obj.circle"),
        ),
        constraints=(
            Constraint(id="c.align", type="align", target_ids=("obj.cube", "obj.triangle")),
        ),
    )
    problem = ProblemTemplate(
        id="p_diagram_001",
        title="Diagram Example",
        canvas=Canvas(width=640, height=360),
        regions=(Region(id="region.diagram", role="diagram"),),
        slots=(),
        diagrams=(diagram,),
    )

    layout = compile_problem_template_to_layout(problem)
    objects = layout["diagrams"][0]["objects"]

    assert [obj["object_type"] for obj in objects] == [
        "cube",
        "triangle",
        "circle",
        "grid",
        "arrow",
        "fraction_area_model",
    ]
    assert objects[1]["variant"] == "isosceles"
    assert objects[2]["mark_center"] is True
    assert layout["diagrams"][0]["constraints"][0]["type"] == "align"


def test_compile_to_layout_preserves_stable_ids() -> None:
    problem = ProblemTemplate(
        id="p_id_001",
        title="ID Example",
        canvas=Canvas(width=400, height=300),
        regions=(Region(id="region.custom", role="custom"),),
        slots=(TextSlot(id="slot.alpha", text="alpha"),),
        groups=(Group(id="group.one", member_ids=("slot.alpha",), role="custom"),),
        constraints=(Constraint(id="cons.one", type="inside", target_ids=("slot.alpha", "region.custom")),),
        diagrams=(DiagramTemplate(id="diagram.one", objects=(Circle(id="obj.one"),)),),
    )

    layout = compile_problem_template_to_layout(problem)

    assert layout["problem_id"] == "p_id_001"
    assert layout["regions"][0]["id"] == "region.custom"
    assert layout["slots"][0]["id"] == "slot.alpha"
    assert layout["groups"][0]["id"] == "group.one"
    assert layout["constraints"][0]["id"] == "cons.one"
    assert layout["diagrams"][0]["id"] == "diagram.one"
    assert layout["diagrams"][0]["objects"][0]["id"] == "obj.one"


def test_compile_to_layout_is_round_trip_safe_and_deterministic() -> None:
    problem = ProblemTemplate(
        id="p_deterministic_001",
        title="Deterministic Example",
        canvas=Canvas(width=500, height=400),
        regions=(),
        slots=(
            TextSlot(id="slot.1", text="문제"),
            ChoiceSlot(id="slot.2", choices=("1", "2"), multiple_select=False),
        ),
        diagrams=(
            DiagramTemplate(
                id="diagram.det",
                objects=(Grid(id="obj.grid", rows=2, cols=2),),
            ),
        ),
    )

    layout_a = compile_problem_template_to_layout(problem)
    layout_b = compile_problem_template_to_layout(problem)

    assert layout_a == layout_b
    assert json.dumps(layout_a, ensure_ascii=False, sort_keys=True) == json.dumps(
        layout_b,
        ensure_ascii=False,
        sort_keys=True,
    )
    assert layout_a["regions"][0]["id"] == "region.stem"
    assert layout_a["regions"][0]["slot_ids"] == ["slot.1", "slot.2"]

