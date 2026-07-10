from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class TutorValidation:
    level: str
    message: str


def tutor_env_status() -> dict[str, Any]:
    return {
        "openai_configured": bool(os.getenv("OPENAI_API_KEY")),
        "model": os.getenv("OPENAI_MODEL") or "gpt-5.4-mini",
    }


def validate_tutor_payload(payload: dict[str, Any]) -> list[TutorValidation]:
    checks: list[TutorValidation] = []
    semantic = _record_or_none(payload.get("semantic"))
    solvable = _record_or_none(payload.get("solvable"))

    if semantic:
        checks.append(TutorValidation("ok", "semantic JSON is available."))
    else:
        checks.append(TutorValidation("warn", "semantic JSON is missing."))

    if solvable:
        checks.append(TutorValidation("ok", "solvable JSON is available."))
    else:
        checks.append(TutorValidation("warn", "solvable JSON is missing."))

    question = _extract_question(semantic)
    if question:
        checks.append(TutorValidation("ok", "question text was found."))
    else:
        checks.append(TutorValidation("warn", "question text could not be found."))

    answer = _extract_answer(semantic, solvable)
    if answer:
        checks.append(TutorValidation("ok", "answer data was found."))
    else:
        checks.append(TutorValidation("warn", "answer data could not be found."))

    steps = _extract_steps(solvable)
    if steps:
        checks.append(TutorValidation("ok", f"{len(steps)} solvable step(s) found."))
    else:
        checks.append(TutorValidation("warn", "solvable steps are missing."))

    return checks


def mock_tutor_response(payload: dict[str, Any], message: str) -> str:
    semantic = _record_or_none(payload.get("semantic"))
    solvable = _record_or_none(payload.get("solvable"))
    answer = _extract_answer(semantic, solvable) or "정답 정보 없음"
    first_step = (_extract_steps(solvable) or ["문제의 조건을 먼저 정리해 봅시다."])[0]
    clean_message = message.strip()
    if not clean_message:
        return "안녕하세요. 이 문제를 함께 풀어볼게요. 먼저 어떤 점이 헷갈리는지 말해 주세요."
    return f"좋아요. 지금 말한 내용은 '{clean_message}'로 이해했어요. 첫 단계는 {first_step} 정답 검사용 값은 {answer}입니다."


def openai_tutor_response(payload: dict[str, Any], message: str, history: list[dict[str, str]]) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY is not set. Add it to .env.")
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise ImportError("openai package is required. Install with: pip install openai") from exc

    model = os.getenv("OPENAI_MODEL") or "gpt-5.4-mini"
    client = OpenAI(api_key=api_key)
    response = client.responses.create(
        model=model,
        input=[
            {"role": "system", "content": [{"type": "input_text", "text": _system_prompt()}]},
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": _preview_context(payload, history, message),
                    }
                ],
            },
        ],
    )
    output_text = getattr(response, "output_text", None)
    if isinstance(output_text, str) and output_text.strip():
        return output_text.strip()
    output = getattr(response, "output", None)
    chunks: list[str] = []
    if isinstance(output, list):
        for item in output:
            content = getattr(item, "content", None)
            if not isinstance(content, list):
                continue
            for part in content:
                if getattr(part, "type", None) == "output_text":
                    text = getattr(part, "text", None)
                    if isinstance(text, str):
                        chunks.append(text)
    merged = "\n".join(chunks).strip()
    if merged:
        return merged
    raise ValueError("Could not extract text output from OpenAI response.")


def _system_prompt() -> str:
    return (
        "You are a Korean elementary math tutor embedded in an authoring preview. "
        "Help the student reason step by step without revealing the final answer immediately. "
        "Use short Korean replies. If the student is correct, acknowledge it and ask for the reasoning. "
        "If the problem data is incomplete, explain what authoring field is missing."
    )


def _preview_context(payload: dict[str, Any], history: list[dict[str, str]], message: str) -> str:
    compact_payload = {
        "problem_id": payload.get("problem_id"),
        "semantic": payload.get("semantic"),
        "solvable": payload.get("solvable"),
        "layout_summary": _layout_summary(_record_or_none(payload.get("layout"))),
    }
    return "\n".join(
        [
            "Authoring preview payload:",
            json.dumps(compact_payload, ensure_ascii=False, indent=2),
            "",
            "Recent chat:",
            json.dumps(history[-8:], ensure_ascii=False, indent=2),
            "",
            f"Student message: {message.strip()}",
        ]
    )


def _layout_summary(layout: dict[str, Any] | None) -> dict[str, Any] | None:
    if not layout:
        return None
    slots = layout.get("slots")
    return {
        "canvas": layout.get("canvas"),
        "slot_count": len(slots) if isinstance(slots, list) else 0,
    }


def _record_or_none(value: Any) -> dict[str, Any] | None:
    return value if isinstance(value, dict) else None


def _extract_question(semantic: dict[str, Any] | None) -> str | None:
    if not semantic:
        return None
    candidates = [
        semantic.get("question"),
        semantic.get("prompt"),
        _nested_get(semantic, ["metadata", "question"]),
        _nested_get(semantic, ["problem", "question"]),
    ]
    for candidate in candidates:
        if isinstance(candidate, str) and candidate.strip():
            return candidate.strip()
    return None


def _extract_answer(semantic: dict[str, Any] | None, solvable: dict[str, Any] | None) -> str | None:
    for source in (solvable, semantic):
        if not source:
            continue
        for key in ("answer", "correctAnswer", "correct_answer"):
            if key in source:
                return _stringify_answer(source[key])
    return None


def _extract_steps(solvable: dict[str, Any] | None) -> list[str]:
    if not solvable:
        return []
    raw_steps = solvable.get("steps") or solvable.get("solution_steps")
    if not isinstance(raw_steps, list):
        return []
    steps: list[str] = []
    for step in raw_steps:
        if isinstance(step, str) and step.strip():
            steps.append(step.strip())
        elif isinstance(step, dict):
            text = step.get("text") or step.get("explanation") or step.get("description")
            if isinstance(text, str) and text.strip():
                steps.append(text.strip())
    return steps


def _nested_get(value: dict[str, Any], path: list[str]) -> Any:
    current: Any = value
    for key in path:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


def _stringify_answer(value: Any) -> str:
    if isinstance(value, str):
        return value.strip()
    return json.dumps(value, ensure_ascii=False)
