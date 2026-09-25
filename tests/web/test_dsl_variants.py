from pathlib import Path
import json

import pytest

from modu_math.dsl.variants import (
    decode,
    delta_path,
    materialized_snapshot,
    read_source,
    review_paths,
    save_variant,
    source_path,
    snapshot,
    write_source,
)
from modu_math_web.editor.services.problems import (
    invalidate_problem_list_cache,
    list_problem_directories,
    read_problem_detail,
    save_problem_dsl,
)

SOURCE = """from modu_math.dsl import Canvas, ProblemTemplate, TextSlot, Region
PROBLEM_TEMPLATE = ProblemTemplate(
    id="sample", title="원본", canvas=Canvas(width=400, height=200),
    regions=(Region(id="region.main", role="prompt", slot_ids=("slot.q",)),),
    slots=(TextSlot(id="slot.q", text="문제", x=10, y=20, width=300, height=50),),
)
"""


@pytest.fixture
def variant(tmp_path, settings):
    root = tmp_path / "problems"
    canonical = root / "ko" / "sample.dsl.py"
    target = root / "uk" / "sample.dsl.py"
    canonical.parent.mkdir(parents=True)
    target.parent.mkdir()
    canonical.write_text(SOURCE, encoding="utf-8")
    translated = SOURCE.replace('"원본"', '"English"').replace('"문제"', '"Question"')
    save_variant(target, canonical, snapshot(translated, target))
    settings.PROBLEMS_ROOT = root
    settings.GOLDEN_PROBLEMS_ROOT = tmp_path / "golden"
    invalidate_problem_list_cache()
    return canonical, target


def test_virtual_listing_read_save_and_svg(variant):
    from modu_math_web.editor.services.build import run_problem_build
    from modu_math_web.editor.services.dsl_patch import apply_layout_patches

    canonical, target = variant
    original = canonical.read_bytes()
    listing = list_problem_directories()
    assert len(listing) == 2
    assert listing[0]["equivalent_problem_ids"]["ko"] == "ko/sample.dsl.py"
    detail = read_problem_detail("uk/sample.dsl.py")
    assert detail["dsl_storage"] == "locale_catalog"
    assert detail["source_problem_id"] == "ko/sample.dsl.py"
    save_problem_dsl("uk/sample.dsl.py", detail["dsl"].replace("Question", "Updated"))
    apply_layout_patches(
        "uk/sample.dsl.py",
        [
            {"target": "slot.q", "op": "update", "value": {"x": 35}},
        ],
    )
    assert canonical.read_bytes() == original
    assert not target.exists()
    assert "Updated" in read_source(target)
    assert read_problem_detail("uk/sample.dsl.py")["layout"]["slots"][0]["content"]["x"] == 35
    result = run_problem_build("ko/sample.dsl.py")
    assert result.ok, result.error
    assert "Updated" in read_problem_detail("uk/sample.dsl.py")["svg"]


def test_source_geometry_inherits_and_translation_needs_review(variant):
    canonical, target = variant
    canonical.write_text(
        SOURCE.replace("x=10", "x=70").replace("문제", "새 문제"), encoding="utf-8"
    )
    template = decode(materialized_snapshot(target)["PROBLEM_TEMPLATE"])
    assert template.slots[0].x == 70
    assert template.slots[0].text == "Question"
    assert review_paths(target)
    write_source(target, read_source(target))
    assert review_paths(target), "Formatting must not mark stale translations reviewed"


def test_fast_canvas_edits_and_answer_metadata_keep_virtual_dsl(variant):
    from modu_math_web.editor.services.build import run_problem_build
    from modu_math_web.editor.services.dsl_patch import apply_layout_patches
    from modu_math_web.editor.services.problems import create_blank_problem

    canonical, target = variant
    assert run_problem_build("uk/sample.dsl.py").ok
    apply_layout_patches(
        "uk/sample.dsl.py",
        [
            {"target": "slot.q", "op": "update", "value": {"x": 77, "text": "Edited"}},
        ],
        fast_overrides=True,
    )
    assert run_problem_build("uk/sample.dsl.py").ok
    detail = read_problem_detail("uk/sample.dsl.py")
    slot = next(slot for slot in detail["layout"]["slots"] if slot["id"] == "slot.q")
    assert slot["content"]["x"] == 77
    assert slot["content"]["text"] == "Edited"
    assert not target.exists()
    assert canonical.read_text(encoding="utf-8") == SOURCE
    with pytest.raises(FileExistsError):
        create_blank_problem("uk/sample.dsl.py")


def test_common_editor_geometry_and_language_override(variant):
    from modu_math_web.editor.services.build import run_problem_build
    from modu_math_web.editor.services.dsl_patch import apply_layout_patches

    _, target = variant
    assert run_problem_build("ko/sample.dsl.py").ok
    apply_layout_patches(
        "ko/sample.dsl.py",
        [
            {"target": "slot.q", "op": "update", "value": {"x": 60}},
        ],
        fast_overrides=True,
    )
    result = run_problem_build("ko/sample.dsl.py")
    assert result.ok, result.error
    detail = read_problem_detail("uk/sample.dsl.py")
    assert detail["layout"]["slots"][0]["content"]["x"] == 60
    assert detail["layout"]["slots"][0]["content"]["text"] == "Question"
    apply_layout_patches(
        "uk/sample.dsl.py",
        [
            {"target": "slot.q", "op": "update", "value": {"x": 80}},
        ],
        fast_overrides=True,
    )
    assert run_problem_build("ko/sample.dsl.py").ok
    assert (
        read_problem_detail("uk/sample.dsl.py")["layout"]["slots"][0]["content"]["x"]
        == 80
    )
    assert not target.exists()


def test_invalid_source_does_not_overwrite_variant(variant):
    _, target = variant
    original = delta_path(target).read_bytes()
    with pytest.raises(SyntaxError):
        write_source(target, "this is not valid python!")
    assert delta_path(target).read_bytes() == original


def test_slot_ids_survive_reordering(variant):
    canonical, target = variant
    changed = SOURCE.replace(
        "slots=(TextSlot",
        'slots=(TextSlot(id="slot.extra", text="Extra", x=0, y=0, width=20, height=20), TextSlot',
    )
    canonical.write_text(changed, encoding="utf-8")
    template = decode(materialized_snapshot(target)["PROBLEM_TEMPLATE"])
    assert template.slots[0].id == "slot.extra"
    assert template.slots[1].text == "Question"


def test_locale_metadata_cannot_redirect_source(variant):
    canonical, target = variant
    data = json.loads(delta_path(target).read_text(encoding="utf-8"))
    data["source"] = "../../../../outside.dsl.py"
    delta_path(target).write_text(json.dumps(data), encoding="utf-8")
    assert source_path(target) == canonical.resolve()
    assert "Question" in read_source(target)
