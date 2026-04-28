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


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate generated problem.dsl.py by running existing modu_math build paths."
    )
    parser.add_argument("--dsl", required=True, help="Path to generated problem.dsl.py")
    parser.add_argument("--out-prefix", default=None, help="Output prefix path for generated artifacts")
    parser.add_argument("--strict", action="store_true", help="Enable strict cross-layer contract validation")
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
    ]
    return [str(path.resolve()) for path in candidates if path.exists()]


def _build_from_legacy_problem(problem: LegacyProblem, *, out_prefix: Path, strict: bool) -> None:
    # Reuse existing legacy build path; no execution of generated DSL beyond import/build object construction.
    problem.save(
        out_prefix,
        validate=bool(strict),
        cross_layer_validate=bool(strict),
        emit_semantic=False,
    )


def _build_from_problem_template(problem: ProblemTemplate, *, out_prefix: Path, strict: bool) -> None:
    semantic = compile_problem_template_to_semantic(problem)
    validate_semantic_json(semantic)

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


def _run_build(dsl_path: Path, out_prefix: Path, strict: bool) -> None:
    module = _load_module(dsl_path)
    problem_obj = _resolve_problem_object(module)
    if isinstance(problem_obj, LegacyProblem):
        _build_from_legacy_problem(problem_obj, out_prefix=out_prefix, strict=strict)
        return
    if isinstance(problem_obj, ProblemTemplate):
        _build_from_problem_template(problem_obj, out_prefix=out_prefix, strict=strict)
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
    }

    try:
        _run_build(dsl_path=dsl_path, out_prefix=out_prefix, strict=bool(args.strict))
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
