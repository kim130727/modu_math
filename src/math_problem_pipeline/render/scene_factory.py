"""Scene factory to map semantic type -> builder function with safety fallbacks."""

from __future__ import annotations

from math_problem_pipeline.models.semantic_models import (
    ArithmeticExpressionProblem,
    ClockReadingProblem,
    FractionShadedAreaProblem,
    GeometryBasicProblem,
    MultipleChoiceTextProblem,
    SemanticProblem,
    TableOrChartBasicProblem,
)
from math_problem_pipeline.models.render_models import StyleHint
from math_problem_pipeline.render import figure_builders as fb


def build_scene_mobjects(problem: SemanticProblem, style_hint: StyleHint | None = None):
    style = style_hint or StyleHint()

    fallback_reason = _fallback_reason(problem)
    if fallback_reason:
        problem.warnings.append(fallback_reason)
        return fb.build_common_text(problem, style)

    if isinstance(problem, MultipleChoiceTextProblem):
        return fb.build_multiple_choice(problem, style)
    if isinstance(problem, ArithmeticExpressionProblem):
        return fb.build_arithmetic(problem, style)
    if isinstance(problem, FractionShadedAreaProblem):
        return fb.build_fraction(problem, style)
    if isinstance(problem, ClockReadingProblem):
        return fb.build_clock(problem, style)
    if isinstance(problem, GeometryBasicProblem):
        return fb.build_geometry(problem, style)
    if isinstance(problem, TableOrChartBasicProblem):
        return fb.build_table_or_chart(problem, style)

    return fb.build_common_text(problem, style)


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
