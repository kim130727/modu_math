"""Build conservative semantic models from problem candidates."""

from __future__ import annotations

import re

from math_problem_pipeline.models.problem_models import ExtractedProblem, ProblemCandidate
from math_problem_pipeline.models.semantic_models import (
    ArithmeticExpressionProblem,
    ClockHandSpec,
    ClockReadingProblem,
    ConfidenceBreakdown,
    FractionPartition,
    FractionShadedAreaProblem,
    GenericTextProblem,
    MultiPartProblem,
    MultipleChoiceTextProblem,
    RejectedCandidateProblem,
    SemanticProblem,
    UnknownVisualMathProblem,
)
from math_problem_pipeline.normalize.type_classifier import classify_problem_type
from math_problem_pipeline.normalize.validators import validate_semantic_problem

CHOICE_SPLIT = re.compile(r"(?:①|②|③|④|⑤|\([1-5]\))")
MULTI_PART_SPLIT = re.compile(r"(?=\(\d+\)|\d+[\.|\)])")


def candidate_to_extracted(candidate: ProblemCandidate) -> ExtractedProblem:
    guess = classify_problem_type(candidate)
    question_text, choices = _split_question_and_choices(candidate.text)

    structure_confidence = 0.0
    if guess.type_name == "fraction_shaded_area" and _parse_fraction_visual_structure(question_text):
        structure_confidence = 0.75
    elif guess.type_name == "clock_reading" and _extract_clock_time(question_text):
        structure_confidence = 0.70
    elif guess.type_name == "arithmetic_expression" and _extract_expression(question_text):
        structure_confidence = 0.65
    elif guess.type_name == "multiple_choice_text" and len(choices) >= 2:
        structure_confidence = 0.65

    warnings = list(candidate.warnings)
    if not candidate.is_probable_problem:
        warnings.append("non_problem_candidate")

    return ExtractedProblem(
        problem_id=candidate.candidate_id,
        candidate_id=candidate.candidate_id,
        source_path=candidate.source_path,
        page_number=candidate.page_number,
        problem_number=candidate.problem_number,
        type_guess=guess.type_name,
        type_guess_reason=guess.reason,
        type_confidence=guess.confidence,
        question_text=question_text,
        choices=choices,
        bbox=candidate.bbox,
        segmentation_confidence=candidate.confidence,
        structure_confidence=structure_confidence,
        warnings=warnings,
        is_probable_problem=candidate.is_probable_problem,
        page_width=candidate.page_width,
        page_height=candidate.page_height,
    )


def extracted_to_semantic(extracted: ExtractedProblem) -> SemanticProblem:
    base = _base_fields(extracted)

    if extracted.type_guess == "rejected_candidate" or not extracted.is_probable_problem:
        problem: SemanticProblem = RejectedCandidateProblem(
            type="rejected_candidate",
            rejection_reason="segmentation_marked_non_problem",
            **base,
        )
    elif extracted.type_guess == "arithmetic_expression":
        expr = _extract_expression(extracted.question_text)
        if expr is None:
            problem = GenericTextProblem(type="generic_text_problem", **base)
            problem.warnings.append("arithmetic_expression_not_reliably_extracted")
        else:
            problem = ArithmeticExpressionProblem(type="arithmetic_expression", expression=expr, **base)
    elif extracted.type_guess == "fraction_shaded_area":
        structure = _parse_fraction_visual_structure(extracted.question_text)
        if structure is None:
            problem = UnknownVisualMathProblem(type="unknown_visual_math_problem", **base)
            problem.warnings.append("fraction_visual_structure_unknown")
        else:
            total, shaded, rows, cols = structure
            problem = FractionShadedAreaProblem(
                type="fraction_shaded_area",
                fraction=FractionPartition(
                    shape="rectangle",
                    total_parts=total,
                    shaded_parts=shaded,
                    rows=rows,
                    cols=cols,
                    partition="grid",
                    shaded_indices=list(range(shaded)),
                ),
                **base,
            )
    elif extracted.type_guess == "clock_reading":
        hm = _extract_clock_time(extracted.question_text)
        if hm is None:
            problem = GenericTextProblem(type="generic_text_problem", **base)
            problem.warnings.append("clock_time_not_reliably_extracted")
        else:
            hour, minute = hm
            problem = ClockReadingProblem(type="clock_reading", clock=ClockHandSpec(hour=hour, minute=minute), **base)
    elif extracted.type_guess == "multi_part_problem":
        parts = _extract_multi_parts(extracted.question_text)
        if len(parts) >= 2:
            problem = MultiPartProblem(type="multi_part_problem", parts=parts, **base)
        else:
            problem = GenericTextProblem(type="generic_text_problem", **base)
            problem.warnings.append("multi_part_structure_unclear")
    elif extracted.type_guess == "multiple_choice_text":
        if len(extracted.choices) >= 2:
            problem = MultipleChoiceTextProblem(type="multiple_choice_text", choices=extracted.choices, **base)
        else:
            problem = GenericTextProblem(type="generic_text_problem", **base)
            problem.warnings.append("choice_structure_unclear")
    elif extracted.type_guess in {"geometry_basic", "table_or_chart_basic", "unknown_visual_math_problem"}:
        problem = UnknownVisualMathProblem(type="unknown_visual_math_problem", **base)
        problem.warnings.append("visual_structure_detection_needed")
    else:
        problem = GenericTextProblem(type="generic_text_problem", **base)

    problem.warnings.extend(validate_semantic_problem(problem))
    problem.warnings = sorted(set(problem.warnings))
    return problem


def _base_fields(extracted: ExtractedProblem) -> dict:
    total_conf = (extracted.segmentation_confidence + extracted.type_confidence + extracted.structure_confidence) / 3
    return {
        "problem_id": extracted.problem_id,
        "source_path": extracted.source_path,
        "page_number": extracted.page_number,
        "question_text": extracted.question_text,
        "bbox": extracted.bbox,
        "confidence": max(0.0, min(1.0, total_conf)),
        "confidence_breakdown": ConfidenceBreakdown(
            segmentation_confidence=extracted.segmentation_confidence,
            type_confidence=extracted.type_confidence,
            structure_confidence=extracted.structure_confidence,
        ),
        "warnings": list(extracted.warnings),
        "type_guess": extracted.type_guess,
        "type_guess_reason": extracted.type_guess_reason,
        "coordinates": {
            "source_coordinates": {
                "page_width": extracted.page_width,
                "page_height": extracted.page_height,
            },
            "semantic_coordinates": {},
            "render_coordinates": {},
        },
    }


def _split_question_and_choices(text: str) -> tuple[str, list[str]]:
    parts = [p.strip() for p in CHOICE_SPLIT.split(text) if p.strip()]
    if len(parts) <= 1:
        return text.strip(), []
    return parts[0], parts[1:]


def _extract_expression(text: str) -> str | None:
    clean = " ".join(text.split())
    if len(clean) > 64:
        return None
    m = re.search(r"([\d\s\+\-\*/\(\)=÷×\.]+)", clean)
    if not m:
        return None
    expr = m.group(1).strip()
    digits = sum(ch.isdigit() for ch in expr)
    ops = sum(ch in "+-*/=÷×" for ch in expr)
    if digits < 2 or ops < 1:
        return None
    return expr


def _parse_fraction_visual_structure(text: str) -> tuple[int, int, int | None, int | None] | None:
    # Accept only explicit and plausible structures such as "8칸 중 3칸".
    m = re.search(r"(\d{1,2})\s*칸\s*중\s*(\d{1,2})\s*칸", text)
    if not m:
        return None

    total = int(m.group(1))
    shaded = int(m.group(2))
    if total <= 0 or shaded < 0 or shaded > total or total > 24:
        return None

    rows = None
    cols = None
    rc = re.search(r"(\d{1,2})\s*[xX×]\s*(\d{1,2})", text)
    if rc:
        rows = int(rc.group(1))
        cols = int(rc.group(2))
        if rows * cols != total:
            rows = None
            cols = None
    return total, shaded, rows, cols


def _extract_clock_time(text: str) -> tuple[int, int] | None:
    hm = re.search(r"(\d{1,2})\s*시\s*(\d{1,2})\s*분", text)
    if hm:
        return int(hm.group(1)) % 12, int(hm.group(2)) % 60
    h = re.search(r"(\d{1,2})\s*시", text)
    if h and "시계" in text:
        return int(h.group(1)) % 12, 0
    return None


def _extract_multi_parts(text: str) -> list[str]:
    parts = [p.strip() for p in MULTI_PART_SPLIT.split(text) if p.strip()]
    return [p for p in parts if len(p) > 1]

