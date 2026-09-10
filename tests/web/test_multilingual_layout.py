from copy import deepcopy
import json
from pathlib import Path
import xml.etree.ElementTree as ET

import pytest

from modu_math.layout.editor_overrides import apply_editor_overrides, prune_editor_overrides
from modu_math.layout.shared_layout import override_path, resolve_shared_layout
from modu_math.layout.text_layout import text_clusters, wrap_text
from modu_math_web.editor.services.dsl_patch import apply_layout_patches
from modu_math_web.editor.services.build import run_problem_build
from test_editor_api import _setup_django, _write_problem


def _dsl(text, *, x=50):
    return f'''
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot, RectSlot
PROBLEM_TEMPLATE = ProblemTemplate(
    id="shared", title="shared", canvas=Canvas(width=500, height=300),
    regions=(Region(id="region.stem", role="stem", slot_ids=("slot.question",)),
             Region(id="region.diagram", role="diagram", flow="absolute", slot_ids=("slot.digits", "slot.frame"))),
    slots=(TextSlot(id="slot.question", text={text!r}, x=20, y=40, font_size=26, semantic_role="question"),
           TextSlot(id="slot.digits", text="8   6   9", x={x}, y=180, font_size=26, semantic_role="diagram_label"),
           RectSlot(id="slot.frame", x=45, y=100, width=240, height=110)),
)
'''


@pytest.mark.parametrize("edited", ["869", "8 6 9", "  8   6  9  ", "8\n6\n9", ""])
def test_saved_spacing_and_geometry_survive_repeated_builds(tmp_path, edited):
    _setup_django(tmp_path)
    folder = _write_problem(tmp_path, "spacing", _dsl("문제"))
    apply_layout_patches("spacing", [{"target": "slot.digits", "op": "update",
                                      "value": {"text": edited, "x": 72.5, "y": 180}}], fast_overrides=True)
    before = (folder / "problem.editor_overrides.json").read_bytes()
    outputs = []
    for _ in range(3):
        built = run_problem_build("spacing")
        assert built.ok, built.error
        layout = json.loads((folder / "problem.layout.json").read_text(encoding="utf-8"))
        slot = next(s for s in layout["slots"] if s["id"] == "slot.digits")
        assert slot["content"]["text"] == edited
        assert (slot["content"]["x"], slot["content"]["y"]) == (72.5, 180)
        outputs.append((folder / "problem.renderer.json").read_bytes())
    assert outputs[0] == outputs[1] == outputs[2]
    assert (folder / "problem.editor_overrides.json").read_bytes() == before


def test_explicit_single_line_text_box_conversion_is_idempotent():
    layout = {"slots": [{"id": "slot.label", "kind": "text", "content": {
        "text": "A", "x": 100, "y": 120, "font_size": 24, "anchor": "middle"}}],
        "regions": [{"id": "region.diagram", "slot_ids": ["slot.label"]}]}
    overrides = {"slots": {"slot.label": {"kind": "text_box", "text": "  A  ",
                                         "x": 60, "y": 70, "width": 80, "height": 32}}}
    for _ in range(3):
        cleaned, changed = prune_editor_overrides(layout, overrides)
        assert not changed
        assert cleaned == overrides
        preview = apply_editor_overrides(deepcopy(layout), cleaned)
        assert preview["slots"][0]["kind"] == "text_box"
        for key, value in overrides["slots"]["slot.label"].items():
            assert preview["slots"][0]["content"][key] == value


@pytest.mark.parametrize("locale,text", [
    ("en", "Choose the multiplication expression represented by the shaded area of the diagram."),
    ("ja", "色を塗った部分がどの数の積を表しているか選んでください。"),
    ("zh", "请选择表示图中涂色部分的乘法算式。"),
    ("km", "ចូរជ្រើសរើសប្រយោគគុណដែលត្រូវនឹងផ្នែកដែលបានផាត់ពណ៌។"),
    ("uk", "Виберіть вираз множення, який відповідає зафарбованій частині малюнка."),
])
def test_shared_geometry_keeps_translation_and_fits_without_moving_diagram(tmp_path, locale, text):
    _setup_django(tmp_path)
    source = _write_problem(tmp_path, "ko/shared", _dsl("색칠한 부분에 맞는 식을 고르세요."))
    target = _write_problem(tmp_path, f"{locale}/shared", _dsl(text, x=280))
    override_path(source / "problem.dsl.py").write_text(json.dumps({
        "slots": {"slot.digits": {"x": 70, "text": "8 6 9"}},
        "deleted_slots": ["slot.frame"],
    }), encoding="utf-8")
    override_path(target / "problem.dsl.py").write_text(json.dumps({
        "layout_source": "../../ko/shared/problem.dsl.py",
    }), encoding="utf-8")
    outputs = []
    for _ in range(2):
        built = run_problem_build(f"{locale}/shared")
        assert built.ok, built.error
        layout = json.loads((target / "problem.layout.json").read_text(encoding="utf-8"))
        slots = {s["id"]: s for s in layout["slots"]}
        assert "slot.frame" not in slots
        assert slots["slot.digits"]["content"]["x"] == 70
        assert slots["slot.digits"]["content"]["y"] == 180
        assert slots["slot.digits"]["content"]["text"] == "8 6 9"
        prompt = slots["slot.question"]["content"]
        assert prompt["text"] == text
        assert prompt["x"] + prompt["width"] <= 500
        assert len(wrap_text(text, prompt["width"], prompt["font_size"])) * prompt["font_size"] * prompt["line_height"] <= prompt["height"]
        outputs.append(layout)
    assert outputs[0] == outputs[1]
    # A later source edit propagates without rebuilding or reading its artifacts.
    apply_layout_patches("ko/shared", [{"target": "slot.digits", "op": "update", "value": {"x": 95}}], fast_overrides=True)
    source_build = run_problem_build("ko/shared")
    assert source_build.ok, source_build.error
    assert "shared_layout" in source_build.stdout
    layout = json.loads((target / "problem.layout.json").read_text(encoding="utf-8"))
    assert next(s for s in layout["slots"] if s["id"] == "slot.digits")["content"]["x"] == 95
    # Explicit target edits still have the final say, including fewer spaces.
    apply_layout_patches(f"{locale}/shared", [{"target": "slot.digits", "op": "update", "value": {"x": 110, "text": "869"}}], fast_overrides=True)
    assert run_problem_build(f"{locale}/shared").ok
    layout = json.loads((target / "problem.layout.json").read_text(encoding="utf-8"))
    digits = next(s for s in layout["slots"] if s["id"] == "slot.digits")["content"]
    assert (digits["x"], digits["text"]) == (110, "869")


def test_shared_layout_cycle_fails_clearly(tmp_path):
    path = tmp_path / "problem.dsl.py"
    path.write_text(_dsl("test"), encoding="utf-8")
    override_path(path).write_text('{"layout_source":"problem.dsl.py"}', encoding="utf-8")
    with pytest.raises(ValueError, match="Circular layout_source"):
        resolve_shared_layout({}, path)


def test_wrap_preserves_spaces_and_khmer_clusters():
    text = "  8   6   9  "
    assert "".join(wrap_text(text, 35, 20)) == text
    khmer = "ប្រយោគគុណ"
    lines = wrap_text(khmer, 30, 20)
    assert "".join(lines) == khmer
    assert text_clusters(khmer) == [cluster for line in lines for cluster in text_clusters(line)]


def test_svg_keeps_authored_newlines_without_inserting_indentation():
    from modu_math.renderer.svg.render import render_svg
    text = " 8  6 \n 9\t0 "
    svg = render_svg({"problem_id": "spacing", "view_box": {"width": 300, "height": 200},
                      "elements": [{"id": "digits", "type": "text", "text": text,
                                    "attributes": {"x": 20, "y": 30, "font-size": 20}}]})
    node = ET.fromstring(svg).find("{http://www.w3.org/2000/svg}text")
    assert node.attrib["data-raw-text"] == text
    assert node.text is None
    assert [span.text for span in node] == text.split("\n")
    assert all(span.tail is None for span in node)
