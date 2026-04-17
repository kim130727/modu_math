from __future__ import annotations

import math
import re
from typing import Any

from . import ir


def _to_float(value: Any, *, default: float = 0.0) -> float:
    if isinstance(value, bool):
        return default
    if isinstance(value, (int, float)):
        return float(value)
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _to_str(value: Any, *, default: str = "") -> str:
    if value is None:
        return default
    return str(value)


def _to_dict(value: Any) -> dict[str, Any]:
    return dict(value) if isinstance(value, dict) else {}


def extract_logic_form(domain: dict[str, Any]) -> dict[str, Any]:
    logic = domain.get("logic_form")
    return logic if isinstance(logic, dict) else {}


def has_geometry_diagram_data(domain: dict[str, Any]) -> bool:
    logic = extract_logic_form(domain)
    points = logic.get("point_positions")
    return isinstance(points, dict) and len(points) >= 2


def parse_point_positions(logic: dict[str, Any]) -> dict[str, tuple[float, float]]:
    raw = logic.get("point_positions")
    points: dict[str, tuple[float, float]] = {}
    if not isinstance(raw, dict):
        return points
    for key, value in raw.items():
        if not isinstance(value, (list, tuple)) or len(value) != 2:
            continue
        name = _to_str(key).strip()
        if not name:
            continue
        points[name] = (_to_float(value[0]), _to_float(value[1]))
    return points


def geometry_region(canvas_w: float, canvas_h: float) -> tuple[float, float, float, float]:
    x = 40.0
    y = 200.0
    w = max(260.0, (canvas_w * 0.58) - 60.0)
    h = max(220.0, canvas_h - y - 40.0)
    return x, y, w, h


def fit_transform_for_points(
    points: dict[str, tuple[float, float]],
    *,
    target_x: float,
    target_y: float,
    target_w: float,
    target_h: float,
    padding: float = 24.0,
) -> dict[str, tuple[float, float]]:
    xs = [p[0] for p in points.values()]
    ys = [p[1] for p in points.values()]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    src_w = max(1e-6, max_x - min_x)
    src_h = max(1e-6, max_y - min_y)

    avail_w = max(20.0, target_w - (padding * 2.0))
    avail_h = max(20.0, target_h - (padding * 2.0))
    s = min(avail_w / src_w, avail_h / src_h)
    used_w = src_w * s
    used_h = src_h * s
    tx = target_x + ((target_w - used_w) / 2.0) - (min_x * s)
    ty = target_y + ((target_h - used_h) / 2.0) - (min_y * s)

    mapped: dict[str, tuple[float, float]] = {}
    for name, (x, y) in points.items():
        mapped[name] = (x * s + tx, y * s + ty)
    return mapped


def level_triangle_base_if_needed(
    *,
    source_points: dict[str, tuple[float, float]],
    mapped_points: dict[str, tuple[float, float]],
) -> dict[str, tuple[float, float]]:
    if len(source_points) != 3 or len(mapped_points) != 3:
        return mapped_points

    names = list(source_points.keys())
    pairs = [(names[0], names[1]), (names[0], names[2]), (names[1], names[2])]

    src_ys = [pt[1] for pt in source_points.values()]
    src_span_y = max(src_ys) - min(src_ys)
    if src_span_y <= 1e-6:
        return mapped_points

    best_pair: tuple[str, str] | None = None
    best_diff = float("inf")
    for a, b in pairs:
        diff = abs(source_points[a][1] - source_points[b][1])
        if diff < best_diff:
            best_diff = diff
            best_pair = (a, b)
    if best_pair is None:
        return mapped_points

    if best_diff > max(2.0, src_span_y * 0.04):
        return mapped_points

    a, b = best_pair
    apex = next((n for n in names if n not in {a, b}), None)
    if apex is None:
        return mapped_points
    pair_mean_y = (source_points[a][1] + source_points[b][1]) / 2.0
    if abs(source_points[apex][1] - pair_mean_y) < max(6.0, src_span_y * 0.12):
        return mapped_points

    adjusted = dict(mapped_points)
    level_y = (mapped_points[a][1] + mapped_points[b][1]) / 2.0
    adjusted[a] = (mapped_points[a][0], level_y)
    adjusted[b] = (mapped_points[b][0], level_y)
    return adjusted


def parse_line_instances(logic: dict[str, Any]) -> list[tuple[str, str]]:
    raw = logic.get("line_instances")
    if not isinstance(raw, list):
        return []
    edges: list[tuple[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for item in raw:
        token = _to_str(item).strip()
        if len(token) != 2:
            continue
        a, b = token[0], token[1]
        if a == b:
            continue
        key = tuple(sorted((a, b)))
        if key in seen:
            continue
        seen.add(key)
        edges.append((a, b))
    return edges


def parse_point_on_line_constraints(diagram_logic_form: list[Any]) -> list[tuple[str, str, str]]:
    out: list[tuple[str, str, str]] = []
    seen: set[tuple[str, str, str]] = set()
    canonical = re.compile(r"PointLiesOnLine\(([A-Za-z]),\s*Line\(([A-Za-z]),\s*([A-Za-z])\)\)")
    for raw in diagram_logic_form:
        line = _to_str(raw).strip()
        m = canonical.search(line)
        if m:
            p, a, b = m.group(1), m.group(2), m.group(3)
            key = (p, a, b)
            if key not in seen:
                out.append(key)
                seen.add(key)
            continue

        # Fallback for normalized Korean-like forms, e.g. "점 H는 IG선 위".
        if "선" in line and "위" in line:
            letters = re.findall(r"[A-Za-z]", line)
            if len(letters) >= 3:
                p, a, b = letters[0], letters[1], letters[2]
                key = (p, a, b)
                if key not in seen:
                    out.append(key)
                    seen.add(key)
    return out


def apply_point_on_line_constraints(
    points: dict[str, tuple[float, float]],
    constraints: list[tuple[str, str, str]],
) -> dict[str, tuple[float, float]]:
    adjusted = dict(points)
    for _ in range(2):
        for p, a, b in constraints:
            if p not in adjusted or a not in adjusted or b not in adjusted:
                continue
            px, py = adjusted[p]
            ax, ay = adjusted[a]
            bx, by = adjusted[b]
            vx = bx - ax
            vy = by - ay
            denom = (vx * vx) + (vy * vy)
            if denom <= 1e-9:
                continue
            t = ((px - ax) * vx + (py - ay) * vy) / denom
            nx = ax + (t * vx)
            ny = ay + (t * vy)
            adjusted[p] = (nx, ny)
    return adjusted


def _edge_key(a: str, b: str) -> tuple[str, str]:
    return (a, b) if a <= b else (b, a)


def auto_snap_points_to_segments(
    points: dict[str, tuple[float, float]],
    edges: list[tuple[str, str]],
    *,
    dist_ratio_tol: float = 0.04,
) -> dict[str, tuple[float, float]]:
    """Heuristic fallback:
    if point P is connected to A,B and AB exists, and P is already near AB,
    snap P onto AB. This reduces micro-misalignment artifacts.
    """
    adjusted = dict(points)
    edge_set = {_edge_key(a, b) for a, b in edges}
    neighbors: dict[str, set[str]] = {}
    for a, b in edges:
        neighbors.setdefault(a, set()).add(b)
        neighbors.setdefault(b, set()).add(a)

    for p, nbrs in neighbors.items():
        if p not in adjusted or len(nbrs) < 2:
            continue
        nbr_list = sorted(nbrs)
        px, py = adjusted[p]
        for i in range(len(nbr_list)):
            for j in range(i + 1, len(nbr_list)):
                a = nbr_list[i]
                b = nbr_list[j]
                if a not in adjusted or b not in adjusted:
                    continue
                if _edge_key(a, b) not in edge_set:
                    continue
                ax, ay = adjusted[a]
                bx, by = adjusted[b]
                vx = bx - ax
                vy = by - ay
                denom = (vx * vx) + (vy * vy)
                if denom <= 1e-9:
                    continue
                t = ((px - ax) * vx + (py - ay) * vy) / denom
                if t < -0.05 or t > 1.05:
                    continue
                nx = ax + (t * vx)
                ny = ay + (t * vy)
                line_len = denom ** 0.5
                dist = ((px - nx) ** 2 + (py - ny) ** 2) ** 0.5
                if line_len <= 1e-9:
                    continue
                if (dist / line_len) <= dist_ratio_tol:
                    adjusted[p] = (nx, ny)
                    px, py = nx, ny
    return adjusted


def simplify_collinear_edges(
    *,
    mapped_points: dict[str, tuple[float, float]],
    edges: list[tuple[str, str]],
    angle_tol: float = 0.02,
    dist_tol: float = 8.0,
    gap_tol: float = 6.0,
) -> list[tuple[tuple[float, float], tuple[float, float]]]:
    """Merge overlapping/adjacent edges on the same supporting line.

    Returns simplified drawable segments in mapped coordinates.
    """
    if not edges:
        return []

    groups: list[dict[str, Any]] = []
    for a, b in edges:
        if a not in mapped_points or b not in mapped_points:
            continue
        ax, ay = mapped_points[a]
        bx, by = mapped_points[b]
        ux, uy = _unit_vector(ax, ay, bx, by)
        if ux == 0.0 and uy == 0.0:
            continue
        if ux < 0 or (abs(ux) < 1e-9 and uy < 0):
            ux, uy = -ux, -uy
        nx, ny = -uy, ux
        dist = (nx * ax) + (ny * ay)

        matched: dict[str, Any] | None = None
        for g in groups:
            gux, guy = g["dir"]
            gdist = g["dist"]
            cross = abs((ux * guy) - (uy * gux))
            if cross <= angle_tol and abs(dist - gdist) <= dist_tol:
                matched = g
                break

        if matched is None:
            matched = {"dir": (ux, uy), "dist": dist, "segments": []}
            groups.append(matched)
        matched["segments"].append(((ax, ay), (bx, by)))

    simplified: list[tuple[tuple[float, float], tuple[float, float]]] = []
    for g in groups:
        ux, uy = g["dir"]
        segments = g["segments"]
        if not segments:
            continue
        ox, oy = segments[0][0]

        intervals: list[tuple[float, float]] = []
        for (p1, p2) in segments:
            t1 = ((p1[0] - ox) * ux) + ((p1[1] - oy) * uy)
            t2 = ((p2[0] - ox) * ux) + ((p2[1] - oy) * uy)
            lo, hi = (t1, t2) if t1 <= t2 else (t2, t1)
            intervals.append((lo, hi))
        intervals.sort(key=lambda x: x[0])
        if not intervals:
            continue

        merged: list[tuple[float, float]] = []
        cur_lo, cur_hi = intervals[0]
        for lo, hi in intervals[1:]:
            if lo <= (cur_hi + gap_tol):
                cur_hi = max(cur_hi, hi)
            else:
                merged.append((cur_lo, cur_hi))
                cur_lo, cur_hi = lo, hi
        merged.append((cur_lo, cur_hi))

        for lo, hi in merged:
            sx = ox + (ux * lo)
            sy = oy + (uy * lo)
            ex = ox + (ux * hi)
            ey = oy + (uy * hi)
            simplified.append(((sx, sy), (ex, ey)))

    return simplified


def parse_length_constraints(diagram_logic_form: list[Any]) -> list[tuple[str, str, str]]:
    out: list[tuple[str, str, str]] = []
    pattern = re.compile(r"Equals\(LengthOf\(Line\(([A-Za-z]),\s*([A-Za-z])\)\),\s*([^\)]+)\)")
    inline_pattern = re.compile(r"^\s*([A-Za-z])\s*([A-Za-z]).*?=\s*([^=]+?)\s*$")
    for raw in diagram_logic_form:
        line = _to_str(raw)
        m = pattern.search(line)
        if m:
            out.append((m.group(1), m.group(2), m.group(3).strip()))
            continue

        lowered = line.lower()
        if "angle" in lowered or "∠" in line or "각" in line or "arc" in lowered:
            continue
        m2 = inline_pattern.search(line)
        if not m2:
            continue
        a = m2.group(1)
        b = m2.group(2)
        value = m2.group(3).strip().rstrip(",").rstrip(")")
        if not value:
            continue
        out.append((a, b, value))
    return out


def parse_equal_segment_constraints(diagram_logic_form: list[Any]) -> list[tuple[str, str, str, str]]:
    out: list[tuple[str, str, str, str]] = []
    canonical = re.compile(
        r"Equals\(LengthOf\(Line\(([A-Za-z]),\s*([A-Za-z])\)\),\s*LengthOf\(Line\(([A-Za-z]),\s*([A-Za-z])\)\)\)"
    )
    inline = re.compile(r"([A-Za-z])\s*([A-Za-z]).*?=\s*([A-Za-z])\s*([A-Za-z])")
    for raw in diagram_logic_form:
        line = _to_str(raw)
        m = canonical.search(line)
        if m:
            out.append((m.group(1), m.group(2), m.group(3), m.group(4)))
            continue
        m2 = inline.search(line)
        if not m2:
            continue
        left = (m2.group(1), m2.group(2))
        right = (m2.group(3), m2.group(4))
        if set(left) == set(right):
            continue
        out.append((left[0], left[1], right[0], right[1]))
    return out


def parse_perpendicular_constraints(diagram_logic_form: list[Any]) -> list[tuple[str, str, str]]:
    out: list[tuple[str, str, str]] = []
    pattern = re.compile(
        r"Perpendicular\(Line\(([A-Za-z]),\s*([A-Za-z])\),\s*Line\(([A-Za-z]),\s*([A-Za-z])\)\)"
    )
    for raw in diagram_logic_form:
        line = _to_str(raw)
        m = pattern.search(line)
        if m:
            a, b, c, d = m.group(1), m.group(2), m.group(3), m.group(4)
            shared = set((a, b)).intersection((c, d))
            if not shared:
                continue
            pivot = next(iter(shared))
            other1 = b if a == pivot else a
            other2 = d if c == pivot else c
            out.append((pivot, other1, other2))
            continue

        if "⊥" not in line and "perpendicular" not in line.lower() and "수직" not in line:
            continue
        segs = re.findall(r"([A-Za-z]{2})", line)
        if len(segs) < 2:
            continue
        s1 = segs[0]
        s2 = segs[1]
        shared = set(s1).intersection(set(s2))
        if not shared:
            continue
        pivot = next(iter(shared))
        o1 = s1[1] if s1[0] == pivot else s1[0]
        o2 = s2[1] if s2[0] == pivot else s2[0]
        out.append((pivot, o1, o2))
    return out


def parse_parallel_constraints(diagram_logic_form: list[Any]) -> list[tuple[str, str, str, str]]:
    out: list[tuple[str, str, str, str]] = []
    pattern = re.compile(r"Parallel\(Line\(([A-Za-z]),\s*([A-Za-z])\),\s*Line\(([A-Za-z]),\s*([A-Za-z])\)\)")
    for raw in diagram_logic_form:
        line = _to_str(raw)
        m = pattern.search(line)
        if m:
            out.append((m.group(1), m.group(2), m.group(3), m.group(4)))
            continue

        lowered = line.lower()
        if "∥" not in line and "||" not in line and "parallel" not in lowered and "평행" not in line:
            continue
        segs = re.findall(r"([A-Za-z]{2})", line)
        if len(segs) < 2:
            continue
        a, b = segs[0][0], segs[0][1]
        c, d = segs[1][0], segs[1][1]
        out.append((a, b, c, d))
    return out


def parse_circle_constraints(logic: dict[str, Any], diagram_logic_form: list[Any]) -> list[tuple[str, list[str]]]:
    by_center: dict[str, set[str]] = {}
    pattern = re.compile(r"PointLiesOnCircle\(([A-Za-z]),\s*Circle\(([A-Za-z]),\s*([^)]+)\)\)")
    for raw in diagram_logic_form:
        line = _to_str(raw)
        m = pattern.search(line)
        if not m:
            continue
        point = m.group(1)
        center = m.group(2)
        if center not in by_center:
            by_center[center] = set()
        by_center[center].add(point)

    circle_instances_raw = logic.get("circle_instances")
    circle_instances = circle_instances_raw if isinstance(circle_instances_raw, list) else []
    for item in circle_instances:
        center = _to_str(item).strip()
        if center:
            by_center.setdefault(center, set())

    out: list[tuple[str, list[str]]] = []
    for center, pts in by_center.items():
        out.append((center, sorted(pts)))
    return out


def parse_angle_constraints(diagram_logic_form: list[Any]) -> list[tuple[str, str, str, str]]:
    out: list[tuple[str, str, str, str]] = []
    angle_ref_pattern = re.compile(r"MeasureOf\(angle\s+([^)]+)\)", re.IGNORECASE)

    def _clean_angle_value(value: str) -> str:
        cleaned = re.sub(r"\bangle\b", "", value, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s+", " ", cleaned).strip()
        return cleaned

    for raw in diagram_logic_form:
        line = _to_str(raw).strip()
        inside_m = re.search(r"Angle\(([^)]*)\)", line)
        if not inside_m:
            lowered = line.lower()
            if ("?" in line or "?" in line or "angle" in lowered) and "=" in line:
                seq = re.search(r"([A-Za-z])\s*([A-Za-z])\s*([A-Za-z])", line)
                if not seq:
                    continue
                a, v, c = seq.group(1), seq.group(2), seq.group(3)
                value = line.split("=", 1)[1].strip()
                value = angle_ref_pattern.sub(lambda m: f"angle {m.group(1).strip()}", value)
                value = _clean_angle_value(value)
                out.append((a, v, c, value))
            continue

        letters = re.findall(r"[A-Za-z]", inside_m.group(1))
        if len(letters) < 3:
            continue
        a, v, c = letters[0], letters[1], letters[2]

        value = ""
        m_legacy = re.search(r"Equals\(MeasureOf\(Angle\([^)]+\)\),\s*(.+)\)$", line)
        if m_legacy:
            value = m_legacy.group(1).strip()
        else:
            m_inline = re.search(r"MeasureOf\(Angle\([^)]+\)\s*,\s*(.+)\)$", line)
            if m_inline:
                value = m_inline.group(1).strip()
        value = angle_ref_pattern.sub(lambda m: f"angle {m.group(1).strip()}", value)
        value = _clean_angle_value(value)
        out.append((a, v, c, value))
    return out


def _unit_vector(ax: float, ay: float, bx: float, by: float) -> tuple[float, float]:
    vx = bx - ax
    vy = by - ay
    norm = (vx * vx + vy * vy) ** 0.5
    if norm <= 1e-9:
        return 0.0, 0.0
    return vx / norm, vy / norm


def _estimate_scale_from_mapping(
    *,
    source_points: dict[str, tuple[float, float]],
    mapped_points: dict[str, tuple[float, float]],
) -> float:
    shared = [k for k in source_points.keys() if k in mapped_points]
    if len(shared) < 2:
        return 1.0
    ratios: list[float] = []
    for i in range(len(shared)):
        for j in range(i + 1, len(shared)):
            a = shared[i]
            b = shared[j]
            sx1, sy1 = source_points[a]
            sx2, sy2 = source_points[b]
            mx1, my1 = mapped_points[a]
            mx2, my2 = mapped_points[b]
            sdist = ((sx2 - sx1) ** 2 + (sy2 - sy1) ** 2) ** 0.5
            mdist = ((mx2 - mx1) ** 2 + (my2 - my1) ** 2) ** 0.5
            if sdist <= 1e-6 or mdist <= 1e-6:
                continue
            ratios.append(mdist / sdist)
            if len(ratios) >= 12:
                break
        if len(ratios) >= 12:
            break
    if not ratios:
        return 1.0
    ratios.sort()
    return ratios[len(ratios) // 2]


def build_perpendicular_marker_elements(
    *,
    mapped_points: dict[str, tuple[float, float]],
    constraints: list[tuple[str, str, str]],
) -> list[ir.Element]:
    out: list[ir.Element] = []
    size = 18.0
    for idx, (pivot, p1, p2) in enumerate(constraints, start=1):
        if pivot not in mapped_points or p1 not in mapped_points or p2 not in mapped_points:
            continue
        px, py = mapped_points[pivot]
        x1, y1 = mapped_points[p1]
        x2, y2 = mapped_points[p2]
        u1x, u1y = _unit_vector(px, py, x1, y1)
        u2x, u2y = _unit_vector(px, py, x2, y2)
        if (u1x == 0.0 and u1y == 0.0) or (u2x == 0.0 and u2y == 0.0):
            continue
        a_x = px + (u1x * size)
        a_y = py + (u1y * size)
        b_x = a_x + (u2x * size)
        b_y = a_y + (u2y * size)
        c_x = px + (u2x * size)
        c_y = py + (u2y * size)
        out.append(
            ir.Line(
                id=f"geom_perp_{idx}_1",
                x1=a_x,
                y1=a_y,
                x2=b_x,
                y2=b_y,
                stroke="#D97706",
                stroke_width=2.0,
                semantic_role="geometry_right_angle",
            )
        )
        out.append(
            ir.Line(
                id=f"geom_perp_{idx}_2",
                x1=b_x,
                y1=b_y,
                x2=c_x,
                y2=c_y,
                stroke="#D97706",
                stroke_width=2.0,
                semantic_role="geometry_right_angle",
            )
        )
    return out


def build_parallel_marker_elements(
    *,
    mapped_points: dict[str, tuple[float, float]],
    constraints: list[tuple[str, str, str, str]],
) -> list[ir.Element]:
    out: list[ir.Element] = []
    marker_len = 12.0
    wing = 6.5

    def _add_on_segment(prefix: str, ax: float, ay: float, bx: float, by: float) -> None:
        ux, uy = _unit_vector(ax, ay, bx, by)
        if ux == 0.0 and uy == 0.0:
            return
        mx = (ax + bx) / 2.0
        my = (ay + by) / 2.0
        tx = mx + (ux * marker_len * 0.5)
        ty = my + (uy * marker_len * 0.5)
        bx0 = mx - (ux * marker_len * 0.5)
        by0 = my - (uy * marker_len * 0.5)
        nx, ny = -uy, ux
        out.append(
            ir.Line(
                id=f"{prefix}_base",
                x1=bx0,
                y1=by0,
                x2=tx,
                y2=ty,
                stroke="#2563EB",
                stroke_width=1.8,
                semantic_role="geometry_parallel_marker",
            )
        )
        out.append(
            ir.Line(
                id=f"{prefix}_w1",
                x1=tx,
                y1=ty,
                x2=tx - (ux * wing) + (nx * wing * 0.65),
                y2=ty - (uy * wing) + (ny * wing * 0.65),
                stroke="#2563EB",
                stroke_width=1.8,
                semantic_role="geometry_parallel_marker",
            )
        )
        out.append(
            ir.Line(
                id=f"{prefix}_w2",
                x1=tx,
                y1=ty,
                x2=tx - (ux * wing) - (nx * wing * 0.65),
                y2=ty - (uy * wing) - (ny * wing * 0.65),
                stroke="#2563EB",
                stroke_width=1.8,
                semantic_role="geometry_parallel_marker",
            )
        )

    for idx, (a, b, c, d) in enumerate(constraints, start=1):
        if a in mapped_points and b in mapped_points:
            ax, ay = mapped_points[a]
            bx, by = mapped_points[b]
            _add_on_segment(f"geom_parallel_{idx}_ab", ax, ay, bx, by)
        if c in mapped_points and d in mapped_points:
            cx, cy = mapped_points[c]
            dx, dy = mapped_points[d]
            _add_on_segment(f"geom_parallel_{idx}_cd", cx, cy, dx, dy)
    return out


def build_equal_length_tick_elements(
    *,
    mapped_points: dict[str, tuple[float, float]],
    constraints: list[tuple[str, str, str, str]],
) -> list[ir.Element]:
    out: list[ir.Element] = []
    tick_len = 10.0

    def _add_tick(prefix: str, ax: float, ay: float, bx: float, by: float) -> None:
        ux, uy = _unit_vector(ax, ay, bx, by)
        if ux == 0.0 and uy == 0.0:
            return
        mx = (ax + bx) / 2.0
        my = (ay + by) / 2.0
        nx, ny = -uy, ux
        half = tick_len * 0.5
        out.append(
            ir.Line(
                id=f"{prefix}_tick",
                x1=mx - (nx * half),
                y1=my - (ny * half),
                x2=mx + (nx * half),
                y2=my + (ny * half),
                stroke="#E91E63",
                stroke_width=2.2,
                semantic_role="geometry_equal_length_tick",
            )
        )

    for idx, (a, b, c, d) in enumerate(constraints, start=1):
        if a in mapped_points and b in mapped_points:
            ax, ay = mapped_points[a]
            bx, by = mapped_points[b]
            _add_tick(f"geom_equal_{idx}_ab", ax, ay, bx, by)
        if c in mapped_points and d in mapped_points:
            cx, cy = mapped_points[c]
            dx, dy = mapped_points[d]
            _add_tick(f"geom_equal_{idx}_cd", cx, cy, dx, dy)
    return out


def build_length_dimension_elements(
    *,
    mapped_points: dict[str, tuple[float, float]],
    constraints: list[tuple[str, str, str]],
) -> list[ir.Element]:
    out: list[ir.Element] = []
    cap_half = 8.0
    arrow_len = 8.0
    arrow_spread = 6.0

    def _arrow_head(prefix: str, tip: tuple[float, float], direction: tuple[float, float]) -> None:
        ux, uy = direction
        if ux == 0.0 and uy == 0.0:
            return
        nx, ny = -uy, ux
        tx, ty = tip
        bx = tx - (ux * arrow_len)
        by = ty - (uy * arrow_len)
        out.append(
            ir.Line(
                id=f"{prefix}_a",
                x1=tx,
                y1=ty,
                x2=bx + (nx * arrow_spread * 0.5),
                y2=by + (ny * arrow_spread * 0.5),
                stroke="#111111",
                stroke_width=1.8,
                semantic_role="geometry_dimension_arrow",
            )
        )
        out.append(
            ir.Line(
                id=f"{prefix}_b",
                x1=tx,
                y1=ty,
                x2=bx - (nx * arrow_spread * 0.5),
                y2=by - (ny * arrow_spread * 0.5),
                stroke="#111111",
                stroke_width=1.8,
                semantic_role="geometry_dimension_arrow",
            )
        )

    for idx, (a, b, _value) in enumerate(constraints, start=1):
        if a not in mapped_points or b not in mapped_points:
            continue
        ax, ay = mapped_points[a]
        bx, by = mapped_points[b]
        ux, uy = _unit_vector(ax, ay, bx, by)
        if ux == 0.0 and uy == 0.0:
            continue
        nx, ny = -uy, ux

        out.append(
            ir.Line(
                id=f"geom_dim_{idx}_cap_a",
                x1=ax - (nx * cap_half),
                y1=ay - (ny * cap_half),
                x2=ax + (nx * cap_half),
                y2=ay + (ny * cap_half),
                stroke="#111111",
                stroke_width=1.5,
                semantic_role="geometry_dimension_cap",
            )
        )
        out.append(
            ir.Line(
                id=f"geom_dim_{idx}_cap_b",
                x1=bx - (nx * cap_half),
                y1=by - (ny * cap_half),
                x2=bx + (nx * cap_half),
                y2=by + (ny * cap_half),
                stroke="#111111",
                stroke_width=1.5,
                semantic_role="geometry_dimension_cap",
            )
        )

        a_tip = (ax + (ux * 5.0), ay + (uy * 5.0))
        b_tip = (bx - (ux * 5.0), by - (uy * 5.0))
        _arrow_head(f"geom_dim_{idx}_arr_a", a_tip, (ux, uy))
        _arrow_head(f"geom_dim_{idx}_arr_b", b_tip, (-ux, -uy))
    return out


def build_circle_elements(
    *,
    source_points: dict[str, tuple[float, float]],
    mapped_points: dict[str, tuple[float, float]],
    circle_constraints: list[tuple[str, list[str]]],
    default_radius: float,
) -> list[ir.Element]:
    out: list[ir.Element] = []
    scale = _estimate_scale_from_mapping(source_points=source_points, mapped_points=mapped_points)
    for idx, (center, on_points) in enumerate(circle_constraints, start=1):
        if center not in mapped_points:
            continue
        cx, cy = mapped_points[center]
        radii: list[float] = []
        if center in source_points:
            sx, sy = source_points[center]
            for p in on_points:
                if p not in source_points:
                    continue
                px, py = source_points[p]
                r = ((px - sx) ** 2 + (py - sy) ** 2) ** 0.5
                if r > 1e-6:
                    radii.append(r)
        if radii:
            radii.sort()
            r_mapped = radii[len(radii) // 2] * scale
        else:
            r_mapped = default_radius
        r_mapped = max(16.0, float(r_mapped))
        out.append(
            ir.Circle(
                id=f"geom_circle_{idx}_{center}",
                x=cx,
                y=cy,
                r=r_mapped,
                fill="none",
                stroke="#2563EB",
                stroke_width=2.0,
                semantic_role="geometry_circle",
            )
        )
    return out


def build_angle_marker_elements(
    *,
    mapped_points: dict[str, tuple[float, float]],
    constraints: list[tuple[str, str, str, str]],
    font_size: int,
) -> list[ir.Element]:
    out: list[ir.Element] = []
    ring_by_vertex: dict[str, int] = {}
    for idx, (a, v, c, value) in enumerate(constraints, start=1):
        if a not in mapped_points or v not in mapped_points or c not in mapped_points:
            continue
        vx, vy = mapped_points[v]
        ax, ay = mapped_points[a]
        cx, cy = mapped_points[c]
        u1x, u1y = _unit_vector(vx, vy, ax, ay)
        u2x, u2y = _unit_vector(vx, vy, cx, cy)
        if (u1x == 0.0 and u1y == 0.0) or (u2x == 0.0 and u2y == 0.0):
            continue
        t1 = math.atan2(u1y, u1x)
        t2 = math.atan2(u2y, u2x)
        delta = t2 - t1
        while delta <= -math.pi:
            delta += math.tau
        while delta > math.pi:
            delta -= math.tau

        ring = ring_by_vertex.get(v, 0) + 1
        ring_by_vertex[v] = ring
        rx = 18.0 + ((ring - 1) * 8.0)
        ry = 12.0 + ((ring - 1) * 6.0)
        seg = 14
        points: list[tuple[float, float]] = []
        for j in range(seg + 1):
            t = t1 + (delta * (j / seg))
            points.append((vx + (rx * math.cos(t)), vy + (ry * math.sin(t))))
        for j in range(seg):
            p0 = points[j]
            p1 = points[j + 1]
            out.append(
                ir.Line(
                    id=f"geom_angle_{idx}_{j + 1:02d}",
                    x1=p0[0],
                    y1=p0[1],
                    x2=p1[0],
                    y2=p1[1],
                    stroke="#7C3AED",
                    stroke_width=2.0,
                    semantic_role="geometry_angle_marker",
                )
            )
        label = _to_str(value).strip()
        if label:
            tm = t1 + (delta * 0.5)
            out.append(
                ir.Text(
                    id=f"geom_angle_label_{idx}",
                    x=vx + ((rx + 12.0) * math.cos(tm)),
                    y=vy + ((ry + 10.0) * math.sin(tm)),
                    text=label,
                    font_size=font_size,
                    fill="#111111",
                    semantic_role="geometry_angle_label",
                )
            )
    return out


def build_geometry_reconstruction_elements(
    *,
    domain: dict[str, Any],
    canvas_w: float,
    canvas_h: float,
    font_scale: float,
) -> list[ir.Element]:
    logic = extract_logic_form(domain)
    points = parse_point_positions(logic)
    if len(points) < 2:
        return []
    diagram_logic_raw = logic.get("diagram_logic_form")
    diagram_logic = diagram_logic_raw if isinstance(diagram_logic_raw, list) else []
    point_on_line_constraints = parse_point_on_line_constraints(diagram_logic)
    points = apply_point_on_line_constraints(points, point_on_line_constraints)
    edges = parse_line_instances(logic)
    points = auto_snap_points_to_segments(points, edges)

    region_x, region_y, region_w, region_h = geometry_region(canvas_w, canvas_h)
    mapped = fit_transform_for_points(
        points,
        target_x=region_x,
        target_y=region_y,
        target_w=region_w,
        target_h=region_h,
    )
    mapped = level_triangle_base_if_needed(source_points=points, mapped_points=mapped)
    length_constraints = parse_length_constraints(diagram_logic)
    equal_constraints = parse_equal_segment_constraints(diagram_logic)
    perp_constraints = parse_perpendicular_constraints(diagram_logic)
    parallel_constraints = parse_parallel_constraints(diagram_logic)
    circle_constraints = parse_circle_constraints(logic, diagram_logic)
    angle_constraints = parse_angle_constraints(diagram_logic)

    label_font = max(12, int(round(12 * font_scale)))
    out: list[ir.Element] = []
    out.append(
        ir.Rect(
            id="geom_diagram_region",
            x=region_x,
            y=region_y,
            width=region_w,
            height=region_h,
            fill="none",
            stroke="#D1D5DB",
            stroke_width=1.0,
            semantic_role="geometry_diagram_region",
        )
    )

    merged_edges = simplify_collinear_edges(mapped_points=mapped, edges=edges)
    # 꼭지점이 정확히 3개이면 삼각형으로 판단하여 단일 Polygon으로 표현
    if len(mapped) == 3:
        vertices = list(mapped.values())
        out.append(
            ir.Polygon(
                id="geom_triangle",
                points=vertices,
                fill="none",
                stroke="#374151",
                stroke_width=2.2,
                semantic_role="geometry_edge",
            )
        )
    else:
        for idx, (start_pt, end_pt) in enumerate(merged_edges, start=1):
            ax, ay = start_pt
            bx, by = end_pt
            out.append(
                ir.Line(
                    id=f"geom_line_{idx}",
                    x1=ax,
                    y1=ay,
                    x2=bx,
                    y2=by,
                    stroke="#374151",
                    stroke_width=2.2,
                    semantic_role="geometry_edge",
                )
            )

    out.extend(
        build_circle_elements(
            source_points=points,
            mapped_points=mapped,
            circle_constraints=circle_constraints,
            default_radius=min(region_w, region_h) * 0.22,
        )
    )

    for name, (x, y) in mapped.items():
        out.append(
            ir.Circle(
                id=f"geom_point_{name}",
                x=x,
                y=y,
                r=3.8,
                fill="#111111",
                stroke="#111111",
                stroke_width=1.0,
                semantic_role="geometry_point",
            )
        )
        out.append(
            ir.Text(
                id=f"geom_label_{name}",
                x=x + 6.0,
                y=y - 6.0,
                text=name,
                font_size=label_font,
                fill="#111111",
                semantic_role="geometry_point_label",
            )
        )

    for idx, (a, b, value) in enumerate(length_constraints, start=1):
        if a not in mapped or b not in mapped:
            continue
        ax, ay = mapped[a]
        bx, by = mapped[b]
        mx = (ax + bx) / 2.0
        my = (ay + by) / 2.0
        out.append(
            ir.Text(
                id=f"geom_len_{idx}_{a}{b}",
                x=mx + 4.0,
                y=my - 4.0,
                text=value,
                font_size=label_font,
                fill="#1F2937",
                semantic_role="geometry_length_label",
            )
        )

    # out.extend(build_length_dimension_elements(mapped_points=mapped, constraints=length_constraints))
    out.extend(build_equal_length_tick_elements(mapped_points=mapped, constraints=equal_constraints))
    out.extend(build_perpendicular_marker_elements(mapped_points=mapped, constraints=perp_constraints))
    out.extend(build_parallel_marker_elements(mapped_points=mapped, constraints=parallel_constraints))
    out.extend(build_angle_marker_elements(mapped_points=mapped, constraints=angle_constraints, font_size=label_font))
    return out


def infer_geometry_shape(
    *,
    problem_type: str,
    domain: dict[str, Any],
    title: str | None,
) -> str:
    text_parts = [problem_type, _to_str(title)]
    for key in ("question_text", "question_expression"):
        text_parts.append(_to_str(domain.get(key)))
    lowered = " ".join(text_parts).lower()
    if "triangle" in lowered:
        return "triangle"
    if "circle" in lowered:
        return "circle"
    if "trapezoid" in lowered:
        return "trapezoid"
    if "parallelogram" in lowered:
        return "parallelogram"
    if "rectangle" in lowered:
        return "rectangle"
    if "line" in lowered:
        return "line"
    return "triangle"


def extract_numeric_tokens(text: str, limit: int = 8) -> list[str]:
    out: list[str] = []
    for m in re.finditer(r"-?\d+(?:\.\d+)?", text):
        out.append(m.group(0))
        if len(out) >= limit:
            break
    return out


def build_geometry_template_elements(
    *,
    problem_type: str,
    domain: dict[str, Any],
    title: str | None,
    canvas_w: float,
    canvas_h: float,
    font_scale: float,
) -> list[ir.Element]:
    region_x, region_y, region_w, region_h = geometry_region(canvas_w, canvas_h)
    label_font = max(11, int(round(11 * font_scale)))
    question_text = _to_str(domain.get("question_text"))
    numeric_tokens = extract_numeric_tokens(question_text or _to_str(title), limit=6)
    shape = infer_geometry_shape(problem_type=problem_type, domain=domain, title=title)

    out: list[ir.Element] = [
        ir.Rect(
            id="geom_template_region",
            x=region_x,
            y=region_y,
            width=region_w,
            height=region_h,
            fill="none",
            stroke="#D1D5DB",
            stroke_width=1.0,
            semantic_role="geometry_template_region",
        )
    ]

    if shape == "triangle":
        p1 = (region_x + (region_w * 0.16), region_y + (region_h * 0.86))
        p2 = (region_x + (region_w * 0.50), region_y + (region_h * 0.16))
        p3 = (region_x + (region_w * 0.84), region_y + (region_h * 0.86))
        out.append(
            ir.Polygon(
                id="geom_template_shape",
                points=[p1, p2, p3],
                fill="none",
                stroke="#374151",
                stroke_width=2.2,
                semantic_role="geometry_shape",
            )
        )
        labels = ["A", "B", "C"]
        for idx, (x, y) in enumerate((p1, p2, p3)):
            out.append(
                ir.Text(
                    id=f"geom_template_pt_{labels[idx]}",
                    x=x + 6.0,
                    y=y - 8.0,
                    text=labels[idx],
                    font_size=label_font,
                    fill="#111111",
                    semantic_role="geometry_point_label",
                )
            )
    elif shape == "circle":
        cx = region_x + (region_w * 0.5)
        cy = region_y + (region_h * 0.52)
        r = min(region_w, region_h) * 0.32
        out.append(
            ir.Circle(
                id="geom_template_shape",
                x=cx,
                y=cy,
                r=r,
                fill="none",
                stroke="#374151",
                stroke_width=2.2,
                semantic_role="geometry_shape",
            )
        )
        out.append(
            ir.Line(
                id="geom_template_radius",
                x1=cx,
                y1=cy,
                x2=cx + (r * 0.86),
                y2=cy,
                stroke="#6B7280",
                stroke_width=1.8,
                semantic_role="geometry_radius",
            )
        )
    elif shape == "rectangle":
        out.append(
            ir.Rect(
                id="geom_template_shape",
                x=region_x + (region_w * 0.18),
                y=region_y + (region_h * 0.26),
                width=region_w * 0.64,
                height=region_h * 0.48,
                fill="none",
                stroke="#374151",
                stroke_width=2.2,
                semantic_role="geometry_shape",
            )
        )
    elif shape == "parallelogram":
        x0 = region_x + (region_w * 0.16)
        y0 = region_y + (region_h * 0.30)
        w = region_w * 0.66
        h = region_h * 0.42
        skew = region_w * 0.14
        out.append(
            ir.Polygon(
                id="geom_template_shape",
                points=[(x0 + skew, y0), (x0 + w + skew, y0), (x0 + w, y0 + h), (x0, y0 + h)],
                fill="none",
                stroke="#374151",
                stroke_width=2.2,
                semantic_role="geometry_shape",
            )
        )
    elif shape == "trapezoid":
        x0 = region_x + (region_w * 0.14)
        y0 = region_y + (region_h * 0.28)
        top_w = region_w * 0.42
        bot_w = region_w * 0.72
        h = region_h * 0.46
        out.append(
            ir.Polygon(
                id="geom_template_shape",
                points=[
                    (x0 + ((bot_w - top_w) / 2.0), y0),
                    (x0 + ((bot_w + top_w) / 2.0), y0),
                    (x0 + bot_w, y0 + h),
                    (x0, y0 + h),
                ],
                fill="none",
                stroke="#374151",
                stroke_width=2.2,
                semantic_role="geometry_shape",
            )
        )
    else:
        y = region_y + (region_h * 0.55)
        out.append(
            ir.Line(
                id="geom_template_shape",
                x1=region_x + (region_w * 0.12),
                y1=y,
                x2=region_x + (region_w * 0.88),
                y2=y,
                stroke="#374151",
                stroke_width=2.2,
                semantic_role="geometry_shape",
            )
        )

    for idx, token in enumerate(numeric_tokens[:3], start=1):
        out.append(
            ir.Text(
                id=f"geom_template_hint_{idx}",
                x=region_x + region_w + 24.0,
                y=region_y + 36.0 + (idx * (label_font * 1.6)),
                text=token,
                font_size=label_font,
                fill="#1F2937",
                semantic_role="geometry_hint",
            )
        )
    return out
