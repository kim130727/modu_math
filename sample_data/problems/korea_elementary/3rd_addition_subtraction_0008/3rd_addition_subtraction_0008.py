from pathlib import Path
import sys

from modu_semantic import Problem, Rect, Region, Text

CANVAS_W = 767
CANVAS_H = 155
PROBLEM_ID = "3rd_addition_subtraction_0008"


def build() -> Problem:
    p = Problem(width=CANVAS_W, height=CANVAS_H, problem_id=PROBLEM_ID, problem_type="max_subtraction_pick_two")
    p.title = "가장 큰 뺄셈"
    p.set_domain({"numbers": [326, 412, 481, 112], "best_expression": "481-112", "result": 369})
    p.set_answer(blanks=[], choices=[], answer_key=[{"target": "answer_expr", "value": "481-112=369"}])

    r = Region(id="root", x=0, y=0, width=CANVAS_W, height=CANVAS_H, visible_debug=False)
    r.add(Rect(id="bg", x=0, y=0, width=CANVAS_W, height=CANVAS_H, fill="#FFFFFF", stroke="none", stroke_width=0))
    r.add(Text(id="i1", x=6, y=34, text="다음 수 중에서 2개를 골라 가장 큰 뺄셈식을 만들려고 합니다. 식과 답을 구하시오.", font_size=17, font_family="Malgun Gothic", fill="#222222"))

    r.add(Rect(id="num_box", x=168, y=86, width=389, height=56, fill="none", stroke="#666666", stroke_width=1.5, rx=10, ry=10))
    for idx, v in enumerate((326, 412, 481, 112)):
        r.add(Text(id=f"n{idx+1}", x=259 + (idx * 75), y=123, text=str(v), font_size=17, font_family="Malgun Gothic", fill="#222222", anchor="middle"))

    r.add(Rect(id="answer_expr", x=520, y=121, width=238, height=28, fill="none", stroke="none", stroke_width=0, semantic_role="answer_anchor"))
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
            "answer_label_font_size": 20,
            "answer_label_x": 756,
            "answer_label_y": 121,
            "answer_label_top_right": False,
        },
    )
    print("[3rd_addition_subtraction_0008] generated:")
    print(f"  - {outputs['svg']}")
    print(f"  - {outputs['answer_svg']}")
