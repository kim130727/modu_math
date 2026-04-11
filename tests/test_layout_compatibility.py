import json
from pathlib import Path

from modu_semantic.ir import Formula, Line, Rect, Text
from modu_semantic.problem import Problem


def build_sample_problem() -> Problem:
    p = Problem(width=800, height=600, problem_id="sample_001", problem_type="demo_geometry")
    p.add(
        Rect(
            id="box1",
            x=100,
            y=120,
            width=220,
            height=120,
            stroke="#222222",
            stroke_width=2,
            fill="#F5F5F5",
            group="question",
            z_index=1,
        )
    )
    p.add(
        Text(
            id="title",
            x=120,
            y=160,
            text="삼각형의 넓이",
            font_size=24,
            fill="#111111",
            anchor="start",
            group="question",
            z_index=2,
        )
    )
    p.add(
        Line(
            id="divider",
            x1=100,
            y1=190,
            x2=320,
            y2=190,
            stroke="#666666",
            stroke_width=1,
            z_index=2,
        )
    )
    p.add(
        Formula(
            id="eq1",
            x=120,
            y=220,
            expr="A = (b * h) / 2",
            font_size=20,
            fill="#111111",
            group="question",
            z_index=2,
        )
    )
    return p


def _load_parseable_layout_files() -> list[dict]:
    payloads: list[dict] = []
    for path in Path("examples/problem").rglob("layout_final.json"):
        try:
            payloads.append(json.loads(path.read_text(encoding="utf-8")))
        except Exception:
            continue
    return payloads


def test_layout_json_is_structurally_compatible_with_existing_samples() -> None:
    existing = _load_parseable_layout_files()
    assert existing, "No parseable existing layout_final.json found for compatibility baseline"

    root_keys_expected = {"schema_version", "problem_id", "metadata", "canvas", "summary", "elements"}

    generated = build_sample_problem().to_layout_json()
    assert set(generated.keys()) == root_keys_expected
    assert generated["schema_version"] == "modu_math.layout.v1"
    assert generated["problem_id"] == "sample_001"

    assert set(generated["canvas"].keys()) == {"width", "height", "viewBox"}
    assert set(generated["summary"].keys()) == {
        "total_elements",
        "count_by_type",
        "with_id",
        "without_id",
    }

    for element in generated["elements"]:
        assert set(["index", "id", "type", "x", "y", "width", "height", "attrs"]).issubset(element.keys())
        assert isinstance(element["attrs"], dict)
        for k, v in element["attrs"].items():
            assert isinstance(k, str)
            assert isinstance(v, str)

    observed_types = set()
    for payload in existing:
        for e in payload.get("elements", []):
            if "type" in e:
                observed_types.add(e["type"])

    generated_types = {e["type"] for e in generated["elements"]}
    assert generated_types.issubset(observed_types)

