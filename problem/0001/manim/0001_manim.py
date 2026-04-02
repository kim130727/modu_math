import argparse
import json
from pathlib import Path
from xml.sax.saxutils import escape

from manim import *


PROBLEM_JSON = r"""
{
  "id": 1,
  "type": "fill_in_blank",
  "category": "time_conversion",
  "instruction": "□안에 알맞은 수를 구하시오.",
  "question": {
    "left_seconds": 410,
    "minutes": 6,
    "blank_symbol": "□",
    "unit_from": "초",
    "unit_mid": "분",
    "unit_to": "초"
  },
  "answer": 50
}
"""


def load_problem_data() -> dict:
    return json.loads(PROBLEM_JSON)


def build_expression(data: dict) -> str:
    q = data["question"]
    return (
        f'{q["left_seconds"]}{q["unit_from"]}='
        f'{q["minutes"]}{q["unit_mid"]} '
        f'{q["blank_symbol"]}{q["unit_to"]}'
    )


def create_semantic_payload(data: dict) -> dict:
    return {
        "meta": {
            "schema": "modu_math.semantic.v1",
            "problem_id": f'{data["id"]:04d}',
            "source": "problem/0001/manim/0001_manim.py",
        },
        "problem": data,
        "canvas": {
            "width": 1280,
            "height": 720,
            "background": "#F6F6F6",
        },
        "elements": [
            {
                "id": "instruction",
                "type": "text",
                "text": data["instruction"],
                "x": 72,
                "y": 92,
                "anchor": "start",
                "font_family": "Malgun Gothic",
                "font_size": 42,
                "fill": "#000000",
            },
            {
                "id": "question_box",
                "type": "rect",
                "x": 280,
                "y": 240,
                "width": 720,
                "height": 180,
                "rx": 24,
                "stroke": "#000000",
                "stroke_width": 3,
                "fill": "none",
            },
            {
                "id": "expression",
                "type": "text",
                "text": build_expression(data),
                "x": 640,
                "y": 345,
                "anchor": "middle",
                "font_family": "Malgun Gothic",
                "font_size": 54,
                "fill": "#000000",
            },
            {
                "id": "left_paren",
                "type": "text",
                "text": "(",
                "x": 780,
                "y": 560,
                "anchor": "middle",
                "font_family": "Malgun Gothic",
                "font_size": 56,
                "fill": "#000000",
            },
            {
                "id": "right_paren",
                "type": "text",
                "text": ")",
                "x": 960,
                "y": 560,
                "anchor": "middle",
                "font_family": "Malgun Gothic",
                "font_size": 56,
                "fill": "#000000",
            },
        ],
    }


def write_semantic_json(out_path: Path, payload: dict) -> Path:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return out_path


def render_svg_from_semantic(semantic: dict, svg_path: Path) -> Path:
    canvas = semantic["canvas"]
    elements = semantic["elements"]

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        (
            f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'width="{canvas["width"]}" height="{canvas["height"]}" '
            f'viewBox="0 0 {canvas["width"]} {canvas["height"]}">'
        ),
        (
            f'  <rect x="0" y="0" width="{canvas["width"]}" '
            f'height="{canvas["height"]}" fill="{canvas["background"]}" />'
        ),
    ]

    for element in elements:
        if element["type"] == "rect":
            lines.append(
                (
                    f'  <rect id="{escape(element["id"])}" x="{element["x"]}" y="{element["y"]}" '
                    f'width="{element["width"]}" height="{element["height"]}" rx="{element.get("rx", 0)}" '
                    f'stroke="{element.get("stroke", "none")}" stroke-width="{element.get("stroke_width", 0)}" '
                    f'fill="{element.get("fill", "none")}" />'
                )
            )
        elif element["type"] == "text":
            text = escape(element["text"])
            anchor = escape(element.get("anchor", "start"))
            family = escape(element.get("font_family", "sans-serif"))
            lines.append(
                (
                    f'  <text id="{escape(element["id"])}" x="{element["x"]}" y="{element["y"]}" '
                    f'font-family="{family}" font-size="{element["font_size"]}" '
                    f'fill="{element.get("fill", "#000000")}" text-anchor="{anchor}">{text}</text>'
                )
            )

    lines.append("</svg>")

    svg_path.parent.mkdir(parents=True, exist_ok=True)
    svg_path.write_text("\n".join(lines), encoding="utf-8")
    return svg_path


def default_paths() -> tuple[Path, Path]:
    problem_dir = Path(__file__).resolve().parents[1]
    json_path = problem_dir / "json" / "semantic.json"
    svg_path = problem_dir / "svg" / "semantic.svg"
    return json_path, svg_path


def run_cli() -> None:
    parser = argparse.ArgumentParser(
        description="Generate semantic.json and render SVG from embedded problem data."
    )
    parser.add_argument(
        "--export-semantic",
        action="store_true",
        help="Create semantic JSON file",
    )
    parser.add_argument(
        "--render-svg",
        action="store_true",
        help="Render SVG from semantic JSON",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run both semantic export and SVG rendering",
    )
    parser.add_argument(
        "--semantic-out",
        type=Path,
        help="Output path for semantic JSON",
    )
    parser.add_argument(
        "--svg-out",
        type=Path,
        help="Output path for SVG",
    )
    parser.add_argument(
        "--semantic-in",
        type=Path,
        help="Input semantic JSON path for SVG rendering (defaults to semantic-out path)",
    )

    args = parser.parse_args()
    do_export = args.export_semantic or args.all
    do_render = args.render_svg or args.all

    if not do_export and not do_render:
        parser.print_help()
        return

    default_json_path, default_svg_path = default_paths()
    semantic_out = args.semantic_out or default_json_path
    svg_out = args.svg_out or default_svg_path
    semantic_in = args.semantic_in or semantic_out

    if do_export:
        payload = create_semantic_payload(load_problem_data())
        out = write_semantic_json(semantic_out, payload)
        print(f"[OK] semantic json created: {out}")

    if do_render:
        if semantic_in.exists():
            semantic = json.loads(semantic_in.read_text(encoding="utf-8"))
        else:
            semantic = create_semantic_payload(load_problem_data())
            write_semantic_json(semantic_out, semantic)
            print(f"[OK] semantic json auto-created: {semantic_out}")

        svg = render_svg_from_semantic(semantic, svg_out)
        print(f"[OK] svg rendered: {svg}")


class TimeConversionProblem(Scene):
    def construct(self):
        data = load_problem_data()

        # 1) 배경
        self.camera.background_color = "#F6F6F6"

        # 2) 상단 지시문
        instruction_text = Text(
            data["instruction"],
            font="Malgun Gothic",
            font_size=28,
            color=BLACK,
        )
        instruction_text.to_edge(UP, buff=0.5).to_edge(LEFT, buff=0.4)

        # 3) 문제 박스
        box = RoundedRectangle(
            corner_radius=0.25,
            width=7.5,
            height=2.0,
            stroke_color=BLACK,
            stroke_width=1.5,
            fill_opacity=0,
        )
        box.move_to(ORIGIN + DOWN * 0.1)

        expr = build_expression(data)
        expr_text = Text(
            expr,
            font="Malgun Gothic",
            font_size=34,
            color=BLACK,
        )
        expr_text.move_to(box.get_center())

        # 4) 아래 괄호(정답 작성 칸)
        left_paren = Text("(", font="Malgun Gothic", font_size=34, color=BLACK)
        right_paren = Text(")", font="Malgun Gothic", font_size=34, color=BLACK)
        left_paren.move_to(DOWN * 2.2 + RIGHT * 1.5)
        right_paren.move_to(DOWN * 2.2 + RIGHT * 4.9)

        # 5) 화면 표시
        self.add(instruction_text, box, expr_text, left_paren, right_paren)
        self.wait(2)


if __name__ == "__main__":
    run_cli()
