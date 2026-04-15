from pathlib import Path
import sys

from modu_semantic import Line, Polygon, Problem, Rect, Region, Text

CANVAS_W = 800
CANVAS_H = 520

ANSWER_LABEL_STYLE = {
    "use_answer_label": True,
    "answer_label_top_right": False,
    "answer_label_x": 24,
    "answer_label_y": 500,
    "answer_label_anchor": "start",
    "answer_label_baseline": "auto",
    "answer_label_font_size": 42,
}

INSTRUCTION_LINES = [
    "다음은 각기둥의 전개도입니다.",
    "전개도를 접어서 만든 입체도형의 모서리는 모두 몇 개인가요?",
]

# 펼친 띠(옆면 6개)
STRIP_X = 250
STRIP_Y = 210
STRIP_W = 300
STRIP_H = 130
FOLD_XS = [300, 350, 400, 450, 500]

# 위/아래 육각형: 중심점 + 오프셋으로 정의(가독성 개선)
HEX_SHORT_DX = 24.534   # 중심 -> 윗/아랫변 꼭짓점 x 오프셋
HEX_LONG_DX = 54.52     # 중심 -> 좌/우 꼭짓점 x 오프셋
HEX_DY = 48.192         # 중심 -> 윗/아랫변 y 오프셋

TOP_HEX_CENTER = (375.0, 160.912)
BOT_HEX_CENTER = (375.322, 389.088)


def _hex_points(cx: float, cy: float) -> list[tuple[float, float]]:
    return [
        (cx - HEX_SHORT_DX, cy + HEX_DY),  # left-bottom
        (cx - HEX_LONG_DX, cy),            # left
        (cx - HEX_SHORT_DX, cy - HEX_DY),  # left-top
        (cx + HEX_SHORT_DX, cy - HEX_DY),  # right-top
        (cx + HEX_LONG_DX, cy),            # right
        (cx + HEX_SHORT_DX, cy + HEX_DY),  # right-bottom
    ]


def build() -> Problem:
    p = Problem(width=CANVAS_W, height=CANVAS_H, problem_id="0012", problem_type="prism_net_edge_count")
    p.title = "전개도와 모서리 수"

    # 육각기둥: 밑면 6개 모서리 + 윗면 6개 모서리 + 옆 모서리 6개 = 총 18개
    p.set_domain(
        {
            "instruction": INSTRUCTION_LINES[0],
            "question": INSTRUCTION_LINES[1],
            "prism_base_sides": 6,
            "edge_count_formula": "6+6+6",
            "answer_count": 18,
        }
    )
    p.set_answer(
        blanks=[{"id": "answer_label", "kind": "numeric", "value": "18"}],
        choices=[],
        answer_key=[{"target": "answer_label", "value": "18"}],
    )

    root = Region(id="problem_root", x=0, y=0, width=CANVAS_W, height=CANVAS_H, visible_debug=False)

    root.add(
        Text(
            id="q1",
            x=18.6,
            y=47.7,
            text=INSTRUCTION_LINES[0],
            font_size=30,
            font_family="Malgun Gothic",
            fill="#222222",
            anchor="start",
            semantic_role="instruction",
        )
    )
    root.add(
        Text(
            id="q2",
            x=16.1,
            y=89.9,
            text=INSTRUCTION_LINES[1],
            font_size=30,
            font_family="Malgun Gothic",
            fill="#222222",
            anchor="start",
            semantic_role="instruction",
        )
    )

    root.add(
        Rect(
            id="strip_rect",
            x=STRIP_X,
            y=STRIP_Y,
            width=STRIP_W,
            height=STRIP_H,
            stroke="#333333",
            stroke_width=2,
            fill="#CFCFCF",
            semantic_role="net",
        )
    )

    for idx, fx in enumerate(FOLD_XS, start=1):
        root.add(
            Line(
                id=f"fold_{idx}",
                x1=fx,
                y1=STRIP_Y,
                x2=fx,
                y2=STRIP_Y + STRIP_H,
                stroke="#333333",
                stroke_width=1,
                semantic_role="fold_line",
                metadata={"stroke_dasharray": "4 4"},
            )
        )

    root.add(
        Polygon(
            id="top_hex",
            points=_hex_points(*TOP_HEX_CENTER),
            stroke="#333333",
            stroke_width=2,
            fill="#CFCFCF",
            semantic_role="net",
        )
    )

    root.add(
        Polygon(
            id="bot_hex",
            points=_hex_points(*BOT_HEX_CENTER),
            stroke="#333333",
            stroke_width=2,
            fill="#CFCFCF",
            semantic_role="net",
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
        "0012",
        answer_semantic_path=CURRENT_DIR / "input" / "json" / "semantic_final.json",
        answer_overrides=ANSWER_LABEL_STYLE,
    )
    print("[0012] generated:")
    print(f"  - {outputs['problem_svg']}")
    print(f"  - {outputs['answer_svg']}")
