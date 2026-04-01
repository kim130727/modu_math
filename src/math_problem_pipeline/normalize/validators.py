"""Validation rules for conservative semantic pipeline."""

from __future__ import annotations

from math_problem_pipeline.models.problem_models import ProblemCandidate
from math_problem_pipeline.models.semantic_models import (
    FractionShadedAreaProblem,
    MultipleChoiceTextProblem,
    SemanticProblem,
)


def validate_candidate(candidate: ProblemCandidate) -> list[str]:
    warnings: list[str] = []
    if candidate.page_height and (candidate.bbox.y1 - candidate.bbox.y0) >= candidate.page_height * 0.5:
        warnings.append("oversized_candidate")
    if len(candidate.text) > 260:
        warnings.append("merged_multiple_problems_suspected")
    if not candidate.is_probable_problem:
        warnings.append("rejected_non_problem_candidate")
    return warnings


def validate_semantic_problem(problem: SemanticProblem) -> list[str]:
    """Return schema-level warning list."""
    warnings: list[str] = []

    if isinstance(problem, FractionShadedAreaProblem):
        frac = problem.fraction
        if frac.shaded_parts > frac.total_parts:
            warnings.append("shaded_parts_exceeds_total_parts")
        if frac.total_parts > 24:
            warnings.append("invalid_fraction_structure")
        if frac.partition == "grid":
            if frac.rows is None or frac.cols is None:
                warnings.append("ambiguous_fraction_partition")
            elif frac.rows * frac.cols != frac.total_parts:
                warnings.append("invalid_fraction_structure")

    if isinstance(problem, MultipleChoiceTextProblem) and len(problem.choices) == 1:
        warnings.append("invalid_choice_extraction")

    page_height = problem.coordinates.source_coordinates.get("page_height") if problem.coordinates else None
    if page_height and problem.bbox and (problem.bbox.y1 - problem.bbox.y0) >= float(page_height) * 0.5:
        warnings.append("oversized_candidate")

    if len(problem.question_text.strip()) > 260:
        warnings.append("merged_multiple_problems_suspected")

    if not problem.question_text.strip():
        warnings.append("missing_question_text")

    return warnings
