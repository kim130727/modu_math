from pathlib import Path
import sys

from modu_semantic import Problem, Rect, Region, Text
from modu_semantic.recipes import add_segment_set_by_points

CANVAS_W = 400
CANVAS_H = 230
PROBLEM_ID = "3rd_shape2d_0007"
PROBLEM_TYPE = "count_right_triangles_with_cuts"
TITLE_TEXT = "직각삼각형 개수"
INSTRUCTION_TEXT = "색종이를 점선을 따라 자르면 직각삼각형은 모두 몇 개 만들어지는지 구하세요."


def _wrap_text_by_width(text: str, *, font_size: float, max_width: float) -> list[str]:
    if not text:
        return [""]
    approx_char_w = font_size * 0.92
    max_chars = max(1, int(max_width / approx_char_w))
    words = text.split(" ")
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = word if not current else f"{current} {word}"
        if len(candidate) <= max_chars:
            current = candidate
        else:
            if current:
                lines.append(current)
                current = word
            else:
                for i in range(0, len(word), max_chars):
                    chunk = word[i : i + max_chars]
                    if len(chunk) == max_chars:
                        lines.append(chunk)
                    else:
                        current = chunk
    if current:
        lines.append(current)
    return lines or [text]


def build() -> Problem:
    p = Problem(width=CANVAS_W, height=CANVAS_H, problem_id=PROBLEM_ID, problem_type=PROBLEM_TYPE)
    p.title = TITLE_TEXT
    p.set_domain({"instruction": INSTRUCTION_TEXT, "right_triangle_count": 6})
    p.set_answer(blanks=[], choices=[], answer_key=[{"target": "answer_value", "value": "6"}])

    r = Region(id="root", x=0, y=0, width=CANVAS_W, height=CANVAS_H, visible_debug=False)
    r.add(Rect(id="bg", x=0, y=0, width=CANVAS_W, height=CANVAS_H, fill="#F6F6F6", stroke="none", stroke_width=0))

    lines = _wrap_text_by_width(INSTRUCTION_TEXT, font_size=17, max_width=392)
    for i, line in enumerate(lines, start=1):
        r.add(Text(id=f"i{i}", x=4, y=34 + ((i - 1) * 30), text=line, font_size=17, font_family="Malgun Gothic", fill="#222222"))

    x0, y0 = 110, 82
    w, h = 175, 120
    r.add(Rect(id="paper", x=x0, y=y0, width=w, height=h, fill="#EEF4C8", stroke="#6A6A6A", stroke_width=1.8))

    # 내부 절단선: 공용 점선 선분 템플릿
    add_segment_set_by_points(
        r,
        id_prefix="d",
        segments=[
            ((110.0, 117.2), (226.0, 117.2)),
            ((156.0, 116.9), (156.0, 202.0)),
            ((110.9, 116.9), (156.0, 202.0)),
            ((155.9, 202.0), (225.5, 118.0)),
            ((226.0, 82.0), (285.0, 118.0)),
            ((226.0, 82.0), (226.0, 202.0)),
            ((226.5, 117.4), (285.5, 117.4)),
            ((225.1, 169.7), (285.3, 169.7)),
            ((258.3, 169.7), (258.3, 202.6)),
        ],
        stroke="#7C7C7C",
        stroke_width=1.8,
        semantic_role="guide",
        dashed=True,
        dash_len=6.0,
        gap_len=4.0,
    )

    r.add(Rect(id="answer_value", x=343, y=196, width=48, height=28, fill="none", stroke="none", stroke_width=0, semantic_role="answer_anchor"))
    p.add(r)
    return p


CURRENT_DIR = Path(__file__).resolve().parent
PARENT_DIR = CURRENT_DIR.parent
if str(PARENT_DIR) not in sys.path:
    sys.path.insert(0, str(PARENT_DIR))
from _problem_runner import save_built_problem_outputs

if __name__ == "__main__":
    outputs = save_built_problem_outputs(build(), CURRENT_DIR, PROBLEM_ID, answer_overrides={"answer_overlay_numeric_font_size": 30})
    print("[3rd_shape2d_0007] generated:")
    print(f"  - {outputs['svg']}")
    print(f"  - {outputs['answer_svg']}")
