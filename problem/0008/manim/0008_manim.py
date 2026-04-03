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
        {
            "id": "num",
            "type": "text",
            "text": str(data["id"]),
            "x": 40,
            "y": 74,
            "anchor": "start",
            "font_family": "Malgun Gothic",
            "font_size": 60,
            "fill": "#6F3FA2",
            "semantic_role": "problem_number",
        },
        {
            "id": "inst",
            "type": "text",
            "text": data["instruction"],
            "x": 118,
            "y": 69,
            "anchor": "start",
            "font_family": "Malgun Gothic",
            "font_size": 36,
            "manim_font_size": 32,
            "fill": "#222222",
            "semantic_role": "instruction",
        },
        {
            "id": "board",
            "type": "rect",
            "x": 145,
            "y": 112,
            "width": 775,
            "height": 625,
            "rx": 40,
            "stroke": "#B58D61",
            "stroke_width": 10,
            "fill": "#EFDDBB",
            "semantic_role": "container",
        },
        {
            "id": "eq1_top",
            "type": "text",
            "text": f"{eq1['a']}",
            "x": 492,
            "y": 259,
            "anchor": "end",
            "font_family": "Cambria",
            "font_size": 62,
            "fill": "#222222",
            "semantic_role": "equation_operand",
        },
        {
            "id": "eq1_mid",
            "type": "text",
            "text": f"+{eq1['b']}",
            "x": 492,
            "y": 335,
            "anchor": "end",
            "font_family": "Cambria",
            "font_size": 62,
            "fill": "#222222",
            "semantic_role": "equation_operand",
        },
        {
            "id": "eq1_line",
            "type": "line",
            "x1": 290,
            "y1": 378,
            "x2": 505,
            "y2": 378,
            "stroke": "#333333",
            "stroke_width": 2,
            "semantic_role": "equation_bar",
        },
        {
            "id": "eq2_top",
            "type": "text",
            "text": f"{eq2['a']}",
            "x": 765,
            "y": 259,
            "anchor": "end",
            "font_family": "Cambria",
            "font_size": 62,
            "fill": "#222222",
            "semantic_role": "equation_operand",
        },
        {
            "id": "eq2_mid",
            "type": "text",
            "text": f"+{eq2['b']}",
            "x": 765,
            "y": 335,
            "anchor": "end",
            "font_family": "Cambria",
            "font_size": 62,
            "fill": "#222222",
            "semantic_role": "equation_operand",
        },
        {
            "id": "eq2_line",
            "type": "line",
            "x1": 563,
            "y1": 378,
            "x2": 778,
            "y2": 378,
            "stroke": "#333333",
            "stroke_width": 2,
            "semantic_role": "equation_bar",
        },
        {
            "id": "map_box",
            "type": "rect",
            "x": 255,
            "y": 454,
            "width": 560,
            "height": 148,
            "rx": 34,
            "stroke": "#000000",
            "stroke_width": 0,
            "fill": "#F9F9F9",
            "semantic_role": "hint_box",
        },
    ]

    dmap = data.get("digit_map", {})
    line1 = "   ".join([f"{k}={dmap.get(k, '?')}" for k in ["1", "2", "3", "4", "5"]])
    line2 = "   ".join([f"{k}={dmap.get(k, '?')}" for k in ["6", "7", "8", "9", "0"]])

    elements.extend(
        [
            {
                "id": "map_line_1",
                "type": "text",
                "text": line1,
                "x": 535,
                "y": 522,
                "anchor": "middle",
                "font_family": "Malgun Gothic",
                "font_size": 34,
                "fill": "#333333",
                "semantic_role": "hint_text",
            },
            {
                "id": "map_line_2",
                "type": "text",
                "text": line2,
                "x": 535,
                "y": 580,
                "anchor": "middle",
                "font_family": "Malgun Gothic",
                "font_size": 34,
                "fill": "#333333",
                "semantic_role": "hint_text",
            },
            {
                "id": "final_l",
                "type": "text",
                "text": "(",
                "x": 572,
                "y": 783,
                "anchor": "middle",
                "font_family": "Cambria",
                "font_size": 58,
                "fill": "#222222",
                "semantic_role": "answer_wrapper",
            },
            {
                "id": "final_r",
                "type": "text",
                "text": ")",
                "x": 946,
                "y": 783,
                "anchor": "middle",
                "font_family": "Cambria",
                "font_size": 58,
                "fill": "#222222",
                "semantic_role": "answer_wrapper",
            },
        ]
    )

    right_edge_1 = 496
    start_x1 = right_edge_1 - (3 * 46 + 2 * 8)
    for i, ch in enumerate(str(eq1["sum"])):
        elements.append(
            {
                "id": f"eq1_blank_{i}",
                "type": "rect",
                "x": start_x1 + i * 54,
                "y": 386,
                "width": 46,
                "height": 46,
                "rx": 6,
                "stroke": "#69BEEA",
                "stroke_width": 3,
                "fill": "none",
                "semantic_role": "answer_blank",
                "answer_blank": True,
                "choice": {"index": i + 2, "value": ch},
            }
        )

    right_edge_2 = 770
    start_x2 = right_edge_2 - (3 * 46 + 2 * 8)
    for i, ch in enumerate(str(eq2["sum"])):
        elements.append(
            {
                "id": f"eq2_blank_{i}",
                "type": "rect",
                "x": start_x2 + i * 54,
                "y": 386,
                "width": 46,
                "height": 46,
                "rx": 6,
                "stroke": "#69BEEA",
                "stroke_width": 3,
                "fill": "none",
                "semantic_role": "answer_blank",
                "answer_blank": True,
                "choice": {"index": i + 5, "value": ch},
            }
        )

    return {
        "meta": {
            "schema": "modu_math.semantic.v2",
            "problem_id": problem_id,
            "source": f"problem/{problem_id}/manim/{problem_id}_manim.py",
        },
        "problem": data,
        "canvas": {"width": 981, "height": 818, "background": "#F6F6F6"},
        "elements": elements,
    }


class HiddenWordAdditionProblem(Scene):
    def construct(self) -> None:
        semantic = create_semantic_payload(load_problem_data(Path(__file__)))
        validate_or_raise(semantic)
        render_manim_from_semantic(self, semantic)
        self.wait(2)


class SceneClass(HiddenWordAdditionProblem):
    pass


if __name__ == "__main__":
    run_cli(Path(__file__), create_semantic_payload)
