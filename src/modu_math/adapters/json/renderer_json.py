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
    """Flattens layout properties into pure visual attributes."""
    attrs: dict[str, Any] = {}
    
    # Common layout
    if hasattr(node, "x"):
        attrs["x"] = node.x
    if hasattr(node, "y"):
        attrs["y"] = node.y
    if hasattr(node, "width") and node.width is not None:
        attrs["width"] = node.width
    if hasattr(node, "height") and node.height is not None:
        attrs["height"] = node.height
        
    # Styles
    for style_key in ["fill", "stroke", "stroke_width", "font_family", "font_size", "font_weight", "rx", "ry", "r", "x1", "y1", "x2", "y2", "points"]:
        if style_key in node.properties:
            # SVG attributes use dashes
            svg_key = style_key.replace("_", "-")
            attrs[svg_key] = node.properties[style_key]
            
    if isinstance(node, TextNode):
        if node.anchor:
            attrs["text-anchor"] = node.anchor
        if node.properties.get("is_formula"):
            attrs["data-formula"] = node.text
            attrs["class"] = "formula-placeholder"

    # Shape specific
    if isinstance(node, ShapeNode):
        if node.shape_type == "circle":
            attrs["cx"] = attrs.pop("x", 0)
            attrs["cy"] = attrs.pop("y", 0)

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
