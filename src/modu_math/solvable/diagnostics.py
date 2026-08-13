from __future__ import annotations

from typing import Any


ERROR_CATALOG: dict[str, dict[str, str]] = {
    "understand.target": {
        "stage": "understand",
        "feedback": "문제에서 무엇을 구해야 하는지 다시 확인해 보세요.",
        "remediation": "identify_target",
        "skill_id": "understand.target",
        "category": "understand",
        "confirmation_question": "문제에서 구해야 하는 것은 한 부분인가요, 전체인가요?",
    },
    "plan.add_operands": {
        "stage": "plan",
        "feedback": "같은 묶음이 몇 번 있는지 먼저 확인해 보세요.",
        "remediation": "repeated_addition",
        "skill_id": "plan.add_parts",
        "category": "plan",
        "confirmation_question": "같은 수를 여러 번 더해야 하는지 먼저 확인해 볼까요?",
    },
    "plan.add_parts": {
        "stage": "plan",
        "feedback": "두 부분을 모두 더해야 하는지 다시 확인해 보세요.",
        "remediation": "add_parts",
        "skill_id": "plan.add_parts",
        "category": "plan",
        "confirmation_question": "문제에서 두 부분을 합쳐 전체를 구하라고 했나요?",
    },
    "plan.copy_one_part": {
        "stage": "plan",
        "feedback": "한쪽 수만 답으로 쓰지 말고 전체를 구해야 하는지 확인해 보세요.",
        "remediation": "identify_target",
        "skill_id": "plan.copy_one_part",
        "category": "plan",
        "confirmation_question": "문제에서 한 부분만 묻는지, 전체를 묻는지 다시 골라 볼까요?",
    },
    "execute.add_fact": {
        "stage": "execute",
        "feedback": "한 자리 덧셈을 다시 확인해 보세요.",
        "remediation": "basic_addition",
        "skill_id": "execute.add_fact",
        "category": "execute",
        "confirmation_question": "한 자리 덧셈부터 다시 확인해 볼까요?",
    },
    "execute.add_carry": {
        "stage": "execute",
        "feedback": "받아올림을 다시 확인해요. 일의 자리부터 더하고 10이 넘으면 다음 자리로 1을 올려요.",
        "remediation": "addition_with_carry",
        "skill_id": "execute.add_carry",
        "category": "execute",
        "confirmation_question": "일의 자리에서 10이 넘을 때 무엇을 다음 자리로 올려야 할까요?",
    },
    "execute.place_value_compose": {
        "stage": "execute",
        "feedback": "받아올림이나 중간 계산을 그대로 이어 쓰면 안 돼요. 각 자리 숫자로 다시 모아 보세요.",
        "remediation": "place_value_compose",
        "skill_id": "execute.place_value_compose",
        "category": "execute",
        "confirmation_question": "각 자리에서 나온 수를 자리값에 맞게 모아 볼까요?",
    },
    "execute.mul_fact": {
        "stage": "execute",
        "feedback": "곱셈 계산을 다시 확인해 보세요.",
        "remediation": "basic_multiplication",
        "skill_id": "execute.mul_fact",
        "category": "execute",
        "confirmation_question": "곱셈 계산 한 가지를 다시 확인해 볼까요?",
    },
    "review.inverse_check": {
        "stage": "review",
        "feedback": "답이 문제 조건과 맞는지 다시 확인해 보세요.",
        "remediation": "inverse_check",
        "skill_id": "review.inverse_check",
        "category": "review",
        "confirmation_question": "구한 답을 문제 조건에 다시 넣어 확인해 볼까요?",
    },
}


def diagnose_student_response(
    solvable: dict[str, Any],
    student_response: Any,
    *,
    correct: bool | None = None,
    confirm: bool = False,
) -> dict[str, Any]:
    """Return a v1.3 diagnostic candidate unless explicit confirmation is requested."""

    response_key = str(student_response).strip()
    diagnostics = solvable.get("diagnostics")
    errors = diagnostics.get("errors") if isinstance(diagnostics, dict) else None
    error_code = errors.get(response_key) if isinstance(errors, dict) else None
    catalog_entry = ERROR_CATALOG.get(error_code) if isinstance(error_code, str) else None

    if catalog_entry:
        return _diagnostic_result(error_code, catalog_entry, confirmed=confirm)

    heuristic = _infer_arithmetic_error(solvable, response_key)
    if heuristic:
        if confirm:
            heuristic["status"] = "confirmed"
            heuristic["diagnostic_status"] = "confirmed"
        return heuristic

    if correct is True:
        return {"status": "correct", "diagnostic_status": "none", "stage": "review"}
    if correct is False:
        return {"status": "incorrect", "diagnostic_status": "none", "stage": "review"}
    return {"status": "unknown", "diagnostic_status": "none", "stage": "review"}


def confirm_diagnostic_response(
    solvable: dict[str, Any],
    error_code: str,
    student_response: Any,
) -> dict[str, Any]:
    """Confirm or reject a previously suspected diagnostic from the next student answer."""

    catalog_entry = ERROR_CATALOG.get(error_code)
    if not catalog_entry:
        return {"status": "unknown", "diagnostic_status": "candidate", "stage": "review"}

    text = str(student_response).strip()
    if _looks_negative(text):
        return {
            **_diagnostic_result(error_code, catalog_entry, confirmed=False),
            "status": "rejected",
            "diagnostic_status": "candidate",
        }
    if _looks_positive(text) or text:
        return _diagnostic_result(error_code, catalog_entry, confirmed=True)
    return _diagnostic_result(error_code, catalog_entry, confirmed=False)


def _diagnostic_result(error_code: str, catalog_entry: dict[str, str], *, confirmed: bool) -> dict[str, Any]:
    diagnostic_status = "confirmed" if confirmed else "candidate"
    return {
        "status": diagnostic_status,
        "diagnostic_status": diagnostic_status,
        "error_code": error_code,
        "stage": catalog_entry["stage"],
        "skill_id": catalog_entry.get("skill_id") or error_code,
        "error_category": catalog_entry.get("category") or catalog_entry["stage"],
        "feedback": catalog_entry["feedback"],
        "confirmation_question": catalog_entry.get("confirmation_question") or catalog_entry["feedback"],
        "remediation": catalog_entry["remediation"],
    }


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
        return _diagnostic_result(
            "execute.place_value_compose",
            ERROR_CATALOG["execute.place_value_compose"],
            confirmed=False,
        )

    if _has_column_carry(terms):
        return _diagnostic_result("execute.add_carry", ERROR_CATALOG["execute.add_carry"], confirmed=False)

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


def _looks_positive(text: str) -> bool:
    normalized = text.strip().lower()
    return normalized in {"y", "yes", "ok", "okay", "맞아", "맞아요", "네", "응", "예", "그래"}


def _looks_negative(text: str) -> bool:
    normalized = text.strip().lower()
    return normalized in {"n", "no", "아니", "아니요", "아냐", "틀려", "몰라"}
