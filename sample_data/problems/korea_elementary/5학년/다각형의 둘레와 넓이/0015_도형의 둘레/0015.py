from pathlib import Path
import sys

from modu_semantic import Line, Problem, Rect, Region, Text

CANVAS_W = 980
CANVAS_H = 730

ANSWER_LABEL_STYLE = {
    "use_answer_label": True,
    "answer_label_top_right": False,
    "answer_label_x": CANVAS_W - 24,
    "answer_label_y": CANVAS_H - 24,
    "answer_label_anchor": "end",
    "answer_label_baseline": "auto",
    "answer_label_font_size": 36,
}

PROBLEM_TYPE = "rectangle_perimeter_from_square_tiling"
TITLE_TEXT = "직사각형의 둘레 구하기"

QUESTION_LINES = [
    "여러 가지 크기의 정사각형을 겹치지 않게 붙여 다음과",
    "같은 직사각형 모양도형을 만들었습니다. 색칠한 정사각형의",
    "한 변의 길이가 15cm일 때, 직사각형 모양도형의",
    "네 변의 길이의 합은 몇 cm입니까?",
    "(각 가로와 세로 정사각형의 크기는 같습니다.)",
]

SIDE_CM = 15
WIDTH_UNITS = 8
HEIGHT_UNITS = 5
PERIMETER_UNITS = 2 * (WIDTH_UNITS + HEIGHT_UNITS)
ANSWER_VALUE = SIDE_CM * PERIMETER_UNITS  # 390

# 도형 기준 좌표
X0 = 202.59975
Y0 = 346.61462
FIG_W = 448.0
FIG_H = 280.0

X_MID = X0 + 168.0
Y_MID = Y0 + 168.0
X_SMALL = X0 + 56.0
Y_SMALL = Y0 + 224.0
SMALL = 56.0


def _add_question(root: Region) -> None:
    qx = 29
    qy0 = 60
    q_step = 44
    for idx, line in enumerate(QUESTION_LINES, start=1):
        root.add(
            Text(
                id=f"q{idx}",
                x=qx,
                y=qy0 + (idx - 1) * q_step,
                text=line,
                font_size=31,
                font_family="Malgun Gothic",
                fill="#222222",
                anchor="start",
                semantic_role="instruction",
            )
        )


def _add_figure(root: Region) -> None:
    root.add(
        Line(
            id="outer_top",
            x1=X0,
            y1=Y0,
            x2=X0 + FIG_W,
            y2=Y0,
            stroke="#222222",
            stroke_width=2,
            semantic_role="segment",
        )
    )
    root.add(
        Line(
            id="outer_right",
            x1=X0 + FIG_W,
            y1=Y0,
            x2=X0 + FIG_W,
            y2=Y0 + FIG_H,
            stroke="#222222",
            stroke_width=2,
            semantic_role="segment",
        )
    )
    root.add(
        Line(
            id="outer_bottom",
            x1=X0,
            y1=Y0 + FIG_H,
            x2=X0 + FIG_W,
            y2=Y0 + FIG_H,
            stroke="#222222",
            stroke_width=2,
            semantic_role="segment",
        )
    )
    root.add(
        Line(
            id="outer_left",
            x1=X0,
            y1=Y0,
            x2=X0,
            y2=Y0 + FIG_H,
            stroke="#222222",
            stroke_width=2,
            semantic_role="segment",
        )
    )

    root.add(
        Line(
            id="v_main",
            x1=X_MID,
            y1=Y0,
            x2=X_MID,
            y2=Y0 + FIG_H,
            stroke="#222222",
            stroke_width=2,
            semantic_role="segment",
        )
    )
    root.add(
        Line(
            id="h_main",
            x1=X0,
            y1=Y_MID,
            x2=X_MID,
            y2=Y_MID,
            stroke="#222222",
            stroke_width=2,
            semantic_role="segment",
        )
    )
    root.add(
        Line(
            id="v_small",
            x1=X_SMALL,
            y1=Y_MID,
            x2=X_SMALL,
            y2=Y0 + FIG_H,
            stroke="#222222",
            stroke_width=2,
            semantic_role="segment",
        )
    )
    root.add(
        Line(
            id="h_small",
            x1=X0,
            y1=Y_SMALL,
            x2=X_SMALL,
            y2=Y_SMALL,
            stroke="#222222",
            stroke_width=2,
            semantic_role="segment",
        )
    )

    root.add(
        Rect(
            id="colored_square",
            x=X0,
            y=Y_SMALL,
            width=SMALL,
            height=SMALL,
            fill="#4E78C2",
            stroke="none",
            stroke_width=0,
            semantic_role="highlight",
        )
    )

    labels = [
        ("label_g", "ㄱ", X0 - 22.0, Y0 - 4.0),
        ("label_n", "ㄴ", X0 + FIG_W + 8.0, Y0 - 4.0),
        ("label_d", "ㄷ", X0 + FIG_W + 8.0, Y0 + FIG_H + 28.0),
        ("label_r", "ㄹ", X0 - 22.0, Y0 + FIG_H + 28.0),
    ]
    for lid, txt, x, y in labels:
        root.add(
            Text(
                id=lid,
                x=x,
                y=y,
                text=txt,
                font_size=42,
                font_family="Malgun Gothic",
                fill="#222222",
                anchor="start",
                semantic_role="label",
            )
        )


def build() -> Problem:
    p = Problem(width=CANVAS_W, height=CANVAS_H, problem_id="0015", problem_type=PROBLEM_TYPE)
    p.title = TITLE_TEXT

    p.set_domain(
        {
            "small_square_side_cm": SIDE_CM,
            "width_units": WIDTH_UNITS,
            "height_units": HEIGHT_UNITS,
            "perimeter_units": PERIMETER_UNITS,
            "computed_answer": ANSWER_VALUE,
            "instruction": " ".join(QUESTION_LINES[:2]),
            "question": " ".join(QUESTION_LINES[2:]),
            "question_lines": QUESTION_LINES,
            "render_profile": "rectangle_perimeter_from_square_tiling.v2",
        }
    )
    p.set_answer(
        blanks=[{"id": "value", "kind": "numeric", "value": str(ANSWER_VALUE)}],
        choices=[],
        answer_key=[{"target": "value", "value": str(ANSWER_VALUE)}],
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
    _add_question(root)
    _add_figure(root)
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
        "0015",
        answer_semantic_path=CURRENT_DIR / "input" / "json" / "semantic_final.json",
        answer_overrides=ANSWER_LABEL_STYLE,
    )
    print("[0015] generated:")
    print(f"  - {outputs['problem_svg']}")
    print(f"  - {outputs['answer_svg']}")
