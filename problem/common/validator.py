from __future__ import annotations

from typing import Callable


ProblemValidator = Callable[[dict], list[str]]


REQUIRED_ROOT_KEYS = ("meta", "problem", "canvas", "elements")
REQUIRED_CANVAS_KEYS = ("width", "height", "background")
ALLOWED_ELEMENT_TYPES = {"text", "rect", "line"}


def validate_semantic(semantic: dict) -> list[str]:
    """Backward-compatible wrapper: structure + logic validation."""
    return [
        *validate_structure(semantic),
        *validate_logic(semantic),
    ]


def validate_structure(semantic: dict) -> list[str]:
    """
    Validate semantic schema/shape only.

    This checks required keys, field types, and allowed element attributes.
    It intentionally does not validate math correctness.
    """
    errors: list[str] = []

    if not isinstance(semantic, dict):
        return ["semantic must be an object"]

    for key in REQUIRED_ROOT_KEYS:
        if key not in semantic:
            errors.append(f"missing root key: {key}")

    canvas = semantic.get("canvas", {})
    if not isinstance(canvas, dict):
        errors.append("canvas must be an object")
    else:
        for key in REQUIRED_CANVAS_KEYS:
            if key not in canvas:
                errors.append(f"missing canvas key: {key}")

    elements = semantic.get("elements", [])
    if not isinstance(elements, list) or not elements:
        errors.append("elements must be a non-empty list")
    else:
        seen_ids: set[str] = set()
        for idx, element in enumerate(elements):
            errors.extend(_validate_element_structure(element, idx, seen_ids))

    problem = semantic.get("problem", {})
    if not isinstance(problem, dict):
        errors.append("problem must be an object")
    elif not isinstance(problem.get("type"), str):
        errors.append("problem.type must be a string")

    return errors


def validate_logic(semantic: dict) -> list[str]:
    """
    Validate domain/math correctness only.

    Examples:
    - unit conversion consistency
    - ruler measurement consistency
    """
    errors: list[str] = []

    if not isinstance(semantic, dict):
        return ["semantic must be an object"]

    problem = semantic.get("problem", {})
    if not isinstance(problem, dict):
        return ["problem must be an object"]

    problem_type = problem.get("type")
    if not isinstance(problem_type, str):
        return ["problem.type must be a string"]

    validators: dict[str, ProblemValidator] = {
        "fill_in_blank": _validate_fill_in_blank_logic,
        "measure_length_with_ruler": _validate_measure_length_with_ruler_logic,
    }
    validator = validators.get(problem_type)
    if validator is None:
        # Unknown types are allowed for forward compatibility.
        return []

    errors.extend(validator(problem))
    errors.extend(_validate_blank_element_consistency(problem_type, semantic.get("elements", [])))
    return errors


def _validate_element_structure(element: dict, idx: int, seen_ids: set[str]) -> list[str]:
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

    semantic_role = element.get("semantic_role")
    if not isinstance(semantic_role, str) or not semantic_role.strip():
        errors.append(f"elements[{idx}].semantic_role must be a non-empty string")

    group = element.get("group")
    if group is not None and not isinstance(group, str):
        errors.append(f"elements[{idx}].group must be a string when provided")

    answer_blank = element.get("answer_blank")
    if answer_blank is not None and not isinstance(answer_blank, bool):
        errors.append(f"elements[{idx}].answer_blank must be a boolean when provided")

    figure_type = element.get("figure_type")
    if figure_type is not None and not isinstance(figure_type, str):
        errors.append(f"elements[{idx}].figure_type must be a string when provided")

    choice = element.get("choice")
    if choice is not None:
        if not isinstance(choice, dict):
            errors.append(f"elements[{idx}].choice must be an object when provided")
        else:
            if "value" not in choice:
                errors.append(f"elements[{idx}].choice missing key: value")
            if "index" in choice and not isinstance(choice["index"], int):
                errors.append(f"elements[{idx}].choice.index must be an integer")

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


def _validate_blank_element_consistency(problem_type: str, elements: object) -> list[str]:
    errors: list[str] = []
    if problem_type != "fill_in_blank":
        return errors
    if not isinstance(elements, list):
        return ["elements must be a list"]

    blank_count = sum(1 for e in elements if isinstance(e, dict) and e.get("answer_blank") is True)
    if blank_count != 1:
        errors.append(f"fill_in_blank requires exactly 1 answer_blank element, found {blank_count}")
    return errors


def _validate_fill_in_blank_logic(problem: dict) -> list[str]:
    errors: list[str] = []

    question = problem.get("question", {})
    if not isinstance(question, dict):
        return ["fill_in_blank: question must be an object"]

    for key in ("left_seconds", "minutes", "blank_symbol", "unit_from", "unit_mid", "unit_to"):
        if key not in question:
            errors.append(f"fill_in_blank.question missing key: {key}")

    left_seconds = question.get("left_seconds")
    minutes = question.get("minutes")
    answer = problem.get("answer")

    if isinstance(left_seconds, (int, float)) and isinstance(minutes, (int, float)) and isinstance(answer, (int, float)):
        expected = left_seconds - minutes * 60
        if abs(expected - answer) > 1e-9:
            errors.append(
                f"fill_in_blank logic mismatch: expected answer {expected}, got {answer}"
            )

    errors.extend(_validate_choices(problem, expected_answer=answer))

    return errors


def _validate_measure_length_with_ruler_logic(problem: dict) -> list[str]:
    errors: list[str] = []

    ruler = problem.get("ruler", {})
    measurement = problem.get("measurement", {})

    for key in ("instruction", "sub_instruction", "object_label", "ruler", "measurement"):
        if key not in problem:
            errors.append(f"measure_length_with_ruler: missing key {key}")

    if not isinstance(ruler, dict):
        return errors + ["measure_length_with_ruler.ruler must be an object"]
    if not isinstance(measurement, dict):
        return errors + ["measure_length_with_ruler.measurement must be an object"]

    for key in ("start_cm", "end_cm", "major_ticks", "minor_per_cm"):
        if key not in ruler:
            errors.append(f"measure_length_with_ruler.ruler missing key: {key}")

    for key in ("left_cm", "right_cm"):
        if key not in measurement:
            errors.append(f"measure_length_with_ruler.measurement missing key: {key}")

    start_cm = ruler.get("start_cm")
    end_cm = ruler.get("end_cm")
    if isinstance(start_cm, (int, float)) and isinstance(end_cm, (int, float)) and not (start_cm < end_cm):
        errors.append("measure_length_with_ruler: ruler.start_cm must be less than ruler.end_cm")

    left_cm = measurement.get("left_cm")
    right_cm = measurement.get("right_cm")
    answer_mm = problem.get("answer_mm")

    if isinstance(left_cm, (int, float)) and isinstance(right_cm, (int, float)):
        if not (left_cm < right_cm):
            errors.append("measure_length_with_ruler: measurement.left_cm must be less than measurement.right_cm")
        if isinstance(answer_mm, (int, float)):
            expected_mm = round((right_cm - left_cm) * 10)
            if abs(answer_mm - expected_mm) > 1e-9:
                errors.append(
                    f"measure_length_with_ruler logic mismatch: expected answer_mm {expected_mm}, got {answer_mm}"
                )

    errors.extend(_validate_choices(problem, expected_answer=answer_mm))

    return errors


def _validate_choices(problem: dict, expected_answer: object) -> list[str]:
    errors: list[str] = []
    choices = problem.get("choices")
    if choices is None:
        return errors
    if not isinstance(choices, list) or not choices:
        return ["choices must be a non-empty list when provided"]

    correct_choices = [c for c in choices if isinstance(c, dict) and c.get("is_correct") is True]
    if len(correct_choices) != 1:
        errors.append(f"choices must contain exactly one correct option, found {len(correct_choices)}")
        return errors

    if expected_answer is not None:
        correct_value = str(correct_choices[0].get("value"))
        if correct_value != str(expected_answer):
            errors.append(
                f"choices correct value mismatch: expected {expected_answer}, got {correct_value}"
            )
    return errors
