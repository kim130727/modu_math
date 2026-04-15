from __future__ import annotations

import json
import pprint
import re
from html import escape
from dataclasses import replace
from pathlib import Path
from typing import Any

from . import ir
from .semantic_geometry import (
    build_angle_marker_elements,
    build_circle_elements,
    build_geometry_reconstruction_elements,
    build_geometry_template_elements,
    build_length_dimension_elements,
    build_parallel_marker_elements,
    build_perpendicular_marker_elements,
    build_equal_length_tick_elements,
    extract_logic_form,
    has_geometry_diagram_data,
    parse_angle_constraints,
    parse_circle_constraints,
    parse_point_on_line_constraints,
    parse_line_instances,
    parse_length_constraints,
    parse_equal_segment_constraints,
    parse_parallel_constraints,
    parse_perpendicular_constraints,
    parse_point_positions,
    simplify_collinear_edges,
    apply_point_on_line_constraints,
    auto_snap_points_to_segments,
)
from .normalizer import normalize_semantic
from .orderer import order_semantic
from .problem import Problem
from .schema import validate_semantic_json


_CANONICAL_TYPES = {"rect", "circle", "line", "polygon", "text", "formula"}
_SUPPORTED_TYPES = set(_CANONICAL_TYPES) | {"problem_text", "multiple_choice", "diagram_logic"}
_DEFAULT_SCHEMA_VERSION = "modu_math.semantic.v3"
_DEFAULT_RENDER_CONTRACT_VERSION = "modu_math.render.v1"
_DEFAULT_FONT_SCALE = 3.0
_PROBLEM_TEXT_MAX_SCALE = 2.0
_MAX_RENDER_FONT_SIZE = 48.0
_WRAPPED_ID_RE = re.compile(r"^(.*?)(?:_ln\d+)+$")


def _is_geometry_render_artifact(element: dict[str, Any]) -> bool:
    role = _to_str(element.get("semantic_role")).strip().lower()
    element_id = _to_str(element.get("id")).strip().lower()
    if role.startswith("geometry_"):
        return True
    if element_id.startswith("geom_"):
        return True
    return False


def _scaled_font_value(size: float, scale: float) -> float:
    return min(_MAX_RENDER_FONT_SIZE, max(1.0, size * scale))


def _effective_text_scale(element: dict[str, Any], default_scale: float) -> float:
    element_id = _to_str(element.get("id"))
    element_type = _to_str(element.get("type"))
    if "_ln" in element_id:
        return 1.0
    if element_type in {"problem_text", "multiple_choice", "diagram_logic"}:
        return min(default_scale, _PROBLEM_TEXT_MAX_SCALE)
    return default_scale


def _base_id_if_wrapped(element_id: str) -> str | None:
    m = _WRAPPED_ID_RE.match(element_id)
    if not m:
        return None
    base = m.group(1).strip()
    return base or None


def _normalize_math_markup(text: str) -> str:
    if not text:
        return ""
    out = str(text)

    # frac{a}{b} / \frac{a}{b} -> a⁄b
    frac_pattern = re.compile(r"\\?frac\{([^{}]+)\}\{([^{}]+)\}")
    for _ in range(8):
        next_out = frac_pattern.sub(lambda m: f"{m.group(1).strip()}⁄{m.group(2).strip()}", out)
        if next_out == out:
            break
        out = next_out

    # sqrt{x} / \sqrt{x} -> √(x)
    sqrt_pattern = re.compile(r"\\?sqrt\{([^{}]+)\}")
    for _ in range(8):
        next_out = sqrt_pattern.sub(lambda m: f"√({m.group(1).strip()})", out)
        if next_out == out:
            break
        out = next_out

    out = out.replace("*", "×")
    return out


def _translate_logic_expression(line: str) -> str:
    text = _normalize_math_markup(line)
    stripped = text.strip()
    m_find = re.fullmatch(r"Find\((.+)\)", stripped)
    if m_find:
        text = m_find.group(1).strip() + " 구하기"

    text = re.sub(
        r"LengthOf\(Line\(([A-Za-z]),\s*([A-Za-z])\)\)",
        lambda m: f"{m.group(1)}{m.group(2)}선 길이",
        text,
    )
    text = re.sub(
        r"Line\(([A-Za-z]),\s*([A-Za-z])\)",
        lambda m: f"{m.group(1)}{m.group(2)}선",
        text,
    )
    text = re.sub(
        r"AreaOf\(Triangle\(([A-Za-z]),\s*([A-Za-z]),\s*([A-Za-z])\)\)",
        lambda m: f"△{m.group(1)}{m.group(2)}{m.group(3)} 넓이",
        text,
    )
    text = re.sub(r"AreaOf\(Shape\(\$\)\)", "도형 넓이", text)
    text = re.sub(
        r"PointLiesOnLine\(([A-Za-z]),\s*([^)]+)\)",
        lambda m: f"점 {m.group(1)}는 {m.group(2)} 위",
        text,
    )
    text = re.sub(
        r"Perpendicular\(([^,]+),\s*([^)]+)\)",
        lambda m: f"{m.group(1).strip()} ⟂ {m.group(2).strip()}",
        text,
    )
    text = re.sub(
        r"Parallel\(([^,]+),\s*([^)]+)\)",
        lambda m: f"{m.group(1).strip()} ∥ {m.group(2).strip()}",
        text,
    )
    text = re.sub(
        r"Equals\(([^,]+),\s*([^)]+)\)",
        lambda m: f"{m.group(1).strip()} = {m.group(2).strip()}",
        text,
    )
    text = re.sub(r"Find\((.+?)\)", lambda m: f"{m.group(1).strip()} 구하기", text)
    return text


def _normalize_text_value(text: str) -> str:
    raw = _normalize_math_markup(text)
    if any(token in raw for token in ("LengthOf(", "Line(", "PointLiesOnLine(", "Perpendicular(", "Parallel(", "Equals(", "Find(")):
        return _translate_logic_expression(raw)
    return raw


def _normalize_string_tree(value: Any) -> Any:
    if isinstance(value, str):
        return _normalize_text_value(value)
    if isinstance(value, list):
        return [_normalize_string_tree(v) for v in value]
    if isinstance(value, dict):
        return {k: _normalize_string_tree(v) for k, v in value.items()}
    return value


def _to_float(value: Any, *, default: float = 0.0) -> float:
    if isinstance(value, bool):
        return default
    if isinstance(value, (int, float)):
        return float(value)
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _to_int(value: Any, *, default: int = 0) -> int:
    if isinstance(value, bool):
        return default
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def _to_str(value: Any, *, default: str = "") -> str:
    if value is None:
        return default
    return str(value)


def _to_dict(value: Any) -> dict[str, Any]:
    return dict(value) if isinstance(value, dict) else {}


def _to_points(value: Any) -> list[tuple[float, float]]:
    points: list[tuple[float, float]] = []
    if not isinstance(value, list):
        return points
    for item in value:
        if not isinstance(item, (list, tuple)) or len(item) != 2:
            continue
        points.append((_to_float(item[0]), _to_float(item[1])))
    return points


def _common_attrs(element: dict[str, Any]) -> dict[str, Any]:
    metadata_raw = element.get("metadata")
    metadata = dict(metadata_raw) if isinstance(metadata_raw, dict) else {}
    return {
        "id": _to_str(element.get("id"), default=""),
        "group": _to_str(element.get("group"), default="") or None,
        "metadata": metadata,
        "z_index": _to_int(element.get("z_index"), default=0),
        "anchor": _to_str(element.get("anchor"), default="start") or "start",
        "alignment": _to_str(element.get("alignment"), default="left") or "left",
        "semantic_role": _to_str(element.get("semantic_role"), default="") or None,
        "stroke": _to_str(element.get("stroke"), default="") or None,
        "stroke_width": _to_float(element.get("stroke_width"), default=0.0)
        if element.get("stroke_width") is not None
        else None,
        "fill": _to_str(element.get("fill"), default="") or None,
        "font_family": _to_str(element.get("font_family"), default="") or None,
        "font_size": _to_float(element.get("font_size"), default=0.0)
        if element.get("font_size") is not None
        else None,
        "font_weight": _to_str(element.get("font_weight"), default="") or None,
    }


def _element_from_semantic(
    element: dict[str, Any],
    *,
    fallback_y: float = 80.0,
    font_scale: float = _DEFAULT_FONT_SCALE,
) -> ir.Element:
    element_type = _to_str(element.get("type"))
    attrs = _common_attrs(element)
    text_scale = _effective_text_scale(element, font_scale)

    if element_type == "rect":
        return ir.Rect(
            **attrs,
            x=_to_float(element.get("x")),
            y=_to_float(element.get("y")),
            width=_to_float(element.get("width")),
            height=_to_float(element.get("height")),
            rx=_to_float(element.get("rx")) if element.get("rx") is not None else None,
            ry=_to_float(element.get("ry")) if element.get("ry") is not None else None,
        )
    if element_type == "circle":
        return ir.Circle(
            **attrs,
            x=_to_float(element.get("x")),
            y=_to_float(element.get("y")),
            r=_to_float(element.get("r")),
        )
    if element_type == "line":
        return ir.Line(
            **attrs,
            x1=_to_float(element.get("x1")),
            y1=_to_float(element.get("y1")),
            x2=_to_float(element.get("x2")),
            y2=_to_float(element.get("y2")),
        )
    if element_type == "polygon":
        return ir.Polygon(
            **attrs,
            points=_to_points(element.get("points")),
        )
    if element_type == "text":
        font_size = attrs["font_size"]
        if font_size is not None:
            attrs["font_size"] = _scaled_font_value(float(font_size), text_scale)
        semantic_role = _to_str(attrs.get("semantic_role")).strip().lower()
        if semantic_role == "problem_text":
            x_value = 40.0
        elif semantic_role == "multiple_choice":
            x_value = 860.0
        else:
            x_value = _to_float(element.get("x"), default=0.0)
        y_default = fallback_y if semantic_role in {"problem_text", "multiple_choice", "diagram_logic"} else 0.0
        y_value = _to_float(element.get("y"), default=y_default)
        if semantic_role == "multiple_choice":
            y_value = max(320.0, y_value)
        return ir.Text(
            **attrs,
            x=x_value,
            y=y_value,
            text=_normalize_text_value(_to_str(element.get("text"))),
        )
    if element_type == "formula":
        font_size = attrs["font_size"]
        if font_size is not None:
            attrs["font_size"] = _scaled_font_value(float(font_size), text_scale)
        expr = element.get("expr")
        if expr is None:
            expr = element.get("text")
        return ir.Formula(
            **attrs,
            x=_to_float(element.get("x")),
            y=_to_float(element.get("y")),
            expr=_normalize_text_value(_to_str(expr)),
        )
    if element_type == "problem_text":
        custom_attrs = dict(attrs)
        custom_attrs["semantic_role"] = attrs["semantic_role"] or "problem_text"
        base_size = custom_attrs["font_size"] if custom_attrs["font_size"] is not None else 16.0
        custom_attrs["font_size"] = _scaled_font_value(float(base_size), text_scale)
        return ir.Text(
            **custom_attrs,
            x=40.0,
            y=fallback_y,
            text=_normalize_text_value(_to_str(element.get("text"))),
        )
    if element_type == "multiple_choice":
        choices = element.get("choices")
        rendered_choices: list[str] = []
        if isinstance(choices, list):
            for idx, choice in enumerate(choices, start=1):
                rendered_choices.append(f"no.{idx} {_normalize_text_value(_to_str(choice))}")
        joined = " / ".join(rendered_choices)
        custom_attrs = dict(attrs)
        custom_attrs["semantic_role"] = attrs["semantic_role"] or "multiple_choice"
        base_size = attrs["font_size"] if attrs["font_size"] is not None else 16.0
        custom_attrs["font_size"] = _scaled_font_value(float(base_size), text_scale)
        return ir.Text(
            **custom_attrs,
            x=860.0,
            y=max(320.0, fallback_y),
            text=joined if joined else "choices",
        )
    if element_type == "diagram_logic":
        logic_form = element.get("diagram_logic_form")
        lines: list[str] = []
        if isinstance(logic_form, list):
            for line in logic_form[:3]:
                lines.append(_translate_logic_expression(_to_str(line)))
        summary = " | ".join(lines) if lines else "diagram_logic"
        custom_attrs = dict(attrs)
        custom_attrs["semantic_role"] = attrs["semantic_role"] or "diagram_logic"
        custom_attrs["metadata"] = {
            **attrs["metadata"],
            "source_type": "diagram_logic",
        }
        base_size = attrs["font_size"] if attrs["font_size"] is not None else 14.0
        custom_attrs["font_size"] = _scaled_font_value(float(base_size), text_scale)
        return ir.Text(
            **custom_attrs,
            x=40.0,
            y=fallback_y,
            text=summary,
        )
    raise ValueError(f"Unsupported semantic element type: {element_type!r}")


def _elements_from_semantic(
    element: dict[str, Any],
    *,
    fallback_y: float,
    canvas_width: float,
    font_scale: float,
) -> tuple[list[ir.Element], float]:
    element_type = _to_str(element.get("type"))
    base = _element_from_semantic(element, fallback_y=fallback_y, font_scale=font_scale)

    if not isinstance(base, (ir.Text, ir.Formula)):
        return [base], fallback_y

    if isinstance(base, ir.Text):
        raw_text = base.text
        default_font = 16.0
    else:
        raw_text = base.expr
        default_font = 18.0

    font_size = float(base.font_size if base.font_size is not None else default_font)
    semantic_role = _to_str(getattr(base, "semantic_role", "")).strip().lower()
    if element_type == "problem_text" or semantic_role == "problem_text":
        max_width = max(80.0, canvas_width * 0.95)
    else:
        max_width = max(80.0, canvas_width - float(base.x) - 16.0)
    wrapped_lines = _wrap_text_lines(raw_text, max_width=max_width, font_size=font_size)
    if len(wrapped_lines) <= 1:
        return [base], fallback_y + 36.0 if element_type in {"problem_text", "multiple_choice", "diagram_logic"} else fallback_y

    line_gap = font_size * 1.35
    line_elements: list[ir.Element] = []
    base_id = base.id or f"auto_text_{int(base.y)}"
    for idx, line in enumerate(wrapped_lines, start=1):
        line_id = f"{base_id}_ln{idx}"
        y_line = float(base.y) + (line_gap * (idx - 1))
        if isinstance(base, ir.Text):
            line_elements.append(replace(base, id=line_id, y=y_line, text=line))
        else:
            line_elements.append(replace(base, id=line_id, y=y_line, expr=line))

    next_fallback_y = fallback_y
    if element_type in {"problem_text", "multiple_choice", "diagram_logic"}:
        next_fallback_y = max(fallback_y + 36.0, float(base.y) + (line_gap * len(wrapped_lines)))
    return line_elements, next_fallback_y


def _collapse_wrapped_text_artifacts(elements: list[Any]) -> list[Any]:
    target_roles = {"problem_text", "multiple_choice", "diagram_logic"}
    buckets: dict[str, list[tuple[int, dict[str, Any]]]] = {}
    first_index_by_base: dict[str, int] = {}
    base_by_index: dict[int, str] = {}

    for idx, raw in enumerate(elements):
        if not isinstance(raw, dict):
            continue
        element_id = _to_str(raw.get("id")).strip()
        base_id = _base_id_if_wrapped(element_id)
        if not base_id:
            continue
        role = _to_str(raw.get("semantic_role")).strip().lower()
        etype = _to_str(raw.get("type")).strip().lower()
        if role not in target_roles or etype not in {"text", "formula"}:
            continue
        buckets.setdefault(base_id, []).append((idx, raw))
        if base_id not in first_index_by_base:
            first_index_by_base[base_id] = idx
        base_by_index[idx] = base_id

    if not buckets:
        return elements

    first_index_to_base = {v: k for k, v in first_index_by_base.items()}
    collapsed: list[Any] = []

    for idx, raw in enumerate(elements):
        base_id = base_by_index.get(idx)
        if base_id is not None:
            if first_index_by_base[base_id] != idx:
                continue
            parts = buckets[base_id]
            sorted_parts = sorted(parts, key=lambda item: (_to_float(item[1].get("y"), default=0.0), item[0]))
            first = dict(sorted_parts[0][1])
            chunks: list[str] = []
            for _, part in sorted_parts:
                if _to_str(part.get("type")).strip().lower() == "formula":
                    chunks.append(_to_str(part.get("expr") if part.get("expr") is not None else part.get("text")))
                else:
                    chunks.append(_to_str(part.get("text")))
            joined = " ".join(" ".join(chunks).split())
            first["id"] = base_id
            if _to_str(first.get("type")).strip().lower() == "formula":
                first["expr"] = joined
            else:
                first["text"] = joined
            role = _to_str(first.get("semantic_role")).strip().lower()
            if role == "multiple_choice":
                first["x"] = 860.0
            collapsed.append(first)
            continue

        if idx in first_index_to_base:
            # Defensive; handled above via base_by_index.
            continue
        collapsed.append(raw)

    return collapsed


def _is_geometry_problem(payload: dict[str, Any]) -> bool:
    metadata = _to_dict(payload.get("metadata"))
    domain = _to_dict(payload.get("domain"))
    problem_type = _to_str(payload.get("problem_type")).lower()
    category = _to_str(metadata.get("category")).lower()
    if "geometry" in problem_type or "geometry" in category:
        return True
    if isinstance(domain.get("logic_form"), dict):
        return True
    return False


def _extract_logic_form(domain: dict[str, Any]) -> dict[str, Any]:
    return extract_logic_form(domain)


def _has_geometry_diagram_data(domain: dict[str, Any]) -> bool:
    return has_geometry_diagram_data(domain)


def _recommended_canvas_size(
    *,
    width: float,
    height: float,
    is_geometry: bool,
    has_diagram: bool,
    point_positions: dict[str, tuple[float, float]] | None = None,
) -> tuple[int, int]:
    w = float(width)
    h = float(height)
    if has_diagram:
        # Keep geometry diagram canvas stable across repeated rebuilds.
        w = max(w, 1400.0)
        h = max(h, 900.0)
        # Clamp runaway legacy canvases using source point bbox as a stable reference.
        if point_positions and len(point_positions) >= 2:
            xs = [pt[0] for pt in point_positions.values()]
            ys = [pt[1] for pt in point_positions.values()]
            src_w = max(1.0, max(xs) - min(xs))
            src_h = max(1.0, max(ys) - min(ys))
            target_w = max(1400.0, (src_w * 3.2) + 240.0)
            target_h = max(900.0, (src_h * 3.2) + 240.0)
            if w > (target_w * 1.8):
                w = target_w
            if h > (target_h * 1.8):
                h = target_h
    elif is_geometry:
        w = max(w, 1400.0)
        h = max(h, 800.0)
    return int(round(max(1.0, w))), int(round(max(1.0, h)))


def _parse_point_positions(logic: dict[str, Any]) -> dict[str, tuple[float, float]]:
    return parse_point_positions(logic)



# geometry transform/line helpers moved to semantic_geometry.py

def build_problem_from_semantic_dict(
    semantic: dict[str, Any],
    *,
    validate_input: bool = True,
    font_scale: float = _DEFAULT_FONT_SCALE,
) -> Problem:
    payload = order_semantic(normalize_semantic(dict(semantic)))

    render = _to_dict(payload.get("render"))
    canvas = _to_dict(render.get("canvas"))
    raw_elements = render.get("elements")
    elements = raw_elements if isinstance(raw_elements, list) else []
    elements = _collapse_wrapped_text_artifacts(elements)

    incoming_types = sorted(
        {
            _to_str(el.get("type"))
            for el in elements
            if isinstance(el, dict) and _to_str(el.get("type"))
        }
    )
    unsupported = sorted(
        {
            _to_str(el.get("type"))
            for el in elements
            if isinstance(el, dict) and _to_str(el.get("type")) not in _SUPPORTED_TYPES
        }
    )
    if unsupported:
        joined = ", ".join(unsupported)
        raise ValueError(f"Unsupported semantic element type(s) for DSL build: {joined}")
    if validate_input and set(incoming_types).issubset(_CANONICAL_TYPES):
        validate_semantic_json(payload)

    domain_obj = _to_dict(payload.get("domain"))
    logic = _extract_logic_form(domain_obj)
    point_positions = _parse_point_positions(logic)
    is_geometry = _is_geometry_problem(payload)
    has_geometry_diagram = _has_geometry_diagram_data(domain_obj)
    canvas_w, canvas_h = _recommended_canvas_size(
        width=_to_float(canvas.get("width"), default=1.0),
        height=_to_float(canvas.get("height"), default=1.0),
        is_geometry=is_geometry,
        has_diagram=has_geometry_diagram,
        point_positions=point_positions,
    )

    normalized_title = _normalize_text_value(_to_str(payload.get("title"), default=""))

    problem = Problem(
        width=canvas_w,
        height=canvas_h,
        background=_to_str(canvas.get("background"), default="#F6F6F6") or "#F6F6F6",
        problem_id=_to_str(payload.get("problem_id"), default="semantic_problem"),
        problem_type=_to_str(payload.get("problem_type"), default="generic"),
        title=normalized_title or None,
    )
    problem.schema_version = _to_str(payload.get("schema_version"), default=_DEFAULT_SCHEMA_VERSION)
    problem.render_contract_version = _to_str(
        payload.get("render_contract_version"),
        default=_DEFAULT_RENDER_CONTRACT_VERSION,
    )
    problem.set_metadata(_to_dict(payload.get("metadata")))
    problem.set_domain(_to_dict(_normalize_string_tree(domain_obj)))
    answer = _to_dict(payload.get("answer"))
    problem.set_answer(
        blanks=list(answer.get("blanks", [])),
        choices=list(answer.get("choices", [])),
        answer_key=list(answer.get("answer_key", [])),
    )

    if has_geometry_diagram:
        for geom in build_geometry_reconstruction_elements(
            domain=domain_obj,
            canvas_w=float(canvas_w),
            canvas_h=float(canvas_h),
            font_scale=font_scale,
        ):
            problem.add(geom)
    elif is_geometry:
        for geom in build_geometry_template_elements(
            problem_type=_to_str(payload.get("problem_type")),
            domain=domain_obj,
            title=_to_str(payload.get("title"), default="") or None,
            canvas_w=float(canvas_w),
            canvas_h=float(canvas_h),
            font_scale=font_scale,
        ):
            problem.add(geom)

    fallback_y = 80.0
    fallback_step = 36.0
    canvas_width = float(canvas_w)
    for raw in elements:
        if not isinstance(raw, dict):
            continue
        if has_geometry_diagram and _is_geometry_render_artifact(raw):
            # Avoid compounding geometry overlays when rebuilding from prior semantic outputs.
            continue
        if has_geometry_diagram and _to_str(raw.get("type")) == "diagram_logic":
            # diagram_logic is rendered via geometry reconstruction visuals.
            continue
        generated, next_fallback_y = _elements_from_semantic(
            raw,
            fallback_y=fallback_y,
            canvas_width=canvas_width,
            font_scale=font_scale,
        )
        for item in generated:
            problem.add(item)
        if next_fallback_y == fallback_y:
            fallback_y += fallback_step
        else:
            fallback_y = next_fallback_y
    return problem


def _insert_before_svg_close(svg_text: str, snippet: str) -> str:
    idx = svg_text.rfind("</svg>")
    if idx < 0:
        return f"{svg_text}\n{snippet}\n"
    return f"{svg_text[:idx]}{snippet}\n{svg_text[idx:]}"


def _extract_answer_label(semantic: dict[str, Any]) -> str:
    answer = semantic.get("answer")
    if not isinstance(answer, dict):
        return ""
    answer_key = answer.get("answer_key")
    if not isinstance(answer_key, list) or not answer_key:
        return ""
    labels: list[str] = []
    for item in answer_key:
        if not isinstance(item, dict):
            continue
        if "label" in item and "value" in item:
            labels.append(f"{item['label']} ({item['value']})")
            continue
        if "value" in item:
            labels.append(str(item["value"]))
            continue
    if not labels:
        return ""
    return ", ".join(labels)


def make_answer_svg(problem_svg: str, semantic: dict[str, Any], *, font_size: int = 52) -> str:
    label = _extract_answer_label(semantic)
    if not label:
        return problem_svg
    viewbox_match = re.search(r'viewBox="([^"]+)"', problem_svg)
    x = "96%"
    y = "96%"
    if viewbox_match:
        parts = viewbox_match.group(1).strip().split()
        if len(parts) == 4:
            try:
                width = float(parts[2])
                height = float(parts[3])
                x = f"{max(0.0, width - 24.0):.3f}".rstrip("0").rstrip(".")
                y = f"{max(0.0, height - 24.0):.3f}".rstrip("0").rstrip(".")
            except ValueError:
                pass
    snippet = (
        "\n  <!-- Auto-generated answer label -->\n"
        f'  <text id="answer_overlay_label" x="{x}" y="{y}" text-anchor="end" dominant-baseline="middle" '
        f'fill="#D32222" font-family="Malgun Gothic" font-size="{font_size}px" font-weight="700">'
        f"정답: {escape(label)}</text>\n"
    )
    return _insert_before_svg_close(problem_svg, snippet)


def _scaffold_text(*, semantic_relative_path: str, problem_id: str) -> str:
    raise RuntimeError("_scaffold_text requires semantic payload; use _render_build_scaffold_text.")


def _py_literal(value: Any) -> str:
    return pprint.pformat(value, width=100, sort_dicts=False, compact=False)


def _repr_text(value: Any) -> str:
    return json.dumps(_to_str(value), ensure_ascii=False)


def _repr_value(value: Any) -> str:
    if isinstance(value, bool):
        return "True" if value else "False"
    if value is None:
        return "None"
    if isinstance(value, str):
        return _repr_text(value)
    if isinstance(value, (int, float)):
        return repr(value)
    return _py_literal(value)


def _append_optional(lines: list[str], key: str, value: Any, *, indent: str = "            ") -> None:
    if value is None:
        return
    if isinstance(value, str) and value == "":
        return
    lines.append(f"{indent}{key}={_repr_value(value)},")


def _scaled_font_size(raw: Any, *, default: float, scale: float) -> int:
    size = _to_float(raw, default=default)
    scaled = max(1.0, size * scale)
    return int(round(scaled))


def _char_advance(ch: str, *, font_size: float) -> float:
    if ch == " ":
        return font_size * 0.33
    if ord(ch) > 127:
        return font_size * 0.95
    return font_size * 0.56


def _wrap_text_lines(text: str, *, max_width: float, font_size: float) -> list[str]:
    source = text.strip()
    if not source:
        return [""]
    if max_width <= 0:
        return [source]

    lines: list[str] = []
    current = ""
    current_w = 0.0
    words = source.split(" ")

    for word in words:
        token = word if not current else f" {word}"
        token_w = sum(_char_advance(ch, font_size=font_size) for ch in token)
        if current and (current_w + token_w) > max_width:
            lines.append(current)
            current = word
            current_w = sum(_char_advance(ch, font_size=font_size) for ch in word)
        else:
            current += token
            current_w += token_w

    if current:
        lines.append(current)

    # Fallback: break very long single-token lines.
    wrapped: list[str] = []
    for line in lines:
        line_w = sum(_char_advance(ch, font_size=font_size) for ch in line)
        if line_w <= max_width:
            wrapped.append(line)
            continue
        part = ""
        part_w = 0.0
        for ch in line:
            ch_w = _char_advance(ch, font_size=font_size)
            if part and (part_w + ch_w) > max_width:
                wrapped.append(part)
                part = ch
                part_w = ch_w
            else:
                part += ch
                part_w += ch_w
        if part:
            wrapped.append(part)
    return wrapped or [source]


def _append_text_like_lines(
    *,
    lines: list[str],
    ctor: str,
    element_id: str,
    x: float,
    y: float,
    content_key: str,
    content: str,
    font_size: int,
    canvas_width: float,
    common_attrs: list[str],
    disable_wrap: bool = False,
    max_width_override: float | None = None,
) -> None:
    if disable_wrap:
        wrapped = [content.strip() or ""]
    else:
        if max_width_override is not None:
            max_width = max(80.0, float(max_width_override))
        else:
            max_width = max(80.0, canvas_width - float(x) - 16.0)
        wrapped = _wrap_text_lines(content, max_width=max_width, font_size=float(font_size))
    line_gap = float(font_size) * 1.35
    for i, part in enumerate(wrapped):
        line_id = element_id if len(wrapped) == 1 else f"{element_id}_ln{i+1}"
        y_line = float(y) + (line_gap * i)
        lines.extend(
            [
                "    p.add(",
                f"        {ctor}(",
                f"            id={_repr_text(line_id)},",
                f"            x={_repr_value(x)},",
                f"            y={_repr_value(y_line)},",
                f"            {content_key}={_repr_text(part)},",
                f"            font_size={font_size},",
            ]
        )
        lines.extend(common_attrs)
        lines.extend(["        )", "    )"])


def _render_canonical_element_lines(
    element: dict[str, Any],
    idx: int,
    *,
    canvas_width: float,
    font_scale: float,
) -> list[str]:
    etype = _to_str(element.get("type"))
    element_id = _to_str(element.get("id"), default=f"el_{idx}")
    common_geom: list[str] = []
    _append_optional(common_geom, "semantic_role", element.get("semantic_role"))
    _append_optional(common_geom, "stroke", element.get("stroke"))
    _append_optional(common_geom, "stroke_width", element.get("stroke_width"))
    _append_optional(common_geom, "fill", element.get("fill"))
    metadata = element.get("metadata")
    if isinstance(metadata, dict) and metadata:
        _append_optional(common_geom, "metadata", metadata)

    common_text: list[str] = []
    _append_optional(common_text, "semantic_role", element.get("semantic_role"))
    _append_optional(common_text, "fill", element.get("fill"))
    _append_optional(common_text, "font_family", element.get("font_family"))
    _append_optional(common_text, "anchor", element.get("anchor"))
    if isinstance(metadata, dict) and metadata:
        _append_optional(common_text, "metadata", metadata)

    lines: list[str] = []
    if etype == "rect":
        lines.extend(
            [
                "    p.add(",
                "        Rect(",
                f"            id={_repr_text(element_id)},",
                f"            x={_repr_value(element.get('x', 0))},",
                f"            y={_repr_value(element.get('y', 0))},",
                f"            width={_repr_value(element.get('width', 0))},",
                f"            height={_repr_value(element.get('height', 0))},",
            ]
        )
        _append_optional(lines, "rx", element.get("rx"))
        _append_optional(lines, "ry", element.get("ry"))
        lines.extend(common_geom)
        lines.extend(["        )", "    )"])
        return lines
    if etype == "circle":
        lines.extend(
            [
                "    p.add(",
                "        Circle(",
                f"            id={_repr_text(element_id)},",
                f"            cx={_repr_value(element.get('x', 0))},",
                f"            cy={_repr_value(element.get('y', 0))},",
                f"            r={_repr_value(element.get('r', 0))},",
            ]
        )
        lines.extend(common_geom)
        lines.extend(["        )", "    )"])
        return lines
    if etype == "line":
        lines.extend(
            [
                "    p.add(",
                "        Line(",
                f"            id={_repr_text(element_id)},",
                f"            x1={_repr_value(element.get('x1', 0))},",
                f"            y1={_repr_value(element.get('y1', 0))},",
                f"            x2={_repr_value(element.get('x2', 0))},",
                f"            y2={_repr_value(element.get('y2', 0))},",
            ]
        )
        lines.extend(common_geom)
        lines.extend(["        )", "    )"])
        return lines
    if etype == "polygon":
        lines.extend(
            [
                "    p.add(",
                "        Polygon(",
                f"            id={_repr_text(element_id)},",
                f"            points={_py_literal(element.get('points', []))},",
            ]
        )
        lines.extend(common_geom)
        lines.extend(["        )", "    )"])
        return lines
    if etype == "text":
        font_size = _scaled_font_size(element.get("font_size"), default=16, scale=font_scale)
        semantic_role = _to_str(element.get("semantic_role")).strip().lower()
        if semantic_role == "problem_text":
            x_value = 40.0
        elif semantic_role == "multiple_choice":
            x_value = 860.0
        else:
            x_value = _to_float(element.get("x"), default=0.0)
        y_default = 80.0 if semantic_role in {"problem_text", "multiple_choice", "diagram_logic"} else 0.0
        y_value = _to_float(element.get("y"), default=y_default)
        if semantic_role == "multiple_choice":
            y_value = max(320.0, y_value)
        _append_text_like_lines(
            lines=lines,
            ctor="Text",
            element_id=element_id,
            x=x_value,
            y=y_value,
            content_key="text",
            content=_to_str(element.get("text")),
            font_size=font_size,
            canvas_width=canvas_width,
            common_attrs=common_text,
            max_width_override=(canvas_width * 0.95) if semantic_role == "problem_text" else None,
        )
        return lines
    if etype == "formula":
        font_size = _scaled_font_size(element.get("font_size"), default=18, scale=font_scale)
        expr = element.get("expr")
        if expr is None:
            expr = element.get("text")
        _append_text_like_lines(
            lines=lines,
            ctor="Formula",
            element_id=element_id,
            x=_to_float(element.get("x"), default=0.0),
            y=_to_float(element.get("y"), default=0.0),
            content_key="expr",
            content=_to_str(expr),
            font_size=font_size,
            canvas_width=canvas_width,
            common_attrs=common_text,
        )
        return lines
    return []


def _render_custom_element_lines(
    element: dict[str, Any],
    idx: int,
    *,
    canvas_width: float,
    font_scale: float,
    is_geometry3k: bool,
) -> list[str]:
    etype = _to_str(element.get("type"))
    element_id = _to_str(element.get("id"), default=f"el_{idx}")

    if etype == "problem_text":
        text = _to_str(element.get("text"))
        lines = ["    # original type: problem_text"]
        _append_text_like_lines(
            lines=lines,
            ctor="Text",
            element_id=element_id,
            x=40.0,
            y=80.0 + (idx * 36.0),
            content_key="text",
            content=text,
            font_size=_scaled_font_size(element.get("font_size"), default=16, scale=font_scale),
            canvas_width=canvas_width,
            common_attrs=["            semantic_role=\"problem_text\","],
            max_width_override=canvas_width * 0.95,
        )
        return lines
    if etype == "multiple_choice":
        raw_choices = element.get("choices")
        choices: list[str] = []
        if isinstance(raw_choices, list):
            for i, choice in enumerate(raw_choices, start=1):
                choices.append(f"no.{i} {_to_str(choice)}")
        rendered = " / ".join(choices) if choices else "choices"
        lines = ["    # original type: multiple_choice"]
        _append_text_like_lines(
            lines=lines,
            ctor="Text",
            element_id=element_id,
            x=860.0,
            y=max(320.0, 80.0 + (idx * 36.0)),
            content_key="text",
            content=rendered,
            font_size=_scaled_font_size(element.get("font_size"), default=16, scale=font_scale),
            canvas_width=canvas_width,
            common_attrs=["            semantic_role=\"multiple_choice\","],
        )
        return lines
    if etype == "diagram_logic":
        if is_geometry3k:
            return [
                "    # original type: diagram_logic",
                "    # geometry3k reconstruction block below consumes logic constraints.",
            ]
        raw_logic = element.get("diagram_logic_form")
        short_lines: list[str] = []
        if isinstance(raw_logic, list):
            for item in raw_logic[:3]:
                short_lines.append(_to_str(item))
        summary = " | ".join(short_lines) if short_lines else "diagram_logic"
        lines = ["    # original type: diagram_logic"]
        _append_text_like_lines(
            lines=lines,
            ctor="Text",
            element_id=element_id,
            x=40.0,
            y=80.0 + (idx * 36.0),
            content_key="text",
            content=summary,
            font_size=_scaled_font_size(element.get("font_size"), default=14, scale=font_scale),
            canvas_width=canvas_width,
            common_attrs=[
                "            semantic_role=\"diagram_logic\",",
                "            metadata={\"source_type\": \"diagram_logic\"},",
            ],
        )
        return lines
    return []



# geometry reconstruction/template helpers moved to semantic_geometry.py

def _render_geometry3k_reconstruction_lines(
    *,
    domain: dict[str, Any],
    font_scale: float,
) -> list[str]:
    logic = _to_dict(domain.get("logic_form"))
    point_positions_raw = logic.get("point_positions")
    if not isinstance(point_positions_raw, dict):
        return []

    point_positions: dict[str, tuple[float, float]] = {}
    for name, value in point_positions_raw.items():
        if not isinstance(value, (list, tuple)) or len(value) != 2:
            continue
        point_positions[_to_str(name)] = (_to_float(value[0]), _to_float(value[1]))
    if not point_positions:
        return []

    diagram_logic_raw = logic.get("diagram_logic_form")
    diagram_logic = diagram_logic_raw if isinstance(diagram_logic_raw, list) else []
    point_on_line_constraints = parse_point_on_line_constraints(diagram_logic)
    point_positions = apply_point_on_line_constraints(point_positions, point_on_line_constraints)
    line_instances = parse_line_instances(logic)
    point_positions = auto_snap_points_to_segments(point_positions, line_instances)
    length_constraints = parse_length_constraints(diagram_logic)
    equal_constraints = parse_equal_segment_constraints(diagram_logic)
    circle_constraints = parse_circle_constraints(logic, diagram_logic)
    angle_constraints = parse_angle_constraints(diagram_logic)
    perp_constraints = parse_perpendicular_constraints(diagram_logic)
    parallel_constraints = parse_parallel_constraints(diagram_logic)

    label_font = _scaled_font_size(12, default=12, scale=font_scale)
    lines: list[str] = []
    lines.append("    # geometry3k template: diagram reconstruction")
    merged_edges = simplify_collinear_edges(mapped_points=point_positions, edges=line_instances)
    for idx, (start_pt, end_pt) in enumerate(merged_edges, start=1):
        ax, ay = start_pt
        bx, by = end_pt
        lines.extend(
            [
                "    p.add(",
                "        Line(",
                f"            id={_repr_text(f'geom_line_{idx}')},",
                f"            x1={_repr_value(ax)},",
                f"            y1={_repr_value(ay)},",
                f"            x2={_repr_value(bx)},",
                f"            y2={_repr_value(by)},",
                "            stroke=\"#8A8A8A\",",
                "            stroke_width=2.0,",
                "            semantic_role=\"geometry_edge\",",
                "        )",
                "    )",
            ]
        )

    circle_elements = build_circle_elements(
        source_points=point_positions,
        mapped_points=point_positions,
        circle_constraints=circle_constraints,
        default_radius=36.0,
    )
    for el in circle_elements:
        if not isinstance(el, ir.Circle):
            continue
        lines.extend(
            [
                "    p.add(",
                "        Circle(",
                f"            id={_repr_text(el.id)},",
                f"            cx={_repr_value(el.x)},",
                f"            cy={_repr_value(el.y)},",
                f"            r={_repr_value(el.r)},",
                f"            fill={_repr_text(el.fill or 'none')},",
                f"            stroke={_repr_text(el.stroke or '#2563EB')},",
                f"            stroke_width={_repr_value(el.stroke_width or 2.0)},",
                "            semantic_role=\"geometry_circle\",",
                "        )",
                "    )",
            ]
        )

    for name, (px, py) in point_positions.items():
        lines.extend(
            [
                "    p.add(",
                "        Circle(",
                f"            id={_repr_text(f'geom_point_{name}')},",
                f"            cx={_repr_value(px)},",
                f"            cy={_repr_value(py)},",
                "            r=3.2,",
                "            fill=\"#111111\",",
                "            stroke=\"#111111\",",
                "            stroke_width=1.0,",
                "            semantic_role=\"geometry_point\",",
                "        )",
                "    )",
                "    p.add(",
                "        Text(",
                f"            id={_repr_text(f'geom_label_{name}')},",
                f"            x={_repr_value(px + 5.0)},",
                f"            y={_repr_value(py - 5.0)},",
                f"            text={_repr_text(name)},",
                f"            font_size={label_font},",
                "            fill=\"#111111\",",
                "            semantic_role=\"geometry_point_label\",",
                "        )",
                "    )",
            ]
        )
    for a, b, value in length_constraints:
        if a not in point_positions or b not in point_positions:
            continue
        ax, ay = point_positions[a]
        bx, by = point_positions[b]
        mx = (ax + bx) / 2.0
        my = (ay + by) / 2.0
        lines.extend(
            [
                "    p.add(",
                "        Text(",
                f"            id={_repr_text(f'geom_len_{a}{b}')},",
                f"            x={_repr_value(mx + 4.0)},",
                f"            y={_repr_value(my - 4.0)},",
                f"            text={_repr_text(value)},",
                f"            font_size={label_font},",
                "            fill=\"#2E2E2E\",",
                "            semantic_role=\"geometry_length_label\",",
                "        )",
                "    )",
            ]
        )

    perp_elements = build_perpendicular_marker_elements(mapped_points=point_positions, constraints=perp_constraints)
    parallel_elements = build_parallel_marker_elements(mapped_points=point_positions, constraints=parallel_constraints)
    dim_elements = build_length_dimension_elements(mapped_points=point_positions, constraints=length_constraints)
    equal_tick_elements = build_equal_length_tick_elements(mapped_points=point_positions, constraints=equal_constraints)
    angle_elements = build_angle_marker_elements(
        mapped_points=point_positions,
        constraints=angle_constraints,
        font_size=label_font,
    )
    for el in [*perp_elements, *parallel_elements, *dim_elements, *equal_tick_elements, *angle_elements]:
        if isinstance(el, ir.Line):
            lines.extend(
                [
                    "    p.add(",
                    "        Line(",
                    f"            id={_repr_text(el.id)},",
                    f"            x1={_repr_value(el.x1)},",
                    f"            y1={_repr_value(el.y1)},",
                    f"            x2={_repr_value(el.x2)},",
                    f"            y2={_repr_value(el.y2)},",
                    f"            stroke={_repr_text(el.stroke or '#111111')},",
                    f"            stroke_width={_repr_value(el.stroke_width or 2.0)},",
                    f"            semantic_role={_repr_text(el.semantic_role or 'geometry_marker')},",
                    "        )",
                    "    )",
                ]
            )
        elif isinstance(el, ir.Text):
            lines.extend(
                [
                    "    p.add(",
                    "        Text(",
                    f"            id={_repr_text(el.id)},",
                    f"            x={_repr_value(el.x)},",
                    f"            y={_repr_value(el.y)},",
                    f"            text={_repr_text(el.text)},",
                    f"            font_size={_repr_value(el.font_size or label_font)},",
                    f"            fill={_repr_text(el.fill or '#111111')},",
                    f"            semantic_role={_repr_text(el.semantic_role or 'geometry_label')},",
                    "        )",
                    "    )",
                ]
            )
    return lines


def _render_build_scaffold_text(
    *,
    semantic_relative_path: str,
    semantic_payload: dict[str, Any],
) -> str:
    normalized = order_semantic(normalize_semantic(dict(semantic_payload)))
    render = _to_dict(normalized.get("render"))
    canvas = _to_dict(render.get("canvas"))
    elements_raw = render.get("elements")
    elements = elements_raw if isinstance(elements_raw, list) else []
    elements = _collapse_wrapped_text_artifacts(elements)

    imports = {"Problem"}
    semantic_path_norm = semantic_relative_path.replace("\\", "/")
    is_geometry3k = "/geometry3k/" in f"/{semantic_path_norm}"
    font_scale = 1.0
    for element in elements:
        if not isinstance(element, dict):
            continue
        etype = _to_str(element.get("type"))
        if etype == "rect":
            imports.add("Rect")
        elif etype == "circle":
            imports.add("Circle")
        elif etype == "line":
            imports.add("Line")
        elif etype == "polygon":
            imports.add("Polygon")
        elif etype in {"text", "problem_text", "multiple_choice", "diagram_logic"}:
            imports.add("Text")
        elif etype == "formula":
            imports.add("Formula")
        else:
            imports.add("Text")
    if is_geometry3k:
        imports.update({"Line", "Circle", "Text"})

    import_list = ", ".join(sorted(imports))
    problem_id = _to_str(normalized.get("problem_id"), default="semantic_problem")
    problem_type = _to_str(normalized.get("problem_type"), default="generic")
    title = normalized.get("title")
    metadata = _to_dict(normalized.get("metadata"))
    domain = _to_dict(normalized.get("domain"))
    answer = _to_dict(normalized.get("answer"))

    lines: list[str] = []
    lines.append("from __future__ import annotations")
    lines.append("")
    lines.append("from pathlib import Path")
    lines.append("")
    lines.append(f"from modu_semantic import {import_list}")
    lines.append("")
    lines.append(f"# source semantic: {semantic_relative_path}")
    lines.append("")
    lines.append(f"PROBLEM_ID = {_repr_text(problem_id)}")
    lines.append(f"PROBLEM_TYPE = {_repr_text(problem_type)}")
    if title is not None:
        lines.append(f"TITLE_TEXT = {_repr_text(title)}")
    lines.append(f"CANVAS_W = {_repr_value(canvas.get('width', 1200))}")
    lines.append(f"CANVAS_H = {_repr_value(canvas.get('height', 600))}")
    lines.append(f"CANVAS_BG = {_repr_text(canvas.get('background', '#F6F6F6'))}")
    lines.append(f"FONT_SCALE = {_repr_value(font_scale)}")
    lines.append("")
    lines.append("")
    lines.append("def build() -> Problem:")
    lines.append(
        "    p = Problem("
        "width=int(CANVAS_W), "
        "height=int(CANVAS_H), "
        "background=CANVAS_BG, "
        "problem_id=PROBLEM_ID, "
        "problem_type=PROBLEM_TYPE"
        ")"
    )
    if title is not None:
        lines.append("    p.title = TITLE_TEXT")
    lines.append(f"    p.set_metadata({_py_literal(metadata)})")
    lines.append(f"    p.set_domain({_py_literal(domain)})")
    lines.append(
        "    p.set_answer("
        f"blanks={_py_literal(list(answer.get('blanks', [])))}"
        ", "
        f"choices={_py_literal(list(answer.get('choices', [])))}"
        ", "
        f"answer_key={_py_literal(list(answer.get('answer_key', [])))}"
        ")"
    )
    lines.append("")
    lines.append("    # elements")
    for idx, element in enumerate(elements):
        if not isinstance(element, dict):
            continue
        if is_geometry3k and _is_geometry_render_artifact(element):
            # geometry3k scaffold emits a dedicated reconstruction block below.
            continue
        etype = _to_str(element.get("type"))
        block = []
        if etype in _CANONICAL_TYPES:
            block = _render_canonical_element_lines(
                element,
                idx,
                canvas_width=float(_to_float(canvas.get("width"), default=1200.0)),
                font_scale=font_scale,
            )
        elif etype in _SUPPORTED_TYPES:
            block = _render_custom_element_lines(
                element,
                idx,
                canvas_width=float(_to_float(canvas.get("width"), default=1200.0)),
                font_scale=font_scale,
                is_geometry3k=is_geometry3k,
            )
        else:
            block = [
                f"    # unsupported source element type skipped: {etype}",
            ]
        lines.extend(block)
        lines.append("")

    if is_geometry3k:
        geo_block = _render_geometry3k_reconstruction_lines(domain=domain, font_scale=font_scale)
        if geo_block:
            lines.extend(geo_block)
            lines.append("")

    lines.append("    return p")
    lines.append("")
    lines.append("")
    lines.append("CURRENT_DIR = Path(__file__).resolve().parent")
    lines.append("")
    lines.append('if __name__ == "__main__":')
    lines.append("    out_prefix = CURRENT_DIR / PROBLEM_ID")
    lines.append("    build().save(out_prefix)")
    lines.append("")
    return "\n".join(lines)


def write_semantic_build_scaffold(
    *,
    target_py_path: str | Path,
    input_semantic_path: str | Path,
    semantic_payload: dict[str, Any],
    problem_id: str,
) -> Path:
    py_path = Path(target_py_path)
    py_path.parent.mkdir(parents=True, exist_ok=True)

    semantic_path = Path(input_semantic_path)
    try:
        rel = semantic_path.relative_to(py_path.parent)
        rel_text = rel.as_posix()
    except ValueError:
        rel_text = semantic_path.as_posix()

    py_path.write_text(
        _render_build_scaffold_text(
            semantic_relative_path=rel_text,
            semantic_payload=semantic_payload,
        ),
        encoding="utf-8",
    )
    return py_path


def build_from_semantic_file(
    *,
    input_semantic_path: str | Path,
    out_prefix: str | Path,
    emit_py_path: str | Path | None = None,
    validate_input: bool = True,
    validate_output: bool = True,
) -> dict[str, Path]:
    semantic_path = Path(input_semantic_path)
    semantic = json.loads(semantic_path.read_text(encoding="utf-8"))
    sidecar_logic_path = semantic_path.parent / "logic_form.json"
    if sidecar_logic_path.exists():
        try:
            raw_logic = json.loads(sidecar_logic_path.read_text(encoding="utf-8"))
            if isinstance(raw_logic, dict):
                domain = semantic.get("domain")
                if not isinstance(domain, dict):
                    domain = {}
                    semantic["domain"] = domain
                domain["logic_form"] = raw_logic
        except Exception:
            pass
    problem = build_problem_from_semantic_dict(
        semantic,
        validate_input=validate_input,
        font_scale=_DEFAULT_FONT_SCALE,
    )

    prefix = Path(out_prefix)
    prefix.parent.mkdir(parents=True, exist_ok=True)
    problem.save(prefix, validate=validate_output)

    outputs = {
        "semantic": prefix.with_suffix(".semantic.json"),
        "layout": prefix.with_suffix(".layout.json"),
        "svg": prefix.with_suffix(".svg"),
    }
    problem_svg = outputs["svg"].read_text(encoding="utf-8")
    answer_svg = make_answer_svg(problem_svg, semantic, font_size=56)
    answer_svg_path = prefix.with_suffix(".answer.svg")
    answer_svg_path.write_text(answer_svg, encoding="utf-8")
    outputs["answer_svg"] = answer_svg_path

    if emit_py_path is not None:
        generated_semantic = json.loads(outputs["semantic"].read_text(encoding="utf-8"))
        py_path = write_semantic_build_scaffold(
            target_py_path=emit_py_path,
            input_semantic_path=semantic_path,
            semantic_payload=generated_semantic,
            problem_id=problem.problem_id or prefix.stem,
        )
        outputs["py"] = py_path

    return outputs
