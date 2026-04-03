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


def build_expression(data: dict) -> str:
    q = data["question"]
    return (
        f'{q["left_seconds"]}{q["unit_from"]}='
        f'{q["minutes"]}{q["unit_mid"]} '
        f'{q["blank_symbol"]}{q["unit_to"]}'
    )


def build_layout() -> dict:
    return {
        "canvas": {
            "width": 1280,
            "height": 720,
            "background": "#F6F6F6",
        },
        "instruction": {"x": 72, "y": 92},
        "question_box": {"x": 280, "y": 240, "width": 720, "height": 180, "rx": 24},
        "expression": {"x": 640, "y": 345},
        "answer_left": {"x": 780, "y": 560},
        "answer_right": {"x": 960, "y": 560},
    }


def create_semantic_payload(data: dict) -> dict:
    problem_id = f'{data["id"]:04d}'
    layout = build_layout()

    return {
        "meta": {
            "schema": "modu_math.semantic.v2",
            "problem_id": problem_id,
            "source": f"problem/{problem_id}/manim/{problem_id}_manim.py",
        },
        "problem": data,
        "canvas": layout["canvas"],
        "elements": [
            {
                "id": "instruction",
                "type": "text",
                "text": data["instruction"],
                "x": layout["instruction"]["x"],
                "y": layout["instruction"]["y"],
                "anchor": "start",
                "font_family": "Malgun Gothic",
                "font_size": 42,
                "fill": "#000000",
                "group": "header",
                "semantic_role": "instruction",
            },
            {
                "id": "question_box",
                "type": "rect",
                "x": layout["question_box"]["x"],
                "y": layout["question_box"]["y"],
                "width": layout["question_box"]["width"],
                "height": layout["question_box"]["height"],
                "rx": layout["question_box"]["rx"],
                "stroke": "#000000",
                "stroke_width": 3,
                "fill": "none",
                "group": "question",
                "semantic_role": "question_container",
                "figure_type": "rounded_box",
            },
            {
                "id": "expression",
                "type": "text",
                "text": build_expression(data),
                "x": layout["expression"]["x"],
                "y": layout["expression"]["y"],
                "anchor": "middle",
                "font_family": "Malgun Gothic",
                "font_size": 54,
                "fill": "#000000",
                "group": "question",
                "semantic_role": "equation",
            },
            {
                "id": "answer_left_paren",
                "type": "text",
                "text": "(",
                "x": layout["answer_left"]["x"],
                "y": layout["answer_left"]["y"],
                "anchor": "middle",
                "font_family": "Malgun Gothic",
                "font_size": 56,
                "fill": "#000000",
                "group": "answer_area",
                "semantic_role": "answer_wrapper",
            },
            {
                "id": "answer_blank_slot",
                "type": "rect",
                "x": 818,
                "y": 526,
                "width": 122,
                "height": 50,
                "rx": 8,
                "stroke": "#000000",
                "stroke_width": 2,
                "fill": "none",
                "group": "answer_area",
                "semantic_role": "answer_blank",
                "answer_blank": True,
                "figure_type": "blank_box",
                "choice": {"index": 1, "value": str(data["answer"])},
            },
            {
                "id": "answer_right_paren",
                "type": "text",
                "text": ")",
                "x": layout["answer_right"]["x"],
                "y": layout["answer_right"]["y"],
                "anchor": "middle",
                "font_family": "Malgun Gothic",
                "font_size": 56,
                "fill": "#000000",
                "group": "answer_area",
                "semantic_role": "answer_wrapper",
            },
        ],
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


class TimeConversionProblem(Scene):
    def construct(self) -> None:
        semantic = create_semantic_payload(load_problem_data())
        validate_or_raise(semantic)
        render_manim_from_semantic(self, semantic)
        self.wait(2)


if __name__ == "__main__":
    run_cli()


