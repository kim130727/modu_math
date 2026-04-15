from pathlib import Path
import sys

from modu_semantic import Line, Problem, Rect, Region, Text

CANVAS_W = 400
CANVAS_H = 210
PROBLEM_ID = "3rd_shape2d_0010"
PROBLEM_TYPE = "count_rectangles_in_figure"
TITLE_TEXT = "직사각형 개수"
INSTRUCTION_TEXT = "다음 도형에서 찾을 수 있는 크고 작은 직사각형은 모두 몇 개인지 구하세요."


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
    p.set_domain(
        {
            "instruction": INSTRUCTION_TEXT,
            "rectangle_count": 12,
            "counting_rule": "분할선 간 폭을 환산한 칸수 기준",
            "x_segments": {
                "x0_x1": 1,
                "x1_x2": 1,
                "x2_x3": 3,
            },
            "y_segments": {
                "y0_y1": 1,
                "y1_y2": 1,
            },
            "example": {
                "x1_x3_y0_y2": 3,
                "x0_x3_y0_y2": 5,
            },
        }
    )
    p.set_answer(blanks=[], choices=[], answer_key=[{"target": "answer_value", "value": "12"}])

    r = Region(id="root", x=0, y=0, width=CANVAS_W, height=CANVAS_H, visible_debug=False)
    r.add(Rect(id="bg", x=0, y=0, width=CANVAS_W, height=CANVAS_H, fill="#F4F4F4", stroke="none", stroke_width=0))

    lines = _wrap_text_by_width(INSTRUCTION_TEXT, font_size=17, max_width=392)
    for i, line in enumerate(lines, start=1):
        r.add(Text(id=f"i{i}", x=4, y=34 + ((i - 1) * 30), text=line, font_size=17, font_family="Malgun Gothic", fill="#222222"))

    x0, y0 = 148, 104
    w, h = 126, 96
    x1 = x0 + 42
    x2 = x0 + 76
    y1 = y0 + 48

    r.add(Rect(id="outer", x=x0, y=y0, width=w, height=h, fill="none", stroke="#4A4A4A", stroke_width=2.0))
    r.add(Line(id="v1", x1=x1, y1=y0, x2=x1, y2=y0 + h, stroke="#4A4A4A", stroke_width=2.0))
    r.add(Line(id="v2", x1=x2, y1=y0, x2=x2, y2=y0 + h, stroke="#4A4A4A", stroke_width=2.0))
    r.add(Line(id="h1", x1=x0, y1=y1, x2=x2, y2=y1, stroke="#4A4A4A", stroke_width=2.0))

    r.add(Rect(id="answer_value", x=336, y=176, width=56, height=28, fill="none", stroke="none", stroke_width=0, semantic_role="answer_anchor"))
    p.add(r)
    return p


CURRENT_DIR = Path(__file__).resolve().parent
PARENT_DIR = CURRENT_DIR.parent
if str(PARENT_DIR) not in sys.path:
    sys.path.insert(0, str(PARENT_DIR))
from _problem_runner import save_built_problem_outputs

if __name__ == "__main__":
    outputs = save_built_problem_outputs(build(), CURRENT_DIR, PROBLEM_ID, answer_overrides={"answer_overlay_numeric_font_size": 30})
    print("[3rd_shape2d_0010] generated:")
    print(f"  - {outputs['svg']}")
    print(f"  - {outputs['answer_svg']}")
