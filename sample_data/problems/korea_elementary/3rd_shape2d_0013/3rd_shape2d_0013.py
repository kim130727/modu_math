from pathlib import Path
import sys

from modu_semantic import Polygon, Problem, Rect, Region, Text

CANVAS_W = 790
CANVAS_H = 240
PROBLEM_ID = "3rd_shape2d_0013"
PROBLEM_TYPE = "find_non_right_triangle"
TITLE_TEXT = "직각삼각형 찾기"
INSTRUCTION_TEXT = "직각삼각형이 아닌 것을 찾아 기호를 쓰고 그 이유를 쓰세요."


def build() -> Problem:
    p = Problem(width=CANVAS_W, height=CANVAS_H, problem_id=PROBLEM_ID, problem_type=PROBLEM_TYPE)
    p.title = TITLE_TEXT
    p.set_domain(
        {
            "instruction": INSTRUCTION_TEXT,
            "right_triangles": ["가", "나", "다"],
            "non_right": "라",
            "reason": "라 도형은 90도인 각이 없다.",
            "solution": {
                "selected_label": "라",
                "explanation": "라 도형은 90도인 각이 없다.",
                "final_answer": "라",
            },
        }
    )
    p.set_answer(
        blanks=[],
        choices=[],
        answer_key=[{"target": "answer_text", "value": "라, 라 도형은 90도인 각이 없다."}],
    )

    r = Region(id="root", x=0, y=0, width=CANVAS_W, height=CANVAS_H, visible_debug=False)
    r.add(Rect(id="bg", x=0, y=0, width=CANVAS_W, height=CANVAS_H, fill="#F4F4F4", stroke="none", stroke_width=0))
    r.add(Text(id="i1", x=4, y=34, text=INSTRUCTION_TEXT, font_size=17, font_family="Malgun Gothic", fill="#222222"))

    r.add(Rect(id="frame", x=112, y=94, width=552, height=106, fill="none", stroke="#8A8A8A", stroke_width=1.4, rx=10, ry=10))

    r.add(Polygon(id="ga", points=[(128, 118), (236, 118), (236, 176)], fill="none", stroke="#303030", stroke_width=2.1))
    r.add(Text(id="ga_t", x=205, y=149, text="가", font_size=18, font_family="Malgun Gothic", fill="#222222", anchor="middle"))

    r.add(Polygon(id="na", points=[(282, 176), (282, 124), (356, 176)], fill="none", stroke="#303030", stroke_width=2.1))
    r.add(Text(id="na_t", x=314, y=156, text="나", font_size=18, font_family="Malgun Gothic", fill="#222222", anchor="middle"))

    r.add(Polygon(id="da", points=[(438, 124), (438, 186), (506, 186)], fill="none", stroke="#303030", stroke_width=2.1))
    r.add(Text(id="da_t", x=460, y=164, text="다", font_size=18, font_family="Malgun Gothic", fill="#222222", anchor="middle"))

    r.add(Polygon(id="ra", points=[(582, 112), (648, 114), (614, 186)], fill="none", stroke="#303030", stroke_width=2.1))
    r.add(Text(id="ra_t", x=614, y=149, text="라", font_size=18, font_family="Malgun Gothic", fill="#222222", anchor="middle"))

    r.add(Rect(id="answer_text", x=462, y=206, width=320, height=28, fill="none", stroke="none", stroke_width=0, semantic_role="answer_anchor"))
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
    print("[3rd_shape2d_0013] generated:")
    print(f"  - {outputs['svg']}")
    print(f"  - {outputs['answer_svg']}")
