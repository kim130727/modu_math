"""문제 0005 DSL 빌드 파일. 두 계산식 비교(큰 값 선택) 레이아웃을 구성합니다."""

from modu_semantic import Problem, Rect, Region, Text

ANSWER_LABEL_STYLE = {
    "use_answer_label": True,
    "answer_label_x": 1520,
    "answer_label_y": 82,
    "answer_label_font_size": 52,
    "answer_label_anchor": "start",
    "answer_label_baseline": "hanging",
    "answer_label_prefix": "Answer: ",
}

# 레이아웃 상수
CANVAS_W = 1852
CANVAS_H = 554

INSTRUCTION_X = 44
INSTRUCTION_Y = 106

CARD_Y = 180
CARD_W = 590
CARD_H = 210
CARD_RX = 75

LEFT_CARD_X = 320
RIGHT_CARD_X = 1200

EXPR_DX = CARD_W / 2
EXPR_Y = 294

PAREN_LEFT_DX = 180
PAREN_RIGHT_DX = 415
PAREN_Y = 478


def _add_choice_card(root: Region, *, prefix: str, x: float, y: float, expr: str) -> None:
    root.add(
        Rect(
            id=f"{prefix}_box",
            x=x,
            y=y,
            width=CARD_W,
            height=CARD_H,
            rx=CARD_RX,
            fill="#D0CABB",
            stroke="none",
            stroke_width=0,
            semantic_role="choice",
        )
    )
    root.add(
        Text(
            id=f"{prefix}_expr",
            x=x + EXPR_DX,
            y=EXPR_Y,
            text=expr,
            font_size=74,
            font_family="Cambria",
            anchor="middle",
            fill="#222222",
            semantic_role="decorative",
        )
    )
    root.add(
        Text(
            id=f"{prefix}_paren_l",
            x=x + PAREN_LEFT_DX,
            y=PAREN_Y,
            text="(",
            font_size=92,
            font_family="Cambria",
            anchor="middle",
            fill="#222222",
            semantic_role="decorative",
        )
    )
    root.add(
        Text(
            id=f"{prefix}_paren_r",
            x=x + PAREN_RIGHT_DX,
            y=PAREN_Y,
            text=")",
            font_size=92,
            font_family="Cambria",
            anchor="middle",
            fill="#222222",
            semantic_role="decorative",
        )
    )


# 레이아웃 상수
def build() -> Problem:
    p = Problem(width=CANVAS_W, height=CANVAS_H, problem_id="0005", problem_type="compare_two_sums")
    root = Region(id="problem_root", x=0, y=0, width=CANVAS_W, height=CANVAS_H, visible_debug=False)

    root.add(
        Text(
            id="instruction",
            x=INSTRUCTION_X,
            y=INSTRUCTION_Y,
            text="계산 결과가 더 큰 것에 ○표 하세요.",
            font_size=72,
            font_family="Malgun Gothic",
            anchor="start",
            fill="#222222",
            semantic_role="decorative",
        )
    )

    _add_choice_card(root, prefix="left", x=LEFT_CARD_X, y=CARD_Y, expr="605+298")
    _add_choice_card(root, prefix="right", x=RIGHT_CARD_X, y=CARD_Y, expr="567+385")

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
        "0005",
        answer_semantic_path=CURRENT_DIR / "input" / "json" / "semantic_final.json",
        answer_overrides=ANSWER_LABEL_STYLE,
    )
    print("[0005] generated:")
    print(f"  - {outputs['problem_svg']}")
    print(f"  - {outputs['answer_svg']}")
