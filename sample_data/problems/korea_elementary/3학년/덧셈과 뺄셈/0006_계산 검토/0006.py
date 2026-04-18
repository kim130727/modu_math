"""문제 0006 DSL 빌드 파일. 오답/정답 계산 패널과 화살표를 배치합니다."""

from modu_semantic import Line, Polygon, Problem, Rect, Region, Text

# 레이아웃 상수
CANVAS_W = 1744
CANVAS_H = 725

INSTRUCTION_X = 115.52105
INSTRUCTION_Y = 95.168732

LEFT_PANEL_X = 203.9678
LEFT_PANEL_Y = 215.6675
LEFT_PANEL_W = 585
LEFT_PANEL_H = 435

RIGHT_PANEL_X = 966.96783
RIGHT_PANEL_Y = 205.6675
RIGHT_PANEL_W = 615
RIGHT_PANEL_H = 455

RIGHT_TAB_X = 1089.9678
RIGHT_TAB_Y = 169.6675
RIGHT_TAB_W = 400
RIGHT_TAB_H = 100
RIGHT_TAB_CENTER_X = RIGHT_TAB_X + (RIGHT_TAB_W / 2)
RIGHT_TAB_TEXT_Y = 231.6675

LEFT_EQ_RIGHT_X = 622.57715
LEFT_TOP_Y = 360
LEFT_MID_Y = 460
LEFT_RESULT_Y = 560

LEFT_LINE_X1 = 296.30759
LEFT_LINE_X2 = 636.30762
LEFT_LINE_Y = 486

ARROW_CENTER_X = 892.96783
ARROW_TIP_X = 914.96783
ARROW_CENTER_Y = 435.66748
ARROW_HALF_H = 27.0
ARROW_BODY_LEN = 40.0


def _add_arrow(root: Region) -> None:
    root.add(
        Line(
            id="arrow_body",
            x1=ARROW_CENTER_X - ARROW_BODY_LEN,
            y1=ARROW_CENTER_Y,
            x2=ARROW_CENTER_X,
            y2=ARROW_CENTER_Y,
            stroke="#9AAAB2",
            stroke_width=14,
            semantic_role="arrow",
        )
    )
    root.add(
        Polygon(
            id="arrow_head",
            points=[
                (ARROW_CENTER_X, ARROW_CENTER_Y - ARROW_HALF_H),
                (ARROW_TIP_X, ARROW_CENTER_Y),
                (ARROW_CENTER_X, ARROW_CENTER_Y + ARROW_HALF_H),
            ],
            fill="#9AAAB2",
            stroke="none",
            stroke_width=0,
            semantic_role="arrow",
        )
    )


# 레이아웃 상수
def build() -> Problem:
    p = Problem(width=CANVAS_W, height=CANVAS_H, problem_id="0006", problem_type="find_wrong_and_correct_addition")
    root = Region(id="problem_root", x=0, y=0, width=CANVAS_W, height=CANVAS_H, visible_debug=False)

    root.add(
        Text(
            id="instruction",
            x=INSTRUCTION_X,
            y=INSTRUCTION_Y,
            text="잘못 계산한 곳에 ○표 하고, 바르게 계산해 보세요.",
            font_size=66,
            font_family="Malgun Gothic",
            anchor="start",
            fill="#222222",
            semantic_role="instruction",
        )
    )

    root.add(
        Rect(
            id="left_panel",
            x=LEFT_PANEL_X,
            y=LEFT_PANEL_Y,
            width=LEFT_PANEL_W,
            height=LEFT_PANEL_H,
            rx=70,
            fill="none",
            stroke="#CFC8BA",
            stroke_width=9,
            semantic_role="panel",
        )
    )
    root.add(
        Rect(
            id="right_panel",
            x=RIGHT_PANEL_X,
            y=RIGHT_PANEL_Y,
            width=RIGHT_PANEL_W,
            height=RIGHT_PANEL_H,
            rx=70,
            fill="none",
            stroke="#CFC8BA",
            stroke_width=9,
            semantic_role="panel",
        )
    )
    root.add(
        Rect(
            id="right_tab",
            x=RIGHT_TAB_X,
            y=RIGHT_TAB_Y,
            width=RIGHT_TAB_W,
            height=RIGHT_TAB_H,
            rx=38,
            fill="#CE8D61",
            stroke="none",
            stroke_width=0,
            semantic_role="tab",
        )
    )
    root.add(
        Text(
            id="right_tab_text",
            x=RIGHT_TAB_CENTER_X,
            y=RIGHT_TAB_TEXT_Y,
            text="바르게 계산하기",
            font_size=42,
            font_family="Malgun Gothic",
            anchor="middle",
            fill="#FFFFFF",
            semantic_role="tab_label",
        )
    )

    root.add(
        Text(
            id="left_top",
            x=LEFT_EQ_RIGHT_X,
            y=LEFT_TOP_Y,
            text="323",
            font_size=88,
            font_family="Cambria",
            anchor="end",
            fill="#222222",
            semantic_role="equation",
        )
    )
    root.add(
        Text(
            id="left_mid",
            x=LEFT_EQ_RIGHT_X,
            y=LEFT_MID_Y,
            text="+998",
            font_size=88,
            font_family="Cambria",
            anchor="end",
            fill="#222222",
            semantic_role="equation",
        )
    )
    root.add(
        Line(
            id="left_line",
            x1=LEFT_LINE_X1,
            y1=LEFT_LINE_Y,
            x2=LEFT_LINE_X2,
            y2=LEFT_LINE_Y,
            stroke="#333333",
            stroke_width=3,
            semantic_role="equation_line",
        )
    )
    root.add(
        Text(
            id="left_result",
            x=LEFT_EQ_RIGHT_X,
            y=LEFT_RESULT_Y,
            text="1221",
            font_size=87,
            font_family="Cambria",
            anchor="end",
            fill="#222222",
            semantic_role="wrong_result",
        )
    )

    _add_arrow(root)

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
        "0006",
        answer_semantic_path=CURRENT_DIR / "input" / "json" / "semantic_final.json",
    )
    print("[0006] generated:")
    print(f"  - {outputs['problem_svg']}")
    print(f"  - {outputs['answer_svg']}")
