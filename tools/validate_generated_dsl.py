from __future__ import annotations

import argparse
import importlib.util
import json
import re
from pathlib import Path
from types import ModuleType
from typing import Any

from modu_math.adapters.dsl.legacy_problem import Problem as LegacyProblem
from modu_math.dsl import ProblemTemplate, compile_problem_template_to_layout, compile_problem_template_to_semantic
from modu_math.layout.validate import validate_layout_json
from modu_math.pipeline.validate_contracts import (
    validate_contract_bundle,
)
from modu_math.renderer.compiler import compile_renderer_json
from modu_math.renderer.svg.render import render_svg
from modu_math.renderer.validate import validate_renderer_json
from modu_math.semantic.validate import validate_semantic_json
from jsonschema import Draft202012Validator


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate generated problem.dsl.py by running existing modu_math build paths."
    )
    parser.add_argument("--dsl", required=True, help="Path to generated problem.dsl.py")
    parser.add_argument("--out-prefix", default=None, help="Output prefix path for generated artifacts")
    parser.add_argument("--strict", action="store_true", help="Enable strict cross-layer contract validation")
    parser.add_argument(
        "--emit-solvable",
        action="store_true",
        help="Emit solvable JSON when DSL defines SOLVABLE or build_solvable().",
    )
    parser.add_argument(
        "--report",
        default=None,
        help="Path to JSON report (default: build_report.json next to --dsl)",
    )
    parser.add_argument(
        "--source-problem-json",
        default=None,
        help="Optional original source problem JSON path. Answer/explanation text from this JSON must not appear in layout/renderer.",
    )
    return parser.parse_args(argv)


def _load_module(path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location("generated_problem_dsl", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load DSL module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _default_out_prefix(dsl_path: Path) -> Path:
    name = dsl_path.name
    if name.endswith(".dsl.py"):
        return dsl_path.with_name(name[: -len(".dsl.py")])
    return dsl_path.with_suffix("")


def _collect_generated_files(out_prefix: Path) -> list[str]:
    candidates = [
        out_prefix.with_suffix(".semantic.json"),
        out_prefix.with_suffix(".layout.json"),
        out_prefix.with_suffix(".renderer.json"),
        out_prefix.with_suffix(".svg"),
    ]
    candidates.extend(sorted(out_prefix.parent.glob(f"{out_prefix.name}.solvable.v*.json")))
    return [str(path.resolve()) for path in candidates if path.exists()]


def _deep_merge_dict(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = dict(base)
    for key, value in override.items():
        if key in out and isinstance(out[key], dict) and isinstance(value, dict):
            out[key] = _deep_merge_dict(out[key], value)
            continue
        out[key] = value
    return out


def _resolve_solvable_object(module: ModuleType) -> dict[str, Any] | None:
    if hasattr(module, "SOLVABLE") and isinstance(module.SOLVABLE, dict):
        return module.SOLVABLE
    if hasattr(module, "build_solvable"):
        built = module.build_solvable()
        if isinstance(built, dict):
            return built
    return None


def _normalize_solvable_for_schema(solvable: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(solvable)
    plan = normalized.get("plan")
    if isinstance(plan, str):
        normalized["plan"] = [plan]
    return normalized


def _parse_solvable_schema_tag(solvable: dict[str, Any]) -> str:
    schema_value = solvable.get("schema")
    if not isinstance(schema_value, str):
        raise ValueError(
            "SOLVABLE['schema'] must be a string like 'modu.solvable.v1.1' or 'modu.solvable.v1.2'."
        )
    prefix = "modu.solvable."
    if not schema_value.startswith(prefix):
        raise ValueError(f"Unsupported solvable schema format: {schema_value}")
    tag = schema_value[len(prefix) :]
    if not tag:
        raise ValueError(f"Invalid solvable schema tag: {schema_value}")
    return tag


def _assert_semantic_override_required(module: ModuleType) -> None:
    value = getattr(module, "SEMANTIC_OVERRIDE", None)
    if not isinstance(value, dict):
        raise ValueError("DSL must define SEMANTIC_OVERRIDE as a dict.")
    problem_id = value.get("problem_id")
    if not isinstance(problem_id, str) or not problem_id.strip():
        raise ValueError("SEMANTIC_OVERRIDE must include non-empty 'problem_id'.")
    if not isinstance(value.get("domain"), dict):
        raise ValueError("SEMANTIC_OVERRIDE must include a 'domain' object.")
    if not isinstance(value.get("answer"), dict):
        raise ValueError("SEMANTIC_OVERRIDE must include an 'answer' object.")


def _assert_semantic_concise(semantic: dict[str, Any]) -> None:
    domain = semantic.get("domain")
    answer = semantic.get("answer")
    if not isinstance(domain, dict) or not isinstance(answer, dict):
        raise ValueError("semantic must contain object-valued 'domain' and 'answer'.")
    objects = domain.get("objects")
    if not isinstance(objects, list):
        raise ValueError("semantic.domain.objects must be an array.")
    slot_like = 0
    typed = 0
    for obj in objects:
        if not isinstance(obj, dict):
            continue
        obj_type = obj.get("type")
        if isinstance(obj_type, str):
            typed += 1
            if obj_type.endswith("_slot"):
                slot_like += 1
    if typed > 0 and slot_like / typed > 0.6:
        raise ValueError(
            "semantic appears slot-enumeration-heavy. Use concise domain/answer-centric semantics."
        )


def _assert_solvable_enriched(solvable: dict[str, Any], problem_id: str) -> None:
    schema = solvable.get("schema")
    if schema not in {"modu.solvable.v1.1", "modu.solvable.v1.2"}:
        raise ValueError("SOLVABLE.schema must be 'modu.solvable.v1.1' or 'modu.solvable.v1.2'.")
    if solvable.get("problem_id") != problem_id:
        raise ValueError("SOLVABLE.problem_id must match semantic/problem id.")
    if not isinstance(solvable.get("answer"), dict):
        raise ValueError("SOLVABLE.answer must be an object.")


def _assert_problem_template_strict(problem: ProblemTemplate) -> None:
    slot_ids = [slot.id for slot in problem.slots]
    slot_id_set = set(slot_ids)
    if len(slot_ids) != len(slot_id_set):
        seen: set[str] = set()
        duplicates: list[str] = []
        for slot_id in slot_ids:
            if slot_id in seen and slot_id not in duplicates:
                duplicates.append(slot_id)
            seen.add(slot_id)
        dup_text = ", ".join(sorted(duplicates))
        raise ValueError(f"Duplicate slot id(s) detected: {dup_text}")

    for region in problem.regions:
        unknown_slot_ids = [slot_id for slot_id in region.slot_ids if slot_id not in slot_id_set]
        if unknown_slot_ids:
            invalid = ", ".join(unknown_slot_ids)
            raise ValueError(
                f"region '{region.id}' references unknown slot_ids: {invalid}"
            )


def _assert_problem_id_consistency(
    *,
    template_problem_id: str,
    semantic: dict[str, Any],
    layout: dict[str, Any],
    renderer: dict[str, Any],
    solvable: dict[str, Any] | None,
    semantic_override_problem_id: Any | None,
) -> None:
    semantic_problem_id = semantic.get("problem_id")
    layout_problem_id = layout.get("problem_id")
    renderer_problem_id = renderer.get("problem_id")

    ids: list[tuple[str, Any]] = [
        ("ProblemTemplate.id", template_problem_id),
        ("semantic.problem_id", semantic_problem_id),
        ("layout.problem_id", layout_problem_id),
        ("renderer.problem_id", renderer_problem_id),
    ]
    if semantic_override_problem_id is not None:
        ids.append(("SEMANTIC_OVERRIDE.problem_id", semantic_override_problem_id))
    if solvable is not None:
        ids.append(("SOLVABLE.problem_id", solvable.get("problem_id")))

    invalid = [name for name, value in ids if not isinstance(value, str) or not value.strip()]
    if invalid:
        raise ValueError(f"Missing/invalid problem_id in: {', '.join(invalid)}")

    baseline = template_problem_id
    mismatches = [f"{name}={value}" for name, value in ids if value != baseline]
    if mismatches:
        raise ValueError(
            "problem_id mismatch detected. Expected all artifacts to match "
            f"'{baseline}': " + "; ".join(mismatches)
        )


def _assert_bundle_consistency(
    *,
    problem: ProblemTemplate,
    semantic_override: dict[str, Any],
    solvable: dict[str, Any] | None,
    layout: dict[str, Any],
) -> None:
    template_problem_id = problem.id
    override_problem_id = semantic_override.get("problem_id")
    if template_problem_id != override_problem_id:
        raise ValueError(
            "ProblemTemplate.id must match SEMANTIC_OVERRIDE.problem_id: "
            f"{template_problem_id!r} != {override_problem_id!r}"
        )

    if solvable is not None:
        solvable_problem_id = solvable.get("problem_id")
        if override_problem_id != solvable_problem_id:
            raise ValueError(
                "SEMANTIC_OVERRIDE.problem_id must match SOLVABLE.problem_id: "
                f"{override_problem_id!r} != {solvable_problem_id!r}"
            )

        override_answer = semantic_override.get("answer")
        solvable_answer = solvable.get("answer")
        if not isinstance(override_answer, dict) or not isinstance(solvable_answer, dict):
            raise ValueError("SEMANTIC_OVERRIDE.answer and SOLVABLE.answer must be objects.")
        if override_answer.get("value") != solvable_answer.get("value"):
            raise ValueError(
                "SEMANTIC_OVERRIDE.answer.value must match SOLVABLE.answer.value: "
                f"{override_answer.get('value')!r} != {solvable_answer.get('value')!r}"
            )

    slots = layout.get("slots")
    if not isinstance(slots, list):
        raise ValueError("layout.slots must be an array")
    layout_slot_ids = set()
    for idx, slot in enumerate(slots):
        if not isinstance(slot, dict):
            raise ValueError(f"layout.slots[{idx}] must be an object")
        slot_id = slot.get("id")
        if not isinstance(slot_id, str) or not slot_id.strip():
            raise ValueError(f"layout.slots[{idx}].id must be a non-empty string")
        layout_slot_ids.add(slot_id)

    for region in problem.regions:
        unknown_slot_ids = [slot_id for slot_id in region.slot_ids if slot_id not in layout_slot_ids]
        if unknown_slot_ids:
            invalid = ", ".join(unknown_slot_ids)
            raise ValueError(
                f"region '{region.id}' references slot_ids not present in layout.slots: {invalid}"
            )


def validate_required_layout_ids(semantic: dict[str, Any], layout: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    metadata = semantic.get("metadata")
    required_layout_ids = None
    if isinstance(metadata, dict):
        required_layout_ids = metadata.get("required_layout_ids")

    if required_layout_ids is None:
        return errors
    if not isinstance(required_layout_ids, list):
        return ["semantic.metadata.required_layout_ids must be an array"]

    slots = layout.get("slots")
    layout_slot_ids: set[str] = set()
    if isinstance(slots, list):
        for slot in slots:
            if isinstance(slot, dict):
                slot_id = slot.get("id")
                if isinstance(slot_id, str) and slot_id.strip():
                    layout_slot_ids.add(slot_id)

    missing_ids: list[str] = []
    for required_id in required_layout_ids:
        if not isinstance(required_id, str) or not required_id.strip():
            errors.append("semantic.metadata.required_layout_ids must contain non-empty strings")
            continue
        if required_id not in layout_slot_ids:
            missing_ids.append(required_id)
    if missing_ids:
        missing_text = ", ".join(missing_ids)
        errors.append(
            "semantic.metadata.required_layout_ids contains missing layout slot ids: "
            f"{missing_text}"
        )
    return errors


def _assert_layout_slot_count_close(problem: ProblemTemplate, layout: dict[str, Any]) -> None:
    dsl_slot_count = len(problem.slots)
    layout_slots = layout.get("slots")
    if not isinstance(layout_slots, list):
        raise ValueError("layout.slots must be an array")
    layout_slot_count = len(layout_slots)

    if dsl_slot_count == 0:
        if layout_slot_count != 0:
            raise ValueError("DSL has 0 slots but layout has non-zero slots")
        return

    diff = abs(dsl_slot_count - layout_slot_count)
    ratio = diff / dsl_slot_count
    if ratio > 0.2 and diff > 2:
        raise ValueError(
            "layout slot count deviates too much from DSL slot count: "
            f"dsl={dsl_slot_count}, layout={layout_slot_count}"
        )


def _build_from_legacy_problem(problem: LegacyProblem, *, out_prefix: Path, strict: bool) -> None:
    # Reuse existing legacy build path; no execution of generated DSL beyond import/build object construction.
    problem.save(
        out_prefix,
        validate=bool(strict),
        cross_layer_validate=bool(strict),
        emit_semantic=False,
    )


def _build_from_problem_template(
    problem: ProblemTemplate,
    *,
    out_prefix: Path,
    strict: bool,
    module: ModuleType,
    emit_solvable: bool,
    source_problem_json_path: Path | None = None,
) -> None:
    _assert_semantic_override_required(module)
    _assert_problem_template_strict(problem)
    semantic_override = module.SEMANTIC_OVERRIDE
    semantic = compile_problem_template_to_semantic(problem)
    if hasattr(module, "SEMANTIC_OVERRIDE") and isinstance(module.SEMANTIC_OVERRIDE, dict):
        semantic = _deep_merge_dict(semantic, semantic_override)
        override_answer = semantic_override.get("answer")
        if isinstance(override_answer, dict):
            # Treat answer override as authoritative to avoid mixed legacy/new answer shapes.
            semantic["answer"] = dict(override_answer)
    if hasattr(module, "SEMANTIC_ANSWER") and isinstance(module.SEMANTIC_ANSWER, dict):
        merged_answer = dict(semantic.get("answer", {}))
        merged_answer.update(module.SEMANTIC_ANSWER)
        semantic["answer"] = merged_answer
    validate_semantic_json(semantic)
    _assert_semantic_concise(semantic)

    layout = compile_problem_template_to_layout(problem)
    validate_layout_json(layout)
    _assert_layout_slot_count_close(problem, layout)
    required_layout_id_errors = validate_required_layout_ids(semantic, layout)
    if required_layout_id_errors:
        for error in required_layout_id_errors:
            print(f"Validation warning: {error}")
        if strict:
            raise ValueError("; ".join(required_layout_id_errors))

    renderer = compile_renderer_json(layout)
    validate_renderer_json(renderer)
    _assert_source_answer_not_in_layout_renderer(
        source_texts=_extract_source_answer_explanation_texts(source_problem_json_path),
        layout=layout,
        renderer=renderer,
    )

    solvable: dict[str, Any] | None = None
    if emit_solvable:
        solvable = _resolve_solvable_object(module)
        if not isinstance(solvable, dict):
            raise ValueError("DSL must define SOLVABLE dict or build_solvable() dict.")
        solvable = _normalize_solvable_for_schema(solvable)
        solvable_tag = _parse_solvable_schema_tag(solvable)
        solvable_schema_path = Path("schema/solvable") / f"solvable.{solvable_tag}.json"
        if not solvable_schema_path.exists():
            raise FileNotFoundError(
                f"Solvable schema file not found for '{solvable.get('schema')}': {solvable_schema_path}"
            )
        solvable_schema = json.loads(
            solvable_schema_path.read_text(encoding="utf-8-sig")
        )
        Draft202012Validator(solvable_schema).validate(solvable)
        _assert_solvable_enriched(solvable, str(semantic.get("problem_id", "")))
    _assert_bundle_consistency(
        problem=problem,
        semantic_override=semantic_override,
        solvable=solvable,
        layout=layout,
    )

    semantic_override_problem_id = None
    if hasattr(module, "SEMANTIC_OVERRIDE") and isinstance(module.SEMANTIC_OVERRIDE, dict):
        semantic_override_problem_id = module.SEMANTIC_OVERRIDE.get("problem_id")
    _assert_problem_id_consistency(
        template_problem_id=problem.id,
        semantic=semantic,
        layout=layout,
        renderer=renderer,
        solvable=solvable,
        semantic_override_problem_id=semantic_override_problem_id,
    )

    if strict:
        validate_contract_bundle(semantic, layout, renderer)

    out_prefix.parent.mkdir(parents=True, exist_ok=True)
    out_prefix.with_suffix(".semantic.json").write_text(
        json.dumps(semantic, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    out_prefix.with_suffix(".layout.json").write_text(
        json.dumps(layout, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    out_prefix.with_suffix(".renderer.json").write_text(
        json.dumps(renderer, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    out_prefix.with_suffix(".svg").write_text(render_svg(renderer), encoding="utf-8")

    if solvable is not None:
        solvable_tag = _parse_solvable_schema_tag(solvable)
        out_prefix.with_suffix(f".solvable.{solvable_tag}.json").write_text(
            json.dumps(solvable, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )


def _resolve_problem_object(module: ModuleType) -> Any:
    if hasattr(module, "build"):
        return module.build()
    if hasattr(module, "PROBLEM_TEMPLATE") and isinstance(module.PROBLEM_TEMPLATE, ProblemTemplate):
        return module.PROBLEM_TEMPLATE
    if hasattr(module, "build_problem_template"):
        return module.build_problem_template()
    raise RuntimeError(
        "DSL must expose one of: build() -> Problem, PROBLEM_TEMPLATE, or build_problem_template()."
    )


def _run_build(
    dsl_path: Path,
    out_prefix: Path,
    strict: bool,
    emit_solvable: bool,
    source_problem_json_path: Path | None = None,
) -> None:
    module = _load_module(dsl_path)
    problem_obj = _resolve_problem_object(module)
    if isinstance(problem_obj, LegacyProblem):
        _build_from_legacy_problem(problem_obj, out_prefix=out_prefix, strict=strict)
        return
    if isinstance(problem_obj, ProblemTemplate):
        _build_from_problem_template(
            problem_obj,
            out_prefix=out_prefix,
            strict=strict,
            module=module,
            emit_solvable=emit_solvable,
            source_problem_json_path=source_problem_json_path,
        )
        return
    raise RuntimeError(
        f"Unsupported DSL return type: {type(problem_obj)!r}. "
        "Expected modu_math Problem or ProblemTemplate."
    )


def _write_report(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def validate_answer_alignment_source(source_text: str) -> list[str]:
    errors: list[str] = []
    # Disallow reversing canonical ownership by copying SOLVABLE.answer into SEMANTIC_OVERRIDE.answer.
    forbidden_patterns = (
        r'SEMANTIC_OVERRIDE\["answer"\]\s*=\s*SOLVABLE\["answer"\]',
        r"SEMANTIC_OVERRIDE\['answer'\]\s*=\s*SOLVABLE\['answer'\]",
    )
    for pattern in forbidden_patterns:
        if re.search(pattern, source_text):
            errors.append(
                "Forbidden answer alignment detected: "
                "SEMANTIC_OVERRIDE['answer'] = SOLVABLE['answer'] is not allowed."
            )
            break
    return errors


def _extract_source_answer_explanation_texts(source_problem_json_path: Path | None) -> list[str]:
    if source_problem_json_path is None or not source_problem_json_path.exists():
        return []
    try:
        data = json.loads(source_problem_json_path.read_text(encoding="utf-8-sig"))
    except Exception:
        return []
    key_hint = ("answer", "해설", "설명", "풀이", "solution", "explain")
    out: list[str] = []

    def walk(node: Any, parent_key: str = "") -> None:
        if isinstance(node, dict):
            for k, v in node.items():
                walk(v, str(k))
        elif isinstance(node, list):
            for v in node:
                walk(v, parent_key)
        elif isinstance(node, (str, int, float, bool)):
            if parent_key and any(h in parent_key.lower() for h in key_hint):
                s = re.sub(r"\s+", " ", str(node)).strip()
                if len(s) >= 6:
                    out.append(s)

    walk(data)
    uniq: list[str] = []
    seen: set[str] = set()
    for s in out:
        if s not in seen:
            seen.add(s)
            uniq.append(s)
        if len(uniq) >= 30:
            break
    return uniq


def _assert_source_answer_not_in_layout_renderer(
    *,
    source_texts: list[str],
    layout: dict[str, Any],
    renderer: dict[str, Any],
) -> None:
    if not source_texts:
        return
    layout_blob = json.dumps(layout, ensure_ascii=False)
    renderer_blob = json.dumps(renderer, ensure_ascii=False)
    hits: list[str] = []
    for s in source_texts:
        if s in layout_blob or s in renderer_blob:
            hits.append(s)
    if hits:
        raise ValueError(
            "Source problem JSON answer/explanation text leaked into layout/renderer: "
            + "; ".join(hits[:3])
        )


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    dsl_path = Path(args.dsl)
    out_prefix = Path(args.out_prefix) if args.out_prefix else _default_out_prefix(dsl_path)
    report_path = Path(args.report) if args.report else dsl_path.with_name("build_report.json")

    if not dsl_path.exists():
        raise FileNotFoundError(f"DSL path does not exist: {dsl_path}")

    report: dict[str, Any] = {
        "dsl_path": str(dsl_path.resolve()),
        "out_prefix": str(out_prefix.resolve()),
        "success": False,
        "generated_files": [],
        "strict": bool(args.strict),
        "emit_solvable": bool(args.emit_solvable),
    }

    try:
        source_text = dsl_path.read_text(encoding="utf-8")
        source_errors = validate_answer_alignment_source(source_text)
        if source_errors:
            for error in source_errors:
                print(f"Validation warning: {error}")
            if args.strict:
                raise ValueError("; ".join(source_errors))
        _run_build(
            dsl_path=dsl_path,
            out_prefix=out_prefix,
            strict=bool(args.strict),
            emit_solvable=bool(args.emit_solvable),
            source_problem_json_path=Path(args.source_problem_json) if args.source_problem_json else None,
        )
        report["success"] = True
        report["generated_files"] = _collect_generated_files(out_prefix)
    except Exception as exc:
        report["error"] = {"type": type(exc).__name__, "message": str(exc)}
    finally:
        _write_report(report_path, report)

    if report["success"]:
        print(f"Build validation succeeded. Report: {report_path}")
        return 0

    print(f"Build validation failed. Report: {report_path}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
