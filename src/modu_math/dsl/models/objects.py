from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class ShapeObject:
    id: str
    object_type: str
    style_role: str = "default"


@dataclass(frozen=True)
class Cube(ShapeObject):
    edge_label_mode: Literal["none", "auto", "custom"] = "none"
    perspective: Literal["isometric", "cabinet"] = "isometric"
    object_type: str = "cube"


@dataclass(frozen=True)
class Triangle(ShapeObject):
    variant: Literal["scalene", "isosceles", "equilateral", "right"] = "scalene"
    object_type: str = "triangle"


@dataclass(frozen=True)
class Circle(ShapeObject):
    mark_center: bool = False
    object_type: str = "circle"


@dataclass(frozen=True)
class Grid(ShapeObject):
    rows: int = 1
    cols: int = 1
    object_type: str = "grid"


@dataclass(frozen=True)
class Arrow(ShapeObject):
    direction: Literal["up", "right", "down", "left"] = "right"
    object_type: str = "arrow"


@dataclass(frozen=True)
class FractionAreaModel(ShapeObject):
    partitions: int = 2
    shaded: int = 1
    orientation: Literal["horizontal", "vertical"] = "horizontal"
    object_type: str = "fraction_area_model"
