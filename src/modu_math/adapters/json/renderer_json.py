from __future__ import annotations
from typing import Any

from ...layout.models.canvas import LayoutCanvas
from ...layout.models.group import LayoutGroup
from ...layout.models.node import LayoutNode, ShapeNode, TextNode
from ...renderer.models.primitive import (
    RenderCircle,
    RenderElement,
    RenderGroup,
    RenderLine,
    RenderPolygon,
    RenderRect,
    RendererAST,
    RenderText,
    RenderViewBox,
)

def _extract_render_attributes(node: LayoutNode) -> dict[str, Any]:
    """Extract only SVG-relevant visual attributes for renderer output."""
    attrs: dict[str, Any] = {}
    props = node.properties if isinstance(node.properties, dict) else {}

    if isinstance(node, TextNode):
        attrs["x"] = node.x
        attrs["y"] = node.y
        if node.anchor:
            attrs["text-anchor"] = node.anchor
        for key in ["fill", "stroke", "stroke_width", "font_family", "font_size", "font_weight", "font_style", "opacity", "transform", "stroke_dasharray"]:
            if key in props:
                attrs[key.replace("_", "-")] = props[key]
        if props.get("is_formula"):
            attrs["data-formula"] = node.text
            attrs["class"] = "formula-placeholder"
        return attrs

    if isinstance(node, ShapeNode):
        shape_style_keys = ["fill", "stroke", "stroke_width", "opacity", "transform", "stroke_dasharray"]
        for key in shape_style_keys:
            if key in props:
                attrs[key.replace("_", "-")] = props[key]

        if node.shape_type == "rect":
            attrs["x"] = node.x
            attrs["y"] = node.y
            if node.width is not None:
                attrs["width"] = node.width
            if node.height is not None:
                attrs["height"] = node.height
            for key in ["rx", "ry"]:
                if key in props:
                    attrs[key] = props[key]
            return attrs

        if node.shape_type == "circle":
            attrs["cx"] = node.x
            attrs["cy"] = node.y
            if "r" in props:
                attrs["r"] = props["r"]
            return attrs

        if node.shape_type == "line":
            attrs["x1"] = props.get("x1", node.x)
            attrs["y1"] = props.get("y1", node.y)
            if "x2" in props:
                attrs["x2"] = props["x2"]
            if "y2" in props:
                attrs["y2"] = props["y2"]
            return attrs

        if node.shape_type == "polygon":
            if "points" in props:
                attrs["points"] = props["points"]
            return attrs

        if node.shape_type == "path":
            if "d" in props:
                attrs["d"] = props["d"]
            return attrs

        # Fallback shape type
        attrs["x"] = node.x
        attrs["y"] = node.y
        if node.width is not None:
            attrs["width"] = node.width
        if node.height is not None:
            attrs["height"] = node.height
        return attrs

    # Unknown node type fallback
    if hasattr(node, "x"):
        attrs["x"] = node.x
    if hasattr(node, "y"):
        attrs["y"] = node.y
    return attrs

def _node_to_render_element(node: LayoutNode) -> RenderElement | None:
    attrs = _extract_render_attributes(node)

    if isinstance(node, ShapeNode):
        if node.shape_type == "rect":
            return RenderRect(id=node.id, attributes=attrs)
        if node.shape_type == "circle":
            return RenderCircle(id=node.id, attributes=attrs)
        if node.shape_type == "line":
            return RenderLine(id=node.id, attributes=attrs)
        if node.shape_type == "polygon":
            return RenderPolygon(id=node.id, attributes=attrs)
        if node.shape_type == "path":
            return RenderElement(id=node.id, type="path", attributes=attrs)
        return RenderElement(id=node.id, type=node.shape_type, attributes=attrs)

    if isinstance(node, TextNode):
        return RenderText(id=node.id, attributes=attrs, text=node.text)

    if isinstance(node, LayoutGroup):
        children = sorted(node.children, key=lambda child: child.z_order)
        group_elements: list[RenderElement] = []
        for child in children:
            child_element = _node_to_render_element(child)
            if child_element:
                group_elements.append(child_element)
        return RenderGroup(id=node.id, attributes=attrs, elements=group_elements)

    return None

def layout_to_renderer(problem_id: str, canvas: LayoutCanvas, nodes: list[LayoutNode]) -> RendererAST:
    """Converts the Layout layer into a pure Renderer AST."""
    
    view_box = RenderViewBox(
        width=canvas.width,
        height=canvas.height,
        background=canvas.background
    )
    
    elements: list[RenderElement] = []
    
    # Sort nodes by z_order
    sorted_nodes = sorted(nodes, key=lambda n: n.z_order)
    
    for node in sorted_nodes:
        element = _node_to_render_element(node)
        if element:
            elements.append(element)
            
    return RendererAST(problem_id=problem_id, view_box=view_box, elements=elements)
