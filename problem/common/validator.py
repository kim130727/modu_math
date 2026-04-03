from __future__ import annotations

import sys
from pathlib import Path
from typing import Any


def _ensure_src_on_path() -> None:
    current = Path(__file__).resolve()
    for parent in current.parents:
        src_dir = parent / "src"
        if src_dir.is_dir():
            src_path = str(src_dir)
            if src_path not in sys.path:
                sys.path.insert(0, src_path)
            return
    raise RuntimeError("Could not locate src directory for validator bridge.")


_ensure_src_on_path()

from modu_math.validators.layout_validator import LayoutValidator
from modu_math.validators.logic_validator import LogicValidator, default_logic_rules
from modu_math.validators.schema_validator import SchemaValidator


def validate_semantic(semantic: dict) -> list[str]:
    """
    Backward-compatible API.

    Existing problem scripts call this function and expect a flat list[str].
    Internally this now delegates to the new split validators in src/modu_math.
    """
    semantic_v3 = _to_v3_if_needed(semantic)
    schema_issues = SchemaValidator().validate(semantic_v3)
    logic_issues = LogicValidator(default_logic_rules()).validate(semantic_v3)
    layout_issues = LayoutValidator().validate(semantic_v3)
    return _issues_to_messages([*schema_issues, *logic_issues, *layout_issues])


def validate_structure(semantic: dict) -> list[str]:
    semantic_v3 = _to_v3_if_needed(semantic)
    issues = SchemaValidator().validate(semantic_v3)
    return _issues_to_messages(issues)


def validate_logic(semantic: dict) -> list[str]:
    semantic_v3 = _to_v3_if_needed(semantic)
    issues = LogicValidator(default_logic_rules()).validate(semantic_v3)
    return _issues_to_messages(issues)


def _issues_to_messages(issues: list) -> list[str]:
    return [f"{i.code}: {i.message}" for i in issues]


def _to_v3_if_needed(semantic: dict[str, Any]) -> dict[str, Any]:
    # Already v3-style.
    if isinstance(semantic, dict) and "render" in semantic and "answer" in semantic:
        return semantic

    if not isinstance(semantic, dict):
        return {
            "schema_version": "modu_math.semantic.v3",
            "problem_id": "unknown",
            "problem_type": "unknown",
            "metadata": {},
            "domain": {},
            "render": {"canvas": {"width": 0, "height": 0, "background": "#FFFFFF"}, "elements": []},
            "answer": {"blanks": [], "choices": [], "answer_key": []},
        }

    meta = semantic.get("meta", {}) if isinstance(semantic.get("meta", {}), dict) else {}
    problem = semantic.get("problem", {}) if isinstance(semantic.get("problem", {}), dict) else {}
    canvas = semantic.get("canvas", {}) if isinstance(semantic.get("canvas", {}), dict) else {}
    elements = semantic.get("elements", []) if isinstance(semantic.get("elements", []), list) else []

    problem_id = str(meta.get("problem_id", problem.get("id", "unknown")))
    problem_type = str(problem.get("type", "unknown"))

    answer_key = _derive_answer_key(problem, elements)
    blanks = _derive_blanks(elements, answer_key)
    choices = problem.get("choices", []) if isinstance(problem.get("choices", []), list) else []

    return {
        "schema_version": "modu_math.semantic.v3",
        "problem_id": problem_id,
        "problem_type": problem_type,
        "metadata": {
            "source_file": meta.get("source", "legacy_problem_common_validator_bridge"),
            "language": "ko-KR",
            "grade_band": "unknown",
        },
        "domain": _derive_domain(problem_type, problem),
        "render": {
            "canvas": {
                "width": canvas.get("width", 0),
                "height": canvas.get("height", 0),
                "background": canvas.get("background", "#FFFFFF"),
            },
            "groups": [],
            "elements": elements,
        },
        "answer": {
            "blanks": blanks,
            "choices": choices,
            "answer_key": answer_key,
        },
    }


def _derive_domain(problem_type: str, problem: dict[str, Any]) -> dict[str, Any]:
    if problem_type in {"fill_in_blank", "time_conversion_fill_blank"}:
        q = problem.get("question", {}) if isinstance(problem.get("question", {}), dict) else {}
        return {
            "left_seconds": q.get("left_seconds"),
            "minutes": q.get("minutes"),
            "unit_from": q.get("unit_from"),
            "unit_mid": q.get("unit_mid"),
            "unit_to": q.get("unit_to"),
        }

    if problem_type == "measure_length_with_ruler":
        return {
            "ruler": problem.get("ruler", {}),
            "measurement": problem.get("measurement", {}),
            "expected_mm": problem.get("answer_mm"),
        }

    if problem_type == "base_ten_block_addition":
        addends = problem.get("addends", []) if isinstance(problem.get("addends", []), list) else []
        return {
            "addends": addends,
            "sum": problem.get("answer"),
        }

    return {}


def _derive_answer_key(problem: dict[str, Any], elements: list[dict[str, Any]]) -> list[dict[str, Any]]:
    blank_id = _first_blank_id(elements)

    if "answer" in problem:
        return [{"target": blank_id, "value": str(problem["answer"])}]
    if "answer_mm" in problem:
        return [{"target": blank_id, "value": str(problem["answer_mm"])}]
    return []


def _derive_blanks(elements: list[dict[str, Any]], answer_key: list[dict[str, Any]]) -> list[dict[str, Any]]:
    blanks: list[dict[str, Any]] = []
    key_value = answer_key[0]["value"] if answer_key else ""

    for elem in elements:
        if not isinstance(elem, dict):
            continue
        if elem.get("answer_blank") is True or elem.get("semantic_role") == "answer_blank":
            blanks.append(
                {
                    "id": str(elem.get("id", "answer_blank")),
                    "kind": "numeric",
                    "value": key_value,
                }
            )

    return blanks


def _first_blank_id(elements: list[dict[str, Any]]) -> str:
    for elem in elements:
        if not isinstance(elem, dict):
            continue
        if elem.get("answer_blank") is True or elem.get("semantic_role") == "answer_blank":
            return str(elem.get("id", "answer_blank"))
    return "answer_blank"
