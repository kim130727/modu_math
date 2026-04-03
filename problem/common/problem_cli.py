from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path
from typing import Callable

from manim import config

from problem.common.paths import (
    find_problem_dir,
    problem_input_json_path,
    semantic_json_path,
    semantic_svg_path,
)
from problem.common.svg_renderer import render_svg_from_semantic
from problem.common.validator import validate_logic, validate_structure


def ensure_repo_root_on_path(from_file: Path) -> None:
    """Add repository root to sys.path for stable local imports."""
    current = from_file.resolve()
    for parent in current.parents:
        if (parent / "problem").is_dir() and (parent / "README.md").exists():
            root = str(parent)
            if root not in sys.path:
                sys.path.insert(0, root)
            return
    raise RuntimeError("Repository root could not be resolved from current file path.")


def configure_manim_output_dirs(from_file: Path) -> None:
    """Keep all Manim artifacts in each problem's own manim directory."""
    problem_dir = find_problem_dir(from_file)
    manim_dir = problem_dir / "manim"
    cache_dir = Path(tempfile.gettempdir()) / "modu_math_manim_cache" / problem_dir.name

    config.media_dir = str(manim_dir)
    config.images_dir = str(manim_dir / "images")
    config.video_dir = str(manim_dir / "videos")
    config.text_dir = str(cache_dir / "text")
    config.tex_dir = str(cache_dir / "tex")
    config.partial_movie_dir = str(cache_dir / "partial_movie_files")


def load_problem_data(from_file: Path, problem_json_path: Path | None = None) -> dict:
    problem_dir = find_problem_dir(from_file)
    path = problem_json_path or problem_input_json_path(problem_dir)
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_semantic_json(out_path: Path, payload: dict) -> Path:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return out_path


def default_paths(from_file: Path) -> tuple[Path, Path]:
    problem_dir = find_problem_dir(from_file)
    return semantic_json_path(problem_dir), semantic_svg_path(problem_dir)


def _normalize_semantic_for_validation(semantic: dict) -> None:
    """Fill minimally required fields for legacy element payloads."""
    elements = semantic.get("elements", [])
    if not isinstance(elements, list):
        return
    for elem in elements:
        if not isinstance(elem, dict):
            continue
        elem.setdefault("semantic_role", "decorative")
        elem.setdefault("group", "default")


def validate_or_raise(semantic: dict) -> None:
    _normalize_semantic_for_validation(semantic)
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


def run_cli(from_file: Path, create_semantic_payload: Callable[[dict], dict]) -> None:
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

    default_json, default_svg = default_paths(from_file)
    semantic_out = args.semantic_out or default_json
    semantic_in = args.semantic_in or semantic_out
    svg_out = args.svg_out or default_svg

    semantic = None
    if semantic_in.exists() and not do_export:
        semantic = json.loads(semantic_in.read_text(encoding="utf-8-sig"))

    if semantic is None:
        semantic = create_semantic_payload(load_problem_data(from_file, args.problem_in))

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
