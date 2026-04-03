from __future__ import annotations

from pathlib import Path
from xml.sax.saxutils import escape

from modu_math.renderers.base_renderer import BaseRenderer


class SvgRenderer(BaseRenderer):
    @staticmethod
    def _optional_common_attrs(e: dict) -> str:
        attrs: list[str] = []
        if "transform" in e:
            attrs.append(f' transform="{escape(str(e["transform"]))}"')
        if "style" in e:
            attrs.append(f' style="{escape(str(e["style"]))}"')
        return "".join(attrs)

    def render_to_file(self, semantic: dict, out_path: Path) -> Path:
        render = semantic["render"]
        canvas = render["canvas"]
        elements = render["elements"]

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

        for elem in elements:
            lines.append(self._render_element(elem))

        lines.append("</svg>")
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text("\n".join(lines), encoding="utf-8")
        return out_path

    def _render_element(self, elem: dict) -> str:
        t = elem["type"]
        if t == "text":
            return self._text(elem)
        if t == "rect":
            return self._rect(elem)
        if t == "line":
            return self._line(elem)
        if t == "circle":
            return self._circle(elem)
        if t == "polygon":
            return self._polygon(elem)
        if t in {"path", "arc", "group", "transform", "image"}:
            raise NotImplementedError(f"svg primitive not yet implemented: {t}")
        raise ValueError(f"unsupported primitive: {t}")

    @staticmethod
    def _text(e: dict) -> str:
        text = escape(e["text"])
        anchor = e.get("anchor", "start")
        family = escape(e.get("font_family", "sans-serif"))
        extra = SvgRenderer._optional_common_attrs(e)
        return (
            f'  <text id="{escape(e["id"])}" x="{e["x"]}" y="{e["y"]}" '
            f'font-family="{family}" font-size="{e.get("font_size", 16)}" '
            f'fill="{e.get("fill", "#000000")}" '
            f'font-weight="{e.get("font_weight", "normal")}" '
            f'text-anchor="{anchor}"{extra}>{text}</text>'
        )

    @staticmethod
    def _rect(e: dict) -> str:
        extra = SvgRenderer._optional_common_attrs(e)
        return (
            f'  <rect id="{escape(e["id"])}" x="{e["x"]}" y="{e["y"]}" '
            f'width="{e["width"]}" height="{e["height"]}" '
            f'rx="{e.get("rx", 0)}" '
            f'stroke="{e.get("stroke", "none")}" '
            f'stroke-width="{e.get("stroke_width", 0)}" '
            f'fill="{e.get("fill", "none")}"{extra} />'
        )

    @staticmethod
    def _line(e: dict) -> str:
        extra = SvgRenderer._optional_common_attrs(e)
        dash = f' stroke-dasharray="{e["dasharray"]}"' if "dasharray" in e else ""
        return (
            f'  <line id="{escape(e["id"])}" x1="{e["x1"]}" y1="{e["y1"]}" '
            f'x2="{e["x2"]}" y2="{e["y2"]}" '
            f'stroke="{e.get("stroke", "#000000")}" '
            f'stroke-width="{e.get("stroke_width", 1)}"{dash}{extra} />'
        )

    @staticmethod
    def _circle(e: dict) -> str:
        extra = SvgRenderer._optional_common_attrs(e)
        return (
            f'  <circle id="{escape(e["id"])}" cx="{e["cx"]}" cy="{e["cy"]}" r="{e["r"]}" '
            f'stroke="{e.get("stroke", "none")}" stroke-width="{e.get("stroke_width", 0)}" '
            f'fill="{e.get("fill", "none")}"{extra} />'
        )

    @staticmethod
    def _polygon(e: dict) -> str:
        extra = SvgRenderer._optional_common_attrs(e)
        points = " ".join(f"{p[0]},{p[1]}" for p in e["points"])
        return (
            f'  <polygon id="{escape(e["id"])}" points="{points}" '
            f'stroke="{e.get("stroke", "none")}" stroke-width="{e.get("stroke_width", 0)}" '
            f'fill="{e.get("fill", "none")}"{extra} />'
        )
