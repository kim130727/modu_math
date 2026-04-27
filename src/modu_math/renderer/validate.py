from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class RendererValidationError(Exception):
    pass

_DRAW_OP_TYPES = {
    "text",
    "rect",
    "line",
    "circle",
    "polygon",
    "arc",
    "formula",
    "image",
    "fill_path",
    "path",
    "group",
}


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
    if element["type"] not in _DRAW_OP_TYPES:
        raise RendererValidationError(
            f"{path}.type must be one of: {', '.join(sorted(_DRAW_OP_TYPES))}"
        )
    if not isinstance(element["attributes"], dict):
        raise RendererValidationError(f"{path}.attributes must be an object")
    if "source_ref" in element and (
        not isinstance(element["source_ref"], str) or not element["source_ref"].strip()
    ):
        raise RendererValidationError(f"{path}.source_ref must be a non-empty string when present")
    if "source_ref" in element["attributes"] and (
        not isinstance(element["attributes"]["source_ref"], str)
        or not str(element["attributes"]["source_ref"]).strip()
    ):
        raise RendererValidationError(f"{path}.attributes.source_ref must be a non-empty string when present")
    if "refs" in element:
        refs = element["refs"]
        if not isinstance(refs, dict):
            raise RendererValidationError(f"{path}.refs must be an object when present")
        for ref_key, ref_value in refs.items():
            if not isinstance(ref_value, str) or not ref_value.strip():
                raise RendererValidationError(f"{path}.refs.{ref_key} must be a non-empty string")

    element_type = element["type"]
    if element_type in {"text", "formula"}:
        if "text" not in element or not isinstance(element["text"], str):
            raise RendererValidationError(f"{path}.text must exist and be a string for {element_type} elements")
    if element_type == "group":
        children = element.get("elements")
        if not isinstance(children, list):
            raise RendererValidationError(f"{path}.elements must be an array for group elements")
        for idx, child in enumerate(children):
            _validate_element(child, f"{path}.elements[{idx}]")
    if element_type == "image":
        href = element["attributes"].get("href")
        if not isinstance(href, str) or not href.strip():
            raise RendererValidationError(f"{path}.attributes.href must be a non-empty string for image elements")


def validate_renderer_json(data: dict[str, Any]) -> None:
    if not isinstance(data, dict):
        raise RendererValidationError("renderer payload must be an object")

    profile_path = Path(__file__).resolve().parents[3] / "schema" / "contract" / "canonical_order_profile.json"
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

    seen_ids: set[str] = set()

    def walk(items: list[dict[str, Any]], path: str) -> None:
        for idx, item in enumerate(items):
            current_path = f"{path}[{idx}]"
            element_id = str(item.get("id"))
            if element_id in seen_ids:
                raise RendererValidationError(
                    f"{current_path}.id duplicates existing element id '{element_id}'"
                )
            seen_ids.add(element_id)
            if item.get("type") == "group":
                children = item.get("elements", [])
                if isinstance(children, list):
                    walk([child for child in children if isinstance(child, dict)], f"{current_path}.elements")

    walk([element for element in elements if isinstance(element, dict)], "$.elements")


def load_and_validate_renderer(path: Path) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    validate_renderer_json(data)
    return data
