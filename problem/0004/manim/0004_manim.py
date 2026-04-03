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
from problem.common.problem_cli import (
    configure_manim_output_dirs,
    load_problem_data,
    run_cli,
    validate_or_raise,
)

configure_manim_output_dirs(Path(__file__))


def _add_hundred_block(elements: list[dict], block_id: str, x: float, y: float) -> None:
    size = 168
    elements.append(
        {
            "id": f"{block_id}_body",
            "type": "rect",
            "x": x,
            "y": y,
            "width": size,
            "height": size,
            "stroke": "#C9A521",
            "stroke_width": 2,
            "fill": "#F3D13C",
            "group": "blocks",
            "semantic_role": "place_hundred",
            "figure_type": "hundred_block",
        }
    )
    step = size / 10
    for i in range(1, 10):
        gx = x + i * step
        gy = y + i * step
        elements.append(
            {
                "id": f"{block_id}_v_{i}",
                "type": "line",
                "x1": gx,
                "y1": y,
                "x2": gx,
                "y2": y + size,
                "stroke": "#DAB735",
                "stroke_width": 1,
                "group": "blocks",
            }
        )
        elements.append(
            {
                "id": f"{block_id}_h_{i}",
                "type": "line",
                "x1": x,
                "y1": gy,
                "x2": x + size,
                "y2": gy,
                "stroke": "#DAB735",
                "stroke_width": 1,
                "group": "blocks",
            }
        )


def _add_ten_rod(elements: list[dict], rod_id: str, x: float, y: float) -> None:
    elements.append(
        {
            "id": rod_id,
            "type": "rect",
            "x": x,
            "y": y,
            "width": 170,
            "height": 24,
            "stroke": "#C9A521",
            "stroke_width": 2,
            "fill": "#F3D13C",
            "group": "blocks",
            "semantic_role": "place_ten",
            "figure_type": "ten_rod",
        }
    )


def _add_one_cube(elements: list[dict], cube_id: str, x: float, y: float) -> None:
    elements.append(
        {
            "id": cube_id,
            "type": "rect",
            "x": x,
            "y": y,
            "width": 26,
            "height": 26,
            "stroke": "#C9A521",
            "stroke_width": 2,
            "fill": "#F3D13C",
            "group": "blocks",
            "semantic_role": "place_one",
            "figure_type": "one_cube",
        }
    )


def create_semantic_payload(data: dict) -> dict:
    problem_id = f"{int(data['id']):04d}"
    a, b = int(data["addends"][0]), int(data["addends"][1])
    ah, at, ao = a // 100, (a % 100) // 10, a % 10
    bh, bt, bo = b // 100, (b % 100) // 10, b % 10

    canvas = {"width": 1366, "height": 600, "background": "#F6F6F6"}
    elements: list[dict] = [
        {
            "id": "problem_no",
            "type": "text",
            "text": str(data["id"]),
            "x": 38,
            "y": 78,
            "anchor": "start",
            "font_family": "Malgun Gothic",
            "font_size": 76,
            "fill": "#6F3FA2",
            "group": "header",
        },
        {
            "id": "instruction",
            "type": "text",
            "text": data["instruction"],
            "x": 145,
            "y": 70,
            "anchor": "start",
            "font_family": "Malgun Gothic",
            "font_size": 56,
            "fill": "#222222",
            "group": "header",
        },
        {
            "id": "model_box",
            "type": "rect",
            "x": 205,
            "y": 125,
            "width": 690,
            "height": 465,
            "stroke": "#9C9CA1",
            "stroke_width": 3,
            "fill": "none",
            "group": "model",
        },
        {
            "id": "divider",
            "type": "line",
            "x1": 205,
            "y1": 262,
            "x2": 895,
            "y2": 262,
            "stroke": "#9C9CA1",
            "stroke_width": 3,
            "group": "model",
        },
        {
            "id": "equation",
            "type": "text",
            "text": f"{a}+{b}=",
            "x": 1048,
            "y": 562,
            "anchor": "middle",
            "font_family": "Malgun Gothic",
            "font_size": 62,
            "fill": "#222222",
            "group": "equation",
        },
        {
            "id": "answer_blank",
            "type": "rect",
            "x": 1170,
            "y": 523,
            "width": 140,
            "height": 68,
            "rx": 10,
            "stroke": "#69BEEA",
            "stroke_width": 4,
            "fill": "none",
            "group": "equation",
            "semantic_role": "answer_blank",
            "answer_blank": True,
            "choice": {"index": 1, "value": str(data["answer"])}
        },
    ]

    for i in range(ah):
        _add_hundred_block(elements, f"a_h_{i}", 225 + i * 28, 154 + (ah - 1 - i) * 10)
    for i in range(at):
        _add_ten_rod(elements, f"a_t_{i}", 503, 152 + i * 32)
    for i in range(ao):
        _add_one_cube(elements, f"a_o_{i}", 719 + (i % 5) * 32, 168 + (i // 5) * 36)

    for i in range(bh):
        _add_hundred_block(elements, f"b_h_{i}", 225 + i * 28, 354 + (bh - 1 - i) * 10)
    for i in range(bt):
        _add_ten_rod(elements, f"b_t_{i}", 503, 292 + i * 31)
    for i in range(bo):
        _add_one_cube(elements, f"b_o_{i}", 719 + (i % 5) * 32, 385 + (i // 5) * 36)

    return {
        "meta": {
            "schema": "modu_math.semantic.v2",
            "problem_id": problem_id,
            "source": f"problem/{problem_id}/manim/{problem_id}_manim.py",
        },
        "problem": data,
        "canvas": canvas,
        "elements": elements,
    }


class BaseTenModelAdditionProblem(Scene):
    def construct(self) -> None:
        semantic = create_semantic_payload(load_problem_data(Path(__file__)))
        validate_or_raise(semantic)
        render_manim_from_semantic(self, semantic)
        self.wait(2)


SceneClass = BaseTenModelAdditionProblem

if __name__ == "__main__":
    run_cli(Path(__file__), create_semantic_payload)
