"""Persist explicit review decisions in the DSL, independently of layout inference."""
from copy import deepcopy

import libcst as cst
from modu_math.dsl import BlankSlot, ChoiceSlot

from .dsl_patch import (
    TutorRendererFlowUpdater,
    _arg_value_to_cst,
    _call_name,
    _keyword_arg,
)
from .problems import resolve_problem_paths


class AnswerSlotKeyUpdater(cst.CSTTransformer):
    """Keep explicit DSL answer slots aligned with the editor review contract."""

    def __init__(self, review):
        self.blank_keys, self.choice_keys = _review_slot_answer_keys(review)
        self.updated_slots = set()

    def leave_Call(self, original_node, updated_node):
        slot_type = _call_name(original_node)
        if slot_type not in {"BlankSlot", "ChoiceSlot"}:
            return updated_node
        id_arg = _keyword_arg(original_node, "id")
        if id_arg is None or not isinstance(id_arg.value, cst.SimpleString):
            return updated_node
        try:
            slot_id = id_arg.value.evaluated_value
        except Exception:
            return updated_node
        answer_key = (
            self.blank_keys.get(slot_id)
            if slot_type == "BlankSlot"
            else self.choice_keys.get(slot_id)
        )
        if answer_key is None:
            return updated_node

        args = list(updated_node.args)
        replacement = cst.Arg(
            keyword=cst.Name("answer_key"), value=_arg_value_to_cst(answer_key)
        )
        for index, arg in enumerate(args):
            if arg.keyword and arg.keyword.value == "answer_key":
                args[index] = replacement
                break
        else:
            args.append(replacement)
        self.updated_slots.add(slot_id)
        return updated_node.with_changes(args=tuple(args))


def _review_slot_answer_keys(review):
    blank_keys = {}
    choice_candidates = {}
    if review["mode"] not in {"choice", "grouped_choice"}:
        for answer in review["answers"]:
            ref = answer.get("ref", "")
            if ref.startswith("slot."):
                blank_keys[ref] = answer["value"]
    elif review["mode"] == "choice":
        for choice in review["choices"]:
            for ref in choice.get("sourceRefs", []):
                if ref.startswith("slot."):
                    choice_candidates.setdefault(ref, []).append(choice)
        # A real ChoiceSlot is referenced by all of its choices. A single
        # reference normally points at a visual TextSlot and must not be edited.
        choice_keys = {
            ref: tuple(item["text"] for item in choices if item["correct"])
            for ref, choices in choice_candidates.items()
            if len(choices) >= 2 and any(item["correct"] for item in choices)
        }
        return blank_keys, choice_keys
    else:
        choice_keys = {}
        for group in review.get("groups", []):
            selected = group["choices"][group["correct_index"]]
            for ref in group.get("source_refs", []):
                if ref.startswith("slot."):
                    choice_keys[ref] = (selected,)
        return blank_keys, choice_keys
    return blank_keys, {}


def normalize_review(value):
    if not isinstance(value, dict):
        raise ValueError("검수 설정이 올바르지 않습니다.")
    mode = value.get("mode")
    status = value.get("status", "pending")
    if mode not in {"panel_input", "choice", "ox", "canvas_slots", "grouped_choice"}:
        raise ValueError("응답 방식을 선택하세요.")
    if status not in {"pending", "needs_changes", "verified"}:
        raise ValueError("검수 상태가 올바르지 않습니다.")
    note = value.get("note", "")
    answers = value.get("answers", [])
    choices = value.get("choices", [])
    if not isinstance(note, str) or len(note) > 10000:
        raise ValueError("검수 메모는 10000자 이내로 입력하세요.")
    if not isinstance(answers, list) or len(answers) > 100 or any(
        not isinstance(a, dict) or not isinstance(a.get("value"), str)
        or not a["value"].strip() or not isinstance(a.get("ref", ""), str)
        for a in answers
    ):
        raise ValueError("각 입력 항목의 정답을 입력하세요.")
    if not isinstance(choices, list) or len(choices) > 100:
        raise ValueError("선택지 형식이 올바르지 않습니다.")
    ids = set()
    cleaned = []
    for choice in choices:
        if not isinstance(choice, dict) or any(not isinstance(choice.get(k), str) or not choice[k].strip() for k in ("id", "text")):
            raise ValueError("선택지 내용과 ID가 필요합니다.")
        if choice["id"] in ids or type(choice.get("correct")) is not bool:
            raise ValueError("선택지 ID와 정답 표시를 확인하세요.")
        if not isinstance(choice.get("label", ""), str):
            raise ValueError("선택지 번호가 올바르지 않습니다.")
        refs = choice.get("sourceRefs", [])
        if not isinstance(refs, list) or any(not isinstance(ref, str) for ref in refs):
            raise ValueError("선택지 연결이 올바르지 않습니다.")
        ids.add(choice["id"])
        cleaned.append({k: choice[k] for k in ("id", "text", "correct")} | {"label": choice.get("label", ""), "sourceRefs": refs})
    if status == "verified" and mode == "choice" and (len(cleaned) < 2 or not any(c["correct"] for c in cleaned)):
        raise ValueError("선택지를 두 개 이상 작성하고 정답을 선택하세요.")
    if status == "verified" and mode not in {"choice", "grouped_choice"} and not answers:
        raise ValueError("정답을 하나 이상 입력하세요.")
    if mode == "ox" and any(a["value"] not in {"O", "X"} for a in answers):
        raise ValueError("OX 정답은 O 또는 X로 지정하세요.")
    result = {"mode": mode, "status": status, "note": note, "answers": answers, "choices": cleaned}
    if mode == "grouped_choice":
        from .choice_groups import normalize_choice_groups
        result["groups"] = normalize_choice_groups(value.get("groups"))
        if not result["groups"]:
            raise ValueError("소문항을 하나 이상 작성하세요.")
    return result


def save_answer_review(problem_id, value):
    review = normalize_review(value)
    paths = resolve_problem_paths(problem_id)
    module = cst.parse_module(paths.dsl_path.read_text(encoding="utf-8"))
    module = module.visit(AnswerSlotKeyUpdater(review))
    updater = TutorRendererFlowUpdater(review, variable_name="EDITOR_ANSWER_REVIEW")
    paths.dsl_path.write_text(module.visit(updater).code, encoding="utf-8")
    return review


def review_with_slot_answer_keys(value, problem):
    """Overlay explicit BlankSlot/ChoiceSlot keys for review hydration.

    Review saves write these keys at the same time, so this mainly handles a
    human changing an answer_key directly in problem.dsl.py.
    """
    review = deepcopy(normalize_review(value))
    slots = getattr(problem, "slots", ())
    if review["mode"] not in {"choice", "grouped_choice"}:
        explicit = {
            slot.id: slot.answer_key
            for slot in slots
            if isinstance(slot, BlankSlot)
            and isinstance(slot.answer_key, str)
            and slot.answer_key.strip()
        }
        if explicit:
            by_ref = {answer.get("ref"): answer for answer in review["answers"]}
            if len(explicit) == 1 and len(review["answers"]) == 1:
                slot_id, answer_key = next(iter(explicit.items()))
                review["answers"][0] = {"ref": slot_id, "value": answer_key}
                by_ref = {slot_id: review["answers"][0]}
            for slot_id, answer_key in explicit.items():
                if slot_id in by_ref:
                    by_ref[slot_id]["value"] = answer_key
                else:
                    review["answers"].append({"ref": slot_id, "value": answer_key})
    elif review["mode"] == "choice":
        keys = {
            slot.id: set(slot.answer_key)
            for slot in slots
            if isinstance(slot, ChoiceSlot) and slot.answer_key
        }
        for choice in review["choices"]:
            refs = choice.get("sourceRefs", [])
            matching = [keys[ref] for ref in refs if ref in keys]
            if matching:
                choice["correct"] = any(choice["text"] in values for values in matching)
    else:
        keys = {
            slot.id: tuple(slot.answer_key)
            for slot in slots
            if isinstance(slot, ChoiceSlot) and slot.answer_key
        }
        for group in review.get("groups", []):
            values = [
                value
                for ref in group.get("source_refs", [])
                for value in keys.get(ref, ())
            ]
            indexes = [
                index
                for index, choice in enumerate(group["choices"])
                if choice in values
            ]
            if len(indexes) == 1:
                group["correct_index"] = indexes[0]
    return normalize_review(review)


def apply_answer_review(semantic, solvable, value):
    review = normalize_review(value)
    semantic, solvable = deepcopy((semantic, solvable))
    for artifact in (semantic, solvable):
        if not isinstance(artifact, dict):
            continue
        answer = artifact.setdefault("answer", {})
        answer["presentation"] = {"mode": {"ox": "panel_input", "grouped_choice": "choice"}.get(review["mode"], review["mode"]), "editor_managed": True, "review": deepcopy(review)}
        answer.pop("choice_groups", None)
        answer.pop("values", None)
        if review["mode"] == "grouped_choice":
            answer["choice_groups"] = deepcopy(review["groups"])
            answer["choices"] = []
            keys = [{"id": g["id"], "value": g["choices"][g["correct_index"]]} for g in review["groups"]]
        elif review["mode"] == "choice":
            answer["choices"] = [{"id": c["id"], "label": c["label"], "text": c["text"], "source_refs": c["sourceRefs"]} for c in review["choices"]]
            keys = [{"id": c["id"], "value": c["text"]} for c in review["choices"] if c["correct"]]
        else:
            answer["choices"] = []
            keys = [{"value": a["value"], **({"slot_id": a["ref"]} if a.get("ref", "").startswith("slot.") else {})} for a in review["answers"]]
        answer["answer_key"] = keys
        answer["value"] = keys[0]["value"] if len(keys) == 1 else [k["value"] for k in keys]
        answer["blanks"] = []
    return semantic, solvable
