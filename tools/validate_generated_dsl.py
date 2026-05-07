from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from types import ModuleType
from typing import Any

from modu_math.adapters.dsl.legacy_problem import Problem as LegacyProblem
from modu_math.dsl import ProblemTemplate, compile_problem_template_to_layout, compile_problem_template_to_semantic
from modu_math.layout.validate import validate_layout_json
from modu_math.pipeline.validate_contracts import validate_contract_bundle
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
        out_prefix.with_suffix(".solvable.v1.json"),
    ]
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


def _assert_semantic_override_required(module: ModuleType) -> None:
    value = getattr(module, "SEMANTIC_OVERRIDE", None)
    if not isinstance(value, dict):
        raise ValueError("DSL must define SEMANTIC_OVERRIDE as a dict.")
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
    if solvable.get("schema") != "modu.solvable.v1":
        raise ValueError("SOLVABLE.schema must be 'modu.solvable.v1'.")
    if solvable.get("problem_id") != problem_id:
        raise ValueError("SOLVABLE.problem_id must match semantic/problem id.")
    for key in ("plan", "steps", "checks"):
        value = solvable.get(key)
        if not isinstance(value, list) or not value:
            raise ValueError(f"SOLVABLE.{key} must be a non-empty array.")


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
) -> None:
    _assert_semantic_override_required(module)
    semantic = compile_problem_template_to_semantic(problem)
    if hasattr(module, "SEMANTIC_OVERRIDE") and isinstance(module.SEMANTIC_OVERRIDE, dict):
        semantic = _deep_merge_dict(semantic, module.SEMANTIC_OVERRIDE)
    if hasattr(module, "SEMANTIC_ANSWER") and isinstance(module.SEMANTIC_ANSWER, dict):
        merged_answer = dict(semantic.get("answer", {}))
        merged_answer.update(module.SEMANTIC_ANSWER)
        semantic["answer"] = merged_answer
    validate_semantic_json(semantic)
    _assert_semantic_concise(semantic)

    layout = compile_problem_template_to_layout(problem)
    validate_layout_json(layout)

    renderer = compile_renderer_json(layout)
    validate_renderer_json(renderer)

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

    if emit_solvable:
        solvable = _resolve_solvable_object(module)
        if not isinstance(solvable, dict):
            raise ValueError("DSL must define SOLVABLE dict or build_solvable() dict.")
        solvable_schema = json.loads(
            Path("schema/solvable/solvable.v1.json").read_text(encoding="utf-8-sig")
        )
        Draft202012Validator(solvable_schema).validate(solvable)
        _assert_solvable_enriched(solvable, str(semantic.get("problem_id", "")))
        out_prefix.with_suffix(".solvable.v1.json").write_text(
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


def _run_build(dsl_path: Path, out_prefix: Path, strict: bool, emit_solvable: bool) -> None:
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
        )
        return
    raise RuntimeError(
        f"Unsupported DSL return type: {type(problem_obj)!r}. "
        "Expected modu_math Problem or ProblemTemplate."
    )


def _write_report(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


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
        _run_build(
            dsl_path=dsl_path,
            out_prefix=out_prefix,
            strict=bool(args.strict),
            emit_solvable=bool(args.emit_solvable),
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
