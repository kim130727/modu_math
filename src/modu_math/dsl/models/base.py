from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

ConstraintType = Literal[
    "align",
    "equal_size",
    "inside",
    "connect",
    "distribute",
]

RegionFlow = Literal["vertical", "horizontal", "absolute", "grid"]


@dataclass(frozen=True)
class Canvas:
    width: int
    height: int
    coordinate_mode: Literal["logical", "absolute"] = "logical"


@dataclass(frozen=True)
class SlotBase:
    id: str
    kind: str
    prompt: str | None = None


@dataclass(frozen=True)
class TextSlot(SlotBase):
    text: str = ""
    style_role: str = "body"
    x: float | None = None
    y: float | None = None
    font_size: int | None = None
    font_family: str | None = None
    anchor: str | None = None
    fill: str | None = None
    semantic_role: str | None = None
    kind: str = "text"


@dataclass(frozen=True)
class ChoiceSlot(SlotBase):
    choices: tuple[str, ...] = ()
    answer_key: tuple[str, ...] = ()
    multiple_select: bool = False
    kind: str = "choice"


@dataclass(frozen=True)
class BlankSlot(SlotBase):
    answer_key: str | None = None
    placeholder: str = ""
    kind: str = "blank"


@dataclass(frozen=True)
class LabelSlot(SlotBase):
    text: str = ""
    target_object_id: str = ""
    target_anchor: Literal["top", "right", "bottom", "left", "center"] = "center"
    kind: str = "label"


@dataclass(frozen=True)
class RectSlot(SlotBase):
    x: float = 0.0
    y: float = 0.0
    width: float = 0.0
    height: float = 0.0
    stroke: str | None = None
    stroke_width: float | None = None
    rx: float | None = None
    ry: float | None = None
    fill: str | None = None
    semantic_role: str | None = None
    kind: str = "rect"


@dataclass(frozen=True)
class LineSlot(SlotBase):
    x1: float = 0.0
    y1: float = 0.0
    x2: float = 0.0
    y2: float = 0.0
    stroke: str | None = None
    stroke_width: float | None = None
    stroke_dasharray: str | None = None
    semantic_role: str | None = None
    kind: str = "line"


@dataclass(frozen=True)
class CircleSlot(SlotBase):
    cx: float = 0.0
    cy: float = 0.0
    r: float = 0.0
    stroke: str | None = None
    stroke_width: float | None = None
    fill: str | None = None
    semantic_role: str | None = None
    kind: str = "circle"


@dataclass(frozen=True)
class PolygonSlot(SlotBase):
    points: tuple[tuple[float, float], ...] = ()
    x: float = 0.0
    y: float = 0.0
    stroke: str | None = None
    stroke_width: float | None = None
    fill: str | None = None
    semantic_role: str | None = None
    kind: str = "polygon"


@dataclass(frozen=True)
class PathSlot(SlotBase):
    d: str = ""
    stroke: str | None = None
    stroke_width: float | None = None
    stroke_dasharray: str | None = None
    fill: str | None = None
    semantic_role: str | None = None
    kind: str = "path"


@dataclass(frozen=True)
class Region:
    id: str
    role: Literal["stem", "diagram", "choices", "answer", "note", "custom"]
    flow: RegionFlow = "vertical"
    slot_ids: tuple[str, ...] = ()


@dataclass(frozen=True)
class Group:
    id: str
    member_ids: tuple[str, ...] = ()
    role: Literal["question_block", "diagram_block", "answer_block", "custom"] = "custom"


@dataclass(frozen=True)
class Constraint:
    id: str
    type: ConstraintType
    target_ids: tuple[str, ...] = ()
    params: dict[str, str] = field(default_factory=dict)
