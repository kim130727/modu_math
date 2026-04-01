"""Build semantic JSON models from problem candidates."""

from __future__ import annotations

import re

from math_problem_pipeline.models.problem_models import ExtractedProblem, ProblemCandidate
from math_problem_pipeline.models.semantic_models import (
    ArithmeticExpressionProblem,
    ClockHandSpec,
    ClockReadingProblem,
    FractionPartition,
    FractionShadedAreaProblem,
    GeometryBasicProblem,
    GeometryPoint,
    GeometrySegment,
    MultipleChoiceTextProblem,
    SemanticProblem,
    TableOrChartBasicProblem,
    TableSpec,
)
from math_problem_pipeline.normalize.type_classifier import classify_problem_type
from math_problem_pipeline.normalize.validators import validate_semantic_problem

CHOICE_SPLIT = re.compile(r"(?:①|②|③|④|⑤|\([1-5]\))")


def candidate_to_extracted(candidate: ProblemCandidate) -> ExtractedProblem:
    type_guess = classify_problem_type(candidate)
    question_text, choices = _split_question_and_choices(candidate.text)
    return ExtractedProblem(
        problem_id=candidate.candidate_id,
        candidate_id=candidate.candidate_id,
        source_pdf=candidate.source_pdf,
        page_number=candidate.page_number,
        problem_number=candidate.problem_number,
        type_guess=type_guess,
        question_text=question_text,
        choices=choices,
        bbox=candidate.bbox,
        confidence=max(0.5, candidate.confidence),
        warnings=candidate.warnings,
    )


def extracted_to_semantic(extracted: ExtractedProblem) -> SemanticProblem:
    base = dict(
        problem_id=extracted.problem_id,
        source_pdf=extracted.source_pdf,
        page_number=extracted.page_number,
        question_text=extracted.question_text,
        bbox=extracted.bbox,
        confidence=extracted.confidence,
        warnings=list(extracted.warnings),
    )

    problem: SemanticProblem

    if extracted.type_guess == "arithmetic_expression":
        expr = _extract_expression(extracted.question_text)
        problem = ArithmeticExpressionProblem(type="arithmetic_expression", expression=expr, **base)
    elif extracted.type_guess == "fraction_shaded_area":
        total, shaded = _extract_fraction_counts(extracted.question_text)
        problem = FractionShadedAreaProblem(
            type="fraction_shaded_area",
            fraction=FractionPartition(
                shape="rectangle",
                total_parts=total,
                shaded_parts=shaded,
                rows=2,
                cols=max(1, total // 2),
                partition="grid",
                shaded_indices=list(range(shaded)),
            ),
            **base,
        )
    elif extracted.type_guess == "clock_reading":
        hour, minute = _extract_clock_time(extracted.question_text)
        problem = ClockReadingProblem(
            type="clock_reading",
            clock=ClockHandSpec(hour=hour, minute=minute),
            **base,
        )
    elif extracted.type_guess == "geometry_basic":
        problem = GeometryBasicProblem(
            type="geometry_basic",
            points=[
                GeometryPoint(label="A", x=0.0, y=0.0),
                GeometryPoint(label="B", x=2.5, y=0.0),
                GeometryPoint(label="C", x=1.2, y=1.8),
            ],
            segments=[
                GeometrySegment(start="A", end="B", length_label=None),
                GeometrySegment(start="B", end="C", length_label=None),
                GeometrySegment(start="C", end="A", length_label=None),
            ],
            polygons=[["A", "B", "C"]],
            **base,
        )
        problem.warnings.append("geometry_inferred_from_defaults")
    elif extracted.type_guess == "table_or_chart_basic":
        problem = TableOrChartBasicProblem(
            type="table_or_chart_basic",
            table=TableSpec(headers=["항목", "값"], rows=[["A", "10"], ["B", "12"]]),
            chart=None,
            **base,
        )
        problem.warnings.append("table_structure_inferred")
    else:
        problem = MultipleChoiceTextProblem(
            type="multiple_choice_text",
            choices=extracted.choices,
            **base,
        )

    problem.warnings.extend(validate_semantic_problem(problem))
    return problem


def _split_question_and_choices(text: str) -> tuple[str, list[str]]:
    parts = [p.strip() for p in CHOICE_SPLIT.split(text) if p.strip()]
    if len(parts) <= 1:
        return text.strip(), []
    return parts[0], parts[1:]


def _extract_expression(text: str) -> str:
    match = re.search(r"([\d\s\+\-\*/\(\)]+)", text)
    if not match:
        return text
    return match.group(1).strip()


def _extract_fraction_counts(text: str) -> tuple[int, int]:
    frac = re.search(r"(\d+)\s*/\s*(\d+)", text)
    if frac:
        return int(frac.group(2)), int(frac.group(1))
    nums = [int(n) for n in re.findall(r"\d+", text)]
    if len(nums) >= 2:
        return max(nums[0], nums[1]), min(nums[0], nums[1])
    return (4, 1)


def _extract_clock_time(text: str) -> tuple[int, int]:
    hm = re.search(r"(\d{1,2})\s*시\s*(\d{1,2})\s*분", text)
    if hm:
        return (int(hm.group(1)) % 12, int(hm.group(2)) % 60)
    h = re.search(r"(\d{1,2})\s*시", text)
    if h:
        return (int(h.group(1)) % 12, 0)
    return (3, 0)
