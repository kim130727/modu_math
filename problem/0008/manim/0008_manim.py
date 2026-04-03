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
    eq1, eq2 = data["equations"]

    elements: list[dict] = [
        {"id": "num", "type": "text", "text": str(data["id"]), "x": 40, "y": 74, "anchor": "start", "font_family": "Malgun Gothic", "font_size": 72, "fill": "#6F3FA2"},
        {"id": "inst", "type": "text", "text": data["instruction"], "x": 118, "y": 69, "anchor": "start", "font_family": "Malgun Gothic", "font_size": 50, "fill": "#222222"},
        {"id": "inst_blank", "type": "rect", "x": 116, "y": 45, "width": 28, "height": 28, "rx": 6, "stroke": "#69BEEA", "stroke_width": 3, "fill": "none"},
        {"id": "board", "type": "rect", "x": 145, "y": 112, "width": 775, "height": 625, "rx": 40, "stroke": "#B58D61", "stroke_width": 10, "fill": "#EFDDBB"},
        {"id": "eq1_top", "type": "text", "text": f"{eq1['a']:>3}", "x": 405, "y": 259, "anchor": "middle", "font_family": "Cambria", "font_size": 62, "fill": "#222222"},
        {"id": "eq1_mid", "type": "text", "text": f"+{eq1['b']:>3}", "x": 405, "y": 335, "anchor": "middle", "font_family": "Cambria", "font_size": 62, "fill": "#222222"},
        {"id": "eq1_line", "type": "line", "x1": 290, "y1": 378, "x2": 505, "y2": 378, "stroke": "#333333", "stroke_width": 2},
        {"id": "eq2_top", "type": "text", "text": f"{eq2['a']:>3}", "x": 677, "y": 259, "anchor": "middle", "font_family": "Cambria", "font_size": 62, "fill": "#222222"},
        {"id": "eq2_mid", "type": "text", "text": f"+{eq2['b']:>3}", "x": 677, "y": 335, "anchor": "middle", "font_family": "Cambria", "font_size": 62, "fill": "#222222"},
        {"id": "eq2_line", "type": "line", "x1": 563, "y1": 378, "x2": 778, "y2": 378, "stroke": "#333333", "stroke_width": 2},
        {"id": "map_box", "type": "rect", "x": 255, "y": 454, "width": 560, "height": 148, "rx": 34, "stroke": "none", "stroke_width": 0, "fill": "#F9F9F9"},
        {"id": "map_line_1", "type": "text", "text": "1=나   2=이   3=요   4=구   5=꿍", "x": 535, "y": 522, "anchor": "middle", "font_family": "Malgun Gothic", "font_size": 30, "fill": "#333333"},
        {"id": "map_line_2", "type": "text", "text": "6=월   7=친   8=와   9=짝   0=너", "x": 535, "y": 580, "anchor": "middle", "font_family": "Malgun Gothic", "font_size": 30, "fill": "#333333"},
        {"id": "final_l", "type": "text", "text": "(", "x": 572, "y": 783, "anchor": "middle", "font_family": "Cambria", "font_size": 58, "fill": "#222222"},
        {"id": "final_r", "type": "text", "text": ")", "x": 946, "y": 783, "anchor": "middle", "font_family": "Cambria", "font_size": 58, "fill": "#222222"},
        {"id": "final_blank", "type": "rect", "x": 595, "y": 752, "width": 320, "height": 46, "rx": 8, "stroke": "#69BEEA", "stroke_width": 3, "fill": "none", "semantic_role": "answer_blank", "answer_blank": True, "choice": {"index": 1, "value": data["hidden_word"]}},
    ]

    start_x1 = 340
    for i, ch in enumerate(str(eq1["sum"])):
        elements.append({"id": f"eq1_blank_{i}", "type": "rect", "x": start_x1 + i * 54, "y": 386, "width": 46, "height": 46, "rx": 6, "stroke": "#69BEEA", "stroke_width": 3, "fill": "none", "semantic_role": "answer_blank", "answer_blank": True, "choice": {"index": i + 2, "value": ch}})

    start_x2 = 612
    for i, ch in enumerate(str(eq2["sum"])):
        elements.append({"id": f"eq2_blank_{i}", "type": "rect", "x": start_x2 + i * 54, "y": 386, "width": 46, "height": 46, "rx": 6, "stroke": "#69BEEA", "stroke_width": 3, "fill": "none", "semantic_role": "answer_blank", "answer_blank": True, "choice": {"index": i + 5, "value": ch}})

    return {"meta": {"schema": "modu_math.semantic.v2", "problem_id": problem_id, "source": f"problem/{problem_id}/manim/{problem_id}_manim.py"}, "problem": data, "canvas": {"width": 981, "height": 818, "background": "#F6F6F6"}, "elements": elements}


class HiddenWordAdditionProblem(Scene):
    def construct(self) -> None:
        semantic = create_semantic_payload(load_problem_data(Path(__file__)))
        validate_or_raise(semantic)
        render_manim_from_semantic(self, semantic)
        self.wait(2)


SceneClass = HiddenWordAdditionProblem

if __name__ == "__main__":
    run_cli(Path(__file__), create_semantic_payload)
