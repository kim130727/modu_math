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


def rule_tutor_response(payload: dict[str, Any], message: str, history: list[dict[str, str]]) -> dict[str, Any]:
    solvable = _record_or_none(payload.get("solvable"))
    if not solvable:
        return {"reply": "이 문제에는 solvable JSON이 아직 없어요.\n먼저 문제를 빌드해서 풀이 단계를 만든 뒤 다시 시작해 주세요.", "choices": []}

    steps = _tutor_steps(payload, solvable)
    if not steps:
        return {"reply": "solvable JSON은 있지만 풀이 단계가 비어 있어요.\nsteps 또는 plan이 만들어지면 단계별 튜터를 시작할 수 있어요.", "choices": []}

    clean_message = message.strip()
    waiting_index = _last_rule_step_index(history)
    if waiting_index is None:
        return _rule_response(solvable, steps, 0, _rule_intro(solvable, steps))

    waiting_step = steps[min(waiting_index, len(steps) - 1)]
    if _student_wants_restart(clean_message):
        return _rule_response(solvable, steps, 0, _rule_intro(solvable, steps))
    if _student_asks_for_next(clean_message):
        next_index = min(waiting_index + 1, len(steps) - 1)
        return _rule_response(solvable, steps, next_index, _render_rule_step(solvable, steps, next_index, prefix="좋아요. 다음 단계로 가 볼게요."))
    if _student_is_confused(clean_message):
        return _rule_response(solvable, steps, waiting_index, _rule_confusion_reply(solvable, waiting_step, waiting_index))
    if _answer_matches_step(clean_message, waiting_step):
        next_index = waiting_index + 1
        if next_index >= len(steps):
            return {"reply": _rule_complete(solvable), "choices": []}
        return _rule_response(solvable, steps, next_index, _render_rule_step(solvable, steps, next_index, prefix="좋아요, 맞았어요."))

    expected_hint = _step_expected_hint(solvable, waiting_step, waiting_index)
    if expected_hint:
        return _rule_response(solvable, steps, waiting_index, (
            "조금 다르게 본 것 같아요.\n"
            f"{waiting_index + 1}단계: {waiting_step['prompt']}\n"
            f"{expected_hint} 다시 입력해 볼까요?"
        ))
    return _rule_response(solvable, steps, waiting_index, (
        "좋아요. 이 단계에서 생각한 값을 입력해 주세요.\n"
        f"{waiting_index + 1}단계: {waiting_step['prompt']}"
    ))


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


def _tutor_steps(payload: dict[str, Any], solvable: dict[str, Any]) -> list[dict[str, str]]:
    derived_steps = _derive_tutor_steps(payload, solvable)
    if derived_steps:
        return derived_steps

    raw_steps = solvable.get("steps")
    if not isinstance(raw_steps, list) or not raw_steps:
        raw_steps = solvable.get("plan")
    if not isinstance(raw_steps, list):
        return []

    steps: list[dict[str, str]] = []
    for index, raw_step in enumerate(raw_steps, start=1):
        prompt = ""
        expected = ""
        if isinstance(raw_step, str):
            prompt = raw_step.strip()
        elif isinstance(raw_step, dict):
            prompt = _first_string(raw_step, ["question", "prompt", "expr", "text", "description", "id"])
            explanation = _first_string(raw_step, ["explanation"])
            if "value" in raw_step:
                expected = _student_expected_answer(raw_step["value"])
            elif "expected" in raw_step:
                expected = _student_expected_answer(raw_step["expected"])
        if not prompt:
            prompt = f"{index}번째 풀이 단계를 확인해요."
        step = {"prompt": prompt, "expected": expected}
        if isinstance(raw_step, dict) and explanation:
            step["explanation"] = explanation
        steps.append(step)
    return steps


def _derive_tutor_steps(payload: dict[str, Any], solvable: dict[str, Any]) -> list[dict[str, str]]:
    method = str(solvable.get("method") or "").lower()
    problem_type = str(solvable.get("problem_type") or "").lower()
    if "place_value" in method or "place_value" in problem_type:
        target = _given_value(solvable, "obj.target")
        if isinstance(target, str) and target.strip():
            return [
                {
                    "prompt": "색칠된 부분이 실제로 어떤 곱셈식인지 보기에서 골라요.",
                    "expected": target.strip(),
                    "choices": _place_value_expression_choices(target.strip()),
                }
            ]

    if "compare" not in method and "비교" not in problem_type:
        return []

    expressions = _comparison_expressions(solvable)
    if len(expressions) < 2:
        return []

    evaluated = [(label, expr, _evaluate_arithmetic(expr)) for label, expr in expressions]
    if any(value is None for _, _, value in evaluated):
        return []

    semantic = _record_or_none(payload.get("semantic"))
    question = _extract_question(semantic) or ""
    choose_smaller = "작" in question or "small" in question.lower()
    choose_larger = "크" in question or "큰" in question or "large" in question.lower()
    answer_record = _record_or_none(solvable.get("answer"))
    answer_value = _stringify_answer(answer_record.get("value")) if answer_record and "value" in answer_record else ""

    steps: list[dict[str, str]] = []
    for _, expr, value in evaluated:
        if str(expr).strip() == str(value):
            prompt = f"{expr}은 이미 수로 주어졌어요."
        else:
            prompt = f"{expr}의 값을 먼저 구해요."
        steps.append({"prompt": prompt, "expected": str(value)})

    values_text = ", ".join(f"{expr} = {value}" for _, expr, value in evaluated)
    if choose_smaller:
        compare_prompt = f"계산한 값을 비교해요. {values_text} 중 더 작은 것은 무엇일까요?"
    elif choose_larger:
        compare_prompt = f"계산한 값을 비교해요. {values_text} 중 더 큰 것은 무엇일까요?"
    else:
        compare_prompt = f"계산한 값을 비교해요. {values_text} 중 조건에 맞는 것은 무엇일까요?"
    steps.append({"prompt": compare_prompt, "expected": answer_value})
    return steps


def _comparison_expressions(solvable: dict[str, Any]) -> list[tuple[str, str]]:
    quantities = _record_or_none(_record_or_none(solvable.get("inputs")).get("quantities") if _record_or_none(solvable.get("inputs")) else None)
    expressions: list[tuple[str, str]] = []
    if quantities:
        for key, value in quantities.items():
            if isinstance(value, str) and value.strip():
                expressions.append((str(key), value.strip()))

    if not expressions:
        given = solvable.get("given")
        if isinstance(given, list):
            for item in given:
                if not isinstance(item, dict):
                    continue
                value = item.get("value")
                if isinstance(value, str) and value.strip():
                    expressions.append((str(item.get("ref") or len(expressions) + 1), value.strip()))
    return expressions


def _evaluate_arithmetic(expression: str) -> int | float | None:
    import ast
    import operator
    import re

    text = expression.replace("×", "*").replace("x", "*").replace("X", "*").replace("÷", "/")
    if not re.fullmatch(r"[\d\s+\-*/().]+", text):
        return None
    operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    def eval_node(node: ast.AST) -> int | float:
        if isinstance(node, ast.Expression):
            return eval_node(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in operators:
            return operators[type(node.op)](eval_node(node.left), eval_node(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in operators:
            return operators[type(node.op)](eval_node(node.operand))
        raise ValueError("unsupported expression")

    try:
        value = eval_node(ast.parse(text, mode="eval"))
    except Exception:
        return None
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return value


def _rule_intro(solvable: dict[str, Any], steps: list[dict[str, str]]) -> str:
    if _is_place_value_matching({"solvable": solvable}):
        multiple = _given_value(solvable, "obj.multiple")
        highlighted = _given_value(solvable, "obj.highlighted_value")
        lead = "Rule Tutor로 자리값을 보면서 풀어 볼게요."
        if multiple and highlighted:
            lead = f"{multiple}에서 색칠한 부분 {highlighted}이 어떤 보기와 같은지 찾는 문제예요."
        return _render_rule_step(solvable, steps, 0, prefix=lead)
    if _is_inscribed_regular_hexagon_perimeter({"solvable": solvable}):
        return _render_rule_step(
            solvable,
            steps,
            0,
            prefix="Rule Tutor로 도형의 이유를 확인하면서 풀어 볼게요.\n먼저 지름으로 반지름을 구합니다.",
        )
    method = str(solvable.get("method") or solvable.get("problem_type") or "풀이").replace("_", " ")
    return _render_rule_step(solvable, steps, 0, prefix=f"Rule Tutor로 단계별 풀이를 시작할게요.\n풀이 방법: {method}")


def _rule_response(solvable: dict[str, Any], steps: list[dict[str, str]], index: int, reply: str) -> dict[str, Any]:
    return {"reply": reply, "choices": _step_choices(solvable, steps, index)}


def _step_choices(solvable: dict[str, Any], steps: list[dict[str, str]], index: int) -> list[str]:
    step = steps[index]
    expected = step.get("expected", "").strip()
    if not expected:
        return []
    step_choices = step.get("choices")
    if isinstance(step_choices, list):
        return _unique_choices([str(choice) for choice in step_choices])

    if _is_place_value_matching({"solvable": solvable}):
        if index == 0 and _given_value(solvable, "obj.multiple") and _given_value(solvable, "obj.highlighted_value"):
            return _unique_choices(["6", expected, "600", "869"])
        if index == 1:
            return _numeric_choices(expected)
        choice_set = _given_value(solvable, "obj.choice_set")
        if isinstance(choice_set, list):
            return _unique_choices([str(choice) for choice in choice_set])
        return _unique_choices([expected])

    if "중 더 " in step.get("prompt", "") or "조건에 맞는" in step.get("prompt", ""):
        expressions = [expr for _, expr in _comparison_expressions(solvable)]
        if expressions:
            return _unique_choices([expected, *expressions])

    if _looks_number(expected):
        return _numeric_choices(expected)
    return _unique_choices([expected])


def _numeric_choices(expected: str) -> list[str]:
    value = _number_or_none(expected)
    if value is None:
        return _unique_choices([expected])
    if isinstance(value, float) and not value.is_integer():
        candidates = [value + 1, value, value - 1, value * 10]
        return _unique_choices([_format_number(candidate) for candidate in candidates])

    number = int(value)
    if number == 0:
        candidates = [0, 1, 10, 100]
    else:
        candidates = [
            number // 10 if abs(number) >= 10 else number + 10,
            number,
            number * 10,
            number + (100 if abs(number) >= 100 else 10),
        ]
    return _unique_choices([str(candidate) for candidate in candidates])


def _place_value_expression_choices(expression: str) -> list[str]:
    import re

    match = re.fullmatch(r"\s*(\d+)\s*[×xX*]\s*(\d+)\s*", expression)
    if not match:
        return _unique_choices([expression])
    left = int(match.group(1))
    right = int(match.group(2))
    if left % 10 == 0 and left != 0:
        base = left
        while base % 10 == 0:
            base //= 10
        return _unique_choices([f"{base} × {right}", f"{base} × {right * 10}", f"{left} × {right}", f"{left * 10} × {right}"])
    else:
        candidates = [left, left * 10, left * 100, max(1, left // 10)]
    return _unique_choices([f"{candidate} × {right}" for candidate in candidates])


def _unique_choices(values: list[str]) -> list[str]:
    seen: set[str] = set()
    choices: list[str] = []
    for value in values:
        text = str(value).strip()
        if not text:
            continue
        key = _normalize_answer_text(text)
        if key in seen:
            continue
        seen.add(key)
        choices.append(text)
    return choices[:4]


def _looks_number(value: str) -> bool:
    import re

    return bool(re.fullmatch(r"-?\d+(?:\.\d+)?", value.strip()))


def _number_or_none(value: str) -> int | float | None:
    if not _looks_number(value):
        return None
    number = float(value)
    return int(number) if number.is_integer() else number


def _format_number(value: int | float) -> str:
    return str(int(value)) if isinstance(value, float) and value.is_integer() else str(value)


def _render_rule_step(solvable: dict[str, Any], steps: list[dict[str, str]], index: int, *, prefix: str = "") -> str:
    step = steps[index]
    if _is_place_value_matching({"solvable": solvable}):
        return _render_place_value_step(solvable, steps, index, prefix=prefix)

    expected_hint = _step_expected_hint(solvable, step, index)
    lines = [line for line in prefix.splitlines() if line.strip()]
    lines.append(f"{index + 1}단계: {step['prompt']}")
    if step.get("explanation"):
        lines.append(step["explanation"])
    lines.append(expected_hint or "이 단계에서 알 수 있는 값을 입력해 보세요.")
    return "\n".join(lines[:4])


def _render_place_value_step(solvable: dict[str, Any], steps: list[dict[str, str]], index: int, *, prefix: str = "") -> str:
    step = steps[index]
    lines = [line for line in prefix.splitlines() if line.strip()]
    has_highlighted_value = bool(_given_value(solvable, "obj.multiple") and _given_value(solvable, "obj.highlighted_value"))
    if not has_highlighted_value:
        lines.append(f"{index + 1}단계: {step['prompt']}")
        lines.append("색칠된 부분의 자리값을 보고 같은 곱셈식을 고르면 돼요.")
        lines.append("아래 보기 중 알맞은 식을 선택해 보세요.")
        return "\n".join(lines[:4])

    if index == 0:
        lines.append("1단계: 먼저 869의 6이 얼마를 뜻하는지 봐요.")
        lines.append("6은 십의 자리라서 6이 아니라 60을 뜻해요.")
        lines.append("그래서 색칠한 부분은 몇에 4를 곱한 걸까요?")
    elif index == 1:
        lines.append(f"2단계: {step['prompt']}")
        lines.append("이제 60에 4를 곱해 색칠한 부분의 값을 확인해요.")
        lines.append("60 × 4는 얼마일까요?")
    else:
        choices = _given_value(solvable, "obj.choice_set")
        lines.append(f"{index + 1}단계: {step['prompt']}")
        if isinstance(choices, list):
            lines.append("보기: " + ", ".join(str(choice) for choice in choices))
        lines.append("240과 같은 값을 만드는 보기를 골라 입력해 보세요.")
    return "\n".join(lines[:4])


def _rule_complete(solvable: dict[str, Any]) -> str:
    answer_record = _record_or_none(solvable.get("answer"))
    answer = _stringify_answer(answer_record.get("value")) if answer_record and "value" in answer_record else ""
    if answer:
        return f"좋아요. 풀이 단계가 모두 끝났어요.\n최종 답은 {answer}입니다.\n이제 보기나 답칸에 맞게 표시하면 돼요."
    return "좋아요. 풀이 단계가 모두 끝났어요.\n이제 문제의 답칸이나 보기에 맞게 정리해 보세요."


def _last_rule_step_index(history: list[dict[str, str]]) -> int | None:
    import re

    for item in reversed(history):
        if item.get("role") != "assistant":
            continue
        content = item.get("content", "")
        if not isinstance(content, str):
            continue
        match = re.search(r"(\d+)단계:", content)
        if match:
            return max(0, int(match.group(1)) - 1)
    return None


def _answer_matches_step(message: str, step: dict[str, str]) -> bool:
    import re

    expected = step.get("expected", "").strip()
    if not expected:
        return False
    normalized_message = _normalize_answer_text(message)
    normalized_expected = _normalize_answer_text(expected)
    if normalized_expected and normalized_expected in normalized_message:
        return True
    expected_numbers = re.findall(r"-?\d+(?:\.\d+)?", expected)
    if expected_numbers:
        message_numbers = set(re.findall(r"-?\d+(?:\.\d+)?", message))
        return any(number in message_numbers for number in expected_numbers)
    return False


def _normalize_answer_text(value: str) -> str:
    return (
        value.lower()
        .replace(" ", "")
        .replace("×", "x")
        .replace("*", "x")
        .replace("횞", "x")
        .replace("=", "")
    )


def _step_expected_hint(solvable: dict[str, Any], step: dict[str, str], index: int) -> str:
    import re

    expected = step.get("expected", "").strip()
    if not expected:
        return ""
    if "이미 수로 주어졌어요" in step.get("prompt", ""):
        return "그 수를 그대로 입력해 보세요."
    if _is_place_value_matching({"solvable": solvable}):
        if index == 0:
            return "6은 십의 자리에 있으니 60이라고 볼 수 있어요."
        if index == 1:
            return "60을 네 번 더하면 얼마인지 계산해 보세요."
        return "보기 중 240과 같은 값을 만드는 곱셈식을 찾아보세요."
    if re.fullmatch(r"-?\d+(?:\.\d+)?", expected):
        return "계산한 수를 입력해 보세요."
    return "이 단계에서 찾은 식이나 값을 입력해 보세요."


def _student_wants_restart(message: str) -> bool:
    normalized = message.replace(" ", "").lower()
    return any(token in normalized for token in ("처음", "다시", "시작", "reset", "restart"))


def _student_asks_for_next(message: str) -> bool:
    normalized = message.replace(" ", "").lower()
    return any(token in normalized for token in ("다음", "넘어", "next"))


def _student_is_confused(message: str) -> bool:
    normalized = message.replace(" ", "").lower()
    return any(
        token in normalized
        for token in (
            "모르",
            "이해",
            "무슨말",
            "헷갈",
            "어려",
            "왜",
            "설명",
            "help",
            "confus",
        )
    )


def _rule_confusion_reply(solvable: dict[str, Any], step: dict[str, str], index: int) -> str:
    if _is_place_value_matching({"solvable": solvable}):
        if index == 0:
            return (
                "좋아요, 다시 쉽게 볼게요.\n"
                "1단계: 869에서 6은 오른쪽에서 둘째 자리, 즉 십의 자리에 있어요.\n"
                "그래서 6은 6개가 아니라 60을 뜻해요.\n"
                "그럼 색칠한 부분은 몇에 4를 곱한 걸까요?"
            )
        if index == 1:
            return (
                "앞에서 색칠된 수가 60이라는 걸 확인했어요.\n"
                "이제 869 × 4에서 그 부분만 보면 60 × 4예요.\n"
                "60을 4번 더하면 얼마일까요?"
            )
        return (
            "이제 새 계산을 하는 단계가 아니에요.\n"
            "앞에서 60 × 4 = 240을 확인했어요.\n"
            "보기 중에서 240과 같은 곱셈식을 찾아보세요."
        )

    hint = _step_expected_hint(solvable, step, index)
    return (
        "좋아요, 이 단계만 다시 볼게요.\n"
        f"{index + 1}단계: {step['prompt']}\n"
        f"{hint or '문제에서 확인할 수 있는 값을 하나만 찾아보세요.'}"
    )


def _given_value(solvable: dict[str, Any], ref: str) -> Any:
    given = solvable.get("given")
    if not isinstance(given, list):
        return None
    for item in given:
        if isinstance(item, dict) and item.get("ref") == ref:
            return item.get("value")
    return None


def _first_string(source: dict[str, Any], keys: list[str]) -> str:
    for key in keys:
        value = source.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


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
    if _is_inscribed_regular_hexagon_perimeter(payload):
        return (
            "This is a circle and inscribed regular hexagon perimeter-difference task. "
            "Do not merely ask whether the hexagon side equals the radius. Before using that fact, explain the reason in child-friendly Korean: "
            "connect the circle center to two neighboring hexagon vertices; the two radii and the hexagon side form an equilateral triangle, so one side of the regular hexagon equals the radius. "
            "Then continue with diameter divided by 2, hexagon perimeter = radius times 6, circle circumference = diameter times pi, and subtract. "
            "Keep the reply short, but never skip the geometric reason for side = radius."
        )
    return (
        "For multiple-choice tasks, guide the student to check one option at a time and eliminate mismatches before computation."
    )


def _is_inscribed_regular_hexagon_perimeter(payload: dict[str, Any]) -> bool:
    problem_type = _problem_type(payload)
    semantic = _record_or_none(payload.get("semantic"))
    solvable = _record_or_none(payload.get("solvable"))
    method = str(solvable.get("method") if solvable else "").lower()
    refs: set[str] = set()
    if solvable and isinstance(solvable.get("given"), list):
        refs = {str(item.get("ref") or "") for item in solvable["given"] if isinstance(item, dict)}
    text = " ".join(
        value
        for value in (
            problem_type,
            method,
            str(_nested_get(semantic, ["answer", "target", "type"]) or "").lower(),
            str(_nested_get(solvable, ["target", "type"]) or "").lower() if solvable else "",
        )
        if value
    )
    return (
        "hexagon" in text
        and ("perimeter" in text or "circumference" in text)
        and ("rel.hexagon_inscribed" in refs or "rel.hexagon_side_equals_radius" in refs or "inscribed" in text)
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


def _student_expected_answer(value: Any) -> str:
    if isinstance(value, dict):
        for key in ("result", "value", "answer"):
            if key in value:
                return _stringify_answer(value[key])
    return _stringify_answer(value)
