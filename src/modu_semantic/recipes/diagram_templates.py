from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable, Mapping

from ..primitives import Line, Polygon, Text
from ..problem import Problem
from ..regions import Region


Point = tuple[float, float]
ShapeBox = tuple[float, float, float, float]


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
    draw_segment: bool = True,
) -> None:
    ux, uy = _unit(end[0] - start[0], end[1] - start[1])
    mx, my = (start[0] + end[0]) * 0.5, (start[1] + end[1]) * 0.5
    if draw_segment:
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
    else:
        add_arrow_head(
            p,
            base_id=f"{line_id}_mid_ah",
            tip=(mx, my),
            direction=(ux, uy),
            size=arrow_size,
            spread=arrow_spread,
            style=arrow_style,
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


def add_dimension_marker(
    p: Problem,
    *,
    base_id: str,
    start: Point,
    end: Point,
    cap_len: float = 44.0,
    inset: float = 4.0,
    line_style: LineStyle = LineStyle(stroke="#111111", stroke_width=2.0, semantic_role="geometry_dimension"),
    arrow_style: LineStyle = LineStyle(stroke="#111111", stroke_width=2.0, semantic_role="geometry_arrow_head"),
    arrow_size: float = 16.0,
    arrow_spread: float = 14.0,
    inward: bool = True,
    label: str | None = None,
    label_offset: Point = (20.0, 8.0),
    label_style: TextStyle = TextStyle(font_size=48, fill="#111111", semantic_role="geometry_length_label"),
) -> None:
    sx, sy = start
    ex, ey = end
    ux, uy = _unit(ex - sx, ey - sy)
    nx, ny = -uy, ux
    half_cap = cap_len * 0.5

    p.add(
        Line(
            id=f"{base_id}_line",
            x1=sx,
            y1=sy,
            x2=ex,
            y2=ey,
            semantic_role=line_style.semantic_role,
            stroke=line_style.stroke,
            stroke_width=line_style.stroke_width,
        )
    )
    p.add(
        Line(
            id=f"{base_id}_cap_start",
            x1=sx - nx * half_cap,
            y1=sy - ny * half_cap,
            x2=sx + nx * half_cap,
            y2=sy + ny * half_cap,
            semantic_role=line_style.semantic_role,
            stroke=line_style.stroke,
            stroke_width=line_style.stroke_width,
        )
    )
    p.add(
        Line(
            id=f"{base_id}_cap_end",
            x1=ex - nx * half_cap,
            y1=ey - ny * half_cap,
            x2=ex + nx * half_cap,
            y2=ey + ny * half_cap,
            semantic_role=line_style.semantic_role,
            stroke=line_style.stroke,
            stroke_width=line_style.stroke_width,
        )
    )

    if inward:
        start_tip = (sx + ux * inset, sy + uy * inset)
        start_dir = (ux, uy)
        end_tip = (ex - ux * inset, ey - uy * inset)
        end_dir = (-ux, -uy)
    else:
        start_tip = (sx + ux * inset, sy + uy * inset)
        start_dir = (-ux, -uy)
        end_tip = (ex - ux * inset, ey - uy * inset)
        end_dir = (ux, uy)

    add_arrow_head(
        p,
        base_id=f"{base_id}_arrow_start",
        tip=start_tip,
        direction=start_dir,
        size=arrow_size,
        spread=arrow_spread,
        style=arrow_style,
    )
    add_arrow_head(
        p,
        base_id=f"{base_id}_arrow_end",
        tip=end_tip,
        direction=end_dir,
        size=arrow_size,
        spread=arrow_spread,
        style=arrow_style,
    )

    if label is not None:
        mx, my = (sx + ex) * 0.5, (sy + ey) * 0.5
        lx = mx + nx * label_offset[0] + ux * label_offset[1]
        ly = my + ny * label_offset[0] + uy * label_offset[1]
        add_text_label(
            p,
            label_id=f"{base_id}_label",
            at=(lx, ly),
            text=label,
            style=label_style,
        )


def parallelogram_fourth_point(a: Point, b: Point, d: Point) -> Point:
    # For vertices ordered A-B-C-D, C = B + D - A.
    return (b[0] + d[0] - a[0], b[1] + d[1] - a[1])


def add_parallelogram_from_three_points(
    p: Problem,
    *,
    base_id: str,
    a: Point,
    b: Point,
    d: Point,
    line_style: LineStyle = LineStyle(),
) -> Point:
    c = parallelogram_fourth_point(a, b, d)
    edges = [
        ("AB", a, b),
        ("BC", b, c),
        ("CD", c, d),
        ("DA", d, a),
    ]
    for suffix, s, e in edges:
        p.add(
            Line(
                id=f"{base_id}_{suffix}",
                x1=s[0],
                y1=s[1],
                x2=e[0],
                y2=e[1],
                semantic_role=line_style.semantic_role,
                stroke=line_style.stroke,
                stroke_width=line_style.stroke_width,
            )
        )
    return c


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


def _anchor_point(box: ShapeBox, anchor: str) -> tuple[float, float]:
    x, y, width, height = box
    if anchor == "left_mid":
        return (x, y + (height / 2.0))
    if anchor == "right_mid":
        return (x + width, y + (height / 2.0))
    if anchor == "top_mid":
        return (x + (width / 2.0), y)
    if anchor == "bottom_mid":
        return (x + (width / 2.0), y + height)
    raise ValueError(f"Unsupported anchor: {anchor}")


def _control_point_from_bend(start: tuple[float, float], end: tuple[float, float], bend: float) -> tuple[float, float]:
    sx, sy = start
    ex, ey = end
    mx = (sx + ex) / 2.0
    my = (sy + ey) / 2.0
    vx = ex - sx
    vy = ey - sy
    dist = math.hypot(vx, vy) or 1.0
    nx = -vy / dist
    ny = vx / dist
    return (mx + (nx * dist * bend), my + (ny * dist * bend))


def add_curved_connector(
    root: Region,
    *,
    aid: str,
    start: tuple[float, float],
    end: tuple[float, float],
    control: tuple[float, float] | None = None,
    bend: float = 0.2,
    arrow: bool = True,
    segments: int = 14,
    stroke: str = "#222222",
    stroke_width: float = 2.0,
    semantic_role: str = "guide",
) -> None:
    cx, cy = control if control is not None else _control_point_from_bend(start, end, bend)
    x0, y0 = start
    x1, y1 = end

    points: list[tuple[float, float]] = []
    for i in range(segments + 1):
        t = i / segments
        omt = 1.0 - t
        x = (omt * omt * x0) + (2 * omt * t * cx) + (t * t * x1)
        y = (omt * omt * y0) + (2 * omt * t * cy) + (t * t * y1)
        points.append((x, y))

    for i in range(segments):
        a = points[i]
        b = points[i + 1]
        root.add(
            Line(
                id=f"{aid}_{i:02d}",
                x1=a[0],
                y1=a[1],
                x2=b[0],
                y2=b[1],
                stroke=stroke,
                stroke_width=stroke_width,
                semantic_role=semantic_role,
            )
        )

    if not arrow:
        return

    tx = points[-1][0] - points[-2][0]
    ty = points[-1][1] - points[-2][1]
    norm = math.hypot(tx, ty) or 1.0
    ux = tx / norm
    uy = ty / norm
    px = -uy
    py = ux
    hx, hy = points[-1]
    size = 7.0
    root.add(
        Polygon(
            id=f"{aid}_head",
            points=[
                (hx, hy),
                (hx - (ux * size) + (px * 4.5), hy - (uy * size) + (py * 4.5)),
                (hx - (ux * size) - (px * 4.5), hy - (uy * size) - (py * 4.5)),
            ],
            fill=stroke,
            stroke=stroke,
            stroke_width=1,
            semantic_role=semantic_role,
        )
    )


def add_curved_connector_by_anchor(
    root: Region,
    *,
    aid: str,
    boxes: Mapping[str, ShapeBox],
    from_box: str,
    from_anchor: str,
    to_box: str,
    to_anchor: str,
    control: tuple[float, float] | None = None,
    bend: float = 0.2,
    arrow: bool = True,
    segments: int = 14,
    stroke: str = "#222222",
    stroke_width: float = 2.0,
    semantic_role: str = "guide",
) -> None:
    start = _anchor_point(boxes[from_box], from_anchor)
    end = _anchor_point(boxes[to_box], to_anchor)
    add_curved_connector(
        root,
        aid=aid,
        start=start,
        end=end,
        control=control,
        bend=bend,
        arrow=arrow,
        segments=segments,
        stroke=stroke,
        stroke_width=stroke_width,
        semantic_role=semantic_role,
    )
