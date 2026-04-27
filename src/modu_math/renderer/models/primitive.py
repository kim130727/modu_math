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

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "RenderElement":
        element_type = str(data.get("type", ""))
        element_cls: type[RenderElement]
        if element_type == "rect":
            element_cls = RenderRect
        elif element_type == "circle":
            element_cls = RenderCircle
        elif element_type == "line":
            element_cls = RenderLine
        elif element_type == "polygon":
            element_cls = RenderPolygon
        elif element_type == "text":
            element_cls = RenderText
        elif element_type == "group":
            element_cls = RenderGroup
        else:
            element_cls = RenderElement
        return element_cls._from_dict_impl(data)

    @classmethod
    def _from_dict_impl(cls, data: dict[str, Any]) -> "RenderElement":
        return cls(
            id=str(data.get("id", "")),
            type=str(data.get("type", "")),
            attributes=dict(data.get("attributes", {})),
        )

@dataclass
class RenderRect(RenderElement):
    type: str = "rect"

@dataclass
class RenderCircle(RenderElement):
    type: str = "circle"

@dataclass
class RenderLine(RenderElement):
    type: str = "line"

@dataclass
class RenderPolygon(RenderElement):
    type: str = "polygon"

@dataclass
class RenderText(RenderElement):
    type: str = "text"
    text: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        d = super().to_dict()
        d["text"] = self.text
        return d

    @classmethod
    def _from_dict_impl(cls, data: dict[str, Any]) -> "RenderText":
        return cls(
            id=str(data.get("id", "")),
            type=str(data.get("type", "text")),
            attributes=dict(data.get("attributes", {})),
            text=str(data.get("text", "")),
        )

@dataclass
class RenderGroup(RenderElement):
    type: str = "group"
    elements: list[RenderElement] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        d = super().to_dict()
        d["elements"] = [element.to_dict() for element in self.elements]
        return d

    @classmethod
    def _from_dict_impl(cls, data: dict[str, Any]) -> "RenderGroup":
        raw_children = data.get("elements", [])
        children: list[RenderElement] = []
        if isinstance(raw_children, list):
            for child in raw_children:
                if isinstance(child, dict):
                    children.append(RenderElement.from_dict(child))
        return cls(
            id=str(data.get("id", "")),
            type=str(data.get("type", "group")),
            attributes=dict(data.get("attributes", {})),
            elements=children,
        )

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

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "RendererAST":
        view_box_data = dict(data.get("view_box", {}))
        view_box = RenderViewBox(
            width=float(view_box_data.get("width", 0)),
            height=float(view_box_data.get("height", 0)),
            background=view_box_data.get("background"),
        )

        raw_elements = data.get("elements", [])
        elements: list[RenderElement] = []
        if isinstance(raw_elements, list):
            for element in raw_elements:
                if isinstance(element, dict):
                    elements.append(RenderElement.from_dict(element))

        return cls(
            problem_id=str(data.get("problem_id", "")),
            view_box=view_box,
            elements=elements,
        )
