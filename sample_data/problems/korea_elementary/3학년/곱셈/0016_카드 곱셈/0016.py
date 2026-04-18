from pathlib import Path
import sys

from modu_semantic import Problem, Rect, Text


def build() -> Problem:
    p = Problem(width=768, height=341, problem_id="0016", problem_type="card_multiplication")

    # 문제 문장 (원본 대비 글자 크기/행간 조정)
    p.add(
        Text(
            id="line1_prefix",
            x=18,
            y=46,
            text="3장의 수 카드를 모두 한 번씩만 사용하여",
            font_size=22,
            font_family="Malgun Gothic",
        )
    )

    # 상단 식: □ × □□ (문장 바로 옆으로 간격 축소)
    p.add(Rect(id="expr_box_1", x=486, y=17, width=33, height=31, stroke="#1f1f1f", fill="none", stroke_width=1))
    p.add(Text(id="expr_mul", x=525, y=45, text="×", font_size=45, font_family="Malgun Gothic"))
    p.add(Rect(id="expr_box_2", x=553, y=17, width=33, height=31, stroke="#1f1f1f", fill="none", stroke_width=1))
    p.add(Rect(id="expr_box_3", x=594, y=17, width=33, height=31, stroke="#1f1f1f", fill="none", stroke_width=1))
    # 원본 문제 표기 유지: 상단 식 네모는 비워 둠

    p.add(
        Text(
            id="line2",
            x=18,
            y=102,
            text="을 만들려고 합니다. 곱이 가장 큰 곱셈식을 만들어 곱을 구하시오",
            font_size=22,
            font_family="Malgun Gothic",
        )
    )

    # 수 카드 9, 2, 4
    p.add(Rect(id="card_9", x=182, y=172, width=73, height=85, stroke="#1f1f1f", fill="#b4b4b4", stroke_width=1))
    p.add(Text(id="num_9", x=206, y=230, text="9", font_size=53, font_family="Malgun Gothic"))

    p.add(Rect(id="card_2", x=327, y=172, width=73, height=85, stroke="#1f1f1f", fill="#b4b4b4", stroke_width=1))
    p.add(Text(id="num_2", x=351, y=230, text="2", font_size=53, font_family="Malgun Gothic"))

    p.add(Rect(id="card_4", x=472, y=172, width=73, height=85, stroke="#1f1f1f", fill="#b4b4b4", stroke_width=1))
    p.add(Text(id="num_4", x=496, y=230, text="4", font_size=53, font_family="Malgun Gothic"))

    # 정답 영역: (      )
    p.add(Text(id="answer_left_paren", x=396, y=304, text="(", font_size=40, font_family="Malgun Gothic"))
    p.add(Text(id="answer_right_paren", x=697, y=304, text=")", font_size=40, font_family="Malgun Gothic"))

    # answer.svg overlay target
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

    # answer.svg에서만 표기: 상단 박스 9×42, 하단 괄호 378
    p.set_answer(
        blanks=[],
        choices=[],
        answer_key=[
            {"target": "expr_box_1", "value": "9"},
            {"target": "expr_box_2", "value": "4"},
            {"target": "expr_box_3", "value": "2"},
            {"target": "answer_blank", "value": "378"},
        ],
    )
    p.set_domain({"computed_answer": "378", "max_expression": "9×42"})

    return p


CURRENT_DIR = Path(__file__).resolve().parent
PARENT_DIR = CURRENT_DIR.parent
if str(PARENT_DIR) not in sys.path:
    sys.path.insert(0, str(PARENT_DIR))

from _problem_runner import save_built_problem_outputs


if __name__ == "__main__":
    outputs = save_built_problem_outputs(build(), CURRENT_DIR, "0016")
    print("[0016] generated:")
    print(f"  - {outputs['problem_svg']}")
    print(f"  - {outputs['answer_svg']}")
