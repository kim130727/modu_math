from modu_math.dsl import (
    BlankSlot,
    Canvas,
    ImageSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
    TextSlot,
    compile_problem_template_to_layout,
)
from modu_math.layout.validate import validate_layout_json
from modu_math.renderer.compiler import compile_renderer_json
from modu_math.renderer.svg.render import inline_local_image_hrefs, render_svg
from modu_math.renderer.validate import validate_renderer_json


def test_text_box_slot_renders_fixed_box_metadata() -> None:
    problem = ProblemTemplate(
        id="text_box_demo",
        title="Text box demo",
        canvas=Canvas(width=300, height=120),
        regions=(
            Region(
                id="region.stem", role="stem", flow="absolute", slot_ids=("slot.tb",)
            ),
        ),
        slots=(
            TextBoxSlot(
                id="slot.tb",
                text="가나다 라마바사",
                x=10,
                y=20,
                width=80,
                height=50,
                font_size=20,
                align="center",
            ),
        ),
    )

    layout = compile_problem_template_to_layout(problem)
    validate_layout_json(layout)
    assert layout["slots"][0]["kind"] == "text_box"
    assert layout["slots"][0]["content"]["width"] == 80.0

    renderer = compile_renderer_json(layout)
    validate_renderer_json(renderer)
    assert renderer["elements"][0]["type"] == "text_box"

    svg = render_svg(renderer)
    assert 'data-slot-kind="text_box"' in svg
    assert 'data-box-width="80"' in svg
    assert 'text-anchor="middle"' in svg
    assert 'data-raw-text="가나다 라마바사"' in svg


def test_text_slot_max_width_does_not_auto_wrap() -> None:
    problem = ProblemTemplate(
        id="text_no_wrap_demo",
        title="Text no wrap demo",
        canvas=Canvas(width=300, height=120),
        regions=(
            Region(
                id="region.stem", role="stem", flow="absolute", slot_ids=("slot.text",)
            ),
        ),
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
    assert 'max_width="30"' in svg
    assert ">long text should stay on one rendered line</text>" in svg


def test_answer_input_rect_uses_white_fill_even_when_authored_dark() -> None:
    problem = ProblemTemplate(
        id="answer_input_style_demo",
        title="Answer input style demo",
        canvas=Canvas(width=160, height=100),
        regions=(
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=("slot.answer_box",),
            ),
        ),
        slots=(
            RectSlot(
                id="slot.answer_box",
                x=30,
                y=40,
                width=20,
                height=20,
                fill="#111111",
                interaction={
                    "type": "input",
                    "role": "answer",
                    "include_in_submission": True,
                },
            ),
        ),
    )

    layout = compile_problem_template_to_layout(problem)
    content = layout["slots"][0]["content"]

    assert content["fill"] == "#ffffff"
    assert content["stroke"] == "#111827"
    assert content["input_style"]["font_size_mode"] == "auto"


def test_text_box_preserves_unbreakable_tokens_and_spacing() -> None:
    problem = ProblemTemplate(
        id="text_box_no_token_break_demo",
        title="Text box no token break demo",
        canvas=Canvas(width=300, height=120),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.number", "slot.digits"),
            ),
        ),
        slots=(
            TextBoxSlot(
                id="slot.number",
                text="(1)",
                x=10,
                y=20,
                width=30,
                height=30,
                font_size=22,
            ),
            TextBoxSlot(
                id="slot.digits",
                text="5  2  9",
                x=10,
                y=60,
                width=80,
                height=30,
                font_size=25,
            ),
        ),
    )

    svg = render_svg(compile_renderer_json(compile_problem_template_to_layout(problem)))

    assert "> (1)<" not in svg
    assert ">(1)</text>" in svg
    assert ">5  2  9</text>" in svg
    assert "<tspan" not in svg


def test_text_box_honors_middle_vertical_alignment() -> None:
    problem = ProblemTemplate(
        id="text_box_middle_valign_demo",
        title="Text box middle valign demo",
        canvas=Canvas(width=300, height=120),
        regions=(
            Region(
                id="region.stem", role="stem", flow="absolute", slot_ids=("slot.tb",)
            ),
        ),
        slots=(
            TextBoxSlot(
                id="slot.tb",
                text="507",
                x=10,
                y=20,
                width=80,
                height=80,
                font_size=20,
                valign="middle",
            ),
        ),
    )

    svg = render_svg(compile_renderer_json(compile_problem_template_to_layout(problem)))

    assert 'y="68"' in svg


def test_text_box_wraps_long_korean_text_without_spaces() -> None:
    problem = ProblemTemplate(
        id="text_box_korean_wrap_demo",
        title="Text box Korean wrap demo",
        canvas=Canvas(width=300, height=160),
        regions=(
            Region(
                id="region.stem", role="stem", flow="absolute", slot_ids=("slot.tb",)
            ),
        ),
        slots=(
            TextBoxSlot(
                id="slot.tb",
                text="가나다라마바사아자차카타파하",
                x=10,
                y=20,
                width=80,
                height=90,
                font_size=20,
            ),
        ),
    )

    svg = render_svg(compile_renderer_json(compile_problem_template_to_layout(problem)))

    assert "<tspan" in svg
    assert 'data-raw-text="가나다라마바사아자차카타파하"' in svg


def test_image_slot_renders_svg_image() -> None:
    problem = ProblemTemplate(
        id="image_slot_demo",
        title="Image slot demo",
        canvas=Canvas(width=300, height=180),
        regions=(
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=("slot.image",),
            ),
        ),
        slots=(
            ImageSlot(
                id="slot.image",
                href="data:image/png;base64,AAAA",
                x=20,
                y=30,
                width=120,
                height=80,
                transform="rotate(15 80 70)",
            ),
        ),
    )

    layout = compile_problem_template_to_layout(problem)
    validate_layout_json(layout)
    assert layout["slots"][0]["kind"] == "image"

    renderer = compile_renderer_json(layout)
    validate_renderer_json(renderer)
    assert renderer["elements"][0]["type"] == "image"

    svg = render_svg(renderer)
    assert "<image " in svg
    assert 'xmlns:xlink="http://www.w3.org/1999/xlink"' in svg
    assert 'href="data:image/png;base64,AAAA"' in svg
    assert 'xlink:href="data:image/png;base64,AAAA"' in svg
    assert 'preserveAspectRatio="xMidYMid meet"' in svg
    assert 'transform="rotate(15 80 70)"' in svg


def test_unplaced_blank_slot_stays_contract_only_when_regions_are_explicit() -> None:
    problem = ProblemTemplate(
        id="contract_only_blank_demo",
        title="Contract-only blank demo",
        canvas=Canvas(width=260, height=140),
        regions=(
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=("slot.visible",),
            ),
        ),
        slots=(
            TextSlot(id="slot.visible", text="□", x=80, y=90, font_size=28),
            BlankSlot(id="answer.contract", prompt="answer", answer_key="7"),
        ),
    )

    layout = compile_problem_template_to_layout(problem)
    region_slot_ids = {
        slot_id for region in layout["regions"] for slot_id in region["slot_ids"]
    }
    renderer = compile_renderer_json(layout)

    assert "answer.contract" not in region_slot_ids
    assert all(
        element["id"] != "answer.contract.blank" for element in renderer["elements"]
    )


def test_svg_renders_text_above_images_even_when_slots_are_mixed() -> None:
    problem = ProblemTemplate(
        id="text_above_image_demo",
        title="Text above image demo",
        canvas=Canvas(width=300, height=180),
        regions=(
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=("slot.text", "slot.image"),
            ),
        ),
        slots=(
            TextSlot(id="slot.text", text="visible text", x=30, y=60, font_size=20),
            ImageSlot(
                id="slot.image",
                href="data:image/png;base64,AAAA",
                x=20,
                y=30,
                width=160,
                height=90,
            ),
        ),
    )

    layout = compile_problem_template_to_layout(problem)
    renderer = compile_renderer_json(layout)
    svg = render_svg(renderer)

    assert svg.index('<image id="slot.image.image"') < svg.index(
        '<text id="slot.text.text"'
    )


def test_inline_local_image_hrefs_embeds_saved_svg_assets(tmp_path) -> None:
    image_path = tmp_path / "local.png"
    image_path.write_bytes(b"\x89PNG\r\n\x1a\n")
    svg = '<svg><image href="local.png" xlink:href="local.png" /></svg>'

    inlined = inline_local_image_hrefs(svg, tmp_path)

    assert inlined.count("data:image/png;base64,") == 2
    assert 'href="local.png"' not in inlined
    assert 'xlink:href="local.png"' not in inlined
