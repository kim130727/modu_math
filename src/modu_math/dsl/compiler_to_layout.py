from __future__ import annotations

from dataclasses import asdict
from typing import Any

from .models.base import BlankSlot, ChoiceSlot, CircleSlot, Constraint, Group, LabelSlot, LineSlot, PathSlot, PolygonSlot, RectSlot, Region, TextSlot
from .models.objects import ShapeObject
from .models.templates import AuthoringSlot, DiagramTemplate, ProblemTemplate


def compile_problem_template_to_layout(problem: ProblemTemplate) -> dict[str, Any]:
    """Compile declarative DSL template objects into a normalized layout contract."""
    _assert_unique_ids(problem)

    slots = [_normalize_slot(slot) for slot in problem.slots]
    normalized_regions = _normalize_regions(problem.regions, slots)
    diagrams = [_normalize_diagram(diagram) for diagram in problem.diagrams]
    groups = [_normalize_group(group) for group in problem.groups]
    constraints = [_normalize_constraint(constraint) for constraint in problem.constraints]

    layout: dict[str, Any] = {
        "schema": "modu.layout.v1",
        "problem_id": problem.id,
        "title": problem.title,
        "canvas": {
            "width": problem.canvas.width,
            "height": problem.canvas.height,
            "coordinate_mode": problem.canvas.coordinate_mode,
            "background": "#FFFFFF",
        },
        "regions": normalized_regions,
        "slots": slots,
        "groups": groups,
        "constraints": constraints,
        "diagrams": diagrams,
        "reading_order": _build_reading_order(normalized_regions, diagrams),
    }
    return layout


def _assert_unique_ids(problem: ProblemTemplate) -> None:
    seen_ids: set[str] = set()

    def consume(node_id: str, scope: str) -> None:
        if node_id in seen_ids:
            raise ValueError(f"Duplicate id '{node_id}' in {scope}")
        seen_ids.add(node_id)

    consume(problem.id, "problem")
    for region in problem.regions:
        consume(region.id, "regions")
    for slot in problem.slots:
        consume(slot.id, "slots")
    for group in problem.groups:
        consume(group.id, "groups")
    for constraint in problem.constraints:
        consume(constraint.id, "constraints")
    for diagram in problem.diagrams:
        consume(diagram.id, "diagrams")
        for obj in diagram.objects:
            consume(obj.id, f"diagram '{diagram.id}' objects")
        for label_slot in diagram.label_slots:
            consume(label_slot.id, f"diagram '{diagram.id}' label_slots")
        for constraint in diagram.constraints:
            consume(constraint.id, f"diagram '{diagram.id}' constraints")


def _normalize_regions(regions: tuple[Region, ...], slots: list[dict[str, Any]]) -> list[dict[str, Any]]:
    slot_ids = [slot["id"] for slot in slots]
    known_slots = set(slot_ids)
    assigned: set[str] = set()
    normalized: list[dict[str, Any]] = []

    for region in regions:
        safe_slot_ids: list[str] = []
        for slot_id in region.slot_ids:
            if slot_id in known_slots and slot_id not in assigned:
                safe_slot_ids.append(slot_id)
                assigned.add(slot_id)
        normalized.append(
            {
                "id": region.id,
                "role": region.role,
                "flow": region.flow,
                "slot_ids": safe_slot_ids,
            }
        )

    unassigned = [slot_id for slot_id in slot_ids if slot_id not in assigned]
    if not normalized:
        normalized.append(
            {
                "id": "region.stem",
                "role": "stem",
                "flow": "vertical",
                "slot_ids": unassigned,
            }
        )
        return normalized

    if unassigned:
        target_region = next((region for region in normalized if region["role"] == "stem"), normalized[0])
        target_region["slot_ids"] = [*target_region["slot_ids"], *unassigned]
    return normalized


def _normalize_slot(slot: AuthoringSlot) -> dict[str, Any]:
    if isinstance(slot, TextSlot):
        content: dict[str, Any] = {
            "text": slot.text,
            "style_role": slot.style_role,
        }
        if slot.x is not None:
            content["x"] = float(slot.x)
        if slot.y is not None:
            content["y"] = float(slot.y)
        if slot.font_size is not None:
            content["font_size"] = int(slot.font_size)
        if isinstance(slot.font_family, str) and slot.font_family:
            content["font_family"] = slot.font_family
        if isinstance(slot.anchor, str) and slot.anchor:
            content["anchor"] = slot.anchor
        if isinstance(slot.fill, str) and slot.fill:
            content["fill"] = slot.fill
        if isinstance(slot.semantic_role, str) and slot.semantic_role:
            content["semantic_role"] = slot.semantic_role
        return {
            "id": slot.id,
            "kind": slot.kind,
            "prompt": slot.prompt or "",
            "content": content,
        }

    if isinstance(slot, ChoiceSlot):
        return {
            "id": slot.id,
            "kind": slot.kind,
            "prompt": slot.prompt or "",
            "content": {
                "choices": list(slot.choices),
                "multiple_select": slot.multiple_select,
            },
        }

    if isinstance(slot, BlankSlot):
        return {
            "id": slot.id,
            "kind": slot.kind,
            "prompt": slot.prompt or "",
            "content": {
                "placeholder": slot.placeholder,
            },
        }

    if isinstance(slot, LabelSlot):
        return {
            "id": slot.id,
            "kind": slot.kind,
            "prompt": slot.prompt or "",
            "content": {
                "text": slot.text,
                "target_object_id": slot.target_object_id,
                "target_anchor": slot.target_anchor,
            },
        }

    if isinstance(slot, RectSlot):
        content: dict[str, Any] = {
            "x": float(slot.x),
            "y": float(slot.y),
            "width": float(slot.width),
            "height": float(slot.height),
        }
        if isinstance(slot.stroke, str):
            content["stroke"] = slot.stroke
        if slot.stroke_width is not None:
            content["stroke_width"] = float(slot.stroke_width)
        if slot.rx is not None:
            content["rx"] = float(slot.rx)
        if slot.ry is not None:
            content["ry"] = float(slot.ry)
        if isinstance(slot.fill, str):
            content["fill"] = slot.fill
        if isinstance(slot.semantic_role, str) and slot.semantic_role:
            content["semantic_role"] = slot.semantic_role
        return {
            "id": slot.id,
            "kind": slot.kind,
            "prompt": slot.prompt or "",
            "content": content,
        }

    if isinstance(slot, LineSlot):
        content: dict[str, Any] = {
            "x1": float(slot.x1 + slot.x),
            "y1": float(slot.y1 + slot.y),
            "x2": float(slot.x2 + slot.x),
            "y2": float(slot.y2 + slot.y),
        }
        if isinstance(slot.stroke, str):
            content["stroke"] = slot.stroke
        if slot.stroke_width is not None:
            content["stroke_width"] = float(slot.stroke_width)
        if isinstance(slot.stroke_dasharray, str) and slot.stroke_dasharray:
            content["stroke_dasharray"] = slot.stroke_dasharray
        if isinstance(slot.semantic_role, str) and slot.semantic_role:
            content["semantic_role"] = slot.semantic_role
        return {
            "id": slot.id,
            "kind": slot.kind,
            "prompt": slot.prompt or "",
            "content": content,
        }

    if isinstance(slot, CircleSlot):
        content: dict[str, Any] = {
            "cx": float(slot.cx),
            "cy": float(slot.cy),
            "r": float(slot.r),
        }
        if isinstance(slot.stroke, str):
            content["stroke"] = slot.stroke
        if slot.stroke_width is not None:
            content["stroke_width"] = float(slot.stroke_width)
        if isinstance(slot.fill, str):
            content["fill"] = slot.fill
        if isinstance(slot.semantic_role, str) and slot.semantic_role:
            content["semantic_role"] = slot.semantic_role
        return {
            "id": slot.id,
            "kind": slot.kind,
            "prompt": slot.prompt or "",
            "content": content,
        }

    if isinstance(slot, PolygonSlot):
        content: dict[str, Any] = {
            "points": [[float(x + slot.x), float(y + slot.y)] for x, y in slot.points],
        }
        if isinstance(slot.stroke, str):
            content["stroke"] = slot.stroke
        if slot.stroke_width is not None:
            content["stroke_width"] = float(slot.stroke_width)
        if isinstance(slot.fill, str):
            content["fill"] = slot.fill
        if isinstance(slot.semantic_role, str) and slot.semantic_role:
            content["semantic_role"] = slot.semantic_role
        return {
            "id": slot.id,
            "kind": slot.kind,
            "prompt": slot.prompt or "",
            "content": content,
        }

    if isinstance(slot, PathSlot):
        content: dict[str, Any] = {
            "d": slot.d,
            "x": float(slot.x),
            "y": float(slot.y),
        }
        if isinstance(slot.stroke, str):
            content["stroke"] = slot.stroke
        if slot.stroke_width is not None:
            content["stroke_width"] = float(slot.stroke_width)
        if isinstance(slot.stroke_dasharray, str) and slot.stroke_dasharray:
            content["stroke_dasharray"] = slot.stroke_dasharray
        if isinstance(slot.fill, str):
            content["fill"] = slot.fill
        if isinstance(slot.semantic_role, str) and slot.semantic_role:
            content["semantic_role"] = slot.semantic_role
        return {
            "id": slot.id,
            "kind": slot.kind,
            "prompt": slot.prompt or "",
            "content": content,
        }

    raise TypeError(f"Unsupported slot type: {type(slot)!r}")


def _normalize_group(group: Group) -> dict[str, Any]:
    return {
        "id": group.id,
        "role": group.role,
        "member_ids": list(group.member_ids),
    }


def _normalize_constraint(constraint: Constraint) -> dict[str, Any]:
    return {
        "id": constraint.id,
        "type": constraint.type,
        "target_ids": list(constraint.target_ids),
        "params": dict(sorted(constraint.params.items())),
    }


def _normalize_diagram(diagram: DiagramTemplate) -> dict[str, Any]:
    return {
        "id": diagram.id,
        "objects": [_normalize_shape_object(obj) for obj in diagram.objects],
        "label_slots": [_normalize_slot(slot) for slot in diagram.label_slots],
        "constraints": [_normalize_constraint(constraint) for constraint in diagram.constraints],
    }


def _normalize_shape_object(obj: ShapeObject) -> dict[str, Any]:
    return asdict(obj)


def _build_reading_order(regions: list[dict[str, Any]], diagrams: list[dict[str, Any]]) -> list[str]:
    ordered: list[str] = []
    seen: set[str] = set()

    def push(value: str) -> None:
        if value not in seen:
            ordered.append(value)
            seen.add(value)

    for region in regions:
        push(str(region["id"]))
        for slot_id in region["slot_ids"]:
            push(str(slot_id))

    for diagram in diagrams:
        push(str(diagram["id"]))
        for obj in diagram["objects"]:
            push(str(obj["id"]))
        for label_slot in diagram["label_slots"]:
            push(str(label_slot["id"]))

    return ordered
