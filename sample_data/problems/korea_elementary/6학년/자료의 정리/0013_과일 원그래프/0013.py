from pathlib import Path
import sys
import math

from modu_semantic import Line, Polygon, Problem, Region, Text

CANVAS_W = 805
CANVAS_H = 591

ANSWER_LABEL_STYLE = {
    "use_answer_label": True,
    "answer_label_top_right": False,
    "answer_label_x": CANVAS_W - 24,
    "answer_label_y": CANVAS_H - 28,
    "answer_label_anchor": "end",
    "answer_label_baseline": "auto",
    "answer_label_font_size": 30,
}

# 텍스트
Q_LINES = [
    "준호네 학교 학생들이 좋아하는 과일을 조사한 원그래프입니다.",
    "바나나를 좋아하는 학생이 60명이면 전체 학생 수는",
    "몇 명인가요?",
]
TITLE_TEXT = "좋아하는 과일별 학생 수"

# 원그래프 기본값
CX = 400.0
CY = 392.0
R = 140.0

# 과일별 비율(%) - 합 100
# banana = 15% -> 60명이면 전체 400명
SECTORS = [
    ("사과", 25.0, "#EFEFEF"),
    ("포도", 20.0, "#E8E8E8"),
    ("바나나", 15.0, "#DDDDDD"),
    ("복숭아", 20.0, "#C9C9C9"),
    ("기타", 20.0, "#B3B3B3"),
]


def _pt(cx: float, cy: float, r: float, deg: float) -> tuple[float, float]:
    rad = math.radians(deg)
    return cx + (r * math.cos(rad)), cy + (r * math.sin(rad))


def _sector_polygon_points(cx: float, cy: float, r: float, start_deg: float, end_deg: float, steps: int = 20) -> list[tuple[float, float]]:
    points: list[tuple[float, float]] = [(cx, cy)]
    for i in range(steps + 1):
        t = i / steps
        deg = start_deg + ((end_deg - start_deg) * t)
        points.append(_pt(cx, cy, r, deg))
    return points


def _mid_angle(start_deg: float, end_deg: float) -> float:
    return (start_deg + end_deg) / 2.0


def build() -> Problem:
    p = Problem(width=CANVAS_W, height=CANVAS_H, problem_id="0013", problem_type="pie_chart_total_from_part")
    p.title = TITLE_TEXT

    p.set_domain(
        {
            "instruction": Q_LINES[0],
            "question": " ".join(Q_LINES[1:]),
            "title": TITLE_TEXT,
            "banana_count": 60,
            "banana_ratio_percent": 15,
            "answer_value": 400,
        }
    )
    p.set_answer(
        blanks=[{"id": "value", "kind": "numeric", "value": "400"}],
        choices=[],
        answer_key=[{"target": "value", "value": "400"}],
    )

    root = Region(id="problem_root", x=0, y=0, width=CANVAS_W, height=CANVAS_H, visible_debug=False)

    root.add(
        Text(
            id="q1",
            x=14,
            y=44,
            text=Q_LINES[0],
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
            x=14,
            y=94,
            text=Q_LINES[1],
            font_size=30,
            font_family="Malgun Gothic",
            fill="#222222",
            anchor="start",
            semantic_role="instruction",
        )
    )
    root.add(
        Text(
            id="q3",
            x=14,
            y=142,
            text=Q_LINES[2],
            font_size=30,
            font_family="Malgun Gothic",
            fill="#222222",
            anchor="start",
            semantic_role="instruction",
        )
    )

    root.add(
        Text(
            id="title",
            x=206,
            y=204,
            text=TITLE_TEXT,
            font_size=32,
            font_family="Malgun Gothic",
            fill="#222222",
            anchor="start",
            semantic_role="label",
        )
    )

    # 0도 = 위쪽(12시)로 맞추기 위해 -90도부터 시작
    start_deg = -90.0
    for idx, (name, ratio, color) in enumerate(SECTORS, start=1):
        sweep = ratio * 3.6
        end_deg = start_deg + sweep

        root.add(
            Polygon(
                id=f"sector_{idx}",
                points=_sector_polygon_points(CX, CY, R, start_deg, end_deg, steps=28),
                fill=color,
                stroke="#222222",
                stroke_width=1.6,
                semantic_role="chart_sector",
            )
        )

        # 방사선
        sx, sy = _pt(CX, CY, R, start_deg)
        root.add(
            Line(
                id=f"radial_{idx}",
                x1=CX,
                y1=CY,
                x2=sx,
                y2=sy,
                stroke="#222222",
                stroke_width=1.6,
                semantic_role="chart_radial",
            )
        )

        # 과일명 라벨
        mid = _mid_angle(start_deg, end_deg)
        tx, ty = _pt(CX, CY, R * 0.62, mid)
        root.add(
            Text(
                id=f"fruit_{idx}",
                x=tx,
                y=ty,
                text=name,
                font_size=26,
                font_family="Malgun Gothic",
                fill="#222222",
                anchor="middle",
                semantic_role="chart_label",
            )
        )

        start_deg = end_deg

    # 원 둘레 눈금(5% 단위)
    for k in range(20):
        deg = -90.0 + (k * 18.0)
        x1, y1 = _pt(CX, CY, R - 1, deg)
        x2, y2 = _pt(CX, CY, R - 14, deg)
        root.add(
            Line(
                id=f"tick_{k:02d}",
                x1=x1,
                y1=y1,
                x2=x2,
                y2=y2,
                stroke="#222222",
                stroke_width=1.4,
                semantic_role="scale_tick",
            )
        )

    # 기준 눈금 숫자(0, 25, 50, 75)
    scale_specs = [("0", -90.0), ("25", 0.0), ("50", 90.0), ("75", 180.0)]
    for sid, (label, deg) in enumerate(scale_specs):
        tx, ty = _pt(CX, CY, R + 25, deg)
        if label == "0":
            ty += 14
        else:
            ty += 8
        root.add(
            Text(
                id=f"scale_{label}",
                x=tx,
                y=ty,
                text=label,
                font_size=30,
                font_family="Malgun Gothic",
                fill="#222222",
                anchor="middle",
                semantic_role="scale_label",
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
        "0013",
        answer_semantic_path=CURRENT_DIR / "input" / "json" / "semantic_final.json",
        answer_overrides=ANSWER_LABEL_STYLE,
    )
    print("[0013] generated:")
    print(f"  - {outputs['problem_svg']}")
    print(f"  - {outputs['answer_svg']}")
