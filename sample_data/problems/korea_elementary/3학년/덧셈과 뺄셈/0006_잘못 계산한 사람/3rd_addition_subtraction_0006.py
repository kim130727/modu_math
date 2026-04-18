from pathlib import Path
import sys

from modu_semantic import Problem, Rect, Region, Text

CANVAS_W = 767
CANVAS_H = 276
PROBLEM_ID = "3rd_addition_subtraction_0006"

INSTRUCTION_TEXT = "지은이와 건우가 875-328을 계산한 방법을 대화로 나타낸 것입니다. 잘못 계산한 사람과 이유를 쓰세요."
JI_EUN_TEXT = "• 지은: 800에서 300을 빼고, 75에서 28을 뺀 다음 두 결과를 더했어."
GEON_U_TEXT = "• 건우: 800에서 300을 빼고 75에서 30을 뺀 다음 2를 빼서 결과를 더했어."


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
    p = Problem(width=CANVAS_W, height=CANVAS_H, problem_id=PROBLEM_ID, problem_type="find_wrong_reason")
    p.title = "잘못 계산한 사람"
    p.set_domain(
        {
            "expression": "875-328",
            "wrong_person": "건우",
            "reason": "75-28에서 30을 빼면 2를 더해야 하는데 2를 뺐다.",
        }
    )
    p.set_answer(blanks=[], choices=[], answer_key=[{"target": "answer_text", "value": "건우, 30으로 바꾸면 2를 더해야 하는데 뺐다."}])

    r = Region(id="root", x=0, y=0, width=CANVAS_W, height=CANVAS_H, visible_debug=False)
    r.add(Rect(id="bg", x=0, y=0, width=CANVAS_W, height=CANVAS_H, fill="#FFFFFF", stroke="none", stroke_width=0))

    instruction_lines = _wrap_text_by_width(INSTRUCTION_TEXT, font_size=17, max_width=CANVAS_W - 20)
    for i, line in enumerate(instruction_lines, start=1):
        r.add(Text(id=f"i{i}", x=6, y=34 + ((i - 1) * 28), text=line, font_size=17, font_family="Malgun Gothic", fill="#222222"))

    bubble_y = 98
    r.add(Rect(id="bubble", x=14, y=bubble_y, width=740, height=116, fill="none", stroke="#666666", stroke_width=1.5, rx=10, ry=10))
    r.add(Text(id="jy", x=24, y=bubble_y + 34, text=JI_EUN_TEXT, font_size=17, font_family="Malgun Gothic", fill="#222222"))
    r.add(Text(id="gw", x=24, y=bubble_y + 76, text=GEON_U_TEXT, font_size=17, font_family="Malgun Gothic", fill="#222222"))

    r.add(Rect(id="answer_text", x=400, y=CANVAS_H - 40, width=350, height=30, fill="none", stroke="none", stroke_width=0, semantic_role="answer_anchor"))
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
        answer_overrides={
            "use_answer_label": True,
            "answer_label_font_size": 17,
            "answer_label_x": 754,
            "answer_label_y": 242,
            "answer_label_top_right": False,
        },
    )
    print("[3rd_addition_subtraction_0006] generated:")
    print(f"  - {outputs['svg']}")
    print(f"  - {outputs['answer_svg']}")
