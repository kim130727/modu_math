"""문제 0009 DSL 빌드 파일. 수직선 분할 길이와 전체 길이 빈칸을 구성합니다."""

from pathlib import Path
import sys

from modu_semantic import Line, Problem, Rect, Region, Text

ANSWER_LABEL_STYLE = {
    "use_answer_label": True,
    "answer_label_top_right": True,
    "answer_label_font_size": 42,
}

# 레이아웃 상수
CANVAS_W = 860
CANVAS_H = 400
Y_OFFSET = 90

INSTRUCTION_TEXT = "□안에 알맞은 수를 넣으세요."
INSTRUCTION_X = 89
INSTRUCTION_Y = 67

LINE_X1 = 208
LINE_X2 = 818
LINE_Y = 168

LEFT_TICK_X = 208
MID_TICK_X = 396
RIGHT_TICK_X = 818
TICK_Y1 = 153
TICK_Y2 = 183

LEFT_SEG_TEXT_X = 302
RIGHT_SEG_TEXT_X = 607
SEG_TEXT_Y = 226

TOTAL_BLANK_X = 455
TOTAL_BLANK_Y = 84
TOTAL_BLANK_W = 96
TOTAL_BLANK_H = 46


def _oy(y: float) -> float:
    return y + Y_OFFSET


def _curve_y(t: float, *, base_y: float, apex_y: float) -> float:
    return apex_y + ((base_y - apex_y) * ((2.0 * t - 1.0) ** 2))


def _add_dashed_curve(
    root: Region,
    *,
    seg_prefix: str,
    x1: float,
    x2: float,
    base_y: float,
    apex_y: float,
    stroke_width: float = 2.0,
    seg_count: int = 72,
) -> None:
    for i in range(0, seg_count, 3):
        t1 = i / seg_count
        t2 = min((i + 1) / seg_count, 1.0)
        xa = x1 + ((x2 - x1) * t1)
        xb = x1 + ((x2 - x1) * t2)
        ya = _curve_y(t1, base_y=base_y, apex_y=apex_y)
        yb = _curve_y(t2, base_y=base_y, apex_y=apex_y)
        root.add(
            Line(
                id=f"{seg_prefix}_seg_{i}",
                x1=xa,
                y1=ya,
                x2=xb,
                y2=yb,
                stroke="#69BEEA",
                stroke_width=stroke_width,
                semantic_role="measurement_guide",
            )
        )

# 레이아웃 상수
def build() -> Problem:
    p = Problem(width=CANVAS_W, height=CANVAS_H, problem_id="0009", problem_type="number_line_missing_total")
    root = Region(id="problem_root", x=0, y=0, width=CANVAS_W, height=CANVAS_H, visible_debug=False)

    root.add(
        Text(
            id="inst",
            x=INSTRUCTION_X,
            y=_oy(INSTRUCTION_Y),
            text=INSTRUCTION_TEXT,
            font_size=47,
            font_family="Malgun Gothic",
            anchor="start",
            fill="#222222",
            semantic_role="instruction",
        )
    )

    root.add(
        Line(
            id="line",
            x1=LINE_X1,
            y1=_oy(LINE_Y),
            x2=LINE_X2,
            y2=_oy(LINE_Y),
            stroke="#3A3539",
            stroke_width=3,
            semantic_role="number_line",
        )
    )
    for tick_id, tick_x in (("tick_l", LEFT_TICK_X), ("tick_m", MID_TICK_X), ("tick_r", RIGHT_TICK_X)):
        root.add(
            Line(
                id=tick_id,
                x1=tick_x,
                y1=_oy(TICK_Y1),
                x2=tick_x,
                y2=_oy(TICK_Y2),
                stroke="#3A3539",
                stroke_width=3,
                semantic_role="point_tick",
            )
        )

    root.add(
        Text(
            id="seg_1_text",
            x=LEFT_SEG_TEXT_X,
            y=_oy(SEG_TEXT_Y),
            text="261",
            font_size=40,
            font_family="Cambria",
            anchor="middle",
            fill="#222222",
            semantic_role="distance_label",
        )
    )
    root.add(
        Text(
            id="seg_2_text",
            x=RIGHT_SEG_TEXT_X,
            y=_oy(SEG_TEXT_Y),
            text="588",
            font_size=40,
            font_family="Cambria",
            anchor="middle",
            fill="#222222",
            semantic_role="distance_label",
        )
    )

    root.add(
        Rect(
            id="total_blank",
            x=TOTAL_BLANK_X,
            y=_oy(TOTAL_BLANK_Y),
            width=TOTAL_BLANK_W,
            height=TOTAL_BLANK_H,
            rx=6,
            stroke="#69BEEA",
            stroke_width=3,
            fill="none",
            semantic_role="answer_blank",
        )
    )

    _add_dashed_curve(root, seg_prefix="seg_total_top", x1=LINE_X1, x2=LINE_X2, base_y=_oy(LINE_Y), apex_y=_oy(145))
    _add_dashed_curve(root, seg_prefix="seg_left_bottom", x1=LEFT_TICK_X, x2=MID_TICK_X, base_y=_oy(LINE_Y), apex_y=_oy(185))
    _add_dashed_curve(root, seg_prefix="seg_right_bottom", x1=MID_TICK_X, x2=RIGHT_TICK_X, base_y=_oy(LINE_Y), apex_y=_oy(186))

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
        "0009",
        answer_semantic_path=CURRENT_DIR / "input" / "json" / "semantic_final.json",
        answer_overrides=ANSWER_LABEL_STYLE,
    )
    print("[0009] generated:")
    print(f"  - {outputs['problem_svg']}")
    print(f"  - {outputs['answer_svg']}")

