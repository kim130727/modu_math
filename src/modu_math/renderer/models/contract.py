from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class RenderRefs:
    layout_node_id: str | None = None
    layout_slot_id: str | None = None
    layout_object_id: str | None = None
    layout_diagram_id: str | None = None

    def to_dict(self) -> dict[str, str]:
        data: dict[str, str] = {}
        if self.layout_node_id:
            data["layout_node_id"] = self.layout_node_id
        if self.layout_slot_id:
            data["layout_slot_id"] = self.layout_slot_id
        if self.layout_object_id:
            data["layout_object_id"] = self.layout_object_id
        if self.layout_diagram_id:
            data["layout_diagram_id"] = self.layout_diagram_id
        return data


@dataclass(frozen=True)
class RenderViewBox:
    width: float
    height: float
    background: str | None = None

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {"width": self.width, "height": self.height}
        if self.background:
            data["background"] = self.background
        return data


@dataclass(frozen=True)
class DrawElement:
    id: str
    type: str
    attributes: dict[str, Any] = field(default_factory=dict)
    source_ref: str | None = None
    refs: RenderRefs | None = None
    text: str | None = None
    elements: tuple["DrawElement", ...] = ()

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {
            "id": self.id,
            "type": self.type,
            "attributes": self.attributes,
        }
        if self.source_ref:
            data["source_ref"] = self.source_ref
        if self.refs:
            refs = self.refs.to_dict()
            if refs:
                data["refs"] = refs
        if self.text is not None:
            data["text"] = self.text
        if self.elements:
            data["elements"] = [child.to_dict() for child in self.elements]
        return data


@dataclass(frozen=True)
class RendererDocument:
    problem_id: str
    view_box: RenderViewBox
    elements: tuple[DrawElement, ...] = ()
    contract_version: str = "modu_math.renderer.v2"

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {
            "problem_id": self.problem_id,
            "view_box": self.view_box.to_dict(),
            "elements": [element.to_dict() for element in self.elements],
        }
        data["contract_version"] = self.contract_version
        return data

