from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path

from .problem import Problem


def _load_problem_from_python_file(path: str) -> Problem:
    path_obj = Path(path)
    spec = importlib.util.spec_from_file_location("user_problem_module", path_obj)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load module from {path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    if not hasattr(module, "build"):
        raise RuntimeError("Input file must define a build() function returning Problem")

    problem = module.build()
    if not isinstance(problem, Problem):
        raise RuntimeError("build() must return modu_semantic.Problem")
    return problem


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="modu")
    subparsers = parser.add_subparsers(dest="command", required=True)

    build_parser = subparsers.add_parser("build")
    build_parser.add_argument("input", help="Python file defining build() -> Problem")
    build_parser.add_argument("-o", "--out", required=True, help="Output prefix path")
    build_parser.add_argument("--no-validate", action="store_true")

    build_semantic_parser = subparsers.add_parser("build-semantic")
    build_semantic_parser.add_argument("input", help="semantic.json path")
    build_semantic_parser.add_argument("-o", "--out", required=True, help="Output prefix path")
    build_semantic_parser.add_argument(
        "--emit-py",
        help="Optional Python scaffold path (for semantic-json build replay)",
    )
    build_semantic_parser.add_argument("--no-input-validate", action="store_true")
    build_semantic_parser.add_argument("--no-output-validate", action="store_true")

    args = parser.parse_args(argv)

    if args.command == "build":
        problem = _load_problem_from_python_file(args.input)
        problem.save(args.out, validate=not args.no_validate)
    elif args.command == "build-semantic":
        from .semantic_json_builder import build_from_semantic_file

        build_from_semantic_file(
            input_semantic_path=args.input,
            out_prefix=args.out,
            emit_py_path=args.emit_py,
            validate_input=not args.no_input_validate,
            validate_output=not args.no_output_validate,
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
