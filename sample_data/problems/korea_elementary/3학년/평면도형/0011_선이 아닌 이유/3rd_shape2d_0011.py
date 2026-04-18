from pathlib import Path
import sys

from modu_semantic import Line, Problem, Rect, Region, Text

CANVAS_W = 640
CANVAS_H = 190
PROBLEM_ID = "3rd_shape2d_0011"
PROBLEM_TYPE = "why_not_line_segment"
TITLE_TEXT = "선분이 아닌 이유"
INSTRUCTION_TEXT = "다음 도형이 선분이 아닌 이유를 쓰세요."


def _wave_points() -> list[tuple[float, float]]:
    return [
        (252, 112), (272, 96), (290, 92), (307, 104), (326, 126), (344, 136),
        (362, 132), (378, 114), (396, 96), (414, 94), (432, 108), (450, 132),
        (468, 142), (486, 132), (504, 102), (521, 98), (540, 108), (566, 128),
    ]


def _smooth_catmull_rom(points: list[tuple[float, float]], samples_per_seg: int = 10) -> list[tuple[float, float]]:
    if len(points) < 2:
        return points
    out: list[tuple[float, float]] = []
    n = len(points)
    for i in range(n - 1):
        p0 = points[i - 1] if i > 0 else points[i]
        p1 = points[i]
        p2 = points[i + 1]
        p3 = points[i + 2] if i + 2 < n else points[i + 1]
        for s in range(samples_per_seg):
            t = s / samples_per_seg
            t2 = t * t
            t3 = t2 * t
            x = 0.5 * (
                (2 * p1[0])
                + (-p0[0] + p2[0]) * t
                + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2
                + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3
            )
            y = 0.5 * (
                (2 * p1[1])
                + (-p0[1] + p2[1]) * t
                + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2
                + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3
            )
            out.append((x, y))
    out.append(points[-1])
    return out


def build() -> Problem:
    p = Problem(width=CANVAS_W, height=CANVAS_H, problem_id=PROBLEM_ID, problem_type=PROBLEM_TYPE)
    p.title = TITLE_TEXT
    p.set_domain({"instruction": INSTRUCTION_TEXT, "reason": "곧은 선이 아니라 구부러진 선이기 때문이다."})
    p.set_answer(blanks=[], choices=[], answer_key=[{"target": "answer_text", "value": "구부러진 선이어서 선분이 아닙니다."}])

    r = Region(id="root", x=0, y=0, width=CANVAS_W, height=CANVAS_H, visible_debug=False)
    r.add(Rect(id="bg", x=0, y=0, width=CANVAS_W, height=CANVAS_H, fill="#F4F4F4", stroke="none", stroke_width=0))
    r.add(Text(id="i1", x=4, y=34, text=INSTRUCTION_TEXT, font_size=17, font_family="Malgun Gothic", fill="#222222"))

    r.add(Rect(id="frame", x=212, y=66, width=430, height=90, fill="none", stroke="#8A8A8A", stroke_width=1.4, rx=12, ry=12))
    pts = _smooth_catmull_rom(_wave_points(), samples_per_seg=12)
    for i in range(len(pts) - 1):
        r.add(Line(id=f"w{i}", x1=pts[i][0], y1=pts[i][1], x2=pts[i + 1][0], y2=pts[i + 1][1], stroke="#222222", stroke_width=2.2))
    r.add(Rect(id="dot_l", x=250, y=110, width=6, height=6, fill="#222222", stroke="#222222", stroke_width=1, rx=3, ry=3))
    r.add(Rect(id="dot_r", x=564, y=126, width=6, height=6, fill="#222222", stroke="#222222", stroke_width=1, rx=3, ry=3))

    r.add(Rect(id="answer_text", x=430, y=8, width=206, height=28, fill="none", stroke="none", stroke_width=0, semantic_role="answer_anchor"))
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
        answer_overrides={"use_answer_label": True, "answer_label_font_size": 16, "answer_label_x": 638, "answer_label_y": 8, "answer_label_top_right": False},
    )
    print("[3rd_shape2d_0011] generated:")
    print(f"  - {outputs['svg']}")
    print(f"  - {outputs['answer_svg']}")
