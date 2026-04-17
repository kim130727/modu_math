from __future__ import annotations

from html import escape
from typing import Any

from ...renderer.models.primitive import RenderElement, RenderGroup, RenderText, RendererAST

def _float_str(value: float) -> str:
    ivalue = int(value)
    return str(ivalue) if value == ivalue else str(value)

def _attrs_to_str(attrs: dict[str, Any]) -> str:
    parts = []
    for key, value in attrs.items():
        if value is None:
            continue
        if key == "points" and isinstance(value, list):
            value = " ".join(
                f"{_float_str(float(point[0]))},{_float_str(float(point[1]))}"
                for point in value
            )
        if isinstance(value, (int, float)):
            value = _float_str(float(value))
        parts.append(f'{key}="{escape(str(value), quote=True)}"')
    return " ".join(parts)

def _element_to_svg_lines(element: RenderElement, depth: int = 1) -> list[str]:
    indent = "  " * depth
    attrs = {"id": element.id, **element.attributes}
    attrs_str = _attrs_to_str(attrs)

    if isinstance(element, RenderText):
        return [f"{indent}<text {attrs_str}>{escape(element.text)}</text>"]

    if isinstance(element, RenderGroup):
        lines = [f"{indent}<g {attrs_str}>"] if attrs_str else [f"{indent}<g>"]
        for child in element.elements:
            lines.extend(_element_to_svg_lines(child, depth + 1))
        lines.append(f"{indent}</g>")
        return lines

    tag = element.type
    if tag in {"rect", "circle", "line", "polygon"}:
        return [f"{indent}<{tag} {attrs_str} />"]
    return [f"{indent}<!-- Unsupported element type: {escape(tag)} -->"]

def render_svg(renderer: RendererAST | dict[str, Any]) -> str:
    if isinstance(renderer, dict):
        renderer_ast = RendererAST.from_dict(renderer)
    else:
        renderer_ast = renderer

    width = _float_str(float(renderer_ast.view_box.width))
    height = _float_str(float(renderer_ast.view_box.height))

    lines: list[str] = [
        "<?xml version=\"1.0\" encoding=\"UTF-8\"?>",
        f"<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"{width}\" height=\"{height}\" viewBox=\"0 0 {width} {height}\">",
    ]
    
    if renderer_ast.view_box.background:
        lines.append(
            f"  <rect x=\"0\" y=\"0\" width=\"{width}\" height=\"{height}\" fill=\"{escape(renderer_ast.view_box.background, quote=True)}\" />"
        )

    for element in renderer_ast.elements:
        lines.extend(_element_to_svg_lines(element, depth=1))

    lines.append("</svg>")
    return "\n".join(lines) + "\n"
