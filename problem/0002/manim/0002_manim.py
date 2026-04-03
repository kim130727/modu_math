from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from manim import *


def _ensure_repo_root_on_path() -> None:
    """
    Add repository root to sys.path so shared modules can be imported reliably.

    This keeps script execution stable on Windows regardless of current working
    directory (for example when launched from IDE or terminal in another path).
    """
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / "problem").is_dir() and (parent / "README.md").exists():
            root = str(parent)
            if root not in sys.path:
                sys.path.insert(0, root)
            return
    raise RuntimeError("Repository root could not be resolved from current file path.")


_ensure_repo_root_on_path()

from problem.common.paths import find_problem_dir, semantic_json_path, semantic_svg_path
from problem.common.svg_renderer import render_svg_from_semantic
from problem.common.validator import validate_semantic


def _configure_manim_output_dirs() -> None:
    """
    Keep all Manim artifacts inside this problem folder.

    Why:
    - Prevents writes to repository-level `media/`
    - Makes per-problem review/debugging easier (`problem/{id}/manim/*`)
    """
    problem_dir = find_problem_dir(Path(__file__))
    manim_dir = problem_dir / "manim"
    cache_dir = manim_dir / "cache"

    config.media_dir = str(manim_dir)
    config.images_dir = str(manim_dir / "images")
    config.video_dir = str(manim_dir / "videos")
    # Avoid creating a visible top-level `texts/` folder in manim output root.
    config.text_dir = str(cache_dir / "text")
    config.tex_dir = str(cache_dir / "tex")
    config.partial_movie_dir = str(cache_dir / "partial_movie_files")


_configure_manim_output_dirs()


PROBLEM_JSON = r"""
{
  "id": 2,
  "type": "measure_length_with_ruler",
  "instruction": "2. 지우개의 길이는 몇 mm입니까?",
  "sub_instruction": "(* 눈금을 잘 보아야 해요)",
  "object_label": "지우개",
  "ruler": {
    "start_cm": 2,
    "end_cm": 5,
    "major_ticks": [2, 3, 4, 5],
    "minor_per_cm": 10
  },
  "measurement": {
    "left_cm": 3.0,
    "right_cm": 4.6
  },
  "answer_mm": 16
}
"""


def load_problem_data() -> dict:
    return json.loads(PROBLEM_JSON)


def build_layout(data: dict) -> dict:
    """
    Build all geometric values in one place.

    Why: this centralizes coordinates so Manim and SVG consume one source of
    truth instead of maintaining duplicated hard-coded positions.
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

    layout = {
        "canvas": canvas,
        "title": {
            "x": 72,
            "y": 80,
        },
        "subtitle": {
            "x": 72,
            "y": 128,
        },
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
        "numbers": {
            "y": ruler["y"] + ruler["height"] - 38,
        },
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
    return layout


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
            }
        )

    return {
        "meta": {
            "schema": "modu_math.semantic.v1",
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
    errors = validate_semantic(semantic)
    if errors:
        issue_text = "\n".join(f"- {error}" for error in errors)
        raise ValueError(f"Semantic validation failed:\n{issue_text}")


def _px_to_scene_x(x: float, canvas_width: float) -> float:
    return (x / canvas_width - 0.5) * config.frame_width


def _px_to_scene_y(y: float, canvas_height: float) -> float:
    return (0.5 - y / canvas_height) * config.frame_height


def _px_to_scene_w(width: float, canvas_width: float) -> float:
    return width / canvas_width * config.frame_width


def _px_to_scene_h(height: float, canvas_height: float) -> float:
    return height / canvas_height * config.frame_height


def render_manim_from_semantic(scene: Scene, semantic: dict) -> None:
    """
    Render Manim objects from semantic elements.

    This enables the gradual transition to "semantic-first" where the scene no
    longer owns layout constants directly.
    """
    canvas = semantic["canvas"]
    scene.camera.background_color = canvas["background"]

    for element in semantic["elements"]:
        manim_obj = _element_to_mobject(element, canvas)
        if manim_obj is not None:
            scene.add(manim_obj)


def _element_to_mobject(element: dict, canvas: dict) -> Mobject | None:
    elem_type = element["type"]

    if elem_type == "text":
        return _build_text_mobject(element, canvas)

    if elem_type == "rect":
        return _build_rect_mobject(element, canvas)

    if elem_type == "line":
        return _build_line_mobject(element, canvas)

    return None


def _build_text_mobject(element: dict, canvas: dict) -> Text:
    font_weight = element.get("font_weight", "normal").lower()
    weight = BOLD if font_weight == "bold" else NORMAL

    text = Text(
        element["text"],
        font=element.get("font_family", "Malgun Gothic"),
        font_size=element.get("font_size", 24),
        color=element.get("fill", "#000000"),
        weight=weight,
    )

    x = _px_to_scene_x(float(element["x"]), float(canvas["width"]))
    y = _px_to_scene_y(float(element["y"]), float(canvas["height"]))

    anchor = element.get("anchor", "middle")
    text.move_to([x, y, 0])

    if anchor == "start":
        # In semantic SVG, start anchor means x is the left text edge.
        text.set_x(x + text.width / 2)

    return text


def _build_rect_mobject(element: dict, canvas: dict) -> Mobject:
    width = _px_to_scene_w(float(element["width"]), float(canvas["width"]))
    height = _px_to_scene_h(float(element["height"]), float(canvas["height"]))
    x = _px_to_scene_x(float(element["x"]), float(canvas["width"])) + width / 2
    y = _px_to_scene_y(float(element["y"]), float(canvas["height"])) - height / 2

    stroke_color = element.get("stroke", "#000000")
    stroke_width = float(element.get("stroke_width", 1))
    fill = element.get("fill", "none")

    if float(element.get("rx", 0)) > 0:
        corner_radius = _px_to_scene_w(float(element.get("rx", 0)), float(canvas["width"]))
        shape: Mobject = RoundedRectangle(
            corner_radius=corner_radius,
            width=width,
            height=height,
            stroke_color=stroke_color,
            stroke_width=stroke_width,
            fill_color=fill if fill != "none" else stroke_color,
            fill_opacity=1.0 if fill != "none" else 0.0,
        )
    else:
        shape = Rectangle(
            width=width,
            height=height,
            stroke_color=stroke_color,
            stroke_width=stroke_width,
            fill_color=fill if fill != "none" else stroke_color,
            fill_opacity=1.0 if fill != "none" else 0.0,
        )

    shape.move_to([x, y, 0])
    return shape


def _build_line_mobject(element: dict, canvas: dict) -> Mobject:
    start = [
        _px_to_scene_x(float(element["x1"]), float(canvas["width"])),
        _px_to_scene_y(float(element["y1"]), float(canvas["height"])),
        0,
    ]
    end = [
        _px_to_scene_x(float(element["x2"]), float(canvas["width"])),
        _px_to_scene_y(float(element["y2"]), float(canvas["height"])),
        0,
    ]

    color = element.get("stroke", "#000000")
    stroke_width = float(element.get("stroke_width", 1))

    dasharray = element.get("dasharray")
    if dasharray:
        first_dash_px = float(str(dasharray).split()[0])
        dash_length = _px_to_scene_w(first_dash_px, float(canvas["width"]))
        return DashedLine(
            start=start,
            end=end,
            color=color,
            stroke_width=stroke_width,
            dash_length=max(0.03, dash_length),
        )

    return Line(start=start, end=end, color=color, stroke_width=stroke_width)


def run_cli() -> None:
    parser = argparse.ArgumentParser(
        description="Generate semantic.json, validate semantic payload, and render SVG."
    )
    parser.add_argument("--export-semantic", action="store_true", help="Create semantic JSON file")
    parser.add_argument("--render-svg", action="store_true", help="Render SVG from semantic JSON")
    parser.add_argument("--validate", action="store_true", help="Validate semantic payload only")
    parser.add_argument("--all", action="store_true", help="Run export + validate + render")
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
    if semantic_in.exists():
        semantic = json.loads(semantic_in.read_text(encoding="utf-8"))

    if semantic is None:
        semantic = create_semantic_payload(load_problem_data())

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
