from __future__ import annotations

import importlib.util
import json
import time
import uuid
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from modu_math.dsl import (
    ProblemTemplate,
    compile_problem_template_to_layout,
    compile_problem_template_to_semantic,
)
from modu_math.layout.editor_overrides import (
    apply_editor_overrides,
    prune_deleted_legacy_answer_slots,
    prune_editor_overrides,
    prune_legacy_answer_blank_slots,
)
from modu_math.layout.sanitizer import sanitize_layout
from modu_math.pipeline.answer_contracts import (
    normalize_answer_for_deleted_slots,
    normalize_answer_for_submit_slots,
    validate_answer_slot_contract,
)
from modu_math.pipeline.semantic_normalizer import normalize_semantic_for_schema
from modu_math.pipeline.validate_contracts import (
    validate_semantic_solvable_answer_match,
)
from modu_math.pipeline.subproblem_projection import project_suffixed_subproblem
from modu_math.pipeline.tutor_renderer_flow import (
    attach_tutor_renderer_flow,
    validate_tutor_renderer_flow,
)
from modu_math.renderer.compiler import compile_renderer_json
from modu_math.renderer.svg.render import inline_local_image_hrefs, render_svg

from .problems import read_artifacts, resolve_problem_paths, validate_problem_id


@dataclass
class BuildResult:
    ok: bool
    stdout: str
    stderr: str
    error: str | None = None


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[4]


@lru_cache(maxsize=8)
def _schema_validator(relative_path: str) -> Draft202012Validator:
    schema_path = _repo_root() / relative_path
    schema = json.loads(schema_path.read_text(encoding="utf-8-sig"))
    return Draft202012Validator(schema)


def _load_dsl_module(dsl_path: Path) -> Any:
    module_name = f"modu_editor_build_{uuid.uuid4().hex}"
    spec = importlib.util.spec_from_file_location(module_name, dsl_path)
    if spec is None or spec.loader is None:
        raise ValueError(f"unable to load DSL file: {dsl_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _problem_template_from_module(module: Any, dsl_path: Path) -> ProblemTemplate:
    if hasattr(module, "PROBLEM_TEMPLATE") and isinstance(
        module.PROBLEM_TEMPLATE, ProblemTemplate
    ):
        return module.PROBLEM_TEMPLATE
    if hasattr(module, "build_problem_template"):
        problem = module.build_problem_template()
        if isinstance(problem, ProblemTemplate):
            return problem
    raise ValueError(
        f"DSL file {dsl_path} does not define PROBLEM_TEMPLATE or build_problem_template()"
    )


def _deep_merge_dict(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    out = dict(base)
    for key, value in override.items():
        if key in out and isinstance(out[key], dict) and isinstance(value, dict):
            out[key] = _deep_merge_dict(out[key], value)
        else:
            out[key] = value
    return out


def _parse_solvable_schema_tag(solvable: dict[str, Any]) -> str:
    schema_value = solvable.get("schema")
    if not isinstance(schema_value, str):
        raise ValueError(
            "SOLVABLE['schema'] must be a string like 'modu.solvable.v1.1', 'modu.solvable.v1.2', or 'modu.solvable.v1.3'."
        )
    prefix = "modu.solvable."
    if not schema_value.startswith(prefix):
        raise ValueError(f"Unsupported solvable schema format: {schema_value}")
    tag = schema_value[len(prefix) :]
    if not tag:
        raise ValueError(f"Invalid solvable schema tag: {schema_value}")
    return tag


def _normalize_solvable_for_schema(solvable: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(solvable)
    plan = normalized.get("plan")
    if isinstance(plan, str):
        normalized["plan"] = [plan]
    return normalized


def _submitted_answer_slot_ids(layout: dict[str, Any]) -> list[str]:
    return [slot["slot_id"] for slot in _submitted_answer_slots(layout)]


def _submitted_answer_slots(layout: dict[str, Any]) -> list[dict[str, Any]]:
    slots: list[dict[str, Any]] = []
    for slot in layout.get("slots", []):
        if not isinstance(slot, dict):
            continue
        slot_id = slot.get("id")
        content = slot.get("content")
        interaction = content.get("interaction") if isinstance(content, dict) else None
        if (
            isinstance(slot_id, str)
            and isinstance(interaction, dict)
            and interaction.get("role") == "answer"
            and interaction.get("type") == "input"
            and interaction.get("include_in_submission") is not False
        ):
            slots.append(
                {
                    "slot_id": slot_id,
                    "answer_key_index": interaction.get("answer_key_index"),
                    "answer_ref": interaction.get("answer_ref"),
                    "order": interaction.get("order"),
                }
            )
    return slots


def _answer_slot_ids(answer: Any) -> set[str]:
    if not isinstance(answer, dict):
        return set()
    out: set[str] = set()
    for key in ("blanks", "answer_key"):
        items = answer.get(key)
        if not isinstance(items, list):
            continue
        for item in items:
            if not isinstance(item, dict):
                continue
            slot_id = item.get("slot_id") or item.get("id") or item.get("blank_id")
            if isinstance(slot_id, str) and slot_id.strip():
                out.add(slot_id)
    return out


def _with_single_submit_slot_answer(answer: Any, slot_id: str) -> Any:
    if not isinstance(answer, dict):
        return answer
    value = answer.get("value")
    if not isinstance(value, str | int | float) or isinstance(value, bool):
        return answer
    if _answer_slot_ids(answer) == {slot_id}:
        return answer
    normalized = dict(answer)
    normalized["blanks"] = [{"id": slot_id, "slot_id": slot_id, "expected": value}]
    normalized["answer_key"] = [{"slot_id": slot_id, "value": value}]
    return normalized


def _attach_single_submit_slot_answer(
    *,
    layout: dict[str, Any],
    semantic: dict[str, Any],
    solvable: dict[str, Any] | None,
) -> tuple[dict[str, Any], dict[str, Any] | None]:
    submit_slot_ids = _submitted_answer_slot_ids(layout)
    if len(submit_slot_ids) != 1:
        return semantic, solvable
    slot_id = submit_slot_ids[0]
    semantic_answer = _with_single_submit_slot_answer(semantic.get("answer"), slot_id)
    if semantic_answer is not semantic.get("answer"):
        semantic = dict(semantic)
        semantic["answer"] = semantic_answer
    if isinstance(solvable, dict):
        solvable_answer = _with_single_submit_slot_answer(
            solvable.get("answer"), slot_id
        )
        if solvable_answer is not solvable.get("answer"):
            solvable = dict(solvable)
            solvable["answer"] = solvable_answer
    return semantic, solvable


def _attach_submit_slot_answers(
    *,
    layout: dict[str, Any],
    semantic: dict[str, Any],
    solvable: dict[str, Any] | None,
) -> tuple[dict[str, Any], dict[str, Any] | None]:
    submit_slots = _submitted_answer_slots(layout)
    if not submit_slots:
        return semantic, solvable

    semantic_answer, semantic_changed = normalize_answer_for_submit_slots(
        semantic.get("answer"),
        submit_slots,
    )
    if semantic_changed:
        semantic = dict(semantic)
        semantic["answer"] = semantic_answer

    if isinstance(solvable, dict):
        solvable_answer, solvable_changed = normalize_answer_for_submit_slots(
            solvable.get("answer"),
            submit_slots,
        )
        if solvable_changed:
            solvable = dict(solvable)
            solvable["answer"] = solvable_answer
    return semantic, solvable


def _build_problem_artifacts(problem_id: str) -> str:
    safe_problem_id = validate_problem_id(problem_id)
    problem_paths = resolve_problem_paths(safe_problem_id)
    module = _load_dsl_module(problem_paths.dsl_path)
    problem = _problem_template_from_module(module, problem_paths.dsl_path)

    semantic = compile_problem_template_to_semantic(
        problem, problem_type="diagram_problem"
    )
    layout = compile_problem_template_to_layout(problem)

    if hasattr(module, "SEMANTIC_OVERRIDE"):
        semantic_override = module.SEMANTIC_OVERRIDE
        if not isinstance(semantic_override, dict):
            raise ValueError("SEMANTIC_OVERRIDE must be a dict when provided.")
        semantic = _deep_merge_dict(semantic, semantic_override)

    if hasattr(module, "SEMANTIC_ANSWER"):
        semantic["answer"] = module.SEMANTIC_ANSWER

    solvable = None
    if hasattr(module, "SOLVABLE"):
        solvable = module.SOLVABLE
    elif hasattr(module, "build_solvable"):
        solvable = module.build_solvable()

    semantic, _semantic_normalized = normalize_semantic_for_schema(semantic)

    deleted_answer_slots: set[str] = set()
    editor_override_slot_ids: set[str] = set()
    editor_overrides_path = (
        problem_paths.base_dir / f"{problem_paths.artifact_base}.editor_overrides.json"
    )
    if editor_overrides_path.exists():
        editor_overrides = json.loads(
            editor_overrides_path.read_text(encoding="utf-8-sig")
        )
        editor_overrides, pruned = prune_editor_overrides(layout, editor_overrides)
        editor_overrides, answer_pruned = prune_deleted_legacy_answer_slots(
            layout,
            editor_overrides,
            semantic.get("answer"),
        )
        pruned = pruned or answer_pruned
        deleted_slots = (
            editor_overrides.get("deleted_slots")
            if isinstance(editor_overrides, dict)
            else None
        )
        override_slots = (
            editor_overrides.get("slots")
            if isinstance(editor_overrides, dict)
            else None
        )
        if isinstance(override_slots, dict):
            editor_override_slot_ids = {
                slot_id for slot_id in override_slots if isinstance(slot_id, str)
            }
        if isinstance(deleted_slots, list):
            deleted_answer_slots = {
                slot_id for slot_id in deleted_slots if isinstance(slot_id, str)
            }
        if pruned:
            editor_overrides_path.write_text(
                json.dumps(editor_overrides, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
        layout = apply_editor_overrides(layout, editor_overrides)

    layout, semantic, solvable, projected_deleted_slots = project_suffixed_subproblem(
        artifact_id=problem_paths.artifact_base,
        template_id=problem.id,
        layout=layout,
        semantic=semantic,
        solvable=solvable if isinstance(solvable, dict) else None,
        protected_slot_ids=editor_override_slot_ids,
    )
    deleted_answer_slots.update(projected_deleted_slots)

    layout, auto_deleted_answer_slots = prune_legacy_answer_blank_slots(
        layout, semantic.get("answer")
    )
    deleted_answer_slots.update(auto_deleted_answer_slots)
    layout = sanitize_layout(layout, deleted_slots=deleted_answer_slots)

    semantic, solvable = _attach_submit_slot_answers(
        layout=layout,
        semantic=semantic,
        solvable=solvable if isinstance(solvable, dict) else None,
    )
    semantic_answer, removed_semantic_answer_slots = normalize_answer_for_deleted_slots(
        semantic.get("answer"),
        deleted_answer_slots,
    )
    if removed_semantic_answer_slots:
        semantic = dict(semantic)
        semantic["answer"] = semantic_answer
    if isinstance(solvable, dict):
        solvable_answer, removed_solvable_answer_slots = (
            normalize_answer_for_deleted_slots(
                solvable.get("answer"),
                deleted_answer_slots,
            )
        )
        if removed_solvable_answer_slots:
            solvable = dict(solvable)
            solvable["answer"] = solvable_answer

    semantic, _semantic_normalized = normalize_semantic_for_schema(semantic)

    renderer = compile_renderer_json(layout)
    if hasattr(module, "TUTOR_RENDERER_FLOW"):
        renderer = attach_tutor_renderer_flow(renderer, module.TUTOR_RENDERER_FLOW)
    svg = inline_local_image_hrefs(render_svg(renderer), problem_paths.base_dir)

    _schema_validator("schema/semantic/semantic.v1.json").validate(semantic)
    _schema_validator("schema/layout/layout.v1.json").validate(layout)
    _schema_validator("schema/renderer/renderer.v1.json").validate(renderer)
    validate_tutor_renderer_flow(
        renderer, solvable if isinstance(solvable, dict) else None
    )

    if solvable:
        if not isinstance(solvable, dict):
            raise ValueError("SOLVABLE must be a dict when provided.")
        solvable = _normalize_solvable_for_schema(solvable)
        solvable, _solvable_normalized = normalize_semantic_for_schema(solvable)
        solvable_tag = _parse_solvable_schema_tag(solvable)
        schema_relative = f"schema/solvable/solvable.{solvable_tag}.json"
        schema_path = _repo_root() / schema_relative
        if not schema_path.exists():
            raise FileNotFoundError(
                f"Solvable schema file not found for '{solvable.get('schema')}': {schema_path}"
            )
        _schema_validator(schema_relative).validate(solvable)
        validate_semantic_solvable_answer_match(semantic, solvable)

    validate_answer_slot_contract(
        layout=layout,
        semantic=semantic,
        solvable=solvable if isinstance(solvable, dict) else None,
        deleted_slots=deleted_answer_slots,
    )

    problem_paths.artifact_path("semantic").write_text(
        json.dumps(semantic, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    problem_paths.artifact_path("layout").write_text(
        json.dumps(layout, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    problem_paths.artifact_path("renderer").write_text(
        json.dumps(renderer, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    problem_paths.artifact_path("svg").write_text(svg, encoding="utf-8")

    if solvable:
        solvable_tag = _parse_solvable_schema_tag(solvable)
        (
            problem_paths.base_dir
            / f"{problem_paths.artifact_base}.solvable.{solvable_tag}.json"
        ).write_text(
            json.dumps(solvable, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    return "build_ok"


def run_problem_build(problem_id: str) -> BuildResult:
    started = time.perf_counter()
    try:
        output = _build_problem_artifacts(problem_id)
    except Exception as exc:  # pragma: no cover
        return BuildResult(ok=False, stdout="", stderr="", error=str(exc))

    elapsed_ms = (time.perf_counter() - started) * 1000
    return BuildResult(
        ok=True,
        stdout=f"{output}\n[editor_build] {elapsed_ms:.0f} ms\n",
        stderr="",
        error=None,
    )


def build_with_artifacts(problem_id: str) -> tuple[BuildResult, dict[str, Any]]:
    result = run_problem_build(problem_id)
    artifacts = read_artifacts(problem_id)
    return result, artifacts
