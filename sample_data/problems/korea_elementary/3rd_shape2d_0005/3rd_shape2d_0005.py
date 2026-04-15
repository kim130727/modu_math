from pathlib import Path
import math
import sys

from modu_semantic import Line, Problem, Rect, Region, Text

CANVAS_W = 430  # 516 / 1.2
CANVAS_H = 280  # 233 * 1.2

PROBLEM_ID = "3rd_shape2d_0005"
PROBLEM_TYPE = "shape2d_square_perimeter"
TITLE_TEXT = "정사각형 둘레 구하기"
INSTRUCTION_TEXT = "한 변의 길이가 6 cm인 정사각형의 네 변의 길이의 합은 몇 cm인지 구하세요."


def _wrap_text_by_width(text: str, *, font_size: float, max_width: float) -> list[str]:
    if not text:
        return [""]
    approx_char_w = font_size * 0.92
    max_chars = max(1, int(max_width / approx_char_w))
    words = text.split(" ")
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = word if not current else f"{current} {word}"
        if len(candidate) <= max_chars:
            current = candidate
        else:
            if current:
                lines.append(current)
                current = word
            else:
                for i in range(0, len(word), max_chars):
                    chunk = word[i : i + max_chars]
                    if len(chunk) == max_chars:
                        lines.append(chunk)
                    else:
                        current = chunk
    if current:
        lines.append(current)
    return lines or [text]


def _circle_from_three_points(
    p1: tuple[float, float], p2: tuple[float, float], p3: tuple[float, float]
) -> tuple[float, float, float] | None:
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    d = (2.0 * ((x1 * (y2 - y3)) + (x2 * (y3 - y1)) + (x3 * (y1 - y2))))
    if abs(d) < 1e-6:
        return None
    ux = (
        ((x1 * x1 + y1 * y1) * (y2 - y3))
        + ((x2 * x2 + y2 * y2) * (y3 - y1))
        + ((x3 * x3 + y3 * y3) * (y1 - y2))
    ) / d
    uy = (
        ((x1 * x1 + y1 * y1) * (x3 - x2))
        + ((x2 * x2 + y2 * y2) * (x1 - x3))
        + ((x3 * x3 + y3 * y3) * (x2 - x1))
    ) / d
    r = math.hypot(x1 - ux, y1 - uy)
    return ux, uy, r


def _norm_angle(a: float) -> float:
    two_pi = 2.0 * math.pi
    return (a % two_pi + two_pi) % two_pi


def _ccw_delta(a0: float, a1: float) -> float:
    return (_norm_angle(a1) - _norm_angle(a0)) % (2.0 * math.pi)


def _is_on_ccw_path(a0: float, a1: float, am: float) -> bool:
    return _ccw_delta(a0, am) <= _ccw_delta(a0, a1) + 1e-6


def _add_dashed_arc_3pt(
    root: Region,
    *,
    arc_id: str,
    start: tuple[float, float],
    end: tuple[float, float],
    through: tuple[float, float],
    dash_deg: float = 8.0,
    gap_deg: float = 7.0,
) -> None:
    circle = _circle_from_three_points(start, through, end)
    if circle is None:
        return
    cx, cy, r = circle
    a0 = math.atan2(start[1] - cy, start[0] - cx)
    a1 = math.atan2(end[1] - cy, end[0] - cx)
    am = math.atan2(through[1] - cy, through[0] - cx)
    use_ccw = _is_on_ccw_path(a0, a1, am)

    dash = math.radians(dash_deg)
    gap = math.radians(gap_deg)
    step = dash + gap
    total = _ccw_delta(a0, a1) if use_ccw else _ccw_delta(a1, a0)

    angle = 0.0
    seg_idx = 0
    while angle < total - 1e-6:
        if use_ccw:
            s = a0 + angle
            e = a0 + min(angle + dash, total)
        else:
            s = a0 - angle
            e = a0 - min(angle + dash, total)
        x1 = cx + (r * math.cos(s))
        y1 = cy + (r * math.sin(s))
        x2 = cx + (r * math.cos(e))
        y2 = cy + (r * math.sin(e))
        root.add(
            Line(
                id=f"{arc_id}_{seg_idx:02d}",
                x1=x1,
                y1=y1,
                x2=x2,
                y2=y2,
                stroke="#7A7A7A",
                stroke_width=1.4,
                semantic_role="guide",
            )
        )
        seg_idx += 1
        angle += step


def build() -> Problem:
    p = Problem(width=CANVAS_W, height=CANVAS_H, problem_id=PROBLEM_ID, problem_type=PROBLEM_TYPE)
    p.title = TITLE_TEXT
    p.set_domain(
        {
            "instruction": INSTRUCTION_TEXT,
            "shape": "square",
            "side_length_cm": 6,
            "perimeter_cm": 24,
        }
    )
    p.set_answer(
        blanks=[],
        choices=[],
        answer_key=[{"target": "answer_value", "value": "24"}],
    )

    root = Region(id="problem_root", x=0, y=0, width=CANVAS_W, height=CANVAS_H, visible_debug=False)
    root.add(
        Rect(
            id="bg",
            x=0,
            y=0,
            width=CANVAS_W,
            height=CANVAS_H,
            fill="#F4F4F4",
            stroke="none",
            stroke_width=0,
            semantic_role="background",
        )
    )

    lines = _wrap_text_by_width(INSTRUCTION_TEXT, font_size=17, max_width=404)
    for i, line in enumerate(lines, start=1):
        root.add(
            Text(
                id=f"instruction_{i}",
                x=6,
                y=34 + ((i - 1) * 32),
                text=line,
                font_size=17,
                font_family="Malgun Gothic",
                fill="#222222",
                anchor="start",
                semantic_role="instruction",
            )
        )

    sx = 150
    sy = 98
    sw = 136
    root.add(
        Rect(
            id="square",
            x=sx,
            y=sy,
            width=sw,
            height=sw,
            fill="none",
            stroke="#2E2E2E",
            stroke_width=2.4,
            semantic_role="shape",
        )
    )

    _add_dashed_arc_3pt(
        root,
        arc_id="side_length_arc",
        start=(sx + sw, sy),
        end=(sx + sw, sy + sw),
        through=(sx + sw + 16, sy + (sw / 2)),
    )
    root.add(
        Text(
            id="side_length",
            x=sx + sw + 20,
            y=sy + 62,
            text="6 cm",
            font_size=17,
            font_family="Malgun Gothic",
            fill="#222222",
            anchor="start",
            semantic_role="label",
        )
    )

    # Invisible anchor for answer overlay in answer.svg only.
    root.add(
        Rect(
            id="answer_value",
            x=364,
            y=214,
            width=48,
            height=30,
            fill="none",
            stroke="none",
            stroke_width=0,
            semantic_role="answer_anchor",
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
        PROBLEM_ID,
        answer_overrides={"answer_overlay_numeric_font_size": 30},
    )
    print("[3rd_shape2d_0005] generated:")
    print(f"  - {outputs['svg']}")
    print(f"  - {outputs['answer_svg']}")
