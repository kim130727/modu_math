from __future__ import annotations

import sys
from pathlib import Path


def _ensure_src_on_path() -> None:
    current = Path(__file__).resolve()
    for parent in current.parents:
        src_dir = parent / "src"
        if src_dir.is_dir():
            src_path = str(src_dir)
            if src_path not in sys.path:
                sys.path.insert(0, src_path)
            return
    raise RuntimeError("Could not locate src directory for paths bridge.")


_ensure_src_on_path()

from modu_math.core.paths import (
    baseline_dir_path,
    find_problem_dir,
    problem_input_json_path,
    semantic_json_path,
    semantic_svg_path,
)

__all__ = [
    "find_problem_dir",
    "semantic_json_path",
    "semantic_svg_path",
    "problem_input_json_path",
    "baseline_dir_path",
]