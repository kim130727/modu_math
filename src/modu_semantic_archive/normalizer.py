from __future__ import annotations

from typing import Any

from .contracts import canonicalize_layout_json, canonicalize_semantic_json, load_contract_json


def _apply_aliases(data: dict[str, Any], aliases: dict[str, str]) -> dict[str, Any]:
    normalized = dict(data)
    for old_key, new_key in aliases.items():
        if old_key in normalized and new_key not in normalized:
            normalized[new_key] = normalized.pop(old_key)
    return normalized


def _dict_or_empty(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list_or_empty(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _normalize_semantic_element(element: Any) -> dict[str, Any]:
    payload = _dict_or_empty(element)
    payload = _apply_aliases(
        payload,
        {
            "zIndex": "z_index",
            "role": "semantic_role",
            "strokeWidth": "stroke_width",
            "fontFamily": "font_family",
            "fontSize": "font_size",
            "fontWeight": "font_weight",
            "align": "alignment",
            "text_anchor": "anchor",
        },
    )

    etype = payload.get("type")
    if isinstance(etype, str):
        lowered = etype.lower()
        if lowered in {"math", "latex"}:
            payload["type"] = "formula"

    if payload.get("type") == "formula" and "expr" not in payload and "text" in payload:
        payload["expr"] = payload["text"]
        payload.pop("text", None)

    if payload.get("type") == "circle":
        if "cx" in payload and "x" not in payload:
            payload["x"] = payload.pop("cx")
        if "cy" in payload and "y" not in payload:
            payload["y"] = payload.pop("cy")

    return payload


def _normalize_semantic_render(render: Any) -> dict[str, Any]:
    render_obj = _dict_or_empty(render)
    render_obj = _apply_aliases(render_obj, {"items": "elements"})

    canvas = _dict_or_empty(render_obj.get("canvas"))
    if "bg" in canvas and "background" not in canvas:
        canvas["background"] = canvas.pop("bg")

    canvas.setdefault("width", 0)
    canvas.setdefault("height", 0)
    canvas.setdefault("background", "#F6F6F6")

    raw_elements = _list_or_empty(render_obj.get("elements"))
    render_obj["elements"] = [_normalize_semantic_element(el) for el in raw_elements]
    render_obj["canvas"] = canvas
    return render_obj


def _reorder_by_profile(data: dict[str, Any], order: list[str]) -> dict[str, Any]:
    reordered: dict[str, Any] = {}
    for key in order:
        if key in data:
            reordered[key] = data[key]
    for key, value in data.items():
        if key not in reordered:
            reordered[key] = value
    return reordered


def normalize_semantic(data: dict[str, Any]) -> dict[str, Any]:
    payload = _apply_aliases(
        _dict_or_empty(data),
        {
            "schemaVersion": "schema_version",
            "renderContractVersion": "render_contract_version",
            "problemId": "problem_id",
            "problemType": "problem_type",
            "meta": "metadata",
            "drawing": "render",
        },
    )

    payload.setdefault("schema_version", "modu_math.semantic.v3")
    payload.setdefault("render_contract_version", "modu_math.render.v1")
    payload.setdefault("problem_id", "unknown_problem")
    payload.setdefault("problem_type", "custom")
    payload["metadata"] = _dict_or_empty(payload.get("metadata"))
    payload["domain"] = _dict_or_empty(payload.get("domain"))
    payload["render"] = _normalize_semantic_render(payload.get("render"))

    answer = _dict_or_empty(payload.get("answer"))
    if "answerKey" in answer and "answer_key" not in answer:
        answer["answer_key"] = answer.pop("answerKey")
    answer.setdefault("blanks", [])
    answer.setdefault("choices", [])
    answer.setdefault("answer_key", [])
    answer["blanks"] = _list_or_empty(answer.get("blanks"))
    answer["choices"] = _list_or_empty(answer.get("choices"))
    answer["answer_key"] = _list_or_empty(answer.get("answer_key"))
    payload["answer"] = answer

    return canonicalize_semantic_json(payload)


def normalize_layout(data: dict[str, Any]) -> dict[str, Any]:
    payload = _apply_aliases(
        _dict_or_empty(data),
        {
            "schemaVersion": "schema_version",
            "problemId": "problem_id",
            "meta": "metadata",
        },
    )

    payload.setdefault("schema_version", "modu_math.layout.v1")
    payload.setdefault("problem_id", "unknown_problem")
    payload["metadata"] = _dict_or_empty(payload.get("metadata"))

    canvas = _dict_or_empty(payload.get("canvas"))
    if "viewbox" in canvas and "viewBox" not in canvas:
        canvas["viewBox"] = canvas.pop("viewbox")
    canvas.setdefault("width", 0)
    canvas.setdefault("height", 0)
    canvas.setdefault("viewBox", f"0 0 {float(canvas['width'])} {float(canvas['height'])}")
    payload["canvas"] = canvas

    payload["summary"] = _dict_or_empty(payload.get("summary"))
    payload["elements"] = _list_or_empty(payload.get("elements"))
    return canonicalize_layout_json(payload)


def normalize_layout_diff(data: dict[str, Any]) -> dict[str, Any]:
    payload = _apply_aliases(
        _dict_or_empty(data),
        {
            "schemaVersion": "schema_version",
            "problemId": "problem_id",
            "meta": "metadata",
        },
    )
    payload.setdefault("schema_version", "modu_math.layout_diff.v1")
    payload.setdefault("problem_id", "unknown_problem")
    payload["metadata"] = _dict_or_empty(payload.get("metadata"))
    payload["diff"] = _dict_or_empty(payload.get("diff"))
    payload["metrics"] = _dict_or_empty(payload.get("metrics"))

    profile = load_contract_json("canonical_order_profile.json")
    return _reorder_by_profile(payload, profile["layout_diff_root_order"])
