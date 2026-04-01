"""Semantic validation rules."""

from __future__ import annotations

from math_problem_pipeline.models.semantic_models import (
    FractionShadedAreaProblem,
    GeometryBasicProblem,
    SemanticProblem,
)


def validate_semantic_problem(problem: SemanticProblem) -> list[str]:
    """Return schema-level warning list."""
    warnings: list[str] = []

    if isinstance(problem, FractionShadedAreaProblem):
        if problem.fraction.shaded_parts > problem.fraction.total_parts:
            warnings.append("shaded_parts_exceeds_total_parts")
        if problem.fraction.partition == "grid" and (problem.fraction.rows is None or problem.fraction.cols is None):
            warnings.append("ambiguous_fraction_partition")

    if isinstance(problem, GeometryBasicProblem):
        if not problem.points:
            warnings.append("missing_geometry_vertices")

    if not problem.question_text.strip():
        warnings.append("missing_question_text")

    return warnings
