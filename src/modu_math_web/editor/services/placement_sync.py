"""Copy only text placement roles between existing translations of one problem."""

from copy import deepcopy
import json

from modu_math.layout.editor_overrides import apply_editor_overrides
from .build import run_problem_build
from .dsl_patch import apply_layout_patches
from .problems import (
    list_problem_directories,
    read_problem_detail,
    resolve_problem_paths,
)

TEXT_KINDS = {"text", "text_box", "label"}
PLACEMENT_ROLES = {"", "question", "instruction", "choice", "diagram_label"}


def _effective_slots(problem_id):
    layout = read_problem_detail(problem_id)["layout"]
    if not isinstance(layout, dict):
        result = run_problem_build(problem_id)
        if not result.ok:
            raise ValueError(result.error or "문항을 빌드하지 못했습니다.")
        layout = read_problem_detail(problem_id)["layout"]
    paths = resolve_problem_paths(problem_id)
    override_path = paths.base_dir / f"{paths.artifact_base}.editor_overrides.json"
    overrides = (
        json.loads(override_path.read_text(encoding="utf-8-sig"))
        if override_path.exists()
        else None
    )
    layout = apply_editor_overrides(deepcopy(layout), overrides)
    return {slot["id"]: slot for slot in layout.get("slots", [])}


def sync_text_placements(problem_id, payload):
    source_id = resolve_problem_paths(problem_id).problem_id
    source = next(
        (
            item
            for item in list_problem_directories()
            if item["problem_id"] == source_id
        ),
        None,
    )
    if not source or not source.get("language"):
        raise ValueError("언어가 지정된 실제 문항을 열어 주세요.")
    languages = payload.get("languages")
    placements = payload.get("placements")
    equivalents = source.get("equivalent_problem_ids", {})
    if (
        not isinstance(languages, list)
        or not languages
        or any(
            not isinstance(lang, str)
            or lang not in equivalents
            or lang == source["language"]
            for lang in languages
        )
    ):
        raise ValueError("같은 문항의 다른 번역 언어를 선택하세요.")
    if not isinstance(placements, list) or not placements or len(placements) > 10000:
        raise ValueError("적용할 글자를 선택하세요.")
    roles = {}
    for placement in placements:
        if not isinstance(placement, dict):
            raise ValueError("표시 위치 설정이 올바르지 않습니다.")
        slot_id, role = placement.get("id"), placement.get("role")
        if (
            not isinstance(slot_id, str)
            or not slot_id
            or slot_id in roles
            or not isinstance(role, str)
            or role not in PLACEMENT_ROLES
        ):
            raise ValueError("표시 위치 설정이 올바르지 않습니다.")
        roles[slot_id] = role
    source_slots = _effective_slots(source_id)
    if any(
        source_slots.get(slot_id, {}).get("kind") not in TEXT_KINDS for slot_id in roles
    ):
        raise ValueError(
            "원본에서 글자를 찾지 못했습니다. 원본 문항을 저장한 뒤 다시 적용하세요."
        )

    results = []
    for language in dict.fromkeys(languages):
        target_id = equivalents[language]
        result = {
            "language": language,
            "problem_id": target_id,
            "applied": 0,
            "missing": [],
            "saved": False,
        }
        try:
            slots = _effective_slots(target_id)
            result["missing"] = [
                slot_id
                for slot_id in roles
                if slots.get(slot_id, {}).get("kind") not in TEXT_KINDS
            ]
            patches = [
                {"target": slot_id, "op": "update", "value": {"semantic_role": role}}
                for slot_id, role in roles.items()
                if slot_id not in result["missing"]
            ]
            if patches:
                apply_layout_patches(
                    target_id, patches, format_source=False, fast_overrides=True
                )
                result.update(saved=True, applied=len(patches))
                built = run_problem_build(target_id)
                if not built.ok:
                    raise ValueError(
                        built.error
                        or "표시 위치는 저장했지만 미리보기 빌드에 실패했습니다."
                    )
            result["status"] = (
                "partial"
                if patches and result["missing"]
                else "success" if patches else "skipped"
            )
        except Exception as exc:
            result.update(status="error", error=str(exc))
        results.append(result)
    return results
