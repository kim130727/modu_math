from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class BaseRenderer(ABC):
    @abstractmethod
    def render_to_file(self, semantic: dict[str, Any], out_path: Path) -> Path:
        raise NotImplementedError
