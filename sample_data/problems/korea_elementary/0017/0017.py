from pathlib import Path
import sys

from modu_semantic import Problem, Rect, Text


def build() -> Problem:
    p = Problem(width=736, height=340, problem_id="0017", problem_type="shape_number_equation")

    # 문제 문장
    p.add(
        Text(
            id="line1",
            x=20,
            y=42,
            text="같은 모양은 같은 수를 나타낼 때 ■는 얼마를 나타냅니까?",
            font_size=22,
            font_family="Malgun Gothic",
        )
    )

    # 식 영역
    p.add(
        Rect(
            id="equation_box",
            x=165,
            y=112,
            width=402,
            height=140,
            rx=22,
            ry=22,
            stroke="#111111",
            stroke_width=1,
            fill="none",
        )
    )
    p.add(Text(id="eq1", x=290, y=164, text="17×▲=■", font_size=44, font_family="Malgun Gothic"))
    p.add(Text(id="eq2", x=290, y=224, text="64÷▲=8", font_size=44, font_family="Malgun Gothic"))

    # 정답 괄호 영역
    p.add(Text(id="answer_left_paren", x=398, y=304, text="(", font_size=40, font_family="Malgun Gothic"))
    p.add(Text(id="answer_right_paren", x=700, y=304, text=")", font_size=40, font_family="Malgun Gothic"))
    p.add(
        Rect(
            id="answer_blank",
            x=430,
            y=272,
            width=235,
            height=44,
            stroke="none",
            fill="none",
            semantic_role="blank_answer",
        )
    )

    # ▲=8, ■=17×8=136
    p.set_answer(blanks=[], choices=[], answer_key=[{"target": "answer_blank", "value": "136"}])
    p.set_domain({"triangle": "8", "square": "136", "computed_answer": "136"})

    return p


CURRENT_DIR = Path(__file__).resolve().parent
PARENT_DIR = CURRENT_DIR.parent
if str(PARENT_DIR) not in sys.path:
    sys.path.insert(0, str(PARENT_DIR))

from _problem_runner import save_built_problem_outputs


if __name__ == "__main__":
    outputs = save_built_problem_outputs(build(), CURRENT_DIR, "0017")
    print("[0017] generated:")
    print(f"  - {outputs['problem_svg']}")
    print(f"  - {outputs['answer_svg']}")
