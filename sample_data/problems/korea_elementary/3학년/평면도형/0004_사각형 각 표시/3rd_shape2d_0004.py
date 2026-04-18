from pathlib import Path
import math
import sys

from modu_semantic import Line, Problem, Rect, Region, Text

CANVAS_W = 440
CANVAS_H = 279

PROBLEM_ID = "3rd_shape2d_0004"
PROBLEM_TYPE = "shape2d_rectangle_find_missing_lengths"
TITLE_TEXT = "직사각형 변의 길이"
INSTRUCTION_TEXT = "다음은 직사각형입니다. □ 안에 알맞은 수를 써넣으세요."


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


def _add_instruction(root: Region) -> None:
    lines = _wrap_text_by_width(INSTRUCTION_TEXT, font_size=17, max_width=398)
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


def _add_dashed_arc(
    root: Region,
    *,
    arc_id: str,
    cx: float,
    cy: float,
    r: float,
    start_deg: float,
    end_deg: float,
    dash_deg: float = 7.0,
    gap_deg: float = 6.0,
) -> None:
    angle = start_deg
    seg_idx = 0
    while angle < end_deg:
        a1 = math.radians(angle)
        a2 = math.radians(min(angle + dash_deg, end_deg))
        x1 = cx + (r * math.cos(a1))
        y1 = cy + (r * math.sin(a1))
        x2 = cx + (r * math.cos(a2))
        y2 = cy + (r * math.sin(a2))
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
        angle += (dash_deg + gap_deg)


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


def _cw_delta(a0: float, a1: float) -> float:
    return (_norm_angle(a0) - _norm_angle(a1)) % (2.0 * math.pi)


def _is_on_ccw_path(a0: float, a1: float, am: float) -> bool:
    return _ccw_delta(a0, am) <= _ccw_delta(a0, a1) + 1e-6


def _add_dashed_arc_3pt(
    root: Region,
    *,
    arc_id: str,
    start: tuple[float, float],
    end: tuple[float, float],
    through: tuple[float, float],
    dash_deg: float = 7.0,
    gap_deg: float = 6.0,
) -> None:
    circle = _circle_from_three_points(start, through, end)
    if circle is None:
        return

    cx, cy, r = circle
    a0 = math.atan2(start[1] - cy, start[0] - cx)
    a1 = math.atan2(end[1] - cy, end[0] - cx)
    am = math.atan2(through[1] - cy, through[0] - cx)

    dash = math.radians(dash_deg)
    gap = math.radians(gap_deg)
    step = dash + gap

    if _is_on_ccw_path(a0, a1, am):
        total = _ccw_delta(a0, a1)
        angle = 0.0
        seg_idx = 0
        while angle < total - 1e-6:
            a_start = a0 + angle
            a_end = a0 + min(angle + dash, total)
            x1 = cx + (r * math.cos(a_start))
            y1 = cy + (r * math.sin(a_start))
            x2 = cx + (r * math.cos(a_end))
            y2 = cy + (r * math.sin(a_end))
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
        return

    total = _cw_delta(a0, a1)
    angle = 0.0
    seg_idx = 0
    while angle < total - 1e-6:
        a_start = a0 - angle
        a_end = a0 - min(angle + dash, total)
        x1 = cx + (r * math.cos(a_start))
        y1 = cy + (r * math.sin(a_start))
        x2 = cx + (r * math.cos(a_end))
        y2 = cy + (r * math.sin(a_end))
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
            "shape": "rectangle",
            "given_lengths_cm": {"left": 7, "bottom": 5},
            "unknown_lengths_cm": {"top": 5, "right": 7},
        }
    )
    p.set_answer(
        blanks=[],
        choices=[],
        answer_key=[
            {"target": "answer_top", "value": "5"},
            {"target": "answer_right", "value": "7"},
        ],
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
    _add_instruction(root)

    # Main rectangle
    rx = 146
    ry = 120
    rw = 92
    rh = 120
    root.add(
        Rect(
            id="main_rect",
            x=rx,
            y=ry,
            width=rw,
            height=rh,
            fill="none",
            stroke="#2E2E2E",
            stroke_width=2.4,
            semantic_role="shape",
        )
    )

    # Dashed guide arcs: smooth outer curves (top/right/bottom/left), matching PNG.
    tl = (rx, ry)
    tr = (rx + rw, ry)
    br = (rx + rw, ry + rh)
    bl = (rx, ry + rh)
    _add_dashed_arc_3pt(root, arc_id="guide_top", start=tl, end=tr, through=(192, 94))
    _add_dashed_arc_3pt(root, arc_id="guide_right", start=tr, end=br, through=(279, 180))
    _add_dashed_arc_3pt(root, arc_id="guide_bottom", start=br, end=bl, through=(192, 250))
    _add_dashed_arc_3pt(root, arc_id="guide_left", start=bl, end=tl, through=(122, 180))

    # Given labels
    root.add(
        Text(
            id="label_left",
            x=92,
            y=187,
            text="7 cm",
            font_size=17,
            font_family="Malgun Gothic",
            fill="#222222",
            anchor="start",
            semantic_role="label",
        )
    )
    root.add(
        Text(
            id="label_bottom",
            x=167,
            y=268,
            text="5 cm",
            font_size=17,
            font_family="Malgun Gothic",
            fill="#222222",
            anchor="start",
            semantic_role="label",
        )
    )

    # Top blank and unit
    root.add(
        Rect(
            id="answer_top",
            x=159,
            y=76,
            width=39,
            height=34,
            fill="none",
            stroke="#595959",
            stroke_width=1.5,
            semantic_role="answer_anchor",
        )
    )
    root.add(
        Text(
            id="unit_top",
            x=202,
            y=99,
            text="cm",
            font_size=17,
            font_family="Malgun Gothic",
            fill="#222222",
            anchor="start",
            semantic_role="label",
        )
    )

    # Right blank and unit
    root.add(
        Rect(
            id="answer_right",
            x=245,
            y=163,
            width=39,
            height=34,
            fill="none",
            stroke="#595959",
            stroke_width=1.5,
            semantic_role="answer_anchor",
        )
    )
    root.add(
        Text(
            id="unit_right",
            x=292,
            y=190,
            text="cm",
            font_size=17,
            font_family="Malgun Gothic",
            fill="#222222",
            anchor="start",
            semantic_role="label",
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
    print("[3rd_shape2d_0004] generated:")
    print(f"  - {outputs['svg']}")
    print(f"  - {outputs['answer_svg']}")
