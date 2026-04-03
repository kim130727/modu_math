from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class ValidationIssue:
    level: str
    code: str
    message: str


class LayoutValidator:
    def validate(self, semantic: dict[str, Any]) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        render = semantic.get("render", {})
        canvas = render.get("canvas", {}) if isinstance(render, dict) else {}
        elements = render.get("elements", []) if isinstance(render, dict) else []

        w = float(canvas.get("width", 0)) if isinstance(canvas, dict) else 0
        h = float(canvas.get("height", 0)) if isinstance(canvas, dict) else 0
        if w <= 0 or h <= 0:
            return [ValidationIssue("error", "layout.canvas_size", "invalid canvas size")]

        for elem in elements:
            if not isinstance(elem, dict):
                continue
            bbox = _bbox(elem)
            if bbox is None:
                continue
            x1, y1, x2, y2 = bbox
            if x1 < 0 or y1 < 0 or x2 > w or y2 > h:
                issues.append(ValidationIssue("warning", "layout.out_of_canvas", f"{elem.get('id')} out of canvas"))

        eq_boxes = [_bbox(e) for e in elements if isinstance(e, dict) and e.get("semantic_role") == "equation"]
        blank_boxes = [_bbox(e) for e in elements if isinstance(e, dict) and e.get("semantic_role") == "answer_blank"]
        for eq in eq_boxes:
            for blank in blank_boxes:
                if eq and blank and _overlap(eq, blank):
                    issues.append(ValidationIssue("warning", "layout.equation_overlap_blank", "equation overlaps answer_blank"))
        return issues


def _bbox(elem: dict[str, Any]) -> tuple[float, float, float, float] | None:
    t = elem.get("type")
    if t == "rect":
        x, y = float(elem["x"]), float(elem["y"])
        w, h = float(elem["width"]), float(elem["height"])
        return (x, y, x + w, y + h)
    if t == "text":
        x, y = float(elem["x"]), float(elem["y"])
        fs = float(elem.get("font_size", 20))
        return (x - fs, y - fs, x + fs * 6, y + fs)
    if t == "line":
        x1, y1 = float(elem["x1"]), float(elem["y1"])
        x2, y2 = float(elem["x2"]), float(elem["y2"])
        return (min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))
    if t == "circle":
        cx, cy, r = float(elem["cx"]), float(elem["cy"]), float(elem["r"])
        return (cx - r, cy - r, cx + r, cy + r)
    if t == "polygon":
        pts = elem.get("points", [])
        if not pts:
            return None
        xs = [float(p[0]) for p in pts]
        ys = [float(p[1]) for p in pts]
        return (min(xs), min(ys), max(xs), max(ys))
    return None


def _overlap(a: tuple[float, float, float, float], b: tuple[float, float, float, float]) -> bool:
    return not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1])
