"""Conservative type classifier for problem candidates."""

from __future__ import annotations

import re
from dataclasses import dataclass

from math_problem_pipeline.models.problem_models import ProblemCandidate


@dataclass
class TypeGuess:
    type_name: str
    reason: str
    confidence: float


FRACTION_VISUAL_WORDS = re.compile(r"색칠|도형|칸|부분|전체")
FRACTION_NUMBER = re.compile(r"\d+\s*/\s*\d+")
CLOCK_WORDS = re.compile(r"시계|몇\s*시|몇\s*분")
GEOMETRY_SHAPE = re.compile(r"삼각형|사각형|원|직선|도형")
GEOMETRY_POINT = re.compile(r"점\s*[A-Z가-힣]|[A-Z]{2,3}")
GEOMETRY_MEASURE = re.compile(r"길이|각도|\d+\s*cm|\d+°")
TABLE_CHART = re.compile(r"표|그래프|막대")
TABLE_DETAIL = re.compile(r"행|열|항목|개수|자료|합계")
ARITH_ONLY = re.compile(r"^[\d\s\+\-\*/\(\)＝=xX÷×\.]+$")
CHOICE_MARKER = re.compile(r"[①②③④⑤]|\(?[1-5]\)")
MULTI_PART = re.compile(r"\(\d+\)|\d+[\.|\)]")


def classify_problem_type(candidate: ProblemCandidate) -> TypeGuess:
    text = " ".join(candidate.text.split())
    if not candidate.is_probable_problem:
        return TypeGuess("rejected_candidate", "candidate_marked_as_non_problem", 0.98)

    if _is_fraction_visual(text):
        return TypeGuess("fraction_shaded_area", "fraction_visual_keywords_and_structure_present", 0.82)

    if CLOCK_WORDS.search(text):
        return TypeGuess("clock_reading", "explicit_clock_time_keywords", 0.86)

    if _is_geometry(text):
        return TypeGuess("geometry_basic", "shape_plus_point_or_measure_keywords", 0.78)

    if _is_table_chart(text):
        return TypeGuess("table_or_chart_basic", "table_chart_keywords_with_structure_clues", 0.80)

    if _is_arithmetic_expression_text(text):
        return TypeGuess("arithmetic_expression", "short_math_expression_dominant", 0.72)

    if _is_multi_part_problem(text):
        return TypeGuess("multi_part_problem", "multiple_subquestion_markers_detected", 0.70)

    if CHOICE_MARKER.search(text):
        return TypeGuess("multiple_choice_text", "choice_markers_detected", 0.68)

    if _looks_visual_but_unknown(text):
        return TypeGuess("unknown_visual_math_problem", "visual_math_clues_without_reliable_structure", 0.55)

    return TypeGuess("generic_text_problem", "no_reliable_type_signal", 0.50)


def _is_fraction_visual(text: str) -> bool:
    return bool(FRACTION_NUMBER.search(text) and len(FRACTION_VISUAL_WORDS.findall(text)) >= 2)


def _is_geometry(text: str) -> bool:
    return bool(GEOMETRY_SHAPE.search(text) and (GEOMETRY_POINT.search(text) or GEOMETRY_MEASURE.search(text)))


def _is_table_chart(text: str) -> bool:
    return bool(TABLE_CHART.search(text) and TABLE_DETAIL.search(text))


def _is_arithmetic_expression_text(text: str) -> bool:
    if len(text) > 140:
        return False
    digits = sum(ch.isdigit() for ch in text)
    ops = sum(ch in "+-*/=÷×" for ch in text)
    if ARITH_ONLY.match(text):
        return digits >= 2 and ops >= 1

    # HWPX OCR/encoding noise can mix words with equations; keep conservative
    # but allow short statements with clear equation structure.
    if digits >= 2 and ("=" in text or ops >= 2):
        return True
    return False


def _is_multi_part_problem(text: str) -> bool:
    return len(MULTI_PART.findall(text)) >= 2


def _looks_visual_but_unknown(text: str) -> bool:
    visual = re.search(r"도형|그림|색칠|표|그래프|시계", text)
    return bool(visual)


