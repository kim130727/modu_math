from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

@dataclass
class LayoutCanvas:
    width: float
    height: float
    background: str | None = None

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            "width": self.width,
            "height": self.height,
        }
        if self.background:
            d["background"] = self.background
        return d


