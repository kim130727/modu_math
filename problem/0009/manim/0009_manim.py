from __future__ import annotations

import sys
from pathlib import Path

from manim import Scene

sys.dont_write_bytecode = True


def _ensure_repo_root_on_path() -> None:
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / "problem").is_dir() and (parent / "README.md").exists():
            root = str(parent)
            if root not in sys.path:
                sys.path.insert(0, root)
            return
    raise RuntimeError("Repository root could not be resolved from current file path.")


_ensure_repo_root_on_path()

from problem.common.manim_renderer import render_manim_from_semantic
from problem.common.problem_cli import configure_manim_output_dirs, load_problem_data, run_cli, validate_or_raise

configure_manim_output_dirs(Path(__file__))


def _quadratic_points(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    bulge: float,
    steps: int,
) -> list[tuple[float, float]]:
    """Create points for a quadratic bezier curve using vertical bulge at midpoint."""
    cx = (x1 + x2) / 2
    cy = (y1 + y2) / 2 + bulge
    pts: list[tuple[float, float]] = []
    for i in range(steps + 1):
        t = i / steps
        mt = 1 - t
        x = mt * mt * x1 + 2 * mt * t * cx + t * t * x2
        y = mt * mt * y1 + 2 * mt * t * cy + t * t * y2
        pts.append((x, y))
    return pts


def _add_dashed_curve(
    elements: list[dict],
    curve_id: str,
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    bulge: float,
    stroke: str = "#17B2F5",
    stroke_width: int = 2,
    steps: int = 30,
    on_segments: int = 1,
    off_segments: int = 1,
) -> None:
    """Approximate a dashed arc with short line segments."""
    pts = _quadratic_points(x1, y1, x2, y2, bulge, steps)
    pattern = on_segments + off_segments
    for i in range(len(pts) - 1):
        if (i % pattern) >= on_segments:
            continue
        sx, sy = pts[i]
        ex, ey = pts[i + 1]
        elements.append(
            {
                "id": f"{curve_id}_seg_{i}",
                "type": "line",
                "x1": sx,
                "y1": sy,
                "x2": ex,
                "y2": ey,
                "stroke": stroke,
                "stroke_width": stroke_width,
                "semantic_role": "measurement_guide",
                "group": "guides",
                "figure_type": "curve_dash",
            }
        )


def create_semantic_payload(data: dict) -> dict:
    problem_id = f"{int(data['id']):04d}"

    lx, mx, rx = 208, 396, 818
    by = 168

    elements = [
        {"id": "num", "type": "text", "text": str(data["id"]), "x": 20, "y": 67, "anchor": "start", "font_family": "Malgun Gothic", "font_size": 54, "fill": "#6F3FA2"},
        {"id": "inst", "type": "text", "text": data["instruction"], "x": 89, "y": 67, "anchor": "start", "font_family": "Malgun Gothic", "font_size": 47, "fill": "#222222"},
        {"id": "line", "type": "line", "x1": lx, "y1": by, "x2": rx, "y2": by, "stroke": "#3A3539", "stroke_width": 3},
        {"id": "tick_l", "type": "line", "x1": lx, "y1": by - 15, "x2": lx, "y2": by + 15, "stroke": "#3A3539", "stroke_width": 3},
        {"id": "tick_m", "type": "line", "x1": mx, "y1": by - 15, "x2": mx, "y2": by + 15, "stroke": "#3A3539", "stroke_width": 3},
        {"id": "tick_r", "type": "line", "x1": rx, "y1": by - 15, "x2": rx, "y2": by + 15, "stroke": "#3A3539", "stroke_width": 3},
        {"id": "seg_1_text", "type": "text", "text": str(data["left_to_mid"]), "x": 304.69382, "y": 226.83633, "anchor": "middle", "font_family": "Cambria", "font_size": 40, "fill": "#222222"},
        {"id": "seg_2_text", "type": "text", "text": str(data["mid_to_right"]), "x": 607, "y": 225.48943, "anchor": "middle", "font_family": "Cambria", "font_size": 40, "fill": "#222222"},
        {"id": "total_blank", "type": "rect", "x": 455.63351, "y": 84.551292, "width": 96, "height": 46, "rx": 6, "stroke": "#69BEEA", "stroke_width": 3, "fill": "none", "semantic_role": "answer_blank", "answer_blank": True, "choice": {"index": 1, "value": str(data["total"])}}
    ]

    # Curved dotted guides to match the original worksheet style.
    _add_dashed_curve(elements, "seg_total", lx, by + 2, rx, by + 2, bulge=-64, steps=40)
    _add_dashed_curve(elements, "seg_1", lx, by + 2, mx, by + 2, bulge=36, steps=24)
    _add_dashed_curve(elements, "seg_2", mx, by + 2, rx, by + 2, bulge=34, steps=30)

    return {"meta": {"schema": "modu_math.semantic.v2", "problem_id": problem_id, "source": f"problem/{problem_id}/manim/{problem_id}_manim.py"}, "problem": data, "canvas": {"width": 860, "height": 247, "background": "#F6F6F6"}, "elements": elements}


class NumberLineBlankProblem(Scene):
    def construct(self) -> None:
        semantic = create_semantic_payload(load_problem_data(Path(__file__)))
        validate_or_raise(semantic)
        render_manim_from_semantic(self, semantic)
        self.wait(2)


SceneClass = NumberLineBlankProblem

if __name__ == "__main__":
    run_cli(Path(__file__), create_semantic_payload)
