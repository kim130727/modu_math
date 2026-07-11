from __future__ import annotations

from modu_math_web.editor.services.tutor_preview import _system_prompt, rule_tutor_response


def test_tutor_prompt_explains_inscribed_hexagon_radius_relation() -> None:
    payload = {
        "solvable": {
            "problem_type": "numeric_answer_perimeter_difference",
            "method": "compare_circle_and_inscribed_hexagon_perimeters",
            "given": [
                {"ref": "rel.hexagon_inscribed", "value": True},
                {"ref": "rel.hexagon_side_equals_radius", "value": True},
            ],
            "target": {"ref": "answer.target", "type": "perimeter_difference"},
        }
    }

    prompt = _system_prompt(payload)

    assert "inscribed regular hexagon" in prompt
    assert "equilateral triangle" in prompt
    assert "never skip the geometric reason" in prompt


def test_rule_tutor_uses_student_result_and_step_explanation() -> None:
    payload = {
        "solvable": {
            "schema": "modu.solvable.v1.1",
            "problem_type": "numeric_answer_perimeter_difference",
            "method": "compare_circle_and_inscribed_hexagon_perimeters",
            "given": [
                {"ref": "rel.hexagon_inscribed", "value": True},
                {"ref": "rel.hexagon_side_equals_radius", "value": True},
            ],
            "target": {"ref": "answer.target", "type": "perimeter_difference"},
            "steps": [
                {"id": "step.1", "expr": "30 ÷ 2", "value": {"result": 15, "meaning": "원의 반지름", "unit": "cm"}},
                {
                    "id": "step.2",
                    "expr": "정육각형의 한 변 = 원의 반지름",
                    "value": {"result": 15, "unit": "cm"},
                    "explanation": "중심과 이웃한 두 꼭짓점을 이으면 정삼각형이 됩니다.",
                },
            ],
            "answer": {"value": 4.2, "unit": "cm"},
        }
    }

    first = rule_tutor_response(payload, "시작", [])
    assert "compare circle" not in first["reply"]
    assert first["choices"] == ["1", "15", "150", "25"]

    second = rule_tutor_response(
        payload,
        "15",
        [
            {"role": "assistant", "content": first["reply"]},
            {"role": "user", "content": "15"},
        ],
    )
    assert "정삼각형" in second["reply"]
    assert second["choices"] == ["1", "15", "150", "25"]
