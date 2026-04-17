from __future__ import annotations

from collections import Counter
from typing import Any

from .contracts import canonicalize_layout_json, canonicalize_semantic_json
from .ir import Circle, Element, Formula, Line, Polygon, ProblemIR, Rect, Text


def _clean_none(data: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in data.items() if v is not None}


def _anchor_from_alignment(anchor: str, alignment: str) -> str:
    if anchor:
        return anchor
    mapping = {"left": "start", "center": "middle", "right": "end"}
    return mapping.get(alignment, "start")


def _base_element_dict(element: Element) -> dict[str, Any]:
    metadata = element.metadata if isinstance(element.metadata, dict) else {}
    return _clean_none(
        {
            "id": element.id,
            "group": element.group,
            "metadata": metadata if metadata else None,
            "semantic_role": element.semantic_role,
            "z_index": element.z_index,
            "anchor": _anchor_from_alignment(element.anchor, element.alignment),
            "alignment": element.alignment,
            "stroke": element.stroke,
            "stroke_width": element.stroke_width,
            "fill": element.fill,
            "font_family": element.font_family,
            "font_size": element.font_size,
            "font_weight": element.font_weight,
        }
    )


def _element_to_semantic_dict(element: Element) -> dict[str, Any]:
    payload = _base_element_dict(element)

    if isinstance(element, Rect):
        payload.update(
            _clean_none(
                {
                    "type": "rect",
                    "x": element.x,
                    "y": element.y,
                    "width": element.width,
                    "height": element.height,
                    "rx": element.rx,
                    "ry": element.ry,
                }
            )
        )
    elif isinstance(element, Circle):
        payload.update({"type": "circle", "x": element.x, "y": element.y, "r": element.r})
    elif isinstance(element, Line):
        payload.update(
            {"type": "line", "x1": element.x1, "y1": element.y1, "x2": element.x2, "y2": element.y2}
        )
    elif isinstance(element, Polygon):
        payload.update({"type": "polygon", "points": [[x, y] for x, y in element.points]})
    elif isinstance(element, Text):
        payload.update({"type": "text", "text": element.text, "x": element.x, "y": element.y})
    elif isinstance(element, Formula):
        payload.update({"type": "formula", "expr": element.expr, "x": element.x, "y": element.y})
    else:
        raise TypeError(f"Unsupported element type: {type(element)!r}")

    return payload


def _stringify_attrs(data: dict[str, Any]) -> dict[str, str]:
    attrs: dict[str, str] = {}
    for key, value in data.items():
        if key in {"type", "z_index", "group", "metadata", "semantic_role", "alignment", "anchor"}:
            continue
        if value is None:
            continue
        normalized = key.replace("_", "-")
        if isinstance(value, (list, tuple)):
            if normalized == "points":
                attrs[normalized] = " ".join([f"{pt[0]},{pt[1]}" for pt in value])
            else:
                attrs[normalized] = str(value)
        else:
            attrs[normalized] = str(value)
    return attrs


def _normalize_number(value: float) -> int | float:
    i = int(value)
    return i if value == i else value


def _layout_geometry_fields(el: dict[str, Any]) -> tuple[float, float, float, float]:
    etype = el["type"]
    if etype == "rect":
        return (
            float(el.get("x", 0)),
            float(el.get("y", 0)),
            float(el.get("width", 0)),
            float(el.get("height", 0)),
        )
    if etype in {"text", "formula"}:
        return float(el.get("x", 0)), float(el.get("y", 0)), 0.0, 0.0
    if etype == "circle":
        r = float(el.get("r", 0))
        cx = float(el.get("x", 0))
        cy = float(el.get("y", 0))
        return cx - r, cy - r, r * 2, r * 2
    if etype == "line":
        x1 = float(el.get("x1", 0))
        y1 = float(el.get("y1", 0))
        x2 = float(el.get("x2", 0))
        y2 = float(el.get("y2", 0))
        return min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1)
    if etype == "polygon":
        points = el.get("points", [])
        if not points:
            return 0.0, 0.0, 0.0, 0.0
        xs = [float(p[0]) for p in points]
        ys = [float(p[1]) for p in points]
        min_x = min(xs)
        min_y = min(ys)
        return min_x, min_y, max(xs) - min_x, max(ys) - min_y
    return 0.0, 0.0, 0.0, 0.0


def _sorted_render_elements(problem: ProblemIR) -> list[dict[str, Any]]:
    sorted_elements = sorted(problem.elements, key=lambda e: e.z_index)
    return [_element_to_semantic_dict(el) for el in sorted_elements]


def _normalize_answer(answer: dict[str, Any] | None) -> dict[str, Any]:
    payload = answer if isinstance(answer, dict) else {}
    return {
        "blanks": list(payload.get("blanks", [])),
        "choices": list(payload.get("choices", [])),
        "answer_key": list(payload.get("answer_key", [])),
    }


def _normalize_metadata(metadata: dict[str, Any] | None) -> dict[str, Any]:
    base = {
        "source": {"input_type": "python_dsl", "generator": "modu_semantic"},
        "warnings": [],
    }
    if not isinstance(metadata, dict):
        return base
    merged = dict(base)
    merged.update(metadata)
    return merged


def compile_semantic_json(
    problem: ProblemIR,
    *,
    schema_version: str = "modu_math.semantic.v3",
    render_contract_version: str = "modu_math.render.v1",
    title: str | None = None,
    metadata: dict[str, Any] | None = None,
    domain: dict[str, Any] | None = None,
    answer: dict[str, Any] | None = None,
) -> dict[str, Any]:
    render_elements = _sorted_render_elements(problem)

    payload = {
        "schema_version": schema_version,
        "render_contract_version": render_contract_version,
        "problem_id": problem.problem_id,
        "problem_type": problem.problem_type,
        "metadata": _normalize_metadata(metadata),
        "domain": dict(domain) if isinstance(domain, dict) else {},
        "render": {
            "canvas": {
                "width": float(problem.width),
                "height": float(problem.height),
                "background": problem.background,
            },
            "elements": render_elements,
        },
        "answer": _normalize_answer(answer),
    }
    if title:
        payload["title"] = title
    return canonicalize_semantic_json(payload)


def compile_layout_json(
    problem: ProblemIR,
    *,
    metadata: dict[str, Any] | None = None,
    title: str | None = None,
    schema_version: str = "modu_math.layout.v1",
    render_contract_version: str = "modu_math.render.v1",
) -> dict[str, Any]:
    render_elements = _sorted_render_elements(problem)

    layout_elements: list[dict[str, Any]] = [
        {
            "index": 1,
            "id": None,
            "type": "rect",
            "x": 0,
            "y": 0,
            "width": problem.width,
            "height": problem.height,
            "attrs": {
                "x": "0",
                "y": "0",
                "width": str(float(problem.width)),
                "height": str(float(problem.height)),
                "fill": problem.background,
            },
        }
    ]

    for idx, el in enumerate(render_elements, start=2):
        x, y, w, h = _layout_geometry_fields(el)
        layout_type = "text" if el["type"] == "formula" else el["type"]

        item = {
            "index": idx,
            "id": el.get("id"),
            "type": layout_type,
            "x": _normalize_number(x),
            "y": _normalize_number(y),
            "width": _normalize_number(w),
            "height": _normalize_number(h),
            "attrs": _stringify_attrs(el),
        }
        if "text" in el:
            item["text"] = el["text"]
            if "font_size" in el:
                item["font_size"] = el["font_size"]
        if "expr" in el:
            item["text"] = el["expr"]
            if "font_size" in el:
                item["font_size"] = el["font_size"]
        layout_elements.append(item)

    type_counts = Counter([e["type"] for e in layout_elements])
    with_id = sum(1 for e in layout_elements if e.get("id"))

    payload = {
        "schema_version": schema_version,
        "problem_id": problem.problem_id,
        "metadata": {
            "source_svg": "generated://modu_semantic/semantic_final.svg",
            "generator": "modu_semantic.compiler_json.compile_layout_json",
        },
        "canvas": {
            "width": problem.width,
            "height": problem.height,
            "viewBox": f"0 0 {float(problem.width)} {float(problem.height)}",
        },
        "summary": {
            "total_elements": len(layout_elements),
            "count_by_type": dict(type_counts),
            "with_id": with_id,
            "without_id": len(layout_elements) - with_id,
        },
        "elements": layout_elements,
    }
    if isinstance(metadata, dict) and metadata:
        payload["metadata"]["problem_metadata"] = metadata
    if title:
        payload["metadata"]["title"] = title
    return canonicalize_layout_json(payload)
