import json
from pathlib import Path

from modu_semantic import Problem, validate_problem_bundle
from modu_semantic.ir import Rect, Text


def test_problem_save_bundle_and_validate(tmp_path: Path) -> None:
    p = Problem(width=320, height=180, problem_id="bundle_001", problem_type="demo")
    p.add(Rect(id="box", x=10, y=20, width=120, height=80, stroke="#111111", fill="#eeeeee"))
    p.add(Text(id="label", x=20, y=40, text="hello"))

    out_dir = tmp_path / "bundle_001"
    outputs = p.save(out_dir, include_layout_diff=False)

    assert "semantic" in outputs
    assert "layout" in outputs
    assert outputs["semantic"].exists()
    assert outputs["layout"].exists()

    semantic = json.loads(outputs["semantic"].read_text(encoding="utf-8"))
    layout = json.loads(outputs["layout"].read_text(encoding="utf-8"))

    assert semantic["schema_version"] == "modu_math.semantic.v3"
    assert layout["schema_version"] == "modu_math.layout.v1"

    errors = validate_problem_bundle(out_dir)
    assert errors == []


def test_problem_save_bundle_with_layout_diff(tmp_path: Path) -> None:
    p = Problem(width=320, height=180, problem_id="bundle_001", problem_type="demo")
    p.add(Rect(id="box", x=10, y=20, width=120, height=80, stroke="#111111", fill="#eeeeee"))
    p.add(Text(id="label", x=20, y=40, text="hello"))

    baseline_layout = Path("tests/fixtures/bundles/0001/json/layout_final/layout_final.json")
    out_dir = tmp_path / "bundle_001_with_diff"
    outputs = p.save(out_dir, include_layout_diff=True, baseline_layout_path=baseline_layout)

    assert "layout_diff" in outputs
    layout_diff = json.loads(outputs["layout_diff"].read_text(encoding="utf-8"))

    assert layout_diff["schema_version"] == "modu_math.layout_diff.v1"
    assert set(layout_diff.keys()) == {"schema_version", "problem_id", "metadata", "diff", "metrics"}
    assert "root" in layout_diff["diff"]
    assert "element" in layout_diff["diff"]

