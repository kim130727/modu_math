from __future__ import annotations

from pathlib import Path
from xml.sax.saxutils import escape


def render_svg_from_semantic(semantic: dict, svg_path: Path) -> Path:
    """
    Render minimal SVG primitives from semantic data.

    Supported elements:
    - text
    - rect
    - line (optional dashed style)
    """
    canvas = semantic["canvas"]
    elements = semantic["elements"]

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        (
            f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'width="{canvas["width"]}" height="{canvas["height"]}" '
            f'viewBox="0 0 {canvas["width"]} {canvas["height"]}">'
        ),
        (
            f'  <rect x="0" y="0" width="{canvas["width"]}" '
            f'height="{canvas["height"]}" fill="{canvas["background"]}" />'
        ),
    ]

    for element in elements:
        element_type = element["type"]

        if element_type == "rect":
            lines.append(_render_rect(element))
        elif element_type == "line":
            lines.append(_render_line(element))
        elif element_type == "text":
            lines.append(_render_text(element))

    lines.append("</svg>")

    svg_path.parent.mkdir(parents=True, exist_ok=True)
    svg_path.write_text("\n".join(lines), encoding="utf-8")
    return svg_path


def _render_rect(element: dict) -> str:
    return (
        f'  <rect id="{escape(element["id"])}" '
        f'x="{element["x"]}" y="{element["y"]}" '
        f'width="{element["width"]}" height="{element["height"]}" '
        f'rx="{element.get("rx", 0)}" '
        f'stroke="{element.get("stroke", "none")}" '
        f'stroke-width="{element.get("stroke_width", 0)}" '
        f'fill="{element.get("fill", "none")}" />'
    )


def _render_line(element: dict) -> str:
    dash = element.get("dasharray")
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'  <line id="{escape(element["id"])}" '
        f'x1="{element["x1"]}" y1="{element["y1"]}" '
        f'x2="{element["x2"]}" y2="{element["y2"]}" '
        f'stroke="{element.get("stroke", "#000000")}" '
        f'stroke-width="{element.get("stroke_width", 1)}"{dash_attr} />'
    )


def _render_text(element: dict) -> str:
    text = escape(element["text"])
    anchor = escape(element.get("anchor", "start"))
    family = escape(element.get("font_family", "sans-serif"))
    return (
        f'  <text id="{escape(element["id"])}" '
        f'x="{element["x"]}" y="{element["y"]}" '
        f'font-family="{family}" font-size="{element["font_size"]}" '
        f'fill="{element.get("fill", "#000000")}" '
        f'font-weight="{element.get("font_weight", "normal")}" '
        f'text-anchor="{anchor}">{text}</text>'
    )
