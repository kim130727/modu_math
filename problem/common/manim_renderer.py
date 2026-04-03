from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from manim import Scene


def _ensure_src_on_path() -> None:
    current = Path(__file__).resolve()
    for parent in current.parents:
        src_dir = parent / "src"
        if src_dir.is_dir():
            src_path = str(src_dir)
            if src_path not in sys.path:
                sys.path.insert(0, src_path)
            return
    raise RuntimeError("Could not locate src directory for manim renderer bridge.")


_ensure_src_on_path()

from modu_math.renderers.manim_renderer import ManimRenderer


def render_manim_from_semantic(scene: Scene, semantic: dict) -> None:
    """
    Backward-compatible API.

    Existing problem scripts pass legacy semantic payloads (meta/problem/canvas/elements).
    This bridge converts them to v3 render shape and delegates to src renderer.
    """
    semantic_v3 = _to_v3_if_needed(semantic)
    renderer = ManimRenderer()
    renderer.render_scene(scene, semantic_v3)


def _to_v3_if_needed(semantic: dict[str, Any]) -> dict[str, Any]:
    if isinstance(semantic, dict) and "render" in semantic and "answer" in semantic:
        return semantic

    if not isinstance(semantic, dict):
        return {
            "schema_version": "modu_math.semantic.v3",
            "problem_id": "unknown",
            "problem_type": "unknown",
            "metadata": {},
            "domain": {},
            "render": {"canvas": {"width": 0, "height": 0, "background": "#FFFFFF"}, "elements": []},
            "answer": {"blanks": [], "choices": [], "answer_key": []},
        }

    meta = semantic.get("meta", {}) if isinstance(semantic.get("meta", {}), dict) else {}
    problem = semantic.get("problem", {}) if isinstance(semantic.get("problem", {}), dict) else {}
    canvas = semantic.get("canvas", {}) if isinstance(semantic.get("canvas", {}), dict) else {}
    elements = semantic.get("elements", []) if isinstance(semantic.get("elements", []), list) else []

    return {
        "schema_version": "modu_math.semantic.v3",
        "problem_id": str(meta.get("problem_id", problem.get("id", "unknown"))),
        "problem_type": str(problem.get("type", "unknown")),
        "metadata": {
            "source_file": meta.get("source", "legacy_manim_bridge"),
            "language": "ko-KR",
            "grade_band": "unknown",
        },
        "domain": {},
        "render": {
            "canvas": {
                "width": canvas.get("width", 0),
                "height": canvas.get("height", 0),
                "background": canvas.get("background", "#FFFFFF"),
            },
            "groups": [],
            "elements": elements,
        },
        "answer": {"blanks": [], "choices": [], "answer_key": []},
    }
