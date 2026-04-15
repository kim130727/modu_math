from pathlib import Path
import sys

from modu_semantic import Problem, Rect, Region, Text
from modu_semantic.recipes import add_point_segment_graph

CANVAS_W = 400
CANVAS_H = 220
PROBLEM_ID = "3rd_shape2d_0006"
PROBLEM_TYPE = "count_right_angles_from_rays"
TITLE_TEXT = "직각 개수 세기"
INSTRUCTION_TEXT = "다음 도형에서 찾을 수 있는 직각은 모두 몇 개인지 구하세요."


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
    p.set_domain({"instruction": INSTRUCTION_TEXT, "right_angle_count": 3})
    p.set_answer(blanks=[], choices=[], answer_key=[{"target": "answer_value", "value": "3"}])

    r = Region(id="root", x=0, y=0, width=CANVAS_W, height=CANVAS_H, visible_debug=False)
    r.add(Rect(id="bg", x=0, y=0, width=CANVAS_W, height=CANVAS_H, fill="#F4F4F4", stroke="none", stroke_width=0))

    lines = _wrap_text_by_width(INSTRUCTION_TEXT, font_size=17, max_width=392)
    for i, line in enumerate(lines, start=1):
        r.add(Text(id=f"i{i}", x=4, y=34 + ((i - 1) * 30), text=line, font_size=17, font_family="Malgun Gothic", fill="#222222"))

    points = {
        "C": (202, 134),
        "R1": (147, 134),
        "R2": (146, 78),
        "R3": (258, 78),
        "R4": (303, 170),
        "R5": (204, 210),
        "R6": (146, 186),
    }
    segments = [("C", "R1"), ("C", "R2"), ("C", "R3"), ("C", "R4"), ("C", "R5"), ("C", "R6")]
    add_point_segment_graph(
        r,
        points=points,
        segments=segments,
        id_prefix="ray_graph",
        segment_stroke="#4A4A4A",
        segment_stroke_width=2.0,
        segment_semantic_role="shape",
        show_points=False,
        show_labels=False,
        highlighted_points=["C"],
        highlight_radius=5.0,
        highlight_stroke="#4A4A4A",
        highlight_stroke_width=1.2,
    )

    r.add(Rect(id="answer_value", x=344, y=186, width=48, height=28, fill="none", stroke="none", stroke_width=0, semantic_role="answer_anchor"))
    p.add(r)
    return p


CURRENT_DIR = Path(__file__).resolve().parent
PARENT_DIR = CURRENT_DIR.parent
if str(PARENT_DIR) not in sys.path:
    sys.path.insert(0, str(PARENT_DIR))
from _problem_runner import save_built_problem_outputs

if __name__ == "__main__":
    outputs = save_built_problem_outputs(build(), CURRENT_DIR, PROBLEM_ID, answer_overrides={"answer_overlay_numeric_font_size": 30})
    print("[3rd_shape2d_0006] generated:")
    print(f"  - {outputs['svg']}")
    print(f"  - {outputs['answer_svg']}")
