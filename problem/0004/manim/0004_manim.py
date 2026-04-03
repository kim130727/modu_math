from __future__ import annotations

import sys
from pathlib import Path

from manim import Scene

sys.dont_write_bytecode = True


def _ensure_repo_root_on_path() -> None:
    """Add repository root to sys.path for stable local imports."""
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


def split_place_values(number: int) -> dict:
    return {
        "hundreds": number // 100,
        "tens": (number % 100) // 10,
        "ones": number % 10,
    }


def build_layout() -> dict:
    # Intentionally aligned with 0003 layout values for consistent look-and-feel.
    return {
        "canvas": {
            "width": 1280,
            "height": 720,
            "background": "#F6F6F6",
        },
        "header": {
            "number_x": 42,
            "number_y": 72,
            "instruction_x": 132,
            "instruction_y": 72,
        },
        "model_box": {
            "x": 130,
            "y": 165,
            "width": 570,
            "height": 490,
        },
        "row_divider_y": 395,
        "top_row": {
            "base_x": 165,
            "base_y": 210,
        },
        "bottom_row": {
            "base_x": 165,
            "base_y": 430,
        },
        "blocks": {
            "cube_size": 11,
            "cube_gap": 1,
            "depth_x": 4,
            "depth_y": 4,
            "hundred_cols": 10,
            "hundred_rows": 10,
            "hundred_group_dx": 22,
            "hundred_group_dy": 18,
            "ten_group_gap": 12,
            "one_group_gap": 10,
        },
        "equation": {
            "text_x": 900,
            "text_y": 615,
            "blank_x": 1045,
            "blank_y": 567,
            "blank_w": 155,
            "blank_h": 78,
            "blank_rx": 10,
        },
        "colors": {
            "black": "#222222",
            "gray_border": "#9C9CA1",
            "yellow_fill": "#F3D13C",
            "yellow_top_fill": "#F8E27A",
            "yellow_side_fill": "#E2BE2D",
            "yellow_shadow_fill": "#CFAB21",
            "yellow_highlight": "#FFF0A8",
            "yellow_stroke": "#D9B427",
            "blue_stroke": "#69BEEA",
        },
    }


def create_semantic_payload(data: dict) -> dict:
    problem_id = f'{data["id"]:04d}'
    layout = build_layout()
    first = split_place_values(int(data["addends"][0]))
    second = split_place_values(int(data["addends"][1]))

    elements: list[dict] = [
        {
            "id": "problem_number",
            "type": "text",
            "text": str(data["id"]),
            "x": layout["header"]["number_x"],
            "y": layout["header"]["number_y"],
            "anchor": "start",
            "font_family": "Malgun Gothic",
            "font_size": 62,
            "fill": "#7D49A4",
            "group": "header",
            "semantic_role": "problem_number",
        },
        {
            "id": "instruction",
            "type": "text",
            "text": data["instruction"],
            "x": layout["header"]["instruction_x"],
            "y": layout["header"]["instruction_y"],
            "anchor": "start",
            "font_family": "Malgun Gothic",
            "font_size": 50,
            "fill": layout["colors"]["black"],
            "group": "header",
            "semantic_role": "instruction",
        },
        {
            "id": "model_box",
            "type": "rect",
            "x": layout["model_box"]["x"],
            "y": layout["model_box"]["y"],
            "width": layout["model_box"]["width"],
            "height": layout["model_box"]["height"],
            "stroke": layout["colors"]["gray_border"],
            "stroke_width": 3,
            "fill": "none",
            "group": "model",
            "semantic_role": "container",
            "figure_type": "box",
        },
        {
            "id": "row_divider",
            "type": "line",
            "x1": layout["model_box"]["x"],
            "y1": layout["row_divider_y"],
            "x2": layout["model_box"]["x"] + layout["model_box"]["width"],
            "y2": layout["row_divider_y"],
            "stroke": layout["colors"]["gray_border"],
            "stroke_width": 3,
            "group": "model",
            "semantic_role": "row_divider",
            "figure_type": "separator",
        },
        {
            "id": "equation_text",
            "type": "text",
            "text": f'{data["addends"][0]}+{data["addends"][1]}=',
            "x": layout["equation"]["text_x"],
            "y": layout["equation"]["text_y"],
            "anchor": "middle",
            "font_family": "Malgun Gothic",
            "font_size": 44,
            "fill": layout["colors"]["black"],
            "group": "equation",
            "semantic_role": "equation",
        },
        {
            "id": "answer_blank",
            "type": "rect",
            "x": layout["equation"]["blank_x"],
            "y": layout["equation"]["blank_y"],
            "width": layout["equation"]["blank_w"],
            "height": layout["equation"]["blank_h"],
            "rx": layout["equation"]["blank_rx"],
            "stroke": layout["colors"]["blue_stroke"],
            "stroke_width": 4,
            "fill": "none",
            "group": "equation",
            "semantic_role": "answer_blank",
            "answer_blank": True,
            "figure_type": "blank_box",
            "choice": {"index": 1, "value": str(data["answer"])} ,
        },
    ]

    elements.extend(_build_place_value_blocks("addend1", first, layout["top_row"]["base_x"], layout["top_row"]["base_y"], layout))
    elements.extend(_build_place_value_blocks("addend2", second, layout["bottom_row"]["base_x"], layout["bottom_row"]["base_y"], layout))

    return {
        "meta": {
            "schema": "modu_math.semantic.v2",
            "problem_id": problem_id,
            "source": f"problem/{problem_id}/manim/{problem_id}_manim.py",
        },
        "problem": data,
        "canvas": layout["canvas"],
        "elements": elements,
    }


def _build_place_value_blocks(prefix: str, place: dict, base_x: float, base_y: float, layout: dict) -> list[dict]:
    blocks = layout["blocks"]
    elements: list[dict] = []

    for i in range(place["hundreds"]):
        hx = base_x + i * blocks["hundred_group_dx"]
        hy = base_y + (place["hundreds"] - 1 - i) * blocks["hundred_group_dy"]
        elements.extend(
            _build_cube_grid(
                id_prefix=f"{prefix}_hundred_{i}",
                start_x=hx,
                start_y=hy,
                cols=blocks["hundred_cols"],
                rows=blocks["hundred_rows"],
                group=prefix,
                semantic_role="place_hundred",
                figure_type="hundred_cubes",
                layout=layout,
            )
        )

    rod_w = blocks["hundred_cols"] * (blocks["cube_size"] + blocks["cube_gap"]) - blocks["cube_gap"]
    rods_x = base_x + 230
    rods_start_y = base_y + 8
    for i in range(place["tens"]):
        y = rods_start_y + i * (blocks["cube_size"] + blocks["ten_group_gap"])
        elements.extend(
            _build_cube_grid(
                id_prefix=f"{prefix}_ten_{i}",
                start_x=rods_x,
                start_y=y,
                cols=10,
                rows=1,
                group=prefix,
                semantic_role="place_ten",
                figure_type="ten_cubes",
                layout=layout,
            )
        )

    ones_x = rods_x + rod_w + 25
    ones_y = base_y + 44
    for i in range(place["ones"]):
        x = ones_x + i * (blocks["cube_size"] + blocks["one_group_gap"])
        y = ones_y
        elements.extend(
            _build_fake3d_cube(
                id_prefix=f"{prefix}_one_{i}",
                x=x,
                y=y,
                group=prefix,
                semantic_role="place_one",
                figure_type="one_cube",
                layout=layout,
            )
        )

    return elements


def _build_cube_grid(
    id_prefix: str,
    start_x: float,
    start_y: float,
    cols: int,
    rows: int,
    group: str,
    semantic_role: str,
    figure_type: str,
    layout: dict,
) -> list[dict]:
    blocks = layout["blocks"]
    elements: list[dict] = []
    for r in range(rows):
        for c in range(cols):
            x = start_x + c * (blocks["cube_size"] + blocks["cube_gap"])
            y = start_y + r * (blocks["cube_size"] + blocks["cube_gap"])
            elements.extend(
                _build_fake3d_cube(
                    id_prefix=f"{id_prefix}_c{c}_r{r}",
                    x=x,
                    y=y,
                    group=group,
                    semantic_role=semantic_role,
                    figure_type=figure_type,
                    layout=layout,
                )
            )
    return elements


def _build_fake3d_cube(
    id_prefix: str,
    x: float,
    y: float,
    group: str,
    semantic_role: str,
    figure_type: str,
    layout: dict,
) -> list[dict]:
    blocks = layout["blocks"]
    colors = layout["colors"]
    s = blocks["cube_size"]
    dx = blocks["depth_x"]
    dy = blocks["depth_y"]

    common = {
        "group": group,
        "semantic_role": semantic_role,
        "figure_type": figure_type,
        "stroke": colors["yellow_stroke"],
        "stroke_width": 1,
    }

    return [
        {
            "id": f"{id_prefix}_shadow",
            "type": "rect",
            "x": x + 1,
            "y": y + 1,
            "width": s,
            "height": s,
            "fill": colors["yellow_shadow_fill"],
            **common,
        },
        {
            "id": f"{id_prefix}_front",
            "type": "rect",
            "x": x,
            "y": y,
            "width": s,
            "height": s,
            "fill": colors["yellow_fill"],
            **common,
        },
        {
            "id": f"{id_prefix}_top",
            "type": "rect",
            "x": x + dx,
            "y": y - dy,
            "width": s,
            "height": dy,
            "fill": colors["yellow_top_fill"],
            **common,
        },
        {
            "id": f"{id_prefix}_side",
            "type": "rect",
            "x": x + s,
            "y": y,
            "width": dx,
            "height": s,
            "fill": colors["yellow_side_fill"],
            **common,
        },
        {
            "id": f"{id_prefix}_highlight_top",
            "type": "line",
            "x1": x + dx,
            "y1": y - dy,
            "x2": x + dx + s,
            "y2": y - dy,
            "stroke": colors["yellow_highlight"],
            "stroke_width": 1,
            "group": group,
            "semantic_role": semantic_role,
            "figure_type": figure_type,
        },
        {
            "id": f"{id_prefix}_highlight_side",
            "type": "line",
            "x1": x + s + dx,
            "y1": y - dy,
            "x2": x + s + dx,
            "y2": y + s,
            "stroke": colors["yellow_highlight"],
            "stroke_width": 1,
            "group": group,
            "semantic_role": semantic_role,
            "figure_type": figure_type,
        },
    ]


class BaseTenModelAdditionProblem(Scene):
    def construct(self) -> None:
        semantic = create_semantic_payload(load_problem_data(Path(__file__)))
        validate_or_raise(semantic)
        render_manim_from_semantic(self, semantic)
        self.wait(2)


SceneClass = BaseTenModelAdditionProblem


if __name__ == "__main__":
    run_cli(Path(__file__), create_semantic_payload)
