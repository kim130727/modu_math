import copy

import pytest

from modu_semantic.validator import BundleValidationError, validate_semantic


def _base_semantic() -> dict:
    return {
        "schema_version": "modu_math.semantic.v3",
        "render_contract_version": "modu_math.render.v1",
        "problem_id": "p001",
        "problem_type": "demo",
        "metadata": {},
        "domain": {},
        "render": {
            "canvas": {"width": 400, "height": 300, "background": "#FFFFFF"},
            "elements": [{"id": "t1", "type": "text", "x": 20, "y": 30, "text": "question"}],
        },
        "answer": {
            "blanks": [{"id": "blank_1", "type": "numeric_or_text"}],
            "choices": [],
            "answer_key": [{"blank_id": "blank_1", "value": 3}],
        },
    }


def test_validate_semantic_profile_passes_with_required_fields() -> None:
    doc = _base_semantic()
    doc["domain"] = {
        "profile": "addition_word_problem",
        "context": "There are apples.",
        "question": "How many are there?",
        "operands": [2, 1],
        "operation": "add",
    }
    validate_semantic(doc)


def test_validate_semantic_profile_missing_required_field_fails() -> None:
    doc = _base_semantic()
    doc["domain"] = {
        "profile": "shape_count",
        "question": "How many triangles are there?",
        "target_shape": "triangle",
    }
    with pytest.raises(BundleValidationError):
        validate_semantic(doc)


def test_validate_semantic_duplicate_element_id_fails() -> None:
    doc = _base_semantic()
    duplicated = copy.deepcopy(doc["render"]["elements"][0])
    doc["render"]["elements"].append(duplicated)
    with pytest.raises(BundleValidationError):
        validate_semantic(doc)


def test_validate_semantic_answer_blank_link_mismatch_fails() -> None:
    doc = _base_semantic()
    doc["answer"]["answer_key"] = [{"blank_id": "blank_x", "value": 3}]
    with pytest.raises(BundleValidationError):
        validate_semantic(doc)
