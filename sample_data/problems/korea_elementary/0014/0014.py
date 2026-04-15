from pathlib import Path
import sys

from modu_semantic import Line, Problem, Rect, Region, Text

CANVAS_W = 980
CANVAS_H = 493

ANSWER_LABEL_STYLE = {
    "use_answer_label": True,
    "answer_label_top_right": False,
    "answer_label_x": CANVAS_W - 24,
    "answer_label_y": CANVAS_H - 24,
    "answer_label_anchor": "end",
    "answer_label_baseline": "auto",
    "answer_label_font_size": 32,
}

PROBLEM_TYPE = "mixed_fraction_division_range_count"
TITLE_TEXT = "대분수 나눗셈의 몫 범위"

LINE_1A = "숫자 카드"
LINE_1B = "를 모두 한 번씩만 사용하여"
LINE_2 = "다음과 같이 (대분수) ÷ (자연수)를 만들려고 합니다."
LINE_3 = "만들 수 있는 값 중 몫이 가장 작을 때의 몫과 몫이"
LINE_4 = "가장 클 때의 몫 사이에 있는 자연수는 모두 몇 개인가요?"

CARD_VALUES = [3, 5, 7, 9]
CARD_RECTS = [
    (188.0, 13.95, 50.87, 52.32),
    (256.5, 13.95, 49.65, 53.54),
    (322.5, 13.97, 52.06, 54.73),
    (389.8, 13.98, 52.05, 55.94),
]

EXPR_BOX = (268.99, 308.46, 315.14, 160.19)
WHOLE_BLANK = (321.11, 373.79, 36.0, 34.0)
FRAC_NUM_BLANK = (383.11, 343.79, 36.0, 34.0)
FRAC_DEN_BLANK = (383.11, 405.79, 36.0, 34.0)
DIV_BLANK = (486.11, 373.79, 36.0, 34.0)
FRAC_BAR_Y = 390.79


def _add_cards(root: Region) -> None:
    for i, (value, rect) in enumerate(zip(CARD_VALUES, CARD_RECTS, strict=True), start=1):
        x, y, w, h = rect
        cx = x + (w / 2.0)
        root.add(
            Rect(
                id=f"card_{i}",
                x=x,
                y=y,
                width=w,
                height=h,
                fill="#BDBDBD",
                stroke="#000000",
                stroke_width=1,
                semantic_role="card",
            )
        )
        root.add(
            Text(
                id=f"card_t_{i}",
                x=cx,
                y=55,
                text=str(value),
                font_size=46,
                font_family="Malgun Gothic",
                fill="#222222",
                anchor="middle",
                semantic_role="card_value",
            )
        )


def _add_expression_frame(root: Region) -> None:
    ex, ey, ew, eh = EXPR_BOX
    root.add(
        Rect(
            id="expr_box",
            x=ex,
            y=ey,
            width=ew,
            height=eh,
            rx=14,
            fill="none",
            stroke="#000000",
            stroke_width=1,
            semantic_role="expression",
        )
    )

    root.add(
        Rect(
            id="whole_blank",
            x=WHOLE_BLANK[0],
            y=WHOLE_BLANK[1],
            width=WHOLE_BLANK[2],
            height=WHOLE_BLANK[3],
            fill="none",
            stroke="#000000",
            stroke_width=1,
            semantic_role="answer_blank",
        )
    )
    root.add(
        Rect(
            id="frac_num_blank",
            x=FRAC_NUM_BLANK[0],
            y=FRAC_NUM_BLANK[1],
            width=FRAC_NUM_BLANK[2],
            height=FRAC_NUM_BLANK[3],
            fill="none",
            stroke="#000000",
            stroke_width=1,
            semantic_role="answer_blank",
        )
    )
    root.add(
        Rect(
            id="frac_den_blank",
            x=FRAC_DEN_BLANK[0],
            y=FRAC_DEN_BLANK[1],
            width=FRAC_DEN_BLANK[2],
            height=FRAC_DEN_BLANK[3],
            fill="none",
            stroke="#000000",
            stroke_width=1,
            semantic_role="answer_blank",
        )
    )
    root.add(
        Line(
            id="frac_bar",
            x1=369.11,
            y1=FRAC_BAR_Y,
            x2=433.11,
            y2=FRAC_BAR_Y,
            stroke="#222222",
            stroke_width=2,
            semantic_role="operator",
        )
    )
    root.add(
        Text(
            id="div_sign",
            x=457.11,
            y=406.79,
            text="÷",
            font_size=64,
            font_family="Malgun Gothic",
            fill="#222222",
            anchor="middle",
            semantic_role="operator",
        )
    )
    root.add(
        Rect(
            id="div_blank",
            x=DIV_BLANK[0],
            y=DIV_BLANK[1],
            width=DIV_BLANK[2],
            height=DIV_BLANK[3],
            fill="none",
            stroke="#000000",
            stroke_width=1,
            semantic_role="answer_blank",
        )
    )


def build() -> Problem:
    p = Problem(width=CANVAS_W, height=CANVAS_H, problem_id="0014", problem_type=PROBLEM_TYPE)
    p.title = TITLE_TEXT

    p.set_domain(
        {
            "cards": CARD_VALUES,
            "instruction_lines": [LINE_1A, LINE_1B, LINE_2, LINE_3, LINE_4],
            "answer_value": 3,
        }
    )
    p.set_answer(
        blanks=[{"id": "value", "kind": "numeric", "value": "3"}],
        choices=[],
        answer_key=[{"target": "value", "value": "3"}],
    )

    root = Region(id="problem_root", x=0, y=0, width=CANVAS_W, height=CANVAS_H, visible_debug=False)
    root.add(
        Rect(
            id="bg",
            x=0,
            y=0,
            width=CANVAS_W,
            height=CANVAS_H,
            fill="#F6F6F6",
            stroke="none",
            stroke_width=0,
            semantic_role="background",
        )
    )

    root.add(
        Text(
            id="l1a",
            x=21.45,
            y=56.56,
            text=LINE_1A,
            font_size=34,
            font_family="Malgun Gothic",
            fill="#222222",
            anchor="start",
            semantic_role="instruction",
        )
    )
    _add_cards(root)
    root.add(
        Text(
            id="l1b",
            x=458.35,
            y=54.10,
            text=LINE_1B,
            font_size=33,
            font_family="Malgun Gothic",
            fill="#222222",
            anchor="start",
            semantic_role="instruction",
        )
    )

    root.add(
        Text(
            id="l2",
            x=21.72,
            y=114.22,
            text=LINE_2,
            font_size=32,
            font_family="Malgun Gothic",
            fill="#222222",
            anchor="start",
            semantic_role="instruction",
        )
    )
    root.add(
        Text(
            id="l3",
            x=19.62,
            y=164.03,
            text=LINE_3,
            font_size=32,
            font_family="Malgun Gothic",
            fill="#222222",
            anchor="start",
            semantic_role="instruction",
        )
    )
    root.add(
        Text(
            id="l4",
            x=18.35,
            y=215.79,
            text=LINE_4,
            font_size=33,
            font_family="Malgun Gothic",
            fill="#222222",
            anchor="start",
            semantic_role="instruction",
        )
    )
    _add_expression_frame(root)
    p.add(root)
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
        "0014",
        answer_semantic_path=CURRENT_DIR / "input" / "json" / "semantic_final.json",
        answer_overrides=ANSWER_LABEL_STYLE,
    )
    print("[0014] generated:")
    print(f"  - {outputs['problem_svg']}")
    print(f"  - {outputs['answer_svg']}")
