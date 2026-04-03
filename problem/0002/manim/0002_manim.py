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


def build_layout(data: dict) -> dict:
    """
    Build all geometric values in one place.

    Why: a single source of coordinates avoids drift between Manim/SVG layers.
    """
    canvas = {
        "width": 1280,
        "height": 720,
        "background": "#F7F7F7",
    }

    ruler = {
        "x": 220,
        "y": 330,
        "width": 820,
        "height": 170,
        "stroke": "#C9A000",
        "stroke_width": 6,
    }

    start_cm = data["ruler"]["start_cm"]
    end_cm = data["ruler"]["end_cm"]
    total_cm = end_cm - start_cm
    minor_per_cm = data["ruler"]["minor_per_cm"]

    def x_from_cm(cm_value: float) -> float:
        ratio = (cm_value - start_cm) / total_cm
        return ruler["x"] + ratio * ruler["width"]

    left_cm = data["measurement"]["left_cm"]
    right_cm = data["measurement"]["right_cm"]
    left_x = x_from_cm(left_cm)
    right_x = x_from_cm(right_cm)

    eraser = {
        "x": left_x,
        "y": 170,
        "width": right_x - left_x,
        "height": 135,
        "rx": 20,
        "stroke": "#4F6FB3",
        "stroke_width": 2,
        "fill": "#D9E5CF",
    }

    return {
        "canvas": canvas,
        "title": {"x": 72, "y": 80},
        "subtitle": {"x": 72, "y": 128},
        "ruler": ruler,
        "ticks": {
            "top_y": ruler["y"],
            "minor_len": 34,
            "major_len": 64,
            "minor_stroke": 5,
            "major_stroke": 6,
            "total_minor_steps": int(total_cm * minor_per_cm),
            "start_cm": start_cm,
            "minor_per_cm": minor_per_cm,
            "x_from_cm": x_from_cm,
        },
        "numbers": {"y": ruler["y"] + ruler["height"] - 38},
        "eraser": eraser,
        "dash": {
            "top_y": eraser["y"] - 20,
            "bottom_y": ruler["y"] + 4,
            "dasharray": "10 8",
            "stroke": "#000000",
            "stroke_width": 3,
            "left_x": left_x,
            "right_x": right_x,
        },
        "answer": {
            "left_paren": {"x": 530, "y": 640},
            "right_paren": {"x": 900, "y": 640},
        },
    }


def create_semantic_payload(data: dict) -> dict:
    problem_id = f'{data["id"]:04d}'
    layout = build_layout(data)

    elements: list[dict] = [
        {
            "id": "instruction",
            "type": "text",
            "text": data["instruction"],
            "x": layout["title"]["x"],
            "y": layout["title"]["y"],
            "anchor": "start",
            "font_family": "Malgun Gothic",
            "font_size": 42,
            "fill": "#000000",
            "group": "header",
            "semantic_role": "instruction",
        },
        {
            "id": "sub_instruction",
            "type": "text",
            "text": data["sub_instruction"],
            "x": layout["subtitle"]["x"],
            "y": layout["subtitle"]["y"],
            "anchor": "start",
            "font_family": "Malgun Gothic",
            "font_size": 30,
            "fill": "#000000",
            "group": "header",
            "semantic_role": "sub_instruction",
        },
        {
            "id": "ruler_body",
            "type": "rect",
            "x": layout["ruler"]["x"],
            "y": layout["ruler"]["y"],
            "width": layout["ruler"]["width"],
            "height": layout["ruler"]["height"],
            "stroke": layout["ruler"]["stroke"],
            "stroke_width": layout["ruler"]["stroke_width"],
            "fill": "none",
            "group": "ruler",
            "semantic_role": "scale",
            "figure_type": "ruler",
        },
        {
            "id": "eraser_body",
            "type": "rect",
            "x": layout["eraser"]["x"],
            "y": layout["eraser"]["y"],
            "width": layout["eraser"]["width"],
            "height": layout["eraser"]["height"],
            "rx": layout["eraser"]["rx"],
            "stroke": layout["eraser"]["stroke"],
            "stroke_width": layout["eraser"]["stroke_width"],
            "fill": layout["eraser"]["fill"],
            "group": "object",
            "semantic_role": "target_object",
            "figure_type": "eraser",
        },
        {
            "id": "eraser_label",
            "type": "text",
            "text": data["object_label"],
            "x": layout["eraser"]["x"] + layout["eraser"]["width"] / 2,
            "y": layout["eraser"]["y"] + layout["eraser"]["height"] / 2 + 14,
            "anchor": "middle",
            "font_family": "Malgun Gothic",
            "font_size": 42,
            "font_weight": "bold",
            "fill": "#000000",
            "group": "object",
            "semantic_role": "object_label",
        },
        {
            "id": "dash_left",
            "type": "line",
            "x1": layout["dash"]["left_x"],
            "y1": layout["dash"]["top_y"],
            "x2": layout["dash"]["left_x"],
            "y2": layout["dash"]["bottom_y"],
            "stroke": layout["dash"]["stroke"],
            "stroke_width": layout["dash"]["stroke_width"],
            "dasharray": layout["dash"]["dasharray"],
            "group": "guide",
            "semantic_role": "measurement_guide",
            "figure_type": "dashed_line",
        },
        {
            "id": "dash_right",
            "type": "line",
            "x1": layout["dash"]["right_x"],
            "y1": layout["dash"]["top_y"],
            "x2": layout["dash"]["right_x"],
            "y2": layout["dash"]["bottom_y"],
            "stroke": layout["dash"]["stroke"],
            "stroke_width": layout["dash"]["stroke_width"],
            "dasharray": layout["dash"]["dasharray"],
            "group": "guide",
            "semantic_role": "measurement_guide",
            "figure_type": "dashed_line",
        },
        {
            "id": "answer_left_paren",
            "type": "text",
            "text": "(",
            "x": layout["answer"]["left_paren"]["x"],
            "y": layout["answer"]["left_paren"]["y"],
            "anchor": "middle",
            "font_family": "Arial",
            "font_size": 54,
            "fill": "#000000",
            "group": "answer_area",
            "semantic_role": "answer_wrapper",
        },
        {
            "id": "answer_right_paren",
            "type": "text",
            "text": ")",
            "x": layout["answer"]["right_paren"]["x"],
            "y": layout["answer"]["right_paren"]["y"],
            "anchor": "middle",
            "font_family": "Arial",
            "font_size": 54,
            "fill": "#000000",
            "group": "answer_area",
            "semantic_role": "answer_wrapper",
            "choice": {"index": 1, "value": str(data["answer_mm"])},
        },
    ]

    ticks = layout["ticks"]
    for i in range(ticks["total_minor_steps"] + 1):
        cm_value = ticks["start_cm"] + i / ticks["minor_per_cm"]
        x = ticks["x_from_cm"](cm_value)
        is_major = abs(cm_value - round(cm_value)) < 1e-8

        elements.append(
            {
                "id": f"tick_{i:02d}",
                "type": "line",
                "x1": x,
                "y1": ticks["top_y"],
                "x2": x,
                "y2": ticks["top_y"] + (ticks["major_len"] if is_major else ticks["minor_len"]),
                "stroke": layout["ruler"]["stroke"],
                "stroke_width": ticks["major_stroke"] if is_major else ticks["minor_stroke"],
                "group": "ruler",
                "semantic_role": "tick_major" if is_major else "tick_minor",
                "figure_type": "scale_tick",
            }
        )

    for major in data["ruler"]["major_ticks"]:
        elements.append(
            {
                "id": f"major_number_{major}",
                "type": "text",
                "text": str(major),
                "x": ticks["x_from_cm"](major),
                "y": layout["numbers"]["y"],
                "anchor": "middle",
                "font_family": "Arial",
                "font_size": 40,
                "fill": "#000000",
                "group": "ruler",
                "semantic_role": "scale_number",
            }
        )

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


class RulerEraserProblem(Scene):
    def construct(self) -> None:
        semantic = create_semantic_payload(load_problem_data())
        validate_or_raise(semantic)
        render_manim_from_semantic(self, semantic)
        self.wait(2)


if __name__ == "__main__":
    run_cli()


