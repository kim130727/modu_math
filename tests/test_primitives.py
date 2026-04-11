from modu_semantic import Circle, Formula, Line, Polygon, Rect, Text


def test_primitives_defaults() -> None:
    r = Rect(id="r", x=1, y=2, width=3, height=4)
    c = Circle(id="c", cx=10, cy=11, r=12)
    l = Line(id="l", x1=0, y1=0, x2=1, y2=1)
    p = Polygon(id="p", points=[(0, 0), (1, 0), (0, 1)])
    t = Text(id="t", x=0, y=0, text="A")
    f = Formula(id="f", x=0, y=0, expr="x+1")

    assert r.fill == "none"
    assert c.stroke == "#000000"
    assert l.stroke_width == 1.0
    assert p.points[0] == (0, 0)
    assert t.font_family == "sans-serif"
    assert f.font_family == "serif"
    assert f.expr == "x+1"


def test_formula_accepts_legacy_text_alias() -> None:
    f = Formula(id="f_legacy", x=10, y=20, text="a+b")
    assert f.expr == "a+b"
