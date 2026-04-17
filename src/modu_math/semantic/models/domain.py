from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

# -- Objects --

@dataclass
class DomainObject:
    id: str
    type: str
    properties: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type,
            "properties": self.properties,
        }

@dataclass
class Point(DomainObject):
    type: str = "point"

@dataclass
class Line(DomainObject):
    type: str = "line"
    # p1, p2 are ids of Point objects
    p1: str | None = None
    p2: str | None = None

    def to_dict(self) -> dict[str, Any]:
        d = super().to_dict()
        if self.p1 and self.p2:
            d["properties"]["endpoints"] = [self.p1, self.p2]
        return d

@dataclass
class Angle(DomainObject):
    type: str = "angle"
    # p1, vertex, p2 are ids of Point objects
    p1: str | None = None
    vertex: str | None = None
    p2: str | None = None

    def to_dict(self) -> dict[str, Any]:
        d = super().to_dict()
        if self.p1 and self.vertex and self.p2:
            d["properties"]["points"] = [self.p1, self.vertex, self.p2]
        return d

@dataclass
class Circle(DomainObject):
    type: str = "circle"
    center: str | None = None

    def to_dict(self) -> dict[str, Any]:
        d = super().to_dict()
        if self.center:
            d["properties"]["center"] = self.center
        return d

# -- Relations --

@dataclass
class DomainRelation:
    type: str
    subjects: list[str] = field(default_factory=list)
    value: Any | None = None

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            "type": self.type,
            "subjects": self.subjects,
        }
        if self.value is not None:
            d["value"] = self.value
        return d

def create_relation(type: str, subjects: list[str], value: Any | None = None) -> DomainRelation:
    return DomainRelation(type=type, subjects=subjects, value=value)
