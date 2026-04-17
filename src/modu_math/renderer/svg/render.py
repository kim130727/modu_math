from __future__ import annotations

from html import escape
from ...layout.models.canvas import LayoutCanvas
from ...layout.models.node import LayoutNode, ShapeNode, TextNode

def _float_str(value: float) -> str:
    ivalue = int(value)
    return str(ivalue) if value == ivalue else str(value)

def _attrs_to_str(attrs: dict[str, str | None]) -> str:
    parts = []
    for key, value in attrs.items():
        if value is None:
            continue
        parts.append(f'{key}="{escape(str(value), quote=True)}"')
    return " ".join(parts)

def _style_attrs(props: dict[str, Any]) -> dict[str, str | None]:
    attrs: dict[str, str | None] = {}
    if "stroke" in props:
        attrs["stroke"] = props["stroke"]
    if "stroke_width" in props:
        attrs["stroke-width"] = _float_str(float(props["stroke_width"]))
    if "fill" in props:
        attrs["fill"] = props["fill"]
    if "font_family" in props:
        attrs["font-family"] = props["font_family"]
    if "font_size" in props:
        attrs["font-size"] = f"{_float_str(float(props['font_size']))}px"
    if "font_weight" in props:
        attrs["font-weight"] = props["font_weight"]
    return attrs

def _base_attrs(node: LayoutNode) -> dict[str, str | None]:
    attrs: dict[str, str | None] = {"id": node.id}
    
    if "group" in node.properties:
        attrs["data-group"] = node.properties["group"]
    if "semantic_role" in node.properties:
        attrs["data-semantic-role"] = node.properties["semantic_role"]
        
    attrs.update(_style_attrs(node.properties))
    return attrs

def _node_to_svg_line(node: LayoutNode) -> str:
    attrs = _base_attrs(node)

    if isinstance(node, ShapeNode):
        shape_type = node.shape_type
        if shape_type == "rect":
            attrs.update({
                "x": _float_str(float(node.x)),
                "y": _float_str(float(node.y)),
                "width": _float_str(float(node.width or 0)),
                "height": _float_str(float(node.height or 0)),
            })
            if "rx" in node.properties:
                attrs["rx"] = _float_str(float(node.properties["rx"]))
            if "ry" in node.properties:
                attrs["ry"] = _float_str(float(node.properties["ry"]))
            return f"  <rect {_attrs_to_str(attrs)} />"
            
        elif shape_type == "circle":
            attrs.update({
                "cx": _float_str(float(node.x)),
                "cy": _float_str(float(node.y)),
                "r": _float_str(float(node.properties.get("r", 0))),
            })
            return f"  <circle {_attrs_to_str(attrs)} />"
            
        elif shape_type == "line":
            attrs.update({
                "x1": _float_str(float(node.properties.get("x1", node.x))),
                "y1": _float_str(float(node.properties.get("y1", node.y))),
                "x2": _float_str(float(node.properties.get("x2", 0))),
                "y2": _float_str(float(node.properties.get("y2", 0))),
            })
            return f"  <line {_attrs_to_str(attrs)} />"
            
        elif shape_type == "polygon":
            points = node.properties.get("points", [])
            points_str = " ".join([f"{_float_str(float(p[0]))},{_float_str(float(p[1]))}" for p in points])
            attrs.update({"points": points_str})
            return f"  <polygon {_attrs_to_str(attrs)} />"

    elif isinstance(node, TextNode):
        attrs.update({
            "x": _float_str(float(node.x)),
            "y": _float_str(float(node.y)),
        })
        if node.anchor:
            attrs["text-anchor"] = node.anchor
            
        if node.properties.get("is_formula", False):
            attrs["data-formula"] = node.text
            attrs["class"] = "formula-placeholder"
            
        return f"  <text {_attrs_to_str(attrs)}>{escape(node.text)}</text>"

    return f"  <!-- Unsupported node type: {node.type} -->"

def render_svg(canvas: LayoutCanvas, nodes: list[LayoutNode]) -> str:
    sorted_nodes = sorted(nodes, key=lambda n: n.z_order)
    width = _float_str(float(canvas.width))
    height = _float_str(float(canvas.height))

    lines: list[str] = [
        "<?xml version=\"1.0\" encoding=\"UTF-8\"?>",
        f"<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"{width}\" height=\"{height}\" viewBox=\"0 0 {width} {height}\">",
    ]
    
    if canvas.background:
        lines.append(f"  <rect x=\"0\" y=\"0\" width=\"{width}\" height=\"{height}\" fill=\"{escape(canvas.background, quote=True)}\" />")

    for node in sorted_nodes:
        lines.append(_node_to_svg_line(node))

    lines.append("</svg>")
    return "\n".join(lines) + "\n"
