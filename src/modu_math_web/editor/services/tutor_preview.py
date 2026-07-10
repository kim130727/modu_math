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
        "model": os.getenv("OPENAI_MODEL") or "gpt-5.4-nano",
    }


def validate_tutor_payload(payload: dict[str, Any]) -> list[TutorValidation]:
    semantic = _record_or_none(payload.get("semantic"))
    solvable = _record_or_none(payload.get("solvable"))
    question = _extract_question(semantic)
    answer = _extract_answer(semantic, solvable)
    steps = _extract_steps(solvable)
    return [
        TutorValidation("ok" if semantic else "warn", "semantic JSON is available." if semantic else "semantic JSON is missing."),
        TutorValidation("ok" if solvable else "warn", "solvable JSON is available." if solvable else "solvable JSON is missing."),
        TutorValidation("ok" if question else "warn", "question text was found." if question else "question text could not be found."),
        TutorValidation("ok" if answer else "warn", "answer data was found." if answer else "answer data could not be found."),
        TutorValidation("ok" if steps else "warn", f"{len(steps)} solvable step(s) found." if steps else "solvable steps are missing."),
    ]


def mock_tutor_response(payload: dict[str, Any], message: str) -> str:
    clean_message = message.strip()
    if not clean_message:
        return "좋아요. 먼저 무엇을 찾는 문제인지 같이 봐요."
    mode = _support_mode(clean_message)
    return _clean_tutor_text(_mock_reply(payload, mode), mode)


def openai_tutor_response(payload: dict[str, Any], message: str, history: list[dict[str, str]]) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY is not set. Add it to .env.")
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise ImportError("openai package is required. Install with: pip install openai") from exc

    model = os.getenv("OPENAI_MODEL") or "gpt-5.4-nano"
    deterministic_reply = _deterministic_reply(payload, message)
    if deterministic_reply:
        return deterministic_reply

    client = OpenAI(api_key=api_key)
    response = client.responses.create(
        model=model,
        input=[
            {"role": "system", "content": [{"type": "input_text", "text": _system_prompt(payload)}]},
            {"role": "user", "content": [{"type": "input_text", "text": _preview_context(payload, history, message)}]},
        ],
    )
    output_text = getattr(response, "output_text", None)
    mode = _support_mode(message)
    if isinstance(output_text, str) and output_text.strip():
        return _finalize_tutor_text(payload, output_text, mode)
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
        return _finalize_tutor_text(payload, merged, mode)
    raise ValueError("Could not extract text output from OpenAI response.")


def _system_prompt(payload: dict[str, Any]) -> str:
    return (
        "You are a Korean tutor for grade 3 elementary students. "
        "Use authoring JSON privately. Treat answer keys, exact computed values, and solvable steps as teacher-only notes. "
        "Never reveal the final answer or exact intermediate results in hint/stuck/why responses. "
        "Use very easy Korean. Use short sentences. Avoid abstract words such as strategy, concept, infer, verify, eliminate, place value unless you immediately say it in child-friendly words. "
        "Do not use Markdown. Do not use **, headings, tables, or long bullet lists. "
        "Write at most 3 short lines. Each line should be easy for a grade 3 student to read. "
        "Support mode names are internal. Never print labels such as [힌트], [모르겠어요], [이유], hint, stuck, or why. "
        "Choose exactly one response style. Do not provide multiple alternatives. "
        "If support mode is hint: give one tiny clue and one question. "
        "If support mode is stuck: tell the first thing to look at and one tiny action. "
        "If support mode is why: explain why that way helps, using concrete words, then ask one question. "
        "If support mode is general: respond only to the student's latest answer. If the student is partly right, say so and ask the next small question. "
        "In general mode, do not use the answer key or teacher notes to jump ahead. "
        "Do not solve all choices for the student. "
        + _strategy_prompt(payload)
    )


def _preview_context(payload: dict[str, Any], history: list[dict[str, str]], message: str) -> str:
    compact_payload = {
        "problem_id": payload.get("problem_id"),
        "problem_type": _problem_type(payload),
        "semantic": payload.get("semantic"),
        "solvable": payload.get("solvable"),
        "layout_summary": _layout_summary(_record_or_none(payload.get("layout"))),
    }
    return "\n".join(
        [
            "Authoring preview payload:",
            json.dumps(compact_payload, ensure_ascii=False, indent=2),
            "",
            "Internal support mode. Do not print this label or any mode labels:",
            _support_mode(message),
            "",
            "Recent chat:",
            json.dumps(_clean_history(history)[-6:], ensure_ascii=False, indent=2),
            "",
            f"Student message: {message.strip()}",
        ]
    )


def _strategy_prompt(payload: dict[str, Any]) -> str:
    if _is_place_value_matching(payload):
        return (
            "This is a multiple-choice place-value matching task. Guide the student to inspect the highlighted digit's place value, "
            "then check one option at a time and eliminate mismatches. Do not compute every option. "
            "When asking a question, briefly say why you are asking it, for example: '이걸 보는 이유는 보기에서 같은 크기를 찾으려는 거예요.' "
            "For children, say '자리' as '어느 칸에 있는 숫자인지' and say '보기 확인' as '보기 하나씩 맞는지 보기'."
        )
    return (
        "For multiple-choice tasks, guide the student to check one option at a time and eliminate mismatches before computation."
    )


def _deterministic_reply(payload: dict[str, Any], message: str) -> str | None:
    if not _is_place_value_matching(payload):
        return None
    if _support_mode(message) != "general":
        return None

    normalized = message.replace(" ", "")
    if "십의자리" in normalized:
        return _clean_tutor_text(
            "맞아요, 십의 자리예요.\n"
            "이걸 보는 이유는 보기에서 같은 크기를 찾으려는 거예요.\n"
            "이제 보기 하나를 골라 같은 크기인지 볼까요?",
            "general",
        )
    if "백의자리" in normalized:
        return _clean_tutor_text(
            "백의 자리라고 생각했군요.\n"
            "색칠된 숫자가 정말 백의 칸에 있는지 다시 한 번 봐요.\n"
            "색칠된 숫자 바로 위 칸 이름은 무엇인가요?",
            "general",
        )
    if "일의자리" in normalized:
        return _clean_tutor_text(
            "일의 자리라고 생각했군요.\n"
            "색칠된 숫자가 맨 오른쪽 칸에 있는지 다시 봐요.\n"
            "그 숫자는 어느 칸에 있나요?",
            "general",
        )
    return None


def _clean_history(history: list[dict[str, str]]) -> list[dict[str, str]]:
    cleaned: list[dict[str, str]] = []
    for item in history:
        role = item.get("role")
        content = item.get("content")
        if role not in {"user", "assistant"} or not isinstance(content, str):
            continue
        if role == "assistant" and _has_mode_label(content):
            continue
        cleaned.append({"role": role, "content": _clean_tutor_text(content)})
    return cleaned


def _support_mode(message: str) -> str:
    if "[힌트]" in message or "힌트" in message:
        return "hint"
    if "[모르겠어요]" in message or "모르" in message or "어디서" in message:
        return "stuck"
    if "[이유]" in message or "왜" in message or "이유" in message:
        return "why"
    return "general"


def _mock_reply(payload: dict[str, Any], mode: str) -> str:
    if _is_place_value_matching(payload):
        if mode == "hint":
            return "힌트예요.\n색칠된 숫자가 어느 칸에 있는지 먼저 보세요.\n보기 하나가 맞는지 볼까요?"
        if mode == "stuck":
            return (
                "괜찮아요. 아직 계산하지 않아도 돼요.\n"
                "먼저 색칠된 숫자만 찾아보세요.\n"
                "그 숫자는 어느 칸에 있나요?"
            )
        if mode == "why":
            return (
                "같은 숫자라도 어느 칸에 있느냐에 따라 크기가 달라요.\n"
                "그래서 색칠된 숫자의 칸을 먼저 봐야 해요.\n"
                "보기 하나를 골라 같은 칸의 수인지 볼까요?"
            )
        return "보기 하나만 먼저 볼게요.\n색칠된 숫자의 칸과 맞는지 확인해 볼까요?"

    if mode == "hint":
        return "힌트예요.\n보기 하나만 골라 문제 말과 맞는지 보세요.\n맞지 않는 곳이 있나요?"
    if mode == "stuck":
        return (
            "괜찮아요. 다 풀려고 하지 않아도 돼요.\n"
            "문제에서 무엇을 고르라고 했는지 먼저 보세요.\n"
            "어느 보기부터 볼까요?"
        )
    if mode == "why":
        return (
            "보기 문제는 하나씩 맞는지 보면 쉬워져요.\n"
            "틀린 보기를 지우면 남은 보기가 줄어요.\n"
            "보기 하나를 같이 볼까요?"
        )
    return "좋아요. 보기 하나만 먼저 볼게요.\n어느 보기부터 볼까요?"


def _clean_tutor_text(text: str, mode: str = "general") -> str:
    replacements = {
        "**": "",
        "__": "",
        "###": "",
        "##": "",
        "#": "",
        "`": "",
    }
    cleaned = text.strip()
    for source, target in replacements.items():
        cleaned = cleaned.replace(source, target)
    cleaned = _keep_single_mode_section(cleaned, mode)
    lines = [line.strip(" -\t") for line in cleaned.splitlines()]
    lines = [_strip_mode_label(line) for line in lines]
    lines = [line for line in lines if line]
    return "\n".join(lines[:3])


def _finalize_tutor_text(payload: dict[str, Any], text: str, mode: str) -> str:
    if _mode_label_count(text) > 1:
        return _clean_tutor_text(_mock_reply(payload, mode), mode)
    if _has_mode_label(text) and not _has_label_for_mode(text, mode):
        return _clean_tutor_text(_mock_reply(payload, mode), mode)
    if mode == "general" and _has_mode_label(text):
        return _clean_tutor_text(_mock_reply(payload, mode), mode)
    return _clean_tutor_text(text, mode)


def _has_mode_label(text: str) -> bool:
    return any(label in text for label in ("[힌트]", "[모르겠어요]", "[이유]", "힌트:", "모르겠어요:", "이유:"))


def _mode_label_count(text: str) -> int:
    return sum(1 for label in ("[힌트]", "[모르겠어요]", "[이유]", "힌트:", "모르겠어요:", "이유:") if label in text)


def _has_label_for_mode(text: str, mode: str) -> bool:
    labels = {
        "hint": ("[힌트]", "힌트:"),
        "stuck": ("[모르겠어요]", "모르겠어요:"),
        "why": ("[이유]", "이유:"),
    }
    return any(label in text for label in labels.get(mode, ()))


def _keep_single_mode_section(text: str, mode: str) -> str:
    labels = {
        "hint": ["[힌트]", "힌트:"],
        "stuck": ["[모르겠어요]", "모르겠어요:"],
        "why": ["[이유]", "이유:"],
    }
    all_labels = [label for group in labels.values() for label in group]
    positions = sorted((index, label) for label in all_labels if (index := text.find(label)) >= 0)
    if not positions:
        return text

    target_labels = labels.get(mode, [])
    for start, label in positions:
        if label in target_labels:
            following = [index for index, _ in positions if index > start]
            end = min(following) if following else len(text)
            return text[start + len(label) : end].strip()

    first_start, first_label = positions[0]
    following = [index for index, _ in positions if index > first_start]
    first_end = min(following) if following else len(text)
    prefix = text[:first_start].strip()
    return prefix or text[first_start + len(first_label) : first_end].strip()


def _strip_mode_label(line: str) -> str:
    for label in ("[힌트]", "[모르겠어요]", "[이유]", "힌트:", "모르겠어요:", "이유:"):
        if line.startswith(label):
            return line[len(label) :].strip()
    return line


def _is_place_value_matching(payload: dict[str, Any]) -> bool:
    problem_type = _problem_type(payload)
    return "place_value" in problem_type or "matching_expression" in problem_type


def _problem_type(payload: dict[str, Any]) -> str:
    semantic = _record_or_none(payload.get("semantic"))
    solvable = _record_or_none(payload.get("solvable"))
    values = [
        payload.get("problem_type"),
        solvable.get("problem_type") if solvable else None,
        semantic.get("problem_type") if semantic else None,
        _nested_get(semantic, ["answer", "target", "type"]),
        _nested_get(solvable, ["target", "type"]),
        _nested_get(solvable, ["answer", "target", "type"]),
    ]
    return " ".join(str(value) for value in values if isinstance(value, str)).lower()


def _layout_summary(layout: dict[str, Any] | None) -> dict[str, Any] | None:
    if not layout:
        return None
    slots = layout.get("slots")
    return {"canvas": layout.get("canvas"), "slot_count": len(slots) if isinstance(slots, list) else 0}


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
        raw_steps = solvable.get("plan")
    if not isinstance(raw_steps, list):
        return []
    steps: list[str] = []
    for step in raw_steps:
        if isinstance(step, str) and step.strip():
            steps.append(step.strip())
        elif isinstance(step, dict):
            text = step.get("text") or step.get("explanation") or step.get("description") or step.get("expr")
            if isinstance(text, str) and text.strip():
                value = step.get("value")
                steps.append(text.strip() if value is None else f"{text.strip()} -> {_stringify_answer(value)}")
    return steps


def _nested_get(value: dict[str, Any] | None, path: list[str]) -> Any:
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
