"""Deterministic, whitespace-preserving text fitting for fixed diagram layouts."""
from __future__ import annotations

from copy import deepcopy
import re
import unicodedata


def text_clusters(text: str) -> list[str]:
    """Keep combining marks, Khmer coeng sequences and joiners with their base."""
    clusters: list[str] = []
    for char in text:
        if clusters and (unicodedata.category(char).startswith("M")
                         or char in "\u200c\u200d"
                         or clusters[-1].endswith(("\u17d2", "\u200d"))):
            clusters[-1] += char
        else:
            clusters.append(char)
    return clusters


def text_width(text: str, font_size: float) -> float:
    # Conservative fallback metrics, independent of a Korean-only font's cmap.
    units = 0.0
    for cluster in text_clusters(text):
        char = cluster[0]
        if char == "\t":
            units += 1.4
        elif char.isspace():
            units += 0.35
        elif char in "\u200b\u200c\u200d" or unicodedata.category(char).startswith("M"):
            continue
        elif unicodedata.east_asian_width(char) in {"W", "F"}:
            units += 1.0
        elif "\u1780" <= char <= "\u17ff":
            units += 1.05
        elif char in "ilI.,:;!'|()":
            units += 0.32
        elif char.isdigit():
            units += 0.58
        elif char in "MWmw@":
            units += 0.95
        else:
            units += 0.65
    return units * font_size


def wrap_text(text: str, max_width: float | None, font_size: float) -> list[str]:
    if not max_width or max_width <= 0:
        return text.split("\n")
    lines: list[str] = []
    for paragraph in text.split("\n"):
        current = ""
        for token in re.findall(r"[^\S\n]+|[^\s]+", paragraph):
            if current and text_width(current + token, font_size) > max_width:
                lines.append(current)
                current = ""
            for cluster in text_clusters(token):
                if current and text_width(current + cluster, font_size) > max_width:
                    lines.append(current)
                    current = ""
                current += cluster
        lines.append(current)
    return lines


def fit_prompt_text(layout: dict) -> dict:
    """Bound prose above the diagram; never move arithmetic or diagram slots.

    Text edits stay in the source unchanged. Only the display layout is fitted.
    An authored text box retains its origin and extent.
    """
    result = deepcopy(layout)
    canvas_width = float(result["canvas"]["width"])
    canvas_height = float(result["canvas"]["height"])
    slots = result.get("slots", [])
    for slot in slots:
        content = slot.get("content", {})
        if slot.get("kind") not in {"text", "text_box"}:
            continue
        if content.get("semantic_role") not in {"question", "instruction"}:
            continue
        if content.get("transform") or content.get("interaction"):
            continue
        if not isinstance(content.get("x"), (int, float)) or not isinstance(content.get("y"), (int, float)):
            continue
        font = float(content.get("font_size") or 26)
        x, y = float(content["x"]), float(content["y"])
        if slot["kind"] == "text":
            # A positioned label in a diagram must not become a prose box.
            if content.get("anchor") not in {None, "start"} or y > canvas_height * 0.3:
                continue
            top = max(0.0, y - font)
            body_tops = []
            for other in slots:
                if other is slot:
                    continue
                c = other.get("content", {})
                if c.get("semantic_role") in {"question", "instruction"}:
                    continue
                candidates = [c[k] for k in ("y", "y1", "y2") if isinstance(c.get(k), (int, float))]
                if candidates:
                    body_top = min(candidates)
                    if other["kind"] == "text":
                        body_top -= float(c.get("font_size") or 26)
                    if body_top >= y:
                        body_tops.append(body_top)
            bottom = min(body_tops, default=min(canvas_height - 16, y + font * 2)) - 8
            if bottom - top < font:
                continue
            slot["kind"] = "text_box"
            content.update(x=x, y=top, width=max(1.0, canvas_width - x - 24),
                           height=bottom - top, align="left", valign="top")
        width = min(float(content.get("width") or 0), canvas_width - x - 16)
        height = min(float(content.get("height") or 0), canvas_height - float(content["y"]))
        if width <= 0 or height <= 0:
            continue
        line_height = float(content.get("line_height") or 1.3)
        text = str(content.get("text", ""))
        # Khmer marks need more vertical room than Latin ascenders.
        if any("\u1780" <= c <= "\u17ff" for c in text):
            line_height = max(line_height, 1.5)
        fitted = font
        minimum = min(font, 12.0)
        while fitted > minimum and len(wrap_text(text, width, fitted)) * fitted * line_height > height:
            fitted = max(minimum, fitted - 0.5)
        if len(wrap_text(text, width, fitted)) * fitted * line_height > height:
            raise ValueError(f"Text slot {slot['id']} does not fit its box; enlarge the text box")
        content.update(width=width, height=height, font_size=fitted, line_height=line_height)
    return result
