from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

@dataclass
class RenderViewBox:
    width: float
    height: float
    background: str | None = None
    
    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {"width": self.width, "height": self.height}
        if self.background:
            d["background"] = self.background
        return d

@dataclass
class RenderElement:
    id: str
    type: str
    attributes: dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type,
            "attributes": self.attributes
        }

@dataclass
class RenderText(RenderElement):
    type: str = "text"
    text: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        d = super().to_dict()
        d["text"] = self.text
        return d

@dataclass
class RendererAST:
    problem_id: str
    view_box: RenderViewBox
    elements: list[RenderElement] = field(default_factory=list)
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "problem_id": self.problem_id,
            "view_box": self.view_box.to_dict(),
            "elements": [e.to_dict() for e in self.elements]
        }
