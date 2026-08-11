from __future__ import annotations

from typing import Any


ERROR_CATALOG: dict[str, dict[str, str]] = {
    "plan.add_operands": {
        "stage": "plan",
        "feedback": "두 수를 바로 더하지 말고 같은 수가 몇 묶음인지 생각해 보세요.",
        "remediation": "repeated_addition",
    },
    "execute.mul_fact": {
        "stage": "execute",
        "feedback": "곱셈 계산을 다시 확인해 보세요.",
        "remediation": "basic_multiplication",
    },
    "plan.copy_one_part": {
        "stage": "plan",
        "feedback": "한쪽 수만 답으로 쓰지 말고 전체를 구해야 하는지 확인해 보세요.",
        "remediation": "identify_target",
    },
    "execute.add_fact": {
        "stage": "execute",
        "feedback": "덧셈 계산을 다시 확인해 보세요.",
        "remediation": "basic_addition",
    },
    "execute.add_carry": {
        "stage": "execute",
        "feedback": "받아올림을 다시 확인해요. 일의 자리부터 더하고, 10이 넘으면 다음 자리로 1을 올려요.",
        "remediation": "addition_with_carry",
    },
    "execute.place_value_compose": {
        "stage": "execute",
        "feedback": "받아올림한 수나 중간 계산을 그대로 이어 쓰면 안 돼요. 각 자리 숫자로 다시 모아 보세요.",
        "remediation": "place_value_compose",
    },
}


def diagnose_student_response(
    solvable: dict[str, Any],
    student_response: Any,
    *,
    correct: bool | None = None,
) -> dict[str, Any]:
    """Return v1.3 diagnostic feedback or fall back to normal correctness."""

    response_key = str(student_response).strip()
    diagnostics = solvable.get("diagnostics")
    errors = diagnostics.get("errors") if isinstance(diagnostics, dict) else None
    error_code = errors.get(response_key) if isinstance(errors, dict) else None
    catalog_entry = ERROR_CATALOG.get(error_code) if isinstance(error_code, str) else None

    if catalog_entry:
        return {
            "status": "diagnosed",
            "error_code": error_code,
            "stage": catalog_entry["stage"],
            "feedback": catalog_entry["feedback"],
            "remediation": catalog_entry["remediation"],
        }

    heuristic = _infer_arithmetic_error(solvable, response_key)
    if heuristic:
        return heuristic

    if correct is True:
        return {"status": "correct", "stage": "review"}
    if correct is False:
        return {"status": "incorrect", "stage": "review"}
    return {"status": "unknown", "stage": "review"}


def _infer_arithmetic_error(solvable: dict[str, Any], response_key: str) -> dict[str, Any] | None:
    if not response_key or not response_key.lstrip("-").isdigit():
        return None

    expected = _expected_integer(solvable)
    if expected is None:
        return None

    expression = _answer_expression(solvable, expected)
    if not expression:
        return None

    terms = _addition_terms(expression)
    if len(terms) < 2 or sum(terms) != expected:
        return None

    normalized = response_key.lstrip("0") or "0"
    if normalized == str(expected):
        return None

    if _has_column_carry(terms) and len(normalized) > len(str(abs(expected))):
        return {
            "status": "diagnosed",
            "error_code": "execute.place_value_compose",
            "stage": "execute",
            "feedback": (
                "받아올림한 수나 중간 계산을 그대로 이어 쓰면 안 돼요. "
                "일의 자리부터 계산해 각 자리 숫자로 다시 모아 보세요."
            ),
            "remediation": "place_value_compose",
        }

    if _has_column_carry(terms):
        return {
            "status": "diagnosed",
            "error_code": "execute.add_carry",
            "stage": "execute",
            "feedback": "받아올림을 다시 확인해요. 일의 자리부터 더하고, 10이 넘으면 다음 자리로 1을 올려요.",
            "remediation": "addition_with_carry",
        }

    return None


def _expected_integer(solvable: dict[str, Any]) -> int | None:
    answer = solvable.get("answer")
    if isinstance(answer, dict):
        value = answer.get("value")
        parsed = _parse_int(value)
        if parsed is not None:
            return parsed
    for step in _raw_steps(solvable):
        if not isinstance(step, dict):
            continue
        for key in ("value", "expected"):
            parsed = _parse_int(_student_expected_value(step.get(key)))
            if parsed is not None:
                return parsed
    return None


def _answer_expression(solvable: dict[str, Any], expected: int) -> str | None:
    for step in _raw_steps(solvable):
        if not isinstance(step, dict):
            continue
        expr = step.get("expr")
        if not isinstance(expr, str) or not expr.strip():
            continue
        terms = _addition_terms(expr)
        if len(terms) >= 2 and sum(terms) == expected:
            return expr
    return None


def _raw_steps(solvable: dict[str, Any]) -> list[Any]:
    steps = solvable.get("steps")
    if isinstance(steps, list):
        return steps
    plan = solvable.get("plan")
    if isinstance(plan, list):
        return plan
    return []


def _student_expected_value(value: Any) -> Any:
    if isinstance(value, dict):
        for key in ("result", "value", "answer", "count"):
            if key in value:
                return value[key]
    return value


def _parse_int(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float) and value.is_integer():
        return int(value)
    if isinstance(value, str) and value.strip().lstrip("-").isdigit():
        return int(value.strip())
    return None


def _addition_terms(expression: str) -> list[int]:
    import re

    if not re.fullmatch(r"\s*\d+\s*(?:\+\s*\d+\s*)+", expression):
        return []
    return [int(token) for token in re.findall(r"\d+", expression)]


def _has_column_carry(terms: list[int]) -> bool:
    carry = 0
    max_digits = max(len(str(abs(term))) for term in terms)
    for place in range(max_digits):
        column_sum = carry + sum((abs(term) // (10**place)) % 10 for term in terms)
        if column_sum >= 10:
            return True
        carry = column_sum // 10
    return carry > 0
