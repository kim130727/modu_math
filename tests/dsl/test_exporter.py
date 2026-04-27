from __future__ import annotations

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
    export_layout_to_dsl_source,
    problem_template_from_layout,
)


def _sample_problem() -> ProblemTemplate:
    return ProblemTemplate(
        id="p_export_001",
        title="도형 구조 회귀",
        canvas=Canvas(width=960, height=540),
        regions=(
            Region(id="region.stem", role="stem", flow="vertical", slot_ids=("slot.stem", "slot.choice")),
            Region(id="region.diagram", role="diagram", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(id="slot.stem", text="정육면체와 삼각형을 비교하세요.", style_role="question"),
            ChoiceSlot(id="slot.choice", choices=("정답 1", "정답 2", "정답 3"), multiple_select=False),
        ),
        groups=(
            Group(id="group.question", role="question_block", member_ids=("slot.stem", "slot.choice")),
        ),
        constraints=(
            Constraint(id="c.inside", type="inside", target_ids=("slot.stem", "region.stem"), params={"pad": "12"}),
        ),
        diagrams=(
            DiagramTemplate(
                id="diagram.main",
                objects=(
                    Cube(id="obj.cube", perspective="cabinet"),
                    Triangle(id="obj.tri", variant="isosceles"),
                    Circle(id="obj.circle", mark_center=True),
                    Grid(id="obj.grid", rows=3, cols=4),
                    Arrow(id="obj.arrow", direction="down"),
                    FractionAreaModel(id="obj.fraction", partitions=8, shaded=3, orientation="vertical"),
                ),
                label_slots=(
                    LabelSlot(id="slot.label", text="A", target_object_id="obj.circle", target_anchor="top"),
                ),
                constraints=(
                    Constraint(id="c.align", type="align", target_ids=("obj.cube", "obj.tri")),
                ),
            ),
        ),
    )


def test_exporter_roundtrip_layout_to_dsl_to_layout_is_structural() -> None:
    layout = compile_problem_template_to_layout(_sample_problem())
    source = export_layout_to_dsl_source(layout)

    namespace: dict[str, object] = {}
    exec(source, namespace)
    rebuilt = namespace["build_problem_template"]()
    assert isinstance(rebuilt, ProblemTemplate)

    regenerated_layout = compile_problem_template_to_layout(rebuilt)
    assert regenerated_layout == layout


def test_exported_dsl_is_deterministic() -> None:
    layout = compile_problem_template_to_layout(_sample_problem())
    source_a = export_layout_to_dsl_source(layout)
    source_b = export_layout_to_dsl_source(layout)
    assert source_a == source_b


def test_exporter_preserves_key_ids_and_ordering() -> None:
    layout = compile_problem_template_to_layout(_sample_problem())
    source = export_layout_to_dsl_source(layout)

    namespace: dict[str, object] = {}
    exec(source, namespace)
    rebuilt = namespace["PROBLEM_TEMPLATE"]
    assert isinstance(rebuilt, ProblemTemplate)
    regenerated_layout = compile_problem_template_to_layout(rebuilt)

    assert [region["id"] for region in regenerated_layout["regions"]] == [region["id"] for region in layout["regions"]]
    assert [slot["id"] for slot in regenerated_layout["slots"]] == [slot["id"] for slot in layout["slots"]]
    assert regenerated_layout["reading_order"] == layout["reading_order"]


def test_exporter_preserves_high_level_object_identity() -> None:
    layout = compile_problem_template_to_layout(_sample_problem())
    source = export_layout_to_dsl_source(layout)

    assert "Cube(" in source
    assert "Triangle(" in source
    assert "Circle(" in source
    assert "Grid(" in source
    assert "Arrow(" in source
    assert "FractionAreaModel(" in source

    rebuilt_template = problem_template_from_layout(layout)
    diagram_objects = rebuilt_template.diagrams[0].objects
    assert isinstance(diagram_objects[0], Cube)
    assert isinstance(diagram_objects[1], Triangle)
    assert isinstance(diagram_objects[2], Circle)
    assert isinstance(diagram_objects[3], Grid)
    assert isinstance(diagram_objects[4], Arrow)
    assert isinstance(diagram_objects[5], FractionAreaModel)
