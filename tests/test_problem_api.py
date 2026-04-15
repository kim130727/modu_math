from modu_semantic import Formula, Problem, Rect, Text


def test_problem_add_and_export() -> None:
    p = Problem(width=800, height=600, problem_id="t1")
    p.add(Rect(id="r1", x=0, y=0, width=100, height=50))
    p.add(Text(id="txt1", x=10, y=20, text="hello"))

    semantic = p.to_semantic_dict()
    svg = p.to_svg()

    assert semantic["problem_id"] == "t1"
    assert len(semantic["render"]["elements"]) == 2
    assert "<svg" in svg
    assert 'id="r1"' in svg

    ir_problem = p.to_ir()
    assert ir_problem.problem_id == "t1"
    assert len(ir_problem.elements) == 2


def test_problem_update_content_supports_text_and_formula() -> None:
    p = Problem(width=400, height=200, problem_id="u1")
    p.add(Text(id="txt1", x=10, y=20, text="hello"))
    p.add(Formula(id="f1", x=30, y=40, expr="a+b"))

    p.update_content("txt1", "updated")
    p.update_text("f1", "x+y")

    assert p.elements[0].text == "updated"
    assert p.elements[1].expr == "x+y"
