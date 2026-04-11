from __future__ import annotations

from pathlib import Path

from .problem import Problem


def export_all(problem: Problem, out_prefix: str | Path, *, validate: bool = True) -> None:
    """Export semantic JSON, layout JSON, and SVG files in one call."""
    problem.save(out_prefix, validate=validate)
