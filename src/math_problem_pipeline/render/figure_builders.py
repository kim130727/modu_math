"""Type-specific mobject builders for semantic problems."""

from __future__ import annotations

from typing import Any

from math_problem_pipeline.models.semantic_models import (
    ArithmeticExpressionProblem,
    ClockReadingProblem,
    FractionShadedAreaProblem,
    GeometryBasicProblem,
    MultipleChoiceTextProblem,
    TableOrChartBasicProblem,
)
from math_problem_pipeline.render.layout_engine import resolve_choices_position, resolve_question_position

try:
    from manim import Circle, Dot, Line, Rectangle, Square, Table, Text, VGroup
except Exception:  # pragma: no cover
    Circle = Dot = Line = Rectangle = Square = Table = Text = VGroup = Any


def build_common_text(problem, style_hint):
    question_pos = resolve_question_position(problem.render_hint)
    question = Text(problem.question_text, font_size=style_hint.font_size)
    question.move_to([question_pos[0], question_pos[1], 0])
    return [question]


def build_multiple_choice(problem: MultipleChoiceTextProblem, style_hint):
    mobjects = build_common_text(problem, style_hint)
    if not problem.choices:
        return mobjects

    cx, cy = resolve_choices_position(problem.render_hint)
    rows = []
    for idx, choice in enumerate(problem.choices, start=1):
        rows.append(Text(f"{idx}. {choice}", font_size=max(22, style_hint.font_size - 6)))
    vg = VGroup(*rows).arrange(direction=[0, -1, 0], aligned_edge=[-1, 0, 0], buff=0.25)
    vg.move_to([cx, cy, 0], aligned_edge=[-1, 1, 0])
    mobjects.append(vg)
    return mobjects


def build_arithmetic(problem: ArithmeticExpressionProblem, style_hint):
    mobjects = build_common_text(problem, style_hint)
    expr = Text(problem.expression, font_size=style_hint.font_size + 6)
    expr.move_to([0, 0, 0])
    mobjects.append(expr)
    return mobjects


def build_fraction(problem: FractionShadedAreaProblem, style_hint):
    mobjects = build_common_text(problem, style_hint)
    frac = problem.fraction

    if frac.shape == "rectangle":
        cols = frac.cols or frac.total_parts
        rows = frac.rows or 1
        size = 3.2
        cell = size / max(cols, rows)
        origin_x = -size / 2
        origin_y = 0.8

        for i in range(frac.total_parts):
            r = i // cols
            c = i % cols
            sq = Square(side_length=cell)
            sq.move_to([origin_x + (c + 0.5) * cell, origin_y - (r + 0.5) * cell, 0])
            if i in frac.shaded_indices or i < frac.shaded_parts:
                sq.set_fill("#60a5fa", opacity=0.8)
            mobjects.append(sq)
    else:
        circle = Circle(radius=1.8)
        circle.move_to([0, 0.8, 0])
        mobjects.append(circle)

    return mobjects


def build_clock(problem: ClockReadingProblem, style_hint):
    mobjects = build_common_text(problem, style_hint)
    clock = Circle(radius=1.8)
    center = [0, 0.8, 0]
    clock.move_to(center)
    mobjects.append(clock)

    hour = problem.clock.hour if problem.clock.hour is not None else 3
    minute = problem.clock.minute if problem.clock.minute is not None else 0

    minute_angle = problem.clock.minute_angle
    if minute_angle is None:
        minute_angle = 90 - minute * 6

    hour_angle = problem.clock.hour_angle
    if hour_angle is None:
        hour_angle = 90 - (hour % 12) * 30 - minute * 0.5

    minute_end = [
        center[0] + 1.4 * _cos_deg(minute_angle),
        center[1] + 1.4 * _sin_deg(minute_angle),
        0,
    ]
    hour_end = [
        center[0] + 1.0 * _cos_deg(hour_angle),
        center[1] + 1.0 * _sin_deg(hour_angle),
        0,
    ]
    mobjects.append(Line(center, hour_end).set_stroke(width=6))
    mobjects.append(Line(center, minute_end).set_stroke(width=3))
    mobjects.append(Dot(center))
    return mobjects


def build_geometry(problem: GeometryBasicProblem, style_hint):
    mobjects = build_common_text(problem, style_hint)
    by_label = {p.label: p for p in problem.points}
    scale = 1.3

    for poly in problem.polygons:
        for i in range(len(poly)):
            a = by_label.get(poly[i])
            b = by_label.get(poly[(i + 1) % len(poly)])
            if not a or not b:
                continue
            mobjects.append(Line([a.x * scale, a.y * scale - 1.2, 0], [b.x * scale, b.y * scale - 1.2, 0]))

    for p in problem.points:
        point = Dot([p.x * scale, p.y * scale - 1.2, 0])
        label = Text(p.label, font_size=24).next_to(point, [0.5, 0.5, 0])
        mobjects.extend([point, label])

    return mobjects


def build_table_or_chart(problem: TableOrChartBasicProblem, style_hint):
    mobjects = build_common_text(problem, style_hint)

    if problem.table:
        values = [problem.table.headers] + problem.table.rows
        table = Table(values, include_outer_lines=True)
        table.scale(0.5)
        table.move_to([0, -0.3, 0])
        mobjects.append(table)

    return mobjects


def _cos_deg(deg: float) -> float:
    import math

    return math.cos(math.radians(deg))


def _sin_deg(deg: float) -> float:
    import math

    return math.sin(math.radians(deg))
