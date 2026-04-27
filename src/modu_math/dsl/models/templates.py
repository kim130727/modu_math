from __future__ import annotations

from dataclasses import dataclass

from .base import BlankSlot, Canvas, ChoiceSlot, CircleSlot, Constraint, Group, LabelSlot, LineSlot, PathSlot, PolygonSlot, RectSlot, Region, TextSlot
from .objects import ShapeObject

AuthoringSlot = TextSlot | ChoiceSlot | BlankSlot | LabelSlot | RectSlot | LineSlot | CircleSlot | PolygonSlot | PathSlot


@dataclass(frozen=True)
class DiagramTemplate:
    id: str
    objects: tuple[ShapeObject, ...] = ()
    label_slots: tuple[LabelSlot, ...] = ()
    constraints: tuple[Constraint, ...] = ()


@dataclass(frozen=True)
class ProblemTemplate:
    id: str
    title: str
    canvas: Canvas
    regions: tuple[Region, ...]
    slots: tuple[AuthoringSlot, ...]
    diagrams: tuple[DiagramTemplate, ...] = ()
    groups: tuple[Group, ...] = ()
    constraints: tuple[Constraint, ...] = ()
    tags: tuple[str, ...] = ()
