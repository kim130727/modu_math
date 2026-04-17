from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .contracts import load_contract_json
from .schema import SchemaValidationError, validate_layout_diff_json, validate_layout_json, validate_semantic_json


class BundleValidationError(SchemaValidationError):
    pass


_PROFILE_REQUIRED_FIELDS: dict[str, set[str]] = {
    "addition_word_problem": {"context", "question", "operands", "operation"},
    "shape_count": {"question", "target_shape", "candidates"},
    "fraction_compare": {"question", "left_fraction", "right_fraction", "comparison"},
    "length_compare": {"question", "segments", "relation"},
}

_COORD_KEYS = {"x", "x1", "x2"}
_COORD_Y_KEYS = {"y", "y1", "y2"}


def load_schema(name: str) -> dict[str, Any]:
    return load_contract_json(name)


def validate_json(data: dict[str, Any], schema: dict[str, Any]) -> None:
    schema_id = schema.get("$id", "")
    if "semantic" in schema_id:
        validate_semantic_json(data)
        return
    if "layout_diff" in schema_id:
        validate_layout_diff_json(data)
        return
    if "layout" in schema_id:
        validate_layout_json(data)
        return
    raise BundleValidationError(f"Unsupported schema id for validation: {schema_id}")


def validate_semantic(data: dict[str, Any]) -> None:
    validate_semantic_json(data)
    _validate_domain_profile_fields(data)
    _validate_canvas_and_element_coordinates(data)
    _validate_unique_element_ids(data)
    _validate_answer_consistency(data)


def validate_layout(data: dict[str, Any]) -> None:
    validate_layout_json(data)


def validate_layout_diff(data: dict[str, Any]) -> None:
    validate_layout_diff_json(data)


def validate_order(data: dict[str, Any], profile: dict[str, Any], kind: str) -> None:
    if kind == "semantic":
        expected = profile["semantic_root_order"]
    elif kind == "layout":
        expected = profile["layout_root_order"]
    elif kind == "layout_diff":
        expected = profile["layout_diff_root_order"]
    else:
        raise BundleValidationError(f"Unsupported order kind: {kind}")

    present_expected = [k for k in expected if k in data]
    actual_prefix = list(data.keys())[: len(present_expected)]
    if actual_prefix != present_expected:
        raise BundleValidationError(
            f"Root key order mismatch for {kind}: expected prefix {present_expected}, got {actual_prefix}"
        )


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _validate_domain_profile_fields(data: dict[str, Any]) -> None:
    domain = data.get("domain")
    if not isinstance(domain, dict):
        return
    profile = domain.get("profile")
    if not isinstance(profile, str):
        return
    required = _PROFILE_REQUIRED_FIELDS.get(profile)
    if required is None:
        return
    missing = sorted([field for field in required if field not in domain])
    if missing:
        raise BundleValidationError(f"domain profile '{profile}' missing required fields: {missing}")


def _validate_canvas_and_element_coordinates(data: dict[str, Any]) -> None:
    render = data.get("render")
    if not isinstance(render, dict):
        return
    canvas = render.get("canvas")
    elements = render.get("elements")
    if not isinstance(canvas, dict) or not isinstance(elements, list):
        return

    width = canvas.get("width")
    height = canvas.get("height")
    if not isinstance(width, (int, float)) or width <= 0:
        raise BundleValidationError("render.canvas.width must be a positive number")
    if not isinstance(height, (int, float)) or height <= 0:
        raise BundleValidationError("render.canvas.height must be a positive number")

    for idx, element in enumerate(elements):
        if not isinstance(element, dict):
            continue
        for key in _COORD_KEYS:
            value = element.get(key)
            if isinstance(value, (int, float)) and not (0 <= value <= width):
                raise BundleValidationError(
                    f"render.elements[{idx}].{key}={value} is outside canvas width range [0, {width}]"
                )
        for key in _COORD_Y_KEYS:
            value = element.get(key)
            if isinstance(value, (int, float)) and not (0 <= value <= height):
                raise BundleValidationError(
                    f"render.elements[{idx}].{key}={value} is outside canvas height range [0, {height}]"
                )
        points = element.get("points")
        if isinstance(points, list):
            for p_idx, point in enumerate(points):
                if not (isinstance(point, list) and len(point) == 2):
                    continue
                x, y = point
                if isinstance(x, (int, float)) and not (0 <= x <= width):
                    raise BundleValidationError(
                        f"render.elements[{idx}].points[{p_idx}][0]={x} is outside canvas width range [0, {width}]"
                    )
                if isinstance(y, (int, float)) and not (0 <= y <= height):
                    raise BundleValidationError(
                        f"render.elements[{idx}].points[{p_idx}][1]={y} is outside canvas height range [0, {height}]"
                    )


def _validate_unique_element_ids(data: dict[str, Any]) -> None:
    render = data.get("render")
    if not isinstance(render, dict):
        return
    elements = render.get("elements")
    if not isinstance(elements, list):
        return
    seen: set[str] = set()
    for idx, element in enumerate(elements):
        if not isinstance(element, dict):
            continue
        element_id = element.get("id")
        if not isinstance(element_id, str):
            continue
        if element_id in seen:
            raise BundleValidationError(f"Duplicate render element id detected: {element_id} at index {idx}")
        seen.add(element_id)


def _validate_answer_consistency(data: dict[str, Any]) -> None:
    answer = data.get("answer")
    if not isinstance(answer, dict):
        return

    blanks = answer.get("blanks")
    choices = answer.get("choices")
    answer_key = answer.get("answer_key")
    if not isinstance(blanks, list) or not isinstance(choices, list) or not isinstance(answer_key, list):
        return

    blank_ids = {blank.get("id") for blank in blanks if isinstance(blank, dict) and isinstance(blank.get("id"), str)}

    for idx, key in enumerate(answer_key):
        if isinstance(key, int):
            if choices and not (0 <= key < len(choices)):
                raise BundleValidationError(
                    f"answer.answer_key[{idx}] choice index {key} is out of range for {len(choices)} choices"
                )
            continue
        if not isinstance(key, dict):
            continue
        blank_id = key.get("blank_id")
        if isinstance(blank_id, str) and blank_id not in blank_ids:
            raise BundleValidationError(
                f"answer.answer_key[{idx}].blank_id '{blank_id}' does not exist in answer.blanks"
            )
        choice_index = key.get("choice_index")
        if isinstance(choice_index, int) and choices and not (0 <= choice_index < len(choices)):
            raise BundleValidationError(
                f"answer.answer_key[{idx}].choice_index {choice_index} is out of range for {len(choices)} choices"
            )


def validate_problem_bundle(path: str | Path) -> list[str]:
    base = Path(path)
    errors: list[str] = []
    profile = load_contract_json("canonical_order_profile.json")

    semantic_path = base / "json" / "semantic_final" / "semantic_final.json"
    layout_path = base / "json" / "layout_final" / "layout_final.json"
    layout_diff_path = base / "json" / "layout_final" / "layout_diff.json"

    if not semantic_path.exists():
        errors.append(f"Missing semantic file: {semantic_path}")
    else:
        try:
            semantic = _read_json(semantic_path)
            validate_semantic(semantic)
            validate_order(semantic, profile, "semantic")
        except Exception as exc:  # noqa: BLE001
            errors.append(f"Semantic validation failed ({semantic_path}): {exc}")

    if layout_path.exists():
        try:
            layout = _read_json(layout_path)
            validate_layout(layout)
            validate_order(layout, profile, "layout")
        except Exception as exc:  # noqa: BLE001
            errors.append(f"Layout validation failed ({layout_path}): {exc}")

    if layout_diff_path.exists():
        try:
            layout_diff = _read_json(layout_diff_path)
            validate_layout_diff(layout_diff)
            validate_order(layout_diff, profile, "layout_diff")
        except Exception as exc:  # noqa: BLE001
            errors.append(f"Layout diff validation failed ({layout_diff_path}): {exc}")

    return errors


def validate_all_examples(root: str | Path = "examples/problem") -> dict[str, list[str]]:
    root_path = Path(root)
    failures: dict[str, list[str]] = {}
    if not root_path.exists():
        return failures

    for problem_dir in sorted([d for d in root_path.iterdir() if d.is_dir()], key=lambda p: p.name):
        errors = validate_problem_bundle(problem_dir)
        if errors:
            failures[str(problem_dir)] = errors
    return failures
