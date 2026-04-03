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
    rows = data["rows"]

    elements: list[dict] = [
        {"id": "inst", "type": "text", "text": data["instruction"], "x": 28, "y": 98, "anchor": "start", "font_family": "Malgun Gothic", "font_size": 72, "fill": "#222222"},
        {"id": "arrow", "type": "line", "x1": 596, "y1": 235, "x2": 1189, "y2": 235, "stroke": "#CCCED2", "stroke_width": 22},
        {"id": "arrow_head1", "type": "line", "x1": 1189, "y1": 235, "x2": 1159, "y2": 205, "stroke": "#CCCED2", "stroke_width": 22},
        {"id": "arrow_head2", "type": "line", "x1": 1189, "y1": 235, "x2": 1159, "y2": 265, "stroke": "#CCCED2", "stroke_width": 22},
        {"id": "plus_circle", "type": "circle", "cx": 893, "cy": 235, "r": 48, "stroke": "#B9D8DA", "stroke_width": 10, "fill": "#F6F6F6"},
        {"id": "plus_h", "type": "line", "x1": 868, "y1": 235, "x2": 918, "y2": 235, "stroke": "#3A3338", "stroke_width": 4},
        {"id": "plus_v", "type": "line", "x1": 893, "y1": 210, "x2": 893, "y2": 260, "stroke": "#3A3338", "stroke_width": 4},
        {"id": "table", "type": "rect", "x": 598, "y": 305, "width": 888, "height": 279, "stroke": "#B9D8DA", "stroke_width": 9, "fill": "none"},
        {"id": "v1", "type": "line", "x1": 895, "y1": 305, "x2": 895, "y2": 584, "stroke": "#B9D8DA", "stroke_width": 4},
        {"id": "v2", "type": "line", "x1": 1188, "y1": 305, "x2": 1188, "y2": 584, "stroke": "#B9D8DA", "stroke_width": 4},
        {"id": "h1", "type": "line", "x1": 598, "y1": 444, "x2": 1486, "y2": 444, "stroke": "#B9D8DA", "stroke_width": 4},
        {"id": "r1c1", "type": "text", "text": str(rows[0]["left"]), "x": 747, "y": 399, "anchor": "middle", "font_family": "Cambria", "font_size": 68, "fill": "#222222"},
        {"id": "r1c2", "type": "text", "text": str(rows[0]["middle"]), "x": 1040, "y": 399, "anchor": "middle", "font_family": "Cambria", "font_size": 68, "fill": "#222222"},
        {"id": "r2c1", "type": "text", "text": str(rows[1]["left"]), "x": 747, "y": 535, "anchor": "middle", "font_family": "Cambria", "font_size": 68, "fill": "#222222"},
        {"id": "r2c2", "type": "text", "text": str(rows[1]["middle"]), "x": 1040, "y": 535, "anchor": "middle", "font_family": "Cambria", "font_size": 68, "fill": "#222222"},
        {"id": "r1_blank", "type": "rect", "x": 1218, "y": 336, "width": 238, "height": 78, "rx": 10, "stroke": "#69BEEA", "stroke_width": 4, "fill": "none", "semantic_role": "answer_blank", "answer_blank": True, "choice": {"index": 1, "value": str(rows[0]["right"])}},
        {"id": "r2_blank", "type": "rect", "x": 1218, "y": 472, "width": 238, "height": 78, "rx": 10, "stroke": "#69BEEA", "stroke_width": 4, "fill": "none", "semantic_role": "answer_blank", "answer_blank": True, "choice": {"index": 2, "value": str(rows[1]["right"])}}
    ]

    return {"meta": {"schema": "modu_math.semantic.v2", "problem_id": problem_id, "source": f"problem/{problem_id}/manim/{problem_id}_manim.py"}, "problem": data, "canvas": {"width": 1498, "height": 644, "background": "#F6F6F6"}, "elements": elements}


class InputOutputTableProblem(Scene):
    def construct(self) -> None:
        semantic = create_semantic_payload(load_problem_data(Path(__file__)))
        validate_or_raise(semantic)
        render_manim_from_semantic(self, semantic)
        self.wait(2)


SceneClass = InputOutputTableProblem

if __name__ == "__main__":
    run_cli(Path(__file__), create_semantic_payload)
