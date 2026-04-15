from pathlib import Path
import sys

from modu_semantic import Problem, Rect, Region, Text

CANVAS_W = 408
CANVAS_H = 212

PROBLEM_ID = "3rd_addition_subtraction_0002"
PROBLEM_TYPE = "addition_pick_two_numbers"
TITLE_TEXT = "덧셈식 만들기"
INSTRUCTION_TEXT = "다음 수 중에서 2개를 골라 덧셈식을 만들려고 합니다. □ 안에 알맞은 수를 써넣으세요."


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
            "candidates": [718, 295, 658, 245],
            "target_sum": 953,
            "valid_pair": [295, 658],
        }
    )
    p.set_answer(
        blanks=[],
        choices=[],
        answer_key=[
            {"target": "blank_left", "value": "295"},
            {"target": "blank_right", "value": "658"},
        ],
    )

    root = Region(id="problem_root", x=0, y=0, width=CANVAS_W, height=CANVAS_H, visible_debug=False)
    root.add(Rect(id="bg", x=0, y=0, width=CANVAS_W, height=CANVAS_H, fill="#FFFFFF", stroke="none", stroke_width=0, semantic_role="background"))

    lines = _wrap_text_by_width(INSTRUCTION_TEXT, font_size=17, max_width=396)
    for i, line in enumerate(lines, start=1):
        root.add(Text(id=f"instruction_{i}", x=6, y=30 + ((i - 1) * 30), text=line, font_size=17, font_family="Malgun Gothic", fill="#222222", anchor="start", semantic_role="instruction"))

    root.add(Rect(id="candidate_box", x=6, y=78, width=396, height=56, fill="none", stroke="#666666", stroke_width=1.5, rx=10, ry=10, semantic_role="guide"))
    for idx, value in enumerate((718, 295, 658, 245)):
        root.add(Text(id=f"candidate_{idx+1}", x=74 + (idx * 86), y=113, text=str(value), font_size=17, font_family="Malgun Gothic", fill="#222222", anchor="middle", semantic_role="label"))

    root.add(Rect(id="blank_left", x=94, y=150, width=69, height=36, fill="none", stroke="#666666", stroke_width=1.5, semantic_role="answer_anchor"))
    root.add(Text(id="plus_sign", x=173, y=176, text="+", font_size=34, font_family="Malgun Gothic", fill="#222222", anchor="middle", semantic_role="label"))
    root.add(Rect(id="blank_right", x=184, y=150, width=69, height=36, fill="none", stroke="#666666", stroke_width=1.5, semantic_role="answer_anchor"))
    root.add(Text(id="equal_expr", x=300, y=176, text="=953", font_size=34, font_family="Malgun Gothic", fill="#222222", anchor="middle", semantic_role="label"))

    p.add(root)
    return p


CURRENT_DIR = Path(__file__).resolve().parent
PARENT_DIR = CURRENT_DIR.parent
if str(PARENT_DIR) not in sys.path:
    sys.path.insert(0, str(PARENT_DIR))

from _problem_runner import save_built_problem_outputs


if __name__ == "__main__":
    outputs = save_built_problem_outputs(build(), CURRENT_DIR, PROBLEM_ID, answer_overrides={"answer_overlay_numeric_font_size": 28})
    print("[3rd_addition_subtraction_0002] generated:")
    print(f"  - {outputs['svg']}")
    print(f"  - {outputs['answer_svg']}")
