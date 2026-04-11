from __future__ import annotations

from typing import Any

from ..contracts import canonicalize_layout_json, canonicalize_semantic_json


def _warn(warnings: list[str], message: str) -> None:
    if message not in warnings:
        warnings.append(message)


def convert_legacy_semantic(data: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    """Convert common legacy semantic payloads into canonical semantic v3 shape.

    The converter is intentionally conservative: it fills known defaults and records
    warnings for missing/ambiguous fields instead of guessing semantic meaning.
    """
    warnings: list[str] = []

    metadata = data.get("metadata") or data.get("meta") or {}
    if "meta" in data and "metadata" not in data:
        _warn(warnings, "Mapped root key 'meta' to 'metadata'.")

    converted = {
        "schema_version": data.get("schema_version", "modu_math.semantic.v3"),
        "render_contract_version": data.get("render_contract_version", "modu_math.render.v1"),
        "problem_id": data.get("problem_id", "unknown_problem"),
        "problem_type": data.get("problem_type", "custom"),
        "metadata": metadata if isinstance(metadata, dict) else {},
        "domain": data.get("domain", {}) if isinstance(data.get("domain", {}), dict) else {},
        "render": data.get("render", {}) if isinstance(data.get("render", {}), dict) else {},
        "answer": data.get("answer", {"blanks": [], "choices": [], "answer_key": []}),
    }

    if not converted["render"]:
        _warn(warnings, "Missing render object. Created empty render placeholder.")
        converted["render"] = {"canvas": {"width": 0, "height": 0, "background": "#F6F6F6"}, "elements": []}

    render = converted["render"]
    if "canvas" not in render:
        _warn(warnings, "Missing render.canvas. Filled default canvas.")
        render["canvas"] = {"width": 0, "height": 0, "background": "#F6F6F6"}
    if "elements" not in render:
        _warn(warnings, "Missing render.elements. Filled empty list.")
        render["elements"] = []
    else:
        normalized_elements: list[dict[str, Any]] = []
        for idx, element in enumerate(render["elements"]):
            if not isinstance(element, dict):
                normalized_elements.append({})
                _warn(warnings, f"render.elements[{idx}] must be object. Replaced with empty object.")
                continue
            item = dict(element)
            if item.get("type") == "formula" and "expr" not in item and "text" in item:
                item["expr"] = item.pop("text")
                _warn(warnings, f"Mapped legacy formula text -> expr at render.elements[{idx}].")
            normalized_elements.append(item)
        render["elements"] = normalized_elements

    if not isinstance(converted["answer"], dict):
        _warn(warnings, "answer must be object. Replaced with empty answer object.")
        converted["answer"] = {"blanks": [], "choices": [], "answer_key": []}

    answer = converted["answer"]
    answer.setdefault("blanks", [])
    answer.setdefault("choices", [])
    answer.setdefault("answer_key", [])

    return canonicalize_semantic_json(converted), warnings


def convert_legacy_layout(data: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    """Convert layout-ish legacy payload into canonical layout v1 shape."""
    warnings: list[str] = []

    metadata = data.get("metadata") or data.get("meta") or {}
    if "meta" in data and "metadata" not in data:
        _warn(warnings, "Mapped root key 'meta' to 'metadata'.")

    converted = {
        "schema_version": data.get("schema_version", "modu_math.layout.v1"),
        "problem_id": data.get("problem_id", "unknown_problem"),
        "metadata": metadata if isinstance(metadata, dict) else {},
        "canvas": data.get("canvas", {}) if isinstance(data.get("canvas", {}), dict) else {},
        "summary": data.get("summary", {}) if isinstance(data.get("summary", {}), dict) else {},
        "elements": data.get("elements", []) if isinstance(data.get("elements", []), list) else [],
    }

    if not converted["canvas"]:
        _warn(warnings, "Missing canvas. Filled with default values.")
        converted["canvas"] = {"width": 0, "height": 0, "viewBox": "0 0 0 0"}

    canvas = converted["canvas"]
    canvas.setdefault("width", 0)
    canvas.setdefault("height", 0)
    canvas.setdefault("viewBox", f"0 0 {float(canvas['width'])} {float(canvas['height'])}")

    return canonicalize_layout_json(converted), warnings
