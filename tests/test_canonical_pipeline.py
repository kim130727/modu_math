import json

import pytest

from modu_semantic import Problem, Rect
from modu_semantic.normalizer import normalize_semantic
from modu_semantic.schema import SchemaValidationError, validate_semantic_json


def _minimal_semantic() -> dict[str, object]:
    return {
        "schema_version": "modu_math.semantic.v3",
        "render_contract_version": "modu_math.render.v1",
        "problem_id": "s001",
        "problem_type": "demo",
        "metadata": {},
        "domain": {},
        "render": {
            "canvas": {"width": 100, "height": 100, "background": "#FFFFFF"},
            "elements": [{"id": "t1", "type": "text", "x": 10, "y": 20, "text": "hello"}],
        },
        "answer": {"blanks": [], "choices": [], "answer_key": []},
    }


def test_normalize_semantic_absorbs_legacy_aliases() -> None:
    legacy = {
        "schemaVersion": "modu_math.semantic.v3",
        "renderContractVersion": "modu_math.render.v1",
        "problemId": "legacy_001",
        "problemType": "legacy_demo",
        "meta": {"source": "legacy"},
        "drawing": {
            "canvas": {"width": 300, "height": 200, "bg": "#FAFAFA"},
            "items": [
                {
                    "id": "eq1",
                    "type": "latex",
                    "x": 40,
                    "y": 50,
                    "text": "a+b",
                    "zIndex": 3,
                }
            ],
        },
        "answer": {"answerKey": [2]},
    }

    normalized = normalize_semantic(legacy)

    assert list(normalized.keys())[:4] == [
        "schema_version",
        "render_contract_version",
        "problem_id",
        "problem_type",
    ]
    assert normalized["metadata"] == {"source": "legacy"}
    assert normalized["render"]["canvas"]["background"] == "#FAFAFA"
    assert normalized["render"]["elements"][0]["type"] == "formula"
    assert normalized["render"]["elements"][0]["expr"] == "a+b"
    assert normalized["render"]["elements"][0]["z_index"] == 3
    assert normalized["answer"]["answer_key"] == [2]


def test_normalize_semantic_maps_legacy_formula_text_to_expr() -> None:
    legacy = {
        "schema_version": "modu_math.semantic.v3",
        "render_contract_version": "modu_math.render.v1",
        "problem_id": "legacy_formula",
        "problem_type": "demo",
        "metadata": {},
        "domain": {},
        "render": {
            "canvas": {"width": 100, "height": 100, "background": "#FFFFFF"},
            "elements": [{"id": "f1", "type": "formula", "x": 10, "y": 20, "text": "a/b"}],
        },
        "answer": {"blanks": [], "choices": [], "answer_key": []},
    }

    normalized = normalize_semantic(legacy)
    element = normalized["render"]["elements"][0]

    assert element["type"] == "formula"
    assert element["expr"] == "a/b"
    assert "text" not in element


def test_validate_semantic_rejects_wrong_root_order() -> None:
    semantic = _minimal_semantic()
    reordered = {
        "problem_id": semantic["problem_id"],
        "schema_version": semantic["schema_version"],
        "render_contract_version": semantic["render_contract_version"],
        "problem_type": semantic["problem_type"],
        "metadata": semantic["metadata"],
        "domain": semantic["domain"],
        "render": semantic["render"],
        "answer": semantic["answer"],
    }

    with pytest.raises(SchemaValidationError):
        validate_semantic_json(reordered)


def test_validate_semantic_rejects_forbidden_text_expr_combo() -> None:
    semantic = _minimal_semantic()
    semantic["render"]["elements"] = [
        {"id": "t1", "type": "text", "x": 10, "y": 20, "text": "hello", "expr": "x+y"}
    ]

    with pytest.raises(SchemaValidationError):
        validate_semantic_json(semantic)


def test_problem_save_flat_outputs_canonical_json(tmp_path) -> None:
    p = Problem(width=320, height=180, problem_id="flat_001", problem_type="demo")
    p.add(Rect(id="box", x=10, y=20, width=120, height=80))

    out_prefix = tmp_path / "flat_001"
    result = p.save(out_prefix, validate=True)
    assert result is None

    semantic = json.loads(out_prefix.with_suffix(".semantic.json").read_text(encoding="utf-8"))

    assert list(semantic.keys())[:4] == [
        "schema_version",
        "render_contract_version",
        "problem_id",
        "problem_type",
    ]
