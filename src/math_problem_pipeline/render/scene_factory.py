"""Scene factory to map semantic type -> builder function."""

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
