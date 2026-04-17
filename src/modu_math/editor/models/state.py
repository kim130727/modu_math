from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

@dataclass
class EditorPan:
    x: float = 0.0
    y: float = 0.0
    
    def to_dict(self) -> dict[str, float]:
        return {"x": self.x, "y": self.y}

@dataclass
class EditorState:
    """Represents the ephemeral visual state of the layout editor."""
    selection: list[str] = field(default_factory=list)
    zoom: float = 1.0
    pan: EditorPan = field(default_factory=EditorPan)
    snap: bool = True

    def to_dict(self) -> dict[str, Any]:
        return {
            "selection": self.selection,
            "zoom": self.zoom,
            "pan": self.pan.to_dict(),
            "snap": self.snap,
        }
