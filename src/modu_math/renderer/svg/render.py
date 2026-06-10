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

def _text_unit_width(ch: str, font_size: float) -> float:
    if ch.isspace():
        return font_size * 0.35
    if ord(ch) < 128:
        return font_size * 0.58
    return font_size * 0.92

def _text_width(text: str, font_size: float) -> float:
    return sum(_text_unit_width(ch, font_size) for ch in text)

def _wrap_long_token(token: str, max_width: float, font_size: float) -> list[str]:
    lines: list[str] = []
    current = ""
    for ch in token:
        trial = current + ch
        if current and _text_width(trial, font_size) > max_width:
            lines.append(current)
            current = ch
        else:
            current = trial
    if current:
        lines.append(current)
    return lines or [token]

def _wrap_text(text: str, max_width: float | None, font_size: float) -> list[str]:
    if not max_width or max_width <= 0:
        return text.split("\n")
    out: list[str] = []
    for paragraph in text.split("\n"):
        if not paragraph:
            out.append("")
            continue
        words = paragraph.split(" ")
        current = ""
        for word in words:
            pieces = _wrap_long_token(word, max_width, font_size)
            for piece in pieces:
                trial = piece if not current else f"{current} {piece}"
                if current and _text_width(trial, font_size) > max_width:
                    out.append(current)
                    current = piece
                else:
                    current = trial
        if current:
            out.append(current)
    return out or [""]

def _element_to_svg_lines(element: RenderElement, depth: int = 1) -> list[str]:
    indent = "  " * depth
    attrs = {"id": element.id, **element.attributes}

    if isinstance(element, RenderText):
        raw_max_width = attrs.pop("max_width", attrs.pop("max-width", None))
        max_width = float(raw_max_width) if isinstance(raw_max_width, (int, float)) else None
        font_size_raw = attrs.get("font-size", attrs.get("font_size", 26))
        font_size = float(font_size_raw) if isinstance(font_size_raw, (int, float)) else 26.0
        text_lines = _wrap_text(element.text, max_width, font_size)
        attrs_str = _attrs_to_str(attrs)
        if len(text_lines) <= 1:
            return [f"{indent}<text {attrs_str}>{escape(element.text)}</text>"]
        
        # Handle multiline text using <tspan>
        x = attrs.get("x", 0)
        res = [f"{indent}<text {attrs_str}>"]
        for i, line in enumerate(text_lines):
            dy = "0" if i == 0 else "1.2em"
            res.append(f'{indent}  <tspan x="{_float_str(float(x))}" dy="{dy}">{escape(line)}</tspan>')
        res.append(f"{indent}</text>")
        return res
    attrs_str = _attrs_to_str(attrs)
    if isinstance(element, RenderGroup):
        lines = [f"{indent}<g {attrs_str}>"] if attrs_str else [f"{indent}<g>"]
        for child in element.elements:
            lines.extend(_element_to_svg_lines(child, depth + 1))
        lines.append(f"{indent}</g>")
        return lines

    tag = "path" if element.type == "fill_path" else element.type
    if tag in {"rect", "circle", "line", "polygon", "path"}:
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
        f"  <metadata><problem_id>{escape(renderer_ast.problem_id)}</problem_id></metadata>",
    ]
    
    if renderer_ast.view_box.background:
        lines.append(
            f"  <rect x=\"0\" y=\"0\" width=\"{width}\" height=\"{height}\" fill=\"{escape(renderer_ast.view_box.background, quote=True)}\" />"
        )

    for element in renderer_ast.elements:
        lines.extend(_element_to_svg_lines(element, depth=1))

    lines.append("</svg>")
    return "\n".join(lines) + "\n"
