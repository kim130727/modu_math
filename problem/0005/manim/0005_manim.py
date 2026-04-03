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


def create_semantic_payload(data: dict) -> dict:
    problem_id = f"{int(data['id']):04d}"
    left_expr, right_expr = data["expressions"]
    correct_index = int(data["correct_index"])

    elements: list[dict] = [
        {"id": "instruction", "type": "text", "text": data["instruction"], "x": 44, "y": 106, "anchor": "start", "font_family": "Malgun Gothic", "font_size": 72, "fill": "#222222"},
        {"id": "circle_marker", "type": "circle", "cx": 695, "cy": 102, "r": 28, "stroke": "#E01392", "stroke_width": 6, "fill": "none"},
        {"id": "left_box", "type": "rect", "x": 320, "y": 180, "width": 590, "height": 210, "rx": 75, "stroke": "none", "stroke_width": 0, "fill": "#D0CABB", "semantic_role": "choice", "choice": {"index": 1, "value": left_expr, "is_correct": correct_index == 0}},
        {"id": "right_box", "type": "rect", "x": 1200, "y": 180, "width": 590, "height": 210, "rx": 75, "stroke": "none", "stroke_width": 0, "fill": "#D0CABB", "semantic_role": "choice", "choice": {"index": 2, "value": right_expr, "is_correct": correct_index == 1}},
        {"id": "left_expr", "type": "text", "text": left_expr, "x": 615, "y": 294, "anchor": "middle", "font_family": "Cambria", "font_size": 74, "fill": "#222222"},
        {"id": "right_expr", "type": "text", "text": right_expr, "x": 1495, "y": 294, "anchor": "middle", "font_family": "Cambria", "font_size": 74, "fill": "#222222"},
        {"id": "left_paren_l", "type": "text", "text": "(", "x": 500, "y": 478, "anchor": "middle", "font_family": "Cambria", "font_size": 92, "fill": "#222222"},
        {"id": "left_paren_r", "type": "text", "text": ")", "x": 735, "y": 478, "anchor": "middle", "font_family": "Cambria", "font_size": 92, "fill": "#222222"},
        {"id": "right_paren_l", "type": "text", "text": "(", "x": 1380, "y": 478, "anchor": "middle", "font_family": "Cambria", "font_size": 92, "fill": "#222222"},
        {"id": "right_paren_r", "type": "text", "text": ")", "x": 1620, "y": 478, "anchor": "middle", "font_family": "Cambria", "font_size": 92, "fill": "#222222"},
    ]

    return {"meta": {"schema": "modu_math.semantic.v2", "problem_id": problem_id, "source": f"problem/{problem_id}/manim/{problem_id}_manim.py"}, "problem": data, "canvas": {"width": 1852, "height": 554, "background": "#F6F6F6"}, "elements": elements}


class CompareSumsProblem(Scene):
    def construct(self) -> None:
        semantic = create_semantic_payload(load_problem_data(Path(__file__)))
        validate_or_raise(semantic)
        render_manim_from_semantic(self, semantic)
        self.wait(2)


SceneClass = CompareSumsProblem

if __name__ == "__main__":
    run_cli(Path(__file__), create_semantic_payload)
