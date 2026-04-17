from __future__ import annotations

from dataclasses import replace
from typing import Any, Iterable

from ..groups import Group
from ..primitives import Circle, Formula, Line, Polygon, Rect, Text
from ..regions import Region


def _offset_element(element: object, dx: float, dy: float) -> object:
    if isinstance(element, Rect):
        return replace(element, x=element.x + dx, y=element.y + dy)
    if isinstance(element, Circle):
        return replace(element, cx=element.cx + dx, cy=element.cy + dy)
    if isinstance(element, Line):
        return replace(element, x1=element.x1 + dx, y1=element.y1 + dy, x2=element.x2 + dx, y2=element.y2 + dy)
    if isinstance(element, Polygon):
        return replace(element, points=[(x + dx, y + dy) for x, y in element.points])
    if isinstance(element, (Text, Formula)):
        return replace(element, x=element.x + dx, y=element.y + dy)
    return element


def _merge_metadata(base: dict[str, Any], extra: dict[str, Any]) -> dict[str, Any]:
    merged = dict(base)
    for key, value in extra.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = _merge_metadata(merged[key], value)
        else:
            merged[key] = value
    return merged


def _apply_group_context(
    element: object,
    *,
    group_id: str | None,
    group_semantic_role: str | None,
    group_metadata: dict[str, Any] | None,
) -> object:
    if group_id is None and group_semantic_role is None and not group_metadata:
        return element
    if not hasattr(element, "__dataclass_fields__"):
        return element

    changes: dict[str, Any] = {}
    if group_semantic_role is not None and getattr(element, "semantic_role", None) is None:
        changes["semantic_role"] = group_semantic_role

    element_metadata_raw = getattr(element, "metadata", None)
    element_metadata = element_metadata_raw if isinstance(element_metadata_raw, dict) else {}
    merged = dict(element_metadata)
    if group_id is not None:
        merged.setdefault("group_id", group_id)
    if group_semantic_role is not None:
        merged.setdefault("group_semantic_role", group_semantic_role)
    if isinstance(group_metadata, dict) and group_metadata:
        existing_group_metadata = merged.get("group_metadata")
        if isinstance(existing_group_metadata, dict):
            merged["group_metadata"] = _merge_metadata(existing_group_metadata, group_metadata)
        else:
            merged["group_metadata"] = dict(group_metadata)
    if merged != element_metadata:
        changes["metadata"] = merged

    if not changes:
        return element
    return replace(element, **changes)


def _iter_leaf_elements(
    elements: Iterable[object],
    dx: float = 0.0,
    dy: float = 0.0,
    *,
    group_id: str | None = None,
    group_semantic_role: str | None = None,
    group_metadata: dict[str, Any] | None = None,
) -> Iterable[object]:
    for element in elements:
        if isinstance(element, Region):
            yield from _iter_leaf_elements(
                element.children,
                element.x,
                element.y,
                group_id=group_id,
                group_semantic_role=group_semantic_role,
                group_metadata=group_metadata,
            )
        elif isinstance(element, Group):
            current_group_id = element.id or group_id
            current_group_role = element.semantic_role or group_semantic_role
            current_group_metadata = _merge_metadata(group_metadata or {}, element.metadata or {})
            yield from _iter_leaf_elements(
                element.children,
                dx,
                dy,
                group_id=current_group_id,
                group_semantic_role=current_group_role,
                group_metadata=current_group_metadata,
            )
        else:
            offset_element = _offset_element(element, dx, dy)
            yield _apply_group_context(
                offset_element,
                group_id=group_id,
                group_semantic_role=group_semantic_role,
                group_metadata=group_metadata,
            )


def problem_to_ir(problem: object):
    """Adapter layer: public Problem model -> canonical ProblemIR."""
    from .. import ir as legacy_ir

    width = float(getattr(problem, "width"))
    height = float(getattr(problem, "height"))
    problem_id = getattr(problem, "problem_id") or "custom_problem"
    problem_type = getattr(problem, "problem_type")
    elements = getattr(problem, "elements")

    legacy_problem = legacy_ir.ProblemIR(
        width=width,
        height=height,
        problem_id=problem_id,
        problem_type=problem_type,
    )

    for element in _iter_leaf_elements(elements):
        if isinstance(
            element,
            legacy_ir.Rect | legacy_ir.Circle | legacy_ir.Line | legacy_ir.Polygon | legacy_ir.Text | legacy_ir.Formula,
        ):
            legacy_problem.elements.append(element)
            continue

        name = type(element).__name__
        if name == "Rect":
            legacy_problem.elements.append(
                legacy_ir.Rect(
                    id=element.id,
                    x=element.x,
                    y=element.y,
                    width=element.width,
                    height=element.height,
                    fill=element.fill,
                    stroke=element.stroke,
                    stroke_width=element.stroke_width,
                    rx=element.rx,
                    ry=element.ry,
                    semantic_role=element.semantic_role,
                    metadata=element.metadata,
                )
            )
        elif name == "Circle":
            legacy_problem.elements.append(
                legacy_ir.Circle(
                    id=element.id,
                    x=element.cx,
                    y=element.cy,
                    r=element.r,
                    fill=element.fill,
                    stroke=element.stroke,
                    stroke_width=element.stroke_width,
                    semantic_role=element.semantic_role,
                    metadata=element.metadata,
                )
            )
        elif name == "Line":
            legacy_problem.elements.append(
                legacy_ir.Line(
                    id=element.id,
                    x1=element.x1,
                    y1=element.y1,
                    x2=element.x2,
                    y2=element.y2,
                    stroke=element.stroke,
                    stroke_width=element.stroke_width,
                    semantic_role=element.semantic_role,
                    metadata=element.metadata,
                )
            )
        elif name == "Polygon":
            legacy_problem.elements.append(
                legacy_ir.Polygon(
                    id=element.id,
                    points=element.points,
                    fill=element.fill,
                    stroke=element.stroke,
                    stroke_width=element.stroke_width,
                    semantic_role=element.semantic_role,
                    metadata=element.metadata,
                )
            )
        elif name == "Text":
            legacy_problem.elements.append(
                legacy_ir.Text(
                    id=element.id,
                    x=element.x,
                    y=element.y,
                    text=element.text,
                    font_size=element.font_size,
                    font_family=element.font_family,
                    fill=element.fill,
                    anchor=element.anchor,
                    semantic_role=element.semantic_role,
                    metadata=element.metadata,
                )
            )
        elif name == "Formula":
            formula_expr = getattr(element, "expr", None)
            if formula_expr is None:
                formula_expr = getattr(element, "text", "")
            legacy_problem.elements.append(
                legacy_ir.Formula(
                    id=element.id,
                    x=element.x,
                    y=element.y,
                    expr=str(formula_expr),
                    font_size=element.font_size,
                    font_family=element.font_family,
                    fill=element.fill,
                    anchor=element.anchor,
                    semantic_role=element.semantic_role,
                    metadata=element.metadata,
                )
            )
        else:
            raise TypeError(f"Unsupported element type for legacy export: {type(element)!r}")

    return legacy_problem


def problem_to_legacy_ir(problem: object):
    """Backward-compatible alias for legacy call sites."""
    return problem_to_ir(problem)
