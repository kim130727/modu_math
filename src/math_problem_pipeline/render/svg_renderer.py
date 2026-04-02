"""SVG renderer entrypoints for intermediate semantic checks."""

from __future__ import annotations

import math
from pathlib import Path
import unicodedata

from math_problem_pipeline.models.semantic_models import (
    ArithmeticExpressionProblem,
    ClockReadingProblem,
    FractionShadedAreaProblem,
    GeometryBasicProblem,
    UnknownVisualMathProblem,
    MultipleChoiceTextProblem,
    SemanticProblem,
    TableOrChartBasicProblem,
)
from math_problem_pipeline.utils.io import ensure_dir


SVG_WIDTH = 1280
SVG_HEIGHT = 720


def render_problem_to_svg(problem: SemanticProblem, output_svg: Path) -> dict:
    """Render a semantic problem into a standalone .svg document."""
    ensure_dir(output_svg.parent)

    fallback_reason = _fallback_reason(problem)
    svg = build_svg_document(problem, fallback_reason=fallback_reason)
    output_svg.write_text(svg, encoding="utf-8")

    if fallback_reason:
        problem.warnings.append(fallback_reason)

    return {
        "problem_id": problem.problem_id,
        "rendered": True,
        "output_svg": str(output_svg),
        "used_fields": ["question_text", "type", "render_hint"],
        "fallback_render_used": bool(fallback_reason),
        "fallback_reason": fallback_reason,
    }


def build_svg_document(problem: SemanticProblem, fallback_reason: str | None = None) -> str:
    question_lines = _wrap_text_lines(problem.question_text, font_size=30, max_width=SVG_WIDTH - 72)
    question_text_svg, question_last_y = _render_multiline_text(
        question_lines,
        x=36,
        y=64,
        font_size=30,
        font_family="Noto Sans KR, Arial, sans-serif",
        line_height=38,
    )
    body_start_y = question_last_y + 56
    body_shift = max(0.0, body_start_y - 140.0)

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{SVG_WIDTH}" height="{SVG_HEIGHT}" viewBox="0 0 {SVG_WIDTH} {SVG_HEIGHT}">',
        '<rect x="0" y="0" width="100%" height="100%" fill="white"/>',
        question_text_svg,
    ]

    if fallback_reason:
        parts.append(
            f'<text x="36" y="110" fill="#777" font-size="20" font-family="Arial, sans-serif">[fallback render] {_escape_xml(fallback_reason)}</text>'
        )
    else:
        body = _problem_body(problem)
        if body_shift > 0:
            parts.append(f'<g transform="translate(0,{body_shift:.2f})">')
            parts.extend(body)
            parts.append('</g>')
        else:
            parts.extend(body)

    parts.append("</svg>")
    return "\n".join(parts)


def _problem_body(problem: SemanticProblem) -> list[str]:
    if isinstance(problem, UnknownVisualMathProblem):
        return _unknown_visual_block(problem)
    if isinstance(problem, MultipleChoiceTextProblem):
        return _multiple_choice_block(problem)
    if isinstance(problem, ArithmeticExpressionProblem):
        return _arithmetic_block(problem)
    if isinstance(problem, FractionShadedAreaProblem):
        return _fraction_block(problem)
    if isinstance(problem, ClockReadingProblem):
        return _clock_block(problem)
    if isinstance(problem, GeometryBasicProblem):
        return _geometry_block(problem)
    if isinstance(problem, TableOrChartBasicProblem):
        return _table_or_chart_block(problem)
    return []


def _unknown_visual_block(problem: UnknownVisualMathProblem) -> list[str]:
    src = problem.coordinates.source_coordinates if problem.coordinates else {}
    sem = problem.coordinates.semantic_coordinates if problem.coordinates else {}
    render = problem.coordinates.render_coordinates if problem.coordinates else {}
    href = str(src.get("image_data_uri") or src.get("image_path") or "").replace("\\", "/")

    x = 56.0
    y = 180.0
    max_w = SVG_WIDTH - 112.0
    max_h = SVG_HEIGHT - 220.0

    w = src.get("image_width")
    h = src.get("image_height")
    if isinstance(w, int) and isinstance(h, int) and w > 0 and h > 0:
        scale = min(max_w / float(w), max_h / float(h))
        draw_w = max(1.0, float(w) * scale)
        draw_h = max(1.0, float(h) * scale)
    else:
        draw_w = max_w
        draw_h = max_h

    out = [
        f'<rect x="{x:.2f}" y="{y:.2f}" width="{draw_w:.2f}" height="{draw_h:.2f}" fill="white" stroke="#222" stroke-width="1"/>',
    ]

    if href:
        out.append(
            f'<image href="{_escape_xml(href)}" x="{x:.2f}" y="{y:.2f}" width="{draw_w:.2f}" height="{draw_h:.2f}" preserveAspectRatio="xMidYMid meet"/>'
        )
    else:
        out.append(
            f'<text x="{x + 12:.2f}" y="{y + 36:.2f}" font-size="20" font-family="Arial, sans-serif" fill="#777">image_path missing in semantic source_coordinates</text>'
        )

    show_overlay = bool(render.get("show_layout_overlay"))
    layout = sem.get("layout_analysis") if isinstance(sem, dict) else None
    regions = layout.get("regions", []) if isinstance(layout, dict) else []

    if show_overlay and isinstance(regions, list):
        color_map = {
            "text_block": "#1f77b4",
            "choice_like": "#2ca02c",
            "diagram_like": "#d62728",
            "table_like": "#9467bd",
            "other": "#ff7f0e",
        }

        src_w = float(w) if isinstance(w, int) and w > 0 else draw_w
        src_h = float(h) if isinstance(h, int) and h > 0 else draw_h
        sx = draw_w / max(1.0, src_w)
        sy = draw_h / max(1.0, src_h)

        for idx, r in enumerate(regions, start=1):
            bbox = r.get("bbox", {}) if isinstance(r, dict) else {}
            kind = str(r.get("kind") or "other") if isinstance(r, dict) else "other"
            conf = r.get("confidence", 0.0) if isinstance(r, dict) else 0.0
            try:
                rx = float(bbox.get("x", 0.0))
                ry = float(bbox.get("y", 0.0))
                rw = float(bbox.get("width", 0.0))
                rh = float(bbox.get("height", 0.0))
            except Exception:
                continue

            ox = x + rx * sx
            oy = y + ry * sy
            ow = max(1.0, rw * sx)
            oh = max(1.0, rh * sy)
            color = color_map.get(kind, "#ff7f0e")

            out.append(
                f'<rect x="{ox:.2f}" y="{oy:.2f}" width="{ow:.2f}" height="{oh:.2f}" fill="none" stroke="{color}" stroke-width="2" opacity="0.8"/>'
            )
            label = f"{idx}:{kind} ({float(conf):.2f})"
            out.append(
                f'<text x="{ox + 2:.2f}" y="{max(y + 14, oy - 4):.2f}" font-size="12" font-family="Arial, sans-serif" fill="{color}">{_escape_xml(label)}</text>'
            )

    return out

def _multiple_choice_block(problem: MultipleChoiceTextProblem) -> list[str]:
    if not problem.choices:
        return []
    lines: list[str] = []
    y = 140
    for idx, choice in enumerate(problem.choices, start=1):
        lines.append(
            f'<text x="56" y="{y}" font-size="26" font-family="Noto Sans KR, Arial, sans-serif">{idx}. {_escape_xml(choice)}</text>'
        )
        y += 48
    return lines


def _arithmetic_block(problem: ArithmeticExpressionProblem) -> list[str]:
    return [
        f'<text x="56" y="150" font-size="38" font-family="Times New Roman, serif">{_escape_xml(problem.expression)}</text>'
    ]


def _fraction_block(problem: FractionShadedAreaProblem) -> list[str]:
    frac = problem.fraction
    if frac.shape == "rectangle":
        return _fraction_rectangle_block(problem)
    return _fraction_circle_block(problem)


def _fraction_rectangle_block(problem: FractionShadedAreaProblem) -> list[str]:
    frac = problem.fraction
    cols = max(1, frac.cols or frac.total_parts)
    rows = max(1, frac.rows or 1)
    x0, y0 = 56.0, 180.0
    width, height = 360.0, 360.0 * rows / cols if cols else 180.0
    cell_w = width / cols
    cell_h = height / rows
    shaded = set(frac.shaded_indices) if frac.shaded_indices else set(range(frac.shaded_parts))

    lines = [
        f'<rect x="{x0:.2f}" y="{y0:.2f}" width="{width:.2f}" height="{height:.2f}" fill="none" stroke="#222" stroke-width="2"/>'
    ]
    for i in range(frac.total_parts):
        r = i // cols
        c = i % cols
        x = x0 + c * cell_w
        y = y0 + r * cell_h
        fill = '#7db7ff' if i in shaded else 'white'
        lines.append(
            f'<rect x="{x:.2f}" y="{y:.2f}" width="{cell_w:.2f}" height="{cell_h:.2f}" fill="{fill}" stroke="#555" stroke-width="1"/>'
        )
    return lines


def _fraction_circle_block(problem: FractionShadedAreaProblem) -> list[str]:
    frac = problem.fraction
    total = max(1, frac.total_parts)
    shaded = frac.shaded_parts
    cx, cy, r = 240.0, 300.0, 130.0
    lines = [f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" fill="none" stroke="#222" stroke-width="2"/>']
    for i in range(total):
        angle = math.radians(90 - (360 / total) * i)
        x = cx + r * math.cos(angle)
        y = cy - r * math.sin(angle)
        lines.append(f'<line x1="{cx:.2f}" y1="{cy:.2f}" x2="{x:.2f}" y2="{y:.2f}" stroke="#555" stroke-width="1"/>')
    if shaded > 0:
        lines.append(
            f'<text x="56" y="560" font-size="24" font-family="Arial, sans-serif" fill="#1f4b8f">shaded parts: {shaded}/{total}</text>'
        )
    return lines


def _clock_block(problem: ClockReadingProblem) -> list[str]:
    hour = problem.clock.hour if problem.clock.hour is not None else 3
    minute = problem.clock.minute if problem.clock.minute is not None else 0

    minute_angle = problem.clock.minute_angle
    if minute_angle is None:
        minute_angle = 90 - minute * 6
    hour_angle = problem.clock.hour_angle
    if hour_angle is None:
        hour_angle = 90 - (hour % 12) * 30 - minute * 0.5

    cx, cy = 240.0, 300.0
    minute_len = 110.0
    hour_len = 78.0
    mx = cx + minute_len * math.cos(math.radians(minute_angle))
    my = cy - minute_len * math.sin(math.radians(minute_angle))
    hx = cx + hour_len * math.cos(math.radians(hour_angle))
    hy = cy - hour_len * math.sin(math.radians(hour_angle))

    return [
        f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="130" fill="none" stroke="#222" stroke-width="2"/>',
        f'<line x1="{cx:.2f}" y1="{cy:.2f}" x2="{hx:.2f}" y2="{hy:.2f}" stroke="#222" stroke-width="4"/>',
        f'<line x1="{cx:.2f}" y1="{cy:.2f}" x2="{mx:.2f}" y2="{my:.2f}" stroke="#222" stroke-width="2"/>',
        f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="4" fill="#222"/>',
    ]


def _geometry_block(problem: GeometryBasicProblem) -> list[str]:
    if not problem.points:
        return []

    min_x = min(p.x for p in problem.points)
    max_x = max(p.x for p in problem.points)
    min_y = min(p.y for p in problem.points)
    max_y = max(p.y for p in problem.points)
    span_x = max(1e-6, max_x - min_x)
    span_y = max(1e-6, max_y - min_y)
    scale = min(360.0 / span_x, 260.0 / span_y)
    x_off, y_off = 56.0, 180.0

    coords: dict[str, tuple[float, float]] = {}
    for p in problem.points:
        x = x_off + (p.x - min_x) * scale
        y = y_off + (p.y - min_y) * scale
        coords[p.label] = (x, y)

    lines: list[str] = []
    for poly in problem.polygons:
        if len(poly) < 2:
            continue
        for i in range(len(poly)):
            a = coords.get(poly[i])
            b = coords.get(poly[(i + 1) % len(poly)])
            if a and b:
                lines.append(f'<line x1="{a[0]:.2f}" y1="{a[1]:.2f}" x2="{b[0]:.2f}" y2="{b[1]:.2f}" stroke="#222" stroke-width="2"/>')

    for seg in problem.segments:
        a = coords.get(seg.start)
        b = coords.get(seg.end)
        if a and b:
            lines.append(f'<line x1="{a[0]:.2f}" y1="{a[1]:.2f}" x2="{b[0]:.2f}" y2="{b[1]:.2f}" stroke="#222" stroke-width="2"/>')

    for label, (x, y) in coords.items():
        lines.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="3" fill="#222"/>')
        lines.append(f'<text x="{x + 6:.2f}" y="{y - 6:.2f}" font-size="20" font-family="Arial, sans-serif">{_escape_xml(label)}</text>')
    return lines


def _table_or_chart_block(problem: TableOrChartBasicProblem) -> list[str]:
    if problem.table:
        return _table_block(problem)
    if problem.chart:
        return _bar_chart_block(problem)
    return []


def _table_block(problem: TableOrChartBasicProblem) -> list[str]:
    assert problem.table is not None
    rows = [problem.table.headers] + problem.table.rows if problem.table.headers else problem.table.rows
    if not rows:
        return []

    x0, y0 = 56, 180
    cell_w, cell_h = 150, 46
    out: list[str] = []
    for r_idx, row in enumerate(rows):
        for c_idx, cell in enumerate(row):
            x = x0 + c_idx * cell_w
            y = y0 + r_idx * cell_h
            out.append(f'<rect x="{x}" y="{y}" width="{cell_w}" height="{cell_h}" fill="white" stroke="#444" stroke-width="1"/>')
            out.append(
                f'<text x="{x + 10}" y="{y + 30}" font-size="20" font-family="Noto Sans KR, Arial, sans-serif">{_escape_xml(cell)}</text>'
            )
    return out


def _bar_chart_block(problem: TableOrChartBasicProblem) -> list[str]:
    assert problem.chart is not None
    bars = problem.chart.bars
    if not bars:
        return []
    max_value = max(1.0, max(float(b.value) for b in bars))
    out = [
        '<line x1="56" y1="580" x2="600" y2="580" stroke="#222" stroke-width="2"/>',
        '<line x1="56" y1="580" x2="56" y2="180" stroke="#222" stroke-width="2"/>',
    ]
    bar_w = 56
    gap = 24
    for idx, bar in enumerate(bars):
        h = 320.0 * (float(bar.value) / max_value)
        x = 86 + idx * (bar_w + gap)
        y = 580.0 - h
        out.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{bar_w}" height="{h:.2f}" fill="#7db7ff" stroke="#335" stroke-width="1"/>')
        out.append(f'<text x="{x:.2f}" y="610" font-size="18" font-family="Noto Sans KR, Arial, sans-serif">{_escape_xml(bar.label)}</text>')
        out.append(f'<text x="{x:.2f}" y="{y - 8:.2f}" font-size="16" font-family="Arial, sans-serif">{bar.value:g}</text>')
    return out


def _fallback_reason(problem: SemanticProblem) -> str | None:
    if isinstance(problem, FractionShadedAreaProblem):
        frac = problem.fraction
        rows = frac.rows
        cols = frac.cols
        grid_ok = rows is not None and cols is not None and rows * cols == frac.total_parts
        if frac.total_parts > 24 or frac.shaded_parts > frac.total_parts or (frac.partition == "grid" and not grid_ok):
            return "render_fallback_due_to_invalid_fraction_structure"

    if isinstance(problem, GeometryBasicProblem):
        if not problem.points or (not problem.segments and not problem.polygons):
            return "render_fallback_due_to_insufficient_geometry_structure"

    if isinstance(problem, TableOrChartBasicProblem):
        table_ok = bool(problem.table and (problem.table.headers or problem.table.rows))
        chart_ok = bool(problem.chart and problem.chart.bars)
        if not (table_ok or chart_ok):
            return "render_fallback_due_to_insufficient_table_chart_structure"

    return None


def _escape_xml(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )



def _wrap_text_lines(text: str, font_size: float, max_width: float) -> list[str]:
    """Greedy wrap for mixed Korean/ASCII text without relying on browser text measurement."""
    src = " ".join((text or "").split())
    if not src:
        return [""]

    tokens = src.split(" ")
    lines: list[str] = []
    cur = ""

    for tok in tokens:
        candidate = tok if not cur else f"{cur} {tok}"
        if _estimate_text_width(candidate, font_size) <= max_width:
            cur = candidate
            continue
        if cur:
            lines.append(cur)
            cur = tok
        else:
            buf = ""
            for ch in tok:
                cand = buf + ch
                if _estimate_text_width(cand, font_size) <= max_width:
                    buf = cand
                else:
                    if buf:
                        lines.append(buf)
                    buf = ch
            cur = buf

    if cur:
        lines.append(cur)
    return lines


def _estimate_text_width(text: str, font_size: float) -> float:
    width = 0.0
    for ch in text:
        if ch.isspace():
            width += font_size * 0.33
            continue
        east_asian = unicodedata.east_asian_width(ch)
        if east_asian in {"W", "F"}:
            width += font_size * 1.0
        elif ch.isascii():
            width += font_size * 0.56
        else:
            width += font_size * 0.85
    return width


def _render_multiline_text(
    lines: list[str],
    x: float,
    y: float,
    font_size: int,
    font_family: str,
    line_height: float,
) -> tuple[str, float]:
    if not lines:
        lines = [""]

    out = [f'<text x="{x}" y="{y}" font-size="{font_size}" font-family="{font_family}">']
    for idx, line in enumerate(lines):
        if idx == 0:
            out.append(f'<tspan>{_escape_xml(line)}</tspan>')
        else:
            out.append(f'<tspan x="{x}" dy="{line_height}">{_escape_xml(line)}</tspan>')
    out.append('</text>')
    return "".join(out), y + (len(lines) - 1) * line_height


