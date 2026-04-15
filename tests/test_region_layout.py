from modu_semantic import Problem, Rect, Region, Text


def test_region_split_v_no_overlap() -> None:
    box = Region(id="problem_box", x=80, y=60, width=1120, height=560)
    sections = box.split_v(
        heights=[100, 240, 140],
        gap=20,
        padding=20,
        ids=["instruction", "figure", "answer"],
    )

    instruction, figure, answer = sections

    assert instruction.x == 100
    assert instruction.y == 80
    assert figure.y == 200
    assert answer.y == 460
    assert instruction.intersects(figure) is False
    assert figure.intersects(answer) is False


def test_region_split_overflow_raises() -> None:
    box = Region(id="problem_box", x=0, y=0, width=400, height=200)

    try:
        box.split_v(heights=[120, 120], gap=10, padding=10)
    except ValueError as exc:
        assert "split overflow" in str(exc)
    else:
        raise AssertionError("Expected split overflow ValueError")


def test_relative_coords_become_absolute_in_layout_and_svg() -> None:
    p = Problem(width=1000, height=700, problem_id="region_001")

    problem_box = Region(id="problem_box", x=80, y=80, width=840, height=520)
    instruction, figure, answer = problem_box.split_v(
        heights=[90, 220, 130],
        gap=20,
        padding=20,
        ids=["instruction", "figure", "answer"],
    )

    instruction.add(Text(id="instr", x=0, y=30, text="다음 도형을 보고 답하세요."))
    figure.add(Rect(id="shape_box", x=20, y=20, width=300, height=180, stroke="#222222"))
    answer.add(Rect(id="answer_box", x=0, y=10, width=280, height=70, stroke="#444444"))

    p.add(problem_box)

    semantic = p.to_semantic_dict()
    by_id = {item["id"]: item for item in semantic["render"]["elements"] if "id" in item}

    # instruction absolute origin = (100,100)
    assert by_id["instr"]["x"] == 100
    assert by_id["instr"]["y"] == 130

    # figure absolute origin = (100, 210)
    assert by_id["shape_box"]["x"] == 120
    assert by_id["shape_box"]["y"] == 230

    svg = p.to_svg()
    assert 'id="instr"' in svg
    assert 'x="100" y="130"' in svg
    assert 'id="shape_box"' in svg


def test_region_inset_and_nested_split_are_absolute() -> None:
    root = Region(id="root", x=50, y=40, width=300, height=200)
    assert root.contains_point(60, 50) is True
    assert root.contains_point(10, 10) is False
    inner = root.inset(10, id="inner")
    assert inner.x == 60
    assert inner.y == 50

    left, right = inner.split_cols(widths=[120, 140], gap=10, padding=5, ids=["left", "right"])
    assert left.x == 65
    assert left.y == 55
    assert right.x == 195
    assert right.y == 55

    top, bottom = right.split_rows(heights=[60, 70], gap=10, padding=5, ids=["top", "bottom"])
    assert top.x == 200
    assert top.y == 60
    assert bottom.x == 200
    assert bottom.y == 130




