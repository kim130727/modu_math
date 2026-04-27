from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
from types import ModuleType
from typing import Any

from .adapters.dsl.legacy_problem import Problem as ModuMathProblem


def _load_module_from_python_file(path: str) -> ModuleType:
    path_obj = Path(path)
    spec = importlib.util.spec_from_file_location("user_problem_module", path_obj)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load module from {path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _is_supported_problem_instance(value: Any) -> bool:
    if isinstance(value, ModuMathProblem):
        return True
    # Backward compatibility: legacy archive Problem may still be returned.
    try:
        from modu_semantic_archive.problem import Problem as ArchiveProblem

        return isinstance(value, ArchiveProblem)
    except Exception:
        return False


def _load_problem_from_python_file(path: str) -> Any:
    module = _load_module_from_python_file(path)
    if not hasattr(module, "build"):
        raise RuntimeError("Input file must define a build() function returning Problem")

    problem = module.build()
    if not _is_supported_problem_instance(problem):
        raise RuntimeError("build() must return modu_math.Problem (or legacy compatible Problem)")
    return problem


def _add_build_parser(subparsers: Any) -> None:
    build_parser = subparsers.add_parser("build")
    build_parser.add_argument("input", help="Python file defining build() -> Problem")
    build_parser.add_argument("-o", "--out", required=True, help="Output prefix path")
    build_parser.add_argument("--no-validate", action="store_true")


def _add_build_semantic_parser(subparsers: Any) -> None:
    build_semantic_parser = subparsers.add_parser("build-semantic")
    build_semantic_parser.add_argument("input", help="semantic.json path")
    build_semantic_parser.add_argument("-o", "--out", required=True, help="Output prefix path")
    build_semantic_parser.add_argument("--no-input-validate", action="store_true")
    build_semantic_parser.add_argument("--no-output-validate", action="store_true")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="modu")
    subparsers = parser.add_subparsers(dest="command", required=True)

    _add_build_parser(subparsers)
    _add_build_semantic_parser(subparsers)
    args = parser.parse_args(argv)

    if args.command == "build":
        problem = _load_problem_from_python_file(args.input)
        try:
            problem.save(args.out, validate=not args.no_validate, emit_semantic=False)
        except TypeError as exc:
            raise RuntimeError(
                "This build path requires a modu_math.Problem instance so semantic output can remain untouched. "
                "Please return modu_math.Problem from build()."
            ) from exc
        return 0

    if args.command == "build-semantic":
        # Keep legacy semantic-json conversion behavior for compatibility.
        from modu_semantic_archive.semantic_json_builder import build_from_semantic_file

        build_from_semantic_file(
            input_semantic_path=args.input,
            out_prefix=args.out,
            emit_py_path=None,
            validate_input=not args.no_input_validate,
            validate_output=not args.no_output_validate,
        )
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
