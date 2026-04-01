"""Geometry helper utilities."""

from __future__ import annotations

from typing import Iterable


def bbox_union(boxes: Iterable[tuple[float, float, float, float]]) -> tuple[float, float, float, float]:
    boxes = list(boxes)
    if not boxes:
        return (0.0, 0.0, 0.0, 0.0)
    x0 = min(b[0] for b in boxes)
    y0 = min(b[1] for b in boxes)
    x1 = max(b[2] for b in boxes)
    y1 = max(b[3] for b in boxes)
    return (x0, y0, x1, y1)


def normalize_point(x: float, y: float, width: float, height: float) -> tuple[float, float]:
    if width == 0 or height == 0:
        return (0.0, 0.0)
    return (x / width, y / height)
