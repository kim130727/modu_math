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
    wrong = data["wrong"]

    elements: list[dict] = [
        {"id": "instruction", "type": "text", "text": data["instruction"], "x": 22, "y": 86, "anchor": "start", "font_family": "Malgun Gothic", "font_size": 66, "manim_font_size": 40, "fill": "#222222"},
                {"id": "left_panel", "type": "rect", "x": 347, "y": 212, "width": 585, "height": 435, "rx": 70, "stroke": "#CFC8BA", "stroke_width": 9, "fill": "none"},
        {"id": "right_panel", "type": "rect", "x": 1110, "y": 202, "width": 615, "height": 455, "rx": 70, "stroke": "#CFC8BA", "stroke_width": 9, "fill": "none"},
        {"id": "right_tab", "type": "rect", "x": 1261, "y": 176, "width": 400, "height": 100, "rx": 38, "stroke": "#000000", "stroke_width": 0, "fill": "#CE8D61"},
        {"id": "right_tab_text", "type": "text", "text": "바르게 계산하기", "x": 1440, "y": 225, "anchor": "middle", "font_family": "Malgun Gothic", "font_size": 35, "font_weight": "bold", "fill": "#FFFFFF"},
        {"id": "left_top", "type": "text", "text": f"{wrong['top']}", "x": 790, "y": 355, "anchor": "end", "font_family": "Cambria", "font_size": 60, "fill": "#222222"},
        {"id": "left_mid", "type": "text", "text": f"+{wrong['bottom']}", "x": 790, "y": 458, "anchor": "end", "font_family": "Cambria", "font_size": 60, "fill": "#222222"},
        {"id": "left_line", "type": "line", "x1": 468, "y1": 516, "x2": 808, "y2": 516, "stroke": "#333333", "stroke_width": 3},
        {"id": "left_result", "type": "text", "text": f"{wrong['shown_result']}", "x": 790, "y": 578, "anchor": "end", "font_family": "Cambria", "font_size": 60, "fill": "#222222"},
                {"id": "arrow_body", "type": "line", "x1": 1008, "y1": 432, "x2": 1070, "y2": 432, "stroke": "#9AAAB2", "stroke_width": 14},
        {"id": "arrow_head1", "type": "line", "x1": 1070, "y1": 432, "x2": 1040, "y2": 405, "stroke": "#9AAAB2", "stroke_width": 14},
        {"id": "arrow_head2", "type": "line", "x1": 1070, "y1": 432, "x2": 1040, "y2": 459, "stroke": "#9AAAB2", "stroke_width": 14},
    ]

    return {"meta": {"schema": "modu_math.semantic.v2", "problem_id": problem_id, "source": f"problem/{problem_id}/manim/{problem_id}_manim.py"}, "problem": data, "canvas": {"width": 1744, "height": 725, "background": "#F6F6F6"}, "elements": elements}


class FixAdditionProblem(Scene):
    def construct(self) -> None:
        semantic = create_semantic_payload(load_problem_data(Path(__file__)))
        validate_or_raise(semantic)
        render_manim_from_semantic(self, semantic)
        self.wait(2)


class SceneClass(FixAdditionProblem):
    pass


if __name__ == "__main__":
    run_cli(Path(__file__), create_semantic_payload)
