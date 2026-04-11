import pytest

from modu_semantic import Problem, Rect
from modu_semantic.schema import SchemaValidationError, validate_semantic_json


def test_validation_passes_for_basic_problem() -> None:
    p = Problem(width=800, height=600, problem_id="valid_001")
    p.add(Rect(id="r1", x=10, y=20, width=30, height=40))
    p.validate()


def test_validation_rejects_non_positive_canvas() -> None:
    p = Problem(width=0, height=600, problem_id="invalid_001")
    p.add(Rect(id="r1", x=10, y=20, width=30, height=40))
    with pytest.raises(ValueError):
        p.validate()


def test_schema_rejects_unknown_domain_profile() -> None:
    semantic = {
        "schema_version": "modu_math.semantic.v3",
        "render_contract_version": "modu_math.render.v1",
        "problem_id": "schema_profile_001",
        "problem_type": "demo",
        "metadata": {},
        "domain": {"profile": "unknown_profile"},
        "render": {
            "canvas": {"width": 320, "height": 200, "background": "#FFFFFF"},
            "elements": [{"id": "t1", "type": "text", "x": 20, "y": 30, "text": "hello"}],
        },
        "answer": {"blanks": [], "choices": [], "answer_key": []},
    }
    with pytest.raises(SchemaValidationError):
        validate_semantic_json(semantic)
