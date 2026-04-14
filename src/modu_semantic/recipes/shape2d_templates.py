from __future__ import annotations

import math
from typing import Mapping, Sequence

from ..primitives import Circle, Line, Polygon, Text
from ..regions import Region

Point = tuple[float, float]


def quarter_sector_points(*, cx: float, cy: float, r: float, steps: int = 20) -> list[Point]:
    points: list[Point] = [(cx, cy - r)]
    for i in range(steps + 1):
        theta = (-90.0 + (90.0 * i / steps)) * math.pi / 180.0
        points.append((cx + (r * math.cos(theta)), cy + (r * math.sin(theta))))
    points.append((cx, cy))
    return points


def regular_polygon_points(*, cx: float, cy: float, r: float, sides: int, rotation_deg: float = -90.0) -> list[Point]:
    if sides < 3:
        raise ValueError("sides must be >= 3")
    points: list[Point] = []
    for i in range(sides):
        theta = (rotation_deg + (360.0 * i / sides)) * math.pi / 180.0
        points.append((cx + (r * math.cos(theta)), cy + (r * math.sin(theta))))
    return points


def make_vertex_map(*, vertex_ids: Sequence[str], points: Sequence[Point]) -> dict[str, Point]:
    if len(vertex_ids) != len(points):
        raise ValueError("vertex_ids length must match points length")
    return {vertex_ids[i]: points[i] for i in range(len(points))}


def add_polygon_with_vertices(
    root: Region,
    *,
    shape_id: str,
    points: Sequence[Point],
    vertex_ids: Sequence[str] | None = None,
    stroke: str = "#2F2F2F",
    stroke_width: float = 2.2,
    fill: str = "none",
    semantic_role: str = "shape",
) -> dict[str, Point]:
    root.add(
        Polygon(
            id=shape_id,
            points=list(points),
            fill=fill,
            stroke=stroke,
            stroke_width=stroke_width,
            semantic_role=semantic_role,
        )
    )
    if vertex_ids is None:
        vertex_ids = [f"v{i + 1}" for i in range(len(points))]
    return make_vertex_map(vertex_ids=vertex_ids, points=points)


def add_segment_by_vertices(
    root: Region,
    *,
    segment_id: str,
    vertices: Mapping[str, Point],
    start_vertex: str,
    end_vertex: str,
    stroke: str = "#222222",
    stroke_width: float = 2.4,
    semantic_role: str = "given_segment",
    ) -> None:
    x1, y1 = vertices[start_vertex]
    x2, y2 = vertices[end_vertex]
    root.add(
        Line(
            id=segment_id,
            x1=x1,
            y1=y1,
            x2=x2,
            y2=y2,
            stroke=stroke,
            stroke_width=stroke_width,
            semantic_role=semantic_role,
        )
    )


def add_segment_by_points(
    root: Region,
    *,
    segment_id: str,
    start: Point,
    end: Point,
    stroke: str = "#222222",
    stroke_width: float = 2.4,
    semantic_role: str = "shape_internal_segment",
    dashed: bool = False,
    dash_len: float = 6.0,
    gap_len: float = 4.0,
) -> None:
    if not dashed:
        root.add(
            Line(
                id=segment_id,
                x1=start[0],
                y1=start[1],
                x2=end[0],
                y2=end[1],
                stroke=stroke,
                stroke_width=stroke_width,
                semantic_role=semantic_role,
            )
        )
        return

    dx = end[0] - start[0]
    dy = end[1] - start[1]
    dist = math.hypot(dx, dy)
    if dist <= 0.01:
        return
    ux = dx / dist
    uy = dy / dist
    step = dash_len + gap_len
    pos = 0.0
    seg = 0
    while pos < dist - 1e-6:
        end_pos = min(pos + dash_len, dist)
        sx = start[0] + (ux * pos)
        sy = start[1] + (uy * pos)
        ex = start[0] + (ux * end_pos)
        ey = start[1] + (uy * end_pos)
        root.add(
            Line(
                id=f"{segment_id}_{seg:02d}",
                x1=sx,
                y1=sy,
                x2=ex,
                y2=ey,
                stroke=stroke,
                stroke_width=stroke_width,
                semantic_role=semantic_role,
            )
        )
        seg += 1
        pos += step


def add_segment_set_by_points(
    root: Region,
    *,
    segments: Sequence[tuple[Point, Point]],
    id_prefix: str = "seg",
    stroke: str = "#222222",
    stroke_width: float = 2.4,
    semantic_role: str = "shape_internal_segment",
    dashed: bool = False,
    dash_len: float = 6.0,
    gap_len: float = 4.0,
) -> None:
    for i, (start, end) in enumerate(segments, start=1):
        add_segment_by_points(
            root,
            segment_id=f"{id_prefix}_{i}",
            start=start,
            end=end,
            stroke=stroke,
            stroke_width=stroke_width,
            semantic_role=semantic_role,
            dashed=dashed,
            dash_len=dash_len,
            gap_len=gap_len,
        )


def add_vertex_markers(
    root: Region,
    *,
    vertices: Mapping[str, Point],
    id_prefix: str,
    radius: float = 3.5,
    fill: str = "#222222",
    stroke: str = "none",
    stroke_width: float = 0.0,
    semantic_role: str = "point",
) -> None:
    for vid, (x, y) in vertices.items():
        root.add(
            Circle(
                id=f"{id_prefix}_{vid}",
                cx=x,
                cy=y,
                r=radius,
                fill=fill,
                stroke=stroke,
                stroke_width=stroke_width,
                semantic_role=semantic_role,
            )
        )


def add_vertex_labels(
    root: Region,
    *,
    vertices: Mapping[str, Point],
    id_prefix: str,
    labels: Mapping[str, str] | None = None,
    dx: float = 8.0,
    dy: float = -8.0,
    font_size: float = 16.0,
    font_family: str = "Malgun Gothic",
    fill: str = "#222222",
    anchor: str = "start",
    semantic_role: str = "label",
) -> None:
    for vid, (x, y) in vertices.items():
        text = labels[vid] if labels and vid in labels else vid
        root.add(
            Text(
                id=f"{id_prefix}_{vid}",
                x=x + dx,
                y=y + dy,
                text=text,
                font_size=font_size,
                font_family=font_family,
                fill=fill,
                anchor=anchor,
                semantic_role=semantic_role,
            )
        )


def add_segment_set_by_vertices(
    root: Region,
    *,
    vertices: Mapping[str, Point],
    segments: Sequence[tuple[str, str]],
    id_prefix: str = "seg",
    stroke: str = "#222222",
    stroke_width: float = 2.4,
    semantic_role: str = "given_segment",
) -> None:
    for i, (start_vertex, end_vertex) in enumerate(segments, start=1):
        add_segment_by_vertices(
            root,
            segment_id=f"{id_prefix}_{i}",
            vertices=vertices,
            start_vertex=start_vertex,
            end_vertex=end_vertex,
            stroke=stroke,
            stroke_width=stroke_width,
            semantic_role=semantic_role,
        )


def add_point_highlights(
    root: Region,
    *,
    vertices: Mapping[str, Point],
    point_ids: Sequence[str],
    id_prefix: str = "highlight",
    radius: float = 7.0,
    stroke: str = "#666666",
    stroke_width: float = 1.6,
    fill: str = "none",
    semantic_role: str = "point_highlight",
) -> None:
    for pid in point_ids:
        x, y = vertices[pid]
        root.add(
            Circle(
                id=f"{id_prefix}_{pid}",
                cx=x,
                cy=y,
                r=radius,
                fill=fill,
                stroke=stroke,
                stroke_width=stroke_width,
                semantic_role=semantic_role,
            )
        )


def add_point_segment_graph(
    root: Region,
    *,
    points: Mapping[str, Point],
    segments: Sequence[tuple[str, str]],
    id_prefix: str = "graph",
    segment_stroke: str = "#222222",
    segment_stroke_width: float = 2.4,
    segment_semantic_role: str = "given_segment",
    show_points: bool = False,
    point_radius: float = 3.5,
    point_fill: str = "#222222",
    point_stroke: str = "none",
    point_stroke_width: float = 0.0,
    point_semantic_role: str = "point",
    show_labels: bool = False,
    labels: Mapping[str, str] | None = None,
    label_dx: float = 8.0,
    label_dy: float = -8.0,
    label_font_size: float = 16.0,
    label_font_family: str = "Malgun Gothic",
    label_fill: str = "#222222",
    label_anchor: str = "start",
    label_semantic_role: str = "label",
    highlighted_points: Sequence[str] | None = None,
    highlight_radius: float = 7.0,
    highlight_stroke: str = "#666666",
    highlight_stroke_width: float = 1.6,
    highlight_fill: str = "none",
    highlight_semantic_role: str = "point_highlight",
) -> dict[str, Point]:
    vertices = dict(points)
    add_segment_set_by_vertices(
        root,
        vertices=vertices,
        segments=segments,
        id_prefix=f"{id_prefix}_seg",
        stroke=segment_stroke,
        stroke_width=segment_stroke_width,
        semantic_role=segment_semantic_role,
    )
    if show_points:
        add_vertex_markers(
            root,
            vertices=vertices,
            id_prefix=f"{id_prefix}_pt",
            radius=point_radius,
            fill=point_fill,
            stroke=point_stroke,
            stroke_width=point_stroke_width,
            semantic_role=point_semantic_role,
        )
    if show_labels:
        add_vertex_labels(
            root,
            vertices=vertices,
            id_prefix=f"{id_prefix}_lb",
            labels=labels,
            dx=label_dx,
            dy=label_dy,
            font_size=label_font_size,
            font_family=label_font_family,
            fill=label_fill,
            anchor=label_anchor,
            semantic_role=label_semantic_role,
        )
    if highlighted_points:
        add_point_highlights(
            root,
            vertices=vertices,
            point_ids=highlighted_points,
            id_prefix=f"{id_prefix}_hl",
            radius=highlight_radius,
            stroke=highlight_stroke,
            stroke_width=highlight_stroke_width,
            fill=highlight_fill,
            semantic_role=highlight_semantic_role,
        )
    return vertices


def add_internal_segments_by_vertices(
    root: Region,
    *,
    vertices: Mapping[str, Point],
    segments: Sequence[tuple[str, str]],
    id_prefix: str = "internal",
    stroke: str = "#222222",
    stroke_width: float = 2.0,
    semantic_role: str = "shape_internal_segment",
    show_points: bool = False,
    show_labels: bool = False,
    labels: Mapping[str, str] | None = None,
    highlighted_points: Sequence[str] | None = None,
) -> dict[str, Point]:
    add_segment_set_by_vertices(
        root,
        vertices=vertices,
        segments=segments,
        id_prefix=f"{id_prefix}_seg",
        stroke=stroke,
        stroke_width=stroke_width,
        semantic_role=semantic_role,
    )
    if show_points:
        add_vertex_markers(root, vertices=vertices, id_prefix=f"{id_prefix}_pt")
    if show_labels:
        add_vertex_labels(root, vertices=vertices, id_prefix=f"{id_prefix}_lb", labels=labels)
    if highlighted_points:
        add_point_highlights(root, vertices=vertices, point_ids=highlighted_points, id_prefix=f"{id_prefix}_hl")
    return dict(vertices)
