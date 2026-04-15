from pathlib import Path
import sys

from modu_semantic import Line, Problem, Polygon, Rect, Region, Text

CANVAS_W = 400
CANVAS_H = 260
PROBLEM_ID = "3rd_shape2d_0008"
PROBLEM_TYPE = "count_rectangles_vs_squares"
TITLE_TEXT = "직사각형과 정사각형"
INSTRUCTION_TEXT = "직사각형은 정사각형보다 몇 개 더 많은지 구하세요."


def _diamond(cx: float, cy: float, w: float, h: float) -> list[tuple[float, float]]:
    return [(cx, cy - h / 2), (cx + w / 2, cy), (cx, cy + h / 2), (cx - w / 2, cy)]


def build() -> Problem:
    p = Problem(width=CANVAS_W, height=CANVAS_H, problem_id=PROBLEM_ID, problem_type=PROBLEM_TYPE)
    p.title = TITLE_TEXT
    p.set_domain({"instruction": INSTRUCTION_TEXT, "rectangle_count": 2, "square_count": 2, "difference": 0})
    p.set_answer(blanks=[], choices=[], answer_key=[{"target": "answer_value", "value": "0"}])

    r = Region(id="root", x=0, y=0, width=CANVAS_W, height=CANVAS_H, visible_debug=False)
    r.add(Rect(id="bg", x=0, y=0, width=CANVAS_W, height=CANVAS_H, fill="#F4F4F4", stroke="none", stroke_width=0))
    r.add(Text(id="i1", x=4, y=34, text=INSTRUCTION_TEXT, font_size=17, font_family="Malgun Gothic", fill="#222222"))

    r.add(Rect(id="frame", x=6, y=52, width=384, height=194, fill="none", stroke="#8A8A8A", stroke_width=1.4, rx=10, ry=10))

    r.add(Polygon(id="ga", points=[(26, 69), (106, 67), (84, 108), (36, 120)], fill="none", stroke="#4A4A4A", stroke_width=2.0))
    r.add(Text(id="ga_t", x=58, y=96, text="가", font_size=32, font_family="Malgun Gothic", fill="#222222", anchor="middle"))

    r.add(Rect(id="na", x=162, y=66, width=64, height=64, fill="none", stroke="#4A4A4A", stroke_width=2.0))
    r.add(Text(id="na_t", x=194, y=106, text="나", font_size=32, font_family="Malgun Gothic", fill="#222222", anchor="middle"))

    r.add(Rect(id="da", x=284, y=77, width=80, height=52, fill="none", stroke="#4A4A4A", stroke_width=2.0, metadata={"transform": "rotate(-35 324 103)"}))
    r.add(Text(id="da_t", x=324, y=106, text="다", font_size=32, font_family="Malgun Gothic", fill="#222222", anchor="middle"))

    r.add(Polygon(id="ra", points=_diamond(56, 170, 88, 72), fill="none", stroke="#4A4A4A", stroke_width=2.0))
    r.add(Text(id="ra_t", x=56, y=184, text="라", font_size=32, font_family="Malgun Gothic", fill="#222222", anchor="middle"))

    r.add(Rect(id="ma", x=136, y=154, width=116, height=42, fill="none", stroke="#4A4A4A", stroke_width=2.0))
    r.add(Text(id="ma_t", x=194, y=184, text="마", font_size=32, font_family="Malgun Gothic", fill="#222222", anchor="middle"))

    r.add(Polygon(id="ba", points=_diamond(328, 174, 86, 48), fill="none", stroke="#4A4A4A", stroke_width=2.0))
    r.add(Text(id="ba_t", x=328, y=186, text="바", font_size=32, font_family="Malgun Gothic", fill="#222222", anchor="middle"))

    r.add(Rect(id="answer_value", x=304, y=212, width=48, height=28, fill="none", stroke="none", stroke_width=0, semantic_role="answer_anchor"))
    p.add(r)
    return p


CURRENT_DIR = Path(__file__).resolve().parent
PARENT_DIR = CURRENT_DIR.parent
if str(PARENT_DIR) not in sys.path:
    sys.path.insert(0, str(PARENT_DIR))
from _problem_runner import save_built_problem_outputs

if __name__ == "__main__":
    outputs = save_built_problem_outputs(build(), CURRENT_DIR, PROBLEM_ID, answer_overrides={"answer_overlay_numeric_font_size": 30})
    print("[3rd_shape2d_0008] generated:")
    print(f"  - {outputs['svg']}")
    print(f"  - {outputs['answer_svg']}")
