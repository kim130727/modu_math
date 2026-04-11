from modu_semantic import Group, Problem, Rect, Text


def test_layout_export_is_flattened() -> None:
    p = Problem(width=320, height=200, problem_id="l1")
    g = Group(id="g1")
    g.add(Rect(id="r1", x=0, y=0, width=100, height=50))
    g.add(Text(id="t1", x=5, y=20, text="hi"))
    p.add(g)

    doc = p.to_layout_dict()

    assert doc["schema_version"] == "modu_math.layout.v1"
    assert doc["problem_id"] == "l1"
    ids = {item.get("id") for item in doc["elements"]}
    assert "r1" in ids
    assert "t1" in ids


def test_layout_export_uses_layout_schema_version() -> None:
    p = Problem(width=320, height=200, problem_id="l2", layout_schema_version="modu_math.layout.v1")
    p.add(Rect(id="r1", x=0, y=0, width=10, height=10))

    doc = p.to_layout_dict()

    assert doc["schema_version"] == "modu_math.layout.v1"
