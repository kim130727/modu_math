from __future__ import annotations

import base64
from html import escape
import mimetypes
from pathlib import Path
import re
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

def _svg_paint_order(element: RenderElement) -> int:
    if isinstance(element, RenderText):
        return 100
    if isinstance(element, RenderGroup):
        return 80
    if element.type == "image":
        return 0
    return 50

def _ordered_for_svg(elements: list[RenderElement]) -> list[RenderElement]:
    return [element for _, element in sorted(enumerate(elements), key=lambda item: (_svg_paint_order(item[1]), item[0]))]

def _element_to_svg_lines(element: RenderElement, depth: int = 1) -> list[str]:
    indent = "  " * depth
    attrs = {"id": element.id, **element.attributes}

    if isinstance(element, RenderText):
        if element.type == "text_box":
            raw_width = attrs.pop("width", attrs.get("data-box-width", None))
            raw_height = attrs.pop("height", attrs.get("data-box-height", None))
            box_width = float(raw_width) if isinstance(raw_width, (int, float)) else 0.0
            box_height = float(raw_height) if isinstance(raw_height, (int, float)) else 0.0
            x = float(attrs.get("x", 0))
            y = float(attrs.get("y", 0))
            font_size_raw = attrs.get("font-size", attrs.get("font_size", 26))
            font_size = float(font_size_raw) if isinstance(font_size_raw, (int, float)) else 26.0
            line_height_raw = attrs.get("data-line-height", 1.2)
            line_height = float(line_height_raw) if isinstance(line_height_raw, (int, float)) else 1.2
            line_step = font_size * line_height
            text_lines = _wrap_text(element.text, box_width if box_width > 0 else None, font_size)
            total_height = max(len(text_lines), 1) * line_step
            valign = str(attrs.pop("data-vertical-align", "top"))
            align = str(attrs.pop("data-text-align", "left"))
            if align == "center":
                attrs["text-anchor"] = "middle"
                line_x = x + box_width / 2
            elif align == "right":
                attrs["text-anchor"] = "end"
                line_x = x + box_width
            else:
                attrs["text-anchor"] = "start"
                line_x = x
            if valign == "middle" and box_height > total_height:
                baseline_y = y + (box_height - total_height) / 2 + font_size
            elif valign == "bottom" and box_height > total_height:
                baseline_y = y + box_height - total_height + font_size
            else:
                baseline_y = y + font_size
            attrs["x"] = line_x
            attrs["y"] = baseline_y
            attrs_str = _attrs_to_str(attrs)
            if len(text_lines) <= 1:
                return [f'{indent}<text {attrs_str}>{escape(element.text)}</text>']
            attrs["data-raw-text"] = element.text
            attrs_str = _attrs_to_str(attrs)
            res = [f"{indent}<text {attrs_str}>"]
            for i, line in enumerate(text_lines):
                line_y = baseline_y + i * line_step
                res.append(f'{indent}  <tspan x="{_float_str(line_x)}" y="{_float_str(line_y)}">{escape(line)}</tspan>')
            res.append(f"{indent}</text>")
            return res

        font_size_raw = attrs.get("font-size", attrs.get("font_size", 26))
        font_size = float(font_size_raw) if isinstance(font_size_raw, (int, float)) else 26.0
        # Plain TextSlot is positioned text, not a text box. Keep SVG output in
        # sync with tldraw by honoring only explicit newlines here; automatic
        # width-based wrapping belongs to text_box.
        text_lines = element.text.split("\n")
        attrs_str = _attrs_to_str(attrs)
        if len(text_lines) <= 1:
            return [f"{indent}<text {attrs_str}>{escape(element.text)}</text>"]

        attrs["data-raw-text"] = element.text
        attrs_str = _attrs_to_str(attrs)
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
        for child in _ordered_for_svg(element.elements):
            lines.extend(_element_to_svg_lines(child, depth + 1))
        lines.append(f"{indent}</g>")
        return lines

    tag = "path" if element.type == "fill_path" else element.type
    if tag == "image" and "href" in attrs and "xlink:href" not in attrs:
        attrs["xlink:href"] = attrs["href"]
        attrs_str = _attrs_to_str(attrs)
    if tag in {"rect", "circle", "line", "polygon", "path", "image"}:
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
        f"<svg xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" width=\"{width}\" height=\"{height}\" viewBox=\"0 0 {width} {height}\">",
        f"  <metadata><problem_id>{escape(renderer_ast.problem_id)}</problem_id></metadata>",
    ]
    
    if renderer_ast.view_box.background:
        lines.append(
            f"  <rect x=\"0\" y=\"0\" width=\"{width}\" height=\"{height}\" fill=\"{escape(renderer_ast.view_box.background, quote=True)}\" />"
        )

    for element in _ordered_for_svg(renderer_ast.elements):
        lines.extend(_element_to_svg_lines(element, depth=1))

    lines.append("</svg>")
    return "\n".join(lines) + "\n"


def inline_local_image_hrefs(svg: str, base_dir: Path) -> str:
    """Embed local image hrefs as data URIs so saved SVG files are standalone."""
    resolved_base = base_dir.resolve()
    cache: dict[str, str] = {}

    def data_uri_for(href: str) -> str | None:
        if (
            not href
            or href.startswith("#")
            or href.startswith("/")
            or href.startswith("data:")
            or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", href)
        ):
            return None
        if "/" in href or "\\" in href:
            return None
        if href in cache:
            return cache[href]
        image_path = (resolved_base / href).resolve()
        if image_path.parent != resolved_base or not image_path.is_file():
            return None
        mime = mimetypes.guess_type(image_path.name)[0] or "image/png"
        encoded = base64.b64encode(image_path.read_bytes()).decode("ascii")
        cache[href] = f"data:{mime};base64,{encoded}"
        return cache[href]

    def replace(match: re.Match[str]) -> str:
        attr = match.group("attr")
        quote = match.group("quote")
        href = match.group("href")
        embedded = data_uri_for(href)
        if embedded is None:
            return match.group(0)
        return f"{attr}={quote}{embedded}{quote}"

    return re.sub(
        r"(?P<attr>\b(?:href|xlink:href))=(?P<quote>['\"])(?P<href>.*?)(?P=quote)",
        replace,
        svg,
    )
