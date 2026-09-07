"""Persist explicit review decisions in the DSL, independently of layout inference."""
from copy import deepcopy

import libcst as cst

from .dsl_patch import TutorRendererFlowUpdater
from .problems import resolve_problem_paths


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
    updater = TutorRendererFlowUpdater(review, variable_name="EDITOR_ANSWER_REVIEW")
    paths.dsl_path.write_text(module.visit(updater).code, encoding="utf-8")
    return review


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
