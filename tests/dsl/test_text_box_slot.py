from modu_math.dsl import Canvas, ProblemTemplate, Region, TextBoxSlot, TextSlot, compile_problem_template_to_layout
from modu_math.layout.validate import validate_layout_json
from modu_math.renderer.compiler import compile_renderer_json
from modu_math.renderer.svg.render import render_svg
from modu_math.renderer.validate import validate_renderer_json


def test_text_box_slot_renders_fixed_box_metadata() -> None:
    problem = ProblemTemplate(
        id="text_box_demo",
        title="Text box demo",
        canvas=Canvas(width=300, height=120),
        regions=(Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.tb",)),),
        slots=(
            TextBoxSlot(
                id="slot.tb",
                text="가나다 라마바사",
                x=10,
                y=20,
                width=120,
                height=50,
                font_size=20,
                align="center",
            ),
        ),
    )

    layout = compile_problem_template_to_layout(problem)
    validate_layout_json(layout)
    assert layout["slots"][0]["kind"] == "text_box"
    assert layout["slots"][0]["content"]["width"] == 120.0

    renderer = compile_renderer_json(layout)
    validate_renderer_json(renderer)
    assert renderer["elements"][0]["type"] == "text_box"

    svg = render_svg(renderer)
    assert 'data-slot-kind="text_box"' in svg
    assert 'data-box-width="120"' in svg
    assert 'text-anchor="middle"' in svg


def test_text_slot_max_width_does_not_auto_wrap() -> None:
    problem = ProblemTemplate(
        id="text_no_wrap_demo",
        title="Text no wrap demo",
        canvas=Canvas(width=300, height=120),
        regions=(Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.text",)),),
        slots=(
            TextSlot(
                id="slot.text",
                text="long text should stay on one rendered line",
                x=10,
                y=20,
                font_size=20,
                max_width=30,
            ),
        ),
    )

    svg = render_svg(compile_renderer_json(compile_problem_template_to_layout(problem)))

    assert "<tspan" not in svg
    assert "long text should stay on one rendered line" in svg
