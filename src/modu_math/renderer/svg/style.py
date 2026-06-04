from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Style:
    fill: str | None = None
    stroke: str | None = None
    stroke_width: float | None = None
    font_family: str | None = None
    font_size: int | None = None
