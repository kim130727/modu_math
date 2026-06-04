from __future__ import annotations

from typing import Any

from ...layout.models.canvas import LayoutCanvas
from ...layout.models.group import LayoutGroup
from ...layout.models.node import LayoutNode, ShapeNode, TextNode


def layout_to_layout_json(problem_id: str, canvas: LayoutCanvas, nodes: list[LayoutNode]) -> dict[str, Any]:
    """Serialize the layout contract payload from layout models."""
    return {
        "problem_id": problem_id,
        "canvas": canvas.to_dict(),
        "nodes": [node.to_dict() for node in nodes],
    }


def layout_json_to_models(data: dict[str, Any]) -> tuple[str, LayoutCanvas, list[LayoutNode]]:
    """
    Parse a layout contract payload into layout models.

    This adapter is intentionally tolerant for backward compatibility with
    older or partially-populated payloads.
    """
    problem_id = str(data.get("problem_id") or "")
    canvas_raw = data.get("canvas", {})
    if not isinstance(canvas_raw, dict):
        canvas_raw = {}
    canvas = LayoutCanvas(
        width=float(canvas_raw.get("width", 0)),
        height=float(canvas_raw.get("height", 0)),
        background=canvas_raw.get("background"),
    )

    nodes_raw = data.get("nodes", [])
    nodes: list[LayoutNode] = []
    if not isinstance(nodes_raw, list):
        return problem_id, canvas, nodes

    for raw in nodes_raw:
        if not isinstance(raw, dict):
            continue
        node = _parse_node(raw)
        if node is not None:
            nodes.append(node)
    return problem_id, canvas, nodes


def _parse_node(raw: dict[str, Any]) -> LayoutNode | None:
    node_type = str(raw.get("type", ""))
    node_id = str(raw.get("id", ""))
    base_kwargs = {
        "id": node_id,
        "x": float(raw.get("x", 0)),
        "y": float(raw.get("y", 0)),
        "width": _optional_float(raw.get("width")),
        "height": _optional_float(raw.get("height")),
        "anchor": raw.get("anchor"),
        "rotation": _optional_float(raw.get("rotation")),
        "z_order": int(raw.get("z_order", 0)) if isinstance(raw.get("z_order", 0), int | float) else 0,
        "source_ref": raw.get("source_ref"),
        "properties": dict(raw.get("properties", {})) if isinstance(raw.get("properties"), dict) else {},
    }

    if node_type == "text":
        props = base_kwargs["properties"]
        text = str(props.get("text", ""))
        return TextNode(text=text, **base_kwargs)

    if node_type == "shape":
        props = base_kwargs["properties"]
        shape_type = str(props.get("shape_type", "rect"))
        return ShapeNode(shape_type=shape_type, **base_kwargs)

    if node_type == "group":
        group = LayoutGroup(**base_kwargs)
        children_raw = raw.get("children", [])
        if isinstance(children_raw, list):
            children: list[LayoutNode] = []
            for child_raw in children_raw:
                if not isinstance(child_raw, dict):
                    continue
                child = _parse_node(child_raw)
                if child is not None:
                    children.append(child)
            group.children = children
        return group

    if node_id:
        return LayoutNode(type=node_type or "node", **base_kwargs)
    return None


def _optional_float(value: Any) -> float | None:
    if value is None:
        return None
    if isinstance(value, int | float):
        return float(value)
    return None
