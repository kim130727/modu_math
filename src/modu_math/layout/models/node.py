from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

@dataclass
class LayoutNode:
    id: str
    type: str
    source_ref: str | None = None
    x: float = 0.0
    y: float = 0.0
    width: float | None = None
    height: float | None = None
    anchor: str | None = None
    rotation: float | None = None
    z_order: int = 0
    properties: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            "id": self.id,
            "type": self.type,
            "x": self.x,
            "y": self.y,
        }
        if self.source_ref:
            d["source_ref"] = self.source_ref
        if self.width is not None:
            d["width"] = self.width
        if self.height is not None:
            d["height"] = self.height
        if self.anchor is not None:
            d["anchor"] = self.anchor
        if self.rotation is not None:
            d["rotation"] = self.rotation
        if self.z_order != 0:
            d["z_order"] = self.z_order
        if self.properties:
            d["properties"] = self.properties
        return d

@dataclass
class TextNode(LayoutNode):
    type: str = "text"
    text: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        d = super().to_dict()
        if "properties" not in d:
            d["properties"] = {}
        d["properties"]["text"] = self.text
        return d

@dataclass
class ShapeNode(LayoutNode):
    type: str = "shape"
    shape_type: str = "rect" # rect, circle, path, line
    
    def to_dict(self) -> dict[str, Any]:
        d = super().to_dict()
        if "properties" not in d:
            d["properties"] = {}
        d["properties"]["shape_type"] = self.shape_type
        return d
