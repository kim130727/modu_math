"""문제 0001 DSL 빌드 파일.
핵심: 단위 변환 식의 빈칸 문제를 구성합니다.
"""

from modu_semantic import Problem, Rect, Region, Text

ANSWER_LABEL_STYLE = {
    "use_answer_label": True,
    "answer_label_x": 980,
    "answer_label_y": 500,
    "answer_label_font_size": 44,
    "answer_label_anchor": "start",
    "answer_label_baseline": "hanging",
    "answer_label_prefix": "정답: ",
}

# 레이아웃 상수
CANVAS_W = 1280
CANVAS_H = 720
INSTRUCTION_X = 72
INSTRUCTION_Y = 92
QUESTION_BOX_X = 280
QUESTION_BOX_Y = 240
QUESTION_BOX_W = 720
QUESTION_BOX_H = 180
EQUATION_X = QUESTION_BOX_X + QUESTION_BOX_W / 2
EQUATION_Y = 345


# 실제 문제 도형/텍스트를 Problem 객체에 쌓습니다.
def build() -> Problem:
    p = Problem(width=CANVAS_W, height=CANVAS_H, problem_id="0001", problem_type="fill_in_blank")
    root = Region(id="problem_root", x=0, y=0, width=CANVAS_W, height=CANVAS_H, visible_debug=False)

    root.add(
        Text(
            id="instruction",
            x=INSTRUCTION_X,
            y=INSTRUCTION_Y,
            text="□안에 알맞은 수를 구하시오.",
            font_size=42,
            font_family="Malgun Gothic",
            anchor="start",
            fill="#000000",
            semantic_role="instruction",
        )
    )
    root.add(
        Rect(
            id="question_box",
            x=QUESTION_BOX_X,
            y=QUESTION_BOX_Y,
            width=QUESTION_BOX_W,
            height=QUESTION_BOX_H,
            rx=24,
            fill="none",
            stroke="#000000",
            stroke_width=3,
            semantic_role="question_container",
        )
    )
    root.add(
        Text(
            id="equation",
            x=EQUATION_X,
            y=EQUATION_Y,
            text="410초=6분 □초",
            font_size=54,
            font_family="Malgun Gothic",
            anchor="middle",
            fill="#000000",
            semantic_role="equation",
        )
    )
    p.add(root)
    return p


from pathlib import Path
import sys

CURRENT_DIR = Path(__file__).resolve().parent
PARENT_DIR = CURRENT_DIR.parent
if str(PARENT_DIR) not in sys.path:
    sys.path.insert(0, str(PARENT_DIR))

from _problem_runner import save_built_problem_outputs


if __name__ == "__main__":
    outputs = save_built_problem_outputs(
        build(),
        CURRENT_DIR,
        "0001",
        answer_semantic_path=CURRENT_DIR / "input" / "json" / "semantic_final.json",
        answer_overrides=ANSWER_LABEL_STYLE,
    )
    print("[0001] generated:")
    print(f"  - {outputs['problem_svg']}")
    print(f"  - {outputs['answer_svg']}")

