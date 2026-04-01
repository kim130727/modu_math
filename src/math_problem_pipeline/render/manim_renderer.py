"""Manim renderer entrypoints."""

from __future__ import annotations

import shutil
from pathlib import Path

from math_problem_pipeline.models.semantic_models import SemanticProblem
from math_problem_pipeline.models.render_models import StyleHint
from math_problem_pipeline.render.scene_factory import build_scene_mobjects
from math_problem_pipeline.utils.io import ensure_dir
from math_problem_pipeline.utils.logging_utils import setup_logger

logger = setup_logger(__name__)

try:
    from manim import Scene, config

    MANIM_AVAILABLE = True
except Exception:  # pragma: no cover
    MANIM_AVAILABLE = False


def render_problem_to_png(problem: SemanticProblem, output_png: Path, media_root: Path) -> dict:
    """Render a single semantic problem into static PNG using Manim.

    Returns metadata for debug reporting.
    """
    ensure_dir(output_png.parent)

    if not MANIM_AVAILABLE:
        logger.warning("Manim is not available. Rendering skipped: %s", problem.problem_id)
        return {
            "problem_id": problem.problem_id,
            "rendered": False,
            "reason": "manim_not_available",
            "used_fields": ["question_text", "type", "render_hint"],
        }

    scene_name = f"Scene_{problem.problem_id.replace('-', '_')}"
    output_dir = ensure_dir(media_root / scene_name)

    style = StyleHint()
    mobjects = build_scene_mobjects(problem, style)

    class ProblemScene(Scene):
        def construct(self):
            for mob in mobjects:
                self.add(mob)

    config.media_dir = str(output_dir)
    config.pixel_width = 1280
    config.pixel_height = 720
    config.frame_rate = 1
    config.write_to_movie = False
    config.save_last_frame = True

    scene = ProblemScene()
    scene.render()

    png_files = sorted(output_dir.rglob("*.png"), key=lambda p: p.stat().st_mtime)
    if not png_files:
        return {
            "problem_id": problem.problem_id,
            "rendered": False,
            "reason": "png_not_generated",
            "used_fields": ["question_text", "type", "render_hint"],
        }

    shutil.copy2(png_files[-1], output_png)
    return {
        "problem_id": problem.problem_id,
        "rendered": True,
        "output_png": str(output_png),
        "used_fields": ["question_text", "type", "render_hint"],
    }
