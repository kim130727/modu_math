from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path

from manim import Scene, config

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
from problem.common.paths import (
    find_problem_dir,
    problem_input_json_path,
    semantic_json_path,
    semantic_svg_path,
)
from problem.common.svg_renderer import render_svg_from_semantic
from problem.common.validator import validate_logic, validate_structure


def _configure_manim_output_dirs() -> None:
    """Keep all Manim artifacts in this problem's manim directory."""
    problem_dir = find_problem_dir(Path(__file__))
    manim_dir = problem_dir / "manim"
    cache_dir = Path(tempfile.gettempdir()) / "modu_math_manim_cache" / problem_dir.name

    config.media_dir = str(manim_dir)
    config.images_dir = str(manim_dir / "images")
    config.video_dir = str(manim_dir / "videos")
    config.text_dir = str(cache_dir / "text")
    config.tex_dir = str(cache_dir / "tex")
    config.partial_movie_dir = str(cache_dir / "partial_movie_files")


_configure_manim_output_dirs()


def load_problem_data(problem_json_path: Path | None = None) -> dict:
    problem_dir = find_problem_dir(Path(__file__))
    path = problem_json_path or problem_input_json_path(problem_dir)
    return json.loads(path.read_text(encoding="utf-8-sig"))


def split_place_values(number: int) -> dict:
    return {
        "hundreds": number // 100,
        "tens": (number % 100) // 10,
        "ones": number % 10,
    }


def build_layout() -> dict:
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
            "width": 550,
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
    colors = layout["colors"]
    elements: list[dict] = []

    # Hundreds: render each 100-block as a 10x10 fake-3D cube array.
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

    # Tens: render each 10-block as a 1x10 fake-3D cube rod.
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

    # Ones: single fake-3D cubes.
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
    """Create a grid of fake-3D unit cubes."""
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
    """
    Build one unit cube as 3 faces (front/top/side) using rect primitives.
    """
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


def write_semantic_json(out_path: Path, payload: dict) -> Path:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return out_path


def default_paths() -> tuple[Path, Path]:
    problem_dir = find_problem_dir(Path(__file__))
    return semantic_json_path(problem_dir), semantic_svg_path(problem_dir)


def validate_or_raise(semantic: dict) -> None:
    structure_errors = validate_structure(semantic)
    logic_errors = validate_logic(semantic)

    if structure_errors or logic_errors:
        lines = ["Semantic validation failed:"]
        if structure_errors:
            lines.append("[structure]")
            lines.extend(f"- {item}" for item in structure_errors)
        if logic_errors:
            lines.append("[logic]")
            lines.extend(f"- {item}" for item in logic_errors)
        raise ValueError("\n".join(lines))


def run_cli() -> None:
    parser = argparse.ArgumentParser(
        description="Generate semantic.json, validate semantic payload, and render SVG."
    )
    parser.add_argument("--export-semantic", action="store_true", help="Create semantic JSON file")
    parser.add_argument("--render-svg", action="store_true", help="Render SVG from semantic JSON")
    parser.add_argument("--validate", action="store_true", help="Validate semantic payload only")
    parser.add_argument("--all", action="store_true", help="Run export + validate + render")
    parser.add_argument("--problem-in", type=Path, help="Input path for problem JSON data")
    parser.add_argument("--semantic-out", type=Path, help="Output path for semantic JSON")
    parser.add_argument("--semantic-in", type=Path, help="Input semantic JSON path")
    parser.add_argument("--svg-out", type=Path, help="Output path for SVG")
    args = parser.parse_args()

    do_export = args.export_semantic or args.all
    do_render = args.render_svg or args.all
    do_validate = args.validate or args.all

    if not (do_export or do_render or do_validate):
        parser.print_help()
        return

    default_json, default_svg = default_paths()
    semantic_out = args.semantic_out or default_json
    semantic_in = args.semantic_in or semantic_out
    svg_out = args.svg_out or default_svg

    semantic = None
    if semantic_in.exists() and not do_export:
        semantic = json.loads(semantic_in.read_text(encoding="utf-8-sig"))

    if semantic is None:
        semantic = create_semantic_payload(load_problem_data(args.problem_in))

    if do_export:
        validate_or_raise(semantic)
        out = write_semantic_json(semantic_out, semantic)
        print(f"[OK] semantic json created: {out}")

    if do_validate:
        validate_or_raise(semantic)
        print("[OK] semantic payload is valid")

    if do_render:
        validate_or_raise(semantic)
        svg = render_svg_from_semantic(semantic, svg_out)
        print(f"[OK] svg rendered: {svg}")


class BaseTenBlockAdditionProblem(Scene):
    def construct(self) -> None:
        semantic = create_semantic_payload(load_problem_data())
        validate_or_raise(semantic)
        render_manim_from_semantic(self, semantic)
        self.wait(2)


if __name__ == "__main__":
    run_cli()
