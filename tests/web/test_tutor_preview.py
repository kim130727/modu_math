from __future__ import annotations

from modu_math_web.editor.services.tutor_preview import _speech_instructions, _speech_voice, _system_prompt, rule_tutor_response, tutor_speech_locale


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


def test_tutor_prompt_uses_problem_language_metadata() -> None:
    payload = {"semantic": {"metadata": {"language": "ja"}}}

    prompt = _system_prompt(payload)

    assert "Japanese tutor" in prompt
    assert "Always speak with the student in Japanese" in prompt


def test_rule_tutor_uses_problem_language_for_default_reply() -> None:
    payload = {
        "semantic": {"metadata": {"language": "en"}},
        "solvable": {
            "schema": "modu.solvable.v1.1",
            "problem_type": "numeric_answer",
            "method": "one_step",
            "steps": [{"id": "step.1", "expr": "2 + 3", "value": {"result": 5}}],
            "answer": {"value": 5},
        },
    }

    first = rule_tutor_response(payload, "start", [])

    assert "Step 1:" in first["reply"]
    assert "단계" not in first["reply"]


def test_tutor_speech_uses_local_accent_instructions() -> None:
    assert tutor_speech_locale({"semantic": {"metadata": {"language": "km"}}}) == "km-KH"
    assert tutor_speech_locale({"semantic": {"metadata": {"language": "my"}}}) == "my-MM"

    assert _speech_voice("km-KH") == "coral"
    assert "Khmer" in _speech_instructions("km-KH")
    assert "Cambodian accent" in _speech_instructions("km-KH")

    assert _speech_voice("my-MM") == "fable"
    assert "Burmese" in _speech_instructions("my-MM")
    assert "Myanmar accent" in _speech_instructions("my-MM")


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
                {
                    "id": "step.1",
                    "expr": "30 ÷ 2",
                    "value": {"result": 15, "meaning": "원의 반지름", "unit": "cm"},
                    "explanation": "지름을 2로 나누면 반지름입니다.",
                },
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
    assert "지름을 2로 나누면 반지름" in second["reply"]
    assert "정삼각형" not in second["reply"]
    assert second["choices"] == ["1", "15", "150", "25"]


def test_rule_tutor_v1_2_uses_understanding_and_plain_numeric_choices() -> None:
    payload = {
        "semantic": {"metadata": {"language": "ko"}},
        "solvable": {
            "schema": "modu.solvable.v1.2",
            "problem_type": "numeric_answer_circle_circumference",
            "method": "derive_radii_then_sum_circumferences",
            "understanding": {
                "summary": "세 원의 원주의 합을 구하는 문제",
                "facts": [
                    {"ref": "measure.middle_right", "label": "가운데와 오른쪽 중심 사이 거리", "value": 18, "unit": "cm"}
                ],
                "unknowns": [
                    {"ref": "answer.target", "label": "세 원의 원주의 합", "unit": "cm"}
                ],
                "relation": {
                    "type": "tangent_circles_center_distance",
                    "statement": "맞닿은 두 원의 중심 사이 거리는 두 반지름의 합입니다.",
                },
                "diagnostic_questions": [
                    {
                        "id": "understand.target",
                        "type": "multiple_choice",
                        "prompt": "이 문제에서 구해야 하는 것은 무엇인가요?",
                        "choices": ["오른쪽 원의 반지름", "세 원의 원주의 합"],
                        "answer_index": 1,
                    },
                    {
                        "id": "understand.relation",
                        "type": "multiple_choice",
                        "prompt": "맞닿은 두 원의 중심 사이 거리는 무엇과 같나요?",
                        "choices": ["두 반지름의 합", "두 반지름의 차"],
                        "answer_index": 0,
                    },
                ],
            },
            "steps": [
                {
                    "id": "step.1",
                    "goal": "가운데 원의 반지름을 구합니다.",
                    "expr": "r_middle = 18 - 10",
                    "value": {"radius": 8, "unit": "cm", "ref": "derived.radius_middle"},
                    "explanation": "18cm에서 오른쪽 원의 반지름 10cm를 뺍니다.",
                },
                {
                    "id": "step.2",
                    "goal": "왼쪽 원의 반지름을 구합니다.",
                    "expr": "r_left = 14 - 8",
                    "value": {"radius": 6, "unit": "cm", "ref": "derived.radius_left"},
                    "explanation": "14cm에서 가운데 원의 반지름 8cm를 뺍니다.",
                },
            ],
            "answer": {"value": 144, "unit": "cm"},
        },
    }

    first = rule_tutor_response(payload, "시작", [])

    assert "derive radii" not in first["reply"]
    assert "확인 1: 이 문제에서 구해야 하는 것은 무엇인가요?" in first["reply"]
    assert "세 원의 원주의 합" in first["choices"]
    assert "{\"radius\"" not in first["choices"]

    second = rule_tutor_response(
        payload,
        "세 원의 원주의 합",
        [
            {"role": "assistant", "content": first["reply"]},
            {"role": "user", "content": "세 원의 원주의 합"},
        ],
    )
    assert "좋아요" in second["reply"]
    assert "확인 2: 맞닿은 두 원의 중심 사이 거리는 무엇과 같나요?" in second["reply"]
    assert second["choices"] == ["두 반지름의 합", "두 반지름의 차"]

    retry = rule_tutor_response(
        payload,
        "오른쪽 원의 반지름",
        [
            {"role": "assistant", "content": first["reply"]},
            {"role": "user", "content": "오른쪽 원의 반지름"},
        ],
    )
    assert "조금 다르게 본 것 같아요." in retry["reply"]
    assert "확인 1: 이 문제에서 구해야 하는 것은 무엇인가요?" in retry["reply"]
    assert "알맞은 것을 골라볼까요?" in retry["reply"]
    assert "이 단계에서 생각한 값을 입력해 주세요" not in retry["reply"]
    assert retry["choices"] == ["오른쪽 원의 반지름", "세 원의 원주의 합"]
