from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class NormalizedSolvable:
    schema: str
    problem_id: str
    given: list[dict[str, Any]]
    target: dict[str, Any]
    method: str
    steps: list[dict[str, Any]]
    answer: dict[str, Any]
    plan: list[str]
    checks: list[Any]
    diagnostics: dict[str, Any] | None


def normalize_solvable(solvable: dict[str, Any]) -> NormalizedSolvable:
    given = [_normalize_ref_item(item) for item in _list_of_dicts(solvable.get("given"))]
    target = _normalize_ref_item(solvable.get("target") if isinstance(solvable.get("target"), dict) else {})
    steps = _list_of_dicts(solvable.get("steps"))
    plan = [str(item) for item in solvable.get("plan", [])] if isinstance(solvable.get("plan"), list) else []
    checks = solvable.get("checks") if isinstance(solvable.get("checks"), list) else []
    diagnostics = solvable.get("diagnostics") if isinstance(solvable.get("diagnostics"), dict) else None
    answer = solvable.get("answer") if isinstance(solvable.get("answer"), dict) else {}

    return NormalizedSolvable(
        schema=str(solvable.get("schema") or ""),
        problem_id=str(solvable.get("problem_id") or ""),
        given=given,
        target=target,
        method=str(solvable.get("method") or ""),
        steps=steps,
        answer=answer,
        plan=plan,
        checks=checks,
        diagnostics=diagnostics,
    )


def _normalize_ref_item(item: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(item)
    if "ref" not in normalized and isinstance(normalized.get("id"), str):
        normalized["ref"] = normalized["id"]
    if "id" not in normalized and isinstance(normalized.get("ref"), str):
        normalized["id"] = normalized["ref"]
    return normalized


def _list_of_dicts(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [dict(item) for item in value if isinstance(item, dict)]
