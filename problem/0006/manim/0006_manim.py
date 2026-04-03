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
        {"id": "instruction", "type": "text", "text": data["instruction"], "x": 22, "y": 86, "anchor": "start", "font_family": "Malgun Gothic", "font_size": 66, "fill": "#222222"},
        {"id": "marker_circle", "type": "circle", "cx": 526, "cy": 77, "r": 26, "stroke": "#E01392", "stroke_width": 6, "fill": "none"},
        {"id": "left_panel", "type": "rect", "x": 347, "y": 212, "width": 585, "height": 435, "rx": 70, "stroke": "#CFC8BA", "stroke_width": 9, "fill": "none"},
        {"id": "right_panel", "type": "rect", "x": 1140, "y": 212, "width": 585, "height": 435, "rx": 70, "stroke": "#CFC8BA", "stroke_width": 9, "fill": "none"},
        {"id": "right_tab", "type": "rect", "x": 1261, "y": 176, "width": 345, "height": 74, "rx": 38, "stroke": "none", "stroke_width": 0, "fill": "#CE8D61"},
        {"id": "right_tab_text", "type": "text", "text": "바르게 계산하기", "x": 1434, "y": 225, "anchor": "middle", "font_family": "Malgun Gothic", "font_size": 52, "font_weight": "bold", "fill": "#FFFFFF"},
        {"id": "left_top", "type": "text", "text": f"{wrong['top']:>4}", "x": 682, "y": 355, "anchor": "middle", "font_family": "Cambria", "font_size": 74, "fill": "#222222"},
        {"id": "left_mid", "type": "text", "text": f"+{wrong['bottom']:>3}", "x": 682, "y": 458, "anchor": "middle", "font_family": "Cambria", "font_size": 74, "fill": "#222222"},
        {"id": "left_line", "type": "line", "x1": 468, "y1": 516, "x2": 808, "y2": 516, "stroke": "#333333", "stroke_width": 3},
        {"id": "left_result", "type": "text", "text": f"{wrong['shown_result']:>4}", "x": 682, "y": 578, "anchor": "middle", "font_family": "Cambria", "font_size": 74, "fill": "#222222"},
        {"id": "wrong_place_circle", "type": "circle", "cx": 620, "cy": 578, "r": 30, "stroke": "#E01392", "stroke_width": 5, "fill": "none", "semantic_role": "wrong_spot"},
        {"id": "arrow_body", "type": "line", "x1": 1008, "y1": 432, "x2": 1070, "y2": 432, "stroke": "#9AAAB2", "stroke_width": 14},
        {"id": "arrow_head1", "type": "line", "x1": 1070, "y1": 432, "x2": 1040, "y2": 405, "stroke": "#9AAAB2", "stroke_width": 14},
        {"id": "arrow_head2", "type": "line", "x1": 1070, "y1": 432, "x2": 1040, "y2": 459, "stroke": "#9AAAB2", "stroke_width": 14},
        {"id": "correct_blank", "type": "rect", "x": 1320, "y": 465, "width": 220, "height": 95, "rx": 10, "stroke": "#69BEEA", "stroke_width": 4, "fill": "none", "semantic_role": "answer_blank", "answer_blank": True, "choice": {"index": 1, "value": str(data["correct_result"])}}
    ]

    return {"meta": {"schema": "modu_math.semantic.v2", "problem_id": problem_id, "source": f"problem/{problem_id}/manim/{problem_id}_manim.py"}, "problem": data, "canvas": {"width": 1744, "height": 725, "background": "#F6F6F6"}, "elements": elements}


class FixAdditionProblem(Scene):
    def construct(self) -> None:
        semantic = create_semantic_payload(load_problem_data(Path(__file__)))
        validate_or_raise(semantic)
        render_manim_from_semantic(self, semantic)
        self.wait(2)


SceneClass = FixAdditionProblem

if __name__ == "__main__":
    run_cli(Path(__file__), create_semantic_payload)
