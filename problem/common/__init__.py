"""Backward-compatible common utilities for problem-level pipelines.

This package now re-exports bridge functions that delegate to the
`src/modu_math` implementation, so legacy scripts can keep imports stable
while new code can migrate to src-first modules.
"""

from __future__ import annotations

from .paths import (
    baseline_dir_path,
    find_problem_dir,
    problem_input_json_path,
    semantic_json_path,
    semantic_svg_path,
)
from .svg_renderer import render_svg_from_semantic
from .validator import validate_logic, validate_semantic, validate_structure

# `manim` may be absent in some environments (e.g. schema-only CI jobs).
# Keep import optional so importing `problem.common` remains safe.
try:
    from .manim_renderer import render_manim_from_semantic
except Exception:  # pragma: no cover - defensive fallback for optional runtime dep
    render_manim_from_semantic = None

__all__ = [
    "find_problem_dir",
    "semantic_json_path",
    "semantic_svg_path",
    "problem_input_json_path",
    "baseline_dir_path",
    "render_svg_from_semantic",
    "render_manim_from_semantic",
    "validate_semantic",
    "validate_structure",
    "validate_logic",
]