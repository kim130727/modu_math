from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable

from ..primitives import Line, Text
from ..problem import Problem


Point = tuple[float, float]


@dataclass(frozen=True)
class LineStyle:
    stroke: str = "#222222"
    stroke_width: float = 4.0
    semantic_role: str = "geometry_edge"


@dataclass(frozen=True)
class TextStyle:
    font_size: int = 48
    fill: str = "#111111"
    semantic_role: str = "geometry_label"
    font_family: str = "Malgun Gothic"


def _unit(dx: float, dy: float) -> Point:
    norm = math.hypot(dx, dy)
    if norm <= 1e-9:
        return (1.0, 0.0)
    return (dx / norm, dy / norm)


def add_arrow_head(
    p: Problem,
    *,
    base_id: str,
    tip: Point,
    direction: Point,
    size: float = 24.0,
    spread: float = 14.0,
    style: LineStyle = LineStyle(semantic_role="geometry_arrow_head"),
) -> None:
    ux, uy = _unit(direction[0], direction[1])
    px, py = -uy, ux
    tx, ty = tip
    bx, by = tx - ux * size, ty - uy * size
    lx, ly = bx + px * spread * 0.5, by + py * spread * 0.5
    rx, ry = bx - px * spread * 0.5, by - py * spread * 0.5
    p.add(
        Line(
            id=f"{base_id}_l",
            x1=tx,
            y1=ty,
            x2=lx,
            y2=ly,
            semantic_role=style.semantic_role,
            stroke=style.stroke,
            stroke_width=style.stroke_width,
        )
    )
    p.add(
        Line(
            id=f"{base_id}_r",
            x1=tx,
            y1=ty,
            x2=rx,
            y2=ry,
            semantic_role=style.semantic_role,
            stroke=style.stroke,
            stroke_width=style.stroke_width,
        )
    )


def add_arrow_line(
    p: Problem,
    *,
    line_id: str,
    start: Point,
    end: Point,
    arrow_start: bool = False,
    arrow_end: bool = True,
    line_style: LineStyle = LineStyle(),
    arrow_style: LineStyle = LineStyle(semantic_role="geometry_arrow_head"),
    arrow_size: float = 24.0,
    arrow_spread: float = 14.0,
) -> None:
    p.add(
        Line(
            id=line_id,
            x1=start[0],
            y1=start[1],
            x2=end[0],
            y2=end[1],
            semantic_role=line_style.semantic_role,
            stroke=line_style.stroke,
            stroke_width=line_style.stroke_width,
        )
    )
    if arrow_end:
        add_arrow_head(
            p,
            base_id=f"{line_id}_end_ah",
            tip=end,
            direction=(end[0] - start[0], end[1] - start[1]),
            size=arrow_size,
            spread=arrow_spread,
            style=arrow_style,
        )
    if arrow_start:
        add_arrow_head(
            p,
            base_id=f"{line_id}_start_ah",
            tip=start,
            direction=(start[0] - end[0], start[1] - end[1]),
            size=arrow_size,
            spread=arrow_spread,
            style=arrow_style,
        )


def add_mid_arrow_marker(
    p: Problem,
    *,
    line_id: str,
    start: Point,
    end: Point,
    marker_len: float = 24.0,
    line_style: LineStyle = LineStyle(),
    arrow_style: LineStyle = LineStyle(semantic_role="geometry_arrow_head"),
    arrow_size: float = 12.0,
    arrow_spread: float = 10.0,
) -> None:
    ux, uy = _unit(end[0] - start[0], end[1] - start[1])
    mx, my = (start[0] + end[0]) * 0.5, (start[1] + end[1]) * 0.5
    s = (mx - ux * marker_len * 0.5, my - uy * marker_len * 0.5)
    e = (mx + ux * marker_len * 0.5, my + uy * marker_len * 0.5)
    add_arrow_line(
        p,
        line_id=line_id,
        start=s,
        end=e,
        arrow_start=False,
        arrow_end=True,
        line_style=line_style,
        arrow_style=arrow_style,
        arrow_size=arrow_size,
        arrow_spread=arrow_spread,
    )


def add_text_label(
    p: Problem,
    *,
    label_id: str,
    at: Point,
    text: str,
    style: TextStyle = TextStyle(),
) -> None:
    p.add(
        Text(
            id=label_id,
            x=at[0],
            y=at[1],
            text=text,
            font_size=style.font_size,
            semantic_role=style.semantic_role,
            fill=style.fill,
            font_family=style.font_family,
        )
    )


def add_degree_label(
    p: Problem,
    *,
    label_id: str,
    at: Point,
    value: str | int | float,
    style: TextStyle = TextStyle(semantic_role="geometry_angle_label"),
) -> None:
    text = str(value)
    if not text.endswith("°"):
        text = f"{text}°"
    add_text_label(p, label_id=label_id, at=at, text=text, style=style)


def add_right_angle_marker(
    p: Problem,
    *,
    marker_id: str,
    vertex: Point,
    along_1: Point,
    along_2: Point,
    size: float = 24.0,
    style: LineStyle = LineStyle(stroke="#111111", stroke_width=2.4, semantic_role="geometry_right_angle"),
) -> None:
    u1 = _unit(along_1[0] - vertex[0], along_1[1] - vertex[1])
    u2 = _unit(along_2[0] - vertex[0], along_2[1] - vertex[1])
    p1 = (vertex[0] + u1[0] * size, vertex[1] + u1[1] * size)
    p2 = (vertex[0] + u2[0] * size, vertex[1] + u2[1] * size)
    c = (p1[0] + u2[0] * size, p1[1] + u2[1] * size)

    p.add(
        Line(
            id=f"{marker_id}_1",
            x1=p1[0],
            y1=p1[1],
            x2=c[0],
            y2=c[1],
            semantic_role=style.semantic_role,
            stroke=style.stroke,
            stroke_width=style.stroke_width,
        )
    )
    p.add(
        Line(
            id=f"{marker_id}_2",
            x1=p2[0],
            y1=p2[1],
            x2=c[0],
            y2=c[1],
            semantic_role=style.semantic_role,
            stroke=style.stroke,
            stroke_width=style.stroke_width,
        )
    )


def add_segment_tick(
    p: Problem,
    *,
    tick_id: str,
    start: Point,
    end: Point,
    t: float = 0.5,
    size: float = 24.0,
    style: LineStyle = LineStyle(stroke="#E91E63", stroke_width=3.0, semantic_role="geometry_tick"),
) -> None:
    cx = start[0] + (end[0] - start[0]) * t
    cy = start[1] + (end[1] - start[1]) * t
    ux, uy = _unit(end[0] - start[0], end[1] - start[1])
    nx, ny = -uy, ux
    h = size * 0.5
    p.add(
        Line(
            id=tick_id,
            x1=cx - nx * h,
            y1=cy - ny * h,
            x2=cx + nx * h,
            y2=cy + ny * h,
            semantic_role=style.semantic_role,
            stroke=style.stroke,
            stroke_width=style.stroke_width,
        )
    )


def add_equal_length_marks(
    p: Problem,
    *,
    base_id: str,
    segments: Iterable[tuple[Point, Point]],
    t: float = 0.5,
    size: float = 24.0,
    style: LineStyle = LineStyle(stroke="#E91E63", stroke_width=3.0, semantic_role="geometry_tick"),
) -> None:
    for i, (s, e) in enumerate(segments, start=1):
        add_segment_tick(
            p,
            tick_id=f"{base_id}_{i}",
            start=s,
            end=e,
            t=t,
            size=size,
            style=style,
        )


def add_choice_block(
    p: Problem,
    *,
    base_id: str,
    x: float,
    y: float,
    choices: Iterable[str],
    separator: str = "    ",
    style: TextStyle = TextStyle(font_size=38, fill="#000000", semantic_role="multiple_choice", font_family="sans-serif"),
) -> None:
    rendered = separator.join(f"{idx + 1}. {choice}" for idx, choice in enumerate(choices))
    add_text_label(p, label_id=base_id, at=(x, y), text=rendered, style=style)
