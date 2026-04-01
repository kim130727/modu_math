"""LaTeX/TikZ renderer entrypoints for intermediate semantic checks."""

from __future__ import annotations

import math
import shutil
import subprocess
from pathlib import Path

from math_problem_pipeline.models.semantic_models import (
    ArithmeticExpressionProblem,
    ClockReadingProblem,
    FractionShadedAreaProblem,
    GeometryBasicProblem,
    MultipleChoiceTextProblem,
    SemanticProblem,
    TableOrChartBasicProblem,
)
from math_problem_pipeline.utils.io import ensure_dir
from math_problem_pipeline.utils.logging_utils import setup_logger

logger = setup_logger(__name__)


def render_problem_to_tikz_tex(problem: SemanticProblem, output_tex: Path, compile_pdf: bool = True) -> dict:
    """Render a semantic problem into a standalone .tex document with TikZ."""
    ensure_dir(output_tex.parent)
    tex = build_tikz_document(problem)
    output_tex.write_text(tex, encoding="utf-8")

    meta = {
        "problem_id": problem.problem_id,
        "rendered": True,
        "output_tex": str(output_tex),
        "used_fields": ["question_text", "type", "render_hint"],
    }

    if compile_pdf:
        pdf_meta = compile_tikz_tex_to_pdf(output_tex)
        meta.update(pdf_meta)

    return meta


def compile_tikz_tex_to_pdf(tex_path: Path) -> dict:
    """Compile standalone TikZ .tex to .pdf if pdflatex is available."""
    pdflatex = shutil.which("pdflatex")
    if not pdflatex:
        return {
            "compiled_pdf": False,
            "compile_reason": "pdflatex_not_found",
        }

    cmd = [
        pdflatex,
        "-interaction=nonstopmode",
        "-halt-on-error",
        "-output-directory",
        str(tex_path.parent),
        str(tex_path),
    ]

    result = subprocess.run(cmd, capture_output=True)
    out_pdf = tex_path.with_suffix(".pdf")
    if result.returncode != 0 or not out_pdf.exists():
        logger.warning("TikZ compile failed for %s", tex_path)
        return {
            "compiled_pdf": False,
            "compile_reason": "pdflatex_failed",
            "latex_log_tail": ((result.stderr or result.stdout or b"").decode("utf-8", errors="ignore"))[-500:],
        }

    return {
        "compiled_pdf": True,
        "output_pdf": str(out_pdf),
    }


def build_tikz_document(problem: SemanticProblem) -> str:
    """Build standalone LaTeX document text for one semantic problem."""
    lines = [
        r"\documentclass[tikz,border=6pt]{standalone}",
        r"\usepackage{tikz}",
        r"\usepackage{amsmath}",
        r"\usetikzlibrary{arrows.meta,calc,matrix,positioning}",
        r"\begin{document}",
        r"\begin{tikzpicture}[x=1cm,y=1cm]",
        _question_block(problem.question_text),
        _problem_body(problem),
        r"\end{tikzpicture}",
        r"\end{document}",
        "",
    ]
    return "\n".join(lines)


def _question_block(text: str) -> str:
    return rf"\node[anchor=north west,align=left,text width=13cm] at (-0.5,4.8) {{{_escape_tex(text)}}};"


def _problem_body(problem: SemanticProblem) -> str:
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
    return ""


def _multiple_choice_block(problem: MultipleChoiceTextProblem) -> str:
    if not problem.choices:
        return ""
    lines = []
    for idx, choice in enumerate(problem.choices, start=1):
        y = 3.6 - (idx - 1) * 0.8
        lines.append(
            rf"\node[anchor=west] at (0,{y:.2f}) {{{idx}. {_escape_tex(choice)}}};"
        )
    return "\n".join(lines)


def _arithmetic_block(problem: ArithmeticExpressionProblem) -> str:
    expr = _escape_tex(problem.expression)
    return rf"\node[anchor=west] at (0,2.8) {{$\displaystyle {expr}$}};"


def _fraction_block(problem: FractionShadedAreaProblem) -> str:
    frac = problem.fraction
    if frac.shape == "rectangle":
        return _fraction_rectangle_block(problem)
    return _fraction_circle_block(problem)


def _fraction_rectangle_block(problem: FractionShadedAreaProblem) -> str:
    frac = problem.fraction
    cols = max(1, frac.cols or frac.total_parts)
    rows = max(1, frac.rows or 1)
    width = 4.0
    height = 4.0 * rows / cols if cols else 2.0
    cell_w = width / cols
    cell_h = height / rows
    x0, y0 = 0.0, 2.8

    lines = [rf"\draw[thick] ({x0:.3f},{y0:.3f}) rectangle ({x0+width:.3f},{y0-height:.3f});"]
    shaded = set(frac.shaded_indices) if frac.shaded_indices else set(range(frac.shaded_parts))
    for i in range(frac.total_parts):
        r = i // cols
        c = i % cols
        x1 = x0 + c * cell_w
        y1 = y0 - r * cell_h
        x2 = x1 + cell_w
        y2 = y1 - cell_h
        if i in shaded:
            lines.append(rf"\fill[blue!35] ({x1:.3f},{y1:.3f}) rectangle ({x2:.3f},{y2:.3f});")
        lines.append(rf"\draw ({x1:.3f},{y1:.3f}) rectangle ({x2:.3f},{y2:.3f});")
    return "\n".join(lines)


def _fraction_circle_block(problem: FractionShadedAreaProblem) -> str:
    frac = problem.fraction
    total = max(1, frac.total_parts)
    shaded = frac.shaded_parts
    cx, cy, r = 2.0, 1.8, 1.5
    lines = [rf"\draw[thick] ({cx:.3f},{cy:.3f}) circle ({r:.3f});"]
    for i in range(total):
        start = 90 - (360 / total) * i
        end = 90 - (360 / total) * (i + 1)
        if i < shaded:
            lines.append(
                rf"\fill[blue!35] ({cx:.3f},{cy:.3f}) -- ++({start:.4f}:{r:.3f}) arc ({start:.4f}:{end:.4f}:{r:.3f}) -- cycle;"
            )
        lines.append(
            rf"\draw ({cx:.3f},{cy:.3f}) -- ++({start:.4f}:{r:.3f});"
        )
    return "\n".join(lines)


def _clock_block(problem: ClockReadingProblem) -> str:
    hour = problem.clock.hour if problem.clock.hour is not None else 3
    minute = problem.clock.minute if problem.clock.minute is not None else 0

    minute_angle = problem.clock.minute_angle
    if minute_angle is None:
        minute_angle = 90 - minute * 6
    hour_angle = problem.clock.hour_angle
    if hour_angle is None:
        hour_angle = 90 - (hour % 12) * 30 - minute * 0.5

    cx, cy = 2.0, 1.8
    minute_len = 1.4
    hour_len = 1.0
    mx = cx + minute_len * math.cos(math.radians(minute_angle))
    my = cy + minute_len * math.sin(math.radians(minute_angle))
    hx = cx + hour_len * math.cos(math.radians(hour_angle))
    hy = cy + hour_len * math.sin(math.radians(hour_angle))

    lines = [
        rf"\draw[thick] ({cx:.3f},{cy:.3f}) circle (1.6);",
        rf"\draw[line width=1.1pt] ({cx:.3f},{cy:.3f}) -- ({hx:.3f},{hy:.3f});",
        rf"\draw[line width=0.7pt] ({cx:.3f},{cy:.3f}) -- ({mx:.3f},{my:.3f});",
        rf"\fill ({cx:.3f},{cy:.3f}) circle (0.05);",
    ]
    return "\n".join(lines)


def _geometry_block(problem: GeometryBasicProblem) -> str:
    if not problem.points:
        return ""

    min_x = min(p.x for p in problem.points)
    max_x = max(p.x for p in problem.points)
    min_y = min(p.y for p in problem.points)
    max_y = max(p.y for p in problem.points)
    span_x = max(1e-6, max_x - min_x)
    span_y = max(1e-6, max_y - min_y)
    scale = min(4.0 / span_x, 3.0 / span_y)
    x_off, y_off = 0.0, 0.8

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
                lines.append(rf"\draw ({a[0]:.3f},{a[1]:.3f}) -- ({b[0]:.3f},{b[1]:.3f});")

    for seg in problem.segments:
        a = coords.get(seg.start)
        b = coords.get(seg.end)
        if a and b:
            lines.append(rf"\draw ({a[0]:.3f},{a[1]:.3f}) -- ({b[0]:.3f},{b[1]:.3f});")

    for label, (x, y) in coords.items():
        lines.append(rf"\fill ({x:.3f},{y:.3f}) circle (0.045);")
        lines.append(rf"\node[anchor=west] at ({x+0.08:.3f},{y+0.08:.3f}) {{{_escape_tex(label)}}};")
    return "\n".join(lines)


def _table_or_chart_block(problem: TableOrChartBasicProblem) -> str:
    if problem.table:
        return _table_block(problem)
    if problem.chart:
        return _bar_chart_block(problem)
    return ""


def _table_block(problem: TableOrChartBasicProblem) -> str:
    assert problem.table is not None
    matrix_rows = [problem.table.headers] + problem.table.rows if problem.table.headers else problem.table.rows
    if not matrix_rows:
        return ""
    rows = []
    for row in matrix_rows:
        cells = " & ".join(_escape_tex(cell) for cell in row)
        rows.append(cells + r" \\")
    body = "\n".join(rows)
    return "\n".join(
        [
            r"\matrix (m) [matrix of nodes, nodes in empty cells, nodes={draw,minimum width=1.8cm,minimum height=0.8cm,anchor=center}] at (3.0,1.8) {",
            body,
            r"};",
        ]
    )


def _bar_chart_block(problem: TableOrChartBasicProblem) -> str:
    assert problem.chart is not None
    bars = problem.chart.bars
    if not bars:
        return ""
    max_value = max(1.0, max(float(b.value) for b in bars))
    lines = [
        r"\draw[->] (0,0.4) -- (6.2,0.4);",
        r"\draw[->] (0,0.4) -- (0,3.8);",
    ]
    bar_w = 0.8
    gap = 0.4
    for idx, bar in enumerate(bars):
        h = 3.0 * (float(bar.value) / max_value)
        x1 = 0.5 + idx * (bar_w + gap)
        x2 = x1 + bar_w
        lines.append(rf"\fill[blue!30] ({x1:.3f},0.4) rectangle ({x2:.3f},{0.4+h:.3f});")
        lines.append(rf"\draw ({x1:.3f},0.4) rectangle ({x2:.3f},{0.4+h:.3f});")
        lines.append(rf"\node[anchor=north] at ({(x1+x2)/2:.3f},0.25) {{{_escape_tex(bar.label)}}};")
        lines.append(rf"\node[anchor=south] at ({(x1+x2)/2:.3f},{0.45+h:.3f}) {{{bar.value:g}}};")
    return "\n".join(lines)


def _escape_tex(text: str) -> str:
    escaped = (
        text.replace("\\", r"\textbackslash{}")
        .replace("&", r"\&")
        .replace("%", r"\%")
        .replace("$", r"\$")
        .replace("#", r"\#")
        .replace("_", r"\_")
        .replace("{", r"\{")
        .replace("}", r"\}")
        .replace("~", r"\textasciitilde{}")
        .replace("^", r"\textasciicircum{}")
    )
    return escaped.replace("\n", r"\\ ")

