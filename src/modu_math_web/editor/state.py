from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class PanState:
    x: float = 0.0
    y: float = 0.0


@dataclass
class ArtifactsState:
    semantic: dict[str, Any] | None = None
    solvable: dict[str, Any] | None = None
    layout: dict[str, Any] | None = None
    renderer: dict[str, Any] | None = None
    svg: str | None = None


@dataclass
class EditorState:
    problem_id: str
    selected_slot_id: str | None = None
    zoom: float = 1.0
    pan: PanState = field(default_factory=PanState)
    artifacts: ArtifactsState = field(default_factory=ArtifactsState)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
