from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable


@dataclass
class Group:
    id: str
    children: list[object] = field(default_factory=list)
    semantic_role: str | None = None
    metadata: dict[str, object] = field(default_factory=dict)

    def add(self, child: object) -> "Group":
        self.children.append(child)
        return self

    def extend(self, children: Iterable[object]) -> "Group":
        self.children.extend(children)
        return self
