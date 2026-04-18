from pathlib import Path
import sys

from modu_semantic import Problem, Rect, Region, Text

CANVAS_W = 406
CANVAS_H = 181
PROBLEM_ID = "3rd_addition_subtraction_0004"


def build() -> Problem:
    p = Problem(width=CANVAS_W, height=CANVAS_H, problem_id=PROBLEM_ID, problem_type="inequality_digit_count")
    p.title = "부등식 가능한 수"
    p.set_domain(
        {
            "inequality": "4□5 + 298 > 763",
            "digit_range": [0, 9],
            "count": 3,
            "valid_digits": [7, 8, 9],
        }
    )
    p.set_answer(blanks=[], choices=[], answer_key=[{"target": "answer_count", "value": "3"}])

    r = Region(id="root", x=0, y=0, width=CANVAS_W, height=CANVAS_H, visible_debug=False)
    r.add(Rect(id="bg", x=0, y=0, width=CANVAS_W, height=CANVAS_H, fill="#FFFFFF", stroke="none", stroke_width=0))
    r.add(Text(id="i1", x=6, y=30, text="0부터 9까지의 수 중에서 □에 들어갈 수를", font_size=17, font_family="Malgun Gothic", fill="#222222"))
    r.add(Text(id="i2", x=6, y=60, text="모두 구하고 개수를 쓰시오.", font_size=17, font_family="Malgun Gothic", fill="#222222"))

    r.add(Rect(id="eq_box", x=2, y=78, width=402, height=56, fill="none", stroke="#666666", stroke_width=1.5, rx=10, ry=10))
    r.add(Text(id="eq", x=201, y=112, text="4□5+298>763", font_size=17, font_family="Malgun Gothic", fill="#222222", anchor="middle"))

    r.add(Text(id="lp", x=230, y=168, text="(", font_size=24, font_family="Malgun Gothic", fill="#222222"))
    r.add(Text(id="rp", x=364, y=168, text=")", font_size=24, font_family="Malgun Gothic", fill="#222222"))
    r.add(Text(id="gaesu", x=378, y=166, text="개", font_size=17, font_family="Malgun Gothic", fill="#222222"))
    r.add(Rect(id="answer_count", x=246, y=146, width=110, height=28, fill="none", stroke="none", stroke_width=0, semantic_role="answer_anchor"))

    p.add(r)
    return p


CURRENT_DIR = Path(__file__).resolve().parent
PARENT_DIR = CURRENT_DIR.parent
if str(PARENT_DIR) not in sys.path:
    sys.path.insert(0, str(PARENT_DIR))
from _problem_runner import save_built_problem_outputs

if __name__ == "__main__":
    outputs = save_built_problem_outputs(build(), CURRENT_DIR, PROBLEM_ID, answer_overrides={"answer_overlay_numeric_font_size": 24})
    print("[3rd_addition_subtraction_0004] generated:")
    print(f"  - {outputs['svg']}")
    print(f"  - {outputs['answer_svg']}")
