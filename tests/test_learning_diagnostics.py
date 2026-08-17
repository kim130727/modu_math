from __future__ import annotations

from modu_math.solvable import (
    build_attempt,
    compute_skill_states,
    confirm_diagnostic_response,
    diagnose_student_response,
    recommend_next_problems,
)
from modu_math_web.editor.services.tutor_preview import rule_tutor_response


def test_registered_error_is_candidate_before_confirmation() -> None:
    solvable = {
        "schema": "modu.solvable.v1.3",
        "problem_id": "p_add",
        "steps": [{"expr": "259 + 248", "value": 507}],
        "answer": {"value": 507, "unit": ""},
        "diagnostics": {"errors": {"259": "plan.copy_one_part"}},
    }

    diagnostic = diagnose_student_response(solvable, "259", correct=False)
    confirmed = confirm_diagnostic_response(solvable, diagnostic["error_code"], "네")

    assert diagnostic["diagnostic_status"] == "candidate"
    assert diagnostic["skill_id"] == "plan.copy_one_part"
    assert confirmed["diagnostic_status"] == "confirmed"


def test_arithmetic_diagnostic_reads_numeric_response_with_unit() -> None:
    solvable = {
        "schema": "modu.solvable.v1.3",
        "problem_id": "p_add",
        "steps": [{"expr": "259 + 248", "value": 507}],
        "answer": {"value": 507, "unit": "개"},
    }

    diagnostic = diagnose_student_response(solvable, "1507개", correct=False)

    assert diagnostic["diagnostic_status"] == "candidate"
    assert diagnostic["skill_id"] == "execute.place_value_compose"


def test_rule_tutor_asks_confirmation_before_feedback() -> None:
    solvable = {
        "schema": "modu.solvable.v1.3",
        "problem_id": "P3_1_01_00040_00469",
        "problem_type": "numeric_answer_addition_word_problem",
        "method": "add_parts",
        "steps": [
            {
                "id": "step.add_counts",
                "goal": "전체 수 구하기",
                "expr": "259 + 248",
                "value": 507,
            }
        ],
        "answer": {"value": 507, "unit": ""},
        "diagnostics": {
            "skills": ["plan.add_parts"],
            "errors": {"259": "plan.copy_one_part"},
        },
    }
    payload = {"semantic": {"metadata": {"language": "ko"}}, "solvable": solvable}
    first = rule_tutor_response(payload, "start", [])

    candidate = rule_tutor_response(
        payload, "259", [{"role": "assistant", "content": first["reply"]}]
    )
    confirmed = rule_tutor_response(
        payload,
        "네",
        [
            {"role": "assistant", "content": first["reply"]},
            {"role": "user", "content": "259"},
            {"role": "assistant", "content": candidate["reply"]},
        ],
    )

    assert candidate["diagnostic"]["diagnostic_status"] == "candidate"
    assert "전체" in candidate["reply"]
    assert confirmed["diagnostic"]["diagnostic_status"] == "confirmed"
    assert confirmed["attempt"]["diagnostic_code"] == "plan.copy_one_part"


def test_skill_state_uses_recent_five_attempts_and_repeated_confirmed_errors() -> None:
    attempts = [
        build_attempt(
            problem_id=f"p{i}",
            skill_ids=["execute.add_carry"],
            submitted_answer="wrong",
            correct=False,
            diagnostic={
                "error_code": "execute.add_carry",
                "diagnostic_status": "confirmed",
                "error_category": "execute",
            },
        )
        for i in range(2)
    ]
    attempts.append(
        build_attempt(
            problem_id="p2",
            skill_ids=["execute.add_carry"],
            submitted_answer="507",
            correct=True,
        )
    )

    states = compute_skill_states(attempts)

    assert states["execute.add_carry"]["state"] == "needs_support"
    assert states["execute.add_carry"]["repeated_error_code"] == "execute.add_carry"


def test_skill_state_marks_stable_after_four_of_five_without_hints() -> None:
    attempts = [
        build_attempt(
            problem_id=f"p{i}",
            skill_ids=["plan.add_parts"],
            submitted_answer="ok",
            correct=i != 0,
        )
        for i in range(5)
    ]

    states = compute_skill_states(attempts)

    assert states["plan.add_parts"]["state"] == "stable"


def test_recommendations_prioritize_repeated_error_skills() -> None:
    states = {
        "execute.add_carry": {
            "state": "needs_support",
            "repeated_error_code": "execute.add_carry",
        },
        "plan.add_parts": {"state": "stable"},
    }
    problems = [
        {"problem_id": "stable", "skill_ids": ["plan.add_parts"]},
        {"problem_id": "support", "skill_ids": ["execute.add_carry"]},
    ]

    recommended = recommend_next_problems(problems, states)

    assert recommended[0]["problem_id"] == "support"
    assert "execute.add_carry" in recommended[0]["recommendation_reason"]
