from pathlib import Path
import sys

from modu_semantic import Problem, Rect, Region, Text

CANVAS_W = 400
CANVAS_H = 180
PROBLEM_ID = "3rd_shape2d_0009"
PROBLEM_TYPE = "clock_right_angle_time"
TITLE_TEXT = "시계와 직각"
INSTRUCTION_TEXT = "시계의 긴바늘과 짧은바늘이 이루는 각이 직각인 시각은 언제인가요?"


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
    p.set_domain({"instruction": INSTRUCTION_TEXT, "choices": ["2시", "6시", "9시", "10시", "11시"], "correct": "③"})
    p.set_answer(blanks=[], choices=[], answer_key=[{"target": "answer_text", "value": "③"}])

    r = Region(id="root", x=0, y=0, width=CANVAS_W, height=CANVAS_H, visible_debug=False)
    r.add(Rect(id="bg", x=0, y=0, width=CANVAS_W, height=CANVAS_H, fill="#F4F4F4", stroke="none", stroke_width=0))
    lines = _wrap_text_by_width(INSTRUCTION_TEXT, font_size=17, max_width=CANVAS_W - 16)
    for i, line in enumerate(lines, start=1):
        r.add(Text(id=f"i{i}", x=4, y=34 + ((i - 1) * 30), text=line, font_size=17, font_family="Malgun Gothic", fill="#222222"))
    r.add(Text(id="c1", x=4, y=106, text="① 2시", font_size=17, font_family="Malgun Gothic", fill="#222222"))
    r.add(Text(id="c2", x=112, y=106, text="② 6시", font_size=17, font_family="Malgun Gothic", fill="#222222"))
    r.add(Text(id="c3", x=224, y=106, text="③ 9시", font_size=17, font_family="Malgun Gothic", fill="#222222"))
    r.add(Text(id="c4", x=4, y=148, text="④ 10시", font_size=17, font_family="Malgun Gothic", fill="#222222"))
    r.add(Text(id="c5", x=112, y=148, text="⑤ 11시", font_size=17, font_family="Malgun Gothic", fill="#222222"))

    r.add(Rect(id="answer_text", x=348, y=146, width=44, height=28, fill="none", stroke="none", stroke_width=0, semantic_role="answer_anchor"))
    p.add(r)
    return p


CURRENT_DIR = Path(__file__).resolve().parent
PARENT_DIR = CURRENT_DIR.parent
if str(PARENT_DIR) not in sys.path:
    sys.path.insert(0, str(PARENT_DIR))
from _problem_runner import save_built_problem_outputs

if __name__ == "__main__":
    outputs = save_built_problem_outputs(
        build(),
        CURRENT_DIR,
        PROBLEM_ID,
        answer_overrides={"use_answer_label": True, "answer_label_font_size": 28, "answer_label_x": 390, "answer_label_y": 144, "answer_label_top_right": False},
    )
    print("[3rd_shape2d_0009] generated:")
    print(f"  - {outputs['svg']}")
    print(f"  - {outputs['answer_svg']}")
