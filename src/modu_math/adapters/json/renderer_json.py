from __future__ import annotations
from typing import Any

from ...layout.models.canvas import LayoutCanvas
from ...layout.models.node import LayoutNode, ShapeNode, TextNode
from ...renderer.models.primitive import RendererAST, RenderViewBox, RenderElement, RenderText

def _extract_render_attributes(node: LayoutNode) -> dict[str, Any]:
    """Flattens layout and semantic properties into pure visual attributes."""
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
        
    # Semantic roles translate to data- attributes for CSS targeting
    if "semantic_role" in node.properties:
        attrs["data-semantic-role"] = node.properties["semantic_role"]
    if "group" in node.properties:
        attrs["data-group"] = node.properties["group"]
        
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
        attrs = _extract_render_attributes(node)
        
        if isinstance(node, ShapeNode):
            elements.append(RenderElement(
                id=node.id,
                type=node.shape_type,
                attributes=attrs
            ))
        elif isinstance(node, TextNode):
            elements.append(RenderText(
                id=node.id,
                attributes=attrs,
                text=node.text
            ))
            
    return RendererAST(problem_id=problem_id, view_box=view_box, elements=elements)
