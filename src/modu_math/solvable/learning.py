from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Iterable


SKILL_STATES = {"insufficient", "needs_support", "developing", "stable"}


@dataclass(frozen=True)
class StudentAttempt:
    problem_id: str
    skill_ids: list[str]
    submitted_answer: str
    correct: bool
    first_try_correct: bool
    final_correct: bool
    max_hint_level_used: int = 0
    solved_without_hint: bool = False
    retry_count: int = 0
    elapsed_ms: int | None = None
    diagnostic_code: str | None = None
    diagnostic_status: str | None = None
    error_category: str | None = None
    remediation_id: str | None = None
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_record(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class LearningSession:
    student_id: str
    attempts: list[StudentAttempt] = field(default_factory=list)

    def record_attempt(self, attempt: StudentAttempt) -> None:
        self.attempts.append(attempt)

    def skill_states(self) -> dict[str, dict[str, Any]]:
        return compute_skill_states(self.attempts)


def build_attempt(
    *,
    problem_id: str,
    skill_ids: Iterable[str],
    submitted_answer: Any,
    correct: bool,
    first_try_correct: bool | None = None,
    final_correct: bool | None = None,
    max_hint_level_used: int = 0,
    retry_count: int = 0,
    elapsed_ms: int | None = None,
    diagnostic: dict[str, Any] | None = None,
) -> StudentAttempt:
    clean_skill_ids = [str(skill_id) for skill_id in skill_ids if str(skill_id).strip()]
    diagnostic = diagnostic if isinstance(diagnostic, dict) else {}
    return StudentAttempt(
        problem_id=problem_id,
        skill_ids=clean_skill_ids,
        submitted_answer=str(submitted_answer).strip(),
        correct=bool(correct),
        first_try_correct=bool(correct if first_try_correct is None else first_try_correct),
        final_correct=bool(correct if final_correct is None else final_correct),
        max_hint_level_used=max(0, int(max_hint_level_used or 0)),
        solved_without_hint=bool((correct if final_correct is None else final_correct) and max_hint_level_used <= 0 and retry_count <= 0),
        retry_count=max(0, int(retry_count or 0)),
        elapsed_ms=elapsed_ms if isinstance(elapsed_ms, int) and elapsed_ms >= 0 else None,
        diagnostic_code=_string_or_none(diagnostic.get("error_code") or diagnostic.get("diagnostic_code")),
        diagnostic_status=_string_or_none(diagnostic.get("diagnostic_status") or diagnostic.get("status")),
        error_category=_string_or_none(diagnostic.get("error_category")),
        remediation_id=_string_or_none(diagnostic.get("remediation") or diagnostic.get("remediation_id")),
    )


def compute_skill_states(attempts: Iterable[StudentAttempt | dict[str, Any]]) -> dict[str, dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for attempt in attempts:
        record = _attempt_record(attempt)
        for skill_id in record.get("skill_ids") or []:
            grouped.setdefault(str(skill_id), []).append(record)

    states: dict[str, dict[str, Any]] = {}
    for skill_id, records in grouped.items():
        recent = records[-5:]
        confirmed_errors = [
            record
            for record in recent
            if record.get("diagnostic_status") == "confirmed" and record.get("diagnostic_code")
        ]
        repeated_error = _repeated_confirmed_error(confirmed_errors)
        solved_with_hint = any(record.get("final_correct") and int(record.get("max_hint_level_used") or 0) > 0 for record in recent)
        stable_solves = [
            record
            for record in recent
            if record.get("first_try_correct") and record.get("final_correct") and int(record.get("max_hint_level_used") or 0) <= 0
        ]

        if len(recent) < 3:
            state = "insufficient"
        elif repeated_error:
            state = "needs_support"
        elif len(recent) >= 5 and len(stable_solves) >= 4 and not confirmed_errors:
            state = "stable"
        elif solved_with_hint or any(record.get("final_correct") for record in recent):
            state = "developing"
        else:
            state = "needs_support"

        states[skill_id] = {
            "state": state,
            "evidence_count": len(recent),
            "recent_problem_ids": [record.get("problem_id") for record in recent],
            "confirmed_error_count": len(confirmed_errors),
            "repeated_error_code": repeated_error,
            "message": _state_message(state),
        }
    return states


def recommend_next_problems(
    problems: Iterable[dict[str, Any]],
    skill_states: dict[str, dict[str, Any]],
    attempted_problem_ids: Iterable[str] = (),
) -> list[dict[str, Any]]:
    attempted = {str(problem_id) for problem_id in attempted_problem_ids}
    ranked: list[tuple[int, str, dict[str, Any]]] = []
    for problem in problems:
        problem_id = str(problem.get("problem_id") or problem.get("id") or "")
        if not problem_id or problem_id in attempted:
            priority = 4
        else:
            priority = _problem_priority(problem, skill_states)
        reason = _recommendation_reason(problem, skill_states, priority)
        ranked.append((priority, problem_id, {**problem, "recommendation_reason": reason, "priority": priority}))
    ranked.sort(key=lambda item: (item[0], item[1]))
    return [item[2] for item in ranked]


def _problem_priority(problem: dict[str, Any], skill_states: dict[str, dict[str, Any]]) -> int:
    skills = [str(skill) for skill in problem.get("skill_ids") or []]
    states = [skill_states.get(skill, {}).get("state") for skill in skills]
    if any(state == "needs_support" for state in states):
        return 0
    if any(state == "developing" for state in states):
        return 1
    if any(state == "insufficient" for state in states):
        return 3
    return 4 if states else 4


def _recommendation_reason(problem: dict[str, Any], skill_states: dict[str, dict[str, Any]], priority: int) -> str:
    skills = [str(skill) for skill in problem.get("skill_ids") or []]
    repeated = [
        str(skill_states.get(skill, {}).get("repeated_error_code"))
        for skill in skills
        if skill_states.get(skill, {}).get("repeated_error_code")
    ]
    if priority == 0 and repeated:
        return f"{repeated[0]} 오류를 다시 확인하는 문제예요."
    if priority == 1:
        return "힌트가 있으면 해결했던 역량을 스스로 연습해요."
    if priority == 3:
        return "아직 판단할 기록이 부족한 역량을 확인해요."
    return "안정적인 역량을 함께 사용하는 문제예요."


def _attempt_record(attempt: StudentAttempt | dict[str, Any]) -> dict[str, Any]:
    if isinstance(attempt, StudentAttempt):
        return attempt.to_record()
    return dict(attempt)


def _repeated_confirmed_error(records: list[dict[str, Any]]) -> str | None:
    counts: dict[str, int] = {}
    for record in records:
        code = str(record.get("diagnostic_code") or "")
        if not code:
            continue
        counts[code] = counts.get(code, 0) + 1
        if counts[code] >= 2:
            return code
    return None


def _state_message(state: str) -> str:
    return {
        "stable": "혼자서 잘 해결해요",
        "developing": "연습하며 성장 중이에요",
        "needs_support": "조금 더 확인이 필요해요",
        "insufficient": "아직 판단할 기록이 부족해요",
    }.get(state, "아직 판단할 기록이 부족해요")


def _string_or_none(value: Any) -> str | None:
    if isinstance(value, str) and value.strip():
        return value.strip()
    return None
