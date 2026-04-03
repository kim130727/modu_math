from __future__ import annotations

from typing import Callable


ProblemValidator = Callable[[dict], list[str]]


REQUIRED_ROOT_KEYS = ("meta", "problem", "canvas", "elements")
REQUIRED_CANVAS_KEYS = ("width", "height", "background")
ALLOWED_ELEMENT_TYPES = {"text", "rect", "line"}


def validate_semantic(semantic: dict) -> list[str]:
    """
    Validate common semantic shape + problem-type specific payload.

    The function returns all issues at once so authors can fix multiple fields
    in one manual review pass.
    """
    errors: list[str] = []

    for key in REQUIRED_ROOT_KEYS:
        if key not in semantic:
            errors.append(f"missing root key: {key}")

    canvas = semantic.get("canvas", {})
    for key in REQUIRED_CANVAS_KEYS:
        if key not in canvas:
            errors.append(f"missing canvas key: {key}")

    elements = semantic.get("elements", [])
    if not isinstance(elements, list) or not elements:
        errors.append("elements must be a non-empty list")
    else:
        seen_ids: set[str] = set()
        for idx, element in enumerate(elements):
            errors.extend(_validate_element(element, idx, seen_ids))

    problem = semantic.get("problem", {})
    if isinstance(problem, dict):
        problem_type = problem.get("type")
        if isinstance(problem_type, str):
            errors.extend(_validate_problem_by_type(problem_type, problem))
        else:
            errors.append("problem.type must be a string")
    else:
        errors.append("problem must be an object")

    return errors


def _validate_element(element: dict, idx: int, seen_ids: set[str]) -> list[str]:
    errors: list[str] = []
    if not isinstance(element, dict):
        return [f"elements[{idx}] must be an object"]

    elem_id = element.get("id")
    if not isinstance(elem_id, str) or not elem_id.strip():
        errors.append(f"elements[{idx}].id must be a non-empty string")
    elif elem_id in seen_ids:
        errors.append(f"duplicate element id: {elem_id}")
    else:
        seen_ids.add(elem_id)

    elem_type = element.get("type")
    if elem_type not in ALLOWED_ELEMENT_TYPES:
        errors.append(f"elements[{idx}].type must be one of {sorted(ALLOWED_ELEMENT_TYPES)}")
        return errors

    if elem_type == "text":
        for key in ("text", "x", "y", "font_size"):
            if key not in element:
                errors.append(f"elements[{idx}] missing key for text: {key}")
    elif elem_type == "rect":
        for key in ("x", "y", "width", "height"):
            if key not in element:
                errors.append(f"elements[{idx}] missing key for rect: {key}")
    elif elem_type == "line":
        for key in ("x1", "y1", "x2", "y2"):
            if key not in element:
                errors.append(f"elements[{idx}] missing key for line: {key}")

    return errors


def _validate_problem_by_type(problem_type: str, problem: dict) -> list[str]:
    validators: dict[str, ProblemValidator] = {
        "fill_in_blank": _validate_fill_in_blank,
        "measure_length_with_ruler": _validate_measure_length_with_ruler,
    }
    validator = validators.get(problem_type)
    if validator is None:
        # Unknown types are allowed for forward compatibility.
        return []
    return validator(problem)


def _validate_fill_in_blank(problem: dict) -> list[str]:
    errors: list[str] = []
    if "instruction" not in problem:
        errors.append("fill_in_blank: missing instruction")
    question = problem.get("question", {})
    if not isinstance(question, dict):
        errors.append("fill_in_blank: question must be an object")
        return errors
    for key in ("left_seconds", "minutes", "blank_symbol", "unit_from", "unit_mid", "unit_to"):
        if key not in question:
            errors.append(f"fill_in_blank.question missing key: {key}")
    return errors


def _validate_measure_length_with_ruler(problem: dict) -> list[str]:
    errors: list[str] = []
    for key in ("instruction", "sub_instruction", "object_label", "ruler", "measurement"):
        if key not in problem:
            errors.append(f"measure_length_with_ruler: missing key {key}")

    ruler = problem.get("ruler", {})
    if isinstance(ruler, dict):
        for key in ("start_cm", "end_cm", "major_ticks", "minor_per_cm"):
            if key not in ruler:
                errors.append(f"measure_length_with_ruler.ruler missing key: {key}")

    measurement = problem.get("measurement", {})
    if isinstance(measurement, dict):
        for key in ("left_cm", "right_cm"):
            if key not in measurement:
                errors.append(f"measure_length_with_ruler.measurement missing key: {key}")

    return errors
