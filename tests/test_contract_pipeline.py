import json

import pytest

from modu_semantic import Problem, validate_problem_bundle
from modu_semantic.ir import Rect, Text


def test_problem_save_bundle_and_validate(tmp_path) -> None:
    p = Problem(width=320, height=180, problem_id="bundle_001", problem_type="demo")
    p.add(Rect(id="box", x=10, y=20, width=120, height=80, stroke="#111111", fill="#eeeeee"))
    p.add(Text(id="label", x=20, y=40, text="hello"))

    out_dir = tmp_path / "bundle_001"
    out_prefix = out_dir / "bundle_001"
    result = p.save(out_prefix, validate=True)
    assert result is None

    semantic_path = out_prefix.with_suffix(".semantic.json")
    assert semantic_path.exists()
    semantic = json.loads(semantic_path.read_text(encoding="utf-8"))
    assert semantic["schema_version"] == "modu_math.semantic.v3"

    errors = validate_problem_bundle(out_dir)
    assert errors == []


def test_problem_save_bundle_with_layout_diff_raises(tmp_path) -> None:
    p = Problem(width=320, height=180, problem_id="bundle_001", problem_type="demo")
    p.add(Rect(id="box", x=10, y=20, width=120, height=80, stroke="#111111", fill="#eeeeee"))
    p.add(Text(id="label", x=20, y=40, text="hello"))

    out_dir = tmp_path / "bundle_001_with_diff"
    with pytest.raises(ValueError):
        p.save(out_dir, include_layout_diff=True)
