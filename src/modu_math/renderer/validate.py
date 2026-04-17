from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class RendererValidationError(Exception):
    pass


def _ensure_keys_in_order(data: dict[str, Any], ordered_keys: list[str], path: str) -> None:
    actual = list(data.keys())
    cursor = 0
    for expected in ordered_keys:
        if expected not in data:
            continue
        while cursor < len(actual) and actual[cursor] != expected:
            cursor += 1
        if cursor >= len(actual):
            raise RendererValidationError(
                f"{path} key order mismatch: expected '{expected}' after previous keys"
            )
        cursor += 1


def _validate_element(element: dict[str, Any], path: str) -> None:
    if not isinstance(element, dict):
        raise RendererValidationError(f"{path} must be an object")

    required = ["id", "type", "attributes"]
    for key in required:
        if key not in element:
            raise RendererValidationError(f"{path} missing required key '{key}'")

    if not isinstance(element["id"], str) or not element["id"]:
        raise RendererValidationError(f"{path}.id must be a non-empty string")
    if not isinstance(element["type"], str) or not element["type"]:
        raise RendererValidationError(f"{path}.type must be a non-empty string")
    if not isinstance(element["attributes"], dict):
        raise RendererValidationError(f"{path}.attributes must be an object")

    element_type = element["type"]
    if element_type == "text":
        if "text" not in element or not isinstance(element["text"], str):
            raise RendererValidationError(f"{path}.text must exist and be a string for text elements")
    if element_type == "group":
        children = element.get("elements")
        if not isinstance(children, list):
            raise RendererValidationError(f"{path}.elements must be an array for group elements")
        for idx, child in enumerate(children):
            _validate_element(child, f"{path}.elements[{idx}]")


def validate_renderer_json(data: dict[str, Any]) -> None:
    if not isinstance(data, dict):
        raise RendererValidationError("renderer payload must be an object")

    profile_path = Path("c:/projects/modu_math/schema/contract/canonical_order_profile.json")
    if profile_path.exists():
        profile = json.loads(profile_path.read_text(encoding="utf-8"))
        root_order = profile.get("renderer_root_order")
        if isinstance(root_order, list):
            _ensure_keys_in_order(data, [str(key) for key in root_order], "$")

        if isinstance(data.get("view_box"), dict):
            view_box_order = profile.get("view_box_order")
            if isinstance(view_box_order, list):
                _ensure_keys_in_order(
                    data["view_box"],
                    [str(key) for key in view_box_order],
                    "$.view_box",
                )

    if "problem_id" not in data or not isinstance(data["problem_id"], str) or not data["problem_id"]:
        raise RendererValidationError("Missing or invalid 'problem_id'")

    view_box = data.get("view_box")
    if not isinstance(view_box, dict):
        raise RendererValidationError("'view_box' must be an object")
    if "width" not in view_box or not isinstance(view_box["width"], (int, float)):
        raise RendererValidationError("'view_box.width' must be a number")
    if "height" not in view_box or not isinstance(view_box["height"], (int, float)):
        raise RendererValidationError("'view_box.height' must be a number")
    if "background" in view_box and view_box["background"] is not None and not isinstance(view_box["background"], str):
        raise RendererValidationError("'view_box.background' must be a string when present")

    elements = data.get("elements")
    if not isinstance(elements, list):
        raise RendererValidationError("'elements' must be an array")

    for idx, element in enumerate(elements):
        _validate_element(element, f"$.elements[{idx}]")


def load_and_validate_renderer(path: Path) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    validate_renderer_json(data)
    return data
