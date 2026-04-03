from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable


@dataclass(slots=True)
class ValidationIssue:
    level: str
    code: str
    message: str


LogicRule = Callable[[dict[str, Any]], list[ValidationIssue]]


class LogicValidator:
    def __init__(self, rules: dict[str, LogicRule] | None = None) -> None:
        self.rules = rules or {}

    def validate(self, semantic: dict[str, Any]) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        problem_type = semantic.get("problem_type")
        if not isinstance(problem_type, str):
            return [ValidationIssue("error", "logic.problem_type", "problem_type must be string")]

        issues.extend(_validate_blank_general(semantic))
        issues.extend(_validate_choices_general(semantic))

        rule = self.rules.get(problem_type)
        if rule is not None:
            issues.extend(rule(semantic))
        return issues


def _validate_blank_general(semantic: dict[str, Any]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    answer = semantic.get("answer", {})
    blanks = answer.get("blanks", []) if isinstance(answer, dict) else []
    elements = semantic.get("render", {}).get("elements", [])
    blank_ids = {b.get("id") for b in blanks if isinstance(b, dict)}

    if not blank_ids:
        return issues

    element_ids = {e.get("id") for e in elements if isinstance(e, dict)}
    for blank_id in blank_ids:
        if blank_id not in element_ids:
            issues.append(ValidationIssue("error", "logic.blank_missing_element", f"blank id not found: {blank_id}"))
    return issues


def _validate_choices_general(semantic: dict[str, Any]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    answer = semantic.get("answer", {})
    choices = answer.get("choices", []) if isinstance(answer, dict) else []
    if not choices:
        return issues

    correct = [c for c in choices if isinstance(c, dict) and c.get("is_correct") is True]
    if len(correct) != 1:
        issues.append(ValidationIssue("error", "logic.choice_correct_count", f"exactly one correct choice required, got {len(correct)}"))

    key_items = answer.get("answer_key", []) if isinstance(answer, dict) else []
    if key_items:
        key_value = str(key_items[0].get("value"))
        if correct and str(correct[0].get("value")) != key_value:
            issues.append(ValidationIssue("error", "logic.choice_answer_key_mismatch", "correct choice value does not match answer_key"))

    return issues


def default_logic_rules() -> dict[str, LogicRule]:
    def _time_conversion(semantic: dict[str, Any]) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        d = semantic.get("domain", {})
        if not isinstance(d, dict):
            return issues
        left_seconds = d.get("left_seconds")
        minutes = d.get("minutes")
        if isinstance(left_seconds, (int, float)) and isinstance(minutes, (int, float)):
            expected = left_seconds - minutes * 60
            key = semantic.get("answer", {}).get("answer_key", [])
            if key and str(key[0].get("value")) != str(expected):
                issues.append(ValidationIssue("error", "logic.time_conversion", f"expected {expected}, got {key[0].get('value')}"))
        return issues

    def _ruler(semantic: dict[str, Any]) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        d = semantic.get("domain", {})
        m = d.get("measurement", {}) if isinstance(d, dict) else {}
        left_cm = m.get("left_cm") if isinstance(m, dict) else None
        right_cm = m.get("right_cm") if isinstance(m, dict) else None
        if isinstance(left_cm, (int, float)) and isinstance(right_cm, (int, float)):
            expected_mm = round((right_cm - left_cm) * 10)
            key = semantic.get("answer", {}).get("answer_key", [])
            if key and str(key[0].get("value")) != str(expected_mm):
                issues.append(ValidationIssue("error", "logic.ruler", f"expected {expected_mm}, got {key[0].get('value')}"))
        return issues

    def _base_ten_add(semantic: dict[str, Any]) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        d = semantic.get("domain", {})
        if not isinstance(d, dict):
            return issues
        addends = d.get("addends", [])
        if isinstance(addends, list) and len(addends) == 2 and all(isinstance(v, (int, float)) for v in addends):
            expected = int(addends[0]) + int(addends[1])
            key = semantic.get("answer", {}).get("answer_key", [])
            if key and str(key[0].get("value")) != str(expected):
                issues.append(ValidationIssue("error", "logic.base_ten_add", f"expected {expected}, got {key[0].get('value')}"))
        return issues

    return {
        "time_conversion_fill_blank": _time_conversion,
        "measure_length_with_ruler": _ruler,
        "base_ten_block_addition": _base_ten_add,
    }
