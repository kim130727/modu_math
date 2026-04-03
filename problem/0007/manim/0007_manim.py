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
    return {"가": 312, "ㄴ": 548, "ㄷ": 978, "큰": 1400}


def create_semantic_payload(data: dict) -> dict:
    problem_id = f"{int(data['id']):04d}"
    p = _point_positions()

    elements: list[dict] = [
        {"id": "instruction", "type": "text", "text": data["instruction"], "x": 20, "y": 76, "anchor": "start", "font_family": "Malgun Gothic", "font_size": 64, "fill": "#222222"},
        {"id": "base_line", "type": "line", "x1": p["가"], "y1": 249, "x2": p["큰"], "y2": 249, "stroke": "#2E2A2D", "stroke_width": 5},
    ]

    for name, x in p.items():
        elements.extend([
            {"id": f"tick_{name}", "type": "line", "x1": x, "y1": 218, "x2": x, "y2": 279, "stroke": "#2E2A2D", "stroke_width": 4},
            {"id": f"label_circle_{name}", "type": "circle", "cx": x, "cy": 316, "r": 22, "stroke": "#3A3336", "stroke_width": 3, "fill": "none"},
            {"id": f"label_{name}", "type": "text", "text": name, "x": x, "y": 327, "anchor": "middle", "font_family": "Malgun Gothic", "font_size": 34, "fill": "#222222"},
        ])

    elements.extend([
        {"id": "dist_ga_n", "type": "line", "x1": p["가"], "y1": 244, "x2": p["ㄴ"], "y2": 244, "stroke": "#0FA9F4", "stroke_width": 3, "dasharray": "4 8"},
        {"id": "dist_ga_n_text", "type": "text", "text": "176 cm", "x": (p["가"] + p["ㄴ"]) / 2, "y": 198, "anchor": "middle", "font_family": "Cambria", "font_size": 58, "fill": "#222222"},
        {"id": "dist_n_big", "type": "line", "x1": p["ㄴ"], "y1": 236, "x2": p["큰"], "y2": 236, "stroke": "#0FA9F4", "stroke_width": 3, "dasharray": "4 8"},
        {"id": "dist_n_big_text", "type": "text", "text": "646 cm", "x": (p["ㄴ"] + p["큰"]) / 2, "y": 192, "anchor": "middle", "font_family": "Cambria", "font_size": 58, "fill": "#222222"},
        {"id": "dist_n_d", "type": "line", "x1": p["ㄴ"], "y1": 307, "x2": p["ㄷ"], "y2": 307, "stroke": "#0FA9F4", "stroke_width": 3, "dasharray": "4 8"},
        {"id": "dist_n_d_text", "type": "text", "text": "325 cm", "x": (p["ㄴ"] + p["ㄷ"]) / 2, "y": 334, "anchor": "middle", "font_family": "Cambria", "font_size": 58, "fill": "#222222"},
        {"id": "answer_blank", "type": "rect", "x": 1230, "y": 24, "width": 170, "height": 56, "rx": 10, "stroke": "#69BEEA", "stroke_width": 4, "fill": "none", "semantic_role": "answer_blank", "answer_blank": True, "choice": {"index": 1, "value": str(data["answer_cm"])}}
    ])

    return {"meta": {"schema": "modu_math.semantic.v2", "problem_id": problem_id, "source": f"problem/{problem_id}/manim/{problem_id}_manim.py"}, "problem": data, "canvas": {"width": 1464, "height": 382, "background": "#F6F6F6"}, "elements": elements}


class DistanceOnLineProblem(Scene):
    def construct(self) -> None:
        semantic = create_semantic_payload(load_problem_data(Path(__file__)))
        validate_or_raise(semantic)
        render_manim_from_semantic(self, semantic)
        self.wait(2)


SceneClass = DistanceOnLineProblem

if __name__ == "__main__":
    run_cli(Path(__file__), create_semantic_payload)
