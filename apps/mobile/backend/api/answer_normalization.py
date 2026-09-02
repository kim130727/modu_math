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


def _extract_tokens(value: Any) -> list[str]:
    if isinstance(value, (list, tuple)):
        return [str(v).strip() for v in value if str(v).strip()]
    text = str(value or "").strip()
    if re.search(r"[/,;|\s]", text):
        parts = [p.strip() for p in re.split(r"[/,;|\s]+", text) if p.strip()]
        if len(parts) > 1:
            return parts
    return []


def _is_permutation_concatenation(tokens: list[str], raw: str) -> bool:
    total_len = sum(len(t) for t in tokens)
    if total_len != len(raw):
        return False

    def helper(remaining: list[str], current: str) -> bool:
        if not remaining:
            return not current
        for i, token in enumerate(remaining):
            if current.startswith(token):
                if helper(remaining[:i] + remaining[i + 1 :], current[len(token) :]):
                    return True
        return False

    return helper(tokens, raw)


def answers_match(student_answer: Any, correct_answer: Any, unit: str = "") -> bool:
    student_number = numeric_answer_text(student_answer, unit)
    correct_number = numeric_answer_text(correct_answer, unit)
    if student_number is not None and correct_number is not None:
        return student_number == correct_number

    s_str = str(student_answer or "").strip()
    c_str = str(correct_answer or "").strip()
    if s_str == c_str:
        return True

    s_tokens = _extract_tokens(student_answer)
    c_tokens = _extract_tokens(correct_answer)

    if s_tokens and c_tokens and len(s_tokens) == len(c_tokens):
        if sorted(s_tokens) == sorted(c_tokens):
            return True

    clean_s = re.sub(r"[\s/,;]", "", s_str)
    clean_c = re.sub(r"[\s/,;]", "", c_str)
    if clean_s == clean_c:
        return True

    if s_tokens and _is_permutation_concatenation(s_tokens, clean_c):
        return True
    if c_tokens and _is_permutation_concatenation(c_tokens, clean_s):
        return True

    if len(clean_s) == len(clean_c) and len(clean_s) >= 4:
        for chunk_size in range(2, len(clean_s) // 2 + 1):
            if len(clean_s) % chunk_size == 0:
                s_chunks = sorted([clean_s[i : i + chunk_size] for i in range(0, len(clean_s), chunk_size)])
                c_chunks = sorted([clean_c[i : i + chunk_size] for i in range(0, len(clean_c), chunk_size)])
                if s_chunks == c_chunks:
                    return True

    return False
