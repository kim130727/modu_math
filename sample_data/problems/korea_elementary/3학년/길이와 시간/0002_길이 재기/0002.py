"""문제 0002 DSL 빌드 파일.
핵심: 눈금자, 물체, 보조선, 답안 영역을 좌표 상수로 구성합니다.
"""

from modu_semantic import Line, Problem, Rect, Region, Text

ANSWER_LABEL_STYLE = {
    "use_answer_label": True,
    "answer_label_x": 980,
    "answer_label_y": 560,
    "answer_label_font_size": 44,
    "answer_label_anchor": "start",
    "answer_label_baseline": "hanging",
    "answer_label_prefix": "정답: ",
}

# 레이아웃 상수
CANVAS_W = 1280
CANVAS_H = 720
INSTRUCTION_X = 72
INSTRUCTION_Y = 80
SUB_INSTRUCTION_X = 72
SUB_INSTRUCTION_Y = 128
RULER_X = 220
RULER_Y = 330
RULER_W = 820
RULER_H = 170
ERASER_X = 493.3333333333333
ERASER_Y = 170
ERASER_W = 437.3333333333333
ERASER_H = 135
ERASER_CENTER_X = ERASER_X + (ERASER_W / 2)
ERASER_LABEL_Y = 251.5
GUIDE_TOP_Y = 150
GUIDE_BOTTOM_Y = 334
LEFT_GUIDE_X = ERASER_X
RIGHT_GUIDE_X = 930.6666666666666
ANSWER_PAREN_Y = 640
ANSWER_LEFT_PAREN_X = 530
ANSWER_RIGHT_PAREN_X = 782.72516
TICK_START_X = RULER_X
TICK_Y1 = RULER_Y
TICK_MAJOR_Y2 = 394
TICK_MINOR_Y2 = 364
TICK_STEP = 54.666666666666664
MAJOR_INDICES = {0, 5, 10, 15}
MAJOR_NUMBER_Y = 462
MAJOR_NUMBER_X = {
    "2": 233.03053,
    "3": 493.3333333333333,
    "4": 766.6666666666666,
    "5": 1027.9718,
}


# 실제 문제 도형/텍스트를 Problem 객체에 쌓습니다.
def build() -> Problem:
    p = Problem(width=CANVAS_W, height=CANVAS_H, problem_id="0002", problem_type="measure_length_with_ruler")
    root = Region(id="problem_root", x=0, y=0, width=CANVAS_W, height=CANVAS_H)

    root.add(
        Text(
            id="instruction",
            x=INSTRUCTION_X,
            y=INSTRUCTION_Y,
            text="2. 지우개의 길이는 몇 mm입니까?",
            font_size=42,
            font_family="Malgun Gothic",
            anchor="start",
            fill="#000000",
            semantic_role="instruction",
        )
    )
    root.add(
        Text(
            id="sub_instruction",
            x=SUB_INSTRUCTION_X,
            y=SUB_INSTRUCTION_Y,
            text="(* 눈금을 보고 써 보아요)",
            font_size=30,
            font_family="Malgun Gothic",
            anchor="start",
            fill="#000000",
            semantic_role="sub_instruction",
        )
    )

    root.add(
        Rect(
            id="ruler_body",
            x=RULER_X,
            y=RULER_Y,
            width=RULER_W,
            height=RULER_H,
            rx=0,
            stroke="#111111",
            stroke_width=6,
            fill="none",
            semantic_role="scale",
        )
    )
    root.add(
        Rect(
            id="eraser_body",
            x=ERASER_X,
            y=ERASER_Y,
            width=ERASER_W,
            height=ERASER_H,
            rx=20,
            stroke="#111111",
            stroke_width=2,
            fill="#E5E5E5",
            semantic_role="target_object",
        )
    )
    root.add(
        Text(
            id="eraser_label",
            x=ERASER_CENTER_X,
            y=ERASER_LABEL_Y,
            text="지우개",
            font_size=42,
            font_family="Malgun Gothic",
            anchor="middle",
            fill="#000000",
            semantic_role="object_label",
        )
    )

    root.add(
        Line(
            id="dash_left",
            x1=LEFT_GUIDE_X,
            y1=GUIDE_TOP_Y,
            x2=LEFT_GUIDE_X,
            y2=GUIDE_BOTTOM_Y,
            stroke="#000000",
            stroke_width=3,
        )
    )
    root.add(
        Line(
            id="dash_right",
            x1=RIGHT_GUIDE_X,
            y1=GUIDE_TOP_Y,
            x2=RIGHT_GUIDE_X,
            y2=GUIDE_BOTTOM_Y,
            stroke="#000000",
            stroke_width=3,
        )
    )
    root.add(
        Text(
            id="answer_left_paren",
            x=ANSWER_LEFT_PAREN_X,
            y=ANSWER_PAREN_Y,
            text="(",
            font_size=54,
            font_family="Arial",
            anchor="middle",
            fill="#000000",
        )
    )
    root.add(
        Text(
            id="answer_right_paren",
            x=ANSWER_RIGHT_PAREN_X,
            y=ANSWER_PAREN_Y,
            text=")",
            font_size=54,
            font_family="Arial",
            anchor="middle",
            fill="#000000",
        )
    )

    for idx in range(16):
        tick_x = TICK_START_X + (TICK_STEP * idx)
        is_major = idx in MAJOR_INDICES
        root.add(
            Line(
                id=f"tick_{idx:02d}",
                x1=tick_x,
                y1=TICK_Y1,
                x2=tick_x,
                y2=TICK_MAJOR_Y2 if is_major else TICK_MINOR_Y2,
                stroke="#111111",
                stroke_width=6 if is_major else 5,
                semantic_role="tick_major" if is_major else "tick_minor",
            )
        )

    for value, x in MAJOR_NUMBER_X.items():
        root.add(
            Text(
                id=f"major_number_{value}",
                x=x,
                y=MAJOR_NUMBER_Y,
                text=value,
                font_size=40,
                font_family="Arial",
                anchor="middle",
                fill="#000000",
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
        "0002",
        answer_semantic_path=CURRENT_DIR / "input" / "json" / "semantic_final.json",
        answer_overrides=ANSWER_LABEL_STYLE,
    )
    print("[0002] generated:")
    print(f"  - {outputs['problem_svg']}")
    print(f"  - {outputs['answer_svg']}")

