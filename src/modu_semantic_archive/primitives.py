from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Rect:
    id: str
    x: float
    y: float
    width: float
    height: float
    fill: str = "none"
    stroke: str = "#000000"
    stroke_width: float = 1.0
    rx: float | None = None
    ry: float | None = None
    semantic_role: str | None = None
    metadata: dict[str, object] = field(default_factory=dict)


@dataclass
class Circle:
    id: str
    cx: float
    cy: float
    r: float
    fill: str = "none"
    stroke: str = "#000000"
    stroke_width: float = 1.0
    semantic_role: str | None = None
    metadata: dict[str, object] = field(default_factory=dict)


@dataclass
class Line:
    id: str
    x1: float
    y1: float
    x2: float
    y2: float
    stroke: str = "#000000"
    stroke_width: float = 1.0
    semantic_role: str | None = None
    metadata: dict[str, object] = field(default_factory=dict)


@dataclass
class Polygon:
    id: str
    points: list[tuple[float, float]]
    fill: str = "none"
    stroke: str = "#000000"
    stroke_width: float = 1.0
    semantic_role: str | None = None
    metadata: dict[str, object] = field(default_factory=dict)


@dataclass
class Text:
    id: str
    x: float
    y: float
    text: str
    font_size: int = 16
    fill: str = "#000000"
    font_family: str = "sans-serif"
    anchor: str = "start"
    semantic_role: str | None = None
    metadata: dict[str, object] = field(default_factory=dict)


@dataclass
class Formula:
    id: str
    x: float
    y: float
    expr: str
    font_size: int = 18
    fill: str = "#000000"
    font_family: str = "serif"
    anchor: str = "start"
    semantic_role: str | None = None
    metadata: dict[str, object] = field(default_factory=dict)

    def __init__(
        self,
        id: str,
        x: float,
        y: float,
        expr: str | None = None,
        *,
        text: str | None = None,
        font_size: int = 18,
        fill: str = "#000000",
        font_family: str = "serif",
        anchor: str = "start",
        semantic_role: str | None = None,
        metadata: dict[str, object] | None = None,
    ) -> None:
        # Backward compatibility: accept legacy `text` input and map to canonical `expr`.
        if expr is None:
            if text is None:
                raise TypeError("Formula requires 'expr' (legacy alias: 'text').")
            expr = text
        self.id = id
        self.x = x
        self.y = y
        self.expr = expr
        self.font_size = font_size
        self.fill = fill
        self.font_family = font_family
        self.anchor = anchor
        self.semantic_role = semantic_role
        self.metadata = dict(metadata) if isinstance(metadata, dict) else {}
