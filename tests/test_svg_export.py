from modu_semantic import Group, Problem, Rect, Text


def test_svg_export_contains_group_elements() -> None:
    p = Problem(width=300, height=200, problem_id="svg1")
    g = Group(id="g1")
    g.add(Rect(id="r1", x=10, y=10, width=40, height=20))
    g.add(Text(id="t1", x=15, y=25, text="ok"))
    p.add(g)

    svg = p.to_svg()

    assert "<svg" in svg
    assert '<rect id="r1"' in svg
    assert '<text id="t1"' in svg
