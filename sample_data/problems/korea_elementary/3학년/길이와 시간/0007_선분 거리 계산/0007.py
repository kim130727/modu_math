"""문제 0007 DSL 빌드 파일. 선분 점/곡선 가이드/거리 라벨을 조합해 거리 문제를 구성합니다."""

from pathlib import Path
import sys

from modu_semantic import Circle, Line, Problem, Region, Text

POINT_LABELS = ["ㄱ", "ㄴ", "ㄷ", "ㄹ"]
INSTRUCTION_TEXT = "ㄱ에서 ㄹ까지의 거리를 구해 보세요."
ANSWER_LABEL_STYLE = {
    "answer_label_x": 1400,
    "answer_label_y": 250,
    "answer_label_font_size": 52,
    "answer_label_anchor": "start",
    "answer_label_baseline": "hanging",
}

# 레이아웃 상수
CANVAS_W = 1464
CANVAS_H = 382

INSTRUCTION_X = 20
INSTRUCTION_Y = 76

LINE_START_X = 188.0
POINT_N_X = 420.9537712895377
POINT_D_X = 851.1240875912408
LINE_END_X = 1276.0
LINE_Y = 249

TICK_TOP_Y = 218
TICK_BOTTOM_Y = 279

LABEL_CIRCLE_Y = 316
LABEL_CIRCLE_R = 22
LABEL_TEXT_Y = 327

TOP_CURVE_BASE_NEAR_LINE = 244
TOP_CURVE_BASE_UPPER = 236
TOP_CURVE_APEX_SHORT = 208
TOP_CURVE_APEX_LONG = 192
BOTTOM_CURVE_BASE = 307
BOTTOM_CURVE_APEX = 342


def _add_point(root: Region, *, idx: int, x: float, label: str) -> None:
    root.add(
        Line(
            id=f"tick_p{idx}",
            x1=x,
            y1=TICK_TOP_Y,
            x2=x,
            y2=TICK_BOTTOM_Y,
            stroke="#2E2A2D",
            stroke_width=4,
            semantic_role="point_tick",
        )
    )
    root.add(
        Circle(
            id=f"label_circle_p{idx}",
            cx=x,
            cy=LABEL_CIRCLE_Y,
            r=LABEL_CIRCLE_R,
            stroke="#3A3336",
            stroke_width=3,
            fill="none",
            semantic_role="point_label",
        )
    )
    root.add(
        Text(
            id=f"label_p{idx}",
            x=x,
            y=LABEL_TEXT_Y,
            text=label,
            font_size=34,
            font_family="Malgun Gothic",
            anchor="middle",
            fill="#222222",
            semantic_role="point_name",
        )
    )


def _curve_y(t: float, *, base_y: float, apex_y: float) -> float:
    return apex_y + ((base_y - apex_y) * ((2.0 * t - 1.0) ** 2))


def _add_measure_curve(
    root: Region,
    *,
    seg_prefix: str,
    x1: float,
    x2: float,
    base_y: float,
    apex_y: float,
    seg_count: int = 28,
) -> None:
    for i in range(0, seg_count, 2):
        t1 = i / seg_count
        t2 = (i + 1) / seg_count
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
                stroke="#0FA9F4",
                stroke_width=3,
                semantic_role="measurement_guide",
            )
        )


# 레이아웃 상수
def build() -> Problem:
    p = Problem(width=CANVAS_W, height=CANVAS_H, problem_id="0007", problem_type="distance_on_line")
    root = Region(id="problem_root", x=0, y=0, width=CANVAS_W, height=CANVAS_H, visible_debug=False)

    root.add(
        Text(
            id="instruction",
            x=INSTRUCTION_X,
            y=INSTRUCTION_Y,
            text=INSTRUCTION_TEXT,
            font_size=64,
            font_family="Malgun Gothic",
            anchor="start",
            fill="#222222",
            semantic_role="instruction",
        )
    )
    root.add(
        Line(
            id="base_line",
            x1=LINE_START_X,
            y1=LINE_Y,
            x2=LINE_END_X,
            y2=LINE_Y,
            stroke="#2E2A2D",
            stroke_width=5,
            semantic_role="number_line",
        )
    )

    _add_point(root, idx=0, x=LINE_START_X, label=POINT_LABELS[0])
    _add_point(root, idx=1, x=POINT_N_X, label=POINT_LABELS[1])
    _add_point(root, idx=2, x=POINT_D_X, label=POINT_LABELS[2])
    _add_point(root, idx=3, x=LINE_END_X, label=POINT_LABELS[3])

    _add_measure_curve(
        root,
        seg_prefix="dist_p0_p1",
        x1=LINE_START_X,
        x2=POINT_N_X,
        base_y=TOP_CURVE_BASE_NEAR_LINE,
        apex_y=TOP_CURVE_APEX_SHORT,
    )
    _add_measure_curve(
        root,
        seg_prefix="dist_p1_p3",
        x1=POINT_N_X,
        x2=LINE_END_X,
        base_y=TOP_CURVE_BASE_UPPER,
        apex_y=TOP_CURVE_APEX_LONG,
    )
    _add_measure_curve(
        root,
        seg_prefix="dist_p1_p2",
        x1=POINT_N_X,
        x2=POINT_D_X,
        base_y=BOTTOM_CURVE_BASE,
        apex_y=BOTTOM_CURVE_APEX,
    )

    root.add(
        Text(
            id="dist_p0_p1_text",
            x=(LINE_START_X + POINT_N_X) / 2,
            y=198,
            text="176 cm",
            font_size=58,
            font_family="Cambria",
            anchor="middle",
            fill="#222222",
            semantic_role="distance_label",
        )
    )
    root.add(
        Text(
            id="dist_p1_p3_text",
            x=(POINT_N_X + LINE_END_X) / 2,
            y=192,
            text="646 cm",
            font_size=58,
            font_family="Cambria",
            anchor="middle",
            fill="#222222",
            semantic_role="distance_label",
        )
    )
    root.add(
        Text(
            id="dist_p1_p2_text",
            x=(POINT_N_X + POINT_D_X) / 2,
            y=334,
            text="325 cm",
            font_size=58,
            font_family="Cambria",
            anchor="middle",
            fill="#222222",
            semantic_role="distance_label",
        )
    )

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
        "0007",
        answer_semantic_path=CURRENT_DIR / "input" / "json" / "semantic_final.json",
        answer_overrides=ANSWER_LABEL_STYLE,
    )
    print("[0007] generated:")
    print(f"  - {outputs['problem_svg']}")
    print(f"  - {outputs['answer_svg']}")
