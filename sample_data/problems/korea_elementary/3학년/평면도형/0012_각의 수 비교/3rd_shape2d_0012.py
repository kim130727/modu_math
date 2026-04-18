from pathlib import Path
import sys

from modu_semantic import Line, Polygon, Problem, Rect, Region, Text

CANVAS_W = 730
CANVAS_H = 435
PROBLEM_ID = "3rd_shape2d_0012"
PROBLEM_TYPE = "order_by_number_of_angles"
TITLE_TEXT = "각의 수 비교"
INSTRUCTION_TEXT = "각이 많은 도형부터 차례로 기호를 쓰려고 합니다. 풀이 과정을 쓰고 답을 구하세요."


def _sample_cubic_bezier(
    p0: tuple[float, float],
    p1: tuple[float, float],
    p2: tuple[float, float],
    p3: tuple[float, float],
    samples: int = 22,
) -> list[tuple[float, float]]:
    pts: list[tuple[float, float]] = []
    for i in range(samples + 1):
        t = i / samples
        omt = 1.0 - t
        x = (
            (omt * omt * omt * p0[0])
            + (3 * omt * omt * t * p1[0])
            + (3 * omt * t * t * p2[0])
            + (t * t * t * p3[0])
        )
        y = (
            (omt * omt * omt * p0[1])
            + (3 * omt * omt * t * p1[1])
            + (3 * omt * t * t * p2[1])
            + (t * t * t * p3[1])
        )
        pts.append((x, y))
    return pts


def build() -> Problem:
    p = Problem(width=CANVAS_W, height=CANVAS_H, problem_id=PROBLEM_ID, problem_type=PROBLEM_TYPE)
    p.title = TITLE_TEXT
    p.set_domain(
        {
            "instruction": INSTRUCTION_TEXT,
            "angle_counts": {"가": 1, "나": 4, "다": 6, "라": 3},
            "order": ["다", "나", "라", "가"],
            "solution": {
                "angles_text": "가 1개, 나 4개, 다 6개, 라 3개",
                "order_text": "다(6) → 나(4) → 라(3) → 가(1)",
                "final_answer": "다, 나, 라, 가",
            },
        }
    )
    p.set_answer(
        blanks=[],
        choices=[],
        answer_key=[
            {"target": "solution_angles", "value": "가 1개, 나 4개, 다 6개, 라 3개"},
            {"target": "solution_order", "value": "다(6) → 나(4) → 라(3) → 가(1)"},
            {"target": "answer_text", "value": "다, 나, 라, 가"},
        ],
    )

    r = Region(id="root", x=0, y=0, width=CANVAS_W, height=CANVAS_H, visible_debug=False)
    r.add(Rect(id="bg", x=0, y=0, width=CANVAS_W, height=CANVAS_H, fill="#F4F4F4", stroke="none", stroke_width=0))
    r.add(Text(id="i1", x=4, y=34, text=INSTRUCTION_TEXT, font_size=17, font_family="Malgun Gothic", fill="#222222"))

    r.add(Rect(id="frame", x=190, y=58, width=408, height=202, fill="none", stroke="#8A8A8A", stroke_width=1.5, rx=12, ry=12))

    # 가 (피자 조각 모양: 꼭짓점 1개 + 둥근 바깥변)
    r.add(Line(id="ga_edge_1", x1=236, y1=166, x2=292, y2=84, stroke="#303030", stroke_width=2.2))
    r.add(Line(id="ga_edge_2", x1=236, y1=166, x2=342, y2=170, stroke="#303030", stroke_width=2.2))
    arc_pts = _sample_cubic_bezier((292, 84), (342, 88), (362, 150), (342, 170), samples=22)
    for i in range(len(arc_pts) - 1):
        r.add(Line(id=f"ga_arc_{i}", x1=arc_pts[i][0], y1=arc_pts[i][1], x2=arc_pts[i + 1][0], y2=arc_pts[i + 1][1], stroke="#303030", stroke_width=2.2))
    r.add(Text(id="ga_t", x=293, y=128, text="가", font_size=30, font_family="Malgun Gothic", fill="#222222", anchor="middle"))

    # 나 (사다리꼴)
    r.add(Polygon(id="na", points=[(454, 94), (536, 96), (506, 162), (474, 160)], fill="none", stroke="#303030", stroke_width=2.2))
    r.add(Text(id="na_t", x=492, y=132, text="나", font_size=30, font_family="Malgun Gothic", fill="#222222", anchor="middle"))

    # 다 (육각형)
    r.add(Polygon(id="da", points=[(250, 210), (280, 180), (326, 180), (356, 210), (326, 242), (280, 242)], fill="none", stroke="#303030", stroke_width=2.2))
    r.add(Text(id="da_t", x=304, y=224, text="다", font_size=30, font_family="Malgun Gothic", fill="#222222", anchor="middle"))

    # 라 (삼각형)
    r.add(Polygon(id="ra", points=[(398, 192), (514, 184), (560, 250)], fill="none", stroke="#303030", stroke_width=2.2))
    r.add(Text(id="ra_t", x=492, y=222, text="라", font_size=30, font_family="Malgun Gothic", fill="#222222", anchor="middle"))

    r.add(Text(id="solution_label", x=40, y=314, text="풀이:", font_size=17, font_family="Malgun Gothic", fill="#222222"))
    r.add(Rect(id="solution_box", x=98, y=292, width=592, height=84, fill="none", stroke="#8A8A8A", stroke_width=1.5, rx=8, ry=8))
    r.add(Text(id="sol_line1", x=112, y=324, text="각 개수:", font_size=16, font_family="Malgun Gothic", fill="#222222"))
    r.add(Text(id="sol_line2", x=112, y=356, text="많은 순서:", font_size=16, font_family="Malgun Gothic", fill="#222222"))
    r.add(Rect(id="solution_angles", x=210, y=306, width=470, height=28, fill="none", stroke="none", stroke_width=0, semantic_role="answer_anchor"))
    r.add(Rect(id="solution_order", x=210, y=338, width=470, height=28, fill="none", stroke="none", stroke_width=0, semantic_role="answer_anchor"))

    r.add(Text(id="answer_label", x=40, y=404, text="답:", font_size=17, font_family="Malgun Gothic", fill="#222222"))
    r.add(Rect(id="answer_box", x=98, y=382, width=260, height=36, fill="none", stroke="#8A8A8A", stroke_width=1.5, rx=8, ry=8))
    r.add(Rect(id="answer_text", x=108, y=386, width=236, height=28, fill="none", stroke="none", stroke_width=0, semantic_role="answer_anchor"))
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
        answer_overrides={"answer_overlay_font_size": 16},
    )
    print("[3rd_shape2d_0012] generated:")
    print(f"  - {outputs['svg']}")
    print(f"  - {outputs['answer_svg']}")
