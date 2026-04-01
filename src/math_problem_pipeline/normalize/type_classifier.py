"""Rule-based type classifier for problem candidates."""

from __future__ import annotations

import re

from math_problem_pipeline.models.problem_models import ProblemCandidate


def classify_problem_type(candidate: ProblemCandidate) -> str:
    text = candidate.text

    if re.search(r"시계|몇\s*시|몇\s*분", text):
        return "clock_reading"
    if re.search(r"색칠|분수|\d+/\d+", text) and re.search(r"칸|부분|도형|원|직사각형", text):
        return "fraction_shaded_area"
    if re.search(r"표|그래프|막대", text):
        return "table_or_chart_basic"
    if re.search(r"삼각형|사각형|각|길이|점\s*[A-Z]", text):
        return "geometry_basic"
    if re.search(r"[\d\s\+\-\*/\(\)]+", text) and re.search(r"=|계산", text):
        return "arithmetic_expression"
    return "multiple_choice_text"
