from pathlib import Path
import sys

from modu_semantic import Problem, Rect, Region, Text
from modu_semantic.recipes import dataframe_table

CANVAS_W = 767
CANVAS_H = 231
PROBLEM_ID = "3rd_addition_subtraction_0007"
INSTRUCTION_TEXT = "주득이네 학교 3학년 학생을 청팀과 백팀으로 나누어 콩주머니 던지기 경기를 했습니다. 청팀과 백팀 중 어느 쪽이 콩주머니를 몇 개 더 넣었는지 식과 답을 구하시오."


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
    p = Problem(width=CANVAS_W, height=CANVAS_H, problem_id=PROBLEM_ID, problem_type="table_compare_totals")
    p.title = "팀별 합계 비교"
    p.set_domain({"cheong_total": 342, "baek_total": 351, "difference": 9, "winner": "백팀"})
    p.set_answer(blanks=[], choices=[], answer_key=[{"target": "answer_text", "value": "백팀 9개"}])

    r = Region(id="root", x=0, y=0, width=CANVAS_W, height=CANVAS_H, visible_debug=False)
    r.add(Rect(id="bg", x=0, y=0, width=CANVAS_W, height=CANVAS_H, fill="#FFFFFF", stroke="none", stroke_width=0))
    lines = _wrap_text_by_width(INSTRUCTION_TEXT, font_size=17, max_width=CANVAS_W - 18)
    for i, line in enumerate(lines, start=1):
        r.add(
            Text(
                id=f"t{i}",
                x=6,
                y=34 + ((i - 1) * 28),
                text=line,
                font_size=17,
                font_family="Malgun Gothic",
                fill="#222222",
            )
        )

    table_items = dataframe_table(
        "team_table",
        188,
        124,
        index=["남학생", "여학생"],
        columns=["청팀", "백팀"],
        data=[["174개", "195개"], ["168개", "156개"]],
        index_col_width=120,
        column_widths=[122, 122],
        row_height=34,
        corner_header="구분",
        font_size=17,
        font_family="Malgun Gothic",
    )
    for item in table_items:
        r.add(item)

    r.add(Rect(id="answer_text", x=560, y=200, width=190, height=26, fill="none", stroke="none", stroke_width=0, semantic_role="answer_anchor"))
    p.add(r)
    return p


CURRENT_DIR = Path(__file__).resolve().parent
PARENT_DIR = CURRENT_DIR.parent
if str(PARENT_DIR) not in sys.path:
    sys.path.insert(0, str(PARENT_DIR))
from _problem_runner import save_built_problem_outputs

if __name__ == "__main__":
    outputs = save_built_problem_outputs(build(), CURRENT_DIR, PROBLEM_ID, answer_overrides={"use_answer_label": True, "answer_label_font_size": 20, "answer_label_x": 750, "answer_label_y": 198, "answer_label_top_right": False})
    print("[3rd_addition_subtraction_0007] generated:")
    print(f"  - {outputs['svg']}")
    print(f"  - {outputs['answer_svg']}")
