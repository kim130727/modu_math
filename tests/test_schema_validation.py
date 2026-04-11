import pytest

from modu_semantic import Problem, Rect


def test_validation_passes_for_basic_problem() -> None:
    p = Problem(width=800, height=600, problem_id="valid_001")
    p.add(Rect(id="r1", x=10, y=20, width=30, height=40))
    p.validate()


def test_validation_rejects_non_positive_canvas() -> None:
    p = Problem(width=0, height=600, problem_id="invalid_001")
    p.add(Rect(id="r1", x=10, y=20, width=30, height=40))
    with pytest.raises(ValueError):
        p.validate()
