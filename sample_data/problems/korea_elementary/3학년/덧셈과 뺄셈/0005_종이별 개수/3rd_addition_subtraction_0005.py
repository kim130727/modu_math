from pathlib import Path
import sys

from modu_semantic import Problem, Rect, Region, Text

CANVAS_W = 767
CANVAS_H = 162
PROBLEM_ID = "3rd_addition_subtraction_0005"
INSTRUCTION_TEXT = "소희는 종이별을 399개 접었고, 은별이는 소희보다 115개만큼 더 많이 접었습니다. 두 사람이 접은 종이별은 모두 몇 개인지 식과 답을 구하시오."


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
    p = Problem(width=CANVAS_W, height=CANVAS_H, problem_id=PROBLEM_ID, problem_type="word_problem_total")
    p.title = "종이별 개수"
    p.set_domain({"sohui": 399, "eunbyeol_more": 115, "total": 913})
    p.set_answer(blanks=[], choices=[], answer_key=[{"target": "answer_total", "value": "913"}])

    r = Region(id="root", x=0, y=0, width=CANVAS_W, height=CANVAS_H, visible_debug=False)
    r.add(Rect(id="bg", x=0, y=0, width=CANVAS_W, height=CANVAS_H, fill="#FFFFFF", stroke="none", stroke_width=0))

    lines = _wrap_text_by_width(INSTRUCTION_TEXT, font_size=17, max_width=CANVAS_W - 28)
    for i, line in enumerate(lines, start=1):
        r.add(Text(id=f"t{i}", x=8, y=32 + ((i - 1) * 28), text=line, font_size=17, font_family="Malgun Gothic", fill="#222222"))

    r.add(Rect(id="answer_total", x=CANVAS_W - 78, y=CANVAS_H - 42, width=60, height=30, fill="none", stroke="none", stroke_width=0, semantic_role="answer_anchor"))
    p.add(r)
    return p


CURRENT_DIR = Path(__file__).resolve().parent
PARENT_DIR = CURRENT_DIR.parent
if str(PARENT_DIR) not in sys.path:
    sys.path.insert(0, str(PARENT_DIR))
from _problem_runner import save_built_problem_outputs

if __name__ == "__main__":
    outputs = save_built_problem_outputs(build(), CURRENT_DIR, PROBLEM_ID, answer_overrides={"answer_overlay_numeric_font_size": 24})
    print("[3rd_addition_subtraction_0005] generated:")
    print(f"  - {outputs['svg']}")
    print(f"  - {outputs['answer_svg']}")
