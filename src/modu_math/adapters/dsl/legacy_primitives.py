from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

from ...layout.models.node import LayoutNode, ShapeNode, TextNode

@dataclass
class Element:
    id: str
    semantic_role: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    z_order: int = 0
    
    # Generic style defaults
    fill: str | None = "none"
    stroke: str | None = "#000000"
    stroke_width: float | None = 1.0
    opacity: float | None = None
    transform: str | None = None
    font_family: str | None = "sans-serif"
    font_size: float | None = 16.0
    font_weight: str | None = None

    def to_layout_node(self) -> LayoutNode:
        raise NotImplementedError

    def _base_props(self) -> dict[str, Any]:
        props: dict[str, Any] = {}
        if self.semantic_role:
            props["semantic_role"] = self.semantic_role
        if self.fill:
            props["fill"] = self.fill
        if self.stroke:
            props["stroke"] = self.stroke
        if self.stroke_width is not None:
            props["stroke_width"] = self.stroke_width
        if self.opacity is not None:
            props["opacity"] = self.opacity
        if self.transform is not None:
            props["transform"] = self.transform
        return props

@dataclass
class Rect(Element):
    x: float = 0.0
    y: float = 0.0
    width: float = 0.0
    height: float = 0.0
    rx: float | None = None
    ry: float | None = None

    def to_layout_node(self) -> ShapeNode:
        props = self._base_props()
        if self.rx is not None:
            props["rx"] = self.rx
        if self.ry is not None:
            props["ry"] = self.ry
        return ShapeNode(
            id=self.id,
            shape_type="rect",
            x=self.x,
            y=self.y,
            width=self.width,
            height=self.height,
            properties=props,
            z_order=self.z_order,
        )

@dataclass
class Circle(Element):
    cx: float = 0.0
    cy: float = 0.0
    r: float = 0.0

    def to_layout_node(self) -> ShapeNode:
        props = self._base_props()
        props["r"] = self.r
        return ShapeNode(
            id=self.id,
            shape_type="circle",
            x=self.cx,
            y=self.cy,
            properties=props,
            z_order=self.z_order,
        )

@dataclass
class Line(Element):
    x1: float = 0.0
    y1: float = 0.0
    x2: float = 0.0
    y2: float = 0.0

    def to_layout_node(self) -> ShapeNode:
        props = self._base_props()
        props["x1"] = self.x1
        props["y1"] = self.y1
        props["x2"] = self.x2
        props["y2"] = self.y2
        return ShapeNode(
            id=self.id,
            shape_type="line",
            x=min(self.x1, self.x2),
            y=min(self.y1, self.y2),
            properties=props,
            z_order=self.z_order,
        )

@dataclass
class Polygon(Element):
    points: list[tuple[float, float]] = field(default_factory=list)

    def to_layout_node(self) -> ShapeNode:
        props = self._base_props()
        props["points"] = self.points
        x = min(p[0] for p in self.points) if self.points else 0.0
        y = min(p[1] for p in self.points) if self.points else 0.0
        return ShapeNode(
            id=self.id,
            shape_type="polygon",
            x=x,
            y=y,
            properties=props,
            z_order=self.z_order,
        )

@dataclass
class Text(Element):
    x: float = 0.0
    y: float = 0.0
    text: str = ""
    anchor: str | None = "middle"
    fill: str | None = "#000000"
    stroke: str | None = "none"
    font_style: str | None = None

    def to_layout_node(self) -> TextNode:
        props = self._base_props()
        if self.font_family:
            props["font_family"] = self.font_family
        if self.font_size is not None:
            props["font_size"] = self.font_size
        if self.font_weight:
            props["font_weight"] = self.font_weight
        if self.font_style:
            props["font_style"] = self.font_style
            
        return TextNode(
            id=self.id,
            text=self.text,
            x=self.x,
            y=self.y,
            anchor=self.anchor,
            properties=props,
            z_order=self.z_order,
        )

@dataclass
class Formula(Text):
    expr: str = ""
    font_family: str | None = "serif"
    
    def __post_init__(self):
        # Backward compatibility for text alias
        if not self.expr and hasattr(self, "text") and self.text:
            self.expr = self.text
            
    def to_layout_node(self) -> TextNode:
        # Override text with expr and mark as formula
        self.text = self.expr
        node = super().to_layout_node()
        node.properties["is_formula"] = True
        return node
