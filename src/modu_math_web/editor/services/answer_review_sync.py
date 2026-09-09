"""Transfer review decisions using identities while retaining translated content."""

import ast
from copy import deepcopy
import re

from .answer_review import normalize_review, save_answer_review
from .build import run_problem_build
from .placement_sync import _effective_slots, translation_targets
from .problems import read_problem_detail


class ReviewMappingError(ValueError):
    pass


def _saved_review(detail):
    module = ast.parse(detail["dsl"])
    for statement in reversed(module.body):
        if isinstance(statement, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == "EDITOR_ANSWER_REVIEW"
            for t in statement.targets
        ):
            return normalize_review(ast.literal_eval(statement.value))
    return None


def _choices(detail, review):
    if review and review["mode"] == "choice":
        return review["choices"]
    answer = (detail.get("semantic") or {}).get("answer", {})
    choices = answer.get("choices") or (
        (detail.get("solvable") or {}).get("answer") or {}
    ).get("choices", [])
    result = []
    for index, value in enumerate(choices):
        item = value if isinstance(value, dict) else {"text": str(value)}
        text = str(item.get("text", item.get("value", "")))
        prefix = re.match(r"^\s*([①-⑳]|\([1-9][0-9]?\)|[1-9][0-9]?[.)])\s*", text)
        result.append(
            {
                "id": item.get("id") or f"choice.{index + 1}",
                "text": text[prefix.end() :] if prefix else text,
                "label": item.get("label")
                or (prefix.group(1) if prefix else str(index + 1)),
                "sourceRefs": item.get(
                    "source_refs", [item["slot_id"]] if item.get("slot_id") else []
                ),
            }
        )
    return result


def _neutral(value):
    return bool(
        re.fullmatch(
            r"[+-]?(?:\d+(?:\.\d+)?|\d+\s*/\s*\d+|\d+\s+\d+\s*/\s*\d+)", value.strip()
        )
    )


def map_review(source, target_review, target_detail, source_slots, target_slots):
    review = deepcopy(source)
    review["note"] = (target_review or {}).get("note", "")
    review["choices"] = []
    review["answers"] = []
    review.pop("groups", None)
    if source["mode"] == "choice":
        candidates = _choices(target_detail, target_review)
        used = set()
        for choice in source["choices"]:
            matches = [item for item in candidates if item["id"] == choice["id"]]
            if not matches and choice.get("sourceRefs"):
                matches = [
                    item
                    for item in candidates
                    if set(item.get("sourceRefs", [])) == set(choice["sourceRefs"])
                ]
            if len(matches) == 1:
                translated = deepcopy(matches[0])
            elif not matches:
                refs = choice.get("sourceRefs") or [choice["id"]]
                texts = [
                    target_slots.get(ref, {}).get("content", {}).get("text")
                    for ref in refs
                ]
                if not texts or any(
                    not isinstance(text, str) or not text.strip() for text in texts
                ):
                    raise ReviewMappingError(
                        f"선택지 ‘{choice['label']} {choice['text']}’에 대응하는 번역을 찾지 못했습니다."
                    )
                translated = {
                    "id": choice["id"],
                    "label": choice["label"],
                    "text": " ".join(texts),
                    "sourceRefs": refs,
                }
            else:
                raise ReviewMappingError(
                    "선택지 연결이 중복되어 정답을 적용하지 않았습니다."
                )
            if translated["id"] in used:
                raise ReviewMappingError("여러 선택지가 같은 번역에 연결되어 있습니다.")
            used.add(translated["id"])
            translated["correct"] = choice["correct"]
            review["choices"].append(translated)
    elif source["mode"] == "grouped_choice":
        groups = (target_review or {}).get("groups") or (
            (target_detail.get("semantic") or {}).get("answer") or {}
        ).get("choice_groups", [])
        review["groups"] = []
        for group in source["groups"]:
            matches = [item for item in groups if item.get("id") == group["id"]]
            if len(matches) != 1 or len(matches[0].get("choices", [])) != len(
                group["choices"]
            ):
                raise ReviewMappingError(
                    f"소문항 ‘{group['label']}’의 선택지 구조가 다릅니다."
                )
            translated = deepcopy(matches[0])
            # String-only group choices have no stable choice IDs. Resolve the
            # selected translated text through the source/target text slots.
            selected = group["choices"][group["correct_index"]]
            translated_value = _translated_answer(selected, source_slots, target_slots)
            indexes = [
                i
                for i, value in enumerate(translated["choices"])
                if value == translated_value
            ]
            if len(indexes) != 1:
                raise ReviewMappingError(
                    f"소문항 ‘{group['label']}’의 번역 정답 연결을 확인해 주세요."
                )
            translated["correct_index"] = indexes[0]
            review["groups"].append(translated)
    else:
        for answer in source["answers"]:
            ref = answer.get("ref", "")
            if ref.startswith("slot.") and ref not in target_slots:
                raise ReviewMappingError("대응하는 정답 입력칸이 없습니다.")
            if source["mode"] == "canvas_slots" and (
                ref not in target_slots
                or not target_slots[ref].get("content", {}).get("interaction")
            ):
                raise ReviewMappingError(
                    "번역 문항의 정답 입력칸 연결을 먼저 지정해 주세요."
                )
            value = (
                answer["value"]
                if source["mode"] == "ox"
                else _translated_answer(answer["value"], source_slots, target_slots)
            )
            review["answers"].append({**answer, "value": value})
    return normalize_review(review)


def _translated_answer(value, source_slots, target_slots):
    if _neutral(value) or value in {"O", "X", "○", "×"}:
        return value
    refs = [
        identity
        for identity, slot in source_slots.items()
        if slot.get("content", {}).get("text", "").strip() == value.strip()
    ]
    texts = {
        target_slots[ref].get("content", {}).get("text")
        for ref in refs
        if ref in target_slots
    }
    if (
        len(texts) == 1
        and isinstance(next(iter(texts)), str)
        and next(iter(texts)).strip()
    ):
        return next(iter(texts))
    raise ReviewMappingError(
        f"문자 정답 ‘{value}’의 번역을 확인해 주세요. 숫자·분수·OX는 바로 적용할 수 있습니다."
    )


def sync_answer_reviews(problem_id, payload):
    source_id, targets = translation_targets(problem_id, payload.get("languages"))
    source = _saved_review(read_problem_detail(source_id))
    if not source:
        raise ValueError("원본 문항의 정답 검수를 먼저 저장하세요.")
    source_slots = _effective_slots(source_id)
    results = []
    for language, target_id in targets.items():
        result = {
            "language": language,
            "problem_id": target_id,
            "saved": False,
            "status": "error",
        }
        try:
            target_slots = _effective_slots(target_id)
            detail = read_problem_detail(target_id)
            translated = map_review(
                source,
                _saved_review(detail),
                detail,
                source_slots,
                target_slots,
            )
            save_answer_review(target_id, translated)
            result["saved"] = True
            built = run_problem_build(target_id)
            if not built.ok:
                raise ValueError(
                    built.error or "저장은 완료했지만 빌드에 실패했습니다."
                )
            result["status"] = "success"
        except ReviewMappingError as exc:
            result.update(status="skipped", error=str(exc))
        except Exception as exc:
            result["error"] = str(exc)
        results.append(result)
    return results
