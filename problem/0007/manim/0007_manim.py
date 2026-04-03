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


def _point_positions() -> dict[str, float]:
    return {"ㄱ": 312, "ㄴ": 548, "ㄷ": 978, "ㄹ": 1400}


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
    stroke: str = "#0FA9F4",
    stroke_width: int = 3,
    steps: int = 28,
    on_segments: int = 1,
    off_segments: int = 1,
) -> None:
    """Approximate a dashed arc with many short line segments."""
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
    p = _point_positions()

    elements: list[dict] = [
        {
            "id": "instruction",
            "type": "text",
            "text": data["instruction"],
            "x": 20,
            "y": 76,
            "anchor": "start",
            "font_family": "Malgun Gothic",
            "font_size": 64,
            "fill": "#222222",
            "semantic_role": "instruction",
            "group": "header",
        },
        {
            "id": "base_line",
            "type": "line",
            "x1": p["ㄱ"],
            "y1": 249,
            "x2": p["ㄹ"],
            "y2": 249,
            "stroke": "#2E2A2D",
            "stroke_width": 5,
            "semantic_role": "number_line",
            "group": "line",
        },
    ]

    for name, x in p.items():
        elements.extend(
            [
                {
                    "id": f"tick_{name}",
                    "type": "line",
                    "x1": x,
                    "y1": 218,
                    "x2": x,
                    "y2": 279,
                    "stroke": "#2E2A2D",
                    "stroke_width": 4,
                    "semantic_role": "point_tick",
                    "group": "line",
                },
                {
                    "id": f"label_circle_{name}",
                    "type": "circle",
                    "cx": x,
                    "cy": 316,
                    "r": 22,
                    "stroke": "#3A3336",
                    "stroke_width": 3,
                    "fill": "none",
                    "semantic_role": "point_label",
                    "group": "line",
                },
                {
                    "id": f"label_{name}",
                    "type": "text",
                    "text": name,
                    "x": x,
                    "y": 327,
                    "anchor": "middle",
                    "font_family": "Malgun Gothic",
                    "font_size": 34,
                    "fill": "#222222",
                    "semantic_role": "point_name",
                    "group": "line",
                },
            ]
        )

    # Curved dashed guides (input image uses arcs, not straight lines).
    _add_dashed_curve(elements, "dist_ga_n", p["ㄱ"], 244, p["ㄴ"], 244, bulge=-72)
    _add_dashed_curve(elements, "dist_n_big", p["ㄴ"], 236, p["ㄹ"], 236, bulge=-88)
    _add_dashed_curve(elements, "dist_n_d", p["ㄴ"], 307, p["ㄷ"], 307, bulge=70)

    elements.extend(
        [
            {
                "id": "dist_ga_n_text",
                "type": "text",
                "text": "176 cm",
                "x": (p["ㄱ"] + p["ㄴ"]) / 2,
                "y": 198,
                "anchor": "middle",
                "font_family": "Cambria",
                "font_size": 58,
                "fill": "#222222",
                "semantic_role": "distance_label",
                "group": "guides",
            },
            {
                "id": "dist_n_big_text",
                "type": "text",
                "text": "646 cm",
                "x": (p["ㄴ"] + p["ㄹ"]) / 2,
                "y": 192,
                "anchor": "middle",
                "font_family": "Cambria",
                "font_size": 58,
                "fill": "#222222",
                "semantic_role": "distance_label",
                "group": "guides",
            },
            {
                "id": "dist_n_d_text",
                "type": "text",
                "text": "325 cm",
                "x": (p["ㄴ"] + p["ㄷ"]) / 2,
                "y": 334,
                "anchor": "middle",
                "font_family": "Cambria",
                "font_size": 58,
                "fill": "#222222",
                "semantic_role": "distance_label",
                "group": "guides",
            },
        ]
    )

    return {
        "meta": {
            "schema": "modu_math.semantic.v2",
            "problem_id": problem_id,
            "source": f"problem/{problem_id}/manim/{problem_id}_manim.py",
        },
        "problem": data,
        "canvas": {"width": 1464, "height": 382, "background": "#F6F6F6"},
        "elements": elements,
    }


class DistanceOnLineProblem(Scene):
    def construct(self) -> None:
        semantic = create_semantic_payload(load_problem_data(Path(__file__)))
        validate_or_raise(semantic)
        render_manim_from_semantic(self, semantic)
        self.wait(2)


class SceneClass(DistanceOnLineProblem):
    pass


if __name__ == "__main__":
    run_cli(Path(__file__), create_semantic_payload)
