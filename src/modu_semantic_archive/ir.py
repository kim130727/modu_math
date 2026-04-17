from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal, Union

Anchor = Literal["start", "middle", "end"]
Alignment = Literal["left", "center", "right"]


@dataclass
class CommonAttrs:
    id: str
    group: str | None = None
    metadata: dict[str, object] = field(default_factory=dict)
    z_index: int = 0
    anchor: Anchor = "start"
    alignment: Alignment = "left"
    semantic_role: str | None = None
    stroke: str | None = None
    stroke_width: float | None = None
    fill: str | None = None
    font_family: str | None = "Malgun Gothic"
    font_size: float | None = None
    font_weight: str | None = "normal"


@dataclass
class Rect(CommonAttrs):
    x: float = 0
    y: float = 0
    width: float = 0
    height: float = 0
    rx: float | None = None
    ry: float | None = None


@dataclass
class Circle(CommonAttrs):
    x: float = 0
    y: float = 0
    r: float = 0


@dataclass
class Line(CommonAttrs):
    x1: float = 0
    y1: float = 0
    x2: float = 0
    y2: float = 0


@dataclass
class Polygon(CommonAttrs):
    points: list[tuple[float, float]] = field(default_factory=list)


@dataclass
class Text(CommonAttrs):
    x: float = 0
    y: float = 0
    text: str = ""


@dataclass
class Formula(CommonAttrs):
    x: float = 0
    y: float = 0
    expr: str = ""


Element = Union[Rect, Circle, Line, Polygon, Text, Formula]


@dataclass
class ProblemIR:
    width: float
    height: float
    background: str = "#F6F6F6"
    problem_id: str = "custom_problem"
    problem_type: str = "custom"
    elements: list[Element] = field(default_factory=list)
