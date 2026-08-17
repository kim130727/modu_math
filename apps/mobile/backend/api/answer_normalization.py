from __future__ import annotations

import re
from typing import Any


def numeric_answer_text(value: Any, unit: str = "") -> str | None:
    if isinstance(value, bool) or value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    text = text.replace(",", "")
    unit_text = unit.strip()
    if unit_text:
        text = re.sub(rf"\s*{re.escape(unit_text)}\s*$", "", text)
    match = re.fullmatch(r"\s*([+-]?\d+(?:\.\d+)?)\s*(?:[^\d\s.,+-]+)?\s*", text)
    if not match:
        return None
    number_text = match.group(1)
    if "." not in number_text:
        return str(int(number_text))
    return str(float(number_text)).rstrip("0").rstrip(".")


def normalize_correct_answer(value: Any, unit: str = "") -> str:
    numeric = numeric_answer_text(value, unit)
    return numeric if numeric is not None else str(value or "").strip()


def answers_match(student_answer: Any, correct_answer: Any, unit: str = "") -> bool:
    student_number = numeric_answer_text(student_answer, unit)
    correct_number = numeric_answer_text(correct_answer, unit)
    if student_number is not None and correct_number is not None:
        return student_number == correct_number
    return str(student_answer or "").strip() == str(correct_answer or "").strip()
