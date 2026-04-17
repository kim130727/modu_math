from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from .node import LayoutNode

@dataclass
class LayoutGroup(LayoutNode):
    type: str = "group"
    children: list[LayoutNode] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        d = super().to_dict()
        d["children"] = [child.to_dict() for child in self.children]
        return d
