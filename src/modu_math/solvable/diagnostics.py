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

    if correct is True:
        return {"status": "correct", "stage": "review"}
    if correct is False:
        return {"status": "incorrect", "stage": "review"}
    return {"status": "unknown", "stage": "review"}
