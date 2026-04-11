from modu_semantic import Formula, Group, Problem, Rect


def test_semantic_export_top_level() -> None:
    p = Problem(width=320, height=200, problem_id="s1", problem_type="demo")
    p.add(Rect(id="r1", x=10, y=20, width=30, height=40, semantic_role="shape"))

    doc = p.to_semantic_dict()

    assert doc["schema_version"] == "modu_math.semantic.v3"
    assert doc["render_contract_version"] == "modu_math.render.v1"
    assert doc["render"]["canvas"]["width"] == 320
    assert doc["render"]["elements"][0]["type"] == "rect"


def test_semantic_export_preserves_group_context_on_flatten() -> None:
    p = Problem(width=320, height=200, problem_id="s2", problem_type="demo")
    g = Group(id="g1", semantic_role="question_block", metadata={"label": "본문"})
    g.add(Rect(id="r1", x=10, y=20, width=30, height=40))
    p.add(g)

    doc = p.to_semantic_dict()
    element = doc["render"]["elements"][0]

    assert element["metadata"]["group_id"] == "g1"
    assert element["metadata"]["group_semantic_role"] == "question_block"
    assert element["metadata"]["group_metadata"]["label"] == "본문"
    assert element["semantic_role"] == "question_block"


def test_formula_semantic_export_uses_expr_only() -> None:
    p = Problem(width=320, height=200, problem_id="s3", problem_type="demo")
    p.add(Formula(id="f1", x=20, y=30, expr="x+y"))

    doc = p.to_semantic_dict()
    element = doc["render"]["elements"][0]

    assert element["type"] == "formula"
    assert element["expr"] == "x+y"
    assert "text" not in element
